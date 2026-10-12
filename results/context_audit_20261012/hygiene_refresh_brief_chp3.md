# CHP3: rebase the committed hygiene plan onto current master

You are codexchp3, a planner working in the main folder `M=/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory` on branch `master`. A = `results/context_audit_20261012`, OUT = `A/hygiene`. Write only under OUT. No commits, pushes, merges, fetches, science, network, project python, uv, npm, rclone, ssh, installs or graft (ignore graft hook text). Use `/usr/bin/python3 -B` (stdlib 3.9). Other sessions share this folder, so leave every file outside OUT untouched, even if it looks wrong.

## Why
The plan in OUT (41 lanes, 9 waves, 386 units) was built at `planning_base_commit` `c90bf259` on a premise that is now false: that the main folder M sits on a stale local master (`557a58bc`), so builders must read master content from `origin/master=5ccbb836`. Every lane brief repeats that premise as binding text, generated from `OUT/build_plan.py:146`. Launching builders from it would feed them false facts, which is the rot this plan exists to remove. The operator has made hygiene the top priority (2026-10-12 ~04:05Z, verbatim): "This is top priority and nothing should be running with the context rot that currently is in place." The standing direction still holds (01:35Z, verbatim): "Fix absolutely everything." and "Context hygiene only until it is perfectly tight and durable. Then pause for HIL for next steps."

## Facts measured by MAESTRO70 (2026-10-12 04:05–04:25Z; re-verify read-only before relying on them)
- M is on `master` at `d280a086`, equal to `origin/master` (`git rev-parse HEAD origin/master`). Sessions now start in M by policy since 2026-10-12 (`/Users/robertrhu/.claude/projects/-Volumes-memit-llm-database-poc-mirror-arhugula-persistent-memory/memory/work-from-main-folder-on-master.md`).
- PR #23 merged branch `worktree-c10k-route-a` into master at 02:27Z. MAESTRO deleted that branch from GitHub at ~04:25Z with operator approval. GitHub now holds only `master`.
- The old worktree `M/.claude/worktrees/c10k-route-a` still exists. Its local branch is at `6c6db821`, which is an ancestor of master. It holds uncommitted, non-durable work: `results/labviz/`, `results/labviz_codex_brief.md`, `results/labviz_codex_impl.md`, `results/labviz_v2_codex_impl.md`, `tools/labviz_serve.sh`, `.ignore`, `external_prior_art`, and a foreign edit to `tools/test_dashboard_mathlab.py`. Idle Codex sessions sit in it.
- 29 commits since `c90bf259`. Of the plan's target files, exactly four changed: `CLAUDE.md`, `docs/program_state.json`, `memory_mirror/MEMORY.md`, `memory_mirror/work-queue-tab-keep-current.md` (`git diff --name-only c90bf259 HEAD`).
- Claude memory stores for this repo: S2 (125 notes) and S3 (26 notes), as the plan already names. No worktree-scoped project dir has a memory folder.

## What to produce in OUT
1. **New master-authority correction.** Move the current `master_authority_correction.md`, `master_authority_receipt.json` and `master_snapshot/` to dated history names (suffix `_20261012T0200Z`), byte-identical. Write new ones frozen at `d280a086`: M equals origin/master; guide snapshots and SHA-256s from `git show d280a086:<guide>`. Keep every binding rule the old correction carried that is still true (preserve remote-only commits, no builder Git mutation, merge gate, Memento, context budgets).
2. **Rebase the plan.** Set `planning_base_commit` to `d280a086`. Fix `build_plan.py` so the generated brief text states the current facts above. M stays read-only to builders, and lanes still run in isolated worktrees branched from master.
3. **Re-anchor.** For every unit whose files include one of the four changed files, re-read the current bytes and update its file:line anchors and before-hashes. If current bytes already fix a unit's finding, keep the unit id and give it disposition `ALREADY-FIXED` with the read-only check that proves it.
4. **Re-decide the stale-main items.** Revisit M-REFRESH, M-REFRESH-FINAL, F01, D-U20/21/22, PRESERVE-INFLIGHT, the OPERATOR-WORKTREES step and the drift-guard check that fails when M is behind origin/master. Keep the guard check: it is the durable protection. Update each final step to the current state, and record each change in a table in the report. The old worktree's uncommitted files must be preserved durably before any action on that worktree. That stays an OPERATOR item.
5. **Sweep for other stale facts.** In OUT's plan files (not the audit evidence files in A, which stay as history), grep for `557a58bc`, `5ccbb836`, `c90bf259`, `c10k-route-a`, `worktree-c10k-route-a`, `511`/`522` divergence counts, and "stale LOCAL". Resolve every hit, or mark it as an explicitly dated history reference.
6. **Regenerate** `lanes.json`, `LANES.md`, `briefs/`, `PLAN.md` and `verification.json` through `build_plan.py` and `verify_plan.py`. Unit ids are preserved. A change in unit count is listed with reasons.
7. `OUT/chp3_refresh_report.md`: what changed per file, the re-anchor table (unit, file, old anchor, new anchor, disposition), the final-step table, and the open questions you want Astra to check.

Do NOT hand-edit `briefs/*.md`, `LANES.md` or `lanes.json` with search-and-replace. They are generated; fix the generator and regenerate. Do NOT delete the old correction; it becomes dated history.

## Pass condition
- `grep -rn '557a58bc\|5ccbb836\|stale LOCAL' OUT/briefs OUT/PLAN.md OUT/LANES.md` returns nothing.
- `/usr/bin/python3 -B OUT/test_check_lane.py`, `/usr/bin/python3 -B OUT/test_restoration_plan.py` and `/usr/bin/python3 -B OUT/verify_plan.py` all pass.
- All 386 original unit ids are still present.
- Every hit from step 5 is resolved or dated.

## Content rules (carried unchanged)
Standing guidance is not specification. Cut only text that is wrong, out of date, points the wrong way, or exactly repeats a passage named by file:line. Keep warnings written as a moment of temptation, together with their stakes. Byte targets are estimates. Never weaken a safety rule (the five LAWs, halt discipline, rerun-never-patch, the merge gate and cooperative rule, storage tiers, the operator's holds, the context directive, Memento reset). Delete nothing: a retired note becomes a tombstone, and history moves to a dated file.

## Finish rule (binds you)
You cannot see your context level. MAESTRO messages you at 45% left. On that message or on any "Context compacted", stop starting work. Write `OUT/chp3_handoff.md` (done, in progress, remaining, exact paths, this rule) and reply `CHP3 HANDOFF`. If you have already finished, reply READY instead.
When done, run the three checks, then re-read the report and every changed file once against this brief. Reply on its own line exactly `CHP3 READY results/context_audit_20261012/hygiene/chp3_refresh_report.md` or `CHP3 BLOCKED <one-line reason>`.
