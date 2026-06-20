---
name: deterministic-null-label-can-hide-real-effect
description: "A pre-registered NEGATIVE/null label means \"didn't clear THIS detector,\" not \"effect absent\" — inspect the raw paired/sign pattern, which carries info a magnitude threshold discards"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 7e49dca7-c684-465a-936b-1c2ce4852502
---

A pre-registered deterministic label is a **detector with finite power**. `LABEL=NEGATIVE/null/cross_real=False` means *"didn't clear this specific rule,"* NOT *"the effect is absent."* Respect the frozen label (don't move pre-registration), but **interpret it correctly** by inspecting the raw per-unit pattern.

**Why (D1 Phase 3, 2026-06-20):** the script rule `cross_real = (mean > granularity AND ≥60% positive)` returned False (mean 3.7pp ≤ 4.2pp/entity single-set resolution), and I nearly concluded "no cross-relation term / single-variable / concentration even MORE dominant." The advisor caught it: the paired within-arm deltas were **6 positive / 3 zero / 0 negative** — a **paired sign test on the 6 non-tie arms = 0.5⁶ ≈ p=0.016**, i.e. evidence FOR a small real effect. The blunt "mean vs single-measurement granularity" rule **threw away the sign-consistency information**; averaging N sign-consistent paired measurements beats the per-measurement floor.

**How to apply:**
- For paired/directional data, **always look at the sign pattern (and run a sign test), not just the verdict string or the mean-vs-threshold.** A pre-reg threshold tuned for one measurement is underpowered for a sub-resolution-but-consistent effect.
- State it as: "frozen LABEL=X by the rule; the rule is underpowered for a ~1-unit effect; the sign pattern indicates a small real Y" — same move as [[pass-label-not-equal-promotable-claim]] but for the NULL direction (a null label hiding a real effect, vs a PASS label overstating).
- Don't over-correct either way: a low-power sign signal is a *directional* signal, not a precise effect size ([[single-seed-limits-generality-not-significance]]). Cross-family review (gpt-5.5) flagged not to headline the p-value as an effect size.
