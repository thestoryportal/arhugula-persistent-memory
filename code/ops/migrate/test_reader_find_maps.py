"""T378: map and report admission, faults and master-byte compatibility."""
import contextlib
import errno
import fcntl
import io
import os
from pathlib import Path
import tempfile
import unittest
from unittest import mock

import fault_kit as FK
from ops.migrate import fdsafe
import reader_find


# Recorded from master 8bbac3f3 for every pre-attack control state.
MASTER_RESULTS = {
    ('clean\n', True, ('one',), 'relocations'):
        (0, '{\n "stale": [],\n "unverified": []\n}\n', ''),
    ('clean\n', True, ('one',), 'unit_map'):
        (0, '{\n "stale": [],\n "unverified": []\n}\n', ''),
    ('clean\n', True, ('one',), 'report'):
        (0, '{\n "stale": [],\n "unverified": []\n}\n', ''),
    ('clean\n', False, ('one',), 'report'):
        (1, '{\n "stale": [],\n "unverified": []\n}\n', 'reader_find: {ROOT}/reports/report.json differs from this scan\n'),
    ('old/place\n', True, ('one',), 'relocations'):
        (1, '{\n "stale": [\n  {\n   "file": "reader",\n   "line": 1,\n   "old": "old/place",\n   "old_text": "old/place"\n  }\n ],\n "unverified": []\n}\n', 'reader_find: reader:1 names old/place\n'),
    ('old/place\n', True, ('one',), 'unit_map'):
        (1, '{\n "stale": [\n  {\n   "file": "reader",\n   "line": 1,\n   "old": "old/place",\n   "old_text": "old/place"\n  }\n ],\n "unverified": []\n}\n', 'reader_find: reader:1 names old/place\n'),
    ('old/place\n', True, ('one',), 'report'):
        (1, '{\n "stale": [\n  {\n   "file": "reader",\n   "line": 1,\n   "old": "old/place",\n   "old_text": "old/place"\n  }\n ],\n "unverified": []\n}\n', 'reader_find: {ROOT}/reports/report.json differs from this scan\nreader_find: reader:1 names old/place\n'),
    ('clean\n', True, ('one',), 'unit'):
        (0, '{\n "stale": [],\n "unverified": []\n}\n', ''),
    ('clean\n', True, ('empty', 'notes', 'one'), 'unit_map'):
        (0, '{\n "stale": [],\n "unverified": []\n}\n', ''),
}


class Maps(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory(prefix='reader-maps-')
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name).resolve()
        self.maps = self.root / 'maps'
        self.maps.mkdir()
        self.relocations = self.maps / 'relocations.tsv'
        self.units = self.root / 'units'
        self.unit = self.units / 'one'
        self.unit.mkdir(parents=True)
        self.unit_map = self.unit / reader_find.UNIT_ROWS
        (self.root / 'reports').mkdir()
        self.report = self.root / 'reports/report.json'
        self.data = b'old\tnew\tdisposition\tunit\nold/place\tnew/place\tmove\tone\n'
        for path in (self.relocations, self.unit_map):
            path.write_bytes(self.data)
        (self.root / 'reader').write_bytes(b'clean\n')
        self.report.write_bytes(b'{\n "stale": [],\n "unverified": []\n}\n')

    def args(self, route):
        scope = ['--check', '--paths', 'reader']
        if route == 'relocations':
            return scope + ['--relocations', str(self.relocations)]
        if route in ('unit', 'unit_map'):
            return scope + ['--units', str(self.units)]
        return scope + ['--old', 'old/place', '--report', str(self.report)]

    def cli(self, route):
        out, err = io.StringIO(), io.StringIO()
        with mock.patch.dict(os.environ, LLMDB_ROOT=str(self.root)), \
                contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            rc = reader_find.main(self.args(route))
        return rc, out.getvalue(), err.getvalue()

    def baseline(self, route):
        state = ((self.root / 'reader').read_text(), self.report.exists(),
                 tuple(sorted(p.name for p in self.units.iterdir())), route)
        rc, out, err = MASTER_RESULTS[state]
        return rc, out.replace('{ROOT}', str(self.root)), err.replace('{ROOT}', str(self.root))

    def control(self, route):
        expected = self.baseline(route)
        self.assertIn(expected[0], (0, 1), expected)
        self.assertEqual(self.cli(route), expected)
        return expected

    def refused(self, result, path, err=None):
        rc, out, diagnostic = result
        self.assertEqual(rc, 2, result)
        self.assertEqual(len(diagnostic.splitlines()), 1, diagnostic)
        self.assertIn('reader_find: refused:', diagnostic)
        self.assertIn(str(path), diagnostic)
        self.assertNotIn('Traceback', diagnostic)
        if err:
            self.assertIn('[' + err + ']', diagnostic)

    def test_regular_and_absent_report_equal_master(self):
        for route in ('relocations', 'unit_map', 'report'):
            self.control(route)
        self.report.unlink()
        result = self.control('report')
        self.assertEqual(result[0], 1)
        self.assertIn('differs', result[2])

    def test_stale_and_different_report_equal_master(self):
        (self.root / 'reader').write_bytes(b'old/place\n')
        for route in ('relocations', 'unit_map', 'report'):
            self.control(route)

    def test_units_ignore_regular_files_and_missing_maps(self):
        (self.units / 'notes').write_bytes(b'ignored')
        (self.units / 'empty').mkdir()
        self.control('unit_map')

    def attack(self, route, kind):
        self.control(route)
        path = getattr(self, route)
        if kind == 'fifo':
            try:
                with FK.fifo_in_place(path, timeout=0.5):
                    result = self.cli(route)
            except FK.AttackTimeout as exc:
                self.fail(str(exc))
        else:
            target = self.root / 'outside'
            if route == 'unit':
                target.mkdir()
                (target / reader_find.UNIT_ROWS).write_bytes(self.data)
            else:
                target.write_bytes(path.read_bytes())
            # Install a real link with the fault kit, then exercise the public CLI.
            with FK.swap_for_symlink('open', 1, path, target):
                fd = os.open(self.root, os.O_RDONLY | os.O_DIRECTORY)
                os.close(fd)
                result = self.cli(route)
        self.refused(result, path)

    def fd_match(self, path):
        real_fcntl = fcntl.fcntl
        def match(fd, *args, **kwargs):
            live = real_fcntl(fd, fcntl.F_GETPATH, bytes(1024))
            return os.fsdecode(live.split(b'\0', 1)[0]) == str(path)
        return match

    def fault(self, route, call, parent=False):
        self.control(route)
        path = getattr(self, route)
        if parent:
            path = path.parent
        if call == 'open':
            match = lambda name, *a, **kw: os.fspath(name) in (str(path), path.name)
        else:
            match = self.fd_match(path)
        with FK.inject_oserror(call, 1, errno.EIO, match=match):
            result = self.cli(route)
        self.refused(result, path, 'EIO')

    def test_units_outer_listing_eio(self):
        self.control('unit_map')
        with FK.inject_oserror('scandir', 1, errno.EIO,
                               match=self.fd_match(self.units)):
            result = self.cli('unit_map')
        self.refused(result, self.units, 'EIO')

    def test_unit_stat_eio(self):
        self.control('unit_map')
        real_stat = os.stat
        def fail(name, *args, **kwargs):
            if name == self.unit.name and kwargs.get('dir_fd') is not None:
                raise OSError(errno.EIO, os.strerror(errno.EIO))
            return real_stat(name, *args, **kwargs)
        with mock.patch.object(os, 'stat', side_effect=fail):
            result = self.cli('unit_map')
        self.refused(result, self.unit, 'EIO')

    def race(self, route, kind):
        self.control(route)
        path = getattr(self, route)
        match = lambda name, *a, **kw: os.fspath(name) in (str(path), path.name)
        target = self.root / 'impostor'
        if route == 'unit':
            target.mkdir()
            (target / reader_find.UNIT_ROWS).write_bytes(self.data)
        else:
            target.write_bytes(path.read_bytes())
        attack = (FK.swap_for_symlink('open', 1, path, target, match=match)
                  if kind == 'symlink' else
                  FK.fifo_in_place(path, name='open', match=match, timeout=0.5))
        try:
            with attack:
                result = self.cli(route)
        except FK.AttackTimeout as exc:
            self.fail(str(exc))
        self.refused(result, path)

    def test_map_parent_renamed_after_hold(self):
        self.control('relocations')
        with FK.rename_and_rebind(FK.GETPATH, 1, self.maps,
                                  match=self.fd_match(self.maps)):
            result = self.cli('relocations')
        self.refused(result, self.maps)

    def unexpected(self, route, exc):
        self.control(route)
        with FK.raise_unexpected('read', 1, exc,
                                 match=self.fd_match(getattr(self, route))):
            with self.assertRaises(exc):
                self.cli(route)


def attack_test(route, kind):
    def test(self):
        self.attack(route, kind)
    return test


def fault_test(route, call, parent):
    def test(self):
        self.fault(route, call, parent)
    return test


for _route in ('relocations', 'unit_map', 'unit', 'report'):
    for _kind in ('symlink', 'fifo'):
        setattr(Maps, f'test_{_route}_{_kind}', attack_test(_route, _kind))
        def test(self, route=_route, kind=_kind):
            self.race(route, kind)
        setattr(Maps, f'test_{_route}_{_kind}_at_open', test)
for _route in ('relocations', 'unit_map', 'report'):
    for _call in ('open', 'read', 'fstat', 'close'):
        setattr(Maps, f'test_{_route}_{_call}_eio', fault_test(_route, _call, False))
    for _call in ('open', 'close', FK.GETPATH):
        setattr(Maps, f'test_{_route}_parent_{_call}_eio', fault_test(_route, _call, True))
setattr(Maps, 'test_units_inner_listing_eio', fault_test('unit_map', 'scandir', True))
for _route in ('relocations', 'report'):
    for _exc in FK.UNEXPECTED:
        def test(self, route=_route, exc=_exc):
            self.unexpected(route, exc)
        setattr(Maps, f'test_{_route}_unexpected_{_exc.__name__}', test)


if __name__ == '__main__':
    unittest.main()
