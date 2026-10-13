---
name: verify-external-artifacts-before-effort
description: Verify external artifacts (repo, arXiv id, 'no code') before they gate effort; verify 'it is fake' claims too (BetaEdit 2605.09285 is real).
metadata:
  type: feedback
---

**Lesson (2026-06-18, A3/BetaEdit):** the runbook carried "BetaEdit | arXiv 2605.09285 (NO public repo) → reimplement (~1–2 days)" as a load-bearing plan item. **Neither half was verified:** an official repo existed (`lbq8942/BetaEdit`, IJCAI 2026) that even ships a Qwen2.5-3B config, and the arXiv id was real. A later note then called the id "fabricated" (2605 read as an impossible/future id format) — that correction was itself unverified and wrong: the research pass opened the abstract on 2026-10-06 ("BetaEdit: Null-Space Constrained Sequential Model Editing", IJCAI 2026; results/research_pass_2026-10-06/contradictions.md §1). The operator surfaced the repo; my planning had taken the "no repo" claim at face value. The mis-estimate was ~1–2 days reimplement vs a few-hours port.

**Why:** a confident, specific external citation (an arXiv number, "no implementation exists") reads as already-verified when it is exactly the kind of thing that gets hallucinated, and it silently sets effort/sequence expectations across sessions.

**How to apply:** before an external-artifact claim gates effort or sequencing, VERIFY it cheaply — WebSearch the method name + "github"/"code", try `git clone`, fetch the real arXiv abstract. Especially distrust (a) a precise-looking ID you didn't actually fetch, (b) any "no public repo / no implementation" assumption, and (c) a claim that something is fake or impossible that nobody fetched either. A 2-minute reconnaissance can collapse a multi-day "reimplement" into a port. Cousin of [[read-authoritative-source-fully]] (that's reading the governing source fully; this is verifying an external artifact EXISTS as claimed). Pointer: [[betaedit-official-repo]].
