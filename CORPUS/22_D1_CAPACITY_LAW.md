# 22 — D1 CAPACITY LAW: global total-edge-count is INSUFFICIENT; drift must be relation-concentration-aware

_Result run 2026-06-20 (interactive session). Builds on G6.1 (`CORPUS/13`), A1 batch (`CORPUS/14`), C2 depth map (`CORPUS/20`), C2-band (`CORPUS/21`). Engine kmeng01/memit **UNMODIFIED**; in-solve AlphaEdit harness (LAW#5 inertness gate PASSED, |Δ|=0.0007). Pre-reg: `docs/D1_CAPACITY_LAW_PREREG.md` (frozen before run). Artifacts: `experiments/track_d/{d1_predictor_map,d1_concentration_sweep}.py`; results `results/d1_predictor_map_result.json`, `results/d1_concentration_sweep_result*.json` (seeds 0/1/2/3); logs `logs/d1_*`. Decision: **D-D1-1**. The F1-critical capacity-law deliverable (§10 readiness checklist; §9 tree "REQUIRED for F1")._

## The question (pre-registered, frozen)
Spec §8.7 models drift as `edge_count_since_anchor` — a **global, relation-agnostic** cumulative edge count (warn @1,500 / hard @8,000 / sub-batch @2,000), all flagged provisional by **OQ-W1** ("cumulative edit volume degradation threshold, model-specific"). G6.1 (`CORPUS/13`) suggested interference is **relation-fan-out-conditioned, not volume-conditioned** (§7.2). **D1 decides the monitored variable:** at a FIXED total edit count N, does held-out same-relation read corruption depend on the **concentration** of edits on one relation, or on **N** itself?

**Operational design (advisor-vetted):** fan-out = **edit-set relation-concentration at fixed N**.
- **CONCENTRATED** arm: all N=50 edits on `capital`.
- **DILUTED** arm: same N=50 interleaved across `{capital(17), language(17), continent(16)}`.
- Verdict by overlay of held-out `capital` top-1 on **x=capital-edit-count** vs **x=total-count** (advisor fix#1, to separate CONFIRM/NULL/PARTIAL). Fixed disjoint 12-entity held-out capital set (fix#2); `continent` = DILUTANT with apply-expression guard ≥95% (fix#3). Positive control: concentrated must actually corrupt.
- Qwen2.5-3B, band [4-8], sequential, in-solve AlphaEdit thresh 0.005. **4 seeds × 2 orderings** (replication = the live falsifier: entity/ordering-specificity).

## Phase 1 — predictor map (no-edit, `compute_ks` only)
- **D1 covariate** (same-relation cross-entity key collinearity @ [4-8]): capital **0.436** > language **0.412** > continent **0.333** → predicts interference-slope ranking capital > language > continent.
- **D7 basis-rotation:** dissociation ratio (same-entity-cross-rel ÷ same-rel-cross-ent) 1.71 ([4-8]) → 2.38 ([8-12]), driven by relation-clustering **falling** (not entity rising) — *weak-to-moderate* support for "relation-structure dilutes faster than entity-structure with depth"; NOT a confirmed rotation. Mechanistic, feeds the C2-band question.

## Phase 2 — the decisive concentration-vs-dilution contrast (REPLICATED)
Held-out `capital` top-1 (out of 12 held-out entities), end-of-arm:

| seed | order | CONC (50 capital) | DIL (17 cap+33 other) | gap @ equal **total-N** | gap @ cap-count | label |
|---|---|---|---|---|---|---|
| 0 | interleaved | 5/12 (41.7%) | 12/12 (100%) | 50.0pp | 0.0 | CONFIRM |
| 1 | interleaved | 7/12 (58.3%) | 10/12 (83.3%) | 16.7pp | 8.3 | PARTIAL |
| 2 | blocked | 7/12 (58.3%) | 9/12 (75.0%) | 41.7pp | 0.0 | CONFIRM |
| 3 | interleaved | 6/12 (50.0%) | 9/12 (75.0%) | 33.4pp | 8.4 | INVALID† |
| **mean** | | **52.1%** | **83.3%** | **16.7–50 (all >5)** | | |

†seed3 INVALID = the dilutant-expression guard firing correctly: `continent` (cardinality-4) under-expressed to 81.2% → "false dilution." Directionally still consistent (DIL>CONC). Flags continent as a weak dilutant, not a contradiction.
Guards (valid seeds): write retention 98–100%, apply-expr 98–100%, within-entity & global locality high; concentrated reproduces A0/G6.1 (100→41.7%) — known-baseline gate ✓.

## VERDICT — PARTIAL (mixed seeds), with ROBUST evidence that total-N-alone is insufficient
Aggregate label = **PARTIAL** (valid seeds: 2 CONFIRM + 1 PARTIAL; seed3 INVALID). Recording it as a clean "CONFIRM" would overstate the pre-registered outcome (the §3 CONFIRM rule requires capital-count overlay ≤5pp on *every* shared milestone — met in 2/3 valid seeds, not all). Two claims, at different strengths:

- **ROBUST (4/4 seeds, both orderings) — `EVIDENCE-SHOWS`:** at equal total edge-count (N=50), the concentrated store (50 capital) is more corrupted on held-out same-relation reads than the diluted store (17 capital + 33 other): valid gaps **50.0 / 16.7 / 41.7pp**, direction consistent 4/4. The within-seed contrast at seed0 (5/12 vs 12/12) is itself significant (Fisher two-sided p≈0.005), but the **binding evidence is the directional replication**, not a single-seed p. → **Global `edge_count_since_anchor` is INSUFFICIENT as a relation-agnostic drift predictor** — the spec would treat both arms identically (both N=50, same compaction trigger), yet one store is clean and one ~30pp corrupted.
- **SUPPORTED-not-settled — `I-INFER`:** relation concentration is the missing variable. But "same-relation count *dominates*" is **not** a settled law: seed1 shows an 8.3pp equal-capital-count gap (≈1 of 12 held-out entities) → a **smaller cross-relation volume term** is present in some samples. So the law is **two-variable (relation-concentration + a smaller cross-relation term)**, not pure single-variable. Magnitude/dominance is unquantified; onset ~cap 20-25 is a preliminary datum, not a threshold.

**Weak-dilutant confound — addressed, not overturning:** seed2 (blocked order, dilutant-expr **100%**, continent 100%) is the cleanest seed and a strong CONFIRM (gap_total 41.7pp) → the effect does NOT depend on weak dilutants. seed3's INVALID (continent cardinality-4 under-expressed) is the guard working; excluding it, 0/1/2 all show DIL>CONC.

## Spec ripple (F1) — the F1-usable claim
- **§8.7 drift contract: global `edge_count_since_anchor` is INADEQUATE.** `drift_state` (IC-WE-1, D83) must include **relation-concentration / per-relation counts** (e.g. max-edits-on-any-single-relation-since-anchor), and **may also need a smaller cross-relation volume term** (the two-variable result). This is the central **OQ-W1** reconciliation — interference is concentration-conditioned, not (only) volume-conditioned (resolves §7.2's "wrong variable" finding). Direction is solid; the exact functional form + thresholds are not set here.
- **Quantitative thresholds NOT set** (single model Qwen2.5-3B, band [4-8], N≤50): *which* variable to monitor is answered (concentration-aware), the warn/hard *numbers* and *dominance criterion* are not. Model-size term open — B1 (`CORPUS/19`) shows the A1 batch-clean result degrades at 7B → needs the B1/Qwen3-4B extension before law-writing.

## Independence — cross-family review (gpt-5.5 via Codex, evidence-embedded), `FIX-FIRST` → APPLIED
Opus `advisor()` (pre-write) said narrow to "total-edge-count wrong; same-relation count is the driver" and replicate-before-CORPUS. Cross-family **gpt-5.5** review (`FIX-FIRST`) tightened further and is adopted above: (1) record **PARTIAL**, not clean CONFIRM (2C/1P); (2) "total-edge-count falsified" → "**insufficient** as a relation-agnostic predictor"; (3) "dominant" is unproven → **two-variable law** (relation-concentration + smaller cross-relation term); (4) don't over-lean on the single-seed p — binding evidence is the directional replication; (5) seed2 rebuts the weak-dilutant confound; high-cardinality-relation replication still required before quantitative law-writing. **Independence obligation CLOSED** for the directional claim; quantitative law-writing remains gated on B1 + a clean 3-high-cardinality-relation replication.

## Limitations / not-yet-promoted to a final spec amendment
- N≤50, **Qwen2.5-3B only**, band [4-8] only; 12-entity held-out (±8.3pp/entity granularity).
- `continent` is a poor (cardinality-4) dilutant (seed3 under-expression); a cleaner replication would use 3 high-cardinality relations.
- Minor cross-relation term present in 2/4 seeds → "dominant," not "sole," driver.
- **Independence:** advisor-vetted (Opus). A **cross-family (Codex/gpt-5.5) review remains owed** before this feeds the F1 determination (per the C2-band precedent, `CORPUS/21`).
- **Disposition:** F1-load-bearing **directional** result, dual-reviewed (Opus advisor + gpt-5.5 cross-family). PROMOTABLE claim = *global total-edge-count is insufficient; §8.7 drift must be relation-concentration-aware*. NOT promotable = the quantitative two-variable capacity law (thresholds, dominance criterion, size term) — remaining D1 work: B1/Qwen3-4B size extension + a clean ≥3-high-cardinality-relation replication (drop cardinality-4 continent as dilutant).
