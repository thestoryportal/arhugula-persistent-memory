#!/bin/bash
# MAESTRO host acceptance. Every command saves output and its exit code here.
# Receipts: tests.exit, render_40.exit, render_100.exit, tmux_start.exit,
# tmux_capture.exit, gpu_check.exit, tmux_cleanup.exit, plus probe and sleeps.
# The real docs/program_state.json is read by the tab, never edited.
set -uo pipefail
HERE=$(cd "$(dirname "$0")" && pwd)
ROOT=$(cd "$HERE/../.." && pwd)
cd "$ROOT" || exit 1
export LLMDB_ROOT="$ROOT" PYTHONDONTWRITEBYTECODE=1
export PATH="/opt/homebrew/bin:$PATH"
owned=0
failed=0

record() {
  local name=$1
  shift
  "$@" >"$HERE/$name.txt" 2>&1
  local code=$?
  printf '%s\n' "$code" >"$HERE/$name.exit"
  return "$code"
}

cleanup() {
  if [ "$owned" = 1 ]; then
    tmux -L q1check kill-server >"$HERE/tmux_cleanup.txt" 2>&1
    local code=$?
    printf '%s\n' "$code" >"$HERE/tmux_cleanup.exit"
    if [ "$code" != 0 ]; then failed=1; fi
    owned=0
  fi
}
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

record tests /usr/bin/python3 -B tools/test_dashboard_queue.py || failed=1
record render_40 /usr/bin/python3 "$ROOT/tools/dashboard_queue.py" --once 40 || failed=1
record render_100 /usr/bin/python3 "$ROOT/tools/dashboard_queue.py" --once 100 || failed=1

# Refuse an existing q1check server; cleanup is authorized only after our start.
tmux -L q1check list-sessions >"$HERE/tmux_probe.txt" 2>&1
probe_code=$?
printf '%s\n' "$probe_code" >"$HERE/tmux_probe.exit"
if [ "$probe_code" = 0 ]; then
  printf '%s\n' 'q1check already has a server; refusing to touch it.' >"$HERE/host_summary.txt"
  exit 1
fi
if [ "$probe_code" != 1 ] || ! grep -Eq '^no server running on |^error connecting to .* \(No such file or directory\)$' "$HERE/tmux_probe.txt"; then
  printf '%s\n' 'q1check probe failed; see tmux_probe.txt. No server was changed.' >"$HERE/host_summary.txt"
  exit 1
fi

tmux -L q1check new-session -d -s q1check -x 100 -y 60 "/usr/bin/python3 '$ROOT/tools/dashboard_queue.py'" >"$HERE/tmux_start.txt" 2>&1
start_code=$?
printf '%s\n' "$start_code" >"$HERE/tmux_start.exit"
if [ "$start_code" != 0 ]; then
  printf '%s\n' 'Throwaway tab did not start; see tmux_start.txt.' >"$HERE/host_summary.txt"
  exit 1
fi
owned=1
record initial_wait sleep 2 || failed=1

# Run the exact read-only gate probe while the throwaway tab is alive.
record gpu_check /usr/bin/python3 -c "import sys; sys.path.insert(0,'tools'); import c10w_p2_gate as g; print(g.check_gpu())" || failed=1
record remaining_wait sleep 6 || failed=1
tmux -L q1check capture-pane -p -S -2000 -t '=q1check' >"$HERE/tmux_capture.txt" 2>&1
capture_code=$?
printf '%s\n' "$capture_code" >"$HERE/tmux_capture.exit"
if [ "$capture_code" != 0 ]; then failed=1; fi
tmux -L q1check list-panes -t '=q1check' -F '#{pane_dead} #{pane_pid} #{pane_start_command}' >"$HERE/tmux_panes.txt" 2>&1
panes_code=$?
printf '%s\n' "$panes_code" >"$HERE/tmux_panes.exit"
if [ "$panes_code" != 0 ]; then failed=1; fi

# Other work may legitimately block the gate. Check this tab's own PID separately.
record queue_exemption /usr/bin/python3 - "$HERE" <<'PY'
import ast
from pathlib import Path
import sys
receipts = Path(sys.argv[1])
gate = ast.literal_eval((receipts / 'gpu_check.txt').read_text())
panes = (receipts / 'tmux_panes.txt').read_text().splitlines()
if len(panes) != 1 or panes[0].split(None, 2)[0] != '0':
    raise SystemExit('Throwaway queue tab is not alive: ' + repr(panes))
pid = panes[0].split(None, 2)[1]
if not isinstance(gate, dict) or 'blocking_processes' not in gate:
    raise SystemExit('GPU inventory was unavailable: ' + repr(gate))
blockers = gate['blocking_processes']
if any(line.split(None, 1)[0] == pid or '/tools/dashboard_queue.py' in line for line in blockers):
    raise SystemExit('Queue tab blocked GPU admission: ' + repr(blockers))
print('PASS: live queue PID ' + pid + ' is absent from GPU blockers.')
print('Full gate outcome (other work may block): ' + repr(gate))
PY
if [ "$?" != 0 ]; then failed=1; fi
cleanup
printf 'Host checks exit %s; see individual .txt and .exit files.\n' "$failed" >"$HERE/host_summary.txt"
cat "$HERE/host_summary.txt"
exit "$failed"
