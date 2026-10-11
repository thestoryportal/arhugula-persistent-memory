#!/bin/bash
# MAESTRO-only read-only acceptance; never rebuilds or controls a live pane.
set -u
if [ "$#" -ne 2 ] || [[ ! "$1" =~ ^[A-Za-z0-9_-]+$ ]] || [[ "$2" != red && "$2" != green ]]; then
    printf 'Usage: bash run_host.sh LABEL red|green\n' >&2
    exit 2
fi
RECEIPT=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd) || exit 2
ROOT=$(cd -- "$RECEIPT/../../.." && pwd) || exit 2
UTC=$(/bin/date -u +%Y%m%dT%H%M%SZ) || exit 2
OUT=$(/usr/bin/mktemp -d "$RECEIPT/host_${1}_${2}_${UTC}_XXXXXX") || exit 2
printf '%s\n' "$UTC" > "$OUT/utc.txt"
printf 'Receipt: %s\n' "$OUT"
LLMDB_ROOT="$ROOT" PYTHONDONTWRITEBYTECODE=1 MB38_HOST_RUN=1 PATH="/opt/homebrew/bin:$PATH" \
    /opt/homebrew/bin/rtk proxy /usr/bin/python3 -B "$ROOT/tests/test_dashboard_live_host.py" \
    --root "$ROOT" --before "$RECEIPT/before" --receipt "$OUT" --phase "$2" \
    > "$OUT/run.log" 2>&1
run_rc=$?
printf '%s\n' "$run_rc" > "$OUT/run.exit"
/opt/homebrew/bin/rtk proxy cat "$OUT/run.log"
exit "$run_rc"
