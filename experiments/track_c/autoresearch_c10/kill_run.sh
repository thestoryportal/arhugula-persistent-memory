#!/bin/bash
# Kill the run (or setup check) that run.sh / setup.sh recorded, and every descendant. From inside Claude Code's Bash
# sandbox the process list is not visible, so this wrapper is excluded from that sandbox. The PID file is in the
# agent-writable sandbox, so the process is verified before it is signalled: its command line must be exactly what
# run.sh / setup.sh start (sandbox-exec with THIS fence's profile, the sandbox's .venv python, edit.py or prepare.py)
# and its working directory must be the sandbox.
FENCE="$(cd "$(dirname "$0")" && pwd)"
SB=/Volumes/memit/llm-database-poc-mirror/autoresearch_sandbox_c10
EXPECT_RUN="/usr/bin/sandbox-exec -f $FENCE/.sandbox.sb .venv/bin/python edit.py"
EXPECT_SETUP="/usr/bin/sandbox-exec -f $FENCE/.sandbox.sb .venv/bin/python prepare.py"

descendants() {   # all descendants of $1, deepest first
  local kids; kids=$(pgrep -P "$1")
  for k in $kids; do descendants "$k"; done
  echo "$kids"
}

for f in "$SB/run.pid" "$SB/setup.pid"; do
  [ -f "$f" ] || continue
  pid=$(tr -dc '0-9' < "$f")
  cmd=$(/bin/ps -o command= -p "$pid" 2>/dev/null)
  cwd=$(/usr/sbin/lsof -a -p "$pid" -d cwd -Fn 2>/dev/null | command sed -n 's/^n//p' | head -1)
  if [ -z "$cmd" ]; then
    echo "$(basename "$f") names pid $pid, which is not running"
  elif { [ "$cmd" = "$EXPECT_RUN" ] || [ "$cmd" = "$EXPECT_SETUP" ] || [ "$cmd" = ".venv/bin/python edit.py" ] || [ "$cmd" = ".venv/bin/python prepare.py" ]; } && [ "$cwd" = "$SB" ]; then
    for d in $(descendants "$pid") "$pid"; do kill -TERM "$d" 2>/dev/null; done
    echo "sent TERM to $pid and its descendants (from $(basename "$f"))"
    sleep 3
    for d in $(descendants "$pid") "$pid"; do kill -KILL "$d" 2>/dev/null; done
  else
    echo "$(basename "$f") names pid $pid, which is not a run of this sandbox (cmd: $cmd; cwd: $cwd); not touched"
  fi
  rm -f "$f"
done
echo "kill_run.sh: done"
