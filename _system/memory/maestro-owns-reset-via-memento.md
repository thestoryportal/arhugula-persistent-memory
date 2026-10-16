---
name: maestro-owns-reset-via-memento
description: Operator 2026-10-16 durable governance: MAESTRO runs its own clear/reset and next-session handoff with Memento finalize-session; no operator /clear+paste
metadata:
  type: feedback
---

Operator ruling 2026-10-16 ~07:55 MDT, verbatim: "You manage your own session clear reset and next session handoff using Memento. This is durable governance."

**Why:** the operator should not have to type `/clear` and paste a kickoff line; at 303k MAESTRO had offered exactly that, and the operator answered with this ruling.

**How to apply:** at the context ceiling (~300k) or the end of a unit, write the handoff file, save learnings, then run `~/.claude/plugins/cache/memento/memento/0.7.0/skills/message-in-a-bottle/bin/finalize-session --reset clear -- 'Continue as MAESTRO. Read <handoff> first and follow it. ...'` and stop the turn (no text after). From the foreground tmux pane (maestro-icm3, `claude --permission-mode auto`) the tmux transport resets in place and keeps the mode. From a background job, follow [[memento-reset-from-bg-job-drops-permission-mode]] (Claude auto-memory, not _system/memory/). Do not hand the operator a paste line. Carry this ruling in every handoff with the context directive. Related: [[context-ceiling-measure-after-continuation]] (Claude auto-memory, not _system/memory/).
