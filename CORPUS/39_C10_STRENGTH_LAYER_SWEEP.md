# CORPUS/39 - C10 edit-strength/layer-count sweep: no behavioral rescue, one non-viable tradeoff

**Decision-ID:** `D-C10g-strengthlayers` ⟨D-C10g-strengthlayers@d691acab⟩. **Date:** 2026-06-26. **Pre-reg:** `docs/C10_STRENGTH_LAYER_SWEEP_PREREG.md` (frozen before run; advisor-revised before build). **Runner:** `experiments/track_c/c10g_strength_layer_sweep.py` (wraps `c10e_bandknob.py`). **Result:** `results/c10g_strength_layer_sweep.json`. **Parents:** `D-C10b-residual` (CORPUS/36), `D-C10e-bandknob` ⟨D-C10e-bandknob@82b491dc⟩ (CORPUS/37), and `D-C10f-band412` ⟨D-C10f-band412@d93d6a19⟩ (CORPUS/38).
**E2e-map cell:** §8.9 L2 behavioral firing/read expression for Layer-4 `domain_concept`; F1 condition **C10**; fixed deployment target = `local Intel CPU + batch writes`. **Class:** **BOUNDED MEMIT-KNOB FALSIFIER / CHARACTERIZATION.** NOT promotable (3B / N=24 / 1-seed / one hard value class).
**Verdict: NO BEHAVIORAL RESCUE WITH ONE NON-VIABLE TRADEOFF.** The three pre-registered MEMIT strength/layer-count candidates do **not** rescue the hard A7 project-coined value class. The binding held-out behavioral read metric is `para_full`; it worsens for every candidate: baseline **20.8% (15/72)** → strength150 **13.9% (10/72)**, lowcov2500 **5.6% (4/72)**, deep-band **0.0% (0/72)**. The deep recipe improves canonical trained-prompt fit (**29.2% to 58.3%**) but collapses A1/A2 controls (**37.5% / 22.2%**) and is not a viable rescue. C10 remains open; this closes the pre-AnyEdit bounded MEMIT knob pass, not MEMIT in general.

## The question
CORPUS/36 localized the realistic coined-value failure away from `compute_z`: the z target is achievable at 0.99, so the remaining bottleneck was W-realization. CORPUS/37 and CORPUS/38 tested two band knobs, later `[8,12]` and widened `[4,12]`, and neither rescued the hard A7 class. This test asks the remaining cheap MEMIT-family question before AnyEdit: **does a tiny pre-registered edit-strength / layer-count sweep materially rescue A7 held-out behavioral readout while preserving A1/A2 controls?**

Advisor-review before authoring returned `FIX-FIRST`; the preregistration made `para_full` the only rescue/lead metric, made canonical-only gains diagnostic only, required exact counts, and declared the stopping rule: after these three candidates, move to AnyEdit or accept-bounded unless a candidate reaches a behavioral lead threshold.

## Design
Same 24 fictional subjects, A1/A2/A7 arms, and held-out paraphrase probes as the C10e/C10f evaluator; relation = capital; binding metric = held-out-paraphrase **full-sequence** exact match across three paraphrases (`72` held-out trials for A7). Recipes:

- baseline `[4,8]`: `configs/hparams/qwen25_3b_memit_hparams.json`
- strength150 `[4,12]`: `configs/hparams/qwen25_3b_memit_hparams_band412_strength150.json`, `clamp_norm_factor=1.50`
- lowcov2500 `[4,12]`: `configs/hparams/qwen25_3b_memit_hparams_band412_lowcov2500.json`, `mom2_update_weight=2500`
- deep `[4..12,18..22]`: `configs/hparams/qwen25_3b_memit_hparams_band41218.json`

LAW#5 inertness passed for every recipe: baseline `|delta_expr|=0.0023`, `|delta_loc|=0.14`; strength150 `0.0002`, `0.00`; lowcov2500 `0.0008`, `0.39`; deep `0.0021`, `0.30`.

## Result table
| recipe | A1 para_full | A2 para_full | A7 canon_full | **A7 para_full** | A7 para_first | A7 tf_cont | verdict role |
|---|---:|---:|---:|---:|---:|---:|---|
| baseline `[4,8]` | 97.2 (70/72) | 100.0 (72/72) | 29.2 (7/24) | **20.8 (15/72)** | 77.8 (56/72) | 61.4 | valid failure envelope |
| strength150 `[4,12]` | 98.6 (71/72) | 100.0 (72/72) | 29.2 (7/24) | **13.9 (10/72)** | 80.6 (58/72) | 59.9 | no material behavioral rescue |
| lowcov2500 `[4,12]` | 94.4 (68/72) | 98.6 (71/72) | 45.8 (11/24) | **5.6 (4/72)** | 31.9 (23/72) | 40.7 | no material behavioral rescue; canonical diagnostic only |
| deep `[4..12,18..22]` | 37.5 (27/72) | 22.2 (16/72) | 58.3 (14/24) | **0.0 (0/72)** | 8.3 (6/72) | 6.5 | non-viable tradeoff / over-editing |

**Frozen wrapper label:** `MIXED_NONPROMOTIONAL` = mixed recipe outcomes, uniformly non-promotional on the binding behavioral criterion. The CORPUS headline is therefore the clearer advisor-recommended reading: **NO BEHAVIORAL RESCUE WITH ONE NON-VIABLE TRADEOFF.**

## What the verdict licenses
**EVIDENCE-SHOWS:** the run is valid under the preregistration. LAW#5 passes for all recipes; baseline A1/A2 controls pass (`97.2`, `100.0`); baseline A7 reproduces the failure envelope (`canon_full 29.2`, `para_full 20.8`).

**EVIDENCE-SHOWS:** neither strength-style `[4,12]` candidate rescues the binding behavioral readout. Strength150 keeps controls clean but worsens A7 `para_full` from `15/72` to `10/72`. Lowcov2500 keeps controls clean but worsens A7 `para_full` to `4/72`; its canonical fit gain (`7/24` to `11/24`, +16.6pp) is below the preregistered W-realization-only threshold and moves opposite the behavioral criterion.

**EVIDENCE-SHOWS:** the deep layer-count extension is not a viable rescue. It improves canonical trained-prompt fit (`7/24` to `14/24`) but collapses controls (`A1 27/72`, `A2 16/72`) and collapses A7 held-out behavior (`0/72`). This is valid evidence of a non-clean tradeoff / over-editing recipe, not rescue evidence.

**I-INFER:** after two band-placement failures (CORPUS/37-38) and this bounded strength/layer-count sweep, the cheap MEMIT-knob route has no current behavioral rescue lead for A7. The remaining practical C10 fork is AnyEdit/per-token editing versus accepting bounded viability for single-token/prior-coherent in-weight values.

**I-INFER:** this does not prove AnyEdit necessary. It does not prove MEMIT capacity universally fails. It says only that these three pre-registered MEMIT knob variants fail under Qwen2.5-3B / A7 / N=24 / 1-seed.

## Severity / F1 impact
C10 remains **OPEN / CONDITIONAL** and F1 readiness is **UNCHANGED**. The result narrows the C10 fork: no tested cheap MEMIT band/strength/layer-count knob has produced a behavioral rescue for hard project-coined multi-word values. Under the preregistered stopping rule, further progress should be AnyEdit/per-token editing or an operator decision to accept the limitation, unless a genuinely new MEMIT hypothesis is separately justified and pre-registered.

## Scope / honesty
Qwen2.5-3B / AlphaEdit-MEMIT / N=24 subjects / 72 held-out A7 paraphrase trials / one seed / fictional subjects / hard A7 coined-coined values / HF-fp16 / these three hparam variants. No Q4_K_M quantization check; no model-size transfer; no broader value-class replication; no AnyEdit port. Candidate 3 is a valid run but a non-viable intervention because controls collapse. Keep this scope flush: this is not a universal MEMIT exhaustion claim.

## Fork
Cheapest overturning test if someone disputes the interpretation: rerun only the best diagnostic variant, `wide_band412_lowcov2500`, on a second seed or slightly larger N and require A7 `para_full` to exceed baseline by the preregistered behavioral-lead threshold while A1/A2 remain clean. Given the observed `4/72` vs baseline `15/72`, the burden is high. The main forward option remains AnyEdit/per-token editing, or accept bounded viability for CORE in-weight values only if they are single-token / prior-coherent.

## Reproduce
`LLMDB_ROOT=/workspace python3.11 experiments/track_c/c10g_strength_layer_sweep.py` writes `results/c10g_strength_layer_sweep.json`.
