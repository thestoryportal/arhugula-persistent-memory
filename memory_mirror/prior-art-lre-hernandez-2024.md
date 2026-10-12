---
name: prior-art-lre-hernandez-2024
description: "Hernandez 2024 LRE: subject-last-token linear relation map; motivates a hypothesis for Route A transfer and C10 coined-value fragility; Qwen test unrun"
metadata:
  type: reference
---

**Paper:** https://lre.baulab.info/ · arXiv 2308.09124 (v2 Feb 2024), ICLR 2024 spotlight; authors include Meng and Bau (ROME/MEMIT). Operator shared it as "new" on 2026-10-04; it is from 2024 but new to the repo. Repo note: `docs/PRIOR_ART_LRE_HERNANDEZ_ICLR2024.md` (§4 = Connected Papers graph triage, operator-supplied; read Christ 2025 "Structure of Relation Decoding Linear Operators" and Choe 2025 cross-architecture recall before any LRE prereg on Qwen).

**Core:** relation decoding ≈ `β·W·s + b` with `s` at the **last subject token**, W = mean Jacobian; >60 % faithfulness on ~half of 47 relations; `country capital city` is in the factual set; open-range name relations (Company CEO < 6 %) are NOT linear; faithfulness holds over a layer window then plummets.

**Why it matters here:** suggests an untested mechanism hypothesis for Route A's result (AnyEdit keys at the last *prompt* token → canonical transfer 1.0, paraphrase ~0.01) and for C10's value-class dependence (coined multi-word values ≈ open-range names, non-linear). Candidate falsifier (forward option (i) in CORPUS/42:35 and CORPUS/43:52; not run as of 2026-10-10): LRE faithfulness at band [4–8] on Qwen2.5-3B as a predictor/admission test for in-weight writes (local-only, cheap).
