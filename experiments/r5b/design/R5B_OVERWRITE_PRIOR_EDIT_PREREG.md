# R5b — Overwrite-prior-edit: the unmeasured UPDATE cell (pre-registration)

**Date:** 2026-06-25 (frozen before build). **Decision-ID:** D-R5b-1 (pending). **CORPUS:** 30 (pending).
**Condition:** F1 **C3/R5** UPDATE path. **Builds on:** R5 (D-R5-1) — closes the "overwrite-prior-edit" cell flagged by advisor + Perplexity cross-family as a SEPARATE, unmeasured regime.

## Question
R5 measured two competitor regimes: NOVEL (no competitor, paraphrase-robust ~100%) and PRIOR (overwrite dense *pretrained* knowledge, fragile ~25%, reverts-to-true). **The realistic deployment update overwrites a *prior `.vindex` edit*, not pretrained knowledge.** Its difficulty is unknown and **must not be assumed to lie between** NOVEL and PRIOR (a prior edit may have *localized* the representation → easier to retarget, OR *entangled* it → harder). This populates that cell.

## Design — 3 arms, matched single-prompt protocol
Qwen2.5-3B / band[4-8] / in-solve AlphaEdit / N≈16 facts/arm / engine UNMODIFIED / LAW#5 gate. Metric = held-out **P_test** paraphrase firing (same P_test as R5, disjoint from any training prompt). All single-prompt (matches R5's *-single baselines).
- **NOVEL** (no competitor, baseline): fictional country → target. (expect ~100%, R5 replication)
- **PRIOR** (pretrained competitor, baseline): real country → counterfactual capital. (expect ~25%, R5 replication)
- **OVERWRITE-EDIT** (NEW): **step 1** fictional country → v1 (a clean novel insert — R5 shows this is paraphrase-robust); **step 2** same fictional country → v2 (≠v1), accumulating on the step-1 weights. v2's ONLY competitor is the prior EDIT v1.

## Metrics
- **PRIMARY:** post-final-edit, **v2 (target) P_test firing** — mean-rate (primary), all-3-hit (stringent), any (diagnostic); per-fact distribution. Compare OVERWRITE-EDIT vs NOVEL vs PRIOR.
- **Mechanism (OVERWRITE-EDIT):** among v2 paraphrase-failures, does **v1 resurface** (= revert-to-prior-edit → the prior edit entrenched/competes) vs some OTHER token (= instability)? Log the failure outputs (R13/R5 diagnostic, now standard).
- **Controls:** canonical-took for v2 (edit installed, ≥~90%); NOVEL/PRIOR reproduce R5 (sanity); P_test target-base ≈ 0 pre-edit.

## Pre-committed reads (able-to-fail)
- **OVERWRITE-EDIT ≈ NOVEL (~robust):** a prior edit is a WEAK competitor → overwriting prior edits is easy → **the realistic update path is fine** (reassuring for F1; the PRIOR-vs-pretrained fragility is the worst case, not the deployment case).
- **⚠ OVERWRITE-EDIT ≈ PRIOR (fragile, v1 resurfaces):** a prior edit entrenches enough to compete → **updates-over-edits are fragile too** → in-weight update path needs the diverse recipe and/or side-store (strengthens B3N side-store delegation for churn).
- **OVERWRITE-EDIT intermediate:** partial — report where it lands + the v1-resurface fraction.
- Degenerate (NOVEL/PRIOR don't reproduce R5, or v2 canonical-took low) → HALT/flag.

## Scope
band[4-8]/3B/N≈16/capital/single-prompt/1-seed. v1 installed single-prompt (paraphrase-robust per R5 NOVEL). NOT promoted without close-out + advisor + cross-family. Generality-limited.

## Artifacts
Runner `experiments/track_c/r5b_overwrite_prior_edit.py` (adapts r5); result `results/r5b_overwrite_prior_edit.json`.
