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
    'named_map_unit':
        (0, '{\n "stale": [],\n "unverified": []\n}\n', ''),
    'no_unit_maps':
        (2, '', 'reader_find: refused: {ROOT}/units: no */path-map-rows.tsv\n'),
    'empty_map':
        (2, '', 'reader_find: refused: {ROOT}/maps/relocations.tsv: expected header old<TAB>new<TAB>disposition<TAB>unit\n'),
    'empty_old':
        (2, '', 'reader_find: refused: {ROOT}/maps/relocations.tsv:2: malformed row\n'),
    'empty_new':
        (2, '', 'reader_find: refused: {ROOT}/maps/relocations.tsv:2: malformed row\n'),
    'unreadable_irrelevant_directory':
        (0, '{\n "stale": [],\n "unverified": []\n}\n', ''),
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

    def assert_master_state(self, state, route):
        rc, out, err = MASTER_RESULTS[state]
        self.assertEqual(self.cli(route),
                         (rc, out.replace('{ROOT}', str(self.root)),
                          err.replace('{ROOT}', str(self.root))))

    def relative_cli(self, *args):
        previous = Path.cwd()
        self.addCleanup(os.chdir, previous)
        os.chdir(self.root)
        out, err = io.StringIO(), io.StringIO()
        with mock.patch.dict(os.environ, LLMDB_ROOT=str(self.root)), \
                contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            rc = reader_find.main(['--paths', 'reader', *args])
        return rc, out.getvalue(), err.getvalue()

    # Pins recorded now from 8bbac3f3's reader_find.py exported to TMPDIR;
    # tests use these literals and never invoke git or the master script.
    def test_relative_units_malformed_row_equal_master(self):
        self.unit_map.write_bytes(
            b'old\tnew\tdisposition\tunit\nold/place\tx\tmove\n')
        self.assertEqual(self.relative_cli('--check', '--units', 'units'),
                         (2, '', 'reader_find: refused: units/one/path-map-rows.tsv:2: malformed row\n'))

    def test_relative_units_duplicate_equal_master(self):
        second = self.units / 'two'
        second.mkdir()
        (second / reader_find.UNIT_ROWS).write_bytes(self.data)
        self.assertEqual(self.relative_cli('--check', '--units', 'units'),
                         (2, '', 'reader_find: refused: units/two/path-map-rows.tsv: old path old/place is in two units\n'))

    def test_relative_relocations_malformed_row_equal_master(self):
        self.relocations.write_bytes(
            b'old\tnew\tdisposition\tunit\nold/place\tx\tmove\n')
        self.assertEqual(self.relative_cli('--check', '--relocations', 'maps/relocations.tsv'),
                         (2, '', 'reader_find: refused: maps/relocations.tsv:2: malformed row\n'))

    def test_relative_report_exists_equal_master(self):
        self.assertEqual(self.relative_cli('--old', 'old/place', '--report', 'reports/report.json'),
                         (2, '', f'reader_find: refused: {self.root}/reports/report.json: exists; never overwritten\n'))

    def test_five_column_row_equal_master(self):
        self.unit_map.write_bytes(self.data.rstrip(b'\n') + b'\textra\n')
        self.assertEqual(self.relative_cli('--check', '--units', 'units'),
                         (2, '', 'reader_find: refused: units/one/path-map-rows.tsv:2: malformed row\n'))

    def test_wrong_header_valid_row_equal_master(self):
        self.unit_map.write_bytes(self.data.replace(b'old\tnew', b'wrong\tnew', 1))
        self.assertEqual(self.relative_cli('--check', '--units', 'units'),
                         (2, '', 'reader_find: refused: units/one/path-map-rows.tsv: expected header old<TAB>new<TAB>disposition<TAB>unit\n'))

    def test_unit_symlink_errno(self):
        self.unit.rename(self.root / 'parked-unit')
        self.unit.symlink_to(self.root / 'parked-unit', target_is_directory=True)
        result = self.cli('unit_map')
        self.refused(result, self.unit, 'ELOOP')
        self.assertTrue(result[2].endswith('[ELOOP]\n'), result)

    def test_unit_fifo_errno(self):
        with FK.fifo_in_place(self.unit, timeout=0.5):
            result = self.cli('unit_map')
        self.refused(result, self.unit, 'ENOTDIR')
        self.assertTrue(result[2].endswith('[ENOTDIR]\n'), result)

    def test_unit_named_map_equal_master(self):
        self.unit.rename(self.units / 'path-map-rows.tsv')
        self.assert_master_state('named_map_unit', 'unit_map')

    def test_no_unit_maps_equal_master(self):
        self.unit_map.unlink()
        self.assert_master_state('no_unit_maps', 'unit_map')

    def test_empty_map_equal_master(self):
        self.relocations.write_bytes(b'')
        self.assert_master_state('empty_map', 'relocations')

    def test_empty_old_equal_master(self):
        self.relocations.write_bytes(
            b'old\tnew\tdisposition\tunit\n\tnew/place\tmove\tone\n')
        self.assert_master_state('empty_old', 'relocations')

    def test_empty_new_equal_master(self):
        self.relocations.write_bytes(
            b'old\tnew\tdisposition\tunit\nold/place\t\tmove\tone\n')
        self.assert_master_state('empty_new', 'relocations')

    def test_mapping_values_and_input_files(self):
        self.assertEqual(reader_find.read_rows(self.relocations),
                         {'old/place': 'new/place'})
        self.assertEqual(reader_find.unit_rows(self.units),
                         ({'old/place': 'new/place'}, [self.unit_map]))

    def test_stale_and_different_report_equal_master(self):
        (self.root / 'reader').write_bytes(b'old/place\n')
        for route in ('relocations', 'unit_map', 'report'):
            self.control(route)

    def test_units_ignore_regular_files_and_missing_maps(self):
        (self.units / 'notes').write_bytes(b'ignored')
        (self.units / 'empty').mkdir()
        self.control('unit_map')

    def test_units_ignore_unreadable_irrelevant_directory(self):
        irrelevant = self.unit / 'irrelevant'
        irrelevant.mkdir()
        self.addCleanup(irrelevant.chmod, 0o755)
        irrelevant.chmod(0)
        self.assertEqual(self.cli('unit_map'),
                         MASTER_RESULTS['unreadable_irrelevant_directory'])

    # R378d: head pins for locked units, an explicit master-compatibility exception.
    def test_units_refuse_locked_unit_000_before(self):
        locked = self.units / 'aa-locked'
        locked.mkdir()
        self.addCleanup(locked.chmod, 0o755)
        locked.chmod(0)
        self.assertEqual(self.cli('unit_map'),
                         (2, '', f"reader_find: refused: '{locked}': Permission denied [EACCES]\n"))

    def test_units_refuse_locked_unit_000_after(self):
        locked = self.units / 'zz-locked'
        locked.mkdir()
        self.addCleanup(locked.chmod, 0o755)
        locked.chmod(0)
        self.assertEqual(self.cli('unit_map'),
                         (2, '', f"reader_find: refused: '{locked}': Permission denied [EACCES]\n"))

    def test_units_refuse_locked_unit_0100(self):
        locked = self.units / 'locked'
        locked.mkdir()
        (locked / reader_find.UNIT_ROWS).write_bytes(
            b'old\tnew\tdisposition\tunit\nold/locked\tnew/locked\tmove\tlocked\n')
        self.addCleanup(locked.chmod, 0o755)
        locked.chmod(0o100)
        self.assertEqual(self.cli('unit_map'),
                         (2, '', f"reader_find: refused: '{locked}': Permission denied [EACCES]\n"))

    def test_units_refuse_locked_unit_0400(self):
        locked = self.units / 'locked'
        locked.mkdir()
        locked_map = locked / reader_find.UNIT_ROWS
        locked_map.write_bytes(
            b'old\tnew\tdisposition\tunit\nold/locked\tnew/locked\tmove\tlocked\n')
        self.addCleanup(locked.chmod, 0o755)
        locked.chmod(0o400)
        self.assertEqual(self.cli('unit_map'),
                         (2, '', f"reader_find: refused: '{locked_map}': Permission denied [EACCES]\n"))

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
        if route == 'unit_map' and parent and call == FK.GETPATH:
            path = self.units
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
        real_scandir = os.scandir
        @contextlib.contextmanager
        def entries(fd):
            with real_scandir(fd) as scanned:
                wrapped = []
                for entry in scanned:
                    proxy = mock.Mock(wraps=entry)
                    proxy.name = entry.name
                    if self.fd_match(self.units)(fd) and entry.name == self.unit.name:
                        proxy.stat.side_effect = OSError(errno.EIO, os.strerror(errno.EIO))
                    wrapped.append(proxy)
                yield iter(wrapped)
        with mock.patch.object(os, 'scandir', side_effect=entries):
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

    def rebind_after_listing(self, folder):
        (self.root / 'reader').write_bytes(b'old/place\n')
        control = self.control('unit_map')
        path = getattr(self, folder)
        with FK.rename_and_rebind('scandir', 1, path, when='after',
                                  match=self.fd_match(path)) as fault:
            attacked_scandir = os.scandir
            def plant(*args, **kwargs):
                entries = attacked_scandir(*args, **kwargs)
                if fault.fired and not self.unit_map.exists():
                    self.unit.mkdir(exist_ok=True)
                    self.unit_map.write_bytes(self.data.replace(b'old/place', b'other/place'))
                return entries
            with mock.patch.object(os, 'scandir', side_effect=plant):
                result = self.cli('unit_map')
        self.assertEqual(fault.fired, 1)
        if result[0] == 2:
            self.refused(result, path)
        else:
            self.assertEqual(result, control)

    def test_unit_rebound_after_listing(self):
        self.rebind_after_listing('unit')

    def test_units_rebound_after_listing(self):
        self.rebind_after_listing('units')

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
