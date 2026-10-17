# Charter: agent workflow program (opened 2026-10-17, MAESTRO)

Goal: bring every agent that builds and lands tickets, MAESTRO included, to an ideal, measured workflow: each agent gets exactly the context, governance, tools and skills its task needs, with no drift. Phase 1 is approved; Phases 2-6 wait for the operator.

## Operator, verbatim (2026-10-17, chat, in order)

**The request.** "Before we launch wave 2 I would like to evaluate exactly how you, MAESTRO, move through the ICM repo workspace in order to precisely gather all required context, governance, tools, etc and optimize that flow so it is 100% durable and accurate. I also want to evaluate how builers, reviewers and other agent use cases for all of our forward ticket implemntations do the same to ensure they also have 100% context and governance for their tasks with perfect precision. The ICM approach is designed for agents to move through workflows in the repo with perfect step by step clarity without drifting. Upon a brief human review I beleive there are some drift point, gaps and ambiguity. Toward that end, it poses the question of how to manage memory files per ICM architecture as these artifacts are currently structured in the ICM architected repo - there are also ~/.claude session, conversation and memory files that we can leverage for very grounded and semi-persistent agent memory by developing an architecture, framework and discipline for moving these into the ICM repo context architecture. Memory stores in Claude and Codex very quickly become useless due to the lack of a map connecting them to what is relevant at any given moment or for a particular task. We have built the parallel lane atomic ticket system that is hopefully, and I think likely, quite efficient for workflows. But without the context grounding, informing, governing and driving that system it will never perform optimally."

**Then:** "Yes, an audit. But it is actually more evals"

**The method.** "Stop...we need to think this through more intelligently. Don't just rush into a fast seat of your pants design. First, we need to clearly outline every agent that will be working on the next sets of tickets, including yourself, with exactly how each operates in the workflow, what context they require as well as all additional context that will maximize performance exponentially, what tools, what skills, what governance, what documents....and on and on and on. We need to have a very clear picture of what the ideal highly optimized workflow is for every agent use case. From there, we need to evaluate historically how those workflows across all agents involved performed and evaluate the differential between our intended highly optimized workflow and the historical findings. We can gather the historical and current baseline through stored historical history as well as evals to observe how agents currently perform. Then we evaluate and identify what in our existing repo architecture, context, governance, skills, tools, etc cause and/or contribute to this. We then very intelligently, precisely and comprehensively design and plan an approach for bringing workflow to 100% alignment with the intended highly optimized state. Once that is implemented we then write evals to test how agents operate, tracking performance metrics and data in a scientificly durable way and tweak based on the data, tweak evals, and optimize the workflow to our ideal state."

**Decisions and Phase 1 scope.** "1. ticket belt and lifecycle for now for build implementations like we are working on currently 2. Fable 3. I am open to a solid budget right now. [...] 3. Full transcripts, agreed. AND the context derived from them must be consolidated into a durable persistent state in the workflow and this must occur consistently so memory remains up to date and well formatteds and organized to serve as a core context for agents in the repo workflows.

Let's start with Phase 1 only for now - The Roster, role cards, ideal optimized high performance. I have a few concepts to consider and assess as part of phase 1:

1. What parts of the roster can be implemented deterministically with scripts in place of an agent? Where might a single file agent offer value and cost optimization? MAESTRO manages a large list of tasks, tools, authoring in your main session context window. Where might a subagent spawned with a perfectly suited model routing along with a skill invoked by MAESTRO to manage parts of the current work/task list optimize for more efficient orchestration, session window context token usage, error free orchestration, etc?

2. We need to identify all skills, tools, MCP, API, knowledge context, schemas, etc our team needs to perform at their hisgest ideal capabilites inside our highly optimized ideal workflows and repo. In addition, our ICM architecture must provide asurface and flow that is implemented with perfect precision and with flawless context engineering."

**Budget (same message, summarised; the operator's figures).** Open to a solid budget: about $250 "Cloud Computing credits"; Claude weekly usage (reset Monday 04:00, plus one extra weekly reset until 10/22); Codex about 76% weekly left, 63,000 credits, two weekly resets (Codex weekly reset 10/22 ~14:30). MAESTRO finding (claude-code-guide, Anthropic docs, 2026-10-17): no documented balance has that name. The closest is a Claude Code cloud-session promo credit (press reports: $250 Max, cloud sessions only, expiry about Nov 4; not verified on an Anthropic page). It does not pay for direct API calls. Claude Code CLI and subagents use the plan's weekly usage.

**Equip first.** "Slow down please...we need to write these evals to best practices for agentic evaluations. You need context and a tool or two:

This is an article from Anthropic: https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents

Two tools that are very useful for evals are Promtfoo as well as Marimo Notebooks which are equipped with two useful skills

We also have access to ArXiv MCP to surface current resarch for the most current and effective approaches.

We also have access to the anthropic skill creator which I believe connects to Vercel's skills.sh where we can install eval related skills. If skill builder doesn't connect there we can install the connection to it. This is a very reputable source for skills.

You need tools and context for properly setting up, running and measuring results of evals. Don't run phase 1 just as the base Claude agent/MAESTRO!!!!!. Equip yourself with what is needed for optimal performance.

Giddy up MAESTRO!!!!!!!!!"

## Decisions in force
- Scope: the ticket belt (plan → cut → lane → brief → build → fix → ship → train → land → release) and the session lifecycle (start, handoff, reset), for build tickets like waves 1-2. Science runs are out of scope for now.
- Decorrelated reviewer of the ideal role cards: Fable (before the operator).
- Transcripts: every full transcript (Claude session and subagent jsonl, Codex sessions) is a source. What is derived from them goes into the repo as durable, consolidated, organized context, kept current every session. Where the raw files live is a Phase 4 design point (the repo is pushed to GitHub).
- Wave 2 stays PAUSED until the operator says start.

## Phases (each ends in files here and an operator gate)
1. **Ideal (approved, in progress).** Roster; one role card per role (trigger, job, exit, inputs by path, required context with its one home, amplifying context, tools, skills, governance, documents, model and effort, context budget, sandbox, outputs and their reader, success metrics, known failure modes); the automation analysis (operator concept 1); the capability inventory (operator concept 2); the ICM surface and flow each role walks. Fable reviews, then the operator.
2. Baseline: history (ledger, METRICS, CI and git; transcripts; review files and rulings; handoffs and memory, ranked by trust) and evals of current behaviour.
3. Differential and causes: one gap table, each gap with a cause class, ranked by effect on the 15-minute goal and on correctness.
4. Design and plan, including the memory architecture and the transcript consolidation discipline.
5. Implement (on the belt).
6. Evals as a lasting instrument: versioned cases with cited ground truth at a pinned commit, pre-registered metrics, repeated trials, recorded config, mechanical or cross-family grading, controls, hold-out cases, an append-only results ledger, a rerun on every governance, tool or skill change.

## Phase 1 work plan
0. Equip (before any Phase 1 sweep): research digests in `drafts/research/` (briefs `brief/equip-*.md`): the Anthropic evals article, current arXiv research, promptfoo + marimo + local eval skills, skills.sh eval skills (vetted before install). The Phase 1 sweeps and cards are then built with that method and those tools.
1. Inventory, read-only, by sweep subagents into `drafts/inventory/`: `roles-today.md`, `capabilities.md`, `maestro-tasks.md`, `context-stores.md` (briefs in `brief/sweep-*.md`). MAESTRO checks each against its sources.
2. Draft `drafts/roster.md` and `drafts/roles/<role>.md` from the inventory, the operator's goals and the incident record; `drafts/automation.md` (concept 1); `drafts/capabilities-ideal.md` (concept 2); `drafts/surface-and-flow.md`.
3. Fable review into `reviews/`; MAESTRO rulings; operator gate.

## Prior work to build on, not repeat
- `projects/context-audit/` (2026-10-12, paused): seven checkers audited CLAUDE.md, AGENTS.md, the three memory stores, hook text and read-first documents; its synthesis and root cause are in its `receipts/` (old paths via `_index/path-map.tsv`). Phase 2 evidence.
- `_system/governance/tickets/gaps.md` (G1-G41) and `L/w1opt/staged/tickets-doc/INVENTORY.md` (the 2026-10-16 component sweep).
- `HO/HANDOFF-STEP*.md`, `TD/ledger.tsv`, `TD/METRICS.md` (roots in `_system/governance/tickets/00-roots-and-roles.md`).

## Context directive (binding; carry through every handoff)
"Do not forget to manage context usage for yours and every team session you are orchestrating. Memento provides some tools to assist with this." / "This context directive must be made durable through any and all handoffs."
