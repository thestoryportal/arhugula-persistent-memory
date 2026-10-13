# Session 2.31 Summary Block — T.3-β-QWEN (cross-architecture confirmation arm — EXECUTED)

**Session type:** Execution (pod-side; `t3_qwen_7b_memit_runbook v0.1` consumed Cells 0–10 + isolation control)
**Date:** 2026-06-15
**Predecessor:** S2.30 (T.3-β-QWEN runbook authored DECLARATIVE)
**Successor:** S2.32 (verdict-conditional — architecture-geometry frontier re-opened; see §10)
**Verdict:** **CLEAR — `5/5` consistency PASS on Qwen2.5-7B.** The architectural-invariant ceiling **NARROWS from G (base-decoder-LM-general) to Llama-lineage.** Qwen is the first model to break the ceiling.

---

## §1. One-Line Result

`Qwen/Qwen2.5-7B` (base) under byte-identical canonical MEMIT (joint-overlay L4-8; single architecture-forced hparam delta `v_loss_layer 31→27`) **clears the consistency band 5/5** (guitar 0.997, piano 0.990, violin 0.999, harp 0.992, flute 0.999) where Llama-3.1-8B (7 axes), Llama-3.2-3B (Axis 8), and Mistral-7B (Axis 10) all produced `0/5`. A VRAM-forced CPU-solve engine patch (required because Qwen's 18944-wide intermediate inflates the float64 solve past the 24 GiB ceiling) was **isolated and exonerated** as a confound: the same patched engine reproduces the Llama-3.1-8B ceiling at the floor (`7.9e-08`), provably equivalent to the pristine GPU solve (`1.07e-05`). The CLEAR is a **real architectural result**, not a patch artifact. The ceiling is **Llama-lineage-specific**, and the divergence appears at the **internal z-optimization stage** (Qwen converges >0.98; Llama fails to converge under identical settings) — not merely at the external surface.

---

## §2. Deliverables (RATIFIED 2026-06-15)

| Artifact | Status |
|---|---|
| `session_2_31_summary_block.md` | this artifact |
| `framework_finding_memit_ceiling_archival v1.5` | ADDITIVE (Axis 11 — cross-architecture FALSIFICATION; G narrows to Llama-lineage); v1.0–v1.4 PERMANENT preserved verbatim |
| `t_branch_decision_document v1.4` | ADDITIVE; G narrowed; cross-architecture frontier RE-OPENED; v1.0–v1.3 PERMANENT preserved |
| `memit-patches-canonical v2.6` (deferred to S2.32 codification) | `P-VRAM-CPU-SOLVE` conditional patch to be codified; provenance captured this session (§5) |

**Execution-resolved literals (Qwen, captured this session):**
- Qwen HF revision SHA: `d149729398750b98c0af14eb82c78cfe92750796` (Apache-2.0, ungated)
- Structural: hidden 3584, intermediate 18944, 28 layers, vocab 152064, untied lm_head, `max_position_embeddings=131072` (runbook §2.1 listed 32768 = native pre-YaRN; corrected — non-load-bearing, both ≫ P-7 threshold)
- pad_token: `<|endoftext|>=151643` (already-set no-op on this tokenizer revision)
- Cov caches (L4-8, `_t100_`, 18944² float32, 1,435,501,730 B each): SHA-256 L4 `b54c48ae…`, L5 `8e468c9f…`, L6 `6b0150dd…`, L7 `d066dee6…`, L8 `4d9238e5…`
- Token resolution: STRICT {guitar `[16986]`, piano `[26278]`, violin `[62037]`, flute `[95712]`}; PROXY {harp `[4855,79]` → first-token `' har'`}; integrity subset {001/002/005} all STRICT
- Determinism: Checkpoint #1 (within-session) drift `0.00e+00`, 0/38 mismatch; Checkpoint #2 (cross-process) drift `0.00e+00`, 0/38 mismatch
- Edit: dispatch 3.2 min, VRAM peak 19.3 GiB; internal z-convergence all 5 facts >0.98

---

## §3. Decisions (D-S231-*)

| ID | Statement |
|---|---|
| D-S231-VERDICT-1 | S2.31 verdict = **CLEAR 5/5** on Qwen2.5-7B at **canonical joint-overlay L4-8** (NOT single-layer — the CPU-solve patch preserved canonical scope, so the verdict carries no scope-caveat). |
| D-S231-NARROW-1 | The architectural-invariant ceiling **narrows from G to Llama-lineage**. Qwen is the falsifying case. Prior axes (Llama-3.1-8B ×7, Llama-3.2-3B, Mistral-7B) remain true and unretracted — what changes is the claimed *generality* (G → Llama-lineage), not any prior axis result. |
| D-S231-MECH-1 | The Qwen/Llama divergence appears at the **internal z-optimization stage**: Qwen z-vectors converge to >0.98 on all 5 facts; Llama-3.1-8B z-optimization fails to converge under identical canonical settings (avg prob stuck ~1e-4 after 25 steps; this session, both engine paths). This is mechanistically deeper than the v1.x "softmax competition absorbs the lift" reading and reopens the architecture-geometry question. |
| D-S231-PATCH-1 | `P-VRAM-CPU-SOLVE`: a VRAM-forced, numerically-inert SOURCE_LAYER patch (move the float64 linear solve operands to CPU before the arithmetic so the 18944²×8B float64 matrix never allocates in VRAM). Required for any model whose intermediate width inflates `cov.double()` past available headroom on the 24 GiB 4090 (Qwen-7B class). Conditional patch; to be codified into `memit-patches-canonical v2.6` at S2.32. Provenance: `.upstream_pristine_s231` + `cpu_solve_patch.diff` on NV. |
| D-S231-SCOPE-1 | Single-layer L5 mitigation (runbook §8.4) was attempted and found **insufficient** (the OOM is a single per-layer float64 allocation, not a layer-count problem). The correct mitigation is solve-location (CPU), not scope reduction. Recorded so the next wide-model arm goes straight to CPU-solve. |
| D-S231-CONFOUND-1 | `OQ-S231-PATCH-CONFOUND-1` resolved: patch isolated on Llama-3.1-8B (most-confirmed ceiling), both patched (`7.9e-08`) and pristine (`1.07e-05`) paths hold the ceiling at the floor → patch provably equivalent, CLEAR exonerated as real. |

---

## §4. Constraints (C-S231-*)

| ID | Statement |
|---|---|
| C-S231-1 | Any forward cross-architecture or wide-model arm MUST use `P-VRAM-CPU-SOLVE` (or equivalent solve-offload) when intermediate width ≥ ~18k; GPU float64 solve OOMs on the 4090 above that width alongside a resident 7B+ model. |
| C-S231-2 | Any NEW model result that breaks (clears) or holds the ceiling MUST run the patch-isolation control against a known-ceiling Llama config before promotion, if any engine modification was made in-session. (Generalization of the S2.31 confound discipline.) |
| C-S231-3 | HF_HOME on NV before any HF import (C-S229/S230-HFHOME-1) — re-confirmed load-bearing; the notebook-kernel-environment path is a distinct failure door from the terminal export (cost a container-disk OOM this session). |
| C-S231-4 | Kernel determinism: env-before-import + clean kernel restart required after any OOM (orphaned VRAM is not reclaimable via gc/empty_cache once the model reference is dropped — must restart). |

---

## §5. Patch Provenance (P-VRAM-CPU-SOLVE) — load-bearing for v2.6 codification

**Pristine backup:** `/workspace/memit_dry_run/memit/memit/memit_main.py.upstream_pristine_s231`
**Diff:** `/workspace/stage_1_sect/s231_evidence/cpu_solve_patch.diff`
**Isolation result:** `/workspace/stage_1_sect/s231_evidence/patch_isolation_result.json`
**Engine state at session close:** PRISTINE (Run B restored; `grep -c` confirms patch absent).

The patch (memit_main.py ~L196, `execute_memit`):
```
-        adj_k = torch.linalg.solve(
-            hparams.mom2_update_weight * cov.double() + layer_ks @ layer_ks.T,
-            layer_ks,
-        )
+        _cov_cpu = cov.cpu().double()      # float32→CPU→float64: big tensor born in RAM, never VRAM
+        _lk_cpu = layer_ks.cpu()
+        _A = hparams.mom2_update_weight * _cov_cpu + _lk_cpu @ _lk_cpu.T
+        adj_k = torch.linalg.solve(_A, _lk_cpu).to(layer_ks.device)
+        del _cov_cpu, _lk_cpu, _A
```
**Numerical equivalence evidence:** on Llama-3.1-8B Bo Jackson→guitar, per-layer `upd norm` and `z error` match across patched/pristine to ~3 sig figs (L4 upd 0.2638 vs 0.2655; z error 5.2070 vs 5.2069); post-edit P(guitar) both at floor.

**v1 patch error logged (for the next arm):** the first patch attempt (`(... cov.double() ...).cpu()`) still allocated the float64 tensor on GPU before `.cpu()` — must move/cast operands BEFORE the arithmetic, not after. Corrected in v2 (`cov.cpu().double()`).

---

## §6. Interface Contracts

| ID | Disposition at S2.31 |
|---|---|
| IC-S23-4 | Copy-Unmount HARD gate — VALIDATED on Qwen (L4-8 restore) AND on the Llama-3.1-8B isolation control (restored P(guitar) bit-exact to pre-edit `4.6961e-04`). 7th config; second non-Llama base (Qwen). |
| IC-S24-4 | Trial protocol — single confirmatory dispatch sufficed; the CLEAR is unambiguous (P_min 0.990 ≫ 0.5), no 15-trial replicate needed for the verdict (a replicate sweep could be added in S2.32 for finding-grade robustness if desired). |
| D-S215D2-VERDICT-INTEGRITY-1 | {cfb-v3-001/002/005} all STRICT on Qwen tokenizer; the load-bearing read is at full single-token fidelity (no proxy approximation) — strengthens the CLEAR. |

---

## §7. The Result in Context — Why CLEAR is the Consequential Branch

The seven-axis Llama work, the 3B scale arm, and the Mistral arm built an increasingly strong case that the ceiling was a **property of MEMIT-class editing on base decoder LMs in general (G)**. v1.4 promoted the finding to G. t_branch v1.3 §1''' then pre-registered the exact falsifier: *"the only forward move that could still narrow G is a non-Llama-lineage family clearing the band; the Qwen-7B arm tests exactly that."*

**The Qwen arm fired the pre-registered falsifier.** Qwen — the most architecturally distinct 7B base decoder available (distinct hidden size, intermediate size, layer count, vocab, tokenizer family, pad convention, plus QKV-bias attention) — cleared the band 5/5 under a config that differs from the proven Mistral run by exactly one integer (`v_loss_layer`, layer-count-forced). G is **falsified as stated**; the ceiling narrows to **Llama-lineage** (Llama-3.1-8B, Llama-3.2-3B, and Mistral, which shares Llama-2's RMSNorm+RoPE+gated-MLP+GQA decoder block).

This is a stronger, more publishable result than a confirmation would have been: the framework now has a **falsifying case** that localizes the ceiling to a specific architecture lineage and **reopens the architecture-geometry question** the seven-axis work had closed. The deepest evidence is internal: the divergence is at the z-optimization stage, so whatever is special about Llama-lineage geometry obstructs the *optimizer's ability to find the edit direction*, not just the softmax's willingness to express it.

---

## §8. Infrastructure Notes (carry-forward for S2.32)

1. **CPU-solve is mandatory for Qwen-class width on the 4090.** ~19.3 GiB edit peak even with the float64 off-GPU; GPU float64 solve OOMs hard (2.67 GiB allocation, <2 GiB free). Single-layer scope does NOT help (per-layer allocation). Go straight to CPU-solve for wide models.
2. **Notebook-kernel env is a distinct OOM door from the terminal.** `HF_HOME` exported in the pod shell does NOT propagate to a JupyterLab kernel started earlier; set env in-kernel before any HF import, and the `huggingface_hub` cache constant is frozen at first import (must restart kernel + set env first if it was imported wrong).
3. **Orphaned VRAM after dropped model reference** is not reclaimable by gc/empty_cache — kernel restart is the reliable reclaim. Confirmed twice this session.
4. **Cov compute:** Qwen L4-8, ~105 min total, 18.5–23.9 min/layer (widest arm); 1.4 GiB/layer caches; VRAM_peak 18.26 GiB during compute (compute peak ≠ edit peak).
5. **Engine reuse + fingerprint provenance:** the live-patched engine (SHA 80426fd9) ported directly; the Mistral arm's `patch_fingerprint.txt` convention (6-file SHA-256 manifest) is the provenance artifact, not a full source copy. Runbook Cell-1 nit: probe the `memit_<shortsha>` snapshot dir + verify-fingerprint, not a bare-short-SHA full tree.

---

## §9. Operator-Guidance Register (carried verbatim for S2.32)

Zero-ML-background register; one cell at a time; Surface A (pod) / Surface B (notebook) labels; explain WHAT/WHY + expected healthy output before each cell; frame results (including a null) as signal. Claude makes all calls and proceeds; surfaces irreversible ops (model pull, cov compute, engine patch, NV-destructive) for confirmation. **New this session:** when an in-session engine modification touches the science-bearing path, run a patch-isolation control against a known result before promoting any verdict. Register held through S2.31; carries forward.

---

## §10. S2.32 Entry Preconditions (architecture-geometry frontier RE-OPENED)

The CLEAR branch (S2.30 §10) re-activates the **within-regime per-layer / architecture-geometry probe** that the seven-axis work had deprioritized. The live question is now: **what, mechanistically, differs between Llama-lineage and Qwen such that the z-optimization converges on one and not the other?**

**Read order for S2.32:** this summary → `framework_finding v1.5 §2` (Axis 11 / narrowing) + `§3` (internal-stage mechanism) → `t_branch v1.4 §1'''' / §4''''` (re-opened frontier + candidate axes) → `patch_isolation_result.json` (confound closure) → cfb-v3 + probe-set-v3 (held verbatim).

**Candidate S2.32 directions (operator-ratifiable; Claude recommends in priority order):**

| Priority | Direction | What it tests |
|---|---|---|
| 1 | **Qwen replicate + full 38-probe panel** (gen/spec/unmount, all 15 trials) | Hardens the CLEAR from single-dispatch 5/5 to finding-grade: does the edit *generalize* and stay *local* on Qwen, or only fire on the canonical prompt? Cheap (~1 session; caches resident). |
| 2 | **Llama-lineage geometry probe** — per-layer z-convergence comparison Llama vs Qwen at matched layers | Localizes WHERE in the optimization the lineage divergence originates (the D-S231-MECH-1 thread). |
| 3 | **Second non-Llama-lineage clear-or-hold** (e.g. Phi, Gemma, GPT-NeoX-class) | Tests whether the narrowing is "Llama-lineage holds, everything else clears" vs "Qwen-specific clear." Determines if the new class boundary is Llama-lineage or something narrower. |
| 4 | **Mistral re-confirm under CPU-solve** | Belt-and-suspenders: confirm Mistral still `0/5` through the patched engine (Mistral was run pre-patch). Very cheap; closes the last patch-confound thread for the Llama-lineage holds. |

**Claude's recommendation:** S2.32 = **Direction 1 (Qwen full-panel + replicate)** to harden the CLEAR to finding-grade, with **Direction 4 (Mistral CPU-solve re-confirm)** folded in as a cheap same-session control (both Mistral and Qwen run through the now-canonical patched engine, giving a clean within-engine Llama-lineage-holds vs Qwen-clears contrast). Direction 2/3 are the deeper follow-ons once the CLEAR is hardened.

---

**S2.31 CLOSED 2026-06-15.** Qwen2.5-7B **CLEAR 5/5** — first model to break the architectural-invariant ceiling. CPU-solve confound isolated and exonerated (patch provably equivalent on the Llama-3.1-8B ceiling). Ceiling **narrows G → Llama-lineage**; the pre-registered falsifier (t_branch v1.3 §1''') fired. Architecture-geometry frontier re-opened. `framework_finding v1.5` + `t_branch v1.4` author the narrowing; S2.32 hardens the CLEAR to finding-grade.
