"""CLI contracts for phase 5 move-source inputs."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from ops.migrate import reader_find

TOOL = Path(reader_find.__file__).resolve()
P = '/Volumes/memit/llm-database-poc-mirror'
SOURCE = P + '/autoresearch_fence_v13_c10'
TARGET = '/archive/c10'
HEADER = 'old\tnew\tdisposition\tunit\n'


class Plans(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.base = Path(tmp.name).resolve()
        self.root = self.base / 'M'
        self.root.mkdir()
        self.note = self.root / 'note.txt'
        self.note.write_text(SOURCE + '/results.json\n')
        self.plans = self.base / 'plans.json'
        self.plan([{'source': SOURCE, 'target': TARGET}])

    def plan(self, moves):
        self.plans.write_text(json.dumps({'entries': [{'moves': moves}]}))

    def cli(self, *args):
        env = dict(os.environ, LLMDB_ROOT=str(self.root), PYTHONPATH=str(TOOL.parents[2]))
        return subprocess.run([sys.executable, '-B', str(TOOL), *map(str, args)],
                              cwd=self.root, env=env, capture_output=True, text=True, timeout=60)

    def scan(self, *args):
        return self.cli('--check', '--paths', 'note.txt', '--plans', self.plans, *args)

    def report(self, result, rows):
        self.assertEqual(result.returncode, int(bool(rows)), result.stderr)
        self.assertEqual(json.loads(result.stdout), {'stale': rows, 'unverified': []})

    def row(self, old=SOURCE, text=None, line=1):
        return {'file': 'note.txt', 'line': line, 'old_text': old if text is None else text,
                'old': old}

    def refused(self, reason, *args):
        result = self.scan(*args)
        self.assertEqual((result.returncode, result.stdout, result.stderr),
                         (2, '', f'reader_find: refused: {self.plans}: {reason}\n'))

    def units(self, old):
        units = self.base / 'units'
        folder = units / 'S220'
        folder.mkdir(parents=True)
        (folder / 'path-map-rows.tsv').write_text(HEADER + f'{old}\tx\tmoved\tS220\n')
        return units

    def relocations(self, old):
        path = self.base / 'map.tsv'
        path.write_text(HEADER + f'{old}\tx\tmoved\tS1\n')
        return path

    def init_git(self):
        def git(*args):
            subprocess.run(['git', '-c', 'core.hooksPath=/dev/null', '-c',
                            'core.fsmonitor=false', '-C', str(self.root), *args],
                           check=True, capture_output=True, timeout=60)
        git('init', '-q')
        sentinel = self.base / 'EXECUTED'
        hook = self.base / 'monitor.sh'
        hook.write_text(f'#!/bin/sh\ntouch {sentinel}\n')
        hook.chmod(0o755)
        git('config', 'core.fsmonitor', str(hook))
        self.addCleanup(lambda: self.assertFalse(sentinel.exists(), 'fsmonitor ran'))

    def test_control_character_cli_refusals(self):
        for field, value in (('source', '/source/old\nforged diagnostic'),
                             ('target', '/target\x7f')):
            with self.subTest(field=field):
                move = {'source': SOURCE, 'target': TARGET}
                move[field] = value
                if field == 'source':
                    move['target'] = value
                self.plan([move])
                result = self.scan()
                self.assertEqual((result.returncode, result.stdout, result.stderr),
                                 (2, '', f'reader_find: refused: {self.plans}: '
                                  f'control character in move {value!r}\n'))
                self.assertEqual(len(result.stderr.splitlines()), 1)

    def test_control_character_range_in_both_fields(self):
        for field in ('source', 'target'):
            for number in (*range(32), 127):
                with self.subTest(field=field, number=number):
                    move = {'source': '/source', 'target': '/target'}
                    value = move[field] + chr(number)
                    move[field] = value
                    data = json.dumps({'entries': [{'moves': [move]}]}).encode()
                    with self.assertRaises(reader_find.Refused) as caught:
                        reader_find.parse_plans(self.plans, data)
                    self.assertEqual(str(caught.exception),
                                     f'{self.plans}: control character in move {value!r}')

    def test_symlinked_plans_file(self):
        self.report(self.scan(), [self.row()])
        regular = self.plans.with_name('regular.json')
        self.plans.rename(regular)
        self.plans.symlink_to(regular)
        result = self.scan()
        self.assertEqual((result.returncode, result.stdout), (2, ''))
        self.assertEqual(len(result.stderr.splitlines()), 1)
        self.assertTrue(result.stderr.startswith('reader_find: refused: '), result.stderr)
        self.assertIn(str(self.plans), result.stderr)

    def test_symlinked_plans_parent(self):
        regular = self.base / 'regular'
        regular.mkdir()
        (regular / 'nested').mkdir()
        link = self.base / 'linked'
        link.symlink_to(regular, target_is_directory=True)
        for relative in (Path('plans.json'), Path('nested/plans.json')):
            with self.subTest(relative=relative):
                self.plans = regular / relative
                self.plan([{'source': SOURCE, 'target': TARGET}])
                self.report(self.scan(), [self.row()])
                self.plans = link / relative
                result = self.scan()
                self.assertEqual((result.returncode, result.stdout), (2, ''))
                self.assertEqual(len(result.stderr.splitlines()), 1)
                self.assertTrue(result.stderr.startswith('reader_find: refused: '), result.stderr)
                self.assertIn(str(link), result.stderr)

    def test_fifo_plans_file(self):
        self.report(self.scan(), [self.row()])
        self.plans.rename(self.plans.with_name('regular.json'))
        os.mkfifo(self.plans)
        env = dict(os.environ, LLMDB_ROOT=str(self.root), PYTHONPATH=str(TOOL.parents[2]))
        result = subprocess.run([sys.executable, '-B', str(TOOL), '--check', '--paths',
                                 'note.txt', '--plans', str(self.plans)], cwd=self.root,
                                env=env, capture_output=True, text=True, timeout=5)
        self.assertEqual((result.returncode, result.stdout), (2, ''))
        self.assertEqual(len(result.stderr.splitlines()), 1)
        self.assertTrue(result.stderr.startswith('reader_find: refused: '), result.stderr)
        self.assertIn(str(self.plans), result.stderr)

    def test_parse_plans_exact_mapping(self):
        data = json.dumps({'entries': [
            {'moves': [{'source': '/first', 'target': '/target1'},
                       {'source': '/second', 'target': '/target2'}]},
            {'moves': [{'source': '/third', 'target': '/target3'}]}]}).encode()
        self.assertEqual(reader_find.parse_plans(self.plans, data),
                         {'/first': '/target1', '/second': '/target2', '/third': '/target3'})

    def test_docstring_plans_line(self):
        expected = '  --check --untracked --units DIR --plans FILE --report FILE  Step 266'
        self.assertEqual(reader_find.__doc__.splitlines()[8], expected)
        self.assertEqual(TOOL.read_text().splitlines()[9], expected)

    def test_refusal_message_controls(self):
        self.plans = self.base / 'plans\nforged diagnostic.json'
        self.plans.write_bytes(b'{invalid')
        result = self.scan()
        escaped = str(self.plans).replace('\n', r'\n')
        self.assertEqual((result.returncode, result.stdout, result.stderr),
                         (2, '', f'reader_find: refused: {escaped}: expected UTF-8 JSON\n'))
        self.assertEqual(len(result.stderr.splitlines()), 1)
        for number in (*range(32), 127):
            with self.subTest(number=number):
                self.assertEqual(reader_find.refusal_message('before' + chr(number) + 'after'),
                                 'before' + repr(chr(number))[1:-1] + 'after')
        unchanged = 'ordinary "quotes" and \'apostrophes\', \\path: café\x85\u2028\u2029'
        self.assertEqual(reader_find.refusal_message(unchanged), unchanged)

    def test_without_plans(self):
        old = str(self.base / 'old')
        relocations = self.relocations(old)
        for args in (('--old', old), ('--relocations', relocations)):
            with self.subTest(args=args):
                self.note.write_text(old + '/child\n')
                stale = self.cli('--check', '--paths', 'note.txt', *args)
                self.report(stale, [self.row(old)])
                self.assertEqual(stale.stderr, f'reader_find: note.txt:1 names {old}\n')
                self.note.write_text('clean\n')
                clean = self.cli('--check', '--paths', 'note.txt', *args)
                self.report(clean, [])
                self.assertEqual(clean.stderr, '')

    def test_untracked_positive_and_units_negative_control(self):
        self.init_git()
        self.report(self.cli('--check', '--untracked', '--plans', self.plans), [self.row()])
        units = self.units('experiments/c10r/runs/autoresearch_fence_v13_c10')
        self.report(self.cli('--check', '--untracked', '--units', units), [])

    def test_child_and_suffix_boundaries(self):
        self.note.write_text(f'{SOURCE}/child\n{SOURCE}_b\n{SOURCE}.bak\n')
        self.report(self.scan(), [self.row()])

    def test_unexpected_decoder_error_is_not_a_refusal(self):
        self.plans.write_text('[' * 100000)
        result = self.scan()
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn('RecursionError', result.stderr)
        self.assertNotIn('reader_find: refused', result.stderr)

    def test_source_inside_root_matches_only_as_written(self):
        source = str(self.root / 'docs')
        self.plan([{'source': source, 'target': TARGET}])
        self.note.write_text(f'{source}/a.txt\ndocs/a.txt\n"docs" "tools"\n')
        self.report(self.scan(), [self.row(source)])

    def test_inside_plans_is_skipped(self):
        self.init_git()
        self.plans = self.root / 'plans.json'
        self.plan([{'source': SOURCE, 'target': TARGET}])
        self.note.write_text('clean\n')
        self.report(self.cli('--check', '--untracked', '--plans', self.plans), [])

    def test_combined_inputs(self):
        self.note.write_text(f'{SOURCE}/child\nunit/child\nreloc/child\nexplicit/child\n')
        self.report(self.scan('--units', self.units('unit'), '--relocations',
                              self.relocations('reloc'), '--old', 'explicit'),
                    [self.row(), self.row('unit', line=2), self.row('reloc', line=3),
                     self.row('explicit', line=4)])

    def test_all_entries_and_moves_ignore_other_keys(self):
        self.plans.write_text(json.dumps({'ignored': None, 'entries': [
            {'id': 'S1', 'moves': [{'source': SOURCE, 'target': TARGET, 'action': 'OTHER'},
                                  {'source': '/second', 'target': '/target2'}]},
            {'moves': [{'source': '/third', 'target': '/target3'}]}]}))
        self.note.write_text(f'{SOURCE}\n/second\n/third\n')
        self.report(self.scan(), [self.row(), self.row('/second', line=2),
                                 self.row('/third', line=3)])

    def test_empty_lists_with_another_old(self):
        for data in ({'entries': []}, {'entries': [{'moves': []}]}):
            with self.subTest(data=data):
                self.plans.write_text(json.dumps(data))
                self.report(self.scan('--old', SOURCE), [self.row()])

    def test_invalid_encoding_and_json(self):
        malformed_string = json.dumps({'entries': [{'moves': [
            {'source': SOURCE, 'target': TARGET}]}]}).encode().replace(b'c10', b'c10\xff')
        for data in (b'\xff', b'{\ninvalid', b'', malformed_string):
            with self.subTest(data=data):
                self.plans.write_bytes(data)
                self.refused('expected UTF-8 JSON')

    def test_entries_shape(self):
        for data in (None, [], 1, 'x', {}, {'entries': None}, {'entries': {}},
                     {'entries': 'x'}, {'entries': 1}):
            with self.subTest(data=data):
                self.plans.write_text(json.dumps(data))
                self.refused('expected list entries')

    def test_moves_shape(self):
        for entry in (None, [], 'x', 1, {}, {'moves': None}, {'moves': {}},
                      {'moves': 'x'}, {'moves': 1}):
            with self.subTest(entry=entry):
                self.plans.write_text(json.dumps({'entries': [entry]}))
                self.refused('expected entry with list moves')

    def test_move_shape_and_absolute_strings(self):
        bad = [None, [], 'x', 1, {}]
        for field in ('source', 'target'):
            for value in (None, [], {}, 1, True, '', 'relative'):
                move = {'source': SOURCE, 'target': TARGET}
                move[field] = value
                bad.append(move)
            move = {'source': SOURCE, 'target': TARGET}
            del move[field]
            bad.append(move)
        for move in bad:
            with self.subTest(move=move):
                self.plan([move])
                self.refused('expected move with absolute source and target strings')

    def test_identity(self):
        self.plan([{'source': SOURCE, 'target': SOURCE}])
        self.refused('identity move ' + SOURCE)

    def test_duplicate_source_across_entries(self):
        for target in (TARGET, '/different'):
            with self.subTest(target=target):
                self.plans.write_text(json.dumps({'entries': [
                    {'moves': [{'source': SOURCE, 'target': TARGET}]},
                    {'moves': [{'source': SOURCE, 'target': target}]}]}))
                self.refused('repeated source ' + SOURCE)

    def test_collisions_with_existing_maps(self):
        units, reloc = self.units(SOURCE), self.relocations(SOURCE)
        for args in (('--units', units), ('--relocations', reloc), ('--old', SOURCE)):
            with self.subTest(args=args):
                self.refused('source already an old path ' + SOURCE, *args)


if __name__ == '__main__':
    unittest.main()
