"""ReaderControls dispatch-coverage and ownership case."""
import json
from pathlib import Path
import unittest

from icm21_fixtures import binding, encoded, put, sealed


class DispatchCoverageCase:
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
