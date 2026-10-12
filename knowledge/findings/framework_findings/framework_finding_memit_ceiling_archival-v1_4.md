# Framework Finding — MEMIT Ceiling Archival — v1.4

**Status:** ADDITIVE AMENDMENT (v1.0 + v1.1 + v1.2 + v1.3 PERMANENT preserved verbatim)

**Version lineage:**
- v1.0 (PERMANENT; ratified S2.18 close 2026-05-05) — rank-1-in-weight class ceiling on Llama-3.1-8B; seven axes
- v1.1 (ADDITIVE; ratified S2.18 close 2026-05-05) — ROME elimination amendment (Axis 7)
- v1.2 (ADDITIVE; ratified S2.20 close) — adapter-mechanism environmental ceiling (GRACE)
- v1.3 (ADDITIVE; ratified S2.28 close 2026-06-15) — Axis 8 (cross-scale, 8B→3B) + AKD-confound elimination + Axis 9 (band-invariance, [2–6] vs [4–8])
- v1.4 (ADDITIVE; ratified S2.29 close 2026-06-15) — **Axis 10 (cross-architecture, Llama → Mistral-7B)**. Promotes the ceiling from "config-independent MEMIT-on-**base-Llama** property" to "config-independent MEMIT-on-**base-decoder-LM** property" — the first axis to vary the base architecture **family**, and the only axis class that could change the *class* of the finding rather than add a same-class confirmation.

---

## §0. Amendment Scope

### §0.1 Statement

v1.4 documents the T.3-α cross-architecture execution arc (S2.29) that ran after v1.3 was ratified. The amendment is **ADDITIVE** — v1.0 + v1.1 + v1.2 + v1.3 integrity preserved verbatim. v1.4 makes one addition to the ceiling characterization, and it is the addition v1.3 §6 explicitly identified as the only remaining axis that could change the finding's *class*:

1. **Axis 10 — cross-architecture generalization (S2.29).** MEMIT at canonical hparams on `mistralai/Mistral-7B-v0.3` (base) produces `0/5` consistency with the identical internal-vs-external signature. The architectural-invariant ceiling is **NOT Llama-family-specific**; it reproduces on a non-Llama base decoder LM with a different pretraining corpus, a different tokenizer, and a different architecture family, at canonical hparams with **zero tuning-knob changes** (single-variable architecture port). This is the **first architecture-family-variation axis** (Axes 1–9 all held the base architecture family fixed at Llama, varying hparams / corpus / target / probe-locus / layer-set / write-engine / scale / layer-band).

The class change this licenses: at v1.3 the ceiling was a **config-independent MEMIT-on-base-Llama property** (L). v1.4 promotes it to a **config-independent MEMIT-on-base-decoder-LM property** (G), of which Llama and Mistral are two instances. This is the portable, framework-level result about the write layer that the entire T-branch arc was built to reach or refute.

### §0.2 Diff vs Prior Versions

| Surface | v1.0 PERMANENT | v1.1 ADDITIVE | v1.2 ADDITIVE | v1.3 ADDITIVE | v1.4 ADDITIVE (this) |
|---|---|---|---|---|---|
| Axes | 1–6 (Llama-3.1-8B, MEMIT) | +7 (ROME) | — (off-axis GRACE) | +8 (3B scale), +9 (band) | **+10 (Mistral architecture)** |
| Model family | Llama | Llama | Llama (GRACE env) | Llama (3B + 8B) | **Llama + Mistral** |
| Ceiling class | MEMIT-on-8B | + rank-1-in-weight class | adapter off-axis | config-independent on **base-Llama** | config-independent on **base-decoder-LM** |
| Strongest closed confound | hparam/corpus/target/locus/layer-set | write-engine swap | — | AKD + layer-band | **architecture family (Llama-specificity)** |
| Open class-changing axis | architecture | architecture | architecture | architecture (§6) | **CLOSED — confirmation now sought (Qwen), not class-change** |

### §0.3 Why Additive

| Integrity surface | v1.0–v1.3 | v1.4 |
|---|---|---|
| Prior axis statements | preserved verbatim | preserved verbatim; v1.4 adds Axis 10 only |
| Determinism discipline | bit-exact across 6 Llama checkpoints | extended: Checkpoint #1 on Mistral (fresh chain), drift 0.00e+00; bit-identical confirmatory dispatch |
| Copy-Unmount validation | 5 configs (all Llama) | extended: 6th config, first non-Llama (Mistral L4-L8), drift 0.00e+00 |
| Mechanism reachability | edit dispatched; signature observed | Axis 10: edit dispatched (0/5); internal gain 240–4000× confirmed; signature reproduced |
| PERMANENT preservation | v1.0/v1.1/v1.2/v1.3 verbatim | all four preserved verbatim; v1.4 amends only |

v1.4 neither extends nor retracts any prior version's claims. It closes the single UNTESTED row in the v1.3 §5.3 table that was flagged as class-changing.

---

## §1. v1.0 + v1.1 + v1.2 + v1.3 Carry-Forward (Statements Preserved Verbatim)

The full statements of v1.0 (§1.1), v1.1 (§1.2), v1.2 (§1.3), and v1.3 (Axes 8/9 + AKD elimination) are preserved verbatim in their source documents and are NOT restated or modified here. v1.4 carries them forward by reference. The load-bearing carry-forward for v1.4 interpretation:

- **v1.0 architectural-invariant ceiling** (PERMANENT): MEMIT cannot consistency-edit base Llama-3.1-8B at canonical hparams on cfb-v3; the edit dispatches and drives its internal objective hard while the external consistency probe registers a multi-order-of-magnitude miss.
- **v1.1 rank-1-in-weight class extension** (PERMANENT): the ceiling extends from MEMIT to ROME — it is a property of the rank-1-in-weight write-engine class, not of MEMIT's specific update rule.
- **v1.3 config-independence on base-Llama** (PERMANENT): the ceiling is independent of hparam config, corpus, target, probe-locus, layer-set, scale (8B→3B), AKD, and layer-band ([2–6] vs [4–8]) — across all nine axes, on base Llama.

v1.4's Axis 10 is the orthogonal extension of the v1.3 base-Llama config-independence to a second architecture family.

---

## §2. v1.4 Axis 10 — Cross-Architecture Generalization (S2.29)

### §2.1 Statement

The "Llama-family-specificity" hypothesis — that the nine-axis ceiling is a property of base Llama's representation geometry rather than of MEMIT-class editing on base decoder LMs generally — is **empirically FALSE**. MEMIT at canonical hparams on `mistralai/Mistral-7B-v0.3` (base), single-variable architecture port from the validated Llama config, produces `0/5` consistency on cfb-v3 with the identical internal-vs-external signature. The ceiling generalizes across base architecture families.

### §2.2 Empirical Surface

| Surface | Value |
|---|---|
| Model | `mistralai/Mistral-7B-v0.3` (base), revision `caa1feb0e54d415e2df31207e5f4e273e33509b1`, fp16 |
| Engine | MEMIT, SHA `80426fd9316cf9a50c5ba15e0912f2c2c5bfe84b` (byte-identical to all nine Llama axes; same patched working tree) |
| Hparams | 8B-canonical JSON, 3 architecture-structural overrides, **0 tuning-knob changes** (§2.4) |
| Edit band | `[4,5,6,7,8]` (EasyEdit MEMIT reference; Axis-9-validated equivalent to `[2–6]`) |
| Corpus / probes | cfb-v3 / probe-set-v3 (held verbatim; token IDs re-resolved against Mistral tokenizer) |
| Consistency verdict | **0/5** (trial 0 and confirmatory trial 1, bit-identical) |
| Internal objective (compute_z) | avg-prob gain **240×–4000×** per fact (guitar 2.94e-6→1.22e-2; piano 4.48e-6→9.69e-3; violin 6.55e-6→3.60e-3; harp 5.88e-6→1.43e-3; flute 1.52e-5→6.54e-3) |
| External post-edit P(target) | guitar 3.38e-4; piano 1.84e-4; violin 3.11e-3; harp 3.92e-4; flute 3.50e-3 — **P_max = 3.50e-3 ≪ 0.05 ≪ 0.5** |
| Top-1 after edit | unmoved on all 5 (his / golf / the / basketball / the) — never became target |
| Determinism | Checkpoint #1 on Mistral (fresh chain): drift 0.00e+00 across 38 probes; confirmatory dispatch bit-identical to trial 0 (compute_z traces, upd norms, external P all identical to the digit) |
| Copy-Unmount | drift 0.00e+00 both unmounts (6th validated config, first non-Llama) |
| VRAM peak | 21.3 GiB (under 24 GiB ceiling; tightest headroom of any arm) |
| Cov compute | 91.1 min for [4–8] band (5 × 822 MB caches, architecture-keyed, fresh) |

### §2.3 Trustworthiness Anchor

The Axis-10 `0/5` is certified by the same verdict-integrity chain as every prior axis, established fresh on Mistral:

1. **Deterministic load** — Checkpoint #1 self-check (capture twice, bit-exact): drift 0.00e+00, 0/38 top-1 mismatches. The fp16 forward pass is bit-stable on Mistral as on every Llama model.
2. **Clean pre-edit baseline** — all five target probabilities 1e-3 to 1e-2 pre-edit (Mistral does not natively associate the athletes with the instruments; same starting regime as Llama). Per-fact natural top-1 captured fresh (his / his / life / the / her — same function-word class as Llama, confirming the edit has the same job).
3. **Edit dispatched and ran** — deltas computed and inserted into all five layers (`Rewrite layer is 8`, `Tying objective to 31` — config propagated; all five `_t100_` cov caches loaded by exact path, no lookup miss); internal objective driven up 240–4000×. The edit is physically present in the weights.
4. **External 0/5** — post-edit P(target) at or below pre-edit on the STRICT facts (guitar went *down*, 8.15e-3 → 3.38e-4), top-1 unmoved.
5. **Bit-exact unmount** — natural top-1 probabilities return to pre-edit values to the last decimal (drift 0.00e+00); the edited model is bit-exact-restorable, certifying the 0/5 as a real property of the edited model, not a corrupted-state artifact.
6. **Confirmatory stability** — a fresh edit on the bit-exact-restored model reproduces the entire optimization deterministically (trial 1 = trial 0 to the digit). 0/5 is a stable, reproducible property, not a single-run accident.

The read is cleanest exactly where it is load-bearing: **guitar (cfb-v3-001) and piano (cfb-v3-002) are STRICT single-token targets on Mistral, both members of the verdict-integrity subset {001, 002, 005}.** They fail at full strength with no proxy weakness. The Mistral-tokenizer fragmentation of violin/harp/flute (§2.6) is therefore immaterial to the load-bearing facts.

### §2.4 Cross-Architecture Config Idiom (extends the v1.3 §2.4 scale-variant idiom)

The proven Mistral MEMIT config is **not bespoke** — it is `json.load(hparams/MEMIT/Llama-3.1-8B.json)` with exactly three structural (non-hparam-tuning) overrides, and **zero tuning-knob changes**:

1. `layers`: `[2,3,4,5,6]` → **`[4,5,6,7,8]`** (EasyEdit MEMIT reference band for the 7B-Llama/Mistral architecture, arXiv 2308.07269 Table 4; adopted per the §6''.1 methodology lock, OQ-V12-T-BRANCH-3; Axis-9-validated equivalent to `[2–6]`). Config-class, not a tuning change.
2. `v_loss_layer`: 31 → **31** (Mistral has 32 layers; n_layers − 1 = 31, identical to 8B by layer-count coincidence — no effective change).
3. `lm_head_module`: `"model.embed_tokens"` (the 3B tied override) → **`"lm_head"`** (Mistral `tie_word_embeddings=False`; `lm_head.weight` IS a named parameter — the untied form, reverting the 3B adaptation back to the 8B-canonical form).

**The cross-architecture idiom is LIGHTER than the scale idiom, not heavier.** The 3B port (v1.3 §2.4) required overriding the tied-embedding `lm_head_module`; the Mistral port *reverts* that override because Mistral, like the 8B canonical, is untied. Mistral shares the 8B's hidden size (4096), intermediate size (14336), and layer count (32) — so the hparam-structural surface is nearly identical to the 8B canonical. The genuine cross-architecture cost lives elsewhere:

- **Tokenizer (the real port surface).** Mistral's SentencePiece 32768-token vocab is entirely disjoint from Llama-3's 128256-token BPE vocab. All probe and target token IDs were re-resolved from scratch (D-S229-TOKEN-RERESOLVE-1). This is the largest correctness surface in a cross-architecture port and the place a careless reuse of Llama token IDs would silently corrupt the verdict.
- **Pad-token convention.** Mistral ships no dedicated pad token; the Pad-Token patch re-derives to `eos_token_id = 2` (D-S229-PADTOKEN-1) — the one patch with model-specific content vs the Llama canonical.
- **P-4 is the structural enabler.** The patch that routes the engine's GPT-J-era config-attribute lookups (`n_embd`, `n_positions`) to the modern HF schema (`hidden_size`, `max_position_embeddings`) already lists Mistral as Required (memit-patches v2.5 §3.5.2) and applies verbatim — it is the reason the byte-identical Llama engine runs unchanged on Mistral.

The tuning-knob audit at config build confirmed `{}` diff vs 8B for `mom2_update_weight` (15000), `v_lr` (0.5), `v_num_grad_steps` (25), `kl_factor` (0.0625), `clamp_norm_factor` (0.75), `v_weight_decay` (0.5). **Not one tuning knob changed.** This is what makes Axis 10 a clean single-variable architecture read: the only differences from the config that produced all nine Llama axes are the three architecture-forced structural overrides.

This "load 8B JSON, override structurally, change no tuning knob, re-resolve the tokenizer" pattern is the canonical **cross-architecture MEMIT config idiom** (D-S229-HPARAM-IDIOM-2, generalizing D-S227-HPARAM-IDIOM-1).

### §2.5 Scope Boundary (load-bearing for interpretation)

Axis 10 establishes the ceiling on **one** non-Llama architecture family (Mistral). A single non-Llama instance is strong evidence for the G (base-decoder-LM-general) reading but is not, on its own, decisive — a skeptic could note that Mistral-7B descends from the same Llama-2 architectural lineage (same RMSNorm, RoPE, gated-MLP, GQA-family decoder block) and argue the result reflects shared *architecture-shape* rather than true family-generality. The **Qwen-7B confirmation arm (S2.30, T.3-β)** addresses exactly this: Qwen is a more architecturally distinct decoder family (different attention/normalization details, different tokenizer lineage), and a `0/5` signature reproduction there would be near-decisive for G. v1.4's claim in its precise form is therefore: **the ceiling generalizes from Llama to Mistral, the first cross-architecture-family axis; a second non-Llama family (Qwen) is sought as confirmation, not as a class-change candidate.**

### §2.6 Mistral-Tokenizer Fragmentation (recorded for the Qwen port and for verdict interpretation)

Mistral's smaller vocab (32768 vs Llama's 128256) fragments three of five cfb-v3 targets that were single-token on Llama:

| Fact | target | Llama-3.2-3B | Mistral-7B-v0.3 | class |
|---|---|---|---|---|
| cfb-v3-001 | guitar | `[17418]` 1-tok | `[11454]` 1-tok | STRICT (unchanged) |
| cfb-v3-002 | piano | `[27374]` 1-tok | `[13989]` 1-tok | STRICT (unchanged) |
| cfb-v3-003 | violin | `[63137]` 1-tok | `[4875,1030]` (viol+in) 2-tok | STRICT → PROXY |
| cfb-v3-004 | harp | `[4960,79]` 2-tok | `[5180,29488]` (har+p) 2-tok | PROXY (unchanged) |
| cfb-v3-005 | flute | `[96812]` 1-tok | `[1740,2491]` (fl+ute) 2-tok | STRICT → PROXY |

**Why this does not weaken the verdict (D-S229-TOKENFRAG-1):** the first-token-proxy measures a *lower-specificity* event than the whole word, so a proxy *PASS* would be a weaker signal than a STRICT pass. But Axis 10 is a `0/5` FAIL, and for a FAIL the proxy is strictly **conservative in the ceiling's favor**: if even the low-bar first-subword probability stays near zero post-edit, the whole-word target is certainly near zero. The full-sequence P was captured alongside the proxy at dispatch (the RE-EVALUATE-at-trial-0 gate); the verdict is read off the full sequence. And the two STRICT facts (001/002) are both in the verdict-integrity subset and fail at full strength. The fragmentation makes proxy *passes* less trustworthy and the observed `0/5` FAIL *more* trustworthy. For the Qwen port, the target tokenization must be re-classified fresh (Qwen has its own vocab); STRICT-fact selection for the integrity subset should prefer targets that remain single-token on the target architecture.

---

## §3. Updated Ceiling Characterization at v1.4

### §3.1 The Ten-Axis Ceiling

```
Architectural-invariant ceiling at v1.4 — ten axes
═══════════════════════════════════════════════════════════════════════
  Axes 1–6  (v1.0)  MEMIT on Llama-3.1-8B:
       hparam sweep / corpus / target / v_lr / mediation-locus / layer-set
  Axis  7   (v1.1)  ROME on Llama-3.1-8B (L17 + L2)
  ─────────────────────────────────────────────────────────────────────
  Axis  8   (v1.3)  MEMIT on Llama-3.2-3B — FIRST MODEL-VARIATION AXIS
       0/5; signature reproduced; scale 8B→3B
  Axis  9   (v1.3)  MEMIT on Llama-3.2-3B, band [4–8] — FIRST CONFIG-VARIATION AXIS
       0/5; signature reproduced; single-variable; delta_vs_2_6_floor ≈ 0
  ─────────────────────────────────────────────────────────────────────
  Axis 10   (v1.4)  MEMIT on Mistral-7B-v0.3 — FIRST ARCHITECTURE-FAMILY AXIS
       0/5; signature reproduced; internal gain 240–4000×; P_max 3.50e-3;
       single-variable architecture port (0 tuning-knob changes)
  ─────────────────────────────────────────────────────────────────────
  Confounds ELIMINATED:
       A / B / C / D (v1.0)           corpus / probe / target / layer-set
       write-engine swap (v1.1)        MEMIT ⇄ ROME (rank-1-in-weight class)
       AKD / key-collision (v1.3)      cfb-v3 measured high-AKD (4.62 band)
       layer-band placement (v1.3)     [2–6] ⇄ [4–8], single-variable 0/5
       Llama-family-specificity (v1.4) Llama ⇄ Mistral, single-variable 0/5

  Coverage: MEMIT + ROME on base decoder LMs, across
            {Llama-3B, Llama-8B, Mistral-7B} × {[2–6], [4–8]}
  Property: config-independent AND architecture-family-independent across all
            axes tested; NOT eliminable within the MEMIT-class-on-base-
            decoder-LM regime by any axis varied to date
═══════════════════════════════════════════════════════════════════════
```

### §3.2 Off-Axis Environmental / Adapter Findings (unchanged from v1.3 §5.2)

The GRACE adapter-mechanism findings (S2.20 environmental ceiling; S2.22 3B environmental eliminability + discriminator-gate non-firing) remain off the rank-1-in-weight axis count, carried forward verbatim from v1.3 §5.2. The adapter-mechanism class carries a separate, weaker, hparam-conditional finding and does not contribute a ceiling axis. v1.4 makes no change to this surface.

### §3.3 What the Ceiling Now Is — and Is Not

| Claim | Status at v1.4 |
|---|---|
| MEMIT cannot consistency-edit base Llama-3.1-8B at canonical hparams (cfb-v3) | EMPIRICALLY VALIDATED (Axes 1–6) |
| Ceiling extends to ROME (rank-1-in-weight class) | EMPIRICALLY VALIDATED (Axis 7) |
| Ceiling generalizes across Llama scale (8B→3B) | EMPIRICALLY VALIDATED (Axis 8) |
| Ceiling is NOT a low-AKD-corpus artifact | EMPIRICALLY VALIDATED (AKD elimination) |
| Ceiling is NOT a layer-band artifact ([2–6] vs [4–8]) | EMPIRICALLY VALIDATED (Axis 9) |
| Ceiling is config-independent across all config axes varied to date | EMPIRICALLY VALIDATED (9 config axes) |
| **Ceiling holds on a non-Llama architecture (Mistral)** | **EMPIRICALLY VALIDATED (Axis 10)** ← v1.4 |
| Ceiling holds on a SECOND non-Llama family (Qwen) | UNTESTED — T.3-β open (§4); confirmation arm, not class-change |
| Ceiling holds on Instruct (vs base) decoder LM | UNTESTED — OQ-S225-BASE-INSTRUCT-1 open |
| Ceiling holds on a high-AKD benchmark corpus (KnowEdit) edit | UNTESTED — external-validity arm open |
| Ceiling holds under per-layer-swept optimal band | UNTESTED — within-regime deeper arm, DEPRIORITIZED |
| Adapter-mechanism (GRACE) viable at non-canonical hparams | UNTESTED — off-axis (§3.2) |

The ceiling is a **config-independent, architecture-family-independent MEMIT-class-on-base-decoder-LM property**. The class-changing axis that v1.3 flagged as the only remaining one (cross-architecture) is now CLOSED for its first instance; the remaining open arms are confirmation (Qwen), external-validity (Instruct, benchmark corpus), and a deprioritized within-regime deeper arm — none of which can change the finding's *class*, only its breadth.

---

## §4. Forward — Qwen Confirmation Arm vs Closure

### §4.1 The Routing Question Resolved

v1.3 §6 posed the cross-architecture axis as the open class-changing question and recommended sequencing it ahead of the within-regime deeper arms. S2.29 executed it. The result (`0/5`, signature reproduced) is the G outcome, which routes — per the S2.29 Cell-13 matrix and the kickoff decision matrix — to the **Qwen-7B confirmation arm (S2.30, T.3-β)**, NOT to the within-regime per-layer sweep (which would have re-activated only on a surprising Mistral CLEAR).

### §4.2 v1.4 Recommendation (Claude's call, surfaced for the record per standing directive)

**Run T.3-β-QWEN as the next session (S2.30).** Rationale:

1. **It is the cheapest near-decisive move.** The T.3 scaffold (this session's runbook) ports directly to Qwen with the same single-variable discipline; the only re-derivations are Qwen's structural fields, tokenizer, and pad convention. The Mistral run proved the port pattern; Qwen reuses it.
2. **It closes the §2.5 scope boundary.** Mistral shares Llama-2's architectural lineage; Qwen is the more distinct decoder family available at the 7B scale. A `0/5` on Qwen converts "generalizes from Llama to a Llama-lineage cousin" into "generalizes across architecturally distinct base decoder LM families" — the strongest form of G obtainable without exhausting the model zoo.
3. **A Qwen CLEAR (low prior) would be highly informative,** narrowing G back toward "Llama-lineage decoder LMs" and re-opening the architecture-geometry question. Either Qwen outcome is decision-relevant.

### §4.3 Recommended Sequencing

| Priority | Arm | Status | Cost | Changes finding class? |
|---|---|---|---|---|
| 1 | T.3-β-QWEN (S2.30) | confirmation arm; routed | ~1 session (port pattern proven) | No — confirms G or narrows to Llama-lineage |
| 2 | Instruct-vs-base (OQ-S225-BASE-INSTRUCT-1) | open | ~1 session | No — adds an orthogonal generalization axis |
| 3 | KnowEdit external-validity edit | open | moderate | No — external validity, not ceiling class |
| — | Within-regime per-layer sweep | DEPRIORITIZED (re-activates only on a cross-arch CLEAR) | high | No |

### §4.4 What This Recommendation Does NOT Do

v1.4 does not declare G *closed* — it declares the first cross-architecture instance VALIDATED and routes to confirmation. It does not author the Qwen runbook (S2.30 deliverable). It does not retract the v1.3 deprioritization of the within-regime per-layer sweep (the Mistral `0/5` keeps it deprioritized — a sweep re-activates only on a CLEAR, which did not occur). It makes no claim about Instruct models, benchmark corpora, or adapter mechanisms.

---

## §5. Cross-Reference Map

### §5.1 v1.4 Inheritance from Session Decisions

| §  | Source decision/constraint |
|---|---|
| §2 Axis 10 statement / surface | D-S229-Q1-1; D-S229-VERDICT (Cell 13 Route A); D-S229-COV-SCOPE-1 |
| §2.3 trustworthiness anchor | C-S229-CHECKPOINT-1 (Checkpoint #1 Mistral); IC-S23-4 (unmount); D-S229-CONFIRM-1 (confirmatory stability) |
| §2.4 cross-architecture idiom | D-S229-HPARAM-IDIOM-2; D-S229-LMHEAD-1; D-S229-PADTOKEN-1; D-S229-Q3-1 |
| §2.6 fragmentation | D-S229-TOKENFRAG-1; D-S229-TOKEN-RERESOLVE-1 |
| §3.1 ten-axis ceiling | D-S229-VERDICT; framework_finding v1.3 §5.1 (nine-axis base) |
| §4 forward / Qwen routing | D-S229-ROUTE-A-1; t_branch_decision_document v1.3 (§-amendment) |

### §5.2 Forward References

| §  | Forward target |
|---|---|
| §3.1 ten-axis ceiling | t_branch_decision_document v1.3 (routing matrix) |
| §4 Qwen confirmation arm | t3_qwen_7b_memit_runbook v0.1 (S2.30 deliverable) |
| §2.4 cross-architecture idiom | reusable for Qwen port + any future architecture-family axis |

### §5.3 Sibling Cross-References

| §  | Sibling artifact |
|---|---|
| §2 Axis 10 (Mistral MEMIT) | `t3_mistral_7b_memit_runbook v0.1`; `session_2_29_summary_block.md` |
| §2.4 idiom | `framework_finding v1.3 §2.4` (scale-variant idiom, generalized here) |
| §3.2 off-axis GRACE | `framework_finding v1.2`; `t_branch_decision_document` (GRACE rows) |

---

**v1.4 status:** ADDITIVE AMENDMENT — RATIFIED S2.29 close 2026-06-15. v1.0 + v1.1 + v1.2 + v1.3 PERMANENT preserved verbatim. Ten-axis architectural-invariant ceiling; first cross-architecture-family axis; ceiling promoted from config-independent-MEMIT-on-base-Llama to config-independent-MEMIT-class-on-base-decoder-LM. Routes to T.3-β-QWEN confirmation arm (S2.30).

*End of framework_finding_memit_ceiling_archival v1.4.*
