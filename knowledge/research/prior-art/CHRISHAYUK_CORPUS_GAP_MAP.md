# Chris Hay (chrishayuk) Corpus — Gap-Map vs Our Open Questions

_Durable record of a Tier-1 deep-read (2026-06-23) of Chris Hay's GitHub corpus (he is the **LARQL author**), mapped against the LLM-as-Database program's open questions. **These are prior-art LEADS, not `CORPUS/` evidence** — high confidence on *what his code says*, lower on transfer to our stack (his models are Gemma-3-**4B** / `tiny-model`, not Qwen; `the-mechanism` is not reproducible without his private `chuk-mlx`/Lazarus; small n; several repos carry **no license** → reference/learn, do not vendor). Genuine gaps logged to `HYPOTHESIS_REGISTER_2026-06-18.md §K`; the load-bearing four flagged in `EXPERIMENT_RUNBOOK.md §0.3`._

## 0. Headline
Chris Hay has independently built a **near-complete parallel implementation of our exact thesis** — `larql` (the serve/query engine + `.vindex`/`.vlp` format) + `tiny-model` (a Gemma-shaped GQA model trained with a **frozen-FFN / retrain-attention** phase + `vindex` extraction) + `the-mechanism` (the key→value FFN read demonstrator, labelled "**LARQL MODE COMPOSE**"). His corpus was **not fully captured in our CORPUS**, and **reading was required** — every load-bearing finding below is a code-level fact (LQL grammar, default quant precision, a hidden `REBALANCE` solver) that no text-network/InfraNodus pass could surface.

---

## 1. The four LOAD-BEARING gaps (bear on live decisions)

### L1 — CP2 read-contract is partly **unsupported** by LARQL (reshapes CP2 scope)
LARQL's LQL (`larql-lql` spec v0.4) is `SELECT/WALK/DESCRIBE/INFER/TRACE` over `(s,r,o)` edges:
```
SELECT [fields] FROM {EDGES|FEATURES|ENTITIES}
  [NEAREST TO <entity> AT LAYER <n>] [WHERE <preds>] [ORDER BY <f> {ASC|DESC}] [LIMIT <n>]
WHERE ops: = != > < >= <= LIKE IN        DELETE FROM EDGES WHERE ...
```
Plus reverse lookup (same `SELECT`, bind `relation`), `NEAREST TO … AT LAYER` (vector-kNN read), and **FR3 synonym-robust relation resolution** (probe resolves "seat"→capital "by meaning"). **But it has NO aggregation, NO GROUP BY, NO JOIN, NO negation/NOT-EXISTS, NO multi-hop in `SELECT`, and NO "violates"/constraint mechanism at all** (verified against the parser + AST + a full grep). Our CP2 frames "L1 SELECT readback + 5 query families + violates-rejection + reverse/aggregation/negation" → **aggregation, negation, and violates are net-new on top of LARQL, not served.** (Aggregation exists only as a *research finding* + a *fleet-routing dispatch conjecture*; multi-hop exists as unexposed `CHAIN`.) Closest substitute for NOT-EXISTS = `ROUTE VERIFY`'s **abstain** path.

Also (`the-mechanism`): the native read **decomposes into 2 stages** — a *clean RELATION index at L10* (synonym-generalises, prob=1.0) × a *fuzzy ENTITY candidate-list at L24–26* (top-1≈0.67 / top-5≈0.84, then rank/verify). So a native readback is intrinsically a **ranked short-list you must verify, not a deterministic single row**, and the **optimal read layer is field-dependent** (relation early, entity/value late). If CP2 assumes deterministic single-row readback at one layer, that's a confound.

### L2 — B3: LARQL **already implements the compaction-bounded hybrid** we *decided* (D-B3N-1) — with a `REBALANCE` solver
LARQL ships a tiered (LSM-like) store and tiers *between* in-weight and side-store:
- `MODE KNN` — **side-store**, L0, residual-key override, "scales freely (25K edges, 87 edges/s)", does **not** touch the forward pass.
- `MODE COMPOSE` — **in-weight** FFN overlay, L1, participates in the forward, **caps ~5–10 facts/layer (Hopfield-style)**.
- `COMPACT MINOR` (L0→L1) / `COMPACT MAJOR [WITH LAMBDA]` (L1→**L2 MEMIT-decomposed**) promotion ladder; **`REBALANCE [UNTIL CONVERGED]`** = a global fixed-point that rescales each compose-install's down-magnitude so target prob lands in `[FLOOR,CEILING]` — **the mechanism that breaks the greedy per-insert cap.**

Our `D-B3N-1` "compaction-bounded hybrid under 3 conditions" **converges with his design** — but he has the *actual* rebalance mechanism we only theorized, and a working tier policy. Side-store reliability lever (`virtual-experts`): **route the normalized canonical *action* (`{expert,operation,parameters}`), not raw NL** → routing becomes deterministic classification; a "routing failure" may be an upstream *normalization* failure (a confound to control).

### L3 — Edit-mechanism mismatch: LARQL serve = **MEMIT (vanilla ridge), NOT AlphaEdit**
LARQL's in-tree solve is `memit_solve` = ridge with **no covariance / null-space projection**; MEMIT bake is gated `LARQL_MEMIT_ENABLE=1` and **off-by-default on Gemma** ("template-sharing cross-hijacks"). Our recipe leans on **AlphaEdit null-space** for locality — **LARQL's serve layer does not provide that guarantee** (and that's *why* its COMPOSE path needs `REBALANCE`). Gap if our write contract assumes AlphaEdit locality semantics at serve time. (`the-mechanism`'s `native.py` is a third point: **training-free, projection-free single-neuron write** at the model's own captured address, 6/6 retention — a cheaper single-fact contrast to both.)

### L4 — Quantization: LARQL keeps FFN `down` at **Q6_K (not Q4_K)** by default, and bakes-then-requantizes-whole
Default Q4_K_M *mix* (`build_q4k_weights.rs`): **Attn Q/K/O=Q4_K, Attn V=Q6_K, FFN gate/up=Q4_K, FFN down=Q6_K** — i.e. it **protects the down-projection** (the exact tensor our edit lives in) at higher precision. COMPILE bakes the edit into **f32** `down_weights.bin` (column-rewrite + additive MEMIT ΔW), **then** re-quantizes the whole vindex (`vindex_to_q4k`). Plus a numerical-stability trick: COMPILE **deliberately does NOT bake the inserted gate vector** (keeps the source's weak gate so dense activation stays small). → Check our **B3/G6.2 (CORPUS/17)** Q4_K_M result: did we quantize `down` at Q4_K or Q6_K?

> **✅ VERIFIED 2026-06-23** (inspected `b3_edited_q4km.gguf` with gguf-py). `Q4_K_M` makes `ffn_down` a **per-layer MIX (18×Q6_K / 18×Q4_K)**. Our edit band is layers **[4,5,6,7,8]** (`mlp.down_proj`); their precision came out **L4=Q4_K, L5=Q4_K, L6=Q6_K, L7=Q4_K, L8=Q4_K** → **4 of 5 edited layers at real 4-bit Q4_K**, only L6 at Q6_K. So our B3 test was **STRICTER** than LARQL's uniform-Q6_K-down serve path — and the edits **still survived 100%**. **Resolution = FAVORABLE:** the B3 quant-survival result is **conservative/robust** (it rode through real 4-bit on the majority of edited layers, not protected at Q6_K); LARQL is merely *more* protective by default (an optional extra margin — force `ffn_down→Q6_K` — that we don't depend on), **not a hidden weakness in ours.** Gotcha logged: `Q4_K_M` ≠ uniform 4-bit; `ffn_down`/`attn_v` are a Q6_K/Q4_K mix — verify per-tensor. (Logged to `[[q4km-quantization-survival-pass]]` + register K4.)

### (L5 — deployment risk) GGUF export is still 🔴 **Planned** in LARQL
Only **safetensors** lands today (`COMPILE INTO MODEL`); **GGUF output is roadmap-only**, there is **no CUDA backend** (CPU + Metal only), and **no continuous batching**. Our GGUF/CPU-deploy story partly assumes a path that isn't merged in LARQL. (Our own llama.cpp Q4_K path is independent — but the LARQL-native GGUF route is not there yet.)

---

## 2. Genuinely OPEN — shared blind spots (he doesn't answer either)
- **GQA architecture-transfer of editing: untested everywhere.** `mha_gqa_benchmark` is an unreliable **LLM-prose-style judge**, *not* weight-editing. GQA's `repeat_interleave` means an edited K/V direction lands on **all heads in a group** — uncharacterized vs MHA. Our **7B (Qwen-GQA) transfer (OQ-W1)** stays genuinely open; the one repo named for it doesn't address the weight-editing form.
- **Multi-token values (G7): unaddressed by LARQL's own author.** `the-mechanism` is all **single-token** (it drops multi-token facts; pools are 1-token); LARQL's clean results are single-token. Confirms our multi-token question is real and unsolved upstream.

## 3. Convergent corroboration (strengthens, doesn't fill)
- **Per-relation capacity ceiling ~"a dozen facts/relation"** from *geometry* (`the-mechanism`: `unique_part()` runs out of near-orthogonal entity directions in d_model) → a **scaling prediction** (wider d_model / more heads = higher cap) that rhymes with our concentration-law (D1) + D20 compaction findings. LARQL's COMPOSE ~5–10/layer cap is the same wall.
- **`frozen_ffn_retrain_attention`** (`tiny-model` Phase 3) + **"attention routes, FFN computes"** (`transformer-by-hand`) = two independent arguments that FFN=store / attention=router is *trainable*, not just hand-constructible — underwrites our edit-FFN/leave-attention strategy. Band-labelling **L14–27="knowledge"** matches our late/mid-band editing.

## 4. Borrowable instruments (for CP2 + eval rigor)
- `chuk-kv-anatomist`: **`kv_inject_test`** (replace attention at one position with one V-direction × coeff; **KL<0.001 = "fact is one direction"**) + **`is_one_dimensional`** rank-of-fact metric → an independent **locality read** we could run on our edited models. ⚠ *Capture the distinction:* his store is **cache/activation-side** (boundary residuals, KV directions); ours is **in-weight** — are these the same fact in two coordinate systems?
- `verifiers` + `virtual-experts` + `structured-outputs` → a **3-way read-contract decomposition** for CP2: **typed form** (schema-constrain the response, `model_json_schema()`→validate-or-reject) + **verified content** (deterministic gold-answer/trace verifiers; isolate the soft LLM-judge) + **routed retrieval**; plus **graduated/decomposed reward** (localizes the *failed stage*: parse/route/exec/content) and an **anti-shortcut/provenance invariant** (a read must not return a value that was only ingested, never derived).

## 5. Serve/format facts captured (reference)
`.vindex` = a frozen-base dir of split weight files (`gate_vectors.bin` **IS** W_gate / KNN index; `down_weights.bin` = bake target; `embeddings.bin`, `down_meta.bin`, …; 3 extract levels Browse/Inference/All; "no data stored twice"). `.vlp` = JSON overlay (`PatchOp`: Insert/Update/Delete/InsertKnn/DeleteKnn; COMPOSE insert stores gate+up+down b64 f32). **APPLY** stacks last-wins; **COMPILE INTO VINDEX** hard-links unchanged files (APFS, free) + column-rewrites down (not gate). `ON CONFLICT {LAST_WINS|HIGHEST_CONFIDENCE|FAIL}` (HIGHEST_CONFIDENCE currently == LAST_WINS for down). CPU first-class (BLAS + ARM Q4 kernels); Metal-only GPU. `larql serve` (HTTP/gRPC, per-session patches), `USE REMOTE` (mutations create a *local* overlay). Future-but-proven: cross-model DIFF (Procrustes), `STEER/CHAIN/LIFT`, **residual-trace context store** (511–3100× vs KV cache). MLX (`chuk-finetune`/`mlx-finetune-record`): Qwen2.5-3B/7B via `mlx_lm`; **edit-survives-MLX-convert+quantize is UNRUN** (the Apple-silicon twin of our GGUF Q4_K result).

---

## 6. Fence, calibration, and a memory correction
- **Fence:** everything here = **LEADS → hypothesis register, never `CORPUS/` evidence.** The load-bearing four (L1–L4) bear on live decisions but must be **verified on our stack (Qwen, our harness)** before any promotion.
- **Calibration:** high confidence on *what his code says*; his empirical results are Gemma-4B / single-seed / small-n / Apple-MLX-bf16 (no Q4_K test in `the-mechanism`), and not independently reproducible without his private stack.
- **⚠ Memory correction needed:** `[[larql-the-mechanism-prior-art]]` currently claims "our same-entity-locality work fills its gap." This deep-read shows LARQL **already implements** a tiered KNN→COMPOSE→MEMIT hybrid + a `REBALANCE` fixed-point — so the "we fill its gap" framing is now **partly inverted** (he has mechanisms we theorized). That note should be revised. *(Not edited here — pending operator sign-off, since it's a canonical-memory correction.)*

## 7. Source repos read (Tier-1)
`larql` (1063★, Rust, Apache-2.0) · `the-mechanism` (9★, Python, **no license**) · `chuk-kv-anatomist` (8★, TS) · `tiny-model` (2★, Python, MIT) · `transformer-by-hand` · `mha_gqa_benchmark` · `chuk-model` · `activation_functions` · `chuk-finetune` · `mlx-finetune-record` · `chuk-mlx-2` · `virtual-experts` (6★, **no license**) · `verifiers` (23★, **no license**) · `structured-outputs` (6★, **no license**). (Tier-2 agent/MCP repos + Tier-3 off-domain not read; see the repo enumeration in chat.)

---

_Document type: process/reference (prior-art gap-map; no experiment D-ID; not subject to `closeout_check`). Captured 2026-06-23. Genuine gaps → `HYPOTHESIS_REGISTER §K`; load-bearing four → `EXPERIMENT_RUNBOOK §0.3` flag._
