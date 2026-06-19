# 14 — A1 BATCH vs SEQUENTIAL (the Genesis-path locality test)

_Result 2026-06-18. Track-A follow-up to the G6.1 falsifier (`CORPUS/13`). Pre-registered in `EXPERIMENT_RUNBOOK.md` §8 A1. Artifacts: `g6_scale_n.py` (harness, `WRITE_MODE=batch` / `batch_staircase`), `g6_scale_n_batch_result.json` (N=100 single point), `g6_scale_n_batch_staircase_result.json` (N=26/50/100 staircase), `a1_batch.log` + `a1_batch_staircase.log` (run logs). Engine UNMODIFIED; LAW#5 inertness gate passed both runs (|Δexpr|=0.0026 / 0.0045)._

## The question (why this is mandatory, not optional)
G6.1 falsified "cross-entity-clean at scale" using **sequential** writes (one record at a time, `cache_c` accumulating). But the spec's foundational write — **Project Genesis (§7.7)** — is an **atomic BATCH** (single 2PC across L1–L4). We had only ever tested the runtime-incremental pattern. A1 asks: does applying N shared-relation edits in ONE joint solve (batch) change the cross-entity read corruption vs one-at-a-time (sequential)? Cheapest informative experiment in the queue (a one-line mode flag), advisor-flagged.

## Pre-registration (set BEFORE the run, `EXPERIMENT_RUNBOOK.md` §8 A1)
- **Metric:** held-out (never-edited) edited-relation **top-1 correctness** at N=100, same 6 held-out entities / 12 probes / fixed disjoint pool as G6.1.
- **PASS** = batch held-out top-1 **≥ 80%** (vs seq 41.7%). **PARTIAL** = 50–80%. **FAIL** = ≤50% (batch ≈ sequential → confirms MEMIT `E_mix`; batch alone not the lever).
- **Prediction (registered):** likely **PARTIAL/FAIL** — theory said a same-relation batch concentrates the shared `k_r` and could be *more* rank-deficient (Perplexity); MEMIT's own `E_mix` predicts ≈average. **The result contradicts this prediction** — which is exactly why it got the extra scrutiny below (a surprise PASS earns more checking than a confirming one).

## VERDICT — PASS (robust): batch ELIMINATES the cross-entity corruption within the tested range (N≤100)

A single PASS point can't distinguish "eliminates" from "defers" (advisor-caught: G6.1 was a *scaling* claim; one point is not a curve). So the headline rides on **batch's own staircase** vs sequential's:

| held-out **edited-relation top-1 correct** | baseline | N=26 | N=50 | N=100 |
|---|---|---|---|---|
| **A0 sequential** (G6.1) | 100% | 91.7% | 58.3% | **41.7%** |
| **A1 batch** (this) | 100% | **100%** | **100%** | **100%** |

Supporting metrics (batch staircase; sequential in parens):

| Metric @ N | N=26 | N=50 | N=100 |
|---|---|---|---|
| held-out edited-rel top-1 **stable** (vs pre) | 100% | 100% | 100% |
| held-out **continent** (unedited rel) stable | 100% | 100% | 100% |
| cross-entity JS-locality | 99.7% (86.1) | 99.2% (66.7) | **97.9% (54.4)** |
| all-record retention | 100% | 100% | 100% (98) |
| apply-time expression | 100% | 100% | 100% |
| within-entity JS-locality | 99.3% (99.8) | 96.1% (99.6) | **90.5% (95.6)** |
| global JS-locality (non-country) | 99.5% | 98.5% | 96.6% (98.4) |

- **Flat at 100%** across the full staircase → batch *eliminates* (not merely defers) the cross-entity read corruption within N≤100. Sequential collapsed 100→92→58→42%; batch holds 100→100→100%.
- **Replicates:** two independent batch N=100 joint solves (the standalone `batch` run and the `batch_staircase` final rung) both give held-out edited-rel top-1 = **100%**, cross-JS 97.7%/97.9%, retention 99%/100% — agreement well inside FP/ordering noise.
- **Continent control:** stable 100% throughout (relation-specific story preserved; the 33.3% "correct" is the model's weak baseline knowledge of these held-out continents, NOT corruption — it is 100% *stable* vs pre).

## Mechanism (why batch is clean where sequential corrupts)
G6.1's corruption was **cumulative pseudo-null / `cache_c` leakage** (BetaEdit mechanism, `cross_entity_research_synthesis.md`): each sequential edit adds a residual that rides the shared high-variance relation direction, and these accumulate across the N solves. A **single joint solve resolves all N constraints simultaneously against one null-space projection** — MEMIT's "conflicts resolved mathematically" — so there is no accumulation term to leak into un-edited same-relation entities. The corruption was therefore an artifact of the **incremental schedule**, not of in-weight storage per se. This refines G6.1: the in-weight store is **not** inherently cross-entity-dirty at scale; the *runtime-incremental* write path is.

## What this resolves, and what it does NOT
- **RESOLVES (Genesis path):** a batched foundational write (§7.7) is **locality-safe at N≤100** on this model/recipe. Genesis gains a positive locality argument for batching. The spec's drift model (OQ-W1) **must separate batch vs incremental** — they have qualitatively different cross-entity behavior (Track D).
- **DOES NOT resolve (runtime path):** the incremental/runtime write — adding one fact at a time after Genesis — is **still the 41.7% corruption** of G6.1. Per the pre-registered fork, **A2 (relation-balanced in-solve sentinels) still runs** as the real lever for the incremental path; batch is folded into the recipe as the Genesis-write mode, not a replacement for the runtime fix.

## Caveats (kept flush — the surprise PASS does not earn a free pass)
- **Range is N≤100, NOT "at scale".** Genesis foundational writes can be **thousands** of facts; "eliminates" is asserted only within the tested staircase. Beyond-100 batch folds naturally into A2's re-screened ~70-entity data (current screen caps usable N≈100; larger N needs an expanded TRUTH dict).
- **Coarse held-out resolution:** n=12 held-out probes (6 entities × 2 relations) → each probe = 8.3%; a flat 100% means 12/12 correct at every rung, but fine-grained slow decline below ~8% per step is below resolution.
- **Within-entity JS-locality is slightly WORSE under batch** (95.6 seq → 90.5 batch @N=100), not better — a real, if small, trade for the large cross-entity gain. Honest direction: batch buys cross-entity isolation at a minor within-entity cost.
- **ONE write ordering** (grouped-by-entity); **3B only** (Qwen2.5-3B); subject-keyed AlphaEdit specifically; single-run top-1 (tracking the replicated JS trend).

## Note on the sequential baseline (run variance)
The A0 column above uses the originally-logged sequential collapse (91.7→58.3→41.7%, preserved in `g6_scale_n_v2.log`, the run CORPUS/13 cites). An independent **A0 re-run** this session (`a0_seq_regen.log`, regenerating the canonical `g6_scale_n_result.json` after the path-collision bug) reproduced the collapse at **91.7→50.0→33.3%** — the exact N=100 value varies run-to-run across ~33–42% from FP/ordering noise. The qualitative finding is unchanged and the contrast with batch's flat 100% is robust (if anything sharper). So `g6_scale_n_result.json` now shows seq N=100 = 33.3%, not the 41.7% headline — same falsifier, different draw.

## Decision
**D-A1-1:** batch (single joint solve) ACCEPTED as the Genesis-path write mode — cross-entity-clean at N≤100 where sequential is not. Does NOT close Track A: A2 sentinels remain the runtime-incremental fix. Fork (§8 A1 PASS branch): fold batch in → still run A2.
