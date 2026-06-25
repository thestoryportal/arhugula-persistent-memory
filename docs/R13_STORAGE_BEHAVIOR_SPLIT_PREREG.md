# R13 — Storage-pass / Behavior-fail split base-rate (pre-registration)

**Date:** 2026-06-25 (frozen before build). **Decision-ID:** D-R13-1 (pending). **CORPUS:** 28 (pending).
**Matrix row:** `docs/READ_QUERY_CONTRACT_MATRIX.md` R13. **Condition:** F1 C2 read-contract leg. **Builds on:** R2/R9 single-batch harness; CP2 (L1 SELECT not weight-native); §8.9/§F.

## Question
The spec (§8.9, §F) mandates **two distinct post-write probes**, never collapsed:
- **L1 Storage probe** — `SELECT` read-back confirms the edge was **written** (all writes).
- **L2 Behavioral probe** — a generation test confirms the fact **fires in inference** (CORE/SUPPORTING).
- Named non-collapsed failure: **`storage-pass / behavior-fail`** (written but doesn't fire; `write_outcome = behavior_fail`).

**What is the base rate of storage-pass/behavior-fail for clean batch edits?** The program has measured behavioral firing (L2) under an L1 label (CP2 finding) and never quantified the split. Unknown a priori.

## ⚠ Structural note (banked regardless of the number)
CP2 already showed a **true L1 `SELECT` read-back is NOT weight-native** (it reads an intent-index, L2-under-L1-label). So in a weights-only store there is no storage probe *distinct from a forward pass* — the only "read" is running the model. **The genuine L1/L2 split requires the external index/`.vindex`** (consistent with R2/R9/R6: storage/retrieval read legs are index-delegated; only behavioral firing is weights-owned). R13 therefore measures the divergence **within forward-pass probes** as the best weights-native approximation:

## Operationalization (decision made + justified)
- **L1 "storage" proxy (weaker bar = "written/recoverable"):** target is **top-1 at the CANONICAL edit prompt** (`"The capital of {C} is the city of"` — the exact edit string). The edit took at its own prompt.
- **L2 "behavioral" (stronger bar = "fires in real inference"):** target is **top-1 across NATURAL paraphrase/assertion probes** (≥2 rephrasings that are NOT the edit string), e.g. `"{C}'s capital city is called"`, `"The city that serves as the capital of {C} is"`. L2-pass = fires on a designated primary paraphrase (paraphrase-set rate also reported).
- **storage-pass / behavior-fail** = L1-pass ∧ L2-fail = a **silent edit** (written, doesn't behave naturally). This is the spec's named mode.

## Design
Qwen2.5-3B / band[4-8] / single joint AlphaEdit / engine UNMODIFIED / LAW#5 inertness gate first. N≈24 screened countries, edit capital → counterfactual single-token city X (X≠real). Per edit, classify into the 2×2: {both-pass, **storage-pass/behavior-fail**, behavior-pass/storage-fail, both-fail}. R14 oracle: `exact_substring` on first-token of X, top-1, frozen.

## Controls
- **Native sanity control:** held-out unedited countries — L1 (canonical→real capital) and L2 (paraphrase→real capital) both fire natively (probes valid; if L2 paraphrase doesn't fire natively, the paraphrase is a bad probe, not a behavior-fail).
- Per-paraphrase breakdown (so a single bad paraphrase doesn't masquerade as behavior-fail).

## Pre-committed reads (CHARACTERIZATION — quantify the base rate)
- **If storage-pass/behavior-fail ≈ 0** (canonical & paraphrase agree): the two probes **collapse in practice** for clean batch edits at this scope → the spec's separate-probe mandate is precautionary, not empirically forced here (still justified by the structural note: L1-SELECT needs the index).
- **If storage-pass/behavior-fail substantial** (say ≥10%): the split is **real and large** → measuring only L1 (or only the canonical prompt) **over-reports**; validates the spec mandate; quantifies silent-edit risk → feeds F1 (write-verification must run L2, not just L1).
- behavior-pass/storage-fail expected ≈0 (L1 is the weaker bar); a non-zero count flags the operationalization.
- Degenerate (native control L2 low) → HALT, paraphrase probes suspect.

## Scope
band[4-8]/3B/N≈24/capital/single-batch/1-seed/counterfactual-single-token. NOT promoted without close-out. Generality-limited.

## Artifacts
Runner `experiments/track_c/r13_storage_behavior_split.py` (adapts r2); result `results/r13_storage_behavior_split.json`.
