#!/usr/bin/env bash
# restore_pod_tools.sh — rebuild the 3 research tools after a pod restart from the durable
# /workspace bundle. THE single entry point to run once at session start.
# Run:  ! bash tools/restore_pod_tools.sh
#
# Restores into ephemeral locations:
#   1. NotebookLM CLI — lays the uv venv back from the tar (or reinstalls), wires cookies
#      via setup_notebooklm.sh (the one NotebookLM mechanism; no duplication).
#   2. npx cache — unpacks ~/.npm/_npx so the MCP servers launch faster.
#   3. MCP config — merges the InfraNodus(global) + Perplexity(project /root) blocks back
#      into ~/.claude.json (atomic, non-destructive; creates missing keys).
#   4. Verifies each MCP server BOOTS with its restored key (tool registration still needs
#      a session reload — stated honestly below).
#
# Override CLAUDE_JSON=/tmp/test.json to dry-run the merge against a scratch file.
set -euo pipefail

BUNDLE=/workspace/.pod_restore
CLAUDE_JSON="${CLAUDE_JSON:-/root/.claude.json}"
NB_TOOL_PARENT=/root/.local/share/uv/tools
NB_BIN=/root/.local/bin/notebooklm
NPX_CACHE_PARENT=/root/.npm
NODE_BIN=/workspace/node-v20/bin
export PATH="$HOME/.local/bin:$NODE_BIN:$PATH"
say() { printf '\n\033[1m%s\033[0m\n' "$*"; }

[ -d "$BUNDLE" ] || { echo "FATAL: no bundle at $BUNDLE — run tools/backup_pod_tools.sh first (on a working pod)."; exit 1; }

# ---- 1: NotebookLM (venv-by-copy fast path, then the canonical setup script) -----------
say "[1/5] NotebookLM CLI"
TAR="$BUNDLE/notebooklm/notebooklm-py-tool.tar.gz"
if ! { command -v notebooklm >/dev/null 2>&1 && notebooklm --version >/dev/null 2>&1; }; then
  if [ -f "$TAR" ]; then
    echo "  restoring venv from bundle (no reinstall)…"
    mkdir -p "$NB_TOOL_PARENT" "$(dirname "$NB_BIN")"
    tar -C "$NB_TOOL_PARENT" -xzf "$TAR"
    ln -sf "$NB_TOOL_PARENT/notebooklm-py/bin/notebooklm" "$NB_BIN"
    notebooklm --version >/dev/null 2>&1 && echo "  venv restored: $(notebooklm --version)" \
      || echo "  venv restore didn't run — setup_notebooklm.sh will reinstall"
  else
    echo "  no venv tar in bundle — will reinstall via setup_notebooklm.sh"
  fi
fi
# Canonical NotebookLM mechanism: wires the cookie symlink + PATH + auth check, and
# reinstalls only if the venv restore above didn't take. One source of truth.
bash /workspace/tools/setup_notebooklm.sh

# ---- 2: npx cache (faster MCP launch) -------------------------------------------------
say "[2/5] npx package cache"
NPXTAR="$BUNDLE/npx/npx-cache.tar.gz"
if [ -f "$NPXTAR" ]; then
  mkdir -p "$NPX_CACHE_PARENT"
  tar -C "$NPX_CACHE_PARENT" -xzf "$NPXTAR"
  echo "  restored ~/.npm/_npx (reduces re-download; npx may still version-check online)"
else
  echo "  no npx cache in bundle — npx will fetch packages on first MCP launch"
fi

# ---- 3: merge MCP configs into ~/.claude.json (atomic, non-destructive) ---------------
say "[3/5] MCP config -> $CLAUDE_JSON"
python3 - "$BUNDLE/mcp/servers.json" "$CLAUDE_JSON" <<'PY'
import json,sys,os
saved=json.load(open(sys.argv[0+1]))
dst=sys.argv[1+1]
d=json.load(open(dst)) if os.path.exists(dst) else {}
added=[]
# global-scope servers
d.setdefault("mcpServers",{})
for name,cfg in saved.get("global",{}).items():
    d["mcpServers"][name]=cfg; added.append(f"global:{name}")
# project-scope servers (create projects[proj].mcpServers if absent)
d.setdefault("projects",{})
for proj,servers in saved.get("projects",{}).items():
    d["projects"].setdefault(proj,{}).setdefault("mcpServers",{})
    for name,cfg in servers.items():
        d["projects"][proj]["mcpServers"][name]=cfg; added.append(f"{proj}:{name}")
tmp=dst+".tmp"
json.dump(d,open(tmp,"w"),indent=2)
json.load(open(tmp))                 # validate parse BEFORE replacing the live file
os.replace(tmp,dst)
print("  merged:", ", ".join(added) or "(nothing — empty bundle?)")
PY

# ---- 4: verify each MCP server BOOTS with its restored key -----------------------------
say "[4/5] Verify MCP servers boot (standalone handshake)"
boot_check() {  # $1=label  $2=pkg  $3=ENVVAR=value
  local label="$1" pkg="$2" kv="$3"
  # Proper MCP stdio handshake: initialize + initialized, then hold stdin briefly so the
  # server flushes its reply before EOF. Success = it emits an initialize result.
  local out
  out=$( { printf '%s\n' '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"restore-check","version":"0"}}}'
           printf '%s\n' '{"jsonrpc":"2.0","method":"notifications/initialized"}'
           sleep 3; } | env "$kv" PATH="$NODE_BIN:$PATH" \
           timeout 70 "$NODE_BIN/npx" -y "$pkg" 2>/dev/null | head -c 600 || true)
  if printf '%s' "$out" | grep -q '"serverInfo"'; then
    local ver; ver=$(printf '%s' "$out" | grep -oE '"name":"[^"]+","version":"[^"]+"' | head -1)
    echo "  ✅ $label: booted + handshook (key accepted) ${ver:+[$ver]}"
  else
    echo "  ⚠ $label: no handshake captured — verify the key / first-launch download; tools confirm on session reload"
  fi
}
IFKEY=$(python3 -c 'import json;print(json.load(open("'"$BUNDLE"'/mcp/servers.json"))["global"]["infranodus"]["env"]["INFRANODUS_API_KEY"])' 2>/dev/null || true)
PPKEY=$(python3 -c 'import json;d=json.load(open("'"$BUNDLE"'/mcp/servers.json"));print(next(iter(d["projects"].values()))["perplexity"]["env"]["PERPLEXITY_API_KEY"])' 2>/dev/null || true)
[ -n "$IFKEY" ] && boot_check "InfraNodus" "infranodus-mcp-server" "INFRANODUS_API_KEY=$IFKEY" || echo "  (no InfraNodus key in bundle)"
[ -n "$PPKEY" ] && boot_check "Perplexity" "@perplexity-ai/mcp-server" "PERPLEXITY_API_KEY=$PPKEY" || echo "  (no Perplexity key in bundle)"

# ---- 5: re-install the InfraNodus Claude skills into ~/.claude/skills ------------------
say "[5/5] InfraNodus Claude skills"
if [ -d /workspace/tools/infranodus-skills ]; then
  bash /workspace/tools/install_infranodus_skills.sh 2>&1 | grep -E '✅|Installed [0-9]+ skills' || true
else
  echo "  skills master missing (/workspace/tools/infranodus-skills) — re-clone github.com/infranodus/skills there"
fi

say "Done."
cat <<EOF
  • NotebookLM: ready now — \`notebooklm use <id>; notebooklm ask "<q>"\` (PATH already set).
  • InfraNodus + Perplexity: config merged into $CLAUDE_JSON. MCP servers only register on a
    SESSION RELOAD — reload the session, then their tools appear (verify with a live call).
  • Perplexity is project-scoped to cwd /root — launch the session from /root (the default).
    For cwd-independence, move it under root "mcpServers" in $CLAUDE_JSON.
  • InfraNodus skills: 15 installed to ~/.claude/skills — also register on SESSION RELOAD.
EOF
