---
name: confirmed-delegated-is-not-delivered
description: "Proving a requirement is NOT met by mechanism X (e.g. not weight-native) does not satisfy it — it relocates the obligation to the delegate layer, which must itself be evidenced before the requirement counts as closed"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: fb61dcd0-ac28-4e0b-a2b3-805299505b73
---

**The trap (F1 read-contract synthesis, 2026-06-25; advisor-caught before it propagated):** the session confirmed reverse-lookup (R2), deletion (R9), closed-world (R6) are **NOT weight-native** → the spec delegates them to the `.vindex`/index layer (§11.2). It felt like the read contract had been "characterized → frontier moves on." **Wrong.** Confirming weights-don't-do-X tells you *where* the obligation lives, not that it's *met*. The structured-query burden didn't shrink — it **relocated** to the `.vindex`/index/query layer, which is prototyped-not-empirical and largely unbuilt (same epistemic status as the un-proven governance layer). "The spec delegates it by design" ≠ "the delegate delivers it."

**The general rule:** proving a NEGATIVE (requirement R is not satisfiable by mechanism A) **discharges nothing** — it moves R to mechanism B (the delegate). R is closed only when B is independently *evidenced*, not merely *named as responsible*. A readiness/F1 verdict must track the obligation to its new home and mark the delegate's evidence status, or it silently drops a load-bearing requirement.

**How to apply:**
- When an experiment confirms "X is not done by the weights/component you tested," ask immediately: *which component now owns X, and is THAT component empirically shown to deliver it?* If the delegate is unbuilt/prototyped, X is still OPEN — re-allocated, not retired.
- In synthesis, write the verdict as a **bifurcation with relocated burden**, not a "frontier-move." Anchor sentence: *"confirming a read leg is not weight-native does not close it — it relocates the obligation to the index/governance layer, which is prototyped-not-empirical; characterized along the weights/index seam, not delivered."*
- Net-readiness after a batch of "confirmed-not-weight-native" findings is typically **unchanged**: conditions sharpen and re-allocate, they don't retire.
- Distinct from [[in-weight-falsifier-must-be-weights-owned]] (that = design a falsifier on a weights-OWNED requirement). This = INTERPRET a confirmed-delegated result without over-crediting it. Pairs with [[calibrate-confidence-mechanics-vs-contracts]], [[name-the-manipulated-variable-not-the-arm-intent]].
