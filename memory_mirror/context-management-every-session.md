---
name: context-management-every-session
description: "BINDING (operator 2026-10-09): manage context for MAESTRO and every orchestrated session (Memento for Claude; handoff + fresh successor for Codex)"
metadata:
  type: feedback
---

Operator, 2026-10-09 ~14:30 MDT: "Do not forget to manage context usage for yours and every team session you are orchestrating. Memento provides some tools to assist with this." Then: "This context directive must be made durable through any and all handoffs."

**Why:** long sessions drift once context fills (earlier directive: never let a session near a full-window compaction — drift and hallucination). Orchestration multiplies the risk across 4–5 sessions.

**How to apply (every orchestrator turn, every handoff):**
- **MAESTRO (Claude):** Memento plugin at `/Users/robertrhu/.claude/plugins/cache/memento/memento/0.7.0/skills/`. `ceiling/bin/ceiling show` (this project: 300,000-token ceiling, raised from 250,000 by the operator 2026-10-10 ~21:20Z; set with `ceiling set project 300000`; enforced by the Stop hook — do not estimate your own count). Run `message-in-a-bottle/bin/finalize-session '<handoff>'` (no `--reset`) at every finished unit of work; use `--reset compact|clear` only when the hook says the ceiling is reached. Every handoff message MUST restate this directive.
- **Codex sessions:** check `Context N% left` in each pane's status line whenever routing work. ≤ ~30% left before a large task, or ≤ ~20% at any time → have it write a handoff note into its report, then start a fresh successor (`start_<name>.sh`, new tmux session; these launchers live in the orchestrating session's scratch dir, e.g. `~/.claude/jobs/<id>/tmp/start_codex*.sh`, not in `tools/`) with the handoff + this directive in its prompt; retire the old session once its work is committed. Give small fix rounds to a session only if it has the room.
- **Idle finished sessions:** close them (`tmux kill-session`) once their work is committed — transcripts persist.
- **Every successor prompt / checkpoint handoff / finalize-session message carries this directive verbatim.** Related: [[operator-overnight-autonomy-2026-10-06]], [[never-idle-arm-completion-watch]].

**Known gap (checked 2026-10-10):** memento is NOT in `enabledPlugins` (`~/.claude/settings.json:110-115`), so its Stop-hook ceiling never fires. Until the operator enables it, MAESTRO resets itself at clean boundaries via `finalize-session --reset clear '<handoff>'` (by path) rather than only recording handoffs and running on.

**Thresholds revised (operator correction 2026-10-10 ~09:10Z, after codexmb7 auto-compacted):** one Codex turn burned 37% → compaction, and a fresh successor spent 50% just reading a large handoff. So: hand a NEW task only to a session with ≥ 60% left — otherwise a fresh successor; tell a session to stop and hand off at ≤ 40%; any "Context compacted" line → handoff + successor immediately. Keep successor briefs lean (point to the handoff, don't make them re-read whole reports). MAESTRO: measure, never guess — read the last `usage` in `~/.claude/projects/<proj>/<session-id>.jsonl` (input + cache_read + cache_creation); `ceiling show` prints only the limit. MAESTRO5 reached ~240k/250k unnoticed. Check every ~10 turns; reset by ~300k (operator 2026-10-10 ~21:20Z: "raise the maestro context ceiling to 300k, instead of 180k"). The watcher (`watch.sh` in the MAESTRO scratchpad) emits CONTEXT steps below 60%, HANDOFF-NOW below 40%, and COMPACTED.
