# C10 W-REALIZATION BAND-KNOB TEST — PRE-REGISTRATION

**Decision-ID:** `D-C10e-bandknob` · **Date:** 2026-06-26 · **Class:** FALSIFIER-resolver / recipe-knob characterization (can-fail; NOT promotable).  
**Parent:** `D-C10b-residual` (`CORPUS/36`). **Target:** fixed deployment path `local Intel CPU + batch writes`.  
**Scope:** Qwen2.5-3B / AlphaEdit harness / single-batch / capital-relation / NOVEL-insert / N=24 / 1-seed / HF-fp16.

## 0. Question

`CORPUS/36` found that realistic project-coined multi-word semantic values are fragile in-weight: A7 coined-coined values reached only **19.4%** held-out paraphrase full-sequence, with **37.5%** canonical full-sequence fit. The z-probe ruled out `compute_z` as the bottleneck (`z=0.99` achievable), relocating the failure to linear W-realization. The runbook's cheap resolver before AnyEdit is: **try a wider/later band or more layers and see whether canonical fit climbs.**

This test asks the narrow question: **does the existing later band `[8,12]` materially improve W-realization for the hard realistic A7 class, and does any fit gain translate into held-out behavioral read expression?**

## 1. Advisor Fix Incorporated

Advisor-review before authoring returned `FIX-FIRST`: do not let `canon_full` replace the actual behavioral-read criterion. Therefore this prereg uses two separate labels:

- **W-realization diagnostic:** `canon_full` on A7.
- **Behavioral-read / §8.9 usability readout:** held-out paraphrase `para_full` on A7.

A canonical-fit improvement is only a recipe lead unless `para_full` also clears a real usability bar. `para_full >= 50` is still below the prior 85% usability gate, so it is called **partial behavioral rescue**, not C10 closure.

## 2. Design

Run two recipes from the same base model and the same stimuli:

1. **baseline:** `configs/hparams/qwen25_3b_memit_hparams.json`, layers `[4,5,6,7,8]`.
2. **later-band:** `configs/hparams/qwen25_3b_memit_hparams_band812.json`, layers `[8,9,10,11,12]`.

Arms:

- **A1 single**: mandatory edit-success sanity control.
- **A2 coherent2**: mandatory multi-token positive control.
- **A7 coined-coined**: binding hard realistic treatment, same construction as `CORPUS/36`.

Each recipe runs its own LAW#5 inertness gate because the harness-side primitive is parameterized by the layer band. The output is namespaced to `results/c10e_bandknob.json`.

## 3. Metrics

Per recipe and arm:

- `canon_full`, `canon_first`
- `para_full`, `para_first`, `para_any_full`
- `P(full|first)`
- teacher-forced continuation per-token accuracy
- mean token length
- edit delta-norm per edited layer
- simple locality/collateral probes on edited subjects (`"{subject} is described as"`), reported as mean JS-locality vs pre-edit

The delta-norm/locality fields are safeguards against over-reading a later-band win. Prior C2-band evidence showed `[8,12]` can redistribute effects and carry collateral (`CORPUS/21`), so a positive result here is a recipe lead unless collateral is also acceptable and replicated.

## 4. Frozen Verdict Rules

Let `B` be baseline A7 and `K` be later-band A7.

### Sanity / Invalid

The run is **INVALID** if any of these fail:

- LAW#5 inertness fails for either recipe.
- Baseline A7 does not reproduce the failure envelope: `B.canon_full <= 55` and `B.para_full <= 35`.
- A1 single-token sanity has `para_full >= 80` under both recipes.
- A2 coherent2 positive control has `para_full >= 80` under both recipes.

### Outcome Bins

- **BEHAVIORAL KNOB RESCUE (partial, not closure):** `K.canon_full >= 80` and `K.para_full >= 50`.  
  Licensed claim: later band materially improves W-realization and produces partial behavioral-read rescue; AnyEdit is not the next mandatory step until this recipe lead is replicated and tested against the 85% gate.

- **W-REALIZATION ONLY:** `K.canon_full - B.canon_full >= 20` and `K.para_full < 50`.  
  Licensed claim: later band helps canonical fitting but does not solve held-out read expression; AnyEdit or another direct continuation objective remains justified.

- **NO MATERIAL KNOB RESCUE:** `(K.canon_full - B.canon_full < 20 and K.para_full - B.para_full < 15) or K.canon_full < 60`.  
  Licensed claim: this cheap later-band knob does not materially solve W-realization; AnyEdit remains mechanistically justified, though not proven necessary.

- **MIXED / PARTIAL LEAD:** any other valid result.  
  Licensed claim: a recipe lead or tradeoff exists, but C10 remains open; do not upgrade the architecture or port decision without a follow-up falsifier.

### Collateral Caveat

If A1/A2 pass but later-band collateral/locality is materially worse than baseline, the result must be labeled as a **tradeoff**, not a clean rescue, even if A7 improves.

## 5. Scope

This is a single model, single seed, single hard realistic value class, and one band comparison. It is not a deployment recipe change, not a proof that AnyEdit is unnecessary, and not a C10 close-out. It can only decide whether the cheap `[8,12]` band knob is worth following before a multi-day AnyEdit port.
