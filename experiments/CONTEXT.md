# experiments

**Job:** Holds one record per experiment: design, reviews, rulings and run results. Each record lives in `experiments/<id>/`. Its guide is `experiments/<id>/CONTEXT.md`. Use the id from `_index/experiments.md` to open that guide.
**Read it when:** You run or read an experiment.
**Written by:** Writer search: none found. Run scripts live in `code/lab/runners/`; a script that names its output folder is the writer.
**Read by:** `code/apps/dashboard/dashboard_experiment.py`; `code/apps/dashboard/dashboard_live.py`; `code/state/build_index.py`.
**Not here:** The list of records: `_index/experiments.md`. Ledger entries: `_index/evidence.md`. The ledger entry files: `evidence/CORPUS/`. Close-out rule: `_system/governance/DISCIPLINE.md`.
