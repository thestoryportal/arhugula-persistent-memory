#!/bin/bash
# GPU experiment and counts published by the Team view from its full live roster.
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
gpu=$(python3 -B "$SCRIPT_DIR/dashboard_live.py" --gpu-summary) || exit $?
counts=$(tmux show-options -w -qv -t dashboard:1 @team_counts) || exit $?
printf '%s   │   %s' "$gpu" "${counts:-team counts unavailable}"
