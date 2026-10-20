"""T354: reader_find reads the scanned link's bytes or refuses the race."""
import contextlib
import ctypes
import errno
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

import fault_kit as FK
from ops.migrate import fdsafe
import reader_find


class ReadLink(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory(prefix='reader-find-link-')
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name).resolve()
        self.path = self.root / 'reader'
        self.path.symlink_to('original')

    def cli(self):
        out, err = io.StringIO(), io.StringIO()
        with mock.patch.dict(os.environ, LLMDB_ROOT=str(self.root)), \
                contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            rc = reader_find.main(['--paths', 'reader', '--old', 'impostor'])
        return rc, out.getvalue(), err.getvalue()

    @contextlib.contextmanager
    def aba(self, *, relative_only=False):
        real_lstat, real_open, real_readlink = os.lstat, os.open, os.readlink
        parked = self.root / 'parked'
        fired, restored = [], []

        def scanned(name, *args, **kwargs):
            st = real_lstat(name, *args, **kwargs)
            named = name == self.path.name and kwargs.get('dir_fd') is not None
            absolute = not relative_only and os.fspath(name) == str(self.path)
            if not fired and (named or absolute):
                # [LAW:behavior-not-structure] Only inode changes among the four identity fields.
                self.path.rename(parked)
                self.path.symlink_to('impostor')
                os.utime(self.path, ns=(st.st_atime_ns, st.st_mtime_ns), follow_symlinks=False)
                changed = real_lstat(self.path)
                self.assertEqual((changed.st_dev, changed.st_size, changed.st_mtime_ns),
                                 (st.st_dev, st.st_size, st.st_mtime_ns))
                self.assertNotEqual(changed.st_ino, st.st_ino)
                fired.append(st)
            return st

        def after_acquire(real):
            def acquire(name, *args, **kwargs):
                result = real(name, *args, **kwargs)
                if fired and not restored and os.fspath(name) in (str(self.path), self.path.name):
                    self.path.unlink()
                    parked.rename(self.path)
                    restored.append(True)
                return result
            return acquire

        with mock.patch.object(os, 'lstat', scanned), \
                mock.patch.object(os, 'open', after_acquire(real_open)), \
                mock.patch.object(os, 'readlink', after_acquire(real_readlink)):
            yield
        self.assertEqual(len(fired), 1)
        self.assertEqual(restored, [True])
        self.assertEqual(real_readlink(self.path), 'original')

    def test_stable_missing_link_returns_text_bytes(self):
        self.assertEqual(reader_find.contents(self.path), b'original')

    def test_existing_target_is_not_read(self):
        (self.root / 'original').write_bytes(b'target contents must not be read')
        self.assertEqual(reader_find.contents(self.path), b'original')

    def test_cli_stable_link_through_in_root_parent_symlink(self):
        (self.root / 'inside').symlink_to(self.root, target_is_directory=True)
        tool = Path(reader_find.__file__).resolve()
        env = dict(os.environ, LLMDB_ROOT=str(self.root), PYTHONPATH=str(tool.parents[2]))
        result = subprocess.run(
            [sys.executable, '-B', str(tool), '--paths', 'inside/reader', '--old', 'original'],
            cwd=self.root, env=env, capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report['stale'], [
            {'file': 'inside/reader', 'line': 1, 'old': 'original', 'old_text': 'original'}])
        self.assertEqual(report['unverified'], [])
        self.assertEqual(result.stderr, '')

    def test_aba_after_lstat_refuses(self):
        with self.aba():
            with self.assertRaises(fdsafe.Refusal) as caught:
                reader_find.contents(self.path)
        self.assertEqual(caught.exception.path, str(self.path))
        self.assertIn('changed between scan and open', str(caught.exception))

    def test_cli_aba_outputs_no_impostor(self):
        with self.aba(relative_only=True):
            rc, out, err = self.cli()
            self.assertEqual(rc, 2, (out, err))
        self.assertEqual(out, '')
        self.assertIn(str(self.path), err)
        self.assertIn('changed between scan and open', err)
        self.assertNotIn('impostor', out)
        self.assertNotIn('Traceback', err)

    def test_fifo_swapped_for_link_refuses_without_blocking(self):
        try:
            with FK.fifo_in_place(
                    self.path, name='open', n=1, timeout=0.5,
                    match=lambda name, *a, **kw: name == self.path.name) as fault:
                with self.assertRaises(fdsafe.Refusal) as caught:
                    reader_find.contents(self.path)
            self.assertEqual(fault.fired, 1)
            self.assertEqual(caught.exception.path, str(self.path))
            self.assertIn('changed between scan and open', str(caught.exception))
        except FK.AttackTimeout as exc:
            self.fail('link open blocked on swapped FIFO: ' + str(exc))

    def test_native_einval_reaches_cli(self):
        regular = self.root / 'regular'
        regular.write_bytes(b'not a link')
        regular_fd = os.open(regular, os.O_RDONLY)
        self.addCleanup(os.close, regular_fd)
        real = fdsafe._freadlink

        def native_error(fd, size):
            ctypes.set_errno(0)
            return real(regular_fd, size)

        # [LAW:no-silent-failure] A real libc failure must reach the CLI's refusal boundary.
        with mock.patch.object(fdsafe, '_freadlink', side_effect=native_error) as fault:
            rc, out, err = self.cli()
        self.assertEqual(rc, 2, (out, err))
        self.assertEqual(fault.call_count, 1)
        self.assertEqual(out, '')
        self.assertIn('reader_find: refused:', err)
        self.assertIn(str(self.path), err)
        self.assertIn('[EINVAL]', err)
        self.assertEqual(len(err.splitlines()), 1)

    def test_parent_replaced_by_fifo_refuses_without_blocking(self):
        parent = self.root / 'parent'
        parent.mkdir()
        path = parent / 'reader'
        path.symlink_to('original')
        try:
            with FK.fifo_in_place(
                    parent, name='open', timeout=0.5,
                    match=lambda name, *a, **kw: name == parent) as fault:
                with self.assertRaises(OSError) as caught:
                    reader_find.contents(path)
            self.assertEqual(fault.fired, 1)
            self.assertEqual(caught.exception.errno, errno.ENOTDIR)
        except FK.AttackTimeout as exc:
            self.fail('parent open blocked on swapped FIFO: ' + str(exc))

    def test_unexpected_exception_is_not_a_cli_refusal(self):
        with FK.raise_unexpected(
                'open', 1, RuntimeError,
                match=lambda name, *a, **kw: name == self.root) as fault:
            with self.assertRaises(RuntimeError):
                self.cli()
        self.assertEqual(fault.fired, 1)


if __name__ == '__main__':
    unittest.main()
