---
name: context-management-every-session
description: "BINDING (operator 2026-10-09): manage context for MAESTRO and every orchestrated session (Memento for Claude; handoff + fresh successor for Codex)"
metadata:
  type: feedback
---

Operator, 2026-10-09 ~14:30 MDT: "Do not forget to manage context usage for yours and every team session you are orchestrating. Memento provides some tools to assist with this." Then: "This context directive must be made durable through any and all handoffs."

**Why:** long sessions drift once context fills (earlier directive: never let a session near a full-window compaction — drift and hallucination). Orchestration multiplies the risk across 4–5 sessions.

**How to apply (every orchestrator turn, every handoff):**
- **MAESTRO (Claude):** Memento plugin at `/Users/robertrhu/.claude/plugins/cache/memento/memento/0.7.0/skills/`. `ceiling/bin/ceiling show` (this project: 250,000-token ceiling, enforced by the Stop hook — do not estimate your own count). Run `message-in-a-bottle/bin/finalize-session '<handoff>'` (no `--reset`) at every finished unit of work; use `--reset compact|clear` only when the hook says the ceiling is reached. Every handoff message MUST restate this directive.
- **Codex sessions:** check `Context N% left` in each pane's status line whenever routing work. ≤ ~30% left before a large task, or ≤ ~20% at any time → have it write a handoff note into its report, then start a fresh successor (`start_<name>.sh`, new tmux session; these launchers live in the orchestrating session's scratch dir, e.g. `~/.claude/jobs/<id>/tmp/start_codex*.sh`, not in `tools/`) with the handoff + this directive in its prompt; retire the old session once its work is committed. Give small fix rounds to a session only if it has the room.
- **Idle finished sessions:** close them (`tmux kill-session`) once their work is committed — transcripts persist.
- **Every successor prompt / checkpoint handoff / finalize-session message carries this directive verbatim.** Related: [[operator-overnight-autonomy-2026-10-06]], [[never-idle-arm-completion-watch]].

**Known gap (checked 2026-10-10):** memento is NOT in `enabledPlugins` (`~/.claude/settings.json:110-115`), so its Stop-hook ceiling never fires. Until the operator enables it, MAESTRO resets itself at clean boundaries via `finalize-session --reset clear '<handoff>'` (by path) rather than only recording handoffs and running on.
