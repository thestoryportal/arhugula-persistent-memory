#!/bin/bash
# Team dashboard: one self-composing Team pane re-lists the lead and live Codex builders
# every 3 s. Its full-roster counts feed tools/dashboard_bar.sh.
# Nothing attaches to the agents' sessions. Re-running rebuilds it in place for anyone watching.
# Tabs: 1 team · 2 active (busy agents) · 3 experiment (GPU run, live) · 4 mathlab · 5 helpers · 6 science (the Science Report
# full width) · 7 storage · 8 queue (+ one ⚙ tab per running helper agent). Switch: Ctrl-b then 1-8, or Ctrl-b n / p for next / previous.
# The lead session is LEAD if set, else found: the newest tmux session with a Claude Code pane working in this repo
# (dashboard_live.lead_session). Usage: [LEAD=<session>] bash tools/team_dashboard.sh
# (or ~/.local/bin/teamdash [team|active|exp|mathlab|science])   Leave: Ctrl-b d   Close: tmux kill-session -t dashboard
T=$(cd "$(dirname "$0")" && pwd)
D=dashboard NEW=dashboard_new
size=$(tmux list-clients -F '#{client_width} #{client_height}' 2>/dev/null | sort -n -r | head -1)   # build at the largest viewer's size
read -r W H <<<"${size:-300 80}"
tmux has-session -t "$NEW" 2>/dev/null && tmux kill-session -t "$NEW"

tmux new-session -d -s "$NEW" -x "$W" -y "$H" -e "LEAD=${LEAD:-}" "/usr/bin/python3 '$T/dashboard_team.py'" || exit 1
tmux set-option -t "$NEW" remain-on-exit on >/dev/null   # a crashed tile stays visible with its error
tmux set-option -t "$NEW" pane-border-lines heavy >/dev/null
tmux set-option -t "$NEW" pane-border-style "fg=colour238" >/dev/null
tmux set-option -t "$NEW" pane-active-border-style "fg=colour238" >/dev/null
tmux set-option -t "$NEW" status-style "bg=colour235,fg=colour252" >/dev/null
tmux set-option -t "$NEW" status-left "#[bg=colour25,fg=colour231,bold]  LLM-as-Database · TEAM DASHBOARD  #[default] " >/dev/null
tmux set-option -t "$NEW" status-left-length 50 >/dev/null
tmux set-option -t "$NEW" status-right "#(bash '$T/dashboard_bar.sh')   #[fg=colour231,bold]%H:%M " >/dev/null
tmux set-option -t "$NEW" status-right-length 150 >/dev/null
tmux set-option -t "$NEW" status-interval 3 >/dev/null
tmux rename-window -t "$NEW" team
tmux new-window -d -t "$NEW" -n active "/usr/bin/python3 '$T/dashboard_active.py'"
tmux new-window -d -t "$NEW" -n experiment "/usr/bin/python3 '$T/dashboard_experiment.py'"
tmux new-window -d -t "$NEW" -n mathlab "/usr/bin/python3 '$T/dashboard_mathlab.py'"
tmux new-window -d -t "$NEW" -n helpers "/usr/bin/python3 '$T/dashboard_subagents.py' manager"   # opens/closes a tab per running helper agent
bash "$T/dashboard_science_tab.sh" "$NEW" >/dev/null || exit 1   # the Science Report alone, full width (its message goes to stderr on failure)
bash "$T/dashboard_storage_tab.sh" "$NEW" >/dev/null || exit 1   # Drive backup and project disks, full width
bash "$T/dashboard_queue_tab.sh" "$NEW" >/dev/null || exit 1   # current and queued work in plain words
tmux set-option -t "$NEW" window-status-format "#[fg=colour250] #I #W " >/dev/null
tmux set-option -t "$NEW" window-status-current-format "#[bg=colour214,fg=colour16,bold] #I #W " >/dev/null

for c in $(tmux list-clients -F '#{client_tty} #{client_session}' | awk -v d="$D" '$2 == d || $2 ~ /^view-/ {print $1}'); do tmux switch-client -c "$c" -t "$NEW"; done
tmux has-session -t "=$D" 2>/dev/null && tmux kill-session -t "=$D"   # exact name: a bare "dashboard" prefix-matches dashboard_new on a fresh server and kills the new build
tmux rename-session -t "$NEW" "$D"
if [ -t 1 ] && [ -z "$TMUX" ] && [ -z "$TEAMDASH_NO_ATTACH" ]; then tmux attach-session -t "$D"; fi
