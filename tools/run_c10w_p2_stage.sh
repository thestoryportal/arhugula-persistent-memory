#!/bin/bash
# D-C10w-oracle P2, one stage per call (D-C10r-rulings-12; folds results/c10w_oracle_reviews/p2_prerun_{astra,advisor}.md).
# An allow-listed stage runs at most once, and only after tools/c10w_p2_gate.py admits it: engine fingerprint bound to this
# worktree, fail-closed GPU inventory, frozen sources + authorization unchanged, the dispatcher's projection guards.
# Exit: 2 usage/repeat, 3 gate refused (no stage log written, P2 directory untouched), otherwise the stage's own exit.
# Launch through tools/run_c10w_p2.sh, the single P2 coordinator - never by hand between stages.
W=/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a
S="$1"; D=$W/results/c10w_oracle_logs; L=$D/$S.log
case "$S" in p2-a7-s1|p2-shuf-s1|p2-canon-s1|p2-a1-s1|p2-a7-rt|p2-shuf-rt|p2-eval) ;; *) echo "usage: $0 p2-a7-s1|p2-shuf-s1|p2-canon-s1|p2-a1-s1|p2-a7-rt|p2-shuf-rt|p2-eval"; exit 2;; esac
[ -e "$L" ] && { echo "REFUSE: $L exists (stage already run)"; exit 2; }
mkdir -p "$D" || exit 2
unset C10_KEY_LOCUS C10_CTX_TEMPLATES C10_ARMS N_EDIT C10_SUBJECT_OFFSET HP_CANDIDATE C10_PROJECTOR C10_RECIPES MODEL_ID MODEL_REV LLMDB_DEVICE
gate=$(LLMDB_ROOT="$W" "$W/.venv/bin/python" -B "$W/tools/c10w_p2_gate.py" "$S" < /dev/null); grc=$?
# Every gate decision is kept, admitted or refused, so a refusal is diagnosable after the fact.
echo "$gate" > "$D/$S.gate.$(date '+%Y%m%dT%H%M%S').$$.json" || exit 2
[ "$grc" -eq 0 ] || { echo "REFUSE: $S gate rc=$grc"; echo "$gate"; exit 3; }
{ echo "P2 gate admitted $S:"; echo "$gate"; } > "$L" || exit 2
LLMDB_ROOT=$W bash "$W/tools/run_c10w_stage.sh" "$S" >> "$L" 2>&1 < /dev/null
rc=$?; echo "STAGE_EXIT=$rc" >> "$L"; exit $rc
