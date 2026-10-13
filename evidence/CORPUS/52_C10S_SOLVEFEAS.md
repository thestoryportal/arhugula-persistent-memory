# 52 — Shared-target solve feasibility: UNDERFIT-AT-50, objective-stopped — added evaluations repair most same-run fit failures, but the frozen per-frame gate still fails; the write arm did not run

_Result 2026-10-07 UTC. Decision-ID D-C10s-solvefeas. ⟨D-C10s-solvefeas@7083a102⟩ Operator ruling D-C10r-rulings-7 (2); overnight standing approval D-C10r-rulings-8. Pre-registration docs/C10S_SOLVEFEAS_PREREG.md v2, inheriting docs/C10S_SHARED_Z_PREREG.md v3 + A1 + A2 v2. Source commit 400f051; all 14 declared hashes verified against that commit and the reviewed source files. Binding records results/c10s_solvefeas/{inertness,run,inject}.json; logs results/c10s_solvefeas_logs/{inertness,arms_first}.log. Run 2026-10-07T053918Z-943c2b98e2f2, bound to complete ALL-INERT record 2026-10-07T053019Z-943c2b98e2f2. Engine unmodified, fingerprint d941a9fb/PASS. Verdict review: results/c10s_solvefeas_codex_verdict.md. Lineage: CORPUS/51, CORPUS/46 F-D1._

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

_Text proposed by the Codex verdict review (`results/c10s_solvefeas_codex_verdict.md` §5) and adopted by the program session._
