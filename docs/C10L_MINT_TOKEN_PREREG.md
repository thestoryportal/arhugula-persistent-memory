# Pre-registration (v2) — option (iv): mint one vocabulary token per coined value; initialisation comparison (P-iv), step-zero probe (I-11), span-vs-novelty arms (D-C10l-mint)

**Date:** 2026-10-05 (v1 → advisor FIX-FIRST, `results/c10l_mint/advisor_v1.md`; v2 = this file, items folded in §0). **Status: v2 — frozen for the next session; nothing has run.** **Decision-ID:** `D-C10l-mint`. **E2e-map cell:** §8.9 write/firing × §7.1 (the minted token is a Git/.vindex-owned artefact; D-C10k-rulings-1 ruling 3). **Class:** falsifier (can fail): the sweep's span-vs-novelty test (`docs/PRIOR_ART_SWEEP_2026-10-04.md` §10.2 (iv) row, with the P-iv premise note). **Model / harness:** as `docs/C10L_COVGEOM_SPARSEBAND_PREREG.md`.

## 0. v1 → v2 (advisor items and their disposition)

| # | advisor item | disposition in v2 |
|---|---|---|
| 0 / 1 | init G built from the value's hidden state inside the canonical frame can leak the subject→value link; the last-token state predicts what follows; "least-squares projection onto the embedding column space" is the identity | **adopted; G redesigned.** No init is built from any frame containing a subject, and no init uses hidden states. All inits are input-side constructions from embedding rows only (§4). A step-0 paraphrase recall is measured for every init before any write and every arm is read as **post-write minus step-0** |
| 2 | "≥ 20/24 dead means not writable" is wrong; dead is the healthy pre-write state; the danger is a row already live at the value slot | **adopted**: dead is not an exclusion; exclusions are cannibal (§4) and step-0 `para_full` > 2/72 (live before the write) |
| 3 | SPAN bar above the harness's ceiling; A1 differs from mint in two ways (familiar and plausible) | **adopted**: SPAN read relative to A1 in the same run (A7-mint ≥ A1 − 5/72); new arm **A1-rare** (existing single-token values implausible for the relation, no tokenizer change, no init choice) completes the ladder real-plausible / real-implausible / minted |
| 4 | P2 checks almost nothing; the real risk is tokenisation of other prompts | **adopted**: P2 = (a) token ids of every harness prompt identical before and after registration; (b) `tok(" " + coined) == [ĥ]` with the engine's tokenizer object; (c) cannibal check = I-11 on unrelated prompts |
| 5 | collinear rows need a sibling-confusion metric | **adopted**: `para_sibling` (top-1 is a different minted id) reported for every mint arm |
| 6 | read the multi-token baseline per token; cheapest test = first-token paraphrase accuracy of A7-multi | **already answered from CORPUS/39:** A7 `para_first` 56/72 (77.8 %) vs `para_full` 15/72 (20.8 %); CORPUS/36 P(full∣first) = 0.226. The first token lands under paraphrase three times out of four; the span prior is strong before any spend. Recorded as P6; `para_first` and per-position accuracy reported for A7-multi in this run |
| 7 | SPAN over-claims route viability; NOVELTY over-claims | **adopted**: SPAN = "the span is the wall at N = 24; route viability open under capacity (271 spare rows is a hard ceiling before a resize) and lifecycle"; NOVELTY = "(iv) closed with these inits" and "the wall is not the span" only if A1-rare also fails |
| 8 | spare rows have unmeasured starting values (tied head received softmax gradient) | **adopted**: init **Z (as-is)** = the spare rows' current values, measured in step 0 as a reference |
| 9 | effective-rank threshold relative to the base reference; check 2604.02324 collapse at init vs after FT; state the LAW#5 inertness argument | **adopted**: threshold ≥ 0.75 × the 24-random-base-rows reference; 2604.02324 abstract (re-read 2026-10-05): collapse is at initialisation **and** not fully recovered by fine-tuning, so the prereg's use is supported; inertness: minted ids never occur as inputs, so keys and covariance are unaffected — the only weight change outside the solve is the 24 spare rows, which are read as outputs only |

## 1. Question

C10's wall is the **span** (a 4–6-token value cannot be realised token by token through the band) or the **novelty** (a coined value has no prior, so even a one-token write fails). Minting one new token `ĥ` per coined value keeps novelty and removes the span. CORPUS/39 already says the first token of a coined value lands under paraphrase 56/72 times while the full sequence lands 15/72: the span prior is strong. Prediction (sweep §10.2): minted A7 approaches A1's level if the span is the wall.

## 2. Model facts that fix the design (checked 2026-10-05)

- `config.json` (`3aab1f19…`): `tie_word_embeddings: true`, `vocab_size: 151936`, `hidden_size: 2048`; hparams `lm_head_module` = `model.embed_tokens`. One row per minted token serves input and output.
- `tokenizer.json`: 151,643 vocabulary entries + 22 added tokens = ids 0–151,664. **271 spare rows** (151,665–151,935): minting ≤ 271 tokens needs no resize; tensor shapes unchanged. **271 is a hard capacity ceiling for this design.**
- Minted rows and tokenizer files are artefacts: saved under `results/c10l_mint/` with SHA-256s in the result JSON; never committed into the engine or the model snapshot.
- Added tokens are matched before BPE (P2 guards every other prompt).

## 3. Premise checks (blocking)

- **P1** — fingerprint PASS (`d941a9fb…`); LAW#3 reproduction of harness arm A (shared with the covgeom prereg's P2 if run in the same session; otherwise run here).
- **P2** — registration is inert for everything except `ĥ`: (a) for every prompt string the harness feeds (CANON, PTEST, `described as`, L1, L3 prompts, all arms' values), token ids before and after registration are identical; (b) `tok(" " + coined) == [ĥ]` for all 24, using the tokenizer object passed to `compute_z`; (c) I-11 cannibal check on 10 unrelated prompts per init (§4).
- **P3** — `compute_z` on the single-token target `ĥ` converges (full-target probability ≥ 0.98 at 25 steps for ≥ 22/24 values, `c10d_zprobe.py` method); otherwise the write cannot be attributed to the solve.
- **P4 (deployment; only after SPAN or PARTIAL-G≫N)** — `convert_hf_to_gguf.py` (B3 toolchain, CORPUS/17) carries added tokens: GGUF-fp16 vs HF-fp16 top-1 agreement 24/24 on edited prompts; `llama-server` tokenises the coined string to `ĥ`. A failure here is a deployment finding, not a science halt.
- **P5** — binding metric = top-1 id at the value slot is `ĥ` on held-out paraphrases; the string readout (greedy decode, compare to the coined string) is reported beside it; emitting the original multi-token spelling is a miss on the binding metric and a hit on the string metric (arXiv 2609.29045).
- **P6** — the prior: A7-multi `para_first` 56/72 vs `para_full` 15/72 (CORPUS/39); P(full∣first) 0.226 (CORPUS/36).

## 4. Step 0 — initialisations and the step-zero probe (no write; one model load)

**Values:** the harness's 24 A7 coined-coined values; one minted token per value (string = value with leading space), ids 151,665–151,688.

**Four initialisations of the 24 rows, input-side constructions only, no frame, no hidden states:**
- (M) **mean** of the constituent-token embedding rows (the sweep's spec; P-iv predicts collapse);
- (G) **de-meaned mean, norm-matched**: subtract the base-vocabulary mean row from each constituent row, average, add the mean row back, rescale to the mean norm of the base rows — the "all-but-the-top" correction that removes the shared component responsible for collapse (the trained-free analogue of the grounding in arXiv 2604.02324);
- (N) **matched-norm random** (control);
- (Z) **as-is**: the spare rows' current values (reference; item 8).

**Probe I-11, per init and value, before any write:** rank and probability of `ĥ` at the value slot on CANON and the three PTEST prompts, and on 10 unrelated prompts; step-0 `para_full` (/72) per init; classes: **cannibal** (top-1 on ≥ 3/10 unrelated prompts), **live** (step-0 `para_full` > 2/72), **shadowed** (ranks directly below one of its constituents on CANON), **dead** (not in top-1000 anywhere; expected and healthy), **free** (none).

**Probe P-iv, per init:** pairwise cosine (mean, min, max, fraction > 0.9) and participation-ratio effective rank of the 24 rows (`c10k_keying_ablation_keygram.py:13–17` `stats()` on embeddings); reference = 24 random base rows.

**Step-0 readings:** (M) collapsed if mean pairwise cosine > 0.9 or effective rank < 0.75 × reference (P-iv confirmed on this model); any init with ≥ 3 cannibal tokens or any live token is **excluded from the arms** (contamination); dead tokens are not an exclusion. If every init is excluded, HALT with the next init named in the halt note (one fix only).

Output `results/c10l_mint/step0_probe.json`; script `experiments/track_c/c10l_mint_step0.py` (new, harness-side; no edit).

## 5. Behavioural arms (harness, band `4–8`, N = 24, one seed, fp16; each run carries A1 as the harness does)

| arm | value | init | answers |
|---|---|---|---|
| **A7-multi** | 4–6-token coined string | — | baseline (CORPUS/39 envelope: `para_full` [11, 18]/72, `para_first` [48, 62]/72) |
| **A1** | real single-token capital (plausible) | — | harness control (≥ 58/72) |
| **A1-rare** | existing rare single-token word implausible for the relation (24 values chosen from the base vocabulary with frequency rank > 50,000 and not a place name; list frozen in the result JSON before the run) | — | real-but-implausible rung of the ladder; no tokenizer change |
| **A7-mint-G** | `ĥ` | G | the span-vs-novelty test |
| A7-mint-N | `ĥ` | N | does the write succeed on a meaningless, well-separated row (pure novelty) |
| A7-mint-M | `ĥ` | M | negative control for P-iv (collinear rows) |
| A7-mint-Z | `ĥ` | Z | as-is rows (only if Z passed step 0) |

Write = the harness's subject-keyed `my_edit`, `target_new = " " + coined_string` → `[ĥ]`. Metrics: `canon_full` (/24), **`para_full` (/72, binding; reported as post-write minus step-0)**, `para_sibling`, `locality_described_as`, L1 and L3 as in the covgeom prereg, the string readout, post-write I-11 (cannibal count after the write, the minted form of frame bleed), and for A7-multi `para_first` and per-position accuracy.

## 6. Pre-registered readings (A7-mint-G against A1, A1-rare and A7-multi from the same run; first match wins)

- **INVALID:** A7-multi outside the envelope; A1 < 58/72; P2 or P3 failed; or L3 < 48/50 in the candidate.
- **SPAN:** A7-mint-G ≥ A1 − 5/72 and ≥ 30/72, with L1 ≤ baseline + 1, `described_as` ≥ baseline − 3, L3 ≥ 48/50, post-write cannibal ≤ 2, `para_sibling` ≤ 3/72. → **"the span is the wall at N = 24"**; route viability stays open under capacity (271) and lifecycle; proceed to P4 and to the ledger-side artefact design; CORPUS entry after advisor + gpt-5.5.
- **PARTIAL:** 30/72 ≤ A7-mint-G < A1 − 5/72 with the locality conditions. Sub-read by the ladder: if A1-rare ≈ A1 and G ≈ A1-rare → implausibility costs nothing and the residual gap is novelty of the row; if G ≫ N → init quality matters (next arm varies the init); if G ≈ N → row content does not matter and the remaining wall is writing a novel key-value pair (the (i) predictors become the instrument).
- **NOVELTY (with these inits):** A7-mint-G < 30/72. → "(iv) closed with inits M/G/N/Z"; **"the wall is not the span" only if A1-rare also < 30/72** (a real token fails when implausible, so novelty/implausibility, not the span, is binding). If A1-rare ≥ A1 − 5/72 while all mints fail, the finding is about minted output rows, and the next arm is a trained init (Token Distillation style) or a wider ridge, not closure.
- **TRADEOFF:** thresholds met, a locality condition or cannibal/sibling bound failed → exchange rate reported; no route until locality is restored.
- (M) is read only as: collapsed rows → lower `para_full` than G **and** higher `para_sibling` + cannibal; if (M) ≥ (G), P-iv's relevance to this model is "not shown".

## 7. What this does not test

Lifecycle of a minted token (deletion, overwrite, compaction — C5/C9); scale beyond N = 24 and the 271-row ceiling; quantisation beyond the P4 validity gate; user-visibility of minted tokens (settled by ruling 3). One seed, one model.

## 8. Cost, order, provenance, halt

Order: P1–P3, P6 → step 0 (≈ 20 min) → A7-multi + A1 (one run) → A1-rare → mint-G → mint-N → mint-M → mint-Z (if admitted) → P4 only on SPAN or PARTIAL-G≫N. ≈ 25 min per behavioural run. `DECISION_ID=D-C10l-mint PREREG=docs/C10L_MINT_TOKEN_PREREG.md OUT=results/c10l_mint/<arm>.json`; minted rows, tokenizer files and the A1-rare list hashed into the JSON. Halt discipline as in the covgeom prereg. Note: this file's name contains "TOKEN" and is hidden by the repo's `*token*` ignore rule — `git add -f`.

## 9. Reviews

v1 advisor → FIX-FIRST (§0). v2 frozen; further pre-run changes are amendments with their own advisor pass. gpt-5.5 at the promote gate only.

## 10. Amendments (post-freeze; each with its own advisor pass before the affected step runs)

### B1 — init G redefined (all-but-the-top, mean not added back); P3 fails closed; "live" resolved; P1 and provenance made mechanical (2026-10-05, found by the Codex gpt-5.5 implementation review before any mint run; `results/c10l_mint/advisor_impl.md`)

**Gate that forced it:** §4's G as written — "subtract the base-vocabulary mean row from each constituent row, average, add the mean row back, rescale" — is algebraically `mean(R − μ) + μ = mean(R)`: the de-meaning cancels and G collapses to M with a norm rescale. The first implementation copied the text faithfully and therefore did not test the prereg's claimed criterion (remove the shared component responsible for collapse). G is the primary span-vs-novelty arm, so this is a design defect in v2, not a coding slip.

**Change (G):** G = *all-but-the-top* of the constituent rows (Mu & Viswanath 2018, the training-free analogue of the grounding in arXiv 2604.02324): for each constituent row `r_i`, subtract the base-vocabulary mean row `μ` **and** project out the top `k = 20 ≈ d/100` principal directions of the centred base embedding (`torch.pca_lowrank` on the 151,665 × 2048 base block; the directions' SHA-256 goes into the JSON); average the corrected rows; rescale to the base rows' mean norm. **The mean row is not added back.** M, N, Z unchanged. The §6 (M)-reading and the "G ≫ N / G ≈ N" sub-reads keep their meaning; "init quality" now means "collapse component removed" as intended.

**Change (P3 fail-closed):** P3 runs **per init** inside step 0 (the tied lm-head row *is* the init, so convergence depends on it) and is **blocking per init**: an init whose `compute_z` reaches ≥ 0.98 on fewer than 22/24 values is excluded from the arms with reason `P3`, beside the cannibal/live exclusions. The arms driver refuses an excluded init.

**Resolution ("live"):** per token, *live* = ĥ is top-1 on ≥ 1 of its 3 paraphrases before any write (its step-0 recall); per init, the exclusion is the prereg's own numeric rule, `step-0 para_full > 2/72` (summed over the 24 tokens) or ≥ 3 cannibal tokens. A live token that survives the init-level rule is not dropped; every mint arm is read as **post-write minus step-0** (§4, §5), which removes its pre-write recall from the count. "Any live token excludes" in §4 is withdrawn in favour of this numeric rule; both counts are reported.

**P1 and provenance:** step 0 runs `tools/engine_fingerprint.py` itself and halts on FAIL; the arms driver takes `LAW3_REF` = the D-C10l-covgeom run of this session whose arm A passed the P2 envelope (A1/A2 ≥ 68/72 asserted at load) and records it. The minted tokenizer files, the A1-rare list (serialised), the init rows and the G directions are all SHA-256-hashed into `step0_probe.json`; each arm JSON carries the step-0 file's hash. A1-rare's "frequency rank > 50,000" is **declared a proxy**: BPE id > 50,000 (merge order), ASCII lowercase alphabetic, length ≥ 6, seeded shuffle; the first twelve are armored, karakter, physicist, letzten, rebate, guitarist, eminent, intricate, siendo, tavern, dealership, fences (non-English loanwords included; they are existing single tokens implausible for the relation, which is the rung's purpose).

**B1 advisor pass (Codex gpt-5.5, `results/c10l_mint/advisor_b1.md`):** FIX-FIRST on one item, folded: the binding mint score is promoted to a top-level arm field `para_full_binding_n` (= post-write `para_full_n` − step-0 `para_full` of the init) and the mechanical reader `experiments/track_c/c10l_mint_read.py` reads only that field for mint arms. G with the mean removed confirmed as the right primary G; k = 20 frozen (no second binding k); the live rule is sound with the adjusted score; no §6 reopening. §10 is binding over the stale §4 prose for G and "live".

### B2 — operator ruling: run P4 (GGUF) despite the PARTIAL-G≈N read (2026-10-05, after CORPUS/45; ruling D-C10l-rulings-1)

**Ruling (operator, 2026-10-05, in reply to the HIL report):** "Item 1: Yes, run it anyways." The frozen rule in §3 P4 / §8 admitted P4 only on SPAN or PARTIAL-G≫N; the operator overrides it for the deployment question (ruling 3 of D-C10k-rulings-1 makes the minted token a Git/.vindex artefact, so whether it survives the compile is a live question). The science read of CORPUS/45 is unchanged; P4 is a **deployment finding**, reported beside it, never a science halt (§3 P4 as written).

**Design (what P4 measures; one run):** take the best admitted mint arm (N, 46/72) re-run with `MINT_SAVE_DIR` so the edited fp16 HF model and the minted tokenizer are saved from inside the arm (the harness restores afterwards; the saved copy is the artefact), then the B3 toolchain exactly as `experiments/track_b/b3_run.sh` used it on this machine: `convert_hf_to_gguf.py --outtype f16` → `llama-quantize Q4_K_M` → `llama-server -ngl 0` for each GGUF. Readouts: (a) **tokenisation** — `/tokenize` of `" " + coined` for all 24 values returns the single minted id (151,665 + k) in both GGUFs; (b) **fp16 parity** — top-1 next token on the 24 CANON prompts agrees with HF-fp16 (the arm JSON: 24/24) — binding ≥ 24/24 as §3 P4 states, and on the 72 PTEST prompts the GGUF-fp16 hit count is reported against the arm's 46; (c) **Q4_K_M retention** — of prompts correct in GGUF-fp16, the fraction still correct in Q4_K_M (CORPUS/17's G6.2 metric); (d) the 30 L3 and 12 L1 prompts under both GGUFs for locality. A converter that drops or renumbers the added tokens, or a server that splits the coined string, is itself the finding (deployment-blocking for option (iv) until fixed).

**Also recorded (operator question):** the shipped form is a compiled GGUF served by llama.cpp on CPU because that is the spec's deployment realisation the program validated (D-SCOPE-1; `docs/SPEC_E2E_GROUND_TRUTH.md` §I; CORPUS/17–18): the lab harness edits the fp16 PyTorch model on MPS, the product serves a compiled `.vindex`-style artefact through a different runtime. On the M3 Pro both run on one machine (D-HW-1), so Q4_K_M is a size choice inherited from the Intel-CPU era, not a necessity; P4 therefore reports **both** the fp16 GGUF and the Q4_K_M GGUF, and the operator can choose the fp16 GGUF as the shipped form if Q4 costs recall.

### B3 — operator ruling: repeat with a second seed (2026-10-05; ruling D-C10l-rulings-1)

**Ruling:** "Item 2: Repeat it." The advisor's cheapest overturning test for the G-vs-N ordering and the minted-vs-rare contrast. **Design:** a second random matched-norm init N (seed 1 → `inits/N_seed1.pt`, probed by step 0 under tag `_seed1` with its own I-11 / P-iv / P3 gates) and fresh-process re-runs of arms **G**, **N(seed 1)** and **A1-rare** (same frozen list), plus the P4 re-run of N(seed 0) from B2 as a fourth replicate. **Reading (pre-registered before the runs):** the G-vs-N ordering is *supported* only if N ≥ G in both replicates by more than the per-process spread (≥ 5/72); *unsupported* if the sign flips or either difference is < 5; the minted-vs-rare contrast is *supported* if every mint replicate exceeds the rare replicates by ≥ 10/72. Nothing in §6's labels changes; this is a replication readout appended to CORPUS/45 after its own advisor pass. Results: `results/c10l_mint/step0_probe_seed1.json`, `arm_G_rep.json`, `arm_N_seed1.json`, `arm_rare_rep.json`, `arm_N_p4.json`.
