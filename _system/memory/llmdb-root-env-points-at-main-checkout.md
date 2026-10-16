---
name: llmdb-root-env-points-at-main-checkout
description: A worktree session inherits LLMDB_ROOT=main checkout from .claude/settings.json env; run tools as `LLMDB_ROOT=$PWD python3 code/...`
metadata:
  type: feedback
---

`code/gates/closeout_check.py:26` and `code/state/render_state.py` set `ROOT = os.environ.get("LLMDB_ROOT") or <their own repo>`. The project settings file `.claude/settings.json` sets `env.LLMDB_ROOT=/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory` (line 102), the main checkout, so every Claude Code session's shell inherits it (corrected 2026-10-06: not the shell profile). Run from a worktree, closeout_check reported every tracker MISSING for a freshly propagated D-ID, the fingerprint tool hashed the main checkout's engine, and render_state wrote, or would have written, the main checkout's generated blocks. On 2026-10-06 that render happened to be a no-op. The pre-commit hook inherits the same variable, so its "no drift" verdict checked the main checkout, not the commit. Again on 2026-10-10: a rerun of `closeout_check.py D-C10z-a4` from the worktree reported "14 MISSING" seconds after it was ALL GREEN, because the trackers were edited in the worktree and the checker read main.

**Why:** a gate that checks the wrong tree passes or fails for reasons unrelated to the work, and a render can modify the shared checkout.

**How to apply:** in a worktree, run every tool as `LLMDB_ROOT=<worktree absolute path> python3 code/…` (or `LLMDB_ROOT=$PWD` where the shell guard allows it), and check the path the tool prints. Inside a script, export it on its own line. If a gate result contradicts files you just wrote, or two sessions disagree RED/GREEN, check `echo $LLMDB_ROOT` before suspecting the files. Related: [[mbp-shell-aliases-trap]], [[gpu-gate-refuses-any-venv-python]].

**Other worktree/shell traps (2026-10-06/07):** never `cd` out of the worktree (it relocated a session permanently, twice) — use absolute paths; bare `git` is rewritten by the rtk hook to `rtk git`, so use `/usr/bin/git` when you need raw output or a guard refuses the rewritten form; `.gitignore` has `*token*` and `*.log` (lines 54, 43), so files with "token" in the name and cited logs need `git add -f`; MPS has no float64 (do float64 math on CPU).
