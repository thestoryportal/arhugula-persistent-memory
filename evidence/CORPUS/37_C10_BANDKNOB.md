# CORPUS/37 - C10 W-realization band-knob: later [8,12] does not rescue hard coined values

**Decision-ID:** `D-C10e-bandknob`. ⟨D-C10e-bandknob@82b491dc⟩ **Date:** 2026-06-26. **Pre-reg:** `docs/C10_BANDKNOB_PREREG.md` (frozen before run; advisor-revised before build). **Runner:** `experiments/track_c/c10e_bandknob.py`. **Result:** `results/c10e_bandknob.json`. **Parent:** `D-C10b-residual` (CORPUS/36).
**E2e-map cell:** §8.9 L2 behavioral firing/read expression for Layer-4 `domain_concept`; F1 condition **C10**; fixed deployment target = `local Intel CPU + batch writes`. **Class:** **KNOB FALSIFIER / CHARACTERIZATION.** NOT promotable (3B / N=24 / 1-seed / one hard value class).
**Verdict: NO MATERIAL KNOB RESCUE.** Moving the edit band from baseline `[4,8]` to later `[8,12]` does **not** rescue the hard realistic coined-coined value class. The later band modestly improves canonical trained-prompt full-sequence fit (`29.2 to 45.8`, +16.6pp) but still misses the pre-registered diagnostic threshold and remains below 60%; the binding behavioral read metric **worsens** (`para_full 13.9 to 5.6`, -8.3pp). C10 remains open; pure later-band W-realization is not enough.

## The question
CORPUS/36 localized the realistic coined-value failure away from `compute_z`: the z target is achievable at 0.99, so the remaining bottleneck was the linear W-edit realizing a long multi-token continuation. The cheapest falsifier before a multi-day AnyEdit port was: **does a later band already fix W-realization for the hard A7 coined-coined arm?**

## Design
Same 24 fictional subjects and A7 coined-coined values as CORPUS/36; relation = capital; binding metric = held-out-paraphrase **full-sequence** exact match across three paraphrases. Two hparam recipes:

- baseline: `configs/hparams/qwen25_3b_memit_hparams.json`, layers `[4,5,6,7,8]`
- later band: `configs/hparams/qwen25_3b_memit_hparams_band812.json`, layers `[8,9,10,11,12]`

Controls were re-run in the same harness: A1 single-token and A2 coherent two-token values. LAW#5 inertness passed for both recipes: baseline `|delta_expr|=0.0011`, `|delta_loc|=0.09`; later `[8,12]` `|delta_expr|=0.0000`, `|delta_loc|=2.19`.

## Result table
| recipe | arm | canon_full | **para_full** | para_first | P(full\|first) | tf_pertok_cont | locality |
|---|---|---:|---:|---:|---:|---:|---:|
| baseline [4,8] | A1 single | 100.0 | **97.2** | 97.2 | 1.000 | - | 91.07 |
| baseline [4,8] | A2 coherent2 | 100.0 | **97.2** | 97.2 | 1.000 | 100.0 | 93.05 |
| baseline [4,8] | A7 coined-coined | 29.2 | **13.9** | 75.0 | 0.185 | 60.2 | 89.26 |
| later [8,12] | A1 single | 100.0 | **97.2** | 97.2 | 1.000 | - | 92.22 |
| later [8,12] | A2 coherent2 | 100.0 | **91.7** | 91.7 | 1.000 | 100.0 | 93.29 |
| later [8,12] | A7 coined-coined | 45.8 | **5.6** | 33.3 | 0.167 | 34.0 | 93.74 |

**Frozen label:** `NO_MATERIAL_KNOB_RESCUE`.

Delta for A7: `canon_full +16.6pp`, `para_full -8.3pp`, `para_first -41.7pp`, `tf_pertok_cont -26.2pp`.

## What the verdict licenses
**EVIDENCE-SHOWS:** a pure later-band shift to `[8,12]` is insufficient for the hard long no-prior coined-coined value class. The binding §8.9 behavioral-read metric is `para_full`, and it gets worse. The canonical trained-prompt gain is a diagnostic only; it does not establish usable storage/readout.

**EVIDENCE-SHOWS:** the failure is specific within the tested arms to the hard no-prior coined-coined class. Under the later band, A1 and A2 remain high (`para_full` 97.2 and 91.7), while A7 is 5.6.

**I-INFER:** later layers may partially fit the trained canonical prompt without improving paraphrase portability or continuation transfer. The A7 `para_first` and teacher-forced continuation drops suggest the later band is worse at carrying the first-token edit into a usable multi-token sequence under paraphrase.

**I-INFER:** delta-norms are mechanism clues, not storage evidence. A7 relative update norms rise into later layers (`L8=0.104`, `L9=0.131`, `L10=0.176`, `L11=0.252`, `L12=0.336`) while the behavioral read worsens. That is consistent with a depth/realization tradeoff, not a rescue.

## Severity / F1 impact
C10 remains **OPEN / CONDITIONAL** and F1 readiness is **UNCHANGED**. CORPUS/36 showed realistic project-coined multi-word semantic values are fragile at baseline `[4,8]`; this result eliminates one cheap W-realization explanation, **not** the broader class of W-realization remedies. AnyEdit remains mechanistically consistent, but not proven necessary. Broader knobs still untested: widened `[4,12]`, more layers, edit-strength, and per-token editors.

## Scope / honesty
3B / AlphaEdit / N=24 / one seed / fictional subjects / hard A7 coined-coined values / HF-fp16. This is a within-run band comparison, not a universal layer claim. Baseline A7 here (`para_full 13.9`, `canon_full 29.2`) is lower than CORPUS/36's A7 (`19.4`, `37.5`) but within the pre-registered failure envelope, so the within-run comparison is valid while not an exact replication of CORPUS/36. Locality is a narrow single-prompt collateral probe; A7 locality did not worsen (`89.26 to 93.74`), so locality does not explain the failure. No Q4_K_M quantization check; no wider/strength sweep; no AnyEdit port; no model-size transfer.

## Fork
If continuing C10 before AnyEdit, the cheapest broader overturning test is a single A7 rerun with widened `[4,12]` or an edit-strength/layer-count knob. If the operator chooses to skip more knobs, the next target-facing test is Q4_K_M survival of multi-token values; B3 only covered single-token batch-clean values.

## Reproduce
`LLMDB_ROOT=/workspace python3.11 experiments/track_c/c10e_bandknob.py` writes `results/c10e_bandknob.json`.
