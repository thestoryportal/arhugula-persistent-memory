#!/bin/bash
# Dashboard status-bar text: the GPU experiment running now, and how many tiles are WORKING / ASKING / ACTIVE / IDLE.
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
gpu=$(python3 -B "$SCRIPT_DIR/dashboard_live.py" --gpu-summary) || exit $?
st=$(tmux list-panes -s -t dashboard -F '#{@status}' 2>/dev/null)
n() { grep -c "^$1\$" <<<"$st"; }
printf '%s   │   working %s · asking %s · active %s · idle %s' "$gpu" "$(n WORKING)" "$(n ASKING)" "$(n ACTIVE)" "$(n IDLE)"
