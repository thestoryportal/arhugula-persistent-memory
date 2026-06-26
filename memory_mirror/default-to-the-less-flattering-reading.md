---
name: default-to-the-less-flattering-reading
description: "At every verdict gate, default to the less-flattering reading and TEST the confound with a controlling arm — don't caveat it; check a partition's axis matches the finding's axis before using it to bound severity"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 77383f65-76b8-42d1-a7de-d3da62645250
---

This session the advisor caught **~6 over-rotations at verdict gates, in BOTH directions** (R11 "spec gap discovered" → actually derivable; C6 "self-undermining gap" → unreconciled-seam; C10 "SATISFIED" on canonical-only → wrong metric; C10 "satisfied" on coherent values → prior-masked; "AnyEdit won't help" → canon=teacher-forcing-artifact misread; C10 "narrow limitation" → axes-conflation). Every time, my draft verdict was the *cleaner/more-convenient* reading. The bias is direction-agnostic: I'll over-soften a falsifier I just fired just as readily as I'll over-claim a gap.

**The remedy that worked every time: TEST the confound, don't caveat it.** When you sense a confound/alternative explanation, the right move is to add the *controlling arm/condition that separates the flattering reading from the real one* (C10: counterfactual→coherent-control→incoherent-binding→diversity-control), NOT to write the confound down as a footnote and proceed. A caveat lets the flattering number stand; a control kills or confirms it. The advisor's recurring phrase: "run the arm that separates the flattering reading from the real one."

**Two specific sharp errors to preempt:**
1. **A "pass"/"satisfied" keyed to the wrong metric.** A canonical-prompt / trained-prompt result is a TEACHER-FORCING / training-fit artifact (`compute_z` optimizes the exact prompt) — near-tautological, NOT generalization. The binding metric is the held-out/usable one (paraphrase). I keyed SATISFIED to canonical despite my own pre-reg citing R13's "trained-prompt over-reports." (See [[in-weight-value-expression-experiment-design]], [[match-metric-to-the-claim]].)
2. **Bounding a finding's severity with a partition whose AXIS differs from the finding's axis.** C10's fragility axis = prior-coherence; §7.1's axis = syntax-vs-semantics — orthogonal. Using §7.1 to call C10 "narrow" silently assumed non-prior-coherent ≈ syntactic (false, and it cut backwards — project-novel semantic entities are *enriched* for fragility). **Before using any spec partition to soften a result, verify the partition splits along the SAME axis the finding established.**

**Why:** reserve confidence for the reading that survives a control, not the one that reads well. **How to apply:** at every pre-verdict gate call advisor (it was load-bearing at all 6); when you catch yourself writing "(caveat: could be X)", ask "can I cheaply TEST X with one more arm?" — if yes, do it before the verdict. Cf. [[calibrate-symmetrically-unresolved-is-a-verdict]], [[name-the-manipulated-variable-not-the-arm-intent]], [[spec-coherence-audit-is-circular]], [[pass-label-not-equal-promotable-claim]].
