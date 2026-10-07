---
name: c10-mint2-r3-provisional-no-direction
description: "CORPUS/54 (D-C10u-mint2, 2026-10-07): step 3 r3 closed PROVISIONAL — no direction reading on either block (F ROUTING-BLOCKED-UNDERFIT with the reference failing the same fit screen 17/24; V2 NOT-COMPARABLE); one-token mint LAW#3 reproduction 46/37/40 vs 14/72; operator ratification of r3 pending."
metadata:
  node_type: memory
  type: project
---

Step 3 of the research-pass sequence (D-C10u-mint2@5c772e4a), H-19, attempt r3 (r1 HALTED, r2 HALTED-HARNESS, neither pooled). r3 ran on program rulings D-C10u-r3go / D-C10u-r3skipV2 under D-C10r-rulings-9; prereg :172 required an operator ruling for any r3, still pending.

**Why:** block F's modifier-only arm was never run (seeds 17/13/14 of 24 on the one-id fit screen), but the in-block multi-token reference fails the same screen (17/24), so nothing follows about modifier-only versus the string. Block V2's baseline was far above the window (31/72, canon 24/24) → NOT-COMPARABLE. mint-1(frozen) 46/37/40 vs 14/72 is CORPUS/45's recipe reproduced (LAW#3), not a new result; the reference leads on first word (53/72). Seed 2's TRADEOFF comes from the reference's perplexity drop. The block-F replica was bit-identical because contexts, inits and targets were frozen: repeatability, not robustness.

**How to apply:** never write "modifier-only underfits" or "two-word split failed" without the reference's 17/24 (or V2's NOT-COMPARABLE) beside it; never present "LEAD" here as an improvement on CORPUS/45 (its PARTIAL stands — a scheme change, not a gain). Nothing routes on r3's labels until the operator rules. Owed: the V2 diagnosis (prereg :78). Do not re-run step 3 under the same design; a successor needs a symmetric fit screen and replication as a fresh context draw. See [[c10-secondkey-null-large-write]], [[mint-replication-spread-and-gguf-survival]].
