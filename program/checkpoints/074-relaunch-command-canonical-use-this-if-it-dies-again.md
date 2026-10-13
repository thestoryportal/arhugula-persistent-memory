## Relaunch command (canonical — use this if it dies again)
```
cd /workspace && setsid bash -c 'cd /workspace && PYTHONUNBUFFERED=1 MODEL=gptj python -u s241_gatecal.py > s241_gatecal_gptj.log 2>&1' </dev/null >/dev/null 2>&1 & disown
```
For Qwen: same with `MODEL=qwen` → `s241_gatecal_qwen.log`. Expect ~tens of minutes (6 layer cov inversions on CPU, then fast GPU edits). Done when `s241_gatecal_<model>.json` exists and log prints `=== GATE-CAL ===`.

