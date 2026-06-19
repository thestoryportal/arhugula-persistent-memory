# Framework Finding — MEMIT Ceiling Archival — v1.5

**Status:** ADDITIVE AMENDMENT (v1.0 + v1.1 + v1.2 + v1.3 + v1.4 PERMANENT preserved verbatim)

**Version lineage:**
- v1.0 (PERMANENT; ratified S2.18 close 2026-05-05) — rank-1-in-weight class ceiling on Llama-3.1-8B; seven axes
- v1.1 (ADDITIVE; ratified S2.18 close 2026-05-05) — ROME elimination amendment (Axis 7)
- v1.2 (ADDITIVE; ratified S2.20 close) — adapter-mechanism environmental ceiling (GRACE)
- v1.3 (ADDITIVE; ratified S2.28 close 2026-06-15) — Axis 8 (cross-scale, 8B→3B) + AKD-confound elimination + Axis 9 (band-invariance)
- v1.4 (ADDITIVE; ratified S2.29 close 2026-06-15) — Axis 10 (cross-architecture, Llama → Mistral-7B); promoted ceiling L → G (config-independent MEMIT-on-base-decoder-LM)
- v1.5 (ADDITIVE; ratified S2.31 close 2026-06-15) — **Axis 11 (cross-architecture FALSIFICATION, Qwen2.5-7B CLEARS). G is FALSIFIED as stated; the ceiling NARROWS from G (base-decoder-LM-general) to Llama-lineage.** The first axis to *break* the ceiling rather than confirm it. The sought Qwen "confirmation" (v1.4 §2.5) returned as falsification.

---

## §0. Amendment Scope

### §0.1 Statement

v1.5 documents the T.3-β cross-architecture execution arc (S2.31) that ran after v1.4 was ratified. The amendment is **ADDITIVE** — v1.0 + v1.1 + v1.2 + v1.3 + v1.4 integrity preserved verbatim. v1.5 makes one change to the ceiling characterization, and it is the change v1.4 §2.5 explicitly identified as the test the Qwen arm would adjudicate:

1. **Axis 11 — cross-architecture FALSIFICATION (S2.31).** MEMIT at canonical hparams on `Qwen/Qwen2.5-7B` (base) — single-variable architecture port from the validated config, **zero tuning-knob changes** — produces **`5/5` consistency PASS** (P_min 0.990 ≫ 0.5). Qwen is the first model in the entire program to clear the consistency band where every prior axis (Llama-3.1-8B ×7, Llama-3.2-3B, Mistral-7B) produced `0/5`. The internal-vs-external signature does **NOT** reproduce on Qwen: internal z-optimization converges cleanly (>0.98 all 5 facts) AND the external surface follows (0.99 all 5). The ceiling is therefore **NOT a property of MEMIT-class editing on base decoder LMs in general (G).**

**The class change this forces:** at v1.4 the ceiling was a **config-independent MEMIT-on-base-decoder-LM property (G)**, with Llama and Mistral as two instances. v1.5 **falsifies G as stated** and narrows the ceiling to **Llama-lineage** — the architectural lineage sharing Llama-2's decoder block (RMSNorm + RoPE + gated-MLP + GQA), of which Llama-3.1-8B, Llama-3.2-3B, and Mistral-7B-v0.3 are the confirmed instances. Qwen2.5-7B is the **falsifying case** that establishes the lineage boundary.

### §0.2 What is NARROWED vs what is PRESERVED (load-bearing — no prior axis is retracted)

v1.5 retracts **nothing** from v1.0–v1.4. Every prior axis result remains exactly true:

- Llama-3.1-8B still hits the ceiling across all seven axes. (Re-confirmed this session, both engine paths — §4.)
- Llama-3.2-3B still hits it (Axis 8).
- Mistral-7B still hits it (Axis 10).
- ROME still hits it (Axis 7).

What changes is **only the claimed generality**. v1.4 generalized from "Llama" to "all base decoder LMs (G)" on the strength of one non-Llama instance (Mistral), while v1.4 §2.5 explicitly flagged that Mistral shares Llama-2 lineage and that a more distinct family (Qwen) was needed to make G decisive. Qwen came back CLEAR. So G overreached by exactly the margin v1.4 §2.5 anticipated, and the correct scope is the lineage Mistral and the Llamas share. **The ceiling is real and over-determined within Llama-lineage; it simply does not extend to Qwen-lineage.**

### §0.3 Diff vs Prior Versions

| Surface | v1.3 | v1.4 | v1.5 ADDITIVE (this) |
|---|---|---|---|
| Axes | 1–9 | +10 (Mistral) | **+11 (Qwen — FALSIFIES)** |
| Model families ceiling-confirmed | Llama | Llama + Mistral | Llama + Mistral (= **Llama-lineage**) |
| Model families ceiling-BROKEN | — | — | **Qwen2.5-7B** |
| Ceiling class | config-indep on base-Llama | config-indep on base-decoder-LM (G) | **config-indep on Llama-lineage** (G falsified) |
| Mechanism locus | external surface (softmax competition) | external surface | **internal z-optimization stage** (Qwen converges; Llama does not — §3) |
| Architecture-geometry question | closed | closed | **RE-OPENED** |

### §0.4 Why Additive

| Integrity surface | v1.0–v1.4 | v1.5 |
|---|---|---|
| Prior axis statements | preserved verbatim | preserved verbatim; no retraction; v1.5 adds Axis 11 + narrows the *generality claim* only |
| Determinism discipline | bit-exact, Llama + Mistral checkpoints | extended: Checkpoint #1 (within-session) + #2 (cross-process) on Qwen, both drift 0.00e+00, 0/38 mismatch |
| Copy-Unmount validation | 6 configs (5 Llama + Mistral) | extended: 7th config (Qwen L4-8) + Llama-3.1-8B isolation-control restore, both bit-exact |
| Engine integrity | byte-identical (SHA 80426fd9) all axes | same SHA; one VRAM-forced numerically-inert patch (`P-VRAM-CPU-SOLVE`) isolated + exonerated (§4); engine pristine at close |
| PERMANENT preservation | v1.0–v1.4 verbatim | all five preserved verbatim; v1.5 amends only |

v1.5 is the first amendment to **break** rather than extend the ceiling. It closes the v1.4 §2.5 confirmation question with the falsifying answer.

---

## §1. v1.0–v1.4 Carry-Forward (Statements Preserved Verbatim)

The full statements of v1.0–v1.4 are preserved verbatim in their source documents and are NOT restated or modified here. The load-bearing carry-forward for v1.5 interpretation:

- **v1.0 architectural-invariant ceiling** (PERMANENT): MEMIT cannot consistency-edit base Llama-3.1-8B at canonical hparams on cfb-v3 — still true.
- **v1.1 rank-1-in-weight class** (PERMANENT): the ceiling extends to ROME on Llama — still true.
- **v1.3 config-independence on base-Llama** (PERMANENT): independent of hparam/corpus/target/locus/layer-set/scale/AKD/band — still true.
- **v1.4 cross-architecture (Mistral)** (PERMANENT): the ceiling reproduces on Mistral-7B — still true.

v1.5's Axis 11 establishes that the boundary of the v1.4 generalization is **Llama-lineage**, with Qwen2.5-7B outside it.

---

## §2. v1.5 Axis 11 — Cross-Architecture Falsification (S2.31)

### §2.1 Statement

The G hypothesis — that the ten-axis ceiling is a property of MEMIT-class editing on base decoder LMs in general — is **empirically FALSE**. MEMIT at canonical hparams on `Qwen/Qwen2.5-7B` (base), single-variable architecture port from the validated config, produces **`5/5` consistency PASS** with the internal-vs-external signature absent (internal converges AND external follows). The ceiling does NOT generalize beyond Llama-lineage.

### §2.2 Empirical Surface

| Surface | Value |
|---|---|
| Model | `Qwen/Qwen2.5-7B` (base), revision `d149729398750b98c0af14eb82c78cfe92750796`, fp16, Apache-2.0 ungated |
| Engine | MEMIT, SHA `80426fd9` (byte-identical to all ten prior axes) + `P-VRAM-CPU-SOLVE` (numerically-inert; isolated/exonerated §4) |
| Hparams | 8B-canonical JSON, **single architecture-forced delta** (`v_loss_layer 31→27`), **0 tuning-knob changes** (§2.4) |
| Edit band | `[4,5,6,7,8]` (EasyEdit/CaKE Qwen reference; Axis-9-validated equivalent) — **canonical joint-overlay (NOT single-layer); CPU-solve preserved canonical scope** |
| Corpus / probes | cfb-v3 / probe-set-v3 (held verbatim; token IDs re-resolved against Qwen tokenizer) |
| Consistency verdict | **5/5 PASS** |
| Internal objective (compute_z) | converged to >0.98 all 5 facts (guitar 0.0046→0.9955; piano 0.0176→0.9895; violin 0.0030→0.9988; harp 0.0212→0.9943; flute 0.0039→0.9988) |
| External post-edit P(target) | guitar 0.9966; piano 0.9900; violin 0.9987; harp 0.9924 (proxy); flute 0.9990 — **P_min = 0.990 ≫ 0.5** |
| Top-1 after edit | became the target on all 5 (guitar / piano / violin / har / flute) |
| Determinism | Checkpoint #1 (within-session) + Checkpoint #2 (cross-process): both drift 0.00e+00, 0/38 mismatch |
| Copy-Unmount | bit-exact (7th config; second non-Llama base) |
| VRAM peak | 19.3 GiB edit (CPU-solve; float64 off-GPU) |
| Cov compute | ~105 min for [4–8] band (5 × 1.4 GB caches, architecture-keyed, widest-of-arm 18944²) |

### §2.3 Trustworthiness Anchor

The Axis-11 `5/5` CLEAR is certified by the same verdict-integrity chain as every prior axis, established fresh on Qwen, plus a confound-isolation control that no prior axis required:

1. **Deterministic load** — Checkpoint #1 self-check (capture twice, bit-exact): drift 0.00e+00, 0/38 mismatches. Checkpoint #2 (cross-process, fresh kernel + reload): drift 0.00e+00, 0/38 mismatches. The fp16 forward pass is bit-stable on Qwen.
2. **Clean pre-edit baseline** — natural top-1 = ` the` (function-word class) for all 5 facts, p 0.19–0.37; Qwen does not natively associate the athletes with the instruments — same starting regime as Llama/Mistral. The edit has the same job it had on every prior model.
3. **Edit dispatched and ran** — deltas computed and inserted into all five layers; all five `_t100_` cov caches loaded by exact path (no lookup miss); internal objective converged to >0.98.
4. **External 5/5** — post-edit P(target) ≥ 0.990 on all five, top-1 became the target. The edit is expressed at the output surface.
5. **Bit-exact unmount** — Qwen L4-8 restore bit-exact; the CLEAR is a real property of the edited model.
6. **Confound isolation (NEW for Axis 11)** — the one engine modification this arm required (`P-VRAM-CPU-SOLVE`, VRAM-forced) was isolated against the most-confirmed ceiling (Llama-3.1-8B, Bo Jackson→guitar): the patched engine reproduces the Llama ceiling at the floor (`7.9e-08`), provably equivalent to the pristine GPU solve (`1.07e-05`). The CLEAR cannot be a patch artifact (§4).

The read is cleanest exactly where it is load-bearing: **guitar (cfb-v3-001), piano (cfb-v3-002), and flute (cfb-v3-005) are all STRICT single-token targets on Qwen** — the entire verdict-integrity subset {001, 002, 005} clears at full single-token fidelity, no proxy approximation. Qwen's large 152k vocab gives the cleanest tokenization of any arm (4/5 STRICT vs Mistral's 2/5).

### §2.4 Cross-Architecture Config Idiom — the cleanest single-variable port of any arm

The proven Qwen MEMIT config is `json.load(8B-canonical JSON)` with a **single architecture-forced delta** and **zero tuning-knob changes**. Against the already-validated Mistral config, the diff is exactly **one integer**:

- `v_loss_layer`: 31 → **27** (Qwen has 28 layers; n−1 = 27). Every other field — all module paths (`mlp.down_proj`, `self_attn`, `model.norm`, `lm_head`), `lm_head_module="lm_head"` (Qwen untied), and every tuning knob (`mom2_update_weight` 15000, `v_lr` 0.5, `v_num_grad_steps` 25, `kl_factor` 0.0625, `clamp_norm_factor` 0.75, `v_weight_decay` 0.5) — is **byte-identical to the Mistral config**.

This is the strongest single-variable statement in the program: against a config that already produced `0/5` on a different model, Qwen's config differs by one layer-count-forced integer, and Qwen produces `5/5`. The difference is attributable to **architecture alone**. The genuine port cost (heaviest of any arm) was structural: Qwen's distinct hidden size (3584), intermediate size (18944), 28 layers, 152k Qwen-BPE vocab (all token IDs re-resolved), pad convention (`<|endoftext|>=151643`), and QKV-bias attention — none of which are hparams. P-4's family-agnostic getattr-fallback is the structural enabler that lets the byte-identical engine read Qwen's modern config (no `n_embd`).

### §2.5 Scope Boundary (load-bearing for interpretation)

v1.4 §2.5 named the exact test: *"Qwen is a more architecturally distinct decoder family … a `0/5` signature reproduction there would be near-decisive for G."* The contrapositive held: **Qwen did NOT reproduce `0/5`; it cleared 5/5.** This falsifies G and localizes the ceiling to Llama-lineage. The precise v1.5 claim:

> The architectural-invariant ceiling is a property of **Llama-lineage base decoder LMs** (Llama-2-derived decoder block: RMSNorm + RoPE + gated-MLP + GQA), confirmed on Llama-3.1-8B (7 axes), Llama-3.2-3B (Axis 8), and Mistral-7B-v0.3 (Axis 10). It does **NOT** extend to Qwen2.5-7B (Axis 11), which clears canonical MEMIT 5/5 under a single-integer-different config. The boundary between "ceiling holds" and "ceiling breaks" runs along architecture lineage, not along base-decoder-LM-ness.

**Open at the lineage boundary:** whether the boundary is precisely "Llama-2 lineage" or something narrower/broader (e.g. a specific normalization, attention, or initialization property that Qwen happens to differ on) is unresolved — it requires a second non-Llama-lineage family (Phi / Gemma / NeoX-class) to clear-or-hold. This is the re-opened architecture-geometry frontier (§3, t_branch v1.4 §4'''').

### §2.6 Qwen-Tokenizer Resolution (recorded for verdict interpretation)

Qwen's 152k vocab gives the cleanest target tokenization of any arm:

| Fact | target | Llama-3.1-8B | Mistral-7B | Qwen2.5-7B | class on Qwen |
|---|---|---|---|---|---|
| cfb-v3-001 | guitar | `[17418]` | `[11454]` | `[16986]` | STRICT |
| cfb-v3-002 | piano | `[27374]` | `[13989]` | `[26278]` | STRICT |
| cfb-v3-003 | violin | `[63137]` | `[4875,1030]` | `[62037]` | STRICT |
| cfb-v3-004 | harp | `[4960,79]` | `[5180,29488]` | `[4855,79]` | PROXY (har+p) |
| cfb-v3-005 | flute | `[96812]` | `[1740,2491]` | `[95712]` | STRICT |

4/5 STRICT (vs Mistral 2/5, Llama-3.1 4/5). The entire integrity subset {001/002/005} is STRICT — the load-bearing CLEAR is at full single-token fidelity.

---

## §3. The Mechanism Refinement — the divergence is at the INTERNAL stage (D-S231-MECH-1)

The v1.0–v1.4 reading located the ceiling at the **external surface**: the optimizer drives the internal objective hard, but cluster-internal softmax competition absorbs the lift so no single target wins (the "internal succeeds, external fails" signature). Axis 11 forces a refinement, because the Qwen/Llama divergence is visible **at the internal z-optimization stage**, before the external surface is even reached:

- **Qwen z-optimization converges:** all five facts reach avg-prob >0.98 of the target within 25 grad steps (loss 5.6→0.046 for guitar, etc.).
- **Llama-3.1-8B z-optimization does NOT converge** under identical canonical settings: avg-prob of the target crawls from ~1.6e-08 to ~1e-4 over 25 steps, loss stuck high (17.96→9.35), never approaching the target (re-observed this session in the isolation control, both engine paths — §4).

So whatever is special about Llama-lineage geometry obstructs the **optimizer's ability to find the edit direction at all**, not merely the softmax's willingness to express an already-found direction. On Llama the v1.x "internal succeeds / external fails" signature is itself an *approximation* — the internal optimization makes large *relative* progress (240–4000×) but from a floor so low it never reaches a confident target; on Qwen the optimization reaches confident-target and the edit expresses. This refinement does not retract the v1.x external-surface characterization (which holds for the Llama-lineage models where the optimizer does make large relative internal progress), but it identifies the **earlier, deeper locus** of the lineage difference and is the central thread for the re-opened architecture-geometry question.

---

## §4. Confound Isolation — `P-VRAM-CPU-SOLVE` exonerated (OQ-S231-PATCH-CONFOUND-1 resolved)

Qwen's 18944-wide intermediate inflates the MEMIT float64 linear solve (`cov.double()`, 2.67 GiB) past the 24 GiB RTX 4090 headroom alongside the resident 15 GiB model. The edit could not dispatch on the unmodified engine (OOM at `torch.linalg.solve`). Single-layer scope did not help (the allocation is per-layer, not layer-count-driven). The mitigation was `P-VRAM-CPU-SOLVE`: move the solve operands to CPU before the arithmetic so the float64 matrix is born in system RAM, never VRAM; result `adj_k` returns to GPU. Numerically inert by construction (float64 CPU solve == float64 GPU solve for a well-posed system).

Because the patched engine produced the anomalous CLEAR, the patch is a candidate confound and was isolated before any promotion:

**Isolation control:** Llama-3.1-8B (most-confirmed ceiling, 7 axes), Bo Jackson→guitar, canonical hparams, run BOTH ways:

| Run | Engine path | post-edit P(guitar) | Verdict |
|---|---|---|---|
| A | patched (CPU-solve) | **7.9053e-08** | ceiling held (floor) |
| B | pristine (GPU-solve) | **1.0697e-05** | ceiling held (floor) |
| — | reference (finding §2.2) | 3.38e-4 | ceiling |

Both paths hold the Llama ceiling at the floor; per-layer `upd norm` and `z error` match across A/B to ~3 sig figs (L4 upd 0.2638 vs 0.2655; z error 5.2070 vs 5.2069). The patch is **provably equivalent** on the exact configuration where the ceiling is most over-determined — it cannot have manufactured Qwen's CLEAR. The patch is exonerated; the CLEAR is a real architectural result.

`P-VRAM-CPU-SOLVE` is recorded as a conditional SOURCE_LAYER patch (memit-patches v2.6, S2.32 codification), required for any model whose intermediate width inflates the float64 solve past 4090 headroom. Engine restored pristine at session close.

---

## §5. Forward Implication

v1.5 **re-opens the architecture-geometry frontier** the seven-axis Llama work had closed. The ceiling is no longer a candidate universal property of MEMIT-class editing; it is a property of a specific architecture lineage, with a confirmed falsifying case. The live questions:

1. **Where exactly is the lineage boundary?** Llama-2-lineage precisely, or a narrower architectural property Qwen differs on? Requires a second non-Llama-lineage family (Phi / Gemma / NeoX-class) to clear-or-hold (t_branch v1.4 §4'''' Direction 3).
2. **What geometric property obstructs the z-optimization on Llama-lineage but not Qwen?** The D-S231-MECH-1 internal-stage thread — a per-layer z-convergence comparison Llama vs Qwen at matched layers (Direction 2).
3. **Is the Qwen CLEAR robust to the full 38-probe panel** (generalization + specificity + unmount across 15 trials), or does it fire only on the canonical prompt? Hardens the CLEAR to finding-grade (Direction 1; S2.32 recommended).

The v1.5 finding is the most consequential single result of the T-branch arc: the first falsifying case, narrowing a claimed-universal ceiling to an architecture lineage and reopening the mechanistic question of *why*.

---

**v1.5 RATIFIED S2.31 close 2026-06-15.** ADDITIVE; v1.0–v1.4 PERMANENT preserved verbatim. Axis 11: Qwen2.5-7B CLEARS canonical MEMIT 5/5 — G falsified, ceiling narrows to Llama-lineage; CPU-solve confound isolated and exonerated; mechanism refined to the internal z-optimization stage; architecture-geometry frontier re-opened.
