# Rules for every Phase 1 inventory sweep (read this first, then your own brief)

You are one of four read-only sweeps for the agent-workflow program. Purpose (operator, 2026-10-17, verbatim): "we need to clearly outline every agent that will be working on the next sets of tickets, including yourself, with exactly how each operates in the workflow, what context they require as well as all additional context that will maximize performance exponentially, what tools, what skills, what governance, what documents". Your job is the FACTUAL part only: what exists and how it works TODAY. You do not design the ideal and you do not judge quality; MAESTRO does that from your file.

## Roots
- M = /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory (the ICM repo; master)
- L = /Volumes/memit/corpus-consolidation-toolkit/workspace/runs/20261013-overnight/G-build/LEAN (ticket tools: L/tools/, L/land.sh)
- W = L/w1opt (plans, briefs, staged tool changes); TD = W/followup-327 (the latest plan: PLAN.md, tickets/, reviews/, ledger.tsv, METRICS.md); wave 2 tickets: L/part2/tickets/
- S = /Users/robertrhu/.claude/skills/atomic-ticketizer (the ticket skill: SKILL.md, references/worker.md, reviewer.md, prober.md, scripts/tickets.py)
- HO = /Volumes/memit/corpus-consolidation-toolkit/workspace/runs/20261013T114331Z-2ec28dcb/icm-v2 (HANDOFF-STEP*.md; latest HANDOFF-STEP71.md)
- MEM = /Users/robertrhu/.claude/projects/-Volumes-memit-llm-database-poc-mirror-arhugula-persistent-memory/memory (Claude auto-memory)
- The governance router: M/CLAUDE.md -> M/_system/governance/TICKETS.md -> M/_system/governance/tickets/*.md (00-roots-and-roles.md defines the roots and who does what).
- Codex home: ~/.codex (config.toml, AGENTS.md, skills/, memories/, rules/, sessions/). Claude home: ~/.claude (settings.json, CLAUDE.md, skills/, agents/, plugins/, projects/).

## Hard rules
- Read-only everywhere. Write ONLY your one output file under M/projects/agent-workflow/drafts/inventory/. No commits, no installs, no network, no edits, no running tests, ship.sh, train.sh, land.sh, codex or claude.
- Do not open or print secrets (tokens, keys, OAuth files, .env). If a config holds one, name the key, never the value.
- Do not read whole transcript files (*.jsonl): they are huge. Use `ls -la`, `wc -l`, `du -sh`, `head -c 2000` only.
- Every claim cites its source as `path:line` (or the exact command and its output for counts and sizes). A claim you cannot cite is marked UNVERIFIED and says why.
- Use exact paths with the root prefix (M/..., L/..., S/...). When a doc names a path that does not exist, record that as a finding (cite the doc line and your `ls` result).
- Report what IS. When two sources disagree (a doc says X, the script does Y), record both with citations under "Disagreements"; do not pick one.
- Context: keep your own window lean. Read headers, usage text and the sections you need; grep before you read; do not read a file over ~400 lines whole unless your brief says so.

## Output form
Markdown. First line: `# <title> (sweep, <date> UTC, read-only)`. Then the sections your brief names, then `## Disagreements`, `## Missing or dead paths`, `## UNVERIFIED`, `## Commands run` (each command, one line). Hard cap: 600 lines. Tables where your brief asks for them.

Bad output (do not do this): "Builders get good context from the brief template." (no citation, a judgment, not a fact). Good output: "Builder brief template names worker.md as the rule file (L/w1opt/brief-template.md:12); worker.md:10-11 requires the revert check."

When done, reply in at most 15 lines: the output path, its line count, and the three facts you think MAESTRO most needs.
