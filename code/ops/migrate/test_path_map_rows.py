"""path_map_rows: exact unit relocation rows, composed and checked over the combined graph."""
import contextlib
import hashlib
import io
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

CODE = Path(__file__).resolve().parents[2]
TOOL = CODE / 'ops' / 'migrate' / 'path_map_rows.py'
V = '/Volumes/memit/llmdb-preserved/icm21-20261013'
T = '/Volumes/memit/llmdb-tools'
HEADER = 'old\tnew\tdisposition\tunit\n'


class PathMapRows(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.tmp = Path(temp.name).resolve()
        self.parent = self.tmp / 'P'
        self.root = self.parent / 'M'
        index = self.root / '_index'
        index.mkdir(parents=True)
        (index / 'path-map.tsv').write_text(
            HEADER
            + f'{self.parent}/hist.json\texperiments/x/runs/hist.json\tmove\tP:hist.json\n'
            + 'docs/stay.md\tdocs/stay.md\tstay\tM:docs\n'
            + 'old/quarantined\t\tquarantine\tM:old\n', encoding='utf-8')
        (index / 'anchor-map.tsv').write_text('monolith\tanchor\tpart\tcurrent_anchor\n',
                                             encoding='utf-8')
        (index / 'icm21-path-map.tsv').write_text(HEADER, encoding='utf-8')
        self.units = self.root / 'program/migrations/icm21/units'
        self.units.mkdir(parents=True)
        self.count = 0

    def run_tool(self, *args):
        env = dict(os.environ, LLMDB_ROOT=str(self.root), PYTHONPATH=str(CODE))
        return subprocess.run([sys.executable, '-B', str(TOOL), *args], cwd=self.root,
                              env=env, capture_output=True, text=True, timeout=60)

    def pairs(self, body, header='old\tnew\n'):
        self.count += 1
        path = self.tmp / f'pairs-{self.count}.tsv'
        path.write_bytes((header + body).encode('utf-8'))
        return path

    def write(self, unit, body, header='old\tnew\n'):
        return self.run_tool('write', '--unit', unit, '--pairs', str(self.pairs(body, header)),
                             '--units', str(self.units))

    def tree(self):
        result = {}
        for path in sorted(self.tmp.rglob('*')):
            name = str(path.relative_to(self.tmp))
            if path.is_symlink():
                result[name] = 'link:' + os.readlink(path)
            elif path.is_dir():
                result[name] = 'dir'
            elif not name.startswith('pairs-'):
                result[name] = hashlib.sha256(path.read_bytes()).hexdigest()
        return result

    def row_file(self, unit):
        return self.units / unit / 'path-map-rows.tsv'

    def assert_refused(self, result, *needles):
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn('path_map_rows: refused: ', result.stderr)
        self.assertEqual(result.stdout, '')
        for needle in needles:
            self.assertIn(needle, result.stderr)

    def assert_write_refused(self, unit, body, *needles, header='old\tnew\n'):
        before = self.tree()
        result = self.write(unit, body, header)
        self.assert_refused(result, *needles)
        self.assertEqual(self.tree(), before)

    def test_write_emits_exact_sorted_rows_and_nothing_else(self):
        before = self.tree()
        result = self.write('S220', 'scratch/a.log\t' + V + '/parent/a.log\n'
                            'experiments/x/runs/hist.json\texperiments/c10r/runs/hist.json\n'
                            f'{self.parent}/loose.txt\texperiments/y/loose.txt\n'
                            'docs/stay.md\tdocs/moved.md\n'
                            'tools/t.py\t' + T + '/icm21/t.py\n')
        self.assertEqual(result.returncode, 0, result.stderr)
        expected = (HEADER
                    + f'{self.parent}/loose.txt\texperiments/y/loose.txt\tmove\tS220\n'
                    + 'docs/stay.md\tdocs/moved.md\tmove\tS220\n'
                    + 'experiments/x/runs/hist.json\texperiments/c10r/runs/hist.json\tmove\tS220\n'
                    + 'scratch/a.log\t' + V + '/parent/a.log\tpreserved\tS220\n'
                    + 'tools/t.py\t' + T + '/icm21/t.py\tpreserved\tS220\n')
        self.assertEqual(self.row_file('S220').read_bytes(), expected.encode('utf-8'))
        after = self.tree()
        added = {name for name in after if name not in before}
        self.assertEqual(added, {'P/M/program/migrations/icm21/units/S220',
                                 'P/M/program/migrations/icm21/units/S220/path-map-rows.tsv'})
        self.assertEqual({name: after[name] for name in before}, before)

    def test_write_never_overwrites_a_row_file(self):
        (self.units / 'S220').mkdir()
        self.row_file('S220').write_bytes(b'keep me\n')
        self.assert_write_refused('S220', 'a/x\tb/x\n', 'never overwritten')
        self.assertEqual(self.row_file('S220').read_bytes(), b'keep me\n')

    def test_row_file_that_appears_after_the_check_is_not_overwritten(self):
        # Simulates a writer racing between the existence check and the open.
        sys.path.insert(0, str(CODE))
        self.addCleanup(sys.path.remove, str(CODE))
        from ops.migrate import path_map_rows
        (self.units / 'S220').mkdir()
        self.row_file('S220').write_bytes(b'keep me\n')
        stderr = io.StringIO()
        with mock.patch.dict(os.environ, LLMDB_ROOT=str(self.root)), \
                mock.patch.object(path_map_rows.os.path, 'lexists', return_value=False), \
                contextlib.redirect_stderr(stderr):
            code = path_map_rows.main(['write', '--unit', 'S220', '--pairs',
                                       str(self.pairs('a/x\tb/x\n')), '--units', str(self.units)])
        self.assertEqual(code, 2)
        self.assertIn('File exists', stderr.getvalue())
        self.assertEqual(self.row_file('S220').read_bytes(), b'keep me\n')

    def test_write_never_follows_a_symlinked_unit_dir(self):
        outside = self.tmp / 'outside'
        outside.mkdir()
        (self.units / 'S220').symlink_to(outside)
        self.assert_write_refused('S220', 'a/x\tb/x\n', 'symlink')
        self.assertEqual(list(outside.iterdir()), [])

    def test_units_dir_outside_root_is_refused(self):
        outside = self.tmp / 'units'
        outside.mkdir()
        before = self.tree()
        result = self.run_tool('write', '--unit', 'S220', '--pairs',
                               str(self.pairs('a/x\tb/x\n')), '--units', str(outside))
        self.assert_refused(result, 'outside')
        self.assertEqual(self.tree(), before)
        self.assert_refused(self.run_tool('compose', '--units', str(outside)), 'outside')

    def test_symlinked_units_dir_is_refused(self):
        link = self.root / 'units-link'
        link.symlink_to(self.units)
        before = self.tree()
        result = self.run_tool('write', '--unit', 'S220', '--pairs',
                               str(self.pairs('a/x\tb/x\n')), '--units', str(link))
        self.assert_refused(result, 'symlink')
        self.assertEqual(self.tree(), before)

    def test_bad_unit_ids_are_refused(self):
        for unit in ('../S220', 'S22', 'X220', 'S220/x', ''):
            with self.subTest(unit=unit):
                self.assert_write_refused(unit, 'a/x\tb/x\n', 'unit')

    def test_duplicate_old_within_a_unit_is_refused(self):
        self.assert_write_refused('S220', 'a/x\tb/x\na/x\tb/y\n', 'duplicate old', 'a/x')

    def test_duplicate_old_across_units_is_refused(self):
        self.assertEqual(self.write('S220', 'a/x\tb/x\n').returncode, 0)
        self.assert_write_refused('S221', 'a/x\tc/x\n', 'duplicate old', 'S220')

    def test_two_olds_one_target_is_refused(self):
        self.assert_write_refused('S220', 'a/x\tb/x\na/y\tb/x\n', 'duplicate target', 'b/x')
        self.assertEqual(self.write('S220', 'a/x\tb/x\n').returncode, 0)
        self.assert_write_refused('S221', 'a/y\tb/x\n', 'duplicate target', 'S220')

    def test_target_already_named_by_the_sealed_map_is_refused(self):
        for new in ('docs/stay.md', 'experiments/x/runs/hist.json', 'old/quarantined'):
            with self.subTest(new=new):
                self.assert_write_refused('S220', f'a/x\t{new}\n', 'sealed', new)

    def test_historical_sealed_key_is_refused_and_named(self):
        self.assert_write_refused('S220', f'{self.parent}/hist.json\tb/x\n', 'sealed',
                                  'experiments/x/runs/hist.json')
        self.assert_write_refused('S220', 'old/quarantined\tb/x\n', 'sealed')

    def test_identity_row_is_refused(self):
        self.assert_write_refused('S220', 'a/x\ta/x\n', 'cycle')

    def test_cycle_across_units_is_refused(self):
        self.assertEqual(self.write('S220', 'a/x\tb/x\n').returncode, 0)
        self.assert_write_refused('S221', 'b/x\ta/x\n', 'cycle')
        self.assertEqual(self.write('S221', 'b/x\tc/x\n').returncode, 0)
        self.assert_write_refused('S222', 'c/x\ta/x\n', 'cycle')

    def test_chain_across_units_is_accepted(self):
        self.assertEqual(self.write('S220', 'a/x\tb/x\n').returncode, 0)
        result = self.write('S221', 'b/x\tc/x\n')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.row_file('S221').read_text(encoding='utf-8'),
                         HEADER + 'b/x\tc/x\tmove\tS221\n')

    def test_bad_paths_are_refused(self):
        cases = {
            'absolute target outside V and T': 'a/x\t/Volumes/memit/elsewhere/x\n',
            'target is the V root itself': 'a/x\t' + V + '\n',
            'target prefix that is not under V': 'a/x\t' + V + '-other/x\n',
            'dotdot target': 'a/x\tb/../../x\n',
            'dot segment': 'a/./x\tb/x\n',
            'trailing slash': 'a/x/\tb/x\n',
            'double slash': 'a//x\tb/x\n',
            'empty target': 'a/x\t\n',
            'empty old': '\tb/x\n',
            'quote': 'a/"x\tb/x\n',
            'control character': 'a/\x01x\tb/x\n',
            'absolute old inside M': f'{self.root}/a/x\tb/x\n',
            'absolute old equal to M': f'{self.root}\tb/x\n',
        }
        for name, body in cases.items():
            with self.subTest(case=name):
                self.assert_write_refused('S220', body)

    def test_malformed_pairs_are_refused(self):
        cases = {
            'wrong header': ('a/x\tb/x\n', 'new\told\n'),
            'three fields': ('a/x\tb/x\tc\n', 'old\tnew\n', 'fields'),
            'one field': ('a/x\n', 'old\tnew\n', 'fields'),
            'no final newline': ('a/x\tb/x', 'old\tnew\n', 'final newline'),
            'carriage return': ('a/x\tb/x\r\n', 'old\tnew\n', 'LF line ends'),
            'blank line': ('a/x\tb/x\n\n', 'old\tnew\n', 'fields'),
            'header only': ('', 'old\tnew\n', 'no rows'),
        }
        for name, (body, header, *needles) in cases.items():
            with self.subTest(case=name):
                self.assert_write_refused('S220', body, *needles, header=header)

    def test_sealed_maps_are_never_written(self):
        sealed = {name: (self.root / '_index' / name).read_bytes()
                  for name in ('path-map.tsv', 'anchor-map.tsv', 'icm21-path-map.tsv')}
        self.assertEqual(self.write('S220', 'a/x\tb/x\n').returncode, 0)
        self.assertEqual(self.run_tool('compose', '--units', str(self.units)).returncode, 0)
        self.assertEqual(self.run_tool('compose', '--check', '--units',
                                       str(self.units)).returncode, 1)
        for name, data in sealed.items():
            self.assertEqual((self.root / '_index' / name).read_bytes(), data, name)

    def test_compose_prints_every_unit_and_check_compares_the_map(self):
        self.assertEqual(self.write('S221', 'z/y\tz/w\nb/x\tc/x\n').returncode, 0)
        self.assertEqual(self.write('S220', 'a/x\tb/x\n').returncode, 0)
        (self.units / 'S222').mkdir()  # a unit with no rows yet is skipped
        composed = self.run_tool('compose', '--units', str(self.units))
        self.assertEqual(composed.returncode, 0, composed.stderr)
        expected = (HEADER + 'a/x\tb/x\tmove\tS220\n' + 'b/x\tc/x\tmove\tS221\n'
                    + 'z/y\tz/w\tmove\tS221\n')
        self.assertEqual(composed.stdout, expected)
        check = self.run_tool('compose', '--check', '--units', str(self.units))
        self.assertEqual(check.returncode, 1, check.stderr)
        self.assertIn('differs', check.stderr)
        (self.root / '_index/icm21-path-map.tsv').write_text(expected, encoding='utf-8')
        check = self.run_tool('compose', '--check', '--units', str(self.units))
        self.assertEqual(check.returncode, 0, check.stderr)
        self.assertEqual(check.stdout, '')

    def test_compose_without_unit_rows_is_refused(self):
        self.assert_refused(self.run_tool('compose', '--check', '--units', str(self.units)),
                            'no unit row files')
        self.assert_refused(self.run_tool('compose', '--units', str(self.units)),
                            'no unit row files')

    def hand_unit(self, units, unit, rows):
        (units / unit).mkdir(parents=True)
        (units / unit / 'path-map-rows.tsv').write_text(HEADER + rows, encoding='utf-8')

    def test_compose_refuses_tampered_unit_files(self):
        cases = {
            'unit column': [('S220', 'a/x\tb/x\tmove\tS999\n')],
            'disposition': [('S220', 'a/x\t' + V + '/x\tmove\tS220\n')],
            'disposition word': [('S220', 'a/x\tb/x\tstay\tS220\n')],
            'header only': [('S220', '')],
            'cross-unit duplicate old': [('S220', 'a/x\tb/x\tmove\tS220\n'),
                                         ('S221', 'a/x\tc/x\tmove\tS221\n')],
            'cross-unit cycle': [('S220', 'a/x\tb/x\tmove\tS220\n'),
                                 ('S221', 'b/x\ta/x\tmove\tS221\n')],
            'bad unit dir name': [('notes', 'a/x\tb/x\tmove\tnotes\n')],
        }
        for number, (name, units) in enumerate(cases.items()):
            with self.subTest(case=name):
                folder = self.root / 'cases' / str(number)
                for unit, rows in units:
                    self.hand_unit(folder, unit, rows)
                self.assert_refused(self.run_tool('compose', '--units', str(folder)))

    def test_compose_refuses_symlinked_row_files_and_unit_dirs(self):
        outside = self.tmp / 'outside'
        outside.mkdir()
        (outside / 'path-map-rows.tsv').write_text(HEADER + 'a/x\tb/x\tmove\tS220\n',
                                                   encoding='utf-8')
        (self.units / 'S220').symlink_to(outside)
        self.assert_refused(self.run_tool('compose', '--units', str(self.units)), 'symlink')
        (self.units / 'S220').unlink()
        (self.units / 'S220').mkdir()
        self.row_file('S220').symlink_to(outside / 'path-map-rows.tsv')
        self.assert_refused(self.run_tool('compose', '--units', str(self.units)), 'symlink')


if __name__ == '__main__':
    unittest.main()
