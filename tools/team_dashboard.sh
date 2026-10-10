#!/bin/bash
# Team dashboard (tmux session "dashboard"), view-only: the lead session and the Science Report
# (tools/dashboard_report.py, from docs/c10_scoreboard.json) side by side on top, every
# other team session in rows of up to five below, each with a coloured header and live status
# (tools/dashboard_tile.py), and a status bar with the GPU job and status counts (tools/dashboard_bar.sh).
# Nothing attaches to the agents' sessions. Re-running rebuilds it in place for anyone watching.
# Tabs: 1 team · 2 active (busy agents) · 3 experiment (GPU run, live) · 4 mathlab · 5 helpers · 6 science (the Science Report
# full width) (+ one ⚙ tab per running helper agent). Switch: Ctrl-b then 1-6, or Ctrl-b n / p for next / previous.
# The lead session is LEAD if set, else found: the newest tmux session with a Claude Code pane working in this repo
# (dashboard_live.lead_session). Usage: [LEAD=<session>] bash tools/team_dashboard.sh
# (or ~/.local/bin/teamdash [team|active|exp|mathlab|science])   Leave: Ctrl-b d   Close: tmux kill-session -t dashboard
T=$(cd "$(dirname "$0")" && pwd)
D=dashboard NEW=dashboard_new PER_ROW=5
LEAD=$(/usr/bin/python3 "$T/dashboard_live.py" --lead) || { echo "team_dashboard: finding the lead session failed (see above)" >&2; exit 1; }
COLORS=(30 64 130 96 24 166 61 100 131 67 136 72)

label() {
  case $1 in
    "$LEAD") echo "LEAD · $LEAD session" ;;
    codex)   echo "Codex A · reviews" ;;
    codexb)  echo "Codex B · step-4 build" ;;
    codexh)  echo "Codex H · step-5 build" ;;
    codexi)  echo "Codex I · ASTRA build" ;;
    codexj)  echo "Codex J · step-3 reader" ;;
    codexviz) echo "Codex · Lab View build" ;;
    codexviz2) echo "Codex · Lab View v2 build" ;;
    codexz)  echo "Codex Z · ASTRA build" ;;
    codexw2) echo "Codex W2 · P2 rerun fix" ;;
    codexx)  echo "Codex X · step-6 build" ;;
    codexy)  echo "Codex Y · step-7 build" ;;
    codexml) echo "Codex ML · math-lab dashboard" ;;
    codexmb) echo "Codex MB · math-lab build" ;;
    codexz2) echo "Codex Z2 · ASTRA V7 probe" ;;
    codex?)  echo "Codex $(printf '%s' "${1:5:1}" | tr a-z A-Z)" ;;
    *)       echo "$1" ;;
  esac
}
tile() { printf "/usr/bin/python3 '%s/dashboard_tile.py' '%s' '%s' '%s'" "$T" "$1" "$(label "$1")" "$2"; }
no_lead() { echo "printf '\\n  LEAD · no lead session found: no tmux session has a Claude Code pane working in this repo.\\n  Start one, or set LEAD=<session>, and re-run tools/team_dashboard.sh.\\n'; exec tail -f /dev/null"; }

others=()
for s in $(tmux list-sessions -F '#{session_name}'); do
  case $s in "$D"|"$NEW"|"$LEAD"|helpers|view-*) ;; *) others+=("$s") ;; esac
done
size=$(tmux list-clients -F '#{client_width} #{client_height}' 2>/dev/null | sort -n -r | head -1)   # build at the largest viewer's size
read -r W H <<<"${size:-300 80}"
tmux has-session -t "$NEW" 2>/dev/null && tmux kill-session -t "$NEW"

lead=$(tmux new-session -d -P -F '#{pane_id}' -s "$NEW" -x "$W" -y "$H" -e "LEAD=$LEAD" "$([ -n "$LEAD" ] && tile "$LEAD" 25 || no_lead)")
n=${#others[@]}
if (( n > 0 )); then
  rows=$(( (n + PER_ROW - 1) / PER_ROW ))
  row_first=$(tmux split-window -v -P -F '#{pane_id}' -t "$lead" -l 50% "$(tile "${others[0]}" "${COLORS[0]}")")
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

tmux split-window -h -t "$lead" -l 50% "/usr/bin/python3 '$T/dashboard_report.py'"   # Science Report beside the lead
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
tmux set-option -t "$NEW" window-status-format "#[fg=colour250] #I #W " >/dev/null
tmux set-option -t "$NEW" window-status-current-format "#[bg=colour214,fg=colour16,bold] #I #W " >/dev/null

for c in $(tmux list-clients -F '#{client_tty} #{client_session}' | awk -v d="$D" '$2 == d || $2 ~ /^view-/ {print $1}'); do tmux switch-client -c "$c" -t "$NEW"; done
tmux has-session -t "=$D" 2>/dev/null && tmux kill-session -t "=$D"   # exact name: a bare "dashboard" prefix-matches dashboard_new on a fresh server and kills the new build
tmux rename-session -t "$NEW" "$D"
if [ -t 1 ] && [ -z "$TMUX" ] && [ -z "$TEAMDASH_NO_ATTACH" ]; then tmux attach-session -t "$D"; fi
