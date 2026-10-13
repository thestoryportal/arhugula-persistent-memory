#!/bin/bash
# D-C10w-oracle P2, one stage per call (D-C10r-rulings-12; folds experiments/c10w/reviews/c10w_oracle_reviews/p2_prerun_{astra,advisor}.md).
# An allow-listed stage runs at most once, and only after code/lab/runners/c10w_p2_gate.py admits it: engine fingerprint bound to this
# worktree, fail-closed GPU inventory, frozen sources + authorization unchanged, the dispatcher's projection guards.
# Exit: 2 usage/repeat, 3 gate refused (no stage log written, P2 directory untouched), otherwise the stage's own exit.
# Launch through code/lab/runners/run_c10w_p2.sh, the single P2 coordinator - never by hand between stages.
W="$(cd -- "$(dirname -- "$0")/../../.." && pwd)" || exit 2
S="$1"; D=$W/experiments/c10w/runs/c10w_oracle/logs; L=$D/$S.log
case "$S" in p2-a7-s1|p2-shuf-s1|p2-canon-s1|p2-a1-s1|p2-a7-rt|p2-shuf-rt|p2-eval) ;; *) echo "usage: $0 p2-a7-s1|p2-shuf-s1|p2-canon-s1|p2-a1-s1|p2-a7-rt|p2-shuf-rt|p2-eval"; exit 2;; esac
REATTEMPT=""; EXTRA=()
if [ "$#" -ne 1 ]; then
  [ "$#" -eq 3 ] && [ "$S" = p2-eval ] && [ "$2" = --reattempt ] || { echo "REFUSE: usage: $0 p2-eval --reattempt <P2 directory>"; exit 2; }
  REATTEMPT=$3; EXTRA=(--reattempt "$REATTEMPT")
  [ ! -e "$REATTEMPT/reattempt2.json" ] || { echo "REFUSE: second re-attempt"; exit 2; }
fi
if [ "$S" = p2-eval ] && [ -e "$W/experiments/c10w/runs/c10w_oracle/p2_20261008T034226_086980Z/attempt1_halted/manifest.json" ] && [ -z "$REATTEMPT" ]; then
  echo "REFUSE: archived P2 requires explicit sealed re-attempt"; exit 2
fi
[ -e "$L" ] && { echo "REFUSE: $L exists (stage already run)"; exit 2; }
mkdir -p "$D" || exit 2
unset C10_KEY_LOCUS C10_CTX_TEMPLATES C10_ARMS N_EDIT C10_SUBJECT_OFFSET HP_CANDIDATE C10_PROJECTOR C10_RECIPES MODEL_ID MODEL_REV LLMDB_DEVICE
gate=$(LLMDB_ROOT="$W" "$W/.venv/bin/python" -B "$W/code/lab/runners/c10w_p2_gate.py" "$S" "${EXTRA[@]}" < /dev/null); grc=$?
# Every gate decision is kept, admitted or refused, so a refusal is diagnosable after the fact.
GATE_FILE="$D/$S.gate.$(date '+%Y%m%dT%H%M%S').$$.json"
(set -C; echo "$gate" > "$GATE_FILE") || exit 2
[ "$grc" -eq 0 ] || { echo "REFUSE: $S gate rc=$grc"; echo "$gate"; exit 3; }
if [ -n "$REATTEMPT" ]; then
  LLMDB_ROOT="$W" "$W/.venv/bin/python" -B "$W/code/lab/runners/c10w_p2_rerun.py" claim "$REATTEMPT" "$GATE_FILE" || exit 2
fi
(set -C; { echo "P2 gate admitted $S:"; echo "$gate"; } > "$L") || exit 2
if [ -n "$REATTEMPT" ]; then
  LLMDB_ROOT="$W" "$W/.venv/bin/python" -B "$W/code/lab/runners/c10w_p2_rerun.py" dispatch "$REATTEMPT" >> "$L" 2>&1 < /dev/null
else
  LLMDB_ROOT=$W bash "$W/code/lab/runners/run_c10w_stage.sh" "$S" >> "$L" 2>&1 < /dev/null
fi
rc=$?; echo "STAGE_EXIT=$rc" >> "$L"; exit $rc
