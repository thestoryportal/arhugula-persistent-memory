---
name: tmux-server-hang-dashboard
description: 2026-10-08 the shared tmux server hung (resize loop) and froze every session incl. the lead and Codex builds; dashboard must stay light on tmux
metadata:
  type: feedback
---
~02:16 2026-10-08 the single tmux server hosting program, all codex*, dashboard and helpers looped forever in resize_window → window_copy_resize → screen_redraw_get_visible_ranges. Trigger: a dashboard auto-rebuild switching three differently sized viewers at once while the new live dashboard made ~40 tmux calls every 2 s, with a pane in copy mode. Codex builds blocked at 0 % CPU writing to their panes; recovery needs `tmux kill-server`, which also kills the lead (Claude runs inside tmux), so only the operator can do it.

**Why:** everything shares one tmux server; dashboard load or resize thrash there stalls all science work.

**How to apply:** keep dashboard tmux reads cached (≥15 s) and few; never auto-rebuild or switch viewers' sessions programmatically; prefer one viewer size; test dashboard changes for tmux load before deploying. Codex builds survive a restart via `codex resume <flags> <rollout id> '<message>'` (the positional PROMPT delivers the restart note; no send-keys). Recovery lessons (02:30 restart): (1) find the build's id as the top-level `codex-tui` rollout whose subagents name it as parent_thread_id (`head -1 <rollout> | jq .payload.source`) — `codex exec` rollouts are reviews, and the handoff's first-guess id for codexviz2 was one (real id 01a11a55…); (2) each resume stops at '5 hooks need review' — answer 3 (continue without trusting; project hooks point at pod-era /workspace paths); (3) always target tmux sessions as `=name`: bare `-t dashboard` prefix-matches dashboard_new (fixed in team_dashboard.sh 89e08ac). In zsh `=name` expands as a command path, so run such tmux calls via bash -c. Related: [[dashboard-live-derivation]].
