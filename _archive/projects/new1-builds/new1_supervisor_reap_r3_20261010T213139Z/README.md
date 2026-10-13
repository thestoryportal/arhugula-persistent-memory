# MB29 — NEW1 supervisor reap R3

BUILD DONE: 97/97 tests GREEN; all 94 existing test methods and helpers remain byte-identical. Fixture evidence only. MAESTRO25 host verification and binding GPT-6-Astra review remain OPEN.

The two supplied SHA-256 pins matched before the first edit; worktree and branch were verified. Read Astra r11 in full and the required R2 precedence table, source ranges, installed CPython poll, and fake patterns.

## R11 blocker 1 — ownership across interrupted reaping

Choice: defer SIGINT and SIGALRM around the supervisor’s own worker poll/wait operations. `tools/new1_supervisor.py:314` masks both signals, restores the exact prior mask on every exit, and applies the existing exception selector if pending delivery raises while restoring it. `tools/new1_supervisor.py:326` contains the sole raw poll; its callers are heartbeat `tools/new1_supervisor.py:438`, loop top `tools/new1_supervisor.py:479`, and loop EOF `tools/new1_supervisor.py:516`. The raw waits are guarded at `tools/new1_supervisor.py:347` and `tools/new1_supervisor.py:407`.

Why: installed CPython subprocess.py:1990 reaps with waitpid before :1992 stores returncode. Keeping that interval uninterruptible makes returncode a current ownership fact before cleanup can use PID fallback. Group cleanup remains unconditional. `tools/new1_supervisor.py:330` retains the protected ownership-check/PID-signal interval using the same guard.

Deferral bound: every masked body is a nonblocking worker poll, a nonblocking ownership check/PID signal, or wait(timeout <= REAP_TIMEOUT_S = 5). No selector, resource probe, persistence, admission, constructor IO, complete retry loop, or arbitrary worker execution is masked. A wait keeps its existing finite timeout; emergency retries share the existing absolute five-second deadline. The successful reap flag is set inside the guard before pending delivery, and `tools/new1_supervisor.py:412` prevents a second wait after that success. The original 2,700-second deadline and 300-second cell deadline continue to be checked after delivery; no deadline is reset or extended.

Regression: `test_interrupted_poll_never_signals_pid_released_before_returncode` at `tests/test_new1_supervisor.py:1342`. It uses the installed Popen._internal_poll with fake successful waitpid and a trace-triggered real SIGINT on the first line after waitpid returns. At injection, returncode is still None. It covers all three poll call sites, denies group signalling, intercepts all PID signals, retains the same original KeyboardInterrupt, and asserts one wait(timeout=5) and no PID fallback. It never sets returncode before injecting the interrupt.

Causal RED on the pinned e61d4802 source, all three subcases (`RED_causal.log:144`, also RED_causal.log:152 and :160):

```text
AssertionError: [call(123, <Signals.SIGKILL: 9>)] != [] : released PID was signalled after successful waitpid and pre-returncode SIGINT
```

## R11 blocker 2 — new heartbeat cleanup control exception

At `tools/new1_supervisor.py:443`, heartbeat cleanup now selects the governing exception before noting an error. A new KeyboardInterrupt/SystemExit overrides an ordinary Stop and propagates into lifetime cleanup; an original control exception remains the same object and exit value. It therefore survives the bounded reap rather than becoming a note on STOPPED-RESOURCE.

Regression: `test_heartbeat_cleanup_control_overrides_ordinary_stop_after_one_reap` at `tests/test_new1_supervisor.py:1389`. After worker creation, observe raises Stop(STOPPED-RESOURCE); group signalling fails; PID signalling raises the specified KeyboardInterrupt or SystemExit(23); lifetime cleanup succeeds. Both cases assert exactly one wait(timeout=5), then propagation of that same control object; SystemExit retains code 23.

Causal RED (`RED_causal.log:128` and `RED_causal.log:136`):

```text
AssertionError: None is not KeyboardInterrupt() : heartbeat cleanup control was swallowed; returned 'STOPPED-RESOURCE'; raised None
AssertionError: None is not SystemExit(23) : heartbeat cleanup control was swallowed; returned 'STOPPED-RESOURCE'; raised None
```

The cleanup-boundary audit also found that terminate’s bare finally wait could replace its first signal exception. `tools/new1_supervisor.py:341` now attempts the same bounded wait and uses the selector, retaining a secondary wait error as a note when it loses. `test_terminate_preserves_signal_exception_over_ordinary_reap_error` at `tests/test_new1_supervisor.py:1409` covers original KeyboardInterrupt, SystemExit(17), and ordinary PermissionError over an ordinary wait error; one bounded wait occurs in each case. Its causal RED is `RED_causal.log:168`:

```text
AssertionError: OSError('fixture wait failed') is not KeyboardInterrupt() : termination reap replaced the original signal exception
```

## Exception precedence and cleanup boundaries

| Priority | Result |
| --- | --- |
| Original control | Original KeyboardInterrupt/SystemExit wins unchanged: same object and exit value. |
| Cleanup control | Without an original control exception, the first cleanup control exception propagates after bounded reaping. |
| Original ordinary | Otherwise, the original ordinary error beats secondary signalling/reap errors, including timeout. |
| No original | The first cleanup error governs. |
| Printing | Failure becomes an exception note and never chooses the governing exception. |

The R2 precedence table is unchanged; R3 makes the heartbeat and terminate boundaries follow it. Audit of each boundary (static inspection plus applicable existing/new fixtures in GREEN):

| Boundary | Final source line | Check |
| --- | --- | --- |
| Constructor deferred delivery | `tools/new1_supervisor.py:281` | Unchanged selector; original controls retained. Existing constructor fixtures. |
| Signal-mask restoration | `tools/new1_supervisor.py:314` | Selector applies before a restoration error can replace the in-flight error. |
| Single-PID fallback | `tools/new1_supervisor.py:330` | Ownership check and signal share the guard; completed reaps prohibit PID fallback. |
| Termination signal then wait | `tools/new1_supervisor.py:341` | First signal error and wait error use the selector; always attempts the bounded wait. New causal termination regression. |
| Heartbeat signal cleanup | `tools/new1_supervisor.py:435` | New cleanup control is raised; lifetime reaping follows. Original controls still win. New and existing heartbeat regressions. |
| Lifetime signal and reap | `tools/new1_supervisor.py:388` | Original/control/signalling/wait precedence preserved; one five-second retry deadline. Successful reap flag is stored before deferred delivery. Existing lifetime regressions. |
| Terminal commit verification | `tools/new1_supervisor.py:540` | Unchanged accepted terminal authority and control precedence; postcommit fixtures. |
| Halt closeout | `tools/new1_supervisor.py:558` | Unchanged accepted control precedence and original remaining-budget rule; halt failure fixtures. |
| Endpoint closing | `tools/new1_supervisor.py:568` | Unchanged selector; close failure fixture. |
| Stderr reporting | `tools/new1_supervisor.py:274` | Unchanged reporting-note rule, including failed stderr fixtures. |

## R11 finding 6 — round-2 RED qualification

The unchanged round-2 `test_pid_fallback_ownership_check_cannot_be_interrupted_by_watchdog_poll` is now at `tests/test_new1_supervisor.py:1423`. It passes on e61d4802 (RED_causal.log:62) because that source already guards the ownership-check/signal interval. Its old round-2 RED was a signature failure (object != 123 against the old numeric-PID helper), not causal evidence of interrupted reaping. It cannot be made causally RED on e61d4802 for the same already-fixed property without changing its target. R3 preserves it byte-for-byte and adds the separate installed-poll regression above.

## Source identity

| File | Start SHA-256 | Final SHA-256 |
| --- | --- | --- |
| `tools/new1_supervisor.py` | `e61d4802fa6c9d4b6a8ecb1c4f612e0a1285a5e21bf104d5ea8f5e1c7e93d65a` | `3bb767f01257d4fd8d38fb21e132f5c89bfd3fa31959805dccf2555549ccf32f` |
| `tests/test_new1_supervisor.py` | `4e8d70a1695a48a6eb3a04d7eee7b41a3a7923c6a26cd3fe96f538ca46e81c90` | `01b1fd268dbd8ceab42f13d4244f1e5e92205cdcb88e24d2c4c0fe1f5666d927` |

The before/ copies match the start pins. RED_causal_tests.py equals GREEN_tests.py and the final test file. GREEN_supervisor.py equals the final source. Full artifact hashes and timestamps are in evidence.json.

## Saved execution evidence

Each log contains exactly one invocation of:

```sh
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B -m unittest -v tests.test_new1_supervisor
```

| Log | Source | Count | Result | Exit |
| --- | --- | --- | --- | --- |
| RED_causal.log | e61d4802 | 97 | 8 causal subtest failures across 3 new methods; 0 errors; all 94 existing methods pass | 1 |
| GREEN.log | Final source | 97 | 97 OK; 0 failures/errors | 0 |

RED_causal.log:187–189 records the RED summary; GREEN.log:116–118 records GREEN. The log paths are `results/mathlab_staging/new1_supervisor_reap_r3_20261010T213139Z/RED_causal.log` and `results/mathlab_staging/new1_supervisor_reap_r3_20261010T213139Z/GREEN.log`.

RED.log and RED_tests.py preserve the earlier rejected fixture setup attempt: 97 tests, eight failures, zero errors, with two heartbeat failures caused by observe being injected during the pre-worker controller.check. That attempt is not blocker-2 RED evidence. Injection was moved into the post-creation selector heartbeat before changing the supervisor; RED_causal.log then records the required swallowed-control assertions.

The audit verifies byte preservation of all 94 existing tests/helpers, the accepted source prefix (caps, Controller and constructor), prediction publication, and the full terminal/closeout/exit-mapping suffix. All worker poll/wait calls were inspected and are guarded. git diff --check passed. R11 findings 3–7, exit codes/outcome strings, terminal-commit authority, event names, 2,700 seconds total, 300 seconds cell wait, resource caps, halt-durability budget, and REAP_TIMEOUT_S = 5 are preserved.

All new tests intercept process construction and group/PID signalling. The full required suite retains its existing short subprocess fixtures. No real long-running NEW1 worker, model/MPS work, PID reuse, commit, push, merge, unrelated deletion, or write to tools/test_dashboard_mathlab.py was performed. Existing integer-SystemExit closeout diagnostics remain in GREEN; the unchanged closeout code still preserves the original control object and exit value. Host/live execution and Astra approval are UNVERIFIED.

Tooling note: the required graft query reported an automatic graph refresh of seven changed inputs. Direct edits are limited to the two authorized source/test files and this fresh receipt; graph results were used for navigation, not acceptance evidence.

## Final diff against the pinned before files

Machine-readable copies: supervisor.diff, tests.diff, and final.diff. The source half is against e61d4802fa6c9d4b6a8ecb1c4f612e0a1285a5e21bf104d5ea8f5e1c7e93d65a; the test half is against the supplied 4e8d70a1 pin.

```diff
diff --git a/results/mathlab_staging/new1_supervisor_reap_r3_20261010T213139Z/before/new1_supervisor.py b/tools/new1_supervisor.py
index 7a488b1..fdaf34b 100644
--- a/results/mathlab_staging/new1_supervisor_reap_r3_20261010T213139Z/before/new1_supervisor.py
+++ b/tools/new1_supervisor.py
@@ -310,23 +310,46 @@ def constructor_ownership(process):
         deliver(entries,original)
 
 
+@contextlib.contextmanager
+def worker_reaping():
+    """Defer SIGINT/SIGALRM across nonblocking poll/kill or a <=5 s wait."""
+    blocked=signal.pthread_sigmask(signal.SIG_BLOCK,{signal.SIGINT,signal.SIGALRM})
+    try: yield
+    finally:
+        original=sys.exc_info()[1]
+        try: signal.pthread_sigmask(signal.SIG_SETMASK,blocked)
+        except BaseException as error:
+            if preferred_exception(original,error) is not original: raise
+            original.add_note(f'Worker signal restoration raised: {error}')
+
+
+def poll_worker(process):
+    with worker_reaping(): return process.poll()
+
+
 def kill_worker(process):
     try: os.killpg(process.pid, signal.SIGKILL)
     except (ProcessLookupError, PermissionError):
         # poll()/wait() releases PID ownership; group cleanup still applies.
         # The main-thread watchdog must not poll between this check and signal.
-        blocked=signal.pthread_sigmask(signal.SIG_BLOCK,{signal.SIGALRM})
-        try:
+        with worker_reaping():
             if process.returncode is None:
                 try: os.kill(process.pid, signal.SIGKILL)
                 except ProcessLookupError: pass
-        finally: signal.pthread_sigmask(signal.SIG_SETMASK,blocked)
 
 
 def terminate(process):
     """Stop the whole isolated group immediately, then reap the direct worker."""
+    original=None
     try: kill_worker(process)
-    finally: process.wait(timeout=REAP_TIMEOUT_S)
+    except BaseException as error: original=error
+    try:
+        with worker_reaping(): process.wait(timeout=REAP_TIMEOUT_S)
+    except BaseException as error:
+        chosen=preferred_exception(original,error)
+        if chosen is not error: chosen.add_note(f'Worker termination reap failed: {error}')
+        raise chosen
+    if original is not None: raise original
 
 
 def publish_predictions(run_dir, path):
@@ -380,11 +403,13 @@ def supervise(command, run_dir, *, admission=None, monitor=sample_resources):
                 timeout=REAP_TIMEOUT_S
                 while True:
                     try:
-                        process.wait(timeout=timeout)
-                        worker_reaped=True
+                        with worker_reaping():
+                            process.wait(timeout=timeout)
+                            worker_reaped=True
                         break
                     except (KeyboardInterrupt,SystemExit) as error:
                         cleanup_control=preferred_exception(cleanup_control,error)
+                        if worker_reaped: break
                         timeout=reap_deadline-time.monotonic()
                         if timeout<=0:
                             wait_error=subprocess.TimeoutExpired(f'worker PID {process.pid}',REAP_TIMEOUT_S)
@@ -410,11 +435,13 @@ def supervise(command, run_dir, *, admission=None, monitor=sample_resources):
     def heartbeat():
         nonlocal kill_sent
         try: controller.observe(process.pid if process is not None and getattr(process,'pid',None) is not None
-            and process.poll() is None else None)
+            and poll_worker(process) is None else None)
         except BaseException as error:
             if process is not None and getattr(process,'pid',None) is not None and not kill_sent:
                 try: kill_worker(process); kill_sent=True
                 except BaseException as signal_error:
+                    chosen=preferred_exception(error,signal_error)
+                    if chosen is not error: raise chosen
                     error.add_note(f'Worker PID {process.pid} heartbeat signal failed: {signal_error}')
             raise
     try:
@@ -449,7 +476,7 @@ def supervise(command, run_dir, *, admission=None, monitor=sample_resources):
                     worker_exited = False
                     while True:
                         remaining = controller.remaining()
-                        if process.poll() is not None and not worker_exited:
+                        if poll_worker(process) is not None and not worker_exited:
                             # Reparented group members may retain IPC after their leader exits.
                             terminate(process); worker_exited=True; kill_sent=True; worker_reaped=True
                         if time.monotonic()-last_sample >= SAMPLE_S and not worker_exited:
@@ -486,7 +513,7 @@ def supervise(command, run_dir, *, admission=None, monitor=sample_resources):
                                         emit(run_dir,'progress',stage='geometry',done=len(list((run_dir/'layers').glob('*.json'))),
                                              total=5,unit='layers')
                                 else: raise Stop('INVALID-PROTOCOL','unexpected IPC message/order')
-                        if process.poll() is not None and eof:
+                        if poll_worker(process) is not None and eof:
                             if buffer or process.returncode or complete is None:
                                 raise Stop('INVALID-WORKER','partial IPC, unsuccessful exit or missing final artifact')
                             if not kill_sent:
diff --git a/results/mathlab_staging/new1_supervisor_reap_r3_20261010T213139Z/before/test_new1_supervisor.py b/tests/test_new1_supervisor.py
index 5e18b97..e799639 100644
--- a/results/mathlab_staging/new1_supervisor_reap_r3_20261010T213139Z/before/test_new1_supervisor.py
+++ b/tests/test_new1_supervisor.py
@@ -1339,6 +1339,87 @@ send({'type':'complete','path':'geometry.json'})
         f.process.wait.assert_called_once_with(timeout=5)
         f.child.close.assert_called()
 
+    def test_interrupted_poll_never_signals_pid_released_before_returncode(self):
+        import sys
+        internal_poll=subprocess.Popen._internal_poll
+        for boundary in ('loop-top','loop-eof','heartbeat'):
+            with self.subTest(boundary=boundary):
+                self.run=self.root/boundary; self.run.mkdir()
+                expected=KeyboardInterrupt(); reaped=[]; interrupted=[]; polls=[]
+                with self.reap_fixture() as f:
+                    f.kill_group.side_effect=PermissionError('fixture group signal denied')
+                    f.process._waitpid_lock.acquire.return_value=True
+                    f.process._handle_exitstatus.side_effect=lambda status:setattr(f.process,'returncode',0)
+                    def waitpid(pid,flags):
+                        self.assertEqual((pid,flags),(123,os.WNOHANG))
+                        reaped.append(pid)
+                        return pid,0
+                    def trace(frame,event,arg):
+                        if (frame.f_code is internal_poll.__code__ and event=='line'
+                                and frame.f_locals.get('pid')==123 and not interrupted):
+                            self.assertEqual(reaped,[123])
+                            interrupted.append(f.process.returncode)
+                            signal.raise_signal(signal.SIGINT)
+                        return trace
+                    def poll():
+                        polls.append(None)
+                        if boundary!='loop-top' and len(polls)==1: return None
+                        return internal_poll(f.process,_waitpid=waitpid)
+                    def wait(*,timeout):
+                        f.process.returncode=0
+                        return 0
+                    f.process.poll.side_effect=poll; f.process.wait.side_effect=wait
+                    if boundary=='heartbeat':
+                        f.selector.select.side_effect=lambda timeout:f.heartbeat()
+                    else:
+                        f.selector.select.return_value=[(None,None)]; f.parent.recv.return_value=b''
+                    previous_handler=signal.getsignal(signal.SIGINT); previous_trace=sys.gettrace()
+                    def interrupt(signum,frame): raise expected
+                    try:
+                        signal.signal(signal.SIGINT,interrupt); sys.settrace(trace)
+                        self.assert_control_exit(expected)
+                    finally:
+                        sys.settrace(previous_trace); signal.signal(signal.SIGINT,previous_handler)
+                self.assertEqual(reaped,[123])
+                self.assertEqual(interrupted,[None],'interrupt must land before returncode is stored')
+                f.process.wait.assert_called_once_with(timeout=5)
+                self.assertEqual(f.kill_pid.call_args_list,[],
+                    'released PID was signalled after successful waitpid and pre-returncode SIGINT')
+
+    def test_heartbeat_cleanup_control_overrides_ordinary_stop_after_one_reap(self):
+        for expected in (KeyboardInterrupt(),SystemExit(23)):
+            with self.subTest(control=type(expected).__name__):
+                self.run=self.root/type(expected).__name__; self.run.mkdir()
+                caught=None; outcome=None
+                with self.reap_fixture() as f:
+                    def heartbeat(timeout):
+                        with mock.patch.object(f.controller,'observe',
+                                side_effect=self.S.Stop('STOPPED-RESOURCE','fixture heartbeat stop')):
+                            f.heartbeat()
+                    f.selector.select.side_effect=heartbeat
+                    f.kill_group.side_effect=PermissionError('fixture group signal denied')
+                    f.kill_pid.side_effect=[expected,None]
+                    try: outcome=self.supervise_reap_fixture()
+                    except BaseException as error: caught=error
+                f.process.wait.assert_called_once_with(timeout=5)
+                self.assertIs(caught,expected,
+                    f'heartbeat cleanup control was swallowed; returned {outcome!r}; raised {caught!r}')
+                if isinstance(expected,SystemExit): self.assertEqual(expected.code,23)
+
+    def test_terminate_preserves_signal_exception_over_ordinary_reap_error(self):
+        for original in (KeyboardInterrupt(),SystemExit(17),PermissionError('fixture PID signal denied')):
+            with self.subTest(original=type(original).__name__):
+                caught=None
+                with self.reap_fixture() as f:
+                    f.kill_group.side_effect=PermissionError('fixture group signal denied')
+                    f.kill_pid.side_effect=original
+                    f.process.wait.side_effect=OSError('fixture wait failed')
+                    try: self.S.terminate(f.process)
+                    except BaseException as error: caught=error
+                f.process.wait.assert_called_once_with(timeout=5)
+                self.assertIs(caught,original,'termination reap replaced the original signal exception')
+                if isinstance(original,SystemExit): self.assertEqual(original.code,17)
+
     def test_pid_fallback_ownership_check_cannot_be_interrupted_by_watchdog_poll(self):
         reaped=[]; signalled=[]
         class Process:
```

## MAESTRO handoff

Done: both r11 blockers fixed with causal RED and complete GREEN; all receipt artifacts saved. Half-applied work: none. In-flight commands: none. Exact paths/hashes: source identity table above and evidence.json. Failing final tests: none. The only RED failures are the saved pre-fix assertions and the separately identified rejected fixture attempt.

Next: MAESTRO25 verifies the final two SHA-256 values and this receipt on the host with the exact test command above, submits the final source/tests plus evidence to binding GPT-6-Astra, and owns any commit. No launch is authorized by this fixture result.

Binding context directive: watch Context N% left for this session and every orchestrated team session. Start a new piece of work only at 60% left or more. At 40% left or less, or immediately upon Context compacted, stop starting work, write a handoff at the end of README with done/half-applied/in-flight work, exact paths and SHA-256 values, failing tests and exact commands, next step and open risks, then reply exactly CONTEXT HANDOFF WRITTEN. Restate this directive in every successor handoff.
