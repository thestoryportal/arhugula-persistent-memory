# GPT-6-Astra (high) — scope ruling r3: NEW-1 four-construction diagnostic, FIX3 STOPPED

Read-only. Worktree = current dir. Your r2 verdict is `results/mathlab_staging/new1_construction_diag_astra_r2.md` (or ~/.claude/jobs/8ac4cacf/tmp/astra_new1construct_r2_out.md). The operator authorized exactly one real run (`results/mathlab_staging/new1_construction_diag_authorization.md`); a defect found after launch costs it. Nothing launches until you rule.

Current uncommitted hashes (git diff shows the full change vs the last commit c914309):
tests/test_new1_construction_diag.py 2f5644627d6f…
tools/new1_construction_diag.py 238a9d9281c8…
tools/new1_identity_diag.py 14329bd0daa0…

## What happened
- FIX2 builder reported GREEN (182/182). On the host, MAESTRO10 found `tests.test_new1_construction_diag.ConstructionDiagnosticTests.test_stalled_launch_returns_within_bound_and_late_handle_cleans_once` red: 2/2 full suite runs and 9/10 solo runs fail at `self.assertEqual(owners[0].proof['kills'], 1)` (0 != 1). Red log: `results/mathlab_staging/new1_construction_diag_fix2_20261010T082936.611614Z/maestro10_verify_red_20261010.log`.
- FIX3 builder (sandbox) reran the unchanged test solo 20×: 7 PASS, 11 FAIL at kills==1, **2 ABRUPT EXIT** (process exit code 2, log ends right after the test name with no unittest result: `results/mathlab_staging/new1_construction_diag_fix2_20261010T082936.611614Z/red_fix3_mb15_solo_06.log`, `_18.log`). Index: `results/mathlab_staging/new1_construction_diag_fix2_20261010T082936.611614Z/red_fix3_mb15_solo.json`.
- The builder STOPPED without editing. Its reasoning, in full: `results/mathlab_staging/new1_construction_diag_fix2_20261010T082936.611614Z/fix3_mb15_root_cause.md`; samples `results/mathlab_staging/new1_construction_diag_fix2_20261010T082936.611614Z/fix3_mb15_ownership_trace_sample_{1,2,3}.json`. Summary of its claim: under the patched LAUNCH_S=CLEANUP_S=.05, the worker's own release guard can refuse and exit 2 before the guardian handles cancellation; `watchdog` checks `waitpid(WNOHANG)` first, reaps it, and never kills, so the proof truthfully says code 2, kills 0. Race with supervisor cancellation, which gives code -9, kills 1. The kills==1 assertion is not in the committed test (c914309); it was added in uncommitted FIX/FIX2 work. The neighboring `test_already_exited_unreleased_worker_is_reaped_without_group_signal` requires 0 kills for an already-exited worker.

## Rule on (cite file:line)
1. Is "exactly one kill" a real safety requirement for this schedule, or is the right property "the late handle is reaped exactly once, before the parent returns, with no live process and all owned fds closed", with kills ∈ {0,1} and consistent with the exit code (kills==1 ⇔ code -9; kills==0 ⇔ the worker exited by itself)? Verify the builder's waitpid-first account against the code.
2. The abrupt exit 2: which code path can make the **test (parent) process** exit with status 2 with no traceback (e.g. a forked child returning into the runner, an `os._exit(2)` reachable in the parent or in a fork that inherited the unittest runner, a guard thread)? Name it. Could the same path end the real diagnostic parent silently? Is it launch-blocking?
3. Give the minimal FIX4 contract as numbered, testable criteria (test-first, each with a RED). Or say no source change is needed and only the assertion changes. Also say how many host solo and full-suite repetitions are enough evidence of non-flakiness for these timing tests.

## Verdict
End with exactly one line: `VERDICT: GO` (launch as is: unlikely given finding 2), `VERDICT: FIX4` (with the contract above), or `VERDICT: NO-GO` (stop iterating; the design needs rethinking; say why).
