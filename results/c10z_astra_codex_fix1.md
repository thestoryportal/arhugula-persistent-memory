DONE

| Item | Changed file:line | Enforcing tests/check | Frozen prereg line |
|---|---|---|---|
| B1: validate go before mkdir/launch; copy JSON to launch; bind exact-byte SHA-256 into H_in | `experiments/track_c/c10z_astra_arms.py:1342`, `:1466`, `:1469`, `:1393`, `:1163`; `experiments/track_c/c10z_astra_read.py:21`, `:373`; `tools/run_c10z_stage.sh:12` | `test_B1_stage0_refuses_without_recorded_go_decision`; `test_fix1_go_malformed_fields_refuse_without_any_attempt_write`; `test_fix1_go_launch_copy_and_manifest_sha`; `test_fix1_go_sha_is_mandatory_reader_provenance`; `test_fix1_shell_preserves_go_env_absolute_outdir_and_no_refusal_write` | `docs/C10Z_ASTRA_PREREG.md:3`, `:137`, `:341–344` |
| B2: refusal exits 2 without diagnostic or attempt mutation; halt sidecar preserves completed pass; watchdog embeds last published record; HALT governs with observations retained | `experiments/track_c/c10z_astra_arms.py:1524`, `:1378`, `:1380`; `experiments/track_c/c10z_astra_read.py:669`, `:673`, `:676`; `tools/run_c10z_stage.sh:12` | `test_B2_stray_stage_call_after_terminal_K1_keeps_the_result`; `test_fix1_refusals_preserve_finished_attempt_byte_for_byte`; `test_fix1_halt_sidecar_retains_completed_observations_for_both_processes`; `test_fix1_watchdog_preserves_last_published_record`; `test_fix1_shell_preserves_go_env_absolute_outdir_and_no_refusal_write` | `docs/C10Z_ASTRA_PREREG.md:123`, `:137`, `:196`, `:204`, `:267`, `:323` |
| B3: classify with recorded ceilings; absent next ceiling terminates clean stage 1 with -STAGE1 or stage 2 with -SINGLE-PROCESS; explicit ABSENT-CEILING omissions; resident uses existing K1 close path | `experiments/track_c/c10z_astra_read.py:567`, `:574`, `:576`, `:586`, `:608`, `:609`; `experiments/track_c/c10z_astra_arms.py:1242`, `:1248` | `test_B3_clean_survivor_without_stage2_ceiling_keeps_stage1_record`; `test_fix1_absent_ceilings_terminal_labels_and_resident_close`; `test_k1_k2_omissions_and_replication` | `docs/C10Z_ASTRA_PREREG.md:196`, `:265–267` |
| B4: adopt proposed 60-test suite verbatim; add 3 always-on blocking demos and 9 fix regressions (72 tests) | `experiments/track_c/c10z_astra_selftest.py:907`, `:1166`, `:1225`, `:1310` | Proposed-prefix byte comparison PASS; `test_review_stage0_law3_gate_precedes_all_new_work`; `test_review_Z5_footprint_rejects_any_write_outside_selected_columns`; `test_review_Z6_restore_covers_all_36_and_verify_detects_drift`; `test_review_wrapper_delegates_under_standing_law5`; `test_review_write_round_cap_columns_and_capacity`; `test_review_write_prestart_projection_refuses_before_observation`; `test_review_stage1_round_over_120s_halts_in_run`; `test_review_stage_call_refusals`; `test_review_reader_instrument_ceilings_audits_and_capacity`; `test_review_cross_process_replication_needs_clean_pair` | `docs/C10Z_ASTRA_PREREG.md:79–81`, `:112`, `:120`, `:123`, `:127`, `:129`, `:137`, `:147–158`, `:196–198`, `:216`, `:265–267`, `:277` |
| A5: conditional change does not apply | No change | `git show e58cebf -- docs/C10Z_ASTRA_PREREG.md`: v2.2 pins stage 0–1 before model import, not to the parent's launch | `docs/C10Z_ASTRA_PREREG.md:196` |
| A6: absolute OUT_DIR at parse and shell handoff, before harness import/chdir | `experiments/track_c/c10z_astra_arms.py:1519`, `:1462`; `tools/run_c10z_stage.sh:10` | `test_fix1_relative_outdir_resolved_at_main_parse`; `test_fix1_shell_preserves_go_env_absolute_outdir_and_no_refusal_write` | `docs/C10Z_ASTRA_PREREG.md:137`, `:204` |
| A9: correct held-out-read comment | `experiments/track_c/c10z_astra_arms.py:674` | Comment/code comparison at `experiments/track_c/c10z_astra_arms.py:814`–`:819`; comment-only change | `docs/C10Z_ASTRA_PREREG.md:124`, `:166` |

RED — .venv/bin/python -B experiments/track_c/c10z_astra_selftest.py — exit 1

```text
test_00_implementation_exists (__main__.SpecTests.test_00_implementation_exists)
Prereg :204: actual driver, reader and stage wrapper exist. ... ok
test_band_boundaries_ordered (__main__.SpecTests.test_band_boundaries_ordered)
Prereg :112, :284: fit -> capacity -> locality -> three exhaustive BAND rows. ... ok
test_budget_origins_prestart_deadlines_round_memory (__main__.SpecTests.test_budget_origins_prestart_deadlines_round_memory)
Prereg :190, :196–198: 5400 seconds, scopes, unknown allowance, exact memory. ... C10Z_PROJECTION {"origins": {"stage01": 100.0}, "ceilings": {"stage01": 5400.0, "stage2": 60.0, "stage3": 6000.0}, "components_s": {"remaining": 1.0}, "scopes": {"stage01": {"elapsed_s": 5399.0, "remaining_s": 1.0, "ceiling_s": 5400.0}}}
C10Z_PROJECTION {"origins": {"stage01": 100.0}, "ceilings": {"stage01": 5400.0, "stage2": 60.0, "stage3": 6000.0}, "components_s": {"remaining": 1.001}, "scopes": {"stage01": {"elapsed_s": 5399.0, "remaining_s": 1.001, "ceiling_s": 5400.0}}}
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
Prereg :198, V13 :225, row 24: a synchronized stage-1 round >120 s halts HALTED-BUDGET in the run. ... C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 5400.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1200.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 2760.0, "ceiling_s": 5400.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 5400.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1200.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 2760.0, "ceiling_s": 5400.0}}}
ok
test_review_stage_call_refusals (__main__.SpecTests.test_review_stage_call_refusals)
Prereg :133, :137, :196, :266: fresh OUT_DIR, K1/K2 and absent-ceiling refusals happen before any launch. ... ok
test_review_wrapper_delegates_under_standing_law5 (__main__.SpecTests.test_review_wrapper_delegates_under_standing_law5)
Prereg :127, :157; V2/V9: run_law5 always takes the original path; ASTRA only behind LAW#3 and instruments. ... ok
test_review_write_prestart_projection_refuses_before_observation (__main__.SpecTests.test_review_write_prestart_projection_refuses_before_observation)
Prereg :196, V13 :225: refuse to start a candidate write when elapsed + projection exceeds the ceiling. ... C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 5400.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1200.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 5399.0, "remaining_s": 2760.0, "ceiling_s": 5400.0}}}
ok
test_review_write_round_cap_columns_and_capacity (__main__.SpecTests.test_review_write_round_cap_columns_and_capacity)
Prereg :79–81, :112: <=10 writes then round cap; only selected columns written; B_Z from Z's A7 only. ... C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 5400.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1200.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 2760.0, "ceiling_s": 5400.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 5400.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1200.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 2760.0, "ceiling_s": 5400.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 5400.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 5400.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 5400.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 5400.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 5400.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 5400.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 5400.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 5400.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 5400.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 5400.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 5400.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 5400.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 5400.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 5400.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 5400.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 5400.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 5400.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 5400.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 5400.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1200.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 2760.0, "ceiling_s": 5400.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 5400.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1200.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 2760.0, "ceiling_s": 5400.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 5400.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 5400.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 5400.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 5400.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 5400.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 5400.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 5400.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 5400.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 5400.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 5400.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 5400.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 5400.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 5400.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 5400.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 5400.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 5400.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 5400.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 5400.0}}}
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
Prereg :3, :341–344: operator go before stage 0; blocking demo B1. ... FAIL
test_B2_stray_stage_call_after_terminal_K1_keeps_the_result (__main__.Fix1Tests.test_B2_stray_stage_call_after_terminal_K1_keeps_the_result)
Prereg :137, :204, :267: a refusal preserves completed records; blocking demo B2. ... HALTED-V12: duplicate, out-of-order, stale or closed stage call
FAIL
test_B3_clean_survivor_without_stage2_ceiling_keeps_stage1_record (__main__.Fix1Tests.test_B3_clean_survivor_without_stage2_ceiling_keeps_stage1_record)
Prereg :196, :265–267: unbudgeted expansion closes STAGE1; blocking demo B3 with lead's suffix ruling. ... FAIL
test_fix1_absent_ceilings_terminal_labels_and_resident_close (__main__.Fix1Tests.test_fix1_absent_ceilings_terminal_labels_and_resident_close)
Prereg :196, :265–267: clean stage1/2 without next budget terminates; no G0/replication claim. ... FAIL
test_fix1_go_launch_copy_and_manifest_sha (__main__.Fix1Tests.test_fix1_go_launch_copy_and_manifest_sha)
Prereg :3, :137, :341–344: validated go copied to launch and its exact bytes bound to H_in. ... ERROR
test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation. ... 
  test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=0)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation. ... FAIL
  test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=1)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation. ... FAIL
  test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=2)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation. ... FAIL
  test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=3)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation. ... FAIL
  test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=4)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation. ... FAIL
  test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=5)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation. ... FAIL
  test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=6)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation. ... FAIL
  test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=7)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation. ... FAIL
  test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=8)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation. ... FAIL
  test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=9)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation. ... FAIL
  test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=10)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation. ... FAIL
  test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=11)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation. ... FAIL
  test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=12)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation. ... FAIL
  test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=13)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation. ... FAIL
  test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=14)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation. ... FAIL
  test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=15)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation. ... FAIL
  test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=16)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation. ... FAIL
  test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=17)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation. ... FAIL
  test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=18)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation. ... FAIL
  test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=19)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation. ... FAIL
  test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=20)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation. ... FAIL
  test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=21)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation. ... FAIL
  test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=22)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation. ... FAIL
  test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=23)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation. ... FAIL
  test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=24)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation. ... FAIL
  test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=25)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation. ... FAIL
  test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=26)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation. ... FAIL
  test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=27)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation. ... FAIL
  test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=28)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation. ... FAIL
  test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=29)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation. ... FAIL
  test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=30)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation. ... FAIL
  test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=31)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation. ... FAIL
  test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=32)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation. ... FAIL
  test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=33)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation. ... FAIL
  test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=34)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation. ... FAIL
  test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=35)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation. ... FAIL
  test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=36)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation. ... FAIL
  test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=37)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation. ... FAIL
  test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=38)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation. ... FAIL
  test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=39)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation. ... FAIL
  test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=40)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation. ... FAIL
  test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=41)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation. ... FAIL
  test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=42)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation. ... FAIL
  test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=43)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation. ... FAIL
  test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=44)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation. ... FAIL
  test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=45)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation. ... FAIL
  test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=46)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation. ... FAIL
  test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=47)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation. ... FAIL
  test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=48)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation. ... FAIL
test_fix1_go_sha_is_mandatory_reader_provenance (__main__.Fix1Tests.test_fix1_go_sha_is_mandatory_reader_provenance)
Prereg :137, V12 :224; §6 :341–344: missing/malformed go digest invalidates the manifest. ... FAIL
test_fix1_halt_sidecar_retains_completed_observations_for_both_processes (__main__.Fix1Tests.test_fix1_halt_sidecar_retains_completed_observations_for_both_processes)
Prereg :123, :267, :323: actual deadline/validity halts keep completed pass bytes and nonbinding observations. ... 
  test_fix1_halt_sidecar_retains_completed_observations_for_both_processes (__main__.Fix1Tests.test_fix1_halt_sidecar_retains_completed_observations_for_both_processes) (process=1, code='HALTED-BUDGET')
Prereg :123, :267, :323: actual deadline/validity halts keep completed pass bytes and nonbinding observations. ... FAIL
  test_fix1_halt_sidecar_retains_completed_observations_for_both_processes (__main__.Fix1Tests.test_fix1_halt_sidecar_retains_completed_observations_for_both_processes) (process=1, code='HALTED-V3')
Prereg :123, :267, :323: actual deadline/validity halts keep completed pass bytes and nonbinding observations. ... FAIL
  test_fix1_halt_sidecar_retains_completed_observations_for_both_processes (__main__.Fix1Tests.test_fix1_halt_sidecar_retains_completed_observations_for_both_processes) (process=2, code='HALTED-BUDGET')
Prereg :123, :267, :323: actual deadline/validity halts keep completed pass bytes and nonbinding observations. ... FAIL
test_fix1_refusals_preserve_finished_attempt_byte_for_byte (__main__.Fix1Tests.test_fix1_refusals_preserve_finished_attempt_byte_for_byte)
Prereg :137, :204, :267: duplicate/closed/out-of-order client refusals do not alter a finished attempt. ... 
  test_fix1_refusals_preserve_finished_attempt_byte_for_byte (__main__.Fix1Tests.test_fix1_refusals_preserve_finished_attempt_byte_for_byte) (stage=0)
Prereg :137, :204, :267: duplicate/closed/out-of-order client refusals do not alter a finished attempt. ... FAIL
  test_fix1_refusals_preserve_finished_attempt_byte_for_byte (__main__.Fix1Tests.test_fix1_refusals_preserve_finished_attempt_byte_for_byte) (stage=1)
Prereg :137, :204, :267: duplicate/closed/out-of-order client refusals do not alter a finished attempt. ... FAIL
  test_fix1_refusals_preserve_finished_attempt_byte_for_byte (__main__.Fix1Tests.test_fix1_refusals_preserve_finished_attempt_byte_for_byte) (stage=2)
Prereg :137, :204, :267: duplicate/closed/out-of-order client refusals do not alter a finished attempt. ... FAIL
  test_fix1_refusals_preserve_finished_attempt_byte_for_byte (__main__.Fix1Tests.test_fix1_refusals_preserve_finished_attempt_byte_for_byte) (stage=3)
Prereg :137, :204, :267: duplicate/closed/out-of-order client refusals do not alter a finished attempt. ... FAIL
test_fix1_relative_outdir_resolved_at_main_parse (__main__.Fix1Tests.test_fix1_relative_outdir_resolved_at_main_parse)
Prereg :8, :137, :204: records use one absolute OUT_DIR before the harness import changes cwd. ... FAIL
test_fix1_shell_preserves_go_env_absolute_outdir_and_no_refusal_write (__main__.Fix1Tests.test_fix1_shell_preserves_go_env_absolute_outdir_and_no_refusal_write)
Prereg :3, :137, :204: shell passes go unchanged and leaves unlaunched attempts untouched. ... FAIL
test_fix1_watchdog_preserves_last_published_record (__main__.Fix1Tests.test_fix1_watchdog_preserves_last_published_record)
Prereg :196, :225, :267: expired stage-2 watchdog preserves the complete earlier pass and labels HALT. ... FAIL

======================================================================
ERROR: test_fix1_go_launch_copy_and_manifest_sha (__main__.Fix1Tests.test_fix1_go_launch_copy_and_manifest_sha)
Prereg :3, :137, :341–344: validated go copied to launch and its exact bytes bound to H_in.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1364, in test_fix1_go_launch_copy_and_manifest_sha
    self.assertEqual(launch_record["go"], _go_record())
                     ~~~~~~~~~~~~~^^^^^^
KeyError: 'go'

======================================================================
FAIL: test_B1_stage0_refuses_without_recorded_go_decision (__main__.Fix1Tests.test_B1_stage0_refuses_without_recorded_go_decision)
Prereg :3, :341–344: operator go before stage 0; blocking demo B1.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1230, in test_B1_stage0_refuses_without_recorded_go_decision
    self.assertEqual(self.launched, [], "stage 0 launched without a go decision")
AssertionError: Lists differ: ['p1'] != []

First list contains 1 additional elements.
First extra element 0:
'p1'

- ['p1']
+ [] : stage 0 launched without a go decision

======================================================================
FAIL: test_B2_stray_stage_call_after_terminal_K1_keeps_the_result (__main__.Fix1Tests.test_B2_stray_stage_call_after_terminal_K1_keeps_the_result)
Prereg :137, :204, :267: a refusal preserves completed records; blocking demo B2.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1241, in test_B2_stray_stage_call_after_terminal_K1_keeps_the_result
    self.assertEqual(self.R.read_directory(out)["label"], "NULL-STAGE1")
AssertionError: 'HALTED-V12' != 'NULL-STAGE1'
- HALTED-V12
+ NULL-STAGE1


======================================================================
FAIL: test_B3_clean_survivor_without_stage2_ceiling_keeps_stage1_record (__main__.Fix1Tests.test_B3_clean_survivor_without_stage2_ceiling_keeps_stage1_record)
Prereg :196, :265–267: unbudgeted expansion closes STAGE1; blocking demo B3 with lead's suffix ruling.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1252, in test_B3_clean_survivor_without_stage2_ceiling_keeps_stage1_record
    self.assertEqual((reading["label"], reading["next_stage"], rec["omissions"]["G0"]["reason"]),
AssertionError: Tuples differ: ('PARTIAL', 2, 'ABSENT-CEILING') != ('PARTIAL-STAGE1', None, 'ABSENT-CEILING')

First differing element 0:
'PARTIAL'
'PARTIAL-STAGE1'

- ('PARTIAL', 2, 'ABSENT-CEILING')
?             ^

+ ('PARTIAL-STAGE1', None, 'ABSENT-CEILING')
?          +++++++   ^^^^


======================================================================
FAIL: test_fix1_absent_ceilings_terminal_labels_and_resident_close (__main__.Fix1Tests.test_fix1_absent_ceilings_terminal_labels_and_resident_close)
Prereg :196, :265–267: clean stage1/2 without next budget terminates; no G0/replication claim.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1467, in test_fix1_absent_ceilings_terminal_labels_and_resident_close
    got = R.read_process(r); self.assertEqual(got["label"], expected); self.assertIsNone(got["next_stage"])
                             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'PARTIAL' != 'PARTIAL-STAGE1'
- PARTIAL
+ PARTIAL-STAGE1


======================================================================
FAIL: test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=0)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1497, in main
    try:return stage_call(stage,out)
               ^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1451, in stage_call
    R.require(child.poll() is None,"HALTED-V12","resident failed before startup record");time.sleep(.1)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_read.py", line 40, in require
    raise Halt(code,detail)
c10z_astra_read.Halt: HALTED-V12: resident failed before startup record

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1342, in test_fix1_go_malformed_fields_refuse_without_any_attempt_write
    self.assertEqual(self.main(out, 0), 2)
                     ^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1223, in main
    return self.D.main()
           ^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1499, in main
    diagnostic(out,exc.code,exc.detail);print(str(exc),file=sys.stderr);return 2
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1124, in __call__
    return self._mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1128, in _mock_call
    return self._execute_mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1183, in _execute_mock_call
    raise effect
AssertionError: refusal wrote diagnostic

======================================================================
FAIL: test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=1)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1497, in main
    try:return stage_call(stage,out)
               ^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1451, in stage_call
    R.require(child.poll() is None,"HALTED-V12","resident failed before startup record");time.sleep(.1)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_read.py", line 40, in require
    raise Halt(code,detail)
c10z_astra_read.Halt: HALTED-V12: resident failed before startup record

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1342, in test_fix1_go_malformed_fields_refuse_without_any_attempt_write
    self.assertEqual(self.main(out, 0), 2)
                     ^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1223, in main
    return self.D.main()
           ^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1499, in main
    diagnostic(out,exc.code,exc.detail);print(str(exc),file=sys.stderr);return 2
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1124, in __call__
    return self._mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1128, in _mock_call
    return self._execute_mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1183, in _execute_mock_call
    raise effect
AssertionError: refusal wrote diagnostic

======================================================================
FAIL: test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=2)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1497, in main
    try:return stage_call(stage,out)
               ^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1451, in stage_call
    R.require(child.poll() is None,"HALTED-V12","resident failed before startup record");time.sleep(.1)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_read.py", line 40, in require
    raise Halt(code,detail)
c10z_astra_read.Halt: HALTED-V12: resident failed before startup record

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1342, in test_fix1_go_malformed_fields_refuse_without_any_attempt_write
    self.assertEqual(self.main(out, 0), 2)
                     ^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1223, in main
    return self.D.main()
           ^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1499, in main
    diagnostic(out,exc.code,exc.detail);print(str(exc),file=sys.stderr);return 2
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1124, in __call__
    return self._mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1128, in _mock_call
    return self._execute_mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1183, in _execute_mock_call
    raise effect
AssertionError: refusal wrote diagnostic

======================================================================
FAIL: test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=3)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1497, in main
    try:return stage_call(stage,out)
               ^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1451, in stage_call
    R.require(child.poll() is None,"HALTED-V12","resident failed before startup record");time.sleep(.1)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_read.py", line 40, in require
    raise Halt(code,detail)
c10z_astra_read.Halt: HALTED-V12: resident failed before startup record

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1342, in test_fix1_go_malformed_fields_refuse_without_any_attempt_write
    self.assertEqual(self.main(out, 0), 2)
                     ^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1223, in main
    return self.D.main()
           ^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1499, in main
    diagnostic(out,exc.code,exc.detail);print(str(exc),file=sys.stderr);return 2
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1124, in __call__
    return self._mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1128, in _mock_call
    return self._execute_mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1183, in _execute_mock_call
    raise effect
AssertionError: refusal wrote diagnostic

======================================================================
FAIL: test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=4)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1497, in main
    try:return stage_call(stage,out)
               ^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1451, in stage_call
    R.require(child.poll() is None,"HALTED-V12","resident failed before startup record");time.sleep(.1)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_read.py", line 40, in require
    raise Halt(code,detail)
c10z_astra_read.Halt: HALTED-V12: resident failed before startup record

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1342, in test_fix1_go_malformed_fields_refuse_without_any_attempt_write
    self.assertEqual(self.main(out, 0), 2)
                     ^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1223, in main
    return self.D.main()
           ^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1499, in main
    diagnostic(out,exc.code,exc.detail);print(str(exc),file=sys.stderr);return 2
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1124, in __call__
    return self._mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1128, in _mock_call
    return self._execute_mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1183, in _execute_mock_call
    raise effect
AssertionError: refusal wrote diagnostic

======================================================================
FAIL: test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=5)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1497, in main
    try:return stage_call(stage,out)
               ^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1451, in stage_call
    R.require(child.poll() is None,"HALTED-V12","resident failed before startup record");time.sleep(.1)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_read.py", line 40, in require
    raise Halt(code,detail)
c10z_astra_read.Halt: HALTED-V12: resident failed before startup record

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1342, in test_fix1_go_malformed_fields_refuse_without_any_attempt_write
    self.assertEqual(self.main(out, 0), 2)
                     ^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1223, in main
    return self.D.main()
           ^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1499, in main
    diagnostic(out,exc.code,exc.detail);print(str(exc),file=sys.stderr);return 2
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1124, in __call__
    return self._mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1128, in _mock_call
    return self._execute_mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1183, in _execute_mock_call
    raise effect
AssertionError: refusal wrote diagnostic

======================================================================
FAIL: test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=6)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1497, in main
    try:return stage_call(stage,out)
               ^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1451, in stage_call
    R.require(child.poll() is None,"HALTED-V12","resident failed before startup record");time.sleep(.1)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_read.py", line 40, in require
    raise Halt(code,detail)
c10z_astra_read.Halt: HALTED-V12: resident failed before startup record

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1342, in test_fix1_go_malformed_fields_refuse_without_any_attempt_write
    self.assertEqual(self.main(out, 0), 2)
                     ^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1223, in main
    return self.D.main()
           ^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1499, in main
    diagnostic(out,exc.code,exc.detail);print(str(exc),file=sys.stderr);return 2
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1124, in __call__
    return self._mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1128, in _mock_call
    return self._execute_mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1183, in _execute_mock_call
    raise effect
AssertionError: refusal wrote diagnostic

======================================================================
FAIL: test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=7)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1497, in main
    try:return stage_call(stage,out)
               ^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1451, in stage_call
    R.require(child.poll() is None,"HALTED-V12","resident failed before startup record");time.sleep(.1)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_read.py", line 40, in require
    raise Halt(code,detail)
c10z_astra_read.Halt: HALTED-V12: resident failed before startup record

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1342, in test_fix1_go_malformed_fields_refuse_without_any_attempt_write
    self.assertEqual(self.main(out, 0), 2)
                     ^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1223, in main
    return self.D.main()
           ^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1499, in main
    diagnostic(out,exc.code,exc.detail);print(str(exc),file=sys.stderr);return 2
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1124, in __call__
    return self._mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1128, in _mock_call
    return self._execute_mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1183, in _execute_mock_call
    raise effect
AssertionError: refusal wrote diagnostic

======================================================================
FAIL: test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=8)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1497, in main
    try:return stage_call(stage,out)
               ^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1451, in stage_call
    R.require(child.poll() is None,"HALTED-V12","resident failed before startup record");time.sleep(.1)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_read.py", line 40, in require
    raise Halt(code,detail)
c10z_astra_read.Halt: HALTED-V12: resident failed before startup record

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1342, in test_fix1_go_malformed_fields_refuse_without_any_attempt_write
    self.assertEqual(self.main(out, 0), 2)
                     ^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1223, in main
    return self.D.main()
           ^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1499, in main
    diagnostic(out,exc.code,exc.detail);print(str(exc),file=sys.stderr);return 2
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1124, in __call__
    return self._mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1128, in _mock_call
    return self._execute_mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1183, in _execute_mock_call
    raise effect
AssertionError: refusal wrote diagnostic

======================================================================
FAIL: test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=9)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1497, in main
    try:return stage_call(stage,out)
               ^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1451, in stage_call
    R.require(child.poll() is None,"HALTED-V12","resident failed before startup record");time.sleep(.1)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_read.py", line 40, in require
    raise Halt(code,detail)
c10z_astra_read.Halt: HALTED-V12: resident failed before startup record

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1342, in test_fix1_go_malformed_fields_refuse_without_any_attempt_write
    self.assertEqual(self.main(out, 0), 2)
                     ^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1223, in main
    return self.D.main()
           ^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1499, in main
    diagnostic(out,exc.code,exc.detail);print(str(exc),file=sys.stderr);return 2
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1124, in __call__
    return self._mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1128, in _mock_call
    return self._execute_mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1183, in _execute_mock_call
    raise effect
AssertionError: refusal wrote diagnostic

======================================================================
FAIL: test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=10)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1497, in main
    try:return stage_call(stage,out)
               ^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1451, in stage_call
    R.require(child.poll() is None,"HALTED-V12","resident failed before startup record");time.sleep(.1)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_read.py", line 40, in require
    raise Halt(code,detail)
c10z_astra_read.Halt: HALTED-V12: resident failed before startup record

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1342, in test_fix1_go_malformed_fields_refuse_without_any_attempt_write
    self.assertEqual(self.main(out, 0), 2)
                     ^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1223, in main
    return self.D.main()
           ^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1499, in main
    diagnostic(out,exc.code,exc.detail);print(str(exc),file=sys.stderr);return 2
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1124, in __call__
    return self._mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1128, in _mock_call
    return self._execute_mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1183, in _execute_mock_call
    raise effect
AssertionError: refusal wrote diagnostic

======================================================================
FAIL: test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=11)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1497, in main
    try:return stage_call(stage,out)
               ^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1451, in stage_call
    R.require(child.poll() is None,"HALTED-V12","resident failed before startup record");time.sleep(.1)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_read.py", line 40, in require
    raise Halt(code,detail)
c10z_astra_read.Halt: HALTED-V12: resident failed before startup record

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1342, in test_fix1_go_malformed_fields_refuse_without_any_attempt_write
    self.assertEqual(self.main(out, 0), 2)
                     ^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1223, in main
    return self.D.main()
           ^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1499, in main
    diagnostic(out,exc.code,exc.detail);print(str(exc),file=sys.stderr);return 2
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1124, in __call__
    return self._mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1128, in _mock_call
    return self._execute_mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1183, in _execute_mock_call
    raise effect
AssertionError: refusal wrote diagnostic

======================================================================
FAIL: test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=12)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1497, in main
    try:return stage_call(stage,out)
               ^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1451, in stage_call
    R.require(child.poll() is None,"HALTED-V12","resident failed before startup record");time.sleep(.1)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_read.py", line 40, in require
    raise Halt(code,detail)
c10z_astra_read.Halt: HALTED-V12: resident failed before startup record

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1342, in test_fix1_go_malformed_fields_refuse_without_any_attempt_write
    self.assertEqual(self.main(out, 0), 2)
                     ^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1223, in main
    return self.D.main()
           ^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1499, in main
    diagnostic(out,exc.code,exc.detail);print(str(exc),file=sys.stderr);return 2
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1124, in __call__
    return self._mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1128, in _mock_call
    return self._execute_mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1183, in _execute_mock_call
    raise effect
AssertionError: refusal wrote diagnostic

======================================================================
FAIL: test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=13)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1497, in main
    try:return stage_call(stage,out)
               ^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1451, in stage_call
    R.require(child.poll() is None,"HALTED-V12","resident failed before startup record");time.sleep(.1)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_read.py", line 40, in require
    raise Halt(code,detail)
c10z_astra_read.Halt: HALTED-V12: resident failed before startup record

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1342, in test_fix1_go_malformed_fields_refuse_without_any_attempt_write
    self.assertEqual(self.main(out, 0), 2)
                     ^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1223, in main
    return self.D.main()
           ^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1499, in main
    diagnostic(out,exc.code,exc.detail);print(str(exc),file=sys.stderr);return 2
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1124, in __call__
    return self._mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1128, in _mock_call
    return self._execute_mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1183, in _execute_mock_call
    raise effect
AssertionError: refusal wrote diagnostic

======================================================================
FAIL: test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=14)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1497, in main
    try:return stage_call(stage,out)
               ^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1451, in stage_call
    R.require(child.poll() is None,"HALTED-V12","resident failed before startup record");time.sleep(.1)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_read.py", line 40, in require
    raise Halt(code,detail)
c10z_astra_read.Halt: HALTED-V12: resident failed before startup record

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1342, in test_fix1_go_malformed_fields_refuse_without_any_attempt_write
    self.assertEqual(self.main(out, 0), 2)
                     ^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1223, in main
    return self.D.main()
           ^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1499, in main
    diagnostic(out,exc.code,exc.detail);print(str(exc),file=sys.stderr);return 2
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1124, in __call__
    return self._mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1128, in _mock_call
    return self._execute_mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1183, in _execute_mock_call
    raise effect
AssertionError: refusal wrote diagnostic

======================================================================
FAIL: test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=15)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1497, in main
    try:return stage_call(stage,out)
               ^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1451, in stage_call
    R.require(child.poll() is None,"HALTED-V12","resident failed before startup record");time.sleep(.1)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_read.py", line 40, in require
    raise Halt(code,detail)
c10z_astra_read.Halt: HALTED-V12: resident failed before startup record

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1342, in test_fix1_go_malformed_fields_refuse_without_any_attempt_write
    self.assertEqual(self.main(out, 0), 2)
                     ^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1223, in main
    return self.D.main()
           ^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1499, in main
    diagnostic(out,exc.code,exc.detail);print(str(exc),file=sys.stderr);return 2
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1124, in __call__
    return self._mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1128, in _mock_call
    return self._execute_mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1183, in _execute_mock_call
    raise effect
AssertionError: refusal wrote diagnostic

======================================================================
FAIL: test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=16)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1497, in main
    try:return stage_call(stage,out)
               ^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1451, in stage_call
    R.require(child.poll() is None,"HALTED-V12","resident failed before startup record");time.sleep(.1)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_read.py", line 40, in require
    raise Halt(code,detail)
c10z_astra_read.Halt: HALTED-V12: resident failed before startup record

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1342, in test_fix1_go_malformed_fields_refuse_without_any_attempt_write
    self.assertEqual(self.main(out, 0), 2)
                     ^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1223, in main
    return self.D.main()
           ^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1499, in main
    diagnostic(out,exc.code,exc.detail);print(str(exc),file=sys.stderr);return 2
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1124, in __call__
    return self._mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1128, in _mock_call
    return self._execute_mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1183, in _execute_mock_call
    raise effect
AssertionError: refusal wrote diagnostic

======================================================================
FAIL: test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=17)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1497, in main
    try:return stage_call(stage,out)
               ^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1451, in stage_call
    R.require(child.poll() is None,"HALTED-V12","resident failed before startup record");time.sleep(.1)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_read.py", line 40, in require
    raise Halt(code,detail)
c10z_astra_read.Halt: HALTED-V12: resident failed before startup record

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1342, in test_fix1_go_malformed_fields_refuse_without_any_attempt_write
    self.assertEqual(self.main(out, 0), 2)
                     ^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1223, in main
    return self.D.main()
           ^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1499, in main
    diagnostic(out,exc.code,exc.detail);print(str(exc),file=sys.stderr);return 2
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1124, in __call__
    return self._mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1128, in _mock_call
    return self._execute_mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1183, in _execute_mock_call
    raise effect
AssertionError: refusal wrote diagnostic

======================================================================
FAIL: test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=18)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1497, in main
    try:return stage_call(stage,out)
               ^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1451, in stage_call
    R.require(child.poll() is None,"HALTED-V12","resident failed before startup record");time.sleep(.1)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_read.py", line 40, in require
    raise Halt(code,detail)
c10z_astra_read.Halt: HALTED-V12: resident failed before startup record

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1342, in test_fix1_go_malformed_fields_refuse_without_any_attempt_write
    self.assertEqual(self.main(out, 0), 2)
                     ^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1223, in main
    return self.D.main()
           ^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1499, in main
    diagnostic(out,exc.code,exc.detail);print(str(exc),file=sys.stderr);return 2
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1124, in __call__
    return self._mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1128, in _mock_call
    return self._execute_mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1183, in _execute_mock_call
    raise effect
AssertionError: refusal wrote diagnostic

======================================================================
FAIL: test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=19)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1497, in main
    try:return stage_call(stage,out)
               ^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1451, in stage_call
    R.require(child.poll() is None,"HALTED-V12","resident failed before startup record");time.sleep(.1)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_read.py", line 40, in require
    raise Halt(code,detail)
c10z_astra_read.Halt: HALTED-V12: resident failed before startup record

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1342, in test_fix1_go_malformed_fields_refuse_without_any_attempt_write
    self.assertEqual(self.main(out, 0), 2)
                     ^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1223, in main
    return self.D.main()
           ^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1499, in main
    diagnostic(out,exc.code,exc.detail);print(str(exc),file=sys.stderr);return 2
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1124, in __call__
    return self._mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1128, in _mock_call
    return self._execute_mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1183, in _execute_mock_call
    raise effect
AssertionError: refusal wrote diagnostic

======================================================================
FAIL: test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=20)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1497, in main
    try:return stage_call(stage,out)
               ^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1451, in stage_call
    R.require(child.poll() is None,"HALTED-V12","resident failed before startup record");time.sleep(.1)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_read.py", line 40, in require
    raise Halt(code,detail)
c10z_astra_read.Halt: HALTED-V12: resident failed before startup record

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1342, in test_fix1_go_malformed_fields_refuse_without_any_attempt_write
    self.assertEqual(self.main(out, 0), 2)
                     ^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1223, in main
    return self.D.main()
           ^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1499, in main
    diagnostic(out,exc.code,exc.detail);print(str(exc),file=sys.stderr);return 2
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1124, in __call__
    return self._mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1128, in _mock_call
    return self._execute_mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1183, in _execute_mock_call
    raise effect
AssertionError: refusal wrote diagnostic

======================================================================
FAIL: test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=21)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1497, in main
    try:return stage_call(stage,out)
               ^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1451, in stage_call
    R.require(child.poll() is None,"HALTED-V12","resident failed before startup record");time.sleep(.1)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_read.py", line 40, in require
    raise Halt(code,detail)
c10z_astra_read.Halt: HALTED-V12: resident failed before startup record

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1342, in test_fix1_go_malformed_fields_refuse_without_any_attempt_write
    self.assertEqual(self.main(out, 0), 2)
                     ^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1223, in main
    return self.D.main()
           ^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1499, in main
    diagnostic(out,exc.code,exc.detail);print(str(exc),file=sys.stderr);return 2
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1124, in __call__
    return self._mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1128, in _mock_call
    return self._execute_mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1183, in _execute_mock_call
    raise effect
AssertionError: refusal wrote diagnostic

======================================================================
FAIL: test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=22)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1497, in main
    try:return stage_call(stage,out)
               ^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1451, in stage_call
    R.require(child.poll() is None,"HALTED-V12","resident failed before startup record");time.sleep(.1)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_read.py", line 40, in require
    raise Halt(code,detail)
c10z_astra_read.Halt: HALTED-V12: resident failed before startup record

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1342, in test_fix1_go_malformed_fields_refuse_without_any_attempt_write
    self.assertEqual(self.main(out, 0), 2)
                     ^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1223, in main
    return self.D.main()
           ^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1499, in main
    diagnostic(out,exc.code,exc.detail);print(str(exc),file=sys.stderr);return 2
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1124, in __call__
    return self._mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1128, in _mock_call
    return self._execute_mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1183, in _execute_mock_call
    raise effect
AssertionError: refusal wrote diagnostic

======================================================================
FAIL: test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=23)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1497, in main
    try:return stage_call(stage,out)
               ^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1451, in stage_call
    R.require(child.poll() is None,"HALTED-V12","resident failed before startup record");time.sleep(.1)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_read.py", line 40, in require
    raise Halt(code,detail)
c10z_astra_read.Halt: HALTED-V12: resident failed before startup record

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1342, in test_fix1_go_malformed_fields_refuse_without_any_attempt_write
    self.assertEqual(self.main(out, 0), 2)
                     ^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1223, in main
    return self.D.main()
           ^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1499, in main
    diagnostic(out,exc.code,exc.detail);print(str(exc),file=sys.stderr);return 2
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1124, in __call__
    return self._mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1128, in _mock_call
    return self._execute_mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1183, in _execute_mock_call
    raise effect
AssertionError: refusal wrote diagnostic

======================================================================
FAIL: test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=24)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1497, in main
    try:return stage_call(stage,out)
               ^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1451, in stage_call
    R.require(child.poll() is None,"HALTED-V12","resident failed before startup record");time.sleep(.1)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_read.py", line 40, in require
    raise Halt(code,detail)
c10z_astra_read.Halt: HALTED-V12: resident failed before startup record

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1342, in test_fix1_go_malformed_fields_refuse_without_any_attempt_write
    self.assertEqual(self.main(out, 0), 2)
                     ^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1223, in main
    return self.D.main()
           ^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1499, in main
    diagnostic(out,exc.code,exc.detail);print(str(exc),file=sys.stderr);return 2
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1124, in __call__
    return self._mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1128, in _mock_call
    return self._execute_mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1183, in _execute_mock_call
    raise effect
AssertionError: refusal wrote diagnostic

======================================================================
FAIL: test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=25)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1497, in main
    try:return stage_call(stage,out)
               ^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1451, in stage_call
    R.require(child.poll() is None,"HALTED-V12","resident failed before startup record");time.sleep(.1)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_read.py", line 40, in require
    raise Halt(code,detail)
c10z_astra_read.Halt: HALTED-V12: resident failed before startup record

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1342, in test_fix1_go_malformed_fields_refuse_without_any_attempt_write
    self.assertEqual(self.main(out, 0), 2)
                     ^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1223, in main
    return self.D.main()
           ^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1499, in main
    diagnostic(out,exc.code,exc.detail);print(str(exc),file=sys.stderr);return 2
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1124, in __call__
    return self._mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1128, in _mock_call
    return self._execute_mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1183, in _execute_mock_call
    raise effect
AssertionError: refusal wrote diagnostic

======================================================================
FAIL: test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=26)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1497, in main
    try:return stage_call(stage,out)
               ^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1451, in stage_call
    R.require(child.poll() is None,"HALTED-V12","resident failed before startup record");time.sleep(.1)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_read.py", line 40, in require
    raise Halt(code,detail)
c10z_astra_read.Halt: HALTED-V12: resident failed before startup record

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1342, in test_fix1_go_malformed_fields_refuse_without_any_attempt_write
    self.assertEqual(self.main(out, 0), 2)
                     ^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1223, in main
    return self.D.main()
           ^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1499, in main
    diagnostic(out,exc.code,exc.detail);print(str(exc),file=sys.stderr);return 2
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1124, in __call__
    return self._mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1128, in _mock_call
    return self._execute_mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1183, in _execute_mock_call
    raise effect
AssertionError: refusal wrote diagnostic

======================================================================
FAIL: test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=27)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1497, in main
    try:return stage_call(stage,out)
               ^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1451, in stage_call
    R.require(child.poll() is None,"HALTED-V12","resident failed before startup record");time.sleep(.1)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_read.py", line 40, in require
    raise Halt(code,detail)
c10z_astra_read.Halt: HALTED-V12: resident failed before startup record

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1342, in test_fix1_go_malformed_fields_refuse_without_any_attempt_write
    self.assertEqual(self.main(out, 0), 2)
                     ^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1223, in main
    return self.D.main()
           ^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1499, in main
    diagnostic(out,exc.code,exc.detail);print(str(exc),file=sys.stderr);return 2
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1124, in __call__
    return self._mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1128, in _mock_call
    return self._execute_mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1183, in _execute_mock_call
    raise effect
AssertionError: refusal wrote diagnostic

======================================================================
FAIL: test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=28)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1497, in main
    try:return stage_call(stage,out)
               ^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1451, in stage_call
    R.require(child.poll() is None,"HALTED-V12","resident failed before startup record");time.sleep(.1)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_read.py", line 40, in require
    raise Halt(code,detail)
c10z_astra_read.Halt: HALTED-V12: resident failed before startup record

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1342, in test_fix1_go_malformed_fields_refuse_without_any_attempt_write
    self.assertEqual(self.main(out, 0), 2)
                     ^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1223, in main
    return self.D.main()
           ^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1499, in main
    diagnostic(out,exc.code,exc.detail);print(str(exc),file=sys.stderr);return 2
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1124, in __call__
    return self._mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1128, in _mock_call
    return self._execute_mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1183, in _execute_mock_call
    raise effect
AssertionError: refusal wrote diagnostic

======================================================================
FAIL: test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=29)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1497, in main
    try:return stage_call(stage,out)
               ^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1451, in stage_call
    R.require(child.poll() is None,"HALTED-V12","resident failed before startup record");time.sleep(.1)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_read.py", line 40, in require
    raise Halt(code,detail)
c10z_astra_read.Halt: HALTED-V12: resident failed before startup record

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1342, in test_fix1_go_malformed_fields_refuse_without_any_attempt_write
    self.assertEqual(self.main(out, 0), 2)
                     ^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1223, in main
    return self.D.main()
           ^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1499, in main
    diagnostic(out,exc.code,exc.detail);print(str(exc),file=sys.stderr);return 2
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1124, in __call__
    return self._mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1128, in _mock_call
    return self._execute_mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1183, in _execute_mock_call
    raise effect
AssertionError: refusal wrote diagnostic

======================================================================
FAIL: test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=30)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1497, in main
    try:return stage_call(stage,out)
               ^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1451, in stage_call
    R.require(child.poll() is None,"HALTED-V12","resident failed before startup record");time.sleep(.1)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_read.py", line 40, in require
    raise Halt(code,detail)
c10z_astra_read.Halt: HALTED-V12: resident failed before startup record

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1342, in test_fix1_go_malformed_fields_refuse_without_any_attempt_write
    self.assertEqual(self.main(out, 0), 2)
                     ^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1223, in main
    return self.D.main()
           ^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1499, in main
    diagnostic(out,exc.code,exc.detail);print(str(exc),file=sys.stderr);return 2
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1124, in __call__
    return self._mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1128, in _mock_call
    return self._execute_mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1183, in _execute_mock_call
    raise effect
AssertionError: refusal wrote diagnostic

======================================================================
FAIL: test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=31)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1497, in main
    try:return stage_call(stage,out)
               ^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1451, in stage_call
    R.require(child.poll() is None,"HALTED-V12","resident failed before startup record");time.sleep(.1)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_read.py", line 40, in require
    raise Halt(code,detail)
c10z_astra_read.Halt: HALTED-V12: resident failed before startup record

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1342, in test_fix1_go_malformed_fields_refuse_without_any_attempt_write
    self.assertEqual(self.main(out, 0), 2)
                     ^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1223, in main
    return self.D.main()
           ^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1499, in main
    diagnostic(out,exc.code,exc.detail);print(str(exc),file=sys.stderr);return 2
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1124, in __call__
    return self._mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1128, in _mock_call
    return self._execute_mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1183, in _execute_mock_call
    raise effect
AssertionError: refusal wrote diagnostic

======================================================================
FAIL: test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=32)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1497, in main
    try:return stage_call(stage,out)
               ^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1451, in stage_call
    R.require(child.poll() is None,"HALTED-V12","resident failed before startup record");time.sleep(.1)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_read.py", line 40, in require
    raise Halt(code,detail)
c10z_astra_read.Halt: HALTED-V12: resident failed before startup record

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1342, in test_fix1_go_malformed_fields_refuse_without_any_attempt_write
    self.assertEqual(self.main(out, 0), 2)
                     ^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1223, in main
    return self.D.main()
           ^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1499, in main
    diagnostic(out,exc.code,exc.detail);print(str(exc),file=sys.stderr);return 2
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1124, in __call__
    return self._mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1128, in _mock_call
    return self._execute_mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1183, in _execute_mock_call
    raise effect
AssertionError: refusal wrote diagnostic

======================================================================
FAIL: test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=33)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1497, in main
    try:return stage_call(stage,out)
               ^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1451, in stage_call
    R.require(child.poll() is None,"HALTED-V12","resident failed before startup record");time.sleep(.1)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_read.py", line 40, in require
    raise Halt(code,detail)
c10z_astra_read.Halt: HALTED-V12: resident failed before startup record

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1342, in test_fix1_go_malformed_fields_refuse_without_any_attempt_write
    self.assertEqual(self.main(out, 0), 2)
                     ^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1223, in main
    return self.D.main()
           ^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1499, in main
    diagnostic(out,exc.code,exc.detail);print(str(exc),file=sys.stderr);return 2
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1124, in __call__
    return self._mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1128, in _mock_call
    return self._execute_mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1183, in _execute_mock_call
    raise effect
AssertionError: refusal wrote diagnostic

======================================================================
FAIL: test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=34)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1497, in main
    try:return stage_call(stage,out)
               ^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1451, in stage_call
    R.require(child.poll() is None,"HALTED-V12","resident failed before startup record");time.sleep(.1)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_read.py", line 40, in require
    raise Halt(code,detail)
c10z_astra_read.Halt: HALTED-V12: resident failed before startup record

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1342, in test_fix1_go_malformed_fields_refuse_without_any_attempt_write
    self.assertEqual(self.main(out, 0), 2)
                     ^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1223, in main
    return self.D.main()
           ^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1499, in main
    diagnostic(out,exc.code,exc.detail);print(str(exc),file=sys.stderr);return 2
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1124, in __call__
    return self._mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1128, in _mock_call
    return self._execute_mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1183, in _execute_mock_call
    raise effect
AssertionError: refusal wrote diagnostic

======================================================================
FAIL: test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=35)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1497, in main
    try:return stage_call(stage,out)
               ^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1451, in stage_call
    R.require(child.poll() is None,"HALTED-V12","resident failed before startup record");time.sleep(.1)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_read.py", line 40, in require
    raise Halt(code,detail)
c10z_astra_read.Halt: HALTED-V12: resident failed before startup record

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1342, in test_fix1_go_malformed_fields_refuse_without_any_attempt_write
    self.assertEqual(self.main(out, 0), 2)
                     ^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1223, in main
    return self.D.main()
           ^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1499, in main
    diagnostic(out,exc.code,exc.detail);print(str(exc),file=sys.stderr);return 2
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1124, in __call__
    return self._mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1128, in _mock_call
    return self._execute_mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1183, in _execute_mock_call
    raise effect
AssertionError: refusal wrote diagnostic

======================================================================
FAIL: test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=36)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1497, in main
    try:return stage_call(stage,out)
               ^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1451, in stage_call
    R.require(child.poll() is None,"HALTED-V12","resident failed before startup record");time.sleep(.1)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_read.py", line 40, in require
    raise Halt(code,detail)
c10z_astra_read.Halt: HALTED-V12: resident failed before startup record

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1342, in test_fix1_go_malformed_fields_refuse_without_any_attempt_write
    self.assertEqual(self.main(out, 0), 2)
                     ^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1223, in main
    return self.D.main()
           ^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1499, in main
    diagnostic(out,exc.code,exc.detail);print(str(exc),file=sys.stderr);return 2
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1124, in __call__
    return self._mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1128, in _mock_call
    return self._execute_mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1183, in _execute_mock_call
    raise effect
AssertionError: refusal wrote diagnostic

======================================================================
FAIL: test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=37)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1497, in main
    try:return stage_call(stage,out)
               ^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1451, in stage_call
    R.require(child.poll() is None,"HALTED-V12","resident failed before startup record");time.sleep(.1)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_read.py", line 40, in require
    raise Halt(code,detail)
c10z_astra_read.Halt: HALTED-V12: resident failed before startup record

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1342, in test_fix1_go_malformed_fields_refuse_without_any_attempt_write
    self.assertEqual(self.main(out, 0), 2)
                     ^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1223, in main
    return self.D.main()
           ^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1499, in main
    diagnostic(out,exc.code,exc.detail);print(str(exc),file=sys.stderr);return 2
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1124, in __call__
    return self._mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1128, in _mock_call
    return self._execute_mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1183, in _execute_mock_call
    raise effect
AssertionError: refusal wrote diagnostic

======================================================================
FAIL: test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=38)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1497, in main
    try:return stage_call(stage,out)
               ^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1451, in stage_call
    R.require(child.poll() is None,"HALTED-V12","resident failed before startup record");time.sleep(.1)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_read.py", line 40, in require
    raise Halt(code,detail)
c10z_astra_read.Halt: HALTED-V12: resident failed before startup record

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1342, in test_fix1_go_malformed_fields_refuse_without_any_attempt_write
    self.assertEqual(self.main(out, 0), 2)
                     ^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1223, in main
    return self.D.main()
           ^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1499, in main
    diagnostic(out,exc.code,exc.detail);print(str(exc),file=sys.stderr);return 2
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1124, in __call__
    return self._mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1128, in _mock_call
    return self._execute_mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1183, in _execute_mock_call
    raise effect
AssertionError: refusal wrote diagnostic

======================================================================
FAIL: test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=39)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1497, in main
    try:return stage_call(stage,out)
               ^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1451, in stage_call
    R.require(child.poll() is None,"HALTED-V12","resident failed before startup record");time.sleep(.1)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_read.py", line 40, in require
    raise Halt(code,detail)
c10z_astra_read.Halt: HALTED-V12: resident failed before startup record

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1342, in test_fix1_go_malformed_fields_refuse_without_any_attempt_write
    self.assertEqual(self.main(out, 0), 2)
                     ^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1223, in main
    return self.D.main()
           ^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1499, in main
    diagnostic(out,exc.code,exc.detail);print(str(exc),file=sys.stderr);return 2
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1124, in __call__
    return self._mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1128, in _mock_call
    return self._execute_mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1183, in _execute_mock_call
    raise effect
AssertionError: refusal wrote diagnostic

======================================================================
FAIL: test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=40)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1497, in main
    try:return stage_call(stage,out)
               ^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1451, in stage_call
    R.require(child.poll() is None,"HALTED-V12","resident failed before startup record");time.sleep(.1)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_read.py", line 40, in require
    raise Halt(code,detail)
c10z_astra_read.Halt: HALTED-V12: resident failed before startup record

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1342, in test_fix1_go_malformed_fields_refuse_without_any_attempt_write
    self.assertEqual(self.main(out, 0), 2)
                     ^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1223, in main
    return self.D.main()
           ^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1499, in main
    diagnostic(out,exc.code,exc.detail);print(str(exc),file=sys.stderr);return 2
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1124, in __call__
    return self._mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1128, in _mock_call
    return self._execute_mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1183, in _execute_mock_call
    raise effect
AssertionError: refusal wrote diagnostic

======================================================================
FAIL: test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=41)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1497, in main
    try:return stage_call(stage,out)
               ^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1451, in stage_call
    R.require(child.poll() is None,"HALTED-V12","resident failed before startup record");time.sleep(.1)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_read.py", line 40, in require
    raise Halt(code,detail)
c10z_astra_read.Halt: HALTED-V12: resident failed before startup record

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1342, in test_fix1_go_malformed_fields_refuse_without_any_attempt_write
    self.assertEqual(self.main(out, 0), 2)
                     ^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1223, in main
    return self.D.main()
           ^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1499, in main
    diagnostic(out,exc.code,exc.detail);print(str(exc),file=sys.stderr);return 2
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1124, in __call__
    return self._mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1128, in _mock_call
    return self._execute_mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1183, in _execute_mock_call
    raise effect
AssertionError: refusal wrote diagnostic

======================================================================
FAIL: test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=42)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1497, in main
    try:return stage_call(stage,out)
               ^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1451, in stage_call
    R.require(child.poll() is None,"HALTED-V12","resident failed before startup record");time.sleep(.1)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_read.py", line 40, in require
    raise Halt(code,detail)
c10z_astra_read.Halt: HALTED-V12: resident failed before startup record

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1342, in test_fix1_go_malformed_fields_refuse_without_any_attempt_write
    self.assertEqual(self.main(out, 0), 2)
                     ^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1223, in main
    return self.D.main()
           ^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1499, in main
    diagnostic(out,exc.code,exc.detail);print(str(exc),file=sys.stderr);return 2
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1124, in __call__
    return self._mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1128, in _mock_call
    return self._execute_mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1183, in _execute_mock_call
    raise effect
AssertionError: refusal wrote diagnostic

======================================================================
FAIL: test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=43)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1497, in main
    try:return stage_call(stage,out)
               ^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1451, in stage_call
    R.require(child.poll() is None,"HALTED-V12","resident failed before startup record");time.sleep(.1)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_read.py", line 40, in require
    raise Halt(code,detail)
c10z_astra_read.Halt: HALTED-V12: resident failed before startup record

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1342, in test_fix1_go_malformed_fields_refuse_without_any_attempt_write
    self.assertEqual(self.main(out, 0), 2)
                     ^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1223, in main
    return self.D.main()
           ^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1499, in main
    diagnostic(out,exc.code,exc.detail);print(str(exc),file=sys.stderr);return 2
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1124, in __call__
    return self._mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1128, in _mock_call
    return self._execute_mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1183, in _execute_mock_call
    raise effect
AssertionError: refusal wrote diagnostic

======================================================================
FAIL: test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=44)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1497, in main
    try:return stage_call(stage,out)
               ^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1451, in stage_call
    R.require(child.poll() is None,"HALTED-V12","resident failed before startup record");time.sleep(.1)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_read.py", line 40, in require
    raise Halt(code,detail)
c10z_astra_read.Halt: HALTED-V12: resident failed before startup record

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1342, in test_fix1_go_malformed_fields_refuse_without_any_attempt_write
    self.assertEqual(self.main(out, 0), 2)
                     ^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1223, in main
    return self.D.main()
           ^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1499, in main
    diagnostic(out,exc.code,exc.detail);print(str(exc),file=sys.stderr);return 2
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1124, in __call__
    return self._mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1128, in _mock_call
    return self._execute_mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1183, in _execute_mock_call
    raise effect
AssertionError: refusal wrote diagnostic

======================================================================
FAIL: test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=45)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1497, in main
    try:return stage_call(stage,out)
               ^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1451, in stage_call
    R.require(child.poll() is None,"HALTED-V12","resident failed before startup record");time.sleep(.1)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_read.py", line 40, in require
    raise Halt(code,detail)
c10z_astra_read.Halt: HALTED-V12: resident failed before startup record

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1342, in test_fix1_go_malformed_fields_refuse_without_any_attempt_write
    self.assertEqual(self.main(out, 0), 2)
                     ^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1223, in main
    return self.D.main()
           ^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1499, in main
    diagnostic(out,exc.code,exc.detail);print(str(exc),file=sys.stderr);return 2
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1124, in __call__
    return self._mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1128, in _mock_call
    return self._execute_mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1183, in _execute_mock_call
    raise effect
AssertionError: refusal wrote diagnostic

======================================================================
FAIL: test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=46)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1497, in main
    try:return stage_call(stage,out)
               ^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1451, in stage_call
    R.require(child.poll() is None,"HALTED-V12","resident failed before startup record");time.sleep(.1)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_read.py", line 40, in require
    raise Halt(code,detail)
c10z_astra_read.Halt: HALTED-V12: resident failed before startup record

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1342, in test_fix1_go_malformed_fields_refuse_without_any_attempt_write
    self.assertEqual(self.main(out, 0), 2)
                     ^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1223, in main
    return self.D.main()
           ^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1499, in main
    diagnostic(out,exc.code,exc.detail);print(str(exc),file=sys.stderr);return 2
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1124, in __call__
    return self._mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1128, in _mock_call
    return self._execute_mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1183, in _execute_mock_call
    raise effect
AssertionError: refusal wrote diagnostic

======================================================================
FAIL: test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=47)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1497, in main
    try:return stage_call(stage,out)
               ^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1451, in stage_call
    R.require(child.poll() is None,"HALTED-V12","resident failed before startup record");time.sleep(.1)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_read.py", line 40, in require
    raise Halt(code,detail)
c10z_astra_read.Halt: HALTED-V12: resident failed before startup record

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1342, in test_fix1_go_malformed_fields_refuse_without_any_attempt_write
    self.assertEqual(self.main(out, 0), 2)
                     ^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1223, in main
    return self.D.main()
           ^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1499, in main
    diagnostic(out,exc.code,exc.detail);print(str(exc),file=sys.stderr);return 2
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1124, in __call__
    return self._mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1128, in _mock_call
    return self._execute_mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1183, in _execute_mock_call
    raise effect
AssertionError: refusal wrote diagnostic

======================================================================
FAIL: test_fix1_go_malformed_fields_refuse_without_any_attempt_write (__main__.Fix1Tests.test_fix1_go_malformed_fields_refuse_without_any_attempt_write) (case=48)
Prereg :3, :137, :341–344: all missing/malformed go fields refuse before launch or output mutation.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1497, in main
    try:return stage_call(stage,out)
               ^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1451, in stage_call
    R.require(child.poll() is None,"HALTED-V12","resident failed before startup record");time.sleep(.1)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_read.py", line 40, in require
    raise Halt(code,detail)
c10z_astra_read.Halt: HALTED-V12: resident failed before startup record

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1342, in test_fix1_go_malformed_fields_refuse_without_any_attempt_write
    self.assertEqual(self.main(out, 0), 2)
                     ^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1223, in main
    return self.D.main()
           ^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1499, in main
    diagnostic(out,exc.code,exc.detail);print(str(exc),file=sys.stderr);return 2
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1124, in __call__
    return self._mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1128, in _mock_call
    return self._execute_mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1183, in _execute_mock_call
    raise effect
AssertionError: refusal wrote diagnostic

======================================================================
FAIL: test_fix1_go_sha_is_mandatory_reader_provenance (__main__.Fix1Tests.test_fix1_go_sha_is_mandatory_reader_provenance)
Prereg :137, V12 :224; §6 :341–344: missing/malformed go digest invalidates the manifest.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1400, in test_fix1_go_sha_is_mandatory_reader_provenance
    self.assertEqual(self.R.read_process(r)["label"], "HALTED-V12")
AssertionError: 'PARTIAL' != 'HALTED-V12'
- PARTIAL
+ HALTED-V12


======================================================================
FAIL: test_fix1_halt_sidecar_retains_completed_observations_for_both_processes (__main__.Fix1Tests.test_fix1_halt_sidecar_retains_completed_observations_for_both_processes) (process=1, code='HALTED-BUDGET')
Prereg :123, :267, :323: actual deadline/validity halts keep completed pass bytes and nonbinding observations.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1432, in test_fix1_halt_sidecar_retains_completed_observations_for_both_processes
    self.assertEqual(passpath.read_bytes(), before)
AssertionError: b'{\n  "attempt_id": "fixture-attempt",\n  "halt"[283 chars]n}\n' != b'{\n  "H_in": "8b17adc07480598d2cdc8a397841bf438[12978043 chars]n}\n'

======================================================================
FAIL: test_fix1_halt_sidecar_retains_completed_observations_for_both_processes (__main__.Fix1Tests.test_fix1_halt_sidecar_retains_completed_observations_for_both_processes) (process=1, code='HALTED-V3')
Prereg :123, :267, :323: actual deadline/validity halts keep completed pass bytes and nonbinding observations.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1432, in test_fix1_halt_sidecar_retains_completed_observations_for_both_processes
    self.assertEqual(passpath.read_bytes(), before)
AssertionError: b'{\n  "attempt_id": "fixture-attempt",\n  "halt"[279 chars]n}\n' != b'{\n  "H_in": "8b17adc07480598d2cdc8a397841bf438[12978043 chars]n}\n'

======================================================================
FAIL: test_fix1_halt_sidecar_retains_completed_observations_for_both_processes (__main__.Fix1Tests.test_fix1_halt_sidecar_retains_completed_observations_for_both_processes) (process=2, code='HALTED-BUDGET')
Prereg :123, :267, :323: actual deadline/validity halts keep completed pass bytes and nonbinding observations.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1432, in test_fix1_halt_sidecar_retains_completed_observations_for_both_processes
    self.assertEqual(passpath.read_bytes(), before)
AssertionError: b'{\n  "attempt_id": "fixture-attempt",\n  "halt"[292 chars]n}\n' != b'{\n  "H_in": "8b17adc07480598d2cdc8a397841bf438[7689685 chars]n}\n'

======================================================================
FAIL: test_fix1_refusals_preserve_finished_attempt_byte_for_byte (__main__.Fix1Tests.test_fix1_refusals_preserve_finished_attempt_byte_for_byte) (stage=0)
Prereg :137, :204, :267: duplicate/closed/out-of-order client refusals do not alter a finished attempt.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1497, in main
    try:return stage_call(stage,out)
               ^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1440, in stage_call
    R.require(not any((out/name).exists() for name in ("manifest.json","pass_p1.json","run.json")),
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_read.py", line 40, in require
    raise Halt(code,detail)
c10z_astra_read.Halt: HALTED-V12: attempt needs fresh OUT_DIR

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1413, in test_fix1_refusals_preserve_finished_attempt_byte_for_byte
    self.assertEqual(self.main(out, stage), 2)
                     ^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1223, in main
    return self.D.main()
           ^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1499, in main
    diagnostic(out,exc.code,exc.detail);print(str(exc),file=sys.stderr);return 2
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1124, in __call__
    return self._mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1128, in _mock_call
    return self._execute_mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1183, in _execute_mock_call
    raise effect
AssertionError: refusal called diagnostic

======================================================================
FAIL: test_fix1_refusals_preserve_finished_attempt_byte_for_byte (__main__.Fix1Tests.test_fix1_refusals_preserve_finished_attempt_byte_for_byte) (stage=1)
Prereg :137, :204, :267: duplicate/closed/out-of-order client refusals do not alter a finished attempt.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1497, in main
    try:return stage_call(stage,out)
               ^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1463, in stage_call
    R.require(stage in (1,2) and not run["closed"] and run["halt"] is None and run["requested"] is None and
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_read.py", line 40, in require
    raise Halt(code,detail)
c10z_astra_read.Halt: HALTED-V12: duplicate, out-of-order, stale or closed stage call

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1413, in test_fix1_refusals_preserve_finished_attempt_byte_for_byte
    self.assertEqual(self.main(out, stage), 2)
                     ^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1223, in main
    return self.D.main()
           ^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1499, in main
    diagnostic(out,exc.code,exc.detail);print(str(exc),file=sys.stderr);return 2
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1124, in __call__
    return self._mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1128, in _mock_call
    return self._execute_mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1183, in _execute_mock_call
    raise effect
AssertionError: refusal called diagnostic

======================================================================
FAIL: test_fix1_refusals_preserve_finished_attempt_byte_for_byte (__main__.Fix1Tests.test_fix1_refusals_preserve_finished_attempt_byte_for_byte) (stage=2)
Prereg :137, :204, :267: duplicate/closed/out-of-order client refusals do not alter a finished attempt.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1497, in main
    try:return stage_call(stage,out)
               ^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1463, in stage_call
    R.require(stage in (1,2) and not run["closed"] and run["halt"] is None and run["requested"] is None and
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_read.py", line 40, in require
    raise Halt(code,detail)
c10z_astra_read.Halt: HALTED-V12: duplicate, out-of-order, stale or closed stage call

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1413, in test_fix1_refusals_preserve_finished_attempt_byte_for_byte
    self.assertEqual(self.main(out, stage), 2)
                     ^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1223, in main
    return self.D.main()
           ^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1499, in main
    diagnostic(out,exc.code,exc.detail);print(str(exc),file=sys.stderr);return 2
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1124, in __call__
    return self._mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1128, in _mock_call
    return self._execute_mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1183, in _execute_mock_call
    raise effect
AssertionError: refusal called diagnostic

======================================================================
FAIL: test_fix1_refusals_preserve_finished_attempt_byte_for_byte (__main__.Fix1Tests.test_fix1_refusals_preserve_finished_attempt_byte_for_byte) (stage=3)
Prereg :137, :204, :267: duplicate/closed/out-of-order client refusals do not alter a finished attempt.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1497, in main
    try:return stage_call(stage,out)
               ^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1456, in stage_call
    R.require(run["closed"] and run["halt"] is None and run["completed"]==2 and
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_read.py", line 40, in require
    raise Halt(code,detail)
c10z_astra_read.Halt: HALTED-V12: stage3 requires clean completed K2 and closed process1

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1413, in test_fix1_refusals_preserve_finished_attempt_byte_for_byte
    self.assertEqual(self.main(out, stage), 2)
                     ^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1223, in main
    return self.D.main()
           ^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py", line 1499, in main
    diagnostic(out,exc.code,exc.detail);print(str(exc),file=sys.stderr);return 2
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1124, in __call__
    return self._mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1128, in _mock_call
    return self._execute_mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1183, in _execute_mock_call
    raise effect
AssertionError: refusal called diagnostic

======================================================================
FAIL: test_fix1_relative_outdir_resolved_at_main_parse (__main__.Fix1Tests.test_fix1_relative_outdir_resolved_at_main_parse)
Prereg :8, :137, :204: records use one absolute OUT_DIR before the harness import changes cwd.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1486, in test_fix1_relative_outdir_resolved_at_main_parse
    self.assertEqual(captured, [(Path.cwd() / "relative/attempt").resolve()])
AssertionError: Lists differ: [PosixPath('relative/attempt')] != [PosixPath('/Volumes/memit/llm-database-poc-mirror/ar[70 chars]pt')]

First differing element 0:
PosixPath('relative/attempt')
PosixPath('/Volumes/memit/llm-database-poc-mirror/ar[69 chars]mpt')

- [PosixPath('relative/attempt')]
+ [PosixPath('/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/relative/attempt')]

======================================================================
FAIL: test_fix1_shell_preserves_go_env_absolute_outdir_and_no_refusal_write (__main__.Fix1Tests.test_fix1_shell_preserves_go_env_absolute_outdir_and_no_refusal_write)
Prereg :3, :137, :204: shell passes go unchanged and leaves unlaunched attempts untouched.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1501, in test_fix1_shell_preserves_go_env_absolute_outdir_and_no_refusal_write
    self.assertEqual(result.stdout.splitlines(), [str(root / "relative/attempt"), go])
AssertionError: Lists differ: [] != ['/var/folders/p7/s31_tv0s2wd81chns8v7gsyw[115 chars]son']

Second list contains 2 additional elements.
First extra element 0:
'/var/folders/p7/s31_tv0s2wd81chns8v7gsyw0000gn/T/tmp0b7sb3hf/relative/attempt'

- []
+ ['/var/folders/p7/s31_tv0s2wd81chns8v7gsyw0000gn/T/tmp0b7sb3hf/relative/attempt',
+  '/var/folders/p7/s31_tv0s2wd81chns8v7gsyw0000gn/T/tmp0b7sb3hf/supplied-go.json']

======================================================================
FAIL: test_fix1_watchdog_preserves_last_published_record (__main__.Fix1Tests.test_fix1_watchdog_preserves_last_published_record)
Prereg :196, :225, :267: expired stage-2 watchdog preserves the complete earlier pass and labels HALT.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_selftest.py", line 1455, in test_fix1_watchdog_preserves_last_published_record
    self.assertEqual((out / "pass_p1.json").read_bytes(), before)
AssertionError: b'{\n  "attempt_id": "fixture-attempt",\n  "budge[7113410 chars]n}\n' != b'{\n  "H_in": "8b17adc07480598d2cdc8a397841bf438[7689656 chars]n}\n'

----------------------------------------------------------------------
Ran 72 tests in 44.072s

FAILED (failures=64, errors=1)
C10Z_ASTRA_SELFTEST_FAIL tests=72
```

GREEN — .venv/bin/python -B experiments/track_c/c10z_astra_selftest.py — exit 0

```text
test_00_implementation_exists (__main__.SpecTests.test_00_implementation_exists)
Prereg :204: actual driver, reader and stage wrapper exist. ... ok
test_band_boundaries_ordered (__main__.SpecTests.test_band_boundaries_ordered)
Prereg :112, :284: fit -> capacity -> locality -> three exhaustive BAND rows. ... ok
test_budget_origins_prestart_deadlines_round_memory (__main__.SpecTests.test_budget_origins_prestart_deadlines_round_memory)
Prereg :190, :196–198: 5400 seconds, scopes, unknown allowance, exact memory. ... C10Z_PROJECTION {"origins": {"stage01": 100.0}, "ceilings": {"stage01": 5400.0, "stage2": 60.0, "stage3": 6000.0}, "components_s": {"remaining": 1.0}, "scopes": {"stage01": {"elapsed_s": 5399.0, "remaining_s": 1.0, "ceiling_s": 5400.0}}}
C10Z_PROJECTION {"origins": {"stage01": 100.0}, "ceilings": {"stage01": 5400.0, "stage2": 60.0, "stage3": 6000.0}, "components_s": {"remaining": 1.001}, "scopes": {"stage01": {"elapsed_s": 5399.0, "remaining_s": 1.001, "ceiling_s": 5400.0}}}
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
Prereg :198, V13 :225, row 24: a synchronized stage-1 round >120 s halts HALTED-BUDGET in the run. ... C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 5400.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1200.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 2760.0, "ceiling_s": 5400.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 5400.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1200.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 2760.0, "ceiling_s": 5400.0}}}
ok
test_review_stage_call_refusals (__main__.SpecTests.test_review_stage_call_refusals)
Prereg :133, :137, :196, :266: fresh OUT_DIR, K1/K2 and absent-ceiling refusals happen before any launch. ... ok
test_review_wrapper_delegates_under_standing_law5 (__main__.SpecTests.test_review_wrapper_delegates_under_standing_law5)
Prereg :127, :157; V2/V9: run_law5 always takes the original path; ASTRA only behind LAW#3 and instruments. ... ok
test_review_write_prestart_projection_refuses_before_observation (__main__.SpecTests.test_review_write_prestart_projection_refuses_before_observation)
Prereg :196, V13 :225: refuse to start a candidate write when elapsed + projection exceeds the ceiling. ... C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 5400.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1200.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 5399.0, "remaining_s": 2760.0, "ceiling_s": 5400.0}}}
ok
test_review_write_round_cap_columns_and_capacity (__main__.SpecTests.test_review_write_round_cap_columns_and_capacity)
Prereg :79–81, :112: <=10 writes then round cap; only selected columns written; B_Z from Z's A7 only. ... C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 5400.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1200.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 2760.0, "ceiling_s": 5400.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 5400.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1200.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 2760.0, "ceiling_s": 5400.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 5400.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 5400.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 5400.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 5400.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 5400.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 5400.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 5400.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 5400.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 5400.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 5400.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 5400.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 5400.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 5400.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 5400.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 5400.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 5400.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 5400.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 5400.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 5400.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1200.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 2760.0, "ceiling_s": 5400.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 5400.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1200.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 2760.0, "ceiling_s": 5400.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 5400.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 5400.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 5400.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 5400.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 5400.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 5400.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 5400.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 5400.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 5400.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 5400.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 5400.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 5400.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 5400.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 5400.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 5400.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 5400.0}}}
C10Z_PROJECTION {"origins": {"stage01": 0.0}, "ceilings": {"stage01": 5400.0, "stage2": null, "stage3": null}, "components_s": {"candidate_rounds": 1.0, "checks_probes_eval": 1380.0, "serialization_restore": 180.0}, "scopes": {"stage01": {"elapsed_s": 0.0, "remaining_s": 1561.0, "ceiling_s": 5400.0}}}
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

----------------------------------------------------------------------
Ran 72 tests in 51.351s

OK
C10Z_ASTRA_SELFTEST_PASS tests=72
```

Mutation result

71 mutants: **70 KILLED; 1 SURVIVED** (`A32_z0_sigma_halt_dropped`). 71/71 targets matched exactly once. CPU scratch mirrors: `/private/tmp/c10z_fix1_mut_75gh119b`; partitions 18/18/18/17; every mutant ran the full 72-test suite with `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1`. Two pre-run and four post-run baselines PASS (72 tests each).

R16 re-anchored from `3 if stage==2 and clean else None` to `3 if stage==2 and clean and budgeted else None`; mutation drops only `clean`, preserving the added budget predicate. Deliberately missing target: exit 1, AssertionError target count 0; never SURVIVED.

```text
R01_law3_lower_exclusive	KILLED	rc=1	killed_by=['test_law3_both_sides']	['Ran 72 tests in 80.992s', 'C10Z_ASTRA_SELFTEST_FAIL tests=72']
R02_law3_A1A2_67	KILLED	rc=1	killed_by=['test_law3_both_sides']	['Ran 72 tests in 80.358s', 'C10Z_ASTRA_SELFTEST_FAIL tests=72']
R03_fit_strict_95	KILLED	rc=1	killed_by=['test_B2_stray_stage_call_after_terminal_K1_keeps_the_result', 'test_B3_clean_survivor_without_stage2_ceiling_keeps_stage1_record', 'test_band_boundaries_ordered', 'test_fit_count_boundaries', 'test_fix1_absent_ceilings_terminal_labels_and_resident_close', 'test_fix1_watchdog_preserves_last_published_record', 'test_k1_k2_omissions_and_replication', 'test_law3_both_sides', 'test_review_stage_call_refusals', 'test_side_gate_boundaries_and_populations', 'test_ttl_every_Z_arm_and_incomplete_actual_repro_failure', 'test_worked_01', 'test_worked_03', 'test_worked_04', 'test_worked_05', 'test_worked_06', 'test_worked_07', 'test_worked_08', 'test_worked_11', 'test_worked_12', 'test_worked_15', 'test_worked_16', 'test_worked_17', 'test_worked_19', 'test_worked_20', 'test_worked_23']	['Ran 72 tests in 68.482s', 'C10Z_ASTRA_SELFTEST_FAIL tests=72']
R04_fit_positive_22	KILLED	rc=1	killed_by=['test_fit_count_boundaries', 'test_worked_09']	['Ran 72 tests in 81.164s', 'C10Z_ASTRA_SELFTEST_FAIL tests=72']
R05_tableT_gain_8	KILLED	rc=1	killed_by=['test_table_T_exhaustive_and_integer_boundaries', 'test_worked_03', 'test_worked_04']	['Ran 72 tests in 84.786s', 'C10Z_ASTRA_SELFTEST_FAIL tests=72']
R06_tableT_lead_30	KILLED	rc=1	killed_by=['test_table_T_exhaustive_and_integer_boundaries']	['Ran 72 tests in 84.123s', 'C10Z_ASTRA_SELFTEST_FAIL tests=72']
R07_G1_plus2	KILLED	rc=1	killed_by=['test_side_gate_boundaries_and_populations']	['Ran 72 tests in 70.270s', 'C10Z_ASTRA_SELFTEST_FAIL tests=72']
R08_G2_any_view	KILLED	rc=1	killed_by=['test_side_gate_boundaries_and_populations']	['Ran 72 tests in 78.383s', 'C10Z_ASTRA_SELFTEST_FAIL tests=72']
R09_G7_plus2	KILLED	rc=1	killed_by=['test_side_gate_boundaries_and_populations', 'test_worked_06', 'test_worked_19']	['Ran 72 tests in 78.942s', 'C10Z_ASTRA_SELFTEST_FAIL tests=72']
R10_G4_28	KILLED	rc=1	killed_by=['test_side_gate_boundaries_and_populations']	['Ran 72 tests in 77.615s', 'C10Z_ASTRA_SELFTEST_FAIL tests=72']
R11_W1_ge	KILLED	rc=1	killed_by=['test_w1_even_median_w2_subject_free', 'test_worked_23']	['Ran 72 tests in 81.216s', 'C10Z_ASTRA_SELFTEST_FAIL tests=72']
R12_subject_free_ge	KILLED	rc=1	killed_by=['test_w1_even_median_w2_subject_free']	['Ran 72 tests in 82.681s', 'C10Z_ASTRA_SELFTEST_FAIL tests=72']
R13_ttl_ge	KILLED	rc=1	killed_by=['test_w1_even_median_w2_subject_free']	['Ran 72 tests in 94.073s', 'C10Z_ASTRA_SELFTEST_FAIL tests=72']
R14_ruleU_dropped	KILLED	rc=1	killed_by=['test_worked_02', 'test_worked_10']	['Ran 72 tests in 95.721s', 'C10Z_ASTRA_SELFTEST_FAIL tests=72']
R15_K1_clean_ignores_qualifiers	KILLED	rc=1	killed_by=['test_ttl_every_Z_arm_and_incomplete_actual_repro_failure', 'test_worked_09', 'test_worked_11', 'test_worked_12', 'test_worked_22']	['Ran 72 tests in 89.923s', 'C10Z_ASTRA_SELFTEST_FAIL tests=72']
R16_K2_next_stage_any	KILLED	rc=1	killed_by=['test_fix1_refusals_preserve_finished_attempt_byte_for_byte', 'test_review_stage_call_refusals', 'test_ttl_every_Z_arm_and_incomplete_actual_repro_failure']	['Ran 72 tests in 92.276s', 'C10Z_ASTRA_SELFTEST_FAIL tests=72']
R17_attr_capacity_ge	KILLED	rc=1	killed_by=['test_band_boundaries_ordered']	['Ran 72 tests in 96.830s', 'C10Z_ASTRA_SELFTEST_FAIL tests=72']
R18_attr_retains_strict	KILLED	rc=1	killed_by=['test_band_boundaries_ordered']	['Ran 72 tests in 95.031s', 'C10Z_ASTRA_SELFTEST_FAIL tests=72']
R19_attr_locality_dropped	KILLED	rc=1	killed_by=['test_worked_19']	['Ran 72 tests in 96.417s', 'C10Z_ASTRA_SELFTEST_FAIL tests=72']
R20_aggregate_clean_ignores_q	KILLED	rc=1	killed_by=['test_review_cross_process_replication_needs_clean_pair']	['Ran 72 tests in 95.614s', 'C10Z_ASTRA_SELFTEST_FAIL tests=72']
R21_R1_threshold_1e-2	KILLED	rc=1	killed_by=['test_k1_k2_omissions_and_replication']	['Ran 72 tests in 97.637s', 'C10Z_ASTRA_SELFTEST_FAIL tests=72']
R22_R2_le3	KILLED	rc=1	killed_by=['test_k1_k2_omissions_and_replication']	['Ran 72 tests in 97.934s', 'C10Z_ASTRA_SELFTEST_FAIL tests=72']
R23_z2_ambiguity_strict	KILLED	rc=1	killed_by=['test_review_reader_instrument_ceilings_audits_and_capacity']	['Ran 72 tests in 97.834s', 'C10Z_ASTRA_SELFTEST_FAIL tests=72']
R24_z2_empty_passes	KILLED	rc=1	killed_by=['test_z2_ambiguous_and_all_validity_gates']	['Ran 72 tests in 92.775s', 'C10Z_ASTRA_SELFTEST_FAIL tests=72']
R25_V5_Z3_dropped	KILLED	rc=1	killed_by=['test_worked_14']	['Ran 72 tests in 92.515s', 'C10Z_ASTRA_SELFTEST_FAIL tests=72']
R26_Z7_tau_ceiling_05	KILLED	rc=1	killed_by=['test_review_reader_instrument_ceilings_audits_and_capacity']	['Ran 72 tests in 93.713s', 'C10Z_ASTRA_SELFTEST_FAIL tests=72']
R27_Z0_sigma_ceiling_025	KILLED	rc=1	killed_by=['test_review_reader_instrument_ceilings_audits_and_capacity']	['Ran 72 tests in 98.281s', 'C10Z_ASTRA_SELFTEST_FAIL tests=72']
R28_Z4_loop_tol_1e-6	KILLED	rc=1	killed_by=['test_review_reader_instrument_ceilings_audits_and_capacity']	['Ran 72 tests in 97.038s', 'C10Z_ASTRA_SELFTEST_FAIL tests=72']
R29_Z5_footprint_unchecked	KILLED	rc=1	killed_by=['test_review_reader_instrument_ceilings_audits_and_capacity']	['Ran 72 tests in 97.736s', 'C10Z_ASTRA_SELFTEST_FAIL tests=72']
R30_V9_override_hits_unchecked	KILLED	rc=1	killed_by=['test_review_reader_instrument_ceilings_audits_and_capacity']	['Ran 72 tests in 96.670s', 'C10Z_ASTRA_SELFTEST_FAIL tests=72']
R31_V2_expr_le	KILLED	rc=1	killed_by=['test_review_reader_instrument_ceilings_audits_and_capacity']	['Ran 72 tests in 93.415s', 'C10Z_ASTRA_SELFTEST_FAIL tests=72']
R32_V7_strict	KILLED	rc=1	killed_by=['test_z2_ambiguous_and_all_validity_gates']	['Ran 72 tests in 91.454s', 'C10Z_ASTRA_SELFTEST_FAIL tests=72']
R33_stage1_round_121	KILLED	rc=1	killed_by=['test_completed_stage2_keeps_stage1_round_ceiling', 'test_worked_24']	['Ran 72 tests in 92.795s', 'C10Z_ASTRA_SELFTEST_FAIL tests=72']
R34_SemCon_capacity_unchecked	KILLED	rc=1	killed_by=['test_review_reader_instrument_ceilings_audits_and_capacity']	['Ran 72 tests in 92.215s', 'C10Z_ASTRA_SELFTEST_FAIL tests=72']
R35_band_distribution_unchecked	KILLED	rc=1	killed_by=['test_review_reader_instrument_ceilings_audits_and_capacity']	['Ran 72 tests in 91.991s', 'C10Z_ASTRA_SELFTEST_FAIL tests=72']
R36_p2_origin_unchecked	KILLED	rc=1	killed_by=['test_review_reader_instrument_ceilings_audits_and_capacity']	['Ran 72 tests in 91.991s', 'C10Z_ASTRA_SELFTEST_FAIL tests=72']
R37_not_replicated_dropped	KILLED	rc=1	killed_by=['test_review_cross_process_replication_needs_clean_pair']	['Ran 72 tests in 86.992s', 'C10Z_ASTRA_SELFTEST_FAIL tests=72']
A01_memory_strict	KILLED	rc=1	killed_by=['test_budget_origins_prestart_deadlines_round_memory']	['Ran 72 tests in 88.495s', 'C10Z_ASTRA_SELFTEST_FAIL tests=72']
A02_round_strict	KILLED	rc=1	killed_by=['test_budget_origins_prestart_deadlines_round_memory']	['Ran 72 tests in 95.511s', 'C10Z_ASTRA_SELFTEST_FAIL tests=72']
A03_projection_strict	KILLED	rc=1	killed_by=['test_budget_origins_prestart_deadlines_round_memory']	['Ran 72 tests in 93.230s', 'C10Z_ASTRA_SELFTEST_FAIL tests=72']
A04_projection_dropped	KILLED	rc=1	killed_by=['test_budget_origins_prestart_deadlines_round_memory', 'test_review_write_prestart_projection_refuses_before_observation']	['Ran 72 tests in 50.563s', 'C10Z_ASTRA_SELFTEST_FAIL tests=72']
A05_deadline_check_dropped	KILLED	rc=1	killed_by=['test_budget_origins_prestart_deadlines_round_memory']	['Ran 72 tests in 50.476s', 'C10Z_ASTRA_SELFTEST_FAIL tests=72']
A06_stage01_ceiling_7200	KILLED	rc=1	killed_by=['test_budget_origins_prestart_deadlines_round_memory']	['Ran 72 tests in 53.064s', 'C10Z_ASTRA_SELFTEST_FAIL tests=72']
A07_gate_observe_no_law3	KILLED	rc=1	killed_by=['test_ordering_and_stage_transport']	['Ran 72 tests in 49.259s', 'C10Z_ASTRA_SELFTEST_FAIL tests=72']
A08_gate_candidate_no_ready	KILLED	rc=1	killed_by=['test_ordering_and_stage_transport']	['Ran 72 tests in 55.087s', 'C10Z_ASTRA_SELFTEST_FAIL tests=72']
A09_stage0_law3_halt_swallowed	KILLED	rc=1	killed_by=['test_review_stage0_law3_gate_precedes_all_new_work']	['Ran 72 tests in 55.352s', 'C10Z_ASTRA_SELFTEST_FAIL tests=72']
A10_stage0_probes_before_law3	KILLED	rc=1	killed_by=['test_review_stage0_law3_gate_precedes_all_new_work']	['Ran 72 tests in 55.328s', 'C10Z_ASTRA_SELFTEST_FAIL tests=72']
A11_select_10_layers	KILLED	rc=1	killed_by=['test_cpu_null_weight_margin_fp16_selection']	['Ran 72 tests in 55.517s', 'C10Z_ASTRA_SELFTEST_FAIL tests=72']
A12_select_layer_tie_desc	KILLED	rc=1	killed_by=['test_cpu_null_weight_margin_fp16_selection']	['Ran 72 tests in 54.103s', 'C10Z_ASTRA_SELFTEST_FAIL tests=72']
A13_select_neuron_widened	KILLED	rc=1	killed_by=['test_cpu_null_weight_margin_fp16_selection']	['Ran 72 tests in 54.222s', 'C10Z_ASTRA_SELFTEST_FAIL tests=72']
A14_band_remainder_le	KILLED	rc=1	killed_by=['test_band_boundaries_ordered']	['Ran 72 tests in 54.458s', 'C10Z_ASTRA_SELFTEST_FAIL tests=72']
A15_band_uncapped	KILLED	rc=1	killed_by=['test_band_boundaries_ordered']	['Ran 72 tests in 54.410s', 'C10Z_ASTRA_SELFTEST_FAIL tests=72']
A16_ridge_1e-2	KILLED	rc=1	killed_by=['test_cpu_joint_algebra_independent_reference', 'test_known_answer_scalar_and_native_fp16_reference']	['Ran 72 tests in 54.720s', 'C10Z_ASTRA_SELFTEST_FAIL tests=72']
A17_competitor_not_excluded	KILLED	rc=1	killed_by=['test_cpu_null_weight_margin_fp16_selection']	['Ran 72 tests in 54.749s', 'C10Z_ASTRA_SELFTEST_FAIL tests=72']
A18_write_double_rounding	KILLED	rc=1	killed_by=['test_known_answer_scalar_and_native_fp16_reference']	['Ran 72 tests in 55.318s', 'C10Z_ASTRA_SELFTEST_FAIL tests=72']
A19_footprint_column_check_dropped	KILLED	rc=1	killed_by=['test_review_Z5_footprint_rejects_any_write_outside_selected_columns']	['Ran 72 tests in 55.305s', 'C10Z_ASTRA_SELFTEST_FAIL tests=72']
A20_footprint_other_params_dropped	KILLED	rc=1	killed_by=['test_review_Z5_footprint_rejects_any_write_outside_selected_columns']	['Ran 72 tests in 54.878s', 'C10Z_ASTRA_SELFTEST_FAIL tests=72']
A21_verify_restore_weakened	KILLED	rc=1	killed_by=['test_review_Z6_restore_covers_all_36_and_verify_detects_drift']	['Ran 72 tests in 54.792s', 'C10Z_ASTRA_SELFTEST_FAIL tests=72']
A22_restore_skips_layer35	KILLED	rc=1	killed_by=['test_review_Z6_restore_covers_all_36_and_verify_detects_drift']	['Ran 72 tests in 54.295s', 'C10Z_ASTRA_SELFTEST_FAIL tests=72']
A23_wrapper_law5_runs_astra	KILLED	rc=1	killed_by=['test_review_wrapper_delegates_under_standing_law5']	['Ran 72 tests in 54.390s', 'C10Z_ASTRA_SELFTEST_FAIL tests=72']
A24_write_prestart_projection_dropped	KILLED	rc=1	killed_by=['test_review_write_prestart_projection_refuses_before_observation']	['Ran 72 tests in 54.352s', 'C10Z_ASTRA_SELFTEST_FAIL tests=72']
A25_round_cap_11	KILLED	rc=1	killed_by=['test_review_write_round_cap_columns_and_capacity']	['Ran 72 tests in 54.295s', 'C10Z_ASTRA_SELFTEST_FAIL tests=72']
A26_stage1_round_guard_dropped	KILLED	rc=1	killed_by=['test_review_stage1_round_over_120s_halts_in_run']	['Ran 72 tests in 54.821s', 'C10Z_ASTRA_SELFTEST_FAIL tests=72']
A27_stage3_K2_check_dropped	KILLED	rc=1	killed_by=['test_fix1_refusals_preserve_finished_attempt_byte_for_byte', 'test_review_stage_call_refusals']	['Ran 72 tests in 53.081s', 'C10Z_ASTRA_SELFTEST_FAIL tests=72']
A28_stage3_ceiling_check_dropped	KILLED	rc=1	killed_by=['test_review_stage_call_refusals']	['Ran 72 tests in 55.479s', 'C10Z_ASTRA_SELFTEST_FAIL tests=72']
A29_stage0_fresh_outdir_dropped	KILLED	rc=1	killed_by=['test_review_stage_call_refusals']	['Ran 72 tests in 51.335s', 'C10Z_ASTRA_SELFTEST_FAIL tests=72']
A30_stage2_K1_survivor_check_dropped	KILLED	rc=1	killed_by=['test_review_stage_call_refusals']	['Ran 72 tests in 51.972s', 'C10Z_ASTRA_SELFTEST_FAIL tests=72']
A31_Z_capacity_from_any_arm	KILLED	rc=1	killed_by=['test_review_write_round_cap_columns_and_capacity']	['Ran 72 tests in 55.260s', 'C10Z_ASTRA_SELFTEST_FAIL tests=72']
A32_z0_sigma_halt_dropped	SURVIVED	rc=0	killed_by=[]	['Ran 72 tests in 54.498s', 'C10Z_ASTRA_SELFTEST_PASS tests=72']
A33_write_json_overwrite_allowed	KILLED	rc=1	killed_by=['test_json_real_writer_and_frozen_sources']	['Ran 72 tests in 53.983s', 'C10Z_ASTRA_SELFTEST_FAIL tests=72']
A34_inherited_knob_unchecked	KILLED	rc=1	killed_by=['test_ordering_and_stage_transport']	['Ran 72 tests in 54.770s', 'C10Z_ASTRA_SELFTEST_FAIL tests=72']
```

Baseline output

```text
pre: BASELINE	SURVIVED	rc=0	killed_by=[]	['Ran 72 tests in 50.554s', 'C10Z_ASTRA_SELFTEST_PASS tests=72']
pre: BASELINE	SURVIVED	rc=0	killed_by=[]	['Ran 72 tests in 53.774s', 'C10Z_ASTRA_SELFTEST_PASS tests=72']
worker1: BASELINE	SURVIVED	rc=0	killed_by=[]	['Ran 72 tests in 53.258s', 'C10Z_ASTRA_SELFTEST_PASS tests=72']
worker2: BASELINE	SURVIVED	rc=0	killed_by=[]	['Ran 72 tests in 53.999s', 'C10Z_ASTRA_SELFTEST_PASS tests=72']
worker3: BASELINE	SURVIVED	rc=0	killed_by=[]	['Ran 72 tests in 55.427s', 'C10Z_ASTRA_SELFTEST_PASS tests=72']
worker4: BASELINE	SURVIVED	rc=0	killed_by=[]	['Ran 72 tests in 54.290s', 'C10Z_ASTRA_SELFTEST_PASS tests=72']
```

Missing-target output — exit 1

```text
Traceback (most recent call last):
  File "<stdin>", line 5, in <module>
  File "/private/tmp/c10z_fix1_mut_75gh119b/mutate.py", line 99, in run
    assert n == 1, (name, "target count", n, old[:80])
           ^^^^^^
AssertionError: ('R16_K2_next_stage_any', 'target count', 0, '__C10Z_MISSING_MUTATION_TARGET__')
```

A1 — Acknowledged: frozen row 22 conflicts with Z2/validity order; conditional row label remains, full reader returns HALTED-V5; no code or prereg change (`docs/C10Z_ASTRA_PREREG.md:149`, `:208`, `:311`).
A2 — Acknowledged: stage-0 projection may refuse within the 5,400-second budget; the allowance/probe concern belongs to the lead's go decision; no change (`docs/C10Z_ASTRA_PREREG.md:196`, `:225`, `:344`).
A3 — Acknowledged: the 7,920-second future_stage2_s allowance remains absent from components_s; no change under the lead's ruling (`docs/C10Z_ASTRA_PREREG.md:196`).
A4 — Acknowledged: W2 includes evaluation, probes and restoration; this remains conservative; no timing change (`docs/C10Z_ASTRA_PREREG.md:200`, `:274`).
A5 — Acknowledged: v2.2/e58cebf requires stage-0–1 timing before model import and does not pin it to the parent's launch; no change (`docs/C10Z_ASTRA_PREREG.md:196`).
A6 — Fixed: relative OUT_DIR becomes absolute before harness import/chdir (`experiments/track_c/c10z_astra_arms.py:1519`; `tools/run_c10z_stage.sh:10`; `docs/C10Z_ASTRA_PREREG.md:137`, `:204`).
A7 — Acknowledged: stage 2 requires a separate external call; budgeted survivors retain the existing waiting behavior; no idle-limit or scheduling change (`docs/C10Z_ASTRA_PREREG.md:131`, `:265`).
A8 — Acknowledged: stage-2 merge still omits stage-1 Z law5_gate/delta_norms from the merged record; no change (`docs/C10Z_ASTRA_PREREG.md:127`, `:157`, `:215`).
A9 — Fixed: comment now states that stage 0 reads pristine held-out leads and held-out reads never enter the solve (`experiments/track_c/c10z_astra_arms.py:674`; `docs/C10Z_ASTRA_PREREG.md:124`, `:166`).
A10 — Acknowledged: A32 is outcome-neutral under the reader/Gates Z0 backstop; A26/A31 are pinned by the adopted runtime tests; no production change (`docs/C10Z_ASTRA_PREREG.md:147`, `:198`, `:224`).
