# CORPUS/23 — D20: Compaction Sub-Batch Granularity (B3N condition 3, component 2)

**Decision-ID:** `D-D20-1`. **Date:** 2026-06-21. **Pre-reg:** `docs/D20_COMPACTION_SUBBATCH_PREREG.md` (advisor-checked). **Runner:** `experiments/track_d/d20_subbatch_sweep.py`. **Results:** `results/d20_subbatch_sweep_result.json` (+`_ord1`/`_ord2`).
**E2e-map cell:** §8 Write Engine / **§11.14 Memory-lifecycle — compaction** (`docs/SPEC_E2E_GROUND_TRUTH.md` §E). **Label:** empirical **weak-form FALSIFICATION**, directional mechanism — **NOT a promoted PROVEN node** (like C2-band: real but scoped).

## Question
B3N condition 3: does the spec's §8.10 compaction stay clean once it **sub-batches**? Orientation finding: the kmeng01/memit engine does a **single joint solve regardless of N** (`memit_main.py:203`) — so "sub-batch at 2,000" is a **SPEC prescription** (spec line 384), not engine behavior. The spec's sub-batching converts one clean joint solve into **sequential accumulation** (the A0/G6.1 corruption mechanism). So condition 3 decomposes into **component 1 (SCALE — single-solve cleanliness as total-N climbs; gated on a larger stimulus pool, NOT tested here)** and **component 2 (CHUNKING — this experiment)**.

## Design
Fixed total **N=100** (the A1 record set; Qwen2.5-3B, band [4-8], in-solve AlphaEdit, **fixed-base P held across chunks**, accumulating `cache_c`). Vary only chunk size **C**: partition the N edits into ⌈N/C⌉ consecutive chunks, each an independent joint solve **accumulating on the running weights**. C=N reproduces A1 (batch); C=1 reproduces A0 (sequential) — **by construction = built-in LAW#3 anchor gates**. Metric: held-out cross-entity top-1 correctness (pooled over 2 disjoint held-out seed-sets). **3 edit orderings** (grouped + shuffle-seed-1 + shuffle-seed-2) — the advisor-mandated 2nd/3rd ordering, because edit-ORDER (not held-out selection) is the binding ~12pp 3B noise axis ([[sequential-edit-run-nondeterminism]]).

## Result (held-out edited-rel top-1 correct %, pooled; expression % in parens)
| C (chunks) | orig | ord1 | ord2 | across-ordering |
|---|---|---|---|---|
| **100** (1, =A1) | 100 (100) | 100 (99) | 100 (99) | **clean, robust** |
| 50 (2) | 90.7 (100) | — | — | orig only |
| **25** (4) | 81.2 (100) | 90.6 (96) | 96.9 (85) | **order-SOFT: −3 to −19pp** |
| **10** (10) | 65.7 (100) | 68.8 (95) | 81.3 (98) | **robustly corrupt: −19 to −34pp (all 3)** |
| 5 (20) | 40.6 (99) | — | — | orig only |
| **1** (100, =A0) | 56.2 (100) | 25.0 (96) | 37.5 (100) | corrupt, high variance (A0 anchor) |

**Anchor gates PASS all 3 orderings:** C=100 clean (100%, expr ≥99); C=1 corrupt (≥15pp below C=100). Harness validated. Expression 96–100% on every arm → **under-editing excluded**; held-out baseline 100% → clean instrument.

## Verdict — weak-form FALSIFICATION of B3N condition 3 (chunking component)
- **A real chunking-induced cross-entity corruption mechanism exists, ROBUST by C=10** (10 sequential sub-batch solves at N=100; worst-case −18.7pp, all 3 orderings well below the clean anchor). → **the spec's mandated sub-batched compaction CANNOT be assumed to return to the clean A1 state once it sub-batches enough. B3N condition 3 cannot be assumed clean.**
- **At C=25 (4 sub-batches) the effect is ORDER-DEPENDENT** (−3.1pp at ord2 = within noise) → **NOT promotable**; the pre-registered "≥10pp at C≥N/4" criterion is met in only 1/3 orderings. The robust falsification floor is **C=10, not C=25**.
- The C=1 spread (25–56%) is the documented ~50pp edit-order nondeterminism in the fully-sequential regime — the robust signal is the **trend** (corruption rises as chunks shrink) + the C=10 floor, not per-point absolutes.

## Scope / what this does NOT show (bounding claim — advisor)
- **Can FALSIFY condition 3, cannot CONFIRM it.** N held at the known-clean value (100=A1) → isolates **chunking**, not **scale**. A clean result would have meant only "chunking-tolerable-at-fixed-N"; the corrupting result transfers upward (chunking harm only worsens with scale).
- **Component 1 (SCALE) remains OPEN:** does a *single joint solve* stay clean as total-N climbs toward the spec's 2,000 cap? And where does the spec's 2,000-*size* boundary sit vs the corruption floor (C=10 here = size-10 sub-batches, 200× smaller than 2,000)? Gated on a **larger screened single-token stimulus pool** (country-attr domain caps at ~low hundreds) — the operator-visible effort call.
- 3B only; single held-out-relation pair (capital/language); the cache_c / fixed-P interaction with chunk size is an **open puzzle** (the C=5<C=1 non-monotonicity at orig was not pursued; mechanism unmeasured).

## Reviews
- **Advisor:** pre-authoring (two-component frame; the "falsify-not-confirm" bound; fixed-base P; relaxed monotonicity) + reconcile (mandated the 2nd-ordering re-run that showed C=25 is order-soft — prevented an over-claim at C=25). The result matched the scoping.
- **gpt-5.5 cross-family:** [pending at promote gate — appended below].

## Forward
Feeds the **B3N verdict (D-B3N-1)**: condition 3 is now **evidenced as failing in its chunking component** (was UNTESTED) → F1 carries condition 3 as "cannot be assumed clean; sub-batched compaction reintroduces corruption by ~10 sub-batches; scale component open." Next on the memory-lifecycle cell: the SCALE component (component 1) if/when the larger stimulus pool is built — an operator effort decision.
