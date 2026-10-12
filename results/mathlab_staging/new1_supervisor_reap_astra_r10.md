**The fix closes the reported deadline-dependent wait skips, but three lifecycle issues still block acceptance.** I verified the source/test hashes against `a310686` and audited the saved RED/GREEN logs. Additional probes executed the unchanged functions with in-memory fakes; no workers were spawned, files changed, or full suite rerun.

1. **Blocking — interruption during process creation can still bypass cleanup entirely.**  
   At [tools/new1_supervisor.py:371](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/new1_supervisor.py:371), `process` is assigned only after `Popen()` returns, while the run alarm is active. If the constructor creates the child and then raises, `process` remains `None`; the guard at :319 skips both signalling and waiting.

   This is a real constructor boundary: the installed CPython implementation creates the child before completing error-pipe handling, and its constructor exception handler closes descriptors without guaranteeing child termination/reaping ([subprocess.py:1883](/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/subprocess.py:1883), :1036).

   A fake of that boundary returned `STOPPED-RESOURCE` with **zero wait calls**. This is pre-existing, but violates requirement 1’s wording, “once … started the worker process.” Cleanup ownership must survive an interrupted constructor; the 15 tests do not cover this boundary.

2. **Blocking — cleanup errors can mask `KeyboardInterrupt`/`SystemExit` and change outcomes.**  
   [worker_lifetime:334–339](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/new1_supervisor.py:334) prints outside any protection for the original exception. Reproduced with in-memory fakes:

   | Original condition | Cleanup condition | Observed result |
   |---|---|---|
   | `SystemExit(17)` | Wait times out; stderr raises `OSError` | Returns `INVALID-WORKER` |
   | `KeyboardInterrupt` | Signalling fails; stderr raises `OSError` | Returns `INVALID-WORKER` |
   | Heartbeat raises `KeyboardInterrupt` | Group and PID signalling fail | Returns `INVALID-WORKER` |
   | `STOPPED-RESOURCE` | Emergency wait raises `KeyboardInterrupt` | Returns `STOPPED-RESOURCE`; interrupt swallowed |

   The heartbeat case originates at [supervisor:347–350](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/new1_supervisor.py:347): `kill_worker()` can raise before the bare `raise` preserves the original exception.

   Preserving an original ordinary error over a secondary reap timeout is reasonable. However, the current implementation does not reliably preserve control exceptions or their exit values. Reporting must not replace them, and interrupts during cleanup need explicit precedence and bounded cleanup handling. These violate requirements 1/4 despite the ordinary cases passing.

3. **Blocking — the PID fallback is not always signalling an owned process.**  
   [kill_worker:268–273](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/new1_supervisor.py:268) receives only a numeric PID. Both loop termination sites call it **after `process.poll()` reports exit** (:380–382 and :417–421). CPython’s successful `poll()` performs `waitpid`, releasing the child PID for reuse.

   Consequently, after group disappearance, `killpg()` can raise `ProcessLookupError` and the new fallback can send `SIGKILL` to an unrelated process that inherited that PID. The fake probe confirmed fallback invocation after reported reaping; actual PID reuse was not exercised.

   Recovering group `PermissionError` is in scope **while direct-child ownership remains valid**. Copying the helper from another supervisor does not establish that condition here. Preserve group cleanup, but make single-PID fallback conditional on valid child ownership. The new test at [tests:1015](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tests/test_new1_supervisor.py:1015) currently expects PID fallback after `poll()` reports exit, so it needs correction.

4. **Not blocking — once the process handle is captured, the ordinary exit-path restructuring is sound.**  
   The trace through [supervise:315–462](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/new1_supervisor.py:315) is:

   | Exit path | Reaping order |
   |---|---|
   | Leader-exit termination, :382 | `terminate()` executes `wait()` in `finally`; flags follow successful return. |
   | Successful loop-bottom termination, :421 | Same ordering, before prediction publication and normal return. |
   | Either termination call raises | Flags remain unset; lifetime cleanup retries outside the run alarm. |
   | Post-launch deadline/resource/monitoring/protocol/worker `Stop` | Lifetime cleanup runs before halt closeout and returned code. |
   | Pre-launch admission/history/resource/enforcement `Stop` | No worker exists, except the creation gap in finding 1. |
   | Post-commit recorded-outcome return, :447 | Successful loop teardown already occurred; lifetime context has exited before reconciliation. |
   | Body `KeyboardInterrupt`/`SystemExit` | Cleanup precedes re-raise, subject to finding 2. |
   | Exception from lifetime cleanup itself | Reaches the outer handler without another lifetime-cleanup pass. Failed wait remains unreaped. |

   **No assignment sets `worker_reaped=True` before `wait()` returns successfully**: the assignments are at :330, :382 and :421. A reported bounded timeout is the explicit exception permitted by requirement 2; it is not completed reaping.

5. **Not blocking — the independent reap bound and halt-receipt ordering are correct, subject to reporting failures above.**  
   Both wait sites use `REAP_TIMEOUT_S = 5` ([supervisor:42](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/new1_supervisor.py:42), :279, :329), without consulting `controller.remaining()`.

   Ordinary loop termination still runs under the run alarm and can be interrupted early. Crucially, the emergency retry does not: context managers exit right-to-left at :353, so `hard_deadline` disables its alarm at :129 before `worker_lifetime` waits.

   The halt receipt cannot precede that cleanup result. `reap_error` is established before the outer handler constructs its message at :449. With functioning stderr and remaining budget, the PID reaches both stderr and the receipt. With exhausted budget, stderr identifies the PID and reports incomplete closeout; no extra receipt budget is granted. A failed loop wait can therefore receive one additional independent five-second wait, not a renewed run budget.

6. **Not blocking — the saved evidence is authentic, but “15 distinct skip paths” overstates its coverage.**  
   I recomputed the before/after source hashes, test hash, saved RED test-copy hash, and both final log hashes. The logs contain exactly the listed **15 RED failures, zero errors**, and **76 GREEN results** ([evidence.json:66](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/mathlab_staging/new1_supervisor_reap_20261010T204549Z/evidence.json:66)).

   | Tests | Actual RED assertion |
   |---|---|
   | Ten: total/cell expiry, heartbeat expiry/denial, exception signalling denial, reporting order, loop signalling denial, closeout setup, KeyboardInterrupt, SystemExit | Expected wait; observed zero calls |
   | Termination wait consumes budget | Expected `[5,5]`; observed `[5]` |
   | Two unreaped-PID diagnostics | Required PID text absent |
   | Halt receipt and halt emit failures | Wait already occurred, but with `2700.0` rather than `5` |

   All 15 use the fake-process fixture at [tests:916](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tests/test_new1_supervisor.py:916), reuse the fake clock, and contain wait assertions. None launches a real worker. Their RED failures are relevant assertions, not import/environment accidents.

   However, the receipt/emit tests are ordering/bound regressions, **not independent original wait skips**. The suite also lacks constructor-interruption, failing-stderr, cleanup-interrupt, heartbeat double-signal-failure precedence, and reaped-PID ownership coverage.

7. **Blocking for advancement — r8 condition 3 remains open; r9’s numerical acceptance is unaffected.**  
   The diff leaves terminal-commit authority, event names, outcome vocabulary, main exit-code mapping, **2,700-second total**, **300-second cell wait**, and resource caps unchanged ([supervisor:24](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/new1_supervisor.py:24), :439–481). Halt durability still consumes only the original remaining budget. Nevertheless, finding 2 changes actual exceptional outcomes, and findings 1/3 leave lifecycle enforcement unsafe.

   Resolve those three findings with targeted failing-first regressions before presenting the combined implementation as ready for launch-readiness review. The projector fix’s r9 GO remains valid; it does not discharge these supervisor blockers or authorize a full attempt.

🌱 graft reported ~49,488 tokens saved this turn, one successful call.

VERDICT: NO-GO
