# Astra high, confirm round: G7 NO-GO fixes on `corpus/icm-v2`

You reviewed `efef4529..4e679b15` and returned NO-GO with four BLOCKING findings. Your full verdict is `knowledge/analyses/icm-v2-restructure/astra-g7-verdict.md` in this worktree. Read it first. The fixes are commits `acfc1755` (8b, guide text), `dd254c8a` (8c, review record and c10y precondition) and `9e6d51dc` (8a, resolver). Review only `git diff 4e679b15..9e6d51dc`.

You are read-only. Do not edit any file. Run repo Python with `LLMDB_ROOT=$PWD PYTHONPATH=code .venv/bin/python -B`. Do not run model or GPU work.

## Questions

1. Finding 1 (resolver fragments): does every old anchor now resolve to a fragment that exists in its destination file? Rerun your 517-anchor check. Also check the new design in `build_anchor_map`: the anchor map now depends on the current headings of the split parts, and a heading edit in a part needs `build_index.py --write`. Can a normal experiment close-out (which adds headings to runbook parts) now break `build_index --check` in a way that the operator cannot fix by regenerating? Can the alignment return a fragment that exists but names the wrong section?
2. Findings 2-4 (guide text): are they fixed? Lane 8b also swept the same three claim classes (the `**Read by:**` line of every guide, claims that `CLAUDE.md` holds rules, claims about embedded status blocks). Is any claim in those classes still false at `9e6d51dc`? Is any new citation wrong?
3. `experiments/c10y/design/PRECONDITION_HALT_WRITER_REPOINT.md` and `knowledge/analyses/icm-v2-restructure/OPEN-ITEMS.md`: is any statement false? Does the precondition file state your Ruling 3 condition correctly?
4. Ruling 4: you rejected the walk-test bar because guide claims were still false. With findings 2-4 fixed and the sweep done, is the restructure fit to merge?

## Output

First line exactly `VERDICT: GO` or `VERDICT: NO-GO`. Then one section per question. Mark each finding BLOCKING or NON-BLOCKING, with file:line and the command and output that prove it. Do not repeat non-blocking open items from your first verdict. Do not report style preferences as findings.
