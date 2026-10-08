#!/bin/bash
# Dashboard status-bar text: the GPU experiment running now, and how many tiles are WORKING / ASKING / ACTIVE / IDLE.
# Same shape as GPU_JOB_RE in dashboard_live.py (the canonical definition): driver, program tool or stage wrapper + its stage.
job=$(/bin/ps -axo command | grep -oE '(experiments/track_c/|tools/(run_)?)c10[a-z][a-z0-9_]*(\.py|_stage\.sh) [A-Za-z0-9-]+' | grep -v ' _job' | head -1)
if [ -n "$job" ]; then
  key=$(grep -oE 'c10[a-z]' <<<"$job" | head -1)
  case ${key:0:4} in
    c10u) name="step 3" ;; c10v) name="step 4" ;; c10w) name="step 5" ;;
    c10x) name="step 6" ;; c10y) name="step 7" ;; c10z) name="ASTRA" ;; *) name=${key:0:4} ;;
  esac
  gpu="GPU: $name · stage ${job##* } running"
else
  gpu="GPU: idle"
fi
st=$(tmux list-panes -s -t dashboard -F '#{@status}' 2>/dev/null)
n() { grep -c "^$1\$" <<<"$st"; }
printf '%s   │   working %s · asking %s · active %s · idle %s' "$gpu" "$(n WORKING)" "$(n ASKING)" "$(n ACTIVE)" "$(n IDLE)"
