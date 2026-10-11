#!/bin/sh
# MAESTRO runs one action per invocation. No activation, remote rclone, commit, push or PR writes. Head observations are read-only and MAESTRO-only.
set -eu
case "${1-}" in
  pins|pins-final|check|package|fixture|freeze|candidate|verify-staged|verify-commit|verify-pr-head|gate-head) ;;
  *) printf '%s\n' 'Usage: host_commands_r13.sh {pins|pins-final|check|package|fixture|freeze|candidate|verify-staged|verify-commit|verify-pr-head|gate-head}' >&2; exit 2 ;;
esac
task_worktree=/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a
task_receipt="$task_worktree/results/backup_gdrive_host_20261011/r13_package_20261011T032105Z"
cd "$task_worktree"
/usr/bin/env LLMDB_ROOT="$task_worktree" PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -B "$task_receipt/capture.py" "$task_receipt/operational_checks" "r13_host_preflight_$1" /usr/bin/python3 -B -c 'import json,os,sys; sys.path.insert(0,sys.argv[1]); from run_py39_coverage import validate_host; validate_host(sys.version_info[:3],os.getpriority(os.PRIO_PROCESS,0),os.environ); print(json.dumps({"interpreter":sys.executable,"version":sys.version,"niceness":os.getpriority(os.PRIO_PROCESS,0)}))' "$task_receipt"
case "$1" in
  pins|pins-final)
    exec /usr/bin/env LLMDB_ROOT="$task_worktree" /usr/bin/python3 -B "$task_receipt/capture.py" "$task_receipt/operational_checks" "r13_host_$1" /usr/bin/shasum -a 256 -c "$task_receipt/pins_v4.sha256"
    ;;
  check)
    exec /usr/bin/env LLMDB_ROOT="$task_worktree" /usr/bin/python3 -B "$task_receipt/capture.py" "$task_receipt" r13_host_plan_check /usr/bin/python3 -B "$task_receipt/check_plan.py" "$task_receipt/activation_plan_v4.md"
    ;;
  package)
    exec /usr/bin/env LLMDB_ROOT="$task_worktree" BACKUP_TEST_NO_RCLONE=1 /usr/bin/python3 -B "$task_receipt/capture.py" "$task_receipt" r13_host_package_driver /usr/bin/python3 -B "$task_receipt/run_r13.py" r13_host_package_green
    ;;
  fixture)
    # This uses real rclone only local→local, isolated HOME, APFS placement/config controls,
    # exact new date,time template, new verify_check, real inventory and owned-group checks.
    exec /usr/bin/env LLMDB_ROOT="$task_worktree" PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -B "$task_receipt/run_py39_coverage.py" r13_host_local_check --mode fixture
    ;;
  freeze)
    # Freeze after new host evidence; capture is outside candidate scope to avoid self-pinning.
    exec /usr/bin/env LLMDB_ROOT="$task_worktree" /usr/bin/python3 -B "$task_receipt/capture.py" "$task_receipt/operational_checks" r13_host_freeze /usr/bin/python3 -B "$task_receipt/freeze_receipt.py"
    ;;
  candidate)
    : "${MAESTRO_SOURCE_COMMIT:?set the full reviewed source SHA after committing this receipt}"
    : "${MAESTRO_CANDIDATE_PATH:?set a fresh isolated absolute candidate path}"
    exec /usr/bin/env LLMDB_ROOT="$task_worktree" /usr/bin/python3 -B "$task_receipt/capture.py" "$task_receipt/operational_checks" r13_host_candidate_create /bin/sh "$task_receipt/make_backup_candidate.sh" create "$task_worktree" "$MAESTRO_SOURCE_COMMIT" "$MAESTRO_CANDIDATE_PATH"
    ;;
  verify-staged)
    : "${MAESTRO_SOURCE_COMMIT:?set the reviewed source SHA}"
    : "${MAESTRO_CANDIDATE_PATH:?set the existing isolated candidate path}"
    exec /usr/bin/env LLMDB_ROOT="$task_worktree" /usr/bin/python3 -B "$task_receipt/capture.py" "$task_receipt/operational_checks" r13_host_verify_staged /bin/sh "$task_receipt/make_backup_candidate.sh" verify-staged "$MAESTRO_CANDIDATE_PATH" "$MAESTRO_SOURCE_COMMIT"
    ;;
  verify-commit)
    : "${MAESTRO_SOURCE_COMMIT:?set the reviewed source SHA}"
    : "${MAESTRO_CANDIDATE_PATH:?set the existing isolated candidate path}"
    : "${MAESTRO_CANDIDATE_COMMIT:?set the captured full candidate commit SHA after MAESTRO commits it}"
    exec /usr/bin/env LLMDB_ROOT="$task_worktree" /usr/bin/python3 -B "$task_receipt/capture.py" "$task_receipt/operational_checks" r13_host_verify_commit /bin/sh "$task_receipt/make_backup_candidate.sh" verify-commit "$MAESTRO_CANDIDATE_PATH" "$MAESTRO_SOURCE_COMMIT" "$MAESTRO_CANDIDATE_COMMIT" --receipt-file "$task_receipt/operational_checks/r13_verified_commit_sha.txt"
    ;;
  verify-pr-head)
    : "${MAESTRO_PR_NUMBER:?set the captured PR number inside the reserved merge window}"
    : "${MAESTRO_CANDIDATE_PATH:?set the existing isolated candidate path}"
    # Saved outputs are validated together before they flow into the binding check.
    /usr/bin/env LLMDB_ROOT="$task_worktree" /usr/bin/python3 -B "$task_receipt/capture.py" "$task_receipt/operational_checks" r13_host_pr_head /opt/homebrew/bin/gh pr view "$MAESTRO_PR_NUMBER" --json headRefOid
    /usr/bin/env LLMDB_ROOT="$task_worktree" /usr/bin/python3 -B "$task_receipt/capture.py" "$task_receipt/operational_checks" r13_host_remote_head /usr/bin/git -C "$MAESTRO_CANDIDATE_PATH" ls-remote origin refs/heads/backup-gdrive-r12
    exec /usr/bin/env LLMDB_ROOT="$task_worktree" /usr/bin/python3 -B "$task_receipt/capture.py" "$task_receipt/operational_checks" r13_host_verify_pr_head /usr/bin/python3 -B "$task_receipt/gate_binding.py" heads "$task_receipt/operational_checks/r13_verified_commit_sha.txt" "$task_receipt/operational_checks/commands/r13_host_pr_head/stdout.txt" "$task_receipt/operational_checks/commands/r13_host_remote_head/stdout.txt"
    ;;
  gate-head)
    : "${MAESTRO_GATE_REPORT:?set the saved gate report JSON path immediately after the gate}"
    exec /usr/bin/env LLMDB_ROOT="$task_worktree" /usr/bin/python3 -B "$task_receipt/capture.py" "$task_receipt/operational_checks" r13_host_gate_head /usr/bin/python3 -B "$task_receipt/gate_binding.py" gate "$task_receipt/operational_checks/r13_verified_commit_sha.txt" "$MAESTRO_GATE_REPORT"
    ;;
esac
