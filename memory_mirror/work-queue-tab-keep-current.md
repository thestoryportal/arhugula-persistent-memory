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

**Live since 2026-10-11 (MAESTRO31):** tab 8 installed; after a code change restart ONLY it: `tmux -L default respawn-window -k -t '=dashboard:queue' "/usr/bin/python3 '<worktree>/tools/dashboard_queue.py'"`. The launch line must stay exactly `/usr/bin/python3 <path>` (no `-B`): the GPU-gate exemption matches that command, and Q3 halted when a brief's "use /usr/bin/python3 -B" was read as applying to the launch — in briefs, scope `-B` to tests/renders. The frame fits the pane height (header + Needs you always shown, rest one line each) and numbers follow the on-screen order (operator, 2026-10-11).

**Trap (MAESTRO34, 2026-10-11):** removing a finished item breaks the whole tab when another item still names it in `depends_on` (`parse_queue`: "no queue item has id …"), and `needs_from_you` must be a list (`[]`), never null. Before dropping items, clear every `depends_on` that references them, then check `parse_queue(open('docs/program_state.json').read())` returns a `Queue`.

**Trap (MAESTRO38, 2026-10-11):** `qset.py` sets fields wholesale, so a `notes` patch REPLACES the item's plain-language history. To add a note, read the current list and write old + new with a short python edit (as `a1aed84e` did), never `qset <id> '{"notes":[...]}'`.

**Trap (MAESTRO69, 2026-10-12):** `docs/program_state.json` is `json.dumps(d, indent=2, ensure_ascii=False) + "\n"`. Rewriting it with `indent=1` turned a one-note edit into an 847-line diff. Assert the round-trip equals the original bytes before editing.
