# Pre-registration — D-C10x-enginepath: forward-replay target construction (arm I-2, FE) and token-level reweighting of the value objective (arm I-1, OverTone), each as a harness seam on the C10 write path (step 6 of the research pass's recommended sequence; H-11) (FROZEN v2.2, 2026-10-07)

**Status: FROZEN v2.2 (2026-10-07) — GPT-6-Astra high: freeze check FIX-FIRST (results/c10x_enginepath_astra_freeze_v2.md, 5 BLOCKING) folded in v2.1; confirmation FIX-FIRST (results/c10x_enginepath_astra_freeze_v21.md, 1 BLOCKING) folded in v2.2; second confirmation FREEZE (results/c10x_enginepath_astra_freeze_v22.md).** v2 history: both reviews folded (2026-10-07). Reviews folded: the advisor pass (`results/c10x_enginepath_advisor_v1.md`, FIX-FIRST, 4 BLOCKING + 9 ADVISORY) and the Codex cross-family design pass (`results/c10x_enginepath_codex_design_v1.md`, FIX-FIRST, 9 BLOCKING + 9 ADVISORY; the reviewer records its exact model ID and effort as UNVERIFIABLE, `:3`); fold log §8, reviewer conflicts §8.1, items open for the program §9. **Program ruling in force (recorded, not re-argued here):** step 6 is demoted behind step 5 (D-C10r-rulings-4 (3), `EXPERIMENT_RUNBOOK.md:331`: behind steps 1–4 and the step-5 oracle); building it model-free is authorised (D-C10r-rulings-9 (3), `EXPERIMENT_RUNBOOK.md:342`); executing it waits for the recorded reconsideration after steps 3, 4 and the step-5 oracle are read. Neither the freeze nor a favourable review launches it. Nothing has run; no code written. Decision-ID `D-C10x-enginepath`. Source lead: research pass 2026-10-06, H-11 (`results/research_pass_2026-10-06/hypotheses.md:118–120`: the queued I-1 and I-2, "no new test is proposed here"); `recommended_sequence.md:28` (step 6) and appendix `:55`; `prereg_stubs.md:69–71` (§Step 6: "the shared contract above adds the per-frame bystander probe, the decomposition readout and the two-process rule … LAW#5 isolation"), shared contract `:5–13`; the InfraNodus arc rows I-1 and I-2 (`docs/INFRANODUS_RESEARCH_ARC_2026-10-05.md:15–16`, paper table `:42`, `:48`, queue `:129`, cheapness note `:11`: "I-1 and I-2 replace or bypass `compute_z` and are science path outright"); integrated queue row 4 (`docs/INTEGRATED_QUEUE_2026-10-07.md:21`: "harness seams only, engine unmodified, LAW#5 inertness first"); ruling D-C10r-rulings-9 (3) (`EXPERIMENT_RUNBOOK.md:342`: Codex builds the step-6 driver model-free in parallel). Papers: FE — *From Backward Spreading to Forward Replay*, arXiv 2605.00358v2 (read 2026-10-07 through the arXiv tool: §3 Eq. 4–6, §4.1 Theorems 1–2 and Tables 1–2, §5, §6.1–6.2 Tables 3 and 5, App. A.1–A.5); OverTone — *Mitigating Heterogeneous Token Overfitting in LLM Knowledge Editing*, arXiv 2502.00602v2 (§2.3 Eq. 1, §3.1 Eq. 2–3 and Algorithm 1, §3.2 Prop. 3.1–3.2, §4.1, §4.4 Table 3, App. B.1). Lineage: CORPUS/36 (z reaches 0.99 on the full target, `CORPUS/36_C10_RESIDUAL_COINED_VALUES.md:28`), CORPUS/44 (P6 injection 49/72 against the edit's 13/72, `CORPUS/44_C10L_COVGEOM_SPARSEBAND.md:23`; envelope `:39`; the ρ correction `:43`), CORPUS/45 (A7-multi per-position curve, `CORPUS/45_C10L_MINT_TOKEN.md:24`), CORPUS/46 F-D1 (injection into the edited model 23/72, `CORPUS/46_C10M_DIAG_READPARTITION_EDITINJECT.md:30`), CORPUS/51 F-S2 (a changed target can move injection 51 → 69/72, `CORPUS/51_C10S_SHAREDZ.md:12`), CORPUS/53 (second key NULL-LARGE-WRITE, `CORPUS/53_C10T_SECONDKEY.md:13`). Rulings in force: D-C10k-rulings-1 (strict held-out bar), D-C10r-rulings-3 (2) write-only (`EXPERIMENT_RUNBOOK.md:330`), D-C10r-rulings-9. Conventions follow `docs/C10V_LAYERPICK_PREREG.md` (v2) and `docs/C10U_MINT2_PREREG.md` (v3), with the inertness lessons of `docs/C10S_SHARED_Z_PREREG.md` §7 A2. Every engine/harness statement below cites a line read on 2026-10-07 (LAW#4).

## 0. Where this sits, and what it is

**The e2e map (`docs/SPEC_E2E_GROUND_TRUTH.md` §C, `:22–31`; read against §F, `:64–65`).** Both arms sit inside the compile step of the write path — the per-commit solve that turns a `.larql` patch into the `.vindex` overlay mounted in Phase 2 of the commit (`:30`), placed as `docs/C10V_LAYERPICK_PREREG.md:7` places the §8.1 solve. I-2 changes *how the per-layer targets of the band are built*; I-1 changes *the objective the target vector is fit to*. Key side, layer set (4–8), covariance/projector, ridge and the read path are untouched. The bar is §F's L2 behavioural probe in its §8.9 form: held-out paraphrase, full sequence, greedy, top-1. Nothing in the read, governance or deployment layers is touched. **§0.3:** step 6 of the agreed sequence (integrated queue row 4).

**Write-only ruling, checked (`EXPERIMENT_RUNBOOK.md:330` (2); `recommended_sequence.md:11`).** Both arms stay a per-commit write derivable from the patch with no training set and no weight-training loop. I-2 = the engine's own `compute_z` (one 25-step optimisation of one hidden-state vector per fact, `memit_dry_run/memit/memit/compute_z.py:104–172`, `configs/hparams/qwen25_3b_memit_hparams.json:6`) called at layer 4 instead of 8, one deterministic forward pass, and the harness's closed-form ridge solve per layer. I-1 = the same 25-step single-vector optimisation with a different per-token loss, then the unchanged solve. The only iterative step in either arm is the one the engine already performs.

**Two premises in the brief, corrected before design.**
1. *"The write realises only about 3 % of its target at the keyed position."* Reversed. `ρ = ‖z − cur_after‖ / ‖z − cur_before‖` (`experiments/track_c/c10l_covgeom_step0.py:134`, `rel` at `:74–75`) is a fraction of residual norm **remaining**. The offline reconstruction left ≈ 0.028 canonical and 0.232 paraphrase residual (`CORPUS/44_C10L_COVGEOM_SPARSEBAND.md:25`, `:43`, the append-only correction); the later single-key behavioural run recorded 0.032650 canonical / 0.233728 held-out (`CORPUS/53_C10T_SECONDKEY.md:62`, baseline arm). Neither statistic measures the fraction of facts correctly recalled. Source pointers: step 6 is `results/research_pass_2026-10-06/recommended_sequence.md:28`, `:55`; the obsolete rationale survives at `:15` / `:28` and `results/research_pass_2026-10-06/prereg_stubs.md:75`; the historical source is not rewritten by this pre-registration. Consequence for I-2: FE's published mechanism is that backward spreading leaves a large final residual (Table 2, "Dividing": 0.96 → 0.36 remaining over layers 4–8 on Llama3-8B-Instruct; FE leaves 0.03, Table 5). **I-INFER:** the harness's ≈ 0.03 canonical remaining residual weakens a large keyed-position shortfall account in the measured configurations; it does not prove that residual size cannot affect greedy behaviour (a residual norm does not establish behaviour, `CORPUS/44:40`). What FE can change is the target layer and **which layers carry the write** (FE front-loads: 0.37 remaining after layer 4 alone, Table 5), and therefore the collateral change at non-keyed positions and on paraphrase prompts (held-out remaining residual ≈ 0.23) — the F-A3 / F-D1 confound (`CORPUS/44:31`, `CORPUS/46:30`); this package does not isolate which.
2. *"Value tokens two onward have no objective."* Not true of the target solve: `compute_z` scores **every** target token (`compute_z.py:60–65` places all target ids; `:141–150` averages their NLL), and z reaches 0.99 on the full multi-token target (`CORPUS/36:28`). What has no objective is the **weight solve at the value positions**: keys are read at the subject's last token only (`compute_ks.py:19–37`, keys at `fact_token = subject_last`, `configs/hparams/qwen25_3b_memit_hparams.json:5`; harness `c10e_bandknob.py:196–211`; the z-solve's own intervention index is the same token, `compute_z.py:68–73`). The post-write per-position weakness is real — A7-multi teacher-forced held-out hits by position 59/72, 66/72, 51/72, 19/72, 34/69, 20/39, the drop at the fourth token (`CORPUS/45:24`). Consequence for I-1: OverTone reweights the tokens *of the target objective* (Eq. 2–3); it adds no objective at the value positions of the weight solve. I-1 here tests the narrower claim "a token-reweighted target is a better target for the same write", not "the continuation gets an objective". (The value-position key was step 2, CORPUS/53: NULL-LARGE-WRITE.)

**What this experiment can and cannot conclude.** A pass advances a candidate engine-path change. A miss means *this candidate configuration was not advanced* — one hyperparameter setting per arm, one band, one seed, N = 24. The stub's "Bad: the closed-form spreading itself is the limit" (`recommended_sequence.md:28`) is not adopted as a NULL reading; a NULL joins CORPUS/37–39, 44 and 50–53 as one more write-path configuration not advanced on this harness.

## 1. Question and hypotheses

- **H-X2 (I-2, forward replay):** building the band's per-layer targets by solving z at the first band layer (4) and forward-propagating it (FE §5, App. A.3), each layer edited toward its own replayed target with the undivided residual, raises A7 held-out `para_full` over the harness's backward spreading (arm A, same process) at the same locality.
- **H-X2-null (the prior):** it does not. The canonical keyed-position remaining residual is already ≈ 0.03 in-harness, ≈ 0.23 held-out (`CORPUS/53:62`; §0 item 1 — norm fractions, not recall); FE reports benchmark experiments on LLaMA3-8B-Instruct / GPT-J / GPT-2 XL with jointly edited benchmark items under MEMIT's λC regulariser (§6.1) and an AlphaEdit extension (`results/infranodus_research_arc_2026-10-05/fulltext/ForwardReplay_2605.00358.md:56`, `:59–61`, `:100`) — its transfer to this Qwen2.5-3B, 24-fact coined-value configuration with these exact projector/cache conventions remains unvalidated; CORPUS/37–39 and 44 F-A2 moved the layer allocation six ways without a LEAD.
- **H-X1 (I-1, OverTone objective):** solving each target with OverTone's clipped forward KL to a filtered, dynamically mixed target distribution per value token (Eq. 2–3, Algorithm 1) raises A7 held-out `para_full` over the engine-objective target (arm A, same process) at the same locality.
- **H-X1-null (the prior):** it does not. The engine target is already fit (0.99, `CORPUS/36:28`) and already carries 49–51/72 by injection (`CORPUS/44:23`, `CORPUS/46:30`); the edit, not the target, loses the value (F-D1). OverTone was applied by its authors to FT-M, LoRA, MELO and WISE; ROME and MEMIT appear only as reference rows with EasyEdit defaults (§4.1; App. B.1) — the transfer to a MEMIT z-solve is this program's own and unvalidated. Against the null: CORPUS/51 F-S2 shows a changed target can move injection by +18 (51 → 69/72), so the target side is not inert.
- **H-X-tradeoff:** an arm gains but costs locality, the controls, or write size (FE's undivided first-layer residual can enlarge ΔW at layer 4; OverTone's early clip can underfit the canonical frame).

## 2. Design (engine unmodified; both arms are harness-side seams in new driver files; `c10e_bandknob.py` is not edited; the LAW#5 gates run on the untouched path and on each seam's reduction)

### 2.1 Engine and harness facts the design depends on (read 2026-10-07, LAW#4)

- **Hparams** `configs/hparams/qwen25_3b_memit_hparams.json`: `layers` [4, 5, 6, 7, 8] (`:2`), `clamp_norm_factor` 0.75 (`:3`), `fact_token` `subject_last` (`:5`), `v_num_grad_steps` 25 (`:6`), `v_lr` 0.5 (`:7`), `v_loss_layer` 35 (`:8`), `v_weight_decay` 0.5 (`:9`), `kl_factor` 0.0625 (`:10`), `layer_module_tmp` `model.layers.{}` (`:14`), tied output head `model.embed_tokens` (`:18`).
- **`compute_z(model, tok, request, hparams, layer, context_templates)`** (`compute_z.py:14–21`) solves at one layer per call; tokenises the whole target (`:41–43`); rewriting prompts = `context.format(prompt) + decode(target_ids[:-1])` over every context template, plus the KL prompt `"{} is a"` last (`:46–51`); every target id is a scored position (`:60–65`); lookup = the subject's last token (`:68–73`); `loss_layer = max(v_loss_layer, layer)` = 35 at any band layer (`:76`); one `delta` (fp32, `:83`) is added to the **block output** at `layer` at the lookup index of every prompt (`:87–101`; `target_init` from prompt 0, `:95`); Adam lr 0.5 (`:104`); per-step loss = log-softmax of `ln_f(h_35) @ lm_w + lm_b` (`:137–140`), gathered at the targets (`:141–146`), summed over target positions and divided by the target length per prompt (`:149`), mean over prompts (`:150`), plus KL (`:151–153`) and weight decay (`:154–156`); the printed "avg prob" is `exp(−nll_each).mean()` (`:162`); **stop when the total loss < 0.05** (`:164–165`) or at the step cap (`:167–168`); clamp to `0.75 · ‖target_init‖` (`:175–178`); returns `target_init + delta` (`:180`).
- **Engine MEMIT** (`memit_main.py`) solves z only at `layers[-1]` (`:101`, `:104–149`) before its layer loop (`:152`), recomputes `cur_zs` at the **z-layer** on the canonical prompt each iteration (`:160–168`), divides the residual by the layers left (`:205`), and does its float64 work on CPU (`:191–194`, `:200–203`; MPS has no float64). Context templates are sampled once per process, identity template first (`:304–323`, `:308`).
- **The harness solve** `my_edit(hp, requests, P, cache_c)` (`experiments/track_c/c10e_bandknob.py:181–221`) is the C10 write: ctx at defaults (`:182`); `z_layer = layers[-1]` (`:184`); targets from `Z_OVERRIDE` iff every `(subject, target str)` key is present and the call is not the LAW#5 check (`:185–189`, `Z_OVERRIDE_HITS` `:187–188`), else `compute_z` at `z_layer` (`:191`); per layer `i`: `K = compute_ks(...).T` (`:196`), `cur` = block output **at `z_layer`** on the canonical prompt at the subject-last token (`:197–201`), `tgt = zs − cur` (`:202`), `resid = tgt / (len(layers) − i)` (`:204`), `A = P[i](K Kᵀ + cache_c[i]) + L2·I`, `B = P[i] K residᵀ` (`:207–210`; `L2 = 1.0`, `:29`; projector from `compute_P`, `:166–178`, `NULL_THRESH = 0.005`, `:28`), `upd = solve(A, B)ᵀ` fp32 on CPU (`:211`), cast and added (`:216–217`); post-edit cache update (`:218–220`).
- **Seams and flow.** `_LAW5_DEFAULT_CTX` (`:403`), `ARM_HOOKS` (`:404`; run after each arm's evaluation with the edit applied, `:494–495`), `Z_OVERRIDE` (`:407`), `Z_OVERRIDE_HITS` (`:408`), `_ARM_STATE` (`:412`, published `:487`). `run_law5` (`:415–446`; engine `apply_memit_to_model` vs harness `my_edit` on one request; pass = `|Δexpr| < 0.05 and |Δloc| < 3`, `:444`). `run_recipe(name, hparam_path)` (`:458–509`): LAW#5 gate first (`:463`); per arm, restore and zero cache (`:473–474`), described_as baseline (`:475–476`), 24 requests on `CANON` (`:480`), **`my_edit` called by module-global name** (`:489`), `eval_arm` (`:358–400`), locality (`:492–493`). Stimuli: `CANON` (`:51`), `PTEST` (`:52–56`), `FICTION` (`:57–61`), A7 values (`:246–249`); `full_seq_match` (`:108–117`), `string_match` (startswith, `:120–130`), `teacher_forced_pertok` (`:133–143`); L1/L3 (`:259–278`), `GENERIC` (`:279–300`), `axes_post` (`:319–339`), `cov_cache_sha256` (`:342–355`); stimulus leak halt (`:568–570`).
- **Precedents reused.** Knob refusal (`c10q_stacked_arms.py:12–15`); the `CANDIDATE_NAME` import trap (`c10q_stacked_arms.py:72`); `FRAME_SUBJECTS` and `frame_probe` (`c10p_twopass_arms.py:30`, `:35–42`); P6 injection mechanics — a forward hook overwriting the block output at one index, tuple-or-tensor safe (`c10l_covgeom_p6_zinject.py:31–46`, overwrite `:38–41`; its block is bound to the z-layer at `:26–28`, so the driver needs a layer-parameterised copy) and greedy decode (`:49–56`); `fingerprint`, `subject_idx`, `compute_zs`, `z_record`, `inject_sweep` (`c10m_diag_arms.py:36–40`, `:43–44`, `:72–77`, `:80–82`, `:85–97`); the wrapper rebinding of `H.my_edit` (`docs/C10V_LAYERPICK_PREREG.md:51`).

### 2.2 Arm I-2 — forward-replay target construction (FE)

**What FE does (paper).** MEMIT optimises the hidden state at the *final* decisive layer and spreads the residual backward, `m_l = h_l + (m_L − h_L)/(L − l + 1)` (App. A.2, Eq. 15–19). FE optimises the hidden state at the *first* decisive layer by the same gradient procedure (§5; App. A.3, Eq. 20–21), then sets each later layer's target to the hidden state at the decisive position obtained by a plain forward pass with `m_1` substituted (Eq. 22–24); "with the exception of the second stage, all other components remain identical to the standard LTE method MEMIT" (§5). Per-layer edit: `Δ_l = argmin ‖Δ_l k_l − (m_l − h_l)‖²` (Eq. 14), sequential shallow to deep. Residual metric: `‖m_L − h_L^{(after l)}‖ / ‖m_L − h_L^{(0)}‖` (App. A.5).

**This harness's transcription (the driver; no engine or harness line changes).**
1. *Targets, solved on the W0-verified pristine model (§2.4) after recipe A has passed the LAW#3 gate (§2.7 step 1) and before any candidate write* (the engine's convention, `memit_main.py:104–149` before `:152`), for every arm (A1, A2, A7) and subject `c`: `rq = H.req(CANON, c, value)`; `z4 = compute_z(H.model, H.tok, rq, hp, 4, ctx)` — the engine function, unmodified, `layer = 4` (`compute_z.py:14–21`; the loss layer stays 35, `:76`; the clamp radius becomes `0.75 · ‖target_init_4‖`, `:175`); `ctx = get_context_templates(model, tok)` (the process-global list, `memit_main.py:304–323`).
2. *Forward replay* (one no-grad forward pass per value-class arm; v2): the 24 canonical prompts `CANON.format(c)` without the value, as **one ordered padded batch matching the writer's canonical `cur` call exactly** (`c10e_bandknob.py:197–201`; `memit_dry_run/memit/rome/repr_tools.py:135–147`) — the same token IDs, attention mask, padding side and subject-last index in each row. A forward hook on `model.model.layers[4]` overwrites row r at its own lookup index `idx_r = find_fact_lookup_idx(CANON, c_r, tok, "subject_last")` (`compute_z.py:234–267`) with that request's `z4` cast to the hidden dtype (P6 overwrite semantics, `c10l_covgeom_p6_zinject.py:38–41`); hooks on blocks 5–8 capture cloned outputs at `idx_r` in the same pass. The layer-4 target is the **unrounded** fp32 `z4`, not its fp16 hook image. Targets are stored fp32 as a dict keyed by actual layer integer, `FE_TARGETS[(subject, target str)] = {4: z4, 5: m5, 6: m6, 7: m7, 8: m8}`, never a list; row identities, token tensors and the layer-keyed table are SHA-256-hashed per arm. The canonical absolute overwrite is the chosen FE transcription. Its equivalence to the target solve's additive `delta` (`compute_z.py:95`, `:180`; the canonical prompt under the identity template is prompt 0 of the solve, `memit_main.py:308`) is mathematical only for the same underlying pre-intervention activation; equality across the different fp16 batches (the solve's teacher-forced padded batch, `compute_z.py:46–57`, against the 24-row canonical batch) is not assumed. The solve's `target_init` against the canonical replay's initial activation, with their shape/context identity, is recorded as a diagnostic, and no reduction tolerance is widened to hide that difference. Only the canonical prompt is replayed because the harness reads `cur` on the canonical prompt only (`c10e_bandknob.py:197–201`). Single-request observations are recorded separately and never compared with 24-row outputs under a same-shape gate.
3. *The write* (`fe_edit(hp, requests, P, cache_c)`, a driver function authored line for line from `my_edit:181–221`, with exactly three changes): (a) the per-layer target `M[layer]` = the stacked `FE_TARGETS[(subject, target str)][layer]` from a strict table keyed by exact request identity and by actual layer integer (never list position; `fe_edit` asserts `set(FE_TARGETS[key]) == set(hp.layers)`) — a missing key or layer raises (HALT), unlike `Z_OVERRIDE`'s silent fallback (`:186`); (b) `cur` is read at **`layer`** instead of `z_layer` (`:197–201` with `z_layer → layer`; the same engine function `get_module_input_output_at_words`, the same canonical prompts, `module_template = hp.layer_module_tmp`); (c) `resid = tgt` — **no division** (`:204` replaced; FE gives each layer an accurate target, Eq. 14). Everything else verbatim: `compute_ks` keys (`:196`), `repeat_interleave` (`:203`), projector `P[i]`, cache, `L2`, the fp32 CPU solve, cast and in-place add (`:205–217`), the post-edit cache update (`:218–220`), the `delta_norms` record (`:213–215`). After each layer's update the wrapper records `ρ_FE(l) = ‖m_8 − cur_8‖ / ‖m_8 − cur_8^{(0)}‖` at the canonical keyed position (`cur_8` read as `:197–201` at layer 8) — FE's Table 5 metric.
4. *Seam mechanism.* The driver rebinds `H.my_edit = dispatch`; `dispatch(hp, requests, P, cache)` delegates **unchanged** to the original `my_edit` whenever `FE_STATE is None` or `H._LAW5_DEFAULT_CTX` is True, else calls `fe_edit`; both recipe states are therefore assigned explicitly before every recipe (§2.7 step 1 and step 5). `run_recipe` reaches it through the global name (`:489`); `run_law5`'s own call (`:433`) runs with `_LAW5_DEFAULT_CTX = True` (`:430`) and so takes the original path. `FE_CALLS` counts `fe_edit` calls. `fe_edit` takes a frozen mode enum `{"fe", "identity"}`; `"identity"` (targets = `zs` at every layer, `cur` at `z_layer`, `resid = tgt / (len − i)`) exists only for inertness check X2-(iii) and is refused inside any recipe; it switches all three FE changes off and so validates only the lines `fe_edit` shares with `my_edit` — the FE-specific lines are validated in `"fe"` mode by X2-(vi), X2-(vii) and G8 (§2.4).
5. *Departures from the paper, stated.* FE uses MEMIT's λC regulariser (Eq. 4–5); here the harness's null-space-projected ridge solve applies unchanged. FE edits 2,000 items jointly (§6.1); here 24 per arm. FE does not say whether `h_l` is read before or after the earlier layers' edits; the engine convention (recompute after the earlier edits, `memit_main.py:160–169`) is used, which is what lets FE's remaining residual "halve per layer".

### 2.3 Arm I-1 — OverTone objective for the target solve

**What OverTone does (paper).** It replaces each token's cross-entropy (Eq. 1) by `max(D_KL[π_tar^{(i)} ‖ π_θ^{(i)}], ε)` summed over the value tokens (Eq. 2), with `π_tar^{(i)} = λ δ_{y_i} + (1 − λ) π_flt^{(i)}` if `y_i` is that mixture's argmax, else `δ_{y_i}` (Eq. 3); `π_flt` = softmax of the current logits after the top-nσ filter `s_k ≤ s_max − n·std(s) → −∞` (Algorithm 1, lines 7–9), recomputed every step (line 10, "dyn"); the clip is a token-level early stop (§3.1). It reduces to CE at `ε = 0, λ = 1` (Prop. 3.1); its extra cost is O(|V|) per token (Prop. 3.2). Ablation (§4.4, Table 3, LoRA on ZsRE): removing the clip, the dynamic target, the argmax check or the filter each lowers the average.

**This harness's transcription.** `compute_z_overtone(model, tok, request, hparams, layer, context_templates, lam, eps, n_sigma)` in `experiments/track_c/c10x_overtone_z.py`, authored from a `cat -n` of `compute_z.py` (LAW#4): lines `:28–140` and `:151–185` copied verbatim (prompts, lookup, delta hook, Adam, KL term, weight decay, total loss, print, the **engine's stopping rule verbatim** — total loss < 0.05 or 25 steps — clamp, return); only the reduction `:141–149` is replaced:
- `ce` = the engine's gathered negative log-probabilities, computed exactly as `:141–145` in the engine's dtype;
- Compute `raw_logits = ln_f(full_repr) @ lm_w + lm_b` once in the engine dtype, then `log_probs = torch.log_softmax(raw_logits, dim=2)` exactly as the engine. Factoring line 140 to name this intermediate changes no arithmetic. Construct detached targets from `raw_logits[scored_mask].detach().float()`. In `extra`, use the differentiable `log_probs[scored_mask].float()`; cast the completed extra term once to `ce.dtype` before addition and clipping. Do not recompute a fp32 head projection or fp32 log-softmax for the optimization objective. The independent audit reproduces these operations and casts.
- per scored position (prompt p, position t, label y), under `no_grad`: logits `s = raw_logits[p, t].detach().float()` (§2.3 `raw_logits` bullet); keep = `s > s.max() − n_sigma · s.std()`; `π_flt` = softmax over the kept entries; `cand = lam · onehot(y) + (1 − lam) · π_flt`; `π_tar = cand` if `argmax(cand) == y` else `onehot(y)`; all detached;
- `extra = Σ_v xlogy(π_tar, π_tar) − Σ_v (π_tar − onehot(y)) · log π_θ` (with `log π_θ` = `log_probs[scored_mask].float()`; cast once to `ce.dtype`), so that `ce + extra = D_KL[π_tar ‖ π_θ]` and `extra ≡ 0` exactly when `π_tar = onehot(y)`;
- `tok_loss = torch.where(ce + extra > eps, ce + extra, eps)` (v2: the constant branch at equality; see the clip-boundary bullet below); `nll_loss_each = (tok_loss · mask).sum(1) / target_ids.size(0)` (the engine's per-prompt mean over tokens, `:149`; the paper sums, Eq. 2 — the mean keeps the engine's balance against KL and weight decay); `nll_loss = nll_loss_each.mean()` (`:150`).
- **Settings (pre-registered):** `lam = 0.1`, `n_sigma = 0.5`, `eps = 0.01` — the paper's FT-M row (App. B.1; LoRA uses ε = 0.05, MELO and WISE n = 1). FT-M, which "fine-tunes a special layer identified by causal-tracing analysis" (§4.1), is the closest of the four to a locate-then-edit target. With ε = 0.01 the clipped mean has floor 0.01, so the engine's 0.05 stop can still fire; steps used are recorded per request.
- **Vectorised** over positions (Algorithm 1 notes the inner loop is parallel); no float64 tensor on MPS (the CORPUS/53 first-attempt halt).
- **Masking and branches (v2).** The OverTone target and KL are constructed only for scored rewriting positions (`rewriting_targets != −100`, `compute_z.py:59–65`; rewriting rows only, `:137–139`), excluding padding and the separately handled KL-prompt row; masking happens before filtering and KL arithmetic, never as a final multiply. Logits are checked finite and the filter's keep-set non-empty before the softmax; an empty keep-set (e.g. all-equal logits: std = 0 under the strict inequality) HALTs with the offending vector. Zero-probability entropy contributions are defined as zero without evaluating log(0) on those entries. Mixture-skipped positions use the original CE value with an exactly-zero extra term; the unused mixture-loss expression is not evaluated for them. Finite scored losses are scattered back into an explicitly zero padded tensor before the engine's mean. The `ce` term is the literal engine arithmetic of `:141–149` inside the copied solver (no delegation of the solve to the engine, no change to its graph or reduction order), and no `lam`- or `eps`-specific code path exists, so X1-(ii) exercises the active branch (at `lam = 1` every `π_tar` is one-hot and `extra` is exactly 0).
- **Clip boundary and gradient (v2, frozen transcription).** `tok_loss = torch.where(kl > eps, kl, eps)` with `kl = ce + extra`: the constant branch at equality, so the gradient at `KL = eps` is zero whatever a library clamp's boundary convention. With detached `π_tar`, the analytic logit gradient of a scored token is `softmax(s) − π_tar` for KL > eps and zero for KL ≤ eps, scaled by the declared token/prompt means; the skip branch gives the original CE gradient; no gradient reaches `π_tar`, and none originates at padding or KL-prompt positions through the token objective. Implementation conventions frozen now: standard deviation with correction = 1, the strict keep inequality `s > s.max() − n_sigma · s.std()`, the first-index argmax tie rule.
- **Seam:** the driver solves the 72 OverTone targets (A1, A2, A7 × 24, `layer = 8`, same `ctx`) before the recipe and supplies them through `Z_OVERRIDE` keyed `(subject, " " + value)` (`c10e_bandknob.py:97`, `:185–189`); `Z_OVERRIDE_HITS` must equal 3 in this recipe; the override is never consulted in the LAW#5 check (`:186`). Spreading, keys and the layer solve are unchanged.
- **Departures, stated.** The paper fine-tunes parameters with OverTone; here it fits one hidden-state vector per fact over six context prompts plus the KL prompt. A fit at stop below the engine's 0.99, and an earlier stop, are an **I-INFER prediction** (the mixture target puts mass 0.1 + 0.9·π_flt(y) on y once y leads), not assumed: they are tested by the recorded per-token `π_θ(y)` at stop, the steps used and the stopping reason (total loss < 0.05, or the step cap) per request. The 0.98 fit screen of §2.5 does not apply to I-1. The tested object is the OverTone-inspired target package as a whole — dynamic detached token targets, filtering, clipping, the retained KL and weight-decay terms and the engine's total-loss stopping rule — and no component is attributed; a CE control matched in stopping or fit would need its own pre-registration.

### 2.4 Inertness (LAW#5), numeric — any failure → HALT before any write arm

**Tolerance rule (C10S §2; `docs/C10V_LAYERPICK_PREREG.md:58`; v2 bounded):** the floor is measured with the same inputs, batch/padding shape, context order, weights, cache, dtype and arithmetic as the quantity compared. For a non-zero reference `a`: relative L2 `‖a − b‖₂ / ‖a‖₂` on detached CPU fp32 copies, max-abs recorded; `tol = max(10 × floor, 1e-4)` **and `tol ≤ 1e-4` is required, i.e. floor ≤ 1e-5; a larger floor HALTs before any parity check** (diagnose the observation layer; never widen acceptance). Relative error ≤ 1e-4 passes. A zero reference is compared for exact equality (no divide-by-zero NaN, no fall-through); every finiteness check is explicit. Cross-batch distances and cross-process variation are diagnostics, never floors for these same-shape gates. No tolerance is calibrated from a candidate result. **Lesson carried from C10S §7 A2:** fp16 kernels round differently across batch shapes and the 25-step optimisation amplifies it (rel 0.122 there); every parity check below therefore compares *identical batch shapes and identical arithmetic*, so the expected distance is 0.0 and the floor rule applies.

- **W0 pristine-weight identity (all cells; v2).** Immediately after loading the unedited model the driver takes one immutable `PRISTINE` snapshot of the five rewrite-module weights (`model.layers.{4..8}.mlp.down_proj.weight`, `rewrite_module_tmp`, hparams `:13`) and records the SHA-256 of each tensor's dtype, shape and contiguous raw bytes. Every standalone write check restores those tensors from `PRISTINE` in a `finally` block and uses a fresh zero cache; replay and injection hooks are removed in `finally` blocks as well. The hashes are verified before recipe A, before target construction, before injection, before every standalone write check and each candidate recipe, after every restoration and after the final recipe. A mismatch or a leftover intervention hook HALTs before the next cell (diagnostic: the checkpoint, the cell, the offending layer). A recipe-local entry snapshot (`run_recipe`'s `base_snap`, `:461`) is not a second authority for "pristine".
- **G (every recipe).** The standing harness gate `run_law5` (`:415–446`; engine `apply_memit_to_model` against `my_edit` on Zorbland → Cairo; `|Δexpr| < 0.05 and |Δloc| < 3` after rounding to four and two decimals, `:440–444`; equality at 0.05 or 3 fails; raw differences recorded) INERT inside every `run_recipe` call (`:463`). During it `FE_STATE` / `Z_OVERRIDE` may remain set; the original path is taken because `_LAW5_DEFAULT_CTX` is True (`:430–435`), tested by `my_edit` (`:186`) and by `dispatch`, which reads `H._LAW5_DEFAULT_CTX` at call time (never a copy taken at import) and delegates to the saved original `my_edit`. G must reach no candidate seam: a candidate-seam call during G HALTs.
- **G8 direct engine reference for the active FE path (v2).** Active singleton FE (`hp1.layers = [8]`; the real FE builder and writer in `"fe"` mode, not `run_law5`'s default-dispatch bypass) against unmodified `apply_memit_to_model` on `hp1`, from the same W0-verified pristine state, with the same context list and the single canonical Zorbland → Cairo request; W0 restored and verified between sides. Pass = the Cairo next-token probability and the `described_as` locality score within G's limits under G's rounding (equality fails); complete distributions and top-1 IDs recorded. This is a behavioural engine-output check, not an assertion of exact engine ΔW equality (the harness solves a projected ridge-1 system in CPU fp32, the engine a covariance-regularised system in CPU float64: `c10e_bandknob.py:205–217`, `memit_main.py:191–206`, hparams `:12`); a G8 failure HALTs and is not excused by the different regularisers.
- **X1-(i) solve floor.** The engine `compute_z` three times for one request (Zorbland, its A7 value) on the same `ctx`; floor = the largest pairwise distance.
- **X1-(ii) reduction parity (Prop. 3.1).** `compute_z_overtone(lam = 1, eps = 0)` against the engine `compute_z` on all 72 requests (A1, A2, A7 × 24), same `ctx`, same process: X1-(ii) passes iff every nonzero-reference returned-z relative error is ≤1e-4, the measured floor is ≤1e-5, and step counts agree exactly. Zero references require exact equality. An exactly-zero engine CE receives the declared constant clip branch; any resulting difference is judged by these same predicates. Bit-exactness is an expectation, not a separate acceptance requirement or a proven consequence of the algebra.
- **X1-(iii) active-path structure (the C10S (iv) lesson: identical prompts cannot catch an index bug; v2: full vocabulary).** For two requests (Zorbland A7, Zorbland A1) at step 0 (`delta = 0`) and at the final evaluated step, the solver saves detached **full-vocabulary, unrounded** pre-softmax logits for every scored rewriting position (vocabulary 151,936; a top-64 view is display-only), the actual engine log-probabilities / CE values, target IDs, position/row maps, dtype and mask, in a lossless CPU binary file with its SHA-256. An independent reference in the reader (Eq. 2–3 and Algorithm 1 lines 7–11, written from the paper text, no code shared with the solver) recomputes from these full inputs the keep-mask, `π_tar(y)`, the mix/skip decision and `tok_loss`, under the frozen conventions of §2.3 (std correction = 1, strict keep inequality, first-index argmax ties) and following the declared intermediate casts and reduction order (never an ideal fp32 KL against a rounded fp16 `ce + extra`). Pass: keep-masks and mix/skip decisions identical; `tok_loss` within 1e-4 relative error with denominator `max(|reference_loss|, eps, 1e-12)`, absolute error recorded; the ideal fp32 KL is reported as a diagnostic, never as the acceptance reference. Selftest positive controls (model-free): a logits vector where y is the top token (the mixture applies) and one where it is not (skip), both matching hand-computed values; and a pair of vectors sharing their top 64 but differing in the tail, which the independent audit must distinguish in filter and loss.
- **X1-(iv) write parity.** `my_edit` with `Z_OVERRIDE` = the X1-(ii) reduced targets against `my_edit` with `Z_OVERRIDE` = the engine targets, A7 24 requests, identical restored weights, `P`, cache and `ctx`: every per-layer ΔW within the X2-(ii) tolerance.
- **X1-(v) objective gradient and boundaries (model-free selftest, CPU fp32; v2).** With fixed synthetic logits and a detached `π_tar`, the solver's token-loss gradient equals the analytic `softmax(s) − π_tar` for KL > eps and zero for KL ≤ eps, scaled by the declared token/prompt means; the skip branch equals the CE gradient; max-absolute error ≤ 1e-6 away from filter/mix ties, the equality branch tested exactly. No gradient reaches `π_tar`; none originates at padding or KL-prompt positions through the token objective. Synthetic controls: mix, skip, clipping, uniform-logit empty support (must HALT), exact filter equality, argmax ties, and differently masked / variable-length rows. This does not replace X1-(ii)'s 72-request returned-z / step-count test.
- **X2-(ii) write floor.** The original `my_edit` twice from identical restored weights, targets pinned through `Z_OVERRIDE` (engine z_8), A7 24 requests; floor = the largest per-layer `‖ΔW_a − ΔW_b‖ / ‖ΔW_a‖`; differences in `canon_full_n` and `para_full_n` recorded.
- **X2-(iii) identity mode.** `fe_edit(mode = "identity")` against the original `my_edit` on identical weights, `P`, cache, `ctx` and pinned targets, A7 24 requests: every per-layer ΔW within tolerance. By-product recorded, not gated: arm A's per-layer remaining ratio `ρ_A(l) = ‖z_8 − cur_8‖ / ‖z_8 − cur_8^{(0)}‖` — the harness analogue of FE's Table 2 "Dividing" row. v2: identity mode switches all three FE changes off, so this check validates only the lines `fe_edit` shares with `my_edit`; the FE path is gated by X2-(vi), X2-(vii) and G8.
- **X2-(iv) replay is the harness's own reading (v2: matched batch shapes on both sides).** For all 72 requests and layers 4–8 on the W0-verified pristine model, per value-class arm in the writer's 24-row padded canonical batch (§2.2 step 2): (a) the un-overwritten 24-row replay captures equal the original engine reader `get_module_input_output_at_words(model, tok, l, [CANON]*24, <the arm's 24 subjects in request order>, hp.layer_module_tmp, "subject_last")[1]` (the `cur` reader, `:197–201`) on **those same 24 rows**, at every band layer, under the bounded tolerance (floor = two plain calls of that function in the same shape); (b) overwriting block 4 in each row at its own index with that row's own output captured from the same batch reproduces the un-overwritten outputs at 5–8 within the same tolerance. Single-request observations may be recorded separately but are never compared with 24-row outputs under a same-shape gate; any singleton diagnostic is checked against a singleton reference.
- **X2-(v) indices.** `find_fact_lookup_idx(CANON, c, tok, "subject_last")` equals `subject_idx(CANON, c)` (`c10m_diag_arms.py:43–44`, the injection index) for all 72 requests; exact.
- **X2-(vi) non-zero active singleton reduction (v2).** In-memory `hp1` differs from the band hparams only by `layers = [8]`; `P1 = [P_8]`, the layer-8 projector from the same verified covariance (`compute_P`, `:166–178`); a zero cache; the same ordered 24 A7 requests. The **actual FE target builder** runs with first and last layer both 8, using unmodified `compute_z(..., layer = 8, ctx)`, and retains the returned fp32 `z_8` as `FE_TARGETS[(subject, target str)][8]` (not its fp16 hook image); with no later layer, replay adds no target. (1) Every built target equals an independently obtained engine `z_8` with identical request, prompt/context list, padding shape, dtype and stopping rule, within the bounded tolerance. (2) From `PRISTINE`, the actual `fe_edit(mode = "fe")` is compared with the saved original `my_edit(hp1, …)` with `Z_OVERRIDE` pinned to those same engine targets — exercising the active table lookup, the layer-local reader and the undivided residual; the identity branch is not called. Compared: the **complete pre-cast ΔW_8 tensor** and the updated cache (relative L2 ≤ 1e-4, max-abs recorded) and the applied fp16 weight tensor (exact); the reference update must be non-zero. Both results are evaluated on the same 24 canonical and 72 held-out prompts and the per-prompt greedy correctness flags must agree exactly (equal aggregate counts alone are insufficient). W0 restored and verified between sides. This validates exact reduction to the unchanged target primitive and the harness writer; it is not an engine-ΔW equivalence (G8 is the engine reference).
- **X2-(vii) active multi-layer null and structure check (v2).** For the production band [4, 5, 6, 7, 8], identity replay targets are built by overwriting block 4 at each row's index with its own pristine output in the same 24-row padded canonical batch the writer uses (as X2-(iv)(b)) and capturing 5–8; these per-subject, per-layer vectors are used in actual `fe_edit(mode = "fe")` from `PRISTINE`. Every residual `M_l − cur_l` and every update must be exactly zero tensors (relative error is undefined for a zero reference), and the five weight hashes must stay pristine. Targets are dicts keyed by actual layer integers with exact `(subject, target str)` identities. An independent same-batch block-output observer (a hook outside `fe_edit`) checks the full `cur_l` vector at every layer — not its norm, not a self-reported layer number — together with the exact request/column order and `resid = M_l − cur_l` before the fp32 CPU solve. Model-free negative controls: a wrong-layer read and a permuted target table must each fail this check. No candidate target is substituted until X2-(vi), X2-(vii) and G8 pass. Consequence, stated: any non-zero X2-(iv)(a) distance, even one within tolerance, makes the exact-zero requirement unmeetable and HALTs the process (§9 item 4).
- **Counters (audit, not inertness; v2).** `H.Z_OVERRIDE_HITS` and `FE_CALLS` are reset to 0 immediately before each `H.run_recipe` and read immediately after it; required exact pairs A = (0, 0), I-2 = (0, 3), I-1 = (3, 0). Standalone X-checks keep separate counters. A candidate-seam call during G, a silent missing-target fallback or a recipe counter mismatch HALTs. `REPRODUCIBILITY.md` concerns cross-process identity and does not excuse these same-process checks.

### 2.5 Diagnostics recorded in the pass (no label depends on them except the two named qualifiers; predictions stated now)

- **Fit at stop.** Engine z_8 and z_4: the engine's printed avg prob of the final evaluated step (`compute_z.py:162`, captured from the redirected stdout) per request. **I-2 fit screen:** z_4 ≥ 0.98 on ≥ 22/24 A7 facts (the C10U P3 admission convention, `docs/C10U_MINT2_PREREG.md:72`), else the I-2 label carries **-UNDERFIT** and cannot pass gate A. I-1: per-token `π_θ(y)` at stop for every position (no screen, §2.3).
- **Injection screen (A7 only, unedited model, one process; `inject_sweep` mechanics, `c10m_diag_arms.py:85–97`, with a layer-parameterised hook):** z_8 at layer 8 (the reference; known 49–51/72, `CORPUS/44:23`, `CORPUS/46:30`); z_4 at layer 4; z_8^OT (I-1) at layer 8. Counts canon /24 and held-out /72, per template. **Rule for I-2:** if inject(z_4 @ 4) ≤ inject(z_8 @ 8) − 10/72, a NULL on I-2 is written **NULL-TARGET-WEAKER** (the layer-4 target is weaker than the layer-8 one before any write, so this NULL does not isolate spreading; the full deficit partition is §3's NULL table). **Rule for I-1:** a difference |inject(z_8^OT) − inject(z_8)| < 6/72 is not interpreted (C10S's screen size; its same-process noise twin moved +3, `CORPUS/51_C10S_SHAREDZ.md:1`).
- **Residual ratios at the canonical keyed position.** `ρ_FE(l)` for l = 4..8 (I-2, §2.2 step 3) against `ρ_A(l)` (X2-(iii)); end-of-write `‖t − cur_after‖ / ‖t − cur_before‖` at layer 8 for every arm of every recipe (t = z_8 for A, z_8^OT for I-1, m_8 for I-2; the C10S A1 readout, `docs/C10S_SHARED_Z_PREREG.md:69`), A1 beside A7 so that a realisation-in-norm reading can be overturned; `‖m_8 − z_8‖ / ‖z_8 − cur_8^{(0)}‖` (how far FE's endpoint lies from the backward-spread target). *Predictions written now:* `ρ_A(8)` ≈ 0.03 (consistent with step 0's 0.028 and the in-harness 0.0327, `CORPUS/53:62`); `ρ_FE(4)` < `ρ_A(4)`; both end ratios ≤ 0.1 — installation-in-norm will not separate the arms, and only the behavioural count can.
- **Per-layer ΔW Frobenius norms** (`delta_norms`, `:213–215`) per arm. **I-INFER prediction, written now so that a -LARGE-WRITE on I-2 is not read as a surprise:** the undivided first-layer residual may concentrate and enlarge the layer-4 write relative to A's layer-4 ΔW (fed 1/5 of the residual, `c10e_bandknob.py:204`) and may produce -LARGE-WRITE; this is measured, not inferred from a band-end remaining ratio.
- **Per-position teacher-forced curve** on the 72 held-out prompts, position j = 0..n−1 (j = 0 is `para_first`), A7, every recipe (comparator `CORPUS/45:24`). *Prediction for the arc's I-1 reading:* if reweighting the per-token objective of the target changes how the written value continues after the write, the teacher-forced counts at positions ≥ 3 may change relative to A; each numerator is recorded with its actual denominator; reported, not gated, and not the binding free-generation metric.

### 2.6 Controls and probes (every recipe)

A1 single-token and A2 prior-coherent two-token values under every recipe, with that recipe's own method (OverTone targets and FE targets for A1 and A2 too: a per-commit method must serve every value class a commit can carry). Locality per the shared contract (`prereg_stubs.md:10`): L1 real-country flips (12, `axes_post` `:327`), L3 unedited-capital top-1 agreement (30, `:332`), `described_as` (`:475–476`, `:492`), generic perplexity (`:315`, `:337`), and the same-frame fictional probe over the six never-edited `FRAME_SUBJECTS` (`c10p_twopass_arms.py:30`, `:35–42`) in each recipe's A7 arm and in **every realised rewriting frame** `context.format(CANON)` from the exact same-process context list, the canonical identity frame included (v2: both target solves fit every context template, `compute_z.py:46–50`, `memit_main.py:308–319`; the shared contract requires a separately counted gate in every fitted frame, `prereg_stubs.md:10`; the existing helper hardcodes the canonical frame and is generalised over frames with unchanged semantics — top-1 membership in the frozen A7 first-token set). Frame texts and their hash are frozen and recorded before any candidate data; counts are per frame (flips /6 each), never pooled, with pristine counts and row IDs beside them. The `"{s} is a"` KL prompt remains objective-anchored and diagnostic, not a held-out frame; no held-out test frame is ever added to the solve. Relation-label probes on the 24 edited subjects, top-1 on the pristine model (once per process) and post-edit in the A7 arm: `"{s} is associated with"` (bystander) and `"{s} is a"` (labelled **objective-anchored**: it is the solve's KL prompt, `compute_z.py:50`); flips counted, no threshold. All probes are read-only driver hooks on `ARM_HOOKS`.

### 2.7 Cells, processes, compute

**Process 1 (one GPU job; the autoresearch loop paused; the operator's go, after the recorded reconsideration of the status line):**
0. Fingerprint `d941a9fb…` and `_cov_cpu == 3` (`c10m_diag_arms.py:36–40` → `tools/engine_fingerprint.py`); refuse inherited knobs (`c10q_stacked_arms.py:13–15`); `LLMDB_ROOT` set explicitly to this worktree (the shell profile points it at the main checkout); `C10_ARMS = A1_single,A2_coherent2,A7_coined_coined` set before importing the harness; import `c10e_bandknob` first and `c10p_twopass_arms` after it (that import rewrites `CANDIDATE_NAME`, `c10q_stacked_arms.py:72`); stimulus base report and leak check (`:449–455`, `:568–570`); the W0 `PRISTINE` snapshot and hashes (§2.4).
1. **Recipe A first, then the in-driver LAW#3 gate (v2).** `H.run_recipe` for **A** with `(FE_STATE=None, H.Z_OVERRIDE=None)` (original path, its own z solve, G inside), with A1, A2, A7 and the full readout of step 5. Immediately the driver applies the LAW#3 predicate of §3 (A7 `5 ≤ para_full_n ≤ 18` /72, `5 ≤ canon_full_n ≤ 10` /24, `42 ≤ para_first_n ≤ 59` /72; A1 and A2 each `para_full_n ≥ 68` /72; denominators verified; endpoints inclusive; `CORPUS/44:39`). On a miss it records A and a HALTED/INVALID diagnostic (§5), exits non-zero and executes no candidate target solve, replay, candidate injection or candidate write; baseline-only halted records never become candidate NULLs. The reader re-checks the same predicate.
2. Targets (only after step 1 passes): engine z_8 (72; the injection reference and the X-check references), engine z_4 (72) and the 24-row replay, OverTone z_8^OT (72); hashes, fits, steps, stopping reasons, norms.
3. Inertness: W0 throughout; X1-(i)–(v), X2-(ii)–(vii), G8 (G runs inside each recipe). Any failure → HALT.
4. Injection screen (§2.5).
5. Candidate recipes: `H.run_recipe` for **I-2**, then **I-1** — immediately before every recipe, explicitly assign both states: A = `(FE_STATE=None, H.Z_OVERRIDE=None)`; I-2 = `(FE_STATE=the frozen FE state, H.Z_OVERRIDE=None)`; I-1 = `(FE_STATE=None, H.Z_OVERRIDE=the frozen OverTone table)`; reset both recipe counters then; restore both states to `None` in `finally`, including after standalone checks, and verify W0 before proceeding — each, like A, with A1, A2, A7, the full readout (`para_full_n`, `para_string_n`, `canon_full_n`, `para_first_n`, `tf_pertok_cont`, `cond_full_given_first`, the per-fact 24-vector, per-template counts, the per-edge rule 3/3), locality, probes and diagnostics. Order fixed A → I-2 → I-1; weights are restored per arm (`:473`) and W0-verified before and after each recipe.

**Process 2 (gate A), only if at least one arm is replication-eligible (§3: base class LEAD or PARTIAL with neither -LARGE-WRITE nor -UNDERFIT; eligibility decided before launch):** the same driver, a fresh process, a fresh `OUT_DIR`, everything rerun in the same order — recipe A and its in-driver LAW#3 gate first (context templates resample per process, `CORPUS/44:32`; the template hash and the frame texts are recorded in both). Both candidate recipes may be recorded, but only arms eligible in process 1 can be advanced; a favourable process-2-only arm is exploratory.

**Compute (this Mac; v2: the evidence and table below are planning estimates; v2.1: the hard caps follow the table).** Evidence: a three-arm recipe ≈ 26–30 min after removing the measured stacked extras (2031 − 466, 1826 − 174, 1877 − 132 s = 26.1 / 27.5 / 29.1 min, `results/c10q_stacked/logs_run.log:41`, `:52`, `:71`, `:82`, `:101`, `:112`); 34 min is kept as a conservative planning allowance, not a measurement. One engine `compute_z` ≈ 7 s (three solves in 21 s for one request, `results/c10s_sharedz_logs/inertness.log:9`), so 216 target solves ≈ 25.2 min and 72 reduction solves ≈ 8.4 min by extrapolation; class-dependent stopping, the active OverTone vocabulary operations and the instrumentation are unmeasured.

| Cell | Planning allowance | Evidence status |
|---|---:|---|
| A, I-2 and I-1 recipes together | 78–102 min | extrapolated from the measured 26–29 min recipes; the candidate recipes are unrun |
| 216 target solves plus replay | 25–40 min | 25.2 min solve extrapolation; v1 allowance; active overhead unmeasured |
| W0, reduction / identity / null gates, G8 and other inertness | 35–50 min | planning allowance; 8.4 min reduction-solve component |
| Three injection screens | 20–25 min | the C10S figure (≈ 8 min per injected target set); the C10X cost unmeasured |
| **Subtotal** | **158–217 min (2.6–3.6 h)** | excludes the unmeasured full-logit audit and hashing overhead |

**Hard stage caps (v2.1).** Hard wall-clock caps, in minutes: setup/import/preflight 10; recipe A 34; target construction 40; inertness and independent audits 50; injection 25; I-2 recipe 34; I-1 recipe 34; final verification/serialization 13. Every operation, including hashing, restoration and diagnostic capture, belongs inside its stage cap. Each process is capped at 250 minutes; two processes at 500 minutes. Before starting each stage, record its projected duration. Initially use its stated cap; when comparable timings exist, use the larger of that allowance and the projection from the slowest measured comparable work units, including remaining overhead. Refuse the stage if its projection exceeds its cap or the remaining process budget after reserving subsequent stages. Recheck before each work unit. An independent watchdog enforces stage and process deadlines, including blocked native calls. Projection refusal or timeout yields HALTED/incomplete, never NULL; no subsequent stage runs and no cap is extended in-run. Process 2 uses the same rules and incorporates process-1 measured timings.

3–3.5 h per process is a plausible target, not validated wall time; v1's "worst case ≈ 7 h" is withdrawn. A LAW#3 miss ends the process after recipe A (≈ 30 min), before any candidate spend; process 2 repeats the full gate sequence and runs only under the eligibility predicate. No optional mechanism-control recipe is included. Runtime or resource exhaustion gives HALTED/incomplete, never a scientific NULL. Model forwards on MPS in fp16, detached objective work in explicit fp32, any float64 on CPU only; model jobs serialised; peak unified memory is measured before the full estimate is accepted (I-INFER allocation scale: one square fp32 11008-wide projector or cache ≈ 462 MiB, five of each ≈ 4.5 GiB before weights and solve temporaries); cell-local projectors and audit buffers are released, not copied. Measured wall-clock per cell goes in the record.

### 2.8 Records and code

Output `results/c10x_enginepath/{targets,inertness,inject,pass1,run}.json` (process 2: `results/c10x_enginepath_r2/`); logs `results/c10x_enginepath_logs/`. Code: driver `experiments/track_c/c10x_enginepath_arms.py` (FE replay, `fe_edit`, `dispatch`, probes), solver `c10x_overtone_z.py`, inertness `c10x_enginepath_inertness.py`, reader `c10x_enginepath_read.py` (**encodes every gate and label of §3**; a run is labelled only by the reader), selftest `c10x_enginepath_selftest.py`. Every record carries: the source commit and the SHA-256 of every declared source file (the CORPUS/51 pattern), the fingerprint output, the hparams file hash, the covariance cache hashes (`:342–355`), the context-template list and its hash, the three target tables' hashes (the `z_record` convention, `c10m_diag_arms.py:80–82`), the OverTone settings, `FE_CALLS` and `Z_OVERRIDE_HITS`. v2 additions: a distinct run/process identity and timestamps; the model ID and revision (pinned by the loader, `c10e_bandknob.py:25–26`, `:45–48`) and the tokenizer artifact hashes; software/device/dtype identity; the W0 pristine-weight hashes and every checkpoint; the frozen pre-registration's SHA-256; the ordered stimuli; the frame texts and their hash; the full-logit audit files and their hashes; source-file hashes verified at start and at end. Existing output artifacts are refused — earlier results and manifests are never overwritten. The reader combines processes only if scientific configuration, source, weights, stimuli and pre-registration hash match, with only the sampled context list and the resulting targets and frames allowed to differ; same-file or same-process reuse is not replication. Reviewer model and effort are recorded as actually run, or UNVERIFIABLE when they cannot be authenticated.

## 3. Pre-registered readings (exact counts; decision order fixed; each arm read separately against arm A of the same process; v2: one total classification)

**Decision order:** validity → LAW#3 (in the driver, before any candidate work) → controls → count class → locality → base class → qualifiers → replication eligibility → replication → interpretation.

**Validity (any failure → INVALID for the whole process; HALT per §5; no scientific classification):** fingerprint `d941a9fb` and `_cov_cpu == 3`; W0 at every checkpoint; G INERT in all three recipes with no candidate-seam call during G; G8; X1-(i)–(v) and X2-(ii)–(vii) pass; every measured floor ≤ 1e-5; stimulus leak ≤ 15 % (`:568`: at most 3 of 24 per arm, 4 fails); counters as in §2.4; every record and hash of §2.8 present; every required field is present and every applicable numeric datum is finite; preserve `tf_pertok_cont=null` iff its recorded continuation-token denominator is zero, and `cond_full_given_first=null` iff `para_first_n=0`, recording an explicit zero-denominator reason; these diagnostic nulls do not invalidate an arm; any other missing value, unexpected null, NaN or Inf is INVALID; all binding gates require defined finite inputs; exact denominators (72, 24, 72 and the per-template 24s) and every count equal to its per-prompt flags and per-fact sums; `para_string_n ≥ para_full_n` in every arm (a string hit through other ids is recorded as alternative tokenisation; `string < full` is INVALID).

**LAW#3 known-baseline gate (recipe A; enforced in the driver before any candidate target or recipe runs, §2.7 step 1; re-checked by the reader; a miss → HALT, no candidate recipe runs or is read):** A's A7 `para_full_n` in **[5, 18]/72**, `canon_full_n` in **[5, 10]/24**, `para_first_n` in **[42, 59]/72**, endpoints inclusive (the identical-baseline envelope, `CORPUS/44_C10L_COVGEOM_SPARSEBAND.md:39`, amendment A4 — this envelope and no narrower one), and A's A1 ≥ 68/72 and A2 ≥ 68/72.

**Controls under a candidate recipe:** A1 ≥ 68/72 and A2 ≥ 68/72 under that recipe, else that arm reads **INVALID-CONTROLS** regardless of its A7 count — the recipe breaks the controls; not advanced; never triggers replication; not a halt (the C10V rule that a control failure is never TRADEOFF, `docs/C10V_LAYERPICK_PREREG.md:66`).

**Binding count:** the arm's A7 `para_full_n` = C /72, against A = recipe A's A7 `para_full_n` in the same process, with per-template counts (3 × 24) and the per-fact 24-vector (per-edge pass iff 3/3). Count classes: `lead_size` iff C ≥ 30; `partial_size` iff 18 < C < 30 and C − A ≥ 10; `sized` iff either holds. A count ≤ 18 is never sized.

**Locality gates (vs A, same process; each passes at equality):** L1 flips ≤ A + 1 (of 12); same-frame fictional flips ≤ A + 1 (of 6) **in each realised frame separately** (§2.6; never pooled); `described_as` ≥ A − 3; L3 agreement ≥ 29/30; generic perplexity ≤ A + 0.5; relation-label flips reported (no threshold in the contract). `loc_pass` iff every gate holds.

**Base class (exactly one for every arm that passed validity and controls):**

| count class | `loc_pass` | base class |
|---|---|---|
| `lead_size` | yes | **LEAD** |
| `partial_size` | yes | **PARTIAL** |
| `lead_size` or `partial_size` | no | **TRADEOFF** (failed axes recorded) |
| not sized | yes or no | **NULL** (any failed locality axes recorded beside it); **-BELOW-BASELINE** appended iff C ≤ A − 10 |

**Qualifiers (applied after the base class; every applicable one recorded; neither is an instrument-invalidity label):** **-LARGE-WRITE** iff the finite A7 ratio Σ_l ‖ΔW_l‖_F (arm) / Σ_l ‖ΔW_l‖_F (A) is strictly > 1.5 (equality passes); **-UNDERFIT** (I-2 only) iff fewer than 22 of the 24 A7 z_4 targets have fit ≥ 0.98 (§2.5; both equalities pass).

**Replication eligibility:** an arm is eligible iff its base class is LEAD or PARTIAL and neither -LARGE-WRITE nor -UNDERFIT applies; decided before process 2 is launched. A qualified result never triggers process 2 and is never adopted.

**Replication (gate A):** process 2 independently passes every validity, LAW#3, control, locality and qualifier gate. Each process's class is ranked LEAD = 2, PARTIAL = 1, anything else (any qualified class included) = 0. If both ranks are non-zero, the replicated class is the lower: LEAD/LEAD → LEAD; LEAD/PARTIAL, PARTIAL/LEAD and PARTIAL/PARTIAL → PARTIAL (replicated). Otherwise the process-1 class carries **-NOT-REPLICATED** and nothing is adopted; a process-2 -LARGE-WRITE or -UNDERFIT cannot replicate. Both processes' counts and classes are preserved. The control, locality and qualifier requirements apply per candidate (each arm separately), not jointly across both candidates. Two processes and a historical envelope do not give a calibrated false-positive rate; a label buys or declines a next step (`prereg_stubs.md:11`: PARTIAL is non-binding at one process).

**Boundary examples (deduced from the predicates, not results):** A = 5, C = 18 → NULL; A = 9, C = 19 → PARTIAL with clean locality; A = 10, C = 19 → NULL; A = 18: C = 27 → NULL, C = 28 or 29 → PARTIAL, C = 30 → LEAD. A ratio of exactly 1.5 is not -LARGE-WRITE; exactly 22/24 at ≥ 0.98 is not -UNDERFIT. Injection deficits 5 / 6 / 9 / 10 take the separate rows of the NULL table. None of these thresholds is changed after seeing candidate outcomes.

**Interpretation (fixed now; it does not change any label; first applicable row wins, so exactly one row applies to every arm; the NULL-table row is recorded beside every NULL even when an earlier row applies):**

| # | condition | I-2 (FE) | I-1 (OverTone) |
|---|---|---|---|
| 1 | INVALID / HALT (process-level; a LAW#3 miss included) | instrument unvalidated; no mechanism reading | the same |
| 2 | INVALID-CONTROLS | the FE package breaks A1/A2 | the OverTone package breaks A1/A2 |
| 3 | any base class with -LARGE-WRITE, or TRADEOFF | not advanced at the measured write-size / locality constraint | not advanced at the measured write-size / locality constraint |
| 4 | -UNDERFIT (I-2 only; any base class) | the layer-4 target-fit screen failed; no spreading conclusion | — |
| 5 | LEAD or PARTIAL, unqualified, replicated | the FE-inspired package (z at layer 4, canonical replayed targets, layer-local residuals, undivided updates under the unchanged projected-ridge solve) is a knob on this harness; replay, shallower target optimisation and residual allocation are not separated | the OverTone-inspired target package (dynamic detached token targets, filtering, clipping, retained KL and weight decay, the engine's total-loss stop) is a knob on this harness; no component is identified — in particular the reweighting is not separated from a changed stop or fit |
| 6 | LEAD or PARTIAL, unqualified, not replicated (-NOT-REPLICATED, or process 2 not yet run) | provisional observation; not adopted | the same |
| 7 | NULL (with or without -BELOW-BASELINE), unqualified | the I-2 rows of the NULL table | the I-1 rows of the NULL table |

**NULL table** (d = reference held-out injection hits − candidate-target held-out injection hits, /72, from the §2.5 screen on the unedited model; reference = z_8 @ 8; I-2 candidate = z_4 @ 4; I-1 candidate = z_8^OT @ 8; the rows partition the integers for each arm):

| arm | d | reading |
|---|---|---|
| I-2 | d ≥ 10 | **NULL-TARGET-WEAKER**: the layer-4 target injects at least 10 fewer held-out hits before any write; this NULL does not isolate spreading |
| I-2 | 6 ≤ d ≤ 9 | NULL; intermediate injection deficit; target-strength interpretation withheld |
| I-2 | d ≤ 5 | this FE package did not advance recall with no injection deficit above five; spreading in general is not ruled out |
| I-1 | d ≥ 6 | NULL; the reweighted target injects at least six fewer hits before any write; no causal claim about the objective |
| I-1 | −5 ≤ d ≤ 5 | NULL; injection difference inside the declared non-interpreted band; the reweighted target was not a better target for this write |
| I-1 | d ≤ −6 | NULL; a target with at least six more injected hits did not advance the weight write |

**What each buys.** A replicated unqualified LEAD → the Codex GPT-6-Astra promote gate, then (if both arms lead) a combined FE + OverTone arm as its own pre-registration. A replicated PARTIAL → that arm stays on the queue behind step 7 (H-3) with its configuration fixed. NULL, INVALID-CONTROLS, -NOT-REPLICATED, TRADEOFF, -LARGE-WRITE or -UNDERFIT → not advanced; the sequence moves to step 7; no claim that the engine path is exhausted, and a NULL never exhausts a method family.

## 4. Not claimed, whatever the outcome

No label in CORPUS/36–53 changes. LEAD is a write-path lead, not §8.9 contract closure (route bar 61/72), not route closure, not an F1 change, not evidence about FE or OverTone outside this harness. NULL does not close target construction, token reweighting, other OverTone settings (λ, ε, n), other band layers, or FE with MEMIT's own λC regulariser. I-1 makes no claim that the continuation tokens get an objective in the weight solve (§0 item 2). The engine (`memit_dry_run/memit`) and the harness file `experiments/track_c/c10e_bandknob.py` are untouched; the seams live in new driver files. Spec amendment: none — both arms keep the §8.1 per-commit solve shape (one target per fact derived from the patch, a closed-form layer solve).

## 5. Halt discipline and close-out

**HALT conditions** (a diagnostic JSON at `architecture_profile/c10x_enginepath_halt_diagnostic.json` with the full state and the offending output; the halt recorded in `SESSION_CHECKPOINT.md`; STOP — no next arm): fingerprint or `_cov_cpu` failure; any inertness check of §2.4 (W0, G, G8, X1-(i)–(v), X2-(ii)–(vii)); a measured floor > 1e-5; the LAW#3 gate (in the driver, after recipe A, before any candidate work); a missing `FE_TARGETS` key or layer; an empty OverTone keep-set; a NaN or Inf in any target, logit, residual or ΔW; any float64 tensor on MPS; a leftover intervention hook; a candidate-seam call during G; a counter mismatch; `string < full`; an existing output artifact at a target path. **One speculative fix after a `cat -n` read of the relevant source, then HALT** if the gate does not clear. Predicted halts and their one fix: X1-(ii) failure of its declared acceptance predicate (returned-z relative error >1e-4 for a nonzero reference, measured floor >1e-5, unequal step counts, or unequal zero-reference outputs; fix: reconcile the reduced path with §2.3's declared arithmetic and rerun X1-(ii) once). A nonzero distance within the declared tolerance is not itself a halt trigger; X2-(iv) mismatch (fix: the hook index or the tuple handling per `c10l_covgeom_p6_zinject.py:38–41`); X2-(iii) mismatch (fix: diff `fe_edit` against `my_edit:181–221` line by line); X2-(vi) / X2-(vii) mismatch (fix: `cur` read at the wrong layer or the table mis-keyed — diff `fe_edit` against `my_edit:194–204` line by line); W0 mismatch (fix: the missing `finally` restore in the offending cell). Close-out through `python3 tools/closeout_check.py D-C10x-enginepath` once the CORPUS entry exists. Codex GPT-6-Astra (high) at the implementation review, the verdict, and the promote gate if LEAD. Runs only on the operator's go, one GPU job at a time, with the autoresearch loop paused, and only after the recorded reconsideration under D-C10r-rulings-4 (3) (status line); each reviewer's actual model and effort is recorded, or UNVERIFIABLE (§2.8).

## 6. Reviews and open points

v1 draft → advisor pass (`results/c10x_enginepath_advisor_v1.md`) → Codex design pass (`results/c10x_enginepath_codex_design_v1.md`) → v2 (this file; fold log §8) → freeze check → implementation (Codex, model-free, D-C10r-rulings-9 (3)) → implementation review → the recorded reconsideration of step 6 (D-C10r-rulings-4 (3)) → process 1 → reader → verdict pass → CORPUS/NN. v1's open points, as resolved in v2: (a) the driver-side rebinding of `my_edit` is kept — both reviews accept it (advisor Q1; Codex #12 fixes the call-time `_LAW5_DEFAULT_CTX` read); (b) OverTone stays on all three value classes (neither review asked otherwise; §7 item 6); (c) the injection screens stay qualifiers, now run before the candidate recipes (advisor #1's order) and read through §3's NULL table; (d) undivided residual only (Codex #8 keeps it; no divided variant added); (e) the D-1 frame-subspace readout is still not carried (neither review raised it).

## 7. Author's decisions where the sources were silent (v1; v2 amendments marked)

1. FE replay on the canonical prompt only, with set (overwrite) semantics at layer 4 (§2.2 step 2). v2: as one 24-row padded batch matching the writer (Codex #10); the set/add equivalence stated as conditional (Codex #17).
2. FE's `h_l` read after the earlier layers' edits (the engine convention) and the residual undivided (§2.2 steps 3 and 5).
3. FE reads `cur` at the edited layer, not the z-layer (§2.2 step 3 (b)) — required for per-layer targets to mean anything.
4. OverTone settings from the FT-M row (λ 0.1, n 0.5, ε 0.01), the target distribution detached, the per-prompt mean over tokens kept (the engine's scale), the engine's stopping rule verbatim (§2.3). v2: clip boundary `torch.where(kl > eps, kl, eps)`, std correction 1, strict keep inequality, first-index ties (Codex #14, #16).
5. OverTone's reduction built as `ce + extra` so the Prop. 3.1 parity is expected to be bit-exact (an expectation, not an acceptance requirement; §2.3, X1-(ii)).
6. Both methods applied to A1 and A2 as well as A7; a control failure under a candidate = INVALID-CONTROLS, not a halt (§2.6, §3).
7. No fit screen for I-1 (its objective is predicted to stop short of 0.99 — an I-INFER prediction, v2, Codex #7); a 0.98 / 22-of-24 screen for I-2's layer-4 target (§2.5).
8. Injection screens as qualifiers, not gates; NULL-TARGET-WEAKER at a 10/72 deficit; I-1 injection differences under 6/72 not interpreted (§2.5). v2: run before the candidate recipes; the full deficit partition is §3's NULL table.
9. Recipe order A → I-2 → I-1 in one process; no combined arm; no FE "OneLayer" control (§2.7, §3). v2: A runs first and its LAW#3 gate is enforced in the driver before any candidate work (advisor #1 / Codex #1); the optional SHALLOW-ONLY-4 and CE-early-stop controls are declined (§8, §9).
10. Both premises of the brief corrected in §0 rather than adopted.

## 8. Review fold log (v1 → v2; one line per review item)

- Advisor #1 (BLOCKING) — applied-with-change: Codex #1's superset text used (the same ordering in process 2; baseline-only halted records never become candidate NULLs); §2.7 steps 1–5, §3 LAW#3, §5.
- Advisor #2 (BLOCKING) — applied-with-change: Codex #2's W0 text used (dtype/shape/raw-byte hashes, `finally` restores and hook removal, leftover-hook HALT, `base_snap` not an authority); §2.4, §2.7, §3 validity, §5.
- Advisor #3 (BLOCKING) — applied-with-change: superseded by Codex #3 — X2-(vi) runs the real target builder and compares full tensors and per-prompt greedy flags, X2-(vii) is an exact-zero multi-layer null with an independent observer and negative controls, G8 adds a direct engine reference; the advisor's norm-based structure check is not used (it cannot detect equal-norm permutations); X2-(iii) kept as an additional shared-lines check; §2.2 steps 3–4, §2.4, §3, §5.
- Advisor #4 (BLOCKING) — applied-with-change: Codex #4's total classification used — the advisor's rows 5 and 6 overlapped at injection deficits 6–8, and its "spreading is not the wall" claimed more than a package NULL shows; §2.7 process 2, §3.
- Advisor #5 (ADVISORY) — applied-with-change: Codex #5's text used (adds appendix `:55`, the `:15` residue, the offline 0.232 paraphrase value and the I-INFER scope); header, §0 item 1, H-X2-null, §2.5 ρ prediction.
- Advisor #6 (ADVISORY) — applied: §0 item 2 key citation and per-position denominators; §2.5 prediction (Codex #6's agreeing wording).
- Advisor #7 (ADVISORY) — applied-with-change: the I-1 reading is narrowed to the package and the lower fit / earlier stop is an I-INFER prediction tested by recorded fits, steps and stop reasons (Codex #7); the optional CE-early-stop diagnostic recipe declined: it widens scope and matches neither fit, steps nor write size (Codex #7); attribution needs its own pre-registration (§9 item 5).
- Advisor #8 (ADVISORY) — applied-with-change: the I-2 package reading and the I-INFER -LARGE-WRITE prediction per Codex #8; "layer 4 carries almost the whole write" not adopted (a band-end ratio does not establish single-layer realisation); the optional layer-4 OneLayer recipe declined: it widens scope and differs from the paper's final-layer OneLayer (Codex #8) (§9 item 5).
- Advisor #9 (ADVISORY) — applied-with-change: Codex #9's bound (tol ≤ 1e-4, i.e. floor ≤ 1e-5) replaces the advisor's floor ≤ 1e-4, which still admitted a tolerance of 1e-3 (§8.1).
- Advisor #10 (ADVISORY) — applied-with-change: treated as BLOCKING per Codex #10; both sides are 24-row batches (§2.2 step 2, X2-(iv)), not only the reference.
- Advisor #11 (ADVISORY) — applied-with-change: treated as BLOCKING per Codex #11; masking happens before filter and KL arithmetic rather than as a final `torch.where` selection; empty-support HALT added; §2.3.
- Advisor #12 (ADVISORY) — applied: the G bullet and the counter resets, with Codex #12's separate standalone counters and the G-seam HALT; §2.4.
- Advisor #13 (ADVISORY) — applied-with-change: Codex #13's figures used (measured 26.1 / 27.5 / 29.1 min; a planning estimate, not a bound; "worst case 7 h" withdrawn); §2.7 Compute.
- Codex #1 (BLOCKING) — applied: §2.7 Process 1 steps 1–5 and the process-2 order, §3 LAW#3, §5.
- Codex #2 (BLOCKING) — applied: W0 in §2.4, §2.7 step 0 and steps 3/5, §3 validity, §5.
- Codex #3 (BLOCKING) — applied: X2-(vi), X2-(vii) and G8 in §2.4; §2.2 steps 3–4; §2.7 step 3; §3 validity; §5.
- Codex #4 (BLOCKING) — applied: §3 count classes, base-class table, qualifiers, eligibility, replication ranks, interpretation and NULL tables, boundary examples; §2.7 process 2.
- Codex #5 (ADVISORY) — applied: header pointers, §0 item 1, H-X2-null.
- Codex #6 (ADVISORY) — applied: §0 item 2, §2.5 per-position prediction.
- Codex #7 (ADVISORY) — applied: §2.3 departures, §3 interpretation row 5, §7 item 7; no extra recipe.
- Codex #8 (ADVISORY) — applied: §2.5 ΔW prediction, §3 interpretation row 5; SHALLOW-ONLY-4 omitted as Codex specifies.
- Codex #9 (ADVISORY) — applied: §2.4 tolerance rule; §3 validity (floor ≤ 1e-5); §5.
- Codex #10 (BLOCKING) — applied: §2.2 step 2, X2-(iv), carried into X2-(vii).
- Codex #11 (BLOCKING) — applied-with-change: "use the literal engine CE arithmetic for lam = 1, eps = 0" is implemented as the literal `compute_z.py:141–149` arithmetic for `ce` in every setting with no `lam`/`eps`-specific code path, so that X1-(ii) exercises the active branch rather than a special case; §2.3.
- Codex #12 (ADVISORY) — applied: §2.2 step 4 dispatch, §2.4 G and counters, §5.
- Codex #13 (ADVISORY) — applied: §2.7 Compute (table, withdrawn 7 h, memory note).
- Codex #14 (BLOCKING) — applied: X1-(iii) full-vocabulary unrounded logits, frozen conventions, the shared-top-64 tail control.
- Codex #15 (BLOCKING) — applied: §2.6 per-frame bystander probes over every realised rewriting frame; §3 locality per frame, never pooled.
- Codex #16 (BLOCKING) — applied-with-change: the equality convention is fixed as `torch.where(kl > eps, kl, eps)` so the zero gradient at equality does not depend on a library clamp's boundary convention, and X1-(ii)'s "by construction" claim is narrowed to match (a position with exactly-zero engine CE takes the constant branch; acceptance follows the X1-(ii) predicate amended in v2.1, not an exact-equality requirement for nonzero references); §2.3, X1-(ii), X1-(v).
- Codex #17 (ADVISORY) — applied: H-X2-null literature clause; §2.2 step 2 set/add conditionality and the `target_init` diagnostic.
- Codex #18 (ADVISORY) — applied: §2.8 manifest, refusal to overwrite and the cross-process match rule; status line and §5 (design approval is not execution approval; reviewer identity recorded or UNVERIFIABLE).

### 8.1 Reviewer conflicts and their resolution (the more conservative option taken)

1. **Advisor #3 vs Codex #3 (FE-path reduction).** The advisor's singleton check supplies the table by hand and checks structure by residual norms; Codex runs the real builder, compares full tensors and greedy flags, adds an exact-zero multi-layer null and the G8 engine reference. Codex taken (more gates, more halts). Codex also says to "replace" the identity-only check; v2 keeps X2-(iii) as an additional shared-lines check (one more halt, no credit taken from it).
2. **Advisor #4 vs Codex #4 (reading rules).** The advisor's rows overlap at injection deficits 6–8 and read a NULL as "spreading is not the wall"; Codex's table is disjoint and package-scoped. Codex taken (claims less).
3. **Advisor #7 / #8 vs Codex #7 / #8 (attribution).** The advisor offers optional control recipes and states an earlier stop and layer-4 concentration as facts; Codex treats both as I-INFER predictions and adds no recipe. Codex taken (claims less; no scope widening).
4. **Advisor #9 vs Codex #9 (tolerance ceiling).** Floor ≤ 1e-4 (tolerance up to 1e-3) against tolerance ≤ 1e-4 (floor ≤ 1e-5). Codex taken (halts sooner).
5. **Advisor #10 / #11 (ADVISORY) vs Codex #10 / #11 (BLOCKING).** Severity and remedy differ: Codex matches both batch sides and masks before the arithmetic. Codex taken, as BLOCKING.
6. **Advisor #13 vs Codex #13 (budget).** A ≈ 2.9 h point estimate against a planning range that is not a bound, with "worst case 7 h" withdrawn. Codex taken (claims less).

### 8.2 Astra freeze-check fold log (v2 → v2.1; `results/c10x_enginepath_astra_freeze_v2.md`, FIX-FIRST)

- Astra-freeze BLOCKING 1 → §2.7 Compute: hard per-stage wall-clock caps, 250-minute process cap (500 for two), pre-stage projection and refusal, independent watchdog, HALTED/incomplete never NULL.
- Astra-freeze BLOCKING 2 → §2.7 steps 1 and 5, §2.2 step 4: both `FE_STATE` and `H.Z_OVERRIDE` assigned explicitly before every recipe; counters reset; both restored to `None` in `finally`; W0 verified.
- Astra-freeze BLOCKING 3 → §3 Validity: legitimate diagnostic nulls (`tf_pertok_cont`, `cond_full_given_first`) preserved with a zero-denominator reason; any other missing or non-finite datum INVALID.
- Astra-freeze BLOCKING 4 → §2.4 X1-(ii), §7 item 5: one acceptance predicate (relative error ≤1e-4, floor ≤1e-5, exact step counts, exact zeros); bit-exactness an expectation only.
- Astra-freeze BLOCKING 5 → §2.3: `raw_logits` computed once in the engine dtype; targets from its detached fp32 cast; `extra` from `log_probs[scored_mask].float()`; no fp32 head recomputation.
- Astra-freeze ADVISORY (last bullet) → §3 interpretation rows 2–3, §2.2 step 2, §3 Replication: causal parentheticals removed; unspecified six-prompt spread diagnostic deleted (no gate or readout used it); per-candidate scope stated. Other ADVISORY bullets are notes only.
- Astra confirmation (v2.1 → v2.2; `results/c10x_enginepath_astra_freeze_v21.md`) BLOCKING (blocker 4 partial) → §5 X1-(ii) halt clause now cites the declared acceptance predicate; §8 Codex #16 parenthetical no longer requires exact equality for nonzero references.

## 9. Open for the program (each with a recommendation; none blocks the freeze check)

1. **Whether step 6 executes at all.** Under D-C10r-rulings-4 (3) execution waits for the recorded reconsideration after steps 3, 4 and the step-5 oracle are read. *Recommendation:* decide then, on those results; v2 presumes nothing about the outcome.
2. **Authentication of the cross-family review.** The Codex design pass records its own model and effort as UNVERIFIABLE (`results/c10x_enginepath_codex_design_v1.md:3`), while CLAUDE.md names GPT-6-Astra at high effort for promote gates. *Recommendation:* run the freeze check through the explicit `codex exec --model gpt-6-astra -c model_reasoning_effort=high …` invocation and keep the command line in its output; until then treat the design pass as cross-family but unauthenticated.
3. **G8 crosses the regulariser difference.** At a single layer the engine's covariance-regularised float64 solve and the harness's projected ridge-1 fp32 solve may differ behaviourally for a reason other than a defect, and v2 makes a G8 miss a HALT (Codex #3). *Recommendation:* keep the HALT; if it fires, the diagnostic decides whether a separately reviewed amendment is needed. G8's limits are never relaxed in-run.
4. **X2-(vii) requires exact zero while X2-(iv) admits ≤ 1e-4.** Any non-zero replay-versus-reader distance therefore HALTs the process. *Recommendation:* keep it; the same-shape floors measured so far are 0.0 (`results/c10s_sharedz_logs/inertness.log:9`; `CORPUS/53_C10T_SECONDKEY.md:15`).
5. **Attribution controls declined here** (a CE control with matched stop or fit for I-1; SHALLOW-ONLY-4 for I-2). *Recommendation:* pre-register them only if an arm reads a replicated, unqualified LEAD or PARTIAL.


## 10. Amendment T — live telemetry and per-prompt answers (2026-10-08, pre-observation; D-C10r-rulings-11, D-C10r-dash-1, D-C10w-p2rerun)

Written before any C10X code, build or process exists. On 2026-10-08 there is no `experiments/track_c/c10x_*` file and no `results/c10x_enginepath/`, `results/c10x_enginepath_r2/` or `results/c10x_enginepath_logs/`. The only `results/c10x_*` entries are the five review files named in the status line (`:3`) and §8. §0–§9 are unchanged. This section adds an instrument and launch rules. It changes no hypothesis, arm, recipe, stimulus, metric, threshold, gate, qualifier, label, interpretation row, stage cap or process cap, and it replaces no sentence above. Where it conflicts with the build brief, this section governs.

Sources:
- runbook §5 rows D-C10r-rulings-11 (`EXPERIMENT_RUNBOOK.md:363`), D-C10w-p2rerun (`:378`) and D-C10r-dash-1 (`:379`);
- the approved pattern, C10Z §9(h) and §9.1 (h′1)–(h′5) (`docs/C10Z_ASTRA_PREREG.md:467–476`, `:554–604`);
- the program's C10X build brief, §5 (telemetry basis) and §9 Q1–Q3 and Q6. This section rules on each of those questions below.

**The rulings, quoted.**
- D-C10r-rulings-11 (`EXPERIMENT_RUNBOOK.md:363`): "an opt-in writer appending small JSONL snapshots during a run to `results/<exp>/telemetry/` (per-layer write norms, per-position target probabilities, logit-lens top-k at each band layer for the probe prompts, phase markers) … It must not change any computed result: off by default, or proven inert under LAW#5 (identical counts and records with telemetry on vs off); test-first; reviewed with the build (advisor + Astra); folded in as a dated pre-observation amendment to each frozen prereg (C10X, C10Y, C10Z) before its build."
- D-C10r-dash-1 (`:379`): "every new experiment build (C10X, C10Y, ASTRA later attempts) streams per-prompt generated text through the opt-in, inertness-proven telemetry path (… a JSONL line per prompt with subject, template, generated text, right/wrong), admitted only after its LAW#5-style inertness check".
- D-C10w-p2rerun (`:378`): "STANDING RULE: a run whose result is compromised (halted, corrupted, or read through a patch) is re-run, never read around by a deviation note".

(T1) **Switch.**
- `C10X_TELEMETRY` absent means telemetry is off. Off is the default.
- Exactly `"1"` means on, and only when `C10X_TELEMETRY_INERTNESS` names a valid INERT record under (T8).
- Any other value (`"0"`, `"true"`, `""`, `" 1"`) is refused, and so is `"1"` with an absent or invalid record. A refusal comes before any write: the driver exits non-zero and creates no out directory, log, record or halt diagnostic. This is a launch refusal, not a run.
- `run.json` (§2.8, `:124`) always carries two keys:
  - `"telemetry": true|false`;
  - `"telemetry_inertness": {"path", "sha256"}` or `null`.

  Under (T7)'s controlled proof, these two values are the only record difference between telemetry on and off. The live exceptions are those enumerated in (T10).
- Only telemetry-on launches require or verify an inertness record; telemetry-off launches require neither that record nor telemetry calibration.
- Every telemetry-off launch line removes both variables explicitly (`env -u C10X_TELEMETRY -u C10X_TELEMETRY_INERTNESS …`), so that an inherited value cannot switch telemetry on (the C10Z (j′) precedent, `docs/C10Z_ASTRA_PREREG.md:608`).

(T2) **Path and line format.**
- The file is `<OUT_DIR>/telemetry/telemetry_p<process>.jsonl`. That is `results/c10x_enginepath/telemetry/telemetry_p1.jsonl` for process 1 and `results/c10x_enginepath_r2/telemetry/telemetry_p2.jsonl` for process 2 (§2.8, `:124`), or the re-run directory of (T12).
- With telemetry off, no `telemetry/` directory exists.
- The file is opened once, in append mode. Its first line is a header.
- Every line holds `kind`, `t_utc`, `elapsed_s`, `cumulative_s`, `process` and `run_id`:
  - `elapsed_s` is the time from entering the telemetry call to just before that line is written;
  - `cumulative_s` is the full time of all earlier lines, writes included (C10Z (h′2), `:558`).
- Each line is serialised with `json.dumps(…, allow_nan=False, sort_keys=True, separators=(",",":"))` plus a newline, then written, flushed and fsynced.
- The telemetry clock is `time.perf_counter`, bound at import. It is never the watchdog clock or the stage-projection clock of §2.7 (`:118`).

(T3) **Line kinds, placement and volume.**

| kind | where | payload |
|---|---|---|
| `phase` | `stage_start`/`stage_end` around each §2.7 stage (`:118`); `recipe_start`/`recipe_end` immediately around each `H.run_recipe` (§2.7 step 5, `:104`); `check_start`/`check_end` around each standalone §2.4 check; `halt` on the worker's halt path, immediately before the §5 diagnostic is written (`:188`) | stage, recipe, check or halt code |
| `write_norms` | in `dispatch` (§2.2 step 4, `:44`), after `my_edit` or `fe_edit` returns, only for recipe-arm writes (`H._LAW5_DEFAULT_CTX` False): 9 per process | recipe, arm, mode. It echoes, and never recomputes, the returned `delta_norms` (`c10e_bandknob.py:213–215`), labelled `harness_fp32`. For `fe_edit` it also echoes the driver's float64 ρ_FE(l) (§2.2 step 3, `:43`) |
| `target_probs` | once after each target table is built (engine z_8, engine z_4, OverTone z_8^OT; §2.7 step 2, `:101`) | values the driver already records (§2.5, `:86`): the engine's final-step average probability per request, captured from its stdout (`compute_z.py:159–163`); for OverTone, the per-token π_θ(y) at stop as parallel arrays (request, prompt, position, p) |
| `logit_lens` | pristine, once in the setup stage after the W0 snapshot (§2.4, `:68`); post-write in the A7 arm of each recipe, inside the driver's own probe hook after its probes (`ARM_HOOKS`, `c10e_bandknob.py:494–495`), with no change to the dict the hook returns | layers `hp.layers` (4–8); the 24 A7 canonical prompts at the last position; top-5 `[id, text, prob]` per layer |
| `answer` | every call of the observed scorer of (T4) | the schema of (T4) |

- **Volume per process:**
  - 864 `answer` lines: 96 per arm × 3 arms × 3 recipes;
  - 4 lens calls × 24 forwards = 96 lens forwards;
  - 9 `write_norms` lines;
  - 3 `target_probs` lines;
  - phase lines and the header.

  No line is written per requirement, except `answer`.
- **Logit lens** (the C10Z (h′5) semantics, `:601–604`):
  - one no-grad forward per prompt, with `output_hidden_states=True`, `use_cache=False` and no hook;
  - the residual after band layer l is `hidden_states[l+1][:, -1, :]` (installed transformers, `modeling_qwen2.py:528–570`);
  - then `model.model.norm`, then `lm_head`;
  - the forward and its tensors are in fp16 on MPS. The softmax and top-5 are computed on a detached CPU float64 copy of the 151,936-wide logits row (T6);
  - it raises if `max(layers) > num_hidden_layers − 2`.
- **Per-position target probabilities: scope stated.** The engine `compute_z` prints only the mean probability over a request's target tokens (`compute_z.py:162`). For engine z_8 and z_4 targets, telemetry therefore reports one value per request. It adds no forward and no solver change to obtain per-position values. Per-position values are reported for OverTone targets, and post-write per-position right/wrong is derivable from each `answer` line's `target_ids` and `generated_ids`.

(T4) **Per-prompt answer lines (D-C10r-dash-1). Build-brief Q2 ruling: the observed scorer is adopted.**

*Reason:* the harness scorer `full_seq_match` computes the generated ids and returns only two booleans (`c10e_bandknob.py:108–117`). A statement-identical observed copy shows exactly the tokens that were scored, with no extra forward. A separate telemetry decode would add about 816 greedy forwards per recipe, and its text could differ from the scored decode.

- **Installation.** Only while telemetry is on, `H.full_seq_match` is rebound to `observed_full_seq_match`:
  - immediately before each scored `H.run_recipe` call (A, I-2, I-1; §2.7 steps 1 and 5);
  - restored to the original object in `finally`.
- **Not installed** for the stimulus base report (`c10e_bandknob.py:449–455`) or for any standalone §2.4 check. Those calls run the original scorer and emit no `answer` line.
- **The copy.** `observed_full_seq_match` is a statement-for-statement copy of `c10e_bandknob.py:108–117`:
  - the same `@torch.no_grad()`, `H.tok`, `H.model` and `H.DEV`;
  - plus exactly one inserted expression statement, `sink(prompt, target_ids, gen)`, placed immediately before the unchanged `return gen == list(target_ids), gen[0] == target_ids[0]` (`:117`).

  The original scorer has no `full` or `first` variable: it returns the two expressions directly (`:117`). The sink computes both predicates with those same expressions, inside its own protected body (T5). It copies `gen` and `target_ids` and never mutates them.
- **With telemetry off,** the driver asserts at each recipe start that `H.full_seq_match` is the original object. This is an assertion only, never a record field.
- **Line schema** (`kind: "answer"`, plus the (T2) common fields):

| field | type | value |
|---|---|---|
| `recipe` | str | the `run_recipe` name |
| `arm` | str | the `H.ARMS` key (`A1_single`, `A2_coherent2`, `A7_coined_coined`; `c10e_bandknob.py:244–246`), matched from `H._ARM_STATE["requests"]` (`:487`) |
| `phase` | str | the §2.7 stage name |
| `subj` | str | the fictional subject whose formatted template equals `prompt` |
| `val` | str | `H.ARMS[arm][subj]`, the value written |
| `template` | str | the unformatted template containing `{}` (`CANON` or one of `PTEST`, `c10e_bandknob.py:51–56`) |
| `prompt` | str | as scored |
| `target_ids`, `generated_ids` | list[int] | as scored |
| `text` | str | `H.tok.decode(generated_ids)` |
| `full` | bool | computed by the sink as `gen == list(target_ids)` (`c10e_bandknob.py:117`), equal to the scorer's first return value: the binding whole-answer right/wrong |
| `first` | bool | computed by the sink as `gen[0] == target_ids[0]` (`:117`), equal to the scorer's second return value |

- **Unresolved attribution is a telemetry failure.** If `arm`, `subj`, `val` or `template` cannot be resolved uniquely, the sink writes no line and disables telemetry (T5). No null `subj` or `template` is ever written, because the tab renders both directly (`tools/dashboard_experiment.py:213–215`).
- **Dashboard: field names match, but the input does not yet exist.**
  - `subj`, `template`, `text` and `full` are the names the tab's record reader takes from `generated` entries (`:193–201`), and `val` the name it takes from `detail` rows (`:197`). They carry the dash-1 items: subject → `subj`, template → `template`, generated text → `text`, right/wrong → `full`.
  - The tab takes these entries only from `recipes[…].arms.A7_coined_coined.extra.generated` in a recorded JSON (`:192–201`). JSONL is not presently a supported input.
  - The unchanged harness records correctness flags, not generated text (`c10e_bandknob.py:366–374`, `:496–498`).
  - Telemetry-off first attempts do not provide generated-answer display through this design; live answers await admitted telemetry and its dashboard adapter.

(T5) **What telemetry never does; failure.**
- Telemetry reads only. It never:
  - writes a parameter or buffer, or registers a hook;
  - calls the watchdog, a stage projection, a deadline or `torch.mps.synchronize`;
  - writes into any §2.8 record or the §5 halt diagnostic, or adds a key to an `ARM_HOOKS` result;
  - feeds any value to a gate, qualifier, label or reader.
- Its `.cpu()` copies may synchronise the device implicitly. They change no value.
- **Failure.** Every public telemetry method body catches `Exception`, never `BaseException`. On failure it:
  - writes exactly one `C10X_TELEMETRY_DISABLED <ExcType>: <msg>` line to `sys.__stderr__`;
  - disables later calls;
  - never propagates the exception, so it never halts or alters the run.

  The marker goes to `sys.__stderr__` because `run_recipe` wraps the write in `contextlib.redirect_stdout` (`c10e_bandknob.py:488–489`), which would swallow a stdout marker raised in `dispatch`.
- If the observed scorer's sink fails, the scorer still returns its identical result. A failure inside the copied scorer statements themselves is not a telemetry failure. It propagates as the original's would.
- A declared disable (the marker above) does not compromise the science record and triggers no re-run; (T11) records it as an audit failure. Any other missing, malformed or unexpected output is handled by (T11).

(T6) **Float64 (the P2 lesson, `EXPERIMENT_RUNBOOK.md:377`: a 22.5M-element fp32 accumulation gave cosines of 1.007–1.009).**
- Every reduction that telemetry itself performs over a model-sized tensor is done on a detached CPU float64 copy. That covers the lens softmax over the 151,936 vocabulary entries.
- Telemetry performs no reduction over a weight-sized tensor. Write norms are echoed: `delta_norms` labelled `harness_fp32`, and the driver's float64 values labelled `driver_float64`.
- Which ΔW the §2.4 parity gates use, and in what arithmetic, is not a telemetry question. It is ruled in §11 (Amendment M), not here.

(T7) **Code-path proof, test-first (the analogue of C10Z (h′4), `:580–585`).**
- **Isolation.** The tests are written and recorded failing before the writer exists. They run CPU-only on a stub `H` and tiny CPU models, under temporary roots, with an audit-hook write guard that refuses any write under the real `results/` or `architecture_profile/`. The guard is proved by a positive control. This is the guard whose absence let a C10W selftest dispatch "a real P2 training stage against the live tree" (`results/c10w_oracle/_quarantine_selftest_leak_20261008/README.md:3`). A test that writes to the live tree fails the build. Deny real experiment subprocess dispatch; allow only explicitly isolated stub workers. Install protection before imports, resolve protected paths, and positively test the subprocess boundary without launching a real stage.
- **Identical with telemetry on and off,** under injected clocks and a fixed `run_id`, JSON-normalised:
  - every return value, record and reader output;
  - the out-directory file set, excluding `telemetry/`;
  - the only exceptions are the two `run.json` values of (T1).
- **Identical counts:**
  - calls to the watchdog clock, the stage projection and `sync`;
  - stub-model forwards, excluding lens forwards tagged as telemetry;
  - the observed scorer's outputs and its exact sequence of model inputs, against the original `full_seq_match`.
- **AST check** against the text of `c10e_bandknob.py:108–117`, read from the file: the observed copy differs only by the one inserted `sink(prompt, target_ids, gen)` statement, and the (T8) reference capture only by its one inserted `capture(prompt, target_ids, gen)` statement.
- **Reference-capture validation.** The (T8) reference capture returns outputs and issues a model-input sequence identical to the original `full_seq_match`, and the IDs it captures equal the generated IDs the original computes.
- **Unchanged across every telemetry call,** checked before and after:
  - every parameter and buffer (`torch.equal` and `data_ptr`);
  - `torch.random.get_rng_state()` and `model.training`;
  - every module's `_forward_hooks`, `_forward_pre_hooks` and `_backward_hooks`;
  - `torch.is_grad_enabled()`.
- A science forward run after a telemetry call is `torch.equal` to one run without it.
- The on-file holds the header and every kind of (T3), with exactly 96 `answer` lines per evaluated arm.
- This proves the code path only. It does not prove live inertness, which is (T8)'s job.

(T8) **MPS inertness check (LAW#5): the admission screen (the analogue of C10Z (h′3), `:566–579`).**
- **Runner.** `experiments/track_c/c10x_enginepath_telemetry_check.py` runs `telemetry_mps_inertness_check()` from the driver:
  - once, on MPS, with the GPU otherwise idle;
  - on the W0-verified pristine model, in one process;
  - writing `results/c10x_enginepath_telemetry_inertness/<UTC>/inertness.json`. An existing `inertness.json` is refused.
- **Method.**
  - One uncompared warm-up: one scorer call and one science forward.
  - Then three passes: P1 plain, T telemetry on, P2 plain. Each pass runs, in order:
    1. in T only, `logit_lens` on the 24 A7 canonical prompts;
    2. the 96 A7 scored prompts in `eval_arm` order (per subject: `CANON`, then the three `PTEST`; `c10e_bandknob.py:360–363`). Each goes through a scorer copy that differs from `:108–117` by one inserted statement before the unchanged return:
       - in P1 and P2, the **reference capture** `capture(prompt, target_ids, gen)`, which appends a copy of `gen` to a plain list;
       - in T, the telemetry `sink(prompt, target_ids, gen)` of (T4), with a live writer.

       Each pass records, per prompt, the exact generated-ID sequence and the `(full, first)` flags that the scorer returned. The reference capture is validated before use by (T7).
    3. in T only, `logit_lens` again;
    4. the writer's science forward: the 24-row canonical `cur` read `get_module_input_output_at_words(model, tok, l, [CANON]*24, <A7 subjects in request order>, hp.layer_module_tmp, "subject_last")[1]` for l = 4…8 (X2-(iv)(a), `:78`; defined at `compute_z.py:188`), kept as CPU fp32 copies.
- **Verdict** (identical tokens are required, as in C10Z, `docs/C10Z_ASTRA_PREREG.md:575`).
  - INVALID if any of the following holds. A disabled writer or missing output is never INERT.
    - The band `down_proj` weights, hashed before and after, differ.
    - A T-pass lens call fails or yields a non-finite value.
    - The T-pass telemetry output is incomplete: a `C10X_TELEMETRY_DISABLED` marker; other than exactly 96 `answer` lines; or other than 2 `logit_lens` lines of 24 prompts each.
  - Otherwise NONDETERMINISTIC-BASELINE, unless P1 and P2 have identical generated-ID sequences and identical flags for all 96 prompts (exact) and `torch.equal` (bitwise) tensors at every layer.
  - Otherwise INERT if T equals P1 in the same three respects, and T's `answer` lines carry those same IDs and flags. NOT-INERT if not.
  - Only INERT admits telemetry. Any other verdict keeps telemetry off for this prereg. A revised writer then needs its own dated amendment.
- **Record.** It holds:
  - `schema`, `decision_id` "D-C10r-rulings-11", `device` "mps", `verdict`, `control_equal`, `telemetry_equal`, `generated_equal`, `telemetry_complete` and `weights_unchanged`;
  - `answer_calls` (96) and `lens_forwards` (48);
  - the measured `lens_forward_seconds` and `answer_line_seconds` (each written T-pass line, timed), for (T10);
  - the SHA-256s of the driver, solver, inertness module, reader, check script, `c10e_bandknob.py`, hparams, `compute_z.py`, `rome/repr_tools.py` (which the science forward runs, `compute_z.py:214`, `:225`), `memit_main.py` and this prereg;
  - `env`: python, machine, platform, torch and transformers versions, and `model_rev`;
  - start and finish times.
- **Admission.** Only telemetry-on launches require or verify an inertness record; telemetry-off launches require neither that record nor telemetry calibration. At each telemetry-on process start, the driver requires every recorded hash and `env` field to match the current files and environment. A changed source makes the record unusable, and the check is then re-run in a new `<UTC>` directory.
- **Scope, stated in the record.** INERT establishes equality only for these pristine outputs, under the recorded identity. It does not establish resource inertness, or equality of edited-arm outputs and records on MPS. Edited outputs and resource inertness remain UNVERIFIED, as in C10Z (h′2) (`:563`). The post-run audit of (T11) adds a per-run check of the answer path.
- **Cost (I-INFER).**
  - Per pass: the A7 scorer runs 528 greedy forwards. That is 24 canonical + 72 held-out prompts of 4–6 tokens, totalling 132 + 396 tokens; the held-out per-position denominators are 72, 72, 72, 72, 69 and 39 (`:13`). Add 5 batch reads.
  - In all: about 1,650 forwards (3 × 533, 48 lens forwards and the warm-up). At C10Z's planning range of t = 0.03–0.15 s per forward (`:579`), that is about 0.8–4.1 GPU-minutes, plus model load and preflight, which are UNMEASURED.
  - The check is its own GPU job, one GPU job at a time. It is outside the 250-minute process cap and the 500-minute two-process cap (`:118`).
  - **Authorization (program ruling 2026-10-08).** The check is GPU spend outside the experiment's caps. The program does not self-authorize it: it is dispatched only under a recorded authorization that names its cost, as C10Z's analogue required the operator's yes (C10Z (h′3), `docs/C10Z_ASTRA_PREREG.md:566–579`). Before dispatch it records a D-ID in runbook §5 with the stated cost, and afterwards the measured GPU time.

(T9) **First process and process 2. Build-brief Q3 ruling (first-process setting).**
- **First attempt: telemetry off (program ruling 2026-10-08).** Process 1 and process 2 of the first attempt run with telemetry unset, whatever any inertness record says. Telemetry may be switched on only for a later attempt, and only after an INERT (T8) record exists under the authorization above.

  *Reason:*
  - C10Z ruled the same for its first attempt (§9.1 (j′), `docs/C10Z_ASTRA_PREREG.md:609–610`).
  - A telemetry-on process that halts on a cap must be re-run in full under D-C10w-p2rerun (`EXPERIMENT_RUNBOOK.md:378`); the first clean measurement takes priority over live display.
  - Telemetry-off first attempts do not provide generated-answer display through this design; live answers await admitted telemetry and its dashboard adapter (T4).
- **Process 2** runs with the telemetry setting of the process-1 directory whose eligible arm it replicates (§2.7, `:106`). A different setting is refused before any write. Only a telemetry-on process 2 re-verifies the inertness record under (T8).
- **Replacements and the replication pair.** A replacement with changed telemetry setting cannot join the prior replication pair. Regenerate the required pair with telemetry off, retaining all original artifacts, eligibility gates and spending requirements.

(T10) **What telemetry can change; caps; description rule. Build-brief Q3 ruling (cost, caps, description rule).**
- **Time counts against the caps.** Telemetry's own time counts against the stage caps, the 250-minute process cap and the watchdog deadlines of §2.7 (`:118`).
  - It is never subtracted from a measured duration, a cap or a projection.
  - No cap is raised for it, in-run or before.
  - Projections that use measured work units include it, because it occurs inside them.
- **Expected volume per scored recipe.** Each scored recipe (cap 34 min) carries:
  - 288 `answer` lines;
  - 3 `write_norms` lines;
  - one lens call of 24 forwards, about 0.7–3.6 s at t = 0.03–0.15 s.

  The setup stage (cap 10 min) carries the pristine lens call of 24 forwards. The per-line write time is measured by (T8) (`answer_line_seconds`).
- **Fields that may differ with telemetry on:**
  - timing fields: per-cell measured wall-clock (`:120`), stage projections, timestamps and run identity (`:118`, `:124`);
  - telemetry's own two `run.json` values (T1).

  A process near a cap can therefore end HALTED/incomplete where a telemetry-off process would not. Every count, flag, hash, target, ΔW and label is otherwise identical under (T7). On MPS that is established only within (T8)'s scope.
- **Description rule** (like C10Z's, `:565`; it changes no gate or label):
  - If a telemetry-on process ends HALTED/incomplete by a stage projection, a watchdog timeout or the process cap, the program reports it as possibly affected by telemetry.
  - Under D-C10w-p2rerun it re-runs that process with telemetry off, in a re-run directory (T12). The pair rule of (T9) applies: a replacement with changed telemetry setting cannot join the prior replication pair, so the required pair is regenerated with telemetry off.
  - It does not treat such a halt as evidence about C10X's cost.

(T11) **Post-run answer audit (model-free).**
- **When.** Before the reader is run on a telemetry-on process, the program runs the check runner's model-free `audit` entry point on that process's out directory. It writes `<OUT_DIR>/telemetry/audit.json`.
- **What it compares,** for every scored recipe and arm, with exact equality:
  - the `answer` lines' `full` and `first`, keyed by (`recipe`, `arm`, `subj`, `template`);
  - the record's per-prompt flags in that recipe's `detail` rows (`c10e_bandknob.py:366–374`): `canon_full` and `canon_first` for `CANON`, and `para_full_hits[k]` and `para_first_hits[k]` for `PTEST[k]`.
- **What the audit checks.** It passes only if every expected line is present, well formed and exact. Each of the following is an audit FAIL, with its cause recorded; none passes silently:
  - MISMATCH: a `full` or `first` that differs from the record;
  - DUPLICATE: two lines with one key;
  - MISSING: an expected key (96 per evaluated arm) with no line and no preceding disabled marker;
  - **Schema rule:** Validate each line against its kind-specific schema. All kinds require T2 fields; only `answer` requires T4 fields and answer-key membership. Admit exactly one initial header under an explicitly defined header schema. Unknown kinds or fields fail against the applicable schema.
    - The header schema: the (T2) fields with `kind` = `"header"`, plus `schema` = `"c10x_enginepath_telemetry/v1"` (str) and `telemetry` = `true` (bool). Nothing else.
    - The schemas of `phase`, `write_norms`, `target_probs` and `logit_lens` are the (T2) fields plus that kind's payload in the (T3) table.
  - MALFORMED: a line that is not strict JSON; a line missing a field its kind's schema requires; a field of the wrong type, or a null where the schema has none; or a header that is absent, not first, or repeated;
  - UNEXPECTED: an unknown `kind`; a field outside its kind's schema; or an `answer` key outside the scored recipes and arms;
  - DISABLED: lines missing after a `C10X_TELEMETRY_DISABLED` marker.
- **Disposition of MISMATCH, DUPLICATE, MISSING, MALFORMED or UNEXPECTED.** The scorer or writer ran outside its proven, declared behaviour:
  - the process is treated as compromised;
  - it is re-run with telemetry off in a re-run directory (T12), never read around (D-C10w-p2rerun);
  - the pair rule of (T9) applies.
- **Disposition of DISABLED.** The declared failure path of (T5) operated:
  - the audit FAILs and is reported;
  - the missing prompts' answer path is unaudited;
  - the science record stands under (T5); no re-run.
- The reader never reads `telemetry/`.

(T12) **Re-run directories. Build-brief Q6 ruling.**
- **The first attempt** of each process keeps the §2.8 paths: `results/c10x_enginepath/`, `results/c10x_enginepath_r2/` and `results/c10x_enginepath_logs/` (`:124`).
- **A re-run** of a halted or compromised process writes to a new directory, and the driver refuses an existing one:
  - process 1: `results/c10x_enginepath_rerun<k>/`, with logs in `results/c10x_enginepath_rerun<k>_logs/`;
  - process 2: `results/c10x_enginepath_r2_rerun<k>/`, with logs in `results/c10x_enginepath_r2_rerun<k>_logs/`;
  - k = 1, 2, … counts the re-runs of that process;
  - telemetry goes in `<dir>/telemetry/`.
- **Earlier directories.** A halted or compromised directory is never modified, moved or renamed.
- **Dashboard constraint.** No re-run name begins with `attempt` or `_quarantine`. The experiment tab treats such names as set-aside records (`tools/dashboard_experiment.py:182`). It maps a `<name>_logs` directory to its data directory `<name>` (`:295–297`).
- **Each re-run record identifies its valid predecessor explicitly:**
  - the directory it replaces, and that directory's halt or audit cause;
  - for process 2, the process-1 directory it pairs with.

  A replacement with changed telemetry setting cannot join the prior replication pair (T9).
- **Scope.** This rule names directories only. Whether a halted process may be re-run, and after what diagnosis, is governed by §5 (`:188`) and D-C10w-p2rerun.

Nothing else changes: §2.4's gates and tolerances, §2.7's order, caps and refusals, §2.8's records (beyond the two `run.json` keys of (T1) and the re-run provenance of (T12)), §3's readings and §5's halt conditions stand as frozen.

## 11. Amendment M — float64 arithmetic for the ΔW parity checks (2026-10-08, pre-observation)

**What this is.** This is a metric amendment, made before any observation. It sets one uniform rule: every gate input that is a reduction over a full ΔW tensor is computed in float64 on CPU.
- No C10X code, build or run exists. On 2026-10-08, `results/c10x_enginepath*` matches only the five review `.md` files of §8 and the status line, and no `results/c10x_enginepath*` directory exists.
- It changes only the reduction arithmetic of the inputs named in (M1). No floor, tolerance, threshold, acceptance rule, gate, qualifier, label or verdict changes.
- §0–§10 are otherwise unchanged. Where §11 conflicts with §2.4, §2.5 or §3 on the arithmetic of the inputs named in (M1), §11 governs.

**Reason.** Uniform float64 arithmetic for all full-tensor gate reductions follows the P2 precedent (`EXPERIMENT_RUNBOOK.md:377`): same-seed cosines of 1.007–1.009 came from "a 22.5M-element fp32 dot", and float64 gave 1.0000000000. The rule is adopted before any observation. Supporting facts:
- each band update is 2048 × 11008 = 22,544,384 elements (`down_proj` of layers 4–8, `:68`);
- the frozen tolerance rule computes relative L2 "on detached CPU fp32 copies" (`:66`), and -LARGE-WRITE uses the harness's fp32 norms (`:89`, `:149`; `c10e_bandknob.py:213`);
- the cross-family review ruled that a float64 gate replacement "requires its own dated metric amendment, explicitly fixing tensor representation and arithmetic" (`results/c10xy_telemetry_amend_astra.md:33`). This section is that amendment.

(M1) **Scope: the gate inputs covered.**
- the per-layer ΔW relative L2 of X1-(iv) (`:74`), X2-(ii) (the floor, `:76`) and X2-(iii) (`:77`);
- the "complete pre-cast ΔW_8 tensor" relative L2 of X2-(vi) (`:80`);
- the -LARGE-WRITE ratio Σ_l ‖ΔW_l‖_F (arm) / Σ_l ‖ΔW_l‖_F (A), over A7 (`:149`).

Everything else keeps its frozen arithmetic:
- the other §2.4 checks;
- X2-(vi)'s updated-cache relative L2, which is not a ΔW tensor, and its exact comparison of the applied fp16 weight;
- the OverTone objective's declared casts (`:52–56`);
- `fe_edit`'s verbatim lines (`:43`), including its own `delta_norms` record.

(M2) **Tensor representation: the pre-cast update, per layer, for every input in (M1).**
- **Which tensor.** "ΔW" means the float32 `upd` returned by `upd_matrix_match_shape(upd.float(), …)` at `c10e_bandknob.py:212`, before its cast and in-place add at `:216–217`. In `fe_edit`, it is the same statement in its line-for-line copy (`:43`).
- **The frozen text is ambiguous here.** X1-(iv), X2-(ii) and X2-(iii) do not say whether ΔW is the pre-cast update or the applied fp16 weight difference (`:74`, `:76–77`). This section takes the representation that X2-(vi) names, "the complete pre-cast ΔW_8 tensor" (`:80`), for three reasons:
  - X2-(vi) is the only §2.4 text that names a representation for a `my_edit` ΔW tensor comparison.
  - The pre-cast tensor is what the solve produces (`c10e_bandknob.py:205–212`). The applied difference adds the fp16 rounding of `W + upd` (`:217`).
  - The X2-(ii) floor and the comparisons it calibrates must share representation and arithmetic (`:66`).
- **-LARGE-WRITE uses the same quantity as the harness's fp32 `delta_norms`.** The float64 norm is taken over exactly the tensor that `c10e_bandknob.py:213` reduces:
  - the per-layer `upd` after `upd_matrix_match_shape` (`:212`), on CPU (solved at `:209–211`), in float32, before the cast at `:217`;
  - `.float()` at `:213` is a no-op on that float32 tensor.

  The harness computes `float(upd.float().norm())` in fp32 and records it as `delta_norm` (`:213–215`). This section computes `upd.double().norm()` on the same tensor. Each sum Σ_l runs over layers 4–8 of the A7 arm, in the arm and in recipe A of the same process.
- **How it is captured.** No harness edit is made. The capture is a pass-through that returns the identical object and hands a detached CPU fp32 clone to the float64 reduction.
  - **Binding.** Install the pass-through in the global binding actually resolved by each writer, including `fe_edit`, preserving and restoring every original binding in `finally`.
    - For `my_edit`, that binding is `H.upd_matrix_match_shape`: it is imported at `c10e_bandknob.py:15` and called by its unqualified name at `:212`.
    - For `fe_edit`, it is the name its line-for-line copy of `:212` resolves in the driver module's own globals (`:43`).
  - **Count.** Verify exactly one capture per expected layer per compared write, with explicit writer/check/recipe/arm/layer attribution; missing or duplicate captures invalidate the measurement.
  - The pass-through's identity is tested with `is`. The original returns its argument or that argument's transpose (`memit_dry_run/memit/memit/memit_main.py:293–296`), so no value changes.
  - It is installed around the standalone check cells and around every recipe-arm write.
  - It is removed in `finally`. A leftover rebinding HALTs, as a leftover hook does (§5, `:188`).
  - For -LARGE-WRITE, each clone is reduced to its float64 norm at capture time and discarded.

(M3) **Arithmetic: float64 on CPU.**
- **Parity inputs.** For each layer, the two captured fp32 copies `a` (reference) and `b` are upcast on CPU with `.double()`, and `rel = ‖a − b‖_F / ‖a‖_F` and `max|a − b|` are computed in float64. The X2-(ii) floor is the largest per-layer `rel` from the same float64 helper.
- **-LARGE-WRITE.** The per-layer norms and the summed ratio are computed in float64.
- **Unchanged.**
  - Zero references are compared for exact equality.
  - Every finiteness check is explicit.
  - `tol = max(10 × floor, 1e-4)`, with `tol ≤ 1e-4` required (floor ≤ 1e-5, else HALT, `:66`); relative error ≤ 1e-4 passes.
  - X1-(iv) and X2-(iii) use X2-(ii)'s tolerance (`:74`, `:77`).
  - X2-(vi)'s relative L2 ≤ 1e-4 (`:80`).
  - -LARGE-WRITE iff the ratio is strictly > 1.5 (`:149`).
- No float64 tensor is created on MPS (`:58`, `:188`).

(M4) **fp32 beside it, report-only.** For every input in (M1), the record also carries the corresponding fp32 value:
- each relative L2 and max-abs computed in fp32 on the same copies (the frozen arithmetic of `:66`);
- the harness's fp32 `delta_norms` (`c10e_bandknob.py:213–215`) and the fp32 -LARGE-WRITE ratio from them.

Every fp32 value is labelled report-only. It can never affect a floor, tolerance, acceptance, HALT, qualifier, eligibility or verdict. If an fp32 and a float64 value fall on opposite sides of a bound, the record says so, and the float64 value decides.

Nothing else changes.

## 12. Amendment P — pinned context templates (2026-10-08, pre-observation; D-C10z-v4fix)

**What this is.** This is an input amendment, made before any observation. It applies the D-C10z-v4fix forward requirement to C10X: every C10X process uses one fixed, recorded set of context templates instead of drawing its own.
- No C10X run exists. On 2026-10-08, `results/c10x_enginepath*` matches only review and build `.md` files (`_advisor_v1`, `_astra_freeze_v2`, `_v21`, `_v22`, `_codex_build`, `_codex_design_v1`). No `results/c10x_enginepath*` directory exists.
- The LAW#3 predicate (§2.7 step 1, `:100`; `CORPUS/44_C10L_COVGEOM_SPARSEBAND.md:39`) is unchanged. So is every gate, floor, tolerance, threshold, arm, recipe, qualifier, label and verdict rule.
- §0–§11 are otherwise unchanged. Where §12 conflicts with them, §12 governs. The two superseded sentences are quoted exactly in (P4).
- **Citation snapshots.** Driver line numbers in (P1)–(P3) refer to the working-tree `experiments/track_c/c10x_enginepath_arms.py` as read on 2026-10-08, SHA-256 `5b20af52…`. That file is untracked and under active edit, so its line numbers must be re-checked at the build review. The pre-pin driver described in (P0) was read earlier the same day. It was not retained as a snapshot, and its line numbers can no longer be re-checked; they are marked "pre-pin".

(P0) **Why.**
- **ASTRA's halt.** ASTRA (C10Z) process 1 halted HALTED-V4 on 2026-10-08 (`results/c10z_astra/run.json`, `halt`). Its recipe A gave A7 first 40, full 7 and canon 7 (of 72, 72 and 24), with A1 69 and A2 69 (`results/c10z_astra/halt_p1.json`, `recipes.A`).
- **A seeded draw.** The ASTRA driver called `torch.manual_seed(0)` before it imported the harness (`experiments/track_c/c10z_astra_arms.py:506–507` at commit `f4ceb71`, the process-1 source). The engine samples its context templates with top-k multinomial sampling (`memit_dry_run/memit/memit/memit_main.py:304–323`; `memit_dry_run/memit/util/generate.py:115–120`). Earlier seed-0 processes recorded `e8605172dce0`; ASTRA's unrecorded set is inferred from matching call order and baseline measurements, not directly observed. Reproduction depends on matching RNG consumption and execution conditions. The recorded seed-0 baseline (`results/autoresearch_c10_equivalence.json:150`, `:155`, `:160`, `:196–197`, `:203`) lies below the A4 envelope, which was built from unseeded draws (`results/c10z_astra_v4_diagnosis.md:37–54`).
- **C10X had the other half of the problem.**
  - No C10X file seeds the global RNG. A grep on 2026-10-08 of `c10x_enginepath_arms.py`, `c10x_overtone_z.py`, `c10x_enginepath_inertness.py`, `c10x_enginepath_read.py`, `c10x_enginepath_telemetry_check.py` and `c10e_bandknob.py` found no `manual_seed`. The only seed is a local `torch.Generator` in the selftest (`c10x_enginepath_selftest.py:591`).
  - The pre-pin driver sampled the templates unseeded (pre-pin `:1072`), before recipe A and before the LAW#3 check.
  - §2.7 states that process 2 resamples (`:106`), and §2.8 lets the reader combine processes whose context lists differ (`:124`). Processes 1 and 2 would therefore not share write inputs, and each process's recipe-A comparator would be a different draw.
- **The template list was lost on a halt.** The pre-pin driver stored `ctx` and `ctx_sha256` only in its completion update (pre-pin `:1104`). A LAW#3-miss record would therefore not have identified its templates, although §2.8 requires every record to carry the list and its hash (`:124`).
- **What pinning gives.** It gives every process the same write inputs, with a set whose recorded counts lie inside the envelope (C10Q: A7 first 52, full 12, canon 8; A1 70, A2 71; `CORPUS/50_C10Q_STACKED_SOLVE.md:14`). It also gives C10X the same recipe-A inputs as ASTRA's benchmark. Results are conditional on this fixed set.

(P1) **The pinned set.**
- **Set.** The C10Q recorded set, `c7dabbe7c25a`. In engine form it is `[["{}"], [five prefixes]]`, as printed at `results/c10q_stacked/logs_run.log:9`.
- **Source.** The driver takes `TEMPLATES` from `experiments/track_c/c10z_astra_benchmark.py:34–40`, the list ASTRA's benchmark froze. It parses the file and does not execute it (`recorded_contexts`, `:103–117`). The engine form is `[[TEMPLATES[0]], list(TEMPLATES[1:])]`.
- **Digest checks.** These run before recipe A. Any failure HALTs (§5) with a diagnostic, and recipe A does not run.
  - The list has six strings, each with exactly one `{}`, and the first is `"{}"`.
  - `hashlib.sha256(json.dumps(engine_form).encode()).hexdigest()` equals `c7dabbe7c25a7e58653621d9cc66e37b35c865ae09b73b6a96073a184c6c98da` (`C10Q_CONTEXT_SHA`, `:31`). Its 12-hex prefix is the scorer's convention (`experiments/track_c/autoresearch_c10/scorer.py:106`).
  - The SHA-256 of `json.dumps(list(TEMPLATES), sort_keys=True, separators=(",", ":"), allow_nan=False)` equals `d6c7c70026dced37bddc6adf316a3487d70227dae80a6e0ed5cdabe50caedfa0`. This is the benchmark's `_digest` (`c10z_astra_benchmark.py:69–71`) and the `inputs.templates_sha256` of `results/c10z_astra_benchmark/20261008T104535Z/benchmark.json`. The driver records this value (`:117`); it must also compare it.
- **Source binding.** `experiments/track_c/c10z_astra_benchmark.py` is in the driver's declared source set (`source_hashes`, `:87–94`; §2.8 `:124`). The digest checks still govern: a changed benchmark file that keeps `TEMPLATES` byte-identical passes them, and a changed list halts.

(P2) **Where the pin goes.** In every C10X process, the driver sets the engine's `CONTEXT_TEMPLATES_CACHE` (`memit_main.py:21`) to the checked engine form at setup (`:1103–1104`; `pinned_contexts`, `:121–131`). This is before the stimulus checks, `probe_setup`, recipe A (`:1115–1116`) and recipe A's first engine edit (`run_law5`'s `apply_memit_to_model`, `c10e_bandknob.py:422–423`). With the cache set, `get_context_templates` returns without sampling (`memit_main.py:307`), and the driver asserts that it does (`:1110`). The `ctx` used by every target solve, X check, probe and recipe is then the pinned set. The setting is a driver assignment, not an engine edit, following the C10U, C10V and C10Y precedents.

(P3) **Records.**
- `<OUT_DIR>/context_templates.json`, holding the engine form, its SHA-256 and its source, is written before recipe A (`:1105`), and so before the LAW#3 check (`:1118`).
- `ctx` and `ctx_sha256` enter the run state at setup (`:1106`). The halted `run.json` therefore carries them too, because the halt path writes that state (`:1170–1176`), and a LAW#3 miss identifies its templates.

(P4) **Superseded text.**
- §2.7's process-2 parenthetical (`:106`), "(context templates resample per process, `CORPUS/44:32`; the template hash and the frame texts are recorded in both)", now reads: "(both processes use the pinned templates of §12 and check their digests; the template hash and the frame texts are recorded in both)".
- §2.8 (`:124`), "The reader combines processes only if scientific configuration, source, weights, stimuli and pre-registration hash match, with only the sampled context list and the resulting targets and frames allowed to differ; same-file or same-process reuse is not replication.", now reads: "The reader combines processes only if scientific configuration, source, weights, stimuli and pre-registration hash match, and both context lists and frame texts match the §12 pin; independently recomputed targets remain subject to existing checks. Same-file or same-process reuse is not replication."
- Replication now tests fixed-template regeneration, not robustness across template draws.
- §2.1's engine fact (`:31`) is unchanged: the engine still samples when its cache is empty, and the pin keeps it from sampling.

(P5) **No template sampling, tested first.** CPU tests with a stub model, written and recorded failing on the pre-amendment driver, must show that:
- a C10X process installs the pinned set before its first `get_context_templates` call and never calls `generate_fast` for templates;
- `context_templates.json` exists before the LAW#3 check;
- a changed `TEMPLATES`, or either digest mismatch, halts before recipe A;
- a LAW#3-miss record carries `ctx` and `ctx_sha256`;
- process 2 builds the same `ctx` as process 1, and the reader refuses to combine processes whose context lists or frame texts differ from the pin.

(P6) **A LAW#3 miss under the pinned set** is a real HALT under §5, with no re-draw and no template change.

Nothing else changes.
