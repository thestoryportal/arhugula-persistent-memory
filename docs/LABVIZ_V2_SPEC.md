# Lab View v2: design spec

**Status:** v2, folded from the Astra and advisor reviews (2026-10-08). Operator ruling **D-C10r-labviz-2** (`EXPERIMENT_RUNBOOK.md`, row at `:372`). Codex brief for Phase 1: `results/labviz_v2_codex_brief.md`. Reviews: `results/labviz_v2_spec_astra.md`, `results/labviz_v2_spec_advisor.md` (both FIX-FIRST); every finding's disposition: `results/labviz_v2_fold_map.md`.
**Scope additions from the operator (2026-10-07):**
- §4A, design and usability, governs every view;
- §11, the program-wide context model and the "how it all connects" map, places every run in its own era's terms. Both are in Phase 1.

**How this was written:** while P2 was running, without any python process. Every field name and value below was read with `jq`, `grep`, `sed` or `ls` from the files named. §3.9 lists the commands, so anyone can re-run them. Values marked *UNMEASURED* are estimates. File and card counts move while P2 writes; each is dated ("at 2026-10-08").

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
| **An AI** (program session, reviewer, Codex) | Reason from data, never from pixels. | One **run card** JSON per run (§6). Every value in it is a typed leaf (§6): a JSON source with its jq path, a document source with its line and quote, a derived value with its inputs, or a named missing value. Every record of an observation replay is labelled NOT EVIDENCE, and every sandbox try EXPLORATORY. |

## 2. Rules that bind every phase

1. **Read-only, model-free.** Lab View reads JSON, JSONL and log files, numbered CORPUS headers, the scoreboard, the evaluations file, referenced hparams, and the model's `config.json`. It never imports or runs experiment or engine code. It never opens `.safetensors`, `.pt`, `.npz`, tokenizer or vocabulary files. It never uses the GPU.
2. **Missing stays missing.** If a field is absent, the card and the picture say "not recorded for this run" and name the tier that would supply it (§4). Nothing is interpolated or guessed.
3. **No python while a GPU stage gate is armed.** `tools/c10w_p2_gate.py:21–30` blocks the next GPU stage if any unknown python process is running. It exempts only two exact Lab View command lines: `.venv/bin/python -B -m http.server 8765 --bind 0.0.0.0 --directory results/labviz/site` and `.venv/bin/python -B tools/labviz/build.py`. Consequences:
   - v2 keeps both command lines **byte-identical**, so it adds no CLI flags, and `tools/labviz_serve.sh` stays unchanged;
   - the builder starts no child process (no `subprocess`, `os.system`, `multiprocessing`); a child python would be an unknown python to the gate;
   - tests, Codex builds and replays run only when no GPU coordinator is live;
   - future gates may not carry these exemptions, so "no python during a gated run" is the safe default.

   **The premise behind the exemption, and the build budget.** `tools/labviz_serve.sh:13–19` reruns the builder every 60 s while the server runs, including during GPU stages, and the science runs carry wall-time and memory guards (INVALID-BUDGET, EXCEEDS-TTL). The exemption holds only while the builder stays model-free (no torch import), short and light. So v2:
   - writes a file only when its bytes change (v1's `write_if_changed`, `build.py:535`) and skips a picture whose inputs are unchanged; tested by a warm rebuild that changes no output mtime and calls the picture renderer zero times;
   - is **deterministic**: output bytes depend only on the bytes (and, for logs, the mtimes v1 already reads) of the input files; no output carries the wall-clock time; the build log may;
   - meets a program-set budget, measured and reported by every build: **warm rebuild (no input changed) ≤ 15 s wall and ≤ 1.5 GB peak RSS; cold build ≤ 120 s and ≤ 2 GB** (UNMEASURED today; Codex measures both with `/usr/bin/time -l` around the unchanged command line and reports them). A miss is reported, never hidden.
4. **Evidence tiers are labelled everywhere** (one vocabulary, used by `evidence_status` in every card and on every page):
   - **RECORDED**: from a scored result file;
   - **TELEMETRY**: in-run JSONL, opt-in, proven inert, not a scored record;
   - **REPLAY (NOT EVIDENCE)**: an offline re-creation of a run;
   - **EXPLORATORY**: a sandbox try (§12), never evidence.

   A replay is a re-creation, never the historical run. When its scored counts equal the run's (§7.5) it is labelled "re-creation; recorded outcomes matched"; otherwise "approximate re-creation", with the mismatch. It is never called "replay of <run>". Matching final counts do not show that the historical internal trajectory was the same: exact historical internal playback is not available for any past run.
5. **Program rulings (D-C10r-labviz-2).** Lab View stays read-only and model-free. Data the runs did not record comes only from the separate observation-replay tool (§7). GPU time for replays and for the Phase 4 sandbox (§12) is scheduled by the program session, only in GPU-idle windows, science runs first, one GPU job at a time (operator ruling D-C10r-labviz-3, `EXPERIMENT_RUNBOOK.md:373`). Live in-run data exists only as the opt-in, proven-inert telemetry JSONL that new builds write (C10Z prereg §9(h), §9.1(h′)).

---

## 3. Data inventory (Step 1): what the runs actually recorded

Notation: `F:path` means the jq path inside file F. `<R>` is a recipe and `<arm>` is an arm label (`A1_single`, `A2_coherent2`, `A7_coined_coined`, plus `A7_shuf` and `A7_canon` in C10W). A7 is the binding arm, the one with made-up two-word answers. Sample values are quoted so the reader can check them. **Values in the §3 tables are rounded for reading; a run-card leaf always keeps the full recorded value, and only the rendering rounds** (e.g. B·A7 layer 8 `delta_norm` is `16.31455421447754`).

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
| reading | `.readings.<R>.{gain, write_ratio, gate_A, attributed, reasons, spearman_G_edge}` | B0 `write_ratio 0.6435379892895584`, `spearman_G_edge −0.47912964570281436`; **B `spearman_G_edge −0.3162875387734472`** (each recipe has its own) |
| reading (join) | `run.json:.pass_sha256.pass1` | `bf8f162a…119f` = `shasum -a 256 pass1.json`: the reading is bound to this exact record. `.readings` has B0, B and Bshuf only; recipe A (the reference) has no reading |
| per fact (reading) | `.readings.<R>.assigned_layers[24]`, `.per_edge_3of3[24]`, `.per_template[3]` | B0: all 8; `per_template [3,3,6]` |
| per layer (reading) | `.readings.<R>.by_layer.<4..8>.{facts, para_full, edges_3of3}` | B layer 8: `{facts:2, para_full:0, edges_3of3:0}` |
| **step 0 (selector)** | `step0.json:.G_table` and `.G_table_repeat` | 24 × 5 (facts × layers 4–8); row 0 ≈ `[0.832, 0.932, 0.948, 0.922, 0.924]` (recorded `0.8315801442894901` …). `pass1.json:.step0` carries a copy, so `G_table` and `winning_margins` occur in 2 files; Lab View reads `step0.json` |
| step 0 | `.winning_margins[2][24]`, `.runner_up[2][24]` | row 0 = first table, row 1 = repeat (`experiments/track_c/c10v_layerpick_read.py:71–92`). Margin = best G − second-best G |
| step 0 | `.map`, `.repeat_map`, `.map_reproduced` (true), `.delta` (0.0), `.concentration` (15), `.status` ("READY"), `.subjects[24]` | |
| step 0 | `.projected_key_norms[24][5]`, `.installed_share_comparison[24]{subj, max_G, installed_share, band_installed_share}` | |

**Not in C10V records:** generated answer text, rewording template text, token text of answer pieces or of the keyed subject piece, logit lens, attention, activations.

### 3.2 C10W ceiling oracle (step 5): `results/c10w_oracle/`

Directories:
- `step0_20261007T223638_531381Z/`;
- the halted `step0_20261007T220253_584752Z/HALT.json`;
- `p1_20261007T223707_598959Z/`;
- `p2_20261008T034226_086980Z/` (running while v1 of this spec was written; at 2026-10-08 06:06 UTC it holds `HALT.json` (`stage` "p2-eval", `reason` "HALT: evaluation process failed"), `eval.json`, `eval_halt.json` and no `verdict.json`. Lab View shows these as recorded, with no reading of its own);
- gate records in `results/c10w_oracle_logs/*.gate.*.json` (`{stage, at, ok, checks{fingerprint, gpu, dispatch_guards}}`).

| Grain | Field | Shape / sample |
|---|---|---|
| per adapter (training) | `train/<arm>_s<seed>_r16[_rt].json:.losses[]` | `{step, loss}` every 10 steps, **40 points**. A7 s0: step 10 = 7.7066 … step 400 = 0.000411 |
| per step | `.step_seconds[]` | 400 values |
| per adapter | `.fit.{correct, n, per_fact[24], per_template[20]}` | A7: 480/480; `per_template` = 24 each. **End of training only** |
| per adapter | `.{arm, phase, seed, retrain, rank, steps, layers, status, wall_seconds, adapter{path, sha256}}` | rank 16, 400 steps, layers [4..8], A7 s0 wall 523.35 s; adapter file 4,179,028 bytes |
| per parameter tensor | `.frozen_parameter_hashes_before` / `_after` (434 keys each) and `.frozen_parameters_unchanged` (true) | Proves the **base** tensors stayed frozen **during adapter training**; it says nothing about the evaluated model, which has the adapter's ΔW merged into down_proj 4–8. Keys name **every module**, e.g. `model.layers.8.self_attn.q_proj.weight`, `…k_proj.bias`, `…o_proj.weight`, `…mlp.gate_proj.weight`, `…mlp.up_proj.weight`, `…mlp.down_proj.weight`, `…input_layernorm.weight`, `…post_attention_layernorm.weight`, `model.embed_tokens.weight` |
| P1 eval | `p1…/eval.json:.recipes` | `closedform`, `oracle_p1`, `oracle_canon_s0` |
| per arm | `.recipes.<R>.arms.<arm>.{para_full_n, para_n, canon_full_n, locality_described_as, locality_axes}` | oracle_p1·A7 **70/72**, described_as 86.72, L3 30/30, ppl 21.755→21.081. closedform·A7 9/72, described_as 87.56 (closedform is the gates' same-process reference arm "A", prereg `:347`). oracle_canon_s0·A7_canon 2/72, L3 **12/30** |
| per arm | `.extra.mmlu.{accuracy, correct_n, n, net_paired_loss, correct_to_wrong, wrong_to_correct}` | oracle_p1·A7: 0.59, 118/200, net 4, 13 lost / 9 gained |
| **per prompt (text)** | `.recipes.<R>.arms.<arm>.extra.generated[72]` | `{subj, template:"If you visit {}, its capital city is", ids[6], text:" Vindex Vaskul,", contains, full, sibling_subjects}`: **the rewording text and the model's generated words**. Order: `generated[3i+j]` is fact i (`detail[i].subj`) under rewording j in `PTEST` order. `full` is the test's recorded scoring rule: `generated[1]` " Vindex Vaskul," is `full:true` for "Vindex Vask" |
| per arm (answers) | `eval.json:.stimulus.<arm>` | per-arm answer metadata `{base, mean_ntok, ntok_range}`, **not** question text (unlike the older `.stimulus`, §3.6) |
| per frame | `.extra.frames.{canon, train[20], heldout[]}` | `{n:6, flips, rows[{subj, top1, tok:" Th", flip}]}` (fictional bystanders, token text recorded) |
| per layer | `.extra.geometry.<4..8>` | `{delta_norm, trace_delta_cov_deltaT, null_cov_share, application_relative_error, delta_sha256}` |
| per layer | `.recipes.<R>.delta_norms.<arm>.<layer>.delta_norm` | oracle_p1·A7 (merged LoRA ΔW): 7.74, 4.53, 4.55, 5.02, 5.61; closedform·A7: 15.82, 11.89, 11.57, 19.24, 27.56 |
| per fact | `.recipes.<R>.detail.<arm>[24]` | same row schema as C10V (`subj`, `val`, `para_full_hits[3]` …) |
| per layer (hash) | `eval.json:.base_band_hash`, `.final_band_hash`, `.recipes.<R>.band_after_hash` | per-layer SHA-256 of down_proj 4–8 at load, after the last restore, and after each recipe's restore. All equal in P1. These are LAW#5 **restore** checks (`experiments/track_c/c10w_oracle_read.py:313`, `:319`), not before/after-write hashes |
| verdict | `p1…/verdict.json:.{final_label, status, c10_status, f1_changed, class}` | `null`, `"INCOMPLETE"`, `"OPEN/BLOCKING"`, `false` (the P1 verdict; P2 has none); `.class` = `"ORACLE MEASUREMENT — not a route; never promotable as a write-engine result (D-C10r-rulings-3 (2))"`, shown verbatim on every C10W card |
| interim reading (one configuration) | `p1…/interim_reader_configuration_v2.json:.oracle_p1_A7_configuration.{label, count, gates, gate_misses, qualifiers}`, `.status`, `.p1_eval.sha256` | `"PARTIAL-CEILING-LOCALITY-COST"`, 70, `{G1:true, G2:true, G3:true, G4:false, G5:true, G6:true, G7:true}`, `["G4"]`, `["BIGRAM"]`; status `"INTERIM — seed-0 configuration only; no final label, no routing (prereg §8 item 3); step 5 not read"`; `p1_eval.sha256` `f8886427…d60f` = `shasum -a 256 eval.json` (join). Named by `CORPUS/55_C10W_ORACLE_P1_INTERIM.md:24`. The older `interim_reader_configuration.json` holds the same values and is not read |
| step 0 (text) | `step0…/step0.json:.head_modifier_splits.<subj>.{head, head_ids, modifier, modifier_ids, eligible}` | answer split into its two words, with ids |
| step 0 (text) | `step0…/seal_audit.json:.rows[].{id, template}` | 22 rows: the 20 sealed **training phrasings** `T01`–`T20` (select `id` starting with `T`) plus the reserves `R1`, `R2`. `T01` is the canonical question |
| step 0 | `step0…/train_inputs.json:.prompt_ids.<k>.<subj>`, `.fiction[]` | token ids per training phrasing |
| step 0 | `step0…/mmlu200.json:.items[200]{question, choices, answer, subject, prompt}` | forgetting instrument |
| P2 | `p2…/train/*.json` (6 at 2026-10-08: s1 seeds, plus `_rt` retrains of s0) | all `status PASS`, 40 loss points, `frozen_parameters_unchanged true` |
| logs | `p1-*.log`, `p2-*.log` | `"<adapter> step N loss X"` lines (40 per adapter), `STAGE_EXIT=0` |

**Not in C10W records:** per-step answers during training (no intermediate adapters are saved, and the eval runs once at the end), logit lens, attention, activations.

### 3.3 C10U new vocabulary word (step 3): `results/c10u_mint2/`

- Per-run records: `r3/F_r<rep>_<kind>_s<seed>.json` (`kind` ∈ `mint1`, `modifier`, `multi`).
- Record identity: `.block` (`F` or `V2`), `.kind`, `.seed`, `.replicate`, `.decision_id`. Example: `F_r0_mint1_s0.json` → `F`, `mint1`, 0, 0; `F_r1_mint1_s0.json` → the same but `replicate` 1. Both have binding count 46.
- **Binding reading: `results/c10u_mint2/r3_read_after_replicateF.json`, and only that file.** It is named as binding by `CORPUS/54_C10U_MINT2.md:5` ("Binding reading results/c10u_mint2/r3_read_after_replicateF.json"), by the prereg's post-observation note `docs/C10U_MINT2_PREREG.md:190`, and by the registry row `docs/EXPERIMENT_REGISTRY.md:58`. The two other readings, `r3_read_after_v2.json` and `r3_read_after_frozen.json`, are earlier and disagree with it (both give `mint1_s0` `LEAD-NOT-REPLICATED` where the binding reading gives `LEAD`). Lab View never takes a label from them.
- Labels: `.F.arms.<kind>_s<seed>.label` and `.V2.arms.<kind>_s<seed>.label`; block readings `.F.direction` (`ROUTING-BLOCKED-UNDERFIT`) and `.V2.direction` (`NOT-COMPARABLE`). An arm reading applies to the **replicate-0** record of that block, kind and seed. Its nested `.replica.label` is the replica read without a replica of its own, never the arm's label (CORPUS/54, READ note). Recorded values in the binding reading: `LEAD`, `TRADEOFF`, `UNDERFIT`, `LEAD-NOT-REPLICATED-NOT-COMPARABLE`, `TRADEOFF-NOT-COMPARABLE`, `UNDERFIT-NOT-COMPARABLE` (`LEAD-NOT-REPLICATED` occurs only in `.replica.label` and in the non-binding readings).
- Gates: `.F.arms.<arm>.gates.{L1, same_frame, described_as, L3, generic_ppl, cannibal, sibling}` (booleans). Reference: `.F.arms.<arm>.reference` (the same-block A7-multi count, 14 in F).
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
| Totals (at 2026-10-08 06:28 UTC; they grow as records are added) | `para_full_hits` 121 files · `delta_norms` 80 · `locality_described_as` 81 · `L1_flipped_to_edited_value` 56 · `per_template_hits` 21 (all c10u) · `losses` 14 (all c10w) · `G_table` and `winning_margins` 2 each (c10v `step0.json` and its copy in `pass1.json`) · `rho_per_prompt` 1 (c10v pass1). |
| Recorded stimulus | `.stimulus.{CANON, PTEST, FICTION, V_<arm>}` in 57 files at 2026-10-08: the flat `c10b`–`c10j` files and the `c10k`–`c10q` folders (plus one autoresearch file). All 57 hold the same `CANON` and the same three `PTEST` strings in the same order. No `c10s`–`c10v` record carries a top-level `.stimulus`; `c10s_solvefeas/run.json:.held_out_forms.PTEST` records the three rewordings (same order) with their `sha256`. |

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
- **What "untouched" can honestly say:**
  - *MEMIT runs, by design*: the engine edits only `rewrite_module_tmp` at the written layers, so every other part is untouched by design. MEMIT records carry no all-module hash, so Lab View says "untouched by design", never "verified".
  - *C10W, exactly this*: "the 434 base tensors were hash-verified frozen during adapter training; the evaluated model has the adapter's ΔW merged into down_proj 4–8; `base_band_hash` = `final_band_hash` shows the base was restored after evaluation." Sources: train record `frozen_parameter_hashes_before` = `_after`, `frozen_parameters_unchanged: true`; `eval.json:.recipes.<R>.delta_norms`; `eval.json:.base_band_hash`, `.final_band_hash` (restore checks, §3.2).
- **Binding hparams and structure to a run.** A leaf read from `configs/hparams/qwen25_3b_memit_hparams.json` is shown for a run only when the run's `identity.source_sha256["configs/hparams/qwen25_3b_memit_hparams.json"]` equals the file's current SHA-256 (`4225cc6a…`, equal for C10V pass1); otherwise "hparams for this run's code version not read". `config.json` facts are shown for a run only when its recorded `.model.id` and `.model.revision` equal the snapshot's (`3aab1f19…`).

### 3.6 Stimulus text: where the words live

| What | Where recorded (preferred) | Where defined (source) |
|---|---|---|
| Made-up subjects (24) | every `detail.<arm>[].subj` | `experiments/track_c/c10e_bandknob.py:57–61` (`FICTION`) |
| Made-up answers | every `detail.<arm>[].val` (e.g. Zorbland → "Vindex Vask") | `c10e_bandknob.py:229–249`: `coined_head` / `coined_mod` lists, then the A7 formula `head[(2i+1)%24] + " " + mod[(3i+2)%24]` |
| Real-word answers (A1/A2 controls) | `detail.A1_single[].val` | drawn from `configs/screens/g6_screen_qwen3b_v2.json` (`c10e_bandknob.py:226–228`, `:242–245`) |
| Canonical question | `.stimulus.CANON` in the 57 c10b–c10q records (§3.4); C10W seal-audit row `T01`; **not** in c10s–c10v records | `c10e_bandknob.py:51`: `CANON = "The capital of {} is the city of"` |
| Three rewordings (held-out) | `.stimulus.PTEST` in the 57 c10b–c10q records; `c10s_solvefeas/run.json:.held_out_forms.PTEST`; C10W `eval.json:…extra.generated[3i+j].template` | `c10e_bandknob.py:52–56` (`PTEST = [` at `:52`, the strings at `:53`, `:54`, `:55`): `"{}'s capital city is called"`, `"If you visit {}, its capital city is"`, `"The main city and seat of government of {} is"`. Index j of `PTEST` = index j of `para_full_hits` |
| The model's generated words | **C10W only:** `extra.generated[].text` (R5 has its own, §3.10) | none |
| Side-effect prompts | `locality_axes.L1_post_top1` (12 countries → first piece) | `c10e_bandknob.py:277–300`: L1/L3 on `CANON`, 20 `GENERIC` sentences; `"{c} is described as"` at `:475` |
| Keyed position | rule only: `fact_token "subject_last"` (hparams `:5`) | the **text** of the subject's last piece is not recorded anywhere; it needs a tokenizer |
| Training phrasings (C10W) | `step0…/seal_audit.json:.rows[]` with `id` `T01`–`T20` (20 of its 22 rows; `R1`, `R2` are reserves) | |
| Answer word split (C10W) | `step0…/step0.json:.head_modifier_splits` | |
| Minted words (C10U) | `F_*.json:.minted_words` | |

**Binding check without importing code.** `sha256(experiments/track_c/c10e_bandknob.py)` = `1f6be581…e695`. This equals `results/c10v_layerpick/pass1.json:.identity.source_sha256["experiments/track_c/c10e_bandknob.py"]` (checked with `shasum -a 256` and `jq`). So a transcription of the constants above, stored in a Lab View data file, can be bound to a run by SHA.

**Precedence for a run's question text** (first that applies):
1. **Recorded** in the run's own record: `.stimulus.CANON` / `.stimulus.PTEST`, `.held_out_forms.PTEST`, or C10W `extra.generated[3i+j].template`.
2. **SHA-bound transcription** (`tools/labviz/stimulus.json`): only when the run's `identity.source_sha256["experiments/track_c/c10e_bandknob.py"]` equals the transcription's SHA. At 2026-10-08 that SHA occurs in 136 result files (c10s, c10t, c10u, c10v, one c10w file, two autoresearch files; `grep -rl` in §3.9).
3. Otherwise **missing**: "question text for this run's code version not transcribed".

**What the binding checks** (never by importing the file):
- the run's recorded source SHA equals the SHA in the transcription file;
- **role and order, not mere presence**: each transcription entry is `{role: "CANON"|"PTEST", index, text, line}`. The cited line must read `CANON = "<text>"` for the canonical entry (`:51`), and `"<text>",` for `PTEST` entry j, at line 53 + j, inside the list opened by `PTEST = [` at `:52`. For a recorded stimulus, the shown list must equal the recorded array element by element, in order. A transcription with two rewordings swapped must fail (fixture);
- for C10W, `generated[3i+j].subj` equals `detail[i].subj` and `generated[3i+j].template` equals `PTEST[j]`;
- the source file's text is read as text only.

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
# added in v2 (all at 2026-10-08)
jq -c '.recipes.B.delta_norms.A7_coined_coined["8"], .recipes.B0.delta_norms.A7_coined_coined["8"], .when_utc' results/c10v_layerpick/pass1.json
jq -c '.readings.B.spearman_G_edge, .readings.B0.spearman_G_edge, .pass_sha256' results/c10v_layerpick/run.json; shasum -a 256 results/c10v_layerpick/pass1.json
jq -c '.winning_margins[0][0]' results/c10v_layerpick/step0.json
jq -c '.when_utc, .identity.created_utc' results/c10v_layerpick/pass1_started.json
for r in v2 replicateF frozen; do jq -c '[.F.arms|to_entries[]|{(.key):.value.label}]' results/c10u_mint2/r3_read_after_$r.json; done
jq -c '{block,kind,seed,replicate,b:.arm.para_full_binding_n}' results/c10u_mint2/r3/F_r0_mint1_s0.json results/c10u_mint2/r3/F_r1_mint1_s0.json
jq -c '.class, .final_label, .status' results/c10w_oracle/p1_*/verdict.json
jq -c '(.oracle_p1_A7_configuration|{label,gates}), .p1_eval.sha256' results/c10w_oracle/p1_*/interim_reader_configuration_v2.json; shasum -a 256 results/c10w_oracle/p1_*/eval.json
E=$(ls results/c10w_oracle/p1_*/eval.json); jq -c --argjson b "$(jq -c .base_band_hash $E)" '[.base_band_hash==.final_band_hash, ([.recipes[].band_after_hash]|all(. == $b))]' $E
jq -c '.recipes.closedform.arms.A7_coined_coined.locality_described_as' results/c10w_oracle/p1_*/eval.json
jq -c '[.rows[].id]' results/c10w_oracle/step0_20261007T223638_531381Z/seal_audit.json
# every label string in the records (the §5 item 1 table is built from this list; infranodus chat exports excluded)
find results -name '*.json' -not -path 'results/labviz/*' -not -path 'results/infranodus_*' -print0 | xargs -0 jq -r 'paths(type=="string") as $p | select(($p[-1]|tostring)|test("^(label|final_label|base_label|count_label|direction)$")) | getpath($p)' | sort | uniq -c
# records carrying a recorded stimulus, and records carrying the current harness SHA
find results -name '*.json' -not -path 'results/labviz/*' -not -path 'results/infranodus_*' -print0 | xargs -0 jq -r 'select(type=="object" and (.stimulus|type)=="object" and (.stimulus.PTEST|type)=="array") | input_filename' | wc -l
grep -rl --include='*.json' 1f6be5811d7e58f3ebda16867a4a174b1cf24d47f9a2514cf9c3f9d29f18e695 results | grep -v /labviz/ | wc -l
# registry: rows, brace expressions, D-ID grammar (word-bounded; the literal "D-ID" is not an ID)
grep -c '^| \*\*' docs/EXPERIMENT_REGISTRY.md; grep '^| \*\*' docs/EXPERIMENT_REGISTRY.md | grep -o '`results/[^`]*`' | grep '[{]'
sed -n '280,389p' EXPERIMENT_RUNBOOK.md | grep -oE '(^|[^A-Za-z0-9-])D-[A-Za-z0-9]+(-[A-Za-z0-9]+)*' | sed 's/^[^D]*//' | grep -vxE 'D-IDs?' | sort -u | wc -l
# v1 site size
grep -o 'class="run"' results/labviz/site/index.html | wc -l; wc -c results/labviz/site/index.html results/labviz/site/data.js
# added in round 2 (2026-10-08 06:45 UTC)
jq -r '.F.arms, .V2.arms | to_entries[] | "\(.key) \(.value.label) \(.value.gates|if .==null then "no gates" else length end)"' results/c10u_mint2/r3_read_after_replicateF.json
jq -c '.u|keys' results/c10w_oracle/p1_*/eval.json
find results -name '*.json' -not -path 'results/labviz/*' -not -path 'results/infranodus_*' -print0 | xargs -0 jq -r 'input_filename as $f | paths(type=="number") as $p | select($p[-1]=="delta_norm" and ($p|index("delta_norms"))!=null) | "\(getpath($p)) \($f)"' | sort -g | tail -1
sed -n '3p' CORPUS/22_D1_CAPACITY_LAW.md | grep -o 'results/d1_[^`]*'
```

### 3.10 Science outside C10 (inventory for the context model and non-C10 pages)

Operator ruling D-C10r-labviz-4 asks for all historical science. Four lines are inventoried here as the Phase 1 test set; every other registry row gets at least its documentary card (§11). Recorded fields, at 2026-10-08:

| Line | Where it is named | Records | Recorded fields (jq) | Tiers per item |
|---|---|---|---|---|
| **G6.1** (in-weight store, cross-entity at N = 100) | registry `:13`, CORPUS/13 | `results/g6_scale_n_result.json` (7 `g6_*.json` files in all) | `.config{model "Qwen/Qwen2.5-3B", N 100, entities 50, fields ["capital","language"], band [4..8], write_mode "sequential"}`; `.records[100]{entity, field, truth, cf, expressed_at_apply, retained_at_end}`; `.rungs[3]{n, all_record_retention, apply_time_expr, unt_within_loc, unt_cross_loc, unt_global_loc, heldout_top1}`; `.diagnostic{clobbered_after_expressing_count, clobbered}` | badge: NOW, registry status verbatim ("SPLIT (cross-entity FALSIFIED)"), no label field; per-record strip: NOW (expressed / retained, its own strip type); gauge: NOW, values only (no preregistered floor recorded); write sizes: not recorded; 7, b-impact, c-flow, d-granular: REPLAY |
| **D1** (capacity law: drift must count per relation) | CORPUS/22 (`D-D1-1`, `D-D1-2`); no registry row (the registry's B1-size-term row `:19` names "D1 concentration law") | 18 `results/d1_*.json` files, e.g. `d1_concentration_sweep_result.json` | `.experiment` "D1_phase2_concentration_sweep", `.verdict` (a sentence, not a label), `.gap_capital_axis_pp` 0.0, `.gap_total_axis_pp` 50.0, `.total_N` 50, `.band` [4..8], `.CONCENTRATED` / `.DILUTED` `{name, trajectory, end, base_heldout_cap_correct}` | badge: the recorded verdict sentence verbatim; trajectory chart: NOW; others as G6.1. Context: CORPUS/22's header (`:3`) names `results/d1_predictor_map_result.json` and the glob `results/d1_concentration_sweep_result*.json` (4 files), so 5 of the 18 match by the §11.2 header rule; the other 13 resolve to "context not recorded" with CORPUS/22 as a candidate unless `contexts.json` maps them (cited) |
| **B3N** (is in-weight storage necessary) | registry `:24` | none: `docs/B3_IN_WEIGHT_NECESSITY_DECISION.md` | none | documentary card only (question, decision, finding, with doc:line citations); no run pictures |
| **R5** (paraphrase robustness) | registry `:31`, CORPUS/29 | `results/r5_paraphrase_robustness.json`, `results/r5_stats.json` | `.label` "CHARACTERIZATION"; `.prereg`; `.templates{canonical, P_train[2], P_test[3]}` (**recorded stimulus**; `P_test` equals C10's `PTEST`); `.arms.<arm>{n, L1_took, ptest_mean_rate, ptest_any, ptest_per_paraphrase[3], revert_to_true_among_fails}` for `NOVEL_single`, `PRIOR_single`, `PRIOR_multi_same`, `PRIOR_multi_para`; `.rows.<arm>[i]{subj, target, L1_canon, ptest_hits[3], ptest_obs[3]}` (the model's answers); `.contrasts` | badge: NOW (label + rate per arm, in R5's own terms: "held-out paraphrases", never "of 72"); per-fact strip: NOW (`ptest_hits`); words: NOW (`ptest_obs`); write sizes: not recorded |

**Experiment → era (explicit, never inferred from dates or names).** `tools/labviz/contexts.json` assigns each of the 54 registry rows exactly one era (`era:t-branch`, `era:viability`, `era:f1-conditions`, `era:c10`), each assignment with a `{file, line, quote}` citation. A run inherits its experiment's era; a run with no experiment shows "era not recorded". A test asserts all 54 rows have exactly one era.

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
| 1 | Result badge (score vs goal, coloured by label) | **NOW** | Count: `para_full_n`/`para_n`, or the reading's `binding`. Goal: `docs/c10_scoreboard.json:.goal` = 61, shown **only on binding cards** (§5 item 1, roles). Label, one named file per family: C10V `run.json:.readings.<R>.label`; C10U `r3_read_after_replicateF.json:.<block>.arms.<kind>_s<seed>.label` (the binding reading, §3.3; never another reading); older `verdict.label`; C10W `verdict.json:.final_label`, currently `null` and shown as "not judged yet", with `.class` verbatim. |
| 2 | Per-fact strip (24 squares, rewordings hit of 3) | **NOW** | `detail.<arm>[].para_full_hits` (121 files at 2026-10-08, incl. C10V and C10W). C10U binding arm: only teacher-forced `per_template_hits`, shown as a distinct, labelled strip type. |
| 3 | Side-effect gauge (value vs allowed limit) | **NOW** | Values: `locality_axes`, `locality_described_as`, `extra.same_frame`, `extra.frames`, `extra.mmlu`. **Pass/fail only from recorded booleans** for that exact configuration: C10V `run.json:.readings.<R>.locality_gates`; C10U `r3_read_after_replicateF.json:.<block>.arms.<arm>.gates`; C10W `interim_reader_configuration_v2.json:.oracle_p1_A7_configuration.gates` (interim, one configuration). Limits are **not stored**: a rule-derived limit is drawn as a "derived reference line", without ✓/✗ (gate table, §5 item 3). No recorded outcome → "not judged yet". Older runs: value only, "no preregistered limit recorded". |
| 4 | Shared write-size scale, numbers on bars, colour only written layers | **NOW** | Written layers = keys of `delta_norms.<arm>` (B0·A7 = `{"8"}` while `band` = 4–8). Units are grouped (absolute norm / relative / ratio); no cross-unit scale. |
| 5 | Side-by-side runs | **NOW** | Pure view over run cards, under the eligibility contract of §5 item 5. |
| 6 | Plain-words caption from `docs/c10_evaluations.json` | **NOW** (for linked runs) | 15 entries, keyed by `ref` (`CORPUS/56` …). Run → entry link through an explicit, tested `links.json` keyed by **record or phase directory**, never by family folder (decision IDs alone are ambiguous: `D-C10u-mint2` appears in CORPUS/53, 54 and 55). |
| 7 | Per-layer answer-signal glow (logit lens) | **NEW** for C10Z attempts that run with telemetry (layers 4–8 only, F0 probe prompts, pristine + each candidate write). **REPLAY** for all past runs and all 36 layers. | §3.7: none recorded. |
| 8 | Per-fact layer map + selection margins | **NOW** (C10V only) | `step0.json:.map`, `.G_table[24][5]`, `.winning_margins[2][24]`, `.runner_up`, `.map_reproduced`; `pass1.json:.recipes.B.map`; `run.json:.readings.<R>.{assigned_layers, by_layer, per_edge_3of3, spearman_G_edge}`; `extra.proxy.rows[].rho_per_prompt`. Other families pick no per-fact layer: one fixed band. |
| 9 | Training-round slider (step-5 ceiling) | **NOW** for loss per 10 steps (40 points), step times (400) and final fit. **REPLAY** for answers at each round (no intermediate adapters saved). **NEW** for C10Z per-round write sizes and target probabilities (its "rounds" are solve rounds, not training). | §3.2 |
| 10 | Machine-readable run card | **NOW** | §6 |
| a | Specific words and phrases per layer | **NOW**: subjects, made-up answers, piece counts, canonical and reworded questions (recorded in c10b–c10q, c10s_solvefeas and C10W; SHA-bound transcription for c10s–c10v; otherwise "not transcribed", §3.6), C10W generated text, C10W training phrasings, C10V which facts were written at which layer. **NEW/REPLAY**: the words each layer "leans to" (logit lens). **Tokenizer-only extract (CPU, no model, no GPU; Phase 2a)**: the text of the keyed subject piece and of each answer piece. | §3.6 |
| b | Granular parts of each layer and their impact | **NOW**: the parts and their sizes (`config.json`), which part was written and by how much (`delta_norms`), and untouched-ness (by design for MEMIT; for C10W, base frozen during training and restored after evaluation, §3.5). **REPLAY**: a sampled summary of how much each part's activity changed (attention / MLP output change, push toward the answer, top-16 MLP inner units: a summary, not every element). | §3.5 |
| c | Wiring, base state and with experiments | **NOW**: the static wiring diagram (main line, two branches per layer, tied output head) and where the edit enters it. **REPLAY**: what flows through it, base vs edited (attention weights, per-part contributions). | §3.5 |
| d | Play a run back, very granular | **NOW**: the Phase 1 recorded-event scrubber (gate records, log markers, 40 loss points, final outcomes). **NEW**: per-round C10Z frames. **REPLAY**: a re-creation per prompt, per generated piece, per layer, per part (the Phase 3 player). **NO**: the historical run's own internal trajectory. | §7 |

| e | **Program-wide context model** (operator scope addition, §11): every run or card is captioned in its own era's terms | **NOW** for the registry, CORPUS and overlay links, the track, hypothesis, condition and decision. **NOW, documents only** for the pre-June model-family era (Mistral, Llama): there are no result files in `results/` for it, so it gets documentary cards only. | `docs/EXPERIMENT_REGISTRY.md` (54 rows), CORPUS headers 00–56, `docs/SPEC_EXPERIMENT_OVERLAY.md`, `docs/F1_DETERMINATION.md` C1–C10, `docs/HYPOTHESIS_REGISTER_2026-06-18.md`, `docs/SPEC_E2E_GROUND_TRUTH.md` §B, `EVIDENCE_INDEX.md`, runbook §8 tracks |
| f | **"How it all connects" map** with a focus mode (§11.4) | **NOW** | the same sources, parsed as markdown tables and with regex; no model |

Every ask gets a view, but part of the historical detail is **not recoverable**, and the UI states it:

- **NOT FEASIBLE: the internal state of past runs as it happened.** Nothing internal was recorded (§3.7). A replay is a re-creation; on MPS it may differ from the run. When its scored counts equal the run's it is labelled "re-creation; recorded outcomes matched" (§7.5), which still does not show the historical trajectory.
- **No full ΔW matrices are stored or replayed.** Each one is 2048 × 11,008 fp32 ≈ 90 MB per layer. Only norms and summaries are stored.
- **Granular internals are sampled summaries.** Replay tier S keeps the top-16 MLP inner units per step, not all 11,008; per-element views are not offered.

---

## 4A. Design and usability (governs every view in §5, §7.6, §8 and §11)

Operator, verbatim: "The Dashboard UI is quite average, not very user friendly for bringing all the science together, fonts are sometimes too small to read, content isn't well organized or connected across disciplines, science, domains. Once this upgrade kicks off we need to put thoughtful, intelligent reasoning and decisions into making sure it addresses these and any other types of issues."

The fault is structural, not cosmetic. Today (v1 build at 2026-10-08), every one of 1,503 cards is rendered into one 4.25 MB `index.html`, plus a 2.72 MB `data.js` (`ls -la results/labviz/site/`). The cards sit in a flat list, filtered only by model and by free text. The tabs are organised by kind of page (Now, Runs, 3D …), not by line of science. Picture text is drawn in points and then scaled down. The design below fixes the structure first, then the type, then checks both from screenshots.

### 4A.1 Information architecture

- **Home = the connections map** (§11.4). The first screen answers three questions: "what lines of science exist, how do they connect, and what is running now". The "Now" content becomes a status strip at the top of every page: the running stage, its last log line and time, from the existing log parser.
- **Five top-level destinations, the same on every page:**
  1. **Map** (home; §11.4).
  2. **Science lines**: browse by line of science → experiment → runs. The lines are the F1 conditions C1–C10, the registry tracks, the spec layers and the eras. Each line has its own page: question, era, status, decisions, CORPUS entries, models and runs, all in that line's own terms (§11.2).
  3. **Runs**: search, filter (line, era, model, label, date) and compare (item 5). Results are grouped by experiment and collapsed; duplicate observation cards of one record nest under it.
  4. **Inside the model**: tower, parts, wiring and player (items 4, 7, b, c, d). The run is chosen with a searchable picker grouped by line, never a single `<select>` of about 1,500 options.
  5. **Learn and evaluations**: era-aware explainers and evaluation entries, each tagged with its line.
- **Consistent frame on every page:**
  - a breadcrumb (`Layer › Condition › Track › Experiment › Run`);
  - a context chip (era and line, colour-coded and labelled in text);
  - a "data for this view" link to the run card or the context JSON;
  - the evidence-tier badge (RECORDED / TELEMETRY / REPLAY: NOT EVIDENCE / EXPLORATORY).
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
- **Charts drawn at display size:** interactive views are inline SVG, or canvas for marks only, drawn by JS in CSS pixels, so the 13px floor holds at every width. **No text is drawn on a canvas** (3D labels are HTML overlays), so every piece of text can be measured (§4A.4 criterion 3). The saved matplotlib pictures stay as downloads only and are regenerated so that their smallest text is ≥ 13px when shown 600px wide. The builder records each picture's width in pixels and the pixel size of every text element, so the test can check it.
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
| `index.html:19–32` | Runs: one flat list of 1,503 cards (at 2026-10-08), 24 per page, filtered by model and text only. No grouping by experiment, line or era. Titles come from filename prefixes (`build.py:27–60`) |
| `index.html:25–27` | Every card repeats the same generic sentences ("This is an observation from the named setup …") instead of the run's own question |
| `index.html:28–30` | Raw field names (`recipes.B.arms…`) are shown as the only explanation of the measurements |
| `index.html:33` | The 3D run picker is one `<select>` with one option per card (1,503 at 2026-10-08), which opens on a run with no layers (investigation §4) |
| `index.html:36` | The Models tab is a dense card per model with C10-only score lines (see §11.3). Nothing links a model to the lines of science it was used for |
| `index.html:37–41` | History: "Every result, in context" shows only the C10 scoreboard on a 72-scale. The 56 CORPUS entries follow as an unconnected flat list |
| `index.html:42` | Learn: ten explainers, all C10-specific (`render.py:138–149`) |
| `index.html:43–45` | Evaluations: C10 entries, then every earlier experiment with the same boilerplate ("Read the cited evidence entry") |
| `index.html:6` | `model.js` is loaded as `type="module"`. Chrome blocks module scripts from `file://`, so the 3D view cannot be reviewed from the file (UNVERIFIED here; Codex verifies). v2 loads it as a classic script: it has no static `import`, and the CDN dynamic `import()` stays |
| site size | `index.html` 4,248,295 bytes plus `data.js` 2,722,695 bytes at 2026-10-08 06:28 UTC (the 60 s rebuild grows them as P2 writes), all loaded up front: slow on a phone over Tailscale |

### 4A.4 Acceptance criteria (checked by a scripted browser run plus screenshots, §4A.5)

Each criterion names how it is measured. Screenshots alone are not enough for sizes, tap counts, URL state or payload, so those are measured by the browser script.

**One forbidden-word list** for non-C10 content, used here and in the brief: `"of 72"`, `"goal 61"`, `"reworded"`, `"made-up"`, `"C10"`. It applies to the **run or model content region** (the element marked `data-region="content"`), not to the global status strip, the navigation, the breadcrumb or the connections panel, which may legitimately name C10.

1. The home screen at 390 × 844 and at 360 × 780 shows the map (or its drill-down list) and the status strip, with no horizontal scroll (`document.documentElement.scrollWidth ≤ innerWidth`, measured).
2. Every page shows the same five-item navigation, a breadcrumb, a context chip and the evidence-tier badge (DOM check on every screen, plus screenshots).
3. **No rendered text below 13 CSS px; body text ≥ 16px**, at every width and at 200 % zoom. Measured as **computed `font-size` × the rendered transform scale** of the text node: for SVG text, the scale from `getScreenCTM()`; for HTML text, the product of ancestor CSS transforms, `zoom` and the page zoom. Boxes (`getBoundingClientRect()`) are used only for clipping and layout checks, never as the font size, because line-box and glyph heights include leading and font metrics. Fixtures: 12px text with generous line height (must fail), 16px SVG text in a `viewBox` scaled to 0.5 (must fail), 13px text in an unscaled SVG (passes). **No text is drawn on a canvas**: the 3D view's labels are HTML overlays positioned over the canvas (today's `model.js:21–23` draws layer labels into canvas textures; v2 replaces that), so they are measured like any other text.
4. No prose block is wider than 72 characters (measured: each prose block's width ÷ the width of "0" in its font ≤ 72).
5. **Composited contrast**: text ≥ 4.5:1 against its effective background, found by compositing the ancestor backgrounds (non-transparent, with alpha) behind the text node. Chart marks, focus rings and control borders ≥ 3:1 against their effective background.
6. The G6.1 run page, a D1 capacity-law page (CORPUS/22, `results/d1_*.json`; "D1" here is that line, not an F1 condition) and the Mistral-7B model page contain none of the forbidden words in their content region. Their captions use their own era's question and measure (§11).
7. **Scripted tap counts**: from any run page, the reader reaches its line of science in 1 tap and that line's place on the map in 2; from Home, the reader reaches C10's status and one link that C10 shares with the D1 line in ≤ 4 taps. The script records each path and its count.
8. Map focus mode on F1 condition C10 highlights its experiments, decisions, CORPUS entries and models, dims the rest, and lists the links it shares with other lines (e.g. §8.9).
9. Every chart has a plain-words caption and a "does not mean" line, both visible without opening anything.
10. **Run picker, scripted**: the picker filters on every keystroke; after at most 6 typed characters of a registry ID (e.g. `C10V` for `C10V-layerpick`) the experiment is among the first 10 results, and choosing it is 1 tap (scripted for five IDs, counts recorded); no list shows more than 50 items at once.
11. At 844 × 390 landscape, the 3D canvas fits (≤ 70 % of the viewport height), with controls visible.
12. Every coloured state is also carried by text or a pattern (checked in a greyscale screenshot).
13. **First-view payload ≤ 1 MB**, measured by the browser script as the sum of the on-disk sizes of every file the first view loads (from the script's request log), and also reported by the build.
14. **Targets**: every interactive element's bounding rectangle is ≥ 44 × 44 CSS px at phone widths (measured).
15. **URL state**: selecting a run, a line and a compare pair writes `#run=…`, `#line=…`, `#compare=…`; reloading that URL restores the same view (scripted).
16. **Keyboard and touch**: every control is reachable by Tab with a visible focus ring, and the map, picker and slider work by keyboard and by touch emulation (scripted).
17. A replay view (when Phase 3 lands) shows the NOT EVIDENCE banner, and a sandbox view (Phase 4) the EXPLORATORY banner, in every screenshot of it.

### 4A.5 Design-review step (part of every phase's done criteria)

1. **Build, then open the file directly.** Open `file://<wt>/results/labviz/site/index.html`, **never the 8765 server**. Do it only when no GPU coordinator is live, as for any build.
2. **Render with a browser driven without python**: Playwright from `/opt/homebrew/bin/node` (v26.8.2), or the session's browser tool.
   - **Availability, checked 2026-10-08:** Playwright is not installed as a resolvable package (`npx --no-install playwright --version` refuses: "missing packages … playwright@1.64.0"); only stale npx-cache copies exist (1.59-alpha, 1.60.0, 1.61.1 under `~/.npm/_npx/`). `~/Library/Caches/ms-playwright` holds `chromium-1208`, `chromium-1243`, the matching `chromium_headless_shell` builds and `ffmpeg-1011`, and **no WebKit build**. So the review installs Playwright into `/private/tmp/labviz-review/` (`npm i playwright`) and adds WebKit with `npx playwright install webkit` (a download; pre-approved infrastructure, narrated). Safari itself is on the Mac (`/Applications/Safari.app`) as a manual cross-check.
   - Engines: Chromium and **WebKit** (the operator reads on iPhone Safari).
   - Sizes: 1440 × 900 desktop, 390 × 844 phone portrait, **360 × 780** narrow phone, 844 × 390 phone landscape; and 1440 × 900 at 200 % zoom.
   - Screens: Map (home), Map in focus mode on C10, one Science-line page per era (T-branch/Mistral, write-engine viability, F1 conditions, C10), the D1 capacity-law line, one C10 run (C10V B·A7), one non-C10 run (G6.1), Compare, Inside the model (2D, and 3D when the CDN loads), Learn, Evaluations.
   - Screenshots go to `results/labviz/review/<UTC>/`.
3. **Measurement dump** from the same script, written as `review/<UTC>/measure.json` with a summary: per visible text node, the rendered size (criterion 3) and composited contrast (5); per interactive element, its rectangle (14); per chart mark class and focus ring, its contrast (5); the first-view request log and byte total (13); and the scripted task paths with tap and keystroke counts (7, 10, 15, 16).
4. **Who judges.** Codex runs this script as a **self-check** and reports its numbers; it does not judge its own build. **After Codex reports, the program session runs the review**: it re-runs the script, looks at the screenshots, and has a decorrelated reviewer (a fresh subagent with no build context, or GPT-6-Astra at high effort per the program's reviewer rule) judge every §4A.4 criterion PASS or FAIL with a one-line reason, written to `review/<UTC>/verdict.md`. Any FAIL goes back to Codex. Disagreement between Codex's self-check and the reviewer is surfaced to the operator, not averaged away.

## 5. Per-item design

Every item lists:
- **Shows** and **Source** (file : path);
- **Tier**;
- **Caption** (operator-facing, plain words);
- **Must not imply**.

All views read only the run card (§6). The card is the single source of truth, and the HTML and pictures are renderings of it.

### Item 1: result badge
- **Shows (binding card):** "12 of 72 reworded questions recalled (goal 61)". Under it, the preregistered label as a coloured chip (`NULL`), and the test's own bar, e.g. "this test's 'lead' bar: 30" (C10V prereg `:69`).
- **Run role decides what a C10 badge may say.** The role table governs **C10 cards only** (records whose path starts with `results/c10`). Every C10 card carries `identity.role` ∈ {`binding`, `control`, `reference`, `shuffled-control`, `canon-control`}, assigned by this table (first matching row; transcribed into `tools/labviz/gates.json`):

  | Family | Configuration | Role |
  |---|---|---|
  | any | arm `A1_*` or `A2_*` | `control` |
  | any | arm `A7_shuf` | `shuffled-control` |
  | any | arm `A7_canon` | `canon-control` |
  | C10V | recipe `A` | `reference` (same-process comparator; it has no reading) |
  | C10V | recipe `Bshuf`, arm A7 | `shuffled-control` (its label is `NULL-CONTROL-ONLY`) |
  | C10V | recipes `B`, `B0`, arm A7 | `binding` |
  | C10W | recipe `closedform` | `reference` (prereg `:347`) |
  | C10W | recipe `oracle_*`, arm `A7_coined_coined` | `binding` (an oracle measurement, see below) |
  | C10U | record `kind` `multi` | `reference` (the same-block A7-multi, prereg `:92`) |
  | C10U | record `kind` `mint1`, `mint2`, `modifier` | `binding` |
  | older C10 (flat `c10b`–`c10j`, `c10k`–`c10q`) | recipe named `baseline`, `baseline_controls` or `A` | `reference` |
  | older C10 | arm `A7_coined_coined` in any other recipe | `binding` (label is the experiment-level `verdict.label`, captioned so) |
  | any other C10 configuration | | missing leaf: "role not in Lab View's table"; no goal, no label chip |

  - **binding**: count, "goal 61" (from `docs/c10_scoreboard.json:.goal`) and the label. The goal and label appear only here.
  - **control**, **reference**, **shuffled-control**, **canon-control**: the count, and in place of goal and label one line saying what the role is, e.g. "control arm: checks that ordinary facts still write; not labelled by design", "reference arm: the comparator the gates are measured against; not labelled by design". `Bshuf`'s recorded `NULL-CONTROL-ONLY` is shown as recorded, under that line.
  - **C10W cards** always print `verdict.json:.class` verbatim ("ORACLE MEASUREMENT — not a route; never promotable as a write-engine result (D-C10r-rulings-3 (2))").
- **Non-C10 cards** (G6.1, D1, R5 and every other line, §3.10) carry no role and never show the C10 goal or a 72-scale. They show their own sourced label or status and their own measure: R5 its recorded `.label` (`CHARACTERIZATION`, class `characterization`) and its per-arm rates (`.arms.<arm>.ptest_mean_rate`, `ptest_any`); D1 its recorded `.verdict` sentence verbatim (no chip); G6.1, which records no label field, the registry status cell as a document-source leaf ("SPLIT (cross-entity FALSIFIED)", registry `:13`) and its rung values (`.rungs[]`). Where a line records neither, the badge says "no label recorded; see <CORPUS entry>".
- **Joins (every label, gate and reading).** A label, gate boolean or reading attaches to a card only when **family, recipe, arm, seed and replicate** all match, and the recorded hash matches where one exists: C10V `run.json:.pass_sha256.pass1` = SHA-256 of `pass1.json`; C10W `interim_reader_configuration_v2.json:.p1_eval.sha256` = SHA-256 of `eval.json`. C10U arm readings `<kind>_s<seed>` attach to the **replicate-0** record only; the replicate-1 record shows "replica of `<kind>_s<seed>`; the configuration's label is on the replicate-0 card". Equal counts never establish a join: `F_r0_mint1_s0` and `F_r1_mint1_s0` both have binding count 46.
- **Source:**
  - count `recipes.<R>.arms.<arm>.para_full_n`, or `para_full_binding_n` if present (existing precedence, build.py `:183`);
  - out of `para_n`;
  - count used by the label `run.json:.readings.<R>.binding`;
  - goal `docs/c10_scoreboard.json:.goal` (binding cards only);
  - label: one named file per family (§4 row 1; C10U: `r3_read_after_replicateF.json` only).
- **Colour:** `tools/labviz/labels.json` is a transcription of the table below, exact string → class. Every label string that occurs in the records is listed (command in §3.9; at 2026-10-08). An unknown string renders verbatim in neutral grey with "label not in Lab View's table", never a guessed colour. **Green (`pass`) is reserved for a final PASS-type label** (e.g. C10W `PASS-CEILING` in `verdict.json:.final_label`, prereg `:360`); no recorded label is green today.

  | Label (exact) | Class | Where it occurs |
  |---|---|---|
  | `LEAD` | `lead` ("promising under this test; see replication") | C10U binding reading |
  | `LEAD-NOT-REPLICATED` | `lead-unreplicated` | C10U `.replica.label` and the non-binding readings (never shown as an arm label) |
  | `LEAD-NOT-REPLICATED-NOT-COMPARABLE` | `not-comparable` | C10U block V2 |
  | `TRADEOFF` | `tradeoff` | C10U |
  | `TRADEOFF-NOT-COMPARABLE` | `not-comparable` | C10U block V2 |
  | `TRADEOFF_NOT_CLEAN_RESCUE` | `tradeoff` | `c10g`, `c10h_anyedit_pilot` |
  | `UNDERFIT` | `underfit` | C10U |
  | `UNDERFIT-NOT-COMPARABLE` | `not-comparable` | C10U block V2 |
  | `UNDERFIT-AT-50` | `underfit` | `c10s_solvefeas` |
  | `ROUTING-BLOCKED-UNDERFIT` | `underfit` | C10U `.F.direction` |
  | `NOT-COMPARABLE` | `not-comparable` | C10U `.V2.direction` |
  | `INCOMPLETE` | `not-labelled` | C10U readings' `direction` |
  | `NULL` | `null` | C10V `label`, `base_label`, `count_label` |
  | `NULL-CONTROL-ONLY` | `control` | C10V `Bshuf` |
  | `NO_MATERIAL_KNOB_RESCUE` | `null` | `c10e`, `c10f`, `c10k_route_a`, `c10l_covgeom` (legacy summary) |
  | `NO_MATERIAL_BEHAVIORAL_RESCUE` | `null` | `c10g` candidates |
  | `MIXED_NONPROMOTIONAL` | `null` | `c10g` ("no candidate reaches a behavioral lead threshold") |
  | `CONTROL_RECOVERY_FAIL` | `halted-invalid` | `c10h`, `c10j` window50 controls |
  | `PARTIAL-CEILING-LOCALITY-COST` | `oracle-measurement` (caption: "oracle measurement, not a route") | C10W interim per-configuration reading |
  | `CHARACTERIZATION`, `CHARACTERIZATION (not falsification)`, `CHARACTERIZATION (not falsification; D16 auto-reverse + §11.2)` | `characterization` | `r2`, `r5`, `r5b`, `r9`, `r13` |
  | `RESOLVED-BY-SCREENING (no full run; cross-family corruption study is confounded family⊥cardinality + redundant with D1)` | `characterization` | `r3_family_screen` |
  | `base`, `post`, `gguf_f16`, `gguf_q4km` | `not-a-verdict` (no chip: these name a configuration) | `r15_constraint_probe`, `c10l_mint/p4_pred_*` |
  | `null` final label (C10W `verdict.json:.final_label`) | `not-labelled`: "not judged yet" | C10W P1 |

  Classes: `pass`, `lead`, `lead-unreplicated`, `partial`, `tradeoff`, `null`, `underfit`, `control`, `halted-invalid`, `not-labelled`, `not-comparable`, `characterization`, `oracle-measurement`, `not-a-verdict`, plus the grey fallback. Qualifiers stay printed verbatim. **C10W per-configuration labels** are always captioned "oracle measurement, not a route", whatever their class. A configuration-level PASS is never promoted to program success.
- **Caption (binding card):** "How many of the 72 reworded questions the model answered completely right after this test. The program's goal is 61. The coloured word is the label the test's rules gave this result before anyone looked at it."
- **Must not imply:**
  - that green means solved: only a final PASS-type label gets green;
  - that `LEAD` means proven: its caption is "promising under this test; see replication" (the replication status is shown beside it; C10U `mint1_s0` was replicated, CORPUS/54);
  - that a count without a label is a result: it shows "not judged yet" (C10W P1 today);
  - that a control or reference arm's high count is a pass waiting for its label (C10V control arms score 68–71 of 72; B·A1 is 68): those cards show no goal and no label.

### Item 2: per-fact strip
- **Shows:** 24 squares in record order, each shaded by how many of its 3 rewordings were answered fully: 0 / 1 / 2 / 3. A missing cell is hatched grey ("not recorded"). A small mark shows a right canonical answer. Tapping a square opens the fact panel (item a).
- **Source:** `recipes.<R>.detail.<arm>[i].{subj, val, para_full_hits, canon_full}`. C10U binding arm: `arm.extra.per_fact_position_curve[i].per_template_hits` (all pieces right with earlier pieces supplied). That strip is titled "with the earlier answer pieces supplied (not a free answer)" and uses a different square outline.
- **Caption:** "One square per made-up fact. Darker = more of its three reworded questions answered fully right."
- **Must not imply:** that strips from the free-answer type and the supplied-pieces type are comparable. They never appear side by side without both titles.

### Item 3: side-effect gauge
- **Shows:** one row per axis: the recorded value and the test's limit drawn as a tick.
  - **✓ / ✗ only from a recorded gate boolean for this exact configuration** (joined as in item 1). Example (C10V B·A7): "Description of the made-up places stayed similar: 86.17; the test's limit 87.0 ✗", where ✗ is `run.json:.readings.B.locality_gates.described_as == false`.
  - Where no recorded boolean exists, the limit is drawn as a **"derived reference line"** (Lab View arithmetic over recorded inputs under the cited rule) with **no ✓/✗** and the words "no recorded gate result".
  - Where the run has no recorded outcome at all, the row says **"not judged yet"**. C10W P1: only the `oracle_p1`·A7 configuration has recorded (interim) booleans; every other C10W P1 configuration shows reference lines and "not judged yet".
  - Other rows, e.g. "Real capitals changed to a made-up answer: 0 of 12", "Unrelated capitals kept: 30 of 30", "Writing difficulty (perplexity) 21.755 → 21.713", C10W "General-knowledge quiz: net 4 of 200 lost".
- **Gate table** (transcribed into `tools/labviz/gates.json`; every row cites its prereg line and the pinned reader line that computes the recorded boolean). Paths are relative to the candidate arm `…arms.<arm>`; "ref" is the same paths in the reference arm.

  **C10V** (`docs/C10V_LAYERPICK_PREREG.md:74`; reader `experiments/track_c/c10v_layerpick_read.py:342–348`). Reference: `pass1.json:.recipes.A.arms.A7_coined_coined` (same process). Applies to: the A7 arm of B0, B and Bshuf (the configurations with a reading). Recorded boolean: `run.json:.readings.<R>.locality_gates.<gate>`.

  | Gate | Value | Rule | Recorded boolean |
  |---|---|---|---|
  | L1 | `.locality_axes.L1_flipped_to_edited_value` (of `L1_n` 12) | ≤ ref + 1 | `.L1` |
  | same_frame | `.extra.same_frame.flips` (of 6) | ≤ ref + 1 | `.same_frame` |
  | described_as | `.locality_described_as` | ≥ ref − 3 | `.described_as` |
  | L3 | `.locality_axes.L3_top1_agree` (of 30) | ≥ 29 | `.L3` |
  | generic_ppl | `.locality_axes.generic_ppl_post` | ≤ ref `generic_ppl_post` + 0.5 | `.generic_ppl` |

  **C10U** (`docs/C10U_MINT2_PREREG.md:107`; reader `experiments/track_c/c10u_mint2_read.py:122–131`, `L3_MIN` = 29 at `:20`). Reference: the same-block A7-multi record (`r3/<block>_r0_multi_snone.json:.arm`). Applies to: binding records (replicate 0) whose arm reading in `r3_read_after_replicateF.json` carries `.gates`: 7 of its 12 arm readings, 49 booleans. The 5 UNDERFIT readings (`F` `modifier_s0`–`s2`, `V2` `mint2_s1`, `mint2_s2`) carry **no** `.gates`; their rows show recorded values where any exist, no reference line, no glyph, and "not judged: UNDERFIT, no gate reading recorded". Recorded boolean: `.<block>.arms.<kind>_s<seed>.gates.<gate>`. The prereg text says "generic perplexity rise ≤ 0.5"; the pinned reader compares against the reference's post value, so the reference line uses the reader's rule and cites both.

  | Gate | Value | Rule (reader) | Recorded boolean |
  |---|---|---|---|
  | L1 | `.locality_axes.L1_flipped_to_edited_value`, `.extra.L1_minted_n` | ≤ ref + 1 and minted = 0 | `.L1` |
  | same_frame | `.extra.same_frame_flips`, `.extra.frame_minted_n` | ≤ ref + 1 and minted = 0 | `.same_frame` |
  | described_as | `.locality_described_as` | ≥ ref − 3 | `.described_as` |
  | L3 | `.locality_axes.L3_top1_agree`, `.extra.L3_minted_n` | ≥ 29 and minted = 0 | `.L3` |
  | generic_ppl | `.locality_axes.generic_ppl_post` | ≤ ref `generic_ppl_post` + 0.5 | `.generic_ppl` |
  | cannibal | `.extra.post_write_cannibal` | ≤ 2 | `.cannibal` |
  | sibling | `.extra.para_sibling` | ≤ 3 | `.sibling` |

  **C10W** (`docs/C10W_ORACLE_PREREG.md:347–357`; reader `experiments/track_c/c10w_oracle_read.py:258–272`). Reference arm "A" = `eval.json:.recipes.closedform.arms.A7_coined_coined` (not `recipes.A`, which does not exist); arm U = `eval.json:.u.A7_coined_coined` (the unedited model's A7 evaluation, for G6) for **every** configuration, O-A7-canon included: `eval.json:.u` has no `A7_canon` key, and the reader passes `p["u"][A7]` (`c10w_oracle_read.py:361` for the ordinary A7 configurations; `:403` for the canonical control; paired MMLU check `:326`). The canonical control's reference arm "A" is likewise `closedform`·A7 (`:403`). Applies to: O-A7 configurations; O-A7-canon is read on G1–G6 only (prereg `:347`). Recorded boolean, today only for `oracle_p1`·A7: `interim_reader_configuration_v2.json:.oracle_p1_A7_configuration.gates.<gate>` (status INTERIM, seed 0 only).

  | Gate | Value | Rule | Notes |
  |---|---|---|---|
  | G1 | `.locality_axes.L1_flipped_to_edited_value` | ≤ ref + 1 (of 12) | |
  | G2 | `.locality_axes.L3_top1_agree` | ≥ 29 (of 30) | |
  | G3 | `.locality_described_as` | ≥ ref − 3 | compared at 0.01 (reader rounds ×100) |
  | G4 | `.extra.frames.canon.flips` **and** `.extra.frames.train[t].flips` for **every** training frame t (20) | each ≤ the ref's same frame + 1 (of 6) | one row per frame on demand; the gauge row fails if any frame fails |
  | G5 | `.locality_axes.generic_ppl_post` − `.generic_ppl_pre` (own rise; not vs ref) | ≤ 0.5 | each rounded to 3 decimals by the reader |
  | G6 | MMLU-200 net paired correct-item loss vs arm U | ≤ 4 of 200 | inputs `u.A7_coined_coined.extra.mmlu.correct` and the arm's `.extra.mmlu.correct` |
  | G7 | the **matched** O-A7-shuf control's original-map cross-score (`…arms.A7_shuf.extra.cross_score.para_full_n` of the same recipe) | ≤ 2 of 72 | needs the shuf control of the same rank, seed and training attempt (prereg `:357`); without it, "not judged yet". P1 interim records it as `.shuf_cross_score_vs_original_map` = 0 |

  **Older C10 families and non-C10 lines:** values only, "no preregistered limit recorded".

  **Missing values:** if the value or any rule input is missing or not finite, the row shows "not recorded for this run" and draws no reference line. A missing recorded boolean never becomes a derived ✓/✗.
- **Consistency check (a test, not a display):** wherever a recorded boolean exists, the gate-table rule applied to the recorded inputs must give the same boolean. On disagreement the gauge shows "limit could not be reproduced from the rule" and the test fails. The real cases are **every present boolean**: every C10V reading × 5 gates (15), the 7 C10U binding-reading arms that carry `.gates` (49), and the C10W interim configuration × 7 gates (7); separately, the 5 C10U UNDERFIT readings without `.gates` must render no glyph and no invented outcome; plus boundary fixtures (exactly at the limit passes; one past it fails, e.g. G6 loss 4 passes and 5 fails, prereg `:368`) and a mismatch fixture (a recorded boolean joined to the wrong configuration).
- **Caption:** "Checks that writing the new facts did not damage other things the model knows. The tick is the limit the test set in advance; ✓/✗ appears only where the test's own reader recorded a result."
- **Must not imply:** that a passing gauge means no damage anywhere (only these axes were measured), that a derived reference line is a verdict, or that a configuration-level pass is program success. Limits exist only where a prereg set them.

### Item 4: write sizes on one shared scale; colour only written layers
- **Shows:** per layer, a bar whose length uses **one scale shared by every run with the same unit**, with the number printed on the bar ("55.42").
  - Only layers present in `delta_norms.<arm>` are coloured ("written").
  - The configured band (`recipes.<R>.band`, or the hparams `layers`) is drawn as an outline bracket labelled "configured band 4–8".
  - So B0 shows one coloured bar at layer 8 and an empty bracket over 4–7.
- **Source:** `recipes.<R>.delta_norms.<arm>.<layer>.delta_norm` (unit "absolute write size"), `.relative_delta_norm`, `rel_delta_norm` (relative). Scale max = the maximum over a **declared eligible population**: every applied `delta_norm` under a `delta_norms` object in a RECORDED card, one population per unit, listed operand by operand in `results/labviz/site/cards/scales.json`; each card's `scale.max` is a derived leaf pointing at it (§6). At 2026-10-08 06:45 UTC that population is 1,183 values in 80 files (path rule as in §3.9), and its maximum is `113.7967300415039` (`results/c10h_anyedit_pilot.json:.recipes.anyedit_window1.delta_norms.A7_coined_coined["8"].delta_norm`); within C10V alone the maximum is B0·A2 layer 8, `55.45940399169922`.
- **What may share a ruler.** Only applied writes of one unit: absolute norm, relative norm and ratio (e.g. `c10k_route_a`'s `update_norm_ratio`) each get their own ruler. Offline **predicted** sizes (`c10l_covgeom/step0_offline.json` `dW_fro`), injection measurements (`c10s_solvefeas/inject.json`), replay values (NOT EVIDENCE) and sandbox values (EXPLORATORY) never enter a RECORDED ruler or its `scale.max`; each is drawn on its own labelled ruler, if at all.
- **Caption:** "How much the stored numbers in each written layer changed. Bars use one ruler for every run, so lengths can be compared. Grey outline = layers the recipe was allowed to write; colour = layers it actually wrote."
- **Must not imply:** that a longer bar means a better result. Write size is effort, not success: B0's 55.42 at layer 8 gave 12/72; P1's oracle wrote ≤ 7.74 per layer and got 70/72. Different units are never drawn on one ruler.
- **Also fix:** today the 3D/2D view colours the configured band (`app.js:49`, `model.js:19`), and the "Recorded run" selector opens on a run with no layers. v2 defaults the selector to the newest card that has `writes`.

### Item 5: side-by-side runs
- **Shows:** 2 cards (3 on desktop width), aligned: badges, strips, gauges, write bars on the shared scale, and a per-fact comparison row: "both right / only left / only right / neither" counts from the recorded booleans, marked *derived*. State lives in the URL (`#compare=<id>,<id>`). Phone: stacked, with a sticky header naming each run.
- **Eligibility for the per-fact row** (otherwise the row shows "not comparable: <reason>" and only the side-by-side pictures remain): the two cards' facts are joined by subject, answer (`val`), question template and scoring kind (free answer vs teacher-forced vs supplied pieces). Different fact sets, a changed answer for the same subject, different templates or different scoring kinds make the row ineligible; facts are never paired by row index. Fixtures: the same 24 facts in shuffled row order (joins correctly), and two runs whose templates differ (refused).
- **Caption:** "Two tests next to each other, drawn with the same rulers."
- **Must not imply:** that a difference between two single runs is a real effect. A banner states "one run each; differences of a few questions can be chance" when either card is a single-seed observation.

### Item 6: plain-words caption
- **Shows:** the evaluation entry's five fields (`question`, `result`, `rules_out`, `leaves_open`, `next_step`) above the pictures, with its `ref`.
- **Source:** `docs/c10_evaluations.json:.entries[k]`, chosen through `tools/labviz/links.json`, keyed by **record file or phase directory**, never by family folder: `{"results/c10v_layerpick/": "CORPUS/56", "results/c10w_oracle/p1_20261007T223707_598959Z/": "CORPUS/55", "results/c10u_mint2/r3/": "CORPUS/54", "results/c10u_mint2/r3_read_after_replicateF.json": "CORPUS/54", …}`. The longest matching key wins. So C10W P2 (`p2_20261008T034226_086980Z/`), which CORPUS/55's P1 interim result does not describe, shows "no plain-words evaluation linked yet" until the program adds its own entry. A test checks, per key: the mapped CORPUS file exists; its **header (first 12 lines)** contains the record's `decision_id`; and an evaluation entry with that `ref` exists. An unmapped run shows "no plain-words evaluation linked yet".
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
  - "rank agreement between G and outcome on recipe B: −0.316 (recorded)", from `run.json:.readings.B.spearman_G_edge` = `−0.3162875387734472`. B0 has its own value (−0.479) and is never shown on B's map.
- **Source:** `step0.json:.{G_table, G_table_repeat, map, repeat_map, winning_margins, runner_up, delta, map_reproduced, concentration}`, `run.json:.readings.B.{assigned_layers, by_layer, per_edge_3of3, spearman_G_edge}` (the map is recipe B's, so every reading leaf is `.readings.B`), `pass1.json:.recipes.B.detail.A7_coined_coined`.
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
See §6. Every page section has a "data for this view" link to the card. Each card file sits at `results/labviz/site/cards/<card-id>.json`, with the AI-facing index at `results/labviz/site/cards/index.json`. They live under the server's root (`--directory results/labviz/site`), so the "data for this view" links resolve over Tailscale as well as from `file://`.

### Item a: words and phrases, per run and per layer
- **Shows:**
  - **Fact panel** (from item 2): subject, made-up answer, number of answer pieces, the canonical question and the 3 rewordings with right/wrong per rewording. Where recorded (C10W), also what the model actually wrote (" Vindex Vaskul,"), with the line "right/wrong is the test's recorded scoring rule" (that text is scored a full answer for "Vindex Vask").
  - **Per-layer word list** (C10V B, B-shuf): the subjects and answers written at each layer (from `map`).
  - **3D:** hovering a written layer lists its facts.
- **Source:** see §3.6, in its precedence order: the run's **recorded** stimulus first; else the SHA-bound transcription `tools/labviz/stimulus.json` (`{source_file, sha256, entries[{role, index, text, line}]}`), checked for role and order as §3.6 states; else "question text for this run's code version not transcribed". Keyed piece: "the last piece of the subject name (piece text not recorded for this run)" until Phase 2a.
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

  The written part (`mlp.down_proj` at written layers) is coloured with its write size. Every other part is labelled "not changed by this method". The basis is shown in exactly these words. MEMIT: "by design (the engine writes only down_proj)". C10W: "the 434 base tensors were hash-verified frozen during adapter training; the evaluated model has the adapter's ΔW merged into down_proj 4–8; `base_band_hash` = `final_band_hash` shows the base was restored after evaluation" (§3.5). The C10W tower therefore colours down_proj 4–8 as written (the merged adapter), never as "unchanged". There is a text table, a 2D SVG and a 3D version.
- **Source:** `config.json` (§3.5), hparams `:13`, `delta_norms`, C10W `frozen_parameters_unchanged`, `frozen_parameter_hashes_*`, `base_band_hash`/`final_band_hash`.
- **Phase 3 adds** per-part activity change (attention-output size, MLP-output size, and their push toward the answer, before vs after the write), from replay frames: a re-creation (NOT EVIDENCE), and a sampled summary (e.g. the top-16 MLP inner units), not every element.
- **Caption:** "Each layer has two workers: attention (looks back at earlier words) and the MLP (a lookup step). Our method changes only the last table of the MLP in a few layers; everything else stays as it was."
- **Must not imply:** that unchanged parts behave the same after the write. Their *stored numbers* are unchanged, but what flows through them can change. That is a Phase 3 replay view.

### Item c: wiring, base state and with experiments
- **Shows (Phase 1, static):** the text enters as pieces and is looked up in the word table. A **main line** (the residual stream) runs up through 36 layers. In each layer, attention and the MLP read from the line and add back to it. At the top, a final normaliser and the same word table (tied) turn the line into next-piece probabilities. An overlay marks where MEMIT's edit enters: `down_proj` at the written layers. The subject's last piece is where the write's **key is read** (`fact_token "subject_last"`); the changed matrix then acts on every token that passes through that layer (`docs/C10V_LAYERPICK_PREREG.md:50`), and the overlay says so. An "animate" toggle runs a pulse along the line, labelled "diagram, not recorded activity".
- **Phase 3 adds** the replayed flow, base vs edited: line strength per layer, attention lines from the answer position back to the subject pieces, and per-part contributions.
- **Caption:** "How information moves through the model. Every layer reads the running summary and adds its own note."
- **Must not imply:** recorded activity in Phase 1.

### Item d: playback
- **Phase 1 (recorded events):** a timeline per run family. It uses:
  - gate records (`results/c10w_oracle_logs/*.gate.*.json` `{stage, at, ok}`);
  - log terminal markers (`STAGE_EXIT=`, `*_DONE`) and record timestamps (`when_utc`, `identity.created_utc`);
  - the 40 loss points per adapter;
  - final outcomes.

  This **recorded-event scrubber** moves through these events only. **Ordering:** events that carry a recorded timestamp (gate records' `at`, e.g. `"2026-10-07T22:22:29-06:00"`; records' `when_utc`) are sorted by that time normalised to UTC, then source path, then position in the source (line, or array index). Events without one (the C10W `.losses[]` points are `{step, loss}` only, `.step_seconds[]` are durations, and a log marker such as `results/c10w_oracle_logs/p1-eval.log:2` is a bare `STAGE_EXIT=0`) are shown in a separate track, in source and step order, labelled "time not recorded". No absolute time is ever inferred from durations, file names or mtimes. It is not the Phase 3 player (§7.6), which is excluded from Phase 1.
- **Phase 2:** C10Z telemetry frames per round (write sizes per layer, target probabilities per question, lens before and after each candidate write).
- **Phase 3:** the observation-replay player (§7.6).
- **Caption:** Phase 1: "What the run recorded, in order." Phase 3: "A re-creation of the run, step by step; recorded outcomes matched (not evidence)", or "an approximate re-creation" when they did not (§7.5).

---

## 6. Run card schema (`labviz.run_card/v1`)

**Leaf types.** Every value that came from a file, or was computed from one, is one of four typed leaves. The builder writes nothing else, except the structural keys whitelisted below.

1. **JSON-source** `{"value": V, "src": {"file": "<repo-relative path>", "path": "<jq path>"}}`: `jq '<path>' <file>` returns exactly `V`, at full recorded precision (`16.31455421447754`, never `16.31`). Rendering rounds; the card never does.
2. **Document-source** `{"value": V, "src": {"file": "<repo-relative path>", "line": N, "quote": "<text>"}}`: line N (1-based) of the file contains `quote` verbatim, and a string `V` occurs verbatim inside `quote`. Quotes are never truncated with "…".
3. **Derived** `{"value": V, "derived": "<rule in words>", "inputs": [leaf, …], "rule_src": <document-source citation or {"spec": "§…"}>}`: Lab View arithmetic over recorded inputs. `inputs` lists **every operand** of the rule and is never empty; an operand that is a whitelisted structural key of the same card is given as `{"value": V, "structural": "<path in this card>"}` (e.g. the card's own `layer`). A derived context edge lists its **whole chain** of edges (§11.2). **Population derivations** (a scale maximum) are the one exception: they have **no `inputs`**; instead `population` is **schema metadata** (not a leaf, so it carries no `value`) of the form `{"file": "results/labviz/site/cards/scales.json", "path": "<jq path to the operand list>"}`. The verifier resolves that path to the complete operand list, validates every operand as a JSON-source leaf, and recomputes `V` from that list alone. The test recomputes every derived `V` and fails if any operand is missing.
4. **Missing** `{"value": null, "missing": "<reason>", "tier": "REPLAY|NEW|NOW-not-recorded|Phase 2a extract|not-judged-yet"}`.

**Structural keys that may be bare** (they name or arrange things; they are not measurements): `schema`, `card_id`, `evidence_status`, `built`, `sources`, `family`, `field`, `recipe`, `arm`, `index`, `layer`, `node_id`, `edge`, `matched_by`, `population`, `structural`, `unit`, `name`, `plain`, `comparison`, `judgement`, `hit_kind`, `colour_class`, `colour_table`, `reader_rules`. Any other bare number, boolean or string fails the leaf test.

**Every source file is hashed.** `sources[]` lists `{file, sha256}` for every file any leaf or rule cites: result records, readings, documents, `config.json`, hparams, and Lab View's own tables (`labels.json`, `gates.json`, `links.json`, `stimulus.json`, `contexts.json`). The test recomputes each hash.

**Determinism.** A card carries no build time. `built` holds only the builder's SHA-256; the build log may record when it ran.

Example (C10V B·A7; every value checked with `jq`, `sed -n` or `shasum -a 256` at 2026-10-08; Lab View tables that do not exist yet show `<sha at build>`):

```json
{
  "schema": "labviz.run_card/v1",
  "card_id": "run-<16 hex, = existing stable id>",
  "evidence_status": "RECORDED (read from result files; Lab View makes no verdict)",
  "built": {"builder_sha256": "<sha256 of tools/labviz/build.py at build>"},
  "sources": [
    {"file": "results/c10v_layerpick/pass1.json", "sha256": "bf8f162a422cd01bf9763673cd24abbb99a532da889f08c3311174d7942a119f"},
    {"file": "results/c10v_layerpick/run.json", "sha256": "f721c804ba6acda88faf68b4b94bdf10b264d1099e041eaaab86a00902fe808f"},
    {"file": "results/c10v_layerpick/step0.json", "sha256": "96b196167984c48f717451addca935376d49caf13efc2adc5ce750a70f1999dd"},
    {"file": "results/labviz/site/cards/scales.json", "sha256": "<sha at build>"},
    {"file": "docs/c10_scoreboard.json", "sha256": "331a32483a3c4d8666bc1a8477a5b30eb96d5c858e84dac8a9647882154feb2d"},
    {"file": "docs/c10_evaluations.json", "sha256": "0c2fb5a96e017315a2fddf56fe40afd297a7b7cc0298ad655c9468b04ff9e97c"},
    {"file": "docs/EXPERIMENT_REGISTRY.md", "sha256": "6f49e8ed7f024ef3c21d99c29964694e540bc0b77235ad664b949a6d9f996ef2"},
    {"file": "docs/SPEC_EXPERIMENT_OVERLAY.md", "sha256": "3c139767ad5c227290f8b0fdd319e6de9fba9948819908a20ede14de870c7beb"},
    {"file": "docs/F1_DETERMINATION.md", "sha256": "a6e62573d9564cbfb10de4590871c6e997065df5e30f9139901c79ceea2f5944"},
    {"file": "docs/SPEC_E2E_GROUND_TRUTH.md", "sha256": "ff7573878ad9aecec5f6b5a7f5243022fb401ece9b56159f0f65a420a283160e"},
    {"file": "docs/C10V_LAYERPICK_PREREG.md", "sha256": "00981bfc9cb5770ccea203f6682d953948afdba653a4bd4173bbc754130ad524"},
    {"file": "configs/hparams/qwen25_3b_memit_hparams.json", "sha256": "4225cc6aabc3eb9fa62d2bb2cac68b1238de3a39c5e469da635e6e1464aa3bb4"},
    {"file": "hf_cache/hub/models--Qwen--Qwen2.5-3B/snapshots/3aab1f1954e9cc14eb9509a215f9e5ca08227a9b/config.json", "sha256": "27467e2fc311a7656c09a43ae9c3d408211e1f212bbddbc93c8596a06423826f"},
    {"file": "tools/labviz/labels.json", "sha256": "<sha at build>"},
    {"file": "tools/labviz/gates.json", "sha256": "<sha at build>"},
    {"file": "tools/labviz/links.json", "sha256": "<sha at build>"},
    {"file": "tools/labviz/stimulus.json", "sha256": "<sha at build>"},
    {"file": "tools/labviz/contexts.json", "sha256": "<sha at build>"}
  ],
  "identity": {
    "family": "c10v_layerpick",
    "field": "recipes.B.arms.A7_coined_coined",
    "recipe": "B", "arm": "A7_coined_coined",
    "role": {"value": "binding", "src": {"file": "tools/labviz/gates.json", "path": ".roles.c10v_layerpick.B.A7_coined_coined"}},
    "seed": {"value": null, "missing": "C10V records one process; no seed field", "tier": "NOW-not-recorded"},
    "replicate": {"value": null, "missing": "no replicate field (replication was not triggered)", "tier": "NOW-not-recorded"},
    "decision_id": {"value": "D-C10v-layerpick", "src": {"file": "results/c10v_layerpick/pass1.json", "path": ".decision_id"}},
    "model": {"value": "Qwen/Qwen2.5-3B", "src": {"file": "results/c10v_layerpick/pass1.json", "path": ".model.id"}},
    "model_revision": {"value": "3aab1f1954e9cc14eb9509a215f9e5ca08227a9b", "src": {"file": "results/c10v_layerpick/pass1.json", "path": ".model.revision"}},
    "date": {"value": "2026-10-08T03:32:38.191318+00:00", "src": {"file": "results/c10v_layerpick/pass1.json", "path": ".when_utc"}},
    "reading_bound_to_record": {"value": "bf8f162a422cd01bf9763673cd24abbb99a532da889f08c3311174d7942a119f", "src": {"file": "results/c10v_layerpick/run.json", "path": ".pass_sha256.pass1"}}
  },
  "context": {
    "experiment": {"node_id": "exp:C10V-layerpick", "edge": "direct", "matched_by": "registry result path (longest folder prefix)",
                   "value": "C10V-layerpick", "src": {"file": "docs/EXPERIMENT_REGISTRY.md", "line": 60, "quote": "**C10V-layerpick**"}},
    "question": {"value": "does editing each fact at its own band layer (argmax of the lone-write coefficient G) raise held-out recall over the band, a fixed layer and a shuffled map? (step 4, H-8)",
                 "src": {"file": "docs/EXPERIMENT_REGISTRY.md", "line": 60, "quote": "does editing each fact at its own band layer (argmax of the lone-write coefficient G) raise held-out recall over the band, a fixed layer and a shuffled map? (step 4, H-8)"}},
    "status_now": {"value": "CLOSED NULL", "src": {"file": "docs/EXPERIMENT_REGISTRY.md", "line": 60, "quote": "CLOSED NULL D-C10v-layerpick ⟨D-C10v-layerpick@3bcae852⟩ (not advanced under the preregistered rules: B 12 vs A 11/72, B0 12, Bshuf 10; replication not triggered)"}},
    "track": {"node_id": "track:track_c", "edge": "direct", "value": "track_c", "src": {"file": "docs/EXPERIMENT_REGISTRY.md", "line": 60, "quote": "| track_c |"}},
    "decision": {"node_id": "dec:D-C10v-layerpick", "edge": "direct", "matched_by": "row anchor",
                 "value": "D-C10v-layerpick", "src": {"file": "docs/EXPERIMENT_REGISTRY.md", "line": 60, "quote": "⟨D-C10v-layerpick@3bcae852⟩"}},
    "corpus": {"node_id": "corpus:56", "edge": "direct", "value": "CORPUS/56", "src": {"file": "docs/EXPERIMENT_REGISTRY.md", "line": 60, "quote": "| CORPUS/56 |"}},
    "hypothesis": {"node_id": "hyp:J6:H-8", "edge": "direct", "value": "H-8", "src": {"file": "docs/EXPERIMENT_REGISTRY.md", "line": 60, "quote": "(step 4, H-8)"}},
    "spec_sections": [{"node_id": "spec:§8.9", "edge": "derived", "value": "§8.9",
                       "derived": "the experiment's decision (registry :60) is named in the overlay row of §8.9 L2",
                       "inputs": [{"value": "D-C10v-layerpick", "src": {"file": "docs/EXPERIMENT_REGISTRY.md", "line": 60, "quote": "⟨D-C10v-layerpick@3bcae852⟩"}},
                                  {"value": "D-C10v-layerpick", "src": {"file": "docs/SPEC_EXPERIMENT_OVERLAY.md", "line": 22, "quote": "D-C10v-layerpick"}},
                                  {"value": "§8.9", "src": {"file": "docs/SPEC_EXPERIMENT_OVERLAY.md", "line": 22, "quote": "**§8.9 L2 — multi-token CORE values (C10 chain)**"}}],
                       "rule_src": {"spec": "§11.2 run → context rule"}}],
    "condition": {"node_id": "cond:C10", "edge": "derived", "value": "C10",
                  "derived": "the F1 condition whose row names the experiment's spec section (chain: registry :60 → overlay :22 → F1 :71)",
                  "inputs": [{"value": "D-C10v-layerpick", "src": {"file": "docs/EXPERIMENT_REGISTRY.md", "line": 60, "quote": "⟨D-C10v-layerpick@3bcae852⟩"}},
                             {"value": "D-C10v-layerpick", "src": {"file": "docs/SPEC_EXPERIMENT_OVERLAY.md", "line": 22, "quote": "D-C10v-layerpick"}},
                             {"value": "§8.9", "src": {"file": "docs/SPEC_EXPERIMENT_OVERLAY.md", "line": 22, "quote": "**§8.9 L2 — multi-token CORE values (C10 chain)**"}},
                             {"value": "§8.9", "src": {"file": "docs/F1_DETERMINATION.md", "line": 71, "quote": "| **C10** | **Multi-token value robustness** (G7; the §8.9 store"}}],
                  "rule_src": {"spec": "§11.2 run → context rule"}},
    "layer": {"node_id": "layer:write-engine", "edge": "derived", "value": "Write Engine",
              "derived": "the experiment's spec section §8.9 is a §8.x section, and §8 is the Write Engine layer (chain: registry :60 → overlay :22 → e2e :14)",
              "inputs": [{"value": "D-C10v-layerpick", "src": {"file": "docs/EXPERIMENT_REGISTRY.md", "line": 60, "quote": "⟨D-C10v-layerpick@3bcae852⟩"}},
                         {"value": "D-C10v-layerpick", "src": {"file": "docs/SPEC_EXPERIMENT_OVERLAY.md", "line": 22, "quote": "D-C10v-layerpick"}},
                         {"value": "§8.9", "src": {"file": "docs/SPEC_EXPERIMENT_OVERLAY.md", "line": 22, "quote": "**§8.9 L2 — multi-token CORE values (C10 chain)**"}},
                         {"value": "Write Engine", "src": {"file": "docs/SPEC_E2E_GROUND_TRUTH.md", "line": 14, "quote": "| **Write Engine** (§8) |"}}],
              "rule_src": {"spec": "§11.1 e2e layers"}},
    "era": {"node_id": "era:c10", "edge": "curated", "value": "c10", "src": {"file": "tools/labviz/contexts.json", "path": ".experiments[\"C10V-layerpick\"].era"}},
    "measure": {"value": "complete answers to 72 reworded questions; goal 61", "src": {"file": "tools/labviz/contexts.json", "path": ".eras.c10.measure"}}
  },
  "headline": {
    "hits": {"value": 12, "src": {"file": "results/c10v_layerpick/pass1.json", "path": ".recipes.B.arms.A7_coined_coined.para_full_n"}},
    "out_of": {"value": 72, "src": {"file": "results/c10v_layerpick/pass1.json", "path": ".recipes.B.arms.A7_coined_coined.para_n"}},
    "count_used_by_label": {"value": 12, "src": {"file": "results/c10v_layerpick/run.json", "path": ".readings.B.binding"}},
    "program_goal": {"value": 61, "src": {"file": "docs/c10_scoreboard.json", "path": ".goal"}},
    "prereg_bars": [{"value": "LEAD", "src": {"file": "docs/C10V_LAYERPICK_PREREG.md", "line": 69, "quote": "**LEAD** if B's count ≥ 30/72 and every locality gate holds."}}]
  },
  "label": {"value": "NULL", "src": {"file": "results/c10v_layerpick/run.json", "path": ".readings.B.label"},
            "base": {"value": "NULL", "src": {"file": "results/c10v_layerpick/run.json", "path": ".readings.B.base_label"}},
            "colour_class": "null", "colour_table": "tools/labviz/labels.json"},
  "gates": [
    {"name": "engine fingerprint", "judgement": "recorded", "passed": {"value": true, "src": {"file": "results/c10v_layerpick/pass1.json", "path": ".fingerprint.ok"}}},
    {"name": "LAW#5 inertness", "judgement": "recorded", "passed": {"value": true, "src": {"file": "results/c10v_layerpick/pass1.json", "path": ".law5.ok"}}},
    {"name": "described_as", "plain": "Description of the made-up places stayed similar", "judgement": "recorded",
     "observed": {"value": 86.17, "src": {"file": "results/c10v_layerpick/pass1.json", "path": ".recipes.B.arms.A7_coined_coined.locality_described_as"}},
     "reference_line": {"value": 87.0, "derived": "reference value − 3", "comparison": "≥",
                        "inputs": [{"value": 90.0, "src": {"file": "results/c10v_layerpick/pass1.json", "path": ".recipes.A.arms.A7_coined_coined.locality_described_as"}}],
                        "rule_src": {"file": "docs/C10V_LAYERPICK_PREREG.md", "line": 74, "quote": "`described_as` ≥ A − 3"}},
     "passed": {"value": false, "src": {"file": "results/c10v_layerpick/run.json", "path": ".readings.B.locality_gates.described_as"}}}
  ],
  "per_fact": [
    {"index": 0, "hit_kind": "free answer",
     "subject": {"value": "Zorbland", "src": {"file": "results/c10v_layerpick/pass1.json", "path": ".recipes.B.detail.A7_coined_coined[0].subj"}},
     "answer": {"value": "Vindex Vask", "src": {"file": "results/c10v_layerpick/pass1.json", "path": ".recipes.B.detail.A7_coined_coined[0].val"}},
     "answer_pieces": {"value": 4, "src": {"file": "results/c10v_layerpick/pass1.json", "path": ".recipes.B.detail.A7_coined_coined[0].ntok"}},
     "rewordings_hit": {"value": [true, true, true], "src": {"file": "results/c10v_layerpick/pass1.json", "path": ".recipes.B.detail.A7_coined_coined[0].para_full_hits"}},
     "canonical_hit": {"value": true, "src": {"file": "results/c10v_layerpick/pass1.json", "path": ".recipes.B.detail.A7_coined_coined[0].canon_full"}},
     "assigned_layer": {"value": 6, "src": {"file": "results/c10v_layerpick/pass1.json", "path": ".recipes.B.map.Zorbland"}},
     "selection_margin": {"value": 0.01560226080429905, "src": {"file": "results/c10v_layerpick/step0.json", "path": ".winning_margins[0][0]"}},
     "generated_text": {"value": null, "missing": "not recorded by this family", "tier": "REPLAY"}}
  ],
  "per_layer": [
    {"layer": 8, "unit": "absolute write size (Frobenius norm of ΔW)",
     "configured": {"value": true, "derived": "this card's layer is in the recipe's band",
                    "inputs": [{"value": [4, 5, 6, 7, 8], "src": {"file": "results/c10v_layerpick/pass1.json", "path": ".recipes.B.band"}},
                               {"value": 8, "structural": "per_layer[0].layer"}],
                    "rule_src": {"spec": "§5 item 4"}},
     "write_size": {"value": 16.31455421447754, "src": {"file": "results/c10v_layerpick/pass1.json", "path": ".recipes.B.delta_norms.A7_coined_coined[\"8\"].delta_norm"}},
     "written": {"value": true, "derived": "a write size is recorded for this layer",
                 "inputs": [{"value": 16.31455421447754, "src": {"file": "results/c10v_layerpick/pass1.json", "path": ".recipes.B.delta_norms.A7_coined_coined[\"8\"].delta_norm"}}],
                 "rule_src": {"spec": "§5 item 4"}},
     "relative_write_size": {"value": 0.13654435355029926, "src": {"file": "results/c10v_layerpick/pass1.json", "path": ".recipes.B.delta_norms.A7_coined_coined[\"8\"].relative_delta_norm"}},
     "facts_assigned": {"value": 2, "src": {"file": "results/c10v_layerpick/run.json", "path": ".readings.B.by_layer[\"8\"].facts"}},
     "lens": {"value": null, "missing": "no logit lens recorded for any past run", "tier": "REPLAY"}}
  ],
  "scale": {"unit": "absolute write size (Frobenius norm of ΔW)",
            "max": {"value": 113.7967300415039, "derived": "maximum of the eligible population (§5 item 4): every applied delta_norm under delta_norms in a RECORDED card",
                    "population": {"file": "results/labviz/site/cards/scales.json", "path": ".absolute_write_size.operands"},
                    "rule_src": {"spec": "§5 item 4"}}},
  "parts": {"written_module": {"value": "model.layers.{}.mlp.down_proj", "src": {"file": "configs/hparams/qwen25_3b_memit_hparams.json", "path": ".rewrite_module_tmp"}},
            "hparams_bound": {"value": "4225cc6aabc3eb9fa62d2bb2cac68b1238de3a39c5e469da635e6e1464aa3bb4", "src": {"file": "results/c10v_layerpick/pass1.json", "path": ".identity.source_sha256[\"configs/hparams/qwen25_3b_memit_hparams.json\"]"}},
            "untouched_basis": {"value": "by design (the engine writes only down_proj)", "src": {"file": "tools/labviz/gates.json", "path": ".untouched_basis.memit"}},
            "structure": {"layers": {"value": 36, "src": {"file": "hf_cache/hub/models--Qwen--Qwen2.5-3B/snapshots/3aab1f1954e9cc14eb9509a215f9e5ca08227a9b/config.json", "path": ".num_hidden_layers"}}}},
  "stimulus": {"canonical": {"value": "The capital of {} is the city of", "src": {"file": "tools/labviz/stimulus.json", "path": ".c10_harness.entries[0].text"}},
               "precedence": {"value": "SHA-bound transcription", "src": {"file": "tools/labviz/stimulus.json", "path": ".c10_harness.tier"}},
               "bound_by": {"value": "1f6be5811d7e58f3ebda16867a4a174b1cf24d47f9a2514cf9c3f9d29f18e695", "src": {"file": "results/c10v_layerpick/pass1.json", "path": ".identity.source_sha256[\"experiments/track_c/c10e_bandknob.py\"]"}},
               "keyed_position": {"value": "subject_last", "src": {"file": "configs/hparams/qwen25_3b_memit_hparams.json", "path": ".fact_token"}},
               "keyed_piece_text": {"value": null, "missing": "token text not recorded; Lab View loads no tokenizer", "tier": "Phase 2a extract"}},
  "plain_words": {"entry": {"value": "evaluation-14", "src": {"file": "docs/c10_evaluations.json", "path": ".entries[14].id"}},
                  "linked_by": {"value": "CORPUS/56", "src": {"file": "tools/labviz/links.json", "path": ".[\"results/c10v_layerpick/\"]"}}},
  "observations": {"telemetry": null, "replays": [], "sandbox": []},
  "reader_rules": [
    "Reason only from leaves; never from colours, bar lengths or glow.",
    "A derived leaf is Lab View arithmetic over recorded inputs; check its inputs. A derived reference line is never a verdict.",
    "A gate is judged only where a recorded boolean exists for this exact configuration (judgement: recorded).",
    "The goal and the label apply only to binding cards; identity.role says what this card is.",
    "Anything under observations.replays is NOT EVIDENCE and anything under observations.sandbox is EXPLORATORY; neither supports a verdict or enters headline, label, gates or scale.",
    "A count is a result only together with its label and gates; a null label = not judged yet."
  ]
}
```

- **Cards per run:** one per existing card id; summary-only cards carry `identity`, `label` and `plain_words` only.
- **Size:** ≈ 30–60 KB per full C10 card, ≈ 1,500 cards in total (1,503 v1 cards at 2026-10-08), of which most are small.
- **Where:** `results/labviz/site/cards/<card-id>.json`, `results/labviz/site/cards/index.json`, and the shared `results/labviz/site/cards/scales.json` (items 4 and 10).
- **Validation (test):**
  - **JSON-source leaves:** resolved with a python implementation of exactly this jq-path grammar: a leading `.`, then any sequence of `.key` (key matches `[A-Za-z_][A-Za-z0-9_]*`), `["key"]` (any JSON string) and `[n]` (non-negative integer). No other jq syntax is allowed in a card. Equality is exact (JSON numbers compared as parsed). A cross-check runs the `jq` binary on at least 50 leaves covering every family and every grammar form, and the two must agree.
  - **Document-source leaves:** the quote occurs verbatim at the cited line; the value occurs in the quote.
  - **Derived leaves:** inputs are themselves valid leaves (structural operands resolve to the named key of the same card); the rule recomputes the value from them alone; every derived context edge carries its full chain. Fixtures that must fail: a derived leaf with an operand removed (e.g. `configured` without the card's layer), a context edge missing a link of its chain, and a card whose recorded write size exceeds its `scale.max` (the C10V B0·A2 layer-8 value `55.45940399169922` is above B0·A7's `55.42212677001953`, so a scale taken from one recipe's binding arm would already fail).
  - **Scale population:** `scales.json` lists, per unit, every operand as a JSON-source leaf, with its own `sources[]` hashes; its operand set equals the eligible population enumerated from the RECORDED cards, and the maximum recomputed from that list equals each card's `scale.max`. Must-fail fixtures: the example card itself with one population member removed (if it is the maximum), and a `scale.max` that differs from the list's maximum.
  - **Structure:** no bare value outside the whitelist; every cited file is in `sources[]` with its current SHA-256.

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
| **S** (always) | logit-lens top-5 (int32 id + fp16 p) · expected-piece prob + rank · main-line size · attention-output size and MLP-output size · their push toward the expected piece (dot with its output-table row) · per head: attention to the keyed subject piece (16 × fp16) and head output size (16 × fp16) · top-16 MLP inner units (id + value; a summary of 11,008, not every element) | ≈ 180 B | ≈ 6.5 KB |
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

**GPU time:** recorded anchors are C10V pass1 ≈ 38 min for 12 arms (`pass1_started.json:.when_utc` … `pass1.json:.when_utc`, 02:54 → 03:32 UTC; `pass1_started.json:.identity.created_utc` is 02:14, the identity record, not the start), C10W P1 eval 5,774 s (`eval.json:.wall_seconds`), and one C10W adapter 523 s (`train/A7_coined_coined_s0_r16.json:.wall_seconds`). The instrumentation overhead is UNMEASURED. The first replay measures it on one arm, and every later request to the operator quotes measured numbers.

### 7.5 Reproduction check and labelling
- **Compared per arm, from the replay's own scoring (pass R, settings as recorded):**
  - `para_full_n`, `canon_full_n`, and the binding count if present;
  - L1 flips, L3 agreement, `same_frame.flips`;
  - every fact's `para_full_hits`.

  Also reported but not gating: `delta_norm` per layer (relative difference) and described-as.
- **Outcomes:**
  - all counts and per-fact hits equal → `"reproduction": "RECORDED OUTCOMES MATCHED"`, shown as "re-creation; recorded outcomes matched". Never "replay of <run>": equal final counts do not show that the internal trajectory was the run's;
  - otherwise → `"APPROXIMATE RE-CREATION"`, with a mismatch table (`recorded` / `replayed` per field). It is never shown as the run: banner "This re-creation differs from the scored run in N places; it is an approximation."
  - the separate eager-attention pass (tier A, §7.3) reports its own answer counts under its own label ("attention pass"), never merged into the check above.
- **Training replays:** the 40 recorded loss points vs replayed (max relative difference reported); final `fit.correct` and eval counts compared as above.
- **Manifest** `replay.json` top level:
  - `"evidence_status": "NOT EVIDENCE — observation replay"`;
  - `source_card`, `source_record` (path + SHA-256), `authorization` (D-ID);
  - `environment` (torch, transformers, device, attention implementation), `observer_inertness`, `reproduction`;
  - `gpu_seconds` (measured), `tiers`, `frames_index`.
- **Lab View rules:**
  - every replay view, export and card entry carries NOT EVIDENCE;
  - run cards list replays only under `observations.replays[]`;
  - replay numbers never enter `headline`, `label`, `gates` or a RECORDED `scale`;
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
- **Banners:** "NOT EVIDENCE: re-creation" always, plus "recorded outcomes matched" or "APPROXIMATE RE-CREATION (N mismatches)".

### 7.7 Scheduling and record per replay
Under D-C10r-labviz-3 the program session schedules each replay itself, in a GPU-idle window, and never ahead of a science run. Before each replay it records a runbook §5.2 row in plain words, for example: "Re-create C10V recipe B (3 arms) with full recording: about X GPU-minutes and Y GB of disk; GPU otherwise idle." It appends the measured GPU time after the run. Anything outside that ruling still needs an operator yes: a replay that would delay a science run, or GPU time charged against an approved experiment budget.

---

## 8. Telemetry views (Phase 2)

- **Parser:** for `results/c10z_astra/**/telemetry/telemetry_p*.jsonl`, written against the driver's real key names once they exist. The first fixture is the (h′4) stub-proof file. It is the **only** way telemetry enters Lab View: the RECORDED reader skips every `telemetry/` folder (§9.1), and telemetry lines appear only under `observations.telemetry`.
- **Views:** per-round write sizes per carrier layer (round and cumulative), with the same shared scale as item 4 (unit: Frobenius norm of the patch); per-round target probability per question (row × fact × view); lens top-5 before and after each candidate write (item 7); the phase timeline (item d).
- **Labels:**
  - "TELEMETRY: recorded during the run, outside the scored records" on every telemetry view;
  - (h′2) description rule: if the attempt ended HALTED-BUDGET or HALTED-V11, or carries EXCEEDS-TTL, also "timing possibly affected by telemetry".
- **Watching a running attempt without python:** the gate blocks unknown python, so the live path must not start python during an armed stage. The built static site plus browser-side JSONL polling covers this:
  - the browser fetches the telemetry file every 30 s;
  - it is served by the already-exempt `http.server` command line, or a python-free server (`/usr/bin/ruby`, `/opt/homebrew/bin/node` exist);
  - the builder itself is not needed for this: `tools/labviz_serve.sh:13–19` already reruns it every 60 s while the server runs, during GPU stages too, so it stays within the §2.3 build budget and writes only changed files.

  Any new server command needs the program session to add it to the gate's exemption list first.
- **Phase 2a: tokenizer-only stimulus extract.** A CPU tool loads only `tokenizer.json` (no weights, no GPU), outside Lab View. It runs once, when no gate is armed and after an operator ruling on tokenizer use. It writes `results/labviz_stimulus/pieces.json`: subject pieces, the keyed last piece, and answer pieces, all with ids. This is cross-checked against the recorded `target_ids`, `minted_ids` and C10W `head_ids`/`modifier_ids`. Lab View then reads it like any other JSON.

## 9. Build order

| Phase | Contents | Depends on | Rough size |
|---|---|---|---|
| **1: AVAILABLE NOW** | **First, as the foundation (§4A, §11):** the §4A information architecture, type scale and progressive loading; the program context model (`contexts.json` plus a derived graph), the era-correct captions on every tab, the fixes from the §11.3 C10-framing audit, and the connections map with focus mode (e, f). **Then:** the §9.1 ingestion boundary; run cards with typed leaves, roles and joins plus the leaf verifier (10); label table and badge (1); per-fact strip and fact panel (2, a-recorded); side-effect gauge with `gates.json`, recorded booleans only (3); shared scale, written-only colour, printed numbers, selector default fix (4); compare view (5); captions through `links.json` (6); C10V layer map and margins (8); C10W training slider over recorded loss and step times (9); stimulus transcription with SHA binding (a); exploded layer and static wiring in 2D/3D with "untouched" basis (b, c); recorded-event timeline (d). **Done only after** the build meets the §2.3 budget and the program session's §4A.5 review passes every §4A.4 criterion. | Nothing new; Codex build only when no GPU coordinator is live. | ≈ 1,600–2,300 lines across build.py, render.py, app.js, model.js, index.html and new JSON tables (≈ 600–800 of them for §11); ≈ 40–50 new tests; one to two Codex sessions plus review |
| **2: telemetry and tokenizer extract** | 2a tokenizer extract (keyed and answer piece text); telemetry parser and views (7 for layers 4–8, 9 for C10Z rounds, d per round); python-free live polling. | C10Z driver implements telemetry; (h′3) INERT check (17–85 GPU-min, operator yes); a telemetry-on attempt; operator ruling on tokenizer use. | ≈ 400–700 lines plus tests |
| **3: replay tool and player** | `tools/replay/` (§7) and the Lab View player (§7.6); then 7, b-impact, c-flow and d-granular for past runs. | GPU-idle window scheduled by the program (§7.7); first replay measures overhead; LAW#4 read-source before authoring hooks. | Tool ≈ 1,000–1,500 lines; player ≈ 600–900 lines; per replay ≈ 0.3–1 GB disk; GPU time per pass ≈ the original run's time × an unmeasured factor |
| **4: sandbox (EXPLORATORY)** | `tools/sandbox/` (§12): quick single edits on a chosen fact, layers and strength, shown in the Lab View tower and fact panel. | Phase 3's observer hooks and inertness check (reused, not rewritten); the program's sign-off of open point 6; GPU-idle windows only, with the §12.4 admission rules. | Tool ≈ 600–900 lines; Lab View page ≈ 300–500 lines; minutes of GPU per try (UNMEASURED) |

### 9.1 Ingestion boundary (Phase 1, tested)

The RECORDED reader never ingests `results/replays/`, `results/sandbox/` or any folder named `telemetry/` (at any depth). Those files enter Lab View only through their own tier readers: the replay manifest reader (§7.5, NOT EVIDENCE), the sandbox reader (§12, EXPLORATORY) and the telemetry parser (§8, TELEMETRY), and only under `observations.replays[]`, `observations.sandbox[]` or `observations.telemetry`. A record anywhere whose `evidence_status` starts with "NOT EVIDENCE" or "EXPLORATORY" is likewise never a RECORDED card. Test: fixtures placed in each of these folders (and a mislabelled one under `results/`) produce no RECORDED card and no value in any `headline`, `label`, `gates` or `scale`.

## 10. Open points for review

1. **Label colour classes** (§5 item 1): **settled in v2.** The program session fixed the complete table of every recorded label string in §5 item 1 at this fold; Codex transcribes it exactly into `labels.json`, and a test binds the two. A label string that appears later renders grey until the program adds a row here.
2. **The `links.json` map** is maintained by the program session; Lab View only tests it.
3. **Phase 2a tokenizer use** needs an explicit ruling: the original brief forbade tokenizers inside Lab View, and this design keeps them outside it.
4. **Backlog** (from `/private/tmp/claude-501/labviz_3d_investigation.md` §3, not Phase 1): readers for `update_norm_ratio` (a ratio) and `dW_fro` (offline *predicted*). Both are different units, and `dW_fro` is not an applied write, so they need their own clearly labelled unit groups.
5. **Era framing captions** in `contexts.json` (§11.2) are curated text with machine-checked quotes. Codex may draft them (marked `"status": "DRAFT"`); the program session reviews the set before it is published, and the site shows DRAFT framing as "draft framing, not yet reviewed".
6. **Sandbox controls and question sets** (§12.2, §12.3): the control types, finite ranges, allowed layer combinations and order, the sandbox fact set and its questions and locality probes. The program session signs off before Phase 4 is built.

---

## 11. Program-wide context model and the "how it all connects" map

Operator, verbatim: "we don't want to just have the LabViz be about CQ10, we want all historical science to be read and visualized based on the specific work we were doing at the time. This needs to be built across all parts of the dashboard. And we want to be able to visualize how a particular focus of science connects to the rest and how all of it ties together."

**What happens today.** Choose Mistral-7B in the Runs model filter and the Models tab. Its panel says "Comparable C10 weight-write summary: not recorded" and "Comparable 72-question harness score: not recorded" (`index.html:36`). That judges a June model-family experiment by the October C10 yardstick. Every other tab does the same (§11.3).

### 11.1 Sources (all parseable without a model; read for this spec with `grep`/`sed`/`jq`)

| Source | What it gives | Parse notes (verified) |
|---|---|---|
| `docs/EXPERIMENT_REGISTRY.md` | **54 experiment rows** (`grep -c '^| \*\*'`): ID, track, the question (the "hypothesis" column), script, result path(s), CORPUS ref, status, decision | Column counts vary: 36 rows have 10 `|`-fields, 16 have 9 (the C10K…C10V rows, which have no decision column; their D-ID sits in the status cell), and one each has 11 and 12 (pipes inside text: C10 and R2). **Parse by regex over the whole row:** first cell = ID; second = track; D-IDs by the grammar `(^|[^A-Za-z0-9-])D-[A-Za-z0-9]+(-[A-Za-z0-9]+)*`, excluding the literal words `D-ID` and `D-IDs` (row 59 contains "D-ID"; a bare `D-…` regex also matches inside `ROUTING-BLOCKED-UNDERFIT` on row 58); `CORPUS/\d+`; backticked `results/…` paths, with brace expansion (§11.2). Test: 54 rows parsed. `docs/experiment_registry.json` is **stale**: 20 rows, dated 2026-10-04. Do not use it as the source. |
| `CORPUS/NN_*.md` (00–56) | Title (line 1), date, Decision-IDs, model names, artifact filenames (header lines), and an "E2e-map cell:" line where present (16 entries: 23 and 26–40) | Decision IDs appear in the bodies of several docs (`D-C10u-mint2` occurs in 53, 54 and 55), so links come from the **header** (first 12 lines), and a run → CORPUS link never comes from a decision ID alone. |
| `docs/SPEC_EXPERIMENT_OVERLAY.md` | Spec section (`§8.7`, `§8.9 L2` …) ↔ decision IDs, CORPUS refs and status (VALIDATED / AMENDED / PROTOTYPED / OPEN) | Markdown tables in sections A–E; regex for `§[\d.]+`, D-IDs and `CORPUS/\d+` per row |
| `docs/SPEC_E2E_GROUND_TRUTH.md` §B (`:10–18`) | The six layers and their spec sections: Schema §7 · Write Engine §8 · Validation §9 · Security §10 · State Consistency §11 · Orchestration §12. Also the cross-cutting areas §C write path, §E memory management, §F verification, §G read path, §I deployment | Spec section → layer by section number (§8.x → Write Engine …). The mapping table is curated once, with this line cited. |
| `docs/F1_DETERMINATION.md:62–71` | F1 conditions **C1–C10**, with title and spec sections | |
| `docs/HYPOTHESIS_REGISTER_2026-06-18.md` | Hypothesis rows: sections A–G use `A1…A9`, `D1…`, and J.6 (`:172–203`) uses `H-1…H-30` with a "sequence step" column | Registry questions name them: e.g. C10V "(step 4, H-8)", C10W "(step 5, H-13 …)", C10U "(step 3, H-19)", C10T "(step 2, H-10/H-5)", C10S "(step 1, H-1)". That gives an exact experiment → hypothesis edge. |
| `EVIDENCE_INDEX.md` | Ledger of the write-engine viability era: Gate A, Phase 0/1, s240–s244, tiers T1/T2 (2026-06-17) | Tables: script → result → headline |
| `EXPERIMENT_RUNBOOK.md` §8 (`:448–608`) and §5 (`:280–389`; 73 distinct D-IDs at 2026-10-08 under the §11.2 D-ID grammar, 93 with the bare regex, which also matches inside words such as `BLOCKED-UNDERFIT`) | Track titles: A "Cross-entity isolation fix", B "Scale / efficiency", C "Multi-token value robustness (G7)", D "Capacity-law / spec reconciliation", E "Deployment", F "Spec implementation-readiness". The decisions ledger. | |
| `docs/t_branch_decision_document_v1_{1..4}.md`, `docs/framework_findings/` (16 files at 2026-10-08), `docs/session_summaries/` (39 files) | The pre-June **model-family era** (T-branch, workstream WS1, sessions S2.x): the MEMIT ceiling on Llama-3.1-8B, Llama-3.2-3B and Mistral-7B; Qwen2.5-7B "CLEARED 5/5" (`t_branch_decision_document_v1_4.md:7`, `:35`, `:37`) | **No result files in `results/`.** `grep -rli mistral results/**/*.json` finds only research-pass and chat logs. This era gets documentary cards: question, decision, finding, models, with doc:line citations. No run pictures, no invented scores. |

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
| Track | `track:<registry track>`; runbook titles are shown beside, never merged by letter | `track:track_e`. Registry `track_e` = the read contract (R1, R1-bit, R11), but runbook "TRACK E" = Deployment (`:602`). |
| Hypothesis | `hyp:<register section>:<id>` | `hyp:A:A7`, `hyp:J6:H-8` |
| Experiment | `exp:<registry ID>` | `exp:A7`, `exp:C10V-layerpick` |
| Decision | `dec:<D-ID>` | `dec:D-C10v-layerpick` |
| CORPUS entry | `corpus:<NN>` | `corpus:56` |
| Run (card) | `run:<card id>` | |
| Model | `model:<name>` | `model:Mistral-7B` |

**Edges, typed.** A link means "documents connect these", never causation or support, and its tooltip says so. Every edge has one of three types, drawn differently on the map (solid, dashed, dotted) and named in the side panel:
- **direct**: one document line names both ends; the edge stores `{file, line}` and the quote for each end (e.g. registry `:60` names `C10V-layerpick` and `CORPUS/56`). Source lines usually name ends in their own words (`C10`, `§8.9`), not in node-ID form (`cond:C10`); the parser maps the words to node IDs by the per-source rules of §11.1, and the test checks the quoted words, not the node IDs.
- **curated**: from `contexts.json`, with a `{file, line, quote}` that supports it (e.g. `era:t-branch` for Mistral-7B).
- **derived**: a chain of direct or curated edges; the edge lists its inputs (e.g. experiment → `cond:C10` through its decision, the overlay row `:22` naming that decision and §8.9, and `F1_DETERMINATION.md:71` naming §8.9 under C10).

**Registry result paths.** A result-path cell may hold a file, a folder (ending `/`), or a brace expression. Expansion: `{a,b}` yields each alternative and `{,x}` includes the empty one, so `results/d20_subbatch_sweep_result{,_ord1,_ord2}.json` (`:25`) yields three files and `results/b1_{3b,7b}_dose_response_result.json` (`:19`) two; nested braces are refused by the parser (none occur). Text outside backticks, such as `(+`_seeds123`/`_seeds345`)` on `:19`, is not a path. A folder matches every record under it.

**Experiment → decision (explicit; never "the first D-ID").** For each registry row, in order:
1. the D-ID inside the row's anchor `⟨D-…@<sha>⟩`, if exactly one distinct D-ID is anchored (rows `:13`–`:20`, `:22`, `:38` and `:42`–`:60` have one at 2026-10-08);
2. else the row's only distinct D-ID (after the grammar of §11.1);
3. else **unknown**, listing the candidates; a row with none says "no decision recorded" (rows 7–12, CP1–G3).

So `C10U-mint2` (`:58`) → `D-C10u-mint2` (anchored), although `D-C10r-rulings-12` appears earlier in the same row.

**Run → context rule.** Applied in order; the first rule that yields exactly one experiment wins. A rule that yields two or more is a **tie**: the context is unknown and the card lists the candidates; nothing is chosen.
1. The record's repo-relative path is an expanded registry result path, or lies under one (longest folder prefix; two rows with equally long prefixes tie).
2. A CORPUS header (first 12 lines) names the record by its repo-relative path, or by a path suffix of at least two components; a bare basename that occurs in more than one results folder (`run.json`, `eval.json`) never matches. Header paths are expanded like registry paths, and a `*` matches within one path segment: `CORPUS/22_D1_CAPACITY_LAW.md:3` names `results/d1_predictor_map_result.json` and `results/d1_concentration_sweep_result*.json` (4 files at 2026-10-08). Only `results/…` paths count; `logs/d1_*` and `experiments/…` paths on the same line do not. A rule-2 match yields a **documentary context**, not an experiment: the CORPUS entry (direct edge to the header line) and the decision anchored in that header (`⟨D-…⟩`, exactly one, else unknown with candidates). It never reaches an experiment through a registry row that merely cites the CORPUS entry: registry `:19` (B1-size-term) cites "CORPUS/22 (B1 §)", and D1 records must not attach to `exp:B1-size-term`. The card's `experiment` is then a missing leaf "no registry row names this record", and its era comes from `contexts.json` `corpus_eras` (curated, with a quote) or reads "era not recorded". So the 5 named D1 records get `corpus:22`, `dec:D-D1-1` (`CORPUS/22_D1_CAPACITY_LAW.md:3`, `⟨D-D1-1db8d819⟩`) and a documentary card.
3. The record's `decision_id` equals the decision (chosen as above) of exactly one row. The card then says "attempt not named in the registry's result paths" when that row lists result paths and none contains the record (e.g. `results/c10u_mint2/r2/…`, the halted `results/c10w_oracle/step0_20261007T220253_584752Z/`, and C10W P2, whose `p2_…/` folder row `:59` does not list).
4. Otherwise the context is **"not recorded"**, and the card shows its candidates. Nothing defaults to C10.

**Fixtures (real rows):** `:19` (brace expression plus a non-path annotation), `:25` (empty brace alternative), `:58` (folder and file paths; anchored decision after `D-C10r-rulings-12`; `ROUTING-BLOCKED-UNDERFIT` must not yield a D-ID), `:59` (the literal "D-ID"; P2 records reach the row only by rule 3), `:60` (a brace expression in a review path); an ambiguous basename (`run.json`); a header glob (`CORPUS/22` matches the 4 `d1_concentration_sweep_result*.json` files, not `logs/d1_*`, and each resulting card carries `corpus:22`, `dec:D-D1-1`, no experiment and not `exp:B1-size-term`); an unmatched historical attempt (`c10u_mint2/r2/`); a two-row tie.

**Per-run `context` block in the run card** (§6). Each field is a typed leaf (direct and curated fields are document-source or JSON-source leaves; derived fields list their inputs), with `node_id` and `edge`:
- `experiment`, `track`, `decision`, `corpus`, `hypothesis`;
- `question`: the registry's question cell, verbatim;
- `condition`, `spec_sections`, `layer` (usually derived);
- **`status_now`**: the registry status cell, verbatim, shown as "status now (registry)". It is kept apart from the era framing below, which says what was asked and measured **at the time**; a page never mixes the two in one sentence;
- `era`, `measure`: from `contexts.json` (curated).

**Era framing (`tools/labviz/contexts.json`, curated).** For each era and each experiment line: the plain-words question, the headline measure, and the bar it was judged against, each with `{file, line, quote}`; and for each of the 54 registry rows, its one era (§3.10). A test asserts every quote occurs verbatim at its line. Where a result file holds the headline number, the entry names its jq path, and the test resolves it. Where none does, the entry says "no single headline number recorded; see the CORPUS entry". Codex may draft entries (`"status": "DRAFT"`); the program session reviews them before publication (open point 5). Examples:
- C10 measure: "complete answers to 72 reworded questions; goal 61" (`docs/c10_scoreboard.json:.out_of`, `.goal`);
- model-family era: the measure is the consistency check out of 5, quoted verbatim as "5/5 consistency PASS" (`docs/t_branch_decision_document_v1_4.md:35`), never paraphrased.

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
| `app.js:49`, `model.js:19` | Band colouring from the configured band (also item 4) | Written layers from the record |

### 11.4 The "how it all connects" map (home view)

- **Layout:** layered columns, left to right: spec layer → spec section → F1 condition → track / experiment → decision → CORPUS entry → model. Runs are counted on each experiment node and expand on demand. It is not a force-directed hairball: columns keep it readable, and nodes are sorted by date inside each column.
- **Focus mode:** tap any node, such as `cond:C10`, `exp:G6.1`, `model:Mistral-7B` or `spec:§8.7`.
  - Its upstream and downstream paths light up and the rest dims.
  - A side panel lists each link in plain words with its source line ("CORPUS/22 names D-B1-2 and §8.7").
  - A "shared with other lines" section lists nodes that the focused line shares with other lines: a spec section, a model or a decision. Example: C10 and the D1 capacity line both run through `layer:write-engine`, and through Qwen2.5-3B.
- **Presets:** each F1 condition C1–C10, each registry track, each era, plus "what is running now".
- **Search** across all node labels.
- **Phone:** a drill-down list, one column at a time, with a breadcrumb and a back button; focus mode becomes "show connections".
- **Must not imply:** that a link is evidence, that line thickness is importance, or that an absent link proves no relation (the documents may simply not name it). Legend text: "Solid line: one program document names both ends. Dashed: a curated link with its quote. Dotted: a chain of links. Tap a line to see the documents."
- **Size:** nodes ≈ 6 layers + ≈ 40 spec sections + 10 conditions + ≈ 15 tracks + ≈ 60 hypotheses + 54 experiments + ≈ 80 decisions (78 distinct D-IDs at 2026-10-08 across CORPUS, registry and overlay, under the §11.2 D-ID grammar) + 57 CORPUS entries + 11 models, i.e. ≈ 350 nodes. Runs (about 1,500) are aggregated.

### 11.5 Tests (added to the Phase 1 brief)

- 54 registry rows parsed. The 9-, 11- and 12-field rows are parsed correctly: C10V → `dec:D-C10v-layerpick` and `hyp:J6:H-8`; R2 keeps its D-ID.
- `exp:A7`, `hyp:A:A7` and the C10 arm `A7_coined_coined` are three distinct nodes. Registry `track_e` and runbook "TRACK E" are not merged.
- `results/c10u_mint2/r3/…` and `r3_read_after_replicateF.json` → `exp:C10U-mint2` through the registry path rule, even though `D-C10u-mint2` also occurs in CORPUS 53 and 55; `C10U-mint2`'s decision is `D-C10u-mint2` (anchored), not `D-C10r-rulings-12`.
- The §11.2 fixtures: brace expansion (`:19`, `:25`, `:60`), the literal "D-ID" (`:59`), no D-ID from `ROUTING-BLOCKED-UNDERFIT` (`:58`), an ambiguous basename (`run.json`), an unmatched attempt (`c10u_mint2/r2/`, flagged "attempt not named in the registry's result paths"), and a two-row tie (unknown, with candidates).
- A run whose source matches no rule shows "context not recorded" with its candidates.
- In the content region (`data-region="content"`), the rendered Mistral-7B page, a G6.1 run page and a D1 capacity-law page contain none of the §4A.4 forbidden words: "of 72", "goal 61", "reworded", "made-up", "C10".
- Every one of the 54 registry rows has exactly one era in `contexts.json`.
- Every `contexts.json` quote occurs verbatim at its cited line. Every direct edge cites, for each end, a line and a quote that contains that end's words; every curated edge has a quote; every derived edge lists inputs that are themselves valid edges.
- The map's focus on `cond:C10` reaches `spec:§8.9` (through `F1_DETERMINATION.md:71`). Through the overlay row "§8.9 L2 — multi-token CORE values (C10 chain)", it reaches every decision that row names and those decisions' experiments and CORPUS entries. The test derives the expected set from the files; it is not hard-coded.
- The model-family era: `model:Mistral-7B` links to `era:t-branch` through `t_branch_decision_document_v1_4.md`, and its page shows documentary cards only.

---

## 12. Phase 4: the sandbox (EXPLORATORY, never evidence; spec only, nothing is built before the open-point-6 sign-off)

Operator, 2026-10-07 ~23:28: "a visual and interactive way to experiment on the model in the visualizer to try concepts and solutions as ideation for solving a block ... before running a full long experiment". Scope ruling: D-C10r-labviz-3 (`EXPERIMENT_RUNBOOK.md:373`).

The sandbox lets the operator try one quick edit and see what it did, in minutes, before anyone writes a prereg. It loads the model, so it is a GPU tool like the replay tool (§7), not part of Lab View. Its results are ideas. Each one is labelled EXPLORATORY. None of them supports a verdict, enters CORPUS, a ledger or the scoreboard, counts toward any experiment's score, or enters a RECORDED card's `headline`, `label`, `gates` or `scale`.

### 12.1 How a try works

1. The operator opens the **Sandbox** page in Lab View (a sub-page of "Inside the model") and chooses:
   - facts from the **sandbox fact set** (§12.3), never the 24 C10 facts;
   - the layers to write, from those with a covariance cache on disk: today `model.layers.4`–`12` `mlp.down_proj` (`covariance_caches/Qwen_Qwen2.5-3B/wikipedia_stats/`, nine files). Any other layer is refused, because a new cache costs hours of GPU; the allowed layer combinations and their order are part of the signed-off control list;
   - the strength and solver settings, from the signed-off list in §12.2.
2. The page sends the request, with the session token, to the sandbox server: a separate local process on its own port, bound to `127.0.0.1` and the Mac's Tailscale interface only (never `0.0.0.0`). Lab View's 8765 server and its command line are unchanged.
3. The server runs the try through a **dedicated sandbox evaluator** (`tools/sandbox/`), which writes with the unmodified engine and scores only the sandbox question set and the sandbox locality probes. **The production scoring path is forbidden**: the sandbox never calls the harness's `eval_arm` (`experiments/track_c/c10e_bandknob.py:358`, called at `:491`), which evaluates `PTEST` (`:363–365`), nor any driver's scoring entry point.
4. It restores the pristine weights and verifies the restore (§12.4). A failed restore discards the worker and writes a diagnostic.
5. The page shows the result in the same pictures as a recorded run: per-fact strip, write bars, side-effect values, and the tower. Every view carries the banner "EXPLORATORY: a quick try, not evidence". Its side-effect rows show **values only, never ✓/✗**: no same-process reference arm exists, so no gate can be judged.
6. A try that looks promising becomes a preregistered experiment through the normal path. The prereg may say "motivated by sandbox tries `<ids>`", and must cite **every** try of that session (the record of all tries, §12.4), not only the promising one. That is all the support the tries give, and a later prereg does not undo the adaptive exposure: the prereg states which sandbox facts, probes and settings were tried.

### 12.2 Controls (needs program sign-off, open point 6 in §10)

The candidates are the hparams the engine already reads (`configs/hparams/qwen25_3b_memit_hparams.json`): `layers`, `clamp_norm_factor` (0.75), `mom2_update_weight` (5000), `v_num_grad_steps` (25), `v_lr` (0.5), `kl_factor` (0.0625) and `v_weight_decay` (0.5). The sign-off fixes, for each control: its type, a finite allowed range, and for `layers` the allowed combinations and order. Values outside are refused, not clipped. **No setting that changes the covariance cache's identity is a control**: `mom2_n_samples` (100000), `mom2_dtype` (`float32`) and `mom2_dataset` (`wikipedia`) are fixed. The sandbox changes values, never code: the engine, the harness and the drivers stay byte-identical (LAW#5), and every try records the engine fingerprint, the hparams it used and the covariance cache files' identities.

### 12.3 The held-out test stays held out

The C10 score is measured on three held-out rewordings (`c10e_bandknob.py:52–56`) of 24 made-up facts, with the L1, L3 and described-as probes as its side-effect instruments. Tuning ideas against any of these would make the next preregistered run measure something it has already been tuned on. So:

- **A separate fact set.** The sandbox uses its own made-up facts, disjoint from the 24 C10 subjects and their answers (`c10e_bandknob.py:57–61`, `detail.<arm>[].val`), and from the fictional bystanders of the C10W frames. They live in `tools/sandbox/facts.json`.
- **Separate questions.** Its questions share no template with the scored three, with the canonical question, or with the C10W sealed phrasings (`seal_audit.json`, all 22 rows; `T01` is the canonical question). They also pass the C10W seal audit's banned-bigram and banned-word lists (`seal_audit.json:.banned_bigrams`, `.banned_words`) against the held-out three. Near-duplicate phrasings are reviewed by hand at sign-off, not left to string tests.
- **Separate side-effect probes**, disjoint from the scored L1 countries, the L3 generic sentences and the described-as prompts (`c10e_bandknob.py:277–300`, `:475`).
- **Tests check what actually reaches the model**, not template strings: every prompt that reaches generation, teacher forcing, the observers and the logs during a try is captured and checked against the held-out set, the C10 facts and the scored probes.
- The fact set, questions and probes are written once, reviewed at sign-off, and hashed; each try records those hashes.

### 12.4 Scheduling, admission and restore

- **Never alongside science.** The server never runs while any GPU coordinator or armed chain exists. The program session stops it before launching any GPU stage or arming a chain. It refuses to start if a coordinator or armed chain exists (same inventory rule as `tools/c10w_p2_gate.py:43–54`, plus a lock file shared with the coordinators), and it re-checks before **every** try (request-time admission), not only at startup. Reason: a running sandbox is an unknown python to the stage gates, and a gate refusal exits 3 (`tools/run_c10w_p2_stage.sh:16`), which would halt an unattended chain.
- **Bounded.** One try at a time, queued; a per-try runtime cap stops an active try (and restores, below); the queue is cancelled if a science stage needs the GPU; the server exits after 10 minutes without a request.
- **Restore, verified every time** (including after a timeout or an exception): before the first try, every parameter and buffer of the freshly loaded model is hashed; that set is the session's pristine identity. (C10W's recorded `frozen_parameter_hashes_before` are not a direct reference: they hash the float32 upcast the trainer uses, `train/*.json:.dtype` = "float32", `c10w_oracle_train.py:168`, while the MEMIT path runs float16. Whether to reproduce that hashing as a cross-check is part of the open-point-6 sign-off.) After each try's restore, every parameter and buffer is hashed again and must match; forward hooks are removed, caches cleared, the RNG reseeded and `eval()` mode set, and the pristine probe re-run with `torch.equal` logits. Any mismatch discards the worker and reloads the model before the next try.
- **Records:** `results/sandbox/<UTC>/try_<n>.json` for **every** try, including refused, timed-out and failed ones, with:
  - `"evidence_status": "EXPLORATORY: sandbox try, not evidence"`;
  - the request, the hparams used, the engine fingerprint and the fact-set, question-set and probe hashes;
  - the pristine and post-restore hashes;
  - the scores in the run-card leaf format (§6);
  - `gpu_seconds`.

  Lab View reads these only through the sandbox reader (§9.1): under `observations.sandbox[]` and on the Sandbox page, never in `headline`, `label`, `gates` or `scale`.
- **Observers:** the lens and part views reuse the Phase 3 hooks and their inertness check (§7.2 item 5). They are not reimplemented.
- **Tests (Phase 4):** timeout, exception mid-try, concurrent launch attempt, request while a coordinator is live, an out-of-range or out-of-scope setting, and a deliberately unrestored tensor must each end in a refusal or a discarded worker, never in a scored try.
- **Cost:** UNMEASURED. As an anchor, C10V pass1 wrote and scored 12 arms in about 38 minutes, so roughly 3 minutes per arm of 24 facts, plus a one-time model load. The first sandbox session measures both, and the program records them.

### 12.5 Not in Phase 4

- typed-in facts that are not in the signed-off sandbox fact set (needs its own question-set and locality design);
- training-based edits (LoRA): the sandbox does MEMIT edits only;
- chaining several tries onto one model state: every try starts from the pristine weights.
