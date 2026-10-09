"""NEW1 enforcement fixtures; no real inputs or geometry execution."""
import importlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest
from unittest import mock

from tools.mathlab_events import read_events, fold


class Clock:
    def __init__(self): self.now = 0.
    def __call__(self): return self.now
    def sleep(self, seconds): self.now += seconds


class SupervisorTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(Path('tools/new1_supervisor.py').is_file(), 'NEW1 supervisor is not built')
        self.S = importlib.import_module('tools.new1_supervisor')
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.run = self.root / 'new1_fixture'
        self.run.mkdir()
        self.clock = Clock()

    def controller(self, values):
        values = iter(values)
        return self.S.Controller(self.run, clock=self.clock, sleep=self.clock.sleep,
            monitor=lambda pid: next(values))

    def state(self):
        events, errors = read_events(self.run/'events.jsonl')
        self.assertEqual(errors, [])
        return events, fold(events)

    def test_svd_requires_thirteen_gib_not_eight(self):
        c = self.controller([self.S.Sample(12.9, 1, 0), self.S.Sample(13, 1, 0)])
        sample = c.wait_cell('covariance-svd', 'l4', 123)
        self.assertEqual(sample.avail_gib, 13)
        self.assertGreater(self.clock.now, 0)
        events, _ = self.state()
        gate = next(e for e in events if e['type']=='gate_result')
        self.assertEqual(gate['bar'], 13)

    def test_cell_timeout_stops_without_lowering_reserve(self):
        c = self.S.Controller(self.run, clock=self.clock, sleep=self.clock.sleep,
            monitor=lambda pid: self.S.Sample(12, 1, 0))
        with self.assertRaisesRegex(self.S.Stop, 'STOPPED-RESOURCE'):
            c.wait_cell('covariance-svd', 'l4', 123)
        self.assertEqual(self.clock.now, 300)

    def test_wait_is_inside_unchanged_1800_second_deadline(self):
        c = self.S.Controller(self.run, clock=self.clock, sleep=self.clock.sleep,
            monitor=lambda pid: self.S.Sample(12, 1, 0))
        self.clock.now = 1799
        with self.assertRaisesRegex(self.S.Stop, 'STOPPED-DEADLINE'):
            c.wait_cell('covariance-svd', 'l4', 123)
        self.assertEqual(self.clock.now, 1800)

    def test_rss_ceiling_is_strict_and_family_memory_is_used(self):
        c = self.controller([self.S.Sample(13, 6, 0), self.S.Sample(13, 6.0001, 0)])
        c.check(123)
        with self.assertRaisesRegex(self.S.Stop, 'STOPPED-RESOURCE'):
            c.check(123)

    def test_emergency_available_floor_is_strict(self):
        c = self.controller([self.S.Sample(6, 1, 0), self.S.Sample(5.999, 1, 0)])
        c.check(123)
        with self.assertRaisesRegex(self.S.Stop, 'STOPPED-RESOURCE'):
            c.check(123)

    def test_failed_and_nonfinite_monitoring_refuse(self):
        for sample in (self.S.Sample(float('nan'), 1, 0), self.S.Sample(13, float('inf'), 0)):
            with self.subTest(sample=sample):
                c = self.controller([sample])
                with self.assertRaisesRegex(self.S.Stop, 'MONITORING'):
                    c.check(123)
        c = self.S.Controller(self.run, monitor=lambda pid: (_ for _ in ()).throw(PermissionError('ps denied')))
        with self.assertRaisesRegex(self.S.Stop, 'MONITORING'):
            c.check(123)

    def test_real_subprocess_failures_and_empty_inventory_are_refusals(self):
        failed = subprocess.run([sys.executable, '-c', 'import sys; sys.stderr.write("denied"); sys.exit(7)'], capture_output=True, text=True)
        empty = subprocess.run([sys.executable, '-c', 'pass'], capture_output=True, text=True)
        for response in (failed, empty):
            with self.subTest(code=response.returncode), mock.patch.object(self.S.subprocess, 'run', return_value=response):
                with self.assertRaisesRegex(self.S.Stop, 'MONITORING'):
                    self.S.sample_resources(123)

    def test_rss_probe_sums_descendants_and_refuses_missing_worker(self):
        vm = subprocess.CompletedProcess([], 0, 'Pages free: 1048576.\nPages inactive: 0.\nPages speculative: 0.\n', '')
        ps = subprocess.CompletedProcess([], 0, '123 1 1048576 1.0\n124 123 524288 2.0\n125 124 262144 3.0\n99 1 9999999 0.0\n', '')
        with mock.patch.object(self.S.subprocess, 'run', side_effect=[vm,ps]):
            value=self.S.sample_resources(123)
        self.assertEqual(value.rss_gib, 1.75)
        self.assertEqual(value.cpu_pct, 6)
        with mock.patch.object(self.S.subprocess, 'run', side_effect=[vm,ps]):
            with self.assertRaisesRegex(self.S.Stop, 'MONITORING'):
                self.S.sample_resources(100)

    def test_resource_receipt_is_durable_before_event(self):
        original = self.S.emit
        def inspect(directory, kind, **fields):
            if kind in ('resource_sample','gate_result'):
                receipts = list((Path(directory)/'receipts').glob('*.json'))
                self.assertTrue(receipts)
                self.assertEqual(json.loads(receipts[-1].read_text())['tier'], 'MATH-PROXY')
            return original(directory, kind, **fields)
        with mock.patch.object(self.S,'emit', side_effect=inspect):
            self.controller([self.S.Sample(13,1,0)]).wait_cell('covariance-svd','l4',123)

    def test_unknown_phase_and_spoofed_reserve_refuse(self):
        c=self.controller([])
        with self.assertRaisesRegex(self.S.Stop,'PROTOCOL'):
            c.wait_cell('tiny-svd','l4',123)
        with self.assertRaisesRegex(self.S.Stop,'PROTOCOL'):
            c.handle_cell({'phase':'covariance-svd','cell':'l4','reserve_gib':0},123)

    def worker(self, source):
        path=self.root/'stub.py'; path.write_text(source)
        return [sys.executable, '-B', str(path)]

    def test_refused_cpu_admission_never_dispatches_worker(self):
        marker=self.root/'dispatched'
        cmd=self.worker(f'from pathlib import Path; Path({str(marker)!r}).touch()')
        outcome=self.S.supervise(cmd,self.run, admission=lambda: {'allowed':False,'reasons':['inventory failed']},
            monitor=lambda pid: self.S.Sample(13,0,0))
        self.assertEqual(outcome,'INVALID-ADMISSION')
        self.assertFalse(marker.exists())
        _,state=self.state(); self.assertEqual(state['status'],'halted')

    def test_blocking_admission_is_interrupted_by_whole_run_deadline(self):
        marker=self.root/'dispatched'
        cmd=self.worker(f'from pathlib import Path; Path({str(marker)!r}).touch()')
        started=time.monotonic()
        with mock.patch.object(self.S,'DEADLINE_S',.05):
            outcome=self.S.supervise(cmd,self.run, admission=lambda: time.sleep(2),
                monitor=lambda pid: self.S.Sample(13,0,0))
        self.assertEqual(outcome,'STOPPED-DEADLINE')
        self.assertLess(time.monotonic()-started,1)
        self.assertFalse(marker.exists())

    def test_default_admission_obeys_parent_lab_stop_policy(self):
        from tools import mathlab_runtime as R, mathlab_admit as A
        with mock.patch.object(A,'probe',return_value={'allowed':True,'reasons':[]}), \
             mock.patch.object(R,'enforce_stop_policy',side_effect=R.Halt('LAB-STOP','third abort')):
            with self.assertRaisesRegex(ValueError,'LAB-STOP'):
                self.S.cpu_admission(self.run)

    def test_real_worker_group_is_terminated_on_rss_breach(self):
        pidfile=self.root/'pid'
        cmd=self.worker(f'import os,time\nfrom pathlib import Path\nPath({str(pidfile)!r}).write_text(str(os.getpid()))\nwhile True: time.sleep(.01)\n')
        def sample(pid):
            return self.S.Sample(13,6.1 if pid and pidfile.exists() else 0,0)
        outcome=self.S.supervise(cmd,self.run,admission=lambda:{'allowed':True,'reasons':[]},monitor=sample)
        self.assertEqual(outcome,'STOPPED-RESOURCE')
        pid=int(pidfile.read_text())
        with self.assertRaises(ProcessLookupError): os.kill(pid,0)
        events,_=self.state()
        halt=next(e for e in events if e['type']=='halted')
        self.assertTrue(Path(halt['diagnostic_path']).is_file())

    def test_torn_ipc_and_worker_exit_without_result_are_invalid(self):
        for number,source in enumerate(('import os,socket\ns=socket.socket(fileno=int(os.environ["NEW1_CONTROL_FD"]))\ns.sendall(b"{")', 'pass')):
            with self.subTest(source=source):
                self.run=self.root/f'ipc_{number}'; self.run.mkdir()
                outcome=self.S.supervise(self.worker(source),self.run,
                    admission=lambda:{'allowed':True,'reasons':[]},monitor=lambda pid:self.S.Sample(13,0,0))
                self.assertEqual(outcome,'INVALID-WORKER')

    def test_invalid_prediction_is_not_boolean_fail_or_calibration(self):
        path=self.run/'geometry.json'
        path.write_text(json.dumps({'tier':'MATH-PROXY','boundary':'math estimate, not evidence',
            'predictions':{'H-COV':'INVALID','H-TOP':'FAIL','H-RANK':'PASS','H-OVERLAP':'PASS'}}))
        self.S.publish_predictions(self.run,path)
        events,state=self.state()
        self.assertNotIn('H-COV',state['gate_outcomes'])
        self.assertEqual(state['gate_outcomes']['H-TOP'],'FAIL')
        self.assertEqual(next(e['outcome'] for e in events if e['type']=='stage_finished' and e['stage']=='H-COV'),'INVALID')
        self.assertIsNone(state['calibration_outcome'])

    def test_direct_worker_cli_refuses_before_numerical_imports(self):
        result=subprocess.run([sys.executable,'-B','tools/new1_geometry.py'],capture_output=True,text=True)
        self.assertNotEqual(result.returncode,0)
        self.assertIn('supervisor',result.stderr.lower())

    def test_bare_supervisor_environment_is_not_execution_authority(self):
        env=dict(os.environ,NEW1_SUPERVISOR_PID=str(os.getpid()),NEW1_CONTROL_FD='9999')
        result=subprocess.run([sys.executable,'-B','tools/new1_geometry.py'],env=env,capture_output=True,text=True)
        self.assertNotEqual(result.returncode,0)
        self.assertIn('supervisor',result.stderr.lower())

    def test_persistence_failure_never_emits_success_gate(self):
        with mock.patch.object(self.S.os,'fsync',side_effect=OSError('disk refused')):
            with self.assertRaises(OSError): self.controller([self.S.Sample(13,1,0)]).wait_cell('covariance-svd','l4',123)
        self.assertFalse((self.run/'events.jsonl').exists())

    def test_observed_breach_stops_before_any_potentially_blocking_persistence(self):
        c=self.controller([self.S.Sample(13,6.1,0)])
        with mock.patch.object(self.S,'receipt',side_effect=OSError('blocked persistence')):
            with self.assertRaisesRegex(self.S.Stop,'STOPPED-RESOURCE'):
                c.check(123)

    def test_private_handshake_and_complete_stub_result_fold_to_completion(self):
        source='''import json,os,socket
from pathlib import Path
s=socket.socket(fileno=int(os.environ['NEW1_CONTROL_FD']))
f=s.makefile('rwb',buffering=0)
def send(v): f.write((json.dumps(v)+'\\n').encode())
send({'type':'hello','pid':os.getpid()}); f.readline()
send({'type':'cell','phase':'covariance-svd','cell':'l4'}); f.readline()
p=Path(os.environ['NEW1_FIXTURE_RUN'])/'geometry.json'
p.write_text(json.dumps({'tier':'MATH-PROXY','boundary':'math estimate, not evidence',
'predictions':{'H-COV':'FAIL','H-TOP':'FAIL','H-RANK':'PASS','H-OVERLAP':'PASS'}}))
send({'type':'complete','path':'geometry.json'})
'''
        with mock.patch.dict(os.environ,NEW1_FIXTURE_RUN=str(self.run)):
            outcome=self.S.supervise(self.worker(source),self.run,admission=lambda:{'allowed':True,'reasons':[]},
                monitor=lambda pid:self.S.Sample(13,0,0))
        self.assertEqual(outcome,'PASS')
        events,state=self.state()
        self.assertEqual(state['steps'][4],'PASS')
        self.assertEqual(state['gate_outcomes']['H-COV'],'FAIL')
        self.assertIsNone(state['calibration_outcome'])
        finding=next(e for e in events if e['type']=='finding_staged')
        self.assertTrue(Path(finding['path']).is_file())

    def test_watchdog_enforces_during_blocked_persistence(self):
        pidfile=self.root/'pid'; blocked=self.root/'blocked'
        command=self.worker(f'import os,time\nfrom pathlib import Path\nPath({str(pidfile)!r}).write_text(str(os.getpid()))\nwhile True: time.sleep(.01)')
        original=self.S.receipt
        def persist(directory,label,data):
            if label=='resource' and pidfile.exists():
                blocked.touch(); time.sleep(2)
            return original(directory,label,data)
        def sample(pid): return self.S.Sample(13,6.1 if blocked.exists() else 0,0)
        started=time.monotonic()
        with mock.patch.object(self.S,'receipt',side_effect=persist),mock.patch.object(self.S,'SAMPLE_S',.01),mock.patch.object(self.S,'DEADLINE_S',.5):
            outcome=self.S.supervise(command,self.run,admission=lambda:{'allowed':True,'reasons':[]},monitor=sample)
        self.assertEqual(outcome,'STOPPED-RESOURCE')
        self.assertLess(time.monotonic()-started,.5)

    def test_watchdog_refuses_memory_drop_during_blocking_admission(self):
        started=time.monotonic()
        def sample(pid): return self.S.Sample(5 if time.monotonic()-started>.03 else 13,0,0)
        with mock.patch.object(self.S,'SAMPLE_S',.01),mock.patch.object(self.S,'DEADLINE_S',.5):
            outcome=self.S.supervise(self.worker('pass'),self.run,
                admission=lambda:subprocess.run([sys.executable,'-c','import time; time.sleep(2)']),monitor=sample)
        self.assertEqual(outcome,'STOPPED-RESOURCE')
        self.assertLess(time.monotonic()-started,.5)


if __name__=='__main__': unittest.main()
