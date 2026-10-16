"""Checker seams: icm21_check.py routes new areas to sibling modules (plan Step 9).

Each case runs a copy of the checker in a scratch directory, so an area module
is present or absent by construction. The copy loads without any sys.path patch:
areas must be found by file path beside icm21_check.py.
"""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


STATE = Path(__file__).resolve().parent
SEAMS = ('icm21_audit_root', 'icm21_audit_views', 'icm21_audit_model',
         'icm21_audit_handoff', 'icm21_references', 'icm21_labviz_wire')
AREAS = {'C-ROOT': 'icm21_audit_root', 'C-WORKTREE': 'icm21_audit_root',
         'C-GENERATED': 'icm21_audit_views', 'C-TWINS': 'icm21_audit_views',
         'C-MODEL': 'icm21_audit_model', 'C-HANDOFF': 'icm21_audit_handoff'}
AUDIT_AREA = '''
FAIL = ()
def check(check_id, root, mode, config, coverage):
    coverage['inspected'].append(str(root))
    if check_id in FAIL:
        finding = {'id': 'F-FIXTURE-' + check_id, 'status': 'FAIL', 'prd_ids': ['ICM-R12'],
                   'paths': [str(root)], 'evidence': [], 'reason': 'fixture violation',
                   'previous_finding': None, 'resolution_receipt': None}
        return 'FAIL', __name__ + ' ' + check_id + ' ' + mode, [finding]
    return 'PASS', __name__ + ' ' + check_id + ' ' + mode, []
'''
REFERENCES_AREA = '''
def check_references(root, manifest):
    return {'schema_version': 1, 'readers': [{'registry_id': 'fixture-reader', 'checks': [
        {'id': 'C-REFERENCES', 'status': manifest['status'], 'prd_ids': ['ICM-R6'],
         'argv': [], 'exit_code': None, 'stdout_sha256': None, 'stderr_sha256': None,
         'findings': [], 'reason': __name__ + ' ' + str(root)}]}]}
'''
LABVIZ_AREA = '''
from pathlib import Path
def validate_labviz_moves(value, schema, fixtures, root):
    if not (Path(root) / 'labviz-marker').is_file() or value.get('bad'):
        raise ValueError(__name__ + ' rejected')
'''
EXPLODING_AREA = '''
from pathlib import Path
Path(__file__).with_suffix('.imported').touch()
raise ImportError('loaded ' + __name__)
'''


def digest(data):
    return hashlib.sha256(data).hexdigest()


class CheckerSeams(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix='icm21-seams-')
        self.addCleanup(temporary.cleanup)
        self.scratch = Path(os.path.realpath(temporary.name))
        self.schema = json.loads((STATE / 'icm21/WIRE-SCHEMAS.json').read_bytes())
        self.examples = json.loads((STATE / 'icm21/WIRE-EXAMPLES.json').read_bytes())

    def checker(self, areas):
        state = self.scratch / 'state'
        (state / 'icm21').mkdir(parents=True)
        shutil.copy(STATE / 'icm21_check.py', state)
        shutil.copy(STATE / 'icm21/WIRE-SCHEMAS.json', state / 'icm21')
        for name, source in areas.items():
            (state / (name + '.py')).write_text(source, encoding='utf-8')
        spec = importlib.util.spec_from_file_location('icm21_check', state / 'icm21_check.py')
        module = importlib.util.module_from_spec(spec)
        before = set(sys.modules)
        spec.loader.exec_module(module)
        self.assertEqual({name for name in set(sys.modules) - before if name in SEAMS}, set())
        return module

    def cli(self, module, *args):
        result = subprocess.run([sys.executable, '-B', module.__file__, *map(str, args)],
                                capture_output=True, timeout=30, cwd=self.scratch)
        return result.returncode, json.loads(result.stdout)

    def config(self, required):
        root = self.scratch / 'root'
        root.mkdir()

        def bind(name, data=b'{}'):
            path = root / name
            path.write_bytes(data)
            return {'path': str(path), 'sha256': digest(data)}

        for name in ('source', 'preserved', 'lanes', 'tools'):
            (self.scratch / name).mkdir()
        return root, {'schema_version': 1, 'canonical_root': str(root),
                      'source_roots': [str(self.scratch / 'source')],
                      'preservation_root': str(self.scratch / 'preserved'),
                      'worktree_root': str(self.scratch / 'lanes'),
                      'tool_root': str(self.scratch / 'tools'),
                      'ownership_path': bind('ownership.tsv',
                                             b'phase\tlane\tpath\tscope\tprd_ids\n'),
                      'registries': bind('registries.json'),
                      'references': bind('references.json'),
                      'retention': bind('retention.json'),
                      'required_checks': list(required), 'nightly_utc': '02:00:00Z',
                      'migration_holds': []}

    def results(self, report):
        return {row['id']: row for row in report['check_results']}

    def test_audit_routes_each_check_to_its_area(self):
        module = self.checker({name: AUDIT_AREA for name in set(AREAS.values())})
        root, config = self.config(AREAS)
        for mode in ('session', 'nightly'):
            report = module.audit(root, mode, config)
            module.validate_wire('AuditReport', report, self.schema, {})
            rows = self.results(report)
            self.assertEqual(set(rows), set(AREAS))
            for check_id, name in AREAS.items():
                self.assertEqual(rows[check_id]['status'], 'PASS')
                self.assertEqual(rows[check_id]['reason'], name + ' ' + check_id + ' ' + mode)
            self.assertEqual(report['overall_status'], 'PASS')
            self.assertIn(str(root), report['coverage']['inspected'])

    def test_audit_area_findings_join_the_report(self):
        areas = {name: AUDIT_AREA for name in set(AREAS.values())}
        areas['icm21_audit_model'] = AUDIT_AREA.replace('FAIL = ()', "FAIL = ('C-MODEL',)")
        module = self.checker(areas)
        root, config = self.config(['C-MODEL', 'C-HANDOFF'])
        report = module.audit(root, 'session', config)
        rows = self.results(report)
        self.assertEqual(rows['C-MODEL']['status'], 'FAIL')
        self.assertEqual(rows['C-MODEL']['findings'], ['F-FIXTURE-C-MODEL'])
        self.assertEqual([f['id'] for f in report['findings']], ['F-FIXTURE-C-MODEL'])
        self.assertEqual(rows['C-HANDOFF']['status'], 'PASS')
        self.assertEqual(report['overall_status'], 'FAIL')

    def test_absent_area_is_unverified_never_pass(self):
        module = self.checker({})
        root, config = self.config(AREAS)
        report = module.audit(root, 'session', config)
        module.validate_wire('AuditReport', report, self.schema, {})
        rows = self.results(report)
        self.assertEqual(set(rows), set(AREAS))
        for check_id, name in AREAS.items():
            self.assertEqual(rows[check_id]['status'], 'UNVERIFIED')
            self.assertIn(name, rows[check_id]['reason'])
        self.assertEqual(report['overall_status'], 'UNVERIFIED')

    def test_area_raising_the_checker_unverified_is_unverified(self):
        areas = {name: AUDIT_AREA for name in set(AREAS.values())}
        areas['icm21_audit_model'] = AUDIT_AREA + (
            "def check(check_id, root, mode, config, coverage):\n"
            "    raise Unverified('fixture cannot verify ' + check_id)\n")
        module = self.checker(areas)
        root, config = self.config(['C-MODEL', 'C-HANDOFF'])
        report = module.audit(root, 'session', config)
        module.validate_wire('AuditReport', report, self.schema, {})
        rows = self.results(report)
        self.assertEqual((rows['C-MODEL']['status'], rows['C-MODEL']['reason']),
                         ('UNVERIFIED', 'fixture cannot verify C-MODEL'))
        self.assertEqual(rows['C-HANDOFF']['status'], 'PASS')
        self.assertEqual(report['overall_status'], 'UNVERIFIED')

    def test_one_absent_area_keeps_the_report_unverified(self):
        present = {name: AUDIT_AREA for name in set(AREAS.values()) if name != 'icm21_audit_views'}
        module = self.checker(present)
        root, config = self.config(AREAS)
        report = module.audit(root, 'session', config)
        rows = self.results(report)
        for check_id, name in AREAS.items():
            self.assertEqual(rows[check_id]['status'],
                             'UNVERIFIED' if name == 'icm21_audit_views' else 'PASS')
        self.assertEqual(report['overall_status'], 'UNVERIFIED')

    def test_references_delegate(self):
        module = self.checker({'icm21_references': REFERENCES_AREA})
        root = self.scratch / 'root'
        root.mkdir()
        value = module.check_references(root, {'status': 'PASS'})
        self.assertEqual(value['readers'][0]['checks'][0]['reason'],
                         'icm21_references ' + str(root))
        for status, exit_code in (('PASS', 0), ('FAIL', 1), ('UNVERIFIED', 2)):
            manifest = self.scratch / (status + '.json')
            manifest.write_text(json.dumps({'status': status}), encoding='utf-8')
            code, value = self.cli(module, 'references', '--root', root, '--manifest', manifest)
            self.assertEqual(code, exit_code, value)
            self.assertEqual(value['readers'][0]['checks'][0]['status'], status)

    def references_cli(self, source):
        module = self.checker({'icm21_references': source})
        root = self.scratch / 'root'
        root.mkdir()
        manifest = self.scratch / 'manifest.json'
        manifest.write_text('{}', encoding='utf-8')
        return self.cli(module, 'references', '--root', root, '--manifest', manifest)

    def test_references_without_readers_is_unverified(self):
        code, value = self.references_cli(
            "def check_references(root, manifest):\n"
            "    return {'schema_version': 1, 'readers': []}\n")
        self.assertEqual((code, value), (2, {'schema_version': 1, 'readers': []}))

    def test_references_out_of_order_readers_fail(self):
        code, value = self.references_cli('''
def check_references(root, manifest):
    return {'schema_version': 1, 'readers': [{'registry_id': reader, 'checks': [
        {'id': 'C-REFERENCES', 'status': 'PASS', 'prd_ids': ['ICM-R6'], 'argv': [],
         'exit_code': None, 'stdout_sha256': None, 'stderr_sha256': None,
         'findings': [], 'reason': 'fixture'}]} for reader in ('z', 'a')]}
''')
        self.assertEqual((code, value), (1, {'reason': 'reader results not in ID order',
                                             'status': 'FAIL'}))

    def test_absent_references_is_unverified(self):
        module = self.checker({})
        root = self.scratch / 'root'
        root.mkdir()
        with self.assertRaises(module.Unverified):
            module.check_references(root, {'status': 'PASS'})
        manifest = self.scratch / 'manifest.json'
        manifest.write_text(json.dumps({'status': 'PASS'}), encoding='utf-8')
        code, value = self.cli(module, 'references', '--root', root, '--manifest', manifest)
        self.assertEqual((code, value['status']), (2, 'UNVERIFIED'))
        self.assertIn('icm21_references', value['reason'])

    def labviz_examples(self, expected, value=None):
        example = next(x for x in self.examples['examples'] if x['type'] == 'LabvizMoves')
        example = dict(example, expected=expected)
        if value is not None:
            example['value'] = value
        path = self.scratch / ('labviz-' + expected + '.json')
        path.write_text(json.dumps({'schema_version': 1, 'fixtures': {},
                                    'examples': [example]}), encoding='utf-8')
        return path

    def wire(self, module, examples):
        root = self.scratch / 'wire-root'
        root.mkdir(exist_ok=True)
        return self.cli(module, 'wire', '--root', root, '--schema',
                        STATE / 'icm21/WIRE-SCHEMAS.json', '--examples', examples)

    def test_labviz_moves_delegate(self):
        module = self.checker({'icm21_labviz_wire': LABVIZ_AREA})
        code, value = self.wire(module, self.labviz_examples('PASS'))
        self.assertEqual((code, value['status']), (1, 'FAIL'))
        self.assertEqual(value['results'][0]['reason'], 'icm21_labviz_wire rejected')
        (self.scratch / 'wire-root/labviz-marker').write_bytes(b'')
        code, value = self.wire(module, self.labviz_examples('PASS'))
        self.assertEqual((code, value['status']), (0, 'PASS'))
        code, value = self.wire(module, self.labviz_examples('FAIL', {'bad': True}))
        self.assertEqual((code, value['status']), (0, 'PASS'))

    def test_labviz_moves_rejects_pre_d2_sealed_positive(self):
        source = (STATE / 'icm21_labviz_wire.py').read_text(encoding='utf-8')
        module = self.checker({'icm21_labviz_wire': source})
        example = next(x for x in self.examples['examples']
                       if x['type'] == 'LabvizMoves' and x['expected'] == 'PASS')
        with self.assertRaisesRegex(ValueError, 'not the D2 identity'):
            module.validate_wire('LabvizMoves', example['value'], self.schema, {},
                                 self.scratch)
        code, value = self.wire(module, self.labviz_examples('PASS'))
        self.assertEqual((code, value['status']), (1, 'FAIL'))
        self.assertEqual([(x['expected'], x['observed']) for x in value['results']],
                         [('PASS', 'FAIL')])
        self.assertIn('not the D2 identity', value['results'][0]['reason'])

    def test_sealed_negative_labviz_example_alone_passes_as_observed_fail(self):
        source = (STATE / 'icm21_labviz_wire.py').read_text(encoding='utf-8')
        module = self.checker({'icm21_labviz_wire': source})
        negative = [x for x in self.examples['examples']
                    if x['id'] == 'labviz-map-input-binding-invalid']
        self.assertEqual([x['expected'] for x in negative], ['FAIL'])
        path = self.scratch / 'labviz-negative.json'
        path.write_text(json.dumps(dict(self.examples, examples=negative)), encoding='utf-8')
        code, value = self.wire(module, path)
        self.assertEqual((code, value['status']), (0, 'PASS'))
        self.assertEqual([(x['id'], x['expected'], x['observed']) for x in value['results']],
                         [('labviz-map-input-binding-invalid', 'FAIL', 'FAIL')])

    def test_absent_labviz_seam_is_unverified_never_pass(self):
        module = self.checker({})
        for expected in ('PASS', 'FAIL'):
            code, value = self.wire(module, self.labviz_examples(expected))
            self.assertEqual((code, value['status']), (2, 'UNVERIFIED'))
            self.assertIn('icm21_labviz_wire', value['reason'])
        with self.assertRaises(module.Unverified):
            module.validate_wire('LabvizMoves', {}, self.schema, {}, self.scratch)

    def test_other_paths_import_no_area_module(self):
        module = self.checker({name: EXPLODING_AREA for name in SEAMS})
        approved = [x for x in self.examples['examples'] if x['type'] in ('Finding', 'Config')]
        self.assertTrue(approved)
        path = self.scratch / 'approved.json'
        path.write_text(json.dumps(dict(self.examples, examples=approved)), encoding='utf-8')
        code, value = self.wire(module, path)
        self.assertEqual((code, value['status']), (0, 'PASS'))
        root, config = self.config(['C-LANES'])
        report = module.audit(root, 'session', config)
        self.assertEqual(self.results(report)['C-LANES']['status'], 'PASS')
        self.assertEqual(sorted(path.name for path in self.scratch.rglob('*.imported')), [])


if __name__ == '__main__':
    unittest.main()
