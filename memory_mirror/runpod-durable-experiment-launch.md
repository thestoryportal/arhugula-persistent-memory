---
name: runpod-durable-experiment-launch
description: "How to launch long MEMIT experiments on the RunPod pod so terminal disconnects don't kill them"
metadata: 
  node_type: memory
  type: project
  originSessionId: 2801cf2e-560f-460c-86df-e227b16051b2
---

On the RunPod RTX 4090 pod, the Claude Code terminal session disconnects intermittently. A normally-launched experiment is a child of the claude process's session and dies (SIGHUP cascade) when the session drops — confirmed 2026-06-17 when the GPT-J GATE-CAL run (PID 44350) and its bash wrapper vanished together, GPU freed, no output.

**Fix:** launch detached in its own session with `setsid`, and unbuffered for live progress:
```
cd /workspace && setsid bash -c 'cd /workspace && PYTHONUNBUFFERED=1 MODEL=gptj python -u s241_gatecal.py > LOG 2>&1' </dev/null >/dev/null 2>&1 & disown
```
Verify detachment: the python's SID must differ from claude's SID (`ps -o sid`). Then a disconnect's SIGHUP cannot reach it; it reparents to init and keeps running.

**Why:** `-u`/PYTHONUNBUFFERED only changes stdout flush timing — it does NOT affect computation, determinism, or JSON results (bit-identical run). Buffered stdout otherwise hides all per-step progress in the log, making a working run look frozen.

See [[memit-cov-inversion-not-a-hang]] for the misleading "frozen log" symptom. Durable state lives in `/workspace/SESSION_CHECKPOINT.md`.
