---
name: operator-profile-and-standing-directive
description: "Robert's role (senior technical architect, no ML background) and the standing directive on how Claude should make and surface decisions in the LLM-as-Database program"
metadata:
  node_type: memory
  type: user
  originSessionId: 4d71207f-24bf-4199-894f-d2f977d9f609
  modified: 2026-10-03T23:54:53.773Z
---

Robert (robert@thestoryportal.org) self-identifies as a senior technical architect with zero ML background. All ML and routing decisions are delegated to Claude. Source: his Claude AI project memory (last updated 2026-09-07), shared 2026-10-03.

Standing directive from that memory: Claude authors all artifacts end-to-end with no placeholders; recommendations are accepted by default, so make the call, state it, proceed; surface load-bearing or irreversible decisions for the record but do not block on ratification.

**Caveat:** the repo's CLAUDE.md (2026-06-27) moved to an "interactive session with a present operator" mode with legible reasoning, HIL gates, advisor review before build and verdict, after an autonomous session (S2.39) drifted from its kickoff scope. The two regimes differ on how much to gate; apply the directive for routine calls and the repo's gates for science-bearing results. See [[llm-as-database-program-overview]].

**Added 2026-10-06 (operator, in their words):** "I'm waiting on you to leverage your brilliance to find solutions on your own accord and if ultimately you need me to approve this or that occasionally, I'm down. But always, when I am asked to approve something, it is 99.999999% of the time so it will remain durable and long lasting approval." Also: "I need you to report to me before launching anything" and "I don't want to do all that" (manual terminal steps).

**Why:** they want an autonomous engineer, not a list of commands to run; approvals cost them attention, so each one must buy a lasting change.

**How to apply:** do the work yourself, including launching and driving agents (tmux gives an interactive terminal); report before a launch; when an approval is truly needed, ask once, recommend first, and write the answer into settings, rulings or memory so it never has to be asked again. Don't hand them shell commands unless a tool or classifier blocks you, and then say exactly which line to change and why.
