---
name: gemma4-rung4-candidate
description: Gemma 4 logged as a rung-4 model-swap candidate for the write-engine viability program
metadata: 
  node_type: memory
  type: project
  originSessionId: 2801cf2e-560f-460c-86df-e227b16051b2
---

Gemma 4 (Google, ~April 2026, Apache 2.0) is a LOGGED rung-4 (model-swap / D12-revisit → Category-C → v1.3) candidate for the write-engine viability program. Full eval + sources + a ready Perplexity deep-research prompt: **`/workspace/gemma_rung4_candidate_note.md`**.

Key points:
- Best MEMIT target on the 24GB 4090: **Gemma 4 E4B** (4.5B eff/8B w/emb, 42 layers, dense GeGLU `down_proj` like Qwen → cov solve fits on-GPU, ~8GB). EXCLUDE 26B A4B MoE (128-expert routing → MEMIT covariance/solve ill-defined, not MEMIT-able). 31B dense doesn't fit fp16 (~62GB).
- Status: DOWN-LADDER, LOW prior — same-entity non-locality is model-general (Gate A + literature + GATE-CAL v2), so don't expect Gemma to escape stock-MEMIT failure. Only reach rung 4 after exhausting rungs 0–3 (which preserve the in-weight thesis). But cheap to probe: GATE-CAL v2 (`s242_gatecal.py`) is tokenizer-agnostic.
- Genuine plus: DeepMind **Gemma Scope** open SAEs → strongest public attribute-disentanglement tooling → relevant to rung-3 entity-aware projection / DiKE.
- Primary sources: ai.google.dev/gemma/docs/core/model_card_4 ; github.com/google-deepmind/gemma (JAX ref — read module defs before building MEMIT hparams, LAW #4). Distrust the 2026 SEO "guide" blogs (disagreed with the official card).

Related: [[easyedit-assets-vendored]] (may have Gemma editor hparams). Durable state: `/workspace/SESSION_CHECKPOINT.md`.
