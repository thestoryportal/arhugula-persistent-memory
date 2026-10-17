# Roots and roles
Part of the tickets guide. Router: `_system/governance/TICKETS.md`. Roots (L, M, S, W, TD, MEM, HO): `00-roots-and-roles.md`.

## Roots and names

Every path in this guide (`TICKETS.md` and `tickets/`) is written from one of these roots. Paste the preamble before running a command from this guide:

```sh
L=/Volumes/memit/corpus-consolidation-toolkit/workspace/runs/20261013-overnight/G-build/LEAN
M=/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory
S=/Users/robertrhu/.claude/skills/atomic-ticketizer
```

- `L` = the LEAN folder: workflow tools (`L/tools`), ticket folders, staged MAESTRO steps.
- `M` = the main checkout on master (MAESTRO's working copy and cwd).
- `S` = the atomic-ticketizer skill. `/Users/robertrhu/.codex/skills/atomic-ticketizer` is a symlink to it, so Claude (`/atomic-ticketizer`) and Codex (`$atomic-ticketizer`) read one copy (S/SKILL.md:100). The skill reads S/agents/openai.yaml for its Codex interface.
- `W` = `L/w1opt`, the folder of the tool steps 301-327 and of the staging area.
- TD = one ticket folder: PLAN.md, tickets/, reviews/, ledger.tsv, the briefs, METRICS.md. In a command, put the folder's absolute path where TD appears. Examples: `L/w1opt/followup-318` (current), `L/w1opt`, `L/part2` (Part 2 wave 1), `L/recut` (ICM v2.1 recut).
- `<T>` = a ticket id (T318) = its plan step number. Branch `tk/<T>`, lane `/Volumes/memit/llmdb-lanes/tk-<T>`.
- MEM = /Users/robertrhu/.claude/projects/-Volumes-memit-llm-database-poc-mirror-arhugula-persistent-memory/memory. HO = /Volumes/memit/corpus-consolidation-toolkit/workspace/runs/20261013T114331Z-2ec28dcb/icm-v2 (handoffs HANDOFF-STEP50 through STEP59).

The tools stay where they are. `L/tools` and the skill are outside every repo and not version-controlled, by operator decision (2026-10-16, stopping a move into the repo: "Is any of this necessary?"). Durable means, in the operator's words, "the workflow that we are running with those skills/tools are clearly known through the ICM repo structure for agents to leverage when relevant": CLAUDE.md routing → `TICKETS.md` → `tickets/` → the absolute paths above. Recovery is the `.bak-*` backups and install_staged.sh. Do not propose moving L/tools or the skill into the repo [G1].

## Who does what

- Operator: approves a plan (the `Approved:` line), starts or pauses waves, grants allow rules. Wave 2 (T204 T205 T217 T271 T209 T218 T210 T213 T215) stays paused until the operator says start [R52].
- MAESTRO: writes plans and briefs, cuts, makes lanes, dispatches, verifies builder work itself, ships, rules on every NO-GO, alone writes allow files, runs the train, stages and installs MAESTRO steps. Only MAESTRO merges, and only through the gate.
- Builder or fixer: one fresh agent per ticket or fix round. Works only in its lane, writes only the ticket's `write` list, never commits, pushes or merges.
- Pre-review: `L/tools/prereview.sh`, model gpt-6.1-sol at medium effort, the same packet as Astra plus the fault_kit attacks.
- Astra: `L/tools/astra.sh`, model gpt-6-astra at high effort, one binding round, only on `astra: true` tickets.

