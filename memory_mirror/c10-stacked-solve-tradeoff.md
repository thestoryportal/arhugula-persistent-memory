---
name: c10-stacked-solve-tradeoff
description: "CORPUS/50 (D-C10q-stacked, 2026-10-06): a second in-place edit aimed at the re-solved target doubles held-out recall (12 → 24/72) but costs a write 1.24× the first and 4.2 points of described_as (gate 3.0) → TRADEOFF-PERM-UNMATCHED; sham inert; the permuted control destroys recall but misses the ×1.5 energy window by 0.04, so no target-specificity claim."
metadata:
  node_type: memory
  type: project
  originSessionId: 4d71207f-24bf-4199-894f-d2f977d9f609
---

The stacked variant of the re-aim family (operator ruling D-C10q-rulings-1). One process, three passes: S (second edit aimed at z_post on top of the first), S-sham (aimed at z_pre again: a 2 % write, readout +2 — inert), S-perm (aimed at the next subject's z_post: 0/72 at a 1.91× write). S reached 12/24, 24/72 (first token 52 → 70) against the reference 8/24, 12/72. Every other locality axis and both controls held; described_as 89.31 → 85.09 failed. Run 1's echo had the same shape (gain 9, described_as −7.7, ratio 1.27).

**Why:** the injection-found direction does transfer to a weight edit when applied sequentially, but only at a locality and write cost, and well short of the 30/72 lead bar. After stacking, the first token is right on 70/72 reads; the remaining failure is the continuation after a correct first token.

**How to apply:** the prereg's TRADEOFF branch routes to the research pass (HIL first), then I-1 / I-2. A capped second write (≤ 0.75 × the first) stays an OPEN register entry: it is not a pre-registered branch after TRADEOFF, and it is not routed to the autoresearch loop, which takes no seeded ideas (docs/AUTORESEARCH.md). A permuted-target control must be energy-matched (scale its residual) to support a target-specificity claim. The frozen reader attaches -LARGE-WRITE only to LEAD/PARTIAL, while the prose applies it to every label (prereg Q2). See [[c10-twopass-solve-null-at-margin]], [[c10-edit-rotates-required-target-direction]].
