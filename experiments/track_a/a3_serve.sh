#!/bin/bash
cd $LLMDB_ROOT/external_prior_art/larql
export OPENBLAS_NUM_THREADS=8 OMP_NUM_THREADS=8 HF_HOME=$LLMDB_ROOT/hf_cache
echo "=== A3: extract vindex from multi-edited Qwen3 weights ==="
rm -rf /dev/shm/qwen3_multiedit.vindex
target/release/larql convert safetensors-to-vindex --output /dev/shm/qwen3_multiedit.vindex --level all --f16 /dev/shm/qwen3_multiedit 2>&1 | tail -2
echo "=== A3: LARQL serves the multi-fact edit? (edited: France->Berlin Japan->Cairo Germany->Lima Italy->Oslo Spain->Hanoi Poland->Nairobi; controls Greece/Egypt/China should be unchanged) ==="
V=/dev/shm/qwen3_multiedit.vindex
for e in France Japan Germany Italy Spain Poland Greece Egypt China; do
  echo "--- $e ---"
  timeout 120 target/release/larql lql "USE \"$V\"; INFER \"The capital of $e is the city of\" TOP 2;" 2>&1 | grep -aviE 'gate=|F[0-9]+ +gate|Inference trace|Using:|walk FFN|ms$|^$' | grep -aiE 'Predictions|^   1\.|^   2\.' | head -3
done
echo "A3_SERVE_DONE"
