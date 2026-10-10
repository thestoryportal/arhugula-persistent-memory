---
name: operator-profile-and-standing-directive
description: Robert's role (senior technical architect, no ML background) and the standing directive on how Claude makes and surfaces decisions in the program
metadata:
  type: user
---

Robert (robert@thestoryportal.org) self-identifies as a senior technical architect with zero ML background. All ML and routing decisions are delegated to Claude. Source: his Claude AI project memory (last updated 2026-09-07), shared 2026-10-03.

Standing directive from that memory: Claude authors all artifacts end-to-end with no placeholders; recommendations are accepted by default, so make the call, state it, proceed; surface load-bearing or irreversible decisions for the record but do not block on ratification.

**How this sits with the repo's gates:** since 2026-10-06/07 the operator's rulings make the program's recommendations rulings and route open questions to the team (Astra + advisor), not to him ([[operator-overnight-autonomy-2026-10-06]]). What still goes to him is listed in CLAUDE.md:15 and [[operator-decision-scope]]: go/no-go and scope, frozen-prereg amendments, storage/spend forks, deletions, credentials. The repo's science gates (advisor and Astra review before build and verdict, the LAWs) apply unchanged. See [[llm-as-database-program-overview]].

**Added 2026-10-06 (operator, in their words):** "I'm waiting on you to leverage your brilliance to find solutions on your own accord and if ultimately you need me to approve this or that occasionally, I'm down. But always, when I am asked to approve something, it is 99.999999% of the time so it will remain durable and long lasting approval." Also: "I need you to report to me before launching anything" and "I don't want to do all that" (manual terminal steps).

**Why:** they want an autonomous engineer, not a list of commands to run; approvals cost them attention, so each one must buy a lasting change. Their pointed challenges ("are you ABSOLUTELY certain?", "have you read the spec end-to-end?") have repeatedly caught real over-claims — treat them as signal to re-search, not to re-defend.

**How to apply:** do the work yourself, including launching and driving agents (tmux gives an interactive terminal); report before a launch; when an approval is truly needed, ask once, recommend first, and write the answer into settings, rulings or memory so it never has to be asked again. Don't hand them shell commands unless a tool or classifier blocks you, and then say exactly which line to change and why.
