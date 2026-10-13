# data

**Job:** Holds external shared inputs. The v2 paths are `data/hf_cache/` (HF models; `HF_HOME`) and `data/covariance/` (MEMIT second-moment statistics). Both are untracked symlinks. A fresh worktree does not have them. Today, only the main checkout has the old-layout links: `hf_cache` points to `/Volumes/memit/llm-database-poc-mirror/hf_cache`; `covariance_caches` points to `/Volumes/memit/llm-database-poc-mirror/covariance_caches`. Phase 5 creates the v2 links.
**Read it when:** You load a model or a covariance cache. Read `_system/governance/STORAGE.md` before any download.
**Written by:** Writer search: none found. Storage rules: `_system/governance/STORAGE.md`.
**Read by:** `code/agents/codex_context_guard.py` (checks the model folder); `code/apps/labviz/build.py` (reads files named under it).
**Not here:** Outputs of runs: `experiments/CONTEXT.md`. The engine: `code/memit/`.
