# C10Z full build implementation report

Implementation/CPU verification: **PASS — model-free plumbing only. Scope compliance: NOT-CLEAN; attribution UNVERIFIABLE.** ASTRA: **171/171**; benchmark: **45/45**; **31/31 mutants killed**, each restored in `finally` with matching SHA-256. Engine fingerprint PASS; engine/harness diff exit 0. Live benchmark, MPS inertness, ASTRA stages and scientific efficacy are **UNVERIFIED / NOT RUN**.

Admission: operator/program confirmation 2026-10-08 00:57 MDT: P2 coordinator exited 6, HALTED `D-C10w-p2halt`; no GPU coordinator or stage live/pending, GPU idle, further GPU work requires an operator ruling. Only root executed Python, serially with the worktree venv, `-B`, absolute paths and `TMPDIR=/private/tmp/c10z_build`. Tests used CPU torch, hand-built modules and required temporary subprocess stand-ins. Neither selftest imported `c10e_bandknob`; import guards also refuse transformers/datasets. No real benchmark, inertness runner, ASTRA stage, real-tree wrapper, c10v/c10w script, model load, MPS tensor or git mutation ran.

Scope caveat: the final git-status comparison has **unattributed changes outside the build write list**. They are reproduced below; exclusive whole-workspace change provenance is UNVERIFIABLE from status snapshots. The FROZEN C10W evaluator SHA changed; other required FROZEN SHA-256s and the prereg SHA match. The C10V listing matches and the C10W listing has unattributed additions. The build tool writes and delegated edits were restricted to the authorized eight deliverables and scratch.

Read-only independent same-family reviews: initial PROCEED; final code FIX-FIRST defects were closed with new RED tests (status containers, timeout paths/freshness, overflowing integer bounds/go numbers, driver identity), followed by source PROCEED. Isolated Claude authentication probe returned loggedIn=false/exit 1; no authenticated out-of-family review or cross-family confidence is claimed.

## 1. Changed files and scope evidence

`shasum -a 256` snapshots: `/private/tmp/c10z_build/{before,after}/write-list-sha256.txt`; the terminal `after` snapshot is refreshed after this report is saved.

| Path | Before SHA-256 | After SHA-256 |
|---|---|---|
| `experiments/track_c/c10z_astra_arms.py` | `0a08b47e1f24a58b257a2c93a41691c0157d28d80fcaa806670b3123394790c8` | `806a9b4d417261945359d45db8c2f8513e4f5a2f3fafaf0b7cefe3a8d5ec3304` |
| `experiments/track_c/c10z_astra_read.py` | `87b96736405df16d99c79e457e129d4a69c13302a99741b06ac268e4288ff341` | `5b35169bac8295a1b58665b12897e91ac1f304b03a994d8a1bc08a293b708b54` |
| `experiments/track_c/c10z_astra_selftest.py` | `74638376ed89a02b153ca76726c210fc49a4fb94fe90c9e8cdbb0ef37b73ed9e` | `144141db1cb1c888d7e56fb8a80530d7a039719703f58bb998b9c7acc2c5d4d9` |
| `experiments/track_c/c10z_astra_benchmark.py` | `ABSENT` | `9b25a207f630fbfa0d60c80a74f22289ad3bb2cc160d0fc72d7e0367f9a47a1a` |
| `experiments/track_c/c10z_astra_benchmark_selftest.py` | `ABSENT` | `751b0e05703de12634d7d32331b158ca53027e5bce9d87c9df75529756567249` |
| `experiments/track_c/c10z_astra_telemetry_check.py` | `ABSENT` | `acaccaffc9caa3883378370b1f5740ce154f6ef65db3f298a8266134dc41e605` |
| `tools/run_c10z_attempt.sh` | `ABSENT` | `613b6eb41e8a532fe4105f9dd3e737ee3fd242313cc2e6a029e1537448eee61e` |
| `results/c10z_build_codex_impl.md` | `9bb0e3143c736ea16b23f34a24ca596ba5f417a0b48c28ef215d7adc698199cb` | `terminal after/write-list-sha256.txt, report row` |

The report’s own final digest is in that external terminal snapshot. Embedding its own byte-exact final SHA inside itself would change those bytes; no stale/self-referential hash is presented.

FROZEN source/input SHA table, independently hashed. The evaluator difference fails the brief’s unchanged-FROZEN scope gate; it is not attributed to a writer.

| FROZEN path | Before SHA-256 | After SHA-256 | Equal |
|---|---|---|---|
| `configs/hparams/qwen25_3b_memit_hparams.json` | `4225cc6aabc3eb9fa62d2bb2cac68b1238de3a39c5e469da635e6e1464aa3bb4` | `4225cc6aabc3eb9fa62d2bb2cac68b1238de3a39c5e469da635e6e1464aa3bb4` | YES |
| `configs/screens/g6_screen_qwen3b.json` | `a51813340571f6c68908ac4310cca197ebac9884939f58e5c33fb75833a3ca05` | `a51813340571f6c68908ac4310cca197ebac9884939f58e5c33fb75833a3ca05` | YES |
| `configs/screens/g6_screen_qwen3b_v2.json` | `482c05f8f33c59d3e469566fe6f3c48eb183d3cb2fbb791f31dcad7102517c5c` | `482c05f8f33c59d3e469566fe6f3c48eb183d3cb2fbb791f31dcad7102517c5c` | YES |
| `docs/C10W_ORACLE_PREREG.md` | `d2aa240eede4556395373678e4fab757e0e55d5491a7d4105ef765c1eb35d2f0` | `d2aa240eede4556395373678e4fab757e0e55d5491a7d4105ef765c1eb35d2f0` | YES |
| `experiments/track_c/c10e_bandknob.py` | `1f6be5811d7e58f3ebda16867a4a174b1cf24d47f9a2514cf9c3f9d29f18e695` | `1f6be5811d7e58f3ebda16867a4a174b1cf24d47f9a2514cf9c3f9d29f18e695` | YES |
| `experiments/track_c/c10p_twopass_arms.py` | `c34ecbe17c86d8f2803efc5520f4cf090dcb23bcc21ef0c3c28a12bfdaeb820f` | `c34ecbe17c86d8f2803efc5520f4cf090dcb23bcc21ef0c3c28a12bfdaeb820f` | YES |
| `experiments/track_c/c10w_oracle_eval.py` | `21f39d81695a3dc9fc144af631b48c7377c5efe08a9bf93db011dcaa8b602027` | `45f2839d0fd576bd131072c0ae8b009a0cb371ddca49b1edadb062944a775f1e` | **NO — OBSERVED DRIFT** |
| `experiments/track_c/c10w_oracle_read.py` | `162966119cf49967f39c402c73e63ebc9c673401c74f335154696eb5ab859b0b` | `162966119cf49967f39c402c73e63ebc9c673401c74f335154696eb5ab859b0b` | YES |
| `experiments/track_c/c10w_oracle_step0.py` | `c0ec236cad0d2f824616f8d5e9e29244f9604168dd5555540f2867ba1f333834` | `c0ec236cad0d2f824616f8d5e9e29244f9604168dd5555540f2867ba1f333834` | YES |
| `experiments/track_c/c10w_oracle_train.py` | `64a01fbcbbd8e836f67e623bc50f66ecff8dd59a29d7c82db3bba287d76ea463` | `64a01fbcbbd8e836f67e623bc50f66ecff8dd59a29d7c82db3bba287d76ea463` | YES |
| `memit_dry_run/memit/memit/memit_main.py` | `d941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65` | `d941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65` | YES |
| `tools/engine_fingerprint.py` | `450ee83ac829817299ead301c4a3d20702f431deaea4be58c77ecfd89a329162` | `450ee83ac829817299ead301c4a3d20702f431deaea4be58c77ecfd89a329162` | YES |
| `docs/C10V_LAYERPICK_PREREG.md` | `00981bfc9cb5770ccea203f6682d953948afdba653a4bd4173bbc754130ad524` | `00981bfc9cb5770ccea203f6682d953948afdba653a4bd4173bbc754130ad524` | YES |
| `tools/run_c10v_stage.sh` | `4c85504d07cf1cee6aebdd60e5f3cb9156ced4ea26affc482bdbaa8e724ace52` | `4c85504d07cf1cee6aebdd60e5f3cb9156ced4ea26affc482bdbaa8e724ace52` | YES |
| `experiments/track_c/c10v_layerpick_arms.py` | `2ab5b27be78b7ff63d32bd74e12b437db62e6840da297f2a1418dcfd7a9284db` | `2ab5b27be78b7ff63d32bd74e12b437db62e6840da297f2a1418dcfd7a9284db` | YES |
| `experiments/track_c/c10v_layerpick_read.py` | `8b0f9d5ac49ec633cd09d33f735d7d243f30227ad9030593114ca5fa5984ef68` | `8b0f9d5ac49ec633cd09d33f735d7d243f30227ad9030593114ca5fa5984ef68` | YES |
| `experiments/track_c/c10v_layerpick_selftest.py` | `69d57e0b9357851e3306882533afe96a2ac02fd449bbe6f1bb1295184dbcd787` | `69d57e0b9357851e3306882533afe96a2ac02fd449bbe6f1bb1295184dbcd787` | YES |

Read-only C10Z prereg before = after: `87fe3d5d28c9a51eab4eadfd82cc7175f1a94f723f25f31658c5e1aeaf628b87`.

Git porcelain comparison, including observations outside the build scope:

```text
--- before/git-status.txt
+++ after/git-status.txt
@@ -1,9 +1,18 @@
  M .gitignore
  M SESSION_CHECKPOINT.md
- M docs/LABVIZ_V2_SPEC.md
- M results/labviz_v2_codex_brief.md
+ M experiments/track_c/c10w_oracle_eval.py
+ M experiments/track_c/c10w_oracle_selftest.py
+ M experiments/track_c/c10z_astra_arms.py
+ M experiments/track_c/c10z_astra_read.py
+ M experiments/track_c/c10z_astra_selftest.py
+ M tools/c10w_p2_gate.py
+ M tools/run_c10w_p2.sh
+ M tools/run_c10w_p2_stage.sh
 ?? .ignore
 ?? architecture_profile/c10w_oracle_halt_diagnostic_20261008T060601_334913Z.json
+?? experiments/track_c/c10z_astra_benchmark.py
+?? experiments/track_c/c10z_astra_benchmark_selftest.py
+?? experiments/track_c/c10z_astra_telemetry_check.py
 ?? external_prior_art
 ?? results/autoresearch_c10_equivalence_2026-10-06T0815.json
 ?? results/autoresearch_reaim/
@@ -48,6 +57,8 @@
 ?? results/labviz/
 ?? results/labviz_codex_brief.md
 ?? results/labviz_codex_impl.md
-?? results/labviz_v2_spec_astra_delta2.md
+?? tools/c10w_p2_evaluator_A1.diff
+?? tools/c10w_p2_rerun.py
 ?? tools/labviz/
 ?? tools/labviz_serve.sh
+?? tools/run_c10z_attempt.sh
```

Observed outside-list status changes: `experiments/track_c/c10w_oracle_eval.py` and `experiments/track_c/c10w_oracle_selftest.py` gain `M`; `tools/c10w_p2_evaluator_A1.diff` and `tools/c10w_p2_rerun.py` gain untracked entries; the prior `M` entries for `docs/LABVIZ_V2_SPEC.md` and `results/labviz_v2_codex_brief.md` disappear; `results/labviz_v2_spec_astra_delta2.md`’s prior untracked entry disappears. These are **observations, unattributed**. No build command or delegated edit targeted them; they were neither repaired nor reverted. The report is ignored/untracked by the status view, so its digest is captured independently.

Frozen c10w result listing: **OBSERVED CHANGE, UNATTRIBUTED**, 57 files before / 62 after. Full `find … -type f | sort` records: `before/c10w-result-files.txt`, `after/c10w-result-files.txt` under the scratch root.

```text
--- 
+++ 
@@ -1,3 +1,8 @@
+/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/c10w_oracle/_quarantine_selftest_leak_20261008/README.md
+/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/c10w_oracle/_quarantine_selftest_leak_20261008/c10w_oracle_halt_diagnostic_20261008T075101_137852Z.json
+/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/c10w_oracle/_quarantine_selftest_leak_20261008/p2_20261008T075056_661871Z/HALT.json
+/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/c10w_oracle/_quarantine_selftest_leak_20261008/p2_20261008T075056_661871Z/p2-a7-s1.log
+/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/c10w_oracle/_quarantine_selftest_leak_20261008/p2_20261008T075056_661871Z/preflight.json
 /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/c10w_oracle/p1_20261007T223707_598959Z/adapters/A1_single_s0_r16.safetensors
 /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/c10w_oracle/p1_20261007T223707_598959Z/adapters/A2_coherent2_s0_r16.safetensors
 /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/c10w_oracle/p1_20261007T223707_598959Z/adapters/A7_canon_s0_r16.safetensors
```

Frozen c10v result listing: **UNCHANGED**, 7 files before / 7 after. Full `find … -type f | sort` records: `before/c10v-result-files.txt`, `after/c10v-result-files.txt` under the scratch root.

## 2. Numbered test list, names and source clauses

Items 1–96 were listed before initial production edits; review regressions 97–108 were listed before their tests/fixes. The retained plan is `/private/tmp/c10z_build/preproduction-test-list.md`. The mapping below expands shorthand into actual `class.method` names and corrects spec-v2 test-number pointers.

1. `IdleGapTests.test_i_idle_expiry` → §9.1(f′), v3 §D(i).
2. `IdleGapTests.test_ii_late_entry` → §9.1(f′), v3 §D(ii).
3. `IdleGapTests.test_iii_deadline_samples` → §9.1(f′), v3 §D(iii).
4. `IdleGapTests.test_iv_process2_envelope` → §9.1(f′), v3 §D(iv).
5. `IdleGapTests.test_v_complete01_only_enter` → §9.1(f′), v3 §D(v).
6. `IdleGapTests.test_vi_mutation_deadlines` → §9.1(f′)(vi).
7. `IdleGapTests.test_vii_entry_invariant` → §9.1(f′), v3 §D(vii), already-green invariant.
8. `IdleGapTests.test_viii_single_timestamp` → §9.1(f′)(viii).
9. `IdleGapTests.test_ix_transition_lock` → §9.1(f′)(ix), instrumented barrier.
10. `BudgetBoundTests.test_c01_neighbors` → §9.1(a′), brief §2B/§4.
11. `LaunchBindingTests.test_switch_zero`, `LaunchBindingTests.test_switch_true`, `LaunchBindingTests.test_switch_empty`, `LaunchBindingTests.test_switch_space` → §9.1(b′3)(2), (h′1).
12. `LaunchBindingTests.test_record_required`, `LaunchBindingTests.test_record_absolute`, `LaunchBindingTests.test_record_outside`, `LaunchBindingTests.test_record_unreadable` → §9.1(b′3)(3).
13. `LaunchBindingTests.test_record_selection`, `LaunchBindingTests.test_record_nonstrict` → §9.1(b′3)(4), same bytes once.
14. `LaunchBindingTests.test_script`, `LaunchBindingTests.test_sources`, `LaunchBindingTests.test_environment` → §9.1(b′3)(5).
15. `LaunchBindingTests.test_record_invalid` → §9.1(b′3)(6), raw-summary consistency.
16. `LaunchBindingTests.test_refused`, `LaunchBindingTests.test_derived` → §9.1(b′3)(7).
17. `LaunchBindingTests.test_stop`, `LaunchBindingTests.test_c01`, `LaunchBindingTests.test_total` → §9.1(b′3)(8), isolated derived/go.
18. `LaunchBindingTests.test_go_ceilings` → §9.1(b′3)(9).
19. `LaunchBindingTests.test_stage2_override`, `LaunchBindingTests.test_stage3_override` → §9.1(b′3)(10).
20. `LaunchBindingTests.test_go_fields` → §9.1(b′2), missing/type/hex/ceiling cases.
21. `LaunchBindingTests.test_success_roundtrip` → §9.1(b′3), brief §4.
22. `LaunchBindingTests.test_substitution` → §9.1(b′3)(4), valid second-record/raw substitution.
23. `LaunchBindingTests.test_stage3_record_drift`, `LaunchBindingTests.test_stage3_script_drift`, `LaunchBindingTests.test_stage3_source_drift`, `LaunchBindingTests.test_stage3_environment_drift` → §9.1(d′).
24. `LaunchBindingTests.test_stage3_switch` → §9.1(h′1), absent/different/invalid switches.
25. `LaunchBindingTests.test_inertness_required`, `LaunchBindingTests.test_inertness_path`, `LaunchBindingTests.test_inertness_json`, `LaunchBindingTests.test_inertness_verdict`, `LaunchBindingTests.test_inertness_sources`, `LaunchBindingTests.test_inertness_environment`, `LaunchBindingTests.test_inertness_schema`, `LaunchBindingTests.test_inertness_counts`, `LaunchBindingTests.test_inertness_success` → §9.1(h′3), brief §2G/T8.
26. `LaunchBindingTests.test_stage3_inertness_drift` → §9.1(d′)/(h′3).
27. `ReaderBindingTests.test_c01_neighbors` → §9.1(e′), range/bool/finite bounds.
28. `ReaderBindingTests.test_pass_launch`, `ReaderBindingTests.test_go_ceilings`, `ReaderBindingTests.test_benchmark_sha`, `ReaderBindingTests.test_history_ceilings`, `ReaderBindingTests.test_scope_ceiling`, `ReaderBindingTests.test_process_ceilings` → §9.1(e′), in-range provenance.
29. `WrapperTests.test_next_stage_types` → v3 §G, brief §4.
30. `WrapperTests.test_relative_out` → v3 §G, brief §4.
31. `WrapperTests.test_stage0_failure` → v3 §G, brief §4.
32. `PinTests.test_temp_copy_byte_drift` → brief §2F/§4, existing pin assertion baseline RED.
33. `TelemetryIntegrationTests.test_on_off_science` → §9.1(h′4), T1/T2/T3/T9, real write_arm/arm_hook.
34. `TelemetryIntegrationTests.test_resident_on_off` → §9.1(h′4)/(h′5), T1/T2, real resident.
35. `TelemetryIntegrationTests.test_placements_ast` → §9.1(h′5), brief §4 AST boundaries.
36. `TelemetryUnitTests.test_T4_public_methods_avoid_science_clocks_and_gates` → §9.1(h′4), T4/M12/M31.
37. `TelemetryUnitTests.test_T3_header_four_kinds_fields_and_full_cost_accounting` → §2D, T3, strict roundtrip.
38. `TelemetryUnitTests.test_T5a_initial_open_failure_is_disabled_once` → T5a.
39. `TelemetryUnitTests.test_T5a_directory_failure_is_disabled_once` → T5a.
40. `TelemetryUnitTests.test_T5b_write_failure_is_disabled_once` → T5b.
41. `TelemetryUnitTests.test_T5c_flush_failure_is_disabled_once` → T5c.
42. `TelemetryUnitTests.test_T5d_fsync_failure_is_disabled_once` → T5d.
43. `TelemetryUnitTests.test_T5e_keyboard_interrupt_propagates` → T5e/M29.
44. `TelemetryUnitTests.test_T6_each_call_preserves_cpu_model_and_inputs` → §9.1(h′4), T6.
45. `TelemetryUnitTests.test_T6_lens_uses_layer_output_top5_and_no_grad` → §9.1(h′5), T6/M27/M28.
46. `TelemetryUnitTests.test_T7_probabilities_dense_reference_and_row_chunk_bound` → §2D, T7.
47. `TelemetryUnitTests.test_T7_default_chunk_keeps_cpu_float32_under64MiB` → §2D.
48. `TelemetryUnitTests.test_T9_write_volume_no_requirement_lines` → §9.1(h′5), T9/M30.
49. `TelemetryInertnessTests.test_deterministic_three_pass_schedule_and_kwargs` → §2G, §9.1(h′3).
50. `TelemetryInertnessTests.test_lens_sensitive_probe_is_not_inert` → §2G.
51. `TelemetryInertnessTests.test_lens_sensitive_batch_is_not_inert` → §2G.
52. `TelemetryInertnessTests.test_plain_drift_is_nondeterministic_baseline` → §2G.
53. `TelemetryInertnessTests.test_full_greedy_suffix_count_and_compare` → §2G.
54. `TelemetryRunnerTests.test_runner_import_is_stdlib_only` → §2G.
55. `TelemetryRunnerTests.test_runner_refuses_relative_out_path` → §2G.
56. `TelemetryRunnerTests.test_runner_refuses_outside_and_existing_record_without_forward` → §2G.
57. `TelemetryRunnerTests.test_runner_roundtrip_identity_and_no_write_engine_calls` → §2G/T8.
58. `TelemetryRunnerTests.test_runner_checks_all36_weights_and_invalid_is_exit2` → §2G.
59. `BenchmarkPopulationTests.test_population_batch_and_digest_match_driver` → spec v2 test1.
60. `BenchmarkPopulationTests.test_full_population_forward_counts` → spec v2 test1/test2(a), complete forward-count schedule
61. `BenchmarkPopulationTests.test_greedy_argmax_and_no_grad` → spec v2 test2(b)/(c)
62. `BenchmarkPopulationTests.test_timed_reads_heartbeat_and_warmup_exclusion` → spec v2 test2(d)/test5
63. `BenchmarkPopulationTests.test_guarded_loop_completes_item_then_stops` → spec v2 test4/test5
64. `BenchmarkRecordTests.test_quantiles_and_statistics` → spec v2 test3
65. `BenchmarkRecordTests.test_nonfinite_statistics_rejected` → spec v2 test3
66. `BenchmarkRecordTests.test_probe_status_boundaries` → §4 status boundaries, M14.
67. `BenchmarkRecordTests.test_strict_atomic_roundtrip_with_identity` → spec v2 test8.
68. `BenchmarkRecordTests.test_nan_preserves_prior_record` → spec v2 test8.
69. `BenchmarkRecordTests.test_interrupted_replace_preserves_prior_record` → spec v2 test8.
70. `BenchmarkRecordTests.test_schema_missing_keys_and_wrong_types` → spec v2 test8.
71. `BenchmarkRecordTests.test_measurement_consistency_rejections` → §9.1(b′1), M20.
72. `BenchmarkRecordTests.test_weights_device_dtype_revision_fingerprint_rejections` → brief §2C.
73. `BenchmarkRecordTests.test_target_lengths_population_and_probe_counts` → full inertness schedule, brief §2G.
74. `BenchmarkIdentityTests.test_source_identity_exact_order_and_root` → §9.1(b′1).
75. `BenchmarkIdentityTests.test_environment_identity_metadata_only` → §9.1(b′1).
76. `BenchmarkIdentityTests.test_top_level_import_stdlib_only_subprocess` → brief §2C.
77. `BenchmarkIdentityTests.test_environment_identity_no_torch_subprocess` → brief §4.
78. `BenchmarkCeilingTests.test_eight_v3_calibration_cases` → spec v2 test12, v3 §C.
79. `BenchmarkCeilingTests.test_raw_values_drive_all_terms` → §9.1(b′1).
80. `BenchmarkCeilingTests.test_mean_outlier_and_complete_eval_tstar` → spec v2 test12.
81. `BenchmarkCeilingTests.test_optional_minima_and_timeout_lower_bound` → spec v2 test7/test12, skipped optional minima and SVD lower bound
82. `BenchmarkCeilingTests.test_refused_records_never_fallback_or_numbers` → spec v2 test12/M15.
83. `BenchmarkCeilingTests.test_exact_rounding_and_c01_stop_boundary` → brief §4.
84. `BenchmarkLifecycleTests.test_start_and_phase_fit_boundaries` → spec v2 test4, brief §4.
85. `BenchmarkLifecycleTests.test_supervisor_600_boundary_fake_clock` → spec v2 test6.
86. `BenchmarkLifecycleTests.test_supervisor_real_process_group_kill_and_interrupted_record` → spec v2 test6.
87. `BenchmarkLifecycleTests.test_supervisor_completed_worker_untouched` → spec v2 test6.
88. `BenchmarkLifecycleTests.test_system_wide_monotonic_subprocess` → spec v2 cross-process clock.
89. `BenchmarkLifecycleTests.test_svd_timeout_565_lower_bound_and_worker_survival` → spec v2 test7
90. `BenchmarkLifecycleTests.test_out_path_refusals_and_prefix_trap` → spec v2 test9
91. `BenchmarkLifecycleTests.test_env_preflight_refusals` → spec v2 test11.
92. `BenchmarkLifecycleTests.test_injected_worker_full_schedule_no_writer_calls` → spec v2 test10
93. `BenchmarkLifecycleTests.test_worker_mutation_invalid_and_refused` → spec v2 test10
94. `BenchmarkLifecycleTests.test_worker_load_over_300_invalid` → spec v2 mandatory phase.
95. `BenchmarkLifecycleTests.test_worker_guard_status_bands_and_reserved_after_hash` → spec v2 test4.
96. `BenchmarkLifecycleTests.test_optional_skip_keeps_top_level_status` → spec v2 test7/test12
97. `BenchmarkRecordTests.test_optional_status_container_is_value_error` → brief §2C ValueError schema boundary.
98. `BenchmarkPopulationTests.test_empty_population_leaves_no_heartbeat` → spec v2 worker lifecycle.
99. `BenchmarkPopulationTests.test_guarded_warmup_records_actual_count` → spec v2 test4/test5, actual warmup measurement count
100. `BenchmarkLifecycleTests.test_supervisor_forbidden_astra_cap_preserves_directory` → spec v2 §0/test9
101. `BenchmarkLifecycleTests.test_supervisor_existing_record_cap_preserves_bytes` → spec v2 test9 freshness
102. `LaunchBindingTests.test_record_optional_status` → brief §2B step6 intended V12 refusal before writes.
103. `BudgetBoundTests.test_huge_integer_refusal` → brief §2B invalid stage01 must HALT.
104. `ReaderBindingTests.test_huge_integer_refusal` → brief §2B phase01 clock provenance.
105. `BenchmarkRecordTests.test_huge_integer_timing_is_value_error` → brief §2C schema ValueError boundary.
106. `TelemetryRunnerTests.test_runner_driver_module_reused` → spec v2 advisor A6, read-only helper module identity.
107. `BenchmarkLifecycleTests.test_supervisor_outside_benchmark_cap_preserves_directory` → spec v2 worker preflight/output namespace at cap.
108. `LaunchBindingTests.test_go_huge_integer_ceiling_refusal` → §9.1(b′2)/(b′3)(9), finite positive JSON integer schema then go-selection refusal.

All original 79 tests remain in the full suite; their scientific assertion bodies were preserved except the expressly permitted noceil expectation. Original constructor/schedule/launch values were adapted as detailed in §4. The original pin assertion now compares with the revised prereg SHA; a temp-copy byte-drift test also fails as expected.

## 3. Test-first RED and GREEN evidence

Untouched baseline, exact venv `python -B …/c10z_astra_selftest.py`: 79 tests, 67.454 s, **one expected pin assertion failure**, zero errors. Saved full output `/private/tmp/c10z_build/baseline.log`; last 15 lines:

```text
Prereg :137, :204, :219, :224: round-trip, immutable outputs, finite science.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 776, in test_json_real_writer_and_frozen_sources
    self.assertEqual(hashlib.sha256((ROOT/"docs/C10Z_ASTRA_PREREG.md").read_bytes()).hexdigest(),PREREG)
AssertionError: '87fe3d5d28c9a51eab4eadfd82cc7175f1a94f723f25f31658c5e1aeaf628b87' != '38f8b68cc2f82d78e0689bff18bfa44f7600e2fe7b1484b07b4e1e88e267b072'
- 87fe3d5d28c9a51eab4eadfd82cc7175f1a94f723f25f31658c5e1aeaf628b87
+ 38f8b68cc2f82d78e0689bff18bfa44f7600e2fe7b1484b07b4e1e88e267b072


----------------------------------------------------------------------
Ran 79 tests in 67.454s

FAILED (failures=1)
C10Z_ASTRA_SELFTEST_FAIL tests=79
```

Before production, the idle-only run drove real `Session.stage1` through `_budget`’s inspected-signature adapter. Nine tests / 0.023 s: **8 behavioral assertion failures, zero errors; (vii) already PASS**. No TypeError/KeyError/AttributeError/project failure is counted as idle RED. An initial version of (vii) had not driven the required stage1 path; its harness was corrected before any production edit, then the authoritative nine-test RED was saved as `idle-red.log`.

| Idle test | Original behavioral assertion message | Final suite |
|---|---|---|
| `IdleGapTests.test_i_idle_expiry` | Halt not raised : idle gap escaped the stage01 deadline | PASS |
| `IdleGapTests.test_ii_late_entry` | Halt not raised : late stage2 entry was accepted | PASS |
| `IdleGapTests.test_iii_deadline_samples` | unexpectedly None : stage1 return or idle had no active deadline | PASS |
| `IdleGapTests.test_iv_process2_envelope` | 7460.0 != 7200.0 : process2 fell back to stage3 during idle | PASS |
| `IdleGapTests.test_ix_transition_lock` | False is not true : deadline() returned while enter(2) held the transition lock | PASS |
| `IdleGapTests.test_v_complete01_only_enter` | Lists differ: ['Session.stage1'] != ['Budget.enter'] | PASS |
| `IdleGapTests.test_vi_mutation_deadlines` | None unexpectedly found in [None, None, None, 7395.0] : an active-set mutation exposed no deadline | PASS |
| `IdleGapTests.test_viii_single_timestamp` | Halt not raised : entry decision did not use its first timestamp | PASS |
| `IdleGapTests.test_vii_entry_invariant` | Already green, preserves entry invariant | PASS |

Initial all-tests RED: `all-red.log`, 166 tests / 48.757 s, failures=135, errors=60 (subtest counts; old scientific fixture mismatches and absent new APIs are separate from the idle behavioral proof). Benchmark RED before its production file existed: `bench-red.log`, 38 tests / 0.091 s, failures=2, errors=59.

Existing tests that failed against original producer/reader because of revised fixture/signature provenance, not claimed as new behavioral RED:

- `SpecTests.test_band_boundaries_ordered`
- `SpecTests.test_budget_origins_prestart_deadlines_round_memory`
- `SpecTests.test_review_stage_call_refusals`
- `SpecTests.test_side_gate_boundaries_and_populations`
- `SpecTests.test_ttl_every_Z_arm_and_incomplete_actual_repro_failure`
- `SpecTests.test_w1_even_median_w2_subject_free`
- `SpecTests.test_worked_15`
- `SpecTests.test_worked_16`
- `SpecTests.test_worked_17`
- `SpecTests.test_worked_18`
- `SpecTests.test_worked_19`
- `SpecTests.test_worked_20`
- `SpecTests.test_worked_21`
- `SpecTests.test_worked_23`
- `SpecTests.test_z2_ambiguous_and_all_validity_gates`
- `Fix1Tests.test_B3_clean_survivor_without_stage2_ceiling_keeps_stage1_record`
- `Fix1Tests.test_fix1_go_launch_copy_and_manifest_sha`
- `Fix1Tests.test_fix1_watchdog_preserves_last_published_record`
- `Fix2Tests.test_fix2_child_receives_parent_resolved_absolute_outdir`
- `Fix2Tests.test_fix2_resident_stops_at_parent_halt_and_preserves_session_fields`
- `SpecTests.test_completed_stage2_keeps_stage1_round_ceiling`
- `SpecTests.test_k1_k2_omissions_and_replication`
- `SpecTests.test_law3_both_sides`
- `SpecTests.test_review_reader_instrument_ceilings_audits_and_capacity`
- `SpecTests.test_worked22_validity_precedes_conditional_label`
- `SpecTests.test_worked_01`
- `SpecTests.test_worked_02`
- `SpecTests.test_worked_03`
- `SpecTests.test_worked_04`
- `SpecTests.test_worked_05`
- `SpecTests.test_worked_06`
- `SpecTests.test_worked_07`
- `SpecTests.test_worked_08`
- `SpecTests.test_worked_09`
- `SpecTests.test_worked_10`
- `SpecTests.test_worked_11`
- `SpecTests.test_worked_12`
- `SpecTests.test_worked_24`
- `Fix1Tests.test_B2_stray_stage_call_after_terminal_K1_keeps_the_result`
- `Fix1Tests.test_fix1_absent_ceilings_terminal_labels_and_resident_close`
- `Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write`
- `Fix2Tests.test_fix2_session_record_absent_ceiling_matches_reader_omissions`

These include old Budget argument bindings, 5400-versus-C01 fixture provenance, go/pin metadata and launch/scope records. They are expected transitional failures. The actual scientific assertions are green in the final full suite.

Review regressions: `review-root-red.log` / `review-launch-red.log` captured C01 huge-int OverflowError and six malformed optional-status TypeErrors; an initial `eval` fixture key was corrected to actual `eval_A7` and rerun before the fix. `review-bench-red.log`: six tests, four behavioral failures and eleven subtest errors (six status containers/five overflowing timing values); `review-loader-red.log`: one identity assertion failure; `review-namespace-red.log`: one missing output refusal failure; `review-go-int-red.log`: one go-number OverflowError. Every added regression is included in final GREEN. The three prematurely applied benchmark hardening edits were reverted before adding/running their new tests, then reapplied only after root recorded their RED.

T3’s first open spy counted unrelated lazy torch file reads; its observation filter was narrowed to the telemetry JSONL path while preserving the one-append-open assertion. T7’s original CPU fp32 calculation missed 1e-6 on offset logits; the strong reference assertion was retained and production now centers an owned chunk before logsumexp/exp. Telemetry GREEN: 26 tests / 4.261 s, then all final tests in the complete suite.

## 4. Changed seams and every fixture adaptation

LAW#4 source reads covered prereg §2.11/§2.12/§6/§9/§9.1, complete v3 and benchmark spec v2, the three original ASTRA files, existing stage wrapper and installed Qwen2 `modeling_qwen2.py:528–570`. §9.1 precedence was applied; no governing-source disagreement was found. Layer output indexing and final-norm exclusion use the installed source convention.

- C01 input/range, RLock deadline transition, one timestamp, live idle deadline; complete01 body unchanged and referenced only inside enter: `experiments/track_c/c10z_astra_arms.py:84`, `experiments/track_c/c10z_astra_arms.py:98`, `experiments/track_c/c10z_astra_arms.py:110`, `experiments/track_c/c10z_astra_arms.py:1428`.
- ordered before-write launch admission and stage3 re-verification; current ROOT evaluated at call time: `experiments/track_c/c10z_astra_arms.py:1517`, `experiments/track_c/c10z_astra_arms.py:1544`, `experiments/track_c/c10z_astra_arms.py:1551`, `experiments/track_c/c10z_astra_arms.py:1565`, `experiments/track_c/c10z_astra_arms.py:1617`, `experiments/track_c/c10z_astra_arms.py:1651`, `experiments/track_c/c10z_astra_arms.py:1693`, `experiments/track_c/c10z_astra_arms.py:1777`.
- range plus complete scope/history/launch/go/pair ceiling provenance: `experiments/track_c/c10z_astra_read.py:457`, `experiments/track_c/c10z_astra_read.py:649`, `experiments/track_c/c10z_astra_read.py:668`.
- separate performance clock, append-once strict JSONL, fsync/fail-soft Exception boundary, native lens/no_grad and full warm/P1/T/P2 equality: `experiments/track_c/c10z_astra_arms.py:339`, `experiments/track_c/c10z_astra_arms.py:355`, `experiments/track_c/c10z_astra_arms.py:378`, `experiments/track_c/c10z_astra_arms.py:401`, `experiments/track_c/c10z_astra_arms.py:412`, `experiments/track_c/c10z_astra_arms.py:422`, `experiments/track_c/c10z_astra_arms.py:434`, `experiments/track_c/c10z_astra_arms.py:444`.
- exact guarded telemetry event placement; scientific producers carry no telemetry fields: `experiments/track_c/c10z_astra_arms.py:805`, `experiments/track_c/c10z_astra_arms.py:827`, `experiments/track_c/c10z_astra_arms.py:874`, `experiments/track_c/c10z_astra_arms.py:968`.
- pure identity/statistics/schema/ceiling core, read-only native forward schedule, mandatory hash reserve, optional fit guards and clock-first supervisor: `experiments/track_c/c10z_astra_benchmark.py:81`, `experiments/track_c/c10z_astra_benchmark.py:85`, `experiments/track_c/c10z_astra_benchmark.py:123`, `experiments/track_c/c10z_astra_benchmark.py:252`, `experiments/track_c/c10z_astra_benchmark.py:278`, `experiments/track_c/c10z_astra_benchmark.py:299`, `experiments/track_c/c10z_astra_benchmark.py:312`, `experiments/track_c/c10z_astra_benchmark.py:334`, `experiments/track_c/c10z_astra_benchmark.py:376`, `experiments/track_c/c10z_astra_benchmark.py:442`, `experiments/track_c/c10z_astra_benchmark.py:538`, `experiments/track_c/c10z_astra_benchmark.py:561`.
- stdlib import, reused canonical driver, output admission, injected-H seam and all36 weight hashes: `experiments/track_c/c10z_astra_telemetry_check.py:19`, `experiments/track_c/c10z_astra_telemetry_check.py:25`, `experiments/track_c/c10z_astra_telemetry_check.py:37`, `experiments/track_c/c10z_astra_telemetry_check.py:51`, `experiments/track_c/c10z_astra_telemetry_check.py:77`, `experiments/track_c/c10z_astra_telemetry_check.py:85`.
- New shell wrapper: `tools/run_c10z_attempt.sh:1`; exact v3 §G block including `-I`; executable mode 0755.


§2F fixture edits (new lines; original locations identify the brief seam):

- `experiments/track_c/c10z_astra_selftest.py:224`: original 220–224: 5400 fixture/scope → C01_FIX=7800; default synthetic fixture only.
- `experiments/track_c/c10z_astra_selftest.py:267`: original 267: each history entry gets a copy of record ceilings and matching scope ceiling_s.
- `experiments/track_c/c10z_astra_selftest.py:637`: original 632–650: all Budget constructors gain C01_FIX, old absolute deadline coordinates become C01-relative, explicit complete01 calls deleted.
- `experiments/track_c/c10z_astra_selftest.py:878`: original 881: default Budget gains C01_FIX.
- `experiments/track_c/c10z_astra_selftest.py:1022`: original 1020: clock becomes C01_FIX−1 and constructor gains C01_FIX.
- `experiments/track_c/c10z_astra_selftest.py:1047`: original 1078–1080 successful stage3 uses real temp benchmark binding and selected pass ceilings, re-sealed; verify_launch_binding is not mocked.
- `experiments/track_c/c10z_astra_selftest.py:1137`: original 1147: default persisted launch uses _launch.
- `experiments/track_c/c10z_astra_selftest.py:1182`: new helper: synthetic stage01/go/benchmark/telemetry provenance, overridable per fixture.
- `experiments/track_c/c10z_astra_selftest.py:1193`: original 1175–1178: three benchmark selection fields, optional binding override.
- `experiments/track_c/c10z_astra_selftest.py:1913`: new helper: read/copy exactly seven sources, real identities/validate/ceilings/writer, raw .056 seconds gives t*=.070 and 7800/12600/20460.
- `experiments/track_c/c10z_astra_selftest.py:1201`: original 1181–1188: temp ROOT, lazy benchmark seam, actual record/env and selected go.
- `experiments/track_c/c10z_astra_selftest.py:1225`: original 1210: patch lazy benchmark import seam for temp ROOT.
- `experiments/track_c/c10z_astra_selftest.py:1253`: original 1237: _launch(stage2=None,stage3=None).
- `experiments/track_c/c10z_astra_selftest.py:1265`: original 1249: same missing-expansion launch fixture.
- `experiments/track_c/c10z_astra_selftest.py:1283`: original 1286/1299–1300: remove stub stage1.complete01; new five-argument Budget factory, controlled clock; optional metrics only for T2 proof.
- `experiments/track_c/c10z_astra_selftest.py:1384`: original 1347–1365: real temp benchmark and binding-aware go equality assertions.
- `experiments/track_c/c10z_astra_selftest.py:1483`: original 1451–1452: _launch preserves own stage2=60/stage3=None.
- `experiments/track_c/c10z_astra_selftest.py:1511`: original 1485–1486: _launch preserves absent expansions.
- `experiments/track_c/c10z_astra_selftest.py:1560`: original 1528: patch lazy benchmark module seam.
- `experiments/track_c/c10z_astra_selftest.py:1571`: original 1533–1546: real temp benchmark, binding-aware go and env.
- `experiments/track_c/c10z_astra_selftest.py:1632`: original 1624–1627: own launch values retained and Budget factory signature updated.
- `experiments/track_c/c10z_astra_selftest.py:1695`: original 1662: re-seal history after modifying fixture ceilings before record().
- `experiments/track_c/c10z_astra_selftest.py:1733`: original 1699: Budget gains C01_FIX.
- `experiments/track_c/c10z_astra_selftest.py:19`: pin updated to the actual revised prereg digest; line 20 defines C01_FIX. This fixture is never treated as the live selected ceiling.

**One permitted assertion change:** the noceil case in `experiments/track_c/c10z_astra_selftest.py:1047` now requires `HALTED-V12: stage3 requires`, retaining `launched == []`. Its pass says stage3=24000 and its launch says None; §9.1(e′) now rejects that mismatch first. The pre-existing absent-stage3 gate at original arms:1484 (current stage_call) is unreachable through a directory whose pass ceilings equal its launch. It is preserved.

## 5. Final complete suites

Command: `TMPDIR=/private/tmp/c10z_build /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python -B /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py` (stdout/stderr saved to scratch); exit **0**. Exact last 15 lines:

```text
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
Ran 171 tests in 83.023s

OK
C10Z_ASTRA_SELFTEST_PASS tests=171
```

Command: `TMPDIR=/private/tmp/c10z_build /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python -B /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_benchmark_selftest.py` (stdout/stderr saved to scratch); exit **0**. Exact last 15 lines:

```text
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
Ran 45 tests in 2.521s

OK
C10Z_BENCH_SELFTEST_PASS tests=45
```

Both main guards assert `"c10e_bandknob" not in sys.modules` before printing their PASS markers. The benchmark suite is 2.521 s, below its 90-s bound.

## 6. Mutation check

For each M1–M31, `/private/tmp/c10z_build/mutate.py` backed up its target bytes under `mut_backup/M<n>/`, applied that prescribed mutant in place, ran its relevant named tests in a fresh root-owned serial interpreter, then restored bytes from backup in `finally` and compared SHA-256. All mutants were killed; **no survivors and no added post-mutation tests**. Detailed tracebacks: `mutations-M<n>.log`; per-mutant pre/mutated/restored hashes: `mutations/M<n>.json`.

| Mutant | Failing named tests (including subtests) | Failures / errors | Restored SHA-256 = pre-mutation |
|---|---|---|---|
| M1 | `IdleGapTests.test_viii_single_timestamp` | 1 / 0 | `806a9b4d417261945359d45db8c2f8513e4f5a2f3fafaf0b7cefe3a8d5ec3304` |
| M2 | `IdleGapTests.test_vi_mutation_deadlines` | 1 / 0 | `806a9b4d417261945359d45db8c2f8513e4f5a2f3fafaf0b7cefe3a8d5ec3304` |
| M3 | `IdleGapTests.test_ix_transition_lock` | 1 / 0 | `806a9b4d417261945359d45db8c2f8513e4f5a2f3fafaf0b7cefe3a8d5ec3304` |
| M4 | `IdleGapTests.test_i_idle_expiry`, `IdleGapTests.test_v_complete01_only_enter` | 2 / 0 | `806a9b4d417261945359d45db8c2f8513e4f5a2f3fafaf0b7cefe3a8d5ec3304` |
| M5 | `BudgetBoundTests.test_c01_neighbors` | 1 / 0 | `806a9b4d417261945359d45db8c2f8513e4f5a2f3fafaf0b7cefe3a8d5ec3304` |
| M6 | `BudgetBoundTests.test_c01_neighbors` | 1 / 0 | `806a9b4d417261945359d45db8c2f8513e4f5a2f3fafaf0b7cefe3a8d5ec3304` |
| M7 | `LaunchBindingTests.test_total` | 1 / 0 | `806a9b4d417261945359d45db8c2f8513e4f5a2f3fafaf0b7cefe3a8d5ec3304` |
| M8 | `LaunchBindingTests.test_derived` | 1 / 0 | `806a9b4d417261945359d45db8c2f8513e4f5a2f3fafaf0b7cefe3a8d5ec3304` |
| M9 | `LaunchBindingTests.test_script` | 1 / 0 | `806a9b4d417261945359d45db8c2f8513e4f5a2f3fafaf0b7cefe3a8d5ec3304` |
| M10 | `LaunchBindingTests.test_success_roundtrip` | 0 / 1 | `806a9b4d417261945359d45db8c2f8513e4f5a2f3fafaf0b7cefe3a8d5ec3304` |
| M11 | `TelemetryIntegrationTests.test_on_off_science` | 1 / 0 | `806a9b4d417261945359d45db8c2f8513e4f5a2f3fafaf0b7cefe3a8d5ec3304` |
| M12 | `TelemetryUnitTests.test_T4_public_methods_avoid_science_clocks_and_gates` | 1 / 0 | `806a9b4d417261945359d45db8c2f8513e4f5a2f3fafaf0b7cefe3a8d5ec3304` |
| M13 | `ReaderBindingTests.test_c01_neighbors` | 5 / 0 | `5b35169bac8295a1b58665b12897e91ac1f304b03a994d8a1bc08a293b708b54` |
| M14 | `BenchmarkRecordTests.test_probe_status_boundaries` | 1 / 0 | `9b25a207f630fbfa0d60c80a74f22289ad3bb2cc160d0fc72d7e0367f9a47a1a` |
| M15 | `BenchmarkCeilingTests.test_refused_records_never_fallback_or_numbers` | 2 / 0 | `9b25a207f630fbfa0d60c80a74f22289ad3bb2cc160d0fc72d7e0367f9a47a1a` |
| M16 | `WrapperTests.test_next_stage_types` | 1 / 0 | `613b6eb41e8a532fe4105f9dd3e737ee3fd242313cc2e6a029e1537448eee61e` |
| M17 | `LaunchBindingTests.test_record_selection`, `LaunchBindingTests.test_substitution` | 2 / 0 | `806a9b4d417261945359d45db8c2f8513e4f5a2f3fafaf0b7cefe3a8d5ec3304` |
| M18 | `LaunchBindingTests.test_sources` | 1 / 0 | `806a9b4d417261945359d45db8c2f8513e4f5a2f3fafaf0b7cefe3a8d5ec3304` |
| M19 | `LaunchBindingTests.test_environment` | 1 / 0 | `806a9b4d417261945359d45db8c2f8513e4f5a2f3fafaf0b7cefe3a8d5ec3304` |
| M20 | `BenchmarkRecordTests.test_measurement_consistency_rejections` | 8 / 0 | `9b25a207f630fbfa0d60c80a74f22289ad3bb2cc160d0fc72d7e0367f9a47a1a` |
| M21 | `LaunchBindingTests.test_c01` | 2 / 2 | `806a9b4d417261945359d45db8c2f8513e4f5a2f3fafaf0b7cefe3a8d5ec3304` |
| M22 | `LaunchBindingTests.test_stage3_record_drift`, `LaunchBindingTests.test_stage3_script_drift`, `LaunchBindingTests.test_stage3_source_drift`, `LaunchBindingTests.test_stage3_environment_drift` | 4 / 0 | `806a9b4d417261945359d45db8c2f8513e4f5a2f3fafaf0b7cefe3a8d5ec3304` |
| M23 | `ReaderBindingTests.test_pass_launch` | 2 / 0 | `5b35169bac8295a1b58665b12897e91ac1f304b03a994d8a1bc08a293b708b54` |
| M24 | `ReaderBindingTests.test_process_ceilings` | 1 / 0 | `5b35169bac8295a1b58665b12897e91ac1f304b03a994d8a1bc08a293b708b54` |
| M25 | `ReaderBindingTests.test_history_ceilings`, `ReaderBindingTests.test_scope_ceiling` | 2 / 0 | `5b35169bac8295a1b58665b12897e91ac1f304b03a994d8a1bc08a293b708b54` |
| M26 | `LaunchBindingTests.test_inertness_required` | 1 / 0 | `806a9b4d417261945359d45db8c2f8513e4f5a2f3fafaf0b7cefe3a8d5ec3304` |
| M27 | `TelemetryUnitTests.test_T6_lens_uses_layer_output_top5_and_no_grad` | 1 / 0 | `806a9b4d417261945359d45db8c2f8513e4f5a2f3fafaf0b7cefe3a8d5ec3304` |
| M28 | `TelemetryUnitTests.test_T6_lens_uses_layer_output_top5_and_no_grad` | 1 / 0 | `806a9b4d417261945359d45db8c2f8513e4f5a2f3fafaf0b7cefe3a8d5ec3304` |
| M29 | `TelemetryUnitTests.test_T5e_keyboard_interrupt_propagates` | 1 / 0 | `806a9b4d417261945359d45db8c2f8513e4f5a2f3fafaf0b7cefe3a8d5ec3304` |
| M30 | `TelemetryUnitTests.test_T9_write_volume_no_requirement_lines` | 1 / 0 | `806a9b4d417261945359d45db8c2f8513e4f5a2f3fafaf0b7cefe3a8d5ec3304` |
| M31 | `TelemetryUnitTests.test_T4_public_methods_avoid_science_clocks_and_gates` | 1 / 0 | `806a9b4d417261945359d45db8c2f8513e4f5a2f3fafaf0b7cefe3a8d5ec3304` |

M14 changes COMPLETE to 399 in both measurement construction and its schema band; M20 removes raw length/statistics/status/batch-summary consistency checks; M25 removes the combined projection/scope ceiling check; M28 puts norm/head in `enable_grad`; M29 changes all telemetry public Exception boundaries to BaseException; M30 emits one target-probability line per requirement. The target assertions caught each behavior. No survivor was disguised by an import error, invalid test name or Python syntax error: mutated ASTs were parsed before execution and loaded test names were validated.

## 7. Engine and harness verification

Read-only command: `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python -B /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/engine_fingerprint.py`, exit 0:

```text
engine fingerprint PASS: /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/memit_dry_run/memit/memit/memit_main.py
  sha256   d941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65  (expected d941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65; pod-era 5c0c706a…)
  _cov_cpu 3  (expected 3)
```

`git -C /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a diff --quiet -- memit_dry_run experiments/track_c/c10e_bandknob.py` → **exit 0**. Engine and c10e hashes match before. The separate FROZEN C10W evaluator drift is reported in §1; this quiet check does not cover that evaluator.

## 8. Open issues, interpretations and limits

- **Scope gate NOT-CLEAN:** FROZEN `experiments/track_c/c10w_oracle_eval.py` changed SHA, and outside-list porcelain differences in §1 prevent a blanket whole-workspace exclusivity claim. No build write targeted those files; ownership/process attribution is UNVERIFIABLE from these observations. The changed evaluator cannot be reverted under this task’s read-only boundary. Other frozen hashes and the prereg match; C10V results are unchanged, while C10W has five observed added quarantine files listed in §1.
- The report’s own final digest is external, by necessity, in the terminal after/write-list-sha256.txt snapshot; seven code/wrapper digests are embedded above.
- The pre-existing stage3 absent-ceiling gate remains unreachable under the new reader provenance check, as required by brief §2F; no surrounding gate/order was removed.
- `inputs.target_lengths` records the 24 raw lengths needed to verify the complete greedy schedule `3*(37*Σ[T(T−1)/2]+84)` and lens count `2*36`; aggregate prefix counts alone cannot recover the squared-length sum. This is schema evidence, not a scheduling option.
- The target-probability private CPU fp32 chunk is centered before logsumexp/exp, mathematically the same probability with better offset stability. Its copy stays ≤64 MiB; T6/T7 prove inputs unchanged and dense-float64 agreement ≤1e-6. Actual MPS allocation/resource behavior is not claimed.
- INVALID partial benchmark diagnostics record the actual completed warmup count 0–20; usable COMPLETE/CAPPED still requires exactly 20. Supervisor freshness is a read-only presence snapshot after first clock, before spawn; full path admission runs after kill/reap before cap writes, so no preflight delays spawning.
- Arbitrary-precision positive go integers remain legal strict finite JSON numbers; mismatched selection is rejected by the ordered V12 comparison. C01 budgets/readers reject outside-range integers before float finiteness conversion; unrepresentable timing values yield ValueError.
- Three static benchmark fixes were briefly applied before their new tests; they were fully reverted, regression tests added and RED recorded, then fixes reapplied. The initial idle vii/T3 observation-layer corrections and T7 production numerical correction are disclosed in §3.
- Out-of-family review was not authenticated; fresh same-family review supplies weaker independence and is labelled accordingly. All live GPU/scientific performance, write qualification, telemetry MPS inertness and F1 readiness remain UNVERIFIED. No other known implementation defect is deferred.

## 9. Commands supplied to the program — NOT RUN

Only the program may dispatch these after the separate operator ruling. `<UTC>`, `<C2>` and `<C3>` are selections from a usable fresh benchmark, not the synthetic fixture. The inertness check has its separate §9.1(h′3) operator GPU-cost gate.

Benchmark, spec v2 §3:

```sh
LLMDB_ROOT=/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python -B /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_benchmark.py --out /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/c10z_astra_benchmark/<UTC>
```

Optional telemetry inertness check:

```sh
LLMDB_ROOT=/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python -B /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_telemetry_check.py --out /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/c10z_astra_telemetry_inertness/<UTC>
```

Prereg §9.1(j′) launch lines, preserved verbatim from `docs/C10Z_ASTRA_PREREG.md:609–610`; `W` denotes the absolute worktree above. Telemetry is explicitly removed for the first attempt:

```sh
W=/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a
nohup caffeinate -i env -u C10Z_TELEMETRY -u C10Z_TELEMETRY_INERTNESS LLMDB_ROOT="$W" C10Z_OUT_DIR="$W/results/c10z_astra" C10Z_GO_RECORD="$W/results/c10z_astra_go_record.json" C10Z_BENCHMARK_RECORD="$W/results/c10z_astra_benchmark/<UTC>/benchmark.json" C10Z_STAGE2_CEILING_S=<C2> C10Z_STAGE3_CEILING_S=<C3> "$W/tools/run_c10z_attempt.sh" > "$W/results/c10z_astra_chain.log" 2>&1 &
nohup caffeinate -i env -u C10Z_TELEMETRY -u C10Z_TELEMETRY_INERTNESS LLMDB_ROOT="$W" C10Z_OUT_DIR="$W/results/c10z_astra" C10Z_GO_RECORD="$W/results/c10z_astra_go_record.json" C10Z_BENCHMARK_RECORD="$W/results/c10z_astra_benchmark/<UTC>/benchmark.json" C10Z_STAGE2_CEILING_S=<C2> C10Z_STAGE3_CEILING_S=<C3> bash -c '"$1" 3; rc=$?; echo "STAGE_3_EXIT=$rc"; exit "$rc"' _ "$W/tools/run_c10z_stage.sh" > "$W/results/c10z_astra_stage3.log" 2>&1 &
```

First command is process1; the second is stage3 only when the stage2 reading has next_stage exactly integer 3. Both need a valid selected go record and a fresh permitted output namespace; none was dispatched by this build.

Completion evidence is retained exclusively under `/private/tmp/c10z_build/`; the report is the only report artifact in W. No tracker, frozen prereg, engine, frozen c10e harness or memory/context ledger was written. The fresh read-only same-family reviewer inspected all nine evidence sections, the complete suites, all 31 mutation records/logs, and direct scope comparisons; source/CPU evidence PROCEED, overall scope gate NOT-CLEAN with UNVERIFIABLE attribution.

## 10. Astra advisories

**PASS — all three advisories implemented, CPU-only.** Final suites: **173/173 ASTRA**, **47/47 benchmark**, both exit 0. All four new tests passed against unchanged production at their first execution and in the final full suites. **No new test failed against current production; no production fix was made.** The previous 171/45 counts in sections 1–9 are historical build evidence.

Execution admission: the program sent GPU-LIVE after the initial targeted tests. No further Python was started during that pause. The program then explicitly authorized **PYTHON-OK (not GPU-CLEAR)** because P2 had passed its only gated stage, and directed this CPU pass to finish. All resumed Python ran serially with the worktree venv, `-B`, `TMPDIR=/private/tmp/c10z_build` and CPU thread limits. No model load, MPS/GPU work, live benchmark, live inertness check, ASTRA stage, or real-tree wrapper ran. Only the two authorized selftest files, this report and scratch were written.

| Advisory | New test and source | GREEN evidence |
|---|---|---|
| Synthetic MPS identity | `BenchmarkLifecycleTests.test_injected_worker_synthetic_mps_identity_validates_derived`, `experiments/track_c/c10z_astra_benchmark_selftest.py:772` | First run: 1 test, OK, 0.095 s (`mps-green.log`); final full suite: 47/47 |
| Full-worker SVD TIMEOUT | `BenchmarkLifecycleTests.test_worker_svd_timeout_preserves_complete_and_capped`, `experiments/track_c/c10z_astra_benchmark_selftest.py:694` | First run: 1 test, OK, 0.187 s (`timeout-green.log`); final full suite: 47/47 |
| Failures during write execution | `TelemetryIntegrationTests.test_write_telemetry_failures_preserve_science`, `experiments/track_c/c10z_astra_selftest.py:2355` | First telemetry run: both new methods OK, 27.267 s (`telemetry-green.log`); final full suite: 173/173 |
| Failures during resident execution | `TelemetryIntegrationTests.test_resident_telemetry_failures_preserve_science`, `experiments/track_c/c10z_astra_selftest.py:2426` | Same first telemetry run; final full suite: 173/173 |

All log names in this section resolve under `/private/tmp/c10z_build/advisories/`. Before the additions, the four existing worker/helper and telemetry integration tests passed in 3.787 s (`baseline.log`). The numbered acceptance list was saved in `test-plan.md` before editing the tests.

The synthetic identity test retains the CPU worker's REFUSED record byte-for-byte, changes only an in-memory copy's device metadata to `mps`, validates it, and requires both `derived == ceilings(record)` and source BENCHMARK. Actual model parameters remain CPU; the synthetic record is never published. This is schema/derivation coverage, not MPS evidence.

The TIMEOUT test executes the full CPU worker and real SVD timeout helper with a stdlib sleeping stand-in instead of an SVD workload. It checks exit 0, a reaped child, TIMEOUT and a positive lower bound, unchanged weights, no error record, and preserved COMPLETE/CAPPED probe and top statuses. The CAPPED branch uses a test-controlled partial measurement from 200 of the measured forwards; it is not a natural timing-cap observation.

The telemetry tests run actual `Session.write_arm`, `arm_hook`, `record` and resident code with CPU collaborators. They compare scientific file bytes, write outputs, records/readings and science call counts against telemetry-off and successful telemetry. Failures affect only the telemetry sink: mkdir/open at construction, and write/flush/fsync during phase, norms, probabilities and lens emission. Every injection must fire exactly once and emit one disable marker. Resident cases additionally require exit 0, completed stage 1, closed state, no HALT, and the same stage/close events. Existing on/off tests retain their positive-control checks.

RED evidence is **expected sensitivity failure under explicitly controlled wrong in-memory doubles**, followed by GREEN on unchanged production. These are not production-file mutations or failed production tests. Each corrected control ran one test, produced one assertion failure and zero errors; exact tracebacks are in the named `.log` and `.json` files.

| Control | Deliberately wrong double | Assertion caught at | Evidence |
|---|---|---|---|
| `R1-synthetic-source` | Synthetic identity REFUSED instead of BENCHMARK | `benchmark_selftest.py:787` | `R1-synthetic-source.log`, `R1-synthetic-source.json` |
| `R2-derived-equality` | Second derivation changes C2 by 300 | `benchmark_selftest.py:786` | `R2-derived-equality.log`, `R2-derived-equality.json` |
| `R3-timeout-status` | SVD TIMEOUT wrongly changes top status to INVALID | `benchmark_selftest.py:720` | `R3-timeout-status.log`, `R3-timeout-status.json` |
| `R4-write-output` | Test double corrupts temporary science.json after a handled fault | `astra_selftest.py:2420` | `R4-write-output.log`, `R4-write-output.json` |
| `R5-resident-output` | Test double changes completed stage from 1 to 2 | `astra_selftest.py:2454` | `R5-resident-output.log`, `R5-resident-output.json` |

`sensitivity.log` ends `ADVISORY_SENSITIVITY_PASS controls=5 source_files_unchanged=true` (exit 0). An initial R2 double fired while an incomplete record still had MPS metadata and exercised the worker exit check rather than derivation equality; that attempt is excluded from the R2 evidence above and preserved in `sensitivity-initial/`. The initial R4 control was interrupted while handling a large mismatch; the scratch runner was changed to use the same strict tuple equality with concise diagnostics. No test-file or production change was made for either control adjustment. The corrected R2 trace catches the derived-equality assertion, and corrected R4 catches the scientific-output comparison.

Final full-suite commands, run sequentially after PYTHON-OK:

```sh
/opt/homebrew/bin/rtk proxy /usr/bin/env TMPDIR=/private/tmp/c10z_build LLMDB_ROOT=/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python -B /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py > /private/tmp/c10z_build/advisories/astra-final.log 2>&1
/opt/homebrew/bin/rtk proxy /usr/bin/env TMPDIR=/private/tmp/c10z_build LLMDB_ROOT=/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python -B /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_benchmark_selftest.py > /private/tmp/c10z_build/advisories/bench-final.log 2>&1
```

Verbatim suite endings:

`astra-final.log` (exit 0):

```text
----------------------------------------------------------------------
Ran 173 tests in 156.768s

OK
C10Z_ASTRA_SELFTEST_PASS tests=173
```

`bench-final.log` (exit 0):

```text
----------------------------------------------------------------------
Ran 47 tests in 3.691s

OK
C10Z_BENCH_SELFTEST_PASS tests=47
```

Advisory-pass SHA-256s:

| Test path | Before | After |
|---|---|---|
| `experiments/track_c/c10z_astra_selftest.py` | `144141db1cb1c888d7e56fb8a80530d7a039719703f58bb998b9c7acc2c5d4d9` | `b99e5e00fafddb0d05d2f5642daa4408fe616220462d7139cad550cdfdc3996c` |
| `experiments/track_c/c10z_astra_benchmark_selftest.py` | `751b0e05703de12634d7d32331b158ca53027e5bce9d87c9df75529756567249` | `1f9cdb5f7200e91a9157b2dda29e836e524554097c80f0913d5ccbaa6bfb9f4a` |

All **24 protected source/input SHA-256s are unchanged**, including the production C10Z files, both wrappers, engine/c10e and prereg. The original report sections 1–9 are byte-identical to the saved before copy. Before/after data and this report's external final SHA are retained in `before.json` / `after.json`; detailed observations are in `scope-comparison.json`.

`results/c10v_layerpick` listing: 7 → 7 files; 0 added, 0 removed. Unchanged. 

`results/c10w_oracle` listing: 62 → 69 files; 10 added, 3 removed. The exact added/removed paths are in `scope-comparison.json`. 

The shared workspace also has unrelated porcelain status additions/removals recorded verbatim in that comparison. These observations have **UNVERIFIABLE attribution**; no exclusive whole-workspace cleanliness is claimed. The advisory tool writes remained within the two test files, this report and scratch. Scientific performance, live MPS inertness and ASTRA qualification remain **UNVERIFIED**.

## 11. Direct script execute permissions

**PASS — one test added, test file only.** `WrapperTests.test_direct_scripts_executable_on_disk_and_git_index` (`experiments/track_c/c10z_astra_selftest.py:2341`) inspects the actual attempt wrapper and discovers its repository shell-script references. Currently the direct script is `tools/run_c10z_stage.sh`, invoked through `$S`; the venv Python is an interpreter, not an indexed repository script. Discovery must be nonempty. For every script the test requires `os.access(path, os.X_OK)` and exactly one stage-0 git index entry with mode **100755**, from read-only `git ls-files -s -z`. It does not rely on the manufactured permissions of temporary script copies.

The program reported the first process-1 launch exited 126 because the stage wrapper was mode 644. Read-only `git show --stat --summary 0d25ed7 -- tools/run_c10z_stage.sh` confirms the existing fix is solely mode **100644 → 100755** with zero content changes. Both wrappers are currently mode 755 on disk and 100755 in the index. This task made no production content, chmod or git index change.

GREEN: the complete `WrapperTests` group, including the new test, passed **4/4**, exit 0, in **1.552 s** (`/private/tmp/c10z_build/execute-bit/green.log`):

```text
test_direct_scripts_executable_on_disk_and_git_index ... ok
test_next_stage_types ... ok
test_relative_out ... ok
test_stage0_failure ... ok
Ran 4 tests in 1.552s
OK
C10Z_WRAPPER_SELFTEST_PASS tests=4
```

RED sensitivity controls used in-memory mocks, without changing the real files or index:

| Control | Expected assertion failure | Evidence |
|---|---|---|
| Disk `os.access(X_OK)` returns false for the stage script | `tools/run_c10z_stage.sh is not executable on disk` | `execute-bit/red-disk.log` |
| Git output reports mode 100644 | `tools/run_c10z_stage.sh must have one git index entry with mode 100755` | `execute-bit/red-index.log` |

Each control produced one failure and zero errors. After mock restoration, the new test passed again. `execute-bit/sensitivity.log` ends `EXECUTE_BIT_SENSITIVITY_PASS expected_RED=2 restored_GREEN=1 imports=stdlib_only`; exact traces are also in `execute-bit/red.json`. These expected mock failures are not production-test failures.

The program explicitly allowed light, serial Python while ASTRA's GPU job was live. Verification used the worktree venv with `-B`, `TMPDIR=/private/tmp/c10z_build` and CPU thread limits. The selected tests imported neither torch nor c10e/transformers/datasets; no model load, GPU/MPS work or real-tree launch ran. The broad scientific suites were not rerun for this file/index permission check; their preceding evidence remains in section 10.

Only `experiments/track_c/c10z_astra_selftest.py` and this section of the report changed; scratch is under `/private/tmp/c10z_build/execute-bit/`. All ten protected files' content hashes and disk modes, including production C10Z files, both wrappers, engine/c10e and prereg, match the before snapshot. Both wrappers' index entries are unchanged. Report sections 1–10 remain byte-identical to the saved before copy.

Selftest SHA-256: `b99e5e00fafddb0d05d2f5642daa4408fe616220462d7139cad550cdfdc3996c` → `8ac35c1e8bd71c79fc99f16bc52ee613438df2a017e047723225838bf4fe08ee`. Scope evidence: `execute-bit/before.json` and `execute-bit/after.json`; the report's final SHA is in the latter, outside the report itself.

## 12. V4 template pin (D-C10z-v4fix)

**PASS — test-first implementation and both full CPU suites GREEN.** Implemented the program's 2026-10-08 ruling, diagnostic addendum and **prereg §10 Amendment V4T** in `experiments/track_c/c10z_astra_arms.py` and its selftest. The newly authorized reader change is its prereg SHA constant only. §10 was read in full; `results/templatepin_amend_astra.md` and its final GO recheck `results/templatepin_amend_astra_delta.md` were read. GO covers amendment text, not live runtime evidence. The diagnosis at `results/c10z_astra_v4_diagnosis.md` was read. This changes the context provenance; it preserves the V4 envelope: A7 full [5,18], canonical [5,10], first [42,59], and A1/A2 full ≥68, all inclusive. No empirical claim about the pinned-template baseline or ASTRA performance follows from these CPU tests.

Process 1 imports `TEMPLATES` from the unchanged benchmark module; no strings are retyped. It installs the engine's original two-group cache shape, identity plus five prefixes, before the first recipe-A edit. Admission requires exact equality between the imported flat list and the selected record's `inputs.templates`, plus equality of its canonical digest with `inputs.templates_sha256`; disagreement refuses **HALTED-V12** before attempt creation or worker launch. The binding carries the selected list and digest into the resident. Before recipe A the resident independently checks all three §10(b) identities: the scorer convention `sha256(json.dumps(engine_form)).hexdigest()[:12] == "c7dabbe7c25a"`, exact flattened-list equality and canonical-digest equality. A miss refuses V12 before writing the template artifact or editing. Process 2 retains the existing input-file load and uses that cached object; it does not replace it with a newly sampled or copied constant.

Both processes now create `context_templates.json` and publish its provenance in `run.json` before recipe A and LAW#3. `run.context_templates` contains the actual file `sha256`, the benchmark canonical `inputs_sha256`, source **`benchmark TEMPLATES / C10Q c7dabbe7c25a`**, `scorer_identity: "c7dabbe7c25a"`, `seed: 0` and `sampling: false`. The original `torch.manual_seed(0)` remains before harness import, and manifest seed 0 is unchanged. Pinned context templates consume no RNG draws. New-writer batch construction, observations, probes and instrument preparation still wait for LAW#3.

A V4 miss retains the template file and provenance through the resident's final publication. The baseline-only `pass_p{n}.json`, `halt_p{n}.json` and architecture diagnostic include `context_templates_sha256`. Architecture diagnostics now use **`architecture_profile/c10z_astra_halt_diagnostic_<UTC>.json`**, with UTC format `YYYYMMDDTHHMMSS.ffffffZ` and create-only `write_json` / exclusive `open("x")`. The historical fixed-path file is untouched; a filename collision refuses instead of replacing the earlier record. This follows the explicit program addendum and latest instruction; §10(d3) describes the earlier fixed-path overwrite behavior.

All evidence below is under **`/private/tmp/c10z_build/v4-template-pin/`**. RED ran the nine new `TemplatePinTests` plus the new admission test against the original driver SHA `806a9b4d417261945359d45db8c2f8513e4f5a2f3fafaf0b7cefe3a8d5ec3304`, before production edits: **10 tests, 8 expected failures, 0 errors**, exit 1, 0.519 s (`red.log`, exact traces in `red.json`).

| New test | Original-driver RED observation | Final GREEN |
|---|---|---|
| `LaunchBindingTests.test_benchmark_template_digest_mismatch_refuses_before_launch` | `AssertionError: Halt not raised` for a valid but different recorded template set | PASS; V12 before launch/output mutation |
| `TemplatePinTests.test_cache_pinned_before_recipe_A_without_sampling` | `AssertionError: generate_fast sampled before the template pin` | PASS; cache is pinned and sampling mock is never called |
| `TemplatePinTests.test_templates_byte_equal_to_benchmark` | `V4 halt omitted context_templates.json` | PASS; grouped JSON bytes and canonical flattened template bytes match values derived from imported `TEMPLATES` |
| `TemplatePinTests.test_templates_and_run_hash_written_before_LAW3_gate` | `templates were not frozen before LAW#3` | PASS; file/hash/source/seed present at gate entry |
| `TemplatePinTests.test_V4_resident_retains_templates_and_halt_hashes` | `resident V4 halt omitted templates` | PASS; real resident publication and V4 diagnostic retain all hashes |
| `TemplatePinTests.test_process2_reuses_loaded_cache_before_baseline` | `process-2 V4 halt omitted its loaded templates` | PASS; loaded cache object retained and never sampled |
| `TemplatePinTests.test_existing_context_artifact_refusal_unchanged` | PASS control | PASS; existing bytes preserved, V12 refusal |
| `TemplatePinTests.test_manual_seed_zero_kept_before_harness_import` | PASS control | PASS; unchanged process-start seed order |
| `TemplatePinTests.test_UTC_diagnostics_preserve_historical_records` | `historical fixed-path diagnostic was overwritten` | PASS; two distinct UTC records, earlier bytes preserved |
| `TemplatePinTests.test_UTC_diagnostic_collision_refuses_exclusive_creation` | `AssertionError: Halt not raised` | PASS; collision refuses and earlier record remains intact |

The engine-cache test compiles only the actual `get_context_templates` function into an isolated module and supplies a failing `generate_fast` mock. It exercises the engine's real cache branch without importing the engine, loading a model/tokenizer or generating text. The V4 resident test executes the actual stage-0 and resident/diagnostic/publication paths with CPU stubs and a scratch `ROOT`. It checks an A7 first count of 40 still yields V4 and leaves a recipe-A-only pass record.

The first implementation check (`green.log`) had **2 errors** from a newly introduced datetime import collision: `AttributeError: module 'datetime' has no attribute 'now'`. This was corrected to use the driver's existing `datetime.datetime` module API; no scientific path or gate was changed for that correction. The expanded regression group then passed **59/59**, zero failures/errors, exit 0 in **17.695 s** (`green-final.log`, `green-final.json`). It includes all ten new tests, the complete launch-binding and wrapper groups, the prior LAW#3 ordering test and diagnostic/watchdog preservation tests. `WrapperTests.test_direct_scripts_executable_on_disk_and_git_index` remained GREEN.

The program appended §10 during the final scope check. That check detected the prereg drift and stopped before issuing DONE; it did not write an `after.json` or alter the prereg. The published SHA was directly verified as **`7c6e52e274e3dbc30cd5123d6b56ae8c9b1dca8c5e7507ff7be15d57e845059d`**. The reader's `PREREG_SHA` and the selftest's `PREREG` were updated; the driver consumes `R.PREREG_SHA` and needs no second literal pin. Replacing the reader's new hash with the original one exactly reproduces its before-snapshot SHA, confirming that its gates and other bytes are unchanged.

Additional §10 RED/GREEN evidence:

| Test | RED before §10 alignment | Final GREEN |
|---|---|---|
| `TemplatePinTests.test_scorer_template_identity_mismatch_refuses_before_recipe_A` | A self-consistent alternate set reached V4 instead of refusing the C10Q identity mismatch | PASS; V12 and zero recipe/edit calls |
| `TemplatePinTests.test_selected_template_list_mismatch_refuses_before_recipe_A` | A different selected list reached V4 instead of refusing exact-list mismatch | PASS; V12 and zero recipe/edit calls |
| `PinTests.test_amended_prereg_pin_shared_by_driver_reader_and_tests` | Reader retained `87fe3d5d…` while the actual amended file was `7c6e52e2…` | PASS; file, reader, driver and tests agree |
| `WrapperTests.test_attempt2_out_and_logs_preserve_attempt1` | PASS control; explicit namespaces already supported | PASS; stages 0/1/2/3 see the new output/go/benchmark paths and earlier run/log bytes remain intact |

`amendment-red.log` / `amendment-red.json`: **4 tests, 3 expected failures, 0 errors**, exit 1, **0.559 s**, before alignment edits (driver SHA `c675b136…`). `amendment-green.log` / `amendment-green.json`: **64/64**, zero failures/errors, exit 0, **19.325 s**, after alignment. Both source identities and the amended prereg hash are captured there. The four additional tests bring the full suite from 184 to **188**. The preceding full-suite evidence at `full-astra.log` (184/184) and `full-benchmark.log` (47/47) is retained as pre-amendment history; the final evidence below was rerun after every source/pin change.

**Attempt-2 namespace (§10(d2)).** The existing launch wrappers already honor explicit `C10Z_OUT_DIR`; their production files remain unchanged. Use both amended launch lines with `C10Z_OUT_DIR="$W/results/c10z_astra_attempt2"`, a new go-record file and the new benchmark-record path. Process 1's outer log is **`$W/results/c10z_astra_attempt2_chain.log`**; stage 3's is **`$W/results/c10z_astra_attempt2_stage3.log`**. Per-process resident logs remain under that fresh OUT_DIR. The wrapper regression uses the actual attempt-script text and scratch stage stubs, exercises the complete 0/1/2 chain plus the stated stage-3 shell line, checks propagated paths and both new log names, and preserves manufactured attempt-1 records/logs byte-for-byte. No attempt-2 launch, directory or outer log was created in the real tree.

Both full suites subsequently ran **serially** with worktree venv Python `-B`, `TMPDIR=/private/tmp/c10z_build`, a fresh scratch `PYTHONPYCACHEPREFIX`, `LLMDB_ROOT` set to the worktree and CPU thread limits of 1. Neither suite loaded c10e/transformers/datasets, a scientific model or the GPU. Exact final output:

```text
# full-astra-amended.log — exit 0
----------------------------------------------------------------------
Ran 188 tests in 114.493s

OK
C10Z_ASTRA_SELFTEST_PASS tests=188

# full-benchmark-amended.log — exit 0
----------------------------------------------------------------------
Ran 47 tests in 2.756s

OK
C10Z_BENCH_SELFTEST_PASS tests=47
```

Final source SHA-256s:

| File | SHA-256 |
|---|---|
| `experiments/track_c/c10z_astra_arms.py` | **`ab6f5c809d8187f4e5eb39e9cc6fbf40b6e357b2ecf5b18ecc887e05de7adebc`** |
| `experiments/track_c/c10z_astra_selftest.py` | `15ccb1884d9bc7fd179f8654de3dd2c80d27d0653e1bdf6fa691d0a20a538f2b` |
| `experiments/track_c/c10z_astra_read.py` — prereg pin only | `5549eb23e8ecfe8dc7b1eb7aaa60a361180762d2118a151d2006d5d85ccc86d5` |

**Scope and provenance.** The 31 remaining protected files' contents and disk modes match `before.json`: engine/MEMIT/util/ROME source, c10e, benchmark and benchmark selftest, telemetry check, hparams, fingerprint tool, both wrappers and diagnosis. Our writes are limited to arms, selftest, the authorized one-line reader pin and this report; the program-owned prereg changed by its published §10 amendment. No other before-snapshot file changed. Both wrappers remain executable on disk and indexed as 100755. The historical `architecture_profile/c10z_astra_halt_diagnostic.json` retains SHA `3dce715148f3b3fcc1883b007d4d71883bb84bbd2a3392a1c6d374c8e3c73e6b`; no real-tree architecture diagnostic was created. No live result record was written. Report sections 1–11 remain byte-identical to `report.before.md`. Final comparison data is in `scope-amended-before-report.json`; `after.json` records the report's external final SHA. The initial section-12 draft is retained as `report.pre-amendment.md`.

The actual go-selected benchmark is `results/c10z_astra_benchmark/20261008T104535Z/benchmark.json`, SHA `a33075393066e6332fbe64b9641caa57e7005fb89c6f8849fb212f5940ccff4a`. Its template source is `results/c10q_stacked/logs_run.log:9`; its `inputs.templates_sha256` **`d6c7c70026dced37bddc6adf316a3487d70227dae80a6e0ed5cdabe50caedfa0`** was directly checked against the imported constant. Its recorded driver identity predates this patch. A read-only call to the real admission helper now correctly refuses that historical selection: **`HALTED-V12: benchmark source identity changed: experiments/track_c/c10z_astra_arms.py`** (`historical-benchmark-refusal-amended.json`). Per §10(d1), final driver review precedes the program's single drift-forced benchmark rerun in a fresh directory, a new go-record file and the attempt-2 launch. The old go record, benchmark and halted results remain data and are never overwritten or promoted. We did not run the benchmark or any GPU job.

The amended prereg, reader, driver and selftest pins all agree on SHA **`7c6e52e274e3dbc30cd5123d6b56ae8c9b1dca8c5e7507ff7be15d57e845059d`**. This is a post-V4, pre-candidate input amendment: it changes both comparator and candidate inputs. Results will be conditional on this fixed set; the original unrecorded seed-0 context attribution remains inferred, and no freedom from selection bias is claimed. A future pinned-set V4 miss remains a final HALT under §10(d4), with no further template change or gate relaxation. No GPU attempt, new live LAW#3 count, scientific ASTRA outcome or live launch admission was claimed.

## 13. Z0 halt probe

**PASS — test-first diagnostic implementation; full CPU suites GREEN (198 / 47). The MPS probe has NOT RUN.** Added `experiments/track_c/c10z_astra_z0_probe.py` and nine tiny CPU tests in the existing selftest. The separately authorized driver change is exactly two lines in `Session.z0`: on the existing `sigma > .125` failure path, save `checks.Z0 = {ok: false, sigma_shape: sigma, original_full_sequence_sigma: full_sigma}` before the unchanged V5 `require`. The threshold, calculations, passing return, reader and science path are unchanged. This driver metadata change is ready for the program's Astra review; no new Astra approval is claimed.

Read-only inspection of the actual attempt-2 records confirmed the template file SHA equals `run.json.context_templates.sha256`: **`9472b663a34cfd9c0bb5448087ae0c2c333b1988b70f211fb2d90baaf8b560b7`**. Its pristine parameter hash is **`87cb5c38789af8ba230c28b88bef28436bd9706fb0fe076a0500101eeb938acd`**. Its V5 halt has no `checks.Z0`; the original measured spread therefore remains **UNVERIFIABLE** from that halt. The operator reports LAW#3 A7 12/52/8 and A1/A2 70/71. These are prior-run observations, not measurements from this build or its CPU tests.

The probe checks the input file SHA before any model import, flattens the saved grouped templates through the driver's own `Session.flatten_templates`, and loads the same harness/model lazily, with seed 0, Qwen2.5-3B revision `3aab1f1954e9cc14eb9509a215f9e5ca08227a9b`, **MPS fp16**, the frozen architecture and tied embedding. Its parameter hash must equal attempt 2's pristine hash before forwards. It bypasses `Session.__init__` because that constructor publishes records and installs edit wrappers. It calls no edit, recipe, write-column, restore, generation or template sampler. Telemetry is off. CPU tests never import the actual harness, transformers or datasets, and a separate fresh import guard also verified that importing the probe loads neither torch nor the scientific runtime.

For A7, the probe calls the actual `Session.make_batch` and `Session._observe(..., carriers=None, full=True, trace_layers=None)` used by the driver's Z0 observation: all six views, 144 rows with the real 24-fact population. It retains only view-0 diagnostic rows. Every `(fact i, target position q)` records four leads, all using the driver's `margin_leads`:

- **Native**: single unpadded prefix `prompt + target[:q]`, final logits, exactly as `z0()`.
- **Batch**: the original observation's gathered lead.
- **Full**: single unpadded full teacher-forced sequence `prompt + target[:-1]` at `len(prompt) + q - 1`, exactly as the driver's full-sequence reference.
- **Batch1**: the same observation method on the single identity row, with its **original global padded width, token IDs, mask and requirement indices preserved**, and only the row index changed to zero. This holds width/mask constant while changing the batch dimension.

The record includes signed and absolute per-position differences; max, median and p95 of **|native-batch|, |native-batch1| and |native-full|**, calculated by subtracting CPU float64 values and using linear quantile interpolation; the worst ten positions ranked by |native-batch|, with decoded token windows and IDs; actual batch shape; timings for loading, hashing, batch, batch1, prefix and full forwards; and before/after parameter and buffer hashes. The built batch is right padded independently of `tok.padding_side`, so both are reported. A temporary rotary pre-hook captures the **actual position_ids passed to the model**, including their broadcast shape, for batch, batch1, native and full forwards. Each row includes those IDs, the exact batch mask, its sum and the scored position's ID. Native/full calls pass no attention-mask argument, matching Z0; their implicit all-token mask sums are recorded. Hooks are removed and the original hook registry checked after every capture.

**Metric distinction:** the driver's `full_sigma` is **max |full-batch|**, not max |native-full|. The JSON separately records `z0_sigma_shape`, `z0_full_sigma` and the full-batch summary, in addition to the three requested native-reference summaries. A shape-sensitive CPU positive control proves that these distinct quantities and all four leads are labelled correctly. The probe refuses any detected parameter/buffer change without restoring or repairing it.

The output argument must be absolute, have exactly the parent `results/c10z_astra_z0_probe/`, and use a valid UTC name `YYYYMMDDTHHMMSS[.ffffff]Z`. Relative, escaped, symlinked or existing paths refuse before model loading. The timestamp directory is claimed exclusively; `probe.json` uses the driver's create-only JSON writer. No prior attempt, diagnostic or result is replaced. An interrupted/refused run's claimed directory remains a record; a later launch needs a fresh UTC path.

**Operator launch command — provided, not executed.** This uses the actual worktree venv and probe CLI. The program chooses when to launch it. It creates only the fresh diagnostic namespace; no stage/recipe driver is launched.

```bash
C10Z_PROBE_ROOT='/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a'
C10Z_PROBE_OUT="$C10Z_PROBE_ROOT/results/c10z_astra_z0_probe/$(/bin/date -u +%Y%m%dT%H%M%SZ)"
/usr/bin/env -u C10_PROJECTOR -u N_EDIT -u C10_SUBJECT_OFFSET \
  -u C10_CTX_TEMPLATES -u C10_ARMS -u C10_KEY_LOCUS -u C10_RECIPES \
  LLMDB_ROOT="$C10Z_PROBE_ROOT" LLMDB_DEVICE=mps C10Z_TELEMETRY=0 \
  MODEL_ID=Qwen/Qwen2.5-3B MODEL_REV=3aab1f1954e9cc14eb9509a215f9e5ca08227a9b \
  PYTHONPYCACHEPREFIX="/private/tmp/c10z_build/z0-probe-bytecode/${C10Z_PROBE_OUT##*/}" \
  OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  "$C10Z_PROBE_ROOT/.venv/bin/python" -B \
  "$C10Z_PROBE_ROOT/experiments/track_c/c10z_astra_z0_probe.py" "$C10Z_PROBE_OUT"
```

Output: **`$C10Z_PROBE_OUT/probe.json`**. No output under the real probe namespace was created by this build. `--help` ran successfully without model loading. The recorded source identities distinguish the new metadata-only driver from the driver used in attempt 2; no future scientific launch admission or benchmark rerun is claimed.

All build evidence is under **`/private/tmp/c10z_build/z0-halt-probe/`**. Tests were written before the new probe and before the driver edit. Initial **RED** ran eight tests against the original driver SHA `ab6f5c809d8187f4e5eb39e9cc6fbf40b6e357b2ecf5b18ecc887e05de7adebc`: exit 1, **8 expected assertion failures, 0 errors**, 1.311 s (`red.txt`). The driver test failed at `self.assertIn("Z0", s.checks, ...)` with **`'Z0' not found in {} : V5 raises before saving its measured Z0 sigmas`**. The seven initial probe tests failed with **`diagnostic probe is not implemented`**. Initial GREEN was 9/9, including the existing frozen-boundary test (`green.txt`). Two additional positive controls exercised nonzero shape differences and the complete CPU JSON pipeline; final targeted **GREEN 11/11**, zero failures/errors, exit 0, 1.195 s (`green-final.txt`). No intermediate implementation failure occurred.

| Test | Final GREEN evidence |
|---|---|
| `Fix2Tests.test_z0_v5_halt_persists_native_and_full_sigma` | V5 detail unchanged; synthetic native sigma .25 and full sigma 1.25 saved before raising, then serialized by the actual diagnostic to both scratch halt records |
| `Fix2Tests.test_fix2_z0_sigma_halts_in_driver_at_frozen_boundary` | .125 still passes; larger sigma still HALTED-V5 |
| `Z0ProbeTests.test_probe_never_writes_weights_or_calls_edit_recipe_sampling` | All parameter/buffer bytes equal; forbidden edit/recipe/sampling spies untouched; hook registry restored |
| `Z0ProbeTests.test_probe_native_prefix_leads_equal_real_z0` | Every native lead and both maximum spreads exactly equal the actual driver Z0 result on fixed tiny CPU inputs |
| `Z0ProbeTests.test_probe_batch1_keeps_padding_and_captures_actual_position_ids` | Original padded width/mask retained; explicit right padding despite left tokenizer setting; captured rotary IDs deliberately start at 11, proving they were observed rather than inferred |
| `Z0ProbeTests.test_probe_diff_statistics_subtract_in_cpu_float64` | Difference of 16777216 and 16777217 retained; quantile inputs CPU float64; exact max/median/p95 oracle |
| `Z0ProbeTests.test_probe_wrong_template_sha_refuses_before_model_load` | Wrong input SHA refused; model loader never called; no output directory created |
| `Z0ProbeTests.test_probe_refuses_existing_or_escaped_output_before_model_load` | Existing, relative, wrong-namespace and non-UTC paths refused; sentinel record preserved; loader untouched |
| `Z0ProbeTests.test_probe_mutation_is_detected_without_restoring_weights` | Deliberately mutating CPU forward is detected and refuses; hooks removed; no repair/restore |
| `Z0ProbeTests.test_probe_distinct_shape_controls_and_full_sigma_match_z0` | Nonzero differences in all requested summaries; four leads and signed diffs agree; driver full-batch sigma distinguished from native-full |
| `Z0ProbeTests.test_probe_cpu_json_pipeline_roundtrip_and_exclusive_output` | Actual run/JSON publication with injected tiny CPU loader; strict round trip, correct input hash/provenance, telemetry off; second invocation refuses and prior bytes remain intact |

Both full suites ran **serially**, with worktree Python `-B`, `TMPDIR=/private/tmp/c10z_build`, separate fresh scratch bytecode prefixes and CPU thread limits of one. Exact final output:

```text
# astra-full.txt — exit 0
----------------------------------------------------------------------
Ran 198 tests in 118.007s

OK
C10Z_ASTRA_SELFTEST_PASS tests=198

# benchmark-full.txt — exit 0
----------------------------------------------------------------------
Ran 47 tests in 2.798s

OK
C10Z_BENCH_SELFTEST_PASS tests=47
```

`WrapperTests.test_direct_scripts_executable_on_disk_and_git_index` remains GREEN within the full suite. Both wrappers are also directly confirmed `os.access(X_OK)` and git index mode 100755. Syntax parsing, model-free import guard and `git diff --check` passed. CPU tests prove the plumbing on synthetic models only. **Actual MPS spreads, worst positions, causal explanation and any scientific remedy remain UNMEASURED / UNVERIFIED.** No scientific model or tokenizer, real harness, engine runtime, GPU/MPS job, benchmark or recipe was loaded/run by this build.

Diagnostic hypotheses remain open: fp16 batch-dimension arithmetic; padded-width/attention-mask/position handling; prefix-versus-full causal/index/margin effects. The batch1 and full controls make those comparisons observable without relaxing V5 or choosing an explanation. The work advances the Track C validity question before a science-path fix. Out-of-family advisor review was attempted per `.codex/skills/advisor-review/SKILL.md`, but the Claude auth probe returned `loggedIn: false, authMethod: none` (exit 1), and the wrapper refused **exit 3**, `FATAL: Claude CLI is not logged in` (`claude-design.txt`). The documented Codex fallback was also attempted and failed **exit 1**, `failed to initialize in-process app-server client: Operation not permitted (os error 1)` (`fallback-design.log`). There is **no independent-review signoff** from those failed invocations; program Astra review remains the intended review for the driver metadata change. The design packet is `design.md`.

Final source SHA-256s:

| File | SHA-256 |
|---|---|
| `experiments/track_c/c10z_astra_z0_probe.py` | **`9502c681a55095217496d8f5e2c6950fdc2f1fe3aebe34e1f015e87d18010799`** |
| `experiments/track_c/c10z_astra_arms.py` | **`bc8ad6aef5778edd9bca49afb71a82e5e076cd937aa00bcb43fc8758b8ddcd16`** |
| `experiments/track_c/c10z_astra_selftest.py` | `41ce04709f92c567da550269cb7efb7bd656c7270c90b8fb5458c405ee38fb20` |

Our repository writes are limited to the new probe, its existing selftest, the two-line driver metadata change and this appended report section. The **16 protected files** in `before.json` remain byte-identical, including reader, benchmark/selftest, harness, engine source, prereg, wrappers, all snapshotted attempt-2 files and existing architecture diagnostics. No real architecture diagnostic or runtime result was written. Sections 1–12 remain byte-identical to `report.before.md`; `scope-before-report.json` contains the comparison and `after.json` records the report's external final SHA. No git mutation or commit was performed. The AGENTS context-save handoff is saved under scratch `context-save/projects/thestoryportal-arhugula-persistent-memory/checkpoints/`; `context-path.txt` names the exact file. Canonical ledgers and memory files are unchanged.

**2026-10-08 program addendum — restored driver, bundled sigma test, native-mask control.** The program reverted the two-line sigma-recording change under **D-C10z-driftcap**. The current benchmark-bound driver remains the Astra-reviewed **`ab6f5c809d8187f4e5eb39e9cc6fbf40b6e357b2ecf5b18ecc887e05de7adebc`**, byte-identical to the pre-probe driver; this follow-up did not edit it. The initial section-13 driver SHA and 198-test evidence above describe the earlier build, before the program's revert.

Moved **`Fix2Tests.test_z0_v5_halt_persists_native_and_full_sigma`** out of the default selftest and into **`results/c10z_z0_sigma_record.patch`** as an added selftest hunk. The test body is preserved verbatim and is automatically collected with Fix2Tests when the patch is applied. The originally saved driver patch remains an exact byte prefix; no live patch application, source-identity change or benchmark rerun occurred. The existing `.125` boundary test and all probe tests remain in the current suite. The bundled test was first confirmed RED against the reverted driver (`red.txt`: 1 expected failure, 0 errors, exit 1, 1.288 s, `'Z0' not found in {}`). `git apply --check` succeeds against the current files. Applying the combined patch **only in a scratch copy**, then running the moved test and boundary test, passed **2/2**, exit 0, 1.067 s (`bundled-green.txt`). No real driver was patched by that check.

The program launched the original diagnostic externally. Read-only inspection of **`results/c10z_astra_z0_probe/20261008T132220Z/probe.json`**, SHA **`7a9abdc0abed2c2fdd1d97fc0e75cda6baecd465933dec0c74f1ef7f2365b65a`**, confirms 132 positions, native/full leads exactly equal everywhere, max |native-full| 0 and max |native-batch| **113108310.0078125**. All recorded native/full mask arguments are null. Native leads span [-113108312, 0]; batch leads span [-15.84765625, 4.046875], and batch1 [-15.85546875, 4.0390625]. This confirms the recorded disparity, **not its cause**. The program's mask-less MPS fp16 SDPA/causal-path hypothesis remains untested by this CPU build.

Added **`--native-mask {none,ones}`** to the existing probe, default **`none`**. `none` retains the current driver's mask-less native and full forwards. `ones` adds exactly **`attention_mask=torch.ones_like(input_ids)`** to those two forward types; batch and batch1 still use their existing observation code and masks. No driver, reader, engine, harness or benchmark change was made. Each output now records top-level **`native_mask`** and the actual **`model.config._attn_implementation`** as **`attn_implementation`**. Every position records **`native_max_abs_logit`**, the maximum absolute logit over that position's entire native-prefix forward, reduced after CPU float32 conversion, and **`native_logits_dtype`**, the raw forward dtype. `native_full_mask_argument` is null for `none` and `"ones"` for `ones`. This control and added observations do not change leads, difference statistics, thresholds or telemetry settings.

Three new CPU tests were written before the probe change:

| Test | RED → final GREEN |
|---|---|
| `Z0ProbeTests.test_probe_native_mask_option_changes_only_forward_kwargs` | Missing `native_mask` parameter → identical paired input IDs, dtype/device and other kwargs; exactly seven native/full calls gain an all-ones mask, while batch calls stay identical; hashes/spies unchanged |
| `Z0ProbeTests.test_probe_records_attention_backend_and_native_logit_bound` | Missing backend metadata → actual tiny-model backend and raw dtype recorded; every bound equals an independently calculated native-forward maximum |
| `Z0ProbeTests.test_probe_native_mask_cli_default_and_ones` | Default dispatch lacks mode and CLI rejects option → default dispatches `none`, explicit option dispatches `ones` |

`mask-red.txt`: **3 tests**, 3 expected assertion failures plus one expected CLI `SystemExit: 2` subtest error, exit 1, 1.082 s. `green.txt`: all twelve probe tests plus the current driver's boundary test **13/13**, zero failures/errors, exit 0, 1.166 s. `--help` confirms the new choices without model loading. Existing native/Z0 parity tests remain GREEN against the unmodified driver.

Both full suites then ran **serially**, with worktree Python `-B`, `TMPDIR=/private/tmp/c10z_build`, separate fresh scratch bytecode prefixes and CPU thread limits of one. Exact output:

```text
# astra-full.txt — exit 0
----------------------------------------------------------------------
Ran 200 tests in 113.290s

OK
C10Z_ASTRA_SELFTEST_PASS tests=200

# benchmark-full.txt — exit 0
----------------------------------------------------------------------
Ran 47 tests in 2.751s

OK
C10Z_BENCH_SELFTEST_PASS tests=47
```

The exec-bit test remains GREEN. Current counts reflect **198 minus one patch-dependent test plus three mask-control tests = 200**. Evidence is under **`/private/tmp/c10z_build/z0-sigma-test-bundle/`**. Syntax parsing and `git diff --check` passed. No pretrained model/tokenizer, real harness or GPU/MPS workload was loaded or launched by this follow-up. **The `ones` probe has not been run by the builder; its scientific result remains UNVERIFIED.**

**Operator launch for `--native-mask ones` — provided, not executed:**

```bash
C10Z_PROBE_ROOT='/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a'
C10Z_PROBE_OUT="$C10Z_PROBE_ROOT/results/c10z_astra_z0_probe/$(/bin/date -u +%Y%m%dT%H%M%SZ)"
/usr/bin/env -u C10_PROJECTOR -u N_EDIT -u C10_SUBJECT_OFFSET \
  -u C10_CTX_TEMPLATES -u C10_ARMS -u C10_KEY_LOCUS -u C10_RECIPES \
  LLMDB_ROOT="$C10Z_PROBE_ROOT" LLMDB_DEVICE=mps C10Z_TELEMETRY=0 \
  MODEL_ID=Qwen/Qwen2.5-3B MODEL_REV=3aab1f1954e9cc14eb9509a215f9e5ca08227a9b \
  PYTHONPYCACHEPREFIX="/private/tmp/c10z_build/z0-probe-bytecode/${C10Z_PROBE_OUT##*/}" \
  OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  "$C10Z_PROBE_ROOT/.venv/bin/python" -B \
  "$C10Z_PROBE_ROOT/experiments/track_c/c10z_astra_z0_probe.py" \
  "$C10Z_PROBE_OUT" --native-mask ones
```

Output remains **`$C10Z_PROBE_OUT/probe.json`**, in a fresh exclusively created UTC directory. The prior GPU diagnostic is unchanged. No future application of the saved driver patch or scientific remedy is authorized or implied by this build.

| Current file | SHA-256 |
|---|---|
| `experiments/track_c/c10z_astra_arms.py` — unchanged | `ab6f5c809d8187f4e5eb39e9cc6fbf40b6e357b2ecf5b18ecc887e05de7adebc` |
| `experiments/track_c/c10z_astra_z0_probe.py` | `e6ddd7a64bd2003475e39ac3587260a33ea239f36a374b2bb7df2a83cfc3cadf` |
| `experiments/track_c/c10z_astra_selftest.py` | `305cc3b03b7828bfb5689bcd324e7f97d023b65ca08af556bc4c277b15a0c99b` |
| `results/c10z_z0_sigma_record.patch` — driver plus matching test | `b81aeb74511118b2ab14bc2b1592ea0a2ee826d9b10eca60cc8ba606c82b1d77` |

Only the probe, selftest, appended patch hunk and this report addendum changed. The ten protected static files in the new snapshot retain their hashes, including driver, reader, benchmark/selftest, harness, engine source, prereg, hparams and both wrappers. The saved driver-patch prefix and complete earlier report remain byte-identical. No git mutation/commit, live result write or new architecture diagnostic occurred. `scope-before-report.json` and `after.json` hold the comparison and final report hash; the scratch context-save path is in `context-path.txt`. CPU evidence establishes kwargs/plumbing only and does not establish the proposed MPS causal explanation.

## 14. V5 copy fix — PATCH ONLY (2026-10-08)

**Delivered:** `results/c10z_v5fix.patch`, SHA-256 **`fc0b7d553bac78ba18862d1d8540c5b19cefe6c2e4f8318a0a7bd91f4f22d3f6`**. It bundles driver/probe fixes, the exact earlier sigma-recording change and matching test, plus eight new selftests. **The live driver remains `ab6f5c809d8187f4e5eb39e9cc6fbf40b6e357b2ecf5b18ecc887e05de7adebc`; no live source/test file was edited.**

Read `results/mps_offset_conversion_audit.md` in full. The operator's torch 2.8 MPS measurements identify corruption when a CPU copy also changes dtype, and a loud TypeError for float64 targets. Clone-first is unreliable. Every proposed fix transfers to CPU **before** casting; no clone-first workaround is used.

| Audited original site | Proposed change |
|---|---|
| `arms.py:224`, `margin_leads` | `logits.detach().cpu().to(torch.float32)` |
| `arms.py:177`, `torch_cpu64` | `value.detach().cpu().to(torch.float64)`; covers covectors/compute_G/z4 (:684–686, :1159–1162, :1213–1215) |
| `arms.py:253`, `semcon` | Separate CPU move and float32 cast |
| `arms.py:343`, `:347`, `target_probabilities` | Separate target/chunk moves and casts; preserve `copy=True` before in-place centering |
| `probe.py:170`, `:171`, `:181` | Explicit CPU/float32 native/full offset rows passed to `D.margin_leads`; split native max-logit conversion |

These remove **all six combined Tensor.to transfers** across the seven `c10z_astra_*.py` files. Audited constructors remain safe: probe :117–118 accepts Python float lists/CPU float64 tensors, :173 consumes `float(lead)`, and arms :1229 consumes a Python list. Allocations/metadata are not tensor transfers. No other ASTRA MPS→CPU cast through `copy_`, setitem, tensor overload or `.type()` was found. The new AST guard covers those explicit forms, positional/keyword/device-object `.to` and clone-first, with **ten unsafe and four safe controls**; it is not a whole-program tensor type proof.

The archived Z0 change saves `sigma_shape` and `original_full_sequence_sigma` before HALTED-V5. Its exact test body is bundled; the `.125` threshold, reader, engine, harness, benchmark and prereg are unchanged. The earlier `results/c10z_z0_sigma_record.patch` remains byte-identical.

**RED → GREEN, scratch only:** `/private/tmp/c10z_build/v5fix-patch/`. Tests preceded implementation. `red-expanded.log`: **9 tests, 5 expected assertion failures, 2 MPS skips, exit 1**. After the delivered patch was applied to a second pristine copy with `patch --batch --fuzz=0 -p1`, `green-patch.log`: **9 tests, 7 passed, 2 skipped, exit 0**.

| Test (new tests in `V5CopyTests`) | RED → GREEN |
|---|---|
| `test_margin_leads_no_combined_device_dtype_transfer_ast` | FAIL → PASS |
| `test_torch_cpu64_moves_to_cpu_before_float64_ast` | FAIL → PASS |
| `test_probe_native_and_full_rows_transfer_before_cast_ast` | FAIL → PASS |
| `test_astra_sources_no_combined_device_dtype_transfer_ast` | Six unsafe sites → none |
| `Fix2Tests.test_z0_v5_halt_persists_native_and_full_sigma` | Missing checks.Z0 → both sigmas persisted |
| `test_ast_guard_covers_all_unsafe_copy_api_forms` | PASS → PASS |
| `test_target_probabilities_preserves_offset_float32_inputs` | PASS → PASS; protects `copy=True` |
| `test_mps_offset_view_corruption_and_exact_split_copy` | SKIP → SKIP |
| `test_mps_torch_cpu64_transfers_before_float64` | SKIP → SKIP |

The MPS tests use tiny offset views and independently authored CPU expectations; they require exact repaired values and characterize the legacy corruption/TypeError. `green-ast-only.log` additionally proves **5/5 AST checks without importing Torch**, `CPU_AST_TORCH_NOT_IMPORTED=True`.

Both full suites ran serially in the fresh patched copy, with worktree Python `-B`, scratch TMPDIR, bytecode writes disabled and CPU thread limits of one:

```text
# astra-full-patch.log — exit 0
Ran 209 tests in 111.648s
OK (skipped=2)
C10Z_ASTRA_SELFTEST_PASS tests=209

# benchmark-full-patch.log — exit 0
Ran 47 tests in 2.736s
OK
C10Z_BENCH_SELFTEST_PASS tests=47
```

`git apply --check` passed against the live baseline. The scratch application had no fuzz/rejects; its three file hashes match the authored candidate. Proposed patched arms SHA-256: **`e3829f4103ead2927b01c01b93e9148a5056d2f03e962a804a62b72d5d73f5d0`**. The execute-bit test remains GREEN. All fourteen protected source/config/doc/wrapper/old-patch hashes are unchanged; the entire earlier report remains an exact byte prefix. Repository writes are limited to the requested patch and this appended section.

**Limits:** torch `2.8.0`; MPS built but unavailable to this session. Both MPS regressions are **UNVERIFIED here**, not hardware GREEN. No pretrained model, real harness/engine runtime, scientific GPU/probe run or benchmark rerun occurred. Live application remains under **D-C10z-driftcap**. Independent review attempts produced no signoff: Claude wrapper exit 3 (not logged in), Codex fallback exit 1 (app-server initialization `Operation not permitted`). Scratch holds full logs, packet, scope hashes and the AGENTS context-save handoff.
