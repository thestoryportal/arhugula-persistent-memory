# program

**Job:** Holds the program state: the north star, the position, the next actions, and the session record.
**Read it when:** You continue the program or ask what is next. Read `program/STATUS.md` first.
**Written by:** `code/state/render_state.py` with `--write` renders `program/STATUS.md`, `_index/program-state.md`, and `program/scorecard.md`. Writer of `program/program_state.json`: none found.
**Read by:** `code/state/render_state.py`; `code/apps/dashboard/dashboard_queue.py` (both read `program/program_state.json`).
**Not here:** Full state view: `_index/program-state.md`. Experiment records: `experiments/CONTEXT.md`.
