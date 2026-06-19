---
name: read-authoritative-source-fully
description: Consume the governing spec/source end-to-end BEFORE framing load-bearing decisions; grep-excerpts misframe.
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 2801cf2e-560f-460c-86df-e227b16051b2
---

For most of a long session I worked from grep-excerpts of the LLM-as-Database spec instead of reading it end-to-end. This produced a multi-turn MISFRAMING of the central question (an imagined "bridge-vs-spec governance architecture decision" the operator couldn't make) that **dissolved the moment I actually read the spec** (§7.1 Schema/Code partition, §9.10 Commit Executor, §10.2/C16 direct-`.vindex`-writes-are-violations, §8.2/D20 mandatory orthogonal projection). The operator had to explicitly ask "have you actually consumed the spec end-to-end?" to surface this.

**Why:** Excerpt-driven understanding silently omits the architecture that reframes everything. I confidently built corpus docs + a decision framing on an incomplete read. Reading the full source is cheap (~30K words) relative to the cost of a wrong frame propagated across many turns.

**How to apply:** Before grounding any load-bearing decision, corpus, or "viability verdict" on a spec/paper/codebase, READ IT END-TO-END first (the governing doc in full, not just grepped sections). If you catch yourself paraphrasing a contract you only grep'd, stop and read the section. See also [[calibrate-confidence-mechanics-vs-contracts]].
