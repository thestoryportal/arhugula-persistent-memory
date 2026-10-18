# Stage 8 — Train (`train.sh`)
Part of the tickets guide. Router: `_system/governance/TICKETS.md`. Roots (L, M, S, W, TD, MEM, HO): `00-roots-and-roles.md`.

```sh
zsh $L/tools/train.sh > <your scratch dir>/train.log 2>&1; echo "train rc=$?"   # cwd = M
```

Run it from cwd = M, Bash background mode. train.sh:21 says "Run it from anywhere"; that comment is wrong [G6]. Its gh calls (train.sh:163, :243, :279) resolve the repo from the cwd, and from L it stops at once with "gh pr view N failed: no git remotes found". The marker stays in `L/tools/ready/`, so a re-run from M is safe [R2].

What one train does, under `L/tools/land.lock`:
- Returns markers a dead train left in `L/tools/ready/claimed`, then claims every `L/tools/ready/T<->` into `L/tools/ready/claimed/` (`L/tools/ready/claimed/T<->`); a re-ship during the train writes a new `L/tools/ready/<T>` that waits for the next train.
- Checks each PR is OPEN at its marker HEAD; a PR that is not gets `stop` and its marker goes to `L/tools/ready/stopped/<T>` (folder `L/tools/ready/stopped`).
- Merges the heads `--no-ff` in READY_AT order onto origin/master in its own worktree `/Volumes/memit/llmdb-lanes/land-<id>` on branch `land/<utc>-<n>`, pushes it (ci.yml:5 runs CI on `land/**`), and runs `M/code/ops/git/git_merge_gate.py --batch --candidate land/<id> PRS --apply`, which waits for candidate CI (480 s) and prints a JSON report.
- PASS: for each PR, the cleanup ship.sh would have done (`land`, `merged`, `lane`, `branch` rows), but only when the lane is clean and its HEAD and branch tip are the marker HEAD inside origin/master; the marker moves to `L/tools/ready/landed`. Then the candidate worktree and branch go, hygiene runs once, and each PR gets `done`.
- Candidate CI failure, confirmed by a failed run: the batch splits in halves down to one PR, which gets `stop` with the run link. A merge conflict: that PR gets `wait` and stays ready. Any other refusal halts the train with nothing cleaned.
- After the gate merges, the train fetches and fast-forwards M (`git -C M merge --ff-only origin/master`, train.sh:158) before any cleanup; a failed fast-forward halts it with nothing cleaned (train.sh:160). The usual cause is a dirty tracked file in M that the merge touches. The PRs are merged by then: commit or move the dirty file, fast-forward M by hand, then clean up each lane and branch the way the train would (below).
- No markers: exit 0 at once (train.sh:265). A malformed marker, a symlinked one, or one still in claimed/ halts the train with 2 before it acts (train.sh:85-100, :268-271).
- A TRANSIENT gate report (the two hygiene refusals, nothing merged) is retried up to 6 times, 20 s apart (train.sh:230-237). MERGED_TRANSIENT (merged, then a transient refusal) goes on to cleanup (train.sh:138, :241).
- A merged PR whose lane fails `owned` (dirty lane, detached HEAD, a branch tip that moved) gets `stop`; its lane and branch are kept and its marker goes to stopped/ (train.sh:168-169). A claimed marker that was never used, whose slot was re-shipped meanwhile, also goes to stopped/ (train.sh:43-48).
- Recovering a marker from `L/tools/ready/stopped/<T>`: fix the cause, then re-ship the ticket; ship.sh writes a fresh marker (an unchanged lane re-ships). Do not move the old marker back by hand: its HEAD and READY_AT describe the earlier attempt. For hand cleanup of a merged PR's lane and branch, the single-command allow rules are `git worktree remove /Volumes/memit/llmdb-lanes/<lane>`, `git branch -D tk/<T>` and `git push origin --delete tk/<T>` (settings.json:31, :33, :35), one command per call, never chained [R23].
- Last line: `train done: landed N, waiting N (conflict), stopped N`.

Linux CI does not run `code/ops/migrate` (ci.yml:60 runs only `code/state/test_icm21*.py`) until Step 213 lands. So a green candidate can still break master there.
- Before a train: a ticket that changes a shape a known consumer reads (a design or PLAN "Ref" names the consumer's step) rides the same train as that consumer's fix. While the fix is not in `L/tools/ready/`, move the producer's marker to `TD/held-markers/<T>` and re-ship the producer after the fix ships. T273 landed alone at 13:57Z on 2026-10-18, and its consumer fix T275 (STEP273-DESIGN.md:22) did not. Master b9dc22fd then failed 210 `test_move_run_core` tests.
- After every train: run `unittest discover -s code/ops/migrate -p 'test_*.py'` on the new master in a clean sparse clone (`git clone --no-checkout --shared M <scratch>`, `sparse-checkout set code`). Control a failure on the previous master with the same command before you call it a break.

One train lands every ready PR in one CI cycle; that is how a batch of tickets meets the 15-minute goal together. You will have one PR ready and two still in Astra and think *"land this one now."* Usually wait for the others: a second train costs a second CI cycle. Land alone only when the others are far behind.

