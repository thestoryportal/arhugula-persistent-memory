---
name: larql-the-mechanism-prior-art
description: "Chris Hay's LARQL + the-mechanism (+ his wider GitHub corpus) vs our write-engine work. ⚠ REVISED 2026-06-23 (Tier-1 deep-read): the old 'our work fills LARQL's gap' claim is PARTLY INVERTED — he's built a parallel impl with mechanisms we theorized. See docs/CHRISHAYUK_CORPUS_GAP_MAP.md + HYPOTHESIS_REGISTER §K + runbook §0.3."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 2801cf2e-560f-460c-86df-e227b16051b2
---

> **⚠ REVISED 2026-06-23 — Tier-1 deep-read of chrishayuk's FULL corpus** (`docs/CHRISHAYUK_CORPUS_GAP_MAP.md`, `HYPOTHESIS_REGISTER §K`, runbook §0.3 flag). Chris Hay has independently built a **near-complete parallel implementation of our thesis** (`larql` engine + `.vindex`/`.vlp` + `tiny-model` Gemma-GQA w/ frozen-FFN-retrain-attention + `the-mechanism`). This **PARTLY INVERTS point 2 below** ("our work fills LARQL's gap"): LARQL already implements a tiered KNN→COMPOSE→L2-MEMIT hybrid **+ a `REBALANCE` fixed-point solver** — mechanisms we only theorized. **Four LOAD-BEARING gaps for us** (LEADS, unverified on Qwen except quant): **(CP2)** LQL has **NO aggregation/negation/JOIN/multi-hop/"violates"** → our read-contract query-families are *net-new on top of LARQL, not served*; native read = relation-index(L10) × fuzzy-entity-top-k(L24-26, rank/verify), **not** single-row. **(B3)** the hybrid + `REBALANCE` above. **(write)** LARQL serve = **MEMIT (vanilla ridge), NOT AlphaEdit** — no null-space locality guarantee at serve. **(quant) ✅ VERIFIED 2026-06-23:** LARQL keeps ffn_down **uniformly Q6_K**; our B3 `Q4_K_M` put **4/5 edited band-[4-8] down_proj layers at Q4_K** (stricter) and edits survived 100% → our result is CONSERVATIVE, LARQL merely more protective. Shared still-OPEN (he doesn't solve either): **GQA edit-transfer** + **multi-token**.

Chris Hay's **LARQL** is INTEGRATED INTO THE LLM-as-DB SPEC (operator, 2026-06-17) as the read/query + deployment layer. Repos cloned (primary source): `/workspace/external_prior_art/larql` (Rust, mature) and `/workspace/external_prior_art/the-mechanism` (Python, 10 Gemma demos = the talk "The Model Doesn't Unpack Its Memory").

**LARQL = vindex (the spec's `.vindex`) + LQL (SQL over weights) + its own MEMIT-class write path + CPU deployment.**
- vindex: model decompiled to queryable store; "down_proj become edge labels." DESCRIBE entity → edges (capital/language/continent/borders) with per-relation layer locations.
- Write path is MEMIT-class: INSERT INTO EDGES … AT LAYER N CONFIDENCE c ALPHA a → allocates a feature in **down_proj** via ridge/MemitStore solve (demo_memit_solve, memit_solve bench). Multi-layer "constellation." Patches (.vlp), COMPILE back to standard safetensors/GGUF (loads in HF/llama.cpp, no special loader).
- Deployment = the operator's Intel-CPU goal, ALREADY BUILT: "No GPU required," CPU Q4K ~26 tok/s mmap walk FFN; supports Qwen 2/2.5. Closes the loop: edit on GPU (our engine) → compile to vindex/safetensors → LARQL serves on CPU.

**Why it matters for our write-engine viability work:**
1. Validates our architecture (down_proj store, multi-attribute entities, MEMIT-class solve) and the CPU-deployment path. See [[deployment-target-intel-cpu]].
2. OUR WORK FILLS LARQL'S GAP — **⚠ PARTLY INVERTED, see top banner: LARQL already ships the compaction hybrid + `REBALANCE` we theorized.** [original claim, now scoped:] LARQL's INSERT checks edit-success + CROSS-entity/neighbor preservation, but does NOT appear to test SAME-ENTITY multi-attribute locality (our Phase 1 axis). Our result (sequential same-subject edits clobber on GPT-J, hold on Qwen) tells LARQL which base models it can safely multi-edit + argues for a same-entity/sequential-edit safety gate.
3. BAND SELECTION: LARQL (INSERT AT LAYER ~24-27, phase transition L24) and the-mechanism (FACT_BAND [23-28], resolve @ L26 on Gemma) write at LATE layers where the fact resolves; our canonical MEMIT edits EARLY-MID ([3-8]) (ROME knowledge-MLP locus). Model-specific. If our small-Qwen early-band underperforms, try a LATER band (the LARQL/mechanism locus) as the one fix.
4. LARQL's late-band constellation+ALPHA insert is a candidate write MECHANISM to test against our same-entity battery (possible Rung-1/2 workaround).

LARQL is Rust; our experiments are Python/transformers — integration is at the artifact level (vindex/safetensors), not code. The `.vindex` here is the spec's §8.4 `.vindex` tier (Rung 2b). Relates to [[easyedit-assets-vendored]] (the other vendored editor toolkit).

**Mechanistic theory (talk transcript `research_and_specs/model_does_not_unpack_memory.md`) — explains our findings + motivates our rungs:**
- Thesis: "the model PACKS to store but ADDRESSES to read; it never unpacks/decodes." Facts are superposed in down_proj slots; each is read by a LINEAR address = RELATION + ENTITY, resolved in a mid-to-late "fact band" (~L23-27), built up layer-by-layer (fuzzy→exact→snap-in). Basis: Geva et al. "FFN = key-value memory."
- SAME-ENTITY BLEED = ADDRESS COLLISION. An entity's attributes sit at distinct relation-addresses in one packed vector, independently readable UNLESS edits collide ("when they collide the model can no longer read it"). Our JS-drift metric effectively measures collision; Qwen local ⇒ its relation-addresses separate more cleanly than GPT-J's. Mechanistic explanation of [[gemma4-rung4-candidate]]/Phase-1 model-dependence.
- Independently motivates RUNG 3 (entity-aware/orthogonal projection): his "trick" = insert "aligned to all relations, firing at one without interfering with others" = write ΔW orthogonal to the entity's OTHER (s,r') addresses.
- BAND: facts build ~L14-25, snap L23-27; LARQL injects in the building band (~L20), NOT late, not purely early. If a model's early-band [3-8] edits bleed/underperform → try the relation-resolution band. (Qwen-7B clean at [4-8], so early works there.)
- Motivates RUNG 5 / externalization: "store the key-value pairs in an external store, respect the addressing sequence, scale to millions" = GRACE-like parameter-preserving escape AND a CPU deployment-scaling path. LARQL roadmap heads there.
- Framing: reads are free+local by construction (addressing); the ONLY hard part of the LLM-as-DB is write-side collision = same-entity locality — exactly what our program isolates.
