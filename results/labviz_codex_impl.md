# Lab View implementation report

Model: Codex, based on GPT-6. The exact deployment variant and configured reasoning-effort value are not exposed in this session; neither is inferred.

Report generated: 2026-10-08T02:30:22.097487+00:00. Scope: the complete `results/labviz_codex_brief.md`, including the binding **Full history** and **Every model tested** additions, re-read after the addendum and before closeout.

## Result and evidence boundary

The local notebook is built at `results/labviz/site/index.html`. It contains **1,369 observation/documentary cards**, **56 numbered CORPUS entries**, **14 scoreboard rows**, and **3 earlier model-branch decision cards**. Every card has its own saved SVG and PNG. `73` results folders/groups are surveyed, including empty and metadata-only directories. There are `11` cited model panels, with tested, inspected, configured, and planned statuses distinguished. The model-name survey also preserves `56` literal spellings/aliases and their source lines.

The displayed records span `2026-06-15` through `2026-10-08`. These are the recorded/header/filename/log-modification dates explicitly labelled on the cards. UTC log dates may fall on the next calendar day relative to the operator's local timezone. Undated historical observations stay undated. Earlier branch cards use decision-document closeout dates, with a warning that their actual run dates can be earlier.

Static build, image, HTML/link, syntax, source-bound parsing, missing-field, and CSS checks **PASS**. Real Safari/Chrome layout, WebGL interaction, CDN failure behavior in a browser, server bind, LAN delivery, and Tailscale delivery are **UNVERIFIED** because this managed sandbox rejects socket binding and the Chromium launch. This report makes no new experiment verdict, model-performance claim, or F1 closure.

Cards count observations, not independent experiments. An arm, a JSON snapshot, a repeated log line, a diagnostic read, and a documentary summary can describe overlapping evidence. The interface labels their schemas and source fields.

## Implementation and files

The builder reads JSON/log evidence, numbered CORPUS headers, the scoreboard, referenced hparams, and small documented model metadata. It never imports or executes experiment/engine code, constructs a model/tokenizer, imports torch, opens tensor/adapter weight files, or uses a GPU. The server exposes the generated site and explicit evidence copies, rather than the workspace tree. There is no browser write API.

The seven tabs are Now, Runs, 3D model, Models, History, Learn, and Evaluations. The frontend uses plain HTML/CSS/JS. Optional three.js and OrbitControls are pinned to `https://cdn.jsdelivr.net/npm/three@0.160.0/`; the local 2D tower remains available when that enhancement fails. Matplotlib renders saved evidence images without interpolating observations. Training and probability plots contain recorded points only.

Stable card IDs hash the relative source path and source field. Unchanged records and renderer code reuse images; unchanged HTML/assets are not rewritten. A synthetic build-twice test verifies byte stability. Source files and logs are changing in the separate program session, so two builds against that live workspace need not have identical bytes. Saved evidence files identify what the final site contains.

The brief specifically requires creating `docs/c10_evaluations.json`; I treated that as its named exception to the general output-directory rule. It currently contains `14` entries, derived exclusively from scoreboard `results`. The task-created seed was refreshed after the program appended a scoreboard result, after confirming it was still byte-equivalent in content to the unmodified seed. Subsequent builder runs preserve that file, including operator edits. The builder does not automatically invent or append evaluations for future scoreboard rows; the program session maintains them.

Package and launcher files created, with final SHA-256:

| File | SHA-256 |
| --- | --- |
| tools/labviz/README.md | c3678b283cd7530c3430b7c3c2992171b45fa05fe00ce075e1837698aee7d787 |
| tools/labviz/__init__.py | f5fa7fb3f638706cde4a96e87807864e73a07dc23519b26e31b4a7c5c5877d51 |
| tools/labviz/app.js | 092b11387f3652ddd7d95b1d8797cc8d2208dbde523651d18bfe6223ea5a71cc |
| tools/labviz/build.py | 57018f2d3709713ba59e0c2923f0f79c8850c27e01a2cf57ad0c029bd228d229 |
| tools/labviz/index.html | 9ba45b81528e7262649b2535907ba7b4e39aa4814eb4ccca03e0941ce7ef4385 |
| tools/labviz/model.js | e7d1e9e8ffd352eaf7a64955d7632cace70178285fbeffee1114b1af3bc7fd4d |
| tools/labviz/models.json | 3f1007412b9df3de941d243ade4a9782c7ea2ab68e19aea0d547821a05b1aa13 |
| tools/labviz/render.py | d9e0109077e070c3050fd28acf1430112ce2e1e105e925e613bc02069c3668ea |
| tools/labviz/style.css | ea44acf1dd9d91e546e6c4b136f7ec9ddf07448d3d12780a3831cc66909ac032 |
| tools/labviz/test_labviz.py | f65f0b72d5e6f49856b82fb32a5a02fbe2f1f68d5d5c02182a569d97cd5d92d5 |
| tools/labviz/test_plan.md | 7662441f5055118f91778b38b92f06965f7d1147e39ff2c2a9f5611b6a584abe |
| tools/labviz_serve.sh | c90afb9ce1bd8c3b54af95f4534f055404587a0105045e931ee34d6cb9a05a4b |
| docs/c10_evaluations.json | f1d98d60f52437ee003d03c601dec7ec6a46554fdd00085700ab21b1d51bbee9 |


Generated deliverables include `site/index.html`, `site/data.js`, `site/style.css`, `site/app.js`, `site/model.js`, `site/history.svg`, explicit source snapshots under `site/evidence/`, per-card `runs/<id>.svg` and `runs/<id>.png`, `survey.json`, `models.json`, `images_manifest.json`, `model_mentions.json`, `test_output.txt`, and `verification.{json,txt}`. `site/runs` is a relative symlink to `../runs`.

The complete machine-checkable SHA-256 list for the package, evaluations, report, generated pictures, and evidence snapshots is `results/labviz/files_sha256.txt`. It excludes its own checksum and the regenerable ignored Matplotlib font cache. It also includes the modified `.gitignore` hash. No Git commit or staging was performed. SVG and PNG evidence images are trackable; `.gitignore` ignores the regenerated site and font cache and explicitly permits the PNGs despite the repository's global PNG ignore rule.

Only task-owned outputs and the authorised `.gitignore` addition were written. The tracked-file baseline comparison found concurrent changes in other program files; these are listed in `verification.json`. They were not written or reverted by this task. The fixture test independently proves that the builder leaves its input record unchanged. No canonical experiment/result/ledger/preregistration was repaired or rewritten.

## Source survey and schema support

Every eligible JSON/log/JSONL/CSV/TSV source under every results folder is surveyed. Tokenizer directories and tensor/binary files are excluded. JSONL, CSV, and TSV are inventoried without interpreting their unknown schemas. Documents without numerical run detail appear through the CORPUS/scoreboard/historical-model cards. Unknown schemas remain in the explicit unsupported list below.

The following supported forms each have real-record regression coverage as well as small synthetic checks where appropriate:

| Schema/form | Real source(s) | Recorded semantics |
| --- | --- | --- |
| Harness arms + detail | results/c10_multitoken_value.json; results/c10e_bandknob.json | Actual counts, percentages, and Boolean template answers; recipe arms remain separate. |
| Mint envelope and recipes | results/c10u_mint2/r3/F_r0_mint1_s2.json | Binding count takes precedence; primary arm and its matching write-size record are retained. |
| Reader probabilities | results/c10u_mint2/r3_read_after_v2.json | Per-position saved probabilities; no probability is manufactured from hit counts. |
| Training JSON | results/c10w_oracle/*/train/*.json | Actual step/loss pairs and recorded metadata; no adapter weights are opened. |
| Harness/training logs | results/c10u_mint2/**/logs/behavior_*.log; results/c10w_oracle/*/*.log | Canonical/reworded counts, L1/L3 denominators, writing difficulty, training steps; each observation cites its line. |
| Legacy fact tables | results/g6_scale_n_batch_result.json; results/c1_kvc_grid_result.json | All saved Boolean outcomes are tallied, original fields retained; no forced conversion to a 72-question test. |
| Numeric arms | results/a2b_refresh_ks_result.json; results/c10s_solvefeas/inject.json | Original numeric field names/units; percentages are not reconstructed as counts. |
| Numeric run arrays | results/b1_7b_dose_response_result.json | Each recorded per-run/cell/rung entry receives a card. |
| Older raw arms and indexed depth tables | results/c2band_compare_result.json; results/c2b_depth_map_result.json; results/c2_result.json | Raw arm fields and numeric-indexed tables; no fabricated C10 score. |
| Older detail/secret/trajectory tables | results/r1_select_readback.json; results/r1_commit_bit_select.json; results/r9_deletion_residue.json; results/d1_concentration_sweep_result.json | Recorded fact-group tables, Boolean outcomes, and trajectory fields with original labels. |
| Documentary records | CORPUS/[0-9][0-9]_*.md; docs/c10_scoreboard.json; docs/t_branch_decision_document_v1_4.md | Verbatim verdict/limit text or explicit missing verdict; references, source-bound model tags and dates. |


Generic older tables show the first 16 numeric fields, with original names and units, and totals of every saved top-level Boolean fact outcome. Their complete data remains available through the source link. They do not receive a guessed `/72` denominator or C10 success interpretation. Numeric-indexed maps are kept as recorded tables rather than treating every nested field as a separate experiment.

The 24 × 3 grids use saved Boolean template answers when available. Mint diagnostic grids with supplied earlier answer pieces are explicitly labelled **teacher-forced hits**; they are not free-generation answers. Missing grid cells are grey. Missing confidence, losses, counts, side effects, layer counts, edited bands, and write sizes explicitly say `not recorded for this run` or the matching model-metadata missing label. Actual /12 and /30 checks retain their recorded denominators. A norm is defined as a single length measuring a numerical change, and relative versus absolute write sizes remain distinct.

Final schema/card counts:

| Schema | Cards |
| --- | --- |
| CORPUS verdict | 56 |
| harness | 280 |
| historical model note | 3 |
| log observation | 141 |
| numeric-arm | 76 |
| numeric-run | 196 |
| reader | 34 |
| recorded-table | 554 |
| scoreboard summary | 14 |
| training | 10 |
| training-log | 5 |


Every surveyed folder/group is listed below. **Files and cards in a parent folder include its descendants; these rows must not be summed.** Unsupported/unreadable counts are the exceptions recorded directly in that group; the unique full lists follow. A zero means no eligible numerical/log observation was parsed there, rather than proof that an experiment never happened. Flat older `c2`, `a1`-related, governance, scale, and deployment files are covered by the flat-files row even when no identically named folder exists.

| Folder/group | Eligible files | Cards | Logs | Unsupported | Unreadable |
| --- | --- | --- | --- | --- | --- |
| results (flat files) | 104 | 454 | 3 | 35 | 0 |
| results/autoresearch_c10_equivalence_run | 2 | 3 | 0 | 1 | 0 |
| results/autoresearch_reaim | 4 | 10 | 1 | 2 | 0 |
| results/autoresearch_reaim/reaim-oct06 | 4 | 10 | 1 | 0 | 0 |
| results/autoresearch_reaim/reaim-oct06/iter_01 | 4 | 10 | 1 | 0 | 0 |
| results/c10k_keying_ablation | 23 | 45 | 0 | 2 | 0 |
| results/c10k_keying_ablation/n1 | 14 | 26 | 0 | 0 | 0 |
| results/c10k_route_a | 21 | 74 | 0 | 0 | 0 |
| results/c10l_covgeom | 25 | 118 | 11 | 0 | 0 |
| results/c10l_covgeom/logs | 0 | 0 | 0 | 0 | 0 |
| results/c10l_mint | 34 | 62 | 19 | 1 | 0 |
| results/c10l_mint/inits | 0 | 0 | 0 | 0 | 0 |
| results/c10l_mint/tokenizer_minted | 0 | 0 | 0 | 0 | 0 |
| results/c10m_diag | 5 | 14 | 3 | 0 | 0 |
| results/c10n_ztransport | 5 | 11 | 3 | 0 | 0 |
| results/c10o_magnitude | 3 | 11 | 2 | 0 | 0 |
| results/c10p_twopass | 6 | 29 | 2 | 0 | 0 |
| results/c10q_stacked | 8 | 38 | 3 | 0 | 0 |
| results/c10q_stacked/run1_crashed | 2 | 9 | 1 | 0 | 0 |
| results/c10s_sharedz | 1 | 1 | 0 | 0 | 0 |
| results/c10s_sharedz_logs | 6 | 0 | 6 | 0 | 0 |
| results/c10s_sharedz_r2 | 3 | 4 | 0 | 0 | 0 |
| results/c10s_solvefeas | 3 | 4 | 0 | 0 | 0 |
| results/c10s_solvefeas_logs | 2 | 0 | 2 | 0 | 0 |
| results/c10t_secondkey | 2 | 6 | 0 | 0 | 0 |
| results/c10t_secondkey_logs | 4 | 7 | 4 | 0 | 0 |
| results/c10t_secondkey_r2 | 3 | 20 | 0 | 0 | 0 |
| results/c10u_mint2 | 171 | 310 | 53 | 62 | 0 |
| results/c10u_mint2/inits | 0 | 0 | 0 | 0 | 0 |
| results/c10u_mint2/logs | 8 | 8 | 8 | 0 | 0 |
| results/c10u_mint2/r2 | 33 | 52 | 10 | 0 | 0 |
| results/c10u_mint2/r2/inits | 0 | 0 | 0 | 0 | 0 |
| results/c10u_mint2/r2/logs | 10 | 8 | 10 | 0 | 0 |
| results/c10u_mint2/r2/step0 | 8 | 20 | 0 | 0 | 0 |
| results/c10u_mint2/r2/zs | 0 | 0 | 0 | 0 | 0 |
| results/c10u_mint2/r3 | 106 | 190 | 35 | 0 | 0 |
| results/c10u_mint2/r3/inits | 0 | 0 | 0 | 0 | 0 |
| results/c10u_mint2/r3/logs | 35 | 26 | 35 | 0 | 0 |
| results/c10u_mint2/r3/step0 | 24 | 60 | 0 | 0 | 0 |
| results/c10u_mint2/r3/zs | 0 | 0 | 0 | 0 | 0 |
| results/c10u_mint2/step0 | 6 | 15 | 0 | 0 | 0 |
| results/c10u_mint2/zs | 0 | 0 | 0 | 0 | 0 |
| results/c10u_mint2_logs | 10 | 1 | 9 | 0 | 0 |
| results/c10u_mint2_logs/r2 | 2 | 0 | 2 | 0 | 0 |
| results/c10u_mint2_logs/r3 | 5 | 0 | 5 | 0 | 0 |
| results/c10v_layerpick | 1 | 0 | 0 | 1 | 0 |
| results/c10v_layerpick_logs | 1 | 0 | 1 | 0 | 0 |
| results/c10w_oracle | 28 | 67 | 9 | 6 | 0 |
| results/c10w_oracle/p1_20261007T223707_598959Z | 19 | 61 | 7 | 0 | 0 |
| results/c10w_oracle/p1_20261007T223707_598959Z/adapters | 0 | 0 | 0 | 0 | 0 |
| results/c10w_oracle/p1_20261007T223707_598959Z/train | 5 | 5 | 0 | 0 | 0 |
| results/c10w_oracle/step0_20261007T220253_584752Z | 4 | 2 | 1 | 0 | 0 |
| results/c10w_oracle/step0_20261007T223638_531381Z | 5 | 4 | 1 | 0 | 0 |
| results/c10w_oracle_logs | 10 | 0 | 10 | 0 | 0 |
| results/c10w_oracle_reviews | 0 | 0 | 0 | 0 | 0 |
| results/infranodus_audit_2026-10-04 | 1 | 0 | 0 | 1 | 0 |
| results/infranodus_audit_2026-10-04/segments | 0 | 0 | 0 | 0 | 0 |
| results/infranodus_research_arc_2026-10-05 | 16 | 0 | 0 | 16 | 0 |
| results/infranodus_research_arc_2026-10-05/fulltext | 1 | 0 | 0 | 0 | 0 |
| results/infranodus_research_arc_2026-10-05/operator_chat_inbox | 13 | 0 | 0 | 0 | 0 |
| results/infranodus_research_arc_2026-10-05/operator_chat_inbox/round3_20261005 | 13 | 0 | 0 | 0 | 0 |
| results/infranodus_research_arc_2026-10-05/part2 | 1 | 0 | 0 | 0 | 0 |
| results/infranodus_research_arc_2026-10-05/segments | 0 | 0 | 0 | 0 | 0 |
| results/law3_repro_2026-10-03 | 9 | 7 | 0 | 3 | 0 |
| results/law3_repro_2026-10-03/b3 | 5 | 3 | 0 | 0 | 0 |
| results/openresearch_archive | 17 | 0 | 0 | 17 | 0 |
| results/openresearch_archive/native | 14 | 0 | 0 | 0 | 0 |
| results/research_pass_2026-10-06 | 25 | 0 | 0 | 25 | 0 |
| results/research_pass_2026-10-06/council | 0 | 0 | 0 | 0 | 0 |
| results/research_pass_2026-10-06/helper_reports | 0 | 0 | 0 | 0 | 0 |
| results/research_pass_2026-10-06/instrument_logs | 25 | 0 | 0 | 0 | 0 |
| results/research_pass_2026-10-06/instrument_logs/browser_raw | 3 | 0 | 0 | 0 | 0 |
| results/research_pass_2026-10-06/instrument_logs/orx_raw | 15 | 0 | 0 | 0 | 0 |


There are `172` unique unsupported sources and `0` unreadable sources in the final survey. Metadata/seals, literature-search records, statistics-only summaries, and unrecognised governance/ledger schemas are not converted into numerical run pictures. Their applicable numbered evidence summaries remain in History/Evaluations.

All unsupported sources, including their root keys or reason:

| Source | Keys/reason |
| --- | --- |
| results/autoresearch_c10_equivalence.json | started, projectors_equal, recipe, scorer_exit, scorer_tail, scorer_vs_run_recipe, templates_sha_this_process, templates_sha_scorer, law5_harness, seed_reproduces_templates, saved_sha256, source_sha256, verdict |
| results/autoresearch_c10_equivalence_2026-10-06T0815.json | started, projectors_equal, recipe, scorer_exit, scorer_tail, scorer_vs_run_recipe, templates_sha_this_process, templates_sha_scorer, law5_harness, seed_reproduces_templates, saved_sha256, source_sha256, verdict |
| results/autoresearch_c10_equivalence_run/edits.json | commit, edit_seconds, setup_seconds, changed |
| results/autoresearch_reaim/reaim-oct06/iter_01/hparams.json | layers, clamp_norm_factor, layer_selection, fact_token, v_num_grad_steps, v_lr, v_loss_layer, v_weight_decay, kl_factor, mom2_adjustment, mom2_update_weight, rewrite_module_tmp, layer_module_tmp, mlp_module_tmp, attn_module_tmp, ln_f_module, lm_head_module, mom2_dataset |
| results/autoresearch_reaim/reaim-oct06/iter_01/knobs.json | resolve_rounds, stack, write_cap, z_blend, layers, ridge, resolve_steps |
| results/b1_7b_size_density_result.json | experiment, date, model, band, N, write_mode, seed, inertness, write_side, PRIMARY_cross_entity, PRIMARY_VERDICT, SECONDARY_size_density, caveats, artifacts |
| results/b3_margin_result.json | edited_top1_margin, native_country_top1_margin, interpretation |
| results/b3_quant_survival_result.json | hf_vs_gguf_f16_agreement, edited_retention, native_country_retention, native_global_retention, delta_edited_minus_native, verdict, threshold |
| results/c10i_anyedit_parity_trace_local.json | decision_id, class, scope, source_result, model_id, model_revision, upstream_anyedit, case, windows, required_next_trace_fields_before_any_A7, licensed_claim |
| results/c10i_anyedit_parity_trace_local_A2.json | decision_id, class, scope, source_result, model_id, model_revision, upstream_anyedit, case, windows, required_next_trace_fields_before_any_A7, licensed_claim |
| results/c10k_keying_ablation/K2_firstpass_parity_halt.json | decision_id, prereg, run, class, scope, stimulus, base_report, recipes, verdict |
| results/c10k_keying_ablation/dryrun_keyed_token.json | templates, subjects, n_templates, valid, bad |
| results/c10l_mint/p4_verdict.json | tokenisation, hf_vs_gguf_f16_parity, hf_vs_gguf_q4km_parity, correct, signatures, L1_flipped_to_minted, q4km_retention_of_f16_correct, gates, reading |
| results/c10t_secondkey_r2_selection_compare.json | published, rerun, compared_keys, differs, identical, allowed_to_differ, request_sha256, facts_second_level |
| results/c10u_mint2/F_r0_mint1_s0_started.json | identity, pid, block, replicate, kind, seed |
| results/c10u_mint2/F_r0_mint1_s1_started.json | identity, pid, block, replicate, kind, seed |
| results/c10u_mint2/F_r0_mint1_s2_started.json | identity, pid, block, replicate, kind, seed |
| results/c10u_mint2/F_r0_multi_snone_started.json | identity, pid, block, replicate, kind, seed |
| results/c10u_mint2/contexts_F.json | decision_id, block, identity, pid, kind, fingerprint, ctx, ctx_sha256, provenance, tokenizer_untouched, spare_rows_untouched, spare_rows_sha256, tokenizer_vocab_sha256 |
| results/c10u_mint2/contexts_F_started.json | identity, pid, block, when_utc |
| results/c10u_mint2/frozen_started.json | identity, stage, fingerprint, plan, when_utc |
| results/c10u_mint2/identity.json | run_id, created_utc, source_sha256, source_digest, law3_reference |
| results/c10u_mint2/r2/F_r0_mint1_s0_started.json | identity, pid, block, replicate, kind, seed |
| results/c10u_mint2/r2/F_r0_mint1_s1_started.json | identity, pid, block, replicate, kind, seed |
| results/c10u_mint2/r2/F_r0_mint1_s2_started.json | identity, pid, block, replicate, kind, seed |
| results/c10u_mint2/r2/F_r0_multi_snone_started.json | identity, pid, block, replicate, kind, seed |
| results/c10u_mint2/r2/contexts_F.json | decision_id, block, identity, pid, kind, fingerprint, ctx, ctx_sha256, provenance, tokenizer_untouched, spare_rows_untouched, spare_rows_sha256, tokenizer_vocab_sha256 |
| results/c10u_mint2/r2/contexts_F_started.json | identity, pid, block, when_utc |
| results/c10u_mint2/r2/frozen_started.json | identity, stage, fingerprint, plan, when_utc |
| results/c10u_mint2/r2/identity.json | run_id, created_utc, source_sha256, source_digest, law3_reference |
| results/c10u_mint2/r2/reproduce_complete.json | identity, stage, readings, when_utc |
| results/c10u_mint2/r2/reproduce_started.json | identity, stage, fingerprint, plan, when_utc |
| results/c10u_mint2/r2/step0/F_r0_mint1_s0_started.json | identity, pid, block, kind, seed |
| results/c10u_mint2/r2/step0/F_r0_mint1_s1_started.json | identity, pid, block, kind, seed |
| results/c10u_mint2/r2/step0/F_r0_mint1_s2_started.json | identity, pid, block, kind, seed |
| results/c10u_mint2/r2/step0/F_r0_modifier_s0_started.json | identity, pid, block, kind, seed |
| results/c10u_mint2/r3/F_r0_mint1_s0_started.json | identity, pid, block, replicate, kind, seed |
| results/c10u_mint2/r3/F_r0_mint1_s1_started.json | identity, pid, block, replicate, kind, seed |
| results/c10u_mint2/r3/F_r0_mint1_s2_started.json | identity, pid, block, replicate, kind, seed |
| results/c10u_mint2/r3/F_r0_multi_snone_started.json | identity, pid, block, replicate, kind, seed |
| results/c10u_mint2/r3/F_r1_mint1_s0_started.json | identity, pid, block, replicate, kind, seed |
| results/c10u_mint2/r3/F_r1_mint1_s1_started.json | identity, pid, block, replicate, kind, seed |
| results/c10u_mint2/r3/F_r1_mint1_s2_started.json | identity, pid, block, replicate, kind, seed |
| results/c10u_mint2/r3/F_r1_multi_snone_started.json | identity, pid, block, replicate, kind, seed |
| results/c10u_mint2/r3/V2_r0_mint1_s0_started.json | identity, pid, block, replicate, kind, seed |
| results/c10u_mint2/r3/V2_r0_mint1_s1_started.json | identity, pid, block, replicate, kind, seed |
| results/c10u_mint2/r3/V2_r0_mint1_s2_started.json | identity, pid, block, replicate, kind, seed |
| results/c10u_mint2/r3/V2_r0_mint2_s0_started.json | identity, pid, block, replicate, kind, seed |
| results/c10u_mint2/r3/V2_r0_multi_snone_started.json | identity, pid, block, replicate, kind, seed |
| results/c10u_mint2/r3/contexts_F.json | decision_id, block, identity, pid, kind, fingerprint, ctx, ctx_sha256, provenance, tokenizer_untouched, spare_rows_untouched, spare_rows_sha256, tokenizer_vocab_sha256 |
| results/c10u_mint2/r3/contexts_F_started.json | identity, pid, block, when_utc |
| results/c10u_mint2/r3/contexts_V2.json | decision_id, block, identity, pid, kind, fingerprint, ctx, ctx_sha256, provenance, tokenizer_untouched, spare_rows_untouched, spare_rows_sha256, tokenizer_vocab_sha256 |
| results/c10u_mint2/r3/contexts_V2_started.json | identity, pid, block, when_utc |
| results/c10u_mint2/r3/frozen_started.json | identity, stage, fingerprint, plan, when_utc |
| results/c10u_mint2/r3/identity.json | run_id, created_utc, source_sha256, source_digest, law3_reference |
| results/c10u_mint2/r3/replicate-F_started.json | identity, stage, fingerprint, plan, when_utc |
| results/c10u_mint2/r3/reproduce_complete.json | identity, stage, readings, when_utc |
| results/c10u_mint2/r3/reproduce_started.json | identity, stage, fingerprint, plan, when_utc |
| results/c10u_mint2/r3/step0/F_r0_mint1_s0_started.json | identity, pid, block, kind, seed |
| results/c10u_mint2/r3/step0/F_r0_mint1_s1_started.json | identity, pid, block, kind, seed |
| results/c10u_mint2/r3/step0/F_r0_mint1_s2_started.json | identity, pid, block, kind, seed |
| results/c10u_mint2/r3/step0/F_r0_modifier_s0_started.json | identity, pid, block, kind, seed |
| results/c10u_mint2/r3/step0/F_r0_modifier_s1_started.json | identity, pid, block, kind, seed |
| results/c10u_mint2/r3/step0/F_r0_modifier_s2_started.json | identity, pid, block, kind, seed |
| results/c10u_mint2/r3/step0/V2_r0_mint1_s0_started.json | identity, pid, block, kind, seed |
| results/c10u_mint2/r3/step0/V2_r0_mint1_s1_started.json | identity, pid, block, kind, seed |
| results/c10u_mint2/r3/step0/V2_r0_mint1_s2_started.json | identity, pid, block, kind, seed |
| results/c10u_mint2/r3/step0/V2_r0_mint2_s0_started.json | identity, pid, block, kind, seed |
| results/c10u_mint2/r3/step0/V2_r0_mint2_s1_started.json | identity, pid, block, kind, seed |
| results/c10u_mint2/r3/step0/V2_r0_mint2_s2_started.json | identity, pid, block, kind, seed |
| results/c10u_mint2/r3/v2_started.json | identity, stage, fingerprint, plan, when_utc |
| results/c10u_mint2/reproduce_complete.json | identity, stage, readings, when_utc |
| results/c10u_mint2/reproduce_started.json | identity, stage, fingerprint, plan, when_utc |
| results/c10u_mint2/step0/F_r0_mint1_s0_started.json | identity, pid, block, kind, seed |
| results/c10u_mint2/step0/F_r0_mint1_s1_started.json | identity, pid, block, kind, seed |
| results/c10u_mint2/step0/F_r0_mint1_s2_started.json | identity, pid, block, kind, seed |
| results/c10v_layerpick/identity.json | run_id, created_utc, source_sha256, source_digest, preflight_controls_reference |
| results/c10w_oracle/p1_20261007T223707_598959Z/authorization_P1.json | P1 |
| results/c10w_oracle/p1_20261007T223707_598959Z/interim_reader_configuration.json | reader_sha256, oracle_p1_A7_configuration, shuf_cross_score_vs_original_map, shuf_own_map_para_full_n |
| results/c10w_oracle/p1_20261007T223707_598959Z/interim_reader_configuration_v2.json | class, decision_id, status, producer, reader, p1_eval, oracle_p1_A7_configuration, shuf_cross_score_vs_original_map, shuf_own_map_para_full_n |
| results/c10w_oracle/p1_20261007T223707_598959Z/verdict.json | class, decision_id, status, final_label, routing, ranks, p3_required, canon_split, reference_count, reference_status, c10_status, f1_changed, g6_sensitivity, projection, stop |
| results/c10w_oracle/step0_20261007T220253_584752Z/HALT.json | status, stage, reason, oracle_measurement_not_route, class, decision_id |
| results/c10w_oracle/step0_20261007T223638_531381Z/mmlu200.json | dataset, config, revision, split_counts, source_identities, source_files, sample_seed, sampled_indices, dev_less_than_five_distinct, answer_mapping, token_checks, items, class, decision_id |
| results/c1_kvc_stats.json | experiment, source, cluster_unit, IDENTIFICATION_NOTE, grid, anchor_gates, single_factor_ONLY_refuted_by_equal_level, monotone_count_law_also_fails, interaction_diff_in_diff, corruption_real_vs_clean, control_dissociation, caveats |
| results/c1_scale_city_country_pool.json | list |
| results/c1_scale_city_country_screen.json | model, template, conf_floor, n_candidates, n_native_correct, n_pass_correct_and_confident, distinct_pass_countries, top_countries_by_pass_count, core_pool_conf>=0.8, achievable_high_concentration_N_single_relation, passed_sample |
| results/c1_truescale_N2000_diag.json | prereg, model, band, N_edit, N_heldout, single_joint_solve, orderings, cost_anchor, edit_expression_pct, heldout_baseline_correct_pct, heldout_post_correct_pct, heldout_retention_pct_of_pre_correct, n_pre_correct, bystander_flips_n, CORE, INERT_law5_delta, flips_sample |
| results/c1_truescale_pilot.json | prereg, model, band, N_edit, N_heldout, single_joint_solve, orderings, cost_anchor, edit_expression_pct, heldout_baseline_correct_pct, heldout_post_correct_pct, heldout_retention_pct_of_pre_correct, n_pre_correct, bystander_flips_n, CORE, INERT_law5_delta, flips_sample |
| results/c1_truescale_substrate_diagnostic.json | class, question, screen, subject_token_census, runs, wall_1, wall_2, cost_anchor, conclusion, advisor |
| results/c6_ledger_immutability_redteam.json | experiment, decision_id, class, honesty_note, ts, checks, verdict_summary, verdict, scope_caveats |
| results/c6_redteam_ledger.jsonl | .jsonl table not interpreted |
| results/connected_papers_index_2026-10-04.json | seeds, papers |
| results/cp1_result.json | T_POS, T_DET, T_GATE, T_ATOM, LEDGER_CHAIN, VERDICT, scope_and_caveats |
| results/cp1_state_ledger.jsonl | .jsonl table not interpreted |
| results/d1_instrument_variance_diagnostic_3b_det.json | experiment, model, hf_id, revision, tag, deterministic, cublas, attn, seed, k_unstable, pick_grid, pick_scan, n_repeat, heldout_n, total_n, band, engine, base_no_edit |
| results/d1_instrument_variance_diagnostic_3b_nondet.json | experiment, model, hf_id, revision, tag, deterministic, cublas, attn, seed, k_unstable, pick_grid, pick_scan, n_repeat, heldout_n, total_n, band, engine, base_no_edit |
| results/e1_larql_serve_result.json | experiment, date, store, framing, Claim_A_VERDICT, Claim_A_evidence, Claim_B_VERDICT, Claim_B_evidence, E1_NET, artifacts, caveats, adversarial_deconfounding_2026-06-18, A7_bias_ablation_causal_test |
| results/f1_pool_sizing.jsonl | .jsonl table not interpreted |
| results/g1_result.json | T_HAPPY, T_D46_GITFAIL, T_COMP_STRUCT, T_COMP_L4, T_ROLLBACK_DUAL, T_DIVERGE, T_PARK_NOT_DIVERGE, T_CIRCUIT, T_TPC4, T_LEDGER, VERDICT, scope_and_caveats |
| results/g1_state_ledger.jsonl | .jsonl table not interpreted |
| results/g2_result.json | T_NO_PRIVKEY, T_TOKEN_CHECKS, T_OVERLAY_SIGFORGE, T_CEREMONY_WRONGKEY, T_CEREMONY, T_LEDGER_TAMPER, T_BLAST_CAP, T_SUSPEND, T_BOOT_ANCHOR, VERDICT, scope_and_caveats |
| results/g2_state_ledger.jsonl | .jsonl table not interpreted |
| results/g3_result.json | T_SCHEMA, T_INDEPENDENCE, T_CASCADE, T_CODE_PASS_PATCH_FAIL, T_INJECTION, T_STORAGE_PROBE, T_RETRY_CONTROL, T_DETERMINISM, T_PASS_HANDOFF, determinism_property, VERDICT, scope_and_caveats |
| results/g3_state_ledger.jsonl | .jsonl table not interpreted |
| results/infranodus_audit_2026-10-04/findings.json | title, subtitle, dateline, kicker, lede, intro, graphs, raw_gaps, latent, findings, closing, footer |
| results/infranodus_research_arc_2026-10-05/fulltext/_summary.json | SWEA, ForwardReplay, JointKE, ATBias, KnowledgeSuperposition, SUIT, EditingOverfit, HeteroTokenOverfit, LatentKnowledgeScalpel, DOWKE |
| results/infranodus_research_arc_2026-10-05/operator_chat_inbox/round3_20261005/infranodus_blanthycolino_science_261005T1207.json | nodes, edges, graph, statementHashtags, statements |
| results/infranodus_research_arc_2026-10-05/operator_chat_inbox/round3_20261005/infranodus_blanthycolino_science_261005T1215.json | nodes, edges, graph, statementHashtags, statements |
| results/infranodus_research_arc_2026-10-05/operator_chat_inbox/round3_20261005/infranodus_blanthycolino_science_261005T1217.json | nodes, edges, graph, statementHashtags, statements |
| results/infranodus_research_arc_2026-10-05/operator_chat_inbox/round3_20261005/infranodus_blanthycolino_science_261005T1219.json | nodes, edges, graph, statementHashtags, statements |
| results/infranodus_research_arc_2026-10-05/operator_chat_inbox/round3_20261005/infranodus_blanthycolino_science_261005T1220.json | nodes, edges, graph, statementHashtags, statements |
| results/infranodus_research_arc_2026-10-05/operator_chat_inbox/round3_20261005/infranodus_blanthycolino_science_261005T1222.json | nodes, edges, graph, statementHashtags, statements |
| results/infranodus_research_arc_2026-10-05/operator_chat_inbox/round3_20261005/infranodus_blanthycolino_science_261005T1223.json | nodes, edges, graph, statementHashtags, statements |
| results/infranodus_research_arc_2026-10-05/operator_chat_inbox/round3_20261005/infranodus_blanthycolino_science_261005T1228.json | nodes, edges, graph, statementHashtags, statements |
| results/infranodus_research_arc_2026-10-05/operator_chat_inbox/round3_20261005/infranodus_blanthycolino_science_261005T1230.json | nodes, edges, graph, statementHashtags, statements |
| results/infranodus_research_arc_2026-10-05/operator_chat_inbox/round3_20261005/infranodus_blanthycolino_science_261005T1233.json | nodes, edges, graph, statementHashtags, statements |
| results/infranodus_research_arc_2026-10-05/operator_chat_inbox/round3_20261005/infranodus_blanthycolino_science_261005T1235.json | nodes, edges, graph, statementHashtags, statements |
| results/infranodus_research_arc_2026-10-05/operator_chat_inbox/round3_20261005/infranodus_blanthycolino_science_261005T1238.json | nodes, edges, graph, statementHashtags, statements |
| results/infranodus_research_arc_2026-10-05/operator_chat_inbox/round3_20261005/infranodus_blanthycolino_science_261005T1240.json | nodes, edges, graph, statementHashtags, statements |
| results/infranodus_research_arc_2026-10-05/part1_graphs.json | _doc, graphs, difference_calls, research_ideas_passes |
| results/infranodus_research_arc_2026-10-05/part2/_arxiv_pass_log.json | date, queries, pass2_date, pass3_date |
| results/law3_repro_2026-10-03/b3/b3_probes.json | config, edited, native |
| results/law3_repro_2026-10-03/b3/b3_quant_survival_result.json | hf_vs_gguf_f16_agreement, edited_retention, native_country_retention, native_global_retention, delta_edited_minus_native, verdict, threshold |
| results/law3_repro_2026-10-03/law5_inertness_p8.json | gate, device, band, engine, harness, pre, thresholds, verdict |
| results/openresearch_archive/experiments.json | list |
| results/openresearch_archive/native/9963da66-3f9c-40f6-9841-0b3dc54449b4.jsonl | .jsonl table not interpreted |
| results/openresearch_archive/native/c7841253-7a5a-48f5-bac0-785b3f36d1ff.jsonl | .jsonl table not interpreted |
| results/openresearch_archive/native/c7841253-7a5a-48f5-bac0-785b3f36d1ff__agent-a2240a695a6eccdcd.jsonl | .jsonl table not interpreted |
| results/openresearch_archive/native/c7841253-7a5a-48f5-bac0-785b3f36d1ff__agent-a2a02da522bfffadf.jsonl | .jsonl table not interpreted |
| results/openresearch_archive/native/c7841253-7a5a-48f5-bac0-785b3f36d1ff__agent-a4c6cc19867776f5a.jsonl | .jsonl table not interpreted |
| results/openresearch_archive/native/c7841253-7a5a-48f5-bac0-785b3f36d1ff__agent-a606bf127e9bf4517.jsonl | .jsonl table not interpreted |
| results/openresearch_archive/native/c7841253-7a5a-48f5-bac0-785b3f36d1ff__agent-a77533816d384e64e.jsonl | .jsonl table not interpreted |
| results/openresearch_archive/native/c7841253-7a5a-48f5-bac0-785b3f36d1ff__agent-a9e140373d114b5a2.jsonl | .jsonl table not interpreted |
| results/openresearch_archive/native/c7841253-7a5a-48f5-bac0-785b3f36d1ff__agent-aae8fe5b721db1a43.jsonl | .jsonl table not interpreted |
| results/openresearch_archive/native/c7841253-7a5a-48f5-bac0-785b3f36d1ff__agent-abf38cb790ed88101.jsonl | .jsonl table not interpreted |
| results/openresearch_archive/native/c7841253-7a5a-48f5-bac0-785b3f36d1ff__agent-ac19d9622c4e4f791.jsonl | .jsonl table not interpreted |
| results/openresearch_archive/native/c7841253-7a5a-48f5-bac0-785b3f36d1ff__agent-ac2953559a5aa1faa.jsonl | .jsonl table not interpreted |
| results/openresearch_archive/native/c7841253-7a5a-48f5-bac0-785b3f36d1ff__agent-af1c29ffc45028499.jsonl | .jsonl table not interpreted |
| results/openresearch_archive/native/dec2fa80-f1d4-4a06-a699-f4d47c91cfa6.jsonl | .jsonl table not interpreted |
| results/openresearch_archive/sessions.json | list |
| results/openresearch_archive/text_index.jsonl | .jsonl table not interpreted |
| results/r11_medium_on_read.json | experiment, decision_id, class, spec_file, ts, read_result_surface_inventory, off_read_mechanisms, auth_medium_contract_under_test, per_class, aggregate, coverage_holes, self_consistency_note_NOT_validation, read_return_shape_specified, verdict, root_gap_attribution, spec_observations, what_is_coherent, scope_caveats |
| results/r1_commit_bit_ledger.jsonl | .jsonl table not interpreted |
| results/r3_family_screen.json | experiment, date, model, label, families_screened, finding, disposition |
| results/r5_stats.json | per_arm, competitor_allhit_fisher_p, competitor_anyhit_fisher_p, recipe_full_continuous_sign, recipe_full_anyhit_mcnemar_p, recipe_full_allhit_mcnemar_p, diversity_isolated_allhit_p, intensity_isolated_allhit_p, note |
| results/r5b_stats.json | all_hit, mean_rate, overwrite_vs_prior_allhit_fisher_p, overwrite_vs_novel_allhit_fisher_p, v1_resurface, note |
| results/research_pass_2026-10-06/instrument_logs/arxiv.json | instrument, queries |
| results/research_pass_2026-10-06/instrument_logs/browser_raw/gscholar_search.json | list |
| results/research_pass_2026-10-06/instrument_logs/browser_raw/s2_paper_pages.json | list |
| results/research_pass_2026-10-06/instrument_logs/browser_raw/s2_search.json | list |
| results/research_pass_2026-10-06/instrument_logs/browser_sources.json | instrument, generated, entries |
| results/research_pass_2026-10-06/instrument_logs/github.json | instrument, queries |
| results/research_pass_2026-10-06/instrument_logs/huggingface.json | instrument, queries |
| results/research_pass_2026-10-06/instrument_logs/infranodus.json | instrument, queries |
| results/research_pass_2026-10-06/instrument_logs/orx_discover.json | instrument, cli, queries |
| results/research_pass_2026-10-06/instrument_logs/orx_raw/emb_coined.json | list |
| results/research_pass_2026-10-06/instrument_logs/orx_raw/exit_emb_recency.json | list |
| results/research_pass_2026-10-06/instrument_logs/orx_raw/exit_kw_recency.json | list |
| results/research_pass_2026-10-06/instrument_logs/orx_raw/kw_covreg.json | list |
| results/research_pass_2026-10-06/instrument_logs/orx_raw/kw_cpt.json | list |
| results/research_pass_2026-10-06/instrument_logs/orx_raw/kw_hypernet.json | list |
| results/research_pass_2026-10-06/instrument_logs/orx_raw/kw_layersel.json | list |
| results/research_pass_2026-10-06/instrument_logs/orx_raw/kw_lora.json | list |
| results/research_pass_2026-10-06/instrument_logs/orx_raw/kw_memlayer.json | list |
| results/research_pass_2026-10-06/instrument_logs/orx_raw/kw_nullspace.json | list |
| results/research_pass_2026-10-06/instrument_logs/orx_raw/kw_oov.json | list |
| results/research_pass_2026-10-06/instrument_logs/orx_raw/kw_seqcoined.json | list |
| results/research_pass_2026-10-06/instrument_logs/orx_raw/kw_tokinit.json | list |
| results/research_pass_2026-10-06/instrument_logs/orx_raw/oa_mtp.json | list |
| results/research_pass_2026-10-06/instrument_logs/orx_raw/oa_untied.json | list |
| results/research_pass_2026-10-06/instrument_logs/perplexity.json | instrument, queries |
| results/superweight_qwen3b_prune_check.json | layer, row, col, weight, before, pruned, restored |


Unreadable sources:

None in the final build snapshot.


## Every model and the full evidence history

Every card and scoreboard History point displays its source-bound model tag. When neither its recorded metadata nor an unambiguous cited CORPUS link supplies a model, it says `model not recorded`. That remains an honest metadata gap, even if the model could be inferred informally from the era or folder name. The tower uses the selected card's cited layer count, exact recorded layer list, and arm-matched write sizes; it does not assume that every run is a 36-layer Qwen run or every band is 4–8.

Cited Models panels:

| Model | Status | Size | Layers | Tagged cards | Sources and layer source | Transition/limit source |
| --- | --- | --- | --- | --- | --- | --- |
| Qwen2.5-3B | tested | 3 billion parameters | 36 | 1066 | CORPUS/13_G6_1_SCALE_OF_N.md; CORPUS/45_C10L_MINT_TOKEN.md; results/superweight_qwen3b.json | CORPUS/45_C10L_MINT_TOKEN.md |
| Qwen2.5-7B | tested | 7 billion parameters | 28 | 28 | CORPUS/19_B1_SIZE_DENSITY.md; CORPUS/19_B1_SIZE_DENSITY.md:11 | CORPUS/19_B1_SIZE_DENSITY.md |
| Qwen3-0.6B | tested | 0.6 billion parameters | 28 | 3 | CORPUS/07_CP1_GOVERNED_INPIPELINE_WRITE.md; CORPUS/18_E1_DEPLOYMENT_SERVING.md; CORPUS/04_ENV_AND_DEPS.md:27 | CORPUS/18_E1_DEPLOYMENT_SERVING.md |
| Qwen2.5-0.5B | artifact inspected | 0.5 billion parameters | not recorded | 0 | CORPUS/18_E1_DEPLOYMENT_SERVING.md:39 | CORPUS/18_E1_DEPLOYMENT_SERVING.md |
| Qwen2.5-0.5B-Instruct | configured for seal checks | 0.5 billion parameters | 24 | 0 | docs/C10W_ORACLE_PREREG.md; hf_cache/hub/models--Qwen--Qwen2.5-0.5B-Instruct/snapshots/7ae557604adf67be50417f59c2c2f167def9a775/config.json | docs/C10W_ORACLE_PREREG.md |
| GPT-J-6B | tested baseline | 6 billion parameters | not recorded | 0 | CORPUS/04_ENV_AND_DEPS.md:26; memory_mirror/memit-cov-inversion-not-a-hang.md | CORPUS/04_ENV_AND_DEPS.md |
| Llama-3.2-3B | tested earlier | 3 billion parameters | not recorded | 1 | docs/t_branch_decision_document_v1_2.md:59; configs/hparams/llama32_3b_memit_hparams.json | docs/t_branch_decision_document_v1_4.md |
| Llama-3.1-8B | tested earlier | 8 billion parameters | not recorded | 1 | docs/t_branch_decision_document_v1_2.md; memory_mirror/runpod-dashboard-vs-pod-metrics.md | docs/t_branch_decision_document_v1_4.md |
| Mistral-7B | tested earlier | 7 billion parameters | not recorded | 1 | docs/t_branch_decision_document_v1_4.md; memory_mirror/runpod-dashboard-vs-pod-metrics.md | docs/t_branch_decision_document_v1_4.md |
| Qwen3-4B | planned, no result found | 4 billion parameters | not recorded | 0 | CORPUS/22_D1_CAPACITY_LAW.md:63 | CORPUS/22_D1_CAPACITY_LAW.md |
| Gemma-3-4B | external artifact inspected | 4 billion parameters | not recorded | 0 | memory_mirror/runpod-dashboard-vs-pod-metrics.md:14; CORPUS/04_ENV_AND_DEPS.md:28 | CORPUS/04_ENV_AND_DEPS.md |


The earlier Llama-3.1-8B, Llama-3.2-3B, and Mistral-7B branch decisions are separate dated cards, citing the surviving decision document rather than inventing a missing CORPUS verdict. GPT-J is documented as an earlier baseline; the parser does not invent a numerical run for it. Qwen2.5-7B's 28 layers and Qwen3-0.6B's 28 layers are documented in the evidence ledger; Qwen2.5-3B's 36 layers are recorded in `results/superweight_qwen3b.json`. The small Instruct variant's 24 layers come from its tiny saved config file, which is model metadata, not model loading. Earlier Llama/Mistral/GPT-J layer counts remain absent because the inspected program artifacts did not provide an authoritative count.

Model panels separate the best comparable C10 **weight-write scoreboard summary** from the largest observed harness score, including ordinary-word controls. A larger control score is not called a better made-up-name weight write. Planned/inspected model lines are not promoted to completed scientific experiments. Some transition decisions predate the numbered CORPUS ledger; their documentary sources and missing CORPUS linkage are explicit.

All literal model spellings found by the model-name survey are listed below. These include aliases, prior-art comparisons, proposals, and documented caches; a mention alone does not prove that this program tested that model. The curated status table above is the evidence for program use. `results/labviz/model_mentions.json` preserves **every** source line collected for each spelling; the report gives representative lines and the reference count.

| Literal spelling | References | Representative source lines |
| --- | --- | --- |
| Qwen2.5-3B | 248 | CORPUS/26_C1_KVC_INTERACTION.md:10; CORPUS/41_C10K_STAGE0_HARDWARE_ENVELOPE.md:16; CORPUS/45_C10L_MINT_TOKEN.md:6 |
| Qwen2.5-7B-Instruct | 28 | CORPUS/41_C10K_STAGE0_HARDWARE_ENVELOPE.md:16; docs/C10K_M3PRO_STAGE0_DIAGNOSTIC.md:26; docs/C10K_M3PRO_STAGE0_DIAGNOSTIC.md:27 |
| Qwen3-0.6B | 23 | CORPUS/09_CP3_MEMIT_COMPLIANCE.md:50; CORPUS/README.md:28; CORPUS/README.md:31 |
| GPT-J-6B | 18 | CORPUS/00_MASTER_EVIDENCE.md:10; CORPUS/00_MASTER_EVIDENCE.md:17; CORPUS/04_ENV_AND_DEPS.md:26 |
| Qwen2.5-7B | 148 | CORPUS/00_MASTER_EVIDENCE.md:11; CORPUS/00_MASTER_EVIDENCE.md:18; CORPUS/00_MASTER_EVIDENCE.md:127 |
| QWEN3-0.6B | 1 | CORPUS/00_MASTER_EVIDENCE.md:50 |
| Qwen3-4B | 29 | CORPUS/22_D1_CAPACITY_LAW.md:42; CORPUS/22_D1_CAPACITY_LAW.md:63; CORPUS/03_STATUS_LEDGER.md:60 |
| qwen2.5-3b | 8 | CORPUS/16_A2b_REFRESH_KS.md:39; docs/RESEARCH_PASS_CORPUS_INVENTORY_2026-10-06.md:16; docs/RESEARCH_PASS_CORPUS_INVENTORY_2026-10-06.md:16 |
| gpt2-xl | 3 | CORPUS/16_A2b_REFRESH_KS.md:39; memory_mirror/SESSION_CHECKPOINT.md:227; memory_mirror/betaedit-official-repo.md:14 |
| Llama-3.1-8B | 494 | docs/t_branch_decision_document_v1_4.md:37; docs/t_branch_decision_document_v1_4.md:39; docs/t_branch_decision_document_v1_4.md:76 |
| Llama-3.2-3B | 194 | docs/t_branch_decision_document_v1_4.md:37; docs/t_branch_decision_document_v1_1.md:156; docs/grace-patches-canonical-v0_2.md:383 |
| Mistral-7B | 120 | docs/t_branch_decision_document_v1_4.md:37; docs/t_branch_decision_document_v1_1.md:156; docs/grace-patches-canonical-v0_2.md:646 |
| Gemma 3 4B | 1 | docs/PRIOR_ART_CHRISHAYUK_LARQL_2026-10.md:11 |
| Llama-3-8B | 13 | docs/INFRANODUS_INBOX_REVIEW_2026-10-05_round3.md:30; docs/INFRANODUS_RESEARCH_ARC_2026-10-05.md:143; docs/RESEARCH_PASS_CORPUS_INVENTORY_2026-10-06.md:39 |
| GPT2-XL | 7 | docs/t_branch_decision_document_v1_1.md:182; docs/PRIOR_ART_SWEEP_2026-10-04.md:20; docs/PRIOR_ART_SWEEP_2026-10-04.md:39 |
| Llama-3.2-1B | 3 | docs/grace-patches-canonical-v0_2.md:645; docs/INFRANODUS_RESEARCH_ARC_2026-10-05.md:9; docs/PRIOR_ART_SWEEP_2026-10-04.md:137 |
| Qwen2.5-0.5B-Instruct | 1 | docs/C10W_ORACLE_PREREG.md:47 |
| LLaMA-2-7B | 3 | docs/INFRANODUS_RESEARCH_ARC_2026-10-05.md:15; docs/PRIOR_ART_SWEEP_2026-10-04.md:81; docs/PRIOR_ART_SWEEP_2026-10-04.md:146 |
| LLaMA-3-8B-Instruct | 1 | docs/INFRANODUS_RESEARCH_ARC_2026-10-05.md:15 |
| GPT-2 XL | 6 | docs/INFRANODUS_RESEARCH_ARC_2026-10-05.md:16; docs/C10X_ENGINEPATH_PREREG.md:20; docs/RESEARCH_PASS_CORPUS_INVENTORY_2026-10-06.md:25 |
| Llama-3.1-8B-Instruct | 5 | docs/INFRANODUS_RESEARCH_ARC_2026-10-05.md:23; docs/PRIOR_ART_ANYEDITPP_BAYES_CHUNK_2026.md:11; docs/PRIOR_ART_SWEEP_2026-10-04.md:15 |
| LLaMA-3-8B | 2 | docs/INFRANODUS_RESEARCH_ARC_2026-10-05.md:25; docs/PRIOR_ART_SWEEP_2026-10-04.md:81 |
| GPT-2-XL | 11 | docs/grace-patches-canonical.md:157; docs/grace-patches-canonical.md:157; docs/grace-patches-canonical.md:176 |
| GPT-J 6B | 7 | docs/rome-patches-canonical.md:270; docs/rome-patches-canonical.md:304; docs/runbooks/stage_1_sect_runbook_v1_5.md:69 |
| Qwen2.5-1.5B | 3 | docs/spec_predev_validation_plan.md:27; docs/PRIOR_ART_SWEEP_2026-10-04.md:137; docs/PRIOR_ART_SWEEP_2026-10-04.md:154 |
| Llama-3-8B-Instruct | 10 | docs/C10K_ROUTEA_AMENDMENT_3_L2_RESCALE.md:40; docs/PRIOR_ART_SWEEP_2026-10-04.md:83; docs/runbooks/pre_s2_6_fork_work_runbook.md:28 |
| Llama-2-7B | 5 | docs/PRIOR_ART_ANYEDITPP_BAYES_CHUNK_2026.md:11; docs/PRIOR_ART_SWEEP_2026-10-04.md:15; docs/PRIOR_ART_SWEEP_2026-10-04.md:83 |
| Gemma 4 26B | 1 | docs/gemma_rung4_candidate_note.md:68 |
| Qwen3-1.7B | 5 | docs/RESEARCH_PASS_CORPUS_INVENTORY_2026-10-06.md:39; docs/G6_G7_PASS_CRITERIA_DRAFT.md:18; docs/G6_G7_PASS_CRITERIA_DRAFT.md:30 |
| Qwen3-8B | 17 | docs/HYPOTHESIS_REGISTER_2026-06-18.md:195; docs/HYPOTHESIS_REGISTER_2026-06-18.md:260; docs/PRIOR_ART_SWEEP_2026-10-04.md:15 |
| Gemma 4 12B | 1 | docs/molab_viability_research_prompt.md:6 |
| Gemma-2-9B | 1 | docs/RESEARCH_PASS_PLAN_2026-10-06.md:70 |
| Gemma-4B | 1 | docs/CHRISHAYUK_CORPUS_GAP_MAP.md:63 |
| LLaMA-13B | 2 | docs/PRIOR_ART_LRE_HERNANDEZ_ICLR2024.md:9; docs/PRIOR_ART_LRE_HERNANDEZ_ICLR2024.md:11 |
| Gemma-3-4B | 1 | docs/LARQL_INTEGRATION_ASSESSMENT.md:10 |
| Qwen2.5-0.5B | 1 | docs/LARQL_INTEGRATION_ASSESSMENT.md:12 |
| gemma-3-4b | 2 | docs/LARQL_INTEGRATION_ASSESSMENT.md:27; memory_mirror/runpod-dashboard-vs-pod-metrics.md:14 |
| LLaMA-3.1-8B | 1 | docs/PRIOR_ART_SWEEP_2026-10-04.md:48 |
| LLaMA-2 7B | 1 | docs/PRIOR_ART_SWEEP_2026-10-04.md:59 |
| Gemma-3-4b | 1 | docs/PRIOR_ART_SWEEP_2026-10-04.md:103 |
| Gemma-2-2B | 2 | docs/PRIOR_ART_SWEEP_2026-10-04.md:104; docs/PRIOR_ART_SWEEP_2026-10-04.md:138 |
| Llama-7B | 4 | docs/PRIOR_ART_SWEEP_2026-10-04.md:123; docs/PRIOR_ART_SWEEP_2026-10-04.md:123; docs/PRIOR_ART_SWEEP_2026-10-04.md:124 |
| Llama-13B | 1 | docs/PRIOR_ART_SWEEP_2026-10-04.md:123 |
| Llama-30B | 1 | docs/PRIOR_ART_SWEEP_2026-10-04.md:123 |
| Llama-3.2-3B-Instruct | 1 | docs/PRIOR_ART_SWEEP_2026-10-04.md:138 |
| Qwen2.5-3B-Instruct | 1 | docs/PRIOR_ART_SWEEP_2026-10-04.md:138 |
| Qwen3-14B | 1 | docs/PRIOR_ART_SWEEP_2026-10-04.md:140 |
| LLaMA-2-7b | 1 | docs/PRIOR_ART_SWEEP_2026-10-04.md:144 |
| Llama-3B | 3 | docs/t_branch_decision_document_v1_3.md:37; docs/runbooks/t3_qwen_7b_memit_runbook_v0_1.md:25; docs/framework_findings/framework_finding_memit_ceiling_archival-v1_4.md:163 |
| Llama-8B | 4 | docs/t_branch_decision_document_v1_3.md:37; docs/runbooks/t3_qwen_7b_memit_runbook_v0_1.md:25; docs/framework_findings/framework_finding_memit_ceiling_archival-v1_4.md:163 |
| Llama-3.1-70B | 1 | docs/RESEARCH_PASS_AGENT_BRIEF_2026-10-06.md:67 |
| gpt-j-6B | 3 | docs/session_summaries/session_2_39_kickoff.md:15; memory_mirror/SESSION_CHECKPOINT.md:510; memory_mirror/easyedit-assets-vendored.md:19 |
| llama-7b | 1 | docs/session_summaries/session_2_26_summary_block.md:154 |
| gptj-6B | 1 | memory_mirror/SESSION_CHECKPOINT.md:373 |
| qwen2.5-7B | 1 | memory_mirror/SESSION_CHECKPOINT.md:373 |
| qwen2.5-7b | 3 | memory_mirror/SESSION_CHECKPOINT.md:510; memory_mirror/easyedit-assets-vendored.md:19; memory_mirror/betaedit-official-repo.md:10 |


Every numbered evidence-header card included in the final snapshot:

| Source | Date/model | Recorded header or missing verdict |
| --- | --- | --- |
| CORPUS/00_MASTER_EVIDENCE.md | 2026-06-18 / model not recorded | not recorded for this run |
| CORPUS/01_PROVENANCE_MANIFEST.md | date not recorded / model not recorded | not recorded for this run |
| CORPUS/02_VANDV_CHAIN.md | date not recorded / Qwen3-0.6B | not recorded for this run |
| CORPUS/03_STATUS_LEDGER.md | 2026-06-18 / Qwen3-0.6B | not recorded for this run |
| CORPUS/04_ENV_AND_DEPS.md | date not recorded / model not recorded | not recorded for this run |
| CORPUS/05_SPEC_CONTRACTS_BY_DOMAIN.md | date not recorded / model not recorded | not recorded for this run |
| CORPUS/06_SPEC_WRITE_PATH_AND_BRIDGE_FRAMING.md | 2026-06-18 / model not recorded | not recorded for this run |
| CORPUS/07_CP1_GOVERNED_INPIPELINE_WRITE.md | 2026-06-18 / Qwen3-0.6B | not recorded for this run |
| CORPUS/08_CP2_QUERY_SCHEMA_CAPABILITY.md | 2026-06-18 / model not recorded | Net verdict |
| CORPUS/09_CP3_MEMIT_COMPLIANCE.md | 2026-06-18 / model not recorded | Verdict (A): the recipe IS "MEMIT" per D12, and additionally satisfies BOTH of D20's mandatory safeguards** — |
| CORPUS/10_G1_TWO_PHASE_COMMIT.md | 2026-06-18 / model not recorded | not recorded for this run |
| CORPUS/11_G2_SECURITY_LAYER.md | 2026-06-18 / model not recorded | not recorded for this run |
| CORPUS/12_G3_VALIDATION_PIPELINE.md | 2026-06-18 / model not recorded | not recorded for this run |
| CORPUS/13_G6_1_SCALE_OF_N.md | 2026-06-18 / Qwen2.5-3B | VERDICT — SPLIT: write-side PASS, cross-entity-consistency FAIL |
| CORPUS/14_A1_BATCH_VS_SEQUENTIAL.md | 2026-06-18 / model not recorded | VERDICT — PASS (robust): batch ELIMINATES the cross-entity corruption within the tested range (N≤100) |
| CORPUS/15_A2_RELATION_BALANCED_SENTINELS.md | 2026-06-18 / model not recorded | VERDICT — PARTIAL (strong, directional): sentinels substantially mitigate but do not eliminate |
| CORPUS/16_A2b_REFRESH_KS.md | 2026-06-18 / model not recorded | VERDICT — K_S STALENESS RULED OUT as the A2 limiter (3-seed paired + clean seed-0 instrument) |
| CORPUS/17_B3_QUANTIZATION_SURVIVAL.md | 2026-06-18 / model not recorded | VERDICT — PASS (edits survive real Q4_K_M deployment quantization) |
| CORPUS/18_E1_DEPLOYMENT_SERVING.md | 2026-06-18 / Qwen2.5-3B | VERDICT — Claim A PASS (llama.cpp) · Claim B FALSIFIED (LARQL, Qwen2.5) |
| CORPUS/19_B1_SIZE_DENSITY.md | 2026-06-18 / model not recorded | VERDICT — PARTIAL: batch-clean does NOT fully replicate at 7B |
| CORPUS/20_C2_KEYING_DEPTH_MAP.md | 2026-06-18 / Qwen2.5-3B | VERDICT — C2 PRUNED; a mechanism map emerges |
| CORPUS/21_C2BAND_FALSIFIER.md | 2026-06-19 / Qwen2.5-3B | VERDICT — PASS (mechanical), NOT PROMOTED to PROVEN: a **real direction-specific REDISTRIBUTION, underpowered, with an unquantified within-entity cost |
| CORPUS/22_D1_CAPACITY_LAW.md | 2026-06-20 / Qwen2.5-3B | VERDICT — PARTIAL (mixed seeds), with ROBUST evidence that total-N-alone is insufficient |
| CORPUS/23_D20_COMPACTION_SUBBATCH.md | 2026-06-21 / Qwen2.5-3B | Verdict — DIRECTIONAL MECHANISM found (NOT a falsification of the spec's condition 3) — tightened by gpt-5.5 |
| CORPUS/24_R15_CONSTRAINT_PROBE.md | 2026-06-24 / Qwen2.5-3B | Net verdict — TWO findings, calibrated |
| CORPUS/25_R9_DELETION_RESIDUE.md | 2026-06-24 / Qwen2.5-3B | Net verdict — CHARACTERIZATION (floor result), framed per advisor |
| CORPUS/26_C1_KVC_INTERACTION.md | 2026-06-24 / Qwen2.5-3B | Verdict |
| CORPUS/27_R2_REVERSE_LOOKUP.md | 2026-06-25 / Qwen2.5-3B | Verdict |
| CORPUS/28_R13_PARAPHRASE_GENERALIZATION.md | 2026-06-25 / model not recorded | Verdict / F1 impact |
| CORPUS/29_R5_PARAPHRASE_ROBUSTNESS.md | 2026-06-25 / Qwen2.5-3B | Verdict / F1 impact — INSERT path improved; UPDATE path bracketed + unresolved |
| CORPUS/30_R5B_OVERWRITE_PRIOR_EDIT.md | 2026-06-25 / Qwen2.5-3B | not recorded for this run |
| CORPUS/31_R1_SELECT_READBACK.md | 2026-06-25 / model not recorded | Verdict — NOT delivered; reconciliation is bleed-UNSOUND (advisor-corrected framing) |
| CORPUS/32_R1_COMMIT_BIT_SELECT.md | 2026-06-25 / model not recorded | not recorded for this run |
| CORPUS/33_R11_MEDIUM_ON_READ.md | 2026-06-25 / model not recorded | Verdict:** **COHERENT-VIA-DERIVATION + PREVENTION; the lone residual is an INSTANCE of the already-recorded "no formal query-language section" root gap — NOT a new F1 condition. |
| CORPUS/34_C6_LEDGER_IMMUTABILITY_REDTEAM.md | 2026-06-25 / model not recorded | Verdict |
| CORPUS/35_C10_MULTI_TOKEN_VALUE.md | 2026-06-25 / model not recorded | not recorded for this run |
| CORPUS/36_C10_RESIDUAL_COINED_VALUES.md | 2026-06-26 / model not recorded | Verdict: RESIDUAL FRAGILE — realistic project-coined multi-word semantic values express at only 19–31% held-out-paraphrase full-sequence (≪ the 85% gate). C10 the CONDITION is CONFIRMED-and-WORSENED for the real value class; the dominant MECHANISM is a DISTINCT multi-token length-realization wall (not C10's fit-then-fail-to-generalize parrot). |
| CORPUS/37_C10_BANDKNOB.md | 2026-06-26 / model not recorded | Verdict: NO MATERIAL KNOB RESCUE.** Moving the edit band from baseline `[4,8]` to later `[8,12]` does **not** rescue the hard realistic coined-coined value class. The later band modestly improves canonical trained-prompt full-sequence fit (`29.2 to 45.8`, +16.6pp) but still misses the pre-registered diagnostic threshold and remains below 60%; the binding behavioral read metric **worsens** (`para_full 13.9 to 5.6`, -8.3pp). C10 remains open; pure later-band W-realization is not enough. |
| CORPUS/38_C10_BAND412.md | 2026-06-26 / model not recorded | Verdict: NO MATERIAL KNOB RESCUE.** The widened `[4,12]` MEMIT/AlphaEdit recipe at the tested strength/hparams does **not** rescue the hard A7 project-coined value class. The binding held-out behavioral read metric worsens (`para_full 11.1 to 6.9`, -4.2pp). Canonical trained-prompt fit improves only modestly (`canon_full 29.2 to 41.7`, +12.5pp), below the pre-registered W-realization-only threshold and far below any usability bar. C10 remains open; this result eliminates this cheap band-widening knob only, not wider-layer recipes in general and not MEMIT capacity. |
| CORPUS/39_C10_STRENGTH_LAYER_SWEEP.md | 2026-06-26 / model not recorded | Verdict: NO BEHAVIORAL RESCUE WITH ONE NON-VIABLE TRADEOFF.** The three pre-registered MEMIT strength/layer-count candidates do **not** rescue the hard A7 project-coined value class. The binding held-out behavioral read metric is `para_full`; it worsens for every candidate: baseline **20.8% (15/72)** → strength150 **13.9% (10/72)**, lowcov2500 **5.6% (4/72)**, deep-band **0.0% (0/72)**. The deep recipe improves canonical trained-prompt fit (**29.2% to 58.3%**) but collapses A1/A2 controls (**37.5% / 22.2%**) and is not a viable rescue. C10 remains open; this closes the pre-AnyEdit bounded MEMIT knob pass, not MEMIT in general. |
| CORPUS/40_C10_ANYEDIT_PILOT.md | 2026-06-27 / model not recorded | Verdict: TRADEOFF_NOT_CLEAN_RESCUE.** The local AnyEdit-style autoregressive target/window transplant with `window_size=1` is **not** a clean C10 rescue. It passes the embedded alignment/no-op gates, but it collapses A1/A2 held-out behavior and worsens the hard A7 project-coined value class. Baseline A7 `para_full` is **12.5% (9/72)**; AnyEdit-window1 A7 `para_full` is **1.4% (1/72)**. More importantly, A1/A2 controls fall from **93.1% / 97.2%** to **0.0% / 0.0%**. C10 remains open; this result does not falsify the AnyEdit family or upstream AnyEdit. |
| CORPUS/41_C10K_STAGE0_HARDWARE_ENVELOPE.md | 2026-10-04 / Qwen2.5-3B | VERDICT — HALTED - HARDWARE_ENVELOPE, with a secondary code UPSTREAM_ENV_UNDEFINED |
| CORPUS/42_C10K_ROUTEA_CONTROLS_NOT_RECOVERED.md | 2026-10-04 / Qwen2.5-3B | VERDICT — HALTED — CONTROLS_NOT_RECOVERED (prereg §3 stop rule; the one allowed fix was spent) |
| CORPUS/43_C10K_KEYING_ABLATION.md | 2026-10-04 / model not recorded | VERDICT — KEYING LOCUS DECIDES WHAT IS WRITTEN — last-token-keyed singles land but do not transfer to paraphrases and bleed onto same-frame prompts to a varying degree (F3 SUFFICIENT, MEMIT, N = 1; frame-bleed BETWEEN) |
| CORPUS/44_C10L_COVGEOM_SPARSEBAND.md | 2026-10-05 / Qwen2.5-3B | VERDICT — NULL for arm B (P := I), arm C ({4, 8}) and arm C′ ({7, 8}); D not admitted; ceiling admits LEAD |
| CORPUS/45_C10L_MINT_TOKEN.md | 2026-10-05 / Qwen2.5-3B | VERDICT — PARTIAL ×2 (A7-mint-G 39/72, A7-mint-N 46/72), §6 sub-read G ≈ N; A1-rare 25/72; P4 (GGUF) withheld by the frozen rule |
| CORPUS/46_C10M_DIAG_READPARTITION_EDITINJECT.md | 2026-10-05 / Qwen2.5-3B | VERDICT — Q1 ABSENT-DOMINANT · Q2 H1 (collateral bucket) · Q3 SEED-SENSITIVE |
| CORPUS/47_C10N_ZTRANSPORT.md | 2026-10-05 / Qwen2.5-3B | VERDICT — TARGET-PORTABLE by the frozen rule, in a LOW-CONTROL process (reported; not promoted as a CORPUS/46 replication) |
| CORPUS/48_C10O_MAGNITUDE_DIRECTION.md | 2026-10-05 / Qwen2.5-3B | VERDICT — DIRECTION (routing label; projection-preserving variant recovers 0.93) |
| CORPUS/49_C10P_TWOPASS_SOLVE.md | 2026-10-05 / Qwen2.5-3B | VERDICT — NULL (gain 8/72 < 10), with the effect stated: +8 held-out, canon 7 → 12, total ΔW ×1.31, described_as −3.08 |
| CORPUS/50_C10Q_STACKED_SOLVE.md | 2026-10-06 / Qwen2.5-3B | VERDICT — TRADEOFF-PERM-UNMATCHED (gain 12 ≥ 10; `described_as` gate fails; the permuted control's energy is unmatched); prose qualifier -LARGE-WRITE (ΔW₂/ΔW₁ 1.24 > 0.75) |
| CORPUS/51_C10S_SHAREDZ.md | 2026-10-06 / Qwen2.5-3B | not recorded for this run |
| CORPUS/52_C10S_SOLVEFEAS.md | 2026-10-07 / Qwen2.5-3B | VERDICT — UNDERFIT-AT-50, qualified objective-stopped |
| CORPUS/53_C10T_SECONDKEY.md | 2026-10-07 / Qwen2.5-3B | VERDICT — NULL-LARGE-WRITE; candidate not advanced |
| CORPUS/54_C10U_MINT2.md | 2026-10-07 / Qwen2.5-3B | VERDICT — PROVISIONAL; no direction reading on either block |
| CORPUS/55_C10W_ORACLE_P1_INTERIM.md | 2026-10-07 / Qwen2.5-3B | not recorded for this run |


History preserves every scoreboard row, including unscored/HALTED/inconclusive rows, on the 72-question scale with goal 61 and baseline approximately 14. Colours use the source's kind. There is no connecting line that invents intermediate performance. Each row links to its own saved-image card; numbered evidence cards and earlier model branches appear below the chart. Evaluations includes the maintained scoreboard entries plus all numbered/earlier documentary entries; absent structured interpretation fields on those older documents are labelled rather than authored as new results.

## Test-first evidence and verification

`tools/labviz/test_plan.md` was written before production code. The initial builder-presence test failed while `build.py` was absent. Additional regressions were observed failing before their corrections: dropped older fact/arm tables, unknown explicit model names, same-day ordering, primary mint write-size attachment, image clipping, and title/score overlap. The last overlap regression observed a 6.391689-point gap against a required 12-point minimum before the renderer correction.

The acceptance list as written:

```text
# Lab View acceptance tests (written before implementation)

Source: `results/labviz_codex_brief.md`, including Full history and Every model tested.
This is a read-only evidence viewer for the write engine / behavioral validation
cells of the F1 map. It makes no new scientific verdicts.

1. Builder exists; first run must fail before production code exists.
2. Single-arm synthetic counts remain exact; binding counts take precedence.
3. Missing fields stay null and pictures explicitly say "not recorded for this run".
4. Percentages are never rounded back into counts.
5. Real legacy arms + detail, recipe wrappers, mint records, reader probability
   arrays, training records, retained-fact records, and per-unit arrays parse.
6. A 24 × 3 grid uses recorded Boolean answers only; missing cells stay unknown.
7. Teacher-forced positions are labelled separately from free-answer outcomes.
8. Probabilities stay separate from teacher-forced hit rates.
9. Side effects preserve recorded denominators and before/after writing quality.
10. Layer sizes are attached only to the matching arm and recipe.
11. Model tags come from recorded fields, referenced hparams, or cited evidence;
    unknown remains "model not recorded". Reviewer names are not tested models.
12. The tower takes real layer counts and exact edited layer sets; no guessed band.
13. A model inventory covers documented earlier lines and distinguishes tested,
    configured, and mentioned-only models. Transition notes cite their sources.
14. Harness log and training log parsers preserve each observation, including zeros.
15. Terminal logs cannot be described as running; timestamps/staleness are visible.
16. Every results folder is surveyed, flat June files included; unsupported and
    unreadable files are listed. Every numbered CORPUS verdict and scoreboard
    row appears, without manufacturing absent historical experiments.
17. Evaluations seed has exactly one entry per scoreboard result; all five fields
    are source-bound. Later builds read it without overwriting operator updates.
18. Build round trip: HTML parses, seven tabs exist, every referenced image exists,
    SVG and PNG are both saved, source citations resolve, no broken card links.
19. Second build has stable IDs and bytes for unchanged inputs; images are reused.
20. Phone CSS constrains all elements to the viewport, has no fixed minimum width
    exceeding 390 px, and provides 44 px touch targets and high contrast text.
21. Browser checks at 390 px portrait and 844 px landscape: all tabs, selector,
    History links and offline / WebGL-unavailable fallback, with screenshots if
    the managed sandbox allows a browser to run.
22. No torch/model/tokenizer import or science-path execution; only authorised
    output files change. Server syntax is valid and binds port 8765 with a 60 s
    rebuild loop; live serving is checked if socket binding is permitted.

The explicit request to create `docs/c10_evaluations.json` is the brief's specific
exception to its output-directory rule. No commits or canonical science updates.
```

Final test command:

```sh
MPLCONFIGDIR=results/labviz/.matplotlib .venv/bin/python -B -m unittest tools.labviz.test_labviz -v
```

Final green output, verbatim:

```text
test_binding_count_and_zero_are_preserved (tools.labviz.test_labviz.LabViewTests.test_binding_count_and_zero_are_preserved) ... ok
test_build_round_trip_idempotent_missing_fields_and_source_safety (tools.labviz.test_labviz.LabViewTests.test_build_round_trip_idempotent_missing_fields_and_source_safety) ... ok
test_builder_is_present (tools.labviz.test_labviz.LabViewTests.test_builder_is_present) ... ok
test_earlier_model_branches_have_dated_source_cards (tools.labviz.test_labviz.LabViewTests.test_earlier_model_branches_have_dated_source_cards) ... ok
test_evaluations_come_from_scoreboard (tools.labviz.test_labviz.LabViewTests.test_evaluations_come_from_scoreboard) ... ok
test_every_results_folder_and_corpus_header_is_surveyed (tools.labviz.test_labviz.LabViewTests.test_every_results_folder_and_corpus_header_is_surveyed) ... ok
test_exact_grid_has_unknown_cells (tools.labviz.test_labviz.LabViewTests.test_exact_grid_has_unknown_cells) ... ok
test_explicit_model_name_outside_catalog_is_retained (tools.labviz.test_labviz.LabViewTests.test_explicit_model_name_outside_catalog_is_retained) ... ok
test_generic_facts_keep_recorded_boolean_outcomes (tools.labviz.test_labviz.LabViewTests.test_generic_facts_keep_recorded_boolean_outcomes) ... ok
test_layer_sizes_match_only_their_arm (tools.labviz.test_labviz.LabViewTests.test_layer_sizes_match_only_their_arm) ... ok
test_log_counts_loss_and_terminal_status (tools.labviz.test_labviz.LabViewTests.test_log_counts_loss_and_terminal_status) ... ok
test_missing_and_percent_only_counts (tools.labviz.test_labviz.LabViewTests.test_missing_and_percent_only_counts) ... ok
test_model_metadata_is_source_bound (tools.labviz.test_labviz.LabViewTests.test_model_metadata_is_source_bound) ... ok
test_no_probability_invented_from_teacher_forced_hits (tools.labviz.test_labviz.LabViewTests.test_no_probability_invented_from_teacher_forced_hits) ... ok
test_no_science_imports (tools.labviz.test_labviz.LabViewTests.test_no_science_imports) ... ok
test_older_per_run_and_injection_tables (tools.labviz.test_labviz.LabViewTests.test_older_per_run_and_injection_tables) ... ok
test_phone_css_contract (tools.labviz.test_labviz.LabViewTests.test_phone_css_contract) ... ok
test_primary_mint_arm_has_its_recorded_write_sizes (tools.labviz.test_labviz.LabViewTests.test_primary_mint_arm_has_its_recorded_write_sizes) ... ok
test_real_supported_schemas (tools.labviz.test_labviz.LabViewTests.test_real_supported_schemas) ... ok
test_runs_use_recorded_time_within_the_same_day (tools.labviz.test_labviz.LabViewTests.test_runs_use_recorded_time_within_the_same_day) ... ok
test_saved_picture_text_does_not_clip_at_right_edge (tools.labviz.test_labviz.LabViewTests.test_saved_picture_text_does_not_clip_at_right_edge) ... ok
test_saved_picture_title_and_score_do_not_overlap (tools.labviz.test_labviz.LabViewTests.test_saved_picture_title_and_score_do_not_overlap) ... ok
test_whole_history_older_arm_fact_and_depth_records (tools.labviz.test_labviz.LabViewTests.test_whole_history_older_arm_fact_and_depth_records) ... ok

----------------------------------------------------------------------
Ran 23 tests in 16.838s

OK
```

Full generated-site round-trip and integrity output, verbatim:

```text
PASS: 1369 unique cards; 7 tabs; 1379 HTML image references; 5697 local links; 1369 SVG/PNG pairs; all cited source snapshots exist.
PASS: JavaScript and launcher syntax; generated site ignored; SVG and PNG evidence images trackable; no science imports.
Runtime browser, WebGL, Safari, localhost/LAN/Tailscale serving: UNVERIFIED (managed sandbox denies browser launch/socket binding).
```

`verification.json` records all syntax-check exit codes, Git-ignore probes, image/link counts, forbidden-import checks, and the tracked-file baseline comparison. All active SVGs were parsed as XML and all active PNGs passed their image integrity checks. Every card's source snapshot exists. The fixture test proves unchanged-input byte stability and preservation of a later operator evaluation edit. The CSS test checks the 390 px constraint and 44 px controls; it is a static contract, not a browser measurement.

## Running locally

From the worktree root:

```sh
bash tools/labviz_serve.sh
```

Open `http://127.0.0.1:8765` on the Mac or `http://<Mac-LAN-or-Tailscale-address>:8765` on the iPhone. The launcher builds once, serves with the repo venv's `python -m http.server` on port 8765 bound to `0.0.0.0` (including localhost and LAN/Tailscale interfaces), then rebuilds every 60 seconds. A failed build stops serving rather than silently showing success. Stop it with Ctrl-C. No route is provided for changing scientific data.

A one-time build is `.venv/bin/python -B tools/labviz/build.py`. Real serving was not launched successfully in this sandbox; host firewall and Tailscale reachability still require verification where socket binding is permitted.

## Phone-width screenshot descriptions

These are **expected 390 px layouts derived from the generated HTML/CSS**, not captured browser screenshots. Real phone/desktop screenshots could not be obtained because the available Chromium process fails under the managed sandbox. The saved experimental PNG was visually inspected; that is evidence-image inspection, not UI layout verification.

1. **Now:** dark navy background, bright white title and wrapped touch-size tabs. A single-column program brief, timestamped latest log observation, latest counts/loss where recorded, and running/queued statements from the scoreboard. The card states that a log snapshot does not prove process liveness.
2. **Runs:** model selector and search stack within the viewport; cards show source-bound model/date/schema badges, a full-width saved picture, and the four plain-language explanations below it. Twenty-four cards are shown initially; a large button reveals more. Missing data is written out. Source and SVG/PNG downloads are in expandable details.
3. **3D model:** full-width recorded-run selector, a short definition, and a 570 px high interaction area. The optional tower has labelled real layers, the exact recorded edited set, and matching write-size bars. The local flat diagram shows the same metadata while the optional enhancement loads or fails. Unknown layer counts produce an explicit message rather than invented slabs.
4. **Models:** one panel per cited model line in a single column, with parameter size, known/unknown layer count, use dates, tagged observations, comparable C10 write summary, separate control-inclusive scores, and source/transition links. Planned and inspected status badges remain visible.
5. **History:** each scoreboard row has a wrapped date/title/model label and a viewport-width score track, with the goal and baseline indicators. Points use the recorded kind's colour. The whole numbered evidence ledger and the earlier model branches continue below it, each linking to its card. The complete chart also has an SVG download.
6. **Learn:** ten short explainers stack in one column; each has a real saved source-bound example image and a link to the associated observation. Definitions cover the language model, layers, a weight write, rewording, tokens, new vocabulary entries, side effects, baselines/repeats, the ceiling test, and 61 of 72.
7. **Evaluations:** the pattern groups expand through large details controls, followed by the five-field maintained entries and the earlier documentary evaluations. They retain the source's verdict and limits. Pattern text explicitly avoids claiming a controlled comparison between idea families.

At landscape width the CSS allows two columns only when the viewport is at least 800 px. Wrapping, zero minimum child width, constrained image widths, and touch controls apply in both orientations. Actual Safari portrait/landscape rendering and pinch/drag behavior remain UNVERIFIED.

## Open issues and limits

- **Live UI/network:** the localhost probe returned `PermissionError(1, 'Operation not permitted')`. Chromium exited with signal 5 / exit 133 and a macOS sandbox fatal error at `content/browser/sandbox_parameters_mac.mm:87`, `Input/output error (5)`. Consequently no browser screenshot, DOM-width measurement, actual tap/keyboard interaction, offline-CDN/WebGL fallback, LAN request, or Tailscale request is claimed as tested. JavaScript and launcher syntax checks passed.
- **Independent external review:** the local Claude CLI auth probe reported `loggedIn: false`, `authMethod: none`. No authenticated out-of-family review ran; no independent-review approval is claimed.
- **Historical gaps:** `269` cards lack an unambiguous parsed model tag. Some older records lack dates, full model architecture metadata, machine-readable free-answer detail, or an actual verdict header. The interface makes those gaps explicit. Unsupported schemas are listed above rather than guessed.
- **Source interpretation:** documentary cards preserve source text, including any source's own historical limitations. A picture does not certify validity/comparability, convert UNDERFIT to NULL, or supersede frozen preregistrations and later ledger corrections. Historical model transitions are cited descriptions, not a newly inferred model-size law.
- **Current-state observation:** the Now tab reads the latest saved log and program queue. It does not inspect or control processes. A fresh log without a terminal marker is not a verified running experiment.
- **Maintenance:** future scoreboard rows need the program session to maintain `docs/c10_evaluations.json`; the builder protects later operator edits. Source snapshots can change on later rebuilds, while original scientific records remain untouched. Runtime-generated font-cache files are intentionally excluded from the deliverable checksums.
- **Repository handoff:** evidence images are saved and trackable, not committed. The program session changed canonical files concurrently; its work was left intact. Only the named report and authorised implementation outputs were produced; no context-save, memory update, roadmap edit, experiment run, or commit was added by this task.
