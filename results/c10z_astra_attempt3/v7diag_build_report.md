# C10Z V7-DIAG build report — D-C10z-v7diag / D-C10z-drift3

CPU BUILD PASS. Probe remains unlaunched. Built tests first. Recorded 2026-10-09T03:24:27.501534+00:00; worktree `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a`, branch `worktree-c10k-route-a`. **33 new tests PASS; existing ASTRA 209 tests PASS with two MPS skips; benchmark 47 tests PASS.** This is 287 executed passing tests and two skipped tests across the final suites.

## Authority, scope and empirical limits

The first command verified the untouched prereg SHA-256 `7aedd4ace95d2611bf398768df63cb60df6fce5afc23cf23209497bcd1d17a29`; final verification gives the same SHA. Binding sources: `docs/C10Z_ASTRA_PREREG.md:707–816` (Amendment V7-DIAG), `docs/C10Z_V7DIAG_BUILD_BRIEF.md:1–38`, ruling `results/c10z_astra_attempt3/v7_ruling_astra.md`, and the diagnosis’s appended reviewer qualification `v7_diagnosis.md:56`. The freeze-check advisory `v7diag_amend_astra.md:19–21` is implemented. The report path follows the user’s explicit instruction, overriding the brief’s default report path; this report is the sole newly written attempt3 file. Runtime probe outputs remain confined to fresh diagnostic namespaces.

The build used only CPU stubs and short new tests. No MPS allocation, actual model load, real local dataset open/forward measurement, GPU job launch, ASTRA solve/write, benchmark dispatch, attempt4 launch, or commit occurred. Existing full-suite CPU runs took 115.116s (ASTRA) and 2.751s (benchmark); the new final suite took 7.744s. The two hardware regressions were deliberately skipped by the CPU runner, not hardware-qualified.

**CPU bit agreement does not establish MPS equivalence. MPS equivalence, real-model execution, live diagnostic runtime, real cache scoring, scientific A1/A2/D disposition, and late-layer fidelity remain UNVERIFIED.** Attempt3 remains closed HALTED-V7. Its dataset identity remains UNVERIFIABLE; F1000 is a new measurement of the frozen recipe. Population bias, finite-sample variability and numerical/cache mismatch remain competing explanations. This build advances the C10 instrument prerequisite, not F1 closure.

## Requirement → test → implementation

Legend: P=`experiments/track_c/c10z_v7_diag.py`, S=`experiments/track_c/c10z_v7_diag_selftest.py`, L=`tools/run_c10z_v7_diag.py`, D=`experiments/track_c/c10z_astra_arms.py`, T=`experiments/track_c/c10z_astra_selftest.py`. Every test link points at the current real test body, every implementation link at the current source.

| Authority / requirement | Required behavior | Test | Implementation |
|---|---|---|---|
| A.1; amendment 742–743 | Driver-identical float64 CPU sums, 36 pre-hooks, right padding/mask, 100-token truncation, 16-row batches, normalization and final float32 cast | [S:92](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py:92) `test_ast_identity_sums_and_loop_only_row_count_varies`<br>[S:112](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py:112) `test_actual_driver_bit_identity_and_independent_tokens_counts_normalization` | [P:137](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag.py:137) `compute_dstats`<br>[P:102](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag.py:102) `row_metadata` |
| A.1; freeze advisory | Mixed 3/17/101/137-token fixture, nonzero padding (ID97), distinct fp16 layer activations, 62×16+8 batch rows; independently verify 55,000 tokens and hand-computed normalization outside compared loop | [S:112](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py:112) `test_actual_driver_bit_identity_and_independent_tokens_counts_normalization`<br>[S:153](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py:153) `test_hook_cleanup_after_forward_error` | [P:137](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag.py:137) `compute_dstats` |
| A.2; amendment 730–735, 801 | Non-streaming revision-pinned local Arrow population; exact shard set/order/length; HF_HOME resolved from worktree symlink; offline datasets | [S:279](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py:279) `test_local_arrow_revision_length_shards_and_offline_only` | [P:164](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag.py:164) `open_local_split` |
| A.2; amendment 730–735 | Before any forward: all three populations’ indices, IDs, text hashes, token IDs/counts; source/engine/model/tokenizer/cache/environment/prereg hashes; historical identity UNVERIFIABLE | [S:303](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py:303) `test_all_pins_include_every_population_before_forwards`<br>[S:472](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py:472) `test_real_entry_CPU_fixture_pins_durable_before_each_forward` | [P:222](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag.py:222) `build_pins`<br>[P:383](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag.py:383) `run` |
| A.2; amendment 801 | Optional bounded current-hub SHA observation; mismatch recorded, never switches the pinned source | [S:303](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py:303) `test_all_pins_include_every_population_before_forwards` | [P:211](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag.py:211) `hub_revision`<br>[P:222](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag.py:222) `build_pins` |
| A.3; amendment 737–748 | Full seed-1 permutation; exact F1000/R1000/R5000; fresh independent computation; conditional R5000 only when both earlier populations fail P | [S:163](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py:163) `test_full_seed_one_permutation_and_exact_population_sizes`<br>[S:240](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py:240) `test_F_pass_stops_and_random_pass_never_measures_R5000`<br>[S:247](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py:247) `test_R5000_independent_conditional_A2_and_D`<br>[S:472](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py:472) `test_real_entry_CPU_fixture_pins_durable_before_each_forward` | [P:95](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag.py:95) `population_indices`<br>[P:322](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag.py:322) `measure_populations` |
| A.4; amendment 747 | All 36 CPU float32 m tensors plus dataset/token/provenance saved with xb, flush/fsync before scoring | [S:264](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py:264) `test_tensor_exclusive_flush_fsync_and_provenance`<br>[S:240](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py:240) `test_F_pass_stops_and_random_pass_never_measures_R5000`<br>[S:247](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py:247) `test_R5000_independent_conditional_A2_and_D` | [P:302](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag.py:302) `save_population`<br>[P:322](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag.py:322) `measure_populations` |
| A.5; amendment 750–758 | Nine caches loaded once; diag(mom2)/int(count); imported driver average-tie Spearman; finite rho>=0.80 without rounding, equality passes; natural-log E report-only with explicit +inf | [S:197](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py:197) `test_cache_diagonal_count_and_loaded_once`<br>[S:183](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py:183) `test_scoring_uses_driver_spearman_ties_natural_log_and_zero_inf`<br>[S:169](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py:169) `test_ordered_routing_equal_boundary_nonfinite_and_report_only_E` | [P:250](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag.py:250) `load_cache_diagonals`<br>[P:265](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag.py:265) `score_population`<br>[P:285](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag.py:285) `passes`<br>[D:1496](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py:1496) `spearman` |
| A.6; amendment 760–767 | Ordered INCONCLUSIVE/A1/A2/D; no C/search/threshold relaxation; incomplete or integrity failure cannot select a continuation | [S:169](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py:169) `test_ordered_routing_equal_boundary_nonfinite_and_report_only_E`<br>[S:253](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py:253) `test_incomplete_failure_retains_prior_m_and_no_selection`<br>[S:533](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py:533) `test_real_source_cache_model_tokenizer_corruption_is_inconclusive_and_retains_m` | [P:291](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag.py:291) `route`<br>[P:348](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag.py:348) `verify_pins`<br>[P:311](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag.py:311) `publish_verdict` |
| A.7; amendment 722–728 | Fresh UTC namespace only under results/c10z_v7_diagnostic; refuses existing/symlink/attempt3 namespace; pristine snapshot forward-only; no solve/write/candidate/reader promotion | [S:363](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py:363) `test_namespace_refuses_reuse_and_attempt3_path`<br>[S:472](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py:472) `test_real_entry_CPU_fixture_pins_durable_before_each_forward` | [P:88](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag.py:88) `reserve_namespace`<br>[P:361](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag.py:361) `load_pristine`<br>[P:383](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag.py:383) `run` |
| A.7; amendment 769–772; freeze deadline advisory | Immutable 3060s origin across launcher/import/setup/forward/scoring/serialization; OS-default SIGALRM hard termination even during native work holding GIL; durable provisional INCONCLUSIVE; late results not admitted | [S:412](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py:412) `test_immutable_3060_includes_preimport_and_exact_boundary`<br>[S:420](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py:420) `test_OS_timer_terminates_sleep_and_native_GIL_hold_retains_inconclusive`<br>[S:397](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py:397) `test_launcher_native_block_is_bounded_before_probe_dispatch`<br>[S:382](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py:382) `test_CLI_bootstrap_timer_exists_before_driver_import`<br>[S:374](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py:374) `test_launcher_origin_carried_and_future_or_nonfinite_origin_refused`<br>[S:454](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py:454) `test_timer_armed_before_namespace_and_initial_publication`<br>[S:259](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py:259) `test_scoring_deadline_cannot_publish_A1_or_increase_cap`<br>[S:499](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py:499) `test_outer_error_preserves_durable_measured_population_details` | [P:10](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag.py:10) `entry_origin`<br>[P:49](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag.py:49) `Deadline`<br>[P:383](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag.py:383) `run`<br>[L:29](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/run_c10z_v7_diag.py:29) `launch` |
| A.7; driver V11 | Same RSS+driver<=40GiB, driver<=32GiB, and float64-on-MPS guards; CPU doubles only | [S:518](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py:518) `test_memory_ceilings_and_float64_MPS_guard_without_MPS_allocation` | [P:126](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag.py:126) `check_memory`<br>[D:74](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py:74) `memory_guard`<br>[D:174](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py:174) `torch_cpu64` |
| A.7; acceptance | Launcher uses only c10w_p2_gate.check_fingerprint/check_gpu; explicit worktree root; refuses occupied namespace/fingerprint failure/live GPU inventory before exec | [S:334](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py:334) `test_launcher_existing_namespace_fingerprint_gpu_refuse_before_exec`<br>[S:350](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py:350) `test_launcher_success_exec_explicit_worktree_and_no_other_gate`<br>[S:397](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py:397) `test_launcher_native_block_is_bounded_before_probe_dispatch` | [L:29](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/run_c10z_v7_diag.py:29) `launch`<br>[L:23](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/run_c10z_v7_diag.py:23) `gate_module` |
| Part B; amendment 777–782 | Fresh dstats persisted immediately on obtain, before G or V7; process2 exact source bytes copied immediately, before loading G; later duplicate removed; G save remains after V7 | [S:574](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py:574) `test_forced_V7_failure_retains_value_and_provenance_before_G_and_scoring`<br>[S:622](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py:622) `test_G_failure_also_retains_immediately_obtained_dstats`<br>[S:629](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py:629) `test_process2_missing_G_retains_dstats_before_G_load`<br>[S:595](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py:595) `test_process2_exact_input_bytes_retained_on_fail_and_pass`<br>[S:610](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py:610) `test_fresh_and_process2_existing_dstats_refuse_overwrite` | [D:1085](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py:1085) `prepare_instruments`<br>[D:1121](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py:1121) `save_tensor_file` |
| Part B; amendment 779–781 | Unchanged scientific values/checks/outcomes and byte-identical forced-pass dstats.pt, G.pt, overlap_audit.json versus frozen old behavior | [S:586](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py:586) `test_forced_pass_outputs_checks_identical_to_frozen_previous_behavior`<br>[S:595](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py:595) `test_process2_exact_input_bytes_retained_on_fail_and_pass` | [D:1085](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py:1085) `prepare_instruments` |
| Part B acceptance; necessary pin synchronization | Existing ASTRA and benchmark suites pass; reader/test pin matches the untouched current prereg | Full existing suites: 209 ASTRA (two MPS skips), 47 benchmark; [T:2618](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py:2618) `test_amended_prereg_pin_shared_by_driver_reader_and_tests` | [T:2618](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py:2618) `test_amended_prereg_pin_shared_by_driver_reader_and_tests` |

## LAW#4 source read and statistic identity

Before editing, `cat -n` reads covered driver `c10z_astra_arms.py:1085–1156`, `:1493–1506`, `:487–561`, `:1330–1366`; harness `c10e_bandknob.py:1–48`; engine `util/globals.py:1–17`, `globals.yml:1–6`, `rome/layer_stats.py:142–165`, `rome/tok_dataset.py:25–30`, and `util/runningstats.py:1543–1556`; `tools/c10w_p2_gate.py:67–84`; `tools/engine_fingerprint.py:29–48`. The pre-change driver is retained at `/private/tmp/c10z_v7diag_build/driver_before.py`, SHA `e3829f4103ead2927b01c01b93e9148a5056d2f03e962a804a62b72d5d73f5d0`. Final numbered-source reads confirmed the edited spans.

The original driver loop is unchanged (now begins at D:1140). The source test compares the sum initializer, every loop-body AST node, bounds 0 and16, and final normalization/return; only the row-count expression changes from1000 to `len(rows)`. The actual driver method runs with `datasets.load_dataset` and `HfApi` replaced by the fixed 1000-row fixture and fixed40-hex revision. The sole size shim maps the literal `torch.zeros(11008, dtype=float64, device=cpu)` to width3; it does not alter either production source or arithmetic. All36 outputs are bit-identical and independently match integer sum-of-squares /55000 followed by float32.

Raw row lengths cycle through3,17,101,137; token IDs are independently truncated to100. Padding ID97 has conspicuously nonzero activation; three fp16 channels differ by layer. There are62 full16-row batches and one8-row batch. Token IDs, row/text provenance, nonpadding total55000, masking, all36 final tensors, normalization and hook cleanup are checked outside the AST-compared loop. The normal-entry CPU integration fixture also executes two independent1000-row measurements with pins read from disk before every forward. These CPU fixtures supply no MPS equivalence evidence.

The local HF_HOME authority is the driver/harness worktree `hf_cache` symlink, resolving to `/Volumes/memit/llm-database-poc-mirror/hf_cache`. The dataset loader opens the local non-streaming Arrow build under exact revision `b04c8d1ceb2f5cd4588862100d08de323dccfbaa`, validates ordered contiguous shards and recorded split length, and never selects a different cached/hub revision. Read-only metadata inspection found6407814 examples and41 shards; the real dataset was not loaded during the build. Cache paths come from the engine’s actual `globals.yml` STATS_DIR; no guessed cache root or harness import is used. Optional hub observation has a5s request timeout and records unavailable/mismatched SHA explicitly.

## Hard deadline evidence and terminal persistence

An ordinary Python signal handler can be delayed behind native code; the implementation instead uses POSIX `ITIMER_REAL` with default SIGALRM termination. [Python signal documentation](https://docs.python.org/3/library/signal.html#execution-of-python-signal-handlers) describes why a Python handler alone would be insufficient.

The launcher arms the timer before gate imports/checks, carries its original monotonic origin to the probe, and `entry_origin` rejects future/nonfinite/negative origins. The probe arms before importing the driver and adopts its bootstrap timer without restarting it. A frozen deadline object checks boundaries too. Namespace creation, pins, independent forwards, m persistence, scoring, integrity verification, final verdict publication and stdout serialization are inside the cap. No CLI cap/seed/population/batch override exists. A late error preserves the already persisted scores and m.

The final short CPU controls measured: ordinary blocked sleep signal exit -14 at0.2154s; native `ctypes.PyDLL(None).usleep` holding the GIL signal exit -14 at0.2221s; launcher blocked in that native call signal exit -14 at0.1755s. Those tests scale the same immutable timer path to0.15s only inside synthetic subprocesses. Bootstrap observation found3059.982783s remaining before the driver import. The3060s exact-boundary and final-score-expiry tests prevent A1 after expiry. Source, engine, cache, model and tokenizer corruption each cause actual verifier failure and pipeline INCONCLUSIVE while preserving scores and saved m.

The fresh namespace has an exclusive, fsynced provisional `verdict.json` before substantive setup. Atomic progress replacements remain INCONCLUSIVE until measurement and integrity complete. Hard termination during measurement leaves the latest durable INCONCLUSIVE record; partially written population files never supply admission. Timeout before the probe has reserved/published its namespace remains an incomplete/nonzero launch, with no measurement or selection. Downstream consumption requires **exit0 AND completion=complete**; even an A1/A2 file surviving termination near exit cannot authorize continuation without successful exit. Launcher refusal occurs before probe exec and creates no scientific measurement.

## Persistence correction and source identity

In `prepare_instruments`, fresh dstats is saved immediately after computation and before `compute_G`; process2 copies its exact input bytes immediately after loading dstats and before loading G. G’s later persistence remains after V7, and the duplicate dstats save is removed. No statistic recast, normalization, reload into arithmetic, threshold, solve or gate change was made. Forced V7, forced G, and missing process2 G controls retain the already obtained statistic. Forced-pass dstats.pt/G.pt/overlap_audit.json bytes and checks match the copied old test oracle exactly; process2 bytes match the source for failure and pass.

Necessary extra scope: the reader’s single `PREREG_SHA` and the two existing selftest hash literals were synchronized from the old `7c6e52e2…` binding to the verified amendment SHA. The untouched prereg had already changed; the required existing suite exposed the stale binding. The pin test was changed first and failed on the reader’s old SHA before the reader was updated. No scientific reader thresholds changed.

The driver source changes invalidate the current benchmark/go-source identity as expected. Historical benchmark/go records were preserved, not rebound. Only a real A1/A2 diagnostic permits the amendment’s conditional drift rerun#3, its reviewed freeze, fresh admissible benchmark and new go record; A2 also requires consistent reference-D budget/ceiling/validator amendment. No fourth rerun is granted. Nothing in this build resumes attempt3 or admits attempt4.

## Review, deviations and open questions

The supplied Astra freeze review was read in full. A cheap live Claude probe returned `loggedIn=false, authMethod=none`; subscription-backed Claude review could not run in this session. A fresh read-only Codex fallback reviewer was used under `experiments/AGENTS.md` / the advisor-review contract, with weaker independence explicitly retained. Design review found the deferred-handler issue; implementation review found missing early import/launcher coverage and a score-loss path; each received tests first, observed RED, then GREEN. Final review: **PROCEED — CPU build acceptance**, no remaining concrete A.1–7/B defect. This fallback does not replace the brief’s lead/GPT-6-Astra implementation freeze before GPU dispatch.

Deviations/accommodations: (1) the user-named report location overrides the brief default; (2) reader/test hash synchronization is necessary for the required suites; (3) CPU-only size3 stub and explicit MPS skips preserve the build boundary; (4) strict JSON exports undefined Spearman as `null` plus reason and infinite E as `"+inf"`, with no routing relaxation; (5) a durable provisional verdict permits genuine OS termination rather than a deferred Python timeout handler. No other scope change or open implementation defect was identified. Real device/run timing remains unmeasured. The advisory’s corrected delegation timestamp is2026-10-09 01:43:41.034UTC (2026-10-08 19:43:41MDT), per the supplied Astra transcript citation; that external transcript was not independently reverified here, and the prereg was not edited.

The first unguarded-temp baseline had6 failures/2 errors: three stale hash tests plus five `/var`→`/private/var` path-alias failures. Full names/output are retained below. Rerunning with canonical `TMPDIR=/private/tmp/c10z_v7diag_build` fixed the path observations without changing production path guards. RTK was found at `/opt/homebrew/bin/rtk`; Homebrew was absent from the initial shell PATH. The sandbox denied a read-only `ps` inventory probe; it was not retried, and no live launcher/GPU-dispatch validation is claimed. Launcher refusal behavior was verified with controlled CPU gate fixtures, including an explicit competing-C10Y record.

## Lead launch command and projected runtime

**Not executed.** Lead use only after program GPU ownership is released and the required implementation review/freeze is complete:

```sh
LLMDB_ROOT='/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a' '/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python' -B '/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/run_c10z_v7_diag.py' --utc "$(date -u +%Y%m%dT%H%M%SZ)"
```

The launcher fixes LLMDB_ROOT to this worktree even if a different root is inherited, checks occupied namespace first, and reuses only `check_fingerprint`/`check_gpu` from the existing gate. The probe independently repeats the start gates. No attempt continuation is automatic.

Amendment `docs/C10Z_ASTRA_PREREG.md:804–814` projection:

| Phase | Seconds | Source |
|---|---:|---|
| import/model/pins |120| attempt3 import_and_pin allowance |
| local Arrow open/length/permutation/row pins |120| new amendment allowance |
| F1000 |300| reference_D per1000 |
| R1000 |300| same |
| conditional independent R5000 |1500| five times per1000 |
| cache/scoring |120| new amendment allowance |
| serialization |180| serialization_and_restore allowance |
| worst-branch sum |2640| sum of above |
| with15percent margin |3036|2640×1.15|
| fixed cap |3060|rounded up to next minute|

Projected allowances: F-only840s (14min), F+R1000=1140s (19min), worst branch2640s (44min), against cap3060s (51min),420s difference. **These are projections, not measured MPS/R5000 runtime.** Actual full-dataset shuffle, artifact hashing, model/load/forwards and cache timings were not measured during this CPU build. No within-run cap increase exists; timeout/incomplete remains INCONCLUSIVE.

## Protected files, final hashes and reproducible CPU checks

All 16 individually baselined protected files retained their hashes: prereg, engine memit_main, unchanged benchmark selftest, and existing top-level attempt3 files. `git diff --exit-code -- docs/C10Z_ASTRA_PREREG.md memit_dry_run/` and `git diff --check` exit0. The attempted initial hash glob also encountered the attempt3 logs directory (reported as a directory); its file entries were still captured and individually validated. That baseline does not claim a recursive log-directory snapshot. No diagnostic namespace was created under the real results tree. The report is create-only. Pre-existing unrelated changes remain outside this patch. Graft refreshed its index/cache during read-only code lookup; no global-tree cleanliness claim is made.

| File | Final SHA-256 |
|---|---|
|`experiments/track_c/c10z_v7_diag.py`|`bd00eb8d79c974726e45238d64f502cf68951e4bfdc8a17dcc938c49d95f8cd4`|
|`experiments/track_c/c10z_v7_diag_selftest.py`|`71e4993047f697513ecb55bb9b7721aae06d67700da08f156f5f1999c70c7452`|
|`tools/run_c10z_v7_diag.py`|`68fdb90dfce25649125ef87eccd14ab2854b2225f6f4a117f2edf6a931fbf10c`|
|`experiments/track_c/c10z_astra_arms.py`|`5d824cf5322a3d1061258ad5775538f08b6981e8623b1d0e5e7c573c2f73ddba`|
|`experiments/track_c/c10z_astra_read.py`|`e9d479fd592b072b25cdaba69d21eba017bc1be0ad361a9c878865b27baa5850`|
|`experiments/track_c/c10z_astra_selftest.py`|`b2f3eb6f4764c23fbcf5f5e953fc00460449fde7ad497732a7a2f41108464ada`|
|`experiments/track_c/c10z_astra_benchmark_selftest.py`|`1f9cdb5f7200e91a9157b2dda29e836e524554097c80f0913d5ccbaa6bfb9f4a`|
|`docs/C10Z_ASTRA_PREREG.md`|`7aedd4ace95d2611bf398768df63cb60df6fce5afc23cf23209497bcd1d17a29`|
|`memit_dry_run/memit/memit/memit_main.py`|`d941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65`|
|`results/c10z_astra_go_record_attempt3.json`|`dfbbe7204bf171d27ddc206478efefcce8f291b0e244ca845a7c6487337dc1d9`|

Final test commands (all exit0; no model/MPS):

```sh
/opt/homebrew/bin/rtk proxy env TMPDIR=/private/tmp/c10z_v7diag_build LLMDB_ROOT=/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a .venv/bin/python -B /private/tmp/c10z_v7diag_build/run_cpu_selftest.py experiments/track_c/c10z_v7_diag_selftest.py
/opt/homebrew/bin/rtk proxy env TMPDIR=/private/tmp/c10z_v7diag_build LLMDB_ROOT=/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a .venv/bin/python -B /private/tmp/c10z_v7diag_build/run_cpu_selftest.py experiments/track_c/c10z_astra_selftest.py
/opt/homebrew/bin/rtk proxy env TMPDIR=/private/tmp/c10z_v7diag_build LLMDB_ROOT=/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a .venv/bin/python -B /private/tmp/c10z_v7diag_build/run_cpu_selftest.py experiments/track_c/c10z_astra_benchmark_selftest.py
```

The exact CPU wrapper used (also kept on disk) is included for reproducibility:

```python
import os
import runpy
import sys
from pathlib import Path
from unittest.mock import patch

os.environ.update(OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", MKL_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1")
import torch
torch.set_num_threads(1)
path = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(path.parent))
print("CPU_ONLY: MPS availability forced false; unmocked MPS calls forbidden; no model load", flush=True)
with patch.object(torch.backends.mps, "is_available", return_value=False), \
     patch.object(torch.mps, "synchronize", side_effect=AssertionError("MPS forbidden in build")), \
     patch.object(torch.mps, "driver_allocated_memory", side_effect=AssertionError("MPS forbidden in build")):
    runpy.run_path(str(path), run_name="__main__")
```

## Full test output

The following transcripts are unabridged. Early failures are expected RED or the documented baseline failures; final suite outcomes are GREEN. Intermediate reruns are included to preserve the entire test-first audit trail.

### Initial existing ASTRA baseline; pre-change pins and default temp path

Captured `/private/tmp/c10z_v7diag_build/baseline_selftest.txt`; exit status `1`.

```text
CPU_ONLY: MPS availability forced false; unmocked MPS calls forbidden; no model load
test_00_implementation_exists (__main__.SpecTests.test_00_implementation_exists)
Prereg :204: actual driver, reader and stage wrapper exist. ... ok
test_band_boundaries_ordered (__main__.SpecTests.test_band_boundaries_ordered)
Prereg :112, :284: fit -> capacity -> locality -> three exhaustive BAND rows. ... ok
test_budget_origins_prestart_deadlines_round_memory (__main__.SpecTests.test_budget_origins_prestart_deadlines_round_memory)
Prereg :190, :196–198: 5400 seconds, scopes, unknown allowance, exact memory. ... C10Z_PROJECTION {"origins": {"stage01": 100.0}, "ceilings": {"stage01": 7800.0, "stage2": 60.0, "stage3": 6000.0}, "components_s": {"remaining": 1.0}, "scopes": {"stage01": {"elapsed_s": 7799.0, "remaining_s": 1.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 100.0}, "ceilings": {"stage01": 7800.0, "stage2": 60.0, "stage3": 6000.0}, "components_s": {"remaining": 1.001}, "scopes": {"stage01": {"elapsed_s": 7799.0, "remaining_s": 1.001, "ceiling_s": 7800.0}}}
ok
test_completed_stage2_keeps_stage1_round_ceiling (__main__.SpecTests.test_completed_stage2_keeps_stage1_round_ceiling)
Prereg :198, :225: completed stage2 still checks stage1 A7 timing. ... ok
test_cpu_joint_algebra_independent_reference (__main__.SpecTests.test_cpu_joint_algebra_independent_reference)
Prereg :76, :78–80, :151: nonsymmetric solve, scalar-loop independent assembly. ... ok
test_cpu_null_weight_margin_fp16_selection (__main__.SpecTests.test_cpu_null_weight_margin_fp16_selection)
Prereg :75, :77–80, :210: independent floor/median, excluded competitor, fp32 add. ... ok
test_fit_count_boundaries (__main__.SpecTests.test_fit_count_boundaries)
Prereg :210, :230–234: exact integer FIT, positive 22/23, canonical 22/23. ... ok
test_fixed_competitor_and_native_reference_contract (__main__.SpecTests.test_fixed_competitor_and_native_reference_contract)
Prereg :155: native gathered logits, fixed competitor, finite last-layer path. ... ok
test_json_real_writer_and_frozen_sources (__main__.SpecTests.test_json_real_writer_and_frozen_sources)
Prereg :137, :204, :219, :224: round-trip, immutable outputs, finite science. ... FAIL
test_k1_k2_omissions_and_replication (__main__.SpecTests.test_k1_k2_omissions_and_replication)
Prereg :265–280: valid early stops != V12, lower labels, R2/R3 boundaries. ... ok
test_known_answer_scalar_and_native_fp16_reference (__main__.SpecTests.test_known_answer_scalar_and_native_fp16_reference)
Prereg :155: independent scalar A/ridge/columns and native finite reference. ... ok
test_law3_both_sides (__main__.SpecTests.test_law3_both_sides)
Prereg :123, :217: all inclusive envelope edges, and A1/A2 67/68. ... ok
test_manifest_population_and_post_instrument_tampering (__main__.SpecTests.test_manifest_population_and_post_instrument_tampering)
Prereg :137, :147–155, :224: complete inputs, missing controls, post-write evidence. ... ok
test_omission_reasons_follow_K1_K2 (__main__.SpecTests.test_omission_reasons_follow_K1_K2)
Prereg :265–267: every unrun expansion is recorded with its actual stopping reason. ... ok
test_ordering_and_stage_transport (__main__.SpecTests.test_ordering_and_stage_transport)
Prereg :120–125, :127–133, :218: no early observation, ordered one-stage requests. ... ok
test_raw_evidence_over_asserted_fit_write_and_repro (__main__.SpecTests.test_raw_evidence_over_asserted_fit_write_and_repro)
Prereg :224, :230, :272, :278: reject forged counts, bytes and certificates. ... ok
test_restore_finally_and_nonempty_hook_registry (__main__.SpecTests.test_restore_finally_and_nonempty_hook_registry)
Prereg :129, :152–153: all36 tensors restored after write/eval/hook failures. ... ok
test_review_Z5_footprint_rejects_any_write_outside_selected_columns (__main__.SpecTests.test_review_Z5_footprint_rejects_any_write_outside_selected_columns)
Prereg :80, :152: only selected W_down columns may differ; every other parameter byte-identical. ... ok
test_review_Z6_restore_covers_all_36_and_verify_detects_drift (__main__.SpecTests.test_review_Z6_restore_covers_all_36_and_verify_detects_drift)
Prereg :64, :129, :153; V3 :216: full 36-layer restore, byte-hash verification halts on drift. ... ok
test_review_cross_process_replication_needs_clean_pair (__main__.SpecTests.test_review_cross_process_replication_needs_clean_pair)
Prereg :277: LEAD/PARTIAL replicate only when both clean; differing base labels otherwise -NOT-REPLICATED. ... ok
test_review_reader_instrument_ceilings_audits_and_capacity (__main__.SpecTests.test_review_reader_instrument_ceilings_audits_and_capacity)
Prereg :147, :151–155, V2/V5/V9/V12, §2.5, §2.11: each recorded gate outcome is re-checked by the reader. ... ok
test_review_stage0_law3_gate_precedes_all_new_work (__main__.SpecTests.test_review_stage0_law3_gate_precedes_all_new_work)
Prereg :120, :123, :302 (row 13): LAW#3 miss halts V4 with baseline-only record; nothing runs before the gate. ... ok
test_review_stage1_round_over_120s_halts_in_run (__main__.SpecTests.test_review_stage1_round_over_120s_halts_in_run)
Prereg :198, V13 :225, row 24: a synchronized stage-1 round >120 s halts HALTED-BUDGET in the run. ... C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1200.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 2760.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1200.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 2760.0, "ceiling_s": 7800.0}}}
ok
test_review_stage_call_refusals (__main__.SpecTests.test_review_stage_call_refusals)
Prereg :133, :137, :196, :266: fresh OUT_DIR, K1/K2 and absent-ceiling refusals happen before any launch. ... ERROR
test_review_wrapper_delegates_under_standing_law5 (__main__.SpecTests.test_review_wrapper_delegates_under_standing_law5)
Prereg :127, :157; V2/V9: run_law5 always takes the original path; ASTRA only behind LAW#3 and instruments. ... ok
test_review_write_prestart_projection_refuses_before_observation (__main__.SpecTests.test_review_write_prestart_projection_refuses_before_observation)
Prereg :196, V13 :225: refuse to start a candidate write when elapsed + projection exceeds the ceiling. ... C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1200.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 7799.0, "remaining_s": 2760.0, "ceiling_s": 7800.0}}}
ok
test_review_write_round_cap_columns_and_capacity (__main__.SpecTests.test_review_write_round_cap_columns_and_capacity)
Prereg :79–81, :112: <=10 writes then round cap; only selected columns written; B_Z from Z's A7 only. ... C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1200.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 2760.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1200.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 2760.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1200.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 2760.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1200.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 2760.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 7800.0}}}
ok
test_side_gate_boundaries_and_populations (__main__.SpecTests.test_side_gate_boundaries_and_populations)
Prereg :239–245: every side gate equality passes, next value fails; no pooling. ... ok
test_table_T_exhaustive_and_integer_boundaries (__main__.SpecTests.test_table_T_exhaustive_and_integer_boundaries)
Prereg :249–261: independent exhaustive T1–T5, n18/19/29/30 and g9/10. ... ok
test_terminal_K1_wrapper_waits_for_close_error (__main__.SpecTests.test_terminal_K1_wrapper_waits_for_close_error)
Prereg :129, :265: terminal K1 response waits for verified close, propagates error. ... ok
test_terminal_halt_overrides_earlier_complete_pass (__main__.SpecTests.test_terminal_halt_overrides_earlier_complete_pass)
Prereg :196, :225: stage2 hard halt invalidates earlier stage1 pass. ... ok
test_transport_wait_publication_and_worker_failure (__main__.SpecTests.test_transport_wait_publication_and_worker_failure)
Prereg :126–139, :196: resident continuity, completed response, bounded failed wait. ... {"label": "PARTIAL", "next_stage": 2}
ok
test_ttl_every_Z_arm_and_incomplete_actual_repro_failure (__main__.SpecTests.test_ttl_every_Z_arm_and_incomplete_actual_repro_failure)
Prereg :267, :274, :278: any Z TTL, and omitted plus failed R1 retain both flags. ... ok
test_w1_even_median_w2_subject_free (__main__.SpecTests.test_w1_even_median_w2_subject_free)
Prereg :210, :272–274: even median, exact W1/W2, depth OR and +1 boundary. ... ok
test_worked22_validity_precedes_conditional_label (__main__.SpecTests.test_worked22_validity_precedes_conditional_label)
Prereg :149, :208, :311: contradictory raw canonical evidence HALTs before labels. ... ok
test_worked_01 (__main__.SpecTests.test_worked_01)
Prereg :290: n = 18, FIT ... ok
test_worked_02 (__main__.SpecTests.test_worked_02)
Prereg :291: n = 18, U (φ_μ = 0.80) ... ok
test_worked_03 (__main__.SpecTests.test_worked_03)
Prereg :292: n = 21, g = 9 (a = 12) ... ok
test_worked_04 (__main__.SpecTests.test_worked_04)
Prereg :293: n = 25, a = 16, g = 9 ... ok
test_worked_05 (__main__.SpecTests.test_worked_05)
Prereg :294: n = 22, g = 10, gates, FIT; stage 2 G0 holds, W1 0.4 (above the paper's SemCon range; reported, not a qualifier) ... ok
test_worked_06 (__main__.SpecTests.test_worked_06)
Prereg :295: n = 22, g = 10, G7 fails 3 (view, fact, depth) gates ... ok
test_worked_07 (__main__.SpecTests.test_worked_07)
Prereg :296: n = 29, gates, FIT; stage 2 Z-A1 = 67/72 ... ok
test_worked_08 (__main__.SpecTests.test_worked_08)
Prereg :297: n = 30, gates, FIT, W1 0.3; p2 n = 29, both processes clean ... ok
test_worked_09 (__main__.SpecTests.test_worked_09)
Prereg :298: n = 31, gates, U (φ_0^id = 22) ... ok
test_worked_10 (__main__.SpecTests.test_worked_10)
Prereg :299: n = 24, g = 6, U ... ok
test_worked_11 (__main__.SpecTests.test_worked_11)
Prereg :300: n = 33, gates, FIT, W1 1.4 ... ok
test_worked_12 (__main__.SpecTests.test_worked_12)
Prereg :301: n = 26, gates, subject-free hits A + 4 ... ok
test_worked_13 (__main__.SpecTests.test_worked_13)
Prereg :302: recipe A A7 = 19/72 ... ok
test_worked_14 (__main__.SpecTests.test_worked_14)
Prereg :303: Z3 (d): one greedy generation differs ... ok
test_worked_15 (__main__.SpecTests.test_worked_15)
Prereg :304: stage 2: n = 26, Z-band FIT, gates clean, capacity matched, n_b = 23 ... ok
test_worked_16 (__main__.SpecTests.test_worked_16)
Prereg :305: stage 2: n = 26, Z-band clean, n_b = 20 ... ok
test_worked_17 (__main__.SpecTests.test_worked_17)
Prereg :306: stage 2: n = 40, Z-band clean, n_b = 28 ... ok
test_worked_18 (__main__.SpecTests.test_worked_18)
Prereg :307: stage 2: n = 26, Z-band U (φ_μ = 0.61), n_b = 14 ... ok
test_worked_19 (__main__.SpecTests.test_worked_19)
Prereg :308: stage 2: n = 26, Z-band FIT, Z-band G7 fails, n_b = 24 ... ok
test_worked_20 (__main__.SpecTests.test_worked_20)
Prereg :309: stage 2: n = 22, Z-band clean, n_b = 17 ... ok
test_worked_21 (__main__.SpecTests.test_worked_21)
Prereg :310: stage 2: Z-band FIT, T = 144, B_Z = 2,304 > 2,200 ... ok
test_worked_22 (__main__.SpecTests.test_worked_22)
Prereg :311: n = 22, g = 10, gates, φ_μ = 0.958, φ_0^id = 24, actual `canon_full_n` = 0 ... ok
test_worked_23 (__main__.SpecTests.test_worked_23)
Prereg :312: n = 26, gates, FIT, W1 = 0.55 exactly ... ok
test_worked_24 (__main__.SpecTests.test_worked_24)
Prereg :313: stage 1: a synchronized round takes 121 s ... ok
test_z2_ambiguous_and_all_validity_gates (__main__.SpecTests.test_z2_ambiguous_and_all_validity_gates)
Prereg :149, :212–225: zero checked Z2 HALTs; V1–V13 each enforced. ... ok
test_B1_stage0_refuses_without_recorded_go_decision (__main__.Fix1Tests.test_B1_stage0_refuses_without_recorded_go_decision)
Prereg :3, :341–344: operator go before stage 0; blocking demo B1. ... ok
test_B2_stray_stage_call_after_terminal_K1_keeps_the_result (__main__.Fix1Tests.test_B2_stray_stage_call_after_terminal_K1_keeps_the_result)
Prereg :137, :204, :267: a refusal preserves completed records; blocking demo B2. ... HALTED-V12: duplicate, out-of-order, stale or closed stage call
ok
test_B3_clean_survivor_without_stage2_ceiling_keeps_stage1_record (__main__.Fix1Tests.test_B3_clean_survivor_without_stage2_ceiling_keeps_stage1_record)
Prereg :196, :265–267: unbudgeted expansion closes STAGE1; blocking demo B3 with lead's suffix ruling. ... HALTED-BUDGET: absent stage2 ceiling
ok
test_fix1_absent_ceilings_terminal_labels_and_resident_close (__main__.Fix1Tests.test_fix1_absent_ceilings_terminal_labels_and_resident_close)
Prereg :196, :265–267: clean stage1/2 without next budget terminates; no G0/replication claim. ... {"label": "PARTIAL-STAGE1", "base_label": "PARTIAL", "qualifiers": ["STAGE1"], "gates": {"G1": true, "G2": true, "G3": true, "G4": true, "G5": true, "G7": true}, "FIT": true, "n": 26, "a": 12, "gain": 14, "attribution": "NOT-RUN", "next_stage": null, "replicated": false, "lead_replicated": false, "artifact_identity": "NOT-EVALUATED", "numeric_behavioral_reproduction": "NOT-EVALUATED", "scientific_verdict": true}
ok
test_fix1_go_launch_copy_and_manifest_sha (__main__.Fix1Tests.test_fix1_go_launch_copy_and_manifest_sha)
Prereg :3, :137, :341–344: validated go copied to launch and its exact bytes bound to H_in. ... {"label": "NULL-STAGE1", "base_label": "NULL", "qualifiers": ["STAGE1"], "gates": {"G1": true, "G2": true, "G3": true, "G4": true, "G5": true, "G7": true}, "FIT": true, "n": 18, "a": 12, "gain": 6, "attribution": "NOT-RUN", "next_stage": null, "replicated": false, "lead_replicated": false, "artifact_identity": "NOT-EVALUATED", "numeric_behavioral_reproduction": "NOT-EVALUATED", "scientific_verdict": true}
ok
test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation. ... ok
test_fix1_go_sha_is_mandatory_reader_provenance (__main__.Fix1Tests.test_fix1_go_sha_is_mandatory_reader_provenance)
Prereg :137, V12 :224; §6 :341–344: missing/malformed go digest invalidates the manifest. ... ok
test_fix1_halt_sidecar_retains_completed_observations_for_both_processes (__main__.Fix1Tests.test_fix1_halt_sidecar_retains_completed_observations_for_both_processes)
Prereg :123, :267, :323: actual deadline/validity halts keep completed pass bytes and nonbinding observations. ... ok
test_fix1_refusals_preserve_finished_attempt_byte_for_byte (__main__.Fix1Tests.test_fix1_refusals_preserve_finished_attempt_byte_for_byte)
Prereg :137, :204, :267: duplicate/closed/out-of-order client refusals do not alter a finished attempt. ... HALTED-V12: attempt needs fresh OUT_DIR
HALTED-V12: duplicate, out-of-order, stale or closed stage call
HALTED-V12: duplicate, out-of-order, stale or closed stage call
HALTED-V12: stage3 requires clean completed K2 and closed process1
ok
test_fix1_relative_outdir_resolved_at_main_parse (__main__.Fix1Tests.test_fix1_relative_outdir_resolved_at_main_parse)
Prereg :8, :137, :204: records use one absolute OUT_DIR before the harness import changes cwd. ... ok
test_fix1_shell_preserves_go_env_absolute_outdir_and_no_refusal_write (__main__.Fix1Tests.test_fix1_shell_preserves_go_env_absolute_outdir_and_no_refusal_write)
Prereg :3, :137, :204: shell passes go unchanged and leaves unlaunched attempts untouched. ... ok
test_fix1_watchdog_preserves_last_published_record (__main__.Fix1Tests.test_fix1_watchdog_preserves_last_published_record)
Prereg :196, :225, :267: expired stage-2 watchdog preserves the complete earlier pass and labels HALT. ... ok
test_fix2_child_receives_parent_resolved_absolute_outdir (__main__.Fix2Tests.test_fix2_child_receives_parent_resolved_absolute_outdir)
Prereg :137, :204; fix2 item 1/O02: direct stage_call resolves the child path before cwd changes. ... ok
test_fix2_disqualified_missing_ceiling_is_k1_not_absent (__main__.Fix2Tests.test_fix2_disqualified_missing_ceiling_is_k1_not_absent)
Prereg :265, :272; B3g: a qualified PARTIAL/LEAD stops for K1 even without an expansion budget. ... ok
test_fix2_failed_resident_detection_closes_halt_and_keeps_passes (__main__.Fix2Tests.test_fix2_failed_resident_detection_closes_halt_and_keeps_passes)
Prereg :267, :323; D-C10z-fix1 (3): all wait_stage failed-resident detections publish a durable HALT. ... ok
test_fix2_go_nonfinite_constants_and_overflow_refused (__main__.Fix2Tests.test_fix2_go_nonfinite_constants_and_overflow_refused)
Prereg V6 :219, §6 :341–344; G11: nested NaN/Infinity and overflowing JSON numbers are refused without writes. ... ok
test_fix2_resident_stops_at_parent_halt_and_preserves_session_fields (__main__.Fix2Tests.test_fix2_resident_stops_at_parent_halt_and_preserves_session_fields)
Prereg :267, :323; item 2/H10/H11: a resumed resident sees the parent's halt at its next terminal check. ... ok
test_fix2_session_record_absent_ceiling_matches_reader_omissions (__main__.Fix2Tests.test_fix2_session_record_absent_ceiling_matches_reader_omissions)
Prereg :196, :265–267; B3d: the actual Session.record producer agrees with the independent reader. ... ok
test_fix2_z0_sigma_halts_in_driver_at_frozen_boundary (__main__.Fix2Tests.test_fix2_z0_sigma_halts_in_driver_at_frozen_boundary)
Prereg :147; A32: the real Z0 function permits sigma=.125 and halts above it before any reader. ... ok
test_z0_v5_halt_persists_native_and_full_sigma (__main__.Fix2Tests.test_z0_v5_halt_persists_native_and_full_sigma)
Diagnosability only: the unchanged V5 refusal publishes both measured maxima. ... ok
test_i_idle_expiry (__main__.IdleGapTests.test_i_idle_expiry) ... C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7200.0, "stage2": 200.0, "stage3": 7460.0}, "components_s": {"candidate_rounds": 1200.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 2760.0, "ceiling_s": 7200.0}}}
ok
test_ii_late_entry (__main__.IdleGapTests.test_ii_late_entry) ... C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7200.0, "stage2": 200.0, "stage3": 7460.0}, "components_s": {"candidate_rounds": 1200.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 2760.0, "ceiling_s": 7200.0}}}
ok
test_iii_deadline_samples (__main__.IdleGapTests.test_iii_deadline_samples) ... C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7200.0, "stage2": 200.0, "stage3": 7460.0}, "components_s": {"candidate_rounds": 1200.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 2760.0, "ceiling_s": 7200.0}}}
ok
test_iv_process2_envelope (__main__.IdleGapTests.test_iv_process2_envelope) ... C10Z_PROJECTION {"origins": {"stage01": 0.0, "stage3": 0.0}, "ceilings": {"stage01": 7200.0, "stage2": 200.0, "stage3": 7460.0}, "components_s": {"candidate_rounds": 1200.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 2760.0, "ceiling_s": 7200.0}, "stage3": {"elapsed_s": 0.0, "remaining_s": 2860.0, "ceiling_s": 7460.0}}}
ok
test_ix_transition_lock (__main__.IdleGapTests.test_ix_transition_lock) ... ok
test_v_complete01_only_enter (__main__.IdleGapTests.test_v_complete01_only_enter) ... ok
test_vi_mutation_deadlines (__main__.IdleGapTests.test_vi_mutation_deadlines) ... C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7200.0, "stage2": 200.0, "stage3": 7460.0}, "components_s": {"candidate_rounds": 1200.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 2760.0, "ceiling_s": 7200.0}}}
ok
test_vii_entry_invariant (__main__.IdleGapTests.test_vii_entry_invariant) ... C10Z_PROJECTION {"origins": {"stage01": 0.0, "stage3": 0.0}, "ceilings": {"stage01": 7200.0, "stage2": 200.0, "stage3": 7460.0}, "components_s": {"candidate_rounds": 1200.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 2760.0, "ceiling_s": 7200.0}, "stage3": {"elapsed_s": 0.0, "remaining_s": 2860.0, "ceiling_s": 7460.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0, "stage3": 0.0}, "ceilings": {"stage01": 7200.0, "stage2": 200.0, "stage3": 7460.0}, "components_s": {"candidate_rounds": 1200.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 2760.0, "ceiling_s": 7200.0}, "stage3": {"elapsed_s": 0.0, "remaining_s": 2860.0, "ceiling_s": 7460.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0, "stage3": 0.0}, "ceilings": {"stage01": 7200.0, "stage2": 200.0, "stage3": 7460.0}, "components_s": {"candidate_rounds": 1200.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 2760.0, "ceiling_s": 7200.0}, "stage3": {"elapsed_s": 0.0, "remaining_s": 2860.0, "ceiling_s": 7460.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0, "stage3": 0.0}, "ceilings": {"stage01": 7200.0, "stage2": 200.0, "stage3": 7460.0}, "components_s": {"candidate_rounds": 1200.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 2760.0, "ceiling_s": 7200.0}, "stage3": {"elapsed_s": 0.0, "remaining_s": 2860.0, "ceiling_s": 7460.0}}}
ok
test_viii_single_timestamp (__main__.IdleGapTests.test_viii_single_timestamp) ... ok
test_c01_neighbors (__main__.BudgetBoundTests.test_c01_neighbors) ... ok
test_huge_integer_refusal (__main__.BudgetBoundTests.test_huge_integer_refusal) ... ok
test_benchmark_template_digest_mismatch_refuses_before_launch (__main__.LaunchBindingTests.test_benchmark_template_digest_mismatch_refuses_before_launch)
D-C10z-v4fix: a valid selected benchmark with different templates refuses V12 before worker/output creation. ... ok
test_c01 (__main__.LaunchBindingTests.test_c01) ... ok
test_derived (__main__.LaunchBindingTests.test_derived) ... ok
test_environment (__main__.LaunchBindingTests.test_environment) ... ok
test_go_ceilings (__main__.LaunchBindingTests.test_go_ceilings) ... ok
test_go_fields (__main__.LaunchBindingTests.test_go_fields) ... ok
test_go_huge_integer_ceiling_refusal (__main__.LaunchBindingTests.test_go_huge_integer_ceiling_refusal) ... ok
test_inertness_counts (__main__.LaunchBindingTests.test_inertness_counts) ... ok
test_inertness_environment (__main__.LaunchBindingTests.test_inertness_environment) ... ok
test_inertness_json (__main__.LaunchBindingTests.test_inertness_json) ... ok
test_inertness_path (__main__.LaunchBindingTests.test_inertness_path) ... ok
test_inertness_required (__main__.LaunchBindingTests.test_inertness_required) ... ok
test_inertness_schema (__main__.LaunchBindingTests.test_inertness_schema) ... ok
test_inertness_sources (__main__.LaunchBindingTests.test_inertness_sources) ... ok
test_inertness_success (__main__.LaunchBindingTests.test_inertness_success) ... FAIL
test_inertness_verdict (__main__.LaunchBindingTests.test_inertness_verdict) ... ok
test_record_absolute (__main__.LaunchBindingTests.test_record_absolute) ... ok
test_record_invalid (__main__.LaunchBindingTests.test_record_invalid) ... ok
test_record_nonstrict (__main__.LaunchBindingTests.test_record_nonstrict) ... ok
test_record_optional_status (__main__.LaunchBindingTests.test_record_optional_status) ... ok
test_record_outside (__main__.LaunchBindingTests.test_record_outside) ... ok
test_record_required (__main__.LaunchBindingTests.test_record_required) ... ok
test_record_selection (__main__.LaunchBindingTests.test_record_selection) ... ok
test_record_unreadable (__main__.LaunchBindingTests.test_record_unreadable) ... ok
test_refused (__main__.LaunchBindingTests.test_refused) ... ok
test_script (__main__.LaunchBindingTests.test_script) ... ok
test_sources (__main__.LaunchBindingTests.test_sources) ... ok
test_stage2_override (__main__.LaunchBindingTests.test_stage2_override) ... ok
test_stage3_environment_drift (__main__.LaunchBindingTests.test_stage3_environment_drift) ... ok
test_stage3_inertness_drift (__main__.LaunchBindingTests.test_stage3_inertness_drift) ... ok
test_stage3_override (__main__.LaunchBindingTests.test_stage3_override) ... ok
test_stage3_record_drift (__main__.LaunchBindingTests.test_stage3_record_drift) ... ok
test_stage3_script_drift (__main__.LaunchBindingTests.test_stage3_script_drift) ... ok
test_stage3_source_drift (__main__.LaunchBindingTests.test_stage3_source_drift) ... ok
test_stage3_switch (__main__.LaunchBindingTests.test_stage3_switch) ... ok
test_stop (__main__.LaunchBindingTests.test_stop) ... ok
test_substitution (__main__.LaunchBindingTests.test_substitution) ... ok
test_success_roundtrip (__main__.LaunchBindingTests.test_success_roundtrip) ... FAIL
test_switch_empty (__main__.LaunchBindingTests.test_switch_empty) ... ok
test_switch_space (__main__.LaunchBindingTests.test_switch_space) ... ok
test_switch_true (__main__.LaunchBindingTests.test_switch_true) ... ok
test_switch_zero (__main__.LaunchBindingTests.test_switch_zero) ... ok
test_total (__main__.LaunchBindingTests.test_total) ... ok
test_benchmark_sha (__main__.ReaderBindingTests.test_benchmark_sha) ... ok
test_c01_neighbors (__main__.ReaderBindingTests.test_c01_neighbors) ... ok
test_go_ceilings (__main__.ReaderBindingTests.test_go_ceilings) ... ok
test_history_ceilings (__main__.ReaderBindingTests.test_history_ceilings) ... ok
test_huge_integer_refusal (__main__.ReaderBindingTests.test_huge_integer_refusal) ... ok
test_pass_launch (__main__.ReaderBindingTests.test_pass_launch) ... ok
test_process_ceilings (__main__.ReaderBindingTests.test_process_ceilings) ... ok
test_scope_ceiling (__main__.ReaderBindingTests.test_scope_ceiling) ... ok
test_attempt2_out_and_logs_preserve_attempt1 (__main__.WrapperTests.test_attempt2_out_and_logs_preserve_attempt1)
Prereg §10(d2): explicit attempt2 output, go/benchmark selection and both redirected logs preserve attempt1. ... ok
test_direct_scripts_executable_on_disk_and_git_index (__main__.WrapperTests.test_direct_scripts_executable_on_disk_and_git_index) ... ok
test_next_stage_types (__main__.WrapperTests.test_next_stage_types) ... ok
test_relative_out (__main__.WrapperTests.test_relative_out) ... ok
test_stage0_failure (__main__.WrapperTests.test_stage0_failure) ... ok
test_UTC_diagnostic_collision_refuses_exclusive_creation (__main__.TemplatePinTests.test_UTC_diagnostic_collision_refuses_exclusive_creation) ... ok
test_UTC_diagnostics_preserve_historical_records (__main__.TemplatePinTests.test_UTC_diagnostics_preserve_historical_records) ... ok
test_V4_resident_retains_templates_and_halt_hashes (__main__.TemplatePinTests.test_V4_resident_retains_templates_and_halt_hashes) ... C10Z_PROJECTION {"origins": {"stage01": 1325162.468082666}, "ceilings": {"stage01": 7800.0, "stage2": 12000.0, "stage3": 24000.0}, "components_s": {"recipe_A": 2040.0, "reference_D": 300.0, "G": 120.0, "verification_and_all_probes": 1380.0, "candidate_rounds": 1200.0, "serialization_and_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.000748584046959877, "remaining_s": 5220.0, "ceiling_s": 7800.0}}}
ok
test_cache_pinned_before_recipe_A_without_sampling (__main__.TemplatePinTests.test_cache_pinned_before_recipe_A_without_sampling) ... ok
test_existing_context_artifact_refusal_unchanged (__main__.TemplatePinTests.test_existing_context_artifact_refusal_unchanged) ... ok
test_manual_seed_zero_kept_before_harness_import (__main__.TemplatePinTests.test_manual_seed_zero_kept_before_harness_import) ... ok
test_process2_reuses_loaded_cache_before_baseline (__main__.TemplatePinTests.test_process2_reuses_loaded_cache_before_baseline) ... ok
test_scorer_template_identity_mismatch_refuses_before_recipe_A (__main__.TemplatePinTests.test_scorer_template_identity_mismatch_refuses_before_recipe_A) ... ok
test_selected_template_list_mismatch_refuses_before_recipe_A (__main__.TemplatePinTests.test_selected_template_list_mismatch_refuses_before_recipe_A) ... ok
test_templates_and_run_hash_written_before_LAW3_gate (__main__.TemplatePinTests.test_templates_and_run_hash_written_before_LAW3_gate) ... ok
test_templates_byte_equal_to_benchmark (__main__.TemplatePinTests.test_templates_byte_equal_to_benchmark) ... ok
test_amended_prereg_pin_shared_by_driver_reader_and_tests (__main__.PinTests.test_amended_prereg_pin_shared_by_driver_reader_and_tests) ... FAIL
test_temp_copy_byte_drift (__main__.PinTests.test_temp_copy_byte_drift) ... FAIL
test_on_off_science (__main__.TelemetryIntegrationTests.test_on_off_science) ... ok
test_placements_ast (__main__.TelemetryIntegrationTests.test_placements_ast) ... ok
test_resident_on_off (__main__.TelemetryIntegrationTests.test_resident_on_off) ... ok
test_resident_telemetry_failures_preserve_science (__main__.TelemetryIntegrationTests.test_resident_telemetry_failures_preserve_science) ... ok
test_write_telemetry_failures_preserve_science (__main__.TelemetryIntegrationTests.test_write_telemetry_failures_preserve_science) ... ok
test_probe_batch1_keeps_padding_and_captures_actual_position_ids (__main__.Z0ProbeTests.test_probe_batch1_keeps_padding_and_captures_actual_position_ids) ... ok
test_probe_cpu_json_pipeline_roundtrip_and_exclusive_output (__main__.Z0ProbeTests.test_probe_cpu_json_pipeline_roundtrip_and_exclusive_output) ... ERROR
test_probe_diff_statistics_subtract_in_cpu_float64 (__main__.Z0ProbeTests.test_probe_diff_statistics_subtract_in_cpu_float64) ... ok
test_probe_distinct_shape_controls_and_full_sigma_match_z0 (__main__.Z0ProbeTests.test_probe_distinct_shape_controls_and_full_sigma_match_z0) ... ok
test_probe_mutation_is_detected_without_restoring_weights (__main__.Z0ProbeTests.test_probe_mutation_is_detected_without_restoring_weights) ... ok
test_probe_native_mask_cli_default_and_ones (__main__.Z0ProbeTests.test_probe_native_mask_cli_default_and_ones) ... ok
test_probe_native_mask_option_changes_only_forward_kwargs (__main__.Z0ProbeTests.test_probe_native_mask_option_changes_only_forward_kwargs) ... ok
test_probe_native_prefix_leads_equal_real_z0 (__main__.Z0ProbeTests.test_probe_native_prefix_leads_equal_real_z0) ... ok
test_probe_never_writes_weights_or_calls_edit_recipe_sampling (__main__.Z0ProbeTests.test_probe_never_writes_weights_or_calls_edit_recipe_sampling) ... ok
test_probe_records_attention_backend_and_native_logit_bound (__main__.Z0ProbeTests.test_probe_records_attention_backend_and_native_logit_bound) ... ok
test_probe_refuses_existing_or_escaped_output_before_model_load (__main__.Z0ProbeTests.test_probe_refuses_existing_or_escaped_output_before_model_load) ... ok
test_probe_wrong_template_sha_refuses_before_model_load (__main__.Z0ProbeTests.test_probe_wrong_template_sha_refuses_before_model_load) ... FAIL
test_ast_guard_covers_all_unsafe_copy_api_forms (__main__.V5CopyTests.test_ast_guard_covers_all_unsafe_copy_api_forms) ... ok
test_astra_sources_no_combined_device_dtype_transfer_ast (__main__.V5CopyTests.test_astra_sources_no_combined_device_dtype_transfer_ast) ... ok
test_margin_leads_no_combined_device_dtype_transfer_ast (__main__.V5CopyTests.test_margin_leads_no_combined_device_dtype_transfer_ast) ... ok
test_mps_offset_view_corruption_and_exact_split_copy (__main__.V5CopyTests.test_mps_offset_view_corruption_and_exact_split_copy) ... skipped 'MPS unavailable: offset-view corruption reproduction UNVERIFIED'
test_mps_torch_cpu64_transfers_before_float64 (__main__.V5CopyTests.test_mps_torch_cpu64_transfers_before_float64) ... skipped 'MPS unavailable: float64 capture regression UNVERIFIED'
test_probe_native_and_full_rows_transfer_before_cast_ast (__main__.V5CopyTests.test_probe_native_and_full_rows_transfer_before_cast_ast) ... ok
test_target_probabilities_preserves_offset_float32_inputs (__main__.V5CopyTests.test_target_probabilities_preserves_offset_float32_inputs) ... ok
test_torch_cpu64_moves_to_cpu_before_float64_ast (__main__.V5CopyTests.test_torch_cpu64_moves_to_cpu_before_float64_ast) ... ok
test_T3_header_four_kinds_fields_and_full_cost_accounting (__main__.TelemetryUnitTests.test_T3_header_four_kinds_fields_and_full_cost_accounting) ... ok
test_T4_public_methods_avoid_science_clocks_and_gates (__main__.TelemetryUnitTests.test_T4_public_methods_avoid_science_clocks_and_gates) ... ok
test_T5a_directory_failure_is_disabled_once (__main__.TelemetryUnitTests.test_T5a_directory_failure_is_disabled_once) ... ok
test_T5a_initial_open_failure_is_disabled_once (__main__.TelemetryUnitTests.test_T5a_initial_open_failure_is_disabled_once) ... ok
test_T5b_write_failure_is_disabled_once (__main__.TelemetryUnitTests.test_T5b_write_failure_is_disabled_once) ... ok
test_T5c_flush_failure_is_disabled_once (__main__.TelemetryUnitTests.test_T5c_flush_failure_is_disabled_once) ... ok
test_T5d_fsync_failure_is_disabled_once (__main__.TelemetryUnitTests.test_T5d_fsync_failure_is_disabled_once) ... ok
test_T5e_keyboard_interrupt_propagates (__main__.TelemetryUnitTests.test_T5e_keyboard_interrupt_propagates) ... ok
test_T6_each_call_preserves_cpu_model_and_inputs (__main__.TelemetryUnitTests.test_T6_each_call_preserves_cpu_model_and_inputs) ... ok
test_T6_lens_uses_layer_output_top5_and_no_grad (__main__.TelemetryUnitTests.test_T6_lens_uses_layer_output_top5_and_no_grad) ... ok
test_T7_default_chunk_keeps_cpu_float32_under64MiB (__main__.TelemetryUnitTests.test_T7_default_chunk_keeps_cpu_float32_under64MiB) ... ok
test_T7_probabilities_dense_reference_and_row_chunk_bound (__main__.TelemetryUnitTests.test_T7_probabilities_dense_reference_and_row_chunk_bound) ... ok
test_T9_write_volume_no_requirement_lines (__main__.TelemetryUnitTests.test_T9_write_volume_no_requirement_lines) ... C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1200.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 2760.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1200.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 2760.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 7800.0}}}
ok
test_deterministic_three_pass_schedule_and_kwargs (__main__.TelemetryInertnessTests.test_deterministic_three_pass_schedule_and_kwargs) ... ok
test_full_greedy_suffix_count_and_compare (__main__.TelemetryInertnessTests.test_full_greedy_suffix_count_and_compare) ... ok
test_lens_sensitive_batch_is_not_inert (__main__.TelemetryInertnessTests.test_lens_sensitive_batch_is_not_inert) ... ok
test_lens_sensitive_probe_is_not_inert (__main__.TelemetryInertnessTests.test_lens_sensitive_probe_is_not_inert) ... ok
test_plain_drift_is_nondeterministic_baseline (__main__.TelemetryInertnessTests.test_plain_drift_is_nondeterministic_baseline) ... ok
test_runner_checks_all36_weights_and_invalid_is_exit2 (__main__.TelemetryRunnerTests.test_runner_checks_all36_weights_and_invalid_is_exit2) ... ok
test_runner_driver_module_reused (__main__.TelemetryRunnerTests.test_runner_driver_module_reused) ... ok
test_runner_import_is_stdlib_only (__main__.TelemetryRunnerTests.test_runner_import_is_stdlib_only) ... ok
test_runner_refuses_outside_and_existing_record_without_forward (__main__.TelemetryRunnerTests.test_runner_refuses_outside_and_existing_record_without_forward) ... ok
test_runner_refuses_relative_out_path (__main__.TelemetryRunnerTests.test_runner_refuses_relative_out_path) ... ok
test_runner_roundtrip_identity_and_no_write_engine_calls (__main__.TelemetryRunnerTests.test_runner_roundtrip_identity_and_no_write_engine_calls) ... ok

======================================================================
ERROR: test_review_stage_call_refusals (__main__.SpecTests.test_review_stage_call_refusals)
Prereg :133, :137, :196, :266: fresh OUT_DIR, K1/K2 and absent-ceiling refusals happen before any launch.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1675, in verify_launch_binding
    R.require(binding==launch["benchmark"],"HALTED-V12","benchmark binding")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_read.py", line 40, in require
    raise Halt(code,detail)
c10z_astra_read.Halt: HALTED-V12: benchmark binding

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1212, in _review_stage_calls_with_go
    return _proposed_stage_calls(self)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1091, in test_review_stage_call_refusals
    self.assertEqual(D.stage_call(3, good), 0); self.assertEqual(launched, ["p2"]); launched.clear()
                     ^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1838, in stage_call
    verify_launch_binding(run["launch"],os.environ)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1684, in verify_launch_binding
    raise R.Halt("HALTED-V12","launch binding changed since stage 0: "+str(exc)) from exc
c10z_astra_read.Halt: HALTED-V12: launch binding changed since stage 0: HALTED-V12: benchmark binding

======================================================================
ERROR: test_probe_cpu_json_pipeline_roundtrip_and_exclusive_output (__main__.Z0ProbeTests.test_probe_cpu_json_pipeline_roundtrip_and_exclusive_output)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 3581, in test_probe_cpu_json_pipeline_roundtrip_and_exclusive_output
    self.assertEqual(self.P.run(out), 0)
                     ^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_z0_probe.py", line 223, in run
    started = time.monotonic(); out = validate_output(out)
                                      ^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_z0_probe.py", line 27, in validate_output
    raise ValueError("out dir must be absolute under results/c10z_astra_z0_probe/<UTC>/ without symlinks")
ValueError: out dir must be absolute under results/c10z_astra_z0_probe/<UTC>/ without symlinks

======================================================================
FAIL: test_json_real_writer_and_frozen_sources (__main__.SpecTests.test_json_real_writer_and_frozen_sources)
Prereg :137, :204, :219, :224: round-trip, immutable outputs, finite science.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 781, in test_json_real_writer_and_frozen_sources
    self.assertEqual(hashlib.sha256((ROOT/"docs/C10Z_ASTRA_PREREG.md").read_bytes()).hexdigest(),PREREG)
AssertionError: '7aedd4ace95d2611bf398768df63cb60df6fce5afc23cf23209497bcd1d17a29' != '7c6e52e274e3dbc30cd5123d6b56ae8c9b1dca8c5e7507ff7be15d57e845059d'
- 7aedd4ace95d2611bf398768df63cb60df6fce5afc23cf23209497bcd1d17a29
+ 7c6e52e274e3dbc30cd5123d6b56ae8c9b1dca8c5e7507ff7be15d57e845059d


======================================================================
FAIL: test_inertness_success (__main__.LaunchBindingTests.test_inertness_success)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 2270, in test_inertness_success
    self.assertEqual(self.launched[-1]["telemetry_inertness"], {"path": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
AssertionError: {'path': '/private/var/folders/p7/s31_tv0s2wd81chns8[157 chars]0f1'} != {'path': '/var/folders/p7/s31_tv0s2wd81chns8v7gsyw00[149 chars]0f1'}
- {'path': '/private/var/folders/p7/s31_tv0s2wd81chns8v7gsyw0000gn/T/tmpqedst4px/results/c10z_astra_telemetry_inertness/T/inertness.json',
?           --------

+ {'path': '/var/folders/p7/s31_tv0s2wd81chns8v7gsyw0000gn/T/tmpqedst4px/results/c10z_astra_telemetry_inertness/T/inertness.json',
   'sha256': '0a0653d38e618f465afb6d96fc51a3206b53337e34fccfc6bb4303dd149b70f1'}

======================================================================
FAIL: test_success_roundtrip (__main__.LaunchBindingTests.test_success_roundtrip)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 2160, in test_success_roundtrip
    self.assertEqual(launch["benchmark"], _selected_launch(self.path, self.binding)["benchmark"])
AssertionError: {'path': '/private/var/folders/p7/s31_tv0s2wd81chns8[1615 chars]fa0'} != {'path': '/var/folders/p7/s31_tv0s2wd81chns8v7gsyw00[1607 chars]460}}
Diff is 2073 characters long. Set self.maxDiff to None to see it.

======================================================================
FAIL: test_amended_prereg_pin_shared_by_driver_reader_and_tests (__main__.PinTests.test_amended_prereg_pin_shared_by_driver_reader_and_tests)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 2621, in test_amended_prereg_pin_shared_by_driver_reader_and_tests
    self.assertEqual(actual, "7c6e52e274e3dbc30cd5123d6b56ae8c9b1dca8c5e7507ff7be15d57e845059d")
AssertionError: '7aedd4ace95d2611bf398768df63cb60df6fce5afc23cf23209497bcd1d17a29' != '7c6e52e274e3dbc30cd5123d6b56ae8c9b1dca8c5e7507ff7be15d57e845059d'
- 7aedd4ace95d2611bf398768df63cb60df6fce5afc23cf23209497bcd1d17a29
+ 7c6e52e274e3dbc30cd5123d6b56ae8c9b1dca8c5e7507ff7be15d57e845059d


======================================================================
FAIL: test_temp_copy_byte_drift (__main__.PinTests.test_temp_copy_byte_drift)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 2628, in test_temp_copy_byte_drift
    check(ROOT / "docs/C10Z_ASTRA_PREREG.md")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 2627, in check
    def check(path): self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), PREREG)
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: '7aedd4ace95d2611bf398768df63cb60df6fce5afc23cf23209497bcd1d17a29' != '7c6e52e274e3dbc30cd5123d6b56ae8c9b1dca8c5e7507ff7be15d57e845059d'
- 7aedd4ace95d2611bf398768df63cb60df6fce5afc23cf23209497bcd1d17a29
+ 7c6e52e274e3dbc30cd5123d6b56ae8c9b1dca8c5e7507ff7be15d57e845059d


======================================================================
FAIL: test_probe_wrong_template_sha_refuses_before_model_load (__main__.Z0ProbeTests.test_probe_wrong_template_sha_refuses_before_model_load)
----------------------------------------------------------------------
ValueError: out dir must be absolute under results/c10z_astra_z0_probe/<UTC>/ without symlinks

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 3515, in test_probe_wrong_template_sha_refuses_before_model_load
    with self.assertRaisesRegex(ValueError, "template.*sha256"): self.P.run(out)
AssertionError: "template.*sha256" does not match "out dir must be absolute under results/c10z_astra_z0_probe/<UTC>/ without symlinks"

----------------------------------------------------------------------
Ran 209 tests in 156.544s

FAILED (failures=6, errors=2, skipped=2)
C10Z_ASTRA_SELFTEST_FAIL tests=209
```

### Initial existing benchmark baseline

Captured `/private/tmp/c10z_v7diag_build/baseline_benchmark.txt`; exit status `0`.

```text
CPU_ONLY: MPS availability forced false; unmocked MPS calls forbidden; no model load
test_eight_v3_calibration_cases (__main__.BenchmarkCeilingTests.test_eight_v3_calibration_cases) ... ok
test_exact_rounding_and_c01_stop_boundary (__main__.BenchmarkCeilingTests.test_exact_rounding_and_c01_stop_boundary) ... ok
test_mean_outlier_and_complete_eval_tstar (__main__.BenchmarkCeilingTests.test_mean_outlier_and_complete_eval_tstar) ... ok
test_optional_minima_and_timeout_lower_bound (__main__.BenchmarkCeilingTests.test_optional_minima_and_timeout_lower_bound) ... ok
test_raw_values_drive_all_terms (__main__.BenchmarkCeilingTests.test_raw_values_drive_all_terms) ... ok
test_refused_records_never_fallback_or_numbers (__main__.BenchmarkCeilingTests.test_refused_records_never_fallback_or_numbers) ... ok
test_environment_identity_metadata_only (__main__.BenchmarkIdentityTests.test_environment_identity_metadata_only) ... ok
test_environment_identity_no_torch_subprocess (__main__.BenchmarkIdentityTests.test_environment_identity_no_torch_subprocess) ... ok
test_source_identity_exact_order_and_root (__main__.BenchmarkIdentityTests.test_source_identity_exact_order_and_root) ... ok
test_top_level_import_stdlib_only_subprocess (__main__.BenchmarkIdentityTests.test_top_level_import_stdlib_only_subprocess) ... ok
test_env_preflight_refusals (__main__.BenchmarkLifecycleTests.test_env_preflight_refusals) ... ok
test_injected_worker_full_schedule_no_writer_calls (__main__.BenchmarkLifecycleTests.test_injected_worker_full_schedule_no_writer_calls) ... C10Z_PROBE_POPULATION {"arm": "A7_coined_coined", "sha256": "02af6172c2ce331a98cd0b6aeee0b656f6062050caf228fa2be50048d6938aaa", "counts": {"F0": 36, "prefix": 3888, "subject_free": 108, "relations": 48}}
ok
test_injected_worker_synthetic_mps_identity_validates_derived (__main__.BenchmarkLifecycleTests.test_injected_worker_synthetic_mps_identity_validates_derived) ... C10Z_PROBE_POPULATION {"arm": "A7_coined_coined", "sha256": "02af6172c2ce331a98cd0b6aeee0b656f6062050caf228fa2be50048d6938aaa", "counts": {"F0": 36, "prefix": 3888, "subject_free": 108, "relations": 48}}
ok
test_optional_skip_keeps_top_level_status (__main__.BenchmarkLifecycleTests.test_optional_skip_keeps_top_level_status) ... C10Z_PROBE_POPULATION {"arm": "A7_coined_coined", "sha256": "02af6172c2ce331a98cd0b6aeee0b656f6062050caf228fa2be50048d6938aaa", "counts": {"F0": 36, "prefix": 3888, "subject_free": 108, "relations": 48}}
ok
test_out_path_refusals_and_prefix_trap (__main__.BenchmarkLifecycleTests.test_out_path_refusals_and_prefix_trap) ... ok
test_start_and_phase_fit_boundaries (__main__.BenchmarkLifecycleTests.test_start_and_phase_fit_boundaries) ... ok
test_supervisor_600_boundary_fake_clock (__main__.BenchmarkLifecycleTests.test_supervisor_600_boundary_fake_clock) ... ok
test_supervisor_completed_worker_untouched (__main__.BenchmarkLifecycleTests.test_supervisor_completed_worker_untouched) ... ok
test_supervisor_existing_record_cap_preserves_bytes (__main__.BenchmarkLifecycleTests.test_supervisor_existing_record_cap_preserves_bytes) ... ok
test_supervisor_forbidden_astra_cap_preserves_directory (__main__.BenchmarkLifecycleTests.test_supervisor_forbidden_astra_cap_preserves_directory) ... ok
test_supervisor_outside_benchmark_cap_preserves_directory (__main__.BenchmarkLifecycleTests.test_supervisor_outside_benchmark_cap_preserves_directory) ... ok
test_supervisor_real_process_group_kill_and_interrupted_record (__main__.BenchmarkLifecycleTests.test_supervisor_real_process_group_kill_and_interrupted_record) ... ok
test_svd_timeout_565_lower_bound_and_worker_survival (__main__.BenchmarkLifecycleTests.test_svd_timeout_565_lower_bound_and_worker_survival) ... ok
test_system_wide_monotonic_subprocess (__main__.BenchmarkLifecycleTests.test_system_wide_monotonic_subprocess) ... ok
test_worker_guard_status_bands_and_reserved_after_hash (__main__.BenchmarkLifecycleTests.test_worker_guard_status_bands_and_reserved_after_hash) ... C10Z_PROBE_POPULATION {"arm": "A7_coined_coined", "sha256": "02af6172c2ce331a98cd0b6aeee0b656f6062050caf228fa2be50048d6938aaa", "counts": {"F0": 36, "prefix": 3888, "subject_free": 108, "relations": 48}}
C10Z_PROBE_POPULATION {"arm": "A7_coined_coined", "sha256": "02af6172c2ce331a98cd0b6aeee0b656f6062050caf228fa2be50048d6938aaa", "counts": {"F0": 36, "prefix": 3888, "subject_free": 108, "relations": 48}}
C10Z_PROBE_POPULATION {"arm": "A7_coined_coined", "sha256": "02af6172c2ce331a98cd0b6aeee0b656f6062050caf228fa2be50048d6938aaa", "counts": {"F0": 36, "prefix": 3888, "subject_free": 108, "relations": 48}}
ok
test_worker_load_over_300_invalid (__main__.BenchmarkLifecycleTests.test_worker_load_over_300_invalid) ... ok
test_worker_mutation_invalid_and_refused (__main__.BenchmarkLifecycleTests.test_worker_mutation_invalid_and_refused) ... C10Z_PROBE_POPULATION {"arm": "A7_coined_coined", "sha256": "02af6172c2ce331a98cd0b6aeee0b656f6062050caf228fa2be50048d6938aaa", "counts": {"F0": 36, "prefix": 3888, "subject_free": 108, "relations": 48}}
ok
test_worker_svd_timeout_preserves_complete_and_capped (__main__.BenchmarkLifecycleTests.test_worker_svd_timeout_preserves_complete_and_capped) ... C10Z_PROBE_POPULATION {"arm": "A7_coined_coined", "sha256": "02af6172c2ce331a98cd0b6aeee0b656f6062050caf228fa2be50048d6938aaa", "counts": {"F0": 36, "prefix": 3888, "subject_free": 108, "relations": 48}}
C10Z_PROBE_POPULATION {"arm": "A7_coined_coined", "sha256": "02af6172c2ce331a98cd0b6aeee0b656f6062050caf228fa2be50048d6938aaa", "counts": {"F0": 36, "prefix": 3888, "subject_free": 108, "relations": 48}}
ok
test_empty_population_leaves_no_heartbeat (__main__.BenchmarkPopulationTests.test_empty_population_leaves_no_heartbeat) ... ok
test_full_population_forward_counts (__main__.BenchmarkPopulationTests.test_full_population_forward_counts) ... C10Z_PROBE_POPULATION {"arm": "A7_coined_coined", "sha256": "02af6172c2ce331a98cd0b6aeee0b656f6062050caf228fa2be50048d6938aaa", "counts": {"F0": 36, "prefix": 3888, "subject_free": 108, "relations": 48}}
C10Z_PROBE_POPULATION {"arm": "A7_coined_coined", "sha256": "286257b9d4f116fd9d47b617a27c81f2258b70e40b1b72ac1cb7389ad59992d4", "counts": {"F0": 36, "prefix": 3888, "subject_free": 108, "relations": 48}}
ok
test_greedy_argmax_and_no_grad (__main__.BenchmarkPopulationTests.test_greedy_argmax_and_no_grad) ... ok
test_guarded_loop_completes_item_then_stops (__main__.BenchmarkPopulationTests.test_guarded_loop_completes_item_then_stops) ... ok
test_guarded_warmup_records_actual_count (__main__.BenchmarkPopulationTests.test_guarded_warmup_records_actual_count) ... ok
test_population_batch_and_digest_match_driver (__main__.BenchmarkPopulationTests.test_population_batch_and_digest_match_driver) ... C10Z_PROBE_POPULATION {"arm": "A7_coined_coined", "sha256": "02af6172c2ce331a98cd0b6aeee0b656f6062050caf228fa2be50048d6938aaa", "counts": {"F0": 36, "prefix": 3888, "subject_free": 108, "relations": 48}}
C10Z_PROBE_POPULATION {"arm": "A7_coined_coined", "sha256": "02af6172c2ce331a98cd0b6aeee0b656f6062050caf228fa2be50048d6938aaa", "counts": {"F0": 36, "prefix": 3888, "subject_free": 108, "relations": 48}}
ok
test_timed_reads_heartbeat_and_warmup_exclusion (__main__.BenchmarkPopulationTests.test_timed_reads_heartbeat_and_warmup_exclusion) ... ok
test_huge_integer_timing_is_value_error (__main__.BenchmarkRecordTests.test_huge_integer_timing_is_value_error) ... ok
test_interrupted_replace_preserves_prior_record (__main__.BenchmarkRecordTests.test_interrupted_replace_preserves_prior_record) ... ok
test_measurement_consistency_rejections (__main__.BenchmarkRecordTests.test_measurement_consistency_rejections) ... ok
test_nan_preserves_prior_record (__main__.BenchmarkRecordTests.test_nan_preserves_prior_record) ... ok
test_nonfinite_statistics_rejected (__main__.BenchmarkRecordTests.test_nonfinite_statistics_rejected) ... ok
test_optional_status_container_is_value_error (__main__.BenchmarkRecordTests.test_optional_status_container_is_value_error) ... ok
test_probe_status_boundaries (__main__.BenchmarkRecordTests.test_probe_status_boundaries) ... ok
test_quantiles_and_statistics (__main__.BenchmarkRecordTests.test_quantiles_and_statistics) ... ok
test_schema_missing_keys_and_wrong_types (__main__.BenchmarkRecordTests.test_schema_missing_keys_and_wrong_types) ... ok
test_strict_atomic_roundtrip_with_identity (__main__.BenchmarkRecordTests.test_strict_atomic_roundtrip_with_identity) ... ok
test_target_lengths_population_and_probe_counts (__main__.BenchmarkRecordTests.test_target_lengths_population_and_probe_counts) ... ok
test_weights_device_dtype_revision_fingerprint_rejections (__main__.BenchmarkRecordTests.test_weights_device_dtype_revision_fingerprint_rejections) ... ok

----------------------------------------------------------------------
Ran 47 tests in 3.148s

OK
C10Z_BENCH_SELFTEST_PASS tests=47
```

### Initial25 new tests before implementation; twenty failures and one retention error corrected to assertion in final RED

Captured `/private/tmp/c10z_v7diag_build/diag_red.txt`; exit status `1`.

```text
CPU_ONLY: MPS availability forced false; unmocked MPS calls forbidden; no model load
test_OS_timer_terminates_sleep_and_native_GIL_hold_retains_inconclusive (__main__.DeadlineTests.test_OS_timer_terminates_sleep_and_native_GIL_hold_retains_inconclusive) ... FAIL
test_immutable_3060_includes_preimport_and_exact_boundary (__main__.DeadlineTests.test_immutable_3060_includes_preimport_and_exact_boundary) ... FAIL
test_forced_V7_failure_retains_value_and_provenance_before_G_and_scoring (__main__.PersistenceCorrectionTests.test_forced_V7_failure_retains_value_and_provenance_before_G_and_scoring) ... FAIL
test_forced_pass_outputs_checks_identical_to_frozen_previous_behavior (__main__.PersistenceCorrectionTests.test_forced_pass_outputs_checks_identical_to_frozen_previous_behavior) ... ok
test_fresh_and_process2_existing_dstats_refuse_overwrite (__main__.PersistenceCorrectionTests.test_fresh_and_process2_existing_dstats_refuse_overwrite) ... ok
test_process2_exact_input_bytes_retained_on_fail_and_pass (__main__.PersistenceCorrectionTests.test_process2_exact_input_bytes_retained_on_fail_and_pass) ... 
  test_process2_exact_input_bytes_retained_on_fail_and_pass (__main__.PersistenceCorrectionTests.test_process2_exact_input_bytes_retained_on_fail_and_pass) (fail=True) ... ERROR
test_all_pins_include_every_population_before_forwards (__main__.PinsAndAdmissionTests.test_all_pins_include_every_population_before_forwards) ... FAIL
test_launcher_existing_namespace_fingerprint_gpu_refuse_before_exec (__main__.PinsAndAdmissionTests.test_launcher_existing_namespace_fingerprint_gpu_refuse_before_exec) ... FAIL
test_launcher_success_exec_explicit_worktree_and_no_other_gate (__main__.PinsAndAdmissionTests.test_launcher_success_exec_explicit_worktree_and_no_other_gate) ... FAIL
test_local_arrow_revision_length_shards_and_offline_only (__main__.PinsAndAdmissionTests.test_local_arrow_revision_length_shards_and_offline_only) ... FAIL
test_namespace_refuses_reuse_and_attempt3_path (__main__.PinsAndAdmissionTests.test_namespace_refuses_reuse_and_attempt3_path) ... FAIL
test_F_pass_stops_and_random_pass_never_measures_R5000 (__main__.ProbePipelineTests.test_F_pass_stops_and_random_pass_never_measures_R5000) ... FAIL
test_R5000_independent_conditional_A2_and_D (__main__.ProbePipelineTests.test_R5000_independent_conditional_A2_and_D) ... FAIL
test_incomplete_failure_retains_prior_m_and_no_selection (__main__.ProbePipelineTests.test_incomplete_failure_retains_prior_m_and_no_selection) ... FAIL
test_scoring_deadline_cannot_publish_A1_or_increase_cap (__main__.ProbePipelineTests.test_scoring_deadline_cannot_publish_A1_or_increase_cap) ... FAIL
test_tensor_exclusive_flush_fsync_and_provenance (__main__.ProbePipelineTests.test_tensor_exclusive_flush_fsync_and_provenance) ... FAIL
test_cache_diagonal_count_and_loaded_once (__main__.SelectionAndScoringTests.test_cache_diagonal_count_and_loaded_once) ... FAIL
test_full_seed_one_permutation_and_exact_population_sizes (__main__.SelectionAndScoringTests.test_full_seed_one_permutation_and_exact_population_sizes) ... FAIL
test_ordered_routing_equal_boundary_nonfinite_and_report_only_E (__main__.SelectionAndScoringTests.test_ordered_routing_equal_boundary_nonfinite_and_report_only_E) ... FAIL
test_scoring_uses_driver_spearman_ties_natural_log_and_zero_inf (__main__.SelectionAndScoringTests.test_scoring_uses_driver_spearman_ties_natural_log_and_zero_inf) ... FAIL
test_actual_driver_bit_identity_and_independent_tokens_counts_normalization (__main__.StatisticTests.test_actual_driver_bit_identity_and_independent_tokens_counts_normalization) ... FAIL
test_ast_identity_sums_and_loop_only_row_count_varies (__main__.StatisticTests.test_ast_identity_sums_and_loop_only_row_count_varies) ... FAIL
test_hook_cleanup_after_forward_error (__main__.StatisticTests.test_hook_cleanup_after_forward_error) ... FAIL

======================================================================
ERROR: test_process2_exact_input_bytes_retained_on_fail_and_pass (__main__.PersistenceCorrectionTests.test_process2_exact_input_bytes_retained_on_fail_and_pass) (fail=True)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 449, in test_process2_exact_input_bytes_retained_on_fail_and_pass
    self.assertEqual((out / "dstats.pt").read_bytes(), (source / "dstats.pt").read_bytes())
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/pathlib.py", line 1050, in read_bytes
    with self.open(mode='rb') as f:
         ^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/pathlib.py", line 1044, in open
    return io.open(self, mode, buffering, encoding, errors, newline)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
FileNotFoundError: [Errno 2] No such file or directory: '/private/tmp/c10z_v7diag_build/tmpotf9d1b9/out/dstats.pt'

======================================================================
FAIL: test_OS_timer_terminates_sleep_and_native_GIL_hold_retains_inconclusive (__main__.DeadlineTests.test_OS_timer_terminates_sleep_and_native_GIL_hold_retains_inconclusive)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 380, in test_OS_timer_terminates_sleep_and_native_GIL_hold_retains_inconclusive
    P = probe(self)
        ^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 34, in probe
    test.assertTrue(path.is_file(), "missing forward-only V7-DIAG implementation")
AssertionError: False is not true : missing forward-only V7-DIAG implementation

======================================================================
FAIL: test_immutable_3060_includes_preimport_and_exact_boundary (__main__.DeadlineTests.test_immutable_3060_includes_preimport_and_exact_boundary)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 372, in test_immutable_3060_includes_preimport_and_exact_boundary
    P = probe(self); now = [0.]; budget = P.Deadline(start=0., clock=lambda: now[0])
        ^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 34, in probe
    test.assertTrue(path.is_file(), "missing forward-only V7-DIAG implementation")
AssertionError: False is not true : missing forward-only V7-DIAG implementation

======================================================================
FAIL: test_forced_V7_failure_retains_value_and_provenance_before_G_and_scoring (__main__.PersistenceCorrectionTests.test_forced_V7_failure_retains_value_and_provenance_before_G_and_scoring)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 424, in test_forced_V7_failure_retains_value_and_provenance_before_G_and_scoring
    with self.assertRaisesRegex(D.R.Halt, "HALTED-V7"): s.prepare_instruments()
                                                        ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1092, in prepare_instruments
    self.dstats=self.compute_dstats();self.G=self.compute_G()
                                             ^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 422, in g
    def g(): self.assertTrue((out / "dstats.pt").is_file(), "dstats missing immediately after obtain"); return compute_G()
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: False is not true : dstats missing immediately after obtain

======================================================================
FAIL: test_all_pins_include_every_population_before_forwards (__main__.PinsAndAdmissionTests.test_all_pins_include_every_population_before_forwards)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 301, in test_all_pins_include_every_population_before_forwards
    P = probe(self)
        ^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 34, in probe
    test.assertTrue(path.is_file(), "missing forward-only V7-DIAG implementation")
AssertionError: False is not true : missing forward-only V7-DIAG implementation

======================================================================
FAIL: test_launcher_existing_namespace_fingerprint_gpu_refuse_before_exec (__main__.PinsAndAdmissionTests.test_launcher_existing_namespace_fingerprint_gpu_refuse_before_exec)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 333, in test_launcher_existing_namespace_fingerprint_gpu_refuse_before_exec
    self.assertTrue(path.is_file(), "missing exclusivity launcher")
AssertionError: False is not true : missing exclusivity launcher

======================================================================
FAIL: test_launcher_success_exec_explicit_worktree_and_no_other_gate (__main__.PinsAndAdmissionTests.test_launcher_success_exec_explicit_worktree_and_no_other_gate)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 348, in test_launcher_success_exec_explicit_worktree_and_no_other_gate
    path = ROOT / "tools/run_c10z_v7_diag.py"; self.assertTrue(path.is_file(), "missing launcher")
                                               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: False is not true : missing launcher

======================================================================
FAIL: test_local_arrow_revision_length_shards_and_offline_only (__main__.PinsAndAdmissionTests.test_local_arrow_revision_length_shards_and_offline_only)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 277, in test_local_arrow_revision_length_shards_and_offline_only
    P = probe(self)
        ^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 34, in probe
    test.assertTrue(path.is_file(), "missing forward-only V7-DIAG implementation")
AssertionError: False is not true : missing forward-only V7-DIAG implementation

======================================================================
FAIL: test_namespace_refuses_reuse_and_attempt3_path (__main__.PinsAndAdmissionTests.test_namespace_refuses_reuse_and_attempt3_path)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 361, in test_namespace_refuses_reuse_and_attempt3_path
    P = probe(self)
        ^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 34, in probe
    test.assertTrue(path.is_file(), "missing forward-only V7-DIAG implementation")
AssertionError: False is not true : missing forward-only V7-DIAG implementation

======================================================================
FAIL: test_F_pass_stops_and_random_pass_never_measures_R5000 (__main__.ProbePipelineTests.test_F_pass_stops_and_random_pass_never_measures_R5000)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 240, in test_F_pass_stops_and_random_pass_never_measures_R5000
    out, result, actual = self.pipeline(case)
                          ^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 209, in pipeline
    P = probe(self); tmp = tempfile.TemporaryDirectory(); self.addCleanup(tmp.cleanup)
        ^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 34, in probe
    test.assertTrue(path.is_file(), "missing forward-only V7-DIAG implementation")
AssertionError: False is not true : missing forward-only V7-DIAG implementation

======================================================================
FAIL: test_R5000_independent_conditional_A2_and_D (__main__.ProbePipelineTests.test_R5000_independent_conditional_A2_and_D)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 246, in test_R5000_independent_conditional_A2_and_D
    out, result, names = self.pipeline({"F1000": .79, "R1000": .79, "R5000": value})
                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 209, in pipeline
    P = probe(self); tmp = tempfile.TemporaryDirectory(); self.addCleanup(tmp.cleanup)
        ^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 34, in probe
    test.assertTrue(path.is_file(), "missing forward-only V7-DIAG implementation")
AssertionError: False is not true : missing forward-only V7-DIAG implementation

======================================================================
FAIL: test_incomplete_failure_retains_prior_m_and_no_selection (__main__.ProbePipelineTests.test_incomplete_failure_retains_prior_m_and_no_selection)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 251, in test_incomplete_failure_retains_prior_m_and_no_selection
    out, result, names = self.pipeline({"F1000": .79}, fault="R1000")
                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 209, in pipeline
    P = probe(self); tmp = tempfile.TemporaryDirectory(); self.addCleanup(tmp.cleanup)
        ^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 34, in probe
    test.assertTrue(path.is_file(), "missing forward-only V7-DIAG implementation")
AssertionError: False is not true : missing forward-only V7-DIAG implementation

======================================================================
FAIL: test_scoring_deadline_cannot_publish_A1_or_increase_cap (__main__.ProbePipelineTests.test_scoring_deadline_cannot_publish_A1_or_increase_cap)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 257, in test_scoring_deadline_cannot_publish_A1_or_increase_cap
    out, result, names = self.pipeline({"F1000": .79, "R1000": .8}, late="R1000")
                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 209, in pipeline
    P = probe(self); tmp = tempfile.TemporaryDirectory(); self.addCleanup(tmp.cleanup)
        ^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 34, in probe
    test.assertTrue(path.is_file(), "missing forward-only V7-DIAG implementation")
AssertionError: False is not true : missing forward-only V7-DIAG implementation

======================================================================
FAIL: test_tensor_exclusive_flush_fsync_and_provenance (__main__.ProbePipelineTests.test_tensor_exclusive_flush_fsync_and_provenance)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 262, in test_tensor_exclusive_flush_fsync_and_provenance
    P = probe(self)
        ^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 34, in probe
    test.assertTrue(path.is_file(), "missing forward-only V7-DIAG implementation")
AssertionError: False is not true : missing forward-only V7-DIAG implementation

======================================================================
FAIL: test_cache_diagonal_count_and_loaded_once (__main__.SelectionAndScoringTests.test_cache_diagonal_count_and_loaded_once)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 195, in test_cache_diagonal_count_and_loaded_once
    P = probe(self)
        ^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 34, in probe
    test.assertTrue(path.is_file(), "missing forward-only V7-DIAG implementation")
AssertionError: False is not true : missing forward-only V7-DIAG implementation

======================================================================
FAIL: test_full_seed_one_permutation_and_exact_population_sizes (__main__.SelectionAndScoringTests.test_full_seed_one_permutation_and_exact_population_sizes)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 161, in test_full_seed_one_permutation_and_exact_population_sizes
    P = probe(self); actual = P.population_indices(5017)
        ^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 34, in probe
    test.assertTrue(path.is_file(), "missing forward-only V7-DIAG implementation")
AssertionError: False is not true : missing forward-only V7-DIAG implementation

======================================================================
FAIL: test_ordered_routing_equal_boundary_nonfinite_and_report_only_E (__main__.SelectionAndScoringTests.test_ordered_routing_equal_boundary_nonfinite_and_report_only_E)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 167, in test_ordered_routing_equal_boundary_nonfinite_and_report_only_E
    P = probe(self)
        ^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 34, in probe
    test.assertTrue(path.is_file(), "missing forward-only V7-DIAG implementation")
AssertionError: False is not true : missing forward-only V7-DIAG implementation

======================================================================
FAIL: test_scoring_uses_driver_spearman_ties_natural_log_and_zero_inf (__main__.SelectionAndScoringTests.test_scoring_uses_driver_spearman_ties_natural_log_and_zero_inf)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 181, in test_scoring_uses_driver_spearman_ties_natural_log_and_zero_inf
    P = probe(self)
        ^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 34, in probe
    test.assertTrue(path.is_file(), "missing forward-only V7-DIAG implementation")
AssertionError: False is not true : missing forward-only V7-DIAG implementation

======================================================================
FAIL: test_actual_driver_bit_identity_and_independent_tokens_counts_normalization (__main__.StatisticTests.test_actual_driver_bit_identity_and_independent_tokens_counts_normalization)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 110, in test_actual_driver_bit_identity_and_independent_tokens_counts_normalization
    P = probe(self); rows = fixture_rows(); old = stub_session(); new = stub_session()
        ^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 34, in probe
    test.assertTrue(path.is_file(), "missing forward-only V7-DIAG implementation")
AssertionError: False is not true : missing forward-only V7-DIAG implementation

======================================================================
FAIL: test_ast_identity_sums_and_loop_only_row_count_varies (__main__.StatisticTests.test_ast_identity_sums_and_loop_only_row_count_varies)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 91, in test_ast_identity_sums_and_loop_only_row_count_varies
    P = probe(self)
        ^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 34, in probe
    test.assertTrue(path.is_file(), "missing forward-only V7-DIAG implementation")
AssertionError: False is not true : missing forward-only V7-DIAG implementation

======================================================================
FAIL: test_hook_cleanup_after_forward_error (__main__.StatisticTests.test_hook_cleanup_after_forward_error)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 151, in test_hook_cleanup_after_forward_error
    P = probe(self); s = stub_session()
        ^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 34, in probe
    test.assertTrue(path.is_file(), "missing forward-only V7-DIAG implementation")
AssertionError: False is not true : missing forward-only V7-DIAG implementation

----------------------------------------------------------------------
Ran 23 tests in 0.079s

FAILED (failures=20, errors=1)
C10Z_V7_DIAG_SELFTEST_FAIL tests=23
```

### 25-test final initial RED:23 failures, no errors; missing probe/launcher and immediate persistence

Captured `/private/tmp/c10z_v7diag_build/diag_red_final.txt`; exit status `1`.

```text
CPU_ONLY: MPS availability forced false; unmocked MPS calls forbidden; no model load
test_OS_timer_terminates_sleep_and_native_GIL_hold_retains_inconclusive (__main__.DeadlineTests.test_OS_timer_terminates_sleep_and_native_GIL_hold_retains_inconclusive) ... FAIL
test_immutable_3060_includes_preimport_and_exact_boundary (__main__.DeadlineTests.test_immutable_3060_includes_preimport_and_exact_boundary) ... FAIL
test_G_failure_also_retains_immediately_obtained_dstats (__main__.PersistenceCorrectionTests.test_G_failure_also_retains_immediately_obtained_dstats) ... FAIL
test_forced_V7_failure_retains_value_and_provenance_before_G_and_scoring (__main__.PersistenceCorrectionTests.test_forced_V7_failure_retains_value_and_provenance_before_G_and_scoring) ... FAIL
test_forced_pass_outputs_checks_identical_to_frozen_previous_behavior (__main__.PersistenceCorrectionTests.test_forced_pass_outputs_checks_identical_to_frozen_previous_behavior) ... ok
test_fresh_and_process2_existing_dstats_refuse_overwrite (__main__.PersistenceCorrectionTests.test_fresh_and_process2_existing_dstats_refuse_overwrite) ... ok
test_process2_exact_input_bytes_retained_on_fail_and_pass (__main__.PersistenceCorrectionTests.test_process2_exact_input_bytes_retained_on_fail_and_pass) ... 
  test_process2_exact_input_bytes_retained_on_fail_and_pass (__main__.PersistenceCorrectionTests.test_process2_exact_input_bytes_retained_on_fail_and_pass) (fail=True) ... FAIL
test_process2_missing_G_retains_dstats_before_G_load (__main__.PersistenceCorrectionTests.test_process2_missing_G_retains_dstats_before_G_load) ... FAIL
test_all_pins_include_every_population_before_forwards (__main__.PinsAndAdmissionTests.test_all_pins_include_every_population_before_forwards) ... FAIL
test_launcher_existing_namespace_fingerprint_gpu_refuse_before_exec (__main__.PinsAndAdmissionTests.test_launcher_existing_namespace_fingerprint_gpu_refuse_before_exec) ... FAIL
test_launcher_success_exec_explicit_worktree_and_no_other_gate (__main__.PinsAndAdmissionTests.test_launcher_success_exec_explicit_worktree_and_no_other_gate) ... FAIL
test_local_arrow_revision_length_shards_and_offline_only (__main__.PinsAndAdmissionTests.test_local_arrow_revision_length_shards_and_offline_only) ... FAIL
test_namespace_refuses_reuse_and_attempt3_path (__main__.PinsAndAdmissionTests.test_namespace_refuses_reuse_and_attempt3_path) ... FAIL
test_F_pass_stops_and_random_pass_never_measures_R5000 (__main__.ProbePipelineTests.test_F_pass_stops_and_random_pass_never_measures_R5000) ... FAIL
test_R5000_independent_conditional_A2_and_D (__main__.ProbePipelineTests.test_R5000_independent_conditional_A2_and_D) ... FAIL
test_incomplete_failure_retains_prior_m_and_no_selection (__main__.ProbePipelineTests.test_incomplete_failure_retains_prior_m_and_no_selection) ... FAIL
test_scoring_deadline_cannot_publish_A1_or_increase_cap (__main__.ProbePipelineTests.test_scoring_deadline_cannot_publish_A1_or_increase_cap) ... FAIL
test_tensor_exclusive_flush_fsync_and_provenance (__main__.ProbePipelineTests.test_tensor_exclusive_flush_fsync_and_provenance) ... FAIL
test_cache_diagonal_count_and_loaded_once (__main__.SelectionAndScoringTests.test_cache_diagonal_count_and_loaded_once) ... FAIL
test_full_seed_one_permutation_and_exact_population_sizes (__main__.SelectionAndScoringTests.test_full_seed_one_permutation_and_exact_population_sizes) ... FAIL
test_ordered_routing_equal_boundary_nonfinite_and_report_only_E (__main__.SelectionAndScoringTests.test_ordered_routing_equal_boundary_nonfinite_and_report_only_E) ... FAIL
test_scoring_uses_driver_spearman_ties_natural_log_and_zero_inf (__main__.SelectionAndScoringTests.test_scoring_uses_driver_spearman_ties_natural_log_and_zero_inf) ... FAIL
test_actual_driver_bit_identity_and_independent_tokens_counts_normalization (__main__.StatisticTests.test_actual_driver_bit_identity_and_independent_tokens_counts_normalization) ... FAIL
test_ast_identity_sums_and_loop_only_row_count_varies (__main__.StatisticTests.test_ast_identity_sums_and_loop_only_row_count_varies) ... FAIL
test_hook_cleanup_after_forward_error (__main__.StatisticTests.test_hook_cleanup_after_forward_error) ... FAIL

======================================================================
FAIL: test_OS_timer_terminates_sleep_and_native_GIL_hold_retains_inconclusive (__main__.DeadlineTests.test_OS_timer_terminates_sleep_and_native_GIL_hold_retains_inconclusive)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 381, in test_OS_timer_terminates_sleep_and_native_GIL_hold_retains_inconclusive
    P = probe(self)
        ^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 34, in probe
    test.assertTrue(path.is_file(), "missing forward-only V7-DIAG implementation")
AssertionError: False is not true : missing forward-only V7-DIAG implementation

======================================================================
FAIL: test_immutable_3060_includes_preimport_and_exact_boundary (__main__.DeadlineTests.test_immutable_3060_includes_preimport_and_exact_boundary)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 373, in test_immutable_3060_includes_preimport_and_exact_boundary
    P = probe(self); now = [0.]; budget = P.Deadline(start=0., clock=lambda: now[0])
        ^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 34, in probe
    test.assertTrue(path.is_file(), "missing forward-only V7-DIAG implementation")
AssertionError: False is not true : missing forward-only V7-DIAG implementation

======================================================================
FAIL: test_G_failure_also_retains_immediately_obtained_dstats (__main__.PersistenceCorrectionTests.test_G_failure_also_retains_immediately_obtained_dstats)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 472, in test_G_failure_also_retains_immediately_obtained_dstats
    self.assertTrue((out / "dstats.pt").is_file(), "G failure lost already computed dstats")
AssertionError: False is not true : G failure lost already computed dstats

======================================================================
FAIL: test_forced_V7_failure_retains_value_and_provenance_before_G_and_scoring (__main__.PersistenceCorrectionTests.test_forced_V7_failure_retains_value_and_provenance_before_G_and_scoring)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 425, in test_forced_V7_failure_retains_value_and_provenance_before_G_and_scoring
    with self.assertRaisesRegex(D.R.Halt, "HALTED-V7"): s.prepare_instruments()
                                                        ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1092, in prepare_instruments
    self.dstats=self.compute_dstats();self.G=self.compute_G()
                                             ^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 423, in g
    def g(): self.assertTrue((out / "dstats.pt").is_file(), "dstats missing immediately after obtain"); return compute_G()
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: False is not true : dstats missing immediately after obtain

======================================================================
FAIL: test_process2_exact_input_bytes_retained_on_fail_and_pass (__main__.PersistenceCorrectionTests.test_process2_exact_input_bytes_retained_on_fail_and_pass) (fail=True)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 450, in test_process2_exact_input_bytes_retained_on_fail_and_pass
    self.assertTrue((out / "dstats.pt").is_file(), "process2 V7 halt lost input bytes")
AssertionError: False is not true : process2 V7 halt lost input bytes

======================================================================
FAIL: test_process2_missing_G_retains_dstats_before_G_load (__main__.PersistenceCorrectionTests.test_process2_missing_G_retains_dstats_before_G_load)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 480, in test_process2_missing_G_retains_dstats_before_G_load
    self.assertTrue((out / "dstats.pt").is_file(), "process2 must copy dstats before loading G")
AssertionError: False is not true : process2 must copy dstats before loading G

======================================================================
FAIL: test_all_pins_include_every_population_before_forwards (__main__.PinsAndAdmissionTests.test_all_pins_include_every_population_before_forwards)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 302, in test_all_pins_include_every_population_before_forwards
    P = probe(self)
        ^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 34, in probe
    test.assertTrue(path.is_file(), "missing forward-only V7-DIAG implementation")
AssertionError: False is not true : missing forward-only V7-DIAG implementation

======================================================================
FAIL: test_launcher_existing_namespace_fingerprint_gpu_refuse_before_exec (__main__.PinsAndAdmissionTests.test_launcher_existing_namespace_fingerprint_gpu_refuse_before_exec)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 334, in test_launcher_existing_namespace_fingerprint_gpu_refuse_before_exec
    self.assertTrue(path.is_file(), "missing exclusivity launcher")
AssertionError: False is not true : missing exclusivity launcher

======================================================================
FAIL: test_launcher_success_exec_explicit_worktree_and_no_other_gate (__main__.PinsAndAdmissionTests.test_launcher_success_exec_explicit_worktree_and_no_other_gate)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 349, in test_launcher_success_exec_explicit_worktree_and_no_other_gate
    path = ROOT / "tools/run_c10z_v7_diag.py"; self.assertTrue(path.is_file(), "missing launcher")
                                               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: False is not true : missing launcher

======================================================================
FAIL: test_local_arrow_revision_length_shards_and_offline_only (__main__.PinsAndAdmissionTests.test_local_arrow_revision_length_shards_and_offline_only)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 278, in test_local_arrow_revision_length_shards_and_offline_only
    P = probe(self)
        ^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 34, in probe
    test.assertTrue(path.is_file(), "missing forward-only V7-DIAG implementation")
AssertionError: False is not true : missing forward-only V7-DIAG implementation

======================================================================
FAIL: test_namespace_refuses_reuse_and_attempt3_path (__main__.PinsAndAdmissionTests.test_namespace_refuses_reuse_and_attempt3_path)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 362, in test_namespace_refuses_reuse_and_attempt3_path
    P = probe(self)
        ^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 34, in probe
    test.assertTrue(path.is_file(), "missing forward-only V7-DIAG implementation")
AssertionError: False is not true : missing forward-only V7-DIAG implementation

======================================================================
FAIL: test_F_pass_stops_and_random_pass_never_measures_R5000 (__main__.ProbePipelineTests.test_F_pass_stops_and_random_pass_never_measures_R5000)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 241, in test_F_pass_stops_and_random_pass_never_measures_R5000
    out, result, actual = self.pipeline(case)
                          ^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 210, in pipeline
    P = probe(self); tmp = tempfile.TemporaryDirectory(); self.addCleanup(tmp.cleanup)
        ^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 34, in probe
    test.assertTrue(path.is_file(), "missing forward-only V7-DIAG implementation")
AssertionError: False is not true : missing forward-only V7-DIAG implementation

======================================================================
FAIL: test_R5000_independent_conditional_A2_and_D (__main__.ProbePipelineTests.test_R5000_independent_conditional_A2_and_D)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 247, in test_R5000_independent_conditional_A2_and_D
    out, result, names = self.pipeline({"F1000": .79, "R1000": .79, "R5000": value})
                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 210, in pipeline
    P = probe(self); tmp = tempfile.TemporaryDirectory(); self.addCleanup(tmp.cleanup)
        ^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 34, in probe
    test.assertTrue(path.is_file(), "missing forward-only V7-DIAG implementation")
AssertionError: False is not true : missing forward-only V7-DIAG implementation

======================================================================
FAIL: test_incomplete_failure_retains_prior_m_and_no_selection (__main__.ProbePipelineTests.test_incomplete_failure_retains_prior_m_and_no_selection)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 252, in test_incomplete_failure_retains_prior_m_and_no_selection
    out, result, names = self.pipeline({"F1000": .79}, fault="R1000")
                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 210, in pipeline
    P = probe(self); tmp = tempfile.TemporaryDirectory(); self.addCleanup(tmp.cleanup)
        ^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 34, in probe
    test.assertTrue(path.is_file(), "missing forward-only V7-DIAG implementation")
AssertionError: False is not true : missing forward-only V7-DIAG implementation

======================================================================
FAIL: test_scoring_deadline_cannot_publish_A1_or_increase_cap (__main__.ProbePipelineTests.test_scoring_deadline_cannot_publish_A1_or_increase_cap)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 258, in test_scoring_deadline_cannot_publish_A1_or_increase_cap
    out, result, names = self.pipeline({"F1000": .79, "R1000": .8}, late="R1000")
                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 210, in pipeline
    P = probe(self); tmp = tempfile.TemporaryDirectory(); self.addCleanup(tmp.cleanup)
        ^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 34, in probe
    test.assertTrue(path.is_file(), "missing forward-only V7-DIAG implementation")
AssertionError: False is not true : missing forward-only V7-DIAG implementation

======================================================================
FAIL: test_tensor_exclusive_flush_fsync_and_provenance (__main__.ProbePipelineTests.test_tensor_exclusive_flush_fsync_and_provenance)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 263, in test_tensor_exclusive_flush_fsync_and_provenance
    P = probe(self)
        ^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 34, in probe
    test.assertTrue(path.is_file(), "missing forward-only V7-DIAG implementation")
AssertionError: False is not true : missing forward-only V7-DIAG implementation

======================================================================
FAIL: test_cache_diagonal_count_and_loaded_once (__main__.SelectionAndScoringTests.test_cache_diagonal_count_and_loaded_once)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 196, in test_cache_diagonal_count_and_loaded_once
    P = probe(self)
        ^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 34, in probe
    test.assertTrue(path.is_file(), "missing forward-only V7-DIAG implementation")
AssertionError: False is not true : missing forward-only V7-DIAG implementation

======================================================================
FAIL: test_full_seed_one_permutation_and_exact_population_sizes (__main__.SelectionAndScoringTests.test_full_seed_one_permutation_and_exact_population_sizes)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 162, in test_full_seed_one_permutation_and_exact_population_sizes
    P = probe(self); actual = P.population_indices(5017)
        ^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 34, in probe
    test.assertTrue(path.is_file(), "missing forward-only V7-DIAG implementation")
AssertionError: False is not true : missing forward-only V7-DIAG implementation

======================================================================
FAIL: test_ordered_routing_equal_boundary_nonfinite_and_report_only_E (__main__.SelectionAndScoringTests.test_ordered_routing_equal_boundary_nonfinite_and_report_only_E)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 168, in test_ordered_routing_equal_boundary_nonfinite_and_report_only_E
    P = probe(self)
        ^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 34, in probe
    test.assertTrue(path.is_file(), "missing forward-only V7-DIAG implementation")
AssertionError: False is not true : missing forward-only V7-DIAG implementation

======================================================================
FAIL: test_scoring_uses_driver_spearman_ties_natural_log_and_zero_inf (__main__.SelectionAndScoringTests.test_scoring_uses_driver_spearman_ties_natural_log_and_zero_inf)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 182, in test_scoring_uses_driver_spearman_ties_natural_log_and_zero_inf
    P = probe(self)
        ^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 34, in probe
    test.assertTrue(path.is_file(), "missing forward-only V7-DIAG implementation")
AssertionError: False is not true : missing forward-only V7-DIAG implementation

======================================================================
FAIL: test_actual_driver_bit_identity_and_independent_tokens_counts_normalization (__main__.StatisticTests.test_actual_driver_bit_identity_and_independent_tokens_counts_normalization)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 111, in test_actual_driver_bit_identity_and_independent_tokens_counts_normalization
    P = probe(self); rows = fixture_rows(); old = stub_session(); new = stub_session()
        ^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 34, in probe
    test.assertTrue(path.is_file(), "missing forward-only V7-DIAG implementation")
AssertionError: False is not true : missing forward-only V7-DIAG implementation

======================================================================
FAIL: test_ast_identity_sums_and_loop_only_row_count_varies (__main__.StatisticTests.test_ast_identity_sums_and_loop_only_row_count_varies)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 91, in test_ast_identity_sums_and_loop_only_row_count_varies
    P = probe(self)
        ^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 34, in probe
    test.assertTrue(path.is_file(), "missing forward-only V7-DIAG implementation")
AssertionError: False is not true : missing forward-only V7-DIAG implementation

======================================================================
FAIL: test_hook_cleanup_after_forward_error (__main__.StatisticTests.test_hook_cleanup_after_forward_error)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 152, in test_hook_cleanup_after_forward_error
    P = probe(self); s = stub_session()
        ^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 34, in probe
    test.assertTrue(path.is_file(), "missing forward-only V7-DIAG implementation")
AssertionError: False is not true : missing forward-only V7-DIAG implementation

----------------------------------------------------------------------
Ran 25 tests in 0.077s

FAILED (failures=23)
C10Z_V7_DIAG_SELFTEST_FAIL tests=25
```

### Amended pin test RED against the stale reader hash

Captured `/private/tmp/c10z_v7diag_build/pin_red.txt`; exit status `1`.

```text
test_amended_prereg_pin_shared_by_driver_reader_and_tests (c10z_astra_selftest.PinTests.test_amended_prereg_pin_shared_by_driver_reader_and_tests) ... FAIL
test_temp_copy_byte_drift (c10z_astra_selftest.PinTests.test_temp_copy_byte_drift) ... ok

======================================================================
FAIL: test_amended_prereg_pin_shared_by_driver_reader_and_tests (c10z_astra_selftest.PinTests.test_amended_prereg_pin_shared_by_driver_reader_and_tests)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 2622, in test_amended_prereg_pin_shared_by_driver_reader_and_tests
    self.assertEqual(R.PREREG_SHA, actual); self.assertEqual(D.R.PREREG_SHA, actual)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: '7c6e52e274e3dbc30cd5123d6b56ae8c9b1dca8c5e7507ff7be15d57e845059d' != '7aedd4ace95d2611bf398768df63cb60df6fce5afc23cf23209497bcd1d17a29'
- 7c6e52e274e3dbc30cd5123d6b56ae8c9b1dca8c5e7507ff7be15d57e845059d
+ 7aedd4ace95d2611bf398768df63cb60df6fce5afc23cf23209497bcd1d17a29


----------------------------------------------------------------------
Ran 2 tests in 0.003s

FAILED (failures=1)
```

### Initial25-test GREEN

Captured `/private/tmp/c10z_v7diag_build/diag_green1.txt`; exit status `0`.

```text
CPU_ONLY: MPS availability forced false; unmocked MPS calls forbidden; no model load
test_OS_timer_terminates_sleep_and_native_GIL_hold_retains_inconclusive (__main__.DeadlineTests.test_OS_timer_terminates_sleep_and_native_GIL_hold_retains_inconclusive) ... ok
test_immutable_3060_includes_preimport_and_exact_boundary (__main__.DeadlineTests.test_immutable_3060_includes_preimport_and_exact_boundary) ... ok
test_G_failure_also_retains_immediately_obtained_dstats (__main__.PersistenceCorrectionTests.test_G_failure_also_retains_immediately_obtained_dstats) ... ok
test_forced_V7_failure_retains_value_and_provenance_before_G_and_scoring (__main__.PersistenceCorrectionTests.test_forced_V7_failure_retains_value_and_provenance_before_G_and_scoring) ... ok
test_forced_pass_outputs_checks_identical_to_frozen_previous_behavior (__main__.PersistenceCorrectionTests.test_forced_pass_outputs_checks_identical_to_frozen_previous_behavior) ... ok
test_fresh_and_process2_existing_dstats_refuse_overwrite (__main__.PersistenceCorrectionTests.test_fresh_and_process2_existing_dstats_refuse_overwrite) ... ok
test_process2_exact_input_bytes_retained_on_fail_and_pass (__main__.PersistenceCorrectionTests.test_process2_exact_input_bytes_retained_on_fail_and_pass) ... ok
test_process2_missing_G_retains_dstats_before_G_load (__main__.PersistenceCorrectionTests.test_process2_missing_G_retains_dstats_before_G_load) ... ok
test_all_pins_include_every_population_before_forwards (__main__.PinsAndAdmissionTests.test_all_pins_include_every_population_before_forwards) ... ok
test_launcher_existing_namespace_fingerprint_gpu_refuse_before_exec (__main__.PinsAndAdmissionTests.test_launcher_existing_namespace_fingerprint_gpu_refuse_before_exec) ... ok
test_launcher_success_exec_explicit_worktree_and_no_other_gate (__main__.PinsAndAdmissionTests.test_launcher_success_exec_explicit_worktree_and_no_other_gate) ... ok
test_local_arrow_revision_length_shards_and_offline_only (__main__.PinsAndAdmissionTests.test_local_arrow_revision_length_shards_and_offline_only) ... ok
test_namespace_refuses_reuse_and_attempt3_path (__main__.PinsAndAdmissionTests.test_namespace_refuses_reuse_and_attempt3_path) ... ok
test_F_pass_stops_and_random_pass_never_measures_R5000 (__main__.ProbePipelineTests.test_F_pass_stops_and_random_pass_never_measures_R5000) ... ok
test_R5000_independent_conditional_A2_and_D (__main__.ProbePipelineTests.test_R5000_independent_conditional_A2_and_D) ... ok
test_incomplete_failure_retains_prior_m_and_no_selection (__main__.ProbePipelineTests.test_incomplete_failure_retains_prior_m_and_no_selection) ... ok
test_scoring_deadline_cannot_publish_A1_or_increase_cap (__main__.ProbePipelineTests.test_scoring_deadline_cannot_publish_A1_or_increase_cap) ... ok
test_tensor_exclusive_flush_fsync_and_provenance (__main__.ProbePipelineTests.test_tensor_exclusive_flush_fsync_and_provenance) ... ok
test_cache_diagonal_count_and_loaded_once (__main__.SelectionAndScoringTests.test_cache_diagonal_count_and_loaded_once) ... ok
test_full_seed_one_permutation_and_exact_population_sizes (__main__.SelectionAndScoringTests.test_full_seed_one_permutation_and_exact_population_sizes) ... ok
test_ordered_routing_equal_boundary_nonfinite_and_report_only_E (__main__.SelectionAndScoringTests.test_ordered_routing_equal_boundary_nonfinite_and_report_only_E) ... ok
test_scoring_uses_driver_spearman_ties_natural_log_and_zero_inf (__main__.SelectionAndScoringTests.test_scoring_uses_driver_spearman_ties_natural_log_and_zero_inf) ... ok
test_actual_driver_bit_identity_and_independent_tokens_counts_normalization (__main__.StatisticTests.test_actual_driver_bit_identity_and_independent_tokens_counts_normalization) ... ok
test_ast_identity_sums_and_loop_only_row_count_varies (__main__.StatisticTests.test_ast_identity_sums_and_loop_only_row_count_varies) ... ok
test_hook_cleanup_after_forward_error (__main__.StatisticTests.test_hook_cleanup_after_forward_error) ... ok

----------------------------------------------------------------------
Ran 25 tests in 3.081s

OK
HARD_DEADLINE_CONTROL native_GIL_hold=False rc=-14 elapsed_s=0.2150
HARD_DEADLINE_CONTROL native_GIL_hold=True rc=-14 elapsed_s=0.2166
C10Z_V7_DIAG_SELFTEST_PASS tests=25
```

### 29-test RED: initial timer order and lost late-error scores

Captured `/private/tmp/c10z_v7diag_build/entry_red.txt`; exit status `1`.

```text
CPU_ONLY: MPS availability forced false; unmocked MPS calls forbidden; no model load
test_OS_timer_terminates_sleep_and_native_GIL_hold_retains_inconclusive (__main__.DeadlineTests.test_OS_timer_terminates_sleep_and_native_GIL_hold_retains_inconclusive) ... ok
test_immutable_3060_includes_preimport_and_exact_boundary (__main__.DeadlineTests.test_immutable_3060_includes_preimport_and_exact_boundary) ... ok
test_memory_ceilings_and_float64_MPS_guard_without_MPS_allocation (__main__.EntryAndGuardTests.test_memory_ceilings_and_float64_MPS_guard_without_MPS_allocation) ... ok
test_outer_error_preserves_durable_measured_population_details (__main__.EntryAndGuardTests.test_outer_error_preserves_durable_measured_population_details) ... HARD_DEADLINE_CONTROL native_GIL_hold=False rc=-14 elapsed_s=0.2209
HARD_DEADLINE_CONTROL native_GIL_hold=True rc=-14 elapsed_s=0.2219
{"decision_id": "D-C10z-v7diag", "outcome": "INCONCLUSIVE", "reason": "TimeoutError: forced final deadline", "completion": "incomplete", "scores": {}, "populations_measured": [], "cap_seconds": 3060, "late_layer_fidelity": "UNVERIFIED", "cpu_agreement_establishes_MPS_equivalence": false, "downstream_requirement": "exit0 plus complete verdict; implementation review before dispatch"}
FAIL
test_real_entry_CPU_fixture_pins_durable_before_each_forward (__main__.EntryAndGuardTests.test_real_entry_CPU_fixture_pins_durable_before_each_forward) ... {"decision_id": "D-C10z-v7diag", "outcome": "A1", "reason": "exactly pinned R1000 passes P", "completion": "complete", "scores": {"F1000": {"rho": {"4": 0.79, "5": 0.79, "6": 0.79, "7": 0.79, "8": 0.79, "9": 0.79, "10": 0.79, "11": 0.79, "12": 0.79}, "E": {"4": "+inf", "5": "+inf", "6": "+inf", "7": "+inf", "8": "+inf", "9": "+inf", "10": "+inf", "11": "+inf", "12": "+inf"}, "P": false}, "R1000": {"rho": {"4": 0.8, "5": 0.8, "6": 0.8, "7": 0.8, "8": 0.8, "9": 0.8, "10": 0.8, "11": 0.8, "12": 0.8}, "E": {"4": "+inf", "5": "+inf", "6": "+inf", "7": "+inf", "8": "+inf", "9": "+inf", "10": "+inf", "11": "+inf", "12": "+inf"}, "P": true}}, "populations_measured": ["F1000", "R1000"], "cap_seconds": 3060, "late_layer_fidelity": "UNVERIFIED", "cpu_agreement_establishes_MPS_equivalence": false, "downstream_requirement": "exit0 plus complete verdict; implementation review before dispatch"}
ok
test_timer_armed_before_namespace_and_initial_publication (__main__.EntryAndGuardTests.test_timer_armed_before_namespace_and_initial_publication) ... {"decision_id": "D-C10z-v7diag", "outcome": "INCONCLUSIVE", "reason": "ValueError: forced setup refusal", "completion": "incomplete", "scores": {}, "populations_measured": [], "cap_seconds": 3060, "late_layer_fidelity": "UNVERIFIED", "cpu_agreement_establishes_MPS_equivalence": false, "downstream_requirement": "exit0 plus complete verdict; implementation review before dispatch"}
FAIL
test_G_failure_also_retains_immediately_obtained_dstats (__main__.PersistenceCorrectionTests.test_G_failure_also_retains_immediately_obtained_dstats) ... ok
test_forced_V7_failure_retains_value_and_provenance_before_G_and_scoring (__main__.PersistenceCorrectionTests.test_forced_V7_failure_retains_value_and_provenance_before_G_and_scoring) ... ok
test_forced_pass_outputs_checks_identical_to_frozen_previous_behavior (__main__.PersistenceCorrectionTests.test_forced_pass_outputs_checks_identical_to_frozen_previous_behavior) ... ok
test_fresh_and_process2_existing_dstats_refuse_overwrite (__main__.PersistenceCorrectionTests.test_fresh_and_process2_existing_dstats_refuse_overwrite) ... ok
test_process2_exact_input_bytes_retained_on_fail_and_pass (__main__.PersistenceCorrectionTests.test_process2_exact_input_bytes_retained_on_fail_and_pass) ... ok
test_process2_missing_G_retains_dstats_before_G_load (__main__.PersistenceCorrectionTests.test_process2_missing_G_retains_dstats_before_G_load) ... ok
test_all_pins_include_every_population_before_forwards (__main__.PinsAndAdmissionTests.test_all_pins_include_every_population_before_forwards) ... ok
test_launcher_existing_namespace_fingerprint_gpu_refuse_before_exec (__main__.PinsAndAdmissionTests.test_launcher_existing_namespace_fingerprint_gpu_refuse_before_exec) ... ok
test_launcher_success_exec_explicit_worktree_and_no_other_gate (__main__.PinsAndAdmissionTests.test_launcher_success_exec_explicit_worktree_and_no_other_gate) ... ok
test_local_arrow_revision_length_shards_and_offline_only (__main__.PinsAndAdmissionTests.test_local_arrow_revision_length_shards_and_offline_only) ... ok
test_namespace_refuses_reuse_and_attempt3_path (__main__.PinsAndAdmissionTests.test_namespace_refuses_reuse_and_attempt3_path) ... ok
test_F_pass_stops_and_random_pass_never_measures_R5000 (__main__.ProbePipelineTests.test_F_pass_stops_and_random_pass_never_measures_R5000) ... ok
test_R5000_independent_conditional_A2_and_D (__main__.ProbePipelineTests.test_R5000_independent_conditional_A2_and_D) ... ok
test_incomplete_failure_retains_prior_m_and_no_selection (__main__.ProbePipelineTests.test_incomplete_failure_retains_prior_m_and_no_selection) ... ok
test_scoring_deadline_cannot_publish_A1_or_increase_cap (__main__.ProbePipelineTests.test_scoring_deadline_cannot_publish_A1_or_increase_cap) ... ok
test_tensor_exclusive_flush_fsync_and_provenance (__main__.ProbePipelineTests.test_tensor_exclusive_flush_fsync_and_provenance) ... ok
test_cache_diagonal_count_and_loaded_once (__main__.SelectionAndScoringTests.test_cache_diagonal_count_and_loaded_once) ... ok
test_full_seed_one_permutation_and_exact_population_sizes (__main__.SelectionAndScoringTests.test_full_seed_one_permutation_and_exact_population_sizes) ... ok
test_ordered_routing_equal_boundary_nonfinite_and_report_only_E (__main__.SelectionAndScoringTests.test_ordered_routing_equal_boundary_nonfinite_and_report_only_E) ... ok
test_scoring_uses_driver_spearman_ties_natural_log_and_zero_inf (__main__.SelectionAndScoringTests.test_scoring_uses_driver_spearman_ties_natural_log_and_zero_inf) ... ok
test_actual_driver_bit_identity_and_independent_tokens_counts_normalization (__main__.StatisticTests.test_actual_driver_bit_identity_and_independent_tokens_counts_normalization) ... ok
test_ast_identity_sums_and_loop_only_row_count_varies (__main__.StatisticTests.test_ast_identity_sums_and_loop_only_row_count_varies) ... ok
test_hook_cleanup_after_forward_error (__main__.StatisticTests.test_hook_cleanup_after_forward_error) ... ok

======================================================================
FAIL: test_outer_error_preserves_durable_measured_population_details (__main__.EntryAndGuardTests.test_outer_error_preserves_durable_measured_population_details)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 478, in test_outer_error_preserves_durable_measured_population_details
    self.assertEqual(result["scores"], measured); self.assertEqual(result["outcome"], "INCONCLUSIVE")
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: {} != {'F1000': {'rho': {'4': 0.79, '5': 0.79, '[465 chars]rue}}
Diff is 1215 characters long. Set self.maxDiff to None to see it.

======================================================================
FAIL: test_timer_armed_before_namespace_and_initial_publication (__main__.EntryAndGuardTests.test_timer_armed_before_namespace_and_initial_publication)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 432, in test_timer_armed_before_namespace_and_initial_publication
    self.assertEqual(events[:3], ["armed", "reserve", "publish"])
AssertionError: Lists differ: ['reserve', 'publish', 'armed'] != ['armed', 'reserve', 'publish']

First differing element 0:
'reserve'
'armed'

- ['reserve', 'publish', 'armed']
+ ['armed', 'reserve', 'publish']

----------------------------------------------------------------------
Ran 29 tests in 6.327s

FAILED (failures=2)
C10Z_V7_DIAG_SELFTEST_FAIL tests=29
```

### 29-test GREEN after boundary corrections

Captured `/private/tmp/c10z_v7diag_build/diag_green_final.txt`; exit status `0`.

```text
CPU_ONLY: MPS availability forced false; unmocked MPS calls forbidden; no model load
test_OS_timer_terminates_sleep_and_native_GIL_hold_retains_inconclusive (__main__.DeadlineTests.test_OS_timer_terminates_sleep_and_native_GIL_hold_retains_inconclusive) ... ok
test_immutable_3060_includes_preimport_and_exact_boundary (__main__.DeadlineTests.test_immutable_3060_includes_preimport_and_exact_boundary) ... ok
test_memory_ceilings_and_float64_MPS_guard_without_MPS_allocation (__main__.EntryAndGuardTests.test_memory_ceilings_and_float64_MPS_guard_without_MPS_allocation) ... ok
test_outer_error_preserves_durable_measured_population_details (__main__.EntryAndGuardTests.test_outer_error_preserves_durable_measured_population_details) ... HARD_DEADLINE_CONTROL native_GIL_hold=False rc=-14 elapsed_s=0.2368
HARD_DEADLINE_CONTROL native_GIL_hold=True rc=-14 elapsed_s=0.2407
{"decision_id": "D-C10z-v7diag", "outcome": "INCONCLUSIVE", "reason": "TimeoutError: forced final deadline", "completion": "incomplete", "scores": {"F1000": {"E": {"10": "+inf", "11": "+inf", "12": "+inf", "4": "+inf", "5": "+inf", "6": "+inf", "7": "+inf", "8": "+inf", "9": "+inf"}, "P": false, "rho": {"10": 0.79, "11": 0.79, "12": 0.79, "4": 0.79, "5": 0.79, "6": 0.79, "7": 0.79, "8": 0.79, "9": 0.79}}, "R1000": {"E": {"10": "+inf", "11": "+inf", "12": "+inf", "4": "+inf", "5": "+inf", "6": "+inf", "7": "+inf", "8": "+inf", "9": "+inf"}, "P": true, "rho": {"10": 0.8, "11": 0.8, "12": 0.8, "4": 0.8, "5": 0.8, "6": 0.8, "7": 0.8, "8": 0.8, "9": 0.8}}}, "populations_measured": ["F1000", "R1000"], "cap_seconds": 3060, "late_layer_fidelity": "UNVERIFIED", "cpu_agreement_establishes_MPS_equivalence": false, "downstream_requirement": "exit0 plus complete verdict; implementation review before dispatch"}
ok
test_real_entry_CPU_fixture_pins_durable_before_each_forward (__main__.EntryAndGuardTests.test_real_entry_CPU_fixture_pins_durable_before_each_forward) ... {"decision_id": "D-C10z-v7diag", "outcome": "A1", "reason": "exactly pinned R1000 passes P", "completion": "complete", "scores": {"F1000": {"rho": {"4": 0.79, "5": 0.79, "6": 0.79, "7": 0.79, "8": 0.79, "9": 0.79, "10": 0.79, "11": 0.79, "12": 0.79}, "E": {"4": "+inf", "5": "+inf", "6": "+inf", "7": "+inf", "8": "+inf", "9": "+inf", "10": "+inf", "11": "+inf", "12": "+inf"}, "P": false}, "R1000": {"rho": {"4": 0.8, "5": 0.8, "6": 0.8, "7": 0.8, "8": 0.8, "9": 0.8, "10": 0.8, "11": 0.8, "12": 0.8}, "E": {"4": "+inf", "5": "+inf", "6": "+inf", "7": "+inf", "8": "+inf", "9": "+inf", "10": "+inf", "11": "+inf", "12": "+inf"}, "P": true}}, "populations_measured": ["F1000", "R1000"], "cap_seconds": 3060, "late_layer_fidelity": "UNVERIFIED", "cpu_agreement_establishes_MPS_equivalence": false, "downstream_requirement": "exit0 plus complete verdict; implementation review before dispatch"}
ok
test_timer_armed_before_namespace_and_initial_publication (__main__.EntryAndGuardTests.test_timer_armed_before_namespace_and_initial_publication) ... {"decision_id": "D-C10z-v7diag", "outcome": "INCONCLUSIVE", "reason": "ValueError: forced setup refusal", "completion": "incomplete", "scores": {}, "populations_measured": [], "cap_seconds": 3060, "late_layer_fidelity": "UNVERIFIED", "cpu_agreement_establishes_MPS_equivalence": false, "downstream_requirement": "exit0 plus complete verdict; implementation review before dispatch"}
ok
test_G_failure_also_retains_immediately_obtained_dstats (__main__.PersistenceCorrectionTests.test_G_failure_also_retains_immediately_obtained_dstats) ... ok
test_forced_V7_failure_retains_value_and_provenance_before_G_and_scoring (__main__.PersistenceCorrectionTests.test_forced_V7_failure_retains_value_and_provenance_before_G_and_scoring) ... ok
test_forced_pass_outputs_checks_identical_to_frozen_previous_behavior (__main__.PersistenceCorrectionTests.test_forced_pass_outputs_checks_identical_to_frozen_previous_behavior) ... ok
test_fresh_and_process2_existing_dstats_refuse_overwrite (__main__.PersistenceCorrectionTests.test_fresh_and_process2_existing_dstats_refuse_overwrite) ... ok
test_process2_exact_input_bytes_retained_on_fail_and_pass (__main__.PersistenceCorrectionTests.test_process2_exact_input_bytes_retained_on_fail_and_pass) ... ok
test_process2_missing_G_retains_dstats_before_G_load (__main__.PersistenceCorrectionTests.test_process2_missing_G_retains_dstats_before_G_load) ... ok
test_all_pins_include_every_population_before_forwards (__main__.PinsAndAdmissionTests.test_all_pins_include_every_population_before_forwards) ... ok
test_launcher_existing_namespace_fingerprint_gpu_refuse_before_exec (__main__.PinsAndAdmissionTests.test_launcher_existing_namespace_fingerprint_gpu_refuse_before_exec) ... ok
test_launcher_success_exec_explicit_worktree_and_no_other_gate (__main__.PinsAndAdmissionTests.test_launcher_success_exec_explicit_worktree_and_no_other_gate) ... ok
test_local_arrow_revision_length_shards_and_offline_only (__main__.PinsAndAdmissionTests.test_local_arrow_revision_length_shards_and_offline_only) ... ok
test_namespace_refuses_reuse_and_attempt3_path (__main__.PinsAndAdmissionTests.test_namespace_refuses_reuse_and_attempt3_path) ... ok
test_F_pass_stops_and_random_pass_never_measures_R5000 (__main__.ProbePipelineTests.test_F_pass_stops_and_random_pass_never_measures_R5000) ... ok
test_R5000_independent_conditional_A2_and_D (__main__.ProbePipelineTests.test_R5000_independent_conditional_A2_and_D) ... ok
test_incomplete_failure_retains_prior_m_and_no_selection (__main__.ProbePipelineTests.test_incomplete_failure_retains_prior_m_and_no_selection) ... ok
test_scoring_deadline_cannot_publish_A1_or_increase_cap (__main__.ProbePipelineTests.test_scoring_deadline_cannot_publish_A1_or_increase_cap) ... ok
test_tensor_exclusive_flush_fsync_and_provenance (__main__.ProbePipelineTests.test_tensor_exclusive_flush_fsync_and_provenance) ... ok
test_cache_diagonal_count_and_loaded_once (__main__.SelectionAndScoringTests.test_cache_diagonal_count_and_loaded_once) ... ok
test_full_seed_one_permutation_and_exact_population_sizes (__main__.SelectionAndScoringTests.test_full_seed_one_permutation_and_exact_population_sizes) ... ok
test_ordered_routing_equal_boundary_nonfinite_and_report_only_E (__main__.SelectionAndScoringTests.test_ordered_routing_equal_boundary_nonfinite_and_report_only_E) ... ok
test_scoring_uses_driver_spearman_ties_natural_log_and_zero_inf (__main__.SelectionAndScoringTests.test_scoring_uses_driver_spearman_ties_natural_log_and_zero_inf) ... ok
test_actual_driver_bit_identity_and_independent_tokens_counts_normalization (__main__.StatisticTests.test_actual_driver_bit_identity_and_independent_tokens_counts_normalization) ... ok
test_ast_identity_sums_and_loop_only_row_count_varies (__main__.StatisticTests.test_ast_identity_sums_and_loop_only_row_count_varies) ... ok
test_hook_cleanup_after_forward_error (__main__.StatisticTests.test_hook_cleanup_after_forward_error) ... ok

----------------------------------------------------------------------
Ran 29 tests in 6.677s

OK
C10Z_V7_DIAG_SELFTEST_PASS tests=29
```

### Bootstrap RED:3 expected failures;38 includes inherited tests removed to avoid duplicate coverage

Captured `/private/tmp/c10z_v7diag_build/bootstrap_red.txt`; exit status `1`.

```text
CPU_ONLY: MPS availability forced false; unmocked MPS calls forbidden; no model load
test_CLI_bootstrap_timer_exists_before_driver_import (__main__.DeadlineTests.test_CLI_bootstrap_timer_exists_before_driver_import) ... FAIL
test_OS_timer_terminates_sleep_and_native_GIL_hold_retains_inconclusive (__main__.DeadlineTests.test_OS_timer_terminates_sleep_and_native_GIL_hold_retains_inconclusive) ... ok
test_immutable_3060_includes_preimport_and_exact_boundary (__main__.DeadlineTests.test_immutable_3060_includes_preimport_and_exact_boundary) ... ok
test_launcher_native_block_is_bounded_before_probe_dispatch (__main__.DeadlineTests.test_launcher_native_block_is_bounded_before_probe_dispatch) ... FAIL
test_launcher_origin_carried_and_future_or_nonfinite_origin_refused (__main__.DeadlineTests.test_launcher_origin_carried_and_future_or_nonfinite_origin_refused) ... FAIL
test_memory_ceilings_and_float64_MPS_guard_without_MPS_allocation (__main__.EntryAndGuardTests.test_memory_ceilings_and_float64_MPS_guard_without_MPS_allocation) ... ok
test_outer_error_preserves_durable_measured_population_details (__main__.EntryAndGuardTests.test_outer_error_preserves_durable_measured_population_details) ... HARD_DEADLINE_CONTROL native_GIL_hold=False rc=-14 elapsed_s=0.2170
HARD_DEADLINE_CONTROL native_GIL_hold=True rc=-14 elapsed_s=0.2262
{"decision_id": "D-C10z-v7diag", "outcome": "INCONCLUSIVE", "reason": "TimeoutError: forced final deadline", "completion": "incomplete", "scores": {"F1000": {"E": {"10": "+inf", "11": "+inf", "12": "+inf", "4": "+inf", "5": "+inf", "6": "+inf", "7": "+inf", "8": "+inf", "9": "+inf"}, "P": false, "rho": {"10": 0.79, "11": 0.79, "12": 0.79, "4": 0.79, "5": 0.79, "6": 0.79, "7": 0.79, "8": 0.79, "9": 0.79}}, "R1000": {"E": {"10": "+inf", "11": "+inf", "12": "+inf", "4": "+inf", "5": "+inf", "6": "+inf", "7": "+inf", "8": "+inf", "9": "+inf"}, "P": true, "rho": {"10": 0.8, "11": 0.8, "12": 0.8, "4": 0.8, "5": 0.8, "6": 0.8, "7": 0.8, "8": 0.8, "9": 0.8}}}, "populations_measured": ["F1000", "R1000"], "cap_seconds": 3060, "late_layer_fidelity": "UNVERIFIED", "cpu_agreement_establishes_MPS_equivalence": false, "downstream_requirement": "exit0 plus complete verdict; implementation review before dispatch"}
ok
test_real_entry_CPU_fixture_pins_durable_before_each_forward (__main__.EntryAndGuardTests.test_real_entry_CPU_fixture_pins_durable_before_each_forward) ... {"decision_id": "D-C10z-v7diag", "outcome": "A1", "reason": "exactly pinned R1000 passes P", "completion": "complete", "scores": {"F1000": {"rho": {"4": 0.79, "5": 0.79, "6": 0.79, "7": 0.79, "8": 0.79, "9": 0.79, "10": 0.79, "11": 0.79, "12": 0.79}, "E": {"4": "+inf", "5": "+inf", "6": "+inf", "7": "+inf", "8": "+inf", "9": "+inf", "10": "+inf", "11": "+inf", "12": "+inf"}, "P": false}, "R1000": {"rho": {"4": 0.8, "5": 0.8, "6": 0.8, "7": 0.8, "8": 0.8, "9": 0.8, "10": 0.8, "11": 0.8, "12": 0.8}, "E": {"4": "+inf", "5": "+inf", "6": "+inf", "7": "+inf", "8": "+inf", "9": "+inf", "10": "+inf", "11": "+inf", "12": "+inf"}, "P": true}}, "populations_measured": ["F1000", "R1000"], "cap_seconds": 3060, "late_layer_fidelity": "UNVERIFIED", "cpu_agreement_establishes_MPS_equivalence": false, "downstream_requirement": "exit0 plus complete verdict; implementation review before dispatch"}
ok
test_timer_armed_before_namespace_and_initial_publication (__main__.EntryAndGuardTests.test_timer_armed_before_namespace_and_initial_publication) ... {"decision_id": "D-C10z-v7diag", "outcome": "INCONCLUSIVE", "reason": "ValueError: forced setup refusal", "completion": "incomplete", "scores": {}, "populations_measured": [], "cap_seconds": 3060, "late_layer_fidelity": "UNVERIFIED", "cpu_agreement_establishes_MPS_equivalence": false, "downstream_requirement": "exit0 plus complete verdict; implementation review before dispatch"}
ok
test_F_pass_stops_and_random_pass_never_measures_R5000 (__main__.IntegrityTests.test_F_pass_stops_and_random_pass_never_measures_R5000) ... ok
test_R5000_independent_conditional_A2_and_D (__main__.IntegrityTests.test_R5000_independent_conditional_A2_and_D) ... ok
test_incomplete_failure_retains_prior_m_and_no_selection (__main__.IntegrityTests.test_incomplete_failure_retains_prior_m_and_no_selection) ... ok
test_real_source_cache_model_tokenizer_corruption_is_inconclusive_and_retains_m (__main__.IntegrityTests.test_real_source_cache_model_tokenizer_corruption_is_inconclusive_and_retains_m) ... ok
test_scoring_deadline_cannot_publish_A1_or_increase_cap (__main__.IntegrityTests.test_scoring_deadline_cannot_publish_A1_or_increase_cap) ... ok
test_tensor_exclusive_flush_fsync_and_provenance (__main__.IntegrityTests.test_tensor_exclusive_flush_fsync_and_provenance) ... ok
test_G_failure_also_retains_immediately_obtained_dstats (__main__.PersistenceCorrectionTests.test_G_failure_also_retains_immediately_obtained_dstats) ... ok
test_forced_V7_failure_retains_value_and_provenance_before_G_and_scoring (__main__.PersistenceCorrectionTests.test_forced_V7_failure_retains_value_and_provenance_before_G_and_scoring) ... ok
test_forced_pass_outputs_checks_identical_to_frozen_previous_behavior (__main__.PersistenceCorrectionTests.test_forced_pass_outputs_checks_identical_to_frozen_previous_behavior) ... ok
test_fresh_and_process2_existing_dstats_refuse_overwrite (__main__.PersistenceCorrectionTests.test_fresh_and_process2_existing_dstats_refuse_overwrite) ... ok
test_process2_exact_input_bytes_retained_on_fail_and_pass (__main__.PersistenceCorrectionTests.test_process2_exact_input_bytes_retained_on_fail_and_pass) ... ok
test_process2_missing_G_retains_dstats_before_G_load (__main__.PersistenceCorrectionTests.test_process2_missing_G_retains_dstats_before_G_load) ... ok
test_all_pins_include_every_population_before_forwards (__main__.PinsAndAdmissionTests.test_all_pins_include_every_population_before_forwards) ... ok
test_launcher_existing_namespace_fingerprint_gpu_refuse_before_exec (__main__.PinsAndAdmissionTests.test_launcher_existing_namespace_fingerprint_gpu_refuse_before_exec) ... ok
test_launcher_success_exec_explicit_worktree_and_no_other_gate (__main__.PinsAndAdmissionTests.test_launcher_success_exec_explicit_worktree_and_no_other_gate) ... ok
test_local_arrow_revision_length_shards_and_offline_only (__main__.PinsAndAdmissionTests.test_local_arrow_revision_length_shards_and_offline_only) ... ok
test_namespace_refuses_reuse_and_attempt3_path (__main__.PinsAndAdmissionTests.test_namespace_refuses_reuse_and_attempt3_path) ... ok
test_F_pass_stops_and_random_pass_never_measures_R5000 (__main__.ProbePipelineTests.test_F_pass_stops_and_random_pass_never_measures_R5000) ... ok
test_R5000_independent_conditional_A2_and_D (__main__.ProbePipelineTests.test_R5000_independent_conditional_A2_and_D) ... ok
test_incomplete_failure_retains_prior_m_and_no_selection (__main__.ProbePipelineTests.test_incomplete_failure_retains_prior_m_and_no_selection) ... ok
test_scoring_deadline_cannot_publish_A1_or_increase_cap (__main__.ProbePipelineTests.test_scoring_deadline_cannot_publish_A1_or_increase_cap) ... ok
test_tensor_exclusive_flush_fsync_and_provenance (__main__.ProbePipelineTests.test_tensor_exclusive_flush_fsync_and_provenance) ... ok
test_cache_diagonal_count_and_loaded_once (__main__.SelectionAndScoringTests.test_cache_diagonal_count_and_loaded_once) ... ok
test_full_seed_one_permutation_and_exact_population_sizes (__main__.SelectionAndScoringTests.test_full_seed_one_permutation_and_exact_population_sizes) ... ok
test_ordered_routing_equal_boundary_nonfinite_and_report_only_E (__main__.SelectionAndScoringTests.test_ordered_routing_equal_boundary_nonfinite_and_report_only_E) ... ok
test_scoring_uses_driver_spearman_ties_natural_log_and_zero_inf (__main__.SelectionAndScoringTests.test_scoring_uses_driver_spearman_ties_natural_log_and_zero_inf) ... ok
test_actual_driver_bit_identity_and_independent_tokens_counts_normalization (__main__.StatisticTests.test_actual_driver_bit_identity_and_independent_tokens_counts_normalization) ... ok
test_ast_identity_sums_and_loop_only_row_count_varies (__main__.StatisticTests.test_ast_identity_sums_and_loop_only_row_count_varies) ... ok
test_hook_cleanup_after_forward_error (__main__.StatisticTests.test_hook_cleanup_after_forward_error) ... ok

======================================================================
FAIL: test_CLI_bootstrap_timer_exists_before_driver_import (__main__.DeadlineTests.test_CLI_bootstrap_timer_exists_before_driver_import)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 395, in test_CLI_bootstrap_timer_exists_before_driver_import
    self.assertEqual(child.returncode, 0, child.stdout + child.stderr); print(child.stdout.strip())
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 1 != 0 : Traceback (most recent call last):
  File "<string>", line 8, in <module>
AssertionError: bootstrap timer absent before driver import


======================================================================
FAIL: test_launcher_native_block_is_bounded_before_probe_dispatch (__main__.DeadlineTests.test_launcher_native_block_is_bounded_before_probe_dispatch)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 408, in test_launcher_native_block_is_bounded_before_probe_dispatch
    self.assertEqual(child.returncode, -signal.SIGALRM, child.stdout + child.stderr)
AssertionError: 3 != -14 : {"status": "REFUSED", "reason": "fingerprint refused: {\"ok\": false}"}


======================================================================
FAIL: test_launcher_origin_carried_and_future_or_nonfinite_origin_refused (__main__.DeadlineTests.test_launcher_origin_carried_and_future_or_nonfinite_origin_refused)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 376, in test_launcher_origin_carried_and_future_or_nonfinite_origin_refused
    self.assertTrue(hasattr(P, "entry_origin"), "missing launcher deadline origin carry")
AssertionError: False is not true : missing launcher deadline origin carry

----------------------------------------------------------------------
Ran 38 tests in 11.691s

FAILED (failures=3)
C10Z_V7_DIAG_SELFTEST_FAIL tests=38
```

### Final33 new tests GREEN

Captured `/private/tmp/c10z_v7diag_build/diag_green_final2.txt`; exit status `0`.

```text
CPU_ONLY: MPS availability forced false; unmocked MPS calls forbidden; no model load
test_CLI_bootstrap_timer_exists_before_driver_import (__main__.DeadlineTests.test_CLI_bootstrap_timer_exists_before_driver_import) ... ok
test_OS_timer_terminates_sleep_and_native_GIL_hold_retains_inconclusive (__main__.DeadlineTests.test_OS_timer_terminates_sleep_and_native_GIL_hold_retains_inconclusive) ... ok
test_immutable_3060_includes_preimport_and_exact_boundary (__main__.DeadlineTests.test_immutable_3060_includes_preimport_and_exact_boundary) ... ok
test_launcher_native_block_is_bounded_before_probe_dispatch (__main__.DeadlineTests.test_launcher_native_block_is_bounded_before_probe_dispatch) ... ok
test_launcher_origin_carried_and_future_or_nonfinite_origin_refused (__main__.DeadlineTests.test_launcher_origin_carried_and_future_or_nonfinite_origin_refused) ... ok
test_memory_ceilings_and_float64_MPS_guard_without_MPS_allocation (__main__.EntryAndGuardTests.test_memory_ceilings_and_float64_MPS_guard_without_MPS_allocation) ... ok
test_outer_error_preserves_durable_measured_population_details (__main__.EntryAndGuardTests.test_outer_error_preserves_durable_measured_population_details) ... PREIMPORT_TIMER_CONTROL remaining_s=3059.982783
HARD_DEADLINE_CONTROL native_GIL_hold=False rc=-14 elapsed_s=0.2154
HARD_DEADLINE_CONTROL native_GIL_hold=True rc=-14 elapsed_s=0.2221
LAUNCHER_HARD_DEADLINE_CONTROL native_GIL_hold=True rc=-14 elapsed_s=0.1755
{"decision_id": "D-C10z-v7diag", "outcome": "INCONCLUSIVE", "reason": "TimeoutError: forced final deadline", "completion": "incomplete", "scores": {"F1000": {"E": {"10": "+inf", "11": "+inf", "12": "+inf", "4": "+inf", "5": "+inf", "6": "+inf", "7": "+inf", "8": "+inf", "9": "+inf"}, "P": false, "rho": {"10": 0.79, "11": 0.79, "12": 0.79, "4": 0.79, "5": 0.79, "6": 0.79, "7": 0.79, "8": 0.79, "9": 0.79}}, "R1000": {"E": {"10": "+inf", "11": "+inf", "12": "+inf", "4": "+inf", "5": "+inf", "6": "+inf", "7": "+inf", "8": "+inf", "9": "+inf"}, "P": true, "rho": {"10": 0.8, "11": 0.8, "12": 0.8, "4": 0.8, "5": 0.8, "6": 0.8, "7": 0.8, "8": 0.8, "9": 0.8}}}, "populations_measured": ["F1000", "R1000"], "cap_seconds": 3060, "late_layer_fidelity": "UNVERIFIED", "cpu_agreement_establishes_MPS_equivalence": false, "downstream_requirement": "exit0 plus complete verdict; implementation review before dispatch"}
ok
test_real_entry_CPU_fixture_pins_durable_before_each_forward (__main__.EntryAndGuardTests.test_real_entry_CPU_fixture_pins_durable_before_each_forward) ... {"decision_id": "D-C10z-v7diag", "outcome": "A1", "reason": "exactly pinned R1000 passes P", "completion": "complete", "scores": {"F1000": {"rho": {"4": 0.79, "5": 0.79, "6": 0.79, "7": 0.79, "8": 0.79, "9": 0.79, "10": 0.79, "11": 0.79, "12": 0.79}, "E": {"4": "+inf", "5": "+inf", "6": "+inf", "7": "+inf", "8": "+inf", "9": "+inf", "10": "+inf", "11": "+inf", "12": "+inf"}, "P": false}, "R1000": {"rho": {"4": 0.8, "5": 0.8, "6": 0.8, "7": 0.8, "8": 0.8, "9": 0.8, "10": 0.8, "11": 0.8, "12": 0.8}, "E": {"4": "+inf", "5": "+inf", "6": "+inf", "7": "+inf", "8": "+inf", "9": "+inf", "10": "+inf", "11": "+inf", "12": "+inf"}, "P": true}}, "populations_measured": ["F1000", "R1000"], "cap_seconds": 3060, "late_layer_fidelity": "UNVERIFIED", "cpu_agreement_establishes_MPS_equivalence": false, "downstream_requirement": "exit0 plus complete verdict; implementation review before dispatch"}
ok
test_timer_armed_before_namespace_and_initial_publication (__main__.EntryAndGuardTests.test_timer_armed_before_namespace_and_initial_publication) ... {"decision_id": "D-C10z-v7diag", "outcome": "INCONCLUSIVE", "reason": "ValueError: forced setup refusal", "completion": "incomplete", "scores": {}, "populations_measured": [], "cap_seconds": 3060, "late_layer_fidelity": "UNVERIFIED", "cpu_agreement_establishes_MPS_equivalence": false, "downstream_requirement": "exit0 plus complete verdict; implementation review before dispatch"}
ok
test_real_source_cache_model_tokenizer_corruption_is_inconclusive_and_retains_m (__main__.IntegrityTests.test_real_source_cache_model_tokenizer_corruption_is_inconclusive_and_retains_m) ... ok
test_G_failure_also_retains_immediately_obtained_dstats (__main__.PersistenceCorrectionTests.test_G_failure_also_retains_immediately_obtained_dstats) ... ok
test_forced_V7_failure_retains_value_and_provenance_before_G_and_scoring (__main__.PersistenceCorrectionTests.test_forced_V7_failure_retains_value_and_provenance_before_G_and_scoring) ... ok
test_forced_pass_outputs_checks_identical_to_frozen_previous_behavior (__main__.PersistenceCorrectionTests.test_forced_pass_outputs_checks_identical_to_frozen_previous_behavior) ... ok
test_fresh_and_process2_existing_dstats_refuse_overwrite (__main__.PersistenceCorrectionTests.test_fresh_and_process2_existing_dstats_refuse_overwrite) ... ok
test_process2_exact_input_bytes_retained_on_fail_and_pass (__main__.PersistenceCorrectionTests.test_process2_exact_input_bytes_retained_on_fail_and_pass) ... ok
test_process2_missing_G_retains_dstats_before_G_load (__main__.PersistenceCorrectionTests.test_process2_missing_G_retains_dstats_before_G_load) ... ok
test_all_pins_include_every_population_before_forwards (__main__.PinsAndAdmissionTests.test_all_pins_include_every_population_before_forwards) ... ok
test_launcher_existing_namespace_fingerprint_gpu_refuse_before_exec (__main__.PinsAndAdmissionTests.test_launcher_existing_namespace_fingerprint_gpu_refuse_before_exec) ... ok
test_launcher_success_exec_explicit_worktree_and_no_other_gate (__main__.PinsAndAdmissionTests.test_launcher_success_exec_explicit_worktree_and_no_other_gate) ... ok
test_local_arrow_revision_length_shards_and_offline_only (__main__.PinsAndAdmissionTests.test_local_arrow_revision_length_shards_and_offline_only) ... ok
test_namespace_refuses_reuse_and_attempt3_path (__main__.PinsAndAdmissionTests.test_namespace_refuses_reuse_and_attempt3_path) ... ok
test_F_pass_stops_and_random_pass_never_measures_R5000 (__main__.ProbePipelineTests.test_F_pass_stops_and_random_pass_never_measures_R5000) ... ok
test_R5000_independent_conditional_A2_and_D (__main__.ProbePipelineTests.test_R5000_independent_conditional_A2_and_D) ... ok
test_incomplete_failure_retains_prior_m_and_no_selection (__main__.ProbePipelineTests.test_incomplete_failure_retains_prior_m_and_no_selection) ... ok
test_scoring_deadline_cannot_publish_A1_or_increase_cap (__main__.ProbePipelineTests.test_scoring_deadline_cannot_publish_A1_or_increase_cap) ... ok
test_tensor_exclusive_flush_fsync_and_provenance (__main__.ProbePipelineTests.test_tensor_exclusive_flush_fsync_and_provenance) ... ok
test_cache_diagonal_count_and_loaded_once (__main__.SelectionAndScoringTests.test_cache_diagonal_count_and_loaded_once) ... ok
test_full_seed_one_permutation_and_exact_population_sizes (__main__.SelectionAndScoringTests.test_full_seed_one_permutation_and_exact_population_sizes) ... ok
test_ordered_routing_equal_boundary_nonfinite_and_report_only_E (__main__.SelectionAndScoringTests.test_ordered_routing_equal_boundary_nonfinite_and_report_only_E) ... ok
test_scoring_uses_driver_spearman_ties_natural_log_and_zero_inf (__main__.SelectionAndScoringTests.test_scoring_uses_driver_spearman_ties_natural_log_and_zero_inf) ... ok
test_actual_driver_bit_identity_and_independent_tokens_counts_normalization (__main__.StatisticTests.test_actual_driver_bit_identity_and_independent_tokens_counts_normalization) ... ok
test_ast_identity_sums_and_loop_only_row_count_varies (__main__.StatisticTests.test_ast_identity_sums_and_loop_only_row_count_varies) ... ok
test_hook_cleanup_after_forward_error (__main__.StatisticTests.test_hook_cleanup_after_forward_error) ... ok

----------------------------------------------------------------------
Ran 33 tests in 7.744s

OK
C10Z_V7_DIAG_SELFTEST_PASS tests=33
```

### Full existing ASTRA209 GREEN; two explicitly skipped MPS tests

Captured `/private/tmp/c10z_v7diag_build/astra_green.txt`; exit status `0`.

```text
CPU_ONLY: MPS availability forced false; unmocked MPS calls forbidden; no model load
test_00_implementation_exists (__main__.SpecTests.test_00_implementation_exists)
Prereg :204: actual driver, reader and stage wrapper exist. ... ok
test_band_boundaries_ordered (__main__.SpecTests.test_band_boundaries_ordered)
Prereg :112, :284: fit -> capacity -> locality -> three exhaustive BAND rows. ... ok
test_budget_origins_prestart_deadlines_round_memory (__main__.SpecTests.test_budget_origins_prestart_deadlines_round_memory)
Prereg :190, :196–198: 5400 seconds, scopes, unknown allowance, exact memory. ... C10Z_PROJECTION {"origins": {"stage01": 100.0}, "ceilings": {"stage01": 7800.0, "stage2": 60.0, "stage3": 6000.0}, "components_s": {"remaining": 1.0}, "scopes": {"stage01": {"elapsed_s": 7799.0, "remaining_s": 1.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 100.0}, "ceilings": {"stage01": 7800.0, "stage2": 60.0, "stage3": 6000.0}, "components_s": {"remaining": 1.001}, "scopes": {"stage01": {"elapsed_s": 7799.0, "remaining_s": 1.001, "ceiling_s": 7800.0}}}
ok
test_completed_stage2_keeps_stage1_round_ceiling (__main__.SpecTests.test_completed_stage2_keeps_stage1_round_ceiling)
Prereg :198, :225: completed stage2 still checks stage1 A7 timing. ... ok
test_cpu_joint_algebra_independent_reference (__main__.SpecTests.test_cpu_joint_algebra_independent_reference)
Prereg :76, :78–80, :151: nonsymmetric solve, scalar-loop independent assembly. ... ok
test_cpu_null_weight_margin_fp16_selection (__main__.SpecTests.test_cpu_null_weight_margin_fp16_selection)
Prereg :75, :77–80, :210: independent floor/median, excluded competitor, fp32 add. ... ok
test_fit_count_boundaries (__main__.SpecTests.test_fit_count_boundaries)
Prereg :210, :230–234: exact integer FIT, positive 22/23, canonical 22/23. ... ok
test_fixed_competitor_and_native_reference_contract (__main__.SpecTests.test_fixed_competitor_and_native_reference_contract)
Prereg :155: native gathered logits, fixed competitor, finite last-layer path. ... ok
test_json_real_writer_and_frozen_sources (__main__.SpecTests.test_json_real_writer_and_frozen_sources)
Prereg :137, :204, :219, :224: round-trip, immutable outputs, finite science. ... ok
test_k1_k2_omissions_and_replication (__main__.SpecTests.test_k1_k2_omissions_and_replication)
Prereg :265–280: valid early stops != V12, lower labels, R2/R3 boundaries. ... ok
test_known_answer_scalar_and_native_fp16_reference (__main__.SpecTests.test_known_answer_scalar_and_native_fp16_reference)
Prereg :155: independent scalar A/ridge/columns and native finite reference. ... ok
test_law3_both_sides (__main__.SpecTests.test_law3_both_sides)
Prereg :123, :217: all inclusive envelope edges, and A1/A2 67/68. ... ok
test_manifest_population_and_post_instrument_tampering (__main__.SpecTests.test_manifest_population_and_post_instrument_tampering)
Prereg :137, :147–155, :224: complete inputs, missing controls, post-write evidence. ... ok
test_omission_reasons_follow_K1_K2 (__main__.SpecTests.test_omission_reasons_follow_K1_K2)
Prereg :265–267: every unrun expansion is recorded with its actual stopping reason. ... ok
test_ordering_and_stage_transport (__main__.SpecTests.test_ordering_and_stage_transport)
Prereg :120–125, :127–133, :218: no early observation, ordered one-stage requests. ... ok
test_raw_evidence_over_asserted_fit_write_and_repro (__main__.SpecTests.test_raw_evidence_over_asserted_fit_write_and_repro)
Prereg :224, :230, :272, :278: reject forged counts, bytes and certificates. ... ok
test_restore_finally_and_nonempty_hook_registry (__main__.SpecTests.test_restore_finally_and_nonempty_hook_registry)
Prereg :129, :152–153: all36 tensors restored after write/eval/hook failures. ... ok
test_review_Z5_footprint_rejects_any_write_outside_selected_columns (__main__.SpecTests.test_review_Z5_footprint_rejects_any_write_outside_selected_columns)
Prereg :80, :152: only selected W_down columns may differ; every other parameter byte-identical. ... ok
test_review_Z6_restore_covers_all_36_and_verify_detects_drift (__main__.SpecTests.test_review_Z6_restore_covers_all_36_and_verify_detects_drift)
Prereg :64, :129, :153; V3 :216: full 36-layer restore, byte-hash verification halts on drift. ... ok
test_review_cross_process_replication_needs_clean_pair (__main__.SpecTests.test_review_cross_process_replication_needs_clean_pair)
Prereg :277: LEAD/PARTIAL replicate only when both clean; differing base labels otherwise -NOT-REPLICATED. ... ok
test_review_reader_instrument_ceilings_audits_and_capacity (__main__.SpecTests.test_review_reader_instrument_ceilings_audits_and_capacity)
Prereg :147, :151–155, V2/V5/V9/V12, §2.5, §2.11: each recorded gate outcome is re-checked by the reader. ... ok
test_review_stage0_law3_gate_precedes_all_new_work (__main__.SpecTests.test_review_stage0_law3_gate_precedes_all_new_work)
Prereg :120, :123, :302 (row 13): LAW#3 miss halts V4 with baseline-only record; nothing runs before the gate. ... ok
test_review_stage1_round_over_120s_halts_in_run (__main__.SpecTests.test_review_stage1_round_over_120s_halts_in_run)
Prereg :198, V13 :225, row 24: a synchronized stage-1 round >120 s halts HALTED-BUDGET in the run. ... C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1200.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 2760.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1200.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 2760.0, "ceiling_s": 7800.0}}}
ok
test_review_stage_call_refusals (__main__.SpecTests.test_review_stage_call_refusals)
Prereg :133, :137, :196, :266: fresh OUT_DIR, K1/K2 and absent-ceiling refusals happen before any launch. ... ok
test_review_wrapper_delegates_under_standing_law5 (__main__.SpecTests.test_review_wrapper_delegates_under_standing_law5)
Prereg :127, :157; V2/V9: run_law5 always takes the original path; ASTRA only behind LAW#3 and instruments. ... ok
test_review_write_prestart_projection_refuses_before_observation (__main__.SpecTests.test_review_write_prestart_projection_refuses_before_observation)
Prereg :196, V13 :225: refuse to start a candidate write when elapsed + projection exceeds the ceiling. ... C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1200.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 7799.0, "remaining_s": 2760.0, "ceiling_s": 7800.0}}}
ok
test_review_write_round_cap_columns_and_capacity (__main__.SpecTests.test_review_write_round_cap_columns_and_capacity)
Prereg :79–81, :112: <=10 writes then round cap; only selected columns written; B_Z from Z's A7 only. ... C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1200.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 2760.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1200.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 2760.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1200.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 2760.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1200.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 2760.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 7800.0}}}
ok
test_side_gate_boundaries_and_populations (__main__.SpecTests.test_side_gate_boundaries_and_populations)
Prereg :239–245: every side gate equality passes, next value fails; no pooling. ... ok
test_table_T_exhaustive_and_integer_boundaries (__main__.SpecTests.test_table_T_exhaustive_and_integer_boundaries)
Prereg :249–261: independent exhaustive T1–T5, n18/19/29/30 and g9/10. ... ok
test_terminal_K1_wrapper_waits_for_close_error (__main__.SpecTests.test_terminal_K1_wrapper_waits_for_close_error)
Prereg :129, :265: terminal K1 response waits for verified close, propagates error. ... ok
test_terminal_halt_overrides_earlier_complete_pass (__main__.SpecTests.test_terminal_halt_overrides_earlier_complete_pass)
Prereg :196, :225: stage2 hard halt invalidates earlier stage1 pass. ... ok
test_transport_wait_publication_and_worker_failure (__main__.SpecTests.test_transport_wait_publication_and_worker_failure)
Prereg :126–139, :196: resident continuity, completed response, bounded failed wait. ... {"label": "PARTIAL", "next_stage": 2}
ok
test_ttl_every_Z_arm_and_incomplete_actual_repro_failure (__main__.SpecTests.test_ttl_every_Z_arm_and_incomplete_actual_repro_failure)
Prereg :267, :274, :278: any Z TTL, and omitted plus failed R1 retain both flags. ... ok
test_w1_even_median_w2_subject_free (__main__.SpecTests.test_w1_even_median_w2_subject_free)
Prereg :210, :272–274: even median, exact W1/W2, depth OR and +1 boundary. ... ok
test_worked22_validity_precedes_conditional_label (__main__.SpecTests.test_worked22_validity_precedes_conditional_label)
Prereg :149, :208, :311: contradictory raw canonical evidence HALTs before labels. ... ok
test_worked_01 (__main__.SpecTests.test_worked_01)
Prereg :290: n = 18, FIT ... ok
test_worked_02 (__main__.SpecTests.test_worked_02)
Prereg :291: n = 18, U (φ_μ = 0.80) ... ok
test_worked_03 (__main__.SpecTests.test_worked_03)
Prereg :292: n = 21, g = 9 (a = 12) ... ok
test_worked_04 (__main__.SpecTests.test_worked_04)
Prereg :293: n = 25, a = 16, g = 9 ... ok
test_worked_05 (__main__.SpecTests.test_worked_05)
Prereg :294: n = 22, g = 10, gates, FIT; stage 2 G0 holds, W1 0.4 (above the paper's SemCon range; reported, not a qualifier) ... ok
test_worked_06 (__main__.SpecTests.test_worked_06)
Prereg :295: n = 22, g = 10, G7 fails 3 (view, fact, depth) gates ... ok
test_worked_07 (__main__.SpecTests.test_worked_07)
Prereg :296: n = 29, gates, FIT; stage 2 Z-A1 = 67/72 ... ok
test_worked_08 (__main__.SpecTests.test_worked_08)
Prereg :297: n = 30, gates, FIT, W1 0.3; p2 n = 29, both processes clean ... ok
test_worked_09 (__main__.SpecTests.test_worked_09)
Prereg :298: n = 31, gates, U (φ_0^id = 22) ... ok
test_worked_10 (__main__.SpecTests.test_worked_10)
Prereg :299: n = 24, g = 6, U ... ok
test_worked_11 (__main__.SpecTests.test_worked_11)
Prereg :300: n = 33, gates, FIT, W1 1.4 ... ok
test_worked_12 (__main__.SpecTests.test_worked_12)
Prereg :301: n = 26, gates, subject-free hits A + 4 ... ok
test_worked_13 (__main__.SpecTests.test_worked_13)
Prereg :302: recipe A A7 = 19/72 ... ok
test_worked_14 (__main__.SpecTests.test_worked_14)
Prereg :303: Z3 (d): one greedy generation differs ... ok
test_worked_15 (__main__.SpecTests.test_worked_15)
Prereg :304: stage 2: n = 26, Z-band FIT, gates clean, capacity matched, n_b = 23 ... ok
test_worked_16 (__main__.SpecTests.test_worked_16)
Prereg :305: stage 2: n = 26, Z-band clean, n_b = 20 ... ok
test_worked_17 (__main__.SpecTests.test_worked_17)
Prereg :306: stage 2: n = 40, Z-band clean, n_b = 28 ... ok
test_worked_18 (__main__.SpecTests.test_worked_18)
Prereg :307: stage 2: n = 26, Z-band U (φ_μ = 0.61), n_b = 14 ... ok
test_worked_19 (__main__.SpecTests.test_worked_19)
Prereg :308: stage 2: n = 26, Z-band FIT, Z-band G7 fails, n_b = 24 ... ok
test_worked_20 (__main__.SpecTests.test_worked_20)
Prereg :309: stage 2: n = 22, Z-band clean, n_b = 17 ... ok
test_worked_21 (__main__.SpecTests.test_worked_21)
Prereg :310: stage 2: Z-band FIT, T = 144, B_Z = 2,304 > 2,200 ... ok
test_worked_22 (__main__.SpecTests.test_worked_22)
Prereg :311: n = 22, g = 10, gates, φ_μ = 0.958, φ_0^id = 24, actual `canon_full_n` = 0 ... ok
test_worked_23 (__main__.SpecTests.test_worked_23)
Prereg :312: n = 26, gates, FIT, W1 = 0.55 exactly ... ok
test_worked_24 (__main__.SpecTests.test_worked_24)
Prereg :313: stage 1: a synchronized round takes 121 s ... ok
test_z2_ambiguous_and_all_validity_gates (__main__.SpecTests.test_z2_ambiguous_and_all_validity_gates)
Prereg :149, :212–225: zero checked Z2 HALTs; V1–V13 each enforced. ... ok
test_B1_stage0_refuses_without_recorded_go_decision (__main__.Fix1Tests.test_B1_stage0_refuses_without_recorded_go_decision)
Prereg :3, :341–344: operator go before stage 0; blocking demo B1. ... ok
test_B2_stray_stage_call_after_terminal_K1_keeps_the_result (__main__.Fix1Tests.test_B2_stray_stage_call_after_terminal_K1_keeps_the_result)
Prereg :137, :204, :267: a refusal preserves completed records; blocking demo B2. ... HALTED-V12: duplicate, out-of-order, stale or closed stage call
ok
test_B3_clean_survivor_without_stage2_ceiling_keeps_stage1_record (__main__.Fix1Tests.test_B3_clean_survivor_without_stage2_ceiling_keeps_stage1_record)
Prereg :196, :265–267: unbudgeted expansion closes STAGE1; blocking demo B3 with lead's suffix ruling. ... HALTED-BUDGET: absent stage2 ceiling
ok
test_fix1_absent_ceilings_terminal_labels_and_resident_close (__main__.Fix1Tests.test_fix1_absent_ceilings_terminal_labels_and_resident_close)
Prereg :196, :265–267: clean stage1/2 without next budget terminates; no G0/replication claim. ... {"label": "PARTIAL-STAGE1", "base_label": "PARTIAL", "qualifiers": ["STAGE1"], "gates": {"G1": true, "G2": true, "G3": true, "G4": true, "G5": true, "G7": true}, "FIT": true, "n": 26, "a": 12, "gain": 14, "attribution": "NOT-RUN", "next_stage": null, "replicated": false, "lead_replicated": false, "artifact_identity": "NOT-EVALUATED", "numeric_behavioral_reproduction": "NOT-EVALUATED", "scientific_verdict": true}
ok
test_fix1_go_launch_copy_and_manifest_sha (__main__.Fix1Tests.test_fix1_go_launch_copy_and_manifest_sha)
Prereg :3, :137, :341–344: validated go copied to launch and its exact bytes bound to H_in. ... {"label": "NULL-STAGE1", "base_label": "NULL", "qualifiers": ["STAGE1"], "gates": {"G1": true, "G2": true, "G3": true, "G4": true, "G5": true, "G7": true}, "FIT": true, "n": 18, "a": 12, "gain": 6, "attribution": "NOT-RUN", "next_stage": null, "replicated": false, "lead_replicated": false, "artifact_identity": "NOT-EVALUATED", "numeric_behavioral_reproduction": "NOT-EVALUATED", "scientific_verdict": true}
ok
test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation. ... ok
test_fix1_go_sha_is_mandatory_reader_provenance (__main__.Fix1Tests.test_fix1_go_sha_is_mandatory_reader_provenance)
Prereg :137, V12 :224; §6 :341–344: missing/malformed go digest invalidates the manifest. ... ok
test_fix1_halt_sidecar_retains_completed_observations_for_both_processes (__main__.Fix1Tests.test_fix1_halt_sidecar_retains_completed_observations_for_both_processes)
Prereg :123, :267, :323: actual deadline/validity halts keep completed pass bytes and nonbinding observations. ... ok
test_fix1_refusals_preserve_finished_attempt_byte_for_byte (__main__.Fix1Tests.test_fix1_refusals_preserve_finished_attempt_byte_for_byte)
Prereg :137, :204, :267: duplicate/closed/out-of-order client refusals do not alter a finished attempt. ... HALTED-V12: attempt needs fresh OUT_DIR
HALTED-V12: duplicate, out-of-order, stale or closed stage call
HALTED-V12: duplicate, out-of-order, stale or closed stage call
HALTED-V12: stage3 requires clean completed K2 and closed process1
ok
test_fix1_relative_outdir_resolved_at_main_parse (__main__.Fix1Tests.test_fix1_relative_outdir_resolved_at_main_parse)
Prereg :8, :137, :204: records use one absolute OUT_DIR before the harness import changes cwd. ... ok
test_fix1_shell_preserves_go_env_absolute_outdir_and_no_refusal_write (__main__.Fix1Tests.test_fix1_shell_preserves_go_env_absolute_outdir_and_no_refusal_write)
Prereg :3, :137, :204: shell passes go unchanged and leaves unlaunched attempts untouched. ... ok
test_fix1_watchdog_preserves_last_published_record (__main__.Fix1Tests.test_fix1_watchdog_preserves_last_published_record)
Prereg :196, :225, :267: expired stage-2 watchdog preserves the complete earlier pass and labels HALT. ... ok
test_fix2_child_receives_parent_resolved_absolute_outdir (__main__.Fix2Tests.test_fix2_child_receives_parent_resolved_absolute_outdir)
Prereg :137, :204; fix2 item 1/O02: direct stage_call resolves the child path before cwd changes. ... ok
test_fix2_disqualified_missing_ceiling_is_k1_not_absent (__main__.Fix2Tests.test_fix2_disqualified_missing_ceiling_is_k1_not_absent)
Prereg :265, :272; B3g: a qualified PARTIAL/LEAD stops for K1 even without an expansion budget. ... ok
test_fix2_failed_resident_detection_closes_halt_and_keeps_passes (__main__.Fix2Tests.test_fix2_failed_resident_detection_closes_halt_and_keeps_passes)
Prereg :267, :323; D-C10z-fix1 (3): all wait_stage failed-resident detections publish a durable HALT. ... ok
test_fix2_go_nonfinite_constants_and_overflow_refused (__main__.Fix2Tests.test_fix2_go_nonfinite_constants_and_overflow_refused)
Prereg V6 :219, §6 :341–344; G11: nested NaN/Infinity and overflowing JSON numbers are refused without writes. ... ok
test_fix2_resident_stops_at_parent_halt_and_preserves_session_fields (__main__.Fix2Tests.test_fix2_resident_stops_at_parent_halt_and_preserves_session_fields)
Prereg :267, :323; item 2/H10/H11: a resumed resident sees the parent's halt at its next terminal check. ... ok
test_fix2_session_record_absent_ceiling_matches_reader_omissions (__main__.Fix2Tests.test_fix2_session_record_absent_ceiling_matches_reader_omissions)
Prereg :196, :265–267; B3d: the actual Session.record producer agrees with the independent reader. ... ok
test_fix2_z0_sigma_halts_in_driver_at_frozen_boundary (__main__.Fix2Tests.test_fix2_z0_sigma_halts_in_driver_at_frozen_boundary)
Prereg :147; A32: the real Z0 function permits sigma=.125 and halts above it before any reader. ... ok
test_z0_v5_halt_persists_native_and_full_sigma (__main__.Fix2Tests.test_z0_v5_halt_persists_native_and_full_sigma)
Diagnosability only: the unchanged V5 refusal publishes both measured maxima. ... ok
test_i_idle_expiry (__main__.IdleGapTests.test_i_idle_expiry) ... C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7200.0, "stage2": 200.0, "stage3": 7460.0}, "components_s": {"candidate_rounds": 1200.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 2760.0, "ceiling_s": 7200.0}}}
ok
test_ii_late_entry (__main__.IdleGapTests.test_ii_late_entry) ... C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7200.0, "stage2": 200.0, "stage3": 7460.0}, "components_s": {"candidate_rounds": 1200.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 2760.0, "ceiling_s": 7200.0}}}
ok
test_iii_deadline_samples (__main__.IdleGapTests.test_iii_deadline_samples) ... C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7200.0, "stage2": 200.0, "stage3": 7460.0}, "components_s": {"candidate_rounds": 1200.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 2760.0, "ceiling_s": 7200.0}}}
ok
test_iv_process2_envelope (__main__.IdleGapTests.test_iv_process2_envelope) ... C10Z_PROJECTION {"origins": {"stage01": 0.0, "stage3": 0.0}, "ceilings": {"stage01": 7200.0, "stage2": 200.0, "stage3": 7460.0}, "components_s": {"candidate_rounds": 1200.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 2760.0, "ceiling_s": 7200.0}, "stage3": {"elapsed_s": 0.0, "remaining_s": 2860.0, "ceiling_s": 7460.0}}}
ok
test_ix_transition_lock (__main__.IdleGapTests.test_ix_transition_lock) ... ok
test_v_complete01_only_enter (__main__.IdleGapTests.test_v_complete01_only_enter) ... ok
test_vi_mutation_deadlines (__main__.IdleGapTests.test_vi_mutation_deadlines) ... C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7200.0, "stage2": 200.0, "stage3": 7460.0}, "components_s": {"candidate_rounds": 1200.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 2760.0, "ceiling_s": 7200.0}}}
ok
test_vii_entry_invariant (__main__.IdleGapTests.test_vii_entry_invariant) ... C10Z_PROJECTION {"origins": {"stage01": 0.0, "stage3": 0.0}, "ceilings": {"stage01": 7200.0, "stage2": 200.0, "stage3": 7460.0}, "components_s": {"candidate_rounds": 1200.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 2760.0, "ceiling_s": 7200.0}, "stage3": {"elapsed_s": 0.0, "remaining_s": 2860.0, "ceiling_s": 7460.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0, "stage3": 0.0}, "ceilings": {"stage01": 7200.0, "stage2": 200.0, "stage3": 7460.0}, "components_s": {"candidate_rounds": 1200.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 2760.0, "ceiling_s": 7200.0}, "stage3": {"elapsed_s": 0.0, "remaining_s": 2860.0, "ceiling_s": 7460.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0, "stage3": 0.0}, "ceilings": {"stage01": 7200.0, "stage2": 200.0, "stage3": 7460.0}, "components_s": {"candidate_rounds": 1200.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 2760.0, "ceiling_s": 7200.0}, "stage3": {"elapsed_s": 0.0, "remaining_s": 2860.0, "ceiling_s": 7460.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0, "stage3": 0.0}, "ceilings": {"stage01": 7200.0, "stage2": 200.0, "stage3": 7460.0}, "components_s": {"candidate_rounds": 1200.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 2760.0, "ceiling_s": 7200.0}, "stage3": {"elapsed_s": 0.0, "remaining_s": 2860.0, "ceiling_s": 7460.0}}}
ok
test_viii_single_timestamp (__main__.IdleGapTests.test_viii_single_timestamp) ... ok
test_c01_neighbors (__main__.BudgetBoundTests.test_c01_neighbors) ... ok
test_huge_integer_refusal (__main__.BudgetBoundTests.test_huge_integer_refusal) ... ok
test_benchmark_template_digest_mismatch_refuses_before_launch (__main__.LaunchBindingTests.test_benchmark_template_digest_mismatch_refuses_before_launch)
D-C10z-v4fix: a valid selected benchmark with different templates refuses V12 before worker/output creation. ... ok
test_c01 (__main__.LaunchBindingTests.test_c01) ... ok
test_derived (__main__.LaunchBindingTests.test_derived) ... ok
test_environment (__main__.LaunchBindingTests.test_environment) ... ok
test_go_ceilings (__main__.LaunchBindingTests.test_go_ceilings) ... ok
test_go_fields (__main__.LaunchBindingTests.test_go_fields) ... ok
test_go_huge_integer_ceiling_refusal (__main__.LaunchBindingTests.test_go_huge_integer_ceiling_refusal) ... ok
test_inertness_counts (__main__.LaunchBindingTests.test_inertness_counts) ... ok
test_inertness_environment (__main__.LaunchBindingTests.test_inertness_environment) ... ok
test_inertness_json (__main__.LaunchBindingTests.test_inertness_json) ... ok
test_inertness_path (__main__.LaunchBindingTests.test_inertness_path) ... ok
test_inertness_required (__main__.LaunchBindingTests.test_inertness_required) ... ok
test_inertness_schema (__main__.LaunchBindingTests.test_inertness_schema) ... ok
test_inertness_sources (__main__.LaunchBindingTests.test_inertness_sources) ... ok
test_inertness_success (__main__.LaunchBindingTests.test_inertness_success) ... ok
test_inertness_verdict (__main__.LaunchBindingTests.test_inertness_verdict) ... ok
test_record_absolute (__main__.LaunchBindingTests.test_record_absolute) ... ok
test_record_invalid (__main__.LaunchBindingTests.test_record_invalid) ... ok
test_record_nonstrict (__main__.LaunchBindingTests.test_record_nonstrict) ... ok
test_record_optional_status (__main__.LaunchBindingTests.test_record_optional_status) ... ok
test_record_outside (__main__.LaunchBindingTests.test_record_outside) ... ok
test_record_required (__main__.LaunchBindingTests.test_record_required) ... ok
test_record_selection (__main__.LaunchBindingTests.test_record_selection) ... ok
test_record_unreadable (__main__.LaunchBindingTests.test_record_unreadable) ... ok
test_refused (__main__.LaunchBindingTests.test_refused) ... ok
test_script (__main__.LaunchBindingTests.test_script) ... ok
test_sources (__main__.LaunchBindingTests.test_sources) ... ok
test_stage2_override (__main__.LaunchBindingTests.test_stage2_override) ... ok
test_stage3_environment_drift (__main__.LaunchBindingTests.test_stage3_environment_drift) ... ok
test_stage3_inertness_drift (__main__.LaunchBindingTests.test_stage3_inertness_drift) ... ok
test_stage3_override (__main__.LaunchBindingTests.test_stage3_override) ... ok
test_stage3_record_drift (__main__.LaunchBindingTests.test_stage3_record_drift) ... ok
test_stage3_script_drift (__main__.LaunchBindingTests.test_stage3_script_drift) ... ok
test_stage3_source_drift (__main__.LaunchBindingTests.test_stage3_source_drift) ... ok
test_stage3_switch (__main__.LaunchBindingTests.test_stage3_switch) ... ok
test_stop (__main__.LaunchBindingTests.test_stop) ... ok
test_substitution (__main__.LaunchBindingTests.test_substitution) ... ok
test_success_roundtrip (__main__.LaunchBindingTests.test_success_roundtrip) ... ok
test_switch_empty (__main__.LaunchBindingTests.test_switch_empty) ... ok
test_switch_space (__main__.LaunchBindingTests.test_switch_space) ... ok
test_switch_true (__main__.LaunchBindingTests.test_switch_true) ... ok
test_switch_zero (__main__.LaunchBindingTests.test_switch_zero) ... ok
test_total (__main__.LaunchBindingTests.test_total) ... ok
test_benchmark_sha (__main__.ReaderBindingTests.test_benchmark_sha) ... ok
test_c01_neighbors (__main__.ReaderBindingTests.test_c01_neighbors) ... ok
test_go_ceilings (__main__.ReaderBindingTests.test_go_ceilings) ... ok
test_history_ceilings (__main__.ReaderBindingTests.test_history_ceilings) ... ok
test_huge_integer_refusal (__main__.ReaderBindingTests.test_huge_integer_refusal) ... ok
test_pass_launch (__main__.ReaderBindingTests.test_pass_launch) ... ok
test_process_ceilings (__main__.ReaderBindingTests.test_process_ceilings) ... ok
test_scope_ceiling (__main__.ReaderBindingTests.test_scope_ceiling) ... ok
test_attempt2_out_and_logs_preserve_attempt1 (__main__.WrapperTests.test_attempt2_out_and_logs_preserve_attempt1)
Prereg §10(d2): explicit attempt2 output, go/benchmark selection and both redirected logs preserve attempt1. ... ok
test_direct_scripts_executable_on_disk_and_git_index (__main__.WrapperTests.test_direct_scripts_executable_on_disk_and_git_index) ... ok
test_next_stage_types (__main__.WrapperTests.test_next_stage_types) ... ok
test_relative_out (__main__.WrapperTests.test_relative_out) ... ok
test_stage0_failure (__main__.WrapperTests.test_stage0_failure) ... ok
test_UTC_diagnostic_collision_refuses_exclusive_creation (__main__.TemplatePinTests.test_UTC_diagnostic_collision_refuses_exclusive_creation) ... ok
test_UTC_diagnostics_preserve_historical_records (__main__.TemplatePinTests.test_UTC_diagnostics_preserve_historical_records) ... ok
test_V4_resident_retains_templates_and_halt_hashes (__main__.TemplatePinTests.test_V4_resident_retains_templates_and_halt_hashes) ... C10Z_PROJECTION {"origins": {"stage01": 1326072.448619916}, "ceilings": {"stage01": 7800.0, "stage2": 12000.0, "stage3": 24000.0}, "components_s": {"recipe_A": 2040.0, "reference_D": 300.0, "G": 120.0, "verification_and_all_probes": 1380.0, "candidate_rounds": 1200.0, "serialization_and_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.000821791822090745, "remaining_s": 5220.0, "ceiling_s": 7800.0}}}
ok
test_cache_pinned_before_recipe_A_without_sampling (__main__.TemplatePinTests.test_cache_pinned_before_recipe_A_without_sampling) ... ok
test_existing_context_artifact_refusal_unchanged (__main__.TemplatePinTests.test_existing_context_artifact_refusal_unchanged) ... ok
test_manual_seed_zero_kept_before_harness_import (__main__.TemplatePinTests.test_manual_seed_zero_kept_before_harness_import) ... ok
test_process2_reuses_loaded_cache_before_baseline (__main__.TemplatePinTests.test_process2_reuses_loaded_cache_before_baseline) ... ok
test_scorer_template_identity_mismatch_refuses_before_recipe_A (__main__.TemplatePinTests.test_scorer_template_identity_mismatch_refuses_before_recipe_A) ... ok
test_selected_template_list_mismatch_refuses_before_recipe_A (__main__.TemplatePinTests.test_selected_template_list_mismatch_refuses_before_recipe_A) ... ok
test_templates_and_run_hash_written_before_LAW3_gate (__main__.TemplatePinTests.test_templates_and_run_hash_written_before_LAW3_gate) ... ok
test_templates_byte_equal_to_benchmark (__main__.TemplatePinTests.test_templates_byte_equal_to_benchmark) ... ok
test_amended_prereg_pin_shared_by_driver_reader_and_tests (__main__.PinTests.test_amended_prereg_pin_shared_by_driver_reader_and_tests) ... ok
test_temp_copy_byte_drift (__main__.PinTests.test_temp_copy_byte_drift) ... ok
test_on_off_science (__main__.TelemetryIntegrationTests.test_on_off_science) ... ok
test_placements_ast (__main__.TelemetryIntegrationTests.test_placements_ast) ... ok
test_resident_on_off (__main__.TelemetryIntegrationTests.test_resident_on_off) ... ok
test_resident_telemetry_failures_preserve_science (__main__.TelemetryIntegrationTests.test_resident_telemetry_failures_preserve_science) ... ok
test_write_telemetry_failures_preserve_science (__main__.TelemetryIntegrationTests.test_write_telemetry_failures_preserve_science) ... ok
test_probe_batch1_keeps_padding_and_captures_actual_position_ids (__main__.Z0ProbeTests.test_probe_batch1_keeps_padding_and_captures_actual_position_ids) ... ok
test_probe_cpu_json_pipeline_roundtrip_and_exclusive_output (__main__.Z0ProbeTests.test_probe_cpu_json_pipeline_roundtrip_and_exclusive_output) ... C10Z_Z0_PROBE_DIAGNOSTIC /private/tmp/c10z_v7diag_build/tmpyuf9qi2f/results/c10z_astra_z0_probe/20261008T220001Z/probe.json
ok
test_probe_diff_statistics_subtract_in_cpu_float64 (__main__.Z0ProbeTests.test_probe_diff_statistics_subtract_in_cpu_float64) ... ok
test_probe_distinct_shape_controls_and_full_sigma_match_z0 (__main__.Z0ProbeTests.test_probe_distinct_shape_controls_and_full_sigma_match_z0) ... ok
test_probe_mutation_is_detected_without_restoring_weights (__main__.Z0ProbeTests.test_probe_mutation_is_detected_without_restoring_weights) ... ok
test_probe_native_mask_cli_default_and_ones (__main__.Z0ProbeTests.test_probe_native_mask_cli_default_and_ones) ... ok
test_probe_native_mask_option_changes_only_forward_kwargs (__main__.Z0ProbeTests.test_probe_native_mask_option_changes_only_forward_kwargs) ... ok
test_probe_native_prefix_leads_equal_real_z0 (__main__.Z0ProbeTests.test_probe_native_prefix_leads_equal_real_z0) ... ok
test_probe_never_writes_weights_or_calls_edit_recipe_sampling (__main__.Z0ProbeTests.test_probe_never_writes_weights_or_calls_edit_recipe_sampling) ... ok
test_probe_records_attention_backend_and_native_logit_bound (__main__.Z0ProbeTests.test_probe_records_attention_backend_and_native_logit_bound) ... ok
test_probe_refuses_existing_or_escaped_output_before_model_load (__main__.Z0ProbeTests.test_probe_refuses_existing_or_escaped_output_before_model_load) ... ok
test_probe_wrong_template_sha_refuses_before_model_load (__main__.Z0ProbeTests.test_probe_wrong_template_sha_refuses_before_model_load) ... ok
test_ast_guard_covers_all_unsafe_copy_api_forms (__main__.V5CopyTests.test_ast_guard_covers_all_unsafe_copy_api_forms) ... ok
test_astra_sources_no_combined_device_dtype_transfer_ast (__main__.V5CopyTests.test_astra_sources_no_combined_device_dtype_transfer_ast) ... ok
test_margin_leads_no_combined_device_dtype_transfer_ast (__main__.V5CopyTests.test_margin_leads_no_combined_device_dtype_transfer_ast) ... ok
test_mps_offset_view_corruption_and_exact_split_copy (__main__.V5CopyTests.test_mps_offset_view_corruption_and_exact_split_copy) ... skipped 'MPS unavailable: offset-view corruption reproduction UNVERIFIED'
test_mps_torch_cpu64_transfers_before_float64 (__main__.V5CopyTests.test_mps_torch_cpu64_transfers_before_float64) ... skipped 'MPS unavailable: float64 capture regression UNVERIFIED'
test_probe_native_and_full_rows_transfer_before_cast_ast (__main__.V5CopyTests.test_probe_native_and_full_rows_transfer_before_cast_ast) ... ok
test_target_probabilities_preserves_offset_float32_inputs (__main__.V5CopyTests.test_target_probabilities_preserves_offset_float32_inputs) ... ok
test_torch_cpu64_moves_to_cpu_before_float64_ast (__main__.V5CopyTests.test_torch_cpu64_moves_to_cpu_before_float64_ast) ... ok
test_T3_header_four_kinds_fields_and_full_cost_accounting (__main__.TelemetryUnitTests.test_T3_header_four_kinds_fields_and_full_cost_accounting) ... ok
test_T4_public_methods_avoid_science_clocks_and_gates (__main__.TelemetryUnitTests.test_T4_public_methods_avoid_science_clocks_and_gates) ... ok
test_T5a_directory_failure_is_disabled_once (__main__.TelemetryUnitTests.test_T5a_directory_failure_is_disabled_once) ... ok
test_T5a_initial_open_failure_is_disabled_once (__main__.TelemetryUnitTests.test_T5a_initial_open_failure_is_disabled_once) ... ok
test_T5b_write_failure_is_disabled_once (__main__.TelemetryUnitTests.test_T5b_write_failure_is_disabled_once) ... ok
test_T5c_flush_failure_is_disabled_once (__main__.TelemetryUnitTests.test_T5c_flush_failure_is_disabled_once) ... ok
test_T5d_fsync_failure_is_disabled_once (__main__.TelemetryUnitTests.test_T5d_fsync_failure_is_disabled_once) ... ok
test_T5e_keyboard_interrupt_propagates (__main__.TelemetryUnitTests.test_T5e_keyboard_interrupt_propagates) ... ok
test_T6_each_call_preserves_cpu_model_and_inputs (__main__.TelemetryUnitTests.test_T6_each_call_preserves_cpu_model_and_inputs) ... ok
test_T6_lens_uses_layer_output_top5_and_no_grad (__main__.TelemetryUnitTests.test_T6_lens_uses_layer_output_top5_and_no_grad) ... ok
test_T7_default_chunk_keeps_cpu_float32_under64MiB (__main__.TelemetryUnitTests.test_T7_default_chunk_keeps_cpu_float32_under64MiB) ... ok
test_T7_probabilities_dense_reference_and_row_chunk_bound (__main__.TelemetryUnitTests.test_T7_probabilities_dense_reference_and_row_chunk_bound) ... ok
test_T9_write_volume_no_requirement_lines (__main__.TelemetryUnitTests.test_T9_write_volume_no_requirement_lines) ... C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1200.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 2760.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1200.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 2760.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 7800.0}}}
ok
test_deterministic_three_pass_schedule_and_kwargs (__main__.TelemetryInertnessTests.test_deterministic_three_pass_schedule_and_kwargs) ... ok
test_full_greedy_suffix_count_and_compare (__main__.TelemetryInertnessTests.test_full_greedy_suffix_count_and_compare) ... ok
test_lens_sensitive_batch_is_not_inert (__main__.TelemetryInertnessTests.test_lens_sensitive_batch_is_not_inert) ... ok
test_lens_sensitive_probe_is_not_inert (__main__.TelemetryInertnessTests.test_lens_sensitive_probe_is_not_inert) ... ok
test_plain_drift_is_nondeterministic_baseline (__main__.TelemetryInertnessTests.test_plain_drift_is_nondeterministic_baseline) ... ok
test_runner_checks_all36_weights_and_invalid_is_exit2 (__main__.TelemetryRunnerTests.test_runner_checks_all36_weights_and_invalid_is_exit2) ... ok
test_runner_driver_module_reused (__main__.TelemetryRunnerTests.test_runner_driver_module_reused) ... ok
test_runner_import_is_stdlib_only (__main__.TelemetryRunnerTests.test_runner_import_is_stdlib_only) ... ok
test_runner_refuses_outside_and_existing_record_without_forward (__main__.TelemetryRunnerTests.test_runner_refuses_outside_and_existing_record_without_forward) ... ok
test_runner_refuses_relative_out_path (__main__.TelemetryRunnerTests.test_runner_refuses_relative_out_path) ... ok
test_runner_roundtrip_identity_and_no_write_engine_calls (__main__.TelemetryRunnerTests.test_runner_roundtrip_identity_and_no_write_engine_calls) ... ok

----------------------------------------------------------------------
Ran 209 tests in 115.116s

OK (skipped=2)
C10Z_ASTRA_SELFTEST_PASS tests=209
```

### Full existing benchmark47 GREEN

Captured `/private/tmp/c10z_v7diag_build/benchmark_green.txt`; exit status `0`.

```text
CPU_ONLY: MPS availability forced false; unmocked MPS calls forbidden; no model load
test_eight_v3_calibration_cases (__main__.BenchmarkCeilingTests.test_eight_v3_calibration_cases) ... ok
test_exact_rounding_and_c01_stop_boundary (__main__.BenchmarkCeilingTests.test_exact_rounding_and_c01_stop_boundary) ... ok
test_mean_outlier_and_complete_eval_tstar (__main__.BenchmarkCeilingTests.test_mean_outlier_and_complete_eval_tstar) ... ok
test_optional_minima_and_timeout_lower_bound (__main__.BenchmarkCeilingTests.test_optional_minima_and_timeout_lower_bound) ... ok
test_raw_values_drive_all_terms (__main__.BenchmarkCeilingTests.test_raw_values_drive_all_terms) ... ok
test_refused_records_never_fallback_or_numbers (__main__.BenchmarkCeilingTests.test_refused_records_never_fallback_or_numbers) ... ok
test_environment_identity_metadata_only (__main__.BenchmarkIdentityTests.test_environment_identity_metadata_only) ... ok
test_environment_identity_no_torch_subprocess (__main__.BenchmarkIdentityTests.test_environment_identity_no_torch_subprocess) ... ok
test_source_identity_exact_order_and_root (__main__.BenchmarkIdentityTests.test_source_identity_exact_order_and_root) ... ok
test_top_level_import_stdlib_only_subprocess (__main__.BenchmarkIdentityTests.test_top_level_import_stdlib_only_subprocess) ... ok
test_env_preflight_refusals (__main__.BenchmarkLifecycleTests.test_env_preflight_refusals) ... ok
test_injected_worker_full_schedule_no_writer_calls (__main__.BenchmarkLifecycleTests.test_injected_worker_full_schedule_no_writer_calls) ... C10Z_PROBE_POPULATION {"arm": "A7_coined_coined", "sha256": "02af6172c2ce331a98cd0b6aeee0b656f6062050caf228fa2be50048d6938aaa", "counts": {"F0": 36, "prefix": 3888, "subject_free": 108, "relations": 48}}
ok
test_injected_worker_synthetic_mps_identity_validates_derived (__main__.BenchmarkLifecycleTests.test_injected_worker_synthetic_mps_identity_validates_derived) ... C10Z_PROBE_POPULATION {"arm": "A7_coined_coined", "sha256": "02af6172c2ce331a98cd0b6aeee0b656f6062050caf228fa2be50048d6938aaa", "counts": {"F0": 36, "prefix": 3888, "subject_free": 108, "relations": 48}}
ok
test_optional_skip_keeps_top_level_status (__main__.BenchmarkLifecycleTests.test_optional_skip_keeps_top_level_status) ... C10Z_PROBE_POPULATION {"arm": "A7_coined_coined", "sha256": "02af6172c2ce331a98cd0b6aeee0b656f6062050caf228fa2be50048d6938aaa", "counts": {"F0": 36, "prefix": 3888, "subject_free": 108, "relations": 48}}
ok
test_out_path_refusals_and_prefix_trap (__main__.BenchmarkLifecycleTests.test_out_path_refusals_and_prefix_trap) ... ok
test_start_and_phase_fit_boundaries (__main__.BenchmarkLifecycleTests.test_start_and_phase_fit_boundaries) ... ok
test_supervisor_600_boundary_fake_clock (__main__.BenchmarkLifecycleTests.test_supervisor_600_boundary_fake_clock) ... ok
test_supervisor_completed_worker_untouched (__main__.BenchmarkLifecycleTests.test_supervisor_completed_worker_untouched) ... ok
test_supervisor_existing_record_cap_preserves_bytes (__main__.BenchmarkLifecycleTests.test_supervisor_existing_record_cap_preserves_bytes) ... ok
test_supervisor_forbidden_astra_cap_preserves_directory (__main__.BenchmarkLifecycleTests.test_supervisor_forbidden_astra_cap_preserves_directory) ... ok
test_supervisor_outside_benchmark_cap_preserves_directory (__main__.BenchmarkLifecycleTests.test_supervisor_outside_benchmark_cap_preserves_directory) ... ok
test_supervisor_real_process_group_kill_and_interrupted_record (__main__.BenchmarkLifecycleTests.test_supervisor_real_process_group_kill_and_interrupted_record) ... ok
test_svd_timeout_565_lower_bound_and_worker_survival (__main__.BenchmarkLifecycleTests.test_svd_timeout_565_lower_bound_and_worker_survival) ... ok
test_system_wide_monotonic_subprocess (__main__.BenchmarkLifecycleTests.test_system_wide_monotonic_subprocess) ... ok
test_worker_guard_status_bands_and_reserved_after_hash (__main__.BenchmarkLifecycleTests.test_worker_guard_status_bands_and_reserved_after_hash) ... C10Z_PROBE_POPULATION {"arm": "A7_coined_coined", "sha256": "02af6172c2ce331a98cd0b6aeee0b656f6062050caf228fa2be50048d6938aaa", "counts": {"F0": 36, "prefix": 3888, "subject_free": 108, "relations": 48}}
C10Z_PROBE_POPULATION {"arm": "A7_coined_coined", "sha256": "02af6172c2ce331a98cd0b6aeee0b656f6062050caf228fa2be50048d6938aaa", "counts": {"F0": 36, "prefix": 3888, "subject_free": 108, "relations": 48}}
C10Z_PROBE_POPULATION {"arm": "A7_coined_coined", "sha256": "02af6172c2ce331a98cd0b6aeee0b656f6062050caf228fa2be50048d6938aaa", "counts": {"F0": 36, "prefix": 3888, "subject_free": 108, "relations": 48}}
ok
test_worker_load_over_300_invalid (__main__.BenchmarkLifecycleTests.test_worker_load_over_300_invalid) ... ok
test_worker_mutation_invalid_and_refused (__main__.BenchmarkLifecycleTests.test_worker_mutation_invalid_and_refused) ... C10Z_PROBE_POPULATION {"arm": "A7_coined_coined", "sha256": "02af6172c2ce331a98cd0b6aeee0b656f6062050caf228fa2be50048d6938aaa", "counts": {"F0": 36, "prefix": 3888, "subject_free": 108, "relations": 48}}
ok
test_worker_svd_timeout_preserves_complete_and_capped (__main__.BenchmarkLifecycleTests.test_worker_svd_timeout_preserves_complete_and_capped) ... C10Z_PROBE_POPULATION {"arm": "A7_coined_coined", "sha256": "02af6172c2ce331a98cd0b6aeee0b656f6062050caf228fa2be50048d6938aaa", "counts": {"F0": 36, "prefix": 3888, "subject_free": 108, "relations": 48}}
C10Z_PROBE_POPULATION {"arm": "A7_coined_coined", "sha256": "02af6172c2ce331a98cd0b6aeee0b656f6062050caf228fa2be50048d6938aaa", "counts": {"F0": 36, "prefix": 3888, "subject_free": 108, "relations": 48}}
ok
test_empty_population_leaves_no_heartbeat (__main__.BenchmarkPopulationTests.test_empty_population_leaves_no_heartbeat) ... ok
test_full_population_forward_counts (__main__.BenchmarkPopulationTests.test_full_population_forward_counts) ... C10Z_PROBE_POPULATION {"arm": "A7_coined_coined", "sha256": "02af6172c2ce331a98cd0b6aeee0b656f6062050caf228fa2be50048d6938aaa", "counts": {"F0": 36, "prefix": 3888, "subject_free": 108, "relations": 48}}
C10Z_PROBE_POPULATION {"arm": "A7_coined_coined", "sha256": "286257b9d4f116fd9d47b617a27c81f2258b70e40b1b72ac1cb7389ad59992d4", "counts": {"F0": 36, "prefix": 3888, "subject_free": 108, "relations": 48}}
ok
test_greedy_argmax_and_no_grad (__main__.BenchmarkPopulationTests.test_greedy_argmax_and_no_grad) ... ok
test_guarded_loop_completes_item_then_stops (__main__.BenchmarkPopulationTests.test_guarded_loop_completes_item_then_stops) ... ok
test_guarded_warmup_records_actual_count (__main__.BenchmarkPopulationTests.test_guarded_warmup_records_actual_count) ... ok
test_population_batch_and_digest_match_driver (__main__.BenchmarkPopulationTests.test_population_batch_and_digest_match_driver) ... C10Z_PROBE_POPULATION {"arm": "A7_coined_coined", "sha256": "02af6172c2ce331a98cd0b6aeee0b656f6062050caf228fa2be50048d6938aaa", "counts": {"F0": 36, "prefix": 3888, "subject_free": 108, "relations": 48}}
C10Z_PROBE_POPULATION {"arm": "A7_coined_coined", "sha256": "02af6172c2ce331a98cd0b6aeee0b656f6062050caf228fa2be50048d6938aaa", "counts": {"F0": 36, "prefix": 3888, "subject_free": 108, "relations": 48}}
ok
test_timed_reads_heartbeat_and_warmup_exclusion (__main__.BenchmarkPopulationTests.test_timed_reads_heartbeat_and_warmup_exclusion) ... ok
test_huge_integer_timing_is_value_error (__main__.BenchmarkRecordTests.test_huge_integer_timing_is_value_error) ... ok
test_interrupted_replace_preserves_prior_record (__main__.BenchmarkRecordTests.test_interrupted_replace_preserves_prior_record) ... ok
test_measurement_consistency_rejections (__main__.BenchmarkRecordTests.test_measurement_consistency_rejections) ... ok
test_nan_preserves_prior_record (__main__.BenchmarkRecordTests.test_nan_preserves_prior_record) ... ok
test_nonfinite_statistics_rejected (__main__.BenchmarkRecordTests.test_nonfinite_statistics_rejected) ... ok
test_optional_status_container_is_value_error (__main__.BenchmarkRecordTests.test_optional_status_container_is_value_error) ... ok
test_probe_status_boundaries (__main__.BenchmarkRecordTests.test_probe_status_boundaries) ... ok
test_quantiles_and_statistics (__main__.BenchmarkRecordTests.test_quantiles_and_statistics) ... ok
test_schema_missing_keys_and_wrong_types (__main__.BenchmarkRecordTests.test_schema_missing_keys_and_wrong_types) ... ok
test_strict_atomic_roundtrip_with_identity (__main__.BenchmarkRecordTests.test_strict_atomic_roundtrip_with_identity) ... ok
test_target_lengths_population_and_probe_counts (__main__.BenchmarkRecordTests.test_target_lengths_population_and_probe_counts) ... ok
test_weights_device_dtype_revision_fingerprint_rejections (__main__.BenchmarkRecordTests.test_weights_device_dtype_revision_fingerprint_rejections) ... ok

----------------------------------------------------------------------
Ran 47 tests in 2.751s

OK
C10Z_BENCH_SELFTEST_PASS tests=47
```

### Actual engine fingerprint PASS

Captured `/private/tmp/c10z_v7diag_build/fingerprint.txt`; exit status `0`.

```text
engine fingerprint PASS: /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/memit_dry_run/memit/memit/memit_main.py
  sha256   d941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65  (expected d941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65; pod-era 5c0c706a…)
  _cov_cpu 3  (expected 3)
```

Graft: two successful calls reported272221 tokens saved (~$0.14); failed CLI/symbol probes were not counted as savings.


## Fix round 1 — 2026-10-09

Recorded 2026-10-09T18:11:43.722426+00:00. **Authorized CPU fix round PASS: 41 probe tests; 209 existing ASTRA tests with two MPS skips; 47 benchmark tests; engine fingerprint PASS.** Across the final suites, 295 executed tests pass and two are skipped. The four-blocker review was read in full at `/Users/robertrhu/.claude/jobs/8ac4cacf/tmp/astra_v7diag_impl_out.md` (GPT-6-Astra high, FIX-FIRST); the dated end addendum to `docs/C10Z_V7DIAG_BUILD_BRIEF.md` approves the persistence-only G extension. This section supersedes the earlier report's execve, early-complete verdict and late-G statements; it preserves that report as historical build evidence.

### Requirement → test → implementation

| Requirement | Test | Implementation | Evidence / resulting behavior |
|---|---|---|---|
| 1. Returned m plus actual provenance before validation; retain mismatches | [S:656](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py:656) `test_returned_m_and_actual_provenance_survive_pin_mismatch`<br>[S:843](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py:843) `test_invalid_returned_m_is_retained_before_tensor_validation`<br>[S:510](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py:510) `test_outer_error_preserves_durable_measured_population_details` | [P:311](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag.py:311) `save_population`<br>[P:317](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag.py:317) `validate_population`<br>[P:347](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag.py:347) `measure_populations`<br>[P:421](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag.py:421) `run` | Exact returned object exclusively saved/flushed/fsynced before CPU-f32/36-layer or provenance checks. Structured expected/actual differences survive a subsequent outer error and cleanup. No scoring on mismatch. |
| 2. Surviving supervisor; fresh UTC halt diagnostic on signal/timeout/crash | [S:702](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py:702) `test_supervisor_retains_fresh_fsynced_halt_after_worker_signal_timeout_crash`<br>[S:401](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py:401) `test_launcher_native_block_is_bounded_before_probe_dispatch` | [L:120](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/run_c10z_v7_diag.py:120) `launch`<br>[L:79](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/run_c10z_v7_diag.py:79) `worker`<br>[L:92](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/run_c10z_v7_diag.py:92) `halt_diagnostic`<br>[L:48](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/run_c10z_v7_diag.py:48) `write_record`<br>[P:336](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag.py:336) `record_phase` | Parent remains model-free and waits; no execve. Child runs only required preflight checks then runpy forward entry. Exclusive fsynced halt_diagnostic_<UTC-with-microseconds>.json names active/incomplete phases, worker exit/cap and retained artifact paths/sizes. Parent ownership record prevents namespace reuse; worker adopts only its token-bound namespace. |
| 3. Original 3060s includes cleanup AND actual worker exit; success after cleanup | [S:783](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py:783) `test_explicit_cleanup_is_inside_original_deadline_before_success`<br>[S:796](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py:796) `test_worker_deadline_remains_armed_after_cleanup_until_actual_exit`<br>[S:808](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py:808) `test_supervisor_admits_only_clean_receipt_and_normal_exit_within_original_cap` | [P:50](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag.py:50) `Deadline`<br>[P:75](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag.py:75) `__exit__`<br>[P:421](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag.py:421) `run`<br>[L:120](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/run_c10z_v7_diag.py:120) `launch` | Explicit hook/reference release, GC and runtime MPS synchronization/cache release execute inside the existing worker deadline. CLI leaves default SIGALRM armed through Python shutdown. Only a pending receipt follows cleanup; parent requires observed exit 0 within original cap and publishes complete afterward. Crash/stall after receipt never admits. |
| 4. Team addendum: G exclusive save/exact byte-copy BEFORE V8, record-only | [S:890](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py:890) `test_fresh_and_process2_G_retained_before_actual_V8_cholesky_failure`<br>[S:609](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py:609) `test_process2_exact_input_bytes_retained_on_fail_and_pass`<br>[S:600](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py:600) `test_forced_pass_outputs_checks_identical_to_frozen_previous_behavior` | [D:1085](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py:1085) `prepare_instruments`<br>[D:1119](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py:1119) `save_tensor_file` | Fresh G saved immediately after compute_G; process2 exact bytes copied immediately after torch.load. Removed late duplicate. Actual negative-definite Cholesky control raises HALTED-V8 while both inputs remain. Forced-pass gate/check/output bytes remain identical to frozen prior behavior. |
| Supervisor integration: actual gate recognizes only verified model-free parent | [S:855](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py:855) `test_real_gpu_gate_excludes_only_verified_parent_and_still_blocks_competing_job` | [L:56](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/run_c10z_v7_diag.py:56) `supervised_gpu_check`<br>[L:79](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/run_c10z_v7_diag.py:79) `worker`<br>[P:421](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag.py:421) `run` | Unchanged check_gpu/real classifier, mocked inventory IO. Parent+worker pass; genuine competing Python and wrong-command parent refuse. Exclusion binds leased PID to actual getppid, token, original origin/cap, launcher hash and exact argv/executable; inventory/tmux errors remain refusals. tools/c10w_p2_gate.py untouched. |

### RED → GREEN and observation checks

Before production edits, the new controls reproduced Astra's four failures exactly: computed m absent on mismatched provenance; signal exit −14 retaining only provisional verdict; cleanup started and completed after timer cancellation (exit 0, 0.3984s); fresh and process2 G absent following actual HALTED-V8. First RED had 37 tests/seven failing assertions, no errors, with all original 33 passing. Initial correction gave 40 tests GREEN. A read-only independent review then found the necessary parent-process integration defect: unchanged GPU gate counted the surviving supervisor as competing compute. Actual classifier with synthetic inventory reproduced that refusal (41-test RED/one failure). The correction removes only the verified parent, retaining refusal for C10Y-like and unknown Python commands.

The next two failing cleanup assertions were traced with captured subprocess stdout to an isolated-fixture `ModuleNotFoundError`, before any model stub was acquired. Adding the real model-free tools path to that fixture restored the intended CPU cleanup path; production path guards were unchanged. The strengthened late-error test then showed one dropped structured mismatch field (41-test RED/one failure); the outer terminal record now carries the already durable field. Final 41-test GREEN includes every original control and those integration/detail controls. All intermediate outcomes are retained in the complete logs below.

Final short CPU deadline evidence: cleanup control exit −14 at 0.2228s, cleanup_started=true/cleanup_done=false; separate worker-shutdown stall exit −14 with cleanup_done=true and no complete verdict. The controls scale the immutable timer to 0.15s in isolated CPU subprocesses; they do not alter runtime 3060s. Signal/timeout/crash supervisor cases all return 2 and retain one fresh fsynced UTC diagnostic. Fsync is observed on each actual diagnostic inode. A normal post-cleanup receipt plus exit 0 admits; stall/crash after that same receipt remains INCONCLUSIVE.

The worker retains the original monotonic origin across launcher/worker/probe imports and never disarms the CLI alarm before exit. Explicit cleanup releases hooks/modules/model/tokenizer/dataset/cache references and runs GC; the MPS synchronization/cache-release branch is implemented but **UNVERIFIED and not executed in this build**. All ordinary measurement verdicts remain durable INCONCLUSIVE until cleanup and observed exit 0. The parent requires the matching post-cleanup receipt, observes worker exit within the same deadline, and checks the cap before/after final success serialization. Timeout kills/reaps the worker and writes postmortem evidence; this diagnostic publication can follow expiry and grants no extra worker time or success admission. Retained-file presence/size is evidence of preservation, not proof that a file interrupted during write is complete or scientifically admissible.

### Required verification commands and source scope

The runner uses one CPU thread, `-B`, canonical writable TMPDIR, forced MPS-unavailable and failure guards on unmocked MPS synchronize/allocation APIs. No actual model load, c10e_bandknob or transformers import, real Arrow open or dataset/model forward, GPU/MPS allocation, live GPU inventory, probe/benchmark/attempt dispatch, prereg edit, engine/c10e_bandknob edit or commit occurred. Synthetic launcher/worker files live only under `/private/tmp/c10z_v7diag_fix1/`; no real diagnostic namespace was created. Existing ASTRA/benchmark suites ran after the G persistence correction; their driver/reader/test/benchmark sources are unchanged since those passes. The final probe run includes the last helper and detail changes.

```sh
TMPDIR=/private/tmp/c10z_v7diag_fix1 LLMDB_ROOT='/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a' .venv/bin/python -B /private/tmp/c10z_v7diag_fix1/run_cpu_selftest.py experiments/track_c/c10z_v7_diag_selftest.py
TMPDIR=/private/tmp/c10z_v7diag_fix1 LLMDB_ROOT='/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a' .venv/bin/python -B /private/tmp/c10z_v7diag_fix1/run_cpu_selftest.py experiments/track_c/c10z_astra_selftest.py
TMPDIR=/private/tmp/c10z_v7diag_fix1 LLMDB_ROOT='/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a' .venv/bin/python -B /private/tmp/c10z_v7diag_fix1/run_cpu_selftest.py experiments/track_c/c10z_astra_benchmark_selftest.py
LLMDB_ROOT='/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a' .venv/bin/python -B tools/engine_fingerprint.py
git diff --check
git diff --exit-code -- docs/C10Z_ASTRA_PREREG.md memit_dry_run/ experiments/track_c/c10e_bandknob.py tools/c10w_p2_gate.py
```

Commands were executed through `/opt/homebrew/bin/rtk proxy`, with complete stdout/stderr captured below. Final engine source SHA is `d941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65`, `_cov_cpu=3`. Both diff checks exit 0. All seven individually pinned protected files (prereg, team brief, engine main, c10e_bandknob, reader, existing ASTRA selftest and benchmark selftest) retain their fix-round-start hashes. Prereg SHA is still `7aedd4ace95d2611bf398768df63cb60df6fce5afc23cf23209497bcd1d17a29`. Only the probe, launcher, probe selftest, record-only driver and this report changed for this round. The shared worktree has pre-existing unrelated edits; this is not a global clean-tree claim. Graft may refresh its own cache/index on lookup.

| Final source | SHA-256 |
|---|---|
| `experiments/track_c/c10z_v7_diag.py` | `f39da78b026bbab0d0c89f879d4e45762bca0f8ea342dd7477ed00f128dca917` |
| `experiments/track_c/c10z_v7_diag_selftest.py` | `1656d4ee51265834fa4adfc7a159ed598fc8faefde3f58816db20946edd27606` |
| `tools/run_c10z_v7_diag.py` | `85d41cce96699576a521340beff978e69e3c563aa51b2fb450f9e299af86ee93` |
| `experiments/track_c/c10z_astra_arms.py` | `7935a9b8c4cb043231b75e44dc02eb678afd46173069fd0807ded66f3fb6baa7` |
| `tools/c10w_p2_gate.py` | `fb6568a6e159e84b22971aa893c3a83bcaaa16085f4abd9c76ca50b4a3362a26` |

### Lead launch command — unchanged, NOT EXECUTED

```sh
LLMDB_ROOT='/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a' '/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python' -B '/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/run_c10z_v7_diag.py' --utc "$(date -u +%Y%m%dT%H%M%SZ)"
```

The parent/worker protocol is internal to this same command; no budget, batch, seed, population, precision, gate predicate or routing override was introduced. The frozen allowance arithmetic remains 2640s, ×1.15=3036s rounded to 3060s; explicit cleanup and worker exit consume that same cap. No MPS timing of the added cleanup/supervision overhead was obtained. Lead must still establish program GPU clearance and obtain required Astra implementation re-review/freeze before dispatch. Benchmark/go source identities remain stale as expected; none was rebound or launched.

**CPU agreement does not establish MPS equivalence. MPS/model behavior, live exclusivity, real cache scoring, measured runtime and any scientific A1/A2/D outcome remain UNVERIFIED.** Attempt3 remains closed HALTED-V7; its historical dataset identity is UNVERIFIABLE. No GPU admission, attempt4 continuation or F1 conclusion is implied by this CPU fix report.

### Complete fix-round output

CPU guard wrapper (unchanged from the initial build):

```python
import os
import runpy
import sys
from pathlib import Path
from unittest.mock import patch

os.environ.update(OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", MKL_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1")
import torch
torch.set_num_threads(1)
path = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(path.parent))
print("CPU_ONLY: MPS availability forced false; unmocked MPS calls forbidden; no model load", flush=True)
with patch.object(torch.backends.mps, "is_available", return_value=False), \
     patch.object(torch.mps, "synchronize", side_effect=AssertionError("MPS forbidden in build")), \
     patch.object(torch.mps, "driver_allocated_memory", side_effect=AssertionError("MPS forbidden in build")):
    runpy.run_path(str(path), run_name="__main__")
```

#### First RED, before any fix implementation: 37 tests, seven substantive failures across the four blocker controls; no errors; original 33 pass

Artifact:`/private/tmp/c10z_v7diag_fix1/probe_red.txt`; captured command exit 1.

```text
CPU_ONLY: MPS availability forced false; unmocked MPS calls forbidden; no model load
test_CLI_bootstrap_timer_exists_before_driver_import (__main__.DeadlineTests.test_CLI_bootstrap_timer_exists_before_driver_import) ... ok
test_OS_timer_terminates_sleep_and_native_GIL_hold_retains_inconclusive (__main__.DeadlineTests.test_OS_timer_terminates_sleep_and_native_GIL_hold_retains_inconclusive) ... ok
test_immutable_3060_includes_preimport_and_exact_boundary (__main__.DeadlineTests.test_immutable_3060_includes_preimport_and_exact_boundary) ... ok
test_launcher_native_block_is_bounded_before_probe_dispatch (__main__.DeadlineTests.test_launcher_native_block_is_bounded_before_probe_dispatch) ... ok
test_launcher_origin_carried_and_future_or_nonfinite_origin_refused (__main__.DeadlineTests.test_launcher_origin_carried_and_future_or_nonfinite_origin_refused) ... ok
test_memory_ceilings_and_float64_MPS_guard_without_MPS_allocation (__main__.EntryAndGuardTests.test_memory_ceilings_and_float64_MPS_guard_without_MPS_allocation) ... ok
test_outer_error_preserves_durable_measured_population_details (__main__.EntryAndGuardTests.test_outer_error_preserves_durable_measured_population_details) ... PREIMPORT_TIMER_CONTROL remaining_s=3059.974145
HARD_DEADLINE_CONTROL native_GIL_hold=False rc=-14 elapsed_s=0.2411
HARD_DEADLINE_CONTROL native_GIL_hold=True rc=-14 elapsed_s=0.2406
LAUNCHER_HARD_DEADLINE_CONTROL native_GIL_hold=True rc=-14 elapsed_s=0.1810
{"decision_id": "D-C10z-v7diag", "outcome": "INCONCLUSIVE", "reason": "TimeoutError: forced final deadline", "completion": "incomplete", "scores": {"F1000": {"E": {"10": "+inf", "11": "+inf", "12": "+inf", "4": "+inf", "5": "+inf", "6": "+inf", "7": "+inf", "8": "+inf", "9": "+inf"}, "P": false, "rho": {"10": 0.79, "11": 0.79, "12": 0.79, "4": 0.79, "5": 0.79, "6": 0.79, "7": 0.79, "8": 0.79, "9": 0.79}}, "R1000": {"E": {"10": "+inf", "11": "+inf", "12": "+inf", "4": "+inf", "5": "+inf", "6": "+inf", "7": "+inf", "8": "+inf", "9": "+inf"}, "P": true, "rho": {"10": 0.8, "11": 0.8, "12": 0.8, "4": 0.8, "5": 0.8, "6": 0.8, "7": 0.8, "8": 0.8, "9": 0.8}}}, "populations_measured": ["F1000", "R1000"], "cap_seconds": 3060, "late_layer_fidelity": "UNVERIFIED", "cpu_agreement_establishes_MPS_equivalence": false, "downstream_requirement": "exit0 plus complete verdict; implementation review before dispatch"}
ok
test_real_entry_CPU_fixture_pins_durable_before_each_forward (__main__.EntryAndGuardTests.test_real_entry_CPU_fixture_pins_durable_before_each_forward) ... {"decision_id": "D-C10z-v7diag", "outcome": "A1", "reason": "exactly pinned R1000 passes P", "completion": "complete", "scores": {"F1000": {"rho": {"4": 0.79, "5": 0.79, "6": 0.79, "7": 0.79, "8": 0.79, "9": 0.79, "10": 0.79, "11": 0.79, "12": 0.79}, "E": {"4": "+inf", "5": "+inf", "6": "+inf", "7": "+inf", "8": "+inf", "9": "+inf", "10": "+inf", "11": "+inf", "12": "+inf"}, "P": false}, "R1000": {"rho": {"4": 0.8, "5": 0.8, "6": 0.8, "7": 0.8, "8": 0.8, "9": 0.8, "10": 0.8, "11": 0.8, "12": 0.8}, "E": {"4": "+inf", "5": "+inf", "6": "+inf", "7": "+inf", "8": "+inf", "9": "+inf", "10": "+inf", "11": "+inf", "12": "+inf"}, "P": true}}, "populations_measured": ["F1000", "R1000"], "cap_seconds": 3060, "late_layer_fidelity": "UNVERIFIED", "cpu_agreement_establishes_MPS_equivalence": false, "downstream_requirement": "exit0 plus complete verdict; implementation review before dispatch"}
ok
test_timer_armed_before_namespace_and_initial_publication (__main__.EntryAndGuardTests.test_timer_armed_before_namespace_and_initial_publication) ... {"decision_id": "D-C10z-v7diag", "outcome": "INCONCLUSIVE", "reason": "ValueError: forced setup refusal", "completion": "incomplete", "scores": {}, "populations_measured": [], "cap_seconds": 3060, "late_layer_fidelity": "UNVERIFIED", "cpu_agreement_establishes_MPS_equivalence": false, "downstream_requirement": "exit0 plus complete verdict; implementation review before dispatch"}
ok
test_explicit_cleanup_is_inside_original_deadline_before_success (__main__.FixRoundOneTests.test_explicit_cleanup_is_inside_original_deadline_before_success) ... FAIL
test_fresh_and_process2_G_retained_before_actual_V8_cholesky_failure (__main__.FixRoundOneTests.test_fresh_and_process2_G_retained_before_actual_V8_cholesky_failure) ... 
  test_fresh_and_process2_G_retained_before_actual_V8_cholesky_failure (__main__.FixRoundOneTests.test_fresh_and_process2_G_retained_before_actual_V8_cholesky_failure) (process2=False) ... FAIL
  test_fresh_and_process2_G_retained_before_actual_V8_cholesky_failure (__main__.FixRoundOneTests.test_fresh_and_process2_G_retained_before_actual_V8_cholesky_failure) (process2=True) ... FAIL
test_returned_m_and_actual_provenance_survive_pin_mismatch (__main__.FixRoundOneTests.test_returned_m_and_actual_provenance_survive_pin_mismatch) ... FAIL
test_supervisor_retains_fresh_fsynced_halt_after_worker_signal_timeout_crash (__main__.FixRoundOneTests.test_supervisor_retains_fresh_fsynced_halt_after_worker_signal_timeout_crash) ... 
  test_supervisor_retains_fresh_fsynced_halt_after_worker_signal_timeout_crash (__main__.FixRoundOneTests.test_supervisor_retains_fresh_fsynced_halt_after_worker_signal_timeout_crash) (mode='signal') ... FAIL
  test_supervisor_retains_fresh_fsynced_halt_after_worker_signal_timeout_crash (__main__.FixRoundOneTests.test_supervisor_retains_fresh_fsynced_halt_after_worker_signal_timeout_crash) (mode='timeout') ... FAIL
  test_supervisor_retains_fresh_fsynced_halt_after_worker_signal_timeout_crash (__main__.FixRoundOneTests.test_supervisor_retains_fresh_fsynced_halt_after_worker_signal_timeout_crash) (mode='crash') ... FAIL
test_real_source_cache_model_tokenizer_corruption_is_inconclusive_and_retains_m (__main__.IntegrityTests.test_real_source_cache_model_tokenizer_corruption_is_inconclusive_and_retains_m) ... ok
test_G_failure_also_retains_immediately_obtained_dstats (__main__.PersistenceCorrectionTests.test_G_failure_also_retains_immediately_obtained_dstats) ... ok
test_forced_V7_failure_retains_value_and_provenance_before_G_and_scoring (__main__.PersistenceCorrectionTests.test_forced_V7_failure_retains_value_and_provenance_before_G_and_scoring) ... ok
test_forced_pass_outputs_checks_identical_to_frozen_previous_behavior (__main__.PersistenceCorrectionTests.test_forced_pass_outputs_checks_identical_to_frozen_previous_behavior) ... ok
test_fresh_and_process2_existing_dstats_refuse_overwrite (__main__.PersistenceCorrectionTests.test_fresh_and_process2_existing_dstats_refuse_overwrite) ... ok
test_process2_exact_input_bytes_retained_on_fail_and_pass (__main__.PersistenceCorrectionTests.test_process2_exact_input_bytes_retained_on_fail_and_pass) ... ok
test_process2_missing_G_retains_dstats_before_G_load (__main__.PersistenceCorrectionTests.test_process2_missing_G_retains_dstats_before_G_load) ... ok
test_all_pins_include_every_population_before_forwards (__main__.PinsAndAdmissionTests.test_all_pins_include_every_population_before_forwards) ... ok
test_launcher_existing_namespace_fingerprint_gpu_refuse_before_exec (__main__.PinsAndAdmissionTests.test_launcher_existing_namespace_fingerprint_gpu_refuse_before_exec) ... ok
test_launcher_success_exec_explicit_worktree_and_no_other_gate (__main__.PinsAndAdmissionTests.test_launcher_success_exec_explicit_worktree_and_no_other_gate) ... ok
test_local_arrow_revision_length_shards_and_offline_only (__main__.PinsAndAdmissionTests.test_local_arrow_revision_length_shards_and_offline_only) ... ok
test_namespace_refuses_reuse_and_attempt3_path (__main__.PinsAndAdmissionTests.test_namespace_refuses_reuse_and_attempt3_path) ... ok
test_F_pass_stops_and_random_pass_never_measures_R5000 (__main__.ProbePipelineTests.test_F_pass_stops_and_random_pass_never_measures_R5000) ... ok
test_R5000_independent_conditional_A2_and_D (__main__.ProbePipelineTests.test_R5000_independent_conditional_A2_and_D) ... ok
test_incomplete_failure_retains_prior_m_and_no_selection (__main__.ProbePipelineTests.test_incomplete_failure_retains_prior_m_and_no_selection) ... ok
test_scoring_deadline_cannot_publish_A1_or_increase_cap (__main__.ProbePipelineTests.test_scoring_deadline_cannot_publish_A1_or_increase_cap) ... ok
test_tensor_exclusive_flush_fsync_and_provenance (__main__.ProbePipelineTests.test_tensor_exclusive_flush_fsync_and_provenance) ... ok
test_cache_diagonal_count_and_loaded_once (__main__.SelectionAndScoringTests.test_cache_diagonal_count_and_loaded_once) ... ok
test_full_seed_one_permutation_and_exact_population_sizes (__main__.SelectionAndScoringTests.test_full_seed_one_permutation_and_exact_population_sizes) ... ok
test_ordered_routing_equal_boundary_nonfinite_and_report_only_E (__main__.SelectionAndScoringTests.test_ordered_routing_equal_boundary_nonfinite_and_report_only_E) ... ok
test_scoring_uses_driver_spearman_ties_natural_log_and_zero_inf (__main__.SelectionAndScoringTests.test_scoring_uses_driver_spearman_ties_natural_log_and_zero_inf) ... ok
test_actual_driver_bit_identity_and_independent_tokens_counts_normalization (__main__.StatisticTests.test_actual_driver_bit_identity_and_independent_tokens_counts_normalization) ... ok
test_ast_identity_sums_and_loop_only_row_count_varies (__main__.StatisticTests.test_ast_identity_sums_and_loop_only_row_count_varies) ... ok
test_hook_cleanup_after_forward_error (__main__.StatisticTests.test_hook_cleanup_after_forward_error) ... ok

======================================================================
FAIL: test_explicit_cleanup_is_inside_original_deadline_before_success (__main__.FixRoundOneTests.test_explicit_cleanup_is_inside_original_deadline_before_success)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 758, in test_explicit_cleanup_is_inside_original_deadline_before_success
    self.assertEqual(child.returncode, -signal.SIGALRM, "cleanup completed after deadline because timer was cancelled")
AssertionError: 0 != -14 : cleanup completed after deadline because timer was cancelled

======================================================================
FAIL: test_fresh_and_process2_G_retained_before_actual_V8_cholesky_failure (__main__.FixRoundOneTests.test_fresh_and_process2_G_retained_before_actual_V8_cholesky_failure) (process2=False)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 777, in test_fresh_and_process2_G_retained_before_actual_V8_cholesky_failure
    self.assertTrue((out / "G.pt").is_file(), "forced V8 failure lost already obtained G")
AssertionError: False is not true : forced V8 failure lost already obtained G

======================================================================
FAIL: test_fresh_and_process2_G_retained_before_actual_V8_cholesky_failure (__main__.FixRoundOneTests.test_fresh_and_process2_G_retained_before_actual_V8_cholesky_failure) (process2=True)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 777, in test_fresh_and_process2_G_retained_before_actual_V8_cholesky_failure
    self.assertTrue((out / "G.pt").is_file(), "forced V8 failure lost already obtained G")
AssertionError: False is not true : forced V8 failure lost already obtained G

======================================================================
FAIL: test_returned_m_and_actual_provenance_survive_pin_mismatch (__main__.FixRoundOneTests.test_returned_m_and_actual_provenance_survive_pin_mismatch)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 657, in test_returned_m_and_actual_provenance_survive_pin_mismatch
    self.assertTrue(path.is_file(), "computed m disappeared on provenance mismatch")
AssertionError: False is not true : computed m disappeared on provenance mismatch

======================================================================
FAIL: test_supervisor_retains_fresh_fsynced_halt_after_worker_signal_timeout_crash (__main__.FixRoundOneTests.test_supervisor_retains_fresh_fsynced_halt_after_worker_signal_timeout_crash) (mode='signal')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 706, in test_supervisor_retains_fresh_fsynced_halt_after_worker_signal_timeout_crash
    self.assertEqual(len(diagnostics), 1, "abnormal exit left only provisional verdict; no fresh halt diagnostic")
AssertionError: 0 != 1 : abnormal exit left only provisional verdict; no fresh halt diagnostic

======================================================================
FAIL: test_supervisor_retains_fresh_fsynced_halt_after_worker_signal_timeout_crash (__main__.FixRoundOneTests.test_supervisor_retains_fresh_fsynced_halt_after_worker_signal_timeout_crash) (mode='timeout')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 706, in test_supervisor_retains_fresh_fsynced_halt_after_worker_signal_timeout_crash
    self.assertEqual(len(diagnostics), 1, "abnormal exit left only provisional verdict; no fresh halt diagnostic")
AssertionError: 0 != 1 : abnormal exit left only provisional verdict; no fresh halt diagnostic

======================================================================
FAIL: test_supervisor_retains_fresh_fsynced_halt_after_worker_signal_timeout_crash (__main__.FixRoundOneTests.test_supervisor_retains_fresh_fsynced_halt_after_worker_signal_timeout_crash) (mode='crash')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 706, in test_supervisor_retains_fresh_fsynced_halt_after_worker_signal_timeout_crash
    self.assertEqual(len(diagnostics), 1, "abnormal exit left only provisional verdict; no fresh halt diagnostic")
AssertionError: 0 != 1 : abnormal exit left only provisional verdict; no fresh halt diagnostic

----------------------------------------------------------------------
Ran 37 tests in 11.510s

FAILED (failures=7)
FIX1_CLEANUP_CONTROL rc=0 cleanup_started=True cleanup_done=True elapsed_s=0.3984
FIX1_V8_CONTROL process2=False dstats=True G=False
FIX1_V8_CONTROL process2=True dstats=True G=False
FIX1_MISMATCH_CONTROL outcome=INCONCLUSIVE retained_m=False
FIX1_TERMINATION_CONTROL mode=signal rc=-14 files=['verdict.json']
FIX1_TERMINATION_CONTROL mode=timeout rc=1 files=['verdict.json']
FIX1_TERMINATION_CONTROL mode=crash rc=1 files=['verdict.json']
C10Z_V7_DIAG_SELFTEST_FAIL tests=37
```

#### Initial four-blocker GREEN: 40 tests; before discovering the surviving-parent inventory integration issue

Artifact:`/private/tmp/c10z_v7diag_fix1/probe_green1.txt`; captured command exit 0.

```text
CPU_ONLY: MPS availability forced false; unmocked MPS calls forbidden; no model load
test_CLI_bootstrap_timer_exists_before_driver_import (__main__.DeadlineTests.test_CLI_bootstrap_timer_exists_before_driver_import) ... ok
test_OS_timer_terminates_sleep_and_native_GIL_hold_retains_inconclusive (__main__.DeadlineTests.test_OS_timer_terminates_sleep_and_native_GIL_hold_retains_inconclusive) ... ok
test_immutable_3060_includes_preimport_and_exact_boundary (__main__.DeadlineTests.test_immutable_3060_includes_preimport_and_exact_boundary) ... ok
test_launcher_native_block_is_bounded_before_probe_dispatch (__main__.DeadlineTests.test_launcher_native_block_is_bounded_before_probe_dispatch) ... ok
test_launcher_origin_carried_and_future_or_nonfinite_origin_refused (__main__.DeadlineTests.test_launcher_origin_carried_and_future_or_nonfinite_origin_refused) ... ok
test_memory_ceilings_and_float64_MPS_guard_without_MPS_allocation (__main__.EntryAndGuardTests.test_memory_ceilings_and_float64_MPS_guard_without_MPS_allocation) ... ok
test_outer_error_preserves_durable_measured_population_details (__main__.EntryAndGuardTests.test_outer_error_preserves_durable_measured_population_details) ... PREIMPORT_TIMER_CONTROL remaining_s=3059.98209
HARD_DEADLINE_CONTROL native_GIL_hold=False rc=-14 elapsed_s=0.2177
HARD_DEADLINE_CONTROL native_GIL_hold=True rc=-14 elapsed_s=0.2251
LAUNCHER_HARD_DEADLINE_CONTROL native_GIL_hold=True rc=2 elapsed_s=0.1741
{"decision_id": "D-C10z-v7diag", "outcome": "INCONCLUSIVE", "reason": "TimeoutError: forced final deadline", "completion": "awaiting_worker_exit", "scores": {"F1000": {"E": {"10": "+inf", "11": "+inf", "12": "+inf", "4": "+inf", "5": "+inf", "6": "+inf", "7": "+inf", "8": "+inf", "9": "+inf"}, "P": false, "rho": {"10": 0.79, "11": 0.79, "12": 0.79, "4": 0.79, "5": 0.79, "6": 0.79, "7": 0.79, "8": 0.79, "9": 0.79}}, "R1000": {"E": {"10": "+inf", "11": "+inf", "12": "+inf", "4": "+inf", "5": "+inf", "6": "+inf", "7": "+inf", "8": "+inf", "9": "+inf"}, "P": true, "rho": {"10": 0.8, "11": 0.8, "12": 0.8, "4": 0.8, "5": 0.8, "6": 0.8, "7": 0.8, "8": 0.8, "9": 0.8}}}, "populations_measured": ["F1000", "R1000"], "cap_seconds": 3060, "late_layer_fidelity": "UNVERIFIED", "cpu_agreement_establishes_MPS_equivalence": false, "downstream_requirement": "supervisor-observed exit0 after cleanup plus complete verdict; implementation review before dispatch", "cleanup_completed": true, "deadline_origin": 1378827.508397916, "worker_exit_pending": true}
ok
test_real_entry_CPU_fixture_pins_durable_before_each_forward (__main__.EntryAndGuardTests.test_real_entry_CPU_fixture_pins_durable_before_each_forward) ... {"decision_id": "D-C10z-v7diag", "outcome": "A1", "reason": "exactly pinned R1000 passes P", "completion": "awaiting_worker_exit", "scores": {"F1000": {"rho": {"4": 0.79, "5": 0.79, "6": 0.79, "7": 0.79, "8": 0.79, "9": 0.79, "10": 0.79, "11": 0.79, "12": 0.79}, "E": {"4": "+inf", "5": "+inf", "6": "+inf", "7": "+inf", "8": "+inf", "9": "+inf", "10": "+inf", "11": "+inf", "12": "+inf"}, "P": false}, "R1000": {"rho": {"4": 0.8, "5": 0.8, "6": 0.8, "7": 0.8, "8": 0.8, "9": 0.8, "10": 0.8, "11": 0.8, "12": 0.8}, "E": {"4": "+inf", "5": "+inf", "6": "+inf", "7": "+inf", "8": "+inf", "9": "+inf", "10": "+inf", "11": "+inf", "12": "+inf"}, "P": true}}, "populations_measured": ["F1000", "R1000"], "cap_seconds": 3060, "late_layer_fidelity": "UNVERIFIED", "cpu_agreement_establishes_MPS_equivalence": false, "downstream_requirement": "supervisor-observed exit0 after cleanup plus complete verdict; implementation review before dispatch", "cleanup_completed": true, "deadline_origin": 1378827.508397916, "worker_exit_pending": true}
ok
test_timer_armed_before_namespace_and_initial_publication (__main__.EntryAndGuardTests.test_timer_armed_before_namespace_and_initial_publication) ... {"decision_id": "D-C10z-v7diag", "outcome": "INCONCLUSIVE", "reason": "ValueError: forced setup refusal", "completion": "awaiting_worker_exit", "scores": {}, "populations_measured": [], "cap_seconds": 3060, "late_layer_fidelity": "UNVERIFIED", "cpu_agreement_establishes_MPS_equivalence": false, "downstream_requirement": "supervisor-observed exit0 after cleanup plus complete verdict; implementation review before dispatch", "cleanup_completed": true, "deadline_origin": 1378827.508397916, "worker_exit_pending": true}
ok
test_explicit_cleanup_is_inside_original_deadline_before_success (__main__.FixRoundOneTests.test_explicit_cleanup_is_inside_original_deadline_before_success) ... ok
test_fresh_and_process2_G_retained_before_actual_V8_cholesky_failure (__main__.FixRoundOneTests.test_fresh_and_process2_G_retained_before_actual_V8_cholesky_failure) ... ok
test_invalid_returned_m_is_retained_before_tensor_validation (__main__.FixRoundOneTests.test_invalid_returned_m_is_retained_before_tensor_validation) ... ok
test_returned_m_and_actual_provenance_survive_pin_mismatch (__main__.FixRoundOneTests.test_returned_m_and_actual_provenance_survive_pin_mismatch) ... ok
test_supervisor_admits_only_clean_receipt_and_normal_exit_within_original_cap (__main__.FixRoundOneTests.test_supervisor_admits_only_clean_receipt_and_normal_exit_within_original_cap) ... ok
test_supervisor_retains_fresh_fsynced_halt_after_worker_signal_timeout_crash (__main__.FixRoundOneTests.test_supervisor_retains_fresh_fsynced_halt_after_worker_signal_timeout_crash) ... ok
test_worker_deadline_remains_armed_after_cleanup_until_actual_exit (__main__.FixRoundOneTests.test_worker_deadline_remains_armed_after_cleanup_until_actual_exit) ... ok
test_real_source_cache_model_tokenizer_corruption_is_inconclusive_and_retains_m (__main__.IntegrityTests.test_real_source_cache_model_tokenizer_corruption_is_inconclusive_and_retains_m) ... ok
test_G_failure_also_retains_immediately_obtained_dstats (__main__.PersistenceCorrectionTests.test_G_failure_also_retains_immediately_obtained_dstats) ... ok
test_forced_V7_failure_retains_value_and_provenance_before_G_and_scoring (__main__.PersistenceCorrectionTests.test_forced_V7_failure_retains_value_and_provenance_before_G_and_scoring) ... ok
test_forced_pass_outputs_checks_identical_to_frozen_previous_behavior (__main__.PersistenceCorrectionTests.test_forced_pass_outputs_checks_identical_to_frozen_previous_behavior) ... ok
test_fresh_and_process2_existing_dstats_refuse_overwrite (__main__.PersistenceCorrectionTests.test_fresh_and_process2_existing_dstats_refuse_overwrite) ... ok
test_process2_exact_input_bytes_retained_on_fail_and_pass (__main__.PersistenceCorrectionTests.test_process2_exact_input_bytes_retained_on_fail_and_pass) ... ok
test_process2_missing_G_retains_dstats_before_G_load (__main__.PersistenceCorrectionTests.test_process2_missing_G_retains_dstats_before_G_load) ... ok
test_all_pins_include_every_population_before_forwards (__main__.PinsAndAdmissionTests.test_all_pins_include_every_population_before_forwards) ... ok
test_launcher_existing_namespace_and_worker_gates_refuse_before_probe (__main__.PinsAndAdmissionTests.test_launcher_existing_namespace_and_worker_gates_refuse_before_probe) ... ok
test_local_arrow_revision_length_shards_and_offline_only (__main__.PinsAndAdmissionTests.test_local_arrow_revision_length_shards_and_offline_only) ... ok
test_namespace_refuses_reuse_and_attempt3_path (__main__.PinsAndAdmissionTests.test_namespace_refuses_reuse_and_attempt3_path) ... ok
test_supervised_worker_reuses_only_required_gates_before_forward_entry (__main__.PinsAndAdmissionTests.test_supervised_worker_reuses_only_required_gates_before_forward_entry) ... ok
test_F_pass_stops_and_random_pass_never_measures_R5000 (__main__.ProbePipelineTests.test_F_pass_stops_and_random_pass_never_measures_R5000) ... ok
test_R5000_independent_conditional_A2_and_D (__main__.ProbePipelineTests.test_R5000_independent_conditional_A2_and_D) ... ok
test_incomplete_failure_retains_prior_m_and_no_selection (__main__.ProbePipelineTests.test_incomplete_failure_retains_prior_m_and_no_selection) ... ok
test_scoring_deadline_cannot_publish_A1_or_increase_cap (__main__.ProbePipelineTests.test_scoring_deadline_cannot_publish_A1_or_increase_cap) ... ok
test_tensor_exclusive_flush_fsync_and_provenance (__main__.ProbePipelineTests.test_tensor_exclusive_flush_fsync_and_provenance) ... ok
test_cache_diagonal_count_and_loaded_once (__main__.SelectionAndScoringTests.test_cache_diagonal_count_and_loaded_once) ... ok
test_full_seed_one_permutation_and_exact_population_sizes (__main__.SelectionAndScoringTests.test_full_seed_one_permutation_and_exact_population_sizes) ... ok
test_ordered_routing_equal_boundary_nonfinite_and_report_only_E (__main__.SelectionAndScoringTests.test_ordered_routing_equal_boundary_nonfinite_and_report_only_E) ... ok
test_scoring_uses_driver_spearman_ties_natural_log_and_zero_inf (__main__.SelectionAndScoringTests.test_scoring_uses_driver_spearman_ties_natural_log_and_zero_inf) ... ok
test_actual_driver_bit_identity_and_independent_tokens_counts_normalization (__main__.StatisticTests.test_actual_driver_bit_identity_and_independent_tokens_counts_normalization) ... ok
test_ast_identity_sums_and_loop_only_row_count_varies (__main__.StatisticTests.test_ast_identity_sums_and_loop_only_row_count_varies) ... ok
test_hook_cleanup_after_forward_error (__main__.StatisticTests.test_hook_cleanup_after_forward_error) ... ok

----------------------------------------------------------------------
Ran 40 tests in 9.016s

OK
FIX1_CLEANUP_CONTROL rc=-14 cleanup_started=True cleanup_done=False elapsed_s=0.2123
FIX1_V8_CONTROL process2=False dstats=True G=True
FIX1_V8_CONTROL process2=True dstats=True G=True
FIX1_MISMATCH_CONTROL outcome=INCONCLUSIVE retained_m=True
FIX1_TERMINATION_CONTROL mode=signal rc=2 files=['halt_diagnostic_20261009T174704.394903Z.json', 'supervisor.json', 'verdict.json', 'worker.log']
FIX1_TERMINATION_CONTROL mode=timeout rc=2 files=['halt_diagnostic_20261009T174704.568086Z.json', 'supervisor.json', 'verdict.json', 'worker.log']
FIX1_TERMINATION_CONTROL mode=crash rc=2 files=['halt_diagnostic_20261009T174704.647383Z.json', 'supervisor.json', 'verdict.json', 'worker.log']
FIX1_WORKER_EXIT_CONTROL rc=-14 cleanup_done=True
C10Z_V7_DIAG_SELFTEST_PASS tests=40
```

#### Actual unchanged GPU-gate classification RED: 41 tests, one failure; parent plus worker alone falsely refuse

Artifact:`/private/tmp/c10z_v7diag_fix1/parent_inventory_red.txt`; captured command exit 1.

```text
CPU_ONLY: MPS availability forced false; unmocked MPS calls forbidden; no model load
test_CLI_bootstrap_timer_exists_before_driver_import (__main__.DeadlineTests.test_CLI_bootstrap_timer_exists_before_driver_import) ... ok
test_OS_timer_terminates_sleep_and_native_GIL_hold_retains_inconclusive (__main__.DeadlineTests.test_OS_timer_terminates_sleep_and_native_GIL_hold_retains_inconclusive) ... ok
test_immutable_3060_includes_preimport_and_exact_boundary (__main__.DeadlineTests.test_immutable_3060_includes_preimport_and_exact_boundary) ... ok
test_launcher_native_block_is_bounded_before_probe_dispatch (__main__.DeadlineTests.test_launcher_native_block_is_bounded_before_probe_dispatch) ... ok
test_launcher_origin_carried_and_future_or_nonfinite_origin_refused (__main__.DeadlineTests.test_launcher_origin_carried_and_future_or_nonfinite_origin_refused) ... ok
test_memory_ceilings_and_float64_MPS_guard_without_MPS_allocation (__main__.EntryAndGuardTests.test_memory_ceilings_and_float64_MPS_guard_without_MPS_allocation) ... ok
test_outer_error_preserves_durable_measured_population_details (__main__.EntryAndGuardTests.test_outer_error_preserves_durable_measured_population_details) ... PREIMPORT_TIMER_CONTROL remaining_s=3059.982593
HARD_DEADLINE_CONTROL native_GIL_hold=False rc=-14 elapsed_s=0.2139
HARD_DEADLINE_CONTROL native_GIL_hold=True rc=-14 elapsed_s=0.2231
LAUNCHER_HARD_DEADLINE_CONTROL native_GIL_hold=True rc=2 elapsed_s=0.1901
{"decision_id": "D-C10z-v7diag", "outcome": "INCONCLUSIVE", "reason": "TimeoutError: forced final deadline", "completion": "awaiting_worker_exit", "scores": {"F1000": {"E": {"10": "+inf", "11": "+inf", "12": "+inf", "4": "+inf", "5": "+inf", "6": "+inf", "7": "+inf", "8": "+inf", "9": "+inf"}, "P": false, "rho": {"10": 0.79, "11": 0.79, "12": 0.79, "4": 0.79, "5": 0.79, "6": 0.79, "7": 0.79, "8": 0.79, "9": 0.79}}, "R1000": {"E": {"10": "+inf", "11": "+inf", "12": "+inf", "4": "+inf", "5": "+inf", "6": "+inf", "7": "+inf", "8": "+inf", "9": "+inf"}, "P": true, "rho": {"10": 0.8, "11": 0.8, "12": 0.8, "4": 0.8, "5": 0.8, "6": 0.8, "7": 0.8, "8": 0.8, "9": 0.8}}}, "populations_measured": ["F1000", "R1000"], "cap_seconds": 3060, "late_layer_fidelity": "UNVERIFIED", "cpu_agreement_establishes_MPS_equivalence": false, "downstream_requirement": "supervisor-observed exit0 after cleanup plus complete verdict; implementation review before dispatch", "cleanup_completed": true, "deadline_origin": 1379252.343024125, "worker_exit_pending": true}
ok
test_real_entry_CPU_fixture_pins_durable_before_each_forward (__main__.EntryAndGuardTests.test_real_entry_CPU_fixture_pins_durable_before_each_forward) ... {"decision_id": "D-C10z-v7diag", "outcome": "A1", "reason": "exactly pinned R1000 passes P", "completion": "awaiting_worker_exit", "scores": {"F1000": {"rho": {"4": 0.79, "5": 0.79, "6": 0.79, "7": 0.79, "8": 0.79, "9": 0.79, "10": 0.79, "11": 0.79, "12": 0.79}, "E": {"4": "+inf", "5": "+inf", "6": "+inf", "7": "+inf", "8": "+inf", "9": "+inf", "10": "+inf", "11": "+inf", "12": "+inf"}, "P": false}, "R1000": {"rho": {"4": 0.8, "5": 0.8, "6": 0.8, "7": 0.8, "8": 0.8, "9": 0.8, "10": 0.8, "11": 0.8, "12": 0.8}, "E": {"4": "+inf", "5": "+inf", "6": "+inf", "7": "+inf", "8": "+inf", "9": "+inf", "10": "+inf", "11": "+inf", "12": "+inf"}, "P": true}}, "populations_measured": ["F1000", "R1000"], "cap_seconds": 3060, "late_layer_fidelity": "UNVERIFIED", "cpu_agreement_establishes_MPS_equivalence": false, "downstream_requirement": "supervisor-observed exit0 after cleanup plus complete verdict; implementation review before dispatch", "cleanup_completed": true, "deadline_origin": 1379252.343024125, "worker_exit_pending": true}
ok
test_timer_armed_before_namespace_and_initial_publication (__main__.EntryAndGuardTests.test_timer_armed_before_namespace_and_initial_publication) ... {"decision_id": "D-C10z-v7diag", "outcome": "INCONCLUSIVE", "reason": "ValueError: forced setup refusal", "completion": "awaiting_worker_exit", "scores": {}, "populations_measured": [], "cap_seconds": 3060, "late_layer_fidelity": "UNVERIFIED", "cpu_agreement_establishes_MPS_equivalence": false, "downstream_requirement": "supervisor-observed exit0 after cleanup plus complete verdict; implementation review before dispatch", "cleanup_completed": true, "deadline_origin": 1379252.343024125, "worker_exit_pending": true}
ok
test_explicit_cleanup_is_inside_original_deadline_before_success (__main__.FixRoundOneTests.test_explicit_cleanup_is_inside_original_deadline_before_success) ... ok
test_fresh_and_process2_G_retained_before_actual_V8_cholesky_failure (__main__.FixRoundOneTests.test_fresh_and_process2_G_retained_before_actual_V8_cholesky_failure) ... ok
test_invalid_returned_m_is_retained_before_tensor_validation (__main__.FixRoundOneTests.test_invalid_returned_m_is_retained_before_tensor_validation) ... ok
test_real_gpu_gate_excludes_only_verified_parent_and_still_blocks_competing_job (__main__.FixRoundOneTests.test_real_gpu_gate_excludes_only_verified_parent_and_still_blocks_competing_job) ... 
  test_real_gpu_gate_excludes_only_verified_parent_and_still_blocks_competing_job (__main__.FixRoundOneTests.test_real_gpu_gate_excludes_only_verified_parent_and_still_blocks_competing_job) (mode='idle') ... FAIL
test_returned_m_and_actual_provenance_survive_pin_mismatch (__main__.FixRoundOneTests.test_returned_m_and_actual_provenance_survive_pin_mismatch) ... ok
test_supervisor_admits_only_clean_receipt_and_normal_exit_within_original_cap (__main__.FixRoundOneTests.test_supervisor_admits_only_clean_receipt_and_normal_exit_within_original_cap) ... ok
test_supervisor_retains_fresh_fsynced_halt_after_worker_signal_timeout_crash (__main__.FixRoundOneTests.test_supervisor_retains_fresh_fsynced_halt_after_worker_signal_timeout_crash) ... ok
test_worker_deadline_remains_armed_after_cleanup_until_actual_exit (__main__.FixRoundOneTests.test_worker_deadline_remains_armed_after_cleanup_until_actual_exit) ... ok
test_real_source_cache_model_tokenizer_corruption_is_inconclusive_and_retains_m (__main__.IntegrityTests.test_real_source_cache_model_tokenizer_corruption_is_inconclusive_and_retains_m) ... ok
test_G_failure_also_retains_immediately_obtained_dstats (__main__.PersistenceCorrectionTests.test_G_failure_also_retains_immediately_obtained_dstats) ... ok
test_forced_V7_failure_retains_value_and_provenance_before_G_and_scoring (__main__.PersistenceCorrectionTests.test_forced_V7_failure_retains_value_and_provenance_before_G_and_scoring) ... ok
test_forced_pass_outputs_checks_identical_to_frozen_previous_behavior (__main__.PersistenceCorrectionTests.test_forced_pass_outputs_checks_identical_to_frozen_previous_behavior) ... ok
test_fresh_and_process2_existing_dstats_refuse_overwrite (__main__.PersistenceCorrectionTests.test_fresh_and_process2_existing_dstats_refuse_overwrite) ... ok
test_process2_exact_input_bytes_retained_on_fail_and_pass (__main__.PersistenceCorrectionTests.test_process2_exact_input_bytes_retained_on_fail_and_pass) ... ok
test_process2_missing_G_retains_dstats_before_G_load (__main__.PersistenceCorrectionTests.test_process2_missing_G_retains_dstats_before_G_load) ... ok
test_all_pins_include_every_population_before_forwards (__main__.PinsAndAdmissionTests.test_all_pins_include_every_population_before_forwards) ... ok
test_launcher_existing_namespace_and_worker_gates_refuse_before_probe (__main__.PinsAndAdmissionTests.test_launcher_existing_namespace_and_worker_gates_refuse_before_probe) ... ok
test_local_arrow_revision_length_shards_and_offline_only (__main__.PinsAndAdmissionTests.test_local_arrow_revision_length_shards_and_offline_only) ... ok
test_namespace_refuses_reuse_and_attempt3_path (__main__.PinsAndAdmissionTests.test_namespace_refuses_reuse_and_attempt3_path) ... ok
test_supervised_worker_reuses_only_required_gates_before_forward_entry (__main__.PinsAndAdmissionTests.test_supervised_worker_reuses_only_required_gates_before_forward_entry) ... ok
test_F_pass_stops_and_random_pass_never_measures_R5000 (__main__.ProbePipelineTests.test_F_pass_stops_and_random_pass_never_measures_R5000) ... ok
test_R5000_independent_conditional_A2_and_D (__main__.ProbePipelineTests.test_R5000_independent_conditional_A2_and_D) ... ok
test_incomplete_failure_retains_prior_m_and_no_selection (__main__.ProbePipelineTests.test_incomplete_failure_retains_prior_m_and_no_selection) ... ok
test_scoring_deadline_cannot_publish_A1_or_increase_cap (__main__.ProbePipelineTests.test_scoring_deadline_cannot_publish_A1_or_increase_cap) ... ok
test_tensor_exclusive_flush_fsync_and_provenance (__main__.ProbePipelineTests.test_tensor_exclusive_flush_fsync_and_provenance) ... ok
test_cache_diagonal_count_and_loaded_once (__main__.SelectionAndScoringTests.test_cache_diagonal_count_and_loaded_once) ... ok
test_full_seed_one_permutation_and_exact_population_sizes (__main__.SelectionAndScoringTests.test_full_seed_one_permutation_and_exact_population_sizes) ... ok
test_ordered_routing_equal_boundary_nonfinite_and_report_only_E (__main__.SelectionAndScoringTests.test_ordered_routing_equal_boundary_nonfinite_and_report_only_E) ... ok
test_scoring_uses_driver_spearman_ties_natural_log_and_zero_inf (__main__.SelectionAndScoringTests.test_scoring_uses_driver_spearman_ties_natural_log_and_zero_inf) ... ok
test_actual_driver_bit_identity_and_independent_tokens_counts_normalization (__main__.StatisticTests.test_actual_driver_bit_identity_and_independent_tokens_counts_normalization) ... ok
test_ast_identity_sums_and_loop_only_row_count_varies (__main__.StatisticTests.test_ast_identity_sums_and_loop_only_row_count_varies) ... ok
test_hook_cleanup_after_forward_error (__main__.StatisticTests.test_hook_cleanup_after_forward_error) ... ok

======================================================================
FAIL: test_real_gpu_gate_excludes_only_verified_parent_and_still_blocks_competing_job (__main__.FixRoundOneTests.test_real_gpu_gate_excludes_only_verified_parent_and_still_blocks_competing_job) (mode='idle')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 884, in test_real_gpu_gate_excludes_only_verified_parent_and_still_blocks_competing_job
    self.assertEqual(bool(entered), mode == "idle", "verified model-free supervisor counted as competing compute")
AssertionError: False != True : verified model-free supervisor counted as competing compute

----------------------------------------------------------------------
Ran 41 tests in 9.084s

FAILED (failures=1)
FIX1_CLEANUP_CONTROL rc=-14 cleanup_started=True cleanup_done=False elapsed_s=0.2115
FIX1_V8_CONTROL process2=False dstats=True G=True
FIX1_V8_CONTROL process2=True dstats=True G=True
FIX1_PARENT_INVENTORY_CONTROL mode=idle reached_entry=False refusal=['gpu exclusivity refused: {"ok": false, "blocking_processes": ["60001 /private/tmp/c10z_v7diag_fix1/tmpnhtvk8tf/.venv/bin/python -B /private/tmp/c10z_v7diag_fix1/tmpnhtvk8tf/tools/run_c10z_v7_diag.py --utc 20261009T000000Z"], "blocking_tmux": []}']
FIX1_PARENT_INVENTORY_CONTROL mode=competing reached_entry=False refusal=['gpu exclusivity refused: {"ok": false, "blocking_processes": ["60001 /private/tmp/c10z_v7diag_fix1/tmpahnkfodq/.venv/bin/python -B /private/tmp/c10z_v7diag_fix1/tmpahnkfodq/tools/run_c10z_v7_diag.py --utc 20261009T000000Z", "60003 /private/tmp/c10z_v7diag_fix1/tmpahnkfodq/.venv/bin/python c10y_calibration4.py"], "blocking_tmux": []}']
FIX1_PARENT_INVENTORY_CONTROL mode=different_command reached_entry=False refusal=['gpu exclusivity refused: {"ok": false, "blocking_processes": ["60001 /private/tmp/c10z_v7diag_fix1/tmpxj3nw2qb/.venv/bin/python unrelated_training.py"], "blocking_tmux": []}']
FIX1_MISMATCH_CONTROL outcome=INCONCLUSIVE retained_m=True
FIX1_TERMINATION_CONTROL mode=signal rc=2 files=['halt_diagnostic_20261009T175409.255742Z.json', 'supervisor.json', 'verdict.json', 'worker.log']
FIX1_TERMINATION_CONTROL mode=timeout rc=2 files=['halt_diagnostic_20261009T175409.432826Z.json', 'supervisor.json', 'verdict.json', 'worker.log']
FIX1_TERMINATION_CONTROL mode=crash rc=2 files=['halt_diagnostic_20261009T175409.520698Z.json', 'supervisor.json', 'verdict.json', 'worker.log']
FIX1_WORKER_EXIT_CONTROL rc=-14 cleanup_done=True
C10Z_V7_DIAG_SELFTEST_FAIL tests=41
```

#### Intermediate validation: parent inventory is GREEN; 41 tests, two cleanup-fixture failures caused by missing model-free tools import in the isolated subprocess

Artifact:`/private/tmp/c10z_v7diag_fix1/probe_green_final.txt`; captured command exit 1.

```text
CPU_ONLY: MPS availability forced false; unmocked MPS calls forbidden; no model load
test_CLI_bootstrap_timer_exists_before_driver_import (__main__.DeadlineTests.test_CLI_bootstrap_timer_exists_before_driver_import) ... ok
test_OS_timer_terminates_sleep_and_native_GIL_hold_retains_inconclusive (__main__.DeadlineTests.test_OS_timer_terminates_sleep_and_native_GIL_hold_retains_inconclusive) ... ok
test_immutable_3060_includes_preimport_and_exact_boundary (__main__.DeadlineTests.test_immutable_3060_includes_preimport_and_exact_boundary) ... ok
test_launcher_native_block_is_bounded_before_probe_dispatch (__main__.DeadlineTests.test_launcher_native_block_is_bounded_before_probe_dispatch) ... ok
test_launcher_origin_carried_and_future_or_nonfinite_origin_refused (__main__.DeadlineTests.test_launcher_origin_carried_and_future_or_nonfinite_origin_refused) ... ok
test_memory_ceilings_and_float64_MPS_guard_without_MPS_allocation (__main__.EntryAndGuardTests.test_memory_ceilings_and_float64_MPS_guard_without_MPS_allocation) ... ok
test_outer_error_preserves_durable_measured_population_details (__main__.EntryAndGuardTests.test_outer_error_preserves_durable_measured_population_details) ... PREIMPORT_TIMER_CONTROL remaining_s=3059.982513
HARD_DEADLINE_CONTROL native_GIL_hold=False rc=-14 elapsed_s=0.2097
HARD_DEADLINE_CONTROL native_GIL_hold=True rc=-14 elapsed_s=0.2322
LAUNCHER_HARD_DEADLINE_CONTROL native_GIL_hold=True rc=2 elapsed_s=0.1813
{"decision_id": "D-C10z-v7diag", "outcome": "INCONCLUSIVE", "reason": "TimeoutError: forced final deadline", "completion": "awaiting_worker_exit", "scores": {"F1000": {"E": {"10": "+inf", "11": "+inf", "12": "+inf", "4": "+inf", "5": "+inf", "6": "+inf", "7": "+inf", "8": "+inf", "9": "+inf"}, "P": false, "rho": {"10": 0.79, "11": 0.79, "12": 0.79, "4": 0.79, "5": 0.79, "6": 0.79, "7": 0.79, "8": 0.79, "9": 0.79}}, "R1000": {"E": {"10": "+inf", "11": "+inf", "12": "+inf", "4": "+inf", "5": "+inf", "6": "+inf", "7": "+inf", "8": "+inf", "9": "+inf"}, "P": true, "rho": {"10": 0.8, "11": 0.8, "12": 0.8, "4": 0.8, "5": 0.8, "6": 0.8, "7": 0.8, "8": 0.8, "9": 0.8}}}, "populations_measured": ["F1000", "R1000"], "cap_seconds": 3060, "late_layer_fidelity": "UNVERIFIED", "cpu_agreement_establishes_MPS_equivalence": false, "downstream_requirement": "supervisor-observed exit0 after cleanup plus complete verdict; implementation review before dispatch", "cleanup_completed": true, "deadline_origin": 1379392.555487291, "worker_exit_pending": true}
ok
test_real_entry_CPU_fixture_pins_durable_before_each_forward (__main__.EntryAndGuardTests.test_real_entry_CPU_fixture_pins_durable_before_each_forward) ... {"decision_id": "D-C10z-v7diag", "outcome": "A1", "reason": "exactly pinned R1000 passes P", "completion": "awaiting_worker_exit", "scores": {"F1000": {"rho": {"4": 0.79, "5": 0.79, "6": 0.79, "7": 0.79, "8": 0.79, "9": 0.79, "10": 0.79, "11": 0.79, "12": 0.79}, "E": {"4": "+inf", "5": "+inf", "6": "+inf", "7": "+inf", "8": "+inf", "9": "+inf", "10": "+inf", "11": "+inf", "12": "+inf"}, "P": false}, "R1000": {"rho": {"4": 0.8, "5": 0.8, "6": 0.8, "7": 0.8, "8": 0.8, "9": 0.8, "10": 0.8, "11": 0.8, "12": 0.8}, "E": {"4": "+inf", "5": "+inf", "6": "+inf", "7": "+inf", "8": "+inf", "9": "+inf", "10": "+inf", "11": "+inf", "12": "+inf"}, "P": true}}, "populations_measured": ["F1000", "R1000"], "cap_seconds": 3060, "late_layer_fidelity": "UNVERIFIED", "cpu_agreement_establishes_MPS_equivalence": false, "downstream_requirement": "supervisor-observed exit0 after cleanup plus complete verdict; implementation review before dispatch", "cleanup_completed": true, "deadline_origin": 1379392.555487291, "worker_exit_pending": true}
ok
test_timer_armed_before_namespace_and_initial_publication (__main__.EntryAndGuardTests.test_timer_armed_before_namespace_and_initial_publication) ... {"decision_id": "D-C10z-v7diag", "outcome": "INCONCLUSIVE", "reason": "ValueError: forced setup refusal", "completion": "awaiting_worker_exit", "scores": {}, "populations_measured": [], "cap_seconds": 3060, "late_layer_fidelity": "UNVERIFIED", "cpu_agreement_establishes_MPS_equivalence": false, "downstream_requirement": "supervisor-observed exit0 after cleanup plus complete verdict; implementation review before dispatch", "cleanup_completed": true, "deadline_origin": 1379392.555487291, "worker_exit_pending": true}
ok
test_explicit_cleanup_is_inside_original_deadline_before_success (__main__.FixRoundOneTests.test_explicit_cleanup_is_inside_original_deadline_before_success) ... FAIL
test_fresh_and_process2_G_retained_before_actual_V8_cholesky_failure (__main__.FixRoundOneTests.test_fresh_and_process2_G_retained_before_actual_V8_cholesky_failure) ... ok
test_invalid_returned_m_is_retained_before_tensor_validation (__main__.FixRoundOneTests.test_invalid_returned_m_is_retained_before_tensor_validation) ... ok
test_real_gpu_gate_excludes_only_verified_parent_and_still_blocks_competing_job (__main__.FixRoundOneTests.test_real_gpu_gate_excludes_only_verified_parent_and_still_blocks_competing_job) ... ok
test_returned_m_and_actual_provenance_survive_pin_mismatch (__main__.FixRoundOneTests.test_returned_m_and_actual_provenance_survive_pin_mismatch) ... ok
test_supervisor_admits_only_clean_receipt_and_normal_exit_within_original_cap (__main__.FixRoundOneTests.test_supervisor_admits_only_clean_receipt_and_normal_exit_within_original_cap) ... ok
test_supervisor_retains_fresh_fsynced_halt_after_worker_signal_timeout_crash (__main__.FixRoundOneTests.test_supervisor_retains_fresh_fsynced_halt_after_worker_signal_timeout_crash) ... ok
test_worker_deadline_remains_armed_after_cleanup_until_actual_exit (__main__.FixRoundOneTests.test_worker_deadline_remains_armed_after_cleanup_until_actual_exit) ... FAIL
test_real_source_cache_model_tokenizer_corruption_is_inconclusive_and_retains_m (__main__.IntegrityTests.test_real_source_cache_model_tokenizer_corruption_is_inconclusive_and_retains_m) ... ok
test_G_failure_also_retains_immediately_obtained_dstats (__main__.PersistenceCorrectionTests.test_G_failure_also_retains_immediately_obtained_dstats) ... ok
test_forced_V7_failure_retains_value_and_provenance_before_G_and_scoring (__main__.PersistenceCorrectionTests.test_forced_V7_failure_retains_value_and_provenance_before_G_and_scoring) ... ok
test_forced_pass_outputs_checks_identical_to_frozen_previous_behavior (__main__.PersistenceCorrectionTests.test_forced_pass_outputs_checks_identical_to_frozen_previous_behavior) ... ok
test_fresh_and_process2_existing_dstats_refuse_overwrite (__main__.PersistenceCorrectionTests.test_fresh_and_process2_existing_dstats_refuse_overwrite) ... ok
test_process2_exact_input_bytes_retained_on_fail_and_pass (__main__.PersistenceCorrectionTests.test_process2_exact_input_bytes_retained_on_fail_and_pass) ... ok
test_process2_missing_G_retains_dstats_before_G_load (__main__.PersistenceCorrectionTests.test_process2_missing_G_retains_dstats_before_G_load) ... ok
test_all_pins_include_every_population_before_forwards (__main__.PinsAndAdmissionTests.test_all_pins_include_every_population_before_forwards) ... ok
test_launcher_existing_namespace_and_worker_gates_refuse_before_probe (__main__.PinsAndAdmissionTests.test_launcher_existing_namespace_and_worker_gates_refuse_before_probe) ... ok
test_local_arrow_revision_length_shards_and_offline_only (__main__.PinsAndAdmissionTests.test_local_arrow_revision_length_shards_and_offline_only) ... ok
test_namespace_refuses_reuse_and_attempt3_path (__main__.PinsAndAdmissionTests.test_namespace_refuses_reuse_and_attempt3_path) ... ok
test_supervised_worker_reuses_only_required_gates_before_forward_entry (__main__.PinsAndAdmissionTests.test_supervised_worker_reuses_only_required_gates_before_forward_entry) ... ok
test_F_pass_stops_and_random_pass_never_measures_R5000 (__main__.ProbePipelineTests.test_F_pass_stops_and_random_pass_never_measures_R5000) ... ok
test_R5000_independent_conditional_A2_and_D (__main__.ProbePipelineTests.test_R5000_independent_conditional_A2_and_D) ... ok
test_incomplete_failure_retains_prior_m_and_no_selection (__main__.ProbePipelineTests.test_incomplete_failure_retains_prior_m_and_no_selection) ... ok
test_scoring_deadline_cannot_publish_A1_or_increase_cap (__main__.ProbePipelineTests.test_scoring_deadline_cannot_publish_A1_or_increase_cap) ... ok
test_tensor_exclusive_flush_fsync_and_provenance (__main__.ProbePipelineTests.test_tensor_exclusive_flush_fsync_and_provenance) ... ok
test_cache_diagonal_count_and_loaded_once (__main__.SelectionAndScoringTests.test_cache_diagonal_count_and_loaded_once) ... ok
test_full_seed_one_permutation_and_exact_population_sizes (__main__.SelectionAndScoringTests.test_full_seed_one_permutation_and_exact_population_sizes) ... ok
test_ordered_routing_equal_boundary_nonfinite_and_report_only_E (__main__.SelectionAndScoringTests.test_ordered_routing_equal_boundary_nonfinite_and_report_only_E) ... ok
test_scoring_uses_driver_spearman_ties_natural_log_and_zero_inf (__main__.SelectionAndScoringTests.test_scoring_uses_driver_spearman_ties_natural_log_and_zero_inf) ... ok
test_actual_driver_bit_identity_and_independent_tokens_counts_normalization (__main__.StatisticTests.test_actual_driver_bit_identity_and_independent_tokens_counts_normalization) ... ok
test_ast_identity_sums_and_loop_only_row_count_varies (__main__.StatisticTests.test_ast_identity_sums_and_loop_only_row_count_varies) ... ok
test_hook_cleanup_after_forward_error (__main__.StatisticTests.test_hook_cleanup_after_forward_error) ... ok

======================================================================
FAIL: test_explicit_cleanup_is_inside_original_deadline_before_success (__main__.FixRoundOneTests.test_explicit_cleanup_is_inside_original_deadline_before_success)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 787, in test_explicit_cleanup_is_inside_original_deadline_before_success
    self.assertEqual(child.returncode, -signal.SIGALRM, "cleanup completed after deadline because timer was cancelled")
AssertionError: 2 != -14 : cleanup completed after deadline because timer was cancelled

======================================================================
FAIL: test_worker_deadline_remains_armed_after_cleanup_until_actual_exit (__main__.FixRoundOneTests.test_worker_deadline_remains_armed_after_cleanup_until_actual_exit)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 800, in test_worker_deadline_remains_armed_after_cleanup_until_actual_exit
    self.assertTrue((Path(tmp) / "cleanup_done").is_file())
AssertionError: False is not true

----------------------------------------------------------------------
Ran 41 tests in 8.910s

FAILED (failures=2)
FIX1_CLEANUP_CONTROL rc=2 cleanup_started=False cleanup_done=False elapsed_s=0.0691
FIX1_V8_CONTROL process2=False dstats=True G=True
FIX1_V8_CONTROL process2=True dstats=True G=True
FIX1_PARENT_INVENTORY_CONTROL mode=idle reached_entry=True refusal=[]
FIX1_PARENT_INVENTORY_CONTROL mode=competing reached_entry=False refusal=['gpu exclusivity refused: {"ok": false, "blocking_processes": ["60003 /private/tmp/c10z_v7diag_fix1/tmp6_hzfwfg/.venv/bin/python c10y_calibration4.py"], "blocking_tmux": [], "verified_model_free_supervisor": ["60001 /private/tmp/c10z_v7diag_fix1/tmp6_hzfwfg/.venv/bin/python -B /private/tmp/c10z_v7diag_fix1/tmp6_hzfwfg/tools/run_c10z_v7_diag.py --utc 20261009T000000Z"]}']
FIX1_PARENT_INVENTORY_CONTROL mode=different_command reached_entry=False refusal=['gpu exclusivity refused: {"ok": false, "blocking_processes": ["60001 /private/tmp/c10z_v7diag_fix1/tmpszk96obx/.venv/bin/python unrelated_training.py"], "blocking_tmux": [], "verified_model_free_supervisor": []}']
FIX1_MISMATCH_CONTROL outcome=INCONCLUSIVE retained_m=True
FIX1_TERMINATION_CONTROL mode=signal rc=2 files=['halt_diagnostic_20261009T175629.290185Z.json', 'supervisor.json', 'verdict.json', 'worker.log']
FIX1_TERMINATION_CONTROL mode=timeout rc=2 files=['halt_diagnostic_20261009T175629.465874Z.json', 'supervisor.json', 'verdict.json', 'worker.log']
FIX1_TERMINATION_CONTROL mode=crash rc=2 files=['halt_diagnostic_20261009T175629.541000Z.json', 'supervisor.json', 'verdict.json', 'worker.log']
FIX1_WORKER_EXIT_CONTROL rc=-14 cleanup_done=False
C10Z_V7_DIAG_SELFTEST_FAIL tests=41
```

#### Observation-layer positive diagnosis: captured control returns 2 with explicit ModuleNotFoundError for run_c10z_v7_diag before model-stub acquisition

Artifact:`/private/tmp/c10z_v7diag_fix1/cleanup_fixture_observation.txt`; captured command exit 0.

```text
CONTROL_RC 2
STDOUT {"decision_id": "D-C10z-v7diag", "outcome": "INCONCLUSIVE", "reason": "ModuleNotFoundError: No module named 'run_c10z_v7_diag'", "completion": "awaiting_worker_exit", "scores": {}, "populations_measured": [], "cap_seconds": 0.15, "late_layer_fidelity": "UNVERIFIED", "cpu_agreement_establishes_MPS_equivalence": false, "downstream_requirement": "supervisor-observed exit0 after cleanup plus complete verdict; implementation review before dispatch", "cleanup_completed": true, "deadline_origin": 1379530.128141166, "worker_exit_pending": true}

STDERR 
```

#### Strengthened terminal-detail RED: 41 tests, one failure; cleanup controls now GREEN, late outer exception drops already recorded mismatch detail

Artifact:`/private/tmp/c10z_v7diag_fix1/mismatch_detail_red.txt`; captured command exit 1.

```text
CPU_ONLY: MPS availability forced false; unmocked MPS calls forbidden; no model load
test_CLI_bootstrap_timer_exists_before_driver_import (__main__.DeadlineTests.test_CLI_bootstrap_timer_exists_before_driver_import) ... ok
test_OS_timer_terminates_sleep_and_native_GIL_hold_retains_inconclusive (__main__.DeadlineTests.test_OS_timer_terminates_sleep_and_native_GIL_hold_retains_inconclusive) ... ok
test_immutable_3060_includes_preimport_and_exact_boundary (__main__.DeadlineTests.test_immutable_3060_includes_preimport_and_exact_boundary) ... ok
test_launcher_native_block_is_bounded_before_probe_dispatch (__main__.DeadlineTests.test_launcher_native_block_is_bounded_before_probe_dispatch) ... ok
test_launcher_origin_carried_and_future_or_nonfinite_origin_refused (__main__.DeadlineTests.test_launcher_origin_carried_and_future_or_nonfinite_origin_refused) ... ok
test_memory_ceilings_and_float64_MPS_guard_without_MPS_allocation (__main__.EntryAndGuardTests.test_memory_ceilings_and_float64_MPS_guard_without_MPS_allocation) ... ok
test_outer_error_preserves_durable_measured_population_details (__main__.EntryAndGuardTests.test_outer_error_preserves_durable_measured_population_details) ... PREIMPORT_TIMER_CONTROL remaining_s=3059.982177
HARD_DEADLINE_CONTROL native_GIL_hold=False rc=-14 elapsed_s=0.2187
HARD_DEADLINE_CONTROL native_GIL_hold=True rc=-14 elapsed_s=0.2231
LAUNCHER_HARD_DEADLINE_CONTROL native_GIL_hold=True rc=2 elapsed_s=0.1912
{"decision_id": "D-C10z-v7diag", "outcome": "INCONCLUSIVE", "reason": "TimeoutError: forced final deadline", "completion": "awaiting_worker_exit", "scores": {"F1000": {"E": {"10": "+inf", "11": "+inf", "12": "+inf", "4": "+inf", "5": "+inf", "6": "+inf", "7": "+inf", "8": "+inf", "9": "+inf"}, "P": false, "rho": {"10": 0.79, "11": 0.79, "12": 0.79, "4": 0.79, "5": 0.79, "6": 0.79, "7": 0.79, "8": 0.79, "9": 0.79}}, "R1000": {"E": {"10": "+inf", "11": "+inf", "12": "+inf", "4": "+inf", "5": "+inf", "6": "+inf", "7": "+inf", "8": "+inf", "9": "+inf"}, "P": true, "rho": {"10": 0.8, "11": 0.8, "12": 0.8, "4": 0.8, "5": 0.8, "6": 0.8, "7": 0.8, "8": 0.8, "9": 0.8}}}, "populations_measured": ["F1000", "R1000"], "cap_seconds": 3060, "late_layer_fidelity": "UNVERIFIED", "cpu_agreement_establishes_MPS_equivalence": false, "downstream_requirement": "supervisor-observed exit0 after cleanup plus complete verdict; implementation review before dispatch", "cleanup_completed": true, "deadline_origin": 1379611.14349875, "worker_exit_pending": true}
FAIL
test_real_entry_CPU_fixture_pins_durable_before_each_forward (__main__.EntryAndGuardTests.test_real_entry_CPU_fixture_pins_durable_before_each_forward) ... {"decision_id": "D-C10z-v7diag", "outcome": "A1", "reason": "exactly pinned R1000 passes P", "completion": "awaiting_worker_exit", "scores": {"F1000": {"rho": {"4": 0.79, "5": 0.79, "6": 0.79, "7": 0.79, "8": 0.79, "9": 0.79, "10": 0.79, "11": 0.79, "12": 0.79}, "E": {"4": "+inf", "5": "+inf", "6": "+inf", "7": "+inf", "8": "+inf", "9": "+inf", "10": "+inf", "11": "+inf", "12": "+inf"}, "P": false}, "R1000": {"rho": {"4": 0.8, "5": 0.8, "6": 0.8, "7": 0.8, "8": 0.8, "9": 0.8, "10": 0.8, "11": 0.8, "12": 0.8}, "E": {"4": "+inf", "5": "+inf", "6": "+inf", "7": "+inf", "8": "+inf", "9": "+inf", "10": "+inf", "11": "+inf", "12": "+inf"}, "P": true}}, "populations_measured": ["F1000", "R1000"], "cap_seconds": 3060, "late_layer_fidelity": "UNVERIFIED", "cpu_agreement_establishes_MPS_equivalence": false, "downstream_requirement": "supervisor-observed exit0 after cleanup plus complete verdict; implementation review before dispatch", "cleanup_completed": true, "deadline_origin": 1379611.14349875, "worker_exit_pending": true}
ok
test_timer_armed_before_namespace_and_initial_publication (__main__.EntryAndGuardTests.test_timer_armed_before_namespace_and_initial_publication) ... {"decision_id": "D-C10z-v7diag", "outcome": "INCONCLUSIVE", "reason": "ValueError: forced setup refusal", "completion": "awaiting_worker_exit", "scores": {}, "populations_measured": [], "cap_seconds": 3060, "late_layer_fidelity": "UNVERIFIED", "cpu_agreement_establishes_MPS_equivalence": false, "downstream_requirement": "supervisor-observed exit0 after cleanup plus complete verdict; implementation review before dispatch", "cleanup_completed": true, "deadline_origin": 1379611.14349875, "worker_exit_pending": true}
ok
test_explicit_cleanup_is_inside_original_deadline_before_success (__main__.FixRoundOneTests.test_explicit_cleanup_is_inside_original_deadline_before_success) ... ok
test_fresh_and_process2_G_retained_before_actual_V8_cholesky_failure (__main__.FixRoundOneTests.test_fresh_and_process2_G_retained_before_actual_V8_cholesky_failure) ... ok
test_invalid_returned_m_is_retained_before_tensor_validation (__main__.FixRoundOneTests.test_invalid_returned_m_is_retained_before_tensor_validation) ... ok
test_real_gpu_gate_excludes_only_verified_parent_and_still_blocks_competing_job (__main__.FixRoundOneTests.test_real_gpu_gate_excludes_only_verified_parent_and_still_blocks_competing_job) ... ok
test_returned_m_and_actual_provenance_survive_pin_mismatch (__main__.FixRoundOneTests.test_returned_m_and_actual_provenance_survive_pin_mismatch) ... ok
test_supervisor_admits_only_clean_receipt_and_normal_exit_within_original_cap (__main__.FixRoundOneTests.test_supervisor_admits_only_clean_receipt_and_normal_exit_within_original_cap) ... ok
test_supervisor_retains_fresh_fsynced_halt_after_worker_signal_timeout_crash (__main__.FixRoundOneTests.test_supervisor_retains_fresh_fsynced_halt_after_worker_signal_timeout_crash) ... ok
test_worker_deadline_remains_armed_after_cleanup_until_actual_exit (__main__.FixRoundOneTests.test_worker_deadline_remains_armed_after_cleanup_until_actual_exit) ... ok
test_real_source_cache_model_tokenizer_corruption_is_inconclusive_and_retains_m (__main__.IntegrityTests.test_real_source_cache_model_tokenizer_corruption_is_inconclusive_and_retains_m) ... ok
test_G_failure_also_retains_immediately_obtained_dstats (__main__.PersistenceCorrectionTests.test_G_failure_also_retains_immediately_obtained_dstats) ... ok
test_forced_V7_failure_retains_value_and_provenance_before_G_and_scoring (__main__.PersistenceCorrectionTests.test_forced_V7_failure_retains_value_and_provenance_before_G_and_scoring) ... ok
test_forced_pass_outputs_checks_identical_to_frozen_previous_behavior (__main__.PersistenceCorrectionTests.test_forced_pass_outputs_checks_identical_to_frozen_previous_behavior) ... ok
test_fresh_and_process2_existing_dstats_refuse_overwrite (__main__.PersistenceCorrectionTests.test_fresh_and_process2_existing_dstats_refuse_overwrite) ... ok
test_process2_exact_input_bytes_retained_on_fail_and_pass (__main__.PersistenceCorrectionTests.test_process2_exact_input_bytes_retained_on_fail_and_pass) ... ok
test_process2_missing_G_retains_dstats_before_G_load (__main__.PersistenceCorrectionTests.test_process2_missing_G_retains_dstats_before_G_load) ... ok
test_all_pins_include_every_population_before_forwards (__main__.PinsAndAdmissionTests.test_all_pins_include_every_population_before_forwards) ... ok
test_launcher_existing_namespace_and_worker_gates_refuse_before_probe (__main__.PinsAndAdmissionTests.test_launcher_existing_namespace_and_worker_gates_refuse_before_probe) ... ok
test_local_arrow_revision_length_shards_and_offline_only (__main__.PinsAndAdmissionTests.test_local_arrow_revision_length_shards_and_offline_only) ... ok
test_namespace_refuses_reuse_and_attempt3_path (__main__.PinsAndAdmissionTests.test_namespace_refuses_reuse_and_attempt3_path) ... ok
test_supervised_worker_reuses_only_required_gates_before_forward_entry (__main__.PinsAndAdmissionTests.test_supervised_worker_reuses_only_required_gates_before_forward_entry) ... ok
test_F_pass_stops_and_random_pass_never_measures_R5000 (__main__.ProbePipelineTests.test_F_pass_stops_and_random_pass_never_measures_R5000) ... ok
test_R5000_independent_conditional_A2_and_D (__main__.ProbePipelineTests.test_R5000_independent_conditional_A2_and_D) ... ok
test_incomplete_failure_retains_prior_m_and_no_selection (__main__.ProbePipelineTests.test_incomplete_failure_retains_prior_m_and_no_selection) ... ok
test_scoring_deadline_cannot_publish_A1_or_increase_cap (__main__.ProbePipelineTests.test_scoring_deadline_cannot_publish_A1_or_increase_cap) ... ok
test_tensor_exclusive_flush_fsync_and_provenance (__main__.ProbePipelineTests.test_tensor_exclusive_flush_fsync_and_provenance) ... ok
test_cache_diagonal_count_and_loaded_once (__main__.SelectionAndScoringTests.test_cache_diagonal_count_and_loaded_once) ... ok
test_full_seed_one_permutation_and_exact_population_sizes (__main__.SelectionAndScoringTests.test_full_seed_one_permutation_and_exact_population_sizes) ... ok
test_ordered_routing_equal_boundary_nonfinite_and_report_only_E (__main__.SelectionAndScoringTests.test_ordered_routing_equal_boundary_nonfinite_and_report_only_E) ... ok
test_scoring_uses_driver_spearman_ties_natural_log_and_zero_inf (__main__.SelectionAndScoringTests.test_scoring_uses_driver_spearman_ties_natural_log_and_zero_inf) ... ok
test_actual_driver_bit_identity_and_independent_tokens_counts_normalization (__main__.StatisticTests.test_actual_driver_bit_identity_and_independent_tokens_counts_normalization) ... ok
test_ast_identity_sums_and_loop_only_row_count_varies (__main__.StatisticTests.test_ast_identity_sums_and_loop_only_row_count_varies) ... ok
test_hook_cleanup_after_forward_error (__main__.StatisticTests.test_hook_cleanup_after_forward_error) ... ok

======================================================================
FAIL: test_outer_error_preserves_durable_measured_population_details (__main__.EntryAndGuardTests.test_outer_error_preserves_durable_measured_population_details)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag_selftest.py", line 529, in test_outer_error_preserves_durable_measured_population_details
    self.assertEqual(result.get("provenance_mismatch"), mismatch, "late error dropped retained mismatch details")
AssertionError: None != {'population': 'F1000', 'fields': {'nonpa[48 chars]01}}} : late error dropped retained mismatch details

----------------------------------------------------------------------
Ran 41 tests in 9.227s

FAILED (failures=1)
FIX1_CLEANUP_CONTROL rc=-14 cleanup_started=True cleanup_done=False elapsed_s=0.2207
FIX1_V8_CONTROL process2=False dstats=True G=True
FIX1_V8_CONTROL process2=True dstats=True G=True
FIX1_PARENT_INVENTORY_CONTROL mode=idle reached_entry=True refusal=[]
FIX1_PARENT_INVENTORY_CONTROL mode=competing reached_entry=False refusal=['gpu exclusivity refused: {"ok": false, "blocking_processes": ["60003 /private/tmp/c10z_v7diag_fix1/tmpvcoexhnr/.venv/bin/python c10y_calibration4.py"], "blocking_tmux": [], "verified_model_free_supervisor": ["60001 /private/tmp/c10z_v7diag_fix1/tmpvcoexhnr/.venv/bin/python -B /private/tmp/c10z_v7diag_fix1/tmpvcoexhnr/tools/run_c10z_v7_diag.py --utc 20261009T000000Z"]}']
FIX1_PARENT_INVENTORY_CONTROL mode=different_command reached_entry=False refusal=['gpu exclusivity refused: {"ok": false, "blocking_processes": ["60001 /private/tmp/c10z_v7diag_fix1/tmpjaj1r723/.venv/bin/python unrelated_training.py"], "blocking_tmux": [], "verified_model_free_supervisor": []}']
FIX1_MISMATCH_CONTROL outcome=INCONCLUSIVE retained_m=True
FIX1_TERMINATION_CONTROL mode=signal rc=2 files=['halt_diagnostic_20261009T180008.118276Z.json', 'supervisor.json', 'verdict.json', 'worker.log']
FIX1_TERMINATION_CONTROL mode=timeout rc=2 files=['halt_diagnostic_20261009T180008.292675Z.json', 'supervisor.json', 'verdict.json', 'worker.log']
FIX1_TERMINATION_CONTROL mode=crash rc=2 files=['halt_diagnostic_20261009T180008.367568Z.json', 'supervisor.json', 'verdict.json', 'worker.log']
FIX1_WORKER_EXIT_CONTROL rc=-14 cleanup_done=True
C10Z_V7_DIAG_SELFTEST_FAIL tests=41
```

#### Final probe GREEN: 41 tests, 9.226s; all four blocker controls and supervisor/retention integration controls pass

Artifact:`/private/tmp/c10z_v7diag_fix1/probe_green_verified.txt`; captured command exit 0.

```text
CPU_ONLY: MPS availability forced false; unmocked MPS calls forbidden; no model load
test_CLI_bootstrap_timer_exists_before_driver_import (__main__.DeadlineTests.test_CLI_bootstrap_timer_exists_before_driver_import) ... ok
test_OS_timer_terminates_sleep_and_native_GIL_hold_retains_inconclusive (__main__.DeadlineTests.test_OS_timer_terminates_sleep_and_native_GIL_hold_retains_inconclusive) ... ok
test_immutable_3060_includes_preimport_and_exact_boundary (__main__.DeadlineTests.test_immutable_3060_includes_preimport_and_exact_boundary) ... ok
test_launcher_native_block_is_bounded_before_probe_dispatch (__main__.DeadlineTests.test_launcher_native_block_is_bounded_before_probe_dispatch) ... ok
test_launcher_origin_carried_and_future_or_nonfinite_origin_refused (__main__.DeadlineTests.test_launcher_origin_carried_and_future_or_nonfinite_origin_refused) ... ok
test_memory_ceilings_and_float64_MPS_guard_without_MPS_allocation (__main__.EntryAndGuardTests.test_memory_ceilings_and_float64_MPS_guard_without_MPS_allocation) ... ok
test_outer_error_preserves_durable_measured_population_details (__main__.EntryAndGuardTests.test_outer_error_preserves_durable_measured_population_details) ... PREIMPORT_TIMER_CONTROL remaining_s=3059.981703
HARD_DEADLINE_CONTROL native_GIL_hold=False rc=-14 elapsed_s=0.2203
HARD_DEADLINE_CONTROL native_GIL_hold=True rc=-14 elapsed_s=0.2206
LAUNCHER_HARD_DEADLINE_CONTROL native_GIL_hold=True rc=2 elapsed_s=0.1714
{"decision_id": "D-C10z-v7diag", "outcome": "INCONCLUSIVE", "reason": "TimeoutError: forced final deadline", "completion": "awaiting_worker_exit", "scores": {"F1000": {"E": {"10": "+inf", "11": "+inf", "12": "+inf", "4": "+inf", "5": "+inf", "6": "+inf", "7": "+inf", "8": "+inf", "9": "+inf"}, "P": false, "rho": {"10": 0.79, "11": 0.79, "12": 0.79, "4": 0.79, "5": 0.79, "6": 0.79, "7": 0.79, "8": 0.79, "9": 0.79}}, "R1000": {"E": {"10": "+inf", "11": "+inf", "12": "+inf", "4": "+inf", "5": "+inf", "6": "+inf", "7": "+inf", "8": "+inf", "9": "+inf"}, "P": true, "rho": {"10": 0.8, "11": 0.8, "12": 0.8, "4": 0.8, "5": 0.8, "6": 0.8, "7": 0.8, "8": 0.8, "9": 0.8}}}, "populations_measured": ["F1000", "R1000"], "cap_seconds": 3060, "late_layer_fidelity": "UNVERIFIED", "cpu_agreement_establishes_MPS_equivalence": false, "downstream_requirement": "supervisor-observed exit0 after cleanup plus complete verdict; implementation review before dispatch", "provenance_mismatch": {"fields": {"nonpadding_tokens": {"actual": 55001, "expected": 55000}}, "population": "F1000"}, "cleanup_completed": true, "deadline_origin": 1379718.485923333, "worker_exit_pending": true}
ok
test_real_entry_CPU_fixture_pins_durable_before_each_forward (__main__.EntryAndGuardTests.test_real_entry_CPU_fixture_pins_durable_before_each_forward) ... {"decision_id": "D-C10z-v7diag", "outcome": "A1", "reason": "exactly pinned R1000 passes P", "completion": "awaiting_worker_exit", "scores": {"F1000": {"rho": {"4": 0.79, "5": 0.79, "6": 0.79, "7": 0.79, "8": 0.79, "9": 0.79, "10": 0.79, "11": 0.79, "12": 0.79}, "E": {"4": "+inf", "5": "+inf", "6": "+inf", "7": "+inf", "8": "+inf", "9": "+inf", "10": "+inf", "11": "+inf", "12": "+inf"}, "P": false}, "R1000": {"rho": {"4": 0.8, "5": 0.8, "6": 0.8, "7": 0.8, "8": 0.8, "9": 0.8, "10": 0.8, "11": 0.8, "12": 0.8}, "E": {"4": "+inf", "5": "+inf", "6": "+inf", "7": "+inf", "8": "+inf", "9": "+inf", "10": "+inf", "11": "+inf", "12": "+inf"}, "P": true}}, "populations_measured": ["F1000", "R1000"], "cap_seconds": 3060, "late_layer_fidelity": "UNVERIFIED", "cpu_agreement_establishes_MPS_equivalence": false, "downstream_requirement": "supervisor-observed exit0 after cleanup plus complete verdict; implementation review before dispatch", "cleanup_completed": true, "deadline_origin": 1379718.485923333, "worker_exit_pending": true}
ok
test_timer_armed_before_namespace_and_initial_publication (__main__.EntryAndGuardTests.test_timer_armed_before_namespace_and_initial_publication) ... {"decision_id": "D-C10z-v7diag", "outcome": "INCONCLUSIVE", "reason": "ValueError: forced setup refusal", "completion": "awaiting_worker_exit", "scores": {}, "populations_measured": [], "cap_seconds": 3060, "late_layer_fidelity": "UNVERIFIED", "cpu_agreement_establishes_MPS_equivalence": false, "downstream_requirement": "supervisor-observed exit0 after cleanup plus complete verdict; implementation review before dispatch", "cleanup_completed": true, "deadline_origin": 1379718.485923333, "worker_exit_pending": true}
ok
test_explicit_cleanup_is_inside_original_deadline_before_success (__main__.FixRoundOneTests.test_explicit_cleanup_is_inside_original_deadline_before_success) ... ok
test_fresh_and_process2_G_retained_before_actual_V8_cholesky_failure (__main__.FixRoundOneTests.test_fresh_and_process2_G_retained_before_actual_V8_cholesky_failure) ... ok
test_invalid_returned_m_is_retained_before_tensor_validation (__main__.FixRoundOneTests.test_invalid_returned_m_is_retained_before_tensor_validation) ... ok
test_real_gpu_gate_excludes_only_verified_parent_and_still_blocks_competing_job (__main__.FixRoundOneTests.test_real_gpu_gate_excludes_only_verified_parent_and_still_blocks_competing_job) ... ok
test_returned_m_and_actual_provenance_survive_pin_mismatch (__main__.FixRoundOneTests.test_returned_m_and_actual_provenance_survive_pin_mismatch) ... ok
test_supervisor_admits_only_clean_receipt_and_normal_exit_within_original_cap (__main__.FixRoundOneTests.test_supervisor_admits_only_clean_receipt_and_normal_exit_within_original_cap) ... ok
test_supervisor_retains_fresh_fsynced_halt_after_worker_signal_timeout_crash (__main__.FixRoundOneTests.test_supervisor_retains_fresh_fsynced_halt_after_worker_signal_timeout_crash) ... ok
test_worker_deadline_remains_armed_after_cleanup_until_actual_exit (__main__.FixRoundOneTests.test_worker_deadline_remains_armed_after_cleanup_until_actual_exit) ... ok
test_real_source_cache_model_tokenizer_corruption_is_inconclusive_and_retains_m (__main__.IntegrityTests.test_real_source_cache_model_tokenizer_corruption_is_inconclusive_and_retains_m) ... ok
test_G_failure_also_retains_immediately_obtained_dstats (__main__.PersistenceCorrectionTests.test_G_failure_also_retains_immediately_obtained_dstats) ... ok
test_forced_V7_failure_retains_value_and_provenance_before_G_and_scoring (__main__.PersistenceCorrectionTests.test_forced_V7_failure_retains_value_and_provenance_before_G_and_scoring) ... ok
test_forced_pass_outputs_checks_identical_to_frozen_previous_behavior (__main__.PersistenceCorrectionTests.test_forced_pass_outputs_checks_identical_to_frozen_previous_behavior) ... ok
test_fresh_and_process2_existing_dstats_refuse_overwrite (__main__.PersistenceCorrectionTests.test_fresh_and_process2_existing_dstats_refuse_overwrite) ... ok
test_process2_exact_input_bytes_retained_on_fail_and_pass (__main__.PersistenceCorrectionTests.test_process2_exact_input_bytes_retained_on_fail_and_pass) ... ok
test_process2_missing_G_retains_dstats_before_G_load (__main__.PersistenceCorrectionTests.test_process2_missing_G_retains_dstats_before_G_load) ... ok
test_all_pins_include_every_population_before_forwards (__main__.PinsAndAdmissionTests.test_all_pins_include_every_population_before_forwards) ... ok
test_launcher_existing_namespace_and_worker_gates_refuse_before_probe (__main__.PinsAndAdmissionTests.test_launcher_existing_namespace_and_worker_gates_refuse_before_probe) ... ok
test_local_arrow_revision_length_shards_and_offline_only (__main__.PinsAndAdmissionTests.test_local_arrow_revision_length_shards_and_offline_only) ... ok
test_namespace_refuses_reuse_and_attempt3_path (__main__.PinsAndAdmissionTests.test_namespace_refuses_reuse_and_attempt3_path) ... ok
test_supervised_worker_reuses_only_required_gates_before_forward_entry (__main__.PinsAndAdmissionTests.test_supervised_worker_reuses_only_required_gates_before_forward_entry) ... ok
test_F_pass_stops_and_random_pass_never_measures_R5000 (__main__.ProbePipelineTests.test_F_pass_stops_and_random_pass_never_measures_R5000) ... ok
test_R5000_independent_conditional_A2_and_D (__main__.ProbePipelineTests.test_R5000_independent_conditional_A2_and_D) ... ok
test_incomplete_failure_retains_prior_m_and_no_selection (__main__.ProbePipelineTests.test_incomplete_failure_retains_prior_m_and_no_selection) ... ok
test_scoring_deadline_cannot_publish_A1_or_increase_cap (__main__.ProbePipelineTests.test_scoring_deadline_cannot_publish_A1_or_increase_cap) ... ok
test_tensor_exclusive_flush_fsync_and_provenance (__main__.ProbePipelineTests.test_tensor_exclusive_flush_fsync_and_provenance) ... ok
test_cache_diagonal_count_and_loaded_once (__main__.SelectionAndScoringTests.test_cache_diagonal_count_and_loaded_once) ... ok
test_full_seed_one_permutation_and_exact_population_sizes (__main__.SelectionAndScoringTests.test_full_seed_one_permutation_and_exact_population_sizes) ... ok
test_ordered_routing_equal_boundary_nonfinite_and_report_only_E (__main__.SelectionAndScoringTests.test_ordered_routing_equal_boundary_nonfinite_and_report_only_E) ... ok
test_scoring_uses_driver_spearman_ties_natural_log_and_zero_inf (__main__.SelectionAndScoringTests.test_scoring_uses_driver_spearman_ties_natural_log_and_zero_inf) ... ok
test_actual_driver_bit_identity_and_independent_tokens_counts_normalization (__main__.StatisticTests.test_actual_driver_bit_identity_and_independent_tokens_counts_normalization) ... ok
test_ast_identity_sums_and_loop_only_row_count_varies (__main__.StatisticTests.test_ast_identity_sums_and_loop_only_row_count_varies) ... ok
test_hook_cleanup_after_forward_error (__main__.StatisticTests.test_hook_cleanup_after_forward_error) ... ok

----------------------------------------------------------------------
Ran 41 tests in 9.226s

OK
FIX1_CLEANUP_CONTROL rc=-14 cleanup_started=True cleanup_done=False elapsed_s=0.2228
FIX1_V8_CONTROL process2=False dstats=True G=True
FIX1_V8_CONTROL process2=True dstats=True G=True
FIX1_PARENT_INVENTORY_CONTROL mode=idle reached_entry=True refusal=[]
FIX1_PARENT_INVENTORY_CONTROL mode=competing reached_entry=False refusal=['gpu exclusivity refused: {"ok": false, "blocking_processes": ["60003 /private/tmp/c10z_v7diag_fix1/tmpzozga4uj/.venv/bin/python c10y_calibration4.py"], "blocking_tmux": [], "verified_model_free_supervisor": ["60001 /private/tmp/c10z_v7diag_fix1/tmpzozga4uj/.venv/bin/python -B /private/tmp/c10z_v7diag_fix1/tmpzozga4uj/tools/run_c10z_v7_diag.py --utc 20261009T000000Z"]}']
FIX1_PARENT_INVENTORY_CONTROL mode=different_command reached_entry=False refusal=['gpu exclusivity refused: {"ok": false, "blocking_processes": ["60001 /private/tmp/c10z_v7diag_fix1/tmpvalbyl10/.venv/bin/python unrelated_training.py"], "blocking_tmux": [], "verified_model_free_supervisor": []}']
FIX1_MISMATCH_CONTROL outcome=INCONCLUSIVE retained_m=True
FIX1_TERMINATION_CONTROL mode=signal rc=2 files=['halt_diagnostic_20261009T180155.524270Z.json', 'supervisor.json', 'verdict.json', 'worker.log']
FIX1_TERMINATION_CONTROL mode=timeout rc=2 files=['halt_diagnostic_20261009T180155.701797Z.json', 'supervisor.json', 'verdict.json', 'worker.log']
FIX1_TERMINATION_CONTROL mode=crash rc=2 files=['halt_diagnostic_20261009T180155.781304Z.json', 'supervisor.json', 'verdict.json', 'worker.log']
FIX1_WORKER_EXIT_CONTROL rc=-14 cleanup_done=True
C10Z_V7_DIAG_SELFTEST_PASS tests=41
```

#### Full existing ASTRA GREEN: 209 tests, 108.136s; 207 executed pass and two MPS skips

Artifact:`/private/tmp/c10z_v7diag_fix1/astra_green.txt`; captured command exit 0.

```text
CPU_ONLY: MPS availability forced false; unmocked MPS calls forbidden; no model load
test_00_implementation_exists (__main__.SpecTests.test_00_implementation_exists)
Prereg :204: actual driver, reader and stage wrapper exist. ... ok
test_band_boundaries_ordered (__main__.SpecTests.test_band_boundaries_ordered)
Prereg :112, :284: fit -> capacity -> locality -> three exhaustive BAND rows. ... ok
test_budget_origins_prestart_deadlines_round_memory (__main__.SpecTests.test_budget_origins_prestart_deadlines_round_memory)
Prereg :190, :196–198: 5400 seconds, scopes, unknown allowance, exact memory. ... C10Z_PROJECTION {"origins": {"stage01": 100.0}, "ceilings": {"stage01": 7800.0, "stage2": 60.0, "stage3": 6000.0}, "components_s": {"remaining": 1.0}, "scopes": {"stage01": {"elapsed_s": 7799.0, "remaining_s": 1.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 100.0}, "ceilings": {"stage01": 7800.0, "stage2": 60.0, "stage3": 6000.0}, "components_s": {"remaining": 1.001}, "scopes": {"stage01": {"elapsed_s": 7799.0, "remaining_s": 1.001, "ceiling_s": 7800.0}}}
ok
test_completed_stage2_keeps_stage1_round_ceiling (__main__.SpecTests.test_completed_stage2_keeps_stage1_round_ceiling)
Prereg :198, :225: completed stage2 still checks stage1 A7 timing. ... ok
test_cpu_joint_algebra_independent_reference (__main__.SpecTests.test_cpu_joint_algebra_independent_reference)
Prereg :76, :78–80, :151: nonsymmetric solve, scalar-loop independent assembly. ... ok
test_cpu_null_weight_margin_fp16_selection (__main__.SpecTests.test_cpu_null_weight_margin_fp16_selection)
Prereg :75, :77–80, :210: independent floor/median, excluded competitor, fp32 add. ... ok
test_fit_count_boundaries (__main__.SpecTests.test_fit_count_boundaries)
Prereg :210, :230–234: exact integer FIT, positive 22/23, canonical 22/23. ... ok
test_fixed_competitor_and_native_reference_contract (__main__.SpecTests.test_fixed_competitor_and_native_reference_contract)
Prereg :155: native gathered logits, fixed competitor, finite last-layer path. ... ok
test_json_real_writer_and_frozen_sources (__main__.SpecTests.test_json_real_writer_and_frozen_sources)
Prereg :137, :204, :219, :224: round-trip, immutable outputs, finite science. ... ok
test_k1_k2_omissions_and_replication (__main__.SpecTests.test_k1_k2_omissions_and_replication)
Prereg :265–280: valid early stops != V12, lower labels, R2/R3 boundaries. ... ok
test_known_answer_scalar_and_native_fp16_reference (__main__.SpecTests.test_known_answer_scalar_and_native_fp16_reference)
Prereg :155: independent scalar A/ridge/columns and native finite reference. ... ok
test_law3_both_sides (__main__.SpecTests.test_law3_both_sides)
Prereg :123, :217: all inclusive envelope edges, and A1/A2 67/68. ... ok
test_manifest_population_and_post_instrument_tampering (__main__.SpecTests.test_manifest_population_and_post_instrument_tampering)
Prereg :137, :147–155, :224: complete inputs, missing controls, post-write evidence. ... ok
test_omission_reasons_follow_K1_K2 (__main__.SpecTests.test_omission_reasons_follow_K1_K2)
Prereg :265–267: every unrun expansion is recorded with its actual stopping reason. ... ok
test_ordering_and_stage_transport (__main__.SpecTests.test_ordering_and_stage_transport)
Prereg :120–125, :127–133, :218: no early observation, ordered one-stage requests. ... ok
test_raw_evidence_over_asserted_fit_write_and_repro (__main__.SpecTests.test_raw_evidence_over_asserted_fit_write_and_repro)
Prereg :224, :230, :272, :278: reject forged counts, bytes and certificates. ... ok
test_restore_finally_and_nonempty_hook_registry (__main__.SpecTests.test_restore_finally_and_nonempty_hook_registry)
Prereg :129, :152–153: all36 tensors restored after write/eval/hook failures. ... ok
test_review_Z5_footprint_rejects_any_write_outside_selected_columns (__main__.SpecTests.test_review_Z5_footprint_rejects_any_write_outside_selected_columns)
Prereg :80, :152: only selected W_down columns may differ; every other parameter byte-identical. ... ok
test_review_Z6_restore_covers_all_36_and_verify_detects_drift (__main__.SpecTests.test_review_Z6_restore_covers_all_36_and_verify_detects_drift)
Prereg :64, :129, :153; V3 :216: full 36-layer restore, byte-hash verification halts on drift. ... ok
test_review_cross_process_replication_needs_clean_pair (__main__.SpecTests.test_review_cross_process_replication_needs_clean_pair)
Prereg :277: LEAD/PARTIAL replicate only when both clean; differing base labels otherwise -NOT-REPLICATED. ... ok
test_review_reader_instrument_ceilings_audits_and_capacity (__main__.SpecTests.test_review_reader_instrument_ceilings_audits_and_capacity)
Prereg :147, :151–155, V2/V5/V9/V12, §2.5, §2.11: each recorded gate outcome is re-checked by the reader. ... ok
test_review_stage0_law3_gate_precedes_all_new_work (__main__.SpecTests.test_review_stage0_law3_gate_precedes_all_new_work)
Prereg :120, :123, :302 (row 13): LAW#3 miss halts V4 with baseline-only record; nothing runs before the gate. ... ok
test_review_stage1_round_over_120s_halts_in_run (__main__.SpecTests.test_review_stage1_round_over_120s_halts_in_run)
Prereg :198, V13 :225, row 24: a synchronized stage-1 round >120 s halts HALTED-BUDGET in the run. ... C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1200.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 2760.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1200.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 2760.0, "ceiling_s": 7800.0}}}
ok
test_review_stage_call_refusals (__main__.SpecTests.test_review_stage_call_refusals)
Prereg :133, :137, :196, :266: fresh OUT_DIR, K1/K2 and absent-ceiling refusals happen before any launch. ... ok
test_review_wrapper_delegates_under_standing_law5 (__main__.SpecTests.test_review_wrapper_delegates_under_standing_law5)
Prereg :127, :157; V2/V9: run_law5 always takes the original path; ASTRA only behind LAW#3 and instruments. ... ok
test_review_write_prestart_projection_refuses_before_observation (__main__.SpecTests.test_review_write_prestart_projection_refuses_before_observation)
Prereg :196, V13 :225: refuse to start a candidate write when elapsed + projection exceeds the ceiling. ... C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1200.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 7799.0, "remaining_s": 2760.0, "ceiling_s": 7800.0}}}
ok
test_review_write_round_cap_columns_and_capacity (__main__.SpecTests.test_review_write_round_cap_columns_and_capacity)
Prereg :79–81, :112: <=10 writes then round cap; only selected columns written; B_Z from Z's A7 only. ... C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1200.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 2760.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1200.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 2760.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1200.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 2760.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1200.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 2760.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 7800.0}}}
ok
test_side_gate_boundaries_and_populations (__main__.SpecTests.test_side_gate_boundaries_and_populations)
Prereg :239–245: every side gate equality passes, next value fails; no pooling. ... ok
test_table_T_exhaustive_and_integer_boundaries (__main__.SpecTests.test_table_T_exhaustive_and_integer_boundaries)
Prereg :249–261: independent exhaustive T1–T5, n18/19/29/30 and g9/10. ... ok
test_terminal_K1_wrapper_waits_for_close_error (__main__.SpecTests.test_terminal_K1_wrapper_waits_for_close_error)
Prereg :129, :265: terminal K1 response waits for verified close, propagates error. ... ok
test_terminal_halt_overrides_earlier_complete_pass (__main__.SpecTests.test_terminal_halt_overrides_earlier_complete_pass)
Prereg :196, :225: stage2 hard halt invalidates earlier stage1 pass. ... ok
test_transport_wait_publication_and_worker_failure (__main__.SpecTests.test_transport_wait_publication_and_worker_failure)
Prereg :126–139, :196: resident continuity, completed response, bounded failed wait. ... {"label": "PARTIAL", "next_stage": 2}
ok
test_ttl_every_Z_arm_and_incomplete_actual_repro_failure (__main__.SpecTests.test_ttl_every_Z_arm_and_incomplete_actual_repro_failure)
Prereg :267, :274, :278: any Z TTL, and omitted plus failed R1 retain both flags. ... ok
test_w1_even_median_w2_subject_free (__main__.SpecTests.test_w1_even_median_w2_subject_free)
Prereg :210, :272–274: even median, exact W1/W2, depth OR and +1 boundary. ... ok
test_worked22_validity_precedes_conditional_label (__main__.SpecTests.test_worked22_validity_precedes_conditional_label)
Prereg :149, :208, :311: contradictory raw canonical evidence HALTs before labels. ... ok
test_worked_01 (__main__.SpecTests.test_worked_01)
Prereg :290: n = 18, FIT ... ok
test_worked_02 (__main__.SpecTests.test_worked_02)
Prereg :291: n = 18, U (φ_μ = 0.80) ... ok
test_worked_03 (__main__.SpecTests.test_worked_03)
Prereg :292: n = 21, g = 9 (a = 12) ... ok
test_worked_04 (__main__.SpecTests.test_worked_04)
Prereg :293: n = 25, a = 16, g = 9 ... ok
test_worked_05 (__main__.SpecTests.test_worked_05)
Prereg :294: n = 22, g = 10, gates, FIT; stage 2 G0 holds, W1 0.4 (above the paper's SemCon range; reported, not a qualifier) ... ok
test_worked_06 (__main__.SpecTests.test_worked_06)
Prereg :295: n = 22, g = 10, G7 fails 3 (view, fact, depth) gates ... ok
test_worked_07 (__main__.SpecTests.test_worked_07)
Prereg :296: n = 29, gates, FIT; stage 2 Z-A1 = 67/72 ... ok
test_worked_08 (__main__.SpecTests.test_worked_08)
Prereg :297: n = 30, gates, FIT, W1 0.3; p2 n = 29, both processes clean ... ok
test_worked_09 (__main__.SpecTests.test_worked_09)
Prereg :298: n = 31, gates, U (φ_0^id = 22) ... ok
test_worked_10 (__main__.SpecTests.test_worked_10)
Prereg :299: n = 24, g = 6, U ... ok
test_worked_11 (__main__.SpecTests.test_worked_11)
Prereg :300: n = 33, gates, FIT, W1 1.4 ... ok
test_worked_12 (__main__.SpecTests.test_worked_12)
Prereg :301: n = 26, gates, subject-free hits A + 4 ... ok
test_worked_13 (__main__.SpecTests.test_worked_13)
Prereg :302: recipe A A7 = 19/72 ... ok
test_worked_14 (__main__.SpecTests.test_worked_14)
Prereg :303: Z3 (d): one greedy generation differs ... ok
test_worked_15 (__main__.SpecTests.test_worked_15)
Prereg :304: stage 2: n = 26, Z-band FIT, gates clean, capacity matched, n_b = 23 ... ok
test_worked_16 (__main__.SpecTests.test_worked_16)
Prereg :305: stage 2: n = 26, Z-band clean, n_b = 20 ... ok
test_worked_17 (__main__.SpecTests.test_worked_17)
Prereg :306: stage 2: n = 40, Z-band clean, n_b = 28 ... ok
test_worked_18 (__main__.SpecTests.test_worked_18)
Prereg :307: stage 2: n = 26, Z-band U (φ_μ = 0.61), n_b = 14 ... ok
test_worked_19 (__main__.SpecTests.test_worked_19)
Prereg :308: stage 2: n = 26, Z-band FIT, Z-band G7 fails, n_b = 24 ... ok
test_worked_20 (__main__.SpecTests.test_worked_20)
Prereg :309: stage 2: n = 22, Z-band clean, n_b = 17 ... ok
test_worked_21 (__main__.SpecTests.test_worked_21)
Prereg :310: stage 2: Z-band FIT, T = 144, B_Z = 2,304 > 2,200 ... ok
test_worked_22 (__main__.SpecTests.test_worked_22)
Prereg :311: n = 22, g = 10, gates, φ_μ = 0.958, φ_0^id = 24, actual `canon_full_n` = 0 ... ok
test_worked_23 (__main__.SpecTests.test_worked_23)
Prereg :312: n = 26, gates, FIT, W1 = 0.55 exactly ... ok
test_worked_24 (__main__.SpecTests.test_worked_24)
Prereg :313: stage 1: a synchronized round takes 121 s ... ok
test_z2_ambiguous_and_all_validity_gates (__main__.SpecTests.test_z2_ambiguous_and_all_validity_gates)
Prereg :149, :212–225: zero checked Z2 HALTs; V1–V13 each enforced. ... ok
test_B1_stage0_refuses_without_recorded_go_decision (__main__.Fix1Tests.test_B1_stage0_refuses_without_recorded_go_decision)
Prereg :3, :341–344: operator go before stage 0; blocking demo B1. ... ok
test_B2_stray_stage_call_after_terminal_K1_keeps_the_result (__main__.Fix1Tests.test_B2_stray_stage_call_after_terminal_K1_keeps_the_result)
Prereg :137, :204, :267: a refusal preserves completed records; blocking demo B2. ... HALTED-V12: duplicate, out-of-order, stale or closed stage call
ok
test_B3_clean_survivor_without_stage2_ceiling_keeps_stage1_record (__main__.Fix1Tests.test_B3_clean_survivor_without_stage2_ceiling_keeps_stage1_record)
Prereg :196, :265–267: unbudgeted expansion closes STAGE1; blocking demo B3 with lead's suffix ruling. ... HALTED-BUDGET: absent stage2 ceiling
ok
test_fix1_absent_ceilings_terminal_labels_and_resident_close (__main__.Fix1Tests.test_fix1_absent_ceilings_terminal_labels_and_resident_close)
Prereg :196, :265–267: clean stage1/2 without next budget terminates; no G0/replication claim. ... {"label": "PARTIAL-STAGE1", "base_label": "PARTIAL", "qualifiers": ["STAGE1"], "gates": {"G1": true, "G2": true, "G3": true, "G4": true, "G5": true, "G7": true}, "FIT": true, "n": 26, "a": 12, "gain": 14, "attribution": "NOT-RUN", "next_stage": null, "replicated": false, "lead_replicated": false, "artifact_identity": "NOT-EVALUATED", "numeric_behavioral_reproduction": "NOT-EVALUATED", "scientific_verdict": true}
ok
test_fix1_go_launch_copy_and_manifest_sha (__main__.Fix1Tests.test_fix1_go_launch_copy_and_manifest_sha)
Prereg :3, :137, :341–344: validated go copied to launch and its exact bytes bound to H_in. ... {"label": "NULL-STAGE1", "base_label": "NULL", "qualifiers": ["STAGE1"], "gates": {"G1": true, "G2": true, "G3": true, "G4": true, "G5": true, "G7": true}, "FIT": true, "n": 18, "a": 12, "gain": 6, "attribution": "NOT-RUN", "next_stage": null, "replicated": false, "lead_replicated": false, "artifact_identity": "NOT-EVALUATED", "numeric_behavioral_reproduction": "NOT-EVALUATED", "scientific_verdict": true}
ok
test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation. ... ok
test_fix1_go_sha_is_mandatory_reader_provenance (__main__.Fix1Tests.test_fix1_go_sha_is_mandatory_reader_provenance)
Prereg :137, V12 :224; §6 :341–344: missing/malformed go digest invalidates the manifest. ... ok
test_fix1_halt_sidecar_retains_completed_observations_for_both_processes (__main__.Fix1Tests.test_fix1_halt_sidecar_retains_completed_observations_for_both_processes)
Prereg :123, :267, :323: actual deadline/validity halts keep completed pass bytes and nonbinding observations. ... ok
test_fix1_refusals_preserve_finished_attempt_byte_for_byte (__main__.Fix1Tests.test_fix1_refusals_preserve_finished_attempt_byte_for_byte)
Prereg :137, :204, :267: duplicate/closed/out-of-order client refusals do not alter a finished attempt. ... HALTED-V12: attempt needs fresh OUT_DIR
HALTED-V12: duplicate, out-of-order, stale or closed stage call
HALTED-V12: duplicate, out-of-order, stale or closed stage call
HALTED-V12: stage3 requires clean completed K2 and closed process1
ok
test_fix1_relative_outdir_resolved_at_main_parse (__main__.Fix1Tests.test_fix1_relative_outdir_resolved_at_main_parse)
Prereg :8, :137, :204: records use one absolute OUT_DIR before the harness import changes cwd. ... ok
test_fix1_shell_preserves_go_env_absolute_outdir_and_no_refusal_write (__main__.Fix1Tests.test_fix1_shell_preserves_go_env_absolute_outdir_and_no_refusal_write)
Prereg :3, :137, :204: shell passes go unchanged and leaves unlaunched attempts untouched. ... ok
test_fix1_watchdog_preserves_last_published_record (__main__.Fix1Tests.test_fix1_watchdog_preserves_last_published_record)
Prereg :196, :225, :267: expired stage-2 watchdog preserves the complete earlier pass and labels HALT. ... ok
test_fix2_child_receives_parent_resolved_absolute_outdir (__main__.Fix2Tests.test_fix2_child_receives_parent_resolved_absolute_outdir)
Prereg :137, :204; fix2 item 1/O02: direct stage_call resolves the child path before cwd changes. ... ok
test_fix2_disqualified_missing_ceiling_is_k1_not_absent (__main__.Fix2Tests.test_fix2_disqualified_missing_ceiling_is_k1_not_absent)
Prereg :265, :272; B3g: a qualified PARTIAL/LEAD stops for K1 even without an expansion budget. ... ok
test_fix2_failed_resident_detection_closes_halt_and_keeps_passes (__main__.Fix2Tests.test_fix2_failed_resident_detection_closes_halt_and_keeps_passes)
Prereg :267, :323; D-C10z-fix1 (3): all wait_stage failed-resident detections publish a durable HALT. ... ok
test_fix2_go_nonfinite_constants_and_overflow_refused (__main__.Fix2Tests.test_fix2_go_nonfinite_constants_and_overflow_refused)
Prereg V6 :219, §6 :341–344; G11: nested NaN/Infinity and overflowing JSON numbers are refused without writes. ... ok
test_fix2_resident_stops_at_parent_halt_and_preserves_session_fields (__main__.Fix2Tests.test_fix2_resident_stops_at_parent_halt_and_preserves_session_fields)
Prereg :267, :323; item 2/H10/H11: a resumed resident sees the parent's halt at its next terminal check. ... ok
test_fix2_session_record_absent_ceiling_matches_reader_omissions (__main__.Fix2Tests.test_fix2_session_record_absent_ceiling_matches_reader_omissions)
Prereg :196, :265–267; B3d: the actual Session.record producer agrees with the independent reader. ... ok
test_fix2_z0_sigma_halts_in_driver_at_frozen_boundary (__main__.Fix2Tests.test_fix2_z0_sigma_halts_in_driver_at_frozen_boundary)
Prereg :147; A32: the real Z0 function permits sigma=.125 and halts above it before any reader. ... ok
test_z0_v5_halt_persists_native_and_full_sigma (__main__.Fix2Tests.test_z0_v5_halt_persists_native_and_full_sigma)
Diagnosability only: the unchanged V5 refusal publishes both measured maxima. ... ok
test_i_idle_expiry (__main__.IdleGapTests.test_i_idle_expiry) ... C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7200.0, "stage2": 200.0, "stage3": 7460.0}, "components_s": {"candidate_rounds": 1200.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 2760.0, "ceiling_s": 7200.0}}}
ok
test_ii_late_entry (__main__.IdleGapTests.test_ii_late_entry) ... C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7200.0, "stage2": 200.0, "stage3": 7460.0}, "components_s": {"candidate_rounds": 1200.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 2760.0, "ceiling_s": 7200.0}}}
ok
test_iii_deadline_samples (__main__.IdleGapTests.test_iii_deadline_samples) ... C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7200.0, "stage2": 200.0, "stage3": 7460.0}, "components_s": {"candidate_rounds": 1200.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 2760.0, "ceiling_s": 7200.0}}}
ok
test_iv_process2_envelope (__main__.IdleGapTests.test_iv_process2_envelope) ... C10Z_PROJECTION {"origins": {"stage01": 0.0, "stage3": 0.0}, "ceilings": {"stage01": 7200.0, "stage2": 200.0, "stage3": 7460.0}, "components_s": {"candidate_rounds": 1200.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 2760.0, "ceiling_s": 7200.0}, "stage3": {"elapsed_s": 0.0, "remaining_s": 2860.0, "ceiling_s": 7460.0}}}
ok
test_ix_transition_lock (__main__.IdleGapTests.test_ix_transition_lock) ... ok
test_v_complete01_only_enter (__main__.IdleGapTests.test_v_complete01_only_enter) ... ok
test_vi_mutation_deadlines (__main__.IdleGapTests.test_vi_mutation_deadlines) ... C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7200.0, "stage2": 200.0, "stage3": 7460.0}, "components_s": {"candidate_rounds": 1200.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 2760.0, "ceiling_s": 7200.0}}}
ok
test_vii_entry_invariant (__main__.IdleGapTests.test_vii_entry_invariant) ... C10Z_PROJECTION {"origins": {"stage01": 0.0, "stage3": 0.0}, "ceilings": {"stage01": 7200.0, "stage2": 200.0, "stage3": 7460.0}, "components_s": {"candidate_rounds": 1200.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 2760.0, "ceiling_s": 7200.0}, "stage3": {"elapsed_s": 0.0, "remaining_s": 2860.0, "ceiling_s": 7460.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0, "stage3": 0.0}, "ceilings": {"stage01": 7200.0, "stage2": 200.0, "stage3": 7460.0}, "components_s": {"candidate_rounds": 1200.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 2760.0, "ceiling_s": 7200.0}, "stage3": {"elapsed_s": 0.0, "remaining_s": 2860.0, "ceiling_s": 7460.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0, "stage3": 0.0}, "ceilings": {"stage01": 7200.0, "stage2": 200.0, "stage3": 7460.0}, "components_s": {"candidate_rounds": 1200.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 2760.0, "ceiling_s": 7200.0}, "stage3": {"elapsed_s": 0.0, "remaining_s": 2860.0, "ceiling_s": 7460.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0, "stage3": 0.0}, "ceilings": {"stage01": 7200.0, "stage2": 200.0, "stage3": 7460.0}, "components_s": {"candidate_rounds": 1200.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 2760.0, "ceiling_s": 7200.0}, "stage3": {"elapsed_s": 0.0, "remaining_s": 2860.0, "ceiling_s": 7460.0}}}
ok
test_viii_single_timestamp (__main__.IdleGapTests.test_viii_single_timestamp) ... ok
test_c01_neighbors (__main__.BudgetBoundTests.test_c01_neighbors) ... ok
test_huge_integer_refusal (__main__.BudgetBoundTests.test_huge_integer_refusal) ... ok
test_benchmark_template_digest_mismatch_refuses_before_launch (__main__.LaunchBindingTests.test_benchmark_template_digest_mismatch_refuses_before_launch)
D-C10z-v4fix: a valid selected benchmark with different templates refuses V12 before worker/output creation. ... ok
test_c01 (__main__.LaunchBindingTests.test_c01) ... ok
test_derived (__main__.LaunchBindingTests.test_derived) ... ok
test_environment (__main__.LaunchBindingTests.test_environment) ... ok
test_go_ceilings (__main__.LaunchBindingTests.test_go_ceilings) ... ok
test_go_fields (__main__.LaunchBindingTests.test_go_fields) ... ok
test_go_huge_integer_ceiling_refusal (__main__.LaunchBindingTests.test_go_huge_integer_ceiling_refusal) ... ok
test_inertness_counts (__main__.LaunchBindingTests.test_inertness_counts) ... ok
test_inertness_environment (__main__.LaunchBindingTests.test_inertness_environment) ... ok
test_inertness_json (__main__.LaunchBindingTests.test_inertness_json) ... ok
test_inertness_path (__main__.LaunchBindingTests.test_inertness_path) ... ok
test_inertness_required (__main__.LaunchBindingTests.test_inertness_required) ... ok
test_inertness_schema (__main__.LaunchBindingTests.test_inertness_schema) ... ok
test_inertness_sources (__main__.LaunchBindingTests.test_inertness_sources) ... ok
test_inertness_success (__main__.LaunchBindingTests.test_inertness_success) ... ok
test_inertness_verdict (__main__.LaunchBindingTests.test_inertness_verdict) ... ok
test_record_absolute (__main__.LaunchBindingTests.test_record_absolute) ... ok
test_record_invalid (__main__.LaunchBindingTests.test_record_invalid) ... ok
test_record_nonstrict (__main__.LaunchBindingTests.test_record_nonstrict) ... ok
test_record_optional_status (__main__.LaunchBindingTests.test_record_optional_status) ... ok
test_record_outside (__main__.LaunchBindingTests.test_record_outside) ... ok
test_record_required (__main__.LaunchBindingTests.test_record_required) ... ok
test_record_selection (__main__.LaunchBindingTests.test_record_selection) ... ok
test_record_unreadable (__main__.LaunchBindingTests.test_record_unreadable) ... ok
test_refused (__main__.LaunchBindingTests.test_refused) ... ok
test_script (__main__.LaunchBindingTests.test_script) ... ok
test_sources (__main__.LaunchBindingTests.test_sources) ... ok
test_stage2_override (__main__.LaunchBindingTests.test_stage2_override) ... ok
test_stage3_environment_drift (__main__.LaunchBindingTests.test_stage3_environment_drift) ... ok
test_stage3_inertness_drift (__main__.LaunchBindingTests.test_stage3_inertness_drift) ... ok
test_stage3_override (__main__.LaunchBindingTests.test_stage3_override) ... ok
test_stage3_record_drift (__main__.LaunchBindingTests.test_stage3_record_drift) ... ok
test_stage3_script_drift (__main__.LaunchBindingTests.test_stage3_script_drift) ... ok
test_stage3_source_drift (__main__.LaunchBindingTests.test_stage3_source_drift) ... ok
test_stage3_switch (__main__.LaunchBindingTests.test_stage3_switch) ... ok
test_stop (__main__.LaunchBindingTests.test_stop) ... ok
test_substitution (__main__.LaunchBindingTests.test_substitution) ... ok
test_success_roundtrip (__main__.LaunchBindingTests.test_success_roundtrip) ... ok
test_switch_empty (__main__.LaunchBindingTests.test_switch_empty) ... ok
test_switch_space (__main__.LaunchBindingTests.test_switch_space) ... ok
test_switch_true (__main__.LaunchBindingTests.test_switch_true) ... ok
test_switch_zero (__main__.LaunchBindingTests.test_switch_zero) ... ok
test_total (__main__.LaunchBindingTests.test_total) ... ok
test_benchmark_sha (__main__.ReaderBindingTests.test_benchmark_sha) ... ok
test_c01_neighbors (__main__.ReaderBindingTests.test_c01_neighbors) ... ok
test_go_ceilings (__main__.ReaderBindingTests.test_go_ceilings) ... ok
test_history_ceilings (__main__.ReaderBindingTests.test_history_ceilings) ... ok
test_huge_integer_refusal (__main__.ReaderBindingTests.test_huge_integer_refusal) ... ok
test_pass_launch (__main__.ReaderBindingTests.test_pass_launch) ... ok
test_process_ceilings (__main__.ReaderBindingTests.test_process_ceilings) ... ok
test_scope_ceiling (__main__.ReaderBindingTests.test_scope_ceiling) ... ok
test_attempt2_out_and_logs_preserve_attempt1 (__main__.WrapperTests.test_attempt2_out_and_logs_preserve_attempt1)
Prereg §10(d2): explicit attempt2 output, go/benchmark selection and both redirected logs preserve attempt1. ... ok
test_direct_scripts_executable_on_disk_and_git_index (__main__.WrapperTests.test_direct_scripts_executable_on_disk_and_git_index) ... ok
test_next_stage_types (__main__.WrapperTests.test_next_stage_types) ... ok
test_relative_out (__main__.WrapperTests.test_relative_out) ... ok
test_stage0_failure (__main__.WrapperTests.test_stage0_failure) ... ok
test_UTC_diagnostic_collision_refuses_exclusive_creation (__main__.TemplatePinTests.test_UTC_diagnostic_collision_refuses_exclusive_creation) ... ok
test_UTC_diagnostics_preserve_historical_records (__main__.TemplatePinTests.test_UTC_diagnostics_preserve_historical_records) ... ok
test_V4_resident_retains_templates_and_halt_hashes (__main__.TemplatePinTests.test_V4_resident_retains_templates_and_halt_hashes) ... C10Z_PROJECTION {"origins": {"stage01": 1379003.328920041}, "ceilings": {"stage01": 7800.0, "stage2": 12000.0, "stage3": 24000.0}, "components_s": {"recipe_A": 2040.0, "reference_D": 300.0, "G": 120.0, "verification_and_all_probes": 1380.0, "candidate_rounds": 1200.0, "serialization_and_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0010366670321673155, "remaining_s": 5220.0, "ceiling_s": 7800.0}}}
ok
test_cache_pinned_before_recipe_A_without_sampling (__main__.TemplatePinTests.test_cache_pinned_before_recipe_A_without_sampling) ... ok
test_existing_context_artifact_refusal_unchanged (__main__.TemplatePinTests.test_existing_context_artifact_refusal_unchanged) ... ok
test_manual_seed_zero_kept_before_harness_import (__main__.TemplatePinTests.test_manual_seed_zero_kept_before_harness_import) ... ok
test_process2_reuses_loaded_cache_before_baseline (__main__.TemplatePinTests.test_process2_reuses_loaded_cache_before_baseline) ... ok
test_scorer_template_identity_mismatch_refuses_before_recipe_A (__main__.TemplatePinTests.test_scorer_template_identity_mismatch_refuses_before_recipe_A) ... ok
test_selected_template_list_mismatch_refuses_before_recipe_A (__main__.TemplatePinTests.test_selected_template_list_mismatch_refuses_before_recipe_A) ... ok
test_templates_and_run_hash_written_before_LAW3_gate (__main__.TemplatePinTests.test_templates_and_run_hash_written_before_LAW3_gate) ... ok
test_templates_byte_equal_to_benchmark (__main__.TemplatePinTests.test_templates_byte_equal_to_benchmark) ... ok
test_amended_prereg_pin_shared_by_driver_reader_and_tests (__main__.PinTests.test_amended_prereg_pin_shared_by_driver_reader_and_tests) ... ok
test_temp_copy_byte_drift (__main__.PinTests.test_temp_copy_byte_drift) ... ok
test_on_off_science (__main__.TelemetryIntegrationTests.test_on_off_science) ... ok
test_placements_ast (__main__.TelemetryIntegrationTests.test_placements_ast) ... ok
test_resident_on_off (__main__.TelemetryIntegrationTests.test_resident_on_off) ... ok
test_resident_telemetry_failures_preserve_science (__main__.TelemetryIntegrationTests.test_resident_telemetry_failures_preserve_science) ... ok
test_write_telemetry_failures_preserve_science (__main__.TelemetryIntegrationTests.test_write_telemetry_failures_preserve_science) ... ok
test_probe_batch1_keeps_padding_and_captures_actual_position_ids (__main__.Z0ProbeTests.test_probe_batch1_keeps_padding_and_captures_actual_position_ids) ... ok
test_probe_cpu_json_pipeline_roundtrip_and_exclusive_output (__main__.Z0ProbeTests.test_probe_cpu_json_pipeline_roundtrip_and_exclusive_output) ... C10Z_Z0_PROBE_DIAGNOSTIC /private/tmp/c10z_v7diag_fix1/tmp1_lu5zy_/results/c10z_astra_z0_probe/20261008T220001Z/probe.json
ok
test_probe_diff_statistics_subtract_in_cpu_float64 (__main__.Z0ProbeTests.test_probe_diff_statistics_subtract_in_cpu_float64) ... ok
test_probe_distinct_shape_controls_and_full_sigma_match_z0 (__main__.Z0ProbeTests.test_probe_distinct_shape_controls_and_full_sigma_match_z0) ... ok
test_probe_mutation_is_detected_without_restoring_weights (__main__.Z0ProbeTests.test_probe_mutation_is_detected_without_restoring_weights) ... ok
test_probe_native_mask_cli_default_and_ones (__main__.Z0ProbeTests.test_probe_native_mask_cli_default_and_ones) ... ok
test_probe_native_mask_option_changes_only_forward_kwargs (__main__.Z0ProbeTests.test_probe_native_mask_option_changes_only_forward_kwargs) ... ok
test_probe_native_prefix_leads_equal_real_z0 (__main__.Z0ProbeTests.test_probe_native_prefix_leads_equal_real_z0) ... ok
test_probe_never_writes_weights_or_calls_edit_recipe_sampling (__main__.Z0ProbeTests.test_probe_never_writes_weights_or_calls_edit_recipe_sampling) ... ok
test_probe_records_attention_backend_and_native_logit_bound (__main__.Z0ProbeTests.test_probe_records_attention_backend_and_native_logit_bound) ... ok
test_probe_refuses_existing_or_escaped_output_before_model_load (__main__.Z0ProbeTests.test_probe_refuses_existing_or_escaped_output_before_model_load) ... ok
test_probe_wrong_template_sha_refuses_before_model_load (__main__.Z0ProbeTests.test_probe_wrong_template_sha_refuses_before_model_load) ... ok
test_ast_guard_covers_all_unsafe_copy_api_forms (__main__.V5CopyTests.test_ast_guard_covers_all_unsafe_copy_api_forms) ... ok
test_astra_sources_no_combined_device_dtype_transfer_ast (__main__.V5CopyTests.test_astra_sources_no_combined_device_dtype_transfer_ast) ... ok
test_margin_leads_no_combined_device_dtype_transfer_ast (__main__.V5CopyTests.test_margin_leads_no_combined_device_dtype_transfer_ast) ... ok
test_mps_offset_view_corruption_and_exact_split_copy (__main__.V5CopyTests.test_mps_offset_view_corruption_and_exact_split_copy) ... skipped 'MPS unavailable: offset-view corruption reproduction UNVERIFIED'
test_mps_torch_cpu64_transfers_before_float64 (__main__.V5CopyTests.test_mps_torch_cpu64_transfers_before_float64) ... skipped 'MPS unavailable: float64 capture regression UNVERIFIED'
test_probe_native_and_full_rows_transfer_before_cast_ast (__main__.V5CopyTests.test_probe_native_and_full_rows_transfer_before_cast_ast) ... ok
test_target_probabilities_preserves_offset_float32_inputs (__main__.V5CopyTests.test_target_probabilities_preserves_offset_float32_inputs) ... ok
test_torch_cpu64_moves_to_cpu_before_float64_ast (__main__.V5CopyTests.test_torch_cpu64_moves_to_cpu_before_float64_ast) ... ok
test_T3_header_four_kinds_fields_and_full_cost_accounting (__main__.TelemetryUnitTests.test_T3_header_four_kinds_fields_and_full_cost_accounting) ... ok
test_T4_public_methods_avoid_science_clocks_and_gates (__main__.TelemetryUnitTests.test_T4_public_methods_avoid_science_clocks_and_gates) ... ok
test_T5a_directory_failure_is_disabled_once (__main__.TelemetryUnitTests.test_T5a_directory_failure_is_disabled_once) ... ok
test_T5a_initial_open_failure_is_disabled_once (__main__.TelemetryUnitTests.test_T5a_initial_open_failure_is_disabled_once) ... ok
test_T5b_write_failure_is_disabled_once (__main__.TelemetryUnitTests.test_T5b_write_failure_is_disabled_once) ... ok
test_T5c_flush_failure_is_disabled_once (__main__.TelemetryUnitTests.test_T5c_flush_failure_is_disabled_once) ... ok
test_T5d_fsync_failure_is_disabled_once (__main__.TelemetryUnitTests.test_T5d_fsync_failure_is_disabled_once) ... ok
test_T5e_keyboard_interrupt_propagates (__main__.TelemetryUnitTests.test_T5e_keyboard_interrupt_propagates) ... ok
test_T6_each_call_preserves_cpu_model_and_inputs (__main__.TelemetryUnitTests.test_T6_each_call_preserves_cpu_model_and_inputs) ... ok
test_T6_lens_uses_layer_output_top5_and_no_grad (__main__.TelemetryUnitTests.test_T6_lens_uses_layer_output_top5_and_no_grad) ... ok
test_T7_default_chunk_keeps_cpu_float32_under64MiB (__main__.TelemetryUnitTests.test_T7_default_chunk_keeps_cpu_float32_under64MiB) ... ok
test_T7_probabilities_dense_reference_and_row_chunk_bound (__main__.TelemetryUnitTests.test_T7_probabilities_dense_reference_and_row_chunk_bound) ... ok
test_T9_write_volume_no_requirement_lines (__main__.TelemetryUnitTests.test_T9_write_volume_no_requirement_lines) ... C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1200.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 2760.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1200.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 2760.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 7800.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 7800.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 7800.0}}}
ok
test_deterministic_three_pass_schedule_and_kwargs (__main__.TelemetryInertnessTests.test_deterministic_three_pass_schedule_and_kwargs) ... ok
test_full_greedy_suffix_count_and_compare (__main__.TelemetryInertnessTests.test_full_greedy_suffix_count_and_compare) ... ok
test_lens_sensitive_batch_is_not_inert (__main__.TelemetryInertnessTests.test_lens_sensitive_batch_is_not_inert) ... ok
test_lens_sensitive_probe_is_not_inert (__main__.TelemetryInertnessTests.test_lens_sensitive_probe_is_not_inert) ... ok
test_plain_drift_is_nondeterministic_baseline (__main__.TelemetryInertnessTests.test_plain_drift_is_nondeterministic_baseline) ... ok
test_runner_checks_all36_weights_and_invalid_is_exit2 (__main__.TelemetryRunnerTests.test_runner_checks_all36_weights_and_invalid_is_exit2) ... ok
test_runner_driver_module_reused (__main__.TelemetryRunnerTests.test_runner_driver_module_reused) ... ok
test_runner_import_is_stdlib_only (__main__.TelemetryRunnerTests.test_runner_import_is_stdlib_only) ... ok
test_runner_refuses_outside_and_existing_record_without_forward (__main__.TelemetryRunnerTests.test_runner_refuses_outside_and_existing_record_without_forward) ... ok
test_runner_refuses_relative_out_path (__main__.TelemetryRunnerTests.test_runner_refuses_relative_out_path) ... ok
test_runner_roundtrip_identity_and_no_write_engine_calls (__main__.TelemetryRunnerTests.test_runner_roundtrip_identity_and_no_write_engine_calls) ... ok

----------------------------------------------------------------------
Ran 209 tests in 108.136s

OK (skipped=2)
C10Z_ASTRA_SELFTEST_PASS tests=209
```

#### Full benchmark GREEN: 47 tests, 2.716s

Artifact:`/private/tmp/c10z_v7diag_fix1/benchmark_green.txt`; captured command exit 0.

```text
CPU_ONLY: MPS availability forced false; unmocked MPS calls forbidden; no model load
test_eight_v3_calibration_cases (__main__.BenchmarkCeilingTests.test_eight_v3_calibration_cases) ... ok
test_exact_rounding_and_c01_stop_boundary (__main__.BenchmarkCeilingTests.test_exact_rounding_and_c01_stop_boundary) ... ok
test_mean_outlier_and_complete_eval_tstar (__main__.BenchmarkCeilingTests.test_mean_outlier_and_complete_eval_tstar) ... ok
test_optional_minima_and_timeout_lower_bound (__main__.BenchmarkCeilingTests.test_optional_minima_and_timeout_lower_bound) ... ok
test_raw_values_drive_all_terms (__main__.BenchmarkCeilingTests.test_raw_values_drive_all_terms) ... ok
test_refused_records_never_fallback_or_numbers (__main__.BenchmarkCeilingTests.test_refused_records_never_fallback_or_numbers) ... ok
test_environment_identity_metadata_only (__main__.BenchmarkIdentityTests.test_environment_identity_metadata_only) ... ok
test_environment_identity_no_torch_subprocess (__main__.BenchmarkIdentityTests.test_environment_identity_no_torch_subprocess) ... ok
test_source_identity_exact_order_and_root (__main__.BenchmarkIdentityTests.test_source_identity_exact_order_and_root) ... ok
test_top_level_import_stdlib_only_subprocess (__main__.BenchmarkIdentityTests.test_top_level_import_stdlib_only_subprocess) ... ok
test_env_preflight_refusals (__main__.BenchmarkLifecycleTests.test_env_preflight_refusals) ... ok
test_injected_worker_full_schedule_no_writer_calls (__main__.BenchmarkLifecycleTests.test_injected_worker_full_schedule_no_writer_calls) ... C10Z_PROBE_POPULATION {"arm": "A7_coined_coined", "sha256": "02af6172c2ce331a98cd0b6aeee0b656f6062050caf228fa2be50048d6938aaa", "counts": {"F0": 36, "prefix": 3888, "subject_free": 108, "relations": 48}}
ok
test_injected_worker_synthetic_mps_identity_validates_derived (__main__.BenchmarkLifecycleTests.test_injected_worker_synthetic_mps_identity_validates_derived) ... C10Z_PROBE_POPULATION {"arm": "A7_coined_coined", "sha256": "02af6172c2ce331a98cd0b6aeee0b656f6062050caf228fa2be50048d6938aaa", "counts": {"F0": 36, "prefix": 3888, "subject_free": 108, "relations": 48}}
ok
test_optional_skip_keeps_top_level_status (__main__.BenchmarkLifecycleTests.test_optional_skip_keeps_top_level_status) ... C10Z_PROBE_POPULATION {"arm": "A7_coined_coined", "sha256": "02af6172c2ce331a98cd0b6aeee0b656f6062050caf228fa2be50048d6938aaa", "counts": {"F0": 36, "prefix": 3888, "subject_free": 108, "relations": 48}}
ok
test_out_path_refusals_and_prefix_trap (__main__.BenchmarkLifecycleTests.test_out_path_refusals_and_prefix_trap) ... ok
test_start_and_phase_fit_boundaries (__main__.BenchmarkLifecycleTests.test_start_and_phase_fit_boundaries) ... ok
test_supervisor_600_boundary_fake_clock (__main__.BenchmarkLifecycleTests.test_supervisor_600_boundary_fake_clock) ... ok
test_supervisor_completed_worker_untouched (__main__.BenchmarkLifecycleTests.test_supervisor_completed_worker_untouched) ... ok
test_supervisor_existing_record_cap_preserves_bytes (__main__.BenchmarkLifecycleTests.test_supervisor_existing_record_cap_preserves_bytes) ... ok
test_supervisor_forbidden_astra_cap_preserves_directory (__main__.BenchmarkLifecycleTests.test_supervisor_forbidden_astra_cap_preserves_directory) ... ok
test_supervisor_outside_benchmark_cap_preserves_directory (__main__.BenchmarkLifecycleTests.test_supervisor_outside_benchmark_cap_preserves_directory) ... ok
test_supervisor_real_process_group_kill_and_interrupted_record (__main__.BenchmarkLifecycleTests.test_supervisor_real_process_group_kill_and_interrupted_record) ... ok
test_svd_timeout_565_lower_bound_and_worker_survival (__main__.BenchmarkLifecycleTests.test_svd_timeout_565_lower_bound_and_worker_survival) ... ok
test_system_wide_monotonic_subprocess (__main__.BenchmarkLifecycleTests.test_system_wide_monotonic_subprocess) ... ok
test_worker_guard_status_bands_and_reserved_after_hash (__main__.BenchmarkLifecycleTests.test_worker_guard_status_bands_and_reserved_after_hash) ... C10Z_PROBE_POPULATION {"arm": "A7_coined_coined", "sha256": "02af6172c2ce331a98cd0b6aeee0b656f6062050caf228fa2be50048d6938aaa", "counts": {"F0": 36, "prefix": 3888, "subject_free": 108, "relations": 48}}
C10Z_PROBE_POPULATION {"arm": "A7_coined_coined", "sha256": "02af6172c2ce331a98cd0b6aeee0b656f6062050caf228fa2be50048d6938aaa", "counts": {"F0": 36, "prefix": 3888, "subject_free": 108, "relations": 48}}
C10Z_PROBE_POPULATION {"arm": "A7_coined_coined", "sha256": "02af6172c2ce331a98cd0b6aeee0b656f6062050caf228fa2be50048d6938aaa", "counts": {"F0": 36, "prefix": 3888, "subject_free": 108, "relations": 48}}
ok
test_worker_load_over_300_invalid (__main__.BenchmarkLifecycleTests.test_worker_load_over_300_invalid) ... ok
test_worker_mutation_invalid_and_refused (__main__.BenchmarkLifecycleTests.test_worker_mutation_invalid_and_refused) ... C10Z_PROBE_POPULATION {"arm": "A7_coined_coined", "sha256": "02af6172c2ce331a98cd0b6aeee0b656f6062050caf228fa2be50048d6938aaa", "counts": {"F0": 36, "prefix": 3888, "subject_free": 108, "relations": 48}}
ok
test_worker_svd_timeout_preserves_complete_and_capped (__main__.BenchmarkLifecycleTests.test_worker_svd_timeout_preserves_complete_and_capped) ... C10Z_PROBE_POPULATION {"arm": "A7_coined_coined", "sha256": "02af6172c2ce331a98cd0b6aeee0b656f6062050caf228fa2be50048d6938aaa", "counts": {"F0": 36, "prefix": 3888, "subject_free": 108, "relations": 48}}
C10Z_PROBE_POPULATION {"arm": "A7_coined_coined", "sha256": "02af6172c2ce331a98cd0b6aeee0b656f6062050caf228fa2be50048d6938aaa", "counts": {"F0": 36, "prefix": 3888, "subject_free": 108, "relations": 48}}
ok
test_empty_population_leaves_no_heartbeat (__main__.BenchmarkPopulationTests.test_empty_population_leaves_no_heartbeat) ... ok
test_full_population_forward_counts (__main__.BenchmarkPopulationTests.test_full_population_forward_counts) ... C10Z_PROBE_POPULATION {"arm": "A7_coined_coined", "sha256": "02af6172c2ce331a98cd0b6aeee0b656f6062050caf228fa2be50048d6938aaa", "counts": {"F0": 36, "prefix": 3888, "subject_free": 108, "relations": 48}}
C10Z_PROBE_POPULATION {"arm": "A7_coined_coined", "sha256": "286257b9d4f116fd9d47b617a27c81f2258b70e40b1b72ac1cb7389ad59992d4", "counts": {"F0": 36, "prefix": 3888, "subject_free": 108, "relations": 48}}
ok
test_greedy_argmax_and_no_grad (__main__.BenchmarkPopulationTests.test_greedy_argmax_and_no_grad) ... ok
test_guarded_loop_completes_item_then_stops (__main__.BenchmarkPopulationTests.test_guarded_loop_completes_item_then_stops) ... ok
test_guarded_warmup_records_actual_count (__main__.BenchmarkPopulationTests.test_guarded_warmup_records_actual_count) ... ok
test_population_batch_and_digest_match_driver (__main__.BenchmarkPopulationTests.test_population_batch_and_digest_match_driver) ... C10Z_PROBE_POPULATION {"arm": "A7_coined_coined", "sha256": "02af6172c2ce331a98cd0b6aeee0b656f6062050caf228fa2be50048d6938aaa", "counts": {"F0": 36, "prefix": 3888, "subject_free": 108, "relations": 48}}
C10Z_PROBE_POPULATION {"arm": "A7_coined_coined", "sha256": "02af6172c2ce331a98cd0b6aeee0b656f6062050caf228fa2be50048d6938aaa", "counts": {"F0": 36, "prefix": 3888, "subject_free": 108, "relations": 48}}
ok
test_timed_reads_heartbeat_and_warmup_exclusion (__main__.BenchmarkPopulationTests.test_timed_reads_heartbeat_and_warmup_exclusion) ... ok
test_huge_integer_timing_is_value_error (__main__.BenchmarkRecordTests.test_huge_integer_timing_is_value_error) ... ok
test_interrupted_replace_preserves_prior_record (__main__.BenchmarkRecordTests.test_interrupted_replace_preserves_prior_record) ... ok
test_measurement_consistency_rejections (__main__.BenchmarkRecordTests.test_measurement_consistency_rejections) ... ok
test_nan_preserves_prior_record (__main__.BenchmarkRecordTests.test_nan_preserves_prior_record) ... ok
test_nonfinite_statistics_rejected (__main__.BenchmarkRecordTests.test_nonfinite_statistics_rejected) ... ok
test_optional_status_container_is_value_error (__main__.BenchmarkRecordTests.test_optional_status_container_is_value_error) ... ok
test_probe_status_boundaries (__main__.BenchmarkRecordTests.test_probe_status_boundaries) ... ok
test_quantiles_and_statistics (__main__.BenchmarkRecordTests.test_quantiles_and_statistics) ... ok
test_schema_missing_keys_and_wrong_types (__main__.BenchmarkRecordTests.test_schema_missing_keys_and_wrong_types) ... ok
test_strict_atomic_roundtrip_with_identity (__main__.BenchmarkRecordTests.test_strict_atomic_roundtrip_with_identity) ... ok
test_target_lengths_population_and_probe_counts (__main__.BenchmarkRecordTests.test_target_lengths_population_and_probe_counts) ... ok
test_weights_device_dtype_revision_fingerprint_rejections (__main__.BenchmarkRecordTests.test_weights_device_dtype_revision_fingerprint_rejections) ... ok

----------------------------------------------------------------------
Ran 47 tests in 2.716s

OK
C10Z_BENCH_SELFTEST_PASS tests=47
```

#### Actual engine fingerprint PASS; expected d941a9fb...d3d65 and _cov_cpu3

Artifact:`/private/tmp/c10z_v7diag_fix1/fingerprint.txt`; captured command exit 0.

```text
engine fingerprint PASS: /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/memit_dry_run/memit/memit/memit_main.py
  sha256   d941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65  (expected d941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65; pod-era 5c0c706a…)
  _cov_cpu 3  (expected 3)
```

### Independent read-only review

PROCEED — CPU build acceptance only. No remaining concrete blocker in this fix round.

Independent read-only reviewer `/root/v7_review` inspected the final source and the final 41-test evidence (9.226s), including native cleanup interruption, worker-exit deadline coverage and supervisor classification. The outer exception now preserves durable provenance mismatch details alongside measured scores.

This is a weaker-independence Codex fallback review. MPS equivalence, scientific behavior and live runtime remain UNVERIFIED. This verdict provides no dispatch approval and does not replace the required Astra re-review/freeze.

