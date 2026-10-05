#!/bin/bash
# D-C10k-keying-ablation §6 amendment: last-token keying at small ridge weights (K3' = 500, K3'' = 50), then K1' only if K3'' is valid.
set -uo pipefail
W="${LLMDB_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"; export LLMDB_ROOT="$W"; export PATH="$W/.venv/bin:$PATH"; export HF_HUB_OFFLINE=1
cd "$W" || exit 1; R="$W/results/c10k_keying_ablation"
run_cell() {  # name locus templates hparams
  echo "ABL: $1 start $(date +%T) locus=$2 templates=$3 hparams=$(basename "$4")"
  HP_CANDIDATE="$4" CANDIDATE_NAME="$1" OUT="$R/$1.json" C10_ARMS=A1_single,A2_coherent2 C10_RECIPES=candidate C10_KEY_LOCUS="$2" C10_CTX_TEMPLATES="$3" \
    python experiments/track_c/c10e_bandknob.py > "$W/logs/c10k_keying_ablation_$1.log" 2>&1; rc=$?
  grep -E "VALIDITY|INERT|A1_single|A2_coherent2" "$W/logs/c10k_keying_ablation_$1.log" | sed "s/^/ABL: $1 /" | cut -c1-400
  [ $rc -eq 0 ] || { echo "ABL: HALT $1 failed (rc=$rc)"; exit 1; }
  python - "$R/$1.json" "$1" <<'EOF' || echo "ABL: $1 has no arms record (INVALID)"
import json, sys; d = json.load(open(sys.argv[1])); a = d["recipes"][sys.argv[2]]["arms"]
print("ABL:", sys.argv[2], "A1 para_full", a["A1_single"]["para_full"], "canon", a["A1_single"]["canon_full"], "loc", a["A1_single"]["locality_described_as"], "| A2 para_full", a["A2_coherent2"]["para_full"], "canon", a["A2_coherent2"]["canon_full"], "loc", a["A2_coherent2"]["locality_described_as"], "| valid:", a["A1_single"]["canon_full"] >= 90 and a["A2_coherent2"]["canon_full"] >= 90)
EOF
}
run_cell K3p last on "$W/configs/hparams/qwen25_3b_memit_hparams_mom2w500.json"
run_cell K3pp last on "$W/configs/hparams/qwen25_3b_memit_hparams_mom2w50.json"
python - "$R/K3pp.json" <<'EOF' && run_cell K1p subject on "$W/configs/hparams/qwen25_3b_memit_hparams_mom2w50.json"
import json, sys; a = json.load(open(sys.argv[1]))["recipes"]["K3pp"]["arms"]; sys.exit(0 if a["A1_single"]["canon_full"] >= 90 and a["A2_coherent2"]["canon_full"] >= 90 else 1)
EOF
echo "ABL: SMALL-RIDGE DONE $(date +%T)"
