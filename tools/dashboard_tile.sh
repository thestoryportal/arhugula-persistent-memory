#!/bin/bash
# One dashboard tile, view-only: a coloured header (label, live status, time since the screen last
# changed), the agent's current task (its window title), then the newest lines of its screen, dimmed.
# Usage: dashboard_tile.sh <session> <label> <256-colour number>
S=$1 LABEL=$2 COLOR=$3
last="" changed=0   # 0 = no change seen yet since this tile started
while :; do
  cols=$(tput cols) rows=$(tput lines) now=$(date +%s)
  raw=$(tmux capture-pane -p -t "$S" 2>/dev/null) || raw="(session $S is gone)"
  task=$(tmux display -p -t "$S" '#{pane_title}' 2>/dev/null)
  sum=$(printf '%s' "$raw" | cksum)
  [ "$sum" != "$last" ] && { [ -n "$last" ] && changed=$now; last=$sum; }
  text=$(printf '%s\n' "$raw" | grep -v '^[[:space:]]*$')
  recent=$(printf '%s\n' "$text" | tail -n 15)
  if grep -qE 'esc to interrupt|Working \(' <<<"$recent"; then st=WORKING; bg=28
  elif grep -qE '[0-9]+ question|Do you want|\[y/n\]|\(y/n\)' <<<"$recent"; then st=ASKING; bg=136
  elif (( changed > 0 && now - changed < 15 )); then st=ACTIVE; bg=30
  else st=IDLE; bg=240; fi
  tmux set-option -p -t "$TMUX_PANE" @status "$st" 2>/dev/null
  age=$(( now - changed ))
  if (( changed == 0 )); then ago="—"; elif (( age < 60 )); then ago="${age}s ago"; elif (( age < 3600 )); then ago="$((age/60))m ago"; else ago="$((age/3600))h$(( age%3600/60 ))m ago"; fi
  left=" ■ $LABEL " right=" $st · last change $ago "
  pad=$(( cols - ${#left} - ${#right} )); (( pad < 1 )) && pad=1
  {
    printf '\e[H'
    printf '\e[1;97;48;5;%sm%s%*s\e[0m\e[1;97;48;5;%sm%s\e[0m\e[K\n' "$COLOR" "$left" "$pad" "" "$bg" "$right"
    printf '\e[3;38;5;%sm ↳ %s\e[0m\e[K\n' "$COLOR" "${task:0:$(( cols - 4 ))}"
    printf '\e[38;5;%sm%s\e[0m\e[K\n' "$COLOR" "$(printf '%*s' "$cols" '' | tr ' ' '-')"
    printf '%s\n' "$text" | tail -n $(( rows - 4 )) | cut -c1-"$cols" | sed $'s/^/\e[38;5;250m/; s/$/\e[0m\e[K/'
    printf '\e[J'
  }
  sleep 2
done
