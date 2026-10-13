#!/bin/bash
# C10K Route A chain — runs the pre-registered stages in order with their stop rules.
# Pre-registration commit: ceeaff8 (2026-10-04 12:32). Every step prints CHAIN: lines.
set -uo pipefail
W=/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a
export LLMDB_ROOT="$W"; export PATH="$W/.venv/bin:$PATH"
cd "$W" || exit 1
L="$W/experiments/track_c/c10k_route_a_launcher.py"; R="$W/results/c10k_route_a"; mkdir -p "$R" "$W/logs"
pf() { python - "$1" "$2" <<'EOF'
import json, sys; d = json.load(open(sys.argv[1])); s = d.get("summary") or {}; print(s.get(sys.argv[2], "NA"))
EOF
}

echo "CHAIN: projector gate v2 (Amendment 1, per-layer thresholds) must already have passed"
python - "$R/projector_gate_v2.json" <<'EOF' || { echo "CHAIN: HALT projector gate v2 not passed"; exit 1; }
import json, sys; d = json.load(open(sys.argv[1])); print("CHAIN: gate v2 ok:", d["gate_ok"], "| P:", d["P_file"]); sys.exit(0 if d["gate_ok"] else 1)
EOF

python - "$R/projector_gate_v2_controls.json" <<'EOF' || { echo "CHAIN: HALT gate v2 controls: key parity failed"; exit 1; }
import json, sys; d = json.load(open(sys.argv[1])); print("CHAIN: controls key_parity_ok:", d["key_parity_ok"], "| interference:", d["interference_reading"]); sys.exit(0 if d["key_parity_ok"] else 1)
EOF

echo "CHAIN: anchor start $(date +%T)"
python "$L" anchor > "$W/logs/c10k_route_a_anchor.log" 2>&1; rc=$?
grep -E '^anchor:' "$W/logs/c10k_route_a_anchor.log" | sed 's/^/CHAIN: /'
[ $rc -eq 0 ] || { echo "CHAIN: HALT dynamic anchor failed (rc=$rc) — INVALID per prereg D5"; exit 1; }

if [ "${SKIP_R0:-0}" = 1 ]; then echo "CHAIN: R0 skipped (Amendment 3 rerun; R0 does not depend on L2)"; else
echo "CHAIN: R0 baseline start $(date +%T)"
HP_CANDIDATE="$W/configs/hparams/qwen25_3b_memit_hparams.json" CANDIDATE_NAME=baseline_rerun OUT="$R/R0_baseline.json" \
  python experiments/track_c/c10e_bandknob.py > "$W/logs/c10k_route_a_R0_baseline.log" 2>&1; rc=$?
grep -E 'INERT|canon=|para=' "$W/logs/c10k_route_a_R0_baseline.log" | sed 's/^/CHAIN: R0 /' | tail -12
[ $rc -eq 0 ] || { echo "CHAIN: HALT R0 baseline failed (rc=$rc)"; exit 1; }
fi

echo "CHAIN: R1 controls start $(date +%T)"
python "$L" run --recipe R1 --arms A1_single,A2_coherent2 > "$W/logs/c10k_route_a_R1_controls.log" 2>&1; rc=$?
grep -E '^R1 ' "$W/logs/c10k_route_a_R1_controls.log" | sed 's/^/CHAIN: /'
[ $rc -eq 0 ] || { echo "CHAIN: HALT R1 controls run failed (rc=$rc)"; exit 1; }
A1=$(pf "$R/R1_w1_A1_single.json" para_full); A2=$(pf "$R/R1_w1_A2_coherent2.json" para_full)
echo "CHAIN: R1 controls para_full A1=$A1 A2=$A2 (gate >= 80 both)"
python - "$A1" "$A2" <<'EOF' || { echo "CHAIN: HALTED - CONTROLS_NOT_RECOVERED (no A7 interpretation; one localized fix allowed per prereg)"; exit 2; }
import sys; a, b = (float(x) if x != "NA" else -1 for x in sys.argv[1:3]); sys.exit(0 if a >= 80 and b >= 80 else 1)
EOF

echo "CHAIN: R1 A7 start $(date +%T)"
python "$L" run --recipe R1 --arms A7_coined_coined,stock > "$W/logs/c10k_route_a_R1_A7.log" 2>&1; rc=$?
grep -E '^R1 ' "$W/logs/c10k_route_a_R1_A7.log" | sed 's/^/CHAIN: /'
echo "CHAIN: R1 A7 para_full=$(pf "$R/R1_w1_A7_coined_coined.json" para_full) items_ge2of3=$(python - "$R/R1_w1_A7_coined_coined.json" <<'EOF'
import json, sys; print((json.load(open(sys.argv[1])).get("summary") or {}).get("items_ge2of3", "NA"))
EOF
)"

echo "CHAIN: diagnostics R2 (w50) and R3 (memit_ARE w1) start $(date +%T)"
python "$L" run --recipe R2 --arms A1_single,A2_coherent2,A7_coined_coined > "$W/logs/c10k_route_a_R2.log" 2>&1; grep -E '^R2 ' "$W/logs/c10k_route_a_R2.log" | sed 's/^/CHAIN: /'
python "$L" run --recipe R3 --arms A1_single,A2_coherent2,A7_coined_coined > "$W/logs/c10k_route_a_R3.log" 2>&1; grep -E '^R3 ' "$W/logs/c10k_route_a_R3.log" | sed 's/^/CHAIN: /'
echo "CHAIN: ALL DONE $(date +%T)"
