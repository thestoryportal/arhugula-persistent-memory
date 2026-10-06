#!/bin/bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd -P)"
DEST=/Volumes/memit/llm-database-poc-mirror/autoresearch_replay_c10_exp2
if [ "$#" -gt 1 ]; then
    echo "usage: run_replay.sh [DEST]" >&2
    exit 2
fi
if [ "$#" -eq 1 ]; then DEST="$1"; fi
cd "$DEST"
DEST="$(pwd -P)"
if busy="$(pgrep -fl 'edit.py|prepare.py|safe-mode|ollama')"; then
    echo "REFUSED: GPU-owner process matches:" >&2
    echo "$busy" >&2
    exit 70
else
    rc=$?
    if [ "$rc" -ne 1 ]; then
        echo "REFUSED: pgrep failed with exit $rc" >&2
        exit "$rc"
    fi
fi
export PYTHONDONTWRITEBYTECODE=1
.venv/bin/python - "$SCRIPT_DIR" "$DEST" <<'PY'
import json
from pathlib import Path
import sys

sys.path.insert(0, sys.argv[1])
from read_replay import inspect_replay

dest = Path(sys.argv[2])
audit = inspect_replay(dest)
(dest / "replay_diff.txt").write_text(audit["diff"])
(dest / "replay_launch.json").write_text(json.dumps(audit, indent=2) + "\n")
print("prelaunch_diff: PASS")
print(f"prelaunch_edit_py_sha256: {audit['edit_py_sha256']}")
PY
if .venv/bin/python -c 'import torch; assert torch.backends.mps.is_available(), "MPS unavailable"' > preflight.log 2>&1; then
    echo "MPS availability: PASS"
else
    echo "INFRASTRUCTURE HALT: MPS unavailable; see $DEST/preflight.log" >&2
    cat preflight.log >&2
    exit 70
fi
.venv/bin/python edit.py > run.log 2>&1 &
pid=$!
echo "$pid" > run.pid
if wait "$pid"; then rc=0; else rc=$?; fi
rm -f run.pid
exit "$rc"
