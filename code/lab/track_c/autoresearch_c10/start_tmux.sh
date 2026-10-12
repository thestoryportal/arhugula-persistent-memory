#!/bin/bash
# Start the autoresearch loop in a detached tmux session, with this program session's
# Claude Code environment stripped so the loop's own Claude Code does not refuse to start nested.
set -euo pipefail
LAUNCH=/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/autoresearch_c10/launch.sh
exec env -u CLAUDECODE -u CLAUDE_CODE_AGENT -u CLAUDE_CODE_BRIDGE_SESSION_ID -u CLAUDE_CODE_CHILD_SESSION \
  -u CLAUDE_CODE_ENTRYPOINT -u CLAUDE_CODE_EXECPATH -u CLAUDE_CODE_MAX_OUTPUT_TOKENS -u CLAUDE_CODE_MESSAGING_SOCKET \
  -u CLAUDE_CODE_MESSAGING_TOKEN -u CLAUDE_CODE_SESSION_ATTENDED -u CLAUDE_CODE_SESSION_ID -u CLAUDE_EFFORT \
  -u CLAUDE_JOB_DIR -u CLAUDE_PID -u AI_AGENT \
  tmux new-session -d -s autoresearch -x 200 -y 50 "bash $LAUNCH; echo; echo '[launch.sh exited with status '\$?']'; sleep 86400"
