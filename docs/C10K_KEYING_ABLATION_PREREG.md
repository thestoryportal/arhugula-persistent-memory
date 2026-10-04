# Pre-registration (v2) — keying-locus ablation in the program's own MEMIT engine (D-C10k-keying-ablation)

**Date:** 2026-10-04 (v1 → advisor FIX-FIRST, `logs/claude_c10k_keying_ablation_prereg_review.md`; v2 resolves every item below). **Trigger:** the Route A result (`docs/C10K_ROUTEA_RESULT.md`, F3) attributes the ported AnyEdit's 0/72 paraphrase result to *where the edit is keyed*; R0 and Route A differ in at least six ways, so that attribution is I-INFER. This ablation changes one thing in the program's own engine. **No engine source is touched** (LAW#5). **Advisor review before the run:** v1 above; v2 `logs/claude_c10k_keying_ablation_prereg_review_v2.md`.

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

## 1. Question

Does keying the write at the **prompt's final token** instead of the **subject's last token** remove held-out-paraphrase generalisation in the program's own MEMIT engine, on the same 24 subjects and three paraphrases, with the same z-objective, covariance ridge, band [4–8], dtype and seed?

## 2. Design — 2 × 2, A1 and A2 arms, N = 24, 1 seed, fp16 (the LAW#3-validated c10e harness)

| cell | key locus (`C10_KEY_LOCUS`) | context templates (`C10_CTX_TEMPLATES`) | request | "keying is causal" predicts | "keying is not the cause" predicts |
|---|---|---|---|---|---|
| K1 (= R0) | `subject` | `on` | prompt `The capital of {} is the city of`, subject = country | A1 ≈ 94 / A2 ≈ 98 (gate) | same |
| K2 | `subject` | `off` (identity template only) | same | high; a few points lower at most | same |
| K3 | `last` | `on` | prompt `The capital of <country> is the city {}`, subject `of` | **< 20** | ≥ 80 |
| K4 | `last` | `off` | same | **< 20** (closest analogue to the port) | ≥ 80 |

Mechanics: `experiments/track_c/c10e_bandknob.py` with `HP_CANDIDATE=configs/hparams/qwen25_3b_memit_hparams.json` (unchanged, `fact_token: subject_last`) for all four cells; knobs `C10_KEY_LOCUS` (line 319: rewrites the requests as above) and `C10_CTX_TEMPLATES` (line 161: `off` ⇒ `ctx = [["{}"]]`); `CANDIDATE_NAME=K1..K4`, `OUT=results/c10k_keying_ablation/K{n}.json`. **Declared side effect of the subject-string design:** the engine's KL locality prompt is built from the subject (`compute_z.py:50`, `"{} is a"`), so in K3/K4 it reads `"of is a"`; the KL term then regularises a degenerate prompt. This is the one place K3/K4 differ from K1/K2 beyond the key locus; it is recorded, and a K3/K4 collapse is read as "sufficient in MEMIT", not as exclusive.

**Metrics per cell:** A1 and A2 `para_full` (24 × 3), per-subject count with ≥ 2/3 paraphrases, `canon_full`, `locality_described_as` JS, LAW#5 INERT line, keyed-token index of the first item.

## 3. Pre-registered readings (binding metric = A1 `para_full`; A2 alongside)

- **Gate (LAW#3):** K1 within ±3 pp of R0 on A1 and A2, else HALT (harness drift).
- **Validity per cell:** `canon_full ≥ 90` and keyed token as intended; otherwise INVALID (no reading).
- **F3 CAUSAL — "keying at the prompt's final token is *sufficient* to remove paraphrase generalisation in MEMIT; consistent with F3; not exclusive":** K1 passes the gate, K2 ≥ 80, K3 < 20 and K4 < 20, and K3/K4 described-as JS within 10 points of K1. Then the Route A mechanism keeps its F3 reading and the memory_mirror rule becomes unconditional; option (ii) keeps its rationale.
- **F3 OVERTURNED:** K3 or K4 ≥ 80 with described-as JS within 10 points of K1. F3 reduces to its observation; the rule is withdrawn; option (ii) loses its rationale; the Route A difference lies elsewhere (z-objective, preservation term, projector), to be named in a new prereg.
- **TEMPLATES ARE A FACTOR (no keying claim):** K2 < 80. The templates, not the locus, carry generalisation in this engine; K3/K4 are reported but do not license a keying claim.
- **INTERACTION:** K3 and K4 differ by ≥ 30 pp; reported as such; no rule written.
- **MIXED:** 20 ≤ K3 or K4 < 80 (and K2 ≥ 80); partial dependence; one seed at N = 24 cannot resolve it; no rule.
- A cell whose described-as JS is more than 10 points below K1 cannot support OVERTURNED (bleed guard).

## 4. What this does not test

Multi-token values (A7), the C10 blocker, are out of scope on purpose. Nothing promotes to C10 from this run.

## 5. Cost and order

K1 ≈ 40 min (two arms + LAW#5 at ≈ 20 min per arm, from the R0 log), then K2–K4 ≈ 2 h. Runs after the Route A close-out is committed (`CORPUS/42`); its outcome is recorded as its own decision.
