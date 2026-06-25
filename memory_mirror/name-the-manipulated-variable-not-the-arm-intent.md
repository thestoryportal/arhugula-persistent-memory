---
name: name-the-manipulated-variable-not-the-arm-intent
description: Recurring experiment-design error — the arm LABEL/intent keeps naming a different variable than what's actually manipulated; identify the true manipulated axis before interpreting
metadata:
  type: feedback
---

Across the 2026-06-25 read-contract/native-knowing slice, the SAME interpretation error recurred in every experiment and the advisor caught each one:
- **C1** "K-vs-C grid" — but count=N/C is an identity, so the 2D grid manipulated only (N,C); "chunk-count" wasn't independently varied.
- **R3** "do families express" — but family is 1-to-1 with cardinality, so a cross-family difference can't be attributed to family (it's cardinality, already D1's within-family result).
- **R5** "storage vs behavior" — both probes were forward-pass (behavioral); the real axis was trained-prompt vs paraphrase (editing-overfit). Also headlined mean-rate but tested any-hit.
- **R5b** "overwrite-prior-EDIT" — but OVERWRITE-EDIT≈NOVEL because both lack a PRETRAINED competitor; the manipulated axis is pretrained-prior presence, NOT prior-edit presence. The arm's INTENT (test prior-edit competition) ≠ what varied (v1 was a negligible competitor).

**Why:** an arm's NAME encodes the intent/hypothesis; the CONTRAST it actually licenses is set by what differs between arms, which is often a different (or confounded) variable. Naming by intent smuggles the unproven attribution into the verdict.

**How to apply (before interpreting ANY multi-arm result):**
1. For each contrast, list EVERY variable that differs between the two arms (not just the one you meant to vary). If >1 differs, you have not isolated your IV — relabel the claim to the confounded/joint variable or add a control arm.
2. Check for identities/co-variation among factors (count=N/C; family↔cardinality; novel↔thin; prior-edit↔pretrained-prior). Co-determined factors are one knob ([[fixed-budget-sweep-couples-iv-with-complement]]).
3. Bind significance to the metric that matches the CLAIM ([[match-metric-to-the-claim]]); don't headline one metric and test another.
4. Write the verdict as "varying X (with Y co-varying) changes Z" — name the manipulated axis, not the arm's intent. Then the untested cell (the one your label implied but didn't isolate) becomes explicit (e.g. R5b's real-subject-re-edit).
5. Call advisor BEFORE writing the verdict — this class of error is invisible from inside the framing that produced it.
