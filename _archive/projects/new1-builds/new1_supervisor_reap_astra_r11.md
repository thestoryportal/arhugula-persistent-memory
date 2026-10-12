**Two lifecycle blockers remain.** I verified the source/test hashes against `61d31d4`, audited the receipts, and ran in-memory probes. No files changed, workers spawned, or full suite rerun.

1. **Blocking — `returncode is None` does not always mean the PID remains owned.**  
   [tools/new1_supervisor.py:320](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/new1_supervisor.py:320) gates fallback correctly after a *completed* poll, but misses interrupted reaping.

   Installed [subprocess.py:1990](/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/subprocess.py:1990) calls `waitpid`; only afterward does :1992 update `returncode`. A `KeyboardInterrupt` between those operations unwinds with the child already reaped and `returncode=None`. Lifetime cleanup then calls `kill_worker`; if group signalling fails, it can signal the released PID.

   I reproduced this using the **installed `_internal_poll` implementation**, a fake successful `waitpid`, and real SIGINT delivery at line 1991. Intercepted output was:

   ```
   waitpid returned reaped PID 123
   SIGINT: returncode=None
   PID fallback: kill(123), returncode=None
   ```

   Actual PID reuse was not exercised. The current SIGALRM mask protects the check→signal interval, not the earlier waitpid→returncode interval. Protect ownership across interrupted reaping and add that regression.

2. **Blocking — heartbeat cleanup still swallows a newly arriving control exception.**  
   At [tools/new1_supervisor.py:414](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/new1_supervisor.py:414), every exception from `kill_worker()` becomes a note on the original heartbeat error.

   Reproduced sequence: `observe()` raises `Stop('STOPPED-RESOURCE', ...)`; group signalling fails; PID signalling raises `KeyboardInterrupt`; subsequent lifetime cleanup succeeds. **Observed: one five-second wait, then returned `STOPPED-RESOURCE`; no interrupt propagated.**

   This contradicts the [README precedence table:24](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/mathlab_staging/new1_supervisor_reap_r2_20261010T210738Z/README.md:24). Without an original control exception, the cleanup control exception must survive bounded cleanup. Apply the same precedence rule at this heartbeat boundary.

3. **Not blocking — all four original r10 table rows now produce the required outcomes.**  
   I independently reproduced each using the unchanged functions and fake IO/processes. The trace through [worker_lifetime:365](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/new1_supervisor.py:365) is:

   | Original condition | Cleanup condition | New-code trace and observed result |
   |---|---|---|
   | `SystemExit(17)` | Wait times out; stderr raises `OSError` | :393 captures timeout; :398–400 retain original control; :274–277 attach reporting failure; :535 re-raises **the same `SystemExit(17)`**. One wait, timeout 5. |
   | `KeyboardInterrupt` | Signalling fails; stderr raises `OSError` | :376 captures signalling failure; :383 still waits; precedence retains original; reporting cannot replace it; :535 re-raises **the same interrupt**. One wait, timeout 5. |
   | Heartbeat raises `KeyboardInterrupt` | Group and PID signalling fail | :417–419 note failure and re-raise original; lifetime cleanup retries signalling and waits; :535 re-raises **the same interrupt**. One wait, timeout 5. |
   | `STOPPED-RESOURCE` | Emergency wait raises `KeyboardInterrupt` | :386–388 retain interrupt and calculate remaining reap time; retry succeeds; :399–405 promote interrupt over ordinary `Stop`; :535 propagates it. Observed waits: **5 and approximately 4.99999 seconds**. |

   The emergency-wait `SystemExit(23)` counterpart and original-control-over-cleanup-control cases are covered at tests :1225 and :1234. Ordinary errors still outrank secondary ordinary signalling/wait errors. The README matches these paths, but its general precedence claim fails in finding 2.

4. **Not blocking — the reported constructor ownership gap is addressed for the examined CPython path.**  
   [tools/new1_supervisor.py:441](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/new1_supervisor.py:441) captures the object before explicit initialization. `constructor_ownership` defers callable signal handlers while its PID is absent; later constructor exceptions leave the handle available to :369.

   This addresses the installed constructor’s `_fork_exec`→`self.pid` boundary at subprocess.py:1885 and subsequent error-pipe reads at :1908. Its :1036 exception handler still does not guarantee reaping; supervisor cleanup now supplies that ownership.

   [tests/test_new1_supervisor.py:1140](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tests/test_new1_supervisor.py:1140) records a simulated child creation **before** injecting the exception or pre-PID alarm. These are meaningful post-creation fixtures, not pre-fork failures. They do not execute a real CPython fork. I found no additional constructor escape in the examined path; finding 1 prevents a universal lifecycle-safety claim.

5. **Not blocking — completed-poll fallback and the corrected test are right.**  
   [tests/test_new1_supervisor.py:1022](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tests/test_new1_supervisor.py:1022) now consistently sets both poll result and `returncode` to zero and expects no PID fallback. Group cleanup remains unconditional at supervisor :314; waiting remains required. Tests :1320 cover both group-failure classes. These establish completed-poll behavior, not the interrupted-poll boundary in finding 1.

6. **Not blocking — receipt identities/counts check out, with one RED-evidence qualification.**  
   The before/final hashes, saved test copy, and final log hashes match. [RED_final.log:368](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/mathlab_staging/new1_supervisor_reap_r2_20261010T210738Z/RED_final.log:368) records **94 tests, 22 failures across 19 methods, zero errors**; GREEN records **94 OK**. All five r10 coverage categories now have fixtures; the added/corrected tests intercept process creation and signalling. The entire suite also contains existing short subprocess fixtures.

   One RED is not the advertised causal assertion: the ownership-race test at :1342 fails against the old signature because it passes `Process()` where the old helper expects a numeric PID. Its first failing assertion is **object != 123**, before checking watchdog ordering. The GREEN assertion is useful, but that RED alone does not demonstrate the race. Neither remaining blocker is covered.

7. **Not blocking — r10’s accepted ordering/budgets and r9’s projector acceptance remain intact.**  
   [tools/new1_supervisor.py:422](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/new1_supervisor.py:422) still disables the run alarm before emergency reaping. Successful waits precede `worker_reaped=True`; cleanup results precede halt receipts. Emergency retries share one five-second deadline.

   Exit mapping, outcome strings, terminal-commit authority, event names, **2,700 s total**, **300 s cell wait**, resource caps, and **`REAP_TIMEOUT_S=5`** are unchanged. Halt durability still uses only `controller.remaining()` at :526. Geometry source/tests are unchanged from `57420ab`.

   Resolve findings **1–2**, with targeted regressions, before advancing the combined implementation to launch-readiness review.

VERDICT: NO-GO

