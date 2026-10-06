#!/bin/bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd -P)"
PROGRAM_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd -P)"
SOURCE=/Volumes/memit/llm-database-poc-mirror/autoresearch_sandbox_c10
DEST=/Volumes/memit/llm-database-poc-mirror/autoresearch_replay_c10_exp2loc
if [ "$#" -gt 1 ]; then echo "usage: setup_replay.sh [DEST]" >&2; exit 2; fi
if [ "$#" -eq 1 ]; then DEST="$1"; fi
if [ -e "$DEST" ] || [ -L "$DEST" ]; then
    echo "REFUSED: DEST already exists: $DEST" >&2
    exit 2
fi
if [ ! -x "$PROGRAM_ROOT/.venv/bin/python" ] || [ ! -x "$SOURCE/.venv/bin/python" ]; then
    echo "REFUSED: pinned runtime interpreter missing" >&2
    exit 2
fi
git clone --no-local --no-checkout -- "$SOURCE" "$DEST"
git -C "$DEST" -c advice.detachedHead=false checkout --detach 92acd0378d23f4935df9a8bccc0137b36695a40f
export PYTHONDONTWRITEBYTECODE=1
"$PROGRAM_ROOT/.venv/bin/python" -B - "$SCRIPT_DIR" "$SOURCE" "$DEST" <<'PY'
import json
from pathlib import Path
import sys
sys.path.insert(0, sys.argv[1])
from read_replay import BASE_COMMIT, PROGRAM_ROOT, expected_edit, git, inspect_replay, require
try:
    source, dest = map(lambda p: Path(p).resolve(strict=True), sys.argv[2:])
    runtime = (source / ".venv").resolve(strict=True)
    require(runtime == (PROGRAM_ROOT / ".venv").resolve(strict=True), "sandbox runtime differs from pinned program runtime")
    (dest / ".venv").symlink_to(runtime, target_is_directory=True)
    original = git(dest, "show", f"{BASE_COMMIT}:edit.py")
    (dest / "edit.py").write_bytes(expected_edit(original).encode())
    audit = inspect_replay(dest)
    (dest / "replay_diff.txt").write_text(audit["diff"])
    (dest / "replay_diff.sha256").write_text(audit["diff_sha256"] + "  replay_diff.txt\n")
    (dest / "replay_setup.json").write_text(json.dumps(audit, indent=2) + "\n")
except (OSError, ValueError, KeyError) as exc:
    print(f"INVALID/HALT: setup refused: {exc}", file=sys.stderr)
    sys.exit(2)
print(f"READY: {dest}")
print(f"base_commit: {BASE_COMMIT}")
print(f"runtime_link: {dest / '.venv'} -> {runtime}")
print(f"edit_py_sha256: {audit['edit_py_sha256']}")
print(f"diff_sha256: {audit['diff_sha256']}")
print("permitted_diff: PASS (weight 1; common-position gather and inert audit additions only)")
print(audit["diff"], end="")
PY
