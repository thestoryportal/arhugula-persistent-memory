---
date: 2026-06-27
source: Perplexity sonar-reasoning-pro review of C10h hypotheses
scope: LLM-as-Database C10 AnyEdit
artifacts:
  - logs/perplexity_c10h_hypothesis_review_20260627_short.md
  - logs/perplexity_c10h_hypothesis_review_20260627.md
---

# Perplexity C10h Review Reranks AnyEdit Failure Geometry-First

External Perplexity Reasoning review agreed the C10h local AnyEdit result mostly
diagnoses local transplant invalidity rather than AnyEdit-as-method failure, and
recommended one focused parity day before abandoning AnyEdit-style methods. The
important correction: it ranked solve/update geometry mismatch as the most likely
cause of A1/A2=0, ahead of the team's initial lookup-index-first hypothesis.

Forward parity audit must therefore trace update geometry as a first-class object:
per-layer gradient norms, delta/update norms, effective step size, regularization
terms, and pre/post target-token logit deltas, not just token IDs, lookup index,
and masks. Cheapest decisive test per review: run upstream AnyEdit unchanged on a
tiny A1/A2 suite for the same Qwen target. If upstream recovers controls, the
local transplant is broken; if upstream also collapses, the issue is deeper than
local transplant parity and counts against AnyEdit-style integration for this stack.
