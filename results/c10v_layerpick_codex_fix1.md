# D-C10v-implfix — fix round 1

**Model:** `gpt-6.1-sol` (Codex). **Effort:** `max` (verified from this session's `turn_context`). **Date:** 2026-10-07.

Implemented the program's rulings in `/Users/robertrhu/.claude/jobs/8ac4cacf/tmp/codex_c10v_fix_brief.md`. **43/43 model-free selftests PASS, exit 0.** This is driver verification for D-C10v-layerpick, not an experiment result or a live LAW#3/LAW#5 clearance.

Worktree: `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a`, branch `worktree-c10k-route-a`. Scope on the e2e map: write engine, compile-time layer placement (§8.1), evaluated against the held-out full-sequence read bar (§8.9); no F1 closure claim. Read the frozen v2 prereg and the entire supplied Claude review `results/c10v_layerpick_advisor_impl.md` before editing. The review plus the lead's explicit rulings supplied the pre-fix advisor input; no external model review was launched in this model-free round.

## Ruling → test → code

All line numbers in this table refer to the final files.

| Program ruling / advisor item | Test and boundary coverage | Implementation |
|---|---|---|
| 1 / item 1: candidate validity is per recipe; continue after invalid controls or string/full mismatch | `experiments/track_c/c10v_layerpick_selftest.py:636`: both passes, B0/B/Bshuf, both controls at 67/68/69; all four recipes execute and complete markers exist; validity fields survive JSON. `:651`: B's string counts 29/30/31 against full count 30; invalid B still permits Bshuf. `:666`: an invalid control cannot hide an override integrity fault. The original candidate-HALT expectation was removed from the dependency test at `:955`. | `experiments/track_c/c10v_layerpick_read.py:172` separates recipe integrity from `:248` recipe validity; `:260` retains the combined baseline validator. `:291` validates pass integrity; `:308` retains per-recipe INVALID reading semantics. `experiments/track_c/c10v_layerpick_arms.py:532` HALTs on integrity, `:536` records `validity = {ok, reasons}` and continues, and `:550` checks integrity before persistence. Recipe A remains the binding same-process gate at `:517`. |
| 2 / item 2: pass1 uses the published map even when fresh selection disagrees | `experiments/track_c/c10v_layerpick_selftest.py:675`: agreement 0/1/23/24, δ 0.0/0.125, published B map actually passed to the recipe runner; JSON round-trip and real pass validation. Existing pass2 concentrated-reselection test remains at `:1027`. | `experiments/track_c/c10v_layerpick_arms.py:508`: retains in-process reproducibility and covariance gates; removes the former `PASS1_FIXED_MAP` equality gate; `:511` builds recipes from the published map. Agreement remains recorded at `:543`. |
| 3 / item 3: measured in-process δ stays unchanged, including 0.0 | The same `experiments/track_c/c10v_layerpick_selftest.py:675` test rereads `record["step0"]["delta"]` as exactly 0.0 or 0.125 and `record["selection_agreement_n"]` as the expected count. | **No change to δ measurement.** `experiments/track_c/c10v_layerpick_read.py:74` still takes the maximum absolute cell difference across the two in-process tables. `experiments/track_c/c10v_layerpick_arms.py:541` stores that complete selector record as `step0`; `:543` stores selection agreement. No epsilon substitution or new δ gate. |
| 4 / item 4: nearest 8 among contenders within δ, subject to the margin rule | `experiments/track_c/c10v_layerpick_selftest.py:245` now requires winner 4 / runner-up 5 below δ → 5. `:255` tests margin exactly δ and its immediate floating-point neighbours, contender inclusion exactly at / immediately within / immediately outside δ, and δ=0 ties. | `experiments/track_c/c10v_layerpick_read.py:81` forms the contenders with score ≥ winner − δ; `:82` retains the winner when margin ≥ δ, otherwise selects `max(near)` among layers 4–8. |
| 5 / item 5: historical record is a preflight control reference | `experiments/track_c/c10v_layerpick_selftest.py:582` copies the actual `results/c10q_stacked/passS.json` into a temporary directory, creates and rereads identity JSON, validates it, reuses it, and detects reference-byte drift. New field present; old field absent. | `experiments/track_c/c10v_layerpick_arms.py:79`, `:115`, `:119` and `experiments/track_c/c10v_layerpick_read.py:117` now use `preflight_controls_reference`. The CLI spelling `--law3-ref` and existing diagnostic gate names are retained. **The binding LAW#3 gate is the same-process recipe-A envelope and validity check, not this historical file.** |
| 6 / item 6: original-path LAW#5 writes must consume pinned targets | `experiments/track_c/c10v_layerpick_selftest.py:359`: hits 0/1/2; 0 is exercised by a missing override key and the real synthetic fallback, 2 by two real synthetic writes. Failure and success restore weights and the previous override. | `experiments/track_c/c10v_layerpick_arms.py:321` requires exactly one hit after every original-path `capture_write` call. The wrapper's existing group-hit check is unchanged. |
| 6 / item 7: LAW#5 singleton and multigroup checks include unassigned layers | `experiments/track_c/c10v_layerpick_selftest.py:380`: faults applied after the real grouped write, independently for singleton and multigroup; zero passes, ±1e-12 on an unassigned layer fails. Restoration checked in both cases. | `experiments/track_c/c10v_layerpick_arms.py:365` requires zero ΔW on all layers except 8; `:381` requires zero ΔW on layers absent from the two-group map. Existing assigned-layer distance checks and tolerances remain. |
| 6 / item 8: Bshuf labels carry a control-only suffix | `experiments/track_c/c10v_layerpick_selftest.py:562`: persisted-directory and actual reader entrypoint coverage for NULL, PARTIAL, LEAD, TRADEOFF-LARGE-WRITE and INVALID; no gate A or replication scheduling for Bshuf. INVALID still exits 2. | `experiments/track_c/c10v_layerpick_read.py:386` appends `-CONTROL-ONLY` before skipping Bshuf replication bookkeeping. `:464` checks `base_label` for INVALID so the suffix cannot hide a failure from the reader exit code. |

An invalid B0 comparator does not invalidate a scientifically valid B reading. Existing attribution logic still withholds selector credit when either comparator is invalid. The reader's locality gates remain on A7, as in the reviewed implementation; this round does not extend those gates to A1/A2.

The historical `passS.json` is the `A7_stacked` record; its preflight A1/A2 counts are 70/71. It is not a baseline-recipe record. Recipe A's binding same-process check retains A7 paraphrase [5,18]/72, canonical [5,10]/24, valid controls and full-string agreement before any candidate starts.

## Test-first evidence

Each behavior-changing ruling had its regression added or inverted, then executed against the still-unfixed code, before the implementation edit. δ itself required no implementation change. Raw outputs and exact command metadata are in `/private/tmp/c10v-fix1-inztgrd7/`; the relevant observations and complete final suite output are also included here.

Focused runs used `.venv/bin/python -B -m unittest -v experiments.track_c.c10v_layerpick_selftest.<Class>.<test>` with the tests named in the mapping above. Each green run below was the **entire** `.venv/bin/python -B experiments/track_c/c10v_layerpick_selftest.py` suite. A fresh `PYTHONPYCACHEPREFIX` under the temporary evidence directory prevented reuse of stale bytecode; `-B` prevented bytecode writes. The wrapper saved unfiltered combined output and the child's exit code.

| Evidence log | Observed RED, exit 1 | Observed GREEN, exit 0 |
|---|---|---|
| `red-validity.log` → `green-validity-suite.log` | `Ran 3 tests`; `FAILED (failures=1, errors=42)`. Candidate 67 controls and unequal string counts raised the old `HALT: RECIPE_VALIDITY ...`; otherwise the new persisted validity field was absent. The combined validity/integrity test observed `CONTROL_A1_single` masking `OVERRIDE_GROUPS`. | 37 tests OK. |
| `red-published-map.log` → `green-published-map.log` | `Ran 1 test`; `FAILED (errors=6)` with `GateError: PASS1_FIXED_MAP` for agreements 0/1/23, at both tested δ values. | 38 tests OK. |
| `red-nearest8.log` → `green-nearest8.log` | `Ran 2 tests`; `FAILED (failures=5)`; old fallback returned 8 where the hand-derived contenders required 5 or 6. | 39 tests OK. |
| `red-reference.log` → `green-reference.log` | `FAILED (failures=1)`; `preflight_controls_reference` absent from the real persisted identity. | 40 tests OK. |
| `red-override-pin.log` → `green-override-pin.log` | `FAILED (failures=2)`; `GateError not raised` for 0 and 2 hits. | 41 tests OK. |
| `red-scope.log` → `green-scope.log` | `FAILED (failures=4)`; `GateError not raised` for both signs of leakage, at both LAW#5 scopes. | 42 tests OK. |
| `red-bshuf.log`, `red-bshuf-exit.log` → `green-bshuf.log` | Five missing-suffix failures first. After adding the suffix, the existing entrypoint check exposed `AssertionError: 0 != 2` for INVALID; that failure was observed before changing the exit-code check. | 43 tests OK. |

One intermediate full-suite failure is retained in `green-validity.log`: 36 of 37 tests passed, but the existing pass2 test's deliberately stubbed `validate_recipe` boundary no longer covered the newly separated `recipe_integrity`. Its stale synthetic predictions then reached `PROXY_PREDICTIONS` instead of its intended later sentinel. The stub was extended to the same integrity boundary; `green-validity-suite.log` then passed 37/37. No extra production fix was used to repair that fixture.

## LAW#4 source reads

Before editing, complete bodies were read with line numbers. These **pre-change** spans refer to the captured session-start sources (saved under the temporary evidence directory), rather than current shifted line numbers:

- `experiments/track_c/c10v_layerpick_arms.py`: `assert_sources` 76–80, `initialise_identity` 110–121, `capture_write` 311–328, `law5_checks` 331–391, `runtime_stage` 475–555.
- `experiments/track_c/c10v_layerpick_read.py`: `select_maps` 68–92, `validate_identity` 111–121, `validate_recipe` 171–249, `pass_validity` 276–294, `read_run` 364–385, `main` 434–445. The integrity/validity helpers are extracted from those actually read validators.
- Existing selftest functions changed: `identity_fixture` 38–42, `fixture_directory` 198–232, `test_margin_delta_below_at_above_and_nearest8_tie` 245–253, `_assert_halt` 542–562, `test_every_validity_gate_routes_to_halt_diagnostic` 564–630, `test_real_stage_dependency_selector_source_and_candidate_halts` 767–807, `test_real_pass2_runs_published_map_despite_concentrated_reselection` 842–864. Newly added tests/helpers had no pre-existing body.
- The unchanged harness's snapshot/restore, projector, `my_edit`, LAW#5 and recipe runner bodies were also read. The original-path override semantics are at `experiments/track_c/c10e_bandknob.py:185`–191; its restore boundary is `:155`–159.

## Diff and constraints

Three source files changed, plus this new report. Source diff versus the starting implementation:

| File | Added | Removed |
|---|---:|---:|
| `experiments/track_c/c10v_layerpick_arms.py` | 14 | 8 |
| `experiments/track_c/c10v_layerpick_read.py` | 50 | 28 |
| `experiments/track_c/c10v_layerpick_selftest.py` | 202 | 17 |

The production changes are the requested validity split, published-map behavior, contender selection, identity-field rename, original-path pin check, unassigned-layer checks and Bshuf suffix/exit handling. No engine primitive, target solve, projector solve, locality threshold or unrelated code was refactored. Nine tests were added to the original 34, with the old candidate-HALT and pass1-map-HALT expectations inverted.

`git diff --check` passed. The actual stdlib fingerprint command passed with SHA-256 `d941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65` and `_cov_cpu == 3`.

All 62 protected-file hashes match the starting snapshot: 59 engine Python files, `experiments/track_c/c10e_bandknob.py`, `docs/C10V_LAYERPICK_PREREG.md`, and `.gitignore`. The protected-file git diff was empty. The harness SHA-256 remains `1f6be5811d7e58f3ebda16867a4a174b1cf24d47f9a2514cf9c3f9d29f18e695`; prereg SHA-256 remains `00981bfc9cb5770ccea203f6682d953948afdba653a4bd4173bbc754130ad524`.

No model/tokenizer/torch-on-MPS/GPU job was launched or imported, and no mutating git command was issued. Model-free driver success tests replace model loading, selector sampling, target preparation, the live LAW#5 call and recipe execution, and stub current-source inventory checks for their temporary worktree. Separate source identity and drift checks are tested directly. The numerical seam, validators, JSON writer, persisted reader and reader entrypoint run directly. Thus EVIDENCE-SHOWS instrument behavior under those fixtures, not live-model inertness, baseline reproduction, or scientific effectiveness. Those remain the live-stage gates.

Graft automatically regenerated its ignored `graft/.cache/ask-index.json` despite its no-refresh flags. No tracked Graft or ignore-file diff remains; that generated cache is not a science artifact. Unrelated work already present or concurrently produced in this shared worktree was not edited.

## SHA-256 of changed source files

| File | SHA-256 |
|---|---|
| `experiments/track_c/c10v_layerpick_arms.py` | `2ab5b27be78b7ff63d32bd74e12b437db62e6840da297f2a1418dcfd7a9284db` |
| `experiments/track_c/c10v_layerpick_read.py` | `8b0f9d5ac49ec633cd09d33f735d7d243f30227ad9030593114ca5fa5984ef68` |
| `experiments/track_c/c10v_layerpick_selftest.py` | `1110f7b87c2117730f2c16dce75c1ea096fa2c74789d0efc187f810331be451c` |

## Full selftest output

Command: `.venv/bin/python -B experiments/track_c/c10v_layerpick_selftest.py`.
Exit code: **0**. Complete unfiltered child output:

```text
test_bshuf_control_only_labels_roundtrip_and_invalid_exit (__main__.SafetyAndPersistenceTests.test_bshuf_control_only_labels_roundtrip_and_invalid_exit) ... ok
test_complete_persisted_chain_positive_control_and_every_chain_gate_halt (__main__.SafetyAndPersistenceTests.test_complete_persisted_chain_positive_control_and_every_chain_gate_halt) ... ok
test_every_record_kind_json_normalised_roundtrip_and_exclusive (__main__.SafetyAndPersistenceTests.test_every_record_kind_json_normalised_roundtrip_and_exclusive) ... ok
test_every_validity_gate_routes_to_halt_diagnostic (__main__.SafetyAndPersistenceTests.test_every_validity_gate_routes_to_halt_diagnostic) ... ok
test_import_and_help_never_import_model_modules (__main__.SafetyAndPersistenceTests.test_import_and_help_never_import_model_modules) ... ok
test_json_nonfinite_corruption_and_each_io_failure (__main__.SafetyAndPersistenceTests.test_json_nonfinite_corruption_and_each_io_failure) ... ok
test_law5_layer_coverage_and_missing_floor_observations (__main__.SafetyAndPersistenceTests.test_law5_layer_coverage_and_missing_floor_observations) ... ok
test_occupied_dangling_symlink_bad_maps_and_wrapper_keys_halt (__main__.SafetyAndPersistenceTests.test_occupied_dangling_symlink_bad_maps_and_wrapper_keys_halt) ... ok
test_preflight_controls_reference_identity_roundtrip_and_drift (__main__.SafetyAndPersistenceTests.test_preflight_controls_reference_identity_roundtrip_and_drift) ... ok
test_preflight_gate_halts_and_never_loads_harness (__main__.SafetyAndPersistenceTests.test_preflight_gate_halts_and_never_loads_harness) ... ok
test_real_pass1_published_map_agreement_and_measured_delta_roundtrip (__main__.SafetyAndPersistenceTests.test_real_pass1_published_map_agreement_and_measured_delta_roundtrip) ... ok
test_real_pass2_runs_published_map_despite_concentrated_reselection (__main__.SafetyAndPersistenceTests.test_real_pass2_runs_published_map_despite_concentrated_reselection) ... ok
test_real_stage_candidate_control_invalid_continues_and_roundtrips (__main__.SafetyAndPersistenceTests.test_real_stage_candidate_control_invalid_continues_and_roundtrips) ... ok
test_real_stage_candidate_full_string_invalid_continues_and_roundtrips (__main__.SafetyAndPersistenceTests.test_real_stage_candidate_full_string_invalid_continues_and_roundtrips) ... ok
test_real_stage_candidate_invalid_does_not_mask_integrity_halt (__main__.SafetyAndPersistenceTests.test_real_stage_candidate_invalid_does_not_mask_integrity_halt) ... ok
test_real_stage_dependency_selector_and_source_halts (__main__.SafetyAndPersistenceTests.test_real_stage_dependency_selector_and_source_halts) ... ok
test_real_stage_each_law5_failure_suppresses_recipes_and_markers (__main__.SafetyAndPersistenceTests.test_real_stage_each_law5_failure_suppresses_recipes_and_markers) ... ok
test_real_stage_order_law5_and_baseline_before_any_marker (__main__.SafetyAndPersistenceTests.test_real_stage_order_law5_and_baseline_before_any_marker) ... ok
test_real_step0_stops_publish_table_without_law5_or_markers (__main__.SafetyAndPersistenceTests.test_real_step0_stops_publish_table_without_law5_or_markers) ... ok
test_source_and_law3_identity_gates_halt (__main__.SafetyAndPersistenceTests.test_source_and_law3_identity_gates_halt) ... ok
test_stopped_output_no_law5_no_markers_and_pending_chain (__main__.SafetyAndPersistenceTests.test_stopped_output_no_law5_no_markers_and_pending_chain) ... ok
test_actual_numeric_law5_and_order_projector_fault_sensitivity (__main__.SelectorAndNumericalTests.test_actual_numeric_law5_and_order_projector_fault_sensitivity) ... ok
test_concentration_19_20_21_and_nonreproducible (__main__.SelectorAndNumericalTests.test_concentration_19_20_21_and_nonreproducible) ... ok
test_frame_membership_and_relation_labels (__main__.SelectorAndNumericalTests.test_frame_membership_and_relation_labels) ... ok
test_hsic_formula_contributions_and_degenerate_diagnostic (__main__.SelectorAndNumericalTests.test_hsic_formula_contributions_and_degenerate_diagnostic) ... ok
test_law5_singleton_and_multigroup_reject_any_unassigned_write (__main__.SelectorAndNumericalTests.test_law5_singleton_and_multigroup_reject_any_unassigned_write) ... ok
test_map_none_and_law5_bypass_and_active_band_identity (__main__.SelectorAndNumericalTests.test_map_none_and_law5_bypass_and_active_band_identity) ... ok
test_margin_delta_below_at_above_and_nearest8_tie (__main__.SelectorAndNumericalTests.test_margin_delta_below_at_above_and_nearest8_tie) ... ok
test_nearest8_contenders_and_margin_immediate_float_boundaries (__main__.SelectorAndNumericalTests.test_nearest8_contenders_and_margin_immediate_float_boundaries) ... ok
test_original_capture_requires_one_override_hit_and_restores (__main__.SelectorAndNumericalTests.test_original_capture_requires_one_override_hit_and_restores) ... ok
test_proxy_matches_independent_full_solve_and_singleton (__main__.SelectorAndNumericalTests.test_proxy_matches_independent_full_solve_and_singleton) ... ok
test_proxy_uses_own_pristine_denominators_and_fp16_qualifier (__main__.SelectorAndNumericalTests.test_proxy_uses_own_pristine_denominators_and_fp16_qualifier) ... ok
test_spearman_ties_and_constant (__main__.SelectorAndNumericalTests.test_spearman_ties_and_constant) ... ok
test_wrapper_groups_targets_hparams_projectors_and_fresh_cache (__main__.SelectorAndNumericalTests.test_wrapper_groups_targets_hparams_projectors_and_fresh_cache) ... ok
test_attribution_9_10_11_against_each_control (__main__.ThresholdTests.test_attribution_9_10_11_against_each_control) ... ok
test_complete_fixture_and_per_template_edge_reading (__main__.ThresholdTests.test_complete_fixture_and_per_template_edge_reading) ... ok
test_controls_and_baseline_envelope_boundaries (__main__.ThresholdTests.test_controls_and_baseline_envelope_boundaries) ... ok
test_count_and_gain_boundaries (__main__.ThresholdTests.test_count_and_gain_boundaries) ... ok
test_each_locality_threshold_inside_at_outside (__main__.ThresholdTests.test_each_locality_threshold_inside_at_outside) ... ok
test_law5_strict_thresholds_floor_and_relative_tolerance (__main__.ThresholdTests.test_law5_strict_thresholds_floor_and_relative_tolerance) ... ok
test_replication_rules_fresh_context_fixed_map_and_loss_of_attribution (__main__.ThresholdTests.test_replication_rules_fresh_context_fixed_map_and_loss_of_attribution) ... ok
test_replication_schedule_and_never_adopt_shuffled (__main__.ThresholdTests.test_replication_schedule_and_never_adopt_shuffled) ... ok
test_write_ratio_and_relation_report_only (__main__.ThresholdTests.test_write_ratio_and_relation_report_only) ... ok

----------------------------------------------------------------------
Ran 43 tests in 6.073s

OK
C10V_LAYERPICK_SELFTEST_PASS: synthetic only; torch/transformers/tokenizers/model imports absent
```

## Stage commands / handoff

Stage commands are **unchanged**. The operator flags, `step0` → `pass1` → conditional `pass2` order, `--law3-ref results/c10q_stacked/passS.json`, and paused/finished-autoresearch gate remain as in `results/c10v_layerpick_codex_impl.md`. The CLI's legacy `--law3-ref` name now populates the accurately named JSON field `preflight_controls_reference`.

Use a fresh output directory under `results/c10v_layerpick/` for the post-fix run: the identity pins all three changed source hashes, and existing stage records are exclusive. No stage was launched by this fix round. The report and retained selftests provide the session handoff for the lead's implementation delta review and subsequent authorized stage schedule.

## Objections

none.
