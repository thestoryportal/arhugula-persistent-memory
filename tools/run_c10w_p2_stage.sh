#!/bin/bash
# D-C10w-oracle P2, one stage per call (D-C10r-rulings-12): P2 stages only, GPU-exclusivity check, worktree env, no FORBIDDEN_ENV, outer log + exit kept, never repeat a stage.
W=/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a
S="$1"; L=$W/results/c10w_oracle_logs/$S.log
case "$S" in p2-a7-s1|p2-shuf-s1|p2-canon-s1|p2-a1-s1|p2-a7-rt|p2-shuf-rt|p2-eval) ;; *) echo "usage: $0 p2-a7-s1|p2-shuf-s1|p2-canon-s1|p2-a1-s1|p2-a7-rt|p2-shuf-rt|p2-eval"; exit 2;; esac
[ -e "$L" ] && { echo "REFUSE: $L exists (stage already run)"; exit 2; }
busy=$(/bin/ps -axo pid,command | grep -E 'python.*(experiments/track_c/|c10w_oracle|autoresearch|memit_dry_run)' | grep -v -E 'grep|selftest|_read\.py|_interim\.py')
[ -n "$busy" ] && { echo "REFUSE: GPU not exclusive:"; echo "$busy"; exit 3; }
tmux has-session -t autoresearch 2>/dev/null && { echo "REFUSE: tmux session autoresearch exists"; exit 3; }
/usr/bin/pgrep -il ollama >/dev/null && { echo "REFUSE: ollama is running"; exit 3; }
mkdir -p "$W/results/c10w_oracle_logs"
unset C10_KEY_LOCUS C10_CTX_TEMPLATES C10_ARMS N_EDIT C10_SUBJECT_OFFSET HP_CANDIDATE C10_PROJECTOR C10_RECIPES MODEL_ID MODEL_REV LLMDB_DEVICE
{ echo "GPU exclusivity checked $(date '+%Y-%m-%dT%H:%M:%S%z'): no other track_c/oracle/autoresearch/engine python process, no ollama"; } > "$L"
LLMDB_ROOT=$W bash "$W/tools/run_c10w_stage.sh" "$S" >> "$L" 2>&1 < /dev/null
rc=$?; echo "STAGE_EXIT=$rc" >> "$L"; exit $rc
