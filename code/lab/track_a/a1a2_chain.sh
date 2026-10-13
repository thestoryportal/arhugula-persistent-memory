#!/bin/bash
cd /workspace
echo "waiting for A1 covariances..."
n=0; until grep -q 'ALL COV DONE' s246_qwen3_cov.log 2>/dev/null; do
  sleep 30; n=$((n+1))
  ! pgrep -f s246_qwen3_cov >/dev/null && ! grep -q 'ALL COV DONE' s246_qwen3_cov.log && { echo "COV PROC DIED early"; grep -aiE 'cov L|error|Traceback' s246_qwen3_cov.log|tail -5; exit 1; }
  [ $n -ge 120 ] && { echo "COV TIMEOUT 60min"; exit 1; }
done
echo "=== A1 COV COMPLETE ==="; grep -aE 'cov L' s246_qwen3_cov.log
echo "=== launching A2 calibration smoke ==="
PYTHONUNBUFFERED=1 python -u s247_qwen3_recipe.py 2>&1 | grep -aviE 'Warning|warn|shards|it/s|deprecated|Computing locally|download' | tail -25
echo "A1A2_CHAIN_DONE"
