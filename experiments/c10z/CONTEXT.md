---
id: c10z
family: c10
title: 'Pre-registration — D-C10z-astra: a forward-only joint output-margin solve (ASTRA) written into selected `W_down` columns, against the closed-form band write, on the C10 harness (queue row 5b) (v2.2, 2026-10-07)'
status: verdict
decision_ids:
- D-C10z-a1pop
- D-C10z-a4
- D-C10z-v7diag
corpus: null
prereg:
  path: experiments/c10z/design/C10Z_ASTRA_PREREG.md
  sha256: 5ad59d2c960b44d18b5d1c5410028b969aab93298eed5d42c527bd81a4d18eac
code:
- code/lab/track_c/c10z_astra_arms.py
- code/lab/track_c/c10z_astra_benchmark.py
- code/lab/track_c/c10z_v7_diag.py
models:
- Qwen/Qwen2.5-3B
runs:
- experiments/c10z/runs/c10z_astra
- experiments/c10z/runs/c10z_astra_attempt2
- experiments/c10z/runs/c10z_astra_attempt3
- experiments/c10z/runs/c10z_astra_attempt4
- experiments/c10z/runs/c10z_astra_attempt4_infrafail_20261009T234321Z
- experiments/c10z/runs/c10z_astra_attempt4_prep
- experiments/c10z/runs/c10z_astra_benchmark
- experiments/c10z/runs/c10z_astra_z0_probe
- experiments/c10z/runs/c10z_v7_diagnostic
started: null
closed: null
supersedes: null
---

# Experiment record

Use the frontmatter to locate the record's sources.
Read the cited sources for claims and verdicts.

- `design/` holds the preregistration, amendments, scope, and build briefs.
- `reviews/` holds reviews.
- `rulings/` holds operator rulings.
- `runs/<slug>/` holds each run's results, logs, halts, and bulk receipts.

