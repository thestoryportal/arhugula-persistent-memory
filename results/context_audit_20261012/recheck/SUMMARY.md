# Context recheck — what is still wrong in CLAUDE.md, AGENTS.md, MEMORY.md

Written 2026-10-11 ~22:50 MDT (2026-10-12 04:50Z) by MAESTRO70.
Scope, operator verbatim: "It also included CLAUDE.md and AGENTS.md and MEMORY.md. That was it...period." (MEMORY.md includes the notes it lists, as on Oct 10.)

Method (the Oct 10 shape): three read-only Codex checkers re-checked tonight's 19:12 MDT audit findings against today's master text (`d280a086`). Each kept finding cites file:line and gives the exact old → new text. Full tables: `RA_claude_agents.md`, `RB_memory_1.md`, `RC_memory_2.md`.

| | still wrong | already fixed | finding was mistaken |
|---|---|---|---|
| CLAUDE.md + AGENTS.md (RA) | 14 | 18 | 43 |
| MEMORY.md + notes, half 1 (RB) | 36 | 0 | 5 |
| MEMORY.md + notes, half 2 (RC) | 20 | 0 | 52 |

## What the 70 still-wrong items are, in plain words

1. **CLAUDE.md and AGENTS.md disagree with each other or with today (about 10 distinct edits).** The "stop at 45%" context step is in the memory note but missing from both. AGENTS.md gives a reading order that conflicts with CLAUDE.md's. AGENTS.md carries a second full copy of the long merge-gate paragraph. Other items: "Node 24" (it is 26), tools listed that are not on disk, a "no-GPU sanity" command that actually overwrites a results file, and hooks claimed to "enforce" something that has not been verified.
2. **Memory notes that steer against current rules (about 17).** Examples:
   - a note that still says the operator merges and work goes on a branch (`commit-forward-work-without-asking`);
   - notes that describe ways around a denied command (`git-add-all-leaks-secrets…`, `autoresearch-sandbox-fence…`);
   - notes that let Perplexity stand in for the Astra review (`codex-runs-inline…` description, `in-weight-value-expression…`);
   - "irreversible decisions do not block on ratification" (`operator-profile…`);
   - older context thresholds (`never-idle…`, `context-management…` line 13);
   - a watch method its own note says failed (`codex-watch-anchor…`).
3. **Notes that overstate science claims (about 13).** "Explains", "impossible" and "the cell is empty in all literature" are written where the evidence is a dated search or one untested setup (the prior-art notes, several in-weight notes, `pass-label…`, `no-model-cleared…`). One note gives unsafe advice: `mps-offset-view-conversion-bug` says "or clone() first" in its description while its own body says clone() is not safe.
4. **Stale pointers, broken links and exact repeats (about 15).** Line numbers into CLAUDE.md that moved, two links to notes that do not exist, the same paragraph pasted five times in two notes (`skills-are-contracts…`, `fallback-that-nullifies…`), an old hash, and old timings.

Every proposed edit is the smallest change to the cited line. None removes a safety rule, a hold or a temptation warning. Style-only trims were not proposed.

## Growth since Oct 10 (why this keeps coming back)
`MEMORY.md` went from 16 KB / 124 lines to 22 KB / 155 lines. Notes went from 171 to 203. CLAUDE.md is 19 KB and AGENTS.md is 25 KB, and every session loads both.

## Next, on the operator's go
A fresh session applies the 70 edits exactly as the tables give them, rereads each changed file, and runs Astra-high on the diff. It folds Astra's fixes, then commits and pushes to master. Nothing outside these three files and the listed notes changes.
