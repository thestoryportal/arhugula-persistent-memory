#!/bin/sh
# RED adapter: v2 exports reviewed files and checks pins, without complete diff scope.
set -eu
task_package=$(/usr/bin/dirname "$0")
exec /usr/bin/python3 -B "$task_package/candidate.py" "$@"
