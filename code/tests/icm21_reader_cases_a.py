"""ReaderControls queue, index, relocation and LabViz-adapter cases (mixin for test_icm21)."""
import copy
import inspect
import json
import os
from pathlib import Path
import unittest
from unittest.mock import patch

from icm21_fixtures import (D2_POSITIVE, HEADER, INDEX_PATHS, MAP_PATH, SOURCE_ROOT,
                            binding, digest, encoded, put, snapshot)


class ReaderCasesA:
    @unittest.skip('ICM v2.1 open ticket: not built yet')
    def test_queue_compatibility_and_candidates(self):
        self.require_file('code/state/icm21_check.py', 'D1 strict queue candidate validation')
        root = self.miniature()
        original = (SOURCE_ROOT / 'program/program_state.json').read_bytes()
        state = json.loads(original)
        items = state['work_queue']['items']
        self.assertEqual(len(items), 16)
        self.assertTrue(all('artifact' not in item for item in items))
        put(root, 'program/program_state.json', original)
        view = self.generate(root)['projects.md'].decode()
        self.assertIn('legacy-unspecified', view)
        self.assertEqual((root / 'program/program_state.json').read_bytes(), original)
        for artifact, label in ((None, 'no-materialized-record'), *(
                ({'kind': kind, 'path': 'records/' + kind}, kind)
                for kind in ('project', 'plan', 'audit', 'research', 'experiment'))):
            with self.subTest(artifact=artifact):
                candidate = copy.deepcopy(state)
                candidate['work_queue']['items'][0]['artifact'] = artifact
                if artifact is not None:
                    (root / artifact['path']).mkdir(parents=True, exist_ok=True)
                data = encoded(candidate)
                put(root, 'program/program_state.json', data)
                self.assertIn(label, self.generate(root)['projects.md'].decode())
                self.assertEqual((root / 'program/program_state.json').read_bytes(), data)
        for artifact in ({}, {'kind': 'unknown', 'path': 'records/project'},
                         {'kind': 'project', 'path': '../escape'},
                         {'kind': 'project', 'path': str(self.scratch)},
                         {'kind': 'project', 'path': 'missing'},
                         {'kind': 'project', 'path': 'records/project', 'extra': 1}):
            candidate = copy.deepcopy(state)
            candidate['work_queue']['items'][0]['artifact'] = artifact
            put(root, 'program/program_state.json', encoded(candidate))
            with self.subTest(invalid=artifact), self.assertRaises(ValueError):
                self.generate(root)
        # The references checker applies strict creation/repair admission separately.
        put(root, 'program/program_state.json', original)
        self.assertEqual(json.loads(original)['updated'], state['updated'])
        self.assertEqual(json.loads(original)['next_actions'][6], state['next_actions'][6])
        self.assertEqual(json.loads(original)['work_queue']['items'][2]['notes'][1],
                         state['work_queue']['items'][2]['notes'][1])

    @unittest.skip('ICM v2.1 open ticket: not built yet')
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

    def reference_manifest(self, root, rows):
        references = put(root, 'references.jsonl', b''.join(encoded(row) + b'\n' for row in rows))
        registries = put(root, 'registries.json', encoded({'schema_version': 1,
            'dispatcher': ['checker'], 'reader_registry': [], 'loader_registry': []}))
        executor = put(root, 'executor.json', encoded({'schema_version': 1, 'operations': []}))
        repairs = put(root, 'repairs.json', encoded({'schema_version': 1, 'repairs': []}))
        coverage = put(root, 'coverage.json', encoded({'schema_version': 1, 'scope': 'miniature',
            'coverage': {'inspected': [str(root)], 'excluded': [],
                         'required_registry_ids': [], 'checked_registry_ids': []}, 'sources': []}))
        return {'schema_version': 1, 'references': binding(references), 'registries': binding(registries),
                'executor': binding(executor), 'repairs': binding(repairs), 'coverage': binding(coverage)}

    @unittest.skip('ICM v2.1 open ticket: not built yet')
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

    @unittest.skip('ICM v2.1 open ticket: not built yet')
    def test_portable_map_identity(self):
        module = self.index_module()
        self.assertIn('--labviz-map-only', inspect.getsource(module.main),
                      'absent behavior: portable derived map generation')
        first, second = self.miniature('A'), self.miniature('B')
        for root in (first, second):
            self.portable_fixture(root)
        original = self.publish_miniature(first)
        for name in (*INDEX_PATHS, MAP_PATH):
            put(second, name, (first / name).read_bytes())
        self.assertNotIn(str(first).encode(), original)
        for root in (first, second):
            before = snapshot(root)
            for flags in (('--check',), ('--check', '--labviz-map-only')):
                result = self.cli(root, 'code/state/build_index.py', *flags)
                self.assertEqual(result.returncode, 0, (result.stdout + result.stderr).decode())
            self.labviz(root)
            self.assertEqual(snapshot(root), before)
        for name in D2_POSITIVE['inputs']:
            initial = (second / name).read_bytes()
            (second / name).write_bytes(initial + b'changed\tinput\tmove\tfixture\n')
            for flags in (('--check',), ('--check', '--labviz-map-only')):
                self.assertEqual(self.cli(second, 'code/state/build_index.py', *flags).returncode, 1)
            with self.assertRaises(ValueError):
                self.labviz(second)
            (second / name).write_bytes(initial)
            self.assertEqual(self.cli(second, 'code/state/build_index.py', '--check').returncode, 0)
            self.labviz(second)
            self.assertEqual((second / MAP_PATH).read_bytes(), original)

    @unittest.skip('ICM v2.1 open ticket: not built yet')
    def test_labviz_adapter_identity(self):
        self.module('code/state/resolve_path.py', 'relocate')
        root = self.miniature()
        leaves = self.portable_fixture(root)
        self.publish_miniature(root)
        module, program = self.labviz(root)
        accepted = json.loads((root / 'leaves.json').read_bytes())
        self.assertEqual(accepted, leaves)
        before = snapshot(root)
        for leaf in accepted:
            self.assertEqual(digest((root / leaf['target']).read_bytes()), leaf['sha256'])
            self.assertEqual(module._moved(leaf['source'], program.moves), [leaf['target']])
            self.assertTrue(program._cites(leaf['source'], leaf['target']))
            self.assertFalse(program._cites(leaf['source'], leaf['target'] + '.wrong'))
        self.assertEqual(module._moved('results/absent/file.md', program.moves), [])
        self.assertTrue(all(isinstance(x, str) for x in module._moved('results/context_rot_audit_20261012/', program.moves)))
        with self.assertRaises(ValueError):
            module._moved('a', {'a': 'b', 'b': 'a'})
        self.assertEqual(snapshot(root), before)
        original = (root / MAP_PATH).read_bytes()
        for field, value in (('path', '/foreign/path-map.tsv'),
                             ('path', '_index/wrong.tsv'), ('path', '../path-map.tsv'),
                             ('sha256', '0' * 64)):
            candidate = json.loads(original)
            candidate['derived_from']['sealed'][field] = value
            put(root, MAP_PATH, encoded(candidate))
            before = snapshot(root)
            with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                self.labviz(root)
            self.assertEqual(snapshot(root), before)
        put(root, MAP_PATH, original)
        for name in D2_POSITIVE['inputs']:
            source = root / name
            parked = source.with_name(source.name + '.parked')
            source.rename(parked)
            with self.subTest(missing=name), self.assertRaises(ValueError):
                self.labviz(root)
            source.symlink_to(parked)
            with self.subTest(linked=name), self.assertRaises(ValueError):
                self.labviz(root)
            source.unlink()
            parked.rename(source)
            self.labviz(root)
        self.assertEqual((root / MAP_PATH).read_bytes(), original)

    @unittest.skip('ICM v2.1 open ticket: not built yet')
    def test_current_index_outputs(self):
        self.require_file('code/state/icm21_check.py', 'installed D1 current index outputs')
        expected = self.generate(SOURCE_ROOT)
        for relative in INDEX_PATHS:
            self.assertEqual(digest((SOURCE_ROOT / relative).read_bytes()),
                             digest(expected[Path(relative).name]), relative)
        self.assertIn('legacy-unspecified', (SOURCE_ROOT / '_index/projects.md').read_text())
