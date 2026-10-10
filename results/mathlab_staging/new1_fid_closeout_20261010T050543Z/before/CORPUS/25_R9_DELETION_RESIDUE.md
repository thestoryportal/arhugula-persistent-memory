# 25 — R9: In-weight deletion residue (result) — Decision-ID **D-R9-1**

_Run 2026-06-24 on the pod. **CHARACTERIZATION, NOT falsification** (label pre-committed — see §below). Pre-reg: `docs/R9_DELETION_RESIDUE_PREREG.md` (advisor pre-authoring R2-redux check + spec read; calibration call + top-5 mechanism check after). Runner `experiments/track_c/r9_deletion_residue.py`; result `results/r9_deletion_residue.json`; log `logs/r9_deletion_residue.log`. Harness: band[4–8] / Qwen2.5-3B / AlphaEdit / fixed-base P / write-batch-then-delete-batch (accumulating cache_c). Engine UNMODIFIED; primitives VERBATIM from `g6_scale_n_param.py`. LAW#5 PASSED (|Δexpr|=0.0031, loc 99.9%)._

## Why CHARACTERIZATION not falsification (spec read, 2026-06-24)
R9's matrix entry was tagged WEIGHTS+GOV "empirical-falsifier." The spec read **re-tagged it to medium-delegated characterization** (R2-class):
- **§11.2/D42:** authoritative medium is **Git** (`structural_entity`) or **`.vindex`** (Layer-4 `domain_concept`/`constraint_rule`). **NO content class is weights-authoritative** (grep: zero "weights authoritative" hits). So a fact resurfacing in raw weights after a delete **confirms** deletion lives in the overlay/tombstone/authoritative layer — it does **not falsify** the spec.
- **No delete-time "must-not-fire"/closed-world/erasure clause** exists (zero hits) — the spec specifies deletion *authority/governance* (§7.8, age floors, Dependency Holds) but **no delete-time behavioral (L2) obligation**.
The "Warden confidentiality" premise that originally motivated R9 as a sharp falsifier **was not found as an actual clause** (advisor R2-redux catch). Result framed accordingly: empirical grounding of §11.2 + a delete-time-L2 spec-gap flag. **No "R9 falsified in-weight" claim is made.**

## Method
24 fictional secrets (`"The secret access code for {} is" → " <single-token CODE>"`). **Matched write/delete breadth:** both write and delete hit **canonical only**; resurfacing tested on **held-out paraphrases neither touched**. Delete = a **corrective** AlphaEdit edit toward the captured **pre-write canonical top-1** (NOT a snapshot revert — avoids the bit-identical-un-write tautology of T2.1). DELETE group = 12; CONTROL group = 12 left written. Delete-took gate (canonical CODE no longer top-1) before any residue claim. Top-1 oracle + rank/p + top-5 hand-adjudication.

## Findings
| signal | value | reading |
|---|---|---|
| LAW#5 / base headroom | INERT; base canonical CODE-top1 **0/24** | clean instrument; fictional → firing attributable to edit |
| write canonical-took | **24/24** | edits express |
| write **generalized** to ≥1 held-out paraphrase | **19/24** | secrets are distributed → deletion has somewhere it *could* leak |
| delete-took (canonical CODE removed) | **12/12** | corrective delete suppresses canonical |
| informative set {write-took ∧ generalized-pre ∧ delete-took} | **7** | the rows where residue is non-vacuously testable |
| **RESIDUE rate** (CODE still top-1 on the generalized held-out paraphrase post-delete) | **0/7** (and 0/7 even in top-5) | **no resurfacing — suppression GENERALIZES to untouched paraphrases** |
| magnitude (hand-adj) | held-out CODE rank **0 (p 0.48–1.00) → 189–27966 (p≈0)** | annihilation, not borderline |
| mechanism (top-5 hand-adj) | post-delete held-out top-5 = **generic filler** (" a"/" an"/" the"/" ") for 6/7 | **overwrite-toward-generic (smear), NOT clean removal restoring a meaningful baseline** |
| **CONTROL bystander collateral** | canonical still-fires **12/12**; held-out still-fires **10/12** | **2/12 undeleted bystanders lost paraphrase-retrievability** = the G6.1 cross-item corruption signature wearing a delete hat |

## Net verdict — CHARACTERIZATION (floor result), framed per advisor
**In-weight corrective delete suppresses a freshly-written localized edit even on paraphrases it never touched (0/7 residue, large magnitude) — but this is the EASIEST-possible deletion, not a "works completely" result.** You are inverting a *known, localized, low-rank edit you just made* — the one case where you effectively hold the inverse operation. Three load-bearing qualifications:
1. **It's a FLOOR result.** The confidentiality-relevant case — redacting **native/deeply-trained or multiply-reinforced** knowledge (no localized inverse in hand) — is **UNTESTED and is exactly where in-weight deletion is expected to be hard**. So R9 confirms the §11.2 overlay-authoritative architecture **from the easy end**: even when in-weight deletion is maximally favorable, the spec still (correctly) does not rely on weights as the authoritative deletion medium.
2. **The mechanism is overwrite-toward-generic, not clean fact-removal.** Post-delete the entity's completion smears to generic filler (top-5 = " a"/" the"/" "), and the held-out CODE falls to floor-of-vocab (rank ~10³–10⁴) — consistent with degrading the entity representation toward filler, NOT restoring a coherent pre-fact baseline. (Pre-write held-out baseline rank was not captured → "restored to clean state" is NOT claimed.)
3. **DELETE induces bystander collateral.** ~17% (2/12) of *undeleted* secrets lost paraphrase-retrievability from the accumulating 12-edit delete batch — the same incremental-path cross-item corruption mechanism as G6.1 ([[in-weight-vs-side-store-f1-question]]). For a database, DELETE degrading unrelated rows' readability is a real defect, not noise.

**Composes with R15 (CORPUS/24):** a localized FFN edit is **easy to remove** (R9, low residue) but **hard to make adversarially robust** (R15, ~½ adversarial firing) — both are statements about what such edits can and cannot carry behaviorally.

## Honest scope / caveats
Single model (3B) / single band / 1 seed / N=24 (informative n=7 — small) / fictional-secret domain / deterministic top-1 + rank + top-5 hand-adjudication. Corrective-delete-toward-pre-write-top-1 is ONE faithful operationalization (redaction-to-sentinel = v2). Native/distributed-knowledge deletion, composition/multi-hop residue, and the overlay/`.vindex` tombstone path (the GOV-authoritative half, effective by construction) are all out of scope.

## Consequence for the program (F1)
R9 is **not** a weights-owned falsifier (§11.2: weights non-authoritative for every class) → re-tagged in `docs/READ_QUERY_CONTRACT_MATRIX.md`. It **empirically grounds the overlay-authoritative architecture from the easy end** and contributes the **delete-time-L2 spec-gap** (no mandated "must-not-fire-after-delete" probe — our result shows one would pass for localized edits, but the spec doesn't require checking, and the hard native-knowledge case is untested). Strengthens the scope-keyed-hybrid conclusion ([[in-weight-necessity-is-scope-keyed-hybrid]], D-B3N-1): the side-medium is authoritative; weights are a serving copy that is easy to *over-suppress* but does so with bystander collateral. **Structural finding surfaced this run: NO content class is weights-authoritative (§11.2)** — re-scopes the matrix's WEIGHTS tags (only R5 native-firing + R15 constraint-firing are genuinely weights-owned, both *behavioral* not *authoritative-storage*).
