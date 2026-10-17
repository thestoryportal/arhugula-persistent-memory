# Operator ruling: multi-agent eval planning pattern (2026-10-17, chat, verbatim)

"Work with the eval agents in parallel TMUX sessions where youand these agents are able to communicate, ask/answer questions, debate  with relevant invoked skills to plan with. Of course all context for phase 1 clearly understood by them as well as ICM clearly understood by them. ICM skills can be invoked with other agents to plan. I suggest spawning Fable and Astra medium thinking on both for these agents to guide the planning. If 3rd or 4th agents with skills are launched in TMUX sessions of their own run Opus 5.5 and Sol 6.1 on High thinkking for those. You remain Orchestrator, the great MAESTRO!!!!!!!!!!

Continue with your track and once you arrive at the multi agent skilled expert planing phase the above is the pattern to use. NOTE: when you launch this pattern you will please send me the individual tmux command line commands ot use in order to have observability into it."

## MAESTRO reading
- Applies at the eval-planning step: after MAESTRO grounding and after the operator reads the planning prompt.
- Each planner runs in its own tmux session. Planners 1-2: Fable and Astra, medium effort. Planners 3-4, if launched: Opus 5.5 and Sol 6.1, high effort.
- Planners invoke the eval skills and the ICM skills (`icm-architect`, `icm-workspace`) themselves. MAESTRO orchestrates; it does not plan in its own session.
- Planners and MAESTRO talk to each other: questions, answers, debate. The channel is set at launch.
- At launch, MAESTRO sends the operator one `tmux attach` command per session.
- Phase 1 context and ICM must be clear to every planner.

## Operator, same day: what the evals evaluate (verbatim)
"Our repo is INDEED an ICM Architected repo and build form the workspace context. And these evaluations are specifically being designed to evaluate how the current ICM architecture is implemented and how agents operate in it in order to optimize the ICM architecture for our builder/reviewers/testers/orchestrator workflow, which is one narrow use of this ICM repo - our roster is framed specifically around this."

MAESTRO reading: the repo is an ICM in the `icm-architect` forms (signpost `CLAUDE.md`, per-folder `CONTEXT.md` contracts, `map/` system map, `_templates/`, generated `_index/`). The `icm-workspace` linter detects only `stages/` trees, so it refuses this repo; its five-layer model and patterns still apply. The evaluated object is the ICM as built plus agent behaviour in it, for the belt roster.
