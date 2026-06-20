---
name: pass-label-not-equal-promotable-claim
description: A pre-registered mechanical PASS label is a starting point for supervised review, not a promotable PROVEN claim — deep-thinking + cross-model independence can downgrade it.
metadata:
  type: feedback
---

A deterministic pre-registered PASS/FAIL label (autonomy driver, frozen rule on a result JSON) classifies the *run*; it is NOT the canonical scientific conclusion. The supervised fold-in still applies the full DISCIPLINE §2 deep-thinking + independent adversarial review, and that can **downgrade a mechanical PASS to CONFOUNDED / not-promoted** without violating pre-registration (you record the LABEL faithfully, then disposition the *claim* separately).

**Why:** pre-registration guards against moving goalposts on the *threshold*; it does not certify the result is unconfounded. The frozen guard may omit the variable that actually decides it.

**How to apply:** on any fold-in, (1) record the mechanical LABEL as-is; (2) check the metric that *matches the claim* (top-1 for a "reads corrupted" claim, not just JS) AND its significance/power; (3) check signs across ALL metrics, not just the headline — a *uniformly weaker/stronger* edit moves every locality the same way, so two localities moving in OPPOSITE directions (one up, one down) **refutes** "weaker edit" and means a real **redistribution**, not an artifact; (4) name the cheapest de-confounder and queue it; (5) same-model review ≠ independence — a cross-model advisor-review is still owed before promotion.

Worked case: C2-band falsifier (`CORPUS/21`, D-C2band-1) — cross-entity JS +18.73pp (mechanical PASS), top-1 leg n.s. (Fisher p≈0.37). First pass called it "indistinguishable from under-editing"; the cross-model advisor refuted that from our own data — cross-loc ROSE while within-loc FELL, and a uniformly-weaker edit raises BOTH, so it is a real direction-specific redistribution; expression=100% both arms also excludes "under-express." Corrected disposition: **real-but-underpowered (single seed; within-entity top-1 cost + mechanism unmeasured), NOT promoted** — not "confounded/might-be-nothing." Lesson: the advisor caught a logic error a same-model adversarial pass had reproduced. Related: [[evidence-over-scaffolding]], [[match-metric-to-the-claim]], [[prototype-tautology-trap]], [[autonomy-error-label-can-mask-completed-run]], [[review-diminishing-returns-evidence-is-binding]].
