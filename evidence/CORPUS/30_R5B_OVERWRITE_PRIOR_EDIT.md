# CORPUS/30 — R5b: Re-editing a NO-pretrained-prior fact stays robust (the axis is pretrained-prior, not prior-edit)

**Decision-ID:** `D-R5b-1`. **Date:** 2026-06-25. **Pre-reg:** `docs/R5B_OVERWRITE_PRIOR_EDIT_PREREG.md`. **Runner:** `experiments/track_c/r5b_overwrite_prior_edit.py` (adapts r5; engine UNMODIFIED, primitives verbatim/inert). **Result:** `results/r5b_overwrite_prior_edit.json` (+ `results/r5b_stats.json`).
**E2e-map cell:** §8.9 L2 native-knowing / UPDATE path (§8 incremental, §11.12 pruning); F1 **C3/R5**; closes the "overwrite-prior-edit" cell flagged open by R5's reviews. **Label:** **CHARACTERIZATION**, **NOT promoted** (N=16/arm, 1 seed, 1 relation).

## Question
R5 left the realistic UPDATE case unmeasured: most deployment updates overwrite a **prior `.vindex` edit**, not dense pretrained knowledge. Its difficulty was an open conjecture (a prior edit could *localize* → easier, or *entangle* → harder; "not assumed between NOVEL and PRIOR"). This measures it.

## Design — 3 arms, matched single-prompt
Qwen2.5-3B/band[4-8]/AlphaEdit/N=16. Held-out **P_test** paraphrase firing (same as R5). **NOVEL** (insert, no competitor) · **PRIOR** (overwrite pretrained knowledge) · **OVERWRITE-EDIT** (step1 fictional→v1 = clean novel insert; step2 same→v2 accumulating — v2's only competitor is the prior EDIT v1). Mechanism: among v2 failures, does v1 resurface (entrench) vs other (instability)?

## Result
| cell | mean-rate | all-3-hit | dist[0,1,2,3] | v1-resurface |
|---|---|---|---|---|
| NOVEL (insert) | 97.9% | 15/16 | [0,0,1,15] | — |
| PRIOR (overwrite **pretrained**) | 14.6% | 0/16 | [10,5,1,0] | — |
| **OVERWRITE-EDIT (overwrite prior edit)** | **93.8%** | **15/16** | [1,0,0,15] | **0/3** |

L1-took 16/16 all arms. Stats (`r5b_stats.json`): **OVERWRITE-EDIT vs PRIOR p<1e-6** (15/16 vs 0/16 all-hit); **OVERWRITE-EDIT vs NOVEL p=1.0** (indistinguishable).

## ⚠ Verdict — the discriminating variable is PRETRAINED-PRIOR presence, NOT prior-EDIT presence (advisor-corrected)
OVERWRITE-EDIT ≈ NOVEL (93.8 vs 97.9, p=1.0) because **both lack an entrenched pretrained competitor** — the fictional subject has no pretrained anchor, and v1 is a single localized edit at the *same key* step 2 overwrites (a negligible competitor; v1 does not resurface, 0/3). So this shows **"re-editing a NOVEL-subject fact stays robust"** (prior-EDIT presence is ~irrelevant to generalization) — NOT the broader "realistic updates are robust." Map the cells by the **actual** variable:

| | 1 edit | 2 edits (edit→re-edit) |
|---|---|---|
| **no pretrained prior** (fictional) | NOVEL **97.9%** ✓ | OVERWRITE-EDIT **93.8%** ✓ |
| **pretrained prior** (real) | PRIOR **14.6%** ✗ | **UNMEASURED — predicted ≈PRIOR** (France→Paris persists under both edits; a 2nd edit doesn't remove it) |

**Axis = pretrained-prior presence: robust without it (edited or not), fragile with it (edited or not). Prior-edit presence ~irrelevant.**

**⭐ F1 / B3N — scoped to the real axis (a CONDITION, not an assumption):**
- **No-pretrained-prior facts** (insert OR re-edit): paraphrase-robust in-weight (~94–98%). ✓
- **Pretrained-prior facts** (correcting post-cutoff facts / pretraining errors; or — predicted — re-editing them): fragile (14.6%), partially recipe-rescuable (R5: →65%).
- **F1 condition (stated, not assumed):** in-weight native-knowing is robust **iff the edited subjects lack an entrenched pretrained competitor.** Whether the spec's workload qualifies is a per-content-class question: **code/structural facts (fictional-ish identifiers) → yes; domain_concepts overlapping common knowledge → no.** B3N: in-weight serves usable forward reads for the no-pretrained-prior class; reserve diverse-recipe/side-store for pretrained-prior overwrites.
- **The real-subject-re-edit cell is left as a noted PREDICTION (≈PRIOR), not run** — same mechanism (pretrained competitor present under both edits) → low marginal information.

## Scope / caveats
band[4-8]/3B/N=16/capital/single-prompt/1-seed. v1 installed single-prompt (paraphrase-robust per R5 NOVEL — the overwritten prior edit WAS a usable fact). OVERWRITE-EDIT all-hit 15/16 = robust **on these 3 paraphrases**. NOT promoted. **Key open cell = real-subject re-edit (pretrained-prior × 2 edits)** — predicted ≈PRIOR, not run. Also open: churn depth >1; v1 as a diverse-recipe (deeper) edit; relation generality beyond capital. 1-seed (the swing moved PRIOR 25→14.6 vs R5 — ordinal result robust).

## Process
Pre-registered; smoke-verified end-to-end (N=3, all arms + two-step accumulating + v1 diagnostic); inertness INERT (|Δexpr|=0.0020). **Advisor done-gate: PASS** — corrected the load-bearing interpretation (the manipulated axis is pretrained-prior presence, NOT prior-edit presence; OVERWRITE-EDIT≈NOVEL because both lack a pretrained competitor → claim is "re-editing a no-prior fact stays robust," and the real-subject-re-edit cell stays unmeasured/predicted-≈PRIOR; F1 update-path claim scoped to no-pretrained-prior subjects as a CONDITION). **Cross-family: WAIVED** — decisive ordinal result (p<1e-6), design vetted across R5's two review passes, and the only soft spot (interpretation) was corrected at the done-gate, not something an independent reader catches better ([[review-diminishing-returns-evidence-is-binding]]); codex auth-expired regardless. **NEXT: F1 synthesis refresh** (fold R2/R3/R13/R5/R5b into one read-contract + native-knowing verdict), not a 7th run.
