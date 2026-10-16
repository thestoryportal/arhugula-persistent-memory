"""Tests for fdsafe's named calls: rename, mkdir and read_named. Attacks come from code/tests/fault_kit.py."""
from __future__ import annotations

import contextlib
import ctypes
import errno
import fcntl
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
    fields.update({k: v(st) for k, v in changes.items()})
    return types.SimpleNamespace(**fields)


@contextlib.contextmanager
def patched(func, n, **changes):
    """Make the Nth call of os.<func> report changed stat fields (a patched witness, as T212 ruling 4 allows)."""
    real, calls = getattr(os, func), [0]

    def hooked(*args, **kwargs):
        calls[0] += 1
        st = real(*args, **kwargs)
        return fake_stat(st, **changes) if calls[0] == n else st
    with mock.patch.object(os, func, hooked):
        yield calls


@contextlib.contextmanager
def lstat_error(err, n=1):
    """fault_kit has no lstat target: raise OSError(err) at the Nth os.lstat call."""
    real, calls = os.lstat, [0]

    def hooked(*args, **kwargs):
        calls[0] += 1
        if calls[0] == n:
            raise OSError(err, os.strerror(err))
        return real(*args, **kwargs)
    with mock.patch.object(os, "lstat", hooked):
        yield calls


@contextlib.contextmanager
def before_call(func, n, action):
    """Run action() just before the Nth call of os.<func>."""
    real, calls = getattr(os, func), [0]

    def hooked(*args, **kwargs):
        calls[0] += 1
        if calls[0] == n:
            action()
        return real(*args, **kwargs)
    with mock.patch.object(os, func, hooked):
        yield calls


def never(func):
    """Patch os.<func> so any call fails the test loudly (a Mock return value could loop a mutant forever)."""
    return mock.patch.object(os, func, side_effect=AssertionError(f"os.{func} must not be called"))


@contextlib.contextmanager
def no_deletes():
    def refuse(*args, **kwargs):
        raise AssertionError(f"fdsafe deleted something: {args!r}")
    with mock.patch.object(os, "unlink", refuse), mock.patch.object(os, "remove", refuse), \
            mock.patch.object(os, "rmdir", refuse):
        yield


@contextlib.contextmanager
def traced():
    """Record every filesystem call fdsafe can make, in order, as (call, first argument)."""
    log = []
    patches = []
    for func in ("open", "lstat", "fstat", "mkdir", "rename", "close", "read", "scandir"):
        real = getattr(os, func)
        patches.append(mock.patch.object(os, func, (lambda f, r: lambda *a, **k: (log.append((f, a[0])), r(*a, **k))[1])(func, real)))
    real_fcntl = fcntl.fcntl
    patches.append(mock.patch.object(
        fcntl, "fcntl", lambda *a: (log.append(("getpath" if a[1] == fcntl.F_GETPATH else "fcntl", a[0])),
                                    real_fcntl(*a))[1]))
    with contextlib.ExitStack() as stack:
        for p in patches:
            stack.enter_context(p)
        yield log


class Base(unittest.TestCase):
    def setUp(self):
        self.base = os.path.realpath(tempfile.mkdtemp(prefix="fdsafe-named-"))
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

    def read(self, path):
        with open(path, "rb") as fh:
            return fh.read()

    def held(self, path=None):
        root = fdsafe.hold_root(path or self.root)
        self.addCleanup(root.close)
        return root

    def refusal(self, call, err=None):
        with self.assertRaises(fdsafe.Refusal) as cm:
            call()
        if err is not None:
            self.assertEqual(cm.exception.errno, err)
            self.assertIn(f"[{errno.errorcode[err]}]", str(cm.exception))
        self.assertNotIn("\n", str(cm.exception))
        return cm.exception


BAD_NAMES = ("", ".", "..", "a/b", "a\0b")


class ReadNamed(Base):
    def setUp(self):
        super().setUp()
        self.leaf = self.put("root/leaf.json", b"0123456789")

    def test_reads_the_exact_bytes_through_the_held_parent(self):
        with mock.patch.object(fdsafe, "CHUNK", 3):
            self.assertEqual(fdsafe.read_named(self.held(), "leaf.json"), b"0123456789")

    def test_names_that_are_not_one_entry_are_refused_unopened(self):
        parent = self.held()
        for name in BAD_NAMES:
            with self.subTest(name=name), never("open") as opened:
                exc = self.refusal(lambda: fdsafe.read_named(parent, name))
                self.assertIn("names no single entry", str(exc))
                opened.assert_not_called()

    def test_missing_name_is_a_refusal_naming_the_path(self):
        exc = self.refusal(lambda: fdsafe.read_named(self.held(), "gone"), errno.ENOENT)
        self.assertEqual(exc.path, os.path.join(self.root, "gone"))

    def test_symlink_or_directory_at_the_name_is_refused_unopened(self):
        secret = self.put("secret", b"outside")
        os.symlink(secret, os.path.join(self.root, "link"))
        self.mkdir("root/sub")
        parent = self.held()
        for name in ("link", "sub"):
            with self.subTest(name=name), never("open") as opened:
                exc = self.refusal(lambda: fdsafe.read_named(parent, name))
                self.assertIn("is not a regular file", str(exc))
                opened.assert_not_called()

    def test_leaf_swapped_for_a_symlink_before_open_is_refused(self):
        secret = self.put("secret", b"outside!!!")
        parent = self.held()
        with self.assertRaises(fdsafe.Refusal) as cm, \
                FK.swap_for_symlink("open", 1, self.leaf, secret, match=named("leaf.json")) as fault:
            fdsafe.read_named(parent, "leaf.json")
        self.assertEqual(fault.fired, 1)
        self.assertEqual(cm.exception.errno, errno.ELOOP)

    def test_fifo_in_place_of_the_leaf_refuses_without_blocking(self):
        parent = self.held()
        with self.assertRaises(fdsafe.Refusal) as cm, \
                FK.fifo_in_place(self.leaf, name="open", match=named("leaf.json"), timeout=5):
            fdsafe.read_named(parent, "leaf.json")
        self.assertIn("changed between scan and open", str(cm.exception))

    def test_leaf_replaced_same_size_same_mtime_before_open_is_refused(self):
        st = os.lstat(self.leaf)
        other = self.put("other", b"ABCDEFGHIJ")
        os.utime(other, ns=(st.st_atime_ns, st.st_mtime_ns))
        parent = self.held()
        with before_call("open", 1, lambda: os.replace(other, self.leaf)):
            exc = self.refusal(lambda: fdsafe.read_named(parent, "leaf.json"))
        self.assertIn("changed between scan and open", str(exc))
        self.assertEqual(exc.path, self.leaf)

    def test_leaf_changed_during_the_read_is_refused(self):
        parent = self.held()
        with patched("fstat", 2, st_size=lambda st: st.st_size + 1):
            exc = self.refusal(lambda: fdsafe.read_named(parent, "leaf.json"))
        self.assertIn("changed while it was read", str(exc))

    def test_parent_rebound_before_the_call_is_refused_unread(self):
        parent = self.held()
        os.rename(self.root, os.path.join(self.base, "moved"))
        os.mkdir(self.root)
        with never("open") as opened:
            exc = self.refusal(lambda: fdsafe.read_named(parent, "leaf.json"))
        opened.assert_not_called()
        self.assertIn("is held at", str(exc))
        self.assertEqual(exc.path, self.root)

    def test_parent_rebound_at_the_live_check_is_refused_unread(self):
        parent = self.held()
        with self.assertRaises(fdsafe.Refusal) as cm, \
                FK.rename_and_rebind(GETPATH, 1, self.root) as fault, never("read") as read:
            fdsafe.read_named(parent, "leaf.json")
        self.assertEqual(fault.fired, 1)
        self.assertIn("is held at", str(cm.exception))
        read.assert_not_called()

    def test_parent_rebound_at_the_open_still_reads_the_held_leaf(self):
        parent = self.held()
        with FK.rename_and_rebind("open", 1, self.root, match=named("leaf.json")) as fault:
            data = fdsafe.read_named(parent, "leaf.json")
        self.assertEqual(fault.fired, 1)
        self.assertEqual(data, b"0123456789")

    def test_fifo_in_place_of_the_parent_is_refused(self):
        parent = self.held()
        with FK.fifo_in_place(self.root, timeout=5):
            exc = self.refusal(lambda: fdsafe.read_named(parent, "leaf.json"))
        self.assertIn("is held at", str(exc))

    def test_errors_are_refusals_naming_the_path_and_errno(self):
        cases = (("open", 1, self.leaf), ("fstat", 1, self.leaf), ("read", 1, self.leaf),
                 ("fstat", 2, self.leaf), ("close", 1, self.leaf), (GETPATH, 1, self.root))
        for name, n, path in cases:
            for err in (errno.EIO, errno.EBADF):
                with self.subTest(call=name, n=n, err=errno.errorcode[err]):
                    parent = fdsafe.hold_root(self.root)
                    try:
                        with self.assertRaises(fdsafe.Refusal) as cm, FK.inject_oserror(name, n, err) as fault:
                            fdsafe.read_named(parent, "leaf.json")
                    finally:
                        parent.close()
                    self.assertEqual(fault.fired, 1)
                    self.assertEqual(cm.exception.path, path)
                    self.assertEqual(cm.exception.errno, err)
                    self.assertIn(repr(path), str(cm.exception))
                    self.assertNotIn("\n", str(cm.exception))

    def test_lstat_error_is_a_refusal(self):
        parent = self.held()
        with lstat_error(errno.EIO):
            exc = self.refusal(lambda: fdsafe.read_named(parent, "leaf.json"), errno.EIO)
        self.assertEqual(exc.path, self.leaf)

    def test_unexpected_errors_propagate_and_close(self):
        parent = self.held()
        for exc_type in FK.UNEXPECTED:
            with self.subTest(exc_type=exc_type.__name__):
                with self.assertRaises(exc_type) as cm, FK.raise_unexpected("read", 1, exc_type):
                    fdsafe.read_named(parent, "leaf.json")
                self.assertNotIsInstance(cm.exception, fdsafe.Refusal)

    def test_parent_live_check_is_the_last_call_before_the_open(self):
        parent = self.held()
        with traced() as log:
            fdsafe.read_named(parent, "leaf.json")
        at = log.index(("open", "leaf.json"))
        self.assertEqual(log[at - 1], ("getpath", parent.fd))


class Mkdir(Base):
    def setUp(self):
        super().setUp()
        self.out = self.mkdir("out")
        self.made = os.path.join(self.out, "new")

    def parent(self, path=None):
        parent = fdsafe.open_out_parent(path or self.out)
        self.addCleanup(parent.close)
        return parent

    def test_creates_and_returns_the_held_new_directory(self):
        new = fdsafe.mkdir(self.parent(), "new")
        self.addCleanup(new.close)
        self.assertIsInstance(new, fdsafe.Dir)
        self.assertEqual(new.path, self.made)
        self.assertEqual(new.live(), self.made)
        self.assertTrue(os.path.isdir(self.made))
        self.assertEqual(os.listdir(self.made), [])
        self.assertEqual(os.fstat(new.fd).st_ino, os.lstat(self.made).st_ino)

    def test_names_that_are_not_one_entry_are_refused(self):
        parent = self.parent()
        for name in BAD_NAMES:
            with self.subTest(name=name):
                exc = self.refusal(lambda: fdsafe.mkdir(parent, name))
                self.assertIn("names no single entry", str(exc))
        self.assertEqual(os.listdir(self.out), [])

    def test_existing_entry_is_refused_and_unchanged(self):
        self.put("out/file", b"kept")
        self.mkdir("out/dir")
        aim = os.path.join(self.base, "aim")
        os.symlink(aim, os.path.join(self.out, "link"))
        parent = self.parent()
        for name in ("file", "dir", "link"):
            with self.subTest(name=name), no_deletes():
                self.refusal(lambda: fdsafe.mkdir(parent, name), errno.EEXIST)
        self.assertEqual(self.read(os.path.join(self.out, "file")), b"kept")
        self.assertFalse(os.path.lexists(aim))

    def test_new_directory_swapped_for_a_symlink_before_open_is_refused_and_kept(self):
        outside = self.mkdir("outside")
        parent = self.parent()
        with no_deletes(), self.assertRaises(fdsafe.Refusal) as cm, \
                FK.swap_for_symlink("open", 1, self.made, outside, match=named("new")) as fault:
            fdsafe.mkdir(parent, "new")
        self.assertEqual(fault.fired, 1)
        # O_DIRECTORY | O_NOFOLLOW on a link to a directory gives ENOTDIR on macOS (accepted in T212 fix 2).
        self.assertIn(cm.exception.errno, (errno.ELOOP, errno.ENOTDIR))
        self.assertIn("left in place", str(cm.exception))
        self.assertTrue(os.path.isdir(fault.parked))

    def test_new_directory_rebound_between_create_and_open_is_refused_and_kept(self):
        parent = self.parent()
        with no_deletes(), self.assertRaises(fdsafe.Refusal) as cm, \
                FK.rename_and_rebind("open", 1, self.made, match=named("new")) as fault:
            fdsafe.mkdir(parent, "new")
        self.assertEqual(fault.fired, 1)
        self.assertIn("changed between create and open", str(cm.exception))
        self.assertTrue(os.path.isdir(fault.parked))

    def test_new_directory_on_another_device_is_refused(self):
        parent = self.parent()
        with patched("fstat", 1, st_dev=lambda st: st.st_dev + 1):
            exc = self.refusal(lambda: fdsafe.mkdir(parent, "new"))
        self.assertIn("changed between create and open", str(exc))

    def test_fifo_in_place_of_the_new_directory_refuses_without_blocking(self):
        parent = self.parent()
        with no_deletes(), self.assertRaises(fdsafe.Refusal) as cm, \
                FK.fifo_in_place(self.made, name="open", match=named("new"), timeout=5):
            fdsafe.mkdir(parent, "new")
        self.assertEqual(cm.exception.errno, errno.ENOTDIR)

    def test_parent_rebound_before_the_call_creates_nothing(self):
        parent = self.parent()
        moved = os.path.join(self.base, "moved")
        os.rename(self.out, moved)
        os.mkdir(self.out)
        with never("mkdir") as made:
            exc = self.refusal(lambda: fdsafe.mkdir(parent, "new"))
        made.assert_not_called()
        self.assertIn("is held at", str(exc))
        self.assertEqual(os.listdir(moved), [])

    def test_parent_rebound_at_the_mkdir_is_refused_and_kept(self):
        parent = self.parent()
        with no_deletes(), self.assertRaises(fdsafe.Refusal) as cm, \
                FK.rename_and_rebind("mkdir", 1, self.out) as fault:
            fdsafe.mkdir(parent, "new")
        self.assertEqual(fault.fired, 1)
        landed = os.path.join(fault.parked, "new")
        self.assertIn(landed, str(cm.exception))
        self.assertIn("left in place", str(cm.exception))
        self.assertTrue(os.path.isdir(landed))
        self.assertEqual(os.listdir(self.out), [])

    def test_fifo_in_place_of_the_parent_is_refused(self):
        parent = self.parent()
        with FK.fifo_in_place(self.out, timeout=5) as fault:
            exc = self.refusal(lambda: fdsafe.mkdir(parent, "new"))
        self.assertIn("is held at", str(exc))
        self.assertEqual(os.listdir(fault.parked), [])

    def test_errors_are_refusals_naming_the_path_and_errno(self):
        # F_GETPATH order: parent (before the mkdir), then the new directory.
        cases = (("mkdir", 1, errno.EIO), ("mkdir", 1, errno.ENOSPC), (GETPATH, 1, errno.EIO),
                 ("open", 1, errno.EIO), ("fstat", 1, errno.EIO), (GETPATH, 2, errno.EIO),
                 (GETPATH, 2, errno.EBADF))
        for name, n, err in cases:
            with self.subTest(call=name, n=n, err=errno.errorcode[err]):
                parent = fdsafe.open_out_parent(self.out)
                try:
                    with no_deletes(), self.assertRaises(fdsafe.Refusal) as cm, \
                            FK.inject_oserror(name, n, err) as fault:
                        new = fdsafe.mkdir(parent, "new")
                        new.close()
                finally:
                    parent.close()
                self.assertEqual(fault.fired, 1)
                self.assertEqual(cm.exception.errno, err)
                self.assertNotIn("\n", str(cm.exception))
                if (name, n) in (("mkdir", 1), (GETPATH, 1)):
                    self.assertFalse(os.path.lexists(self.made))
                    expect = self.out if name == GETPATH else self.made
                    self.assertEqual(cm.exception.path, expect)
                else:
                    self.assertIn(f"{self.made} (created, left in place)", str(cm.exception))
                    self.assertTrue(os.path.isdir(self.made))
                    os.rmdir(self.made)

    def test_lstat_and_close_errors_are_refusals_keeping_the_directory(self):
        parent = self.parent()
        with no_deletes(), lstat_error(errno.EIO):
            exc = self.refusal(lambda: fdsafe.mkdir(parent, "new"), errno.EIO)
        self.assertIn(f"{self.made} (created, left in place)", str(exc))
        os.rmdir(self.made)
        # A close that fails while a refusal unwinds is itself a refusal naming the kept directory.
        with no_deletes(), self.assertRaises(fdsafe.Refusal) as cm, \
                patched("fstat", 1, st_ino=lambda st: st.st_ino + 1), \
                FK.inject_oserror("close", 1, errno.EIO) as fault:
            fdsafe.mkdir(parent, "new")
        self.assertEqual(fault.fired, 1)
        self.assertEqual(cm.exception.errno, errno.EIO)
        self.assertIn(f"{self.made} (created, left in place)", str(cm.exception))
        self.assertTrue(os.path.isdir(self.made))

    def test_unexpected_errors_propagate_and_close(self):
        parent = self.parent()
        for i, (call, exc_type) in enumerate((("mkdir", ValueError), ("fstat", KeyError), (GETPATH, RuntimeError))):
            with self.subTest(call=call):
                n = 2 if call == GETPATH else 1
                name = f"new{i}"
                with no_deletes(), self.assertRaises(exc_type) as cm, FK.raise_unexpected(call, n, exc_type):
                    fdsafe.mkdir(parent, name)
                self.assertNotIsInstance(cm.exception, fdsafe.Refusal)

    def test_parent_live_check_is_the_last_call_before_the_mkdir(self):
        parent = self.parent()
        with traced() as log:
            fdsafe.mkdir(parent, "new").close()
        at = log.index(("mkdir", "new"))
        self.assertEqual(log[at - 1], ("getpath", parent.fd))


REAL_RENAME = os.rename
NOREPLACE = fdsafe._rename_noreplace


@contextlib.contextmanager
def noreplace_at_os_rename():
    """Route fdsafe's exclusive rename through os.rename, so fault_kit's "rename" target (an os function) wraps it.

    os.rename runs the real exclusive call for fdsafe's dir-fd calls; the tests' own path moves keep the plain rename."""
    def os_rename(src, dst, *, src_dir_fd=None, dst_dir_fd=None):
        if src_dir_fd is None and dst_dir_fd is None:
            return REAL_RENAME(src, dst)
        return NOREPLACE(src, dst, src_dir_fd=src_dir_fd, dst_dir_fd=dst_dir_fd)
    with mock.patch.object(os, "rename", os_rename), \
            mock.patch.object(fdsafe, "_rename_noreplace", lambda *a, **k: os.rename(*a, **k)):
        yield


class Rename(Base):
    def setUp(self):
        super().setUp()
        self.enterContext(noreplace_at_os_rename())
        self.src = self.mkdir("root/src")
        self.dst = self.mkdir("root/dst")
        self.leaf = self.put("root/src/leaf", b"payload")
        self.target = os.path.join(self.dst, "leaf")

    def parents(self):
        """Hold the root and both parents before any attack starts; move() then opens nothing of its own."""
        self.roots = [self.held()]
        src, dst = fdsafe.hold_root(self.src), fdsafe.hold_root(self.dst)
        self.addCleanup(src.close)
        self.addCleanup(dst.close)
        return src, dst

    def move(self, src_name="leaf", dst_name="leaf", roots=None, parents=None):
        src, dst = parents or self.parents()
        return fdsafe.rename(src, src_name, dst, dst_name, self.roots if roots is None else roots)

    def assertUnmoved(self):
        self.assertEqual(self.read(self.leaf), b"payload")
        self.assertFalse(os.path.lexists(self.target))

    def test_moves_a_file_and_returns_its_live_path(self):
        ino = os.lstat(self.leaf).st_ino
        with no_deletes():
            self.assertEqual(self.move(), self.target)
        self.assertEqual(self.read(self.target), b"payload")
        self.assertEqual(os.lstat(self.target).st_ino, ino)
        self.assertFalse(os.path.lexists(self.leaf))

    def test_moves_a_directory_with_its_contents_under_a_new_name(self):
        self.mkdir("root/src/unit/inner")
        self.put("root/src/unit/inner/f", b"deep")
        self.assertEqual(self.move("unit", "renamed"), os.path.join(self.dst, "renamed"))
        self.assertEqual(self.read(os.path.join(self.dst, "renamed", "inner", "f")), b"deep")
        self.assertFalse(os.path.lexists(os.path.join(self.src, "unit")))

    def test_names_that_are_not_one_entry_are_refused(self):
        parents = self.parents()
        for src_name, dst_name in [(n, "leaf") for n in BAD_NAMES] + [("leaf", n) for n in BAD_NAMES]:
            with self.subTest(src=src_name, dst=dst_name):
                exc = self.refusal(lambda: self.move(src_name, dst_name, parents=parents))
                self.assertIn("names no single entry", str(exc))
        self.assertUnmoved()

    def test_existing_target_is_never_overwritten(self):
        self.put("root/dst/leaf", b"original")
        self.mkdir("root/dst/emptydir")
        aim = os.path.join(self.base, "aim")
        os.symlink(aim, os.path.join(self.dst, "link"))
        parents = self.parents()
        for name in ("leaf", "emptydir", "link"):
            with self.subTest(name=name), no_deletes(), never("rename") as renamed:
                self.refusal(lambda: self.move(dst_name=name, parents=parents), errno.EEXIST)
                renamed.assert_not_called()
        self.assertEqual(self.read(self.target), b"original")
        self.assertTrue(os.path.isdir(os.path.join(self.dst, "emptydir")))
        self.assertEqual(self.read(self.leaf), b"payload")
        self.assertFalse(os.path.lexists(aim))

    def test_no_held_root_is_refused_before_the_source_is_opened(self):
        parents = self.parents()
        with never("open"):
            exc = self.refusal(lambda: self.move(roots=[], parents=parents))
        self.assertIn("no held root to check the move against", str(exc))
        self.assertEqual(exc.path, self.target)
        self.assertUnmoved()

    def test_parents_outside_every_held_root_are_refused(self):
        outside = self.mkdir("outside")
        sibling = self.mkdir("root2")
        for path in (outside, sibling):
            self.put(os.path.join(os.path.basename(path), "leaf"), b"other")
            for side in ("src", "dst"):
                with self.subTest(path=path, side=side):
                    other = fdsafe.hold_root(path)
                    src, dst = self.parents()
                    try:
                        pair = (other, dst) if side == "src" else (src, other)
                        with never("rename") as renamed:
                            exc = self.refusal(lambda: self.move(dst_name="moved", parents=pair))
                        renamed.assert_not_called()
                    finally:
                        other.close()
                    self.assertIn("inside no held root", str(exc))
                    self.assertEqual(exc.path, path)
        self.assertUnmoved()

    def test_every_held_root_counts(self):
        second = self.mkdir("second")
        src, _ = self.parents()
        dst = self.held(second)
        roots = [self.held(), self.held(second)]
        self.assertEqual(fdsafe.rename(src, "leaf", dst, "leaf", roots), os.path.join(second, "leaf"))
        # The same move with only the first root refuses, so the second root is what admitted it.
        self.put("root/src/leaf2", b"x")
        exc = self.refusal(lambda: fdsafe.rename(src, "leaf2", dst, "leaf2", roots[:1]))
        self.assertIn("inside no held root", str(exc))

    def test_symlink_source_is_refused_unmoved(self):
        os.symlink(self.leaf, os.path.join(self.src, "link"))
        exc = self.refusal(lambda: self.move("link", "link"), errno.ELOOP)
        self.assertEqual(exc.path, os.path.join(self.src, "link"))
        self.assertTrue(os.path.islink(os.path.join(self.src, "link")))
        self.assertFalse(os.path.lexists(os.path.join(self.dst, "link")))

    def test_fifo_source_is_refused_unmoved(self):
        fifo = os.path.join(self.src, "fifo")
        os.mkfifo(fifo)
        with never("rename") as renamed:
            exc = self.refusal(lambda: self.move("fifo", "fifo"))
        renamed.assert_not_called()
        self.assertIn("is not a regular file or directory", str(exc))

    def test_missing_source_is_a_refusal(self):
        exc = self.refusal(lambda: self.move("gone", "gone"), errno.ENOENT)
        self.assertEqual(exc.path, os.path.join(self.src, "gone"))

    def test_source_swapped_for_a_symlink_at_open_is_refused_unmoved(self):
        secret = self.put("secret", b"outside")
        parents = self.parents()
        with self.assertRaises(fdsafe.Refusal) as cm, \
                FK.swap_for_symlink("open", 1, self.leaf, secret, match=named("leaf")) as fault:
            self.move(parents=parents)
        self.assertEqual(fault.fired, 1)
        self.assertEqual(cm.exception.errno, errno.ELOOP)
        self.assertFalse(os.path.lexists(self.target))
        self.assertEqual(self.read(fault.parked), b"payload")

    def test_fifo_in_place_of_the_source_is_refused_without_blocking(self):
        parents = self.parents()
        with self.assertRaises(fdsafe.Refusal) as cm, \
                FK.fifo_in_place(self.leaf, name="open", match=named("leaf"), timeout=5):
            self.move(parents=parents)
        self.assertIn("is not a regular file or directory", str(cm.exception))
        self.assertFalse(os.path.lexists(self.target))

    def test_source_swapped_between_the_checks_and_the_rename_is_refused_and_kept(self):
        parents = self.parents()
        with no_deletes(), self.assertRaises(fdsafe.Refusal) as cm, \
                FK.swap_for_symlink("rename", 1, self.leaf, "elsewhere") as fault:
            self.move(parents=parents)
        self.assertEqual(fault.fired, 1)
        self.assertIn("is not the object that was held", str(cm.exception))
        self.assertIn(f"{self.target} (moved, left in place)", str(cm.exception))
        self.assertTrue(os.path.islink(self.target))
        self.assertEqual(self.read(fault.parked), b"payload")

    def test_source_replaced_by_another_file_before_the_rename_is_refused_and_kept(self):
        other = self.put("other", b"payload")
        parents = self.parents()
        with no_deletes(), before_call("rename", 1, lambda: os.replace(other, self.leaf)):
            exc = self.refusal(lambda: self.move(parents=parents))
        self.assertIn("is not the object that was held", str(exc))
        self.assertTrue(os.path.isfile(self.target))

    def changed_after_move(self, func, n, **change):
        parents = self.parents()
        with no_deletes(), patched(func, n, **change):
            exc = self.refusal(lambda: self.move(parents=parents))
        self.assertIn(f"{self.target} (moved, left in place)", str(exc))
        self.assertEqual(self.read(self.target), b"payload")
        return exc

    def test_held_source_dev_changed_after_the_rename_is_refused(self):
        exc = self.changed_after_move("fstat", 2, st_dev=lambda st: st.st_dev + 1)
        self.assertIn("changed while it was moved", str(exc))

    def test_held_source_ino_changed_after_the_rename_is_refused(self):
        exc = self.changed_after_move("fstat", 2, st_ino=lambda st: st.st_ino + 1)
        self.assertIn("changed while it was moved", str(exc))

    def test_held_source_size_changed_after_the_rename_is_refused(self):
        exc = self.changed_after_move("fstat", 2, st_size=lambda st: st.st_size + 1)
        self.assertIn("changed while it was moved", str(exc))

    def test_held_source_mtime_changed_after_the_rename_is_refused(self):
        exc = self.changed_after_move("fstat", 2, st_mtime_ns=lambda st: st.st_mtime_ns + 1)
        self.assertIn("changed while it was moved", str(exc))

    def test_target_on_another_device_after_the_rename_is_refused(self):
        # os.lstat calls: the absent-target check (1, raises ENOENT so not counted by the patch), then the target.
        exc = self.changed_after_move("lstat", 2, st_dev=lambda st: st.st_dev + 1)
        self.assertIn("is not the object that was held", str(exc))

    def test_target_with_another_inode_after_the_rename_is_refused(self):
        exc = self.changed_after_move("lstat", 2, st_ino=lambda st: st.st_ino + 1)
        self.assertIn("is not the object that was held", str(exc))

    def test_held_source_touched_before_the_rename_is_refused_and_kept(self):
        parents = self.parents()
        st = os.lstat(self.leaf)
        with no_deletes(), before_call("rename", 1, lambda: os.utime(self.leaf, ns=(0, st.st_mtime_ns + 10**9))):
            exc = self.refusal(lambda: self.move(parents=parents))
        self.assertIn("changed while it was moved", str(exc))
        self.assertTrue(os.path.isfile(self.target))

    def test_destination_parent_rebound_at_the_rename_is_refused_and_kept(self):
        parents = self.parents()
        with no_deletes(), self.assertRaises(fdsafe.Refusal) as cm, \
                FK.rename_and_rebind("rename", 1, self.dst) as fault:
            self.move(parents=parents)
        self.assertEqual(fault.fired, 1)
        self.assertIn("is held at", str(cm.exception))
        self.assertIn("(moved, left in place)", str(cm.exception))
        self.assertEqual(self.read(os.path.join(fault.parked, "leaf")), b"payload")
        self.assertEqual(os.listdir(self.dst), [])

    def test_root_rebound_at_the_rename_is_refused_and_kept(self):
        parents = self.parents()
        with no_deletes(), self.assertRaises(fdsafe.Refusal) as cm, \
                FK.rename_and_rebind("rename", 1, self.root) as fault:
            self.move(parents=parents)
        self.assertEqual(fault.fired, 1)
        self.assertIn("(moved, left in place)", str(cm.exception))
        self.assertEqual(self.read(os.path.join(fault.parked, "dst", "leaf")), b"payload")

    def test_destination_parent_moved_out_of_the_root_at_the_rename_is_refused_and_kept(self):
        parents = self.parents()
        away = os.path.join(self.base, "away")
        with no_deletes(), before_call("rename", 1, lambda: (os.rename(self.dst, away), os.mkdir(self.dst))):
            exc = self.refusal(lambda: self.move(parents=parents))
        self.assertIn("(moved, left in place)", str(exc))
        self.assertTrue(os.path.isfile(os.path.join(away, "leaf")))

    def test_root_moved_away_from_the_destination_at_the_rename_is_refused_and_kept(self):
        # The destination parent stays at its own path, but the held root no longer contains it.
        parents = self.parents()
        away = os.path.join(self.base, "away")

        def move_root_away():
            os.rename(self.root, away)
            os.mkdir(self.root)
            os.rename(os.path.join(away, "dst"), self.dst)
        with no_deletes(), before_call("rename", 1, move_root_away):
            exc = self.refusal(lambda: self.move(parents=parents))
        self.assertIn("inside no held root", str(exc))
        self.assertIn(f"{self.target} (moved, left in place)", str(exc))
        self.assertEqual(self.read(self.target), b"payload")

    def test_parents_or_root_rebound_before_the_call_are_refused_unmoved(self):
        for path in (self.src, self.dst, self.root):
            with self.subTest(path=path):
                root = fdsafe.hold_root(self.root)
                src, dst = fdsafe.hold_root(self.src), fdsafe.hold_root(self.dst)
                try:
                    with FK.rename_and_rebind(GETPATH, 1, path) as fault, \
                            never("rename") as renamed:
                        with self.assertRaises(fdsafe.Refusal) as cm:
                            fdsafe.rename(src, "leaf", dst, "leaf", [root])
                    renamed.assert_not_called()
                finally:
                    for d in (root, src, dst):
                        d.close()
                self.assertEqual(fault.fired, 1)
                self.assertIn("is held at", str(cm.exception))
                os.rmdir(path)
                os.rename(fault.parked, path)
                os.rmdir(os.path.dirname(fault.parked))
                self.assertUnmoved()

    def test_fifo_in_place_of_either_parent_is_refused(self):
        self.roots = [self.held()]
        for path in (self.src, self.dst):
            with self.subTest(path=path):
                src, dst = fdsafe.hold_root(self.src), fdsafe.hold_root(self.dst)
                try:
                    with FK.fifo_in_place(path, timeout=5) as fault, never("rename") as renamed:
                        exc = self.refusal(lambda: self.move(parents=(src, dst)))
                    renamed.assert_not_called()
                finally:
                    src.close()
                    dst.close()
                self.assertIn("is held at", str(exc))
                os.unlink(path)
                os.rename(fault.parked, path)
                os.rmdir(os.path.dirname(fault.parked))

    def test_errors_before_the_rename_are_refusals_and_move_nothing(self):
        # F_GETPATH order: root, src parent, dst parent (before); root, dst parent (after).
        cases = (("open", 1, self.leaf), ("fstat", 1, self.leaf), (GETPATH, 1, self.root),
                 (GETPATH, 2, self.src), (GETPATH, 3, self.dst))
        for name, n, path in cases:
            for err in (errno.EIO, errno.EBADF):
                with self.subTest(call=name, n=n, err=errno.errorcode[err]):
                    parents = self.parents()
                    with self.assertRaises(fdsafe.Refusal) as cm, FK.inject_oserror(name, n, err) as fault:
                        self.move(parents=parents)
                    self.assertEqual(fault.fired, 1)
                    self.assertEqual(cm.exception.path, path)
                    self.assertEqual(cm.exception.errno, err)
                    self.assertIn(repr(path), str(cm.exception))
                    self.assertUnmoved()

    def test_rename_error_is_a_refusal_naming_both_paths(self):
        for err in (errno.EIO, errno.ENOSPC):
            with self.subTest(err=errno.errorcode[err]):
                parents = self.parents()
                with self.assertRaises(fdsafe.Refusal) as cm, FK.inject_oserror("rename", 1, err) as fault:
                    self.move(parents=parents)
                self.assertEqual(fault.fired, 1)
                self.assertEqual(cm.exception.errno, err)
                self.assertIn(self.leaf, str(cm.exception))
                self.assertIn(self.target, str(cm.exception))
                self.assertUnmoved()

    def test_absent_check_error_is_a_refusal(self):
        parents = self.parents()
        with lstat_error(errno.EIO), never("rename") as renamed:
            exc = self.refusal(lambda: self.move(parents=parents), errno.EIO)
        renamed.assert_not_called()
        self.assertEqual(exc.path, self.target)

    def test_errors_after_the_rename_are_refusals_naming_the_kept_target(self):
        kept = f"{self.target} (moved, left in place)"
        cases = (("fstat", 2), (GETPATH, 4), (GETPATH, 5), ("close", 1))
        for name, n in cases:
            with self.subTest(call=name, n=n):
                parents = self.parents()
                with no_deletes(), self.assertRaises(fdsafe.Refusal) as cm, \
                        FK.inject_oserror(name, n, errno.EIO) as fault:
                    self.move(parents=parents)
                self.assertEqual(fault.fired, 1)
                self.assertEqual(cm.exception.errno, errno.EIO)
                self.assertIn(kept, str(cm.exception))
                self.assertEqual(self.read(self.target), b"payload")
                os.rename(self.target, self.leaf)
        parents = self.parents()
        with no_deletes(), lstat_error(errno.EIO, n=2):
            exc = self.refusal(lambda: self.move(parents=parents), errno.EIO)
        self.assertIn(kept, str(exc))

    def test_unexpected_errors_propagate_and_close(self):
        for call, n, exc_type in (("rename", 1, ValueError), ("fstat", 1, KeyError), (GETPATH, 3, RuntimeError)):
            with self.subTest(call=call):
                parents = self.parents()
                with no_deletes(), self.assertRaises(exc_type) as cm, FK.raise_unexpected(call, n, exc_type):
                    self.move(parents=parents)
                self.assertNotIsInstance(cm.exception, fdsafe.Refusal)
                self.assertUnmoved()

    def test_parent_live_checks_are_the_last_calls_before_the_rename(self):
        src, dst = self.parents()
        with traced() as log:
            self.move(parents=(src, dst))
        at = log.index(("rename", "leaf"))
        self.assertEqual(log[at - 2:at], [("getpath", src.fd), ("getpath", dst.fd)])


@contextlib.contextmanager
def after_call(func, n, action):
    """Run action() just after the Nth call of os.<func>, also when that call raises."""
    real, calls = getattr(os, func), [0]

    def hooked(*args, **kwargs):
        calls[0] += 1
        nth = calls[0] == n
        try:
            return real(*args, **kwargs)
        finally:
            if nth:
                action()
    with mock.patch.object(os, func, hooked):
        yield calls


class ExclusiveRename(Base):
    """fdsafe.rename's own exclusive call (RENAME_EXCL / RENAME_NOREPLACE), with no test routing (RULING.md ruling 1)."""
    parents = Rename.parents
    move = Rename.move
    assertUnmoved = Rename.assertUnmoved

    def setUp(self):
        super().setUp()
        self.src = self.mkdir("root/src")
        self.dst = self.mkdir("root/dst")
        self.leaf = self.put("root/src/leaf", b"payload")
        self.target = os.path.join(self.dst, "leaf")

    def test_target_created_between_the_absent_check_and_the_rename_is_never_overwritten(self):
        parents = self.parents()
        # os.lstat call 1 is the absent-target check; the racer's file appears right after it.
        with no_deletes(), after_call("lstat", 1, lambda: self.put("root/dst/leaf", b"racer")) as calls:
            exc = self.refusal(lambda: self.move(parents=parents), errno.EEXIST)
        self.assertGreaterEqual(calls[0], 1)
        self.assertIn(self.target, str(exc))
        self.assertEqual(self.read(self.target), b"racer")
        self.assertEqual(self.read(self.leaf), b"payload")

    def no_fallback(self):
        stack = contextlib.ExitStack()
        stack.enter_context(no_deletes())
        for func in ("rename", "replace", "link"):
            stack.enter_context(never(func))
        return stack

    def test_missing_exclusive_call_is_refused_without_a_fallback(self):
        parents = self.parents()
        with self.no_fallback(), mock.patch.object(fdsafe, "_NOREPLACE", None):
            exc = self.refusal(lambda: self.move(parents=parents), errno.ENOTSUP)
        self.assertIn(self.leaf, str(exc))
        self.assertIn(self.target, str(exc))
        self.assertUnmoved()

    def test_flag_rejected_by_the_filesystem_is_refused_without_a_fallback(self):
        for err in (errno.EINVAL, errno.ENOTSUP):
            with self.subTest(err=errno.errorcode[err]):
                parents = self.parents()

                def rejects(*args):
                    ctypes.set_errno(err)
                    return -1
                with self.no_fallback(), mock.patch.object(fdsafe, "_NOREPLACE", (rejects, fdsafe._NOREPLACE[1])):
                    exc = self.refusal(lambda: self.move(parents=parents), err)
                self.assertIn(self.target, str(exc))
                self.assertUnmoved()


if __name__ == "__main__":
    unittest.main()
