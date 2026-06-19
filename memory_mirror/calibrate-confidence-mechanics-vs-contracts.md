---
name: calibrate-confidence-mechanics-vs-contracts
description: "Default to precise, hedged, evidence-anchored claims; \"mechanics proven\" ≠ \"full contracts satisfied\"; log reversals."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 2801cf2e-560f-460c-86df-e227b16051b2
---

This session I over-claimed repeatedly and was corrected by the advisor twice and the operator several times: "high-certainty viable path demonstrated" (it was one fact, served) → recalibrated; "LARQL is Gemma-only" → wrong (qwen.rs exists); "Option B needs LARQL dev / bleed unfixable without code" → wrong (ROUTE VERIFY + the bridge); "rollback fails" → wrong (file-level rollback works); "DIFF = the bridge" → wrong (DIFF captured metadata only). Each over-claim cost trust + rework.

**Why:** Proving a MECHANISM works (an edit expresses, a read serves) is not the same as proving the SPEC CONTRACT is satisfied (governance, authorization, query schema, in-pipeline operation). Collapsing the two produces false confidence. Excitement at a working result ("the bridge works!") amplified the overreach.

**How to apply:** Use precise language by default — distinguish "the math/mechanics work" from "the contract is satisfied"; say what's tested vs untested vs inferred. When you feel most confident, that's the moment to call advisor() — it caught these errors precisely when I was sure. Keep an explicit corrections ledger; cite artifact + exact number per claim. Bias toward under-claiming. See also [[read-authoritative-source-fully]], [[review-diminishing-returns-evidence-is-binding]].
