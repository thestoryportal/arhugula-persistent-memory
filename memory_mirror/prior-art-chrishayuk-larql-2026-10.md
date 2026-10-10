---
name: prior-art-chrishayuk-larql-2026-10
description: "Chris Hay's repos surveyed 2026-10-04 — LARQL (program's query layer) now ships its own Rust MEMIT engine + L0/L1/L2 memory tiers + GGUF export/bake-out + Metal; single-token targets only; the-mechanism unchanged since 2026-06-08; tinystories absorb-vs-delegate = locality template"
metadata:
  node_type: memory
  type: reference
  originSessionId: 4d71207f-24bf-4199-894f-d2f977d9f609
  modified: 2026-10-05T00:34:58.240Z
---

**Repo note:** `docs/PRIOR_ART_CHRISHAYUK_LARQL_2026-10.md`. Account: 155 repos; all program-relevant activity is on page 1 (`larql` pushed 2026-10-02, 1,941 commits since June).

**LARQL (Apache-2.0, Rust, 1,162★):** VINDEX3 container (`vindex encode` → `larql vindex3 exec|observe|serve`), Metal default on macOS (88 tok/s Gemma-3-4B; "within 10 % of llama.cpp" credibility rule), GGUF export (2026-08-31) and `COMPILE … INTO MODEL FORMAT gguf` that bakes INSERTed facts via MEMIT into W_down; GGUF-in refused for V3 (V2 only). **Rust MEMIT** `crates/larql-inference/src/forward/memit.rs`: ΔW = (V* − WK*)(K*ᵀC⁻¹K* + λI)⁻¹K*ᵀC⁻¹, Cholesky f64, built-in covariance prompts, λ default 1e-3, "200/200 at N=200 on TinyStories 115M L8–12"; **`MemitFact` = one `target_token_id` (single-token only — do not inherit)**; untouched since 2026-05-10. Memory tiers: L0 KNN → L1 compose → L2 MEMIT (`COMPACT MINOR/MAJOR`), immutable base + patch overlays, "edits verifiable via TRACE parity and reversible". the-mechanism's fleet/routing arc was ported into LARQL's FR track (entity key at L24–26).

**Why it matters:** (a) a decorrelated MEMIT implementation to cross-check our solve/λ/covariance and the key-interference finding ([[c10k-route-a-resume]]); (b) a Metal-native serving alternative to llama.cpp with its own gate; (c) lifecycle vocabulary for the e2e map's Layer 6; (d) `tinystories-train-video` (absorb NLL +6.8 % fails a pre-registered ≤ +5 % gate; delegate −1.5 %) is an M3-runnable locality-metric template. the-mechanism: no change since the program read it. See [[prior-art-sweep-2026-10]].
