"""T352: manifest link text belongs to the scanned inode."""
import ctypes
import hashlib
import json
import os
from unittest import mock

import fault_kit as FK
from ops.migrate import fdsafe
from test_unit_manifest import Base


class ManifestReadLink(Base):
    def setUp(self):
        super().setUp()
        self.link = self.unit / "ln"
        os.symlink("original", self.link)

    def assert_refused(self, result, needle):
        code, out, err = result
        reason = self.assert_json_fail(code, out, needle, err)["reason"]
        self.assertIn(str(self.link), reason)
        self.assertEqual(err, "")
        self.assertFalse(os.path.lexists(self.out))
        self.assertNotIn("replaced", out + err)

    def test_stable_link_hashes_its_text(self):
        code, out, err = self.run_inproc()
        self.assertEqual(code, 0, out + err)
        self.assertEqual(json.loads(out)["status"], "PASS")
        leaf, = json.loads(self.out.read_bytes())["leaves"]
        self.assertEqual(leaf["kind"], "symlink")
        self.assertEqual(leaf["link_text"], "original")
        self.assertEqual(leaf["sha256"], hashlib.sha256(b"original").hexdigest())

    def test_aba_after_scan_refuses_same_length_impostor(self):
        self.assert_aba_refused()

    def assert_aba_refused(self):
        real_lstat, real_open, real_readlink = os.lstat, os.open, os.readlink
        parked = self.tmp / "parked"
        fired, restored, reads = [], [], []

        def restore():
            os.replace(parked, self.link)
            restored.append(True)

        def scanned(path, *args, **kwargs):
            st = real_lstat(path, *args, **kwargs)
            if not fired and os.fspath(path) == str(self.link):
                fired.append(True)
                os.rename(self.link, parked)
                os.symlink("replaced", self.link)
                os.utime(self.link, ns=(st.st_atime_ns, st.st_mtime_ns), follow_symlinks=False)
                now = real_lstat(self.link)
                # [LAW:behavior-not-structure] Inode alone distinguishes the scan identity from the impostor.
                self.assertEqual((now.st_dev, now.st_size, now.st_mtime_ns),
                                 (st.st_dev, st.st_size, st.st_mtime_ns))
                self.assertNotEqual(now.st_ino, st.st_ino)
            return st

        def opened(path, *args, **kwargs):
            fd = real_open(path, *args, **kwargs)
            if fired and not restored and os.fspath(path) == "ln":
                restore()
            return fd

        def readlink(path, *args, **kwargs):
            text = real_readlink(path, *args, **kwargs)
            if fired and not restored:
                reads.append(text)
                if len(reads) == 2:
                    restore()
            return text

        # [LAW:verifiable-goals] Swap after the scan, before either reader; restore to defeat a path after-check.
        try:
            with mock.patch.object(os, "lstat", scanned), mock.patch.object(os, "open", opened), \
                    mock.patch.object(os, "readlink", readlink):
                result = self.run_inproc()
        finally:
            if fired and not restored:
                restore()
        self.assertEqual(fired, [True])
        self.assertEqual(real_readlink(self.link), "original")
        self.assert_refused(result, "changed between scan and open")

    def test_post_open_swap_keeps_original_text_and_hash(self):
        with FK.swap_for_symlink("open", 1, self.link, "replaced", when="after",
                                 match=lambda path, *a, **kw: path == "ln" and "dir_fd" in kw) as fault:
            code, out, err = self.run_inproc()
        self.assertEqual(fault.fired, 1)
        self.assertEqual(code, 0, out + err)
        raw = self.out.read_bytes()
        leaf, = json.loads(raw)["leaves"]
        # [LAW:behavior-not-structure] Both manifest values must come from the held link, despite the new path.
        self.assertEqual(leaf["link_text"], "original")
        self.assertEqual(leaf["sha256"], hashlib.sha256(b"original").hexdigest())
        self.assertNotIn("replaced", out + err + raw.decode())

    def test_link_fds_close_after_success_and_refusal(self):
        before = len(os.listdir("/dev/fd"))
        code, out, err = self.run_inproc()
        self.assertEqual(code, 0, out + err)
        self.out = self.tmp / "refused.json"
        self.assert_aba_refused()
        # [LAW:verifiable-goals] Success and refusal must both release their link descriptors.
        self.assertEqual(len(os.listdir("/dev/fd")), before)

    def test_fifo_swapped_before_open_refuses_without_blocking(self):
        try:
            with FK.fifo_in_place(self.link, name="open", n=1,
                                  match=lambda path, *a, **kw: path == "ln", timeout=0.5) as fault:
                result = self.run_inproc()
            self.assertEqual(fault.fired, 1)
        except FK.AttackTimeout as exc:
            self.fail("link open blocked on swapped FIFO: " + str(exc))
        self.assert_refused(result, "changed between scan and open")

    def test_native_einval_is_json_refusal(self):
        regular = self.tmp / "regular"
        regular.write_bytes(b"not a link")
        fd = os.open(regular, os.O_RDONLY)
        self.addCleanup(os.close, fd)
        real = fdsafe._freadlink

        def invalid(link_fd, size):
            ctypes.set_errno(0)
            return real(fd, size)

        # [LAW:no-silent-failure] A real libc error must reach the public refusal, without a traceback.
        with mock.patch.object(fdsafe, "_freadlink", invalid):
            result = self.run_inproc()
        self.assert_refused(result, "[EINVAL]")

    def test_unexpected_link_read_error_propagates(self):
        # [LAW:no-silent-failure] Programming errors must not become ordinary filesystem refusals.
        with mock.patch.object(fdsafe, "_freadlink", side_effect=RuntimeError("unexpected read failure")):
            with self.assertRaisesRegex(RuntimeError, "unexpected read failure"):
                self.run_inproc()
        self.assertFalse(os.path.lexists(self.out))
