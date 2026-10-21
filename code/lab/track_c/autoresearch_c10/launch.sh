#!/bin/bash
# Program-side only. Install with v13_build.py first; all launch gates fail closed.
set -euo pipefail
[ "$#" -eq 0 ] || { echo "launch.sh takes no arguments" >&2; exit 1; }
PROGRAM="/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a"
FENCE="/Volumes/memit/llmdb-preserved/icm21-20261013/parent/autoresearch_fence_v13_c10"
ANCHOR="$(/usr/bin/shasum -a 256 "$FENCE/sealed/manifest.json")"
exec /usr/bin/env -i HOME="$HOME" USER="$USER" PATH=/usr/bin:/bin:/usr/sbin:/sbin \
  PYTHONDONTWRITEBYTECODE=1 "$PROGRAM/.venv/bin/python" -I -B \
  "$FENCE/v13_launcher.py" "$FENCE" "${ANCHOR%% *}"
