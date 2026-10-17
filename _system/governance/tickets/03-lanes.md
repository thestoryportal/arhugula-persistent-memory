# Stage 3 — Lanes (`mklane.sh`)
Part of the tickets guide. Router: `_system/governance/TICKETS.md`. Roots (L, M, S, W, TD, MEM, HO): `00-roots-and-roles.md`.

```sh
zsh $L/tools/mklane.sh T319 TD
```

- One lane per ticket: a worktree of M at `/Volumes/memit/llmdb-lanes/tk-<T>` on branch `tk/<T>`, from freshly fetched origin/master, as a non-cone sparse checkout (mklane.sh:9: `/*`, minus `/experiments/` except `/experiments/*/CONTEXT.md`, minus `/knowledge/` except `/knowledge/**/*.md`, minus `/_archive/`), widened by the 16 files in `L/tools/t012-widen.txt` that tests read, with `/code/memit/vendor/notebooks/` excluded (mklane.sh:11). It logs `dispatch` to TD/ledger.tsv. About 43-50 MB instead of 6.5 GB, which is what lets ten lanes fit on the disk [R15].
- Use mklane.sh, not `git worktree add` by hand (which S/SKILL.md:64 still shows [G10]): a `/code`-only lane is too narrow for tests that read `knowledge/specs/*.md`, and guard_mutants refuses the vendor notebook symlinks, so a hand lane fails at ship, not at dispatch [R15].
- No `uv run` in a lane. It makes an 824 MB `.venv` inside the lane, and the pre-commit hook's first interpreter is the lane's `.venv` (pre-commit:15), so a venv without yaml and markdown_it blocks the close commit. If one appears, probe `<lane>/.venv/bin/python -c 'import yaml, markdown_it'` before close; `git worktree remove` clears it [R16]. The one interpreter for builders, gates, hygiene and the sampler is `M/.venv/bin/python -B`.
- The pre-commit hook is live in M and in every lane (`git config core.hooksPath = code/ops/git/hooks`, file `M/code/ops/git/hooks/pre-commit`): it blocks stale generated state, stale fingerprints, a staged closure that is not PASS, secrets, and a non-default index. So a ticket that changes the hook is a production change, and commits are plain `git commit` with no paths, `-a` or `-i` (tickets.py:245-250 does this) [R19]. The closure check fails on an untracked file inside a staged folder; never chain a heredoc after `git commit &&`, because when the hook blocks, the heredoc never runs and a later step reads a missing file [R20].

