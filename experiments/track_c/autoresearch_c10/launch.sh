#!/bin/bash
# Build or refresh the autoresearch sandbox from this directory's reviewed source, then start the agent there.
# Run it yourself, from any directory:   bash experiments/track_c/autoresearch_c10/launch.sh
# The agent session is interactive: answer its setup confirmation, then leave it running.
set -euo pipefail

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROGRAM="/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a"
REPO="/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory"
SB="$REPO/.claude/worktrees/autoresearch-c10"
OLD_SB="$REPO/.claude/worktrees/autoresearch-reaim-oct06"   # an earlier half-built attempt (a symlink and two copied files)
GIT=/usr/bin/git
PY="$PROGRAM/.venv/bin/python"
export LLMDB_ROOT="$PROGRAM"
# the program repository's commit hooks guard the research branch, not the sandbox
export GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=core.hooksPath GIT_CONFIG_VALUE_0=/dev/null

die() { echo "launch.sh: $*" >&2; exit 1; }

# 1. one experiment at a time, and nothing else on the GPU
if pgrep -f "edit.py|run_iteration.py|c10e_bandknob" > /dev/null; then die "an experiment process is already running"; fi
if pgrep -f "ollama serve|llama-server" > /dev/null; then die "Ollama is running and would share the GPU: brew services stop ollama"; fi

# 1b. the equivalence check must have passed for exactly this prepare.py, edit.py and harness (docs/AUTORESEARCH.md)
EQ="$PROGRAM/results/autoresearch_c10_equivalence.json"
[ -f "$EQ" ] || die "no equivalence result: run  \$PY $SRC/check_equivalence.py  first"
"$PY" - "$EQ" "$SRC" "$PROGRAM/experiments/track_c/c10e_bandknob.py" <<'PYEOF' || die "equivalence check missing, failed, or stale for the current source: re-run check_equivalence.py"
import hashlib, json, sys
eq, src, harness = sys.argv[1], sys.argv[2], sys.argv[3]
d = json.load(open(eq))
want = {"prepare.py": f"{src}/prepare.py", "edit.py": f"{src}/edit.py", "harness": harness}
cur = {k: hashlib.sha256(open(p, "rb").read()).hexdigest() for k, p in want.items()}
sys.exit(0 if d.get("verdict") == "PASS" and d.get("source_sha256") == cur else 1)
PYEOF

# 2. retire the earlier half-built sandbox (its branch never had a commit)
if [ -d "$OLD_SB" ]; then
  "$GIT" -C "$REPO" worktree remove --force "$OLD_SB"
  "$GIT" -C "$REPO" branch -D autoresearch/reaim-oct06 2>/dev/null || true   # unborn branch: may not exist as a ref
fi

# 3. the sandbox worktree on autoresearch/master (orphan: it holds only the sandbox files)
if [ ! -d "$SB" ]; then
  if "$GIT" -C "$REPO" show-ref --verify --quiet refs/heads/autoresearch/master; then
    "$GIT" -C "$REPO" worktree add "$SB" autoresearch/master
  else
    "$GIT" -C "$REPO" worktree add --orphan -b autoresearch/master "$SB"
  fi
fi

# 4. the base commit: the reviewed source, copied in, only while the sandbox is on autoresearch/master
BRANCH="$("$GIT" -C "$SB" symbolic-ref --short HEAD)"
if [ "$BRANCH" = "autoresearch/master" ]; then
  for f in README.md prepare.py edit.py program.md pyproject.toml; do cp "$SRC/$f" "$SB/$f"; done
  cp "$SRC/gitignore.sandbox" "$SB/.gitignore"
  ln -sfn "$PROGRAM/experiments/track_c/c10e_bandknob.py" "$SB/c10e_bandknob.py"
  ln -sfn "$PROGRAM/.venv" "$SB/.venv"
  "$GIT" -C "$SB" add -A
  if ! "$GIT" -C "$SB" diff --cached --quiet 2>/dev/null || ! "$GIT" -C "$SB" rev-parse --verify --quiet HEAD > /dev/null; then
    "$GIT" -C "$SB" commit -q -m "sandbox base from $("$GIT" -C "$PROGRAM" rev-parse --short HEAD):experiments/track_c/autoresearch_c10"
  fi
else
  echo "launch.sh: sandbox is on $BRANCH (a run in progress); source not re-copied"
fi

# 5. start the agent: no outside context (safe mode), Opus 5.5 at extra-high effort, permissions disabled as the
#    fork's README directs ("spin up your Claude ... in this repo (and disable all permissions)")
cd "$SB"
exec claude --safe-mode \
  --model claude-opus-5-5 --effort xhigh \
  --dangerously-skip-permissions \
  "Hi have a look at program.md and let's kick off a new experiment! let's do the setup first."
