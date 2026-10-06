#!/bin/bash
# Emit each new agent line (⏺) from the tmux pane, plus run.log / HALT signals, until the session goes away.
seen="${TMPDIR:-/tmp}/autoresearch_pane_seen.txt"   # per-session scratch; any session can run this
touch "$seen"
SB=/Volumes/memit/llm-database-poc-mirror/autoresearch_sandbox_c10
while tmux has-session -t autoresearch 2>/dev/null; do
  tmux capture-pane -p -t autoresearch -S -200 2>/dev/null \
    | command sed 's/\x1b\[[0-9;]*m//g' \
    | command grep -E '^(⏺|❯)|Done! Ready|HALT|Traceback|confirm|Confirm|results\.tsv|heldout_full|guards:' \
    | while IFS= read -r line; do
        key=$(printf '%s' "$line" | command md5 -q)
        if ! command grep -q "$key" "$seen"; then
          echo "$key" >> "$seen"
          printf '%s\n' "$line"
        fi
      done
  if [ -f "$SB/HALT.md" ]; then echo "HALT.md present in sandbox"; fi
  sleep 15
done
echo "tmux session autoresearch is gone"
