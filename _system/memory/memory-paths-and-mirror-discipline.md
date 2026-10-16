---
name: memory-paths-and-mirror-discipline
description: "Memory lives twice: harness-live ~/.claude/projects/<hash>/memory and git-tracked _system/memory/; sync one way, never cp a thin dir over MEMORY.md"
metadata:
  type: reference
---

Memory lives in TWO places and they can desync:
- **Harness-live:** MAESTRO sessions start in the main checkout, so recall reads `~/.claude/projects/-Volumes-memit-llm-database-poc-mirror-arhugula-persistent-memory/memory/`; sessions started at the mirror root read `…-Volumes-memit-llm-database-poc-mirror/memory/`. Check which path the system-reminder names.
- **Durable archive:** `<repo>/_system/memory/` — git-tracked, the **canonical full set + MEMORY.md index**. This is the recovery source.
- `code/gates/closeout_check.py:289-305` compares only `LLMDB_LIVE_MEMORY` (default: the mirror-root dir) with `_system/memory/`; set `LLMDB_LIVE_MEMORY` to the store you wrote.

**Trap hit 2026-06-20 (on the pod):** `cp $LIVE/*.md $MIRROR/` blindly copied a thin (restart-wiped) live dir over the mirror — **clobbering the mirror's full MEMORY.md with a 1-line stub.** Recovered via `git checkout HEAD -- _system/memory/MEMORY.md`.

**How to apply:**
- After writing a memory: write the note, add its one-line pointer to `MEMORY.md`, then copy the note into the other location so both match. **If one dir looks thin, repopulate it FROM the fuller one** — never overwrite the mirror's MEMORY.md with a thin copy.
- The mirror's `MEMORY.md` is git-tracked → if you clobber it, `git checkout HEAD -- _system/memory/MEMORY.md` restores it. Re-read after writing ([[verify-canonical-state-edits-persist]]).
