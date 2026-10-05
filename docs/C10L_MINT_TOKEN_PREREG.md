# Pre-registration (v1) — option (iv): mint one vocabulary token per coined value, with the initialisation comparison (P-iv) and the step-zero recall probe (I-11) (D-C10l-mint)

**Date:** 2026-10-05 (v1, drafted after the research arc `docs/INFRANODUS_RESEARCH_ARC_2026-10-05.md` §1 I-3/I-11, §10 P-iv, §11 Q1–Q2, and D-C10k-rulings-1 ruling 3: a minted token is a Git/.vindex-owned artefact and option (iv) may run). **Status: DRAFT — advisor review pending; nothing runs before the review is folded in as §0.** **Decision-ID (proposed):** `D-C10l-mint`. **E2e-map cell:** §8.9 write/firing × §7.1 syntax/semantics boundary (the token is an artefact owned by the ledger side). **Class:** falsifier (can fail); it is the "span vs novelty" test the sweep recommended (`docs/PRIOR_ART_SWEEP_2026-10-04.md` §10.2 (iv) row and §9.2). **Model / harness:** as in `docs/C10L_COVGEOM_SPARSEBAND_PREREG.md` (Qwen2.5-3B fp16 MPS, `c10e_bandknob.py`).

## 0. Advisor items (to be filled before any run)

_(empty in v1)_

## 1. Question

C10's wall is either the **span** (a value that is 4–6 tokens long cannot be realised token by token through the band) or the **novelty** (a coined value has no prior, so even a one-token write of it would fail). Minting one new token `ĥ` per coined value makes the value single-token and keeps it novel; it separates the two. The sweep's prediction (§10.2 row): A7 minted ≥ 90 % held-out if the wall is the span.

Two things the research arc added, both now part of the design: **(P-iv)** the sweep's init recipe (mean of constituent-token embeddings) is shown degenerate by *Grounded Token Initialization* (arXiv 2604.02324: all new tokens collapse into one low-rank subspace that fine-tuning does not fully recover), which for 24 minted values would recreate CORPUS/43's collinearity at the embedding; **(I-11)** no paper measures whether a freshly initialised token can be emitted at all before training (arc §11 Q1); the step-zero rank probe is therefore the program's own and runs before any write.

## 2. Model facts that fix the design (checked 2026-10-05)

- `config.json` (snapshot `3aab1f19…`): `tie_word_embeddings: true`, `vocab_size: 151936`, `hidden_size: 2048`. The input embedding matrix is also the output head; the hparams already point `lm_head_module` at `model.embed_tokens`. **One row per minted token serves both reading and writing.**
- `tokenizer.json`: 151,643 vocabulary entries + 22 added tokens = 151,665 ids (max id 151,664). **271 spare embedding rows exist** (151,936 − 151,665). Minting ≤ 271 tokens needs **no resize**: register the token in the tokenizer (`added_tokens`) at the next free id and write its row. The weight matrix shape is unchanged, so the GGUF converter sees the same tensor shapes; only the tokenizer files change (P4 below checks the converter honours them).
- Minted rows are an artefact: they are saved as `results/c10l_mint/minted_rows.safetensors` + the modified tokenizer files, hashed, and listed in the result JSON; they are **not** committed into the engine or the model snapshot (D-C10k-rulings-1 ruling 3: ledger/.vindex-owned).

## 3. Premise checks (blocking)

- **P1** — fingerprint PASS; LAW#3 baseline reproduction of the harness's recipe A (as in the covgeom prereg P2) — shared with that prereg if run in the same session.
- **P2** — adding tokens to the tokenizer and writing spare rows does not change any pre-existing logit: for 50 held-out prompts, top-20 ids and probabilities before vs after registration are identical to fp16 tolerance (the new rows are reachable only if their logits exceed others; verify they do not for existing prompts — see I-11 "cannibal" below).
- **P3** — `compute_z` on a single-token target `ĥ` runs to its usual convergence (`c10d_zprobe.py`-style probe: full-target prob ≥ 0.98 at 25 steps for ≥ 22/24 values); otherwise the write cannot be attributed.
- **P4 (deployment, gated on §6 PASS/LEAD only)** — `convert_hf_to_gguf.py` (B3 toolchain, CORPUS/17) carries the added tokens: GGUF-fp16 vs HF-fp16 top-1 agreement on the 24 edited prompts = 24/24, and `llama-server` tokenises the coined string to `ĥ`. If the prebuilt `b11382` cannot, that is a deployment finding, recorded, not a science halt.
- **P5** — alternative tokenisations: the binding metric is "top-1 id at the value slot is `ĥ`" on held-out paraphrases (single-token, so full-sequence = first token). The *string* readout (decode the greedy continuation until a stop and compare to the coined string) is reported alongside; a model that emits the original multi-token spelling instead of `ĥ` is a **miss** on the binding metric and a hit on the string metric, and the two are kept apart (arXiv 2609.29045).

## 4. Step 0 — initialisation and the step-zero probe (no write; one model load)

**Values:** the 24 A7 coined-coined values the harness builds (`V_A7`, e.g. "Vindex Vask"; mean 5.5 tokens, CORPUS/36). One minted token per value, string = the coined value with its leading space, ids 151,665–151,688.

**Three initialisations of row `E[ĥ]`, each as a separate copy of the 24 rows:**
- (M) **mean** of the constituent-token embeddings (the sweep's spec; P-iv predicts collapse);
- (G) **contextual readout, norm-matched**: run the coined value's own tokens through the frozen model inside the canonical frame, take the final-layer hidden state at the value's last token, map it to embedding space through the tied head's geometry (least-squares projection onto the embedding matrix's column space), and rescale to the mean row norm of the 151,643 base rows. This is the trained-free analogue of Token Distillation's target (the model's own multi-token representation, arXiv 2505.20133) and avoids the hypernetwork of HYPEROFA (2504.21018);
- (N) **matched-norm random** (control for the probe).

**Probe I-11, per init, per value, before any write:**
- rank and probability of `ĥ` at the value slot on `CANON` and on the three `PTEST` paraphrases, and in 10 unrelated prompts;
- classification: **dead** (never in top-1000 anywhere), **cannibal** (top-1 on ≥ 3/10 unrelated prompts), **shadowed** (rank just below one of its own constituent tokens on the canonical prompt), **free** (none of the above).

**Probe P-iv, per init:** pairwise cosine (mean, min, max, fraction > 0.9) and participation-ratio effective rank of the 24 minted rows (the CORPUS/43 keygram `stats()` applied to embeddings, `c10k_keying_ablation_keygram.py:13–17`); the same statistics for 24 random base-vocabulary rows as a reference.

**Pre-registered readings of step 0:**
- (M) is expected **collapsed** (mean pairwise cosine > 0.9, effective rank < 3) — if so, P-iv is confirmed on this model and (M) is run in §5 only as the negative control, not as a candidate.
- An init with ≥ 20/24 **dead** tokens is not writable and is dropped before §5 (nothing to attribute).
- An init with ≥ 3 **cannibal** tokens fails P2 and is dropped.
- The init(s) with the most **free** tokens and effective rank ≥ 12 proceed to §5. If none qualifies, **HALT**: option (iv) has an initialisation problem to solve before a write makes sense (recorded as a finding; next init to try is written in the halt note, one fix only).

Output `results/c10l_mint/step0_probe.json`; script `experiments/track_c/c10l_mint_step0.py` (new, harness-side; no edit).

## 5. Behavioural arms (harness, N = 24, one seed, fp16, baseline hparams `[4,5,6,7,8]`)

| arm | value representation | init | what it answers |
|---|---|---|---|
| **A7-multi (baseline)** | the 4–6-token coined string | — | reproduces CORPUS/36–39 (15–27 % `para_full` envelope) |
| **A7-mint-G** | `ĥ` (single token) | G | **the span-vs-novelty test** |
| A7-mint-M | `ĥ` | M | negative control for P-iv (collinear rows) |
| A7-mint-N | `ĥ` | N | does the write succeed on a meaningless but well-separated row (pure novelty) |
| A1 single real (control) | real capital, single token | — | harness control, ≥ 58/72 |

The write is the harness's subject-keyed `my_edit` with `target_new = " " + coined_string` tokenising to `[ĥ]`. Metrics: `canon_full` (/24), **`para_full` (/72, binding)**, `locality_described_as`, the two S-3 axes from the covgeom prereg (L1 real-country flips /12; `delta_norms`), the string readout (P5), and **post-write I-11** (does `ĥ` become cannibal after the write — the minted-token form of frame bleed).

## 6. Pre-registered readings (first match wins; arm A7-mint-G against A7-multi from the same run)

- **INVALID:** A7-multi outside the envelope, or A1 < 58/72, or P2/P3 failed.
- **SPAN (PASS for the hypothesis):** A7-mint-G `para_full` ≥ 65/72 (≈ 90 %, the sweep's prediction) with L1 ≤ baseline + 1 and `locality_described_as` ≥ baseline − 3, and post-write cannibal count ≤ 2. → C10's wall is the span; option (iv) is a route; proceed to P4 (deployment) and to the ledger-side design of the minted-token artefact; CORPUS entry after advisor + gpt-5.5.
- **PARTIAL:** 30/72 ≤ A7-mint-G < 65/72 with the locality conditions. → single-token novelty still fails sometimes; compare A7-mint-N: if N ≈ G, the embedding content does not matter and the remaining wall is the write of a novel key-value pair (the admission-test predictors I-4/I-4b become the next instrument); if G ≫ N, initialisation quality matters and the next arm varies the init.
- **NOVELTY (hypothesis falsified for (iv)):** A7-mint-G < 30/72. → the wall is not the span; a coined value fails even as one token; (iv) is closed as a C10 route and the admission test (i) becomes the primary line.
- **TRADEOFF:** `para_full` thresholds met but a locality condition fails, or post-write cannibal > 2 → exchange rate reported; not a route until locality is restored.
- The (M) arm is read only as: collapsed rows → lower `para_full` than G **and** higher post-write cannibal count (the collinearity prediction). If (M) ≥ (G), P-iv's relevance to this model is recorded as not shown.

## 7. What this does not test

Not the lifecycle of a minted token (deletion, overwrite, compaction — C5/C9); not scale (N = 24); not quantisation survival beyond the P4 validity gate (B3 applies at promotion); not whether a minted token should be visible to the user (spec §7.1 is settled by ruling 3). One seed, one model.

## 8. Cost, order, provenance

Order: P1–P3 → step 0 → arms (baseline, G, N, M; A1 inside each run as the harness does) → P4 only on SPAN/PARTIAL-with-G≫N. Step 0 < 30 min; each behavioural run ≈ 25 min. `DECISION_ID=D-C10l-mint PREREG=docs/C10L_MINT_TOKEN_PREREG.md OUT=results/c10l_mint/<arm>.json`. Minted rows and tokenizer files hashed into the result JSON. Halt discipline as in the covgeom prereg.

## 9. Advisor and cross-family

To `tools/claude_advisor.sh` before any run; items folded in as §0 (v2). gpt-5.5 at the promote gate only.
