#!/bin/bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd -P)"
SOURCE=/Volumes/memit/llm-database-poc-mirror/autoresearch_sandbox_c10
DEST=/Volumes/memit/llm-database-poc-mirror/autoresearch_replay_c10_exp2
if [ "$#" -gt 1 ]; then
    echo "usage: setup_replay.sh [DEST]" >&2
    exit 2
fi
if [ "$#" -eq 1 ]; then DEST="$1"; fi
if [ -e "$DEST" ] || [ -L "$DEST" ]; then
    echo "REFUSED: DEST already exists: $DEST" >&2
    exit 2
fi
if [ ! -x "$SOURCE/.venv/bin/python" ]; then
    echo "REFUSED: sandbox runtime interpreter is missing: $SOURCE/.venv/bin/python" >&2
    exit 2
fi
git clone --no-local --no-checkout -- "$SOURCE" "$DEST"
git -C "$DEST" -c advice.detachedHead=false checkout --detach 92acd0378d23f4935df9a8bccc0137b36695a40f
export PYTHONDONTWRITEBYTECODE=1
"$SOURCE/.venv/bin/python" - "$SCRIPT_DIR" "$SOURCE" "$DEST" <<'PY'
from pathlib import Path
import sys

script_dir, source, dest = map(Path, sys.argv[1:])
sys.path.insert(0, str(script_dir))
from read_replay import BASE_COMMIT, expected_edit, git, inspect_replay

dest = dest.resolve()
runtime = (source / ".venv").resolve(strict=True)
(dest / ".venv").symlink_to(runtime, target_is_directory=True)
original = git(dest, "show", f"{BASE_COMMIT}:edit.py")
(dest / "edit.py").write_bytes(expected_edit(original).encode())
diff = git(dest, "diff", "--no-ext-diff", "--no-textconv", BASE_COMMIT, "--", "edit.py")
(dest / "replay_diff.txt").write_text(diff)
audit = inspect_replay(dest)
print(f"READY: {dest}")
print(f"base_commit: {BASE_COMMIT}")
print(f"runtime_link: {dest / '.venv'} -> {runtime}")
print(f"edit_py_sha256: {audit['edit_py_sha256']}")
print(f"diff_sha256: {audit['diff_sha256']}")
print("permitted_diff: PASS (zero weight and exact logging additions only)")
PY
