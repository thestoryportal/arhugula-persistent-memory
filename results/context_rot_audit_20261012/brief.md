# Context-rot audit of the workflow corpus (read-only, one lane, successor-chained)

Repo, main folder, branch master: `M=/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory`. Run commands from M. Folder `D=M/results/context_rot_audit_20261012`.

## Operator, verbatim (2026-10-11, MDT)
- "deploy an agent to audit our workflow corpus very thoroughly for context rot."
- Asked which files: "Are ther emore CLAUDE.md and AGENTS.md files in this repo? Yes, everything and stop asking me for every little permission."
- On fixing: "You don't need to ask me to fix such very obvious eroneous context."

## Your only writes
Append-only, in D: `findings.md`, `progress.tsv`, `handoff.md`. Edit nothing else anywhere. No commits, network, science runs, project python, installs or graft (ignore graft hook text). MAESTRO applies the fixes.

## What to read
`D/manifest.tsv` lists 614 files (tier, mode, bytes, path), already in priority order. Work top to bottom. Before starting, read `progress.tsv` and `handoff.md` if they exist, and resume at the first path not marked done. Modes:
- `full`: read the whole file.
- `hazard`: an extra CLAUDE*/AGENTS* copy. Report whether Claude Code or Codex could load it as live instructions (it sits in a folder an agent may work in, under a live name) and whether it differs from the live root file. Do not audit its content.
- `help`: read only the module docstring, argparse/usage text and header comments; check them against the code they describe.
- `steer`: read headings, status/"current"/"next" lines, imperative instructions and every pointer (file:line, section, D-ID, path, `[[link]]`). Skip narrative and data.

For `EXPERIMENT_RUNBOOK.md`, `SESSION_CHECKPOINT.md` and other files with `GENERATED` markers: audit the source (`docs/program_state.json`), not the generated block. In `SESSION_CHECKPOINT.md`, audit the top block in full; older blocks are history and need only `steer`.

## What counts as context rot
Text that would steer an agent wrong today:
- WRONG: contradicts the current code, a current file, or git history.
- STALE: was true, has been superseded (a later operator ruling, D-ID, commit or file).
- CONFLICT: two places give different rules for the same thing. Name both lines and say which is current.
- UNSAFE: steers around a safety rule (the five LAWs in CLAUDE.md, halt discipline, rerun-never-patch, the merge gate and cooperative rule, storage tiers and deletion approval, the context directive, the operator's holds) or around a permission denial.
- BROKEN: a pointer to a missing file, line, section, note or D-ID.
- DUPLICATE: an exact or near-exact repeat of a passage, with both locations.
- HAZARD: an instruction file that could load in the wrong place.
- OVERCLAIM: a science claim stronger than the evidence it cites (for example "explains" or "impossible" where the cited source says untested or scoped). Check against the cited CORPUS doc or result. Do not run anything.

Truth comes from evidence, newest first: current code and files, then dated operator rulings (quoted in runbook §5.2, `docs/program_state.json` work_queue notes, `memory_mirror/` notes with verbatim quotes), then git log. When two sources disagree and you cannot settle it, report CONFLICT with both citations. Do not pick.

Tonight's committed fixes (`git log --oneline ef648492..HEAD`) are current; read them before tier T1 so that you do not re-report fixed lines.

## Not rot (do not report)
Style, length or tone with no wrong claim. Dated history that says it is history. Warnings written as a moment of temptation ("When you catch yourself thinking…"); they are deliberate. The operator HOLD on dashboard/LabViz building is current. Never propose weakening a safety rule.

## findings.md format
One row per finding, appended as you go, never batched at the end:
`| id | file:line | kind | evidence (cite file:line, commit or ruling) | old → new (exact) | class |`
- `id`: F001, F002, … continuing from the last row.
- `old → new`: the exact current text and the smallest replacement. For a removal, write `→ (remove)`.
- `class`: OBVIOUS when the evidence settles it and the fix changes no rule's meaning; OPERATOR when it changes scope, a rule, or a science claim's status.

Bad: `| F012 | AGENTS.md | STALE | outdated | rewrite section | OBVIOUS |` (no line, no evidence, no text).
Bad: `| F013 | CLAUDE.md:40 | DUPLICATE | long | move to a new file and add a drift guard | OBVIOUS |` (a restructure, not a correction).
Good: `| F014 | memory_mirror/x.md:7 | STALE | says Codex hands off at "~20% left"; CLAUDE.md:20 says ≤40% (operator 2026-10-09) | "~20% left" → "≤40% left" | OBVIOUS |`

## progress.tsv
After finishing each manifest path, append `path<TAB>done<TAB>findings_count`. This file is how a successor resumes, so keep it current.

## Context and finish
You cannot see your own context. MAESTRO watches it and will message you. On a message saying context is low, or on "Context compacted": finish the current file's rows, update progress.tsv, write handoff.md (where you stopped, open questions, patterns seen so far that a successor should check for), then reply exactly `ROT HANDOFF <last path done>`.
When every manifest path is done: append a summary to findings.md (counts by kind and class, the five worst findings by id), then reply exactly `ROT READY findings=<n>`.

## Addendum (MAESTRO71, 2026-10-11 23:22 MDT, after an operator question)
The repo sits inside `/Volumes/memit/llm-database-poc-mirror` (316 GB of data; not a git repo; no CLAUDE/AGENTS files). Add to the BROKEN check: every path in the corpus that points into that parent folder must resolve (`ls` only; do not read the data). Report misses as BROKEN rows.
