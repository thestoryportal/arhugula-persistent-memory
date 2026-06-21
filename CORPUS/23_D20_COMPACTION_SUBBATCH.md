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

## Verdict — DIRECTIONAL MECHANISM found (NOT a falsification of the spec's condition 3) — tightened by gpt-5.5
- **DIRECTIONAL MECHANISM (the defensible claim):** *accumulating sequential sub-batching can reintroduce held-out cross-entity corruption even when the equivalent single joint solve is clean.* **Order-insensitive across all 3 tested orderings at C=10** (drops −19 to −34pp, sign-consistent and exceeding the ~12pp 3B noise), but n=3 orderings → **directional, NOT a tightly-bounded effect size.** C=25 is order-dependent (−3.1pp at ord2 = within noise) → **not promotable; the robust floor is C=10.** C=1 spread (25–56%) = the documented ~50pp sequential-regime edit-order noise → trust the trend + the C=10 floor, not per-point absolutes.
- **NOT PROVEN (do not claim):** that the spec's **2,000-edit-SIZE** sub-batched compaction fails, or that clean compaction cannot return at larger N/C. This run **pressures** B3N condition 3 (compaction can't be *naively assumed* clean once it sub-batches) but does **not falsify** it — see the two load-bearing gaps below.
- **⚠ K-vs-C CONFOUND (the central open gap, gpt-5.5):** at fixed N=100, chunk-SIZE C=10 is also chunk-COUNT K=10 — inseparable. The corruption may be driven by **accumulated-update-COUNT** (more sequential solve applications / cache_c accumulations / residualizations), **not chunk size per se.** The apparent "chunk-size floor" may really be an update-count floor. **Disambiguating test: a 2D grid varying N and C independently (or same-K-larger-C once a larger stimulus pool exists).**
- **⚠ SPEC-SEMANTICS MISMATCH:** the spec's compaction is a "full MEMIT re-run on archived patches" at chunk-SIZE ~2,000 (few large solves); this test is many small solves at N=100 (200× smaller chunks) with our **harness-specific accumulating `cache_c`**. If the spec's sub-batching does not use this accumulating-cache sequential semantics, the result indicts **our sub-batching algorithm**, not "compaction" generally. Whether the spec mandates the same semantics is **unverified**.

## Scope / what this does NOT show (bounding claim — advisor)
- **Can FALSIFY condition 3, cannot CONFIRM it.** N held at the known-clean value (100=A1) → isolates **chunking**, not **scale**. A clean result would have meant only "chunking-tolerable-at-fixed-N"; the corrupting result transfers upward (chunking harm only worsens with scale).
- **Component 1 (SCALE) remains OPEN:** does a *single joint solve* stay clean as total-N climbs toward the spec's 2,000 cap? And where does the spec's 2,000-*size* boundary sit vs the corruption floor (C=10 here = size-10 sub-batches, 200× smaller than 2,000)? Gated on a **larger screened single-token stimulus pool** (country-attr domain caps at ~low hundreds) — the operator-visible effort call.
- 3B only; single held-out-relation pair (capital/language); the cache_c / fixed-P interaction with chunk size is an **open puzzle** (the C=5<C=1 non-monotonicity at orig was not pursued; mechanism unmeasured).

## Reviews
- **Advisor:** pre-authoring (two-component frame; the "falsify-not-confirm" bound; fixed-base P; relaxed monotonicity) + reconcile (mandated the 2nd-ordering re-run that showed C=25 is order-soft — prevented an over-claim at C=25). The result matched the scoping.
- **gpt-5.5 cross-family (FIX-FIRST, applied):** concurs "directional mechanism found, not proven that spec-scale 2,000-edit sub-batching fails." Fixes folded: **(1)** verdict softened from "FALSIFY condition 3" → "directional mechanism; pressures-not-falsifies" (the spec's condition is about 2,000-SIZE compaction with possibly-different semantics); **(2)** "robust by C=10" → "order-insensitive across 3 tested orderings, directional not effect-size-bounded"; **(3)** named the **K-vs-C confound** (accumulated-update-COUNT vs chunk-SIZE — the central gap → 2D N×C grid) + **cache_c accumulation semantics** (may indict our algorithm, not compaction generally) + scope to "under this harness" (band[4-8]/3B/AlphaEdit/fixed-P, not MEMIT-class broadly) + held-out-pool coupling (2 seed-sets may share structure → lower effective independence) + order distribution (3 non-adversarial orderings → "order-insensitive" stays weak). Independence obligation CLOSED.

## Forward
Feeds the **B3N verdict (D-B3N-1)**: condition 3 is now **directionally pressured** (was UNTESTED) → F1 carries condition 3 as "**cannot be naively assumed clean** — accumulating sub-batching reintroduces corruption when the joint solve is clean (directional, this harness); the spec's 2,000-SIZE compaction is **not** shown to fail, and the **K-vs-C confound** (count vs size) is open." **Next, two disambiguating tests (both gated on a larger screened stimulus pool — operator effort call):** (a) a **2D N×C grid** (or same-K-larger-C) to separate accumulated-update-COUNT from chunk-SIZE; (b) **component 1 (SCALE):** single-solve cleanliness as total-N→thousands + where the spec's 2,000-SIZE boundary sits vs the corruption floor. Also cheap: verify whether the spec's prescribed sub-batching uses accumulating-cache sequential semantics (else the finding indicts our algorithm, not compaction).
