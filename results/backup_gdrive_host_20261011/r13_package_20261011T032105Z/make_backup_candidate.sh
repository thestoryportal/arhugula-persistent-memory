#!/bin/sh
# MAESTRO only: create an isolated candidate; stage files but never commit/push/open a PR.
set -eu
task_package=$(/usr/bin/dirname "$0")
exec /usr/bin/python3 -B "$task_package/candidate.py" "$@"
