#!/bin/bash
# D-C10l-mint P4 (amendment B2): mint-edited HF model (saved by c10l_mint_arms.py with MINT_SAVE_DIR) -> fp16 GGUF -> Q4_K_M
# -> llama-server (-ngl 0, CPU) probes of both -> results/c10l_mint/p4_*.json. Toolchain = the B3 one on this machine
# (convert_hf_to_gguf.py from llama_cpp_src; official prebuilt b11382 binaries; no native build, Command Line Tools broken).
set -euo pipefail
export LLMDB_ROOT=/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a
MAIN=/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory
SRC=$MAIN/llama_cpp_src
BIN=$SRC/prebuilt/llama-b11382
PY=$LLMDB_ROOT/.venv/bin/python
RES=$LLMDB_ROOT/results/c10l_mint
ED=${MINT_SAVE_DIR:-$MAIN/c10l_mint_edited_qwen3b_N}
ARM=${ARM_JSON:-$RES/arm_N_p4.json}
F16=$MAIN/c10l_mint_N_f16.gguf
Q4=$MAIN/c10l_mint_N_q4km.gguf
mkdir -p "$RES"
echo "=== [1/4] convert HF -> fp16 GGUF ($ED)"
"$PY" "$SRC/convert_hf_to_gguf.py" "$ED" --outfile "$F16" --outtype f16 > "$RES/logs_p4_convert.log" 2>&1
echo "=== [2/4] quantize -> Q4_K_M"
"$BIN/llama-quantize" "$F16" "$Q4" Q4_K_M > "$RES/logs_p4_quantize.log" 2>&1
probe () {  # gguf out port label
  "$BIN/llama-server" -m "$1" -ngl 0 -c 2048 --port "$3" --host 127.0.0.1 > "$RES/logs_p4_server_$3.log" 2>&1 &
  SPID=$!
  sleep 4
  "$PY" "$LLMDB_ROOT/experiments/track_c/c10l_mint_p4_probe.py" "http://127.0.0.1:$3" "$ED" "$2" "$4"
  kill $SPID 2>/dev/null || true
  sleep 2
}
echo "=== [3/4] probe fp16 GGUF"
probe "$F16" "$RES/p4_pred_f16.json" 8241 gguf_f16
echo "=== [4/4] probe Q4_K_M GGUF"
probe "$Q4" "$RES/p4_pred_q4km.json" 8242 gguf_q4km
ls -la "$F16" "$Q4"
shasum -a 256 "$F16" "$Q4" > "$RES/p4_gguf_sha256.txt"
"$PY" "$LLMDB_ROOT/experiments/track_c/c10l_mint_p4_verdict.py" "$RES/p4_pred_f16.json" "$RES/p4_pred_q4km.json" "$RES/p4_verdict.json"
echo P4_DONE
