---
name: q4km-quantization-survival-pass
description: B3/G6.2 PASS — the A1-clean batch in-weight store survives real Q4_K_M deployment quantization (edits 100% vs native 97.4%); margin confound characterized
metadata: 
  node_type: memory
  type: project
  originSessionId: ba0f7d12-2172-4518-b3b6-963f1e0dd709
---

2026-06-18 (`CORPUS/17`). **B3/G6.2 = PASS.** The A1-clean BATCH in-weight store (Qwen2.5-3B, 100 edits / 50 entities × 2 fields, single joint AlphaEdit solve) **survives real Q4_K_M deployment quantization**: edited-fact retention **100% (99/99)** vs native-country **97.4% (75/77)**, Δ=+2.6 pts (threshold ≥ −3). Validity gate clean (HF↔GGUF-fp16 top-1 agreement 100% on edited AND native → conversion faithful, not a converter artifact). Edits also served correctly under llama.cpp **CPU** inference (`-ngl 0`) = partial E1. Real Q4_K_M (4.99 BPW) via self-built llama.cpp — NOT FP4, NOT the crude sim.

**Key caveat (characterized, not just flagged):** `compute_z` inflates edited-fact margins by construction — edited top-1 prob median **0.979** vs native **0.812** (min 0.33). Larger margin → harder to flip under quantization. So 100% edited retention is plausibly a margin artifact. The earned claim is "**edits survive Q4_K_M deployment quantization**" — NOT the pre-registration's literal "indistinguishable from native knowledge." (Advisor caught this slide from private reasoning into a dropped footnote; reinforces [[match-metric-to-the-claim]].)

**Scope:** quantization survival only — NOT "CPU deployment validated." The LARQL `gguf-to-vindex` ingest + serving on the real Intel-CPU target is **E1, untested**. N≤100, 3B only, Q4_K_M only, one ordering, batch store (incremental + [[scope-gate-batch-is-deployment-model]]'s parked A3 untested).

**How to apply:** the batch store is quantization-deployable at Q4_K_M; this clears a real CPU-deployment falsifier. Next live falsifiers: E1 (real deployment loop), B1 (larger model), C/G7 (multi-token), D1 (capacity law for F1). llama.cpp built at `/workspace/llama_cpp_src/build/bin/` — server target needs `-DLLAMA_BUILD_UI=OFF` (web-UI download is network-gated). Edited model saved at `/workspace/b3_edited_qwen3b` + GGUFs `b3_edited_{f16,q4km}.gguf`.
