#!/usr/bin/env bash
# setup_codex.sh — install the Codex CLI on this RunPod pod for cross-family advisor-review.
# Created 2026-06-20. Run:  ! bash tools/setup_codex.sh
#
# Does (idempotent): installs the Codex binary to /workspace/bin (durable NV volume),
# confirms CODEX_HOME + skill/config are in place, reports auth status, prints next steps.
# Does NOT do OAuth login — that is interactive + uses YOUR ChatGPT account (see Step 3 below).
set -euo pipefail

export CODEX_HOME=/workspace/.codex
BIN_DIR=/workspace/bin
export PATH="$BIN_DIR:$PATH"
mkdir -p "$BIN_DIR" "$CODEX_HOME"

say() { printf '\n\033[1m%s\033[0m\n' "$*"; }

# ---- Step 1: install the binary (skip if already present) ----------------------------
if command -v codex >/dev/null 2>&1; then
  say "Codex already installed: $(command -v codex)  ($(codex --version 2>/dev/null || echo '?'))"
else
  say "[1/3] Installing Codex CLI (x86_64 linux musl) -> $BIN_DIR/codex"
  cd /tmp
  # IMPORTANT: anchor on the "/codex-x86_64-" filename so we don't grab the bundled
  # bwrap-* sandbox helper, or codex-exec-* / codex-responses-api-proxy-* side binaries.
  ASSETS=$(curl -fsSL https://api.github.com/repos/openai/codex/releases/latest \
        | grep -oE '"browser_download_url": *"[^"]*"' | sed 's/.*: *"//; s/"//' \
        | grep -E '/codex-x86_64-unknown-linux-musl' | grep -viE '\.sha256|\.sig|\.pem')
  # prefer .tar.gz, then .zst, then anything matching
  URL=$(printf '%s\n' "$ASSETS" | grep -E '\.tar\.gz$' | head -1)
  [ -n "$URL" ] || URL=$(printf '%s\n' "$ASSETS" | grep -E '\.zst$' | head -1)
  [ -n "$URL" ] || URL=$(printf '%s\n' "$ASSETS" | head -1)
  [ -n "$URL" ] || { echo "FATAL: no /codex-x86_64-unknown-linux-musl asset on the latest release." >&2; echo "candidates were:" >&2; printf '%s\n' "$ASSETS" >&2; exit 1; }
  echo "  asset: $URL"
  FN="cx_dl.${URL##*/}"
  curl -fsSL "$URL" -o "$FN"
  case "$FN" in
    *.tar.gz|*.tgz) tar xf "$FN" ;;
    *.tar.zst)      tar --use-compress-program=unzstd -xf "$FN" 2>/dev/null || { unzstd -f "$FN" && tar xf "${FN%.zst}"; } ;;
    *.zst)          unzstd -f "$FN" ;;
    *.zip)          unzip -o "$FN" ;;
    *)              echo "  (no known archive ext; treating as raw binary)"; cp "$FN" codex-x86_64-unknown-linux-musl ;;
  esac
  # find the extracted codex binary (name varies by release)
  CXBIN=$(find . -maxdepth 2 -type f \( -name 'codex' -o -name 'codex-x86_64-unknown-linux-musl' \) 2>/dev/null | head -1)
  [ -n "$CXBIN" ] || { echo "FATAL: extracted archive but found no 'codex' binary." >&2; ls -la; exit 1; }
  mv "$CXBIN" "$BIN_DIR/codex"
  chmod +x "$BIN_DIR/codex"
  say "Installed: $($BIN_DIR/codex --version 2>/dev/null || echo 'version check failed')"
fi

# ---- Step 2/4 verification (these were scaffolded already; confirm) -------------------
say "[2/3] Config checks"
grep -q 'CODEX_HOME=/workspace/.codex' ~/.bashrc 2>/dev/null \
  && echo "  ~/.bashrc CODEX_HOME export: present" \
  || { echo "# Codex home on durable NV volume" >> ~/.bashrc; echo 'export CODEX_HOME=/workspace/.codex' >> ~/.bashrc; echo "  ~/.bashrc CODEX_HOME export: ADDED"; }
grep -q 'PATH=/workspace/bin' ~/.bashrc 2>/dev/null \
  && echo "  ~/.bashrc PATH /workspace/bin: present" \
  || { echo 'export PATH=/workspace/bin:$PATH' >> ~/.bashrc; echo "  ~/.bashrc PATH /workspace/bin: ADDED"; }
[ -f "$CODEX_HOME/config.toml" ]                       && echo "  config.toml: present (model=$(grep -oE 'model = "[^"]+"' "$CODEX_HOME/config.toml" | head -1))" || echo "  config.toml: MISSING"
[ -f "$CODEX_HOME/skills/advisor-review/SKILL.md" ]   && echo "  advisor-review skill: present" || echo "  advisor-review skill: MISSING"

# ---- Step 3: auth status + next steps ------------------------------------------------
say "[3/3] Auth status"
if [ -f "$CODEX_HOME/auth.json" ]; then
  echo "  auth.json present at $CODEX_HOME/auth.json — Codex is logged in."
  cat <<'EOF'

  ✅ READY. Test cross-family review (closes the C2-band obligation):

    cd /workspace && CODEX_HOME=/workspace/.codex PATH=/workspace/bin:$PATH \
    codex exec -m gpt-5.5 "$(cat tools/advisor_review_prompt.md)

    FINDING (review the disposition): C2-band falsifier — mechanical PASS, NOT promoted
    (real-but-underpowered direction-specific redistribution). Cross-loc JS 67.68->86.41
    (+18.73pp); within-loc 95.48->77.77; retention 98->96; expr 100/100; held-out top-1
    7/12->10/12 (Fisher p~0.37). Disposition+de-confounders: CORPUS/21_C2BAND_FALSIFIER.md;
    raw results/c2band_compare_result.json. Is 'real redistribution, not under-editing'
    sound, and is 'not promoted' the right disposition?"
EOF
else
  cat <<'EOF'
  auth.json NOT found — you still need to log in (OAuth, your ChatGPT account).

  STEP 3 — OAuth login (recommended SSH port-forward path):
    1) From your laptop:   ssh -L 1455:localhost:1455 root@<pod-host>
    2) In the pod:         CODEX_HOME=/workspace/.codex PATH=/workspace/bin:$PATH codex login
    3) Open the printed URL in your laptop browser and sign in.
       -> auth.json writes to /workspace/.codex/ (durable across pod restarts).

  Alternative: run `codex login` on your laptop, then copy your local
    ~/.codex/auth.json  ->  /workspace/.codex/auth.json   (versions must match).

  Then re-run this script (or the Step-5 test above) to confirm.
EOF
fi

say "Note: ~/.bashrc lives in ephemeral /root — exports survive this session but not a pod restart."
say "      auth.json on /workspace IS durable. After a restart, re-run this script or prefix cmds with CODEX_HOME=/workspace/.codex."
