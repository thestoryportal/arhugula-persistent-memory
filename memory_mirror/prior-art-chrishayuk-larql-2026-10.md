---
name: prior-art-chrishayuk-larql-2026-10
description: "LARQL (Chris Hay): Rust MEMIT (single-token only), L0/L1/L2 tiers, GGUF bake-out, Metal; cross-check for our solve and a serving alternative"
metadata:
  type: reference
---

**Repo note:** `docs/PRIOR_ART_CHRISHAYUK_LARQL_2026-10.md`. Account: 155 repos; all program-relevant activity is on page 1 (`larql` pushed 2026-10-02, 1,941 commits since June).

**LARQL (Apache-2.0, Rust, 1,162★):** VINDEX3 container (`vindex encode` → `larql vindex3 exec|observe|serve`), Metal default on macOS (88 tok/s Gemma-3-4B; "within 10 % of llama.cpp" credibility rule), GGUF export (2026-08-31) and `COMPILE … INTO MODEL FORMAT gguf` that bakes INSERTed facts via MEMIT into W_down; GGUF-in refused for V3 (V2 only). **Rust MEMIT** `crates/larql-inference/src/forward/memit.rs`: ΔW = (V* − WK*)(K*ᵀC⁻¹K* + λI)⁻¹K*ᵀC⁻¹, Cholesky f64, built-in covariance prompts, λ default 1e-3, "200/200 at N=200 on TinyStories 115M L8–12"; **`MemitFact` = one `target_token_id` (single-token only — do not inherit)**; untouched since 2026-05-10. Memory tiers: L0 KNN → L1 compose → L2 MEMIT (`COMPACT MINOR/MAJOR`), immutable base + patch overlays, "edits verifiable via TRACE parity and reversible". the-mechanism's fleet/routing arc was ported into LARQL's FR track (entity key at L24–26).

**Why it matters:** (a) a decorrelated MEMIT implementation to cross-check our solve/λ/covariance and the key-interference finding (CORPUS/42–43); (b) a Metal-native serving alternative to llama.cpp with its own gate; (c) lifecycle vocabulary for the e2e map's Layer 6; (d) `tinystories-train-video` (absorb NLL +6.8 % fails a pre-registered ≤ +5 % gate; delegate −1.5 %) is an M3-runnable locality-metric template. the-mechanism: no change since the program read it. See [[prior-art-sweep-2026-10]].

**From the 2026-06-23 deep-read (absorbed from the retired larql-the-mechanism-prior-art note; detail `docs/CHRISHAYUK_CORPUS_GAP_MAP.md`):** theory (talk transcript `research_and_specs/model_does_not_unpack_memory.md`) — the model PACKS to store but ADDRESSES to read (linear RELATION + ENTITY address); same-entity bleed = address collision. Four load-bearing gaps for us: **(CP2)** LQL has no aggregation/negation/JOIN/multi-hop/"violates" → our read-contract query families are net-new on top of LARQL; **(B3)** LARQL already ships a tiered KNN→COMPOSE→L2-MEMIT hybrid + a `REBALANCE` fixed-point solver (the hybrid we decided in D-B3N-1); **(write)** LARQL serve uses vanilla ridge MEMIT, not AlphaEdit — no null-space locality guarantee; **(quant)** LARQL keeps ffn_down uniformly Q6_K, so our B3 Q4_K_M survival (4/5 edited band layers at Q4_K, 100% survival, CORPUS/17) is the stricter test. Shared and still open: GQA edit transfer and multi-token values.
