#!/bin/bash
set -eu
mb25_build_receipt=results/backup_gdrive_mb25_20261010T202206Z
mb25_host_receipt=$(/opt/homebrew/bin/rtk proxy /usr/bin/mktemp -d /private/tmp/backup_gdrive_mb25_host.XXXXXX)
[ -n "$mb25_host_receipt" ] && [ -d "$mb25_host_receipt" ]
/opt/homebrew/bin/rtk proxy /bin/mkdir "$mb25_host_receipt/fixtures"
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/rtk proxy .venv/bin/python -B \
  "$mb25_build_receipt/real_path_listing.py" "$mb25_host_receipt/real_paths_before.json"
if LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 BACKUP_TEST_RECEIPTS="$mb25_host_receipt/fixtures" \
  /opt/homebrew/bin/rtk proxy /usr/bin/env -u BACKUP_TEST_NO_RCLONE \
  .venv/bin/python -B -m unittest tools.test_backup_gdrive_addendum -v \
  > "$mb25_host_receipt/full_addendum.log" 2>&1; then
  mb25_addendum_rc=0
else
  mb25_addendum_rc=$?
fi
printf '%s\n' "$mb25_addendum_rc" > "$mb25_host_receipt/addendum_exit_code.txt"
if LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 BACKUP_TEST_RECEIPTS="$mb25_host_receipt/fixtures" \
  /opt/homebrew/bin/rtk proxy /usr/bin/env -u BACKUP_TEST_NO_RCLONE \
  .venv/bin/python -B -m unittest tools.test_backup_gdrive -v \
  > "$mb25_host_receipt/base_suite.log" 2>&1; then
  mb25_base_rc=0
else
  mb25_base_rc=$?
fi
printf '%s\n' "$mb25_base_rc" > "$mb25_host_receipt/base_exit_code.txt"
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/rtk proxy .venv/bin/python -B \
  "$mb25_build_receipt/real_path_listing.py" "$mb25_host_receipt/real_paths_after.json"
if /opt/homebrew/bin/rtk proxy /usr/bin/cmp \
  "$mb25_host_receipt/real_paths_before.json" "$mb25_host_receipt/real_paths_after.json"; then
  printf 'identical\n' > "$mb25_host_receipt/inventory_comparison.txt"
else
  printf 'DIFFERENT\n' > "$mb25_host_receipt/inventory_comparison.txt"
  printf 'MB25 host inventories differ; receipts: %s\n' "$mb25_host_receipt" >&2
  exit 1
fi
printf 'MB25 host addendum exit %s, base exit %s; receipts: %s\n' "$mb25_addendum_rc" "$mb25_base_rc" "$mb25_host_receipt"
if [ "$mb25_addendum_rc" -ne 0 ]; then exit "$mb25_addendum_rc"; fi
if [ "$mb25_base_rc" -ne 0 ]; then exit "$mb25_base_rc"; fi
if /opt/homebrew/bin/rtk proxy rg -q '^Ran 137 tests ' "$mb25_host_receipt/full_addendum.log" && \
   /opt/homebrew/bin/rtk proxy rg -q '^OK$' "$mb25_host_receipt/full_addendum.log" && \
   /opt/homebrew/bin/rtk proxy rg -q '^Ran 10 tests ' "$mb25_host_receipt/base_suite.log" && \
   /opt/homebrew/bin/rtk proxy rg -q '^OK$' "$mb25_host_receipt/base_suite.log"; then
  printf '137 addendum OK, 10 base OK, 0 skipped; inventory identical\n' > "$mb25_host_receipt/acceptance.txt"
else
  printf 'MB25 host count, status or skip mismatch; inspect receipts: %s\n' "$mb25_host_receipt" >&2
  exit 1
fi
