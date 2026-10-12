# MB27 NEW1 supervisor reap build

Status: BUILD DONE; final fixture suite 76/76 GREEN. All 15 new regressions are RED on the exact frozen supervisor, with all 61 pre-existing tests passing in both RED and GREEN. This is the separately scoped lifecycle work requested by Astra r8 Q4 (:55) and condition 3 (:71), not a worker launch or scientific result.

Branch/worktree verified: `worktree-c10k-route-a`, `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a`.

## Verified findings and paths

The original wait at tools/new1_supervisor.py:418 depended on `Controller.remaining()` twice. Either total or cell deadline exhaustion skips it entirely. The heartbeat signals without waiting; signalling exceptions and closeout alarm setup also skip the exception wait. Failed loop termination leaves reaping unfinished and can consume the budget that the exception handler formerly required.

Original line citations below refer to the SHA-pinned copies under `before/`. Final line citations refer to the current worktree source.

| Path or boundary | Frozen source | Final enforcement | Regression |
| --- | --- | --- | --- |
| Total run budget spent before exception closeout | before/new1_supervisor.py:202-204, 413-418 | tools/new1_supervisor.py worker_lifetime:315-339; bounded wait:329; halt budget:452 | `test_reap_after_deadline_exhaustion` (tests/test_new1_supervisor.py:946) |
| Cell-wait budget spent before exception closeout | before/new1_supervisor.py:205-208, 413-418 | tools/new1_supervisor.py same independent wait at :329; Controller limits unchanged | `test_reap_after_cell_deadline_exhaustion` (tests/test_new1_supervisor.py:959) |
| Heartbeat signals and sets kill_sent, but exhausted budget prevents exception wait | before/new1_supervisor.py:305-314, 413-418 | tools/new1_supervisor.py heartbeat:344-350; lifetime waits even when kill_sent is true | `test_reap_after_heartbeat_kill_at_exhausted_deadline` (tests/test_new1_supervisor.py:969) |
| Heartbeat group signal raises and exception cleanup signal raises again | before/new1_supervisor.py:311-314, 414-418 | tools/new1_supervisor.py owned-PID fallback:268-273; lifetime:315-339 | `test_reap_when_heartbeat_group_signal_is_denied` (tests/test_new1_supervisor.py:980) |
| Exception cleanup group signal raises before wait | before/new1_supervisor.py:413-418 | tools/new1_supervisor.py signal failure cannot bypass wait:323-329 | `test_reap_when_exception_group_signal_is_denied` (tests/test_new1_supervisor.py:992) |
| Loop terminate group signal raises before its wait and before exception wait | before/new1_supervisor.py:264-268, 345, 384, 414-418 | tools/new1_supervisor.py terminate waits in finally:276-279; fallback:268-273 | `test_reap_when_loop_termination_group_signal_is_denied` (tests/test_new1_supervisor.py:1015) |
| Loop terminate wait times out, spends remaining budget, and exception cannot finish reaping | before/new1_supervisor.py:268, 345, 384, 417-418 | tools/new1_supervisor.py independent lifetime wait:329 follows failed loop termination | `test_reap_when_termination_wait_timeout_exhausts_budget` (tests/test_new1_supervisor.py:1024) |
| Exception closeout alarm setup raises before wait | before/new1_supervisor.py:95-99, 417-418 | tools/new1_supervisor.py lifetime exits before closeout alarm setup:353, 452 | `test_reap_when_closeout_deadline_setup_raises` (tests/test_new1_supervisor.py:1039) |
| KeyboardInterrupt is re-raised after budget exhaustion without wait | before/new1_supervisor.py:417-418, 425 | tools/new1_supervisor.py lifetime exits before exception handler; re-raise retained:459 | `test_reap_before_keyboard_interrupt_is_reraised` (tests/test_new1_supervisor.py:1109) |
| SystemExit is re-raised after budget exhaustion without wait | before/new1_supervisor.py:417-418, 425 | tools/new1_supervisor.py lifetime exits before exception handler; original exit value retained | `test_reap_before_system_exit_is_reraised` (tests/test_new1_supervisor.py:1115) |
| Group/PID signalling errors and reporting IO must not preempt wait | before/new1_supervisor.py:414-424 (group failure skips wait) | tools/new1_supervisor.py errors are held until after wait:326-339; reporting at :334-339 | `test_reap_before_reporting_group_and_pid_signal_failures` (tests/test_new1_supervisor.py:1001) |
| Reap timeout lacks PID diagnostic and skips halt persistence despite positive budget | before/new1_supervisor.py:418-424 | tools/new1_supervisor.py unreaped PID:331-338; included in halt diagnostic:449-458 | `test_reap_timeout_reports_unreaped_pid_in_halt_and_stderr` (tests/test_new1_supervisor.py:1082) |
| Exhausted budget plus failed bounded reap still must identify unreaped PID | before/new1_supervisor.py:417-424 | tools/new1_supervisor.py stderr includes PID; original zero halt budget is retained | `test_reap_timeout_after_exhaustion_names_pid_without_extra_halt_budget` (tests/test_new1_supervisor.py:1096) |
| Halt receipt raises after wait (audited: not an independent original skip) | before/new1_supervisor.py:418-419, 423-424 | tools/new1_supervisor.py wait finishes before receipt; fixed five-second bound | `test_reap_when_halt_receipt_raises` (tests/test_new1_supervisor.py:1054) |
| Halt emit raises after wait (audited: not an independent original skip) | before/new1_supervisor.py:418-422, 423-424 | tools/new1_supervisor.py wait finishes before emit; fixed five-second bound | `test_reap_when_halt_emit_raises` (tests/test_new1_supervisor.py:1068) |

Post-commit recorded-outcome return is also audited: frozen :402-410, final :439-447. On the real control flow it follows successful loop teardown (:345 or :384 frozen; :382 or :421 final), so it was not an independent original skip. The terminal-commit authority block is unchanged. The new lifetime context has exited before the exception handler reconciles the committed outcome. Existing post-commit, IO-failure, and publication-deadline regressions remain GREEN. Normal successful teardown remains covered by `test_successful_exit_at_loop_bottom_still_terminates_group` (final tests/test_new1_supervisor.py:896), which still asserts one wait. Receipt/emit regressions above were RED because their wait used remaining run time rather than the required fixed bound; the original receipt/emit calls already followed the wait.

## Reap rule and durability

`REAP_TIMEOUT_S = 5`: SIGKILLed processes exit promptly; five seconds is short and retains the pre-existing `terminate` wait bound. Every post-SIGKILL wait now uses this fixed value, without consulting the remaining run budget. The lifetime context surrounds the run alarm, so the alarm is removed before emergency reaping. Successful loop teardown marks the worker reaped and avoids a redundant wait; a failed loop wait may be followed by one separately bounded emergency wait. The first wait remains inside the original run deadline. Signalling uses the reviewed group-kill/owned-PID fallback from tools/new1_identity_diag.py:278-283, and even signalling/reporting failures cannot preempt the wait attempt.

An unsuccessful emergency wait identifies `unreaped worker PID <pid>` in stderr and in the halt diagnostic message when the original budget still permits persistence. It preserves the original halt code/raised interruption. At zero original remaining budget, a new durable halt receipt cannot be written under the retained durability rule: stderr carries the enriched halt diagnostic, names the unreaped PID, and reports closeout incomplete. The exhausted-budget timeout test explicitly verifies that no extra halt-persistence budget is borrowed. No timeout is treated as a successful reap.

The 2,700-second total, 300-second cell wait, resource caps, event names, outcome vocabulary, exit behavior, and terminal-commit authority are unchanged. Only reaping gets a separate fixed bound; halt receipt/event durability uses `hard_deadline(controller.remaining())` exactly as before.

## Source identity and scope

| File | Start SHA-256 (verified before first edit) | Final SHA-256 |
| --- | --- | --- |
| tools/new1_supervisor.py | `a69d410724b65a5dbacaf8e34fc45b73c9f545daf54eda9b6cfeb150e344557b` | `da9f250e244b8e29392e13dbba83ceb90e6980fdfee2b43fa66a3feed3c86a9c` |
| tests/test_new1_supervisor.py | `33c61282862cea1d0297396cb860963bfc48adf33d054db3f933fed11d6d23ec` | `c3440f6bc8afc5c476257865121249d0f98299a05a4b52a3835d7637074eccd5` |

MB27 wrote only these two code files and this fresh receipt directory. Frozen copies are under `before/`; the final failing-first test source is also saved as `RED_final_tests.py`. `GREEN_first_source.py` preserves the intermediate 75-test GREEN source. The additional signal-reporting regression and final change were introduced after static inspection of that intermediate build. MB26 geometry files and tools/test_dashboard_mathlab.py were left alone. No commit, push, merge, or external process kill was performed.

## RED and GREEN evidence

Every invocation used exactly:

```sh
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B -m unittest -v tests.test_new1_supervisor
```

Each log contains one complete invocation with combined stdout/stderr; the command's real exit status was captured. Bytecode was disabled. No other suite ran. Added tests use the existing fake-process/clock pattern, fake Popen, and intercepted group/PID signals; they launch no process. Pre-existing subprocess fixtures remain part of the authorized suite.

| Log path | Exit | Tests | Result |
| --- | --- | --- | --- |
| results/mathlab_staging/new1_supervisor_reap_20261010T204549Z/RED.log | 1 | 75 | 61 pass; 14 new failures; 0 errors |
| results/mathlab_staging/new1_supervisor_reap_20261010T204549Z/GREEN.log | 0 | 75 | 75 pass; 0 failures; 0 errors |
| results/mathlab_staging/new1_supervisor_reap_20261010T204549Z/RED_final.log | 1 | 76 | 61 pass; all 15 new failures; 0 errors |
| results/mathlab_staging/new1_supervisor_reap_20261010T204549Z/GREEN_final.log | 0 | 76 | 76 pass; 0 failures; 0 errors |

Final RED/GREEN membership was checked mechanically: the 15 added method names exactly equal the 15 RED failure names; no errors or pre-existing failures; final GREEN has 76 tests and OK. The baseline's 64 test/class/setup declaration lines contain 61 actual tests. `evidence.json` binds each log to the source hashes, exit status, counts, and log SHA-256.

## Limits and reviewer handoff

UNVERIFIED: real full-worker enforcement on the host and Astra's binding lifecycle/readiness review. The fixture result is build evidence for MAESTRO24; Condition 3 still requires review before launch. MAESTRO verifies and commits; GPT-6-Astra reviews. No NEW-1 model/geometry worker or scientific run was launched by this task.

Known remaining implementation issues in this scope: none found after the final path audit. No test is failing or half-applied. Next step: MAESTRO24 verifies this receipt and final source identities on the host, then submits the lifecycle change to Astra for review before any separately authorized launch.

## Final diff against frozen source

```diff
--- results/mathlab_staging/new1_supervisor_reap_20261010T204549Z/before/new1_supervisor.py	2026-10-10 14:46:44
+++ tools/new1_supervisor.py	2026-10-10 14:52:08
@@ -36,6 +36,10 @@
     def __init__(self, code, message):
         self.code = code
         super().__init__(code + ': ' + message)
+
+
+# SIGKILL exits promptly; reaping gets at most five seconds even after run expiry.
+REAP_TIMEOUT_S = 5
 
 
 @dataclass(frozen=True)
@@ -261,11 +265,18 @@
         return self.wait_cell(message['phase'], message['cell'], pid)
 
 
+def kill_worker(pid):
+    try: os.killpg(pid, signal.SIGKILL)
+    except (ProcessLookupError, PermissionError):
+        # A group signal can be refused while the owned PID remains signalable.
+        try: os.kill(pid, signal.SIGKILL)
+        except ProcessLookupError: pass
+
+
 def terminate(process):
     """Stop the whole isolated group immediately, then reap the direct worker."""
-    try: os.killpg(process.pid, signal.SIGKILL)
-    except ProcessLookupError: pass
-    process.wait(timeout=5)
+    try: kill_worker(process.pid)
+    finally: process.wait(timeout=REAP_TIMEOUT_S)
 
 
 def publish_predictions(run_dir, path):
@@ -296,8 +307,36 @@
     controller = Controller(run_dir, monitor=monitor)
     process = None
     kill_sent = False
+    worker_reaped = False
+    reap_error = None
     terminal = None
     parent, child = socket.socketpair()
+    @contextlib.contextmanager
+    def worker_lifetime():
+        nonlocal kill_sent, worker_reaped, reap_error
+        try: yield
+        finally:
+            if process is not None and not worker_reaped:
+                original_error = sys.exc_info()[1]
+                signal_error = None
+                wait_error = None
+                try:
+                    if not kill_sent:
+                        kill_worker(process.pid); kill_sent=True
+                except BaseException as error:
+                    signal_error = error
+                try:
+                    process.wait(timeout=REAP_TIMEOUT_S)
+                    worker_reaped=True
+                except BaseException as error:
+                    wait_error = error
+                    reap_error = f'unreaped worker PID {process.pid}: {error}'
+                if signal_error is not None:
+                    print(f'Worker PID {process.pid} signal failed: {signal_error}',file=sys.stderr)
+                if wait_error is not None:
+                    print(reap_error,file=sys.stderr)
+                    if original_error is None: raise wait_error
+                if signal_error is not None and original_error is None: raise signal_error
     def terminal_ready(publication):
         nonlocal terminal
         controller.remaining()
@@ -307,13 +346,11 @@
         try: controller.observe(process.pid if process is not None and process.poll() is None else None)
         except BaseException:
             if process is not None and not kill_sent:
-                try:
-                    os.killpg(process.pid,signal.SIGKILL)
-                    kill_sent=True
-                except ProcessLookupError: pass
+                kill_worker(process.pid); kill_sent=True
             raise
     try:
-        with hard_deadline(controller.remaining(),heartbeat=heartbeat,budget=controller.remaining):
+        # Exit the run alarm before the lifetime's separately bounded reap.
+        with worker_lifetime(), hard_deadline(controller.remaining(),heartbeat=heartbeat,budget=controller.remaining):
             emit(run_dir, 'run_started', step=4, title='NEW1 adapter geometry — math estimate, not evidence',
                  deadline_ts=(datetime.now(timezone.utc)+timedelta(seconds=controller.remaining())).isoformat(),
                  pid=os.getpid(), purpose='experiment')
@@ -342,7 +379,7 @@
                         remaining = controller.remaining()
                         if process.poll() is not None and not worker_exited:
                             # Reparented group members may retain IPC after their leader exits.
-                            terminate(process); worker_exited=True; kill_sent=True
+                            terminate(process); worker_exited=True; kill_sent=True; worker_reaped=True
                         if time.monotonic()-last_sample >= SAMPLE_S and not worker_exited:
                             controller.check(process.pid); last_sample=time.monotonic()
                         ready=selector.select(min(.1,remaining)) if not eof else []
@@ -381,7 +418,7 @@
                             if buffer or process.returncode or complete is None:
                                 raise Stop('INVALID-WORKER','partial IPC, unsuccessful exit or missing final artifact')
                             if not kill_sent:
-                                terminate(process); worker_exited=True; kill_sent=True
+                                terminate(process); worker_exited=True; kill_sent=True; worker_reaped=True
                             break
                         if eof: time.sleep(min(.05,controller.remaining()))
             predictions=publish_predictions(run_dir,complete)
@@ -409,19 +446,16 @@
                     if isinstance(error,(KeyboardInterrupt,SystemExit)): raise
                     return recorded
         code=getattr(error,'code','INVALID-WORKER')
+        message=str(error) + ('; '+reap_error if reap_error is not None else '')
         try:
-            if process is not None and not kill_sent:
-                try: os.killpg(process.pid,signal.SIGKILL)
-                except ProcessLookupError: pass
-            # Cleanup and halt durability consume only the original remaining budget.
+            # Halt durability consumes only the original remaining budget.
             with hard_deadline(controller.remaining()):
-                if process is not None: process.wait(timeout=controller.remaining())
-                diagnostic=receipt(run_dir,'halt',{'code':code,'message':str(error),
+                diagnostic=receipt(run_dir,'halt',{'code':code,'message':message,
                     'observed':getattr(error,'observed',None),'prediction_verdict':'NOT COMPUTED'})
                 controller.remaining()
-                emit(run_dir,'halted',reason=code+': '+str(error),diagnostic_path=diagnostic['path'])
+                emit(run_dir,'halted',reason=code+': '+message,diagnostic_path=diagnostic['path'])
         except BaseException as closeout_error:
-            print(f'{code}: {error}; closeout incomplete: {closeout_error}; no prediction verdict',file=sys.stderr)
+            print(f'{code}: {message}; closeout incomplete: {closeout_error}; no prediction verdict',file=sys.stderr)
         if isinstance(error,(KeyboardInterrupt,SystemExit)): raise
         return code
     finally:

--- results/mathlab_staging/new1_supervisor_reap_20261010T204549Z/before/test_new1_supervisor.py	2026-10-10 14:46:44
+++ tests/test_new1_supervisor.py	2026-10-10 14:51:35
@@ -12,6 +12,7 @@
 import tempfile
 import time
 import unittest
+from types import SimpleNamespace
 from unittest import mock
 
 from tools.mathlab_events import read_events, fold
@@ -910,6 +911,213 @@
         self.assertEqual(outcome,'PASS')
         kill.assert_called_once_with(123,signal.SIGKILL)
         process.wait.assert_called_once()
+
+    @contextlib.contextmanager
+    def reap_fixture(self):
+        parent=mock.Mock(); child=mock.Mock(); child.fileno.return_value=99
+        process=mock.Mock(pid=123,returncode=None)
+        process.poll.return_value=None; process.wait.return_value=0
+        selector=mock.MagicMock(); selected=selector.__enter__.return_value
+        controller=self.S.Controller(self.run,clock=self.clock,sleep=self.clock.sleep,
+            monitor=lambda pid:self.S.Sample(13,0,0))
+        watchdog={}; hard_deadline=self.S.hard_deadline
+        @contextlib.contextmanager
+        def deadline(seconds,**kwargs):
+            if 'heartbeat' in kwargs: watchdog['callback']=kwargs['heartbeat']
+            with hard_deadline(seconds,**kwargs): yield
+        with mock.patch.object(self.S.socket,'socketpair',return_value=(parent,child)),\
+             mock.patch.object(self.S.subprocess,'Popen',return_value=process),\
+             mock.patch.object(self.S.selectors,'DefaultSelector',return_value=selector),\
+             mock.patch.object(self.S,'Controller',return_value=controller),\
+             mock.patch.object(self.S,'hard_deadline',side_effect=deadline),\
+             mock.patch.object(self.S.os,'killpg') as kill_group,\
+             mock.patch.object(self.S.os,'kill') as kill_pid:
+            yield SimpleNamespace(process=process,selector=selected,controller=controller,
+                kill_group=kill_group,kill_pid=kill_pid,heartbeat=lambda:watchdog['callback']())
+
+    def expire_run(self,error):
+        self.clock.now=2700
+        raise error
+
+    def supervise_reap_fixture(self):
+        return self.S.supervise(['fixture-only'],self.run,
+            admission=lambda:{'allowed':True,'reasons':[]})
+
+    def test_reap_after_deadline_exhaustion(self):
+        stderr=io.StringIO()
+        with self.reap_fixture() as f,contextlib.redirect_stderr(stderr):
+            f.selector.select.side_effect=lambda timeout:self.expire_run(
+                self.S.Stop('STOPPED-DEADLINE','fixture run budget exhausted'))
+            outcome=self.supervise_reap_fixture()
+        f.process.wait.assert_called_once_with(timeout=5)
+        f.kill_group.assert_called_with(123,signal.SIGKILL)
+        self.assertEqual(outcome,'STOPPED-DEADLINE')
+        events,_=self.state()
+        self.assertFalse(any(e['type']=='halted' for e in events))
+        self.assertIn('closeout incomplete',stderr.getvalue())
+
+    def test_reap_after_cell_deadline_exhaustion(self):
+        with self.reap_fixture() as f:
+            def expire_cell(timeout):
+                f.controller.cell_deadline=300; self.clock.now=300
+                raise self.S.Stop('STOPPED-RESOURCE','fixture cell wait exhausted')
+            f.selector.select.side_effect=expire_cell
+            outcome=self.supervise_reap_fixture()
+        f.process.wait.assert_called_once_with(timeout=5)
+        self.assertEqual(outcome,'STOPPED-RESOURCE')
+
+    def test_reap_after_heartbeat_kill_at_exhausted_deadline(self):
+        with self.reap_fixture() as f:
+            def heartbeat(timeout):
+                self.clock.now=2700
+                f.heartbeat()
+            f.selector.select.side_effect=heartbeat
+            outcome=self.supervise_reap_fixture()
+        f.process.wait.assert_called_once_with(timeout=5)
+        f.kill_group.assert_called_with(123,signal.SIGKILL)
+        self.assertEqual(outcome,'STOPPED-DEADLINE')
+
+    def test_reap_when_heartbeat_group_signal_is_denied(self):
+        with self.reap_fixture() as f:
+            f.kill_group.side_effect=PermissionError('fixture group signal denied')
+            def heartbeat(timeout):
+                f.controller.monitor=lambda pid:(_ for _ in ()).throw(
+                    self.S.Stop('STOPPED-RESOURCE','fixture watchdog stop'))
+                f.heartbeat()
+            f.selector.select.side_effect=heartbeat
+            self.supervise_reap_fixture()
+        f.process.wait.assert_called_once_with(timeout=5)
+        f.kill_pid.assert_called_with(123,signal.SIGKILL)
+
+    def test_reap_when_exception_group_signal_is_denied(self):
+        with self.reap_fixture() as f:
+            f.kill_group.side_effect=PermissionError('fixture group signal denied')
+            f.selector.select.side_effect=self.S.Stop('STOPPED-RESOURCE','fixture stop')
+            outcome=self.supervise_reap_fixture()
+        f.process.wait.assert_called_once_with(timeout=5)
+        f.kill_pid.assert_called_with(123,signal.SIGKILL)
+        self.assertEqual(outcome,'STOPPED-RESOURCE')
+
+    def test_reap_before_reporting_group_and_pid_signal_failures(self):
+        with self.reap_fixture() as f:
+            class AfterReapStderr(io.StringIO):
+                def write(stream,value):
+                    if value.strip(): f.process.wait.assert_called_once_with(timeout=5)
+                    return super().write(value)
+            f.kill_group.side_effect=PermissionError('fixture group signal denied')
+            f.kill_pid.side_effect=PermissionError('fixture PID signal denied')
+            f.selector.select.side_effect=self.S.Stop('STOPPED-RESOURCE','fixture stop')
+            with contextlib.redirect_stderr(AfterReapStderr()):
+                outcome=self.supervise_reap_fixture()
+        f.process.wait.assert_called_once_with(timeout=5)
+        self.assertEqual(outcome,'STOPPED-RESOURCE')
+
+    def test_reap_when_loop_termination_group_signal_is_denied(self):
+        with self.reap_fixture() as f:
+            f.process.poll.return_value=0
+            f.kill_group.side_effect=PermissionError('fixture group signal denied')
+            f.selector.select.side_effect=self.S.Stop('STOPPED-RESOURCE','fixture stop after leader exit')
+            self.supervise_reap_fixture()
+        f.process.wait.assert_called_once_with(timeout=5)
+        f.kill_pid.assert_called_with(123,signal.SIGKILL)
 
+    def test_reap_when_termination_wait_timeout_exhausts_budget(self):
+        with self.reap_fixture() as f:
+            f.process.poll.return_value=0
+            attempts=[]
+            def wait(*,timeout):
+                attempts.append(timeout)
+                if len(attempts)==1:
+                    self.clock.now=2700
+                    raise subprocess.TimeoutExpired('fixture-only',timeout)
+                return 0
+            f.process.wait.side_effect=wait
+            outcome=self.supervise_reap_fixture()
+        self.assertEqual(attempts,[5,5])
+        self.assertEqual(outcome,'INVALID-WORKER')
 
+    def test_reap_when_closeout_deadline_setup_raises(self):
+        with self.reap_fixture() as f:
+            deadline=self.S.hard_deadline; calls=[]
+            @contextlib.contextmanager
+            def failing_closeout(seconds,**kwargs):
+                calls.append(seconds)
+                if len(calls)==2:
+                    raise self.S.Stop('INVALID-ENFORCEMENT','fixture closeout alarm refused')
+                with deadline(seconds,**kwargs): yield
+            f.selector.select.side_effect=self.S.Stop('STOPPED-RESOURCE','fixture stop')
+            with mock.patch.object(self.S,'hard_deadline',side_effect=failing_closeout):
+                outcome=self.supervise_reap_fixture()
+        f.process.wait.assert_called_once_with(timeout=5)
+        self.assertEqual(outcome,'STOPPED-RESOURCE')
+
+    def test_reap_when_halt_receipt_raises(self):
+        receipt=self.S.receipt
+        with self.reap_fixture() as f:
+            def fail_receipt(run_dir,kind,data):
+                if kind=='halt':
+                    f.process.wait.assert_called_once_with(timeout=5)
+                    raise OSError('fixture halt receipt failed')
+                return receipt(run_dir,kind,data)
+            f.selector.select.side_effect=self.S.Stop('STOPPED-RESOURCE','fixture stop')
+            with mock.patch.object(self.S,'receipt',side_effect=fail_receipt):
+                outcome=self.supervise_reap_fixture()
+        f.process.wait.assert_called_once_with(timeout=5)
+        self.assertEqual(outcome,'STOPPED-RESOURCE')
+
+    def test_reap_when_halt_emit_raises(self):
+        emit=self.S.emit
+        with self.reap_fixture() as f:
+            def fail_emit(run_dir,kind,**data):
+                if kind=='halted':
+                    f.process.wait.assert_called_once_with(timeout=5)
+                    raise OSError('fixture halt emit failed')
+                return emit(run_dir,kind,**data)
+            f.selector.select.side_effect=self.S.Stop('STOPPED-RESOURCE','fixture stop')
+            with mock.patch.object(self.S,'emit',side_effect=fail_emit):
+                outcome=self.supervise_reap_fixture()
+        f.process.wait.assert_called_once_with(timeout=5)
+        self.assertEqual(outcome,'STOPPED-RESOURCE')
+
+    def test_reap_timeout_reports_unreaped_pid_in_halt_and_stderr(self):
+        stderr=io.StringIO()
+        with self.reap_fixture() as f,contextlib.redirect_stderr(stderr):
+            f.selector.select.side_effect=self.S.Stop('STOPPED-RESOURCE','fixture stop')
+            f.process.wait.side_effect=subprocess.TimeoutExpired('fixture-only',5)
+            outcome=self.supervise_reap_fixture()
+        self.assertIn('unreaped worker PID 123',stderr.getvalue())
+        events,_=self.state()
+        halted=next(e for e in events if e['type']=='halted')
+        diagnostic=json.loads(Path(halted['diagnostic_path']).read_text())
+        self.assertIn('unreaped worker PID 123',diagnostic['message'])
+        self.assertEqual(outcome,'STOPPED-RESOURCE')
+        f.process.wait.assert_called_once_with(timeout=5)
+
+    def test_reap_timeout_after_exhaustion_names_pid_without_extra_halt_budget(self):
+        stderr=io.StringIO()
+        with self.reap_fixture() as f,contextlib.redirect_stderr(stderr):
+            f.selector.select.side_effect=lambda timeout:self.expire_run(
+                self.S.Stop('STOPPED-DEADLINE','fixture run budget exhausted'))
+            f.process.wait.side_effect=subprocess.TimeoutExpired('fixture-only',5)
+            outcome=self.supervise_reap_fixture()
+        self.assertIn('unreaped worker PID 123',stderr.getvalue())
+        self.assertEqual(outcome,'STOPPED-DEADLINE')
+        events,_=self.state()
+        self.assertFalse(any(e['type']=='halted' for e in events))
+        f.process.wait.assert_called_once_with(timeout=5)
+
+    def test_reap_before_keyboard_interrupt_is_reraised(self):
+        with self.reap_fixture() as f:
+            f.selector.select.side_effect=lambda timeout:self.expire_run(KeyboardInterrupt())
+            with self.assertRaises(KeyboardInterrupt): self.supervise_reap_fixture()
+        f.process.wait.assert_called_once_with(timeout=5)
+
+    def test_reap_before_system_exit_is_reraised(self):
+        with self.reap_fixture() as f:
+            f.selector.select.side_effect=lambda timeout:self.expire_run(SystemExit(17))
+            with self.assertRaises(SystemExit) as raised: self.supervise_reap_fixture()
+        f.process.wait.assert_called_once_with(timeout=5)
+        self.assertEqual(raised.exception.code,17)
+
+
 if __name__=='__main__': unittest.main()
```

## Context saved for MAESTRO24 / successor

Done: 15 failing-first regressions, independently bounded reaping, signal fallback, PID diagnostics, final 76/76 GREEN, source identities, full diff, and saved logs. Half-applied/in-flight work: none. Exact paths, SHA-256 values, commands, and log counts are above and in evidence.json. Failing tests: none on final source; all 15 deliberate RED failures are preserved in RED_final.log. Open risk: fixture evidence does not replace host enforcement or binding Astra review. Next step is the MAESTRO/Astra review described above.

Binding context directive, restated: watch "Context N% left". Start a new piece of work only at 60% left or more. At 40% left or less, stop starting work; write a handoff at the end of this README with done/half-applied work, exact paths and SHA-256, failing tests and exact commands, and next step; reply exactly "CONTEXT HANDOFF WRITTEN". If "Context compacted" appears, do this immediately without another edit or test. The AGENTS.md context-management directive also binds every team session: stop before full-window compaction, preserve a precise handoff, and restate the directive in every subsequent handoff.
