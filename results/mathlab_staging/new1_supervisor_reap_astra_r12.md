1. **Blocking — the cleanup audit omits context-manager exits that can erase control exceptions.**  
   [tools/new1_supervisor.py:466](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/new1_supervisor.py:466) opens the log files; :473 enters the selector. Their exits run **before** `worker_lifetime` captures the governing exception at :393.

   I replayed **both r11 sequences through the new code**, using the installed `_internal_poll`, real SIGINT delivery, fake processes/signals, and in-memory filesystem sinks:

   | Sequence | Cleanup succeeds | Selector close raises `OSError` |
   |---|---|---|
   | Successful `waitpid` → SIGINT before `returncode` → group signal denied | Same `KeyboardInterrupt`; zero PID signals; one `wait(timeout=5)` | Returns `INVALID-WORKER`; interrupt lost; zero PID signals; one wait |
   | `STOPPED-RESOURCE` → group signal denied → PID signal raises `KeyboardInterrupt` | Same interrupt after one `wait(timeout=5)` | Returns `INVALID-WORKER`; interrupt lost; one wait |

   The selector replay used the installed `BaseSelector.__exit__`, which calls `close()`. Separate stdout/stderr exit probes likewise replaced both `KeyboardInterrupt` and `SystemExit(17)` with `INVALID-WORKER`. The ordinary close error becomes `original_error`; lifetime cleanup cannot recover the earlier control exception.

   This predates R3, but contradicts the claimed comprehensive precedence audit. Preserve exception precedence across selector and log-file exits and add regressions before promotion.

2. **Not blocking — r11 finding 1 is fixed for the specified interrupted-poll sequence.**  
   [tools/new1_supervisor.py:314](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/new1_supervisor.py:314) masks SIGINT/SIGALRM across polling and restores the previous mask afterward. In all three poll locations, SIGINT was injected after successful `waitpid` while `returncode=None`; exit-status assignment completed before delivery. Failed group signalling therefore caused **no single-PID signal**.

   The documented masked bodies contain nonblocking polling/signalling or a wait bounded by five seconds. They exclude resource probes, persistence, selector waits and constructor IO. Ctrl-C delivery during emergency waiting can now wait up to the remaining reap bound; the run alarm is already disabled there. Normal-path `terminate()` follows an exited-worker poll, so its real wait returns immediately. Neither absolute deadline is reset.

3. **Not blocking — r11 finding 2’s heartbeat boundary is fixed.**  
   [tools/new1_supervisor.py:443](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/new1_supervisor.py:443) promotes the new cleanup control exception over the ordinary resource stop. With subsequent cleanup successful, both `KeyboardInterrupt` and `SystemExit(23)` propagated unchanged after **exactly one `wait(timeout=5)`**.

   The listed boundaries follow their stated policies, including the explicit reporting-only exception for stderr failures. The audit’s completeness fails at finding 1.

4. **Not blocking — the `terminate()` change is correct and within scope.**  
   [tools/new1_supervisor.py:341](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/new1_supervisor.py:341) still attempts the bounded wait after signalling fails, but retains the first exception when a secondary ordinary wait error loses precedence. All three new cases passed. I also replayed the four previously accepted r10 exception-precedence rows; their outcomes remain unchanged.

5. **Not blocking — the replacement RED evidence is causal.**  
   [tests/test_new1_supervisor.py:1342](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tests/test_new1_supervisor.py:1342) and the next two methods reproduced **eight failures on the pinned old source and zero on the new source**: three released-PID signals, two swallowed controls, and three replaced termination exceptions. These reached the intended assertions, not signature failures.

   Source/test pins and all 17 receipt artifact hashes verified. Saved logs show **97 tests / eight failures** and **97 tests / OK**. The round-2 signature-failure qualification is correctly retained. New regressions spawn no worker; the full saved suite includes existing short subprocess fixtures. I did not rerun that full suite.

6. **Not blocking — accepted constants and terminal authority are unchanged.**  
   [tools/new1_supervisor.py:24](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/new1_supervisor.py:24), :42, :530, :553 and :590 preserve resource caps, 2,700 seconds, 300-second cell waiting, five-second reaping, terminal-commit authority, halt-durability budgeting, event/outcome strings and exit mapping. Geometry source/tests are byte-identical to `57420ab`. **Finding 1 blocks entry into launch-readiness review.** No files changed or workers launched during this review.

🌱 graft reported ~6,979 tokens saved this turn, one successful call.

VERDICT: NO-GO

