# Session 2.33 Summary Block — Llama-vs-Qwen Internal-Stage Geometry Probe (HALT — harness bug diagnosed)

**Session type:** Execution (pod-side), diagnostic. No verdict arm — instruments the z-optimization stage. Produced no mechanism localization (blocked by harness bug); produced a fully-diagnosed halt instead.
**Date:** 2026-06-15
**Predecessor:** S2.32 — Qwen CLEAR hardened to finding-grade-and-qualified; engine left PATCHED (P-VRAM-CPU-SOLVE) for S2.33 continuity.
**Successor:** S2.34 (resume — fix the BOS lookup bug, then complete the probe).
**Verdict:** **HALT_DIAGNOSED.** The probe's first arm (Llama compute_z trajectory capture) surfaced a precisely-characterized harness-integration bug — a BOS off-by-one in subject-last fact-lookup for the direct (out-of-pipeline) `compute_z` call. No trajectory data promoted; the harness-correctness gate (Llama endpoints must reproduce framework_finding v1.5 §3) is UNMET and stands as a hard precondition for the session's data.

---

## §1. One-Line Result

The session is a **clean diagnosed halt, not a failure**: the correctness gate (run the well-characterized Llama arm first, check its endpoints against the known v1.5 §3 baseline) caught a harness bug that would otherwise have silently produced a fake "Llama stalls" trajectory. The bug is diagnosed to the token; the fix is scoped but not yet applied (it requires reading engine source not yet read this session, and a science-path change under isolation discipline). The probe resumes at S2.34 from the saved diagnostic state.

---

## §2. What Executed (and what it proved)

**Entry sequence — all clean:**
- Engine state confirmed PATCHED: `grep -c "_cov_cpu" = 3`; `memit_main.py` SHA-256 = `5c0c706a66c385273d0a48ebbb8274a1c31bf3e101ca309e47db9cb8b6c78770` (byte-identical to S2.32). No re-apply needed.
- Manifest divergence confirmed and **deferred** (see §5). Both manifests left untouched.
- Kernel hygiene: `HF_HOME=/workspace/hf_cache`, `os.chdir(ENGINE_ROOT)` before engine import, `globals.yml` present. Verified.
- Llama-3.1-8B loaded fp16, pinned revision `d04e592bb4f6aa9cfee91e2e20afa771667e1d4b`. Pad-token set to `<|end_of_text|>` (id 128001) per C-S232-2. Identity checks all matched (32 layers, hidden 4096, vocab 128256).
- Canonical hparams loaded from `/workspace/architecture_profile/meta-llama_Llama-3.1-8B.json` (note: dots, not underscores — manifest path record was stale). v_loss_layer 31 ✓, knobs canonical (v_lr 0.5, grad_steps 25, mom2 15000, fact_token subject_last, clamp 0.75).

**Source reads (read-only, this session):**
- `memit/compute_z.py` — confirmed the optimizer prints per-step `loss … avg prob of [target] …` every iteration (lines 157–161); early-break at loss < 5e-2 (line 162). Resolves the capture method: read the existing per-step log, no instrumentation needed.
- `memit/memit_main.py` — confirmed `execute_memit` self-restores weights (invariant: model unchanged at function exit, lines 230–233) and that `get_context_templates` (lines 304–323) is the engine's own template generator. This made a **direct, weights-untouched `compute_z` call** the correct capture method (no edit, no unmount, no patch-isolation needed). The live engine source already carries `P-VRAM-CPU-SOLVE` (lines 196–204).

---

## §3. The Bug (fully diagnosed — D-S233-HALT-1)

**Name:** BOS off-by-one in subject-last fact-lookup for the direct `compute_z` call.

**Symptom:** `find_fact_lookup_idx("{} plays the instrument of", "Bo Jackson", tok, "subject_last")` returns **index 3 (` plays`)**. The correct subject-last index is **2 (` Jackson`)**.

**Tokenization (the proof):**

| index | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| token | `<\|begin_of_text\|>` | `Bo` | ` Jackson` | ` plays` | ` the` | ` instrument` | ` of` |
| id | 128000 | 1255 | 13972 | 11335 | 279 | 14473 | 315 |

The subject "Bo Jackson" is indices 1–2; its last token is **2** (` Jackson`). The lookup returned **3** — off by exactly one. Cause: the Llama-3 tokenizer auto-prepends `<|begin_of_text|>` (id 128000) at index 0; the GPT-J-authored `repr_tools` subject-index computation (reached via `find_fact_lookup_idx` for the `subject_last` strategy) does not subtract for that prepended BOS, so every subject index is one position high.

**Consequence:** the optimization anchored the edit key on ` plays` (the verb) rather than the subject. This produced a **non-canonical trajectory** whose endpoints miss the known v1.5 §3 Llama baseline by ~3 orders of magnitude:

| quantity | this (corrupted) run | v1.5 §3 known canonical |
|---|---|---|
| first avg-prob | 1.26e-05 | ~1.6e-08 |
| last avg-prob | 2.83e-05 | ~1e-4 |
| start loss | 11.34 | ~17.96 |
| end loss | 10.59 | ~9.35 |

The corrupted trajectory also showed a discontinuous step-20 cliff (avg-prob collapsing from 1.21e-03 back to 1.62e-05), consistent with the wrong-anchor / malformed-template assembly. It is preserved in the diagnostic artifact for diffing against the corrected run.

**Ruled out this session:**
- `tok.add_bos_token = False` — **no effect.** The slow Llama tokenizer ignores the attribute (reported `N/A`); BOS still at index 0, lookup still returns 3.
- A documented engine patch — **none exists.** Confirmed via patch-canonical search: P-1..P-9 + Pad-Token + Copy-Unmount + P-3'/Device-Map do NOT touch `repr_tools` or `find_fact_lookup_idx`. The fix is not a patch we failed to apply.

**Corroboration the science is fine, the harness is the anomaly:** the prior-session baseline `llama_3_2_3b_baselines.json` records this exact fact with sensible subject-anchored numbers (e.g. `p-cfb-v3-001-cons-3` pre-edit top-1 ` guitar` p=0.265). The canonical pipeline resolves this correctly; only our isolated call is wrong.

---

## §4. Decisions (D-S233-*)

| ID | Statement | Status |
|---|---|---|
| D-S233-LAYERMATCH-1 | Compare each model at its native `v_loss_layer` (Llama 31 / Qwen 27); architecturally faithful — each model runs its canonical config. avg-prob is depth-normalized so cross-model comparison is valid; raw loss read within-model. | STANDS |
| D-S233-BAND-1 | The canonical `meta-llama_Llama-3.1-8B.json` carries a **stale** `layers=[2,3,4,5,6]`. Override in code to the cross-architecture-canonical `[4,5,6,7,8]` (matches Qwen/Mistral arms; z_layer=8 matched to the Qwen comparison numbers). Single auditable band correction; v_loss_layer stays native 31. Per D-S232-BAND-OVERRIDE-1 discipline. | STANDS |
| D-S233-CAPTURE-METHOD-1 | Capture via a **direct `compute_z` call** using the engine's own `get_context_templates` + JSON-loaded hparams. No weight write, no unmount, no patch-isolation. Method is sound; blocked only by the lookup bug. | STANDS (blocked) |
| D-S233-MANIFEST-1 | The two reproducibility manifests have diverged on **content** (each holds sessions the other lacks — NOT a stale subset). No merge/overwrite/delete this session. Merge to a verified union at resume; do NOT write the S2.33 manifest entry into either divergent file until merged. | DEFERRED to S2.34 |
| D-S233-HALT-1 | Halt the capture at a clean diagnosed state (BOS off-by-one). No trajectory promoted. Harness-correctness gate (Llama endpoints reproduce v1.5 §3) is a hard precondition for any data. | RATIFIED |

---

## §5. Carry-Forward / Open Items

1. **Manifest merge (D-S233-MANIFEST-1):** still pending. `/workspace/reproducibility_manifest.json` (sessions pre-S2.6, 2.5b, 2.6, 2.8, 2.15-D2, 2.24, 2.26, 2.27, 2.29 + S2.32 in `entries[]`) and `/workspace/architecture_profile/reproducibility_manifest.json` (sessions 2.18, 2.20, S2.22-CHECKPOINT-1, S2.22; no `entries[]`) must be merged to a verified union. Neither written to this session. The S2.33 entry is NOT yet recorded anywhere — author it into the merged manifest at resume.
2. **Engine state:** left PATCHED (P-VRAM-CPU-SOLVE live, SHA `5c0c706a…`), unmodified by this session. Same carry-forward convention S2.32 used. Pristine restore point is the S2.32 backup if ever needed.
3. **Diagnostic artifact:** `/workspace/architecture_profile/s233_halt_diagnostic.json` holds the full bug state + the corrupted trajectory (for diffing) + config-confirmed-good record.

---

## §6. Resume Instruction for S2.34 (precise)

**Goal:** fix the BOS lookup bug, re-run the Llama arm, clear the v1.5 §3 endpoint gate, then complete the probe (Qwen arm + entanglement Probe B).

**Steps, in order:**
1. **Read `rome/repr_tools.py`** (read-only `cat -n`) — specifically `get_words_idxs_in_templates`, the function `find_fact_lookup_idx` delegates to for `subject_last`. Locate where the subject index is computed and how (or whether) it accounts for a prepended BOS. This is the one source file not yet read.
2. **Determine the canonical fix.** Most likely candidate: tokenize the lookup with `add_special_tokens=False` (so no BOS is prepended at the lookup step), OR a BOS-aware index correction in `repr_tools`. Decide from what the source actually does — do not guess. If the fix is a source change to the science path, apply the **in-session-patch-isolation discipline** (C-S232-CPUSOLVE-1 lineage): isolate against a known result before promoting any verdict produced under it.
3. **Re-run the Llama trajectory capture** (the D-S233-CAPTURE-METHOD-1 cell, with the fix). 
4. **GATE — hard precondition:** confirm Llama endpoints reproduce v1.5 §3 (first avg-prob ~1.6e-08, last ~1e-4, loss ~17.96→~9.35) BEFORE trusting any data or touching the Qwen arm. If endpoints still miss, the fix is wrong — iterate, do not proceed.
5. **Only after the gate passes:** capture the Qwen arm (band [4,5,6,7,8], v_loss_layer 27, z_layer 8; P-VRAM-CPU-SOLVE required for Qwen's wide intermediate), then the entanglement Probe B (per-layer delta-norm vs same-subject biographical drift). Write `z_convergence_trace_llama_vs_qwen.json` and author `framework_finding v1.7` (ADDITIVE).
6. **Resolve the deferred manifest merge** and write the S2.33+S2.34 entries into the merged manifest.

**Specialist routing (unchanged):** memit-specialist (primary), state-consistency-theorist (secondary), framework-spec-writer (artifact authoring). validation-contract-architect inactive (diagnostic, no verdict gate).

---

**S2.33 HALT 2026-06-15.** Clean diagnosed halt on a BOS off-by-one in subject-last fact-lookup (direct `compute_z` call); Llama-3 tokenizer auto-prepends `<|begin_of_text|>` (id 128000), GPT-J-authored `repr_tools` does not account for it, subject index shifts +1 (` plays` not ` Jackson`), trajectory non-canonical (endpoints miss v1.5 §3 by ~3 OOM). No data promoted; correctness gate did its job. Fix scoped (read `repr_tools`; likely `add_special_tokens=False` at lookup, under isolation discipline), not yet applied. Config decisions (LAYERMATCH-1, BAND-1, CAPTURE-METHOD-1) stand; manifest merge (MANIFEST-1) deferred. Resume at S2.34 per §6.
