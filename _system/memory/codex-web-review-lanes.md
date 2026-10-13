---
name: codex-web-review-lanes
description: Codex web-research review lanes burn context ~15%/min and need --search only (no sandbox network); size lanes to ~10 items with a successor ready
metadata:
  type: feedback
---

2026-10-11 (MAESTRO46), operator's dashboard/skills/dataviz lists reviewed by five Codex lanes (`results/dashboard_integration_review_20261011/`).

1. **Launch with `codex --search` only.** Adding `-c sandbox_workspace_write.network_access=true` (plus curl fallback) to unattended `-a never` builders was refused by the Claude Code auto-mode classifier ("Create Unsafe Agents"). `--search` (model-side web search, sandbox stays offline) worked for every lane.
**Why:** an unattended agent with sandbox network is treated as unsafe; model-side search is enough for reading READMEs and SKILL.md pages.

2. **Web reading burns context fast.** Lanes fell 86% → 55% in ~2 minutes and one hit 40% in 5. Ten to thirteen items per lane finished in one session (or with one small successor) when the brief capped reads at "README/SKILL.md plus one more page" and told the agent to write "not opened" rather than guess.
**How to apply:** keep lanes ≤ ~12 items; generate successors with `~/.claude/jobs/8ac4cacf/tmp/mk_dir_successor.py <lane>` (new token LANE2, handoff2 file); include "if already finished, reply READY instead" in every stop message, because two lanes finished just as the stop arrived. Hand the cross-lane summary to a fresh Codex session, not MAESTRO, to save Claude context.

Related: [[codex-brief-handoff-file-narrow-reads]], [[context-management-every-session]].
