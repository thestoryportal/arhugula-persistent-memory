#!/bin/bash
# The dashboard's 'storage' tab: Drive backup progress/history and cached project disk sizes.
# Adds one window only. A no-op when the session already has a 'storage' window.
# code/apps/dashboard/team_dashboard.sh calls this for every build, so the tab is defined only here.
# Usage: bash code/apps/dashboard/dashboard_storage_tab.sh [session]   (default: dashboard)
T=$(cd "$(dirname "$0")" && pwd)
S=${1:-dashboard}
windows=$(tmux list-windows -t "=$S" -F '#{window_name}') || { echo "dashboard_storage_tab: no '$S' session to add the tab to (code/apps/dashboard/team_dashboard.sh builds it)" >&2; exit 1; }
if grep -qx storage <<<"$windows"; then
  echo "dashboard_storage_tab: '$S' already has a storage tab; nothing to do"
  exit 0
fi
tmux new-window -d -t "=$S:" -n storage "/usr/bin/python3 '$T/dashboard_storage.py'" || { echo "dashboard_storage_tab: tmux new-window failed" >&2; exit 1; }
echo "dashboard_storage_tab: added the storage tab to '$S'"
