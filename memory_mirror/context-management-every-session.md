---
name: context-management-every-session
description: BINDING operator directive (2026-10-09) — manage context for MAESTRO and every orchestrated session (Memento for Claude; handoff + fresh successor for Codex); must survive every handoff
metadata:
  type: feedback
---

Operator, 2026-10-09 ~14:30 MDT: "Do not forget to manage context usage for yours and every team session you are orchestrating. Memento provides some tools to assist with this." Then: "This context directive must be made durable through any and all handoffs."

**Why:** long sessions drift once context fills (earlier directive: never let a session near a full-window compaction — drift and hallucination). Orchestration multiplies the risk across 4–5 sessions.

**How to apply (every orchestrator turn, every handoff):**
- **MAESTRO (Claude):** Memento plugin at `/Users/robertrhu/.claude/plugins/cache/memento/memento/0.7.0/skills/`. `ceiling/bin/ceiling show` (this project: 250,000-token ceiling, enforced by the Stop hook — do not estimate your own count). Run `message-in-a-bottle/bin/finalize-session '<handoff>'` (no `--reset`) at every finished unit of work; use `--reset compact|clear` only when the hook says the ceiling is reached. Every handoff message MUST restate this directive.
- **Codex sessions:** check `Context N% left` in each pane's status line whenever routing work. ≤ ~30% left before a large task, or ≤ ~20% at any time → have it write a handoff note into its report, then start a fresh successor (`start_<name>.sh`, new tmux session) with the handoff + this directive in its prompt; retire the old session once its work is committed. Give small fix rounds to a session only if it has the room.
- **Idle finished sessions:** close them (`tmux kill-session`) once their work is committed — transcripts persist.
- **Every successor prompt / checkpoint handoff / finalize-session message carries this directive verbatim.** Related: [[operator-overnight-autonomy-2026-10-06]], [[never-idle-arm-completion-watch]].

**Gap found 2026-10-10:** the memento plugin is NOT in `enabledPlugins` (~/.claude/settings.json), so its Stop-hook ceiling never fired — this session reached ~700k tokens with a 250k ceiling. Until the operator enables it, MAESTRO must reset itself at clean boundaries via `finalize-session --reset clear '<handoff>'` (by path), never just record handoffs and run on.
