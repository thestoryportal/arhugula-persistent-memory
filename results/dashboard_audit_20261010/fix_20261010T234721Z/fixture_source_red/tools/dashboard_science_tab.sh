#!/bin/bash
# The dashboard's 'science' tab: the Science Report (tools/dashboard_report.py) alone in a window of its own, full width
# (the report sizes itself from its pane). Adds that one window to a running dashboard session and nothing else: no
# other window or pane is moved, resized or restarted. A no-op when the session already has a 'science' window.
# tools/team_dashboard.sh calls this for every build, so the tab is defined only here.
# Usage: bash tools/dashboard_science_tab.sh [session]   (default: dashboard)
T=$(cd "$(dirname "$0")" && pwd)
S=${1:-dashboard}
windows=$(tmux list-windows -t "=$S" -F '#{window_name}') || { echo "dashboard_science_tab: no '$S' session to add the tab to (tools/team_dashboard.sh builds it)" >&2; exit 1; }
if grep -qx science <<<"$windows"; then
  echo "dashboard_science_tab: '$S' already has a science tab; nothing to do"
  exit 0
fi
tmux new-window -d -t "=$S:" -n science "/usr/bin/python3 '$T/dashboard_report.py'" || { echo "dashboard_science_tab: tmux new-window failed" >&2; exit 1; }
echo "dashboard_science_tab: added the science tab to '$S'"
