---
name: work-from-main-folder-on-master
description: Since 2026-10-12 the main checkout on master is the one working copy; MAESTRO pushes master directly; worktrees are one-lane builder sandboxes or the merge gate's isolated integration worktree
metadata:
  type: feedback
---
From Oct 4 to Oct 12, 2026, MAESTRO worked in `.claude/worktrees/c10k-route-a` while the main folder sat at the Oct 4 master. 540 commits piled up on the side branch, and anything reading the main folder saw week-old findings. The operator spotted the split first. PR #23 (master e0ac5426) merged the branch through the gate and the main folder was fast-forwarded. The operator then directed: "get us set to main locally and fully and durably set for forward work", and "Push master yes, as long as it is safe".

**Why:** a long-lived worktree makes a second, silently stale copy of the evidence; every tool that defaults to the main folder (LLMDB_ROOT, core.hooksPath) then reads or runs the stale one.

**How to apply:** start every MAESTRO session in `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory` on master; at start `git fetch -q origin && git status -sb` and fast-forward if behind. Commit on master and push after the local checks; fix a red master CI run first. Builders still get a worktree per lane, merged through the gate the same day; removing a worktree folder needs operator approval. Rule home: CLAUDE.md § operating model. Related: [[atomic-units-parallel-worktree-lanes]], [[context-hygiene-must-reach-every-store]].
