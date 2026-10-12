# GPT-6-Astra (high) — r5 ruling: NEW-1 four-construction diagnostic, step 4 (mechanism, production-fix scope, qualification plan)

Read-only. Worktree = current dir. Your r4 verdict is `results/mathlab_staging/new1_construction_diag_astra_r4.md` (VERDICT: INVESTIGATE, steps 1–4). Steps 1–3 were run under r4's caps and every cap is exhausted; step 4 is yours. Nothing has been fixed, nothing launches, and no host 100/10 batch runs until you rule. The failed FIX4 batch stays 0/3 permanently (r4 §4).

## Candidate (uncommitted, unchanged since r4; all five hashes re-verified 2026-10-10 by MAESTRO17)
tools/new1_construction_diag.py b1db5aa9ab2d6914c3f4b3601f0164a9c78686c443ebdaa3445f9ea9d0d391a4
tools/new1_identity_diag.py 1161503c55346fb5d47bbed462ec3de3b17698b0b94752dfef4d7bf4d0e2ff8a
tests/test_new1_construction_diag.py c80e08c5b36ffb9e5c83a2a47d9fdf28b223fb9e7e5d47a003893b681cbf69d4
tests/test_new1_identity_diag.py 7a9a6d3b74fe600cb4784c5711cde6fc6c373e11743ab7538d8afc86e155c6b1
results/mathlab_staging/new1_construction_diag_scope.md 77f3086cac50de8ba5896e5d7e4e4d5a3661ec43d136fa8c1a2cab53d1f8c607

Committed and unchanged: `tools/new1_supervisor.py`, `tests/test_new1_supervisor.py` (hashes in your r4 packet).

## The evidence
Receipt dir (RECEIPT): `results/mathlab_staging/new1_construction_diag_investigate_20261010T174911.191674Z/`. Report: `RECEIPT/investigation_report.md`. **Read the "## MB19 evidence audit" appendix (line 366 to the end) as the authoritative reading.** It is a run-free audit of MB18's lines 1–364 against the raw receipts and supersedes MB18's provisional readings; consult MB18's sections only where the audit cites them. R = `results/mathlab_staging/new1_construction_diag_fix4_20261010T104024.648040Z/` (the r4 subject).

Audited readings, under your r4 labels:
- **Step 1 — FAIL/inconclusive.** Three clean 188-method full runs; no attributable failure captured.
- **Step 2 — PASS-for-attribution.** Pre-FIX4 baseline run 3 (`RECEIPT/step2_baseline_03/suite.log:276–278`, 182 run / 7 failures) reproduced all six supervisor assertion categories plus the old construction kills assertion. The caller mask changes [] → [2,14] at the boundary after the unchanged identity deadline fixture (`RECEIPT/baseline_mask_transitions.json $.transitions[1]`; events `77436_000276.json`, `77436_000277.json`). The exact leaking instruction is not established.
- **Step 3 — FAIL.** Nine comparison runs (alone / numerical / lifecycle, 3 each) were clean. But the actual construction parent, with [2,14] imposed in-process before its main, missed the <.3 s deadline (masked preflight 2.02 s, masked monitor 2.05 s) and took production's own native exits: `tools/new1_identity_diag.py:631` (preflight, bounded terminal recording failed) and `:614` (monitor, cleanup reaping bound failed). Unmasked: 0.02–0.12 s, exit 0. Monitor ownership proof is incomplete. MAESTRO16 and MAESTRO17 confirmed both `_exit(2)` sites in source.
- **Lead table** (audit "### Final lead table"): established = blocked/pending SIGALRM defeating interruption under [2,14]; the unchanged `tools/new1_supervisor.py:411–428` cleanup-before-wait path (static budget exhaustion can skip `process.wait()`; distinct from the construction parent). Refuted = FIX4 required for the six symptoms; a runner/watchdog causing the masked exits. Open = the exact mask-leak instruction (source leads `tools/new1_identity_diag.py:495` and `:510`, before their inner restoration try/finally), observer role, warned PIDs 25689/78284, native-thread effects, real externally inherited-mask launch exposure, environment load.
- **MB19's proposal** (audit "### Revised PROPOSAL for Astra r5") is input to weigh, not a recommendation you must accept.

**Host-load note (MAESTRO15, `RECEIPT/maestro15_drift_reconciliation.md:14–16`), verbatim:** "every step-3 run (18:08–18:12Z) fell inside MB20's working window, during which MB20 ran only targeted unit-test classes. Step 1/2 times are in their own receipts. The step-3 actual-parent controls contrast unmasked 0.02–0.12 s with masked 2.02–2.05 s in the same window; load is recorded, not ruled out."

Storage note: the per-run `events/` directories (~81 MB) are on local disk at their receipt paths, read them there. A Drive backup copy is being made; the local copy stays until r5 closes.

## Rule on (cite file:line)
1. **Mechanism.** Do the receipts support a mechanism precise enough to fix against: a blocked [2,14] mask (from whatever source) leaves SIGALRM pending, so `supervise`'s deadline cannot preempt and the parent reaches the native fail-closed exits? Or is a missing piece (the exact leak instruction, inherited-launch exposure, load) load-bearing for the fix rather than merely open? Rule separately on the test-fixture leak (`:495`/`:510` leads) and on the production parent's behavior under a blocked mask.
2. **Production-fix scope.** Which arrangement is correct, and in which files: (a) reliable mask restoration / critical-section handling at the leak; (b) an explicit, bounded, fail-closed entry condition when the caller's mask blocks enforcement (an inherited blocked mask is permitted by the OS contract, so a fresh interpreter does not guarantee an empty one); (c) both; (d) another source-supported arrangement. Say whether `tools/new1_supervisor.py:411–428` (skipped wait) enters this fix's scope or stays a separate ownership issue, and whether the two native-exit branches at `:614`/`:631` are correct fail-closed behavior or themselves need change.
3. **Qualification plan.** With all step 1–3 caps exhausted: what must a corrected candidate pass, in order? Address: fresh 3/3 full sandbox batch under r4 §4; whether a masked actual-parent control becomes a required acceptance test (and its pass bar: <.3 s fixture, .2 s parent bound, ownership inspected before cleanup, native exit distinguished from terminal return); whether an externally inherited-mask launch control is material (it needs new operator authorization; name its single run if so); the host bar (r4: 100 solo + 10 full via `R/run_checks.py`, stop on first failure) restated or changed; and how the host-load note bears on any of it.
4. **Status from here.** Confirm the batch stays 0/3. State whether the current five candidate bytes may survive into the corrected candidate or must change.

## Verdict
End with exactly one line:
- `VERDICT: FIX5`: give the production-fix contract as numbered, testable criteria, each with a RED, plus the qualification sequence from item 3.
- `VERDICT: INVESTIGATE`: name the one further step that is load-bearing, why the fix cannot proceed without it, and its run count; it needs new operator authorization, since every r4 cap is spent.
- `VERDICT: NO-GO`: stop iterating on this diagnostic; say why.
