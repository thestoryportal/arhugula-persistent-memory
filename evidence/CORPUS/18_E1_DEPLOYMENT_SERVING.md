# 18 — E1 / CPU DEPLOYMENT SERVING (LARQL ingest + the bias-ablation causal test)

_Result 2026-06-18. Track-E run, gated on a validated store (B3 `CORPUS/17`: the A1-clean batch store, quantized to real Q4_K_M). Pre-registered in `EXPERIMENT_RUNBOOK.md` §8 E1 ("parametric recall holds on CPU at Q4_K with acceptable tok/s"). Advisor-vetted framing (the "/" in the runbook E1 = **either** serving engine — a LARQL failure is NOT an E1 failure). Artifacts: `experiments/deployment/e1_probe.py`, `experiments/track_a/a7_bias_ablation.py`; results `results/e1_larql_serve_result.json`; logs `logs/e1_q4km_convert.log`, `logs/a7_bias_ablation.log`; store `b3_q4km.vindex` (13 GB, LARQL vindex from `gguf-to-vindex`). Engine UNMODIFIED; LARQL UNMODIFIED. Decision: **D-E1-1 ⟨D-E1-1@55708623⟩**._

## The question
The end product must serve the edited store on CPU (Intel target; [[deployment-target-intel-cpu]]). B3 showed Q4_K_M quantization preserves the edits and `llama.cpp` serves them on CPU. E1 asks the spec's actual question: does **LARQL's `gguf-to-vindex` ingest + serve** — the "LLM-as-Database" serving substrate — deliver correct parametric recall on CPU at acceptable throughput? Split into two claims, labeled BEFORE the run (advisor-mandated, [[resolve-the-gates-real-criterion]]):
- **Claim A — the deployment loop closes on CPU** (correct recall + acceptable tok/s).
- **Claim B — LARQL is the serving substrate** (`gguf-to-vindex` serves it). This is the genuinely-new test.

## Design (advisor-vetted)
- **Store:** the B3 A1-clean batch-edited Qwen2.5-3B, quantized Q4_K_M (`b3_edited_q4km.gguf`).
- **LARQL path:** `larql convert gguf-to-vindex --level inference` → vindex; serve via `larql lql 'USE …; INFER "<prompt>" TOP k'` (single load, no per-prompt reload). Validity gate FIRST: serve un-edited **native** facts → if garbage, that is the finding (the known Qwen2.5 attention-bias extraction bug), not an E1 failure. Then probe the edited facts; tok/s via `larql bench`.
- **De-confounding (added after the result, on operator challenge):** six hypotheses (H1–H6) for why the negative result could be skewed, tested against existing artifacts; then **A7**, a causal ablation in the reference model.

## VERDICT — Claim A PASS (llama.cpp) · Claim B FALSIFIED (LARQL, Qwen2.5)

| measure | value |
|---|---|
| **Claim A — CPU serving correctness** | **PASS** via llama.cpp + Q4_K_M GGUF (B3): edited retention 100% (99/99) vs native 97.4% (75/77), `-ngl 0` CPU |
| **Claim A — throughput (pod CPU proxy)** | **~8–13 tok/s** prompt-eval (forward ~80–126 ms/token) on Q4_K_M 3B; Intel-CPU confirmation deferred |
| **Claim B — LARQL `gguf-to-vindex` serves Qwen2.5-3B** | **FALSIFIED** — two extraction defects (below) → garbage output |
| LARQL compile cost | ~1 h CPU decompile for a 3B (`--level inference`); CPU-ONLY (no CUDA backend; see caveats) |

**Two LARQL extraction defects (both confirmed in the vindex):**
1. **Vocab mismatch → load failure.** `index.json` records `vocab_size 151643`, but `lm_head.weight`/`embeddings` tensors are **151936** (Qwen2.5's padded vocab; HF config confirms 151936) → `ShapeError/IncompatibleShape` on weight load. No-code workaround: set config `vocab_size→151936` → then it loads.
2. **Attention biases dropped → garbage.** `weight_manifest.json` has **0 bias entries** (the GGUF's 108 q/k/v biases dropped at extraction). After the vocab fix, serving is token salad ("Algeria language → *iros*", systematic across 4 prompts). = the known Qwen2.5 missing-bias extraction bug (`LARQL_INTEGRATION_ASSESSMENT`), now confirmed for `gguf-to-vindex`.

## A7 — the causal test (does the bias-drop CAUSE the garbage?)
Zeroed the 108 q/k/v attention biases in HF Qwen2.5-3B (the edited model) and re-probed the exact prompts LARQL garbled:

| condition | Algeria-lang | Japan-cap | water | France-cap (edited) |
|---|---|---|---|---|
| **with bias** (reference) | Arabic ✓ | Tokyo ✓ | oxygen ✓ | **Oslo** ✓ (edit served) |
| **bias zeroed** | 摅 | ZA | "() | ZA |

**Zeroing attention bias alone destroys factual recall → garbage.** This upgrades the attribution from correlation to a **proven sufficient cause**: LARQL dropping the biases is sufficient to explain the garbage. **Open (not resolved):** the bias-zeroed garbage does NOT token-match LARQL's (0/4) — consistent with EITHER a second decompile/dequant defect OR (more likely) chaotic implementation-sensitivity of broken-attention output. Does not move the verdict (bias-drop is sufficient and present).

## De-confounding ledger (H1–H6, on operator challenge — all addressed)
- **H1 (Q4_K dequant, not bias): COLLAPSED** — the Qwen2.5-**0.5B** vindexes (made via `safetensors-to-vindex`, NO quant, both `--level all` and `--level inference`) ALSO have 0 bias entries. Bias-drop is path- and quant-independent.
- **H3 (my vocab edit corrupts): COLLAPSED** — HF config vocab IS 151936; the edit is correct.
- **H4 (level inference vs all): COLLAPSED** — `--level all` 0.5B also drops bias.
- **H5 (toolchain broken now): COLLAPSED** — a Qwen3 vindex serves cleanly NOW (France→Berlin 99.43%, walk-FFN).
- **H6 (n=1): COLLAPSED** — systematic garbage across 4 prompts.
- **H2 (attribution): SUPPORTED & now causal** via A7.

## Scope & caveats (kept flush)
- **LARQL is CPU-ONLY on this NVIDIA pod.** Its only compute backends are CPU + Apple **Metal**; CUDA is an unimplemented "future" backend (binary links OpenBLAS, zero CUDA symbols; the convert ran at 0 MiB GPU). The "compile offline on GPU" deployment idea must mean Apple-Metal or cheap offline CPU — **not** an NVIDIA GPU. (The GPU usage in prior decouple tests was OUR PyTorch edit/cov step, not LARQL.)
- **Did NOT serve a fresh non-quantized Qwen2.5-3B vindex** (used the existing 0.5B non-quant as the de-confound — near-certainly redundant given both show 0-bias+garbage, but not the identical model). A ~1 h `safetensors-to-vindex` run would make it airtight.
- **Did NOT debug LARQL's Rust** (per the T2.4 advisor: avoid unbounded Path-A debugging of someone else's unvalidated path). No no-code bias injection exists (attention bias is not foldable into weights; `.vlp` has no bias slot).
- LARQL serving is viable on **bias-free architectures** — demonstrated in-weight on CPU at **Qwen3-0.6B** (T2.4 decouple: France→Berlin 99.43% via walk-FFN). The Qwen2.5 family (which our edit-science A1/B3 validated) is the immature path.
- Throughput is a **pod-CPU proxy**, not the operator Intel CPU (G5/D1).

## Decision
**D-E1-1:** The **CPU deployment loop is CLOSED via `llama.cpp` + Q4_K_M GGUF** (Claim A PASS). **LARQL `gguf-to-vindex` is NOT a viable serving substrate for the Qwen2.5 family** (Claim B FALSIFIED — LARQL-side bias-drop, causally proven, not a fault of the store). **Spec implication = a MODEL-FAMILY SPLIT:** the edit-validated family (Qwen2.5) and the LARQL-servable family (Qwen3, bias-free) currently differ. Resolutions (logged, not chosen here): (a) serve Qwen2.5 via llama.cpp and forgo the LARQL query layer; (b) port the edit-science to Qwen3; (c) build the database query layer ourselves over any served model (G3 prototyped this) — decoupling the DB layer from LARQL. See `docs/HYPOTHESIS_REGISTER_2026-06-18.md` B2/B3/C1.

## FORK
PASS-A / FAIL-B → CPU serving works (llama.cpp); LARQL-as-substrate is bias-architecture-gated. The "LLM-as-Database" *serving* half is demonstrated; the *database-query* half stays open (CP2: LARQL triple-readback absent regardless). Next live falsifiers: **B1** (done, `CORPUS/19`), **C2/keying** (done, `CORPUS/20`), **the B3/E3 L2-necessity decision** (is in-weight even required, or does L1-retrieval + external index suffice?), **D1** (capacity law, required for F1).
