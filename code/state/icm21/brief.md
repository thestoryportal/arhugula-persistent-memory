## Lane G (builder "Chisel V"): cut the ICM v2.1 build units for S1-S4 and S6

Lane folder: `N/G-build` (N = `/Volumes/memit/corpus-consolidation-toolkit/workspace/runs/20261013-overnight`). Tokens: `LANE-G-DONE`, `LANE-G-HANDOFF`.

Use the atomic-ticketizer skill EXACTLY as written in `/Volumes/memit/corpus-consolidation-toolkit/workspace/runs/20261012T114331Z-2ec28dcb/sdlc-atomic/v3` at commit `ee823a0` (SKILL.md, references/, scripts/tickets.py). It is not installed yet; run its helper from that path with `python3 -B`.

Admission input (approved): `N/A-icm21/IMPLEMENTATION_PLAN.md` with MAESTRO's `N/A-icm21/PLAN-RULING.md` (S1, S2, S3, S4, S6 approved; S5 HELD — do not cut S5), the approved `N/A-icm21/PRD.md`, `N/A-icm21/SPEC.md` + companions, and `N/A-icm21/RULING.md`. Root: the repo M = `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory`, base = origin/master as MAESTRO states in this brief's launch message. Build lanes run in external worktrees OUTSIDE the repo tree (ICM-R7), under `/Volumes/memit/llmdb-lanes/<ticket>`.

Operator build lifecycle (verbatim): "The idea with atomic units for builders is you can delegate multiple agents to each implement a unit, fast and with a small amount of context usage. Omce they implement a unit, it is reviewed and runs through the review implementatiion loop and once that loop is GREEN those agents are released and session window cleared so those agents can pick up the next unit. If acode crosses over into multiple agents units they complete, push and the code that crossed over is evaluated to determine which might be the better implementation and the winner is what lands with the merge." And: "Effective and durable but not bloated overcomplicated design and implementation".

Task: write the package to `N/G-build/package/` with a generator script next to it. Run `check` and `ready`; save outputs. Write `N/G-build/DISPATCH.md`: the ready set and the order, which tickets can run in parallel (disjoint writes), any declared competitions, each builder ticket's one-line goal and write files, and every gate (MAESTRO verify, Astra lane review, host proof, operator authority) with where it sits. Do NOT dispatch or implement. Do not edit M. Record any place the skill forced a guess in `N/G-build/SKILL-FRICTION.md`. End with `LANE-G-DONE` on its own line.
# Team brief: overnight design arc (2026-10-13). Common rules for every lane.

You are a builder on a team. MAESTRO (a Claude orchestrator) gave you this brief. MAESTRO verifies your work; Astra (a high-reasoning reviewer) reviews it; MAESTRO commits approved documents into the repo. Write all documents and reports in Simplified Technical English (STE): short sentences, active voice, one idea per sentence.

## Context

- Repo (READ ONLY for you): `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory` (call it M), branch master, ICM v2 layout merged 2026-10-13 (commit a95d6207). It runs the "LLM-as-Database" research program on the operator's MacBook M3 Pro. Start with `M/CLAUDE.md` and `M/CONTEXT.md`, then only the folder guides your lane needs.
- Governance to keep front of mind: `M/_system/governance/DISCIPLINE.md`, `OPERATING-MODEL.md`, `STORAGE.md`.
- Operator rulings that bind every lane (2026-10-13): "ICM is governance for our framework, repo, workflows and science now. It is how all repo and context is structured, implemented and managed moving forward, no exceptions." "Models are stored in a very clear directory structure /models/model-name/. And the stray data, findings, experiments, dovuments, ANYTHING in there are organized and logged our ICM governance." "Graft should be completely removed form our workflow now." "Ensure any work you completre does not overcomplicate or slowdown our'a or the team's work. Effective and durable but not bloated overcomplicated design and implementation."
- The documentation chain is: design → PRD → spec → implementation plan → atomic units. Its contracts are in `/Volumes/memit/corpus-consolidation-toolkit/workspace/runs/20261012T114331Z-2ec28dcb/sdlc-atomic/v3/references/sdlc.md`. Read it; your document must meet the contract for its phase.

## Hard limits

1. Do not edit, move or delete anything in M or anywhere outside your lane folder. Read only. No git writes anywhere.
2. No downloads, no installs, no model or GPU runs.
3. Do not type hashes; compute them. Cite every claim about the repo with file:line or the exact command and output.
4. The shell has `rtk` aliases that change `ls`, `tail`, `ps`. Use `/bin/ls`, `/usr/bin/tail`, `/bin/ps` and Python for measurements. `du` on big trees is slow: measure once, save the output in your lane folder.
5. Keep designs lean. Every rule, folder or tool you propose must name the failure it prevents or the job it does. If you cannot name one, cut it.

## Context management (BINDING, operator directive 2026-10-09; copy this section into every handoff you write)

Operator: "Do not forget to manage context usage for yours and every team session you are orchestrating. Memento provides some tools to assist with this." "This context directive must be made durable through any and all handoffs."

- Watch your own context. Start a new piece of work only at 60% or more context left.
- At 45% or less left, with a long step pending: stop, and write the handoff file.
- At 40% or less left, or at once on any "Context compacted": stop starting work. Write `HANDOFF.md` in your lane folder (what is done, what is in flight, exact file paths, the next step, open risks, and this section verbatim). Then reply with your lane's HANDOFF token.

## How to finish

Write `REPORT.md` in your lane folder: what you produced (paths, sha256), the evidence you gathered, open questions, and what is UNVERIFIED. End your final reply with your lane's DONE token on its own line.
