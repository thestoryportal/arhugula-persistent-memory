"""T349: reader occurrences use link text without opening the target."""
import contextlib
import ctypes
import errno
import json
import os
import tempfile
import unittest
from unittest import mock

import fault_kit as FK
from ops.migrate import fdsafe
import test_move_unit_plan as plan
import test_move_unit_run as run


@contextlib.contextmanager
def aba_link(parent, path, impostor):
    """Park at the live check; restore after acquiring the replacement object or text."""
    with FK.swap_for_symlink(FK.GETPATH, 1, path, impostor,
                             match=lambda fd, *args, **kwargs: fd == parent.fd) as fault:
        def restore_after(real):
            def restored(*args, **kwargs):
                result = real(*args, **kwargs)
                os.unlink(path)
                os.rename(fault.parked, path)
                return result
            return restored

        # [LAW:verifiable-goals] The legacy readlink hook makes the same ABA attack test K1 too.
        with mock.patch.object(fdsafe.os, "open", restore_after(os.open)), \
                mock.patch.object(fdsafe.os, "readlink", restore_after(os.readlink)):
            yield fault


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
        real = os.open

        def replace(name, *args, **kwargs):
            os.rename(self.path, self.path + ".parked")
            with open(self.path, "wb") as stream:
                stream.write(b"replacement must not be read")
            return real(name, *args, **kwargs)

        with fdsafe.hold_root(self.root) as held:
            with mock.patch.object(fdsafe.os, "open", side_effect=replace) as hook:
                with self.refusal("changed between scan and open"):
                    fdsafe.read_named_or_link(held, "reader")
        self.assertEqual(hook.call_count, 1)

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

    def test_link_read_uses_held_parent_after_rebind(self):
        os.symlink("held-text", self.path)
        real, calls = os.open, []
        parked = self.root + ".parked"

        def opened(name, *args, **kwargs):
            calls.append((name, kwargs.get("dir_fd")))
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

        with fdsafe.hold_root(self.root) as held, mock.patch.object(fdsafe.os, "open", opened):
            self.assertEqual(fdsafe.read_named_or_link(held, "reader"), b"held-text")
        self.assertEqual(calls, [("reader", held.fd)])

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

    def test_fifo_swapped_for_link_between_scan_and_open(self):
        os.symlink("original", self.path)
        try:
            with fdsafe.hold_root(self.root) as held:
                with FK.fifo_in_place(self.path, name="open", n=1,
                                      match=plan.named("reader"), timeout=0.5) as fault:
                    with self.refusal("changed between scan and open"):
                        fdsafe.read_named_or_link(held, "reader")
                self.assertEqual(fault.fired, 1)
        except FK.AttackTimeout as exc:
            self.fail("link open blocked on swapped FIFO: " + str(exc))

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

    def test_link_swapped_between_scan_and_link_read_refuses(self):
        os.symlink("original", self.path)
        # [LAW:behavior-not-structure] Equal lengths isolate identity from text size.
        with fdsafe.hold_root(self.root) as held:
            with FK.swap_for_symlink("open", 1, self.path, "replaced",
                                     match=plan.named("reader")) as fault:
                with self.refusal("changed between scan and open"):
                    fdsafe.read_named_or_link(held, "reader")
        self.assertEqual(fault.fired, 1)

    def test_aba_same_length_before_link_read_refuses(self):
        os.symlink("original", self.path)
        with fdsafe.hold_root(self.root) as held:
            with aba_link(held, self.path, "replaced") as fault:
                with self.refusal("changed between scan and open"):
                    fdsafe.read_named_or_link(held, "reader")
        self.assertEqual(fault.fired, 1)
        self.assertEqual(os.readlink(self.path), "original")

    def test_swap_after_open_link_read_returns_scanned_text(self):
        os.symlink("original", self.path)
        real = fdsafe._freadlink

        def swapped(fd, size):
            os.rename(self.path, self.path + ".parked")
            os.symlink("replaced", self.path)
            return real(fd, size)

        # [LAW:behavior-not-structure] A post-open swap cannot change the held inode's text.
        with fdsafe.hold_root(self.root) as held:
            with mock.patch.object(fdsafe, "_freadlink", side_effect=swapped) as hook:
                self.assertEqual(fdsafe.read_named_or_link(held, "reader"), b"original")
        self.assertEqual(hook.call_count, 1)
        self.assertEqual(os.readlink(self.path), "replaced")

    def test_link_read_errors_name_reader_and_close_fd(self):
        os.symlink("original", self.path)
        real_open, real_fstat, real_close = os.open, os.fstat, os.close

        def failed_freadlink(*args):
            ctypes.set_errno(errno.EIO)
            return -1

        for target in ("open", "fstat", "close", "freadlink", "unsupported"):
            with self.subTest(target=target), fdsafe.hold_root(self.root) as held:
                opened = []

                def tracked_open(*args, **kwargs):
                    fd = real_open(*args, **kwargs)
                    opened.append(fd)
                    return fd

                # [LAW:no-silent-failure] Both refusal diagnostics and fd release are observable.
                try:
                    with contextlib.ExitStack() as patches:
                        patches.enter_context(mock.patch.object(fdsafe.os, "open", tracked_open))
                        if target in ("open", "fstat", "close"):
                            match = plan.named("reader") if target == "open" else lambda fd: fd in opened
                            fault = patches.enter_context(FK.inject_oserror(
                                target, 1, errno.EIO, match=match))
                        else:
                            hook = patches.enter_context(mock.patch.object(
                                fdsafe, "_FREADLINK",
                                None if target == "unsupported" else mock.Mock(side_effect=failed_freadlink)))
                        try:
                            with self.refusal("[ENOTSUP]" if target == "unsupported" else "[EIO]"):
                                fdsafe.read_named_or_link(held, "reader")
                        except OSError as exc:
                            self.fail("link error escaped without a Refusal: " + str(exc))
                    if target in ("open", "fstat", "close"):
                        self.assertEqual(fault.fired, 1)
                    elif target == "freadlink":
                        self.assertEqual(hook.call_count, 1)
                    self.assertEqual(len(opened), 0 if target == "open" else 1)
                    for fd in opened:
                        with self.assertRaises(OSError) as caught:
                            real_fstat(fd)
                        self.assertEqual(caught.exception.errno, errno.EBADF)
                finally:
                    # Clean up a mutant's leak without hiding its failed assertion.
                    for fd in opened:
                        try:
                            real_fstat(fd)
                        except OSError as exc:
                            if exc.errno != errno.EBADF:
                                raise
                        else:
                            real_close(fd)

    def test_named_or_link_call_order(self):
        for kind, expected in (("link", ["lstat", "fcntl", "open", "fstat", "freadlink", "close"]),
                               ("regular", ["lstat", "fcntl", "open", "fstat", "read", "read", "fstat", "close"])):
            with self.subTest(kind=kind):
                path = os.path.join(self.root, kind)
                if kind == "link":
                    os.symlink("original", path)
                else:
                    with open(path, "wb") as stream:
                        stream.write(b"original")
                calls = []

                def recorder(label, real):
                    def recorded(*args, **kwargs):
                        calls.append(label)
                        return real(*args, **kwargs)
                    return recorded

                class RecordingOS:
                    def __getattr__(self, name):
                        value = getattr(os, name)
                        if callable(value) and name not in ("fsencode", "fsdecode", "fspath", "strerror"):
                            return recorder(name, value)
                        return value

                # [LAW:verifiable-goals] Every filesystem call participates in the ruled order.
                with fdsafe.hold_root(self.root) as held:
                    with mock.patch.object(fdsafe, "os", RecordingOS()), \
                            mock.patch.object(fdsafe.fcntl, "fcntl", recorder("fcntl", fdsafe.fcntl.fcntl)), \
                            mock.patch.object(fdsafe, "_FREADLINK", recorder("freadlink", fdsafe._FREADLINK)):
                        self.assertEqual(fdsafe.read_named_or_link(held, kind), b"original")
                self.assertEqual(calls, expected)


class LeafLinks(plan.Base):
    def test_nonreader_plan_inputs_stay_regular_file_only(self):
        # [LAW:one-source-of-truth] Borrow the catalogue, fixtures and argv from the plan suite.
        leaves = {cmd: tuple(attr for attr in attrs if (cmd, attr) != ("check-plans", "reader"))
                  for cmd, attrs in plan.LEAVES.items()}
        for fx, path, argv in plan.Attacks.cases(self, leaves):
            with self.subTest(path=path):
                os.rename(path, path + ".parked")
                os.symlink(fx.decoy, path)
                self.assert_refused(self.main(*argv), path, "is not a regular file")


class RunLeafLinks(run.Base):
    inputs = run.Attacks.inputs

    def test_run_inputs_stay_regular_file_only(self):
        for label in self.inputs():
            with self.subTest(label=label):
                self.setUp()
                path = self.inputs()[label]
                os.rename(path, path + ".parked")
                os.symlink(os.path.join(self.fx.decoy, "a.json"), path)
                self.assert_refused(self.main(*self.fx.args()), path, "is not a regular file")
                for unit in self.fx.units:
                    self.assertFalse(os.path.lexists(self.fx.target(unit)))


class ReaderLink(plan.Base):
    def setUp(self):
        super().setUp()
        fx = self.fx
        os.rename(fx.reader, fx.reader + ".parked")
        os.symlink(fx.old, fx.reader)
        fx.stale["line"] = 1
        fx.rewrite(fx.readers, json.dumps(fx.readers_doc).encode())
        fx.rewrite(fx.repairs, (plan.REPAIR_HEADER + "\n").encode())

    def test_aba_same_length_link_exits_two(self):
        fx = self.fx
        original = fx.old + " " + fx.old
        impostor = fx.old + " " + "x" * len(fx.old)
        os.unlink(fx.reader)
        os.symlink(original, fx.reader)
        fx.rewrite(fx.repairs, (plan.REPAIR_HEADER + "\ndocs/a.md\t1\t" + fx.old +
                               "\t" + fx.candidate + "/a.json\t261\n").encode())
        baseline = self.main(*fx.check_plans_args())
        self.assertEqual(baseline[0], 1)
        self.assertEqual(json.loads(baseline[1])[0][0], "not-once")
        real, fired = fdsafe.read_named_or_link, []

        def attacked(parent, name):
            if name != "a.md":
                return real(parent, name)
            with aba_link(parent, fx.reader, impostor) as fault:
                try:
                    return real(parent, name)
                finally:
                    fired.append(fault.fired)

        # [LAW:behavior-not-structure] Exercise check-plans' exit and output contract under ABA.
        with mock.patch.object(fdsafe, "read_named_or_link", attacked):
            result = self.main(*fx.check_plans_args())
        self.assertEqual(fired, [1])
        self.assertEqual(os.readlink(fx.reader), original)
        self.assertEqual(result[0], 2)
        self.assertEqual(result[1], "")
        self.assertIn(fx.reader, result[2])
        self.assertIn("changed between scan and open", result[2])
        self.assertNotIn("Traceback", result[2])

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
