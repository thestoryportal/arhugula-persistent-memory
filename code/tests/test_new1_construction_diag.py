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
        try: self.D = importlib.import_module('lab.runners.new1_construction_diag')
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
        self.assertEqual(self.D.SOURCE_PINS['code/lab/runners/new1_identity_diag.py'],
                         '919b3a11a836973ea4c0d2abdd2514634ea62792e6009e828a63d81f297c3d0d')
        self.assertIn('experiments/new1/rulings/new1_construction_diag_authorization.md', self.D.SOURCE_PINS)
        self.assertIn('experiments/new1/reviews/new1_identity_diag_astra.md', self.D.SOURCE_PINS)

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
        code = ('import sys; import lab.runners.new1_construction_diag; '
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
                'from lab.runners import new1_construction_diag as D; '
                'D.verify_launch=lambda *args:None; '
                f'Path({str(marker.with_suffix(".waiting"))!r}).write_text("bootstrap ready"); '
                f'D.measure=lambda:(Path({str(marker)!r}).write_text("arithmetic reached"),'
                'time.sleep(.1),{"status":"MEASURED","synthetic":True})[-1]; '
                'sys.exit(D.main(["--worker","--scope-sha","0"*64,"--source-sha","0"*64]))')

    @contextlib.contextmanager
    def owned_fixture(self, delay=0, interrupt=False):
        owners = []; original = self.D.I.OwnedWorker.start
        def start(owner, *args):
            owners.append(owner); original(owner, *args)
            if interrupt: os.kill(os.getpid(), signal.SIGINT)
            if delay: time.sleep(delay)
        with mock.patch.object(self.D.I.OwnedWorker, 'start', new=start):
            yield owners
        for owner in owners:
            self.assertIsNotNone(owner.returncode, 'guardian not reaped before terminal return')
            self.assertIsNotNone(owner.proof, 'worker reaping proof missing')
            with self.assertRaises(ChildProcessError): os.waitpid(owner.pid, os.WNOHANG)
            with self.assertRaises(ProcessLookupError): os.kill(owner.worker_pid, 0)
            self.assertTrue(all(fd is None for pair in owner.channels.values() for fd in pair))

    def reap_fixture(self, children):
        for child in children:
            if child.poll() is None: os.killpg(child.pid, signal.SIGKILL)
            child.communicate(timeout=1)

    def test_real_watchdog_late_popen_handle_is_owned_killed_and_reaped(self):
        with tempfile.TemporaryDirectory() as temp, self.owned_fixture(delay=.2) as owners:
            directory = self.D.new_directory(Path(temp))
            status, result = self.run_fixture([sys.executable, '-B', '-c', 'import time;time.sleep(30)'], directory, seconds=.05)
            self.assertEqual(status, 2)
            self.assertIn('STOPPED-DEADLINE', result['error'])
            self.assertEqual(len(owners), 1)
            with self.assertRaises(ProcessLookupError): os.kill(owners[0].worker_pid, 0)
            self.assertEqual(result['worker_pid'], owners[0].worker_pid)

    def test_deadline_during_registration_never_releases_worker_arithmetic(self):
        with tempfile.TemporaryDirectory() as temp, self.owned_fixture(delay=.2) as owners:
            marker = Path(temp)/'arithmetic'; directory = self.D.new_directory(Path(temp)/'runs')
            status, result = self.run_fixture([sys.executable, '-B', '-c', self.gated_fixture(marker)], directory, seconds=.05)
            self.assertEqual(status, 2)
            self.assertFalse(marker.exists())
            with self.assertRaises(ProcessLookupError): os.kill(owners[0].worker_pid, 0)

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
        with tempfile.TemporaryDirectory() as temp, self.owned_fixture(delay=.2) as owners:
            marker = Path(temp)/'arithmetic'; directory = self.D.new_directory(Path(temp)/'runs')
            with mock.patch.object(self.D.I, 'LAUNCH_S', .05):
                status, result = self.run_fixture([sys.executable, '-B', '-c', self.gated_fixture(marker)], directory, seconds=2)
            self.assertEqual(status, 2)
            self.assertIn('STOPPED-LAUNCH', result['error'])
            self.assertFalse(marker.exists())
            with self.assertRaises(ProcessLookupError): os.kill(owners[0].worker_pid, 0)

    def test_worker_exits_promptly_when_release_never_arrives_or_pipe_closes(self):
        for close in (False, True):
            with self.subTest(close=close), tempfile.TemporaryDirectory() as temp:
                marker = Path(temp)/'arithmetic'; end = time.monotonic()+.15
                owner = self.D.I.OwnedWorker(end)
                owner.start([sys.executable, '-B', '-c', self.gated_fixture(marker)], time.monotonic()+1, time.monotonic()+1.2)
                try:
                    if close: owner.close_fd('auth', 1); owner.close_fd('release', 1)
                    limit = time.monotonic()+1
                    while (owner.proof is None or owner.returncode is None or owner.streams) and time.monotonic()<limit:
                        owner.step(.005)
                    self.assertIsNotNone(owner.proof)
                    self.assertNotEqual(owner.proof['code'], 0)
                    self.assertFalse(marker.exists())
                    self.assertIn(b'LAUNCH', owner.buffers['stderr'])
                finally: owner.request_stop(); owner.close()

    def test_worker_exits_on_parent_death_even_with_another_writer_open(self):
        self.assertTrue(hasattr(self.D.I, 'wait_for_release'), 'worker release/liveness guard missing')
        with tempfile.TemporaryDirectory() as temp:
            marker = Path(temp)/'arithmetic'
            code = self.gated_fixture(marker)
            parent_code = ('import os,sys,time,json;from lab.runners import new1_identity_diag as I;'
                'end=time.monotonic()+4;owner=I.OwnedWorker(end);'
                f'owner.start([sys.executable,"-B","-c",{code!r}],end+1,end+1.2);'
                '\nwhile not owner.ready:owner.step(.005)\n'
                'keeper=os.fork();'
                '\nif keeper==0:\n os.close(1);os.close(2);time.sleep(.8);os._exit(0)\n'
                'print(json.dumps({"worker":owner.worker_pid,"keeper":keeper}),flush=True);time.sleep(.2);'
                'assert owner.proof is None,"worker exited before parent death"')
            parent = subprocess.Popen([sys.executable, '-B', '-c', parent_code], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = parent.communicate(timeout=2)
            self.assertEqual(parent.returncode, 0, stderr)
            value = json.loads(stdout); os.kill(value['keeper'], 0)
            limit = time.monotonic()+.5
            while time.monotonic()<limit:
                try: os.kill(value['worker'], 0)
                except ProcessLookupError: break
                time.sleep(.005)
            with self.assertRaises(ProcessLookupError): os.kill(value['worker'], 0)
            self.assertFalse(marker.exists())

    def test_keyboard_interrupt_during_popen_registration_cleans_without_release(self):
        previous = signal.getsignal(signal.SIGINT)
        signal.signal(signal.SIGINT, signal.default_int_handler)
        try:
            with tempfile.TemporaryDirectory() as temp, self.owned_fixture(interrupt=True) as owners:
                marker = Path(temp)/'arithmetic'; directory = self.D.new_directory(Path(temp)/'runs')
                status, result = self.run_fixture([sys.executable, '-B', '-c', self.gated_fixture(marker)], directory, seconds=2)
                self.assertEqual(status, 130)
                self.assertFalse(marker.exists())
                with self.assertRaises(ProcessLookupError): os.kill(owners[0].worker_pid, 0)
        finally: signal.signal(signal.SIGINT, previous)

    def test_stalled_launch_returns_within_bound_and_late_handle_cleans_once(self):
        with tempfile.TemporaryDirectory() as temp, self.owned_fixture(delay=2) as owners:
            marker = Path(temp)/'arithmetic'; directory = self.D.new_directory(Path(temp)/'runs')
            start = time.monotonic()
            with mock.patch.object(self.D.I, 'LAUNCH_S', .05), mock.patch.object(self.D.I, 'CLEANUP_S', .05):
                status, result = self.run_fixture([sys.executable, '-B', '-c', self.gated_fixture(marker)], directory, seconds=.8)
            self.assertEqual(status, 2)
            self.assertIn('STOPPED-LAUNCH', result['error'])
            self.assertLess(time.monotonic()-start, .3)
            self.assertFalse(marker.exists())
            self.assertEqual(owners[0].proof['pid'], owners[0].worker_pid)
            with self.assertRaises(ChildProcessError): os.waitpid(owners[0].pid, os.WNOHANG)
            with self.assertRaises(ProcessLookupError): os.kill(owners[0].worker_pid, 0)
            self.assertIsNotNone(owners[0].returncode)
            self.assertTrue(all(fd is None for pair in owners[0].channels.values() for fd in pair))
            self.assertFalse(owners[0].streams)

    def test_already_exited_unreleased_worker_is_reaped_without_group_signal(self):
        with tempfile.TemporaryDirectory() as temp, self.owned_fixture() as owners:
            marker = Path(temp)/'arithmetic'; directory = self.D.new_directory(Path(temp)/'runs')
            with mock.patch.object(self.D.I, 'release_frame', return_value=b'bad'):
                status, result = self.run_fixture([sys.executable, '-B', '-c', self.gated_fixture(marker)], directory, seconds=1)
            self.assertEqual(status, 2)
            self.assertEqual(owners[0].proof['code'], 2)
            self.assertEqual(owners[0].proof['kills'], 0, 'already exited worker must be reaped without signalling its group')
            self.assertFalse(marker.exists())
            with self.assertRaises(ProcessLookupError): os.kill(owners[0].worker_pid, 0)

    def test_released_worker_exits_on_parent_death_while_main_is_blocked(self):
        with tempfile.TemporaryDirectory() as temp:
            marker = Path(temp)/'released'
            worker = ('import time;from pathlib import Path;from lab.runners import new1_identity_diag as I;'
                'I.wait_for_release();' + f'Path({str(marker)!r}).write_text("released");time.sleep(5)')
            parent_code = ('import sys,time;from pathlib import Path;from lab.runners import new1_identity_diag as I;'
                'end=time.monotonic()+3;owner=I.OwnedWorker(end);'
                f'owner.start([sys.executable,"-B","-c",{worker!r}],end+1,end+1.2);'
                '\nwhile not owner.ready:owner.step(.005)\n'
                'owner.release();print(owner.worker_pid,flush=True);limit=time.monotonic()+1;'
                f'\nwhile not Path({str(marker)!r}).exists() and time.monotonic()<limit:time.sleep(.005)\n'
                f'assert Path({str(marker)!r}).exists(),"worker never received release"')
            parent = subprocess.Popen([sys.executable, '-B', '-c', parent_code], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = parent.communicate(timeout=2)
            self.assertEqual(parent.returncode, 0, stderr)
            self.assertEqual(marker.read_text(), 'released')
            pid = int(stdout); limit = time.monotonic()+.5
            while time.monotonic()<limit:
                try: os.kill(pid, 0)
                except ProcessLookupError: break
                time.sleep(.005)
            with self.assertRaises(ProcessLookupError): os.kill(pid, 0)

    def test_released_worker_has_independent_whole_deadline_while_main_is_blocked(self):
        end = time.monotonic()+.3; owner = self.D.I.OwnedWorker(end)
        code = ('import time;from lab.runners import new1_identity_diag as I;I.wait_for_release();'
                'print("RELEASED",flush=True);time.sleep(5)')
        owner.start([sys.executable, '-B', '-c', code], end, end+.2)
        try:
            while not owner.ready: owner.step(.005)
            owner.release()
            while owner.proof is None or owner.returncode is None or owner.streams: owner.step(.005)
            self.assertEqual(bytes(owner.buffers['stdout']).strip(), b'RELEASED')
            self.assertEqual(owner.proof['code'], -signal.SIGKILL)
            self.assertEqual(owner.proof['kills'], 1)
        finally: owner.close()

class AstraR2LaunchTests(unittest.TestCase):
    """Stdlib-only regressions for the four independently reproduced r2 schedules."""
    def setUp(self):
        self.I = importlib.import_module('lab.runners.new1_identity_diag')

    def supervised(self, code, directory, seconds):
        with contextlib.redirect_stderr(io.StringIO()):
            status = self.I.supervise([sys.executable, '-B', '-c', code], directory,
                preflight=lambda: None, admission=lambda: {'allowed': True},
                monitor=lambda pid: {'rss_gib': .01, 'process_count': 1}, seconds=seconds)
        return status, json.loads((directory/'result.json').read_text())

    def test_r2_interrupt_after_cleanup_starts_cannot_return_with_live_or_unreaped_child(self):
        owners = []; original = self.I.OwnedWorker.start; injected = []
        original_step = self.I.OwnedWorker.step
        previous = signal.getsignal(signal.SIGINT)
        signal.signal(signal.SIGINT, signal.default_int_handler)
        def capture(owner, *args):
            owners.append(owner); return original(owner, *args)
        def step(owner, seconds):
            original_step(owner, seconds)
            if not owner.stopping and owner.ready and owner.channels['release'][1] is None and owner.proof is None:
                raise self.I.G.Invalid('fixture released-worker cleanup')
        def trace(frame, event, arg):
            if frame.f_code.co_name == 'stop_and_close' and event == 'line':
                started = frame.f_locals.get('cleanup_started')
                pending = 'cleanup_complete' in frame.f_locals and not frame.f_locals['cleanup_complete']
                if (started or pending) and not injected:
                    injected.append(True); os.kill(os.getpid(), signal.SIGINT)
            return trace
        try:
            with tempfile.TemporaryDirectory() as temp, mock.patch.object(self.I.OwnedWorker, 'start', new=capture), \
                 mock.patch.object(self.I.OwnedWorker, 'step', new=step):
                directory = self.I.new_directory(Path(temp)/'runs')
                sys.settrace(trace)
                try: status, result = self.supervised('import time;time.sleep(30)', directory, 1)
                finally: sys.settrace(None)
                self.assertEqual(status, 2)
                self.assertTrue(injected, 'cleanup interrupt schedule was not exercised')
                self.assertIsNotNone(result['worker_pid'])
                with self.assertRaises(ProcessLookupError): os.kill(result['worker_pid'], 0)
                self.assertIsNotNone(owners[0].returncode, 'guardian was not reaped before terminal return')
                self.assertEqual(owners[0].proof['pid'], result['worker_pid'])
                with self.assertRaises(ChildProcessError): os.waitpid(owners[0].pid, os.WNOHANG)
        finally:
            sys.settrace(None); signal.signal(signal.SIGINT, previous)

    def test_r2_stalled_constructor_and_terminal_recording_fit_one_absolute_cap(self):
        owners = []; original = self.I.OwnedWorker.start
        def stalled(owner, *args):
            owners.append(owner); original(owner, *args); time.sleep(.7)
        with tempfile.TemporaryDirectory() as temp, mock.patch.object(self.I.OwnedWorker, 'start', new=stalled):
            directory = self.I.new_directory(Path(temp)/'runs'); start = time.monotonic()
            status, result = self.supervised('import time;time.sleep(30)', directory, .15)
            elapsed = time.monotonic()-start
            self.assertEqual(status, 2)
            self.assertLess(elapsed, .20, 'launch/teardown/terminal exceeded .15-s cap plus .05-s fixture scheduling allowance')
            self.assertIsNotNone(result['worker_pid'])
            with self.assertRaises(ProcessLookupError): os.kill(result['worker_pid'], 0)
            self.assertIsNotNone(owners[0].returncode, 'constructor-stalled guardian remained unreaped')
            self.assertEqual(owners[0].proof['pid'], result['worker_pid'])
            with self.assertRaises(ChildProcessError): os.waitpid(owners[0].pid, os.WNOHANG)

    def test_r2_both_actual_entries_refuse_duplicate_and_guessed_release(self):
        for module in ('new1_identity_diag', 'new1_construction_diag'):
            for frame in (b'RUN\n', b'RUN\nRUN\n'):
                with self.subTest(module=module, frame=frame):
                    read_fd, write_fd = os.pipe(); end = time.monotonic()+1
                    env = dict(os.environ, NEW1_IDENTITY_PARENT=str(os.getpid()),
                        NEW1_IDENTITY_RELEASE_FD=str(read_fd), NEW1_IDENTITY_RELEASE_BY=str(end),
                        NEW1_IDENTITY_DEADLINE=str(end))
                    code = (f'from lab.runners import {module} as D;'
                        'D.verify_launch=lambda *args:None;'
                        'D.measure=lambda:(print("ARITHMETIC",flush=True),{"status":"MEASURED"})[-1];'
                        'raise SystemExit(D.main(["--worker","--scope-sha","0"*64,"--source-sha","0"*64]))')
                    child = subprocess.Popen([sys.executable,'-B','-c',code],env=env,pass_fds=(read_fd,),
                        stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
                    os.close(read_fd)
                    try:
                        os.write(write_fd,frame);os.close(write_fd);write_fd=None
                        stdout,stderr=child.communicate(timeout=2)
                        self.assertEqual(child.returncode,2)
                        self.assertNotIn(b'ARITHMETIC',stdout)
                    finally:
                        if write_fd is not None:os.close(write_fd)
                        if child.poll() is None:os.killpg(child.pid,signal.SIGKILL)
                        child.communicate(timeout=1)

    def test_r2_parent_death_kills_released_gil_holding_worker_within_half_second(self):
        with tempfile.TemporaryDirectory() as temp:
            marker=Path(temp)/'entered_native'; directory=Path(temp)/'runs'; directory.mkdir()
            worker=('import ctypes,json,os;from pathlib import Path;from lab.runners import new1_identity_diag as I;'
                'I.wait_for_release();'
                f'Path({str(marker)!r}).write_text(json.dumps({{"pid":os.getpid()}}));'
                'ctypes.PyDLL(None).sleep(2)')
            parent_code=('import sys;from pathlib import Path;from lab.runners import new1_identity_diag as I;'
                f'raise SystemExit(I.supervise([sys.executable,"-B","-c",{worker!r}],Path({str(directory)!r}),'
                'preflight=lambda:None,admission=lambda:{"allowed":True},'
                'monitor=lambda pid:{"rss_gib":.01,"process_count":1},seconds=3))')
            parent=subprocess.Popen([sys.executable,'-B','-c',parent_code],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            pid=None
            try:
                limit=time.monotonic()+1
                while not marker.exists() and time.monotonic()<limit:time.sleep(.005)
                self.assertTrue(marker.exists(), 'legitimate release/native-entry positive control failed')
                pid=json.loads(marker.read_text())['pid'];time.sleep(.1)
                os.kill(pid,0);start=time.monotonic();parent.kill();parent.wait(timeout=1)
                limit=start+.5
                while time.monotonic()<limit:
                    try:os.kill(pid,0)
                    except ProcessLookupError:break
                    time.sleep(.005)
                with self.assertRaises(ProcessLookupError):os.kill(pid,0)
                self.assertLess(time.monotonic()-start,.5)
            finally:
                if parent.poll() is None:parent.kill()
                if pid is not None:
                    try:os.killpg(pid,signal.SIGKILL)
                    except ProcessLookupError:pass
                parent.communicate(timeout=3)


class OwnedLaunchControls(unittest.TestCase):
    def setUp(self): self.I = importlib.import_module('lab.runners.new1_identity_diag')
    supervised = AstraR2LaunchTests.supervised

    def test_locally_handled_callback_exception_cannot_disable_absolute_deadline(self):
        for callback in ('preflight', 'admission', 'monitor'):
            with self.subTest(callback=callback), tempfile.TemporaryDirectory() as temp:
                entered = []
                def blocked():
                    try: raise ValueError('fixture locally handled exception')
                    except ValueError:
                        entered.append(True)
                        time.sleep(2)
                    return {'allowed': True, 'rss_gib': .01, 'process_count': 1}
                options = {'preflight': lambda: None, 'admission': lambda: {'allowed': True},
                           'monitor': lambda pid: {'rss_gib': .01, 'process_count': 1}}
                options[callback] = (lambda pid: blocked()) if callback == 'monitor' else blocked
                directory = self.I.new_directory(Path(temp)); start = time.monotonic()
                with contextlib.redirect_stderr(io.StringIO()):
                    status = self.I.supervise([sys.executable, '-B', '-c', 'raise SystemExit(99)'],
                                             directory, seconds=.4, **options)
                elapsed = time.monotonic()-start
                self.assertTrue(entered, 'locally handled exception positive control missing')
                self.assertEqual(status, 2)
                self.assertLess(elapsed, .45, '.4-s original cap plus .05-s scheduling allowance exceeded')
                result = json.loads((directory/'result.json').read_text())
                self.assertIn('STOPPED-DEADLINE', result['error'])
                self.assertIsNone(result['worker_pid'])
                self.assertFalse(signal.getitimer(signal.ITIMER_REAL)[0])

    def test_callback_finally_cannot_outlive_absolute_end_after_first_alarm(self):
        for callback in ('preflight', 'admission', 'monitor'):
            with self.subTest(callback=callback), tempfile.TemporaryDirectory() as temp:
                entered = []
                def blocked():
                    try:
                        entered.append('body'); time.sleep(2)
                    finally:
                        entered.append('finally'); time.sleep(2)
                    return {'allowed': True, 'rss_gib': .01, 'process_count': 1}
                options = {'preflight': lambda: None, 'admission': lambda: {'allowed': True},
                           'monitor': lambda pid: {'rss_gib': .01, 'process_count': 1}}
                options[callback] = (lambda pid: blocked()) if callback == 'monitor' else blocked
                directory = self.I.new_directory(Path(temp)); start = time.monotonic()
                with contextlib.redirect_stderr(io.StringIO()):
                    status = self.I.supervise([sys.executable, '-B', '-c', 'raise SystemExit(99)'],
                                             directory, seconds=.4, **options)
                elapsed = time.monotonic()-start
                self.assertEqual(entered, ['body', 'finally'])
                self.assertEqual(status, 2)
                self.assertLess(elapsed, .45, 'active callback finally exceeded original .4-s cap')
                self.assertIn('STOPPED-DEADLINE', json.loads((directory/'result.json').read_text())['error'])

    def test_alarm_at_primary_exception_event_cannot_replace_error_before_context_exit(self):
        owners, injected, observations = [], [], []
        original = self.I.OwnedWorker.start
        def capture(owner, *args): owners.append(owner); return original(owner, *args)
        def monitor(pid):
            if pid:
                observations.append(pid)
                if len(observations) == 1: raise self.I.G.Invalid('fixture primary before context exit')
                return {'rss_gib': 11., 'process_count': 1}
            return {'rss_gib': .01, 'process_count': 1}
        def trace(frame, event, arg):
            if frame.f_code.co_name == 'supervise' and event == 'exception' and not injected and \
                    str(arg[1]) == 'fixture primary before context exit':
                injected.append(True); os.kill(os.getpid(), signal.SIGALRM)
            return trace
        with tempfile.TemporaryDirectory() as temp, mock.patch.object(self.I.OwnedWorker, 'start', new=capture):
            directory = self.I.new_directory(Path(temp)); sys.settrace(trace)
            try:
                with contextlib.redirect_stderr(io.StringIO()):
                    status = self.I.supervise([sys.executable, '-B', '-c', 'import time;time.sleep(30)'], directory,
                        preflight=lambda: None, admission=lambda: {'allowed': True}, monitor=monitor, seconds=.5)
            finally: sys.settrace(None)
            self.assertTrue(injected, 'primary exception-event alarm positive control missing')
            self.assertEqual(status, 2)
            result = json.loads((directory/'result.json').read_text())
            self.assertEqual(result['error'], 'fixture primary before context exit')
            self.assertEqual(owners[0].proof['kills'], 1)
            self.assertIsNotNone(owners[0].returncode)
            with self.assertRaises(ChildProcessError): os.waitpid(owners[0].pid, os.WNOHANG)
            with self.assertRaises(ProcessLookupError): os.kill(result['worker_pid'], 0)
            self.assertTrue(all(fd is None for pair in owners[0].channels.values() for fd in pair))

    def test_expired_pending_alarm_at_phase_entry_cannot_enter_stalled_launch(self):
        frames, delayed, launched = [], [], []
        def stalled(owner, *args): launched.append(True); time.sleep(1)
        def trace(frame, event, arg):
            owned_entry = frame.f_code.co_name == '__enter__' and \
                type(frame.f_locals.get('self')).__name__ == 'deadline_until'
            legacy_entry = frame.f_code.co_name == 'deadline_until'
            if event == 'line' and (owned_entry or legacy_entry) and frame not in frames and \
                    signal.getitimer(signal.ITIMER_REAL)[0] > 0 and \
                    signal.SIGALRM in signal.pthread_sigmask(signal.SIG_BLOCK, []):
                frames.append(frame)
                if len(frames) == 2:
                    delayed.append(True); time.sleep(.25)
            return trace
        with tempfile.TemporaryDirectory() as temp, mock.patch.object(self.I.OwnedWorker, 'start', new=stalled):
            directory = self.I.new_directory(Path(temp)); start = time.monotonic(); sys.settrace(trace)
            try:
                with contextlib.redirect_stderr(io.StringIO()):
                    status = self.I.supervise([sys.executable, '-B', '-c', 'raise SystemExit(99)'], directory,
                        preflight=lambda: None, admission=lambda: {'allowed': True},
                        monitor=lambda pid: {'rss_gib': .01, 'process_count': 1}, seconds=.4)
            finally: sys.settrace(None)
            self.assertTrue(delayed, 'armed and masked launch-entry positive control missing')
            self.assertEqual(status, 2)
            self.assertLess(time.monotonic()-start, .45)
            self.assertFalse(launched, 'expired launch entry reached the stalled constructor')
            self.assertIsNone(json.loads((directory/'result.json').read_text())['worker_pid'])

    def test_terminal_finally_at_absolute_end_fail_stops_without_terminal_or_python_return(self):
        for stderr in ('normal', 'closed', 'full'):
            with self.subTest(stderr=stderr), tempfile.TemporaryDirectory() as temp:
                directory = Path(temp)/'run'; directory.mkdir(); marker = Path(temp)/'terminal_entered'
                setup = 'os.close(2)\n' if stderr == 'closed' else ''
                if stderr == 'full':
                    setup = ('read_fd,write_fd=os.pipe()\nos.set_blocking(write_fd,False)\n'
                             'while True:\n'
                             ' try: os.write(write_fd,b"x"*4096)\n'
                             ' except BlockingIOError: break\n'
                             'os.set_blocking(write_fd,True)\nos.dup2(write_fd,2)\nos.close(write_fd)\n')
                code = ('import os,time;from pathlib import Path;from lab.runners import new1_identity_diag as I;\n'+setup+
                        'def blocked(out,value):\n'
                        f' Path({str(marker)!r}).write_text(str(time.monotonic()))\n'
                        ' try: time.sleep(2)\n'
                        ' finally: time.sleep(2)\n'
                        'I.Output.finish=blocked\n'
                        f'I.supervise([],Path({str(directory)!r}),preflight=lambda:None,admission=lambda:{{"allowed":False}},'
                        'monitor=lambda pid:{"rss_gib":.01,"process_count":1},seconds=.2)\n'
                        'print("SUPERVISOR-RETURNED")')
                try:
                    child = subprocess.run([sys.executable, '-B', '-c', code], capture_output=True, timeout=1)
                except subprocess.TimeoutExpired:
                    self.assertTrue(marker.exists(), 'terminal callback positive control missing')
                    self.fail('terminal finally survived original .2-s end beyond 1-s external fixture bound')
                self.assertTrue(marker.exists(), 'terminal callback positive control missing')
                self.assertLess(time.monotonic()-float(marker.read_text()), .3)
                self.assertEqual(child.returncode, 2)
                self.assertNotIn(b'SUPERVISOR-RETURNED', child.stdout)
                self.assertFalse((directory/'result.json').exists())
                events = [json.loads(line) for line in (directory/'receipt.jsonl').read_text().splitlines()]
                self.assertNotIn('terminal', [event['kind'] for event in events])

    def test_refused_admission_reporting_with_full_or_closed_stderr_stays_inside_original_end(self):
        for stderr in ('full', 'closed'):
            with self.subTest(stderr=stderr), tempfile.TemporaryDirectory() as temp:
                directory = Path(temp)/'run'; directory.mkdir(); marker = Path(temp)/'started'
                setup = 'os.close(2)\n'
                if stderr == 'full':
                    setup = ('read_fd,write_fd=os.pipe()\nos.set_blocking(write_fd,False)\n'
                             'while True:\n'
                             ' try: os.write(write_fd,b"x"*4096)\n'
                             ' except BlockingIOError: break\n'
                             'os.set_blocking(write_fd,True)\nos.dup2(write_fd,2)\nos.close(write_fd)\n')
                code = ('import os,time;from pathlib import Path;from lab.runners import new1_identity_diag as I;\n'+setup+
                        f'Path({str(marker)!r}).write_text(str(time.monotonic()))\n'
                        f'status=I.supervise([],Path({str(directory)!r}),preflight=lambda:None,admission=lambda:{{"allowed":False}},'
                        'monitor=lambda pid:{"rss_gib":.01,"process_count":1},seconds=.2)\n'
                        'print("SUPERVISOR-RETURNED");raise SystemExit(status)')
                try: child = subprocess.run([sys.executable, '-B', '-c', code], capture_output=True, timeout=1)
                except subprocess.TimeoutExpired:
                    self.assertTrue(marker.exists(), 'full-stderr admission positive control missing')
                    self.fail('refused-admission reporting escaped the original .2-s end')
                self.assertTrue(marker.exists())
                self.assertLess(time.monotonic()-float(marker.read_text()), .3)
                self.assertEqual(child.returncode, 2)
                self.assertNotIn(b'SUPERVISOR-RETURNED', child.stdout)
                result = json.loads((directory/'result.json').read_text())
                self.assertEqual(result['status'], 'INVALID')
                self.assertIn('INVALID-ADMISSION', result['error'])
                self.assertIsNone(result['worker_pid'])

    def test_sigint_at_outer_exception_transition_cannot_escape_reaping(self):
        owners, injected = [], []
        original = self.I.OwnedWorker.start
        def capture(owner, *args): owners.append(owner); return original(owner, *args)
        def monitor(pid):
            if pid: raise self.I.G.Invalid('fixture primary error')
            return {'rss_gib': .01, 'process_count': 1}
        def trace(frame, event, arg):
            if frame.f_code.co_name == 'supervise' and event == 'line' and not injected and \
                    'error' in frame.f_locals and str(frame.f_locals['error']) == 'fixture primary error':
                injected.append(True); os.kill(os.getpid(), signal.SIGINT)
            return trace
        previous = signal.getsignal(signal.SIGINT); signal.signal(signal.SIGINT, signal.default_int_handler)
        try:
            with tempfile.TemporaryDirectory() as temp, mock.patch.object(self.I.OwnedWorker, 'start', new=capture):
                directory = self.I.new_directory(Path(temp)); sys.settrace(trace)
                try:
                    with contextlib.redirect_stderr(io.StringIO()):
                        status = self.I.supervise([sys.executable, '-B', '-c', 'import time;time.sleep(30)'], directory,
                            preflight=lambda:None, admission=lambda:{'allowed':True}, monitor=monitor, seconds=.5)
                except KeyboardInterrupt: self.fail('repeated SIGINT escaped before confirmed reaping')
                finally: sys.settrace(None)
                self.assertTrue(injected)
                self.assertEqual(status, 2)
                result = json.loads((directory/'result.json').read_text())
                self.assertEqual(result['error'], 'fixture primary error')
                self.assertEqual(owners[0].proof['kills'], 1)
                self.assertIsNotNone(owners[0].returncode)
                with self.assertRaises(ChildProcessError): os.waitpid(owners[0].pid, os.WNOHANG)
                with self.assertRaises(ProcessLookupError): os.kill(result['worker_pid'], 0)
                self.assertTrue(all(fd is None for pair in owners[0].channels.values() for fd in pair))
        finally:
            sys.settrace(None); signal.signal(signal.SIGINT, previous)
            for owner in owners:
                if owner.returncode is None or owner.proof is None:
                    owner.request_stop(); end = time.monotonic()+1
                    while (owner.returncode is None or owner.proof is None) and time.monotonic()<end: owner.step(.005)
                    owner.close()

    def test_repeated_alarm_at_deadline_exit_preserves_primary_and_reaping(self):
        owners, injected = [], []
        original = self.I.OwnedWorker.start
        def capture(owner, *args): owners.append(owner); return original(owner, *args)
        def monitor(pid):
            if pid: raise self.I.G.Invalid('fixture deadline-transition primary')
            return {'rss_gib': .01, 'process_count': 1}
        def trace(frame, event, arg):
            if event == 'line' and owners and not injected:
                legacy = frame.f_code.co_name == 'hard_deadline' and frame.f_lineno == 126
                owned = frame.f_code.co_name == '__exit__' and frame.f_locals.get('clearing', False)
                if legacy or owned:
                    injected.append(True)
                    for sig in (signal.SIGINT, signal.SIGALRM, signal.SIGALRM): os.kill(os.getpid(), sig)
            return trace
        with tempfile.TemporaryDirectory() as temp, mock.patch.object(self.I.OwnedWorker, 'start', new=capture):
            directory = self.I.new_directory(Path(temp)); sys.settrace(trace)
            try:
                with contextlib.redirect_stderr(io.StringIO()):
                    status = self.I.supervise([sys.executable, '-B', '-c', 'import time;time.sleep(30)'], directory,
                        preflight=lambda:None, admission=lambda:{'allowed':True}, monitor=monitor, seconds=.5)
            finally: sys.settrace(None)
            self.assertTrue(injected)
            self.assertEqual(status, 2)
            self.assertEqual(json.loads((directory/'result.json').read_text())['error'], 'fixture deadline-transition primary')
            self.assertIsNotNone(owners[0].returncode)
            self.assertEqual(owners[0].proof['kills'], 1)
            with self.assertRaises(ChildProcessError): os.waitpid(owners[0].pid, os.WNOHANG)
            with self.assertRaises(ProcessLookupError): os.kill(owners[0].worker_pid, 0)

    def test_authenticated_duplicate_trailing_wrong_secret_and_missing_eof_refuse_both_entries(self):
        self.assertTrue(hasattr(self.I, 'OwnedWorker'), 'independent ownership API missing')
        for module in ('new1_identity_diag', 'new1_construction_diag'):
            for kind in ('valid', 'duplicate', 'trailing', 'wrong_secret', 'missing_eof'):
                with self.subTest(module=module, kind=kind), tempfile.TemporaryDirectory() as temp:
                    directory = self.I.new_directory(Path(temp))
                    marker = Path(temp)/'arithmetic'
                    code = (f'from lab.runners import {module} as D;from pathlib import Path;D.verify_launch=lambda *args:None;'
                            f'D.measure=lambda:(Path({str(marker)!r}).write_text("reached"),{{"status":"MEASURED"}})[-1];'
                            'raise SystemExit(D.main(["--worker","--scope-sha","0"*64,"--source-sha","0"*64]))')
                    original_frame, original_close = self.I.release_frame, self.I.OwnedWorker.close_fd
                    def frame(secret):
                        data = original_frame(secret)
                        return data*2 if kind == 'duplicate' else data+b'x' if kind == 'trailing' else \
                            b'RUN '+b'0'*64+b'\n' if kind == 'wrong_secret' else data
                    def close(owner, key, index):
                        if kind == 'missing_eof' and key == 'release' and index == 1 and not owner.stopping: return
                        return original_close(owner, key, index)
                    with mock.patch.object(self.I, 'release_frame', new=frame), \
                         mock.patch.object(self.I.OwnedWorker, 'close_fd', new=close):
                        status, result = self.supervised(code, directory, .5)
                    if kind == 'valid':
                        self.assertEqual(status, 0); self.assertEqual(result['status'], 'MEASURED')
                        self.assertTrue(marker.exists())
                    else:
                        self.assertEqual(status, 2)
                        self.assertEqual(result['status'], 'INVALID')
                        self.assertFalse(marker.exists())
                    with self.assertRaises(ProcessLookupError): os.kill(result['worker_pid'], 0)

    def test_repeated_sigint_and_sigalrm_during_teardown_preserve_primary_and_reap(self):
        self.assertTrue(hasattr(self.I, 'OwnedWorker'), 'independent ownership API missing')
        owners = []; injected = []; original = self.I.OwnedWorker.start
        original_stop = self.I.OwnedWorker.request_stop
        def capture(owner, *args): owners.append(owner); return original(owner, *args)
        def stop(owner):
            if not injected:
                injected.append(True)
                for sig in (signal.SIGINT, signal.SIGALRM, signal.SIGINT, signal.SIGALRM): os.kill(os.getpid(), sig)
            return original_stop(owner)
        with tempfile.TemporaryDirectory() as temp, mock.patch.object(self.I.OwnedWorker, 'start', new=capture), \
             mock.patch.object(self.I.OwnedWorker, 'request_stop', new=stop):
            directory = self.I.new_directory(Path(temp))
            status, result = self.supervised('import time;time.sleep(30)', directory, .2)
        self.assertTrue(injected)
        self.assertEqual(status, 2)
        self.assertIn('STOPPED-DEADLINE', result['error'])
        self.assertEqual(owners[0].proof['kills'], 1)
        self.assertIsNotNone(owners[0].returncode)
        with self.assertRaises(ChildProcessError): os.waitpid(owners[0].pid, os.WNOHANG)
        with self.assertRaises(ProcessLookupError): os.kill(result['worker_pid'], 0)
        self.assertTrue(all(fd is None for pair in owners[0].channels.values() for fd in pair))

    def test_gil_holding_native_worker_is_killed_and_reaped_within_original_deadline(self):
        with tempfile.TemporaryDirectory() as temp:
            marker = Path(temp)/'native'; directory = self.I.new_directory(Path(temp)/'runs')
            code = ('import ctypes;from pathlib import Path;from lab.runners import new1_identity_diag as I;I.wait_for_release();'
                    f'Path({str(marker)!r}).write_text("entered");ctypes.PyDLL(None).sleep(2)')
            start = time.monotonic(); status, result = self.supervised(code, directory, .8)
            self.assertTrue(marker.exists(), 'authenticated native-entry positive control missing: '+str(result))
            self.assertEqual(status, 2)
            self.assertLess(time.monotonic()-start, .85)
            with self.assertRaises(ProcessLookupError): os.kill(result['worker_pid'], 0)

    def test_sigint_at_raw_fork_return_retains_pid_and_all_descriptors(self):
        self.assertTrue(hasattr(self.I, 'OwnedWorker'), 'independent ownership API missing')
        root = os.getpid(); original = os.fork; owners = []; start = self.I.OwnedWorker.start
        def capture(owner, *args): owners.append(owner); return start(owner, *args)
        def interrupted():
            pid = original()
            if os.getpid() == root and pid > 0: os.kill(root, signal.SIGINT)
            return pid
        previous = signal.getsignal(signal.SIGINT); signal.signal(signal.SIGINT, signal.default_int_handler)
        try:
            with tempfile.TemporaryDirectory() as temp, mock.patch.object(self.I.os, 'fork', new=interrupted), \
                 mock.patch.object(self.I.OwnedWorker, 'start', new=capture):
                status, result = self.supervised('import time;time.sleep(30)', self.I.new_directory(Path(temp)), .5)
            self.assertEqual(status, 130)
            self.assertIsNotNone(owners[0].returncode)
            self.assertEqual(owners[0].proof['pid'], result['worker_pid'])
            with self.assertRaises(ChildProcessError): os.waitpid(owners[0].pid, os.WNOHANG)
            with self.assertRaises(ProcessLookupError): os.kill(result['worker_pid'], 0)
            self.assertTrue(all(fd is None for pair in owners[0].channels.values() for fd in pair))
        finally: signal.signal(signal.SIGINT, previous)

    def test_worker_stream_memory_bound_cancels_and_reaps(self):
        with tempfile.TemporaryDirectory() as temp:
            status, result = self.supervised('import os;os.write(1,b"x"*600000)', self.I.new_directory(Path(temp)), .5)
            self.assertEqual(status, 2)
            self.assertIn('STOPPED-DISK', result['error'])
            with self.assertRaises(ProcessLookupError): os.kill(result['worker_pid'], 0)


def _fix4_observed_child(trace_path, schedule):
    """Run real forks under an external observer, retaining native fail-stop exits."""
    import ctypes
    import errno
    I = importlib.import_module('lab.runners.new1_identity_diag')
    trace_path = Path(trace_path)
    role, owners, exceptions = 'parent', [], []
    raw_fork, raw_exit, raw_write = os.fork, os._exit, os.write
    raw_wait, raw_kill, raw_group, raw_setsid = os.waitpid, os.kill, os.killpg, os.setsid
    raw_init, raw_start, raw_supervise = I.OwnedWorker.__init__, I.OwnedWorker.start, I.supervise

    def emit(event, **value):
        fd = os.open(trace_path, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
        try:
            raw_write(fd, (json.dumps(dict(event=event, pid=os.getpid(), role=role,
                monotonic=time.monotonic(), **value), default=str)+'\n').encode())
        finally: os.close(fd)

    def init(owner, *args):
        raw_init(owner, *args); owners.append(owner)

    def fork():
        nonlocal role
        former = role; pid = raw_fork()
        if pid == 0: role = 'guardian' if former == 'parent' else 'worker'
        emit('fork', child=pid, former=former)
        return pid

    def wait(pid, flags):
        if role == 'guardian' and schedule == 'already_exited': flags = 0
        result = raw_wait(pid, flags)
        if result[0]: emit('reaped', child=result[0], code=os.waitstatus_to_exitcode(result[1]))
        elif role == 'guardian': emit('wait-live', child=pid)
        return result

    def kill(pid, sig):
        emit('pid-probe' if sig == 0 else 'pid-signal', child=pid, signal=sig)
        return raw_kill(pid, sig)

    def group(pid, sig):
        if role == 'guardian' and schedule in ('group_denied', 'live', 'exit_between'):
            if schedule == 'exit_between':
                (trace_path.parent/'exit-request').touch()
                libc = ctypes.CDLL(None, use_errno=True)
                info = ctypes.create_string_buffer(128)
                rc = libc.waitid(1, pid, ctypes.byref(info), os.WEXITED | os.WNOWAIT)
                if rc: raise OSError(ctypes.get_errno(), 'fixture waitid(WNOWAIT) failed')
                emit('exited-before-signal', child=pid)
            else:
                raw_kill(pid, 0); emit('live-before-signal', child=pid)
            emit('group-refused', child=pid)
            raise PermissionError(errno.EPERM, 'FIX4 captured guardian group-signal refusal')
        return raw_group(pid, sig)

    def setsid():
        if role == 'guardian' and schedule == 'setup_exception':
            raise RuntimeError('FIX4 guardian setup exception before protected try')
        return raw_setsid()

    def write(fd, data):
        if role == 'guardian' and data.startswith(b'{"event": "reaped"') and schedule == 'receipt_exception':
            emit('receipt-send-refused')
            raise OSError(errno.EIO, 'FIX4 final reaping receipt send exception')
        return raw_write(fd, data)

    def exiting(code):
        frame = sys._getframe(1); stack = []
        cursor = frame
        while cursor is not None:
            local = cursor.f_locals
            stack.append(dict(function=cursor.f_code.co_name, line=cursor.f_lineno,
                file=cursor.f_code.co_filename,
                errors={k:repr(local[k]) for k in ('error','failure','cleanup_error','recording_error') if k in local},
                remaining_s=local['end']-time.monotonic() if isinstance(local.get('end'), (float,int)) else None))
            cursor = cursor.f_back
        emit('_exit', code=code, stack=stack, exceptions=exceptions[-24:],
             ownership=[dict(guardian=o.pid, worker=o.worker_pid, proof=o.proof,
                             guardian_code=o.returncode, channels=o.channels, streams=list(o.streams)) for o in owners])
        raw_exit(code)

    def tracing(frame, event, arg):
        if frame.f_code.co_filename != I.__file__: return None
        if event == 'exception':
            kind, error, _ = arg
            exceptions.append(dict(type=kind.__name__, error=str(error), function=frame.f_code.co_name,
                                   line=frame.f_lineno))
            if role == 'guardian' and frame.f_code.co_name == 'supervise':
                emit('inherited-supervisor', exception=repr(error))
        return tracing

    def start(owner, command, *args):
        if schedule == 'already_exited': command = [sys.executable, '-B', '-c', 'raise SystemExit(2)']
        elif schedule == 'live': command = [sys.executable, '-B', '-c', 'import time;time.sleep(.2)']
        elif schedule == 'group_denied':
            command = [*command[:-1], 'import time;time.sleep(.2);'+command[-1]]
        elif schedule == 'exit_between':
            exit_path = trace_path.parent/'exit-request'
            code = ('import time;from pathlib import Path;'
                    f'p=Path({str(exit_path)!r});'
                    '\nwhile not p.exists():time.sleep(.001)\nraise SystemExit(2)')
            command = [sys.executable, '-B', '-c', code]
        raw_start(owner, command, *args)
        emit('start-returned')
        if schedule in ('setup_exception','receipt_exception'): time.sleep(2)

    def snapshot(owner):
        try: raw_wait(owner.pid, os.WNOHANG)
        except ChildProcessError: guardian_reaped = True
        else: guardian_reaped = False
        worker_absent = owner.worker_pid is None
        if owner.worker_pid is not None:
            try: raw_kill(owner.worker_pid, 0)
            except ProcessLookupError: worker_absent = True
        return dict(guardian=owner.pid, worker=owner.worker_pid, proof=owner.proof,
                    guardian_code=owner.returncode, guardian_reaped=guardian_reaped,
                    worker_absent=worker_absent,
                    descriptors_closed=all(fd is None for pair in owner.channels.values() for fd in pair),
                    streams_closed=not owner.streams)

    class BrokenStderr:
        def write(self, data): raise OSError('FIX4 terminal stderr failure')
        def flush(self): pass

    def supervise(*args, **kwargs):
        if schedule == 'terminal_failure':
            with contextlib.redirect_stderr(BrokenStderr()): status = raw_supervise(*args, **kwargs)
        else: status = raw_supervise(*args, **kwargs)
        emit('supervision-return', status=status, ownership=[snapshot(o) for o in owners])
        return status

    def finish(*args): raise OSError('FIX4 terminal output failure')

    I.OwnedWorker.__init__, I.OwnedWorker.start, I.supervise = init, start, supervise
    os.fork, os.waitpid, os.kill, os.killpg, os.setsid, os.write, os._exit = fork, wait, kill, group, setsid, write, exiting
    if schedule == 'terminal_failure': I.Output.finish = finish
    sys.settrace(tracing)
    emit('fixture-start', schedule=schedule)
    if schedule in ('setup_exception','receipt_exception'):
        with mock.patch.object(I, 'LAUNCH_S', .05), mock.patch.object(I, 'CLEANUP_S', .05), contextlib.redirect_stderr(io.StringIO()):
            status = I.supervise([sys.executable,'-B','-c','import time;time.sleep(30)'],
                I.new_directory(trace_path.parent/'runs'), preflight=lambda:None,
                admission=lambda:{'allowed':True}, monitor=lambda pid:{'rss_gib':.01,'process_count':1}, seconds=.8)
        emit('fixture-complete', status=status)
        return 0
    target = 'tests.test_new1_construction_diag.ConstructionDiagnosticTests.test_stalled_launch_returns_within_bound_and_late_handle_cleans_once'
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromName(target))
    emit('unittest-complete', tests=result.testsRun, failures=len(result.failures), errors=len(result.errors))
    return 0 if result.wasSuccessful() else 1


class Fix4LifecycleTests(unittest.TestCase):
    def observed(self, schedule):
        with tempfile.TemporaryDirectory() as temp:
            trace = Path(temp)/'trace.jsonl'
            code = ('import sys;from tests.test_new1_construction_diag import _fix4_observed_child;'
                    'sys.exit(_fix4_observed_child(sys.argv[1],sys.argv[2]))')
            command = [sys.executable,'-B','-W','error::ResourceWarning','-c',code,str(trace),schedule]
            proc = subprocess.run(command, capture_output=True, text=True, timeout=8)
            events = [json.loads(line) for line in trace.read_text().splitlines()]
            record = dict(schedule=schedule, native_exit=proc.returncode, command=command,
                          events=events, stdout=proc.stdout, stderr=proc.stderr)
            if os.environ.get('NEW1_FIX4_RECEIPTS'):
                path = Path(os.environ['NEW1_FIX4_RECEIPTS'])/(schedule+'_'+str(time.time_ns())+'.json')
                path.write_text(json.dumps(record,indent=2)+'\n')
        self.assertNotIn('ResourceWarning', proc.stderr, record)
        return record

    def ownership(self, record):
        self.assertEqual(record['native_exit'], 0, record)
        completed = [e for e in record['events'] if e['event']=='unittest-complete']
        self.assertEqual(len(completed), 1, record)
        self.assertEqual((completed[0]['tests'],completed[0]['failures'],completed[0]['errors']), (1,0,0), record)
        returned = [e for e in record['events'] if e['event']=='supervision-return']
        self.assertEqual(len(returned), 1, record)
        self.assertEqual(returned[0]['status'], 2, record)
        self.assertEqual(len(returned[0]['ownership']), 1, record)
        owner = returned[0]['ownership'][0]
        for key in ('guardian_reaped','worker_absent','descriptors_closed','streams_closed'):
            self.assertIs(owner[key], True, record)
        self.assertIsNotNone(owner['guardian_code'], record)
        self.assertEqual(owner['proof']['pid'], owner['worker'], record)
        reaps = [e for e in record['events'] if e['event']=='reaped']
        self.assertEqual([(e['role'],e['child']) for e in reaps],
                         [('guardian',owner['worker']),('parent',owner['guardian'])], record)
        return owner['proof']

    def test_fix4_c1_already_exited_is_reaped_without_a_signal_before_return(self):
        record = self.observed('already_exited'); proof = self.ownership(record)
        self.assertEqual((proof['kills'],proof['code']), (0,2), record)
        self.assertFalse(any(e['event'] in ('pid-signal','group-refused') for e in record['events']), record)

    def test_fix4_c1_live_worker_is_killed_and_reaped_before_return(self):
        record = self.observed('live'); proof = self.ownership(record)
        self.assertEqual((proof['kills'],proof['code']), (1,-signal.SIGKILL), record)
        self.assertTrue(any(e['event']=='live-before-signal' for e in record['events']), record)

    def test_fix4_c1_exit_between_wait_and_kill_retains_actual_exit_status(self):
        record = self.observed('exit_between'); proof = self.ownership(record)
        self.assertEqual((proof['kills'],proof['code']), (1,2), record)
        ordered = [e['event'] for e in record['events']]
        self.assertLess(ordered.index('wait-live'), ordered.index('exited-before-signal'), record)
        self.assertLess(ordered.index('exited-before-signal'), ordered.index('group-refused'), record)

    def test_fix4_c2_guardian_setup_exception_cannot_unwind_into_supervisor(self):
        record = self.observed('setup_exception')
        self.assertFalse(any(e['event']=='inherited-supervisor' for e in record['events']), record)
        self.assertFalse(any(e['event']=='start-returned' and e['role']=='guardian' for e in record['events']), record)
        self.assertEqual(record['native_exit'], 0, record)
        self.assertTrue(any(e['event']=='fixture-complete' and e['status']==2 for e in record['events']), record)
        exits = [e for e in record['events'] if e['event']=='_exit' and e['role']=='guardian']
        self.assertEqual(len(exits), 1, record)
        self.assertEqual(exits[0]['code'], 2, record)

    def test_fix4_c2_final_send_exception_retains_reaping_and_child_boundary(self):
        record = self.observed('receipt_exception')
        self.assertTrue(any(e['event']=='receipt-send-refused' for e in record['events']), record)
        self.assertFalse(any(e['event']=='inherited-supervisor' for e in record['events']), record)
        self.assertEqual(record['native_exit'], 2, record)
        self.assertEqual(len([e for e in record['events'] if e['event']=='reaped' and e['role']=='guardian']), 1, record)
        self.assertFalse(any(e['event'] in ('supervision-return','fixture-complete') for e in record['events']), record)
        parent = [e for e in record['events'] if e['event']=='_exit' and e['role']=='parent']
        self.assertEqual(len(parent), 1, record)
        self.assertIn('guardian exit lacks worker reaping proof', str(parent[0]), record)

    def test_fix4_c3_captured_exit_schedule_returns_but_true_failures_fail_stop(self):
        self.ownership(self.observed('group_denied'))
        for schedule, cause in (('receipt_exception','guardian exit lacks worker reaping proof'),
                                ('terminal_failure','FIX4 terminal stderr failure')):
            with self.subTest(schedule=schedule):
                record = self.observed(schedule)
                self.assertEqual(record['native_exit'], 2, record)
                self.assertFalse(any(e['event'] in ('supervision-return','fixture-complete','unittest-complete') for e in record['events']), record)
                exits = [e for e in record['events'] if e['event']=='_exit' and e['role']=='parent']
                self.assertEqual(len(exits), 1, record)
                self.assertEqual(exits[0]['code'], 2, record)
                self.assertIn(cause, str(exits[0]), record)
                self.assertGreater(exits[0]['stack'][0]['remaining_s'], 0, record)


if __name__ == '__main__': unittest.main()


class Fix5ParentEntryTests(unittest.TestCase):
    def refusal(self, blocked):
        from tests.test_new1_identity_diag import _fix5_isolated, _fix5_refusal
        if _fix5_isolated(self): return
        from lab.runners import new1_construction_diag as D
        _fix5_refusal(self, D, blocked)

    def test_fix5_c2_construction_main_sigalrm_refuses_before_file_work(self): self.refusal([signal.SIGALRM])
    def test_fix5_c2_construction_main_sigint_refuses_before_file_work(self): self.refusal([signal.SIGINT])
    def test_fix5_c2_construction_main_both_refuses_before_file_work(self): self.refusal([signal.SIGINT, signal.SIGALRM])
