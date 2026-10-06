#!/bin/bash
# Kill the run (or setup check) that run.sh / setup.sh recorded, and every descendant. From inside Claude Code's Bash
# sandbox the process list is not visible, so this wrapper is excluded from that sandbox. The PID file is in the
# agent-writable sandbox, so the process is checked before it is signalled: it must be a sandbox-exec'd python running
# edit.py or prepare.py from the sandbox.
SB=/Volumes/memit/llm-database-poc-mirror/autoresearch_sandbox_c10

descendants() {   # all descendants of $1, deepest first
  local kids; kids=$(pgrep -P "$1")
  for k in $kids; do descendants "$k"; done
  echo "$kids"
}

for f in "$SB/run.pid" "$SB/setup.pid"; do
  [ -f "$f" ] || continue
  pid=$(tr -dc '0-9' < "$f")
  cmd=$(/bin/ps -o command= -p "$pid" 2>/dev/null)
  case "$cmd" in
    *".venv/bin/python edit.py"*|*".venv/bin/python prepare.py"*|*"sandbox-exec -f"*)
      for d in $(descendants "$pid") "$pid"; do kill -TERM "$d" 2>/dev/null; done
      echo "sent TERM to $pid and its descendants (from $(basename "$f"))"
      sleep 3
      for d in $(descendants "$pid") "$pid"; do kill -KILL "$d" 2>/dev/null; done
      ;;
    "") echo "$(basename "$f") names pid $pid, which is not running" ;;
    *)  echo "$(basename "$f") names pid $pid, which is not a run of this sandbox ($cmd); not touched" ;;
  esac
  rm -f "$f"
done
echo "kill_run.sh: done"
