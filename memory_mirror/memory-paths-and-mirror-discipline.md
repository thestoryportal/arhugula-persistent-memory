---
name: memory-paths-and-mirror-discipline
description: "Two memory dirs (harness-live -workspace/memory vs durable git-tracked /workspace/memory_mirror); pod restart wipes the live one; never cp a thin live dir over the mirror's full MEMORY.md index"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 7e49dca7-c684-465a-936b-1c2ce4852502
---

Memory lives in TWO places and they can desync:
- **Harness-live:** `/root/.claude/projects/-workspace/memory/` (what recall reads this session; the system-reminder names this path). On `/root` — **a pod restart can wipe it** (it was down to ~6 files this session while the archive had 34).
- **Durable archive:** `/workspace/memory_mirror/` — git-tracked, on the persistent volume, the **canonical full set + MEMORY.md index** (40+ lines). This is the recovery source.
- (A stale third path `/root/.claude/projects/-root/memory/` exists from earlier sessions — ignore; the live path is `-workspace`.)

**Trap hit 2026-06-20:** `cp $LIVE/*.md $MIRROR/` blindly copied a thin (restart-wiped) live dir over the mirror — **clobbering the mirror's full MEMORY.md with a 1-line stub.** Recovered via `git checkout HEAD -- memory_mirror/MEMORY.md`.

**How to apply:**
- After writing a memory: write to the live path, append the one-line pointer to `MEMORY.md`, then mirror. But **if the live dir looks thin (post-restart), repopulate it FROM the mirror first** (`cp $MIRROR/*.md $LIVE/`), don't overwrite the mirror with it.
- The mirror's `MEMORY.md` is git-tracked → if you clobber it, `git checkout HEAD -- memory_mirror/MEMORY.md` restores it. Re-read after writing ([[verify-canonical-state-edits-persist]]).
- Same pod-restart cause as [[pod-restart-wipes-system-python-ml-stack]].
