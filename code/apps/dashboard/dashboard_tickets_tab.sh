#!/bin/bash
# The dashboard's 'tickets' tab: every lean ticket with live timers, a timeline, review rounds and findings.
# Adds one window only. A no-op when the session already has a 'tickets' window.
# code/apps/dashboard/team_dashboard.sh calls this for every build, so the tab is defined only here.
# The view reads every G-build/LEAN/*/ folder that has tickets/ (dashboard_tickets.LEAN).
# Usage: bash code/apps/dashboard/dashboard_tickets_tab.sh [session]   (default: dashboard)
T=$(cd "$(dirname "$0")" && pwd)
S=${1:-dashboard}
windows=$(tmux list-windows -t "=$S" -F '#{window_name}') || { echo "dashboard_tickets_tab: no '$S' session to add the tab to (code/apps/dashboard/team_dashboard.sh builds it)" >&2; exit 1; }
if grep -qx tickets <<<"$windows"; then
  echo "dashboard_tickets_tab: '$S' already has a tickets tab; nothing to do"
  exit 0
fi
tmux new-window -d -t "=$S:" -n tickets "/usr/bin/python3 '$T/dashboard_tickets.py'" || { echo "dashboard_tickets_tab: tmux new-window failed" >&2; exit 1; }
echo "dashboard_tickets_tab: added the tickets tab to '$S'"
