# C5 — Compaction-verify soundness audit (spec-read + sampling-power analysis)

**Decision-ID:** `D-C5-1`. **Date:** 2026-06-25. **Class:** ANALYSIS (spec-read + CPU power calc) — NOT an experiment, NOT a falsifier. **Triggered by:** the C5 mount-verify governance fork (the obligation R1-bit/R10 surfaced). **Spec read end-to-end:** §8.9 (post-write verify), §8.10 (anchor-superseded archive / compaction = full MEMIT re-run), §11.2 (D42 authoritative medium), §11.3 (D43 strong consistency), §11.5 (2PC), §11.14 (D62–D66/D86 overlay compaction + C-OC3), §12.5 (consistency-status API). **Artifacts:** `results/c5_compaction_probe_power.json`.

## 0. ⚠ CORRECTION FIRST (walk back a pushed over-claim)
The prior R1-bit/R10 annotations (matrix R10, F1 register C5, CORPUS/31–32, checkpoint — pushed in commit 810d24f) framed post-compaction divergence-detection as a **spec gap** ("the spec does not state compaction re-enters validation"). **That is WRONG.** The spec **mandates** it:

> **§11.14 (D66/D86, C-OC3):** "Behavioral Probe returns a structured `CompactionProbeReport` to the TC **before Phase-2 commit**… Sampling: **100% of CORE edges** (full), ≥20% SUPPORTING (floor 5), 10% INCIDENTAL (floor 3)… **CORE pass rate MUST equal 1.0 (C-OC3 — any CORE failure is an immediate compaction abort)**; SUPPORTING ≥95%; INCIDENTAL ≥80%. Abort → existing overlays retained, `COMPACTION_ABORTED` Ledger entry." + **"Compaction is a single atomic 2PC event (C-OC2)."**

So a CORE-diverged recompile **never becomes the active served store** — it aborts and the prior clean overlay is retained. The spec's consistency model (D43 strong-consistency single-writer FIFO + mount-block; 2PC commit; C-OC3 compaction regression verify) is *designed* to prevent silent divergence. R1's in-weight per-read proxy was therefore both **bleed-unsound AND not the spec's mechanism**. Corrections applied to all five artifacts (this session).

## 1. The genuine open question (reframed, advisor-sharpened)
The spec's verifier EXISTS and is mandatory. So C5's open work is its **soundness + power + scale**, not building a detector. Two findings (analysis) + one prediction (routed elsewhere).

## 2. FINDING A — C-OC3 tolerates non-CORE fidelity loss that nothing surfaces at read (the R13 split, post-compaction, un-flagged)
**What D43 does NOT say (checked).** §11.3/D43 "strong consistency globally… no stale-read fallback" is — on the full spec read — a **transactional-isolation** guarantee (don't serve a pre-mount snapshot; single-writer FIFO serialization at the Commit Executor queue), **not** a ledger↔weights *fidelity* guarantee. The spec defines "stale" everywhere else as version/provenance/pruning staleness (§8.10, §26, §18 pruning), never as "the serving copy fails to reproduce a committed fact." And **§11.2/D42 explicitly makes the weights a *lossy* serving copy.** So a non-CORE fact dropped by a *passing* compaction is **lossy, not "stale"** — that is permitted by D42, not a D43 violation. (This retracts an earlier draft's "D43↔C-OC3 coherence gap" headline, which over-read D43 as fidelity.)

**The real, firmer finding — anchored on the spec's own vocabulary + our own R13.** §8.9 (D19/D30) names **`storage-pass / behavior-fail`** as a first-class outcome: SELECT-able but does-not-fire, "explicitly not collapsed into success." C-OC3 **by design tolerates** post-compaction `behavior_fail` below CORE (≤5% SUPPORTING, ≤20% INCIDENTAL pass the probe). The gap is not that this loss is permitted — it is that **nothing surfaces the known-tolerated `behavior_fail` at READ time**: R1-bit's delivered commit-status bit is **tier-blind and carries no post-compaction freshness mark**, so `SELECT` on a non-CORE fact that a passing compaction silently dropped returns the committed triple as though valid. This is the **post-compaction reappearance of the R13 L1/L2 split** (SELECT-able ≠ fires; CORPUS/28), un-flagged — exactly the read-surface ambiguity §8.9/D19 says must "not be collapsed." → under-specified read surface, fixable by a tier/freshness mark on the bit (§4); CORE is unaffected (full census).

## 3. FINDING B — C-OC3 non-CORE sampling has a real detection-power deficit near its thresholds (quantified, CPU)
Exact-hypergeometric power of the C-OC3 probe to **detect (abort on) a non-CORE stratum whose true divergence rate breaches its threshold** (`results/c5_compaction_probe_power.json`). Floors dominate small strata; a single sampled failure aborts when the floor is small.

**SUPPORTING (≥95% bar) — false-negative = breaching stratum silently PASSES and goes live:**
| stratum size S | sample n | true 6% | true 10% | true 20% |
|---|---|---|---|---|
| 25 | 5 | **0.63** | 0.63 | 0.29 |
| 100 | 20 | **0.66** | 0.36 | 0.05 |
| 250 | 50 | 0.39 | 0.09 | 0.00 |
| 1000 | 200 | 0.32 | 0.00 | 0.00 |

**INCIDENTAL (≥80% bar):** even weaker relative to its tolerance — S=50/n=5 at true 21%: FN **0.74**; S=100/n=10 at 21%: 0.65.

**Reading (calibrated).** Read the **10% column (2× the ≥95% bar)** as the honest, floor-driven deficit: a SUPPORTING stratum at a true **10%** divergence (double the abort threshold) still passes undetected **0.36** of the time at S=100, 0.63 at S=25. The **6% column is inherent near-threshold behaviour** — no acceptance-sampling scheme distinguishes 94% from 95% at n=5 — so it indicts sampling-near-a-threshold in general, not C-OC3 specifically; included for shape, not as the indictment. Detection becomes reliable only at **large strata (S≥250)** or **large breach (≥2× the bar)**. This is a property of the **sampling design**, *independent of any empirical divergence rate*. **CORE is fully protected** (100% census, no deficit) — the spec gets the important tier right; the deficit is strictly the floor-dominated non-CORE tiers, and it **compounds Finding A** (an undetected dropped non-CORE fact then reads as committed via the tier-blind bit). NOT a claim such rates occur — see Prediction B′.

## 4. Recommendations (spec amendments — operator-gated, NOT auto-applied)
1. **Make the C-OC3 non-CORE tolerance explicit at the read surface** (not a D43 wording change — D43 is isolation, not fidelity). The spec should state that a *passing* compaction can drop ≤5% SUPPORTING / ≤20% INCIDENTAL facts (a known `behavior_fail` per D19/D30), and that this loss MUST be surfaced to readers (next item) rather than read as valid.
2. **Tier-aware / freshness-marked commit-bit** (extends R1-bit): carry `declared_importance` + a `last_verified_anchor` on the ledger row so `SELECT` can surface a non-CORE fact as *possibly-stale-since-last-compaction* rather than silently committed. Closes the Finding-A read-surface gap.
3. **Lift the small-stratum floors** (or census small non-CORE strata): floors of 5/3 give <0.4 detection power near the thresholds; a census below e.g. S≤50 removes the worst window cheaply.

## 5. PREDICTION B′ — CORE=1.0 vs sub-batched-compaction-at-scale (NOT concluded; routed to C1-true-scale / B3N cond-3)
A *conditional* concern, recorded as a **prediction, not a finding** (the chain is multiply untested):
- *If* compaction at HARD-drift scale (§8.7: 8,000 edges) exceeds the 2,000-edge MEMIT batch and enters the **sequential sub-batch** regime, *and* that regime reproduces the D20/C1 corruption interaction for a **CORE** edge, *then* C-OC3 (CORE=1.0) aborts every attempt → with HARD-drift suspending writes until compaction completes → a **livelock**.
- **Why NOT concluded (regime-conflation guards):** (i) D20 found the *engine* does a single joint solve regardless of N; "sub-batch at 2,000" is a spec **prescription**, not measured engine behavior — whether compaction-at-8,000 even enters the corrupting *sequential* regime is open. (ii) C1's 94.8% is **all-committed expression at N=100**, not CORE-specific and not at 8,000; and its *direction* is that committed facts are the **robust** ones (held-out bystanders collapse). CORE ⊂ committed (`declared_importance`), so "~5% CORE divergence at 8,000" is a **double extrapolation** (wrong N, wrong population).
- **This IS B3N condition 3** ("compaction's own sub-batched re-run must stay clean at the realized drift size — UNTESTED, the sharpest open falsifier") and the **operator-scope-gated C1-true-scale** cell. Hand it there; do not extrapolate here.

## 6. Net
- **Correction:** post-compaction verify is spec-MANDATED (C-OC3) — the earlier gap-claim is retracted.
- **New (analysis, for-scope):** C-OC3 tolerates non-CORE `behavior_fail` (D19/D30) that **nothing surfaces at read** (the tier-blind commit-bit → the R13 L1/L2 split reappears post-compaction, un-flagged), plus a **quantified non-CORE sampling-power deficit** near the thresholds (floor-dominated; reliable only at large strata / large breach). Both are read-surface under-specifications with cheap fixes (§4). D43 is isolation not fidelity (no wording gap there); CORE is correctly protected (full census).
- **Prediction routed:** the CORE=1.0-vs-sub-batched-compaction livelock → C1-true-scale (operator scope call), NOT concluded.
- **F1 net readiness unchanged.** C5 stays PROTOTYPED-NOT-EMPIRICAL; this audit corrects an over-claim and sharpens what the Phase-2 governance work must check.
