---
name: gpu-gate-blocks-any-python
description: "The C10W P2 per-stage gate (and gates built by analogy, e.g. P3) refuses to dispatch if ANY python process is running — system python3 included — so builds, test suites, reviewers' python probes and close-out scripts can stop a live GPU run."
metadata:
  type: project
---

`tools/c10w_p2_gate.py:22` matches any executable named python*/Python (case-insensitive) that is not on its exact-command EXEMPT list; a refusal makes `run_c10w_p2.sh` exit (finish 6). Found 2026-10-07 22:10 by the advisor's re-check of C10Z §9.1 (blocking N1). `run_c10v_stage.sh:7` has the same kind of rule.

**Why:** fail-closed GPU exclusivity (one GPU run at a time). Short foreground python3 calls only collide if they overlap a stage dispatch (a few seconds per ~7-min stage), but builds/test suites run for minutes.

**How to apply:** while a GPU coordinator is live, run no `.venv` python except the exempt readers; keep any system python3 (render_state, closeout_check, board_fmt, pre-commit hook) short and foreground, never backgrounded; tell subagents and Codex reviewers the same. Codex builds (e.g. the C10Z/ASTRA build) start only after `COORDINATOR_EXIT=` and no other GPU stage pending. Scope (2026-10-08): the rule protects a *pending gated stage*. Once a coordinator is past its last gated stage (e.g. the P2 re-attempt: one `p2-eval` stage, then only the ungated read, `run_c10w_p2.sh:57–66`), python can no longer stop it — lift the freeze for light CPU work (PYTHON-OK) and re-impose it before the next gated launch. Also: a watcher started as `python3 -B <path>` is NOT exempt (the regex expects the script path right after the interpreter) — start it without -B. Related: [[c10k-route-a-resume]], [[model-and-compute-allocation]].
