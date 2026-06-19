# 19 — B1 / SIZE-DENSITY (does A1's batch-clean result replicate upward to 7B?)

_Result 2026-06-18. Track-B run, follow-up to A1 (`CORPUS/14`: batch ELIMINATES the G6.1 cross-entity corruption at 3B, flat 100→100→100%) and G6.1 (`CORPUS/13`). Pre-registered & advisor-vetted before authoring. Artifacts: `experiments/scale/g6_scale_n_param.py` (model-parametrized harness), `configs/hparams/qwen25_7b_memit_hparams.json`, `configs/screens/g6_screen_qwen7b.json`; result `results/b1_7b_size_density_result.json` (+ `results/g6_scale_n_batch_result_qwen7b.json`); log `logs/b1_7b_batch.log`. Engine UNMODIFIED; LAW#5 inertness gate INERT (|Δexpr|=0.0000). Decision: **D-B1-1**._

## The question
A1 showed the **batch** (single joint solve, Genesis-style) write eliminates the G6.1 cross-entity read corruption at Qwen2.5-3B. Was that cleanliness **size-robust**, or a 3B artifact? The batch isn't clean merely from lacking `cache_c` accumulation — the single joint solve still has to *absorb* the shared-relation-direction interference (the actual G6.1 mechanism), and whether it does depends on representational geometry, which changes with model size. **Same-family size control** (Qwen2.5-3B → 7B) isolates size from architecture; the 7B band-[4-8] covariance was already cached.

## Design (advisor-split by confound-sensitivity)
- **PRIMARY (load-bearing, confound-robust): does A1 batch-clean replicate at 7B?** PASS = held-out same-relation top-1 at N=100 ≥ N=0 baseline − margin (measured as the A1/G6.1 staircase from a confident-correct screened baseline).
- **SECONDARY (characterization only): seq-decline vs 3B** — multiply confounded (band relative-depth, entity pool, mom2_uw, only 2 points) → **directional color, not a size law** (that is D1's job; do not let B1 poach it).
- Setup: Qwen2.5-7B (28L, hidden 3584), band [4-8] (cov cached), AlphaEdit in-solve, N=100 (50 entities × 2 fields), batch mode. 7B-screened confident-correct pool. Expression gate (apply-expr) folded in. VRAM: the 18944-dim SVD/solve moved to CPU to fit the 7B beside the matrices.

## VERDICT — PARTIAL: batch-clean does NOT fully replicate at 7B

| measure | 3B (A1) | 7B (B1) |
|---|---|---|
| write-side retention / apply-expr | ~99–100% / 100% | **100% / 100%** |
| inertness gate | INERT | INERT (|Δexpr|=0.0000) |
| held-out edited-rel top-1, **baseline (N=0)** | 100% | **100%** (12 probes) |
| held-out edited-rel top-1, **N=100** | **100%** (flat) | **91.7%** (11/12) |
| within-relation control (continent) | stable | **100% stable** (no corruption) |

**At 7B the batch is *nearly* clean but NOT the perfectly-flat 100% of the 3B** — held-out edited-relation top-1 declines 100→91.7% (one of 12 probes flipped). The continent control stays 100% stable (the leak is relation-specific, as in G6.1). This **scopes the A1 headline**: "batch eliminates cross-entity corruption" → "...at 3B/N≤100; a small residual (~8%) appears at 7B."

## Scope & caveats (kept flush)
- **n=12 held-out probes** (one flip) — small denominator; do not over-read the magnitude.
- **Single seed**; one write ordering; batch store only.
- **Band relative-depth confound:** band [4-8] is *relatively deeper* in 7B (4-8 / 28L ≈ 14-29%) than 3B (4-8 / 36L ≈ 11-22%). The PRIMARY (within-model batch-clean Y/N) does not care; the SECONDARY size comparison is confounded by it (and by entity pool + mom2_uw) → directional only.
- **Direction of the secondary:** 7B (91.7%) is *less* clean than 3B (100%) — i.e. the *larger* model is slightly *worse*, the **opposite** of "smaller dense models collapse faster." Reported as color, not a claim. The real capacity law is **D1**.
- CPU linear-algebra (SVD + solve moved off GPU for the 7B) — numerically identical, just slower; does not affect the result.
- **Deployment direction:** 7B confirms the batch path is robust *upward*; deployment targets *small* (Intel CPU) and 3B is already clean — so "minimum viable size" eventually needs a point *below* 3B, not just above. B1 does not close the size question.

## Decision
**D-B1-1:** A1's batch-clean property is **largely but not perfectly size-robust** — a small cross-entity residual emerges at 7B. The 3B batch-deployment path (the operator's target) stands; the result tightens the scope of the A1 claim and feeds D1 (the capacity law) as a data point. Not a blocker.

## FORK
PARTIAL → the batch path remains the clean deployment path at the target size (3B), with a logged size-sensitivity. Feeds **D1** (capacity law, the F1 deliverable). Does not re-open A3/BetaEdit (still parked on a confirmed incremental requirement).
