#!/usr/bin/env bash
# install_infranodus_skills.sh — install the InfraNodus Claude skills (github.com/infranodus/skills)
# into ~/.claude/skills so Claude Code activates them globally. Run:  ! bash tools/install_infranodus_skills.sh
#
# Source of truth = the durable master on /workspace (survives pod restarts; gitignored).
# ~/.claude/skills is on the ephemeral overlay, so this must be re-run after a pod restart
# (it's wired into restore_pod_tools.sh). Each skill folder is copied to ~/.claude/skills/<name>/
# where <name> is the SKILL.md frontmatter name. Idempotent (overwrites). Skills register on the
# next SESSION RELOAD — Claude Code enumerates skills at startup.
set -euo pipefail

SRC="${INFRANODUS_SKILLS_SRC:-/workspace/tools/infranodus-skills}"
DEST="$HOME/.claude/skills"
say() { printf '\n\033[1m%s\033[0m\n' "$*"; }

[ -d "$SRC" ] || { echo "FATAL: skills master not found at $SRC (clone github.com/infranodus/skills there first)."; exit 1; }
mkdir -p "$DEST"

say "Installing InfraNodus skills:  $SRC  ->  $DEST"
n=0
# every directory that contains a SKILL.md is a skill
while IFS= read -r skillmd; do
  d="$(dirname "$skillmd")"
  # parse the frontmatter `name:` (first --- block); fall back to the folder name
  name="$(python3 - "$skillmd" <<'PY'
import sys,re
t=open(sys.argv[1],encoding="utf-8").read()
m=re.search(r'^---\s*\n(.*?)\n---\s*\n', t, re.S)
name=""
if m:
    fm=m.group(1)
    nm=re.search(r'^\s*name:\s*(.+?)\s*$', fm, re.M)
    if nm: name=nm.group(1).strip().strip('\'"')
print(name)
PY
)"
  [ -n "$name" ] || name="$(basename "$d")"
  rm -rf "$DEST/$name"
  cp -a "$d" "$DEST/$name"
  find "$DEST/$name" -name '.DS_Store' -delete 2>/dev/null || true
  printf '  ✅ %-26s (from %s)\n' "$name" "$(basename "$d")"
  n=$((n+1))
done < <(find "$SRC" -name SKILL.md | sort)

say "Installed $n skills to $DEST"
echo "Skill names now available (after a session reload):"
ls -1 "$DEST" | sed 's/^/  /'
cat <<'EOF'

⚠ Claude Code enumerates skills at STARTUP — reload the session for these to appear in the
  skill list / be invocable. Verify with:  /skill   (or just ask to use one, e.g. "use the
  shifting-perspective skill"). Several skills call InfraNodus MCP tools — keep that server live.
EOF
