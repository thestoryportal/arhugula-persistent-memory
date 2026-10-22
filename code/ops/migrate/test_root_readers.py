"""Fixture-only reader shell tests; faults target filesystem seams, not the core."""
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
from ops.migrate import root_readers, fdsafe


class Readers(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory(prefix='readers-')
        self.addCleanup(tmp.cleanup)
        self.base = Path(tmp.name).resolve()
        self.root = self.base / 'repo'
        self.root.mkdir()
        self.old = self.base / 'old'
        self.registry = self.base / 'registry.tsv'
        self.registry.write_text('')
        self.report = self.base / 'report.json'
        self.leaf = self.root / 'leaf'
        self.leaf.write_bytes(b'clean')

    def args(self, *extra):
        return ['--root', str(self.root), '--old-root', str(self.old),
                '--registry', str(self.registry), '--stage', 'pre',
                '--report', str(self.report), *extra]

    def call(self, *extra):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            result = root_readers.main(self.args(*extra))
        return result, out.getvalue(), err.getvalue()

    def doc(self):
        return json.loads(self.report.read_bytes())

    def refused(self, result, word):
        self.assertEqual(result[:2], (2, ''), result)
        self.assertEqual(len(result[2].splitlines()), 1, result)
        self.assertIn(word, result[2])
        self.assertNotIn('Traceback', result[2])

    def test_binary_hit_and_no_input_write(self):
        data = b'\0' + str(self.old).encode() + b'\xff'
        self.leaf.write_bytes(data)
        before = self.leaf.stat()
        self.assertEqual(self.call(), (1, '', ''))
        self.assertEqual(self.doc()['hits'], {'leaf': 1})
        self.assertEqual(self.doc()['classifications'], [['leaf', 'unregistered']])
        self.assertEqual(self.leaf.read_bytes(), data)
        self.assertEqual(fdsafe._identity(self.leaf.stat()), fdsafe._identity(before))
        self.assertEqual(sorted(p.name for p in self.base.iterdir()),
                         ['registry.tsv', 'repo', 'report.json'])

    def test_pre_replace_record_and_component_boundary(self):
        self.registry.write_text(f'REPLACE\tleaf\t{self.old}\tnew\t2\nRECORD\thistory\n')
        self.leaf.write_bytes(str(self.old).encode() * 2)
        (self.root / 'history').mkdir()
        (self.root / 'history' / 'x').write_bytes(str(self.old).encode())
        (self.root / 'history-live').write_bytes(str(self.old).encode())
        self.assertEqual(self.call(), (1, '', ''))
        self.assertEqual(dict(self.doc()['classifications']),
                         {'leaf': 'LIVE', 'history/x': 'RECORD', 'history-live': 'unregistered'})
        self.assertEqual(self.doc()['findings'], ['history-live: unregistered'])

    def test_pre_pass_and_count_mismatch(self):
        self.registry.write_text('REPLACE\tleaf\tclean\tnew\t1\n')
        self.assertEqual(self.call(), (0, '', ''))
        self.assertEqual(self.doc()['findings'], [])
        self.assertEqual(self.doc()['counts'], [['leaf', 'clean', 1], ['leaf', 'new', 0]])
        self.refused(self.call(), 'EEXIST')
        self.leaf.write_bytes(b'clean clean')
        self.assertEqual(self.call('--report', str(self.base / 'mismatch')), (1, '', ''))

    def test_post_and_measured_snapshot(self):
        self.registry.write_text(f'REPLACE\tleaf\t{self.old}\tnew\tmeasured\n')
        self.leaf.write_bytes(str(self.old).encode() * 2)
        self.assertEqual(self.call(), (0, '', ''))
        self.assertEqual(self.doc()['measured_counts'], [[0, 2]])
        self.leaf.write_bytes(b'newnew')
        post = self.base / 'post'
        self.assertEqual(self.call('--stage', 'post', '--pre-report', str(self.report),
                                   '--report', str(post)), (0, '', ''))
        self.old.mkdir()
        self.assertEqual(self.call('--stage', 'post', '--pre-report', str(self.report),
                                   '--report', str(self.base / 'post2')), (1, '', ''))
        self.assertIn('old root still exists', json.loads((self.base / 'post2').read_bytes())['findings'])

    def test_missing_measured_snapshot_refuses(self):
        self.registry.write_text('REPLACE\tleaf\told\tclean\tmeasured\n')
        self.refused(self.call('--stage', 'post'), 'missing pre-stage')

    def test_missing_registered_file_refuses(self):
        self.registry.write_text('REPLACE\tmissing\told\tnew\t1\n')
        self.refused(self.call(), 'missing count')
        self.assertFalse(self.report.exists())

    def test_additional_root_absolute_keys_and_one_walk_each(self):
        outside = self.base / 'outside'
        outside.mkdir()
        (outside / 'x').write_bytes(str(self.old).encode())
        self.registry.write_text(f'RECORD\t{outside}\n')
        real = os.scandir
        scanned = []
        def watch(fd):
            scanned.append(fdsafe.live_path(fd, 'test'))
            return real(fd)
        with mock.patch.object(os, 'scandir', watch):
            self.assertEqual(self.call('--scan-root', str(outside)), (0, '', ''))
        self.assertEqual(scanned, [str(self.root), str(outside)])
        self.assertEqual(self.doc()['hits'], {str(outside / 'x'): 1})

    def test_links_are_read_but_never_followed(self):
        outside = self.base / 'outside'
        outside.mkdir()
        (outside / 'hit').write_bytes(str(self.old).encode())
        (self.root / 'linkdir').symlink_to(outside)
        (self.root / 'broken').symlink_to(self.old)
        self.assertEqual(self.call(), (1, '', ''))
        self.assertEqual(self.doc()['hits'], {'broken': 1})
        self.assertEqual(self.doc()['skipped'], {'fifo': 0, 'socket': 0})

    def test_fifo_and_socket_skipped_counted(self):
        os.mkfifo(self.root / 'fifo')
        sock = socket.socket(socket.AF_UNIX)
        self.addCleanup(sock.close)
        # Darwin's socket address limit is shorter than guard_mutants' TMPDIR.
        cwd = os.getcwd()
        try:
            os.chdir(self.root)
            sock.bind('socket')
        finally:
            os.chdir(cwd)
        self.assertEqual(self.call(), (0, '', ''))
        self.assertEqual(self.doc()['skipped'], {'fifo': 1, 'socket': 1})

    def test_report_inside_scan_refuses(self):
        self.refused(self.call('--report', str(self.root / 'report')), 'inside root')
        self.assertFalse((self.root / 'report').exists())

    def test_report_symlink_preserved(self):
        self.report.symlink_to(self.leaf)
        self.refused(self.call(), 'EEXIST')
        self.assertTrue(self.report.is_symlink())
        self.assertEqual(self.leaf.read_bytes(), b'clean')

    def test_overlapping_roots_refuse(self):
        child = self.root / 'child'
        child.mkdir()
        for root in (self.root, child, self.base):
            with self.subTest(root=root):
                self.refused(self.call('--scan-root', str(root)), 'overlap')

    def test_registry_malformed_and_non_utf8_refuse(self):
        for data in (b'BOGUS\tx', b'\xff'):
            self.registry.write_bytes(data)
            self.refused(self.call(), 'EINVAL')

    def test_invalid_pre_reports_refuse(self):
        pre = self.base / 'pre'
        for text in ('{', '[]', '{}', '{"stage":"post"}',
                     '{"stage":"pre"}', '{"stage":"pre","measured_counts":{}}',
                     '{"stage":"pre","measured_counts":[1]}',
                     '{"stage":"pre","measured_counts":[[0]]}',
                     '{"stage":"pre","measured_counts":[["0",1]]}',
                     '{"stage":"pre","measured_counts":[[0,1],[0,2]]}'):
            with self.subTest(text=text):
                pre.write_text(text)
                self.refused(self.call('--pre-report', str(pre)), 'EINVAL')
                self.assertFalse(self.report.exists())

    def test_invalid_old_root_refuses(self):
        for value in ('', 'relative'):
            with self.subTest(value=value):
                self.refused(self.call('--old-root', value), 'EINVAL')

    def test_non_utf8_record_reason_is_not_replaced(self):
        self.registry.write_bytes(b'RECORD\thistory\t\xff\n')
        self.refused(self.call(), 'expected UTF-8 metadata')

    def test_duplicate_valid_measured_index_refuses(self):
        self.registry.write_text('REPLACE\tleaf\tclean\tnew\tmeasured\n')
        pre = self.base / 'pre'
        pre.write_text('{"stage":"pre","measured_counts":[[0,1],[0,1]]}')
        self.refused(self.call('--pre-report', str(pre)), 'duplicate measured index')

    def test_unencodable_old_root_never_replaces_bytes(self):
        with self.assertRaises(UnicodeEncodeError):
            self.call('--old-root', str(self.base / '\udcff'))

    def test_relative_metadata_and_report_cwd_errors_refuse(self):
        for flag, value in (('--registry', 'registry.tsv'), ('--report', 'report.json')):
            with self.subTest(flag=flag):
                with mock.patch.object(os, 'getcwd', side_effect=OSError(errno.EIO, os.strerror(errno.EIO))):
                    self.refused(self.call(flag, value), 'EIO')
        with mock.patch.object(os, 'getcwd', side_effect=OSError(errno.EIO, os.strerror(errno.EIO))):
            with self.assertRaises(fdsafe.Refusal) as caught:
                root_readers.exists('old')
        self.assertEqual(caught.exception.errno, errno.EIO)

    def test_pre_report_unexpected_read_errors_propagate(self):
        pre = self.base / 'pre'
        pre.write_text('{"stage":"pre","measured_counts":[]}')
        for exc in FK.UNEXPECTED:
            with self.subTest(exc=exc):
                with FK.raise_unexpected('read', 1, exc,
                                         match=lambda fd, *a: fdsafe.live_path(fd, 'test') == str(pre)):
                    with self.assertRaises(exc) as caught:
                        self.call('--pre-report', str(pre))
                self.assertNotIsInstance(caught.exception, fdsafe.Refusal)

    def test_old_root_unexpected_stat_error_propagates(self):
        real = os.lstat
        def failing(path, *a, **kw):
            if path == 'old':
                raise RuntimeError('stat bug')
            return real(path, *a, **kw)
        with mock.patch.object(os, 'lstat', failing):
            with self.assertRaisesRegex(RuntimeError, 'stat bug'):
                self.call()

    def test_old_root_lstat_error_is_not_absence(self):
        real = os.lstat
        def failing(path, *a, **kw):
            if path == 'old':
                raise OSError(errno.EIO, os.strerror(errno.EIO))
            return real(path, *a, **kw)
        with mock.patch.object(os, 'lstat', failing):
            self.refused(self.call('--stage', 'post'), 'EIO')
        self.assertFalse(self.report.exists())

    def test_dangling_old_root_counts_as_existing(self):
        self.old.symlink_to(self.base / 'absent')
        self.assertEqual(self.call('--stage', 'post'), (1, '', ''))
        self.assertEqual(self.doc()['findings'], ['old root still exists'])

    def test_existing_old_root_with_trailing_separator_is_not_absent(self):
        self.old.mkdir()
        self.assertEqual(self.call('--stage', 'post', '--old-root', str(self.old) + '/'), (1, '', ''))
        self.assertEqual(self.doc()['findings'], ['old root still exists'])

    def test_malformed_registry_names_its_file_and_line(self):
        self.registry.write_text('BOGUS\tx\n')
        result = self.call()
        self.refused(result, str(self.registry))
        self.assertIn('registry line 1', result[2])

    def test_empty_root_renamed_after_scan_refuses(self):
        empty = self.base / 'empty'
        empty.mkdir()
        with FK.rename_and_rebind('scandir', 2, empty, when='after'):
            self.refused(self.call('--scan-root', str(empty)), 'held at')

    def test_output_parent_rebound_keeps_report_in_held_directory(self):
        out = self.base / 'output'
        out.mkdir()
        with FK.rename_and_rebind('write', 1, out, when='after') as fault:
            result = self.call('--report', str(out / 'report'))
        # The held output stays in the original directory; it is never redirected.
        self.assertEqual(result, (0, '', ''))
        self.assertFalse((out / 'report').exists())
        self.assertEqual(json.loads((Path(fault.parked) / 'report').read_bytes())['findings'], [])

    def test_output_parent_moved_into_scan_root_refuses(self):
        out = self.base / 'output'
        out.mkdir()
        real = os.write
        def moved(fd, data):
            result = real(fd, data)
            os.rename(out, self.root / 'moved')
            return result
        with mock.patch.object(os, 'write', moved):
            self.refused(self.call('--report', str(out / 'report')), 'inside root')
        self.assertTrue((self.root / 'moved' / 'report').exists())

    def test_output_close_error_names_kept_report(self):
        real = os.close
        def failing(fd):
            path = fdsafe.live_path(fd, 'test')
            real(fd)
            if path == str(self.report):
                raise OSError(errno.EIO, os.strerror(errno.EIO))
        with mock.patch.object(os, 'close', failing):
            self.refused(self.call(), 'created, left in place')
        self.assertEqual(self.doc()['findings'], [])

    def test_byte_hit_across_read_boundary(self):
        data = b'x' * (fdsafe.CHUNK - 2) + str(self.old).encode() + b'\xff'
        self.leaf.write_bytes(data)
        self.assertEqual(self.call(), (1, '', ''))
        self.assertEqual(self.doc()['hits'], {'leaf': 1})

    def test_cli_real_process(self):
        proc = subprocess.run([sys.executable, '-B', '-m', 'ops.migrate.root_readers', *self.args()],
                              capture_output=True, text=True, check=False)
        self.assertEqual((proc.returncode, proc.stdout, proc.stderr), (0, '', ''))
        self.assertEqual(self.doc()['findings'], [])

    def test_leaf_swap_link_and_fifo_refuse(self):
        decoy = self.base / 'decoy'
        decoy.write_bytes(b'clean')
        match = lambda name, *a, **kw: name == 'leaf'
        with FK.swap_for_symlink('open', 1, self.leaf, decoy, match=match):
            result = self.call()
        self.refused(result, 'ELOOP')

    def test_fifo_swap_after_scan_refuses(self):
        with FK.fifo_in_place(self.leaf, name='open', match=lambda name, *a, **kw: name == 'leaf'):
            result = self.call()
        self.refused(result, 'changed between scan and open')

    def test_root_link_and_fifo_refuse(self):
        with FK.fifo_in_place(self.root):
            result = self.call()
        self.refused(result, 'ENOTDIR')

    def test_root_swap_refuses(self):
        other = self.base / 'other'
        other.mkdir()
        with FK.swap_for_symlink('open', 1, self.root, other,
                                 match=lambda name, *a, **kw: name == str(self.root)):
            result = self.call()
        self.refused(result, str(self.root))

    def test_root_rename_and_rebind_refuses(self):
        with FK.rename_and_rebind('scandir', 1, self.root, when='after'):
            result = self.call()
        self.refused(result, 'held at')

    def test_rebound_child_refuses_before_reading_its_leaf(self):
        child = self.root / 'child'
        child.mkdir()
        (child / 'protected').write_bytes(b'secret')
        real = os.open
        opened = []
        def watched(name, *a, **kw):
            opened.append(name)
            return real(name, *a, **kw)
        with mock.patch.object(os, 'open', watched):
            with FK.rename_and_rebind('scandir', 2, child, when='after'):
                self.refused(self.call(), 'held at')
        self.assertNotIn('protected', opened)

    def test_registry_swap_refuses(self):
        with FK.swap_for_symlink('open', 1, self.registry, self.leaf,
                                 match=lambda name, *a, **kw: name == 'registry.tsv'):
            result = self.call()
        self.refused(result, 'ELOOP')

    def test_short_write_completes_report(self):
        with FK.one_byte_writes():
            self.assertEqual(self.call(), (0, '', ''))
        self.assertEqual(self.doc()['findings'], [])

    def test_write_failure_keeps_partial_report(self):
        with FK.inject_oserror('write', 1, errno.ENOSPC):
            result = self.call()
        self.refused(result, 'ENOSPC')
        self.assertTrue(self.report.exists())
        self.assertEqual(self.report.read_bytes(), b'')

    def test_errors_refuse_and_unexpected_propagate(self):
        for target in ('open', 'scandir', 'read', 'fstat', 'close', FK.GETPATH):
            with self.subTest(target=target):
                with FK.inject_oserror(target, 1, errno.EIO):
                    self.refused(self.call(), 'EIO')
        for exc in FK.UNEXPECTED:
            with self.subTest(exc=exc):
                with FK.raise_unexpected('read', 1, exc):
                    with self.assertRaises(exc) as caught:
                        self.call()
                self.assertNotIsInstance(caught.exception, fdsafe.Refusal)


if __name__ == '__main__':
    unittest.main()
