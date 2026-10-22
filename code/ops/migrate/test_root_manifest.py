"""Whole-root inventory contract; every input is a disposable fixture."""
import contextlib
import errno
import hashlib
import io
import json
import os
from pathlib import Path
import runpy
import socket
import stat
import subprocess
import tempfile
import unittest
import sys
from unittest import mock

import fault_kit
from ops.migrate import root_manifest


class RootManifest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(prefix="rm")
        self.addCleanup(temp.cleanup)
        self.top = Path(temp.name).resolve()
        self.root = self.top / "root"
        self.root.mkdir()
        self.out = self.top / "out.json"
        (self.root / "file").write_bytes(b"payload")

    def run_tool(self):
        stdout, stderr = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr), \
                mock.patch.object(subprocess, "run", side_effect=AssertionError("subprocess.run")), \
                mock.patch.object(subprocess, "Popen", side_effect=AssertionError("subprocess.Popen")):
            code = root_manifest.main(["--root", str(self.root), "--out", str(self.out)])
        return code, stdout.getvalue(), stderr.getvalue()

    def test_complete_manifest(self):
        files = {".git/config": b"[core]\n hookspath = /unused/hooks\n",
                 "sub/.git/HEAD": b"ref: refs/heads/main\n", ".gitignore": b"ignored\n",
                 "ignored": b"ignored bytes", "executable": b"exec", "private": b"secret",
                 "a/z": b"nested", "a.": b"sibling"}
        for name, data in files.items():
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        (self.root / "executable").chmod(0o755)
        (self.root / "private").chmod(0o600)
        outside = self.top / "outside"
        outside.mkdir()
        (outside / "secret").write_bytes(b"must not read")
        (self.root / "link").symlink_to(outside)
        (self.root / ".git" / "link").symlink_to(outside)
        (self.root / "gitfile").mkdir()
        (self.root / "gitfile" / ".git").write_bytes(b"gitdir: /unused\n")
        os.link(self.root / "file", self.root / "hard")
        expected = {}
        for name in ["file", "hard", "link", ".git/link", "gitfile/.git", *files]:
            path = self.root / name
            st = path.lstat()
            link = os.readlink(path) if path.is_symlink() else None
            body = os.fsencode(link) if link is not None else path.read_bytes()
            expected[str(path)] = dict(source=str(path), kind="symlink" if link else "file",
                                      bytes=st.st_size, sha256=hashlib.sha256(body).hexdigest(),
                                      link_text=link, device=st.st_dev, inode=st.st_ino,
                                      nlink=st.st_nlink, mode=stat.S_IMODE(st.st_mode))
        code, stdout, stderr = self.run_tool()
        self.assertEqual(code, 0, stdout + stderr)
        manifest = json.loads(self.out.read_bytes())
        self.assertEqual(manifest, dict(schema_version=1, root=str(self.root), git_roots=[],
                                       leaves=sorted(expected.values(), key=lambda x: os.fsencode(x["source"]))))
        self.assertEqual(json.loads(stdout), dict(status="PASS", manifest=str(self.out),
                         sha256=hashlib.sha256(self.out.read_bytes()).hexdigest(),
                         leaves=len(expected), git_roots=0))
        self.assertEqual(stderr, "")
        for name, data in files.items():
            self.assertEqual((self.root / name).read_bytes(), data)

    def test_socket(self):
        sock = socket.socket(socket.AF_UNIX)
        self.addCleanup(sock.close)
        path = self.root / "sock"
        cwd = os.getcwd()
        try:
            os.chdir(path.parent)
            sock.bind(path.name)
        finally:
            os.chdir(cwd)
        code, stdout, stderr = self.run_tool()
        self.assertEqual(code, 0, stdout + stderr)
        leaf = next(x for x in json.loads(self.out.read_bytes())["leaves"] if x["source"] == str(path))
        self.assertEqual(leaf["kind"], "socket")
        self.assertEqual(leaf["mode"], stat.S_IMODE(path.lstat().st_mode))
        self.assertEqual(leaf["sha256"], hashlib.sha256(b"").hexdigest())

    def test_file_root(self):
        self.root = self.root / "file"
        self.assertEqual(self.run_tool()[0], 0)
        self.assertEqual(json.loads(self.out.read_bytes())["leaves"][0]["source"], str(self.root))

    def test_empty_root(self):
        self.root = self.top / "empty"
        self.root.mkdir()
        self.assertEqual(self.run_tool()[0], 0)
        self.assertEqual(json.loads(self.out.read_bytes())["leaves"], [])

    def test_existing_output(self):
        self.out.write_bytes(b"keep")
        with mock.patch.object(os, "read", side_effect=AssertionError("read with existing output")):
            self.assertEqual(self.run_tool()[0], 2)
        self.assertEqual(self.out.read_bytes(), b"keep")

    def test_output_inside(self):
        self.out = self.root / "out"
        self.assertEqual(self.run_tool()[0], 2)
        self.assertFalse(self.out.exists())

    def test_missing_root(self):
        self.root = self.top / "missing"
        self.assertEqual(self.run_tool()[0], 2)

    def test_link_root(self):
        link = self.top / "alias"
        link.symlink_to(self.root)
        self.root = link
        self.assertEqual(self.run_tool()[0], 2)

    def test_link_ancestor(self):
        link = self.top / "alias"
        link.symlink_to(self.root)
        self.root = link / "file"
        self.assertEqual(self.run_tool()[0], 1)
        self.assertFalse(self.out.exists())

    def test_short_writes(self):
        with fault_kit.one_byte_writes():
            self.assertEqual(self.run_tool()[0], 0)
        self.assertEqual(len(json.loads(self.out.read_bytes())["leaves"]), 1)

    def test_fifo_swap(self):
        path = self.root / "file"
        with fault_kit.fifo_in_place(path, name="open", match=lambda name, *a, **k: name == "file"):
            self.assertEqual(self.run_tool()[0], 1)
        self.assertFalse(self.out.exists())

    def test_link_swap(self):
        path = self.root / "file"
        with fault_kit.swap_for_symlink("open", 1, path, self.top,
                                      match=lambda name, *a, **k: name == "file"):
            self.assertEqual(self.run_tool()[0], 1)
        self.assertFalse(self.out.exists())

    def test_root_rebind(self):
        with fault_kit.rename_and_rebind("read", 1, self.root):
            self.assertEqual(self.run_tool()[0], 1)
        self.assertFalse(self.out.exists())

    def assert_root_identity_change(self, field):
        original = self.root.lstat()
        real_fstat = os.fstat
        changed = []

        def fstat(fd):
            opened = real_fstat(fd)
            if not changed and (opened.st_dev, opened.st_ino) == (original.st_dev, original.st_ino):
                values = list(opened)
                values[field] += 1
                changed.append(fd)
                return os.stat_result(values)
            return opened

        with mock.patch.object(root_manifest.os, "fstat", side_effect=fstat):
            code, stdout, stderr = self.run_tool()
        self.assertEqual(len(changed), 1)
        self.assertEqual(code, 1, stdout + stderr)
        self.assertEqual(json.loads(stdout), dict(
            status="FAIL", reason=str(root_manifest.fdsafe.Refusal(
                str(self.root), "root changed between lstat and open"))))
        self.assertEqual(stderr, "")
        self.assertFalse(self.out.exists())

    def test_root_open_device_change(self):
        self.assert_root_identity_change(stat.ST_DEV)

    def test_root_open_inode_change(self):
        self.assert_root_identity_change(stat.ST_INO)

    def test_errors(self):
        for target in ("open", "scandir", "read", "write", "fstat", "close", fault_kit.GETPATH):
            for err in fault_kit.ERRNOS:
                with self.subTest(target=target, err=err):
                    self.out = self.top / (target + str(err))
                    with fault_kit.inject_oserror(target, 1, err):
                        code, stdout, stderr = self.run_tool()
                    self.assertIn(code, (1, 2), stdout + stderr)
                    self.assertIn(errno.errorcode[err], stdout + stderr)
                    self.assertIn(str(self.top), stdout + stderr)
                    self.assertEqual(len((stdout + stderr).splitlines()), 1)

    def test_unexpected(self):
        for exc in fault_kit.UNEXPECTED:
            with fault_kit.raise_unexpected("read", 1, exc), self.assertRaises(exc):
                self.run_tool()

    def test_entrypoint(self):
        argv = ["root_manifest", "--root", str(self.root), "--out", str(self.out)]
        with mock.patch.object(sys, "argv", argv), contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaises(SystemExit) as caught:
                runpy.run_path(root_manifest.__file__, run_name="__main__")
        self.assertEqual(caught.exception.code, 0)
        self.assertEqual(json.loads(self.out.read_bytes())["leaves"][0]["kind"], "file")

    def test_ancestor_link_refuses_before_read(self):
        alias = self.top / "alias"
        alias.symlink_to(self.top)
        self.root = alias / "root"
        with mock.patch.object(os, "read", side_effect=AssertionError("read through linked ancestor")):
            self.assertEqual(self.run_tool()[0], 1)

    def test_unsupported_leaf(self):
        os.mkfifo(self.root / "fifo")
        code, stdout, stderr = self.run_tool()
        self.assertEqual(code, 1, stdout + stderr)
        self.assertIn("fifo", stdout)
        self.assertEqual(stderr, "")
        self.assertFalse(self.out.exists())

    def test_directory_rebind(self):
        sub = self.root / "sub"
        sub.mkdir()
        (sub / "file").write_bytes(b"keep")
        with fault_kit.rename_and_rebind("open", 1, sub, match=lambda name, *a, **k: name == "sub"):
            self.assertEqual(self.run_tool()[0], 1)
        self.assertFalse(self.out.exists())

    def test_root_open_rebind(self):
        with fault_kit.rename_and_rebind("open", 1, self.root,
                                       match=lambda name, *a, **k: name == str(self.root)):
            self.assertEqual(self.run_tool()[0], 1)
        self.assertFalse(self.out.exists())

    def test_output_parent_moves_inside(self):
        parent = self.top / "output"
        parent.mkdir()
        self.out = parent / "manifest"
        real_read = os.read
        moved = False

        def read(fd, size):
            nonlocal moved
            if not moved:
                moved = True
                parent.rename(self.root / "moved")
                parent.mkdir()
            return real_read(fd, size)

        with mock.patch.object(os, "read", side_effect=read):
            self.assertEqual(self.run_tool()[0], 1)
        self.assertFalse((self.root / "moved" / "manifest").exists())

    def test_create_error_is_invocation_error(self):
        with fault_kit.inject_oserror("open", 1, errno.EIO,
                                     match=lambda name, *a, **k: name == self.out.name):
            code, stdout, stderr = self.run_tool()
        self.assertEqual(code, 2)
        self.assertEqual(stdout, "")
        self.assertIn("EIO", stderr)

    def test_write_error_keeps_output(self):
        with fault_kit.inject_oserror("write", 1, errno.ENOSPC):
            code, stdout, stderr = self.run_tool()
        self.assertEqual(code, 1)
        self.assertEqual(stderr, "")
        self.assertIn("ENOSPC", json.loads(stdout)["reason"])
        self.assertIn(str(self.out), json.loads(stdout)["reason"])
        self.assertTrue(self.out.exists())

    def test_descriptors_closed(self):
        (self.root / "sub").mkdir()
        (self.root / "sub" / "file").write_bytes(b"keep")
        opened = set()
        real_open = os.open

        def record(*args, **kwargs):
            fd = real_open(*args, **kwargs)
            opened.add(fd)
            return fd

        def cleanup():
            for fd in opened:
                try:
                    os.close(fd)
                except OSError as exc:
                    self.assertEqual(exc.errno, errno.EBADF)

        self.addCleanup(cleanup)
        with mock.patch.object(os, "open", side_effect=record):
            self.assertEqual(self.run_tool()[0], 0)
        for fd in opened:
            with self.assertRaises(OSError) as caught:
                os.fstat(fd)
            self.assertEqual(caught.exception.errno, errno.EBADF)

    def test_public_walk_preserves_git_policy(self):
        unit = root_manifest.unit_manifest
        gitdir = self.root / ".git"
        gitdir.mkdir()
        (gitdir / "link").symlink_to(self.top)
        with root_manifest.fdsafe.hold_root(str(self.root)) as held:
            with self.assertRaisesRegex(unit.Refusal, "Git would follow"):
                unit.walk(held.fd, str(self.root), [], [], False)

    def test_public_walk_collects_git_directories(self):
        (self.root / ".git").mkdir()
        (self.root / "other").mkdir()
        leaves, gitdirs = [], []
        with root_manifest.fdsafe.hold_root(str(self.root)) as held:
            root_manifest.unit_manifest.walk(held.fd, str(self.root), leaves, gitdirs, False)
        self.assertEqual(gitdirs, [str(self.root / ".git")])
        self.assertEqual([x["source"] for x in leaves], [str(self.root / "file")])

    def test_unit_manifest_still_walks(self):
        with root_manifest.fdsafe.hold_root(str(self.root)) as held, \
                mock.patch.object(subprocess, "run", side_effect=AssertionError("Git invoked")):
            manifest = root_manifest.unit_manifest.build_manifest(str(self.root), held.fd)
        self.assertEqual([x["source"] for x in manifest["leaves"]], [str(self.root / "file")])

    def test_later_filesystem_errors(self):
        (self.root / "sub").mkdir()
        for target, number, match in (("fstat", 2, None), ("open", 2, None),
                                      ("open", 1, lambda name, *a, **k: name == "sub")):
            with self.subTest(target=target, number=number, directory=match is not None):
                with fault_kit.inject_oserror(target, number, errno.EIO, match=match):
                    code, stdout, stderr = self.run_tool()
                self.assertEqual(code, 1, stdout + stderr)
                self.assertIn("EIO", stdout)
                self.assertEqual(stderr, "")

    def test_output_stat_error_is_not_absence(self):
        real_stat = os.lstat

        def lstat(path, *args, **kwargs):
            if path == str(self.out):
                raise OSError(errno.EIO, "stat failed")
            return real_stat(path, *args, **kwargs)

        with mock.patch.object(os, "lstat", side_effect=lstat):
            code, stdout, stderr = self.run_tool()
        self.assertEqual(code, 2)
        self.assertEqual(stdout, "")
        self.assertIn("EIO", stderr)
        self.assertFalse(self.out.exists())


    def assert_invalid_text_refused(self, path):
        run = subprocess.run([sys.executable, "-B", "-m", "ops.migrate.root_manifest",
                              "--root", str(self.root), "--out", str(self.out)],
                             capture_output=True, text=True)
        self.assertEqual(run.returncode, 1, run.stdout + run.stderr)
        self.assertEqual(run.stderr, "")
        self.assertEqual(len(run.stdout.splitlines()), 1)
        result = json.loads(run.stdout)
        self.assertEqual(result["status"], "FAIL")
        self.assertIn(repr(str(path)), result["reason"])
        self.assertFalse(self.out.exists())

    def test_non_utf8_link_text(self):
        path = self.root / "link"
        os.symlink(b"/unresolvable-\xff", os.fsencode(path))
        self.assert_invalid_text_refused(path)
        self.assertEqual(os.readlink(os.fsencode(path)), b"/unresolvable-\xff")

    def assert_non_utf8_name_refused(self, backing):
        # APFS rejects byte names at creation; expose one through the filesystem seam.
        invalid = os.fsdecode(b"byte-\xff")
        real_lstat, real_open = os.lstat, os.open
        real_scandir, real_live = os.scandir, root_manifest.fdsafe.live_path

        def actual(value):
            return value.replace(invalid, "byte-name") if isinstance(value, str) else value

        @contextlib.contextmanager
        def scandir(fd):
            with real_scandir(fd) as entries:
                names = []
                for entry in entries:
                    item = mock.Mock()
                    item.name = entry.name.replace("byte-name", invalid)
                    names.append(item)
                yield iter(names)

        path = str(backing).replace("byte-name", invalid)
        self.root = Path(str(self.root).replace("byte-name", invalid))
        with mock.patch.object(os, "scandir", side_effect=scandir), \
                mock.patch.object(os, "lstat", side_effect=lambda p, *a, **k: real_lstat(actual(p), *a, **k)), \
                mock.patch.object(os, "open", side_effect=lambda p, *a, **k: real_open(actual(p), *a, **k)), \
                mock.patch.object(root_manifest.fdsafe, "live_path", side_effect=lambda *a:
                                  real_live(*a).replace("byte-name", invalid)):
            code, stdout, stderr = self.run_tool()
        self.assertEqual(code, 1, stdout + stderr)
        self.assertEqual(stderr, "")
        self.assertEqual(len(stdout.splitlines()), 1)
        result = json.loads(stdout)
        self.assertEqual(result["status"], "FAIL")
        self.assertIn(repr(path), result["reason"])
        self.assertFalse(self.out.exists())

    def test_non_utf8_file_name(self):
        path = self.root / "byte-name"
        path.write_bytes(b"keep")
        self.assert_non_utf8_name_refused(path)
        self.assertEqual(path.read_bytes(), b"keep")

    def test_non_utf8_empty_folder_name(self):
        path = self.root / "byte-name"
        path.mkdir()
        self.assert_non_utf8_name_refused(path)
        self.assertEqual(list(path.iterdir()), [])

    def test_non_utf8_folder_component(self):
        path = self.root / "byte-name"
        path.mkdir()
        (path / "file").write_bytes(b"keep")
        self.assert_non_utf8_name_refused(path)
        self.assertEqual((path / "file").read_bytes(), b"keep")

    def test_non_utf8_directory_root(self):
        self.root = self.top / "byte-name"
        self.root.mkdir()
        self.assert_non_utf8_name_refused(self.root)

    def test_non_utf8_file_root(self):
        self.root = self.top / "byte-name"
        self.root.write_bytes(b"keep")
        self.assert_non_utf8_name_refused(self.root)

    def assert_output_move_refused(self, destination):
        real_write = os.write
        written_fds = []

        def write(fd, body):
            count = real_write(fd, body)
            if not written_fds:
                self.out.rename(destination)
                written_fds.append(fd)
            return count

        with mock.patch.object(os, "write", side_effect=write):
            code, stdout, stderr = self.run_tool()
        self.assertEqual(len(written_fds), 1)
        self.assertEqual(code, 1, stdout + stderr)
        self.assertEqual(stderr, "")
        self.assertEqual(len(stdout.splitlines()), 1)
        result = json.loads(stdout)
        self.assertEqual(result["status"], "FAIL")
        self.assertIn(str(destination), result["reason"])
        self.assertIn("left in place", result["reason"])
        self.assertFalse(self.out.exists())
        self.assertEqual(json.loads(destination.read_bytes())["root"], str(self.root))
        with self.assertRaises(OSError) as caught:
            os.fstat(written_fds[0])
        self.assertEqual(caught.exception.errno, errno.EBADF)

    def test_output_moves_inside_during_write(self):
        self.assert_output_move_refused(self.root / "moved.json")

    def test_output_renamed_during_write(self):
        self.assert_output_move_refused(self.top / "renamed.json")


    def test_file_parent_path_error_refuses_before_read(self):
        self.root = self.root / "file"
        with fault_kit.inject_oserror(fault_kit.GETPATH, 3, errno.EIO), \
                mock.patch.object(os, "read", side_effect=AssertionError("read after path error")):
            code, stdout, stderr = self.run_tool()
        self.assertEqual(code, 1, stdout + stderr)
        self.assertEqual(stderr, "")
        self.assertIn(repr(str(self.root.parent)), json.loads(stdout)["reason"])
        self.assertIn("EIO", stdout)
        self.assertFalse(self.out.exists())

    def test_file_root_descriptors_closed(self):
        self.root = self.root / "file"
        real_open = os.open
        opened = set()

        def record(*args, **kwargs):
            fd = real_open(*args, **kwargs)
            opened.add(fd)
            return fd

        with mock.patch.object(os, "open", side_effect=record):
            self.assertEqual(self.run_tool()[0], 0)
        for fd in opened:
            with self.assertRaises(OSError) as caught:
                os.fstat(fd)
            self.assertEqual(caught.exception.errno, errno.EBADF)

    def test_output_linked_ancestor_inside_refuses_before_read(self):
        (self.root / "inside").mkdir()
        alias = self.top / "alias"
        alias.symlink_to(self.root)
        self.out = alias / "inside" / "manifest"
        with mock.patch.object(os, "read", side_effect=AssertionError("read with output inside")):
            code, stdout, stderr = self.run_tool()
        self.assertEqual(code, 2, stdout + stderr)
        self.assertEqual(stdout, "")
        self.assertIn("inside", stderr)
        self.assertFalse(self.out.exists())

    def test_root_and_output_parent_move_after_inventory(self):
        parent = self.top / "output"
        parent.mkdir()
        self.out = parent / "manifest"
        moved = self.top / "moved"
        canonical = root_manifest.unit_manifest.canonical

        def encode(manifest):
            body = canonical(manifest)
            self.root.rename(moved)
            parent.rename(moved / "output")
            return body

        with mock.patch.object(root_manifest.unit_manifest, "canonical", side_effect=encode):
            code, stdout, stderr = self.run_tool()
        self.assertEqual(code, 1, stdout + stderr)
        self.assertEqual(stderr, "")
        self.assertIn("output directory moved inside root", json.loads(stdout)["reason"])
        self.assertFalse((moved / "output" / "manifest").exists())


    def test_utf8_names_and_link_text_pass(self):
        folder = self.root / "枝"
        folder.mkdir()
        (folder / "葉").write_bytes(b"keep")
        link = folder / "連"
        link.symlink_to("外")
        self.assertEqual(self.run_tool()[0], 0)
        leaves = {row["source"]: row for row in json.loads(self.out.read_bytes())["leaves"]}
        self.assertEqual(leaves[str(link)]["link_text"], "外")
        self.assertEqual(leaves[str(folder / "葉")]["sha256"], hashlib.sha256(b"keep").hexdigest())


    def test_required_arguments_exit_2_without_traceback(self):
        for args in ([], ["--root", str(self.root)], ["--out", str(self.out)]):
            with self.subTest(args=args):
                run = subprocess.run([sys.executable, "-B", "-m", "ops.migrate.root_manifest", *args],
                                     capture_output=True, text=True)
                self.assertEqual(run.returncode, 2, run.stdout + run.stderr)
                self.assertEqual(run.stdout, "")
                self.assertIn("required", run.stderr)
                self.assertNotIn("Traceback", run.stderr)
                self.assertFalse(self.out.exists())


    def test_unexpected_text_encoding_error_propagates(self):
        (self.root / "link").symlink_to("outside")
        real_decode = os.fsdecode
        for error in (*fault_kit.UNEXPECTED, MemoryError):
            with self.subTest(error=error):
                class Text(str):
                    def encode(self, *args, **kwargs):
                        raise error("unexpected encoder failure")

                def decode(value):
                    return Text("outside") if value == b"outside" else real_decode(value)

                with mock.patch.object(os, "fsdecode", side_effect=decode), self.assertRaises(error):
                    self.run_tool()
                self.assertFalse(self.out.exists())


    def assert_child_rebind_refused(self, replacement):
        sub = self.root / "sub"
        sub.mkdir()
        leaf = sub / "leaf"
        leaf.write_bytes(b"original")
        real_read = os.read
        original = sub.stat()
        leaf_inode = leaf.stat().st_ino

        def read(fd, size):
            if replacement and not leaf.exists():
                leaf.write_bytes(b"NEW CONTENT")
            return real_read(fd, size)

        # [LAW:behavior-not-structure] Rebind an entered directory during its leaf read.
        with mock.patch.object(os, "read", side_effect=read), \
                fault_kit.rename_and_rebind("read", 1, sub,
                    match=lambda fd, size: os.fstat(fd).st_ino == leaf_inode) as attack:
            code, stdout, stderr = self.run_tool()
        self.assertEqual(attack.fired, 1)
        self.assertNotEqual(sub.stat().st_ino, original.st_ino)
        self.assertEqual(code, 1, stdout + stderr)
        self.assertEqual(stderr, "")
        self.assertEqual(len(stdout.splitlines()), 1)
        result = json.loads(stdout)
        self.assertEqual(result["status"], "FAIL")
        self.assertIn(repr(str(sub)), result["reason"])
        self.assertFalse(self.out.exists())

    def test_child_rebind_during_read(self):
        self.assert_child_rebind_refused(False)

    def test_child_rebind_with_replacement_leaf(self):
        self.assert_child_rebind_refused(True)

    def test_nested_leaf_error_names_leaf(self):
        leaf = self.root / "sub" / "deep" / "leaf"
        leaf.parent.mkdir(parents=True)
        leaf.write_bytes(b"keep")
        # The kit dispatches os targets by name; register lstat for this scoped attack.
        with mock.patch.object(fault_kit, "TARGETS", (*fault_kit.TARGETS, "lstat")), \
                fault_kit.inject_oserror("lstat", 1, errno.EIO,
                match=lambda path, *a, **k: path == str(leaf)) as attack:
            code, stdout, stderr = self.run_tool()
        self.assertEqual(attack.fired, 1)
        self.assertEqual(code, 1, stdout + stderr)
        self.assertEqual(stderr, "")
        self.assertEqual(len(stdout.splitlines()), 1)
        result = json.loads(stdout)
        self.assertEqual(result["status"], "FAIL")
        self.assertIn(repr(str(leaf)), result["reason"])
        self.assertIn("EIO", result["reason"])
        self.assertFalse(self.out.exists())

    def test_public_walk_collects_nested_git_directories(self):
        gitdir = self.root / "sub" / "deep" / ".git"
        gitdir.mkdir(parents=True)
        leaf = gitdir / "HEAD"
        leaf.write_bytes(b"ref: refs/heads/main\n")
        leaves, gitdirs = [], []
        with root_manifest.fdsafe.hold_root(str(self.root)) as held:
            root_manifest.unit_manifest.walk(held.fd, str(self.root), leaves, gitdirs, False)
        self.assertEqual(gitdirs, [str(gitdir)])
        self.assertEqual([row["source"] for row in leaves],
                         [str(self.root / "file"), str(leaf)])


    def assert_empty_child_relocated(self, replacement):
        child = self.root / "a" / "empty"
        child.mkdir(parents=True)
        real_read = os.read
        moved = []

        def read(fd, size):
            if not moved:
                child.rename(self.top / "parked")
                if replacement == "symlink":
                    child.symlink_to(self.top / "parked")
                moved.append(child)
            return real_read(fd, size)

        with mock.patch.object(os, "read", side_effect=read):
            code, stdout, stderr = self.run_tool()
        self.assertEqual(moved, [child])
        self.assertEqual(code, 1, stdout + stderr)
        self.assertEqual(stderr, "")
        self.assertEqual(len(stdout.splitlines()), 1)
        result = json.loads(stdout)
        self.assertEqual(result["status"], "FAIL")
        self.assertIn(repr(str(child)), result["reason"])
        self.assertFalse(self.out.exists())

    def test_empty_descendant_absent_after_walk(self):
        self.assert_empty_child_relocated("absent")

    def test_empty_descendant_replaced_by_symlink(self):
        self.assert_empty_child_relocated("symlink")

    def test_directory_recheck_device_change(self):
        child = self.root / "empty"
        child.mkdir()
        real_lstat = os.lstat
        calls = []

        def lstat(path, *args, **kwargs):
            result = real_lstat(path, *args, **kwargs)
            if path == str(child):
                calls.append(path)
                if len(calls) == 2:
                    values = list(result)
                    values[stat.ST_DEV] += 1
                    return os.stat_result(values)
            return result

        with mock.patch.object(os, "lstat", side_effect=lstat):
            code, stdout, stderr = self.run_tool()
        self.assertEqual(code, 1, stdout + stderr)
        self.assertEqual(stderr, "")
        self.assertEqual(len(stdout.splitlines()), 1)
        self.assertEqual(json.loads(stdout)["status"], "FAIL")
        self.assertIn(repr(str(child)), json.loads(stdout)["reason"])
        self.assertFalse(self.out.exists())


if __name__ == "__main__":
    unittest.main()
