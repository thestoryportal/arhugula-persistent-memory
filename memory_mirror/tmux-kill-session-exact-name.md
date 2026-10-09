---
name: tmux-kill-session-exact-name
description: tmux targets prefix-match — `kill-session -t codexy` killed live codexy2; always use `-t =name` for kill-session and verify with tmux ls first
metadata:
  type: feedback
---

2026-10-09 ~14:35 MDT: closing idle Codex sessions, `tmux kill-session -t codexy` killed **codexy2** (live, mid-task) because `codexy` no longer existed and tmux fell back to prefix matching. Earlier `capture-pane -t codexy:` had likewise shown codexy2's pane, so the "idle" reading was wrong. No work lost (repin had not started; tree matched 93080f5), successor codexy3 started.

**Why:** tmux target resolution is exact-then-prefix; a missing exact name silently selects another session.

**How to apply:** for destructive tmux ops use the exact form `tmux kill-session -t '=name'`; run `tmux ls` first and act only on names it lists; never infer a session's state from a capture of a name not in `tmux ls`. (capture-pane keeps the `'name:'` form; verify the name exists first.) Related: [[context-management-every-session]].
