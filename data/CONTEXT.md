# data

**Job:** Holds external shared inputs. The v2 paths are `data/hf_cache/` (HF models; `HF_HOME`) and `data/covariance/` (MEMIT second-moment statistics). These links do not exist in this v2 worktree yet. Today, use `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/hf_cache` for HF models and `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/covariance_caches` for covariance statistics. These old-layout links point to `/Volumes/memit/llm-database-poc-mirror/hf_cache` and `/Volumes/memit/llm-database-poc-mirror/covariance_caches`. The repo sync creates the untracked v2 links.
**Read it when:** You load a model or a covariance cache. Read `_system/governance/STORAGE.md` before any download.
**Written by:** Writer search: none found. Storage rules: `_system/governance/STORAGE.md`.
**Read by:** `code/agents/codex_context_guard.py` (checks the model folder); `code/apps/labviz/build.py` (reads files named under it).
**Not here:** Outputs of runs: `experiments/CONTEXT.md`. The engine: `code/memit/`.
