---
name: infranodus-standing-approval
description: InfraNodus approved for all work (2026-10-08); allow rule mcp__infranodus is in settings. Send scrubbed prose only; treat its gaps as leads
metadata:
  type: feedback
---
Operator, 2026-10-08: "I approve the use of InfraNodus for all work now and forever." This covers sending CORPUS/research prose to the hosted InfraNodus service (graphs land in their account). Strip credentials, emails and home paths first; prose only, no code.

**Why:** they want InfraNodus gap audits as a candidate-question source (the math lab's step 4, CORPUS/60) and for CORPUS audits.

**How to apply:** call the `mcp__infranodus__*` tools directly; the allow rule `"mcp__infranodus"` is in `~/.claude/settings.json` permissions.allow (added by the operator 2026-10-08 ~19:45 after the auto-mode classifier had refused three calls as "Data Exfiltration"). If a call is refused again, don't retry in variant forms — the fix is on the operator's side. First trial (results/mathlab_staging/infranodus_trial/SUMMARY.md): its generated questions restated known C10 results; one gap (editing ↔ oracle/adapter) pointed at an unexamined, offline-testable link. Use its gaps as pointers and read the files to sharpen them; outputs are leads, never CORPUS evidence ([[infranodus-discourse-lens-not-coverage-tool]]).
