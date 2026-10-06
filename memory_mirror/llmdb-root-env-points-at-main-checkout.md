---
name: llmdb-root-env-points-at-main-checkout
description: "The project settings file (.claude/settings.json `env` block) sets LLMDB_ROOT=<main checkout>; every repo tool (closeout_check, render_state, engine_fingerprint, harness drivers) prefers it over its own path, so from a worktree they silently read and write the MAIN checkout. Prefix each tool call with LLMDB_ROOT=<worktree literal path>."
metadata:
  node_type: memory
  type: feedback
  originSessionId: 4d71207f-24bf-4199-894f-d2f977d9f609
---

`tools/closeout_check.py` and `tools/render_state.py` set `ROOT = os.environ.get("LLMDB_ROOT") or <their own repo>`. The project settings file `.claude/settings.json` sets `env.LLMDB_ROOT=/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory`, the main checkout, so every Claude Code session's shell inherits it (corrected 2026-10-06: not the shell profile). Run from a worktree, closeout_check reported every tracker MISSING for a freshly propagated D-ID, the fingerprint tool hashed the main checkout's engine, and render_state wrote, or would have written, the main checkout's generated blocks. On 2026-10-06 that render happened to be a no-op. The pre-commit hook inherits the same variable, so its "no drift" verdict checked the main checkout, not the commit.

**Why:** a gate that checks the wrong tree passes or fails for reasons unrelated to the work, and a render can modify the shared checkout.

**How to apply:** in a worktree, run every tool as `LLMDB_ROOT=<worktree absolute path> python3 tools/…`, spelling the path literally, because the shell guard rejects `export X=$PWD` in compound lines. Inside a script, export it on its own line. If a gate result contradicts files you just wrote, check `echo $LLMDB_ROOT` first. Related: [[mbp-shell-aliases-trap]].
