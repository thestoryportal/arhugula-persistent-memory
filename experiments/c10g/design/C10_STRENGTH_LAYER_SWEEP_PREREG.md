# C10 EDIT-STRENGTH / LAYER-COUNT SWEEP - PRE-REGISTRATION

**Decision-ID:** `D-C10g-strengthlayers` · **Date:** 2026-06-26 · **Class:** FALSIFIER-resolver / bounded MEMIT-knob characterization (can-fail; NOT promotable).
**Parent:** `D-C10b-residual` (`CORPUS/36`), `D-C10e-bandknob` (`CORPUS/37`), and `D-C10f-band412` (`CORPUS/38`). **Target:** fixed deployment path `local Intel CPU + batch writes`.
**Scope:** Qwen2.5-3B / AlphaEdit-MEMIT harness / single-batch / capital-relation / NOVEL-insert / N=24 / 1-seed / HF-fp16.

## 0. Question

C10 found that the tested in-weight path expresses simple single-token and prior-coherent multi-token values robustly, but fails realistic project-coined multi-word semantic values. CORPUS/36 localized the realistic failure away from `compute_z` target-achievability: `z=0.99` is reachable, so the open bottleneck is W-realization. CORPUS/37 and CORPUS/38 then tested two band knobs, later `[8,12]` and widened `[4,12]`; both failed to rescue the hard A7 coined-coined value class.

This test asks the remaining cheap MEMIT-family question before an AnyEdit port: **does a tiny pre-registered edit-strength / layer-count sweep materially rescue A7 held-out behavioral readout while preserving A1/A2 controls?**

This is not an optimizer. It is the final bounded MEMIT-knob pass before the fork narrows to AnyEdit vs. accept-as-bounded, unless a candidate crosses a behavioral lead threshold below.

## 1. Advisor Fixes Incorporated

Advisor-review before authoring returned `FIX-FIRST`. Incorporated changes:

- Held-out paraphrase full-sequence `para_full` is the only rescue/lead metric.
- `canon_full` is diagnostic only. Canonical-only gains are explicitly **non-rescue** and do not license postponing AnyEdit by themselves.
- `MIXED` cannot become an interpretive success bucket. Anything below the behavioral thresholds is non-promotional.
- Exact hit counts must be reported with percentages because N=24 and three paraphrases means one held-out paraphrase item is 1/72 = 1.39pp; one subject canonical item is 1/24 = 4.17pp.
- Candidate A1/A2 control damage is not invalid, but it is evidence for over-editing/tradeoff, not a clean rescue.
- Stopping rule: after these three pre-registered candidates, move to AnyEdit or accept-bounded unless a candidate reaches `USABILITY_RESCUE_LEAD` or `BEHAVIORAL_LEAD`.

## 2. Design

Run one baseline and three candidates from the same base model and same stimuli, reusing the vetted C10e evaluator (`experiments/track_c/c10e_bandknob.py`):

0. **baseline:** `configs/hparams/qwen25_3b_memit_hparams.json`, layers `[4,5,6,7,8]`, `clamp_norm_factor=0.75`, `mom2_update_weight=5000`.
1. **wide_band412_strength150:** `configs/hparams/qwen25_3b_memit_hparams_band412_strength150.json`, layers `[4..12]`, `clamp_norm_factor=1.50`, `mom2_update_weight=5000`. Tests whether the C10f recipe under-drove the target vector through too-tight clamp.
2. **wide_band412_lowcov2500:** `configs/hparams/qwen25_3b_memit_hparams_band412_lowcov2500.json`, layers `[4..12]`, `clamp_norm_factor=0.75`, `mom2_update_weight=2500`. Tests whether the W-solve was over-regularized by the covariance term.
3. **deep_band41218:** `configs/hparams/qwen25_3b_memit_hparams_band41218.json`, layers `[4..12,18..22]`, `clamp_norm_factor=0.75`, `mom2_update_weight=5000`. Tests layer-count/depth extension using already cached covariance layers; this is least diagnostic because it changes depth and layer count together, so it runs last.

Arms:

- **A1 single:** edit-success sanity control.
- **A2 coherent2:** prior-coherent multi-token positive control.
- **A7 coined-coined:** binding hard realistic treatment.

Run command:

`LLMDB_ROOT=/workspace python3.11 experiments/track_c/c10g_strength_layer_sweep.py`

Output:

`results/c10g_strength_layer_sweep.json`

## 3. Metrics

Per recipe and arm:

- `canon_full`, `canon_first`
- `para_full`, `para_first`, `para_any_full`
- exact counts: `canon_full_hits/24`, `para_full_hits/72`, `para_first_hits/72`
- `P(full|first)`
- teacher-forced continuation per-token accuracy
- mean token length
- edit delta-norm per edited layer
- simple locality/collateral probe on edited subjects (`"{subject} is described as"`), reported as mean JS-locality vs pre-edit

## 4. Frozen Validity Rules

The run is **INVALID** if any of these fail:

- LAW#5 inertness fails for baseline or all candidates.
- Baseline A7 does not reproduce the failure envelope: `baseline_A7.canon_full <= 55` and `baseline_A7.para_full <= 35`.
- Baseline A1 or A2 has `para_full < 80`.

Candidate A1/A2 below 80 is **not invalid**. It is a valid tradeoff / over-editing result and not a clean C10 rescue.

## 5. Frozen Outcome Rules

Let `B` be baseline A7. For each candidate `K`, compute:

- `delta_para = K.para_full - B.para_full`
- `delta_canon = K.canon_full - B.canon_full`
- `control_min = min(K.A1.para_full, K.A2.para_full)`

Candidate-level bins:

- **USABILITY_RESCUE_LEAD_NOT_PROMOTED:** `K.A7.para_full >= 85` and `control_min >= 80`.
- **BEHAVIORAL_LEAD_NOT_CLOSURE:** `delta_para >= 25` and `K.A7.para_full >= 40` and `control_min >= 80`.
- **TRADEOFF_NOT_CLEAN_RESCUE:** `control_min < 80`. Licensed claim: the knob damages easy controls; any A7 gain is not a clean C10 rescue and may be over-editing.
- **W_REALIZATION_ONLY_NON_RESCUE:** `delta_canon >= 20` and `K.A7.para_full < 40` and `control_min >= 80`. Licensed claim: canonical trained-prompt fitting improved, but the behavioral read criterion remains unusable; this is mechanism evidence only.
- **NO_MATERIAL_BEHAVIORAL_RESCUE:** `delta_para < 15` and `K.A7.para_full < 40` and `control_min >= 80`, regardless of small/moderate `canon_full` movement.
- **AMBIGUOUS_NONPROMOTIONAL:** any other valid candidate. Licensed claim: scoped signal is ambiguous and does not move C10 toward closure without replication.

Sweep-level bins:

- **USABILITY_RESCUE_LEAD_NOT_PROMOTED:** any candidate reaches the candidate-level usability bin.
- **BEHAVIORAL_LEAD_NOT_CLOSURE:** otherwise, any candidate reaches the candidate-level behavioral lead bin.
- **TRADEOFF_NOT_CLEAN_RESCUE:** otherwise, the best A7 behavioral gain comes from a tradeoff candidate.
- **W_REALIZATION_ONLY_NON_RESCUE:** otherwise, at least one candidate is canonical-only W-realization evidence.
- **NO_MATERIAL_KNOB_RESCUE:** otherwise, all valid candidates are no-material behavioral rescues.
- **MIXED_NONPROMOTIONAL:** otherwise.

No result below `A7 para_full >= 85` can be called C10 closure. No canonical-only result can be called a behavioral lead.

## 6. Licensed Claims

If negative, this test rules out only this small pre-registered MEMIT strength/layer-count sweep on Qwen2.5-3B / A7 / N=24 / 1-seed. It does **not** prove AnyEdit necessary, does **not** prove MEMIT capacity universally fails, and does **not** update the deployment recipe.

If positive, it is a lead only. It requires replication, Q4_K_M survival, and broader value-class checks before C10 closure.
