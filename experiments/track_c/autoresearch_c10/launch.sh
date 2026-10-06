#!/bin/bash
# Build or refresh the autoresearch sandbox from this directory's reviewed source, then start the agent there.
# Run it yourself, from any directory:   bash experiments/track_c/autoresearch_c10/launch.sh
# The agent session is interactive: answer its setup confirmation, then leave it running.
set -euo pipefail

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROGRAM="/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a"
REPO="/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory"
SB="/Volumes/memit/llm-database-poc-mirror/autoresearch_sandbox_c10"      # standalone repository, outside the program checkout
FENCE="/Volumes/memit/llm-database-poc-mirror/autoresearch_fence_c10"     # profile + wrappers; the agent cannot write here
OLD_SB="$REPO/.claude/worktrees/autoresearch-reaim-oct06"   # an earlier half-built attempt (a symlink and two copied files)
OLD_WT_SB="$REPO/.claude/worktrees/autoresearch-c10"        # the first launch's sandbox (a worktree; retired 2026-10-06)
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

# 2. retire the earlier sandboxes that were git worktrees of the program repository. A worktree shares the program's
#    object database, so from inside one `git show <program-branch>:<file>` reads any program file (found by the
#    cross-family reviewer, 2026-10-06). The sandbox is now a standalone repository outside the program checkout.
for old in "$OLD_SB" "$OLD_WT_SB"; do
  if [ -d "$old" ]; then "$GIT" -C "$REPO" worktree remove --force "$old"; fi
done
for b in autoresearch/reaim-oct06 autoresearch/master autoresearch/oct6; do
  "$GIT" -C "$REPO" branch -D "$b" 2>/dev/null || true   # the worktree-era branches; unborn ones may not exist as refs
done

# 3. the sandbox: its own repository on autoresearch/master, no shared history with the program
if [ ! -d "$SB/.git" ]; then
  mkdir -p "$SB"
  "$GIT" -C "$SB" init -q -b autoresearch/master
fi

# 4. the base commit: the reviewed source, copied in, only while the sandbox is on autoresearch/master
BRANCH="$("$GIT" -C "$SB" symbolic-ref --short HEAD)"
if [ "$BRANCH" = "autoresearch/master" ]; then
  for f in README.md prepare.py edit.py program.md pyproject.toml; do cp "$SRC/$f" "$SB/$f"; done
  rm -f "$SB/run.sh" "$SB/setup.sh" "$SB/kill_run.sh"   # the wrappers live in the fence directory now, not in the sandbox
  cp "$SRC/gitignore.sandbox" "$SB/.gitignore"
  # a copy, not a link: a link's target showed the agent where the program checkout lives, and on 2026-10-06 it
  # followed it and started summarizing the program's earlier experiments (the sandboxed-context ruling forbids that)
  rm -f "$SB/c10e_bandknob.py"
  cp "$PROGRAM/experiments/track_c/c10e_bandknob.py" "$SB/c10e_bandknob.py"
  chmod a-w "$SB/c10e_bandknob.py"
  ln -sfn "$PROGRAM/.venv" "$SB/.venv"
  "$GIT" -C "$SB" add -A
  if ! "$GIT" -C "$SB" diff --cached --quiet 2>/dev/null || ! "$GIT" -C "$SB" rev-parse --verify --quiet HEAD > /dev/null; then
    "$GIT" -C "$SB" commit -q -m "sandbox base from $("$GIT" -C "$PROGRAM" rev-parse --short HEAD):experiments/track_c/autoresearch_c10"
  fi
else
  echo "launch.sh: sandbox is on $BRANCH (a run in progress); source not re-copied"
fi

# 4b. on every launch, the sandbox's harness copy must be the harness the equivalence check passed on (also on resume)
"$PY" - "$EQ" "$SB/c10e_bandknob.py" <<'PYEOF' || die "the sandbox's c10e_bandknob.py differs from the harness in the equivalence result"
import hashlib, json, sys
eq, copy = sys.argv[1], sys.argv[2]
want = json.load(open(eq))["source_sha256"]["harness"]
sys.exit(0 if hashlib.sha256(open(copy, "rb").read()).hexdigest() == want else 1)
PYEOF

# 4c. the fence, rewritten on every launch (docs/AUTORESEARCH.md, "Context isolation"): Claude Code's Bash sandbox +
#     Read/Edit-tool denies for the agent, and a macOS Seatbelt profile for the model runs, which need the GPU. The
#     settings, the profile and the three wrappers live in $FENCE, which neither layer lets the agent write.
mkdir -p "$FENCE"
chmod -R u+w "$FENCE"
"$PY" "$SRC/sandbox_settings.py" "$PROGRAM" "$REPO" "$SB" "$FENCE" > "$FENCE/.sandbox_settings.json"
"$PY" "$SRC/sandbox_settings.py" "$PROGRAM" "$REPO" "$SB" "$FENCE" --seatbelt > "$FENCE/.sandbox.sb"
for f in run.sh setup.sh kill_run.sh; do cp "$SRC/$f" "$FENCE/$f"; chmod 555 "$FENCE/$f"; done
"$PY" "$SRC/write_reference_controls.py" "$PROGRAM/results/c10l_covgeom/run1_armB_identity.json" "$FENCE/reference_controls.json"
chmod 444 "$FENCE/reference_controls.json"
chmod 444 "$FENCE/.sandbox_settings.json" "$FENCE/.sandbox.sb"
chmod 555 "$FENCE"
# the sandbox must still carry the harness the equivalence check passed on (checked above) and the fence must be complete
for f in .sandbox_settings.json .sandbox.sb run.sh setup.sh kill_run.sh reference_controls.json; do [ -s "$FENCE/$f" ] || die "fence file missing: $FENCE/$f"; done

# 5. start the agent: no outside context (safe mode), Fable 5.1 at high effort (operator, 2026-10-06), permissions disabled as the
#    fork's README directs ("spin up your Claude ... in this repo (and disable all permissions)"), inside the fence
cd "$SB"
exec claude --safe-mode \
  --model claude-fable-5-1 --effort high \
  --dangerously-skip-permissions \
  --settings "$FENCE/.sandbox_settings.json" \
  "Hi have a look at program.md and let's kick off a new experiment! let's do the setup first."
