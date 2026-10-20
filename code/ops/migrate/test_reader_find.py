"""reader_find: a lexical scan of tracked and untracked readers of old unit paths.

Every fixture lives in a temporary directory. Nothing is executed except git ls-files
inside the fixture, with an fsmonitor hook planted to prove it never runs.
"""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import reader_find

TOOL = Path(reader_find.__file__).resolve()
P = '/Volumes/memit/llm-database-poc-mirror'
OLD = P + '/stage_1_sect'
OLD_C10 = P + '/autoresearch_fence_v13_c10'
HEADER = 'old\tnew\tdisposition\tunit\n'


def git(root, *args):
    # The fixture's own git calls disable the planted monitor; only the tool is under test.
    subprocess.run(['git', '-c', 'core.hooksPath=/dev/null', '-c', 'core.fsmonitor=false',
                    '-C', str(root), *args],
                   check=True, capture_output=True)


class Fixture(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.base = Path(tmp.name).resolve()
        self.root = self.base / 'M'
        self.root.mkdir()
        git(self.root, 'init', '-q')
        # Planted executables: if anything runs them, the sentinel appears.
        self.sentinel = self.base / 'EXECUTED'
        hook = self.base / 'monitor.sh'
        hook.write_text(f'#!/bin/sh\ntouch {self.sentinel}\n')
        hook.chmod(0o755)
        git(self.root, 'config', 'core.fsmonitor', str(hook))
        self.addCleanup(lambda: self.assertFalse(self.sentinel.exists(), 'a hook or script ran'))

    def write(self, rel, data):
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(data, str):
            data = data.encode()
        path.write_bytes(data)
        return path

    def track(self, *rels):
        git(self.root, 'add', '--', *rels)

    def relocations(self, rows, name='map.tsv'):
        path = self.base / name
        path.write_text(HEADER + ''.join('\t'.join(r) + '\n' for r in rows))
        return path

    def cli(self, *args, env_root=True):
        env = {k: v for k, v in os.environ.items() if k != 'LLMDB_ROOT'}
        if env_root:
            env['LLMDB_ROOT'] = str(self.root)
        env['PYTHONPATH'] = str(TOOL.parents[2])
        return subprocess.run([sys.executable, '-B', str(TOOL), *map(str, args)],
                              cwd=self.root, env=env, capture_output=True, text=True, timeout=60)


class Spellings(Fixture):
    def scan(self, rel, text, olds=(OLD,)):
        self.write(rel, text)
        return reader_find.scan_files(self.root, [rel], list(olds))

    def stale(self, report):
        return [(r['file'], r['line'], r['old_text']) for r in report['stale']]

    def test_absolute_old_path_and_child_are_stale(self):
        report = self.scan('a.sh', f'x\ncp {OLD}/patch.py .\nls "{OLD}"\n')
        self.assertEqual(self.stale(report), [('a.sh', 2, OLD), ('a.sh', 3, OLD)])
        self.assertEqual(report['stale'][0]['old'], OLD)

    def test_sentence_period_is_stale_but_sibling_names_are_not(self):
        report = self.scan('n.md', f'see {OLD}.\n{OLD}_S215D2\n{OLD}.json\n{OLD}-v2\n')
        self.assertEqual(self.stale(report), [('n.md', 1, OLD)])

    def test_relative_key_matches_its_m_spellings_only(self):
        rel = 'memit_dry_run'
        text = (f'{P}/memit_dry_run/x\n'            # the P unit, a different path
                f'{self.root}/memit_dry_run/y\n'    # absolute spelling of the M key
                f'cd ./memit_dry_run\n'
                f'"memit_dry_run"\n'
                f'other/memit_dry_run\n')           # a different relative path
        report = self.scan('r.txt', text, [rel])
        self.assertEqual([r[1] for r in self.stale(report)], [2, 3, 4])
        self.assertEqual(self.stale(report)[0][2], f'{self.root}/memit_dry_run')

    def test_dynamic_spelling_is_unverified_not_stale(self):
        report = self.scan('d.py', f'base = f"{P}/autoresearch_{{name}}"\nroot = "{P}/"\n',
                           [OLD_C10])
        self.assertEqual(report['stale'], [])
        self.assertEqual([(u['file'], u['line'], u['reason']) for u in report['unverified']],
                         [('d.py', 1, 'dynamic'), ('d.py', 2, 'dynamic')])
        self.assertEqual(report['unverified'][0]['text'], P + '/autoresearch_')

    def test_full_key_that_prefixes_another_key_is_stale_not_dynamic(self):
        short, long = P + '/autoresearch_sandbox_c10', P + '/autoresearch_sandbox_c10_sealed'
        report = self.scan('s.sh', f'SOURCE={short}\n', [short, long])
        self.assertEqual(report['unverified'], [])
        self.assertEqual(self.stale(report), [('s.sh', 1, short)])

    def test_unrelated_sibling_under_parent_is_not_unverified(self):
        report = self.scan('s.md', f'{P}/arhugula-persistent-memory/x\n{P}/hf_cache\n', [OLD_C10])
        self.assertEqual(report, {'stale': [], 'unverified': []})

    def test_notebook_is_read_as_data(self):
        cell = {'cell_type': 'code', 'source': [f"open('{OLD}/r.json')\n",
                                                f"import os; os.system('touch {self.sentinel}')"],
                'metadata': {}, 'outputs': [], 'execution_count': None}
        nb = json.dumps({'cells': [cell], 'metadata': {}, 'nbformat': 4, 'nbformat_minor': 5},
                        indent=1)
        report = self.scan('nb.ipynb', nb)
        self.assertEqual(len(report['stale']), 1)
        self.assertEqual(report['stale'][0]['file'], 'nb.ipynb')

    def test_binary_is_scanned_and_unverified(self):
        report = self.scan('w.bin', b'\x00\x01' + OLD.encode() + b'\x00rest')
        self.assertEqual(self.stale(report), [('w.bin', 1, OLD)])
        self.assertEqual([u['reason'] for u in report['unverified']], ['binary'])

    def test_symlink_text_is_read_and_target_is_never_followed(self):
        outside = self.base / 'outside.txt'
        outside.write_text(f'{OLD}\n')
        (self.root / 'out').symlink_to(outside)
        (self.root / 'old').symlink_to(OLD + '/patch.py')
        report = reader_find.scan_files(self.root, ['out', 'old'], [OLD])
        self.assertEqual(self.stale(report), [('old', 1, OLD)])

    def test_longest_key_wins_one_occurrence(self):
        report = self.scan('k.md', f'{OLD}/sub/f\n', [OLD, OLD + '/sub'])
        self.assertEqual(self.stale(report), [('k.md', 1, OLD + '/sub')])


class Scopes(Fixture):
    def setUp(self):
        super().setUp()
        self.write('.gitignore', 'ignored.log\n')
        self.write('code/run.sh', f'#!/bin/sh\ntouch {self.sentinel}\npython {OLD}/a.py\n')
        (self.root / 'code/run.sh').chmod(0o755)
        self.track('.gitignore', 'code/run.sh')
        self.write('notes/u.md', f'untracked {OLD}\n')
        self.write('ignored.log', f'{OLD}\n')

    def test_tracked_and_untracked_scopes(self):
        self.assertEqual(reader_find.list_files(self.root, untracked=False), ['.gitignore', 'code/run.sh'])
        self.assertEqual(reader_find.list_files(self.root, untracked=True), ['notes/u.md'])

    def test_check_untracked_exits_1_and_lists_only_untracked(self):
        units = self.base / 'units'
        (units / 'S220').mkdir(parents=True)
        (units / 'S220/path-map-rows.tsv').write_text(HEADER + f'{OLD}\tx/stage_1_sect\tmoved\tS220\n')
        result = self.cli('--check', '--untracked', '--units', units)
        self.assertEqual(result.returncode, 1, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual([r['file'] for r in report['stale']], ['notes/u.md'])

    def test_tracked_absent_file_is_unverified_but_a_named_absent_file_is_refused(self):
        self.write('gone.md', f'{OLD}\n')
        self.track('gone.md')
        os.unlink(self.root / 'gone.md')
        reloc = self.relocations([(OLD, 'x', 'moved', 'S1')])
        result = self.cli('--check', '--tracked', '--relocations', reloc)
        self.assertEqual(result.returncode, 1, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual([r['file'] for r in report['stale']], ['code/run.sh'])
        self.assertEqual(report['unverified'], [{'file': 'gone.md', 'reason': 'absent'}])
        self.assertEqual(self.cli('--check', '--paths', 'gone.md', '--relocations', reloc).returncode, 2)

    def test_report_is_written_once_then_checked(self):
        units = self.root / 'units'
        (units / 'S220').mkdir(parents=True)
        # The map itself names the old path; it is an input, never a reader.
        (units / 'S220/path-map-rows.tsv').write_text(HEADER + f'{OLD}\tx/stage_1_sect\tmoved\tS220\n')
        self.write('notes/u.md', f'dyn = "{P}/stage_{{n}}"\n')
        report = self.root / 'out/untracked-readers.json'
        report.parent.mkdir()
        listed = self.cli('--untracked', '--units', units, '--report', report)
        self.assertEqual(listed.returncode, 0, listed.stderr)
        first = report.read_bytes()
        self.assertEqual(json.loads(first)['unverified'][0]['file'], 'notes/u.md')
        again = self.cli('--untracked', '--units', units, '--report', report)
        self.assertEqual(again.returncode, 2)
        self.assertEqual(report.read_bytes(), first)
        self.assertEqual(self.cli('--check', '--untracked', '--units', units, '--report', report).returncode, 0)
        self.write('notes/new.txt', f'{OLD}\n')
        self.assertEqual(self.cli('--check', '--untracked', '--units', units, '--report', report).returncode, 1)
        (self.root / 'notes/new.txt').write_text('repaired\n')
        report.write_bytes(first.replace(b'"dynamic"', b'"binary"'))
        self.assertEqual(self.cli('--check', '--untracked', '--units', units, '--report', report).returncode, 1)


class PathsCli(Fixture):
    def test_check_paths_fails_until_repaired(self):
        reloc = self.relocations([(OLD, 'experiments/c10r/stage_1_sect', 'moved', 'S224')])
        note = self.write('_system/memory/n.md', f'run from {OLD}/a.py\n')
        plist = self.base / 'LaunchAgents/x.plist'
        plist.parent.mkdir()
        plist.write_text('<plist><string>ok</string></plist>\n')
        failing = self.cli('--check', '--paths', '_system/memory/n.md', plist, '--relocations', reloc)
        self.assertEqual(failing.returncode, 1, failing.stderr)
        self.assertEqual(json.loads(failing.stdout)['stale'][0]['line'], 1)
        note.write_text('run from experiments/c10r/stage_1_sect/a.py\n')
        passing = self.cli('--check', '--paths', '_system/memory/n.md', plist, '--relocations', reloc)
        self.assertEqual(passing.returncode, 0, passing.stderr)
        self.assertEqual(json.loads(passing.stdout), {'stale': [], 'unverified': []})

    def test_absolute_plist_by_path_is_scanned(self):
        reloc = self.relocations([(OLD, 'x', 'moved', 'S1')])
        plist = self.base / 'LaunchAgents/y.plist'
        plist.parent.mkdir()
        plist.write_text(f'<plist><string>{OLD}/watch.sh</string></plist>\n')
        result = self.cli('--check', '--paths', plist, '--relocations', reloc)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(json.loads(result.stdout)['stale'][0]['file'], str(plist))

    def test_binary_plist_is_unverified(self):
        reloc = self.relocations([(OLD, 'x', 'moved', 'S1')])
        plist = self.base / 'z.plist'
        plist.write_bytes(b'bplist00\x00\x01')
        result = self.cli('--check', '--paths', plist, '--relocations', reloc)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)['unverified'][0]['reason'], 'binary')

    def refused(self, *args, env_root=True):
        result = self.cli(*args, env_root=env_root)
        self.assertEqual(result.returncode, 2, (result.stdout, result.stderr))
        self.assertIn('reader_find: refused', result.stderr)

    def test_refusals(self):
        self.write('a.md', f'{OLD}\n')
        good = self.relocations([(OLD, 'x', 'moved', 'S1')])
        self.refused('--check', '--paths', 'a.md', '--relocations', self.relocations([], 'empty.tsv'))
        bad_header = self.base / 'bad.tsv'
        bad_header.write_text('old\tnew\n' + OLD + '\tx\n')
        self.refused('--check', '--paths', 'a.md', '--relocations', bad_header)
        self.refused('--check', '--paths', 'a.md', '--relocations',
                     self.relocations([(OLD, OLD, 'moved', 'S1')], 'identity.tsv'))
        self.refused('--check', '--paths', 'a.md', '--relocations',
                     self.relocations([(OLD, 'x', 'moved', 'S1'), (OLD, 'y', 'moved', 'S2')], 'dup.tsv'))
        self.refused('--check', '--paths', 'a.md', '--relocations',
                     self.relocations([(OLD, 'x', 'moved')], 'short.tsv'))
        self.refused('--check', '--paths', 'missing.md', '--relocations', good)
        (self.base / 'outside.md').write_text(f'{OLD}\n')
        self.refused('--check', '--paths', '../outside.md', '--relocations', good)
        (self.root / 'linkdir').symlink_to(self.base)
        self.refused('--check', '--paths', 'linkdir/map.tsv', '--relocations', good)
        self.refused('--check', '--paths', 'a.md', '--relocations', good, env_root=False)
        self.refused('--check', '--untracked', '--units', self.base / 'nounits')
        (self.base / 'u1/A').mkdir(parents=True)
        (self.base / 'u1/B').mkdir(parents=True)
        (self.base / 'u1/A/path-map-rows.tsv').write_text(HEADER + f'{OLD}\tx\tmoved\tA\n')
        (self.base / 'u1/B/path-map-rows.tsv').write_text(HEADER + f'{OLD}\ty\tmoved\tB\n')
        self.refused('--check', '--untracked', '--units', self.base / 'u1')
        self.refused('--check', '--relocations', good)


if __name__ == '__main__':
    unittest.main()
