#!/bin/bash
# Prospective collector only; run from the admitted worktree/export root.
set -euo pipefail
umask 077
bound=results/research_engine_phase1_20261011/intel_provisioning_manifest_v5_bound.json
if [[ $# -lt 2 || "$2" != "$bound" ]]; then
    echo "REFUSED: supply MODE $bound [ENTRY]" >&2
    exit 1
fi
exec /usr/bin/python3 -I -B results/research_engine_phase1_20261011/r1e_collector.py "$@"
