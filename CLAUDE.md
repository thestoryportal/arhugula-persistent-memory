# LLM-as-Database research program: routing

This repo runs the "LLM-as-Database" research program on the operator's MacBook M3 Pro (Apple MPS, no CUDA). Its goal is the F1 determination: prove or falsify that the spec is implementable, falsification-first.
MAESTRO (Claude, the orchestrator) and the builders (Codex and Claude) all read this file. `AGENTS.md` and `routing.md` are generated copies. Edit only `CLAUDE.md`.

These rules OVERRIDE default behavior. Correctness beats completion: "A halted session with clean diagnostic state is a SUCCESS." (`_system/governance/DISCIPLINE.md`, prime directive)

This file is a signpost. It does not contain the rules. If you think "I know this rule, I do not need to open the file", that is the moment to open the file. A rule that you apply from memory drifts, and the drift is silent.

Context directive (operator, binding): "Do not forget to manage context usage for yours and every team session you are orchestrating. Memento provides some tools to assist with this." / "This context directive must be made durable through any and all handoffs." Home: `_system/governance/OPERATING-MODEL.md` § Context management.

## Start here

Read `CONTEXT.md` (the umbrella). Then read the one folder `CONTEXT.md` that your task needs. Do not read the whole tree.

## What do I read now?

| Moment | Read first |
|---|---|
| You continue the program, or you need "what is next" | `program/CONTEXT.md` |
| You run or read an experiment | `experiments/CONTEXT.md` |
| You change code | `map/CLAUDE.md` (the catalog of `code/`) |
| You plan an experiment, a hypothesis or a decision | `knowledge/specs/SPEC_E2E_GROUND_TRUTH.md` (find its layer in §B first) |
| You start a session, or before any dispatch or run | `_system/governance/DISCIPLINE.md` (correctness gates) |
| A run fails, a gate misses, or you must halt | `_system/governance/DISCIPLINE.md` (halt discipline) |
| You close an experiment or a decision | `_system/governance/DISCIPLINE.md` (close-out gate) |
| You start a session or any non-trivial action, orchestrate a team, work in a worktree, or write a handoff | `_system/governance/OPERATING-MODEL.md` |
| You work as a Codex builder, or you need a Codex tool | `_system/governance/CODEX.md` |
| Before any merge | `_system/governance/MERGING.md` |
| You plan, cut, build, review, ship or land an atomic ticket, or change its tools | `_system/governance/TICKETS.md` |
| Before a bulk write, a download or a deletion, or when you close work that wrote files | `_system/governance/STORAGE.md` |
| You re-run a known arm, or trace a claim to its artifact | `_system/governance/REPRODUCIBILITY.md` |
| Before an unattended run of `code/lab/runners/autonomy_driver.py` | `_system/governance/AUTONOMY.md` |
| You need the shape of the whole workflow | `_system/governance/WORKFLOWS_OVERVIEW.md` |
| You start work that is like past work | `_system/memory/MEMORY.md` |
| An old path does not resolve | `_index/path-map.tsv`, or `LLMDB_ROOT=$PWD .venv/bin/python code/state/resolve_path.py <old-path>` |

## Where things live

| Folder guide | What the folder holds |
|---|---|
| `program/CONTEXT.md` | Program state, the runbook, checkpoints and sessions |
| `experiments/CONTEXT.md` | One record per experiment |
| `projects/CONTEXT.md` | In-flight work-queue items only |
| `evidence/CONTEXT.md` | The attested ledger: CORPUS entries and manifests |
| `knowledge/CONTEXT.md` | Findings, analyses, model profiles, specs, research and papers |
| `code/CONTEXT.md` | All code, grouped by job |
| `map/CONTEXT.md` | The system map of `code/`: catalog, noun index and inventory (cards, process records and an effects index come after v2) |
| `data/CONTEXT.md` | External shared inputs (caches, covariance). They stay out of git. |
| `_system/CONTEXT.md` | The governance rules and the agent memory mirror |
| `_templates/CONTEXT.md` | The stamps for a new experiment or project |
| `_index/CONTEXT.md` | Generated indexes, written by `code/state/build_index.py` |
| `_archive/CONTEXT.md` | Retired material: pod era, old projects, old backups |

A top-level folder that is not in this table is from the old layout. Find its new home in `_index/path-map.tsv`.

The rules live in `_system/governance/`. Read the file for your moment before you act.
