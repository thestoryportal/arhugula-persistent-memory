---
name: gpu-gate-refuses-any-venv-python
description: tools/c10w_p2_gate.check_gpu refuses dispatch while ANY .venv python runs (incl. Codex CPU unittests); poll until clear twice, then launch
metadata:
  type: project
---

2026-10-09: the first V7 probe launch (results/c10z_v7_diagnostic/20261009T182053Z) exited 3 pre-load because Codex ML's LabViz unittest (`.venv/bin/python -m unittest …`) was running. Correct fail-closed behavior; Astra ruled it a non-run (no attempt consumed, no reading-around). With 4–5 Codex builders active, a .venv python is running most of the time.

**Why:** check_gpu (tools/c10w_p2_gate.py:73) blocks on every matching python process and on named tmux sessions; it cannot tell a CPU test from a GPU job.

**How to apply:** launch GPU jobs via a background loop that calls `check_gpu()['ok']` every 3 s and dispatches only after two consecutive clears (worked after ~52 polls). Never weaken the gate. Related: [[never-idle-arm-completion-watch]].
