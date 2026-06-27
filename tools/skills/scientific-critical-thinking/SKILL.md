---
name: scientific-critical-thinking
description: >-
  Use to audit scientific claims, experiment designs, result interpretations,
  and evidence packages for bias, confounding, metric mismatch, over-claiming,
  and evidence-vs-inference drift in the LLM-as-Database program.
license: repo-local-derived
---

# Scientific Critical Thinking

Use this before preregistration, before interpreting a result, before promotion,
and after failures or surprising results.

## Audit Pass

1. State the actual claim and the binding metric.
2. Separate `EVIDENCE-SHOWS` from `I-INFER`.
3. List plausible confounders, including harness error and measurement mismatch.
4. Name the cheapest control that could overturn the claim.
5. Check denominator, sampling unit, and power/MDE.
6. Cap the label if any preregistered confound remains open.

## Evidence Rules

- Cite artifact paths and exact numbers or mark `UNVERIFIABLE`.
- Mechanics proven does not mean the spec contract is satisfied.
- Design viability is not empirical evidence.
- Same-model critique is process hygiene, not independent evidence.
