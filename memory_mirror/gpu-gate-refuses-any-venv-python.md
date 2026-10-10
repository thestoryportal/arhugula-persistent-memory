---
name: gpu-gate-refuses-any-venv-python
description: tools/c10w_p2_gate.check_gpu refuses dispatch while ANY .venv python runs (incl. Codex CPU unittests); poll until clear twice, then launch
metadata:
  type: project
---

2026-10-09: the first V7 probe launch (results/c10z_v7_diagnostic/20261009T182053Z) exited 3 pre-load because Codex ML's LabViz unittest (`.venv/bin/python -m unittest …`) was running. Correct fail-closed behavior; Astra ruled it a non-run (no attempt consumed, no reading-around). With 4–5 Codex builders active, a .venv python is running most of the time.

**Why:** check_gpu (tools/c10w_p2_gate.py:73) blocks on every matching python process and on named tmux sessions; it cannot tell a CPU test from a GPU job.

**How to apply:** launch GPU jobs via a background loop that calls `check_gpu()['ok']` every 3 s and dispatches only after two consecutive clears (worked after ~52 polls). Never weaken the gate. **Teamdash trap (2026-10-10):** the dashboard status bar spawns `dashboard_live.py --gpu-summary` every ~3 s (each <1 s); NEW-1's CPU admission (`A.probe`) counted them as unaccounted GPU blockers and refused (run new1_20261010T025311). Launch right after a poll ends (`until pgrep -f 'dashboard_live.py --gpu-summary'; do sleep .05; done; while pgrep …; do sleep .05; done; launch`) — worked first try. Durable fix (exclude the detector's own polls from blocking_processes) not yet built. Related: [[never-idle-arm-completion-watch]].
