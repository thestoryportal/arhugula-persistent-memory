# Astra NEW-1 r10: review of the supervisor reap fix (MB27)

You are GPT-6-Astra, the cross-family reviewer for the LLM-as-Database program. This is a read-only review. Repo: this worktree, branch `worktree-c10k-route-a`, subject commit **a310686**.

## Subject
Your r8 verdict (`results/mathlab_staging/new1_construction_diag_astra_r8.md`, Q4 at :49-57, conditions at :66-75) named a launch blocker: `new1_supervisor.supervise` could skip `process.wait()` after a signal or deadline exhaustion. Condition 3 says: "Resolve and review full-worker lifecycle enforcement before launch." Codex MB27 built the fix test-first.
- Source: `tools/new1_supervisor.py`, a69d4107… → da9f250e…. It adds `REAP_TIMEOUT_S = 5`, `kill_worker` (group SIGKILL with a single-PID fallback, following `tools/new1_identity_diag.py:278-283`), and a `worker_lifetime()` context manager around `hard_deadline` inside `supervise`. The halt path no longer waits under `hard_deadline(controller.remaining())`. Review the full diff with `git show a310686 -- tools/new1_supervisor.py`.
- Tests: `tests/test_new1_supervisor.py`, 33c61282… → c3440f6b…. There are 15 new `test_reap_*` tests; the full list is in `evidence.json`.
- Receipts: `results/mathlab_staging/new1_supervisor_reap_20261010T204549Z/` (README.md, evidence.json, RED_final.log, GREEN_final.log, RED_final_tests.py, before/). The builder reports RED 76 run, 15 failed on a69d4107, and GREEN 76/76 on da9f250e. MAESTRO25 checked that the 15 RED failures are exactly the 15 new tests, that RED_final_tests.py hashes to c3440f6b…, and that a host rerun gives 76 OK.

## The brief's requirements (verbatim)
1. Invariant: once `supervise` has started the worker process, every exit from `supervise` (normal return, returned halt code, re-raised KeyboardInterrupt/SystemExit, post-commit recorded-outcome return) happens only after the worker has been signalled if still alive AND reaped by `process.wait()`. That includes the case where the run budget is already exhausted.
2. The reap after SIGKILL must not depend on positive remaining run budget. Use one fixed, short, documented post-SIGKILL reap bound (a SIGKILLed process exits promptly). If the reap still times out, the outcome must say so: the halt diagnostic and stderr name the unreaped PID. It must not return silently as if reaped.
3. Halt-receipt durability keeps its current rule: it consumes only the original remaining budget.
4. Unchanged: exit codes and outcome strings, the terminal-commit authority, event names, the budget numbers (2,700 s total, 300 s cell wait), and resource caps.
5. Failing-first: one test per distinct skip path, each RED on a69d4107… and GREEN after the fix; the deadline-exhaustion case is mandatory.

## Questions
1. Does requirement 1 hold on every exit path in the final source? Trace each one: normal completion via `terminate()`, the loop-exit terminate, every `Stop`, the post-commit recorded-outcome return (~:440-447), KeyboardInterrupt/SystemExit, and an exception raised inside `worker_lifetime`'s own finally. Name any path that returns before the wait, or that sets `worker_reaped=True` without a completed wait.
2. Requirement 2: is the 5 s bound independent of `controller.remaining()` on every reap? Confirm that `worker_lifetime` exits after `hard_deadline` (so the run alarm cannot interrupt the reap), and that an unreaped PID reaches both the halt receipt message and stderr. Can the ordering cause the halt receipt to be written before the reap result is known?
3. Error precedence: when an original error exists, a reap failure goes to stderr and into the halt message instead of being raised. When none exists, the wait error is raised. Is this correct? Can a reap or signal error mask a KeyboardInterrupt/SystemExit, or change an exit code or outcome string (requirement 4)?
4. `kill_worker` now treats a `PermissionError` from `killpg` as recoverable and falls back to `os.kill`. The old code caught only `ProcessLookupError`. Is that widening safe and in scope? Can it signal a PID the supervisor does not own?
5. Requirements 3 and 4: is anything else changed, including the halt-durability budget, the terminal-commit authority, event names, budgets and caps?
6. Requirement 5: is each of the 15 tests a real distinct skip path, built on the existing fake process/clock fixtures, with no real worker spawned? Does each one assert the wait itself, not just `killpg`? Are the RED failures the intended assertion and not an incidental error? Is any skip path left uncovered?
7. Is there anything else that blocks this fix, together with r9's projector fix (57420ab, VERDICT: GO), from entering the launch-readiness review for one full five-layer Amendment-B attempt?

## Output
Give numbered findings with file:line, each marked blocking or not blocking. End with exactly one line: `VERDICT: GO`, `VERDICT: GO-WITH-CONDITIONS` (list the conditions), or `VERDICT: NO-GO`.

A finding like "tests pass, looks fine" with no trace of the exit paths will not be accepted.
