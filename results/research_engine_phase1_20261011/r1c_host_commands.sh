#!/bin/bash
# Prospective collector only; run from the admitted worktree/export root.
set -euo pipefail
umask 077
exec /usr/bin/python3 -I -B results/research_engine_phase1_20261011/r1c_collector.py "$@"
