"""T353: admitted link bytes stay bound to the site's scanned inode."""
import contextlib
import ctypes
import os
from unittest import mock

import admitted_list as AL
import fault_kit as FK
from ops.migrate import fdsafe
import test_admitted_list as base


class ReadLink(base.Fixture):
    def setUp(self):
        super().setUp()
        self.path = os.path.join(self.repo, "reader")
        os.symlink("original", self.path)

    @contextlib.contextmanager
    def swapped_after_scan(self):
        real_stat, real_open, real_readlink = os.lstat, os.open, os.readlink
        scanned = []
        parked = self.path + ".parked"
        restored = False

        def scan(path, *args, **kwargs):
            st = real_stat(path, *args, **kwargs)
            if os.fsdecode(path) in (self.path, "reader") and not scanned:
                scanned.append(st)
                os.rename(self.path, parked)
                os.symlink("impostor", self.path)
                os.utime(self.path, ns=(st.st_atime_ns, st.st_mtime_ns), follow_symlinks=False)
                now = real_stat(self.path)
                # [LAW:behavior-not-structure] In the binding identity, only the inode differs.
                self.assertEqual((now.st_dev, now.st_size, now.st_mtime_ns),
                                 (st.st_dev, st.st_size, st.st_mtime_ns))
                self.assertNotEqual(now.st_ino, st.st_ino)
            return st

        def acquire(real):
            def call(path, *args, **kwargs):
                nonlocal restored
                result = real(path, *args, **kwargs)
                if scanned and not restored and os.fsdecode(path) in (self.path, "reader"):
                    os.replace(parked, self.path)
                    restored = True
                return result
            return call

        with mock.patch.object(os, "lstat", scan), \
                mock.patch.object(os, "open", acquire(real_open)), \
                mock.patch.object(os, "readlink", acquire(real_readlink)):
            yield
        self.assertEqual(len(scanned), 1)
        self.assertTrue(restored)

    def test_stable_link_returns_own_bytes_with_dir_fd(self):
        parent = os.open(self.repo, os.O_RDONLY | os.O_DIRECTORY)
        self.addCleanup(os.close, parent)
        self.assertEqual(AL.read_link_or_file("reader", dir_fd=parent), (b"original", True))

    def test_stable_link_preserves_non_utf8_bytes(self):
        path = os.path.join(self.outside, "raw")
        os.symlink(b"absent-\xff", os.fsencode(path))
        self.assertEqual(AL.read_link_or_file(path), (b"absent-\xff", True))

    def test_stable_link_main_writes_admitted_rows(self):
        code, text, err = self.run_cli({"add": [{"dst": "reader"}]})
        self.assertEqual((code, text, err), (0, "A\treader\n", ""))

    def test_aba_after_site_lstat_refuses(self):
        parent = os.open(self.repo, os.O_RDONLY | os.O_DIRECTORY)
        self.addCleanup(os.close, parent)
        with self.swapped_after_scan():
            with self.assertRaisesRegex(fdsafe.Refusal, "reader.*changed between scan and open"):
                AL.read_link_or_file("reader", dir_fd=parent)

    def test_aba_main_refuses_without_output(self):
        with self.swapped_after_scan():
            code, text, err = self.run_cli({"add": [{"dst": "reader"}]})
        self.assertEqual(code, 2, err)
        self.assertIsNone(text)
        self.assertIn("reader", err)
        self.assertIn("changed between scan and open", err)
        self.assertNotIn("impostor", err)

    def test_fifo_swap_refuses_without_blocking(self):
        try:
            with FK.fifo_in_place(self.path, name="open", n=2,
                                  match=lambda path, *a, **kw: path == self.path,
                                  timeout=0.5) as fault:
                with self.assertRaisesRegex(fdsafe.Refusal, "reader.*changed between scan and open"):
                    AL.read_link_or_file(self.path)
            self.assertEqual(fault.fired, 1)
        except FK.AttackTimeout as exc:
            self.fail("link read blocked on swapped FIFO: " + str(exc))

    def test_native_einval_main_refuses_without_output(self):
        regular_path = self.write("regular", b"not a link", root=self.outside)
        regular = os.open(regular_path, os.O_RDONLY)
        self.addCleanup(os.close, regular)
        real = fdsafe._freadlink

        def native_error(fd, size):
            ctypes.set_errno(0)
            return real(regular, size)

        # [LAW:no-silent-failure] Exercise libc's errno through the existing CLI refusal.
        with mock.patch.object(fdsafe, "_freadlink", native_error):
            code, text, err = self.run_cli({"add": [{"dst": "reader"}]})
        self.assertEqual(code, 2, err)
        self.assertIsNone(text)
        self.assertIn("reader", err)
        self.assertIn("[EINVAL]", err)
        self.assertEqual(len(err.splitlines()), 1)
