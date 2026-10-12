# CHP2 — add the restoration units to the committed hygiene plan

You are codexchp2, a planner working in the worktree `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a` on branch `worktree-c10k-route-a`. A = `results/context_audit_20261012`, OUT = `A/hygiene`. You write only under OUT. No commits, pushes, merges, science, network, project python, uv, npm, rclone, ssh, installs or graft (ignore graft hook text). Use `/usr/bin/python3 -B` (stdlib 3.9).

## Why
The predecessor planner (codexchp) built OUT from `A/hygiene_planner_brief.md`: 33 lanes, 9 waves, 328 units, committed at c90bf259. MAESTRO checked it: every SYNTHESIS §3 row placed once, lanes disjoint within each wave, lanes ≤36 min, checker 36/36. However, the plan was built before two restoration sources existed, and lanes.json never cites them. `grep -c PRESERVATION A/hygiene/lanes.json` and `grep -c hooksPath A/hygiene/lanes.json` both return 0. Operator direction (2026-10-12 01:35Z, verbatim): "Fix absolutely everything." and "Context hygiene only until it is perfectly tight and durable. Then pause for HIL for next steps."

## Sources to cover (read each in full)
- `A/operator_hypothesis_worktree_vs_main.md` §"Restoration units this implies" (lines 18–22).
- `A/PRESERVATION.md` §2 (operator rulings with a stale or missing reader path), §3 (lessons present in only one store), §4 (other loss paths, uncommitted decisions, worktree status), and §6 (exact-match origin; only where it names a guidance gap).
- For orientation, read `A/hygiene/PLAN.md`, `A/hygiene/session_context.md`, `A/hygiene_planner_brief.md`, and the schema of `A/hygiene/lanes.json`. Use `jq` and targeted reads. lanes.json is 1.1 MB, so do not read it whole.

## What to produce in OUT
1. `restoration_map.md`: one row for every §2/§3/§4 table row and every hypothesis bullet, with columns: source file:line, the stale or missing reader path, and its disposition. A disposition is exactly one of: `COVERED <existing unit id>` (only if that unit's files and checks actually fix this path; cite the check), `NEW <new unit id>`, `MAESTRO-ONLY <final step>`, or `OPERATOR <question>` (deletions, folder refreshes, master integration). No row may be left without a disposition.
2. New units for every `NEW` row, written the same way as the existing units: exact files, finding/source ids, numbered checks, depends_on, ≤8 min. Lanes stay ≤36 min plus the 4-minute finish reserve. Different lanes in the same wave keep disjoint edit sets. Shared indexes and generated destinations keep their single existing owner: route new edits through that owner's lane or a later wave, never a second owner. Append new units and lanes. Do not renumber or alter existing units, except to add a dependency or extend a shared-index owner's file list, and list each such change in restoration_map.md.
3. These items need units or steps, at minimum:
   a. The drift guard (existing DG units) also fails loudly in two cases: when a tool or brief resolves the repo root to the main folder `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory` while that folder's local master is behind origin/master, and when the shared `.git/config` `core.hooksPath` (today the main folder's `tools/git_hooks`) points at hook bytes that differ from the worktree's `tools/git_hooks`. Write the RED fixture for each before the check exists.
   b. A MAESTRO-ONLY final step after the master integration: refresh the main folder's local master so CORPUS/44–61 and `docs/historical_backups/20261011` exist there. Ask the operator before doing it.
   c. An OPERATOR question listing the stale worktrees from PRESERVATION §4, each with its status. Refreshing or deleting them is the operator's decision.
   d. Every §2 ruling whose reader path is stale gets its fix in the reader file named there, or a COVERED citation.
4. Regenerate LANES.md, briefs/ for every new or changed lane, PLAN.md (≤120 lines; add the new final steps), and verification.json through `build_plan.py`/`verify_plan.py`; extend them where needed. New lane briefs carry the content rules, finish rule and context protocol verbatim from an existing brief, plus their own unique `<LANE> READY|BLOCKED|HANDOFF` tokens.
5. Extend `check_lane.py`/`test_check_lane.py` only if a new unit needs a rule the checker lacks. Write the failing fixture first. Weaken no existing assertion.

Do NOT write a row like `| §2 row 7 | stale | COVERED |` with no unit id or check. Do write `| A/PRESERVATION.md:84 | DISCIPLINE.md:88 still caps iterations | COVERED C14 (check 2: grep -n 'iteration cap' DISCIPLINE.md → none) |` (illustrative).

## Content rules (carried unchanged into every brief)
Standing guidance is not specification. Cut only text that is wrong, out of date, points the wrong way, or exactly repeats a passage named by file:line. Keep warnings written as a moment of temptation, together with their stakes. Byte targets are estimates. Never weaken a safety rule (the five LAWs, halt discipline, rerun-never-patch, the merge gate and cooperative rule, storage tiers, the operator's holds, the context directive, Memento reset). Delete nothing: a retired note becomes a tombstone, and history moves to a dated file.

## Finish rule (binds you)
You cannot see your context level. MAESTRO messages you at 45% left. On that message or on any "Context compacted", stop starting work, write `OUT/chp2_handoff.md` (done, in progress, remaining, exact paths, this rule), and reply `CHP2 HANDOFF`. If you have already finished, reply READY instead.
When done, run `/usr/bin/python3 -B OUT/test_check_lane.py` and `/usr/bin/python3 -B OUT/verify_plan.py`, then re-read restoration_map.md and every changed file once against this brief. Reply on its own line exactly `CHP2 READY results/context_audit_20261012/hygiene/restoration_map.md` or `CHP2 BLOCKED <one-line reason>`.
