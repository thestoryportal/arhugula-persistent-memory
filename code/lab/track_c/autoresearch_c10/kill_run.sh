#!/bin/bash
# Generated at installation: no arguments, no inherited credential/runtime variables.
set -euo pipefail
[ "$#" -eq 0 ] || { echo "status: failure"; exit 1; }
actual="$(/usr/bin/shasum -a 256 '@FENCE@/@ENTRY@')"
[ "${actual%% *}" = '@ENTRY_SHA@' ] || { echo "status: failure"; exit 1; }
exec /usr/bin/env -i HOME='@HOME@' USER='@USER@' PATH=/usr/bin:/bin:/usr/sbin:/sbin \
  PYTHONDONTWRITEBYTECODE=1 '@PY@' -I -B -X 'pycache_prefix=@FENCE@/scorer_tmp/parent_pycache' '@FENCE@/@ENTRY@' '@ANCHOR@'
