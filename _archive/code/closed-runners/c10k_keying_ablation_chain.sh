#!/bin/bash
# D-C10k-keying-ablation chain (docs/C10K_KEYING_ABLATION_PREREG.md v3): K1 gate (LAW#3, ±3 pp of R0 A1 94.4 / A2 98.6) then K2–K4.
# Each cell = c10e harness, candidate recipe only, arms A1+A2, base hparams (fact_token subject_last); knobs set the key locus and templates.
set -uo pipefail
export DECISION_ID=D-C10k-keying-ablation PREREG="docs/C10K_KEYING_ABLATION_PREREG.md" RUN_LABEL="C10K keying-locus ablation"   # provenance: Codex review v2 found the harness default D-C10e-bandknob in the result JSONs
W="${LLMDB_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"; export LLMDB_ROOT="$W"; export PATH="$W/.venv/bin:$PATH"; export HF_HUB_OFFLINE=1
cd "$W" || exit 1; R="$W/results/c10k_keying_ablation"; mkdir -p "$R" "$W/logs"
run_cell() {  # name locus templates
  echo "ABL: $1 start $(date +%T) locus=$2 templates=$3"
  HP_CANDIDATE="$W/configs/hparams/qwen25_3b_memit_hparams.json" CANDIDATE_NAME="$1" OUT="$R/$1.json" \
  C10_ARMS=A1_single,A2_coherent2 C10_RECIPES=candidate C10_KEY_LOCUS="$2" C10_CTX_TEMPLATES="$3" \
    python experiments/track_c/c10e_bandknob.py > "$W/logs/c10k_keying_ablation_$1.log" 2>&1; rc=$?
  grep -E "VALIDITY|INERT|A1_single|A2_coherent2" "$W/logs/c10k_keying_ablation_$1.log" | sed "s/^/ABL: $1 /" | cut -c1-400
  [ $rc -eq 0 ] || { echo "ABL: HALT $1 failed (rc=$rc)"; exit 1; }
  python - "$R/$1.json" "$1" <<'EOF'
import json, sys; d = json.load(open(sys.argv[1])); a = d["recipes"][sys.argv[2]]["arms"]
print("ABL:", sys.argv[2], "A1 para_full", a["A1_single"]["para_full"], "canon", a["A1_single"]["canon_full"], "loc", a["A1_single"]["locality_described_as"], "| A2 para_full", a["A2_coherent2"]["para_full"], "canon", a["A2_coherent2"]["canon_full"], "loc", a["A2_coherent2"]["locality_described_as"])
EOF
}
run_cell K1 subject on
python - "$R/K1.json" <<'EOF' || { echo "ABL: HALT K1 outside LAW#3 tolerance (±3 pp of 94.4 / 98.6)"; exit 1; }
import json, sys; a = json.load(open(sys.argv[1]))["recipes"]["K1"]["arms"]; a1, a2 = a["A1_single"]["para_full"], a["A2_coherent2"]["para_full"]
ok = abs(a1 - 94.4) <= 3 and abs(a2 - 98.6) <= 3; print("ABL: K1 gate", "PASS" if ok else "FAIL", a1, a2); sys.exit(0 if ok else 1)
EOF
run_cell K2 subject off
run_cell K3 last on
run_cell K4 last off
echo "ABL: ALL DONE $(date +%T)"
