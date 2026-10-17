# Stage 9 — Land (the gate, and the TRAIN=0 path)
Part of the tickets guide. Router: `_system/governance/TICKETS.md`. Roots (L, M, S, W, TD, MEM, HO): `00-roots-and-roles.md`.

The merge gate is the only merge path, and MAESTRO is the only caller: train.sh calls it in batch mode; with `TRAIN=0`, ship.sh calls `L/land.sh PR LANE`, which waits up to 20 minutes for CI on the lane head, runs the single-PR gate, and on the gate's two stale-base wordings merges origin/master into the lane, pushes and retries once. ship.sh then fast-forwards M the same way (ship.sh:458-462) and stops on a failure, with the PR already merged; recover as for the train. The full merge rule and the cooperative rule the gate relies on are in `_system/governance/MERGING.md`.

You will see green checks on a PR and think *"CI is green, `gh pr merge` is one command."* That is the moment. The gate's lock binds only the writers that take it; a hand merge races every one of them, skips the cleanup marks the next train reads, and the damage lands on master with no name on it.

- Land one PR per land.sh call; a loop of land.sh calls was denied, and so was a combined `worktree remove && branch -D && push --delete` (Git Destructive) [R23].
- The gate refuses while extra branches exist, so hygiene runs first; after `gh pr update-branch` the local branch is behind and the gate reports MERGED_WITH_FAILURE [R51].
- land.sh's CI wait hides gh errors and reports "none" after 20 minutes [G14].

