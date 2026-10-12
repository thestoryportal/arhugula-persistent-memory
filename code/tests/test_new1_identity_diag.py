"""Synthetic CPU fixtures only; no real covariance, capture or admission."""
import contextlib
import hashlib
import io
import gc
import importlib
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import time
import unittest
import warnings
from unittest import mock


class IdentityDiagnosticTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(Path('code/lab/runners/new1_identity_diag.py').is_file(),
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
        signal_before = _fix5_state()
        start = time.monotonic()
        status, directory, result = self.run_fixture('import time; time.sleep(30)', seconds=.15)
        self.assertEqual(_fix5_state(), signal_before, 'deadline return must preserve signal state before teardown')
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
        seen, owners = [], []
        original = self.D.OwnedWorker.start
        def capture(owner, *args):
            owners.append(owner); return original(owner, *args)
        def interrupted(pid):
            if pid:
                seen.append(pid)
                raise KeyboardInterrupt('fixture interrupt')
            return {'rss_gib': .1, 'process_count': 1}
        with mock.patch.object(self.D.OwnedWorker, 'start', new=capture):
            try:
                status, _, result = self.run_fixture('import time; time.sleep(30)', monitor=interrupted, seconds=.2)
            except KeyboardInterrupt:
                self.fail('the interrupted diagnostic left cleanup to its caller')
        self.assertNotEqual(status, 0)
        self.assertEqual(result['status'], 'INVALID')
        self.assertEqual(len(seen), 1)
        with self.assertRaises(ProcessLookupError): os.kill(seen[0], 0)
        self.assertIsNotNone(owners[0].returncode)
        self.assertEqual(owners[0].proof['pid'], seen[0])
        self.assertTrue(all(fd is None for pair in owners[0].channels.values() for fd in pair))

    def test_worker_cleanup_timeout_is_attempted_once_and_preserves_original_error(self):
        owners = []
        original_start = self.D.OwnedWorker.start
        original_kill = self.D.kill_worker
        def capture(owner, *args):
            owners.append(owner); return original_start(owner, *args)
        def delayed_kill(pid):
            time.sleep(.08)
            return original_kill(pid)
        def failing_monitor(pid):
            if pid: raise self.D.G.Invalid('fixture original diagnostic error')
            return {'rss_gib': .1, 'process_count': 1}
        start = time.monotonic()
        with mock.patch.object(self.D.OwnedWorker, 'start', new=capture), \
             mock.patch.object(self.D, 'kill_worker', new=delayed_kill), \
             mock.patch.object(self.D, 'CLEANUP_S', .05):
            try:
                status, _, result = self.run_fixture('import time; time.sleep(30)', monitor=failing_monitor, seconds=1)
            except self.D.S.Stop as error:
                self.fail('cleanup error replaced the original error and skipped its receipt: ' + str(error))
        self.assertNotEqual(status, 0)
        self.assertEqual(result['error'], 'fixture original diagnostic error')
        self.assertIn('STOPPED-DEADLINE', result['cleanup_error'])
        self.assertEqual(owners[0].proof['kills'], 1, 'worker group killed exactly once')
        self.assertEqual(owners[0].proof['pid'], result['worker_pid'])
        self.assertIsNotNone(owners[0].returncode, 'guardian reaped before terminal return')
        with self.assertRaises(ChildProcessError): os.waitpid(owners[0].pid, os.WNOHANG)
        with self.assertRaises(ProcessLookupError): os.kill(result['worker_pid'], 0)
        self.assertLess(time.monotonic() - start, .2)
        self.assertTrue(all(fd is None for pair in owners[0].channels.values() for fd in pair))

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
        proc = subprocess.run([sys.executable, '-B', 'code/lab/runners/new1_identity_diag.py',
            '--scope-sha', '0' * 64, '--source-sha', '0' * 64],
            capture_output=True, text=True, timeout=3,
            env=dict(os.environ, LLMDB_ROOT=str(Path.cwd()), LLMDB_DEVICE='cpu',
                     CUDA_VISIBLE_DEVICES='', OMP_NUM_THREADS='8', MKL_NUM_THREADS='8'))
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn('SHA mismatch', proc.stderr)


if __name__ == '__main__': unittest.main()


# FIX5 snapshots precede assertions and fixture cleanup; leaking REDs run in a child.
def _fix5_state():
    return dict(mask=sorted(map(int, signal.pthread_sigmask(signal.SIG_BLOCK, []))),
                pending=sorted(map(int, signal.sigpending())),
                handlers={str(int(s)): repr(signal.getsignal(s)) for s in (signal.SIGINT, signal.SIGALRM)},
                timer=list(signal.getitimer(signal.ITIMER_REAL)))


def _fix5_record(test, kind, value):
    print('FIX5 '+json.dumps(dict(test=test.id(), kind=kind, **value), sort_keys=True), flush=True)
    if os.environ.get('NEW1_FIX5_RECEIPTS'):
        path = Path(os.environ['NEW1_FIX5_RECEIPTS'])/(test.id()+'_'+kind+'_'+str(os.getpid())+'.json')
        with path.open('x') as out:
            json.dump(value, out, indent=2); out.write('\n'); out.flush(); os.fsync(out.fileno())


def _fix5_isolated(test):
    if os.environ.get('NEW1_FIX5_INNER_ID') == test.id(): return False
    command = [sys.executable, '-B', '-W', 'error::ResourceWarning', '-m', 'unittest', test.id(), '-v']
    child = subprocess.run(command, capture_output=True, text=True, timeout=5,
        env=dict(os.environ, NEW1_FIX5_INNER_ID=test.id(), PYTHONDONTWRITEBYTECODE='1'))
    print(child.stdout+(child.stderr if child.returncode else ''), end='', flush=True)
    _fix5_record(test, 'interpreter_exit', dict(native_exit=child.returncode, command=command,
        python_return_marker='"python_return"' in child.stdout))
    test.assertEqual(child.returncode, 0, child.stdout+child.stderr)
    test.assertNotIn('ResourceWarning:', child.stderr)
    test.assertNotIn('Exception ignored in', child.stderr)
    return True


def _fix5_owner(owner):
    guardian_collected = owner.pid is None
    if owner.pid is not None:
        try: os.waitpid(owner.pid, os.WNOHANG)
        except ChildProcessError: guardian_collected = True
    absent = group_absent = owner.worker_pid is None
    if owner.worker_pid is not None:
        try: os.kill(owner.worker_pid, 0)
        except ProcessLookupError: absent = True
        try: os.killpg(owner.worker_pid, 0)
        except ProcessLookupError: group_absent = True
    return dict(guardian=owner.pid, worker=owner.worker_pid, returncode=owner.returncode,
                proof=owner.proof, guardian_collected=guardian_collected,
                worker_absent=absent, worker_group_absent=group_absent,
                channels={k:list(v) for k,v in owner.channels.items()}, streams=dict(owner.streams))


def _fix5_assert_owned(test, value):
    test.assertIsNotNone(value['returncode'])
    test.assertIsNotNone(value['proof'])
    test.assertEqual(value['proof']['pid'], value['worker'])
    test.assertTrue(value['guardian_collected'])
    test.assertTrue(value['worker_absent'])
    test.assertTrue(value['worker_group_absent'])
    test.assertTrue(all(fd is None for pair in value['channels'].values() for fd in pair))
    test.assertEqual(value['streams'], {})


def _fix5_refusal(test, entry, blocked, *, direct=False):
    from tools import new1_identity_diag as I
    with tempfile.TemporaryDirectory(dir='/private/tmp') as temp:
        directory = Path(temp)/'never-created'
        signal.pthread_sigmask(signal.SIG_BLOCK, blocked)
        for sig in blocked: os.kill(os.getpid(), sig)
        before = _fix5_state(); calls = []; error = None; status = None
        def touched(*args, **kwargs):
            calls.append('protected-work')
            raise I.S.Stop('INVALID-FIX5-WORK', 'protected work reached before refusal')
        out, err = io.StringIO(), io.StringIO()
        start = time.monotonic()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            if direct:
                try:
                    with mock.patch.object(I, 'Output', side_effect=touched), \
                         mock.patch.object(I, 'OwnedWorker', side_effect=touched):
                        status = I.supervise([sys.executable, '-B', '-c', 'raise SystemExit(99)'], directory,
                            preflight=touched, admission=touched, monitor=touched, seconds=.2)
                except I.S.Stop as failure: error = failure
            else:
                with mock.patch.object(entry.G, 'verify_file', side_effect=touched), \
                     mock.patch.object(entry, 'new_directory', side_effect=touched), \
                     mock.patch.object(entry, 'verify_launch', side_effect=touched), \
                     mock.patch.object(I, 'OwnedWorker', side_effect=touched), \
                     mock.patch.object(I, 'Output', side_effect=touched):
                    status = entry.main(['--scope-sha','0'*64,'--source-sha','0'*64])
        elapsed = time.monotonic()-start
        after = _fix5_state()
        record = dict(before=before, after=after, calls=calls, python_return=status,
                      exception=str(error) if error else None, elapsed_s=elapsed,
                      directory_exists=directory.exists(), output=list(Path(temp).rglob('*')),
                      stdout=out.getvalue(), stderr=err.getvalue())
        record['output'] = [str(p) for p in record['output']]
        _fix5_record(test, 'before_cleanup', record)
        test.assertEqual(after, before, 'caller mask, pending signals, handlers and timer must survive refusal')
        test.assertLess(elapsed, .3)
        if direct:
            test.assertIsNotNone(error, 'direct supervision must raise INVALID-ENFORCEMENT')
            test.assertEqual(error.code, 'INVALID-ENFORCEMENT')
        else:
            test.assertEqual(status, 2)
            test.assertIn('INVALID-ENFORCEMENT', err.getvalue())
        test.assertEqual(calls, [])
        test.assertFalse(directory.exists())
        test.assertEqual(record['output'], [])
        test.assertEqual(out.getvalue(), '')


class Fix5SignalTests(unittest.TestCase):
    def boundary(self, target, *, owned=False, handler=False, worker=False, final=False):
        if _fix5_isolated(self): return
        from tools import new1_identity_diag as I
        # SIGUSR1 is unrelated to enforcement; production must preserve it.
        signal.pthread_sigmask(signal.SIG_BLOCK, [signal.SIGUSR1])
        before = _fix5_state(); owners = []; injections = []; status = None; error = None
        raw_mask, raw_handler = signal.pthread_sigmask, signal.signal
        supervisor_blocks = 0
        entry_failed = False
        raw_require = I.G.require
        NativeOwner = I.OwnedWorker
        class ObservedOwner(NativeOwner):
            def __init__(owner, *args):
                super().__init__(*args); owners.append(owner)
        def mutate(how, bits):
            nonlocal supervisor_blocks
            old = raw_mask(how, bits)
            frame = sys._getframe(1)
            if how == signal.SIG_BLOCK and bits and frame.f_code.co_name == 'supervise':
                supervisor_blocks += 1
            if (not injections and (target != '__exit__' or entry_failed)
                and (not final or supervisor_blocks > 1) and how == signal.SIG_BLOCK and set(bits) == {signal.SIGINT, signal.SIGALRM}
                and frame.f_code.co_filename == I.__file__ and frame.f_code.co_name == target
                and (not owned or any(o.ready and o.worker_pid for o in owners))):
                injections.append(dict(function=target, line=frame.f_lineno, prior=sorted(map(int, old)),
                    after_real_mutation=sorted(map(int, raw_mask(signal.SIG_BLOCK, [])))))
                raise I.S.Stop('INVALID-FIX5-BOUNDARY', 'interrupt after real mask mutation')
            return old
        def fail_entry(condition, message):
            nonlocal entry_failed
            if (target == '__exit__' and message == 'nested deadline phase' and not entry_failed
                and (not owned or any(o.ready and o.worker_pid for o in owners))):
                entry_failed = True
                raise I.S.Stop('INVALID-FIX5-ENTRY', 'entry failure before active phase assignment')
            return raw_require(condition, message)
        def install(sig, value):
            old = raw_handler(sig, value)
            if not injections and callable(value) and value.__name__ == 'on_signal':
                injections.append(dict(function='handler-install', signal=int(sig),
                    after_real_mutation=sorted(map(int, raw_mask(signal.SIG_BLOCK, [])))))
                raise I.S.Stop('INVALID-FIX5-BOUNDARY', 'interrupt after real handler installation')
            return old
        with tempfile.TemporaryDirectory(dir='/private/tmp') as temp:
            directory = I.new_directory(Path(temp)/'runs')
            channel = None
            owner = ObservedOwner(time.monotonic()+.2) if worker else None
            if target == 'close_fd':
                channel = list(os.pipe()); owner.channels['fixture'] = channel
            start = time.monotonic()
            try:
                with mock.patch.object(signal, 'pthread_sigmask', new=mutate if not handler else raw_mask), \
                     mock.patch.object(signal, 'signal', new=install if handler else raw_handler), \
                     mock.patch.object(I, 'OwnedWorker', ObservedOwner), \
                     mock.patch.object(I.G, 'require', new=fail_entry), \
                     contextlib.redirect_stderr(io.StringIO()):
                    if worker:
                        if target == 'start': owner.start([sys.executable,'-B','-c','pass'], start+.1, start+.2)
                        elif target == 'step': owner.step(0)
                        else: owner.close_fd('fixture', 0)
                    else:
                        status = I.supervise([sys.executable,'-B','-c',
                            'from tools import new1_identity_diag as I; I.wait_for_release(); import time; time.sleep(2)'],
                            directory, preflight=lambda:None, admission=lambda:{'allowed':True},
                            monitor=lambda pid:{'rss_gib':.01,'process_count':1}, seconds=.2)
            except I.S.Stop as failure: error = str(failure)
            elapsed = time.monotonic()-start
            after = _fix5_state(); ownership = [_fix5_owner(o) for o in owners]
            _fix5_record(self, 'before_cleanup', dict(before=before, after=after, injections=injections,
                python_return=status, exception=error, elapsed_s=elapsed, ownership=ownership))
            try:
                self.assertEqual(len(injections), 1, 'schedule must interrupt the actual production mutation')
                self.assertEqual(after, before, 'production stranded signal state before fixture cleanup')
                self.assertLess(elapsed, .3)
                if owned:
                    self.assertEqual(len(ownership), 1)
                    _fix5_assert_owned(self, ownership[0])
                if worker: self.assertIn('INVALID-FIX5-BOUNDARY', error)
                elif target in ('__enter__', '__exit__'): self.assertEqual(status, 2)
            finally:
                if channel:
                    for fd in channel:
                        if fd is not None: os.close(fd)

    def test_fix5_c1_deadline_entry_restores_unrelated_block(self): self.boundary('__enter__')
    def test_fix5_c1_deadline_exit_restores_unrelated_block(self): self.boundary('__exit__')
    def test_fix5_c1_deadline_exit_with_owned_child_reaps_before_cleanup(self): self.boundary('__exit__', owned=True)
    def test_fix5_c1_handler_install_restores_substituted_handler(self): self.boundary('supervise', handler=True)
    def test_fix5_c1_handler_restore_restores_caller_mask(self): self.boundary('supervise', final=True)
    def test_fix5_c1_owned_start_restores_mask_after_mutation(self): self.boundary('start', worker=True)
    def test_fix5_c1_owned_step_restores_mask_after_mutation(self): self.boundary('step', worker=True)
    def test_fix5_c1_owned_close_fd_restores_mask_after_mutation(self): self.boundary('close_fd', worker=True)

    def refusal(self, entry, blocked):
        if _fix5_isolated(self): return
        from tools import new1_identity_diag as I
        _fix5_refusal(self, I, blocked, direct=entry == 'direct')

    def test_fix5_c2_direct_sigalrm_refuses_without_consuming_pending(self): self.refusal('direct', [signal.SIGALRM])
    def test_fix5_c2_direct_sigint_refuses_without_consuming_pending(self): self.refusal('direct', [signal.SIGINT])
    def test_fix5_c2_direct_both_refuses_without_consuming_pending(self): self.refusal('direct', [signal.SIGINT, signal.SIGALRM])
    def test_fix5_c2_identity_main_sigalrm_refuses_before_file_work(self): self.refusal('main', [signal.SIGALRM])
    def test_fix5_c2_identity_main_sigint_refuses_before_file_work(self): self.refusal('main', [signal.SIGINT])
    def test_fix5_c2_identity_main_both_refuses_before_file_work(self): self.refusal('main', [signal.SIGINT, signal.SIGALRM])
