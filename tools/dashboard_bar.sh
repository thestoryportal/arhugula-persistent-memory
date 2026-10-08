#!/bin/bash
# Dashboard status-bar text: the GPU experiment running now, and how many tiles are WORKING / ASKING / ACTIVE / IDLE.
# Same rule as script_call + GPU_JOB_RE in dashboard_live.py (canonical): only an interpreter's own script argument counts.
job=$(/bin/ps -axo command | awk '{n=split($1,a,"/"); if (a[n] ~ /^([Pp]ython[0-9.]*|bash|sh)$/) {s=""; for(i=2;i<=NF;i++) if ($i !~ /^-/) s=s" "$i; print s}}' | grep -oE '(experiments/track_c/|tools/(run_)?)c10[a-z][a-z0-9_]*(\.py|_stage\.sh) [A-Za-z0-9-]+' | grep -v ' _job' | head -1)
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
