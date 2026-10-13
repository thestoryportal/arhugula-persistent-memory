## EXTERNAL PRIOR ART (operator-supplied 2026-06-17): LARQL is IN THE SPEC
Cloned to `/workspace/external_prior_art/{larql,the-mechanism}` (Chris Hay). Memory: `larql-the-mechanism-prior-art`.
- LARQL (Rust) = vindex (the spec's `.vindex`) + LQL (SQL over weights) + MEMIT-class INSERT→down_proj (ridge/MemitStore solve, multi-layer constellation, AT LAYER/ALPHA/CONFIDENCE) + COMPILE→standard safetensors/GGUF + CPU/no-GPU serving (~26 tok/s Q4K). Supports Qwen2.5. = the read/query + DEPLOYMENT layer (closes our Intel-CPU loop: edit on GPU → compile vindex → LARQL serves on CPU).
- OUR same-entity-locality work FILLS LARQL'S GAP (it checks edit-success + cross-entity, not same-entity multi-attribute locality).
- BAND cross-ref: LARQL + the-mechanism write at LATE fact-resolution band (Gemma ~L23-28); our MEMIT edits early-mid [3-8]. If a model's early-band underperforms, try late band.

