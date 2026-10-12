#!/bin/bash
# The dashboard's 'queue' tab: plain words for current and queued work.
# Adds one window only. A no-op when the session already has a 'queue' window.
# code/apps/dashboard/team_dashboard.sh calls this for every build, so the tab is defined only here.
# Usage: bash code/apps/dashboard/dashboard_queue_tab.sh [session]   (default: dashboard)
T=$(cd "$(dirname "$0")" && pwd)
S=${1:-dashboard}
windows=$(tmux list-windows -t "=$S" -F '#{window_name}') || { echo "dashboard_queue_tab: no '$S' session to add the tab to (code/apps/dashboard/team_dashboard.sh builds it)" >&2; exit 1; }
if grep -qx queue <<<"$windows"; then
  echo "dashboard_queue_tab: '$S' already has a queue tab; nothing to do"
  exit 0
fi
tmux new-window -d -t "=$S:" -n queue "/usr/bin/python3 '$T/dashboard_queue.py'" || { echo "dashboard_queue_tab: tmux new-window failed" >&2; exit 1; }
echo "dashboard_queue_tab: added the queue tab to '$S'"
