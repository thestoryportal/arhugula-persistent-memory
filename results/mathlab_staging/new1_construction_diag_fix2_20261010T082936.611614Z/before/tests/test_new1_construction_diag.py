import contextlib
import hashlib
import importlib
import io
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import time
import unittest
from unittest import mock
import weakref


class ConstructionDiagnosticTests(unittest.TestCase):
    def setUp(self):
        try: self.D = importlib.import_module('tools.new1_construction_diag')
        except ModuleNotFoundError as error: self.fail('construction diagnostic missing: ' + str(error))
        import torch
        self.t = torch
        self.t.set_num_threads(1)

    def fixture(self):
        C = self.t.diag(self.t.tensor([.02, .005, .004, .002, .0001]))
        P = self.t.diag(self.t.tensor([0., 0., 1., 1., 1.]))
        probes = [P @ self.t.randn(5, generator=self.t.Generator().manual_seed(j)) for j in range(4)]
        return C, 3, self.D.G.tensor_sha(P), probes

    def report(self, **changes):
        C, count, sha, probes = self.fixture()
        return self.D.construction_reports(C, changes.get('count', count),
                                           changes.get('sha', sha), changes.get('probes', probes))

    def run_fixture(self, command, directory, **kw):
        with contextlib.redirect_stderr(io.StringIO()):
            status = self.D.I.supervise(command, directory, preflight=lambda: None,
                admission=kw.pop('admission', lambda: {'allowed': True, 'synthetic': True}),
                monitor=kw.pop('monitor', lambda pid: {'rss_gib': .01, 'process_count': 1}),
                seconds=kw.pop('seconds', 2), **kw)
        return status, json.loads((directory / 'result.json').read_text())

    def test_order_is_predeclared_four_patterns_and_single_native_svd(self):
        C, count, sha, probes = self.fixture()
        original = self.t.linalg.svd
        with mock.patch.object(self.t.linalg, 'svd', wraps=original) as svd:
            report = self.D.construction_reports(C, count, sha, probes)
        self.assertEqual(svd.call_count, 1)
        self.assertIs(svd.call_args.args[0], C)
        self.assertEqual(svd.call_args.kwargs, {'full_matrices': False})
        self.assertEqual([p['construction'] for p in report['constructions']],
                         ['list_shared', 'list_separate', 'long_shared', 'long_separate'])
        self.assertEqual(report['native_before'], report['native_after'])
        self.assertEqual([p['index_kind'] for p in report['constructions']], ['list', 'list', 'long', 'long'])
        self.assertTrue(all(p['allowed_count'] == 3 and p['excluded_count'] == 2 for p in report['constructions']))

    def test_each_projector_calls_the_actual_unchanged_gate(self):
        with mock.patch.object(self.D.G, 'projector_matches', wraps=self.D.G.projector_matches) as gate:
            rows = self.report()['constructions']
        self.assertEqual(gate.call_count, 4)
        self.assertTrue(all(row['matches_capture_gate'] for row in rows))
        for call in gate.call_args_list:
            self.assertEqual(call.args[1:3], (3, 3))
            self.assertEqual(len(call.args[4]), 4)

    def test_report_records_returned_gate_not_a_reimplemented_boolean(self):
        with mock.patch.object(self.D.G, 'projector_matches', return_value=False):
            rows = self.report()['constructions']
        self.assertTrue(all(row['projector_sha_matches'] and row['all_probes_match_1e6'] for row in rows))
        self.assertTrue(all(row['matches_capture_gate'] is False for row in rows))

    def test_all_probes_reported_even_when_sha_matches(self):
        rows = self.report()['constructions']
        for row in rows:
            self.assertEqual([p['seed'] for p in row['probes']], list(range(4)))
            self.assertTrue(all(p['relative_error'] == 0 and p['absolute_l2_residual'] == 0 for p in row['probes']))
            self.assertTrue(row['projector_sha_matches'])
            self.assertEqual(row['captured_allowed_count'], 3)
            self.assertEqual(row['captured_excluded_count'], 2)

    def test_count_short_circuit_does_not_hide_sha_or_any_probe(self):
        rows = self.report(count=2)['constructions']
        for row in rows:
            self.assertFalse(row['count_matches'])
            self.assertFalse(row['matches_capture_gate'])
            self.assertTrue(row['projector_sha_matches'])
            self.assertTrue(row['all_probes_match_1e6'])
            self.assertEqual(len(row['probes']), 4)

    def test_failed_first_probe_does_not_hide_later_probes(self):
        C, count, sha, probes = self.fixture()
        probes[0] = probes[0] + .1
        rows = self.D.construction_reports(C, count, '0' * 64, probes)['constructions']
        for row in rows:
            self.assertFalse(row['matches_capture_gate'])
            self.assertEqual(row['probes'][0]['match'], 'NO-MATCH')
            self.assertEqual([p['match'] for p in row['probes'][1:]], ['MATCH'] * 3)
            self.assertGreater(row['max_probe_relative_error'], 1e-6)

    def test_sha_short_circuit_retains_sampled_probe_disagreement(self):
        C, count, sha, probes = self.fixture()
        probes[3] = probes[3] + .1
        for row in self.D.construction_reports(C, count, sha, probes)['constructions']:
            self.assertTrue(row['matches_capture_gate'])
            self.assertFalse(row['all_probes_match_1e6'])
            self.assertEqual(row['probes'][3]['match'], 'NO-MATCH')

    def test_storage_stride_hash_facts_discriminate_gather_shapes(self):
        rows = self.report()['constructions']
        for row in rows:
            shared = row['gather_style'] == 'shared'
            self.assertEqual(row['gather_count'], 1 if shared else 2)
            self.assertEqual(row['operands_share_storage'], shared)
            self.assertFalse(row['left_shares_U_storage'])
            self.assertFalse(row['right_shares_U_storage'])
            self.assertTrue(row['right_equals_left_transpose_bytes'])
            self.assertEqual(row['left']['shape'], [5, 3])
            self.assertEqual(row['right']['shape'], [3, 5])
            self.assertEqual(row['left']['stride'], [3, 1])
            self.assertEqual(row['right']['stride'], [1, 3])
            self.assertEqual(row['left']['storage_bytes'], 60)
            self.assertEqual(row['right']['storage_offset'], 0)
            self.assertEqual(row['left']['dtype'], 'torch.float32')
        self.assertEqual(len({row['left']['sha256'] for row in rows}), 1)
        self.assertEqual(len({row['right']['sha256'] for row in rows}), 1)

    def test_projector_and_gathers_are_released_before_next_construction(self):
        previous = []
        original = self.D.G.projector_matches
        def check(P, *args):
            self.assertTrue(all(ref() is None for ref in previous))
            previous.append(weakref.ref(P))
            return original(P, *args)
        with mock.patch.object(self.D.G, 'projector_matches', new=check): self.report()
        self.assertEqual(len(previous), 4)
        self.assertTrue(all(ref() is None for ref in previous))

    def test_operand_hashing_occurs_after_matmul(self):
        original = self.D.G.projector_matches
        events = []
        original_facts = self.D.tensor_facts
        def gate(P, *args):
            events.append('projector_complete')
            return original(P, *args)
        def facts(value):
            if tuple(value.shape) in ((5, 3), (3, 5)):
                self.assertTrue(events and events[-1] == 'projector_complete')
            return original_facts(value)
        with mock.patch.object(self.D.G, 'projector_matches', side_effect=gate), \
             mock.patch.object(self.D, 'tensor_facts', side_effect=facts): self.report()
        self.assertEqual(len(events), 4)

    def test_shared_native_operands_are_fingerprinted_and_mutation_refuses(self):
        C, count, sha, probes = self.fixture()
        U, s, Vh = self.t.linalg.svd(C, full_matrices=False)
        def corrupt(P, *args):
            U[0, 0] = .123
            return False
        with mock.patch.object(self.t.linalg, 'svd', return_value=(U, s, Vh)), \
             mock.patch.object(self.D.G, 'projector_matches', side_effect=corrupt):
            with self.assertRaisesRegex(self.D.G.Invalid, 'native operands mutated'):
                self.D.construction_reports(C, count, sha, probes)

    def test_invalid_covariance_never_reaches_svd(self):
        C, count, sha, probes = self.fixture()
        for bad in (C.double(), C[:, :3], self.t.full((5, 5), float('nan'))):
            with self.subTest(shape=tuple(bad.shape), dtype=bad.dtype), \
                 mock.patch.object(self.t.linalg, 'svd') as svd:
                with self.assertRaises(self.D.G.Invalid): self.D.construction_reports(bad, count, sha, probes)
                svd.assert_not_called()

    def test_invalid_probe_metadata_never_reaches_svd(self):
        C, count, sha, probes = self.fixture()
        for bad in (probes[:3], [probes[0].double(), *probes[1:]],
                    [self.t.zeros(5), *probes[1:]], [self.t.ones(4), *probes[1:]],
                    [self.t.full((5,), float('inf')), *probes[1:]]):
            with self.subTest(probe_count=len(bad)), mock.patch.object(self.t.linalg, 'svd') as svd:
                with self.assertRaises(self.D.G.Invalid): self.D.construction_reports(C, count, sha, bad)
                svd.assert_not_called()

    def test_invalid_counts_and_sha_are_not_coerced(self):
        C, count, sha, probes = self.fixture()
        for bad_count, bad_sha in ((True, sha), (-1, sha), (6, sha), (3.0, sha), (3, 'bad'), (3, 'g' * 64)):
            with self.subTest(count=bad_count, sha=bad_sha), mock.patch.object(self.t.linalg, 'svd') as svd:
                with self.assertRaises(self.D.G.Invalid): self.D.construction_reports(C, bad_count, bad_sha, probes)
                svd.assert_not_called()

    def test_probe_tolerance_remains_inclusive_and_promotes_residuals(self):
        ref = self.t.tensor([1., 0.], dtype=self.t.float64)
        at = self.D.I.probe_metrics(self.t.tensor([1., 1e-6], dtype=self.t.float64), ref)
        above = self.D.I.probe_metrics(self.t.tensor([1., 1.001e-6], dtype=self.t.float64), ref)
        self.assertEqual(at['match'], 'MATCH')
        self.assertEqual(above['match'], 'NO-MATCH')

    def test_capture_metadata_selects_only_l4_count_hash_and_four_probes(self):
        C, count, sha, probes = self.fixture()
        bundle = {'l4.Pi_null_n': self.t.tensor(count),
                  'l4.Pi_sha256': self.t.tensor(list(bytes.fromhex(sha)), dtype=self.t.uint8),
                  **{f'l4.Pi_probe{j}': p for j, p in enumerate(probes)}, 'l4.upd_precast': object()}
        actual_count, actual_sha, actual_probes = self.D.capture_metadata(bundle, 5)
        self.assertEqual((actual_count, actual_sha), (count, sha))
        self.assertEqual(len(actual_probes), 4)
        for p, original in zip(actual_probes, probes):
            self.assertTrue(self.t.equal(p, original))
            self.assertNotEqual(p.data_ptr(), original.data_ptr())

    def test_missing_or_wrong_capture_metadata_refuses(self):
        for bundle in ({}, {'l4.Pi_null_n': self.t.tensor(3.), 'l4.Pi_sha256': self.t.zeros(32, dtype=self.t.uint8)},
                       {'l4.Pi_null_n': self.t.tensor(3), 'l4.Pi_sha256': self.t.zeros(31, dtype=self.t.uint8)}):
            with self.subTest(keys=list(bundle)), self.assertRaises(self.D.G.Invalid):
                self.D.capture_metadata(bundle, 5)

    def test_report_is_scalar_json_without_dense_persistence(self):
        report = self.report()
        encoded = json.dumps(report, allow_nan=False).encode()
        self.assertLess(len(encoded), 50000)
        self.assertEqual(len(report['captured_probe_sha256']), 4)
        self.assertEqual(report['native_before']['indices_list_count'], 3)
        self.assertEqual(report['native_before']['indices_list_sha256'],
            hashlib.sha256(json.dumps([2, 3, 4], separators=(',', ':')).encode()).hexdigest())

    def test_measure_consumes_only_three_synthetic_inputs_with_cpu_mmap(self):
        C, count, sha, probes = self.fixture()
        bundle = {'l4.Pi_null_n': self.t.tensor(count),
                  'l4.Pi_sha256': self.t.tensor(list(bytes.fromhex(sha)), dtype=self.t.uint8),
                  **{f'l4.Pi_probe{j}': p for j, p in enumerate(probes)}}
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            cache, capture, manifest = (str(directory/name) for name in ('cache.npz', 'capture.pt', 'manifest.json'))
            Path(manifest).write_text(json.dumps({'covariances': {'4': {'path': cache, 'sha256': 'a'*64}},
                                                  'torch_version': 'synthetic'}))
            pins = {cache:'a'*64, capture:'b'*64, manifest:'c'*64}
            @contextlib.contextmanager
            def bound(path, expected):
                self.assertEqual(pins[str(path)], expected)
                yield Path(path)
            with mock.patch.multiple(self.D, CACHE=cache, CAPTURE=capture, MANIFEST=manifest,
                                     INPUT_PINS=pins, DIMENSION=5), \
                 mock.patch.object(self.D.G, 'bound_input', side_effect=bound) as inputs, \
                 mock.patch.object(self.D.G, 'load_covariance', return_value=C) as load_C, \
                 mock.patch.object(self.t, 'load', return_value=bundle) as load_capture, \
                 mock.patch.object(self.t.linalg, 'svd', wraps=self.t.linalg.svd) as svd:
                result = self.D.measure()
            self.assertEqual(result['status'], 'MEASURED')
            self.assertEqual(inputs.call_count, 3)
            self.assertEqual(svd.call_count, 1)
            load_C.assert_called_once_with(Path(cache))
            load_capture.assert_called_once_with(Path(capture), map_location='cpu', weights_only=True, mmap=True)
            self.assertEqual(result['provenance']['captured_torch_version'], 'synthetic')
            self.assertEqual(result['provenance']['captured_threads'], 'UNKNOWN')
            self.assertEqual(len(result['constructions']), 4)
            self.assertNotIn('energies', result)
            self.assertNotIn('predictions', result)

    def test_manifest_cache_disagreement_refuses_before_covariance_or_capture_load(self):
        with tempfile.TemporaryDirectory() as temp:
            manifest = Path(temp)/'manifest.json'
            manifest.write_text(json.dumps({'covariances': {'4': {'path':'wrong', 'sha256':'0'*64}}}))
            @contextlib.contextmanager
            def bound(path, expected): yield Path(path)
            with mock.patch.multiple(self.D, CACHE='synthetic.npz', CAPTURE='synthetic.pt', MANIFEST=str(manifest),
                    INPUT_PINS={'synthetic.npz':'a'*64, 'synthetic.pt':'b'*64, str(manifest):'c'*64}), \
                 mock.patch.object(self.D.G, 'bound_input', side_effect=bound), \
                 mock.patch.object(self.D.G, 'load_covariance') as load_C, mock.patch.object(self.t, 'load') as capture:
                with self.assertRaisesRegex(self.D.G.Invalid, 'manifest L4 cache identity'): self.D.measure()
            load_C.assert_not_called(); capture.assert_not_called()

    def test_measured_status_can_contain_four_failed_gates(self):
        rows = self.report(sha='0' * 64, count=1)['constructions']
        self.assertFalse(any(row['matches_capture_gate'] for row in rows))
        self.assertEqual(len(rows), 4)

    def test_runtime_caps_and_pins_reuse_frozen_identity_contract(self):
        self.assertEqual((self.D.I.DEADLINE_S, self.D.I.RSS_CAP_GIB, self.D.I.THREADS, self.D.I.DISK_BYTES),
                         (600, 11., 8, 1000000))
        self.assertEqual(self.D.INPUT_PINS, self.D.I.INPUT_PINS)
        self.assertEqual(self.D.SOURCE_PINS['tools/new1_identity_diag.py'],
                         'c4601c6df61cf7c36c6223d5955236c0c8f901ded216889755bcd397ae25c1d3')
        self.assertIn('results/mathlab_staging/new1_construction_diag_authorization.md', self.D.SOURCE_PINS)
        self.assertIn('results/mathlab_staging/new1_identity_diag_astra.md', self.D.SOURCE_PINS)

    def test_verify_launch_refuses_nice_20_before_input_pins(self):
        with mock.patch.object(self.D.G, 'verify_file'), \
             mock.patch.object(self.D.I, 'verify_pins') as pins, \
             mock.patch.object(self.D, 'verify_historical_source'), \
             mock.patch.object(os, 'getpriority', return_value=20), \
             mock.patch.dict(os.environ, {'LLMDB_DEVICE':'cpu', 'CUDA_VISIBLE_DEVICES':'',
                                        'OMP_NUM_THREADS':'8', 'MKL_NUM_THREADS':'8'}):
            with self.assertRaisesRegex(self.D.G.Invalid, 'nice 10'): self.D.verify_launch('0'*64, '0'*64)
        self.assertEqual(pins.call_count, 1)

    def test_direct_worker_refuses_before_numerical_imports_and_input_pins(self):
        with mock.patch.dict(os.environ, {}, clear=True), mock.patch.object(self.D, 'measure') as measure, \
             mock.patch.object(self.D, 'verify_launch') as verify, contextlib.redirect_stderr(io.StringIO()):
            status = self.D.main(['--worker', '--scope-sha', '0'*64, '--source-sha', '0'*64])
        self.assertEqual(status, 2)
        measure.assert_not_called(); verify.assert_not_called()

    def test_bad_source_pin_refuses_before_namespace_or_real_inputs(self):
        with mock.patch.object(self.D, 'new_directory') as directory, \
             mock.patch.object(self.D, 'verify_launch') as verify, contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(self.D.main(['--scope-sha','0'*64,'--source-sha','0'*64]), 2)
        directory.assert_not_called(); verify.assert_not_called()

    def test_namespace_is_construction_and_exclusive(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = self.D.new_directory(Path(temp))
            self.assertTrue(directory.name.startswith('construction_'))
            self.D.I.Output(directory)
            with self.assertRaises(FileExistsError): self.D.I.Output(directory)

    def test_refused_admission_cannot_start_fixture_worker(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = self.D.new_directory(Path(temp)); marker = Path(temp)/'marker'
            status, result = self.run_fixture([sys.executable, '-B', '-c',
                f'from pathlib import Path; Path({str(marker)!r}).write_text("ran")'], directory,
                admission=lambda: {'allowed': False})
            self.assertEqual(status, 2); self.assertFalse(marker.exists())
            self.assertEqual(result['status'], 'INVALID')

    def test_fixture_worker_deadline_and_family_rss_are_fail_closed(self):
        for kind in ('deadline', 'rss'):
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as temp:
                directory = self.D.new_directory(Path(temp)); start = time.monotonic()
                kw = {'seconds': .08} if kind == 'deadline' else {
                    'monitor': lambda pid: {'rss_gib': 11. if pid else .01, 'process_count': 1}}
                status, result = self.run_fixture([sys.executable, '-B', '-c', 'import time; time.sleep(5)'],
                                                  directory, **kw)
                self.assertEqual(status, 2); self.assertEqual(result['status'], 'INVALID')
                self.assertLess(time.monotonic() - start, 2)

    def test_fixture_terminal_receipt_round_trips_small_scalar_report(self):
        report = {'status': 'MEASURED', **self.report()}
        with tempfile.TemporaryDirectory() as temp:
            directory = self.D.new_directory(Path(temp))
            status, result = self.run_fixture([sys.executable, '-B', '-c', f'print({json.dumps(report)!r})'], directory)
            receipts = [json.loads(line) for line in (directory/'receipt.jsonl').read_text().splitlines()]
            self.assertEqual(status, 0); self.assertEqual(result['constructions'], report['constructions'])
            self.assertEqual(receipts[-1]['status'], 'MEASURED')
            self.assertEqual(receipts[-1]['result_sha256'], self.D.S.sha_file(directory/'result.json'))
            self.assertEqual({p.name for p in directory.iterdir()}, {'receipt.jsonl', 'result.json'})
            self.assertLess(sum(p.stat().st_size for p in directory.iterdir()), 1000000)

    def test_launch_command_computes_increment_and_contains_exact_pins(self):
        command = self.D.launch_command('1'*64, '2'*64)
        self.assertIn('10-current', command)
        self.assertIn('nice -n "$new1_nice_increment"', command)
        self.assertIn('--scope-sha ' + '1'*64, command)
        self.assertIn('--source-sha ' + '2'*64, command)
        probe = command.splitlines()[0]
        proc = subprocess.run(['/bin/sh', '-c', probe + '\nprintf "%s\\n" "$new1_nice_increment"'],
                              capture_output=True, text=True, timeout=3)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(int(proc.stdout), 10-os.getpriority(os.PRIO_PROCESS, 0))

    def test_import_is_stdlib_only_and_unset_root_fails_loudly(self):
        code = ('import sys; import tools.new1_construction_diag; '
                'assert not any(x in sys.modules for x in ("torch","numpy","transformers","safetensors"))')
        env = dict(os.environ, LLMDB_ROOT=str(Path.cwd()), PYTHONDONTWRITEBYTECODE='1')
        proc = subprocess.run([sys.executable, '-B', '-c', code], capture_output=True, text=True, env=env, timeout=3)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        env.pop('LLMDB_ROOT')
        proc = subprocess.run([sys.executable, '-B', '-c', code], capture_output=True, text=True, env=env, timeout=3)
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn('LLMDB_ROOT', proc.stderr)

    def gated_fixture(self, marker):
        return ('import sys,time; from pathlib import Path; '
                'from tools import new1_construction_diag as D; '
                'D.verify_launch=lambda *args:None; '
                f'Path({str(marker.with_suffix(".waiting"))!r}).write_text("bootstrap ready"); '
                f'D.measure=lambda:(Path({str(marker)!r}).write_text("arithmetic reached"),'
                'time.sleep(.1),{"status":"MEASURED","synthetic":True})[-1]; '
                'sys.exit(D.main(["--worker","--scope-sha","0"*64,"--source-sha","0"*64]))')

    def reap_fixture(self, children):
        for child in children:
            if child.poll() is None: os.killpg(child.pid, signal.SIGKILL)
            child.communicate(timeout=1)

    def test_real_watchdog_late_popen_handle_is_owned_killed_and_reaped(self):
        children = []
        original = self.D.I.subprocess.Popen
        def late(*args, **kw):
            child = original(*args, **kw); children.append(child)
            time.sleep(.2)
            return child
        try:
            with tempfile.TemporaryDirectory() as temp, mock.patch.object(self.D.I.subprocess, 'Popen', new=late):
                directory = self.D.new_directory(Path(temp))
                status, result = self.run_fixture([sys.executable, '-B', '-c', 'import time;time.sleep(30)'],
                                                  directory, seconds=.05)
                self.assertEqual(status, 2)
                self.assertIn('STOPPED-DEADLINE', result['error'])
                self.assertEqual(len(children), 1)
                with self.assertRaises(ProcessLookupError): os.kill(children[0].pid, 0)
                self.assertEqual(result['worker_pid'], children[0].pid)
        finally: self.reap_fixture(children)

    def test_deadline_during_registration_never_releases_worker_arithmetic(self):
        children = []
        original = self.D.I.subprocess.Popen
        def late(*args, **kw):
            child = original(*args, **kw); children.append(child)
            time.sleep(.2)
            return child
        try:
            with tempfile.TemporaryDirectory() as temp:
                marker = Path(temp)/'arithmetic'
                directory = self.D.new_directory(Path(temp)/'runs')
                with mock.patch.object(self.D.I.subprocess, 'Popen', new=late):
                    status, result = self.run_fixture([sys.executable, '-B', '-c', self.gated_fixture(marker)],
                                                      directory, seconds=.05)
                self.assertEqual(status, 2)
                self.assertFalse(marker.exists())
                with self.assertRaises(ProcessLookupError): os.kill(children[0].pid, 0)
        finally: self.reap_fixture(children)

    def test_registered_resource_refusal_precedes_worker_release(self):
        with tempfile.TemporaryDirectory() as temp:
            marker = Path(temp)/'arithmetic'
            directory = self.D.new_directory(Path(temp)/'runs')
            def refuse(pid):
                if pid:
                    limit = time.monotonic()+.7
                    while not marker.with_suffix('.waiting').exists() and time.monotonic()<limit: time.sleep(.005)
                    self.assertTrue(marker.with_suffix('.waiting').exists())
                    time.sleep(.03)
                    self.assertFalse(marker.exists())
                return {'rss_gib':11. if pid else .01, 'process_count':1}
            status, result = self.run_fixture([sys.executable, '-B', '-c', self.gated_fixture(marker)],
                                              directory, monitor=refuse)
            self.assertEqual(status, 2)
            self.assertIn('STOPPED-RESOURCE', result['error'])
            self.assertFalse(marker.exists())

    def test_registered_worker_requires_explicit_release_before_measure(self):
        with tempfile.TemporaryDirectory() as temp:
            marker = Path(temp)/'arithmetic'
            directory = self.D.new_directory(Path(temp)/'runs')
            seen = []
            def observe(pid):
                if pid:
                    limit = time.monotonic()+.7
                    while not marker.with_suffix('.waiting').exists() and time.monotonic()<limit: time.sleep(.005)
                    self.assertTrue(marker.with_suffix('.waiting').exists())
                    time.sleep(.03)
                    self.assertFalse(marker.exists())
                    seen.append(pid)
                return {'rss_gib':.01, 'process_count':1}
            status, result = self.run_fixture([sys.executable, '-B', '-c', self.gated_fixture(marker)],
                                              directory, monitor=observe)
            self.assertEqual(status, 0)
            self.assertTrue(marker.exists())
            self.assertTrue(seen)
            self.assertTrue(result['synthetic'])

    def test_launch_has_its_own_bound_while_whole_run_budget_remains(self):
        children = []
        original = self.D.I.subprocess.Popen
        def late(*args, **kw):
            child = original(*args, **kw); children.append(child)
            time.sleep(.2)
            return child
        try:
            with tempfile.TemporaryDirectory() as temp:
                marker = Path(temp)/'arithmetic'; directory = self.D.new_directory(Path(temp)/'runs')
                with mock.patch.object(self.D.I, 'LAUNCH_S', .05, create=True), \
                     mock.patch.object(self.D.I.subprocess, 'Popen', new=late):
                    status, result = self.run_fixture([sys.executable, '-B', '-c', self.gated_fixture(marker)],
                                                      directory, seconds=2)
                self.assertEqual(status, 2)
                self.assertIn('STOPPED-LAUNCH', result['error'])
                self.assertFalse(marker.exists())
                with self.assertRaises(ProcessLookupError): os.kill(children[0].pid, 0)
        finally: self.reap_fixture(children)

    def test_worker_exits_promptly_when_release_never_arrives_or_pipe_closes(self):
        for close in (False, True):
            with self.subTest(close=close), tempfile.TemporaryDirectory() as temp:
                marker = Path(temp)/'arithmetic'; read_fd, write_fd = os.pipe()
                env = dict(os.environ, NEW1_IDENTITY_PARENT=str(os.getpid()),
                           NEW1_IDENTITY_RELEASE_FD=str(read_fd), NEW1_IDENTITY_RELEASE_BY=str(time.monotonic()+.15),
                           NEW1_IDENTITY_DEADLINE=str(time.monotonic()+1))
                child = subprocess.Popen([sys.executable, '-B', '-c', self.gated_fixture(marker)], env=env,
                    pass_fds=(read_fd,), start_new_session=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                os.close(read_fd)
                try:
                    if close: os.close(write_fd); write_fd = None
                    stdout, stderr = child.communicate(timeout=1)
                    self.assertNotEqual(child.returncode, 0)
                    self.assertFalse(marker.exists())
                    self.assertIn(b'LAUNCH', stderr)
                finally:
                    if write_fd is not None: os.close(write_fd)
                    self.reap_fixture([child])

    def test_worker_exits_on_parent_death_even_with_another_writer_open(self):
        self.assertTrue(hasattr(self.D.I, 'wait_for_release'), 'worker release/liveness guard missing')
        with tempfile.TemporaryDirectory() as temp:
            marker = Path(temp)/'arithmetic'; gate_read, gate_write = os.pipe(); status_read, status_write = os.pipe()
            grandchild = ('import os,time;from pathlib import Path;from tools import new1_identity_diag as I;'
                '\ntry:I.wait_for_release()\n'
                'except I.S.Stop:os.write(int(os.environ["FIXTURE_STATUS_FD"]),b"STOPPED");raise SystemExit(2)\n'
                f'Path({str(marker)!r}).write_text("arithmetic reached")')
            parent_code = ('import os,subprocess,sys,time;'
                'env=dict(os.environ,NEW1_IDENTITY_PARENT=str(os.getpid()),'
                'NEW1_IDENTITY_RELEASE_BY=str(time.monotonic()+4),NEW1_IDENTITY_DEADLINE=str(time.monotonic()+5));'
                f'p=subprocess.Popen([sys.executable,"-B","-c",{grandchild!r}],env=env,'
                f'pass_fds=({gate_read},{status_write}));'
                'print(p.pid,flush=True);time.sleep(.2);'
                'sys.exit("worker exited before parent death") if p.poll() is not None else None')
            env = dict(os.environ, NEW1_IDENTITY_RELEASE_FD=str(gate_read), FIXTURE_STATUS_FD=str(status_write))
            parent = subprocess.Popen([sys.executable, '-B', '-c', parent_code], env=env,
                pass_fds=(gate_read,status_write), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            os.close(gate_read); os.close(status_write)
            try:
                stdout, stderr = parent.communicate(timeout=1)
                self.assertEqual(parent.returncode, 0, stderr)
                import select
                self.assertTrue(select.select([status_read], [], [], .5)[0], 'worker did not notice parent death')
                self.assertEqual(os.read(status_read, 32), b'STOPPED')
                self.assertFalse(marker.exists())
            finally:
                os.close(gate_write); os.close(status_read)
                if parent.poll() is None: parent.kill()
                parent.communicate(timeout=1)

    def test_keyboard_interrupt_during_popen_registration_cleans_without_release(self):
        children = []
        original = self.D.I.subprocess.Popen
        previous = signal.getsignal(signal.SIGINT)
        signal.signal(signal.SIGINT, signal.default_int_handler)
        def late(*args, **kw):
            child = original(*args, **kw); children.append(child)
            time.sleep(.05)
            os.kill(os.getpid(), signal.SIGINT)
            time.sleep(.15)
            return child
        try:
            with tempfile.TemporaryDirectory() as temp:
                marker = Path(temp)/'arithmetic'; directory = self.D.new_directory(Path(temp)/'runs')
                with mock.patch.object(self.D.I.subprocess, 'Popen', new=late):
                    status, result = self.run_fixture([sys.executable, '-B', '-c', self.gated_fixture(marker)],
                                                      directory, seconds=2)
                self.assertEqual(status, 130)
                self.assertFalse(marker.exists())
                with self.assertRaises(ProcessLookupError): os.kill(children[0].pid, 0)
        finally:
            signal.signal(signal.SIGINT, previous)
            self.reap_fixture(children)

    def test_stalled_launch_returns_within_bound_and_late_handle_cleans_once(self):
        import threading
        children = []; finish = threading.Event()
        original = self.D.I.subprocess.Popen
        def stalled(*args, **kw):
            child = original(*args, **kw); children.append(child)
            finish.wait(2)
            return child
        try:
            with tempfile.TemporaryDirectory() as temp:
                marker = Path(temp)/'arithmetic'; directory = self.D.new_directory(Path(temp)/'runs')
                start = time.monotonic()
                with mock.patch.object(self.D.I, 'LAUNCH_S', .05, create=True), \
                     mock.patch.object(self.D.I, 'CLEANUP_S', .05), \
                     mock.patch.object(self.D.I.subprocess, 'Popen', new=stalled):
                    status, result = self.run_fixture([sys.executable, '-B', '-c', self.gated_fixture(marker)],
                                                      directory, seconds=.8)
                self.assertEqual(status, 2)
                self.assertIn('STOPPED-LAUNCH', result['error'])
                self.assertLess(time.monotonic()-start, .3)
                self.assertFalse(marker.exists())
                finish.set()
                limit = time.monotonic()+1
                while children[0].poll() is None and time.monotonic()<limit: time.sleep(.01)
                self.assertIsNotNone(children[0].poll())
                limit = time.monotonic()+1
                while not children[0].stdout.closed and time.monotonic()<limit: time.sleep(.01)
                self.assertTrue(children[0].stdout.closed and children[0].stderr.closed)
        finally:
            finish.set(); self.reap_fixture(children)

    def test_already_exited_unreleased_worker_is_reaped_without_group_signal(self):
        children = []
        original = self.D.I.subprocess.Popen
        def late(*args, **kw):
            child = original(*args, **kw); children.append(child)
            time.sleep(.3)
            return child
        def denied(child): raise PermissionError('fixture signal denied for exited process group')
        try:
            with tempfile.TemporaryDirectory() as temp:
                marker = Path(temp)/'arithmetic'; directory = self.D.new_directory(Path(temp)/'runs')
                with mock.patch.object(self.D.I.subprocess, 'Popen', new=late), \
                     mock.patch.object(self.D.S, 'terminate', side_effect=denied) as terminate:
                    status, result = self.run_fixture([sys.executable, '-B', '-c', self.gated_fixture(marker)],
                                                      directory, seconds=.05)
                self.assertEqual(status, 2)
                self.assertEqual(children[0].returncode, 2)
                terminate.assert_not_called()
                self.assertFalse(marker.exists())
                with self.assertRaises(ProcessLookupError): os.kill(children[0].pid, 0)
        finally: self.reap_fixture(children)

    def test_released_worker_exits_on_parent_death_while_main_is_blocked(self):
        with tempfile.TemporaryDirectory() as temp:
            marker = Path(temp)/'released'; gate_read, gate_write = os.pipe(); status_read, status_write = os.pipe()
            worker = ('import os,time;from pathlib import Path;from tools import new1_identity_diag as I;'
                'I.wait_for_release();'
                f'Path({str(marker)!r}).write_text("released");'
                'os.write(int(os.environ["FIXTURE_STATUS_FD"]),b"RELEASED");time.sleep(5)')
            parent_code = ('import os,subprocess,sys,time;from pathlib import Path;'
                'env=dict(os.environ,NEW1_IDENTITY_PARENT=str(os.getpid()),'
                'NEW1_IDENTITY_RELEASE_BY=str(time.monotonic()+3),NEW1_IDENTITY_DEADLINE=str(time.monotonic()+4));'
                f'p=subprocess.Popen([sys.executable,"-B","-c",{worker!r}],env=env,pass_fds=({gate_read},{status_write}));'
                f'os.write({gate_write},b"RUN\\n");limit=time.monotonic()+1;'
                f'\nwhile not Path({str(marker)!r}).exists() and time.monotonic()<limit:time.sleep(.005)\n'
                f'assert Path({str(marker)!r}).exists(),"worker never received release"')
            env = dict(os.environ, NEW1_IDENTITY_RELEASE_FD=str(gate_read), FIXTURE_STATUS_FD=str(status_write))
            parent = subprocess.Popen([sys.executable, '-B', '-c', parent_code], env=env,
                pass_fds=(gate_read,gate_write,status_write), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            os.close(gate_read); os.close(status_write)
            try:
                stdout, stderr = parent.communicate(timeout=2)
                self.assertEqual(parent.returncode, 0, stderr)
                self.assertEqual(os.read(status_read, 8), b'RELEASED')
                import select
                self.assertTrue(select.select([status_read], [], [], .5)[0], 'released worker outlived dead parent')
                self.assertEqual(os.read(status_read, 1), b'')
            finally:
                os.close(gate_write); os.close(status_read)
                if parent.poll() is None: parent.kill()
                parent.communicate(timeout=1)

    def test_released_worker_has_independent_whole_deadline_while_main_is_blocked(self):
        read_fd, write_fd = os.pipe()
        end = time.monotonic()+.3
        env = dict(os.environ, NEW1_IDENTITY_PARENT=str(os.getpid()), NEW1_IDENTITY_RELEASE_FD=str(read_fd),
                   NEW1_IDENTITY_RELEASE_BY=str(end), NEW1_IDENTITY_DEADLINE=str(end))
        code = ('import time;from tools import new1_identity_diag as I;I.wait_for_release();'
                'print("RELEASED",flush=True);time.sleep(5)')
        child = subprocess.Popen([sys.executable,'-B','-c',code],env=env,pass_fds=(read_fd,),
            start_new_session=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        os.close(read_fd)
        try:
            os.write(write_fd,b'RUN\n');os.close(write_fd);write_fd=None
            stdout, stderr = child.communicate(timeout=1)
            self.assertEqual(stdout.strip(),b'RELEASED')
            self.assertEqual(child.returncode,2)
        finally:
            if write_fd is not None:os.close(write_fd)
            self.reap_fixture([child])


if __name__ == '__main__': unittest.main()
