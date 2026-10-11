#!/bin/sh
# MAESTRO runs one action per invocation. No activation, remote rclone, PR, or push here.
set -eu
case "${1-}" in
  pins|pins-final|check|package|fixture|freeze|candidate|candidate-verify) ;;
  *) printf '%s\n' 'Usage: host_commands_r12.sh {pins|pins-final|check|package|fixture|freeze|candidate|candidate-verify}' >&2; exit 2 ;;
esac
task_worktree=/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a
task_receipt="$task_worktree/results/backup_gdrive_host_20261011/r12_package_20261011T024815Z"
cd "$task_worktree"
/usr/bin/env LLMDB_ROOT="$task_worktree" PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -B "$task_receipt/capture.py" "$task_receipt/operational_checks" "r12_host_preflight_$1" /usr/bin/python3 -B -c 'import json,os,sys; sys.path.insert(0,sys.argv[1]); from run_py39_coverage import validate_host; validate_host(sys.version_info[:3],os.getpriority(os.PRIO_PROCESS,0),os.environ); print(json.dumps({"interpreter":sys.executable,"version":sys.version,"niceness":os.getpriority(os.PRIO_PROCESS,0)}))' "$task_receipt"
case "$1" in
  pins|pins-final)
    exec /usr/bin/env LLMDB_ROOT="$task_worktree" /usr/bin/python3 -B "$task_receipt/capture.py" "$task_receipt/operational_checks" "r12_host_$1" /usr/bin/shasum -a 256 -c "$task_receipt/pins_v3.sha256"
    ;;
  check)
    exec /usr/bin/env LLMDB_ROOT="$task_worktree" /usr/bin/python3 -B "$task_receipt/capture.py" "$task_receipt" r12_host_plan_check /usr/bin/python3 -B "$task_receipt/check_plan.py" "$task_receipt/activation_plan_v3.md"
    ;;
  package)
    exec /usr/bin/env LLMDB_ROOT="$task_worktree" BACKUP_TEST_NO_RCLONE=1 /usr/bin/python3 -B "$task_receipt/capture.py" "$task_receipt" r12_host_package_driver /usr/bin/python3 -B "$task_receipt/run_sandbox.py" r12_host_package_green
    ;;
  fixture)
    # This uses real rclone only local→local, isolated HOME, APFS placement/config controls,
    # exact new date,time template, new verify_check, real inventory and owned-group checks.
    exec /usr/bin/env LLMDB_ROOT="$task_worktree" PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -B "$task_receipt/run_py39_coverage.py" r12_host_local_check --mode fixture
    ;;
  freeze)
    # Freeze after new host evidence; capture is outside candidate scope to avoid self-pinning.
    exec /usr/bin/env LLMDB_ROOT="$task_worktree" /usr/bin/python3 -B "$task_receipt/capture.py" "$task_receipt/operational_checks" r12_host_freeze /usr/bin/python3 -B "$task_receipt/freeze_receipt.py"
    ;;
  candidate)
    : "${MAESTRO_SOURCE_COMMIT:?set the full reviewed source SHA after committing this receipt}"
    : "${MAESTRO_CANDIDATE_PATH:?set a fresh isolated absolute candidate path}"
    exec /usr/bin/env LLMDB_ROOT="$task_worktree" /usr/bin/python3 -B "$task_receipt/capture.py" "$task_receipt/operational_checks" r12_host_candidate_create /bin/sh "$task_receipt/make_backup_candidate.sh" create "$task_worktree" "$MAESTRO_SOURCE_COMMIT" "$MAESTRO_CANDIDATE_PATH"
    ;;
  candidate-verify)
    : "${MAESTRO_SOURCE_COMMIT:?set the reviewed source SHA}"
    : "${MAESTRO_CANDIDATE_PATH:?set the existing isolated candidate path}"
    exec /usr/bin/env LLMDB_ROOT="$task_worktree" /usr/bin/python3 -B "$task_receipt/capture.py" "$task_receipt/operational_checks" r12_host_candidate_verify /bin/sh "$task_receipt/make_backup_candidate.sh" verify "$MAESTRO_CANDIDATE_PATH" "$MAESTRO_SOURCE_COMMIT"
    ;;
esac
