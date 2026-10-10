# 13 — G6.1 SCALE-OF-N (many-overlay accumulation) — the first empirical falsifier
_Result 2026-06-18. Pre-registered in `G6_G7_PASS_CRITERIA_DRAFT.md` §G6.1. Artifacts: `g6_scale_n.py` (harness), `g6_screen.py` + `g6_screen_qwen3b.json` (screened stimulus), `g6_scale_n_result.json` (result), `g6_scale_n_v2.log` (run log). Engine UNMODIFIED; LAW#5 inertness gate passed (|Δexpr|=0.0020)._

## Why this one matters (vs CP1–G3)
CP1–G3 were design-viability prototypes ([[prototype-tautology-trap]]) — built to pass. **G6.1 is the first run that could actually FAIL, and it partially DID.** It is the binding empirical signal of the arc so far.

## What was run
Qwen2.5-3B, in-solve AlphaEdit (null-space `thresh=0.005`, L2=1.0, mom2_uw=5000, band [4-8]) — the validated recipe. **N=100 records = 50 entities × 2 fields (capital, language)**, each screened confident+correct, applied SEQUENTIALLY (grouped by entity) with `cache_c` accumulating and never reset. Staircase rungs at N=26/50/100. Counterfacts = distinct-permutation single-token real values. THREE untouched signals + (advisor-mandated) **held-out top-1 correctness** measured on the same metric as the write side.

## VERDICT — SPLIT: write-side PASS, cross-entity-consistency FAIL

### ✅ Write-side (the store holds and returns what you write) — PASS at N=100
| Metric | N=26 | N=50 | N=100 | Bar | |
|---|---|---|---|---|---|
| all-record retention | 100% | 100% | **98%** | ≥98% | PASS (high 98–100%; no systematic decline detectable at N≤100, but N=100 can't rule out slow decline — NOT asserted as a stable plateau; v1 was 100→98→98, v2 100→100→98) |
| apply-time expression | 100% | 100% | **100%** | diagnostic | PASS |
| within-entity locality (JS) | 99.8% | 99.6% | **95.6%** | ≥ baseline−5 | PASS |
| global locality (JS, non-country) | 99.5% | 99.2% | **98.4%** | no broad damage | PASS |

- The 2% loss at N=100 = exactly **2 clobbered-after-expressing** records (run-dependent: Thailand/Nigeria or Lithuania/Bangladesh capital), **0 never-expressed**.
- **The advisor's #1 risk did NOT fire:** growing `cache_c` did not strangle late edits — apply-time expression held at 100% through record 100. Clean negative result.
- Within-entity + global isolation hold at scale → editing an entity's fields does not damage its other attributes or the broader model.

### ❌ Cross-entity consistency (reads of UN-WRITTEN entities at the edited relation) — FAIL, scale-amplifying
**Held-out top-1 correctness (6 never-edited entities; baseline 100% correct on capital/language):**
| | baseline | N=26 | N=50 | N=100 |
|---|---|---|---|---|
| held-out **edited-relation top-1 correct** | 100% | 91.7% | 58.3% | **41.7%** |
| held-out **edited-relation top-1 stable** | — | 91.7% | 58.3% | 41.7% |
| held-out **continent (unedited relation) stable** | — | 100% | 100% | **100%** |
| cross-entity JS-locality (corroborating) | — | 86.1% | 66.7% | 54.4% |

- **This is genuine READ CORRUPTION, not distributional softening:** measured on top-1 (matching the claim), `stable == correct` at every rung (flips go AWAY from the truth), and it degrades **monotonically with N** (100→92→58→42%). At N=100, ~58% of un-written entities' capital/language reads have flipped to wrong answers — purely from storing facts about OTHER entities.
- **Corroboration strength:** the top-1 numbers are **single-run (v2)** but track the cross-entity **JS trend that DID replicate v1↔v2**, and the magnitude (held-out edited-relation: 12/12 correct → 5/12) is far outside the which-2-records-clobber GPU-FP noise → well-corroborated direction and magnitude, even though the exact top-1 percentages are not themselves a two-run average.
- **Relation-SPECIFIC:** the unedited relation (continent) stays **100% top-1 stable** throughout. Storing capital/language facts corrupts other entities' capital/language, NOT their continent → confirms the **shared-relation-token** mechanism.

## What it falsifies (stated strongly, because the evidence supports it)
The naive claim *"the in-weight store is cross-entity-clean at scale"* is **FALSIFIED** for subject-keyed in-solve AlphaEdit. The store reliably **retains and returns** written records (write-side strong), but writing many records at a shared relation **progressively corrupts top-1 reads of un-written entities at that relation**. For a database this is a **consistency/serializability defect that grows with N** — write isolation holds, cross-entity read isolation does not.

## Mechanism (known, now quantified at scale)
AlphaEdit's null-space `P` + `cache_c` preserve the EDITED facts' keys (→ 100% retention + within-entity hold) but provide **no protection for un-edited entities sharing the relation**. The prior session saw this at small scale (relation-keyed CE bleed ~83.6%; `SESSION_CHECKPOINT` hybrid-ladder). G6.1 shows it is **scale-amplifying and corrupts top-1 reads**, not just distributions. The known complete fix is **entity-aware in-solve projection** (Rung-3 direction: project out OTHER entities' same-relation keys) — LARQL's "address = relation + ENTITY". G6.1 gives that fix **quantified scale urgency**.

## Caveats (kept flush)
- **ONE write ordering** (grouped-by-entity); order-sensitivity not swept (pre-registered scope caveat).
- **Subject-keyed AlphaEdit specifically**; relation/entity-keyed variants untested at scale.
- Held-out set = 6 entities (12 edited-relation probes). **Continent baseline is noisy (33% correct — the "South [America]" tokenization)** so continent is used only as a top-1 **stability** control, NOT a correctness measure.
- **Qwen2.5-3B only**; larger-model behavior is the deferred G6 step (does the collapse worsen/ease with scale?).
- The pre-registered "cross-entity ≥ baseline−5" bar used a within-entity n=2 baseline (80.7%) → apples-to-oranges (advisor-noted); the **monotonic top-1 collapse is the real evidence and stands on its own**, independent of that bar.
- Determinism: v1/v2 reproduce JS within ~1pt and retention to 98% (which 2 records clobber varies — GPU FP); "deterministic in the governance sense," not bit-identical (consistent with CP1).
- **Edit operation = counterfactual reassignment** (we only write values the model does NOT already hold — the realistic edit op). Whether the same corruption magnitude appears under **non-conflicting inserts** is untested. The staircase cleanly isolates density→corruption regardless, so this bounds wording, not the finding.

## ⚠️ This SCOPES a prior headline (do not read in isolation)
The earlier "**COMPLETE multi-field store VALIDATED**" result (in-solve AlphaEdit thresh 0.005: 100% sequential retention / 80.7% untouched / 100% expression; `write_engine_viability_determination_report.md`) was **entirely same-entity / small-N** — sequential capital→currency on ONE entity, untouched = that entity's OWN other attributes. **Cross-entity-at-scale was never in that test.** G6.1 is the **first cross-entity test of the recipe**. Conclusion: the recipe that passed every prior test is **necessary-but-insufficient for a multi-ENTITY store** — same-entity multi-field is solved; cross-entity read isolation at scale is NOT (and was not previously claimed to be, though the triumphant wording glossed the relkey CE-bleed seed). Any "VALIDATED" claim must now read "validated **for same-entity multi-field**; cross-entity-at-scale OPEN/failing."

## Feeds-forward
- **Next falsifier:** does entity-aware in-solve projection (Rung-3 at scale) restore cross-entity read isolation at N=100 without losing the write-side wins? This is now the highest-value follow-up.
- The larger-Qwen3 + real-Q4_K G6 steps remain deferred (volume-space gated).
