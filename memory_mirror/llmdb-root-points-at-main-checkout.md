---
name: llmdb-root-points-at-main-checkout
description: The shell exports LLMDB_ROOT=main checkout, so repo tools run from a worktree silently check main; prefix LLMDB_ROOT=$PWD
metadata:
  type: feedback
---

The login shell exports `LLMDB_ROOT=/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory` (the MAIN checkout). Tools that honour it — `tools/closeout_check.py:25`, `tools/engine_fingerprint.py`, the GPU gate, experiment launchers — therefore read the main checkout even when run from `.claude/worktrees/c10k-route-a`.

**Why:** 2026-10-10 MAESTRO2 reran `closeout_check.py D-C10z-a4` from the worktree and got "14 MISSING" seconds after Codex Z4 had it ALL GREEN; the trackers were edited in the worktree, the checker read main. The engine fingerprint likewise reported main's `memit_main.py` path.

**How to apply:** in a worktree always run repo tools as `LLMDB_ROOT=$PWD python3 tools/...` and check the path the tool prints. A RED/GREEN disagreement between sessions → compare roots before suspecting the files. Related: [[gpu-gate-refuses-any-venv-python]].
