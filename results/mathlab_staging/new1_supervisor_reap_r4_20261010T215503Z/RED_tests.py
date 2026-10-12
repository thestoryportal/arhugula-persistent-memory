"""NEW1 enforcement fixtures; no real inputs or geometry execution."""
import importlib
import contextlib
import io
import json
import os
from pathlib import Path
import subprocess
import signal
import stat
import sys
import tempfile
import time
import unittest
from types import SimpleNamespace
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
        self.tmp = tempfile.TemporaryDirectory(dir='/private/tmp')
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

    def test_float64_svd_and_checks_require_nineteen_gib_with_fixed_reserves(self):
        for phase in ('covariance-svd-f64','covariance-checks'):
            with self.subTest(phase=phase):
                self.run=self.root/phase; self.run.mkdir(); self.clock.now=0
                c=self.controller([self.S.Sample(18.9,8.06,0),self.S.Sample(19,8.06,0)])
                sample=c.wait_cell(phase,'l4',123)
                self.assertEqual(sample.avail_gib,19)
                self.assertEqual(self.clock.now,1)
                events,_=self.state()
                gate=next(e for e in events if e['type']=='gate_result')
                self.assertEqual(gate['bar'],19)

    def test_float64_cell_keeps_three_hundred_second_wait_and_fail_closed_monitor(self):
        c=self.S.Controller(self.run,clock=self.clock,sleep=self.clock.sleep,
            monitor=lambda pid:self.S.Sample(18,8.06,0))
        with self.assertRaisesRegex(self.S.Stop,'STOPPED-RESOURCE'):
            c.wait_cell('covariance-svd-f64','l4',123)
        self.assertEqual(self.clock.now,300)
        c=self.S.Controller(self.run,monitor=lambda pid:(_ for _ in ()).throw(PermissionError('ps denied')))
        with self.assertRaisesRegex(self.S.Stop,'INVALID-MONITORING'):
            c.wait_cell('covariance-svd-f64','l4',123)

    def test_cell_timeout_stops_without_lowering_reserve(self):
        c = self.S.Controller(self.run, clock=self.clock, sleep=self.clock.sleep,
            monitor=lambda pid: self.S.Sample(12, 1, 0))
        with self.assertRaisesRegex(self.S.Stop, 'STOPPED-RESOURCE'):
            c.wait_cell('covariance-svd', 'l4', 123)
        self.assertEqual(self.clock.now, 300)

    def test_wait_is_inside_amended_2700_second_deadline(self):
        c = self.S.Controller(self.run, clock=self.clock, sleep=self.clock.sleep,
            monitor=lambda pid: self.S.Sample(12, 1, 0))
        self.clock.now = 2699
        with self.assertRaisesRegex(self.S.Stop, 'STOPPED-DEADLINE'):
            c.wait_cell('covariance-svd', 'l4', 123)
        self.assertEqual(self.clock.now, 2700)

    def test_cell_cannot_admit_a_memory_probe_that_finishes_at_301_seconds(self):
        def monitor(pid):
            self.clock.now=301
            return self.S.Sample(13,1,0)
        c=self.S.Controller(self.run,clock=self.clock,sleep=self.clock.sleep,monitor=monitor)
        with self.assertRaisesRegex(self.S.Stop,'STOPPED-RESOURCE'):
            c.wait_cell('covariance-svd','late-probe',123)
        events,_=self.state() if (self.run/'events.jsonl').exists() else ([],None)
        self.assertFalse(any(e['type']=='gate_result' for e in events))

    def test_cell_deadline_covers_resource_and_admission_persistence(self):
        original=self.S.receipt
        for label in ('resource','cell'):
            with self.subTest(label=label):
                self.run=self.root/label; self.run.mkdir(); self.clock.now=0
                def persist(directory,kind,data):
                    proof=original(directory,kind,data)
                    if kind==label: self.clock.now=301
                    return proof
                c=self.controller([self.S.Sample(13,1,0)])
                with mock.patch.object(self.S,'receipt',side_effect=persist),self.assertRaisesRegex(self.S.Stop,'STOPPED-RESOURCE'):
                    c.wait_cell('covariance-svd','late-write',123)
                events,_=self.state() if (self.run/'events.jsonl').exists() else ([],None)
                self.assertFalse(any(e['type']=='gate_result' for e in events))

    def test_cell_alarm_interrupts_blocked_persistence_inside_total_cap(self):
        original=self.S.receipt; started=time.monotonic()
        def persist(directory,label,data):
            if label=='cell': time.sleep(1)
            return original(directory,label,data)
        c=self.S.Controller(self.run,monitor=lambda pid:self.S.Sample(13,1,0))
        with mock.patch.object(self.S,'WAIT_S',.04),mock.patch.object(self.S,'SAMPLE_S',.01),\
             mock.patch.object(self.S,'receipt',side_effect=persist):
            with self.assertRaisesRegex(self.S.Stop,'STOPPED-RESOURCE'):
                with self.S.hard_deadline(.4,heartbeat=lambda:c.observe(123)):
                    c.wait_cell('covariance-svd','blocked-cell-write',123)
        self.assertLess(time.monotonic()-started,.2)

    def test_supervisor_cell_deadline_interrupts_a_blocked_resource_probe(self):
        active=False; S=self.S
        class CellController(S.Controller):
            def wait_cell(controller,*args):
                nonlocal active
                active=True
                return super().wait_cell(*args)
        source='''import json,os,socket
s=socket.socket(fileno=int(os.environ['NEW1_CONTROL_FD']))
f=s.makefile('rwb',buffering=0)
f.write((json.dumps({'type':'hello','pid':os.getpid()})+'\\n').encode()); f.readline()
f.write((json.dumps({'type':'cell','phase':'covariance-svd','cell':'slow-probe'})+'\\n').encode()); f.readline()
'''
        def monitor(pid):
            if active: time.sleep(.25)
            return S.Sample(13,0,0)
        started=time.monotonic()
        with mock.patch.object(S,'Controller',CellController),mock.patch.object(S,'WAIT_S',.04),\
             mock.patch.object(S,'SAMPLE_S',.01),mock.patch.object(S,'DEADLINE_S',.4):
            outcome=S.supervise(self.worker(source),self.run,admission=lambda:{'allowed':True,'reasons':[]},monitor=monitor)
        self.assertEqual(outcome,'STOPPED-RESOURCE')
        self.assertLess(time.monotonic()-started,.2)

    def test_rss_ceiling_is_strict_and_family_memory_is_used(self):
        c = self.controller([self.S.Sample(13, 11, 0), self.S.Sample(13, 11.0001, 0)])
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
        ps=subprocess.CompletedProcess([],0,'123 1 123 1048576 1.0\n124 1 123 11534336 2.0\n99 1 99 9999999 0.0\n','')
        with mock.patch.object(self.S.subprocess,'run',side_effect=[vm,ps]):
            sample=self.S.sample_resources(123)
        self.assertEqual(sample.rss_gib,12)
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

    def history_fixture(self, label='history'):
        root=self.root/label
        current=root/'results/mathlab_staging/runs/new1_current'
        current.mkdir(parents=True)
        return root,current

    def history_run(self, root, name, *, step=4, title='NEW1 history fixture',
                    purpose='experiment', reasons=()):
        directory=root/'results/mathlab_staging/runs'/name
        directory.mkdir()
        self.S.emit(directory,'run_started',step=step,title=title,purpose=purpose,
            deadline_ts='2026-10-10T03:00:00Z',pid=1)
        for reason in reasons:
            self.S.emit(directory,'halted',reason=reason+': fixture abort',diagnostic_path='fixture')
        return directory

    def failed_mathlab_history(self, root):
        directory=self.history_run(root,'m3_failed_fixture',step=3,title='MathLab calibration fixture')
        self.S.emit(directory,'gate_result',gate_id='calibration',plain_words='Frozen calibration',
            observed='FAIL',bar='PASS',comparison='meets',passed=False)
        self.S.emit(directory,'run_finished',outcome='FAIL',summary='Synthetic failed MathLab calibration')

    def test_new1_history_ignores_failed_mathlab_calibration(self):
        from tools import mathlab_admit as A
        root,current=self.history_fixture()
        self.failed_mathlab_history(root)
        decision={'allowed':True,'reasons':[]}
        with mock.patch.object(self.S,'ROOT',root), mock.patch.object(A,'probe',return_value=decision) as probe:
            self.assertIs(self.S.cpu_admission(current),decision)
        probe.assert_called_once_with('cpu',None)

    def test_mathlab_stop_policy_still_rejects_failed_calibration(self):
        from tools import mathlab_runtime as R
        root,current=self.history_fixture()
        self.failed_mathlab_history(root)
        with self.assertRaises(R.Halt) as raised:
            R.enforce_stop_policy(root,4,exclude=current)
        self.assertEqual(raised.exception.code,'LAB-STOP')

    def test_new1_history_fewer_than_three_aborted_runs_allows_cpu_probe(self):
        from tools import mathlab_admit as A
        for count in (0,1,2):
            with self.subTest(prior_runs=count):
                root,current=self.history_fixture(str(count))
                self.failed_mathlab_history(root)
                for number in range(count):
                    reason=('STOPPED-RESOURCE','STOPPED-DEADLINE')[number%2]
                    self.history_run(root,f'new1_previous_{number}',reasons=(reason,))
                decision={'allowed':True,'reasons':[]}
                with mock.patch.object(self.S,'ROOT',root), mock.patch.object(A,'probe',return_value=decision) as probe:
                    self.assertIs(self.S.cpu_admission(current),decision)
                probe.assert_called_once_with('cpu',None)

    def test_new1_history_three_aborted_runs_requires_operator(self):
        from tools import mathlab_admit as A
        for reasons in (('STOPPED-RESOURCE',)*3,('STOPPED-DEADLINE',)*3,
                        ('STOPPED-RESOURCE','STOPPED-DEADLINE','STOPPED-RESOURCE')):
            with self.subTest(reasons=reasons):
                root,current=self.history_fixture('_'.join(reasons))
                self.failed_mathlab_history(root)
                for number,reason in enumerate(reasons):
                    self.history_run(root,f'new1_previous_{number}',reasons=(reason,))
                with mock.patch.object(self.S,'ROOT',root), mock.patch.object(A,'probe') as probe:
                    with self.assertRaises(self.S.Stop) as raised:
                        self.S.cpu_admission(current)
                self.assertEqual(raised.exception.code,'OPERATOR')
                probe.assert_not_called()

    def test_new1_history_ignores_true_mathlab_step_four_aborts(self):
        from tools import mathlab_admit as A
        root,current=self.history_fixture()
        for number in range(3):
            self.history_run(root,f'm4_previous_{number}',title='MathLab candidate questions',
                reasons=(('STOPPED-RESOURCE','STOPPED-DEADLINE')[number%2],))
        decision={'allowed':True,'reasons':[]}
        with mock.patch.object(self.S,'ROOT',root), mock.patch.object(A,'probe',return_value=decision) as probe:
            self.assertIs(self.S.cpu_admission(current),decision)
        probe.assert_called_once_with('cpu',None)

    def test_new1_history_ignores_other_mathlab_stops_and_unrelated_bad_streams(self):
        from tools import mathlab_admit as A
        root,current=self.history_fixture()
        self.history_run(root,'m2_failed_fixture',step=2,title='MathLab reproduction',reasons=('LAB-STOP-2a',))
        self.history_run(root,'m1_halted_fixture',step=1,title='MathLab harvest',reasons=('STOPPED-RESOURCE',))
        malformed=root/'results/mathlab_staging/runs/m3_torn_fixture'
        malformed.mkdir(); (malformed/'events.jsonl').write_text('{')
        decision={'allowed':True,'reasons':[]}
        with mock.patch.object(self.S,'ROOT',root), mock.patch.object(A,'probe',return_value=decision) as probe:
            self.assertIs(self.S.cpu_admission(current),decision)
        probe.assert_called_once_with('cpu',None)

    def test_new1_history_excludes_current_missing_torn_or_aborted_run(self):
        from tools import mathlab_admit as A
        for current_state in ('missing','torn','aborted'):
            with self.subTest(current_state=current_state):
                root,current=self.history_fixture(current_state)
                for number in range(2):
                    self.history_run(root,f'new1_previous_{number}',reasons=('STOPPED-RESOURCE',))
                if current_state=='torn': (current/'events.jsonl').write_text('{')
                if current_state=='aborted':
                    self.S.emit(current,'run_started',step=4,title='NEW1 current fixture',purpose='experiment',
                        deadline_ts='2026-10-10T03:00:00Z',pid=1)
                    self.S.emit(current,'halted',reason='STOPPED-DEADLINE: current fixture',diagnostic_path='fixture')
                decision={'allowed':True,'reasons':[]}
                with mock.patch.object(self.S,'ROOT',root), mock.patch.object(A,'probe',return_value=decision) as probe:
                    self.assertIs(self.S.cpu_admission(current),decision)
                probe.assert_called_once_with('cpu',None)

    def test_new1_history_counts_each_prior_run_once(self):
        from tools import mathlab_admit as A
        root,current=self.history_fixture()
        self.failed_mathlab_history(root)
        self.history_run(root,'new1_repeated_abort',reasons=('STOPPED-RESOURCE','STOPPED-DEADLINE','STOPPED-RESOURCE'))
        self.history_run(root,'new1_second_abort',reasons=('STOPPED-DEADLINE',))
        self.history_run(root,'new1_other_halt',reasons=('INVALID-ADMISSION',))
        decision={'allowed':True,'reasons':[]}
        with mock.patch.object(self.S,'ROOT',root), mock.patch.object(A,'probe',return_value=decision) as probe:
            self.assertIs(self.S.cpu_admission(current),decision)
            probe.assert_called_once_with('cpu',None)
            probe.reset_mock()
            self.history_run(root,'new1_third_abort',reasons=('STOPPED-RESOURCE',))
            with self.assertRaises(self.S.Stop) as raised:
                self.S.cpu_admission(current)
            self.assertEqual(raised.exception.code,'OPERATOR')
            probe.assert_not_called()

    def test_new1_history_missing_or_malformed_refuses_before_cpu_probe(self):
        from tools import mathlab_admit as A
        for defect in ('missing','empty','malformed','torn','not-directory'):
            with self.subTest(defect=defect):
                root,current=self.history_fixture(defect)
                directory=root/'results/mathlab_staging/runs/new1_bad'
                if defect=='not-directory': directory.write_text('not a run directory')
                elif defect=='missing': directory.mkdir()
                else:
                    directory=self.history_run(root,'new1_bad')
                    path=directory/'events.jsonl'
                    if defect=='empty': path.write_text('')
                    elif defect=='malformed': path.write_text('{\n')
                    else: path.write_bytes(path.read_bytes()+b'{')
                with mock.patch.object(self.S,'ROOT',root), mock.patch.object(A,'probe') as probe:
                    with self.assertRaises(self.S.Stop) as raised:
                        self.S.cpu_admission(current)
                self.assertEqual(raised.exception.code,'INVALID-HISTORY')
                probe.assert_not_called()

    def test_new1_history_contradictory_identity_refuses_before_cpu_probe(self):
        from tools import mathlab_admit as A
        for defect in ('step','title','purpose','missing-purpose','no-start','duplicate-start','run-id','mixed-run-ids'):
            with self.subTest(defect=defect):
                root,current=self.history_fixture(defect)
                directory=self.history_run(root,'new1_bad')
                path=directory/'events.jsonl'
                rows=[json.loads(line) for line in path.read_text().splitlines()]
                if defect=='step': rows[0]['step']=3
                elif defect=='title': rows[0]['title']='MathLab candidate questions'
                elif defect=='purpose': rows[0]['purpose']='admission'
                elif defect=='missing-purpose': rows[0].pop('purpose')
                elif defect=='duplicate-start': rows.append(dict(rows[0]))
                elif defect=='run-id': rows[0]['run_id']='new1_other'
                else:
                    self.S.emit(directory,'resource_sample',avail_gib=13,floor_gib=6,rss_gib=0,cpu_pct=0)
                    rows=[json.loads(line) for line in path.read_text().splitlines()]
                    if defect=='no-start': rows=rows[1:]
                    else: rows[-1]['run_id']='new1_other'
                path.write_text(''.join(json.dumps(row)+'\n' for row in rows))
                with mock.patch.object(self.S,'ROOT',root), mock.patch.object(A,'probe') as probe:
                    with self.assertRaises(self.S.Stop) as raised:
                        self.S.cpu_admission(current)
                self.assertEqual(raised.exception.code,'INVALID-HISTORY')
                probe.assert_not_called()

    def test_new1_history_symlink_alias_refuses_before_cpu_probe(self):
        from tools import mathlab_admit as A
        root,current=self.history_fixture()
        previous=self.history_run(root,'new1_previous',reasons=('STOPPED-RESOURCE',))
        (previous.parent/'new1_alias').symlink_to(previous.name,target_is_directory=True)
        with mock.patch.object(self.S,'ROOT',root), mock.patch.object(A,'probe') as probe:
            with self.assertRaises(self.S.Stop) as raised:
                self.S.cpu_admission(current)
        self.assertEqual(raised.exception.code,'INVALID-HISTORY')
        probe.assert_not_called()

    def test_default_admission_preserves_cpu_lead_probe(self):
        from tools import mathlab_admit as A
        root,current=self.history_fixture()
        lead={'fixture':'verified coordinator lead'}
        path=root/'lead.json'; path.write_text(json.dumps(lead))
        decision={'allowed':True,'reasons':[]}
        with mock.patch.object(self.S,'ROOT',root), mock.patch.object(A,'probe',return_value=decision) as probe:
            self.assertIs(self.S.cpu_admission(current,path),decision)
        probe.assert_called_once_with('cpu',lead)

    def test_default_admission_refusal_reaches_cpu_probe_without_dispatch(self):
        from tools import mathlab_admit as A
        root,self.run=self.history_fixture()
        self.failed_mathlab_history(root)
        with mock.patch.object(self.S,'ROOT',root), \
             mock.patch.object(A,'probe',return_value={'allowed':False,'reasons':['inventory failed']}) as probe, \
             mock.patch.object(self.S.subprocess,'Popen',side_effect=AssertionError('dispatch forbidden')) as dispatch:
            outcome=self.S.supervise(['fixture-worker'],self.run,monitor=lambda pid:self.S.Sample(13,0,0))
        self.assertEqual(outcome,'INVALID-ADMISSION')
        probe.assert_called_once_with('cpu',None)
        dispatch.assert_not_called()
        events,state=self.state()
        self.assertEqual(state['status'],'halted')
        self.assertEqual(state['gate_outcomes']['admission'],'FAIL')
        self.assertFalse(any(e['type'] in ('stage_started','finding_staged','run_finished') for e in events))

    def test_real_worker_group_is_terminated_on_rss_breach(self):
        pidfile=self.root/'pid'
        cmd=self.worker(f'import os,time\nfrom pathlib import Path\nPath({str(pidfile)!r}).write_text(str(os.getpid()))\nwhile True: time.sleep(.01)\n')
        def sample(pid):
            return self.S.Sample(13,11.1 if pid and pidfile.exists() else 0,0)
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
        self.assertNotIn('H-TOP',state['gate_outcomes'],'prediction outcomes remain provisional before completion')
        self.assertEqual(next(e['outcome'] for e in events if e['type']=='stage_finished' and e['stage']=='H-COV'),'INVALID')
        self.assertIsNone(state['calibration_outcome'])

    def test_boundary_sensitive_prediction_is_preserved_without_boolean_fail_gate(self):
        path=self.run/'geometry.json'
        path.write_text(json.dumps({'tier':'MATH-PROXY','boundary':'math estimate, not evidence',
            'predictions':{'H-COV':'BOUNDARY-SENSITIVE','H-TOP':'FAIL','H-RANK':'PASS','H-OVERLAP':'PASS'}}))
        outcomes=self.S.publish_predictions(self.run,path)
        self.assertEqual(outcomes['H-COV'],'BOUNDARY-SENSITIVE')
        events,_=self.state()
        self.assertFalse(any(e['type']=='gate_result' and e['gate_id']=='H-COV' for e in events))
        stage=next(e for e in events if e['type']=='stage_finished' and e['stage']=='H-COV')
        self.assertEqual(stage['outcome'],'INVALID')
        self.assertIn('BOUNDARY-SENSITIVE',stage['summary'])
        proof=next((self.run/'receipts').glob('predictions_*.json'))
        self.assertEqual(json.loads(proof.read_text())['predictions']['H-COV'],'BOUNDARY-SENSITIVE')

    def test_boundary_sensitive_completed_worker_cannot_publish_robust_pass(self):
        self.assertEqual(self.complete_fixture('BOUNDARY-SENSITIVE'),'INVALID')
        events,state=self.state()
        self.assertEqual(state['outcome'],'INVALID')
        self.assertNotIn('H-COV',state['gate_outcomes'])
        finding=json.loads((self.run/'finding.json').read_text())
        self.assertEqual(finding['predictions']['H-COV'],'BOUNDARY-SENSITIVE')

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
        c=self.controller([self.S.Sample(13,11.1,0)])
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
        def sample(pid): return self.S.Sample(13,11.1 if blocked.exists() else 0,0)
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
                monitor=lambda pid:self.S.Sample(13,11.1 if pid and ticks.exists() else 0,0))
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

    def complete_fixture(self,cov_outcome='FAIL'):
        (self.run/'geometry.json').write_text(json.dumps({'tier':'MATH-PROXY','boundary':'math estimate, not evidence',
            'predictions':{'H-COV':cov_outcome,'H-TOP':'FAIL','H-RANK':'PASS','H-OVERLAP':'PASS'}}))
        parent=mock.Mock(); child=mock.Mock(); child.fileno.return_value=99
        parent.recv.side_effect=[b'{"type":"hello","pid":123}\n{"type":"complete","path":"geometry.json"}\n',b'']
        process=mock.Mock(pid=123,returncode=0); process.poll.side_effect=[None,None,None,0]
        selector=mock.MagicMock(); selector.__enter__.return_value.select.return_value=[(None,None)]
        with mock.patch.object(self.S.socket,'socketpair',return_value=(parent,child)),\
             mock.patch.object(self.S.subprocess,'Popen',self.popen_factory(process)),\
             mock.patch.object(self.S.selectors,'DefaultSelector',return_value=selector),\
             mock.patch.object(self.S.os,'killpg'):
            return self.S.supervise(['fixture-only'],self.run,admission=lambda:{'allowed':True,'reasons':[]},
                monitor=lambda pid:self.S.Sample(13,0,0))

    def assert_no_prediction_verdict(self,state):
        labels={'H-COV','H-TOP','H-RANK','H-OVERLAP'}
        self.assertTrue(labels.isdisjoint(state['gate_outcomes']),state['gate_outcomes'])
        self.assertFalse(any(g['gate_id'] in labels for g in state['gates']))
        self.assertFalse(any(s.get('outcome') in ('PASS','FAIL') for s in state['stages'] if s['stage'] in labels))
        self.assertFalse(any(f['finding_id']=='NEW1' for f in state['findings']))

    @contextlib.contextmanager
    def terminal_fsync_control(self, failure):
        from tools import mathlab_events as E
        write, fsync = E.os.write, E.os.fsync
        terminal_inodes = set(); snapshots = []
        def append(fd, data):
            count = write(fd, data)
            if b'"type":"run_finished"' in data:
                stat = os.fstat(fd)
                terminal_inodes.add((stat.st_dev, stat.st_ino))
            return count
        def sync(fd):
            stat = os.fstat(fd)
            if (stat.st_dev, stat.st_ino) in terminal_inodes:
                events, errors = read_events(self.run/'events.jsonl')
                self.assertEqual(errors, [])
                snapshots.append(fold(events))
                failure()
            return fsync(fd)
        with mock.patch.object(E.os, 'write', side_effect=append), mock.patch.object(E.os, 'fsync', side_effect=sync):
            yield snapshots

    def test_terminal_fsync_timeout_has_no_committed_outcome_or_predictions(self):
        def blocked(): time.sleep(2)
        stderr = io.StringIO()
        with self.terminal_fsync_control(blocked) as snapshots, mock.patch.object(self.S, 'DEADLINE_S', .15), \
             contextlib.redirect_stderr(stderr):
            outcome = self.complete_fixture()
        self.assertEqual(outcome, 'STOPPED-DEADLINE')
        self.assertTrue(snapshots, 'control must reach fsync after writing terminal bytes')
        _, final = self.state()
        for state in snapshots + [final]:
            self.assertIsNone(state['outcome'], state)
            self.assertEqual(state['status'], 'invalid: no verdict')
            self.assert_no_prediction_verdict(state)

    def test_persistent_terminal_fsync_failure_with_failed_halt_has_no_verdict(self):
        original = self.S.receipt; stderr = io.StringIO()
        def failed(): raise OSError('fixture persistent terminal fsync failure')
        def receipt(directory, label, data):
            if label == 'halt': raise OSError('fixture halt persistence failure')
            return original(directory, label, data)
        with self.terminal_fsync_control(failed) as snapshots, mock.patch.object(self.S, 'receipt', side_effect=receipt), \
             contextlib.redirect_stderr(stderr):
            outcome = self.complete_fixture()
        self.assertEqual(outcome, 'INVALID-WORKER')
        self.assertTrue(snapshots, 'control must reach fsync after writing terminal bytes')
        self.assertIn('halt persistence failure', stderr.getvalue())
        events, final = self.state()
        self.assertFalse(any(e['type'] == 'halted' for e in events))
        for state in snapshots + [final]:
            self.assertIsNone(state['outcome'], state)
            self.assertEqual(state['status'], 'invalid: no verdict')
            self.assert_no_prediction_verdict(state)

    def test_terminal_directory_sync_or_replace_failure_with_failed_halt_has_no_verdict(self):
        from tools import mathlab_events as E
        write, fsync, replace, receipt = E.os.write, E.os.fsync, E.os.replace, self.S.receipt
        for point in ('directory-fsync', 'replace'):
            with self.subTest(point=point):
                self.run = self.root/point; self.run.mkdir()
                terminal_written = False; snapshots = []; stderr = io.StringIO()
                def fail():
                    events, errors = read_events(self.run/'events.jsonl')
                    self.assertEqual(errors, [])
                    snapshots.append(fold(events))
                    raise OSError('fixture terminal publication refused')
                def append(fd, data):
                    nonlocal terminal_written
                    count = write(fd, data)
                    if b'"type":"run_finished"' in data: terminal_written = True
                    return count
                def sync(fd):
                    if point == 'directory-fsync' and terminal_written and stat.S_ISDIR(os.fstat(fd).st_mode): fail()
                    return fsync(fd)
                def publish(source, target):
                    if point == 'replace' and Path(target).name == 'events.jsonl': fail()
                    return replace(source, target)
                def halt_receipt(directory, label, data):
                    if label == 'halt': raise OSError('fixture halt persistence failure')
                    return receipt(directory, label, data)
                with mock.patch.object(E.os, 'write', side_effect=append), mock.patch.object(E.os, 'fsync', side_effect=sync), \
                     mock.patch.object(E.os, 'replace', side_effect=publish), mock.patch.object(self.S, 'receipt', side_effect=halt_receipt), \
                     contextlib.redirect_stderr(stderr):
                    self.assertEqual(self.complete_fixture(), 'INVALID-WORKER')
                self.assertTrue(snapshots, 'control must hit the terminal publication boundary')
                _, final = self.state()
                for state in snapshots + [final]:
                    self.assertIsNone(state['outcome'])
                    self.assertEqual(state['status'], 'invalid: no verdict')
                    self.assert_no_prediction_verdict(state)

    def test_prediction_visibility_requires_successful_terminal_and_no_halt(self):
        self.assertEqual(self.complete_fixture(),'PASS')
        events,state=self.state()
        self.assertEqual(state['gate_outcomes']['H-COV'],'FAIL')
        for end in range(1,len(events)):
            self.assert_no_prediction_verdict(fold(events[:end]))
        self.S.emit(self.run,'halted',reason='fixture post-terminal I/O failure',diagnostic_path=str(self.run/'diagnostic.json'))
        _,state=self.state()
        self.assertEqual(state['status'],'halted')
        self.assert_no_prediction_verdict(state)

    def test_late_exception_after_terminal_commit_returns_recorded_outcome(self):
        from tools import mathlab_events as E
        replace = E.os.replace
        for point in ('io', 'deadline'):
            with self.subTest(point=point):
                self.run = self.root/('postcommit_'+point); self.run.mkdir()
                stderr = io.StringIO()
                def publish(source, target):
                    replace(source, target)
                    if Path(target).name == 'events.jsonl':
                        if point == 'deadline': time.sleep(2)
                        raise OSError('fixture interruption after committed replacement')
                with mock.patch.object(E.os, 'replace', side_effect=publish), mock.patch.object(self.S, 'DEADLINE_S', .15), \
                     contextlib.redirect_stderr(stderr):
                    self.assertEqual(self.complete_fixture(), 'PASS')
                self.assertIn('postcommit', stderr.getvalue())
                _, state = self.state()
                self.assertEqual(state['status'], 'finished')
                self.assertEqual(state['outcome'], 'PASS')
                self.assertEqual(state['gate_outcomes']['H-COV'], 'FAIL')

    def test_publication_io_failure_distinguishes_before_and_after_terminal_commit(self):
        original_write=self.S.durable_json; original_emit=self.S.emit
        for point in ('finding.json','stage_started','gate_result','stage_finished','finding_staged','run_finished'):
            with self.subTest(point=point):
                self.run=self.root/('io_'+point); self.run.mkdir()
                fired=False
                def write(path,data):
                    if point=='finding.json' and Path(path).name==point: raise OSError('fixture finding persistence refused')
                    return original_write(path,data)
                def emit(directory,kind,**fields):
                    nonlocal fired
                    result=original_emit(directory,kind,**fields)
                    primary=fields.get('stage')=='H-RANK' or fields.get('gate_id')=='H-RANK'
                    if not fired and kind==point and (primary or kind in ('finding_staged','run_finished')):
                        fired=True; raise OSError('fixture publication I/O refused')
                    return result
                stderr=io.StringIO()
                with mock.patch.object(self.S,'durable_json',side_effect=write),mock.patch.object(self.S,'emit',side_effect=emit), \
                     contextlib.redirect_stderr(stderr):
                    self.assertEqual(self.complete_fixture(),'PASS' if point=='run_finished' else 'INVALID-WORKER')
                _,state=self.state()
                if point=='run_finished':
                    self.assertIn('postcommit',stderr.getvalue())
                    self.assertEqual(state['status'],'finished')
                    self.assertEqual(state['gate_outcomes']['H-COV'],'FAIL')
                else:
                    self.assertEqual(state['status'],'halted')
                    self.assert_no_prediction_verdict(state)

    def test_publication_deadline_expiry_hides_provisional_verdicts(self):
        original_write=self.S.durable_json; original_emit=self.S.emit; original_receipt=self.S.receipt
        for point in ('predictions','stage_started','gate_result','stage_finished','finding.json','finding_staged','run_finished'):
            with self.subTest(point=point):
                self.run=self.root/('deadline_'+point); self.run.mkdir()
                def receipt(directory,label,data):
                    result=original_receipt(directory,label,data)
                    if point=='predictions' and label==point: time.sleep(1)
                    return result
                def write(path,data):
                    result=original_write(path,data)
                    if point=='finding.json' and Path(path).name==point: time.sleep(1)
                    return result
                def emit(directory,kind,**fields):
                    primary=fields.get('stage')=='H-RANK' or fields.get('gate_id')=='H-RANK'
                    if kind==point and kind=='run_finished': time.sleep(1)
                    result=original_emit(directory,kind,**fields)
                    if kind==point and (primary or kind=='finding_staged'): time.sleep(1)
                    return result
                with mock.patch.object(self.S,'DEADLINE_S',.06),mock.patch.object(self.S,'receipt',side_effect=receipt),\
                     mock.patch.object(self.S,'durable_json',side_effect=write),mock.patch.object(self.S,'emit',side_effect=emit),\
                     contextlib.redirect_stderr(io.StringIO()):
                    self.assertEqual(self.complete_fixture(),'STOPPED-DEADLINE')
                _,state=self.state()
                self.assert_no_prediction_verdict(state)

    def test_non_prediction_calibration_gate_stays_visible_after_halt(self):
        self.S.emit(self.run,'gate_result',gate_id='calibration',plain_words='existing aggregate',
            observed='FAIL',bar='registered',comparison='meets',passed=False)
        self.S.emit(self.run,'halted',reason='fixture refusal',diagnostic_path=str(self.run/'halt.json'))
        _,state=self.state()
        self.assertEqual(state['calibration_outcome'],'FAIL')

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
             mock.patch.object(self.S.subprocess,'Popen',self.popen_factory(process)),\
             mock.patch.object(self.S.selectors,'DefaultSelector',return_value=selector),\
             mock.patch.object(self.S.os,'killpg') as kill:
            outcome=self.S.supervise(['fixture-only'],self.run,admission=lambda:{'allowed':True,'reasons':[]},
                monitor=lambda pid:self.S.Sample(13,0,0))
        self.assertEqual(outcome,'PASS')
        kill.assert_called_once_with(123,signal.SIGKILL)
        process.wait.assert_called_once()

    def popen_factory(self,process):
        class FakePopen:
            def __new__(cls,*args,**kwargs): return process
            def __init__(handle,*args,**kwargs): pass
        return FakePopen

    @contextlib.contextmanager
    def reap_fixture(self):
        parent=mock.Mock(); child=mock.Mock(); child.fileno.return_value=99
        process=mock.Mock(pid=123,returncode=None)
        process.poll.return_value=None; process.wait.return_value=0
        selector=mock.MagicMock(); selected=selector.__enter__.return_value
        controller=self.S.Controller(self.run,clock=self.clock,sleep=self.clock.sleep,
            monitor=lambda pid:self.S.Sample(13,0,0))
        watchdog={}; hard_deadline=self.S.hard_deadline
        @contextlib.contextmanager
        def deadline(seconds,**kwargs):
            if 'heartbeat' in kwargs: watchdog['callback']=kwargs['heartbeat']
            with hard_deadline(seconds,**kwargs): yield
        with mock.patch.object(self.S.socket,'socketpair',return_value=(parent,child)),\
             mock.patch.object(self.S.subprocess,'Popen',self.popen_factory(process)),\
             mock.patch.object(self.S.selectors,'DefaultSelector',return_value=selector),\
             mock.patch.object(self.S,'Controller',return_value=controller),\
             mock.patch.object(self.S,'hard_deadline',side_effect=deadline),\
             mock.patch.object(self.S.os,'killpg') as kill_group,\
             mock.patch.object(self.S.os,'kill') as kill_pid:
            yield SimpleNamespace(process=process,selector=selected,controller=controller,
                kill_group=kill_group,kill_pid=kill_pid,parent=parent,child=child,
                heartbeat=lambda:watchdog['callback']())

    def expire_run(self,error):
        self.clock.now=2700
        raise error

    def supervise_reap_fixture(self):
        return self.S.supervise(['fixture-only'],self.run,
            admission=lambda:{'allowed':True,'reasons':[]})

    def test_reap_after_deadline_exhaustion(self):
        stderr=io.StringIO()
        with self.reap_fixture() as f,contextlib.redirect_stderr(stderr):
            f.selector.select.side_effect=lambda timeout:self.expire_run(
                self.S.Stop('STOPPED-DEADLINE','fixture run budget exhausted'))
            outcome=self.supervise_reap_fixture()
        f.process.wait.assert_called_once_with(timeout=5)
        f.kill_group.assert_called_with(123,signal.SIGKILL)
        self.assertEqual(outcome,'STOPPED-DEADLINE')
        events,_=self.state()
        self.assertFalse(any(e['type']=='halted' for e in events))
        self.assertIn('closeout incomplete',stderr.getvalue())

    def test_reap_after_cell_deadline_exhaustion(self):
        with self.reap_fixture() as f:
            def expire_cell(timeout):
                f.controller.cell_deadline=300; self.clock.now=300
                raise self.S.Stop('STOPPED-RESOURCE','fixture cell wait exhausted')
            f.selector.select.side_effect=expire_cell
            outcome=self.supervise_reap_fixture()
        f.process.wait.assert_called_once_with(timeout=5)
        self.assertEqual(outcome,'STOPPED-RESOURCE')

    def test_reap_after_heartbeat_kill_at_exhausted_deadline(self):
        with self.reap_fixture() as f:
            def heartbeat(timeout):
                self.clock.now=2700
                f.heartbeat()
            f.selector.select.side_effect=heartbeat
            outcome=self.supervise_reap_fixture()
        f.process.wait.assert_called_once_with(timeout=5)
        f.kill_group.assert_called_with(123,signal.SIGKILL)
        self.assertEqual(outcome,'STOPPED-DEADLINE')

    def test_reap_when_heartbeat_group_signal_is_denied(self):
        with self.reap_fixture() as f:
            f.kill_group.side_effect=PermissionError('fixture group signal denied')
            def heartbeat(timeout):
                f.controller.monitor=lambda pid:(_ for _ in ()).throw(
                    self.S.Stop('STOPPED-RESOURCE','fixture watchdog stop'))
                f.heartbeat()
            f.selector.select.side_effect=heartbeat
            self.supervise_reap_fixture()
        f.process.wait.assert_called_once_with(timeout=5)
        f.kill_pid.assert_called_with(123,signal.SIGKILL)

    def test_reap_when_exception_group_signal_is_denied(self):
        with self.reap_fixture() as f:
            f.kill_group.side_effect=PermissionError('fixture group signal denied')
            f.selector.select.side_effect=self.S.Stop('STOPPED-RESOURCE','fixture stop')
            outcome=self.supervise_reap_fixture()
        f.process.wait.assert_called_once_with(timeout=5)
        f.kill_pid.assert_called_with(123,signal.SIGKILL)
        self.assertEqual(outcome,'STOPPED-RESOURCE')

    def test_reap_before_reporting_group_and_pid_signal_failures(self):
        with self.reap_fixture() as f:
            class AfterReapStderr(io.StringIO):
                def write(stream,value):
                    if value.strip(): f.process.wait.assert_called_once_with(timeout=5)
                    return super().write(value)
            f.kill_group.side_effect=PermissionError('fixture group signal denied')
            f.kill_pid.side_effect=PermissionError('fixture PID signal denied')
            f.selector.select.side_effect=self.S.Stop('STOPPED-RESOURCE','fixture stop')
            with contextlib.redirect_stderr(AfterReapStderr()):
                outcome=self.supervise_reap_fixture()
        f.process.wait.assert_called_once_with(timeout=5)
        self.assertEqual(outcome,'STOPPED-RESOURCE')

    def test_reap_when_loop_termination_group_signal_is_denied(self):
        with self.reap_fixture() as f:
            f.process.poll.return_value=0; f.process.returncode=0
            f.kill_group.side_effect=PermissionError('fixture group signal denied')
            f.selector.select.side_effect=self.S.Stop('STOPPED-RESOURCE','fixture stop after leader exit')
            self.supervise_reap_fixture()
        f.process.wait.assert_called_once_with(timeout=5)
        f.kill_pid.assert_not_called()

    def test_reap_when_termination_wait_timeout_exhausts_budget(self):
        with self.reap_fixture() as f:
            f.process.poll.return_value=0
            attempts=[]
            def wait(*,timeout):
                attempts.append(timeout)
                if len(attempts)==1:
                    self.clock.now=2700
                    raise subprocess.TimeoutExpired('fixture-only',timeout)
                return 0
            f.process.wait.side_effect=wait
            outcome=self.supervise_reap_fixture()
        self.assertEqual(attempts,[5,5])
        self.assertEqual(outcome,'INVALID-WORKER')

    def test_reap_when_closeout_deadline_setup_raises(self):
        with self.reap_fixture() as f:
            deadline=self.S.hard_deadline; calls=[]
            @contextlib.contextmanager
            def failing_closeout(seconds,**kwargs):
                calls.append(seconds)
                if len(calls)==2:
                    raise self.S.Stop('INVALID-ENFORCEMENT','fixture closeout alarm refused')
                with deadline(seconds,**kwargs): yield
            f.selector.select.side_effect=self.S.Stop('STOPPED-RESOURCE','fixture stop')
            with mock.patch.object(self.S,'hard_deadline',side_effect=failing_closeout):
                outcome=self.supervise_reap_fixture()
        f.process.wait.assert_called_once_with(timeout=5)
        self.assertEqual(outcome,'STOPPED-RESOURCE')

    def test_reap_when_halt_receipt_raises(self):
        receipt=self.S.receipt
        with self.reap_fixture() as f:
            def fail_receipt(run_dir,kind,data):
                if kind=='halt':
                    f.process.wait.assert_called_once_with(timeout=5)
                    raise OSError('fixture halt receipt failed')
                return receipt(run_dir,kind,data)
            f.selector.select.side_effect=self.S.Stop('STOPPED-RESOURCE','fixture stop')
            with mock.patch.object(self.S,'receipt',side_effect=fail_receipt):
                outcome=self.supervise_reap_fixture()
        f.process.wait.assert_called_once_with(timeout=5)
        self.assertEqual(outcome,'STOPPED-RESOURCE')

    def test_reap_when_halt_emit_raises(self):
        emit=self.S.emit
        with self.reap_fixture() as f:
            def fail_emit(run_dir,kind,**data):
                if kind=='halted':
                    f.process.wait.assert_called_once_with(timeout=5)
                    raise OSError('fixture halt emit failed')
                return emit(run_dir,kind,**data)
            f.selector.select.side_effect=self.S.Stop('STOPPED-RESOURCE','fixture stop')
            with mock.patch.object(self.S,'emit',side_effect=fail_emit):
                outcome=self.supervise_reap_fixture()
        f.process.wait.assert_called_once_with(timeout=5)
        self.assertEqual(outcome,'STOPPED-RESOURCE')

    def test_reap_timeout_reports_unreaped_pid_in_halt_and_stderr(self):
        stderr=io.StringIO()
        with self.reap_fixture() as f,contextlib.redirect_stderr(stderr):
            f.selector.select.side_effect=self.S.Stop('STOPPED-RESOURCE','fixture stop')
            f.process.wait.side_effect=subprocess.TimeoutExpired('fixture-only',5)
            outcome=self.supervise_reap_fixture()
        self.assertIn('unreaped worker PID 123',stderr.getvalue())
        events,_=self.state()
        halted=next(e for e in events if e['type']=='halted')
        diagnostic=json.loads(Path(halted['diagnostic_path']).read_text())
        self.assertIn('unreaped worker PID 123',diagnostic['message'])
        self.assertEqual(outcome,'STOPPED-RESOURCE')
        f.process.wait.assert_called_once_with(timeout=5)

    def test_reap_timeout_after_exhaustion_names_pid_without_extra_halt_budget(self):
        stderr=io.StringIO()
        with self.reap_fixture() as f,contextlib.redirect_stderr(stderr):
            f.selector.select.side_effect=lambda timeout:self.expire_run(
                self.S.Stop('STOPPED-DEADLINE','fixture run budget exhausted'))
            f.process.wait.side_effect=subprocess.TimeoutExpired('fixture-only',5)
            outcome=self.supervise_reap_fixture()
        self.assertIn('unreaped worker PID 123',stderr.getvalue())
        self.assertEqual(outcome,'STOPPED-DEADLINE')
        events,_=self.state()
        self.assertFalse(any(e['type']=='halted' for e in events))
        f.process.wait.assert_called_once_with(timeout=5)

    def test_reap_before_keyboard_interrupt_is_reraised(self):
        with self.reap_fixture() as f:
            f.selector.select.side_effect=lambda timeout:self.expire_run(KeyboardInterrupt())
            with self.assertRaises(KeyboardInterrupt): self.supervise_reap_fixture()
        f.process.wait.assert_called_once_with(timeout=5)

    def test_reap_before_system_exit_is_reraised(self):
        with self.reap_fixture() as f:
            f.selector.select.side_effect=lambda timeout:self.expire_run(SystemExit(17))
            with self.assertRaises(SystemExit) as raised: self.supervise_reap_fixture()
        f.process.wait.assert_called_once_with(timeout=5)
        self.assertEqual(raised.exception.code,17)

    def broken_stderr(self):
        class BrokenStderr(io.StringIO):
            def write(stream,value): raise OSError('fixture stderr failed')
        return BrokenStderr()

    def assert_control_exit(self,expected,invoke=None):
        caught=None; outcome=None
        try: outcome=(invoke or self.supervise_reap_fixture)()
        except BaseException as error: caught=error
        self.assertIs(caught,expected,f'returned {outcome!r}; raised {caught!r}')

    def constructor_factory(self,f,error=None,before_pid=False):
        created=[]
        class FakePopen:
            def __init__(handle,*args,**kwargs):
                handle.returncode=None; handle.wait=f.process.wait; handle.poll=f.process.poll
                created.append(123)
                if before_pid:
                    self.clock.now=2700
                    signal.getsignal(signal.SIGALRM)(signal.SIGALRM,None)
                handle.pid=123
                if error is not None: raise error
        return FakePopen,created

    def test_constructor_interruption_reaps_created_child(self):
        with self.reap_fixture() as f:
            factory,created=self.constructor_factory(f,self.S.Stop('STOPPED-RESOURCE','constructor after fork'))
            with mock.patch.object(self.S.subprocess,'Popen',factory):
                outcome=self.supervise_reap_fixture()
        self.assertEqual(created,[123])
        f.process.wait.assert_called_once_with(timeout=5)
        f.kill_group.assert_called_with(123,signal.SIGKILL)
        self.assertEqual(outcome,'STOPPED-RESOURCE')

    def test_constructor_system_exit_reaps_child_and_preserves_exit_value(self):
        expected=SystemExit(17)
        with self.reap_fixture() as f:
            factory,created=self.constructor_factory(f,expected)
            with mock.patch.object(self.S.subprocess,'Popen',factory):
                self.assert_control_exit(expected)
        self.assertEqual(created,[123])
        f.process.wait.assert_called_once_with(timeout=5)
        self.assertEqual(expected.code,17)

    def test_constructor_alarm_before_pid_assignment_is_deferred_until_owned(self):
        with self.reap_fixture() as f:
            factory,created=self.constructor_factory(f,before_pid=True)
            with mock.patch.object(self.S.subprocess,'Popen',factory):
                outcome=self.supervise_reap_fixture()
        self.assertEqual(created,[123])
        f.process.wait.assert_called_once_with(timeout=5)
        self.assertEqual(outcome,'STOPPED-DEADLINE')

    def test_system_exit_survives_reap_timeout_and_failing_stderr(self):
        expected=SystemExit(17)
        with self.reap_fixture() as f,contextlib.redirect_stderr(self.broken_stderr()):
            f.selector.select.side_effect=expected
            f.process.wait.side_effect=subprocess.TimeoutExpired('fixture-only',5)
            self.assert_control_exit(expected)
        f.process.wait.assert_called_once_with(timeout=5)
        self.assertEqual(expected.code,17)
        self.assertTrue(any('stderr reporting failed' in n for n in expected.__notes__))

    def test_keyboard_interrupt_survives_signal_failure_and_failing_stderr(self):
        expected=KeyboardInterrupt()
        with self.reap_fixture() as f,contextlib.redirect_stderr(self.broken_stderr()):
            f.selector.select.side_effect=expected
            f.kill_group.side_effect=PermissionError('fixture group denied')
            f.kill_pid.side_effect=PermissionError('fixture PID denied')
            self.assert_control_exit(expected)
        f.process.wait.assert_called_once_with(timeout=5)
        self.assertTrue(any('stderr reporting failed' in n for n in expected.__notes__))

    def test_heartbeat_keyboard_interrupt_survives_double_signal_failure(self):
        expected=KeyboardInterrupt()
        with self.reap_fixture() as f:
            def heartbeat(timeout):
                with mock.patch.object(f.controller,'observe',side_effect=expected): f.heartbeat()
            f.selector.select.side_effect=heartbeat
            f.kill_group.side_effect=PermissionError('fixture group denied')
            f.kill_pid.side_effect=PermissionError('fixture PID denied')
            self.assert_control_exit(expected)
        f.process.wait.assert_called_once_with(timeout=5)
        f.kill_pid.assert_called_with(123,signal.SIGKILL)

    def test_emergency_wait_keyboard_interrupt_overrides_ordinary_stop_after_reap(self):
        expected=KeyboardInterrupt()
        with self.reap_fixture() as f:
            f.selector.select.side_effect=self.S.Stop('STOPPED-RESOURCE','fixture stop')
            f.process.wait.side_effect=[expected,0]
            self.assert_control_exit(expected)
        self.assertEqual(f.process.wait.call_count,2)
        self.assertEqual(f.process.wait.call_args_list[0],mock.call(timeout=5))
        self.assertGreater(f.process.wait.call_args.kwargs['timeout'],0)
        self.assertLessEqual(f.process.wait.call_args.kwargs['timeout'],5)

    def test_emergency_wait_system_exit_overrides_ordinary_stop_after_reap(self):
        expected=SystemExit(23)
        with self.reap_fixture() as f:
            f.selector.select.side_effect=self.S.Stop('STOPPED-RESOURCE','fixture stop')
            f.process.wait.side_effect=[expected,0]
            self.assert_control_exit(expected)
        self.assertEqual(f.process.wait.call_count,2)
        self.assertEqual(expected.code,23)

    def test_original_control_exception_beats_cleanup_control_after_reap(self):
        for original,secondary in ((KeyboardInterrupt(),SystemExit(19)),(SystemExit(17),KeyboardInterrupt())):
            with self.subTest(original=type(original).__name__):
                self.run=self.root/type(original).__name__; self.run.mkdir()
                with self.reap_fixture() as f:
                    f.selector.select.side_effect=original
                    f.process.wait.side_effect=[secondary,0]
                    self.assert_control_exit(original)
                self.assertEqual(f.process.wait.call_count,2)

    def test_cleanup_interrupt_survives_retry_timeout_with_unreaped_pid(self):
        expected=KeyboardInterrupt(); stderr=io.StringIO()
        with self.reap_fixture() as f,contextlib.redirect_stderr(stderr):
            f.selector.select.side_effect=self.S.Stop('STOPPED-RESOURCE','fixture stop')
            f.process.wait.side_effect=[expected,subprocess.TimeoutExpired('fixture-only',5)]
            self.assert_control_exit(expected)
        self.assertEqual(f.process.wait.call_count,2)
        self.assertIn('unreaped worker PID 123',stderr.getvalue())
        events,_=self.state()
        halted=next(e for e in events if e['type']=='halted')
        self.assertIn('unreaped worker PID 123',json.loads(Path(halted['diagnostic_path']).read_text())['message'])

    def test_cleanup_interrupts_share_one_five_second_reap_bound(self):
        expected=KeyboardInterrupt()
        with self.reap_fixture() as f,mock.patch.object(self.S.time,'monotonic',self.clock):
            def wait(*,timeout):
                self.clock.now+=5
                raise expected
            f.selector.select.side_effect=self.S.Stop('STOPPED-RESOURCE','fixture stop')
            f.process.wait.side_effect=wait
            self.assert_control_exit(expected)
        f.process.wait.assert_called_once_with(timeout=5)
        self.assertEqual(self.clock.now,5)

    def test_system_exit_survives_halt_receipt_failure_and_failing_stderr(self):
        expected=SystemExit(17); receipt=self.S.receipt
        with self.reap_fixture() as f,contextlib.redirect_stderr(self.broken_stderr()):
            def fail_receipt(run_dir,kind,data):
                if kind=='halt': raise OSError('fixture halt receipt failed')
                return receipt(run_dir,kind,data)
            f.selector.select.side_effect=expected
            with mock.patch.object(self.S,'receipt',side_effect=fail_receipt): self.assert_control_exit(expected)
        f.process.wait.assert_called_once_with(timeout=5)
        self.assertEqual(expected.code,17)

    def test_postcommit_control_exception_survives_failing_stderr(self):
        for expected in (KeyboardInterrupt(),SystemExit(17)):
            with self.subTest(original=type(expected).__name__):
                self.run=self.root/type(expected).__name__; self.run.mkdir()
                emit=self.S.emit
                def fail_emit(run_dir,kind,**data):
                    if kind=='run_finished':
                        publication=mock.Mock(); publication.committed_outcome.return_value='PASS'
                        data['before_publish'](publication)
                        raise expected
                    return emit(run_dir,kind,**data)
                with mock.patch.object(self.S,'emit',side_effect=fail_emit),contextlib.redirect_stderr(self.broken_stderr()):
                    self.assert_control_exit(expected,self.complete_fixture)

    def test_recorded_outcome_survives_failing_postcommit_stderr(self):
        emit=self.S.emit; original=OSError('fixture postcommit error')
        def fail_emit(run_dir,kind,**data):
            if kind=='run_finished':
                publication=mock.Mock(); publication.committed_outcome.return_value='PASS'
                data['before_publish'](publication)
                raise original
            return emit(run_dir,kind,**data)
        caught=None; outcome=None
        with mock.patch.object(self.S,'emit',side_effect=fail_emit),contextlib.redirect_stderr(self.broken_stderr()):
            try: outcome=self.complete_fixture()
            except BaseException as error: caught=error
        self.assertIsNone(caught)
        self.assertEqual(outcome,'PASS')

    def test_ordinary_error_beats_reap_timeout_with_failing_stderr_and_pid_receipt(self):
        original=self.S.Stop('STOPPED-RESOURCE','fixture stop')
        with self.reap_fixture() as f,contextlib.redirect_stderr(self.broken_stderr()):
            f.selector.select.side_effect=original
            f.process.wait.side_effect=subprocess.TimeoutExpired('fixture-only',5)
            outcome=self.supervise_reap_fixture()
        self.assertEqual(outcome,'STOPPED-RESOURCE')
        self.assertTrue(any('unreaped worker PID 123' in n for n in original.__notes__))
        events,_=self.state()
        halted=next(e for e in events if e['type']=='halted')
        self.assertIn('unreaped worker PID 123',json.loads(Path(halted['diagnostic_path']).read_text())['message'])

    def test_group_cleanup_after_poll_never_signals_reaped_pid(self):
        for failure in (PermissionError,ProcessLookupError):
            with self.subTest(failure=failure.__name__):
                self.run=self.root/failure.__name__; self.run.mkdir()
                with self.reap_fixture() as f:
                    f.process.poll.return_value=0; f.process.returncode=0
                    f.kill_group.side_effect=failure('fixture group signal failure')
                    f.selector.select.side_effect=self.S.Stop('STOPPED-RESOURCE','fixture stop')
                    self.supervise_reap_fixture()
                f.kill_group.assert_called_with(123,signal.SIGKILL)
                f.kill_pid.assert_not_called()
                f.process.wait.assert_called_once_with(timeout=5)

    def test_original_control_survives_socket_close_failure_and_failing_stderr(self):
        expected=SystemExit(17)
        with self.reap_fixture() as f,contextlib.redirect_stderr(self.broken_stderr()):
            f.selector.select.side_effect=expected
            f.parent.close.side_effect=OSError('fixture socket close failed')
            self.assert_control_exit(expected)
        f.process.wait.assert_called_once_with(timeout=5)
        f.child.close.assert_called()

    def test_interrupted_poll_never_signals_pid_released_before_returncode(self):
        import sys
        internal_poll=subprocess.Popen._internal_poll
        for boundary in ('loop-top','loop-eof','heartbeat'):
            with self.subTest(boundary=boundary):
                self.run=self.root/boundary; self.run.mkdir()
                expected=KeyboardInterrupt(); reaped=[]; interrupted=[]; polls=[]
                with self.reap_fixture() as f:
                    f.kill_group.side_effect=PermissionError('fixture group signal denied')
                    f.process._waitpid_lock.acquire.return_value=True
                    f.process._handle_exitstatus.side_effect=lambda status:setattr(f.process,'returncode',0)
                    def waitpid(pid,flags):
                        self.assertEqual((pid,flags),(123,os.WNOHANG))
                        reaped.append(pid)
                        return pid,0
                    def trace(frame,event,arg):
                        if (frame.f_code is internal_poll.__code__ and event=='line'
                                and frame.f_locals.get('pid')==123 and not interrupted):
                            self.assertEqual(reaped,[123])
                            interrupted.append(f.process.returncode)
                            signal.raise_signal(signal.SIGINT)
                        return trace
                    def poll():
                        polls.append(None)
                        if boundary!='loop-top' and len(polls)==1: return None
                        return internal_poll(f.process,_waitpid=waitpid)
                    def wait(*,timeout):
                        f.process.returncode=0
                        return 0
                    f.process.poll.side_effect=poll; f.process.wait.side_effect=wait
                    if boundary=='heartbeat':
                        f.selector.select.side_effect=lambda timeout:f.heartbeat()
                    else:
                        f.selector.select.return_value=[(None,None)]; f.parent.recv.return_value=b''
                    previous_handler=signal.getsignal(signal.SIGINT); previous_trace=sys.gettrace()
                    def interrupt(signum,frame): raise expected
                    try:
                        signal.signal(signal.SIGINT,interrupt); sys.settrace(trace)
                        self.assert_control_exit(expected)
                    finally:
                        sys.settrace(previous_trace); signal.signal(signal.SIGINT,previous_handler)
                self.assertEqual(reaped,[123])
                self.assertEqual(interrupted,[None],'interrupt must land before returncode is stored')
                f.process.wait.assert_called_once_with(timeout=5)
                self.assertEqual(f.kill_pid.call_args_list,[],
                    'released PID was signalled after successful waitpid and pre-returncode SIGINT')

    def test_heartbeat_cleanup_control_overrides_ordinary_stop_after_one_reap(self):
        for expected in (KeyboardInterrupt(),SystemExit(23)):
            with self.subTest(control=type(expected).__name__):
                self.run=self.root/type(expected).__name__; self.run.mkdir()
                caught=None; outcome=None
                with self.reap_fixture() as f:
                    def heartbeat(timeout):
                        with mock.patch.object(f.controller,'observe',
                                side_effect=self.S.Stop('STOPPED-RESOURCE','fixture heartbeat stop')):
                            f.heartbeat()
                    f.selector.select.side_effect=heartbeat
                    f.kill_group.side_effect=PermissionError('fixture group signal denied')
                    f.kill_pid.side_effect=[expected,None]
                    try: outcome=self.supervise_reap_fixture()
                    except BaseException as error: caught=error
                f.process.wait.assert_called_once_with(timeout=5)
                self.assertIs(caught,expected,
                    f'heartbeat cleanup control was swallowed; returned {outcome!r}; raised {caught!r}')
                if isinstance(expected,SystemExit): self.assertEqual(expected.code,23)

    def test_terminate_preserves_signal_exception_over_ordinary_reap_error(self):
        for original in (KeyboardInterrupt(),SystemExit(17),PermissionError('fixture PID signal denied')):
            with self.subTest(original=type(original).__name__):
                caught=None
                with self.reap_fixture() as f:
                    f.kill_group.side_effect=PermissionError('fixture group signal denied')
                    f.kill_pid.side_effect=original
                    f.process.wait.side_effect=OSError('fixture wait failed')
                    try: self.S.terminate(f.process)
                    except BaseException as error: caught=error
                f.process.wait.assert_called_once_with(timeout=5)
                self.assertIs(caught,original,'termination reap replaced the original signal exception')
                if isinstance(original,SystemExit): self.assertEqual(original.code,17)

    def test_pid_fallback_ownership_check_cannot_be_interrupted_by_watchdog_poll(self):
        reaped=[]; signalled=[]
        class Process:
            pid=123
            @property
            def returncode(handle):
                signal.raise_signal(signal.SIGALRM)
                return None
        previous=signal.getsignal(signal.SIGALRM)
        signal.signal(signal.SIGALRM,lambda signum,frame:reaped.append(123))
        def kill(pid,signum):
            self.assertEqual(pid,123)
            self.assertEqual(reaped,[],'watchdog reaped the PID before fallback signalling')
            signalled.append(pid)
        try:
            with mock.patch.object(self.S.os,'killpg',side_effect=ProcessLookupError('fixture missing group')),\
                 mock.patch.object(self.S.os,'kill',side_effect=kill):
                self.S.kill_worker(Process())
        finally: signal.signal(signal.SIGALRM,previous)
        self.assertEqual(signalled,[123])
        self.assertEqual(reaped,[123])


    @contextlib.contextmanager
    def resource_release_fixture(self,f,boundary,error):
        released=[]; path_open=Path.open
        class Selector:
            __exit__=self.S.selectors.BaseSelector.__exit__
            def __enter__(handle): return f.selector
            def close(handle):
                released.append('selector')
                if boundary=='selector': raise error
        class Log:
            def __init__(handle,stream,label): handle.stream=stream; handle.label=label
            def __enter__(handle): return handle.stream.__enter__()
            def __exit__(handle,*args): handle.close()
            def close(handle):
                released.append(handle.label); handle.stream.close()
                if boundary==handle.label: raise error
        def open_log(path,*args,**kwargs):
            stream=path_open(path,*args,**kwargs)
            for label in ('stdout','stderr'):
                if path==self.run/('worker_'+label+'.log'): return Log(stream,label)
            return stream
        f.parent.close.side_effect=lambda:released.append('parent')
        f.child.close.side_effect=lambda:released.append('child')
        with mock.patch.object(self.S.selectors,'DefaultSelector',return_value=Selector()),\
             mock.patch.object(Path,'open',open_log):
            yield released

    @contextlib.contextmanager
    def interrupted_reap_fixture(self,f,internal_poll,expected):
        import sys
        reaped=[]; interrupted=[]
        f.process._waitpid_lock.acquire.return_value=True
        f.process._handle_exitstatus.side_effect=lambda status:setattr(f.process,'returncode',0)
        def waitpid(pid,flags):
            self.assertEqual((pid,flags),(123,os.WNOHANG)); reaped.append(pid)
            return pid,0
        def trace(frame,event,arg):
            if (frame.f_code is internal_poll.__code__ and event=='line'
                    and frame.f_locals.get('pid')==123 and not interrupted):
                self.assertEqual(reaped,[123]); interrupted.append(f.process.returncode)
                signal.raise_signal(signal.SIGINT)
            return trace
        f.process.poll.side_effect=lambda:internal_poll(f.process,_waitpid=waitpid)
        def wait(*,timeout): f.process.returncode=0; return 0
        f.process.wait.side_effect=wait
        previous_handler=signal.getsignal(signal.SIGINT); previous_trace=sys.gettrace()
        def interrupt(signum,frame): raise expected
        try:
            signal.signal(signal.SIGINT,interrupt); sys.settrace(trace)
            yield SimpleNamespace(reaped=reaped,interrupted=interrupted)
        finally:
            sys.settrace(previous_trace); signal.signal(signal.SIGINT,previous_handler)

    def assert_resource_releases(self,released):
        for name in ('selector','stdout','stderr','parent','child'):
            self.assertIn(name,released,'release error prevented a remaining resource release')
        for name in ('selector','stdout','stderr'): self.assertEqual(released.count(name),1)

    def test_resource_release_preserves_control_after_interrupted_poll(self):
        internal_poll=subprocess.Popen._internal_poll
        for boundary in ('selector','stdout','stderr'):
            for expected in (KeyboardInterrupt(),SystemExit(17)):
                with self.subTest(boundary=boundary,control=type(expected).__name__):
                    self.run=self.root/(boundary+type(expected).__name__); self.run.mkdir()
                    caught=None; outcome=None; failure=OSError('fixture '+boundary+' close failed')
                    with self.reap_fixture() as f:
                        f.kill_group.side_effect=PermissionError('fixture group signal denied')
                        with self.resource_release_fixture(f,boundary,failure) as released,\
                             self.interrupted_reap_fixture(f,internal_poll,expected) as replay:
                            try: outcome=self.supervise_reap_fixture()
                            except BaseException as error: caught=error
                    self.assertEqual(replay.reaped,[123]); self.assertEqual(replay.interrupted,[None])
                    f.kill_pid.assert_not_called(); f.process.wait.assert_called_once_with(timeout=5)
                    self.assert_resource_releases(released)
                    self.assertIs(caught,expected,
                        f'{boundary} release lost original control after waitpid; returned {outcome!r}')
                    self.assertTrue(any(str(failure) in note for note in expected.__notes__))
                    if isinstance(expected,SystemExit): self.assertEqual(expected.code,17)

    def test_resource_release_preserves_control_from_heartbeat_cleanup(self):
        for boundary in ('selector','stdout','stderr'):
            for expected in (KeyboardInterrupt(),SystemExit(17)):
                with self.subTest(boundary=boundary,control=type(expected).__name__):
                    self.run=self.root/(boundary+type(expected).__name__); self.run.mkdir()
                    caught=None; outcome=None; failure=OSError('fixture '+boundary+' close failed')
                    with self.reap_fixture() as f:
                        def heartbeat(timeout):
                            with mock.patch.object(f.controller,'observe',
                                    side_effect=self.S.Stop('STOPPED-RESOURCE','fixture heartbeat stop')):
                                f.heartbeat()
                        f.selector.select.side_effect=heartbeat
                        f.kill_group.side_effect=PermissionError('fixture group signal denied')
                        f.kill_pid.side_effect=[expected,None]
                        with self.resource_release_fixture(f,boundary,failure) as released:
                            try: outcome=self.supervise_reap_fixture()
                            except BaseException as error: caught=error
                    f.process.wait.assert_called_once_with(timeout=5)
                    self.assert_resource_releases(released)
                    self.assertIs(caught,expected,
                        f'{boundary} release lost heartbeat cleanup control; returned {outcome!r}')
                    self.assertTrue(any(str(failure) in note for note in expected.__notes__))
                    if isinstance(expected,SystemExit): self.assertEqual(expected.code,17)

    def test_resource_release_precedence_and_unmasked_release_error(self):
        for boundary in ('selector','stdout','stderr'):
            for failure in (OSError('fixture ordinary close failed'),KeyboardInterrupt(),SystemExit(23)):
                with self.subTest(boundary=boundary,release=type(failure).__name__):
                    self.run=self.root/(boundary+type(failure).__name__); self.run.mkdir()
                    original=self.S.Stop('STOPPED-RESOURCE','fixture ordinary stop'); caught=None; outcome=None
                    with self.reap_fixture() as f:
                        f.selector.select.side_effect=original
                        with self.resource_release_fixture(f,boundary,failure) as released:
                            try: outcome=self.supervise_reap_fixture()
                            except BaseException as error: caught=error
                    f.process.wait.assert_called_once_with(timeout=5); self.assert_resource_releases(released)
                    if isinstance(failure,(KeyboardInterrupt,SystemExit)): self.assertIs(caught,failure)
                    else:
                        self.assertEqual(outcome,'STOPPED-RESOURCE','ordinary release replaced original Stop')
                        self.assertTrue(any(str(failure) in note for note in original.__notes__))
        self.run=self.root/'root-close'; self.run.mkdir()
        failure=OSError('fixture unmasked socket close failed')
        with self.reap_fixture() as f:
            f.selector.select.side_effect=self.S.Stop('STOPPED-RESOURCE','fixture already handled stop')
            f.parent.close.side_effect=failure
            caught=None
            try: self.supervise_reap_fixture()
            except BaseException as error: caught=error
        self.assertIs(caught,failure,'release error with no in-flight exception was suppressed')
        f.process.wait.assert_called_once_with(timeout=5); f.child.close.assert_called()

    def supervise_ownership_audit(self,source):
        import ast
        tree=ast.parse(source); function=tree.body[0]; inspected=[]; problems=[]
        def tag(node):
            if isinstance(node,ast.Name): return node.id
            if isinstance(node,ast.Attribute):
                base=tag(node.value) if isinstance(node.value,(ast.Name,ast.Attribute)) else 'expression'
                return base+'.'+node.attr
            if (isinstance(node,ast.BoolOp) and isinstance(node.values[0],ast.Name)
                    and node.values[0].id=='admission'): return 'admission callback'
            return ast.unparse(node)
        safe_calls={
            'Path','Controller','ResourceOwner','ValueError','getattr','str','dict','isinstance','set','Stop',
            'emit','receipt','cpu_admission','admission callback','datetime.now','timedelta','os.getpid',
            'controller.remaining','controller.check','controller.observe','controller.handle_cell',
            'child.fileno','parent.setblocking','parent.recv','parent.sendall',
            'selector.register','selector.unregister','selector.select','buffer.split','message.pop','data.get',
            'run_dir.mkdir','run_dir.resolve','expression.exists','expression.resolve','expression.glob',
            'expression.isoformat','expression.encode','path.is_relative_to','path.read_text',
            'strict_json','sha_file','len','list','min','time.sleep','time.monotonic','any','predictions.values',
            'publish_predictions','durable_json','terminal.committed_outcome','sys.exc_info',
            'kill_worker','poll_worker','terminate','preferred_exception','report_error','error.add_note',
            'process.wait','subprocess.TimeoutExpired','subprocess.Popen.__new__','subprocess.Popen.__init__',
            'resources.scope','resources.context','resources.acquire_many','resources.release','resources.close'
        }
        for node in ast.walk(function):
            if isinstance(node,(ast.With,ast.AsyncWith)):
                for item in node.items:
                    label=ast.unparse(item.context_expr); inspected.append(('with',node.lineno,label))
                    if (not isinstance(item.context_expr,ast.Call)
                            or tag(item.context_expr.func)!='resources.scope'):
                        problems.append(('unowned with',node.lineno,label))
            if isinstance(node,ast.Call):
                label=tag(node.func); inspected.append(('call',node.lineno,label))
                if label not in safe_calls: problems.append(('unreviewed call/acquisition',node.lineno,label))
                if label in ('resources.context','resources.acquire_many'):
                    inspected.append(('owned acquisition',node.lineno,ast.unparse(node.args[0])))
        main_scopes=[node for node in ast.walk(function) if isinstance(node,ast.With)
            and node.body and isinstance(node.body[0],ast.Expr)
            and isinstance(node.body[0].value,ast.Call)
            and tag(node.body[0].value.func)=='resources.context'
            and isinstance(node.body[0].value.args[0],ast.Name)
            and node.body[0].value.args[0].id=='worker_lifetime']
        allocations=[node for node in ast.walk(function) if isinstance(node,ast.Assign)
            and isinstance(node.value,ast.Call) and tag(node.value.func)=='subprocess.Popen.__new__']
        if len(main_scopes)!=1 or len(allocations)!=1:
            problems.append(('unowned worker allocation',function.lineno,'lifetime registration/preallocation'))
        elif (not any(node is allocations[0] for node in ast.walk(main_scopes[0]))
                or [ast.unparse(target) for target in allocations[0].targets]!=['process']):
            problems.append(('unowned worker allocation',allocations[0].lineno,'preallocated handle escaped lifetime'))
        constructors=[node for node in ast.walk(function) if isinstance(node,ast.With) and node.body
            and isinstance(node.body[0],ast.Expr) and isinstance(node.body[0].value,ast.Call)
            and tag(node.body[0].value.func)=='resources.context'
            and isinstance(node.body[0].value.args[0],ast.Name)
            and node.body[0].value.args[0].id=='constructor_ownership']
        if len(constructors)!=1: problems.append(('unowned constructor',function.lineno,'constructor signal context'))
        roots=[node for node in function.body if isinstance(node,ast.Try) and node.finalbody]
        if len(roots)!=1 or not any(isinstance(node,ast.Call) and tag(node.func)=='resources.close'
                for statement in roots[0].finalbody for node in ast.walk(statement)):
            problems.append(('unowned root release',function.lineno,'socket owner final drain'))
        return inspected,problems

    def test_supervise_resource_acquisitions_share_precedence_owner(self):
        import inspect,textwrap
        source=textwrap.dedent(inspect.getsource(self.S.supervise))
        inspected,problems=self.supervise_ownership_audit(source)
        for kind,lineno,label in inspected:
            print(f'OWNERSHIP_AST {kind} tools/new1_supervisor.py:{self.S.supervise.__code__.co_firstlineno+lineno-1} {label}')
        self.assertEqual(problems,[],'supervise has a cleanup boundary/acquisition outside the single owner')
        for addition in ('\n    with arbitrary_factory():\n        pass\n',
                '\n    escaped=arbitrary_factory()\n',
                '\n    escaped=(run_dir/"extra.log").open("xb")\n',
                '\n    parent.close()\n'):
            with self.subTest(mutant=addition.strip()):
                _,mutant_problems=self.supervise_ownership_audit(source+addition)
                self.assertTrue(mutant_problems,'structural guard accepted an unmanaged boundary/acquisition')


if __name__=='__main__': unittest.main()
