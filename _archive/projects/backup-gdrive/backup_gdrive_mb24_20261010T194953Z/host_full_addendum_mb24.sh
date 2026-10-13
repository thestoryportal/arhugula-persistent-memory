#!/bin/bash
set -eu
mb24_build_receipt=results/backup_gdrive_mb24_20261010T194953Z
mb24_host_receipt=$(/opt/homebrew/bin/rtk proxy /usr/bin/mktemp -d /private/tmp/backup_gdrive_mb24_host.XXXXXX)
/opt/homebrew/bin/rtk proxy /bin/mkdir "$mb24_host_receipt/fixtures"
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/rtk proxy .venv/bin/python -B \
  "$mb24_build_receipt/real_path_listing.py" "$mb24_host_receipt/real_paths_before.json"
if LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 BACKUP_TEST_RECEIPTS="$mb24_host_receipt/fixtures" \
  /opt/homebrew/bin/rtk proxy /usr/bin/env -u BACKUP_TEST_NO_RCLONE \
  .venv/bin/python -B -m unittest tools.test_backup_gdrive_addendum -v \
  > "$mb24_host_receipt/full_addendum.log" 2>&1; then
  mb24_suite_rc=0
else
  mb24_suite_rc=$?
fi
printf '%s\n' "$mb24_suite_rc" > "$mb24_host_receipt/full_suite_exit_code.txt"
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/rtk proxy .venv/bin/python -B \
  "$mb24_build_receipt/real_path_listing.py" "$mb24_host_receipt/real_paths_after.json"
if /opt/homebrew/bin/rtk proxy /usr/bin/cmp \
  "$mb24_host_receipt/real_paths_before.json" "$mb24_host_receipt/real_paths_after.json"; then
  printf 'identical\n' > "$mb24_host_receipt/inventory_comparison.txt"
else
  printf 'DIFFERENT\n' > "$mb24_host_receipt/inventory_comparison.txt"
  printf 'MB24 host inventories differ; receipts: %s\n' "$mb24_host_receipt" >&2
  exit 1
fi
printf 'MB24 host full addendum exit %s; receipts: %s\n' "$mb24_suite_rc" "$mb24_host_receipt"
exit "$mb24_suite_rc"
