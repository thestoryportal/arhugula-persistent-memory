# Pre-registration — D-C10y-directdw: the band's ΔW optimised directly through the deployed forward pass (DOW-KE), against the closed-form write, an anchor-closure sham and a norm-matched control (step 7 of the research pass's recommended sequence; H-3) (FROZEN v2.2, 2026-10-07)

**Status: FROZEN v2.2 (2026-10-07) — GPT-6-Astra high: freeze check FIX-FIRST (results/c10y_directdw_astra_freeze_v2.md, 7 BLOCKING) folded in v2.1; confirmation FIX-FIRST (results/c10y_directdw_astra_freeze_v21.md, 3 BLOCKING) folded in v2.2; second confirmation FREEZE (results/c10y_directdw_astra_freeze_v22.md). MEASUREMENT-ONLY, not a write route.** Nothing has run; no code written. Decision-ID `D-C10y-directdw`. Classification: **MEASUREMENT-ONLY, not a write route** (§2.7; D-C10r-rulings-3 (2), `EXPERIMENT_RUNBOOK.md:330`; D-C10u-Aenv (2), `:343`). Building is authorised model-free under D-C10r-rulings-9 (3). Execution remains GATED on the recorded reconsideration required by D-C10r-rulings-4 (3), after steps 3, 4 and the step-5 oracle have been read. That reconsideration may be made under the existing D-C10r-rulings-8/9 standing approval and must be recorded before dispatch. Step 7 is MEASUREMENT-ONLY under D-C10u-Aenv (2). A low oracle result informs the spending recommendation; it is not a proved capacity bound and does not mechanically invalidate this different writer. No mandatory two-process block is authorised by the queue's build instruction. (`EXPERIMENT_RUNBOOK.md:331,338,342–343`; `docs/INTEGRATED_QUEUE_2026-10-07.md:18–22`.) Reviewer conflict, resolved conservatively: the runbook's correction entry says steps 6–7 "are re-argued with the operator before scheduling" (`EXPERIMENT_RUNBOOK.md:914`), so this document recommends that the operator make the reconsideration (§6 decision 0; §8 Open for the program). When it runs: stage 1 only (§2.6 item 5), one GPU job at a time, after the GPU items ahead of it in `docs/INTEGRATED_QUEUE_2026-10-07.md:18–22`.

Source lead: research pass 2026-10-06, H-3 (`results/research_pass_2026-10-06/hypotheses.md:41–50`); `recommended_sequence.md:27` (step 7 row) and appendix `:54`; `prereg_stubs.md:73–80` (§Step 7) and `:5–13` (§Shared contract); `council_critique.md:13, :66, :88, :167, :244` (reproducibility and write-size items that bind any gradient writer); `docs/INFRANODUS_RESEARCH_ARC_2026-10-05.md:50` (DOW-KE row: "eval | no | paraphrase | autoregressive | closure gap"). Paper: DOW-KE, arXiv 2608.16932 v1 (Chen, Zhang, Zhou, Deng, Jiang), read 2026-10-07 from its LaTeX source: §3.2 (anchor-target objective), §4.1 (closure gap, Fig. 1–2), §4.3 (removing the anchor), §5 (method), §6.2 (setup, Table 1), §6.4 (Tables 2–3). No public code is located (`hypotheses.md:44`). The LaTeX source is not retained in this repo: the local extract `results/infranodus_research_arc_2026-10-05/fulltext/DOWKE_2608.16932.md` confirms the Table 1 and Table 2 numbers used here (`:158`, `:403`) but carries no §4.1 or §5 body, so r_gap ≈ 0.33 and the §5 quotations below are UNVERIFIABLE from the repo; no threshold depends on them (advisor Checks; Codex #7). Lineage: CORPUS/44 ⟨D-C10l-covgeom@af2e38f7⟩ (P6 injection 49/72 vs weight edit 13/72; ρ correction `:43`), CORPUS/46 ⟨D-C10m-diag@9a9b5343⟩ (F-D1 collateral bucket), CORPUS/47 ⟨D-C10n-ztransport@982edcbd⟩ and CORPUS/48 ⟨D-C10o-magnitude@31389765⟩ (the edited model decodes a rotated target), CORPUS/50 ⟨D-C10q-stacked@8e5c7f12⟩ (re-aim in place 12 → 24/72 at a ×1.24 second write and a 4.2-point `described_as` cost), CORPUS/53 ⟨D-C10t-secondkey@76a722d3⟩ (×2.05 write with prefix-conditioned spillover). Rulings in force: D-C10k-rulings-1 (strict held-out bar), D-C10k-rulings-2 (Qwen anchor), D-C10r-rulings-3 (2) (write-only, quoted in §2.7), D-C10r-rulings-4 (3) (`EXPERIMENT_RUNBOOK.md:331`: steps 6–7 demoted behind steps 1–4 and the step-5 oracle, 'decided again only after those results'), D-C10r-rulings-8 (`:338`, standing approval), D-C10r-rulings-9, D-C10u-Aenv (2) (`:343`: step 7 carries "measurement, not a route"). Conventions follow `docs/C10V_LAYERPICK_PREREG.md` (v2) and `docs/C10U_MINT2_PREREG.md` (v3). Every engine, harness and library statement below cites a line read on 2026-10-07 (LAW#4).

**Binding rules, quoted (CLAUDE.md).** LAW#4: "Before writing any cell that depends on engine internals, `cat -n` the relevant engine source and author from what it actually does. Never reconstruct engine call signatures, context-template prep, or lookup logic from memory." LAW#5: "Any source change to the science-bearing edit path (`compute_z` / `execute_memit` / `repr_tools` / the solve) must be isolated against a known-ceiling reference result and proven inert (LAW#5) before any verdict produced under it is promoted. Demonstrate inertness; do not assume it. The MEMIT engine, LARQL, and git stay **UNMODIFIED**." The writer below is a new harness-side solve: it calls the engine's `compute_z` and `compute_ks` and reads the covariance cache, all read-only, and changes nothing under `memit_dry_run/memit`.

## 0. Where this sits, and what it is

**The e2e map (`docs/SPEC_E2E_GROUND_TRUTH.md` §C, `:22–30`).** Write layer, step 5–6 of the §C flow: the Commit Executor's compile of the `.larql` patch into an overlay, and the `COMMITTED` ledger entry "with overlay hash" (`:30`; spec `:671`). The arm replaces one step inside the compile — how the closed form's per-layer residuals are allocated — and keeps the write site (`down_proj` of layers 4–8), the key (subject-last), the target solver and the preservation projector. Read against the **§8.9 L2 behavioural bar** (e2e §F, `:64`). Shape: **Genesis-shaped** (one batch of 24, e2e §D `:32`); the Incremental shape (sequential overlays) is not tested. Lifecycle cells it touches by implication and does not test: compaction is "a full MEMIT re-run on all active `.larql` patches" (e2e §E, `:54`), so a writer that is not bit-reproducible changes what compaction regenerates (§2.7); the Write Lock has a 60-minute TTL (`:62`; spec `:783`) and the PREPARED window defaults to 2 h for incremental writes (spec `:678`), so the writer's wall-clock is a spec-fit readout. Nothing in the read, governance or deployment layers is touched. **§0.3 / queue:** step 7 of the agreed sequence (`recommended_sequence.md:27`).

**Correction carried into this document — the "3 %" premise is reversed.** The research pass frames H-3 as matching "the program's own finding that the edit realises only about 3 percent of its target at the keyed position" (`hypotheses.md:43`; `recommended_sequence.md:13`, `:27`). That reading is withdrawn: ρ_c is a *remaining*-residual ratio, `rho_c_band = ‖z − cur_after‖ / ‖z − cur_before‖` (`experiments/track_c/c10l_covgeom_step0.py:134`; `rel` at `:74–75`), so the 0.028 of step 0 means ≈ 2.8 % of the canonical residual norm **remains** after the band write; ≈ 23 % remains on paraphrase prompts (ρ_p 0.232) (`CORPUS/44_C10L_COVGEOM_SPARSEBAND.md:25`, correction `:43`; `docs/C10V_LAYERPICK_PREREG.md:9`). DOW-KE names the analogous quantity the terminal closure gap `r_gap = ‖z − h̃‖/‖z − h‖` (2608.16932 §4.1; definitions may differ). ρ is a remaining-residual norm ratio, not the percentage of facts installed. Offline reconstruction reported ρ_c≈0.028 and ρ_p≈0.232, with a behaviourally uninformative paraphrase proxy (CORPUS/44:25,43). A subsequent single-key in-harness reference reported 0.032650/0.233728 (CORPUS/53:62). The paper's approximately 0.33 and exact method quotations remain UNVERIFIABLE until their source/version is retained. They do not set a threshold or justify a quantitative cross-model comparison. This run records its own merged-model residuals, comparable in scope to CORPUS/53; it is not fulfilling an as-yet-unmeasured obligation. Consequences: (a) the anchor-closure half of DOW-KE has little room at the canonical position here, which is what arm B-z tests (§2.5) with a stated NULL prior; (b) the case for H-3 rests on the other half of the paper's principle — "what is optimized must be exactly what is deployed" (abstract; §4.3) — i.e. the edit objective evaluated in the edited model, which is where the program's evidence points: injecting the target on the unedited model carries the value (24/24, 49/72, `CORPUS/44:23`), injecting the same target on the edited model does not (23/72, `CORPUS/46:17`, F-D1 `:30`), the edited model decodes a rotated ≈ 30 %-longer target instead (`CORPUS/47:21`, F-Z2 `:26`; DIRECTION, `CORPUS/48:22`), and a second in-place write aimed at that re-solved target doubled held-out recall at a write and locality cost (`CORPUS/50:15`, F-S1 `:25`). An end-to-end objective re-aims the write inside the deployed forward pass at every step, with no intermediate target to go stale. **Second inherited premise, withdrawn.** The inherited statement 'later value tokens have no objective' (`recommended_sequence.md:13`) is withdrawn. compute_z labels every target token and averages their NLL (`memit_dry_run/memit/memit/compute_z.py:60–65,141–150`). The closed-form weight solve reads subject-last keys and a keyed block-output residual; it has no direct value-position loss (`experiments/track_c/c10e_bandknob.py:196–211`). B-e2e changes the optimisation variable and the model in which the loss is evaluated, not the target-token coverage of compute_z.

**What this experiment can and cannot conclude.** A pass advances one candidate configuration (one parameterisation, one optimiser setting, one batch of N = 24, one model). A miss means *this configuration was not advanced*. The stub's "NULL → the layers cannot hold the value; model axis" (`prereg_stubs.md:79`) is not adopted: one optimiser setting cannot establish what the layers can hold.

## 1. Question and hypotheses

- **H-Y1 (end-to-end objective — the claim under test).** Optimising each band layer's update `ΔW^l = A^l B^l` (B^l the closed form's own solution operator, held fixed; A^l free) against the target-token NLL **evaluated in the model carrying all five updates**, with the KL term on the essence prompt, raises A7 held-out full-sequence recall over the same-process closed-form write (recipe A), at the same locality, and not merely by writing larger.
- **H-Y2 (anchor closure — the research pass's stated premise).** Optimising the same parameterisation to close the residual to the engine's own target at the anchor (block-8 output at the subject-last token) raises recall. **Prior: NULL** — the canonical gap is already ≈ 2.8 % (§0), and removing the projector, which leaves 0.8 %, made canon worse (7 → 4, `CORPUS/44:29`).
- **H-Y0 (null).** Neither moves A7 outside the identical-baseline envelope.
- **H-Y3 (trade-off).** B-e2e gains, but through a larger write that leaks (the CORPUS/50 and /53 pattern: ×2.24 total write with `described_as` −4.2, `CORPUS/50:15`; ×2.05 with ten failed per-prefix gates, `CORPUS/53:29, :33`). The norm-matched control (§2.5) separates this from H-Y1.
- **Expectation stated now.** The nearest analogue the program has run is the in-place re-aim (CORPUS/50: 24/72, TRADEOFF). The likeliest outcomes for B-e2e are therefore TRADEOFF or a LARGE-WRITE-qualified gain; LEAD (≥ 30/72) is not the expected outcome. B-z is expected to sit inside [5, 18]/72 and within 5 of recipe A. DOW-KE's reported gains are CounterFact first-token metrics on real entities (Llama-3-8B generalization 96.64 vs AlphaEdit 94.22, Table 1), not this bar (`hypotheses.md:49`).

## 2. Design (engine unmodified; one new harness-side writer in a driver; recipe A and the LAW#5 gate run the untouched path)

### 2.1 Engine and harness seams, read 2026-10-07 (LAW#4)

- **Model** `Qwen/Qwen2.5-3B` @ `3aab1f19…` (`experiments/track_c/c10e_bandknob.py:25–26`), loaded fp16 on MPS (`:48`). Config (`hf_cache/hub/models--Qwen--Qwen2.5-3B/snapshots/3aab1f1954e9cc14eb9509a215f9e5ca08227a9b/config.json`): hidden 2048 (`:9`), intermediate 11008 (`:11`), 16 attention heads (`:15`), 36 layers (`:16`), 2 KV heads (`:17`), tied embeddings (`:21`), vocab 151936 (`:27`).
- **Hparams** `configs/hparams/qwen25_3b_memit_hparams.json`: `layers` [4–8] (`:2`), `clamp_norm_factor` 0.75 (`:3`), `fact_token` `subject_last` (`:5`), `v_num_grad_steps` 25 (`:6`), `v_lr` 0.5 (`:7`), `v_loss_layer` 35 (`:8`), `v_weight_decay` 0.5 (`:9`), `kl_factor` 0.0625 (`:10`), `rewrite_module_tmp` `model.layers.{}.mlp.down_proj` (`:13`), `lm_head_module` `model.embed_tokens` (`:19`), `mom2_n_samples` 100000 (`:21`).
- **Target solver** `compute_z(model, tok, request, hparams, layer, context_templates)` (`memit_dry_run/memit/memit/compute_z.py:14–21`): target ids from `tok(request["target_new"]["str"])` (`:41–43`); rewriting prompts `context.format(prompt) + decode(target_ids[:-1])` over every context template, KL prompts `["{} is a"]` (`:46–50`); one padded batch (`:53–57`); targets placed at `ex_len − len(target_ids) : ex_len` (`:60–65`, which presumes right padding); lookup index = subject-last token per prompt (`:68–73`); `loss_layer = max(v_loss_layer, layer)` = 35 (`:76`); one `delta` added at the lookup index of every prompt at the rewrite layer, `target_init` recorded from prompt 0 (`:90–99`); Adam on `delta` at `v_lr` (`:104`) for `v_num_grad_steps` (`:108`); NLL from the loss-layer output through `ln_f` and the tied head (`:137–140`), per-prompt mean over target positions and mean over prompts (`:149–150`); KL `kl_factor · kl_div(kl_distr_init, kl_log_probs, log_target=True, batchmean)` (`:151–153`); weight decay on ‖delta‖ (`:154–156`); stop when the total loss < 0.05 (`:164`); clamp (`:175–178`); returns `target_init + delta` (`:180`). **The engine already runs a per-patch gradient loop** (at most 25 loss evaluations and 24 Adam updates per fact, `compute_z.py:108,164–172`); this matters for §2.7.
- **Keys** `compute_ks` = `down_proj` input at the subject-last token averaged within each context group and then equally across groups (here identity weight ½ and each sampled context weight ⅒), one row per request, from `prompt` and `subject` only (`memit_dry_run/memit/memit/compute_ks.py:11–50`).
- **Engine solve and caches.** `execute_memit` solves every z before its layer loop (`memit_main.py:100–149`) and recomputes `cur` after each layer's edit (`:152–169`); float64 is used only on CPU — "MPS has no float64" (`:49`, `:191–194`); covariance served from the process cache `COV_CACHE` keyed by `(model_name, layer_name)` (`:256–259`), stored as CPU float32 (`:280`); context templates sampled once per process into `CONTEXT_TEMPLATES_CACHE` (`:21`, `:304–323`).
- **Harness closed form** `my_edit(hp, requests, P, cache_c)` (`c10e_bandknob.py:181–221`): `z_layer = layers[-1]` (`:184`); targets from `Z_OVERRIDE` when every `(subject, target str)` key is present and the call is not the LAW#5 check, with `Z_OVERRIDE_HITS` counted (`:185–189`), else `compute_z` per request (`:191`); per layer: `K = compute_ks(...).T` (`:196`), `cur` = block-`z_layer` output at the subject-last token of the canonical prompt (`:197–201`), `resid = (zs − cur)/(len(layers) − i)` (`:202–204`), `A = P(KKᵀ + cache) + L2·I`, `B = P K residᵀ`, `upd = solve(A, B)ᵀ`, float32 on CPU (`:205–211`), added to the fp16 weight before the next layer's keys are read (`:216–217`); post-edit cache update (`:218–220`). `L2 = 1.0`, `NULL_THRESH = 0.005` (`:28–29`); `compute_P` = one projector per layer from the covariance's SVD, kept where singular value < 0.005 (`:166–178`; SVD `:173–175`).
- **Recipe runner** `run_recipe(name, hparam_path)` (`:458–509`): projector (`:462`), LAW#5 gate before the arms (`:463`; `run_law5` `:415–446`, pass = `|Δexpr| < 0.05 and |Δloc| < 3`, `:444`); per arm restore and zero cache (`:473–474`), 24 requests `req(CANON, c, value)` (`:480`; `req` `:96–97`), `my_edit` called by module-global name (`:489`), evaluation (`:490–493`), hooks (`:494–495`), ΔW norms (`:498`). Seams: `ARM_HOOKS` (`:404`), `Z_OVERRIDE`/`Z_OVERRIDE_HITS` (`:407–408`), `_LAW5_DEFAULT_CTX` (`:403`), `_ARM_STATE` (`:412`).
- **Stimuli and readouts.** `CANON`, `PTEST` (three sealed held-out templates), `FICTION` (`:51–61`); arms A1 single-token, A2 coherent two-token, A7 coined two-word values (`:224–250`); `full_seq_match` (`:109–117`), `string_match` (`:121–130`), `teacher_forced_pertok` (`:134–143`); `eval_arm` with exact counts (`:358–400`); L1 = 12 real countries, L3 = 30 unedited capitals (`:259–278`); `GENERIC` 20 sentences and perplexity (`:279–308`); `axes_post` (`:319–339`); `described_as` on the 24 edited subjects (`:475–476`, `:492`); covariance-cache SHA-256s (`:342–355`). Same-frame probe: `FRAME_SUBJECTS` (`experiments/track_c/c10p_twopass_arms.py:30`) and `frame_probe` (`:36–42`), six never-edited subjects in the CANON frame, flip = top-1 is the first token of any edited A7 value.
- **Fingerprint** `tools/engine_fingerprint.py`: expected SHA-256 `d941a9fb…` (`:34`) and the `_cov_cpu` site count (`:42`).

### 2.2 The parameterisation — DOW-KE §5 on this harness, derived from `my_edit:209–211`

DOW-KE §5 observes that the AlphaEdit closed form factors as `Δ = R B`, with R the allocated residuals and B "a solution operator built solely from the edit keys and the preservation statistics", and optimises a free `A^l` in place of R with B fixed. On this harness, for layer l with keys `K_l` (11008 × 24), residuals `R_l` (2048 × 24), cache `C_l` (zero for a fresh arm, `:474`) and projector `P_l`, write `M_l = K_l K_lᵀ + C_l` and `𝒜_l = P_l M_l + L2·I`. By linearity of the solve, `solve(𝒜_l, P_l K_l R_lᵀ) = X_l R_lᵀ` with `X_l = solve(𝒜_l, P_l K_l)` (11008 × 24), so

  **ΔW^l_A = R_l B_l,  B_l := X_lᵀ (24 × 11008).**

From `𝒜_l X_l = P_l K_l`: `X_l = P_l (K_l − M_l X_l) / L2` (L2 = 1.0, `c10e:29`), so in exact arithmetic, for an orthogonal P_l, X_l lies in the range of P_l (an orthogonal projector, `U Uᵀ` from the SVD at `:173–175`) and **`B_l k = 0` for every key k with `P_l k = 0`**, the covariance directions with singular value ≥ 0.005. Hence `ΔW^l = A^l B_l` is zero on the protected span **for every A^l** — the property DOW-KE builds into its parameterisation ("for any k ∈ span(U_τ), B^l k = 0; hence Δ^l k = 0 for every A^l", §5), here with the harness's own projector. The constraint is exact in exact arithmetic; it carries no penalty weight. ΔW = AB has rank ≤ 24 before finite-precision materialisation; the implementation tests numerical factorisation and projector tolerances, and does not assert bit-exact factorisation or exact preservation of the quantised deployed update (§2.8 (v) gates the planned and the actual applied update). Each update is rank ≤ 24 and lives in the closed form's own row space; the program measured R0's ΔW null-space share at 1.000 (`CORPUS/44:25`), and V7 (§3) requires the same of every optimised write.

**Capture solve.** `R_l` and `B_l` depend on the sequential state: layer l's keys and `cur` are read after layers < l were edited (`:196–201` follow `:217`). The driver therefore recomputes `my_edit`'s loop line for line (`:194–217`: same `compute_ks`, same `get_module_input_output_at_words` call, same `resid`, same float32 CPU solve, same fp16 addition) and records `R_l`, `X_l`, `B_l` per layer and arm; LAW#5 check (ii) (§2.8) proves this capture equals `my_edit`'s write. **Initialisation:** `A^l(0) = R_l`, so the zero-step write is recipe A's write exactly (check (iii)).

### 2.3 Objectives

- **B-e2e (DOW-KE, eq. "DOW-KE objective" in §5).** `L = L_edit + 0.0625 · KL_raw`, the coefficient applied exactly once (Codex #17), both evaluated on the model carrying all five updates. **Deployed arithmetic (Codex #16).** Optimisation forwards use the deployed effective weight arithmetic: `W_eff^l = fp16(W0^l + fp16(A^l B_l))`, with `A^l B_l` computed in float32 and `W0^l` the pristine fp16 band weight, detached and frozen, and the same module input dtype and kernel path as final deployment (the linear `down_proj`, `.venv/lib/python3.11/site-packages/transformers/models/qwen2/modeling_qwen2.py:53–59`). It is implemented as a forward hook on each band `down_proj` that returns `F.linear(input, W_eff^l)` in place of the module output; the driver does not train through the sum of a base output and a separately evaluated low-rank output. The fp16 casts' backward and the subject routing below are explicitly surrogate-gradient choices; forward values match deployment. `L_edit` is built exactly as `compute_z` builds its rewriting loss: the same rewriting prompts (`compute_z.py:46–50`), tokenisation (`:53–57`), target placement (`:60–65`) and per-prompt / per-request means (`:149–150`), averaged over the 24 requests; NLL read from the final hidden state through `model.norm` and the tied head **at the target positions only** (memory, §2.10). **KL (Codex #17).** `KL_raw = F.kl_div(log_p_pristine, log_q_current, log_target=True, reduction='batchmean')` over the 24 `"{} is a"` rows at the subject-last index, i.e. KL(q_current ‖ p_pristine), unweighted — the expression of `compute_z.py:151–153` before its `kl_factor`; the pristine log distribution is computed once and detached; raw and weighted KL are recorded separately. The new objective deliberately has no activation-vector weight-decay term (`compute_z.py:154–156`); the total loss is not `compute_z`'s total (departure D-12). **Gradient routing (DOW-KE §5, Table 2 row 4):** in `L_edit` only, for positions t before the subject-last index `s_i` of each rewriting sequence (`compute_z.py:68–73`), the hook takes its output from `W_eff,det^l = fp16(W0^l + fp16(A^l.detach() B_l))` (identical in value), selected per position by a mask, so those positions reach A^l only through later keys; forward values are unchanged. The KL term uses the standard path. **Graph hygiene (Codex #17).** Base parameters frozen with their gradients asserted absent; only A is optimised; eval mode, no `no_grad`/inference context around the differentiable forward, `use_cache=False`.
- **B-z (anchor closure; doubles as the stub's sham, `prereg_stubs.md:76`).** Same parameterisation, init and optimiser; objective = closure of the engine's own anchor, as DOW-KE §3.2 defines it, across the same rewriting prompts: with `δ_i = z_i − h⁰_{i,0}` (the solved delta; `z = target_init + delta`, `compute_z.py:95, :180`) and `h_{i,j}` the block-8 output at the subject-last token of rewriting prompt j in the edited model, `L_z = mean_i [ Σ_j ‖h_{i,j} − (h⁰_{i,j} + δ_i)‖² / (J ‖δ_i‖²) ]` (J = number of rewriting prompts; `h⁰` pristine). On the identity template this is the squared remaining ratio of step 0. The forward may stop after block 8 (implementation-review item: a truncated forward or a full one; a full one only costs time). Gradient routing as in B-e2e. Deployed arithmetic and graph hygiene as in B-e2e. Evaluate the zero-denominator rule at every B-z objective and fit evaluation. For `||δ_i||=0`, a zero residual contributes zero; any nonzero residual immediately yields INVALID-ANCHOR-NORMALISATION. Do not evaluate a masked 0/0 expression.

### 2.4 Optimiser hyperparameters — fixed now, with reasons (DOW-KE's are in its supplementary Appendix A, §6.2, which is not in the arXiv source; every value below is this program's)

| knob | value | reason |
|---|---|---|
| free variable | `A^l ∈ ℝ^{2048×24}`, float32, l = 4…8 (245,760 numbers) | DOW-KE §5 |
| fixed operator | `B_l` from the capture solve, float32 | DOW-KE §5 "keeps B fixed" |
| initialisation | `A^l(0) = R_l` | zero-step write = recipe A exactly; makes every B arm a refinement of A and gives check (iii) |
| optimiser | Adam, β = (0.9, 0.999), ε = 1e-8, no weight decay | the optimiser class `compute_z` uses (`compute_z.py:104`); DOW-KE's objective has no norm penalty |
| learning rate | per layer `lr_l = 0.02 · rms(R_l)` (rms over the 2048 × 24 entries), constant | an unmeasured fixed heuristic, not a proved fair optimisation budget and not a bound on write growth (Adam normalises moments; an entrywise bound on A does not bound ‖AB‖/‖RB‖; Codex #13); actual per-layer norms are recorded every step and the fit rule (§3) applies at every stop |
| step cap | T_max = 100 optimiser steps per write | 4 × `v_num_grad_steps` 25 (hparams `:6`) for ≈ 120 × the variables of one z; compute budget (§2.11) |
| stopping rule | B-e2e: stop before the update when total loss `L < 0.05`; B-z: stop when `L_z ≤ 1e-4` (remaining ratio ≤ 1 % in RMS); else at T_max | B-e2e uses the anchor solver's own threshold (`compute_z.py:164`); B-z's is the closure the stub asks for; the fit rule (§3) is tested at every termination, threshold or cap (Codex #4) |
| constraint weight | `0.0625 · KL_raw`, applied once (hparams `:10`; §2.3); the null-space constraint is exact (§2.2), no penalty weight | DOW-KE §5: "the same losses as in Eq. (anchor loss)" |
| key-side projector | the harness's P (`NULL_THRESH` 0.005, absolute, `:28`, `:173–175`) | keeps the protected subspace identical to recipe A, so only the optimisation differs (departure D-1) |
| output-side projector | none | no unrelated-output second moment `D_0` is cached; computing one is a covariance-scale job, unmeasured here (departure D-2) |
| gradient routing | on, edit loss only | DOW-KE §5, Table 2 row 4 (generalization +1.02, specificity −1.38 on Llama-3-8B) |
| scale α | 1 | DOW-KE §6.4 default |
| precision | fp16 frozen model; A, B and the low-rank product float32; forward through `W_eff = fp16(W0 + fp16(AB))` (§2.3); static loss scale 2¹⁰. Per accepted step: zero the accumulated gradients, scale the loss, backpropagate, unscale the A gradients exactly once, test finiteness, call `Adam.step`. An overflow discards all micro-batch gradients and changes neither A nor the Adam moments or step counter; the scale is halved and the step retried; retries are bounded (V10) and recorded separately from accepted updates (Codex #17). No float64 on MPS (`memit_main.py:49`); any float64 diagnostic or solve first moves its tensors to CPU | the deployed precision; the program's first step-2 attempt halted on float64 on MPS (`EXPERIMENT_RUNBOOK.md:42`) |
| batching | the objective is the full-batch mean over 24 requests; gradients accumulated over 4 micro-batches of 6 requests per optimiser step | memory, §2.10; check (vi) tests accumulation parity on a fixed 12-request subset (Codex #9) |
| seed | `torch.manual_seed(0)` at process start and before each write | no stochastic component is expected; recorded |
| deployment | after the last step, `W_l += (A^l B_l).to(fp16)` as `my_edit:216–217` does; the merged fp16 model is the one scored | DOW-KE's principle: score what is deployed |

### 2.5 Recipes and arms (A1, A2 and A7 under every recipe, except that the stage-1 screen runs B-e2e on A7 only; stages in §2.6 item 5)

- **A — closed-form baseline**, the harness as it stands (`my_edit` untouched), with the driver's pre-solved targets supplied through `Z_OVERRIDE` (§2.6). Its A7 count is the comparator; its envelope is the LAW#3 gate.
- **B-z — anchor-closure / sham** (§2.3). Reproducing A within the envelope is the expected outcome; a gain revives the closure account on this harness.
- **B-e2e — DOW-KE proper** (§2.3). The candidate.
- **B-e2e-NM — total-norm control (conditional in stages 2 and 3, never stage 1; run iff `N_B > N_A`; advisor #11b, Codex #11b).** Let `D_B,l` be the actual effective candidate update and `N_B = Σ_l ‖D_B,l‖_F`; define `N_A` analogously. If `N_B > N_A`, use one scalar `s = N_A / N_B < 1` for all layers and apply `s·D_B,l` to the same pristine band (mode `apply_stored`). No layer is scaled up. Measure the merged control's actual updates: the summed norm must match `N_A` within 1 %, with per-layer direction cosine to `D_B,l` ≥ 0.999 for nonzero updates. Otherwise the size control is SIZE-UNTESTED. All readout/validity/locality/fit checks applicable to this stored-update path still apply. If `N_B ≤ N_A`, no NM-total is required, but the per-layer size question is not moot (B-e2e-ENV).
- **B-e2e-ENV — per-layer envelope control (conditional in stages 2 and 3, never stage 1; run iff `s_env < 1`; Codex #18).** `s_env = min(1, min_l ‖D_A,l‖_F / ‖D_B,l‖_F)`, the inner minimum taken only over nonzero candidate layers; a zero reference layer with a nonzero candidate layer forces `s_env = 0`. `s_env·D_B,l` is applied as for NM-total, preserving the candidate's layer directions while bringing every layer within recipe A's per-layer norms. Actual merged layer norms ≤ 1.01 × recipe A's and direction cosine ≥ 0.999 on nonzero control layers, else SIZE-UNTESTED. This is an envelope control, not an exactly total-norm-matched control. An all-zero candidate needs no rescaling and cannot be credited as a positive on unchanged base predictions.

### 2.6 Execution by stage (driver; mechanism follows C10V §2 item 4 and C10U §2)

1. **Fingerprint** `d941a9fb` and `_cov_cpu == 3`, stored in full. The driver refuses the inherited harness knobs (`C10_PROJECTOR` `:40`, `N_EDIT`/`C10_SUBJECT_OFFSET` `:62–63`, `C10_CTX_TEMPLATES` `:182`, `C10_ARMS` `:254`, `C10_KEY_LOCUS` `:477`). The driver also refuses mismatched `MODEL_ID`/`MODEL_REV` (`c10e:25–26`), device and knob overrides before harness import, stores SHA-256s of the pristine band, verifies them at every restore boundary, and rechecks source and input identity at each stage; source drift HALTs, without overwriting prior records (Codex #21).
2. **Context templates frozen.** The stage-1 process lets the engine sample `CONTEXT_TEMPLATES_CACHE` once (`memit_main.py:304–323`), writes it to `results/c10y_directdw/context_templates.json` with its SHA-256; every later process (stages 2 and 3, item 5) sets the module global from that file **before** the first LAW#5 `apply_memit_to_model` (`c10e:423`). A driver assignment, no engine edit (the C10U precedent, `docs/C10U_MINT2_PREREG.md:67`). The templates are sampled unseeded per process (`CORPUS/44:32`, F-A4), so without the freeze the two processes would not share write inputs. **Overlap audit (advisor #12, Codex #12).** Before writing, publish and hash every frozen context template and the instantiated canonical-rewrite/target-prefix/KL inputs. Normalise using case folding, punctuation removal and whitespace collapse while preserving a subject placeholder; report exact and held-out-frame containment matches against PTEST (`c10e:51–61`). A held-out frame inside a write input is INVALID-LEAKAGE and HALTs before candidate optimisation. Generate inputs without using held-out scores; do not redraw a leaking context set until it happens to pass. Store the audit and the fixed rule in H_in. Held-out prompts may be used for prescribed evaluation, never for gradients, checkpoint selection, timing-smoke selection or stopping.
3. **Targets pre-solved once per arm** on the pristine model with the engine's `compute_z` at layer 8 and the frozen templates, stored with their SHA-256s, and placed in `Z_OVERRIDE` under `(subject, " " + value)` (`:97`, consumed `:185–189`). Recipes A, B-z and B-e2e of one process therefore share z and, through the capture solve, B_l and R_l. Audit (Codex closing note): an execution ledger keyed by (stage, recipe, arm, check) declares before each call the overrides it must consume; completed writes and checks must consume exactly their declared overrides, and NOT-RUN arms are recorded as NOT-RUN, never counted as completed (V6). A later process recomputes its targets independently from the same pristine inputs; each process's target hashes are stored as intermediate outputs, not expected to share one content hash (Codex #21).
4. **Wrapper.** `run_recipe` calls `my_edit` by module-global name (`:489`); the driver rebinds `H.my_edit` to a wrapper with a mode ∈ {`None`, `anchor`, `e2e`, `apply_stored`}. Mode `None`, and every call with `H._LAW5_DEFAULT_CTX` True (`:403`, `:430`), delegate unchanged to the original. Modes `anchor`/`e2e`: capture solve → restore the band (`restore_layers`, `:155–159`) → optimise A^l with hooks → remove hooks → merge. Mode `apply_stored`: restore, add the stored NM updates. Each recipe is one `H.run_recipe(name, HP_BASE)` call (the `C10_RECIPES=candidate` semantics, `:582`), so every recipe runs its own LAW#5 gate and its own evaluation code path unchanged. Hook registrations on every band `down_proj` are snapshotted before each write and must equal the snapshot afterwards (§2.8 (viii)). For a recipe that writes A7 only (stage 1), the driver rebinds the module global `H.ARMS` (`c10e:253–255`) to its A7 entry for that `run_recipe` call and restores the full dict afterwards — a driver assignment, not the refused `C10_ARMS` variable.
5. **Order and stages (advisor #3, Codex #3, Codex #15).** Every process runs: fingerprint and read-only input audit (items 1–2) → initialise/freeze contexts and solve pristine targets (item 3) → untouched recipe A and its standing LAW#5 gate → **LAW#3 (V4)** → new-path reduction/inertness/objective/deployment checks (§2.8 (ii)–(viii)) → candidate timing/backward smoke (§2.8 (ix)) → substantive candidate writes. No new-path candidate hook forward, backward, optimiser iteration, closure arm or NM/ENV evaluation occurs before the baseline gate. Static arithmetic and untouched-engine target solves are permitted beforehand.
   - **Stage 1: single-process A7 spending screen; maximum 120 minutes elapsed from process start, including loading, target solves, projector construction, all proofs, timing smoke, optimisation, merge and readout.** First run untouched recipe A on A1/A2/A7 and pass LAW#3. Then prove the new e2e path inert on A7, including the executed-loop identity and deployment checks. Only after those gates run the three-step timing smoke; discard its state and restore the pristine band. Time all expensive stages with MPS synchronisation. Preserve T_max=100 and the frozen optimiser settings. The pre-start gate, the independent supervisor with cap C₁ = 7,200 s and the in-run projections of item 6 govern the whole process, from before worker launch. Run **B-e2e on A7 only**; the screen's reading is the §3 screen table (threshold n ≥ max(19, a+10)). A7-only optimisation is the cheapest direct overturning test of H-Y1 here. Its diagnostic kill closes this screened configuration/spending decision, not DOW-KE, H-Y2, model capacity or C10. The stage-1 process ends after its readout.
   - **Stage 2, conditional:** only a SCREEN-PASS buys B-e2e A1/A2, B-z with its own preceding inertness/fit checks, and the required size controls. Run the same positive configuration without retuning. Because a recorded spending decision falls between the stages, stage 2 is a fresh process that repeats the whole order above from the same `H_in` (its own recipe A and LAW#3 before candidates) and runs B-e2e on A1, A2 and A7, B-z, and NM-total/ENV where triggered; it is process 1 of the full reading. The stage-1 and stage-2 B-e2e A7 counts are both reported. Only a valid, fit, clean positive surviving attribution earns a request to spend on stage 3. **Stage 3:** a fresh-process regeneration from the same declared inputs, including its own baseline gate before candidates, only for that survivor (process 2 of the full reading); it independently regenerates B-e2e, B-z and the required controls (item 7). A second process is not mandatory after a screen kill. Stages 2–3 each require a measured cost forecast, a finite numeric cap and a recorded spending decision before launch (item 6); the draft's total 5–11 hours remains UNVERIFIABLE, not an approved upper bound.
6. **Budget control, every stage (Astra freeze-check BLOCKING 1).** **Pre-start budget gate, every stage.** Before launching the model-bearing process, record a phase-by-phase duration forecast using the best available measured timings on this Mac. Cite each timing artifact, workload, repetition count and scaling assumption. Include loading, context/target preparation, all baseline and inertness runs, repeated projectors/capture solves, parity checks, smoke, the full remaining 100-update budget, permitted overflow retries, merge, readouts and shutdown. Do not assume early convergence. Use conservative upper estimates; an unmeasured component without a defensible bound makes the forecast UNVERIFIED and dispatch is refused.

   Stage 1 has cap C₁ = 7,200 seconds. Stages 2 and 3 each require a finite numeric cap recorded in their spending decision before launch; an absent cap refuses dispatch. If the projected total exceeds the stage cap, record HALTED-BUDGET with `launched=false`; equality passes. The existing 110–165-minute inference is not a measured feasibility certificate.

   An independent supervisor starts the deadline before worker launch and enforces it throughout loading, baseline, proofs, optimisation and evaluation, including blocked calls. It owns only this stage's worker/process group. Its bounded termination allowance is inside the cap, with forced termination at the deadline if necessary. A model-free hanging-worker test must verify enforcement before dispatch.

   Retain in-run projections before every expensive phase and at optimiser-step boundaries. Use synchronised measurements and reserve at least 23 minutes for stage-1 final readout, increased when measured evidence requires it. Exceeding the projected budget stops work without changing T_max, batching or optimiser settings. A budget stop caused by either an in-run projection or the supervisor deadline is HALTED-BUDGET before write completion, and INCOMPLETE-BUDGET after write completion but before required readout completion. Neither earns a scientific label. Obtaining missing calibration timings is separately budgeted work and cannot bypass LAW#3.
7. **Size controls (Astra freeze-check BLOCKING 3).** NM-total and ENV are conditional controls in **both stages 2 and 3**, never stage 1. Derive each arm's scale from that process's corresponding recipe-A and B-e2e actual updates. A triggered control recipe supplies A1/A2/A7 records; an arm requiring no downscale uses scale 1 and may reference its identical, fully evaluated B-e2e artifact with explicit provenance. It is not NOT-RUN.

   Stage 3 independently regenerates B-e2e, B-z and the required controls. For cross-process comparison, a control untriggered in one process uses that process's scale-1 candidate counterpart. No stage-2 tensor substitutes for stage-3 regeneration. Both processes must independently satisfy attribution.

   Stored updates use the explicit arithmetic `W_post = fp16(W0 + fp16(s·D_B))`, with `s·D_B` computed in float32; geometry and matching use the resulting actual D.

### 2.7 Write-only ruling and the reproducibility rule

**The ruling, quoted** (`EXPERIMENT_RUNBOOK.md:330`, D-C10r-rulings-3 (2)): "Write-only ruling, the operator's words: training per commit defeats the spec's objective; likelihood of deploying it is essentially zero; run it only as a measurement — H-13/H-15 are an oracle measurement, not a route; H-18 demoted." The criterion it rests on (`recommended_sequence.md:11`): "The write must stay a per-commit solve that can be regenerated from the committed patch. Anything that needs a training set or a training loop per commit is out as a route (it breaks real-time use, the audit trail and compaction)."

**Classification: MEASUREMENT-ONLY, not a write route.** This experiment trains the effective weight-update factors A by gradient steps on the patch's own prompts. Frozen base parameter objects, a low-rank overlay and dataset-free inputs do not remove that training loop. This differs from the accepted engine's activation-vector optimisation on frozen weights followed by a closed-form weight solve. Under D-C10r-rulings-3 (2) and D-C10u-Aenv (2), any positive result is diagnostic evidence about this objective and parameterisation only. It neither qualifies the deployment route nor relaxes the operator's criterion. Route status would require an explicit superseding scope ruling; wall-clock or regeneration success alone does not supply one. The spec's exclusion of full fine-tuning is cited narrowly, not as a prohibition on the existing compute_z activation solve. (`EXPERIMENT_RUNBOOK.md:330,343`; `memit_dry_run/memit/memit/compute_z.py:83,104–105,170–172`; `experiments/track_c/c10e_bandknob.py:209–217`; spec §8.2, `research_and_specs/llm-as-database-v1_2-integrated-spec.md:313`.)

A replicated positive measurement may motivate a separately authorised method experiment. It does not automatically become a candidate engine variant, close C10, justify a model-axis ceiling claim, or amend the spec.

Compaction requires a full recompile over active patches (spec `:413`, `:837–855`; e2e `:54`), and this writer's per-step cost grows with the number of facts (§2.11); this N = 24 run and its regeneration test do not validate compaction cost or cleanliness (advisor #2, Codex #2). The classification is a program ruling in force (D-C10r-rulings-3 (2); D-C10u-Aenv (2)) and is recorded here, not put to the operator; the wall-clock, reproducibility and regeneration readouts below are measured as readouts, not as qualification evidence.

**Reproducibility rule (the overlay-hash question, `council_critique.md:13, :88, :244`; Codex #21).** An iterative solve on MPS is not bit-reproducible (CLAUDE.md gate 2). Common H_in binds the ordered request lists for **all three arms**, model ID/revision and base-weight artifact identity, tokenizer artifacts/settings, covariance/hparams/context hashes, preregistration and complete objective/optimiser/stage table, harness/driver/reader and every used engine primitive source hash (`compute_z`, `compute_ks`, `repr_tools`, `memit_main`), library/backend versions, resolved MPS device, dtypes, seed, routing and batching settings. Refuse mismatched model/revision/device/knob overrides before harness import. Store pristine-band hashes and verify them at every restore boundary. Recheck source/input identity at each stage; source drift HALTs, without overwriting prior records.

Recompute targets independently from the same pristine inputs in process 2; store each process's target hashes as intermediate outputs, not an expectation that potentially nonidentical regenerated targets share one content hash. Within a process, share each arm's pinned targets and capture inputs across its comparators. Store hashes of the named/dtyped/shaped update tensors (`H_out`), the actual applied band state and the immutable serialized overlay. Preserve the **actual committed overlay hash** required by §11.5 (spec `:671`); H_in and a regeneration certificate are supplementary audit metadata. Do not replace artifact identity with behavioural similarity or conclude that a failed similarity gate means no ledger could record the artifact.

R1–R3 certify fixed-input cross-process regeneration under this experiment. Same seed, frozen contexts and the same 24 facts are not independent-seed robustness or compaction-at-scale evidence. Report that scope explicitly. This experiment proposes no automatic §11.5 hash amendment and grants no route status.

### 2.8 Inertness (LAW#5) and step-0 checks — numeric, same process; any failure → HALT (§5)

The known-ceiling reference for this new solve path is untouched same-process recipe A with its CORPUS/44 A7 envelope (V4), the established A1/A2 controls (A1 ≥ 70/72 in every CORPUS/44 arm, `CORPUS/44:21`), and the capture, zero-step and executed-loop reductions below. A separate K1 rerun is not required; K1 is not an A7 ceiling (`CORPUS/43_C10K_KEYING_ABLATION.md:6, :12–17, :52`; advisor #13 (a), Codex #13 (a)). Standing check (i) precedes LAW#3 for recipe A; all new-path checks follow LAW#3. Checks (ii), (iii), (iii-b), (iv), (v) and (viii) apply to each optimised mode/arm before its substantive result is trusted. Check (vi)'s NLL/KL construction audit is e2e/A7; its accumulation comparison applies separately to each optimised objective on the fixed A7 subset. Check (vii) applies to each optimised mode/arm. Check (ix) is the e2e/A7 smoke once per process.

`apply_stored` instead requires scale-1 reference reproduction, restoration/hook checks, planned stored-update and actual-update geometry, and complete merged-model readouts. Optimiser, gradient and train–deploy-hook checks are explicitly NOT-APPLICABLE to this mode. Final-state checks run after optimisation/merge and before classification, not before the state exists. Reduced LAW#5 writes are not substantive fit-tested candidates.

Check each mode before trusting that mode's substantive output; stage 1 checks e2e/A7, later stages check their additional modes/arms before use (Codex #6).
- **(i) Standing gate.** `run_law5` in every recipe (`:463`, rule `:444`) → INERT; |Δexpr| recorded (CORPUS/50: 0.0001; CORPUS/53: 0.0). Standing run_law5 certifies original engine/harness parity only: the wrapper delegates every `_LAW5_DEFAULT_CTX` call to the original (`c10e:430–433`), so (i) is inert by construction for B modes; new-path LAW#5 is (ii), (iii), (iii-b) and (viii) (advisor #6, Codex #6).
- **(ii) Capture-solve identity.** On identical restored weights, templates, P and pinned targets: run the original `my_edit` twice (floor = largest per-layer `‖ΔW_a − ΔW_b‖_F / ‖ΔW_a‖_F`), then the driver's capture solve; per-layer relative distance to `my_edit`'s write ≤ max(10 × floor, 1e-4) (the C10V (ii) rule, `docs/C10V_LAYERPICK_PREREG.md:58`), on every arm the stage writes (A7 in stage 1; A1, A2, A7 in stages 2–3).
- **(iii) Zero-step identity.** Each B mode with T_max = 0 (A^l = R_l, merged) gives weights within (ii)'s tolerance of recipe A's and identical `canon_full_n`, `para_full_n`, `para_first_n`.
- **(iii-b) Executed-loop identity (advisor #6, Codex #6).** New-path LAW#5 consists of the capture reduction, T=0 identity and **exactly three forced iterations at lr=0**, with early stopping disabled for this check. Run hooks, routing, four-way accumulation, loss scaling/unscaling, Adam.step, cleanup and merge. Both B modes must reproduce the original reference's merged weights within the frozen reduction tolerance and identical canon_full_n/para_full_n/para_first_n. apply_stored must separately reproduce a stored reference at scale 1 before any NM or ENV result is trusted.
- **(iv) Train–deploy parity (Codex #16).** At init and at the final state of every optimised B-z or B-e2e write, the optimisation forward (§2.3) and the merged fp16 model generate identical target-length token-id sequences, hence identical full-sequence hit vectors, on all 24 canonical plus 72 held-out prompts of the arm. Require teacher-forced loss difference ≤ max(1e−4, 1e−3·|L_merged|), for the total and each component separately. Record loss components and logit differences. A miss is INVALID-TRAIN-DEPLOY-GAP, before any positive interpretation. Held-out parity evaluation never selects a checkpoint. The merged model remains the scored artifact. The proposed functional path and tolerances themselves need this LAW#5 validation; no claim that they have already passed is made.
- **(v) Projector property, planned and actual (Codex #20).** Report two objects: planned float32 `A^l B_l` and actual `D_l = W_post.float() − W_pristine.float()`. All write-size, NM/ENV matching and regeneration gates use D. Null-space share `‖ΔW^l P_l‖²_F / ‖ΔW^l‖²_F` and covariance-weighted energy are reported for both; the share must be ≥ 0.999 per layer for the planned and the actual nonzero update, at init and at the final state of every B write; zero updates are recorded as zero. If the untouched reference (recipe A's own actual D) cannot meet this tolerance, HALT for a precision diagnosis before candidate interpretation; do not weaken it after a candidate result. Rank ≤ 24 and zero response on ker(P) are exact-arithmetic properties of AB, not asserted exact properties of D.
- **(vi) Objective construction.** On the pristine model, the driver's per-request `L_edit` equals `compute_z`'s iteration-0 NLL for the same request (its printed value at delta = 0, `compute_z.py:159–163`, rounded to 3 decimals) within 2e-3, 24/24 for A7; the driver's tokenised batch, target positions and lookup indices are a line-for-line construction of `compute_z.py:41–73`. **KL (Codex #17):** the driver's `KL_raw` and weighted KL are validated against `compute_z`'s KL expression (`compute_z.py:151–153`) at delta = 0 and at one fixed nonzero intervention — request 0's solved `delta` (§2.6 item 3) added at every KL row's lookup index as `compute_z.py:90–99` adds it — each within 2e-3; matching a zero KL at init alone is insufficient. **Accumulation parity (Codex #9):** a fixed 12-request A7 subset — requests 0–11 of the A7 request list, published now — with identical padded token tensors, and a one-batch reference only after its measured headroom passes the §2.10 guard. Compare that reference with splits 6+6 and 5+7, weighted by request count. Require finite nonzero layer gradients, cosine ≥ 0.999 **and relative L2 error ≤ 0.01** for every layer. Test the 24-request weighting/index logic separately without allocating a 24-request autograd graph. The scope is accumulation parity on the subset, not empirical full-24 parity. Failure to fit the reference within the guard is HALTED-RESOURCE, not a licence to loosen the gate after seeing results.
- **(vii) Gradient finiteness and magnitude.** At init, the unscaled gradient is finite and nonzero on every layer at scale 2¹⁰ or after at most three halvings; per-layer gradient norms are recorded and checked in magnitude, not only direction, under (vi) (Codex #17).
- **(viii) Restoration and hooks (advisor #6, Codex #6).** Snapshot hook registrations before the writer; afterwards require exactly the original registrations and no writer-owned hook handles. If the initial registries are empty, final forward/pre-hook registries must be empty. Confirm the pristine band, optimiser/global wrapper state and override counters are restored between checks/arms. A failed restoration or reduction is HALTED/INVALID, not TRADEOFF. Do not erase unknown pre-existing hooks to make the assertion pass.
- **(ix) Candidate smoke, after LAW#3 and (ii)–(viii) (Codex #17).** Three B-e2e steps on A7 at the frozen nonzero lr: A changes on every layer, gradients finite on every layer, fixed-input loss recorded before and after, base-weight invariance (band hashes) and restoration verified; the state is then discarded. The steps are timed with MPS synchronisation for the in-run projections of §2.6 item 6. Mere finite gradients or a successful lr = 0 loop do not prove the real update works.

### 2.9 Readouts (every recipe, every arm unless noted)

- **Binding and decomposition** (`eval_arm`, `:358–400`): `para_full_n` /72, per held-out template (3 × 24), per-fact 24-vector with the per-edge rule (pass iff 3/3), `canon_full_n` /24, `para_first_n` /72, `para_string_n`, `tf_pertok_cont`, `cond_full_given_first` (the last two typed-nullable under V13).
- **Raw gate inputs (Astra freeze-check BLOCKING 6).** The driver records unrounded `described_as` and generic perplexity using the harness's same distributions, prompts and reductions, before final presentation rounding. G3/G5 use these raw fields exclusively. Preserve legacy rounded fields for display. A rounded value cannot substitute for a missing raw gate input.
- **Locality**: L1 flips /12, L3 top-1 agreement /30 and mean KL, generic perplexity pre/post (`:319–339`); `described_as` (`:492`); same-frame `frame_probe` flips /6 (`c10p:36–42`) in CANON and, separately, with the six never-edited `FRAME_SUBJECTS` in each of the six frozen rewriting frames (§3 G2; Codex #19); relation-label probes on the 24 edited subjects, top-1 pre/post, flips counted: `"{s} is associated with"` (bystander) and `"{s} is a"` (**objective-anchored** — it is B-e2e's own KL prompt, so it is not a clean bystander).
- **Write geometry, per layer, for the planned float32 `A^l B_l` and the actual applied `D_l` (§2.8 (v); Codex #20)**: ‖·‖_F, ratio to recipe A per layer and summed, null-space share, covariance-weighted norm `tr(ΔW C ΔWᵀ)` (`council_critique.md:66, :167`), cosine to recipe A's update.
- **Premise readouts** (A7 and A1, recipes A, B-z, B-e2e): the remaining ratio at block 8, canonical and on the three held-out prompts, by the formulas of `c10l_covgeom_step0.py:134–137` with each arm's own z, measured in the merged post-edit model (comparable in scope to `CORPUS/53:62`). Prediction recorded now: if B-e2e gains, its canonical remaining ratio to `z_pre` may *rise* (it re-aims toward a rotated target, CORPUS/47–48) — a high ratio with a high count would say the anchor is not the goal. Reported, not gated.
- **Optimisation trace per write**: loss components per step, steps taken, stop reason (threshold / cap), loss-scale halvings, final hooked-versus-merged loss difference, wall-clock per write, the §2.10 memory telemetry per heavy phase; per-layer ‖A^l B_l‖_F every step; accepted steps and overflow retries counted separately; the merged-model fit matrix `f_ij` (24 × 6) and, for B-z, `r_ij` (§3 Fit; advisor #4, Codex #4). Complete per-patch compile time, including target solves, capture, optimisation, merge and mandatory production probes, reported separately from one-time setup and experimental controls (Codex #10).
- **Reproducibility** (process 1 vs 2): per-layer cosine and relative distance of the actual applied D for A and B arms; per-fact cosine of z; per-prompt agreement on the 72 held-out A7 prompts.

### 2.10 Memory arithmetic (48 GB unified memory; CPU caches count against the same pool)

| item | arithmetic | size |
|---|---|---|
| model weights, fp16 | 3,085,938,688 params (embedding 151,936 × 2048 = 311.2 M; per layer 77.08 M = attention 9.44 M + MLP 3 × 2048 × 11008 = 67.63 M + norms; × 36) × 2 B | 6.17 GB (5.75 GiB) |
| covariance cache, CPU float32 (`memit_main.py:280`) | 5 × 11008² × 4 B | 2.42 GB (2.26 GiB) |
| projectors P (`c10e:175`) | 5 × 11008² × 4 B | 2.42 GB |
| band snapshot (`c10e:150–152`) | 5 × 2048 × 11008 × 2 B | 0.23 GB |
| live arm cache (`c10e:474`; Codex #9) | 5 × 11008² × 4 B | 2.42 GB (2.26 GiB) |
| deployed-arithmetic weights (§2.3; Codex #16) | float32 `AB`, fp16 `fp16(AB)`, fp16 `W_eff`, and their gradients: 5 × 2048 × 11008 × (4 + 2 + 2) B × 2 | ≈ 1.8 GB (≈ 1.7 GiB) |
| A, B, Adam state | 245,760 × 4 B × 3 + 5 × 24 × 11008 × 4 B | < 0.01 GB |
| saved activations per token per layer (fp16) | RMSNorm in/out 2 × 2048; q and GQA-expanded k, v saved by attention 3 × 2048; attention output 2048; post-attention norm in/out 2 × 2048; attention weights 16 × T (T ≈ 28) ≈ 450; MLP gate, SiLU out, up, product 4 × 11008 → ≈ 62,900 values × 2 B | ≈ 126 KB (≈ 160 KB with temporaries) |
| layers holding activations | layers 4–35 (no tensor requires grad before the first hooked `down_proj`) | 32 |
| tokens per request | 6 rewriting prompts (one identity + five sampled templates, `memit_main.py:308–319`) + 1 KL prompt, padded to T ≈ 28 (prefix ≤ 10 + ". " + CANON with subject ≈ 10–12 + value[:-1] ≤ 5) | ≈ 196 |
| activations, full batch of 24 | 4,704 tokens × 32 × 126–160 KB | 19–24 GB |
| activations, micro-batch of 6 (adopted) | 1,176 tokens × 32 × 126–160 KB | 4.7–6.0 GB |
| head at target positions only | (144 × ≤ 6 + 24) ≈ 888 positions × 151,936 × 4 B, plus fp16 logits and gradients | ≈ 1.3 GB full batch, ≈ 0.33 GB per micro-batch |
| **peak, micro-batch 6** | 5.75 + 2.26 + 2.26 + 2.26 + 0.21 + 1.7 + 4.4–5.6 + 0.3 GiB, before solve/SVD temporaries and retained updates | **≈ 19–20.5 GiB (UNVERIFIED)** |
| peak, full batch (not adopted) | same with 18–22 GiB activations | ≈ 33–37 GiB |

Full-logit computation over all positions, as `compute_z` does (`compute_z.py:122`, `:140`), would add 4,704 × 151,936 × (2 + 4) B ≈ 4.3 GB per full batch and is not used. B-z needs activations only for blocks 4–8 (≈ 5/32 of the above). **Memory feasibility is UNVERIFIED (Codex #9).** Charge model, covariance, projectors, live arm caches, snapshots, solve/SVD temporaries, stored updates, head tensors, activations and optimiser state to the one unified pool. Record synchronised current/driver MPS allocation, process RSS and host available memory separately; do not sum overlapping metrics and call the sum measured physical usage. Before and during every heavy phase, HALT if driver allocation > 32 GiB, RSS > 40 GiB, or host available memory < 8 GiB. Equality is allowed. In addition (advisor #9, kept as the more conservative guard): HALT if driver allocation + RSS > 40 GiB — a possibly double-counting guard, not a measurement of physical usage. Missing required telemetry is a preflight failure, not a silent assumption. Record peak values through projector construction, capture solves, parity checks, backward, merge and evaluation; a single init sample is not a peak. fp16 model and float32 A/B stay on MPS; every float64 diagnostic/solve must first move its tensors to CPU. No CUDA operation or new covariance job is part of this screen. A guard trip is a HALT, not a silent micro-batch change. T ≈ 28 is an assumption; step 0 records the real padded length.

### 2.11 Compute estimate (unmeasured on this path; the post-LAW#3 smoke, §2.8 (ix), measures before any substantive candidate write)

- **Per B-e2e optimiser step:** forward 2 × 2.775 B non-embedding params ≈ 5.55 GFLOP per token; activation-gradient backward through layers 4–35 ≈ 4.9 GFLOP per token; head at ≈ 888 positions ≈ 0.55 TFLOP forward and as much backward. Total ≈ 4,704 × 10.5 GFLOP + 1.1 TFLOP ≈ **50 TFLOP per step**. At an effective 1–3 TFLOP/s on MPS (not measured for this path): **17–50 s per step**, so ≤ 100 steps = **28–83 min per write**; the threshold stop can end a write earlier.
- **Stage 1 (advisor #3, Codex #3; I-INFER, not a measured duration):** ≈ 34 min untouched baseline (one historical three-arm pass: three passes in ≈ 99 min, `CORPUS/50_C10Q_STACKED_SOLVE.md:3, :6`, `hypotheses.md:8`; C10P ≈ 23.2 min per pass, `results/c10p_twopass/logs_c10p_chain.log:1–6`) + ≈ 25 min proofs and setup + 28–83 min for one 100-step A7 write + a 23-min readout reservation ≈ **110–165 min**; capture identities and repeated SVDs can add further cost (`c10e:166–175, :209–211, :458–474`). This range is not a measured feasibility certificate: the pre-start budget gate (§2.6 item 6) refuses launch (HALTED-BUDGET, `launched=false`, not NULL) when the forecast from measured timings exceeds the 120-minute cap. Stages 2–3 each require a measured cost forecast, a finite numeric cap and a recorded spending decision; the v1 total of 5–11 h is UNVERIFIABLE, not an approved upper bound.
- **Budget rule:** §2.6 item 6 governs (pre-start gate, independent supervisor, in-run projections). The smoke (§2.8 (ix)) supplies in-run timings only and is not the budget gate. T_max, micro-batching and the optimiser settings are never changed to fit the budget.

### 2.12 Records

`results/c10y_directdw/`: `context_templates.json` (+ SHA-256), `manifest.json` (`H_in` and its parts), `targets_p{1,2}.pt` (+ SHA-256s), `overlap_audit.json` (§2.6 item 2), `ledger.json` (execution ledger, V6), `screen.json` (stage-1 screen record and label; files suffixed `p1`/`p2` belong to the stage-2 and stage-3 processes), `step0_p{1,2}.json` (checks (iv)–(ix), memory telemetry, timing), `law5_p{1,2}.json` (checks (i)–(iii-b) and V4), `pass_p{1,2}.json` (every recipe and arm, readouts of §2.9, optimisation traces, `H_out` per write), `repro.json` (R1–R3), `run.json`; logs under `results/c10y_directdw/logs/`. Driver `experiments/track_c/c10y_directdw_arms.py`; reader `experiments/track_c/c10y_directdw_read.py`, which encodes every gate and label in §3 (the reader, not prose, issues labels — the CORPUS/50 prose/code divergence, `CORPUS/50:19`, is the reason). HALT diagnostics `architecture_profile/sNNN_halt_diagnostic.json`.

## 3. Pre-registered readings (exact counts; decision order fixed)

**Decision order (Codex #5).** Recorded halt/invalid/budget outcomes → completeness of the recipe's own records and V5 controls → instrument/validity gates → fit → per-process count and locality label → write/deployment qualifiers → cross-process comparison → attribution. Missing recipe records or V5 controls give INCOMPLETE; missing size or anchor comparators qualify the candidate through attribution, as specified below. Failed validity gives INVALID (named halt gates stop dispatch); fit failure gives UNDERFIT. Neither is a negative mechanism result. A stage-1 record is a SCREEN result under §2.6, not a complete scientific verdict. Every table below is read top to bottom and the first matching row applies, so each table is exhaustive and its rows mutually exclusive. Compare unrounded finite metrics, not formatted strings; every stated limit passes at equality (≤, ≥, closed intervals) unless a row says otherwise. The reader, not prose, issues every label (`CORPUS/50:19`).

**Validity — any failure → INVALID for that recipe (V1, V4, V12 and the named §5 gates → HALT):**
- **V1** fingerprint `d941a9fb` and `_cov_cpu == 3`, full output stored.
- **V2** `run_law5` INERT in every recipe (`c10e:444`) — evidence of original engine/harness parity only (§2.8 (i)).
- **V3** the §2.8 checks pass as scoped by §2.8's applicability statement (ordering, per-mode and per-arm scope, `apply_stored` substitutions), each before the result it covers.
- **V4 (LAW#3; Codex #15)** LAW#3 requires all three A7 integer counts of recipe A simultaneously: `para_full_n` ∈ [5, 18], `canon_full_n` ∈ [5, 10], `para_first_n` ∈ [42, 59], with denominators 72/24/72 respectively and baseline A1/A2 ≥ 68/72. Every endpoint is inclusive (`CORPUS/44_C10L_COVGEOM_SPARSEBAND.md:39`; shared controls `results/research_pass_2026-10-06/prereg_stubs.md:10`). It is checked before any new-path candidate operation (§2.6 item 5). Any miss HALTs the entire planned schedule, including future processes, before candidates. Do not use this reproduction interval as a candidate positive threshold or widen it after observing the baseline.
- **V5** A1 ≥ 68/72 and A2 ≥ 68/72 under the candidate recipe (a control failure is INVALID, never TRADEOFF). In stage 1 the candidate's A1/A2 are NOT-RUN and the screen is non-binding.
- **V6** the execution ledger (§2.6 item 3): every completed write or check consumed exactly its declared overrides; NOT-RUN arms are recorded as NOT-RUN; the §2.8 check calls are recorded separately.
- **V7** null-space share ≥ 0.999 on every nonzero layer of the planned and the actual update of every B write (§2.8 (v)).
- **V8** `para_string_n ≥ para_full_n` for every arm.
- **V9** Train–deploy parity (§2.8 (iv)) is required at init and at the final state of every optimised B-z or B-e2e write; a miss is INVALID-TRAIN-DEPLOY-GAP. For `apply_stored`, V9 is NOT-APPLICABLE; the stored-update checks specified in §2.8 remain mandatory.
- **V10** ≤ 5 overflow retries per write (§2.4).
- **V11** `H_in`, every SHA-256 of §2.7 and §2.12, the stop reason, the accepted-step count and the retry count per write in the record.
- **V12** overlap audit clean (§2.6 item 2); a miss is INVALID-LEAKAGE and HALTs before candidate optimisation.
- **V13 — typed metric validity.** Required fields must be present. Applicable numeric values must be finite. `tf_pertok_cont=null` is valid exactly when the recorded continuation-token denominator is zero; `cond_full_given_first=null` is valid exactly when `para_first_n=0`. Preserve their denominators and an explicit undefined reason. These diagnostic nulls neither invalidate an arm nor count as passed scientific gates. An unjustified null, NaN or infinity fails V13. Explicit zero-update/not-applicable cases follow their named rules.

**Fit (Codex #4; read before any count is interpreted).** Compute final **merged-model** f_ij=exp(−mean target-token NLL) for each of 24 requests i and all six rewriting frames j, and record the entire 24×6 matrix. This is a geometric mean of teacher-forced token probabilities, not sequence probability. **FIT-E2E** means min_ij f_ij ≥0.90 and canon_full_n ≥20/24. Equality passes. Test it at every termination, including threshold stops. Otherwise base fit status is UNDERFIT, regardless of held-out count; report the held-out count and any sized gain alongside it, but do not issue a clean LEAD/PARTIAL or a conclusive NULL. State the stop reason separately; no budget increase occurs within this preregistration. FIT-E2E applies in the same way to the merged NM-total and ENV controls. Record fit separately for every substantive arm. A recipe passes FIT-E2E or FIT-Z only when all its required arms pass; stage 1 requires A7 only. Recipe A and reduced inertness checks are exempt from candidate fit gates.

**FIT-Z** means merged L_z ≤1e−3 and max_ij r_ij ≤0.05, where r_ij=||h_ij−(h0_ij+delta_i)||/||delta_i||. Equality passes. The optimiser's stricter mean stopping threshold 1e−4 remains unchanged, but cannot excuse a failed maximum-entry fit check. The zero-denominator rule of §2.3 applies. An unfit B-z is not usable to exclude anchor closure. These are newly proposed diagnostic fit thresholds, not inherited empirical calibration; they are frozen here, and counts are retained on UNDERFIT.

**Record completeness (Astra freeze-check BLOCKING 2).** Read recorded halt/invalid/budget outcomes first; missing records caused by a halt do not manufacture another validity failure. Otherwise, missing records of the recipe being classified, including its required V5 controls, give INCOMPLETE before fit or counts are tested. Missing size or anchor comparators instead give the candidate SIZE-UNTESTED or ANCHOR-UNTESTED under attribution; they do not replace its base label with INCOMPLETE. Stage-1 candidate A1/A2 and later-stage records are deliberately NOT-RUN and are not required screen records. Only complete, valid screen records reach S4–S7.

**Stage-1 screen (Codex #3; one process, B-e2e on A7 only).** a = recipe A's A7 `para_full_n`; n = B-e2e's merged A7 `para_full_n`; ratio = W1's summed actual-write ratio.

| row | condition (first match) | reading |
|---|---|---|
| S1 | a named HALT of §5 other than HALTED-BUDGET, or any applicable validity failure (V1–V4, V6–V13) | HALTED / INVALID — no screen label |
| S2 | the pre-start gate of §2.6 item 6 refuses launch (`launched=false`), or an in-run projection or the supervisor deadline stops work before write completion | HALTED-BUDGET |
| S3 | the write completes but an in-run budget projection or the supervisor deadline stops work before the required readout completes | INCOMPLETE-BUDGET |
| S4 | FIT-E2E fails | SCREEN-UNDERFIT (n, a and the fit matrix reported) |
| S5 | n < max(19, a + 10) | SCREEN-NULL |
| S6 | n ≥ max(19, a + 10) and (any of G1, G2 in CANON or in any of the six frames, G3, G4, G5 fails, or ratio > 1.5) | SCREEN-NOT-ADVANCED, with the observed reason |
| S7 | otherwise | SCREEN-PASS — provisional and non-binding; buys a stage-2 spending decision |

Missing candidate A1/A2 or replication remains explicitly NOT-RUN. H-Y2 is NOT-TESTED if B-z is not run; never conclude H-Y0, 'neither objective works', from this screen.

**Per-process labels (stages 2–3; Codex #5).** For a recipe in one process (B-e2e is the candidate; B-z, NM-total and ENV are read by the same rows, B-z with FIT-Z in place of FIT-E2E), a = the same-process recipe A A7 baseline, n = the recipe's merged A7 held-out count, and sized := n > 18 AND n − a ≥ 10 (equivalently n ≥ max(19, a + 10)).

| row | condition (first match) | base label |
|---|---|---|
| P1 | a required record of the recipe, or its V5 controls, missing | INCOMPLETE |
| P2 | any validity failure (V1–V13) | INVALID |
| P3 | fit fails (FIT-E2E; FIT-Z for B-z) | UNDERFIT (count reported) |
| P4 | sized, n ≥ 30, G1–G5 pass | LEAD |
| P5 | sized, n < 30, G1–G5 pass | PARTIAL |
| P6 | sized, any of G1–G5 fails | TRADEOFF |
| P7 | otherwise (not sized) | NULL |

Missing size or anchor controls are read through attribution (SIZE-UNTESTED, ANCHOR-UNTESTED), not P1. G6 is reported, not silently treated as a passed locality gate. **Qualifiers never change the base label:** ratio > 1.5 (W1) adds LARGE-WRITE to every applicable label; W2 adds EXCEEDS-TTL; reproduction failure adds NOT-REPRODUCIBLE; attribution adds SIZE-NOT-EXCLUDED, SIZE-UNTESTED, ANCHOR-NOT-EXCLUDED or ANCHOR-UNTESTED; one completed process adds SINGLE-PROCESS. Positive-looking labels with blocking qualifiers do not advance; every qualifier except EXCEEDS-TTL (a reported warning, Codex #10) is blocking.

**Cross-process (stage 3; Codex #5).**

| row | condition (first match) | step label |
|---|---|---|
| X1 | process 2 not run, halted or incomplete | the process-1 label + SINGLE-PROCESS, non-binding; process 2 is recorded as NOT-RUN / HALTED / INCOMPLETE, never a fabricated NULL |
| X2 | both processes completed with identical base labels | that base label |
| X3 | both processes completed with different base labels | MIXED-NOT-REPLICATED, both per-process labels and counts stored |

Every row takes the union of blocking qualifiers; any R1–R3 failure adds NOT-REPRODUCIBLE. A positive is replicated only if its base label and all required validity, fit, locality, size and attribution conditions hold in both processes.

**Reproducibility (process 1 vs process 2, same `H_in`; per B recipe):**
- **R1 (Codex #11a)** For nonzero updates, per-layer cross-process cosine ≥ 0.99 **and `distance = ||D_p1−D_p2||_F / max(||D_p1||_F, ||D_p2||_F) ≤ 0.10`**, on actual applied updates, for every completed arm/recipe required for the positive. Record baseline distances too. Baseline cosine < 0.99 or relative distance > 0.10 is a failed baseline regeneration instrument, not permission to lower the candidate threshold; the reproducibility reading is then INVALID and the step label carries NOT-REPRODUCIBLE. Zero norms are represented explicitly: two exactly zero updates are identical; one zero and one nonzero fails. These gates certify this fixed-input regeneration only.
- **R2** |`para_full_n`(p1) − `para_full_n`(p2)| ≤ 5 on A7 (the per-process spread ±3–5/72, `CORPUS/44:41`).
- **R3** disagreeing held-out A7 prompts (of 72) ≤ d_A + 3, d_A = recipe A's count of disagreeing prompts across the two processes. R3 counts unequal `para_full_hits` booleans for identical `(subject, PTEST_index)` pairs; it does not count differences between two incorrect generated strings.
- A failure of R1, R2 or R3 adds **NOT-REPRODUCIBLE**: the label is reported and cannot advance (it does not satisfy gate A).

**Locality gates (vs recipe A, same process; `prereg_stubs.md:10`):** **G1** L1 flips ≤ A + 1 (of 12); **G2 (Codex #19)** for CANON and for each of the six frozen rewriting frames, independently probe the six never-edited FRAME_SUBJECTS for edited-value first-token flips, before/after recipe A and the candidate; require candidate flips ≤ A + 1 (of 6) separately in every frame; do not pool away a failing frame; **G3** raw `described_as` ≥ A − 3; **G4** L3 agreement ≥ 29/30; **G5** raw generic perplexity ≤ A + 0.5; **G6** relation-label flips reported, no threshold: the '{s} is a' distribution is an objective-anchored preservation readout, not an independent bystander; associated_with remains a reported non-objective probe. A clean label means clean on these named gated axes only; it does not mean all neighbouring facts or relation labels were preserved.

**Write size:** **W1** `Σ_l ‖D^l_B‖_F / Σ_l ‖D^l_A‖_F` on actual applied updates (§2.8 (v)) > 1.5 adds **LARGE-WRITE** (as `CORPUS/53:29`); LARGE-WRITE blocks advancement and gate A. Per-layer ratios and the covariance-weighted norm ratio are reported beside it. **W2 (Codex #10)** Report complete per-patch compile time, including target solves, capture, optimisation, merge and mandatory production probes; report one-time setup and experimental controls separately. Compile duration ≥ 3600 seconds adds EXCEEDS-TTL as a necessary lock-fit warning, including equality at expiry. A duration below 3600 is not sufficient for lock compliance: the lock begins at task declaration, so remaining TTL at actual commit must be positive. The two-hour PREPARED default is an incremental compatibility comparison, not this Genesis-shaped batch's configured timeout. Neither a timing pass nor a timeout qualifier changes MEASUREMENT-ONLY status. N=24 timings are not a measured compaction scaling result.

**Attribution (H-Y1 is credited only here; Codex #18 and #11c).**
- **Control-positive.** Define control-positive in each process using the **same** complete validity, FIT-E2E, n ≥ max(19, a+10), G1–G5 and actual-size requirements as the candidate (NM-total: summed norm within 1 % of N_A; ENV: per-layer norms ≤ 1.01 × recipe A's; direction cosine ≥ 0.999). A norm control inside [5, 18], or with any failed locality/fit condition, does not exclude size even if its baseline-relative gain is 10.
- **T2 (size).** Required controls: NM-total iff N_B > N_A; ENV iff s_env < 1 (§2.5). Record every per-layer actual-write ratio; if any layer grows while the total does not, size redistribution remains a confound, which ENV addresses. A failed instrument/control requirement (or a required control not run) gives **SIZE-UNTESTED**; otherwise a valid tested control without a clean positive gives **SIZE-NOT-EXCLUDED**. Neither qualifier proves that size caused the gain. n_eff := the minimum count over the required controls, or n when none is required (every per-layer actual ratio ≤ 1.0).
- **T1 (anchor).** For an otherwise eligible e2e positive: missing, invalid or unfit B-z gives ANCHOR-UNTESTED. Otherwise, `n_eff−n_z<10` gives ANCHOR-NOT-EXCLUDED, regardless of whether B-z itself has a sized gain. A difference ≥10 passes this comparison. Neither outcome establishes a unique causal mechanism. Boundary cases: `(a,n_eff,n_z)=(12,22,13)` → ANCHOR-NOT-EXCLUDED and `(12,23,13)` → comparison passes.
- **H-Y1 credit.** To credit H-Y1, both processes must show a valid fit clean positive after the required size control(s), and that resulting e2e control must beat the valid fit B-z by ≥ 10 (n_eff − n_z ≥ 10). A positive raw B-e2e difference that disappears after size matching is insufficient. Credit is scoped to this objective/parameterisation; it does not establish that closed-form allocation is the unique limit.
- **B-z's own reading.** B-z is an anchor-objective comparator and H-Y2 test, read by the per-process rows with FIT-Z. Its ANCHOR-SHAM-INERT descriptor means |n_z−a| ≤ 5 and total actual-write ratio in [0.8, 1.25], a window newly set here; CORPUS/50's second-write rule does not transfer. The descriptor is not a validity or fit gate and does not replace B-z's scientific status. The actual inertness controls are the reduced/no-change paths in §2.8.

**Truth table, recorded before any run (Codex #5's cases, extended).** a = 12 and B-z = 13 throughout; complete controls, fit, every gate and R1–R3 pass, and every per-layer actual ratio ≤ 1.0, unless stated.

| stage | observation | reading |
|---|---|---|
| 1 | a = 19 (or recipe A canon 11, first 41, or A1 67) | LAW#3 HALT; no candidate operation; schedule halted |
| 1 | pre-start forecast from measured timings projects 130 min | HALTED-BUDGET, `launched=false` (authored row) |
| 1 | supervisor deadline reached after the write completes, readout incomplete | INCOMPLETE-BUDGET (authored row) |
| 1 | write complete; the pre-readout projection exceeds the cap before the supervisor deadline | INCOMPLETE-BUDGET |
| 1 | n = 25, min f_ij = 0.85 | SCREEN-UNDERFIT |
| 1 | n = 21 (threshold max(19, 22) = 22) | SCREEN-NULL |
| 1 | n = 22, clean, ratio 1.2 | SCREEN-PASS |
| 1 | n = 31, clean, ratio 1.8 | SCREEN-NOT-ADVANCED (size); the per-process rows would read LEAD-LARGE-WRITE |
| 1 | n = 25, `described_as` −4.0 | SCREEN-NOT-ADVANCED (G3); per-process TRADEOFF |
| 1 | n = 27, frame-3 flips A + 2, other frames clean | SCREEN-NOT-ADVANCED (G2, frame 3) |
| 1 | a = 18, n = 27 / n = 28, clean | SCREEN-NULL / SCREEN-PASS (gain 9 / 10) |
| 1 | a = 5, n = 19, clean | SCREEN-PASS (19 = max(19, 15)) |
| 2–3 | n = 33/33, clean, ratio 1.2, valid clean NM = 26/26 and ENV = 24/24 | LEAD; size excluded (both ≥ 22); H-Y1 credited (n_eff 24 − 13 = 11 ≥ 10) |
| 2–3 | as above but ENV = 20/20 | LEAD-SIZE-NOT-EXCLUDED (20 < 22); no H-Y1 credit |
| 2–3 | n = 24/25, clean, ratio 1.3, NM = 17/17 | PARTIAL-SIZE-NOT-EXCLUDED |
| 2–3 | B-z = 24/24 with FIT-Z, n = 27/27, clean | PARTIAL-ANCHOR-NOT-EXCLUDED (27 − 24 = 3 < 10) |
| 2–3 | B-z unfit, n = 27/27, clean | PARTIAL-ANCHOR-UNTESTED; no H-Y1 credit |
| 2–3 | n = 22/22, clean, B-z = 13/13 with FIT-Z (no sized gain) | PARTIAL-ANCHOR-NOT-EXCLUDED (22 − 13 = 9 < 10); no H-Y1 credit (authored row) |
| 2–3 | n = 23/23, clean, B-z = 13/13 with FIT-Z | PARTIAL; anchor comparison passes (23 − 13 = 10) (authored row) |
| 2–3 | n = 18/18 | NULL regardless of baseline-relative gain |
| 2–3 | n = 30/22 | MIXED-NOT-REPLICATED-NOT-REPRODUCIBLE; per-process LEAD/PARTIAL; difference 8 > 5 |
| 2–3 | a = 5, n = 19/19, clean, ratio 1.2, NM = 18/18 | PARTIAL-SIZE-NOT-EXCLUDED (NM 18 < 19) |
| 2–3 | p1 = LEAD, p2 = TRADEOFF or UNDERFIT | MIXED-NOT-REPLICATED, with the actual two statuses |
| 2–3 | p1 = PARTIAL, process 2 halted | PARTIAL-SINGLE-PROCESS, non-binding; process 2 HALTED |
| 2–3 | candidate A1 = 67, or any required metric non-finite | INVALID; no positive or negative mechanism label |

Freeze reader cases for both sides of every boundary: n=18/19/29/30; gain=9/10; A1/A2=67/68; write ratio=1.0 and 1.5 (equality passes those limits); G1/G2 at A+1/A+2; G3 at A−3/A−3.01; G4=28/29; G5 at A+0.5/A+0.51; R2 difference=5/6; R3 disagreement=d_A+3/+4; min f_ij 0.90 and canon 20/24 (equality passes); L_z 1e−3 and max r_ij 0.05; each LAW#3 endpoint and one count outside it; a stage-1 projection of exactly 120 min (fits).

**What each buys (advisor #2, Codex #2).** SCREEN-PASS → a measured cost forecast for stages 2–3 and a recorded spending decision; nothing else. A replicated, attributed, reproducible LEAD or PARTIAL with no blocking qualifier → a replicated attributed positive shows that this fixed weight-space optimisation configuration outperformed recipe A under the named gates. It does not identify closed-form allocation as the unique cause. It may motivate a separately authorised method experiment. It does not automatically become a candidate engine variant, close C10, justify a model-axis ceiling claim, or amend the spec; route status would require an explicit superseding scope ruling. PARTIAL → also a second configuration as its own pre-registration (output-side projector, or OverTone-style token weights from step 6, which act on the same objective). TRADEOFF, LARGE-WRITE or SIZE-NOT-EXCLUDED → report the observed gain and failed condition. It does not establish that increased size caused the gain; any norm-constrained follow-up requires separate preregistration and authorisation. SCREEN-NULL or NULL → this configuration not advanced; the sequence moves on (step 8, or the model axis by the operator's ruling) — not "the layers cannot hold the value". SCREEN-UNDERFIT or UNDERFIT → inconclusive under this optimiser budget, never NULL. HALTED, INVALID, HALTED-BUDGET or INCOMPLETE-BUDGET → no scientific label; any further spend is a new recorded decision.

## 4. Not claimed, whatever the outcome

No label in CORPUS/44–53 changes. LEAD is a measurement (§2.7), not a write-path candidate, not §8.9 contract closure, not route closure, not an F1 change, and not a replication of DOW-KE (different model, metric, batch shape and projector; departures in §7). NULL does not close direct optimisation, end-to-end objectives in general, or the realisation question. Nothing is claimed about which positions or components carry the value. The key, the target solver, the context templates and the projector stay as the engine and harness have them; the engine is untouched. **Spec-amendment flag:** write site none (`hypotheses.md:47`: still an overlay on `down_proj`, D20 projection kept exactly); otherwise none proposed: the step is MEASUREMENT-ONLY (§2.7), so no §8.2 change and no route status are proposed, and this experiment proposes no automatic §11.5 hash amendment — the actual committed overlay hash (spec `:671`) is preserved and H_in plus the regeneration certificate are supplementary audit metadata (Codex #21); a compile of ≥ 3600 s does not fit the Write Lock TTL (spec `:783`; W2).

## 5. Halt discipline and close-out

One speculative fix after a `cat -n` read, then HALT with a diagnostic JSON under `architecture_profile/` and a `SESSION_CHECKPOINT.md` entry. Pre-named halts: V1 fingerprint; V4 LAW#3 miss (halts the entire planned schedule, including future processes, before any candidate operation; the runs made are kept as data, not promoted); any of checks (i)–(ix); V7 projector property (a bug, not a result; recipe A's own actual-update miss is a precision-diagnosis HALT); more than 5 overflow retries in a write; INVALID-LEAKAGE (V12); INVALID-TRAIN-DEPLOY-GAP (V9); INVALID-ANCHOR-NORMALISATION (§2.3); a failed restoration or hook registry (§2.8 (viii)); HALTED-RESOURCE (§2.8 (vi)); the §2.10 memory guards (driver > 32 GiB, RSS > 40 GiB, host available < 8 GiB, driver + RSS > 40 GiB, missing telemetry); HALTED-BUDGET (§2.6 item 6); source or input drift at a stage boundary (§2.6 item 1); any float64 tensor on MPS. Close-out through `tools/closeout_check.py D-C10y-directdw` once the CORPUS entry exists. Advisor pass before any code (done at v1, FIX-FIRST). The cross-family design pass was run by gpt-6.1-sol at effort max, not the named GPT-6-Astra/high (recorded identity, `results/c10y_directdw_codex_design_v1.md:3`; §8 Open for the program). Codex GPT-6-Astra (high) at the implementation review, the verdict, and the promote gate if LEAD.

## 6. Reviews and open points

v1 draft → advisor pass (FIX-FIRST, `results/c10y_directdw_advisor_v1.md`) → cross-family design pass (gpt-6.1-sol, effort max; FIX-FIRST, `results/c10y_directdw_codex_design_v1.md`) → v2 → Astra freeze check (FIX-FIRST, `results/c10y_directdw_astra_freeze_v2.md`) → v2.1 → Astra confirmation (`results/c10y_directdw_astra_freeze_v21.md`, FIX-FIRST) → v2.2 (this file) → Astra confirmation → freeze → implementation (driver: independent supervisor and pre-start budget gate, capture solve, deployed-arithmetic hooks with routing, objectives, micro-batching, loss scaling, wrapper modes, NM-total/ENV application, execution ledger, overlap audit, memory telemetry, readouts, manifest; reader encoding every §3 table and boundary case) → implementation review → recorded D-C10r-rulings-4 (3) reconsideration (decision 0) → pre-start budget gate (§2.6 item 6) → stage 1 → [SCREEN-PASS only: measured forecast and recorded spending decision → stage 2 → stage 3] → verdict → CORPUS/NN.

**Reviewer questions (a)–(e), answered (advisor #13, Codex #13; Codex's answer where they differ).** (a) Use untouched same-process recipe A, its CORPUS/44 A7 envelope, the established A1/A2 controls, and the capture/zero-step/executed-loop reductions. A separate K1 rerun is not required; K1 is not an A7 ceiling. (b) lr_l=0.02·rms(R_l) and T_max=100 are unmeasured fixed heuristics, not a proved fair optimisation budget or a bound on write growth. Record actual norms each step and apply the fit rule at every stop ('at most roughly triple' removed from §2.4). (c) Keep h0_ij+delta_i: compute_z adds the same activation delta at each prompt's lookup index (`memit_dry_run/memit/memit/compute_z.py:95–99,180–185`). (d) Routing-off is not part of the default spend; if it is needed for attribution, freeze it as a separately budgeted secondary experiment before running it. (e) Use the fixed R1 contract (§3), not a progressively permissive baseline-derived floor.

**Decisions (recommendation first).** 0. *Re-schedule after demotion (D-C10r-rulings-4 (3)):* with the results of steps 3 and 4 and the step-5 oracle read, run stage 1 (§2.6 item 5)? The recommendation is made at that time and recorded before dispatch; if the oracle's held-out A7 count is ≤ 18/72, the recommendation is no — a prior from a different writer, not a capacity bound or a gate (advisor #1, Codex #1). This document recommends that the operator make this reconsideration (`EXPERIMENT_RUNBOOK.md:914`; §8 Open for the program). 1. *Write-only scope:* settled — MEASUREMENT-ONLY, not a write route, by program ruling (D-C10r-rulings-3 (2), D-C10u-Aenv (2); §2.7); not put to the operator. 2. *Budget:* stage 1 only, ≤ 120 min elapsed (pre-start gate and independent supervisor, §2.6 item 6); stages 2–3 only after SCREEN-PASS, each with a measured cost forecast, a finite cap and a recorded spending decision; recommend yes to stage 1 only.

## 7. Departures from DOW-KE and decisions where the sources are silent (each open to the reviews)

- **D-1** Key-side projector = the harness's absolute-threshold P (`c10e:28, :173–175`), not DOW-KE's spectral-energy rule `P = I − U_τ U_τᵀ` (§5): keeps the protected subspace identical to recipe A.
- **D-2** No output-side projector `P_out` (§5; Table 3: removing it cost 0.6–2.4 specificity points and moved generalization by −0.5 to +0.75 on Llama-3-8B): no `D_0` statistic exists and building one is a covariance-scale job.
- **D-3** `A^l(0) = R_l` (the paper's initialisation is not in the available text).
- **D-4** One Genesis-shaped batch of 24 requests, not 20 sequential batches of 100 (§6.2); no previous-batch keys `K_p`; cache zero (`c10e:474`).
- **D-5** `B_l` from the sequential capture solve (post-edit keys at layers > 4), so the zero-step write equals the harness's.
- **D-6** Learning rate, step cap and stopping rule are the program's (§2.4); DOW-KE's are in an appendix not in the arXiv source.
- **D-7** α = 1; the NM arm rescales by design as a control, not as an operating point (DOW-KE §6.4 treats α as an operating point).
- **D-8** fp16 frozen model with float32 variables and static loss scaling (no float64 on MPS); the merged fp16 model is scored.
- **D-9** B-z added as both the stub's sham and the test of the research pass's (corrected) premise; the stub's sham "must reproduce A" (`prereg_stubs.md:76`) is read as the ANCHOR-SHAM-INERT descriptor (window [0.8, 1.25] newly set here; CORPUS/50's second-write rule does not transfer), not as a validity or fit gate, because B-z is an active alternative objective and under H-Y2 a gain is a result (advisor #11c, Codex #11c).
- **D-10** The size controls are NM-total (one scalar s = N_A/N_B < 1, run iff N_B > N_A) and ENV (uniform per-layer envelope downscale s_env, run iff s_env < 1), both on actual applied updates and both conditional in stages 2 and 3, never stage 1; no layer is ever scaled up (advisor #11b, Codex #11b, #18).
- **D-11** Process 2 runs only for a stage-2 survivor, as stage 3, with its own baseline gate before candidates; it is the reproducibility run and gate A. A second process is not mandatory after a screen kill (advisor #3, Codex #3).
- **D-12** No activation-vector weight-decay term (`compute_z.py:154–156`); the KL coefficient 0.0625 is applied once to the raw KL (Codex #17).
- **D-13** Optimisation forwards use the deployed effective weight `fp16(W0 + fp16(AB))`; the fp16 casts' backward and the subject-routing mask are surrogate-gradient choices (Codex #16).
- **D-14** The first spend is a single-process A7-only screen capped at 120 min elapsed; B-z, A1/A2 under the candidate, the size controls and process 2 are conditional (Codex #3).

## 8. Review fold log

Reviews folded at v2 (2026-10-07): advisor — Claude Opus 5.5 (`claude-opus-5-5`), `results/c10y_directdw_advisor_v1.md`, FIX-FIRST; cross-family — **gpt-6.1-sol, reasoning effort max** (the actual identity, `results/c10y_directdw_codex_design_v1.md:3`; not the named GPT-6-Astra/high), reviewing v1 SHA-256 `f95c6f64…7554773`, FIX-FIRST. Program rulings recorded, not re-argued: MEASUREMENT-ONLY (D-C10r-rulings-3 (2), D-C10u-Aenv (2)); demotion behind step 5 (D-C10r-rulings-4 (3)), Codex #1's text; the stage-1 screen adopted with Codex #3's design.

- advisor #1 (BLOCKING) — applied-with-change: D-C10r-rulings-4 (3) added to the rulings in force; the scheduling text is Codex #1's (the oracle is a prior, not a bound); decision 0 keeps the advisor's "oracle ≤ 18 → recommend no" as a recommendation, not a gate.
- advisor #2 (BLOCKING) — applied-with-change: §2.7, §3 "What each buys" and §4 use Codex #2's MEASUREMENT-ONLY text, which claims less than "a candidate for an operator route ruling"; §6 decision 1 records the scope as settled by program ruling instead of recommending it; the compaction point kept in §2.7.
- advisor #3 (BLOCKING) — applied-with-change: Codex #3's concrete 120-min A7 screen; recipe A and LAW#3 run before the step-0 checks and smoke (Codex #15), not after; stage 2 is a fresh process, because a spending decision is recorded between stages.
- advisor #4 (BLOCKING) — applied-with-change: Codex #4's fit rule (tested at every stop, minimum over the 24 × 6 matrix, UNDERFIT whatever the held-out count) replaces the cap-only rule and the -UNDERFIT qualifier on counts > 18.
- advisor #5 (BLOCKING) — applied-with-change: Codex #5's exclusive per-process rows and MIXED-NOT-REPLICATED replace the lower-of-two ordering; truth table re-derived.
- advisor #6 (BLOCKING) — applied-with-change: Codex #6's form (exactly three forced lr = 0 iterations with early stopping disabled; a hook-registry snapshot rather than a bare emptiness assertion).
- advisor #7 (ADVISORY) — applied-with-change: Codex #7's text (no cross-model "order of magnitude" comparison; paper numbers marked UNVERIFIABLE from the repo).
- advisor #8 (ADVISORY) — applied: Codex #8's wording, with the advisor's `recommended_sequence.md:13` source.
- advisor #9 (ADVISORY) — applied-with-change: treated as BLOCKING with Codex #9's separate thresholds; the advisor's driver + RSS > 40 GiB sum kept as an extra HALT guard (more conservative), labelled as a non-physical sum.
- advisor #10 (ADVISORY) — applied-with-change: Codex #10's whole-compile rule (≥ 3600 s, warning qualifier); the per-step-time-versus-N compaction note dropped, since N = 24 timings are not a scaling result (Codex #10).
- advisor #11 (ADVISORY) — applied-with-change: (a) Codex's fixed R1 (cosine ≥ 0.99 and relative L2 ≤ 0.10) instead of the ≥ 0.95 floor; (b) single-scalar NM applied, with Codex's matching checks; (c) sham citation applied.
- advisor #12 (ADVISORY) — applied-with-change: Codex #12's audit, under which leakage HALTs (V12) instead of only being recorded.
- advisor #13 (ADVISORY) — applied-with-change: (a) and (c) applied; (b) the fit rule applied but the ×3 write-growth bound removed (Codex #13); (d) routing-off moved out of stage 2 into a separately budgeted secondary (Codex #13); (e) per #11a.
- advisor #14 (ADVISORY) — applied: Codex #14's wording in §2.2.
- Codex #1 (BLOCKING) — applied: verbatim in the status line, plus the conservative recommendation that the operator makes the reconsideration (`EXPERIMENT_RUNBOOK.md:914`).
- Codex #2 (BLOCKING) — applied: §2.7, §3 "What each buys", §4, §6 decision 1.
- Codex #3 (BLOCKING) — applied: §2.6 item 5, §2.11, §3 screen table, D-11, D-14, §6 decision 2; stage 2 fixed as a fresh process that repeats the baseline gate.
- Codex #4 (BLOCKING) — applied: §3 Fit, §2.3 B-z zero-denominator rule, §2.4, §2.9.
- Codex #5 (BLOCKING) — applied: §3 decision order and tables; truth table extended with ENV values, screen rows and boundary cases; INCOMPLETE scoped to the recipe's own records and V5 controls, with missing size/anchor controls read through attribution.
- Codex #6 (BLOCKING) — applied: §2.8 (i), (iii-b), (viii); V3.
- Codex #7 (ADVISORY) — applied: §0, header source caveat, §2.9.
- Codex #8 (ADVISORY) — applied: §0.
- Codex #9 (BLOCKING) — applied: §2.10 (arm cache row, telemetry and thresholds) and §2.8 (vi), with the 12-request subset fixed as A7 requests 0–11; advisor #9's summed guard added.
- Codex #10 (ADVISORY) — applied: §3 W2, §2.9.
- Codex #11 (ADVISORY) — applied: R1; §2.5 NM-total; B-z reading and D-9. A failed baseline regeneration instrument is read as NOT-REPRODUCIBLE (conservative; the review left its label unstated).
- Codex #12 (ADVISORY) — applied: §2.6 item 2, V12.
- Codex #13 (ADVISORY) — applied: §2.4 learning-rate reason, §2.8 preamble, §6 answers.
- Codex #14 (ADVISORY) — applied: §2.2.
- Codex #15 (BLOCKING) — applied: §2.6 item 5 order, V4, §5.
- Codex #16 (BLOCKING) — applied: §2.3, §2.8 (iv), V9, §2.10 row, D-13; the functional path is fixed as a forward hook returning `F.linear(input, W_eff)` with a per-position routing mask.
- Codex #17 (BLOCKING) — applied: §2.3 KL and graph hygiene, §2.4 precision row, §2.8 (vi), (vii), (ix), D-12; the nonzero KL intervention is fixed as request 0's solved delta.
- Codex #18 (BLOCKING) — applied: §2.5 ENV, §3 attribution, D-10.
- Codex #19 (BLOCKING) — applied: §3 G2 and G6, §2.9.
- Codex #20 (BLOCKING) — applied: §2.2, §2.8 (v), V7, W1, §2.9.
- Codex #21 (BLOCKING) — applied: §2.6 items 1 and 3, §2.7 reproducibility rule, §4 spec-amendment flag withdrawn.
- Codex closing note, override ledger (ADVISORY) — applied: §2.6 item 3, V6, §2.12 `ledger.json`.

Declined: none.

**Reviewer conflicts and their resolution (the more conservative option, which halts, blocks routing or claims less).**
1. Who makes the D-C10r-rulings-4 (3) reconsideration: Codex #1 allows the standing approval; the advisor and `EXPERIMENT_RUNBOOK.md:914` point to the operator. Codex's text is kept, as the program instructed, with the recommendation that the operator decides (Open, item 1).
2. Oracle ≤ 18: advisor, recommend no; Codex, not a bound. Both kept: a recommendation from a prior, never a gate.
3. Stage-1 order: the advisor ran step 0 before recipe A; Codex #15 requires LAW#3 first. Codex taken.
4. Fit: the advisor tested only capped writes and qualified counts > 18; Codex tests every stop and withholds the base label. Codex taken.
5. Cross-process: the advisor took the lower of two labels; Codex stores both as MIXED-NOT-REPLICATED. Codex taken (claims less).
6. Memory: the advisor summed driver + RSS; Codex forbids the sum as a measurement. Both applied as HALT guards.
7. Memory severity: advisor ADVISORY, Codex BLOCKING. Treated as BLOCKING.
8. R1: the advisor's ≥ 0.95 floor; Codex's fixed 0.99 plus relative L2 ≤ 0.10. Codex taken.
9. Overlap audit: the advisor records it; Codex HALTs on leakage. Codex taken.
10. Learning-rate rationale: the advisor accepted a ×3 bound; Codex shows it is not a bound. Codex taken.
11. Routing-off: the advisor allowed a stage-2 secondary; Codex requires a separately budgeted experiment. Codex taken.
12. TTL: the advisor flagged a write over 60 min; Codex flags a whole compile of ≥ 3600 s, equality included. Codex taken.

**Open for the program (recommendation first).**
1. *Reconsideration authority.* Recommend the operator make the D-C10r-rulings-4 (3) reconsideration in person, since the runbook says steps 6–7 "are re-argued with the operator before scheduling" (`EXPERIMENT_RUNBOOK.md:914`). The alternative is to record it under the D-C10r-rulings-8/9 standing approval (Codex #1).
2. *Reviewer identity.* The design pass was gpt-6.1-sol at effort max, not the GPT-6-Astra/high reviewer that CLAUDE.md names. Recommend accepting it as the cross-family design pass, recording the identity, and keeping GPT-6-Astra/high for the implementation review, the verdict and any promote gate.
3. *DOW-KE source.* r_gap ≈ 0.33 and the §5 quotations cannot be verified from the repo. Recommend retaining the arXiv 2608.16932 v1 LaTeX source under `external_prior_art/` before the freeze. No gate depends on these numbers, so the freeze need not wait for it.
4. *Stage-1 cap.* The cap C₁ = 7,200 s is kept (Codex #3). The I-INFER arithmetic (110–165 min) is not a measured certificate; the pre-start gate (§2.6 item 6) refuses launch when the forecast from measured timings exceeds the cap, so no spend precedes discovering infeasibility. A refusal comes back as a recorded spending decision, not as a result.

### Astra freeze-check fold log (v2 → v2.1)

`results/c10y_directdw_astra_freeze_v2.md`, GPT-6-Astra, FIX-FIRST, 7 BLOCKING, reviewing v2 SHA-256 `a6028bdf…2a2151`. Source claims (H:134–136, 162–163, 315, 337, 382–392, 492) re-read and confirmed before folding.

- Astra-freeze BLOCKING 1 → §2.6 items 5–6, §2.11, §3 S2/S3 and truth table, §5, §6 decision 2, Open 4: pre-start budget gate with a finite cap per stage (C₁ = 7,200 s), `launched=false` refusal, independent supervisor with a hanging-worker test, in-run projections; the "post-smoke projection" rule and the acceptance of discovering infeasibility after spending removed.
- Astra-freeze BLOCKING 2 → §3 V13 and a new record-completeness paragraph before the screen table (§2.9 field list annotated): typed nullable diagnostics; INCOMPLETE ordering; NOT-RUN records not required.
- Astra-freeze BLOCKING 3 → §2.5 NM/ENV headers, §2.6 items 5 and 7, D-10: "stage 2 only" replaced by conditional in stages 2 and 3, scale-1 provenance, stage-3 regeneration, explicit stored-update arithmetic.
- Astra-freeze BLOCKING 4 → §3 T1, truth table (two authored rows), "What each buys": uncovered a=12 case closed; causal readings of the positive and of TRADEOFF/LARGE-WRITE/SIZE-NOT-EXCLUDED removed.
- Astra-freeze BLOCKING 5 → §2.8 preamble and V3: per-check applicability, `apply_stored` substitutions, standing check (i) before LAW#3.
- Astra-freeze BLOCKING 6 → §2.9 raw gate inputs, §3 G3/G5, R1 distance denominator, R3 clarification.
- Astra-freeze BLOCKING 7 → §2.3 B-z (zero-denominator at every evaluation) and §3 Fit (per-arm fit scope across A1/A2/A7).
- ADVISORY applied (one-line wording): §2.1 `compute_z` "at most 25 loss evaluations and 24 Adam updates"; §2.1 `compute_ks` group averaging. Not applied (notes only): P:45/47 exact-arithmetic-identity wording; fold-audit and LAW#3 transcription notes need no change.
- Astra confirmation BLOCKING 1 (v2.1 → v2.2) → §2.8 (iv) and V9: parity scoped to every optimised B-z or B-e2e write; V9 NOT-APPLICABLE for `apply_stored`, stored-update checks of §2.8 remain mandatory.
- Astra confirmation BLOCKING 2 (v2.1 → v2.2) → §3 decision order and record-completeness paragraph: INCOMPLETE only for missing records of the recipe being classified (incl. V5 controls); missing size/anchor comparators give SIZE-UNTESTED/ANCHOR-UNTESTED under attribution.
- Astra confirmation BLOCKING 3 (v2.1 → v2.2) → §2.6 budget paragraph, §3 S3, truth table: a budget stop by an in-run projection or the supervisor deadline is HALTED-BUDGET before write completion and INCOMPLETE-BUDGET after write completion but before readout completes; new pre-readout-projection reader case.

Declined: none.


## 9. Amendment T — live telemetry and per-prompt answers (2026-10-08, pre-observation; D-C10r-rulings-11, D-C10r-dash-1, D-C10w-p2rerun)

Written before any C10Y code, build or process exists. On 2026-10-08 there is no `experiments/track_c/c10y_*` file and no `results/c10y_directdw/`. The only `results/c10y_*` entries are the five review files named in the status line (`:3`) and §6. §0–§8 are unchanged. This section adds an instrument and launch rules. It changes no hypothesis, recipe, arm, objective, optimiser setting, stimulus, metric, threshold, gate, qualifier, label, table row, stage cap, budget rule or memory guard, and it replaces no sentence above. Where it conflicts with the build brief, this section governs.

Sources:
- runbook §5 rows D-C10r-rulings-11 (`EXPERIMENT_RUNBOOK.md:363`), D-C10w-p2rerun (`:378`) and D-C10r-dash-1 (`:379`);
- the approved pattern, C10Z §9(h) and §9.1 (h′1)–(h′5) (`docs/C10Z_ASTRA_PREREG.md:467–476`, `:554–604`);
- the program's C10Y build brief, §5 (telemetry basis) and §9 Q1–Q3 and Q7. This section rules on each of those questions below.

**Terms.** "Live telemetry" below means the opt-in JSONL writer of this section. It is not the §2.10 **memory telemetry** (`:146`, `:169`): the synchronised allocation, RSS and host-memory samples that the memory guards read. Memory telemetry is required, and its absence is a preflight failure (`:169`). The live-telemetry switch never disables, alters or adds to it.

**The rulings, quoted.**
- D-C10r-rulings-11 (`EXPERIMENT_RUNBOOK.md:363`): "an opt-in writer appending small JSONL snapshots during a run to `results/<exp>/telemetry/` (per-layer write norms, per-position target probabilities, logit-lens top-k at each band layer for the probe prompts, phase markers) … It must not change any computed result: off by default, or proven inert under LAW#5 (identical counts and records with telemetry on vs off); test-first; reviewed with the build (advisor + Astra); folded in as a dated pre-observation amendment to each frozen prereg (C10X, C10Y, C10Z) before its build."
- D-C10r-dash-1 (`:379`): "every new experiment build (C10X, C10Y, ASTRA later attempts) streams per-prompt generated text through the opt-in, inertness-proven telemetry path (… a JSONL line per prompt with subject, template, generated text, right/wrong), admitted only after its LAW#5-style inertness check".
- D-C10w-p2rerun (`:378`): "STANDING RULE: a run whose result is compromised (halted, corrupted, or read through a patch) is re-run, never read around by a deviation note".

(T1) **Switch.**
- `C10Y_TELEMETRY` absent means live telemetry is off. Off is the default.
- Exactly `"1"` means on, and only when `C10Y_TELEMETRY_INERTNESS` names a valid INERT record under (T8), and the stage's pre-start forecast carries the telemetry phase of (T10).
- Any other value (`"0"`, `"true"`, `""`, `" 1"`) is refused, and so is `"1"` with an absent or invalid record. A refusal comes before any write and before the supervisor launches a worker: the driver exits non-zero and writes nothing. This is a launch refusal, not a run.
- `run.json` (§2.12, `:179`) always carries two keys:
  - `"telemetry": true|false`;
  - `"telemetry_inertness": {"path", "sha256"}` or `null`.

  Under (T7)'s controlled proof, these two values are the only record difference between telemetry on and off. The live exceptions are those enumerated in (T10).
- Only telemetry-on launches require or verify an inertness record; telemetry-off launches require neither that record nor telemetry calibration.
- Every telemetry-off launch line removes both variables explicitly (`env -u C10Y_TELEMETRY -u C10Y_TELEMETRY_INERTNESS …`; the C10Z (j′) precedent, `docs/C10Z_ASTRA_PREREG.md:608`).

(T2) **Path and line format.**
- The file is `<OUT_DIR>/telemetry/telemetry_<tag>.jsonl`:
  - `<tag>` is `s1` for stage 1, `p1` for stage 2 and `p2` for stage 3, following §2.12's rule that files suffixed `p1`/`p2` belong to the stage-2 and stage-3 processes (`:179`);
  - `OUT_DIR` is `results/c10y_directdw/`, or the re-run directory of (T12).
- With telemetry off, no `telemetry/` directory exists.
- The file is opened once, in append mode. Its first line is a header.
- Every line holds `kind`, `t_utc`, `elapsed_s`, `cumulative_s`, `process` and `run_id`:
  - `elapsed_s` is the time from entering the telemetry call to just before that line is written;
  - `cumulative_s` is the full time of all earlier lines, writes included (C10Z (h′2), `:558`).
- Each line is serialised with `json.dumps(…, allow_nan=False, sort_keys=True, separators=(",",":"))` plus a newline, then written, flushed and fsynced.
- The telemetry clock is `time.perf_counter`, bound at import. It is never the supervisor clock, the budget-projection clock or the memory-guard sampler of §2.6 item 6 and §2.10 (`:96–98`, `:169`).

(T3) **Line kinds, placement and volume.**

| kind | where | payload |
|---|---|---|
| `phase` | `stage_start`/`stage_end` around each §2.6 item 5 phase (`:89`); `recipe_start`/`recipe_end` immediately around each `H.run_recipe`; `write_start`/`write_end` in the wrapper for modes `anchor`, `e2e` and `apply_stored` (§2.6 item 4, `:88`); `halt` on the worker's halt path, immediately before the diagnostic is written (§5, `:301`) | phase, recipe, mode, arm or halt code |
| `opt_step` | after each **accepted** optimiser step (§2.4, `:70`); an overflow retry writes no `opt_step` | step; the loss components already computed (`L_edit`, `KL_raw`, weighted KL, or `L_z`); loss scale; retries so far; per-layer planned ‖A^l B_l‖_F as recorded in the §2.9 trace (`:146`) |
| `target_probs` | after each accepted B-e2e step; once per completed write for the merged fit | per (request, frame, target position), `p = exp(−nll)` from the detached gathered target log-probabilities that `L_edit` already computed (§2.3, `:51`). These are retained per micro-batch until the step is accepted, discarded on an overflow retry, and exponentiated on CPU in float64. Once per write: the merged fit matrix `f_ij` (24 × 6), and for B-z also `r_ij`, as the driver records them (§2.9, `:146`; §3 Fit, `:200–202`) |
| `write_norms` | after each completed write in every scored recipe, where the driver records §2.9 write geometry (`:144`) | per layer: actual ‖D_l‖_F, planned ‖A^l B_l‖_F and the ratio to recipe A, echoed from the driver's float64 values (T6). Recipe A's harness `delta_norms` (`c10e_bandknob.py:213–215`) are echoed labelled `harness_fp32` |
| `logit_lens` | pristine: once, immediately after LAW#3 (V4) passes and the restored pristine-band hashes verify (§2.6 items 1 and 5, `:85`, `:89`). Post-write: in the A7 arm of each scored **candidate** recipe (B-z, B-e2e, NM-total, ENV; never recipe A, whose post-write hook runs before V4), inside the driver's own probe hook after its probes (`ARM_HOOKS`, `c10e_bandknob.py:494–495`), with no change to the dict the hook returns | layers `hp.layers` (4–8); the 24 A7 canonical prompts at the last position; top-5 `[id, text, prob]` per layer |
| `answer` | every call of the observed scorer of (T4) | the schema of (T4) |

- The pristine lens call is a no-hook, no-write forward on the pristine band. It is placed after V4, and recipe A's post-write lens call is suppressed, so that no instrument forward precedes the baseline gate (`:89`). The observed scorer runs during recipe A, but it adds no forward (T4).
- **Volume, stage 1:**
  - 384 `answer` lines: recipe A on A1, A2 and A7, 3 × 96; B-e2e on A7, 96;
  - 2 lens calls × 24 = 48 lens forwards: the pristine call after V4, and the B-e2e A7 arm;
  - at most 100 `opt_step` and 101 `target_probs` lines per B-e2e write (T_max = 100, `:63`); a B-z write has at most 100 `opt_step` lines and one `target_probs` line;
  - 4 `write_norms` lines: recipe A's three arms and the B-e2e A7 write;
  - phase lines and the header.
- **Volume, stages 2 and 3:**
  - 96 `answer` lines per evaluated arm of each scored recipe (A, B-z, B-e2e, and NM-total or ENV where triggered; §2.5, `:77–81`);
  - one lens call after V4 (pristine), and one per scored candidate recipe's A7 arm.

  No line is written per requirement, except `answer`.
- **Logit lens** (the C10Z (h′5) semantics, `:601–604`):
  - one no-grad forward per prompt, with `output_hidden_states=True`, `use_cache=False` and no hook;
  - this runs after the write's hooks are removed (§2.6 item 4, `:88`), on the merged model;
  - the residual after band layer l is `hidden_states[l+1][:, -1, :]` (installed transformers, `modeling_qwen2.py:528–570`);
  - then `model.model.norm`, then `lm_head`;
  - the softmax and top-5 are computed on a detached CPU float64 copy of the 151,936-wide logits row (T6);
  - it raises if `max(layers) > num_hidden_layers − 2`.

(T4) **Per-prompt answer lines (D-C10r-dash-1). Build-brief Q2 ruling: the observed scorer is adopted.**

*Reason:*
- The harness scorer `full_seq_match` computes the generated ids and returns only two booleans (`c10e_bandknob.py:108–117`).
- A statement-identical observed copy shows exactly the tokens that were scored and adds no forward.
- A separate telemetry decode would add about 816 greedy forwards per three-arm recipe inside the 7,200-s stage-1 cap (`:94`), and its text could differ from the scored decode.

- **Installation.** Only while telemetry is on, `H.full_seq_match` is rebound to `observed_full_seq_match`:
  - immediately before each scored `H.run_recipe` call (the recipes of §2.5, `:77–81`);
  - restored to the original object in `finally`.
- **Not installed** for:
  - the stimulus base report (`c10e_bandknob.py:449–455`);
  - any §2.8 check cell;
  - the train–deploy parity generation of §2.8 (iv) (`:132`), which is driver code, not the scorer.

  Those run unchanged and emit no `answer` line.
- **The copy.** `observed_full_seq_match` is a statement-for-statement copy of `c10e_bandknob.py:108–117`:
  - the same `@torch.no_grad()`, `H.tok`, `H.model` and `H.DEV`;
  - plus exactly one inserted expression statement, `sink(prompt, target_ids, gen)`, placed immediately before the unchanged `return gen == list(target_ids), gen[0] == target_ids[0]` (`:117`).

  The original scorer has no `full` or `first` variable: it returns the two expressions directly (`:117`). The sink computes both predicates with those same expressions, inside its own protected body (T5). It copies `gen` and `target_ids` and never mutates them.
- **With telemetry off,** the driver asserts at each recipe start that `H.full_seq_match` is the original object. This is an assertion only, never a record field.
- **Line schema** (`kind: "answer"`, plus the (T2) common fields):

| field | type | value |
|---|---|---|
| `recipe` | str | the `run_recipe` name |
| `arm` | str | the `H.ARMS` key (`A1_single`, `A2_coherent2`, `A7_coined_coined`; `c10e_bandknob.py:244–246`), matched from `H._ARM_STATE["requests"]` (`:487`). Stage 1's A7-only rebinding of `H.ARMS` (`:88`) is honoured |
| `phase` | str | the §2.6 item 5 phase |
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
- Live telemetry reads only. It never:
  - writes a parameter, buffer or A, or registers a hook. The deployed-arithmetic hooks and routing masks of §2.3 (`:51`) are the driver's own;
  - calls `backward`, retains a graph or reads anything not already `.detach()`ed;
  - changes A's `.grad`, the Adam state, the loss scale or the retry count;
  - calls the supervisor, a budget projection, a memory-guard sample, `torch.mps.synchronize` or the stage clock;
  - writes into any §2.12 record or the execution ledger (V6, `:191`), or adds a key to an `ARM_HOOKS` result;
  - feeds a gate, label, qualifier or reader.
- Its `.cpu()` copies may synchronise the device implicitly. They change no value.
- **Failure.** Every public method body catches `Exception`, never `BaseException`. On failure it:
  - writes exactly one `C10Y_TELEMETRY_DISABLED <ExcType>: <msg>` line to `sys.__stderr__`;
  - disables later calls;
  - never propagates the exception.

  The marker goes to `sys.__stderr__` because `run_recipe` runs the write, and with it the wrapper's optimisation, inside `contextlib.redirect_stdout` (`c10e_bandknob.py:488–489`).
- If the sink fails, the observed scorer still returns its identical result. A failure inside the copied scorer statements propagates as the original's would.
- A declared disable (the marker above) does not compromise the science record and triggers no re-run; (T11) records it as an audit failure. Any other missing, malformed or unexpected output is handled by (T11).

(T6) **Float64 (the P2 lesson, `EXPERIMENT_RUNBOOK.md:377`: a 22.5M-element fp32 accumulation gave cosines of 1.007–1.009). The 2048 × 11008 band updates are exactly that size.**
- Every value that live telemetry emits as a reduction over a model-sized tensor (hidden, intermediate, vocabulary or weight-sized) is computed in float64 on CPU. Telemetry either echoes the driver's float64 value, or computes it itself from detached CPU float64 copies: the lens softmax, and `exp(−nll)`.
- The single exception is recipe A's harness `delta_norms`, echoed and labelled `harness_fp32`.
- Telemetry never emits an unlabelled fp32-reduced norm.
- Live telemetry holds at most one 151,936-wide float64 row (about 1.2 MB) and one line at a time. The §2.10 guards (`:169`) apply unchanged.

(T7) **Code-path proof, test-first (the analogue of C10Z (h′4), `:580–585`).**
- **Isolation.** The tests are written and recorded failing before the writer exists. They run CPU-only on a stub `H` and tiny CPU models, under temporary roots, with an audit-hook write guard that refuses any write under the real `results/` or `architecture_profile/`. The guard is proved by a positive control. This is the guard whose absence let a C10W selftest dispatch "a real P2 training stage against the live tree" (`results/c10w_oracle/_quarantine_selftest_leak_20261008/README.md:3`). A test that writes to the live tree fails the build. Deny real experiment subprocess dispatch; allow only explicitly isolated stub workers. Install protection before imports, resolve protected paths, and positively test the subprocess boundary without launching a real stage.
- **Identical with telemetry on and off,** under injected clocks, a fixed `run_id` and a fixed seed (`:72`):
  - A at every optimiser step (`torch.equal`);
  - the merged weights;
  - every return value, record, ledger entry and reader output;
  - the out-directory file set, excluding `telemetry/` (JSON-normalised);
  - the only exceptions are the two `run.json` values of (T1).
- **Identical counts:**
  - calls to the supervisor clock, the budget projection, the memory-guard sampler and `sync`;
  - stub-model forwards, excluding lens forwards tagged as telemetry;
  - the observed scorer's outputs and its exact sequence of model inputs, against the original `full_seq_match`.
- **AST check** against the text of `c10e_bandknob.py:108–117`, read from the file: the observed copy differs only by the one inserted `sink(prompt, target_ids, gen)` statement, and the (T8) reference capture only by its one inserted `capture(prompt, target_ids, gen)` statement.
- **Reference-capture validation.** The (T8) reference capture returns outputs and issues a model-input sequence identical to the original `full_seq_match`, and the IDs it captures equal the generated IDs the original computes.
- **Unchanged across every telemetry call,** checked before and after:
  - every parameter and buffer (`torch.equal` and `data_ptr`);
  - `torch.random.get_rng_state()` and `model.training`;
  - every module's `_forward_hooks`, `_forward_pre_hooks` and `_backward_hooks`;
  - `torch.is_grad_enabled()`;
  - A's `.grad`.
- The on-file holds the header and every kind of (T3), with exactly 96 `answer` lines per evaluated arm.
- This proves the code path only. It does not prove live inertness, which is (T8)'s job.

(T8) **MPS inertness check (LAW#5): the admission screen (the analogue of C10Z (h′3), `:566–579`).**
- **Runner.** `experiments/track_c/c10y_directdw_telemetry_check.py` runs `telemetry_mps_inertness_check()` from the driver:
  - once, on MPS, with the GPU otherwise idle;
  - in one process, on the pristine model, with context templates sampled once in-process (`memit_main.py:304–323`) before any pass;
  - writing `results/c10y_directdw_telemetry_inertness/<UTC>/inertness.json`. An existing `inertness.json` is refused.
- **Method.**
  - One uncompared warm-up: one scorer call and one science forward.
  - Then three passes: P1 plain, T telemetry on, P2 plain. Each pass runs, in order:
    1. in T only, `logit_lens` on the 24 A7 canonical prompts;
    2. the 96 A7 scored prompts in `eval_arm` order (per subject: `CANON`, then the three `PTEST`; `c10e_bandknob.py:360–363`). Each goes through a scorer copy that differs from `:108–117` by one inserted statement before the unchanged return:
       - in P1 and P2, the **reference capture** `capture(prompt, target_ids, gen)`, which appends a copy of `gen` to a plain list;
       - in T, the telemetry `sink(prompt, target_ids, gen)` of (T4), with a live writer.

       Each pass records, per prompt, the exact generated-ID sequence and the `(full, first)` flags that the scorer returned. The reference capture is validated before use by (T7).
    3. in T only, `logit_lens` again;
    4. the science forward: the pristine `L_edit` batch of A7 requests 0–5 (one micro-batch, §2.4, `:71`), built as `compute_z.py:41–73`, with logits gathered at the target positions only (§2.3, `:51`) and kept as CPU fp32 copies.
- **Verdict** (identical tokens are required, as in C10Z, `docs/C10Z_ASTRA_PREREG.md:575`).
  - INVALID if any of the following holds. A disabled writer or missing output is never INERT.
    - The five band `down_proj` weights, hashed before and after, differ.
    - A T-pass lens call fails or yields a non-finite value.
    - The T-pass telemetry output is incomplete: a `C10Y_TELEMETRY_DISABLED` marker; other than exactly 96 `answer` lines; or other than 2 `logit_lens` lines of 24 prompts each.
  - Otherwise NONDETERMINISTIC-BASELINE, unless P1 and P2 have identical generated-ID sequences and identical flags for all 96 prompts (exact) and `torch.equal` (bitwise) gathered logits.
  - Otherwise INERT if T equals P1 in the same three respects, and T's `answer` lines carry those same IDs and flags. NOT-INERT if not.
  - Only INERT admits live telemetry. Any other verdict keeps it off for this prereg. A revised writer then needs its own dated amendment.
- **Timing section** (after P2; never compared, and never part of the verdict). For the (T10) per-kind bounds, it emits each line kind of (T3) with full-size payloads, built from MPS tensors of the stage's shapes, and times every emission from preparation (detach, CPU transfer, float64 reduction, serialisation) through fsync, with the repetition count recorded:
  - `opt_step`: five layers' planned norms and the loss components;
  - `target_probs`: one accepted step's gathered target log-probabilities for 24 requests × 6 frames × the A7 target positions, and one 24 × 6 `f_ij`;
  - `write_norms`: five layers;
  - `phase`.
- **Record.** It holds:
  - `schema`, `decision_id` "D-C10r-rulings-11", `device` "mps", `verdict`, `control_equal`, `telemetry_equal`, `generated_equal`, `telemetry_complete` and `weights_unchanged`;
  - `answer_calls` (96) and `lens_forwards` (48);
  - the measured `lens_forward_seconds` and `answer_line_seconds` (each written T-pass line, timed), and the timing section's per-kind seconds with their payload sizes and repetition counts, which (T10) cites as its timing artifact;
  - the SHA-256s of the driver, reader, check script, `c10e_bandknob.py`, hparams, `compute_z.py`, `compute_ks.py`, `rome/repr_tools.py`, `memit_main.py` and this prereg;
  - `env`: python, machine, platform, torch and transformers versions, and `model_rev`;
  - start and finish times.
- **Admission.** Only telemetry-on launches require or verify an inertness record; telemetry-off launches require neither that record nor telemetry calibration. At every telemetry-on stage start, the driver requires every recorded hash and `env` field to match the current files and environment. A changed source makes the record unusable, and the check is then re-run in a new `<UTC>` directory.
- **Scope, stated in the record.** INERT establishes equality only for these pristine outputs, under the recorded identity. It does not establish resource inertness, or inertness of the optimisation loop or of edited-arm outputs on MPS. The loop is covered by (T7) on CPU only. On MPS, edited outputs, the optimisation loop and resource inertness remain UNVERIFIED, as in C10Z (h′2) (`:563`). The post-run audit of (T11) adds a per-run check of the answer path.
- **Cost (I-INFER).**
  - Per pass: the A7 scorer runs 528 greedy forwards. That is 132 canonical + 396 held-out tokens: the C10 A7 values are 4–6 tokens, with held-out per-position denominators 72, 72, 72, 72, 69 and 39 (`docs/C10X_ENGINEPATH_PREREG.md:13`, citing `CORPUS/45_C10L_MINT_TOKEN.md:24`). Add one micro-batch forward.
  - In all: about 1,640 forwards. At C10Z's planning range of t = 0.03–0.15 s per forward (`docs/C10Z_ASTRA_PREREG.md:579`), that is about 0.8–4.1 GPU-minutes, plus model load, context sampling and preflight, which are UNMEASURED.
  - The check is its own GPU job, one GPU job at a time, outside C₁ (`:94`) and outside any stage-2/3 cap.
  - **Authorization (program ruling 2026-10-08).** The check is GPU spend outside the experiment's caps. The program does not self-authorize it: it is dispatched only under a recorded authorization that names its cost, as C10Z's analogue required the operator's yes (C10Z (h′3), `docs/C10Z_ASTRA_PREREG.md:566–579`). Before dispatch it records a D-ID in runbook §5 with the stated cost, and afterwards the measured GPU time.

(T9) **Telemetry setting per stage. Build-brief Q3 ruling (first-stage setting).**
- **First attempt: telemetry off (program ruling 2026-10-08).** Every stage of the first attempt runs with live telemetry unset, whatever any inertness record says; the §2.10 memory telemetry is unaffected and stays required. Live telemetry may be switched on only for a later attempt, only after an INERT (T8) record exists under the authorization above, and only when the stage-1 forecast carries the (T10) telemetry phase.

  *Reason:*
  - C10Z ruled the same for its first attempt (§9.1 (j′), `docs/C10Z_ASTRA_PREREG.md:609–610`).
  - A telemetry-on stage that halts on budget must be re-run in full under D-C10w-p2rerun (`EXPERIMENT_RUNBOOK.md:378`); the first clean measurement takes priority over live display.
  - Telemetry-off first attempts do not provide generated-answer display through this design; live answers await admitted telemetry and its dashboard adapter (T4).
- **Stage 3** runs with the setting of the stage-2 process it regenerates, so that R1–R3 compare equally instrumented processes (`:244–248`). A different setting is refused before any write. Only telemetry-on stages re-verify the inertness record under (T8).
- **Replacements and the replication pair.** A replacement with changed telemetry setting cannot join the prior replication pair. Regenerate the required pair with telemetry off, retaining all original artifacts, eligibility gates and spending requirements.

(T10) **What telemetry can change; budget; description rule. Build-brief Q3 ruling (cost, caps, description rule).**
- **Budget.** Off dispatch needs no telemetry phase. With telemetry on, the stage's pre-start forecast (§2.6 item 6, `:92`) includes a telemetry phase, built from separately justified per-kind bounds covering preparation through fsync, with workload counts and scaling assumptions:
  - for each line kind of (T3) (`phase`, `opt_step`, `target_probs`, `write_norms`, `logit_lens`, `answer`):
    - the stage's workload count at T_max = 100 accepted steps and the stage's arms;
    - the per-emission upper bound, taken from the maximum measured time for that kind in the (T8) record (the timing section, `answer_line_seconds` and `lens_forward_seconds`) at a payload no smaller than the stage's;
    - the scaling assumption from the measured payload to the stage's payload, stated.
  - No kind's bound is borrowed from another kind.
  - Any kind without a measured, defensible bound is an unbounded component: the forecast is UNVERIFIED and telemetry-on dispatch is refused, as the frozen `docs/C10Y_DIRECTDW_PREREG.md:92` requires.
  - Telemetry's time counts against C₁ = 7,200 s (`:94`), any stage-2/3 cap, the in-run projections and the ≥ 23-minute readout reserve (`:98`).
  - It is never subtracted from a duration, cap, projection or W2.
  - T_max, micro-batching and the optimiser settings never change for it (`:175`).
- **Fields that may differ with telemetry on:**
  - timing fields: W2's per-patch compile time (`:252`), per-write wall-clock and the §2.9 trace timings (`:146`), in-run projections (`:98`), and timestamps;
  - memory-telemetry observations: driver allocation and RSS (`:169`);
  - telemetry's own two `run.json` values (T1).

  A stage near a limit can therefore end HALTED-BUDGET or INCOMPLETE-BUDGET (`:98`), trip a §2.10 memory guard (`:169`), or gain EXCEEDS-TTL (`:252`) where a telemetry-off stage would not. Every count, flag, hash, target, A trajectory, merged weight and label is otherwise identical under (T7). On MPS that is established only within (T8)'s scope.
- **Description rule** (like C10Z's, `docs/C10Z_ASTRA_PREREG.md:565`; it changes no gate or label):
  - If a telemetry-on stage ends HALTED-BUDGET, INCOMPLETE-BUDGET or with a memory-guard HALT, the program reports it as possibly affected by telemetry. Under D-C10w-p2rerun it re-runs that stage with telemetry off, in a re-run directory (T12). The pair rule of (T9) applies: a replacement with changed telemetry setting cannot join the prior replication pair, so the required pair is regenerated with telemetry off.
  - If a telemetry-on write carries EXCEEDS-TTL, a non-blocking qualifier (`:232`), the program reports it as possibly affected by telemetry. It does not treat that write as evidence about compile time until a telemetry-off process says the same.

(T11) **Post-run answer audit (model-free).**
- **When.** Before the reader is run on a telemetry-on stage, the program runs the check runner's model-free `audit` entry point on that stage's out directory. It writes `<OUT_DIR>/telemetry/audit_<tag>.json`.
- **What it compares,** for every scored recipe and arm, with exact equality:
  - the `answer` lines' `full` and `first`, keyed by (`recipe`, `arm`, `subj`, `template`);
  - the per-prompt flags that `run_recipe` returns as `detail` (`c10e_bandknob.py:497`; row fields at `:366–374`), as the stage's record holds them (§2.12, `:179`): `canon_full` and `canon_first` for `CANON`, and `para_full_hits[k]` and `para_first_hits[k]` for `PTEST[k]`.
- **What the audit checks.** It passes only if every expected line is present, well formed and exact. Each of the following is an audit FAIL, with its cause recorded; none passes silently:
  - MISMATCH: a `full` or `first` that differs from the record;
  - DUPLICATE: two lines with one key;
  - MISSING: an expected key (96 per evaluated arm) with no line and no preceding disabled marker;
  - **Schema rule:** Validate each line against its kind-specific schema. All kinds require T2 fields; only `answer` requires T4 fields and answer-key membership. Admit exactly one initial header under an explicitly defined header schema. Unknown kinds or fields fail against the applicable schema.
    - The header schema: the (T2) fields with `kind` = `"header"`, plus `schema` = `"c10y_directdw_telemetry/v1"` (str) and `telemetry` = `true` (bool). Nothing else.
    - The schemas of `phase`, `opt_step`, `target_probs`, `write_norms` and `logit_lens` are the (T2) fields plus that kind's payload in the (T3) table.
  - MALFORMED: a line that is not strict JSON; a line missing a field its kind's schema requires; a field of the wrong type, or a null where the schema has none; or a header that is absent, not first, or repeated;
  - UNEXPECTED: an unknown `kind`; a field outside its kind's schema; or an `answer` key outside the scored recipes and arms;
  - DISABLED: lines missing after a `C10Y_TELEMETRY_DISABLED` marker.
- **Disposition of MISMATCH, DUPLICATE, MISSING, MALFORMED or UNEXPECTED.** The scorer or writer ran outside its proven, declared behaviour:
  - the stage is treated as compromised;
  - it is re-run with telemetry off in a re-run directory (T12), never read around (D-C10w-p2rerun);
  - the pair rule of (T9) applies.
- **Disposition of DISABLED.** The declared failure path of (T5) operated:
  - the audit FAILs and is reported;
  - the missing prompts' answer path is unaudited;
  - the science record stands under (T5); no re-run.
- The reader never reads `telemetry/`.

(T12) **Re-run directories. Build-brief Q7 ruling.**
- **The first attempt** keeps §2.12's single directory `results/c10y_directdw/` (`:179`).
- **A re-run** of stage s (1, 2 or 3) after a halt or a compromised result writes to a new directory, `results/c10y_directdw_s<s>_rerun<k>/`, with logs in `<dir>/logs/`. The driver refuses an existing one.
  - k = 1, 2, … counts the re-runs of that stage.
  - File names inside the directory follow §2.12 unchanged.
  - Telemetry goes in `<dir>/telemetry/`.
- **Stage-2 and stage-3 re-runs** read the frozen `context_templates.json` of the stage-1 directory they continue (§2.6 item 2, `:86`), by absolute path. They record that path and its SHA-256 in `manifest.json`. A SHA-256 mismatch refuses the launch.
- **Earlier directories.** A halted or compromised directory is never modified, moved or renamed.
- **Each re-run's `manifest.json` identifies its valid predecessor explicitly:**
  - the directory it replaces, and that directory's halt or audit cause;
  - for stage 3, the stage-2 directory it pairs with.

  A replacement with changed telemetry setting cannot join the prior replication pair (T9).
- **Dashboard constraint.** No re-run name begins with `attempt` or `_quarantine`. The experiment tab treats such names as set-aside records (`tools/dashboard_experiment.py:182`). It takes the first two path parts of a log directory as the experiment's data directory (`:295–296`).
- **Scope.** This rule names directories only:
  - it does not lift a V4 schedule halt (`:189`);
  - it does not decide whether a halted stage may be re-run, or after what diagnosis. §5 (`:301`) and D-C10w-p2rerun govern that.

Nothing else changes: §2's design, the §2.6 budget rules and §2.10 guards, §2.12's records (beyond the two `run.json` keys of (T1) and the re-run provenance of (T12)), §3's tables and §5's halt conditions stand as frozen.

## 10. Amendment C — stage-1 calibration process (2026-10-08, pre-observation)

Written before any C10Y process has run. On 2026-10-08 there is no `results/c10y_directdw/` and no `results/c10y_directdw_calib*/`. The model-free build is in progress: `experiments/track_c/c10y_directdw_selftest.py` exists and no driver does yet. §0–§9 are unchanged. This section pre-registers the "separately budgeted work" that `:98` names and that no section defines. It changes no hypothesis, recipe, arm, objective, optimiser setting, stimulus, metric, threshold, gate, qualifier, label, table row, stage cap, budget rule, memory guard or telemetry rule, and it replaces no sentence above. Where it conflicts with the build brief, this section governs.

**Why it is needed (frozen text, quoted).**
- The pre-start gate: "an unmeasured component without a defensible bound makes the forecast UNVERIFIED and dispatch is refused" (`:92`).
- The B-e2e step cost is "unmeasured on this path" (`:171`), at an effective MPS rate "not measured for this path" (`:173`).
- "Obtaining missing calibration timings is separately budgeted work and cannot bypass LAW#3" (`:98`).
- "No new-path candidate hook forward, backward, optimiser iteration, closure arm or NM/ENV evaluation occurs before the baseline gate" (`:89`).
- Program ruling (build brief §10 Q4, `codex_c10y_build_brief.md:187`): calibration needs its own dated, reviewed amendment before any C10Y dispatch. It runs recipe A, then LAW#3, then the smoke test.

(C1) **What calibration is.**
- One model-bearing process. It runs stage 1's own frozen order (§2.6 item 5, `:89–90`) up to and including the candidate smoke, then stops:
  1. the fingerprint, the §2.6 item 1 refusals and the pristine-band SHA-256s (`:85`);
  2. sampling the context templates once in-process (`memit_main.py:304–323`), then the overlap audit (`:86`). A leak is INVALID-LEAKAGE and halts calibration (V12, `:197`);
  3. solving the pristine targets for A1, A2 and A7 with the engine's `compute_z` at layer 8, under the execution ledger (`:87`; V6 `:191`);
  4. untouched recipe A on A1, A2 and A7 in one `H.run_recipe` call, with its own projector and the standing LAW#5 gate (i) (`:90`, `:128`; `c10e_bandknob.py:462–463`);
  5. LAW#3 (V4, `:189`);
  6. checks (ii)–(viii) for e2e on A7 only, which is how stage 1 scopes them (`:127`, `:129–136`);
  7. the candidate smoke (ix): three B-e2e steps on A7 at the frozen nonzero lr. The state is discarded, the pristine band is restored and its hashes are verified (`:137`);
  8. writing the records, then exit.
- **Why (ii)–(viii) are included.** The program's ruling names "recipe A, then LAW#3, then the smoke test". The frozen smoke runs only "after LAW#3 and (ii)–(viii)" (`:137`), so leaving them out would change a frozen order. They are also stage-1 phases that the forecast must time (`:92`: "all baseline and inertness runs, repeated projectors/capture solves, parity checks, smoke").
- **Never run in calibration:**
  - a substantive candidate write;
  - any B-e2e, B-z, NM-total or ENV `run_recipe`;
  - any substantive candidate readout. Merged-model evaluations required by the frozen reduction and init-parity checks ((iii), (iii-b), (iv); `:130–132`) remain mandatory and yield no scientific candidate reading;
  - the (T8) telemetry check;
  - any stage-2 or stage-3 item.
- Calibration replaces nothing in stage 1. Stage 1 still runs its own recipe A, LAW#3, checks and smoke (`:89–90`).

(C2) **What it times and records.**
- **Timing method.**
  - Every step of (C1) is timed with MPS synchronisation at both ends (`:90`).
  - The timer is the stage clock, never the telemetry clock (T2, `:448`).
- **Separate timing entries:**
  - preflight;
  - model and tokenizer load;
  - context sampling with the overlap audit;
  - the target solve for each arm (24 `compute_z` calls each);
  - inside recipe A's `run_recipe`:
    - projector construction (`c10e:462`);
    - `run_law5` (`:463`);
    - for each arm, the write and the evaluation-plus-hooks, timed separately;
    - the rest of the call, recorded as recipe-level overhead;
  - the LAW#3 evaluation;
  - in (ii): each original `my_edit` call, and the capture solve;
  - (iii): its merge and its evaluation;
  - (iii-b): each of the three lr = 0 iterations separately, then the merge and the evaluation;
  - (iv) at init;
  - (v);
  - (vi), including the 12-request reference and both splits;
  - (vii);
  - (viii);
  - (ix): each of the three steps separately, then the restore and hash check;
  - shutdown: from the last record write to process exit, measured by the supervisor.
- **For each hooked iteration in (iii-b) and (ix)**, record:
  - whether it was accepted or an overflow retry;
  - the loss-scale halvings (`:70`).
- **Workload for each phase**, recorded:
  - the arms, requests, scored prompts, micro-batches, accepted steps and retries;
  - the real padded length of every A7 `L_edit` micro-batch (`:169`: "step 0 records the real padded length"). T_cal is the maximum of these;
  - the token length of each sampled context template.
- **Memory.** The §2.10 memory telemetry applies unchanged:
  - synchronised driver allocation, process RSS and host available memory, each recorded separately and never summed as a measurement;
  - peaks through every heavy phase (`:169`);
  - missing memory telemetry is a preflight failure (`:169`, `:419`);
  - the four memory guards halt calibration exactly as they halt a stage (`:169`, `:301`);
  - recorded peaks are observations only. They feed no stage gate and no forecast. The guards themselves remain in-run instrument/resource halts on calibration (see (C4)).
- **Repetitions.** One process. Inside it, every repeated unit is timed on its own:
  - the three recipe-A arms;
  - the two original `my_edit` calls of (ii), plus recipe A's own A7 write;
  - six hooked iterations of the same shape: three at lr = 0 in (iii-b) and three at the frozen lr in (ix).

  Calibration adds no candidate step beyond the three that the smoke freezes (`:137`).

(C3) **What the stage-1 pre-start forecast takes from calibration.**
- **Rule.** For each phase, cite comparable measured timings, workloads, repetitions and a justified scaling assumption or independently defensible upper estimate. Neither 99/69.53 nor T≈28 establishes an upper bound. Any component lacking such support makes the forecast UNVERIFIED and refuses dispatch (§2.6 item 6).
- No numeric safety factor is pre-registered here, because the frozen text justifies none. Where a measurement has repetitions, the forecast cites all of them, never the mean alone. In-run projections (`:98`) do not satisfy the pre-start requirement (`:92`).
- **Mapping.** For each stage-1 phase of the `:92` list, the comparable calibration measurement. The table names the source only; the forecast record supplies and justifies each phase's scaling assumption or upper estimate:

| stage-1 phase | comparable calibration measurement | count in stage 1 |
|---|---|---|
| preflight; load; contexts and overlap audit; target solves; recipe A (projector, LAW#5, three arms); LAW#3; checks (ii)–(viii) for e2e/A7; smoke (ix) | the same phase | 1 each. Stage 1 repeats all of them (`:89–90`) |
| overhead of the B-e2e `run_recipe` call: its own projector and LAW#5 gate (`:88`; `c10e:462–463`) | recipe A's recipe-level overhead: projector, plus `run_law5`, plus the rest | 1 |
| capture solve for the substantive write (`:47`) | the (ii) capture solve | 1 |
| optimisation over the full budget | the six timed hooked iterations, each with its padded length | 105 = T_max 100 accepted steps (`:63`) + 5 permitted overflow retries (V10, `:195`). The frozen text says "Do not assume early convergence" (`:92`) |
| merge | the larger of the (iii) and (iii-b) merges | 1 |
| readout, meaning all B-e2e A7 work after the merge | the sum of: recipe A's A7 evaluation-plus-hooks; (iv) and (v) as timed at init, because final-state checks are the same operations; the timed hooked iterations for the 24 × 6 fit matrix, which is a forward over the same rewriting batch (each iteration runs that forward plus a backward) | the reserve is at least 1,380 s, raised to the phase's supported upper estimate when that is larger (`:98`: "at least 23 minutes, increased when measured evidence requires it") |
| shutdown | as measured | 1 |

- **Dispatch rule.** Stage 1 is dispatched only if the summed forecast is at most 7,200 s; equality passes (`:94`). Above that, the outcome is HALTED-BUDGET with `launched=false` (`:94`, S2 `:211`).
- Any stage-1 phase with no row above, or whose row lacks a justified scaling assumption or a defensible upper estimate, is unsupported. The forecast is then UNVERIFIED and dispatch is refused (`:92`).
- **What the forecast record cites:**
  - the path and SHA-256 of `calibration.json`;
  - every calibration timing it uses, with its workload and repetition count;
  - for each phase, the scaling assumption or independent upper estimate with its justification. This includes the dependence on stage 1's own padded length, which is unknown before launch because stage 1 samples its own templates (`:86`, `:90`; T≈28 is an assumption, `:162`, `:169`).

(C4) **No scientific reading.**
- **Nothing scientific comes out of calibration.**
  - It produces no candidate-arm result, no screen record, no label and no verdict input.
  - The smoke state is discarded (`:137`). No substantive candidate readout; merged-model evaluations required by the frozen reduction and init-parity checks remain mandatory and yield no scientific candidate reading (`:130–132`).
  - Those checks' mandatory diagnostic outputs (their counts, distances, losses and parity records, `:129–137`) are still recorded in full; they are prescribed instrument checks, not candidate measurements (`:125`).
- **Where its records may go.**
  - Calibration supplies timing evidence only. Its records enter no stage gate except the stage-1 pre-start forecast, and only as timing artifacts (`:92`).
  - The exception is calibration's own instrument and resource halts: V4, the §2.8 checks, V7, V10, V12, the memory guards, float64 on MPS and drift halt calibration exactly as they would halt a stage (`:189`, `:301`). A V4 miss also halts the schedule (below).
  - Its recipe-A counts are not the stage-1 comparator a, which comes from the same process (`:206`).
  - Its contexts, targets, `R_l`, `B_l` and smoke losses are never stage inputs:
    - stage 1 samples its own contexts and solves its own targets (`:86–87`);
    - stages 2 and 3 take contexts only from a stage-1 directory (T12, `:679`).
  - The reader never reads a calibration directory, and the driver refuses a calibration path as a context-template source.
- **Held-out prompts** are used only by recipe A's prescribed evaluation and the frozen check readouts. They are never used for gradients, timing-smoke selection or stopping (`:86`).
- **The one effect the frozen text forces.** V4 applies as written: "Any miss HALTs the entire planned schedule, including future processes, before candidates" (`:189`).
  - A calibration LAW#3 miss writes the schedule-halt record, and every later stage launch refuses on it.
  - This is V4 applied to the process that ran it. It is not a calibration timing entering a stage gate. Reading it any other way would weaken V4.
- **Other halts.** Every other named §5 halt in calibration is a HALT with a diagnostic, under §5 and one-fix-then-halt (`:301`). These are:
  - checks (i)–(ix);
  - V7, including the precision-diagnosis halt;
  - V10;
  - V12;
  - the memory guards;
  - float64 on MPS;
  - source or input drift.
- **Overlap audit.** INVALID-LEAKAGE HALTs calibration. Do not redraw contexts until they pass; §2.6 item 2 and §5 remain binding (`:86`, `:197`, `:301`).

(C5) **Output directory and records.**
- **Directory.**
  - `results/c10y_directdw_calib<k>/`, with k = 1, 2, … in order, and logs in `<dir>/logs/`. The driver refuses an existing directory.
  - Calibration never writes `results/c10y_directdw/` or any `_s<s>_rerun<k>/` directory. Those stay reserved for stages (T12, `:674–676`).
  - A calibration directory is never modified, moved or renamed after its process ends (cf. `:680`).
  - The name begins with neither `attempt` nor `_quarantine` (`:686`).
- **Records.** No file is ever overwritten.
  - `calibration.json`, holding:
    - the timings, workloads, repetitions and memory of (C2);
    - `outcome`: COMPLETE, or the halt code;
    - the fingerprint output in full;
    - the source and input SHA-256s of §2.7 (`:115`);
    - `env`: python, machine, platform, torch and transformers versions, and `model_rev`;
    - this prereg's SHA-256;
    - T_cal and the per-template token lengths;
    - the start and finish times.
  - The §2.12 files that the frozen order produces up to (ix), with the suffix `calib`:
    - `context_templates_calib.json` (+ SHA-256);
    - `overlap_audit_calib.json`;
    - `targets_calib.pt` (+ SHA-256);
    - `ledger_calib.json`;
    - `law5_calib.json`, holding (i)–(iii-b) and V4;
    - `step0_calib.json`, holding (iv)–(ix);
    - `run.json`.
  - Calibration never writes `screen.json`, `pass_*.json` or `repro.json`.
- **HALT diagnostic.** The diagnostic path `architecture_profile/c10y_halt_diagnostic_<UTC>.json` is a required launch argument. An existing file is refused (brief §10 Q6, `:189`). The diagnostic records `"process": "calibration"` and the calibration directory.

(C6) **Cost, cap, authorisation, halts.**
- **Estimate (I-INFER, not a measured duration): about 61–64 GPU-minutes.** It is the sum of:
  - ≈ 34 min for untouched recipe A (`:174`);
  - ≈ 25 min of proofs and setup (`:174`);
  - six hooked iterations at 17–50 s each (`:173`), which is 2–5 min.

  Capture identities and repeated SVDs can add more (`:174`).
- **Cap.** C_cal = 7,200 s = C₁ (`:94`).
  - *Reason:* calibration is a strict prefix of the stage-1 process and does the same work. If the prefix cannot finish within C₁, stage 1 cannot fit C₁ either, so a larger calibration cap buys no feasible stage 1 under the currently frozen C₁ (a C₁ raise is the separate route below).
  - The spend record requires `0 < cap_s ≤ 7200`.
- **Enforcement.**
  - Calibration is not a stage, and it has no pre-start forecast of its own: it is the measurement that the forecast lacks.
  - It runs under the §2.6 item 6 independent supervisor, with C_cal as the deadline (`:96`):
    - the deadline starts before the worker launches;
    - enforcement holds through blocked calls;
    - the termination allowance sits inside the cap;
    - the model-free hanging-worker test passes before dispatch.
  - The memory guards apply unchanged.
- **Dispatch requires all of the following:**
  - (a) the decision-0 `--go` record. Execution under this prereg is gated on the recorded D-C10r-rulings-4 (3) reconsideration (`:3`), and calibration is model-bearing execution;
  - (b) a `--spend` record: `{"decision_id", "stage": "calibration", "cap_s"}`, with `0 < cap_s ≤ 7200` (brief §10 Q8 schema, `:191`);
  - (c) a recorded authorisation under D-C10r-rulings-14 (`EXPERIMENT_RUNBOOK.md:381`). That operator ruling gives the program standing authority to raise any experiment's budget, "including … the C10Y calibration spends", when measured evidence requires it. Its conditions: the raise is recorded with its arithmetic in runbook §5.2 and in a dated authorisation before the spend. Calibration is GPU spend outside C₁, which (T8)'s rule (`:615`) previously left to a recorded authorisation. The program authors both machine records and records the authorisation before dispatch. The authorisation names the cost (≈ 61–64 GPU-min, I-INFER, arithmetic above) and the cap (`0 < cap_s ≤ 7200`). The evidence requiring this spend is the absence of any measured stage-1 timing on this path (prereg :171–174, "unmeasured on this path"), which makes every forecast UNVERIFIED under :92; the 61–64-min figure is an inferred cost estimate, not that evidence. The measured GPU time is recorded afterwards.
  - One GPU job at a time (`:3`).
- **A calibration that halts is re-run, never read around.**
  - A halt for any cause yields no forecast input. Causes include a §5 halt, a memory guard and the supervisor deadline.
  - Its partial timings are never read into a forecast. No deviation note stands in for them (D-C10w-p2rerun, `EXPERIMENT_RUNBOOK.md:378`).
  - Except after a V4 miss, the remedy is a re-run in `calib<k+1>`, after the §5 diagnosis and under a new spend record.
  - A V4 miss keeps the entire schedule HALTED. No automatic rerun is permitted; any required rerun remains pending diagnosis and authorization resolving that halt. A new directory or spend record alone cannot lift it (`:189`; T12 scope, `:687–689`).
  - Incomplete calibration supplies no forecast inputs. Dispatch remains refused unless every required phase is supported by admissible measured timings or a defensible bound under §2.6 item 6 (`:92`).
- **Raising the stage-1 cap.** The post-calibration forecast for stage 1 may exceed C₁ = 7,200 s (`:94`). In that case, a stage-1 cap raise is a separate dated amendment, never part of this one. Its new cap is derived from the admissible per-phase bounds of (C3), with the arithmetic shown. It is Astra-reviewed and recorded under D-C10r-rulings-14 (`EXPERIMENT_RUNBOOK.md:381`) before dispatch. A cap chosen without that arithmetic is never used. Until such an amendment exists, the frozen outcome stands: HALTED-BUDGET with `launched=false` (`:94`). This paragraph sets no new cap and changes no frozen rule.
- **Staleness.** A forecast may cite a calibration only when all of these equal stage 1's at the pre-start gate:
  - its recorded source SHA-256s: driver, `c10e_bandknob.py`, hparams, `compute_z.py`, `compute_ks.py`, `rome/repr_tools.py`, `memit_main.py` and this prereg;
  - its fingerprint;
  - its `env`;
  - its device.

  Any difference makes the calibration unusable and the forecast UNVERIFIED. This is how (T8) treats its own record (`:609`).

(C7) **Telemetry.**
- Live telemetry is off. The first-attempt rule (T9, `:618`) applies to calibration.
- The launch line removes both variables: `env -u C10Y_TELEMETRY -u C10Y_TELEMETRY_INERTNESS …` (T1, `:436`). A set variable is refused before any write.
- `run.json` carries `"telemetry": false` and `"telemetry_inertness": null` (`:430–432`).
- The §2.10 memory telemetry stays required (`:419`).
- Calibration timings therefore bound only a telemetry-off stage forecast. A telemetry-on forecast also needs the (T10) telemetry phase from a (T8) record (`:628–634`), which calibration does not supply.

(C8) **Build and review.**
- Calibration is a driver entry point that runs the stage-1 code path and stops after (ix).
- It is built test-first and model-free, under the build brief's isolation rules. The tests show that:
  - no candidate hook forward, backward or iteration precedes V4 (spies);
  - the process stops after (ix), with no substantive write, no candidate `run_recipe` and no substantive candidate readout, while the mandatory (iii), (iii-b) and (iv) merged-model evaluations still run and are recorded;
  - an existing directory and the telemetry variables are refused;
  - the forecast builder:
    - refuses any phase that lacks a cited measured timing, workload, repetition count and justified scaling assumption or defensible upper estimate (UNVERIFIED);
    - refuses a stale calibration, and takes no input from an incomplete one;
    - passes exactly 7,200 s and refuses 7,200.001 s.
- It is reviewed with the build (advisor + GPT-6-Astra high) before dispatch.

Nothing else changes. These all stand as frozen and amended:
- §2's design;
- the §2.6 budget rules, including stage 1's own in-run projections and smoke;
- the §2.10 guards;
- §2.12's records;
- §3's tables;
- §5's halt conditions;
- §9.
