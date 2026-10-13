# D-C10s-solvefeas — verdict review

Reviewer: Codex  
Model: GPT-6 (exact runtime variant not exposed)  
Effort: high (review depth)  
Date: 2026-10-07

**Verdict: UNDERFIT-AT-50 CONFIRMED — qualification: objective-stopped.**

Review only. I ran the specified model-free reader with `LLMDB_ROOT` set to this worktree and `C10S_ARM=solvefeas`; it exited 0 with this label. I also recomputed the frame fits, stopping classifications, paired screen, twin and snapshot totals from the JSON, and checked the recorded source hashes against `/usr/bin/git show 400f051:<path>` and current file bytes. No model was loaded and no GPU experiment was run during this review.

## 1. Validity and provenance

**The completed cell-1 run is valid under v2. No blocking defect found.**

- **Source identity:** all 14 declared hashes in each of the standalone inertness, run and injection records match commit `400f0516788c25efbace7c647fbd2cab85e8948b` and the current source files. Their aggregate digest recomputes to `943c2b98e2f200a3097da343146f1e7bf7ce9762de8ec0e68c0050c654b91c40`. The implementation commit predates the inertness run. The run/injection identity is `2026-10-07T053918Z-943c2b98e2f2`, bound to inertness `2026-10-07T053019Z-943c2b98e2f2`. The embedded inertness record equals the standalone record exactly; run and injection identities also agree exactly. (`results/c10s_solvefeas/run.json:10`; `results/c10s_solvefeas/inertness.json:8`; `results/c10s_solvefeas/inject.json:8`; digest construction: `experiments/track_c/c10s_sharedz_arms.py:191`.)
- **Settings and selector:** the two settings files differ only in `v_num_grad_steps`, 25 → 50. The actual steps50 file hashes to `f7a10f00eb1f7e37764aba0f6a231b3b0d316066f7f734f1e418a339acaeff33`, matching the records and every counted solve. The closed selector binds the solvefeas Decision-ID, prereg, halt path, settings and cap together; the driver sets `HP_CANDIDATE` before importing the harness, then rebinds and asserts `hp`. The fixed unknown-arm path exits without writing step 1's diagnostic. (`docs/C10S_SOLVEFEAS_PREREG.md:31`; `experiments/track_c/c10s_sharedz_read.py:62`; `experiments/track_c/c10s_sharedz_arms.py:100`, `:126`, `:146`; `results/c10s_solvefeas/run.json:2`.)
- **Inertness binding:** complete ALL INERT, all five checks true, engine fingerprint d941a9fb/PASS. Single, triplicate and heterogeneous same-batch parity are 0.0. The standing harness gate has |Δexpr| = 0.0003 and |Δloc| = 0.19 with `Z_OVERRIDE` unset. The 7-row versus 19-row engine distance 0.2223415 and step-0 NLL discrepancies are recorded quantities under A2, not failed parity gates. The driver's binding checks both settings and source identity before cell 1. (`results/c10s_solvefeas/inertness.json:83`, `:2657`, `:5595`, `:8909`, `:8916`; `docs/C10S_SHARED_Z_PREREG.md:80`, `:82`; `experiments/track_c/c10s_sharedz_arms.py:703`.)
- **Budget positive control:** 48 counted engine solves, comprising 24 canonical and 24 noise twins, plus 24 shared histories. Recomputed counts show 20 canonical, 22 twins and 23 shared solves ran more than 25 evaluations; 13 engine solves and six shared solves reached evaluation 50. This is an exercised budget, not merely a recorded setting. The reader returns no injection-validity reasons and budget `ok=True`, `positive_control=True`. Training-form hashes, held-out hash and the zero-overlap audit also recompute correctly. (`results/c10s_solvefeas/inject.json:82570`, `:83436`; `results/c10s_solvefeas/run.json:9076`, `:9091`, `:9099`; rules: `experiments/track_c/c10s_sharedz_read.py:137`, `:163`.)

Validity here covers cell 1. The write-pass A1/A2 ≥ 68 gates, reference envelope, locality, write-size and replication checks were not reached; `passes` is empty and neither pass file exists. The inertness harness check does not substitute for those write-pass gates. (`results/c10s_solvefeas/run.json:9202`; `docs/C10S_SOLVEFEAS_PREREG.md:11`, `:27`.)

## 2. What the label and the 0.98 bar mean

The frozen fit rule vetoes advancement whenever any subject/frame fit is below 0.98. Both residual failures ended on `loss<0.05` at **evaluation 27, after 26 Adam updates**:

| Entry | Fit at evaluation 25 | Fit at stop | Total loss at stop | Class |
|---|---:|---:|---:|---|
| Plurnak T2 | 0.977341956 | 0.971150439 | 0.048825458 | objective-stopped |
| Vorlex T2 | 0.964667247 | 0.975820187 | 0.049707673 | objective-stopped |

Sources: `results/c10s_solvefeas/inject.json:7131`, `:7864`, `:7942`, `:68727`, `:69460`, `:69538`; classification: `docs/C10S_SOLVEFEAS_PREREG.md:18`, `:25`; `experiments/track_c/c10s_sharedz_read.py:98`, `:127`.

**“AT-50” names the configured cap; it does not mean these two solves exhausted 50 evaluations.** The code uses the engine's verbatim mean-NLL + KL + weight-decay threshold, checked before the next update. Satisfying that scalar loss does not imply every frame clears 0.98. Fit is an average across context templates of `exp(-mean token NLL)`, a teacher-forced diagnostic, not a full-sequence probability or a minimum over individual prompts. The two criteria were deliberately frozen separately. This is a valid failure of the advancement gate under the faithful stopping rule, not a reason to waive the gate or declare the implementation invalid. (`memit_dry_run/memit/memit/compute_z.py:149`, `:158`, `:164`; `experiments/track_c/c10s_sharedz_arms.py:355`, `:371`; `experiments/track_c/c10s_sharedz_read.py:265`; `docs/C10S_SHARED_Z_PREREG.md:22`, `:31`, `:33`.)

Plurnak's T2 fit declines from evaluation 25 through the stop even while total loss crosses the threshold. Thus more evaluations need not improve every frame. Neither early objective stopping nor that decline proves the radius is insufficient, the KL/weight-decay trade-off is binding, or the frames are inherently incompatible. Read prereg §3's “neither the budget nor (b)/(c)” as a **termination classification**, not a causal exclusion of (b)/(c). Those explanations remain unseparated. Increasing only the cap again would retain the same evaluation-27 early stops in this process. (`results/c10s_solvefeas/inject.json:7133`, `:7864`; `docs/C10S_SOLVEFEAS_PREREG.md:18`.)

CORPUS/52 may record the valid qualified label, improved same-run fits, injection observations, noise twin and control c. It must retain the underfit veto, unedited-model scope, missing write evidence and unresolved frame hypothesis. The screen's 72/72 and the snapshot's 70/72 do not establish a successful weight edit: CORPUS/46 F-D1 directly demonstrates dependence on the surrounding model. (`results/c10s_solvefeas/inject.json:57`, `:125`, `:82097`, `:83443`; `CORPUS/46_C10M_DIAG_READPARTITION_EDITINJECT.md:30`.)

Count clarification: the printed `mean_steps=37.83` is mean **Adam updates**; mean loss evaluations is **38.83**. Use both names accurately. (`experiments/track_c/c10s_sharedz_arms.py:386`, `:579`; `results/c10s_solvefeas/inject.json:158`.)

## 3. Comparison with CORPUS/51 and explanations (a)/(b)/(c)

CORPUS/51 had 18 underfit entries across seven subjects at its 25-evaluation stop, minimum 0.8437, with canonical/shared/twin injection 51/69/54. This run ends with two underfit entries and injection 54/72/56. That comparison is **across different context-template draws**, not a paired estimate of the budget effect. (`CORPUS/51_C10S_SHAREDZ.md:10`, `:12`, `:16`, `:20`; `docs/C10S_SOLVEFEAS_PREREG.md:6`; recorded draws: `results/c10s_sharedz_r2/inject.json` field `ctx`, `results/c10s_solvefeas/inject.json:45`.)

The binding comparison is stronger and different: **inside this run, 29 failing entries across 13 subjects at evaluation 25 become two across two subjects at the stop**; the minimum rises **0.925487 → 0.971150**. All 27 other initially failing entries clear 0.98 at the stop. The shared-target injection moves **70/72 → 72/72** on the same held-out prompts, a record-only observation. The snapshot is taken before evaluation 25's update, matching the 25-cap returned state. (`results/c10s_solvefeas/inject.json:83246`, `:83397`, `:83443`; `experiments/track_c/c10s_sharedz_arms.py:369`; `docs/C10S_SOLVEFEAS_PREREG.md:14`.)

**EVIDENCE-SHOWS:** additional allowed evaluations at the same radius repair much of the fit deficit in this process. **I-INFER:** explanation (a), insufficient iterations, contributed substantially; the record weakens an interpretation of the earlier underfit as intrinsic joint-frame infeasibility. It does **not** earn the prereg label BUDGET-BINDING, which requires the complete final fit gate to pass. The two remaining failures are objective-stopped, not plateaued or still-descending at evaluation 50. There is no classified plateau evidence for (b) or (c), and both remain untested as explanations of attainable fit under another stopping/objective design. All 24 solves hitting the clamp does not establish an infeasible radius. (`docs/C10S_SOLVEFEAS_PREREG.md:23`, `:25`; `results/c10s_solvefeas/inject.json:157`, `:83413`.)

## 4. Next step and candidate

**Agree: step 2 next, carrying the canonical target.** Every UNDERFIT-AT-50 branch routes there. The shared target has not earned the replicated write-arm LEAD needed to become the default; no second process is required to promote this underfit screen. (`docs/C10S_SOLVEFEAS_PREREG.md:25`; `docs/C10S_SHARED_Z_PREREG.md:44`, `:51`; `docs/C10T_SECONDKEY_PREREG.md:7`.)

**Candidate only:** a separately pre-registered fit-guarded stopping rule: retain the mean objective, current radius and 0.98 diagnostic, but allow an objective-based early stop only when `total_loss < 0.05` **and every training frame clears 0.98**. Keep a fixed cap and classify failure at that cap honestly. This deliberately departs from the engine's verbatim stopping rule; it is a new hypothesis about stopping adequacy, not a repair needed for this valid run. It requires its own review and applicable inertness controls before any run, cannot relabel this result, and has not earned priority ahead of step 2. A larger radius or different KL/weight-decay objective would be separate candidates. (`docs/C10S_SHARED_Z_PREREG.md:22`; `docs/C10S_SOLVEFEAS_PREREG.md:11`; observed early stops: `results/c10s_solvefeas/inject.json:7131`, `:68727`.)

## 5. Exact proposed CORPUS/52 wording

The following is proposed text only; this review does not create or edit CORPUS/52.

```markdown
# 52 — Shared-target solve feasibility: UNDERFIT-AT-50, objective-stopped — added evaluations repair most same-run fit failures, but the frozen per-frame gate still fails; the write arm did not run

_Result 2026-10-07 UTC. Decision-ID D-C10s-solvefeas. Pre-registration docs/C10S_SOLVEFEAS_PREREG.md v2, inheriting docs/C10S_SHARED_Z_PREREG.md v3 + A1 + A2 v2. Source commit 400f051; all 14 declared hashes verified against that commit and the reviewed source files. Binding records results/c10s_solvefeas/{inertness,run,inject}.json; logs results/c10s_solvefeas_logs/{inertness,arms_first}.log. Run 2026-10-07T053918Z-943c2b98e2f2, bound to complete ALL-INERT record 2026-10-07T053019Z-943c2b98e2f2. Engine unmodified, fingerprint d941a9fb/PASS. Verdict review: results/c10s_solvefeas_codex_verdict.md. Lineage: CORPUS/51, CORPUS/46 F-D1._

## Pre-registration and claim class

This is a mechanism/solve-feasibility screen on the C10 write path, target definition: Qwen2.5-3B fp16 MPS, z-layer 8 of band 4–8, N = 24 A7 facts × three held-out prompts, one process, injection into the unedited model. Cell 2 did not run.

The sole settings change is the solve cap, 25 → 50 evaluations, for canonical, shared, twin and inertness solves. The frames, held-out set, radius 0.75, KL/weight-decay settings and engine-verbatim total-loss stopping rule remain fixed. The advancement gate requires every subject/frame's context-averaged teacher-forced fit ≥ 0.98; any failure gives UNDERFIT-AT-50 with the prescribed stopping qualification. A fit pass would be BUDGET-BINDING if evaluation 25 failed, or FIT-PASSES-AT-25 otherwise. The prereg's rationale predicted added evaluations could relieve ongoing descent and expected most shared solves to use all 50; actually six reached evaluation 50, five budget-stopped and one objective-stopped. The pre-registered classification accommodates early stopping.

## VERDICT — UNDERFIT-AT-50, qualified objective-stopped

The run is valid: settings and source identities bind, all inertness checks pass, and the larger-budget positive control is exercised. Shared and engine targets agree exactly at the same batch shape; engine 7-row versus 19-row relative distance 0.2223415 is recorded under A2, not gated. The standing harness inertness gate is |Δexpr| = 0.0003, |Δloc| = 0.19. Training-form hashes and zero word-3-gram overlap are present and verified. Source: results/c10s_solvefeas/run.json:10; inertness.json:2657, :5595, :8909; inject.json:83436.

| Same-run readout | Evaluation 25 | At the stop |
|---|---:|---:|
| Subject/frame entries below 0.98 | 29 / 72, across 13 subjects | 2 / 72, across two subjects |
| Minimum teacher-forced frame fit | 0.925487 | 0.971150 |
| Shared-z held-out injection, full-sequence greedy (record only) | 70 / 72 | 72 / 72 |

The evaluation-25 snapshot is the pre-update state a 25-cap solve would return in this process. Source: results/c10s_solvefeas/inject.json:83246, :83397, :83443; experiments/track_c/c10s_sharedz_arms.py:369.

| Remaining underfit entry | Evaluation-25 fit | Final fit | Stop |
|---|---:|---:|---|
| Plurnak T2 | 0.977342 | 0.971150 | loss 0.048825 < 0.05, evaluation 27 / 26 Adam updates |
| Vorlex T2 | 0.964667 | 0.975820 | loss 0.049708 < 0.05, evaluation 27 / 26 Adam updates |

Both entries are objective-stopped. “AT-50” denotes the configured cap, not exhaustion of that cap by these solves. Mean Adam updates 37.83; mean loss evaluations 38.83. All 24 shared solves hit the clamp at least once. Sources: results/c10s_solvefeas/inject.json:7131, :7864, :68727, :69460, :157, :158.

## Recorded observations — injection screen, unedited model

Final canonical/shared held-out injection is 54/72 versus 72/72, net +18: +5/+10/+3 over the three held-out templates, positive net gain on 15 subjects. Canonical-template injection is 24/24 for both. The screen arithmetic passes, but the fit veto takes precedence. The same-run evaluation-25 shared target scores 70/72, distributed 23/23/24; it is record-only and does not enter a gate. Sources: results/c10s_solvefeas/inject.json:57, :112, :83443.

The canonical-objective noise twin at the shared batch shape scores 56/72 versus canonical 54/72: gain +2, admissible under |gain| < 6, with 14/72 pairs disagreeing. This is observed null discordance, not a false-positive rate or proof of freedom from numerical effects. Its gain is not subtracted from the shared gain. Source: results/c10s_solvefeas/inject.json:82097.

Control c, plain training prompts, full-sequence greedy canonical/shared:

| Frame | Additive intervention | Absolute overwrite |
|---|---|---|
| CANON | 24/24 vs 24/24 | 24/24 vs 24/24 |
| T1 | 4/24 vs 24/24 | 3/24 vs 24/24 |
| T2 | 5/24 vs 24/24 | 11/24 vs 24/24 |

The canonical delta is reconstructed as z_engine − captured target_init; the shared delta is the saved optimizer delta. Plain-prompt greedy success does not override contextual teacher-forced underfit. Source: results/c10s_solvefeas/inject.json:125; experiments/track_c/c10s_sharedz_arms.py:529.

## Mechanism — what this resolves and does not resolve

EVIDENCE-SHOWS: at the same radius and on the same context draw, extra allowed evaluations repair 27 of 29 initially failing subject/frame entries. I-INFER: insufficient iterations contributed to the fit deficit in this process. Nevertheless, the complete gate fails, so this is not the pre-registered BUDGET-BINDING outcome.

The two remaining solves satisfy the engine's averaged total-loss threshold before all frames satisfy the diagnostic bar. The averaged rule is not an all-frame guarantee. Plurnak's T2 fit falls from 0.977342 at evaluation 25 to 0.971150 at the returned stop; improvement is not monotone in every frame. With the same stopping rule, merely increasing the cap again would retain these early stops. No residual entry is classified plateaued or still-descending at evaluation 50. Radius/regularization limits and intrinsic frame tension remain unseparated and unproven; clamp hits alone do not establish infeasibility. Sources: results/c10s_solvefeas/inject.json:83413; memit_dry_run/memit/memit/compute_z.py:149, :164.

CORPUS/51 recorded 18 underfit entries at its 25-evaluation stop, minimum 0.8437, and canonical/shared/twin injection 51/69/54. This run's two final failures and 54/72/56 injection are observations on a different context-template draw. The paired budget evidence is this run's 29 → 2 and 0.925487 → 0.971150, not a causal 18 → 2 comparison across processes. CORPUS/51 remains unchanged. Sources: CORPUS/51_C10S_SHAREDZ.md:10, :12, :20; docs/C10S_SOLVEFEAS_PREREG.md:6.

## Caveats kept flush

The target remains underfit under the frozen rule. All injection counts are on the unedited model: CORPUS/46 F-D1 found the same pre-edit target fall from 51/72 to 23/72 when injected after the edit. Consequently 72/72 does not establish a successful write, an edited-model ceiling, a replicated LEAD, §8.9 closure or an F1 change. Fit is the context average of exp(−per-prompt mean token NLL), not full-sequence probability. The forms were authored with the held-out set in view; zero shared word-3-grams establishes lexical separation, not an author-blind or structurally independent hold-out. The screen is not a calibrated significance test. Write performance, write-pass controls, locality, write size and replication remain untested. H-1 stays unresolved; C10 stays OPEN/BLOCKING; F1 unchanged. Sources: CORPUS/46_C10M_DIAG_READPARTITION_EDITINJECT.md:30; docs/C10S_SHARED_Z_PREREG.md:26, :53.

## Decision-ID and FORK

D-C10s-solvefeas: valid UNDERFIT-AT-50, objective-stopped; this candidate configuration was not advanced and the write arm did not run. Per prereg §3, next is step 2, the value-internal second key, carrying the canonical target. The shared target has not earned adoption.

Candidate only: a new fit-guarded early-stop hypothesis requiring each frame's ≥ 0.98 fit in addition to the averaged total-loss criterion, with its own pre-registration, review and applicable inertness controls. This deliberately departs from the engine's verbatim stopping rule, does not relabel this run, and is not substituted for step 2 here. Source: docs/C10S_SOLVEFEAS_PREREG.md:25; docs/C10S_SHARED_Z_PREREG.md:22, :51.
```

**Recommendation:** record the qualified UNDERFIT-AT-50 finding and its unedited-model observations; continue to step 2 with the canonical target. Keep the fit-guarded stopping rule as a separately testable candidate. Do not advance the shared target or infer an F1 readiness change from the injection count.
