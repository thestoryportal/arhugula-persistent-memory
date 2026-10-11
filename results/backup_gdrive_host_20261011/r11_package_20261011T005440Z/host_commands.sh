#!/bin/sh
# One host evidence command per invocation. This never executes the activation plan.
set -eu
case "${1-}" in
  e-red|e-green|coverage|fixture|frozen|package|check-red|check-green|pins) ;;
  *) printf '%s\n' 'Usage: host_commands.sh {e-red|e-green|coverage|fixture|frozen|package|check-red|check-green|pins}' >&2; exit 2 ;;
esac
task_worktree=/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a
task_receipt="$task_worktree/results/backup_gdrive_host_20261011/r11_package_20261011T005440Z"
cd "$task_worktree"
/usr/bin/env LLMDB_ROOT="$task_worktree" PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -B "$task_receipt/capture.py" "$task_receipt" "r11_hostfix1_preflight_$1" /usr/bin/python3 -B -c 'import json,os,sys; sys.path.insert(0,sys.argv[1]); from run_py39_coverage import validate_host; validate_host(sys.version_info[:3],os.getpriority(os.PRIO_PROCESS,0),os.environ); print(json.dumps({"version":sys.version,"interpreter":sys.executable,"niceness":os.getpriority(os.PRIO_PROCESS,0)}))' "$task_receipt"
case "$1" in
  e-red) task_label=r11_hostfix1_e_red; task_mode=e-red ;;
  e-green) task_label=r11_hostfix1_e_green; task_mode=e-green ;;
  coverage) task_label=r11_hostfix1_py39_coverage; task_mode=coverage ;;
  fixture) task_label=r11_hostfix1_local_check; task_mode=fixture ;;
  frozen) task_label=r11_hostfix1_green; task_mode=frozen ;;
  package) task_label=r11_hostfix1_package_green; task_mode=package ;;
  check-red) task_label=r11_hostfix1_check_v1_red; task_mode=check-red ;;
  check-green) task_label=r11_hostfix1_check_v2_green; task_mode=check-green ;;
  pins)
    exec /usr/bin/env LLMDB_ROOT="$task_worktree" PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -B "$task_receipt/capture.py" "$task_receipt" r11_hostfix1_pins /usr/bin/shasum -a 256 -c "$task_receipt/pins_v2.sha256"
    ;;
esac
exec /usr/bin/env LLMDB_ROOT="$task_worktree" PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -B "$task_receipt/run_py39_coverage.py" "$task_label" --mode "$task_mode"
