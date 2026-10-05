#!/bin/bash
# D-C10k-keying-ablation discriminator (advisor v2 on §6): single-fact (N = 1) last-token writes at the operating weight w = 5000,
# six subjects (offsets 0..5), A1 arm, templates on. If single edits land (canon = 100 for the one item), the collapse at N = 24
# is key-similarity/interference, not ridge magnitude; if they also fail, the ridge account gains support. Prints ABL lines.
set -uo pipefail
W="${LLMDB_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"; export LLMDB_ROOT="$W"; export PATH="$W/.venv/bin:$PATH"; export HF_HUB_OFFLINE=1
cd "$W" || exit 1; R="$W/results/c10k_keying_ablation/n1"; mkdir -p "$R"
for off in 0 1 2 3 4 5; do
  for locus in last subject; do
    name="N1_${locus}_$off"; echo "ABL: $name start $(date +%T)"
    HP_CANDIDATE="$W/configs/hparams/qwen25_3b_memit_hparams.json" CANDIDATE_NAME="$name" OUT="$R/$name.json" N_EDIT=1 C10_SUBJECT_OFFSET=$off \
    C10_ARMS=A1_single C10_RECIPES=candidate C10_KEY_LOCUS="$locus" C10_CTX_TEMPLATES=on python experiments/track_c/c10e_bandknob.py > "$W/logs/c10k_keying_ablation_$name.log" 2>&1; rc=$?
    grep -E "VALIDITY|A1_single " "$W/logs/c10k_keying_ablation_$name.log" | grep -v "base=" | sed "s/^/ABL: $name /" | cut -c1-300
    [ $rc -eq 0 ] || echo "ABL: $name failed (rc=$rc)"
  done
done
echo "ABL: N1 DONE $(date +%T)"
