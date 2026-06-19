#!/bin/bash
# B3/G6.2 orchestrator: convert edited HF -> fp16 GGUF -> Q4_K_M -> probe both -> verdict.
set -e
cd /workspace
SRC=$LLMDB_ROOT/llama_cpp_src
BIN=$SRC/build/bin
ED=$LLMDB_ROOT/b3_edited_qwen3b
F16=$LLMDB_ROOT/b3_edited_f16.gguf
Q4=$LLMDB_ROOT/b3_edited_q4km.gguf

echo "=== [1/5] convert HF -> fp16 GGUF ==="
python $SRC/convert_hf_to_gguf.py $ED --outfile $F16 --outtype f16

echo "=== [2/5] quantize -> Q4_K_M (REAL) ==="
$BIN/llama-quantize $F16 $Q4 Q4_K_M

probe_model () {  # $1=gguf  $2=outpred  $3=port
  echo "  starting server on :$3 for $1"
  $BIN/llama-server -m "$1" -ngl 0 -c 2048 --port "$3" --host 127.0.0.1 > $LLMDB_ROOT/b3_server_$3.log 2>&1 &
  SPID=$!
  sleep 3
  python $LLMDB_ROOT/experiments/track_b/b3_probe.py "http://127.0.0.1:$3" "$2"
  kill $SPID 2>/dev/null || true
  sleep 2
}

echo "=== [2.5] SMOKE: fp16 GGUF reproduces HF edit (France->Cairo) before full probe ==="
$BIN/llama-server -m "$F16" -ngl 0 -c 2048 --port 8230 --host 127.0.0.1 > $LLMDB_ROOT/logs/b3_server_smoke.log 2>&1 &
SMPID=$!; sleep 3
python $LLMDB_ROOT/experiments/track_b/b3_smoke.py "http://127.0.0.1:8230" || true
kill $SMPID 2>/dev/null || true; sleep 2

echo "=== [3/5] probe fp16 GGUF ==="
probe_model "$F16" $LLMDB_ROOT/results/b3_pred_f16.json 8231
echo "=== [4/5] probe Q4_K_M GGUF ==="
probe_model "$Q4" $LLMDB_ROOT/results/b3_pred_q4.json 8232

echo "=== [5/5] verdict ==="
python $LLMDB_ROOT/experiments/track_b/b3_verdict.py
echo "B3_RUN_DONE"
