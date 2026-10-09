---
name: infranodus-standing-approval
description: Operator gave standing approval (2026-10-08) to send research text to InfraNodus; the auto-mode classifier still blocks it
metadata:
  type: feedback
---
Operator, 2026-10-08: "I approve the use of InfraNodus for all work now and forever." This covers sending CORPUS/research prose to the hosted InfraNodus service (graphs land in their account). Strip credentials, emails and home paths first; prose only, no code.

**Why:** they want InfraNodus gap audits as the candidate-question source for the math lab's step 4 and for CORPUS audits ([[math-lab]]).

**How to apply:** Claude Code's auto-mode classifier still refused it three times the same day: two subagent launches, then a direct mcp__infranodus__generate_research_questions call ("Data Exfiltration"), even after this approval. Earlier direct use (2026-06-23) had worked, most likely under a different permission mode. A scrubbed 15 KB C10 verdict extract is staged at results/mathlab_staging/infranodus_trial/c10_verdicts_extract.txt. Don't retry in variant forms. The unblock is on the operator's side: an allow rule `"mcp__infranodus"` in ~/.claude/settings.json permissions.allow (the denial message itself names this fix), or invoking `/infranodus-gap-audit` themselves.

**Resolved 2026-10-08 ~19:45:** operator added allow rule `mcp__infranodus` via /permissions; direct calls now pass. First trial (results/mathlab_staging/infranodus_trial/SUMMARY.md): its generated questions restated known C10 results; one gap (editing ↔ oracle/adapter) pointed at an unexamined, offline-testable link. Use its gaps as pointers, read the files to sharpen them.
