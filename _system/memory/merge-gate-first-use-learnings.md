---
name: merge-gate-first-use-learnings
description: First real git_merge_gate.py merge (PR #21, 2026-10-10) — gate --apply allow-listed since 15 Oct, run hygiene --dry-run early, integrate in a detached worktree
metadata:
  type: project
---
The first gated merge (D-C10r-gitmerge-1: PR #21 → master a424085, 2026-10-10) taught three things:
1. The session's auto-mode safety check blocked `git_merge_gate.py --apply` even though the operator's GO had arrived through a handoff. Only the operator's direct approval in chat cleared it. The chat-approval requirement was superseded by the 15 Oct allow rule; never route around a permission refusal.
2. The gate refuses to merge while any branch exists beyond master, the worktree branches and the PR head. Run hygiene `--dry-run` early to size the cleanup (it was 42 merged branches).
3. Merging origin/master into a branch that already carries every earlier PR merge produced no tree change. A detached integration worktree kept that step isolated from live builder work.

4. (2026-10-15, PR #30) After `gh pr update-branch`, the local branch stays at the pre-update SHA, so the gate's post_hygiene `branch -d` fails (MERGED_WITH_FAILURE; the merge itself is fine). Fix: `git pull --ff-only`, prove the branch is an ancestor of master, then `branch -d` it and `push --delete` the remote. The gate `--apply` still needed the operator's chat OK in this session as well.

5. (2026-10-15) The operator installed a narrow allow rule in ~/.claude/settings.json: `Bash(<M>/.venv/bin/python -B <M>/code/ops/git/git_merge_gate.py:*)` (absolute paths). `--apply` now runs without a chat OK. Before T035 on 16 Oct, the gate refused any PR whose head lacked the current origin/master ("branches: FAIL ... update branch then obtain fresh CI"). So every merge makes the other open PRs stale: land them one at a time. Merge origin/master into the lane branch, push, wait for CI on that exact head SHA, then run the gate. Do not use `gh pr update-branch` (see 4). Since 2026-10-16 (T035, git_merge_gate.py:143, MERGING.md:7) the gate accepts a stale base when no file the PR changes changed on master since the merge-base and GitHub says MERGEABLE; the merge-master/fresh-CI loop is only for an overlapping PR.

**Why:** these cost MAESTRO9 a stall and an extra round-trip with the operator; the stale-base refusal cost two refused gate runs on 15 Oct.

**How to apply:** invoke the gate with the exact absolute command the rule names. Land PRs one at a time through the gate with green candidate-head CI. Only an overlapping stale-base PR needs the merge-master/fresh-CI loop; a non-overlapping stale base is accepted when GitHub reports MERGEABLE. Run hygiene `--dry-run` early. Follow `_system/governance/MERGING.md`. Related: [[rerun-builder-tests-host-tmpdir]], [[lean-ticket-lane-traps]] (Claude auto-memory, not _system/memory/).
