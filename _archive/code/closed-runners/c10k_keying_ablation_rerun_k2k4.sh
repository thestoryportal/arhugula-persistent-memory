#!/bin/bash
# D-C10k-keying-ablation: re-run the templates-off cells (K2, K4) after the LAW#5 parity check was made knob-independent
# (first pass: NOT INERT by construction → harness halted → K2/K4 INVALID as run). K1 gate already PASSED (95.8 / 97.2).
set -uo pipefail
W="${LLMDB_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"; export LLMDB_ROOT="$W"; export PATH="$W/.venv/bin:$PATH"; export HF_HUB_OFFLINE=1
cd "$W" || exit 1; R="$W/results/c10k_keying_ablation"
run_cell() {
  echo "ABL: $1 start $(date +%T) locus=$2 templates=$3 (rerun)"
  HP_CANDIDATE="$W/configs/hparams/qwen25_3b_memit_hparams.json" CANDIDATE_NAME="$1" OUT="$R/$1.json" \
  C10_ARMS=A1_single,A2_coherent2 C10_RECIPES=candidate C10_KEY_LOCUS="$2" C10_CTX_TEMPLATES="$3" \
    python experiments/track_c/c10e_bandknob.py > "$W/logs/c10k_keying_ablation_$1.log" 2>&1; rc=$?
  grep -E "VALIDITY|INERT|A1_single|A2_coherent2" "$W/logs/c10k_keying_ablation_$1.log" | sed "s/^/ABL: $1 /" | cut -c1-400
  [ $rc -eq 0 ] || { echo "ABL: HALT $1 failed (rc=$rc)"; exit 1; }
  python - "$R/$1.json" "$1" <<'EOF' || echo "ABL: $1 has no arms record (INVALID)"
import json, sys; d = json.load(open(sys.argv[1])); a = d["recipes"][sys.argv[2]]["arms"]
print("ABL:", sys.argv[2], "A1 para_full", a["A1_single"]["para_full"], "canon", a["A1_single"]["canon_full"], "loc", a["A1_single"]["locality_described_as"], "| A2 para_full", a["A2_coherent2"]["para_full"], "canon", a["A2_coherent2"]["canon_full"], "loc", a["A2_coherent2"]["locality_described_as"])
EOF
}
run_cell K2 subject off
[ "${RERUN_K4:-0}" = 1 ] && run_cell K4 last off
echo "ABL: K2 RERUN DONE $(date +%T)"
