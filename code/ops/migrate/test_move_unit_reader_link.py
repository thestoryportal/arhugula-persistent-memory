"""T349: reader occurrences use link text without opening the target."""
import contextlib
import errno
import json
import os
import tempfile
import unittest
from unittest import mock

import fault_kit as FK
from ops.migrate import fdsafe
import test_move_unit_plan as plan


class NamedOrLink(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory(prefix="reader-link-")
        self.addCleanup(tmp.cleanup)
        self.root = os.path.realpath(tmp.name)
        self.path = os.path.join(self.root, "reader")

    def test_link_returns_own_bytes_even_for_missing_target(self):
        target = b"absent-\xff"
        os.symlink(target, os.fsencode(self.path))
        with fdsafe.hold_root(self.root) as held:
            self.assertEqual(fdsafe.read_named_or_link(held, "reader"), target)

    def test_link_does_not_read_existing_target(self):
        target = os.path.join(self.root, "target")
        with open(target, "wb") as stream:
            stream.write(b"not the link text")
        os.symlink(target, self.path)
        with fdsafe.hold_root(self.root) as held:
            self.assertEqual(fdsafe.read_named_or_link(held, "reader"), os.fsencode(target))

    def test_regular_file_equals_read_named(self):
        with open(self.path, "wb") as stream:
            stream.write(b"regular\x00\xff\n")
        with fdsafe.hold_root(self.root) as held:
            self.assertEqual(fdsafe.read_named_or_link(held, "reader"),
                             fdsafe.read_named(held, "reader"))

    def test_fifo_refused(self):
        with open(self.path, "wb"):
            pass
        with FK.fifo_in_place(self.path), fdsafe.hold_root(self.root) as held:
            with self.assertRaisesRegex(fdsafe.Refusal, "is not a regular file"):
                fdsafe.read_named_or_link(held, "reader")

    def test_lstat_eio_names_path(self):
        os.symlink("missing", self.path)
        with fdsafe.hold_root(self.root) as held, plan.lstat_error(errno.EIO, "reader"):
            with self.assertRaises(fdsafe.Refusal) as caught:
                fdsafe.read_named_or_link(held, "reader")
        self.assertEqual(caught.exception.path, self.path)
        self.assertIn("[EIO]", str(caught.exception))

    def test_link_replaced_by_regular_file_refuses(self):
        os.symlink("missing", self.path)
        real = os.readlink
        calls = []

        def replace(name, *args, **kwargs):
            calls.append(name)
            os.rename(self.path, self.path + ".parked")
            with open(self.path, "wb") as stream:
                stream.write(b"replacement must not be read")
            return real(name, *args, **kwargs)

        with fdsafe.hold_root(self.root) as held, mock.patch.object(os, "readlink", replace):
            with self.assertRaises(fdsafe.Refusal) as caught:
                fdsafe.read_named_or_link(held, "reader")
        self.assertEqual(len(calls), 1)
        self.assertEqual(caught.exception.path, self.path)
        self.assertIn("[EINVAL]", str(caught.exception))

    def test_parent_moved_after_lstat_refuses(self):
        os.symlink("missing", self.path)
        real = os.lstat
        calls = []

        def moved(name, *args, **kwargs):
            result = real(name, *args, **kwargs)
            if name == "reader" and "dir_fd" in kwargs:
                calls.append(name)
                os.rename(self.root, self.root + ".moved")
            return result

        with fdsafe.hold_root(self.root) as held:
            try:
                with mock.patch.object(os, "lstat", moved), self.assertRaisesRegex(
                        fdsafe.Refusal, "is held at"):
                    fdsafe.read_named_or_link(held, "reader")
            finally:
                if calls:
                    os.rename(self.root + ".moved", self.root)
        self.assertEqual(calls, ["reader"])


    def regular_reader(self):
        with open(self.path, "wb") as stream:
            stream.write(b"reader bytes")

    @contextlib.contextmanager
    def reader_fd(self):
        real, fds = os.open, set()

        def opened(name, *args, **kwargs):
            fd = real(name, *args, **kwargs)
            if name == "reader":
                fds.add(fd)
            else:
                fds.discard(fd)
            return fd

        with mock.patch.object(os, "open", opened):
            yield lambda fd, *args, **kwargs: fd in fds

    @contextlib.contextmanager
    def refusal(self, message, path=None):
        with self.assertRaises(fdsafe.Refusal) as caught:
            yield
        self.assertEqual(caught.exception.path, self.path if path is None else path)
        self.assertIn(message, str(caught.exception))

    def test_child_must_name_single_entry(self):
        with fdsafe.hold_root(self.root) as held:
            for name in ("", "..", "a/b"):
                with self.subTest(name=name), self.refusal(
                        "names no single entry", os.path.join(self.root, name)):
                    fdsafe.read_named_or_link(held, name)

    def test_readlink_uses_held_parent_after_rebind(self):
        os.symlink("held-text", self.path)
        real, calls = os.readlink, []
        parked = self.root + ".parked"

        def readlink(name, *args, **kwargs):
            calls.append(name)
            os.rename(self.root, parked)
            try:
                os.mkdir(self.root)
                os.symlink("impostor-text", self.path)
                return real(name, *args, **kwargs)
            finally:
                if os.path.lexists(self.path):
                    os.unlink(self.path)
                if os.path.isdir(self.root):
                    os.rmdir(self.root)
                os.rename(parked, self.root)

        with fdsafe.hold_root(self.root) as held, mock.patch.object(os, "readlink", readlink):
            self.assertEqual(fdsafe.read_named_or_link(held, "reader"), b"held-text")
        self.assertEqual(len(calls), 1)

    def test_fifo_swapped_between_scan_and_open(self):
        self.regular_reader()
        try:
            with fdsafe.hold_root(self.root) as held:
                with FK.fifo_in_place(self.path, name="open", n=1,
                                      match=plan.named("reader"), timeout=0.5) as fault:
                    with self.refusal("changed between scan and open"):
                        fdsafe.read_named_or_link(held, "reader")
                self.assertEqual(fault.fired, 1)
        except FK.AttackTimeout as exc:
            self.fail("reader open blocked on swapped FIFO: " + str(exc))

    def test_regular_replaced_between_scan_and_open(self):
        self.regular_reader()
        real, calls = os.open, []

        def opened(name, *args, **kwargs):
            if name == "reader":
                calls.append(name)
                os.rename(self.path, self.path + ".parked")
                self.regular_reader()
            return real(name, *args, **kwargs)

        with fdsafe.hold_root(self.root) as held, mock.patch.object(os, "open", opened):
            with self.refusal("changed between scan and open"):
                fdsafe.read_named_or_link(held, "reader")
        self.assertEqual(calls, ["reader"])

    def test_read_eio_names_reader(self):
        self.regular_reader()
        with fdsafe.hold_root(self.root) as held, self.reader_fd() as match:
            with FK.inject_oserror("read", 1, errno.EIO, match=match):
                with self.refusal("[EIO]"):
                    fdsafe.read_named_or_link(held, "reader")

    def test_reader_changes_during_read(self):
        self.regular_reader()
        real, changed = os.read, []
        with fdsafe.hold_root(self.root) as held, self.reader_fd() as match:
            def read(fd, count):
                data = real(fd, count)
                if match(fd) and data and not changed:
                    before = os.stat(self.path)
                    os.utime(self.path, ns=(before.st_atime_ns, before.st_mtime_ns + 1_000_000_000))
                    changed.append(True)
                return data
            with mock.patch.object(os, "read", read), self.refusal("changed while it was read"):
                fdsafe.read_named_or_link(held, "reader")
        self.assertEqual(changed, [True])

    def test_short_read_with_unchanged_identity_refuses(self):
        self.regular_reader()
        real, shortened = os.read, []
        with fdsafe.hold_root(self.root) as held, self.reader_fd() as match:
            def read(fd, count):
                data = real(fd, count)
                if match(fd) and data:
                    shortened.append(True)
                    return data[:3]
                return data
            with mock.patch.object(os, "read", read), self.refusal("read 3 bytes, scanned 12"):
                fdsafe.read_named_or_link(held, "reader")
        self.assertEqual(shortened, [True])

    def test_close_eio_names_reader(self):
        self.regular_reader()
        with fdsafe.hold_root(self.root) as held, self.reader_fd() as match:
            with FK.inject_oserror("close", 1, errno.EIO, match=match):
                with self.refusal("[EIO]"):
                    fdsafe.read_named_or_link(held, "reader")

    def test_fstat_eio_before_and_after_read_names_reader(self):
        self.regular_reader()
        for n in (1, 2):
            with self.subTest(n=n), fdsafe.hold_root(self.root) as held, self.reader_fd() as match:
                with FK.inject_oserror("fstat", n, errno.EIO, match=match):
                    with self.refusal("[EIO]"):
                        fdsafe.read_named_or_link(held, "reader")

class ReaderLink(plan.Base):
    def setUp(self):
        super().setUp()
        fx = self.fx
        os.rename(fx.reader, fx.reader + ".parked")
        os.symlink(fx.old, fx.reader)
        fx.stale["line"] = 1
        fx.rewrite(fx.readers, json.dumps(fx.readers_doc).encode())
        fx.rewrite(fx.repairs, (plan.REPAIR_HEADER + "\n").encode())

    def test_historical_link_exits_zero_without_findings(self):
        fx = self.fx
        fx.rewrite(fx.historical, f"file\tline\told_text\ndocs/a.md\t1\t{fx.old}\n".encode())
        proc = self.cli(*fx.check_plans_args())
        self.assertEqual((proc.returncode, proc.stdout, proc.stderr), (0, "[]\n", ""))

    def test_uncovered_link_exits_one_with_no_row(self):
        proc = self.cli(*self.fx.check_plans_args())
        self.assertEqual((proc.returncode, proc.stderr), (1, ""))
        self.assertEqual([row[0] for row in json.loads(proc.stdout)], ["no-row"])


if __name__ == "__main__":
    unittest.main()
