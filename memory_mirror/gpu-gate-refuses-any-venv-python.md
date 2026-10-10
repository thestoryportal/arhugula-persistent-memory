---
name: gpu-gate-refuses-any-venv-python
description: GPU gate (c10w_p2_gate.check_gpu) refuses on ANY python process; poll until clear twice, then launch; keep python short while a stage is pending
metadata:
  type: project
---

2026-10-09: the first V7 probe launch (results/c10z_v7_diagnostic/20261009T182053Z) exited 3 pre-load because Codex ML's LabViz unittest (`.venv/bin/python -m unittest …`) was running. Correct fail-closed behavior; Astra ruled it a non-run (no attempt consumed, no reading-around). With 4–5 Codex builders active, a .venv python is running most of the time.

**Why:** check_gpu (`tools/c10w_p2_gate.py:73`) blocks on every process whose executable matches `COMPUTE_EXE` (`:22`, any `python*`/`Python` incl. system python3, plus ollama/llama/mlx) unless its exact command is on the `EXEMPT` list, and on an `autoresearch` tmux session; it cannot tell a CPU test from a GPU job. `run_c10v_stage.sh:7` has the same kind of rule. Found first on 2026-10-07 by the advisor's re-check of C10Z §9.1.

**How to apply:** launch GPU jobs via a background loop that calls `check_gpu()['ok']` every 3 s and dispatches only after two consecutive clears (worked after ~52 polls). Never weaken the gate. While a gated stage is pending, run no `.venv` python except the exempt readers; keep system python3 calls (render_state, closeout_check, pre-commit hook) short and foreground; tell subagents and Codex the same; Codex builds start only after `COORDINATOR_EXIT=` with no other GPU stage pending. Scope: the rule protects a *pending gated stage* — once a coordinator is past its last gated stage (e.g. the P2 re-attempt's `p2-eval`, then only the ungated read, `run_c10w_p2.sh:57–66`), lift the freeze for light CPU work and re-impose it before the next gated launch. A watcher started as `python3 -B <path>` is NOT exempt (the regex expects the script path right after the interpreter) — start it without -B.

**Teamdash trap (2026-10-10):** the dashboard status bar spawns `dashboard_live.py --gpu-summary` every ~3 s (each <1 s); NEW-1's CPU admission (`A.probe`) counted them as unaccounted GPU blockers and refused (run new1_20261010T025311). Launch right after a poll ends (`until pgrep -f 'dashboard_live.py --gpu-summary'; do sleep .05; done; while pgrep …; do sleep .05; done; launch`) — worked first try. Durable fix (exclude the detector's own polls from blocking_processes) not yet built. Related: [[never-idle-arm-completion-watch]], [[model-and-compute-allocation]].
