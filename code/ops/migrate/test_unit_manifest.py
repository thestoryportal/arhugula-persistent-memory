"""Tests for unit_manifest: a read-only, no-follow, hashed re-inventory of one unit."""
from __future__ import annotations

import contextlib
import errno
import hashlib
import io
import json
import os
import shutil
import socket
import stat
import subprocess
import sys
import tempfile
import threading
import unittest
from pathlib import Path
from unittest import mock

import unit_manifest

TOOL = Path(unit_manifest.__file__).resolve()
SECRET = b"hf_SECRETTOKENBYTES0123456789"
GIT_ENV = {
    "PATH": os.environ.get("PATH", "/usr/bin:/bin"),
    "GIT_CONFIG_NOSYSTEM": "1",
    "GIT_CONFIG_GLOBAL": os.devnull,
    "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t",
}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(obj) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def git(cwd: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=cwd, env=GIT_ENV, check=True,
                          capture_output=True, text=True).stdout.strip()


def snapshot(top: Path) -> dict:
    """Every object under top (no-follow) with its identity, size, mtime and content hash."""
    out = {}
    for dirpath, dirnames, filenames in os.walk(top):
        for name in dirnames + filenames:
            p = os.path.join(dirpath, name)
            st = os.lstat(p)
            body = Path(p).read_bytes() if stat.S_ISREG(st.st_mode) else None
            out[p] = (st.st_mode, st.st_ino, st.st_size, st.st_mtime_ns, body and sha(body))
    return out


class Base(unittest.TestCase):
    def setUp(self):
        # Resolved: the tool refuses a root with a symlink component (macOS TMPDIR is under /var -> private/var).
        self.tmp = Path(tempfile.mkdtemp(prefix="um")).resolve()
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.unit = self.tmp / "unit"
        self.unit.mkdir()
        self.out = self.tmp / "manifest.json"

    def run_cli(self, *extra: str, root: Path | None = None, out: Path | None = None, env: dict | None = None):
        proc = subprocess.run(
            [sys.executable, "-B", str(TOOL), "--root", str(root or self.unit), "--out", str(out or self.out), *extra],
            capture_output=True, timeout=60, stdin=subprocess.DEVNULL, env=env)
        return proc

    def patched_inproc(self, name: str, hook):
        """Run main in-process with os.<name> wrapped: hook(path_or_fd, result) runs after the real call."""
        real = getattr(os, name)

        def wrapper(*args, **kwargs):
            result = real(*args, **kwargs)
            hook(args[0], result)
            return result

        with mock.patch.object(unit_manifest.os, name, side_effect=wrapper):
            return self.run_inproc()

    def patched_before(self, name: str, hook):
        """Run main in-process with os.<name> wrapped: hook(*args) runs before the real call."""
        real = getattr(os, name)

        def wrapper(*args, **kwargs):
            hook(*args)
            return real(*args, **kwargs)

        with mock.patch.object(unit_manifest.os, name, side_effect=wrapper):
            return self.run_inproc()

    def bind_socket(self, path: Path) -> None:
        """Bind an AF_UNIX socket at path through a short alias, so a long TMPDIR stays under the 104-byte limit."""
        short = Path(tempfile.mkdtemp(prefix="um", dir="/private/tmp"))
        self.addCleanup(shutil.rmtree, short, True)
        os.symlink(path.parent, short / "d")
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.addCleanup(sock.close)
        sock.bind(str(short / "d" / path.name))
        self.assertTrue(stat.S_ISSOCK(os.lstat(path).st_mode))

    def assert_json_fail(self, code: int, out: str, needle: str, err: str = ""):
        self.assertEqual(code, 1, out + err)
        lines = out.splitlines()
        self.assertEqual(len(lines), 1, out + err)
        result = json.loads(lines[0])
        self.assertEqual(result["status"], "FAIL")
        self.assertIn(needle, result["reason"])
        return result

    def run_inproc(self):
        buf_out, buf_err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(buf_out), contextlib.redirect_stderr(buf_err):
            code = unit_manifest.main(["--root", str(self.unit), "--out", str(self.out)])
        return code, buf_out.getvalue(), buf_err.getvalue()


class ManifestContent(Base):
    def build_fixture(self):
        u = self.unit
        self.outside = self.tmp / "outside"
        self.outside.mkdir()
        (self.outside / "secret.txt").write_bytes(SECRET)
        files = {
            "a.txt": b"alpha\n",
            "B.bin": bytes(range(256)),
            "z-y": b"dash",
            "z/x": b"slash",
            "sub/é.txt": "été".encode(),
            "new\nline.txt": b"newline name",
            ".hf_token": SECRET,
        }
        for rel, body in files.items():
            (u / rel).parent.mkdir(parents=True, exist_ok=True)
            (u / rel).write_bytes(body)
        os.link(u / "a.txt", u / "hard")
        os.symlink("../outside", u / "dirlink")
        os.symlink("a.txt", u / "filelink")
        self.bind_socket(u / "sock")
        return files

    def test_manifest_is_sorted_hashed_canonical_and_no_follow(self):
        files = self.build_fixture()
        before_unit = snapshot(self.unit)
        before_outside = snapshot(self.outside)
        before_tmp = sorted(os.listdir(self.tmp))

        proc = self.run_cli()
        self.assertEqual(proc.returncode, 0, proc.stderr.decode(errors="replace"))
        raw = self.out.read_bytes()
        doc = json.loads(raw)

        # Canonical bytes, no trailing newline, digest over the complete file.
        self.assertEqual(raw, canonical(doc))
        self.assertFalse(raw.endswith(b"\n"))
        result = json.loads(proc.stdout)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["sha256"], sha(raw))
        self.assertEqual(result["manifest"], str(self.out))

        self.assertEqual(doc["schema_version"], 1)
        self.assertEqual(doc["root"], str(self.unit))
        self.assertEqual(doc["git_roots"], [])
        leaves = doc["leaves"]
        rels = [leaf["source"][len(str(self.unit)) + 1:] for leaf in leaves]
        # UTF-8 byte order: "B" < "a"; "z-y" (0x2d) < "z/x" (0x2f); "é" bytes after ASCII.
        self.assertEqual(rels, [".hf_token", "B.bin", "a.txt", "dirlink", "filelink", "hard",
                                "new\nline.txt", "sock", "sub/é.txt", "z-y", "z/x"])
        for leaf in leaves:
            self.assertEqual(sorted(leaf), ["bytes", "device", "inode", "kind", "link_text", "nlink", "sha256", "source"])
        by = dict(zip(rels, leaves))

        for rel, body in files.items():
            st = os.lstat(self.unit / rel)
            self.assertEqual(by[rel]["kind"], "file")
            self.assertEqual(by[rel]["bytes"], len(body))
            self.assertEqual(by[rel]["sha256"], sha(body))
            self.assertIsNone(by[rel]["link_text"])
            self.assertEqual((by[rel]["device"], by[rel]["inode"]), (st.st_dev, st.st_ino))

        # Hard link: same device/inode, nlink 2 on both names.
        self.assertEqual((by["hard"]["device"], by["hard"]["inode"]), (by["a.txt"]["device"], by["a.txt"]["inode"]))
        self.assertEqual(by["hard"]["nlink"], 2)
        self.assertEqual(by["a.txt"]["nlink"], 2)
        self.assertEqual(by["B.bin"]["nlink"], 1)

        # Symlinks are recorded as links and never followed.
        for rel, text in (("dirlink", "../outside"), ("filelink", "a.txt")):
            self.assertEqual(by[rel]["kind"], "symlink")
            self.assertEqual(by[rel]["link_text"], text)
            self.assertEqual(by[rel]["sha256"], sha(text.encode()))
            self.assertEqual(by[rel]["bytes"], len(text.encode()))
            self.assertEqual(by[rel]["inode"], os.lstat(self.unit / rel).st_ino)
        self.assertFalse(any(r.startswith("dirlink/") for r in rels))

        # Socket is recorded, not opened.
        self.assertEqual(by["sock"]["kind"], "socket")
        self.assertEqual(by["sock"]["bytes"], 0)
        self.assertEqual(by["sock"]["sha256"], sha(b""))
        self.assertIsNone(by["sock"]["link_text"])

        # No credential bytes on stdout or stderr; the outside secret never enters the manifest.
        self.assertNotIn(SECRET, proc.stdout)
        self.assertNotIn(SECRET, proc.stderr)
        self.assertNotIn(SECRET, raw)

        # Read only: unit and outside untouched; the only new object is the output path.
        self.assertEqual(snapshot(self.unit), before_unit)
        self.assertEqual(snapshot(self.outside), before_outside)
        self.assertEqual(sorted(os.listdir(self.tmp)), sorted(before_tmp + ["manifest.json"]))

    def test_same_tree_gives_same_digest(self):
        (self.unit / "f").write_bytes(b"x")
        first = self.run_cli()
        second = self.run_cli(out=self.tmp / "again.json")
        self.assertEqual(first.returncode, 0)
        self.assertEqual(second.returncode, 0)
        self.assertEqual(json.loads(first.stdout)["sha256"], json.loads(second.stdout)["sha256"])


class ChangedDuringHash(Base):
    """Mutate the file right after the tool opened it and began reading; the run must exit 1 and write nothing."""

    def setUp(self):
        super().setUp()
        self.target = self.unit / "data.bin"
        self.target.write_bytes(b"0123456789" * 1000)
        (self.unit / "other").write_bytes(b"keep")
        self.st = os.lstat(self.target)

    def run_with_mutation(self, mutate):
        real_read = os.read
        done = []

        def read(fd, n):
            if not done and os.fstat(fd).st_ino == self.st.st_ino:
                done.append(True)
                mutate()
            return real_read(fd, n)

        with mock.patch.object(unit_manifest.os, "read", side_effect=read):
            code, out, err = self.run_inproc()
        self.assertTrue(done, "the mutation hook never fired: the tool did not read the file")
        self.assertEqual(code, 1, out + err)
        self.assertEqual(json.loads(out)["status"], "FAIL")
        self.assertIn("data.bin", json.loads(out)["reason"])
        self.assertFalse(os.path.lexists(self.out))

    def test_size_change_only(self):
        def mutate():
            with open(self.target, "ab") as fh:
                fh.write(b"X")
            os.utime(self.target, ns=(self.st.st_atime_ns, self.st.st_mtime_ns))
            now = os.lstat(self.target)
            assert (now.st_ino, now.st_mtime_ns) == (self.st.st_ino, self.st.st_mtime_ns)
        self.run_with_mutation(mutate)

    def test_mtime_change_only(self):
        def mutate():
            os.utime(self.target, ns=(self.st.st_atime_ns, self.st.st_mtime_ns + 7_000_000_000))
        self.run_with_mutation(mutate)

    def test_inode_change_only(self):
        def mutate():
            repl = self.tmp / "repl.bin"
            repl.write_bytes(b"9876543210" * 1000)
            os.utime(repl, ns=(self.st.st_atime_ns, self.st.st_mtime_ns))
            os.replace(repl, self.target)
            now = os.lstat(self.target)
            assert (now.st_size, now.st_mtime_ns) == (self.st.st_size, self.st.st_mtime_ns)
            assert now.st_ino != self.st.st_ino
        self.run_with_mutation(mutate)

    def swap_after_lstat(self, make):
        fired = []

        def hook(path, _result):
            if not fired and os.fspath(path) == str(self.target):
                fired.append(True)
                os.replace(self.target, self.tmp / "moved-away.bin")
                make(str(self.target))
        return fired, hook

    def test_symlink_swapped_in_after_lstat_is_not_followed(self):
        (self.tmp / "lure.bin").write_bytes(b"lure")
        fired, hook = self.swap_after_lstat(lambda p: os.symlink(self.tmp / "lure.bin", p))
        code, out, err = self.patched_inproc("lstat", hook)
        self.assertTrue(fired)
        self.assertEqual(code, 1, out + err)
        # Refused at open (no-follow), not merely by the later identity recheck.
        self.assertIn("symbolic links", json.loads(out)["reason"])
        self.assertFalse(os.path.lexists(self.out))

    def test_fifo_swapped_in_after_lstat_does_not_block(self):
        fired, hook = self.swap_after_lstat(os.mkfifo)
        result = {}

        def body():
            result["r"] = self.patched_inproc("lstat", hook)

        worker = threading.Thread(target=body, daemon=True)
        worker.start()
        worker.join(20)
        if worker.is_alive():  # unblock the stuck open() so the thread can finish
            fd = os.open(self.target, os.O_WRONLY | os.O_NONBLOCK)
            os.close(fd)
            worker.join(20)
            self.fail("open() blocked on a FIFO swapped in after lstat")
        code, out, err = result["r"]
        self.assertEqual(code, 1, out + err)
        self.assertIn("changed kind", json.loads(out)["reason"])
        self.assertFalse(os.path.lexists(self.out))

    def test_symlink_retargeted_during_readlink_is_refused(self):
        os.symlink("other", self.unit / "ln")

        def hook(path, _result):
            if os.fspath(path) == str(self.unit / "ln"):
                tmp_link = self.tmp / "ln2"
                os.symlink("data.bin-much-longer-text", tmp_link)
                os.replace(tmp_link, self.unit / "ln")
        code, out, err = self.patched_inproc("readlink", hook)
        self.assertEqual(code, 1, out + err)
        self.assertIn("changed during hash", json.loads(out)["reason"])
        self.assertFalse(os.path.lexists(self.out))

    def test_output_created_during_walk_is_never_overwritten(self):
        def hook(path, _result):
            if os.fspath(path) == str(self.target) and not os.path.lexists(self.out):
                self.out.write_bytes(b"someone else's file, longer than nothing")
        code, out, err = self.patched_inproc("lstat", hook)
        self.assertEqual(code, 2, out + err)
        self.assertEqual(self.out.read_bytes(), b"someone else's file, longer than nothing")

    def test_unchanged_file_passes_same_path(self):
        code, out, err = self.run_inproc()
        self.assertEqual(code, 0, out + err)
        self.assertTrue(self.out.exists())


class NestedRepo(Base):
    def make_repo(self) -> Path:
        repo = self.unit / "inner"
        repo.mkdir()
        git(repo, "init", "-q", "-b", "main")
        (repo / "tracked.txt").write_bytes(b"v1\n")
        git(repo, "add", "tracked.txt")
        git(repo, "commit", "-q", "-m", "c1")
        return repo

    def test_nested_repo_records_head_branch_and_dirty_state(self):
        repo = self.make_repo()
        (repo / "tracked.txt").write_bytes(b"v2 changed\n")
        (repo / "untracked.txt").write_bytes(b"new\n")
        head = git(repo, "rev-parse", "HEAD")
        index_before = (repo / ".git" / "index").read_bytes()
        before = snapshot(self.unit)

        proc = self.run_cli()
        self.assertEqual(proc.returncode, 0, proc.stderr.decode(errors="replace"))
        doc = json.loads(self.out.read_bytes())
        self.assertEqual(doc["git_roots"], [{
            "path": str(repo),
            "head": head,
            "branch": "refs/heads/main",
            "dirty": [" M tracked.txt", "?? untracked.txt"],
        }])
        sources = [leaf["source"] for leaf in doc["leaves"]]
        self.assertIn(str(repo / ".git" / "HEAD"), sources)
        self.assertIn(str(repo / "untracked.txt"), sources)
        # Read only: the nested index and every other byte are unchanged.
        self.assertEqual((repo / ".git" / "index").read_bytes(), index_before)
        self.assertEqual(snapshot(self.unit), before)

    def test_clean_detached_repo(self):
        repo = self.make_repo()
        head = git(repo, "rev-parse", "HEAD")
        git(repo, "checkout", "-q", "--detach")
        proc = self.run_cli()
        self.assertEqual(proc.returncode, 0, proc.stderr.decode(errors="replace"))
        roots = json.loads(self.out.read_bytes())["git_roots"]
        self.assertEqual(roots, [{"path": str(repo), "head": head, "branch": None, "dirty": []}])

    def test_git_roots_sorted_by_utf8_bytes_and_unborn_head_is_null(self):
        for rel in ("r/s", "r-t"):
            (self.unit / rel).mkdir(parents=True)
            git(self.unit / rel, "init", "-q", "-b", "main")
        proc = self.run_cli()
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        roots = json.loads(self.out.read_bytes())["git_roots"]
        # "r-t" (0x2d) sorts before "r/s" (0x2f); a component-wise walk order would put r/s first.
        self.assertEqual(roots, [
            {"path": str(self.unit / "r-t"), "head": None, "branch": "refs/heads/main", "dirty": []},
            {"path": str(self.unit / "r/s"), "head": None, "branch": "refs/heads/main", "dirty": []},
        ])

    def assert_refused(self, proc, needle: str):
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        result = json.loads(proc.stdout)
        self.assertEqual(result["status"], "FAIL")
        self.assertIn(needle, result["reason"])
        self.assertFalse(os.path.lexists(self.out))

    def test_gitfile_link_is_refused(self):
        other = self.tmp / "elsewhere.git"
        other.mkdir()
        (self.unit / "wt").mkdir()
        (self.unit / "wt" / ".git").write_bytes(b"gitdir: " + str(other).encode() + b"\n")
        self.assert_refused(self.run_cli(), "wt/.git")

    def test_alternates_link_is_refused(self):
        repo = self.make_repo()
        (repo / ".git" / "objects" / "info" / "alternates").write_bytes(str(self.tmp).encode() + b"\n")
        self.assert_refused(self.run_cli(), "alternates")

    def test_commondir_link_is_refused(self):
        repo = self.make_repo()
        (repo / ".git" / "commondir").write_bytes(str(self.tmp).encode() + b"\n")
        self.assert_refused(self.run_cli(), "commondir")

    def test_broken_nested_git_never_reports_the_enclosing_repo(self):
        git(self.tmp, "init", "-q", "-b", "outer")
        (self.unit / "broken" / ".git").mkdir(parents=True)
        self.assert_refused(self.run_cli(), "broken")

    def test_caller_and_user_git_config_are_ignored(self):
        repo = self.make_repo()
        home = self.tmp / "home"
        home.mkdir()
        (home / ".gitconfig").write_bytes(b"[filter \"lfs\"]\n\tclean = git-lfs clean -- %f\n")
        env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
        env["HOME"] = str(home)
        env.update(GIT_CONFIG_COUNT="1", GIT_CONFIG_KEY_0="filter.caller.clean", GIT_CONFIG_VALUE_0="cat")
        proc = self.run_cli(env=env)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        roots = json.loads(self.out.read_bytes())["git_roots"]
        self.assertEqual([r["path"] for r in roots], [str(repo)])

    def test_fsmonitor_hook_is_not_run(self):
        repo = self.make_repo()
        marker = self.tmp / "fsmonitor-ran"
        hook = self.tmp / "fsmon.sh"
        hook.write_bytes(f"#!/bin/sh\ntouch '{marker}'\nexit 1\n".encode())
        hook.chmod(0o755)
        git(repo, "config", "core.fsmonitor", str(hook))
        # MAESTRO follow-up A: a core.fsmonitor key is now refused before any git call.
        self.assert_refused(self.run_cli(), "core.fsmonitor")
        self.assertFalse(marker.exists())

    def test_filter_driver_is_refused_and_not_run(self):
        repo = self.make_repo()
        marker = self.tmp / "filter-ran"
        git(repo, "config", "filter.evil.clean", f"touch {marker}; cat")
        (repo / ".gitattributes").write_bytes(b"*.txt filter=evil\n")
        (repo / "tracked.txt").write_bytes(b"v3\n")
        self.assert_refused(self.run_cli(), "filter")
        self.assertFalse(marker.exists())


class Refusals(Base):
    def test_fifo_is_refused_without_blocking(self):
        (self.unit / "f").write_bytes(b"x")
        os.mkfifo(self.unit / "pipe")
        proc = self.run_cli()
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        self.assertIn("pipe", json.loads(proc.stdout)["reason"])
        self.assertFalse(os.path.lexists(self.out))

    def test_existing_output_is_never_overwritten(self):
        (self.unit / "f").write_bytes(b"x")
        self.out.write_bytes(b"previous")
        proc = self.run_cli()
        self.assertEqual(proc.returncode, 2)
        self.assertEqual(self.out.read_bytes(), b"previous")

    def test_existing_output_is_refused_before_the_walk(self):
        os.mkfifo(self.unit / "pipe")  # the walk would refuse this with exit 1
        self.out.write_bytes(b"previous")
        proc = self.run_cli()
        self.assertEqual(proc.returncode, 2, proc.stdout + proc.stderr)
        self.assertEqual(proc.stdout, b"")

    def test_unreadable_directory_is_a_json_fail(self):
        locked = self.unit / "locked"
        locked.mkdir()
        locked.chmod(0)
        self.addCleanup(locked.chmod, 0o755)
        proc = self.run_cli()
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        result = json.loads(proc.stdout)
        self.assertEqual(result["status"], "FAIL")
        self.assertIn("locked", result["reason"])
        self.assertFalse(os.path.lexists(self.out))

    def test_output_inside_unit_is_refused(self):
        (self.unit / "f").write_bytes(b"x")
        before = snapshot(self.unit)
        proc = self.run_cli(out=self.unit / "m.json")
        self.assertEqual(proc.returncode, 2)
        self.assertEqual(snapshot(self.unit), before)

    def test_symlinked_root_is_refused(self):
        (self.unit / "f").write_bytes(b"x")
        link = self.tmp / "rootlink"
        os.symlink(self.unit, link)
        proc = self.run_cli(root=link)
        self.assertEqual(proc.returncode, 2)
        self.assertFalse(os.path.lexists(self.out))

    def test_dangling_output_symlink_is_not_followed(self):
        (self.unit / "f").write_bytes(b"x")
        target = self.tmp / "landing.json"
        os.symlink(target, self.out)
        proc = self.run_cli()
        self.assertEqual(proc.returncode, 2)
        self.assertFalse(os.path.lexists(target))


class OtherDevice:
    """A stat result for the same inode number on another device: the witness for the device component."""

    def __init__(self, st):
        self._st = st

    def __getattr__(self, name):
        return getattr(self._st, name)

    @property
    def st_dev(self):
        return self._st.st_dev + 1


def basename_is(path, name: str) -> bool:
    return not isinstance(path, int) and os.path.basename(os.fspath(path)) == name


class Traversal(Base):
    """Ruling 1: descend only through directory fds, never through a link, and refuse a linked root ancestor."""

    def setUp(self):
        super().setUp()
        self.child = self.unit / "child"
        self.child.mkdir()
        (self.child / "in.txt").write_bytes(b"inside")
        self.outside = self.tmp / "outside"
        self.outside.mkdir()
        (self.outside / "secret.txt").write_bytes(SECRET)

    def swap_child_before_open(self, make):
        fired = []

        def hook(path, *rest):
            if not fired and basename_is(path, "child"):
                fired.append(True)
                os.rename(self.child, self.tmp / "moved-child")
                make()
        code, out, err = self.patched_before("open", hook)
        self.assertTrue(fired, "the tool never opened the directory by name: it did not descend through an fd")
        self.assertNotIn(SECRET.decode(), out + err)
        self.assertFalse(os.path.lexists(self.out))
        return code, out, err

    def test_directory_swapped_for_a_symlink_is_not_followed(self):
        code, out, err = self.swap_child_before_open(lambda: os.symlink(self.outside, self.child))
        # Refused by the no-follow open itself, not only by the identity check after it.
        self.assert_json_fail(code, out, os.strerror(errno.ENOTDIR), err)

    def test_directory_replaced_by_another_directory_is_refused(self):
        code, out, err = self.swap_child_before_open(lambda: os.rename(self.outside, self.child))
        self.assertIn("child", self.assert_json_fail(code, out, "changed during walk", err)["reason"])

    def test_root_with_a_symlinked_ancestor_is_a_json_fail(self):
        alias = self.tmp / "alias"
        os.symlink(self.tmp, alias)
        proc = self.run_cli(root=alias / "unit")
        self.assert_json_fail(proc.returncode, proc.stdout.decode(), "symlink", proc.stderr.decode())
        self.assertFalse(os.path.lexists(self.out))


class LeafIdentity(Base):
    """Ruling 1: a leaf is read through its directory fd and must stay the scanned object before and after the read."""

    def setUp(self):
        super().setUp()
        self.target = self.unit / "data.bin"
        self.target.write_bytes(b"0123456789" * 1000)
        self.st = os.lstat(self.target)

    def test_file_replaced_before_open_is_refused_before_any_read(self):
        new = b"NEW_UNADMITTED_" * 700
        fired, reads = [], []

        def hook(path, *rest):
            if not fired and basename_is(path, "data.bin"):
                fired.append(True)
                repl = self.tmp / "repl.bin"
                repl.write_bytes(new)
                os.replace(repl, self.target)
        real_read = os.read

        def read(fd, n):
            data = real_read(fd, n)
            reads.append(data)
            return data
        with mock.patch.object(unit_manifest.os, "read", side_effect=read):
            code, out, err = self.patched_before("open", hook)
        self.assertTrue(fired)
        self.assert_json_fail(code, out, "data.bin", err)
        self.assertFalse(any(b"NEW_UNADMITTED_" in data for data in reads), "read the replacement before refusing")
        self.assertFalse(os.path.lexists(self.out))

    def test_change_seen_only_by_the_after_read_fstat_is_refused(self):
        real_read, real_fstat = os.read, os.fstat
        state = {"appended": False, "fstats": 0}

        def read(fd, n):
            if not state["appended"] and real_fstat(fd).st_ino == self.st.st_ino:
                state["appended"] = True
                with open(self.target, "ab") as fh:
                    fh.write(b"X")
                os.utime(self.target, ns=(self.st.st_atime_ns, self.st.st_mtime_ns))
            return real_read(fd, n)

        def fstat(fd):
            result = real_fstat(fd)
            if result.st_ino == self.st.st_ino:
                state["fstats"] += 1
                if state["fstats"] == 2:  # after the read: restore size and mtime before any later check
                    os.truncate(self.target, self.st.st_size)
                    os.utime(self.target, ns=(self.st.st_atime_ns, self.st.st_mtime_ns))
            return result
        with mock.patch.object(unit_manifest.os, "read", side_effect=read), \
                mock.patch.object(unit_manifest.os, "fstat", side_effect=fstat):
            code, out, err = self.run_inproc()
        self.assertTrue(state["appended"])
        self.assertEqual(state["fstats"], 2)
        self.assert_json_fail(code, out, "data.bin", err)
        self.assertFalse(os.path.lexists(self.out))

    def test_opened_file_on_another_device_is_refused(self):
        real_fstat = os.fstat
        forged = []

        def fstat(fd):
            result = real_fstat(fd)
            if not forged and result.st_ino == self.st.st_ino:
                forged.append(True)
                return OtherDevice(result)
            return result
        with mock.patch.object(unit_manifest.os, "fstat", side_effect=fstat):
            code, out, err = self.run_inproc()
        self.assertTrue(forged)
        self.assert_json_fail(code, out, "data.bin", err)
        self.assertFalse(os.path.lexists(self.out))


class NestedRepoInputs(Base):
    """Ruling 2 and guard coverage: Git reads nothing outside the unit and every Git failure refuses."""

    def make_repo(self) -> Path:
        return NestedRepo.make_repo(self)

    def assert_refused(self, proc, needle: str):
        NestedRepo.assert_refused(self, proc, needle)

    def link_inside_git(self, rel: str):
        repo = self.make_repo()
        link = repo / ".git" / rel
        external = self.tmp / "external"
        source = link if link.exists() else repo / ".git" / "refs" / "heads" / "main"
        external.write_bytes(source.read_bytes())
        if link.exists():
            link.unlink()
        os.symlink(external, link)
        self.assert_refused(self.run_cli(), f".git/{rel}")

    def test_config_symlink_inside_nested_git_is_refused(self):
        self.link_inside_git("config")

    def test_deep_symlink_inside_nested_git_is_refused(self):
        self.link_inside_git("refs/heads/evil")

    def test_socket_inside_nested_git_is_refused(self):
        repo = self.make_repo()
        self.bind_socket(repo / ".git" / "fsmonitor--daemon.ipc")
        self.assert_refused(self.run_cli(), "fsmonitor--daemon.ipc")

    def fake_git_env(self, subcommand: str, code: int, message: str) -> dict:
        real = shutil.which("git")
        bindir = self.tmp / "fakebin"
        bindir.mkdir()
        script = bindir / "git"
        script.write_text(f'#!/bin/sh\nfor a in "$@"; do\n  if [ "$a" = "{subcommand}" ]; then\n'
                          f'    echo "{message}" >&2\n    exit {code}\n  fi\ndone\nexec "{real}" "$@"\n')
        script.chmod(0o755)
        return dict(os.environ, PATH=f"{bindir}{os.pathsep}{os.environ.get('PATH', '')}")

    def test_rev_parse_error_is_refused(self):
        self.make_repo()
        self.assert_refused(self.run_cli(env=self.fake_git_env("rev-parse", 128, "fatal: injected")), "rev-parse")

    def test_rev_parse_exit_1_with_stderr_is_refused(self):
        self.make_repo()
        self.assert_refused(self.run_cli(env=self.fake_git_env("rev-parse", 1, "warning: injected")), "rev-parse")

    def test_symbolic_ref_error_is_refused(self):
        self.make_repo()
        self.assert_refused(self.run_cli(env=self.fake_git_env("symbolic-ref", 128, "fatal: injected")),
                            "symbolic-ref")

    def test_status_error_is_refused(self):
        self.make_repo()
        self.assert_refused(self.run_cli(env=self.fake_git_env("status", 128, "fatal: injected")), "status failed")

    def test_dirty_submodule_is_reported_by_its_own_root_only(self):
        repo = self.make_repo()
        sub = repo / "sub"
        sub.mkdir()
        git(sub, "init", "-q", "-b", "main")
        (sub / "s.txt").write_bytes(b"s1\n")
        git(sub, "add", "s.txt")
        git(sub, "commit", "-q", "-m", "s")
        git(repo, "add", "sub")
        git(repo, "commit", "-q", "-m", "gitlink")
        (sub / "s.txt").write_bytes(b"s2 changed\n")
        proc = self.run_cli()
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        roots = {r["path"]: r["dirty"] for r in json.loads(self.out.read_bytes())["git_roots"]}
        self.assertEqual(roots, {str(repo): [], str(sub): [" M s.txt"]})

    def refused_config(self, key: str, value: str, needle: str):
        repo = self.make_repo()
        outside = self.tmp / "outside.cfg"
        outside.write_bytes(b"[user]\n\tname = outside\n")
        git(repo, "config", key, value.format(outside=outside))
        self.assert_refused(self.run_cli(), needle)

    def test_config_include_path_is_refused(self):
        self.refused_config("include.path", "{outside}", "include.path")

    def test_config_include_if_is_refused(self):
        self.refused_config("includeIf.gitdir:/.path", "{outside}", "includeif.gitdir:/.path")

    def test_config_core_excludes_file_is_refused(self):
        self.refused_config("core.excludesFile", "{outside}", "core.excludesfile")

    def test_config_core_attributes_file_is_refused(self):
        self.refused_config("core.attributesFile", "{outside}", "core.attributesfile")

    def test_config_unknown_core_key_is_refused(self):
        self.refused_config("core.somethingNew", "1", "core.somethingnew")

    def test_non_utf8_branch_name_is_a_json_fail(self):
        repo = self.make_repo()
        (repo / ".git" / "HEAD").write_bytes(b"ref: refs/heads/\xff\n")
        self.assert_refused(self.run_cli(), "UnicodeDecodeError")


class Invocation(Base):
    def test_missing_root_exits_2(self):
        proc = self.run_cli(root=self.tmp / "missing")
        self.assertEqual(proc.returncode, 2, proc.stdout + proc.stderr)
        self.assertEqual(proc.stdout, b"")
        self.assertFalse(os.path.lexists(self.out))

    def test_root_and_out_are_required(self):
        for argv in (["--out", str(self.out)], ["--root", str(self.unit)]):
            with self.subTest(argv=argv):
                proc = subprocess.run([sys.executable, "-B", str(TOOL), *argv], capture_output=True, timeout=60,
                                      stdin=subprocess.DEVNULL)
                self.assertEqual(proc.returncode, 2, proc.stdout + proc.stderr)
                self.assertIn(b"required", proc.stderr)
                self.assertFalse(os.path.lexists(self.out))

    def test_output_in_a_subdirectory_of_the_unit_is_refused(self):
        (self.unit / "dest").mkdir()
        before = snapshot(self.unit)
        proc = self.run_cli(out=self.unit / "dest" / "m.json")
        self.assertEqual(proc.returncode, 2, proc.stdout + proc.stderr)
        self.assertEqual(snapshot(self.unit), before)

    def test_output_reached_through_a_linked_ancestor_is_refused(self):
        (self.unit / "dest").mkdir()
        alias = self.tmp / "alias"
        os.symlink(self.tmp, alias)
        before = snapshot(self.unit)
        proc = self.run_cli(out=alias / "unit" / "dest" / "m.json")
        self.assertEqual(proc.returncode, 2, proc.stdout + proc.stderr)
        self.assertEqual(snapshot(self.unit), before)


class Output(Base):
    """Rulings 3 and 4: containment bound to the opened output directory; write failures are one JSON FAIL."""

    def setUp(self):
        super().setUp()
        (self.unit / "f").write_bytes(b"inside")
        self.dest = self.tmp / "dest"
        self.dest.mkdir()
        self.out = self.dest / "manifest.json"

    def run_with_leaf_hook(self, action):
        fired = []

        def hook(path, *rest):
            if not fired and basename_is(path, "f"):
                fired.append(True)
                action()
        result = self.patched_before("open", hook)
        self.assertTrue(fired)
        return result

    def test_output_parent_swapped_for_a_link_into_the_unit_writes_nothing_inside(self):
        before = snapshot(self.unit)

        def swap():
            os.rename(self.dest, self.tmp / "old-dest")
            os.symlink(self.unit, self.dest)
        self.run_with_leaf_hook(swap)
        self.assertFalse(os.path.lexists(self.unit / "manifest.json"))
        self.assertEqual(snapshot(self.unit), before)

    def test_pass_names_the_real_path_of_the_written_file(self):
        def swap():
            os.rename(self.dest, self.tmp / "old-dest")
            os.symlink(self.unit, self.dest)
        code, out, err = self.run_with_leaf_hook(swap)
        self.assertEqual(code, 0, out + err)
        result = json.loads(out)
        landed = self.tmp / "old-dest" / "manifest.json"
        self.assertEqual(result["manifest"], str(landed))
        self.assertEqual(result["sha256"], sha(landed.read_bytes()))

    def test_output_parent_moved_into_the_unit_during_the_walk_is_refused(self):
        code, out, err = self.run_with_leaf_hook(lambda: os.rename(self.dest, self.unit / "dest"))
        self.assert_json_fail(code, out, "inside the unit", err)
        self.assertEqual(os.listdir(self.unit / "dest"), [])

    def test_output_parent_moved_into_the_unit_during_the_write_is_reported_and_kept(self):
        fired = []

        def hook(fd, *rest):
            if not fired:
                fired.append(True)
                os.rename(self.dest, self.unit / "dest")
        code, out, err = self.patched_before("write", hook)
        self.assertTrue(fired, "the output was not written with os.write on the created fd")
        written = self.unit / "dest" / "manifest.json"
        reason = self.assert_json_fail(code, out, "inside the unit", err)["reason"]
        self.assertIn(str(written), reason)
        self.assertIn("left in place", reason)
        self.assertTrue(written.exists(), "never delete: the written output must stay where it landed")

    def test_write_failure_is_one_json_fail_and_the_partial_output_is_kept(self):
        launcher = ("import resource, runpy, signal, sys; signal.signal(signal.SIGXFSZ, signal.SIG_IGN); "
                    "resource.setrlimit(resource.RLIMIT_FSIZE, (1, 1)); sys.argv = sys.argv[1:]; "
                    "runpy.run_path(sys.argv[0], run_name='__main__')")
        proc = subprocess.run([sys.executable, "-B", "-c", launcher, str(TOOL), "--root", str(self.unit),
                               "--out", str(self.out)], capture_output=True, timeout=60, stdin=subprocess.DEVNULL)
        reason = self.assert_json_fail(proc.returncode, proc.stdout.decode(), "incomplete", proc.stderr.decode())
        self.assertIn(str(self.out), reason["reason"])
        self.assertEqual(self.out.read_bytes(), b"{")


if __name__ == "__main__":
    unittest.main()
