---
name: merge-gate-first-use-learnings
description: First real git_merge_gate.py merge (PR #21, 2026-10-10) — ask the operator in chat before --apply, run hygiene --dry-run early, integrate in a detached worktree
metadata:
  type: project
---
The first gated merge (D-C10r-gitmerge-1: PR #21 → master a424085, 2026-10-10) taught three things:
1. The session's auto-mode safety check blocked `git_merge_gate.py --apply` even though the operator's GO had arrived through a handoff. Only the operator's direct approval in chat cleared it. Ask in chat before step 5; never route around the check.
2. The gate refuses to merge while any branch exists beyond master, the worktree branches and the PR head. Run hygiene `--dry-run` early to size the cleanup (it was 42 merged branches).
3. Merging origin/master into a branch that already carries every earlier PR merge produced no tree change. A detached integration worktree kept that step isolated from live builder work.

**Why:** these cost MAESTRO9 a stall and an extra round-trip with the operator.

**How to apply:** for each merge, open a new PR (the old branch is ahead of master by receipts), run hygiene `--dry-run`, ask the operator in chat for `--apply`, then follow CLAUDE.md § Merging. Related: [[rerun-builder-tests-host-tmpdir]].
