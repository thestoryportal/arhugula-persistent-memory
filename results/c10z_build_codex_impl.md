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
