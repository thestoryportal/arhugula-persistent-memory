#!/usr/bin/env bash
set -euo pipefail
LABVIZ_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
cd "$LABVIZ_ROOT"
export MPLCONFIGDIR="$LABVIZ_ROOT/projects/labviz-spec-v3/receipts/bulk/labviz/.matplotlib"
mkdir -p "$MPLCONFIGDIR"
.venv/bin/python -B code/apps/labviz/build.py
# 0.0.0.0 includes localhost, LAN, and the host's Tailscale address.
echo 'Lab View: http://127.0.0.1:8765 (also LAN / Tailscale address, port 8765)'
.venv/bin/python -B -m http.server 8765 --bind 0.0.0.0 --directory projects/labviz-spec-v3/receipts/bulk/labviz/site &
LABVIZ_SERVER_PID=$!
(
  while kill -0 "$LABVIZ_SERVER_PID"; do
    sleep 60
    if ! .venv/bin/python -B code/apps/labviz/build.py; then
      echo 'Lab View rebuild failed; stopping the server.' >&2
      kill "$LABVIZ_SERVER_PID"
      exit 1
    fi
  done
) &
LABVIZ_REBUILD_PID=$!
cleanup() {
  for LABVIZ_PID in "$LABVIZ_REBUILD_PID" "$LABVIZ_SERVER_PID"; do
    if kill -0 "$LABVIZ_PID"; then kill "$LABVIZ_PID"; fi
  done
}
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM
wait "$LABVIZ_SERVER_PID"
