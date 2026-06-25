# CORPUS/26 — C1-(a): Compaction corruption = SCALE × SUB-BATCHING interaction

**Decision-ID:** `D-C1KVC-1`. **Date:** 2026-06-24. **Pre-reg:** `docs/C1_KVC_PREREG.md` (advisor-endorsed pre-build). **Runner:** `experiments/track_d/c1_kvc_grid.py` (extends `d20_subbatch_sweep.py`; engine UNMODIFIED; my_edit/compute_P/inertness gate copied verbatim, proven inert). **Results:** `results/c1_kvc_grid_result.json` (+ `results/c1_kvc_stats.json`).
**E2e-map cell:** §8 Write Engine / §11.14 Memory-lifecycle compaction (`docs/SPEC_E2E_GROUND_TRUTH.md` §E); F1 condition **C1** (`docs/F1_DETERMINATION.md`). **Label:** empirical **CHARACTERIZATION** that advances D20 — **NOT a promoted PROVEN node** (modest scale, 1 held-out set, 8 orderings).

## Question
Follow-up to D20 (`CORPUS/23`), which found accumulating sub-batching reintroduces corruption at fixed N=100 but flagged the **K-vs-C confound** (at fixed N, chunk-SIZE C and chunk-COUNT N/C are reciprocal) as its central open gap, proposing a 2D N×C grid. This runs that grid on the **real country pool** (native-knowledge validity — corruption is to facts the model actually knows, the G6.1 bystander phenomenon).

## Design
Qwen2.5-3B / band[4-8] / in-solve AlphaEdit (fixed-base P shared, accumulating cache_c). 2D grid: edited entities {25,50} → N records {50,100} (capital+language); held-out **28 disjoint** entities (56 bystander probes) + continent within-entity control + 6 global controls. Cells: N50×C{50,25,10}, N100×C{100,50,25,10}. **8 orderings** per corrupting cell, 2 per clean (cost-reduced from the power-adequate ~12; compute_z cost — see caveats). **Cluster unit = edit-ORDERING** (held-out probes within an ordering are correlated sub-samples). Stats: cluster-bootstrap + Welch-t on cluster means (`tools/stats.py`), binary top-1 + JS-divergence (the more-powerful metric). Anchor gates (LAW#3): C=N must reproduce A1-clean.

## Result (held-out bystander top-1 correct %, mean over orderings)
| N | C | chunks | ho-correct% | expr% | role |
|---|---|---|---|---|---|
| 50 | 50 | 1 | **100.0** | 100 | clean anchor ✓ |
| 50 | 25 | 2 | 99.8 | 96 | |
| 50 | 10 | 5 | 98.0 | 97 | sub-batching ALONE (low N) |
| 100 | 100 | 1 | **98.2** | 99 | clean anchor ✓ — concentration ALONE |
| 100 | 50 | 2 | 96.2 | 94 | |
| 100 | 25 | 4 | 91.7 | 94 | |
| 100 | 10 | 10 | **73.2** | 95 | interaction (high N × many chunks) |

Anchor gates PASS (both clean cells ≥85% & expr≥95%); baseline held-out 100%; expression 94–100% (under-editing excluded). Decisive cell per-ordering spread **51.8–89.3** (~37pp).

## ⚠ Identification (the load-bearing correction — advisor + cross-family CONVERGED)
**count = N/C is an identity.** Only **2 free knobs (N, C)**; chunk-count is derived. Every cross-N contrast moves *two* of {N, C, count}. So this **does NOT fully break D20's literal size-vs-count question** (still reciprocal at fixed N) — it *rotates* the confound (size↔count → count↔N), the [[fixed-budget-sweep-couples-iv-with-complement]] lesson one level deeper. What IS identified:

**1. Every single-factor-ONLY account is REFUTED — by EQUAL-LEVEL contrasts** (the defining prediction: a one-factor model says *same level ⇒ same outcome*; cluster-Welch significant):
- **size-only refuted:** equal chunk-SIZE C=10 — N50_C10 (98.0) vs N100_C10 (73.2) differ (Δ=−0.248, p=0.001).
- **count-only refuted:** equal chunk-COUNT=2 — N50_C25 (99.8) vs N100_C50 (96.2) differ (Δ=−0.036, p=0.0038); also count=1 anchors N50_C50 (100) vs N100_C100 (98.2) differ (Δ=−0.018, but only 2 orderings/zero-variance → fragile). *(My earlier "4-chunks-vs-5-chunks more corrupt" contrast was wrong — it only breaks a* monotone *count law, not a general count-only model; corrected per cross-family review.)*
- **N-only refuted:** equal N=100 — C100 (98.2) vs C10 (73.2) differ (Δ=−0.250, p=0.0009).
- *A monotone "more chunks ⇒ more corruption" law also fails* (4 chunks N100_C25=91.7 is MORE corrupt than 5 chunks N50_C10=98.0 — caveat: also changes N).

**2. The positive result — a non-additive (N,C) INTERACTION (difference-in-differences):**
- N-effect (N50→N100) **at C=50 = −3.8pp** (100.0→96.2); **at C=10 = −24.8pp** (98.0→73.2). The N-effect *depends on C* → no additive model Y=a(N)+b(C) fits → **genuine N×C interaction.**
- Read as corners: concentration alone (N100 single solve)=98.2 clean; sub-batching alone (N50,5ch)=98.0 clean; together (N100,10ch)=73.2 corrupt. **NOT pure scale, NOT pure sub-batching.**
- ⚠ This **rules out all single-factor-only and additive models; it does NOT pin the (N,C) functional form** (composite forms like N×g(C) remain compatible). JS metric agrees throughout (N100_C10 vs clean Δjs=+0.168, p=0.0001; all contrasts p≤0.009).

**3. Control dissociation (G6.1 signature):** continent (within-entity, 78–85%) and global probes (~95–99%) are **flat across chunking**; only **cross-entity bystanders** corrupt. The damage is cross-entity, matching G6.1 (`CORPUS/13`).

## Verdict
**Compaction corruption is a SCALE × SUB-BATCHING INTERACTION, not pure either factor.** A single joint solve at N=100 is clean (98.2%); sub-batching at N=50 is clean (98.0%); sub-batching at N=100 corrupts hard (73.2%). This **unifies D1 (concentration drives drift, `CORPUS/22`) + D20 (sub-batching corrupts, `CORPUS/23`)**: *sub-batching corrupts in proportion to concentration; a single joint solve at the same scale stays clean.*

**Spec impact (F1 C1 / §8.10 / B3N condition 3):** the spec mandates sub-batching above 2,000 edits (§10.4) = many smaller sequential solves vs one joint solve. This result says that is dangerous **specifically when concentration is high** — i.e. exactly at the scale where compaction matters. The single-joint-solve cleanliness at N=100 is reassuring for the *un-sub-batched* path; the interaction is the hazard. **Pressures condition 3; does not falsify it** (modest scale; spec's 2,000-SIZE regime still untested = C1 tier b, stimulus-gated).

## Scope / what this does NOT show
- **Does NOT break D20's literal size-vs-count** (reciprocal at fixed N; needs ≥3 N-levels or same-count-different-size cells the 78-entity pool can't supply).
- **Modest scale (N≤100)** by stimulus limit; **true-scale (N→2,000 + ≥300-CORE exact-1.0 gate) untested** (C1 tier b — real multi-domain pool OR explicit fictional confound).
- **CORE-retention proxy = edited-expr on ≤100 records** → rule-of-three bounds CORE-failure <3%, NOT the spec's <1%.
- **8 orderings (~60-70% power for 20pp top-1); 1 held-out set** → generality-limited ([[single-seed-limits-generality-not-significance]]); decisive cell CI wide (~37pp spread) → lean on JS + direction, not the −25pp point estimate.
- band[4-8]/3B/country-domain/AlphaEdit/accumulating-cache_c sub-batch semantics (the D20 spec-semantics caveat carries over).

## Process
Pre-registered before build; smoke-verified end-to-end (inertness gate INERT |Δexpr|=0.0008). **Advisor** pre-build (blocked a fictional substrate = phenomenon-swap) + post-result (caught the count=N/C identification overclaim → relabeled "K-vs-C break" → "interaction + single-factor refutation"). **Cross-family review = Perplexity Sonar Reasoning Pro** (different family from the Opus advisor; **codex/gpt-5.5 was auth-expired** — `refresh_token_reused`, needs operator re-login). Cross-family CONVERGED with the advisor and caught two further fixes (applied): (1) my count-only refutation was invalid (the 4-vs-5-chunk contrast only breaks a *monotone* count law) → switched to **equal-count contrasts** (same count ⇒ same outcome, the defining prediction); (2) the interaction must be shown by **difference-in-differences** on overlapping C levels (N-effect −3.8pp@C50 vs −24.8pp@C10), not a 3-corner vignette; (3) softened "identified" → "rules out single-factor + additive; functional form not pinned." Both reviewers agree the altitude (single-factor refutation + non-additive interaction) is correct.
