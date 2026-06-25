---
name: spec-coherence-audit-is-circular
description: "A spec-coherence audit whose runner encodes your own spec-reading is circular; check derivability-from-a-mandated-invariant before declaring a gap; don't count an instance of a known gap as new"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 77383f65-76b8-42d1-a7de-d3da62645250
---

Hit twice in one session (R11, D-R11-1) even after the advisor flagged it once. When a "leg" is a SPEC-COHERENCE / spec-gap audit (no model, no empirical effect — the kind every remaining C2 read-contract cell R4/R7/R8/R11/R16 now is, post-frontier-inflection), three traps:

1. **The runner is circular by construction.** Its verdict is fully determined by the flags you hardcoded to encode your spec-reading (e.g. `carries_class=False`). A "matches expectation: True" is your encoding agreeing with your reading — a documentation echo, NOT validation. Validity = completeness of the spec read. Say so plainly; don't let the green read as evidence. (New shape of [[prototype-tautology-trap]]: not "my resolver routes right" but "my encoding of my reading agrees with my reading.")
2. **Check derivability from a MANDATED invariant before declaring a "gap."** R11 looked like a 3-gap "spec-gap discovered" only because the runner silently baked in "reads don't return entity_type." But §7.2/C4 MANDATES every entity is typed → content-class and severity are *derivable* functions of the returned type → COHERENT-via-derivation, not gapped. Be consistent: if you credit an off-path mechanism on one axis (D43 prevention), you must evaluate derivation-from-returned-data on the other. Derivation is stronger coherence than prevention.
3. **Don't count an instance of a known gap as new.** R11's residual was just the already-recorded "no formal query-language section" root gap re-stated at the medium/severity altitude → NOT new F1 conditions; do not double-count. (Cf. [[confirmed-delegated-is-not-delivered]].)

**Why:** these audits all resolve to the same place ("characterized, instance of the known gap, here's a spec rec," F1 readiness UNCHANGED) — so reflexively grabbing the next R# manufactures motion, not evidence. **How to apply:** at a frontier where remaining cells are all non-falsifiers, stop after one clean audit and either BUILD a genuinely-testable unit (a query-result schema + SELECT checkable against the deployed store) or surface the BUILD-vs-REGIME scope call to the operator — don't chain audits. Advisor + pre-register before, advisor before the verdict, both caught real over-claims here. Minor: R11 read-time recoverability-severity actually rests on §11.2 (medium-by-class → Git backstop exists for structural, none for L4), with §11.7 as corroboration not the function.
