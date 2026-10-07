# Pre-registration — D-C10w-oracle: a merged band-LoRA trained on the 24 coined facts, scored on the C10 harness, as a ceiling measurement (ORACLE MEASUREMENT, NOT A ROUTE) (step 5 of the research pass's recommended sequence; H-13) (v1, 2026-10-07)

**Status: v1 DRAFT — for advisor + Codex review; not frozen.** Nothing has run; no driver exists. Decision-ID `D-C10w-oracle`. Every output of this experiment (title, record files, verdict, CORPUS entry, register row) carries the label **"oracle measurement, not a route"**. A result here can never be promoted as a write-engine result, and a pass does not change C10's status (`results/research_pass_2026-10-06/prereg_stubs.md:62`).

Source lead: research pass 2026-10-06, H-13 (`results/research_pass_2026-10-06/hypotheses.md:135–145`), with H-15 as the stronger oracle not run here (`hypotheses.md:154–162`) and H-30 as the conditional follow-up (`hypotheses.md:309–310`); the step-5 stub (`prereg_stubs.md:59–67`) under the shared contract (`prereg_stubs.md:5–13`); the sequence row (`recommended_sequence.md:25`); the council's H-13 objections (`council_critique.md:7–13`, `:63–79`, `:97–107`, `:128–133`, `:163–168`, `:198–206`, `:238–250`). Lineage: CORPUS/44 ⟨D-C10l-covgeom@af2e38f7⟩ (identical-baseline envelope, `CORPUS/44_C10L_COVGEOM_SPARSEBAND.md:39`; ρ correction, `:43`), CORPUS/45 ⟨D-C10l-mint@a4a6f4c7⟩ (A1 68–72/72 under the write and the one-token mint at 34–46/72, `CORPUS/45_C10L_MINT_TOKEN.md:1`, `:61`), CORPUS/46 Q3 (mint seed range 46/34/36, `CORPUS/46_C10M_DIAG_READPARTITION_EDITINJECT.md:22`), CORPUS/49 (same-frame probe pre-edit 1/6, `CORPUS/49_C10P_TWOPASS_SOLVE.md:12`). Format and conventions follow `docs/C10V_LAYERPICK_PREREG.md` (v2) and `docs/C10U_MINT2_PREREG.md` (v3).

**Operator rulings that bind this design (quoted):**
- **Write-only ruling, D-C10r-rulings-3 (2)** (`EXPERIMENT_RUNBOOK.md:330`, §5.2): *"training per commit defeats the spec's objective; likelihood of deploying it is essentially zero; run it only as a measurement — H-13/H-15 are an oracle measurement, not a route."* The research pass's first decision says the same: *"Any route that needs a training set or a training loop per commit is not a route"* (`HANDOFF.md:7`; ranking criterion 1, `recommended_sequence.md:11`).
- **Step 5 moved ahead of step 4, D-C10r-rulings-9 (2)** (`EXPERIMENT_RUNBOOK.md:342`; queue row `docs/INTEGRATED_QUEUE_2026-10-07.md:19`).
- **Local only**: the M3 Pro, Apple MPS, no CUDA, no rented compute; MPS has no float64 (`experiments/track_c/c10l_mint_lib.py:66`).
- **One GPU run at a time** (`docs/INTEGRATED_QUEUE_2026-10-07.md:37`); the MEMIT engine under `memit_dry_run/memit` stays UNMODIFIED (LAW#5); the LAWs, halt discipline and close-out gate of `CLAUDE.md` bind unchanged.

## 0. Where this sits, and what it is

**The e2e map (`docs/SPEC_E2E_GROUND_TRUTH.md`, binding per `DISCIPLINE.md:30`).** Layer: the **Write Engine** (§8; `SPEC_E2E_GROUND_TRUTH.md:14`), at the cell where the write path's Commit Executor calls MEMIT (§C step 5, `SPEC_E2E_GROUND_TRUTH.md:22–30`). This experiment replaces the MEMIT solve with gradient training, which puts it **outside the spec's write path**: the spec designates MEMIT and excludes full fine-tuning (`research_and_specs/llm-as-database-v1_2-integrated-spec.md:313`). It is an oracle beside the write path, read against the §8.9 bar (`spec:388`). Its readouts mirror the §F split (`SPEC_E2E_GROUND_TRUTH.md:64–65`): storage (training-phrasing exact match, canonical prompt) and behaviour (held-out paraphrase) are separate columns. Nothing in the Schema, Validation, Security, State Consistency or Orchestration layers is touched.

**SPEC-FIRST (`DISCIPLINE.md:32`).** The spec already settles whether training is a write engine: it is not (`spec:313`). That is why this is a measurement and why H-13's spec amendment (`hypotheses.md:142`) is **not pursued**. The council's objections about composition (§8.10 D62), rollback (§8.4), transaction windows (§11.5.1, §11.9), determinism (§12.2) and integrity (§10.2) (`council_critique.md:10`, `:13`, `:99–102`, `:201–204`, `:244`) are objections to H-13 **as a route**. They are listed in §4 as untested and not claimed. They are not run here.

**The question, in the research agent's words:** *"If even training cannot reach the bar on this model, no solver will, and the question becomes the model. If training reaches it, the wall is a missing objective that steps 6 and 7 can supply inside the solver"* (`recommended_sequence.md:25`). Pass → spend the engine days (steps 6–7). Fail → the model axis (operator decision on the ceiling rule, `HANDOFF.md:56`).

**What it can and cannot conclude.** It measures one strong training recipe: LoRA on the five band `down_proj` matrices, every value token in the loss, 20 sealed-safe phrasings, rank 16 with a conditional rank-64 capacity check. A PASS shows that these five matrices of this model *can* hold the 24 coined values with held-out transfer at the bar and locality clean. A FAIL shows that *this recipe family* cannot. The step from that to "no solver will" is an inference with this scope (§4). It is not a proof.

## 1. Question and hypotheses

- **H-W1 (reachable ceiling):** a merged rank-16 LoRA on `down_proj` L4–8, trained with token-level cross-entropy on every value token over 20 training phrasings that are sealed against the held-out templates, reaches ≥ 61/72 on the A7 held-out full-sequence count with every locality and forgetting gate holding. The mechanism claim is H-13's: the loss acts on every value token at every position in every phrasing, which the closed-form write lacks (`hypotheses.md:136`).
- **H-W0 (null, the model is the wall):** it stays below 30/72 with the trainer's positive controls passing and the training set fitted, and the rank-64 capacity check also stays below the bar.
- **H-W2 (trade-off):** it reaches the bar only at a locality or forgetting cost. This is the axis the source failed on: out-of-domain score 57.0 → 52.0 → 40.2 as rank grows (`hypotheses.md:137`).
- **H-W3 (bigram, not binding):** a high count comes from value-internal continuation ("head → modifier" regardless of subject) rather than a bound fact (`council_critique.md:69`). The bigram control (§2.6) tests it.

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

### 2.3 Training data and the seal

**Decision: fixed, authored, relation-level templates instead of base-model generation.** The stub asked for about 20 phrasings per fact generated by the pristine base checkpoint (`prereg_stubs.md:64`). This draft publishes 20 fixed templates instead, for four reasons:
1. They can be reviewed before freeze.
2. They are deterministic. No generator prompt exists to leak or to sample on MPS.
3. The consistency lens's read-your-writes concern cannot arise, because no model generates the training data (`council_critique.md:100`).
4. The memit lens's objection that model-generated frames cover the held-out templates (`council_critique.md:73`) applies to generation just as much.

The authorship fault the council named, that whoever authors the set has seen the sealed templates (`council_critique.md:8`), is not removed by any generation scheme. The remedy here is the mechanical audit, an independent adjudication, publication before freeze and hashing. The author stage is the program session, at v1.

**The training set.** 20 templates × 24 subjects = 480 items per adapter, each `template.format(subject)` followed by `" " + value`. The same 20 templates are used for A1, A2, A7 and A7-shuf.

| id | template | max S3 vs Q1–Q3 |
|---|---|---|
| T01 | `The capital of {} is the city of` (= `CANON`, the program's write prompt) | 0.469 |
| T02 | `The capital of {} is` | 0.551 |
| T03 | `Q: What is the capital of {}? A:` | 0.492 |
| T04 | `Question: Which city serves as the capital of {}? Answer:` | 0.466 |
| T05 | `Capital of {}:` | 0.444 |
| T06 | `Encyclopedia entry: {}. Capital:` | 0.500 |
| T07 | `In an atlas, the entry for {} lists the capital as` | 0.523 |
| T08 | `Every map of {} marks the capital as` | 0.480 |
| T09 | `The capital of the nation of {} is` | 0.578 |
| T10 | `The country {} has the capital` | 0.551 |
| T11 | `Officially, the capital of {} is` | 0.486 |
| T12 | `The national capital of {} is` | 0.538 |
| T13 | `The capital of {} is the town of` | 0.469 |
| T14 | `Reference card for {}. Capital:` | 0.471 |
| T15 | `The official capital of {} is the city of` | 0.425 |
| T16 | `The capital of {} is located in` | 0.540 |
| T17 | `The capital of {} has always been` | 0.462 |
| T18 | `Historians agree that the capital of {} is` | 0.444 |
| T19 | `On the map, the capital of {} appears as` | 0.477 |
| T20 | `Geography quiz: the capital of {} is` | 0.459 |

SHA-256 of the 20 templates joined by `"\n"` in the order T01–T20: `55363a859fe24559ae1f37334f8d167f7049835c90005269943a4bef19a70bda`. **Reserve list**, used in this fixed order to replace any template the audit or the adjudication rejects: R1 `The capital of the republic of {} is`, R2 `According to the records, the capital of {} is`, R3 `Fact: the capital of {} is`. SHA-256 of the reserves joined the same way: `c0ef01e366c3e6895a6789f8c551ed6254d1b2d279314afe9879b01aec267fd5`. All three pass every mechanical rule (max S3 0.565, 0.426 and 0.514).

**Why a seal, and the rule (`results/autoresearch_c10_heldout_mirroring_2026-10-06.md`).** That note found an earlier write-prompt set containing close paraphrases of the sealed templates: `{}'s capital is the city of` for Q1, `When you travel to {}, the capital is the city of` for Q2, and `The largest city and capital of {} is the city of` for Q3 (`:5–9`). The inflation was clear on Q1 (4 → 10 the run its paraphrase was added, `:36`), and the loop's held-out score stopped measuring transfer to unseen wording (`:30`). Every training phrasing asks the same relation as the held-out templates; that is the point of a transfer test. **"Paraphrase of a held-out template" here means sharing its distinctive wording or its distinctive structure.** It is enforced by S1–S7, all of which must pass for every template:

Normalisation: `tokens(s) = re.findall(r"subj|'s|[a-z]+", s.lower().replace("{}", " subj "))`. `Q1, Q2, Q3` = `PTEST` in order. `CANON` words and bigrams are exempt, because `CANON` is the write prompt by construction.
- **S1 — banned words.** No token in `B = (words(Q1) ∪ words(Q2) ∪ words(Q3)) − words(CANON)`, computed: `'s, and, called, government, if, its, main, seat, visit, you`. No token in the authored synonym extension either: `name named names known call calls refer refers referred title titled visiting visits visitor visitors travel travels traveling travelling traveler travelers traveller travellers go goes going trip tour tourist tourists when whenever once your yours principal chief largest biggest primary leading foremost administrative administration govern governs governed governing governmental parliament seated sits sit power ruling rule rules` (67 banned words in total).
- **S2 — banned bigrams and openings.** No bigram in `bigrams(Q1 ∪ Q2 ∪ Q3) − bigrams(CANON)`, computed: `('s, capital) (and, seat) (capital, city) (city, and) (city, is) (government, of) (if, you) (is, called) (its, capital) (main, city) (of, government) (seat, of) (subj, 's) (subj, its) (the, main) (visit, subj) (you, visit)`. No template may open with `subj 's` (Q1's possessive opening).
- **S2c — Q2's shape.** No template in which the subject slot is followed by a clause break and then a clause predicating the capital: the regex `\{\}\s*[,:;—-].*capital.*\bis\b` must not match.
- **S3 — surface similarity.** `difflib.SequenceMatcher(None, " ".join(tokens(T)), " ".join(tokens(Qj))).ratio() < 0.60` for each j. For reference, `CANON` scores 0.438 / 0.423 / 0.469.
- **S4 — no entity leak.** No token, case-insensitive, equal to a `FICTION` subject, a `FRAME_SUBJECTS` name, a `coined_head` or `coined_mod` word (`bandknob:229–238`), any country or capital of either g6 screen (`configs/screens/g6_screen_qwen3b*.json`), or an A1/A2 value. Exactly one `{}` slot.
- **S5 — no locality-probe frame.** No bigram `(is, described)`, `(is, a)` or `(is, associated)`. The `described_as` gate and the `is_a` / `associated_with` relation probes must stay bystanders, not training frames.
- **S6 — trainer isolation.** The trainer reads only `train_inputs.json` (templates, `FICTION`, value maps, target ids). Step 0 asserts that none of the three `PTEST` strings, and none of their normalised token strings, is a substring of that file. It also asserts that the trainer source contains neither the strings `c10e_bandknob` nor `PTEST`. The trainer never imports the harness.
- **S7 — independent adjudication.** At the design pass, the cross-family reviewer (GPT-6-Astra, high) receives the 20 templates, the reserves and the three held-out templates, and is asked to name any template it judges a paraphrase of a held-out template under the definition above. Each named template is replaced by the next reserve. The audit is re-run, and the replacement and the reviewer's verdict per template are recorded in `seal_audit.json` before freeze. More than three rejections exhaust the reserves → the design returns to v2 authoring (no ad hoc additions at freeze).

**Audit results at v1** (computed with exactly the rules above; Python stdlib, no model): all 20 templates and all 3 reserves pass S1–S5; the largest S3 is 0.578 (T09 against Q3). **Two authored candidates were rejected before the list was fixed:** `For {}, the capital is` (S3 0.667 against Q2, and S2c) and `Among the facts about {}: the capital is` (S2c; S3 0.564). Both have Q2's "phrase containing the subject, then a clause about the capital" shape. Step 0 recomputes every rule with the harness's actual constants and the engine's tokenizer, and halts on any difference from this table.

### 2.4 The LoRA writer (`experiments/track_c/c10w_oracle_train.py`, one OS process per adapter)

Hand-written LoRA, no `peft` (not installed, §2.1; a hand-written adapter also makes ΔW explicit). Each `model.layers.{ℓ}.mlp.down_proj` for ℓ ∈ {4, …, 8} is wrapped so that `y = W x + s · B (A x)`, with A ∈ ℝ^{r×11008}, B ∈ ℝ^{2048×r}, s = α / r. The merged delta is **ΔW_ℓ = s · B_ℓ A_ℓ** (2048 × 11008, the weight's own shape). Every other parameter is frozen.

| hyperparameter | value | reason |
|---|---|---|
| target matrices | `down_proj` at layers 4, 5, 6, 7, 8 only | the same five matrices the closed form edits (`hparams:2`, `:13`); the oracle asks whether *these* can hold the value |
| rank r | 16 (binding); 64 only in the conditional capacity check (§3) | 16 is the stub's (`prereg_stubs.md:63`) and the source's middle rank (79 % paraphrase exact match at r = 16, `hypotheses.md:137`). The stub's exploratory r ∈ {8, 32} is replaced by one larger rank: a smaller rank cannot strengthen a ceiling, and a larger one guards the FAIL routing against the graph lens's capacity objection (rank 16 < 24 facts, `council_critique.md:131`) |
| α | equal to r (scale s = 1.0) | keeps the learning rate interpretable across r = 16 and 64; one knob fewer |
| init | A ~ `kaiming_uniform_(a = √5)` (the common LoRA default), B = 0 | ΔW = 0 at step 0, so training starts exactly at the base model |
| dropout | 0 | deterministic forward; a ceiling run has no reason to regularise by noise |
| base weights in training | loaded with `torch_dtype=torch.float16` (as `bandknob:48`), then `.float()` | the base weights are exactly the fp16 values the eval model holds, upcast. The adapter is trained against the weights it will be merged into |
| compute dtype | fp32 on MPS for forward and backward; LoRA parameters and AdamW state fp32 | fp16/bf16 training on MPS would need loss scaling; LoRA gradients are small. No float64 on MPS (`c10l_mint_lib.py:66`). CPU-side diagnostics may use float64 |
| loss | token-level cross-entropy over **every value-token position** (labels = target ids; prompt positions −100); mean over all value tokens in the batch | the H-13 mechanism (`hypotheses.md:136`); a token mean does not down-weight 6-id values against 4-id ones |
| sequence | `tok(template.format(subject))["input_ids"] + tgt_ids(value)`, right-padded with `eos` and an attention mask | exactly the tokenisation the harness scores (`bandknob:67–68`, `:109–117`); Qwen2 positions are unaffected by right padding |
| optimiser | `torch.optim.AdamW`, lr 3 × 10⁻⁴, β = (0.9, 0.999), ε = 10⁻⁸, weight decay 0; linear warm-up over 20 steps from 0, then constant; gradient-norm clip 1.0 | a standard LoRA range, at its upper end because a ceiling run must fit; no schedule search (no held-out data may select anything) |
| batch | 24 items; each epoch is one seeded permutation of the 480 items (`torch.Generator().manual_seed(1000·seed + epoch)`) | 20 steps per epoch |
| steps | **400, fixed** (20 epochs); no early stopping | an early stop on training-phrasing EM (`hypotheses.md:140`) makes the step count data-dependent (`council_critique.md:202`); the fit gate below replaces it |
| seeds | binding seed 0; replication seed 1; same-seed retrain seed 0 in a fresh process | `torch.manual_seed(seed)` before init; seed 1 varies init and order; the retrain measures MPS non-determinism (`council_critique.md:13`, `:244`) |

**Training readouts (storage column; no held-out data in this process).** The loss every 10 steps; train-EM at the end on all 480 items, per template (/24) and per fact (/20). Train-EM is computed by teacher-forced argmax in batched forward passes. This is exactly equivalent to greedy full-sequence match: the greedy sequence equals the target iff the argmax at every target position, given the target prefix, equals the target id. Also recorded: wall-clock per step, total training wall time (reported as the "lock hold time" the orchestration lens asked for, `council_critique.md:206`, record only), and peak MPS memory (`torch.mps.driver_allocated_memory()`). **Fit gate (validity):** train-EM ≥ 456/480 (95 %) for every adapter. A miss gets **one pre-declared retry** at 800 steps with everything else identical, labelled `-RETRY800`. A second miss → that adapter is INVALID-UNDERFIT and the phase HALTs (§5).

**Outputs per adapter:** `adapters/<tag>.safetensors` holding A_ℓ, B_ℓ (fp32), s and the layer list. Its SHA-256, the `train_inputs.json` SHA-256, the trainer source SHA-256, the model revision and the package versions go into `train/<tag>.json`.

### 2.5 Evaluation on the standard harness (`experiments/track_c/c10w_oracle_eval.py`)

The eval driver imports the harness as `H` (fp16 model, `bandknob:48`), does not call `H.main()`, and calls `H.run_recipe` per recipe with `H.ARMS` set per recipe. It refuses to start if any inherited harness knob is set: `C10_KEY_LOCUS`, `C10_CTX_TEMPLATES`, `C10_ARMS`, `N_EDIT`, `C10_SUBJECT_OFFSET`, `HP_CANDIDATE`, `C10_PROJECTOR`, `C10_RECIPES` (the refusal C10V records, `C10V_LAYERPICK_PREREG.md:60`). `LLMDB_ROOT` must resolve to this worktree's root: the shell profile points it at the main checkout (`memory_mirror/llmdb-root-env-points-at-main-checkout.md`), and `bandknob:2–8` derive the engine, configs and `HF_HOME` from it.

**The write seam (no harness edit).** The driver rebinds `H.my_edit` to `oracle_edit(hp, requests, P, cache_c)`, keeping the original object as `ORIGINAL_MY_EDIT`. This is the rebinding mechanism of `C10V_LAYERPICK_PREREG.md:51`. Its behaviour:
- `MODE = "closedform"` → always delegate to `ORIGINAL_MY_EDIT` (the harness exactly).
- `MODE = "oracle"` → if `H._LAW5_DEFAULT_CTX` is True (`bandknob:403`, `:430`), delegate, so the standing LAW#5 gate always runs the engine-parity path. Otherwise, look up the adapter registered for `frozenset((rq["subject"], rq["target_new"]["str"]) for rq in requests)`. **No registered adapter → raise and HALT** (never a silent fallback to the closed form). Then:
  1. Assert that the SHA-256 of the five band tensors equals the base-snapshot hash taken at process start. This proves the harness restored the weights before this arm (`bandknob:473`).
  2. Verify the adapter file's SHA-256 against its training record.
  3. For each ℓ in `hp.layers` (must equal the adapter's layer list), compute ΔW_ℓ = s · B_ℓ A_ℓ in fp32 on CPU, assert `ΔW_ℓ.shape == W_ℓ.shape`, and add `ΔW_ℓ.to(W.device, W.dtype)` in place. This is the harness's own fp16 application (`:216–217`).
  4. Return `delta_norms` in the harness's format (`:213–215`).
  5. Increment `ORACLE_HITS`.
  The engine's post-edit cache update (`:218–220`) has no analogue. Each arm zeroes its cache (`:474`), so nothing downstream reads it.

**Arms per eval process (A1 in every run, `prereg_stubs.md:9`):**
- **U — unedited model.** `H.pre_base_report()` (`:449–455`) and `H.eval_arm(Vmap)` on the pristine weights for the A1, A2, A7 and A7-shuf maps, plus every probe in §2.6 and MMLU-200. This is the stimulus-leak check and the reference for the forgetting gates.
- **A — closed-form baseline**, recipe `closedform`, `MODE = "closedform"`, `H.ARMS = {A1, A2, A7}`, `HP_BASE` (`:30`). This is the harness as it stands. It is the LAW#3 reproduction (§2.7) and the same-process locality comparator the contract names (`prereg_stubs.md:10`).
- **O — oracle**, recipe `oracle_<tag>`, `MODE = "oracle"`, `H.ARMS` = exactly the arms with a registered adapter for that recipe; the standing LAW#5 gate runs inside it (`:463`). Phase P1: O-A1, O-A2, O-A7, O-A7-shuf (seed 0, r = 16). Phase P2: recipe `oracle_s1` = O-A1 and O-A7 at seed 1; recipe `oracle_s0rt` = O-A7 at seed 0, retrained. Phase P3 (conditional, §3): O-A7 at r = 64, seeds 0 and 1, one recipe per seed.

**Binding readout:** O-A7 `para_full_n` /72 (`bandknob:396`), with the per-template split (3 × /24, from `para_full_hits` indices) and `canon_full_n` /24 reported (canonical is storage-like here, because T01 = `CANON` is a training template). Also reported: the per-fact 24-vector with the per-edge rule (pass iff 3/3 templates, `prereg_stubs.md:7`); the decomposition `para_first_n`, `tf_pertok_cont`, `cond_full_given_first` (`prereg_stubs.md:8`); and the gain over the same-process closed-form A7.

### 2.6 Locality, forgetting, frame-habit and bigram readouts

All of these run in `ARM_HOOKS` while the edit is applied (`bandknob:404`, `:494–495`), and in arm U on pristine weights.
- **Harness axes (identical to the C10 harness):** L1 flips /12, L3 agreement /30, `described_as`, generic perplexity pre/post (`:319–339`, `:492`).
- **Same-frame fictional probe, per frame.** `frame_probe` over the six `FRAME_SUBJECTS` on `CANON` (/6; `c10p_twopass_arms.py:35–42`). The same probe runs on **each of the 20 training templates** (6 × 20 prompts, flips per template). The council requires a bystander probe in every frame the arm was fit to, counted separately (`council_critique.md:9`; `prereg_stubs.md:10`). On the three held-out templates the probe is reported only (6 × 3).
- **Relation-label probes:** `"{s} is a"` and `"{s} is associated with"` on the 24 edited subjects, top-1 pre (arm U) and post, flips counted /24 each (contract: reported, no threshold, `prereg_stubs.md:10`).
- **Forgetting instrument (named now, as the council requires: `council_critique.md:13`, `:165`; `hypotheses.md:316`): MMLU-200**, the instrument the stub names (`prereg_stubs.md:65`).
  - Source: `cais/mmlu`, config `all`. Test items: `random.Random(20261007).sample(range(len(test)), 200)`. Prompt: the 5 `dev` exemplars of the item's subject in the standard format ("The following are multiple choice questions (with answers) about {subject}.", each question with options `A.`–`D.` and `Answer: X`), then the item and `Answer:`.
  - Scoring: argmax over the logits of the four single-token ids `tok(" A")`, `tok(" B")`, `tok(" C")`, `tok(" D")`. Step 0 asserts that each of the four is one id.
  - Step 0 freezes the 200 items and the prompts into `mmlu200.json` with SHA-256. The download is pre-approved infra (`CLAUDE.md`, operating model item 2). If it cannot be obtained, the design returns to review; there is no substitute instrument.
  - **Floor: accuracy ≥ U − 2.0 points**, paired on identical items: at most 4 net items lost of 200.
  - Reported for U, every closed-form arm and every oracle arm. The harness's generic-perplexity gate (rise ≤ 0.5, `prereg_stubs.md:10`) stays beside it.
- **Write-size and geometry (reported, not gated).** Σ‖ΔW‖_F ratio O / A. Per layer, `tr(ΔW C ΔWᵀ)` (CPU, float64), with C = `get_cov` for that layer (the harness's covariance, `bandknob:169–172`), and the null(C) share ‖ΔW P‖²_F / ‖ΔW‖²_F, with P from `compute_P` (`:166–178`). These are reported for both writers. The closed form's share is 1.000 (`CORPUS/44_C10L_COVGEOM_SPARSEBAND.md:25`). The validation lens says a Frobenius ratio measures the wrong quantity for a different writer (`council_critique.md:167`), so **-LARGE-WRITE is not a gate here**.
- **Bigram control (H-W3; `council_critique.md:11`, `:69`; executable form adopted from `C10U_MINT2_PREREG.md:85`, `:97` for the frozen values).**
  - Step 0 asserts that each A7 target splits as `tok(" " + head)` ids followed by the modifier ids. A fact where it does not split cleanly is excluded from this control, with the count recorded.
  - Post-edit, the head ids are teacher-forced after `CANON` under four subject conditions: (i) the correct subject; (ii) the swapped subject *i* + 1 mod 24, which shares neither head nor modifier (§2.2); (iii) each of the six `FRAME_SUBJECTS`; (iv) the head-sharing sibling *i* + 12 mod 24.
  - Per fact, record `c_k`, `s_k` and `b_k` ∈ {0, 1}: fact *k*'s modifier ids are all teacher-forced argmax under (i), (ii) and (iv) respectively. Also record `n_k`, the fraction of the six never-edited subjects under which they are.
  - **-BIGRAM** if *C* ≥ 1 and *X* ≥ *C*, where *C* = #{c_k = 1} and *X* = #{s_k = 1 or b_k = 1 or n_k ≥ 1/2}.
- **Frame habit (shuffled control).** O-A7-shuf is scored twice:
  - On its own (shuffled) map: reported beside O-A7. A gap > 15/72 gives **-PAIRING-SPECIFIC** (reported).
  - Against the **original** A7 map (cross-score): a subject emitting a value it was not trained on. **Gate: cross-score ≤ 2/72**, else **-FRAME-HABIT** on O-A7. The closed form shows no sibling confusion (`CORPUS/45_C10L_MINT_TOKEN.md:28`).
  - **Sibling emission:** for every O-A7 held-out miss, whether the greedy output equals another subject's value (count / misses; the graph lens's confusion readout, `council_critique.md:131`).
- **Alternative tokenisation (`council_critique.md:250`).** `para_string_n` (startswith) beside `para_full_n`, plus a "contains `" " + value`" count from a hook decode of `n + 2` ids (the `C10U_MINT2_PREREG.md:82` judgment). `alt_tok_n = string − full` is reported; `para_string_n < para_full_n` halts.
- **Merge versus mount (`council_critique.md:101`; reported).** After the other readouts, the hook restores the base weights, attaches fp32 forward hooks that add s · B(Ax) to each band `down_proj` output (cast to fp16), re-runs `eval_arm` for that map, and detaches. |merged − mounted| `para_full_n` > 5/72 → **-MERGE-LOSS** (fp16 merge fidelity is a confound of an fp32-trained adapter). Also reported: the per-layer relative error ‖(W_after − W_before) − ΔW‖_F / ‖ΔW‖_F of the fp16 application, beside the same quantity for the closed-form `upd`. Weights are left restored; the next arm restores again (`:473`).

### 2.7 Gates: fingerprint, LAW#3, LAW#5

- **Engine fingerprint.** `python3 tools/engine_fingerprint.py` passes (SHA-256 `d941a9fb…`, `_cov_cpu` sites 3; `tools/engine_fingerprint.py:34`, `:36`) at the start of every eval process; the closed-form arm uses the engine. The trainer does not use the engine (`prereg_stubs.md:67`), so its records carry their own provenance: the trainer source SHA-256, data SHA-256, adapter SHA-256, model revision and package versions. The fingerprint result is copied into them for provenance only.
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
  - **(v)** `ORACLE_HITS` = number of oracle arms in the process.
  - Any failure of (i)–(v) → HALT. `REPRODUCIBILITY.md`'s cross-process caveat does not excuse these same-process checks (`C10V_LAYERPICK_PREREG.md:58`).

### 2.8 Phases and order of cells

**Step 0** (`c10w_oracle_step0.py`; imports the harness; no write):
1. Freeze the value maps, the A7-shuf map (asserted, §2.2), the target ids and the head/modifier splits.
2. Write `train_inputs.json` (no `PTEST`) and its SHA-256, plus SHA-256 of each `PTEST` template.
3. Run S1–S6 with the harness's real constants and write `seal_audit.json`. S7 is filled in at the design pass, before freeze.
4. Freeze `mmlu200.json`.
5. Check the four answer-letter ids.
6. Run the fingerprint gate.
Any audit failure → HALT before training.

**Phase P1 (binding)**, in order, each a fresh OS process, never concurrent with any other GPU job (autoresearch loop paused, Ollama stopped):
1. Train O-A1 s0. The first 10 steps are timed. If the projected 400-step time exceeds 90 min, stop and HALT for a budget ruling.
2. Train O-A7 s0, then O-A2 s0, then O-A7-shuf s0.
3. One eval process: fingerprint, U, LAW#5 (ii), recipe `closedform` (LAW#3), recipe `oracle_p1`.

**Phase P2 (replication; always runs before any label is used for routing):**
1. Train O-A7 s1, O-A1 s1, and O-A7 s0 retrained, in fresh processes.
2. One eval process: fingerprint, U, LAW#5 (ii), `closedform` (LAW#3), `oracle_s1`, `oracle_s0rt`.
3. Same-seed agreement is reported: per-layer cosine of ΔW between P1's seed 0 and the retrain, per-prompt agreement /72, and |count difference|.

**Phase P3 (capacity check; only if the replicated r = 16 label is PARTIAL- or FAIL-CEILING, §3):** train O-A7 at r = 64 (α = 64) for seeds 0 and 1, then one eval process with U, `closedform` (LAW#3) and both oracle recipes. O-A1 is not retrained at r = 64: the trainer's pipeline was validated at r = 16, and the closed-form A1 is in this run.

The reader `c10w_oracle_read.py` encodes every gate and label of §3 and prints them. Labels are computed by the reader only, never by hand.

### 2.9 Compute estimate on MPS (unmeasured on this Mac for training; the smoke in P1 step 1 measures it)

| item | estimate | basis |
|---|---|---|
| fp32 weights (trainer) | ≈ 12.3 GB | 3.09 B params × 4 B (`model.safetensors.index.json` total 6.17 GB at 2 B/param) |
| fp16 weights (eval; bf16 would be the same) | ≈ 6.2 GB | the same, × 2 B |
| LoRA parameters + AdamW state | 1.04 M params at r = 16 (5 × 16 × (11008 + 2048)) ≈ 4.2 MB, × 3 with state; 4.18 M at r = 64 | arithmetic |
| trainer activations + logits (batch 24 × ≤ 25 tokens ≈ 600 tokens) | ≈ 4 GB saved activations (layers 4–35) + ≈ 1.1 GB logits and their gradient (600 × 151,936 × 4 B × ≈ 3) | arithmetic; layers 0–3 need no backward |
| trainer peak | ≈ 18–20 GB; **HALT if > 40 GB** | sum, with margin for the OS on 48 GB unified memory |
| eval process | ≈ 12 GB (fp16 model + five 462 MiB fp32 covariances and five projectors on CPU, `hypotheses.md:11`) | arithmetic |
| FLOPs per training step | ≈ 3 × 2 × 3.09 × 10⁹ × 600 ≈ 1.1 × 10¹³ | forward + backward ≈ 3 × forward |
| time per adapter (400 steps) | ≈ 19–37 min, assuming 2–4 TFLOP/s effective fp32 throughput (an assumption, not a measurement) | the budget stop at 90 min projected guards it |
| closed-form recipe pass | ≈ 33 min | timing anchor (`hypotheses.md:8`) |
| oracle arm eval incl. hooks and MMLU-200 | ≈ 10 min per arm | eval_arm + about 400 probe forwards + 200 MMLU forwards |
| **P1** | ≈ 3–4 h (4 trainings + one eval with U, closed form, 4 oracle arms) | sum |
| **P2** | ≈ 2–3 h | sum |
| **P3 (conditional)** | ≈ 1.5–2.5 h | sum |
| **total** | ≈ 5–7 h binding; ≈ 7–9.5 h with P3 | supersedes the stub's 2–3 h (`prereg_stubs.md:67`), which priced one adapter and no replication |

### 2.10 Records and outputs

Each phase writes into a fresh `results/c10w_oracle/<phase>_<UTC-timestamp>/` and **refuses to start if the directory exists**. Nothing is ever overwritten; this follows the "fresh OUT_DIR" rule of `EXPERIMENT_RUNBOOK.md:342`.
- Files: `step0.json`, `train_inputs.json`, `seal_audit.json`, `mmlu200.json` (step 0); `train/<arm>_s<seed>_r<rank>[_rt].json` (one per adapter); `eval.json` (U, both recipes' `run_recipe` outputs, all hook readouts, gates, `ORACLE_HITS`, LAW#5 (ii)–(v)); `verdict.json` (reader output); a run log.
- Every JSON carries `"class": "ORACLE MEASUREMENT — not a route; never promotable as a write-engine result (D-C10r-rulings-3 (2))"` and the Decision-ID.
- **Edited weights are never committed.** Adapters are `adapters/*.safetensors`, ignored by `.gitignore:25`. Merged weights are never saved; they exist only in the eval process's memory and are restored by the harness. The reader refuses to proceed if any adapter path is tracked.

## 3. Pre-registered readings (exact counts; decision order fixed)

**Decision order:** validity (INVALID ends the reading) → binding count → locality and forgetting gates → per-configuration label → replication → capacity check (if triggered) → routing.

**Validity (any failure → INVALID; no label, no routing):**
- the fingerprint;
- the seal (S1–S7 recorded and passing; `PTEST` absent from trainer inputs and source);
- the stimulus checks of arm U;
- LAW#5 (i)–(v);
- LAW#3 (closed-form envelope, A1/A2 ≥ 68);
- **trainer positive controls O-A1 ≥ 68/72 and O-A2 ≥ 68/72** (P1), O-A1 s1 ≥ 68/72 (P2);
- the fit gate (train-EM ≥ 456/480) for every adapter whose arm is read;
- every hash present and matching (adapter, `train_inputs.json`, trainer source, `mmlu200.json`, template sets);
- `para_string_n ≥ para_full_n` in every arm.

**Gates on an O-A7 configuration** (vs the same-process closed-form A7 arm "A" and arm U; the contract's numbers, `prereg_stubs.md:10`):

| gate | rule |
|---|---|
| G1 | L1 flips ≤ A + 1 (of 12) |
| G2 | L3 ≥ 29/30 |
| G3 | `described_as` ≥ A − 3 |
| G4 | same-frame flips on `CANON` ≤ A + 1 (of 6), **and** for each training template t, flips(t) ≤ A(t) + 1 (of 6) |
| G5 | generic perplexity post − pre ≤ 0.5 |
| G6 | MMLU-200 ≥ U − 2.0 points |
| G7 | shuffled cross-score ≤ 2/72 (no -FRAME-HABIT; P1, applied to every O-A7 configuration's label) |

**Labels per configuration** (count = O-A7 `para_full_n` /72):
- **PASS-CEILING:** count ≥ 61 and G1–G7 all hold.
- **PARTIAL-CEILING-LOCALITY-COST:** count ≥ 61 with any of G1–G7 missed (the gate is named in the label). The ceiling with locality clean is not shown.
- **PARTIAL-CEILING:** 30 ≤ count ≤ 60; any gate miss is appended as a qualifier.
- **FAIL-CEILING:** count < 30; gate misses are reported.
- **INVALID:** any validity failure.
- Qualifiers carried and reported, not changing the band: -BIGRAM, -PAIRING-SPECIFIC, -MERGE-LOSS, -RETRY800.

**Replication (required before any label routes; a second seed in a second process).** The r = 16 label is computed on **min(count_s0, count_s1)**, with both configurations valid and the union of their gate misses. If |count_s0 − count_s1| > 15/72, or the same-seed retrain differs from P1's seed 0 by > 10/72, the label is **-UNSTABLE**: no routing, the operator is informed, diagnosis first. For calibration, the mint's init-seed range was 12/72 (`CORPUS/46…:22`) and the closed form's per-process spread ±3–5/72 (`CORPUS/44…:41`).

**Capacity check (P3; only if the replicated r = 16 label is PARTIAL- or FAIL-CEILING).** The r = 64 label is computed on min(count_s0, count_s1) by the same rules. **Final label = the better of the r = 16 and r = 64 labels, both replicated**; it is written `…(capacity r = 64)` if r = 64 supplied it. The FAIL routing to the model axis therefore requires both ranks to fail.

**Routing (every case: "oracle measurement, not a route"; C10 stays OPEN/BLOCKING; nothing is promoted as a write-engine result):**

| final label | routing consequence |
|---|---|
| **PASS-CEILING** (either rank) | The five band matrices of this model can hold the 24 coined values with held-out transfer at the bar and locality clean. The wall is a missing objective or its realisation, so the engine days are spent: steps 6 (H-11) and 7 (H-3) proceed (`recommended_sequence.md:26–27`). H-30 weight grafting (`hypotheses.md:309–310`) becomes eligible as its own pre-registration, to localise what carried the value. |
| **PARTIAL-CEILING** (any form, incl. -LOCALITY-COST) | Training on this model beats the closed form (≈ 12/72) but does not reach the bar cleanly. Steps 6–7 proceed, with the replicated oracle count recorded as their practical reference ceiling: an engine arm that matches it has closed the objective gap, and reaching 61 beyond it would need the model axis. The model-axis go/no-go (`HANDOFF.md:56`) is surfaced to the operator in parallel, with the recommendation stated at the verdict. |
| **FAIL-CEILING** (both ranks) | Even this training cannot reach "worth replicating" on this model. The question becomes the model: the operator's ceiling-rule decision (D-C10k-rulings-2; `HANDOFF.md:56`) is surfaced with this result as the evidence. Steps 6–7 are deprioritised pending that ruling, not cancelled. Before the ruling, the operator may choose H-15 (full-band fine-tuning, `hypotheses.md:154–162`) as a stronger oracle. |
| **INVALID / -UNSTABLE** | No routing. HALT and diagnosis (§5). |

## 4. Not claimed, whatever the outcome; risks and confounds

**Never claimed:**
- that training is a write engine, a route, overlay-compatible, compactable, rollback-safe, deterministic enough for the §10.2 integrity check, or able to fit the §11.5.1 / §11.9 windows. None of these is tested (`council_critique.md:10`, `:13`, `:99–102`, `:201–204`, `:244`);
- the two-overlay composition, retraction and relation-family tests the consistency and graph lenses proposed (`council_critique.md:99`, `:130`, `:132`). These are route tests and belong to a route, which this is not;
- any change to C10's status, to F1, or to a CORPUS/37–53 label;
- "graph stored": at most "edge stored under one relation label" (`council_critique.md:14`);
- that a coined value became a semantic node. The loss is a string objective (`council_critique.md:133`).

**Risks and confounds:**
1. **Scope of a FAIL.** It covers one recipe family: LoRA at r ∈ {16, 64}, 20 templates, lr 3 × 10⁻⁴, 400 steps, N = 24, one relation, fp16 merged eval. It is not "no solver will". A different representation already reached 34–46/72 with the closed form (the one-token mint, `CORPUS/45…:61`). An oracle FAIL below that bounds this objective on this representation, not every write.
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
- the training budget (> 90 min projected per adapter);
- peak memory > 40 GB;
- `para_string_n < para_full_n`;
- an oracle recipe meeting an arm without a registered adapter.

On a science-path or driver bug, at most one speculative fix after a `cat -n` read; if it does not clear the gate, HALT. A HALT writes a diagnostic JSON to `architecture_profile/sNNN_halt_diagnostic.json`, records the halt in `SESSION_CHECKPOINT.md` (plus a CORPUS note if it is a finding), and STOPs: no further phase. Close-out goes through `python3 tools/closeout_check.py D-C10w-oracle` once the CORPUS entry exists. The CORPUS entry, register row and overlay row carry "oracle measurement, not a route"; the overlay row is §8.2 D12, oracle measurement, no amendment. The advisor reviews before the run. Codex GPT-6-Astra (high) reviews at the design pass (including S7), at the implementation review, and at the verdict. This experiment runs only on the operator's go, with the GPU free (`docs/INTEGRATED_QUEUE_2026-10-07.md:37`).

## 6. Reviews

**v1 draft (this file)** → advisor pass → Codex GPT-6-Astra design pass (incl. S7 adjudication) → v2 → lead read-through → freeze → implementation (Codex, model-free, per D-C10r-rulings-9 (3), `EXPERIMENT_RUNBOOK.md:342`): `c10w_oracle_step0.py`, `c10w_oracle_train.py`, `c10w_oracle_eval.py`, `c10w_oracle_read.py` → implementation review → step 0 → P1 → P2 → (P3) → verdict review → CORPUS/NN.

## 7. Review fold log

No review folded yet.

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
