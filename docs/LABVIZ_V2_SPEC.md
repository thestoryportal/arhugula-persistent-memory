# Lab View v2: design spec

**Status:** DRAFT for advisor and Astra review, 2026-10-07. Operator ruling **D-C10r-labviz-2** (`EXPERIMENT_RUNBOOK.md`, row at `:372`). Codex brief for Phase 1: `results/labviz_v2_codex_brief.md`.
**Scope additions from the operator (2026-10-07):**
- §4A, design and usability, governs every view;
- §11, the program-wide context model and the "how it all connects" map, places every run in its own era's terms. Both are in Phase 1.

**How this was written:** while P2 was running, without any python process. Every field name and value below was read with `jq`, `grep`, `sed` or `ls` from the files named. §3.9 lists the commands, so anyone can re-run them. Values marked *UNMEASURED* are estimates.

---

## 0. Where this sits

Lab View is observation tooling for two parts of the end-to-end framework (`docs/SPEC_E2E_GROUND_TRUTH.md`): **§C, the write path** (what a write changed inside the model) and **§F, post-write verification** (whether the fact can be recalled from reworded questions, and what else changed). It touches no science cell:

- it makes no verdict;
- it changes no gate, label, prereg, ledger or result file;
- it never loads a model, a tokenizer or a weight file.

A display that is wrong can still mislead a decision. For that reason every number on screen and in the run card carries its source file and its JSON key path.

## 1. Readers and goals

| Reader | Needs | Form |
|---|---|---|
| **Operator** (an architect, no ML background) | See what each experiment did inside the model, in plain words. See the result against the goal and the side effects. Compare runs. Watch a run play back. | Badges, strips, gauges, a tower with layers and parts, a wiring diagram, a player. Every picture has a one-line caption in plain words. Every picture also says what it does **not** mean. |
| **An AI** (program session, reviewer, Codex) | Reason from data, never from pixels. | One **run card** JSON per run (§6). Every number in it is `{value, src:{file, path}}`. Derived numbers name their formula and inputs. Every record of an observation replay is labelled NOT EVIDENCE. |

## 2. Rules that bind every phase

1. **Read-only, model-free.** Lab View reads JSON, JSONL and log files, numbered CORPUS headers, the scoreboard, the evaluations file, referenced hparams, and the model's `config.json`. It never imports or runs experiment or engine code. It never opens `.safetensors`, `.pt`, `.npz`, tokenizer or vocabulary files. It never uses the GPU.
2. **Missing stays missing.** If a field is absent, the card and the picture say "not recorded for this run" and name the tier that would supply it (§4). Nothing is interpolated or guessed.
3. **No python while a GPU stage gate is armed.** `tools/c10w_p2_gate.py:21–30` blocks the next GPU stage if any unknown python process is running. It exempts only two exact Lab View command lines: `.venv/bin/python -B -m http.server 8765 --bind 0.0.0.0 --directory results/labviz/site` and `.venv/bin/python -B tools/labviz/build.py`. Consequences:
   - v2 keeps both command lines **byte-identical**, so it adds no CLI flags;
   - tests, Codex builds and replays run only when no GPU coordinator is live;
   - future gates may not carry these exemptions, so "no python during a gated run" is the safe default.
4. **Evidence tiers are labelled everywhere:**
   - **RECORDED**: from a scored result file;
   - **TELEMETRY**: in-run JSONL, opt-in, proven inert, not a scored record;
   - **REPLAY (NOT EVIDENCE)**: an offline re-creation of a run.

   A replay is shown *as the run* only when it reproduces the run's counts (§7.5). Otherwise it is shown as an "approximate replay", with the mismatch.
5. **Program rulings (D-C10r-labviz-2).** Lab View stays read-only and model-free. Data the runs did not record comes only from the separate observation-replay tool (§7). Every replay needs an operator yes for its GPU time. Live in-run data exists only as the opt-in, proven-inert telemetry JSONL that new builds write (C10Z prereg §9(h), §9.1(h′)).

---

## 3. Data inventory (Step 1): what the runs actually recorded

Notation: `F:path` means the jq path inside file F. `<R>` is a recipe and `<arm>` is an arm label (`A1_single`, `A2_coherent2`, `A7_coined_coined`, plus `A7_shuf` and `A7_canon` in C10W). A7 is the binding arm, the one with made-up two-word answers. Sample values are quoted so the reader can check them.

### 3.1 C10V layer-pick (step 4): `results/c10v_layerpick/`

Files: `step0.json`, `pass1.json` (542 KB), `run.json` (the reading), `law5.json`, `identity.json`, `pass1_started.json`, `pass1_complete.json`.

| Grain | Field (jq path) | Shape / sample |
|---|---|---|
| per run | `pass1.json:.decision_id` | `"D-C10v-layerpick"` |
| per run | `pass1.json:.model` | `{"id":"Qwen/Qwen2.5-3B","revision":"3aab1f19…","dtype":"float16","device":"mps"}` |
| per run (gates) | `pass1.json:.fingerprint.ok`, `.law5.ok`, `.law5.standing` | `true`, `true`, `{"expr_delta":0.0003,"loc_delta":0.03,"ok":true}` |
| per run | `pass1.json:.ctx` (key-averaging context prefixes; first group is the identity template) | 2 groups: `["{}"]` and 5 prefixes such as `"Because of the COVID-19 pandemic, the. {}"` |
| per recipe | `pass1.json:.recipes` | keys `A`, `B0`, `B`, `Bshuf` |
| per recipe | `.recipes.<R>.band` | `[4,5,6,7,8]` for **all four**, including B0 (see item 4) |
| per recipe | `.recipes.<R>.map` | per subject → layer, e.g. B: `Zorbland 6, Plurnak 8, Skornwell 4, Thelby 7 …` |
| per arm | `.recipes.<R>.arms.<arm>.para_full_n` / `.para_n` | A·A7 **11/72**; B0·A7 12/72; B·A7 12/72; Bshuf·A7 10/72; A1 68–70/72; A2 70–71/72 |
| per arm | `.canon_full_n`, `.canon_n` | B·A7 7/24 |
| per arm | `.locality_described_as` | A·A7 90.0; **B·A7 86.17**; B0·A7 90.11; Bshuf·A7 87.37 |
| per arm | `.locality_axes` | `L1_flipped_to_edited_value 0`, `L1_n 12`, `L3_top1_agree 30`, `L3_n 30`, `L3_mean_kl 0.00027`, `generic_ppl_pre 21.755`, `generic_ppl_post 21.713`, `L1_post_top1{12 countries → token text}` |
| per arm | `.extra` | keys `proxy`, `relation_labels`, `same_frame`. `same_frame` = `{flips:1, n:6, rows[{subj, top1, flip}]}` |
| per layer · per arm | `.recipes.<R>.delta_norms.<arm>.<layer>` | `{delta_norm, weight_norm_before, relative_delta_norm}`. **Keys are the layers actually written.** B0·A7: only `"8"` (55.42). B·A7: 4–8 = 4.85, 16.13, 27.69, 9.71, 16.31. A·A7: 4–8 = 15.86, 11.93, 11.87, 19.27, 27.20 |
| per fact · per arm | `.recipes.<R>.detail.<arm>[i]` (24 rows) | `{subj:"Zorbland", val:"Vindex Vask", ntok:4, canon_full, canon_first, para_full_hits:[t,t,t], para_first_hits, para_string_hits, tf_correct:9, tf_total:9}` |
| per fact · per prompt | `.recipes.<R>.arms.<arm>.extra.proxy.rows[i].rho_per_prompt` | 4 values: the remaining-residual ratio on the canonical prompt plus the three rewordings (prereg `docs/C10V_LAYERPICK_PREREG.md:54`). Also `layer`, `realised_fraction`, `full_G_diagonal`, `pristine_residual_norms[4]`. 192 paths in the file |
| per fact | `.recipes.<R>.predictions_before_write.<arm>.<subj>` | `{full_G_diagonal, group_G_diagonal}` |
| per fact | `.recipes.<R>.target_ids.<arm>.<subj>` | answer **token ids** only (e.g. `[94311]`), no token text |
| per layer (diagnostic) | `.hsic.layers.<4..8>.{HSIC_b, per_fact_c[24], status:"DIAGNOSTIC"}` | role: "A7 diagnostic only; layer-8 pristine residuals; never selector or gate" |
| per layer (LAW#5) | `.law5.{identity,singleton,multigroup,floor}.relative_by_layer` | inertness detail |
| **reading** | `run.json:.readings.<R>.label` / `.base_label` / `.count_label` | B0 `NULL`, B `NULL`, Bshuf `NULL-CONTROL-ONLY` |
| reading | `run.json:.readings.<R>.binding` | B0 12, B 12, Bshuf 10 (the count the label used) |
| reading | `run.json:.readings.<R>.locality_gates` | B: `{L1:true, same_frame:true, described_as:false, L3:true, generic_ppl:true}` (booleans only; the floors are not stored) |
| reading | `.readings.<R>.{gain, write_ratio, gate_A, attributed, reasons, spearman_G_edge}` | B0 `write_ratio 0.6435`, `spearman_G_edge −0.479` |
| per fact (reading) | `.readings.<R>.assigned_layers[24]`, `.per_edge_3of3[24]`, `.per_template[3]` | B0: all 8; `per_template [3,3,6]` |
| per layer (reading) | `.readings.<R>.by_layer.<4..8>.{facts, para_full, edges_3of3}` | B layer 8: `{facts:2, para_full:0, edges_3of3:0}` |
| **step 0 (selector)** | `step0.json:.G_table` and `.G_table_repeat` | 24 × 5 (facts × layers 4–8); row 0 = `[0.832, 0.932, 0.948, 0.922, 0.924]` |
| step 0 | `.winning_margins[2][24]`, `.runner_up[2][24]` | row 0 = first table, row 1 = repeat (`experiments/track_c/c10v_layerpick_read.py:71–92`). Margin = best G − second-best G |
| step 0 | `.map`, `.repeat_map`, `.map_reproduced` (true), `.delta` (0.0), `.concentration` (15), `.status` ("READY"), `.subjects[24]` | |
| step 0 | `.projected_key_norms[24][5]`, `.installed_share_comparison[24]{subj, max_G, installed_share, band_installed_share}` | |

**Not in C10V records:** generated answer text, rewording template text, token text of answer pieces or of the keyed subject piece, logit lens, attention, activations.

### 3.2 C10W ceiling oracle (step 5): `results/c10w_oracle/`

Directories:
- `step0_20261007T223638_531381Z/`;
- the halted `step0_20261007T220253_584752Z/HALT.json`;
- `p1_20261007T223707_598959Z/`;
- `p2_20261008T034226_086980Z/` (**running**);
- gate records in `results/c10w_oracle_logs/*.gate.*.json` (`{stage, at, ok, checks{fingerprint, gpu, dispatch_guards}}`).

| Grain | Field | Shape / sample |
|---|---|---|
| per adapter (training) | `train/<arm>_s<seed>_r16[_rt].json:.losses[]` | `{step, loss}` every 10 steps, **40 points**. A7 s0: step 10 = 7.7066 … step 400 = 0.000411 |
| per step | `.step_seconds[]` | 400 values |
| per adapter | `.fit.{correct, n, per_fact[24], per_template[20]}` | A7: 480/480; `per_template` = 24 each. **End of training only** |
| per adapter | `.{arm, phase, seed, retrain, rank, steps, layers, status, wall_seconds, adapter{path, sha256}}` | rank 16, 400 steps, layers [4..8], A7 s0 wall 523.35 s; adapter file 4,179,028 bytes |
| per parameter tensor | `.frozen_parameter_hashes_before` / `_after` (434 keys each) and `.frozen_parameters_unchanged` (true) | Keys name **every module**, e.g. `model.layers.8.self_attn.q_proj.weight`, `…k_proj.bias`, `…o_proj.weight`, `…mlp.gate_proj.weight`, `…mlp.up_proj.weight`, `…mlp.down_proj.weight`, `…input_layernorm.weight`, `…post_attention_layernorm.weight`, `model.embed_tokens.weight` |
| P1 eval | `p1…/eval.json:.recipes` | `closedform`, `oracle_p1`, `oracle_canon_s0` |
| per arm | `.recipes.<R>.arms.<arm>.{para_full_n, para_n, canon_full_n, locality_described_as, locality_axes}` | oracle_p1·A7 **70/72**, described_as 86.72, L3 30/30, ppl 21.755→21.081. closedform·A7 9/72. oracle_canon_s0·A7_canon 2/72, L3 **12/30** |
| per arm | `.extra.mmlu.{accuracy, correct_n, n, net_paired_loss, correct_to_wrong, wrong_to_correct}` | oracle_p1·A7: 0.59, 118/200, net 4, 13 lost / 9 gained |
| **per prompt (text)** | `.recipes.<R>.arms.<arm>.extra.generated[72]` | `{subj, template:"If you visit {}, its capital city is", ids[6], text:" Vindex Vaskul,", contains, full, sibling_subjects}`: **the rewording text and the model's generated words** |
| per frame | `.extra.frames.{canon, train[20], heldout[]}` | `{n:6, flips, rows[{subj, top1, tok:" Th", flip}]}` (fictional bystanders, token text recorded) |
| per layer | `.extra.geometry.<4..8>` | `{delta_norm, trace_delta_cov_deltaT, null_cov_share, application_relative_error, delta_sha256}` |
| per layer | `.recipes.<R>.delta_norms.<arm>.<layer>.delta_norm` | oracle_p1·A7 (merged LoRA ΔW): 7.74, 4.53, 4.55, 5.02, 5.61; closedform·A7: 15.82, 11.89, 11.57, 19.24, 27.56 |
| per fact | `.recipes.<R>.detail.<arm>[24]` | same row schema as C10V (`subj`, `val`, `para_full_hits[3]` …) |
| per layer (hash) | `eval.json:.base_band_hash`, `.final_band_hash`, `.recipes.<R>.band_after_hash` | per-layer SHA-256 of down_proj 4–8 |
| verdict | `p1…/verdict.json:.{final_label, status, c10_status, f1_changed}` | `null`, `"INCOMPLETE"`, `"OPEN/BLOCKING"`, `false` (P2 still running) |
| step 0 (text) | `step0…/step0.json:.head_modifier_splits.<subj>.{head, head_ids, modifier, modifier_ids, eligible}` | answer split into its two words, with ids |
| step 0 (text) | `step0…/seal_audit.json:.rows[].template` | the 20 sealed **training phrasings** |
| step 0 | `step0…/train_inputs.json:.prompt_ids.<k>.<subj>`, `.fiction[]` | token ids per training phrasing |
| step 0 | `step0…/mmlu200.json:.items[200]{question, choices, answer, subject, prompt}` | forgetting instrument |
| P2 | `p2…/train/*.json` (6 so far: s1 seeds, plus `_rt` retrains of s0) | all `status PASS`, 40 loss points, `frozen_parameters_unchanged true` |
| logs | `p1-*.log`, `p2-*.log` | `"<adapter> step N loss X"` lines (40 per adapter), `STAGE_EXIT=0` |

**Not in C10W records:** per-step answers during training (no intermediate adapters are saved, and the eval runs once at the end), logit lens, attention, activations.

### 3.3 C10U new vocabulary word (step 3): `results/c10u_mint2/`

- Per-run records: `r3/F_r<rep>_<kind>_s<seed>.json` (`kind` ∈ `mint1`, `modifier`, `multi`).
- Readings: `r3_read_after_{v2,replicateF,frozen}.json`.
- Labels: `r3_read_after_v2.json:.F.arms.<arm>.label`. Recorded values: `LEAD`, `LEAD-NOT-REPLICATED`, `LEAD-NOT-REPLICATED-NOT-COMPARABLE`, `TRADEOFF`, `TRADEOFF-NOT-COMPARABLE`, `UNDERFIT`, `UNDERFIT-NOT-COMPARABLE`.
- Per arm: `.arm.{para_full_n, para_n, para_full_binding_n, canon_full_n, locality_described_as, locality_axes}`. Sample: `F_r1_multi_snone.json` → 14/72, binding 14, described_as 88.22.
- **Per fact (binding arm): teacher-forced only.** `.arm.extra.per_fact_position_curve[24]{subj, underfit, per_template_hits[3][pieces]}`, plus `.arm.extra.per_position_teacher_forced.<0..5>{hits, n}`. Free-answer `para_full_hits` exist only for the A1/A2 controls (`.recipe.detail.A1_single[…]`, 48 paths).
- Text: `.minted_words`, `.minted_ids`, `.values`; prompt text under `.step0.rank_probes[].modifier_paraphrase_probes[].prompt`.
- Per layer: `.recipe.delta_norms`, and `.arm.extra.post_geometry`.

### 3.4 Earlier C10 runs that build.py already reads

| Family | What is there (counts = files containing the key, from `grep -rl`, excluding `results/labviz/`) |
|---|---|
| Flat `results/c10_*.json`, `c10b…c10j` | `detail.<arm>[].para_full_hits` (per fact × 3 rewordings) and `recipes.<R>.delta_norms` (c10e/f/g/h/j). **Percent only** in c10e (`para_full_n` is `null`). `locality_described_as` present; `locality_axes` absent. Label at `verdict.label` (c10e: `"NO_MATERIAL_KNOB_RESCUE"`). |
| `c10k_keying_ablation` (16), `c10k_route_a` (8) | Harness detail and delta_norms. `c10k_route_a/R1_w1_A7_coined_coined.json:.update_norm_ratio` = `{4:4.94, 5:1.12, 6:1.02, 7:1.017, 8:1.010}` (a ratio, not a norm). |
| `c10l_covgeom` (9), `c10l_mint` (9), `c10m…c10t` | Harness detail, delta_norms, `locality_axes` (L1/L3 from c10l on). `c10l_covgeom/step0_offline.json:.regularisers.<R>.per_layer.<l>.dW_fro` (offline **predicted**, not applied). `c10q_stacked/passS.json:…extra.stacked_delta_norms`. |
| Totals | `para_full_hits` 119 files · `delta_norms` 78 · `locality_described_as` 78 · `L1_flipped_to_edited_value` 53 · `per_template_hits` 21 (all c10u) · `losses` 12 (all c10w) · `G_table` and `winning_margins` 1 each (c10v step0) · `rho_per_prompt` 1 (c10v pass1). |

### 3.5 Model structure (Qwen2.5-3B)

- **`config.json`:** `<wt>/hf_cache/hub/models--Qwen--Qwen2.5-3B/snapshots/3aab1f1954e9cc14eb9509a215f9e5ca08227a9b/config.json`. `hf_cache` is a symlink to `/Volumes/memit/llm-database-poc-mirror/hf_cache`. The revision equals the one in the records.
  - `num_hidden_layers 36`, `hidden_size 2048`, `intermediate_size 11008`;
  - `num_attention_heads 16`, `num_key_value_heads 2` (grouped-query: 8 query heads share each key/value head);
  - `hidden_act "silu"`, `rms_norm_eps 1e-6`, `vocab_size 151936`;
  - `tie_word_embeddings true`: the output head reuses the input word table.
- **Module names** (exact, from the 434 keys of `frozen_parameter_hashes_after` in any C10W train record). Per layer `model.layers.{i}.`:
  - `input_layernorm.weight`;
  - `self_attn.{q,k,v}_proj.{weight,bias}` and `self_attn.o_proj.weight`;
  - `post_attention_layernorm.weight`;
  - `mlp.{gate,up,down}_proj.weight`.

  Plus `model.embed_tokens.weight` and `model.norm.weight`: 36 × 12 + 2 = 434.
- **Per-layer flow:** input RMSNorm → self-attention (q/k/v/o, grouped-query heads) → add back to the main line → post-attention RMSNorm → MLP (gate_proj and up_proj, SiLU on gate × up, then down_proj) → add back to the main line.
- **What MEMIT writes** (`configs/hparams/qwen25_3b_memit_hparams.json`):
  - `:2` `"layers": [4,5,6,7,8]` (the configured band);
  - `:13` `"rewrite_module_tmp": "model.layers.{}.mlp.down_proj"`;
  - `:5` `"fact_token": "subject_last"`;
  - `:17` `"ln_f_module": "model.norm"`;
  - `:18` `"lm_head_module": "model.embed_tokens"` (tied head);
  - `:16` `attn_module_tmp`.

  The C10W LoRA targets the same five `down_proj` matrices (`docs/C10W_ORACLE_PREREG.md:27`, `:168`, `:172`).
- **"Untouched" has two levels of proof:**
  - *configured*: the MEMIT engine edits only `rewrite_module_tmp` at the written layers, so every other part is untouched by design;
  - *hash-verified*: C10W train records hash all 434 tensors before and after training (`frozen_parameters_unchanged: true`), and `eval.json` hashes down_proj 4–8 before and after.

  MEMIT records carry no all-module hash, so for MEMIT runs Lab View must say "untouched by design", not "verified".

### 3.6 Stimulus text: where the words live

| What | Where recorded (preferred) | Where defined (source) |
|---|---|---|
| Made-up subjects (24) | every `detail.<arm>[].subj` | `experiments/track_c/c10e_bandknob.py:57–61` (`FICTION`) |
| Made-up answers | every `detail.<arm>[].val` (e.g. Zorbland → "Vindex Vask") | `c10e_bandknob.py:229–249`: `coined_head` / `coined_mod` lists, then the A7 formula `head[(2i+1)%24] + " " + mod[(3i+2)%24]` |
| Real-word answers (A1/A2 controls) | `detail.A1_single[].val` | drawn from `configs/screens/g6_screen_qwen3b_v2.json` (`c10e_bandknob.py:226–228`, `:242–245`) |
| Canonical question | not in C10V records | `c10e_bandknob.py:51`: `"The capital of {} is the city of"` |
| Three rewordings (held-out) | **C10W only:** `eval.json:…extra.generated[].template` | `c10e_bandknob.py:52–56` (`PTEST`): `"{}'s capital city is called"`, `"If you visit {}, its capital city is"`, `"The main city and seat of government of {} is"` (same order as `para_full_hits`) |
| The model's generated words | **C10W only:** `extra.generated[].text` | none |
| Side-effect prompts | `locality_axes.L1_post_top1` (12 countries → first piece) | `c10e_bandknob.py:277–300`: L1/L3 on `CANON`, 20 `GENERIC` sentences; `"{c} is described as"` at `:475` |
| Keyed position | rule only: `fact_token "subject_last"` (hparams `:5`) | the **text** of the subject's last piece is not recorded anywhere; it needs a tokenizer |
| Training phrasings (C10W) | `step0…/seal_audit.json:.rows[].template` (20) | |
| Answer word split (C10W) | `step0…/step0.json:.head_modifier_splits` | |
| Minted words (C10U) | `F_*.json:.minted_words` | |

**Binding check without importing code.** `sha256(experiments/track_c/c10e_bandknob.py)` = `1f6be581…e695`. This equals `results/c10v_layerpick/pass1.json:.identity.source_sha256["experiments/track_c/c10e_bandknob.py"]` (checked with `shasum -a 256` and `jq`). So a transcription of the constants above, stored in a Lab View data file, can be bound to a run by SHA:

- the builder checks that the run's recorded source SHA equals the SHA in the transcription file;
- it checks that each transcribed string occurs verbatim in the source file's text;
- it never imports the file.

### 3.7 What no run recorded

`grep -rhoE '"[A-Za-z_]*(logit_lens|attention|attn|activation|hidden_state|telemetry)[A-Za-z_]*"\s*:'` over every `results/**/*.json` finds only configuration or unrelated keys:
- `attn_module_tmp` (an hparams copy);
- `"attn": "eager"` in `d1_instrument_variance_diagnostic_3b_*.json`;
- `num_attention_heads` and `attention_dropout` (config copies);
- the minted tokenizer's `tokenizer.json` / `vocab.json`;
- an infranodus chat export.

The 127 files containing the string `logit_lens` match only the engine filename `util/logit_lens.py` inside `identity.source_sha256`. **No logit-lens, attention, activation or hidden-state data exists for any past run.**

### 3.8 C10Z telemetry (new builds only; not yet produced)

`results/c10z_astra/` does not exist yet. `experiments/track_c/c10z_astra_arms.py` has no telemetry code yet (`grep -n "telemetry|logit_lens|write_norms|target_probs"`: no hits). The design is fixed in `docs/C10Z_ASTRA_PREREG.md` §9(h) (`:467–476`) and §9.1(h′1–h′5) (`:554–604`):

- **File:** `<OUT_DIR>/telemetry/telemetry_p<process>.jsonl`, opt-in through `C10Z_TELEMETRY=1`, admitted only after an INERT MPS check (h′3).
- **The first ASTRA attempt runs with telemetry off.**
- **Line kinds:**
  - phase markers (stage start/end, recipe start/end, write-start, round-end with that round's `seconds`, halt code);
  - one `write_norms` line per round: the Frobenius norm of that round's patch and of the cumulative patch, per carrier layer;
  - one `target_probs` line per round, plus one for the final post: parallel arrays (row, fact, view, q, p);
  - one `logit_lens` line per pristine baseline and per candidate write: top-5 (id, text, prob) at band layers 4–8 for the A7 F0 probe prompts, read at `hidden_states[l+1][:, -1, :]` → `model.model.norm` → `lm_head`, valid for l ≤ 34.
- Every line carries `elapsed_s` and `cumulative_s`.
- **Exact JSON key names are not fixed** until the driver implements them. Phase 2 parses the driver's real output, starting with the stub-proof file that (h′4) produces.

### 3.9 Re-runnable evidence commands (all python-free)

```
jq -r '[paths|select(length<=5)|map(if type=="number" then "[]" else . end)|join(".")]|unique|.[]' results/c10v_layerpick/{step0,pass1,run}.json
jq -c '.recipes.B0.delta_norms.A7_coined_coined, .recipes.B0.band' results/c10v_layerpick/pass1.json
jq -r '.recipes|to_entries[]|.key as $r|.value.arms|to_entries[]|"\($r).\(.key) \(.value.para_full_n)/\(.value.para_n) \(.value.locality_described_as)"' results/c10v_layerpick/pass1.json
jq -c '.readings.B.locality_gates, .readings.B0.label' results/c10v_layerpick/run.json
jq -c '{arm,steps,nloss:(.losses|length),fit:.fit.correct,frozen_parameters_unchanged}' results/c10w_oracle/p1_*/train/*.json
jq -c '.recipes.oracle_p1.arms.A7_coined_coined.extra.generated[0]' results/c10w_oracle/p1_*/eval.json
grep -rl --include='*.json' -e '"para_full_hits"' results | grep -v /labviz/ | wc -l
shasum -a 256 experiments/track_c/c10e_bandknob.py
```

---

## 4. Feasibility of the 14 asks, plus the two scope additions (e, f)

Tiers:
- **NOW**: AVAILABLE NOW (recorded);
- **NEW**: NEW-BUILDS ONLY (needs telemetry);
- **REPLAY**: REPLAY ONLY (observation replay, GPU, operator yes);
- **NO**: NOT FEASIBLE.

Several asks split across tiers.

| # | Item | Tier | Basis |
|---|---|---|---|
| 1 | Result badge (score vs goal, coloured by label) | **NOW** | Count: `para_full_n`/`para_n`, or the reading's `binding`. Goal: `docs/c10_scoreboard.json:.goal` = 61. Label: C10V `run.json:.readings.<R>.label`; C10U `r3_read_after_*.json:.<block>.arms.<arm>.label`; older `verdict.label`; C10W `verdict.json:.final_label`, currently `null` and shown as "not yet labelled". |
| 2 | Per-fact strip (24 squares, rewordings hit of 3) | **NOW** | `detail.<arm>[].para_full_hits` (119 files incl. C10V and C10W). C10U binding arm: only teacher-forced `per_template_hits`, shown as a distinct, labelled strip type. |
| 3 | Side-effect gauge (value vs allowed floor) | **NOW** | Values: `locality_axes`, `locality_described_as`, `extra.same_frame`, `extra.mmlu`. Gate pass/fail: C10V `readings.<R>.locality_gates`. Floors are **not stored**: they are derived from prereg rules (C10V `:74`; C10W `:351–357`) with recipe A's recorded value as input, e.g. 90.0 − 3 = 87.0 vs 86.17. Shown as "derived from rule". Older runs: value only, "no preregistered floor recorded". |
| 4 | Shared write-size scale, numbers on bars, colour only written layers | **NOW** | Written layers = keys of `delta_norms.<arm>` (B0·A7 = `{"8"}` while `band` = 4–8). Units are grouped (absolute norm / relative / ratio); no cross-unit scale. |
| 5 | Side-by-side runs | **NOW** | Pure view over run cards. |
| 6 | Plain-words caption from `docs/c10_evaluations.json` | **NOW** (for linked runs) | 15 entries, keyed by `ref` (`CORPUS/56` …). Run → entry link through an explicit, tested `links.json` (decision IDs alone are ambiguous: `D-C10u-mint2` appears in CORPUS/53, 54 and 55). |
| 7 | Per-layer answer-signal glow (logit lens) | **NEW** for C10Z attempts that run with telemetry (layers 4–8 only, F0 probe prompts, pristine + each candidate write). **REPLAY** for all past runs and all 36 layers. | §3.7: none recorded. |
| 8 | Per-fact layer map + selection margins | **NOW** (C10V only) | `step0.json:.map`, `.G_table[24][5]`, `.winning_margins[2][24]`, `.runner_up`, `.map_reproduced`; `pass1.json:.recipes.B.map`; `run.json:.readings.<R>.{assigned_layers, by_layer, per_edge_3of3, spearman_G_edge}`; `extra.proxy.rows[].rho_per_prompt`. Other families pick no per-fact layer: one fixed band. |
| 9 | Training-round slider (step-5 ceiling) | **NOW** for loss per 10 steps (40 points), step times (400) and final fit. **REPLAY** for answers at each round (no intermediate adapters saved). **NEW** for C10Z per-round write sizes and target probabilities (its "rounds" are solve rounds, not training). | §3.2 |
| 10 | Machine-readable run card | **NOW** | §6 |
| a | Specific words and phrases per layer | **NOW**: subjects, made-up answers, piece counts, canonical and reworded questions (recorded in C10W; SHA-bound transcription for C10V and older), C10W generated text, C10W training phrasings, C10V which facts were written at which layer. **NEW/REPLAY**: the words each layer "leans to" (logit lens). **Tokenizer-only extract (CPU, no model, no GPU; Phase 2a)**: the text of the keyed subject piece and of each answer piece. | §3.6 |
| b | Granular parts of each layer and their impact | **NOW**: the parts and their sizes (`config.json`), which part was written and by how much (`delta_norms`), and untouched-ness (by design for MEMIT, hash-verified for C10W). **REPLAY**: how much each part's activity changed (attention / MLP output change, push toward the answer). | §3.5 |
| c | Wiring, base state and with experiments | **NOW**: the static wiring diagram (main line, two branches per layer, tied output head) and where the edit enters it. **REPLAY**: what flows through it, base vs edited (attention weights, per-part contributions). | §3.5 |
| d | Play a run back, very granular | **NOW**: coarse playback of recorded events (gate records, log markers, 40 loss points, final outcomes). **NEW**: per-round C10Z frames. **REPLAY**: per prompt, per generated piece, per layer, per part. | §7 |

| e | **Program-wide context model** (operator scope addition, §11): every run or card is captioned in its own era's terms | **NOW** for the registry, CORPUS and overlay links, the track, hypothesis, condition and decision. **NOW, documents only** for the pre-June model-family era (Mistral, Llama): there are no result files in `results/` for it, so it gets documentary cards only. | `docs/EXPERIMENT_REGISTRY.md` (54 rows), CORPUS headers 00–56, `docs/SPEC_EXPERIMENT_OVERLAY.md`, `docs/F1_DETERMINATION.md` C1–C10, `docs/HYPOTHESIS_REGISTER_2026-06-18.md`, `docs/SPEC_E2E_GROUND_TRUTH.md` §B, `EVIDENCE_INDEX.md`, runbook §8 tracks |
| f | **"How it all connects" map** with a focus mode (§11.4) | **NOW** | the same sources, parsed as markdown tables and with regex; no model |

Nothing is NOT FEASIBLE outright. Two limits are real, though, and must be stated in the UI:

- **No true "live state" of past runs.** A replay is a re-creation. On MPS it may differ from the run, so it is shown as the run only when the counts reproduce (§7.5).
- **No full ΔW matrices are stored or replayed.** Each one is 2048 × 11,008 fp32 ≈ 90 MB per layer. Only norms and summaries are stored.

---

## 4A. Design and usability (governs every view in §5, §7.6, §8 and §11)

Operator, verbatim: "The Dashboard UI is quite average, not very user friendly for bringing all the science together, fonts are sometimes too small to read, content isn't well organized or connected across disciplines, science, domains. Once this upgrade kicks off we need to put thoughtful, intelligent reasoning and decisions into making sure it addresses these and any other types of issues."

The fault is structural, not cosmetic. Today, every one of 1,438 cards is rendered into one 4.06 MB `index.html`, plus a 2.58 MB `data.js` (`ls -la results/labviz/site/`). The cards sit in a flat list, filtered only by model and by free text. The tabs are organised by kind of page (Now, Runs, 3D …), not by line of science. Picture text is drawn in points and then scaled down. The design below fixes the structure first, then the type, then checks both from screenshots.

### 4A.1 Information architecture

- **Home = the connections map** (§11.4). The first screen answers three questions: "what lines of science exist, how do they connect, and what is running now". The "Now" content becomes a status strip at the top of every page: the running stage, its last log line and time, from the existing log parser.
- **Five top-level destinations, the same on every page:**
  1. **Map** (home; §11.4).
  2. **Science lines**: browse by line of science → experiment → runs. The lines are the F1 conditions C1–C10, the registry tracks, the spec layers and the eras. Each line has its own page: question, era, status, decisions, CORPUS entries, models and runs, all in that line's own terms (§11.2).
  3. **Runs**: search, filter (line, era, model, label, date) and compare (item 5). Results are grouped by experiment and collapsed; duplicate observation cards of one record nest under it.
  4. **Inside the model**: tower, parts, wiring and player (items 4, 7, b, c, d). The run is chosen with a searchable picker grouped by line, never a single `<select>` of 1,438 options.
  5. **Learn and evaluations**: era-aware explainers and evaluation entries, each tagged with its line.
- **Consistent frame on every page:**
  - a breadcrumb (`Layer › Condition › Track › Experiment › Run`);
  - a context chip (era and line, colour-coded and labelled in text);
  - a "data for this view" link to the run card or the context JSON;
  - the evidence-tier badge (RECORDED / TELEMETRY / REPLAY: NOT EVIDENCE).
- **Selection carries across views:** a run chosen anywhere is the run shown in "Inside the model" and is pre-filled in Compare. The URL hash holds the state (`#run=…`, `#line=…`, `#compare=…`), so any view can be linked.
- **Progressive loading:** the first view loads ≤ 1 MB of HTML + CSS + JS + data, uncompressed. Each line's cards load on demand as `cards/<line>.js` chunks.
  - These are classic scripts that assign to `window`, not `fetch()` of JSON. A page opened from `file://` cannot `fetch` local files in Chrome, and the design review (§4A.5) opens the file directly.
  - Run-card `.json` files are written alongside, for AI readers.

### 4A.2 Typography and readability

- **Sizes:**
  - body text 17px on desktop and 16px on a phone, line height 1.5–1.6;
  - **nothing on any page below 13px**: badges, sources, legends, axis labels, layer labels, chart annotations and SVG text all count, measured at rendered size.
- **Line length:** prose blocks at most 72 characters wide (`max-width: 72ch`). Tables and charts may be wider.
- **Contrast:** text ≥ 4.5:1 against its background (WCAG AA). Chart marks, focus rings and control borders ≥ 3:1. Colour is never the only carrier: every coloured state also has a word, a symbol or a pattern (label chips, hatched "not recorded" cells, ✓/✗ on gauges).
- **Charts drawn at display size:** interactive views are inline SVG or canvas drawn by JS in CSS pixels, so the 13px floor holds at every width. The saved matplotlib pictures stay as downloads only and are regenerated so that their smallest text is ≥ 13px when shown 600px wide.
- **Phone:**
  - no horizontal page scroll at 360px;
  - 44px touch targets;
  - the 3D canvas at most 70% of the viewport height;
  - tables become stacked label–value rows;
  - the map becomes a drill-down list (§11.4).
- **Numbers:** tabular figures; units always printed; counts written as "12 of 72", not as a bare "12".

### 4A.3 Audit of today's `tools/labviz/style.css` and `index.html`

| File:line | Problem |
|---|---|
| `style.css:17` | `.eyebrow` at `.8rem` = 12.8px, uppercase with wide letter-spacing: below the 13px floor and hard to read |
| `style.css:19` | `.source` at `.8rem` = 12.8px. The source citations, which carry the evidence trail, are the smallest text on the page |
| `style.css:26` | `.badge` at `.78rem` = 12.5px: date, model and schema badges are below the floor |
| `style.css:36` | `.slab` at `12px`: the 2D tower's layer labels |
| `style.css:47` | `.legend` at `.9rem` = 14.4px: readable, but smaller than the body text it explains |
| `style.css:11` | `max-width: 1200px` with no prose measure: paragraphs run to about 130 characters per line on desktop |
| `style.css:33` | `#tower { height: 570px }` is fixed: taller than a 390px-high phone in landscape |
| `style.css:41–42` | The C10 goal and baseline are hard-coded as positions (`84.7222%` = 61/72, `19.4444%` = 14/72) and applied to the history rows |
| `style.css:50` | At ≥ 800px the run picture shares a two-column grid with the text, so the picture shrinks to about half width |
| `render.py:18`, `:78`, `:94`, `:102`, `:105` | Picture fonts are 9pt, 8pt and **6pt** in a 5.1-inch figure (`:61`). Shown at a phone's ≈ 360px content width, they render at about 9px, 8px and **6px** (5.1 in = 367 pt ≈ 490 CSS px, scaled to 360) |
| `index.html:8` | Seven tabs organised by kind of page, not by line of science. They wrap to 3–4 rows on a phone. No breadcrumb, no persistent context |
| `index.html:19–32` | Runs: one flat list of 1,438 cards, 24 per page, filtered by model and text only. No grouping by experiment, line or era. Titles come from filename prefixes (`build.py:27–60`) |
| `index.html:25–27` | Every card repeats the same generic sentences ("This is an observation from the named setup …") instead of the run's own question |
| `index.html:28–30` | Raw field names (`recipes.B.arms…`) are shown as the only explanation of the measurements |
| `index.html:33` | The 3D run picker is one `<select>` with 1,438 options, which opens on a run with no layers (investigation §4) |
| `index.html:36` | The Models tab is a dense card per model with C10-only score lines (see §11.3). Nothing links a model to the lines of science it was used for |
| `index.html:37–41` | History: "Every result, in context" shows only the C10 scoreboard on a 72-scale. The 56 CORPUS entries follow as an unconnected flat list |
| `index.html:42` | Learn: ten explainers, all C10-specific (`render.py:138–149`) |
| `index.html:43–45` | Evaluations: C10 entries, then every earlier experiment with the same boilerplate ("Read the cited evidence entry") |
| `index.html:6` | `model.js` is loaded as `type="module"`. Chrome blocks module scripts from `file://`, so the 3D view cannot be reviewed from the file (UNVERIFIED here; Codex verifies). v2 loads it as a classic script: it has no static `import`, and the CDN dynamic `import()` stays |
| site size | `index.html` 4,056,930 bytes plus `data.js` 2,580,998 bytes, all loaded up front: slow on a phone over Tailscale |

### 4A.4 Acceptance criteria (a design reviewer checks these from screenshots, plus one computed-style dump)

1. The home screen at 390 × 844 shows the map (or its drill-down list) and the status strip, with no horizontal scroll.
2. Every page shows the same five-item navigation, a breadcrumb, a context chip and the evidence-tier badge.
3. The computed-style dump (§4A.5) reports **no visible text node below 13px** and body text ≥ 16px, at every width.
4. No prose block is wider than 72 characters. Spot-check three paragraphs per screenshot.
5. Text contrast ≥ 4.5:1 for every colour pair in the token list. The reviewer checks the token table the build prints.
6. A non-C10 run (G6.1 or D1) and the Mistral-7B model page show **no** C10 terms ("72", "61", "reworded", "made-up"). Their captions use their own era's question and measure (§11).
7. From any run, the reader reaches its line of science in one tap, and that line's place on the map in two.
8. Map focus mode on F1 condition C10 highlights its experiments, decisions, CORPUS entries and models, dims the rest, and lists the links it shares with other lines (e.g. §8.9).
9. Every chart has a plain-words caption and a "does not mean" line, both visible without opening anything.
10. Run picker: at most 2 taps or keystrokes to find a run by experiment name; no list longer than 50 visible items at once.
11. At 844 × 390 landscape, the 3D canvas fits, with controls visible.
12. Every coloured state is also carried by text or a pattern (checked in a greyscale screenshot).
13. First-view payload ≤ 1 MB, reported by the build.
14. A replay view (when Phase 3 lands) shows the NOT EVIDENCE banner in every screenshot of it.

### 4A.5 Design-review step (part of every phase's done criteria)

1. **Build, then open the file directly.** Open `file://<wt>/results/labviz/site/index.html`, **never the 8765 server**. Do it only when no GPU coordinator is live, as for any build.
2. **Render with a headless browser driven without python**, e.g. Playwright or Puppeteer from `/opt/homebrew/bin/node`, or the session's browser tool.
   - Widths: 1440 × 900 desktop, 390 × 844 phone portrait, 844 × 390 phone landscape.
   - Screens: Map (home), Map in focus mode on C10, one Science-line page per era (T-branch/Mistral, write-engine viability, F1 conditions such as D1, C10), one C10 run (C10V B·A7), one non-C10 run (G6.1), Compare, Inside the model (2D, and 3D when the CDN loads), Learn, Evaluations.
   - Screenshots go to `results/labviz/review/<UTC>/`.
3. **Computed-style dump** from the same browser script: for every visible text node, the font size, colour and background colour. Written as `review/<UTC>/styles.json` with a summary of the minimum size and the minimum contrast.
4. **Decorrelated review.** A reviewer with no part in the build judges every criterion of §4A.4 as PASS or FAIL with a one-line reason: a fresh subagent with no build context, or GPT-6-Astra at high effort per the program's reviewer rule. The verdict table goes to `review/<UTC>/verdict.md`. Any FAIL goes back to the builder. Disagreement between the builder's self-check and the reviewer is surfaced to the operator, not averaged away.

## 5. Per-item design

Every item lists:
- **Shows** and **Source** (file : path);
- **Tier**;
- **Caption** (operator-facing, plain words);
- **Must not imply**.

All views read only the run card (§6). The card is the single source of truth, and the HTML and pictures are renderings of it.

### Item 1: result badge
- **Shows:** "12 / 72 reworded questions recalled (goal 61)". Under it, the preregistered label as a coloured chip (`NULL`), and the test's own bar, e.g. "this test's 'lead' bar: 30" (C10V prereg `:69`).
- **Source:**
  - count `recipes.<R>.arms.<arm>.para_full_n`, or `para_full_binding_n` if present (existing precedence, build.py `:183`);
  - out of `para_n`;
  - count used by the label `run.json:.readings.<R>.binding`;
  - goal `docs/c10_scoreboard.json:.goal`;
  - label (per family, §4 row 1).
- **Colour:** from a new table `tools/labviz/labels.json`, exact label string → class. Classes: `pass`, `lead`, `lead-unreplicated`, `partial`, `tradeoff`, `null`, `underfit`, `control`, `halted-invalid`, `not-labelled`. Qualifier suffixes (`-NOT-REPLICATED`, `-NOT-COMPARABLE`, `-LARGE-WRITE` …) stay printed verbatim. An unknown label renders verbatim in neutral grey with "label not in Lab View's table", never as a guessed colour.
- **Caption:** "How many of the 72 reworded questions the model answered completely right after this test. The program's goal is 61. The coloured word is the label the test's rules gave this result before anyone looked at it."
- **Must not imply:**
  - that green means solved: only a PASS-type label gets green;
  - that `LEAD` means proven: its caption is "promising; not yet repeated";
  - that a count without a label is a result: it shows "not yet labelled" (C10W P1 today).

### Item 2: per-fact strip
- **Shows:** 24 squares in record order, each shaded by how many of its 3 rewordings were answered fully: 0 / 1 / 2 / 3. A missing cell is hatched grey ("not recorded"). A small mark shows a right canonical answer. Tapping a square opens the fact panel (item a).
- **Source:** `recipes.<R>.detail.<arm>[i].{subj, val, para_full_hits, canon_full}`. C10U binding arm: `arm.extra.per_fact_position_curve[i].per_template_hits` (all pieces right with earlier pieces supplied). That strip is titled "with the earlier answer pieces supplied (not a free answer)" and uses a different square outline.
- **Caption:** "One square per made-up fact. Darker = more of its three reworded questions answered fully right."
- **Must not imply:** that strips from the free-answer type and the supplied-pieces type are comparable. They never appear side by side without both titles.

### Item 3: side-effect gauge
- **Shows:** one row per axis: recorded value, allowed limit, a tick at the limit, and pass/fail.
  - "Description of the made-up places stayed similar: 86.17 (needed ≥ 87.0) ✗";
  - "Real capitals changed to a made-up answer: 0 of 12 (allowed ≤ A+1)";
  - "Unrelated capitals kept: 30 of 30 (needed ≥ 29)";
  - "Writing difficulty (perplexity) 21.755 → 21.713";
  - C10W only: "General-knowledge quiz: net 4 of 200 lost (allowed ≤ 4)".
- **Source:**
  - values: `arms.<arm>.locality_described_as`, `.locality_axes.{L1_flipped_to_edited_value, L1_n, L3_top1_agree, L3_n, generic_ppl_pre, generic_ppl_post}`, `.extra.same_frame.{flips, n}`, `.extra.mmlu.net_paired_loss`;
  - recorded pass/fail: `run.json:.readings.<R>.locality_gates.<axis>`;
  - limits: a new `tools/labviz/gates.json`, one entry per family and axis: `{rule:"A − 3", reference_path:"recipes.A.arms.<arm>.locality_described_as", prereg:"docs/C10V_LAYERPICK_PREREG.md", line:74}`.
- **Consistency check:** the derived limit's pass/fail must equal the recorded boolean where one exists. On disagreement the gauge shows "limit could not be reproduced from the rule", and the test fails on the real C10V record.
- **Caption:** "Checks that writing the new facts did not damage other things the model knows. The mark is the limit the test set in advance."
- **Must not imply:** that a passing gauge means no damage anywhere. Only these axes were measured. Limits only exist where a prereg set them.

### Item 4: write sizes on one shared scale; colour only written layers
- **Shows:** per layer, a bar whose length uses **one scale shared by every run with the same unit**, with the number printed on the bar ("55.42").
  - Only layers present in `delta_norms.<arm>` are coloured ("written").
  - The configured band (`recipes.<R>.band`, or the hparams `layers`) is drawn as an outline bracket labelled "configured band 4–8".
  - So B0 shows one coloured bar at layer 8 and an empty bracket over 4–7.
- **Source:** `recipes.<R>.delta_norms.<arm>.<layer>.delta_norm` (unit "absolute write size"), `.relative_delta_norm`, `rel_delta_norm` (relative). Scale max = max over all cards with the same unit (recorded in the card as `scale.max` with its source card).
- **Caption:** "How much the stored numbers in each written layer changed. Bars use one ruler for every run, so lengths can be compared. Grey outline = layers the recipe was allowed to write; colour = layers it actually wrote."
- **Must not imply:** that a longer bar means a better result. Write size is effort, not success: B0's 55.42 at layer 8 gave 12/72; P1's oracle wrote ≤ 7.74 per layer and got 70/72. Different units are never drawn on one ruler.
- **Also fix:** today the 3D/2D view colours the configured band (`app.js:50`, `model.js:19`), and the "Recorded run" selector opens on a run with no layers. v2 defaults the selector to the newest card that has `writes`.

### Item 5: side-by-side runs
- **Shows:** 2 cards (3 on desktop width), aligned: badges, strips, gauges, write bars on the shared scale, and a per-fact comparison row: "both right / only left / only right / neither" counts from the recorded booleans, marked *derived*. State lives in the URL (`#compare=<id>,<id>`). Phone: stacked, with a sticky header naming each run.
- **Caption:** "Two tests next to each other, drawn with the same rulers."
- **Must not imply:** that a difference between two single runs is a real effect. A banner states "one run each; differences of a few questions can be chance" when either card is a single-seed observation.

### Item 6: plain-words caption
- **Shows:** the evaluation entry's five fields (`question`, `result`, `rules_out`, `leaves_open`, `next_step`) above the pictures, with its `ref`.
- **Source:** `docs/c10_evaluations.json:.entries[k]`, chosen through `tools/labviz/links.json` (`{"results/c10v_layerpick/": "CORPUS/56", "results/c10w_oracle/": "CORPUS/55", "results/c10u_mint2/": "CORPUS/54", …}`). A test checks that each mapped CORPUS file exists and contains the record's `decision_id`. An unmapped run shows "no plain-words evaluation linked yet".
- **Must not imply:** that the seeded entries are reviewed analyses. Several seeded fields say "not recorded"; they are shown as they are.

### Item 7: per-layer answer-signal glow (logit lens), Phase 2 and Phase 3
- **Shows:** on the tower, each layer glows by the probability that this layer's "early read-out" gives the expected answer piece. Beside it are the top-5 words at that layer. Before-write and after-write are side by side.
- **Source:**
  - Phase 2: C10Z telemetry `logit_lens` lines (top-5 id/text/prob, layers 4–8, F0 probe prompts). When the expected piece is outside the top-5, the glow shows "below top 5", never 0.
  - Phase 3: replay frames (§7.3, all 36 layers; layer 35 is read from the final logits).
- **Caption:** "A shortcut that asks each stage: if you had to answer now, what would you say? Brighter = more likely to say the stored answer."
- **Must not imply:** that the fact is stored where the glow is bright. The lens shows where the answer becomes readable, not where it was written.

### Item 8: per-fact layer map and selection margins (C10V)
- **Shows:** a 24 × 5 grid (facts × layers 4–8), shaded by `G`. The chosen layer is marked with a ring, the runner-up with a dot. Each row has a margin bar (best − second-best) with the repeat's margin beside it, and the fact's outcome on recipe B (rewordings hit out of 3). Footer:
  - per layer: facts assigned / hits / facts right on all 3 (`by_layer`);
  - "map reproduced on repeat: yes, δ = 0.0";
  - "rank agreement between G and outcome: −0.479 (recorded)".
- **Source:** `step0.json:.{G_table, G_table_repeat, map, repeat_map, winning_margins, runner_up, delta, map_reproduced, concentration}`, `run.json:.readings.<R>.{assigned_layers, by_layer, per_edge_3of3, spearman_G_edge}`, `pass1.json:.recipes.B.detail.A7_coined_coined`.
- **Caption:** "Before writing, a quick test guessed the best depth for each fact. Ring = the chosen depth. Long bar = a clear choice; short bar = nearly a tie."
- **Must not imply:** that the chosen depth is where the fact lives, or that the choice helped. The recorded reading is NULL, and B0 (all at layer 8) scored the same 12.

### Item 9: training-round slider (C10W)
- **Shows:** a slider over training steps 10…400.
  - The loss curve for each adapter of the run family, overlaid: s0, s1, and the s0 retrain `_rt`.
  - Time per step, and the final fit (`fit.correct/fit.n`, `per_fact`).
  - At each slider position: "answers at this step: not recorded; an observation replay can re-create them (NOT EVIDENCE)".
- **Source:** `train/*.json:.{losses, step_seconds, fit, seed, retrain}`; logs `p*-*.log` lines `step N loss X`.
- **Caption:** "Training repeats the facts 400 times. The line shows how many mistakes it still made while learning (lower is better). This is not the score on reworded questions."
- **Must not imply:** that low training loss means the reworded questions are answered: training loss reached ≈ 0.0004, but the score was measured once, at the end.

### Item 10: run card
See §6. Every page section has a "data for this view" link to the card. Each card file sits at `results/labviz/cards/<card-id>.json`, with an index at `results/labviz/cards/index.json`.

### Item a: words and phrases, per run and per layer
- **Shows:**
  - **Fact panel** (from item 2): subject, made-up answer, number of answer pieces, the canonical question and the 3 rewordings with right/wrong per rewording. Where recorded (C10W), also what the model actually wrote ("Vindex Vaskul,").
  - **Per-layer word list** (C10V B, B-shuf): the subjects and answers written at each layer (from `map`).
  - **3D:** hovering a written layer lists its facts.
- **Source:** see §3.6. For C10V and older runs, question text comes from `tools/labviz/stimulus.json` (transcribed constants with `{source_file, lines, sha256}`). A test proves each string occurs verbatim in the source file and that the run's recorded `identity.source_sha256` equals the transcription's SHA. On a mismatch the panel says "question text for this run's code version not transcribed". Keyed piece: "the last piece of the subject name (piece text not recorded for this run)" until Phase 2a.
- **Caption:** "The exact made-up facts and questions this test used."
- **Must not imply:** that the words listed per layer are what that layer "thinks". That reading is item 7.

### Item b: parts of each layer and the impact on them
- **Shows:** an "exploded layer". Each layer opens into its parts, in order:
  1. input normaliser;
  2. attention (16 question-heads sharing 2 key/value groups; q/k/v/o);
  3. add-back;
  4. second normaliser;
  5. MLP (gate, up, SiLU, down; 2,048 → 11,008 → 2,048);
  6. add-back.

  The written part (`mlp.down_proj` at written layers) is coloured with its write size. Every other part is labelled "not changed by this method". The basis is shown: "by design (engine writes only down_proj)" for MEMIT, "checked: 434 of 434 stored tables unchanged by training" for C10W train records. There is a text table, a 2D SVG and a 3D version.
- **Source:** `config.json` (§3.5), hparams `:13`, `delta_norms`, C10W `frozen_parameters_unchanged`, `frozen_parameter_hashes_*`, `base_band_hash`/`final_band_hash`.
- **Phase 3 adds** per-part activity change (attention-output size, MLP-output size, and their push toward the answer, before vs after the write), from replay frames.
- **Caption:** "Each layer has two workers: attention (looks back at earlier words) and the MLP (a lookup step). Our method changes only the last table of the MLP in a few layers; everything else stays as it was."
- **Must not imply:** that unchanged parts behave the same after the write. Their *stored numbers* are unchanged, but what flows through them can change. That is a Phase 3 replay view.

### Item c: wiring, base state and with experiments
- **Shows (Phase 1, static):** the text enters as pieces and is looked up in the word table. A **main line** (the residual stream) runs up through 36 layers. In each layer, attention and the MLP read from the line and add back to it. At the top, a final normaliser and the same word table (tied) turn the line into next-piece probabilities. An overlay marks where MEMIT's edit enters: the output of `down_proj` at the written layers, at the position of the subject's last piece. An "animate" toggle runs a pulse along the line, labelled "diagram, not recorded activity".
- **Phase 3 adds** the replayed flow, base vs edited: line strength per layer, attention lines from the answer position back to the subject pieces, and per-part contributions.
- **Caption:** "How information moves through the model. Every layer reads the running summary and adds its own note."
- **Must not imply:** recorded activity in Phase 1.

### Item d: playback
- **Phase 1 (recorded events):** a timeline per run family. It uses:
  - gate records (`results/c10w_oracle_logs/*.gate.*.json` `{stage, at, ok}`);
  - log terminal markers (`STAGE_EXIT=`, `*_DONE`) and record timestamps (`when_utc`, `identity.created_utc`);
  - the 40 loss points per adapter;
  - final outcomes.

  Scrubbing moves through these events only.
- **Phase 2:** C10Z telemetry frames per round (write sizes per layer, target probabilities per question, lens before and after each candidate write).
- **Phase 3:** the observation-replay player (§7.6).
- **Caption:** Phase 1: "What the run recorded, in order." Phase 3: "A re-creation of the run, step by step (not evidence)."

---

## 6. Run card schema (`labviz.run_card/v1`)

**Leaf rule:** every number, boolean or string that came from a file is a *leaf*: `{"value": V, "src": {"file": "<repo-relative path>", "path": "<jq path>"}}`, and `jq '<path>' <file>` must return `V`. A *derived* leaf replaces `src` with `{"derived": "<formula>", "inputs": [leaf, …], "rule_src": {"file", "line"}}`. A missing value is `{"value": null, "missing": "<reason>", "tier": "REPLAY|NEW|NOW-not-recorded"}`. The builder writes only leaves, never bare numbers.

```json
{
  "schema": "labviz.run_card/v1",
  "card_id": "run-<16 hex, = existing stable id>",
  "evidence_status": "RECORDED (read from result files; Lab View makes no verdict)",
  "built": {"builder_sha256": "<sha of tools/labviz/build.py>", "built_utc": "<iso>"},
  "identity": {
    "family": "c10v_layerpick",
    "source_record": {"file": "results/c10v_layerpick/pass1.json", "sha256": "<sha>"},
    "field": "recipes.B.arms.A7_coined_coined",
    "decision_id": {"value": "D-C10v-layerpick", "src": {"file": "results/c10v_layerpick/pass1.json", "path": ".decision_id"}},
    "recipe": "B", "arm": "A7_coined_coined", "binding_arm": true,
    "seed": null, "replicate": null,
    "model": {"value": "Qwen/Qwen2.5-3B", "src": {"file": "…/pass1.json", "path": ".model.id"}},
    "model_revision": {"value": "3aab1f19…", "src": {"file": "…/pass1.json", "path": ".model.revision"}},
    "date": {"value": "2026-10-08T03:32:38Z", "src": {"file": "…/pass1.json", "path": ".when_utc"}}
  },
  "context": {
    "experiment": {"value": "exp:C10V-layerpick", "src": {"file": "docs/EXPERIMENT_REGISTRY.md", "line": 60}, "matched_by": "registry result path"},
    "question": {"value": "does editing each fact at its own band layer … (step 4, H-8)", "src": {"file": "docs/EXPERIMENT_REGISTRY.md", "line": 60}},
    "track": "track:track_c", "condition": "cond:C10", "spec_sections": ["spec:§8.9"], "layer": "layer:write-engine",
    "era": "era:c10", "hypothesis": "hyp:J6:H-8", "corpus": "corpus:56",
    "measure": {"value": "complete answers to 72 reworded questions; goal 61", "src": {"file": "tools/labviz/contexts.json", "path": ".eras.c10.measure"}}
  },
  "headline": {
    "hits": {"value": 12, "src": {"file": "…/pass1.json", "path": ".recipes.B.arms.A7_coined_coined.para_full_n"}},
    "out_of": {"value": 72, "src": {"file": "…/pass1.json", "path": ".recipes.B.arms.A7_coined_coined.para_n"}},
    "count_used_by_label": {"value": 12, "src": {"file": "results/c10v_layerpick/run.json", "path": ".readings.B.binding"}},
    "program_goal": {"value": 61, "src": {"file": "docs/c10_scoreboard.json", "path": ".goal"}},
    "prereg_bars": [{"name": "LEAD", "text": "count ≥ 30/72 and every locality gate holds", "rule_src": {"file": "docs/C10V_LAYERPICK_PREREG.md", "line": 69}}]
  },
  "label": {"value": "NULL", "src": {"file": "results/c10v_layerpick/run.json", "path": ".readings.B.label"},
            "base": {"value": "NULL", "src": {"file": "…/run.json", "path": ".readings.B.base_label"}},
            "colour_class": "null", "colour_table": "tools/labviz/labels.json"},
  "gates": [
    {"name": "engine fingerprint", "passed": {"value": true, "src": {"file": "…/pass1.json", "path": ".fingerprint.ok"}}},
    {"name": "LAW#5 inertness", "passed": {"value": true, "src": {"file": "…/pass1.json", "path": ".law5.ok"}}},
    {"name": "described_as", "plain": "Description of the made-up places stayed similar",
     "observed": {"value": 86.17, "src": {"file": "…/pass1.json", "path": ".recipes.B.arms.A7_coined_coined.locality_described_as"}},
     "limit": {"value": 87.0, "derived": "A − 3", "comparison": "≥",
               "inputs": [{"value": 90.0, "src": {"file": "…/pass1.json", "path": ".recipes.A.arms.A7_coined_coined.locality_described_as"}}],
               "rule_src": {"file": "docs/C10V_LAYERPICK_PREREG.md", "line": 74}},
     "passed": {"value": false, "src": {"file": "…/run.json", "path": ".readings.B.locality_gates.described_as"}},
     "derived_agrees_with_recorded": true}
  ],
  "per_fact": [
    {"index": 0,
     "subject": {"value": "Zorbland", "src": {"file": "…/pass1.json", "path": ".recipes.B.detail.A7_coined_coined[0].subj"}},
     "answer": {"value": "Vindex Vask", "src": {"file": "…", "path": ".recipes.B.detail.A7_coined_coined[0].val"}},
     "answer_pieces": {"value": 4, "src": {"file": "…", "path": ".recipes.B.detail.A7_coined_coined[0].ntok"}},
     "rewordings_hit": {"value": [true, true, true], "src": {"file": "…", "path": ".recipes.B.detail.A7_coined_coined[0].para_full_hits"}},
     "hit_kind": "free answer",
     "canonical_hit": {"value": true, "src": {"file": "…", "path": ".recipes.B.detail.A7_coined_coined[0].canon_full"}},
     "assigned_layer": {"value": 6, "src": {"file": "…/pass1.json", "path": ".recipes.B.map.Zorbland"}},
     "selection_margin": {"value": 0.0156, "src": {"file": "results/c10v_layerpick/step0.json", "path": ".winning_margins[0][0]"}},
     "generated_text": {"value": null, "missing": "not recorded by this family", "tier": "REPLAY"}}
  ],
  "per_layer": [
    {"layer": 8, "configured": true,
     "written": {"value": true, "derived": "layer key present in delta_norms", "inputs": []},
     "write_size": {"value": 16.31, "unit": "absolute write size (Frobenius norm of ΔW)", "src": {"file": "…/pass1.json", "path": ".recipes.B.delta_norms.A7_coined_coined[\"8\"].delta_norm"}},
     "relative_write_size": {"value": 0.1365, "src": {"file": "…", "path": ".recipes.B.delta_norms.A7_coined_coined[\"8\"].relative_delta_norm"}},
     "facts_assigned": {"value": 2, "src": {"file": "…/run.json", "path": ".readings.B.by_layer[\"8\"].facts"}},
     "lens": {"value": null, "missing": "no logit lens recorded for any past run", "tier": "REPLAY"}}
  ],
  "scale": {"unit": "absolute write size (Frobenius norm of ΔW)", "max": {"value": 55.42, "src": {"file": "…", "path": ".recipes.B0.delta_norms.A7_coined_coined[\"8\"].delta_norm"}}},
  "parts": {"written_module": {"value": "model.layers.{}.mlp.down_proj", "src": {"file": "configs/hparams/qwen25_3b_memit_hparams.json", "path": ".rewrite_module_tmp"}},
            "untouched_basis": "by design (engine writes only this module)",
            "structure": {"layers": {"value": 36, "src": {"file": "hf_cache/hub/models--Qwen--Qwen2.5-3B/snapshots/3aab1f1954e9cc14eb9509a215f9e5ca08227a9b/config.json", "path": ".num_hidden_layers"}}}},
  "stimulus": {"canonical": {"value": "The capital of {} is the city of", "src": {"file": "tools/labviz/stimulus.json", "path": ".c10_harness.canonical"}},
               "bound_by": {"value": "1f6be581…e695", "src": {"file": "…/pass1.json", "path": ".identity.source_sha256[\"experiments/track_c/c10e_bandknob.py\"]"}},
               "keyed_position": {"value": "subject_last", "src": {"file": "configs/hparams/qwen25_3b_memit_hparams.json", "path": ".fact_token"}},
               "keyed_piece_text": {"value": null, "missing": "token text not recorded; Lab View loads no tokenizer", "tier": "Phase 2a extract"}},
  "plain_words": {"entry": {"value": "evaluation-14", "src": {"file": "docs/c10_evaluations.json", "path": ".entries[14].id"}}, "linked_by": "tools/labviz/links.json"},
  "observations": {"telemetry": null, "replays": []},
  "reader_rules": [
    "Reason only from leaves; never from colours, bar lengths or glow.",
    "A derived leaf is Lab View arithmetic over recorded inputs; check its inputs.",
    "Anything under observations.replays is NOT EVIDENCE and never supports a verdict.",
    "A count is a result only together with its label and gates; label null = not yet labelled."
  ]
}
```

- **Cards per run:** one per existing card id; summary-only cards carry `identity`, `label` and `plain_words` only.
- **Size:** ≈ 30–60 KB per full C10 card, ≈ 1,400 cards in total, of which most are small.
- **Validation:** a test resolves **every leaf of every card** with the same jq-path semantics (implemented in python with `json` only) and asserts equality, and asserts that no bare number appears outside a leaf.

---

## 7. Observation-replay tool (Phase 3)

A separate GPU tool. It is **not** part of Lab View. It loads the model and writes NOT-EVIDENCE observation files that Lab View then reads like any other JSON.

### 7.1 Inputs
- A source record and selector, e.g. `results/c10v_layerpick/pass1.json` + `recipe=B, arm=A7_coined_coined`, or a C10W train record + eval recipe.
- A replay plan (`plan.json`):
  - tiers (S, A, R);
  - fact subset;
  - phases (write, eval, locality, training checkpoints);
  - step-checkpoint interval for training replays.
- An operator authorization: the runbook §5.2 D-ID and the GPU-time figure the operator said yes to.

### 7.2 Preconditions (any failure refuses; nothing is written except a refusal record)
1. No GPU coordinator is live, judged by the same inventory rule as `tools/c10w_p2_gate.py:43–54`.
2. Engine fingerprint PASS (LAW#1; `python3 tools/engine_fingerprint.py`, `_cov_cpu == 3`).
3. Every file in the record's `identity.source_sha256` has the same SHA now, or the replay runs from a separate git worktree at a commit where they match. The engine, harness and drivers are **never edited**.
4. Covariance caches match the record's `cov_cache_sha256`. Model id and revision match the record.
5. **Observer inertness (LAW#5 analogue):** on the pristine model, the probe forwards with and without the observers attached give identical tokens and `torch.equal` logits, three passes as in C10Z (h′3). Any other verdict refuses.

### 7.3 What it records

The tool re-executes the recorded recipe through the run's own harness functions, imported unmodified; their import loads the model, as in the drivers. It attaches **read-only** forward hooks and `output_hidden_states`. A *step* is one forward at one position: the last position of a prompt, or of a prompt plus the pieces generated so far.

| Tier | Per step, per layer (×36) | Bytes / layer | Per step |
|---|---|---|---|
| **S** (always) | logit-lens top-5 (int32 id + fp16 p) · expected-piece prob + rank · main-line size · attention-output size and MLP-output size · their push toward the expected piece (dot with its output-table row) · per head: attention to the keyed subject piece (16 × fp16) and head output size (16 × fp16) · top-16 MLP inner units (id + value) | ≈ 180 B | ≈ 6.5 KB |
| **A** (opt-in) | attention weights from the current position to every earlier position, all 16 heads (fp16; ~16 positions) | ≈ 0.5 KB | ≈ 18 KB |
| **R** (opt-in, ≤ 2 facts) | the full main-line vector (2,048 × fp16) | 4 KB | ≈ 147 KB |

Write phase:
- per fact × written layer: the key (11,008 × fp16) and the target residual (2,048 × fp16), ≈ 26 KB;
- per write-optimisation step: loss, expected-piece probability, change size;
- per layer: ‖ΔW‖, the top-16 singular values and the ΔW SHA-256.

The full ΔW is not stored; it is recomputable from the keys, residuals and the SHA-pinned covariance.

Training replay (C10W): same seed, and an adapter checkpoint every 10 steps (4.18 MB each, the recorded adapter size). At each checkpoint the 72 rewordings are evaluated at tier S.

**Attention maps need eager attention.** That can change the numerics, so tier A runs as a **separate observation pass** over the reproduced edited weights. Its own answer counts are shown separately. It is never used for the reproduction check.

### 7.4 Storage budget per run (estimate; UNMEASURED until the first replay)

One arm evaluation:
- 24 facts × (1 canonical + 3 rewordings) × ≈ 6.5 generation steps (A7 `mean_ntok` 5.5 + 1) ≈ 624 steps;
- plus teacher-forced positions (≈ 500) and side-effect prompts (≈ 120: L1 12, L3 30, described-as 24, same-frame 6, relation probes);
- ≈ 1,250 steps per model state, so **≈ 2,500 per arm** (before + after the write).

| Replay | Tier S | Tier S + A |
|---|---|---|
| one arm (incl. ≈ 4 MB write phase) | **≈ 20 MB** | **≈ 65 MB** |
| a C10V-sized pass (4 recipes × 3 arms) | ≈ 0.25 GB | ≈ 0.8 GB |
| C10W P1 eval (8 recipe-arm configs) | ≈ 0.16 GB | ≈ 0.5 GB |
| C10W training replay, one adapter (40 checkpoints ≈ 167 MB + 40 × 468 eval steps at S ≈ 122 MB) | ≈ 0.3 GB | (n/a) |
| tier R add-on (2 facts) | +≈ 15 MB per arm | |

Free space on `/Volumes/memit` today: 119 GiB (`df -h`). Frames are binary (fp16/int32, little-endian) with a JSON index, because JSON encoding would roughly triple the size. Output goes to `results/replays/<family>/<card-id>/<UTC>/`. Lab View copies only the manifests into the site and serves frames lazily. Frames are not tensors of the model, but the builder still treats `.bin` frames as opaque and never interprets them on the server.

**GPU time:** recorded anchors are C10V pass1 ≈ 38 min for 12 arms (`pass1_started.json:.identity.created_utc`… `pass1.json:.when_utc`, 02:54 → 03:32 UTC), C10W P1 eval 5,774 s (`eval.json:.wall_seconds`), and one C10W adapter 523 s (`train/A7_coined_coined_s0_r16.json:.wall_seconds`). The instrumentation overhead is UNMEASURED. The first replay measures it on one arm, and every later request to the operator quotes measured numbers.

### 7.5 Reproduction check and labelling
- **Compared per arm, from the replay's own scoring (pass R, settings as recorded):**
  - `para_full_n`, `canon_full_n`, and the binding count if present;
  - L1 flips, L3 agreement, `same_frame.flips`;
  - every fact's `para_full_hits`.

  Also reported but not gating: `delta_norm` per layer (relative difference) and described-as.
- **Outcomes:**
  - all counts and per-fact hits equal → `"reproduction": "COUNTS REPRODUCED"`, shown as "replay of <run>";
  - otherwise → `"APPROXIMATE REPLAY"`, with a mismatch table (`recorded` / `replayed` per field). It is never shown as the run: banner "This re-creation differs from the scored run in N places; it is an approximation."
- **Training replays:** the 40 recorded loss points vs replayed (max relative difference reported); final `fit.correct` and eval counts compared as above.
- **Manifest** `replay.json` top level:
  - `"evidence_status": "NOT EVIDENCE — observation replay"`;
  - `source_card`, `source_record` (path + SHA-256), `authorization` (D-ID);
  - `environment` (torch, transformers, device, attention implementation), `observer_inertness`, `reproduction`;
  - `gpu_seconds` (measured), `tiers`, `frames_index`.
- **Lab View rules:**
  - every replay view carries a fixed NOT EVIDENCE banner;
  - run cards list replays only under `observations.replays[]`;
  - replay numbers never enter `headline`, `label` or `gates`;
  - replays never feed CORPUS, ledgers or the scoreboard.

### 7.6 Player UI
- **Timeline scrubber** with tracks: phase (write → evaluate → side effects), fact, question, generated piece. Controls:
  - play/pause, step ±1, speed 0.25×–8×;
  - jump to fact or question;
  - keyboard arrows and touch drag, 44 px targets.
- **Synchronised panes:**
  - tower: lens glow and top-5 words per layer;
  - exploded layer: attention vs MLP push toward the answer, per head;
  - wiring: attention lines from the current position to earlier pieces (tier A only);
  - text strip: the question with the pieces generated so far.
- **Before / after:** the same question with pristine and edited frames side by side; differences highlighted.
- **Loading:** frames load per chunk (e.g. per fact), so a phone streams ≈ 1–3 MB at a time.
- **Banners:** "NOT EVIDENCE" always; "APPROXIMATE REPLAY (N mismatches)" when applicable.

### 7.7 Operator gate per replay
The operator is asked in plain words, for example: "Re-create C10V recipe B (3 arms) with full recording: about X GPU-minutes and Y GB of disk; the GPU must be otherwise idle." The yes is recorded as a D-ID in runbook §5.2, and the measured GPU time is appended after the run.

---

## 8. Telemetry views (Phase 2)

- **Parser:** for `results/c10z_astra/**/telemetry/telemetry_p*.jsonl`, written against the driver's real key names once they exist. The first fixture is the (h′4) stub-proof file.
- **Views:** per-round write sizes per carrier layer (round and cumulative), with the same shared scale as item 4 (unit: Frobenius norm of the patch); per-round target probability per question (row × fact × view); lens top-5 before and after each candidate write (item 7); the phase timeline (item d).
- **Labels:**
  - "TELEMETRY: recorded during the run, outside the scored records" on every telemetry view;
  - (h′2) description rule: if the attempt ended HALTED-BUDGET or HALTED-V11, or carries EXCEEDS-TTL, also "timing possibly affected by telemetry".
- **Watching a running attempt without python:** the gate blocks unknown python, so the live path must not start python during an armed stage. The built static site plus browser-side JSONL polling covers this:
  - the browser fetches the telemetry file every 30 s;
  - it is served by the already-exempt `http.server` command line, or a python-free server (`/usr/bin/ruby`, `/opt/homebrew/bin/node` exist);
  - the builder does not rebuild during the run.

  Any new server command needs the program session to add it to the gate's exemption list first.
- **Phase 2a: tokenizer-only stimulus extract.** A CPU tool loads only `tokenizer.json` (no weights, no GPU), outside Lab View. It runs once, when no gate is armed and after an operator ruling on tokenizer use. It writes `results/labviz_stimulus/pieces.json`: subject pieces, the keyed last piece, and answer pieces, all with ids. This is cross-checked against the recorded `target_ids`, `minted_ids` and C10W `head_ids`/`modifier_ids`. Lab View then reads it like any other JSON.

## 9. Build order

| Phase | Contents | Depends on | Rough size |
|---|---|---|---|
| **1: AVAILABLE NOW** | **First, as the foundation (§4A, §11):** the §4A information architecture, type scale and progressive loading; the program context model (`contexts.json` plus a derived graph), the era-correct captions on every tab, the fixes from the §11.3 C10-framing audit, and the connections map with focus mode (e, f). **Then:** run cards plus leaf verifier (10); label table and badge (1); per-fact strip and fact panel (2, a-recorded); side-effect gauge with `gates.json` (3); shared scale, written-only colour, printed numbers, selector default fix (4); compare view (5); captions through `links.json` (6); C10V layer map and margins (8); C10W training slider over recorded loss and step times (9); stimulus transcription with SHA binding (a); exploded layer and static wiring in 2D/3D with "untouched" basis (b, c); recorded-event timeline (d). **Done only after** the §4A.5 file:// screenshot review passes every §4A.4 criterion. | Nothing new; Codex build only when no GPU coordinator is live. | ≈ 1,600–2,300 lines across build.py, render.py, app.js, model.js, index.html and new JSON tables (≈ 600–800 of them for §11); ≈ 40–50 new tests; one to two Codex sessions plus review |
| **2: telemetry and tokenizer extract** | 2a tokenizer extract (keyed and answer piece text); telemetry parser and views (7 for layers 4–8, 9 for C10Z rounds, d per round); python-free live polling. | C10Z driver implements telemetry; (h′3) INERT check (17–85 GPU-min, operator yes); a telemetry-on attempt; operator ruling on tokenizer use. | ≈ 400–700 lines plus tests |
| **3: replay tool and player** | `tools/replay/` (§7) and the Lab View player (§7.6); then 7, b-impact, c-flow and d-granular for past runs. | Operator yes per replay (GPU time); first replay measures overhead; LAW#4 read-source before authoring hooks. | Tool ≈ 1,000–1,500 lines; player ≈ 600–900 lines; per replay ≈ 0.3–1 GB disk; GPU time per pass ≈ the original run's time × an unmeasured factor |

## 10. Open points for review

1. **Label colour classes** (§5 item 1): the exact mapping of each recorded label to a class needs the program session's sign-off. That is a display choice, but it can mislead.
2. **The `links.json` map** is maintained by the program session; Lab View only tests it.
3. **Phase 2a tokenizer use** needs an explicit ruling: the original brief forbade tokenizers inside Lab View, and this design keeps them outside it.
4. **Backlog** (from `/private/tmp/claude-501/labviz_3d_investigation.md` §3, not Phase 1): readers for `update_norm_ratio` (a ratio) and `dW_fro` (offline *predicted*). Both are different units, and `dW_fro` is not an applied write, so they need their own clearly labelled unit groups.
5. **Era framing captions** in `contexts.json` (§11.2) are curated text with checked quotes. The program session should review the first set once.

---

## 11. Program-wide context model and the "how it all connects" map

Operator, verbatim: "we don't want to just have the LabViz be about CQ10, we want all historical science to be read and visualized based on the specific work we were doing at the time. This needs to be built across all parts of the dashboard. And we want to be able to visualize how a particular focus of science connects to the rest and how all of it ties together."

**What happens today.** Choose Mistral-7B in the Runs model filter and the Models tab. Its panel says "Comparable C10 weight-write summary: not recorded" and "Comparable 72-question harness score: not recorded" (`index.html:36`). That judges a June model-family experiment by the October C10 yardstick. Every other tab does the same (§11.3).

### 11.1 Sources (all parseable without a model; read for this spec with `grep`/`sed`/`jq`)

| Source | What it gives | Parse notes (verified) |
|---|---|---|
| `docs/EXPERIMENT_REGISTRY.md` | **54 experiment rows** (`grep -c '^| \*\*'`): ID, track, the question (the "hypothesis" column), script, result path(s), CORPUS ref, status, decision | Column counts vary: 36 rows have 10 `|`-fields, 16 have 9 (the C10K…C10V rows, which have no decision column; their D-ID sits in the status cell), and one each has 11 and 12 (pipes inside text: C10 and R2). **Parse by regex over the whole row:** first cell = ID; second = track; `D-[A-Za-z0-9][A-Za-z0-9_.-]*`; `CORPUS/\d+`; backticked `results/…` paths. Test: 54 rows parsed. `docs/experiment_registry.json` is **stale**: 20 rows, dated 2026-10-04. Do not use it as the source. |
| `CORPUS/NN_*.md` (00–56) | Title (line 1), date, Decision-IDs, model names, artifact filenames (header lines), and an "E2e-map cell:" line where present (16 entries: 23 and 26–40) | Decision IDs appear in the bodies of several docs (`D-C10u-mint2` occurs in 53, 54 and 55), so links come from the **header** (first 12 lines), and a run → CORPUS link never comes from a decision ID alone. |
| `docs/SPEC_EXPERIMENT_OVERLAY.md` | Spec section (`§8.7`, `§8.9 L2` …) ↔ decision IDs, CORPUS refs and status (VALIDATED / AMENDED / PROTOTYPED / OPEN) | Markdown tables in sections A–E; regex for `§[\d.]+`, D-IDs and `CORPUS/\d+` per row |
| `docs/SPEC_E2E_GROUND_TRUTH.md` §B (`:10–17`) | The six layers and their spec sections: Schema §7 · Write Engine §8 · Validation §9 · Security §10 · State Consistency §11 · Orchestration §12. Also the cross-cutting areas §C write path, §E memory management, §F verification, §G read path, §I deployment | Spec section → layer by section number (§8.x → Write Engine …). The mapping table is curated once, with this line cited. |
| `docs/F1_DETERMINATION.md:62–71` | F1 conditions **C1–C10**, with title and spec sections | |
| `docs/HYPOTHESIS_REGISTER_2026-06-18.md` | Hypothesis rows: sections A–G use `A1…A9`, `D1…`, and J.6 (`:172–193`) uses `H-1…H-20+` with a "sequence step" column | Registry questions name them: e.g. C10V "(step 4, H-8)", C10W "(step 5, H-13 …)", C10U "(step 3, H-19)", C10T "(step 2, H-10/H-5)", C10S "(step 1, H-1)". That gives an exact experiment → hypothesis edge. |
| `EVIDENCE_INDEX.md` | Ledger of the write-engine viability era: Gate A, Phase 0/1, s240–s244, tiers T1/T2 (2026-06-17) | Tables: script → result → headline |
| `EXPERIMENT_RUNBOOK.md` §8 (`:447–604`) and §5 (`:280–389`, 76 distinct D-IDs) | Track titles: A "Cross-entity isolation fix", B "Scale / efficiency", C "Multi-token value robustness (G7)", D "Capacity-law / spec reconciliation", E "Deployment", F "Spec implementation-readiness". The decisions ledger. | |
| `docs/t_branch_decision_document_v1_{1..4}.md`, `docs/framework_findings/` (10 files), `docs/session_summaries/` (39 files) | The pre-June **model-family era** (T-branch, workstream WS1, sessions S2.x): the MEMIT ceiling on Llama-3.1-8B, Llama-3.2-3B and Mistral-7B; Qwen2.5-7B "CLEARED 5/5" (`t_branch_decision_document_v1_4.md:7`, `:35`, `:37`) | **No result files in `results/`.** `grep -rli mistral results/**/*.json` finds only research-pass and chat logs. This era gets documentary cards: question, decision, finding, models, with doc:line citations. No run pictures, no invented scores. |

### 11.2 The context model

**Namespaced node IDs (mandatory).** The same short IDs mean different things in different sources:
- `A7` is a registry experiment (bias ablation, track_b), a hypothesis-register row (section A, "Bias ablation in HF Qwen2.5-3B") and a C10 arm (`A7_coined_coined`);
- `A1` and `A2` are both registry experiments and C10 arms;
- `C2` and `C10` are both F1 conditions and experiments.

Nodes are therefore typed:

| Node | ID form | Example |
|---|---|---|
| Spec layer | `layer:<name>` | `layer:write-engine` |
| Spec section | `spec:<§>` | `spec:§8.7` |
| F1 condition | `cond:<Cn>` | `cond:C10` |
| Era | `era:<slug>` | `era:t-branch`, `era:viability`, `era:f1-conditions`, `era:c10` |
| Track | `track:<registry track>`; runbook titles are shown beside, never merged by letter | `track:track_e`. Registry `track_e` = the read contract (R1, R1-bit, R11), but runbook "TRACK E" = Deployment (`:601`). |
| Hypothesis | `hyp:<register section>:<id>` | `hyp:A:A7`, `hyp:J6:H-8` |
| Experiment | `exp:<registry ID>` | `exp:A7`, `exp:C10V-layerpick` |
| Decision | `dec:<D-ID>` | `dec:D-C10v-layerpick` |
| CORPUS entry | `corpus:<NN>` | `corpus:56` |
| Run (card) | `run:<card id>` | |
| Model | `model:<name>` | `model:Mistral-7B` |

**Edges.** Every edge stores the document and line that names both ends. A link means "a document names both", not causation or support, and its tooltip says so.

**Run → context rule.** Applied in order; the first match wins. Ties are listed, never chosen:
1. The source path matches a registry row's result path (exact file, or longest folder prefix).
2. The record's file name appears in exactly one CORPUS header (first 12 lines).
3. The record's `decision_id` equals the first D-ID of exactly one registry row.
4. Otherwise the context is **"not recorded"**, and the card shows its candidates. Nothing defaults to C10.

**Per-run `context` block in the run card** (§6). Each field is a leaf with `src {file, line}`:
- `experiment`, `track`;
- `question`: the registry's question cell, verbatim;
- `condition`, `spec_sections`, `layer`, `era`, `corpus`, `decision`;
- `status`: the registry status cell, verbatim;
- `measure`: what this line counted as its headline, and its unit and bar, if any.

**Era framing (`tools/labviz/contexts.json`, curated).** For each era and each experiment line: the plain-words question, the headline measure, and the bar it was judged against, each with `{file, line, quote}`. A test asserts the quote occurs verbatim at that line. Where a result file holds the headline number, the entry names its jq path, and the test resolves it. Where none does, the entry says "no single headline number recorded; see the CORPUS entry". Example:
- C10 measure: "complete answers to 72 reworded questions; goal 61" (`docs/c10_scoreboard.json:.out_of`, `.goal`);
- model-family era: "facts cleared out of 5 at canonical settings" (`t_branch_decision_document_v1_4.md:35`).

**Every tab reads the context, not C10:**
- *Runs*: grouped and titled by experiment and line, captioned with the line's question.
- *Inside the model*: the band, the written module and the unit come from that run's own record or hparams.
- *History*: one timeline per line, in its own measure, plus a program timeline of decisions across all lines. The C10 72-scale applies only to C10 rows.
- *Models*: each model lists the lines and eras it served, with that era's finding.
- *Learn*: explainers tagged by era. The C10 explainers stay, and the earlier eras get theirs, written from their CORPUS and doc text.
- *Evaluations*: entries tagged by line. Earlier experiments show their registry status and CORPUS verdict line, not boilerplate.

### 11.3 Audit: where today's code hard-codes C10 framing

| File:line | Hard-coded C10 assumption | v2 change |
|---|---|---|
| `build.py:27–54` (`PLAIN`), `:57–60` | Run titles come from filename prefixes, mostly C10 phrases; anything unmatched becomes "Measure the recorded condition …" | Title = the registry/context question of the run's experiment |
| `build.py:193`, `:202` | Grid titles "Reworded questions — free answers" / "Rewordings with supplied earlier pieces" | Title from the line's measure; C10 wording only for C10 runs |
| `build.py:230–234` | Any field label starting `A1`, `A2` or `A7` is captioned as a C10 arm ("one ordinary answer word", "made-up answer names"), which would mislabel the registry experiments A1 (batch vs sequential), A2 (sentinels) and A7 (bias ablation) | Arm roles only for C10-harness contexts |
| `build.py:236` | Card title = `plain_trial + role` | Context-based title |
| `build.py:346–354` | Evaluations seeded only from the C10 scoreboard | Keep the C10 entries; other lines read their registry status and CORPUS verdict |
| `build.py:381`, `:447–457` | History = `docs/c10_scoreboard.json` results only | Per-line timelines plus a cross-line decision timeline |
| `build.py:494–495` | Each model's "best" = C10 scoreboard `kind == 'write'`, or `out_of == 72` | Per-model list of lines, with each line's own headline |
| `build.py:496` | "Now" looks only at `results/c10w_oracle/` logs | Newest log under any results folder, plus the scoreboard queue |
| `build.py:516–519`, `:541` | Evaluations and evidence are C10-only files | Add the context sources to the copied evidence |
| `render.py:28–35` (`score_text`) | Any count reads "N of M **reworded answers**"; any percent reads "% reworded answers" | Unit and noun from the line's measure |
| `render.py:80`, `:85` | "Fact × rewording grid", "Answer piece (token)" | Same |
| `render.py:114–132` (`history_svg`) | x-scale `/72`, lines at 61 ("Goal 61") and 14 ("Usual method ≈14") | Per-line scale; the C10 lines only on C10 |
| `render.py:138–149` | All ten Learn explainers are C10-specific ("61 of 72", "24 facts", "ceiling test") | Era-tagged explainers |
| `index.html:11`, `:16` | "Where we are" = the C10 scoreboard brief and queue | Status strip plus the map (§4A.1) |
| `index.html:36` | Models tab: "Best C10 weight-write summary: … of 72", "Comparable 72-question harness score" for every model, Mistral included | Lines and eras per model |
| `index.html:37–39` | History: "Score out of 72. Dashed green: goal 61. Dashed gold: usual method about 14"; dot position `score / 72` | Per-line |
| `index.html:44–45` | Evaluations: C10 entries first, then the earlier work as boilerplate | Grouped by line |
| `style.css:41–42` | Goal and baseline positions hard-coded (61/72, 14/72) | Remove; drawn from data |
| `models.json:2` | The Qwen2.5-3B note describes only the C10 vocabulary-word result, though the model served every era since June | Note per era |
| `app.js:45`, `model.js:19` | Band colouring from the configured band (also item 4) | Written layers from the record |

### 11.4 The "how it all connects" map (home view)

- **Layout:** layered columns, left to right: spec layer → spec section → F1 condition → track / experiment → decision → CORPUS entry → model. Runs are counted on each experiment node and expand on demand. It is not a force-directed hairball: columns keep it readable, and nodes are sorted by date inside each column.
- **Focus mode:** tap any node, such as `cond:C10`, `exp:G6.1`, `model:Mistral-7B` or `spec:§8.7`.
  - Its upstream and downstream paths light up and the rest dims.
  - A side panel lists each link in plain words with its source line ("CORPUS/22 names D-B1-2 and §8.7").
  - A "shared with other lines" section lists nodes that the focused line shares with other lines: a spec section, a model or a decision. Example: C10 and the D1 capacity line both run through `layer:write-engine`, and through Qwen2.5-3B.
- **Presets:** each F1 condition C1–C10, each registry track, each era, plus "what is running now".
- **Search** across all node labels.
- **Phone:** a drill-down list, one column at a time, with a breadcrumb and a back button; focus mode becomes "show connections".
- **Must not imply:** that a link is evidence, that line thickness is importance, or that an absent link proves no relation (the documents may simply not name it). Legend text: "A line means a program document names both ends. Tap a line to see which document."
- **Size:** nodes ≈ 6 layers + ≈ 40 spec sections + 10 conditions + ≈ 15 tracks + ≈ 60 hypotheses + 54 experiments + ≈ 90 decisions (distinct D-IDs across CORPUS, registry and overlay; `grep -ohE` count) + 57 CORPUS entries + 11 models, i.e. ≈ 350 nodes. Runs (1,438) are aggregated.

### 11.5 Tests (added to the Phase 1 brief)

- 54 registry rows parsed. The 9-, 11- and 12-field rows are parsed correctly: C10V → `dec:D-C10v-layerpick` and `hyp:J6:H-8`; R2 keeps its D-ID.
- `exp:A7`, `hyp:A:A7` and the C10 arm `A7_coined_coined` are three distinct nodes. Registry `track_e` and runbook "TRACK E" are not merged.
- `results/c10u_mint2/…` → `exp:C10U-mint2` through the registry path rule, even though `D-C10u-mint2` also occurs in CORPUS 53 and 55.
- A run whose source matches no rule shows "context not recorded" with its candidates.
- The rendered Mistral-7B page and a G6.1 run page contain none of "of 72", "goal 61", "reworded", "made-up", "C10".
- Every `contexts.json` quote occurs verbatim at its cited line. Every edge's source line contains both ends' identifiers.
- The map's focus on `cond:C10` reaches `spec:§8.9` (through `F1_DETERMINATION.md:71`). Through the overlay row "§8.9 L2 — multi-token CORE values (C10 chain)", it reaches every decision that row names and those decisions' experiments and CORPUS entries. The test derives the expected set from the files; it is not hard-coded.
- The model-family era: `model:Mistral-7B` links to `era:t-branch` through `t_branch_decision_document_v1_4.md`, and its page shows documentary cards only.
