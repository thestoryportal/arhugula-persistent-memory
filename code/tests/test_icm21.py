"""Frozen ICM v2.1 fixture interface (T004; product acceptance is separate).

Sources: sealed COMMAND-DERIVATION.md, SPEC.md and IMPLEMENTATION_PLAN.md D1/D2.
Fixtures contain miniature data only. No operational client, model or loader runs.
"""
import copy
import json
from pathlib import Path
import unittest

# BASE, binding, snapshot and the rest stay importable here for test_context_audit.
from icm21_fixtures import (BASE, D2_POSITIVE, HEADER, INDEX_PATHS, MAP_PATH, SOURCE_ROOT,
                            FixtureCase, binding, d2_map, digest, encoded, put, sealed, snapshot)
from icm21_staged_cases import StagedCases
from icm21_case_labviz_map import CurrentLabvizOutputCase, GeneratorScopeCase
from icm21_guard_cases import GuardCases
from icm21_reader_cases_a import ReaderCasesA
from icm21_reader_cases_b import ReaderCasesB


SELECTED = {
    'GuardControls': ('test_admission_shapes', 'test_bounded_runner',
                      'test_create_recheck', 'test_fault_denial',
                      'test_unsupported_sandbox_denial'),
    'StagedControls': ('test_ci_bypass', 'test_generator_scope', 'test_real_hook',
                       'test_source_output_closure'),
    'ReaderControls': ('test_candidate_registry_adapter', 'test_current_index_outputs',
                       'test_current_labviz_output', 'test_d2_wire_parser',
                       'test_dispatch_coverage_and_ownership',
                       'test_exact_relocation_and_citations',
                       'test_labviz_adapter_identity', 'test_portable_map_identity',
                       'test_queue_compatibility_and_candidates',
                       'test_relocated_anchor_targets'),
    'ApprovedWireControls': ('test_approved_scope_examples',),
}


class ApprovedWireControls(FixtureCase):
    def test_approved_scope_examples(self):
        self.require_file('code/state/icm21_check.py', 'validated common wire types')
        examples = json.loads(sealed('WIRE-EXAMPLES.json'))
        approved = {'Finding', 'CheckResult', 'RegistryEntry', 'Registries', 'Config',
                    'ReferenceRow', 'ReferenceRow[]', 'ReferenceManifest', 'Repair',
                    'ApprovedRequests', 'Admit', 'AuditReport'}
        examples['examples'] = [x for x in examples['examples'] if x['type'] in approved]
        self.assertGreater(len(examples['examples']), 0)
        self.assertNotIn('LabvizMoves', {x['type'] for x in examples['examples']})
        result = self.result(self.wire(self.scratch, examples), 0)
        self.assertEqual(result['status'], 'PASS')
        for type_name, change in (
                ('Finding', lambda v: v.update(extra=True)),
                ('Finding', lambda v: v.update(prd_ids=['ICM-R99'])),
                ('Admit', lambda v: v['request'].update(schema_version=True)),
                ('RegistryEntry', lambda v: v.update(check_ids=['UNKNOWN']))):
            with self.subTest(type=type_name):
                candidate = copy.deepcopy(next(x for x in examples['examples']
                                               if x['type'] == type_name and x['expected'] == 'PASS'))
                change(candidate['value'])
                probe = copy.deepcopy(examples)
                probe['examples'] = [candidate]
                self.assertEqual(self.wire(self.scratch, probe).returncode, 1,
                                 'wire parser accepted invalid ' + type_name)


class GuardControls(GuardCases, FixtureCase):
    pass


class StagedControls(StagedCases, GeneratorScopeCase, FixtureCase):
    pass


class ReaderControls(ReaderCasesA, ReaderCasesB, CurrentLabvizOutputCase, FixtureCase):
    pass


class FixtureContractControls(unittest.TestCase):
    def test_complete_collection(self):
        loader = unittest.TestLoader()
        for name, methods in SELECTED.items():
            cls = globals()[name]
            self.assertTrue(issubclass(cls, unittest.TestCase))
            self.assertEqual(set(loader.getTestCaseNames(cls)), set(methods))
            self.assertEqual(loader.loadTestsFromTestCase(cls).countTestCases(), len(methods))

    def test_d2_complete_input_identity(self):
        self.assertEqual(set(D2_POSITIVE), {'inputs', 'map'})
        self.assertEqual(set(D2_POSITIVE['inputs']), {'_index/path-map.tsv', '_index/icm21-path-map.tsv'})
        self.assertTrue(all(isinstance(value, bytes) for value in D2_POSITIVE['inputs'].values()))
        self.assertEqual(D2_POSITIVE['map'], d2_map(D2_POSITIVE['inputs'], {}))
        self.assertFalse(D2_POSITIVE['map'].endswith(b'\n'))
        for key in ('sealed', 'relocations'):
            self.assertFalse(Path(json.loads(D2_POSITIVE['map'])['derived_from'][key]['path']).is_absolute())

    def test_sealed_interface_definition(self):
        definitions = json.loads(sealed('foundation-specs.json'))['T004']
        self.assertEqual(definitions['subject'], 'code/tests/test_icm21.py')
        self.assertEqual(definitions['contract'], type(self).__name__)
        for name, methods in definitions['required'].items():
            self.assertTrue(set(methods) <= set(SELECTED[name]))


if __name__ == '__main__':
    unittest.main()
