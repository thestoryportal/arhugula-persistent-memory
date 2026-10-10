---
name: autonomy-driver-stale-guard-deletes-result
description: autonomy_driver.py unlinks result_json before running the unit (dry-run now guarded); keep expensive results derivable from arm JSONs
metadata:
  type: reference
---

`tools/autonomy_driver.py` runs a per-unit "stale-result guard" that `rj.unlink()`s the unit's `label_rule.result_json` so a prior night's JSON isn't misread as this run's output. It expects the unit command to regenerate it.

**Two hazards:**
1. **Dry-run used to delete it too** — the unlink ran *before* the `--dry-run` check, so a harmless-looking `--dry-run` destroyed a real artifact (it deleted `results/c2band_compare_result.json` on 2026-06-20). **FIXED:** `tools/autonomy_driver.py:269-270` now reads `if rj.exists() and not args.dry_run:` before the unlink.
2. **Even in a real run**, if the regenerating command fails, the old result is already gone. For results that cost GPU-hours (not cheaply regenerable), this is dangerous.

**How to apply:** (a) never `--dry-run` the driver against a mission whose `result_json` points at an artifact you want to keep, unless on the fixed version; (b) keep expensive combined results **derivable from their source/arm JSONs** — `c2band_compare_result.json` was regenerated exactly from `results/g6_scale_n_result_c2band_{base,812}.json` via the same combine logic as `band_corruption_compare.py main()`, no GPU re-run; (c) untracked results aren't recoverable from git — the arm JSONs were the save. Related: [[durable-artifact-path-collision]], [[verify-canonical-state-edits-persist]].
