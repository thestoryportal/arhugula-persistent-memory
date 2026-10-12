---
name: autonomy-error-label-can-mask-completed-run
description: An autonomy driver can stage LABEL=ERROR while the run completes seconds later; compare result-JSON mtimes to the staging time first
metadata:
  type: reference
---

The `tools/autonomy_driver.py` wall-clock budget (`--budget-min`) can expire *between* a run finishing and the driver's post-run staging firing. Result: `logs/pending_findings/NN_*.md` says `LABEL = ERROR (insufficient wall-clock)` and `(no result JSON produced)`, yet the result files exist with a slightly later mtime.

**How to apply:** before treating any staged ERROR/INVALID as "no result," `ls -la` the expected `results/*.json` and compare mtime to the staged-finding timestamp. If the JSON exists and post-dates the staging, investigate: verify run identity, exit/completion receipts, parseability and every frozen validity gate before supervised fold-in. A later mtime alone proves no completion; never read around a halted or compromised run.

Worked case: C2-band falsifier (2026-06-19) staged ERROR @09:37, but `results/c2band_compare_result.json` @10:01 → completed; mechanical label was actually PASS. See [[pass-label-not-equal-promotable-claim]] (`CORPUS/21`, D-C2band-1).
