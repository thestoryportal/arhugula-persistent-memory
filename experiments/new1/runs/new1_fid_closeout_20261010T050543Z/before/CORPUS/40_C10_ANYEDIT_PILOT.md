# CORPUS/40 - C10 AnyEdit small-window pilot: local window_size=1 transplant collapses controls

**Decision-ID:** `D-C10h-anyedit-pilot`. **Date:** 2026-06-27. **Pre-reg:** `docs/C10_ANYEDIT_PILOT_PREREG.md` (frozen after advisor FIX-FIRST; alignment gate embedded before GPU run). **Runner:** `experiments/track_c/c10h_anyedit_pilot.py`. **Result:** `results/c10h_anyedit_pilot.json`. **Parents:** `D-C10-1`, `D-C10b-residual`, `D-C10e-bandknob`, `D-C10f-band412`, and `D-C10g-strengthlayers`.
**E2e-map cell:** section 8.9 L2 behavioral firing/read expression for Layer-4 `domain_concept`; F1 condition **C10**; fixed deployment target = `local Intel CPU + batch writes`. **Class:** **ANYEDIT FEASIBILITY PILOT / SCOPED RESOLVER.** NOT promotable beyond this harness-side fixed small-window transplant.
**Verdict: TRADEOFF_NOT_CLEAN_RESCUE.** The local AnyEdit-style autoregressive target/window transplant with `window_size=1` is **not** a clean C10 rescue. It passes the embedded alignment/no-op gates, but it collapses A1/A2 held-out behavior and worsens the hard A7 project-coined value class. Baseline A7 `para_full` is **12.5% (9/72)**; AnyEdit-window1 A7 `para_full` is **1.4% (1/72)**. More importantly, A1/A2 controls fall from **93.1% / 97.2%** to **0.0% / 0.0%**. C10 remains open; this result does not falsify the AnyEdit family or upstream AnyEdit.

## The question
CORPUS/35-39 established that project-coined multi-word values are the live C10 blocker for the fixed deployment target and that cheap MEMIT band/strength/layer-count knobs do not rescue held-out behavior. The next proposed rescue was AnyEdit/per-token autoregressive editing. This pilot asks the smallest falsifiable version: **does a local AnyEdit-style small-window target construction rescue hard A7 held-out behavior while preserving A1/A2 controls?**

Advisor-review before authoring returned FIX-FIRST. The preregistration therefore made token/window alignment a hard pre-run gate, froze the same-run baseline comparator (`configs/hparams/qwen25_3b_memit_hparams.json`, layers `[4,5,6,7,8]`), required no-op inertness before trusting evidence, and required A1/A2 controls to remain clean before interpreting any A7 gain.

## Design
Same 24 fictional subjects and capital relation as the C10e-g harness family. Arms:

- A1 single-token known capitals.
- A2 prior-coherent two-token capitals.
- A7 project-coined/coined multi-token values.

Binding metric is held-out paraphrase **full-sequence** exact match across three paraphrases (`72` trials per arm). The AnyEdit pilot keeps local MEMIT/AlphaEdit primitives and changes only harness-side target/window construction: an AnyEdit ARE-style autoregressive target sequence with `window_size=1`.

Alignment gates:

- Dry-run token/window gate passed before GPU evidence: A1 token length `1/1/1`, A2 `2/2/2`, A7 range `4-6`, mean `5.5`.
- Baseline LAW#5 passed: `expr_delta=0.0001`, `loc_delta=1.82`.
- AnyEdit no-op gate passed: `expr_delta=0.0`, `loc_delta=0.0`, `param_max_abs_delta=0.0`, `token_plan_ok=True`.
- AnyEdit token/window gates passed for A1, A2, and A7.

## Result table
| recipe | A1 para_full | A2 para_full | A7 canon_full | **A7 para_full** | A7 para_first | A7 tf_cont | locality | verdict role |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| baseline `[4,8]` | 93.1 (67/72) | 97.2 (70/72) | 33.3 (8/24) | **12.5 (9/72)** | 79.2 (57/72) | 56.8 | 89.94 | valid failure envelope |
| AnyEdit window1 | 0.0 (0/72) | 0.0 (0/72) | 8.3 (2/24) | **1.4 (1/72)** | 2.8 (2/72) | 65.1 | 97.62 | non-clean control collapse |

Additional control details: A1 canonical falls from `100.0 (24/24)` to `25.0 (6/24)`; A2 canonical falls from `100.0 (24/24)` to `4.2 (1/24)`. AnyEdit A7 `para_any_full` is `4.2 (3/72)` versus baseline `29.2 (21/72)`. The frozen script verdict is `TRADEOFF_NOT_CLEAN_RESCUE`, with A7 `para_full` delta `-11.1pp` and `control_min_para_full=0.0`.

## What the verdict licenses
**EVIDENCE-SHOWS:** under the pre-registered C10h harness, the tested local AnyEdit small-window transplant is not a clean rescue. It passes alignment and no-op gates, but it worsens A7 held-out behavior and collapses A1/A2 controls.

**EVIDENCE-SHOWS:** the dominant empirical result is a control-path failure, not a selective hard-value rescue/failure. A1/A2 are easy for the same-run baseline (`93.1%`, `97.2%`) and fail under AnyEdit-window1 (`0.0%`, `0.0%`), so the A7 degradation is not interpretable as an isolated property of hard coined-coined values.

**I-INFER:** this small-window transplant likely mis-specifies some dependency/window behavior needed for normal edit expression. That mechanism is not proven by this run; the result only warrants the narrower claim that this fixed `window_size=1` local transplant is not viable as tested.

**I-INFER:** upstream AnyEdit, AnyEdit++, muKE, or a dependency-aware/default-window condition remain un-falsified. The cheapest overturning diagnostic is an A1/A2-only run with `window_size=50` or an upstream-equivalent dependency/window condition; require A1/A2 `para_full >= 80%` before spending GPU on A7.

## Severity / F1 impact
C10 remains **OPEN / CONDITIONAL** and F1 readiness is **UNCHANGED**. The result kills the immediate local small-window AnyEdit rescue attempt, but it does not close the AnyEdit family fork. The forward choice is now either a narrow upstream-equivalent A1/A2 diagnostic, or accept the current bounded architecture with project-coined multi-word semantic values routed through a side-store/index path.

## Scope / honesty
Qwen2.5-3B / AlphaEdit-MEMIT primitives / local AnyEdit-style ARE target construction / `window_size=1` / N=24 / one seed / fictional subjects / capital relation / HF-fp16 / no Q4_K_M survival check / no upstream AnyEdit code execution. This is not a universal AnyEdit failure and not evidence that per-token methods cannot rescue C10.

## Fork
If continuing the AnyEdit route: run the advisor-recommended A1/A2-only dependency/window diagnostic (`window_size=50` or upstream-equivalent behavior). Only if controls recover to at least `80%` held-out `para_full`, run A7. If controls remain collapsed, route project-coined multi-word values through the external index/side-store path and mark in-weight C10 as bounded.

## Reproduce
`LLMDB_ROOT=/workspace python3 experiments/track_c/c10h_anyedit_pilot.py --dry-run` writes `results/c10h_anyedit_token_window_dryrun.json`.

`LLMDB_ROOT=/workspace python3 experiments/track_c/c10h_anyedit_pilot.py` writes `results/c10h_anyedit_pilot.json` and logs to `logs/c10h_anyedit_pilot.log`.

⟨D-C10h-anyedit-pilot@6413cc67⟩

⟨D-C10e-bandknob@82b491dc D-C10f-band412@d93d6a19 D-C10g-strengthlayers@d691acab⟩
