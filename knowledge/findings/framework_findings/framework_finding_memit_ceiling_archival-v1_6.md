# Framework Finding — MEMIT Ceiling Archival — v1.6

**Status:** ADDITIVE AMENDMENT (v1.0 + v1.1 + v1.2 + v1.3 + v1.4 + v1.5 PERMANENT preserved verbatim)

**Version lineage:**
- v1.0 (PERMANENT; S2.18) — rank-1-in-weight class ceiling on Llama-3.1-8B; seven axes
- v1.1 (ADDITIVE; S2.18) — ROME elimination (Axis 7)
- v1.2 (ADDITIVE; S2.20) — adapter-mechanism environmental ceiling (GRACE)
- v1.3 (ADDITIVE; S2.28) — Axis 8 (cross-scale 8B→3B) + AKD elimination + Axis 9 (band-invariance)
- v1.4 (ADDITIVE; S2.29) — Axis 10 (cross-architecture, Mistral-7B); promoted ceiling L → G
- v1.5 (ADDITIVE; S2.31) — Axis 11 (cross-architecture FALSIFICATION, Qwen2.5-7B CLEARS); G falsified, ceiling narrows to Llama-lineage; mechanism refined to internal z-optimization stage; CPU-solve confound exonerated
- v1.6 (ADDITIVE; S2.32) — **Axis 11 CLEAR-hardening.** The Qwen CLEAR is hardened from single-dispatch 5/5 consistency to a **full-panel, 4-trial finding-grade-AND-qualified** result: the edit *expresses* (consistency 5/5 stable, across 2/3 surface forms) but is **entity-local-not-attribute-local** — it collaterally perturbs the edited entity's own biographical attributes (generalization 3/15, stable, bit-exact reversible) while leaving non-edited entities pristine (specificity 3/3). Mistral re-confirms 0/5 through the same patched engine (within-engine Llama-lineage-holds/Qwen-clears contrast).

---

## §0. Amendment Scope

### §0.1 Statement

v1.6 documents the S2.32 CLEAR-hardening arc that ran after v1.5 was ratified. The amendment is **ADDITIVE** — v1.0–v1.5 integrity preserved verbatim. v1.6 makes **no change to the ceiling characterization** (the G→Llama-lineage narrowing of v1.5 stands unmodified and is strengthened). v1.6 adds a precise *quality* characterization of the Qwen CLEAR that v1.5's single dispatch could not resolve:

1. **The Qwen CLEAR is finding-grade.** Across the full 38-probe panel and 4 trials, the edit demonstrably expresses: consistency 5/5 aggregate (stable), robust on two of three independent surface forms, specificity 3/3 pristine, unmount bit-exact. Qwen genuinely breaks the Llama-lineage ceiling — the narrowing is not a single-prompt artifact.
2. **The Qwen CLEAR is qualified.** The expressed edit is **not attribute-local**: it collaterally perturbs the edited entity's own unrelated biographical facts (generalization 3/15, all 12 failures same-subject, large directional drift), while leaving non-edited entities pristine (specificity 3/3). The perturbation is entity-confined, not global, and is bit-exact reversible (provably edit-caused).

**The disposition this forces:** v1.5 established "Qwen CLEARS 5/5 consistency." v1.6 sharpens this to: **Qwen breaks the consistency ceiling — the edit expresses where Llama-lineage cannot — but the expressed edit is entity-local-not-attribute-local: it writes the new fact while damaging the edited entity's neighboring attributes.** This is a sharper, more publishable result than either pole of the promote-vs-qualify binary the S2.32 kickoff anticipated.

### §0.2 What is ADDED vs what is PRESERVED (no prior axis or narrowing is retracted)

v1.6 retracts **nothing** from v1.0–v1.5. The G→Llama-lineage narrowing (v1.5 Axis 11) stands and is **strengthened** — the within-engine Mistral re-confirm (§4) shows the lineage boundary holding on both sides through one engine. What v1.6 adds is the *quality* of the Qwen CLEAR, invisible to v1.5's single consistency dispatch:

- Qwen still clears consistency (v1.5) — re-confirmed 5/5 stable ×4 (§2).
- Mistral still holds (v1.4) — re-confirmed 0/5 through the patched engine (§4).
- What is NEW: the Qwen edit, though it expresses, is **not clean** — it perturbs the edited entity's other attributes (§3). This is a property of *how Qwen breaks the ceiling*, not a change to *whether* it breaks it.

### §0.3 Diff vs Prior Versions

| Surface | v1.4 | v1.5 | v1.6 ADDITIVE (this) |
|---|---|---|---|
| Axes | +10 (Mistral) | +11 (Qwen FALSIFIES) | +11 hardened (Qwen full-panel ×4) |
| Ceiling class | config-indep on base-decoder-LM (G) | config-indep on Llama-lineage (G falsified) | **unchanged — Llama-lineage** |
| Qwen CLEAR grade | — | single-dispatch 5/5 consistency | **finding-grade (5/5 stable ×4, 2/3 surface forms, spec 3/3, unmount bit-exact)** |
| Qwen CLEAR quality | — | unresolved | **qualified: entity-local-NOT-attribute-local (gen 3/15 same-subject drift)** |
| Within-engine lineage contrast | — | — | **established (Qwen 5/5 / Mistral 0/5 through one patched engine)** |
| Copy-Unmount configs | 6 | 7 (Qwen L4-8) | 7, re-confirmed ×4 + edit-attribution corollary |

### §0.4 Why Additive

| Integrity surface | v1.0–v1.5 | v1.6 |
|---|---|---|
| Prior axis statements | preserved verbatim | preserved verbatim; no retraction |
| G→Llama-lineage narrowing | established v1.5 | preserved + strengthened (within-engine contrast) |
| Determinism discipline | bit-exact, multiple checkpoints | Checkpoint #1 re-established on fresh kernel (drift 0.00e+00); 4-trial deterministic reproduction |
| Copy-Unmount validation | 7 configs | 7th re-confirmed ×4 + edit-attribution corollary (biographical drift reverses bit-exact) |
| Engine integrity | byte-identical + P-VRAM-CPU-SOLVE exonerated | same; patch re-applied, fingerprinted (`5c0c706a…`); Mistral re-confirm closes the holds-side confound thread |
| PERMANENT preservation | v1.0–v1.5 verbatim | all six preserved verbatim; v1.6 amends only |

---

## §1. v1.0–v1.5 Carry-Forward (Statements Preserved Verbatim)

Full statements of v1.0–v1.5 are preserved verbatim in their source documents. Load-bearing carry-forward for v1.6:

- **v1.5 narrowing** (PERMANENT): the architectural-invariant ceiling is a property of **Llama-lineage** base decoder LMs (Llama-3.1-8B ×7 axes, Llama-3.2-3B, Mistral-7B-v0.3), NOT base decoder LMs generally; Qwen2.5-7B is the falsifying case. — unchanged.
- **v1.5 internal-stage mechanism** (PERMANENT): the lineage divergence appears at the internal z-optimization stage (Qwen converges >0.98; Llama does not). — unchanged; v1.6 adds the external-surface consequence (the converged Qwen edit expresses but damages neighbors).

v1.6 hardens v1.5's Axis 11 and adds the CLEAR's quality characterization.

---

## §2. v1.6 Axis 11 Hardening — the CLEAR is finding-grade (S2.32 Arm 1)

### §2.1 Statement

The Qwen CLEAR survives the full 38-probe panel across 4 trials. The edit expresses at the output surface — consistency 5/5 aggregate, stable, robust across two of three independent surface forms, specificity-clean, bit-exact reversible. It is not a single-prompt or single-trial artifact.

### §2.2 Empirical Surface (Qwen, through `P-VRAM-CPU-SOLVE`-patched engine, 4 trials)

| Surface | Value |
|---|---|
| Model | `Qwen/Qwen2.5-7B`, rev `d149729398750b98c0af14eb82c78cfe92750796`, fp16 |
| Engine | MEMIT SHA `80426fd9` + `P-VRAM-CPU-SOLVE` (patched `memit_main.py` SHA `5c0c706a…`) |
| Config | 8B-canonical JSON; ARCH-FORCED `v_loss_layer 31→27`; PORT-CONSTANT band `[4,5,6,7,8]`; 0 tuning-knob changes |
| Determinism | Checkpoint #1 (fresh kernel) drift 0.00e+00, 0/5 mismatch |
| compute_z (internal) | converged >0.98 all 5 (guitar 0.0047→0.9903; piano 0.0129→0.9965; violin 0.0042→0.9992; harp 0.0192→0.9932; flute 0.0042→0.9803) |
| Consistency aggregate | **5/5 facts (≥2/3 probes), stable ×4** |
| Surface-form breakdown | cons-1 5/5; cons-3 5/5; cons-2 (cleft) 2/5 |
| Internal-vs-external | signature ABSENT (external follows internal; top-1 moved all 5) |
| Specificity | **3/3 pristine** (Paris Δ0.005, Jupiter Δ0.001, Au Δ0.001), stable ×4 |
| Unmount | **bit-exact 0.00e+00**, stable ×4 — 7th Copy-Unmount config, 2nd non-Llama |
| VRAM peak | 19.39 GiB (CPU-solve; float64 off-GPU) |
| Token fidelity | integrity subset {001/002/005} 3/3 STRICT — load-bearing read at full single-token fidelity |

### §2.3 Surface-form sensitivity (the cons-2 cleft)

The edit is robust on cons-1 ("plays the musical instrument of") and cons-3 ("is a musician who plays the") — 5/5 each. It is soft on cons-2 ("The instrument that {X} plays is"), the cleft form where the subject is displaced from the prompt-end at which `fact_token="subject_last"` anchors the edit key: guitar 0.47 (top-1 moved but below band), harp 0.38 (moved, below band), flute 0.0018 (did not take). This is a genuine generalization-of-edit limit on the hardest surface form — but it is **materially different** from the Llama-lineage ceiling, where *no* surface form expresses and the internal optimizer never converges. The narrowing is not retracted.

---

## §3. The CLEAR's Quality — entity-local-NOT-attribute-local (the v1.6 qualifier)

### §3.1 Generalization (locality): 3/15, all failures same-subject

Generalization predicate (probe-set-v3 §126): `abs(Δp_top_1) < 0.05 AND top_1 unmoved`, evaluated against the **Qwen-captured** pre-edit baseline (NOT the YAML's Llama-captured `expected_top_1`). Result: **3/15 PASS, stable across 4 trials.** All 12 failures are on the edited subjects' **own biographical probes**:

- Hakeem "born in the country of" Nigeria 0.831 → 0.189 (Δ0.642)
- Deion born-state Georgia 0.313 → 0.747 (Δ0.434)
- Tiger "attended college at" Stanford → ` the` (top-1 moved)
- Bo "attended college at" Auburn → ` the` (top-1 moved)
- Lindsey born-state Colorado → ` New` (top-1 moved)
- (and 7 more, all same-subject)

### §3.2 Specificity: 3/3 pristine — the perturbation is entity-confined

Shared world-fact probes that name no edited subject (France→Paris, Jupiter, gold→Au) are untouched (Δ<0.005, stable ×4). Combined with §3.1, the perturbation is **confined to the five edited entities** — it is not a global degradation of the model.

### §3.3 Edit-attribution: the perturbation reverses bit-exact

On Copy-Unmount, the §3.1 biographical drift reverses to the exact pre-edit values (Nigeria→0.831, Stanford→0.656, Auburn→0.149, all Δ vs pre = 0.00e+00). The collateral damage is **edit-caused and edit-removable** — not pre-existing state, not measurement noise. The qualification is causally grounded.

### §3.4 Mechanistic reading

The MEMIT joint-overlay edit at L4-8 on `{subject} plays the instrument of` does not merely install the instrument association — it perturbs the model's broader representation of *that subject*. Asking the same subject's college or birthplace afterward returns a shifted answer. The edit is **subject-local but not fact-local**: it changes more about the edited entity than just the target attribute. This connects to the v1.5 §3 internal-stage thread — on Qwen the optimizer *finds* an edit direction (converges >0.98), but the direction it finds is entangled with the subject's broader representation, so expressing the new instrument fact drags neighboring attributes with it. On Llama-lineage the optimizer never finds the direction at all, so the question of attribute-locality never arises. **The lineage difference is not just "does the edit express" but "what does the expressed edit cost."**

---

## §4. Within-Engine Lineage Contrast — Mistral re-confirms 0/5 (S2.32 Arm 2)

Mistral-7B-v0.3 (S2.29-pinned SHA `caa1feb0…`, S2.29-identical config: band [4-8], v_loss_layer 31 unmodified, pad=eos) through the **same `P-VRAM-CPU-SOLVE`-patched engine**: **consistency 0/5.** The edit ran to completion (2.4 min, 18.08 GiB — not a crash); post-edit top-1s reassert native priors (`'golf'` for Tiger Woods, `'basketball'` for Hakeem, function words otherwise); target probabilities at floor (8.4e-04–1.98e-03), lower than pre-edit in 4/5. The genuine Llama-lineage signature.

This **closes the patch-confound thread on the holds side.** v1.5 §4 proved the patch cannot manufacture a CLEAR (Llama isolation). v1.6 §4 proves it cannot manufacture a hold either. The within-engine contrast is now complete and stated through one engine:

> Same patched engine, same band [4-8], canonical config differing by exactly one architecture-forced integer (Mistral v_loss_layer 31 / Qwen 27): **Qwen converges >0.98 and expresses 5/5; Mistral crawls and holds 0/5.** The difference is architecture lineage.

This is the strongest single-session statement of the v1.5 lineage boundary — both sides demonstrated through one engine.

---

## §5. Forward Implication

v1.6 leaves the v1.5 architecture-geometry frontier open and deepens it with a second mechanistic sub-question:

1. **Where exactly is the lineage boundary?** (v1.5 §5.1; t_branch v1.4 Axis 3) — unchanged; requires a second non-Llama-lineage family (Phi / Gemma / NeoX) to clear-or-hold.
2. **What geometric property obstructs the z-optimization on Llama-lineage but not Qwen?** (v1.5 §5.2; Axis 2) — unchanged; per-layer z-convergence comparison.
3. **NEW: why does the expressed Qwen edit damage the edited entity's neighboring attributes?** — the §3.4 entanglement thread. Whether this is intrinsic to MEMIT-on-Qwen or tunable away (narrower band, single-layer scope, lower mom2_update_weight) is the applied "is the LLM-as-database write layer viable on Qwen" question, bearing directly on the framework's parametric-memory premise.

The v1.6 finding refines the consequential v1.5 result: Qwen does not merely break the ceiling — it breaks it **incompletely**, expressing the target fact at the cost of collateral damage to the edited entity. The write layer is *editable* on Qwen-lineage in a way it is not on Llama-lineage, but the edit is not *clean*. This is the precise, qualified form of the cross-architecture CLEAR.

---

**v1.6 RATIFIED S2.32 close 2026-06-15.** ADDITIVE; v1.0–v1.5 PERMANENT preserved verbatim. Axis 11 hardened: Qwen2.5-7B CLEAR is finding-grade (5/5 consistency stable ×4, 2/3 surface forms, specificity 3/3, unmount bit-exact) AND qualified (entity-local-not-attribute-local: gen 3/15 same-subject drift, bit-exact reversible). Mistral re-confirms 0/5 through the patched engine — within-engine Llama-lineage-holds/Qwen-clears contrast established; patch-confound thread closed both sides. G→Llama-lineage narrowing preserved and strengthened. OQ-S231-CLEAR-ROBUSTNESS-1 resolved.
