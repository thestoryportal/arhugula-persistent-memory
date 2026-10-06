#!/bin/bash
# Start the equivalence re-run in a detached tmux session (outlives tool timeouts), with the Claude env stripped.
exec env -u CLAUDECODE -u CLAUDE_CODE_ENTRYPOINT -u CLAUDE_CODE_SESSION_ID -u CLAUDE_JOB_DIR \
  tmux new-session -d -s equiv "bash /Users/robertrhu/.claude/jobs/4d71207f/tmp/run_equivalence.sh; sleep 3600"
