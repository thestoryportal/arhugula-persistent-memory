# _index

**Job:** Holds the generated indexes and the old-path map.
**Read it when:** You list experiments, projects, evidence or checkpoints, or you resolve an old path.
**Written by:** `code/state/build_index.py` (writes the indexes and the path maps); `code/state/render_state.py` (writes `_index/program-state.md`).
**Read by:** `code/state/resolve_path.py` (reads the path map); `code/gates/closeout_check.py` (reads `_index/program-state.md`).
**Not here:** Hand-kept records: `experiments/`, `evidence/`. Edit rules for generated files: `code/state/ANTI_DRIFT.md`.
