---
name: verify-external-artifacts-before-effort
description: "Verify external artifacts (repo existence, arXiv IDs, availability claims) before they gate an effort estimate — a fabricated arXiv id + unchecked 'no public repo' nearly drove a 1–2 day reimplement of what's a few-hours port"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 379d00c4-1e87-4399-8a95-fd542f99e336
---

**Lesson (2026-06-18, A3/BetaEdit):** the runbook carried "BetaEdit | arXiv 2605.09285 (NO public repo) → reimplement (~1–2 days)" as a load-bearing plan item. **Both halves were false:** the arXiv id was fabricated (2605 = impossible/future id format — a precise-looking hallucination), and an official repo existed (`lbq8942/BetaEdit`, IJCAI 2026) that even ships our EXACT Qwen2.5-3B config. The operator surfaced the repo; my planning had taken the "no repo" claim at face value. The mis-estimate was ~1–2 days reimplement vs a few-hours port.

**Why:** a confident, specific external citation (an arXiv number, "no implementation exists") reads as already-verified when it is exactly the kind of thing that gets hallucinated, and it silently sets effort/sequence expectations across sessions.

**How to apply:** before an external-artifact claim gates effort or sequencing, VERIFY it cheaply — WebSearch the method name + "github"/"code", try `git clone`, fetch the real arXiv abstract. Especially distrust (a) a precise-looking ID you didn't actually fetch, and (b) any "no public repo / no implementation" assumption. A 2-minute reconnaissance can collapse a multi-day "reimplement" into a port. Cousin of [[read-authoritative-source-fully]] (that's reading the governing source fully; this is verifying an external artifact EXISTS as claimed). Pointer: [[betaedit-official-repo]].
