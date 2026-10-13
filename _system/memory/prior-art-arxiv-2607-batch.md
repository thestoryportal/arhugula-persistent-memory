---
name: prior-art-arxiv-2607-batch
description: "Four arXiv 2607.* memory papers (Metis, Memory Decoder at Scale, MemHarness, MemTxn): no LEAD; MemTxn's rollback test is the reusable lifecycle design"
metadata:
  type: reference
---

Note: `results/prior_art_arxiv_2607_batch_2026-10-06.md` (full-text read via the arXiv MCP; WebFetch summaries disagreed between calls, so trust the MCP).
- **2607.26760 Metis** — CONTEXT: per-session fast-weight memory state learned by mid-training (Qwen3.5 backbone), not a weight write; Table 5 MemOps Gold Remember 28.27 / Update 31.02 / Forget 10.91; Table 10 IFEval −22.18 once irrelevant memory is stored (a locality cost of filling memory).
- **2607.27919 Memory Decoder at Scale** — FALLBACK (research-pass disposition holds; its "pool/lookup" wording was wrong: a separate trained module mixed at the output, Eq. 2, lookup offline only). Table 5 (verified): BioInst memory 23.21 vs CPT 13.00 vs none 5.39 (Qwen3 1.7B) — soft targets beat hard labels; not a paraphrase test.
- **2607.28272 MemHarness** — NOT RELEVANT (RL rewriting of retrieved agent text).
- **2607.27834 MemTxn** — CONTEXT: external SQLite governance; complete-state rollback (0 failures over 272 runs vs single-key baseline failing all 136), stale-rate metric, replayable admission → template for a delete/rollback test: write N, delete or roll back k, all N readouts must equal the snapshot.
Related: [[prior-art-sleeping-llm-2026]], [[prior-art-sweep-2026-10]].
