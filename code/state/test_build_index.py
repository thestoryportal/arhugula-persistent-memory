import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import json
from unittest.mock import patch

SCRIPT = Path(__file__).with_name('build_index.py')


class IndexTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        subprocess.run(['git', 'init', '-q', str(self.root)], check=True)
        for folder in ('experiments/e1', 'experiments/e2', 'projects/w1',
                       'projects/orphan', 'evidence/CORPUS', 'program/checkpoints'):
            (self.root / folder).mkdir(parents=True)
        (self.root / 'program/program_state.json').write_text(json.dumps({
            'work_queue': {'items': [{'id': 'w1', 'title': 'First', 'state': 'running'},
                                     {'id': 'w2', 'title': 'Next', 'state': 'queued'},
                                     {'id': 'closed', 'title': 'Done', 'state': 'done'}]}}))
        (self.root / 'experiments/e1/CONTEXT.md').write_text(
            '---\nid: e1\nfamily: c\ntitle: "A: test"\nstatus: designed\n'
            'corpus: [01, 02]\ndecision_ids:\n  - D-1\n---\n# Context\n')
        (self.root / 'experiments/e2/result.json').write_text('{}\n')
        (self.root / 'projects/orphan/notes.md').write_text('# Notes\n')
        (self.root / 'evidence/CORPUS/01.md').write_text('# Evidence\n')
        (self.root / 'program/checkpoints/000-rules.md').write_text('## Rules\n')
        (self.root / 'program/checkpoints/001-live.md').write_text('## LIVE HANDOFF\n')
        self.map = self.root / 'approved.tsv'
        self.map.write_text('old\tnew\tdisposition\tunit\n' + ''.join(
            f'old/{i}\tnew/{i}\tmove\tu\n' for i in range(31820)))

    def run_tool(self, *args):
        return subprocess.run([sys.executable, '-B', str(SCRIPT), *args],
                              env={**os.environ, 'LLMDB_ROOT': str(self.root)},
                              capture_output=True, text=True)

    def write(self):
        result = self.run_tool('--write', '--path-map', str(self.map))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_round_trip_and_determinism(self):
        self.write()
        before = {p.name: p.read_bytes() for p in (self.root / '_index').iterdir()}
        self.write()
        self.assertEqual(before, {p.name: p.read_bytes() for p in (self.root / '_index').iterdir()})
        self.assertEqual(self.run_tool('--check').returncode, 0)
        self.assertEqual((self.root / '_index/path-map.tsv').read_bytes(), self.map.read_bytes())

    def test_drift_in_each_markdown_file(self):
        self.write()
        for name in ('experiments.md', 'projects.md', 'evidence.md', 'checkpoints.md'):
            with self.subTest(name=name):
                path = self.root / '_index' / name
                original = path.read_bytes()
                path.write_bytes(original + b'edited\n')
                result = self.run_tool('--check')
                self.assertEqual(result.returncode, 1)
                self.assertIn(name, result.stdout + result.stderr)
                path.write_bytes(original)
        (self.root / '_index/program-state.md').write_text('unrelated')
        self.assertEqual(self.run_tool('--check').returncode, 0)

    def test_bad_status(self):
        path = self.root / 'experiments/e1/CONTEXT.md'
        path.write_text(path.read_text().replace('designed', 'invalid'))
        result = self.run_tool('--write', '--path-map', str(self.map))
        self.assertEqual(result.returncode, 1)
        self.assertIn('experiments/e1/CONTEXT.md', result.stdout + result.stderr)

    def test_rows_and_handoff(self):
        self.write()
        experiments = (self.root / '_index/experiments.md').read_text()
        self.assertIn('| e2 | — | — | — | — | — |', experiments)
        self.assertIn('Unstamped: 1', experiments)
        self.assertIn('A: test', experiments)
        projects = (self.root / '_index/projects.md').read_text()
        self.assertIn('no queue item', projects)
        self.assertIn('no folder', projects)
        self.assertNotIn('| closed |', projects)
        checkpoints = (self.root / '_index/checkpoints.md').read_text()
        self.assertIn('Newest live handoff: program/checkpoints/001-live.md', checkpoints)
        self.assertLess(checkpoints.index('| 000-rules.md'), checkpoints.index('| 001-live.md'))

    def test_git_invisible_folders_and_folder_guides_are_not_rows(self):
        # git keeps no empty folder, so a fresh checkout must index the same rows
        (self.root / 'experiments/empty/runs').mkdir(parents=True)
        (self.root / 'projects/empty').mkdir()
        for folder in ('experiments', 'evidence/CORPUS', 'program/checkpoints'):
            (self.root / folder / 'CONTEXT.md').write_text('# Guide\n')
        self.write()
        index = self.root / '_index'
        self.assertNotIn('| empty |', (index / 'experiments.md').read_text())
        self.assertIn('Unstamped: 1', (index / 'experiments.md').read_text())
        self.assertNotIn('| empty |', (index / 'projects.md').read_text())
        self.assertNotIn('CONTEXT.md', (index / 'evidence.md').read_text())
        self.assertNotIn('CONTEXT.md', (index / 'checkpoints.md').read_text())

    def test_rows_follow_git_not_the_disk(self):
        (self.root / '.gitignore').write_text('__pycache__/\n')
        (self.root / 'experiments/cache_only/__pycache__').mkdir(parents=True)
        (self.root / 'experiments/cache_only/__pycache__/x.pyc').write_bytes(b'')
        (self.root / 'experiments/link_only').mkdir()
        (self.root / 'experiments/link_only/result.json').symlink_to('missing-target')
        self.write()
        experiments = (self.root / '_index/experiments.md').read_text()
        self.assertNotIn('| cache_only |', experiments)
        self.assertIn('| link_only |', experiments)

    def test_duplicate_old(self):
        self.write()
        path = self.root / '_index/path-map.tsv'
        path.write_text(path.read_text() + 'old/0\tother\tmove\tu\n')
        result = self.run_tool('--check')
        self.assertEqual(result.returncode, 1)
        self.assertIn('old/0', result.stdout + result.stderr)

    def test_map_header_and_count(self):
        self.write()
        path = self.root / '_index/path-map.tsv'
        original = path.read_bytes()
        for content in (b'bad\theader\n', b'old\tnew\tdisposition\tunit\na\tb\tm\tu\n'):
            path.write_bytes(content)
            self.assertEqual(self.run_tool('--check').returncode, 1)
        path.write_bytes(original)

    def test_approved_empty_destination(self):
        self.map.write_text(self.map.read_text() + 'quarantined\t\tquarantine\tu\n')
        self.write()
        self.assertEqual(self.run_tool('--check').returncode, 0)

    def test_header_is_exact_text(self):
        self.write()
        path = self.root / '_index/path-map.tsv'
        path.write_text(path.read_text().replace('old\tnew', '"old"\tnew', 1))
        self.assertEqual(self.run_tool('--check').returncode, 1)

    def test_setext_evidence_heading(self):
        (self.root / 'evidence/CORPUS/02.md').write_text('Setext title\n============\n')
        self.write()
        self.assertIn('| 02.md | Setext title |',
                      (self.root / '_index/evidence.md').read_text())

    def test_frontmatter_before_first_heading(self):
        for name, body, expected in (
                ('02.md', '# Actual heading\n', 'Actual heading'),
                ('03.md', 'Actual setext\n=============\n', 'Actual setext'),
                ('04.md', 'No heading.\n', '—')):
            (self.root / 'evidence/CORPUS' / name).write_text(
                '---\ntitle: metadata\n---\n' + body)
        self.write()
        evidence = (self.root / '_index/evidence.md').read_text()
        for name, expected in [('02.md', 'Actual heading'),
                               ('03.md', 'Actual setext'), ('04.md', '—')]:
            self.assertIn(f'| {name} | {expected} |', evidence)

    def test_original_anchor_map_by_position(self):
        from state.build_index import build_anchor_map, read_anchor_map
        folder = self.root / 'program/runbook'
        folder.mkdir()
        (folder / '00-first.md').write_text('## Rewritten first\n')
        (folder / '08-second.md').write_text('## Rewritten second\n')
        original = ('# Preamble\n## Original first\n### CORPUS/14\n'
                    '```\n## Not a heading\n```\n'
                    '## Original second\n### CORPUS/14\n')
        response = subprocess.CompletedProcess([], 0, original, '')
        with patch('state.build_index.subprocess.run', return_value=response) as git:
            data = build_anchor_map(self.root, {
                'EXPERIMENT_RUNBOOK.md': 'program/EXPERIMENT_RUNBOOK.md'})
        self.assertEqual(git.call_args.args[0],
                         ['git', 'show', '3f1a3b95:EXPERIMENT_RUNBOOK.md'])
        entries = read_anchor_map(data, self.root)
        monolith = 'program/EXPERIMENT_RUNBOOK.md'
        self.assertEqual(entries[(monolith, 'corpus14')], 'program/runbook/00-first.md')
        self.assertEqual(entries[(monolith, 'corpus14-1')], 'program/runbook/08-second.md')
        self.assertNotIn((monolith, 'not-a-heading'), entries)
        self.assertEqual(data.splitlines()[0], b'monolith\tanchor\tpart')

    def test_anchor_map_validation_without_git(self):
        self.write()
        path = self.root / '_index/anchor-map.tsv'
        header = 'monolith\tanchor\tpart\n'
        row = 'program/SESSION_CHECKPOINT.md\tlive\tprogram/checkpoints/001-live.md\n'
        path.write_text(header + row)
        # A fixture has no git repository. --check must use the sealed map.
        self.assertEqual(self.run_tool('--check').returncode, 0)
        for data in ('bad\theader\n', header + row + row,
                     header + 'm\ta\tmissing.md\n'):
            path.write_text(data)
            result = self.run_tool('--check')
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn('anchor-map.tsv', result.stderr)


if __name__ == '__main__':
    unittest.main()
