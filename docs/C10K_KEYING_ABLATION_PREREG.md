# Pre-registration — keying-locus ablation in the program's own MEMIT engine (D-C10k-keying-ablation)

**Date:** 2026-10-04. **Trigger:** the Route A result (`docs/C10K_ROUTEA_RESULT.md`, F3) attributes the ported AnyEdit's 0/72 paraphrase result to *where the edit is keyed* (last token of the written context vs the subject's last token). The advisor (second review, `logs/claude_c10k_route_a_result_review_v2.md`) correctly notes that R0 and Route A differ in at least six ways, so the attribution is I-INFER. This ablation isolates the keying locus in a setting where everything else is held fixed: the vendored MEMIT engine, with `fact_token` as a native option. **No engine source is touched** (LAW#5: the engine is unmodified; the variable is a hyperparameter plus one harness knob). **Advisor review before the run:** `logs/claude_c10k_keying_ablation_prereg_review.md`.

## 1. Question

Does keying the write at the **last prompt token** (`fact_token: last`) instead of the **subject's last token** (`fact_token: subject_last`) remove held-out-paraphrase generalisation on the program's own engine, on the same 24 subjects and the same three paraphrases, with the same z-objective, projector-free covariance ridge, band [4–8], dtype and seed?

## 2. Design — 2 × 2, A1 and A2 arms, N = 24, 1 seed, fp16 (the LAW#3-validated c10e harness)

| cell | `fact_token` | context templates | expectation under "keying locus is causal" (F3) | expectation under "keying is not the cause" |
|---|---|---|---|---|
| K1 (= R0) | `subject_last` | on (engine default, `get_context_templates`) | A1 ≈ 94 / A2 ≈ 98 `para_full` (known) | same |
| K2 | `subject_last` | **off** (identity template `{}` only) | high, possibly a few points lower (templates add robustness, not locus) | same |
| K3 | `last` | on | **collapses** (predict < 20) | stays ≥ 80 |
| K4 | `last` | off | **collapses** (predict < 20); closest analogue to the AnyEdit port | stays ≥ 80 |

Mechanics: `experiments/track_c/c10e_bandknob.py` run four times with `HP_CANDIDATE` pointing at `configs/hparams/qwen25_3b_memit_hparams.json` (K1/K2) or a copy with `"fact_token": "last"` (K3/K4; nothing else changed), and a new harness env knob `C10_CTX_TEMPLATES=on|off` (off ⇒ `ctx = [["{}"]]` in `my_edit`; the engine's own `compute_z`/`compute_ks` receive the list unchanged). `CANDIDATE_NAME` = K1..K4; `OUT` = `results/c10k_keying_ablation/K{n}.json`. LAW#5 inertness line printed by the harness must read INERT for every cell (it compares engine vs harness apply on one fact and is independent of the knobs).

**Pre-registered readings.** Binding metric = A1 `para_full` (24 items × 3 paraphrases); A2 reported alongside; canonical `canon_full` and described-as JS reported for every cell.
- **F3 CAUSAL (EVIDENCE-SHOWS):** K3 and K4 both < 20 `para_full` on A1 while K1 ≥ 80 (K2 reported). The Route A mechanism and the memory_mirror rule become unconditional; option (ii) (subject-keyed per-token hybrid) keeps its rationale.
- **F3 OVERTURNED:** K3 or K4 ≥ 80 on A1. The keying locus is not the cause of Route A's 0/72; F3 is reduced to its observation (0/72 at three ridges), the rule is withdrawn, and option (ii) loses its rationale; the Route A difference then lies in the z-objective, the preservation term, or the projector (next ablation named then, not now).
- **MIXED (20 ≤ K3 or K4 < 80):** partial dependence; reported as such, no rule written.
- Canonical fit must stay ≥ 90 in every cell or the cell is INVALID (the write failed for an unrelated reason).

## 3. What this does not test

Multi-token values (A7) — the C10 blocker — are out of scope here on purpose: this is a single-variable test of the mechanism claimed in F3, not a rescue attempt. Nothing promotes to C10 from this run.

## 4. Cost and order

Four c10e runs at ≈ 20 min each on the M3 Pro (fp16, LAW#3 harness) ≈ 80 min. Runs after the Route A close-out is committed (`CORPUS/42`), so the ablation's outcome is recorded as its own decision, not folded into Route A's verdict.
