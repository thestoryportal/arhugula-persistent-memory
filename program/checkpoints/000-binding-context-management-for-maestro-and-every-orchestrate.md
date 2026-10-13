# SESSION CHECKPOINT — Write-Engine Viability Determination

## ⭐ BINDING — context management for MAESTRO and every orchestrated session (operator, 2026-10-09; must survive every handoff)
"Do not forget to manage context usage for yours and every team session you are orchestrating. Memento provides some tools to assist with this." — "This context directive must be made durable through any and all handoffs." MAESTRO: Memento `ceiling show` (300k ceiling, raised from 250k by the operator 2026-10-10; MAESTRO resets by ~300k) + `finalize-session` handoff at every finished unit, `--reset` only when the hook fires. Codex: watch `Context N% left`; new task only at ≥60% left; ≤40% or any "Context compacted" → handoff note + fresh successor; close idle finished sessions. Every handoff (checkpoint, successor prompt, finalize-session message) restates this block. Full rule: memory `context-management-every-session.md`; Codex rule: AGENTS.md top section.

