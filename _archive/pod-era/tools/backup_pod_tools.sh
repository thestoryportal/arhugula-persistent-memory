#!/usr/bin/env bash
# backup_pod_tools.sh — snapshot the ephemeral pieces of the 3 research tools into a
# durable bundle on /workspace, so a pod restart can restore them by copy (no rebuild).
# Run:  ! bash tools/backup_pod_tools.sh        (re-run after key/version changes)
#
# Captures into /workspace/.pod_restore/ (gitignored — holds live API keys):
#   • mcp/servers.json        — the InfraNodus (global) + Perplexity (project /root) MCP
#                               config blocks WITH their API keys, tagged with their scope.
#   • notebooklm/*.tar.gz      — the 20M uv venv for the `notebooklm` CLI (restore by copy).
#   • npx/npx-cache.tar.gz     — ~/.npm/_npx (the MCP server packages) to cut re-download.
# NotebookLM Google cookies already live durable at /workspace/.notebooklm — not re-copied
# here (the restore script just re-points the ~/.notebooklm symlink at them).
set -euo pipefail

BUNDLE=/workspace/.pod_restore
CLAUDE_JSON="${CLAUDE_JSON:-/root/.claude.json}"
NB_TOOL=/root/.local/share/uv/tools/notebooklm-py
NPX_CACHE=/root/.npm/_npx
say() { printf '\n\033[1m%s\033[0m\n' "$*"; }

mkdir -p "$BUNDLE/mcp" "$BUNDLE/notebooklm" "$BUNDLE/npx"

# ---- 1: MCP server config blocks (with keys + scope) ----------------------------------
say "[1/4] MCP server configs -> $BUNDLE/mcp/servers.json"
python3 - "$CLAUDE_JSON" "$BUNDLE/mcp/servers.json" <<'PY'
import json,sys,os
src,dst=sys.argv[1],sys.argv[2]
d=json.load(open(src))
out={"global":{}, "projects":{}}
# global-scope servers we manage
for name in ("infranodus",):
    s=d.get("mcpServers",{}).get(name)
    if s: out["global"][name]=s
# project-scope servers we manage
for proj,cfg in d.get("projects",{}).items():
    for name in ("perplexity",):
        s=cfg.get("mcpServers",{}).get(name)
        if s: out.setdefault("projects",{}).setdefault(proj,{})[name]=s
tmp=dst+".tmp"
json.dump(out,open(tmp,"w"),indent=2)
json.load(open(tmp))            # validate it re-parses
os.replace(tmp,dst)
g=list(out["global"]); p={k:list(v) for k,v in out["projects"].items()}
print(f"  captured global={g}  projects={p}")
PY
chmod 600 "$BUNDLE/mcp/servers.json" 2>/dev/null || true

# ---- 2: NotebookLM venv (restore-by-copy) ---------------------------------------------
say "[2/4] NotebookLM uv venv -> $BUNDLE/notebooklm/notebooklm-py-tool.tar.gz"
if [ -d "$NB_TOOL" ]; then
  tar -C "$(dirname "$NB_TOOL")" -czf "$BUNDLE/notebooklm/notebooklm-py-tool.tar.gz" "$(basename "$NB_TOOL")"
  echo "  $(du -h "$BUNDLE/notebooklm/notebooklm-py-tool.tar.gz" | cut -f1) archived"
else
  echo "  (notebooklm venv not present — skipped; restore will uv-reinstall instead)"
fi

# ---- 3: npx package cache (MCP servers) -----------------------------------------------
say "[3/4] npx cache -> $BUNDLE/npx/npx-cache.tar.gz"
if [ -d "$NPX_CACHE" ]; then
  tar -C "$(dirname "$NPX_CACHE")" -czf "$BUNDLE/npx/npx-cache.tar.gz" "$(basename "$NPX_CACHE")"
  echo "  $(du -h "$BUNDLE/npx/npx-cache.tar.gz" | cut -f1) archived (speeds up MCP launch; not a guaranteed-offline path)"
else
  echo "  (no npx cache yet — skipped; npx will fetch on first MCP launch)"
fi

# ---- 4: manifest ----------------------------------------------------------------------
say "[4/4] Manifest"
{
  echo "# pod_restore bundle — captured $(date -u '+%Y-%m-%d %H:%M:%SZ')"
  echo "Restore with:  bash /workspace/tools/restore_pod_tools.sh"
  echo
  echo "Contents:"
  echo "  mcp/servers.json   InfraNodus(global) + Perplexity(project /root) configs + API keys"
  echo "  notebooklm/*.tar.gz  uv venv for the notebooklm CLI"
  echo "  npx/npx-cache.tar.gz ~/.npm/_npx (MCP server node packages)"
  echo
  echo "NotebookLM cookies are NOT here — they live durable at /workspace/.notebooklm."
  echo "Perplexity is project-scoped to cwd /root; restore re-creates that exact scope."
} > "$BUNDLE/MANIFEST.md"
cat "$BUNDLE/MANIFEST.md"
say "Done. Bundle: $BUNDLE  ($(du -sh "$BUNDLE" | cut -f1)).  Gitignored (holds live keys)."
