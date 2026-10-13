## RUNG-4 CANDIDATE LOGGED: Gemma 4 (2026-06-17, operator-requested)
See **`/workspace/docs/gemma_rung4_candidate_note.md`** (full eval + sources + a ready Perplexity deep-research prompt).
- Best MEMIT target on this pod: **Gemma 4 E4B** (4.5B eff/8B, 42 layers, dense GeGLU `down_proj` like Qwen → on-GPU cov solve, ~8GB). Exclude 26B MoE (not MEMIT-able). 31B doesn't fit fp16.
- Status: down-ladder (rung 4 = D12-revisit/Category-C → v1.3), LOW prior (same-entity failure is model-general), but cheap to probe (GATE-CAL v2 is portable). Genuine plus: DeepMind **Gemma Scope** SAEs (disentanglement → rung-3/DiKE angle).
- Sources: ai.google.dev/gemma/docs/core/model_card_4 + /core ; github.com/google-deepmind/gemma (JAX ref, read for module defs before building hparams).
- Decision pending: queue the E4B GATE-CAL v2 probe, or keep as logged candidate while we finish in-paradigm rungs 0–3.

