---
name: in-weight-falsifier-must-be-weights-owned
description: "Before building an in-weight falsifier, confirm the requirement is WEIGHTS-owned (no medium-delegation) AND the edit mechanism can't determine the outcome by construction"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 52b6bccd-cd7e-4d09-ba27-988e5f3f0a72
---

When designing an experiment to FALSIFY a spec read/behavior requirement in the weights, two pre-authoring gates (advisor caught the medium-delegation trap on BOTH R15 and R9, 2026-06-24):

**⭐ STRUCTURAL FACT (spec read §11.2/D42, 2026-06-24) — read this FIRST, it resolves every read-contract row at once:** in the LLM-as-DB spec **NO content class is weights-authoritative** — Git is authoritative for `structural_entity`, `.vindex` for Layer-4 `domain_concept`/`constraint_rule`; weights carry zero authoritative content (grep "weights authoritative" = 0 hits). So **in-weight storage is always a derived/serving copy.** ⚠ The `READ_QUERY_CONTRACT_MATRIX.md` WEIGHTS/WEIGHTS+GOV tags are **DERIVED, not authoritative** — they were optimistic, and the session paid the per-row rediscovery tax TWICE (R2 dead-end, R9 mid-stream re-tag). **Read §11.2 first and re-tag the whole matrix in one pass**, don't trust a row's pre-existing tag.

**The correct THREE-way taxonomy (the session's core output) — classify the requirement before authoring:**
1. **Weights-owned BEHAVIORAL + spec-MANDATED** (a committed fact must FIRE §8.9/§1; a prohibition must fire §21.2) → a genuine **FALSIFIER**. Examples: R5 native-firing, R15 constraint-firing.
2. **Weights-owned BEHAVIORAL + spec-UNMANDATED** (e.g. a deleted fact must-not-fire — NO delete-time L2 clause exists) → **CHARACTERIZATION + spec-gap.** Still a weights-owned behavioral probe, still worth running — **probing an unmandated weights-owned behavior is itself a spec-gap-generating move** (this is exactly how R9's resurfacing half produced a finding). NOT "falsified," NOT "not worth probing."
3. **STORAGE / AUTHORITY** (persistence, deletion-completeness, consistency, reverse-lookability) → medium-delegated per §11.2; an in-weight failure CONFIRMS the overlay, never falsifies. Examples: R2 reverse, R9's authority half, R1/R6/R10/R11/R16.

(R9 spans 2+3: its resurfacing/behavioral half is category 2, its deletion-authority half is category 3. R2 is category 3. Don't collapse "characterization" into "medium-delegated" — they're different reasons.)

1. **Is the requirement WEIGHTS-owned, or medium-delegated?** Our own `docs/READ_QUERY_CONTRACT_MATRIX.md` tags each read requirement HYBRID/GOV/WEIGHTS. A requirement tagged HYBRID/GOV (e.g. **R2 reverse-lookup** — D4 §7.6 is *medium-agnostic* and the write engine *auto-generates* the reverse, so it may live on an index) **cannot be falsified in-weight**: an in-weight failure *confirms* "lives on the index layer," which the architecture already accepts. Pick the cell with **no delegation route** (e.g. **R15 constraint-firing** — a refusal/flag must be *generated*; no passive index serves it).

2. **Can the edit mechanism make the test pass/fail by construction?** AlphaEdit/MEMIT keys the edit to the **subject token's** representation. A reverse probe keys on the **object token** the edit never touched → reverse fails *mechanically*, not empirically = the [[prototype-tautology-trap]]. Verify the probe keys on the same token/direction the edit actually modifies.

**Why:** R2 looked like a sharp "reversal-curse" falsifier but was doubly moot (HYBRID-tagged + tautological). R15 was the real falsifier. **How to apply:** at the pre-authoring advisor call, state the matrix medium-tag of the target requirement and the token the edit keys vs the token the probe reads. Related: [[resolve-the-gates-real-criterion]] (test the spec's actual disjunctive criterion, not a flattering harder one — R15 §21.2 = "refuses, FLAGS, or applies"; substring-of-flag matches the *flags* disjunct, don't silently elevate refuse-rather-than-comply), [[match-metric-to-the-claim]], [[pass-label-not-equal-promotable-claim]] (frozen-oracle counts are the mechanical result; hand-adjudicate before a CORPUS determination when the oracle errs both ways). R15 result = `CORPUS/24` (D-R15-1); R9 deletion characterization = `CORPUS/25` (D-R9-1). Composed finding: a localized FFN edit is **easy to REMOVE** (R9, residue 0/7 — but that's the easiest case, inverting a self-made localized edit; native-knowledge redaction untested) yet **hard to make adversarially ROBUST** (R15, ~½ adversarial firing) — both are statements about what such edits can/can't carry *behaviorally*. Watch for the **G6.1 corruption signature** even in delete experiments (R9: applying a batch of corrective deletes knocked out paraphrase-retrievability for ~17% of undeleted bystanders).
