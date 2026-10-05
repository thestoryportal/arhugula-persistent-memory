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

## 6. Amendment (v2, after advisor review `logs/claude_c10k_keying_ablation_amendment_review.md`; pre-registered before the run) — last-token keying at small ridge weights

**Trigger.** First pass: K3/K4 INVALID (canon 29.2 / 25.0 % A1, 4.2 / 8.3 % A2; `docs/C10K_KEYING_ABLATION_RESULT.md`). Both reviewers named the same de-confounder; the **z-probe** (`results/c10k_keying_ablation/zprobe.json`) shows K3-style `compute_z` reaches the target (final target probability ≥ 0.983; K1-style ≥ 0.986; KL term 0.02 in both), so the loss is at the solve. The engine's solve is `(w·C + KKᵀ)⁻¹K` with `w = mom2_update_weight` (`memit_dry_run/memit/memit/memit_main.py:202`, read), so the ridge scales linearly with `w`; the Route A ridge diagnostic puts last-token keys 17–180× under the ridge at `w = 15000`-equivalent geometry (`results/c10k_route_a/memit_ridge_diag.json`, energy-weighted ratio at the program's `w = 5000`: 37–180× is the 15000 figure; the ratio scales with `w`).

**Two separate claims are tested, and kept apart:** (A) *the ridge is a limiter of writability for last-token keys* — a dose-response prediction on canonical fit; (B) *a last-token write that lands does or does not generalise* — the prereg's §1 question, readable only from a valid cell **with a matched subject-keyed control at the same weight**.

**Cells (A1 + A2 arms; A1 binds, A2 is read separately and an invalid A2 does not block an A1 reading):**

| cell | key locus | templates | `w` | runs |
|---|---|---|---|---|
| K3′ | last | on | 500 | always |
| K3″ | last | on | 50 | always |
| K4″ | last | **off** | 50 | always (the port's closest analogue; binding OVERTURNED cell, as in v3) |
| K1′@500 | subject | on | 500 | if K3′ is valid |
| K1′@50 | subject | on | 50 | if K3″ or K4″ is valid |
| K3‴ | last | on | 25 | if K3″ is invalid (clears the 180× ratio: 5000/25 = 200×) |
| K1′@25 | subject | on | 25 | if K3‴ is valid |

Grid {500, 50, 25} is fixed now. Hparams files `configs/hparams/qwen25_3b_memit_hparams_mom2w{500,50,25}.json` differ from the base only in `mom2_update_weight`. All of §3's validity rules apply (canon ≥ 90, keyed token as intended, identical eval strings). Every cell runs whatever the earlier cells show, except the conditional controls as listed.

**Readings (precedence; first match wins):**

1. **Dose–response (claim A):** A1 canon across w = 5000 (29.2, first pass) → 500 → 50 (→ 25). **Rising monotonically and reaching ≥ 90 at some w** → the ridge is *a* limiter of last-token writability (EVIDENCE-SHOWS). **Rising but < 90 at every w run** → consistent with the ridge, grid too coarse: *inconclusive*, not "the ridge is not the limiter". **Flat or falling** → the ridge mechanism is falsified for this failure; the limiter is elsewhere in the solve.
2. **Binding cell for claim B:** the valid last-token cell with the **largest w**; if two valid last-token cells disagree by ≥ 30 pp on A1 `para_full`, read **INTERACTION** (no rule). The matched control is K1′ at that w.
3. **F3 SUFFICIENT (MEMIT, small ridge):** binding cell valid, A1 `para_full` < 20, **and K1′ at the same w ≥ 80** (so a small ridge does not itself remove generalisation, and locality damage at that w does not explain the failure — K1′ carries the same damage). Templates are not addressed by this reading (K3-type cells have templates on; K2's result is about subject keying at w = 5000).
4. **OVERTURNED:** **K4″** valid with A1 `para_full` ≥ 80 and described-as JS within 10 points of K1 (bleed guard); K3′/K3″ reported alongside. A last-token write that lands generalises in MEMIT; Route A's 0/72 has another cause; option (ii) loses its rationale.
5. **CONTROL-FAILED:** binding cell valid with `para_full` < 20 but K1′ at that w < 80 → the small ridge removes generalisation for any key; no keying reading.
6. **MIXED:** binding cell valid, 20 ≤ `para_full` < 80 → no rule.
7. **NO VALID CELL** (all last-token cells canon < 90 through w = 25) → combine with reading 1: if canon rose, "ridge is a limiter but not the only one at w ≥ 25"; if not, "ridge falsified"; in both cases F3 stays I-INFER and the keying question moves to a different harness (option ii).

**Scope note.** Any result at w ≤ 50 is about *mechanism*, not deployment: the ridge is the engine's locality protection and is expected to degrade at these weights (Route A F4). Independently of this amendment, the first-pass writability finding (canon 29 / 25 / 4 / 8 at the operating weight) already supports a practical "key at the subject" rule on engineering grounds; the amendment decides whether F3's *generalisation* claim can be made causal inside this engine.

**Cost:** 3–7 cells at ≈ 20 min each. **Advisor:** v1 of this section → FIX-FIRST (above, resolved here); v2 review `logs/claude_c10k_keying_ablation_amendment_review_v2.md` before the run.


## 6b. Amendment v3 (2026-10-04, after the second advisor round on §6, `logs/claude_c10k_keying_ablation_amendment_review_v2.md`) — discriminator before sweep; the N = 1 cells are the valid last-token cells

**Trigger.** The v2 reviewer returned FIX-FIRST: the §6 sweep assumes the ridge is the limiter, but a second mechanism fits the z-probe equally well and was never named — the 24 last-token keys sit on the same token `" of"` in the same local context and may be near-identical, in which case one closed-form solve must map one key to 24 targets and canon collapses by interference, not by ridge magnitude. The reviewer asked for a minutes-long discriminator (key Gram matrices; single edits at w = 5000) before any sweep. Both were run; the sweep (`tools/c10k_keying_ablation_smallridge.sh`, hparams `mom2w{500,50,25}`) is **not run unless** the single edits fail to land.

**Resolution of the v2 items.**

| item | resolution |
|---|---|
| 1. ratio numbers contradict themselves | `results/c10k_route_a/memit_ridge_diag.json` `ridge_over_key_energy_15000_mean` = 132 / 181 / 65 / 37 / 17 (L4…L8) is at **w = 15000**; the energy-weighted ratio at the program's w = 5000 is 44 / 60 / 22 / 12 / 5.7 for last-token keys and 5.3 / 1.2 / 0.54 / 0.60 / 0.48 for subject keys (`results/c10k_keying_ablation/keygram.json`). The "5000/25 = 200× clears 180×" arithmetic is withdrawn. |
| 2. calibrated prediction | w* = 5000 × (subject ratio ÷ last-token ratio) = 600 / 103 / 124 / 240 / 423 per layer (keygram `w_star_last_matches_subject`). If the sweep ever runs, claim A reads "canon crosses 90 near w* ≈ 100–600", not "rises". |
| 3. claim A over-sounds | narrowed to "consistent with the ridge and not separated from key similarity" unless the discriminator separates them. |
| 4–5. readings favour F3 / precedence broken | apply only if the sweep runs: separate lists for claims A and B; bleed guard measured against K1′ at the same w; UNCLASSIFIED fallback; OVERTURNED readable from the binding cell. |
| 6. bleed probe for ridge-free keys | adopted here for the N = 1 cells (frame-bleed probe below), where it decides what a *landed* last-token write is keyed to. |
| 7. drift | discriminator first; the sweep is conditional (above). |
| 8. tolerances; hparam diff | "non-decreasing within 5 pp" if the sweep runs; `diff` of the three `mom2w*` hparams against the base shows only `mom2_update_weight` and JSON whitespace in the `layers` array (checked 2026-10-04). |

**Discriminator (a) — key similarity (EVIDENCE-SHOWS; `experiments/track_c/c10k_keying_ablation_keygram.py` → `keygram.json`, already in `docs/C10K_KEYING_ABLATION_RESULT.md` §3c).** The 24 last-token keys have pairwise cosine 0.985–0.991 (every pair > 0.9) and effective rank 1.02–1.03 at every band layer; the 24 subject keys have cosine 0.02–0.07 and effective rank 16–23. One key, 24 targets: interference is predicted to dominate the K3/K4 collapse at N = 24, with the ridge second (the small inter-subject differences lie in low-variance directions that the ridge suppresses; w* above is where they would be amplified to the subject keys' ratio).

**Discriminator (b) — single edits (`tools/c10k_keying_ablation_n1.sh` → `results/c10k_keying_ablation/n1/N1_{last,subject}_{0..5}.json`).** Six subjects (`FICTION[0..5]`), A1 values, w = 5000, templates on, one request per run, both loci; the subject-keyed single is the matched control. Each run reports canon (1 item), the three paraphrases, and the described-as JS.

**Timing disclosure.** The chain started at 18:10 as the writability discriminator (reading fixed by the reviewer: singles land → interference; singles fail → ridge). The claim-B reading and the frame-bleed probe below were written at 18:50, when three of the twelve runs were visible (N1_last_0 canon 100 / para 0/3; N1_subject_0 canon 100 / para 3/3; N1_last_1 canon 100 / para 0/3). Those three count toward the criteria; this section pre-registers the reading for the remaining nine runs and for the probe, and says so.

**Readings — claim A (writability at N = 1).**
1. ≥ 5/6 last-token singles land (canon = 100) → the N = 24 collapse is **key interference first**; ridge magnitude is withdrawn as the primary cause at w = 5000; the sweep is not run.
2. 0/6 land → the ridge or the position itself limits writability without interference; the sweep runs as §6 specifies.
3. 1–4 land → mixed; the sweep runs.

**Readings — claim B (generalisation, read only from landed N = 1 cells; A1 `para` out of 3 per subject).**
1. **F3 SUFFICIENT (MEMIT, N = 1):** ≥ 5/6 last-token singles land with para ≤ 1/3 **and** ≥ 5/6 subject-keyed singles land with para ≥ 2/3, with the last-token singles' described-as JS within 10 points of the subject singles'. Wording: "in the program's engine, keying a single write at the prompt's final token is sufficient to remove held-out-paraphrase generalisation that the same write keyed at the subject has; consistent with F3; not exclusive; N = 1, 6 subjects, one seed."
2. **OVERTURNED (N = 1):** ≥ 4/6 landed last-token singles have para ≥ 2/3 → a last-token write that lands generalises; F3 reduces to its observation; the keying rule is withdrawn.
3. **CONTROL-FAILED:** fewer than 5/6 subject singles land with para ≥ 2/3 → no reading.
4. **MIXED:** anything else → reported, no rule.

**Frame-bleed probe (item 6; `experiments/track_c/c10k_keying_ablation_n1_framebleed.py` → `results/c10k_keying_ablation/n1/framebleed.json`; runs after the chain).** For subjects `FICTION[0..2]`, both loci, one edit each at w = 5000 through the harness's own edit path (P computed once; weights restored between edits): after the edit, read top-1 at the twelve Route A real-country frame prompts (`The capital of <Albania…Cuba> is the city of`) and at six never-edited fictional frame prompts (`FICTION[12..17]`), and count flips to the edited value plus real-capital correctness and the real-prompt JS.
- **H-frame (predicted by the keygram):** the landed last-token single flips ≥ 6/12 real and ≥ 3/6 bystander frame prompts to its value; the subject single flips ≤ 1/12 and ≤ 1/6. Then the landed last-token write is a **frame write**, not a subject fact: it fails the paraphrases because it never encoded the subject, and it breaks locality in exactly the neighbourhood the described-as probe does not see. The claim-B label, if reached, is qualified to "a write keyed at the frame token is read from the frame, not the subject".
- **H-subject:** the last-token single flips ≤ 1/12 and ≤ 1/6, like the control → the landed write is subject-specific yet non-transferable; the claim-B label stands unqualified.
- Anything between → reported; the label carries "partly frame-keyed".

**Scope.** N = 1, six subjects (three in the probe), A1 single-token values, one seed, one engine, w = 5000. Mechanism evidence about where a write is keyed; nothing promotes to C10 (A7 untouched). **Cost:** chain ≈ 1.7 h (running); probe ≈ 15 min. **Advisor:** Claude result review v2 and the gpt-5.5 cross-family review on the rendered result doc before `CORPUS/43`.

**§6b post-hoc addendum (2026-10-04 ~20:15, after both result reviews):** the Codex cross-family review asked for the cheapest overturning control — distinct per-subject values at N = 1 (all twelve chain runs had used the value `Beirut`). The frame-bleed probe already yields exactly that for `FICTION[0..2]`; it was re-run for `FICTION[3..5]` (`results/c10k_keying_ablation/n1/framebleed_b.json`), so the probe covers six subjects with six distinct values. Reading, fixed before the second run: if any landed last-token single scores ≥ 2/3 paraphrases, claim B weakens to MIXED; if all score ≤ 1/3 while every subject-keyed single scores ≥ 2/3, claim B stands with the same-value limitation removed. The frame-bleed H-frame / H-subject thresholds apply unchanged across all six.
