#!/bin/bash
# Kill the run (or setup check) that run.sh / setup.sh recorded, and its children. From inside Claude Code's Bash
# sandbox the process list is not visible, so this wrapper is excluded from that sandbox.
SB=/Volumes/memit/llm-database-poc-mirror/autoresearch_sandbox_c10
for f in "$SB/run.pid" "$SB/setup.pid"; do
  if [ -f "$f" ]; then
    pid=$(cat "$f")
    pkill -TERM -P "$pid" 2>/dev/null
    kill -TERM "$pid" 2>/dev/null && echo "sent TERM to $pid (from $(basename "$f"))"
    sleep 3
    pkill -KILL -P "$pid" 2>/dev/null
    kill -KILL "$pid" 2>/dev/null
    rm -f "$f"
  fi
done
echo "kill_run.sh: done"
