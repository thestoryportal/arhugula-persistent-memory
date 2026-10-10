---
name: prior-art-blendsql-small-models-2026
description: "BlendSQL small models (arXiv 2606.31808): facts in a DB + typed small-LM query functions; CONTEXT for writes, LEAD for read contract, F1 comparator"
metadata:
  type: reference
---

**Source:** https://arxiv.org/html/2606.31808v1 ; code https://github.com/CapitalOne-Research/play-by-the-type-rules/tree/main/sembench (adapted from SemBench).

**What it is:** BlendSQL v0.1.0 = SQL plus polymorphic LM functions (row-wise or aggregate) over DuckDB/SQLite/PostgreSQL; outputs grammar-constrained to declared datatypes (llguidance CFG) — "play by the type rules". Small quantized Gemma 3/4 (E2B, E4B, 4B, 12B) in 16 GB VRAM via vLLM. No weight editing or fine-tuning. SemBench: 5 scenarios (movie, wildlife, e-commerce, cars, MMQA; text/image/audio). Reported: wins 57 % of queries vs Gemini 2.5 Flash, $0.58 vs $226.64 total, ~3.8x lower latency; text competitive, audio weak (0.0 on audio-heavy cars). Early dedup before LM calls saves time; memory footprint flat with scale.

**Placement on the e2e map (docs/SPEC_E2E_GROUND_TRUTH.md):** opposite paradigm to §A (in-context/external store vs in-weight). Write engine (§C, C10): CONTEXT only. **Read path (§G): LEAD** — the spec lists read requirements (exact, reverse, traversal, aggregation/negation) but no query language; typed LM functions over a store are a template for that contract. **Post-write probe (§F):** type-constrained decoding could make the L2 behavioral probe a closed-set check. **F1 comparator:** "DB + small typed LM" is the natural baseline the in-weight approach must beat on cost/reliability.

**Local fit:** code is vLLM + CUDA (RTX 5080); not runnable on the M3 Pro as-is ([[local-only-no-rented-compute]]); a local port is not proposed. Related: [[prior-art-sweep-2026-10]], [[prior-art-chrishayuk-larql-2026-10]].
