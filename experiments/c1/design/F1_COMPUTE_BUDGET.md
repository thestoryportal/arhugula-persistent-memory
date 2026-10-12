# F1 — Compute Budget for the Remaining Conditions Register

**Date:** 2026-06-26 · **Owner artifact for:** "what does it cost to run the remaining spec experiments?"
**Source of truth for the conditions:** `docs/F1_DETERMINATION.md` §3 (the C1–C10 register) + §4 (closure path).
**Status:** advisor-checked framing; numbers are ENGINEERING ESTIMATES (anchored to logged run times), not measured budgets.

---

## 0. The premise correction (read first)

**There is no GPU spend that "closes" the spec.** The F1 determination is CONCLUDED as
**NOT-READY-WITH-CONDITIONS** and §5 states explicitly that *no single solo action flips that verdict* —
the falsification frontier for the 3B / AlphaEdit / single-token-real-knowledge regime is reached.

So a single "GPU-hours to closure" figure would answer a flattering *adjacent* question
([[resolve-the-gates-real-criterion]]). The real answer is two-part:

1. The GPU-runnable remainder is **trivially cheap — tens of dollars** (a 4090 is $0.34–0.59/hr).
2. **GPU cost was never the binding constraint.** What gates closure is *substrate availability* (C1),
   *multi-day engineering* (C2/C5/C6/C7 + the AnyEdit port), and *operator scope decisions* (regime change
   vs. accept-as-bounded). None of those move on a GPU budget.

---

## 1. Cost anchors (from the logged record)

| Quantity | Anchor | Source |
|---|---|---|
| 3B edit + held-out probe run (band[4-8], N≤100) | ~20–50 min | runbook §8 (Track C/D); `docs/C10_RESIDUAL_TEST_PREREG.md` |
| Covariance recompute (if uncached) | ~20 min/process; ~11–17 min/layer × 5 ≈ 70 min fresh band | `CORPUS/04_ENV_AND_DEPS.md`; `CORPUS/36` |
| N=2,000 single-joint-solve run | **62 min, 8.4 GB VRAM** | `docs/C1_TRUESCALE_SUBSTRATE_DIAGNOSTIC.md` (D-C1TS-1) |
| Q4_K_M GGUF build + ingest | ~10–20 min | `docs/G6_G7_PASS_CRITERIA_DRAFT.md` |
| 7B edit run (5-layer band) | ~2–4 h | runbook §8 model table; `docs/cross_architecture_axis_scoping_note.md` |
| Hardware | single RunPod **RTX 4090 (24 GB)**, serialized by information value | runbook §6; `docs/REGROUNDING_PLAN_v2.md` |
| Price | **$0.34/hr Community · $0.59/hr Secure** (per-second billing) | runpod.io/pricing (2026-03) |

The single 4090 serializes all heavy GPU runs — these are wall-clock-additive, not parallel.

---

## 2. The three buckets

### Bucket 1 — GPU-runnable falsifier legs (estimable, cheap)
On the existing Qwen2.5-3B / band[4-8] / AlphaEdit recipe.

| Cond | Remaining work | Est. GPU-h | Locality |
|---|---|---|---|
| **C3** | R5 native-firing scale + Q4_K_M firing curve + powered diversity-vs-intensity run | ~7–15 | **GPU-edit-bound** (edit step); Q4_K_M serve/probe legs run local CPU |
| **C8** | R15-v2 adversarial constraint-firing (relational pairs + frozen-judge oracle) | ~3–6 | **GPU-edit-bound** (edits); adversarial probing of an edited model = local CPU |
| **C9** | R9 hard case — redact a *native/distributed* fact; residue + collateral + delete-time L2 probe | ~3–6 | **GPU-edit-bound** (deletion-edit); residue/collateral probes = local CPU |
| **C10** | AnyEdit/per-token pilot after code-level viability gate (A7 + A1/A2; held-out full-seq) | ~5–10 | **GPU-edit-bound validation** after local CPU port authoring; no upstream-as-is run |

**Subtotal: ~18–37 GPU-h → ~$6–22.** Locality split: the **edit (MEMIT/AlphaEdit solve) stays on the 4090**; the **read/serve/probe half of each leg is local-CPU-runnable** against the shipped edited model.

### Bucket 2 — C4 is the fat tail (one heavy, uncertain GPU item)
**C4 (7B numeric transfer of the §8.7 concentration threshold, OQ-W1).** Dominates the total and is
*gated on a determinism instrument that is not yet built*. Per
[[clustered-design-power-determinism-cheaper-lever]], at the realized ~50pp run-to-run swing, detecting a
~20pp effect needs ≳15 clusters/arm:

- **If determinism cuts the swing:** ~20–40 GPU-h → ~$7–24
- **If it does not:** ~60–120 GPU-h → ~$20–70

Present C4 as "the one heavy, uncertain GPU item, gated on prior instrument work" — **not** a tidy point estimate.

### Bucket 3 — Not GPU-runnable / not a GPU question

| Item | Status / GPU | Locality |
|---|---|---|
| **C1** compaction self-heal at true scale | **SUBSTRATE-CEILING'd** (D-C1TS-1); $0 productive GPU — *blocked, not budgeted* (the 62-min/N=2,000 runs collapse the model: ΔW blow-up, all-`!` output → not valid datapoints) | N/A (not runnable anywhere) |
| **C2** index/query layer build (SELECT read-back, 5 families, aggregation) | Phase-2 BUILD; negligible GPU | ✅ **Local CPU** — index build is software; reads run against an already-edited model on CPU |
| **C5** governance/orchestration (2PC, ledger, TC, circuit-breaker, fault-injection) | Phase-2 BUILD; **no GPU** | ✅ **Local CPU today** — G1/G3 scripts are torch-free pure Python |
| **C6** security red-team (Ed25519, Gate/token forgery, ledger-immutability, STH anchor) | Phase-2 red-team; **no GPU** | ✅ **Local CPU today** — G2 is torch-free crypto/systems |
| **C7** pruning/GC orchestration (Pruning Agent 2PC, staleness backpressure, reconciliation queue) | Phase-2 BUILD; negligible GPU | ✅ **Local CPU** (logic) — only the deletion-*edit* step is GPU-bound |
| **AnyEdit port** (C10 option A) | multi-day **human labor** plus a hard code-level viability gate; eval +~5–10 GPU-h if the gate passes | ◐ **Port authoring local CPU**; **validation runs GPU-edit-bound**. Advisor-review says PROCEED only after verifying the official AnyEdit per-token/window loop can be transplanted onto local Qwen2.5-3B / `transformers==4.51.0` without replacing science-path MEMIT primitives or breaking LAW#5. FABLE is fallback; AnyEdit++ is paper-only risk note. |

---

## 2b. The locality principle — edit vs. inference

The boundary is **not** "GPU vs CPU science" — it is **"does this step edit weights or not."** Verified at the
code level: `g1_two_phase_commit.py` / `g2_security_layer.py` / `g3_validation_pipeline.py` import **no torch**
(pure governance/crypto/validation machinery reusing a pre-existing overlay); only `cp1_governed_write.py` loads
the model, because it wraps an actual MEMIT *write*. This matches the fixed deployment split
([[deployment-target-intel-cpu]]: **edit-time = GPU/offline, inference-time = CPU**).

**Workflow:** edit on the 4090 → ship the edited model (or the **Q4_K_M GGUF, ~2 GB**) to the local Intel
machine → run all governance / security / index / read-contract / serve-validation science there. Moving the
**read/serve validation local is not just allowed — it closes the open `real-Intel-CPU serving validation` gap**
(E1 was only a pod-CPU proxy). The only thing that *must* stay on the GPU is producing new edited-weight
artifacts (the float64 MEMIT/AlphaEdit solve + covariance).

**Local-env requirements (operator's machine: 2 GHz quad-core Intel i5, 16 GB LPDDR4X — a 2020-class Intel
MacBook):**
- **Governance / security / index (C2/C5/C6/C7)** — Python only (no CUDA, no torch). Trivial on this machine.
- **Read / serve / probe** — **recommend the Q4_K_M GGUF + llama.cpp path** (~2 GB resident), NOT CPU
  `transformers` fp16. Rationale: 3B fp16 is ~6 GB weights + KV-cache/activations/Python overhead → ~8–10 GB
  resident, which on a 16 GB machine shared with macOS is tight and risks swapping; the Q4_K_M GGUF is ~2 GB and
  fits with wide headroom. It is also the **actual deployment artifact** (B3 proved it serves edits 100% on CPU),
  so testing on it tests the real target, not a proxy. Expect slow-but-correct inference on 4 cores — which is
  the point, since this CPU substrate *is* the deployment target.

---

## 3. Bottom line

| Scope | GPU-h | Cost (4090 @ $0.34–0.59/hr) |
|---|---|---|
| Bucket 1 (3B falsifier legs + viability-gated C10 pilot) | ~18–37 | ~$6–22 |
| + C4 typical (determinism cuts swing) | ~35–70 total | ~$12–40 |
| + C4 worst case (swing uncut) | ~75–150 total | ~$25–90 |
| C1 true-scale | — | **blocked (substrate ceiling)** |
| C2 / C5 / C6 / C7 / AnyEdit port | ~negligible GPU | multi-day **engineering**, not GPU |

**Headline:** even the worst case is **under ~$100**. The dollar figure is the non-story. Spec closure is gated
by the **C1 substrate ceiling**, the **multi-day AnyEdit port + Phase-2 governance/index/security/pruning BUILD**,
and **operator scope decisions** (regime change vs. accept-as-bounded) — none of which a GPU budget can buy down.

---

## 4. Caveats

- Estimates are anchored to logged single-run times; they do **not** include re-runs for GPU nondeterminism
  (held-out corruption swings ~50pp run-to-run on the same config — see [[sequential-edit-run-nondeterminism]]),
  which is exactly why C4 needs the determinism instrument first.
- All Bucket-1/2 figures assume cached covariance for the existing 3B band[4-8]; new bands/models add ~20–70 min
  cov each.
- Within standing infra auth ([[standing-auth-forward-requirements]]); a *wide* C3/C4 grid breadth is a one-line
  scope call for the operator, not a hidden cost.
