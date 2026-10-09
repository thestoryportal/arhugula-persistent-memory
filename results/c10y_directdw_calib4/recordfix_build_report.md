# C10Y record-only persistence correction — build report

**BUILT; CPU acceptance PASS.** Final selftest: **285 tests, 22.478 s, OK** (260 existing + 25 new). Astra implementation review: **PROCEED for record-only build acceptance**. No GPU, model/tokenizer load, science launch or commit was performed. Calibration 4 remains terminal `ZERO_STEP-IDENTITY`; this correction supplies no causal numerical conclusion and authorizes no calibration 5 or stage dispatch.

Authority: [build brief](../../docs/C10Y_RECORDFIX_BUILD_BRIEF.md), prereg §12, and [Astra ruling](zero_step_ruling_astra.md), ruling 3. The brief and ruling were read in full before implementation; numbered source was inspected before editing. Branch/root were verified as `worktree-c10k-route-a` in the supplied worktree.

## Requirement → test → implementation (ruling 3)

All named tests below are in `PrefixPersistenceTests` at `experiments/track_c/c10y_directdw_selftest.py:4850`; the complete output is attached below.

| Requirement | Tests/evidence | Implementation |
|---|---|---|
| R3.1 Retain already-computed data and offending inputs before validation | `test_calibration_forced_gates_retain_records_and_cleanup`, `test_inputs_durable_before_gate_and_phase_bytes_immutable`, `test_baseline_helper_return_retained_before_later_arm_failure`, `test_unit_result_survives_post_action_memory_halt` | Immutable local phase JSON before the gate; returned unit data saved before its existing memory cleanup; baseline helper/arm returns saved before later-arm work. Partial state survives the original prefix cleanup through an attached exception record. No recomputation. |
| R3.1 Include the actual inputs of helper gates | `test_helper_local_gradient_accumulation_and_ledger_gates`, `test_helper_local_parity_and_objective_offending_inputs`, `test_additional_original_gate_families_retain_inputs`, `test_baseline_projector_and_planned_update_gates_keep_readouts`, `test_executed_count_snapshot_retains_each_actual_count_operand`, `test_memory_floor_schema_and_budget_inputs_precede_original_gates` | Existing parity, gradient attempts, objective construction, accumulation comparisons/padding, consumption ledger, raw memory and budget observations are serialized before validation. Executed-loop snapshots include actual accepted-step and trajectory counts as well as the unchanged gate detail/proof. |
| R3.2 Exclusive durable writes; never freeze an early incomplete final aggregate | `test_prefix_final_collision_refuses_each_name_without_overwrite`, `test_actual_phase_collision_and_owned_context_tampering`, `test_phase_collision_and_io_failure_restore_state`, `test_tensor_phase_records_use_binary_sidecars_without_list_expansion` | Phase JSON/PT names are both prechecked; existing `write_json`/`save_tensors` retain exclusive create, flush and fsync. Required tensors use binary sidecars with member/dtype/shape and SHA references. Final names are published once after return or halt. Dense projector operators are not expanded: their already-used gate input is presence. |
| R3.3 Unreached/incomplete records are explicit and truthful | `test_failed_exact_phase_checks_mark_incomplete`, `test_later_mode_halt_does_not_mark_unreached_arms_started`, `test_target_partial_and_leakage_inputs_are_preserved`, `test_proof_early_exception_not_replaced_by_recording` | Missing final slots have `NOT-RUN` or `INCOMPLETE` and `halted_phase`; computed partial data stays under `data`. Starts are tracked by exact `(mode, arm, check)`, so another arm cannot manufacture an INCOMPLETE or passed result. Missing proof parity/timings are explicitly NOT-RUN. Existing successful check records remain intact. |
| R3.4 Preserve scientific outcome, diagnostic and cleanup | `test_malformed_baseline_preserves_law3_and_partial_records`, `test_nonfinite_gate_inputs_do_not_replace_original_halt`, `test_cleanup_only_and_primary_plus_cleanup_keep_partial_evidence`, `test_recorder_restores_existing_none_attributes`; cleanup assertions on real-prefix forced halts | Original code/detail/phase, traceback and primary-plus-cleanup chain retained. Missing baseline LAW#5 cannot replace LAW#3 with KeyError. Existing weight/global/hook/cache cleanup remains; added journal attributes restore prior values, including None. IO failures stay visible and are not retried at the failed sink. |
| R3.5 Calibration and shared stage paths | `test_stage_halt_uses_same_partial_record_retention`, later-mode stage-2 test, existing three-stage transport/common-artifact tests in the full suite | Both outer callers recover the attached partial prefix. Final collisions are refused except exact owned, hash-matching contexts/current predecessor common files; a tampered ownership hash is rejected. Stage-specific phase directories use `calib`, `s1`, `p1`, `p2`. |
| Acceptance: successful final names/schema/values unchanged | `test_success_serializer_preserves_computed_values_and_exact_names`, `test_success_final_serialization_matches_existing_schema`; separate verified prechange comparison | All six final files match the prechange fixture in JSON schema/values and tensor values under fixed clocks. Added phase records are the only extra output family. Binary archive byte equality is not claimed; loaded tensor equality is. |

The forced real-prefix cases cover LAW#3 (invalid counts and missing field), capture, zero-step identity, executed-loop identity/count (each actual count operand independently), target solve, leakage, missing merged/planned baseline readouts, precision, restoration, smoke and source drift, plus ordinary baseline exceptions. Focused helper cases invoke the real gradient, accumulation, override-ledger, train/deploy parity, objective, memory and budget gates with controlled leaves. Memory-schema/floor faults are injected at the CPU sampling boundary, with the original memory gate. These are fixture/plumbing evidence, not live science evidence.

## RED → GREEN chronology

Logs are preserved under `/private/tmp/c10y_build/recordfix_20261009/`; failed/obsolete fixture runs have not been relabeled as scientific or final passes.

| Evidence | Result |
|---|---|
| `before_suite.log`, unmodified current-source baseline | 260 tests, 14.645 s: **8 failures, 112 errors**; empty observed sink drift/forbidden modules. Appended §12 does not match the old production prereg pins; the initial scratch protected table was also stale. |
| `before_fixture_suite.log` | Intermediate fixture setup: 260 tests, 16.199 s, 1 failure/10 errors. Second transport source-copy site and scratch hash baseline then corrected. |
| `before_contract_suite.log`, before production persistence changes | **260 tests, 18.571 s, OK** under the byte-verified legacy-contract fixture setup below. |
| `registration.md`, `red_complete.log` | Requirements/tests recorded before implementation; **9 tests, 0.553 s, 25 assertion failures, no errors**. Earlier `red.log`/`red_corrected.log` fixture debugging is retained separately. |
| `green1.log`, `full1.log` | 9 targeted PASS; first full **269 PASS, 21.868 s**. Review 1 found real remaining gaps despite this pass. |
| `red_review1.log` → `green_review1.log` | Malformed LAW#3, status scope and partial-baseline loss reproduced: 13 tests, 5 assertion failures → **13 PASS**. |
| `red_review2.log` → `green_review2.log` | Missing post-action data and early proof secondary AttributeError reproduced: 18 tests, 1 failure/1 error → expanded **20 PASS**. |
| `red_review3.log` → `green_review3.log` | Tensor list expansion and missing proof parity status reproduced; a separate source-drift fixture error was corrected. **23 targeted PASS, 3.824 s**. The historical comparator was subsequently extracted from the permanent suite. |
| `full2.log` | **284 PASS, 22.248 s**. Review 3 requested actual count operands and a PT collision case. |
| `red_count_operands.log` → `green_final.log` | Each omitted actual executed-loop count reproduced: 1 test, 2 assertion failures → **25 targeted PASS, 3.881 s**, including JSON/PT collision cases. |
| `full_final.log` | **285 PASS, 22.478 s**; zero skips reported, empty owned/unattributed observed sink drift, no forbidden imports. Includes existing full-size 2048×11008 CPU reduction cases, native hanging-child deadline controls. |
| `prechange_equivalence_final.log` | **1 comparison PASS** on final source; all six final names, JSON schema/values and loaded tensor values equal. |

All Python was serial, CPU-only, `-B`, one Torch thread, under `/private/tmp/c10y_build`; `C10Y_ALLOWED_CHILD_TESTS=1` admitted only existing hash-allowlisted stub children. No real model worker was dispatched. The audit hook rejects writes to real results/diagnostic sinks and rejects non-stub subprocesses; `c10e_bandknob`, `transformers`, and `datasets` were not imported. Frozen scorer source is read as text by CPU fixtures.

## Diff and science-path verification

Only `experiments/track_c/c10y_directdw_arms.py`, its selftest and this new named report were written in the workspace by this build. The driver adds record helpers at lines 1307–1391 and hooks/caller recovery around the shared prefix at line 2615. No reader, telemetry checker, harness, engine, prereg, model config or launch script was edited.

`scope_audit.py` compares the verified prechange source to final source. Writer AST is identical. Original numerical/scientific call AST multisets and every original direct HALT condition in changed science helpers match (only the `source_end` local binding is normalized). Prefix/unit original cleanup AST is identical; the proof record hook is appended after its original cleanup assignments. Call ordering was also inspected in the actual diff by the builder and Astra; the multiset check alone does not prove order. Solve/forward/backward/write reductions, gate expressions, tolerances and thresholds were not changed. Fixed-clock successful payload equality supplies a behavioral CPU control in addition to this static evidence.

The historical comparator is scratch-only, with SHA-verified original `instrument_prefix` **and** `persist_prefix` taken from the before snapshot (identical to committed source 40d0d7d). It uses shared current numerical helpers and controlled CPU producers; those helpers are separately covered by the AST/diff checks. The permanent tests have a self-contained expected-payload serializer fixture and no dependency on this scratch snapshot.

## Deviations and limits (flush)

1. **Historical-contract fixture setup, not current admission.** Current prereg SHA is `005391a39e31d8174419de3e39078a42209ded1b7ab8caaf098d5d8a4f755004`; production driver/reader still pin `e069b358c362b2a05e3b668e8a29f33061e15a24306e321452e6fa46a4e83331`. Repinning was outside this record-only correction. `fixture_source` copies the exact pre-§12 body into scratch, accepting it only if its SHA matches both unchanged pins. Both existing source-copy sites use that verified fixture; arbitrary truncation/fallback is rejected. The scratch 193-path protected table was refreshed to the authorized current bytes/owned sources, with frozen paths checked against the before manifest. Thus the original current-source baseline failure remains an explicit limitation; a fixture PASS does not make current production preflight admissible.
2. **Nonfinite record representation.** NaN/Inf scalar observations are tagged (`nonfinite_float: nan/+inf/-inf`) so strict JSON cannot replace the scientific HALT. `exception_fields` uses the same encoding for nonfinite detail. Finite values and the raised original `Halt.detail` are unchanged; tensor sidecars retain dtype and values without casting. This deliberate diagnostic representation change is required to retain those inputs.
3. **No live performance/measurement claim.** Binary sidecars prevent enormous Python-scalar expansion, but still add dtype-preserving CPU transfers and disk IO. Dense projector internals are omitted in favor of the existing presence gate input. No new numerical summaries are computed. Real timing/resource outcomes may change because recording takes time; live MPS/model behavior and LAW#3/LAW#5 remain UNVERIFIED. Fresh source identity/timing evidence and separate program admission would still be required for any future run.
4. **Historical audit attribution.** Of 58 sampled calib1–4/diagnostic paths, 57 stayed byte-identical. Only `precast_scope_astra.log` changed concurrently from `7d78e3b4a181f4784581152473e096479eacf70ee4ee2de85da6a52f51a658be` to `7c0ff14f828335052854d9c7363414f93273db28e18ba5600d415f392f5a7b95`; its tail contains a completed precast-scope review. This build did not write that log; its author was not independently established. No sampled historical science JSON/tensor/diagnostic bytes changed, and no backfill was performed. The new report is intentionally excluded from that before manifest. Do not infer an unchanged entire historical tree.
5. **Review independence.** Requested GPT-6-Astra (high) inspected source/artifacts read-only and issued final PROCEED after FIX-FIRST rounds; this is same-family, weaker independence. It ran no tests/model/GPU and wrote only its scratch review. The full review chronology is attached below. No roadmap/CORPUS/memory/context-save edits were made because they are outside this record-only task.

## File identity and protected scope

| File | Before SHA-256 | Final SHA-256 |
|---|---|---|
| `experiments/track_c/c10y_directdw_arms.py` | `4b99827ea532e5d16168e1bb0aeca0569772132f413c08da359aa521fe452d3d` | `ead3cef2266a7c81035e5acb6c3a97b42f83da556ba093a9fd28ec403f7e158c` |
| `experiments/track_c/c10y_directdw_selftest.py` | `87874697c329a6caff41272268a488856619502b8c55929abcd9ce8940084364` | `81f3c07ec36fe1aa10bf31526f712cb3b015b0a86f714ba7aa3123a81875dd25` |

194 protected paths checked: 192 byte-identical; exactly the two authorized code/test files changed. Reader/checker hashes remain `f8d2598b01956be3ad390c76b2336ae1398e77d05045fb8870a3ae6e42cb2e78` and `843429cd8e9125fed44de85aabcb059542278cb955a1eff827d0343644236ffb`. Program-attributed C10Z/dashboard work is outside this correction; no such path changed in this sampled manifest.

## Reproduce the final checks

```sh
W=/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a
N=/private/tmp/c10y_build/recordfix_20261009
env C10Y_ALLOWED_CHILD_TESTS=1 TMPDIR=/private/tmp/c10y_build PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 "$W/.venv/bin/python" -B "$W/experiments/track_c/c10y_directdw_selftest.py"
env C10Y_ALLOWED_CHILD_TESTS=1 TMPDIR=/private/tmp/c10y_build PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 "$W/.venv/bin/python" -B "$N/compare_prechange.py"
env TMPDIR=/private/tmp/c10y_build PYTHONDONTWRITEBYTECODE=1 "$W/.venv/bin/python" -B "$N/scope_audit.py"
```

Executed via `/opt/homebrew/bin/rtk proxy`; shell paths were absolute, without changing cwd. The separate comparator/audit require their preserved scratch snapshots; the main selftest retains its existing scratch-baseline setup contract.

<details>
<summary>Full pre-implementation legacy-contract suite output</summary>

```text
test_observed_scorer_rejects_any_added_forward_keyword (__main__.AttentionMaskTests.test_observed_scorer_rejects_any_added_forward_keyword) ... ok
test_owned_forwards_preserve_original_mask_contract (__main__.AttentionMaskTests.test_owned_forwards_preserve_original_mask_contract) ... ok
test_padded_objective_and_lens_preserve_tokenizer_attention_mask (__main__.AttentionMaskTests.test_padded_objective_and_lens_preserve_tokenizer_attention_mask) ... ok
test_single_sequence_decode_and_observed_scorer_do_not_inject_mask (__main__.AttentionMaskTests.test_single_sequence_decode_and_observed_scorer_do_not_inject_mask) ... ok
test_admitted_main_calibration_handoff_failure_has_no_success_run (__main__.CalibrationErrorTests.test_admitted_main_calibration_handoff_failure_has_no_success_run) ... ok
test_calibration_context_failure_is_not_prefix_phase (__main__.CalibrationErrorTests.test_calibration_context_failure_is_not_prefix_phase) ... ok
test_calibration_publication_error_surfaces_phase (__main__.CalibrationErrorTests.test_calibration_publication_error_surfaces_phase) ... ok
test_calibration_valueerror_and_halt_trace_phase_persist (__main__.CalibrationErrorTests.test_calibration_valueerror_and_halt_trace_phase_persist) ... ok
test_main_unadmitted_preflight_error_has_trace_and_phase_without_writes (__main__.CalibrationErrorTests.test_main_unadmitted_preflight_error_has_trace_and_phase_without_writes) ... ok
test_nested_phase_retains_failure_and_restores_success_parent (__main__.CalibrationErrorTests.test_nested_phase_retains_failure_and_restores_success_parent) ... ok
test_nonzero_child_exit_overrides_prepublished_success_authority (__main__.CalibrationErrorTests.test_nonzero_child_exit_overrides_prepublished_success_authority) ... ok
test_nonzero_child_retains_budget_halt_precedence (__main__.CalibrationErrorTests.test_nonzero_child_retains_budget_halt_precedence) ... ok
test_primary_error_phase_survives_cleanup_failure (__main__.CalibrationErrorTests.test_primary_error_phase_survives_cleanup_failure) ... ok
test_primary_law3_halt_survives_cleanup_and_latches_schedule (__main__.CalibrationErrorTests.test_primary_law3_halt_survives_cleanup_and_latches_schedule) ... ok
test_pristine_probe_canonical_and_three_heldout_real_representation_pair (__main__.CalibrationErrorTests.test_pristine_probe_canonical_and_three_heldout_real_representation_pair) ... ok
test_remaining_readout_canonical_and_three_heldout_real_pair (__main__.CalibrationErrorTests.test_remaining_readout_canonical_and_three_heldout_real_pair) ... ok
test_stage_valueerror_and_halt_trace_phase_persist (__main__.CalibrationErrorTests.test_stage_valueerror_and_halt_trace_phase_persist) ... ok
test_supervisor_preserves_worker_original_trace_and_outcome (__main__.CalibrationErrorTests.test_supervisor_preserves_worker_original_trace_and_outcome) ... ok
test_supervisor_worker_exit_before_handoff_is_diagnosed (__main__.CalibrationErrorTests.test_supervisor_worker_exit_before_handoff_is_diagnosed) ... ok
test_t8_admitted_validation_failures_emit_trace_and_invalid (__main__.CalibrationErrorTests.test_t8_admitted_validation_failures_emit_trace_and_invalid) ... ok
test_telemetry_halt_and_instrument_error_trace_phase (__main__.CalibrationErrorTests.test_telemetry_halt_and_instrument_error_trace_phase) ... ok
test_all_three_targets_and_baseline_arm_timings_required (__main__.CalibrationForecastContractTests.test_all_three_targets_and_baseline_arm_timings_required) ... ok
test_bad_bound_records_return_unverified (__main__.CalibrationForecastContractTests.test_bad_bound_records_return_unverified) ... ok
test_calibration_schema_and_c5_completeness (__main__.CalibrationForecastContractTests.test_calibration_schema_and_c5_completeness) ... ok
test_cap_types_stage1_limit_and_later_stage_spend (__main__.CalibrationForecastContractTests.test_cap_types_stage1_limit_and_later_stage_spend) ... ok
test_each_phase_rejects_wrong_measured_mapping (__main__.CalibrationForecastContractTests.test_each_phase_rejects_wrong_measured_mapping) ... ok
test_full_c3_measured_map_and_every_repetition (__main__.CalibrationForecastContractTests.test_full_c3_measured_map_and_every_repetition) ... ok
test_independent_bound_requires_explicit_justification (__main__.CalibrationForecastContractTests.test_independent_bound_requires_explicit_justification) ... ok
test_input_identity_drift_and_padded_max_are_invalid (__main__.CalibrationForecastContractTests.test_input_identity_drift_and_padded_max_are_invalid) ... ok
test_merge_uses_larger_of_two_timed_merges (__main__.CalibrationForecastContractTests.test_merge_uses_larger_of_two_timed_merges) ... ok
test_missing_c3_unit_is_not_complete_support (__main__.CalibrationForecastContractTests.test_missing_c3_unit_is_not_complete_support) ... ok
test_noncalibration_measured_flag_cannot_replace_supported_bound (__main__.CalibrationForecastContractTests.test_noncalibration_measured_flag_cannot_replace_supported_bound) ... ok
test_optimisation_comparable_shape_and_iteration_flags (__main__.CalibrationForecastContractTests.test_optimisation_comparable_shape_and_iteration_flags) ... ok
test_optimisation_full_105_attempt_stage_workload (__main__.CalibrationForecastContractTests.test_optimisation_full_105_attempt_stage_workload) ... ok
test_optimisation_requires_three_accepted_rows_in_each_check (__main__.CalibrationForecastContractTests.test_optimisation_requires_three_accepted_rows_in_each_check) ... ok
test_optimisation_uses_slowest_iteration_not_mean (__main__.CalibrationForecastContractTests.test_optimisation_uses_slowest_iteration_not_mean) ... ok
test_original_my_edit_requires_two_distinct_repetitions (__main__.CalibrationForecastContractTests.test_original_my_edit_requires_two_distinct_repetitions) ... ok
test_overflow_attempt_is_cited_in_addition_to_six_accepted_rows (__main__.CalibrationForecastContractTests.test_overflow_attempt_is_cited_in_addition_to_six_accepted_rows) ... ok
test_prestart_gate_rechecks_schema_and_staleness (__main__.CalibrationForecastContractTests.test_prestart_gate_rechecks_schema_and_staleness) ... ok
test_prestart_gate_rejects_forged_or_omitted_measurement (__main__.CalibrationForecastContractTests.test_prestart_gate_rejects_forged_or_omitted_measurement) ... ok
test_raw_seconds_sync_status_and_workload_are_typed (__main__.CalibrationForecastContractTests.test_raw_seconds_sync_status_and_workload_are_typed) ... ok
test_readout_1380_reserve_and_larger_measured_bound (__main__.CalibrationForecastContractTests.test_readout_1380_reserve_and_larger_measured_bound) ... ok
test_calibration_forecast_rejects_partial_and_stale (__main__.CalibrationTests.test_calibration_forecast_rejects_partial_and_stale) ... ok
test_calibration_forecast_uses_all_repetitions_no_memory_or_inputs (__main__.CalibrationTests.test_calibration_forecast_uses_all_repetitions_no_memory_or_inputs) ... ok
test_calibration_go_spend_caps (__main__.CalibrationTests.test_calibration_go_spend_caps) ... ok
test_calibration_prefix_only_and_required_records (__main__.CalibrationTests.test_calibration_prefix_only_and_required_records) ... ok
test_calibration_reader_and_context_source_refused (__main__.CalibrationTests.test_calibration_reader_and_context_source_refused) ... ok
test_calibration_telemetry_variables_and_existing_directory_refused (__main__.CalibrationTests.test_calibration_telemetry_variables_and_existing_directory_refused) ... ok
test_calibration_v4_halt_persists_schedule (__main__.CalibrationTests.test_calibration_v4_halt_persists_schedule) ... ok
test_calibration_wrong_namespace_refused (__main__.CalibrationTests.test_calibration_wrong_namespace_refused) ... ok
test_frozen_bytes_suite_end (__main__.CalibrationTests.test_frozen_bytes_suite_end) ... ok
test_ast_rejects_keyword_positional_and_mixed_combined_transfers (__main__.DeviceConversionTests.test_ast_rejects_keyword_positional_and_mixed_combined_transfers) ... ok
test_cpu64_copies_offset_view_before_dtype_cast (__main__.DeviceConversionTests.test_cpu64_copies_offset_view_before_dtype_cast) ... ok
test_no_combined_device_dtype_transfer_in_owned_runtime (__main__.DeviceConversionTests.test_no_combined_device_dtype_transfer_in_owned_runtime) ... ok
test_reachable_helpers_only_combine_recorded_cpu_solve_transfer (__main__.DeviceConversionTests.test_reachable_helpers_only_combine_recorded_cpu_solve_transfer) ... ok
test_stored_weight_aligns_device_before_scale_and_fp16_add (__main__.DeviceConversionTests.test_stored_weight_aligns_device_before_scale_and_fp16_add) ... ok
test_to_like_transfers_before_casting_offset_view (__main__.DeviceConversionTests.test_to_like_transfers_before_casting_offset_view) ... ok
test_calibration_callsite_persists_complete_timing_tags (__main__.FinalReviewRegressionTests.test_calibration_callsite_persists_complete_timing_tags) ... ok
test_complete_compile_accounting_drives_ttl_equality (__main__.FinalReviewRegressionTests.test_complete_compile_accounting_drives_ttl_equality) ... ok
test_complete_compile_at_actual_scientific_hook_boundary (__main__.FinalReviewRegressionTests.test_complete_compile_at_actual_scientific_hook_boundary) ... ok
test_each_telemetry_method_preserves_every_state_and_A_grad (__main__.FinalReviewRegressionTests.test_each_telemetry_method_preserves_every_state_and_A_grad) ... ok
test_forecast_aware_first_expensive_action_is_not_entered (__main__.FinalReviewRegressionTests.test_forecast_aware_first_expensive_action_is_not_entered) ... ok
test_live_objective_graph_guard_precedes_backward_and_adam (__main__.FinalReviewRegressionTests.test_live_objective_graph_guard_precedes_backward_and_adam) ... /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py:3354: UserWarning: Converting a tensor with requires_grad=True to a scalar may lead to unexpected behavior.
Consider using tensor.detach() first. (Triggered internally at /Users/runner/work/pytorch/pytorch/pytorch/torch/csrc/autograd/generated/python_variable_methods.cpp:836.)
  self.assertEqual(opt.state,{});self.assertIsNone(p.grad);self.assertEqual(float(p[0]),1.)
ok
test_merged_fit_reduces_vocabulary_on_cpu_float64 (__main__.FinalReviewRegressionTests.test_merged_fit_reduces_vocabulary_on_cpu_float64) ... ok
test_off_scorer_is_original_during_actual_recipe_call (__main__.FinalReviewRegressionTests.test_off_scorer_is_original_during_actual_recipe_call) ... ok
test_phase_markers_cover_units_without_changing_operational_calls (__main__.FinalReviewRegressionTests.test_phase_markers_cover_units_without_changing_operational_calls) ... ok
test_premerge_parity_cannot_spend_postmerge_reserve (__main__.FinalReviewRegressionTests.test_premerge_parity_cannot_spend_postmerge_reserve) ... ok
test_real_writer_durable_merge_precedes_postmerge_readout (__main__.FinalReviewRegressionTests.test_real_writer_durable_merge_precedes_postmerge_readout) ... ok
test_real_writer_per_write_line_formula (__main__.FinalReviewRegressionTests.test_real_writer_per_write_line_formula) ... ok
test_recorded_contexts_never_sample_even_after_seeding (__main__.FinalReviewRegressionTests.test_recorded_contexts_never_sample_even_after_seeding) ... ok
test_actual_launcher_refuses_missing_calibration_before_import (__main__.IntegrationTests.test_actual_launcher_refuses_missing_calibration_before_import) ... ok
test_candidate_operations_require_baseline (__main__.IntegrationTests.test_candidate_operations_require_baseline) ... ok
test_native_hanging_worker_deadline_before_and_after_write (__main__.IntegrationTests.test_native_hanging_worker_deadline_before_and_after_write) ... ok
test_sequential_capture_matches_original (__main__.IntegrationTests.test_sequential_capture_matches_original) ... ok
test_stage_runner_artifacts_feed_real_reader_and_halt_before_candidates (__main__.IntegrationTests.test_stage_runner_artifacts_feed_real_reader_and_halt_before_candidates) ... ok
test_stored_control_scale1_identity (__main__.IntegrationTests.test_stored_control_scale1_identity) ... ok
test_strict_json_and_immutable_records (__main__.IntegrationTests.test_strict_json_and_immutable_records) ... ok
test_three_forced_zero_lr_iterations_and_telemetry_trajectory (__main__.IntegrationTests.test_three_forced_zero_lr_iterations_and_telemetry_trajectory) ... ok
test_all_cases_use_base (__main__.IsolationTests.test_all_cases_use_base) ... ok
test_live_write_positive_control (__main__.IsolationTests.test_live_write_positive_control) ... ok
test_real_dispatch_denied_with_temp_environment (__main__.IsolationTests.test_real_dispatch_denied_with_temp_environment) ... ok
test_relative_and_symlink_guard (__main__.IsolationTests.test_relative_and_symlink_guard) ... ok
test_seed_uses_only_cpu_generator (__main__.IsolationTests.test_seed_uses_only_cpu_generator) ... ok
test_selftest_root_refusal (__main__.IsolationTests.test_selftest_root_refusal) ... ok
test_later_stage_cannot_consume_stage1_calibration_measurements (__main__.LaunchDeltaTests.test_later_stage_cannot_consume_stage1_calibration_measurements) ... ok
test_nm_decimal_boundary_through_real_reader (__main__.LaunchDeltaTests.test_nm_decimal_boundary_through_real_reader) ... ok
test_nm_decimal_boundary_through_scientific_hook (__main__.LaunchDeltaTests.test_nm_decimal_boundary_through_scientific_hook) ... ok
test_norm_readouts_are_inside_writer_wall_clock (__main__.LaunchDeltaTests.test_norm_readouts_are_inside_writer_wall_clock) ... ok
test_real_iteration_producer_passes_c2_timing_validator (__main__.LaunchDeltaTests.test_real_iteration_producer_passes_c2_timing_validator) ... ok
test_stored_scale_sum_matches_reader_float64_sum (__main__.LaunchDeltaTests.test_stored_scale_sum_matches_reader_float64_sum) ... ok
test_supervisor_timeout_records_observed_template_hash_without_child (__main__.LaunchDeltaTests.test_supervisor_timeout_records_observed_template_hash_without_child) ... ok
test_t8_overlap_audit_precedes_first_forward_and_never_redraws (__main__.LaunchDeltaTests.test_t8_overlap_audit_precedes_first_forward_and_never_redraws) ... ok
test_context_freeze_and_leakage (__main__.LaunchTests.test_context_freeze_and_leakage) ... ok
test_direct_launch_shell_dependencies_are_executable_and_git_100755 (__main__.LaunchTests.test_direct_launch_shell_dependencies_are_executable_and_git_100755) ... ok
test_every_inherited_preflight_knob_refused (__main__.LaunchTests.test_every_inherited_preflight_knob_refused) ... ok
test_forecast_unverified_and_cap (__main__.LaunchTests.test_forecast_unverified_and_cap) ... ok
test_go_spend_and_stage_eligibility (__main__.LaunchTests.test_go_spend_and_stage_eligibility) ... ok
test_memory_boundaries (__main__.LaunchTests.test_memory_boundaries) ... ok
test_schedule_halt_survives_new_directory (__main__.LaunchTests.test_schedule_halt_survives_new_directory) ... ok
test_step_projection_reserves_readout (__main__.LaunchTests.test_step_projection_reserves_readout) ... ok
test_wrapper_delegate_dynamic_and_arm_restore (__main__.LaunchTests.test_wrapper_delegate_dynamic_and_arm_restore) ... ok
test_anchor_zero_denominator (__main__.NumericTests.test_anchor_zero_denominator) ... ok
test_capture_factorization (__main__.NumericTests.test_capture_factorization) ... ok
test_control_boundaries (__main__.NumericTests.test_control_boundaries) ... ok
test_full_size_float64_reductions (__main__.NumericTests.test_full_size_float64_reductions) ... ok
test_gram_norm_dense_reference (__main__.NumericTests.test_gram_norm_dense_reference) ... ok
test_mps_double_refused (__main__.NumericTests.test_mps_double_refused) ... ok
test_null_share_boundaries (__main__.NumericTests.test_null_share_boundaries) ... ok
test_size_scales_and_stored_arithmetic (__main__.NumericTests.test_size_scales_and_stored_arithmetic) ... ok
test_effective_weight_and_routing_gradient (__main__.OptimizerTests.test_effective_weight_and_routing_gradient) ... ok
test_kl_coefficient_once (__main__.OptimizerTests.test_kl_coefficient_once) ... ok
test_loss_scale_transaction (__main__.OptimizerTests.test_loss_scale_transaction) ... ok
test_microbatch_request_weighting (__main__.OptimizerTests.test_microbatch_request_weighting) ... ok
test_request_batch_and_target_only_objective (__main__.OptimizerTests.test_request_batch_and_target_only_objective) ... ok
test_sixth_overflow_halts_without_mutation (__main__.OptimizerTests.test_sixth_overflow_halts_without_mutation) ... ok
test_stopping_boundaries (__main__.OptimizerTests.test_stopping_boundaries) ... ok
test_unknown_hooks_preserved (__main__.OptimizerTests.test_unknown_hooks_preserved) ... ok
test_changed_template_source_or_stage1_content_halts (__main__.PinnedTemplateTests.test_changed_template_source_or_stage1_content_halts) ... ok
test_stage1_and_calibration_pin_before_first_engine_call (__main__.PinnedTemplateTests.test_stage1_and_calibration_pin_before_first_engine_call) ... ok
test_stages2_3_install_stage1_bytes_before_first_engine_use (__main__.PinnedTemplateTests.test_stages2_3_install_stage1_bytes_before_first_engine_use) ... ok
test_t8_digest_failure_has_halt_diagnostic_before_scoring (__main__.PinnedTemplateTests.test_t8_digest_failure_has_halt_diagnostic_before_scoring) ... ok
test_t8_installs_pin_and_writes_context_before_any_pass (__main__.PinnedTemplateTests.test_t8_installs_pin_and_writes_context_before_any_pass) ... ok
test_anchor_comparison_does_not_require_bz_sized_gain (__main__.ReaderAttributionTests.test_anchor_comparison_does_not_require_bz_sized_gain) ... ok
test_anchor_missing_invalid_and_unfit_untested (__main__.ReaderAttributionTests.test_anchor_missing_invalid_and_unfit_untested) ... ok
test_anchor_sham_descriptor_windows_not_fit_or_validity (__main__.ReaderAttributionTests.test_anchor_sham_descriptor_windows_not_fit_or_validity) ... ok
test_control_positive_requires_envelope_gain_fit_locality_and_validity (__main__.ReaderAttributionTests.test_control_positive_requires_envelope_gain_fit_locality_and_validity) ... ok
test_hy1_credit_requires_both_processes_attributed (__main__.ReaderAttributionTests.test_hy1_credit_requires_both_processes_attributed) ... ok
test_neff_minimum_and_anchor_gap_nine_ten (__main__.ReaderAttributionTests.test_neff_minimum_and_anchor_gap_nine_ten) ... ok
test_no_downscale_controls_required_at_actual_ratio_one (__main__.ReaderAttributionTests.test_no_downscale_controls_required_at_actual_ratio_one) ... ok
test_size_control_matching_and_direction_boundaries (__main__.ReaderAttributionTests.test_size_control_matching_and_direction_boundaries) ... ok
test_total_and_per_layer_growth_trigger_independent_controls (__main__.ReaderAttributionTests.test_total_and_per_layer_growth_trigger_independent_controls) ... ok
test_zero_reference_size_normalisation_conservative_provisional (__main__.ReaderAttributionTests.test_zero_reference_size_normalisation_conservative_provisional) ... ok
test_cross_shared_hin_and_telemetry_pair_identity (__main__.ReaderCrossProcessTests.test_cross_shared_hin_and_telemetry_pair_identity) ... ok
test_r1_cosine_and_distance_every_layer_boundaries (__main__.ReaderCrossProcessTests.test_r1_cosine_and_distance_every_layer_boundaries) ... ok
test_r1_required_controls_and_all_arms_independent (__main__.ReaderCrossProcessTests.test_r1_required_controls_and_all_arms_independent) ... ok
test_r1_zero_norm_rules_and_baseline_instrument (__main__.ReaderCrossProcessTests.test_r1_zero_norm_rules_and_baseline_instrument) ... ok
test_r2_count_spread_five_six (__main__.ReaderCrossProcessTests.test_r2_count_spread_five_six) ... ok
test_r3_incorrect_strings_do_not_count_as_disagreement (__main__.ReaderCrossProcessTests.test_r3_incorrect_strings_do_not_count_as_disagreement) ... ok
test_r3_keyed_boolean_disagreement_da_plus_three_four (__main__.ReaderCrossProcessTests.test_r3_keyed_boolean_disagreement_da_plus_three_four) ... ok
test_regenerated_target_hashes_need_not_match_shared_hin (__main__.ReaderCrossProcessTests.test_regenerated_target_hashes_need_not_match_shared_hin) ... ok
test_x1_not_run_halted_and_incomplete_never_fabricated_null (__main__.ReaderCrossProcessTests.test_x1_not_run_halted_and_incomplete_never_fabricated_null) ... ok
test_x2_identical_labels_and_union_qualifiers (__main__.ReaderCrossProcessTests.test_x2_identical_labels_and_union_qualifiers) ... ok
test_x3_mixed_labels_store_actual_counts (__main__.ReaderCrossProcessTests.test_x3_mixed_labels_store_actual_counts) ... ok
test_fit_e2e_minimum_canonical_and_every_stop (__main__.ReaderFitAndScreenTests.test_fit_e2e_minimum_canonical_and_every_stop) ... ok
test_fit_per_required_arm_and_apply_stored (__main__.ReaderFitAndScreenTests.test_fit_per_required_arm_and_apply_stored) ... ok
test_fit_requires_full_merged_matrix (__main__.ReaderFitAndScreenTests.test_fit_requires_full_merged_matrix) ... ok
test_fit_z_mean_and_maximum_boundaries (__main__.ReaderFitAndScreenTests.test_fit_z_mean_and_maximum_boundaries) ... ok
test_fit_z_zero_denominator_named_rule (__main__.ReaderFitAndScreenTests.test_fit_z_zero_denominator_named_rule) ... ok
test_s1_named_halts_without_screen_label (__main__.ReaderFitAndScreenTests.test_s1_named_halts_without_screen_label) ... ok
test_s2_s3_budget_write_boundary (__main__.ReaderFitAndScreenTests.test_s2_s3_budget_write_boundary) ... ok
test_s4_fit_precedes_high_count_locality_and_size (__main__.ReaderFitAndScreenTests.test_s4_fit_precedes_high_count_locality_and_size) ... ok
test_s5_s7_envelope_and_gain_boundaries (__main__.ReaderFitAndScreenTests.test_s5_s7_envelope_and_gain_boundaries) ... ok
test_s6_size_boundary_and_null_first_match (__main__.ReaderFitAndScreenTests.test_s6_size_boundary_and_null_first_match) ... ok
test_stage1_recorded_projection_exactly_120_minutes_fits (__main__.ReaderFitAndScreenTests.test_stage1_recorded_projection_exactly_120_minutes_fits) ... ok
test_load_calibration_directory_refused_before_read (__main__.ReaderLoadTests.test_load_calibration_directory_refused_before_read) ... ok
test_load_does_not_read_telemetry (__main__.ReaderLoadTests.test_load_does_not_read_telemetry) ... ok
test_load_later_self_contained_record_uses_own_outcome (__main__.ReaderLoadTests.test_load_later_self_contained_record_uses_own_outcome) ... ok
test_load_saved_halt_first_with_missing_science_artifacts (__main__.ReaderLoadTests.test_load_saved_halt_first_with_missing_science_artifacts) ... ok
test_load_strict_json_nonfinite_refused (__main__.ReaderLoadTests.test_load_strict_json_nonfinite_refused) ... ok
test_existing_arm_missing_metric_is_v13_invalid (__main__.ReaderOrderTests.test_existing_arm_missing_metric_is_v13_invalid) ... ok
test_missing_comparators_qualify_without_incomplete (__main__.ReaderOrderTests.test_missing_comparators_qualify_without_incomplete) ... ok
test_own_record_and_v5_missing_precede_validity_and_fit (__main__.ReaderOrderTests.test_own_record_and_v5_missing_precede_validity_and_fit) ... ok
test_recorded_halt_invalid_and_budget_first (__main__.ReaderOrderTests.test_recorded_halt_invalid_and_budget_first) ... ok
test_source_and_prereg_identity_refused (__main__.ReaderOrderTests.test_source_and_prereg_identity_refused) ... ok
test_stage1_not_run_controls_and_later_records_not_required (__main__.ReaderOrderTests.test_stage1_not_run_controls_and_later_records_not_required) ... ok
test_validity_precedes_fit_and_fit_precedes_counts (__main__.ReaderOrderTests.test_validity_precedes_fit_and_fit_precedes_counts) ... ok
test_g1_g2_each_frame_both_sides (__main__.ReaderProcessLocalityTests.test_g1_g2_each_frame_both_sides) ... ok
test_g3_g4_g5_unrounded_boundaries (__main__.ReaderProcessLocalityTests.test_g3_g4_g5_unrounded_boundaries) ... ok
test_g3_g5_display_rounding_cannot_substitute (__main__.ReaderProcessLocalityTests.test_g3_g5_display_rounding_cannot_substitute) ... ok
test_g6_relation_flips_report_only (__main__.ReaderProcessLocalityTests.test_g6_relation_flips_report_only) ... ok
test_p1_p2_p3 (__main__.ReaderProcessLocalityTests.test_p1_p2_p3) ... ok
test_p4_p5_p7_count_and_gain_boundaries (__main__.ReaderProcessLocalityTests.test_p4_p5_p7_count_and_gain_boundaries) ... ok
test_p6_tradeoff_and_p7_null_first_match (__main__.ReaderProcessLocalityTests.test_p6_tradeoff_and_p7_null_first_match) ... ok
test_w1_actual_size_boundary_qualifier_preserves_base (__main__.ReaderProcessLocalityTests.test_w1_actual_size_boundary_qualifier_preserves_base) ... ok
test_w2_ttl_warning_equality_nonblocking (__main__.ReaderProcessLocalityTests.test_w2_ttl_warning_equality_nonblocking) ... ok
test_authored_full_truth_rows_277_289 (__main__.ReaderTruthTableTests.test_authored_full_truth_rows_277_289) ... ok
test_authored_stage1_truth_rows_265_276 (__main__.ReaderTruthTableTests.test_authored_stage1_truth_rows_265_276) ... ok
test_v10_overflow_retries_five_six (__main__.ReaderValidityTests.test_v10_overflow_retries_five_six) ... ok
test_v11_hin_hashes_and_write_trace_required (__main__.ReaderValidityTests.test_v11_hin_hashes_and_write_trace_required) ... ok
test_v12_leakage_named_halt (__main__.ReaderValidityTests.test_v12_leakage_named_halt) ... ok
test_v13_every_applicable_numeric_family_nonfinite (__main__.ReaderValidityTests.test_v13_every_applicable_numeric_family_nonfinite) ... ok
test_v13_nonfinite_unjustified_null_and_typed_integer (__main__.ReaderValidityTests.test_v13_nonfinite_unjustified_null_and_typed_integer) ... ok
test_v13_typed_nulls_and_reasons (__main__.ReaderValidityTests.test_v13_typed_nulls_and_reasons) ... ok
test_v1_fingerprint_sha_sites_and_full_output (__main__.ReaderValidityTests.test_v1_fingerprint_sha_sites_and_full_output) ... ok
test_v2_each_recipe_standing_law5 (__main__.ReaderValidityTests.test_v2_each_recipe_standing_law5) ... ok
test_v3_accumulation_raw_cosine_distance_finiteness_and_scope (__main__.ReaderValidityTests.test_v3_accumulation_raw_cosine_distance_finiteness_and_scope) ... ok
test_v3_apply_stored_substitutions_not_optimiser_checks (__main__.ReaderValidityTests.test_v3_apply_stored_substitutions_not_optimiser_checks) ... ok
test_v3_capture_zero_step_and_executed_loop_raw_values (__main__.ReaderValidityTests.test_v3_capture_zero_step_and_executed_loop_raw_values) ... ok
test_v3_check_failure_order_and_scope (__main__.ReaderValidityTests.test_v3_check_failure_order_and_scope) ... ok
test_v3_gradient_halvings_hooks_and_smoke_raw_values (__main__.ReaderValidityTests.test_v3_gradient_halvings_hooks_and_smoke_raw_values) ... ok
test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) ... ok
test_v3_objective_nll_and_nonzero_kl_raw_boundaries (__main__.ReaderValidityTests.test_v3_objective_nll_and_nonzero_kl_raw_boundaries) ... ok
test_v4_a1_a2_and_exact_denominators (__main__.ReaderValidityTests.test_v4_a1_a2_and_exact_denominators) ... ok
test_v4_all_inclusive_baseline_endpoints (__main__.ReaderValidityTests.test_v4_all_inclusive_baseline_endpoints) ... ok
test_v4_before_candidates_required (__main__.ReaderValidityTests.test_v4_before_candidates_required) ... ok
test_v5_candidate_controls_67_68_each_arm (__main__.ReaderValidityTests.test_v5_candidate_controls_67_68_each_arm) ... ok
test_v6_overrides_are_exact_sets_not_counts (__main__.ReaderValidityTests.test_v6_overrides_are_exact_sets_not_counts) ... ok
test_v7_initial_projector_raw_share_cannot_hide_behind_passed (__main__.ReaderValidityTests.test_v7_initial_projector_raw_share_cannot_hide_behind_passed) ... ok
test_v7_planned_actual_each_layer_boundary_and_zero (__main__.ReaderValidityTests.test_v7_planned_actual_each_layer_boundary_and_zero) ... ok
test_v7_untouched_reference_miss_halts_precision_diagnosis (__main__.ReaderValidityTests.test_v7_untouched_reference_miss_halts_precision_diagnosis) ... ok
test_v8_string_full_equality_and_one_below_every_arm (__main__.ReaderValidityTests.test_v8_string_full_equality_and_one_below_every_arm) ... ok
test_v9_init_final_tokens_and_each_loss_component (__main__.ReaderValidityTests.test_v9_init_final_tokens_and_each_loss_component) ... ok
test_T11_audit_accepts_every_kind_with_only_kind_specific_fields (__main__.TelemetryCheckContract.test_T11_audit_accepts_every_kind_with_only_kind_specific_fields) ... ok
test_T11_audit_checks_payload_types_for_every_non_answer_kind (__main__.TelemetryCheckContract.test_T11_audit_checks_payload_types_for_every_non_answer_kind) ... ok
test_T11_audit_complete_answer_keys_pass_and_roundtrip (__main__.TelemetryCheckContract.test_T11_audit_complete_answer_keys_pass_and_roundtrip) ... ok
test_T11_audit_declared_disabled_missing_output_keeps_science_record (__main__.TelemetryCheckContract.test_T11_audit_declared_disabled_missing_output_keeps_science_record) ... ok
test_T11_audit_disabled_marker_does_not_excuse_a_gap_before_later_answers (__main__.TelemetryCheckContract.test_T11_audit_disabled_marker_does_not_excuse_a_gap_before_later_answers) ... ok
test_T11_audit_disabled_marker_does_not_excuse_mismatching_existing_line (__main__.TelemetryCheckContract.test_T11_audit_disabled_marker_does_not_excuse_mismatching_existing_line) ... ok
test_T11_audit_duplicate_answer_key_compromises_stage (__main__.TelemetryCheckContract.test_T11_audit_duplicate_answer_key_compromises_stage) ... ok
test_T11_audit_header_must_be_present_initial_and_unique (__main__.TelemetryCheckContract.test_T11_audit_header_must_be_present_initial_and_unique) ... ok
test_T11_audit_mismatch_compromises_stage_and_requires_telemetry_off_rerun (__main__.TelemetryCheckContract.test_T11_audit_mismatch_compromises_stage_and_requires_telemetry_off_rerun) ... ok
test_T11_audit_missing_answer_field_is_malformed (__main__.TelemetryCheckContract.test_T11_audit_missing_answer_field_is_malformed) ... ok
test_T11_audit_missing_expected_key_compromises_stage (__main__.TelemetryCheckContract.test_T11_audit_missing_expected_key_compromises_stage) ... ok
test_T11_audit_missing_file_is_missing_output (__main__.TelemetryCheckContract.test_T11_audit_missing_file_is_missing_output) ... ok
test_T11_audit_model_free_entrypoint_never_loads_driver_or_harness (__main__.TelemetryCheckContract.test_T11_audit_model_free_entrypoint_never_loads_driver_or_harness) ... ok
test_T11_audit_never_mutates_science_records_or_reader_output (__main__.TelemetryCheckContract.test_T11_audit_never_mutates_science_records_or_reader_output) ... ok
test_T11_audit_refuses_existing_audit_without_rewriting_evidence (__main__.TelemetryCheckContract.test_T11_audit_refuses_existing_audit_without_rewriting_evidence) ... ok
test_T11_audit_rejects_unknown_field_on_every_known_kind (__main__.TelemetryCheckContract.test_T11_audit_rejects_unknown_field_on_every_known_kind) ... ok
test_T11_audit_strict_json_rejects_nonfinite_and_duplicate_json_fields (__main__.TelemetryCheckContract.test_T11_audit_strict_json_rejects_nonfinite_and_duplicate_json_fields) ... ok
test_T11_audit_unknown_key_or_kind_or_field_is_unexpected (__main__.TelemetryCheckContract.test_T11_audit_unknown_key_or_kind_or_field_is_unexpected) ... ok
test_T11_audit_uses_stage_two_and_three_tags_and_record_paths (__main__.TelemetryCheckContract.test_T11_audit_uses_stage_two_and_three_tags_and_record_paths) ... ok
test_T11_audit_wrong_types_and_nulls_are_malformed (__main__.TelemetryCheckContract.test_T11_audit_wrong_types_and_nulls_are_malformed) ... ok
test_T11_reader_does_not_open_telemetry_or_use_audit_as_gate (__main__.TelemetryCheckContract.test_T11_reader_does_not_open_telemetry_or_use_audit_as_gate) ... ok
test_T8_runner_inert_pristine_stub_never_calls_writer_or_recipe (__main__.TelemetryCheckContract.test_T8_runner_inert_pristine_stub_never_calls_writer_or_recipe) ... ok
test_T8_runner_other_verdicts_exit_zero_and_preserve_verdict (__main__.TelemetryCheckContract.test_T8_runner_other_verdicts_exit_zero_and_preserve_verdict) ... ok
test_T8_runner_preflight_refuses_knob_before_output_creation (__main__.TelemetryCheckContract.test_T8_runner_preflight_refuses_knob_before_output_creation) ... ok
test_T8_runner_preserves_existing_record (__main__.TelemetryCheckContract.test_T8_runner_preserves_existing_record) ... ok
test_T8_runner_records_complete_current_identity_and_strict_roundtrip (__main__.TelemetryCheckContract.test_T8_runner_records_complete_current_identity_and_strict_roundtrip) ... ok
test_T8_runner_rejects_namespace_itself_and_nested_subdirectories (__main__.TelemetryCheckContract.test_T8_runner_rejects_namespace_itself_and_nested_subdirectories) ... ok
test_T8_runner_rejects_output_outside_namespace (__main__.TelemetryCheckContract.test_T8_runner_rejects_output_outside_namespace) ... ok
test_T8_runner_rejects_relative_output_before_writes (__main__.TelemetryCheckContract.test_T8_runner_rejects_relative_output_before_writes) ... ok
test_T8_runner_rejects_symlink_escape (__main__.TelemetryCheckContract.test_T8_runner_rejects_symlink_escape) ... ok
test_T8_runner_weight_change_is_invalid_exit_two (__main__.TelemetryCheckContract.test_T8_runner_weight_change_is_invalid_exit_two) ... ok
test_full_stage_counts_and_payload_not_smaller (__main__.TelemetryForecastTests.test_full_stage_counts_and_payload_not_smaller) ... ok
test_inertness_bytes_once_and_duplicate_nonfinite_refused (__main__.TelemetryForecastTests.test_inertness_bytes_once_and_duplicate_nonfinite_refused) ... ok
test_on_requires_separate_phase_before_dispatch (__main__.TelemetryForecastTests.test_on_requires_separate_phase_before_dispatch) ... ok
test_per_kind_measurements_workload_and_sum_enforced (__main__.TelemetryForecastTests.test_per_kind_measurements_workload_and_sum_enforced) ... ok
test_frozen_harness_scorers_receive_no_injected_kwargs (__main__.TelemetryReferenceTests.test_frozen_harness_scorers_receive_no_injected_kwargs) ... ok
test_reference_scorer_is_exact_frozen_capture_copy (__main__.TelemetryReferenceTests.test_reference_scorer_is_exact_frozen_capture_copy) ... ok
test_t8_uses_frozen_off_reference_and_observed_on_scorer (__main__.TelemetryReferenceTests.test_t8_uses_frozen_off_reference_and_observed_on_scorer) ... ok
test_every_kind_state_preservation_and_volume (__main__.TelemetryTests.test_every_kind_state_preservation_and_volume) ... ok
test_frozen_hparams_lens_uses_actual_linear_head (__main__.TelemetryTests.test_frozen_hparams_lens_uses_actual_linear_head) ... ok
test_inertness_and_drifting_baseline (__main__.TelemetryTests.test_inertness_and_drifting_baseline) ... ok
test_invalid_switches_refused_before_write (__main__.TelemetryTests.test_invalid_switches_refused_before_write) ... ok
test_io_failures_disable_once_and_baseexception_propagates (__main__.TelemetryTests.test_io_failures_disable_once_and_baseexception_propagates) ... ok
test_off_has_no_object_or_directory (__main__.TelemetryTests.test_off_has_no_object_or_directory) ... ok
test_scorer_ast_and_exact_inputs (__main__.TelemetryTests.test_scorer_ast_and_exact_inputs) ... ok
test_t8_serialized_wrong_answer_is_not_inert (__main__.TelemetryTests.test_t8_serialized_wrong_answer_is_not_inert) ... ok
test_telemetry_never_calls_operational_clock_or_writes_input_record (__main__.TelemetryTests.test_telemetry_never_calls_operational_clock_or_writes_input_record) ... ok
test_actual_cpu_update_direction_changes_fail_real_reader_repro_gate (__main__.TransportTests.test_actual_cpu_update_direction_changes_fail_real_reader_repro_gate) ... ok
test_completed_stage1_runner_to_reader_and_cpu_pt_transport (__main__.TransportTests.test_completed_stage1_runner_to_reader_and_cpu_pt_transport) ... ok
test_completed_three_stages_preserve_common_files_and_compute_real_repro (__main__.TransportTests.test_completed_three_stages_preserve_common_files_and_compute_real_repro) ... ok
test_real_scored_recipe_accounts_for_scientific_hook_readout_time (__main__.TransportTests.test_real_scored_recipe_accounts_for_scientific_hook_readout_time) ... ok
test_requested_stage_forecast_is_checked_before_dispatch_and_worker (__main__.TransportTests.test_requested_stage_forecast_is_checked_before_dispatch_and_worker) ... ok
test_saved_overlay_hash_is_the_immutable_serialized_bundle (__main__.TransportTests.test_saved_overlay_hash_is_the_immutable_serialized_bundle) ... ok
test_stage3_pair_mismatch_is_refused_in_parent_before_any_launch_write (__main__.TransportTests.test_stage3_pair_mismatch_is_refused_in_parent_before_any_launch_write) ... ok
test_stage3_telemetry_setting_cannot_change_after_stage2 (__main__.TransportTests.test_stage3_telemetry_setting_cannot_change_after_stage2) ... ok
test_tampered_stage2_pt_refuses_stage3_before_scientific_callbacks (__main__.TransportTests.test_tampered_stage2_pt_refuses_stage3_before_scientific_callbacks) ... ok
test_telemetry_off_on_transport_changes_only_T1_fields_at_every_stage (__main__.TransportTests.test_telemetry_off_on_transport_changes_only_T1_fields_at_every_stage) ... ok
test_wrong_stage3_predecessor_refuses_in_main_before_harness_or_supervisor (__main__.TransportTests.test_wrong_stage3_predecessor_refuses_in_main_before_harness_or_supervisor) ... ok

----------------------------------------------------------------------
Ran 260 tests in 18.571s

OK
{"launched": false, "reasons": ["missing/unknown/duplicate phases"], "status": "UNVERIFIED"}
ISOLATION OWNED LISTING DRIFT: []
ISOLATION OTHER OBSERVED UNATTRIBUTED: []
SYS_MODULES_FORBIDDEN: []
C10Y_DIRECTDW_SELFTEST PASS — CPU ONLY; LIVE LAW#3/LAW#5 UNVERIFIED
```

</details>

<details>
<summary>Full final selftest output</summary>

```text
test_observed_scorer_rejects_any_added_forward_keyword (__main__.AttentionMaskTests.test_observed_scorer_rejects_any_added_forward_keyword) ... ok
test_owned_forwards_preserve_original_mask_contract (__main__.AttentionMaskTests.test_owned_forwards_preserve_original_mask_contract) ... ok
test_padded_objective_and_lens_preserve_tokenizer_attention_mask (__main__.AttentionMaskTests.test_padded_objective_and_lens_preserve_tokenizer_attention_mask) ... ok
test_single_sequence_decode_and_observed_scorer_do_not_inject_mask (__main__.AttentionMaskTests.test_single_sequence_decode_and_observed_scorer_do_not_inject_mask) ... ok
test_admitted_main_calibration_handoff_failure_has_no_success_run (__main__.CalibrationErrorTests.test_admitted_main_calibration_handoff_failure_has_no_success_run) ... ok
test_calibration_context_failure_is_not_prefix_phase (__main__.CalibrationErrorTests.test_calibration_context_failure_is_not_prefix_phase) ... ok
test_calibration_publication_error_surfaces_phase (__main__.CalibrationErrorTests.test_calibration_publication_error_surfaces_phase) ... ok
test_calibration_valueerror_and_halt_trace_phase_persist (__main__.CalibrationErrorTests.test_calibration_valueerror_and_halt_trace_phase_persist) ... ok
test_main_unadmitted_preflight_error_has_trace_and_phase_without_writes (__main__.CalibrationErrorTests.test_main_unadmitted_preflight_error_has_trace_and_phase_without_writes) ... ok
test_nested_phase_retains_failure_and_restores_success_parent (__main__.CalibrationErrorTests.test_nested_phase_retains_failure_and_restores_success_parent) ... ok
test_nonzero_child_exit_overrides_prepublished_success_authority (__main__.CalibrationErrorTests.test_nonzero_child_exit_overrides_prepublished_success_authority) ... ok
test_nonzero_child_retains_budget_halt_precedence (__main__.CalibrationErrorTests.test_nonzero_child_retains_budget_halt_precedence) ... ok
test_primary_error_phase_survives_cleanup_failure (__main__.CalibrationErrorTests.test_primary_error_phase_survives_cleanup_failure) ... ok
test_primary_law3_halt_survives_cleanup_and_latches_schedule (__main__.CalibrationErrorTests.test_primary_law3_halt_survives_cleanup_and_latches_schedule) ... ok
test_pristine_probe_canonical_and_three_heldout_real_representation_pair (__main__.CalibrationErrorTests.test_pristine_probe_canonical_and_three_heldout_real_representation_pair) ... ok
test_remaining_readout_canonical_and_three_heldout_real_pair (__main__.CalibrationErrorTests.test_remaining_readout_canonical_and_three_heldout_real_pair) ... ok
test_stage_valueerror_and_halt_trace_phase_persist (__main__.CalibrationErrorTests.test_stage_valueerror_and_halt_trace_phase_persist) ... ok
test_supervisor_preserves_worker_original_trace_and_outcome (__main__.CalibrationErrorTests.test_supervisor_preserves_worker_original_trace_and_outcome) ... ok
test_supervisor_worker_exit_before_handoff_is_diagnosed (__main__.CalibrationErrorTests.test_supervisor_worker_exit_before_handoff_is_diagnosed) ... ok
test_t8_admitted_validation_failures_emit_trace_and_invalid (__main__.CalibrationErrorTests.test_t8_admitted_validation_failures_emit_trace_and_invalid) ... ok
test_telemetry_halt_and_instrument_error_trace_phase (__main__.CalibrationErrorTests.test_telemetry_halt_and_instrument_error_trace_phase) ... ok
test_all_three_targets_and_baseline_arm_timings_required (__main__.CalibrationForecastContractTests.test_all_three_targets_and_baseline_arm_timings_required) ... ok
test_bad_bound_records_return_unverified (__main__.CalibrationForecastContractTests.test_bad_bound_records_return_unverified) ... ok
test_calibration_schema_and_c5_completeness (__main__.CalibrationForecastContractTests.test_calibration_schema_and_c5_completeness) ... ok
test_cap_types_stage1_limit_and_later_stage_spend (__main__.CalibrationForecastContractTests.test_cap_types_stage1_limit_and_later_stage_spend) ... ok
test_each_phase_rejects_wrong_measured_mapping (__main__.CalibrationForecastContractTests.test_each_phase_rejects_wrong_measured_mapping) ... ok
test_full_c3_measured_map_and_every_repetition (__main__.CalibrationForecastContractTests.test_full_c3_measured_map_and_every_repetition) ... ok
test_independent_bound_requires_explicit_justification (__main__.CalibrationForecastContractTests.test_independent_bound_requires_explicit_justification) ... ok
test_input_identity_drift_and_padded_max_are_invalid (__main__.CalibrationForecastContractTests.test_input_identity_drift_and_padded_max_are_invalid) ... ok
test_merge_uses_larger_of_two_timed_merges (__main__.CalibrationForecastContractTests.test_merge_uses_larger_of_two_timed_merges) ... ok
test_missing_c3_unit_is_not_complete_support (__main__.CalibrationForecastContractTests.test_missing_c3_unit_is_not_complete_support) ... ok
test_noncalibration_measured_flag_cannot_replace_supported_bound (__main__.CalibrationForecastContractTests.test_noncalibration_measured_flag_cannot_replace_supported_bound) ... ok
test_optimisation_comparable_shape_and_iteration_flags (__main__.CalibrationForecastContractTests.test_optimisation_comparable_shape_and_iteration_flags) ... ok
test_optimisation_full_105_attempt_stage_workload (__main__.CalibrationForecastContractTests.test_optimisation_full_105_attempt_stage_workload) ... ok
test_optimisation_requires_three_accepted_rows_in_each_check (__main__.CalibrationForecastContractTests.test_optimisation_requires_three_accepted_rows_in_each_check) ... ok
test_optimisation_uses_slowest_iteration_not_mean (__main__.CalibrationForecastContractTests.test_optimisation_uses_slowest_iteration_not_mean) ... ok
test_original_my_edit_requires_two_distinct_repetitions (__main__.CalibrationForecastContractTests.test_original_my_edit_requires_two_distinct_repetitions) ... ok
test_overflow_attempt_is_cited_in_addition_to_six_accepted_rows (__main__.CalibrationForecastContractTests.test_overflow_attempt_is_cited_in_addition_to_six_accepted_rows) ... ok
test_prestart_gate_rechecks_schema_and_staleness (__main__.CalibrationForecastContractTests.test_prestart_gate_rechecks_schema_and_staleness) ... ok
test_prestart_gate_rejects_forged_or_omitted_measurement (__main__.CalibrationForecastContractTests.test_prestart_gate_rejects_forged_or_omitted_measurement) ... ok
test_raw_seconds_sync_status_and_workload_are_typed (__main__.CalibrationForecastContractTests.test_raw_seconds_sync_status_and_workload_are_typed) ... ok
test_readout_1380_reserve_and_larger_measured_bound (__main__.CalibrationForecastContractTests.test_readout_1380_reserve_and_larger_measured_bound) ... ok
test_calibration_forecast_rejects_partial_and_stale (__main__.CalibrationTests.test_calibration_forecast_rejects_partial_and_stale) ... ok
test_calibration_forecast_uses_all_repetitions_no_memory_or_inputs (__main__.CalibrationTests.test_calibration_forecast_uses_all_repetitions_no_memory_or_inputs) ... ok
test_calibration_go_spend_caps (__main__.CalibrationTests.test_calibration_go_spend_caps) ... ok
test_calibration_prefix_only_and_required_records (__main__.CalibrationTests.test_calibration_prefix_only_and_required_records) ... ok
test_calibration_reader_and_context_source_refused (__main__.CalibrationTests.test_calibration_reader_and_context_source_refused) ... ok
test_calibration_telemetry_variables_and_existing_directory_refused (__main__.CalibrationTests.test_calibration_telemetry_variables_and_existing_directory_refused) ... ok
test_calibration_v4_halt_persists_schedule (__main__.CalibrationTests.test_calibration_v4_halt_persists_schedule) ... ok
test_calibration_wrong_namespace_refused (__main__.CalibrationTests.test_calibration_wrong_namespace_refused) ... ok
test_frozen_bytes_suite_end (__main__.CalibrationTests.test_frozen_bytes_suite_end) ... ok
test_ast_rejects_keyword_positional_and_mixed_combined_transfers (__main__.DeviceConversionTests.test_ast_rejects_keyword_positional_and_mixed_combined_transfers) ... ok
test_cpu64_copies_offset_view_before_dtype_cast (__main__.DeviceConversionTests.test_cpu64_copies_offset_view_before_dtype_cast) ... ok
test_no_combined_device_dtype_transfer_in_owned_runtime (__main__.DeviceConversionTests.test_no_combined_device_dtype_transfer_in_owned_runtime) ... ok
test_reachable_helpers_only_combine_recorded_cpu_solve_transfer (__main__.DeviceConversionTests.test_reachable_helpers_only_combine_recorded_cpu_solve_transfer) ... ok
test_stored_weight_aligns_device_before_scale_and_fp16_add (__main__.DeviceConversionTests.test_stored_weight_aligns_device_before_scale_and_fp16_add) ... ok
test_to_like_transfers_before_casting_offset_view (__main__.DeviceConversionTests.test_to_like_transfers_before_casting_offset_view) ... ok
test_calibration_callsite_persists_complete_timing_tags (__main__.FinalReviewRegressionTests.test_calibration_callsite_persists_complete_timing_tags) ... ok
test_complete_compile_accounting_drives_ttl_equality (__main__.FinalReviewRegressionTests.test_complete_compile_accounting_drives_ttl_equality) ... ok
test_complete_compile_at_actual_scientific_hook_boundary (__main__.FinalReviewRegressionTests.test_complete_compile_at_actual_scientific_hook_boundary) ... ok
test_each_telemetry_method_preserves_every_state_and_A_grad (__main__.FinalReviewRegressionTests.test_each_telemetry_method_preserves_every_state_and_A_grad) ... ok
test_forecast_aware_first_expensive_action_is_not_entered (__main__.FinalReviewRegressionTests.test_forecast_aware_first_expensive_action_is_not_entered) ... ok
test_live_objective_graph_guard_precedes_backward_and_adam (__main__.FinalReviewRegressionTests.test_live_objective_graph_guard_precedes_backward_and_adam) ... /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py:3354: UserWarning: Converting a tensor with requires_grad=True to a scalar may lead to unexpected behavior.
Consider using tensor.detach() first. (Triggered internally at /Users/runner/work/pytorch/pytorch/pytorch/torch/csrc/autograd/generated/python_variable_methods.cpp:836.)
  self.assertEqual(opt.state,{});self.assertIsNone(p.grad);self.assertEqual(float(p[0]),1.)
ok
test_merged_fit_reduces_vocabulary_on_cpu_float64 (__main__.FinalReviewRegressionTests.test_merged_fit_reduces_vocabulary_on_cpu_float64) ... ok
test_off_scorer_is_original_during_actual_recipe_call (__main__.FinalReviewRegressionTests.test_off_scorer_is_original_during_actual_recipe_call) ... ok
test_phase_markers_cover_units_without_changing_operational_calls (__main__.FinalReviewRegressionTests.test_phase_markers_cover_units_without_changing_operational_calls) ... ok
test_premerge_parity_cannot_spend_postmerge_reserve (__main__.FinalReviewRegressionTests.test_premerge_parity_cannot_spend_postmerge_reserve) ... ok
test_real_writer_durable_merge_precedes_postmerge_readout (__main__.FinalReviewRegressionTests.test_real_writer_durable_merge_precedes_postmerge_readout) ... ok
test_real_writer_per_write_line_formula (__main__.FinalReviewRegressionTests.test_real_writer_per_write_line_formula) ... ok
test_recorded_contexts_never_sample_even_after_seeding (__main__.FinalReviewRegressionTests.test_recorded_contexts_never_sample_even_after_seeding) ... ok
test_actual_launcher_refuses_missing_calibration_before_import (__main__.IntegrationTests.test_actual_launcher_refuses_missing_calibration_before_import) ... ok
test_candidate_operations_require_baseline (__main__.IntegrationTests.test_candidate_operations_require_baseline) ... ok
test_native_hanging_worker_deadline_before_and_after_write (__main__.IntegrationTests.test_native_hanging_worker_deadline_before_and_after_write) ... ok
test_sequential_capture_matches_original (__main__.IntegrationTests.test_sequential_capture_matches_original) ... ok
test_stage_runner_artifacts_feed_real_reader_and_halt_before_candidates (__main__.IntegrationTests.test_stage_runner_artifacts_feed_real_reader_and_halt_before_candidates) ... ok
test_stored_control_scale1_identity (__main__.IntegrationTests.test_stored_control_scale1_identity) ... ok
test_strict_json_and_immutable_records (__main__.IntegrationTests.test_strict_json_and_immutable_records) ... ok
test_three_forced_zero_lr_iterations_and_telemetry_trajectory (__main__.IntegrationTests.test_three_forced_zero_lr_iterations_and_telemetry_trajectory) ... ok
test_all_cases_use_base (__main__.IsolationTests.test_all_cases_use_base) ... ok
test_live_write_positive_control (__main__.IsolationTests.test_live_write_positive_control) ... ok
test_real_dispatch_denied_with_temp_environment (__main__.IsolationTests.test_real_dispatch_denied_with_temp_environment) ... ok
test_relative_and_symlink_guard (__main__.IsolationTests.test_relative_and_symlink_guard) ... ok
test_seed_uses_only_cpu_generator (__main__.IsolationTests.test_seed_uses_only_cpu_generator) ... ok
test_selftest_root_refusal (__main__.IsolationTests.test_selftest_root_refusal) ... ok
test_later_stage_cannot_consume_stage1_calibration_measurements (__main__.LaunchDeltaTests.test_later_stage_cannot_consume_stage1_calibration_measurements) ... ok
test_nm_decimal_boundary_through_real_reader (__main__.LaunchDeltaTests.test_nm_decimal_boundary_through_real_reader) ... ok
test_nm_decimal_boundary_through_scientific_hook (__main__.LaunchDeltaTests.test_nm_decimal_boundary_through_scientific_hook) ... ok
test_norm_readouts_are_inside_writer_wall_clock (__main__.LaunchDeltaTests.test_norm_readouts_are_inside_writer_wall_clock) ... ok
test_real_iteration_producer_passes_c2_timing_validator (__main__.LaunchDeltaTests.test_real_iteration_producer_passes_c2_timing_validator) ... ok
test_stored_scale_sum_matches_reader_float64_sum (__main__.LaunchDeltaTests.test_stored_scale_sum_matches_reader_float64_sum) ... ok
test_supervisor_timeout_records_observed_template_hash_without_child (__main__.LaunchDeltaTests.test_supervisor_timeout_records_observed_template_hash_without_child) ... ok
test_t8_overlap_audit_precedes_first_forward_and_never_redraws (__main__.LaunchDeltaTests.test_t8_overlap_audit_precedes_first_forward_and_never_redraws) ... ok
test_context_freeze_and_leakage (__main__.LaunchTests.test_context_freeze_and_leakage) ... ok
test_direct_launch_shell_dependencies_are_executable_and_git_100755 (__main__.LaunchTests.test_direct_launch_shell_dependencies_are_executable_and_git_100755) ... ok
test_every_inherited_preflight_knob_refused (__main__.LaunchTests.test_every_inherited_preflight_knob_refused) ... ok
test_forecast_unverified_and_cap (__main__.LaunchTests.test_forecast_unverified_and_cap) ... ok
test_go_spend_and_stage_eligibility (__main__.LaunchTests.test_go_spend_and_stage_eligibility) ... ok
test_memory_boundaries (__main__.LaunchTests.test_memory_boundaries) ... ok
test_schedule_halt_survives_new_directory (__main__.LaunchTests.test_schedule_halt_survives_new_directory) ... ok
test_step_projection_reserves_readout (__main__.LaunchTests.test_step_projection_reserves_readout) ... ok
test_wrapper_delegate_dynamic_and_arm_restore (__main__.LaunchTests.test_wrapper_delegate_dynamic_and_arm_restore) ... ok
test_anchor_zero_denominator (__main__.NumericTests.test_anchor_zero_denominator) ... ok
test_capture_factorization (__main__.NumericTests.test_capture_factorization) ... ok
test_control_boundaries (__main__.NumericTests.test_control_boundaries) ... ok
test_full_size_float64_reductions (__main__.NumericTests.test_full_size_float64_reductions) ... ok
test_gram_norm_dense_reference (__main__.NumericTests.test_gram_norm_dense_reference) ... ok
test_mps_double_refused (__main__.NumericTests.test_mps_double_refused) ... ok
test_null_share_boundaries (__main__.NumericTests.test_null_share_boundaries) ... ok
test_size_scales_and_stored_arithmetic (__main__.NumericTests.test_size_scales_and_stored_arithmetic) ... ok
test_effective_weight_and_routing_gradient (__main__.OptimizerTests.test_effective_weight_and_routing_gradient) ... ok
test_kl_coefficient_once (__main__.OptimizerTests.test_kl_coefficient_once) ... ok
test_loss_scale_transaction (__main__.OptimizerTests.test_loss_scale_transaction) ... ok
test_microbatch_request_weighting (__main__.OptimizerTests.test_microbatch_request_weighting) ... ok
test_request_batch_and_target_only_objective (__main__.OptimizerTests.test_request_batch_and_target_only_objective) ... ok
test_sixth_overflow_halts_without_mutation (__main__.OptimizerTests.test_sixth_overflow_halts_without_mutation) ... ok
test_stopping_boundaries (__main__.OptimizerTests.test_stopping_boundaries) ... ok
test_unknown_hooks_preserved (__main__.OptimizerTests.test_unknown_hooks_preserved) ... ok
test_changed_template_source_or_stage1_content_halts (__main__.PinnedTemplateTests.test_changed_template_source_or_stage1_content_halts) ... ok
test_stage1_and_calibration_pin_before_first_engine_call (__main__.PinnedTemplateTests.test_stage1_and_calibration_pin_before_first_engine_call) ... ok
test_stages2_3_install_stage1_bytes_before_first_engine_use (__main__.PinnedTemplateTests.test_stages2_3_install_stage1_bytes_before_first_engine_use) ... ok
test_t8_digest_failure_has_halt_diagnostic_before_scoring (__main__.PinnedTemplateTests.test_t8_digest_failure_has_halt_diagnostic_before_scoring) ... ok
test_t8_installs_pin_and_writes_context_before_any_pass (__main__.PinnedTemplateTests.test_t8_installs_pin_and_writes_context_before_any_pass) ... ok
test_actual_phase_collision_and_owned_context_tampering (__main__.PrefixPersistenceTests.test_actual_phase_collision_and_owned_context_tampering) ... ok
test_additional_original_gate_families_retain_inputs (__main__.PrefixPersistenceTests.test_additional_original_gate_families_retain_inputs) ... ok
test_baseline_helper_return_retained_before_later_arm_failure (__main__.PrefixPersistenceTests.test_baseline_helper_return_retained_before_later_arm_failure) ... ok
test_baseline_projector_and_planned_update_gates_keep_readouts (__main__.PrefixPersistenceTests.test_baseline_projector_and_planned_update_gates_keep_readouts) ... ok
test_calibration_forced_gates_retain_records_and_cleanup (__main__.PrefixPersistenceTests.test_calibration_forced_gates_retain_records_and_cleanup) ... ok
test_cleanup_only_and_primary_plus_cleanup_keep_partial_evidence (__main__.PrefixPersistenceTests.test_cleanup_only_and_primary_plus_cleanup_keep_partial_evidence) ... ok
test_executed_count_snapshot_retains_each_actual_count_operand (__main__.PrefixPersistenceTests.test_executed_count_snapshot_retains_each_actual_count_operand) ... ok
test_failed_exact_phase_checks_mark_incomplete (__main__.PrefixPersistenceTests.test_failed_exact_phase_checks_mark_incomplete) ... ok
test_helper_local_gradient_accumulation_and_ledger_gates (__main__.PrefixPersistenceTests.test_helper_local_gradient_accumulation_and_ledger_gates) ... ok
test_helper_local_parity_and_objective_offending_inputs (__main__.PrefixPersistenceTests.test_helper_local_parity_and_objective_offending_inputs) ... ok
test_inputs_durable_before_gate_and_phase_bytes_immutable (__main__.PrefixPersistenceTests.test_inputs_durable_before_gate_and_phase_bytes_immutable) ... ok
test_later_mode_halt_does_not_mark_unreached_arms_started (__main__.PrefixPersistenceTests.test_later_mode_halt_does_not_mark_unreached_arms_started) ... ok
test_malformed_baseline_preserves_law3_and_partial_records (__main__.PrefixPersistenceTests.test_malformed_baseline_preserves_law3_and_partial_records) ... ok
test_memory_floor_schema_and_budget_inputs_precede_original_gates (__main__.PrefixPersistenceTests.test_memory_floor_schema_and_budget_inputs_precede_original_gates) ... ok
test_nonfinite_gate_inputs_do_not_replace_original_halt (__main__.PrefixPersistenceTests.test_nonfinite_gate_inputs_do_not_replace_original_halt) ... ok
test_phase_collision_and_io_failure_restore_state (__main__.PrefixPersistenceTests.test_phase_collision_and_io_failure_restore_state) ... ok
test_prefix_final_collision_refuses_each_name_without_overwrite (__main__.PrefixPersistenceTests.test_prefix_final_collision_refuses_each_name_without_overwrite) ... ok
test_proof_early_exception_not_replaced_by_recording (__main__.PrefixPersistenceTests.test_proof_early_exception_not_replaced_by_recording) ... ok
test_recorder_restores_existing_none_attributes (__main__.PrefixPersistenceTests.test_recorder_restores_existing_none_attributes) ... ok
test_stage_halt_uses_same_partial_record_retention (__main__.PrefixPersistenceTests.test_stage_halt_uses_same_partial_record_retention) ... ok
test_success_final_serialization_matches_existing_schema (__main__.PrefixPersistenceTests.test_success_final_serialization_matches_existing_schema) ... ok
test_success_serializer_preserves_computed_values_and_exact_names (__main__.PrefixPersistenceTests.test_success_serializer_preserves_computed_values_and_exact_names) ... ok
test_target_partial_and_leakage_inputs_are_preserved (__main__.PrefixPersistenceTests.test_target_partial_and_leakage_inputs_are_preserved) ... ok
test_tensor_phase_records_use_binary_sidecars_without_list_expansion (__main__.PrefixPersistenceTests.test_tensor_phase_records_use_binary_sidecars_without_list_expansion) ... ok
test_unit_result_survives_post_action_memory_halt (__main__.PrefixPersistenceTests.test_unit_result_survives_post_action_memory_halt) ... ok
test_anchor_comparison_does_not_require_bz_sized_gain (__main__.ReaderAttributionTests.test_anchor_comparison_does_not_require_bz_sized_gain) ... ok
test_anchor_missing_invalid_and_unfit_untested (__main__.ReaderAttributionTests.test_anchor_missing_invalid_and_unfit_untested) ... ok
test_anchor_sham_descriptor_windows_not_fit_or_validity (__main__.ReaderAttributionTests.test_anchor_sham_descriptor_windows_not_fit_or_validity) ... ok
test_control_positive_requires_envelope_gain_fit_locality_and_validity (__main__.ReaderAttributionTests.test_control_positive_requires_envelope_gain_fit_locality_and_validity) ... ok
test_hy1_credit_requires_both_processes_attributed (__main__.ReaderAttributionTests.test_hy1_credit_requires_both_processes_attributed) ... ok
test_neff_minimum_and_anchor_gap_nine_ten (__main__.ReaderAttributionTests.test_neff_minimum_and_anchor_gap_nine_ten) ... ok
test_no_downscale_controls_required_at_actual_ratio_one (__main__.ReaderAttributionTests.test_no_downscale_controls_required_at_actual_ratio_one) ... ok
test_size_control_matching_and_direction_boundaries (__main__.ReaderAttributionTests.test_size_control_matching_and_direction_boundaries) ... ok
test_total_and_per_layer_growth_trigger_independent_controls (__main__.ReaderAttributionTests.test_total_and_per_layer_growth_trigger_independent_controls) ... ok
test_zero_reference_size_normalisation_conservative_provisional (__main__.ReaderAttributionTests.test_zero_reference_size_normalisation_conservative_provisional) ... ok
test_cross_shared_hin_and_telemetry_pair_identity (__main__.ReaderCrossProcessTests.test_cross_shared_hin_and_telemetry_pair_identity) ... ok
test_r1_cosine_and_distance_every_layer_boundaries (__main__.ReaderCrossProcessTests.test_r1_cosine_and_distance_every_layer_boundaries) ... ok
test_r1_required_controls_and_all_arms_independent (__main__.ReaderCrossProcessTests.test_r1_required_controls_and_all_arms_independent) ... ok
test_r1_zero_norm_rules_and_baseline_instrument (__main__.ReaderCrossProcessTests.test_r1_zero_norm_rules_and_baseline_instrument) ... ok
test_r2_count_spread_five_six (__main__.ReaderCrossProcessTests.test_r2_count_spread_five_six) ... ok
test_r3_incorrect_strings_do_not_count_as_disagreement (__main__.ReaderCrossProcessTests.test_r3_incorrect_strings_do_not_count_as_disagreement) ... ok
test_r3_keyed_boolean_disagreement_da_plus_three_four (__main__.ReaderCrossProcessTests.test_r3_keyed_boolean_disagreement_da_plus_three_four) ... ok
test_regenerated_target_hashes_need_not_match_shared_hin (__main__.ReaderCrossProcessTests.test_regenerated_target_hashes_need_not_match_shared_hin) ... ok
test_x1_not_run_halted_and_incomplete_never_fabricated_null (__main__.ReaderCrossProcessTests.test_x1_not_run_halted_and_incomplete_never_fabricated_null) ... ok
test_x2_identical_labels_and_union_qualifiers (__main__.ReaderCrossProcessTests.test_x2_identical_labels_and_union_qualifiers) ... ok
test_x3_mixed_labels_store_actual_counts (__main__.ReaderCrossProcessTests.test_x3_mixed_labels_store_actual_counts) ... ok
test_fit_e2e_minimum_canonical_and_every_stop (__main__.ReaderFitAndScreenTests.test_fit_e2e_minimum_canonical_and_every_stop) ... ok
test_fit_per_required_arm_and_apply_stored (__main__.ReaderFitAndScreenTests.test_fit_per_required_arm_and_apply_stored) ... ok
test_fit_requires_full_merged_matrix (__main__.ReaderFitAndScreenTests.test_fit_requires_full_merged_matrix) ... ok
test_fit_z_mean_and_maximum_boundaries (__main__.ReaderFitAndScreenTests.test_fit_z_mean_and_maximum_boundaries) ... ok
test_fit_z_zero_denominator_named_rule (__main__.ReaderFitAndScreenTests.test_fit_z_zero_denominator_named_rule) ... ok
test_s1_named_halts_without_screen_label (__main__.ReaderFitAndScreenTests.test_s1_named_halts_without_screen_label) ... ok
test_s2_s3_budget_write_boundary (__main__.ReaderFitAndScreenTests.test_s2_s3_budget_write_boundary) ... ok
test_s4_fit_precedes_high_count_locality_and_size (__main__.ReaderFitAndScreenTests.test_s4_fit_precedes_high_count_locality_and_size) ... ok
test_s5_s7_envelope_and_gain_boundaries (__main__.ReaderFitAndScreenTests.test_s5_s7_envelope_and_gain_boundaries) ... ok
test_s6_size_boundary_and_null_first_match (__main__.ReaderFitAndScreenTests.test_s6_size_boundary_and_null_first_match) ... ok
test_stage1_recorded_projection_exactly_120_minutes_fits (__main__.ReaderFitAndScreenTests.test_stage1_recorded_projection_exactly_120_minutes_fits) ... ok
test_load_calibration_directory_refused_before_read (__main__.ReaderLoadTests.test_load_calibration_directory_refused_before_read) ... ok
test_load_does_not_read_telemetry (__main__.ReaderLoadTests.test_load_does_not_read_telemetry) ... ok
test_load_later_self_contained_record_uses_own_outcome (__main__.ReaderLoadTests.test_load_later_self_contained_record_uses_own_outcome) ... ok
test_load_saved_halt_first_with_missing_science_artifacts (__main__.ReaderLoadTests.test_load_saved_halt_first_with_missing_science_artifacts) ... ok
test_load_strict_json_nonfinite_refused (__main__.ReaderLoadTests.test_load_strict_json_nonfinite_refused) ... ok
test_existing_arm_missing_metric_is_v13_invalid (__main__.ReaderOrderTests.test_existing_arm_missing_metric_is_v13_invalid) ... ok
test_missing_comparators_qualify_without_incomplete (__main__.ReaderOrderTests.test_missing_comparators_qualify_without_incomplete) ... ok
test_own_record_and_v5_missing_precede_validity_and_fit (__main__.ReaderOrderTests.test_own_record_and_v5_missing_precede_validity_and_fit) ... ok
test_recorded_halt_invalid_and_budget_first (__main__.ReaderOrderTests.test_recorded_halt_invalid_and_budget_first) ... ok
test_source_and_prereg_identity_refused (__main__.ReaderOrderTests.test_source_and_prereg_identity_refused) ... ok
test_stage1_not_run_controls_and_later_records_not_required (__main__.ReaderOrderTests.test_stage1_not_run_controls_and_later_records_not_required) ... ok
test_validity_precedes_fit_and_fit_precedes_counts (__main__.ReaderOrderTests.test_validity_precedes_fit_and_fit_precedes_counts) ... ok
test_g1_g2_each_frame_both_sides (__main__.ReaderProcessLocalityTests.test_g1_g2_each_frame_both_sides) ... ok
test_g3_g4_g5_unrounded_boundaries (__main__.ReaderProcessLocalityTests.test_g3_g4_g5_unrounded_boundaries) ... ok
test_g3_g5_display_rounding_cannot_substitute (__main__.ReaderProcessLocalityTests.test_g3_g5_display_rounding_cannot_substitute) ... ok
test_g6_relation_flips_report_only (__main__.ReaderProcessLocalityTests.test_g6_relation_flips_report_only) ... ok
test_p1_p2_p3 (__main__.ReaderProcessLocalityTests.test_p1_p2_p3) ... ok
test_p4_p5_p7_count_and_gain_boundaries (__main__.ReaderProcessLocalityTests.test_p4_p5_p7_count_and_gain_boundaries) ... ok
test_p6_tradeoff_and_p7_null_first_match (__main__.ReaderProcessLocalityTests.test_p6_tradeoff_and_p7_null_first_match) ... ok
test_w1_actual_size_boundary_qualifier_preserves_base (__main__.ReaderProcessLocalityTests.test_w1_actual_size_boundary_qualifier_preserves_base) ... ok
test_w2_ttl_warning_equality_nonblocking (__main__.ReaderProcessLocalityTests.test_w2_ttl_warning_equality_nonblocking) ... ok
test_authored_full_truth_rows_277_289 (__main__.ReaderTruthTableTests.test_authored_full_truth_rows_277_289) ... ok
test_authored_stage1_truth_rows_265_276 (__main__.ReaderTruthTableTests.test_authored_stage1_truth_rows_265_276) ... ok
test_v10_overflow_retries_five_six (__main__.ReaderValidityTests.test_v10_overflow_retries_five_six) ... ok
test_v11_hin_hashes_and_write_trace_required (__main__.ReaderValidityTests.test_v11_hin_hashes_and_write_trace_required) ... ok
test_v12_leakage_named_halt (__main__.ReaderValidityTests.test_v12_leakage_named_halt) ... ok
test_v13_every_applicable_numeric_family_nonfinite (__main__.ReaderValidityTests.test_v13_every_applicable_numeric_family_nonfinite) ... ok
test_v13_nonfinite_unjustified_null_and_typed_integer (__main__.ReaderValidityTests.test_v13_nonfinite_unjustified_null_and_typed_integer) ... ok
test_v13_typed_nulls_and_reasons (__main__.ReaderValidityTests.test_v13_typed_nulls_and_reasons) ... ok
test_v1_fingerprint_sha_sites_and_full_output (__main__.ReaderValidityTests.test_v1_fingerprint_sha_sites_and_full_output) ... ok
test_v2_each_recipe_standing_law5 (__main__.ReaderValidityTests.test_v2_each_recipe_standing_law5) ... ok
test_v3_accumulation_raw_cosine_distance_finiteness_and_scope (__main__.ReaderValidityTests.test_v3_accumulation_raw_cosine_distance_finiteness_and_scope) ... ok
test_v3_apply_stored_substitutions_not_optimiser_checks (__main__.ReaderValidityTests.test_v3_apply_stored_substitutions_not_optimiser_checks) ... ok
test_v3_capture_zero_step_and_executed_loop_raw_values (__main__.ReaderValidityTests.test_v3_capture_zero_step_and_executed_loop_raw_values) ... ok
test_v3_check_failure_order_and_scope (__main__.ReaderValidityTests.test_v3_check_failure_order_and_scope) ... ok
test_v3_gradient_halvings_hooks_and_smoke_raw_values (__main__.ReaderValidityTests.test_v3_gradient_halvings_hooks_and_smoke_raw_values) ... ok
test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) ... ok
test_v3_objective_nll_and_nonzero_kl_raw_boundaries (__main__.ReaderValidityTests.test_v3_objective_nll_and_nonzero_kl_raw_boundaries) ... ok
test_v4_a1_a2_and_exact_denominators (__main__.ReaderValidityTests.test_v4_a1_a2_and_exact_denominators) ... ok
test_v4_all_inclusive_baseline_endpoints (__main__.ReaderValidityTests.test_v4_all_inclusive_baseline_endpoints) ... ok
test_v4_before_candidates_required (__main__.ReaderValidityTests.test_v4_before_candidates_required) ... ok
test_v5_candidate_controls_67_68_each_arm (__main__.ReaderValidityTests.test_v5_candidate_controls_67_68_each_arm) ... ok
test_v6_overrides_are_exact_sets_not_counts (__main__.ReaderValidityTests.test_v6_overrides_are_exact_sets_not_counts) ... ok
test_v7_initial_projector_raw_share_cannot_hide_behind_passed (__main__.ReaderValidityTests.test_v7_initial_projector_raw_share_cannot_hide_behind_passed) ... ok
test_v7_planned_actual_each_layer_boundary_and_zero (__main__.ReaderValidityTests.test_v7_planned_actual_each_layer_boundary_and_zero) ... ok
test_v7_untouched_reference_miss_halts_precision_diagnosis (__main__.ReaderValidityTests.test_v7_untouched_reference_miss_halts_precision_diagnosis) ... ok
test_v8_string_full_equality_and_one_below_every_arm (__main__.ReaderValidityTests.test_v8_string_full_equality_and_one_below_every_arm) ... ok
test_v9_init_final_tokens_and_each_loss_component (__main__.ReaderValidityTests.test_v9_init_final_tokens_and_each_loss_component) ... ok
test_T11_audit_accepts_every_kind_with_only_kind_specific_fields (__main__.TelemetryCheckContract.test_T11_audit_accepts_every_kind_with_only_kind_specific_fields) ... ok
test_T11_audit_checks_payload_types_for_every_non_answer_kind (__main__.TelemetryCheckContract.test_T11_audit_checks_payload_types_for_every_non_answer_kind) ... ok
test_T11_audit_complete_answer_keys_pass_and_roundtrip (__main__.TelemetryCheckContract.test_T11_audit_complete_answer_keys_pass_and_roundtrip) ... ok
test_T11_audit_declared_disabled_missing_output_keeps_science_record (__main__.TelemetryCheckContract.test_T11_audit_declared_disabled_missing_output_keeps_science_record) ... ok
test_T11_audit_disabled_marker_does_not_excuse_a_gap_before_later_answers (__main__.TelemetryCheckContract.test_T11_audit_disabled_marker_does_not_excuse_a_gap_before_later_answers) ... ok
test_T11_audit_disabled_marker_does_not_excuse_mismatching_existing_line (__main__.TelemetryCheckContract.test_T11_audit_disabled_marker_does_not_excuse_mismatching_existing_line) ... ok
test_T11_audit_duplicate_answer_key_compromises_stage (__main__.TelemetryCheckContract.test_T11_audit_duplicate_answer_key_compromises_stage) ... ok
test_T11_audit_header_must_be_present_initial_and_unique (__main__.TelemetryCheckContract.test_T11_audit_header_must_be_present_initial_and_unique) ... ok
test_T11_audit_mismatch_compromises_stage_and_requires_telemetry_off_rerun (__main__.TelemetryCheckContract.test_T11_audit_mismatch_compromises_stage_and_requires_telemetry_off_rerun) ... ok
test_T11_audit_missing_answer_field_is_malformed (__main__.TelemetryCheckContract.test_T11_audit_missing_answer_field_is_malformed) ... ok
test_T11_audit_missing_expected_key_compromises_stage (__main__.TelemetryCheckContract.test_T11_audit_missing_expected_key_compromises_stage) ... ok
test_T11_audit_missing_file_is_missing_output (__main__.TelemetryCheckContract.test_T11_audit_missing_file_is_missing_output) ... ok
test_T11_audit_model_free_entrypoint_never_loads_driver_or_harness (__main__.TelemetryCheckContract.test_T11_audit_model_free_entrypoint_never_loads_driver_or_harness) ... ok
test_T11_audit_never_mutates_science_records_or_reader_output (__main__.TelemetryCheckContract.test_T11_audit_never_mutates_science_records_or_reader_output) ... ok
test_T11_audit_refuses_existing_audit_without_rewriting_evidence (__main__.TelemetryCheckContract.test_T11_audit_refuses_existing_audit_without_rewriting_evidence) ... ok
test_T11_audit_rejects_unknown_field_on_every_known_kind (__main__.TelemetryCheckContract.test_T11_audit_rejects_unknown_field_on_every_known_kind) ... ok
test_T11_audit_strict_json_rejects_nonfinite_and_duplicate_json_fields (__main__.TelemetryCheckContract.test_T11_audit_strict_json_rejects_nonfinite_and_duplicate_json_fields) ... ok
test_T11_audit_unknown_key_or_kind_or_field_is_unexpected (__main__.TelemetryCheckContract.test_T11_audit_unknown_key_or_kind_or_field_is_unexpected) ... ok
test_T11_audit_uses_stage_two_and_three_tags_and_record_paths (__main__.TelemetryCheckContract.test_T11_audit_uses_stage_two_and_three_tags_and_record_paths) ... ok
test_T11_audit_wrong_types_and_nulls_are_malformed (__main__.TelemetryCheckContract.test_T11_audit_wrong_types_and_nulls_are_malformed) ... ok
test_T11_reader_does_not_open_telemetry_or_use_audit_as_gate (__main__.TelemetryCheckContract.test_T11_reader_does_not_open_telemetry_or_use_audit_as_gate) ... ok
test_T8_runner_inert_pristine_stub_never_calls_writer_or_recipe (__main__.TelemetryCheckContract.test_T8_runner_inert_pristine_stub_never_calls_writer_or_recipe) ... ok
test_T8_runner_other_verdicts_exit_zero_and_preserve_verdict (__main__.TelemetryCheckContract.test_T8_runner_other_verdicts_exit_zero_and_preserve_verdict) ... ok
test_T8_runner_preflight_refuses_knob_before_output_creation (__main__.TelemetryCheckContract.test_T8_runner_preflight_refuses_knob_before_output_creation) ... ok
test_T8_runner_preserves_existing_record (__main__.TelemetryCheckContract.test_T8_runner_preserves_existing_record) ... ok
test_T8_runner_records_complete_current_identity_and_strict_roundtrip (__main__.TelemetryCheckContract.test_T8_runner_records_complete_current_identity_and_strict_roundtrip) ... ok
test_T8_runner_rejects_namespace_itself_and_nested_subdirectories (__main__.TelemetryCheckContract.test_T8_runner_rejects_namespace_itself_and_nested_subdirectories) ... ok
test_T8_runner_rejects_output_outside_namespace (__main__.TelemetryCheckContract.test_T8_runner_rejects_output_outside_namespace) ... ok
test_T8_runner_rejects_relative_output_before_writes (__main__.TelemetryCheckContract.test_T8_runner_rejects_relative_output_before_writes) ... ok
test_T8_runner_rejects_symlink_escape (__main__.TelemetryCheckContract.test_T8_runner_rejects_symlink_escape) ... ok
test_T8_runner_weight_change_is_invalid_exit_two (__main__.TelemetryCheckContract.test_T8_runner_weight_change_is_invalid_exit_two) ... ok
test_full_stage_counts_and_payload_not_smaller (__main__.TelemetryForecastTests.test_full_stage_counts_and_payload_not_smaller) ... ok
test_inertness_bytes_once_and_duplicate_nonfinite_refused (__main__.TelemetryForecastTests.test_inertness_bytes_once_and_duplicate_nonfinite_refused) ... ok
test_on_requires_separate_phase_before_dispatch (__main__.TelemetryForecastTests.test_on_requires_separate_phase_before_dispatch) ... ok
test_per_kind_measurements_workload_and_sum_enforced (__main__.TelemetryForecastTests.test_per_kind_measurements_workload_and_sum_enforced) ... ok
test_frozen_harness_scorers_receive_no_injected_kwargs (__main__.TelemetryReferenceTests.test_frozen_harness_scorers_receive_no_injected_kwargs) ... ok
test_reference_scorer_is_exact_frozen_capture_copy (__main__.TelemetryReferenceTests.test_reference_scorer_is_exact_frozen_capture_copy) ... ok
test_t8_uses_frozen_off_reference_and_observed_on_scorer (__main__.TelemetryReferenceTests.test_t8_uses_frozen_off_reference_and_observed_on_scorer) ... ok
test_every_kind_state_preservation_and_volume (__main__.TelemetryTests.test_every_kind_state_preservation_and_volume) ... ok
test_frozen_hparams_lens_uses_actual_linear_head (__main__.TelemetryTests.test_frozen_hparams_lens_uses_actual_linear_head) ... ok
test_inertness_and_drifting_baseline (__main__.TelemetryTests.test_inertness_and_drifting_baseline) ... ok
test_invalid_switches_refused_before_write (__main__.TelemetryTests.test_invalid_switches_refused_before_write) ... ok
test_io_failures_disable_once_and_baseexception_propagates (__main__.TelemetryTests.test_io_failures_disable_once_and_baseexception_propagates) ... ok
test_off_has_no_object_or_directory (__main__.TelemetryTests.test_off_has_no_object_or_directory) ... ok
test_scorer_ast_and_exact_inputs (__main__.TelemetryTests.test_scorer_ast_and_exact_inputs) ... ok
test_t8_serialized_wrong_answer_is_not_inert (__main__.TelemetryTests.test_t8_serialized_wrong_answer_is_not_inert) ... ok
test_telemetry_never_calls_operational_clock_or_writes_input_record (__main__.TelemetryTests.test_telemetry_never_calls_operational_clock_or_writes_input_record) ... ok
test_actual_cpu_update_direction_changes_fail_real_reader_repro_gate (__main__.TransportTests.test_actual_cpu_update_direction_changes_fail_real_reader_repro_gate) ... ok
test_completed_stage1_runner_to_reader_and_cpu_pt_transport (__main__.TransportTests.test_completed_stage1_runner_to_reader_and_cpu_pt_transport) ... ok
test_completed_three_stages_preserve_common_files_and_compute_real_repro (__main__.TransportTests.test_completed_three_stages_preserve_common_files_and_compute_real_repro) ... ok
test_real_scored_recipe_accounts_for_scientific_hook_readout_time (__main__.TransportTests.test_real_scored_recipe_accounts_for_scientific_hook_readout_time) ... ok
test_requested_stage_forecast_is_checked_before_dispatch_and_worker (__main__.TransportTests.test_requested_stage_forecast_is_checked_before_dispatch_and_worker) ... ok
test_saved_overlay_hash_is_the_immutable_serialized_bundle (__main__.TransportTests.test_saved_overlay_hash_is_the_immutable_serialized_bundle) ... ok
test_stage3_pair_mismatch_is_refused_in_parent_before_any_launch_write (__main__.TransportTests.test_stage3_pair_mismatch_is_refused_in_parent_before_any_launch_write) ... ok
test_stage3_telemetry_setting_cannot_change_after_stage2 (__main__.TransportTests.test_stage3_telemetry_setting_cannot_change_after_stage2) ... ok
test_tampered_stage2_pt_refuses_stage3_before_scientific_callbacks (__main__.TransportTests.test_tampered_stage2_pt_refuses_stage3_before_scientific_callbacks) ... ok
test_telemetry_off_on_transport_changes_only_T1_fields_at_every_stage (__main__.TransportTests.test_telemetry_off_on_transport_changes_only_T1_fields_at_every_stage) ... ok
test_wrong_stage3_predecessor_refuses_in_main_before_harness_or_supervisor (__main__.TransportTests.test_wrong_stage3_predecessor_refuses_in_main_before_harness_or_supervisor) ... ok

----------------------------------------------------------------------
Ran 285 tests in 22.478s

OK
{"launched": false, "reasons": ["missing/unknown/duplicate phases"], "status": "UNVERIFIED"}
ISOLATION OWNED LISTING DRIFT: []
ISOLATION OTHER OBSERVED UNATTRIBUTED: []
SYS_MODULES_FORBIDDEN: []
C10Y_DIRECTDW_SELFTEST PASS — CPU ONLY; LIVE LAW#3/LAW#5 UNVERIFIED
```

</details>

<details>
<summary>Full final targeted output</summary>

```text
test_actual_phase_collision_and_owned_context_tampering (c10y_directdw_selftest.PrefixPersistenceTests.test_actual_phase_collision_and_owned_context_tampering) ... ok
test_additional_original_gate_families_retain_inputs (c10y_directdw_selftest.PrefixPersistenceTests.test_additional_original_gate_families_retain_inputs) ... ok
test_baseline_helper_return_retained_before_later_arm_failure (c10y_directdw_selftest.PrefixPersistenceTests.test_baseline_helper_return_retained_before_later_arm_failure) ... ok
test_baseline_projector_and_planned_update_gates_keep_readouts (c10y_directdw_selftest.PrefixPersistenceTests.test_baseline_projector_and_planned_update_gates_keep_readouts) ... ok
test_calibration_forced_gates_retain_records_and_cleanup (c10y_directdw_selftest.PrefixPersistenceTests.test_calibration_forced_gates_retain_records_and_cleanup) ... ok
test_cleanup_only_and_primary_plus_cleanup_keep_partial_evidence (c10y_directdw_selftest.PrefixPersistenceTests.test_cleanup_only_and_primary_plus_cleanup_keep_partial_evidence) ... ok
test_executed_count_snapshot_retains_each_actual_count_operand (c10y_directdw_selftest.PrefixPersistenceTests.test_executed_count_snapshot_retains_each_actual_count_operand) ... ok
test_failed_exact_phase_checks_mark_incomplete (c10y_directdw_selftest.PrefixPersistenceTests.test_failed_exact_phase_checks_mark_incomplete) ... ok
test_helper_local_gradient_accumulation_and_ledger_gates (c10y_directdw_selftest.PrefixPersistenceTests.test_helper_local_gradient_accumulation_and_ledger_gates) ... ok
test_helper_local_parity_and_objective_offending_inputs (c10y_directdw_selftest.PrefixPersistenceTests.test_helper_local_parity_and_objective_offending_inputs) ... ok
test_inputs_durable_before_gate_and_phase_bytes_immutable (c10y_directdw_selftest.PrefixPersistenceTests.test_inputs_durable_before_gate_and_phase_bytes_immutable) ... ok
test_later_mode_halt_does_not_mark_unreached_arms_started (c10y_directdw_selftest.PrefixPersistenceTests.test_later_mode_halt_does_not_mark_unreached_arms_started) ... ok
test_malformed_baseline_preserves_law3_and_partial_records (c10y_directdw_selftest.PrefixPersistenceTests.test_malformed_baseline_preserves_law3_and_partial_records) ... ok
test_memory_floor_schema_and_budget_inputs_precede_original_gates (c10y_directdw_selftest.PrefixPersistenceTests.test_memory_floor_schema_and_budget_inputs_precede_original_gates) ... ok
test_nonfinite_gate_inputs_do_not_replace_original_halt (c10y_directdw_selftest.PrefixPersistenceTests.test_nonfinite_gate_inputs_do_not_replace_original_halt) ... ok
test_phase_collision_and_io_failure_restore_state (c10y_directdw_selftest.PrefixPersistenceTests.test_phase_collision_and_io_failure_restore_state) ... ok
test_prefix_final_collision_refuses_each_name_without_overwrite (c10y_directdw_selftest.PrefixPersistenceTests.test_prefix_final_collision_refuses_each_name_without_overwrite) ... ok
test_proof_early_exception_not_replaced_by_recording (c10y_directdw_selftest.PrefixPersistenceTests.test_proof_early_exception_not_replaced_by_recording) ... ok
test_recorder_restores_existing_none_attributes (c10y_directdw_selftest.PrefixPersistenceTests.test_recorder_restores_existing_none_attributes) ... ok
test_stage_halt_uses_same_partial_record_retention (c10y_directdw_selftest.PrefixPersistenceTests.test_stage_halt_uses_same_partial_record_retention) ... ok
test_success_final_serialization_matches_existing_schema (c10y_directdw_selftest.PrefixPersistenceTests.test_success_final_serialization_matches_existing_schema) ... ok
test_success_serializer_preserves_computed_values_and_exact_names (c10y_directdw_selftest.PrefixPersistenceTests.test_success_serializer_preserves_computed_values_and_exact_names) ... ok
test_target_partial_and_leakage_inputs_are_preserved (c10y_directdw_selftest.PrefixPersistenceTests.test_target_partial_and_leakage_inputs_are_preserved) ... ok
test_tensor_phase_records_use_binary_sidecars_without_list_expansion (c10y_directdw_selftest.PrefixPersistenceTests.test_tensor_phase_records_use_binary_sidecars_without_list_expansion) ... ok
test_unit_result_survives_post_action_memory_halt (c10y_directdw_selftest.PrefixPersistenceTests.test_unit_result_survives_post_action_memory_halt) ... ok

----------------------------------------------------------------------
Ran 25 tests in 3.881s

OK
ISOLATION/FORBIDDEN-MODULE CHECK: PASS
```

</details>

<details>
<summary>Full final prechange-comparison output</summary>

```text
runTest (__main__.Comparison.runTest) ... ok

----------------------------------------------------------------------
Ran 1 test in 0.237s

OK
PRECHANGE/CURRENT: all six final names, JSON schema/values, tensor values equal; fixed clocks/CPU leaves
ISOLATION/FORBIDDEN-MODULE CHECK: PASS
```

</details>

<details>
<summary>Full static/file audit output</summary>

```text
{
  "Writer_AST": "UNCHANGED",
  "changed_existing_symbols": [
    "Budget",
    "_accumulation_check",
    "_gradient_check",
    "_ledger_call",
    "_objective_audit",
    "_unit",
    "_write_proof",
    "calibrate",
    "exception_fields",
    "instrument_prefix",
    "persist_prefix",
    "run",
    "sample_memory",
    "train_deploy_parity"
  ],
  "changed_owned": [
    "experiments/track_c/c10y_directdw_arms.py",
    "experiments/track_c/c10y_directdw_selftest.py"
  ],
  "cleanup_AST": "UNCHANGED; proof recorder appended after original cleanup",
  "current_prereg_sha256": "005391a39e31d8174419de3e39078a42209ded1b7ab8caaf098d5d8a4f755004",
  "final_sha256": {
    "experiments/track_c/c10y_directdw_arms.py": "ead3cef2266a7c81035e5acb6c3a97b42f83da556ba093a9fd28ec403f7e158c",
    "experiments/track_c/c10y_directdw_selftest.py": "81f3c07ec36fe1aa10bf31526f712cb3b015b0a86f714ba7aa3123a81875dd25"
  },
  "historical_changes": {
    "results/c10y_directdw_calib4/precast_scope_astra.log": {
      "after": "7c0ff14f828335052854d9c7363414f93273db28e18ba5600d415f392f5a7b95",
      "before": "7d78e3b4a181f4784581152473e096479eacf70ee4ee2de85da6a52f51a658be"
    }
  },
  "historical_paths_unchanged": 57,
  "original_gate_condition_AST": "UNCHANGED (source_end binding normalized)",
  "protected_paths": 194,
  "protected_unchanged": 192,
  "science_call_AST": "UNCHANGED"
}
```

</details>

<details>
<summary>Full Astra implementation review (chronology retained)</summary>

# C10Y recordfix implementation review

## Review 1 — initial implementation, 269-test suite

**FIX-FIRST.** The broad architecture follows ruling 3, but two concrete exception/status defects and incomplete baseline retention remain. The new tests do not yet establish the full acceptance claims.

Scope: read-only comparison against `/private/tmp/c10y_build/recordfix_20261009/arms_before.py` and `selftest_before.py`; inspected actual source, new test bodies and saved logs. No Python, torch/model/tokenizer imports, tests, GPU, launches, commits, or workspace writes performed by this reviewer. Same-family GPT review provides weaker independence. Citations refer to the initial implementation inspected in this pass.

### Blocking findings

1. **Malformed LAW#3 input changes the original outcome.** `_retain_prefix` unconditionally reads `state['baseline']['law5']` inside its exception handler (`experiments/track_c/c10y_directdw_arms.py:1352–1353`). A baseline with arms/metrics but missing `law5` correctly raises `Halt('LAW#3', {'baseline': ..., 'missing': ...})` in the original gate; the new handler then raises `KeyError('law5')` before attaching `_c10y_prefix`. The caller records INSTRUMENT-ERROR, loses partial state and misses the LAW#3 schedule latch. Guard missing fields without inventing a standing result. Add a real-prefix malformed-baseline test asserting exact original code/detail/phase, schedule latch, retained rows, and cleanup.

2. **Check statuses are inferred from unrelated global phase names.** The fallback at `:1356–1358` uses any `phase.startswith(name+'_')` across all arms/modes. Exact phase names `objective` (`:2447`) and `smoke` (`:2842`) never match; their failed checks become NOT-RUN despite execution. A previously executed arm/mode can instead make an unreached later check INCOMPLETE. Track explicit scope and start/completion state for each `(mode, arm, check)`; do not guess from a global string prefix. Add objective/smoke failure tests and a stage-2 later-arm/mode HALT test proving exact unreached statuses and no false `passed=True`.

3. **Partial baseline evidence is still lost.** `progress['baseline']` is bound only after `scored_recipe` returns (`:2696–2699`). Already-computed standing LAW#5/evaluation results inside the timed baseline wrappers, and completed earlier-arm rows, do not reach progress or snapshots if a later arm/helper/cleanup raises. This is the same loss pattern at a nested boundary. Persist the actual returned standing/evaluation/arm records at their construction points before subsequent gates, without recomputing or changing the final success record. Force a baseline failure after an earlier arm has completed and prove those exact values survive.

4. **Acceptance tests leave major claims unproved.** The fixture substitutes `_write_proof`, `_gradient_check`, `_objective_audit`, and `_accumulation_check` (`c10y_directdw_selftest.py:4924–4927`). `test_helper_local_gates_have_prevalidation_record_hooks` merely checks source contains `_prefix_snapshot(` (`:5055–5058`); this cannot prove ordering, offending-input identity, exception preservation, or cleanup. `test_phase_collision_and_io_failure_restore_state` (`:5006`) only injects an OSError, with no pre-existing phase file. The success test (`:5060`) checks selected fields but never compares old and new successful final payloads. Add focused real helper-gate regressions, actual phase collision, cleanup-only and primary-plus-cleanup failure, owned-context tampering/rerun collision, and a prechange/final payload comparison under fixed clocks. Reuse the existing three-stage common-byte test for supported ownership reuse. At minimum exercise every explicit prefix gate family, including EXECUTED-LOOP-COUNT, memory malformed/resource inputs, restoration/smoke/source drift and ordinary exceptions, with the scientific gate expressions unchanged.

### Positive findings and limits

- Diff inspection finds additive serialization hooks and one source-hash local binding; no changed solve, distance, norm, threshold, arithmetic, or numerical gate expression. The prevalidation memory hook keeps the existing memory aggregate update order. This is static evidence, not MPS equivalence.
- Phase files use the existing exclusive `write_json` flush/fsync primitive. Final artifact prechecks reject unowned existing names; canonical later-stage common-file ownership is anchored to predecessor manifest hashes. Finite successful payloads are passed unchanged by `persist_prefix`.
- Tagged NaN/Inf snapshot encoding avoids the demonstrated JSON-serialization-before-capture-HALT failure. The new nonfinite test covers that path. `exception_fields` now encodes nonfinite detail for durable JSON; this is a deliberate record representation change, while the raised scientific exception retains its raw input.
- The outer decorator receives exceptions after the original prefix `finally`, a sound way to retain cleanup-chain context. Its correctness is still conditional on removing the handler defect and adding the missing cleanup regressions. Existing restored H/budget attributes also need an explicit test, including prior attributes set to None.
- Every snapshot currently copies the entire accumulated non-tensor record state (`arms.py:1338–1343`) on every memory/budget callback. This can multiply disk work substantially as target stdout and baseline readouts grow. Prefer phase-local inputs plus durable references or milestone aggregates where possible. Production timing/resource effects remain unmeasured; no admission is justified by CPU tests.

### Evidence inspected

| Saved log | Observed result | Interpretation |
|---|---|---|
| `before_contract_suite.log` | 260 tests, 18.571 s, OK; no observed isolation drift/forbidden modules | Legacy-contract fixture baseline; production pins unchanged |
| `red_complete.log` | 9 tests, 0.553 s, 25 assertion failures | Regression RED before implementation; earlier fixture-error logs preserved separately |
| `green1.log` | 9 tests, 3.135 s, OK | Narrow new CPU fixture coverage |
| `full1.log` | 269 tests, 21.868 s, OK; no observed isolation drift/forbidden modules | Full current fixture suite PASS, with gaps above |

These outputs were read, not rerun by the reviewer. The initial current-source baseline failure caused by appended prereg §12 must remain in the builder report; the byte-verified historical fixture setup is not current production admission. All live model/MPS/science behavior remains UNVERIFIED. No calibration 5 or stage dispatch authorized.

## Review 2 — corrected retention and 20-test targeted suite

**FIX-FIRST, narrowed to serialization scale, early-proof status, and self-contained verification.** Review 1's malformed-baseline exception defect, global status inference, and loss of earlier baseline helper returns are corrected in the inspected source. New behavioral tests exercise malformed LAW#3, partial baseline, objective/smoke status, later-mode scope, actual phase collision/context tampering, cleanup-only/primary-plus-cleanup, and existing None attributes. Helper tests now invoke the real gradient/accumulation/ledger/parity/objective gates with controlled numerical leaves. These are meaningful improvements over source-string checks.

The additional `_unit` return record correctly precedes its existing post-action memory cleanup. `_write_proof` now tolerates absent timing attributes on an early writer exception. Static diff review still finds no changed scientific arithmetic, tolerance, or gate expression; computing `source_end` once preserves the prior source-hash check. IO adds wall-clock time and transfers, so unchanged live timing/resource outcomes are not established.

### Remaining findings

1. **Full dense tensors are expanded into JSON Python scalars.** `_record_value` uses `tensor.detach().cpu().tolist()` and `_unit` now sends every return through it, including baseline projectors, capture factors and gradients; baseline-write records also contain full planned and actual matrices. The pinned model config has `hidden_size=2048`, `intermediate_size=11008` (`hf_cache/hub/models--Qwen--Qwen2.5-3B/snapshots/3aab1f1954e9cc14eb9509a215f9e5ca08227a9b/config.json:9–11`), and hparams select five down-projection layers (`configs/hparams/qwen25_3b_memit_hparams.json:2`, `:15`). Five dense projectors therefore contain **605,880,320 elements**. The generic unit-return snapshot expands all of these into a huge nested Python structure, and the timed baseline wrapper records the same projector again. The 4×4 fixtures cannot expose this host-memory amplification. Retain required tensor values through existing exclusive durable binary tensor sidecars with JSON references, or narrow generic return recording to the already required scalar records. Do not compute new summaries/statistics. Add a structural/CPU test that proves tensor recording does not call `tolist` or expand values into JSON; prove sidecar equality and collision refusal if sidecars are chosen.

2. **Early proof parity still uses `{}`.** The new timing defaults explicitly say NOT-RUN, but `getattr(writer,'parity',{})` remains in `_write_proof` cleanup. The added early-exception test only checks the phase name. Supply explicit NOT-RUN parity (and phase context) when no parity ran, and assert all unreached proof fields are truthful. Existing empty list/dict defaults must not substitute for unexecuted check status.

3. **The new repository test depends on an ephemeral scratch file.** `test_success_matches_verified_prechange_prefix_output` reads `/private/tmp/c10y_build/recordfix_20261009/arms_before.py` by default. A clean checkout or scratch cleanup therefore breaks the full selftest suite. Keep this byte-verified comparison as a separately documented scratch acceptance check, with a self-contained golden fixture regression in the repository test, or provide the frozen comparator through an allowed durable test fixture. Its present comparison executes old `instrument_prefix` with current helpers and current `persist_prefix` on both sides; that establishes prefix-output equivalence on the fixture, not an independent old/new serialization comparison. Use the verified old persistence function too, or state this limitation precisely.

### Additional evidence read

| Log | Result |
|---|---|
| `red_review1.log` | 13 tests, 4.769 s, 5 assertion failures, including LAW#3 replaced by INSTRUMENT-ERROR |
| `green_review1.log` | 13 tests, 1.623 s, OK |
| `red_review2.log` | 18 tests, 2.018 s, 1 assertion failure and 1 error: missing post-action return record; recording replaced early writer failure with AttributeError |
| `green_review2.log` | 20 tests, 2.371 s, OK; isolation/forbidden-module check PASS |

The builder is adding remaining gate-family cases and will run the expanded full suite; neither is yet claimed complete in this review. Review chronology remains preserved above. No live/model/MPS execution or admission authorized.

## Review 3 — binary phase sidecars and expanded full suite

The three Review 2 blockers are corrected in source: phase tensors use exclusive durable binary sidecars with JSON member/dtype/shape and SHA references; dense projector phases record the already-used presence input; early proof parity has explicit NOT-RUN; and the permanent success test has no scratch-baseline dependency. The separate scratch comparator now compiles both byte-verified old `instrument_prefix` and old `persist_prefix`, using shared current numerical helpers/CPU leaves and fixed clocks. Its evidence establishes six final artifact names and JSON/tensor payload equality for that fixture, not MPS or production timing equality.

Read evidence: `green_review3.log` reports 23 targeted tests, 3.824 s, OK. `prechange_equivalence.log` reports 1 comparison, 0.239 s, OK. `full2.log` reports **284 tests, 22.248 s, OK**, zero observed isolation listing drift and no forbidden modules. The permanent 284-test suite uses the new self-contained serializer fixture; the earlier 23-test log still included the now-extracted historical comparator. The red tensor-list-expansion and early-parity failures are preserved in `red_review3.log`; its third failure was a separately corrected source-drift fixture condition.

Final small corrections requested before acceptance:

- Cover a pre-existing `.pt` phase sidecar in the existing collision test, not only `.json`; assert unchanged bytes and no newly created sibling. Source already prechecks both names, so no production change is indicated by this gap.
- The `executed_loop_count` snapshot records expected `forced_iterations`, proof and parity, but omits the actual `writer.last_trace['accepted_steps']` and `len(writer.trajectory)` used by the immediately following gate. Preserve those two existing observations in the snapshot envelope, without changing gate expressions or exception detail; force each mismatch independently in a regression. Otherwise a HALT caused only by one of these operands lacks its offending count in the durable record.

No other production blocker identified in this pass. Static scientific arithmetic/gate-expression comparison remains unchanged. Binary recording can still add device transfers and disk IO; live performance/resource behavior remains unmeasured and future admission remains separately gated. Reviewed driver SHA before these final additions: `b31a581ba61b70696c13155b2fa83be1e65d6819a6a4a52bcc70a1d4038c867a`; prereg remained `005391a39e31d8174419de3e39078a42209ded1b7ab8caaf098d5d8a4f755004`.

## Final disposition — PROCEED for record-only build acceptance

**PROCEED. No outstanding implementation blocker identified within the record-only scope.** Both final corrections are present and tested: the executed-loop phase envelope preserves the actual accepted-step and trajectory counts while the gate and exception detail remain unchanged (`c10y_directdw_arms.py:2810–2813`); the collision test independently covers JSON and tensor sidecars, preserves old bytes and asserts no sibling creation (`c10y_directdw_selftest.py:5143–5156`).

The count-operand regression was RED first (`red_count_operands.log`: 1 test, 0.277 s, 2 assertion failures). Final targeted evidence is **25 tests PASS in 3.881 s** (`green_final.log`); final full evidence is **285 tests PASS in 22.478 s** (`full_final.log`), with empty observed owned/unattributed sink-listing drift and no forbidden modules. These logs were read by the reviewer; no tests were executed by the reviewer. No extra rerun of the historical comparator is required solely for the final two scalar snapshot fields: they affect only added phase records, and the final serializer regression/full suite passes. The earlier six-artifact comparison's limits remain as recorded in Review 3.

Read `scope_audit.py`, its log and JSON. The saved audit finds unchanged Writer AST, original gate conditions (normalizing only the `source_end` binding), selected scientific-call ASTs, original prefix/unit cleanup bodies, and the original proof cleanup followed by the added record hook. Its selected-call comparison is a multiset check; unchanged scientific ordering is additionally supported by direct diff inspection, not claimed from that counter alone. Of 194 protected paths, 192 remained unchanged and exactly the two authorized driver/test files changed. Historical manifest comparison reports 57 of 58 unchanged: `results/c10y_directdw_calib4/precast_scope_astra.log` changed concurrently. The builder reports this was another session's append; this reviewer did not independently establish authorship. Do not claim the entire historical tree was unchanged. No historical science JSON/tensor/diagnostic change appears in the audited manifest.

Final file hashes independently reread with `shasum -a 256`:

| File | SHA-256 |
|---|---|
| `experiments/track_c/c10y_directdw_arms.py` | `ead3cef2266a7c81035e5acb6c3a97b42f83da556ba093a9fd28ec403f7e158c` |
| `experiments/track_c/c10y_directdw_selftest.py` | `81f3c07ec36fe1aa10bf31526f712cb3b015b0a86f714ba7aa3123a81875dd25` |
| `docs/C10Y_DIRECTDW_PREREG.md` | `005391a39e31d8174419de3e39078a42209ded1b7ab8caaf098d5d8a4f755004` |

Acceptance is limited to persistence/serialization and CPU fixture evidence. The unchanged old production prereg pins still do not admit the appended §12 document; repinning is outside this correction. Binary sidecars avoid Python-scalar amplification but still add IO/device transfers. Live memory/timing effects, model/MPS behavior and all science gates remain **UNVERIFIED**. This same-family review and record-only correction authorize **no calibration 5, stage dispatch, causal numerical conclusion, or F1 closure**. The named build report remains the builder's final deliverable.

</details>
