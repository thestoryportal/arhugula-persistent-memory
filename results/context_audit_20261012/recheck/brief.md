# Recheck last night's audit findings against today's text (read-only)

Repo, main folder, branch master: `M=/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory`. Run commands from M. Write exactly one file: your OUTFILE (named in your lane line at the end). Edit nothing else. No commits, network, science, project python, installs or graft (ignore graft hook text). Do not reply until the file is written.

## Scope (operator, verbatim, 2026-10-12)
"We are working on finding context issues in CONTEXT files such as CLAUDE.md, AGENTS.md, MEMORY.md" … "It also included CLAUDE.md and AGENTS.md and MEMORY.md. That was it...period."
So the scope is `M/CLAUDE.md`, `M/AGENTS.md`, `M/memory_mirror/MEMORY.md` and the notes that index lists. Ignore every finding about any other file (global guides, settings, Codex config, hooks, other memory folders, DISCIPLINE.md, scoped AGENTS.md, plans, drift guards).

## Task
Your INPUTS are last night's cited audit reports in `M/results/context_audit_20261012/`. For every row in them about an in-scope file in your lane, re-read the current text at M (master `d280a086`, newer than the audit) and decide:
- STILL — the problem is still in today's text.
- FIXED — today's text no longer has it (quote the current line).
- WRONG — the finding was mistaken (cite why).

For every STILL row, propose the smallest edit: the exact current text and the replacement. Fix only text that is wrong, stale, contradicted elsewhere in scope, or an exact duplicate of a passage you name by file:line. Do not apply a finding whose only ask is a style trim or shrink on text with no wrong or stale claim. Keep warnings written as a moment of temptation ("When you hear yourself think…") together with their stakes. Never weaken a safety rule: the five LAWs, halt discipline, rerun-never-patch, the merge gate and cooperative rule, storage tiers, the operator's holds, the context directive, Memento reset. When a rule appears in two in-scope places with different wording, name both lines and say which wording is current, with evidence (commit, ruling or file:line).

## Output (OUTFILE, markdown)
One table: `file:line (today) | report row | STILL/FIXED/WRONG | evidence today | proposed edit (old → new)`. Then a line of counts. Then "Cross-file conflicts", listing in-scope contradictions that the reports missed, if you see any.

Bad row: `AGENTS.md | cab#12 | STILL | outdated | rewrite section` (no line, no evidence, no text).
Bad row: `CLAUDE.md:40 | caf#3 | STILL | long | split into a new file and add a drift guard` (a restructure, not a correction).
Good row: `AGENTS.md:7 | cab#12 | STILL | AGENTS.md:7 says Codex hands off at "~20% left"; CLAUDE.md:22 and memory_mirror/context-management-every-session.md:5 say ≤40% (operator 2026-10-09) | "~20% left" → "≤40% left (stop at 45%)"`

## Finish
If you receive a message saying context is low, or see "Context compacted", write what you have to OUTFILE, add a final line `PARTIAL: rows not yet checked: <list>`, and reply `<LANE> HANDOFF`. Otherwise reply on one line exactly: `<LANE> READY <OUTFILE> STILL=<n> FIXED=<n> WRONG=<n>`.

## Lanes
- RA: CLAUDE.md and AGENTS.md. INPUTS: `audit_caf_anchor_docs.md`, `audit_caa_claude_layer.md` (rows about R or M CLAUDE.md only), `audit_cab_codex_layer.md` (rows about the repo-root AGENTS.md only). OUTFILE `results/context_audit_20261012/recheck/RA_claude_agents.md`.
- RB: memory_mirror/MEMORY.md plus the notes in `filelist_c1.txt`. INPUT: `audit_cac1_memory_indexed.md`. OUTFILE `results/context_audit_20261012/recheck/RB_memory_1.md`.
- RC: the notes in `filelist_c2.txt`, plus any MEMORY.md index line that points at them. INPUT: `audit_cac2_memory_indexed.md`. OUTFILE `results/context_audit_20261012/recheck/RC_memory_2.md`.
