#!/bin/bash
# D-C10u-mint2 one stage (usage: run_c10u_stage.sh <stage>); explicit worktree root; never two at once.
STAGE="$1"
[ -n "$STAGE" ] || { echo "usage: run_c10u_stage.sh <stage>"; exit 2; }
W=/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a
export LLMDB_ROOT=$W PYTHONUNBUFFERED=1
unset LLMDB_DEVICE
cd "$W" || exit 2
LOGS=$W/results/c10u_mint2_logs/r2
mkdir -p "$LOGS"
"$W/.venv/bin/python" "$W/experiments/track_c/c10u_mint2_arms.py" "$STAGE" --law3-ref "$W/results/c10l_covgeom/run1_armB_identity.json" --out-dir "$W/results/c10u_mint2/r2" > "$LOGS/$STAGE.log" 2>&1
rc=$?
echo "STAGE_EXIT=$rc" >> "$LOGS/$STAGE.log"
exit $rc
