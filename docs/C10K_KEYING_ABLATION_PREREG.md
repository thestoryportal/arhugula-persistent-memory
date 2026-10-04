# Pre-registration (v3) — keying-locus ablation in the program's own MEMIT engine (D-C10k-keying-ablation)

**Date:** 2026-10-04 (v1 → advisor FIX-FIRST, `logs/claude_c10k_keying_ablation_prereg_review.md`; v2 → advisor FIX-FIRST, `logs/claude_c10k_keying_ablation_prereg_review_v2.md`; v3 resolves both rounds, §0 and §0b). **Trigger:** the Route A result (`docs/C10K_ROUTEA_RESULT.md`, F3) attributes the ported AnyEdit's 0/72 paraphrase result to *where the edit is keyed*; R0 and Route A differ in at least six ways, so that attribution is I-INFER. This ablation changes one thing in the program's own engine. **No engine source is touched** (LAW#5). **Advisor reviews:** v1 and v2 above (both FIX-FIRST, resolved); v3 is the run version.

## 0. v1 → v2 (advisor items)

| item | resolution |
|---|---|
| The engine's `fact_token: last` path is unfinished | **Confirmed by source read:** `memit_dry_run/memit/memit/compute_z.py:217-218` raises `"This is definitely bugged, fix it."` and `:246-247` returns index −1 (which lands on padding in a batch). `fact_token: last` is **not used**; `configs/hparams/qwen25_3b_memit_hparams_facttoken_last.json` is withdrawn. |
| Keyed token may land on padding | Design replaced (§2): the write is keyed at the prompt's final token through the engine's **own `subject_last` path** by naming that token the subject (request prompt `"The capital of Zorbland is the city {}"`, subject `"of"`). `repr_tools.get_words_idxs_in_templates` locates it by template split, not by index −1. **Dry run (tokenizer only, `experiments/track_c/c10k_keying_ablation_dryrun.py` → `results/c10k_keying_ablation/dryrun_keyed_token.json`): keyed token decodes to `" of"` and is the last token for 3/3 subjects, with and without a context-template prefix (idx 9/9 and 16/16); the control keys at the subject's last token (`land`, `il`, `ak`).** Validity criterion kept: the harness prints the keyed index for the first item of every cell; it must be the final prompt token (K3/K4) or the subject's last token (K1/K2). |
| Spurious OVERTURNED through bleed at a shared ending | §3: a cell can support OVERTURNED only if its described-as JS locality is within 10 points of K1's (c10e already reports `locality_described_as`; K1 = 91.9); the paraphrases end on `called` / `is` / `is`, not `of`, so bleed through the keyed token itself is not available, but the rule is kept. |
| Inertness gate does not cover the knobs | The INERT line compares engine-vs-harness apply on one fact with the harness's default settings; it is a sanity check, not a knob test. **LAW#3 gate instead:** K1 runs first and must reproduce R0 (A1 94.4 / A2 98.6, `logs/c10k_route_a_R0_baseline.log`; CORPUS/14 line) within ±3 pp before K2–K4 run. `C10_CTX_TEMPLATES=on` and `C10_KEY_LOCUS=subject` leave the harness byte-for-byte on its previous path (both knobs default to the old code). |
| Outcomes without a reading | §3 adds readings for K2 < 80 (templates are a factor → no keying claim), K3/K4 divergence (interaction), INVALID cells, and the MIXED band at N = 24. |
| CAUSAL over-claims | §3 wording: "sufficient in MEMIT; consistent with F3; not exclusive." |
| Minor | per-subject ≥ 2/3 reported; runtime cited from R0 (3 arms + LAW#5 in 56 min → ≈ 20 min per arm); one seed resolves < 20 vs ≥ 80 only. |

## 0b. v2 → v3 (second advisor round)

| item | resolution |
|---|---|
| Evaluation leakage through the subject string | **Source read:** c10e's evaluation never reads `request["subject"]`: paraphrase prompts come from `PTEST.format(country)` over `FICTION`, described-as locality prompts from `FICTION` (`c10e_bandknob.py:317`), `eval_arm(Vmap)` is keyed by country, and the LAW#5 INERT fact is built separately (`:274-281`). The subject string reaches only the engine's `compute_z`/`compute_ks` through `my_edit(hp, requests, …)`. Validity print added anyway (below). |
| KL side effect; better subject string | **Adopted.** K3/K4 request: prompt `"The capital of {}"`, subject `"<country> is the city of"`. `subject_last` keys the final `" of"`; the engine's KL prompt (`compute_z.py:50`, `"{} is a"`) becomes `"<country> is the city of is a"`, keyed at `" of"` at index 5–7 (never 0) and distinct per request; no batch-identity collision. **Dry run v2 on all 24 subjects × the engine's 6 real context templates (`get_context_templates(model, tok)`) + identity: keyed token `" of"` and last for 24/24 under every template; K1 control keys at each subject's last token** (`results/c10k_keying_ablation/dryrun_keyed_token.json`, `valid: true`). |
| Readings overlap / gaps | §3 rewritten with a precedence order and an UNCLASSIFIED fallback; OVERTURNED now requires **K4 ≥ 80** (the port's closest analogue), with K3 reported. |
| Batch identity collision | removed by the per-country subject string. |
| Label over-claims | **"F3 SUFFICIENT (MEMIT)"** replaces "F3 CAUSAL". |
| Dry run coverage | 24/24 subjects, real templates (above). The harness prints, for item 0 of every cell, the keyed index and decoded token, the request prompt/subject, the three paraphrase prompts, one described-as prompt; the paraphrase/locality strings must be byte-identical across K1–K4 or the cell is INVALID. |
| Minor | A1 = 24 fictional countries → single-token real capitals; A2 = the same subjects → two-token coherent capitals (both as in C10/CORPUS/35–36). The K1 gate is the evidence that the knobs' defaults leave the harness on its old path. ±3 pp at N = 72 is a drift tripwire (≈ 2 items), not a reproducibility claim. |
| Drift (defer behind A7 if option (ii) is not live) | Option (ii) is live in `docs/C10K_ROUTEA_RESULT.md` §5; the run is ≈ 2.7 h local and decides whether a memory rule and (ii)'s rationale rest on evidence. It runs after `CORPUS/42` is committed. |

## 1. Question

Does keying the write at the **prompt's final token** instead of the **subject's last token** remove held-out-paraphrase generalisation in the program's own MEMIT engine, on the same 24 subjects and three paraphrases, with the same z-objective, covariance ridge, band [4–8], dtype and seed?

## 2. Design — 2 × 2, A1 and A2 arms, N = 24, 1 seed, fp16 (the LAW#3-validated c10e harness)

| cell | key locus (`C10_KEY_LOCUS`) | context templates (`C10_CTX_TEMPLATES`) | request | "keying is causal" predicts | "keying is not the cause" predicts |
|---|---|---|---|---|---|
| K1 (= R0) | `subject` | `on` | prompt `The capital of {} is the city of`, subject = country | A1 ≈ 94 / A2 ≈ 98 (gate) | same |
| K2 | `subject` | `off` (identity template only) | same | high; a few points lower at most | same |
| K3 | `last` | `on` | prompt `The capital of {}`, subject `<country> is the city of` | **< 20** | ≥ 80 |
| K4 | `last` | `off` | same | **< 20** (closest analogue to the port) | ≥ 80 |

Mechanics: `experiments/track_c/c10e_bandknob.py` with `HP_CANDIDATE=configs/hparams/qwen25_3b_memit_hparams.json` (unchanged, `fact_token: subject_last`) for all four cells; knobs `C10_KEY_LOCUS` (line 319: rewrites the requests as above) and `C10_CTX_TEMPLATES` (line 161: `off` ⇒ `ctx = [["{}"]]`); `CANDIDATE_NAME=K1..K4`, `OUT=results/c10k_keying_ablation/K{n}.json`. **Declared side effect of the subject-string design:** the engine's KL locality prompt is built from the subject (`compute_z.py:50`, `"{} is a"`), so in K3/K4 it reads `"<country> is the city of is a"`, keyed at the `" of"` position (dry run: never index 0; distinct per request). It still differs from K1/K2's `"<country> is a"`; this is the one difference beyond the key locus, recorded, and a K3/K4 collapse is read as "sufficient in MEMIT", not as exclusive.

**Metrics per cell:** A1 and A2 `para_full` (24 × 3), per-subject count with ≥ 2/3 paraphrases, `canon_full`, `locality_described_as` JS, LAW#5 INERT line, keyed-token index of the first item.

## 3. Pre-registered readings (binding metric = A1 `para_full`; A2 alongside) — applied in this precedence order, first match wins

1. **GATE (LAW#3):** K1 within ±3 pp of R0 on A1 and A2 (94.4 / 98.6), else HALT (harness drift); nothing below is read.
2. **INVALID (per cell):** `canon_full < 90`, or the keyed token is not as intended, or the paraphrase/locality strings differ from K1's → that cell has no reading.
3. **TEMPLATES ARE A FACTOR:** K2 < 80 → templates, not locus, carry generalisation here; K3/K4 reported, no keying claim.
4. **INTERACTION:** |K3 − K4| ≥ 30 pp → reported; no rule.
5. **F3 SUFFICIENT (MEMIT):** K2 ≥ 80, K3 < 20, K4 < 20, and K3/K4 described-as JS within 10 points of K1 → "keying at the prompt's final token is sufficient to remove paraphrase generalisation in MEMIT; consistent with F3; not exclusive". The memory_mirror rule becomes unconditional; option (ii) keeps its rationale.
6. **OVERTURNED:** K4 ≥ 80 (K3 reported) with K4's described-as JS within 10 points of K1 → F3 reduces to its observation; the rule is withdrawn; option (ii) loses its rationale; the Route A difference lies elsewhere (z-objective, preservation term, projector), to be named in a new prereg.
7. **MIXED:** 20 ≤ K4 < 80 → partial dependence; one seed at N = 24 cannot resolve it; no rule.
8. **UNCLASSIFIED:** anything else (e.g. K3/K4 < 20 with described-as JS > 10 points below K1) → reported, no rule.

Per-subject ≥ 2/3 counts are reported beside every `para_full`.

## 4. What this does not test

Multi-token values (A7), the C10 blocker, are out of scope on purpose. Nothing promotes to C10 from this run.

## 5. Cost and order

K1 ≈ 40 min (two arms + LAW#5 at ≈ 20 min per arm, from the R0 log), then K2–K4 ≈ 2 h. Runs after the Route A close-out is committed (`CORPUS/42`); its outcome is recorded as its own decision.
