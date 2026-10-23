# models/Qwen_Qwen2.5-3B

**Job:** Holds the edited payloads of Qwen/Qwen2.5-3B, revision `3aab1f1954e9cc14eb9509a215f9e5ca08227a9b`. The base stays in the HF cache (`hf_cache/hub/models--Qwen--Qwen2.5-3B/snapshots/3aab1f1954e9cc14eb9509a215f9e5ca08227a9b/`) and is the active model line. Every file, size and digest is in `manifests/variants.json`.
**Read it when:** You use one of these variants:
- `variants/b3/` (`safetensors-f16`, `gguf-f16`, `gguf-q4km`): the A1-clean 100-edit batch. Experiment `experiments/b3`; evidence `evidence/CORPUS/17_B3_QUANTIZATION_SURVIVAL.md`. E1 serves `gguf-q4km/b3_edited_q4km.gguf` (`evidence/CORPUS/18_E1_DEPLOYMENT_SERVING.md`).
- `variants/c10l-mint-n/` (`safetensors-f16`, `gguf-f16`, `gguf-q4km`): 24 minted tokens, init arm N. Experiment `experiments/c10l`; evidence `evidence/CORPUS/45_C10L_MINT_TOKEN.md`; committed GGUF digests `experiments/c10l/runs/c10l_mint/p4_gguf_sha256.txt`.
- `variants/c10w-oracle/lora-safetensors/` (runs p1 and p2): 11 rank-16 LoRA adapters. Experiment `experiments/c10w`; evidence `evidence/CORPUS/57_C10W_ORACLE_FINAL.md`. The rest of each run is in `experiments/c10w/runs/c10w_oracle/bulk/c10w_oracle/`.
**Written by:** The root tidy of 2026-10-23 (`program/migrations/root-tidy-20261023/`: old path, new path and before/after digests of every file).
**Read by:** `code/lab/track_b/b3_run.sh`, `b3_edit_and_save.py`, `b3_expand_native.py`, `code/lab/track_a/a7_bias_ablation.py` (b3); `code/lab/track_c/c10l_mint_p4_probe.py` (c10l, path passed as an argument). Recorded run JSON keeps the old paths; the manifest maps old to new.
**Not here:** Covariance statistics: `data/CONTEXT.md`. Run records: `experiments/<id>/`.
