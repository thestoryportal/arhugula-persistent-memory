import csv
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).with_name('resolve_path.py')


class DestinationFragmentTests(unittest.TestCase):
    def test_all_mapped_fragments_exist_in_destination(self):
        from state.resolve_path import heading_entries, resolve
        root = Path(os.environ['LLMDB_ROOT'])
        missing = []
        with (root / '_index/anchor-map.tsv').open(encoding='utf-8') as source:
            rows = list(csv.DictReader(source, delimiter='\t'))
        self.assertEqual(len(rows), 517)
        for row in rows:
            old = f'{row["monolith"]}#{row["anchor"]}'
            destination, marker, fragment = resolve(old).partition('#')
            slugs = {slug for _, slug in heading_entries(
                (root / destination).read_text(encoding='utf-8').splitlines())}
            if not marker or fragment not in slugs:
                missing.append(f'{old} -> {destination}#{fragment}')
        print(f'{len(rows)} rows checked and {len(missing)} missing')
        self.assertEqual(missing, [], '\n'.join(missing))

    def test_a1_fragment_exists_in_destination(self):
        from state.resolve_path import heading_entries, resolve
        root = Path(os.environ['LLMDB_ROOT'])
        destination, marker, fragment = resolve(
            'EXPERIMENT_RUNBOOK.md#'
            'a1--batch-vs-sequential-write--done--pass-robust-corpus14-d-a1-1'
        ).partition('#')
        slugs = {slug for _, slug in heading_entries(
            (root / destination).read_text(encoding='utf-8').splitlines())}
        self.assertEqual(marker, '#')
        self.assertIn(fragment, slugs)
        self.assertEqual(fragment,
                         'a1--batch-vs-sequential-write--done--pass-robust-'
                         'evidencecorpus14-d-a1-1')


class ResolverTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / '_index').mkdir()
        (self.root / 'program/runbook').mkdir(parents=True)
        (self.root / '_index/path-map.tsv').write_text(
            'old\tnew\tdisposition\tunit\n'
            'old/file.md\tnew/file.md\tmove\tu\n'
            'program/EXPERIMENT_RUNBOOK.md\tprogram/runbook\tsplit\tu\n')
        (self.root / 'program/runbook/00-entry.md').write_text(
            '## §0 — ENTRY POINT (read first, every session)\n\n### Child heading\n')

        (self.root / 'program/runbook/08-decisions.md').write_text(
            '## Decisions\n'
            '#### A1 · Batch vs sequential write · **DONE — PASS (robust). '
            '`evidence/CORPUS/14`, `D-A1-1`.**\n'
            '#### A2 · Relation-balanced in-solve sentinels (3 disjoint pools) · '
            '**DONE — PARTIAL (strong, directional). `evidence/CORPUS/15`, `D-A2-1`.**\n'
            '### Child heading\n### Current only\n')
        (self.root / '_index/anchor-map.tsv').write_text(
            'monolith\tanchor\tpart\tcurrent_anchor\n'
            'program/EXPERIMENT_RUNBOOK.md\t'
            'a1--batch-vs-sequential-write--done--pass-robust-corpus14-d-a1-1\t'
            'program/runbook/08-decisions.md\t'
            'a1--batch-vs-sequential-write--done--pass-robust-evidencecorpus14-d-a1-1\n'
            'program/EXPERIMENT_RUNBOOK.md\t'
            'a2--relation-balanced-in-solve-sentinels-3-disjoint-pools--done--partial-strong-directional-corpus15-d-a2-1\t'
            'program/runbook/08-decisions.md\t'
            'a2--relation-balanced-in-solve-sentinels-3-disjoint-pools--done--partial-strong-directional-evidencecorpus15-d-a2-1\n'
            'program/EXPERIMENT_RUNBOOK.md\tchild-heading\t'
            'program/runbook/08-decisions.md\tchild-heading\n')

    def run_tool(self, value):
        return subprocess.run([sys.executable, '-B', str(SCRIPT), value],
                              env={**os.environ, 'LLMDB_ROOT': str(self.root)},
                              capture_output=True, text=True)

    def test_moved_file(self):
        result = self.run_tool('old/file.md')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), 'new/file.md')

    def test_split_anchor_and_folder(self):
        anchor = '0--entry-point-read-first-every-session'
        result = self.run_tool('program/EXPERIMENT_RUNBOOK.md#' + anchor)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), 'program/runbook/00-entry.md#' + anchor)
        self.assertEqual(self.run_tool('program/EXPERIMENT_RUNBOOK.md').stdout.strip(), 'program/runbook')

    def test_unknown_does_not_match_prefix(self):
        for value in ('old/file.md/extra', 'missing', 'program/EXPERIMENT_RUNBOOK.md#missing'):
            result = self.run_tool(value)
            self.assertEqual(result.returncode, 2)
            self.assertIn('Unknown', result.stderr)

    def test_function(self):
        from state.resolve_path import resolve
        with patch.dict(os.environ, LLMDB_ROOT=str(self.root)):
            self.assertEqual(resolve('old/file.md'), 'new/file.md')

    def test_no_assigned_destination(self):
        path = self.root / '_index/path-map.tsv'
        path.write_text(path.read_text() + 'quarantined\t\tquarantine\tu\n')
        result = self.run_tool('quarantined')
        self.assertEqual(result.returncode, 2)
        self.assertIn('No new path', result.stderr)

    def test_pre_split_map_destination(self):
        path = self.root / '_index/path-map.tsv'
        path.write_text(path.read_text() +
                        'EXPERIMENT_RUNBOOK.md\tprogram/EXPERIMENT_RUNBOOK.md\tmove\tu\n')
        result = self.run_tool('EXPERIMENT_RUNBOOK.md#0--entry-point-read-first-every-session')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(),
                         'program/runbook/00-entry.md#0--entry-point-read-first-every-session')

    def test_original_rewritten_anchors(self):
        path = self.root / '_index/path-map.tsv'
        path.write_text(path.read_text() +
                        'EXPERIMENT_RUNBOOK.md\tprogram/EXPERIMENT_RUNBOOK.md\tmove\tu\n')
        for anchor in (
                'a1--batch-vs-sequential-write--done--pass-robust-corpus14-d-a1-1',
                'a2--relation-balanced-in-solve-sentinels-3-disjoint-pools--done--partial-strong-directional-corpus15-d-a2-1'):
            for old in ('program/EXPERIMENT_RUNBOOK.md', 'EXPERIMENT_RUNBOOK.md'):
                result = self.run_tool(old + '#' + anchor)
                self.assertEqual(result.returncode, 0, result.stderr)
                destination, _, fragment = result.stdout.strip().partition('#')
                from state.resolve_path import heading_entries
                slugs = {slug for _, slug in heading_entries(
                    (self.root / destination).read_text().splitlines())}
                self.assertIn(fragment, slugs)
                self.assertEqual(fragment, anchor.replace('corpus', 'evidencecorpus'))

    def test_sealed_fragment_keeps_existing_encoded_anchor(self):
        result = self.run_tool('program/EXPERIMENT_RUNBOOK.md#%63hild-heading')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(),
                         'program/runbook/08-decisions.md#%63hild-heading')

    def test_stale_sealed_fragment_is_an_error(self):
        (self.root / 'program/runbook/08-decisions.md').write_text('## Decisions\n')
        result = self.run_tool('program/EXPERIMENT_RUNBOOK.md#child-heading')
        self.assertEqual(result.returncode, 2)
        self.assertIn('Unknown anchor', result.stderr)

    def test_sealed_anchor_precedence_and_current_exact_source(self):
        result = self.run_tool('program/EXPERIMENT_RUNBOOK.md#child-heading')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), 'program/runbook/08-decisions.md#child-heading')
        result = self.run_tool('program/EXPERIMENT_RUNBOOK.md#current-only')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), 'program/runbook/08-decisions.md#current-only')


if __name__ == '__main__':
    unittest.main()
