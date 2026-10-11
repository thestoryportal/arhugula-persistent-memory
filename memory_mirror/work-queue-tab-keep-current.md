---
name: work-queue-tab-keep-current
description: The dashboard queue tab reads docs/program_state.json work_queue; MAESTRO updates it at every builder turn end with qset.py
metadata:
  type: project
---

Operator, 2026-10-11: a dedicated tmux tab listing current and all queued work in plain words, readable on the iPhone (Termius), "dynamically updated so it is never stale".

**Design (MAESTRO30):** the queue lives in ONE place, `docs/program_state.json` key `work_queue` (items in priority order: plain title/summary, state running|needs_you|in_review|ready|blocked, who, session, started, estimate {low_min, high_min, set}, depends_on, blocked_by, needs_from_you, notes). `tools/dashboard_queue.py` renders it (stdlib, Python 3.9, so the GPU-gate exemption at tools/c10w_p2_gate.py:35 covers it) and adds live-detected work (codex* tmux sessions, Astra `codex exec`, live experiment runs) on top, so running work shows even before it is described.

**Why:** the hand-written part goes stale unless someone owns it; the tab shows "queue edited N min ago" and flags >3 h.

**How to apply:** at every builder turn end (the watcher's "finished turn" line now says "update docs/program_state.json work_queue") and every state change, run `python3 ~/.claude/jobs/8ac4cacf/tmp/qset.py <id> '<json patch>'` from the worktree (stamps `edited`); remove finished items; commit with the next commit. Open on the phone: `tmux new-session -t dashboard \; set destroy-unattached on \; select-window -t queue`. Related: [[context-management-every-session]], [[tmux-kill-session-exact-name]].
