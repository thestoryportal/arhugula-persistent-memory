"""The references CLI saves the complete adapter outputs its digests bind (WIRE-CONTRACTS.md:44),
and the executor input is validated as ExecutorEvidence (T016 fix-round ruling). Adapter runs are mocked."""
import builtins
import contextlib
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import types
import unittest
from unittest.mock import MagicMock, patch


STATE = Path(__file__).resolve().parent
PYTHON = '.venv/bin/python'
INDEX = [PYTHON, '-B', 'code/state/build_index.py', '--check']
CONTROLS = [PYTHON, '-B', '-m', 'unittest', 'test_icm21.ReaderControls']
OUTPUTS = {tuple(INDEX): (b'checked 3 files\nINDEX CLEAN\n', b''),
           tuple(CONTROLS): (b'', b'...\n------\nRan 3 tests in 0.010s\n\nOK\n')}


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode('utf-8')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def load(name):
    spec = importlib.util.spec_from_file_location(name, STATE / (name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def snapshot(directory):
    return {str(p.relative_to(directory)): digest(p.read_bytes())
            for p in directory.rglob('*') if p.is_file()}


def reader_entry(id, path, check, argv):
    return {'id': id, 'path': path, 'role': 'reader', 'owner': 'integration',
            'source_sha256': None, 'adapter_argv': argv, 'check_ids': [check],
            'status': 'SPECIFIED', 'hold_id': None}


def operation(root):
    return {'operation_id': 'PLAN-1', 'prd_ids': ['ICM-R6'],
            'plan': {'path': str(root / 'plan.json'), 'sha256': '1' * 64},
            'approval': {'path': str(root / 'approval.json'), 'sha256': '2' * 64},
            'journal': {'path': str(root / 'journal.json'), 'sha256': '3' * 64},
            'verification': None, 'readers': None, 'acceptance': None, 'rollback': None}


def adapter(argv, **_):
    stdout, stderr = OUTPUTS[tuple(argv)]
    return subprocess.CompletedProcess(argv, 0, stdout, stderr)


class ReferenceEvidence(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix='icm21-evidence-')
        self.addCleanup(temporary.cleanup)
        self.scratch = Path(os.path.realpath(temporary.name))
        self.root = self.scratch / 'root'
        self.evidence = self.scratch / 'evidence'
        self.evidence.mkdir()
        for relative in (PYTHON, 'code/state/build_index.py', 'labviz.md'):
            (self.root / relative).parent.mkdir(parents=True, exist_ok=True)
            (self.root / relative).write_bytes(b'fixture\n')
        working = os.getcwd()
        os.chdir(self.scratch)
        self.addCleanup(os.chdir, working)

    def manifest(self, operations=()):
        readers = [reader_entry('generated', 'code/state/build_index.py', 'C-GENERATED', INDEX),
                   reader_entry('labviz', 'labviz.md', 'C-LABVIZ', CONTROLS)]
        values = {'registries': {'schema_version': 1, 'dispatcher': ['checker'],
                                 'reader_registry': readers, 'loader_registry': []},
                  'references': b'',
                  'repairs': {'schema_version': 1, 'repairs': []},
                  'executor': {'schema_version': 1, 'operations': list(operations)},
                  'coverage': {'schema_version': 1, 'scope': 'fixture', 'sources': [],
                               'coverage': {'inspected': [str(self.root)], 'excluded': [],
                                            'required_registry_ids': ['generated', 'labviz'],
                                            'checked_registry_ids': []}}}
        manifest = {'schema_version': 1}
        for key, value in values.items():
            data = value if isinstance(value, bytes) else encoded(value)
            path = self.root / (key + '.json')
            path.write_bytes(data)
            manifest[key] = {'path': str(path), 'sha256': digest(data)}
        path = self.scratch / 'manifest.json'
        path.write_bytes(encoded(manifest))
        return manifest, path

    def cli(self, *extra):
        """(exit code, printed result, subprocess.run calls) of `icm21_check.py references`."""
        _, manifest = self.manifest()
        argv = ['icm21_check.py', 'references', '--root', str(self.root),
                '--manifest', str(manifest), *extra]
        printed = io.StringIO()
        with patch.object(sys, 'argv', argv), contextlib.redirect_stdout(printed), \
                patch('subprocess.run', side_effect=adapter) as run:
            code = load('icm21_check').main()
        return code, json.loads(printed.getvalue()), run.call_count

    def digests(self, result):
        return {check[key] for reader in result['readers'] for check in reader['checks']
                for key in ('stdout_sha256', 'stderr_sha256') if check[key] is not None}

    def test_saved_files_match_digests(self):
        code, result, calls = self.cli('--evidence-dir', str(self.evidence))
        self.assertEqual((code, calls), (0, 2), result)
        named = self.digests(result)
        self.assertEqual(named, {digest(data) for pair in OUTPUTS.values() for data in pair})
        for name in named:
            with self.subTest(digest=name):
                self.assertEqual(digest((self.evidence / name).read_bytes()), name)
        self.assertEqual(set(snapshot(self.evidence)), named)

    def test_identical_existing_file_accepted(self):
        self.cli('--evidence-dir', str(self.evidence))
        before = {p: p.stat().st_mtime_ns for p in self.evidence.iterdir()}
        code, result, _ = self.cli('--evidence-dir', str(self.evidence))
        self.assertEqual(code, 0, result)
        self.assertEqual({p: p.stat().st_mtime_ns for p in self.evidence.iterdir()}, before)

    def test_different_bytes_refuse(self):
        name = digest(OUTPUTS[tuple(INDEX)][0])
        (self.evidence / name).write_bytes(b'other bytes\n')
        code, result, _ = self.cli('--evidence-dir', str(self.evidence))
        self.assertEqual(code, 1, result)
        self.assertEqual(result['status'], 'FAIL')
        self.assertIn('existing evidence differs', result['reason'])
        self.assertEqual((self.evidence / name).read_bytes(), b'other bytes\n')

    def test_no_write_without_dir(self):
        self.manifest()
        before = snapshot(self.scratch)
        code, result, calls = self.cli()
        self.assertEqual((code, calls), (0, 2), result)
        self.assertTrue(self.digests(result))
        self.assertEqual(snapshot(self.scratch), before)

    def test_invalid_executor_refused(self):
        valid = operation(self.root)
        invalid = {key: value for key, value in valid.items() if key != 'plan'}
        references = load('icm21_references')
        with patch('subprocess.run', side_effect=adapter):
            results, _ = references.dispatch(self.root, self.manifest([valid])[0])
            self.assertEqual(len(results['readers']), 2)
            with self.assertRaises(ValueError):
                references.dispatch(self.root, self.manifest([invalid])[0])

    def save(self, directory, results, outputs, **patches):
        """save_references with a mocked dispatch; returns the dispatch mock and the raised error."""
        module = load('icm21_check')
        dispatch = MagicMock(return_value=(results, outputs))
        loaded = module.area
        def area(name):
            return types.SimpleNamespace(dispatch=dispatch) if name == 'icm21_references' \
                else loaded(name)
        with contextlib.ExitStack() as stack:
            stack.enter_context(patch.object(module, 'area', area))
            for name, value in patches.items():
                stack.enter_context(patch.object(module, name, value, create=True))
            with self.assertRaises(ValueError) as raised:
                module.save_references(self.root, None, directory)
        return dispatch, raised.exception

    def test_missing_dir_refused_before_dispatch(self):
        missing = self.scratch / 'absent'
        data = b'complete adapter output\n'
        dispatch, error = self.save(missing, {'schema_version': 1, 'readers': []},
                                    {digest(data): data})
        self.assertIn('evidence directory absent', str(error))
        dispatch.assert_not_called()
        self.assertFalse(os.path.lexists(missing))

    def test_invalid_dispatch_result_refused(self):
        data = b'complete adapter output\n'
        dispatch, _ = self.save(self.evidence, {'schema_version': 2, 'readers': []},
                                {digest(data): data})
        dispatch.assert_called_once()
        self.assertEqual(list(self.evidence.iterdir()), [])

    def test_exclusive_create_race_refused(self):
        data = b'complete adapter output\n'
        competing = b'concurrent bytes\n'
        modes = []
        def race_open(path, mode='r', *args, **kwargs):
            modes.append(mode)
            with builtins.open(path, 'wb') as handle:
                handle.write(competing)
            if mode == 'xb':
                raise FileExistsError(str(path))
            return builtins.open(path, mode, *args, **kwargs)
        _, error = self.save(self.evidence, {'schema_version': 1, 'readers': []},
                             {digest(data): data}, open=race_open)
        self.assertIn('existing evidence differs', str(error))
        self.assertEqual(modes, ['xb'])
        self.assertEqual((self.evidence / digest(data)).read_bytes(), competing)
        self.assertEqual(list(self.evidence.iterdir()), [self.evidence / digest(data)])


if __name__ == '__main__':
    unittest.main()
