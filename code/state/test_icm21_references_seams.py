"""Reference dispatcher seams: icm21_references.py checks what each owned row and reader claims
(T016 review findings 1-6). Small manifests are bound in a scratch root. Adapter runs are mocked."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch


STATE = Path(__file__).resolve().parent


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode('utf-8')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def put(root, relative, data):
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data if isinstance(data, bytes) else data.encode('utf-8'))
    return path


def snapshot(root):
    return {str(p.relative_to(root)): (p.lstat().st_mtime_ns, digest(p.read_bytes()))
            for p in root.rglob('*') if p.is_file()}


def load(name):
    """A state module loaded by path, as icm21_check loads its areas."""
    spec = importlib.util.spec_from_file_location(name, STATE / (name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def reader_entry(id='reader', path='consumer.md', check='C-REFERENCES', argv=None):
    return {'id': id, 'path': path, 'role': 'reader', 'owner': 'integration',
            'source_sha256': None, 'adapter_argv': argv, 'check_ids': [check],
            'status': 'SPECIFIED', 'hold_id': None}


def reference_row(role='historical-source', final_target='target.md'):
    return {'schema_version': 1, 'id': 'REF-1', 'prd_ids': ['ICM-R6'], 'consumer': 'consumer.md',
            'consumer_sha256': '0' * 64, 'consumer_final': 'consumer.md', 'reference': 'target.md',
            'intermediate': 'target.md', 'final_target': final_target, 'role': role,
            'byte_offset': None, 'owner': 'integration', 'check_id': 'C-REFERENCES',
            'repair_path': 'consumer.md' if role == 'current-reader' else None}


def operation(root, operation_id='PLAN-1', plan_sha256='1' * 64):
    return {'operation_id': operation_id, 'prd_ids': ['ICM-R6'],
            'plan': {'path': str(root / 'plan.json'), 'sha256': plan_sha256},
            'approval': {'path': str(root / 'approval.json'), 'sha256': '2' * 64},
            'journal': {'path': str(root / 'journal.json'), 'sha256': '3' * 64},
            'verification': None, 'readers': None, 'acceptance': None, 'rollback': None}


def repair(root, id='REPAIR-1', reference_id='REF-1', reader_id='reader', plan_id='PLAN-1'):
    source = str(root / 'consumer.md')
    return {'schema_version': 1, 'id': id, 'prd_ids': ['ICM-R6'], 'plan_id': plan_id,
            'plan_sha256': '1' * 64, 'source': source, 'target': source,
            'before_sha256': '0' * 64, 'after_sha256': '0' * 64, 'edits': [],
            'reader_ids': [reader_id], 'reference_ids': [reference_id]}


class ReferenceSeams(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix='icm21-references-')
        self.addCleanup(temporary.cleanup)
        self.root = Path(os.path.realpath(temporary.name)) / 'root'
        self.root.mkdir()
        put(self.root, 'consumer.md', 'see target.md\n')
        put(self.root, 'target.md', '# Present\n\nline three\n')

    def manifest(self, readers, rows=(), repairs=(), operations=(), required=None, changes=None):
        """A bound ReferenceManifest beside small inputs; changes(values) may corrupt one input."""
        values = {'registries': {'schema_version': 1, 'dispatcher': ['checker'],
                                 'reader_registry': list(readers), 'loader_registry': []},
                  'references': list(rows),
                  'repairs': {'schema_version': 1, 'repairs': list(repairs)},
                  'executor': {'schema_version': 1, 'operations': list(operations)},
                  'coverage': {'schema_version': 1, 'scope': 'fixture', 'sources': [],
                               'coverage': {'inspected': [str(self.root)], 'excluded': [],
                                            'required_registry_ids': [x['id'] for x in readers]
                                            if required is None else required,
                                            'checked_registry_ids': []}}}
        if changes is not None:
            changes(values)
        manifest = {'schema_version': 1}
        for key, value in values.items():
            data = (b''.join(encoded(x) + b'\n' for x in value) if key == 'references'
                    else encoded(value))
            path = put(self.root, key + '.json', data)
            manifest[key] = {'path': str(path), 'sha256': digest(data)}
        return manifest

    def checked(self, manifest):
        """Statuses through icm21_check's seam, which validates the ReferenceResults."""
        value = load('icm21_check').check_references(self.root, manifest)
        return {(x['registry_id'], c['id']): c['status'] for x in value['readers'] for c in x['checks']}

    def test_target_and_anchor_resolve(self):
        for target, expected in (('missing.md', 'FAIL'), ('target.md#absent', 'FAIL'),
                                 ('missing.md#present', 'FAIL'), ('target.md:2-9', 'FAIL'),
                                 ('target.md', 'PASS'), ('target.md#present', 'PASS'),
                                 ('target.md:1–3', 'PASS'), ('target.md:3,1', 'PASS')):
            with self.subTest(target=target):
                manifest = self.manifest([reader_entry()], [reference_row(final_target=target)])
                self.assertEqual(self.checked(manifest), {('reader', 'C-REFERENCES'): expected})

    def test_line_anchors_use_line_count(self):
        for target, expected in (('target.md#L2', 'PASS'), ('target.md#L1-L3', 'PASS'),
                                 ('target.md#L4', 'FAIL'), ('target.md#L2-L9', 'FAIL'),
                                 ('missing.md#L1', 'FAIL')):
            with self.subTest(target=target):
                manifest = self.manifest([reader_entry()], [reference_row(final_target=target)])
                self.assertEqual(self.checked(manifest), {('reader', 'C-REFERENCES'): expected})

    def test_queue_items_resolve(self):
        (self.root / 'projects/real').mkdir(parents=True)
        queue = reader_entry('queue-locators', 'program/program_state.json', 'C-QUEUE')
        for artifact, expected in (({'kind': 'nonsense', 'path': 'projects/real'}, 'FAIL'),
                                   ({'kind': 'project', 'path': 'projects/absent'}, 'FAIL'),
                                   ({'kind': 'project', 'path': 'projects/real'}, 'PASS'),
                                   (None, 'PASS')):
            with self.subTest(artifact=artifact):
                put(self.root, 'program/program_state.json', encoded(
                    {'work_queue': {'items': [{'id': 'q1', 'state': 'open', 'artifact': artifact}]}}))
                self.assertEqual(self.checked(self.manifest([queue])),
                                 {('queue-locators', 'C-QUEUE'): expected})

    def test_exact_admitted_repair(self):
        row = reference_row('current-reader')
        operation = {'operation_id': 'PLAN-1', 'prd_ids': ['ICM-R6'],
                     'plan': {'path': str(self.root / 'plan.json'), 'sha256': '1' * 64},
                     'approval': {'path': str(self.root / 'approval.json'), 'sha256': '2' * 64},
                     'journal': {'path': str(self.root / 'journal.json'), 'sha256': '3' * 64},
                     'verification': None, 'readers': None, 'acceptance': None, 'rollback': None}
        exact = str(self.root / 'consumer.md')
        for source, plan, expected in (('/unrelated/source.md', ('PLAN-1', '1' * 64), 'FAIL'),
                                       (exact, ('unadmitted', '0' * 64), 'UNVERIFIED'),
                                       (exact, ('PLAN-1', '0' * 64), 'UNVERIFIED'),
                                       (exact, ('PLAN-1', '1' * 64), 'PASS')):
            with self.subTest(source=source, plan=plan):
                repair = {'schema_version': 1, 'id': 'REPAIR-1', 'prd_ids': ['ICM-R6'],
                          'plan_id': plan[0], 'plan_sha256': plan[1], 'source': source,
                          'target': source, 'before_sha256': '0' * 64, 'after_sha256': '0' * 64,
                          'edits': [], 'reader_ids': ['reader'], 'reference_ids': ['REF-1']}
                manifest = self.manifest([reader_entry()], [row], [repair], [operation])
                self.assertEqual(self.checked(manifest), {('reader', 'C-REFERENCES'): expected})

    def test_bound_inputs_are_wire_valid(self):
        corruptions = {
            'registries': lambda v: v['registries']['reader_registry'][0].update(status='GARBAGE'),
            'references': lambda v: v['references'][0].update(extra=True),
            'repairs': lambda v: v['repairs'].update(extra=True),
            'coverage': lambda v: v['coverage'].update(schema_version=2)}
        for key, change in corruptions.items():
            with self.subTest(input=key):
                manifest = self.manifest([reader_entry()], [reference_row()], changes=change)
                with self.assertRaises(ValueError):
                    self.checked(manifest)
        manifest = self.manifest([reader_entry()], [reference_row()])
        self.assertEqual(self.checked(manifest), {('reader', 'C-REFERENCES'): 'PASS'})

    def test_missing_required_is_unverified(self):
        manifest = self.manifest([reader_entry()], [reference_row()],
                                 required=['missing-required', 'reader'])
        value = load('icm21_check').check_references(self.root, manifest)
        self.assertEqual([x['registry_id'] for x in value['readers']], ['missing-required', 'reader'])
        missing = value['readers'][0]['checks']
        self.assertEqual(len(missing), 1)
        self.assertEqual(missing[0]['status'], 'UNVERIFIED')
        self.assertEqual(value['readers'][1]['checks'][0]['status'], 'PASS')

    def adapter_runs(self, module, readers, output=b'Ran 1 test in 0.001s\n\nOK\n'):
        """(results or the ValueError, argv of every subprocess call) of one dispatch."""
        put(self.root, module.PYTHON, b'')
        for entry in readers:
            if not (self.root / entry['path']).exists():
                put(self.root, entry['path'], b'')
        seen = []

        def process(argv, **options):
            seen.append(argv)
            return subprocess.CompletedProcess(argv, 0, b'', output)
        with patch.object(module.subprocess, 'run', side_effect=process):
            try:
                return module.check_references(self.root, self.manifest(readers)), seen
            except ValueError as error:
                return error, seen

    def test_conflict_refused_before_execution(self):
        module = load('icm21_references')
        aliases = [list(argv) for argv, kind in module.ADAPTERS.items() if kind == 'unittest']
        self.assertEqual(len(aliases), 2)
        result, seen = self.adapter_runs(module, [reader_entry('a', 'a.py', 'C-LABVIZ', aliases[0]),
                                                  reader_entry('b', 'b.py', 'C-LABVIZ', aliases[1])])
        self.assertIsInstance(result, ValueError)
        self.assertEqual(seen, [])

    def test_aliases_run_one_adapter(self):
        module = load('icm21_references')
        aliases = [list(argv) for argv, kind in module.ADAPTERS.items() if kind == 'unittest']
        result, seen = self.adapter_runs(module, [
            reader_entry('a', 'a.py', 'C-LABVIZ', aliases[0]),
            reader_entry('b', 'b.py', 'C-REFERENCES', aliases[1])])
        self.assertEqual(len(seen), 1)
        checks = [reader['checks'][0] for reader in result['readers']]
        self.assertEqual([check['status'] for check in checks], ['PASS', 'PASS'])
        self.assertEqual(len({(check['stdout_sha256'], check['stderr_sha256']) for check in checks}), 1)

    def test_final_summary_decides(self):
        module = load('icm21_references')
        put(self.root, module.PYTHON, b'')
        argv = next(argv for argv, kind in module.ADAPTERS.items() if kind == 'unittest')
        for output, expected in ((b'Ran 1 test in 0.001s\n\nRan 0 tests in 0.001s\n\nOK\n', 'UNVERIFIED'),
                                 (b'Ran 0 tests in 0.001s\n\nOK\n', 'UNVERIFIED'),
                                 (b'Ran 2 tests in 0.001s\n\nOK (skipped=1)\n', 'UNVERIFIED'),
                                 (b'Ran 0 tests in 0.001s\n\nRan 2 tests in 0.001s\n\nOK\n', 'PASS')):
            with self.subTest(output=output):
                with patch.object(module.subprocess, 'run', return_value=subprocess.CompletedProcess(
                        list(argv), 0, b'', output)):
                    self.assertEqual(module.run_adapter(self.root, argv)[0], expected)

    def test_complete_outputs_exposed(self):
        module = load('icm21_references')
        self.assertTrue(callable(getattr(module, 'dispatch', None)), 'absent behavior: dispatch')
        argv = next(argv for argv, kind in module.ADAPTERS.items() if kind == 'index')
        manifest = self.manifest([reader_entry('index', 'index.py', 'C-GENERATED', list(argv))])
        put(self.root, module.PYTHON, b'')
        put(self.root, 'index.py', b'')
        stdout, stderr = b'scanned 3 files\nINDEX CLEAN\n', b'note: complete stderr\n'
        before = snapshot(self.root)
        with patch.object(module.subprocess, 'run', return_value=subprocess.CompletedProcess(
                list(argv), 0, stdout, stderr)):
            results, outputs = module.dispatch(self.root, manifest)
            self.assertEqual(module.check_references(self.root, manifest), results)
        self.assertEqual(snapshot(self.root), before)
        self.assertEqual(set(results), {'schema_version', 'readers'})
        check = results['readers'][0]['checks'][0]
        self.assertEqual(check['status'], 'PASS')
        self.assertEqual(outputs[check['stdout_sha256']], stdout)
        self.assertEqual(outputs[check['stderr_sha256']], stderr)
        for key, data in outputs.items():
            self.assertEqual(key, digest(data))

    # Round 2 finding 1: every ReaderControls alias dispatches the spelling that loads.
    def test_reader_controls_alias_dispatches_loadable_name(self):
        module = load('icm21_references')
        aliases = [list(argv) for argv, kind in module.ADAPTERS.items() if kind == 'unittest']
        self.assertEqual(len(aliases), 2)
        for alias in aliases:
            with self.subTest(alias=alias[-1]):
                result, seen = self.adapter_runs(module, [reader_entry('a', 'a.py', 'C-LABVIZ', alias)])
                self.assertEqual(len(seen), 1)
                self.assertEqual(seen[0][-1], 'test_icm21.ReaderControls')
                self.assertEqual(result['readers'][0]['checks'][0]['argv'], list(seen[0]))
                loader = unittest.TestLoader()
                suite = loader.loadTestsFromName(seen[0][-1])
                self.assertGreater(suite.countTestCases(), 0)
                self.assertEqual(loader.errors, [])

    def mocked(self, module, manifest, stdout=b'', stderr=b'', code=0):
        """(check statuses or the ValueError, argv of every subprocess call) of one dispatch."""
        put(self.root, module.PYTHON, b'')
        seen = []

        def process(argv, **options):
            seen.append(argv)
            return subprocess.CompletedProcess(argv, code, stdout, stderr)
        with patch.object(module.subprocess, 'run', side_effect=process):
            try:
                value = module.check_references(self.root, manifest)
            except ValueError as error:
                return error, seen
        return {(x['registry_id'], c['id']): c['status']
                for x in value['readers'] for c in x['checks']}, seen

    # Round 2 finding 2: C-LABVIZ needs a unittest result, C-GENERATED an index result.
    def test_consuming_checks_need_their_adapter_kind(self):
        module = load('icm21_references')
        index = list(next(argv for argv, kind in module.ADAPTERS.items() if kind == 'index'))
        unit = list(next(argv for argv, kind in module.ADAPTERS.items() if kind == 'unittest'))
        outputs = {'index': (b'INDEX CLEAN\n', b''), 'unit': (b'', b'Ran 1 test in 0.001s\n\nOK\n'),
                   None: (b'', b'')}
        for check, argv, output, expected in (
                ('C-LABVIZ', None, None, 'UNVERIFIED'), ('C-LABVIZ', index, 'index', 'UNVERIFIED'),
                ('C-LABVIZ', unit, 'unit', 'PASS'), ('C-GENERATED', None, None, 'UNVERIFIED'),
                ('C-GENERATED', unit, 'unit', 'UNVERIFIED'), ('C-GENERATED', index, 'index', 'PASS')):
            with self.subTest(check=check, argv=argv):
                row = dict(reference_row(), check_id=check)
                manifest = self.manifest([reader_entry(check=check, argv=argv)], [row])
                statuses, _ = self.mocked(module, manifest, *outputs[output])
                self.assertEqual(statuses, {('reader', check): expected})
        # A null-adapter reader consumes the producer's result of the required kind.
        manifest = self.manifest([reader_entry('labviz', 'labviz.py', 'C-LABVIZ', unit),
                                  reader_entry(check='C-LABVIZ')],
                                 [dict(reference_row(), check_id='C-LABVIZ')])
        put(self.root, 'labviz.py', b'')
        statuses, seen = self.mocked(module, manifest, *outputs['unit'])
        self.assertEqual(statuses, {('labviz', 'C-LABVIZ'): 'PASS', ('reader', 'C-LABVIZ'): 'PASS'})
        self.assertEqual(len(seen), 1)

    # Round 2 finding 3a: a SPECIFIED reader's own path is required.
    def test_required_reader_path_unreadable(self):
        locked = put(self.root, 'locked.md', 'see target.md\n')
        locked.chmod(0)
        self.addCleanup(locked.chmod, 0o644)
        self.assertFalse(os.access(locked, os.R_OK))
        for path, expected in (('absent.md', 'UNVERIFIED'), ('locked.md', 'UNVERIFIED'),
                               ('consumer.md', 'PASS')):
            with self.subTest(path=path):
                row = dict(reference_row(), consumer=path, consumer_final=path)
                manifest = self.manifest([reader_entry(path=path)], [row])
                self.assertEqual(self.checked(manifest), {('reader', 'C-REFERENCES'): expected})
        # An absolute (external) path is used as written; ReferenceRow consumers are relative,
        # so these readers carry the row-free C-QUEUE check.
        put(self.root, 'program/program_state.json', encoded({'work_queue': {'items': []}}))
        outside = put(self.root.parent, 'external.md', 'external\n')
        for path, expected in ((str(self.root.parent / 'absent.md'), 'UNVERIFIED'),
                               (str(outside), 'PASS')):
            with self.subTest(path=path):
                manifest = self.manifest([reader_entry(path=path, check='C-QUEUE')])
                self.assertEqual(self.checked(manifest), {('reader', 'C-QUEUE'): expected})

    # Round 2 finding 3b: an unreadable final target or resolver read is UNVERIFIED; absent is FAIL.
    def test_unreadable_target_is_unverified(self):
        locked = put(self.root, 'locked.md', '# Present\n')
        locked.chmod(0)
        self.addCleanup(locked.chmod, 0o644)
        for target, expected in (('locked.md#present', 'UNVERIFIED'), ('locked.md:1', 'UNVERIFIED'),
                                 ('absent.md#present', 'FAIL'), ('target.md#present', 'PASS')):
            with self.subTest(target=target):
                manifest = self.manifest([reader_entry()], [reference_row(final_target=target)])
                self.assertEqual(self.checked(manifest), {('reader', 'C-REFERENCES'): expected})
        module = load('icm21_references')
        real = module.sibling

        def sibling(name):
            loaded = real(name)
            if name == 'resolve_path':
                def denied(*arguments):
                    raise PermissionError('fixture: resolver read denied')
                loaded.resolve_reference = denied
            return loaded
        manifest = self.manifest([reader_entry()], [reference_row()])
        with patch.object(module, 'sibling', side_effect=sibling):
            value = module.check_references(self.root, manifest)
        self.assertEqual(value['readers'][0]['checks'][0]['status'], 'UNVERIFIED')

    # Round 3 finding 1: an unanchored final target is read too; a directory target is listed.
    def test_unreadable_unanchored_target_is_unverified(self):
        locked = put(self.root, 'locked.md', '# Present\n')
        locked.chmod(0)
        self.addCleanup(locked.chmod, 0o644)
        self.assertFalse(os.access(locked, os.R_OK))
        (self.root / 'folder').mkdir()
        for target, expected in (('locked.md', 'UNVERIFIED'), ('folder', 'PASS'),
                                 ('absent.md', 'FAIL')):
            with self.subTest(target=target):
                manifest = self.manifest([reader_entry()], [reference_row(final_target=target)])
                self.assertEqual(self.checked(manifest), {('reader', 'C-REFERENCES'): expected})

    # Round 2 finding 4, round 1 finding 1: M39, M41, M44, M45, M48.
    def test_target_boundaries(self):
        put(self.root.parent, 'outside.md', '# Present\n')
        (self.root / 'folder').mkdir()
        for target, expected in (('../outside.md', 'FAIL'), ('folder#present', 'FAIL'),
                                 ('folder', 'PASS'), ('target.md:0', 'FAIL'),
                                 ('target.md#L0', 'FAIL'), ('target.md:3-1', 'FAIL'),
                                 ('target.md#L3-L1', 'FAIL'), ('target.md:1-3', 'PASS')):
            with self.subTest(target=target):
                row = dict(reference_row(final_target=target), reference=target, intermediate=target)
                manifest = self.manifest([reader_entry()], [row])
                self.assertEqual(self.checked(manifest), {('reader', 'C-REFERENCES'): expected})

    def test_unreadable_queue_is_unverified(self):
        queue = reader_entry('queue-locators', 'consumer.md', 'C-QUEUE')
        self.assertFalse((self.root / 'program/program_state.json').exists())
        self.assertEqual(self.checked(self.manifest([queue])),
                         {('queue-locators', 'C-QUEUE'): 'UNVERIFIED'})
        put(self.root, 'program/program_state.json', encoded({'work_queue': {'items': []}}))
        self.assertEqual(self.checked(self.manifest([queue])), {('queue-locators', 'C-QUEUE'): 'PASS'})

    # Round 2 finding 4, round 1 finding 2: each mismatch changes one ID only (M50, M51, M54).
    def test_repair_reference_id_must_match(self):
        put(self.root, 'other.md', 'other\n')
        rows = [reference_row('current-reader'),
                dict(reference_row('current-reader', 'other.md'), id='REF-2',
                     reference='other.md', intermediate='other.md')]
        for first, expected in (('REF-1', 'PASS'), ('REF-2', 'UNVERIFIED')):
            with self.subTest(reference_id=first):
                repairs = [repair(self.root, 'REPAIR-1', first),
                           repair(self.root, 'REPAIR-2', 'REF-2')]
                manifest = self.manifest([reader_entry()], rows, repairs, [operation(self.root)])
                self.assertEqual(self.checked(manifest), {('reader', 'C-REFERENCES'): expected})

    def test_repair_reader_id_must_match(self):
        put(self.root, 'second.md', 'second\n')
        readers = [reader_entry(), reader_entry('reader-2', 'second.md')]
        for reader_id, expected in (('reader', 'PASS'), ('reader-2', 'UNVERIFIED')):
            with self.subTest(reader_id=reader_id):
                manifest = self.manifest(readers, [reference_row('current-reader')],
                                         [repair(self.root, reader_id=reader_id)],
                                         [operation(self.root)])
                self.assertEqual(self.checked(manifest)[('reader', 'C-REFERENCES')], expected)

    def test_repair_operation_id_must_match(self):
        for plan_id, expected in (('PLAN-1', 'PASS'), ('PLAN-2', 'UNVERIFIED')):
            with self.subTest(plan_id=plan_id):
                manifest = self.manifest([reader_entry()], [reference_row('current-reader')],
                                         [repair(self.root, plan_id=plan_id)], [operation(self.root)])
                self.assertEqual(self.checked(manifest), {('reader', 'C-REFERENCES'): expected})

    # Round 2 finding 4, WIRE-CONTRACTS.md:43: exit 0 alone does not decide (M05, M06).
    def test_exit_and_marker_decide_together(self):
        module = load('icm21_references')
        put(self.root, module.PYTHON, b'')
        index = next(argv for argv, kind in module.ADAPTERS.items() if kind == 'index')
        unit = next(argv for argv, kind in module.ADAPTERS.items() if kind == 'unittest')
        for argv, code, stdout, stderr, expected in (
                (index, 1, b'INDEX CLEAN\n', b'', 'FAIL'),
                (unit, 1, b'', b'Ran 2 tests in 0.001s\n\nOK\n', 'FAIL'),
                (index, 0, b'scanned 3 files\nINDEX DIRTY\n', b'', 'UNVERIFIED'),
                (index, 0, b'', b'', 'UNVERIFIED'),
                (index, 0, b'INDEX CLEAN\n', b'', 'PASS')):
            with self.subTest(argv=argv[-1], code=code, stdout=stdout):
                with patch.object(module.subprocess, 'run', return_value=subprocess.CompletedProcess(
                        list(argv), code, stdout, stderr)):
                    self.assertEqual(module.run_adapter(self.root, argv)[0], expected)

    # Round 2 finding 4, WIRE-CONTRACTS.md:71-72: held entries and unknown argv never run (M33, M35).
    def test_held_adapter_never_runs(self):
        module = load('icm21_references')
        index = list(next(argv for argv, kind in module.ADAPTERS.items() if kind == 'index'))
        held = dict(reader_entry(check='C-GENERATED', argv=index), status='UNVERIFIED',
                    hold_id='HOLD-1')
        statuses, seen = self.mocked(module, self.manifest([held]), b'INDEX CLEAN\n')
        self.assertEqual(seen, [])
        self.assertEqual(statuses, {('reader', 'C-GENERATED'): 'UNVERIFIED'})

    def test_unlisted_argv_never_runs(self):
        module = load('icm21_references')
        argv = [module.PYTHON, '-B', '-c', 'print("INDEX CLEAN")']
        self.assertNotIn(tuple(argv), module.ADAPTERS)
        statuses, seen = self.mocked(module, self.manifest([reader_entry(argv=argv)]),
                                     b'INDEX CLEAN\n', b'Ran 1 test in 0.001s\n\nOK\n')
        self.assertEqual(seen, [])
        self.assertEqual(statuses, {('reader', 'C-REFERENCES'): 'UNVERIFIED'})


if __name__ == '__main__':
    unittest.main()
