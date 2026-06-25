# R2 — Reverse-lookup / bidirectional native-knowing (pre-registration)

**Date:** 2026-06-25 (frozen before build). **Decision-ID:** D-R2-1 (pending). **CORPUS:** 27 (pending).
**Matrix row:** `docs/READ_QUERY_CONTRACT_MATRIX.md` R2. **Condition:** F1 C2 read-contract leg. **Builds on:** R9/R15 single-batch harness; §11.2 structural finding.

## ⚠ LABEL PRE-COMMITTED: CHARACTERIZATION, NOT falsification (advisor-corrected)
The spec does **NOT** require weight-native reverse-lookup:
- **D16 (spec line 267):** "the write engine **auto-generates the reverse**; agents declare the canonical direction only." Reverse-edge generation is explicitly delegated to the write engine, mechanism (index vs weight) unspecified.
- **§11.2/D42 + our structural finding:** reverse-lookup is **storage/retrieval**, not behavioral firing → medium-delegated (HYBRID/`.vindex`), like R6 and R9. A weight-native reverse-FAIL **CONFIRMS the overlay architecture** ([[in-weight-falsifier-must-be-weights-owned]]); it cannot falsify the spec.

**So why run it (the value):** the *behavioral* question — **does in-weight editing produce bidirectional native-knowing, or forward-only?** — is genuinely unmeasured in this program. Its *degree* **bounds how much of the read contract weights can carry → feeds D-B3N-1** (in-weight vs side-store). Same class/value as R9's residue number. (If the only finding were "the reversal curse exists," this would be dispositioned, not run; the bounding number is the justification.)

## Question
When MEMIT edits a forward fact (subject C → object X), keyed on the **subject token C**, is the **reverse** (X → C, via the inverse relation) readable from the weights? Mechanism prior: MEMIT updates C's representation, not X's → reversal-curse predicts the reverse edge is NOT created (write-only). Open: the *degree* (partial generalization is unmeasured).

## Design
Qwen2.5-3B / band[4-8] / in-solve AlphaEdit (single joint batch, cache_c from 0) / engine UNMODIFIED / LAW#5 inertness gate first.
- **Relation: capital↔country ONLY** (≈bijective; language→country is many→one, ill-posed reverse — excluded, advisor must-have #2).
- **Edited set:** N≈24 screened countries C, each edited to a **counterfactual single-token capital X** (X ≠ C's real capital). Forward prompt `"The capital of {C} is the city of"` → X.
- **Reverse prompt:** `"{X} is the capital of the country of"` (+ a paraphrase `"{X} is the capital city of"`). Graded for country C.

## Controls (both advisor must-haves)
1. **Native-reverse POSITIVE control** (must-have #1 — distinguishes "write-only edge" from "dead probe"): on held-out **unedited** real pairs, verify the reverse template fires natively — `"{RealCapital} is the capital of"` → its true country (top-1). If this is high, the reverse template + model capability are valid, so a null edited-reverse = a real write-only-edge finding, not a broken probe.
2. **Forward-took control:** post-edit, `"capital of {C} is"` → X (top-1) — confirms the edit took (a null reverse with a null forward = nothing happened).

## Metric / R14 oracle (bound + frozen here)
- **Primary (reverse-edge creation):** at the reverse prompt, **ΔP(C) pre→post** (continuous margin) **and top-1 = C rate** (binary). Grading method = `exact_substring` on the **first token of C** (country name), case-insensitive; ΔP from the full softmax. *Frozen at this commit (§21.4).*
- Forward-took: `exact_substring` on first-token of X, top-1.
- Native-reverse control: `exact_substring` on first-token of the true country, top-1.

## Pre-committed reads (CHARACTERIZATION — no pass/fail "falsify")
- **Expected (reversal curse / write-only):** forward-took high (~100%), native-reverse control high (template valid), **edited-reverse ΔP(C)≈0 and top-1=C rate ≈ base rate** → *in-weight reverse is NOT created; reverse-lookup must be index/auto-generated (D16) → HYBRID, weights non-authoritative (§11.2 confirmed).* Bounds: weights carry forward native-knowing but NOT reverse → read-contract reverse leg is side-store-delegated.
- **If edited-reverse fires substantially** (ΔP(C) ≫ 0, top-1=C well above base): a surprising **partial bidirectional native-knowing** — report the degree; raises how much weights can carry.
- A degenerate result (forward-took low, or native-control low) → HALT, harness/probe suspect (not interpretable).

## Scope
band[4-8]/3B/N≈24/country-capital/single-batch/1-seed/counterfactual-single-token. NOT promoted without close-out + advisor + cross-family. Generality-limited (1 relation, 1 seed).

## Artifacts (to produce)
Runner `experiments/track_c/r2_reverse_lookup.py` (adapts `r9_deletion_residue.py`); result `results/r2_reverse_lookup.json`.
