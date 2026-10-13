#!/usr/bin/env bash
# setup_notebooklm.sh — make the NotebookLM CLI (teng-lin/notebooklm-py) usable on this
# RunPod pod after a restart. Run:  ! bash tools/setup_notebooklm.sh
#
# WHY this exists: a pod restart wipes the ephemeral overlay (/root, /usr/local, ~/.local),
# which destroys the uv-installed `notebooklm` CLI *and* its auth dir (~/.notebooklm).
# Only /workspace (the MFS network volume) survives. This script rebuilds the ephemeral
# pieces and re-wires auth to the durable copy on /workspace.
#
# Does (idempotent):
#   1. Symlinks ~/.notebooklm -> /workspace/.notebooklm  (durable Google cookies; future
#      cookie ROTATIONS write straight to the persistent volume, so they never get lost).
#   2. Reinstalls the `notebooklm` CLI via uv into ephemeral ~/.local (fast local imports;
#      re-run on every boot is cheaper + more robust than a venv on the network FS).
#   3. Puts ~/.local/bin on PATH (this session + ~/.bashrc convenience).
#   4. Reports auth status and prints a ready-to-run test (or re-auth instructions).
# Does NOT do interactive `notebooklm login` (needs a browser/display the pod lacks) — auth
# comes from the durable storage_state.json the operator seeded from a laptop login.
set -euo pipefail

DURABLE_HOME=/workspace/.notebooklm          # persists across restarts (gitignored)
LOCAL_HOME="$HOME/.notebooklm"               # ephemeral default the CLI looks for
PROFILE_REL=profiles/default/storage_state.json
export PATH="$HOME/.local/bin:$PATH"

say() { printf '\n\033[1m%s\033[0m\n' "$*"; }

# ---- Step 1: wire auth to the durable volume (symlink the whole home dir) --------------
say "[1/4] Wiring auth -> durable volume ($DURABLE_HOME)"
mkdir -p "$DURABLE_HOME/profiles/default"
if [ -L "$LOCAL_HOME" ]; then
  echo "  ~/.notebooklm already a symlink -> $(readlink "$LOCAL_HOME")"
elif [ -e "$LOCAL_HOME" ]; then
  # A real dir exists (e.g. a fresh login this boot). Preserve the FRESHEST cookies, then
  # replace the dir with a symlink so rotations land on /workspace from here on.
  if [ -f "$LOCAL_HOME/$PROFILE_REL" ]; then
    if [ ! -f "$DURABLE_HOME/$PROFILE_REL" ] || \
       [ "$LOCAL_HOME/$PROFILE_REL" -nt "$DURABLE_HOME/$PROFILE_REL" ]; then
      echo "  local cookies are newer -> copying into durable home before symlinking"
      cp -p "$LOCAL_HOME/$PROFILE_REL" "$DURABLE_HOME/$PROFILE_REL"
    fi
  fi
  rm -rf "$LOCAL_HOME"
  ln -s "$DURABLE_HOME" "$LOCAL_HOME"
  echo "  replaced real ~/.notebooklm with symlink -> $DURABLE_HOME"
else
  ln -s "$DURABLE_HOME" "$LOCAL_HOME"
  echo "  created symlink ~/.notebooklm -> $DURABLE_HOME"
fi
[ -f "$DURABLE_HOME/$PROFILE_REL" ] && chmod 600 "$DURABLE_HOME/$PROFILE_REL" || true

# ---- Step 2: ensure uv is available ---------------------------------------------------
say "[2/4] Ensuring uv"
if command -v uv >/dev/null 2>&1; then
  echo "  uv present: $(command -v uv)  ($(uv --version 2>/dev/null || echo '?'))"
else
  echo "  uv missing -> pip install uv"
  pip install -q uv
  echo "  installed: $(uv --version 2>/dev/null || echo '?')"
fi

# ---- Step 3: install the CLI (skip if it already runs) --------------------------------
say "[3/4] Installing notebooklm CLI"
if command -v notebooklm >/dev/null 2>&1 && notebooklm --version >/dev/null 2>&1; then
  echo "  already installed: $(command -v notebooklm)  ($(notebooklm --version 2>/dev/null))"
else
  # Plain notebooklm-py (no [browser] extra): the pod only does headless token queries
  # (ask/list/summary via the cookie->token path); interactive `login`/Chromium is done on
  # the laptop, so Playwright is not needed here. Pin matches the operator's working setup.
  uv tool install --python /usr/bin/python3.11 "notebooklm-py==0.7.2"
  echo "  installed: $(notebooklm --version 2>/dev/null || echo 'version check FAILED')"
fi
# ~/.bashrc PATH convenience (ephemeral home — survives this session, not a restart)
grep -q '\.local/bin' "$HOME/.bashrc" 2>/dev/null \
  && echo "  ~/.bashrc PATH ~/.local/bin: present" \
  || { echo 'export PATH=$HOME/.local/bin:$PATH' >> "$HOME/.bashrc"; echo "  ~/.bashrc PATH ~/.local/bin: ADDED"; }

# ---- Step 4: auth status + next steps -------------------------------------------------
say "[4/4] Auth status"
if notebooklm auth check --test --json 2>/dev/null | grep -q '"status": *"ok"'; then
  echo "  auth check: OK (cookie->token fetch works) — NotebookLM is queryable headless."
  cat <<'EOF'

  ✅ READY. Test a live grounded query:

    export PATH="$HOME/.local/bin:$PATH"
    notebooklm list                 # confirm notebook titles
    notebooklm use f667f1f2         # LLM-as-Database spec v1.2   (or 23ba5f2d = Model-as-Graph)
    notebooklm ask "In one sentence, what is the core idea of this notebook?"
EOF
else
  cat <<EOF
  auth check: NOT ok — the durable cookies are missing or expired.

  Re-auth (cookies can't be minted on a headless pod):
    1) On your laptop: log in to NotebookLM in a browser, export storage_state.json
       (or run \`notebooklm login\` locally).
    2) Copy it to the DURABLE path (NOT into the git tree):
         $DURABLE_HOME/$PROFILE_REL
    3) Re-run this script.
EOF
fi

say "Durability note:"
echo "  • Cookies + rotations live on /workspace ($DURABLE_HOME) — survive pod restarts."
echo "  • The CLI binary + ~/.bashrc PATH live in ephemeral /root — re-run this script after"
echo "    a restart (it reinstalls in ~10s). 'pod restart' == 'new session' here, so the hook"
echo "    is: run this once at session start (see SESSION_BOOTSTRAP.md)."
