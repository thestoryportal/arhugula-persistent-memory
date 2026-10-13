DONE

Scope 1 → `experiments/track_c/c10w_oracle_step0.py:205`, `:218`, `:220`, `:223`, `:229`: per-item metadata, derived once per subject from the existing dev identities; the five source indices remain in `dev_identities`. Exactly five rows, source order and duplicate occurrences preserved; zero through four and six rows halt. Whole-dev summary includes unsampled subjects. Later-repeat indices are `[53]`; both members of the real duplicate group are `[50, 53]`.
Tests → `experiments/track_c/c10w_oracle_selftest.py:1414` (`test_duplicate_five_rows_accepted_and_preserved_in_source_order`); `experiments/track_c/c10w_oracle_selftest.py:1431` (`test_four_dev_rows_refused_as_invalid_instrument`); `experiments/track_c/c10w_oracle_selftest.py:1435` (`test_six_dev_rows_refused_as_invalid_instrument`); `experiments/track_c/c10w_oracle_selftest.py:1439` (`test_zero_to_three_dev_rows_refused_as_invalid_instrument`); `experiments/track_c/c10w_oracle_selftest.py:1449` (`test_five_distinct_rows_keep_pre_amendment_prompt_bytes`); `experiments/track_c/c10w_oracle_selftest.py:1459` (`test_whole_dev_summary_includes_exactly_low_distinct_subjects`).
§9 → `docs/C10W_ORACLE_PREREG.md:538`: “For each sampled subject, step 0 requires **exactly five `dev` rows** — the subject's published five-shot set — and uses all five, in source order, including a row whose content duplicates another row. Fewer or more than five rows is INVALID-INSTRUMENT.” The same paragraph requires recorded distinct counts, duplicate source indices and the whole-dev summary.

Scope 2 → `experiments/track_c/c10w_oracle_read.py:20`: amended prereg hash pinned. Other invalidated code/test pins: none; phase fixtures consume this constant, step-0 source identities are computed at freezing, and the historical hash remains only as a rejection fixture.
Tests → `experiments/track_c/c10w_oracle_selftest.py:1480` (`test_reader_accepts_actual_amended_prereg_hash`); `experiments/track_c/c10w_oracle_selftest.py:1491` (`test_reader_rejects_old_prereg_hash`).
§9 → `docs/C10W_ORACLE_PREREG.md:548`: “The reader's frozen prereg SHA-256 is updated to this amended file.”
PREREG_SHA → `d2aa240eede4556395373678e4fab757e0e55d5491a7d4105ef765c1eb35d2f0`.

Scope 3 → `experiments/track_c/c10w_oracle_read.py:76`, `:86`, `:497`: existing full-record JSON persistence and file-hash verification retain the new fields; no field whitelist or evaluator change is needed.
Tests → `experiments/track_c/c10w_oracle_selftest.py:1469` (`test_producer_record_json_roundtrip_keeps_new_fields`); `experiments/track_c/c10w_oracle_selftest.py:1480` (`test_reader_accepts_actual_amended_prereg_hash`).
§9 → `docs/C10W_ORACLE_PREREG.md:538`: “For each sampled subject, `mmlu200.json` records the five `dev` source indices, the number of distinct rows (by row SHA-256) and the source indices of every duplicate; a top-level summary lists every subject of the whole `dev` split with fewer than five distinct rows.”

A → `experiments/track_c/c10w_oracle_step0.py:175`: no HEAD lookup; `:177`, `:179`, `:181`, `:184`, `:188`, `:189`, `:190`, `:192`: fixed revision, exact counts, canonical Parquet snapshot-path/revision and SHA checks. Original Arrow cache provenance is retained alongside canonical Parquet refs; logical canonical paths retain their basenames despite blob symlinks.
Tests → `experiments/track_c/c10w_oracle_selftest.py:1497` (`test_acquisition_pins_revision_counts_and_canonical_source_hashes_without_head`); `experiments/track_c/c10w_oracle_selftest.py:1508` (`test_each_split_count_off_by_one_is_invalid_instrument`); `experiments/track_c/c10w_oracle_selftest.py:1514` (`test_each_wrong_canonical_source_hash_is_invalid_instrument`); `experiments/track_c/c10w_oracle_selftest.py:1519` (`test_different_source_revision_is_invalid_instrument`).
§9 → `docs/C10W_ORACLE_PREREG.md:544`: “The rerun loads `all`/`test` and `all`/`dev` explicitly at `c30699e8356da336a370243923dbaf21066bb9fe`; it does not resolve a replacement HEAD.” That paragraph requires 14,042/285 rows, deterministic sampling, both pinned source-file hashes, and INVALID-INSTRUMENT on mismatch.

B → `experiments/track_c/c10w_oracle_step0.py:209`: duplicate metadata uses `identities["dev"][i]["row_sha256"]`, with no second row hash.
Tests → `experiments/track_c/c10w_oracle_selftest.py:1523` (`test_duplicates_use_existing_identity_hash_without_rehashing_rows`); `experiments/track_c/c10w_oracle_selftest.py:1414` (`test_duplicate_five_rows_accepted_and_preserved_in_source_order`). The producer makes exactly 14,042 + 285 identity-hash calls and 200 prompt-hash calls.
§9 → `docs/C10W_ORACLE_PREREG.md:544`: “Duplicates are defined by the one recorded row hash (`identities["dev"][i]["row_sha256"]`).”

C → `experiments/track_c/c10w_oracle_selftest.py:1534`: actual offline dataset acquisition and cached Qwen tokenizer call the complete production `freeze_mmlu`; every `R.require` site is counted. Cached Arrow inputs and metadata are copied to `/private/tmp` for loader locks; source Parquets and tokenizer are read from the repo cache. Tensor imports are blocked. Skips are permitted only for absent cached pinned dataset/tokenizer files; no skip occurred.
Tests → `experiments/track_c/c10w_oracle_selftest.py:1534` (`test_real_cached_acquisition_and_tokenizer_exercise_every_require`). Exactly one low-distinct subject (`college_physics`), duplicate group `[50, 53]`, affected sample `[1427, 1453]`, 0/200 suffix failures, 9/9 require sites.
§9 → `docs/C10W_ORACLE_PREREG.md:548`: “The driver change is made test-first: a synthetic case (five rows, two identical; four and six rows halt) and a real-data check on the cached pinned files (exactly one subject with fewer than five distinct rows, `college_physics`, duplicate indices [50, 53]; affected sampled items [1427, 1453]; 0 of 200 suffix failures).”

D → `experiments/track_c/c10w_oracle_read.py:408`, `:426`: `g6_sensitivity` reports every U/closed-form/oracle arm's full net loss, count and net loss excluding 1427/1453, affected source indices and signed contribution, with `report_only: true`. Existing G6, labels and routing are unchanged; diagnostic denominators reflect actual recorded identities.
Tests → `experiments/track_c/c10w_oracle_selftest.py:1594` (`test_report_only_198_sensitivity_keeps_full_200_gate_and_label`). Synthetic cases `(198 loss, affected contribution, 200 loss, label)` are `(2,+2,4,PASS-CEILING)`, `(3,+2,5,PARTIAL-CEILING-LOCALITY-COST)`, `(5,-1,4,PASS-CEILING)`, `(6,-2,4,PASS-CEILING)`; reader labels equal the existing full-200 configuration/replication label and inputs are not mutated.
§9 → `docs/C10W_ORACLE_PREREG.md:546`: “G6's net paired loss is also reported on the 198 items without the two affected `college_physics` items (1427, 1453), with their signed contribution, from the per-item correctness bits already recorded.”

RED → `.venv/bin/python -B experiments/track_c/c10w_oracle_selftest.py`; before implementation edits; 79 tests, FAILED (failures=25), exit 1. Verbatim output:

```text
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
test_acquisition_pins_revision_counts_and_canonical_source_hashes_without_head (__main__.DupDevTests.test_acquisition_pins_revision_counts_and_canonical_source_hashes_without_head) ... FAIL
test_different_source_revision_is_invalid_instrument (__main__.DupDevTests.test_different_source_revision_is_invalid_instrument) ... FAIL
test_duplicate_five_rows_accepted_and_preserved_in_source_order (__main__.DupDevTests.test_duplicate_five_rows_accepted_and_preserved_in_source_order) ... FAIL
test_duplicates_use_existing_identity_hash_without_rehashing_rows (__main__.DupDevTests.test_duplicates_use_existing_identity_hash_without_rehashing_rows) ... FAIL
test_each_split_count_off_by_one_is_invalid_instrument (__main__.DupDevTests.test_each_split_count_off_by_one_is_invalid_instrument) ... 
  test_each_split_count_off_by_one_is_invalid_instrument (__main__.DupDevTests.test_each_split_count_off_by_one_is_invalid_instrument) (split='test', delta=-1) ... FAIL
  test_each_split_count_off_by_one_is_invalid_instrument (__main__.DupDevTests.test_each_split_count_off_by_one_is_invalid_instrument) (split='test', delta=1) ... FAIL
  test_each_split_count_off_by_one_is_invalid_instrument (__main__.DupDevTests.test_each_split_count_off_by_one_is_invalid_instrument) (split='dev', delta=-1) ... FAIL
  test_each_split_count_off_by_one_is_invalid_instrument (__main__.DupDevTests.test_each_split_count_off_by_one_is_invalid_instrument) (split='dev', delta=1) ... FAIL
test_each_wrong_canonical_source_hash_is_invalid_instrument (__main__.DupDevTests.test_each_wrong_canonical_source_hash_is_invalid_instrument) ... 
  test_each_wrong_canonical_source_hash_is_invalid_instrument (__main__.DupDevTests.test_each_wrong_canonical_source_hash_is_invalid_instrument) (split='test') ... FAIL
  test_each_wrong_canonical_source_hash_is_invalid_instrument (__main__.DupDevTests.test_each_wrong_canonical_source_hash_is_invalid_instrument) (split='dev') ... FAIL
test_five_distinct_rows_keep_pre_amendment_prompt_bytes (__main__.DupDevTests.test_five_distinct_rows_keep_pre_amendment_prompt_bytes) ... FAIL
test_four_dev_rows_refused_as_invalid_instrument (__main__.DupDevTests.test_four_dev_rows_refused_as_invalid_instrument) ... FAIL
test_producer_record_json_roundtrip_keeps_new_fields (__main__.DupDevTests.test_producer_record_json_roundtrip_keeps_new_fields) ... FAIL
test_reader_accepts_actual_amended_prereg_hash (__main__.DupDevTests.test_reader_accepts_actual_amended_prereg_hash) ... FAIL
test_reader_rejects_old_prereg_hash (__main__.DupDevTests.test_reader_rejects_old_prereg_hash) ... ok
test_real_cached_acquisition_and_tokenizer_exercise_every_require (__main__.DupDevTests.test_real_cached_acquisition_and_tokenizer_exercise_every_require) ... FAIL
test_report_only_198_sensitivity_keeps_full_200_gate_and_label (__main__.DupDevTests.test_report_only_198_sensitivity_keeps_full_200_gate_and_label) ... 
  test_report_only_198_sensitivity_keeps_full_200_gate_and_label (__main__.DupDevTests.test_report_only_198_sensitivity_keeps_full_200_gate_and_label) (remaining=2, contribution=2) ... FAIL
  test_report_only_198_sensitivity_keeps_full_200_gate_and_label (__main__.DupDevTests.test_report_only_198_sensitivity_keeps_full_200_gate_and_label) (remaining=3, contribution=2) ... FAIL
  test_report_only_198_sensitivity_keeps_full_200_gate_and_label (__main__.DupDevTests.test_report_only_198_sensitivity_keeps_full_200_gate_and_label) (remaining=5, contribution=-1) ... FAIL
  test_report_only_198_sensitivity_keeps_full_200_gate_and_label (__main__.DupDevTests.test_report_only_198_sensitivity_keeps_full_200_gate_and_label) (remaining=6, contribution=-2) ... FAIL
test_six_dev_rows_refused_as_invalid_instrument (__main__.DupDevTests.test_six_dev_rows_refused_as_invalid_instrument) ... FAIL
test_whole_dev_summary_includes_exactly_low_distinct_subjects (__main__.DupDevTests.test_whole_dev_summary_includes_exactly_low_distinct_subjects) ... FAIL
test_zero_to_three_dev_rows_refused_as_invalid_instrument (__main__.DupDevTests.test_zero_to_three_dev_rows_refused_as_invalid_instrument) ... 
  test_zero_to_three_dev_rows_refused_as_invalid_instrument (__main__.DupDevTests.test_zero_to_three_dev_rows_refused_as_invalid_instrument) (count=0) ... FAIL
  test_zero_to_three_dev_rows_refused_as_invalid_instrument (__main__.DupDevTests.test_zero_to_three_dev_rows_refused_as_invalid_instrument) (count=1) ... FAIL
  test_zero_to_three_dev_rows_refused_as_invalid_instrument (__main__.DupDevTests.test_zero_to_three_dev_rows_refused_as_invalid_instrument) (count=2) ... FAIL
  test_zero_to_three_dev_rows_refused_as_invalid_instrument (__main__.DupDevTests.test_zero_to_three_dev_rows_refused_as_invalid_instrument) (count=3) ... FAIL

======================================================================
FAIL: test_acquisition_pins_revision_counts_and_canonical_source_hashes_without_head (__main__.DupDevTests.test_acquisition_pins_revision_counts_and_canonical_source_hashes_without_head)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1499, in test_acquisition_pins_revision_counts_and_canonical_source_hashes_without_head
    self.assertEqual(sources["head_calls"],[])
AssertionError: Lists differ: ['cais/mmlu'] != []

First list contains 1 additional elements.
First extra element 0:
'cais/mmlu'

- ['cais/mmlu']
+ []

======================================================================
FAIL: test_different_source_revision_is_invalid_instrument (__main__.DupDevTests.test_different_source_revision_is_invalid_instrument)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1520, in test_different_source_revision_is_invalid_instrument
    with self.assertRaisesRegex(R.Halt,"INVALID-INSTRUMENT:.*source revision"):
AssertionError: Halt not raised

======================================================================
FAIL: test_duplicate_five_rows_accepted_and_preserved_in_source_order (__main__.DupDevTests.test_duplicate_five_rows_accepted_and_preserved_in_source_order)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1395, in _accepted
    try: return self._producer(**kwargs)
                ^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1390, in _producer
    record = S.freeze_mmlu(Tokenizer())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_step0.py", line 199, in freeze_mmlu
    R.require(len(examples)==5 and len({R.sha_text(json.dumps(r,sort_keys=True)) for _,r in examples})==5,"INVALID-INSTRUMENT: exactly five distinct dev exemplars required")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_read.py", line 42, in require
    raise Halt("HALT: " + reason)
c10w_oracle_read.Halt: HALT: INVALID-INSTRUMENT: exactly five distinct dev exemplars required

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1415, in test_duplicate_five_rows_accepted_and_preserved_in_source_order
    record, sources = self._accepted()
                      ^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1396, in _accepted
    except R.Halt as exc: self.fail("published five-row fixture was refused: "+str(exc))
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: published five-row fixture was refused: HALT: INVALID-INSTRUMENT: exactly five distinct dev exemplars required

======================================================================
FAIL: test_duplicates_use_existing_identity_hash_without_rehashing_rows (__main__.DupDevTests.test_duplicates_use_existing_identity_hash_without_rehashing_rows)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1395, in _accepted
    try: return self._producer(**kwargs)
                ^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1390, in _producer
    record = S.freeze_mmlu(Tokenizer())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_step0.py", line 199, in freeze_mmlu
    R.require(len(examples)==5 and len({R.sha_text(json.dumps(r,sort_keys=True)) for _,r in examples})==5,"INVALID-INSTRUMENT: exactly five distinct dev exemplars required")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_read.py", line 42, in require
    raise Halt("HALT: " + reason)
c10w_oracle_read.Halt: HALT: INVALID-INSTRUMENT: exactly five distinct dev exemplars required

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1525, in test_duplicates_use_existing_identity_hash_without_rehashing_rows
    record,sources=self._accepted()
                   ^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1396, in _accepted
    except R.Halt as exc: self.fail("published five-row fixture was refused: "+str(exc))
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: published five-row fixture was refused: HALT: INVALID-INSTRUMENT: exactly five distinct dev exemplars required

======================================================================
FAIL: test_each_split_count_off_by_one_is_invalid_instrument (__main__.DupDevTests.test_each_split_count_off_by_one_is_invalid_instrument) (split='test', delta=-1)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1511, in test_each_split_count_off_by_one_is_invalid_instrument
    with self.subTest(split=split,delta=delta), self.assertRaisesRegex(R.Halt,"INVALID-INSTRUMENT:.*split count"):
AssertionError: Halt not raised

======================================================================
FAIL: test_each_split_count_off_by_one_is_invalid_instrument (__main__.DupDevTests.test_each_split_count_off_by_one_is_invalid_instrument) (split='test', delta=1)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1511, in test_each_split_count_off_by_one_is_invalid_instrument
    with self.subTest(split=split,delta=delta), self.assertRaisesRegex(R.Halt,"INVALID-INSTRUMENT:.*split count"):
AssertionError: Halt not raised

======================================================================
FAIL: test_each_split_count_off_by_one_is_invalid_instrument (__main__.DupDevTests.test_each_split_count_off_by_one_is_invalid_instrument) (split='dev', delta=-1)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1511, in test_each_split_count_off_by_one_is_invalid_instrument
    with self.subTest(split=split,delta=delta), self.assertRaisesRegex(R.Halt,"INVALID-INSTRUMENT:.*split count"):
AssertionError: Halt not raised

======================================================================
FAIL: test_each_split_count_off_by_one_is_invalid_instrument (__main__.DupDevTests.test_each_split_count_off_by_one_is_invalid_instrument) (split='dev', delta=1)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1511, in test_each_split_count_off_by_one_is_invalid_instrument
    with self.subTest(split=split,delta=delta), self.assertRaisesRegex(R.Halt,"INVALID-INSTRUMENT:.*split count"):
AssertionError: Halt not raised

======================================================================
FAIL: test_each_wrong_canonical_source_hash_is_invalid_instrument (__main__.DupDevTests.test_each_wrong_canonical_source_hash_is_invalid_instrument) (split='test')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1516, in test_each_wrong_canonical_source_hash_is_invalid_instrument
    with self.subTest(split=split), self.assertRaisesRegex(R.Halt,"INVALID-INSTRUMENT:.*source file hash"):
AssertionError: Halt not raised

======================================================================
FAIL: test_each_wrong_canonical_source_hash_is_invalid_instrument (__main__.DupDevTests.test_each_wrong_canonical_source_hash_is_invalid_instrument) (split='dev')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1516, in test_each_wrong_canonical_source_hash_is_invalid_instrument
    with self.subTest(split=split), self.assertRaisesRegex(R.Halt,"INVALID-INSTRUMENT:.*source file hash"):
AssertionError: Halt not raised

======================================================================
FAIL: test_five_distinct_rows_keep_pre_amendment_prompt_bytes (__main__.DupDevTests.test_five_distinct_rows_keep_pre_amendment_prompt_bytes)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1455, in test_five_distinct_rows_keep_pre_amendment_prompt_bytes
    self.assertIn("dev_distinct_n",item); self.assertIn("dev_duplicate_source_indices",item)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'dev_distinct_n' not found in {'subject': 'college_physics', 'question': 'college_physics question 2427', 'choices': ['choice A', 'choice B', 'choice C', 'choice D'], 'answer': 3, 'source_index': 1427, 'source_identity': {'source_index': 1427, 'row_sha256': '66e69fe8972d9141aa92aea08e1cd6f56886f8ee208ede7f7162980de5cc12ac'}, 'dev_identities': [{'source_index': 50, 'row_sha256': '527e51ae8bf4630b1b110d8f30786af315be2d5cd9d74767c56c0cdbfb5fbcf7'}, {'source_index': 51, 'row_sha256': '3c4e16be273593a1b91a059ae85e91e99215542bde346af8be79c0e7dd069e2a'}, {'source_index': 52, 'row_sha256': '086d79082d2bbe202ec5c78683335ac4594d1b41e25cfb495ebd4a33ea515a1f'}, {'source_index': 53, 'row_sha256': '5a0d3f31b00c4ab98eb846456a8ca9f560a126d44af26181a3fe25a7ed217ba2'}, {'source_index': 54, 'row_sha256': 'ac16531724a697d3835cf30e1b80e517703ac1d033679edb7196137f5fd98468'}], 'dev_examples': [{'subject': 'college_physics', 'question': 'college_physics question 0', 'choices': ['choice A', 'choice B', 'choice C', 'choice D'], 'answer': 0}, {'subject': 'college_physics', 'question': 'college_physics question 1', 'choices': ['choice A', 'choice B', 'choice C', 'choice D'], 'answer': 1}, {'subject': 'college_physics', 'question': 'college_physics question 2', 'choices': ['choice A', 'choice B', 'choice C', 'choice D'], 'answer': 2}, {'subject': 'college_physics', 'question': 'college_physics question 3', 'choices': ['choice A', 'choice B', 'choice C', 'choice D'], 'answer': 3}, {'subject': 'college_physics', 'question': 'college_physics question 4', 'choices': ['choice A', 'choice B', 'choice C', 'choice D'], 'answer': 0}], 'prompt': 'The following are multiple choice questions (with answers) about college physics.\n\ncollege_physics question 0\nA. choice A\nB. choice B\nC. choice C\nD. choice D\nAnswer: A\n\ncollege_physics question 1\nA. choice A\nB. choice B\nC. choice C\nD. choice D\nAnswer: B\n\ncollege_physics question 2\nA. choice A\nB. choice B\nC. choice C\nD. choice D\nAnswer: C\n\ncollege_physics question 3\nA. choice A\nB. choice B\nC. choice C\nD. choice D\nAnswer: D\n\ncollege_physics question 4\nA. choice A\nB. choice B\nC. choice C\nD. choice D\nAnswer: A\n\ncollege_physics question 2427\nA. choice A\nB. choice B\nC. choice C\nD. choice D\nAnswer:', 'prompt_utf8_sha256': 'ab97d07a5f03bfe5a555221c5c4897ac69ac6237feb850081202716eb5068124', 'prompt_ids': [84, 104, 101, 32, 102, 111, 108, 108, 111, 119, 105, 110, 103, 32, 97, 114, 101, 32, 109, 117, 108, 116, 105, 112, 108, 101, 32, 99, 104, 111, 105, 99, 101, 32, 113, 117, 101, 115, 116, 105, 111, 110, 115, 32, 40, 119, 105, 116, 104, 32, 97, 110, 115, 119, 101, 114, 115, 41, 32, 97, 98, 111, 117, 116, 32, 99, 111, 108, 108, 101, 103, 101, 32, 112, 104, 121, 115, 105, 99, 115, 46, 10, 10, 99, 111, 108, 108, 101, 103, 101, 95, 112, 104, 121, 115, 105, 99, 115, 32, 113, 117, 101, 115, 116, 105, 111, 110, 32, 48, 10, 65, 46, 32, 99, 104, 111, 105, 99, 101, 32, 65, 10, 66, 46, 32, 99, 104, 111, 105, 99, 101, 32, 66, 10, 67, 46, 32, 99, 104, 111, 105, 99, 101, 32, 67, 10, 68, 46, 32, 99, 104, 111, 105, 99, 101, 32, 68, 10, 65, 110, 115, 119, 101, 114, 58, 32, 65, 10, 10, 99, 111, 108, 108, 101, 103, 101, 95, 112, 104, 121, 115, 105, 99, 115, 32, 113, 117, 101, 115, 116, 105, 111, 110, 32, 49, 10, 65, 46, 32, 99, 104, 111, 105, 99, 101, 32, 65, 10, 66, 46, 32, 99, 104, 111, 105, 99, 101, 32, 66, 10, 67, 46, 32, 99, 104, 111, 105, 99, 101, 32, 67, 10, 68, 46, 32, 99, 104, 111, 105, 99, 101, 32, 68, 10, 65, 110, 115, 119, 101, 114, 58, 32, 66, 10, 10, 99, 111, 108, 108, 101, 103, 101, 95, 112, 104, 121, 115, 105, 99, 115, 32, 113, 117, 101, 115, 116, 105, 111, 110, 32, 50, 10, 65, 46, 32, 99, 104, 111, 105, 99, 101, 32, 65, 10, 66, 46, 32, 99, 104, 111, 105, 99, 101, 32, 66, 10, 67, 46, 32, 99, 104, 111, 105, 99, 101, 32, 67, 10, 68, 46, 32, 99, 104, 111, 105, 99, 101, 32, 68, 10, 65, 110, 115, 119, 101, 114, 58, 32, 67, 10, 10, 99, 111, 108, 108, 101, 103, 101, 95, 112, 104, 121, 115, 105, 99, 115, 32, 113, 117, 101, 115, 116, 105, 111, 110, 32, 51, 10, 65, 46, 32, 99, 104, 111, 105, 99, 101, 32, 65, 10, 66, 46, 32, 99, 104, 111, 105, 99, 101, 32, 66, 10, 67, 46, 32, 99, 104, 111, 105, 99, 101, 32, 67, 10, 68, 46, 32, 99, 104, 111, 105, 99, 101, 32, 68, 10, 65, 110, 115, 119, 101, 114, 58, 32, 68, 10, 10, 99, 111, 108, 108, 101, 103, 101, 95, 112, 104, 121, 115, 105, 99, 115, 32, 113, 117, 101, 115, 116, 105, 111, 110, 32, 52, 10, 65, 46, 32, 99, 104, 111, 105, 99, 101, 32, 65, 10, 66, 46, 32, 99, 104, 111, 105, 99, 101, 32, 66, 10, 67, 46, 32, 99, 104, 111, 105, 99, 101, 32, 67, 10, 68, 46, 32, 99, 104, 111, 105, 99, 101, 32, 68, 10, 65, 110, 115, 119, 101, 114, 58, 32, 65, 10, 10, 99, 111, 108, 108, 101, 103, 101, 95, 112, 104, 121, 115, 105, 99, 115, 32, 113, 117, 101, 115, 116, 105, 111, 110, 32, 50, 52, 50, 55, 10, 65, 46, 32, 99, 104, 111, 105, 99, 101, 32, 65, 10, 66, 46, 32, 99, 104, 111, 105, 99, 101, 32, 66, 10, 67, 46, 32, 99, 104, 111, 105, 99, 101, 32, 67, 10, 68, 46, 32, 99, 104, 111, 105, 99, 101, 32, 68, 10, 65, 110, 115, 119, 101, 114, 58]}

======================================================================
FAIL: test_four_dev_rows_refused_as_invalid_instrument (__main__.DupDevTests.test_four_dev_rows_refused_as_invalid_instrument)
----------------------------------------------------------------------
c10w_oracle_read.Halt: HALT: INVALID-INSTRUMENT: exactly five distinct dev exemplars required

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1432, in test_four_dev_rows_refused_as_invalid_instrument
    with self.assertRaisesRegex(R.Halt,"INVALID-INSTRUMENT: exactly five dev rows required"):
AssertionError: "INVALID-INSTRUMENT: exactly five dev rows required" does not match "HALT: INVALID-INSTRUMENT: exactly five distinct dev exemplars required"

======================================================================
FAIL: test_producer_record_json_roundtrip_keeps_new_fields (__main__.DupDevTests.test_producer_record_json_roundtrip_keeps_new_fields)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1395, in _accepted
    try: return self._producer(**kwargs)
                ^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1390, in _producer
    record = S.freeze_mmlu(Tokenizer())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_step0.py", line 199, in freeze_mmlu
    R.require(len(examples)==5 and len({R.sha_text(json.dumps(r,sort_keys=True)) for _,r in examples})==5,"INVALID-INSTRUMENT: exactly five distinct dev exemplars required")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_read.py", line 42, in require
    raise Halt("HALT: " + reason)
c10w_oracle_read.Halt: HALT: INVALID-INSTRUMENT: exactly five distinct dev exemplars required

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1470, in test_producer_record_json_roundtrip_keeps_new_fields
    record, sources = self._accepted()
                      ^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1396, in _accepted
    except R.Halt as exc: self.fail("published five-row fixture was refused: "+str(exc))
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: published five-row fixture was refused: HALT: INVALID-INSTRUMENT: exactly five distinct dev exemplars required

======================================================================
FAIL: test_reader_accepts_actual_amended_prereg_hash (__main__.DupDevTests.test_reader_accepts_actual_amended_prereg_hash)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1482, in test_reader_accepts_actual_amended_prereg_hash
    self.assertEqual(R.PREREG_SHA,actual)
AssertionError: '2baeb4e9865dd1080ecb5765652c5eae67336eca6047d93b4f5948545854c344' != 'd2aa240eede4556395373678e4fab757e0e55d5491a7d4105ef765c1eb35d2f0'
- 2baeb4e9865dd1080ecb5765652c5eae67336eca6047d93b4f5948545854c344
+ d2aa240eede4556395373678e4fab757e0e55d5491a7d4105ef765c1eb35d2f0


======================================================================
FAIL: test_real_cached_acquisition_and_tokenizer_exercise_every_require (__main__.DupDevTests.test_real_cached_acquisition_and_tokenizer_exercise_every_require)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1590, in test_real_cached_acquisition_and_tokenizer_exercise_every_require
    self.assertEqual(run.returncode,0,run.stdout+run.stderr)
AssertionError: 1 != 0 : None of PyTorch, TensorFlow >= 2.0, or Flax have been found. Models won't be available and only tokenizers, configuration and file/data utilities can be used.
Traceback (most recent call last):
  File "<string>", line 30, in <module>
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_step0.py", line 177, in freeze_mmlu
    revision=HfApi().dataset_info("cais/mmlu").sha
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/lib/python3.11/site-packages/huggingface_hub/utils/_validators.py", line 114, in _inner_fn
    return fn(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/lib/python3.11/site-packages/huggingface_hub/hf_api.py", line 2730, in dataset_info
    r = get_session().get(path, headers=headers, timeout=timeout, params=params)
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/lib/python3.11/site-packages/requests/sessions.py", line 671, in get
    return self.request("GET", url, params=params, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/lib/python3.11/site-packages/requests/sessions.py", line 651, in request
    resp = self.send(prep, **send_kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/lib/python3.11/site-packages/requests/sessions.py", line 784, in send
    r = adapter.send(request, **kwargs)
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/lib/python3.11/site-packages/huggingface_hub/utils/_http.py", line 107, in send
    raise OfflineModeIsEnabled(
huggingface_hub.errors.OfflineModeIsEnabled: Cannot reach https://huggingface.co/api/datasets/cais/mmlu: offline mode is enabled. To disable it, please unset the `HF_HUB_OFFLINE` environment variable.


======================================================================
FAIL: test_report_only_198_sensitivity_keeps_full_200_gate_and_label (__main__.DupDevTests.test_report_only_198_sensitivity_keeps_full_200_gate_and_label) (remaining=2, contribution=2)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1618, in test_report_only_198_sensitivity_keeps_full_200_gate_and_label
    self.assertIn("g6_sensitivity",reading)
AssertionError: 'g6_sensitivity' not found in {'class': 'ORACLE MEASUREMENT — not a route; never promotable as a write-engine result (D-C10r-rulings-3 (2))', 'decision_id': 'D-C10w-oracle', 'status': 'VALID', 'final_label': 'PASS-CEILING', 'routing': {'action': 'MOTIVATE-INDEPENDENT-STEPS-6-7-5b', 'h30_eligible': True, 'oracle_measurement_not_route': True, 'mechanism_attribution': False}, 'ranks': {'16': {'count': 61, 'seed_counts': [61, 61], 'configurations': [{'count': 61, 'gates': {'G1': True, 'G2': True, 'G3': True, 'G4': True, 'G5': True, 'G6': True, 'G7': True}, 'gate_misses': [], 'label': 'PASS-CEILING', 'qualifiers': [], 'unstable_merge': False, 'mounted_count': 61, 'steps': 400, 'per_template_counts': [21, 20, 20], 'per_fact_counts': [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 0, 0, 0], 'per_edge_pass': [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, False, False, False, False], 'gain_over_closedform': 49}, {'count': 61, 'gates': {'G1': True, 'G2': True, 'G3': True, 'G4': True, 'G5': True, 'G6': True, 'G7': True}, 'gate_misses': [], 'label': 'PASS-CEILING', 'qualifiers': [], 'unstable_merge': False, 'mounted_count': 61, 'steps': 400, 'per_template_counts': [21, 20, 20], 'per_fact_counts': [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 0, 0, 0], 'per_edge_pass': [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, False, False, False, False], 'gain_over_closedform': 49}], 'same_seed': {'count': 61, 'gates': {'G1': True, 'G2': True, 'G3': True, 'G4': True, 'G5': True, 'G6': True, 'G7': True}, 'gate_misses': [], 'label': 'PASS-CEILING', 'qualifiers': [], 'unstable_merge': False, 'mounted_count': 61, 'steps': 400, 'per_template_counts': [21, 20, 20], 'per_fact_counts': [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 0, 0, 0], 'per_edge_pass': [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, False, False, False, False], 'gain_over_closedform': 49}, 'gate_misses': [], 'label': 'PASS-CEILING', 'qualifiers': [], 'stable': True, 'instability': []}}, 'p3_required': False, 'canon_split': 'a', 'reference_count': 30, 'reference_status': 'O-A7-CANON-REFERENCE', 'c10_status': 'OPEN/BLOCKING', 'f1_changed': False}

======================================================================
FAIL: test_report_only_198_sensitivity_keeps_full_200_gate_and_label (__main__.DupDevTests.test_report_only_198_sensitivity_keeps_full_200_gate_and_label) (remaining=3, contribution=2)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1618, in test_report_only_198_sensitivity_keeps_full_200_gate_and_label
    self.assertIn("g6_sensitivity",reading)
AssertionError: 'g6_sensitivity' not found in {'class': 'ORACLE MEASUREMENT — not a route; never promotable as a write-engine result (D-C10r-rulings-3 (2))', 'decision_id': 'D-C10w-oracle', 'status': 'VALID', 'final_label': 'PARTIAL-CEILING-LOCALITY-COST', 'routing': {'action': 'INDEPENDENT-PREREG-ONLY', 'h30_eligible': False, 'oracle_measurement_not_route': True, 'mechanism_attribution': False}, 'ranks': {'16': {'count': 61, 'seed_counts': [61, 61], 'configurations': [{'count': 61, 'gates': {'G1': True, 'G2': True, 'G3': True, 'G4': True, 'G5': True, 'G6': False, 'G7': True}, 'gate_misses': ['G6'], 'label': 'PARTIAL-CEILING-LOCALITY-COST', 'qualifiers': [], 'unstable_merge': False, 'mounted_count': 61, 'steps': 400, 'per_template_counts': [21, 20, 20], 'per_fact_counts': [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 0, 0, 0], 'per_edge_pass': [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, False, False, False, False], 'gain_over_closedform': 49}, {'count': 61, 'gates': {'G1': True, 'G2': True, 'G3': True, 'G4': True, 'G5': True, 'G6': False, 'G7': True}, 'gate_misses': ['G6'], 'label': 'PARTIAL-CEILING-LOCALITY-COST', 'qualifiers': [], 'unstable_merge': False, 'mounted_count': 61, 'steps': 400, 'per_template_counts': [21, 20, 20], 'per_fact_counts': [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 0, 0, 0], 'per_edge_pass': [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, False, False, False, False], 'gain_over_closedform': 49}], 'same_seed': {'count': 61, 'gates': {'G1': True, 'G2': True, 'G3': True, 'G4': True, 'G5': True, 'G6': False, 'G7': True}, 'gate_misses': ['G6'], 'label': 'PARTIAL-CEILING-LOCALITY-COST', 'qualifiers': [], 'unstable_merge': False, 'mounted_count': 61, 'steps': 400, 'per_template_counts': [21, 20, 20], 'per_fact_counts': [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 0, 0, 0], 'per_edge_pass': [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, False, False, False, False], 'gain_over_closedform': 49}, 'gate_misses': ['G6'], 'label': 'PARTIAL-CEILING-LOCALITY-COST', 'qualifiers': [], 'stable': True, 'instability': []}}, 'p3_required': False, 'canon_split': 'c', 'reference_count': None, 'reference_status': 'NO-GATE-CLEAN-REFERENCE', 'c10_status': 'OPEN/BLOCKING', 'f1_changed': False}

======================================================================
FAIL: test_report_only_198_sensitivity_keeps_full_200_gate_and_label (__main__.DupDevTests.test_report_only_198_sensitivity_keeps_full_200_gate_and_label) (remaining=5, contribution=-1)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1618, in test_report_only_198_sensitivity_keeps_full_200_gate_and_label
    self.assertIn("g6_sensitivity",reading)
AssertionError: 'g6_sensitivity' not found in {'class': 'ORACLE MEASUREMENT — not a route; never promotable as a write-engine result (D-C10r-rulings-3 (2))', 'decision_id': 'D-C10w-oracle', 'status': 'VALID', 'final_label': 'PASS-CEILING', 'routing': {'action': 'MOTIVATE-INDEPENDENT-STEPS-6-7-5b', 'h30_eligible': True, 'oracle_measurement_not_route': True, 'mechanism_attribution': False}, 'ranks': {'16': {'count': 61, 'seed_counts': [61, 61], 'configurations': [{'count': 61, 'gates': {'G1': True, 'G2': True, 'G3': True, 'G4': True, 'G5': True, 'G6': True, 'G7': True}, 'gate_misses': [], 'label': 'PASS-CEILING', 'qualifiers': [], 'unstable_merge': False, 'mounted_count': 61, 'steps': 400, 'per_template_counts': [21, 20, 20], 'per_fact_counts': [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 0, 0, 0], 'per_edge_pass': [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, False, False, False, False], 'gain_over_closedform': 49}, {'count': 61, 'gates': {'G1': True, 'G2': True, 'G3': True, 'G4': True, 'G5': True, 'G6': True, 'G7': True}, 'gate_misses': [], 'label': 'PASS-CEILING', 'qualifiers': [], 'unstable_merge': False, 'mounted_count': 61, 'steps': 400, 'per_template_counts': [21, 20, 20], 'per_fact_counts': [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 0, 0, 0], 'per_edge_pass': [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, False, False, False, False], 'gain_over_closedform': 49}], 'same_seed': {'count': 61, 'gates': {'G1': True, 'G2': True, 'G3': True, 'G4': True, 'G5': True, 'G6': True, 'G7': True}, 'gate_misses': [], 'label': 'PASS-CEILING', 'qualifiers': [], 'unstable_merge': False, 'mounted_count': 61, 'steps': 400, 'per_template_counts': [21, 20, 20], 'per_fact_counts': [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 0, 0, 0], 'per_edge_pass': [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, False, False, False, False], 'gain_over_closedform': 49}, 'gate_misses': [], 'label': 'PASS-CEILING', 'qualifiers': [], 'stable': True, 'instability': []}}, 'p3_required': False, 'canon_split': 'a', 'reference_count': 30, 'reference_status': 'O-A7-CANON-REFERENCE', 'c10_status': 'OPEN/BLOCKING', 'f1_changed': False}

======================================================================
FAIL: test_report_only_198_sensitivity_keeps_full_200_gate_and_label (__main__.DupDevTests.test_report_only_198_sensitivity_keeps_full_200_gate_and_label) (remaining=6, contribution=-2)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1618, in test_report_only_198_sensitivity_keeps_full_200_gate_and_label
    self.assertIn("g6_sensitivity",reading)
AssertionError: 'g6_sensitivity' not found in {'class': 'ORACLE MEASUREMENT — not a route; never promotable as a write-engine result (D-C10r-rulings-3 (2))', 'decision_id': 'D-C10w-oracle', 'status': 'VALID', 'final_label': 'PASS-CEILING', 'routing': {'action': 'MOTIVATE-INDEPENDENT-STEPS-6-7-5b', 'h30_eligible': True, 'oracle_measurement_not_route': True, 'mechanism_attribution': False}, 'ranks': {'16': {'count': 61, 'seed_counts': [61, 61], 'configurations': [{'count': 61, 'gates': {'G1': True, 'G2': True, 'G3': True, 'G4': True, 'G5': True, 'G6': True, 'G7': True}, 'gate_misses': [], 'label': 'PASS-CEILING', 'qualifiers': [], 'unstable_merge': False, 'mounted_count': 61, 'steps': 400, 'per_template_counts': [21, 20, 20], 'per_fact_counts': [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 0, 0, 0], 'per_edge_pass': [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, False, False, False, False], 'gain_over_closedform': 49}, {'count': 61, 'gates': {'G1': True, 'G2': True, 'G3': True, 'G4': True, 'G5': True, 'G6': True, 'G7': True}, 'gate_misses': [], 'label': 'PASS-CEILING', 'qualifiers': [], 'unstable_merge': False, 'mounted_count': 61, 'steps': 400, 'per_template_counts': [21, 20, 20], 'per_fact_counts': [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 0, 0, 0], 'per_edge_pass': [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, False, False, False, False], 'gain_over_closedform': 49}], 'same_seed': {'count': 61, 'gates': {'G1': True, 'G2': True, 'G3': True, 'G4': True, 'G5': True, 'G6': True, 'G7': True}, 'gate_misses': [], 'label': 'PASS-CEILING', 'qualifiers': [], 'unstable_merge': False, 'mounted_count': 61, 'steps': 400, 'per_template_counts': [21, 20, 20], 'per_fact_counts': [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 0, 0, 0], 'per_edge_pass': [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, False, False, False, False], 'gain_over_closedform': 49}, 'gate_misses': [], 'label': 'PASS-CEILING', 'qualifiers': [], 'stable': True, 'instability': []}}, 'p3_required': False, 'canon_split': 'a', 'reference_count': 30, 'reference_status': 'O-A7-CANON-REFERENCE', 'c10_status': 'OPEN/BLOCKING', 'f1_changed': False}

======================================================================
FAIL: test_six_dev_rows_refused_as_invalid_instrument (__main__.DupDevTests.test_six_dev_rows_refused_as_invalid_instrument)
----------------------------------------------------------------------
c10w_oracle_read.Halt: HALT: INVALID-INSTRUMENT: exactly five distinct dev exemplars required

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1436, in test_six_dev_rows_refused_as_invalid_instrument
    with self.assertRaisesRegex(R.Halt,"INVALID-INSTRUMENT: exactly five dev rows required"):
AssertionError: "INVALID-INSTRUMENT: exactly five dev rows required" does not match "HALT: INVALID-INSTRUMENT: exactly five distinct dev exemplars required"

======================================================================
FAIL: test_whole_dev_summary_includes_exactly_low_distinct_subjects (__main__.DupDevTests.test_whole_dev_summary_includes_exactly_low_distinct_subjects)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1395, in _accepted
    try: return self._producer(**kwargs)
                ^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1390, in _producer
    record = S.freeze_mmlu(Tokenizer())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_step0.py", line 199, in freeze_mmlu
    R.require(len(examples)==5 and len({R.sha_text(json.dumps(r,sort_keys=True)) for _,r in examples})==5,"INVALID-INSTRUMENT: exactly five distinct dev exemplars required")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_read.py", line 42, in require
    raise Halt("HALT: " + reason)
c10w_oracle_read.Halt: HALT: INVALID-INSTRUMENT: exactly five distinct dev exemplars required

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1460, in test_whole_dev_summary_includes_exactly_low_distinct_subjects
    record, sources = self._accepted()
                      ^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1396, in _accepted
    except R.Halt as exc: self.fail("published five-row fixture was refused: "+str(exc))
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: published five-row fixture was refused: HALT: INVALID-INSTRUMENT: exactly five distinct dev exemplars required

======================================================================
FAIL: test_zero_to_three_dev_rows_refused_as_invalid_instrument (__main__.DupDevTests.test_zero_to_three_dev_rows_refused_as_invalid_instrument) (count=0)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1442, in test_zero_to_three_dev_rows_refused_as_invalid_instrument
    try: self._producer(dev_count=count,duplicate=False)
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1390, in _producer
    record = S.freeze_mmlu(Tokenizer())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_step0.py", line 198, in freeze_mmlu
    row=checked(test[index]); examples=by_subject[row["subject"]]
                                       ~~~~~~~~~~^^^^^^^^^^^^^^^^
KeyError: 'college_physics'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1446, in test_zero_to_three_dev_rows_refused_as_invalid_instrument
    self.fail("missing dev set must halt as INVALID-INSTRUMENT: "+str(exc))
AssertionError: missing dev set must halt as INVALID-INSTRUMENT: 'college_physics'

======================================================================
FAIL: test_zero_to_three_dev_rows_refused_as_invalid_instrument (__main__.DupDevTests.test_zero_to_three_dev_rows_refused_as_invalid_instrument) (count=1)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1442, in test_zero_to_three_dev_rows_refused_as_invalid_instrument
    try: self._producer(dev_count=count,duplicate=False)
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1390, in _producer
    record = S.freeze_mmlu(Tokenizer())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_step0.py", line 199, in freeze_mmlu
    R.require(len(examples)==5 and len({R.sha_text(json.dumps(r,sort_keys=True)) for _,r in examples})==5,"INVALID-INSTRUMENT: exactly five distinct dev exemplars required")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_read.py", line 42, in require
    raise Halt("HALT: " + reason)
c10w_oracle_read.Halt: HALT: INVALID-INSTRUMENT: exactly five distinct dev exemplars required

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1444, in test_zero_to_three_dev_rows_refused_as_invalid_instrument
    self.assertIn("INVALID-INSTRUMENT: exactly five dev rows required",str(exc))
AssertionError: 'INVALID-INSTRUMENT: exactly five dev rows required' not found in 'HALT: INVALID-INSTRUMENT: exactly five distinct dev exemplars required'

======================================================================
FAIL: test_zero_to_three_dev_rows_refused_as_invalid_instrument (__main__.DupDevTests.test_zero_to_three_dev_rows_refused_as_invalid_instrument) (count=2)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1442, in test_zero_to_three_dev_rows_refused_as_invalid_instrument
    try: self._producer(dev_count=count,duplicate=False)
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1390, in _producer
    record = S.freeze_mmlu(Tokenizer())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_step0.py", line 199, in freeze_mmlu
    R.require(len(examples)==5 and len({R.sha_text(json.dumps(r,sort_keys=True)) for _,r in examples})==5,"INVALID-INSTRUMENT: exactly five distinct dev exemplars required")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_read.py", line 42, in require
    raise Halt("HALT: " + reason)
c10w_oracle_read.Halt: HALT: INVALID-INSTRUMENT: exactly five distinct dev exemplars required

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1444, in test_zero_to_three_dev_rows_refused_as_invalid_instrument
    self.assertIn("INVALID-INSTRUMENT: exactly five dev rows required",str(exc))
AssertionError: 'INVALID-INSTRUMENT: exactly five dev rows required' not found in 'HALT: INVALID-INSTRUMENT: exactly five distinct dev exemplars required'

======================================================================
FAIL: test_zero_to_three_dev_rows_refused_as_invalid_instrument (__main__.DupDevTests.test_zero_to_three_dev_rows_refused_as_invalid_instrument) (count=3)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1442, in test_zero_to_three_dev_rows_refused_as_invalid_instrument
    try: self._producer(dev_count=count,duplicate=False)
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1390, in _producer
    record = S.freeze_mmlu(Tokenizer())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_step0.py", line 199, in freeze_mmlu
    R.require(len(examples)==5 and len({R.sha_text(json.dumps(r,sort_keys=True)) for _,r in examples})==5,"INVALID-INSTRUMENT: exactly five distinct dev exemplars required")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_read.py", line 42, in require
    raise Halt("HALT: " + reason)
c10w_oracle_read.Halt: HALT: INVALID-INSTRUMENT: exactly five distinct dev exemplars required

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1444, in test_zero_to_three_dev_rows_refused_as_invalid_instrument
    self.assertIn("INVALID-INSTRUMENT: exactly five dev rows required",str(exc))
AssertionError: 'INVALID-INSTRUMENT: exactly five dev rows required' not found in 'HALT: INVALID-INSTRUMENT: exactly five distinct dev exemplars required'

----------------------------------------------------------------------
Ran 79 tests in 8.021s

FAILED (failures=25)
EXIT_CODE=1
```

GREEN → `.venv/bin/python -B experiments/track_c/c10w_oracle_selftest.py`; 79 tests, OK, exit 0. Verbatim output:

```text
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
test_acquisition_pins_revision_counts_and_canonical_source_hashes_without_head (__main__.DupDevTests.test_acquisition_pins_revision_counts_and_canonical_source_hashes_without_head) ... ok
test_different_source_revision_is_invalid_instrument (__main__.DupDevTests.test_different_source_revision_is_invalid_instrument) ... ok
test_duplicate_five_rows_accepted_and_preserved_in_source_order (__main__.DupDevTests.test_duplicate_five_rows_accepted_and_preserved_in_source_order) ... ok
test_duplicates_use_existing_identity_hash_without_rehashing_rows (__main__.DupDevTests.test_duplicates_use_existing_identity_hash_without_rehashing_rows) ... ok
test_each_split_count_off_by_one_is_invalid_instrument (__main__.DupDevTests.test_each_split_count_off_by_one_is_invalid_instrument) ... ok
test_each_wrong_canonical_source_hash_is_invalid_instrument (__main__.DupDevTests.test_each_wrong_canonical_source_hash_is_invalid_instrument) ... ok
test_five_distinct_rows_keep_pre_amendment_prompt_bytes (__main__.DupDevTests.test_five_distinct_rows_keep_pre_amendment_prompt_bytes) ... ok
test_four_dev_rows_refused_as_invalid_instrument (__main__.DupDevTests.test_four_dev_rows_refused_as_invalid_instrument) ... ok
test_producer_record_json_roundtrip_keeps_new_fields (__main__.DupDevTests.test_producer_record_json_roundtrip_keeps_new_fields) ... ok
test_reader_accepts_actual_amended_prereg_hash (__main__.DupDevTests.test_reader_accepts_actual_amended_prereg_hash) ... ok
test_reader_rejects_old_prereg_hash (__main__.DupDevTests.test_reader_rejects_old_prereg_hash) ... ok
test_real_cached_acquisition_and_tokenizer_exercise_every_require (__main__.DupDevTests.test_real_cached_acquisition_and_tokenizer_exercise_every_require) ... C10W_DUPDEV_REAL_DATA PASS: test=14042 dev=285 subject=college_physics duplicate_group=[50, 53] affected=[1427, 1453] suffix_failures=0/200 require_sites=9/9; offline; no tensor imports or model load
ok
test_report_only_198_sensitivity_keeps_full_200_gate_and_label (__main__.DupDevTests.test_report_only_198_sensitivity_keeps_full_200_gate_and_label) ... ok
test_six_dev_rows_refused_as_invalid_instrument (__main__.DupDevTests.test_six_dev_rows_refused_as_invalid_instrument) ... ok
test_whole_dev_summary_includes_exactly_low_distinct_subjects (__main__.DupDevTests.test_whole_dev_summary_includes_exactly_low_distinct_subjects) ... ok
test_zero_to_three_dev_rows_refused_as_invalid_instrument (__main__.DupDevTests.test_zero_to_three_dev_rows_refused_as_invalid_instrument) ... ok

----------------------------------------------------------------------
Ran 79 tests in 9.449s

OK
C10W_ORACLE_SELFTEST PASS: 79 tests; model-free; oracle measurement, not a route
EXIT_CODE=0
```

GREEN → `.venv/bin/python -B experiments/track_c/c10w_oracle_torchcheck.py`; 3 CPU tests, OK, exit 0. Verbatim output:

```text
test_nonzero_delta_applies_and_zero_entries_keep_their_bits (__main__.SignedZeroTests.test_nonzero_delta_applies_and_zero_entries_keep_their_bits) ... ok
test_quantized_zero_boundary (__main__.SignedZeroTests.test_quantized_zero_boundary) ... ok
test_zero_delta_preserves_every_fp16_byte (__main__.SignedZeroTests.test_zero_delta_preserves_every_fp16_byte) ... ok

----------------------------------------------------------------------
Ran 3 tests in 0.041s

OK
EXIT_CODE=0
```

GREEN → protected-file SHA check, exit 0:

```text
protected_research_files_checked 148 differences []
reader_pin_match True
shared_graft_cache_drift ["graft/.cache/extract.c3679fb5d24a63a0.json", "graft/.cache/fingerprint.c3679fb5d24a63a0.json", "graft/.cache/stats.json", "graft/.cache/ask-index.json", "graft/.cache/session/ecc3585e-98b4-435a-8cd5-469bb3bd9851.json", "graft/.cache/session/01a11696-15d1-7ac1-9d58-28340febd456.json", "graft/.cache/session/01a11808-1d14-7ef2-a2e4-9a12ba874205.json"]
```

Mutation result → supplied `/Users/robertrhu/.claude/jobs/8ac4cacf/tmp/c10w_mut/mutate.py` runs CPU-only. Scratch copy `/private/tmp/c10w_dupdev_mut_2t5f05o6/mutate.py` uses current pristine sources, validates test transcripts/baseline exit codes, and adds/runs the three required mutants. Each literal target matches exactly once; 3 killed, 0 survived; the 49 pre-existing mutants were not rerun. Both baseline runs pass all 79 tests. Verbatim output:

```text
M50_drop_five_row_check target_matches=1 step0.py:218
M51_dedupe_prompt target_matches=1 step0.py:220
M52_drop_duplicate_record target_matches=1 step0.py:212
BASELINE		SURVIVED	
M50_drop_five_row_check	step0.py:218	KILLED	test_four_dev_rows_refused_as_invalid_instrument,test_six_dev_rows_refused_as_invalid_instrument,test_zero_to_three_dev_rows_refused_as_invalid_instrument
M51_dedupe_prompt	step0.py:220	KILLED	test_duplicate_five_rows_accepted_and_preserved_in_source_order
M52_drop_duplicate_record	step0.py:212	KILLED	test_duplicate_five_rows_accepted_and_preserved_in_source_order,test_duplicates_use_existing_identity_hash_without_rehashing_rows,test_five_distinct_rows_keep_pre_amendment_prompt_bytes,test_producer_record_json_roundtrip_keeps_new_fields,test_real_cached_acquisition_and_tokenizer_exercise_every_require,test_whole_dev_summary_includes_exactly_low_distinct_subjects
BASELINE		SURVIVED
EXIT_CODE=0
```
