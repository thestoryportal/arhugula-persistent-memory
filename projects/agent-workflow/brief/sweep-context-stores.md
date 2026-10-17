# Sweep brief: context stores (output: P/drafts/inventory/context-stores.md)

Read M/projects/agent-workflow/brief/sweep-common.md first. Its roots, hard rules, evidence rules and output form apply here. Rules 4 (authority, date, supersession) and 6 (trace identifiers) are the core of this sweep.

## Task
List every store of context that an agent on the belt reads or writes TODAY, and record how each one is loaded, who writes it, what authority its contents carry, how old they are, and how a superseded entry is marked. Operator, verbatim (2026-10-17): "there are also ~/.claude session, conversation and memory files that we can leverage for very grounded and semi-persistent agent memory by developing an architecture, framework and discipline for moving these into the ICM repo context architecture. Memory stores in Claude and Codex very quickly become useless due to the lack of a map connecting them to what is relevant at any given moment or for a particular task." You map what exists. You do not design the memory architecture.

## Stores (start list; add every other store you find cited)
- Harness-loaded instructions: ~/.claude/CLAUDE.md, ~/.claude/RTK.md, M/CLAUDE.md, M/AGENTS.md, M/routing.md, ~/.codex/AGENTS.md; MEM/MEMORY.md (auto-loaded into Claude sessions); hook text injected at session start or per prompt (the hook entries in ~/.claude/settings.json and M/.claude/settings.json; record what each injects, cited).
- ICM tree: M/CONTEXT.md and every folder CONTEXT.md that the routes reach from M/CLAUDE.md ("Where things live" and the links in each CONTEXT.md); M/_index/; M/map/. Then, as a completeness control, list the tracked CONTEXT.md files with `git -C M ls-files '*CONTEXT.md' ':!_archive/*'`. Each one that no route reached is an `OFF-ROUTE` row.
- Governance: M/_system/governance/*.md and M/_system/governance/tickets/*.md.
- Memory: MEM/ (Claude auto-memory); M/_system/memory/ (the repo mirror: MEMORY.md, SESSION_CHECKPOINT.md, the topic files); ~/.codex/memories/ and ~/.codex/memories_1.sqlite (size and table names only, from `sqlite3 -readonly <file> .tables` if sqlite3 exists).
- Handoffs: HO/HANDOFF-STEP*.md; ~/.claude/memento/handoffs/; ~/.claude/handoffs/.
- Transcripts: the Claude project jsonl files and `*/subagents/` folders in MEM's parent folder; ~/.codex/sessions/; ~/.codex/history.jsonl; ~/.codex/session_index.jsonl. Sizes, counts and date range only, plus the identifier fields from `head -c 2000` of one Claude main transcript, one Claude subagent transcript and one Codex session file.
- Program state and ledgers: M/program/program_state.json; M/program/ checkpoints; TD/ledger.tsv; TD/METRICS.md; W/ledger.tsv; M/evidence/ (the CONTEXT.md and the top-level layout only).
- Reviews, rulings and plans: TD/reviews/; W/reviews/; P/rulings/; W/PLAN.md and TD/PLAN.md (the `Approved:` lines only).
- Prior audit: M/projects/context-audit/receipts/ (cite its findings about stores as REPORT; do not redo them).

## Sections
1. `## Store table`: one row per store. Columns: store | path | route (the ICM line that names it, or `OFF-ROUTE`) | size (bytes and file count, with the command) | date range (oldest and newest, from text dates or mtimes; say which) | writer (who writes it; cite the doc or script line) | reader and load mode (`harness-loaded`, `told-to-read by <path:line>`, or `none found` with the grep) | authority classes present (sample 3 entries; cite each) | supersession mechanism (cite, or `none found` with the grep) | git status (run `git -C M ls-files --error-unmatch <path>` and `git -C M check-ignore <path>`; outside M: `not in repo`).
2. `## Mirrors and copies`: each pair of stores that holds copies of the same content (for example MEM/MEMORY.md and M/_system/memory/MEMORY.md; M/CLAUDE.md, M/AGENTS.md and M/routing.md). For each pair: the copy mechanism (cite the script or doc), and `cmp` or `diff --stat` output.
3. `## Same fact, several stores`: pick 8 facts that appear in two or more stores (for example the context ceiling, the 45% rule, the wave-2 pause, the merge gate). For each fact, quote each store's wording with path:line. Mark `AGREE` or `DIFFER`.
4. `## Staleness sample`: pick 10 MEM files and 5 M/_system/memory files. For each, list each file path, script name or flag it names, and check whether it still exists (`ls`, or grep in the named script). Columns: memory file | named thing | exists (yes or no, with the command) | dated (yes or no).
5. `## Trace identifiers`: for each transcript kind, the fields that identify the session, the writer (agent or tool), the parent, the model and the position in the trace, quoted from `head -c 2000`. Write `absent` for a field that is not there.
6. `## Eval-relevant artifacts today`: facts only, in the six areas of ~/.claude/skills/eval-audit/SKILL.md (read its "Diagnostic Checks" headings). For each area, list what exists: trace sources (from section 5), labeled verdicts (review files with GO, NO-GO or REVISE: count them per folder, with the command), failure-category lists (M/_system/governance/tickets/gaps.md and others; for each list, record whether its entries cite an observed event or not), metrics files, and who reviewed what (from the review file headers). Do not say whether any of it is adequate.
7. `## Size against caps`: each store that has a stated cap (for example MEMORY.md 24,400 bytes in ~/.claude/CLAUDE.md, the 2048-byte ticket JSON limit) with its cap citation and its measured size.

## Acceptance
Every store in the start list has a row, or a `## Missing or dead paths` line. Every authority, date and supersession cell has a citation or a `none found` with its grep. No transcript was read beyond `head -c 2000`.

## Bad and good cells
These cells show the form only. Their facts are not checked.
- BAD: "supersession: entries are updated in place" (no citation; may be the writer's intent, not the end state)
- GOOD: "supersession: `none found` (`grep -rn -i 'supersed' MEM/ | wc -l` → 3, all inside topic text, none a marker); ~/.claude/CLAUDE.md:NN asks to 'change existing status lines in place' [DOC, INTERPRETED]"
