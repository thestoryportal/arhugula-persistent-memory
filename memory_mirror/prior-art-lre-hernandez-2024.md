---
name: prior-art-lre-hernandez-2024
description: "Operator-supplied prior art (2026-10-04): Hernandez et al. ICLR 2024 \"Linearity of Relation Decoding\" (LRE, Bau lab) — subject-last-token linear relation map; frames Route A's zero paraphrase transfer and C10's value-class fragility"
metadata:
  node_type: memory
  type: reference
  originSessionId: 4d71207f-24bf-4199-894f-d2f977d9f609
  modified: 2026-10-04T21:34:14.937Z
---

**Paper:** https://lre.baulab.info/ · arXiv 2308.09124 (v2 Feb 2024), ICLR 2024 spotlight; authors include Meng and Bau (ROME/MEMIT). Operator shared it as "new" on 2026-10-04; it is from 2024 but new to the repo. Repo note: `docs/PRIOR_ART_LRE_HERNANDEZ_ICLR2024.md` (§4 = Connected Papers graph triage, operator-supplied; read Christ 2025 "Structure of Relation Decoding Linear Operators" and Choe 2025 cross-architecture recall before any LRE prereg on Qwen).

**Core:** relation decoding ≈ `β·W·s + b` with `s` at the **last subject token**, W = mean Jacobian; >60 % faithfulness on ~half of 47 relations; `country capital city` is in the factual set; open-range name relations (Company CEO < 6 %) are NOT linear; faithfulness holds over a layer window then plummets.

**Why it matters here:** gives a mechanism for Route A's result (AnyEdit keys at the last *prompt* token → canonical transfer 1.0, paraphrase ~0.01) and for C10's value-class dependence (coined multi-word values ≈ open-range names, non-linear). Candidate next falsifier: LRE faithfulness at band [4–8] on Qwen2.5-3B as a predictor/admission test for in-weight writes (local-only, cheap). See [[c10k-route-a-resume]].
