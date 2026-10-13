DONE

| Item | Changed file:line | Enforcing tests | Prereg file:line |
|---|---|---|---|
| B1 | `experiments/track_c/c10w_oracle_eval.py:113–114` | `SignedZeroTests.test_zero_delta_preserves_every_fp16_byte; test_nonzero_delta_applies_and_zero_entries_keep_their_bits; test_quantized_zero_boundary` | `docs/C10W_ORACLE_PREREG.md:201,250` |
| B2 | `experiments/track_c/c10w_oracle_read.py:264` | `DefectTests.test_G3_equality_passes_across_the_range; FixRoundTests.test_G3_hundredths_at_inside_and_outside_boundary` | `docs/C10W_ORACLE_PREREG.md:353,368` |
| B3 | `experiments/track_c/c10w_oracle_step0.py:303–313,392–396` | `FixRoundTests.test_P1_516_minutes_refuses_and_counts_failed_attempts; test_all_eval_stages_check_budget_before_child_at_inside_outside` | `docs/C10W_ORACLE_PREREG.md:312,314,316` |
| B4 | `experiments/track_c/c10w_oracle_eval.py:224,344–349,368–469; experiments/track_c/c10w_oracle_step0.py:399–406` | `FixRoundTests.test_LAW3_failure_persists_partial_readouts_and_boundary_controls; test_validity_failure_writes_eval_before_validation; test_setup_and_U_failures_keep_partial_evidence_and_cleanup; test_nonfinite_failure_preserves_reason_and_raw_diagnostic; test_p1_project_invalid_record_returns_reader_verdict; test_unedited_saves_stimulus_before_leak_validation; test_P2_diagnostic_failure_restores_function_instead_of_training_record` | `docs/C10W_ORACLE_PREREG.md:241,246,252,322–324,329–345,448` |
| A1 | `experiments/track_c/c10w_oracle_eval.py:319–320` | `FixRoundTests.test_tracer_limits_local_line_events_to_recipe_and_original` | `docs/C10W_ORACLE_PREREG.md:196–204,249,252,316` |
| A2 | `experiments/track_c/c10w_oracle_eval.py:240–248` | `FixRoundTests.test_null_hash_records_zero_application_before_restore_for_reader; ProposedTests.test_null_application_that_changes_band_halts_before_scoring; test_null_after_hash_mismatch_invalid` | `docs/C10W_ORACLE_PREREG.md:250–251` |
| A3 | `experiments/track_c/c10w_oracle_train.py:148–152` | `FixRoundTests.test_training_offline_environment_precedes_transformers_import` | `docs/C10W_ORACLE_PREREG.md:192,194,342` |
| A4 | `experiments/track_c/c10w_oracle_step0.py:308–313,315–322` | `FixRoundTests.test_P1_budget_ruling_requires_operator_identity; test_training_guard_also_requires_P1_ruling_identity` | `docs/C10W_ORACLE_PREREG.md:314,316` |

RED — full model-free suite, before implementation
```text
$ /opt/homebrew/bin/rtk proxy .venv/bin/python -B experiments/track_c/c10w_oracle_selftest.py
test_G1_to_G7_both_sides (__main__.OracleTests.test_G1_to_G7_both_sides)
§3 lines 351–368: equality passes for every locality/forgetting boundary. ... ok
test_P2_P3_authorization_even_under_projection_limit (__main__.OracleTests.test_P2_P3_authorization_even_under_projection_limit)
§2.8,2.9,8 lines278,280,285,314,532: no implicit post-P1 approval. ... ok
test_P3_replication_must_belong_to_authorized_P1 (__main__.OracleTests.test_P3_replication_must_belong_to_authorized_P1)
§2.8,3 lines278–285,339–340: another P1's replication cannot enable rank64. ... ok
test_all_final_label_table_rows (__main__.OracleTests.test_all_final_label_table_rows)
§3 lines 374–384: every row, including both PARTIAL/FAIL antecedents. ... ok
test_bigram_pairing_retry_and_merge_loss_qualifiers (__main__.OracleTests.test_bigram_pairing_retry_and_merge_loss_qualifiers)
§2.6,3 lines230,232,236,365–370: exact qualifier thresholds and exception. ... ok
test_canonical_read_conditions_and_merge_loss (__main__.OracleTests.test_canonical_read_conditions_and_merge_loss)
§3 line388: canonical seed gap, fit, G1–G6 and merge gap, no exception. ... ok
test_configuration_labels_and_integer_count_boundaries (__main__.OracleTests.test_configuration_labels_and_integer_count_boundaries)
§3 lines 359–368: every label, 29/30 and 60/61, through real reader. ... ok
test_embedded_training_evidence_must_equal_hashed_attempt (__main__.OracleTests.test_embedded_training_evidence_must_equal_hashed_attempt)
§3 lines339–342: a valid file hash cannot authenticate different embedded fit/steps. ... ok
test_entry_preflight_and_training_provenance_precede_model_load (__main__.OracleTests.test_entry_preflight_and_training_provenance_precede_model_load)
§2.5,2.7 lines192–194,241,260: no inherited knob or mismatched certificate. ... ok
test_eval_seam_order_missing_adapter_and_hit_counters (__main__.OracleTests.test_eval_seam_order_missing_adapter_and_hit_counters)
§2.5,2.7 lines198–203,241,253: trained dispatch gated before application. ... ok
test_fit_matched_controls_steps_and_provenance (__main__.OracleTests.test_fit_matched_controls_steps_and_provenance)
§2.2,2.4,3 lines54,186,331–345: own fit, exact matching, incomplete INVALID. ... ok
test_guards_projection_memory_and_eval_wall_boundaries (__main__.OracleTests.test_guards_projection_memory_and_eval_wall_boundaries)
§2.9,5 lines314–318,439–441: equality passes; guards are HALT,not FAIL. ... ok
test_law3_envelope_all_endpoints_and_controls (__main__.OracleTests.test_law3_envelope_all_endpoints_and_controls)
§2.7 lines 241–245: inclusive 4/5/18/19,4/5/10/11,41/42/59/60,67/68. ... ok
test_no_gate_clean_reference_and_locality_cost_never_p3 (__main__.OracleTests.test_no_gate_clean_reference_and_locality_cost_never_p3)
§3 lines 372,395: empty clean rank set -> null, never costly substitution. ... ok
test_null_per_prompt_swap_cannot_hide_behind_counts_or_certificate (__main__.OracleTests.test_null_per_prompt_swap_cannot_hide_behind_counts_or_certificate)
§2.7 line250: every per-prompt hit must match, even with equal aggregate counts. ... ok
test_pure_P1_reprojection_and_real_launcher_refusal (__main__.OracleTests.test_pure_P1_reprojection_and_real_launcher_refusal)
§2.8,2.9 lines278,303–314,316: measured P2/P3 inventory,stage entry refuses. ... ok
test_recipe_delegation_keeps_original_engine_gradient_context (__main__.OracleTests.test_recipe_delegation_keeps_original_engine_gradient_context)
§2.5,2.7 lines197,249,252: unchanged engine-parity recipe, including compute_z gradients. ... ok
test_records_exclusive_roundtrip_and_nonfinite_halt (__main__.OracleTests.test_records_exclusive_roundtrip_and_nonfinite_halt)
§2.10,3 lines322–325,344: real writer, append-only, every JSON classification. ... ok
test_replication_minimum_seed_and_same_seed_boundaries (__main__.OracleTests.test_replication_minimum_seed_and_same_seed_boundaries)
§3 lines 368–370: min-of-two,15/16,10/11,band and each gate crossing. ... ok
test_required_metrics_counts_finiteness_and_denominators (__main__.OracleTests.test_required_metrics_counts_finiteness_and_denominators)
§3 lines342–345: missing/nonfinite/incorrect denominators never pass. ... ok
test_required_probe_rows_and_gate_summaries_cannot_diverge (__main__.OracleTests.test_required_probe_rows_and_gate_summaries_cannot_diverge)
§2.6,3 lines218,224,233,342–345: raw frame, MMLU and cross-score evidence is required. ... ok
test_restore_and_frozen_scope_require_actual_hash_evidence (__main__.OracleTests.test_restore_and_frozen_scope_require_actual_hash_evidence)
§2.4,2.7,3 lines170,251,339–345: contradictory hashes invalidate passing summaries. ... ok
test_retries_charged_before_each_fresh_process (__main__.OracleTests.test_retries_charged_before_each_fresh_process)
§2.2,2.9 lines54,312,314–316: full retry and forced mate cost before spending. ... ok
test_routing_every_row_and_canonical_split (__main__.OracleTests.test_routing_every_row_and_canonical_split)
§3 lines 388–397: PASS(a,b,c), PARTIAL(a,b,c), FAIL, no routing. ... ok
test_seal_real_constants_S1_to_S6_and_shuffled_map (__main__.OracleTests.test_seal_real_constants_S1_to_S6_and_shuffled_map)
§2.2,2.3 lines52,70–104,106,264–266: real constants without importing H. ... ok
test_stimulus_law5_strict_restore_delegation_and_counters (__main__.OracleTests.test_stimulus_law5_strict_restore_delegation_and_counters)
§2.7 lines 245,249–255: strict LAW5 and exact process manifest counters. ... ok
test_training_schedule_exact_seed_steps_warmup_and_fit (__main__.OracleTests.test_training_schedule_exact_seed_steps_warmup_and_fit)
§2.4 lines181–186: N-specific epochs,1000*seed+epoch,400/800 updates. ... ok
test_P3_entry_requires_scientific_eligibility (__main__.ProposedTests.test_P3_entry_requires_scientific_eligibility) ... ok
test_adapter_hash_verified_before_load (__main__.ProposedTests.test_adapter_hash_verified_before_load) ... ok
test_dispatch_refuses_P2_without_authorization_before_creating_phase (__main__.ProposedTests.test_dispatch_refuses_P2_without_authorization_before_creating_phase) ... ok
test_dispatch_refuses_out_of_order_training_unit (__main__.ProposedTests.test_dispatch_refuses_out_of_order_training_unit) ... ok
test_dispatch_refuses_training_unit_when_projection_exceeds_phase_limit (__main__.ProposedTests.test_dispatch_refuses_training_unit_when_projection_exceeds_phase_limit) ... ok
test_each_seal_rule_is_independently_binding (__main__.ProposedTests.test_each_seal_rule_is_independently_binding) ... ok
test_eval_P2_rechecks_authorization (__main__.ProposedTests.test_eval_P2_rechecks_authorization) ... ok
test_eval_law3_miss_halts_before_any_oracle_recipe (__main__.ProposedTests.test_eval_law3_miss_halts_before_any_oracle_recipe) ... ok
test_eval_verifies_preflight_certificate_before_model_load (__main__.ProposedTests.test_eval_verifies_preflight_certificate_before_model_load) ... ok
test_latest_directory_refuses_halted_phase (__main__.ProposedTests.test_latest_directory_refuses_halted_phase) ... ok
test_load_frozen_rejects_prereg_hash_mismatch (__main__.ProposedTests.test_load_frozen_rejects_prereg_hash_mismatch) ... ok
test_merge_loss_exception_requires_clean_gates (__main__.ProposedTests.test_merge_loss_exception_requires_clean_gates) ... ok
test_null_after_hash_mismatch_invalid (__main__.ProposedTests.test_null_after_hash_mismatch_invalid) ... ok
test_null_application_that_changes_band_halts_before_scoring (__main__.ProposedTests.test_null_application_that_changes_band_halts_before_scoring) ... ok
test_oracle_entry_requires_restored_band (__main__.ProposedTests.test_oracle_entry_requires_restored_band) ... ok
test_pass_routing_split_b_is_not_motivation (__main__.ProposedTests.test_pass_routing_split_b_is_not_motivation) ... ok
test_same_seed_band_crossing_at_61 (__main__.ProposedTests.test_same_seed_band_crossing_at_61) ... ok
test_trainer_projection_guard_fires_after_warmup_not_at_wall_limit (__main__.ProposedTests.test_trainer_projection_guard_fires_after_warmup_not_at_wall_limit) ... A7_canon_s0_r16 step 10 loss 1.0
A7_canon_s0_r16 step 20 loss 1.0
ok
test_trainer_verifies_preflight_before_torch (__main__.ProposedTests.test_trainer_verifies_preflight_before_torch) ... ok
test_warmup_is_linear_over_20_steps (__main__.ProposedTests.test_warmup_is_linear_over_20_steps) ... ok
test_G3_equality_passes_across_the_range (__main__.DefectTests.test_G3_equality_passes_across_the_range) ... FAIL
test_G3_hundredths_at_inside_and_outside_boundary (__main__.FixRoundTests.test_G3_hundredths_at_inside_and_outside_boundary) ... 
  test_G3_hundredths_at_inside_and_outside_boundary (__main__.FixRoundTests.test_G3_hundredths_at_inside_and_outside_boundary) (ref=64.01, offset=0.0) ... FAIL
  test_G3_hundredths_at_inside_and_outside_boundary (__main__.FixRoundTests.test_G3_hundredths_at_inside_and_outside_boundary) (ref=64.04, offset=0.0) ... FAIL
test_LAW3_failure_persists_partial_readouts_and_boundary_controls (__main__.FixRoundTests.test_LAW3_failure_persists_partial_readouts_and_boundary_controls) ... 
  test_LAW3_failure_persists_partial_readouts_and_boundary_controls (__main__.FixRoundTests.test_LAW3_failure_persists_partial_readouts_and_boundary_controls) (count=4) ... FAIL
C10W evaluation PASS controls; oracle measurement, not a route
  test_LAW3_failure_persists_partial_readouts_and_boundary_controls (__main__.FixRoundTests.test_LAW3_failure_persists_partial_readouts_and_boundary_controls) (count=5) ... FAIL
C10W evaluation PASS controls; oracle measurement, not a route
  test_LAW3_failure_persists_partial_readouts_and_boundary_controls (__main__.FixRoundTests.test_LAW3_failure_persists_partial_readouts_and_boundary_controls) (count=18) ... FAIL
  test_LAW3_failure_persists_partial_readouts_and_boundary_controls (__main__.FixRoundTests.test_LAW3_failure_persists_partial_readouts_and_boundary_controls) (count=19) ... FAIL
test_P1_516_minutes_refuses_and_counts_failed_attempts (__main__.FixRoundTests.test_P1_516_minutes_refuses_and_counts_failed_attempts) ... FAIL
test_P1_budget_ruling_requires_operator_identity (__main__.FixRoundTests.test_P1_budget_ruling_requires_operator_identity) ... 
  test_P1_budget_ruling_requires_operator_identity (__main__.FixRoundTests.test_P1_budget_ruling_requires_operator_identity) (key='authorized', replacement=None) ... FAIL
  test_P1_budget_ruling_requires_operator_identity (__main__.FixRoundTests.test_P1_budget_ruling_requires_operator_identity) (key='authorized', replacement='') ... FAIL
  test_P1_budget_ruling_requires_operator_identity (__main__.FixRoundTests.test_P1_budget_ruling_requires_operator_identity) (key='recorded_by', replacement=None) ... FAIL
  test_P1_budget_ruling_requires_operator_identity (__main__.FixRoundTests.test_P1_budget_ruling_requires_operator_identity) (key='recorded_by', replacement='') ... FAIL
  test_P1_budget_ruling_requires_operator_identity (__main__.FixRoundTests.test_P1_budget_ruling_requires_operator_identity) (key='recorded_at', replacement=None) ... FAIL
  test_P1_budget_ruling_requires_operator_identity (__main__.FixRoundTests.test_P1_budget_ruling_requires_operator_identity) (key='recorded_at', replacement='') ... FAIL
  test_P1_budget_ruling_requires_operator_identity (__main__.FixRoundTests.test_P1_budget_ruling_requires_operator_identity) (limit=515.99) ... FAIL
test_all_eval_stages_check_budget_before_child_at_inside_outside (__main__.FixRoundTests.test_all_eval_stages_check_budget_before_child_at_inside_outside) ... 
  test_all_eval_stages_check_budget_before_child_at_inside_outside (__main__.FixRoundTests.test_all_eval_stages_check_budget_before_child_at_inside_outside) (phase='P1', offset=0.01) ... FAIL
  test_all_eval_stages_check_budget_before_child_at_inside_outside (__main__.FixRoundTests.test_all_eval_stages_check_budget_before_child_at_inside_outside) (phase='P2', offset=0.01) ... FAIL
  test_all_eval_stages_check_budget_before_child_at_inside_outside (__main__.FixRoundTests.test_all_eval_stages_check_budget_before_child_at_inside_outside) (phase='P3', offset=0.01) ... FAIL
test_nonfinite_failure_preserves_reason_and_raw_diagnostic (__main__.FixRoundTests.test_nonfinite_failure_preserves_reason_and_raw_diagnostic) ... FAIL
test_null_hash_records_zero_application_before_restore_for_reader (__main__.FixRoundTests.test_null_hash_records_zero_application_before_restore_for_reader) ... 
  test_null_hash_records_zero_application_before_restore_for_reader (__main__.FixRoundTests.test_null_hash_records_zero_application_before_restore_for_reader) (mutated=True) ... FAIL
test_p1_project_invalid_record_returns_reader_verdict (__main__.FixRoundTests.test_p1_project_invalid_record_returns_reader_verdict) ... ERROR
test_setup_and_U_failures_keep_partial_evidence_and_cleanup (__main__.FixRoundTests.test_setup_and_U_failures_keep_partial_evidence_and_cleanup) ... 
  test_setup_and_U_failures_keep_partial_evidence_and_cleanup (__main__.FixRoundTests.test_setup_and_U_failures_keep_partial_evidence_and_cleanup) (failure='constructor') ... FAIL
  test_setup_and_U_failures_keep_partial_evidence_and_cleanup (__main__.FixRoundTests.test_setup_and_U_failures_keep_partial_evidence_and_cleanup) (failure='guard') ... FAIL
  test_setup_and_U_failures_keep_partial_evidence_and_cleanup (__main__.FixRoundTests.test_setup_and_U_failures_keep_partial_evidence_and_cleanup) (failure='U') ... FAIL
test_tracer_limits_local_line_events_to_recipe_and_original (__main__.FixRoundTests.test_tracer_limits_local_line_events_to_recipe_and_original) ... FAIL
test_training_guard_also_requires_P1_ruling_identity (__main__.FixRoundTests.test_training_guard_also_requires_P1_ruling_identity) ... 
  test_training_guard_also_requires_P1_ruling_identity (__main__.FixRoundTests.test_training_guard_also_requires_P1_ruling_identity) (missing='authorized') ... FAIL
  test_training_guard_also_requires_P1_ruling_identity (__main__.FixRoundTests.test_training_guard_also_requires_P1_ruling_identity) (missing='recorded_by') ... FAIL
  test_training_guard_also_requires_P1_ruling_identity (__main__.FixRoundTests.test_training_guard_also_requires_P1_ruling_identity) (missing='recorded_at') ... FAIL
test_training_offline_environment_precedes_transformers_import (__main__.FixRoundTests.test_training_offline_environment_precedes_transformers_import) ... FAIL
test_unedited_saves_stimulus_before_leak_validation (__main__.FixRoundTests.test_unedited_saves_stimulus_before_leak_validation) ... ERROR
test_validity_failure_writes_eval_before_validation (__main__.FixRoundTests.test_validity_failure_writes_eval_before_validation) ... 
  test_validity_failure_writes_eval_before_validation (__main__.FixRoundTests.test_validity_failure_writes_eval_before_validation) (count=67) ... FAIL
C10W evaluation PASS controls; oracle measurement, not a route
C10W evaluation PASS controls; oracle measurement, not a route

======================================================================
ERROR: test_p1_project_invalid_record_returns_reader_verdict (__main__.FixRoundTests.test_p1_project_invalid_record_returns_reader_verdict)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1215, in test_p1_project_invalid_record_returns_reader_verdict
    rc = S.dispatch_stage("p1-project")
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_step0.py", line 390, in dispatch_stage
    ev=R.load_json(p1/"eval.json"); R.validate_phase(ev)
                                    ^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_read.py", line 300, in validate_phase
    require(all(p["validity"][k] is True for k in ("fingerprint","seal","instrument","hashes","entry","seam")),"phase correctness controls failed")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_read.py", line 42, in require
    raise Halt("HALT: " + reason)
c10w_oracle_read.Halt: HALT: phase correctness controls failed

======================================================================
ERROR: test_unedited_saves_stimulus_before_leak_validation (__main__.FixRoundTests.test_unedited_saves_stimulus_before_leak_validation)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1229, in test_unedited_saves_stimulus_before_leak_validation
    self.assertEqual(e.stimulus,stimulus)
                     ^^^^^^^^^^
AttributeError: 'Evaluator' object has no attribute 'stimulus'

======================================================================
FAIL: test_G3_equality_passes_across_the_range (__main__.DefectTests.test_G3_equality_passes_across_the_range)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 987, in test_G3_equality_passes_across_the_range
    self.assertNotIn("G3",self.read(d)["ranks"]["16"]["gate_misses"],ref)
AssertionError: 'G3' unexpectedly found in ['G3'] : 64.01

======================================================================
FAIL: test_G3_hundredths_at_inside_and_outside_boundary (__main__.FixRoundTests.test_G3_hundredths_at_inside_and_outside_boundary) (ref=64.01, offset=0.0)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1001, in test_G3_hundredths_at_inside_and_outside_boundary
    self.assertEqual(R.gates(candidate, reference, arm())["G3"], passes)
AssertionError: False != True

======================================================================
FAIL: test_G3_hundredths_at_inside_and_outside_boundary (__main__.FixRoundTests.test_G3_hundredths_at_inside_and_outside_boundary) (ref=64.04, offset=0.0)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1001, in test_G3_hundredths_at_inside_and_outside_boundary
    self.assertEqual(R.gates(candidate, reference, arm())["G3"], passes)
AssertionError: False != True

======================================================================
FAIL: test_LAW3_failure_persists_partial_readouts_and_boundary_controls (__main__.FixRoundTests.test_LAW3_failure_persists_partial_readouts_and_boundary_controls) (count=4)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1154, in test_LAW3_failure_persists_partial_readouts_and_boundary_controls
    self.assertTrue((d/"eval_halt.json").is_file())
AssertionError: False is not true

======================================================================
FAIL: test_LAW3_failure_persists_partial_readouts_and_boundary_controls (__main__.FixRoundTests.test_LAW3_failure_persists_partial_readouts_and_boundary_controls) (count=5)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1162, in test_LAW3_failure_persists_partial_readouts_and_boundary_controls
    self.assertEqual(harness.ARM_HOOKS,[hook])
AssertionError: Lists differ: [] != [<function FixRoundTests._full_eval_patches.<locals>.<lambda> at 0x106ad74c0>]

Second list contains 1 additional elements.
First extra element 0:
<function FixRoundTests._full_eval_patches.<locals>.<lambda> at 0x106ad74c0>

- []
+ [<function FixRoundTests._full_eval_patches.<locals>.<lambda> at 0x106ad74c0>]

======================================================================
FAIL: test_LAW3_failure_persists_partial_readouts_and_boundary_controls (__main__.FixRoundTests.test_LAW3_failure_persists_partial_readouts_and_boundary_controls) (count=18)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1162, in test_LAW3_failure_persists_partial_readouts_and_boundary_controls
    self.assertEqual(harness.ARM_HOOKS,[hook])
AssertionError: Lists differ: [] != [<function FixRoundTests._full_eval_patches.<locals>.<lambda> at 0x106ad7e20>]

Second list contains 1 additional elements.
First extra element 0:
<function FixRoundTests._full_eval_patches.<locals>.<lambda> at 0x106ad7e20>

- []
+ [<function FixRoundTests._full_eval_patches.<locals>.<lambda> at 0x106ad7e20>]

======================================================================
FAIL: test_LAW3_failure_persists_partial_readouts_and_boundary_controls (__main__.FixRoundTests.test_LAW3_failure_persists_partial_readouts_and_boundary_controls) (count=19)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1154, in test_LAW3_failure_persists_partial_readouts_and_boundary_controls
    self.assertTrue((d/"eval_halt.json").is_file())
AssertionError: False is not true

======================================================================
FAIL: test_P1_516_minutes_refuses_and_counts_failed_attempts (__main__.FixRoundTests.test_P1_516_minutes_refuses_and_counts_failed_attempts)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1050, in test_P1_516_minutes_refuses_and_counts_failed_attempts
    self.assertIn("INVALID-BUDGET", self._eval_dispatch("P1",516) or "")
AssertionError: 'INVALID-BUDGET' not found in ''

======================================================================
FAIL: test_P1_budget_ruling_requires_operator_identity (__main__.FixRoundTests.test_P1_budget_ruling_requires_operator_identity) (key='authorized', replacement=None)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1062, in test_P1_budget_ruling_requires_operator_identity
    self.assertIn("authorization", self._eval_dispatch("P1",516,ruling) or "")
AssertionError: 'authorization' not found in ''

======================================================================
FAIL: test_P1_budget_ruling_requires_operator_identity (__main__.FixRoundTests.test_P1_budget_ruling_requires_operator_identity) (key='authorized', replacement='')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1062, in test_P1_budget_ruling_requires_operator_identity
    self.assertIn("authorization", self._eval_dispatch("P1",516,ruling) or "")
AssertionError: 'authorization' not found in ''

======================================================================
FAIL: test_P1_budget_ruling_requires_operator_identity (__main__.FixRoundTests.test_P1_budget_ruling_requires_operator_identity) (key='recorded_by', replacement=None)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1062, in test_P1_budget_ruling_requires_operator_identity
    self.assertIn("authorization", self._eval_dispatch("P1",516,ruling) or "")
AssertionError: 'authorization' not found in ''

======================================================================
FAIL: test_P1_budget_ruling_requires_operator_identity (__main__.FixRoundTests.test_P1_budget_ruling_requires_operator_identity) (key='recorded_by', replacement='')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1062, in test_P1_budget_ruling_requires_operator_identity
    self.assertIn("authorization", self._eval_dispatch("P1",516,ruling) or "")
AssertionError: 'authorization' not found in ''

======================================================================
FAIL: test_P1_budget_ruling_requires_operator_identity (__main__.FixRoundTests.test_P1_budget_ruling_requires_operator_identity) (key='recorded_at', replacement=None)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1062, in test_P1_budget_ruling_requires_operator_identity
    self.assertIn("authorization", self._eval_dispatch("P1",516,ruling) or "")
AssertionError: 'authorization' not found in ''

======================================================================
FAIL: test_P1_budget_ruling_requires_operator_identity (__main__.FixRoundTests.test_P1_budget_ruling_requires_operator_identity) (key='recorded_at', replacement='')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1062, in test_P1_budget_ruling_requires_operator_identity
    self.assertIn("authorization", self._eval_dispatch("P1",516,ruling) or "")
AssertionError: 'authorization' not found in ''

======================================================================
FAIL: test_P1_budget_ruling_requires_operator_identity (__main__.FixRoundTests.test_P1_budget_ruling_requires_operator_identity) (limit=515.99)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1066, in test_P1_budget_ruling_requires_operator_identity
    self.assertEqual(failure is None, passes)
AssertionError: True != False

======================================================================
FAIL: test_all_eval_stages_check_budget_before_child_at_inside_outside (__main__.FixRoundTests.test_all_eval_stages_check_budget_before_child_at_inside_outside) (phase='P1', offset=0.01)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1045, in test_all_eval_stages_check_budget_before_child_at_inside_outside
    self.assertIn("INVALID-BUDGET", failure or "")
AssertionError: 'INVALID-BUDGET' not found in ''

======================================================================
FAIL: test_all_eval_stages_check_budget_before_child_at_inside_outside (__main__.FixRoundTests.test_all_eval_stages_check_budget_before_child_at_inside_outside) (phase='P2', offset=0.01)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1045, in test_all_eval_stages_check_budget_before_child_at_inside_outside
    self.assertIn("INVALID-BUDGET", failure or "")
AssertionError: 'INVALID-BUDGET' not found in ''

======================================================================
FAIL: test_all_eval_stages_check_budget_before_child_at_inside_outside (__main__.FixRoundTests.test_all_eval_stages_check_budget_before_child_at_inside_outside) (phase='P3', offset=0.01)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1045, in test_all_eval_stages_check_budget_before_child_at_inside_outside
    self.assertIn("INVALID-BUDGET", failure or "")
AssertionError: 'INVALID-BUDGET' not found in ''

======================================================================
FAIL: test_nonfinite_failure_preserves_reason_and_raw_diagnostic (__main__.FixRoundTests.test_nonfinite_failure_preserves_reason_and_raw_diagnostic)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1203, in test_nonfinite_failure_preserves_reason_and_raw_diagnostic
    self.assertTrue((d/"eval_halt.json").is_file())
AssertionError: False is not true

======================================================================
FAIL: test_null_hash_records_zero_application_before_restore_for_reader (__main__.FixRoundTests.test_null_hash_records_zero_application_before_restore_for_reader) (mutated=True)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1274, in test_null_hash_records_zero_application_before_restore_for_reader
    self.assertEqual(R.read_measurement({"P1":data})["status"],"INVALID" if mutated else "INCOMPLETE")
AssertionError: 'INCOMPLETE' != 'INVALID'
- INCOMPLETE
+ INVALID


======================================================================
FAIL: test_setup_and_U_failures_keep_partial_evidence_and_cleanup (__main__.FixRoundTests.test_setup_and_U_failures_keep_partial_evidence_and_cleanup) (failure='constructor')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1188, in test_setup_and_U_failures_keep_partial_evidence_and_cleanup
    self.assertTrue((d/"eval_halt.json").is_file())
AssertionError: False is not true

======================================================================
FAIL: test_setup_and_U_failures_keep_partial_evidence_and_cleanup (__main__.FixRoundTests.test_setup_and_U_failures_keep_partial_evidence_and_cleanup) (failure='guard')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1188, in test_setup_and_U_failures_keep_partial_evidence_and_cleanup
    self.assertTrue((d/"eval_halt.json").is_file())
AssertionError: False is not true

======================================================================
FAIL: test_setup_and_U_failures_keep_partial_evidence_and_cleanup (__main__.FixRoundTests.test_setup_and_U_failures_keep_partial_evidence_and_cleanup) (failure='U')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1188, in test_setup_and_U_failures_keep_partial_evidence_and_cleanup
    self.assertTrue((d/"eval_halt.json").is_file())
AssertionError: False is not true

======================================================================
FAIL: test_tracer_limits_local_line_events_to_recipe_and_original (__main__.FixRoundTests.test_tracer_limits_local_line_events_to_recipe_and_original)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1252, in test_tracer_limits_local_line_events_to_recipe_and_original
    self.assertEqual([v for k,v in observed if k == "nested"],[False,False])
AssertionError: Lists differ: [True, True] != [False, False]

First differing element 0:
True
False

- [True, True]
+ [False, False]

======================================================================
FAIL: test_training_guard_also_requires_P1_ruling_identity (__main__.FixRoundTests.test_training_guard_also_requires_P1_ruling_identity) (missing='authorized')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1079, in test_training_guard_also_requires_P1_ruling_identity
    with self.assertRaisesRegex(R.Halt,"authorization"): S.guard_training_unit(*args)
AssertionError: Halt not raised

======================================================================
FAIL: test_training_guard_also_requires_P1_ruling_identity (__main__.FixRoundTests.test_training_guard_also_requires_P1_ruling_identity) (missing='recorded_by')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1079, in test_training_guard_also_requires_P1_ruling_identity
    with self.assertRaisesRegex(R.Halt,"authorization"): S.guard_training_unit(*args)
AssertionError: Halt not raised

======================================================================
FAIL: test_training_guard_also_requires_P1_ruling_identity (__main__.FixRoundTests.test_training_guard_also_requires_P1_ruling_identity) (missing='recorded_at')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1079, in test_training_guard_also_requires_P1_ruling_identity
    with self.assertRaisesRegex(R.Halt,"authorization"): S.guard_training_unit(*args)
AssertionError: Halt not raised

======================================================================
FAIL: test_training_offline_environment_precedes_transformers_import (__main__.FixRoundTests.test_training_offline_environment_precedes_transformers_import)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1294, in test_training_offline_environment_precedes_transformers_import
    self.assertEqual(seen,[("transformers",str(R.ROOT/"hf_cache"),"1")])
AssertionError: Lists differ: [('transformers', 'wrong', '0')] != [('transformers', '/Volumes/memit/llm-database-poc-mirror/ar[67 chars]'1')]

First differing element 0:
('transformers', 'wrong', '0')
('transformers', '/Volumes/memit/llm-database-poc-mirror/ar[66 chars] '1')

- [('transformers', 'wrong', '0')]
+ [('transformers',
+   '/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/hf_cache',
+   '1')]

======================================================================
FAIL: test_validity_failure_writes_eval_before_validation (__main__.FixRoundTests.test_validity_failure_writes_eval_before_validation) (count=67)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1174, in test_validity_failure_writes_eval_before_validation
    self.assertTrue((d/"eval.json").is_file())
AssertionError: False is not true

----------------------------------------------------------------------
Ran 62 tests in 5.067s

FAILED (failures=29, errors=2)
```

RED — tiny CPU tensors, before implementation
```text
$ /opt/homebrew/bin/rtk proxy .venv/bin/python -B experiments/track_c/c10w_oracle_torchcheck.py
test_nonzero_delta_applies_and_zero_entries_keep_their_bits (__main__.SignedZeroTests.test_nonzero_delta_applies_and_zero_entries_keep_their_bits) ... FAIL
test_quantized_zero_boundary (__main__.SignedZeroTests.test_quantized_zero_boundary) ... 
  test_quantized_zero_boundary (__main__.SignedZeroTests.test_quantized_zero_boundary) (sign=1, factor=0.99) ... FAIL
  test_quantized_zero_boundary (__main__.SignedZeroTests.test_quantized_zero_boundary) (sign=1, factor=1.0) ... FAIL
test_zero_delta_preserves_every_fp16_byte (__main__.SignedZeroTests.test_zero_delta_preserves_every_fp16_byte) ... FAIL

======================================================================
FAIL: test_nonzero_delta_applies_and_zero_entries_keep_their_bits (__main__.SignedZeroTests.test_nonzero_delta_applies_and_zero_entries_keep_their_bits)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_torchcheck.py", line 39, in test_nonzero_delta_applies_and_zero_entries_keep_their_bits
    self.assertEqual(bits(weight), bits(expected))
AssertionError: Lists differ: [0, 0, 0, 188, 0, 61, 0, 192] != [0, 128, 0, 188, 0, 61, 0, 192]

First differing element 1:
0
128

- [0, 0, 0, 188, 0, 61, 0, 192]
?       ---

+ [0, 128, 0, 188, 0, 61, 0, 192]
?     +++++


======================================================================
FAIL: test_quantized_zero_boundary (__main__.SignedZeroTests.test_quantized_zero_boundary) (sign=1, factor=0.99)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_torchcheck.py", line 50, in test_quantized_zero_boundary
    self.assertEqual(bits(weight), bits(expected))
AssertionError: Lists differ: [0, 0] != [0, 128]

First differing element 1:
0
128

- [0, 0]
+ [0, 128]

======================================================================
FAIL: test_quantized_zero_boundary (__main__.SignedZeroTests.test_quantized_zero_boundary) (sign=1, factor=1.0)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_torchcheck.py", line 50, in test_quantized_zero_boundary
    self.assertEqual(bits(weight), bits(expected))
AssertionError: Lists differ: [0, 0] != [0, 128]

First differing element 1:
0
128

- [0, 0]
+ [0, 128]

======================================================================
FAIL: test_zero_delta_preserves_every_fp16_byte (__main__.SignedZeroTests.test_zero_delta_preserves_every_fp16_byte)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_torchcheck.py", line 33, in test_zero_delta_preserves_every_fp16_byte
    self.assertEqual(bits(weight), before)
AssertionError: Lists differ: [0, 0, 0, 0, 0, 60, 0, 192] != [0, 128, 0, 0, 0, 60, 0, 192]

First differing element 1:
0
128

- [0, 0, 0, 0, 0, 60, 0, 192]
?             ---

+ [0, 128, 0, 0, 0, 60, 0, 192]
?     +++++


----------------------------------------------------------------------
Ran 3 tests in 0.042s

FAILED (failures=4)
```

RED — P2 cleanup regression, before the saved-seam rename
```text
test_P2_diagnostic_failure_restores_function_instead_of_training_record (c10w_oracle_selftest.FixRoundTests.test_P2_diagnostic_failure_restores_function_instead_of_training_record) ... FAIL

======================================================================
FAIL: test_P2_diagnostic_failure_restores_function_instead_of_training_record (c10w_oracle_selftest.FixRoundTests.test_P2_diagnostic_failure_restores_function_instead_of_training_record)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1212, in test_P2_diagnostic_failure_restores_function_instead_of_training_record
    self.assertIs(harness.my_edit,original)
AssertionError: {'class': 'ORACLE MEASUREMENT — not a route; never promotable as a write-engine result (D-C10r-rulings-3 (2))', 'decision_id': 'D-C10w-oracle', 'status': 'PASS', 'arm': 'A7_coined_coined', 'seed': 1, 'rank': 16, 'retrain': False, 'steps': 400, 'fit': {'correct': 480, 'n': 480}, 'phase': 'P2', 'frozen_parameters_unchanged': True, 'model_id': 'Qwen/Qwen2.5-3B', 'frozen_parameter_hashes_before': {'synthetic.weight': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'}, 'frozen_parameter_hashes_after': {'synthetic.weight': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'}, 'model_revision': '3aab1f1954e9cc14eb9509a215f9e5ca08227a9b', 'layers': [4, 5, 6, 7, 8], 'dtype': 'float32', 'device': 'mps', 'adapter': {'path': 'synthetic.safetensors', 'sha256': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'}, 'provenance': {'train_inputs': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 'trainer_source': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 'mmlu200': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 'templates': '306cb0089dddb066242398c0f03f4d10d67086fbf7b0143f850342906087b272', 'prereg': '2baeb4e9865dd1080ecb5765652c5eae67336eca6047d93b4f5948545854c344'}, 'wall_seconds': 1.0, 'sampled_peak_driver_bytes': 1, 'record_file': {'path': '/private/var/folders/p7/s31_tv0s2wd81chns8v7gsyw0000gn/T/tmp5d3h8nya/train/A7_coined_coined_s1_r16.json', 'sha256': '7faaf118d0523dbee1b8650a6ee86c9f5298b152521fe8668fbeb388ec525996'}} is not <function FixRoundTests._full_eval_patches.<locals>.<lambda> at 0x10afbb380>

----------------------------------------------------------------------
Ran 1 test in 0.092s

FAILED (failures=1)
```

GREEN — final model-free suite
```text
$ /opt/homebrew/bin/rtk proxy .venv/bin/python -B experiments/track_c/c10w_oracle_selftest.py
test_G1_to_G7_both_sides (__main__.OracleTests.test_G1_to_G7_both_sides)
§3 lines 351–368: equality passes for every locality/forgetting boundary. ... ok
test_P2_P3_authorization_even_under_projection_limit (__main__.OracleTests.test_P2_P3_authorization_even_under_projection_limit)
§2.8,2.9,8 lines278,280,285,314,532: no implicit post-P1 approval. ... ok
test_P3_replication_must_belong_to_authorized_P1 (__main__.OracleTests.test_P3_replication_must_belong_to_authorized_P1)
§2.8,3 lines278–285,339–340: another P1's replication cannot enable rank64. ... ok
test_all_final_label_table_rows (__main__.OracleTests.test_all_final_label_table_rows)
§3 lines 374–384: every row, including both PARTIAL/FAIL antecedents. ... ok
test_bigram_pairing_retry_and_merge_loss_qualifiers (__main__.OracleTests.test_bigram_pairing_retry_and_merge_loss_qualifiers)
§2.6,3 lines230,232,236,365–370: exact qualifier thresholds and exception. ... ok
test_canonical_read_conditions_and_merge_loss (__main__.OracleTests.test_canonical_read_conditions_and_merge_loss)
§3 line388: canonical seed gap, fit, G1–G6 and merge gap, no exception. ... ok
test_configuration_labels_and_integer_count_boundaries (__main__.OracleTests.test_configuration_labels_and_integer_count_boundaries)
§3 lines 359–368: every label, 29/30 and 60/61, through real reader. ... ok
test_embedded_training_evidence_must_equal_hashed_attempt (__main__.OracleTests.test_embedded_training_evidence_must_equal_hashed_attempt)
§3 lines339–342: a valid file hash cannot authenticate different embedded fit/steps. ... ok
test_entry_preflight_and_training_provenance_precede_model_load (__main__.OracleTests.test_entry_preflight_and_training_provenance_precede_model_load)
§2.5,2.7 lines192–194,241,260: no inherited knob or mismatched certificate. ... ok
test_eval_seam_order_missing_adapter_and_hit_counters (__main__.OracleTests.test_eval_seam_order_missing_adapter_and_hit_counters)
§2.5,2.7 lines198–203,241,253: trained dispatch gated before application. ... ok
test_fit_matched_controls_steps_and_provenance (__main__.OracleTests.test_fit_matched_controls_steps_and_provenance)
§2.2,2.4,3 lines54,186,331–345: own fit, exact matching, incomplete INVALID. ... ok
test_guards_projection_memory_and_eval_wall_boundaries (__main__.OracleTests.test_guards_projection_memory_and_eval_wall_boundaries)
§2.9,5 lines314–318,439–441: equality passes; guards are HALT,not FAIL. ... ok
test_law3_envelope_all_endpoints_and_controls (__main__.OracleTests.test_law3_envelope_all_endpoints_and_controls)
§2.7 lines 241–245: inclusive 4/5/18/19,4/5/10/11,41/42/59/60,67/68. ... ok
test_no_gate_clean_reference_and_locality_cost_never_p3 (__main__.OracleTests.test_no_gate_clean_reference_and_locality_cost_never_p3)
§3 lines 372,395: empty clean rank set -> null, never costly substitution. ... ok
test_null_per_prompt_swap_cannot_hide_behind_counts_or_certificate (__main__.OracleTests.test_null_per_prompt_swap_cannot_hide_behind_counts_or_certificate)
§2.7 line250: every per-prompt hit must match, even with equal aggregate counts. ... ok
test_pure_P1_reprojection_and_real_launcher_refusal (__main__.OracleTests.test_pure_P1_reprojection_and_real_launcher_refusal)
§2.8,2.9 lines278,303–314,316: measured P2/P3 inventory,stage entry refuses. ... ok
test_recipe_delegation_keeps_original_engine_gradient_context (__main__.OracleTests.test_recipe_delegation_keeps_original_engine_gradient_context)
§2.5,2.7 lines197,249,252: unchanged engine-parity recipe, including compute_z gradients. ... ok
test_records_exclusive_roundtrip_and_nonfinite_halt (__main__.OracleTests.test_records_exclusive_roundtrip_and_nonfinite_halt)
§2.10,3 lines322–325,344: real writer, append-only, every JSON classification. ... ok
test_replication_minimum_seed_and_same_seed_boundaries (__main__.OracleTests.test_replication_minimum_seed_and_same_seed_boundaries)
§3 lines 368–370: min-of-two,15/16,10/11,band and each gate crossing. ... ok
test_required_metrics_counts_finiteness_and_denominators (__main__.OracleTests.test_required_metrics_counts_finiteness_and_denominators)
§3 lines342–345: missing/nonfinite/incorrect denominators never pass. ... ok
test_required_probe_rows_and_gate_summaries_cannot_diverge (__main__.OracleTests.test_required_probe_rows_and_gate_summaries_cannot_diverge)
§2.6,3 lines218,224,233,342–345: raw frame, MMLU and cross-score evidence is required. ... ok
test_restore_and_frozen_scope_require_actual_hash_evidence (__main__.OracleTests.test_restore_and_frozen_scope_require_actual_hash_evidence)
§2.4,2.7,3 lines170,251,339–345: contradictory hashes invalidate passing summaries. ... ok
test_retries_charged_before_each_fresh_process (__main__.OracleTests.test_retries_charged_before_each_fresh_process)
§2.2,2.9 lines54,312,314–316: full retry and forced mate cost before spending. ... ok
test_routing_every_row_and_canonical_split (__main__.OracleTests.test_routing_every_row_and_canonical_split)
§3 lines 388–397: PASS(a,b,c), PARTIAL(a,b,c), FAIL, no routing. ... ok
test_seal_real_constants_S1_to_S6_and_shuffled_map (__main__.OracleTests.test_seal_real_constants_S1_to_S6_and_shuffled_map)
§2.2,2.3 lines52,70–104,106,264–266: real constants without importing H. ... ok
test_stimulus_law5_strict_restore_delegation_and_counters (__main__.OracleTests.test_stimulus_law5_strict_restore_delegation_and_counters)
§2.7 lines 245,249–255: strict LAW5 and exact process manifest counters. ... ok
test_training_schedule_exact_seed_steps_warmup_and_fit (__main__.OracleTests.test_training_schedule_exact_seed_steps_warmup_and_fit)
§2.4 lines181–186: N-specific epochs,1000*seed+epoch,400/800 updates. ... ok
test_P3_entry_requires_scientific_eligibility (__main__.ProposedTests.test_P3_entry_requires_scientific_eligibility) ... ok
test_adapter_hash_verified_before_load (__main__.ProposedTests.test_adapter_hash_verified_before_load) ... ok
test_dispatch_refuses_P2_without_authorization_before_creating_phase (__main__.ProposedTests.test_dispatch_refuses_P2_without_authorization_before_creating_phase) ... ok
test_dispatch_refuses_out_of_order_training_unit (__main__.ProposedTests.test_dispatch_refuses_out_of_order_training_unit) ... ok
test_dispatch_refuses_training_unit_when_projection_exceeds_phase_limit (__main__.ProposedTests.test_dispatch_refuses_training_unit_when_projection_exceeds_phase_limit) ... ok
test_each_seal_rule_is_independently_binding (__main__.ProposedTests.test_each_seal_rule_is_independently_binding) ... ok
test_eval_P2_rechecks_authorization (__main__.ProposedTests.test_eval_P2_rechecks_authorization) ... ok
test_eval_law3_miss_halts_before_any_oracle_recipe (__main__.ProposedTests.test_eval_law3_miss_halts_before_any_oracle_recipe) ... ok
test_eval_verifies_preflight_certificate_before_model_load (__main__.ProposedTests.test_eval_verifies_preflight_certificate_before_model_load) ... ok
test_latest_directory_refuses_halted_phase (__main__.ProposedTests.test_latest_directory_refuses_halted_phase) ... ok
test_load_frozen_rejects_prereg_hash_mismatch (__main__.ProposedTests.test_load_frozen_rejects_prereg_hash_mismatch) ... ok
test_merge_loss_exception_requires_clean_gates (__main__.ProposedTests.test_merge_loss_exception_requires_clean_gates) ... ok
test_null_after_hash_mismatch_invalid (__main__.ProposedTests.test_null_after_hash_mismatch_invalid) ... ok
test_null_application_that_changes_band_halts_before_scoring (__main__.ProposedTests.test_null_application_that_changes_band_halts_before_scoring) ... ok
test_oracle_entry_requires_restored_band (__main__.ProposedTests.test_oracle_entry_requires_restored_band) ... ok
test_pass_routing_split_b_is_not_motivation (__main__.ProposedTests.test_pass_routing_split_b_is_not_motivation) ... ok
test_same_seed_band_crossing_at_61 (__main__.ProposedTests.test_same_seed_band_crossing_at_61) ... ok
test_trainer_projection_guard_fires_after_warmup_not_at_wall_limit (__main__.ProposedTests.test_trainer_projection_guard_fires_after_warmup_not_at_wall_limit) ... A7_canon_s0_r16 step 10 loss 1.0
A7_canon_s0_r16 step 20 loss 1.0
ok
test_trainer_verifies_preflight_before_torch (__main__.ProposedTests.test_trainer_verifies_preflight_before_torch) ... ok
test_warmup_is_linear_over_20_steps (__main__.ProposedTests.test_warmup_is_linear_over_20_steps) ... ok
test_G3_equality_passes_across_the_range (__main__.DefectTests.test_G3_equality_passes_across_the_range) ... ok
test_G3_hundredths_at_inside_and_outside_boundary (__main__.FixRoundTests.test_G3_hundredths_at_inside_and_outside_boundary) ... ok
test_LAW3_failure_persists_partial_readouts_and_boundary_controls (__main__.FixRoundTests.test_LAW3_failure_persists_partial_readouts_and_boundary_controls) ... C10W evaluation PASS controls; oracle measurement, not a route
C10W evaluation PASS controls; oracle measurement, not a route
ok
test_P1_516_minutes_refuses_and_counts_failed_attempts (__main__.FixRoundTests.test_P1_516_minutes_refuses_and_counts_failed_attempts) ... ok
test_P1_budget_ruling_requires_operator_identity (__main__.FixRoundTests.test_P1_budget_ruling_requires_operator_identity) ... ok
test_P2_diagnostic_failure_restores_function_instead_of_training_record (__main__.FixRoundTests.test_P2_diagnostic_failure_restores_function_instead_of_training_record) ... ok
test_all_eval_stages_check_budget_before_child_at_inside_outside (__main__.FixRoundTests.test_all_eval_stages_check_budget_before_child_at_inside_outside) ... ok
test_nonfinite_failure_preserves_reason_and_raw_diagnostic (__main__.FixRoundTests.test_nonfinite_failure_preserves_reason_and_raw_diagnostic) ... ok
test_null_hash_records_zero_application_before_restore_for_reader (__main__.FixRoundTests.test_null_hash_records_zero_application_before_restore_for_reader) ... ok
test_p1_project_invalid_record_returns_reader_verdict (__main__.FixRoundTests.test_p1_project_invalid_record_returns_reader_verdict) ... ok
test_setup_and_U_failures_keep_partial_evidence_and_cleanup (__main__.FixRoundTests.test_setup_and_U_failures_keep_partial_evidence_and_cleanup) ... ok
test_tracer_limits_local_line_events_to_recipe_and_original (__main__.FixRoundTests.test_tracer_limits_local_line_events_to_recipe_and_original) ... ok
test_training_guard_also_requires_P1_ruling_identity (__main__.FixRoundTests.test_training_guard_also_requires_P1_ruling_identity) ... ok
test_training_offline_environment_precedes_transformers_import (__main__.FixRoundTests.test_training_offline_environment_precedes_transformers_import) ... ok
test_unedited_saves_stimulus_before_leak_validation (__main__.FixRoundTests.test_unedited_saves_stimulus_before_leak_validation) ... ok
test_validity_failure_writes_eval_before_validation (__main__.FixRoundTests.test_validity_failure_writes_eval_before_validation) ... C10W evaluation PASS controls; oracle measurement, not a route
C10W evaluation PASS controls; oracle measurement, not a route
ok

----------------------------------------------------------------------
Ran 63 tests in 5.497s

OK
C10W_ORACLE_SELFTEST PASS: 63 tests; model-free; oracle measurement, not a route
```

GREEN — tiny CPU tensors
```text
$ /opt/homebrew/bin/rtk proxy .venv/bin/python -B experiments/track_c/c10w_oracle_torchcheck.py
test_nonzero_delta_applies_and_zero_entries_keep_their_bits (__main__.SignedZeroTests.test_nonzero_delta_applies_and_zero_entries_keep_their_bits) ... ok
test_quantized_zero_boundary (__main__.SignedZeroTests.test_quantized_zero_boundary) ... ok
test_zero_delta_preserves_every_fp16_byte (__main__.SignedZeroTests.test_zero_delta_preserves_every_fp16_byte) ... ok

----------------------------------------------------------------------
Ran 3 tests in 0.042s

OK
```

GREEN — preservation checks
```text
PROPOSED_SUITE PRESERVED: original 27 + proposed 20; DefectTests always on; 15 new fix-round regressions.
PROPOSED_VERBATIM_COPY_SHA256 e1d130bc56ab55d5db813ad49885af6272fbae6994684d1befb35fc09a261672
PROTECTED_HASHES PASS: 139 files; engine/prereg/harness/launcher/prior reports unchanged.
AST_SYNTAX PASS: six C10W Python files.
LAUNCHER_MODE PASS: 0755.
git diff --check (five allowed existing Python files): exit 0
```

Mutation result — supplied CPU-only harness; 48 killed / 1 survived / 49 total; survivor M49_trainer_preflight_law3_hi; baseline before and after PASS
```text
HARNESS /Users/robertrhu/.claude/jobs/8ac4cacf/tmp/c10w_mut/mutate.py
HARNESS_SHA256 037724063655579e9590bdb90c03762edf9d02a5fbe241cca401836d4a9fe273
CPU_ONLY model-free suite; scratch mirror relocated to /private/tmp; fixed source baseline; M07/M40 anchors retargeted without changing mutant meanings.
BASELINE		SURVIVED	
BASELINE_PRE PASS
M01_law3_A1A2_67	read.py:151	KILLED	test_law3_envelope_all_endpoints_and_controls
M02_law3_para_lo_strict	read.py:153	KILLED	test_LAW3_failure_persists_partial_readouts_and_boundary_controls,test_law3_envelope_all_endpoints_and_controls
M03_law3_canon_hi_strict	read.py:153	KILLED	test_law3_envelope_all_endpoints_and_controls
M04_stimulus_le4	read.py:149	KILLED	test_stimulus_law5_strict_restore_delegation_and_counters
M05_u_leak_le3	read.py:150	KILLED	test_stimulus_law5_strict_restore_delegation_and_counters
M06_G1_plus2	read.py:262	KILLED	test_G1_to_G7_both_sides
M07_G3_strict	read.py:264	KILLED	test_G1_to_G7_both_sides,test_G3_equality_passes_across_the_range,test_G3_hundredths_at_inside_and_outside_boundary
M08_G4_train_plus2	read.py:265	KILLED	test_G1_to_G7_both_sides
M09_G6_strict	read.py:267	KILLED	test_G1_to_G7_both_sides
M10_G7_le3	read.py:271	KILLED	test_G1_to_G7_both_sides
M11_band_61_boundary	read.py:276	KILLED	test_same_seed_band_crossing_at_61
M12_label_30_boundary	read.py:280	KILLED	test_all_final_label_table_rows,test_configuration_labels_and_integer_count_boundaries,test_routing_every_row_and_canonical_split
M13_pairing_ge15	read.py:366	KILLED	test_bigram_pairing_retry_and_merge_loss_qualifiers
M14_merge_ge5	read.py:369	KILLED	test_bigram_pairing_retry_and_merge_loss_qualifiers
M15_merge_exception_ignores_gates	read.py:372	KILLED	test_merge_loss_exception_requires_clean_gates
M16_seedgap_gt16	read.py:384	KILLED	test_all_final_label_table_rows,test_replication_minimum_seed_and_same_seed_boundaries
M17_sameseed_gt11	read.py:388	KILLED	test_replication_minimum_seed_and_same_seed_boundaries
M18_sameseed_gate_crossing_dropped	read.py:390	KILLED	test_replication_minimum_seed_and_same_seed_boundaries
M19_p3_on_locality_cost	read.py:421	KILLED	test_configuration_labels_and_integer_count_boundaries,test_no_gate_clean_reference_and_locality_cost_never_p3,test_replication_minimum_seed_and_same_seed_boundaries
M20_final_order_swap	read.py:431	KILLED	test_all_final_label_table_rows
M21_canon_split_gap16	read.py:401	KILLED	test_canonical_read_conditions_and_merge_loss
M22_pass_split_b_motivates	read.py:446	KILLED	test_pass_routing_split_b_is_not_motivation
M23_positive_control_67	read.py:349	KILLED	test_law3_envelope_all_endpoints_and_controls,test_validity_failure_writes_eval_before_validation
M24_law5i_le	read.py:321	KILLED	test_stimulus_law5_strict_restore_delegation_and_counters
M25_eval_wall_strict	read.py:114	KILLED	test_guards_projection_memory_and_eval_wall_boundaries
M26_auth_flag_dropped	read.py:125	KILLED	test_P2_P3_authorization_even_under_projection_limit
M27_auth_cert_check_dropped	read.py:574	KILLED	test_entry_preflight_and_training_provenance_precede_model_load
M28_latest_dir_ignores_HALT	read.py:479	KILLED	test_latest_directory_refuses_halted_phase
M29_prereg_sha_unchecked	read.py:486	KILLED	test_load_frozen_rejects_prereg_hash_mismatch
M30_null_hash_evidence_dropped	read.py:311	KILLED	test_null_after_hash_mismatch_invalid,test_null_hash_records_zero_application_before_restore_for_reader
M31_fit_gate_455	read.py:339	KILLED	test_fit_matched_controls_steps_and_provenance
M32_dispatch_no_authorization	step0.py:348	KILLED	test_dispatch_refuses_P2_without_authorization_before_creating_phase
M33_dispatch_P3_eligibility_dropped	step0.py:324	KILLED	test_P3_entry_requires_scientific_eligibility
M34_dispatch_no_prestart_guard	step0.py:370	KILLED	test_dispatch_refuses_training_unit_when_projection_exceeds_phase_limit
M35_dispatch_no_prior_unit_check	step0.py:365	KILLED	test_dispatch_refuses_out_of_order_training_unit
M36_seal_S2c_dropped	step0.py:71	KILLED	test_each_seal_rule_is_independently_binding
M37_seal_S3_061	step0.py:73	KILLED	test_each_seal_rule_is_independently_binding
M38_seal_synonyms_dropped	step0.py:62	KILLED	test_each_seal_rule_is_independently_binding
M39_eval_law3_not_called	eval.py:359	KILLED	test_LAW3_failure_persists_partial_readouts_and_boundary_controls,test_eval_law3_miss_halts_before_any_oracle_recipe
M40_eval_null_assert_dropped	eval.py:239	KILLED	test_null_application_that_changes_band_halts_before_scoring
M41_oracle_gate_flags_dropped	eval.py:34	KILLED	test_eval_seam_order_missing_adapter_and_hit_counters
M42_oracle_entry_assert_dropped	eval.py:35	KILLED	test_oracle_entry_requires_restored_band
M43_eval_adapter_hash_unverified	eval.py:98	KILLED	test_adapter_hash_verified_before_load
M44_eval_no_training_preflight	eval.py:347	KILLED	test_eval_verifies_preflight_certificate_before_model_load
M45_eval_P2_auth_dropped	eval.py:352	KILLED	test_eval_P2_rechecks_authorization
M46_trainer_no_preflight	train.py:142	KILLED	test_trainer_verifies_preflight_before_torch
M47_trainer_inrun_time_guard_dropped	train.py:216	KILLED	test_trainer_projection_guard_fires_after_warmup_not_at_wall_limit
M48_trainer_warmup_10	train.py:34	KILLED	test_warmup_is_linear_over_20_steps
M49_trainer_preflight_law3_hi	train.py:57	SURVIVED	
BASELINE		SURVIVED	
BASELINE_POST PASS
MUTATION_RESULT {"killed": 48, "survived": 1, "total": 49}
```
