# Codex brief — review the replay clone lock before the D-C10r-exp2ctl rerun

Review only: no model, no GPU; edit nothing but your output file **`results/c10r_exp2ctl_lock_codex_review.md`**; `/usr/bin/git`. Then say DONE.

Context: `architecture_profile/c10r_exp2ctl_halt_diagnostic.json` and `results/c10r_exp2ctl_run1_invalid_2026-10-06.md`. Graft rewrote tracked files in the frozen replay clone (`.gitignore`, then `graft/.cache/ask-index.json`), and the frozen-checkout check correctly invalidated the run. Operator ruling D-C10r-rulings-7: rerun with the clone locked read-only right after setup.

New file: `experiments/track_c/autoresearch_c10/replay_exp2/lock_clone.py`. A dry run on the spent r2 clone printed `LOCK PASS: 19 files read-only, 3 subdirectories unwritable`. Procedure for the rerun: `setup_replay.sh <DEST_r3>` → `lock_clone.py <DEST_r3>` → `tokenizer_precheck.py <DEST_r3>` → `REPLAY_EXCLUSIVE_WINDOW=paused-no-relaunch run_replay.sh <DEST_r3>`. You wrote the v3.1 replay driver, so check the lock against it:

1. Does any step of the precheck, runner, recipe (`edit.py` at 92acd03 plus the frozen patch), scorer (`prepare.py --score`) or reader write to, rename over, or chmod an EXISTING file or directory inside DEST other than DEST itself (for example `results.tsv`, `run.log`, `prepare.log`, `.hparams_*.json`, `__pycache__`, anything under `graft/`, the setup records)? If yes, name it and whether the lock would break the run.
2. Does any check read file modes, or does git report a mode change on tracked files (0444 vs 0644 is not tracked; confirm)?
3. Is skipping `.git` and the `.venv` symlink safe, and is there another writer path (for example graft writing into `.git`, or the precheck's temporary-file rename at DEST root) the lock misses?
4. Verdict: **PROCEED or FIX-FIRST** with exact fixes.
