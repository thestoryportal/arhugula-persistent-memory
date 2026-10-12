---
name: c10-stacked-solve-tradeoff
description: "HISTORICAL: CORPUS/50 stacked second edit doubles held-out recall (12→24/72) at a 1.24× write and described_as −4.2; no target-specificity claim."
metadata:
  type: project
---

The stacked variant of the re-aim family (operator ruling D-C10q-rulings-1). One process, three passes: S (second edit aimed at z_post on top of the first), S-sham (aimed at z_pre again: a 2 % write, readout +2 — inert), S-perm (aimed at the next subject's z_post: 0/72 at a 1.91× write). S reached 12/24, 24/72 (first token 52 → 70) against the reference 8/24, 12/72. Every other locality axis and both controls held; described_as 89.31 → 85.09 failed. Run 1's echo had the same shape (gain 9, described_as −7.7, ratio 1.27).

**Why:** the injection-found direction does transfer to a weight edit when applied sequentially, but only at a locality and write cost, and well short of the 30/72 lead bar. After stacking, the first token is right on 70/72 reads; the remaining failure is the continuation after a correct first token.

**How to apply:** the prereg's TRADEOFF branch routes to the research pass (HIL first), then I-1 / I-2. A capped second write (≤ 0.75 × the first) stays an OPEN register entry: it is not a pre-registered branch after TRADEOFF, and it is not routed to the autoresearch loop, which takes no seeded ideas (docs/AUTORESEARCH.md). A permuted-target control must be energy-matched (scale its residual) to support a target-specificity claim. The frozen reader attaches -LARGE-WRITE only to LEAD/PARTIAL, while the prose applies it to every label (prereg Q2). See [[c10-twopass-solve-null-at-margin]], [[c10-edit-rotates-required-target-direction]].
