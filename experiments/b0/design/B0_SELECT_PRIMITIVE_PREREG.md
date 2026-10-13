# B0 — SELECT-primitive go/no-go: PRE-REGISTRATION (frozen before run)

**Date:** 2026-06-22. **Phase-1 critical-path step 1** (per `REGROUNDING_PLAN_v2.md` §9 D2). **Scope:** a PILOT (small-N, single seed) — a go/no-go signal that reshapes the read-contract plan, NOT a statistical claim. Engine fingerprint VERIFIED `5c0c706a…` ✓, `_cov_cpu`=3 ✓ (LAW#1). Qwen2.5-3B, band[4-8], in-solve AlphaEdit (proven recipe, `g6_scale_n_param.py` primitives, LAW#5 inertness gate runs first).

## The question
Is there a **weight-native read primitive distinct from free-form INFER** — i.e., can the in-weight store return a value for **committed** keys AND **abstain (null)** for **absent** keys — OR are reads purely generative (the model confabulates absent keys indistinguishably from committed ones)? This is the BLOCKER that gates the whole read contract: the program has only ever read via INFER (greedy top-1), which **always emits a token, never null**. A database SELECT returns null for absent keys; an LLM does not. CP2 found LARQL `SELECT FROM EDGES` cannot read back a triple — B0 tests whether *any* weight-native closed-world read exists.

## Why this is not a tautology (anti-prototype-trap)
The test can return the NO outcome: absent fictional keys are free to confabulate at the same confidence as committed facts. Nothing in the construction forces separability. We measure whether the store can *self-distinguish* present from absent — a property it may simply lack.

## Method
- **Fictional entities** (advisor D8 — base model has no prior, so any read-back tests the EDIT not pretraining). Each fictional entity gets a real single-token value (e.g. fictional `Zorbia` → capital `Lyon`); the *association* is novel.
- **COMMITTED set:** edit ~8 fictional (entity, attribute→value) facts. Read-back: top-1 == committed value? + max-softmax-prob.
- **ABSENT-fictional set:** ~8 fictional entities/attributes NOT edited. Query → top-1 + max-prob (= confabulation confidence on pure absence).
- **ABSENT-real set (leak probe):** ~6 real un-edited entities the model knows (e.g. France capital). Query → does the store "SELECT" leak pretrained knowledge? (provenance/commit-status discriminator-bit probe, D8.)
- **Separation metric:** does a confidence threshold τ exist that classifies COMMITTED (above) vs ABSENT-fictional (below)? Report committed read-back rate, absent confabulation rate, and the max-prob distributions for both.

## Pre-registered outcomes (frozen — can fail both ways)
- **OUTCOME-A · SELECT-PLAUSIBLE (weight-native closed-world read may be viable):** committed read-back ≥ 80% at max-prob ≥ 0.5, AND a τ exists s.t. ≥80% of committed are above τ and ≥80% of absent-fictional are below τ (abstention-by-confidence is feasible in-weight).
- **OUTCOME-B · NO-WEIGHT-NATIVE-SELECT (reads are generative INFER; closed-world needs an EXTERNAL gate):** absent-fictional max-prob overlaps committed (no clean τ; absent confabulates at max-prob ≥ 0.5 frequently) → the store cannot self-distinguish present from absent → the read contract's closed-world/SELECT obligation is **HYBRID/governance-layer**, not `WEIGHTS_MUST_CARRY`. **Loops to B3N** (in-weight-vs-side-store).
- **OUTCOME-C · MIXED/INCONCLUSIVE:** partial separation (τ exists but weak, 50–80%) → escalate to a larger pilot before the pool build.

## F1 relevance either way (Medium-of-Obligation Table)
- A → SELECT is a candidate `WEIGHTS_MUST_CARRY`/`HYBRID_ALLOWED` capability; proceed to pool V0 + B1 negative-reads at scale.
- B → SELECT/closed-world is `GOVERNANCE_MAY_ENFORCE`/`HYBRID_ALLOWED` only; the spec's "natively know" read paradigm under-specifies this; F1 records "weight-native SELECT unshown; read contract requires external commit-status/provenance gate." This is a substantive F1 finding, recorded honestly (no scope-laundering — Codex D1).

## Leak-probe note
If ABSENT-real (un-edited France etc.) reads back the correct pretrained fact at high confidence, that confirms reads are open-world generative (the store has no commit-status bit) — independent corroboration of OUTCOME-B and direct evidence the discriminator bits (commit-status/provenance) are NOT weight-native (Warden C6).

## Artifacts
`experiments/track_e/b0_select_primitive.py` → `results/b0_select_primitive_pilot.json`. Single seed; pilot. Pre-registered BEFORE the run (this doc, frozen).
