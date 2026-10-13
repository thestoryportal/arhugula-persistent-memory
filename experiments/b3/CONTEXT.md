---
id: b3
family: track_b
title: edits survive real Q4_K_M quantization
status: verdict
decision_ids:
- D-B3-1
corpus: '17'
prereg: null
code:
- code/lab/track_b/b3_run.sh
models: []
runs:
- experiments/b3/runs/b3_edit
- experiments/b3/runs/b3_margin
- experiments/b3/runs/b3_pred_f16
- experiments/b3/runs/b3_pred_q4
- experiments/b3/runs/b3_quant_survival
started: null
closed: null
supersedes: null
---

# Experiment record

Use the frontmatter to locate the record's sources.
Read the cited sources for claims and verdicts.

Standard record folders. A folder exists only when it has content.
- `design/` holds the preregistration, amendments, scope, and build briefs.
- `reviews/` holds reviews.
- `rulings/` holds operator rulings.
- `runs/<slug>/` holds each run's results, logs, halts, and bulk receipts.

