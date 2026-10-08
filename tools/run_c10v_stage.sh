#!/bin/bash
# D-C10v-layerpick, one stage per call (D-C10v-go): GPU-exclusivity check, worktree env, no inherited harness knobs, outer log + exit kept, never repeat a stage.
W=/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a
S="$1"; L=$W/results/c10v_layerpick_logs/$S.log
case "$S" in step0|pass1|pass2) ;; *) echo "usage: $0 step0|pass1|pass2"; exit 2;; esac
[ -e "$L" ] && { echo "REFUSE: $L exists (stage already run)"; exit 2; }
busy=$(/bin/ps -axo pid,command | grep -E 'python.*(experiments/track_c/|c10w_oracle|autoresearch|memit_dry_run)' | grep -v -E 'grep|selftest|_read\.py|_interim\.py')
[ -n "$busy" ] && { echo "REFUSE: GPU not exclusive:"; echo "$busy"; exit 3; }
tmux has-session -t autoresearch 2>/dev/null && { echo "REFUSE: tmux session autoresearch exists"; exit 3; }
mkdir -p "$W/results/c10v_layerpick_logs"
unset MODEL_ID MODEL_REV HP_CANDIDATE OUT CANDIDATE_NAME DECISION_ID PREREG RUN_LABEL Z_OVERRIDE C10_PROJECTOR N_EDIT C10_SUBJECT_OFFSET C10_ARMS C10_KEY_LOCUS C10_CTX_TEMPLATES C10_RECIPES MINT_ARM MINT_STEP0 MINT_INITS MINT_N_SEED LAW3_REF LLMDB_DEVICE
{ echo "GPU exclusivity checked $(date '+%Y-%m-%dT%H:%M:%S%z'): no other track_c/oracle/autoresearch/engine python process"; } > "$L"
env LLMDB_ROOT=$W "$W/.venv/bin/python" -B "$W/experiments/track_c/c10v_layerpick_arms.py" "$S" \
  --root "$W" --law3-ref "$W/results/c10q_stacked/passS.json" \
  --operator-go --steps-1-3-complete --autoresearch-state paused >> "$L" 2>&1 < /dev/null
rc=$?; echo "STAGE_EXIT=$rc" >> "$L"; exit $rc
