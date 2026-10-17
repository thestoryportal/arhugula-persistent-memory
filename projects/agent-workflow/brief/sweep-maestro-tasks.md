# Sweep brief: MAESTRO tasks (output: P/drafts/inventory/maestro-tasks.md)

Read M/projects/agent-workflow/brief/sweep-common.md first. Its roots, hard rules, evidence rules and output form apply here.

## Task
List every task that MAESTRO (the orchestrating Claude Code session) performs on the ticket belt and in the session lifecycle TODAY. For each task, record how it is done: by a script, partly by a script, by hand in MAESTRO's own context, or by a subagent. Also record what MAESTRO reads to do it and what governs it. This inventory feeds the operator's concept 1 (verbatim, 2026-10-17): "What parts of the roster can be implemented deterministically with scripts in place of an agent? Where might a single file agent offer value and cost optimization? MAESTRO manages a large list of tasks, tools, authoring in your main session context window. Where might a subagent spawned with a perfectly suited model routing along with a skill invoked by MAESTRO to manage parts of the current work/task list optimize for more efficient orchestration, session window context token usage, error free orchestration, etc?" You give the facts only. MAESTRO answers the question.

## Sources
- M/_system/governance/TICKETS.md; M/_system/governance/tickets/*.md (all of them; together about 380 lines); M/_system/governance/OPERATING-MODEL.md; M/_system/governance/MERGING.md; M/_system/governance/STORAGE.md; the sections of M/_system/governance/DISCIPLINE.md that name MAESTRO or the belt (grep first).
- What MAESTRO actually did: HO/HANDOFF-STEP70.md through the latest; TD/ledger.tsv; TD/METRICS.md; W/ledger.tsv.
- MAESTRO duties recorded in memory: MEM/MEMORY.md (index lines) and the MEM files they point to, only where a line names a MAESTRO duty. Also M/_system/memory/MEMORY.md, the repo mirror: record whether it matches MEM/MEMORY.md (`cmp`, or `diff | head -20`).
- Subagent use: the count of subagent transcripts per MAESTRO session (`ls ~/.claude/projects/-Volumes-memit-llm-database-poc-mirror-arhugula-persistent-memory/*/subagents/ | wc -l` or similar), and P/brief/ as the current example.

## Sections
1. `## Task table`: one row per task. Columns: id (MT01...) | stage | trigger | what MAESTRO does (one line) | how today: `SCRIPT <path>`, `PARTIAL <script> + <manual steps>`, `MANUAL`, or `SUBAGENT <how dispatched>` | inputs MAESTRO reads (paths, with `wc -c` bytes) | outputs | judgment required (quote the governing line that asks MAESTRO to decide, with path:line; or `none in docs`, with the doc line that gives the fixed procedure) | frequency (count from the ledger or handoffs, with the command) | governing rules (path:line, ENFORCED or INTERPRETED) | route (the ICM hops from M/CLAUDE.md to the governing doc; `OFF-ROUTE` when the only source is a handoff or a memory file) | incidents (G-ids or MEM file names).
2. `## Session start load`: the files that the harness loads into a MAESTRO session and the files that M/CLAUDE.md itself names for a session start. Columns: path | bytes | loaded by (harness, or the M/CLAUDE.md line) | authority class.
3. `## Model, effort and context management today`: MAESTRO's model and effort setting (cite the config or transcript `model` field, from `head -c 2000`); the context ceiling and the watcher (cite OPERATING-MODEL.md and context_watch.py usage text); the reset path (Memento finalize-session; cite).
4. `## Incidents (uncoded)`: per sweep-common rule 5, limited to incidents where MAESTRO acted. At most 60 rows.

## Acceptance
Every stage in TICKETS.md and tickets/01-plan.md through 11-maestro-steps.md, plus close-out.md, has at least one task row, or a line that says the stage has no MAESTRO task, with the citation. Every "how today" value names a script path, or quotes the doc line that makes it manual.

## The trap in this sweep
You will reach a task like "write the brief" and think "this is obviously scriptable" or "this needs judgment". Do not write either. Record what the docs say and what the scripts do. A judgment column value is a quoted doc line, never your opinion. If no line asks for a decision, write `none in docs`.
