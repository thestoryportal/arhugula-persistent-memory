# Pre-registration — D-C10z-astra: a forward-only joint output-margin solve (ASTRA) written into selected `W_down` columns, against the closed-form band write, on the C10 harness (queue row 5b) (v1, 2026-10-07)

**Status: v1 DRAFT — for advisor + Codex review; not frozen.** Nothing has run; no code written. Decision-ID `D-C10z-astra`. Queue row 5b of `docs/INTEGRATED_QUEUE_2026-10-07.md:23` ("candidate … Prereg after step 7's review; it may replace step 7 if the reviews judge DOW-KE's per-patch optimisation outside the write-only ruling"). Step 7's advisor review did so judge (`results/c10y_directdw_advisor_v1.md`, Scope A; recorded at `EXPERIMENT_RUNBOOK.md:343` item (2)). Building is model-free and may start after the reviews; running needs the operator's go (§6, decisions 0–2), one GPU job at a time (D-C10r-rulings-4 (1), `EXPERIMENT_RUNBOOK.md:331`).

Source lead: scout note `results/scout_2026-10-07_realisation_wall.md:11–19`. Paper: ASTRA, Gu, Zhang, Chen, Aleti, "Mind the Gaps: From Failure Attribution to Closed-Form Repair of Code Language Models", arXiv 2610.05277 v1, read 2026-10-07 through the arXiv MCP (LaTeX source and HTML text): §3.1 Preliminaries, §3.2 Locating Failing Tokens, §3.3 Targeting Carrier Neurons, §3.4 Tailoring Joint Patches (Algorithm 1), §3.5 Re-linearizing the Repaired Model, §4 "Configuration" paragraph, §4.2 (layer placement), §4.3 (ablation table, timing), §4.4 (side effects, unseen phrasing), §5 Discussion. **Section numbers are the paper's own** (its HTML prints "3.5. Re-linearizing the Repaired Model"). The queue row and the scout cite the ablation as "§5.3"; that is the arXiv MCP outline's numbering, which counts the abstract as section 1. The same paragraph is the paper's §4.3. No public code was found (scout `:16`); the writer is built from Algorithm 1 as a harness-side driver. Lineage: CORPUS/44 ⟨D-C10l-covgeom@af2e38f7⟩ (envelope `:39`, ρ correction `:43`), CORPUS/36 (C10 signature, `:28`), CORPUS/53 ⟨D-C10t-secondkey@76a722d3⟩ (in-harness residual `:62`; prefix-spillover gates), `docs/C10T_SECONDKEY_PREREG.md:48–49, :69, :71` (the F1 per-prefix and subject-free probes reused here). Rulings in force: D-C10k-rulings-1 (strict held-out bar), D-C10k-rulings-2 (Qwen anchor), D-C10r-rulings-3 (2) (write-only, quoted in §0), D-C10r-rulings-4 (1) and (3) (one GPU run at a time; steps 6–7 demoted, `EXPERIMENT_RUNBOOK.md:331`), D-C10r-rulings-9 (`:342`). Conventions follow `docs/C10Y_DIRECTDW_PREREG.md` (v1) with the step-6 and step-7 advisor findings applied (`results/c10x_enginepath_advisor_v1.md`, `results/c10y_directdw_advisor_v1.md`). Every repo statement cites a line read on 2026-10-07 (LAW#4) or is marked UNVERIFIED.

**Binding rules, quoted (CLAUDE.md).** LAW#3: "When re-running a previously-characterized arm, the reproduction MUST land near the known values BEFORE any new data is trusted or any new arm is run." LAW#4: "Before writing any cell that depends on engine internals, `cat -n` the relevant engine source and author from what it actually does." LAW#5: "Any source change to the science-bearing edit path … must be isolated against a known-ceiling reference result and proven inert (LAW#5) before any verdict produced under it is promoted. Demonstrate inertness; do not assume it. The MEMIT engine, LARQL, and git stay **UNMODIFIED**." The writer below is a new harness-side solve in a new driver file. It calls no engine edit function, reads the model's own weights, and changes nothing under `memit_dry_run/memit` or in `experiments/track_c/c10e_bandknob.py`.

### Requirement map (the nine hard requirements of the brief → where each is met)

| # | requirement | where |
|---|---|---|
| 1 | LAW#3 baseline reproduction runs and is read before any candidate arm; a miss halts | §2.6 stage 0 steps 3–4; §3 V4; §5 |
| 2 | LAW#5 reduction that exercises the new code path, with an fp16/MPS-calibrated tolerance | §2.8 checks Z0–Z6 (Z3 = reduction to the unedited model through the full solve-and-write path; Z0 calibrates τ) |
| 3 | pristine model pinned by a weight-snapshot hash | §2.6 stage 0 step 1; §2.8 Z6; §3 V3 |
| 4 | complete, non-overlapping truth table with boundary values | §3.3 table T and §3.6 worked rows |
| 5 | underfit gate: solve objective not met → UNDERFIT, never NULL | §3.2 fit rule; §3.3 rule U |
| 6 | cheap early-kill stage (≈ 1–2 h) with a stated threshold | §2.6 stage 1; kill rule K1 in §3.4; cost §2.11 |
| 7 | engine and `c10e_bandknob.py` unmodified; solver in a new driver | §2.1 last bullet; §2.6; §3 V1 |
| 8 | M3 Pro 48 GB, MPS, fp16, no float64 on MPS, no CUDA; 34 min / 23 min measured costs | §2.4 precision row; §2.10; §2.11 |
| 9 | ρ_c stated as the remaining residual; `compute_z` scores every target token, the weight solve lacks value-position keys | §0 "Two facts stated correctly" |

## 0. Where this sits, and what it is

**The e2e map (`docs/SPEC_E2E_GROUND_TRUTH.md` §C, `:22–30`).** Write layer, steps 5–6 of the §C flow: the Commit Executor's compile of the `.larql` patch into an overlay, ending in the `COMMITTED` ledger entry "with overlay hash" (`:30`; spec `:671`). The arm replaces the whole compile step for one batch: a different solver, a different write site (selected columns of `W_down` in the layers the solver picks, not layers 4–8), and a different objective (output-logit margins at every value position, not a hidden-state target at the subject's last token). Read against the **§8.9 L2 behavioural bar** (e2e §F, `:64–65`). Shape: **Genesis-shaped**, one batch of 24 facts (e2e §D, `:32–34`); the Incremental shape is not tested. Lifecycle cells touched by implication and not tested: compaction re-runs the writer over all active patches (e2e §E, `:54`), so regeneration from the patch and the solve's growth with the fact count are spec-fit readouts (§2.7); the Write Lock's 60-minute TTL (spec `:783`) and the 2 h incremental PREPARED default (spec `:678`) bound the write's wall-clock. Read, governance and deployment layers are not touched. **§0.3 / queue:** row 5b, candidate replacement for step 7.

**Two facts stated correctly (earlier drafts had both backwards).**
- *ρ_c is a remaining residual.* `rho_c_band = ‖z − cur_after‖ / ‖z − cur_before‖` (`experiments/track_c/c10l_covgeom_step0.py:134`, as cited at `CORPUS/44_C10L_COVGEOM_SPARSEBAND.md:43`). Step 0's 0.028 means about 2.8 % of the canonical residual norm *remains unrealised* at the keyed position after the band write. About 23 % remains on the paraphrase prompts (ρ_p 0.232, `CORPUS/44:25`, correction `:43`). The in-harness values are 0.0327 canonical and 0.234 held-out (`CORPUS/53_C10T_SECONDKEY.md:62`). It is not "3 % lands". The scout note still carries the reversed phrase ("a single-key shortfall (3 % realised)", `results/scout_2026-10-07_realisation_wall.md:33`); that wording is withdrawn here, as at `docs/INTEGRATED_QUEUE_2026-10-07.md:38`.
- *`compute_z` scores every target token.* It places every target id at the end of each rewriting prompt (`memit_dry_run/memit/memit/compute_z.py:60–65`) and averages the NLL over all of them (`:141–150`); z reaches 0.99 (CORPUS/36:28, as cited at `INTEGRATED_QUEUE:39`). What has no objective at the value positions is the **weight solve**: its keys are read at the subject's last token only (`memit_dry_run/memit/memit/compute_ks.py:19–37`, `fact_token = subject_last`, hparams `configs/hparams/qwen25_3b_memit_hparams.json:5`; harness `experiments/track_c/c10e_bandknob.py:196`).

**Why ASTRA is aimed at the wall.** The wall, stated on that corrected reading: the band write realises the target at the keyed position on the canonical prompt (≈ 3 % remaining) but the value does not come out on held-out phrasings or at later value positions (A7 `para_full` 13/72 against 49/72 under injection, `CORPUS/44:23`). ASTRA's write *is* the missing per-position solve. It puts one linear requirement on the weights at every value-predicting position of every view ("one requirement per failing token", §3.4). The key of each requirement is the carrier's activation at that position, not at the subject. All requirements are solved together, because "the failing tokens of a sample share their carriers, so the correction of one token moves the leads of the others" (§4.3). Its ablations are the two numbers that motivate the arm (§4.3, Table "Ablation"): replacing the joint solve by a token-by-token solve costs 34.2 Pass@1 points pooled; a margin of 1 logit instead of 5 costs 31.4, because "a lead of one logit does not survive" the change from teacher-forced views to free generation from another prompt.

**Is ASTRA a write under the operator's ruling? Argued here; the operator rules (§6 decision 1).**

The ruling, quoted (`EXPERIMENT_RUNBOOK.md:330`, D-C10r-rulings-3 (2)): "Write-only ruling, the operator's words: training per commit defeats the spec's objective; likelihood of deploying it is essentially zero; run it only as a measurement — H-13/H-15 are an oracle measurement, not a route; H-18 demoted." The criterion it rests on (`results/research_pass_2026-10-06/recommended_sequence.md:13`): "The write must stay a per-commit solve that can be regenerated from the committed patch. Anything that needs a training set or a training loop per commit is out as a route (it breaks real-time use, the audit trail and compaction)."

1. *No training set.* The writer's inputs are the patch (24 subject/value requests in the CANON frame) and fixed artefacts: the model revision, the frozen context-template file, the null-space-weight statistics file and the output-metric file (§2.2, §2.12). Its six views per fact are exactly the strings `compute_z` already builds from the request: the identity template plus five engine-sampled prefixes (`compute_z.py:46–50`; `memit_dry_run/memit/memit/memit_main.py:304–323`). No paraphrase, no held-out template, no generated answer and no dataset row enters the solve. The reference text used for the null-space weights is a fixed statistic of the same kind as the engine's covariance cache (§2.2 item 5).
2. *No training loop.* Nothing is optimised by gradient. ASTRA "needs no optimizer, no step size and no backward pass" (§3.4); "each round needs one forward pass per view and one small linear solve, and no step needs a gradient" (§4.3). The up-to-ten rounds are re-linearisations: observe the deficits, solve one linear system exactly, write the solution, observe again (§3.5; Algorithm 1). That is an iterated closed-form solve, the shape of a Newton iteration, not descent on a loss. This is the line step 7's review drew. Step 7 "updates model weights … by gradient descent on an LM loss through layers 4–35", which is training (`results/c10y_directdw_advisor_v1.md`, Scope A). ASTRA is on the solve side of that line. For comparison only, not as the qualifying argument: the accepted engine itself runs up to 25 Adam steps per fact inside `compute_z` (`compute_z.py:104–172`; hparams `:6`). ASTRA has no gradient anywhere.
3. *Regenerable from the patch.* Every step is a forward pass at a fixed batch shape plus a float64 CPU solve. Same-shape fp16 forwards on this Mac have a measured run-to-run floor of 0.0 (`results/c10s_sharedz_halt_analysis_2026-10-06.md`, check (i)). Regeneration in a fresh process is therefore expected to be exact or near exact; it is measured, not assumed (§2.7, R1–R3).
4. *Real time and compaction are measured.* The paper reports 2.7 s per repair on a GPU (abstract; §4.3). Here, wall-clock per write is a readout against the 60-minute Write Lock TTL (W2, §3.5). Compaction would re-run the solve over all active patches. The linear system has one row per failing token, so it grows with the fact base: F² float64 entries, 0.8 GB at F = 10,000 and 10.4 GB at F = 36,000. That growth is reported, not tested (§4).

**Verdict proposed for the operator: a write candidate, not training.** On the ruling's own words it is a per-commit solve with no training set and no training loop, regenerable from the patch. Two qualifications go with it, and neither is a ruling issue. (a) It is **not the spec's designated engine**: §8.2 designates MEMIT and excludes "full fine-tuning" (spec `:311–313`). ASTRA replaces the D20 "orthogonal projection" (spec `:316`) with a diagonal null-space weight (§3.4) and has no "covariance balancer" (spec `:317`). Route adoption would need a §8.2 amendment. (b) Its write site is chosen per batch in the late layers (§4.2: never in the first 58 % of the depth; the last three layers in ≥ 97.0 % of repairs). Spec §8.2 places MEMIT in "middle-to-late FFN layers (L15–L25 for a 32-layer model)" (`:313`), about L17–L28 when scaled to 36 layers. Carriers outside that range are reported (§2.9); the harness band 4–8 is itself outside it. If the operator reads "a training loop per commit" to cover any iterated per-commit procedure, the arm runs as a measurement under the same design, and the labels in §3 are unchanged.

**Demotion status (§6 decision 0).** D-C10r-rulings-4 (3) demotes "Steps 6–7 (… H-3 direct ΔW)" behind steps 1–4 and the step-5 oracle, "their '3 % installed' motivation having been reversed by the CORPUS/44 correction" (`EXPERIMENT_RUNBOOK.md:331`). Row 5b is not named in it. Its motivation does not rest on the reversed premise: it rests on the missing value-position keys of the weight solve (above). Whether it inherits step 7's slot behind step 5 is the operator's call.

**What this experiment can and cannot conclude.** A pass advances one configuration: one view set, one margin, one carrier budget, one batch of N = 24, one model. A miss means *this configuration was not advanced*. It does not show that margin-constrained solves, late-layer writes or the model cannot hold the value.

## 1. Question and hypotheses

- **H-Z1 (the claim under test).** A joint output-margin solve, with one requirement per value position per view (μ = 5 logits) on the patch's own six views, written into SemCon-selected `W_down` columns and re-linearised for up to 10 rounds, raises A7 held-out full-sequence recall (`para_full_n` /72) to ≥ 19 and ≥ recipe A + 10 in the same process, at the locality of recipe A.
- **H-Z0 (null).** The count stays ≤ 18 or within 9 of recipe A.
- **H-Z2 (canonical fit, held-out miss: the C10 signature).** The solve meets its own objective on the six views (fit gate met; canon near 24/24), but held-out recall stays in the envelope. This is "fit the trained prompt … then fail paraphrase" (`CORPUS/36_C10_RESIDUAL_COINED_VALUES.md:28`). Its mechanism here would be that all six views share the CANON frame and differ only in a prefix (§2.2 item 2), while ASTRA's robustness to an unseen phrasing came from four *differently worded* views (§3.1, §4.4; one view instead of four cost 6.5 points, §4.3).
- **H-Z3 (spillover).** The count rises through frame- or prefix-conditioned completions that fire for subjects never edited. Read from the same-frame probe F0, the 24 per-prefix gates F1 and the subject-free probe (§2.9). This is the queue's named first risk: "carriers fire on the value's own context, so step-2-style prefix spillover is the first thing to gate" (`INTEGRATED_QUEUE:23`); step 2's write failed 10 of 24 such gates (`CORPUS/53:33`).
- **Expectation, stated now.** H-Z2 is the likeliest outcome, H-Z3 (TRADEOFF or -SUBJECT-FREE) the next. LEAD (≥ 30/72) is not expected. The paper's evidence is code repair on 1B–9B models, with no fact-editing result; its side effects were "larger on the small one" (abstract; §4.4: BLEU-RPD −4.11 % on the 1B model against −0.14 % and −2.03 % on the 8B/9B models), and Qwen2.5-3B is nearer the small one.

## 2. Design (engine and harness unmodified; one new writer in a new driver; recipe A and the LAW#5 gate run the untouched path)

### 2.1 Engine and harness seams, read 2026-10-07 (LAW#4)

- **Model** `Qwen/Qwen2.5-3B` @ `3aab1f19…` (`c10e_bandknob.py:25–26`), loaded fp16 on MPS (`:48`). Config (`hf_cache/hub/models--Qwen--Qwen2.5-3B/snapshots/3aab1f1954e9cc14eb9509a215f9e5ca08227a9b/config.json`): hidden 2048 (`:9`), intermediate 11008 (`:11`), 36 layers (`:16`), `rms_norm_eps` 1e-06 (`:18`), tied embeddings (`:21`), vocab 151936 (`:27`). Hparams: final norm `model.norm` (`qwen25_3b_memit_hparams.json:17`), output embedding `model.embed_tokens` (`:18`), rewrite module `model.layers.{}.mlp.down_proj` (`:13`), band [4–8] (`:2`), covariance source `wikipedia` with 100,000 samples (`:19–20`).
- **Stimuli and evaluator.** `CANON` = "The capital of {} is the city of" (`c10e:51`), three sealed held-out templates `PTEST` (`:52–56`), 24 `FICTION` subjects (`:57–61`). Values: `tgt_ids(s) = tok(" " + s, add_special_tokens=False)` (`:67–68`); arms A1 single-token capitals, A2 two-token capitals, A7 coined two-word values (`:224–250`, A7 `:246–249`). `full_seq_match` = greedy decode from the prompt's ids, appending generated ids (`:108–117`); `string_match` (`:120–130`); `teacher_forced_pertok` (`:133–143`); `eval_arm` with exact counts `canon_full_n`, `para_full_n`, `para_first_n`, `para_string_n` (`:358–400`).
- **Locality.** L1 12 real countries and L3 30 unedited capitals (`:259–278`); 20 `GENERIC` sentences and perplexity (`:279–308`); `axes_pre`/`axes_post` (`:311–339`); `described_as` on the 24 edited subjects (`:475–476`, `:490–492`). Same-frame probe: `FRAME_SUBJECTS` (`experiments/track_c/c10p_twopass_arms.py:30`) and `frame_probe` (`:36–42`). Per-prefix bleed gates F1 and the subject-free prefix probe as defined for step 2 (`docs/C10T_SECONDKEY_PREREG.md:48–49`, gate `:69`, qualifier `:71`).
- **Recipe runner** `run_recipe(name, hparam_path)` (`c10e:458–509`): band snapshot `base_snap = snap_layers(hp)` (`:461`), projector (`:462`), standing LAW#5 gate `run_law5` (`:463`; rule `|Δexpr| < 0.05 and |Δloc| < 3`, `:444`; it calls `my_edit` under `_LAW5_DEFAULT_CTX = True`, `:429–435`), `pre_axes` once per recipe (`:471`), per arm: band restore (`:473`), `described_as` baseline (`:475–476`), `my_edit(...)` called by module-global name (`:489`), evaluation (`:490–493`), `ARM_HOOKS` (`:494–495`), `delta_norms` (`:498`); final band restore (`:506`). Seams: `ARM_HOOKS` (`:404`), `Z_OVERRIDE`/`Z_OVERRIDE_HITS` (`:407–408`), `_LAW5_DEFAULT_CTX` (`:403`). `main()` runs only under `__main__` (`:598–599`), so importing the module loads the model (`:48`) and builds the stimuli (`:253`, `:276`) without a forward pass.
- **The restore trap (found by this read).** `snap_layers` and `restore_layers` cover `hp.layers` only, layers 4–8 (`:150–152`, `:155–159`). An ASTRA write in layers outside the band is **not** undone by `run_recipe`'s per-arm restore (`:473`) or its final restore (`:506`). The next arm's `described_as` baseline (`:476`) would then be measured on an edited model. The driver therefore owns a full snapshot and restore of all 36 `down_proj` weights (§2.6 item 5; §2.8 Z6).
- **Closed form (recipe A).** `my_edit` (`:181–221`): `compute_z` per request at `z_layer = 8` (`:184`, `:191`); per band layer keys `compute_ks` (`:196`), `cur` at the subject-last token (`:197–201`), residual divided over the remaining layers (`:204`), float32 CPU solve with projector and `L2 = 1.0` (`:205–211`, `:28–29`), added to the fp16 weight (`:216–217`).
- **Engine facts used.** Context templates sampled once per process into `CONTEXT_TEMPLATES_CACHE` (`memit_main.py:21`, `:304–323`: the identity `"{}"` plus 5 sampled prefixes, so 6 views). `execute_memit` calls `get_context_templates` at `:100`, before any weight change. float64 is used only on CPU ("MPS has no float64", `:191–194`). Covariance via `get_cov` → `layer_stats` (`:240–280`), dataset `wikimedia/wikipedia` 20231101.en (`memit_dry_run/memit/rome/layer_stats.py:97–99`), cached as uncentred second moments for Qwen2.5-3B **layers 4–12 only** (`covariance_caches/Qwen_Qwen2.5-3B/wikipedia_stats/`, listed 2026-10-07). There is no cache for the late layers ASTRA selects.
- **Fingerprint** `tools/engine_fingerprint.py`: expected SHA-256 `d941a9fb…` (`:34`), `_cov_cpu` sites 3 (`:36`).
- **Unmodified files.** `git status` on 2026-10-07 shows `experiments/track_c/c10e_bandknob.py` and `memit_dry_run/memit/` clean (last harness commit `b3c21ae`). The driver hashes both at start and end (V1). The ASTRA writer lives only in `experiments/track_c/c10z_astra_arms.py` (new).

### 2.2 The method — ASTRA §3.1–3.5 on this harness

Notation follows the paper. For layer l and neuron j, `k^l_{j,t}` is the key activation, i.e. the input of `down_proj` at the position that predicts answer token t ("the product of the activated gate projection and the up projection", §3.1). `w^l_j` is column j of `W^l_down` (2048 × 11008). For the final hidden state x_t entering the final norm: scale `s_t = sqrt(mean(x_t²) + 1e-6)` (eps from config `:18`), gain g = `model.norm.weight`, output embedding W = `model.embed_tokens.weight` (tied, config `:21`; hparams `:18`). Logits = W (g ⊙ x_t / s_t) (§3.1).

1. **Views (§3.1, adapted; departure D-2).** For each fact i and each of the J = 6 frozen context templates c_j: prompt string `c_j.format(CANON).format(subject_i)`, the construction `compute_z` uses (`compute_z.py:47`, `:54`). Prompt ids = `tok(prompt)["input_ids"]`, the call `full_seq_match` uses (`c10e:110`). The input is prompt ids followed by `tgt_ids(value_i)[:-1]` (`c10e:67–68`), as id sequences, not decoded and re-tokenised (D-8). The requirement positions are the T_i positions that predict the T_i value tokens. All 144 sequences (24 × 6) go into **one right-padded forward of fixed shape**, in every round and every check (the C10S lesson: fp16 results depend on batch shape, `results/c10s_sharedz_halt_analysis_2026-10-06.md`).
2. **Observation (§3.2).** Teacher-forced forward; at every requirement position t: target y_t, competitor `p_t` = the highest-logit token other than y_t; lead_t = logit(y_t) − logit(p_t). **Failing** iff lead_t < μ, μ = 5.0 logits; deficit γ_t = μ − lead_t. Captured at failing positions: x_t through a forward pre-hook on `model.norm` (not from `output_hidden_states`, whose pre/post-norm convention is not read here: UNVERIFIED), s_t, and `k^l_{j,t}` through forward pre-hooks on `down_proj` (all 36 layers in round 1; carriers only afterwards).
3. **Covector and preferred direction (§3.2).** `c_t = (W_{y_t} − W_{p_t}) ⊙ g`. Output metric `G = W_gᵀ W_g`, `W_g = W diag(g)`, 2048 × 2048, accumulated over vocabulary chunks in **float64 on CPU**, factored once per process by Cholesky (G does not change: the patch touches only `down_proj`). `d_t = G⁻¹ c_t / (c_tᵀ G⁻¹ c_t)`, so `c_t · d_t = 1`.
4. **Carrier selection, round 1 only (§3.3).** SemCon `CS^l_j = Σ_{t∈F} |k^l_{j,t} (c_t · w^l_j) / s_t|` over all 36 layers. Keep the quarter of the layers with the highest summed scores (36 / 4 = **9 layers**), and in each kept layer the `n_L = clamp(⌈R·T / L_S⌉, 16, ⌊0.04 · 11008⌋ = 440)` highest-scoring neurons, R = 16 neurons per answer token, L_S = 9. For the joint batch, T = Σ_i T_i, the answer tokens of the 24 facts counted once, not per view (D-3). For A7 with T_i ∈ [3, 6] (UNVERIFIED; recorded by `pre_base_report`, `c10e:449–455`): T ∈ [72, 144], n_L ∈ [128, 256], |S| ∈ [1,152, 2,304] carriers, 0.29–0.58 % of the model's 396,288 FFN neurons (the paper reports 0.22–0.95 %, §4 Configuration). A1: T = 24, n_L = 43; A2: T = 48, n_L = 86. The set is fixed after round 1 (§3.3: "a fixed set keeps the patch within its budget and lets later rounds refine the same columns").
5. **Null-space weights (§3.4, adapted; D-5).** `D^l_j = 1 / max(m^l_j, 10⁻³ · median_j m^l_j)`, with `m^l_j` the mean squared key activation of neuron (l, j) over a fixed reference set. Reference set: the first 1,000 rows of `wikimedia/wikipedia` 20231101.en (the engine's covariance source, `layer_stats.py:97–99`), each truncated to its first 100 tokens (the cache's `t100`), 100,000 tokens. Computed once for all 36 layers by forward passes only, stored with its SHA-256. The floor stops near-silent neurons from taking unbounded weight. The count of floored neurons is recorded.
6. **Joint solve (§3.4; Algorithm 1 line 6).** `A_tu = (c_t · d_u) (1/s_t) Σ_l Σ_{j∈S_l} D^l_j k^l_{j,t} k^l_{j,u}`, one row and column per failing token across all facts and views. Solve `(A + ρ · mean(diag A) · I) λ = γ` with **ρ = 10⁻³** (the paper says only "a fraction of the mean diagonal entry"; D-6), in **float64 on CPU** (`torch.linalg.solve`). F ≤ 6 × 144 = 864 rows for A7.
7. **Write (§3.4; Algorithm 1 line 7).** `δw^l_j = D^l_j Σ_{u∈F} λ_u k^l_{j,u} d_u` for every carrier. The new column is `fp16(fp32(w^l_j) + fp32(δw^l_j))`, written in place: one rounding per column per round (D-7). Only the selected columns of the kept layers change.
8. **Re-linearisation (§3.5).** Repeat items 2, 3, 6 and 7 over the same carriers until no requirement fails in any view, or 10 rounds. The final patch is the sum of all rounds, already in the weights. The model observed in each round is the deployed fp16 model, so there is no train/deploy gap (unlike step 7's hooked optimisation).

### 2.3 Objective, and what ASTRA does not have

ASTRA's only objective is the margin system of §2.2 items 2 and 6. It has no KL or essence term (compute_z has one, `compute_z.py:151–153`), no hidden-state target and no projector. Protection of unrelated behaviour comes only from the diagonal weight D and the sparsity of the carrier set (§3.3–3.4). Locality is therefore measured, not assumed (§2.9), and spillover is gated (G2, G7, -SUBJECT-FREE in §3).

### 2.4 Settings — fixed now, with reasons

| knob | value | reason |
|---|---|---|
| margin μ | 5.0 logits | paper §4 Configuration; ablation μ = 1 costs 31.4 points (§4.3) |
| views J | 6: identity + 5 engine-sampled prefixes, frozen to a file | the strings `compute_z` builds (`compute_z.py:46–50`); write inputs identical to recipe A's; no new phrasing near the sealed `PTEST` (D-2) |
| rounds | ≤ 10; stop when no requirement fails | §3.5, Algorithm 1 |
| layers kept L_S | 9 of 36 (a quarter) | §3.3, §4 Configuration ("the quarter of the layers") |
| neurons per kept layer | clamp(⌈16·T/9⌉, 16, 440) | §3.3 budget R = 16, bounds 16 and 4 % of the width |
| selection | SemCon, once, in round 1 | §3.3 |
| null-space weight | 1 / max(m, 10⁻³ · layer median), 1,000 Wikipedia rows × 100 tokens | §3.4 (inverse mean squared key activation on reference prompts); D-5 |
| ridge | 10⁻³ × mean diagonal of A | §3.4 ("a fraction"); D-6 |
| solve and G | float64 on CPU | no float64 on MPS (`memit_main.py:191–194`) |
| model precision | fp16 on MPS throughout; captures cast to float32 at the hook | the deployed precision (`c10e:48`); the paper ran bfloat16 (§4 Models) |
| write | per column `fp16(fp32(w) + δw)` per round | D-7 |
| batch shape | one right-padded batch of 144 rows, every round and every check | C10S lesson |
| seed | `torch.manual_seed(0)` at process start | nothing stochastic is expected; recorded |

### 2.5 Recipes and arms (exact counts; same harness, arms and counts as C10Y)

- **A — closed-form baseline**: the harness as it stands (`my_edit` untouched, `Z_OVERRIDE = None`), arms A1, A2, A7. Its A7 count is the comparator and its envelope is the LAW#3 gate.
- **Z — ASTRA (the candidate)**: §2.2 on the same 24 requests per arm. Stage 1: A7 only. Stage 2: A1 and A2.
- **Z-band — attribution (stage 2, A7 only)**: identical to Z except that carrier selection is restricted to layers 4–8 (all five kept, L_S = 5, n_L = clamp(⌈16·T/5⌉, 16, 440)). It asks whether a gain needs ASTRA's late-layer site or comes from the per-position objective at the harness's own band.

The binding count is A7 `para_full_n` /72 of the fp16 model as merged, read by the unmodified `eval_arm` (`c10e:358–400`).

### 2.6 Execution: stages (one process per pass; mechanism follows C10Y §2.6 with the step-6/7 review fixes)

The driver imports the harness as module `H` and refuses the inherited knobs (`C10_PROJECTOR` `:40`, `N_EDIT`/`C10_SUBJECT_OFFSET` `:62–63`, `C10_CTX_TEMPLATES` `:182`, `C10_ARMS` `:254`, `C10_KEY_LOCUS` `:477`, `C10_RECIPES` `:582`). Arms are restricted per call by assigning `H.ARMS` (read at `:472`): a driver assignment, not a harness edit.

**Stage 0 — instruments and the LAW#3 gate (no ASTRA code touches the model before step 4).**
1. **Fingerprint and pristine pin.** `tools/engine_fingerprint.py` → `d941a9fb` and `_cov_cpu == 3`; SHA-256 of `c10e_bandknob.py` and of the driver. Immediately after import: **`H_pristine`** = SHA-256 over the bytes of every tensor in `model.named_parameters()` order, plus per-layer SHA-256 of the 36 `down_proj` weights. `PRISTINE` = a CPU copy of the 36 `down_proj` weights (1.62 GB). Also recorded: the SHA-256 of each `model*.safetensors` file in the snapshot directory. In process 2, `H_pristine` must equal process 1's.
2. **Pristine-model probes**: F1 and subject-free "base" hits (needed for "newly induced" counts, §2.9) and the Z0 shape spread (§2.8).
3. **Recipe A**: `H.run_recipe("A", HP_BASE)` with the original `my_edit`, arms A1, A2, A7, `ARM_HOOKS = [probe_hook, restore_hook]` (§2.9, item 5 below). In process 1 the engine samples the context templates here (`memit_main.py:100`); the driver then writes `CONTEXT_TEMPLATES_CACHE` to `results/c10z_astra/context_templates.json` with its SHA-256. Process 2 sets the module global from that file before recipe A (the C10U/C10Y precedent, `docs/C10Y_DIRECTDW_PREREG.md:85`).
4. **LAW#3 gate, in the driver, before anything else runs.** Recipe A, A7: `para_full_n` ∈ [5, 18]/72, `canon_full_n` ∈ [5, 10]/24, `para_first_n` ∈ [42, 59]/72 (`CORPUS/44:39`); A1 and A2 `para_full_n` ≥ 68/72. A miss writes `pass_p{n}.json` with recipe A only, writes `architecture_profile/c10z_astra_halt_diagnostic.json`, exits non-zero: label HALTED-V4. No D statistic, no G, no check and no Z recipe runs. The reader re-checks the same numbers.
5. **Instruments for the new path**: D statistics (§2.2 item 5) and G (item 3), each stored with its SHA-256; the V7/V8 sanity checks; then the LAW#5 checks Z0–Z6 (§2.8). Any failure → HALT.

**Stage 1 — early kill (≈ 1.0–1.5 h including stage 0, §2.11).** `H.my_edit` is rebound to a wrapper. With mode `None`, or whenever `H._LAW5_DEFAULT_CTX` is True (`:403`, `:429–435`), it delegates unchanged to the original. With mode `astra`, it restores all 36 `down_proj` from `PRISTINE`, verifies their hashes, runs §2.2 on the arm's requests and returns a `delta_norms` dict per touched layer in the harness's format (`:213–215`). Then `H.ARMS = {A7}` and `H.run_recipe("Z", HP_BASE)`. `restore_hook`, the last entry of `ARM_HOOKS`, copies `PRISTINE` back into all 36 layers and checks the hashes after each arm's readouts, so the next arm's `described_as` baseline (`:476`) is pristine (the restore trap, §2.1). **Kill rule K1 (§3.4)** is read here.

**Stage 2 — survivors of K1 only (same process).** `H.ARMS = {A1, A2}` under Z (side gate G0); `H.ARMS = {A7}` under Z-band (attribution). The label is recomputed with G0 (§3.3).

**Stage 3 — process 2, only if stage 2 ends in an unqualified PARTIAL or LEAD** (§3.4 rule K2). A fresh process repeats stages 0–2 from the same input manifest, loading the frozen templates, the D file and the G file by SHA-256. Recipe A and its LAW#3 gate run first again. This is the reproducibility run and gate A ("Replicate any arm ≥ 30/72 in a second process", `INTEGRATED_QUEUE:26`).

### 2.7 Reproducibility rule (the overlay-hash question)

Record: an **input manifest hash** `H_in` = SHA-256 over (the 24 request JSONs per arm, model revision, `H_pristine`, context-template file SHA-256, D-statistics SHA-256, G SHA-256, the §2.4 table as JSON, driver and reader source SHA-256s, seed). An **output hash** `H_out` = SHA-256 of the final fp16 bytes of every touched `down_proj` column, with the (layer, column) list. A **regeneration certificate**: process 2 regenerates from `H_in`, and the write counts as the same write iff R1–R3 hold (§3.5). This is the experiment's proposal for how a ledger could own the write (spec `:671`); it is not a spec change.

### 2.8 Inertness (LAW#5) and step-0 checks — numeric, same process; any failure → HALT

**Why the reduction is to the unedited model, not to the engine's write.** ASTRA and the closed form solve different problems: logit margins at value positions against a hidden-state target at the subject-last token; different keys; different site. No configuration of ASTRA reproduces `my_edit`'s ΔW, so a reduction to it cannot be built honestly. The checks below instead reduce the new path to the unedited model through its full code path (Z3), test its algebra on its real inputs (Z4), tie its observation to the binding evaluator (Z1, Z2), and bound what it writes (Z5, Z6). The known-ceiling reference is recipe A in the same process, gated by LAW#3 (stage 0 step 4).

**Tolerance calibration (the C10S lesson).** In C10S a 1e-4 bar broke because two fp16 forwards of the same text at different batch shapes differ by a few fp16 units (step-0 NLL Δ 0.0117, two references 0.0166 apart; `results/c10s_sharedz_halt_analysis_2026-10-06.md`). Comparisons here are therefore of two kinds. **Same-shape** comparisons of the same weights are bitwise: the measured floor is 0.0 (ibid., check (i)), so their tolerance is exactly 0. **Cross-shape** comparisons (the 144-row observation batch against the single-sequence forwards the evaluator uses, `c10e:110`) use τ, measured in Z0.

- **Z0 (shape spread → τ).** Pristine model, A7: σ = max over the 24 facts and all T_i value positions of the identity view of |lead in the 144-row batch − lead in a single unpadded forward of the same sequence|. **τ = max(2σ, 0.02) logits.** If σ > 0.125 logits (τ would exceed 0.25, 5 % of μ), HALT: the spread itself is the anomaly to diagnose (the C10X advisor's ceiling rule, `results/c10x_enginepath_advisor_v1.md` issue 9).
- **Z1 (lead reconstruction).** In the same forward, the driver's float32 lead recomputed from the captured x_t, s_t, g and the rows W_{y_t}, W_{p_t} equals the model's own fp16 logit lead within τ at every requirement position. This catches a post-norm capture, a wrong position offset or a wrong competitor.
- **Z2 (agreement with the binding evaluator).** On the pristine model, and again after every Z write: E_drv = facts whose identity-view leads are all > 0, excluding facts with any |lead| ≤ τ (counted as ambiguous). E_eval = facts with `canon_full` True in `eval_arm` (the identity view is `CANON.format(subject)`). Pass iff E_drv = E_eval on the non-ambiguous facts. Teacher-forced top-1 at every position is the same event as a greedy full match.
- **Z3 (reduction to the unedited model through the full path).** One round on the A7 batch with the real failing set F (μ = 5) and every deficit γ_t replaced by 0.0: observation, covectors, G⁻¹, SemCon selection, assembly of A with ridge, float64 solve and the per-column write-back all execute. Pass iff (a) λ is exactly 0 in float64; (b) the write-back executed for exactly |S| columns (counter); (c) all 36 `down_proj` weights are value-equal to `PRISTINE` (`torch.equal`; the fp16→fp32→fp16 round trip is exact, though −0 may become +0, so bytes are not compared here); (d) on the 96 A7 evaluation prompts (24 CANON + 72 PTEST), greedy generations equal the pristine ones and max |Δ logit| at the last prompt position is 0.0 (same weights, same shape: tolerance 0). The driver then restores `PRISTINE` by copy and checks the byte hashes (Z6).
- **Z4 (first-order identity of the active path, float64 CPU, no model forward).** On the real round-1 quantities of the A7 batch (real γ, patch computed and not written): v_t = Σ_l Σ_{j∈S_l} k^l_{j,t} δw^l_j; predicted Δlead_t = (W_{y_t} − W_{p_t}) · (g ⊙ v_t) / s_t, computed from the embedding rows directly, not from d or A. Pass iff |Δlead_t − (A λ)_t| ≤ 1e-8 · max(1, |γ_t|) for every t ∈ F. Plus an independent loop implementation of A over (t, u, l, j) for 32 randomly chosen rows (seed 0): relative difference ≤ 1e-10. This exercises the d_t, D, k, index and assembly code with the deficits the solve really sees. Recorded, not gated: the ridge residual ‖A λ − γ‖_∞ / ‖γ‖_∞ and cond(A + ρ·mean diag·I).
- **Z5 (write footprint), after every Z write.** The set of (layer, column) pairs differing from `PRISTINE` is a subset of S. Every parameter other than the 36 `down_proj` weights still matches its `H_pristine` component (per-tensor SHA-256). No float64 tensor exists on MPS (asserted at the solve boundary).
- **Z6 (pristine identity).** Per-layer SHA-256 of all 36 `down_proj` equals `PRISTINE`'s: before each `run_recipe` call, after every `restore_hook`, after every check that writes, and after each recipe.
- **Standing gate.** `run_law5` inside every recipe (`c10e:463`, rule `:444`) must read INERT. For the ASTRA modes it is inert *by construction* (the wrapper delegates under `_LAW5_DEFAULT_CTX`); it is reported as harness/engine parity only. The new writer's inertness is Z1–Z6.
- **Instrument sanity.** **V7:** for each band layer 4–8, the Spearman correlation between `m^l_j` (§2.2 item 5) and the diagonal of the cached second moment (`covariance_caches/Qwen_Qwen2.5-3B/wikipedia_stats/…_mom2_t100_100000.npz`) is ≥ 0.80; a lower value means the 1,000-row statistic does not track the engine's 100,000-sample one → HALT. **V8:** the float64 Cholesky of G succeeds; cond(G) is recorded.

### 2.9 Readouts (every recipe, every arm unless noted)

- **Binding and decomposition** (`eval_arm`): `para_full_n` /72, per held-out template (3 × 24), per-fact 24-vector, `canon_full_n` /24, `para_first_n` /72, `para_string_n`, `tf_pertok_cont`, `cond_full_given_first`.
- **Locality** (vs recipe A, same process): L1 flips /12, L3 top-1 agreement /30 and mean KL, generic perplexity pre/post (`c10e:319–339`); `described_as` (`:492`); **F0** same-frame flips /6 (`c10p:36–42`, with the current arm's first tokens); **F1** 24 per-prefix bleed gates: for each fact i, the six prompts `CANON.format(s) + decode(V_ids^i[:1])` over the six `FRAME_SUBJECTS`; newly induced next-token hits (top-1 = `V_ids^i[1]`) and full-remainder hits, against base (`docs/C10T_SECONDKEY_PREREG.md:48`, with j_i = 1 for every fact because every value position carries a requirement here); **subject-free probe**: `"The name is" + decode(V_ids^i[:1])`, 24 prompts, full-remainder hits (`:49`). F1 and the subject-free probe are defined for multi-token values and run on A7 (and A2); on A1 they are recorded as not applicable.
- **ASTRA diagnostics per write**: |F| and Σγ per round; stop reason (no failing token / round cap); rounds used; layers kept and carriers per layer; neuron share of the 396,288 FFN neurons; carriers outside L17–L28 (the spec range scaled, §0); cond(A); λ range; floored D count; **relative patch norm** ‖δw_j‖/‖w_j‖ per carrier (median, IQR; the paper's diagnostic, §4.2, §5); **parallelism** |cos(δw_j, w_j)| (§4.2); fp16 cast retention (‖realised column change‖ / ‖intended‖, median); **linearisation fidelity** (round-1 predicted vs realised Δlead: Pearson r and slope); wall-clock per write; peak memory.
- **Fit (§3.2)**: φ_μ, φ_0^id and the per-fact minimum lead on each view, in the final observation.
- **Premise readouts (not gated)**: per-position teacher-forced lead on the 72 held-out A7 prompts, pre and post, positions 1 and ≥ 2 separately (where the wall sits after a margin write); **predicted transfer**: the first-order Δlead the round-1 patch predicts at the 72 held-out prompts' value positions (Z4's formula, applied to held-out keys), against the realised change. Held-out quantities are read only after the write and never enter the solve.
- **Write geometry**: ‖ΔW‖_F per touched layer; Σ‖ΔW‖_F of Z over recipe A's (reported only; the sites differ).

### 2.10 Memory arithmetic (48 GB unified memory; CPU tensors share the pool)

| item | arithmetic | size |
|---|---|---|
| model weights fp16 | 3,085,938,688 params × 2 B (C10Y §2.10 breakdown) | 6.17 GB (5.75 GiB) |
| band covariances, CPU float32, loaded by `compute_P` in every `run_recipe` (`c10e:169–172`; `memit_main.py:280`) | 5 × 11008² × 4 B | 2.42 GB |
| band projectors P (`c10e:175`) | 5 × 11008² × 4 B | 2.42 GB |
| band snapshot (`c10e:152`) | 5 × 2048 × 11008 × 2 B | 0.23 GB |
| `PRISTINE`, all 36 `down_proj` (CPU) | 36 × 2048 × 11008 × 2 B | 1.62 GB |
| G and its Cholesky factor, float64 CPU | 2 × 2048² × 8 B; vocabulary chunks of 8,192 rows × 2048 × 8 B while accumulating | 0.07 GB + 0.13 GB transient |
| D statistics | 36 × 11008 × 4 B | < 0.01 GB |
| observation forward, no grad (144 rows, padded length T_pad ≈ 28, UNVERIFIED until step 0) | 4,032 tokens; per-layer transients ≈ 4,032 × (6 × 2048 + 4 × 11008) × 2 B, freed layer by layer | ≈ 0.46 GB transient |
| round-1 key captures, all layers, float32 | ≤ 864 positions × 36 × 11008 × 4 B | ≤ 1.37 GB |
| later-round captures (carriers only) | ≤ 864 × 3,960 × 4 B | < 0.02 GB |
| logits at requirement positions, top-2 only, chunked | 864 × 151936 × 2 B per chunk pass | ≤ 0.26 GB transient |
| SemCon per layer | `W_down` fp32 copy 90 MB + `W_downᵀ C` 11008 × 864 × 4 B | ≈ 0.13 GB transient |
| A and its solve (F ≤ 864) | 864² × 8 B × 3 | < 0.02 GB |
| D-statistics pass, batch 16 × 100 tokens | transient activations | ≈ 0.2 GB |
| **peak** | 5.75 + 2.26 + 2.26 + 0.21 + 1.51 + 1.28 + ≈ 1.0 transient (GiB) | **≈ 14.3 GiB** |

**Ceiling:** at step 0 and at every write, `torch.mps.driver_allocated_memory()` + process RSS (`psutil`) > 40 GiB, or MPS driver memory alone > 32 GiB → HALT (the step-7 advisor's fix, issue 9). Both recorded. Memory is far from the 48 GB limit; the chip is the limit (D-C10r-rulings-4 (1)).

### 2.11 Compute estimate (measured where marked; ASTRA's own cost is unmeasured on this machine)

- **Measured anchors (brief, 2026-10-07):** a three-arm harness pass ≈ 34 min; one behaviour run ≈ 23 min (`INTEGRATED_QUEUE:18`: "measured ≈ 23 min per run"). Read here as: per recipe ≈ 34 min = ≈ 23 min of evaluation for three arms (≈ 7.7 min per arm) + ≈ 11 min of solves, projector SVD and LAW#5. One `compute_z` ≈ 7 s (`results/c10x_enginepath_advisor_v1.md` issue 13).
- **ASTRA per write (unmeasured; estimate):** one round = one forward of 4,032 tokens ≈ 4,032 × 6 GFLOP ≈ 24 TFLOP → ≈ 5–12 s at an assumed 2–5 TFLOP/s; top-2 logits at ≤ 864 positions ≈ 0.5 TFLOP; round-1 SemCon over 36 layers ≈ 1.4 TFLOP; float64 solve of ≤ 864 rows < 1 s. **≈ 10–20 s per round, ≤ 3.5 min per write at 10 rounds.**
- **One-off:** D statistics 100,000 tokens ≈ 0.6 PFLOP ≈ 2–5 min; G 151,936 × 2048² × 2 ≈ 1.3 TFLOP float64 on CPU ≈ 10–60 s; Z0–Z6 ≈ 5 min; hashing (6.2 GB full, 1.6 GB `down_proj`) ≈ 10–30 s per full hash.
- **Stage 0 + stage 1:** fingerprint and hashes ≈ 2 min + recipe A ≈ 34 min + D, G and checks ≈ 10 min + Z on A7 (SVD and LAW#5 ≈ 3 min, write ≤ 3.5 min, evaluation ≈ 7.7 min, F0/F1/subject-free ≈ 2 min) ≈ 16 min → **≈ 62 min; budget 1.0–1.5 h.** A LAW#3 miss ends the process after ≈ 36 min.
- **Stage 2:** Z on A1+A2 ≈ 3 + 2 × 13 ≈ 29 min; Z-band A7 ≈ 16 min → ≈ 45 min.
- **Stage 3:** process 2 = stages 0–2 again ≈ 1.8 h.
- **Maximum:** ≈ 1.5 + 0.75 + 1.8 ≈ **4.1 h**, of which only stage 0–1 is committed.
- **Budget rule:** if a stage-1 round exceeds 120 s (projected > 20 min per write), HALT for an operator budget ruling; the round cap is not lowered silently.

### 2.12 Records

`results/c10z_astra/`: `context_templates.json` (+ SHA-256), `dstats.pt` and `G.pt` (+ SHA-256s), `pristine_hash.json` (`H_pristine`, per-layer hashes, safetensors file hashes), `manifest.json` (`H_in` and its parts), `checks_p{1,2}.json` (Z0–Z6, V7, V8, memory, timing), `pass_p{1,2}.json` (every recipe and arm: readouts of §2.9, per-write ASTRA traces, `H_out`), `repro.json` (R1–R3), `run.json`; logs under `results/c10z_astra/logs/`. Driver `experiments/track_c/c10z_astra_arms.py`; reader `experiments/track_c/c10z_astra_read.py`, which encodes every gate, label and qualifier of §3 (the reader, not prose, issues labels; the CORPUS/50 prose/code divergence is the reason). HALT diagnostic `architecture_profile/c10z_astra_halt_diagnostic.json`.

## 3. Pre-registered readings (exact counts; decision order fixed)

**Decision order:** HALT checks → fit (U) → binding count → side gates → base label → qualifiers → attribution → replication.

### 3.1 Validity — any failure → HALT with label HALTED-V*k* (no candidate label is issued)

- **V1** Fingerprint `d941a9fb` and `_cov_cpu == 3`; SHA-256 of `c10e_bandknob.py` and of everything under `memit_dry_run/memit/memit/` equal at start and end of the process.
- **V2** `run_law5` INERT in every recipe (`c10e:444`).
- **V3** `H_pristine` recorded at import; Z6 holds at every named point; in process 2, `H_pristine` equals process 1's.
- **V4 (LAW#3)** Recipe A: A7 `para_full_n` ∈ [5, 18]/72, `canon_full_n` ∈ [5, 10]/24, `para_first_n` ∈ [42, 59]/72; A1 and A2 `para_full_n` ≥ 68/72. Checked in the driver before any new code touches the model.
- **V5** Z0–Z5 pass (§2.8).
- **V6** No non-finite value in any A, λ, δw or captured tensor.
- **V7, V8** Instrument sanity (§2.8).
- **V9** Audit counters: within each Z or Z-band recipe, wrapper ASTRA calls = number of arms run, original-path calls = 0 outside `run_law5`, `Z_OVERRIDE_HITS` = 0 (`c10e:408`).
- **V10** `para_string_n ≥ para_full_n` for every arm.
- **V11** Memory ceiling (§2.10) and no float64 on MPS.
- **V12** `H_in`, `H_out`, every SHA-256 of §2.12, stop reason and rounds used per write are in the record.

### 3.2 Fit rule (the underfit gate)

In the final observation of the deployed fp16 model (the 144-row batch, after the last round):
- φ_μ = share of all requirement triples (fact, view, value position) with lead ≥ 5.0 logits;
- φ_0^id = number of facts (of 24) whose identity-view leads are > 0 at every value position.

**U (UNDERFIT) iff φ_μ < 0.95 or φ_0^id < 23.** Boundaries: φ_μ = 0.95 with φ_0^id = 23 is FIT; φ_μ = 0.9499 is U; φ_0^id = 22 is U. A write that stops because no requirement fails has φ_μ = 1.0 by construction. The 0.95 allows for the cross-shape spread and the fp16 write rounding (both ≪ μ).

### 3.3 Labels (per process; A7 is the binding arm)

Let n = Z's A7 `para_full_n` /72, a = recipe A's A7 `para_full_n` /72 in the same process (a ∈ [5, 18] by V4), g = n − a. Side gates, each against recipe A of the same process (`results/research_pass_2026-10-06/prereg_stubs.md:10` form, as C10Y §3):
- **G1** L1 flips ≤ A + 1 (of 12);
- **G2** F0 same-frame flips ≤ A + 1 (of 6);
- **G3** `described_as` ≥ A − 3.0;
- **G4** L3 agreement ≥ 29/30;
- **G5** generic perplexity ≤ A + 0.5;
- **G7** each of the 24 F1 per-prefix gates: newly induced next-token hits ≤ A's newly induced hits on the same six prompts + 1 (of 6);
- **G0** (stage 2 only) Z's A1 `para_full_n` ≥ 68/72 and Z's A2 `para_full_n` ≥ 68/72.

S = all side gates measured so far hold (stage 1: G1–G5, G7; stage 2 onward: plus G0).

**Table T — base label B (rows are disjoint and cover every (n, g, S)):**

| row | n | g = n − a | S | B |
|---|---|---|---|---|
| T1 | 0–18 | any | any | NULL |
| T2 | 19–72 | ≤ 9 | any | NULL |
| T3 | 19–29 | ≥ 10 | true | PARTIAL |
| T4 | 30–72 | ≥ 10 | true | LEAD |
| T5 | 19–72 | ≥ 10 | false | TRADEOFF |

Since a ≤ 18, n ≥ 30 implies g ≥ 12, so T4 never needs the g condition. It is kept for symmetry.

**Rule U:** if U holds and B = NULL, the label is **UNDERFIT** ("inconclusive under this solve budget"), never NULL. If U holds and B ∈ {TRADEOFF, PARTIAL, LEAD}, the label is B with **-UNDERFIT**.

### 3.4 Stage rules

- **K1 (stage-1 kill, read on A7 after stage 1):** continue to stage 2 iff n ≥ 19 **and** g ≥ 10 (rows T3–T5). Otherwise stop. The final label is T1/T2 under rule U (NULL or UNDERFIT) with **-STAGE1** (G0, Z-band and process 2 not run; none of them could raise a NULL). Kill threshold in plain numbers: Z's A7 held-out count ≤ 18/72, or less than recipe A's + 10.
- **K2 (process 2):** runs iff the stage-2 label is PARTIAL or LEAD carrying none of -UNDERFIT, -LARGE-WRITE, -SUBJECT-FREE, -EXCEEDS-TTL. Otherwise the stage-2 label is final, with **-SINGLE-PROCESS** (non-binding, as `results/research_pass_2026-10-06/prereg_stubs.md:11` states for one-process results).

### 3.5 Qualifiers (attach to any base label; never change it; any qualifier blocks adoption and gate A)

- **-UNDERFIT**: rule U.
- **-LARGE-WRITE (W1)**: the median relative patch norm ‖δw_j‖/‖w_j‖ over carriers (final summed patch against `PRISTINE`) > 1.0. This is ASTRA's own size diagnostic (§4.2, §5); C10Y's Σ‖ΔW‖ ratio does not transfer across write sites.
- **-SUBJECT-FREE**: subject-free probe full-remainder hits > recipe A's + 1 (of 24), the step-2 rule (`docs/C10T_SECONDKEY_PREREG.md:71`).
- **-EXCEEDS-TTL (W2)**: any Z write wall-clock > 60 min (spec `:783`).
- **-STAGE1**, **-SINGLE-PROCESS**: §3.4.
- **Across processes (stage 3 only).** Rank NULL = UNDERFIT = 0 < TRADEOFF = 1 < PARTIAL = 2 < LEAD = 3. The step label is the lower-ranked process label. At rank 0 it is UNDERFIT if either process is U, else NULL. Qualifiers are the union. **-NOT-REPLICATED** if the two base labels differ. **-NOT-REPRODUCIBLE** if any of R1–R3 fails:
  - **R1** identical carrier set S and identical rounds used, and per touched layer ‖ΔW_p1 − ΔW_p2‖_F / ‖ΔW_p1‖_F ≤ 1e-3, for every Z arm;
  - **R2** |n(p1) − n(p2)| ≤ 2;
  - **R3** ≤ 3 of the 72 held-out A7 prompts disagree between processes.

  These are tighter than C10Y's because nothing in ASTRA is stochastic. The frozen templates, D and G are loaded by hash, and same-shape forwards have a 0.0 floor. A process-2 result outside them is a finding about regeneration.

**Attribution (stage 2; recorded beside the label, does not change it).** Let n_b = Z-band's A7 count. **OBJECTIVE-CARRIES** if n_b ≥ n − 5 (the gain holds at the harness's own band); else **SITE-DEPENDENT** if n_b ≤ a + 9; else **MIXED**. The order of tests makes the three disjoint.

### 3.6 Worked rows, recorded before any run (a = 12 unless stated; "gates" = every side gate holds)

| case | inputs | label |
|---|---|---|
| 1 | n = 18, FIT | NULL-STAGE1 (T1; K1 stops) |
| 2 | n = 18, U (φ_μ = 0.80) | UNDERFIT-STAGE1 |
| 3 | n = 21, g = 9 (a = 12) | NULL-STAGE1 (T2) |
| 4 | n = 25, a = 16, g = 9 | NULL-STAGE1 (T2) |
| 5 | n = 22, g = 10, gates, FIT; stage 2 G0 holds, W1 0.4 | PARTIAL → process 2; p2 n = 23 → PARTIAL (replicated, reproducible if R1–R3) |
| 6 | n = 22, g = 10, G7 fails 3 of 24 | TRADEOFF-SINGLE-PROCESS |
| 7 | n = 29, gates, FIT; stage 2 Z-A1 = 67/72 | TRADEOFF-SINGLE-PROCESS (G0 fails) |
| 8 | n = 30, gates, FIT, W1 0.6; p2 n = 29 | p1 LEAD, p2 PARTIAL → PARTIAL-NOT-REPLICATED (R2 holds: \|30 − 29\| = 1) |
| 9 | n = 31, gates, U (φ_0^id = 22) | LEAD-UNDERFIT-SINGLE-PROCESS (K2 not met) |
| 10 | n = 24, g = 6, U | UNDERFIT-STAGE1 |
| 11 | n = 33, gates, FIT, W1 1.4 | LEAD-LARGE-WRITE-SINGLE-PROCESS |
| 12 | n = 26, gates, subject-free hits A + 4 | PARTIAL-SUBJECT-FREE-SINGLE-PROCESS |
| 13 | recipe A A7 = 19/72 | HALTED-V4 (no Z code runs) |
| 14 | Z3 (d): one greedy generation differs | HALTED-V5 |
| 15 | stage 2: n = 26, n_b = 23 | PARTIAL …, attribution OBJECTIVE-CARRIES (23 ≥ 21) |
| 16 | stage 2: n = 26, n_b = 20 | attribution SITE-DEPENDENT (20 < 21 and 20 ≤ 21) |
| 17 | stage 2: n = 40, a = 12, n_b = 28 | attribution MIXED (28 < 35 and 28 > 21) |

**What each buys.** LEAD, unqualified, replicated and reproducible → a write-path candidate: the operator's route ruling (§6 decision 1), then the Incremental shape, Q4_K_M survival (`INTEGRATED_QUEUE:32`) and the §8.2 amendment question. PARTIAL → the next configuration as its own pre-registration (differently worded deterministic views; Z on top of recipe A's write; per-fact sequential shape). TRADEOFF or -SUBJECT-FREE → report: margin writes at value positions buy recall with spillover, the CORPUS/53 family. NULL with FIT → H-Z2 or H-Z0 for this configuration; the premise readouts say which position fails. UNDERFIT → inconclusive; any budget change is a new pre-registration.

## 4. Not claimed, whatever the outcome

No label in CORPUS/44–53 changes. LEAD is a write-path candidate. It is not §8.9 contract closure, not route closure, not an F1 change and not a replication of ASTRA (different domain, model, precision, view set, batch shape, reference set; §7). NULL does not close margin solves, joint solves or late-layer writes. Nothing is claimed about which components carry the value beyond the attribution rule. **Spec-amendment flags if ever adopted:** §8.2's designated engine and D20 safeguards (spec `:311–317`, §0); the `COMMITTED` overlay hash (spec `:671`) becoming the `H_in`/`H_out`/certificate triple (§2.7); the write site moving outside L17–L28-scaled when carriers sit there (§2.9). **Compaction at scale is not tested:** F grows with facts × views × value tokens; a 10,000-row system needs 0.8 GB in float64 and a 36,000-row one 10.4 GB.

## 5. Halt discipline and close-out

One speculative fix after a `cat -n` read, then HALT with a diagnostic JSON (`architecture_profile/c10z_astra_halt_diagnostic.json`) and a `SESSION_CHECKPOINT.md` entry. Pre-named halts: V1 fingerprint or file hashes; V3 pristine hash mismatch; **V4 recipe A outside the envelope (LAW#3; the process exits before any ASTRA code runs; the runs made are kept as data, not promoted)**; any of Z0–Z6; V6 non-finite values; V7 D-statistic sanity; V8 Cholesky failure; V11 memory ceiling or float64 on MPS; a stage-1 round over 120 s (budget ruling). Close-out through `tools/closeout_check.py D-C10z-astra` once the CORPUS entry exists. Advisor pass before any code; Codex GPT-6-Astra (high) at the design pass, the implementation review, the verdict, and the promote gate if LEAD.

## 6. Reviews and open points

v1 draft (this file) → advisor pass → Codex GPT-6-Astra design pass → v2 → lead read-through → freeze → implementation (driver: wrapper modes, full-band snapshot/restore and `restore_hook`, observation batch, captures, G, D statistics, SemCon selection, joint solve, write, rounds, F0/F1/subject-free probes, Z0–Z6, manifest; reader) → implementation review → stage 0–1 → K1 → stage 2 → K2 → process 2 → verdict → CORPUS/NN.

**Questions for the reviewers.**
- (a) *Views.* The six views share the CANON frame and differ only in a sampled prefix, which is weaker diversity than ASTRA's four rewordings (§3.1; −6.5 points for one view, §4.3). Adding deterministic renderings derived from the request would bring new phrasing near the sealed `PTEST`, and would need the overlap audit of `results/research_pass_2026-10-06/prereg_stubs.md:12`. Keep six engine views for v1, or add renderings?
- (b) *Joint batch of 24 versus 24 independent repairs* (the paper's protocol, §4 Protocol). The joint system is the Genesis shape and comparable with recipe A; the sequential shape is the Incremental one. Is the budget rule T = Σ T_i right for the joint case?
- (c) *Null-space weights.* 1,000 Wikipedia rows instead of 32 out-of-domain prompts; the 10⁻³-median floor; V7's 0.80 bar.
- (d) *Margin scale.* μ = 5 was tuned on bfloat16 code models. Qwen2.5-3B's typical top-1 leads on these prompts are not measured; should step 0 record the pristine lead distribution as a readout (proposed: yes, non-gating)?
- (e) *LAW#5 sufficiency.* No ASTRA configuration reproduces the engine's write (§2.8). Is Z3 (full path to the unedited model) + Z4 (first-order identity on real inputs) + Z1/Z2 (observation tied to the evaluator) + recipe A under LAW#3 an adequate known-ceiling reference?
- (f) *Fit thresholds* φ_μ ≥ 0.95 and φ_0^id ≥ 23/24.
- (g) *W1 threshold* 1.0 on the median relative patch norm (the paper reports medians per setting but its macro values were not resolvable from the LaTeX source; UNVERIFIED that 1.0 is outside its range).
- (h) *A stacked variant* (ASTRA rounds started from recipe A's merged write, repairing the band write's value positions) is the most direct "realisation" repair, but it mixes two writers and two sites. It is left out of v1 as its own pre-registration; is that right?

**Decisions for the operator at the go (recommendation first; one yes/no each).**
0. *Scheduling under D-C10r-rulings-4 (3):* recommend yes, schedule row 5b in step 7's slot once the reviews pass. The demotion's stated reason (the reversed "3 % installed" premise) does not apply to this arm (§0), and the queue already names it as step 7's possible replacement (`INTEGRATED_QUEUE:23`). The alternative is to hold it behind the step-5 oracle with step 7.
1. *Write qualification:* recommend **write candidate** (a per-commit solve with no training set and no training loop, regenerable from the patch, §0), with the spec flags of §4 kept open. A "measurement" ruling changes no gate or label.
2. *Budget:* stage 0–1 ≈ 1.0–1.5 h committed; stages 2–3 ≈ 2.6 h only on survival; recommend yes to stage 0–1.

## 7. Departures and decisions where the source is silent (each open to the reviews)

- **D-1 Domain.** Fact writes of coined values into a 3B base model, not API-repair of code models (§4 Benchmarks). The paper has no fact-editing result (scout `:18`).
- **D-2 Views.** Six engine context-template views (identity + five sampled prefixes, frozen), not four hand-written renderings (§3.1). Reason: write inputs identical to recipe A's and no new wording near the sealed held-out set.
- **D-3 Batch.** One joint system over the failing tokens of all 24 facts, one carrier set, budget T = Σ T_i. The paper repairs "one failing sample at a time" from the original weights (§3; §4 Protocol). Reason: the Genesis shape of recipe A.
- **D-4 Layer count.** A quarter of 36 = 9 layers (the paper's quarter kept 6, 8 and 8 layers on its models, §4 Configuration).
- **D-5 Reference set for D.** 1,000 Wikipedia rows × 100 tokens (the engine's covariance source) instead of "32 test prompts of the other benchmark" (§4 Configuration). Plus a floor at 10⁻³ of the layer median, which the paper does not mention.
- **D-6 Ridge.** ρ = 10⁻³ of the mean diagonal; the paper gives no value (§3.4).
- **D-7 Precision.** fp16 model on MPS with float32 captures, float64 G and solve on CPU, one fp16 rounding per column per round. The paper used bfloat16 on one GPU (§4 Models). No float64 on MPS.
- **D-8 Token construction.** Prompt ids concatenated with value ids, matching `full_seq_match` (`c10e:110–116`), not `compute_z`'s decode-and-re-tokenise (`compute_z.py:47`).
- **D-9 Scale.** s_t from the final norm's input with eps 1e-6 (config `:18`); the paper defines it as the RMS (§3.1) without an epsilon.
- **D-10 Fit criterion.** The paper stops when no token fails (§3.5) and has no fit gate. Here the underfit gate reads φ_μ ≥ 0.95 and φ_0^id ≥ 23 after the loop (§3.2).
- **D-11 No KL or essence term.** Faithful to the paper. Recorded because every earlier C10 writer had one (`compute_z.py:151–153`).
- **D-12 Selection pool.** All 36 layers, the band included. The paper does not exclude early layers by rule; its selections never fell in the first 58 % of the depth (§4.2).
- **D-13 Z-band** attribution recipe (not in the paper).
- **D-14 Process 2** is conditional (K2) and doubles as gate A.
- **D-15 Competitor.** p_t is the highest-logit token other than y_t over all 151,936 logits, the same space as the evaluator's argmax (`c10e:114`).
- **D-16 Citation numbering.** The paper's own section numbers are used throughout; the queue's "§5.3" is the paper's §4.3.

## 8. Review fold log

(empty at v1)
