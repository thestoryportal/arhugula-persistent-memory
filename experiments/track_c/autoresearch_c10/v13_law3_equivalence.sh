#!/bin/bash
# PROGRAM SESSION ONLY. Loads the real model; never run during no-model work.
# Expected fd16592: heldout_full=7/72, dw_total=88.974, templates_sha=e8605172dce0.
# Absolute tensor hashes: A1 2f72fee29064643ce2214e7d644f88a71292e56c35ab657b3b3d355405cbaab1
# A2 f94e1be2258482a84201432aec35f88c59f25e7b9d325345a447a108e0e2dd56
# A7 c30664a92b06be43485a2043b4512d08d977df2708289f558d5ba03a5a7da965
set -euo pipefail
PROGRAM="/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a"
FENCE="/Volumes/memit/llm-database-poc-mirror/autoresearch_fence_v13_c10"
ANCHOR="$(/usr/bin/shasum -a 256 "$FENCE/sealed/manifest.json")"
exec /usr/bin/env -i HOME="$HOME" USER="$USER" PATH=/usr/bin:/bin:/usr/sbin:/sbin \
  PYTHONDONTWRITEBYTECODE=1 "$PROGRAM/.venv/bin/python" -I -B \
  "$FENCE/v13_verify_gpu.py" "$FENCE" "${ANCHOR%% *}"
