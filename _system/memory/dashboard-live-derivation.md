---
name: dashboard-live-derivation
description: Team dashboard NOW section is computed live; a pending operator ruling shows only if its runbook §5.2 status cell says "awaiting operator"
metadata:
  type: project
---
Since 2026-10-08 (commit after c5ef456): `tools/dashboard_live.py` derives the Science Report's NOW section on every report redraw (cadence owned by `tools/dashboard_report.py`) — runbook §5.2 rows whose **status cell** contains "awaiting operator" (shown as "! NEEDS YOUR RULING"), the GPU job (ps) or the newest `results/c10*_logs/*coordinator*.log` COORDINATOR_EXIT, Codex sessions whose tile is WORKING, running helper agents. `docs/c10_scoreboard.json` `current` is no longer rendered; brief/results/queue stay hand-written and get a red "predates" banner when a coordinator exit, HALT.json or CORPUS change is newer than its `updated`. Panes re-exec on any `tools/dashboard_*.py` change; the report rebuilds the team tab ~15 s after a tmux session starts or ends.

**Why:** the operator requires the dashboard to update "durably and instantly" by itself; hand-typed status went stale (Step 5 shown as queued after it halted).

**How to apply:** when a decision needs the operator, write "awaiting operator" in its §5.2 status cell, and change the status when ruled — that is what clears the line. Still update the scoreboard brief/results at every state change (the banner shows when you forget). Keep NOW symbols single-width (emoji like ⚙ ⚑ make tmux lines wrap and scroll the pane). Related: [[lab-view-and-live-telemetry]].

**Detection rules have ONE home (2026-10-08):** `tools/dashboard_live.py` holds `GPU_JOB_RE`, `script_call` (only python/bash/sh running a live-tree script counts; prompts quoting paths and temp-root selftest copies never do) and `BUSY_RE` (spinner, "Working (", Codex footer "· Working ·", slow-model menu). The tile, watcher, experiment tab, NOW section and bar.sh all use them; four separate drifted copies caused false "GPU idle/running", "finished" and "stopped after an error" alerts in one night. Never add a local copy.
