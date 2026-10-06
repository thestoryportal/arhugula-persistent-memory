#!/bin/bash
# Re-run the transcript audit every 2 minutes; print a line only when something new appears outside the sandbox, a
# helper agent is spawned, or the denial count changes. Run it under a Monitor from the program session.
HERE="$(cd "$(dirname "$0")" && pwd)"
PY=/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python
prev=""
while true; do
  out=$("$PY" "$HERE/audit_transcript.py" 2>&1)
  outside=$(printf '%s\n' "$out" | sed -n '/OUTSIDE the sandbox/,/^denials seen/p' | grep -v -E "OUTSIDE the sandbox|^denials seen|/opt/homebrew/bin/git" | grep -v '^\s*$')
  agents=$(printf '%s\n' "$out" | grep "Agent/Task calls:")
  den=$(printf '%s\n' "$out" | grep "denials seen in tool results:")
  calls=$(printf '%s\n' "$out" | grep "^tool calls:")
  cur="$outside|$agents|$den"
  if [ "$cur" != "$prev" ]; then
    echo "AUDIT: $calls | $agents | $den"
    if [ -n "$outside" ]; then echo "OUTSIDE PATHS: $outside"; fi
    prev="$cur"
  fi
  sleep 120
done
