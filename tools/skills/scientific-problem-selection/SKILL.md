---
name: scientific-problem-selection
description: >-
  Use for research problem selection, stuck-project strategy, experiment
  prioritization, and strategic scientific decisions. Repo-local adaptation of
  the audited Apache-2.0 scientific-problem-selection framework: risk,
  optimization function, decision tree, adversity planning, and problem
  inversion.
license: repo-local-derived
---

# Scientific Problem Selection

Use when choosing the next F1-moving experiment, deciding whether to continue a
method family, or reframing a stuck line of work.

## Framework

1. Name the F1 gap or runbook section 0.3 falsifier.
2. Define the optimization function: truth about buildability, not score maximization.
3. Identify parameters under our control and fixed constraints.
4. Build a decision tree with stop/continue/fallback branches.
5. Run adversity planning: how could this waste time or produce false confidence?
6. Invert the problem: what result would make the current path unnecessary?
7. Pick the cheapest test that changes a readiness condition.
8. Record open hypotheses in the hypothesis register when applicable.

## Guardrails

- Do not use this to avoid running a cheap falsifier.
- Do not turn candidate generation into evidence.
- If the spec already answers the question, follow the spec.
- If our research corpus already covers the method, cite it instead of re-surveying.
## Output Contract

Do **not** output the framework as a preamble. Use it internally, then return a
ranked route decision:

- `F1 gap:` the exact condition or runbook §0.3 falsifier.
- `Non-negotiable contract:` what the spec/operator says cannot be sacrificed.
- `Routes:` 2-4 options with expected information gain, cost, and failure mode.
- `Stop rule:` what result ends each route.
- `Recommended next move:` the cheapest faithful test that can change readiness.

A fallback that nullifies the intended in-weight memory contract is an
engineering escape hatch, not an F1 closure. If that fallback is proposed, label
it explicitly and keep the scientific condition OPEN/BLOCKING.

