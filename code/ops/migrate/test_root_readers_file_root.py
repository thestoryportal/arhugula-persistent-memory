"""Fixture-only checks for regular-file scan roots (Step 426)."""
import contextlib
import errno
import io
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

import fault_kit as FK
from ops.migrate import fdsafe, root_readers


class FileRoots(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory(prefix='file-roots-')
        self.addCleanup(tmp.cleanup)
        self.base = Path(tmp.name).resolve()
        self.root = self.base / 'repo'
        self.root.mkdir()
        self.home = self.base / 'home'
        self.home.mkdir()
        self.leaf = self.home / 'reader'
        self.old = self.base / 'old'
        self.new = self.base / 'new'
        self.data = str(self.old).encode() * 2 + b'\xff'
        self.leaf.write_bytes(self.data)
        self.registry = self.base / 'registry.tsv'
        self.registry.write_text('')
        self.report = self.home / 'report.json'

    def args(self, *extra):
        return ['--root', str(self.root), '--scan-root', str(self.leaf),
                '--old-root', str(self.old), '--registry', str(self.registry),
                '--stage', 'pre', '--report', str(self.report), *extra]

    def call(self, *extra):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            result = root_readers.main(self.args(*extra))
        return result, out.getvalue(), err.getvalue()

    def refused(self, result, word):
        self.assertEqual(result[:2], (2, ''), result)
        self.assertEqual(len(result[2].splitlines()), 1, result)
        self.assertIn(word, result[2])
        self.assertNotIn('Traceback', result[2])
        self.assertFalse(self.report.exists())

    def doc(self):
        return json.loads(self.report.read_bytes())

    def test_file_is_one_absolute_entry_and_inputs_unchanged(self):
        (self.home / 'unscanned-sibling').write_bytes(self.data)
        (self.root / 'inside').write_bytes(str(self.old).encode())
        before = fdsafe._identity(self.leaf.stat())
        self.assertEqual(self.call(), (1, '', ''))
        self.assertEqual(self.doc()['hits'], {str(self.leaf): 2, 'inside': 1})
        self.assertEqual(dict(self.doc()['classifications']),
                         {str(self.leaf): 'unregistered', 'inside': 'unregistered'})
        self.assertEqual(self.doc()['scan_roots'], [str(self.root), str(self.leaf)])
        self.assertEqual(self.doc()['skipped'], {'fifo': 0, 'socket': 0})
        self.assertEqual(self.leaf.read_bytes(), self.data)
        self.assertEqual(fdsafe._identity(self.leaf.stat()), before)

    def test_replace_measured_pre_and_post_counts(self):
        self.registry.write_text(f'REPLACE\t{self.leaf}\t{self.old}\t{self.new}\tmeasured\n')
        self.assertEqual(self.call(), (0, '', ''))
        self.assertEqual(self.doc()['classifications'], [[str(self.leaf), 'LIVE']])
        self.assertEqual(self.doc()['measured_counts'], [[0, 2]])
        self.assertEqual(self.doc()['counts'], sorted([
            [str(self.leaf), str(self.old), 2], [str(self.leaf), str(self.new), 0]]))
        self.leaf.write_bytes(str(self.new).encode() * 2)
        post = self.home / 'post.json'
        self.assertEqual(self.call('--stage', 'post', '--pre-report', str(self.report),
                                   '--report', str(post)), (0, '', ''))
        doc = json.loads(post.read_bytes())
        self.assertEqual(doc['findings'], [])
        self.assertEqual(doc['counts'], sorted([
            [str(self.leaf), str(self.old), 0], [str(self.leaf), str(self.new), 2]]))

    def test_record_and_component_boundary_with_sibling_file_roots(self):
        sibling = self.home / 'reader-other'
        sibling.write_bytes(self.data)
        self.registry.write_text(f'RECORD\t{self.leaf}\thistory\n')
        self.assertEqual(self.call('--scan-root', str(sibling), '--stage', 'post'), (1, '', ''))
        self.assertEqual(dict(self.doc()['classifications']),
                         {str(self.leaf): 'RECORD', str(sibling): 'unregistered'})
        self.assertEqual(self.doc()['scan_roots'],
                         [str(self.root), str(self.leaf), str(sibling)])

    def test_empty_file_has_zero_counts(self):
        self.leaf.write_bytes(b'')
        self.registry.write_text(f'REPLACE\t{self.leaf}\told\tnew\t0\n')
        self.assertEqual(self.call(), (0, '', ''))
        self.assertEqual(self.doc()['hits'], {})
        self.assertEqual(self.doc()['counts'],
                         [[str(self.leaf), 'new', 0], [str(self.leaf), 'old', 0]])

    def test_repo_root_still_refuses_regular_file(self):
        self.refused(self.call('--root', str(self.leaf)), 'ENOTDIR')

    def test_file_root_overlaps_duplicate_and_parent(self):
        for path in (self.leaf, self.home):
            with self.subTest(path=path):
                self.refused(self.call('--scan-root', str(path)), 'overlap')

    def test_file_root_inside_repo_refuses(self):
        self.refused(self.call('--root', str(self.home)), 'overlap')

    def test_folder_before_file_overlap_refuses(self):
        self.refused(self.call('--root', str(self.home), '--scan-root', str(self.root)), 'overlap')

    def test_nonregular_roots_refuse_with_errno(self):
        link = self.base / 'link'
        link.symlink_to(self.leaf)
        fifo = self.base / 'fifo'
        os.mkfifo(fifo)
        for path, error in ((link, 'ENOTDIR|ELOOP'), (fifo, 'ENOTDIR'),
                            (self.base / 'missing', 'ENOENT')):
            with self.subTest(path=path):
                result = self.call('--scan-root', str(path))
                self.refused(result, str(path))
                self.assertRegex(result[2], error)

    def test_socket_root_refuses(self):
        sock = socket.socket(socket.AF_UNIX)
        self.addCleanup(sock.close)
        cwd = os.getcwd()
        try:
            os.chdir(self.base)
            sock.bind('socket')
        finally:
            os.chdir(cwd)
        result = self.call('--scan-root', str(self.base / 'socket'))
        self.refused(result, str(self.base / 'socket'))
        self.assertIn('ENOTDIR', result[2])

    def test_link_in_parent_refuses(self):
        alias = self.base / 'alias'
        alias.symlink_to(self.base)
        self.refused(self.call('--scan-root', str(alias / 'home' / 'reader')), 'component is a link')

    def test_swap_for_link_between_scan_and_open_refuses(self):
        with FK.swap_for_symlink('open', 1, self.leaf, self.registry,
                                 match=lambda name, *a, **kw: name == self.leaf.name):
            self.refused(self.call(), 'ELOOP')

    def test_swap_for_fifo_between_scan_and_open_refuses(self):
        with FK.fifo_in_place(self.leaf, name='open',
                             match=lambda name, *a, **kw: name == self.leaf.name):
            self.refused(self.call(), 'changed between scan and open')

    def test_regular_replacement_between_scan_and_open_refuses(self):
        replacement = self.base / 'replacement'
        replacement.write_bytes(self.data)
        def swap(fault, original, args, kwargs):
            self.leaf.rename(self.home / 'parked')
            replacement.rename(self.leaf)
            return original(*args, **kwargs)
        with FK._at_call('open', 1, swap, lambda name, *a, **kw: name == self.leaf.name):
            self.refused(self.call(), 'changed between scan and open')

    def test_rewrite_during_read_refuses(self):
        def rewrite(fault, original, args, kwargs):
            data = original(*args, **kwargs)
            self.leaf.write_bytes(b'changed')
            return data
        with FK._at_call('read', 1, rewrite,
                         lambda fd, *a: fdsafe.live_path(fd, 'test') == str(self.leaf)):
            self.refused(self.call(), 'changed between scan and open/read')

    def test_parent_rebind_at_open_refuses(self):
        with FK.rename_and_rebind('open', 1, self.home,
                                 match=lambda name, *a, **kw: name == self.leaf.name):
            self.refused(self.call(), str(self.home))

    def test_scan_lstat_error_refuses(self):
        real = os.lstat
        def failing(path, *args, **kwargs):
            if os.fspath(path) == str(self.leaf):
                raise OSError(errno.EIO, os.strerror(errno.EIO))
            return real(path, *args, **kwargs)
        with mock.patch.object(os, 'lstat', failing):
            self.refused(self.call(), 'EIO')

    def test_file_read_error_refuses(self):
        with FK.inject_oserror('read', 1, errno.EIO,
                               match=lambda fd, *a: fdsafe.live_path(fd, 'test') == str(self.leaf)):
            self.refused(self.call(), 'EIO')

    def test_real_cli(self):
        self.registry.write_text(f'RECORD\t{self.leaf}\n')
        proc = subprocess.run([sys.executable, '-B', '-m', 'ops.migrate.root_readers', *self.args()],
                              capture_output=True, text=True, timeout=10, check=False)
        self.assertEqual((proc.returncode, proc.stdout, proc.stderr), (0, '', ''))
        self.assertEqual(self.doc()['hits'], {str(self.leaf): 2})

    def test_relative_file_root_has_absolute_key(self):
        self.registry.write_text(f'RECORD\t{self.leaf}\n')
        args = self.args()
        args[3] = os.path.relpath(self.leaf)
        proc = subprocess.run([sys.executable, '-B', '-m', 'ops.migrate.root_readers', *args],
                              capture_output=True, text=True, timeout=10, check=False)
        self.assertEqual((proc.returncode, proc.stdout, proc.stderr), (0, '', ''))
        self.assertEqual(self.doc()['hits'], {str(self.leaf): 2})
        self.assertEqual(self.doc()['scan_roots'], [str(self.root), str(self.leaf)])

    def test_report_cannot_overwrite_file_root(self):
        self.refused(self.call('--report', str(self.leaf)), 'EEXIST')
        self.assertEqual(self.leaf.read_bytes(), self.data)

    def test_report_at_parked_file_root_refuses_and_stays_untouched(self):
        self.report = self.leaf
        self.registry.write_text(f'RECORD\t{self.leaf}\n')
        parked = self.home / 'saved-reader'
        written = []
        real_write = fdsafe.write_held
        def capture(held, data):
            real_write(held, data)
            written.append((self.leaf.read_bytes(), self.leaf.stat().st_ino))
        def park(fault, original, args, kwargs):
            self.leaf.rename(parked)
            return original(*args, **kwargs)
        with FK._at_call('open', 1, park,
                         lambda name, flags, *a, **kw:
                         name == self.leaf.name and bool(flags & os.O_CREAT)), \
                mock.patch.object(fdsafe, 'write_held', capture), \
                mock.patch.object(os, 'unlink', wraps=os.unlink) as unlink, \
                mock.patch.object(os, 'remove', wraps=os.remove) as remove:
            result = self.call()
        self.assertEqual(result[:2], (2, ''), result)
        self.assertEqual(result[2].splitlines(),
                         [f"{str(self.leaf)!r}: was written inside root {self.leaf}; left in place"])
        self.assertNotIn('PASS', ''.join(result[1:]))
        self.assertEqual(len(written), 1)
        self.assertEqual((self.leaf.read_bytes(), self.leaf.stat().st_ino), written[0])
        self.assertEqual(json.loads(written[0][0])['hits'], {str(self.leaf): 2})
        self.assertEqual(parked.read_bytes(), self.data)
        unlink.assert_not_called()
        remove.assert_not_called()

    def test_parent_rebind_at_leaf_close_refuses(self):
        self.registry.write_text(f'RECORD\t{self.leaf}\n')
        with FK.rename_and_rebind('close', 1, self.home,
                                 match=lambda fd, *a:
                                 fdsafe.live_path(fd, 'test') == str(self.leaf)):
            self.refused(self.call(), 'is held at')

    def test_replacement_before_parent_open_keeps_scanned_identity(self):
        self.registry.write_text(f'RECORD\t{self.leaf}\n')
        replacement = self.base / 'replacement'
        replacement.write_bytes(str(self.old).encode() * 7)
        def swap(fault, original, args, kwargs):
            self.leaf.rename(self.home / 'saved-reader')
            replacement.rename(self.leaf)
            return original(*args, **kwargs)
        with FK._at_call('open', 1, swap,
                         lambda name, *a, **kw: name == str(self.home)):
            self.refused(self.call(), 'changed between scan and open/read')

    def test_file_root_fds_close_on_pass_and_refusal(self):
        before = len(os.listdir('/dev/fd'))
        self.assertEqual(self.call(), (1, '', ''))
        self.assertEqual(len(os.listdir('/dev/fd')), before)
        result = self.call('--scan-root', str(self.leaf))
        self.assertEqual(result[:2], (2, ''))
        self.assertIn('overlap', result[2])
        self.assertEqual(len(os.listdir('/dev/fd')), before)


if __name__ == '__main__':
    unittest.main()
