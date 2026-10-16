import csv
import hashlib
import json
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


class CommonMarkHeadingTests(unittest.TestCase):
    def test_rendered_duplicates_reject_pinned_anchor(self):
        from state.resolve_path import resolve
        root = Path(os.environ['LLMDB_ROOT'])
        part = root / 'knowledge/specs/integrated-spec-v1_2/11-security-layer.md'
        text = part.read_text(encoding='utf-8')
        key = 'knowledge/specs/llm-as-database-v1_2-integrated-spec.md#101-purpose'
        heading = '### 10.1 Purpose\nNEW SECTION\n\n'
        fence = '`' * 3
        cases = [
            ('ATX control', heading + text),
            ('Setext', '10.1 Purpose\n---\nNEW SECTION\n\n' + text),
            ('blockquote', '> ### 10.1 Purpose\n> NEW SECTION\n\n' + text),
            ('list', '- ### 10.1 Purpose\n\n  NEW SECTION\n\n' + text),
            ('mixed fence', fence + '\n~~~\n' + fence + '\n\n' + heading +
             fence + '\n~~~\n' + fence + '\n\n' + text),
            ('long fence', fence + '`\n' + fence + '\n' + fence + '`\n\n' +
             heading + fence + '`\n' + fence + '\n' + fence + '`\n\n' + text),
            ('indented code', '    ' + fence + '\n\n' + heading +
             '    ' + fence + '\n\n' + text),
        ]
        read = Path.read_text
        for name, changed in cases:
            with self.subTest(case=name), patch.object(
                    Path, 'read_text', lambda path, *a, **k:
                    changed if path == part else read(path, *a, **k)):
                with self.assertRaisesRegex(ValueError, 'live headings match'):
                    resolve(key)

    def test_html_comment_returns_original_heading_text(self):
        from markdown_it import MarkdownIt
        from state.resolve_path import heading_entries, resolve
        root = Path(os.environ['LLMDB_ROOT'])
        part = root / 'program/runbook/13-changelog-append-only.md'
        slug = '13-changelog--2026-06-19'
        base, number = slug.rsplit('-', 1)
        changed = ('<!--\n' + ('### ' + base + '\n') * (int(number) + 1) +
                   '-->\n\n' + part.read_text(encoding='utf-8') +
                   '\n\n### ' + slug + '-1\nOTHER SECTION\n')
        read = Path.read_text
        with patch.object(Path, 'read_text', lambda path, *a, **k:
                          changed if path == part else read(path, *a, **k)):
            destination = resolve('program/EXPERIMENT_RUNBOOK.md#' + slug)
        self.assertEqual(destination, str(part.relative_to(root)) + '#' + slug)
        fragment = destination.partition('#')[2]
        heading = next(heading for heading, anchor in heading_entries(changed.splitlines())
                       if anchor == fragment)
        self.assertEqual(heading, '### §13 changelog — 2026-06-19')
        # Check the destination text with the parser, independent of the resolver.
        tokens = MarkdownIt('commonmark').parse(changed)
        headings = [tokens[i + 1].content for i, token in enumerate(tokens)
                    if token.type == 'heading_open']
        self.assertEqual(headings.count('§13 changelog — 2026-06-19'), 1)
        self.assertNotIn(base, headings)
        self.assertEqual(headings[-1], slug + '-1')


class RenderedInlineHeadingTests(unittest.TestCase):
    def assert_duplicate_rejected(self, inline, definitions=''):
        from state.resolve_path import resolve
        root = Path(os.environ['LLMDB_ROOT'])
        part = root / 'knowledge/specs/integrated-spec-v1_2/11-security-layer.md'
        original = part.read_text(encoding='utf-8')
        key = 'knowledge/specs/llm-as-database-v1_2-integrated-spec.md#101-purpose'
        read = Path.read_text
        for position in ('before', 'after'):
            duplicate = '### ' + inline + '\nNEW\n\n' + definitions
            changed = (duplicate + original if position == 'before'
                       else original + '\n\n' + duplicate)
            with self.subTest(position=position), patch.object(
                    Path, 'read_text', lambda path, *a, **k:
                    changed if path == part else read(path, *a, **k)):
                with self.assertRaisesRegex(ValueError, '2 live headings match'):
                    resolve(key)

    def test_underscore_emphasis_duplicate(self):
        self.assert_duplicate_rejected('10.1 _Purpose_')

    def test_reference_link_duplicate(self):
        self.assert_duplicate_rejected('[10.1 Purpose][ref]',
                                       '[ref]: https://example.com\n\n')

    def test_nested_link_destination_duplicate(self):
        self.assert_duplicate_rejected('[10.1 Purpose](https://example.com/a(b)c)')

    def test_padded_code_span_duplicate(self):
        self.assert_duplicate_rejected('` 10.1 Purpose `')

    def test_quoted_html_attribute_duplicate(self):
        self.assert_duplicate_rejected('<span title=">x">10.1 Purpose</span>')

    def test_inline_html_comment_duplicate(self):
        self.assert_duplicate_rejected('10.1 <!-- > -->Purpose')

    def test_source_heading_preserved_with_rendered_slug(self):
        from state.resolve_path import heading_entries
        for inline in ('10.1 _Purpose_', '[10.1 Purpose][ref]',
                       '[10.1 Purpose](https://example.com/a(b)c)',
                       '` 10.1 Purpose `', '<span title=">x">10.1 Purpose</span>',
                       '10.1 <!-- > -->Purpose', '10.1 Purpo&#115;e'):
            heading = '### ' + inline
            with self.subTest(inline=inline):
                self.assertEqual(list(heading_entries(
                    [heading, '', '[ref]: https://example.com'])),
                    [(heading, '101-purpose')])

    def test_rendered_slugs_share_counts(self):
        from state.resolve_path import heading_entries
        counts = {}
        self.assertEqual(list(heading_entries(['### 10.1 _Purpose_'], counts)),
                         [('### 10.1 _Purpose_', '101-purpose')])
        self.assertEqual(list(heading_entries(['### ` 10.1 Purpose `'], counts)),
                         [('### ` 10.1 Purpose `', '101-purpose-1')])
        self.assertEqual(list(heading_entries(['### 10.1 Purpose'], counts)),
                         [('### 10.1 Purpose', '101-purpose-2')])

    def test_unchanged_pinned_heading_resolves(self):
        from state.resolve_path import resolve
        self.assertEqual(resolve(
            'knowledge/specs/llm-as-database-v1_2-integrated-spec.md#101-purpose'),
            'knowledge/specs/integrated-spec-v1_2/11-security-layer.md#101-purpose')


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
        (self.root / '_index/icm21-path-map.tsv').write_text('old\tnew\tdisposition\tunit\n')
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

    def test_absent_relocation_map_raises(self):
        from state.resolve_path import resolve
        (self.root / '_index/icm21-path-map.tsv').unlink()
        with patch.dict(os.environ, LLMDB_ROOT=str(self.root)):
            with self.assertRaisesRegex(ValueError, 'icm21-path-map.tsv'):
                resolve('old/file.md')

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

    def test_sealed_fragment_returns_pinned_anchor(self):
        result = self.run_tool('program/EXPERIMENT_RUNBOOK.md#%63hild-heading')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(),
                         'program/runbook/08-decisions.md#child-heading')

    def test_stale_sealed_fragment_is_an_error(self):
        (self.root / 'program/runbook/08-decisions.md').write_text('## Decisions\n')
        result = self.run_tool('program/EXPERIMENT_RUNBOOK.md#child-heading')
        self.assertEqual(result.returncode, 2)
        self.assertIn('Unknown anchor', result.stderr)
        self.assertIn('heading changed after the pin', result.stderr)

    def test_old_slug_cannot_override_pinned_identity(self):
        anchor = 'a1--batch-vs-sequential-write--done--pass-robust-corpus14-d-a1-1'
        path = self.root / 'program/runbook/08-decisions.md'
        original = path.read_text()
        decoy = ('#### A1 · Batch vs sequential write · **DONE — PASS (robust). '
                 '`CORPUS/14`, `D-A1-1`.**\n')
        path.write_text(original + decoy)
        result = self.run_tool('program/EXPERIMENT_RUNBOOK.md#' + anchor)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), 'program/runbook/08-decisions.md#' +
                         anchor.replace('corpus', 'evidencecorpus'))

    def test_old_slug_cannot_rescue_changed_pinned_heading(self):
        anchor = 'a1--batch-vs-sequential-write--done--pass-robust-corpus14-d-a1-1'
        path = self.root / 'program/runbook/08-decisions.md'
        path.write_text(path.read_text().replace('`evidence/CORPUS/14`', '`CORPUS/14`'))
        result = self.run_tool('program/EXPERIMENT_RUNBOOK.md#' + anchor)
        self.assertEqual(result.returncode, 2)
        self.assertIn('Unknown anchor', result.stderr)
        self.assertIn('heading changed after the pin', result.stderr)

    def test_duplicate_a1_before_pinned_heading_is_an_error(self):
        from state.resolve_path import resolve
        path = self.root / 'program/runbook/08-decisions.md'
        text = path.read_text()
        heading = next(line for line in text.splitlines() if line.startswith('#### A1 '))
        path.write_text(text.replace(heading, heading + '\n' + heading, 1))
        old = ('program/EXPERIMENT_RUNBOOK.md#'
               'a1--batch-vs-sequential-write--done--pass-robust-corpus14-d-a1-1')
        with patch.dict(os.environ, LLMDB_ROOT=str(self.root)):
            with self.assertRaisesRegex(ValueError, 'live headings match') as caught:
                resolve(old)
        self.assertEqual(str(caught.exception),
                         'Unknown anchor for ' + old.replace('#', ': ') +
                         '; 2 live headings match the pinned heading')

    def test_duplicate_a1_after_pinned_heading_is_an_error(self):
        from state.resolve_path import resolve
        path = self.root / 'program/runbook/08-decisions.md'
        text = path.read_text()
        heading = next(line for line in text.splitlines() if line.startswith('#### A1 '))
        path.write_text(text + heading + '\n')
        old = ('program/EXPERIMENT_RUNBOOK.md#'
               'a1--batch-vs-sequential-write--done--pass-robust-corpus14-d-a1-1')
        with patch.dict(os.environ, LLMDB_ROOT=str(self.root)):
            with self.assertRaisesRegex(ValueError, 'live headings match') as caught:
                resolve(old)
        self.assertEqual(str(caught.exception),
                         'Unknown anchor for ' + old.replace('#', ': ') +
                         '; 2 live headings match the pinned heading')

    def test_sealed_anchor_precedence_and_current_exact_source(self):
        result = self.run_tool('program/EXPERIMENT_RUNBOOK.md#child-heading')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), 'program/runbook/08-decisions.md#child-heading')
        result = self.run_tool('program/EXPERIMENT_RUNBOOK.md#current-only')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), 'program/runbook/08-decisions.md#current-only')


class DuplicateBinding(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def manifest(self, targets):
        rows = [{'id': f'R{number}', 'reference': 'old/file.md', 'consumer': 'a.md',
                 'consumer_final': 'b/a.md', 'final_target': target}
                for number, target in enumerate(targets, 1)]
        data = ''.join(json.dumps(row) + '\n' for row in rows).encode('utf-8')
        (self.root / 'refs.jsonl').write_bytes(data)
        return {'references': {'path': 'refs.jsonl',
                               'sha256': hashlib.sha256(data).hexdigest()}}

    def test_identical_targets_resolve(self):
        from state.resolve_path import resolve_reference
        manifest = self.manifest(['new/file.md#part', 'new/file.md#part'])
        with patch.dict(os.environ, LLMDB_ROOT=str(self.root)):
            self.assertEqual(resolve_reference('a.md', 'old/file.md', manifest),
                             'new/file.md#part')

    def test_distinct_targets_ambiguous(self):
        from state.resolve_path import resolve_reference
        manifest = self.manifest(['new/file.md', 'other/file.md'])
        with patch.dict(os.environ, LLMDB_ROOT=str(self.root)):
            with self.assertRaisesRegex(ValueError, 'Ambiguous') as caught:
                resolve_reference('a.md', 'old/file.md', manifest)
        self.assertIn('R1', str(caught.exception))
        self.assertIn('R2', str(caught.exception))


if __name__ == '__main__':
    unittest.main()
