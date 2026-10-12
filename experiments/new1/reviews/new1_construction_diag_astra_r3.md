**FIX4 is required.** The exact-one-kill assertion is overstrict, but changing it alone would leave unexplained parent termination and a child-containment defect.

Read-only review completed against all three supplied hashes; they remained unchanged. No tests, workers, or real diagnostic were launched.

**1. Ownership is the requirement; exactly one kill is not.**

The builder’s account is correct, with one qualification: the guardian drains the registration ACK before checking `waitpid(WNOHANG)`. Once that ACK is drained, it checks/reaps the worker **before** processing cancellation. A collected exit sets `status` and bypasses both cancellation and the final conditional kill. See `tools/new1_identity_diag.py:325–354`.

The worker can independently refuse an expired or invalid release at `tools/new1_identity_diag.py:227–265`; the construction worker entry converts that refusal into exit **2** at `tools/new1_construction_diag.py:243–245`. Thus **code 2, kills 0** is legitimate. The three ownership samples support this explanation, but their OS checks occurred **after test completion**, not precisely at supervisor return.

The required property is: worker reaped once, guardian reaped once, no surviving owned worker, all owned descriptors closed, and no arithmetic reached—before ordinary supervisor return. Preserve the existing `.3 s` bound and `STOPPED-LAUNCH` assertion at `tests/test_new1_construction_diag.py:520–532`. The neighboring zero-kill test agrees (`:534–543`). Inspection of `c914309` confirms the stalled-launch test originally contained no kill-count assertion.

**Do not replace it with the proposed unconditional biconditional.** `kills` counts a termination **attempt** (`tools/new1_identity_diag.py:278–301`). A worker can exit between the nonblocking wait and that attempt; **kills 1, code 2** can therefore also be truthful. Require `(0, 2)` for a deterministically already-exited fixture and `(1, -9)` for a deterministically live worker killed by this guardian. Treat the unsynchronized race according to actual wait status and attempted action.

**2. The parent has explicit silent-exit paths.**

These are ordinary supervisor code, not a worker guard thread:

| Location | Reachable condition |
|---|---|
| `tools/new1_identity_diag.py:478–485` | Alarm handling reaches the original absolute end: `_exit(2)` at **482**. |
| `tools/new1_identity_diag.py:604–612` | Initial cleanup fails, then `cleanup(end)` also raises: `_exit(2)` at **612**. This can happen **before** the deadline if both failures are immediate. |
| `tools/new1_identity_diag.py:623–629` | Terminal recording fails and bounded fallback reporting also fails: `_exit(2)` at **629**. |

These calls bypass unittest completion and traceback reporting. Moreover, the fixture redirects stderr into an in-memory buffer (`tests/test_new1_construction_diag.py:37–43`), so intermediate messages can disappear with the process.

There is also a concrete **fork-containment hole**: `OwnedWorker.start()` calls `watchdog()` in the child without an unconditional child-exit boundary (`tools/new1_identity_diag.py:380–389`). Guardian initialization precedes its protected `try` (`:287–302`), and its final wait/send can raise before `_exit` (`:345–354`). Such exceptions can unwind into the inherited supervisor/test stack. A failed guardian can then leave the actual parent without a worker-reaping proof, triggering cleanup failure and parent exit at **612**.

**The saved logs cannot establish which path fired in runs 06 and 18.** They contain no PID, exit-site, stack, or cleanup-error evidence. Claiming an exact historical attribution would be invented.

**Yes, the real diagnostic parent can terminate through these same paths:** its entry calls this supervisor at `tools/new1_construction_diag.py:239–240`. The unexplained occurrence during an ordinary stalled-launch fixture is launch-blocking. A deliberate fail-stop for genuinely unresolved ownership must not simply be removed.

**3. Minimal FIX4 contract**

1. **Correct and strengthen the ownership test.**  
   **RED:** preserve the existing zero-kill failures; add deterministic already-exited, still-live, and exit-between-wait-and-kill schedules. Record ownership state immediately when supervision returns, before fixture teardown can repair it.  
   **GREEN:** retain the current timing, failure-status, and no-arithmetic requirements; prove both reaps and descriptor closure. Check kill attempts against each controlled schedule without imposing a false global biconditional.

2. **Contain every guardian-child escape.**  
   **RED:** inject a guardian setup exception before its current `try`, and separately a final receipt-send exception; detect any return/unwind into inherited supervisor or unittest code using PID-tagged sentinels.  
   **GREEN:** the guardian child always terminates within its child boundary. Failures after worker creation retain bounded worker termination/reaping responsibility. The actual parent handles missing proof as failure; it never invents successful cleanup.

3. **Identify and reproduce the abrupt parent exit before fixing its trigger.**  
   **RED:** run the unchanged failing schedule under an external fixture observer, recording PID/role, exact `_exit` caller, primary and cleanup exceptions, deadline remaining, and ownership state. Instrumentation must preserve actual exit behavior. Capture an occurrence, then make its triggering schedule deterministic.  
   **GREEN:** that ordinary stalled-launch schedule returns bounded `STOPPED-LAUNCH`, with completed ownership checks and unittest completion. Separately force genuine cleanup-proof failure and terminal-output failure: preserve bounded fail-closed behavior and externally distinguish it from successful cleanup. Do not obtain GREEN by deleting emergency exits, adding retries, or enlarging caps.

Keep production edits within lifecycle/error handling and necessary source-pin updates. Preserve scientific functions, inputs, projector gate, output schema, four constructions, and authorization. Refresh hash-bound receipts and launch command, then return for review; FIX4 is **not** launch approval.

For repeatability, require **100 consecutive fresh-process host solo runs** of the corrected failing test and **10 consecutive fresh-process runs of all four acceptance suites**, retaining the existing 182 methods plus new regressions. Every run must have exit 0, complete expected unittest results, and no ResourceWarnings, timeout, abrupt exit, or cleanup leakage. Preserve all failures; do not restart counting selectively.

Those repetitions are a practical acceptance threshold, **not proof of non-flakiness**. Deterministic coverage of the identified schedules is essential.

🌱 graft reported ~49,053 tokens saved (~$0.04); one successful call and one failed probe.

VERDICT: FIX4

