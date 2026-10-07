#!/bin/bash
# Team dashboard (tmux session "dashboard"), view-only: the lead session as a large tile on top, every
# other team session in rows of up to five below, each with a coloured header and live status
# (tools/dashboard_tile.sh), and a status bar with the GPU job and status counts (tools/dashboard_bar.sh).
# Nothing attaches to the agents' sessions. Re-running rebuilds it in place for anyone watching.
# Usage: bash tools/team_dashboard.sh     Leave: Ctrl-b then d.     Close: tmux kill-session -t dashboard
T=$(cd "$(dirname "$0")" && pwd)
D=dashboard NEW=dashboard_new LEAD=program PER_ROW=5
COLORS=(30 64 130 96 24 166 61 100 131 67 136 72)

label() {
  case $1 in
    program) echo "LEAD · program session" ;;
    codex)   echo "Codex A · reviews" ;;
    codexb)  echo "Codex B · step-4 build" ;;
    codexh)  echo "Codex H · step-5 build" ;;
    codexi)  echo "Codex I · ASTRA build" ;;
    codexj)  echo "Codex J · step-3 reader" ;;
    codex?)  echo "Codex $(printf '%s' "${1:5:1}" | tr a-z A-Z)" ;;
    *)       echo "$1" ;;
  esac
}
tile() { printf "bash '%s/dashboard_tile.sh' '%s' '%s' '%s'" "$T" "$1" "$(label "$1")" "$2"; }

others=()
for s in $(tmux list-sessions -F '#{session_name}'); do
  case $s in "$D"|"$NEW"|"$LEAD") ;; *) others+=("$s") ;; esac
done
tmux has-session -t "$LEAD" 2>/dev/null || { echo "no '$LEAD' session"; exit 1; }
size=$(tmux list-clients -t "$D" -F '#{client_width} #{client_height}' 2>/dev/null | head -1)
read -r W H <<<"${size:-300 80}"
tmux has-session -t "$NEW" 2>/dev/null && tmux kill-session -t "$NEW"

tmux new-session -d -s "$NEW" -x "$W" -y "$H" "$(tile "$LEAD" 25)"
n=${#others[@]}
if (( n > 0 )); then
  rows=$(( (n + PER_ROW - 1) / PER_ROW ))
  row_first=$(tmux split-window -v -P -F '#{pane_id}' -t "$NEW" -l 60% "$(tile "${others[0]}" "${COLORS[0]}")")
  starts=("$row_first")
  for (( r = 1; r < rows; r++ )); do   # carve the bottom area into equal rows
    i=$(( r * PER_ROW ))
    pct=$(( (rows - r) * 100 / (rows - r + 1) ))
    starts+=("$(tmux split-window -v -P -F '#{pane_id}' -t "${starts[r-1]}" -l "$pct%" "$(tile "${others[i]}" "${COLORS[i % 12]}")")")
  done
  for (( r = 0; r < rows; r++ )); do   # carve each row into equal columns
    first=$(( r * PER_ROW )) last=$(( first + PER_ROW < n ? first + PER_ROW : n ))
    k=$(( last - first )) prev=${starts[r]}
    for (( j = 1; j < k; j++ )); do
      i=$(( first + j )) pct=$(( (k - j) * 100 / (k - j + 1) ))
      prev=$(tmux split-window -h -P -F '#{pane_id}' -t "$prev" -l "$pct%" "$(tile "${others[i]}" "${COLORS[i % 12]}")")
    done
  done
fi

tmux set-option -t "$NEW" pane-border-lines heavy >/dev/null
tmux set-option -t "$NEW" pane-border-style "fg=colour238" >/dev/null
tmux set-option -t "$NEW" pane-active-border-style "fg=colour238" >/dev/null
tmux set-option -t "$NEW" status-style "bg=colour235,fg=colour252" >/dev/null
tmux set-option -t "$NEW" status-left "#[bg=colour25,fg=colour231,bold]  LLM-as-Database · TEAM DASHBOARD  #[default] " >/dev/null
tmux set-option -t "$NEW" status-left-length 50 >/dev/null
tmux set-option -t "$NEW" status-right "#(bash '$T/dashboard_bar.sh')   #[fg=colour231,bold]%H:%M " >/dev/null
tmux set-option -t "$NEW" status-right-length 150 >/dev/null
tmux set-option -t "$NEW" status-interval 3 >/dev/null
tmux set-option -t "$NEW" window-status-format "" >/dev/null
tmux set-option -t "$NEW" window-status-current-format "" >/dev/null

for c in $(tmux list-clients -t "$D" -F '#{client_tty}' 2>/dev/null); do tmux switch-client -c "$c" -t "$NEW"; done
tmux has-session -t "$D" 2>/dev/null && tmux kill-session -t "$D"
tmux rename-session -t "$NEW" "$D"
if [ -t 1 ] && [ -z "$TMUX" ]; then tmux attach-session -t "$D"; fi
