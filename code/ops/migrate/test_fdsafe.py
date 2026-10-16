"""Tests for fdsafe: fd-bound walk, read and write. Attacks come from code/tests/fault_kit.py."""
from __future__ import annotations

import contextlib
import errno
import os
import shutil
import tempfile
import types
import unittest
from unittest import mock

import fault_kit as FK
from ops.migrate import fdsafe

GETPATH = FK.GETPATH


def open_fds() -> int:
    return len(os.listdir("/dev/fd"))


def named(path):
    """A fault_kit match: the call's first argument is this name or path."""
    return lambda first, *args, **kwargs: first == path


def fake_stat(st, **changes):
    fields = {k: getattr(st, k) for k in ("st_mode", "st_dev", "st_ino", "st_size", "st_mtime_ns")}
    fields.update(changes)
    return types.SimpleNamespace(**fields)


@contextlib.contextmanager
def patched_fstat(n, **changes):
    """Make the Nth os.fstat call report changed fields (a patched witness, as T212 ruling 4 allows)."""
    real, calls = os.fstat, [0]

    def hooked(fd):
        calls[0] += 1
        st = real(fd)
        return fake_stat(st, **{k: v(st) for k, v in changes.items()}) if calls[0] == n else st
    with mock.patch.object(os, "fstat", hooked):
        yield calls


@contextlib.contextmanager
def no_deletes():
    def refuse(*args, **kwargs):
        raise AssertionError(f"fdsafe deleted something: {args!r}")
    with mock.patch.object(os, "unlink", refuse), mock.patch.object(os, "remove", refuse), \
            mock.patch.object(os, "rmdir", refuse):
        yield


class Base(unittest.TestCase):
    def setUp(self):
        self.base = os.path.realpath(tempfile.mkdtemp(prefix="fdsafe-"))
        self.addCleanup(shutil.rmtree, self.base)
        self.root = self.mkdir("root")
        self.fds = open_fds()
        self.addCleanup(self.assertNoLeak)

    def assertNoLeak(self):
        self.assertEqual(open_fds(), self.fds, "an fd was left open")

    def mkdir(self, rel):
        path = os.path.join(self.base, rel)
        os.makedirs(path)
        return path

    def put(self, rel, data=b"bytes"):
        path = os.path.join(self.base, rel)
        with open(path, "wb") as fh:
            fh.write(data)
        return path

    def held(self, path=None):
        root = fdsafe.hold_root(path or self.root)
        self.addCleanup(root.close)
        return root

    def entries(self, root=None):
        seen = []
        fdsafe.walk(root or self.held(), seen.append)
        return seen

    def refusal(self, call, err=None):
        with self.assertRaises(fdsafe.Refusal) as cm:
            call()
        if err is not None:
            self.assertEqual(cm.exception.errno, err)
            self.assertIn(f"[{errno.errorcode[err]}]", str(cm.exception))
        self.assertNotIn("\n", str(cm.exception))
        return cm.exception


class RefusalType(Base):
    def test_refusal_is_a_valueerror_naming_path_and_errno(self):
        leaf = self.put("root/leaf")
        [entry] = self.entries()
        with FK.inject_oserror("open", 1, errno.EIO, match=named("leaf")) as fault:
            exc = self.refusal(lambda: fdsafe.read_bytes(entry), errno.EIO)
        self.assertEqual(fault.fired, 1)
        self.assertIsInstance(exc, ValueError)
        self.assertEqual(exc.path, leaf)
        self.assertIn(repr(leaf), str(exc))

    def test_non_oserror_is_not_turned_into_a_refusal(self):
        for exc_type in FK.UNEXPECTED:
            with self.subTest(exc_type=exc_type.__name__):
                with self.assertRaises(exc_type) as cm, FK.raise_unexpected("scandir", 1, exc_type):
                    fdsafe.walk(self.held(), lambda e: None)
                self.assertNotIsInstance(cm.exception, fdsafe.Refusal)


class HoldRoot(Base):
    def test_root_is_held_and_its_live_path_is_real(self):
        root = self.held()
        self.assertEqual(root.live(), self.root)
        self.assertEqual(root.path, self.root)

    def test_root_that_is_a_symlink_is_refused(self):
        link = os.path.join(self.base, "link")
        os.symlink(self.root, link)
        self.refusal(lambda: fdsafe.hold_root(link))

    def test_root_swapped_for_a_symlink_at_open_is_refused(self):
        outside = self.mkdir("outside")
        with self.assertRaises(fdsafe.Refusal), \
                FK.swap_for_symlink("open", 1, self.root, outside, match=named(self.root)) as fault:
            fdsafe.hold_root(self.root)
        self.assertEqual(fault.fired, 1)

    def test_root_with_a_linked_ancestor_is_refused_and_closed(self):
        self.mkdir("root/sub")
        link = os.path.join(self.base, "anc")
        os.symlink(self.root, link)
        exc = self.refusal(lambda: fdsafe.hold_root(os.path.join(link, "sub")))
        self.assertIn("is not its own real path", str(exc))

    def test_fifo_in_place_of_the_root_refuses_without_blocking(self):
        with FK.fifo_in_place(self.root, timeout=5):
            self.refusal(lambda: fdsafe.hold_root(self.root), errno.ENOTDIR)

    def test_errors_holding_the_root_are_refusals(self):
        for name, match in (("open", named(self.root)), (GETPATH, None), ("close", None)):
            with self.subTest(call=name):
                with self.assertRaises(fdsafe.Refusal) as cm, \
                        FK.inject_oserror(name, 1, errno.EIO, match=match) as fault:
                    root = fdsafe.hold_root(self.root)
                    root.close()
                self.assertEqual(fault.fired, 1)
                self.assertIn("[EIO]", str(cm.exception))
                self.assertIn(self.root, str(cm.exception))


class Walk(Base):
    def test_walk_visits_every_entry_sorted_and_depth_first_without_following_links(self):
        outside = self.mkdir("outside")
        self.put("outside/secret")
        names = ["n%02d" % i for i in (7, 3, 12, 0, 19, 5, 1, 16, 9, 14, 2, 18, 11, 4, 8, 6, 17, 10, 13, 15)]
        for name in names:
            self.put(f"root/{name}")
        self.mkdir("root/d")
        self.put("root/d/inner")
        os.symlink(outside, os.path.join(self.root, "link"))
        seen = self.entries()
        self.assertEqual([e.rel for e in seen], ["d", "d/inner", "link"] + sorted(names))
        self.assertEqual(seen[1].path, os.path.join(self.root, "d", "inner"))
        self.assertNotIn("secret", [e.name for e in seen])

    def test_directory_swapped_for_a_symlink_between_scan_and_open_is_refused(self):
        self.mkdir("root/sub")
        outside = self.mkdir("outside")
        self.put("outside/secret")
        seen = []
        root = self.held()
        with self.assertRaises(fdsafe.Refusal), \
                FK.swap_for_symlink("open", 1, os.path.join(self.root, "sub"), outside,
                                    match=named("sub")) as fault:
            fdsafe.walk(root, seen.append)
        self.assertEqual(fault.fired, 1)
        self.assertEqual([e.rel for e in seen], ["sub"])

    def test_directory_renamed_and_rebound_between_scan_and_open_is_refused(self):
        self.mkdir("root/sub")
        self.put("root/sub/leaf")
        root = self.held()
        with self.assertRaises(fdsafe.Refusal) as cm, \
                FK.rename_and_rebind("open", 1, os.path.join(self.root, "sub"), match=named("sub")) as fault:
            fdsafe.walk(root, lambda e: None)
        self.assertEqual(fault.fired, 1)
        self.assertIn("directory changed between scan and open", str(cm.exception))

    def test_directory_on_another_device_is_refused(self):
        self.mkdir("root/sub")
        root = self.held()
        with self.assertRaises(fdsafe.Refusal) as cm, patched_fstat(1, st_dev=lambda st: st.st_dev + 1):
            fdsafe.walk(root, lambda e: None)
        self.assertIn("directory changed between scan and open", str(cm.exception))

    def test_fifo_in_place_of_a_directory_refuses_without_blocking(self):
        self.mkdir("root/sub")
        root = self.held()
        with self.assertRaises(fdsafe.Refusal) as cm, \
                FK.fifo_in_place(os.path.join(self.root, "sub"), name="open", match=named("sub"), timeout=5):
            fdsafe.walk(root, lambda e: None)
        self.assertEqual(cm.exception.errno, errno.ENOTDIR)

    def test_walk_errors_are_refusals_naming_the_directory(self):
        sub = self.mkdir("root/sub")
        cases = (("scandir", 1, self.root), ("open", 1, sub), ("fstat", 1, sub), ("close", 1, sub),
                 ("scandir", 2, sub))
        for name, n, path in cases:
            for err in (errno.EIO, errno.EBADF):
                with self.subTest(call=name, n=n, err=errno.errorcode[err]):
                    root = fdsafe.hold_root(self.root)
                    try:
                        with self.assertRaises(fdsafe.Refusal) as cm, FK.inject_oserror(name, n, err) as fault:
                            fdsafe.walk(root, lambda e: None)
                    finally:
                        root.close()
                    self.assertEqual(fault.fired, 1)
                    self.assertEqual(cm.exception.path, path)
                    self.assertEqual(cm.exception.errno, err)

    def test_entry_gone_between_scan_and_stat_is_a_refusal(self):
        self.put("root/a")
        gone = self.put("root/b")

        def visit(entry):
            if entry.name == "a":
                os.unlink(gone)
        exc = self.refusal(lambda: fdsafe.walk(self.held(), visit), errno.ENOENT)
        self.assertEqual(exc.path, gone)

    def test_walk_reads_the_held_root_after_its_path_is_rebound(self):
        self.put("root/leaf", b"held")
        root = self.held()
        seen = []
        with FK.rename_and_rebind("scandir", 1, self.root) as fault:
            fdsafe.walk(root, seen.append)
        self.assertEqual(fault.fired, 1)
        self.assertEqual([e.rel for e in seen], ["leaf"])
        self.assertEqual(fdsafe.read_bytes(seen[0]), b"held")
        self.assertEqual(os.listdir(self.root), [])

    def test_held_root_as_a_context_manager_closes_its_fd(self):
        with fdsafe.hold_root(self.root) as root:
            self.assertEqual(root.live(), self.root)
        self.refusal(root.live, errno.EBADF)

    def test_a_refusing_visitor_leaves_no_fd_open(self):
        self.mkdir("root/a/b")
        self.put("root/a/b/leaf")

        def visit(entry):
            if entry.name == "leaf":
                raise fdsafe.Refusal(entry.path, "visitor refused")
        with self.assertRaises(fdsafe.Refusal):
            fdsafe.walk(self.held(), visit)


class ReadLeaf(Base):
    def entry(self, data=b"leaf bytes"):
        self.leaf = self.put("root/leaf", data)
        [entry] = self.entries()
        return entry

    def test_reads_exact_bytes_in_chunks(self):
        entry = self.entry(b"0123456789")
        chunks = []
        with mock.patch.object(fdsafe, "CHUNK", 3):
            self.assertEqual(fdsafe.read_leaf(entry, chunks.append), 10)
        self.assertEqual(chunks, [b"012", b"345", b"678", b"9"])
        self.assertEqual(fdsafe.read_bytes(entry), b"0123456789")

    def test_leaf_swapped_for_a_symlink_between_scan_and_open_is_refused_unread(self):
        entry = self.entry()
        secret = self.put("secret", b"outside!!!")
        sink = mock.Mock()
        with self.assertRaises(fdsafe.Refusal) as cm, \
                FK.swap_for_symlink("open", 1, self.leaf, secret, match=named("leaf")) as fault:
            fdsafe.read_leaf(entry, sink)
        self.assertEqual(fault.fired, 1)
        self.assertEqual(cm.exception.errno, errno.ELOOP)
        sink.assert_not_called()

    def test_fifo_in_place_of_a_leaf_refuses_without_blocking(self):
        entry = self.entry()
        sink = mock.Mock()
        with self.assertRaises(fdsafe.Refusal) as cm, \
                FK.fifo_in_place(self.leaf, name="open", match=named("leaf"), timeout=5):
            fdsafe.read_leaf(entry, sink)
        self.assertIn("changed between scan and open", str(cm.exception))
        sink.assert_not_called()

    def changed_before_open(self, change):
        entry = self.entry(b"0123456789")
        change(entry.st)
        sink = mock.Mock()
        exc = self.refusal(lambda: fdsafe.read_leaf(entry, sink))
        self.assertIn("changed between scan and open", str(exc))
        sink.assert_not_called()

    def test_replaced_file_same_size_same_mtime_is_refused_before_any_read(self):
        def replace(st):
            other = self.put("other", b"ABCDEFGHIJ")
            os.utime(other, ns=(st.st_atime_ns, st.st_mtime_ns))
            os.replace(other, self.leaf)
        self.changed_before_open(replace)

    def test_grown_file_same_mtime_is_refused_before_any_read(self):
        def grow(st):
            with open(self.leaf, "ab") as fh:
                fh.write(b"more")
            os.utime(self.leaf, ns=(st.st_atime_ns, st.st_mtime_ns))
        self.changed_before_open(grow)

    def test_touched_file_same_size_is_refused_before_any_read(self):
        self.changed_before_open(lambda st: os.utime(self.leaf, ns=(st.st_atime_ns, st.st_mtime_ns + 10**9)))

    def test_file_on_another_device_is_refused_before_any_read(self):
        entry = self.entry()
        sink = mock.Mock()
        with self.assertRaises(fdsafe.Refusal) as cm, patched_fstat(1, st_dev=lambda st: st.st_dev + 1):
            fdsafe.read_leaf(entry, sink)
        self.assertIn("changed between scan and open", str(cm.exception))
        sink.assert_not_called()

    def test_file_changed_during_the_read_is_refused(self):
        entry = self.entry()
        real = os.read

        def touching(fd, n):
            data = real(fd, n)
            os.utime(self.leaf, ns=(0, entry.st.st_mtime_ns + 10**9))
            return data
        with mock.patch.object(os, "read", touching):
            exc = self.refusal(lambda: fdsafe.read_leaf(entry, lambda chunk: None))
        self.assertIn("changed while it was read", str(exc))

    def test_short_read_is_refused(self):
        entry = self.entry()
        with mock.patch.object(os, "read", lambda fd, n: b""):
            exc = self.refusal(lambda: fdsafe.read_leaf(entry, lambda chunk: None))
        self.assertIn("read 0 bytes, scanned 10", str(exc))

    def test_non_regular_entry_is_refused_unopened(self):
        os.symlink("elsewhere", os.path.join(self.root, "link"))
        [entry] = self.entries()
        with mock.patch.object(os, "open") as opened:
            exc = self.refusal(lambda: fdsafe.read_bytes(entry))
        opened.assert_not_called()
        self.assertIn("is not a regular file", str(exc))

    def test_read_errors_are_refusals_naming_the_leaf(self):
        cases = (("open", 1), ("fstat", 1), ("read", 1), ("fstat", 2), ("close", 1))
        for name, n in cases:
            for err in (errno.EIO, errno.EBADF):
                with self.subTest(call=name, n=n, err=errno.errorcode[err]):
                    entry = self.entry()
                    with self.assertRaises(fdsafe.Refusal) as cm, FK.inject_oserror(name, n, err) as fault:
                        fdsafe.read_bytes(entry)
                    self.assertEqual(fault.fired, 1)
                    self.assertEqual(cm.exception.path, self.leaf)
                    self.assertEqual(cm.exception.errno, err)
                    os.unlink(self.leaf)

    def test_oserror_from_the_callers_sink_or_visitor_is_not_a_refusal(self):
        entry = self.entry()

        def failing(_):
            raise OSError(errno.EIO, "caller's own error")
        for call in (lambda: fdsafe.read_leaf(entry, failing), lambda: fdsafe.walk(self.held(), failing)):
            with self.assertRaises(OSError) as cm:
                call()
            self.assertNotIsInstance(cm.exception, fdsafe.Refusal)

    def test_unexpected_error_from_read_propagates_and_closes(self):
        entry = self.entry()
        with self.assertRaises(RuntimeError) as cm, FK.raise_unexpected("read", 1, RuntimeError):
            fdsafe.read_bytes(entry)
        self.assertNotIsInstance(cm.exception, fdsafe.Refusal)


class CreateFile(Base):
    def setUp(self):
        super().setUp()
        self.outdir = self.mkdir("out")
        self.target = os.path.join(self.outdir, "result.json")

    def parent(self, path=None):
        parent = fdsafe.open_out_parent(path or self.outdir)
        self.addCleanup(parent.close)
        return parent

    def create(self, data=b"payload\n", roots=None, name="result.json", parent=None):
        return fdsafe.create_file(parent or self.parent(), name, data,
                                  [self.held()] if roots is None else roots)

    def test_creates_exact_bytes_and_returns_the_live_path(self):
        self.assertEqual(self.create(b"exact"), self.target)
        with open(self.target, "rb") as fh:
            self.assertEqual(fh.read(), b"exact")

    def test_one_byte_writes_still_give_the_exact_file(self):
        with FK.one_byte_writes() as fault:
            self.create(b"0123456789abcdef")
        self.assertEqual(fault.calls, 16)
        with open(self.target, "rb") as fh:
            self.assertEqual(fh.read(), b"0123456789abcdef")

    def test_existing_file_is_never_overwritten(self):
        self.put("out/result.json", b"original")
        with no_deletes():
            self.refusal(lambda: self.create(), errno.EEXIST)
        with open(self.target, "rb") as fh:
            self.assertEqual(fh.read(), b"original")

    def test_symlink_planted_at_the_name_is_never_followed(self):
        aim = os.path.join(self.root, "planted")
        os.symlink(aim, self.target)
        self.refusal(lambda: self.create(), errno.EEXIST)
        self.assertFalse(os.path.lexists(aim))

    def test_names_that_are_not_one_file_are_refused(self):
        parent = self.parent()
        for name in ("", ".", "..", "a/b", "a\0b"):
            with self.subTest(name=name):
                exc = self.refusal(lambda: self.create(name=name, parent=parent))
                self.assertIn("names no single file", str(exc))
        self.assertEqual(os.listdir(self.outdir), [])

    def test_no_held_root_is_refused(self):
        exc = self.refusal(lambda: self.create(roots=[]))
        self.assertIn("no held root", str(exc))
        self.assertFalse(os.path.lexists(self.target))

    def test_parent_inside_a_root_is_refused_before_creating(self):
        inner = self.mkdir("root/inner")
        other = self.mkdir("other")
        roots = [self.held(other), self.held()]
        exc = self.refusal(lambda: self.create(roots=roots, parent=self.parent(inner)))
        self.assertIn("is inside root", str(exc))
        self.assertEqual(os.listdir(inner), [])

    def test_parent_that_is_the_root_is_refused(self):
        exc = self.refusal(lambda: self.create(parent=self.parent(self.root)))
        self.assertIn("is inside root", str(exc))
        self.assertEqual(os.listdir(self.root), [])

    def test_sibling_with_a_shared_prefix_is_outside(self):
        sibling = self.mkdir("root2")
        self.assertEqual(self.create(parent=self.parent(sibling)), os.path.join(sibling, "result.json"))

    def test_out_parent_swapped_for_a_symlink_into_the_root_is_refused(self):
        with self.assertRaises(fdsafe.Refusal), \
                FK.swap_for_symlink("open", 1, self.outdir, self.root, match=named(self.outdir)) as fault:
            fdsafe.open_out_parent(self.outdir)
        self.assertEqual(fault.fired, 1)
        self.assertEqual(os.listdir(self.root), [])

    def test_fifo_as_the_out_parent_refuses_without_blocking(self):
        with FK.fifo_in_place(self.outdir, timeout=5):
            self.refusal(lambda: fdsafe.open_out_parent(self.outdir), errno.ENOTDIR)

    def relocate_root_around_parent(self):
        """Move the root's directory to a new name and the out dir into it, then rebind both old paths."""
        moved = os.path.join(self.base, "moved")
        os.rename(self.root, moved)
        os.rename(self.outdir, os.path.join(moved, "out"))
        os.mkdir(self.root)
        os.mkdir(self.outdir)
        return os.path.join(moved, "out", "result.json")

    def test_parent_check_uses_the_live_root_not_its_old_path(self):
        root, parent = self.held(), self.parent()
        self.relocate_root_around_parent()
        exc = self.refusal(lambda: fdsafe.create_file(parent, "result.json", b"x", [root]))
        self.assertIn("is inside root", str(exc))
        self.assertEqual(os.listdir(os.path.join(self.base, "moved", "out")), [])

    def write_hook(self, move):
        real = os.write

        def hooked(fd, data):
            move()
            with mock.patch.object(os, "write", real):
                return real(fd, data)
        return mock.patch.object(os, "write", hooked)

    def test_root_and_parent_relocated_during_the_write_is_refused_and_kept(self):
        root, parent = self.held(), self.parent()
        landed = []
        with no_deletes(), self.write_hook(lambda: landed.append(self.relocate_root_around_parent())):
            exc = self.refusal(lambda: fdsafe.create_file(parent, "result.json", b"x", [root]))
        self.assertIn("was written inside root", str(exc))
        self.assertIn(landed[0], str(exc))
        self.assertTrue(os.path.isfile(landed[0]))

    def test_parent_moved_into_the_root_during_the_write_is_refused_and_kept(self):
        root, parent = self.held(), self.parent()
        inside = os.path.join(self.root, "out")
        with no_deletes(), self.write_hook(lambda: os.rename(self.outdir, inside)):
            exc = self.refusal(lambda: fdsafe.create_file(parent, "result.json", b"x", [root]))
        self.assertIn("was written inside root", str(exc))
        self.assertTrue(os.path.isfile(os.path.join(inside, "result.json")))

    def test_file_renamed_during_the_write_is_refused_and_kept(self):
        moved = os.path.join(self.outdir, "elsewhere.json")
        with no_deletes(), self.write_hook(lambda: os.rename(self.target, moved)):
            exc = self.refusal(lambda: self.create())
        self.assertIn("was moved during the write", str(exc))
        self.assertIn(moved, str(exc))
        self.assertTrue(os.path.isfile(moved))
        self.assertFalse(os.path.lexists(self.target))

    def test_write_errors_are_refusals_and_the_file_is_kept(self):
        for err in (errno.EIO, errno.ENOSPC, errno.EBADF):
            with self.subTest(err=errno.errorcode[err]):
                with no_deletes(), self.assertRaises(fdsafe.Refusal) as cm, \
                        FK.inject_oserror("write", 1, err) as fault:
                    self.create()
                self.assertEqual(fault.fired, 1)
                self.assertEqual(cm.exception.errno, err)
                self.assertIn(self.target, str(cm.exception))
                self.assertIn("left in place", str(cm.exception))
                self.assertTrue(os.path.isfile(self.target))
                os.unlink(self.target)

    def test_create_open_error_is_a_refusal(self):
        with self.assertRaises(fdsafe.Refusal) as cm, \
                FK.inject_oserror("open", 1, errno.EIO, match=named("result.json")) as fault:
            self.create()
        self.assertEqual(fault.fired, 1)
        self.assertEqual(cm.exception.path, self.target)
        self.assertEqual(cm.exception.errno, errno.EIO)

    def test_getpath_and_close_errors_are_refusals(self):
        # F_GETPATH order: parent, root (before), file, root, parent (after); then the file close.
        cases = [(GETPATH, n) for n in range(1, 6)] + [("close", 1)]
        for name, n in cases:
            with self.subTest(call=name, n=n):
                root, parent = fdsafe.hold_root(self.root), fdsafe.open_out_parent(self.outdir)
                try:
                    with no_deletes(), self.assertRaises(fdsafe.Refusal) as cm, \
                            FK.inject_oserror(name, n, errno.EIO) as fault:
                        fdsafe.create_file(parent, "result.json", b"x", [root])
                finally:
                    root.close()
                    parent.close()
                self.assertEqual(fault.fired, 1)
                self.assertIn("[EIO]", str(cm.exception))
                if n > 2 or name == "close":
                    self.assertIn(f"{self.target} (created, left in place)", str(cm.exception))
                    self.assertTrue(os.path.isfile(self.target))
                    os.unlink(self.target)
                else:
                    self.assertFalse(os.path.lexists(self.target))

    def test_unexpected_error_from_write_propagates_and_keeps_the_file(self):
        with no_deletes(), self.assertRaises(KeyError), FK.raise_unexpected("write", 1, KeyError):
            self.create()
        self.assertTrue(os.path.isfile(self.target))


if __name__ == "__main__":
    unittest.main()
