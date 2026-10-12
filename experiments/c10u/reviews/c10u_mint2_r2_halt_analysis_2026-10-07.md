# D-C10u-mint2 r2 — stage `frozen` HALT analysis (2026-10-07 08:52 MDT)

**Verdict: harness defect, not a science gate.** r2 closes HALTED-HARNESS; step 3 continues as r3 under D-C10u-r3go with a one-line driver fix.

## What the run did before the halt
- Stage `reproduce` passed (STAGE_EXIT=0; LAW#3 reference A1 71 / A2 70; commit 66c662e).
- Stage `frozen` started 08:24. The block-F multi check passed the LAW#3 window: para_full 10 ∈ [5,18], canon 9 ∈ [5,10], para_first 52 ∈ [42,59]; A1 69/72 (`results/c10u_mint2/r2/F_r0_multi_snone.json`).
- Step 0 for `modifier` seed 0 returned **UNDERFIT** at the P3 admission screen: 17 of 24 heads at fit ≥ 0.98, underfit indices [1, 5, 8, 12, 13, 16, 20]; lowest capture Oxbarrow 0.133 (`results/c10u_mint2/r2/step0/F_r0_modifier_s0.json`, `logs/step0_F_r0_modifier_s0.log`). This is a designed, recordable outcome.

## The defect
- `behavior_job` (`experiments/track_c/c10u_mint2_arms.py:771–778` at r2's pinned hash bb122445…) handles a non-admitted step 0 by writing an explicit record (`outcome: UNDERFIT`, no `_started.json`, no model work) and returning **without printing anything**.
- The parent `spawn_job` (`:892–893`) treats an empty child log as a failed child and halts: `if result.returncode != 0 or not log.stat().st_size: halt("child failed; …")`. The child returned 0, its record `F_r0_modifier_s0.json` exists and is well-formed, and its log is 0 bytes.
- Diagnostic: `architecture_profile/c10u_mint2_halt_diagnostic_6508cfa1c1c945f294ad8e8115404dfa.json` (returncode 0, log path).
- No selftest exercised the non-admitted branch together with the parent's empty-log guard; this is the same class as the earlier false HALT the test-first rule was written for.

## Why r2 cannot simply resume
The driver never overwrites an occupied output (`:57–60`), the stage marker `frozen_started.json` is permanent, and every record pins the driver's source hash; D-C10u-r2go (3) forbids editing a pinned file while r2 is open. Any fix therefore requires a fresh output directory.

## Fix (the one read-then-fix allowed under halt discipline)
- `behavior_job` non-admitted branch now prints `BEHAVIOR <tag>: no behavioral run; step0 outcome=<outcome>` after writing its record. The parent's empty-log guard is kept unchanged (it still catches silent crashes).
- Test first: `SafetyTests.test_nonadmitted_behavior_child_logs_and_parent_accepts` drives the real `behavior_job` with a stubbed UNDERFIT step 0. It failed before the fix (`'UNDERFIT' not found in ''`) and passes after; suite 61/61.
- r3 launcher `tools/run_c10u_stage_r3.sh` differs from r2's only in the two output paths and the header comment.

## Cost
r3 repeats `reproduce` (r2: 07:13 → 08:23, 70 min) and the `frozen` work done so far (≈ 27 min) before reaching new ground. If r3 hits a further harness or science HALT, it stops there under halt discipline (no second speculative fix).
