# PACKAGE — ✅ Validation Contract Architect
_Run under COUNCIL_PROTOCOL.md. Audit vs CORPUS 05 §Validation. Concern: is the output correct before commit; who tests it; is the Validator independent._

## Your spec contract (audit baseline)
Reflexion loop (Coder→Test→Fail→Fix→Retry); TGA cascade; Validator + Meta-Validator with actor-critic INDEPENDENCE (D32-33, no self-testing); **L1 Storage probe (mandatory all writes): SELECT read-back confirms edge written**; L2 behavioral/inference probe for CORE/SUPPORTING (§21); `declared_importance` gates verification intensity; deterministic sandbox; retry exit criteria.

## Relevant evidence (cite from 01)
- Our experiments USED a validation discipline analogous to the probes: expression gate (post_p>0.5) ≈ behavioral check; same/cross-entity locality measurement; LAW#5 inertness gate; explicit PASS criteria set pre-result (CORPUS 02 V&V chain).
- T1.3 verdict field literally said "FAIL/DEGRADED" from a too-strict gate — a cautionary example of a mis-specified pass criterion (the edit-survival actually passed). [03 §CORRECTED]
- Self-correction history: multiple over-claims caught + reversed (03 §CORRECTED-FROM) — evidence that the program's OWN validation was imperfect and needed external review.

## Standing questions to adversarially answer
1. **No pipeline (G3)**: there is NO Reflexion loop, NO Validator/Meta-Validator, NO deterministic pre-commit patch validation in our work — we hand-checked. The spec REQUIRES this. UNTESTED.
2. **L1 storage probe = SELECT read-back**: the spec's mandatory write-verification is a `SELECT` read-back — we verified via `INFER`, NOT `SELECT`. Does our verification satisfy the L1 contract, or is the SELECT-read-back path untested? (Ties to Graph G4.)
3. **Validator independence**: in our process, the same agent (me) produced AND judged the evidence — exactly the "self-testing agent" the contract forbids. The COUNCIL itself is the independence mechanism. Audit: are our PASS criteria (CORPUS 02) rigorous, and were any results graded leniently?
4. **Pass-criterion rigor**: review the V&V chain (02) — are the criteria falsifiable and set before results? Flag any post-hoc-looking criteria.

## Seeded gap: G3 (validation pipeline). Also AUDIT THE AUDIT — you are the check on whether our self-graded PASS/PARTIAL verdicts hold. This is your highest-value contribution: independently re-grade the evidence in 02/03.
