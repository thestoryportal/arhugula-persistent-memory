# program/checkpoints

**Job:** Holds one handoff block per file, from the split session checkpoint.
**Read it when:** You take over a session. `_index/checkpoints.md` names the newest live handoff.
**Written by:** Writer search: none found.
**Read by:** `code/state/build_index.py` (indexes them); `code/state/llmdb_records.py` (reads the split parts whole).
**Not here:** The index: `_index/checkpoints.md`. Memory lessons: `_system/memory/`.
