"""T360: file roots retain their identity and produce one canonical leaf."""
import json
import os
from unittest import mock

import fault_kit as FK
import unit_manifest
from test_unit_manifest import Base, OtherDevice, canonical, sha


class FileUnit(Base):
    def setUp(self):
        super().setUp()
        self.file = self.unit / "model.json"
        self.data = b'{"weights":[1,2,3]}\n'
        self.file.write_bytes(self.data)

    def run_file(self):
        self.unit = self.file
        return self.run_inproc()

    def assert_refused(self, result, needle):
        code, out, err = result
        self.assert_json_fail(code, out, needle, err)
        self.assertFalse(os.path.lexists(self.out))

    def test_file_root_is_one_canonical_leaf(self):
        proc = self.run_cli(root=self.file)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        st = os.lstat(self.file)
        raw = self.out.read_bytes()
        self.assertEqual(raw, canonical({
            "schema_version": 1, "root": str(self.file), "git_roots": [],
            "leaves": [{"source": str(self.file), "kind": "file", "bytes": len(self.data),
                        "sha256": sha(self.data), "link_text": None, "device": st.st_dev,
                        "inode": st.st_ino, "nlink": 1}]}))
        result = json.loads(proc.stdout)
        self.assertEqual((result["status"], result["leaves"], result["git_roots"], result["sha256"]),
                         ("PASS", 1, 0, sha(raw)))

    def test_output_beside_file_is_allowed(self):
        out = self.file.with_suffix(".manifest")
        proc = self.run_cli(root=self.file, out=out)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertEqual(json.loads(out.read_bytes())["root"], str(self.file))

    def assert_invalid_root(self, path):
        real_open, opened = os.open, []

        def opening(*args, **kwargs):
            opened.append(args[0])
            return real_open(*args, **kwargs)

        self.unit = path
        with mock.patch.object(os, "open", opening):
            code, out, err = self.run_inproc()
        self.assertEqual(code, 2, out + err)
        self.assertEqual(opened, [], "invalid root reached open")
        self.assertFalse(os.path.lexists(self.out))

    def test_symlink_root_exits_2_before_open(self):
        link = self.tmp / "link"
        os.symlink(self.file, link)
        self.assert_invalid_root(link)

    def test_socket_root_exits_2_before_open(self):
        path = self.tmp / "socket"
        self.bind_socket(path)
        self.assert_invalid_root(path)

    def test_fifo_root_exits_2_before_open(self):
        path = self.tmp / "fifo"
        os.mkfifo(path)
        self.assert_invalid_root(path)

    def test_build_manifest_refuses_held_fifo(self):
        path = self.tmp / "fifo"
        os.mkfifo(path)
        fd = os.open(path, os.O_RDONLY | os.O_NONBLOCK)
        self.addCleanup(os.close, fd)
        with self.assertRaisesRegex(unit_manifest.Refusal, "neither a directory nor a regular file"):
            unit_manifest.build_manifest(str(path), fd)

    def test_linked_ancestor_refuses(self):
        alias = self.tmp / "alias"
        os.symlink(self.file.parent, alias)
        proc = self.run_cli(root=alias / self.file.name)
        self.assert_refused((proc.returncode, proc.stdout.decode(), proc.stderr.decode()), "symlink")

    def test_symlink_after_lstat_is_not_followed(self):
        lure = self.tmp / "lure"
        lure.write_bytes(b"unadmitted bytes")
        with FK.swap_for_symlink("open", 1, self.file, lure,
                                 match=lambda path, *a, **kw: path == str(self.file)) as fault:
            result = self.run_file()
        self.assertEqual(fault.fired, 1)
        self.assert_refused(result, "symbolic links")

    def test_fifo_after_lstat_does_not_block(self):
        # [LAW:verifiable-goals] A deadline makes loss of O_NONBLOCK a behavioral failure.
        try:
            with FK.fifo_in_place(self.file, name="open", n=1, timeout=0.5,
                                  match=lambda path, *a, **kw: path == str(self.file)) as fault:
                result = self.run_file()
            self.assertEqual(fault.fired, 1)
        except FK.AttackTimeout as exc:
            self.fail(str(exc))
        self.assert_refused(result, "root")

    def test_regular_replacement_after_lstat_refuses(self):
        real, fired = os.lstat, []

        def scanned(path, *args, **kwargs):
            st = real(path, *args, **kwargs)
            if not fired and os.fspath(path) == str(self.file):
                fired.append(True)
                self.file.rename(self.tmp / "original")
                self.file.write_bytes(b"replacement")
            return st

        with mock.patch.object(os, "lstat", scanned):
            result = self.run_file()
        self.assertTrue(fired)
        self.assert_refused(result, "root changed")

    def test_replacement_after_held_type_check_refuses(self):
        real, calls = os.fstat, []
        identity = os.stat(self.file)

        def held(fd):
            st = real(fd)
            if os.path.samestat(st, identity):
                calls.append(fd)
                if len(calls) == 2:
                    self.file.rename(self.tmp / "original")
                    self.file.write_bytes(b"replacement")
            return st

        with mock.patch.object(os, "fstat", held):
            result = self.run_file()
        self.assertGreaterEqual(len(calls), 2)
        self.assert_refused(result, "root changed after it was opened")

    def test_parent_entry_on_another_device_refuses(self):
        real, fired = os.stat, []

        def entry(path, *args, **kwargs):
            st = real(path, *args, **kwargs)
            if path == self.file.name and kwargs.get("dir_fd") is not None:
                fired.append(True)
                return OtherDevice(st)
            return st

        with mock.patch.object(os, "stat", entry):
            result = self.run_file()
        self.assertTrue(fired)
        self.assert_refused(result, "root changed after it was opened")

    def test_file_descriptors_close_on_success(self):
        before = sorted(os.listdir("/dev/fd"))
        code, out, err = self.run_file()
        self.assertEqual(code, 0, out + err)
        self.assertEqual(sorted(os.listdir("/dev/fd")), before)

    def test_parent_swapped_for_fifo_does_not_block(self):
        parent = self.file.parent
        before = sorted(os.listdir("/dev/fd"))
        try:
            with FK.fifo_in_place(parent, name="open", n=1, timeout=0.5,
                                  match=lambda path, *a, **kw: path == str(parent)) as fault:
                result = self.run_file()
            self.assertEqual(fault.fired, 1)
        except FK.AttackTimeout as exc:
            self.fail(str(exc))
        self.assert_refused(result, "Not a directory")
        self.assertEqual(sorted(os.listdir("/dev/fd")), before)

    def test_parent_symlink_to_same_inode_is_not_followed(self):
        parent = self.file.parent
        alias = self.tmp / "alias"
        alias.mkdir()
        os.link(self.file, alias / self.file.name)
        # [LAW:behavior-not-structure] The same inode defeats identity-only protection of the parent open.
        with FK.swap_for_symlink("open", 1, parent, alias,
                                 match=lambda path, *a, **kw: path == str(parent)) as fault:
            result = self.run_file()
        self.assertEqual(fault.fired, 1)
        self.assert_refused(result, "Not a directory")

    def test_root_open_on_another_device_refuses(self):
        real, fired = os.fstat, []
        identity = os.stat(self.file)

        def held(fd):
            st = real(fd)
            if not fired and os.path.samestat(st, identity):
                fired.append(True)
                return OtherDevice(st)
            return st

        with mock.patch.object(os, "fstat", held):
            result = self.run_file()
        self.assertTrue(fired)
        self.assert_refused(result, "root changed between lstat and open")

    def test_file_parent_rebound_during_read_refuses(self):
        with FK.rename_and_rebind("read", 1, self.file.parent) as fault:
            attacked = os.read

            def read(fd, size):
                data = attacked(fd, size)
                if not self.file.exists():
                    self.file.write_bytes(b"replacement")
                return data

            with mock.patch.object(os, "read", read):
                result = self.run_file()
        self.assertEqual(fault.fired, 1)
        # [LAW:behavior-not-structure] A later refusal must not mask the owning root check.
        self.assert_refused(result, "root moved during the inventory")

    def test_directory_parent_rebound_during_read_refuses(self):
        self.unit = self.unit / "directory"
        self.unit.mkdir()
        (self.unit / "leaf").write_bytes(self.data)
        with FK.rename_and_rebind("read", 1, self.unit.parent) as fault:
            attacked = os.read

            def read(fd, size):
                data = attacked(fd, size)
                if not self.unit.exists():
                    self.unit.mkdir()
                    (self.unit / "leaf").write_bytes(b"replacement")
                return data

            with mock.patch.object(os, "read", read):
                result = self.run_inproc()
        self.assertEqual(fault.fired, 1)
        self.assert_refused(result, "root moved during the inventory")
