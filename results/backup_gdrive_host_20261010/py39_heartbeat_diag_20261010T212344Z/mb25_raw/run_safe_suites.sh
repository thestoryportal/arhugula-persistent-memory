#!/bin/bash
set -eu
mb25_receipt="$PWD/results/backup_gdrive_host_20261010/py39_run_20261010T210113Z"
mb25_fixture_home=$(/opt/homebrew/bin/rtk proxy /bin/cat "$mb25_receipt/run_home.txt")
[ -n "$mb25_fixture_home" ] && [ -d "$mb25_fixture_home" ]
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/rtk proxy /usr/bin/python3 -B \
  "$mb25_receipt/real_path_listing.py" "$mb25_receipt/real_paths_before.json"
if /opt/homebrew/bin/rtk proxy /usr/bin/env HOME="$mb25_fixture_home" LLMDB_ROOT="$PWD" \
  PYTHONDONTWRITEBYTECODE=1 BACKUP_PYTHON=/usr/bin/python3 BACKUP_TEST_NO_RCLONE=1 \
  BACKUP_TEST_RECEIPTS="$mb25_receipt/fixtures" PYTHONPATH="$mb25_receipt/observer" \
  PY39_TRACE="$mb25_receipt/execution_trace.jsonl" PY39_TARGET_STATUS="$PWD/tools/backup_gdrive_status.py" \
  /usr/bin/python3 -B -m unittest \
  tools.test_backup_gdrive.BackupTest.test_held_lock_refuses_and_logs_without_changing_destination \
  tools.test_backup_gdrive.BackupTest.test_stale_lock_refuses_explicitly_without_auto_removal -v \
  > "$mb25_receipt/base_suite.log" 2>&1; then
  mb25_base_rc=0
else
  mb25_base_rc=$?
fi
printf '%s\n' "$mb25_base_rc" > "$mb25_receipt/base_suite.exit"
if /opt/homebrew/bin/rtk proxy /usr/bin/env HOME="$mb25_fixture_home" LLMDB_ROOT="$PWD" \
  PYTHONDONTWRITEBYTECODE=1 BACKUP_PYTHON=/usr/bin/python3 BACKUP_TEST_NO_RCLONE=1 \
  BACKUP_TEST_RECEIPTS="$mb25_receipt/fixtures" PYTHONPATH="$mb25_receipt/observer" \
  PY39_TRACE="$mb25_receipt/execution_trace.jsonl" PY39_TARGET_STATUS="$PWD/tools/backup_gdrive_status.py" \
  /usr/bin/python3 -B -m unittest \
  tools.test_backup_gdrive_addendum.StatusTest \
  tools.test_backup_gdrive_addendum.HeartbeatTest \
  tools.test_backup_gdrive_addendum.LaunchReceiptTest \
  tools.test_backup_gdrive_addendum.GenerationStatusTest \
  tools.test_backup_gdrive_addendum.GenerationLaunchTest \
  tools.test_backup_gdrive_addendum.R5RecoveryTest \
  tools.test_backup_gdrive_addendum.R7PublicationTemporaryTest \
  tools.test_backup_gdrive_addendum.R7ArchivePrecisionTest \
  tools.test_backup_gdrive_addendum.R8CurrentUnresolvedTest \
  tools.test_backup_gdrive_addendum.R8DuplicateKeysTest \
  tools.test_backup_gdrive_addendum.R5CompactionTest \
  tools.test_backup_gdrive_addendum.GenerationWrapperTest \
  tools.test_backup_gdrive_addendum.ArchiveTest -v \
  > "$mb25_receipt/addendum_suite.log" 2>&1; then
  mb25_addendum_rc=0
else
  mb25_addendum_rc=$?
fi
printf '%s\n' "$mb25_addendum_rc" > "$mb25_receipt/addendum_suite.exit"
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/rtk proxy /usr/bin/python3 -B \
  "$mb25_receipt/real_path_listing.py" "$mb25_receipt/real_paths_after_suites.json"
if /opt/homebrew/bin/rtk proxy /usr/bin/cmp "$mb25_receipt/real_paths_before.json" "$mb25_receipt/real_paths_after_suites.json"; then
  printf 'identical\n' > "$mb25_receipt/inventory_comparison.txt"
else
  printf 'DIFFERENT\n' > "$mb25_receipt/inventory_comparison.txt"
  exit 1
fi
printf 'base exit=%s, addendum exit=%s\n' "$mb25_base_rc" "$mb25_addendum_rc"
/opt/homebrew/bin/rtk proxy rg '^Ran |^OK|^FAILED|^ERROR:|^FAIL:' "$mb25_receipt/base_suite.log" "$mb25_receipt/addendum_suite.log"
if [ "$mb25_base_rc" -ne 0 ]; then exit "$mb25_base_rc"; fi
exit "$mb25_addendum_rc"
