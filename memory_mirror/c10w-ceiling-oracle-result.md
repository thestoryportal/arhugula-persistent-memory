---
name: c10w-ceiling-oracle-result
description: C10 step 5 ceiling oracle FINAL (2026-10-08, CORPUS/57, D-C10w-oracle CLOSED) — band LoRA recalls 70-71/72 but with locality/forgetting cost; no gate-clean reference
metadata:
  type: project
---
Step 5 (merged rank-16 LoRA on the five band down_proj matrices, Qwen2.5-3B, 24 coined two-word facts) final replicated reading: PARTIAL-CEILING-LOCALITY-COST(G4,G6), BIGRAM. Seeds 70 and 71 of 72 → replicated 70/72 (goal 61; closed form 9–16/72 across preflight/P1/P2). G4 same-frame locality missed at both seeds (15/20 training frames); G6 MMLU loss 6/200 at seed 1 (limit 4). P3 not required; canonical split NOT-READ; reference_count null (NO-GATE-CLEAN-REFERENCE); routing INDEPENDENT-PREREG-ONLY. Astra CONFIRM (results/c10w_p2_reading_astra.md). P2 eval was re-run after an fp32 cosine halt (D-C10w-p2rerun).

**Why:** capacity on this band is not the wall for coined multi-token values, but no clean ceiling exists; it is an oracle measurement, never a route or write-engine result. C10 stays OPEN; F1 unchanged.

**How to apply:** never cite 70/72 as a reference count or target for steps 6–7 (C10X/C10Y) — they proceed on their own preregistered rationale; never call it PASS. CORPUS/55 is the P1 interim only; cite CORPUS/57. Related: [[rerun-never-patch]], [[fp32-reductions-over-big-tensors]].
