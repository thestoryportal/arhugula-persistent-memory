DONE

## Test list mapped to prereg lines

| Brief test | Selftest | Prereg lines enforced |
| --- | --- | --- |
| a | test_nonadmitted_seven_record_regression_retains_replication_without_a_count | docs/C10U_MINT2_PREREG.md:72, 76, 78, 81, 115, 179 |
| b | test_nonadmitted_p3_screen_is_recomputed_at_22_and_exact_098 | docs/C10U_MINT2_PREREG.md:72, 90, 115 |
| c | test_nonadmitted_rejects_behavioral_keys_positive_pid_multi_and_failed_p2 | docs/C10U_MINT2_PREREG.md:69–73, 76, 90, 115 |
| d | test_nonadmitted_does_not_weaken_done_pid_or_unknown_outcome_gates | docs/C10U_MINT2_PREREG.md:78, 90, 115 |
| e | test_nonadmitted_mint1_in_frozen_block_fails_law3 | docs/C10U_MINT2_PREREG.md:77, 115, 175 |
| f | test_nonadmitted_replication_pairs_record_underfit_done_in_both_directions | docs/C10U_MINT2_PREREG.md:63, 67, 72, 78, 92, 115 |
| g | test_nonadmitted_p4_selection_skips_unexecuted_modifier | docs/C10U_MINT2_PREREG.md:86, 92, 115 |
| h | test_nonadmitted_json_round_trip_keeps_block_reading | docs/C10U_MINT2_PREREG.md:72, 115, 180 |
| Admission/provenance preservation | test_nonadmitted_keeps_material_and_p2_audits | docs/C10U_MINT2_PREREG.md:63, 67, 70–71, 90 |
| Admission/provenance preservation | test_nonadmitted_rejects_malformed_p3_and_recomputes_i11 | docs/C10U_MINT2_PREREG.md:72–73, 90, 115 |
| Admission/provenance preservation | test_nonadmitted_replication_still_rejects_material_and_init_mismatches | docs/C10U_MINT2_PREREG.md:63, 67, 78, 90 |
| Executed-process preservation | test_nonadmitted_population_checks_pids_only_for_executed_runs | docs/C10U_MINT2_PREREG.md:78, 90, 115 |
| V2 replication/control | test_nonadmitted_v2_keeps_replication_and_blocks_control | docs/C10U_MINT2_PREREG.md:72, 76, 78, 95, 115, 179 |
| a (real producer) | test_nonadmitted_real_producer_record_retains_seven_replication_jobs | docs/C10U_MINT2_PREREG.md:71–73, 76, 78, 90, 115, 179 |
| Follow-up producer proof and child log | test_nonadmitted_behavior_child_logs_and_parent_accepts | docs/C10U_MINT2_PREREG.md:71–73, 90, 115 |

## RED output — initial reader regression

```text
$ /opt/homebrew/bin/rtk proxy .venv/bin/python -B experiments/track_c/c10u_mint2_selftest.py
test_aenv_baseline_boundaries_in_both_blocks_and_replicates (__main__.AenvTests.test_aenv_baseline_boundaries_in_both_blocks_and_replicates) ... ok
test_aenv_envelope_review_counterexamples_keep_null_precedence (__main__.AenvTests.test_aenv_envelope_review_counterexamples_keep_null_precedence) ... ok
test_aenv_halt_stops_both_blocks_in_initial_and_replication_stages (__main__.AenvTests.test_aenv_halt_stops_both_blocks_in_initial_and_replication_stages) ... ok
test_aenv_null_boundaries_and_replication_exclusion (__main__.AenvTests.test_aenv_null_boundaries_and_replication_exclusion) ... ok
test_aenv_r1_counts_pass_a4_and_fail_original_window_without_reading_r1 (__main__.AenvTests.test_aenv_r1_counts_pass_a4_and_fail_original_window_without_reading_r1) ... ok
test_aenv_replica_compatibility_can_overturn_positive_routing (__main__.AenvTests.test_aenv_replica_compatibility_can_overturn_positive_routing) ... ok
test_aenv_schedule_keeps_reference_and_negative_direction_replication (__main__.AenvTests.test_aenv_schedule_keeps_reference_and_negative_direction_replication) ... ok
test_aenv_source_identity_pins_amended_prereg_reader_and_driver (__main__.AenvTests.test_aenv_source_identity_pins_amended_prereg_reader_and_driver) ... ok
test_aenv_stage_completion_round_trips_missing_and_replication_missing (__main__.AenvTests.test_aenv_stage_completion_round_trips_missing_and_replication_missing) ... ok
test_aenv_truth_table_verbatim_through_range_and_replication (__main__.AenvTests.test_aenv_truth_table_verbatim_through_range_and_replication) ... ok
test_nonadmitted_does_not_weaken_done_pid_or_unknown_outcome_gates (__main__.NonadmittedTests.test_nonadmitted_does_not_weaken_done_pid_or_unknown_outcome_gates) ... ok
test_nonadmitted_json_round_trip_keeps_block_reading (__main__.NonadmittedTests.test_nonadmitted_json_round_trip_keeps_block_reading) ... FAIL
test_nonadmitted_keeps_material_and_p2_audits (__main__.NonadmittedTests.test_nonadmitted_keeps_material_and_p2_audits) ... ok
test_nonadmitted_mint1_in_frozen_block_fails_law3 (__main__.NonadmittedTests.test_nonadmitted_mint1_in_frozen_block_fails_law3) ... 
  test_nonadmitted_mint1_in_frozen_block_fails_law3 (__main__.NonadmittedTests.test_nonadmitted_mint1_in_frozen_block_fails_law3) (replicate=0) ... FAIL
  test_nonadmitted_mint1_in_frozen_block_fails_law3 (__main__.NonadmittedTests.test_nonadmitted_mint1_in_frozen_block_fails_law3) (replicate=1) ... FAIL
test_nonadmitted_p3_screen_is_recomputed_at_22_and_exact_098 (__main__.NonadmittedTests.test_nonadmitted_p3_screen_is_recomputed_at_22_and_exact_098) ... 
  test_nonadmitted_p3_screen_is_recomputed_at_22_and_exact_098 (__main__.NonadmittedTests.test_nonadmitted_p3_screen_is_recomputed_at_22_and_exact_098) (nfit=17) ... FAIL
  test_nonadmitted_p3_screen_is_recomputed_at_22_and_exact_098 (__main__.NonadmittedTests.test_nonadmitted_p3_screen_is_recomputed_at_22_and_exact_098) (nfit=21) ... FAIL
test_nonadmitted_p3_screen_is_recomputed_at_22_and_exact_098 (__main__.NonadmittedTests.test_nonadmitted_p3_screen_is_recomputed_at_22_and_exact_098) ... FAIL
test_nonadmitted_p4_selection_skips_unexecuted_modifier (__main__.NonadmittedTests.test_nonadmitted_p4_selection_skips_unexecuted_modifier) ... ERROR
test_nonadmitted_population_checks_pids_only_for_executed_runs (__main__.NonadmittedTests.test_nonadmitted_population_checks_pids_only_for_executed_runs) ... FAIL
test_nonadmitted_rejects_behavioral_keys_positive_pid_multi_and_failed_p2 (__main__.NonadmittedTests.test_nonadmitted_rejects_behavioral_keys_positive_pid_multi_and_failed_p2) ... ok
test_nonadmitted_rejects_malformed_p3_and_recomputes_i11 (__main__.NonadmittedTests.test_nonadmitted_rejects_malformed_p3_and_recomputes_i11) ... ok
test_nonadmitted_replication_pairs_record_underfit_done_in_both_directions (__main__.NonadmittedTests.test_nonadmitted_replication_pairs_record_underfit_done_in_both_directions) ... 
  test_nonadmitted_replication_pairs_record_underfit_done_in_both_directions (__main__.NonadmittedTests.test_nonadmitted_replication_pairs_record_underfit_done_in_both_directions) (outcomes=('UNDERFIT', 'DONE')) ... FAIL
  test_nonadmitted_replication_pairs_record_underfit_done_in_both_directions (__main__.NonadmittedTests.test_nonadmitted_replication_pairs_record_underfit_done_in_both_directions) (outcomes=('DONE', 'UNDERFIT')) ... FAIL
  test_nonadmitted_replication_pairs_record_underfit_done_in_both_directions (__main__.NonadmittedTests.test_nonadmitted_replication_pairs_record_underfit_done_in_both_directions) (outcomes=('UNDERFIT', 'UNDERFIT')) ... FAIL
test_nonadmitted_replication_still_rejects_material_and_init_mismatches (__main__.NonadmittedTests.test_nonadmitted_replication_still_rejects_material_and_init_mismatches) ... ok
test_nonadmitted_seven_record_regression_retains_replication_without_a_count (__main__.NonadmittedTests.test_nonadmitted_seven_record_regression_retains_replication_without_a_count) ... FAIL
test_nonadmitted_v2_keeps_replication_and_blocks_control (__main__.NonadmittedTests.test_nonadmitted_v2_keeps_replication_and_blocks_control) ... 
  test_nonadmitted_v2_keeps_replication_and_blocks_control (__main__.NonadmittedTests.test_nonadmitted_v2_keeps_replication_and_blocks_control) (index=1) ... FAIL
  test_nonadmitted_v2_keeps_replication_and_blocks_control (__main__.NonadmittedTests.test_nonadmitted_v2_keeps_replication_and_blocks_control) (index=4) ... FAIL
test_a1_68_boundary_and_missing_shape_fail_closed (__main__.ReaderTests.test_a1_68_boundary_and_missing_shape_fail_closed) ... ok
test_admission_22_values_and_per_position_underfit_remain_distinct (__main__.ReaderTests.test_admission_22_values_and_per_position_underfit_remain_distinct) ... ok
test_bigram_shape_rejects_missing_duplicate_or_invalid_fraction (__main__.ReaderTests.test_bigram_shape_rejects_missing_duplicate_or_invalid_fraction) ... ok
test_bigram_uses_fact_union_and_zero_correct_is_no_continuation (__main__.ReaderTests.test_bigram_uses_fact_union_and_zero_correct_is_no_continuation) ... ok
test_block_rejects_changed_context_data_and_pairing (__main__.ReaderTests.test_block_rejects_changed_context_data_and_pairing) ... ok
test_blocked_direction_has_no_pending_control (__main__.ReaderTests.test_blocked_direction_has_no_pending_control) ... ok
test_blocks_never_pool_or_recover_missing_seed (__main__.ReaderTests.test_blocks_never_pool_or_recover_missing_seed) ... ok
test_cli_reads_only_records_and_excludes_context_bootstrap (__main__.ReaderTests.test_cli_reads_only_records_and_excludes_context_bootstrap) ... ok
test_complete_record_and_raw_minus_pre_binding (__main__.ReaderTests.test_complete_record_and_raw_minus_pre_binding) ... ok
test_contains_allows_alternative_ids_and_startswith_is_separate (__main__.ReaderTests.test_contains_allows_alternative_ids_and_startswith_is_separate) ... ok
test_control_spending_requires_a_routable_valid_span_block (__main__.ReaderTests.test_control_spending_requires_a_routable_valid_span_block) ... ok
test_control_uses_the_registered_initial_comparison_not_an_extra_replica_control (__main__.ReaderTests.test_control_uses_the_registered_initial_comparison_not_an_extra_replica_control) ... ok
test_direction_keeps_candidate_large_write_and_bigram_qualifiers (__main__.ReaderTests.test_direction_keeps_candidate_large_write_and_bigram_qualifiers) ... ok
test_full_fourteen_schedule_and_conditional_stages (__main__.ReaderTests.test_full_fourteen_schedule_and_conditional_stages) ... ok
test_geometry_collapse_boundaries_are_diagnostic (__main__.ReaderTests.test_geometry_collapse_boundaries_are_diagnostic) ... ok
test_hashes_context_and_row_counts_are_recomputed (__main__.ReaderTests.test_hashes_context_and_row_counts_are_recomputed) ... ok
test_i11_admission_boundaries_and_geometry_is_diagnostic (__main__.ReaderTests.test_i11_admission_boundaries_and_geometry_is_diagnostic) ... ok
test_inertness_fingerprint_and_override_audits_reject_tampering (__main__.ReaderTests.test_inertness_fingerprint_and_override_audits_reject_tampering) ... ok
test_inertness_precision_gate (__main__.ReaderTests.test_inertness_precision_gate) ... ok
test_large_write_is_qualifier_not_gate (__main__.ReaderTests.test_large_write_is_qualifier_not_gate) ... ok
test_law3_miss_suspends_frozen_block (__main__.ReaderTests.test_law3_miss_suspends_frozen_block) ... ok
test_law3_seed_envelopes_median_and_multi_envelope (__main__.ReaderTests.test_law3_seed_envelopes_median_and_multi_envelope) ... ok
test_locality_boundaries_and_falsefires (__main__.ReaderTests.test_locality_boundaries_and_falsefires) ... ok
test_malformed_block_objects_fail_closed_without_raising (__main__.ReaderTests.test_malformed_block_objects_fail_closed_without_raising) ... ok
test_mechanism_curve_respects_first_position_loss_without_a_percentage_cutoff (__main__.ReaderTests.test_mechanism_curve_respects_first_position_loss_without_a_percentage_cutoff) ... ok
test_missing_norm_layer_and_empty_p2_rows_are_invalid (__main__.ReaderTests.test_missing_norm_layer_and_empty_p2_rows_are_invalid) ... ok
test_modifier_recovery_truth_table_frozen_at_v3 (__main__.ReaderTests.test_modifier_recovery_truth_table_frozen_at_v3) ... ok
test_not_comparable_and_underfit_precede_direction (__main__.ReaderTests.test_not_comparable_and_underfit_precede_direction) ... ok
test_null_band_precedes_gain_and_tradeoff_uses_binding (__main__.ReaderTests.test_null_band_precedes_gain_and_tradeoff_uses_binding) ... ok
test_p4_full_sequences_gate_and_q4_correctness_is_report_only (__main__.ReaderTests.test_p4_full_sequences_gate_and_q4_correctness_is_report_only) ... ok
test_p4_reports_fp16_gguf_to_q4_survival_with_its_own_denominator (__main__.ReaderTests.test_p4_reports_fp16_gguf_to_q4_survival_with_its_own_denominator) ... ok
test_p4_tokenizer_population_and_subject_specific_ids_fail_closed (__main__.ReaderTests.test_p4_tokenizer_population_and_subject_specific_ids_fail_closed) ... ok
test_pair_nonoverlap_rule_and_seed_range (__main__.ReaderTests.test_pair_nonoverlap_rule_and_seed_range) ... ok
test_public_readings_round_trip_as_strict_json (__main__.ReaderTests.test_public_readings_round_trip_as_strict_json) ... ok
test_reference_and_i11_helpers_keep_known_baseline_and_whole_recall (__main__.ReaderTests.test_reference_and_i11_helpers_keep_known_baseline_and_whole_recall) ... ok
test_replica_locality_miss_prevents_replication (__main__.ReaderTests.test_replica_locality_miss_prevents_replication) ... ok
test_replication_uses_same_seed_context_rows_and_fresh_pid (__main__.ReaderTests.test_replication_uses_same_seed_context_rows_and_fresh_pid) ... ok
test_reproduction_provenance_is_checked_before_any_new_arm (__main__.ReaderTests.test_reproduction_provenance_is_checked_before_any_new_arm) ... ok
test_span_requires_replication_and_matched48_control (__main__.ReaderTests.test_span_requires_replication_and_matched48_control) ... ok
test_string_below_full_invalid_even_when_binding_is_lead (__main__.ReaderTests.test_string_below_full_invalid_even_when_binding_is_lead) ... ok
test_underfit_mask_is_reported_without_changing_binding (__main__.ReaderTests.test_underfit_mask_is_reported_without_changing_binding) ... ok
test_conditional_empty_stage_refuses_before_any_marker (__main__.SafetyTests.test_conditional_empty_stage_refuses_before_any_marker) ... ok
test_import_does_not_load_runtime (__main__.SafetyTests.test_import_does_not_load_runtime) ... ok
test_nonadmitted_behavior_child_logs_and_parent_accepts (__main__.SafetyTests.test_nonadmitted_behavior_child_logs_and_parent_accepts) ... ok
test_p2_audits_the_engine_default_tokenizer_call (__main__.SafetyTests.test_p2_audits_the_engine_default_tokenizer_call) ... ok
test_p2_audits_two_ids_and_all_720_bigram_prompts (__main__.SafetyTests.test_p2_audits_two_ids_and_all_720_bigram_prompts) ... ok
test_p2_checks_the_whole_modifier_target_even_when_last_id_matches (__main__.SafetyTests.test_p2_checks_the_whole_modifier_target_even_when_last_id_matches) ... ok
test_p2_detects_runtime_context_retokenization (__main__.SafetyTests.test_p2_detects_runtime_context_retokenization) ... ok
test_p4_selection_requires_replication_and_comparability (__main__.SafetyTests.test_p4_selection_requires_replication_and_comparability) ... ok
test_preflight_rejects_inherited_knobs_before_external_calls (__main__.SafetyTests.test_preflight_rejects_inherited_knobs_before_external_calls) ... ok
test_write_json_is_exclusive_and_rereads_exact_payload (__main__.SafetyTests.test_write_json_is_exclusive_and_rereads_exact_payload) ... ok

======================================================================
ERROR: test_nonadmitted_p4_selection_skips_unexecuted_modifier (__main__.NonadmittedTests.test_nonadmitted_p4_selection_skips_unexecuted_modifier)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_selftest.py", line 732, in test_nonadmitted_p4_selection_skips_unexecuted_modifier
    selected = A.p4_configurations(a + b)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_arms.py", line 957, in p4_configurations
    raise ValueError("P4 requires replicated LEAD/PARTIAL mint-2 or modifier configuration")
ValueError: P4 requires replicated LEAD/PARTIAL mint-2 or modifier configuration

======================================================================
FAIL: test_nonadmitted_json_round_trip_keeps_block_reading (__main__.NonadmittedTests.test_nonadmitted_json_round_trip_keeps_block_reading)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_selftest.py", line 720, in test_nonadmitted_json_round_trip_keeps_block_reading
    self.assertEqual(reading["direction"], "ROUTING-BLOCKED-UNDERFIT")
AssertionError: 'INVALID' != 'ROUTING-BLOCKED-UNDERFIT'
- INVALID
+ ROUTING-BLOCKED-UNDERFIT


======================================================================
FAIL: test_nonadmitted_mint1_in_frozen_block_fails_law3 (__main__.NonadmittedTests.test_nonadmitted_mint1_in_frozen_block_fails_law3) (replicate=0)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_selftest.py", line 665, in test_nonadmitted_mint1_in_frozen_block_fails_law3
    self.assertEqual(reading["direction"], "HALT-LAW3")
AssertionError: 'INVALID' != 'HALT-LAW3'
- INVALID
+ HALT-LAW3


======================================================================
FAIL: test_nonadmitted_mint1_in_frozen_block_fails_law3 (__main__.NonadmittedTests.test_nonadmitted_mint1_in_frozen_block_fails_law3) (replicate=1)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_selftest.py", line 665, in test_nonadmitted_mint1_in_frozen_block_fails_law3
    self.assertEqual(reading["direction"], "HALT-LAW3")
AssertionError: 'INVALID' != 'HALT-LAW3'
- INVALID
+ HALT-LAW3


======================================================================
FAIL: test_nonadmitted_p3_screen_is_recomputed_at_22_and_exact_098 (__main__.NonadmittedTests.test_nonadmitted_p3_screen_is_recomputed_at_22_and_exact_098) (nfit=17)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_selftest.py", line 600, in test_nonadmitted_p3_screen_is_recomputed_at_22_and_exact_098
    self.assertEqual(not R._population([record], "F", 0)["reasons"], valid)
AssertionError: False != True

======================================================================
FAIL: test_nonadmitted_p3_screen_is_recomputed_at_22_and_exact_098 (__main__.NonadmittedTests.test_nonadmitted_p3_screen_is_recomputed_at_22_and_exact_098) (nfit=21)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_selftest.py", line 600, in test_nonadmitted_p3_screen_is_recomputed_at_22_and_exact_098
    self.assertEqual(not R._population([record], "F", 0)["reasons"], valid)
AssertionError: False != True

======================================================================
FAIL: test_nonadmitted_p3_screen_is_recomputed_at_22_and_exact_098 (__main__.NonadmittedTests.test_nonadmitted_p3_screen_is_recomputed_at_22_and_exact_098)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_selftest.py", line 603, in test_nonadmitted_p3_screen_is_recomputed_at_22_and_exact_098
    self.assertEqual(R._population([record], "F", 0)["reasons"], [])
AssertionError: Lists differ: ['incomplete/malformed/invalid run: process/replicate malformed'] != []

First list contains 1 additional elements.
First extra element 0:
'incomplete/malformed/invalid run: process/replicate malformed'

- ['incomplete/malformed/invalid run: process/replicate malformed']
+ []

======================================================================
FAIL: test_nonadmitted_population_checks_pids_only_for_executed_runs (__main__.NonadmittedTests.test_nonadmitted_population_checks_pids_only_for_executed_runs)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_selftest.py", line 701, in test_nonadmitted_population_checks_pids_only_for_executed_runs
    self.assertEqual(R._population(records, "F", 0)["reasons"], [])
AssertionError: Lists differ: ['incomplete/malformed/invalid run: proces[83 chars]med'] != []

First list contains 2 additional elements.
First extra element 0:
'incomplete/malformed/invalid run: process/replicate malformed'

+ []
- ['incomplete/malformed/invalid run: process/replicate malformed',
-  'incomplete/malformed/invalid run: process/replicate malformed']

======================================================================
FAIL: test_nonadmitted_replication_pairs_record_underfit_done_in_both_directions (__main__.NonadmittedTests.test_nonadmitted_replication_pairs_record_underfit_done_in_both_directions) (outcomes=('UNDERFIT', 'DONE'))
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_selftest.py", line 677, in test_nonadmitted_replication_pairs_record_underfit_done_in_both_directions
    self.assertEqual(reading["direction"], "ROUTING-BLOCKED-UNDERFIT")
AssertionError: 'INVALID' != 'ROUTING-BLOCKED-UNDERFIT'
- INVALID
+ ROUTING-BLOCKED-UNDERFIT


======================================================================
FAIL: test_nonadmitted_replication_pairs_record_underfit_done_in_both_directions (__main__.NonadmittedTests.test_nonadmitted_replication_pairs_record_underfit_done_in_both_directions) (outcomes=('DONE', 'UNDERFIT'))
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_selftest.py", line 677, in test_nonadmitted_replication_pairs_record_underfit_done_in_both_directions
    self.assertEqual(reading["direction"], "ROUTING-BLOCKED-UNDERFIT")
AssertionError: 'INVALID' != 'ROUTING-BLOCKED-UNDERFIT'
- INVALID
+ ROUTING-BLOCKED-UNDERFIT


======================================================================
FAIL: test_nonadmitted_replication_pairs_record_underfit_done_in_both_directions (__main__.NonadmittedTests.test_nonadmitted_replication_pairs_record_underfit_done_in_both_directions) (outcomes=('UNDERFIT', 'UNDERFIT'))
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_selftest.py", line 677, in test_nonadmitted_replication_pairs_record_underfit_done_in_both_directions
    self.assertEqual(reading["direction"], "ROUTING-BLOCKED-UNDERFIT")
AssertionError: 'INVALID' != 'ROUTING-BLOCKED-UNDERFIT'
- INVALID
+ ROUTING-BLOCKED-UNDERFIT


======================================================================
FAIL: test_nonadmitted_seven_record_regression_retains_replication_without_a_count (__main__.NonadmittedTests.test_nonadmitted_seven_record_regression_retains_replication_without_a_count)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_selftest.py", line 587, in test_nonadmitted_seven_record_regression_retains_replication_without_a_count
    self.assertEqual(reading["direction"], "ROUTING-BLOCKED-UNDERFIT")
AssertionError: 'INVALID' != 'ROUTING-BLOCKED-UNDERFIT'
- INVALID
+ ROUTING-BLOCKED-UNDERFIT


======================================================================
FAIL: test_nonadmitted_v2_keeps_replication_and_blocks_control (__main__.NonadmittedTests.test_nonadmitted_v2_keeps_replication_and_blocks_control) (index=1)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_selftest.py", line 711, in test_nonadmitted_v2_keeps_replication_and_blocks_control
    self.assertEqual(reading["direction"], "ROUTING-BLOCKED-UNDERFIT")
AssertionError: 'INVALID' != 'ROUTING-BLOCKED-UNDERFIT'
- INVALID
+ ROUTING-BLOCKED-UNDERFIT


======================================================================
FAIL: test_nonadmitted_v2_keeps_replication_and_blocks_control (__main__.NonadmittedTests.test_nonadmitted_v2_keeps_replication_and_blocks_control) (index=4)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_selftest.py", line 711, in test_nonadmitted_v2_keeps_replication_and_blocks_control
    self.assertEqual(reading["direction"], "ROUTING-BLOCKED-UNDERFIT")
AssertionError: 'INVALID' != 'ROUTING-BLOCKED-UNDERFIT'
- INVALID
+ ROUTING-BLOCKED-UNDERFIT


----------------------------------------------------------------------
Ran 74 tests in 1.708s

FAILED (failures=13, errors=1)
exit_code: 1
```

## RED output — producer follow-up

```text
$ /opt/homebrew/bin/rtk proxy .venv/bin/python -B experiments/track_c/c10u_mint2_selftest.py
test_aenv_baseline_boundaries_in_both_blocks_and_replicates (__main__.AenvTests.test_aenv_baseline_boundaries_in_both_blocks_and_replicates) ... ok
test_aenv_envelope_review_counterexamples_keep_null_precedence (__main__.AenvTests.test_aenv_envelope_review_counterexamples_keep_null_precedence) ... ok
test_aenv_halt_stops_both_blocks_in_initial_and_replication_stages (__main__.AenvTests.test_aenv_halt_stops_both_blocks_in_initial_and_replication_stages) ... ok
test_aenv_null_boundaries_and_replication_exclusion (__main__.AenvTests.test_aenv_null_boundaries_and_replication_exclusion) ... ok
test_aenv_r1_counts_pass_a4_and_fail_original_window_without_reading_r1 (__main__.AenvTests.test_aenv_r1_counts_pass_a4_and_fail_original_window_without_reading_r1) ... ok
test_aenv_replica_compatibility_can_overturn_positive_routing (__main__.AenvTests.test_aenv_replica_compatibility_can_overturn_positive_routing) ... ok
test_aenv_schedule_keeps_reference_and_negative_direction_replication (__main__.AenvTests.test_aenv_schedule_keeps_reference_and_negative_direction_replication) ... ok
test_aenv_source_identity_pins_amended_prereg_reader_and_driver (__main__.AenvTests.test_aenv_source_identity_pins_amended_prereg_reader_and_driver) ... ok
test_aenv_stage_completion_round_trips_missing_and_replication_missing (__main__.AenvTests.test_aenv_stage_completion_round_trips_missing_and_replication_missing) ... ok
test_aenv_truth_table_verbatim_through_range_and_replication (__main__.AenvTests.test_aenv_truth_table_verbatim_through_range_and_replication) ... ok
test_nonadmitted_does_not_weaken_done_pid_or_unknown_outcome_gates (__main__.NonadmittedTests.test_nonadmitted_does_not_weaken_done_pid_or_unknown_outcome_gates) ... ok
test_nonadmitted_json_round_trip_keeps_block_reading (__main__.NonadmittedTests.test_nonadmitted_json_round_trip_keeps_block_reading) ... ok
test_nonadmitted_keeps_material_and_p2_audits (__main__.NonadmittedTests.test_nonadmitted_keeps_material_and_p2_audits) ... ok
test_nonadmitted_mint1_in_frozen_block_fails_law3 (__main__.NonadmittedTests.test_nonadmitted_mint1_in_frozen_block_fails_law3) ... ok
test_nonadmitted_p3_screen_is_recomputed_at_22_and_exact_098 (__main__.NonadmittedTests.test_nonadmitted_p3_screen_is_recomputed_at_22_and_exact_098) ... ok
test_nonadmitted_p4_selection_skips_unexecuted_modifier (__main__.NonadmittedTests.test_nonadmitted_p4_selection_skips_unexecuted_modifier) ... ok
test_nonadmitted_population_checks_pids_only_for_executed_runs (__main__.NonadmittedTests.test_nonadmitted_population_checks_pids_only_for_executed_runs) ... ok
test_nonadmitted_rejects_behavioral_keys_positive_pid_multi_and_failed_p2 (__main__.NonadmittedTests.test_nonadmitted_rejects_behavioral_keys_positive_pid_multi_and_failed_p2) ... ok
test_nonadmitted_rejects_malformed_p3_and_recomputes_i11 (__main__.NonadmittedTests.test_nonadmitted_rejects_malformed_p3_and_recomputes_i11) ... ok
test_nonadmitted_replication_pairs_record_underfit_done_in_both_directions (__main__.NonadmittedTests.test_nonadmitted_replication_pairs_record_underfit_done_in_both_directions) ... ok
test_nonadmitted_replication_still_rejects_material_and_init_mismatches (__main__.NonadmittedTests.test_nonadmitted_replication_still_rejects_material_and_init_mismatches) ... ok
test_nonadmitted_seven_record_regression_retains_replication_without_a_count (__main__.NonadmittedTests.test_nonadmitted_seven_record_regression_retains_replication_without_a_count) ... ok
test_nonadmitted_v2_keeps_replication_and_blocks_control (__main__.NonadmittedTests.test_nonadmitted_v2_keeps_replication_and_blocks_control) ... ok
test_a1_68_boundary_and_missing_shape_fail_closed (__main__.ReaderTests.test_a1_68_boundary_and_missing_shape_fail_closed) ... ok
test_admission_22_values_and_per_position_underfit_remain_distinct (__main__.ReaderTests.test_admission_22_values_and_per_position_underfit_remain_distinct) ... ok
test_bigram_shape_rejects_missing_duplicate_or_invalid_fraction (__main__.ReaderTests.test_bigram_shape_rejects_missing_duplicate_or_invalid_fraction) ... ok
test_bigram_uses_fact_union_and_zero_correct_is_no_continuation (__main__.ReaderTests.test_bigram_uses_fact_union_and_zero_correct_is_no_continuation) ... ok
test_block_rejects_changed_context_data_and_pairing (__main__.ReaderTests.test_block_rejects_changed_context_data_and_pairing) ... ok
test_blocked_direction_has_no_pending_control (__main__.ReaderTests.test_blocked_direction_has_no_pending_control) ... ok
test_blocks_never_pool_or_recover_missing_seed (__main__.ReaderTests.test_blocks_never_pool_or_recover_missing_seed) ... ok
test_cli_reads_only_records_and_excludes_context_bootstrap (__main__.ReaderTests.test_cli_reads_only_records_and_excludes_context_bootstrap) ... ok
test_complete_record_and_raw_minus_pre_binding (__main__.ReaderTests.test_complete_record_and_raw_minus_pre_binding) ... ok
test_contains_allows_alternative_ids_and_startswith_is_separate (__main__.ReaderTests.test_contains_allows_alternative_ids_and_startswith_is_separate) ... ok
test_control_spending_requires_a_routable_valid_span_block (__main__.ReaderTests.test_control_spending_requires_a_routable_valid_span_block) ... ok
test_control_uses_the_registered_initial_comparison_not_an_extra_replica_control (__main__.ReaderTests.test_control_uses_the_registered_initial_comparison_not_an_extra_replica_control) ... ok
test_direction_keeps_candidate_large_write_and_bigram_qualifiers (__main__.ReaderTests.test_direction_keeps_candidate_large_write_and_bigram_qualifiers) ... ok
test_full_fourteen_schedule_and_conditional_stages (__main__.ReaderTests.test_full_fourteen_schedule_and_conditional_stages) ... ok
test_geometry_collapse_boundaries_are_diagnostic (__main__.ReaderTests.test_geometry_collapse_boundaries_are_diagnostic) ... ok
test_hashes_context_and_row_counts_are_recomputed (__main__.ReaderTests.test_hashes_context_and_row_counts_are_recomputed) ... ok
test_i11_admission_boundaries_and_geometry_is_diagnostic (__main__.ReaderTests.test_i11_admission_boundaries_and_geometry_is_diagnostic) ... ok
test_inertness_fingerprint_and_override_audits_reject_tampering (__main__.ReaderTests.test_inertness_fingerprint_and_override_audits_reject_tampering) ... ok
test_inertness_precision_gate (__main__.ReaderTests.test_inertness_precision_gate) ... ok
test_large_write_is_qualifier_not_gate (__main__.ReaderTests.test_large_write_is_qualifier_not_gate) ... ok
test_law3_miss_suspends_frozen_block (__main__.ReaderTests.test_law3_miss_suspends_frozen_block) ... ok
test_law3_seed_envelopes_median_and_multi_envelope (__main__.ReaderTests.test_law3_seed_envelopes_median_and_multi_envelope) ... ok
test_locality_boundaries_and_falsefires (__main__.ReaderTests.test_locality_boundaries_and_falsefires) ... ok
test_malformed_block_objects_fail_closed_without_raising (__main__.ReaderTests.test_malformed_block_objects_fail_closed_without_raising) ... ok
test_mechanism_curve_respects_first_position_loss_without_a_percentage_cutoff (__main__.ReaderTests.test_mechanism_curve_respects_first_position_loss_without_a_percentage_cutoff) ... ok
test_missing_norm_layer_and_empty_p2_rows_are_invalid (__main__.ReaderTests.test_missing_norm_layer_and_empty_p2_rows_are_invalid) ... ok
test_modifier_recovery_truth_table_frozen_at_v3 (__main__.ReaderTests.test_modifier_recovery_truth_table_frozen_at_v3) ... ok
test_not_comparable_and_underfit_precede_direction (__main__.ReaderTests.test_not_comparable_and_underfit_precede_direction) ... ok
test_null_band_precedes_gain_and_tradeoff_uses_binding (__main__.ReaderTests.test_null_band_precedes_gain_and_tradeoff_uses_binding) ... ok
test_p4_full_sequences_gate_and_q4_correctness_is_report_only (__main__.ReaderTests.test_p4_full_sequences_gate_and_q4_correctness_is_report_only) ... ok
test_p4_reports_fp16_gguf_to_q4_survival_with_its_own_denominator (__main__.ReaderTests.test_p4_reports_fp16_gguf_to_q4_survival_with_its_own_denominator) ... ok
test_p4_tokenizer_population_and_subject_specific_ids_fail_closed (__main__.ReaderTests.test_p4_tokenizer_population_and_subject_specific_ids_fail_closed) ... ok
test_pair_nonoverlap_rule_and_seed_range (__main__.ReaderTests.test_pair_nonoverlap_rule_and_seed_range) ... ok
test_public_readings_round_trip_as_strict_json (__main__.ReaderTests.test_public_readings_round_trip_as_strict_json) ... ok
test_reference_and_i11_helpers_keep_known_baseline_and_whole_recall (__main__.ReaderTests.test_reference_and_i11_helpers_keep_known_baseline_and_whole_recall) ... ok
test_replica_locality_miss_prevents_replication (__main__.ReaderTests.test_replica_locality_miss_prevents_replication) ... ok
test_replication_uses_same_seed_context_rows_and_fresh_pid (__main__.ReaderTests.test_replication_uses_same_seed_context_rows_and_fresh_pid) ... ok
test_reproduction_provenance_is_checked_before_any_new_arm (__main__.ReaderTests.test_reproduction_provenance_is_checked_before_any_new_arm) ... ok
test_span_requires_replication_and_matched48_control (__main__.ReaderTests.test_span_requires_replication_and_matched48_control) ... ok
test_string_below_full_invalid_even_when_binding_is_lead (__main__.ReaderTests.test_string_below_full_invalid_even_when_binding_is_lead) ... ok
test_underfit_mask_is_reported_without_changing_binding (__main__.ReaderTests.test_underfit_mask_is_reported_without_changing_binding) ... ok
test_conditional_empty_stage_refuses_before_any_marker (__main__.SafetyTests.test_conditional_empty_stage_refuses_before_any_marker) ... ok
test_import_does_not_load_runtime (__main__.SafetyTests.test_import_does_not_load_runtime) ... ok
test_nonadmitted_behavior_child_logs_and_parent_accepts (__main__.SafetyTests.test_nonadmitted_behavior_child_logs_and_parent_accepts) ... FAIL
test_nonadmitted_real_producer_record_retains_seven_replication_jobs (__main__.SafetyTests.test_nonadmitted_real_producer_record_retains_seven_replication_jobs) ... FAIL
test_p2_audits_the_engine_default_tokenizer_call (__main__.SafetyTests.test_p2_audits_the_engine_default_tokenizer_call) ... ok
test_p2_audits_two_ids_and_all_720_bigram_prompts (__main__.SafetyTests.test_p2_audits_two_ids_and_all_720_bigram_prompts) ... ok
test_p2_checks_the_whole_modifier_target_even_when_last_id_matches (__main__.SafetyTests.test_p2_checks_the_whole_modifier_target_even_when_last_id_matches) ... ok
test_p2_detects_runtime_context_retokenization (__main__.SafetyTests.test_p2_detects_runtime_context_retokenization) ... ok
test_p4_selection_requires_replication_and_comparability (__main__.SafetyTests.test_p4_selection_requires_replication_and_comparability) ... ok
test_preflight_rejects_inherited_knobs_before_external_calls (__main__.SafetyTests.test_preflight_rejects_inherited_knobs_before_external_calls) ... ok
test_write_json_is_exclusive_and_rereads_exact_payload (__main__.SafetyTests.test_write_json_is_exclusive_and_rereads_exact_payload) ... ok

======================================================================
FAIL: test_nonadmitted_behavior_child_logs_and_parent_accepts (__main__.SafetyTests.test_nonadmitted_behavior_child_logs_and_parent_accepts)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_selftest.py", line 759, in test_nonadmitted_behavior_child_logs_and_parent_accepts
    self.assertEqual(rec["admission"].get("P2"), p2)
AssertionError: None != {'ok': True, 'checks': {'inventory_unchan[9887 chars]ier'}

======================================================================
FAIL: test_nonadmitted_real_producer_record_retains_seven_replication_jobs (__main__.SafetyTests.test_nonadmitted_real_producer_record_retains_seven_replication_jobs)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_selftest.py", line 785, in test_nonadmitted_real_producer_record_retains_seven_replication_jobs
    self.assertEqual(reading["direction"], "ROUTING-BLOCKED-UNDERFIT")
AssertionError: 'INVALID' != 'ROUTING-BLOCKED-UNDERFIT'
- INVALID
+ ROUTING-BLOCKED-UNDERFIT


----------------------------------------------------------------------
Ran 75 tests in 1.806s

FAILED (failures=2)
exit_code: 1
```

## GREEN full-suite output

```text
$ /opt/homebrew/bin/rtk proxy .venv/bin/python -B experiments/track_c/c10u_mint2_selftest.py
test_aenv_baseline_boundaries_in_both_blocks_and_replicates (__main__.AenvTests.test_aenv_baseline_boundaries_in_both_blocks_and_replicates) ... ok
test_aenv_envelope_review_counterexamples_keep_null_precedence (__main__.AenvTests.test_aenv_envelope_review_counterexamples_keep_null_precedence) ... ok
test_aenv_halt_stops_both_blocks_in_initial_and_replication_stages (__main__.AenvTests.test_aenv_halt_stops_both_blocks_in_initial_and_replication_stages) ... ok
test_aenv_null_boundaries_and_replication_exclusion (__main__.AenvTests.test_aenv_null_boundaries_and_replication_exclusion) ... ok
test_aenv_r1_counts_pass_a4_and_fail_original_window_without_reading_r1 (__main__.AenvTests.test_aenv_r1_counts_pass_a4_and_fail_original_window_without_reading_r1) ... ok
test_aenv_replica_compatibility_can_overturn_positive_routing (__main__.AenvTests.test_aenv_replica_compatibility_can_overturn_positive_routing) ... ok
test_aenv_schedule_keeps_reference_and_negative_direction_replication (__main__.AenvTests.test_aenv_schedule_keeps_reference_and_negative_direction_replication) ... ok
test_aenv_source_identity_pins_amended_prereg_reader_and_driver (__main__.AenvTests.test_aenv_source_identity_pins_amended_prereg_reader_and_driver) ... ok
test_aenv_stage_completion_round_trips_missing_and_replication_missing (__main__.AenvTests.test_aenv_stage_completion_round_trips_missing_and_replication_missing) ... ok
test_aenv_truth_table_verbatim_through_range_and_replication (__main__.AenvTests.test_aenv_truth_table_verbatim_through_range_and_replication) ... ok
test_nonadmitted_does_not_weaken_done_pid_or_unknown_outcome_gates (__main__.NonadmittedTests.test_nonadmitted_does_not_weaken_done_pid_or_unknown_outcome_gates) ... ok
test_nonadmitted_json_round_trip_keeps_block_reading (__main__.NonadmittedTests.test_nonadmitted_json_round_trip_keeps_block_reading) ... ok
test_nonadmitted_keeps_material_and_p2_audits (__main__.NonadmittedTests.test_nonadmitted_keeps_material_and_p2_audits) ... ok
test_nonadmitted_mint1_in_frozen_block_fails_law3 (__main__.NonadmittedTests.test_nonadmitted_mint1_in_frozen_block_fails_law3) ... ok
test_nonadmitted_p3_screen_is_recomputed_at_22_and_exact_098 (__main__.NonadmittedTests.test_nonadmitted_p3_screen_is_recomputed_at_22_and_exact_098) ... ok
test_nonadmitted_p4_selection_skips_unexecuted_modifier (__main__.NonadmittedTests.test_nonadmitted_p4_selection_skips_unexecuted_modifier) ... ok
test_nonadmitted_population_checks_pids_only_for_executed_runs (__main__.NonadmittedTests.test_nonadmitted_population_checks_pids_only_for_executed_runs) ... ok
test_nonadmitted_rejects_behavioral_keys_positive_pid_multi_and_failed_p2 (__main__.NonadmittedTests.test_nonadmitted_rejects_behavioral_keys_positive_pid_multi_and_failed_p2) ... ok
test_nonadmitted_rejects_malformed_p3_and_recomputes_i11 (__main__.NonadmittedTests.test_nonadmitted_rejects_malformed_p3_and_recomputes_i11) ... ok
test_nonadmitted_replication_pairs_record_underfit_done_in_both_directions (__main__.NonadmittedTests.test_nonadmitted_replication_pairs_record_underfit_done_in_both_directions) ... ok
test_nonadmitted_replication_still_rejects_material_and_init_mismatches (__main__.NonadmittedTests.test_nonadmitted_replication_still_rejects_material_and_init_mismatches) ... ok
test_nonadmitted_seven_record_regression_retains_replication_without_a_count (__main__.NonadmittedTests.test_nonadmitted_seven_record_regression_retains_replication_without_a_count) ... ok
test_nonadmitted_v2_keeps_replication_and_blocks_control (__main__.NonadmittedTests.test_nonadmitted_v2_keeps_replication_and_blocks_control) ... ok
test_a1_68_boundary_and_missing_shape_fail_closed (__main__.ReaderTests.test_a1_68_boundary_and_missing_shape_fail_closed) ... ok
test_admission_22_values_and_per_position_underfit_remain_distinct (__main__.ReaderTests.test_admission_22_values_and_per_position_underfit_remain_distinct) ... ok
test_bigram_shape_rejects_missing_duplicate_or_invalid_fraction (__main__.ReaderTests.test_bigram_shape_rejects_missing_duplicate_or_invalid_fraction) ... ok
test_bigram_uses_fact_union_and_zero_correct_is_no_continuation (__main__.ReaderTests.test_bigram_uses_fact_union_and_zero_correct_is_no_continuation) ... ok
test_block_rejects_changed_context_data_and_pairing (__main__.ReaderTests.test_block_rejects_changed_context_data_and_pairing) ... ok
test_blocked_direction_has_no_pending_control (__main__.ReaderTests.test_blocked_direction_has_no_pending_control) ... ok
test_blocks_never_pool_or_recover_missing_seed (__main__.ReaderTests.test_blocks_never_pool_or_recover_missing_seed) ... ok
test_cli_reads_only_records_and_excludes_context_bootstrap (__main__.ReaderTests.test_cli_reads_only_records_and_excludes_context_bootstrap) ... ok
test_complete_record_and_raw_minus_pre_binding (__main__.ReaderTests.test_complete_record_and_raw_minus_pre_binding) ... ok
test_contains_allows_alternative_ids_and_startswith_is_separate (__main__.ReaderTests.test_contains_allows_alternative_ids_and_startswith_is_separate) ... ok
test_control_spending_requires_a_routable_valid_span_block (__main__.ReaderTests.test_control_spending_requires_a_routable_valid_span_block) ... ok
test_control_uses_the_registered_initial_comparison_not_an_extra_replica_control (__main__.ReaderTests.test_control_uses_the_registered_initial_comparison_not_an_extra_replica_control) ... ok
test_direction_keeps_candidate_large_write_and_bigram_qualifiers (__main__.ReaderTests.test_direction_keeps_candidate_large_write_and_bigram_qualifiers) ... ok
test_full_fourteen_schedule_and_conditional_stages (__main__.ReaderTests.test_full_fourteen_schedule_and_conditional_stages) ... ok
test_geometry_collapse_boundaries_are_diagnostic (__main__.ReaderTests.test_geometry_collapse_boundaries_are_diagnostic) ... ok
test_hashes_context_and_row_counts_are_recomputed (__main__.ReaderTests.test_hashes_context_and_row_counts_are_recomputed) ... ok
test_i11_admission_boundaries_and_geometry_is_diagnostic (__main__.ReaderTests.test_i11_admission_boundaries_and_geometry_is_diagnostic) ... ok
test_inertness_fingerprint_and_override_audits_reject_tampering (__main__.ReaderTests.test_inertness_fingerprint_and_override_audits_reject_tampering) ... ok
test_inertness_precision_gate (__main__.ReaderTests.test_inertness_precision_gate) ... ok
test_large_write_is_qualifier_not_gate (__main__.ReaderTests.test_large_write_is_qualifier_not_gate) ... ok
test_law3_miss_suspends_frozen_block (__main__.ReaderTests.test_law3_miss_suspends_frozen_block) ... ok
test_law3_seed_envelopes_median_and_multi_envelope (__main__.ReaderTests.test_law3_seed_envelopes_median_and_multi_envelope) ... ok
test_locality_boundaries_and_falsefires (__main__.ReaderTests.test_locality_boundaries_and_falsefires) ... ok
test_malformed_block_objects_fail_closed_without_raising (__main__.ReaderTests.test_malformed_block_objects_fail_closed_without_raising) ... ok
test_mechanism_curve_respects_first_position_loss_without_a_percentage_cutoff (__main__.ReaderTests.test_mechanism_curve_respects_first_position_loss_without_a_percentage_cutoff) ... ok
test_missing_norm_layer_and_empty_p2_rows_are_invalid (__main__.ReaderTests.test_missing_norm_layer_and_empty_p2_rows_are_invalid) ... ok
test_modifier_recovery_truth_table_frozen_at_v3 (__main__.ReaderTests.test_modifier_recovery_truth_table_frozen_at_v3) ... ok
test_not_comparable_and_underfit_precede_direction (__main__.ReaderTests.test_not_comparable_and_underfit_precede_direction) ... ok
test_null_band_precedes_gain_and_tradeoff_uses_binding (__main__.ReaderTests.test_null_band_precedes_gain_and_tradeoff_uses_binding) ... ok
test_p4_full_sequences_gate_and_q4_correctness_is_report_only (__main__.ReaderTests.test_p4_full_sequences_gate_and_q4_correctness_is_report_only) ... ok
test_p4_reports_fp16_gguf_to_q4_survival_with_its_own_denominator (__main__.ReaderTests.test_p4_reports_fp16_gguf_to_q4_survival_with_its_own_denominator) ... ok
test_p4_tokenizer_population_and_subject_specific_ids_fail_closed (__main__.ReaderTests.test_p4_tokenizer_population_and_subject_specific_ids_fail_closed) ... ok
test_pair_nonoverlap_rule_and_seed_range (__main__.ReaderTests.test_pair_nonoverlap_rule_and_seed_range) ... ok
test_public_readings_round_trip_as_strict_json (__main__.ReaderTests.test_public_readings_round_trip_as_strict_json) ... ok
test_reference_and_i11_helpers_keep_known_baseline_and_whole_recall (__main__.ReaderTests.test_reference_and_i11_helpers_keep_known_baseline_and_whole_recall) ... ok
test_replica_locality_miss_prevents_replication (__main__.ReaderTests.test_replica_locality_miss_prevents_replication) ... ok
test_replication_uses_same_seed_context_rows_and_fresh_pid (__main__.ReaderTests.test_replication_uses_same_seed_context_rows_and_fresh_pid) ... ok
test_reproduction_provenance_is_checked_before_any_new_arm (__main__.ReaderTests.test_reproduction_provenance_is_checked_before_any_new_arm) ... ok
test_span_requires_replication_and_matched48_control (__main__.ReaderTests.test_span_requires_replication_and_matched48_control) ... ok
test_string_below_full_invalid_even_when_binding_is_lead (__main__.ReaderTests.test_string_below_full_invalid_even_when_binding_is_lead) ... ok
test_underfit_mask_is_reported_without_changing_binding (__main__.ReaderTests.test_underfit_mask_is_reported_without_changing_binding) ... ok
test_conditional_empty_stage_refuses_before_any_marker (__main__.SafetyTests.test_conditional_empty_stage_refuses_before_any_marker) ... ok
test_import_does_not_load_runtime (__main__.SafetyTests.test_import_does_not_load_runtime) ... ok
test_nonadmitted_behavior_child_logs_and_parent_accepts (__main__.SafetyTests.test_nonadmitted_behavior_child_logs_and_parent_accepts) ... ok
test_nonadmitted_real_producer_record_retains_seven_replication_jobs (__main__.SafetyTests.test_nonadmitted_real_producer_record_retains_seven_replication_jobs) ... ok
test_p2_audits_the_engine_default_tokenizer_call (__main__.SafetyTests.test_p2_audits_the_engine_default_tokenizer_call) ... ok
test_p2_audits_two_ids_and_all_720_bigram_prompts (__main__.SafetyTests.test_p2_audits_two_ids_and_all_720_bigram_prompts) ... ok
test_p2_checks_the_whole_modifier_target_even_when_last_id_matches (__main__.SafetyTests.test_p2_checks_the_whole_modifier_target_even_when_last_id_matches) ... ok
test_p2_detects_runtime_context_retokenization (__main__.SafetyTests.test_p2_detects_runtime_context_retokenization) ... ok
test_p4_selection_requires_replication_and_comparability (__main__.SafetyTests.test_p4_selection_requires_replication_and_comparability) ... ok
test_preflight_rejects_inherited_knobs_before_external_calls (__main__.SafetyTests.test_preflight_rejects_inherited_knobs_before_external_calls) ... ok
test_write_json_is_exclusive_and_rereads_exact_payload (__main__.SafetyTests.test_write_json_is_exclusive_and_rereads_exact_payload) ... ok

----------------------------------------------------------------------
Ran 75 tests in 1.808s

OK
C10U_MINT2_SELFTEST_DONE (stdlib only; no model/torch/GPU/driver)
exit_code: 0
```

## Repro script output — shape diagnostic; acceptance check waived by the lead

```text
$ /opt/homebrew/bin/rtk proxy .venv/bin/python -B /Users/robertrhu/.claude/jobs/8ac4cacf/tmp/repro_7v0.py
complete block jobs: 7 MIXED
real-shape keys match: False
with UNDERFIT jobs: 0
INVALID False ['incomplete/malformed/invalid non-admitted record: non-admitted P3 actually passes 22/24 screen']
exit_code: 0
```

## r2 reader output — expected INVALID for missing P2; HALTED-HARNESS retained

```text
$ /opt/homebrew/bin/rtk proxy .venv/bin/python -B experiments/track_c/c10u_mint2_read.py results/c10u_mint2/r2
{
  "F": {
    "direction": "INVALID",
    "arms": {},
    "reasons": [
      "incomplete/malformed/invalid non-admitted record: 'P2'"
    ],
    "replication_pending": false,
    "controls_pending": false,
    "raw_direction": null
  },
  "V2": {
    "direction": "INCOMPLETE",
    "arms": {},
    "reasons": [],
    "replication_pending": false,
    "controls_pending": false,
    "raw_direction": null
  }
}
exit_code: 2
```

## Diff summary

| File | Function | Line range | Why |
| --- | --- | --- | --- |
| experiments/track_c/c10u_mint2_read.py | _material_validity | 181–204 | Share the original identity, provenance, relation, pairing, context and fingerprint checks between both outcome kinds. |
| experiments/track_c/c10u_mint2_read.py | run_validity | 207–279 | Call the shared material checks while retaining every executed-run validity gate. |
| experiments/track_c/c10u_mint2_read.py | nonadmitted_validity | 282–314 | Validate a minted, process-free failed P3 admission with P2/I-11 evidence and no behavioural keys. |
| experiments/track_c/c10u_mint2_read.py | _record_validity | 317–321 | Dispatch validity by outcome; unknown outcomes retain the executed-run rejection path. |
| experiments/track_c/c10u_mint2_read.py | _replica_matches | 333–335 | Keep material/init/seed/block/kind/replicate matching and require distinct PIDs for executed pairs. |
| experiments/track_c/c10u_mint2_read.py | run_reading | 358–410 | Report UNDERFIT without counts and retain mixed-outcome replica data without treating it as successful behavioural replication. |
| experiments/track_c/c10u_mint2_read.py | _population | 438–455 | Validate both outcome kinds and check PID uniqueness across executed runs. |
| experiments/track_c/c10u_mint2_read.py | block_reading | 487–581 | Suppress ranges on non-admission while retaining completed-arm replication obligations and the block-F LAW#3 gate. |
| experiments/track_c/c10u_mint2_selftest.py | fixture_nonadmitted | 109–120 | Derive the exact top-level key set from the real r2 file and construct the 17/24 admission fixture. |
| experiments/track_c/c10u_mint2_selftest.py | NonadmittedTests | 581–733 | Add 13 regression tests covering brief cases a–h and validity preservation. |
| experiments/track_c/c10u_mint2_arms.py | p4_configurations | 935–958 | Skip non-admitted original records before requesting behavioural readings. |
| experiments/track_c/c10u_mint2_arms.py | behavior_job (non-admitted record dict only) | 773–776 | Include step P2 in the record's admission proof so the pure reader can validate it. |
| experiments/track_c/c10u_mint2_selftest.py | test_nonadmitted_behavior_child_logs_and_parent_accepts | 741–763 | Supply and assert the producer's P2 proof and 17/24 P3 screen while preserving the child log check. |
| experiments/track_c/c10u_mint2_selftest.py | test_nonadmitted_real_producer_record_retains_seven_replication_jobs | 765–791 | Read the real producer's JSON output and prove UNDERFIT routing retains seven replication jobs. |

## Review round

Both independent FIX-FIRST reports, `results/c10u_mint2_readerfix_astra.md` and `results/c10u_mint2_readerfix_advisor.md`, identified the same V2 comparability-precedence blocker. This round implements that blocker plus advisor A3 and the requested part of A2. The failing suite below ran after the regression tests were added and before any reader implementation changes; the subsequent full suite is GREEN.

V2 comparability now runs before either admission or per-position underfit routing. Every required multi/mint-1 reference must be DONE before its counts can establish comparability, in both the original and replica populations. An unestablished screen returns `NOT-COMPARABLE`, names the missing reference evidence, and appends `-NOT-COMPARABLE` to every arm label; the existing P4 selector refuses those V2 configurations. A comparable block still returns `ROUTING-BLOCKED-UNDERFIT` with its replication obligations intact. Each admission or per-position cause appears in `reasons`, including original and replica arms and any supplied control.

The non-admitted validator now requires published `P3.ok is False`, an integer `n_ge_0.98` equal to the recomputed count, and `admission.outcome == "UNDERFIT"`. Its existing material, P2, I-11, process, and absent-behaviour checks remain in place. Block F still applies LAW#3 before routing, has no V2 comparability screen, and retains P4 selection for eligible replicated executed arms. The historical r2 records and HALTED-HARNESS status are unchanged; the previous missing-P2 diagnostic remains in this report.

### Tests → prereg lines

All prereg citations below refer to `docs/C10U_MINT2_PREREG.md`. Line 175 supplies the amended A4 window; tests retain the frozen thresholds.

| Regression test in experiments/track_c/c10u_mint2_selftest.py | Prereg lines | Verified behaviour |
| --- | --- | --- |
| `test_review_v2_multi_envelope_miss_precedes_each_admission_underfit_combination` (753–761) | 78, 86, 92, 175 | Astra's 19/72 multi, mint-1 34/36/46, mint-2 30/31/32 counterexample remains NOT-COMPARABLE with all DONE, original-only UNDERFIT, replica-only UNDERFIT, or both; every label is qualified and P4 refuses. |
| `test_review_v2_mint1_median_miss_precedes_admission_underfit` (763–771) | 78, 86, 92, 175 | Passing multi plus mint-1 20/21/22 stays NOT-COMPARABLE across all three admission-underfit placements; P4 refuses. |
| `test_review_v2_nonadmitted_mint1_leaves_comparability_unestablished_without_counts` (773–795) | 72, 78, 90, 115, 175, 179 | Non-admitted original, replica, or both mint-1 references yield NOT-COMPARABLE without a count or exception. An unreplicated block still schedules seven replication jobs. |
| `test_review_comparability_requires_done_multi_and_mint1_before_reading_counts` (797–804) | 78, 175 | Direct comparability evaluation returns False before reading absent multi/mint-1 arm counts. The population validator still rejects a non-admitted multi record. |
| `test_review_comparable_v2_retains_underfit_replication_and_names_the_arm` (806–814) | 72, 78, 115, 179 | Comparable V2 with mint-2 s0 non-admitted preserves seven replication jobs and reports the exact arm, replicate and 17/24 admission cause. |
| `test_review_frozen_modifier_underfit_keeps_replication_and_eligible_p4_arms` (816–828) | 77, 78, 86, 92, 115, 175, 179 | F modifier s0 non-admitted preserves seven replicate-F jobs, passes F's reference gate, and keeps eligible replicated modifier seeds 1 and 2 available to P4. Existing `test_nonadmitted_mint1_in_frozen_block_fails_law3` retains the F mint-1 HALT-LAW3 check. |
| `test_review_published_admission_must_match_recomputed_underfit` (830–840) | 72, 90, 115 | A published count mismatch, P3.ok True, or admission-outcome mismatch fails validity and yields INVALID. |
| `test_review_underfit_reasons_name_all_admission_and_per_position_causes` (842–855) | 72, 115 | Every blocking original/replica arm is named with its admission or per-position cause; a solely per-position V2 failure also names its arm. |

### RED

Full suite with the new regressions and the pre-fix reader: 83 tests, 18 failures and 4 errors. The missing-count errors and failed comparability/P4 assertions reproduce the blocker; the other failures reproduce the requested admission-field and diagnostic advisories.

```text
$ /opt/homebrew/bin/rtk proxy .venv/bin/python -B experiments/track_c/c10u_mint2_selftest.py
test_aenv_baseline_boundaries_in_both_blocks_and_replicates (__main__.AenvTests.test_aenv_baseline_boundaries_in_both_blocks_and_replicates) ... ok
test_aenv_envelope_review_counterexamples_keep_null_precedence (__main__.AenvTests.test_aenv_envelope_review_counterexamples_keep_null_precedence) ... ok
test_aenv_halt_stops_both_blocks_in_initial_and_replication_stages (__main__.AenvTests.test_aenv_halt_stops_both_blocks_in_initial_and_replication_stages) ... ok
test_aenv_null_boundaries_and_replication_exclusion (__main__.AenvTests.test_aenv_null_boundaries_and_replication_exclusion) ... ok
test_aenv_r1_counts_pass_a4_and_fail_original_window_without_reading_r1 (__main__.AenvTests.test_aenv_r1_counts_pass_a4_and_fail_original_window_without_reading_r1) ... ok
test_aenv_replica_compatibility_can_overturn_positive_routing (__main__.AenvTests.test_aenv_replica_compatibility_can_overturn_positive_routing) ... ok
test_aenv_schedule_keeps_reference_and_negative_direction_replication (__main__.AenvTests.test_aenv_schedule_keeps_reference_and_negative_direction_replication) ... ok
test_aenv_source_identity_pins_amended_prereg_reader_and_driver (__main__.AenvTests.test_aenv_source_identity_pins_amended_prereg_reader_and_driver) ... ok
test_aenv_stage_completion_round_trips_missing_and_replication_missing (__main__.AenvTests.test_aenv_stage_completion_round_trips_missing_and_replication_missing) ... ok
test_aenv_truth_table_verbatim_through_range_and_replication (__main__.AenvTests.test_aenv_truth_table_verbatim_through_range_and_replication) ... ok
test_nonadmitted_does_not_weaken_done_pid_or_unknown_outcome_gates (__main__.NonadmittedTests.test_nonadmitted_does_not_weaken_done_pid_or_unknown_outcome_gates) ... ok
test_nonadmitted_json_round_trip_keeps_block_reading (__main__.NonadmittedTests.test_nonadmitted_json_round_trip_keeps_block_reading) ... ok
test_nonadmitted_keeps_material_and_p2_audits (__main__.NonadmittedTests.test_nonadmitted_keeps_material_and_p2_audits) ... ok
test_nonadmitted_mint1_in_frozen_block_fails_law3 (__main__.NonadmittedTests.test_nonadmitted_mint1_in_frozen_block_fails_law3) ... ok
test_nonadmitted_p3_screen_is_recomputed_at_22_and_exact_098 (__main__.NonadmittedTests.test_nonadmitted_p3_screen_is_recomputed_at_22_and_exact_098) ... ok
test_nonadmitted_p4_selection_skips_unexecuted_modifier (__main__.NonadmittedTests.test_nonadmitted_p4_selection_skips_unexecuted_modifier) ... ok
test_nonadmitted_population_checks_pids_only_for_executed_runs (__main__.NonadmittedTests.test_nonadmitted_population_checks_pids_only_for_executed_runs) ... ok
test_nonadmitted_rejects_behavioral_keys_positive_pid_multi_and_failed_p2 (__main__.NonadmittedTests.test_nonadmitted_rejects_behavioral_keys_positive_pid_multi_and_failed_p2) ... ok
test_nonadmitted_rejects_malformed_p3_and_recomputes_i11 (__main__.NonadmittedTests.test_nonadmitted_rejects_malformed_p3_and_recomputes_i11) ... ok
test_nonadmitted_replication_pairs_record_underfit_done_in_both_directions (__main__.NonadmittedTests.test_nonadmitted_replication_pairs_record_underfit_done_in_both_directions) ... 
  test_nonadmitted_replication_pairs_record_underfit_done_in_both_directions (__main__.NonadmittedTests.test_nonadmitted_replication_pairs_record_underfit_done_in_both_directions) (outcomes=('UNDERFIT', 'DONE')) ... FAIL
  test_nonadmitted_replication_pairs_record_underfit_done_in_both_directions (__main__.NonadmittedTests.test_nonadmitted_replication_pairs_record_underfit_done_in_both_directions) (outcomes=('DONE', 'UNDERFIT')) ... FAIL
  test_nonadmitted_replication_pairs_record_underfit_done_in_both_directions (__main__.NonadmittedTests.test_nonadmitted_replication_pairs_record_underfit_done_in_both_directions) (outcomes=('UNDERFIT', 'UNDERFIT')) ... FAIL
test_nonadmitted_replication_still_rejects_material_and_init_mismatches (__main__.NonadmittedTests.test_nonadmitted_replication_still_rejects_material_and_init_mismatches) ... ok
test_nonadmitted_seven_record_regression_retains_replication_without_a_count (__main__.NonadmittedTests.test_nonadmitted_seven_record_regression_retains_replication_without_a_count) ... ok
test_nonadmitted_v2_keeps_replication_and_blocks_control (__main__.NonadmittedTests.test_nonadmitted_v2_keeps_replication_and_blocks_control) ... 
  test_nonadmitted_v2_keeps_replication_and_blocks_control (__main__.NonadmittedTests.test_nonadmitted_v2_keeps_replication_and_blocks_control) (index=1) ... FAIL
test_a1_68_boundary_and_missing_shape_fail_closed (__main__.ReaderTests.test_a1_68_boundary_and_missing_shape_fail_closed) ... ok
test_admission_22_values_and_per_position_underfit_remain_distinct (__main__.ReaderTests.test_admission_22_values_and_per_position_underfit_remain_distinct) ... ok
test_bigram_shape_rejects_missing_duplicate_or_invalid_fraction (__main__.ReaderTests.test_bigram_shape_rejects_missing_duplicate_or_invalid_fraction) ... ok
test_bigram_uses_fact_union_and_zero_correct_is_no_continuation (__main__.ReaderTests.test_bigram_uses_fact_union_and_zero_correct_is_no_continuation) ... ok
test_block_rejects_changed_context_data_and_pairing (__main__.ReaderTests.test_block_rejects_changed_context_data_and_pairing) ... ok
test_blocked_direction_has_no_pending_control (__main__.ReaderTests.test_blocked_direction_has_no_pending_control) ... ok
test_blocks_never_pool_or_recover_missing_seed (__main__.ReaderTests.test_blocks_never_pool_or_recover_missing_seed) ... ok
test_cli_reads_only_records_and_excludes_context_bootstrap (__main__.ReaderTests.test_cli_reads_only_records_and_excludes_context_bootstrap) ... ok
test_complete_record_and_raw_minus_pre_binding (__main__.ReaderTests.test_complete_record_and_raw_minus_pre_binding) ... ok
test_contains_allows_alternative_ids_and_startswith_is_separate (__main__.ReaderTests.test_contains_allows_alternative_ids_and_startswith_is_separate) ... ok
test_control_spending_requires_a_routable_valid_span_block (__main__.ReaderTests.test_control_spending_requires_a_routable_valid_span_block) ... ok
test_control_uses_the_registered_initial_comparison_not_an_extra_replica_control (__main__.ReaderTests.test_control_uses_the_registered_initial_comparison_not_an_extra_replica_control) ... ok
test_direction_keeps_candidate_large_write_and_bigram_qualifiers (__main__.ReaderTests.test_direction_keeps_candidate_large_write_and_bigram_qualifiers) ... ok
test_full_fourteen_schedule_and_conditional_stages (__main__.ReaderTests.test_full_fourteen_schedule_and_conditional_stages) ... ok
test_geometry_collapse_boundaries_are_diagnostic (__main__.ReaderTests.test_geometry_collapse_boundaries_are_diagnostic) ... ok
test_hashes_context_and_row_counts_are_recomputed (__main__.ReaderTests.test_hashes_context_and_row_counts_are_recomputed) ... ok
test_i11_admission_boundaries_and_geometry_is_diagnostic (__main__.ReaderTests.test_i11_admission_boundaries_and_geometry_is_diagnostic) ... ok
test_inertness_fingerprint_and_override_audits_reject_tampering (__main__.ReaderTests.test_inertness_fingerprint_and_override_audits_reject_tampering) ... ok
test_inertness_precision_gate (__main__.ReaderTests.test_inertness_precision_gate) ... ok
test_large_write_is_qualifier_not_gate (__main__.ReaderTests.test_large_write_is_qualifier_not_gate) ... ok
test_law3_miss_suspends_frozen_block (__main__.ReaderTests.test_law3_miss_suspends_frozen_block) ... ok
test_law3_seed_envelopes_median_and_multi_envelope (__main__.ReaderTests.test_law3_seed_envelopes_median_and_multi_envelope) ... ok
test_locality_boundaries_and_falsefires (__main__.ReaderTests.test_locality_boundaries_and_falsefires) ... ok
test_malformed_block_objects_fail_closed_without_raising (__main__.ReaderTests.test_malformed_block_objects_fail_closed_without_raising) ... ok
test_mechanism_curve_respects_first_position_loss_without_a_percentage_cutoff (__main__.ReaderTests.test_mechanism_curve_respects_first_position_loss_without_a_percentage_cutoff) ... ok
test_missing_norm_layer_and_empty_p2_rows_are_invalid (__main__.ReaderTests.test_missing_norm_layer_and_empty_p2_rows_are_invalid) ... ok
test_modifier_recovery_truth_table_frozen_at_v3 (__main__.ReaderTests.test_modifier_recovery_truth_table_frozen_at_v3) ... ok
test_not_comparable_and_underfit_precede_direction (__main__.ReaderTests.test_not_comparable_and_underfit_precede_direction) ... ok
test_null_band_precedes_gain_and_tradeoff_uses_binding (__main__.ReaderTests.test_null_band_precedes_gain_and_tradeoff_uses_binding) ... ok
test_p4_full_sequences_gate_and_q4_correctness_is_report_only (__main__.ReaderTests.test_p4_full_sequences_gate_and_q4_correctness_is_report_only) ... ok
test_p4_reports_fp16_gguf_to_q4_survival_with_its_own_denominator (__main__.ReaderTests.test_p4_reports_fp16_gguf_to_q4_survival_with_its_own_denominator) ... ok
test_p4_tokenizer_population_and_subject_specific_ids_fail_closed (__main__.ReaderTests.test_p4_tokenizer_population_and_subject_specific_ids_fail_closed) ... ok
test_pair_nonoverlap_rule_and_seed_range (__main__.ReaderTests.test_pair_nonoverlap_rule_and_seed_range) ... ok
test_public_readings_round_trip_as_strict_json (__main__.ReaderTests.test_public_readings_round_trip_as_strict_json) ... ok
test_reference_and_i11_helpers_keep_known_baseline_and_whole_recall (__main__.ReaderTests.test_reference_and_i11_helpers_keep_known_baseline_and_whole_recall) ... ok
test_replica_locality_miss_prevents_replication (__main__.ReaderTests.test_replica_locality_miss_prevents_replication) ... ok
test_replication_uses_same_seed_context_rows_and_fresh_pid (__main__.ReaderTests.test_replication_uses_same_seed_context_rows_and_fresh_pid) ... ok
test_reproduction_provenance_is_checked_before_any_new_arm (__main__.ReaderTests.test_reproduction_provenance_is_checked_before_any_new_arm) ... ok
test_span_requires_replication_and_matched48_control (__main__.ReaderTests.test_span_requires_replication_and_matched48_control) ... ok
test_string_below_full_invalid_even_when_binding_is_lead (__main__.ReaderTests.test_string_below_full_invalid_even_when_binding_is_lead) ... ok
test_underfit_mask_is_reported_without_changing_binding (__main__.ReaderTests.test_underfit_mask_is_reported_without_changing_binding) ... ok
test_review_comparability_requires_done_multi_and_mint1_before_reading_counts (__main__.ReviewRoundTests.test_review_comparability_requires_done_multi_and_mint1_before_reading_counts) ... 
  test_review_comparability_requires_done_multi_and_mint1_before_reading_counts (__main__.ReviewRoundTests.test_review_comparability_requires_done_multi_and_mint1_before_reading_counts) (index=0) ... ERROR
  test_review_comparability_requires_done_multi_and_mint1_before_reading_counts (__main__.ReviewRoundTests.test_review_comparability_requires_done_multi_and_mint1_before_reading_counts) (index=1) ... ERROR
test_review_comparable_v2_retains_underfit_replication_and_names_the_arm (__main__.ReviewRoundTests.test_review_comparable_v2_retains_underfit_replication_and_names_the_arm) ... ERROR
test_review_frozen_modifier_underfit_keeps_replication_and_eligible_p4_arms (__main__.ReviewRoundTests.test_review_frozen_modifier_underfit_keeps_replication_and_eligible_p4_arms) ... ERROR
test_review_published_admission_must_match_recomputed_underfit (__main__.ReviewRoundTests.test_review_published_admission_must_match_recomputed_underfit) ... 
  test_review_published_admission_must_match_recomputed_underfit (__main__.ReviewRoundTests.test_review_published_admission_must_match_recomputed_underfit) (mutation=0) ... FAIL
  test_review_published_admission_must_match_recomputed_underfit (__main__.ReviewRoundTests.test_review_published_admission_must_match_recomputed_underfit) (mutation=1) ... FAIL
  test_review_published_admission_must_match_recomputed_underfit (__main__.ReviewRoundTests.test_review_published_admission_must_match_recomputed_underfit) (mutation=2) ... FAIL
test_review_underfit_reasons_name_all_admission_and_per_position_causes (__main__.ReviewRoundTests.test_review_underfit_reasons_name_all_admission_and_per_position_causes) ... FAIL
test_review_v2_mint1_median_miss_precedes_admission_underfit (__main__.ReviewRoundTests.test_review_v2_mint1_median_miss_precedes_admission_underfit) ... 
  test_review_v2_mint1_median_miss_precedes_admission_underfit (__main__.ReviewRoundTests.test_review_v2_mint1_median_miss_precedes_admission_underfit) (outcomes=('UNDERFIT', 'DONE')) ... FAIL
  test_review_v2_mint1_median_miss_precedes_admission_underfit (__main__.ReviewRoundTests.test_review_v2_mint1_median_miss_precedes_admission_underfit) (outcomes=('DONE', 'UNDERFIT')) ... FAIL
  test_review_v2_mint1_median_miss_precedes_admission_underfit (__main__.ReviewRoundTests.test_review_v2_mint1_median_miss_precedes_admission_underfit) (outcomes=('UNDERFIT', 'UNDERFIT')) ... FAIL
test_review_v2_multi_envelope_miss_precedes_each_admission_underfit_combination (__main__.ReviewRoundTests.test_review_v2_multi_envelope_miss_precedes_each_admission_underfit_combination) ... 
  test_review_v2_multi_envelope_miss_precedes_each_admission_underfit_combination (__main__.ReviewRoundTests.test_review_v2_multi_envelope_miss_precedes_each_admission_underfit_combination) (outcomes=('UNDERFIT', 'DONE')) ... FAIL
  test_review_v2_multi_envelope_miss_precedes_each_admission_underfit_combination (__main__.ReviewRoundTests.test_review_v2_multi_envelope_miss_precedes_each_admission_underfit_combination) (outcomes=('DONE', 'UNDERFIT')) ... FAIL
  test_review_v2_multi_envelope_miss_precedes_each_admission_underfit_combination (__main__.ReviewRoundTests.test_review_v2_multi_envelope_miss_precedes_each_admission_underfit_combination) (outcomes=('UNDERFIT', 'UNDERFIT')) ... FAIL
test_review_v2_nonadmitted_mint1_leaves_comparability_unestablished_without_counts (__main__.ReviewRoundTests.test_review_v2_nonadmitted_mint1_leaves_comparability_unestablished_without_counts) ... 
  test_review_v2_nonadmitted_mint1_leaves_comparability_unestablished_without_counts (__main__.ReviewRoundTests.test_review_v2_nonadmitted_mint1_leaves_comparability_unestablished_without_counts) (outcomes=('UNDERFIT', 'DONE')) ... FAIL
  test_review_v2_nonadmitted_mint1_leaves_comparability_unestablished_without_counts (__main__.ReviewRoundTests.test_review_v2_nonadmitted_mint1_leaves_comparability_unestablished_without_counts) (outcomes=('DONE', 'UNDERFIT')) ... FAIL
  test_review_v2_nonadmitted_mint1_leaves_comparability_unestablished_without_counts (__main__.ReviewRoundTests.test_review_v2_nonadmitted_mint1_leaves_comparability_unestablished_without_counts) (outcomes=('UNDERFIT', 'UNDERFIT')) ... FAIL
test_review_v2_nonadmitted_mint1_leaves_comparability_unestablished_without_counts (__main__.ReviewRoundTests.test_review_v2_nonadmitted_mint1_leaves_comparability_unestablished_without_counts) ... FAIL
test_conditional_empty_stage_refuses_before_any_marker (__main__.SafetyTests.test_conditional_empty_stage_refuses_before_any_marker) ... ok
test_import_does_not_load_runtime (__main__.SafetyTests.test_import_does_not_load_runtime) ... ok
test_nonadmitted_behavior_child_logs_and_parent_accepts (__main__.SafetyTests.test_nonadmitted_behavior_child_logs_and_parent_accepts) ... ok
test_nonadmitted_real_producer_record_retains_seven_replication_jobs (__main__.SafetyTests.test_nonadmitted_real_producer_record_retains_seven_replication_jobs) ... ok
test_p2_audits_the_engine_default_tokenizer_call (__main__.SafetyTests.test_p2_audits_the_engine_default_tokenizer_call) ... ok
test_p2_audits_two_ids_and_all_720_bigram_prompts (__main__.SafetyTests.test_p2_audits_two_ids_and_all_720_bigram_prompts) ... ok
test_p2_checks_the_whole_modifier_target_even_when_last_id_matches (__main__.SafetyTests.test_p2_checks_the_whole_modifier_target_even_when_last_id_matches) ... ok
test_p2_detects_runtime_context_retokenization (__main__.SafetyTests.test_p2_detects_runtime_context_retokenization) ... ok
test_p4_selection_requires_replication_and_comparability (__main__.SafetyTests.test_p4_selection_requires_replication_and_comparability) ... ok
test_preflight_rejects_inherited_knobs_before_external_calls (__main__.SafetyTests.test_preflight_rejects_inherited_knobs_before_external_calls) ... ok
test_write_json_is_exclusive_and_rereads_exact_payload (__main__.SafetyTests.test_write_json_is_exclusive_and_rereads_exact_payload) ... ok

======================================================================
ERROR: test_review_comparability_requires_done_multi_and_mint1_before_reading_counts (__main__.ReviewRoundTests.test_review_comparability_requires_done_multi_and_mint1_before_reading_counts) (index=0)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_selftest.py", line 804, in test_review_comparability_requires_done_multi_and_mint1_before_reading_counts
    self.assertFalse(R._comparability(pop))
                     ^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_read.py", line 473, in _comparability
    ref = records[("multi", None)]["arm"]
          ~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^
KeyError: 'arm'

======================================================================
ERROR: test_review_comparability_requires_done_multi_and_mint1_before_reading_counts (__main__.ReviewRoundTests.test_review_comparability_requires_done_multi_and_mint1_before_reading_counts) (index=1)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_selftest.py", line 804, in test_review_comparability_requires_done_multi_and_mint1_before_reading_counts
    self.assertFalse(R._comparability(pop))
                     ^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_read.py", line 474, in _comparability
    return all(low <= ref[key] <= high for key, (low, high) in BASELINE_WINDOW.items()) and statistics.median(records[("mint1", s)]["arm"]["para_full_binding_n"] for s in SEEDS) >= LEAD_MIN
                                                                                            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/statistics.py", line 562, in median
    data = sorted(data)
           ^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_read.py", line 474, in <genexpr>
    return all(low <= ref[key] <= high for key, (low, high) in BASELINE_WINDOW.items()) and statistics.median(records[("mint1", s)]["arm"]["para_full_binding_n"] for s in SEEDS) >= LEAD_MIN
                                                                                                              ~~~~~~~~~~~~~~~~~~~~~^^^^^^^
KeyError: 'arm'

======================================================================
ERROR: test_review_comparable_v2_retains_underfit_replication_and_names_the_arm (__main__.ReviewRoundTests.test_review_comparable_v2_retains_underfit_replication_and_names_the_arm)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_selftest.py", line 811, in test_review_comparable_v2_retains_underfit_replication_and_names_the_arm
    self.assertTrue(reading["comparability_ok"])
                    ~~~~~~~^^^^^^^^^^^^^^^^^^^^
KeyError: 'comparability_ok'

======================================================================
ERROR: test_review_frozen_modifier_underfit_keeps_replication_and_eligible_p4_arms (__main__.ReviewRoundTests.test_review_frozen_modifier_underfit_keeps_replication_and_eligible_p4_arms)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_selftest.py", line 823, in test_review_frozen_modifier_underfit_keeps_replication_and_eligible_p4_arms
    self.assertTrue(reading["comparability_ok"])
                    ~~~~~~~^^^^^^^^^^^^^^^^^^^^
KeyError: 'comparability_ok'

======================================================================
FAIL: test_nonadmitted_replication_pairs_record_underfit_done_in_both_directions (__main__.NonadmittedTests.test_nonadmitted_replication_pairs_record_underfit_done_in_both_directions) (outcomes=('UNDERFIT', 'DONE'))
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_selftest.py", line 681, in test_nonadmitted_replication_pairs_record_underfit_done_in_both_directions
    self.assertEqual(reading["reasons"], ["modifier_s0 r" + str(rep) + ": admission UNDERFIT n_ge_0.98=17/24"
AssertionError: Lists differ: [] != ['modifier_s0 r0: admission UNDERFIT n_ge_0.98=17/24']

Second list contains 1 additional elements.
First extra element 0:
'modifier_s0 r0: admission UNDERFIT n_ge_0.98=17/24'

- []
+ ['modifier_s0 r0: admission UNDERFIT n_ge_0.98=17/24']

======================================================================
FAIL: test_nonadmitted_replication_pairs_record_underfit_done_in_both_directions (__main__.NonadmittedTests.test_nonadmitted_replication_pairs_record_underfit_done_in_both_directions) (outcomes=('DONE', 'UNDERFIT'))
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_selftest.py", line 681, in test_nonadmitted_replication_pairs_record_underfit_done_in_both_directions
    self.assertEqual(reading["reasons"], ["modifier_s0 r" + str(rep) + ": admission UNDERFIT n_ge_0.98=17/24"
AssertionError: Lists differ: [] != ['modifier_s0 r1: admission UNDERFIT n_ge_0.98=17/24']

Second list contains 1 additional elements.
First extra element 0:
'modifier_s0 r1: admission UNDERFIT n_ge_0.98=17/24'

- []
+ ['modifier_s0 r1: admission UNDERFIT n_ge_0.98=17/24']

======================================================================
FAIL: test_nonadmitted_replication_pairs_record_underfit_done_in_both_directions (__main__.NonadmittedTests.test_nonadmitted_replication_pairs_record_underfit_done_in_both_directions) (outcomes=('UNDERFIT', 'UNDERFIT'))
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_selftest.py", line 681, in test_nonadmitted_replication_pairs_record_underfit_done_in_both_directions
    self.assertEqual(reading["reasons"], ["modifier_s0 r" + str(rep) + ": admission UNDERFIT n_ge_0.98=17/24"
AssertionError: Lists differ: [] != ['modifier_s0 r0: admission UNDERFIT n_ge_[61 chars]/24']

Second list contains 2 additional elements.
First extra element 0:
'modifier_s0 r0: admission UNDERFIT n_ge_0.98=17/24'

- []
+ ['modifier_s0 r0: admission UNDERFIT n_ge_0.98=17/24',
+  'modifier_s0 r1: admission UNDERFIT n_ge_0.98=17/24']

======================================================================
FAIL: test_nonadmitted_v2_keeps_replication_and_blocks_control (__main__.NonadmittedTests.test_nonadmitted_v2_keeps_replication_and_blocks_control) (index=1)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_selftest.py", line 715, in test_nonadmitted_v2_keeps_replication_and_blocks_control
    self.assertEqual(reading["direction"], "NOT-COMPARABLE" if index == 1 else "ROUTING-BLOCKED-UNDERFIT")
AssertionError: 'ROUTING-BLOCKED-UNDERFIT' != 'NOT-COMPARABLE'
- ROUTING-BLOCKED-UNDERFIT
+ NOT-COMPARABLE


======================================================================
FAIL: test_review_published_admission_must_match_recomputed_underfit (__main__.ReviewRoundTests.test_review_published_admission_must_match_recomputed_underfit) (mutation=0)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_selftest.py", line 839, in test_review_published_admission_must_match_recomputed_underfit
    self.assertTrue(R.nonadmitted_validity(record))
AssertionError: [] is not true

======================================================================
FAIL: test_review_published_admission_must_match_recomputed_underfit (__main__.ReviewRoundTests.test_review_published_admission_must_match_recomputed_underfit) (mutation=1)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_selftest.py", line 839, in test_review_published_admission_must_match_recomputed_underfit
    self.assertTrue(R.nonadmitted_validity(record))
AssertionError: [] is not true

======================================================================
FAIL: test_review_published_admission_must_match_recomputed_underfit (__main__.ReviewRoundTests.test_review_published_admission_must_match_recomputed_underfit) (mutation=2)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_selftest.py", line 839, in test_review_published_admission_must_match_recomputed_underfit
    self.assertTrue(R.nonadmitted_validity(record))
AssertionError: [] is not true

======================================================================
FAIL: test_review_underfit_reasons_name_all_admission_and_per_position_causes (__main__.ReviewRoundTests.test_review_underfit_reasons_name_all_admission_and_per_position_causes)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_selftest.py", line 850, in test_review_underfit_reasons_name_all_admission_and_per_position_causes
    self.assertEqual(reading["reasons"], ["modifier_s0 r0: admission UNDERFIT n_ge_0.98=17/24",
AssertionError: Lists differ: [] != ['modifier_s0 r0: admission UNDERFIT n_ge_[89 chars]fit']

Second list contains 3 additional elements.
First extra element 0:
'modifier_s0 r0: admission UNDERFIT n_ge_0.98=17/24'

- []
+ ['modifier_s0 r0: admission UNDERFIT n_ge_0.98=17/24',
+  'modifier_s1 r0: per-position underfit',
+  'modifier_s2 r1: per-position underfit']

======================================================================
FAIL: test_review_v2_mint1_median_miss_precedes_admission_underfit (__main__.ReviewRoundTests.test_review_v2_mint1_median_miss_precedes_admission_underfit) (outcomes=('UNDERFIT', 'DONE'))
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_selftest.py", line 771, in test_review_v2_mint1_median_miss_precedes_admission_underfit
    self.assert_not_comparable(a, b)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_selftest.py", line 746, in assert_not_comparable
    self.assertEqual(reading["direction"], "NOT-COMPARABLE")
AssertionError: 'ROUTING-BLOCKED-UNDERFIT' != 'NOT-COMPARABLE'
- ROUTING-BLOCKED-UNDERFIT
+ NOT-COMPARABLE


======================================================================
FAIL: test_review_v2_mint1_median_miss_precedes_admission_underfit (__main__.ReviewRoundTests.test_review_v2_mint1_median_miss_precedes_admission_underfit) (outcomes=('DONE', 'UNDERFIT'))
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_selftest.py", line 771, in test_review_v2_mint1_median_miss_precedes_admission_underfit
    self.assert_not_comparable(a, b)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_selftest.py", line 746, in assert_not_comparable
    self.assertEqual(reading["direction"], "NOT-COMPARABLE")
AssertionError: 'ROUTING-BLOCKED-UNDERFIT' != 'NOT-COMPARABLE'
- ROUTING-BLOCKED-UNDERFIT
+ NOT-COMPARABLE


======================================================================
FAIL: test_review_v2_mint1_median_miss_precedes_admission_underfit (__main__.ReviewRoundTests.test_review_v2_mint1_median_miss_precedes_admission_underfit) (outcomes=('UNDERFIT', 'UNDERFIT'))
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_selftest.py", line 771, in test_review_v2_mint1_median_miss_precedes_admission_underfit
    self.assert_not_comparable(a, b)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_selftest.py", line 746, in assert_not_comparable
    self.assertEqual(reading["direction"], "NOT-COMPARABLE")
AssertionError: 'ROUTING-BLOCKED-UNDERFIT' != 'NOT-COMPARABLE'
- ROUTING-BLOCKED-UNDERFIT
+ NOT-COMPARABLE


======================================================================
FAIL: test_review_v2_multi_envelope_miss_precedes_each_admission_underfit_combination (__main__.ReviewRoundTests.test_review_v2_multi_envelope_miss_precedes_each_admission_underfit_combination) (outcomes=('UNDERFIT', 'DONE'))
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_selftest.py", line 761, in test_review_v2_multi_envelope_miss_precedes_each_admission_underfit_combination
    self.assert_not_comparable(a, b)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_selftest.py", line 746, in assert_not_comparable
    self.assertEqual(reading["direction"], "NOT-COMPARABLE")
AssertionError: 'ROUTING-BLOCKED-UNDERFIT' != 'NOT-COMPARABLE'
- ROUTING-BLOCKED-UNDERFIT
+ NOT-COMPARABLE


======================================================================
FAIL: test_review_v2_multi_envelope_miss_precedes_each_admission_underfit_combination (__main__.ReviewRoundTests.test_review_v2_multi_envelope_miss_precedes_each_admission_underfit_combination) (outcomes=('DONE', 'UNDERFIT'))
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_selftest.py", line 761, in test_review_v2_multi_envelope_miss_precedes_each_admission_underfit_combination
    self.assert_not_comparable(a, b)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_selftest.py", line 746, in assert_not_comparable
    self.assertEqual(reading["direction"], "NOT-COMPARABLE")
AssertionError: 'ROUTING-BLOCKED-UNDERFIT' != 'NOT-COMPARABLE'
- ROUTING-BLOCKED-UNDERFIT
+ NOT-COMPARABLE


======================================================================
FAIL: test_review_v2_multi_envelope_miss_precedes_each_admission_underfit_combination (__main__.ReviewRoundTests.test_review_v2_multi_envelope_miss_precedes_each_admission_underfit_combination) (outcomes=('UNDERFIT', 'UNDERFIT'))
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_selftest.py", line 761, in test_review_v2_multi_envelope_miss_precedes_each_admission_underfit_combination
    self.assert_not_comparable(a, b)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_selftest.py", line 746, in assert_not_comparable
    self.assertEqual(reading["direction"], "NOT-COMPARABLE")
AssertionError: 'ROUTING-BLOCKED-UNDERFIT' != 'NOT-COMPARABLE'
- ROUTING-BLOCKED-UNDERFIT
+ NOT-COMPARABLE


======================================================================
FAIL: test_review_v2_nonadmitted_mint1_leaves_comparability_unestablished_without_counts (__main__.ReviewRoundTests.test_review_v2_nonadmitted_mint1_leaves_comparability_unestablished_without_counts) (outcomes=('UNDERFIT', 'DONE'))
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_selftest.py", line 780, in test_review_v2_nonadmitted_mint1_leaves_comparability_unestablished_without_counts
    reading = self.assert_not_comparable(a, b)
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_selftest.py", line 746, in assert_not_comparable
    self.assertEqual(reading["direction"], "NOT-COMPARABLE")
AssertionError: 'ROUTING-BLOCKED-UNDERFIT' != 'NOT-COMPARABLE'
- ROUTING-BLOCKED-UNDERFIT
+ NOT-COMPARABLE


======================================================================
FAIL: test_review_v2_nonadmitted_mint1_leaves_comparability_unestablished_without_counts (__main__.ReviewRoundTests.test_review_v2_nonadmitted_mint1_leaves_comparability_unestablished_without_counts) (outcomes=('DONE', 'UNDERFIT'))
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_selftest.py", line 780, in test_review_v2_nonadmitted_mint1_leaves_comparability_unestablished_without_counts
    reading = self.assert_not_comparable(a, b)
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_selftest.py", line 746, in assert_not_comparable
    self.assertEqual(reading["direction"], "NOT-COMPARABLE")
AssertionError: 'ROUTING-BLOCKED-UNDERFIT' != 'NOT-COMPARABLE'
- ROUTING-BLOCKED-UNDERFIT
+ NOT-COMPARABLE


======================================================================
FAIL: test_review_v2_nonadmitted_mint1_leaves_comparability_unestablished_without_counts (__main__.ReviewRoundTests.test_review_v2_nonadmitted_mint1_leaves_comparability_unestablished_without_counts) (outcomes=('UNDERFIT', 'UNDERFIT'))
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_selftest.py", line 780, in test_review_v2_nonadmitted_mint1_leaves_comparability_unestablished_without_counts
    reading = self.assert_not_comparable(a, b)
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_selftest.py", line 746, in assert_not_comparable
    self.assertEqual(reading["direction"], "NOT-COMPARABLE")
AssertionError: 'ROUTING-BLOCKED-UNDERFIT' != 'NOT-COMPARABLE'
- ROUTING-BLOCKED-UNDERFIT
+ NOT-COMPARABLE


======================================================================
FAIL: test_review_v2_nonadmitted_mint1_leaves_comparability_unestablished_without_counts (__main__.ReviewRoundTests.test_review_v2_nonadmitted_mint1_leaves_comparability_unestablished_without_counts)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_selftest.py", line 793, in test_review_v2_nonadmitted_mint1_leaves_comparability_unestablished_without_counts
    self.assertEqual(reading["direction"], "NOT-COMPARABLE")
AssertionError: 'ROUTING-BLOCKED-UNDERFIT' != 'NOT-COMPARABLE'
- ROUTING-BLOCKED-UNDERFIT
+ NOT-COMPARABLE


----------------------------------------------------------------------
Ran 83 tests in 1.968s

FAILED (failures=18, errors=4)
exit_code: 1
```

### GREEN

Full suite after the smallest reader fix: all 83 tests pass. Verification uses the required `.venv/bin/python -B` interpreter and the suite's CPU/stdlib fixtures; it is not model/GPU or scientific-result evidence.

```text
$ /opt/homebrew/bin/rtk proxy .venv/bin/python -B experiments/track_c/c10u_mint2_selftest.py
test_aenv_baseline_boundaries_in_both_blocks_and_replicates (__main__.AenvTests.test_aenv_baseline_boundaries_in_both_blocks_and_replicates) ... ok
test_aenv_envelope_review_counterexamples_keep_null_precedence (__main__.AenvTests.test_aenv_envelope_review_counterexamples_keep_null_precedence) ... ok
test_aenv_halt_stops_both_blocks_in_initial_and_replication_stages (__main__.AenvTests.test_aenv_halt_stops_both_blocks_in_initial_and_replication_stages) ... ok
test_aenv_null_boundaries_and_replication_exclusion (__main__.AenvTests.test_aenv_null_boundaries_and_replication_exclusion) ... ok
test_aenv_r1_counts_pass_a4_and_fail_original_window_without_reading_r1 (__main__.AenvTests.test_aenv_r1_counts_pass_a4_and_fail_original_window_without_reading_r1) ... ok
test_aenv_replica_compatibility_can_overturn_positive_routing (__main__.AenvTests.test_aenv_replica_compatibility_can_overturn_positive_routing) ... ok
test_aenv_schedule_keeps_reference_and_negative_direction_replication (__main__.AenvTests.test_aenv_schedule_keeps_reference_and_negative_direction_replication) ... ok
test_aenv_source_identity_pins_amended_prereg_reader_and_driver (__main__.AenvTests.test_aenv_source_identity_pins_amended_prereg_reader_and_driver) ... ok
test_aenv_stage_completion_round_trips_missing_and_replication_missing (__main__.AenvTests.test_aenv_stage_completion_round_trips_missing_and_replication_missing) ... ok
test_aenv_truth_table_verbatim_through_range_and_replication (__main__.AenvTests.test_aenv_truth_table_verbatim_through_range_and_replication) ... ok
test_nonadmitted_does_not_weaken_done_pid_or_unknown_outcome_gates (__main__.NonadmittedTests.test_nonadmitted_does_not_weaken_done_pid_or_unknown_outcome_gates) ... ok
test_nonadmitted_json_round_trip_keeps_block_reading (__main__.NonadmittedTests.test_nonadmitted_json_round_trip_keeps_block_reading) ... ok
test_nonadmitted_keeps_material_and_p2_audits (__main__.NonadmittedTests.test_nonadmitted_keeps_material_and_p2_audits) ... ok
test_nonadmitted_mint1_in_frozen_block_fails_law3 (__main__.NonadmittedTests.test_nonadmitted_mint1_in_frozen_block_fails_law3) ... ok
test_nonadmitted_p3_screen_is_recomputed_at_22_and_exact_098 (__main__.NonadmittedTests.test_nonadmitted_p3_screen_is_recomputed_at_22_and_exact_098) ... ok
test_nonadmitted_p4_selection_skips_unexecuted_modifier (__main__.NonadmittedTests.test_nonadmitted_p4_selection_skips_unexecuted_modifier) ... ok
test_nonadmitted_population_checks_pids_only_for_executed_runs (__main__.NonadmittedTests.test_nonadmitted_population_checks_pids_only_for_executed_runs) ... ok
test_nonadmitted_rejects_behavioral_keys_positive_pid_multi_and_failed_p2 (__main__.NonadmittedTests.test_nonadmitted_rejects_behavioral_keys_positive_pid_multi_and_failed_p2) ... ok
test_nonadmitted_rejects_malformed_p3_and_recomputes_i11 (__main__.NonadmittedTests.test_nonadmitted_rejects_malformed_p3_and_recomputes_i11) ... ok
test_nonadmitted_replication_pairs_record_underfit_done_in_both_directions (__main__.NonadmittedTests.test_nonadmitted_replication_pairs_record_underfit_done_in_both_directions) ... ok
test_nonadmitted_replication_still_rejects_material_and_init_mismatches (__main__.NonadmittedTests.test_nonadmitted_replication_still_rejects_material_and_init_mismatches) ... ok
test_nonadmitted_seven_record_regression_retains_replication_without_a_count (__main__.NonadmittedTests.test_nonadmitted_seven_record_regression_retains_replication_without_a_count) ... ok
test_nonadmitted_v2_keeps_replication_and_blocks_control (__main__.NonadmittedTests.test_nonadmitted_v2_keeps_replication_and_blocks_control) ... ok
test_a1_68_boundary_and_missing_shape_fail_closed (__main__.ReaderTests.test_a1_68_boundary_and_missing_shape_fail_closed) ... ok
test_admission_22_values_and_per_position_underfit_remain_distinct (__main__.ReaderTests.test_admission_22_values_and_per_position_underfit_remain_distinct) ... ok
test_bigram_shape_rejects_missing_duplicate_or_invalid_fraction (__main__.ReaderTests.test_bigram_shape_rejects_missing_duplicate_or_invalid_fraction) ... ok
test_bigram_uses_fact_union_and_zero_correct_is_no_continuation (__main__.ReaderTests.test_bigram_uses_fact_union_and_zero_correct_is_no_continuation) ... ok
test_block_rejects_changed_context_data_and_pairing (__main__.ReaderTests.test_block_rejects_changed_context_data_and_pairing) ... ok
test_blocked_direction_has_no_pending_control (__main__.ReaderTests.test_blocked_direction_has_no_pending_control) ... ok
test_blocks_never_pool_or_recover_missing_seed (__main__.ReaderTests.test_blocks_never_pool_or_recover_missing_seed) ... ok
test_cli_reads_only_records_and_excludes_context_bootstrap (__main__.ReaderTests.test_cli_reads_only_records_and_excludes_context_bootstrap) ... ok
test_complete_record_and_raw_minus_pre_binding (__main__.ReaderTests.test_complete_record_and_raw_minus_pre_binding) ... ok
test_contains_allows_alternative_ids_and_startswith_is_separate (__main__.ReaderTests.test_contains_allows_alternative_ids_and_startswith_is_separate) ... ok
test_control_spending_requires_a_routable_valid_span_block (__main__.ReaderTests.test_control_spending_requires_a_routable_valid_span_block) ... ok
test_control_uses_the_registered_initial_comparison_not_an_extra_replica_control (__main__.ReaderTests.test_control_uses_the_registered_initial_comparison_not_an_extra_replica_control) ... ok
test_direction_keeps_candidate_large_write_and_bigram_qualifiers (__main__.ReaderTests.test_direction_keeps_candidate_large_write_and_bigram_qualifiers) ... ok
test_full_fourteen_schedule_and_conditional_stages (__main__.ReaderTests.test_full_fourteen_schedule_and_conditional_stages) ... ok
test_geometry_collapse_boundaries_are_diagnostic (__main__.ReaderTests.test_geometry_collapse_boundaries_are_diagnostic) ... ok
test_hashes_context_and_row_counts_are_recomputed (__main__.ReaderTests.test_hashes_context_and_row_counts_are_recomputed) ... ok
test_i11_admission_boundaries_and_geometry_is_diagnostic (__main__.ReaderTests.test_i11_admission_boundaries_and_geometry_is_diagnostic) ... ok
test_inertness_fingerprint_and_override_audits_reject_tampering (__main__.ReaderTests.test_inertness_fingerprint_and_override_audits_reject_tampering) ... ok
test_inertness_precision_gate (__main__.ReaderTests.test_inertness_precision_gate) ... ok
test_large_write_is_qualifier_not_gate (__main__.ReaderTests.test_large_write_is_qualifier_not_gate) ... ok
test_law3_miss_suspends_frozen_block (__main__.ReaderTests.test_law3_miss_suspends_frozen_block) ... ok
test_law3_seed_envelopes_median_and_multi_envelope (__main__.ReaderTests.test_law3_seed_envelopes_median_and_multi_envelope) ... ok
test_locality_boundaries_and_falsefires (__main__.ReaderTests.test_locality_boundaries_and_falsefires) ... ok
test_malformed_block_objects_fail_closed_without_raising (__main__.ReaderTests.test_malformed_block_objects_fail_closed_without_raising) ... ok
test_mechanism_curve_respects_first_position_loss_without_a_percentage_cutoff (__main__.ReaderTests.test_mechanism_curve_respects_first_position_loss_without_a_percentage_cutoff) ... ok
test_missing_norm_layer_and_empty_p2_rows_are_invalid (__main__.ReaderTests.test_missing_norm_layer_and_empty_p2_rows_are_invalid) ... ok
test_modifier_recovery_truth_table_frozen_at_v3 (__main__.ReaderTests.test_modifier_recovery_truth_table_frozen_at_v3) ... ok
test_not_comparable_and_underfit_precede_direction (__main__.ReaderTests.test_not_comparable_and_underfit_precede_direction) ... ok
test_null_band_precedes_gain_and_tradeoff_uses_binding (__main__.ReaderTests.test_null_band_precedes_gain_and_tradeoff_uses_binding) ... ok
test_p4_full_sequences_gate_and_q4_correctness_is_report_only (__main__.ReaderTests.test_p4_full_sequences_gate_and_q4_correctness_is_report_only) ... ok
test_p4_reports_fp16_gguf_to_q4_survival_with_its_own_denominator (__main__.ReaderTests.test_p4_reports_fp16_gguf_to_q4_survival_with_its_own_denominator) ... ok
test_p4_tokenizer_population_and_subject_specific_ids_fail_closed (__main__.ReaderTests.test_p4_tokenizer_population_and_subject_specific_ids_fail_closed) ... ok
test_pair_nonoverlap_rule_and_seed_range (__main__.ReaderTests.test_pair_nonoverlap_rule_and_seed_range) ... ok
test_public_readings_round_trip_as_strict_json (__main__.ReaderTests.test_public_readings_round_trip_as_strict_json) ... ok
test_reference_and_i11_helpers_keep_known_baseline_and_whole_recall (__main__.ReaderTests.test_reference_and_i11_helpers_keep_known_baseline_and_whole_recall) ... ok
test_replica_locality_miss_prevents_replication (__main__.ReaderTests.test_replica_locality_miss_prevents_replication) ... ok
test_replication_uses_same_seed_context_rows_and_fresh_pid (__main__.ReaderTests.test_replication_uses_same_seed_context_rows_and_fresh_pid) ... ok
test_reproduction_provenance_is_checked_before_any_new_arm (__main__.ReaderTests.test_reproduction_provenance_is_checked_before_any_new_arm) ... ok
test_span_requires_replication_and_matched48_control (__main__.ReaderTests.test_span_requires_replication_and_matched48_control) ... ok
test_string_below_full_invalid_even_when_binding_is_lead (__main__.ReaderTests.test_string_below_full_invalid_even_when_binding_is_lead) ... ok
test_underfit_mask_is_reported_without_changing_binding (__main__.ReaderTests.test_underfit_mask_is_reported_without_changing_binding) ... ok
test_review_comparability_requires_done_multi_and_mint1_before_reading_counts (__main__.ReviewRoundTests.test_review_comparability_requires_done_multi_and_mint1_before_reading_counts) ... ok
test_review_comparable_v2_retains_underfit_replication_and_names_the_arm (__main__.ReviewRoundTests.test_review_comparable_v2_retains_underfit_replication_and_names_the_arm) ... ok
test_review_frozen_modifier_underfit_keeps_replication_and_eligible_p4_arms (__main__.ReviewRoundTests.test_review_frozen_modifier_underfit_keeps_replication_and_eligible_p4_arms) ... ok
test_review_published_admission_must_match_recomputed_underfit (__main__.ReviewRoundTests.test_review_published_admission_must_match_recomputed_underfit) ... ok
test_review_underfit_reasons_name_all_admission_and_per_position_causes (__main__.ReviewRoundTests.test_review_underfit_reasons_name_all_admission_and_per_position_causes) ... ok
test_review_v2_mint1_median_miss_precedes_admission_underfit (__main__.ReviewRoundTests.test_review_v2_mint1_median_miss_precedes_admission_underfit) ... ok
test_review_v2_multi_envelope_miss_precedes_each_admission_underfit_combination (__main__.ReviewRoundTests.test_review_v2_multi_envelope_miss_precedes_each_admission_underfit_combination) ... ok
test_review_v2_nonadmitted_mint1_leaves_comparability_unestablished_without_counts (__main__.ReviewRoundTests.test_review_v2_nonadmitted_mint1_leaves_comparability_unestablished_without_counts) ... ok
test_conditional_empty_stage_refuses_before_any_marker (__main__.SafetyTests.test_conditional_empty_stage_refuses_before_any_marker) ... ok
test_import_does_not_load_runtime (__main__.SafetyTests.test_import_does_not_load_runtime) ... ok
test_nonadmitted_behavior_child_logs_and_parent_accepts (__main__.SafetyTests.test_nonadmitted_behavior_child_logs_and_parent_accepts) ... ok
test_nonadmitted_real_producer_record_retains_seven_replication_jobs (__main__.SafetyTests.test_nonadmitted_real_producer_record_retains_seven_replication_jobs) ... ok
test_p2_audits_the_engine_default_tokenizer_call (__main__.SafetyTests.test_p2_audits_the_engine_default_tokenizer_call) ... ok
test_p2_audits_two_ids_and_all_720_bigram_prompts (__main__.SafetyTests.test_p2_audits_two_ids_and_all_720_bigram_prompts) ... ok
test_p2_checks_the_whole_modifier_target_even_when_last_id_matches (__main__.SafetyTests.test_p2_checks_the_whole_modifier_target_even_when_last_id_matches) ... ok
test_p2_detects_runtime_context_retokenization (__main__.SafetyTests.test_p2_detects_runtime_context_retokenization) ... ok
test_p4_selection_requires_replication_and_comparability (__main__.SafetyTests.test_p4_selection_requires_replication_and_comparability) ... ok
test_preflight_rejects_inherited_knobs_before_external_calls (__main__.SafetyTests.test_preflight_rejects_inherited_knobs_before_external_calls) ... ok
test_write_json_is_exclusive_and_rereads_exact_payload (__main__.SafetyTests.test_write_json_is_exclusive_and_rereads_exact_payload) ... ok

----------------------------------------------------------------------
Ran 83 tests in 2.108s

OK
C10U_MINT2_SELFTEST_DONE (stdlib only; no model/torch/GPU/driver)
exit_code: 0
```

### Diff summary

Line ranges below describe the final files after this review round.

| File | Function / test | Line range | Why |
| --- | --- | --- | --- |
| experiments/track_c/c10u_mint2_read.py | nonadmitted_validity | 282–317 | Check all three requested published admission fields against the recomputed UNDERFIT screen. |
| experiments/track_c/c10u_mint2_read.py | _comparability | 474–479 | Require every multi/mint-1 reference to be DONE before accessing its counts. |
| experiments/track_c/c10u_mint2_read.py | block_reading | 492–593 | Decide comparability before underfit routing, qualify every non-comparable arm, explain unestablished references, and enumerate all admission/per-position underfit causes. Preserve F LAW#3, replication and locality precedence. |
| experiments/track_c/c10u_mint2_selftest.py | fixture_nonadmitted | 109–121 | Publish the fixture's actual admission count and outcome. |
| experiments/track_c/c10u_mint2_selftest.py | test_nonadmitted_p3_screen_is_recomputed_at_22_and_exact_098 | 597–608 | Keep the published count synchronized in the valid 21/24 boundary case while independently checking the 22/24 screen. |
| experiments/track_c/c10u_mint2_selftest.py | test_nonadmitted_replication_pairs_record_underfit_done_in_both_directions | 671–691 | Assert the requested per-arm reasons across original/replica admission outcomes. |
| experiments/track_c/c10u_mint2_selftest.py | test_nonadmitted_v2_keeps_replication_and_blocks_control | 709–718 | Expect NOT-COMPARABLE for a non-admitted mint-1 reference while retaining replication and control-spending checks. |
| experiments/track_c/c10u_mint2_selftest.py | ReviewRoundTests | 740–855 | Add eight regression methods and the shared comparability/P4 assertion helper for the blocker and both requested advisories. |
| experiments/track_c/c10u_mint2_arms.py | unchanged this round | — | The existing P4 selector rejects the restored NOT-COMPARABLE block direction; eligible F-arm selection is verified without a driver change. |
| results/c10u_mint2_reader_fix_codex.md | Review round | appended | Preserve earlier evidence and append prereg mapping, complete RED/GREEN output and this diff summary; first line remains DONE. |

Scope audit: source comparisons against the pre-review snapshot show exactly the three reader functions above changed, with no reader functions removed and no changes to top-level constants/imports. All other reader functions, including DONE validity, reproduction, direction thresholds, stage planning and P4 reading, are byte-for-byte unchanged as source segments. The driver is byte-for-byte unchanged this round. `git diff --check` passes for the named files. The worktree remains `worktree-c10k-route-a` at the requested root. No commits, launches, engine edits, sidecar reads, historical-record rewrites or other file edits were performed in this round.

