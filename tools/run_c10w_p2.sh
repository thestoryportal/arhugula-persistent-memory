#!/bin/bash
# D-C10w-oracle P2 launch coordinator (P2 pre-run review: Astra B1/B2, advisor A2). The ONE process that dispatches P2:
# it waits out the predecessor GPU job, then runs the seven P2 stages in order through tools/run_c10w_p2_stage.sh,
# holding the GPU from p2-a7-s1 to the P2 reading, so no other GPU job is launched between stages.
# It advances only on an exact outer STAGE_EXIT=0 with no new HALT record. The dispatcher's inner STAGE_EXIT=75
# (underfit, followed by its one declared 800-step retry) stays inside a stage and is never read here.
# Resumable after a STOP: a stage whose outer log ends STAGE_EXIT=0 is skipped; any other existing stage log STOPs.
# The last line of the coordinator log is always COORDINATOR_EXIT=<code> <reason>; a missing line means it died.
# Usage: run_c10w_p2.sh <predecessor pid> <predecessor log> | --reattempt-eval <P2 directory>
W="$(cd -- "$(dirname -- "$0")/.." && pwd)" || exit 2
[ $# -eq 2 ] || { echo "usage: $0 <predecessor pid> <predecessor log>"; exit 2; }
PRED_PID=$1; PRED_LOG=$2
D=$W/results/c10w_oracle_logs; C=$D/p2-coordinator.log; AP=$W/architecture_profile
REATTEMPT=""
if [ "$1" = --reattempt-eval ]; then
  REATTEMPT=$2
  [ "$REATTEMPT" = "$W/results/c10w_oracle/p2_20261008T034226_086980Z" ] || { echo "REFUSE: re-attempt belongs to another P2 directory"; exit 2; }
  LLMDB_ROOT="$W" "$W/.venv/bin/python" -B "$W/tools/c10w_p2_rerun.py" verify || exit 3
  C=$D/p2-reattempt-coordinator.$(date '+%Y%m%dT%H%M%S').$$.log
  (set -C; : > "$C") || { echo "REFUSE: coordinator invocation log exists"; exit 2; }
fi
mkdir -p "$D" || exit 2
say() { echo "$(date '+%Y-%m-%dT%H:%M:%S%z') $*" >> "$C"; }
finish() { say "COORDINATOR_EXIT=$1 $2"; exit "$1"; }
halt_diagnostics() { find "$AP" -maxdepth 1 -name 'c10w_oracle_halt_diagnostic_*.json' | wc -l | tr -d ' '; }
say "START coordinator pid=$$ predecessor pid=$PRED_PID log=$PRED_LOG"
if [ -z "$REATTEMPT" ]; then
  while /bin/ps -p "$PRED_PID" > /dev/null; do sleep 30; done
  pred=$(grep '^STAGE_EXIT=' "$PRED_LOG" | tail -1)
  [ -n "$pred" ] || finish 4 "predecessor exited without STAGE_EXIT in $PRED_LOG"
  say "predecessor finished: $pred"
fi
newest_p2() { find "$W/results/c10w_oracle" -maxdepth 1 -type d -name 'p2_*' | sort | tail -1; }
for S in p2-a7-s1 p2-shuf-s1 p2-canon-s1 p2-a1-s1 p2-a7-rt p2-shuf-rt p2-eval; do
  L=$D/$S.log
  # Checked before every stage, skipped ones included, so a resumed run never walks past a HALTED directory.
  p2=$(newest_p2); [ -z "$p2" ] || [ ! -e "$p2/HALT.json" ] || finish 7 "P2 directory HALTED before $S ($p2)"
  if [ -e "$L" ]; then
    [ "$(tail -1 "$L")" = "STAGE_EXIT=0" ] || finish 5 "$S log exists without STAGE_EXIT=0; a stage is never repeated"
    say "SKIP $S (already STAGE_EXIT=0)"; continue
  fi
  [ -z "$REATTEMPT" ] || [ "$S" = p2-eval ] || finish 5 "re-attempt cannot dispatch training $S"
  before=$(halt_diagnostics)
  say "DISPATCH $S"
  if [ -n "$REATTEMPT" ]; then
    bash "$W/tools/run_c10w_p2_stage.sh" "$S" --reattempt "$REATTEMPT" >> "$C" 2>&1 < /dev/null; rc=$?
  else
    bash "$W/tools/run_c10w_p2_stage.sh" "$S" >> "$C" 2>&1 < /dev/null; rc=$?
  fi
  last=""; [ -f "$L" ] && last=$(tail -1 "$L")
  [ "$rc" -eq 0 ] && [ "$last" = "STAGE_EXIT=0" ] || finish 6 "$S stopped: wrapper rc=$rc, outer log last line '$last'"
  [ "$(halt_diagnostics)" = "$before" ] || finish 7 "$S wrote a new HALT diagnostic in $AP"
  p2=$(newest_p2)
  [ -n "$p2" ] && [ ! -e "$p2/HALT.json" ] || finish 7 "$S: P2 directory missing or HALTED ($p2)"
  say "DONE $S"
done
R=$D/p2-read.json
if [ -n "$REATTEMPT" ]; then
  R=$D/p2-read-attempt2.json
  (set -C; LLMDB_ROOT=$W "$W/.venv/bin/python" -B "$W/tools/c10w_p2_rerun.py" read > "$R" 2>> "$C" < /dev/null); rrc=$?
else
  LLMDB_ROOT=$W "$W/.venv/bin/python" -B "$W/experiments/track_c/c10w_oracle_read.py" > "$R" 2>> "$C" < /dev/null; rrc=$?
fi
status=$("$W/.venv/bin/python" -B -c 'import json,sys; print(json.load(open(sys.argv[1]))["status"])' "$R") || finish 8 "P2 reading did not parse (reader rc=$rrc, $R)"
case "$status" in INVALID|UNSTABLE) finish 9 "P2 reading status $status (reader rc=$rrc, $R)";; esac
finish 0 "P2 complete; reading status=$status (reader rc=$rrc, $R)"
