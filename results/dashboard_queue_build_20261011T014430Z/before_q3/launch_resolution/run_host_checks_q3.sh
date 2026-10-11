#!/bin/bash
# MAESTRO host acceptance. Q3 outputs are new, under host_attempt3/.
# Receipts: tests.exit, render_40.exit, render_100.exit, tmux_start.exit,
# tmux_capture.exit, gpu_check.exit, tmux_cleanup.exit, plus probe and sleeps.
# Q3: default_sessions.exit, experiment_inventory.exit, queue_live_checks.exit.
# Q3: visible_fit.exit and sized_render_fit.exit enforce pane and frame bounds.
# The real docs/program_state.json is read by the tab, never edited.
set -uo pipefail
RECEIPT=$(cd "$(dirname "$0")" && pwd)
ROOT=$(cd "$RECEIPT/../.." && pwd)
HERE="$RECEIPT/host_attempt3"
if ! mkdir "$HERE"; then
  printf '%s\n' 'Cannot create fresh host_attempt3; existing receipts will not be overwritten.' >&2
  exit 1
fi
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
    tmux -L q3check kill-server >"$HERE/tmux_cleanup.txt" 2>&1
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
record render_40 /usr/bin/python3 -B "$ROOT/tools/dashboard_queue.py" --once 40 30 || failed=1
record render_100 /usr/bin/python3 -B "$ROOT/tools/dashboard_queue.py" --once 100 45 || failed=1

# Refuse an existing q3check server; cleanup is authorized only after our start.
tmux -L q3check list-sessions >"$HERE/tmux_probe.txt" 2>&1
probe_code=$?
printf '%s\n' "$probe_code" >"$HERE/tmux_probe.exit"
if [ "$probe_code" = 0 ]; then
  printf '%s\n' 'q3check already has a server; refusing to touch it.' >"$HERE/host_summary.txt"
  exit 1
fi
if [ "$probe_code" != 1 ] || ! grep -Eq '^no server running on |^error connecting to .* \(No such file or directory\)$' "$HERE/tmux_probe.txt"; then
  printf '%s\n' 'q3check probe failed; see tmux_probe.txt. No server was changed.' >"$HERE/host_summary.txt"
  exit 1
fi

tmux -L q3check new-session -d -s q3check -x 40 -y 30 "/usr/bin/python3 -B '$ROOT/tools/dashboard_queue.py'" >"$HERE/tmux_start.txt" 2>&1
start_code=$?
printf '%s\n' "$start_code" >"$HERE/tmux_start.exit"
if [ "$start_code" != 0 ]; then
  printf '%s\n' 'Throwaway tab did not start; see tmux_start.txt.' >"$HERE/host_summary.txt"
  exit 1
fi
owned=1
record initial_wait sleep 2 || failed=1

# Run the exact read-only gate probe while the throwaway tab is alive.
record gpu_check /usr/bin/python3 -B -c "import sys; sys.path.insert(0,'tools'); import c10w_p2_gate as g; print(g.check_gpu())" || failed=1
record remaining_wait sleep 6 || failed=1
tmux -L q3check capture-pane -p -t '=q3check:' >"$HERE/tmux_capture.txt" 2>&1
capture_code=$?
printf '%s\n' "$capture_code" >"$HERE/tmux_capture.exit"
if [ "$capture_code" != 0 ]; then failed=1; fi
record visible_fit /usr/bin/python3 -B - "$HERE" <<'PYFIT'
from pathlib import Path
import sys
lines = (Path(sys.argv[1]) / 'tmux_capture.txt').read_text().splitlines()
first = next((line for line in lines if line.strip()), '')
if not first.startswith('Work queue') or len(lines) > 30:
    raise SystemExit('FAIL: visible pane lost header or exceeded 30 rows: %r, %d rows' % (first, len(lines)))
print('PASS: visible pane starts with Work queue and has %d rows.' % len(lines))
PYFIT
if [ "$?" != 0 ]; then failed=1; fi
record sized_render_fit /usr/bin/python3 -B - "$HERE" <<'PYFIT'
from pathlib import Path
import sys
here = Path(sys.argv[1])
for width, height in ((40, 30), (100, 45)):
    lines = (here / ('render_%d.txt' % width)).read_text().splitlines()
    if not lines or not lines[0].startswith('Work queue') or len(lines) > height or any(len(line) > width for line in lines):
        raise SystemExit('FAIL: --once %d %d exceeds frame bounds or lost header' % (width, height))
    print('PASS: --once %d %d fits (%d rows).' % (width, height, len(lines)))
PYFIT
if [ "$?" != 0 ]; then failed=1; fi
tmux -L q3check list-panes -t '=q3check' -F '#{pane_dead} #{pane_pid} #{pane_start_command}' >"$HERE/tmux_panes.txt" 2>&1
panes_code=$?
printf '%s\n' "$panes_code" >"$HERE/tmux_panes.exit"
if [ "$panes_code" != 0 ]; then failed=1; fi

# Inventory only: never start or change anything on the default server.
record default_sessions tmux -L default list-sessions -F '#{session_name}'
record experiment_inventory /bin/ps -axww -o pid=,ppid=,etime=,command= || failed=1
record queue_live_checks /usr/bin/python3 -B "$RECEIPT/check_q2_host_live.py" "$ROOT" "$HERE" || failed=1

# Other work may legitimately block the gate. Check this tab's own PID separately.
record queue_exemption /usr/bin/python3 -B - "$HERE" <<'PY'
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
