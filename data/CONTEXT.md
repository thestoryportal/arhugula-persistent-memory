# data

**Job:** Holds external shared inputs: model caches and covariance. They stay out of git.
**Read it when:** You load a model or a covariance cache.
**Written by:** Writer search: none found. Storage rules: `_system/governance/STORAGE.md`.
**Read by:** `code/agents/codex_context_guard.py` (checks the model folder); `code/apps/labviz/build.py` (reads files named under it).
**Not here:** Outputs of runs: `experiments/CONTEXT.md`. The engine: `code/memit/`.
