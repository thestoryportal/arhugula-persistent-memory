"""T350: late git-add binds link text to the inode from its scan."""
import ctypes
import os
import unittest
from unittest import mock

import fault_kit as FK
from ops.migrate import fdsafe
import test_move_unit_run as run


class LateAddLink(run.Base):
    def setUp(self):
        super().setUp()
        os.symlink("notes.txt", self.u.source + "/link.txt")
        self.u.files["link.txt"] = b"notes.txt"
        self.fx.seal()
        self.target = self.fx.target(self.u) + "/link.txt"

    def late_link(self, name, *args, **kwargs):
        return (name == "link.txt" and kwargs.get("dir_fd") is not None
                and fdsafe.live_path(kwargs["dir_fd"], self.target)
                == os.path.dirname(self.target))

    def refused_unstaged(self, result, reason):
        self.assert_refused(result, self.target, reason)
        self.assertEqual(run.git(self.fx.m, "ls-files", "-s", "--", self.target), b"")
        self.assertNotIn("other.txt", "".join(result[1:]))

    def test_stable_link_stages_own_text_and_mode(self):
        # [LAW:behavior-not-structure] Inspect the real index and blob, not the reader call.
        self.run_ok()
        row = run.git(self.fx.m, "ls-files", "-s", "--", self.target).split()
        self.assertEqual(row[0], b"120000")
        self.assertEqual(run.git(self.fx.m, "cat-file", "blob", row[1].decode()), b"notes.txt")

    def test_aba_after_lstat_with_only_inode_changed_refuses(self):
        real_lstat, real_open, real_readlink = os.lstat, os.open, os.readlink
        parked = self.fx.base + "/parked-link"
        scanned = []
        restored = []

        def swap(name, *args, **kwargs):
            st = real_lstat(name, *args, **kwargs)
            if self.late_link(name, *args, **kwargs) and not scanned:
                scanned.append(st)
                os.rename(self.target, parked)
                os.symlink("other.txt", self.target)
                os.utime(self.target, ns=(st.st_atime_ns, st.st_mtime_ns), follow_symlinks=False)
                now = real_lstat(self.target)
                # [LAW:verifiable-goals] Of the four identity fields, only inode may differ.
                self.assertEqual((now.st_dev, now.st_size, now.st_mtime_ns),
                                 (st.st_dev, st.st_size, st.st_mtime_ns))
                self.assertNotEqual(now.st_ino, st.st_ino)
            return st

        def restore_after(real):
            def read(name, *args, **kwargs):
                late = self.late_link(name, *args, **kwargs)
                result = real(name, *args, **kwargs)
                if late and scanned and not restored:
                    os.unlink(self.target)
                    os.rename(parked, self.target)
                    restored.append(True)
                return result
            return read

        # [LAW:behavior-not-structure] Both readers face the same ABA; a later lstat sees the impostor.
        with mock.patch.object(os, "lstat", swap), \
                mock.patch.object(os, "open", restore_after(real_open)), \
                mock.patch.object(os, "readlink", restore_after(real_readlink)):
            result = self.main(*self.fx.args())
        self.assertEqual(len(scanned), 1)
        self.assertEqual(restored, [True])
        self.assertEqual(os.readlink(self.target), "notes.txt")
        self.refused_unstaged(result, "changed between scan and open")

    def test_fifo_between_scan_and_open_refuses_without_blocking(self):
        try:
            with FK.fifo_in_place(self.target, name="open", n=1,
                                  match=self.late_link, timeout=0.5) as fault:
                result = self.main(*self.fx.args())
            self.assertEqual(fault.fired, 1)
        except FK.AttackTimeout as exc:
            self.fail("late git-add blocked on FIFO: " + str(exc))
        self.refused_unstaged(result, "changed between scan and open")

    def test_native_einval_names_target(self):
        regular = os.open(self.u.source + "/notes.txt", os.O_RDONLY)
        self.addCleanup(os.close, regular)
        real = fdsafe._freadlink

        def invalid(fd, size):
            ctypes.set_errno(0)
            return real(regular, size)

        # [LAW:no-silent-failure] The native errno must reach the command refusal.
        with mock.patch.object(fdsafe, "_freadlink", side_effect=invalid) as hook:
            result = self.main(*self.fx.args())
        self.assertEqual(hook.call_count, 1)
        self.refused_unstaged(result, "[EINVAL]")


if __name__ == "__main__":
    unittest.main()
