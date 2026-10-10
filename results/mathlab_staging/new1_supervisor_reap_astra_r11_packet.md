# Astra NEW-1 r11: re-review of the supervisor reap fix, round 2

You are GPT-6-Astra, the cross-family reviewer for the LLM-as-Database program. This is a read-only review. Repo: this worktree, branch `worktree-c10k-route-a`, subject commit **61d31d4**.

## Subject
Your r10 verdict (`results/mathlab_staging/new1_supervisor_reap_astra_r10.md`, VERDICT: NO-GO) found three blocking lifecycle issues in a310686 (finding 1: interrupted `Popen()` constructor; finding 2: cleanup errors masking KeyboardInterrupt/SystemExit; finding 3: PID fallback after reap). It also listed coverage gaps (finding 6). Codex MB27 fixed them test-first.
- Source: `tools/new1_supervisor.py`, da9f250e… → e61d4802…. Review it with `git diff a310686 61d31d4 -- tools/new1_supervisor.py`.
- Tests: `tests/test_new1_supervisor.py`, c3440f6b… → 4e8d70a1…, with 18 new tests plus a correction to the round-1 test now at :1022.
- Receipts: `results/mathlab_staging/new1_supervisor_reap_r2_20261010T210738Z/` (README.md with the constructor rationale and a precedence table, evidence.json, RED_final.log, GREEN_final.log, RED_final_tests.py, before/). The builder reports RED on da9f250e as 94 run with 22 assertion failures across 19 methods (18 new plus the corrected one; subtests account for the rest) and zero errors, and GREEN as 94/94. MAESTRO25 checked that before/ hashes to da9f250e/c3440f6b, that RED_final_tests.py equals the final test file, and that a host rerun gives 94 OK.

## Questions
1. Finding 1: can a child created by `Popen()` now escape signalling and reaping on any path, including an exception or alarm between child creation and assignment? Check the approach against the installed CPython constructor you cited (subprocess.py ~:1036, ~:1883). Does the test exercise "child created, then the constructor raises or is interrupted", not just a pre-fork failure?
2. Finding 2: reproduce your r10 table (four rows). Does each row now give the correct outcome: original KeyboardInterrupt/SystemExit re-raised with its exit value; an interrupt during the emergency wait propagating after bounded cleanup; the heartbeat path (`kill_worker()` raising) not replacing the original? Is the precedence table in the README what the code does? Is ordinary-error behavior unchanged?
3. Finding 3: does the single-PID fallback run only while the child is unreaped (`returncode is None`)? Is group cleanup preserved? Is the corrected test at :1022 right?
4. Did round 2 change anything requirement 4 of r10 protects: exit codes and outcome strings, terminal-commit authority, event names, 2,700 s, 300 s cell wait, resource caps, the halt-durability budget, `REAP_TIMEOUT_S = 5`? Did it reopen anything you accepted in r10 findings 4-5?
5. Coverage: are your r10 finding-6 gaps now covered (constructor interruption, failing stderr, cleanup interrupt, heartbeat double-signal-failure precedence, reaped-PID ownership)? Are the RED failures the intended assertions, with no real worker spawned?
6. Anything else that blocks this supervisor, together with r9's projector fix (57420ab), from entering the launch-readiness review?

## Output
Give numbered findings with file:line, each marked blocking or not blocking. End with exactly one line: `VERDICT: GO`, `VERDICT: GO-WITH-CONDITIONS` (list the conditions), or `VERDICT: NO-GO`.

A finding that does not trace the four r10 table rows through the new code will not be accepted.
