# 17 — B3 / G6.2 REAL Q4_K_M QUANTIZATION SURVIVAL (the CPU-deployment falsifier)

_Result 2026-06-18. Track-B run, unblocked by A1 (`CORPUS/14`: the batch store is the artifact to quantize) and by the scope-gate resolution (D-SCOPE-1: deployment = edit-offline-GPU → COMPILE → serve-CPU = the batch-rebuild model, so A3 parked and the CPU-deployment falsifier is next). Pre-registered in `G6_G7_PASS_CRITERIA_DRAFT.md` §G6.2 + `EXPERIMENT_RUNBOOK.md` §8 B3. Artifacts: `b3_edit_and_save.py` (produce+save the A1-clean batch-edited model), `b3_expand_native.py` (native pool ≥20), `b3_run.sh` (convert→quantize→smoke→probe→verdict), `b3_probe.py`, `b3_verdict.py`, `b3_margin.py`; results `b3_quant_survival_result.json`, `b3_margin_result.json`; logs `b3_run.log`, `b3_edit_and_save.log`. Engine UNMODIFIED; LAW#5 inertness gate INERT (|Δexpr|<0.05). Real Q4_K_M via self-built `llama.cpp` (CPU build, b-tip), NOT FP4, NOT the crude sim quantizer._

## The question
The end product must run on CPU (Intel target; [[deployment-target-intel-cpu]]), which means real **Q4_K_M** quantization via llama.cpp/LARQL. Does the multi-field, multi-entity **batch** store (A1-clean: 100 edits over 50 entities × 2 fields, single joint AlphaEdit solve) **survive deployment quantization** — do the edited facts degrade no more than the model's native knowledge through the *same* quantizer? This is the literal CPU-deployment falsifier and could genuinely fail (edited band-[4-8] `down_proj` perturbations are exactly the kind of low-rank signal quantization could smear).

## Design (advisor-vetted before the verdict)
- **Store:** reuse the A1 batch path VERBATIM (`my_edit(reqs,"alphaedit",P,cache)` over all 100 records, Genesis-style single joint solve). 99/100 edited facts express in fp16 (matches A1). Saved to HF safetensors → `b3_edited_qwen3b`.
- **Toolchain:** `convert_hf_to_gguf.py` → fp16 GGUF → `llama-quantize … Q4_K_M` (5886 MiB → 1835 MiB, **4.99 BPW** — real Q4_K_M). Probed via `llama-server` greedy `n_predict=1` (top-1 next token), `-ngl 0` (**CPU inference**).
- **Metric (pre-registered G6.2):** of facts CORRECT in GGUF-fp16 (eligible), fraction still correct in GGUF-Q4_K_M = **retention**. Edited target = the counterfactual; native target = the truth. PASS = edited retention ≥ native-country retention − 3 pts. Native = facts of **entirely un-edited entities** (28 entities from the 56+78 screens minus the 50 edited; capital/language/continent) → no edit interference. n=84 native_country (77 fp16-correct), 100 edited (99 fp16-correct) — both clear the pre-registered n≥20 floor.
- **VALIDITY GATE (advisor, load-bearing):** HF-fp16 vs GGUF-fp16 top-1 agreement, **split edited vs native**, gates the verdict — an edit-specific conversion loss could otherwise hide behind a global number. Required ≥95% on edited prompts. Plus a 30-sec smoke (France-capital edit reproduced) before the full probe.

## VERDICT — PASS (edits survive real Q4_K_M deployment quantization)

| measure | value |
|---|---|
| **Validity: HF-fp16 ↔ GGUF-fp16 top-1 agreement** | **edited 100% (100/100), native 100% (90/90)** → conversion faithful; verdict interpretable |
| Smoke (France→counterfactual) | GGUF == HF ✓ (band-[4-8] edit preserved through conversion) |
| **Edited-fact retention (Q4_K_M)** | **100.0% (99/99 eligible)** |
| **Native-country retention (same quantizer)** | **97.4% (75/77)** |
| Native-global retention (self-consistency, small n) | 83.3% (5/6) |
| **G6.2 verdict** | edited 100% vs native 97.4%, **Δ = +2.6 pts** (threshold ≥ −3) → **PASS** |

**The edited multi-field batch store survives real Q4_K_M quantization** — edited facts degrade no more than native knowledge through the same quantizer. The store also returned **correct edits under llama.cpp CPU inference** (`-ngl 0`), a real partial step toward E1.

## Scope & caveats (kept flush with the result)
- **MARGIN CONFOUND (characterized, not just flagged — `b3_margin_result.json`).** MEMIT's `compute_z` optimizes edited targets to high p(target) by construction, so edited facts carry **systematically larger top-1 margins** than native: **edited median 0.979 (mean 0.974, min 0.82, q1 0.966) vs native-country median 0.812 (mean 0.779, min 0.33, q1 0.67).** Larger margin → harder to flip under quantization. So 100% edited retention is **plausibly a margin artifact, not intrinsic robustness parity.** The earned claim is "**edited facts survive Q4_K_M deployment quantization (100%)**" — a valid deployment result — **NOT** the pre-registration's literal "indistinguishable from native knowledge." (This completes the pre-registered `post_p` metric, which `b3_quant_survival_result.json` itself dropped.)
- **B3 ≠ "CPU deployment validated."** B3 validates exactly one thing: Q4_K_M quantization preserves the edits, and llama.cpp CPU inference serves them. The **LARQL `gguf-to-vindex` ingest path + serving on the actual Intel-CPU target = E1, still untested.** Scope this to "quantization survival," not "deployment loop closed."
- **First-token prefix matching** lets multi-token native truths (e.g. "Alg"→Algiers) pass on the first token — *easier* than the single-token edited counterfactuals. Native still scored *lower* (97.4 < 100), so the PASS direction is **conservative**.
- **Native-global 83.3% = 5/6** — n too small to interpret; not evidence of broad-knowledge fragility.
- **Standard scope:** N≤100, Qwen2.5-3B only, Q4_K_M only, one write ordering, single run, **batch store** (the incremental path + A3/BetaEdit remain parked & untested per D-SCOPE-1).

## FORK
PASS → the batch store is **quantization-deployable** at Q4_K_M. Track-B B3 done. Remaining live falsifiers (independent of the parked incremental work): **E1** (LARQL `gguf-to-vindex` ingest + real Intel-CPU serving — the actual deployment loop B3 only partially touched), **B1** (larger-model replication, size-density), **C/G7** (multi-token value robustness), **D1** (capacity law, required for F1). A3/BetaEdit stays parked until incremental online single-fact writes become a confirmed requirement.
