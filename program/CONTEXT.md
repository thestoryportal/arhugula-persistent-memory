# program

**Job:** Holds the program state: the north star, the position, the next actions, and the session record. Subfolders: the runbook (`program/runbook/CONTEXT.md`), checkpoints (`program/checkpoints/`) and session records (`program/sessions/`).
**Read it when:** You continue the program or ask what is next. Read `program/STATUS.md` first.
**Written by:** `code/state/render_state.py` with `--write` renders `program/STATUS.md`, `_index/program-state.md`, and `program/scorecard.md`. Writer of `program/program_state.json`: none found.
**Read by:** `code/state/render_state.py`, `code/state/build_index.py`, `code/apps/dashboard/dashboard_queue.py` and `code/apps/dashboard/dashboard_report.py` (all read `program/program_state.json`).
**Not here:** Full state view: `_index/program-state.md`. Experiment records: `experiments/CONTEXT.md`.
