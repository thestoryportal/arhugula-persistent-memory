"""Tests for unit_manifest: a read-only, no-follow, hashed re-inventory of one unit."""
from __future__ import annotations

import contextlib
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
        self.tmp = Path(tempfile.mkdtemp(prefix="um"))
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
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.addCleanup(sock.close)
        sock.bind(str(u / "sock"))
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
        proc = self.run_cli()
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
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


if __name__ == "__main__":
    unittest.main()
