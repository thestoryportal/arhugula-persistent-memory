# Pre-registration — D-C10w-oracle: a merged band-LoRA trained on the 24 coined facts, scored on the C10 harness, as a ceiling measurement (ORACLE MEASUREMENT, NOT A ROUTE) (step 5 of the research pass's recommended sequence; H-13) (v2, 2026-10-07)

**Status: v2.1 — freeze-check fixes applied (2026-10-07); pending freeze-check confirmation.** Nothing has run; no driver exists. Decision-ID `D-C10w-oracle`. Every output of this experiment (title, record files, verdict, CORPUS entry, register row) carries the label **"oracle measurement, not a route"**. A result here can never be promoted as a write-engine result, and a pass does not change C10's status (`results/research_pass_2026-10-06/prereg_stubs.md:62`).

Source lead: research pass 2026-10-06, H-13 (`results/research_pass_2026-10-06/hypotheses.md:135–145`), with H-15 as the stronger oracle not run here (`hypotheses.md:154–162`) and H-30 as the conditional follow-up (`hypotheses.md:309–310`); the step-5 stub (`prereg_stubs.md:59–67`) under the shared contract (`prereg_stubs.md:5–13`); the sequence row (`recommended_sequence.md:25`); the council's H-13 objections (`council_critique.md:7–13`, `:63–79`, `:97–107`, `:128–133`, `:163–168`, `:198–206`, `:238–250`). Lineage: CORPUS/44 ⟨D-C10l-covgeom@af2e38f7⟩ (identical-baseline envelope, `CORPUS/44_C10L_COVGEOM_SPARSEBAND.md:39`; ρ correction, `:43`), CORPUS/45 ⟨D-C10l-mint@a4a6f4c7⟩ (A1 68–72/72 under the write and the one-token mint at 34–46/72, `CORPUS/45_C10L_MINT_TOKEN.md:1`, `:61`), CORPUS/46 Q3 (mint seed range 46/34/36, `CORPUS/46_C10M_DIAG_READPARTITION_EDITINJECT.md:22`), CORPUS/49 (same-frame probe pre-edit 1/6, `CORPUS/49_C10P_TWOPASS_SOLVE.md:12`). Format and conventions follow `docs/C10V_LAYERPICK_PREREG.md` (v2) and `docs/C10U_MINT2_PREREG.md` (v3).

**Operator rulings that bind this design (quoted):**
- **Write-only ruling, D-C10r-rulings-3 (2)** (`EXPERIMENT_RUNBOOK.md:330`, §5.2): *"training per commit defeats the spec's objective; likelihood of deploying it is essentially zero; run it only as a measurement — H-13/H-15 are an oracle measurement, not a route."* The research pass's first decision says the same: *"Any route that needs a training set or a training loop per commit is not a route"* (`HANDOFF.md:7`; ranking criterion 1, `recommended_sequence.md:11`).
- **Step 5 moved ahead of step 4, D-C10r-rulings-9 (2)** (`EXPERIMENT_RUNBOOK.md:342`; queue row `docs/INTEGRATED_QUEUE_2026-10-07.md:19`).
- **Local only**: the M3 Pro, Apple MPS, no CUDA, no rented compute; MPS has no float64 (`experiments/track_c/c10l_mint_lib.py:66`).
- **One GPU run at a time** (`docs/INTEGRATED_QUEUE_2026-10-07.md:43`); the MEMIT engine under `memit_dry_run/memit` stays UNMODIFIED (LAW#5); the LAWs, halt discipline and close-out gate of `CLAUDE.md` bind unchanged.

## 0. Where this sits, and what it is

**The e2e map (`docs/SPEC_E2E_GROUND_TRUTH.md`, binding per `DISCIPLINE.md:30`).** Layer: the **Write Engine** (§8; `SPEC_E2E_GROUND_TRUTH.md:14`), at the cell where the write path's Commit Executor calls MEMIT (§C step 5, `SPEC_E2E_GROUND_TRUTH.md:22–30`). This experiment replaces the MEMIT solve with gradient training, which puts it **outside the spec's write path**: the spec designates MEMIT and excludes full fine-tuning (`research_and_specs/llm-as-database-v1_2-integrated-spec.md:313`). It is an oracle beside the write path, read against the §8.9 bar (`spec:388`). Its readouts mirror the §F split (`SPEC_E2E_GROUND_TRUTH.md:64–65`): storage (training-phrasing exact match, canonical prompt) and behaviour (held-out paraphrase) are separate columns. Nothing in the Schema, Validation, Security, State Consistency or Orchestration layers is touched.

**SPEC-FIRST (`DISCIPLINE.md:32`).** The spec already settles whether training is a write engine: it is not (`spec:313`). That is why this is a measurement and why H-13's spec amendment (`hypotheses.md:142`) is **not pursued**. The council's objections about composition (§8.10 D62), rollback (§8.4), transaction windows (§11.5.1, §11.9), determinism (§12.2) and integrity (§10.2) (`council_critique.md:10`, `:13`, `:99–102`, `:201–204`, `:244`) are objections to H-13 **as a route**. They are listed in §4 as untested and not claimed. They are not run here.

**The question, in the research agent's words:** *"If even training cannot reach the bar on this model, no solver will, and the question becomes the model. If training reaches it, the wall is a missing objective that steps 6 and 7 can supply inside the solver"* (`recommended_sequence.md:25`). **v2 does not adopt that sentence's inferences** (Codex #1): the oracle's count is an attained result of one finite recipe, not an upper bound, so a FAIL does not show that no solver will, and a PASS does not identify a missing objective as the cause. PASS or PARTIAL may motivate steps 6–7 as independently pre-registered tests; FAIL may inform the operator's existing model-axis decision (the ceiling rule, `HANDOFF.md:56`) without settling it (§3).

*Correction carried from `docs/INTEGRATED_QUEUE_2026-10-07.md:38–39`: the sequence's rationale for steps 6–7 ("about 3 percent installed", `recommended_sequence.md:13`, `:27`) is backwards. ρ_c and ρ_p are remaining-residual ratios: about 2.8 % of the target stays unrealised at the keyed position and about 23 % on the mixed-prefix paraphrase proxy, in an offline reconstruction, not a behavioural-run measurement (`CORPUS/44_C10L_COVGEOM_SPARSEBAND.md:25`, `:43`). The gap this experiment measures against is transfer from the keyed position to paraphrases and later value positions, not a write that barely lands.*

**What it can and cannot conclude.** It measures one strong training recipe: LoRA on the five band `down_proj` matrices, every value token in the loss, 20 sealed-safe phrasings, rank 16 with a conditional rank-64 capacity check, and a single-frame variant (O-A7-canon, §2.2) that separates phrasing diversity from the rest. This is an oracle measurement, not a route. It measures attained performance of a predeclared finite LoRA recipe on this fixed benchmark; its count is a reference result, not an upper bound on this model or on other writers. PASS-CEILING means that a merged delta confined to the five specified matrices reaches at least 61/72 held-out prompt successes in the required replications while the named gates pass. It does not mean that all 24 facts pass the per-edge 3/3 rule, that general locality is clean, or that a missing objective has been identified as the cause. PARTIAL-CEILING records the attained counts and gate costs; matching those counts with another writer does not prove objective-gap closure, and exceeding them does not require a model change. FAIL-CEILING means that each evaluated rank's minimum across its two valid, stable seeds is below 30/72. It does not mean that every fitted adapter scored below 30/72. Report all seed counts; this is a recipe-level replication outcome, not a model-capacity bound. It is neither a model-capacity falsification nor evidence that no solver can succeed. PASS and PARTIAL may motivate steps 6–7 as independently pre-registered tests. FAIL may inform the operator's existing model-axis decision, with recipe, representation, optimisation and merge precision still unresolved; it does not independently settle that decision. C10 remains OPEN/BLOCKING and F1 is unchanged. The labels keep their v1 names; "CEILING" names the oracle's role, not a bound.

## 1. Question and hypotheses

- **H-W1 (reachable ceiling):** a merged rank-16 LoRA on `down_proj` L4–8, trained with token-level cross-entropy on every value token over 20 training phrasings that are sealed against the held-out templates, reaches ≥ 61/72 on the A7 held-out full-sequence count with every locality and forgetting gate holding. The mechanism claim, corrected from H-13: the closed form already optimises its target z against **every** value token (`memit_dry_run/memit/memit/compute_z.py:60–65`, `:141–150`; H-13's "no direct objective on tokens 2…N", `hypotheses.md:136`, is false as written, `docs/INTEGRATED_QUEUE_2026-10-07.md:39`), but in one frame and through a weight solve whose keys sit at the subject's last token only (`fact_token` `subject_last`, `configs/hparams/qwen25_3b_memit_hparams.json:5`; `memit_dry_run/memit/memit/compute_ks.py:19–37`; `c10e_bandknob.py:196–201`), so the solve places no constraint at the frame or value positions. The oracle's loss differs in three ways at once: every phrasing (20 frames), every position (ΔW acts on, and is trained through, every token), and iterative fitting. O-A7-canon (§2.2) separates the first from the other two. The oracle also differs in optimiser, precision, and the absence of a write-size or covariance-preservation constraint (§2.4, §2.6), so a PASS does not isolate which change caused it (§0).
- **H-W0 (recipe-level negative):** both valid, stable, replicated ranks (16 and 64) have minimum seed count below 30/72, with the trainer's positive controls passing and every read adapter fitted. This is a negative result for these recipes, not a model-wall hypothesis (§0).
- **H-W2 (trade-off):** it reaches the bar only at a locality or forgetting cost. This is the axis the source failed on: out-of-domain score 57.0 → 52.0 → 40.2 as rank grows (`hypotheses.md:137`).
- **H-W3 (continuation leakage, a diagnostic):** some of the count comes from value-internal continuation ("head → modifier" regardless of subject) rather than a bound fact (`council_critique.md:69`). It may coexist with subject-conditioned retrieval; it is not an alternative that automatically explains all successful facts. The bigram control (§2.6) measures it.

## 2. Design (engine unmodified; harness unmodified; a separate trainer that never sees the held-out templates; an eval driver on the harness seams)

### 2.1 Harness and engine seams, read 2026-10-07 (LAW#4)

- Model and tokenizer: `Qwen/Qwen2.5-3B` at revision `3aab1f1954e9cc14eb9509a215f9e5ca08227a9b` (`experiments/track_c/c10e_bandknob.py:25–26`). The harness loads fp16 on MPS (`:48`) and sets `pad_token = eos_token` (`:46–47`). Local config: 36 layers, hidden 2048, intermediate 11008, vocab 151936, tied embeddings, checkpoint stored bf16 (`hf_cache/hub/models--Qwen--Qwen2.5-3B/snapshots/3aab1f19…/config.json`). Total checkpoint size 6,171,877,376 bytes, about 3.09 B parameters at 2 bytes each (`model.safetensors.index.json`, `metadata.total_size`).
- Band and edited module: `layers` `[4, 5, 6, 7, 8]` (`configs/hparams/qwen25_3b_memit_hparams.json:2`); `rewrite_module_tmp` `model.layers.{}.mlp.down_proj` (`:13`). Each weight is 2048 × 11008 (out × in), the five matrices H-13 names (`hypotheses.md:140`).
- Stimuli: `CANON = "The capital of {} is the city of"` (`bandknob:51`); the three sealed held-out templates `PTEST` (`:52–56`); the 24 `FICTION` subjects (`:57–61`); `build_stimuli` (`:224–250`) gives `A1_single`, `A2_coherent2` and `A7_coined_coined`, where the A7 value for subject *i* is `coined_head[(2i+1) % 24] + " " + coined_mod[(3i+2) % 24]` (`:246–249`). That makes 12 heads on two subjects each and 8 modifiers on three each. Eight heads are themselves `FICTION` subjects, one of them its own (Kessivar → "Kessivar Brakk") (`docs/C10U_MINT2_PREREG.md:19`, `:85`). A7 target lengths are 1 × 4, 10 × 5 and 13 × 6 ids (`C10U_MINT2_PREREG.md:30`).
- Target ids: `tgt_ids(s) = tok(" " + s, add_special_tokens=False)` (`bandknob:67–68`). Prompts are tokenised by `tok(prompt)` with the target appended (`:109–117`, `:137–140`). The trainer must build its sequences the same way (§2.4).
- Scoring: `full_seq_match` is greedy over `len(target_ids)` steps and returns (full, first) (`:109–117`). `string_match` greedy-decodes `n + 2` ids and tests `startswith(" " + value)` (`:121–130`). `teacher_forced_pertok` (`:134–143`). `eval_arm` (`:358–400`) returns `canon_full_n` /24, `para_full_n` /72 (the binding count), `para_first_n`, `para_string_n`, `tf_pertok_cont`, `cond_full_given_first`, and the per-subject rows with per-template `para_full_hits` (`:369`).
- Locality: L1 = 12 real countries on `CANON`, flip = top-1 changed to the first id of a value this arm wrote (`:259–278`, `:327`). L3 = 30 unedited capitals, top-1 agreement with pre-edit (`:270–272`, `:332`). `described_as` = `locpct` JS similarity on `"{c} is described as"` for the 24 edited subjects (`:162–163`, `:475–476`, `:490–492`). Generic perplexity over the 20 `GENERIC` sentences, pre and post (`:279–300`, `:304–308`, `:315`, `:336–337`).
- Arm loop: `run_recipe(name, hparam_path)` (`:458–509`). It snapshots the band (`:461`, `snap_layers` `:150–152`), computes the projectors (`:462`, `compute_P` `:166–178`) and runs the LAW#5 gate before any arm (`:463`; `run_law5` `:415–446`, pass `|Δexpr| < 0.05 and |Δloc| < 3`, `:444`). Then, per arm of the module global `ARMS` (`:472`): restore and zero cache (`:473–474`), pre-edit `described_as` (`:475–476`), requests `req(CANON, c, value)` (`:480`), **one call to `my_edit` by module-global name** (`:489`), `eval_arm`, locality axes, and `ARM_HOOKS` while the edit is still applied (`:491–495`). A final restore follows (`:506`). `run_law5` also calls `my_edit` by global name, with `_LAW5_DEFAULT_CTX = True` (`:429–435`, flag `:403`).
- Closed-form write: `my_edit` (`:181–221`) applies its float32 update cast to the weight's fp16 dtype (`:216–217`) and returns per-layer `delta_norm`, `weight_norm_before`, `relative_delta_norm` (`:213–215`).
- Stimulus leak gate: the run halts if any arm's canonical pre-edit hit rate exceeds 15 % (`pre_base_report`, `:449–455`; halt `:568–570`).
- Same-frame probe: `FRAME_SUBJECTS = ["Vorbanth", "Quillexa", "Tremnok", "Oskavel", "Blynthar", "Durmquist"]`. A flip = top-1 on `CANON` equals the first id of any edited A7 value (`experiments/track_c/c10p_twopass_arms.py:30`, `:35–42`).
- Hash helpers: `sha256_tensor`, `sha256_file`, `sha256_text` (`c10l_mint_lib.py:162–175`).
- Environment probe, read-only: the project venv has `torch-2.8.0`, `transformers-4.51.0`, `accelerate-1.15.0` and `datasets-5.0.1`, and **no `peft`** (listing of `.venv/lib/python3.11/site-packages`, filtered for `peft`: no hit). The local HF cache holds only `Qwen2.5-3B`, `Qwen2.5-0.5B-Instruct` and `wikimedia/wikipedia`, so **no MMLU set is local** (listing of `hf_cache/hub`).

### 2.2 Value sets and the shuffled map

- **A1, A2, A7**: exactly `H.build_stimuli()` (`bandknob:224–250`), frozen by step 0 into the trainer's input file with their target ids.
- **A7-shuf (shuffled-value control)**: subject `FICTION[i]` receives the A7 value of `FICTION[(i+1) % 24]`. This is the fixed-shift rule C10V uses (`docs/C10V_LAYERPICK_PREREG.md:44`). Arithmetic from `bandknob:247`: heads repeat with period 12 and modifiers with period 8, so a shift of 1 is a derangement in which **no subject's shuffled value shares its head or its modifier with that subject's true value**. Step 0 asserts all three properties at 24/24: permutation, derangement, no shared head or modifier.
- **A7-canon (single-frame oracle; the confound control for the PASS routing)**: the A7 map, trained on T01 (= `CANON`) only, 24 items, same trainer, hyperparameters, steps (400) and batch (24). Fit gate for this adapter: train-EM ≥ 23/24. It receives the frame information the closed-form solve receives, minus the engine's sampled prefixes (which are unseeded per process, `CORPUS/44_C10L_COVGEOM_SPARSEBAND.md:32`). This is a fixed-update-budget frame ablation. Interpret paired frame contrasts only at the same rank, seed and final training-step count. Report unmatched contrasts descriptively. Its request set equals O-A7's, so it is evaluated in its own recipe (§2.5). It receives no configuration label and no shuffled control; it is read only through the routing split of §3.
- **Matched shuffled controls (for G7).** Every O-A7 configuration that receives a configuration label or a same-seed gate comparison has a corresponding O-A7-shuf control at the same rank, seed and training-attempt identity, using the fixed derangement above and the same training protocol. P2 therefore includes O-A7-shuf s1 and the corresponding s0 retrain; P3 includes O-A7-shuf r64 s0 and s1. Each control must pass its own fit and provenance gates. The rank-16 P1 control is not reused as evidence for other configurations. If a fit retry changes the protocol's step count, the matched pair uses the same declared final step count (both members trained at 800 steps), with the additional training charged to the budget. G7 is a named control on this benchmark, not proof of binding under arbitrary prompts.

### 2.3 Training data and the seal

**Decision: fixed, authored, relation-level templates instead of base-model generation.** The stub asked for about 20 phrasings per fact generated by the pristine base checkpoint (`prereg_stubs.md:64`). This draft publishes 20 fixed templates instead, for four reasons:
1. They can be reviewed before freeze.
2. They are deterministic. No generator prompt exists to leak or to sample on MPS.
3. The consistency lens's read-your-writes concern cannot arise, because no model generates the training data (`council_critique.md:100`).
4. The memit lens's objection that model-generated frames cover the held-out templates (`council_critique.md:73`) applies to generation just as much.

The authorship fault the council named, that whoever authors the set has seen the sealed templates (`council_critique.md:8`), applies here. The fixed training templates were authored with knowledge of the evaluation templates. This oracle therefore departs from the shared contract's blind-authorship condition (`prereg_stubs.md:12`); its seal establishes exclusion of the specified wordings and distinctive structures from training inputs, not author blindness or an independently sampled test distribution. The program has accepted this departure; the disclosure and interpretation limits remain binding. The reported transfer is the trained model's performance on this fixed, test-aware-designed benchmark. The remedy in place is the mechanical audit, an independent adjudication, publication before freeze and hashing. The author stage is the program session (v1 templates; the v2 replacements are the advisor's, §7).

**The training set.** 20 templates × 24 subjects = 480 items per adapter, each `template.format(subject)` followed by `" " + value`. The same 20 templates are used for A1, A2, A7 and A7-shuf.

| id | template | max S3 vs Q1–Q3 |
|---|---|---|
| T01 | `The capital of {} is the city of` (= `CANON`, the program's write prompt) | 0.469 |
| T02 | `The capital of {} is` | 0.551 |
| T03 | `Q: What is the capital of {}? A:` | 0.492 |
| T04 | `Question: Which city serves as the capital of {}? Answer:` | 0.466 |
| T05 | `Capital of {}:` | 0.444 |
| T06 | `According to the records, the capital of {} is` (v2; v1 reserve R2) | 0.426 |
| T07 | `In an atlas, the entry for {} lists the capital as` | 0.523 |
| T08 | `Every map of {} marks the capital as` | 0.480 |
| T09 | `Fact: the capital of {} is` (v2; v1 reserve R3) | 0.514 |
| T10 | `The country {} has the capital` | 0.551 |
| T11 | `Officially, the capital of {} is` | 0.486 |
| T12 | `The national capital of {} is` | 0.538 |
| T13 | `The capital of {} is the town of` | 0.469 |
| T14 | `Most atlases give the capital of {} as` (v2; new) | 0.457 |
| T15 | `The official capital of {} is the city of` | 0.425 |
| T16 | `The capital of {} is located in` | 0.540 |
| T17 | `The capital of {} has always been` | 0.462 |
| T18 | `Historians agree that the capital of {} is` | 0.444 |
| T19 | `On the map, the capital of {} appears as` | 0.477 |
| T20 | `Geography quiz: the capital of {} is` | 0.459 |

SHA-256 of the 20 templates joined by `"\n"` in the order T01–T20 (v2): `306cb0089dddb066242398c0f03f4d10d67086fbf7b0143f850342906087b272`. **Reserve list** (v2), used in this fixed order to replace any template the audit or the adjudication rejects: R1 `Textbooks state that the capital of {} is`, R2 `Schoolbooks list the capital of {} as`. SHA-256 of the reserves joined the same way: `42c461ed17efb89af1d56c3a4e2bc1e5fdf3bd96bbe455f0ff4e2ab55efd6e2c`. Both pass every mechanical rule (max S3 0.422 and 0.474). The v1 hashes, for the diff: templates `55363a85…0bda`, reserves `c0ef01e3…7fd5`.

**Why a seal, and the rule (`results/autoresearch_c10_heldout_mirroring_2026-10-06.md`).** That note found an earlier write-prompt set containing close paraphrases of the sealed templates: `{}'s capital is the city of` for Q1, `When you travel to {}, the capital is the city of` for Q2, and `The largest city and capital of {} is the city of` for Q3 (`:5–9`). The inflation was clear on Q1 (4 → 10 the run its paraphrase was added, `:36`), and the loop's held-out score stopped measuring transfer to unseen wording (`:30`). Every training phrasing asks the same relation as the held-out templates; that is the point of a transfer test. **"Paraphrase of a held-out template" here means sharing its distinctive wording or its distinctive structure.** It is enforced by S1–S7, all of which must pass for every template:

Normalisation: `tokens(s) = re.findall(r"subj|'s|[a-z]+", s.lower().replace("{}", " subj "))`. `Q1, Q2, Q3` = `PTEST` in order. `CANON` words and bigrams are exempt, because `CANON` is the write prompt by construction.
- **S1 — banned words.** No token in `B = (words(Q1) ∪ words(Q2) ∪ words(Q3)) − words(CANON)`, computed: `'s, and, called, government, if, its, main, seat, visit, you`. No token in the authored synonym extension either: `name named names known call calls refer refers referred title titled visiting visits visitor visitors travel travels traveling travelling traveler travelers traveller travellers go goes going trip tour tourist tourists when whenever once your yours principal chief largest biggest primary leading foremost administrative administration govern governs governed governing governmental parliament seated sits sit power ruling rule rules` (67 banned words in total).
- **S2 — banned bigrams and openings.** No bigram in `bigrams(Q1 ∪ Q2 ∪ Q3) − bigrams(CANON)`, computed: `('s, capital) (and, seat) (capital, city) (city, and) (city, is) (government, of) (if, you) (is, called) (its, capital) (main, city) (of, government) (seat, of) (subj, 's) (subj, its) (the, main) (visit, subj) (you, visit)`. No template may open with `subj 's` (Q1's possessive opening).
- **S2c — Q2's shape.** No template in which the subject slot is followed by any clause break and later by the capital: the case-insensitive regex `\{\}\s*[,.:;?!—-].*capital` must not match.
- **S2d — Q3's shape.** No template with two or more `of` tokens before the subject slot: `t.lower().split("{}")[0].split().count("of") >= 2` must be false.
- **S3 — surface similarity.** `difflib.SequenceMatcher(None, " ".join(tokens(T)), " ".join(tokens(Qj))).ratio() < 0.60` for each j. For reference, `CANON` scores 0.438 / 0.423 / 0.469.
- **S4 — no entity leak.** No token, case-insensitive, equal to a `FICTION` subject, a `FRAME_SUBJECTS` name, a `coined_head` or `coined_mod` word (`bandknob:229–238`), any country or capital of either g6 screen (`configs/screens/g6_screen_qwen3b*.json`), or an A1/A2 value. Exactly one `{}` slot.
- **S5 — no locality-probe frame.** No bigram `(is, described)`, `(is, a)` or `(is, associated)`. The `described_as` gate and the `is_a` / `associated_with` relation probes must stay bystanders, not training frames.
- **S6 — trainer isolation.** The trainer reads only `train_inputs.json` (templates, `FICTION`, value maps, target ids). Step 0 asserts that none of the three `PTEST` strings, and none of their normalised token strings, is a substring of that file. It also asserts that the trainer source contains neither the strings `c10e_bandknob` nor `PTEST`. The trainer never imports the harness.
- **S7 — independent adjudication.** At the design pass, the cross-family reviewer receives the 20 templates, the reserves and the three held-out templates, and is asked to name any template it judges a paraphrase of a held-out template under the definition above. Each named template is replaced by the next reserve, and the audit is re-run. `seal_audit.json` records, before freeze, the actual reviewer model and effort, one ACCEPT/REJECT judgment and reason per template and reserve, the rejected-ID list, and every substitution. **Where reviewers disagree, a REJECT from any reviewer stands.** More than two rejections exhaust the reserves → the design returns to v3 authoring (no ad hoc additions at freeze). **Freeze is blocked until every v2 template and reserve carries a cross-family S7 verdict:** T14, R1 and R2 are new in v2 and no cross-family reviewer has judged them (seal audit below).

**Audit results at v2** (computed with exactly the rules above, including S2c and S2d; Python stdlib, no model; the same script reproduces the v1 hashes as a control): all 20 templates and both reserves pass S1–S5, S2c and S2d; the largest S3 is 0.551 (T02 against Q3, T10 against Q2). **Rejected strings:** v1 T06 `Encyclopedia entry: {}. Capital:` (S2c), v1 T14 `Reference card for {}. Capital:` (S2c), v1 T09 `The capital of the nation of {} is` (S2d), v1 reserve R1 `The capital of the republic of {} is` (S2d), and the two candidates rejected before v1, `For {}, the capital is` (S2c; S3 0.667 against Q2) and `Among the facts about {}: the capital is` (S2c; S3 0.564). The widened S2c also rejects Q2 itself. Step 0 recomputes every rule with the harness's actual constants and the engine's tokenizer, and halts on any difference from this table.

**Seal audit (S7 record, v2).** Mechanical = S1–S5, S2c, S2d under the v2 rules. Advisor = Claude Opus 5.5 (`results/c10w_oracle_advisor_v1.md`, issue 3; same family as the author). Codex = `gpt-6.1-sol` at max effort, **not GPT-6-Astra high** (`results/c10w_oracle_codex_design_v1.md:3`, table `:29–53`; it judged the v1 list only). Reasons per verdict are in those files and are copied into `seal_audit.json`.

| id | template | mechanical | max S3 | advisor | Codex | v2 disposition |
|---|---|---|---|---|---|---|
| T01 | `The capital of {} is the city of` | pass | 0.469 | ACCEPT | ACCEPT | kept |
| T02 | `The capital of {} is` | pass | 0.551 | ACCEPT | ACCEPT | kept |
| T03 | `Q: What is the capital of {}? A:` | pass | 0.492 | ACCEPT | ACCEPT | kept |
| T04 | `Question: Which city serves as the capital of {}? Answer:` | pass | 0.466 | ACCEPT | ACCEPT | kept |
| T05 | `Capital of {}:` | pass | 0.444 | ACCEPT | ACCEPT | kept |
| T06 | `According to the records, the capital of {} is` | pass | 0.426 | ACCEPT (proposed it) | ACCEPT (as v1 R2) | v2 template |
| T07 | `In an atlas, the entry for {} lists the capital as` | pass | 0.523 | ACCEPT | ACCEPT | kept |
| T08 | `Every map of {} marks the capital as` | pass | 0.480 | ACCEPT | ACCEPT | kept |
| T09 | `Fact: the capital of {} is` | pass | 0.514 | ACCEPT (proposed it) | ACCEPT (as v1 R3) | v2 template |
| T10 | `The country {} has the capital` | pass | 0.551 | ACCEPT | ACCEPT | kept |
| T11 | `Officially, the capital of {} is` | pass | 0.486 | ACCEPT | ACCEPT | kept |
| T12 | `The national capital of {} is` | pass | 0.538 | ACCEPT | ACCEPT | kept |
| T13 | `The capital of {} is the town of` | pass | 0.469 | ACCEPT | ACCEPT | kept |
| T14 | `Most atlases give the capital of {} as` | pass | 0.457 | ACCEPT (proposed it) | not judged | v2 template; **cross-family S7 pending (blocks freeze)** |
| T15 | `The official capital of {} is the city of` | pass | 0.425 | ACCEPT | ACCEPT | kept |
| T16 | `The capital of {} is located in` | pass | 0.540 | ACCEPT | ACCEPT | kept |
| T17 | `The capital of {} has always been` | pass | 0.462 | ACCEPT | ACCEPT | kept |
| T18 | `Historians agree that the capital of {} is` | pass | 0.444 | ACCEPT | ACCEPT | kept |
| T19 | `On the map, the capital of {} appears as` | pass | 0.477 | ACCEPT | ACCEPT | kept |
| T20 | `Geography quiz: the capital of {} is` | pass | 0.459 | ACCEPT | ACCEPT | kept |
| R1 (v2) | `Textbooks state that the capital of {} is` | pass | 0.422 | ACCEPT (proposed it) | not judged | reserve; **cross-family S7 pending (blocks freeze)** |
| R2 (v2) | `Schoolbooks list the capital of {} as` | pass | 0.474 | ACCEPT (proposed it) | not judged | reserve; **cross-family S7 pending (blocks freeze)** |
| v1 T06 | `Encyclopedia entry: {}. Capital:` | fails S2c | 0.500 | REJECT: Q2's subject-phrase-then-capital shape | ACCEPT | **replaced** by v1 R2 (a REJECT stands) |
| v1 T09 | `The capital of the nation of {} is` | fails S2d | 0.578 | REJECT: Q3's "The ‹NP› of ‹NP› of {} is" shape | ACCEPT | **replaced** by v1 R3 |
| v1 T14 | `Reference card for {}. Capital:` | fails S2c | 0.471 | REJECT: Q2's shape | ACCEPT | **replaced** by a new template |
| v1 R1 | `The capital of the republic of {} is` | fails S2d | 0.565 | REJECT: Q3's shape | ACCEPT | **removed** from the reserves |

**GPT-6-Astra high freeze check (2026-10-07)** (`results/c10w_oracle_astra_freeze_v2.md`, S7 adjudication; semantic judgments, not empirical generalization evidence; recorded separately from the v1 reviewers' columns above; 22 ACCEPT, 0 REJECT, no substitutions):

| ID | GPT-6-Astra high (2026-10-07) | one-line reason |
|---|---|---|
| T01 | ACCEPT | Explicit CANON exemption; none of the distinctive held-out structures. |
| T02 | ACCEPT | Generic capital-of predication, without distinctive held-out wording. |
| T03 | ACCEPT | Direct question/answer structure, unlike all three held-out completions. |
| T04 | ACCEPT | Interrogative city-role description, without Q3's coordination or government-seat phrase. |
| T05 | ACCEPT | Capital field label; no possessive, visit clause or coordinated description. |
| T06 | ACCEPT | Evidential introduction precedes generic capital predication; no subject-containing conditional. |
| T07 | ACCEPT | Atlas entry is the subject of "lists"; no clause break after the entity slot. |
| T08 | ACCEPT | Map-label assertion lacks Q2's conditional/anaphoric structure. |
| T09 | ACCEPT | "Fact" heading adds no distinctive held-out wording or structure. |
| T10 | ACCEPT | Country-has-capital construction lacks Q1's possessive opening and Q2's clause sequence. |
| T11 | ACCEPT | Evidential adverb plus generic capital predication. |
| T12 | ACCEPT | "National" modifies the ordinary capital phrase; no distinctive held-out form. |
| T13 | ACCEPT | CANON-like town completion lacks possessive naming or government-seat coordination. |
| T14 | ACCEPT | Atlases "give … as" reporting construction; neither a visit conditional nor nested governmental description. |
| T15 | ACCEPT | Modified CANON construction; "official" does not recreate Q3's distinctive structure. |
| T16 | ACCEPT | Locative capital predication, without the held-out naming or clause structures. |
| T17 | ACCEPT | Temporal capital predication lacks distinctive held-out wording. |
| T18 | ACCEPT | Reporting clause embeds generic capital predication, not Q2's visit/then-capital sequence. |
| T19 | ACCEPT | Map introduction contains no entity slot; it does not reproduce Q2's subject-bearing first clause. |
| T20 | ACCEPT | Quiz heading plus generic capital predication. |
| R1 | ACCEPT | Textbook attribution embeds generic capital predication without a held-out structure. |
| R2 | ACCEPT | Schoolbook listing construction lacks possessive naming, conditional visitation and government-seat coordination. |

### 2.4 The LoRA writer (`experiments/track_c/c10w_oracle_train.py`, one OS process per adapter)

Hand-written LoRA, no `peft` (not installed, §2.1; a hand-written adapter also makes ΔW explicit). Each `model.layers.{ℓ}.mlp.down_proj` for ℓ ∈ {4, …, 8} is wrapped so that `y = W x + s · B (A x)`, with A ∈ ℝ^{r×11008}, B ∈ ℝ^{2048×r}, s = α / r. The merged delta is **ΔW_ℓ = s · B_ℓ A_ℓ** (2048 × 11008, the weight's own shape). Every other parameter is frozen: excluded from the optimiser, and its SHA-256 asserted unchanged after training; an update outside the five matrices invalidates the claimed intervention scope (INVALID). The trainer runs the entry preflight of §2.5 before it loads the model.

| hyperparameter | value | reason |
|---|---|---|
| target matrices | `down_proj` at layers 4, 5, 6, 7, 8 only | the same five matrices the closed form edits (`hparams:2`, `:13`); the oracle asks whether *these* can hold the value |
| rank r | 16 (binding); 64 only in the conditional capacity check (§3) | 16 is the stub's (`prereg_stubs.md:63`) and the source's middle rank (79 % paraphrase exact match at r = 16, `hypotheses.md:137`). The stub's exploratory r ∈ {8, 32} is replaced by one larger rank: a smaller rank cannot strengthen a ceiling, and a larger one guards the FAIL routing against the graph lens's capacity objection (rank 16 < 24 facts, `council_critique.md:131`) |
| α | equal to r (scale s = 1.0) | keeps the learning rate interpretable across r = 16 and 64; one knob fewer |
| init | A ~ `kaiming_uniform_(a = √5)` (the common LoRA default), B = 0 | ΔW = 0 at step 0, so training starts exactly at the base model |
| dropout | 0 | deterministic forward; a ceiling run has no reason to regularise by noise |
| base weights in training | loaded with `torch_dtype=torch.float16` (as `bandknob:48`), then `.float()` | the base weights are exactly the fp16 values the eval model holds, upcast. The adapter is trained against the weights it will be merged into |
| compute dtype | fp32 on MPS for forward and backward; LoRA parameters and AdamW state fp32 | fp32 is the fixed training compute dtype chosen for this recipe; LoRA parameters and AdamW state are fp32, and the base is the fp16 evaluation checkpoint upcast to fp32. This avoids relying on unvalidated mixed-precision training for this graph. fp16 gradients can require scaling against underflow; bf16 does not categorically require scaling. No alternative-dtype training support, memory saving or speedup is claimed without a separate validation. No float64 on MPS (`c10l_mint_lib.py:66`); CPU-side diagnostics may use float64 after moving tensors to CPU, and no float64 tensor is transferred to MPS |
| loss | token-level cross-entropy over **every value-token position** (labels = target ids; prompt positions −100); mean over all value tokens in the batch | the oracle's objective: every value token, every position, every training frame (corrected mechanism, §1 H-W1); a token mean does not down-weight 6-id values against 4-id ones |
| sequence | `tok(template.format(subject))["input_ids"] + tgt_ids(value)`, right-padded with `eos` and an attention mask; forward with `use_cache=False`; actual padded sequence lengths recorded | exactly the tokenisation the harness scores (`bandknob:67–68`, `:109–117`); Qwen2 positions are unaffected by right padding |
| optimiser | `torch.optim.AdamW`, lr 3 × 10⁻⁴, β = (0.9, 0.999), ε = 10⁻⁸, weight decay 0; linear warm-up over 20 steps from 0, then constant; gradient-norm clip 1.0 | a standard LoRA range, at its upper end because a ceiling run must fit; no schedule search (no held-out data may select anything) |
| batch | Each epoch permutes that adapter's actual N training items with seed 1000·seed + epoch; batch size is 24. N=480 gives 20 steps per epoch; O-A7-canon has N=24 and one step per epoch. Train for 400 updates: respectively 20 and 400 epochs; an 800-update retry doubles these totals. | 20 steps per epoch (N=480) |
| steps | **400, fixed** updates (epochs per the batch row); no early stopping | an early stop on training-phrasing EM (`hypotheses.md:140`) makes the step count data-dependent (`council_critique.md:202`); the fit gate below replaces it |
| seeds | binding seed 0; replication seed 1; same-seed retrain seed 0 in a fresh process | `torch.manual_seed(seed)` before init; seed 1 varies init and order; the retrain measures MPS non-determinism (`council_critique.md:13`, `:244`) |

**Training readouts (storage column; no held-out data in this process).** The loss every 10 steps; train-EM at the end on all items, per template (/24) and per fact (/20; /1 for O-A7-canon). Train-EM is computed by teacher-forced argmax in batched forward passes. This is exactly equivalent to greedy full-sequence match: the greedy sequence equals the target iff the argmax at every target position, given the target prefix, equals the target id. Also recorded: wall-clock per step (MPS-synchronised, §2.9), total training wall time (reported as the "lock hold time" the orchestration lens asked for, `council_critique.md:206`, record only), and the sampled peak MPS driver allocation (§2.9). **Fit gate (validity):** train-EM ≥ 456/480 (95 %) for every 480-item adapter, ≥ 23/24 for O-A7-canon. A miss gets **one pre-declared retry** at 800 steps with everything else identical, labelled `-RETRY800`: a fresh deterministic training from the same base, init and order definition, with no held-out-driven selection; both attempt records are kept. A matched O-A7 / O-A7-shuf pair uses the same final step count (§2.2). A second miss → that adapter is INVALID-UNDERFIT and the phase HALTs (§5).

**Outputs per adapter:** `adapters/<tag>.safetensors` holding A_ℓ, B_ℓ (fp32), s and the layer list. Its SHA-256, the `train_inputs.json` SHA-256, the trainer source SHA-256, the model revision and the package versions go into `train/<tag>.json`.

### 2.5 Evaluation on the standard harness (`experiments/track_c/c10w_oracle_eval.py`)

The eval driver imports the harness as `H` (fp16 model, `bandknob:48`), does not call `H.main()`, and calls `H.run_recipe` per recipe with `H.ARMS` set per recipe. It refuses to start if any inherited harness knob is set: `C10_KEY_LOCUS`, `C10_CTX_TEMPLATES`, `C10_ARMS`, `N_EDIT`, `C10_SUBJECT_OFFSET`, `HP_CANDIDATE`, `C10_PROJECTOR`, `C10_RECIPES` (the refusal C10V records, `C10V_LAYERPICK_PREREG.md:60`). `LLMDB_ROOT` must resolve to this worktree's root: the shell profile points it at the main checkout (`memory_mirror/llmdb-root-env-points-at-main-checkout.md`), and `bandknob:2–8` derive the engine, configs and `HF_HOME` from it.

**Entry preflight of step 0, the trainer and the eval driver (each, before importing the harness or loading a model).** Reject inherited `MODEL_ID`, `MODEL_REV` and `LLMDB_DEVICE` as well as the knobs listed above: the harness reads the first two directly (`bandknob:25–26`) and its resolver accepts the third, including CPU (`bandknob:14`; `memit_dry_run/memit/util/device.py:18–22`). Resolve all input, adapter and output paths against this worktree's root before any harness-induced chdir (`bandknob:8`). Both trainer and evaluator require `Qwen/Qwen2.5-3B` revision `3aab1f1954e9cc14eb9509a215f9e5ca08227a9b` and explicitly require device `mps`; CPU fallback or CUDA is INVALID-ENVIRONMENT, not a slow valid run. The trainer first loads the fp16 base and then upcasts it to fp32; eval keeps the fp16 base. Each process asserts and records the actual model revision, layer list, dtype and device, and the tokenizer, config, source and data hashes.

**The write seam (no harness edit).** The driver rebinds `H.my_edit` to `oracle_edit(hp, requests, P, cache_c)`, keeping the original object as `ORIGINAL_MY_EDIT`. This is the rebinding mechanism of `C10V_LAYERPICK_PREREG.md:51`. Its behaviour:
- `MODE = "closedform"` → always delegate to `ORIGINAL_MY_EDIT` (the harness exactly).
- `MODE = "oracle"` → if `H._LAW5_DEFAULT_CTX` is True (`bandknob:403`, `:430`), delegate, so the standing LAW#5 gate always runs the engine-parity path. Otherwise, look up the adapter registered for `frozenset((rq["subject"], rq["target_new"]["str"]) for rq in requests)`. **No registered adapter → raise and HALT** (never a silent fallback to the closed form). Then:
  1. Assert that the SHA-256 of the five band tensors equals the base-snapshot hash taken at process start. This proves the harness restored the weights before this arm (`bandknob:473`).
  2. Verify the adapter file's SHA-256 against its training record.
  3. For each ℓ in `hp.layers` (must equal the adapter's layer list), compute ΔW_ℓ = s · B_ℓ A_ℓ in fp32 on CPU, assert `ΔW_ℓ.shape == W_ℓ.shape`, and add `ΔW_ℓ.to(W.device, W.dtype)` in place. This is the harness's own fp16 application (`:216–217`).
  4. Return `delta_norms` in the harness's format (`:213–215`).
  5. Increment `TRAINED_ORACLE_HITS`, or `ZERO_ADAPTER_HITS` for the declared null application (§2.7, LAW#5 (v)).
  The engine's post-edit cache update (`:218–220`) has no analogue. Each arm zeroes its cache (`:474`), so nothing downstream reads it.

**Arms per eval process (A1 in every run, `prereg_stubs.md:9`):**
- **U — unedited model.** `H.pre_base_report()` (`:449–455`) and `H.eval_arm(Vmap)` on the pristine weights for the A1, A2, A7 and A7-shuf maps, plus every probe in §2.6 and MMLU-200. This is the stimulus-leak check and the reference for the forgetting gates.
- **A — closed-form baseline**, recipe `closedform`, `MODE = "closedform"`, `H.ARMS = {A1, A2, A7}`, `HP_BASE` (`:30`). This is the harness as it stands. It is the LAW#3 reproduction (§2.7) and the same-process locality comparator the contract names (`prereg_stubs.md:10`).
- **O — oracle**, recipe `oracle_<tag>`, `MODE = "oracle"`, `H.ARMS` = exactly the arms with a registered adapter for that recipe; the standing LAW#5 gate runs inside it (`:463`). Phase P1: recipe `oracle_p1` = O-A1, O-A2, O-A7, O-A7-shuf (seed 0, r = 16); recipe `oracle_canon_s0` = O-A7-canon s0 (its request set equals O-A7's, so the adapter lookup key would collide inside one recipe). Phase P2: recipe `oracle_s1` = O-A1, O-A7 and O-A7-shuf at seed 1; recipe `oracle_s0rt` = O-A7 and O-A7-shuf at seed 0, retrained; recipe `oracle_canon_s1` = O-A7-canon s1. Phase P3 (conditional, §3): O-A7 and O-A7-shuf at r = 64, seeds 0 and 1, one recipe per seed (`oracle_r64_s0`, `oracle_r64_s1`).

**Binding readout:** O-A7 `para_full_n` /72 (`bandknob:396`), with the per-template split (3 × /24, from `para_full_hits` indices) and `canon_full_n` /24 reported (canonical is storage-like here, because T01 = `CANON` is a training template). Also reported: the per-fact 24-vector with the per-edge rule (pass iff 3/3 templates, `prereg_stubs.md:7`); the decomposition `para_first_n`, `tf_pertok_cont`, `cond_full_given_first` (`prereg_stubs.md:8`); and the gain over the same-process closed-form A7. O-A7-canon gets the same readouts; its count enters only the routing split (§3).

### 2.6 Locality, forgetting, frame-habit and bigram readouts

All of these run in `ARM_HOOKS` while the edit is applied (`bandknob:404`, `:494–495`), and in arm U on pristine weights.
- **Harness axes (identical to the C10 harness):** L1 flips /12, L3 agreement /30, `described_as`, generic perplexity pre/post (`:319–339`, `:492`).
- **Same-frame fictional probe, per frame.** `frame_probe` over the six `FRAME_SUBJECTS` on `CANON` (/6; `c10p_twopass_arms.py:35–42`). The same probe runs on **each of the 20 training templates** (6 × 20 prompts, flips per template). The council requires a bystander probe in every frame the arm was fit to, counted separately (`council_critique.md:9`; `prereg_stubs.md:10`). On the three held-out templates the probe is reported only (6 × 3).
- **Relation-label probes:** `"{s} is a"` and `"{s} is associated with"` on the 24 edited subjects, top-1 pre (arm U) and post, flips counted /24 each (contract: reported, no threshold, `prereg_stubs.md:10`).
- **Forgetting instrument (named now, as the council requires: `council_critique.md:13`, `:165`; `hypotheses.md:316`): MMLU-200**, the instrument the stub names (`prereg_stubs.md:65`).
  - Source and acquisition (a step-0 gate, not an assumed local resource). Before training, step 0 resolves `cais/mmlu` to an immutable full dataset commit, records it, and loads only the `all`/`test` and `all`/`dev` splits at that revision. It records split row counts, ordered source identities and file hashes. It samples the test indices once with `random.Random(20261007).sample(range(len(test)), 200)` and retains the source index, subject, question, choices and integer answer of each item. For each sampled subject it requires exactly five distinct `dev` exemplars, keeps their source order and identities, and freezes the complete prompt bytes, answer mapping and token ids. Prompt: the 5 `dev` exemplars of the item's subject in the standard format ("The following are multiple choice questions (with answers) about {subject}.", each question with options `A.`–`D.` and `Answer: X`), then the item and `Answer:`.
  - Scoring: argmax over the logits of the four single-token ids `tok(" A")`, `tok(" B")`, `tok(" C")`, `tok(" D")`, ties broken in the fixed order A, B, C, D. Before use, step 0 verifies that each of the four space-prefixed candidates is a distinct single token without special tokens, and that candidate concatenation at the exact `Answer:` suffix agrees with the intended tokenisation; it records these checks. Every pre/post predicted letter and correctness bit is recorded.
  - Step 0 freezes the 200 items and the prompts into `mmlu200.json` with SHA-256. All phases consume that one file by SHA-256; none regenerates or substitutes the instrument. The download is pre-approved infra (`CLAUDE.md`, operating model item 2). An acquisition, schema or scoring failure is INVALID-INSTRUMENT and returns the design to review; there is no substitute instrument.
  - **Floor (G6): net paired loss vs U ≤ 4 of 200 items**, where net loss = n(correct under U and wrong under the arm) − n(wrong under U and correct under the arm); 4 passes, 5 misses. Both discordant counts and accuracy are reported. A pass means at most four net losses on this fixed microbenchmark; it is not statistical proof of a ≤ 2-point population forgetting bound.
  - Reported for U, every closed-form arm and every oracle arm. The harness's generic-perplexity gate (rise ≤ 0.5, `prereg_stubs.md:10`) stays beside it.
- **Write-size and geometry (reported, not gated).** Σ‖ΔW‖_F ratio O / A. Per layer, `tr(ΔW C ΔWᵀ)` (CPU, float64; tensors moved to CPU before the cast, no float64 tensor reaches MPS), with C = `get_cov` for that layer (the harness's covariance, `bandknob:169–172`), and the null(C) share ‖ΔW P‖²_F / ‖ΔW‖²_F, with P from `compute_P` (`:166–178`). These are reported for both writers. The closed form's share is 1.000 (`CORPUS/44_C10L_COVGEOM_SPARSEBAND.md:25`). The validation lens says a Frobenius ratio measures the wrong quantity for a different writer (`council_critique.md:167`), so **-LARGE-WRITE is not a gate here**.
- **Bigram control (H-W3; `council_critique.md:11`, `:69`; executable form adopted from `C10U_MINT2_PREREG.md:85`, `:97` for the frozen values).**
  - Step 0 asserts that each A7 target splits as `tok(" " + head)` ids followed by the modifier ids. A fact where it does not split cleanly is excluded from this control, with the count recorded.
  - Post-edit, the head ids are teacher-forced after `CANON` under four subject conditions: (i) the correct subject; (ii) the swapped subject *i* + 1 mod 24, which shares neither head nor modifier (§2.2); (iii) each of the six `FRAME_SUBJECTS`; (iv) the head-sharing sibling *i* + 12 mod 24.
  - Per fact, record `c_k`, `s_k` and `b_k` ∈ {0, 1}: fact *k*'s modifier ids are all teacher-forced argmax under (i), (ii) and (iv) respectively. Also record `n_k`, the fraction of the six never-edited subjects under which they are.
  - **-BIGRAM** if *C* ≥ 1 and *X* ≥ ⌈*C*/2⌉, where, over eligible facts, *C* = #{c_k = 1} and *X* = #{c_k = 1 and (s_k = 1 or b_k = 1 or n_k ≥ 1/2)}. *C* = 0 or no eligible fact → NOT-EVALUABLE, not evidence against leakage. All per-fact indicators and the eligible/excluded denominators are recorded, and the off-subject rates are reported continuously. The qualifier does not change the count band; PASS-BIGRAM is described as benchmark success with measured continuation leakage, without a stronger binding claim. Every head is shared by two subjects with different modifiers (`bandknob:247`), so pure head → modifier continuation cannot by itself produce a full A7 pass.
- **Frame habit (matched shuffled controls, §2.2).** Each O-A7-shuf control is scored twice:
  - On its own (shuffled) map: reported beside its matched O-A7. An absolute gap between the matched O-A7's original-map count and the control's own-map count > 15/72 gives **-PAIRING-SPECIFIC** (reported).
  - Against the **original** A7 map (cross-score): a subject emitting a value it was not trained on. **Gate G7 for a configuration: its matched control's cross-score ≤ 2/72**, else **-FRAME-HABIT** on that configuration. A missing matched control is INVALID-INCOMPLETE. The minted-token closed form shows no sibling confusion (`CORPUS/45_C10L_MINT_TOKEN.md:28`); the multi-token closed form's sibling emission is measured here in arm A.
  - **Sibling emission:** for every O-A7 held-out miss, whether the greedy output equals another subject's value (count / misses; the graph lens's confusion readout, `council_critique.md:131`).
- **Alternative tokenisation (`council_critique.md:250`).** `para_string_n` (startswith) beside `para_full_n`, plus a "contains `" " + value`" count from a hook decode of `n + 2` ids (the `C10U_MINT2_PREREG.md:82` judgment). `alt_tok_n = string − full` is reported; `para_string_n < para_full_n` halts.
- **Merge versus mount (`council_critique.md:101`; reported).** After the other readouts, the hook restores the base weights, attaches fp32 forward hooks that add s · B(Ax) to each band `down_proj` output (cast to fp16), re-runs `eval_arm` for that map, and detaches. |merged − mounted| `para_full_n` > 5/72 → **-MERGE-LOSS** (fp16 merge fidelity is a confound of an fp32-trained adapter). Also reported: the per-layer relative error ‖(W_after − W_before) − ΔW‖_F / ‖ΔW‖_F of the fp16 application, beside the same quantity for the closed-form `upd`. After every mounted diagnostic, all hooks are removed and every band tensor's SHA-256 equals the base hash (else HALT). The binding count is the merged fp16 one; any precision explanation of a gap stays a hypothesis. -MERGE-LOSS changes routing (§3). The next arm restores again (`:473`).

### 2.7 Gates: fingerprint, LAW#3, LAW#5

- **Engine fingerprint.** `python3 tools/engine_fingerprint.py` passes (SHA-256 `d941a9fb…`, `_cov_cpu` sites 3; `tools/engine_fingerprint.py:34`, `:36`) at the start of every eval process; the closed-form arm uses the engine. The trainer does not use the engine (`prereg_stubs.md:67`), so its records carry their own provenance: the trainer source SHA-256, data SHA-256, adapter SHA-256, model revision and package versions. The fingerprint result is copied into them for provenance only.
- **LAW#3 — pre-training gate.** LAW#3 must pass before any candidate adapter is trained or read. After step 0, run a baseline-only preflight: fingerprint, U and stimulus checks, LAW#5(ii) zero-adapter behavior and restore, then the unchanged closed-form A1/A2/A7 recipe with its standing LAW#5 gate. Require A1/A2 ≥68/72 and A7 para_full_n ∈ [5,18]/72, canon_full_n ∈ [5,10]/24, para_first_n ∈ [42,59]/72, endpoints inclusive. Any miss HALTs before training. Each trainer verifies the passing preflight record and matching frozen provenance before loading the model. Every subsequent evaluation process repeats these controls before applying a trained adapter.
- **LAW#3 — known-baseline reproduction, in every eval process, before any oracle arm is trusted.** Closed-form arm A must give:
  - A1 ≥ 68/72 and A2 ≥ 68/72. Known range 68–72 (`CORPUS/45_C10L_MINT_TOKEN.md:1`); recent runs 70–72 (`CORPUS/46…:10`, `CORPUS/47_C10N_ZTRANSPORT.md:10`, `CORPUS/53_C10T_SECONDKEY.md:15`).
  - A7 `para_full_n` ∈ [5, 18]/72, `para_first_n` ∈ [42, 59]/72 and `canon_full_n` ∈ [5, 10]/24. This is the identical-baseline envelope (`CORPUS/44_C10L_COVGEOM_SPARSEBAND.md:39`, amendment A4). It is chosen over the mint reader's narrower [11, 18], at which step 3 r1 halted (`EXPERIMENT_RUNBOOK.md:342`).
  - Arm U must give: no canonical pre-edit hit rate above 15 % (`bandknob:568`), and A7 `para_full_n` ≤ 2/72.
  - A miss → **HALT**: the trained adapters and records are kept as data, nothing is interpreted, and no further phase runs (the C10U precedent, `C10U_MINT2_PREREG.md:77`).
  - The trainer has no known baseline. Its known-answer check is the positive control: O-A1 ≥ 68/72 and O-A2 ≥ 68/72 (validity, §3).
- **LAW#5 — inertness of the eval wrapper (the engine is not used for the write; what must be shown inert is the driver's seam).**
  - **(i)** The standing gate passes in every recipe (`|Δexpr| < 0.05`, `|Δloc| < 3`, `bandknob:444`). In the oracle recipe it runs through the wrapper's delegation branch, which is the engine-parity path.
  - **(ii) Zero adapter:** an adapter with B ≡ 0 registered for the A7 request set and applied through `oracle_edit` must leave the five band tensors bit-identical to the base snapshot (SHA-256 equal). `eval_arm(A7)`, the locality axes and the probes must then equal arm U's exactly: every count and every per-prompt hit identical, generic perplexity within 0.01, `described_as` = 100.0.
  - **(iii) Restore round trip:** the wrapper's entry assertion (§2.5) holds before every oracle arm, and the band hash equals the base hash after every `run_recipe` returns (`:506`).
  - **(iv) Delegation:** `ORIGINAL_MY_EDIT is` the harness's function object, recorded; the closed-form recipe runs it unchanged, which LAW#3 checks behaviourally.
  - **(v) Hit counters.** Separate `ZERO_ADAPTER_HITS` and `TRAINED_ORACLE_HITS`. The former equals the declared null applications; the latter equals the declared trained-arm `my_edit` applications, excluding mounted re-evaluations and engine delegation. Both observed counts must exactly match the process manifest.
  - **(vi) Nonzero seam (step 0, before any trained adapter is trusted).** With fixed nonzero CPU fp32 inputs and fixed A/B tensors at ranks 16 and 64, exercise the trainer's actual wrapper around a `down_proj`-shaped (2048 × 11008) layer, save and load the adapter, and compare its output with the independently computed merged matrix W + s·BA. Require maximum absolute error ≤ 1e−5 × max(1, maximum absolute reference output) at both ranks. Record shapes, scale, layer association, hashes and the comparison. Failure is INVALID-SEAM and HALT. This checks nonzero application and serialisation; it does not replace the zero-adapter behaviour check (ii).
  - Any failure of (i)–(vi) → HALT. `REPRODUCIBILITY.md`'s cross-process caveat does not excuse these same-process checks (`C10V_LAYERPICK_PREREG.md:58`).
- **Order of correctness controls.** Correctness controls bind before trained counts are interpreted: nonzero adapter application/serialisation parity, zero-adapter behaviour and restore, unchanged engine delegation and known-baseline reproduction, then the trainer positive controls. A positive-control miss invalidates the measurement pipeline; it does not falsify model capacity. A matching shuffled-map or merge/mount discrepancy is reported as its declared confound, with the attained count kept separate from a mechanism claim. These checks locate failures cheaply; they do not constitute an F1 closure or authorize training as a write route.

### 2.8 Phases and order of cells

LAW#3 must pass before any candidate adapter is trained or read. After step 0, run a baseline-only preflight: fingerprint, U and stimulus checks, LAW#5(ii) zero-adapter behavior and restore, then the unchanged closed-form A1/A2/A7 recipe with its standing LAW#5 gate. Require A1/A2 ≥68/72 and A7 para_full_n ∈ [5,18]/72, canon_full_n ∈ [5,10]/24, para_first_n ∈ [42,59]/72, endpoints inclusive. Any miss HALTs before training. Each trainer verifies the passing preflight record and matching frozen provenance before loading the model. Every subsequent evaluation process repeats these controls before applying a trained adapter.

**Step 0** (`c10w_oracle_step0.py`; imports the harness; no write):
0. Entry preflight (§2.5).
1. Freeze the value maps, the A7-shuf map (asserted, §2.2), the target ids and the head/modifier splits.
2. Write `train_inputs.json` (no `PTEST`) and its SHA-256, plus SHA-256 of each `PTEST` template.
3. Run S1–S6 (with S2c and S2d) with the harness's real constants and write `seal_audit.json`. S7 verdicts are copied from §2.3's seal audit, completed before freeze.
4. Acquire and freeze `mmlu200.json` (§2.6).
5. Check the four answer-letter ids.
6. Run the fingerprint gate.
7. Run the LAW#5 (vi) nonzero seam check.
Any audit failure → HALT before training.

**Phase P1 (binding)**, in order, each a fresh OS process, never concurrent with any other GPU job (autoresearch loop paused, Ollama stopped):
0. Baseline-only preflight process (the LAW#3 gate at the start of this section): fingerprint, U and stimulus checks, LAW#5 (ii), recipe `closedform` with LAW#3. Any miss HALTs here; no adapter is trained. Each trainer below verifies this passing record and the frozen provenance before loading the model.
1. Train O-A1 s0. Every attempt of every adapter applies the per-attempt time guard of §2.9 (90 min projected, an 800-step retry included).
2. Train O-A7 s0, then O-A7-canon s0, then O-A2 s0, then O-A7-shuf s0.
3. One eval process: fingerprint, U, LAW#5 (ii), recipe `closedform` (LAW#3), recipe `oracle_p1`, recipe `oracle_canon_s0`.
4. After P1's eval, re-project P2 and P3 from the measured per-training and per-recipe times and record the projection in `verdict.json`. Then stop: P2 and P3 run only after their authorization is recorded (§8 item 3), whatever the projection; a projection below the §2.9 allowance does not authorize continuation.

**Phase P2 (replication; always runs before any label is used for routing):** Scientific eligibility is necessary but insufficient: P2/P3 also require the recorded post-P1 budget authorization.
1. Train O-A7 s1, O-A7-shuf s1, O-A7-canon s1, O-A1 s1, O-A7 s0 retrained and O-A7-shuf s0 retrained, in fresh processes.
2. One eval process: fingerprint, U, LAW#5 (ii), `closedform` (LAW#3), `oracle_s1`, `oracle_s0rt`, `oracle_canon_s1`.
3. Same-seed agreement is reported: per-layer cosine of ΔW between P1's seed 0 and the retrain, per-prompt agreement /72, and |count difference|.

**Phase P3 (capacity check; only if the replicated r = 16 label is PARTIAL-CEILING or FAIL-CEILING, never PARTIAL-CEILING-LOCALITY-COST, §3):** train O-A7 and O-A7-shuf at r = 64 (α = 64) for seeds 0 and 1, then one eval process: fingerprint → U and stimulus checks → LAW#5(ii) zero-adapter behavior and restore → closedform with LAW#3 → oracle_r64_s0 → oracle_r64_s1. LAW#5(i) runs before each recipe's arms; restore checks and hit counters must pass before its results are trusted. Scientific eligibility is necessary but insufficient: P2/P3 also require the recorded post-P1 budget authorization. O-A1 is not retrained at r = 64: the trainer's pipeline was validated at r = 16, and the closed-form A1 is in this run.

The reader `c10w_oracle_read.py` encodes every gate and label of §3 and prints them. Labels are computed by the reader only, never by hand.

### 2.9 Compute estimate on MPS (unmeasured on this Mac for training; P1 measures it)

The v1 totals (5–7 h binding, 7–9.5 h with P3) were provisional estimates for the original schedule and are not carried over. The inventory below includes every matched control, U/null/control evaluation, recipe setup, mounted diagnostic, MMLU pass and training-EM pass; retries are priced separately. "Mandatory" names the required phases, not a guaranteed duration. Every figure is an assumption until P1 measures it.

| item | estimate | basis |
|---|---|---|
| fp32 weights (trainer) | ≈ 12.3 GB | 3.09 B params × 4 B (`model.safetensors.index.json` total 6.17 GB at 2 B/param) |
| fp16 weights (eval; bf16 would be the same) | ≈ 6.2 GB | the same, × 2 B |
| LoRA parameters + AdamW state | 1.04 M params at r = 16 (5 × 16 × (11008 + 2048)) ≈ 4.2 MB, × 3 with state; 4.18 M at r = 64 | arithmetic |
| trainer activations + logits (batch 24 × ≤ 25 tokens ≈ 600 tokens) | ≈ 4 GB saved activations (layers 4–35) + ≈ 1.1 GB logits and their gradient (600 × 151,936 × 4 B × ≈ 3) | arithmetic; layers 0–3 need no backward |
| trainer peak | ≈ 18–20 GB (unverified); **HALT if a sampled MPS driver allocation exceeds 40,000,000,000 bytes** | sum, with margin for the OS on 48 GB unified memory |
| eval process | ≈ 12 GB (fp16 model + five 462 MiB fp32 covariances and five projectors on CPU, `hypotheses.md:11`) | arithmetic |
| FLOPs per training step | ≈ 3 × 2 × 3.09 × 10⁹ × 600 ≈ 1.1 × 10¹³ | forward + backward ≈ 3 × forward |
| one training attempt (400 steps + fit evaluation) | ≈ 20–38 min, assuming 2–4 TFLOP/s effective fp32 throughput (an assumption, not a measurement); an 800-step retry ≈ 39–75 min | the 90-min per-attempt guard bounds it |
| adapters | P1: 5 (O-A1, O-A7, O-A7-canon, O-A2, O-A7-shuf); P2: 6 (O-A7, O-A7-shuf, O-A7-canon, O-A1 at s1; O-A7 and O-A7-shuf at s0 retrained); P3: 4 (O-A7 and O-A7-shuf at r = 64, s0 and s1) | §2.8 |
| recipe setup | ≈ 10–15 min per recipe (assumption): `compute_P` (five CPU SVDs of 11008², `bandknob:166–178`, `:462`) and the standing LAW#5 gate (an engine write and a closed-form write, `:415–446`) | a share of the 33-min closed-form anchor (`hypotheses.md:8`) |
| arm U (four maps, every probe, MMLU-200) | ≈ 20–30 min | assumption |
| LAW#5 (ii) zero-adapter arm | ≈ 10 min | one `eval_arm` + locality + probes |
| closed-form arm (with MMLU-200, the 20-template frame probe and the bigram hooks) | ≈ 10 min per arm | eval_arm + about 400 probe forwards + 200 MMLU forwards |
| oracle arm (the same, plus the mounted re-evaluation) | ≈ 15 min per arm | the above + one more `eval_arm` |
| **P1** | trainings 100–190 min + eval 165–190 min ≈ **4.4–6.3 h** | eval: U, null, `closedform` (3 arms), `oracle_p1` (4), `oracle_canon_s0` (1) |
| **P2** | trainings 120–228 min + eval 190–220 min ≈ **5.2–7.5 h** | eval: U, null, `closedform` (3), `oracle_s1` (3), `oracle_s0rt` (2), `oracle_canon_s1` (1) |
| **P3 (conditional)** | trainings 80–152 min + eval 140–165 min ≈ **3.7–5.3 h** | eval: U, null, `closedform` (3), two recipes × 2 arms |
| **total** | ≈ **9.6–13.8 h mandatory** (P1 + P2); ≈ **13.3–19.1 h** with P3; each 800-step retry adds ≈ 39–75 min per adapter (two adapters for a matched pair) | supersedes v1's totals and the stub's 2–3 h (`prereg_stubs.md:67`), which priced one adapter and no replication |

The baseline-only pre-training preflight (§2.8) and the P3 null evaluation are charged to this section; the totals above exclude them and cannot stand unchanged, so P1's measured times re-project them.

**Runtime guards.** For each adapter and each rank, time completed forward/backward/optimiser work with MPS synchronisation around the timing. After warm-up, project the declared 400- or 800-step attempt plus the final fit evaluation, and apply the 90-minute guard to every attempt. Measure a complete evaluation unit including the actual frozen five-shot prompts, all hooks and the mounted readout, and update the remaining-time projection before additional phases. If measurements exceed the revised schedule allowance above, HALT for the existing budget ruling before spending on additional units. Any eval process exceeding 4 h wall-clock HALTs. Timing does not change any scientific threshold. A runtime or memory guard miss produces HALT / INVALID-BUDGET, never FAIL-CEILING.

**Memory measurement.** Sample `torch.mps.driver_allocated_memory()` (current driver allocation, not a historical peak) after the forward, backward and optimiser stages, and record the maximum as the sampled peak MPS driver allocation; record CPU/process memory separately, without adding overlapping unified-memory measures. The 40 GB limit means 40,000,000,000 sampled driver bytes: equality passes, a larger observation HALTs. This is not a proof of the total unified-memory peak. An allocator/OOM failure HALTs with a diagnostic and no model-negative conclusion. CPU float64 diagnostics are serialised and included in the measured evaluation budget.

### 2.10 Records and outputs

Each phase writes into a fresh `results/c10w_oracle/<phase>_<UTC-timestamp>/` and **refuses to start if the directory exists**. Nothing is ever overwritten; this follows the "fresh OUT_DIR" rule of `EXPERIMENT_RUNBOOK.md:342`.
- Files: `step0.json`, `train_inputs.json`, `seal_audit.json`, `mmlu200.json` (step 0); `train/<arm>_s<seed>_r<rank>[_rt][_retry800].json` (one per training attempt); `eval.json` (U, every recipe's `run_recipe` outputs, all hook readouts, gates, `ZERO_ADAPTER_HITS`, `TRAINED_ORACLE_HITS`, LAW#5 (ii)–(v)); `verdict.json` (reader output, with the P1 re-projection); a run log. LAW#5 (vi) is in `step0.json`. Step 0's files are written once; every later phase reads them by path and SHA-256 and never regenerates them.
- Every JSON carries `"class": "ORACLE MEASUREMENT — not a route; never promotable as a write-engine result (D-C10r-rulings-3 (2))"` and the Decision-ID.
- **Edited weights are never committed.** Adapters are `adapters/*.safetensors`, ignored by `.gitignore:25`. Merged weights are never saved; they exist only in the eval process's memory and are restored by the harness. The reader refuses to proceed if any adapter path is tracked.

## 3. Pre-registered readings (exact counts; decision order fixed)

**Decision order:** validity (INVALID ends the reading) → binding count → locality and forgetting gates → per-configuration label → replication → capacity check (if triggered) → final label → O-A7-canon split → routing.

**Validity (any failure → INVALID; no label, no routing):**
- the fingerprint;
- the entry preflight (no INVALID-ENVIRONMENT) and the frozen-parameter hash check (§2.4);
- the seal (S1–S7 with S2c and S2d recorded and passing; `PTEST` absent from trainer inputs and source);
- the stimulus checks of arm U;
- LAW#5 (i)–(vi) (no INVALID-SEAM);
- LAW#3 (closed-form envelope, A1/A2 ≥ 68);
- **trainer positive controls O-A1 ≥ 68/72 and O-A2 ≥ 68/72** (P1), O-A1 s1 ≥ 68/72 (P2);
- the fit gate (train-EM ≥ 456/480; ≥ 23/24 for O-A7-canon) for every adapter whose arm is read;
- a matched O-A7-shuf control for every labelled O-A7 configuration (no INVALID-INCOMPLETE);
- the MMLU instrument (no INVALID-INSTRUMENT);
- every hash present and matching (adapter, `train_inputs.json`, trainer source, `mmlu200.json`, template sets);
- `para_string_n ≥ para_full_n` in every arm;
- every required metric present, finite and on its declared denominator (a missing or NaN metric is INVALID, never a silent gate pass);
- no runtime or memory guard miss (INVALID-BUDGET: HALT, never FAIL-CEILING).

**Gates on an O-A7 configuration** (vs the same-process closed-form A7 arm "A" and arm U; the contract's numbers, `prereg_stubs.md:10`; O-A7-canon is read on G1–G6 only):

| gate | rule |
|---|---|
| G1 | L1 flips ≤ A + 1 (of 12) |
| G2 | L3 ≥ 29/30 |
| G3 | `described_as` ≥ A − 3 |
| G4 | same-frame flips on `CANON` ≤ A + 1 (of 6), **and** for each training template t, flips(t) ≤ A(t) + 1 (of 6) |
| G5 | generic perplexity post − pre ≤ 0.5 |
| G6 | MMLU-200 net paired correct-item loss vs U ≤ 4 of 200 (integer; §2.6) |
| G7 | the matched O-A7-shuf control's original-map cross-score ≤ 2/72 (same rank, seed and training-attempt identity, §2.2; no -FRAME-HABIT) |

**Labels per configuration** (count = O-A7 `para_full_n` /72):
- **PASS-CEILING:** count ≥ 61 and G1–G7 all hold.
- **PARTIAL-CEILING-LOCALITY-COST:** count ≥ 61 with any of G1–G7 missed (the gate is named in the label). The ceiling with locality clean is not shown.
- **PARTIAL-CEILING:** 30 ≤ count ≤ 60; any gate miss is appended as a qualifier.
- **FAIL-CEILING:** count < 30; gate misses are reported.
- **INVALID:** any validity failure.
- Qualifiers carried and reported, not changing the band: -BIGRAM, -PAIRING-SPECIFIC, -RETRY800.
- **-MERGE-LOSS changes routing.** If it fires on any configuration that enters a replicated label, that label routes as **-UNSTABLE** (no routing; merged and mounted counts reported; diagnosis first, §5), with one exception: a configuration whose merged count is ≥ 61 with every gate holding and whose mounted count is higher than its merged count keeps its label (the merge lost and the merged result still passed). A merged FAIL or PARTIAL with -MERGE-LOSS is not read and cannot be interpreted as a model-capacity failure; the binding result stays the merged fp16 count, and any precision explanation stays a hypothesis.

**Reader boundaries (executable).** Count boundaries are 29 → FAIL, 30 → PARTIAL, 60 → PARTIAL, and 61 → PASS only when all required gates pass. Fit 455/480 misses and invokes the declared retry; 456/480 passes (O-A7-canon: 22/24 misses, 23/24 passes). Positive controls 67/72 miss and 68/72 pass. G1 and each G4 comparison permit exactly one additional flip; two additional flips miss. G2 permits 29/30 and misses at 28/30. G3 permits equality to A − 3; G5 permits equality to a +0.5 rise. G6 is evaluated as integer net correct-item loss ≤ 4/200: loss 4 passes, loss 5 misses. G7 cross-score 2 passes, 3 misses. Absolute seed gap 15 passes the numerical stability rule, 16 fails; same-seed gap 10 passes that numerical rule, 11 fails, subject also to the band/gate crossing rule. Absolute shuffled-own-score gap 15 is unqualified, 16 adds -PAIRING-SPECIFIC. Absolute merge/mount count gap 5 is unqualified, 6 adds -MERGE-LOSS. Exact equality to the LAW#5 limits 0.05 or 3 fails, because those inequalities are strict. LAW#3 envelope endpoints are inclusive. G3 and G5 use the harness's recorded precision consistently in both comparators: two decimal places for `described_as` and three for perplexity (`bandknob:163`, `:315`, `:337`; recorded precision, not a claim that the rounded values are exact).

**Replication (required before any label routes; a second seed in a second process).** At each rank the primary replicated count is min(count_s0, count_s1), both configurations valid, and the replicated label is computed from that count and the union of their gate misses. No count is combined with another rank's or seed's clean gates. **-UNSTABLE** (no routing; the operator is informed; diagnosis first) if: |count_s0 − count_s1| > 15/72 at either rank; or, at rank 16, the same-seed retrain differs from P1's seed 0 by > 10/72, **or** changes seed 0's count band (≤ 29, 30–60, ≥ 61), **or** changes any binding gate's (G1–G7) pass/fail result; or -MERGE-LOSS as above. Rank 64 has two-seed replication only; same-seed reproducibility at rank 64 is unmeasured. For calibration, the mint's init-seed range was 12/72 (`CORPUS/46…:22`) and the closed form's per-process spread ±3–5/72 (`CORPUS/44…:41`).

**Capacity check (P3) and final label.** P3 runs iff the replicated r = 16 label is PARTIAL-CEILING or FAIL-CEILING; it does not run on PARTIAL-CEILING-LOCALITY-COST (P3 is excluded after LOCALITY-COST by the preregistered scope and budget policy; this is not evidence that higher rank cannot improve locality), PASS-CEILING, INVALID or -UNSTABLE. The r = 64 label is computed on min(count_s0, count_s1) by the same rules. Scientific eligibility is necessary but insufficient: P2/P3 also require the recorded post-P1 budget authorization. Label order, best first: PASS-CEILING > PARTIAL-CEILING-LOCALITY-COST > PARTIAL-CEILING > FAIL-CEILING. Final PASS-CEILING requires at least one completed rank whose replicated count is ≥ 61 with every gate holding. If a required phase is incomplete, no final label is issued. Both ranks' counts, labels and gate misses are always reported. The final label is fixed by this table (every case covered, none overlapping):

| replicated r = 16 label | P3 | replicated r = 64 label | final label |
|---|---|---|---|
| INVALID, -UNSTABLE, or a required P1/P2 unit incomplete | not run | — | none: HALT, diagnosis (§5) |
| PASS-CEILING | not run | — | PASS-CEILING |
| PARTIAL-CEILING-LOCALITY-COST | not run | — | PARTIAL-CEILING-LOCALITY-COST |
| PARTIAL-CEILING or FAIL-CEILING | runs | INVALID, -UNSTABLE, or incomplete | none: HALT, diagnosis (§5) |
| PARTIAL-CEILING or FAIL-CEILING | runs | PASS-CEILING | PASS-CEILING (capacity r = 64) |
| PARTIAL-CEILING or FAIL-CEILING | runs | PARTIAL-CEILING-LOCALITY-COST | PARTIAL-CEILING-LOCALITY-COST (capacity r = 64) |
| PARTIAL-CEILING or FAIL-CEILING | runs | PARTIAL-CEILING | PARTIAL-CEILING |
| PARTIAL-CEILING | runs | FAIL-CEILING | PARTIAL-CEILING |
| FAIL-CEILING | runs | FAIL-CEILING | FAIL-CEILING |

The FAIL routing therefore requires both ranks to fail. The PARTIAL routing's reference count is set in the routing table below; a LOCALITY-COST count is reported beside it, never used as the reference.

**O-A7-canon split (read only for routing a PASS or PARTIAL).** canon_count = min(O-A7-canon s0, O-A7-canon s1), r = 16. The split is **READ** iff both canon adapters are valid (fit ≥ 23/24, provenance), |s0 − s1| ≤ 15/72, neither has -MERGE-LOSS, and G1–G6 hold at both seeds; otherwise it is **NOT-READ**. Cases: **(a)** READ and canon_count ≥ 30; **(b)** READ and canon_count ≤ 29; **(c)** NOT-READ.

**Routing (every case: "oracle measurement, not a route"; C10 stays OPEN/BLOCKING; nothing is promoted as a write-engine result):**

| final label | routing consequence |
|---|---|
| **PASS-CEILING** (either rank) | A merged delta confined to the five band matrices reached ≥ 61/72 held-out with the named gates holding, replicated (§0 says what this does not mean). Route on the O-A7-canon split. **(a)** Fitting at every position without extra frames already transfers: steps 6 (H-11), 7 (H-3) and 5b (joint output-margin solve, `docs/INTEGRATED_QUEUE_2026-10-07.md:23`) are motivated as independently pre-registered tests, with O-A7-canon's replicated count as their reference result (matching it does not prove an objective gap closed; exceeding it needs no model change). **(b)** The rank-16 canonical-only recipe did not reach a replicated minimum of 30/72. This does not establish that the extra frames caused the successful result. A rank-64 PASS has no matched rank-64 canonical control here. Steps 6–7 proceed only on their independent preregistered rationale; the result may motivate a separately preregistered multi-frame test without causal attribution. **(c)** The split is not read: steps 6–7 proceed on their own rationale only, with no attribution. H-30 weight grafting (`hypotheses.md:309–310`) becomes eligible as its own pre-registration in every case. |
| **PARTIAL-CEILING** (any form, incl. -LOCALITY-COST) | Training on this model beats the closed form (≈ 12/72) but does not reach the bar cleanly. Steps 6–7 may proceed as independently pre-registered tests. Under split (a) or (b), the reference is O-A7-canon's replicated count. Under (c), select the maximum replicated minimum among completed, valid, stable O-A7 ranks with G1–G7 passing at both seeds. If that set is empty, record reference_count = null and reference_status = NO-GATE-CLEAN-REFERENCE. Report attained counts and gate costs; do not substitute a costly count or issue a reference-based comparison. Matching the reference with another writer does not prove objective-gap closure, and exceeding it does not require a model change; a PARTIAL count is not an input to the model-axis decision. |
| **FAIL-CEILING** (both ranks) | FAIL-CEILING means that each evaluated rank's minimum across its two valid, stable seeds is below 30/72. It does not mean that every fitted adapter scored below 30/72. Report all seed counts; this is a recipe-level replication outcome, not a model-capacity bound (multi-token **string** value on these five matrices). This is not evidence against the model as a whole, nor that no solver can succeed: a minted single-token value on the same model and band already transfers 34–46/72 under the closed form (`CORPUS/45_C10L_MINT_TOKEN.md:61`). The result is surfaced to the operator for the ceiling-rule decision (D-C10k-rulings-2; `HANDOFF.md:56`) as evidence about the **string representation on this band under these recipes**, with recipe, representation, optimisation and merge precision still unresolved and the representation route (step 3, minting) named beside the model axis; it does not independently settle that decision. Steps 6–7 are deprioritised pending that ruling, not cancelled. Before the ruling, the operator may choose H-15 (full-band fine-tuning, `hypotheses.md:154–162`) as a stronger oracle. |
| **INVALID / -UNSTABLE / no final label** (a required phase incomplete) | No routing. HALT and diagnosis (§5). |

## 4. Not claimed, whatever the outcome; risks and confounds

**Never claimed:**
- that training is a write engine, a route, overlay-compatible, compactable, rollback-safe, deterministic enough for the §10.2 integrity check, or able to fit the §11.5.1 / §11.9 windows. None of these is tested (`council_critique.md:10`, `:13`, `:99–102`, `:201–204`, `:244`);
- the two-overlay composition, retraction and relation-family tests the consistency and graph lenses proposed (`council_critique.md:99`, `:130`, `:132`). These are route tests and belong to a route, which this is not;
- any change to C10's status, to F1, or to a CORPUS/37–53 label;
- "graph stored": at most "edge stored under one relation label" (`council_critique.md:14`);
- that the oracle's count is an upper bound on this model or on other writers, that matching it closes an objective gap, or that a PASS identifies a missing objective as the cause (§0);
- that the transfer measured here generalises beyond this fixed, test-aware-designed benchmark (§2.3);
- that a coined value became a semantic node. The loss is a string objective (`council_critique.md:133`).

**Risks and confounds:**
1. **Scope of a FAIL.** It covers the evaluated, fitted recipes only: LoRA at r ∈ {16, 64}, 20 templates, lr 3 × 10⁻⁴, 400 steps (800 on a retry), N = 24, one relation, fp16 merged eval. It is neither a model-capacity falsification nor evidence that no solver can succeed. A different representation already reached 34–46/72 with the closed form (the one-token mint, `CORPUS/45…:61`). An oracle FAIL below that is a negative result for this recipe on this representation, not for every write.
1b. **Position versus fitting.** Even O-A7-canon cannot say whether its gain comes from ΔW acting at every position or from iterative fitting; H-30 grafting (or a later position-restricted adapter) is the separating test, not this experiment.
2. **Training-family narrowness.** All 20 templates are capital-relation completions with the value last. The seal removes the held-out wordings, so transfer is to genuinely unseen wording, and the family's diversity bounds it. A FAIL may partly reflect the template family. The reviewer may propose further templates before freeze.
3. **Shared relation words.** `capital`, `city`, `of`, `is`, `the` occur in both sets. This is unavoidable, since the relation is the question. The seal is about distinctive wording and structure (§2.3).
4. **Bigram learning** (H-W3) is measured, not prevented (-BIGRAM).
5. **Values that contain subject names.** 8 heads are `FICTION` subjects, one its own (§2.1). This is measured by the shuffled control and sibling emission.
6. **fp32-trained adapter, fp16 merge.** Measured by merge versus mount (-MERGE-LOSS) and by the application-error readout.
7. **MPS non-determinism.** Measured by the same-seed retrain (-UNSTABLE rule).
8. **Locality coverage.** The battery measures named axes. Training changes `down_proj` at layers 4–8 for every token, so collateral off those axes is not measured. MMLU-200 is coarse: about 3.4 points sampling SE unpaired at 65 % accuracy. The floor is applied paired on identical items.
9. **Canonical count.** It is near-storage, because T01 = `CANON` is trained. It is reported, not binding.
10. **Bar selection.** 61/72 and 30/72 are the program's (`recommended_sequence.md:34–37`). The oracle's own per-process spread is unknown until P2 measures it.

**What this measurement cannot tell us:**
- whether any closed-form or solver objective reaches the oracle's count (that is what steps 6–7 test);
- which component or position carries the value (H-30);
- anything about the Incremental mode, the tier stack, drift or compaction (§D–§E of the e2e map);
- whether another model would do better (the model axis).

## 5. Halt discipline and close-out

**HALT conditions:**
- the fingerprint;
- any seal-audit failure at step 0;
- the stimulus leak;
- LAW#5 (i)–(v);
- LAW#3;
- a second fit-gate miss after `-RETRY800`;
- NaN/Inf loss;
- the training budget (> 90 min projected for any training attempt, an 800-step retry included), or a measured schedule above the revised §2.9 allowance;
- any eval process exceeding 4 h wall-clock;
- a sampled MPS driver allocation > 40,000,000,000 bytes, or an allocator/OOM failure (diagnostic, no model-negative conclusion);
- `para_string_n < para_full_n`;
- an oracle recipe meeting an arm without a registered adapter;
- INVALID-ENVIRONMENT, INVALID-SEAM or INVALID-INSTRUMENT at step 0 or at any process entry;
- a frozen (non-band) parameter hash changing in training;
- a band hash differing from the base after a mounted diagnostic or a `run_recipe`.

On a science-path or driver bug, at most one speculative fix after a `cat -n` read; if it does not clear the gate, HALT. A HALT writes a diagnostic JSON to `architecture_profile/sNNN_halt_diagnostic.json`, records the halt in `SESSION_CHECKPOINT.md` (plus a CORPUS note if it is a finding), and STOPs: no further phase. Close-out goes through `python3 tools/closeout_check.py D-C10w-oracle` once the CORPUS entry exists. The CORPUS entry, register row and overlay row carry "oracle measurement, not a route"; the overlay row is §8.2 D12, oracle measurement, no amendment. The advisor reviews before the run. The cross-family reviewer reviews at the design pass (done 2026-10-07 by Codex `gpt-6.1-sol` at max effort, not GPT-6-Astra high; §7), at the freeze check (S7 of the v2 strings, §2.3, by GPT-6-Astra high), at the implementation review, and at the verdict. This experiment runs only on the operator's go, with the GPU free (`docs/INTEGRATED_QUEUE_2026-10-07.md:43`).

## 6. Reviews

v1 draft → advisor pass → Codex design pass (incl. S7 adjudication; `gpt-6.1-sol`, max) → **v2 (this file)** → freeze check (lead read-through; cross-family S7 verdicts on T14, R1 and R2; the rulings in §8) → freeze → implementation (Codex, model-free, per D-C10r-rulings-9 (3), `EXPERIMENT_RUNBOOK.md:342`): `c10w_oracle_step0.py`, `c10w_oracle_train.py`, `c10w_oracle_eval.py`, `c10w_oracle_read.py` → implementation review → step 0 → P1 → P2 → (P3) → verdict review → CORPUS/NN.

## 7. Review fold log

Fold of 2026-10-07 (v1 → v2). Reviews: advisor = `results/c10w_oracle_advisor_v1.md` (Claude Opus 5.5, FIX-FIRST, 6 BLOCKING); Codex = `results/c10w_oracle_codex_design_v1.md` (`gpt-6.1-sol` at max effort, not GPT-6-Astra high; FIX-FIRST, 8 BLOCKING; reviewed v1 SHA-256 `7bb764ff…511f4e`, which is the committed v1). Fold rule: where the reviews conflict, the option that halts, blocks routing or claims less is taken.

- advisor #1 (BLOCKING) — applied-with-change: O-A7-canon added (§2.2, §2.5, §2.8, §2.9) and the PASS/PARTIAL routing split on it as written; worded per Codex #1 ("motivated as independently pre-registered tests", "reference result" instead of "proceed" and "reference ceiling"), and the split is READ only with valid fits, a seed gap ≤ 15 and G1–G6 at both seeds, with a NOT-READ case (c).
- advisor #2 (BLOCKING) — applied-with-change: H-W1 mechanism, loss-row reason and the §0 correction applied; "the wall this experiment bounds" reworded to "the gap this experiment measures against", and the replacement PASS-row sentence ("the closed form's shortfall is therefore in what its solve constrains") not used, because Codex #1 forbids a causal reading of a PASS; the PASS row no longer makes that claim.
- advisor #3 (BLOCKING) — applied: S2c widened and S2d added; T06, T09, T14 and reserve R1 replaced; new reserves; both SHA-256 values recomputed with stdlib (the same script reproduces the v1 hashes); "more than two rejections"; audit sentence names the rejected strings. Conflict 1.
- advisor #4 (BLOCKING) — applied-with-change: label order and P3 trigger (not on LOCALITY-COST) adopted; the final label is a complete truth table that also carries Codex #3's rules (PASS needs one clean ≥ 61 rank; no count combined with another rank's gates; incomplete → no label). Conflict 2.
- advisor #5 (BLOCKING) — applied-with-change: -MERGE-LOSS → -UNSTABLE adopted; "a merged PASS stays PASS" narrowed to a merged PASS whose mounted count is higher (the merge lost and still passed); a merged PASS with a mounted count lower by ≥ 6 is an anomaly and routes -UNSTABLE. Conflict 7.
- advisor #6 (BLOCKING) — applied: FAIL row reframed to the string representation with minting named; H-W0's "below the bar" corrected (the H-W0 text is Codex #3's, which says below 30/72).
- advisor #7 (ADVISORY) — applied: -BIGRAM fires at X ≥ ⌈C/2⌉ over facts with c_k = 1. Conflict 5.
- advisor #8 (ADVISORY) — applied-with-change: superseded by Codex #4's matched controls, which cover r = 64 seeds 0 and 1 and also r = 16 seed 1 and the retrain. Conflict 3.
- advisor #9 (ADVISORY) — applied: P1 re-projection into `verdict.json`; HALT on an eval process > 4 h; budget recounted in §2.9 together with Codex #8.
- advisor #10 (ADVISORY) — applied-with-change: dataset revision pin and the five-dev-items assertion applied (through Codex #7's text); the floor max(4, closed-form A7 net loss + 2) declined, because Codex #3 fixes G6 at net loss ≤ 4 and the stricter gate is the conservative option. Conflict 4.
- advisor #11 (ADVISORY) — applied: queue citation `:37` → `:43` (header and §5); the CORPUS/45:28 sentence now says minted-token closed form, with arm A measuring the multi-token one.
- advisor #12 (ADVISORY) — applied: §4 risk 1b.
- Codex #1 (BLOCKING) — applied: §0 question and interpretation paragraph, the H-W1 mechanism (merged with advisor #2, plus `compute_ks.py:19–37` and `subject_last`), the §3 routing rows, §4 risk 1 and two "never claimed" items; the labels keep their v1 names, with "CEILING" noted as a role, not a bound.
- Codex #2 (BLOCKING) — applied: authorship paragraph replaced; S7 recording requirements; the actual reviewer model recorded; the verdicts are the §2.3 seal audit table; accepting the blind-authorship departure is in §8. Conflict 1.
- Codex #3 (BLOCKING) — applied-with-change: H-W0, the replication rule with band/gate crossing, the final-label rules and the reader boundaries applied; P3 does not run on LOCALITY-COST, against this item's text. Conflict 2.
- Codex #4 (BLOCKING) — applied: matched O-A7-shuf controls for r = 16 s1 and the s0 retrain and r = 64 s0 and s1; G7 per configuration; INVALID-INCOMPLETE; the matched-pair step-count rule; phase and budget tables updated.
- Codex #5 (BLOCKING) — applied: LAW#5 (vi) nonzero seam check at r = 16 and 64; split hit counters; band hash after every mounted diagnostic; -MERGE-LOSS not a capacity failure. The LAW#3 envelope is retained, as this item adjudicates.
- Codex #6 (BLOCKING) — applied: entry preflight for step 0, the trainer and eval (`MODEL_ID`, `MODEL_REV`, `LLMDB_DEVICE`; paths resolved before chdir; `mps` required; revision, dtype, device and hashes recorded); frozen-parameter hash check; the CPU-then-float64 rule.
- Codex #7 (BLOCKING) — applied: MMLU acquisition at a pinned commit, ordering, prompt freezing, token checks, tie order, net-loss definition, one shared `mmlu200.json`, INVALID-INSTRUMENT.
- Codex #8 (BLOCKING) — applied: inventory recounted (15 adapters, recipe setup, U/null/mounted evaluations; retries priced separately) with revised projections of 9.6–13.8 h mandatory and 13.3–19.1 h with P3; the 90-min guard on every attempt including retries; MPS-synchronised timing; sampled driver-allocation peak with the 40,000,000,000-byte limit; `use_cache=False`; INVALID-BUDGET, never FAIL. The new total goes to the operator (§8).
- Codex #9 (ADVISORY) — applied-with-change: H-W3 reworded; NOT-EVALUABLE, the denominators and the PASS-BIGRAM wording adopted; the threshold X_success = C replaced by advisor #7's X ≥ ⌈C/2⌉. Conflict 5.
- Codex #10 (ADVISORY) — applied: compute-dtype reason replaced.
- Codex #11 (ADVISORY) — applied: "Order of correctness controls" added to §2.7.

Fold of 2026-10-07 (v2 → v2.1), review `results/c10w_oracle_astra_freeze_v2.md` (GPT-6-Astra, high; FIX-FIRST; S7 22 ACCEPT / 0 REJECT):
- Astra-freeze #1 (BLOCKING) — applied: reviewer text added at §2.7 and the start of §2.8, P3 evaluation sequence replaced; budget charge stated in §2.9 as a note without new totals (reviewer gave no numbers; P1 measured times re-project them), and "null" added to the P3 eval list; existing P1 step 3 post-training eval order kept as the repeat-controls process.
- Astra-freeze #2 (BLOCKING) — applied: §3 PASS (b) and the line-53 ablation sentence replaced with reviewer text.
- Astra-freeze #3 (BLOCKING) — applied: PARTIAL row reference-selection sentences replaced; the former closing sentence on LOCALITY-COST counts is subsumed by the reviewer text.
- Astra-freeze #4 (BLOCKING) — applied: reviewer FAIL sentence placed at §0 and the FAIL row; the surrounding "not a model-capacity falsification" clauses retained (closest faithful version, not a literal whole-sentence swap).
- Astra-freeze #5 (BLOCKING) — applied: §8 opening and items replaced; the pending-acceptance sentence replaced; authorization sentence appended to the P2 and P3 phase paragraphs and the §3 P3 paragraph.
- Astra-freeze #6 (ADVISORY) — applied: batch/epoch text replaced (rows in §2.4; the steps row now defers to it) and the "cannot repair a locality miss" rationale replaced at §3 and conflict 2 in §7.
- Program check of the v2.1 fold (2026-10-07): the P1 step list still opened with training and its step 4 implied continuation within budget; added P1 step 0 (the baseline-only preflight, as a numbered step) and replaced step 4's last sentence with the stop rule of §8 item 3.
- Astra-freeze #7 (ADVISORY) — declined: reviewer states no replacement is required (fold-accounting verification; its S7 table is added to §2.3 instead).

**Conflicts between the reviews and how they were resolved (the more conservative option each time):**
1. S7 seal: advisor #3 rejects v1 T06, T09, T14 and R1 by S2c/S2d; Codex #2 accepts all 23 strings. The rejections stand (stricter seal). T06 and T09 of v2 are v1 reserves Codex accepted; T14, R1 and R2 of v2 have no cross-family verdict, so freeze is blocked until they get one (§2.3 S7).
2. P3 on PARTIAL-CEILING-LOCALITY-COST: advisor #4 says no; Codex #3 says yes. Not run: running it could only upgrade the claim. P3 is excluded after LOCALITY-COST by the preregistered scope and budget policy; this is not evidence that higher rank cannot improve locality.
3. Shuffled controls: advisor #8 adds one r = 64 seed-0 control; Codex #4 requires a matched control for every labelled configuration. Codex's (more controls, more INVALID paths).
4. MMLU floor: advisor #10 proposes max(4, closed-form A7 net loss + 2); Codex #3 fixes net loss ≤ 4. Fixed ≤ 4 (stricter gate, so a PASS is harder).
5. -BIGRAM threshold: advisor #7 X ≥ ⌈C/2⌉; Codex #9 X_success = C. Advisor's (fires more often, so a PASS is qualified more often).
6. PASS/PARTIAL routing: advisor #1 "steps 6–7 proceed with O-A7-canon's count as their reference ceiling"; Codex #1 "may motivate independently pre-registered tests; a reference result, not an upper bound". Codex's wording on the advisor's split.
7. -MERGE-LOSS: advisor #5 routes it as -UNSTABLE; Codex #5 keeps the merged count binding and reports the gap. Advisor's (blocks routing), narrowed as in advisor #5's line.

**Citation note.** `recommended_sequence.md` line citations in this file use its numbering at commit afb8780 (the v1 base). Commit 7b9a30d prepended a two-line correction note, so current line = cited line + 2. Not renumbered, because no review item touches those lines.

**v1 author's decisions where the sources were silent, or where this draft departs from the stub (each one is for the reviewers to overturn):**
1. Fixed authored templates, published and audited, instead of base-model generation (stub `prereg_stubs.md:64`). Reasons in §2.3.
2. The seal rule S1–S7: banned-word and banned-bigram sets derived mechanically from `PTEST` minus `CANON`; an authored synonym extension; S3 threshold 0.60; S2c for Q2's shape; S5 probe-frame exclusion; S7 reviewer adjudication with three fixed-order reserves.
3. A trainer process isolated from the harness (no `PTEST` in its inputs or source).
4. Hand-written LoRA (no `peft`), α = r, A kaiming-uniform / B = 0, dropout 0.
5. lr 3 × 10⁻⁴, AdamW, 20-step warm-up, clip 1.0, batch 24, 400 fixed steps, no early stop (stub's early stop replaced, `hypotheses.md:140`); fit gate 456/480; one retry at 800 steps.
6. fp16-loaded base upcast to fp32 for training; fp16 merge for eval (the harness's dtype).
7. Rank sweep {8, 32} replaced by one conditional capacity check at r = 64 that guards the FAIL routing.
8. Forgetting instrument: MMLU-200 from `cais/mmlu` (download), seed 20261007, 5-shot, letter-logit scoring, floor U − 2 points; generic perplexity +0.5 kept.
9. Shuffled control as a shift-by-1 derangement; cross-score gate ≤ 2/72; -PAIRING-SPECIFIC at a gap > 15/72.
10. A2 trainer control added beside the requested A1 (shared contract, `prereg_stubs.md:9`).
11. Arm U's A7 leak gate ≤ 2/72, on top of the harness's 15 % canonical gate.
12. "≥ 61 with a gate miss" read as PARTIAL-CEILING-LOCALITY-COST, not PASS and not INVALID.
13. Replicated label on the minimum of two seeds; -UNSTABLE at a seed gap > 15/72 or a same-seed gap > 10/72.
14. The per-training-frame bystander gate is compared against the closed-form arm in the same frame.
15. -LARGE-WRITE reported, not gated; covariance-weighted norm and null(C) share reported.
16. The LAW#3 envelope is CORPUS/44 A4's [5, 18] / [42, 59] / [5, 10], not the mint reader's [11, 18].
17. LAW#5 for a non-engine writer: delegation, zero-adapter bit-identity, restore round trip, hit count; merge versus mount reported.
18. Budget and memory stop rules (90 min per adapter projected; 40 GB peak).
19. Output layout, the fresh-directory refusal, adapters as git-ignored `.safetensors`, and the four script names.
20. The routing for PARTIAL-CEILING (steps 6–7 proceed with the oracle as reference ceiling; the model axis surfaced in parallel), which the sources leave between "pass" and "fail".


## 8. Open for the program

These rulings are settled by the program's freeze-check instruction:
1. The blind-authorship departure is ACCEPTED, with the disclosure and restricted interpretation in §2.3.
2. This freeze check is the GPT-6-Astra/high pass. Its S7 judgments supplement the earlier gpt-6.1-sol/max design review; any reviewer REJECT remains binding. The present verdict is FIX-FIRST.
3. P1 alone is approved. After P1, record measured training/evaluation times and separate P2/P3 projections. Stop before either additional phase until its authorization is recorded. Estimates below an allowance do not authorize continuation. Without required replication, issue no final scientific label or routing.
