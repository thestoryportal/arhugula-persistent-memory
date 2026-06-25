# C1 true-scale PILOT — single-joint-solve at N=2,000 (pre-registration)

**Date:** 2026-06-25 (frozen before build). **Decision-ID:** D-C1TS-1 (pending). **Class:** PILOT (1 ordering — cost anchor + first true-scale datapoint, NOT a powered falsifier). **Operator scope:** "pilot first" (chosen 2026-06-25). **Builds on:** C1-(a) (`CORPUS/26`, D-C1KVC-1) + the city→country screen (`results/c1_scale_city_country_screen.json`: 2,631 native-known single-token facts, 725 conf≥0.8). **Stimulus advisor-mandated:** real native knowledge (NOT fictional — phenomenon-swap), single high-cardinality relation (NOT multi-domain — would dilute per-relation concentration, the false-negative trap).

## Question
Does **single-joint-solve** in-weight editing at **true scale (N=2,000** — the spec's MEMIT batch boundary, §8.7) on a **high-concentration single relation** (city→country) keep **held-out bystander** facts clean? This is the **un-sub-batched** compaction path: C1-(a) found a single joint solve clean at N=100 (98.2%) while sub-batching corrupts; the open question (B3N cond-3) is whether that cleanliness **holds at 20× scale** toward the spec's regime. Plus: (2) a real **GPU-cost anchor** for the full-grid scope call; (3) **CORE=1.0 feasibility** at scale.

## Design (engine UNMODIFIED; my_edit/compute_P/inertness copied VERBATIM from `c1_kvc_grid.py`, proven inert)
Qwen2.5-3B / band[4-8] / in-solve AlphaEdit (fixed-base P, cache_c from 0) / **single joint solve (C=N=2,000, one chunk)** / 1 ordering (pilot).
- **Pool:** the 2,631 screened city→country facts (`results/c1_scale_city_country_pool.json`). Template `"The city of {} is located in the country of"` (screen-winning, 15/15 known).
- **Edit set:** N=2,000 cities → each to a **counterfactual single-token country** (X ≠ true; derangement of the country pool). Relation held constant = **maximum per-relation concentration at N=2,000**.
- **Held-out bystander:** 600 disjoint screened facts (un-edited), measured for top-1 retention to their TRUE country + JS vs pre-edit.
- **CORE subset:** the conf≥0.8 members of held-out, graded **exact-1.0** (the spec's §11.14/C-OC3 CORE gate proxy).
- **Timing:** wall-clock around the N=2,000 `my_edit` (the cost anchor).

## Metrics / oracle (frozen)
- **Held-out bystander top-1 retention %** (primary; `correct()` first-token match) + mean JS vs pre.
- **Edit expression %** (do the 2,000 edits take — top-1==counterfactual).
- **CORE exact-1.0** (held-out conf≥0.8 subset all-correct?).
- **wall-clock seconds** for the N=2,000 edit (+ compute_P, model-load separately).

## Pre-committed reads (CHARACTERIZATION + cost anchor — 1 ordering, NOT powered for the 20pp effect)
- **Expected (per C1-(a) single-solve cleanliness):** held-out retention stays HIGH (near the pre-edit baseline) → the **un-sub-batched path holds at true scale**; the hazard is sub-batching (the full grid's job), not scale per se. Edit expression high (≥90%).
- **If held-out drops materially even at single-solve:** a NEW finding — even the un-sub-batched (genesis/batch-core) path corrupts at true scale → would pressure A1/B3 genesis-core cleanliness beyond N≤100. Report directionally.
- **Anchor/validity gates (HALT if violated):** pre-edit held-out baseline must be high (screened); edit expression ≥~85% (else under-editing → not interpretable, possibly VRAM/solve degradation at N=2,000).

## Scope / caveats
**1 ordering** = a point estimate, NOT powered (the ~9–12 orderings are the full grid). Single relation (city→country) / band[4-8] / 3B / single-token / counterfactual / AlphaEdit fixed-P. The pilot's job: (a) first true-scale datapoint, (b) GPU-cost anchor to size the operator's full-grid scope call, (c) confirm the N=2,000 solve is numerically healthy (no VRAM/under-editing degradation). NOT promoted. Sub-batched arms + N×C grid + powered orderings + the exact-1.0 gate at ≥300 CORE = the full grid (next scope step).

## Artifacts (to produce)
Runner `experiments/track_d/c1_truescale_pilot.py`; result `results/c1_truescale_pilot.json`.
