"""Synthetic CPU fixtures only; no real covariance, capture or admission."""
import hashlib
import gc
import importlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest
import warnings
from unittest import mock


class IdentityDiagnosticTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(Path('tools/new1_identity_diag.py').is_file(),
                        'the identity diagnostic has not been built')
        self.D = importlib.import_module('tools.new1_identity_diag')
        import numpy as np
        import torch
        self.np, self.t = np, torch
        torch.set_num_threads(1)
        self.tmp = tempfile.TemporaryDirectory(dir='/private/tmp')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def test_numpy_path_uses_fp32_ufunc_division(self):
        moment = self.np.array([[6.33, 1.01], [1.01, 9.99]], dtype=self.np.float32)
        count = self.np.array(7, dtype=self.np.int64)
        got = self.D.normalization_paths(moment, count)
        expected = self.np.divide(moment, count, dtype=self.np.float32)
        self.assertEqual(got['A'].numpy().tobytes(), expected.tobytes())
        self.assertEqual(got['A'].dtype, self.t.float32)

    def test_torch_path_uses_loaded_fp32_tensor_and_python_integer(self):
        moment = self.np.array([[6.33, 1.01], [1.01, 9.99]], dtype=self.np.float32)
        got = self.D.normalization_paths(moment, self.np.array(7, dtype=self.np.int64))
        expected = self.t.from_numpy(moment.copy()) / 7
        self.assertEqual(got['B'].numpy().tobytes(), expected.numpy().tobytes())
        self.assertEqual(got['B'].dtype, self.t.float32)
        self.assertEqual(got['B'].device.type, 'cpu')

    def test_normalizations_leave_raw_moment_and_count_unchanged(self):
        moment = self.np.eye(3, dtype=self.np.float32)
        count = self.np.array(100000, dtype=self.np.int64)
        before = moment.tobytes(), count.tobytes()
        self.D.normalization_paths(moment, count)
        self.assertEqual((moment.tobytes(), count.tobytes()), before)

    def test_invalid_normalization_operands_fail_closed(self):
        n = self.np
        pairs = [(n.eye(2, dtype=n.float64), n.array(2, dtype=n.int64)),
                 (n.ones((2, 3), dtype=n.float32), n.array(2, dtype=n.int64)),
                 (n.eye(2, dtype=n.float32), n.array(0, dtype=n.int64)),
                 (n.eye(2, dtype=n.float32), n.array(-1, dtype=n.int64)),
                 (n.eye(2, dtype=n.float32), n.array(2., dtype=n.float32)),
                 (n.eye(2, dtype=n.float32), n.array([2], dtype=n.int64)),
                 (n.full((2, 2), n.nan, dtype=n.float32), n.array(2, dtype=n.int64))]
        for moment, count in pairs:
            with self.subTest(shape=moment.shape, count=count), self.assertRaises(self.D.G.Invalid):
                self.D.normalization_paths(moment, count)

    def test_normalized_hashes_and_blocked_maximum_difference(self):
        A = self.t.tensor([[1., 2.], [3., 4.]], dtype=self.t.float32)
        B = self.t.tensor([[1., 2.], [3.25, 4.]], dtype=self.t.float32)
        self.assertEqual(self.D.G.tensor_sha(A), hashlib.sha256(A.numpy().tobytes()).hexdigest())
        self.assertEqual(self.D.maximum_difference(A, B), .25)
        self.assertEqual(self.D.maximum_difference(A, A), 0.)

    def test_relative_probe_error_uses_captured_norm_and_double_residual(self):
        got = self.D.probe_metrics(self.t.tensor([3., 4.]), self.t.tensor([0., 4.]))
        self.assertEqual(got['relative_error'], .75)
        self.assertEqual(got['absolute_l2_residual'], 3.)
        self.assertEqual(got['max_absolute_residual'], 3.)
        self.assertEqual(got['actual_l2_norm'], 5.)
        self.assertEqual(got['captured_l2_norm'], 4.)
        self.assertEqual(got['match'], 'NO-MATCH')

    def test_one_e_minus_six_is_inclusive_and_larger_error_is_no_match(self):
        ref = self.t.tensor([1e6, 0.], dtype=self.t.float64)
        at = self.D.probe_metrics(self.t.tensor([1e6, 1.], dtype=self.t.float64), ref)
        above = self.D.probe_metrics(self.t.tensor([1e6, 1.001], dtype=self.t.float64), ref)
        self.assertEqual(at['relative_error'], 1e-6)
        self.assertEqual(at['match'], 'MATCH')
        self.assertEqual(above['match'], 'NO-MATCH')

    def test_zero_or_nonfinite_probe_reference_is_invalid(self):
        for ref in (self.t.zeros(2), self.t.tensor([float('nan'), 1.])):
            with self.assertRaises(self.D.G.Invalid):
                self.D.probe_metrics(self.t.ones(2), ref)

    def test_native_recipe_reports_all_four_probes_even_on_exact_sha(self):
        t = self.t
        C = t.diag(t.tensor([.01, .004, .002], dtype=t.float32))
        expected = t.diag(t.tensor([0., 1., 1.]))
        digest = hashlib.sha256(expected.numpy().tobytes()).hexdigest()
        probes = [expected @ t.randn(3, generator=t.Generator().manual_seed(j)) for j in range(4)]
        result = self.D.path_report(C, 2, digest, probes)
        self.assertEqual(result['excluded_count'], 1)
        self.assertEqual(result['allowed_count'], 2)
        self.assertEqual(result['projector_sha256'], digest)
        self.assertEqual([p['seed'] for p in result['probes']], [0, 1, 2, 3])
        self.assertEqual([p['relative_error'] for p in result['probes']], [0.] * 4)
        self.assertTrue(result['matches_capture_gate'])

    def test_sha_mismatch_can_match_by_probes_but_count_mismatch_cannot(self):
        t = self.t
        C = t.diag(t.tensor([.01, .004, .002]))
        P = t.diag(t.tensor([0., 1., 1.]))
        probes = [P @ t.randn(3, generator=t.Generator().manual_seed(j)) for j in range(4)]
        result = self.D.path_report(C, 2, '0' * 64, probes)
        self.assertFalse(result['projector_sha_matches'])
        self.assertTrue(result['all_probes_match_1e6'])
        self.assertTrue(result['matches_capture_gate'])
        bad_count = self.D.path_report(C, 1, '0' * 64, probes)
        self.assertFalse(bad_count['matches_capture_gate'])

    def test_failed_probe_is_reported_without_short_circuit(self):
        t = self.t
        C = t.diag(t.tensor([.01, .004, .002]))
        P = t.diag(t.tensor([0., 1., 1.]))
        probes = [P @ t.randn(3, generator=t.Generator().manual_seed(j)) for j in range(4)]
        probes[1][1] += .1
        result = self.D.path_report(C, 2, '0' * 64, probes)
        self.assertEqual(len(result['probes']), 4)
        self.assertEqual(result['probes'][1]['match'], 'NO-MATCH')
        self.assertFalse(result['matches_capture_gate'])

    def test_pin_mismatch_aborts_and_valid_pin_can_be_consumed(self):
        path = self.root / 'fixture.txt'
        path.write_bytes(b'fixture')
        pin = hashlib.sha256(b'fixture').hexdigest()
        self.D.verify_pins(self.root, {'fixture.txt': pin})
        path.write_bytes(b'changed')
        with self.assertRaisesRegex(self.D.G.Invalid, 'SHA mismatch'):
            self.D.verify_pins(self.root, {'fixture.txt': pin})

    def test_rss_sums_parent_and_descendants_instead_of_unrelated_process(self):
        inventory = '10 1 1048576\n20 10 2097152\n30 20 3145728\n40 1 99999999\n'
        self.assertEqual(self.D.family_rss(inventory, 10, 20)['rss_gib'], 6.)

    def test_missing_duplicate_empty_or_malformed_inventory_is_invalid(self):
        for text in ('', '10 1 nope', '10 1 1\n10 1 1', '20 1 1', '10 1 -1'):
            with self.subTest(text=text), self.assertRaises(self.D.S.Stop):
                self.D.family_rss(text, 10)
        with self.assertRaises(self.D.S.Stop):
            self.D.family_rss('10 1 1', 10, 20)

    def run_fixture(self, code, **kw):
        directory = self.D.new_directory(self.root / 'runs')
        status = self.D.supervise([sys.executable, '-B', '-c', code], directory,
            preflight=lambda: None, admission=lambda: {'allowed': True, 'reasons': []},
            monitor=kw.pop('monitor', lambda pid: {'rss_gib': .1, 'process_count': 1}),
            **kw)
        return status, directory, json.loads((directory / 'result.json').read_text())

    def test_deadline_kills_and_reaps_a_real_blocked_child(self):
        start = time.monotonic()
        status, directory, result = self.run_fixture('import time; time.sleep(30)', seconds=.15)
        self.assertNotEqual(status, 0)
        self.assertEqual(result['status'], 'INVALID')
        self.assertIn('STOPPED-DEADLINE', result['error'])
        self.assertLess(time.monotonic() - start, 3)
        with self.assertRaises(ProcessLookupError): os.kill(result['worker_pid'], 0)
        self.assertLess(sum(p.stat().st_size for p in directory.iterdir()), 1000000)

    def test_deadline_also_interrupts_blocked_admission(self):
        directory = self.D.new_directory(self.root / 'runs')
        def blocked(): time.sleep(30)
        status = self.D.supervise([sys.executable, '-c', 'raise SystemExit(99)'], directory,
            preflight=lambda: None, admission=blocked,
            monitor=lambda pid: {'rss_gib': .1, 'process_count': 1}, seconds=.05)
        self.assertNotEqual(status, 0)
        result = json.loads((directory / 'result.json').read_text())
        self.assertIn('STOPPED-DEADLINE', result['error'])
        self.assertIsNone(result['worker_pid'])

    def test_rss_at_or_above_cap_stops_the_worker(self):
        for rss in (11., 11.001):
            def observe(pid): return {'rss_gib': rss if pid else .1, 'process_count': 1}
            status, _, result = self.run_fixture('import time; time.sleep(30)', monitor=observe, seconds=1)
            self.assertNotEqual(status, 0)
            self.assertIn('STOPPED-RESOURCE', result['error'])
            with self.assertRaises(ProcessLookupError): os.kill(result['worker_pid'], 0)

    def test_aborted_worker_pipes_are_closed(self):
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter('always', ResourceWarning)
            self.run_fixture('import time; time.sleep(30)', seconds=.05)
            gc.collect()
        leaks = [str(w.message) for w in caught if issubclass(w.category, ResourceWarning)]
        self.assertEqual(leaks, [])

    def test_failure_after_result_creation_retains_data_and_records_invalid_terminal(self):
        original = self.D.Output.record
        def fail_terminal_once(out, kind, **value):
            if kind == 'terminal' and value['status'] == 'MEASURED':
                raise OSError('fixture terminal fsync failed')
            return original(out, kind, **value)
        with mock.patch.object(self.D.Output, 'record', new=fail_terminal_once):
            try:
                status, directory, result = self.run_fixture('print("{\\\"status\\\":\\\"MEASURED\\\"}")', seconds=1)
            except FileExistsError as error:
                self.fail('failure handling attempted to overwrite the saved scalar result: ' + str(error))
        self.assertNotEqual(status, 0)
        self.assertEqual(result['status'], 'MEASURED', 'preserve uncommitted scalar bytes')
        records = [json.loads(line) for line in (directory / 'receipt.jsonl').read_text().splitlines()]
        self.assertEqual(records[-1]['kind'], 'halted')
        self.assertEqual(records[-1]['status'], 'INVALID')
        self.assertFalse(records[-1]['result_committed'])
        self.assertIn('fixture terminal fsync failed', records[-1]['error'])

    def test_blocked_terminal_cleanup_has_its_own_bound(self):
        def blocked_finish(out, value): time.sleep(.3)
        start = time.monotonic()
        with mock.patch.object(self.D.Output, 'finish', new=blocked_finish), \
             mock.patch.object(self.D, 'CLEANUP_S', .05, create=True):
            directory = self.D.new_directory(self.root / 'runs')
            status = self.D.supervise([sys.executable, '-c', 'raise SystemExit(99)'], directory,
                preflight=lambda: None, admission=lambda: {'allowed': False},
                monitor=lambda pid: {'rss_gib': .1, 'process_count': 1}, seconds=.2)
        self.assertNotEqual(status, 0)
        self.assertLess(time.monotonic() - start, .2)

    def test_keyboard_interrupt_after_dispatch_cannot_leave_worker_alive(self):
        seen = []
        children = []
        original = self.D.subprocess.Popen
        def spawn(*args, **kwargs):
            child = original(*args, **kwargs)
            children.append(child)
            return child
        def interrupted(pid):
            if pid:
                seen.append(pid)
                raise KeyboardInterrupt('fixture interrupt')
            return {'rss_gib': .1, 'process_count': 1}
        try:
            with mock.patch.object(self.D.subprocess, 'Popen', new=spawn):
                try:
                    status, _, result = self.run_fixture('import time; time.sleep(30)', monitor=interrupted, seconds=.2)
                except KeyboardInterrupt:
                    self.fail('the interrupted diagnostic left cleanup to its caller')
            self.assertNotEqual(status, 0)
            self.assertEqual(result['status'], 'INVALID')
            self.assertEqual(len(seen), 1)
            with self.assertRaises(ProcessLookupError): os.kill(seen[0], 0)
        finally:
            for child in children:
                if child.poll() is None: os.killpg(child.pid, 9)
                child.communicate(timeout=1)

    def test_worker_cleanup_timeout_is_attempted_once_and_preserves_original_error(self):
        children, calls = [], []
        original = self.D.subprocess.Popen
        def spawn(*args, **kwargs):
            child = original(*args, **kwargs)
            children.append(child)
            return child
        def broken_terminate(child):
            calls.append(child.pid)
            time.sleep(.3)
        def failing_monitor(pid):
            if pid: raise self.D.G.Invalid('fixture original diagnostic error')
            return {'rss_gib': .1, 'process_count': 1}
        start = time.monotonic()
        try:
            with mock.patch.object(self.D.subprocess, 'Popen', new=spawn), \
                 mock.patch.object(self.D.S, 'terminate', new=broken_terminate), \
                 mock.patch.object(self.D, 'CLEANUP_S', .05):
                try:
                    status, _, result = self.run_fixture('import time; time.sleep(30)',
                                                        monitor=failing_monitor, seconds=1)
                except self.D.S.Stop as error:
                    self.fail('cleanup error replaced the original error and skipped its receipt: ' + str(error))
            self.assertNotEqual(status, 0)
            self.assertEqual(result['error'], 'fixture original diagnostic error')
            self.assertIn('STOPPED-DEADLINE', result['cleanup_error'])
            self.assertEqual(len(calls), 1)
            self.assertLess(time.monotonic() - start, .2)
            self.assertTrue(children[0].stdout.closed and children[0].stderr.closed)
        finally:
            for child in children:
                if child.poll() is None: os.killpg(child.pid, 9)
                child.communicate(timeout=1)

    def test_admission_refusal_never_dispatches_worker(self):
        marker = self.root / 'must_not_exist'
        directory = self.D.new_directory(self.root / 'runs')
        status = self.D.supervise([sys.executable, '-c', f'open({str(marker)!r}, "w").write("bad")'], directory,
            preflight=lambda: None, admission=lambda: {'allowed': False, 'reasons': ['fixture refusal']},
            monitor=lambda pid: {'rss_gib': .1, 'process_count': 1}, seconds=1)
        self.assertNotEqual(status, 0)
        self.assertFalse(marker.exists())
        result = json.loads((directory / 'result.json').read_text())
        self.assertIn('INVALID-ADMISSION', result['error'])

    def test_success_writes_only_result_and_receipt_under_the_disk_cap(self):
        status, directory, result = self.run_fixture('print("{\\\"status\\\":\\\"MEASURED\\\",\\\"fixture\\\":true}")', seconds=1)
        self.assertEqual(status, 0)
        self.assertEqual(result['status'], 'MEASURED')
        self.assertEqual({p.name for p in directory.iterdir()}, {'result.json', 'receipt.jsonl'})
        records = [json.loads(line) for line in (directory / 'receipt.jsonl').read_text().splitlines()]
        self.assertEqual(records[-1]['kind'], 'terminal')
        self.assertEqual(records[-1]['result_sha256'], hashlib.sha256((directory / 'result.json').read_bytes()).hexdigest())
        self.assertLess(sum(p.stat().st_size for p in directory.iterdir()), 1000000)

    def test_output_budget_rejects_large_receipt_before_writing_it(self):
        directory = self.D.new_directory(self.root / 'runs')
        out = self.D.Output(directory)
        out.record('fixture', value=1)
        before = (directory / 'receipt.jsonl').read_bytes()
        with self.assertRaises(self.D.S.Stop): out.record('oversized', value='x' * 1000000)
        self.assertEqual((directory / 'receipt.jsonl').read_bytes(), before)

    def test_namespace_reuse_is_refused(self):
        directory = self.D.new_directory(self.root / 'runs')
        self.D.Output(directory)
        with self.assertRaises(FileExistsError): self.D.Output(directory)

    def test_cli_bad_script_pin_returns_nonzero_before_real_inputs(self):
        proc = subprocess.run([sys.executable, '-B', 'tools/new1_identity_diag.py',
            '--scope-sha', '0' * 64, '--source-sha', '0' * 64],
            capture_output=True, text=True, timeout=3,
            env=dict(os.environ, LLMDB_ROOT=str(Path.cwd()), LLMDB_DEVICE='cpu',
                     CUDA_VISIBLE_DEVICES='', OMP_NUM_THREADS='8', MKL_NUM_THREADS='8'))
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn('SHA mismatch', proc.stderr)


if __name__ == '__main__': unittest.main()
