#!/bin/bash
# Tile every team tmux session in one window (tmux session "dashboard"), view-only.
# Each tile re-copies the newest lines of one session's screen every 2 s (capture-pane); nothing
# attaches to the agents' sessions, so watching can never resize or type into them.
# Usage: bash tools/team_dashboard.sh     Leave: Ctrl-b then d.     Close: tmux kill-session -t dashboard
D=dashboard
tmux has-session -t "$D" 2>/dev/null && tmux kill-session -t "$D"
names=$(tmux list-sessions -F '#{session_name}' | grep -vx "$D")
[ -n "$names" ] || { echo "no tmux sessions running"; exit 1; }
first=1
for n in $names; do
  cmd="while :; do c=\$(tput cols); l=\$(tput lines); out=\$(tmux capture-pane -p -t '$n' 2>&1 | grep -v '^[[:space:]]*\$' | tail -n \$l | cut -c1-\$c); clear; printf '%s' \"\$out\"; sleep 2; done"
  if [ $first = 1 ]; then
    tmux new-session -d -s "$D" -x 320 -y 90 "$cmd"
    first=0
  else
    tmux split-window -t "$D" "$cmd"
    tmux select-layout -t "$D" tiled >/dev/null
  fi
  tmux set-option -p -t "$D" @name "$n"
done
tmux select-layout -t "$D" tiled >/dev/null
tmux set-option -t "$D" pane-border-status top >/dev/null
tmux set-option -t "$D" pane-border-format " #{@name} " >/dev/null
if [ -n "$TMUX" ]; then tmux switch-client -t "$D"; else tmux attach-session -t "$D"; fi
