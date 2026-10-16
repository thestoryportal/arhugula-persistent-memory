"""ReaderControls D2 wire, dispatch-coverage and registry-adapter cases (mixin for test_icm21)."""
import copy
import json
from pathlib import Path
import unittest

from icm21_fixtures import D2_POSITIVE, HEADER, binding, digest, encoded, put, sealed


class ReaderCasesB:
    @unittest.skip('ICM v2.1 open ticket: not built yet')
    def test_d2_wire_parser(self):
        self.require_file('code/state/icm21_check.py', 'D2-only MapBinding parser')
        examples = json.loads(sealed('WIRE-EXAMPLES.json'))
        examples['examples'] = [x for x in examples['examples'] if x['type'] == 'LabvizMoves']
        self.assertEqual(len(examples['examples']), 2)
        positive = copy.deepcopy(examples['examples'][0])
        positive['value'] = json.loads(D2_POSITIVE['map'])
        positive['expected'] = 'PASS'
        examples['examples'] = [positive]
        for name, data in D2_POSITIVE['inputs'].items():
            put(self.scratch, name, data)
        self.assertEqual(self.wire(self.scratch, examples).returncode, 0)
        for spelling in ('/foreign/path-map.tsv', '_index/wrong.tsv', '../path-map.tsv'):
            candidate = copy.deepcopy(examples)
            candidate['examples'][0]['value']['derived_from']['sealed']['path'] = spelling
            self.assertEqual(self.wire(self.scratch, candidate).returncode, 1)
        for name in D2_POSITIVE['inputs']:
            original = (self.scratch / name).read_bytes()
            (self.scratch / name).write_bytes(original + b'changed')
            self.assertEqual(self.wire(self.scratch, examples).returncode, 1)
            (self.scratch / name).write_bytes(original)
        for change in (lambda v: v.update(extra=True),
                       lambda v: v.update(about='wrong identity'),
                       lambda v: v.update(moves=[]),
                       lambda v: v['derived_from']['sealed'].update(extra=True),
                       lambda v: v['derived_from']['sealed'].update(sha256='short')):
            candidate = copy.deepcopy(examples)
            change(candidate['examples'][0]['value'])
            self.assertEqual(self.wire(self.scratch, candidate).returncode, 1)
        for name in D2_POSITIVE['inputs']:
            source = self.scratch / name
            parked = source.with_name(source.name + '.parked')
            source.rename(parked)
            self.assertEqual(self.wire(self.scratch, examples).returncode, 1)
            source.symlink_to(parked)
            self.assertEqual(self.wire(self.scratch, examples).returncode, 1)
            source.unlink()
            parked.rename(source)
        self.assertEqual(self.wire(self.scratch, examples).returncode, 0)
        # Only LabvizMoves changes: ordinary Binding must remain absolute.
        ordinary = copy.deepcopy(examples)
        ordinary['examples'][0].update(type='Binding', value={'path': '_index/path-map.tsv',
                                                             'sha256': digest(HEADER)})
        self.assertEqual(self.wire(self.scratch, ordinary).returncode, 1)

    @unittest.skip('ICM v2.1 open ticket: not built yet')
    def test_dispatch_coverage_and_ownership(self):
        self.module('code/state/icm21_check.py', 'check_references')
        # Reuse the sealed representative records and semantic counterexamples.
        examples = json.loads(sealed('WIRE-EXAMPLES.json'))
        examples['examples'] = [x for x in examples['examples'] if x['type'] in
                                ('ReferenceManifest', 'ReferenceRow[]', 'RegistryEntry', 'AuditReport')]
        self.assertGreater(len(examples['examples']), 0)
        self.assertEqual(self.wire(self.scratch, examples).returncode, 0)
        registry = json.loads(sealed('REGISTRIES.json'))
        resolver = next(x for x in registry['reader_registry'] if x['id'] == 'state-resolver')
        self.assertEqual(resolver['check_ids'], ['C-REFERENCES'])
        root = self.miniature()
        manifest = self.reference_manifest(root, [])
        registry_path = Path(manifest['registries']['path'])
        registry_path.write_bytes(encoded(registry))
        manifest['registries'] = binding(registry_path)
        path = put(root, 'manifest.json', encoded(manifest))
        value = self.result(self.cli(root, 'code/state/icm21_check.py', 'references',
                                    '--root', root, '--manifest', path), 2)
        ids = [x['registry_id'] for x in value['readers']]
        self.assertEqual(ids, sorted(ids))
        self.assertEqual(len(ids), len(set(ids)))
        expected = {x['id']: x['check_ids'] for x in registry['reader_registry']}
        for row in value['readers']:
            self.assertIn(row['registry_id'], expected)
            self.assertEqual([x['id'] for x in row['checks']], expected[row['registry_id']])
        self.assertTrue(any(check['status'] == 'UNVERIFIED'
                            for row in value['readers'] for check in row['checks']))

    @unittest.skip('ICM v2.1 open ticket: not built yet')
    def test_candidate_registry_adapter(self):
        self.require_file('code/state/icm21_check.py', 'candidate registry adapter integration')
        candidate = self.require_file('plans/icm21/specs/REGISTRIES.json', 'candidate registry')
        registry = json.loads(candidate.read_bytes())
        original = json.loads(sealed('REGISTRIES.json'))
        for collection in ('reader_registry', 'loader_registry'):
            old = {row['id']: row for row in original[collection]}
            new = {row['id']: row for row in registry[collection]}
            self.assertEqual(set(new), set(old))
            self.assertEqual(len(new), len(registry[collection]))
            for key in old:
                self.assertEqual(new[key]['check_ids'], old[key]['check_ids'])
        entry = next(row for row in registry['reader_registry'] if row['id'] == 'labviz-context')
        self.assertEqual(entry['adapter_argv'], ['.venv/bin/python', '-B', '-m', 'unittest',
                                                 'test_icm21.ReaderControls'])
        self.assertNotIn('code.tests', ' '.join(entry['adapter_argv']))
        self.assertEqual(registry['dispatcher'], original['dispatcher'])
