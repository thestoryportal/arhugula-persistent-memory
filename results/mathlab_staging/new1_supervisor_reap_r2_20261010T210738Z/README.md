# MB27 supervisor reap R2 — MAESTRO25

BUILD DONE: 94/94 fixture tests GREEN. Astra binding re-review and host verification remain OPEN. Read the complete 75-line r10 verdict before choosing the implementation; verified branch/worktree and the two source pins before editing. Round-1 accepted lifetime/reap/receipt ordering remains intact.

## Finding 1 — constructor ownership

Choice: retain the handle before construction, and protect the pre-PID signal interval. tools/new1_supervisor.py:441 assigns a preallocated Popen object before explicit __init__. tools/new1_supervisor.py:281 defers raising callable signal handlers only while pid is absent, retries pending delivery in 1 ms, then forwards handlers normally once pid exists. It restores the original handlers and applies control-exception precedence on all constructor exits. tools/new1_supervisor.py:369 then cleans up partially initialized handles that have a PID. Later constructor IO remains interruptible. No signal mask is inherited through creation; the original absolute run deadline is not reset.

Why: the installed CPython /Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/subprocess.py:1026-1062 and :1883-1958 was read directly. It assigns self.pid at :1885 before error-pipe reads at :1908. The constructor exception handler at :1036 closes descriptors and re-raises without guaranteed termination/reaping. Preallocation gives cleanup the handle after child creation even if __init__ raises. Signal deferral covers the C-spawn-return/PID-store gap without making later constructor IO uninterruptible.

Tests explicitly create a fake child identity before raising or invoking the alarm; none merely raises before child creation:

- `test_constructor_interruption_reaps_created_child` (tests/test_new1_supervisor.py:1153)
- `test_constructor_system_exit_reaps_child_and_preserves_exit_value` (tests/test_new1_supervisor.py:1163)
- `test_constructor_alarm_before_pid_assignment_is_deferred_until_owned` (tests/test_new1_supervisor.py:1173)

## Finding 2 — precedence and best-effort reporting

The selector is tools/new1_supervisor.py:268; emergency cleanup is tools/new1_supervisor.py:365; reporting is tools/new1_supervisor.py:274. Reporting failures are attached as exception notes, including the attempted diagnostic, rather than silently passed or used as replacement errors. Heartbeat kill failures are noted on the original exception at tools/new1_supervisor.py:418, followed by its bare re-raise. Reporting remains after the wait attempt.

| Priority | Result |
| --- | --- |
| Original control | Original KeyboardInterrupt/SystemExit wins unchanged: same object and exit value. |
| Cleanup control | Without an original control exception, the first cleanup control exception propagates after bounded reaping. |
| Original ordinary | Otherwise, the original ordinary error beats secondary signalling/reap errors, including timeout. |
| No original | The first cleanup error governs. |
| Printing | Failure becomes an exception note and never chooses the governing exception. |

Astra finding-2's four explicit cases:

| Original | Cleanup | Required result | Test |
| --- | --- | --- | --- |
| SystemExit(17) | Wait timeout; stderr raises | Same original SystemExit(17) | `test_system_exit_survives_reap_timeout_and_failing_stderr` (tests/test_new1_supervisor.py:1182) |
| KeyboardInterrupt | Signal failure; stderr raises | Same original KeyboardInterrupt | `test_keyboard_interrupt_survives_signal_failure_and_failing_stderr` (tests/test_new1_supervisor.py:1192) |
| Heartbeat KeyboardInterrupt | Group and PID signals fail | Same original KeyboardInterrupt | `test_heartbeat_keyboard_interrupt_survives_double_signal_failure` (tests/test_new1_supervisor.py:1202) |
| STOPPED-RESOURCE | Wait raises KeyboardInterrupt | Reap within bound, then propagate interrupt | `test_emergency_wait_keyboard_interrupt_overrides_ordinary_stop_after_reap` (tests/test_new1_supervisor.py:1214) |

Other precedence, reporting, retry-bound and closeout regressions:

- `test_emergency_wait_system_exit_overrides_ordinary_stop_after_reap` (tests/test_new1_supervisor.py:1225)
- `test_original_control_exception_beats_cleanup_control_after_reap` (tests/test_new1_supervisor.py:1234)
- `test_cleanup_interrupt_survives_retry_timeout_with_unreaped_pid` (tests/test_new1_supervisor.py:1244)
- `test_cleanup_interrupts_share_one_five_second_reap_bound` (tests/test_new1_supervisor.py:1256)
- `test_system_exit_survives_halt_receipt_failure_and_failing_stderr` (tests/test_new1_supervisor.py:1268)
- `test_postcommit_control_exception_survives_failing_stderr` (tests/test_new1_supervisor.py:1279)
- `test_recorded_outcome_survives_failing_postcommit_stderr` (tests/test_new1_supervisor.py:1293)
- `test_ordinary_error_beats_reap_timeout_with_failing_stderr_and_pid_receipt` (tests/test_new1_supervisor.py:1308)
- `test_original_control_survives_socket_close_failure_and_failing_stderr` (tests/test_new1_supervisor.py:1333)

The emergency wait shares one deadline computed at tools/new1_supervisor.py:379. First wait uses 5 seconds; an interrupted wait retries with only the remaining part of that same five seconds, independent of controller.remaining(). A successful retry marks reaping complete before propagation. Exhaustion/timeout still names the unreaped PID in stderr and the halt diagnostic when the original durability budget permits. Failed stderr retains the diagnostic/reporting error in notes; durable receipt writing still proceeds if allowed. An original ordinary Stop still wins over a secondary timeout.

Post-commit authority still uses the exact committed publication. Ordinary post-commit errors return its recorded outcome; original control exceptions are re-raised after reconciliation even with failing stderr. Halt closeout and final socket closure preserve the governing control exception. No new terminal authority, event name, or verdict source was added.

## Finding 3 — PID ownership

tools/new1_supervisor.py:313 now receives the process object. Group cleanup via killpg remains. The os.kill fallback runs only while process.returncode is None. CPython's installed poll implementation (:1973-1998) performs waitpid and sets returncode, releasing the PID. At tools/new1_supervisor.py:318, only SIGALRM is blocked around the ownership check/single-PID signal so the main-thread watchdog cannot poll between them; the prior mask is restored immediately. This mask is applied after group signalling fails, not during creation.

- `test_group_cleanup_after_poll_never_signals_reaped_pid` (tests/test_new1_supervisor.py:1320)
- `test_pid_fallback_ownership_check_cannot_be_interrupted_by_watchdog_poll` (tests/test_new1_supervisor.py:1342)

Required existing-test correction: `test_reap_when_loop_termination_group_signal_is_denied` (tests/test_new1_supervisor.py:1022) (round-1 :1015). Its poll-exited fake now sets returncode=0 and expects no PID fallback. Group signalling and wait assertions remain. Three mock Popen factory sites were adapted through popen_factory for explicit preallocated initialization; no other existing outcome/assertion was changed. Mechanical method comparison verified the other 75 existing tests after normalizing that fixture wiring.

## Identity, scope and evidence

Worktree/branch: /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a / worktree-c10k-route-a. Frozen supervisor is da9f250e from a310686. Before copies are in before/. RED_final_tests.py exactly matches final tests; GREEN_first_source.py preserves the intermediate 93-test passing source.

| File | Start SHA-256 | Final SHA-256 |
| --- | --- | --- |
| tools/new1_supervisor.py | `da9f250e244b8e29392e13dbba83ceb90e6980fdfee2b43fa66a3feed3c86a9c` | `e61d4802fa6c9d4b6a8ecb1c4f612e0a1285a5e21bf104d5ea8f5e1c7e93d65a` |
| tests/test_new1_supervisor.py | `c3440f6bc8afc5c476257865121249d0f98299a05a4b52a3835d7637074eccd5` | `4e8d70a1695a48a6eb3a04d7eee7b41a3a7923c6a26cd3fe96f538ca46e81c90` |

Writes are limited to those two code files and this fresh receipt directory. MB25's backup results directory was ignored; tools/test_dashboard_mathlab.py was untouched. No commit, push, merge, real NEW-1/model worker, or external process kill was performed. New tests use fake processes/clocks/intercepted kill calls; the ownership race probe delivers a harmless in-memory SIGALRM handler. Existing short subprocess fixtures remain in the authorized suite.

Each log contains one complete invocation, with actual exit status and combined stdout/stderr:

```sh
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B -m unittest -v tests.test_new1_supervisor
```

| Log path | Exit | Tests | Assertion failures |
| --- | --- | --- | --- |
| results/mathlab_staging/new1_supervisor_reap_r2_20261010T210738Z/RED.log | 1 | 93 | 21 |
| results/mathlab_staging/new1_supervisor_reap_r2_20261010T210738Z/GREEN.log | 0 | 93 | 0 |
| results/mathlab_staging/new1_supervisor_reap_r2_20261010T210738Z/RED_final.log | 1 | 94 | 22 |
| results/mathlab_staging/new1_supervisor_reap_r2_20261010T210738Z/GREEN_final.log | 0 | 94 | 0 |

Final RED: 94 tests, 22 assertion failures across 19 methods (all 18 new methods plus the deliberately corrected existing ownership expectation), zero errors; 75 other existing tests pass. Subtests account for the extra assertions. Final GREEN: 94/94, comprising 76 existing names plus 18 added methods. Initial RED/GREEN had 93 tests; a subsequent ownership-race regression received a fresh RED on da9f250e and final GREEN. evidence.json binds source/log hashes, counts, exit codes, exact command and RED membership. git diff --check passed.

Finding 6 accuracy: round-1 halt receipt and halt emit tests were ordering/bound regressions, not independent original wait skips. Their wait already occurred with timeout 2700.0 rather than 5. This receipt does not equate test count with distinct skip paths.

Preserved: exit-code/outcome vocabulary, terminal-commit authority, event names, 2,700 s total, 300 s cell wait, resource caps, REAP_TIMEOUT_S=5, and original halt-durability budget. Only reaping has the independent fixed bound; halt persistence still uses original controller.remaining(). At exhausted budget, PID reporting and incomplete-closeout reporting remain explicit without borrowing persistence time.

## Final diff against da9f250e / c3440f6b

```diff
--- results/mathlab_staging/new1_supervisor_reap_r2_20261010T210738Z/before/new1_supervisor.py	2026-10-10 15:09:35
+++ tools/new1_supervisor.py	2026-10-10 15:17:27
@@ -265,17 +265,67 @@
         return self.wait_cell(message['phase'], message['cell'], pid)
 
 
-def kill_worker(pid):
-    try: os.killpg(pid, signal.SIGKILL)
+def preferred_exception(original,secondary):
+    if original is None or (not isinstance(original,(KeyboardInterrupt,SystemExit))
+            and isinstance(secondary,(KeyboardInterrupt,SystemExit))): return secondary
+    return original
+
+
+def report_error(error,message):
+    try: print(message,file=sys.stderr)
+    except BaseException as reporting_error:
+        error.add_note(f'stderr reporting failed: {reporting_error}; {message}')
+
+
+@contextlib.contextmanager
+def constructor_ownership(process):
+    """Defer raising signal handlers only until CPython has stored the child PID."""
+    handlers={s:signal.getsignal(s) for s in signal.valid_signals()
+        if callable(signal.getsignal(s))}
+    pending={}
+    def deliver(entries,original=None):
+        chosen=original
+        for signum,frame in entries:
+            try: handlers[signum](signum,frame)
+            except BaseException as error:
+                winner=preferred_exception(chosen,error)
+                if winner is chosen: chosen.add_note(f'deferred signal raised: {error}')
+                chosen=winner
+        if chosen is not original: raise chosen
+    def guarded(signum,frame):
+        if getattr(process,'pid',None) is None:
+            pending[signum]=frame
+            # Retry pending delivery promptly; the original absolute budget stays.
+            signal.setitimer(signal.ITIMER_REAL,.001)
+            return
+        entries=list(pending.items()); pending.clear()
+        deliver(entries+[(signum,frame)])
+    try:
+        for signum in handlers: signal.signal(signum,guarded)
+        yield
+    finally:
+        original=sys.exc_info()[1]
+        for signum,handler in handlers.items(): signal.signal(signum,handler)
+        entries=list(pending.items()); pending.clear()
+        deliver(entries,original)
+
+
+def kill_worker(process):
+    try: os.killpg(process.pid, signal.SIGKILL)
     except (ProcessLookupError, PermissionError):
-        # A group signal can be refused while the owned PID remains signalable.
-        try: os.kill(pid, signal.SIGKILL)
-        except ProcessLookupError: pass
+        # poll()/wait() releases PID ownership; group cleanup still applies.
+        # The main-thread watchdog must not poll between this check and signal.
+        blocked=signal.pthread_sigmask(signal.SIG_BLOCK,{signal.SIGALRM})
+        try:
+            if process.returncode is None:
+                try: os.kill(process.pid, signal.SIGKILL)
+                except ProcessLookupError: pass
+        finally: signal.pthread_sigmask(signal.SIG_SETMASK,blocked)
 
 
 def terminate(process):
     """Stop the whole isolated group immediately, then reap the direct worker."""
-    try: kill_worker(process.pid)
+    try: kill_worker(process)
     finally: process.wait(timeout=REAP_TIMEOUT_S)
 
 
@@ -316,37 +366,56 @@
         nonlocal kill_sent, worker_reaped, reap_error
         try: yield
         finally:
-            if process is not None and not worker_reaped:
+            if process is not None and getattr(process,'pid',None) is not None and not worker_reaped:
                 original_error = sys.exc_info()[1]
                 signal_error = None
                 wait_error = None
                 try:
                     if not kill_sent:
-                        kill_worker(process.pid); kill_sent=True
+                        kill_worker(process); kill_sent=True
                 except BaseException as error:
                     signal_error = error
-                try:
-                    process.wait(timeout=REAP_TIMEOUT_S)
-                    worker_reaped=True
-                except BaseException as error:
-                    wait_error = error
+                cleanup_control = None
+                reap_deadline=time.monotonic()+REAP_TIMEOUT_S
+                timeout=REAP_TIMEOUT_S
+                while True:
+                    try:
+                        process.wait(timeout=timeout)
+                        worker_reaped=True
+                        break
+                    except (KeyboardInterrupt,SystemExit) as error:
+                        cleanup_control=preferred_exception(cleanup_control,error)
+                        timeout=reap_deadline-time.monotonic()
+                        if timeout<=0:
+                            wait_error=subprocess.TimeoutExpired(f'worker PID {process.pid}',REAP_TIMEOUT_S)
+                            break
+                    except BaseException as error:
+                        wait_error=error
+                        break
+                if wait_error is not None:
+                    error=wait_error
                     reap_error = f'unreaped worker PID {process.pid}: {error}'
+                chosen=preferred_exception(original_error,signal_error)
+                chosen=preferred_exception(chosen,cleanup_control)
+                chosen=preferred_exception(chosen,wait_error)
                 if signal_error is not None:
-                    print(f'Worker PID {process.pid} signal failed: {signal_error}',file=sys.stderr)
+                    report_error(chosen,f'Worker PID {process.pid} signal failed: {signal_error}')
                 if wait_error is not None:
-                    print(reap_error,file=sys.stderr)
-                    if original_error is None: raise wait_error
-                if signal_error is not None and original_error is None: raise signal_error
+                    report_error(chosen,reap_error)
+                if chosen is not None and chosen is not original_error: raise chosen
     def terminal_ready(publication):
         nonlocal terminal
         controller.remaining()
         terminal = publication
     def heartbeat():
         nonlocal kill_sent
-        try: controller.observe(process.pid if process is not None and process.poll() is None else None)
-        except BaseException:
-            if process is not None and not kill_sent:
-                kill_worker(process.pid); kill_sent=True
+        try: controller.observe(process.pid if process is not None and getattr(process,'pid',None) is not None
+            and process.poll() is None else None)
+        except BaseException as error:
+            if process is not None and getattr(process,'pid',None) is not None and not kill_sent:
+                try: kill_worker(process); kill_sent=True
+                except BaseException as signal_error:
+                    error.add_note(f'Worker PID {process.pid} heartbeat signal failed: {signal_error}')
             raise
     try:
         # Exit the run alarm before the lifetime's separately bounded reap.
@@ -368,8 +437,11 @@
                        LLMDB_DEVICE='cpu', CUDA_VISIBLE_DEVICES='', OMP_NUM_THREADS='8', MKL_NUM_THREADS='8',
                        PYTHONDONTWRITEBYTECODE='1')
             with (run_dir/'worker_stdout.log').open('xb') as stdout, (run_dir/'worker_stderr.log').open('xb') as stderr:
-                process = subprocess.Popen(command, cwd=ROOT, env=env, start_new_session=True,
-                    pass_fds=(child.fileno(),), stdin=subprocess.DEVNULL, stdout=stdout, stderr=stderr)
+                # Capture the handle before __init__ can create a child and raise.
+                process = subprocess.Popen.__new__(subprocess.Popen)
+                with constructor_ownership(process):
+                    subprocess.Popen.__init__(process,command, cwd=ROOT, env=env, start_new_session=True,
+                        pass_fds=(child.fileno(),), stdin=subprocess.DEVNULL, stdout=stdout, stderr=stderr)
                 child.close(); parent.setblocking(False)
                 with selectors.DefaultSelector() as selector:
                     selector.register(parent,selectors.EVENT_READ)
@@ -438,11 +510,13 @@
         # additional persistence budget is needed to reconcile that boundary.
         if terminal is not None:
             try: recorded = terminal.committed_outcome()
-            except OSError as verification_error:
-                print(f'Terminal commit verification failed: {verification_error}',file=sys.stderr)
+            except BaseException as verification_error:
+                if not isinstance(verification_error,OSError) and not isinstance(error,(KeyboardInterrupt,SystemExit)):
+                    raise
+                report_error(error,f'Terminal commit verification failed: {verification_error}')
             else:
                 if recorded is not None:
-                    print(f'NEW1 postcommit interruption: {error}; recorded outcome {recorded}',file=sys.stderr)
+                    report_error(error,f'NEW1 postcommit interruption: {error}; recorded outcome {recorded}')
                     if isinstance(error,(KeyboardInterrupt,SystemExit)): raise
                     return recorded
         code=getattr(error,'code','INVALID-WORKER')
@@ -455,11 +529,19 @@
                 controller.remaining()
                 emit(run_dir,'halted',reason=code+': '+message,diagnostic_path=diagnostic['path'])
         except BaseException as closeout_error:
-            print(f'{code}: {message}; closeout incomplete: {closeout_error}; no prediction verdict',file=sys.stderr)
+            report_error(error,f'{code}: {message}; closeout incomplete: {closeout_error}; no prediction verdict')
+            if isinstance(closeout_error,(KeyboardInterrupt,SystemExit)) and not isinstance(error,(KeyboardInterrupt,SystemExit)):
+                raise
         if isinstance(error,(KeyboardInterrupt,SystemExit)): raise
         return code
     finally:
-        parent.close(); child.close()
+        original=sys.exc_info()[1]; chosen=original
+        for endpoint in (parent,child):
+            try: endpoint.close()
+            except BaseException as close_error:
+                chosen=preferred_exception(chosen,close_error)
+                report_error(chosen,f'Control socket close failed: {close_error}')
+        if chosen is not original: raise chosen
 
 
 def main():

--- results/mathlab_staging/new1_supervisor_reap_r2_20261010T210738Z/before/test_new1_supervisor.py	2026-10-10 15:09:35
+++ tests/test_new1_supervisor.py	2026-10-10 15:17:06
@@ -694,7 +694,7 @@
         process=mock.Mock(pid=123,returncode=0); process.poll.side_effect=[None,None,None,0]
         selector=mock.MagicMock(); selector.__enter__.return_value.select.return_value=[(None,None)]
         with mock.patch.object(self.S.socket,'socketpair',return_value=(parent,child)),\
-             mock.patch.object(self.S.subprocess,'Popen',return_value=process),\
+             mock.patch.object(self.S.subprocess,'Popen',self.popen_factory(process)),\
              mock.patch.object(self.S.selectors,'DefaultSelector',return_value=selector),\
              mock.patch.object(self.S.os,'killpg'):
             return self.S.supervise(['fixture-only'],self.run,admission=lambda:{'allowed':True,'reasons':[]},
@@ -903,7 +903,7 @@
         process.poll.side_effect=[None,None,None,0]
         selector=mock.MagicMock(); selector.__enter__.return_value.select.return_value=[(None,None)]
         with mock.patch.object(self.S.socket,'socketpair',return_value=(parent,child)),\
-             mock.patch.object(self.S.subprocess,'Popen',return_value=process),\
+             mock.patch.object(self.S.subprocess,'Popen',self.popen_factory(process)),\
              mock.patch.object(self.S.selectors,'DefaultSelector',return_value=selector),\
              mock.patch.object(self.S.os,'killpg') as kill:
             outcome=self.S.supervise(['fixture-only'],self.run,admission=lambda:{'allowed':True,'reasons':[]},
@@ -912,6 +912,12 @@
         kill.assert_called_once_with(123,signal.SIGKILL)
         process.wait.assert_called_once()
 
+    def popen_factory(self,process):
+        class FakePopen:
+            def __new__(cls,*args,**kwargs): return process
+            def __init__(handle,*args,**kwargs): pass
+        return FakePopen
+
     @contextlib.contextmanager
     def reap_fixture(self):
         parent=mock.Mock(); child=mock.Mock(); child.fileno.return_value=99
@@ -926,14 +932,15 @@
             if 'heartbeat' in kwargs: watchdog['callback']=kwargs['heartbeat']
             with hard_deadline(seconds,**kwargs): yield
         with mock.patch.object(self.S.socket,'socketpair',return_value=(parent,child)),\
-             mock.patch.object(self.S.subprocess,'Popen',return_value=process),\
+             mock.patch.object(self.S.subprocess,'Popen',self.popen_factory(process)),\
              mock.patch.object(self.S.selectors,'DefaultSelector',return_value=selector),\
              mock.patch.object(self.S,'Controller',return_value=controller),\
              mock.patch.object(self.S,'hard_deadline',side_effect=deadline),\
              mock.patch.object(self.S.os,'killpg') as kill_group,\
              mock.patch.object(self.S.os,'kill') as kill_pid:
             yield SimpleNamespace(process=process,selector=selected,controller=controller,
-                kill_group=kill_group,kill_pid=kill_pid,heartbeat=lambda:watchdog['callback']())
+                kill_group=kill_group,kill_pid=kill_pid,parent=parent,child=child,
+                heartbeat=lambda:watchdog['callback']())
 
     def expire_run(self,error):
         self.clock.now=2700
@@ -1014,12 +1021,12 @@
 
     def test_reap_when_loop_termination_group_signal_is_denied(self):
         with self.reap_fixture() as f:
-            f.process.poll.return_value=0
+            f.process.poll.return_value=0; f.process.returncode=0
             f.kill_group.side_effect=PermissionError('fixture group signal denied')
             f.selector.select.side_effect=self.S.Stop('STOPPED-RESOURCE','fixture stop after leader exit')
             self.supervise_reap_fixture()
         f.process.wait.assert_called_once_with(timeout=5)
-        f.kill_pid.assert_called_with(123,signal.SIGKILL)
+        f.kill_pid.assert_not_called()
 
     def test_reap_when_termination_wait_timeout_exhausts_budget(self):
         with self.reap_fixture() as f:
@@ -1118,6 +1125,241 @@
             with self.assertRaises(SystemExit) as raised: self.supervise_reap_fixture()
         f.process.wait.assert_called_once_with(timeout=5)
         self.assertEqual(raised.exception.code,17)
+
+    def broken_stderr(self):
+        class BrokenStderr(io.StringIO):
+            def write(stream,value): raise OSError('fixture stderr failed')
+        return BrokenStderr()
+
+    def assert_control_exit(self,expected,invoke=None):
+        caught=None; outcome=None
+        try: outcome=(invoke or self.supervise_reap_fixture)()
+        except BaseException as error: caught=error
+        self.assertIs(caught,expected,f'returned {outcome!r}; raised {caught!r}')
+
+    def constructor_factory(self,f,error=None,before_pid=False):
+        created=[]
+        class FakePopen:
+            def __init__(handle,*args,**kwargs):
+                handle.returncode=None; handle.wait=f.process.wait; handle.poll=f.process.poll
+                created.append(123)
+                if before_pid:
+                    self.clock.now=2700
+                    signal.getsignal(signal.SIGALRM)(signal.SIGALRM,None)
+                handle.pid=123
+                if error is not None: raise error
+        return FakePopen,created
+
+    def test_constructor_interruption_reaps_created_child(self):
+        with self.reap_fixture() as f:
+            factory,created=self.constructor_factory(f,self.S.Stop('STOPPED-RESOURCE','constructor after fork'))
+            with mock.patch.object(self.S.subprocess,'Popen',factory):
+                outcome=self.supervise_reap_fixture()
+        self.assertEqual(created,[123])
+        f.process.wait.assert_called_once_with(timeout=5)
+        f.kill_group.assert_called_with(123,signal.SIGKILL)
+        self.assertEqual(outcome,'STOPPED-RESOURCE')
+
+    def test_constructor_system_exit_reaps_child_and_preserves_exit_value(self):
+        expected=SystemExit(17)
+        with self.reap_fixture() as f:
+            factory,created=self.constructor_factory(f,expected)
+            with mock.patch.object(self.S.subprocess,'Popen',factory):
+                self.assert_control_exit(expected)
+        self.assertEqual(created,[123])
+        f.process.wait.assert_called_once_with(timeout=5)
+        self.assertEqual(expected.code,17)
+
+    def test_constructor_alarm_before_pid_assignment_is_deferred_until_owned(self):
+        with self.reap_fixture() as f:
+            factory,created=self.constructor_factory(f,before_pid=True)
+            with mock.patch.object(self.S.subprocess,'Popen',factory):
+                outcome=self.supervise_reap_fixture()
+        self.assertEqual(created,[123])
+        f.process.wait.assert_called_once_with(timeout=5)
+        self.assertEqual(outcome,'STOPPED-DEADLINE')
+
+    def test_system_exit_survives_reap_timeout_and_failing_stderr(self):
+        expected=SystemExit(17)
+        with self.reap_fixture() as f,contextlib.redirect_stderr(self.broken_stderr()):
+            f.selector.select.side_effect=expected
+            f.process.wait.side_effect=subprocess.TimeoutExpired('fixture-only',5)
+            self.assert_control_exit(expected)
+        f.process.wait.assert_called_once_with(timeout=5)
+        self.assertEqual(expected.code,17)
+        self.assertTrue(any('stderr reporting failed' in n for n in expected.__notes__))
+
+    def test_keyboard_interrupt_survives_signal_failure_and_failing_stderr(self):
+        expected=KeyboardInterrupt()
+        with self.reap_fixture() as f,contextlib.redirect_stderr(self.broken_stderr()):
+            f.selector.select.side_effect=expected
+            f.kill_group.side_effect=PermissionError('fixture group denied')
+            f.kill_pid.side_effect=PermissionError('fixture PID denied')
+            self.assert_control_exit(expected)
+        f.process.wait.assert_called_once_with(timeout=5)
+        self.assertTrue(any('stderr reporting failed' in n for n in expected.__notes__))
+
+    def test_heartbeat_keyboard_interrupt_survives_double_signal_failure(self):
+        expected=KeyboardInterrupt()
+        with self.reap_fixture() as f:
+            def heartbeat(timeout):
+                with mock.patch.object(f.controller,'observe',side_effect=expected): f.heartbeat()
+            f.selector.select.side_effect=heartbeat
+            f.kill_group.side_effect=PermissionError('fixture group denied')
+            f.kill_pid.side_effect=PermissionError('fixture PID denied')
+            self.assert_control_exit(expected)
+        f.process.wait.assert_called_once_with(timeout=5)
+        f.kill_pid.assert_called_with(123,signal.SIGKILL)
+
+    def test_emergency_wait_keyboard_interrupt_overrides_ordinary_stop_after_reap(self):
+        expected=KeyboardInterrupt()
+        with self.reap_fixture() as f:
+            f.selector.select.side_effect=self.S.Stop('STOPPED-RESOURCE','fixture stop')
+            f.process.wait.side_effect=[expected,0]
+            self.assert_control_exit(expected)
+        self.assertEqual(f.process.wait.call_count,2)
+        self.assertEqual(f.process.wait.call_args_list[0],mock.call(timeout=5))
+        self.assertGreater(f.process.wait.call_args.kwargs['timeout'],0)
+        self.assertLessEqual(f.process.wait.call_args.kwargs['timeout'],5)
+
+    def test_emergency_wait_system_exit_overrides_ordinary_stop_after_reap(self):
+        expected=SystemExit(23)
+        with self.reap_fixture() as f:
+            f.selector.select.side_effect=self.S.Stop('STOPPED-RESOURCE','fixture stop')
+            f.process.wait.side_effect=[expected,0]
+            self.assert_control_exit(expected)
+        self.assertEqual(f.process.wait.call_count,2)
+        self.assertEqual(expected.code,23)
+
+    def test_original_control_exception_beats_cleanup_control_after_reap(self):
+        for original,secondary in ((KeyboardInterrupt(),SystemExit(19)),(SystemExit(17),KeyboardInterrupt())):
+            with self.subTest(original=type(original).__name__):
+                self.run=self.root/type(original).__name__; self.run.mkdir()
+                with self.reap_fixture() as f:
+                    f.selector.select.side_effect=original
+                    f.process.wait.side_effect=[secondary,0]
+                    self.assert_control_exit(original)
+                self.assertEqual(f.process.wait.call_count,2)
 
+    def test_cleanup_interrupt_survives_retry_timeout_with_unreaped_pid(self):
+        expected=KeyboardInterrupt(); stderr=io.StringIO()
+        with self.reap_fixture() as f,contextlib.redirect_stderr(stderr):
+            f.selector.select.side_effect=self.S.Stop('STOPPED-RESOURCE','fixture stop')
+            f.process.wait.side_effect=[expected,subprocess.TimeoutExpired('fixture-only',5)]
+            self.assert_control_exit(expected)
+        self.assertEqual(f.process.wait.call_count,2)
+        self.assertIn('unreaped worker PID 123',stderr.getvalue())
+        events,_=self.state()
+        halted=next(e for e in events if e['type']=='halted')
+        self.assertIn('unreaped worker PID 123',json.loads(Path(halted['diagnostic_path']).read_text())['message'])
 
+    def test_cleanup_interrupts_share_one_five_second_reap_bound(self):
+        expected=KeyboardInterrupt()
+        with self.reap_fixture() as f,mock.patch.object(self.S.time,'monotonic',self.clock):
+            def wait(*,timeout):
+                self.clock.now+=5
+                raise expected
+            f.selector.select.side_effect=self.S.Stop('STOPPED-RESOURCE','fixture stop')
+            f.process.wait.side_effect=wait
+            self.assert_control_exit(expected)
+        f.process.wait.assert_called_once_with(timeout=5)
+        self.assertEqual(self.clock.now,5)
+
+    def test_system_exit_survives_halt_receipt_failure_and_failing_stderr(self):
+        expected=SystemExit(17); receipt=self.S.receipt
+        with self.reap_fixture() as f,contextlib.redirect_stderr(self.broken_stderr()):
+            def fail_receipt(run_dir,kind,data):
+                if kind=='halt': raise OSError('fixture halt receipt failed')
+                return receipt(run_dir,kind,data)
+            f.selector.select.side_effect=expected
+            with mock.patch.object(self.S,'receipt',side_effect=fail_receipt): self.assert_control_exit(expected)
+        f.process.wait.assert_called_once_with(timeout=5)
+        self.assertEqual(expected.code,17)
+
+    def test_postcommit_control_exception_survives_failing_stderr(self):
+        for expected in (KeyboardInterrupt(),SystemExit(17)):
+            with self.subTest(original=type(expected).__name__):
+                self.run=self.root/type(expected).__name__; self.run.mkdir()
+                emit=self.S.emit
+                def fail_emit(run_dir,kind,**data):
+                    if kind=='run_finished':
+                        publication=mock.Mock(); publication.committed_outcome.return_value='PASS'
+                        data['before_publish'](publication)
+                        raise expected
+                    return emit(run_dir,kind,**data)
+                with mock.patch.object(self.S,'emit',side_effect=fail_emit),contextlib.redirect_stderr(self.broken_stderr()):
+                    self.assert_control_exit(expected,self.complete_fixture)
+
+    def test_recorded_outcome_survives_failing_postcommit_stderr(self):
+        emit=self.S.emit; original=OSError('fixture postcommit error')
+        def fail_emit(run_dir,kind,**data):
+            if kind=='run_finished':
+                publication=mock.Mock(); publication.committed_outcome.return_value='PASS'
+                data['before_publish'](publication)
+                raise original
+            return emit(run_dir,kind,**data)
+        caught=None; outcome=None
+        with mock.patch.object(self.S,'emit',side_effect=fail_emit),contextlib.redirect_stderr(self.broken_stderr()):
+            try: outcome=self.complete_fixture()
+            except BaseException as error: caught=error
+        self.assertIsNone(caught)
+        self.assertEqual(outcome,'PASS')
+
+    def test_ordinary_error_beats_reap_timeout_with_failing_stderr_and_pid_receipt(self):
+        original=self.S.Stop('STOPPED-RESOURCE','fixture stop')
+        with self.reap_fixture() as f,contextlib.redirect_stderr(self.broken_stderr()):
+            f.selector.select.side_effect=original
+            f.process.wait.side_effect=subprocess.TimeoutExpired('fixture-only',5)
+            outcome=self.supervise_reap_fixture()
+        self.assertEqual(outcome,'STOPPED-RESOURCE')
+        self.assertTrue(any('unreaped worker PID 123' in n for n in original.__notes__))
+        events,_=self.state()
+        halted=next(e for e in events if e['type']=='halted')
+        self.assertIn('unreaped worker PID 123',json.loads(Path(halted['diagnostic_path']).read_text())['message'])
+
+    def test_group_cleanup_after_poll_never_signals_reaped_pid(self):
+        for failure in (PermissionError,ProcessLookupError):
+            with self.subTest(failure=failure.__name__):
+                self.run=self.root/failure.__name__; self.run.mkdir()
+                with self.reap_fixture() as f:
+                    f.process.poll.return_value=0; f.process.returncode=0
+                    f.kill_group.side_effect=failure('fixture group signal failure')
+                    f.selector.select.side_effect=self.S.Stop('STOPPED-RESOURCE','fixture stop')
+                    self.supervise_reap_fixture()
+                f.kill_group.assert_called_with(123,signal.SIGKILL)
+                f.kill_pid.assert_not_called()
+                f.process.wait.assert_called_once_with(timeout=5)
+
+    def test_original_control_survives_socket_close_failure_and_failing_stderr(self):
+        expected=SystemExit(17)
+        with self.reap_fixture() as f,contextlib.redirect_stderr(self.broken_stderr()):
+            f.selector.select.side_effect=expected
+            f.parent.close.side_effect=OSError('fixture socket close failed')
+            self.assert_control_exit(expected)
+        f.process.wait.assert_called_once_with(timeout=5)
+        f.child.close.assert_called()
+
+    def test_pid_fallback_ownership_check_cannot_be_interrupted_by_watchdog_poll(self):
+        reaped=[]; signalled=[]
+        class Process:
+            pid=123
+            @property
+            def returncode(handle):
+                signal.raise_signal(signal.SIGALRM)
+                return None
+        previous=signal.getsignal(signal.SIGALRM)
+        signal.signal(signal.SIGALRM,lambda signum,frame:reaped.append(123))
+        def kill(pid,signum):
+            self.assertEqual(pid,123)
+            self.assertEqual(reaped,[],'watchdog reaped the PID before fallback signalling')
+            signalled.append(pid)
+        try:
+            with mock.patch.object(self.S.os,'killpg',side_effect=ProcessLookupError('fixture missing group')),\
+                 mock.patch.object(self.S.os,'kill',side_effect=kill):
+                self.S.kill_worker(Process())
+        finally: signal.signal(signal.SIGALRM,previous)
+        self.assertEqual(signalled,[123])
+        self.assertEqual(reaped,[123])
+
+
 if __name__=='__main__': unittest.main()
```

## Context / reviewer handoff

Done: 18 failing-first methods, constructor ownership/signal deferral, explicit precedence, bounded cleanup-interrupt retry, reporting notes, ownership-gated PID fallback/watchdog protection, corrected existing expectation, final 94/94 GREEN, hashes, logs, evidence.json and final diff. Half-applied/in-flight work: none. Failing final tests: none. Exact paths, SHA-256 values, commands and deliberate RED failures are above and in evidence.json.

UNVERIFIED: real full-worker host enforcement and binding Astra re-review. No launch readiness GO is claimed. Next step: MAESTRO25 verifies identities and fixture evidence on the host and submits to GPT-6-Astra; MAESTRO alone commits. No remaining implementation issue in this scope was identified by the final audit.

Binding context directive: watch "Context N% left". Start a new piece of work only at 60% left or more. At 40% left or less, stop starting work and append a handoff here with done/half-applied work, exact paths and SHA-256, failing tests and exact commands, and next step; reply exactly "CONTEXT HANDOFF WRITTEN". If "Context compacted" appears, do this immediately without another edit/test. Preserve this directive in every team session and successor handoff; stop before full-window compaction and pass a precise handoff.
