import os
from pathlib import Path
import subprocess
import shutil
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

    def test_original_anchor_map_at_pin(self):
        from state.build_index import build_anchor_map, read_anchor_map
        folder = self.root / 'program/runbook'
        folder.mkdir()
        (folder / '00-first.md').write_text(
            '# Preamble\n## Rewritten first\n### evidence/CORPUS/14\n')
        (folder / '08-second.md').write_text(
            '## Rewritten second\n### evidence/CORPUS/14\n')
        original = ('# Preamble\n## Original first\n### CORPUS/14\n'
                    '```\n## Not a heading\n```\n'
                    '## Original second\n### CORPUS/14\n')
        pinned = {
            '3f1a3b95:EXPERIMENT_RUNBOOK.md': original,
            '4e679b15:program/runbook/00-first.md':
                '# Preamble\n## Rewritten first\n### evidence/CORPUS/14\n',
            '4e679b15:program/runbook/08-second.md':
                '## Rewritten second\n### evidence/CORPUS/14\n',
        }
        (folder / '00-first.md').write_text('## Later live heading\n')
        def git_show(args, **kwargs):
            return subprocess.CompletedProcess(args, 0, pinned[args[-1]], '')
        with patch('state.build_index.subprocess.run', side_effect=git_show):
            data = build_anchor_map(self.root, {
                'EXPERIMENT_RUNBOOK.md': 'program/EXPERIMENT_RUNBOOK.md'})
        entries = read_anchor_map(data, self.root)
        monolith = 'program/EXPERIMENT_RUNBOOK.md'
        self.assertEqual(entries[(monolith, 'preamble')],
                         ('program/runbook/00-first.md', 'preamble'))
        self.assertEqual(entries[(monolith, 'corpus14')],
                         ('program/runbook/00-first.md', 'evidencecorpus14'))
        self.assertEqual(entries[(monolith, 'corpus14-1')],
                         ('program/runbook/08-second.md', 'evidencecorpus14'))
        self.assertNotIn((monolith, 'not-a-heading'), entries)
        self.assertEqual(data.splitlines()[0], b'monolith\tanchor\tpart\tcurrent_anchor')

    def test_anchor_map_rejects_unequal_pinned_counts(self):
        from state.build_index import build_anchor_map
        folder = self.root / 'program/runbook'
        folder.mkdir()
        (folder / '00-first.md').write_text('## First\n')
        responses = [subprocess.CompletedProcess([], 0, body, '') for body in
                     ('## First\n### Missing\n', '## First\n')]
        with patch('state.build_index.subprocess.run', side_effect=responses):
            with self.assertRaisesRegex(ValueError, 'heading counts'):
                build_anchor_map(self.root, {
                    'EXPERIMENT_RUNBOOK.md': 'program/EXPERIMENT_RUNBOOK.md'})

    def test_anchor_map_rejects_changed_pinned_level(self):
        from state.build_index import build_anchor_map
        folder = self.root / 'program/runbook'
        folder.mkdir()
        (folder / '00-first.md').write_text('## First\n#### Child\n')
        responses = [subprocess.CompletedProcess([], 0, body, '') for body in
                     ('## First\n### Child\n', '## First\n#### Child\n')]
        with patch('state.build_index.subprocess.run', side_effect=responses):
            with self.assertRaisesRegex(ValueError, 'heading level'):
                build_anchor_map(self.root, {
                    'EXPERIMENT_RUNBOOK.md': 'program/EXPERIMENT_RUNBOOK.md'})

    def test_anchor_map_rejects_unreadable_pin(self):
        from state.build_index import build_anchor_map
        folder = self.root / 'program/runbook'
        folder.mkdir()
        (folder / '00-first.md').write_text('## First\n')
        responses = [subprocess.CompletedProcess([], 0, '## First\n', ''),
                     subprocess.CompletedProcess([], 1, '', 'pin not found')]
        with patch('state.build_index.subprocess.run', side_effect=responses):
            with self.assertRaisesRegex(ValueError, 'cannot read 4e679b15:'):
                build_anchor_map(self.root, {
                    'EXPERIMENT_RUNBOOK.md': 'program/EXPERIMENT_RUNBOOK.md'})

    def test_anchor_map_validation_without_git(self):
        self.write()
        path = self.root / '_index/anchor-map.tsv'
        header = 'monolith\tanchor\tpart\tcurrent_anchor\n'
        row = ('program/SESSION_CHECKPOINT.md\tlive\t'
               'program/checkpoints/001-live.md\tlive-handoff\n')
        path.write_text(header + row)
        # A fixture has no git repository. --check must use the sealed map.
        self.assertEqual(self.run_tool('--check').returncode, 0)
        for data in ('bad\theader\n', header + row + row,
                     header + 'm\ta\tmissing.md\ta\n',
                     header + 'm\ta\tprogram/checkpoints/001-live.md\t\n'):
            path.write_text(data)
            result = self.run_tool('--check')
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn('anchor-map.tsv', result.stderr)


class LivingAnchorMapTests(unittest.TestCase):
    def setUp(self):
        from state.resolve_path import SPLITS
        source = Path(os.environ['LLMDB_ROOT'])
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / '_index').mkdir()
        shutil.copy2(source / '_index/path-map.tsv', self.root / '_index/path-map.tsv')
        for folder in SPLITS.values():
            (self.root / folder).mkdir(parents=True)
            for part in (source / folder).glob('[0-9]*.md'):
                shutil.copy2(part, self.root / folder / part.name)
        self.part = self.root / 'program/runbook/08-experiment-decision-tree-tracks-af.md'
        self.git_dir = subprocess.run(
            ['git', '-C', str(source), 'rev-parse', '--absolute-git-dir'],
            capture_output=True, text=True, check=True).stdout.strip()

    def rebuild(self):
        from state.build_index import build_anchor_map, read_anchor_map, read_path_map
        mapping = read_path_map((self.root / '_index/path-map.tsv').read_bytes())
        with patch.dict(os.environ, GIT_DIR=self.git_dir):
            data = build_anchor_map(self.root, mapping)
        (self.root / '_index/anchor-map.tsv').write_bytes(data)
        return read_anchor_map(data, self.root)

    def assert_fragment_exists(self, destination):
        from state.resolve_path import heading_entries
        part, marker, fragment = destination.partition('#')
        self.assertEqual(marker, '#')
        slugs = {slug for _, slug in heading_entries(
            (self.root / part).read_text(encoding='utf-8').splitlines())}
        self.assertIn(fragment, slugs)

    def assert_mutation_keeps_identity(self, changed):
        from state.resolve_path import resolve
        self.rebuild()
        before = (self.root / '_index/anchor-map.tsv').read_bytes()
        self.part.write_text(changed, encoding='utf-8')
        self.rebuild()
        with self.subTest(check='map bytes'):
            self.assertEqual((self.root / '_index/anchor-map.tsv').read_bytes(), before)
        old_anchors = (
            'a1--batch-vs-sequential-write--done--pass-robust-corpus14-d-a1-1',
            'a2--relation-balanced-in-solve-sentinels-3-disjoint-pools--done--partial-strong-directional-corpus15-d-a2-1')
        from state.resolve_path import heading_entries
        with patch.dict(os.environ, LLMDB_ROOT=str(self.root)):
            for label, old_anchor in zip(('A1 ', 'A2 '), old_anchors):
                with self.subTest(heading=label):
                    try:
                        part, marker, fragment = resolve(
                            'EXPERIMENT_RUNBOOK.md#' + old_anchor).partition('#')
                    except ValueError as error:
                        self.fail(f'{label}valid alias was lost: {error}')
                    headings = {slug: heading for heading, slug in heading_entries(
                        (self.root / part).read_text(encoding='utf-8').splitlines())}
                    self.assertEqual(marker, '#')
                    self.assertIn(fragment, headings)
                    self.assertIn(label, headings[fragment])
                    print(f'{label.strip()} -> {headings[fragment]}')

    def test_insert_heading_keeps_alias_identity(self):
        text = self.part.read_text(encoding='utf-8')
        heading = '#### A1 · Batch vs sequential write'
        self.assertEqual(text.count(heading), 1)
        self.assert_mutation_keeps_identity(text.replace(
            heading, '### New close-out heading\n' + heading, 1))

    def test_swap_sections_keeps_alias_identity(self):
        text = self.part.read_text(encoding='utf-8')
        a, z, end = [text.index('#### ' + label) for label in ('A1 ', 'A2 ', 'A2b ')]
        self.assert_mutation_keeps_identity(
            text[:a] + text[z:end] + text[a:z] + text[end:])

    def test_identity_at_pin_differs_only_by_path_rewrite(self):
        from state.build_index import read_path_map
        from state.resolve_path import heading_entries
        entries = self.rebuild()
        mapping = read_path_map((self.root / '_index/path-map.tsv').read_bytes())
        pairs = [(key, value) for key, value in entries.items() if key[1] != value[1]]
        self.assertTrue(pairs)
        for (monolith, old_anchor), (part, current_anchor) in pairs:
            old = next(name for name, new in mapping.items() if new == monolith)
            def headings_at(revision, path):
                result = subprocess.run(['git', 'show', f'{revision}:{path}'],
                                        cwd=self.root, env={**os.environ, 'GIT_DIR': self.git_dir},
                                        capture_output=True, text=True, check=True)
                return {slug: heading for heading, slug in heading_entries(
                    result.stdout.splitlines())}
            historical = headings_at('3f1a3b95', old)[old_anchor]
            pinned = headings_at('4e679b15', part)[current_anchor]
            self.assertEqual(pinned, historical.replace('`CORPUS/', '`evidence/CORPUS/'))
            self.assertEqual(current_anchor, old_anchor.replace('corpus', 'evidencecorpus'))
            print(f'PIN PAIR {monolith}#{old_anchor} -> {part}#{current_anchor}')

    def test_deleted_heading_errors_and_all_other_fragments_exist(self):
        from state.resolve_path import resolve
        text = self.part.read_text(encoding='utf-8')
        heading = '### TRACK A — Cross-entity isolation fix (THE active blocker)\n'
        self.assertEqual(text.count(heading), 1)
        self.part.write_text(text.replace(heading, '', 1), encoding='utf-8')
        entries = self.rebuild()
        removed = ('program/EXPERIMENT_RUNBOOK.md',
                   'track-a--cross-entity-isolation-fix-the-active-blocker')
        self.assertEqual(len(entries), 517)
        self.assertEqual(entries[removed][1], removed[1])
        with patch.dict(os.environ, LLMDB_ROOT=str(self.root)):
            with self.assertRaisesRegex(ValueError, 'Unknown anchor'):
                resolve('#'.join(removed))
            for key in entries:
                if key != removed:
                    self.assert_fragment_exists(resolve('#'.join(key)))


if __name__ == '__main__':
    unittest.main()
