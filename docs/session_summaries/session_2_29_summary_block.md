# Session 2.29 Summary Block — T.3-α-MISTRAL (cross-architecture MEMIT port)

**Session type:** Execution (fold: thin runbook authoring micro-pass + cell-by-cell execution)
**Date:** 2026-06-15
**Predecessor:** S2.28 (T.3 re-scope ratification; D-S228-T3-RESCOPE-1)
**Successor:** S2.30 (T.3-β-QWEN confirmation arm)
**Verdict:** `ROUTE_A_HALT — 0/5 SIGNATURE-REPRODUCED` → ceiling promoted **Llama-family-specific (L) → base-decoder-LM-general (G)**. Axis 10 confirmed.

---

## §1. One-Line Result

MEMIT at canonical hparams on `mistralai/Mistral-7B-v0.3` (base) produces **0/5 consistency** on cfb-v3 with the identical internal-vs-external signature seen on every Llama axis — internal objective driven up **240–4000×** while external P(target) stays **≤ 3.50e-3** and top-1 never moves. The architectural-invariant ceiling is **not Llama-specific**; it reproduces on a non-Llama base decoder LM at canonical hparams with **zero tuning-knob changes**. This is **Axis 10** — the first architecture-family-variation axis and the only axis class that could change the finding's *class*.

---

## §2. Deliverables (RATIFIED 2026-06-15)

| Artifact | Lines | Status |
|---|---|---|
| `t3_mistral_7b_memit_runbook v0.1` | 973 | DECLARATIVE → EXECUTED (full authoring, zero placeholders; all 23 cells run) |
| `framework_finding_memit_ceiling_archival v1.4` | — | ADDITIVE AMENDMENT (Axis 10; v1.0–v1.3 PERMANENT preserved verbatim) |
| `t_branch_decision_document v1.3` | — | ADDITIVE (T.3-α executed; Mistral L→G recorded; Qwen routed) |
| `session_2_29_summary_block.md` | — | this artifact |
| `s229_mistral_memit_hparams.json` | — | NV; Mistral MEMIT config (3 structural overrides, 0 tuning changes) |
| `mistral_7b_v0_3_baselines.json` | — | NV; Checkpoint #1 producer artifact (fresh determinism chain) |
| `s229_fact_verdicts.json` | — | NV; Mistral-resolved token IDs + allowlist |
| `s229_trial0_record.json` | — | NV; per-trial verdict record |
| 5 × Mistral cov caches (L4–L8) | — | NV (~4.1 GiB; architecture-keyed; `_t100_`) |

---

## §3. Decisions (D-S229-*)

| ID | Statement |
|---|---|
| D-S229-Q1-1 | Runbook structural inheritance from `t1_alt_model_3b_memit_runbook v0.1` with cross-architecture substitutions; corpus / probe-strings / trial protocol / acceptance bands held verbatim |
| D-S229-Q2-1 | Cell 5 PRODUCES Mistral Checkpoint #1 (fresh determinism chain; no prior baseline to consume) — drift 0.00e+00 |
| D-S229-Q3-1 | Reference band `[4,5,6,7,8]` adopted from EasyEdit MEMIT critical-range (OQ-V12-T-BRANCH-3); Axis-9-validated equivalent to `[2–6]` |
| D-S229-Q4-1 | Cell 8 fresh Mistral cov computation at `[4..8]`; 91.1 min; 5 × 822 MB; architecture-keyed |
| D-S229-LMHEAD-1 | `lm_head_module='lm_head'` (UNTIED; reverts the 3B tied override to 8B form); verified untied at Cell 1.5 (the INVERSE of the 3B adaptation) |
| D-S229-PADTOKEN-1 | Pad-Token RE-DERIVED to `eos_token_id=2` per Mistral convention (the one patch with model-specific content) |
| D-S229-PATCH-INHERITANCE-1 | All MEMIT patches inherited live from the byte-identical Llama-arm engine (SHA 80426fd9); P-4 (Mistral=Required) ×4 sites + P-7 verified live; Cell 2 = verification pass, not re-apply |
| D-S229-TOKEN-RERESOLVE-1 | ALL probe + target token IDs re-resolved against the Mistral tokenizer; Llama allowlist NOT inherited |
| D-S229-TOKENFRAG-1 | Mistral 32k vocab fragments violin/harp/flute (STRICT→PROXY); proceed — fragmentation is conservative-in-ceiling's-favor for a 0/5 FAIL; STRICT facts (001/002, both in integrity subset) carry the load-bearing read |
| D-S229-COV-SCOPE-1 | Full band `[4..8]` cov scope (not L5-only); parity with all nine prior axes |
| D-S229-HPARAM-IDIOM-2 | Cross-architecture config idiom: load 8B JSON, 3 structural overrides, 0 tuning changes, re-resolve tokenizer (generalizes D-S227-HPARAM-IDIOM-1) |
| D-S229-ENGINE-REUSE-1 | Engine reused live-patched (SHA 80426fd9), not freshly cloned; byte-identical to all nine Llama axes — stronger for the single-variable claim than a fresh clone; patch fingerprint snapshotted for the manifest |
| D-S229-ROUTE-A-1 | Cell 13 Route A (single confirmatory dispatch, not 15 trials) on 0/5 + reproduced signature; confirmatory trial bit-identical to trial 0 → STABLE |
| D-S229-CONFIRM-1 | Confirmatory dispatch reproduces trial 0 to the digit (compute_z traces, upd norms, external P all identical) — 0/5 is a stable, deterministic property |

---

## §4. Constraints (C-S229-*)

| ID | Statement |
|---|---|
| C-S229-1 | MEMIT engine SHA pinned (80426fd9316cf9a50c5ba15e0912f2c2c5bfe84b); Mistral model SHA pinned (caa1feb0e54d415e2df31207e5f4e273e33509b1) |
| C-S229-2 | Engine patch-fingerprint snapshot at `/workspace/architecture_profile/engine_source_snapshot/memit_80426fd9/` (6-file SHA-256) |
| C-S229-3 | Cov-cache provenance: per-layer size (822084770 B) + SHA-256 recorded for the Cell 18 integrity gate |
| C-S229-4 | Layer-set bound assertion: all of `[4..8]` within `0 ≤ idx < 32` |
| C-S229-LMHEAD-1 | `lm_head.weight` PRESENT (untied) verified via `named_parameters()` before `lm_head_module='lm_head'` set |
| C-S229-PADTOKEN-1 | `pad_token_id == eos_token_id == 2` asserted |
| C-S229-MODULE-1 | All four MEMIT module-path templates resolve to real named modules on `MistralForCausalLM` (verified Cell 1.5: down_proj shape [4096,14336]) |
| C-S229-CHECKPOINT-1 | Mistral Checkpoint #1 within-session determinism: drift 0.00e+00 / 0 top-1 mismatch across 38 probes |
| C-S229-HFHOME-1 | `HF_HOME=/workspace/hf_cache` (D-S25-8) is a Cell-0 prerequisite — model cache MUST be on NV, not the 20 GiB container disk (caught a 100%-full container-disk OOM at first load) |

---

## §5. Open Questions

### §5.1 Resolved at S2.29

| ID | Resolution |
|---|---|
| OQ-V12-T-BRANCH-1 | Mistral-7B-v0.3 base, revision caa1feb0 pinned programmatically |
| OQ-V12-T-BRANCH-2 | Architecture-structural field set derived via `named_parameters()`: untied lm_head, n_layers=32→v_loss_layer=31, module paths verified |
| OQ-V12-T-BRANCH-3 | Reference band `[4..8]` adopted (EasyEdit; Axis-9-validated equivalent); no re-sweep |
| OQ-V12-T-BRANCH-4 | **THE class-changing question — RESOLVED: signature reproduced on Mistral → G (base-decoder-LM-general)** |
| OQ-S229-MISTRAL-TOP1-1 | Mistral natural top-1 = his/his/life/the/her — same function-word class as Llama (edit has the same job) |
| OQ-S229-HARP-1 | harp 2-token on Mistral (proxy required, as Llama); additionally violin + flute fragmented (STRICT→PROXY) |
| OQ-S229-COV-TIME-1 | ~18 min/layer (91.1 min full band) — slightly above the 9–15 min projection (8B-width intermediate dim) |
| OQ-S229-VRAM-1 | 21.3 GiB peak — fits under 24 (tightest headroom of any arm; §2.3 projection confirmed) |

### §5.2 Carried forward / opened

| ID | Status |
|---|---|
| OQ-S229-1 | `mom2_update_weight=15000` calibration on Mistral — PROVISIONAL inheritance; re-tuning out of scope for the single-variable port (a deeper arm, not pursued; 0/5 is the canonical-hparam result) |
| OQ-S225-BASE-INSTRUCT-1 | Instruct-vs-base generalization — still open (orthogonal axis) |
| OQ-V12-T-BRANCH-5 | Cross-arch CLEAR follow-ups — INAPPLICABLE (no CLEAR occurred); within-regime sweep stays deprioritized |
| OQ-S230-QWEN-FRAG-1 (NEW) | Qwen target tokenization must be re-classified fresh; prefer single-token targets for the integrity subset |

---

## §6. Interface Contracts

| ID | Disposition at S2.29 |
|---|---|
| IC-S23-4 | Copy-Unmount HARD gate — VALIDATED on Mistral (drift 0.00e+00 ×2); **6th config, first non-Llama** |
| IC-S24-4 | Trial protocol — Route-A single confirmatory replicate (not full 5×3) per 0/5 discipline |
| D-S215D2-VERDICT-INTEGRITY-1 | {cfb-v3-001/002/005} subset — 001+002 are STRICT single-token on Mistral; carry the load-bearing read at full strength |

---

## §7. Verdict Surface (load-bearing data)

```
fact         target  cls     pre_P     post_P    top1_post   internal_gain   verdict
cfb-v3-001   guitar  STRICT  8.15e-03  3.38e-04  his         ~4000×          FAIL
cfb-v3-002   piano   STRICT  1.01e-03  1.84e-04  golf        ~2000×          FAIL
cfb-v3-003   violin  proxy   7.57e-04  3.11e-03  the          ~550×          FAIL
cfb-v3-004   harp    proxy   2.63e-03  3.92e-04  basketball   ~240×          FAIL
cfb-v3-005   flute   proxy   8.55e-03  3.50e-03  the          ~430×          FAIL
─────────────────────────────────────────────────────────────────────────────
consistency PASS: 0/5  |  signature_reproduced: True  |  P_max: 3.50e-03
trial 0 = trial 1 (confirmatory, bit-identical)  |  unmount drift: 0.00e+00 ×2
```

The two STRICT facts (guitar, piano — both in the verdict-integrity subset) fail at full strength with no proxy weakness. Tiger Woods → `golf` (the model reaches for the real association over the injected one). Internal gain confirmed on every fact; external miss of 2–4 orders of magnitude.

---

## §8. Infrastructure Notes (reusable for S2.30 Qwen)

1. **HF_HOME on NV is a hard Cell-0 prerequisite (C-S229-HFHOME-1).** Container disk is 20 GiB and fills on a single model pull; `HF_HOME=/workspace/hf_cache` + `HF_HUB_CACHE=/workspace/hf_cache/hub` set BEFORE any HF import. Caught a 100%-full-disk OOM at first Mistral load; the v0.1 runbook draft should have carried this explicitly (v0.2 codification note).
2. **Mistral is ungated (Apache-2.0).** No license acceptance needed — unlike Llama. Qwen gating to be checked at S2.30 entry (Qwen-7B is typically Apache-2.0/Tongyi-Qianwen-license, likely ungated, verify).
3. **Stale-kernel VRAM reclaim.** Found an idle ipykernel holding ~8 GiB; `kill <pid>` reclaimed to 24210 MiB free. The Mistral edit peaks at 21.3 GiB — a clean card is required (the GRACE/sweep arms leave kernels resident). Reclaim is a pre-load step.
4. **TOKENIZERS_PARALLELISM=false** — set at notebook top to silence the fork warning during cov compute (cosmetic; v0.2 Cell-0 note).
5. **Engine reuse pattern.** The live-patched Llama engine (SHA 80426fd9, working tree at `/workspace/memit_dry_run/memit/`) is byte-identical across all axes and reused directly; P-4 (Required for Mistral AND Qwen) already live. Qwen needs the same Cell-1.5 module introspection + Pad-Token re-derivation, no new engine work.

---

## §9. Operator-Guidance Register (carried verbatim for S2.30, per S2.24 §9)

Zero-ML-background register, one cell at a time, label Surface A (pod) / Surface B (notebook), explain WHAT/WHY + expected healthy output before each cell, frame a null result as signal. Claude makes all calls and proceeds; surfaces only irreversible ops (model pull, cov compute, NV-destructive ops) for confirmation. This register held throughout S2.29 and carries forward verbatim.

---

## §10. S2.30 Entry Preconditions (Qwen confirmation arm)

**ALL routing preconditions SATISFIED.** S2.30 = T.3-β-QWEN — MEMIT on a second non-Llama family (Qwen-7B), confirmation arm for G (not a class-change candidate). Reuses the T.3 scaffold proven this session.

Read order: this summary → `framework_finding v1.4 §2.4` (cross-architecture idiom) + `§4` (Qwen routing) → `t_branch v1.3 §6'''` → `t3_mistral_7b_memit_runbook v0.1` (structural template) → cfb-v3 + probe-set-v3 (held verbatim).

Derive at entry: Qwen HF revision SHA + license check; `tie_word_embeddings` check (Qwen-7B is untied — likely `lm_head` form); `n_layers` → `v_loss_layer`; MLP down-proj module-path templates via `named_parameters()` (Qwen uses `model.layers.{}.mlp.down_proj` — verify); EasyEdit Qwen reference band; fresh cov caches; fresh determinism chain (Checkpoint #1 on Qwen); probe token IDs re-resolved against Qwen tokenizer (re-classify STRICT/PROXY; prefer single-token targets for integrity subset per OQ-S230-QWEN-FRAG-1).

Decision matrix at close: Qwen `0/5` + signature reproduced → G near-decisive (ceiling across architecturally-distinct base decoder LM families) → external-validity arms (Instruct, KnowEdit) become the frontier. Qwen CLEARS → G narrows to Llama-lineage decoder LMs → architecture-geometry question re-opens.

---

**S2.29 CLOSED 2026-06-15.** Axis 10 confirmed; ceiling promoted L→G; Qwen confirmation arm routed.
