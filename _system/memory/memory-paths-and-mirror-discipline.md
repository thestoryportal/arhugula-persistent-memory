---
name: memory-paths-and-mirror-discipline
description: "Memory lives twice: harness-live ~/.claude/projects/<hash>/memory and git-tracked memory_mirror/; sync one way, never cp a thin dir over MEMORY.md"
metadata:
  type: reference
---

Memory lives in TWO places and they can desync:
- **Harness-live:** `~/.claude/projects/-Volumes-memit-llm-database-poc-mirror/memory/` (52 files at 2026-10-10) — what recall reads in sessions started from the mirror root. Sessions started elsewhere get their own project dir (e.g. `~/.claude/projects/-Volumes-memit-llm-database-poc-mirror-arhugula-persistent-memory/memory/` held 2 files; a worktree session has its own hash and usually no memory dir), so check which path the system-reminder names.
- **Durable archive:** `<repo>/memory_mirror/` — git-tracked, the **canonical full set + MEMORY.md index**. This is the recovery source.
- `tools/closeout_check.py` (lines ~240-257) compares the live dir (`LLMDB_LIVE_MEMORY`, default the first path above) with `memory_mirror/` and reports any live note that is missing from or differs in the mirror, and checks every MEMORY.md link resolves; a missing live dir is reported as WARN, never skipped.

**Trap hit 2026-06-20 (on the pod):** `cp $LIVE/*.md $MIRROR/` blindly copied a thin (restart-wiped) live dir over the mirror — **clobbering the mirror's full MEMORY.md with a 1-line stub.** Recovered via `git checkout HEAD -- memory_mirror/MEMORY.md`.

**How to apply:**
- After writing a memory: write the note, add its one-line pointer to `MEMORY.md`, then copy the note into the other location so both match. **If one dir looks thin, repopulate it FROM the fuller one** — never overwrite the mirror's MEMORY.md with a thin copy.
- The mirror's `MEMORY.md` is git-tracked → if you clobber it, `git checkout HEAD -- memory_mirror/MEMORY.md` restores it. Re-read after writing ([[verify-canonical-state-edits-persist]]).
