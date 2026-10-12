---
name: premortem-the-fool
description: >-
  Use as a pre-mortem and red-team reasoning pass for plans, decisions,
  interpretations, and readiness claims. It challenges assumptions and asks how
  the work could be wrong without treating critique as evidence.
license: repo-local-derived
---

# Premortem: The Fool

Use before committing to an approach or declaring a result conclusive.

## Questions

- If this result is wrong, what is the most likely reason?
- What would make this look successful while missing the real criterion?
- Which assumption came from convenience rather than evidence?
- What is the cheapest test that would embarrass this plan?
- Are we optimizing a metric instead of falsifying the spec?

## Output Shape

- Top 3 failure modes.
- One cheapest overturning test.
- One scope/caveat that must stay flush with the claim.
- Decision: proceed, fix first, or stop.

A premortem is an input to the experiment gate, not evidence for CORPUS.
## Output Contract

Do **not** recite generic questions. Return an adversarial, decision-specific
pre-mortem:

- `Likeliest way we fool ourselves:` one concrete failure mode.
- `North-star drift risk:` how this plan could preserve activity while weakening
  F1.
- `Spec-contract risk:` what requirement might be silently relaxed.
- `Cheapest embarrassing test:` one test that would overturn the plan.
- `Decision:` proceed / fix-first / stop, with the reason.

