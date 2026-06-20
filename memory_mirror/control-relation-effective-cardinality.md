---
name: control-relation-effective-cardinality
description: "When picking a dilutant/control relation for editing experiments, check the EFFECTIVE cardinality of the confident+correct+single-token pool, not nominal distinct values — low effective cardinality breaks the control"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 7e49dca7-c684-465a-936b-1c2ce4852502
---

For relation-based editing experiments (G6/D1 family), a relation used as a **dilutant / control / counterfactual-target** must have high **EFFECTIVE** cardinality in the *confident+correct+single-token* pool — NOT just high nominal distinct-value count.

**Why (D1, 2026-06-20):**
- `continent` = cardinality-4 (Europe/Asia/Africa/Oceania) → counterfactual-among-4 edits under-express (Phase 2 seed3 INVALID: continent dilutant expression 81.2% < 95%).
- `currency` looked high-card (50 nominal distinct values in the raw screen) but the **confident+correct+single-token pool collapsed to ~17 entities / ~5 distinct values** (euro-dominated) → effectively low-cardinality, same failure mode.
- Only `capital` (44) and `language` (74) survive as clean high-cardinality dilutants on Qwen2.5-3B with the `g6_screen_qwen3b_v2.json` pool.

**How to apply:** before using a relation as a dilutant/control, compute `len(set(truth for confident+correct+single_tok entities))` — the *effective* distinct-value count in the usable pool. Low effective cardinality → counterfactual edits under-express (fails the apply-expression guard → false dilution) AND the answer space is too small to measure corruption cleanly. Check this in screening, not after a wasted run. Related: [[match-metric-to-the-claim]].
