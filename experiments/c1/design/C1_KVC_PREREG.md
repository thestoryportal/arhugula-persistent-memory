# C1-(a) K-vs-C — Compaction sub-batch CONFOUND BREAK (pre-registration)

**Date:** 2026-06-24 (frozen before the run). **Decision-ID:** D-C1KVC-1 (pending). **CORPUS:** 26 (pending).
**Condition:** F1 `docs/F1_DETERMINATION.md` C1 tier (a). **Builds on:** D20 (`CORPUS/23`, `docs/D20_COMPACTION_SUBBATCH_PREREG.md`). **Sizing:** `docs/F1_STIMULUS_POOL_SIZING.md`.
**Advisor:** design endorsed pre-build (run validity-clean real-pool grid; do NOT use a fictional substrate — it swaps the native-bystander phenomenon).

## Question
D20 showed accumulating sub-batching reintroduces held-out corruption at **fixed N=100**, but could not separate three co-moving factors: chunk-**SIZE** (C), chunk-**COUNT** (n_chunks = N/C), and **total-N**. This experiment breaks that confound with a **2D N×C grid** on the **real country pool** (native-knowledge validity intact — the corruption is to facts the model actually knows, the G6.1 phenomenon).

## Scope (committed BEFORE the run)
- Qwen2.5-3B / band[4-8] / AlphaEdit in-solve (fixed-base P computed once, accumulating cache_c across chunks). **Engine UNMODIFIED.** LAW#5 inertness gate runs first (harness MEMIT-mode vs engine `apply_memit`); HALT on |Δexpr|≥0.05.
- Pool: `configs/screens/g6_screen_qwen3b_v2.json` (78 entities). **Edited and held-out entity sets DISJOINT.**
- Split: edited entities **{25, 50}** → N records **{50, 100}** (capital+language, the Knowledge family); **held-out = 28 entities** → 28 capital + 28 language bystander probes (items ≈ 28/relation, near the 32 target) + continent on edited entities (within-entity control) + 6 GLOBAL probes (unrelated control).
- **This is MODEST scale (N≤100), NOT true-scale.** Bounding claim: breaks K-vs-C with native validity; does NOT test N→2,000 (stimulus-gated, C1 tier b).

## Grid cells
| N (records) | C (chunk size) | n_chunks | role |
|---|---|---|---|
| 50 | 50 | 1 | clean anchor (==A1) |
| 50 | 25 | 2 | |
| 50 | 10 | 5 | |
| 100 | 100 | 1 | clean anchor (==A1) |
| 100 | 50 | 2 | |
| 100 | 25 | 4 | |
| 100 | 10 | 10 | |

**Orderings:** **8** per corrupting cell (C<N), **2** per clean cell (C=N is a single joint solve → orderings identical; 2 = a sanity duplicate). Edit-ORDER permuted per ordering-seed (the binding nondeterminism axis, [[sequential-edit-run-nondeterminism]]). Edited/held-out sets fixed; only application order varies.

> ⚠ **Cost-driven reduction (recorded BEFORE the run).** Smoke measured `compute_z` ≈ 16–20s; compute_z calls per cell = N×orderings. The power-adequate count is ~11–12 orderings (re-size at the measured ~30–35pp swing, `results/f1_pool_sizing.jsonl`), but a 12-ordering 7-cell grid is ~20h+. **8 orderings (≈16h) is a deliberate power/runtime trade — ~60–70% power for a 20pp top-1 effect at swing≈30.** Mitigations: (1) the **continuous JS metric is the primary significance lever** (~4× more powerful per ordering than binary top-1, per the sizing); (2) this is a **first-pass directional** K-vs-C read, NOT a promotable reliability claim. The cost itself is a finding: proper-power clustered grids are multi-day at this compute_z rate → reinforces the determinism-instrument priority (cut swing ⇒ fewer orderings ⇒ affordable).

## The confound-breaking contrasts (pre-committed reads)
- **Fixed chunk-SIZE, varying COUNT:** (N50,C25 → 2 chunks) vs (N100,C25 → 4 chunks); (N50,C10 → 5) vs (N100,C10 → 10). Isolates chunk-count at fixed size.
- **Fixed chunk-COUNT, varying SIZE+N:** (N50,C25 → 2 chunks) vs (N100,C50 → 2 chunks). Isolates size/total-N at fixed count.
- **Fixed N, varying C:** the D20 axis, replicated at two N levels.

## Hypotheses (one will be supported; a null is a valid outcome)
- **H_count:** corruption tracks n_chunks (accumulated-update count) → same-count cells match regardless of size/N.
- **H_size:** corruption tracks chunk-SIZE → same-C cells match regardless of count/N.
- **H_N:** corruption tracks total-N → same-N cells match regardless of C.

## Metrics
- **PRIMARY (bystander corruption):** held-out (unedited-entity) edited-relation **top-1-correct-vs-truth**, pooled, per ordering. The G6.1 signature.
- **Secondary (more powerful):** held-out **JS-divergence** vs pre (continuous margin — `tools/stats.py`).
- **CORE-retention proxy:** edited records' expression % (the exact-1.0 gate proxy). ⚠ ≤100 records → rule-of-three bounds CORE-failure **<3%**, NOT the spec's <1% (a ≥300-CORE set needs the tier-b pool). Documented limitation.
- **Controls:** continent within-entity top-1 (edited entities); GLOBAL probes.

## Pass / fail (frozen)
1. **ANCHOR gate (LAW#3):** at BOTH N, the C=N cell reproduces A1-clean (pooled held-out ≥85% AND expr ≥95%). FAIL → harness suspect → HALT, result not trustworthy.
2. **Discrimination criterion:** a between-cell corruption difference counts as REAL only if the cluster-level contrast over orderings exceeds the noise band — **cluster-level Welch / cluster-bootstrap on per-ordering pooled held-out (`tools/stats.py`)**, at the measured between-ordering swing (~30–35pp → ~12 orderings powers a 20pp effect). The supported hypothesis is the factor whose contrasts are significant while the others' are within-band.
3. **Reportable null:** if no factor moves corruption beyond the swing band, report "modest-scale corruption is order-noise-dominated, K-vs-C unresolved at this scale" — a valid, honest outcome.
4. **NOT a promoted node** without `tools/closeout_check.py` green + advisor + gpt-5.5 cross-family at the promote gate. band[4-8]/3B/N≤100/country-domain/single-batch-per-chunk.

## Artifacts (to be produced)
Runner `experiments/track_d/c1_kvc_grid.py` (extends `d20_subbatch_sweep.py`); result `results/c1_kvc_grid_result.json`; per-ordering raw in a `per_unit` block (so `tools/stats.py` cluster-bootstrap can run — `tools/STATS_LOGGING_CONVENTION.md`).
