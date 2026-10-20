"""T351: split binds link text to the inode observed by the scan."""
import contextlib
import ctypes
import os
from unittest import mock

import fault_kit as FK
from ops.migrate import fdsafe
import record_split as R
from test_record_split import Fixture


class ReadLink(Fixture):
    def test_stable_link_preserves_text_and_classification(self):
        text = os.fsdecode(b"missing-\xff")
        os.symlink(text, self.unit / "alias")
        self.assertEqual(self.split(), {
            "alias": R.Row("alias", R.TRACKED, "link", None, None, text),
        })

    def test_aba_after_scan_refuses_impostor_text(self):
        path = self.unit / "alias"
        parked = self.base / "parked"
        os.symlink("original", path)
        real_scandir, real_open, real_readlink = os.scandir, os.open, os.readlink
        scanned = []
        restored = []
        case = self

        def restore():
            path.unlink()
            parked.rename(path)
            restored.append(True)

        class Entry:
            def __init__(self, entry):
                self.entry = entry
                self.name = entry.name

            def stat(self, **kwargs):
                st = self.entry.stat(**kwargs)
                # [LAW:behavior-not-structure] Swap after the real scan stat, before any later lstat/open.
                if self.name == "alias" and not scanned:
                    scanned.append(st)
                    path.rename(parked)
                    os.symlink("impostor", path)
                    os.utime(path, ns=(st.st_atime_ns, st.st_mtime_ns), follow_symlinks=False)
                    now = os.lstat(path)
                    fields = ("st_dev", "st_ino", "st_size", "st_mtime_ns")
                    case.assertEqual([f for f in fields if getattr(st, f) != getattr(now, f)],
                                     ["st_ino"])
                return st

        @contextlib.contextmanager
        def listing(fd):
            with real_scandir(fd) as entries:
                yield (Entry(entry) for entry in entries)

        def acquired(real):
            def hook(name, *args, **kwargs):
                result = real(name, *args, **kwargs)
                if name == "alias" and scanned and not restored:
                    restore()
                return result
            return hook

        rows = []
        try:
            with mock.patch.object(os, "scandir", listing), \
                    mock.patch.object(os, "open", acquired(real_open)), \
                    mock.patch.object(os, "readlink", acquired(real_readlink)):
                with self.assertRaisesRegex(R.Refusal, "changed between scan and open") as caught:
                    rows.extend(R.split_unit(self.unit, []))
            self.assertIn(str(path), str(caught.exception))
        finally:
            if scanned and not restored:
                restore()
        self.assertEqual(len(scanned), 1)
        self.assertEqual(restored, [True])
        self.assertEqual(rows, [])
        self.assertEqual(real_readlink(path), "original")

    def test_fifo_swapped_for_link_refuses_without_blocking(self):
        path = self.unit / "alias"
        os.symlink("original", path)
        try:
            with FK.fifo_in_place(path, name="open", n=1,
                                  match=lambda name, *a, **kw: name == "alias",
                                  timeout=0.5) as fault:
                with self.assertRaisesRegex(R.Refusal, "changed between scan and open") as caught:
                    self.split()
            self.assertEqual(fault.fired, 1)
            self.assertIn(str(path), str(caught.exception))
        except FK.AttackTimeout as exc:
            self.fail("link open blocked on swapped FIFO: " + str(exc))

    def test_native_einval_reaches_split_refusal(self):
        path = self.unit / "alias"
        os.symlink("original", path)
        regular = self.base / "regular"
        regular.write_bytes(b"not a link")
        fd = os.open(regular, os.O_RDONLY)
        self.addCleanup(os.close, fd)
        real = fdsafe._freadlink

        def native_error(link_fd, size):
            ctypes.set_errno(0)
            return real(fd, size)

        # [LAW:no-silent-failure] Keep libc's real errno through the site's refusal boundary.
        with mock.patch.object(fdsafe, "_freadlink", side_effect=native_error) as fault:
            with self.assertRaisesRegex(R.Refusal, r"\[EINVAL\]") as caught:
                self.split()
        self.assertEqual(fault.call_count, 1)
        self.assertIn(str(path), str(caught.exception))
