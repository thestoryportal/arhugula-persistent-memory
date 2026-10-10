"""NEW1 enforcement fixtures; no real inputs or geometry execution."""
import importlib
import contextlib
import io
import json
import os
from pathlib import Path
import subprocess
import signal
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
        ps = subprocess.CompletedProcess([], 0, '123 1 123 1048576 1.0\n124 123 123 524288 2.0\n125 124 123 262144 3.0\n99 1 99 9999999 0.0\n', '')
        with mock.patch.object(self.S.subprocess, 'run', side_effect=[vm,ps]):
            value=self.S.sample_resources(123)
        self.assertEqual(value.rss_gib, 1.75)
        self.assertEqual(value.cpu_pct, 6)
        with mock.patch.object(self.S.subprocess, 'run', side_effect=[vm,ps]):
            with self.assertRaisesRegex(self.S.Stop, 'MONITORING'):
                self.S.sample_resources(100)

    def test_reparented_group_member_still_counts_toward_rss_cap(self):
        vm=subprocess.CompletedProcess([],0,'Pages free: 1048576.\nPages inactive: 0.\nPages speculative: 0.\n','')
        ps=subprocess.CompletedProcess([],0,'123 1 123 1048576 1.0\n124 1 123 6291456 2.0\n99 1 99 9999999 0.0\n','')
        with mock.patch.object(self.S.subprocess,'run',side_effect=[vm,ps]):
            sample=self.S.sample_resources(123)
        self.assertEqual(sample.rss_gib,7)
        self.assertEqual(sample.cpu_pct,3)
        with self.assertRaisesRegex(self.S.Stop,'STOPPED-RESOURCE'):
            self.controller([sample]).check(123)

    def prereg_fixture(self,status):
        path=self.root/'docs/NEW1_ADAPTER_GEOMETRY_PREREG.md'
        path.parent.mkdir(exist_ok=True)
        path.write_text('# NEW-1 — fixture\n\n'+status+'\n\nHistorical: DRAFT v2 remains NOT FROZEN.\n')
        return path,self.S.sha_file(path)

    def supervisor_main(self,digest):
        def dispatch(command,directory,*,admission):
            self.assertTrue(admission()['allowed'])
            return 'PASS'
        with mock.patch.object(self.S,'ROOT',self.root),mock.patch.object(sys,'argv',['new1','--prereg-sha',digest]),\
             mock.patch.object(self.S,'supervise',side_effect=dispatch),\
             mock.patch.object(self.S,'cpu_admission',return_value={'allowed':True,'reasons':[]}) as admit,\
             contextlib.redirect_stdout(io.StringIO()):
            result=self.S.main()
        return result,admit.call_count

    def test_supervisor_accepts_authoritative_freeze_with_historical_draft_footer(self):
        _,digest=self.prereg_fixture('**FROZEN v2 · 2026-10-09 (D-NEW1-1; reviewed).**')
        self.assertEqual(self.supervisor_main(digest),(0,1))

    def test_supervisor_refuses_draft_header_even_with_quoted_frozen_text(self):
        path,digest=self.prereg_fixture('**DRAFT v2**')
        path.write_text(path.read_text().replace('Historical: DRAFT v2 remains NOT FROZEN.','Quoted: **FROZEN v2**'))
        with self.assertRaisesRegex(self.S.Stop,'INVALID-PREREG'):
            self.supervisor_main(self.S.sha_file(path))

    def test_supervisor_refuses_exact_prereg_hash_mismatch(self):
        self.prereg_fixture('**FROZEN v2 · 2026-10-09 (D-NEW1-1; reviewed).**')
        with self.assertRaisesRegex(self.S.Stop,'INVALID-PREREG'):
            self.supervisor_main('0'*64)

    def test_worker_accepts_same_freeze_before_imports_without_geometry(self):
        G=importlib.import_module('tools.new1_geometry')
        _,digest=self.prereg_fixture('**FROZEN v2 · 2026-10-09 (D-NEW1-1; reviewed).**')
        client=mock.Mock(); client.cell.side_effect=RuntimeError('fixture reached import admission')
        with mock.patch.object(G,'ROOT',self.root),self.assertRaisesRegex(RuntimeError,'fixture reached import admission'):
            G.run(client,self.run,digest)
        client.cell.assert_called_once_with('imports','numerical-dependencies')

    def test_worker_refuses_draft_header_before_imports(self):
        G=importlib.import_module('tools.new1_geometry')
        path,_=self.prereg_fixture('**DRAFT v2**')
        path.write_text(path.read_text().replace('Historical: DRAFT v2 remains NOT FROZEN.','Quoted: **FROZEN v2**'))
        client=mock.Mock(); client.cell.side_effect=RuntimeError('fixture reached imports')
        with mock.patch.object(G,'ROOT',self.root),self.assertRaises(G.Invalid):
            G.run(client,self.run,self.S.sha_file(path))
        client.cell.assert_not_called()

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
        events,_=self.state()
        self.assertTrue(any(e['type']=='halted' for e in events),'watchdog kill must still reap and persist its halt')

    def test_watchdog_refuses_memory_drop_during_blocking_admission(self):
        started=time.monotonic()
        def sample(pid): return self.S.Sample(5 if time.monotonic()-started>.03 else 13,0,0)
        with mock.patch.object(self.S,'SAMPLE_S',.01),mock.patch.object(self.S,'DEADLINE_S',.5):
            outcome=self.S.supervise(self.worker('pass'),self.run,
                admission=lambda:subprocess.run([sys.executable,'-c','import time; time.sleep(2)']),monitor=sample)
        self.assertEqual(outcome,'STOPPED-RESOURCE')
        self.assertLess(time.monotonic()-started,.5)

    def grandchild_worker(self,leader_exits):
        leader=self.root/'leader_pid'; child=self.root/'grandchild_pid'; ticks=self.root/'ticks'
        child_source=f'import os,time\nfrom pathlib import Path\nPath({str(child)!r}).write_text(str(os.getpid()))\nwhile True:\n Path({str(ticks)!r}).write_text(str(time.monotonic_ns()))\n time.sleep(.01)\n'
        source=f'import os,subprocess,sys,time\nfrom pathlib import Path\nPath({str(leader)!r}).write_text(str(os.getpid()))\nsubprocess.Popen([sys.executable,"-B","-c",{child_source!r}],pass_fds=(int(os.environ["NEW1_CONTROL_FD"]),))\nwhile not Path({str(ticks)!r}).exists(): time.sleep(.005)\n'
        if not leader_exits: source+='while True: time.sleep(.01)\n'
        def cleanup():
            if leader.exists():
                if ticks.exists():
                    before=ticks.read_text(); time.sleep(.03)
                    if ticks.read_text()==before: return
                try: os.killpg(int(leader.read_text()),signal.SIGKILL)
                except ProcessLookupError: pass
        self.addCleanup(cleanup)
        return self.worker(source),child,ticks

    def assert_grandchild_stopped(self,child,ticks):
        self.assertTrue(child.exists(),'grandchild reached the live positive control')
        before=ticks.read_text()
        time.sleep(.04)
        self.assertEqual(ticks.read_text(),before,'grandchild kept running after supervisor closeout')

    def test_real_grandchild_is_killed_on_observed_rss_breach(self):
        command,child,ticks=self.grandchild_worker(False)
        with mock.patch.object(self.S,'SAMPLE_S',.01),mock.patch.object(self.S,'DEADLINE_S',.8):
            outcome=self.S.supervise(command,self.run,admission=lambda:{'allowed':True,'reasons':[]},
                monitor=lambda pid:self.S.Sample(13,6.1 if pid and ticks.exists() else 0,0))
        self.assertEqual(outcome,'STOPPED-RESOURCE')
        self.assert_grandchild_stopped(child,ticks)

    def test_leader_exit_kills_ipc_holding_grandchild_without_waiting_for_deadline(self):
        command,child,ticks=self.grandchild_worker(True)
        started=time.monotonic()
        with mock.patch.object(self.S,'SAMPLE_S',.01),mock.patch.object(self.S,'DEADLINE_S',.8):
            outcome=self.S.supervise(command,self.run,admission=lambda:{'allowed':True,'reasons':[]},
                monitor=lambda pid:self.S.Sample(13,0,0))
        elapsed=time.monotonic()-started
        self.assertEqual(outcome,'INVALID-WORKER')
        self.assertLess(elapsed,.6)
        self.assert_grandchild_stopped(child,ticks)

    def test_blocked_halt_persistence_cannot_extend_total_deadline(self):
        original=self.S.receipt; stderr=io.StringIO()
        def blocked(directory,label,data):
            if label=='halt': time.sleep(2)
            return original(directory,label,data)
        started=time.monotonic()
        with mock.patch.object(self.S,'DEADLINE_S',.08),mock.patch.object(self.S,'receipt',side_effect=blocked),\
             contextlib.redirect_stderr(stderr):
            outcome=self.S.supervise(self.worker('pass'),self.run,
                admission=lambda:{'allowed':False,'reasons':['fixture refusal']},monitor=lambda pid:self.S.Sample(13,0,0))
        elapsed=time.monotonic()-started
        self.assertEqual(outcome,'INVALID-ADMISSION','original refusal must survive cleanup timeout')
        self.assertLess(elapsed,.3)
        self.assertIn('closeout incomplete',stderr.getvalue())
        events,_=self.state()
        self.assertFalse(any(e['type'] in ('halted','run_finished','finding_staged') for e in events))

    def test_successful_exit_at_loop_bottom_still_terminates_group(self):
        (self.run/'geometry.json').write_text(json.dumps({'tier':'MATH-PROXY','boundary':'math estimate, not evidence',
            'predictions':{'H-COV':'FAIL','H-TOP':'FAIL','H-RANK':'PASS','H-OVERLAP':'PASS'}}))
        parent=mock.Mock(); child=mock.Mock(); child.fileno.return_value=99
        parent.recv.side_effect=[b'{"type":"hello","pid":123}\n{"type":"complete","path":"geometry.json"}\n',b'']
        process=mock.Mock(pid=123,returncode=0)
        # Alive at the second loop's top; exited by the EOF check at its bottom.
        process.poll.side_effect=[None,None,None,0]
        selector=mock.MagicMock(); selector.__enter__.return_value.select.return_value=[(None,None)]
        with mock.patch.object(self.S.socket,'socketpair',return_value=(parent,child)),\
             mock.patch.object(self.S.subprocess,'Popen',return_value=process),\
             mock.patch.object(self.S.selectors,'DefaultSelector',return_value=selector),\
             mock.patch.object(self.S.os,'killpg') as kill:
            outcome=self.S.supervise(['fixture-only'],self.run,admission=lambda:{'allowed':True,'reasons':[]},
                monitor=lambda pid:self.S.Sample(13,0,0))
        self.assertEqual(outcome,'PASS')
        kill.assert_called_once_with(123,signal.SIGKILL)
        process.wait.assert_called_once()


if __name__=='__main__': unittest.main()
