# C10 — Multi-token VALUE expression at the batch path (pre-registration)

**Date:** 2026-06-25 (frozen before build). **Decision-ID:** D-C10-1 (pending). **CORPUS:** 35 (pending).
**Class:** **FALSIFIER — can-fail by construction.** The **co-sharpest write-side falsifier** for the now-fixed deployment target (`local Intel CPU + batch writes`, 2026-06-25). A real local *code/project* DB must hold **multi-token values** (file paths, function names, multi-word domain concepts); the entire evidence base to date is **single-token values** (capital/language → mostly 1 token). C10/G7 in the F1 conditions register; matrix-adjacent to R5/R13 (expression/firing).
**Advisor-refined design (2026-06-25):** (1) run at the **proven N≤100 batch path FIRST** to isolate value-token-length from scale (scale leg = batch-genesis-at-scale, gated on target fact-count, run later). (2) Multi-token **VALUES ≠ the multi-token SUBJECTS** that caused ΔW blow-up in C1-true-scale — **subjects are held single-token / clean across both arms**, so the expected failure mode is **expression fragility (R13/R5-like continuation failure), not solve collapse.** That distinction is exactly why it's worth running.

## Question
At the proven batch-genesis path (Qwen2.5-3B / band[4-8] / AlphaEdit / N≤100 / single-batch), does an in-weight edit express a **multi-token value** (the FULL value sequence) as reliably as a single-token value — or does it fire the first value-token but fail to produce the full continuation?

## Design (within-relation single-vs-multi-token-VALUE contrast; subjects held constant)
Reuses the **verbatim** R13/R5 editing harness (engine UNMODIFIED; LAW#5 inertness gate). Same relation (`capital`), same fixed subject pool (confident-correct, **single-token-clean subjects** — countries from `g6_screen_qwen3b_v2.json`), counterfactual targets drawn from real capitals of OTHER pool countries:
- **Arm SINGLE (control):** target X = a **single-token** capital (e.g., Cairo, Paris). N edits, one batch genesis.
- **Arm MULTI (treatment):** target X = a **multi-token** capital (e.g., "Cape Town", "Phnom Penh", "Ulaanbaatar", 2–5 tokens). N edits, one batch genesis on the **same subjects** (separate run; weights restored between arms).
N per arm = 24 (proven R13 scope); both arms identical except value token-length.

## Metrics (the NEW piece vs R13 = FULL-SEQUENCE expression, not first-token only)
Per edited fact, on the canonical prompt and on 3 held-out paraphrases:
- **first_token_top1** — top-1 of the first value token (R13's metric; isolates "did the edit land at all").
- **full_sequence_match** — greedy-decode `len(target_tokens)` tokens; exact match to ALL target token ids (**the C10 headline**).
- The **within-arm gap** `first_token − full_sequence` in Arm MULTI = the continuation-failure signature.
NATIVE control (unedited real capitals) confirms probes valid, as in R13.

## Pre-registered criteria (frozen; symmetric)
Let S = Arm SINGLE full_sequence rate (canonical), M = Arm MULTI full_sequence rate, M1 = Arm MULTI first_token rate.
- **C10 SATISFIED-for-batch-path** iff M ≥ 85% AND (S − M) ≤ 10pp → multi-token values express reliably at N≤100 → the batch+CPU DB can hold them (this condition stops being a blocker for the target).
- **C10 FALSIFIER FIRES** iff (S − M) > 15pp AND M1 ≈ S (first-token lands but full value doesn't) → **multi-token-value expression is FRAGILE** (continuation failure) → a real local code/project DB cannot reliably hold multi-token values with this recipe → **sharpens the F1 verdict for the fixed target** (a new must-fix condition: multi-token write robustness, e.g., AnyEdit-style multi-token editing).
- **AMBIGUOUS** (between the bands, or M1 also low = the edit didn't land) → CHARACTERIZATION; report the curve by token-length, no promotion.
**Pre-committed expectation (stated to avoid post-hoc):** advisor predicts **fragility** (M1 ≈ S but M ≪ S) — the edit sets the first object token strongly; the multi-token continuation relies on the model and decays. A result CONTRADICTING this (M ≈ S, robust multi-token) is the more favorable outcome and is equally informative.

## Scope / caveats
N≤100 / 3B / band[4-8] / AlphaEdit / capital relation / 1-seed / HF-fp16 level. **Isolates value-token-length only** — scale (batch-genesis-at-scale) is a separate gated leg; **Q4_K_M survival of multi-token values is a follow-up** (this run is HF-level expression/firing, the core C10 question). Subjects single-token-clean (no C1 subject-blowup confound). NOT a spec falsification of the whole spec; a scoped write-robustness falsifier for the fixed target. advisor before the verdict (mandated). Cross-family at promote gate if it fires decisively.

## ⭐ ADDENDUM (2026-06-25, post-Run-1, advisor-corrected) — the BINDING test is the NOVEL-insert run
Run 1 (counterfactual targets, `results/c10_multitoken_value.json`) **must NOT be reported as SATISFIED.** Two corrections (advisor):
- **Floor effect, not confound (and the contrast IS clean).** The counterfactual prior is held constant across arms, so single-vs-multi *does* isolate token-length — but both arms are **floored** on the usable (paraphrase) metric (SINGLE 7/24 items fire, MULTI 3/24; 7 vs 3 n.s., Fisher p≈0.3). Floored → **underpowered**, so a real token-length penalty couldn't show. Fix = **lift the floor**, not remove a confound.
- **Canonical full-match is near-tautological — downgrade hard.** `compute_z` optimizes the full target sequence on the canonical prompt; greedy-decoding that same prompt back is a **training-fit** check, not generalization. SINGLE=MULTI=100% on canonical shows only "the AlphaEdit solve can fit a multi-token target (not just the first token)" — a weak mechanism positive; it does **NOT** refute continuation-fragility in any deployment-relevant sense (the only place fragility matters — held-out prompts — is exactly where Run 1 floored). **The pre-reg above mis-specified SATISFIED against the canonical metric — contradicting this very doc's own R13 citation ("trained-prompt over-reports; L2 must use held-out paraphrases"). Owned.**

**BINDING criterion (Run 2 = NOVEL-insert, the representative regime for a fresh code/project DB whose values have no pretrained competitor):** subjects = the proven R5 `FICTION` pool (novel, no-prior; held constant across arms), values = single-token vs multi-token **novel** mappings; binding metric = **held-out-paraphrase FULL-SEQUENCE match** (usable knowledge, off the floor — R5 proved novel single-token inserts are paraphrase-robust ~100%). Let Ns = NOVEL_single paraphrase-full rate, Nm = NOVEL_multi:
- **C10 SATISFIED-for-batch-path** iff Nm ≥ 85% AND (Ns − Nm) ≤ 10pp → multi-token novel values are robust → the batch+CPU DB can hold them.
- **C10 FALSIFIER FIRES** iff Ns high (off the floor) AND (Ns − Nm) > 15pp → multi-token values degrade *usable* knowledge → new must-fix condition (e.g. AnyEdit-style multi-token editing).
- Restore R13's fuller **LAW#5 gate** (p-delta AND locality), not p-delta alone. Pre-edit base controls (canonical + paraphrase ~0) confirm the fictional subjects carry no prior. Report **one combined C10 entry** covering both runs.

## Artifacts (to produce)
Pre-reg: this file (frozen). Runner: `experiments/track_c/c10_multitoken_value.py` (adapts r13). Result: `results/c10_multitoken_value.json`. Analysis: `CORPUS/35_C10_MULTI_TOKEN_VALUE.md`. Then propagate D-C10-1 to all canonical trackers + `closeout_check.py D-C10-1`; update F1 C10 row.
