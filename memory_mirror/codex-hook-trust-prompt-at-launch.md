---
name: codex-hook-trust-prompt-at-launch
description: A fresh Codex builder can stall at a "hooks are new or changed" trust prompt; check the pane ~20 s after launch and choose Continue without trusting
metadata:
  type: feedback
---

A freshly launched Codex session may stop before doing anything on "N hooks are new or changed … 1 Review / 2 Trust all / 3 Continue without trusting". It waits there silently, and a watcher that only looks for progress or context lines will not flag it.

**Why:** MAESTRO19 found MB24 parked on this prompt (2026-10-10). Choosing "Trust all" would grant hook trust on the operator's behalf, which is not MAESTRO's call.

**How to apply:** ~20 s after every `tmux new-session … start_codexmbNN.sh`, capture the pane. If the prompt is there, send `3` then Enter (continue without trusting). Then re-arm the Monitor. Related: [[context-management-every-session]], [[never-idle-arm-completion-watch]].
