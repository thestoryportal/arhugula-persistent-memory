"""Exact relocation and relocated anchor resolver cases (ReaderControls)."""
import inspect
import os
from unittest.mock import patch

from icm21_fixtures import HEADER, digest, put


class ResolverCase:
    def test_exact_relocation_and_citations(self):
        resolver = self.module('code/state/resolve_path.py', 'relocate', 'resolve_reference')
        mapping = {'old/file.md': 'middle/file.md', 'middle/file.md': 'final/file.md'}
        self.assertEqual(resolver.relocate('old/file.md', mapping), 'final/file.md')
        self.assertEqual(resolver.relocate('middle/file.md', mapping), 'final/file.md')
        self.assertEqual(resolver.relocate('current/file.md', mapping), 'current/file.md')
        self.assertEqual(resolver.relocate('old/file.md.extra', mapping), 'old/file.md.extra')
        for bad in ({'a': 'a'}, {'a': 'b', 'b': 'a'}, {'z': 'z', **mapping}):
            with self.subTest(mapping=bad), self.assertRaises(ValueError):
                resolver.relocate('current/file.md', bad)
        root = self.miniature()
        rows = []
        for suffix in (':1,3,9-12', ':3–7', '#exact-anchor'):
            for consumer, spelling, intermediate, final in (
                    ('plans/old/verdict.md', 'design.md', 'plans/old/design.md', 'plans/new/decisions_log.md'),
                    ('plans/old/handoff.md', 'verdict.md', 'plans/old/verdict.md', 'plans/new/design.md')):
                rows.append({'schema_version': 1, 'id': 'REF-' + str(len(rows)),
                    'prd_ids': ['ICM-R6'], 'consumer': consumer,
                    'consumer_final': consumer.replace('/old/', '/new/'),
                    'consumer_sha256': digest(b'historical fixture'), 'reference': spelling + suffix,
                    'intermediate': intermediate + suffix, 'final_target': final + suffix,
                    'role': 'historical-source', 'byte_offset': None, 'repair_path': None,
                    'owner': 'integration', 'check_id': 'C-REFERENCES'})
        manifest = self.reference_manifest(root, rows)
        with patch.dict(os.environ, {'LLMDB_ROOT': str(root)}):
            for row in rows:
                for consumer in (row['consumer'], row['consumer_final']):
                    self.assertEqual(resolver.resolve_reference(consumer, row['reference'], manifest),
                                     row['final_target'])
            with self.assertRaises(ValueError):
                resolver.resolve_reference('unrelated/verdict.md', rows[0]['reference'], manifest)
        duplicate = dict(rows[0], id='REF-AMBIGUOUS', final_target='wrong/file.md:1,3,9-12')
        manifest = self.reference_manifest(root, rows + [duplicate])
        with self.assertRaises(ValueError):
            resolver.resolve_reference(rows[0]['consumer'], rows[0]['reference'], manifest)

    def test_relocated_anchor_targets(self):
        module = self.index_module()
        self.assertIn('relocations', inspect.signature(module.read_anchor_map).parameters,
                      'absent behavior: sealed anchors validate relocated parts')
        root = self.miniature()
        raw = b'monolith\tanchor\tpart\tcurrent_anchor\nprogram/EXPERIMENT_RUNBOOK.md\told-heading\tprogram/runbook/01.md\texact-heading\n'
        target = put(root, 'program/final/01.md', b'## Exact heading\n')
        mapping = {'program/runbook/01.md': 'program/final/01.md'}
        self.assertEqual(module.read_anchor_map(raw, root, relocations=mapping),
                         {('program/EXPERIMENT_RUNBOOK.md', 'old-heading'):
                          ('program/runbook/01.md', 'exact-heading')})
        with self.assertRaises(ValueError):
            module.read_anchor_map(raw, root)
        with self.assertRaises(ValueError):
            module.read_anchor_map(raw, root, relocations={'program/runbook/01.md': 'missing.md'})
        put(root, '_index/anchor-map.tsv', raw)
        put(root, '_index/path-map.tsv', HEADER + b'RUNBOOK.md\tprogram/EXPERIMENT_RUNBOOK.md\tmove\tfixture\n')
        put(root, '_index/icm21-path-map.tsv', HEADER + b'program/runbook/01.md\tprogram/final/01.md\tmove\tfixture\n')
        resolver = self.module('code/state/resolve_path.py', 'relocate')
        with patch.dict(os.environ, {'LLMDB_ROOT': str(root)}):
            self.assertEqual(resolver.resolve('RUNBOOK.md#old-heading'), 'program/final/01.md#exact-heading')
            target.write_bytes(b'## Changed heading\n')
            with self.assertRaises(ValueError):
                resolver.resolve('RUNBOOK.md#old-heading')
            target.write_bytes(b'## Exact heading\n## Exact heading\n')
            with self.assertRaises(ValueError):
                resolver.resolve('RUNBOOK.md#old-heading')
        self.assertEqual((root / '_index/anchor-map.tsv').read_bytes(), raw)
