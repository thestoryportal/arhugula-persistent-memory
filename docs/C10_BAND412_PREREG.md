# C10 W-REALIZATION WIDENED-BAND [4,12] TEST - PRE-REGISTRATION

**Decision-ID:** `D-C10f-band412` · **Date:** 2026-06-26 · **Class:** FALSIFIER-resolver / recipe-knob characterization (can-fail; NOT promotable).  
**Parent:** `D-C10e-bandknob` (`CORPUS/37`) and `D-C10b-residual` (`CORPUS/36`). **Target:** fixed deployment path `local Intel CPU + batch writes`.  
**Scope:** Qwen2.5-3B / AlphaEdit harness / single-batch / capital-relation / NOVEL-insert / N=24 / 1-seed / HF-fp16.

## 0. Question

`CORPUS/36` found that realistic project-coined multi-word semantic values are fragile in-weight: A7 coined-coined values reached only **19.4%** held-out paraphrase full-sequence, with weak canonical fit. The z-probe ruled out `compute_z` target-achievability as the bottleneck (`z=0.99` reachable), relocating the failure to W-realization. `CORPUS/37` then tested a pure later-band shift `[8,12]`; A7 canonical fit improved only **29.2 -> 45.8**, while the binding held-out paraphrase full-sequence readout worsened **13.9 -> 5.6**.

This test asks the narrow follow-up: **does widening the existing MEMIT/AlphaEdit band to `[4,12]` materially improve the hard A7 held-out behavioral readout, without damaging the easy A1/A2 controls?**

## 1. Advisor Fix Incorporated

Advisor-review before authoring returned `FIX-FIRST`. Incorporated changes:

- `[4,12]` is a **wider recipe**, not an isolated mechanism claim. It changes layer coverage, layer count, and aggregate update opportunity.
- Held-out paraphrase `para_full` is the headline criterion. `canon_full` is a diagnostic only.
- A widened recipe that damages A1/A2 is a valid **tradeoff / not-clean-rescue**, not an invalid run.
- No result below **85%** A7 `para_full` can be called C10 closure. Positive results below that are leads only.
- A `[4,12]` failure does not prove AnyEdit necessary; it only says this remaining MEMIT band-widening knob did not rescue C10 under this harness.

## 2. Design

Run two recipes from the same base model and same stimuli:

1. **baseline:** `configs/hparams/qwen25_3b_memit_hparams.json`, layers `[4,5,6,7,8]`.
2. **wide-band:** `configs/hparams/qwen25_3b_memit_hparams_band412.json`, layers `[4,5,6,7,8,9,10,11,12]`.

Arms:

- **A1 single:** edit-success sanity control.
- **A2 coherent2:** multi-token positive control.
- **A7 coined-coined:** binding hard realistic treatment.

The runner reuses the C10e evaluator with env-selected hparams: `experiments/track_c/c10f_band412.py`. Output is namespaced to `results/c10f_band412.json`.

## 3. Metrics

Per recipe and arm:

- `canon_full`, `canon_first`
- `para_full`, `para_first`, `para_any_full`
- `P(full|first)`
- teacher-forced continuation per-token accuracy
- mean token length
- edit delta-norm per edited layer
- simple locality/collateral probe on edited subjects (`"{subject} is described as"`), reported as mean JS-locality vs pre-edit

## 4. Frozen Verdict Rules

Let `B` be baseline A7 and `K` be wide-band A7.

### Invalid

The run is **INVALID** if any of these fail:

- LAW#5 inertness fails for either recipe.
- Baseline A7 does not reproduce the failure envelope: `B.canon_full <= 55` and `B.para_full <= 35`.
- Baseline A1 or A2 has `para_full < 80`.

Wide-band A1/A2 below 80 is **not invalid**. It is a valid tradeoff / negative result.

### Outcome Bins

- **USABILITY RESCUE LEAD, NOT PROMOTED:** `K.para_full >= 85` and wide-band A1/A2 both `para_full >= 80`.  
  Licensed claim: widened recipe reaches the C10 usability bar in this scoped run. It still requires replication, quantization, and broader checks before C10 closure.

- **BEHAVIORAL LEAD, NOT CLOSURE:** `K.para_full - B.para_full >= 25` and `K.para_full >= 40`, with wide-band A1/A2 both `para_full >= 80`.  
  Licensed claim: widened recipe materially improves held-out read expression but remains below the 85% usability gate.

- **W-REALIZATION ONLY:** `K.canon_full - B.canon_full >= 20` and `K.para_full < 50`, with wide-band A1/A2 both `para_full >= 80`.  
  Licensed claim: widened recipe helps canonical fitting but does not solve held-out read expression.

- **TRADEOFF / NOT CLEAN RESCUE:** wide-band A1 or A2 has `para_full < 80`.  
  Licensed claim: the knob damages easy controls; any A7 gain is not a clean C10 rescue.

- **NO MATERIAL KNOB RESCUE:** `K.para_full - B.para_full < 15`, `K.para_full < 40`, and `K.canon_full < 80`.  
  Licensed claim: widened MEMIT band does not materially solve the C10 held-out read-expression failure.

- **MIXED / PARTIAL LEAD:** any other valid result.  
  Licensed claim: a recipe lead or tradeoff exists, but C10 remains open.

## 5. Scope

This is a single model, single seed, single hard realistic value class, and one widened-band comparison. It is not a deployment recipe change, not proof that AnyEdit is unnecessary, and not proof that AnyEdit is necessary if it fails. It decides only whether the remaining cheap MEMIT band-widening knob is worth following before a multi-day per-token editor port.

## 6. Reproduce

`LLMDB_ROOT=/workspace python3.11 experiments/track_c/c10f_band412.py`
