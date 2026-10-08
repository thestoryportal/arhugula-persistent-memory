# C10X engine-path model-free build — D-C10x-enginepath

**BUILD PASS (CPU/model-free): 63 tests passed; all 18 required mutants rejected; every mutated file restored with matching SHA-256.** No C10X GPU/model run, live LAW#3/LAW#5 gate, T8 MPS admission check or scientific outcome was observed.

Model: Codex / GPT-6 as named by the host. Exact backend ID and reasoning effort: **UNVERIFIABLE**. Date: 2026-10-08. Worktree: `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a`; branch: `worktree-c10k-route-a`, verified at session start and again at closeout. Below, W means this absolute worktree; A/I/R/Z/T/S mean the six files under `experiments/track_c/` in the file table.

**Current pinned prereg SHA-256:** `43a81103d68b953c2007e978b3ebecf11aadf66a7f121346047279845e8fc883`. The program replaced the original `d6b6701ad8c5e81d317ffdb29059addbdd83d284c1b63439735f29c3e31d855d` pin by appending §12 Amendment P during this build. Both pins and the original before-state are preserved in the evidence. The first 585 lines of the new prereg still hash to the original pin.

Authority: the complete `/Users/robertrhu/.claude/jobs/8ac4cacf/tmp/codex_c10x_build_brief.md`, including binding §10; the complete prereg §§0–11; then §12 :587–635, read in full when the program supplied it. Brief §10 replaces all earlier Q1–Q7 defaults. Amendment P replaces the original :106 resampling and :124 combination sentences. Replication now measures **fixed-template regeneration**, conditional on the selected recorded C10Q set.

The 03:45 MDT program confirmation permitted initial serial CPU work. Later explicit GPU-LIVE instructions paused Python after the current command; GPU-CLEAR and the later permission for light serial Python permitted resumption. All tests used CPU tensors and one torch thread under `/private/tmp/c10x_build/roots/`. The 58-test run and fingerprint finished before the last GPU-LIVE message. While that benchmark was live, work used file reads/edits only. After BENCH-DONE, light one-thread CPU tests resumed. A sequencing mistake briefly overlapped two exploratory mutation runs; those logs are excluded, both checks were rerun individually, and every accepted final mutation was serial. The final restored suite has 63 tests. No model, tokenizer, transformers or datasets were loaded by tests, and no MPS tensor/API was used.

## Files and scope

All six source files and this report were absent in the original R2 before-state. Only these seven repository paths were written by this build; other build artifacts are under `/private/tmp/c10x_build/`. No git write, commit, chmod, experiment execution, ledger update or engine edit was performed.

| New source file | Final SHA-256 |
|---|---|
| `experiments/track_c/c10x_enginepath_arms.py` | `798993b823232643575a2749ba9e9278bc8a4bae62b6b3d4d25563c615c10ed2` |
| `experiments/track_c/c10x_enginepath_inertness.py` | `665e954cc75624f44b01353e015eb55b3c61d80a87042be1d835712d663921cf` |
| `experiments/track_c/c10x_enginepath_read.py` | `b9543fc18961feb505dfa76a393c94a0438ea6081d1a9559148ff50134e40978` |
| `experiments/track_c/c10x_enginepath_selftest.py` | `2e617a787bff334c20ead6f73d1518b474a85c762058f30f2e8a407d05f909f4` |
| `experiments/track_c/c10x_enginepath_telemetry_check.py` | `f0d55574c3a23908b34c4f4081d11f4270a92314eedfbe81432ebe0024eace4f` |
| `experiments/track_c/c10x_overtone_z.py` | `70ad3d1b57db5ced0c6b69eb9ea40b50aed0773b8c0e04e9bad086c84f0d8664` |

The final report's own SHA is recorded after publication in `/private/tmp/c10x_build/report_receipt.json`; a file cannot embed its final self-hash. The intermediate pre-code plan has SHA `a5f404def6318a2eef1820d4774719a7af6c01a39f2b28ff4baa74b1b24ef7da` and is preserved at `/private/tmp/c10x_build/precode_plan.md`.

Scope receipts:

- Original before-state: `/private/tmp/c10x_build/before/` — porcelain, 188 file-by-file R5 hashes, seven R2 absent/null entries, and 7,086 `(path,size,mtime_ns)` listing entries.
- Post-program-amendment baseline: `/private/tmp/c10x_build/amendment_p_before/`.
- Final source/test snapshot: `/private/tmp/c10x_build/after_final_closeout/`. All 188 hashes equal the post-amendment baseline. Relative to the original snapshot, **187 are unchanged** and the only difference is the program-authored prereg appendix, old pin → new pin above. The exact old-text prefix hash confirms append-only preservation. The build did not edit the prereg.
- The benchmark is a newly named read-only input under P1, not an original R5 table omission silently rebased. Its observed pin-stage and final SHA is `9b25a207f630fbfa0d60c80a74f22289ad3bb2cc160d0fc72d7e0367f9a47a1a`; its bytes were not edited here.
- Final listing: 7,681 entries; one attributed report entry, **zero unexplained protected entries**, and 2,733 observed/unattributed changes elsewhere. These include concurrent C10W/C10Y/C10Z/labviz activity; they are not attributed to this build. The complete delta is `after_final_closeout/listing_difference.json`, SHA `4d55517be16d7b444c6ebf4bf79ca5e87b9ef84930b05d1c10a7d6a1ededffc9`. Before listing SHA: `bb67c43f89f2a04217c4e59bc034771f6f671a4ddb5e44936aa7f5d8b4e1c364`; final listing SHA: `7e4f27496e36b81909ad6cad303bba808597d6a91ada1f6a34f24aa27ed08c35`.
- The final suite itself reported no protected or unattributed listing change during its own execution. Global-tree cleanliness is not claimed. The report's final publication is the remaining authorized R2 write.

Full before/after porcelain diff; C10X's six source additions and report addition are attributed here, all other deltas are observed/unattributed:

```diff
--- before/status
+++ after_final_closeout/status
@@ -1,33 +1,54 @@
  M .gitignore
- M experiments/track_c/c10w_oracle_eval.py
- M experiments/track_c/c10w_oracle_selftest.py
- M experiments/track_c/c10z_astra_arms.py
- M experiments/track_c/c10z_astra_read.py
  M experiments/track_c/c10z_astra_selftest.py
- M tools/c10w_p2_gate.py
- M tools/run_c10w_p2.sh
- M tools/run_c10w_p2_stage.sh
+ M tools/labviz/review.mjs
+ M tools/labviz/test_fix_harness.cjs
 ?? .ignore
 ?? architecture_profile/c10w_oracle_halt_diagnostic_20261008T060601_334913Z.json
-?? experiments/track_c/c10z_astra_benchmark.py
-?? experiments/track_c/c10z_astra_benchmark_selftest.py
-?? experiments/track_c/c10z_astra_telemetry_check.py
+?? architecture_profile/c10z_astra_halt_diagnostic.json
+?? architecture_profile/c10z_astra_halt_diagnostic_20261008T124710.311412Z.json
+?? experiments/track_c/c10x_enginepath_arms.py
+?? experiments/track_c/c10x_enginepath_inertness.py
+?? experiments/track_c/c10x_enginepath_read.py
+?? experiments/track_c/c10x_enginepath_selftest.py
+?? experiments/track_c/c10x_enginepath_telemetry_check.py
+?? experiments/track_c/c10x_overtone_z.py
+?? experiments/track_c/c10y_directdw_arms.py
+?? experiments/track_c/c10y_directdw_read.py
+?? experiments/track_c/c10y_directdw_selftest.py
+?? experiments/track_c/c10y_directdw_telemetry_check.py
 ?? external_prior_art
+?? memory_mirror/test-first-one-round-builds.md
 ?? results/autoresearch_c10_equivalence_2026-10-06T0815.json
 ?? results/autoresearch_reaim/
-?? results/c10w_oracle/p2_20261008T034226_086980Z/
-?? results/c10w_oracle/step0_20261007T223638_531381Z/amendment_A1_evaluator.json
+?? results/c10w_oracle/p2_20261008T034226_086980Z/attempt1_halted/HALT.json
+?? results/c10w_oracle/p2_20261008T034226_086980Z/attempt1_halted/eval.json
+?? results/c10w_oracle/p2_20261008T034226_086980Z/attempt1_halted/eval_halt.json
+?? results/c10w_oracle/p2_20261008T034226_086980Z/eval.json
+?? results/c10w_oracle/p2_20261008T034226_086980Z/preflight.json
+?? results/c10w_oracle/p2_20261008T034226_086980Z/reattempt2_dispatch.json
+?? results/c10w_oracle/p2_20261008T034226_086980Z/reattempt2_dispatch_entered.json
+?? results/c10w_oracle/p2_20261008T034226_086980Z/reattempt2_eval_started.json
+?? results/c10w_oracle/p2_20261008T034226_086980Z/train/
 ?? results/c10w_oracle_logs/attempt1_halted/
 ?? results/c10w_oracle_logs/p2-a1-s1.gate.20261007T220211.50811.json
 ?? results/c10w_oracle_logs/p2-a7-rt.gate.20261007T220753.90179.json
 ?? results/c10w_oracle_logs/p2-a7-s1.gate.20261007T214226.17018.json
 ?? results/c10w_oracle_logs/p2-canon-s1.gate.20261007T215636.11061.json
 ?? results/c10w_oracle_logs/p2-eval.gate.20261008T030455.59962.json
+?? results/c10w_oracle_logs/p2-read-attempt2.json
 ?? results/c10w_oracle_logs/p2-shuf-rt.gate.20261007T221517.41222.json
 ?? results/c10w_oracle_logs/p2-shuf-s1.gate.20261007T214924.63725.json
 ?? results/c10w_oracle_logs/p2_launch_fingerprint.txt
-?? results/c10w_p2rerun_codex_impl.md
-?? results/c10z_build_codex_impl.md
+?? results/c10x_enginepath_codex_build.md
+?? results/c10y_directdw_codex_build.md
+?? results/c10z_astra/
+?? results/c10z_astra_attempt2/
+?? results/c10z_astra_benchmark/20261008T104535Z/heartbeat.json
+?? results/c10z_astra_benchmark/20261008T104535Z/run.json
+?? results/c10z_astra_benchmark/20261008T104535Z/svd_child.json
+?? results/c10z_astra_benchmark/20261008T121345Z/heartbeat.json
+?? results/c10z_astra_benchmark/20261008T121345Z/run.json
+?? results/c10z_astra_benchmark/20261008T121345Z/svd_child.json
 ?? results/infranodus_research_arc_2026-10-05/fulltext/
 ?? results/infranodus_research_arc_2026-10-05/operator_chat_inbox/round3_20261005/infranodus-transcend-corpus-topics-C10.txt.rtf
 ?? results/infranodus_research_arc_2026-10-05/operator_chat_inbox/round3_20261005/infranodus-transcend-corpus-topics-C10_2.txt.rtf
@@ -61,8 +82,8 @@
 ?? results/labviz_codex_impl.md
 ?? results/labviz_v2_codex_impl.md
 ?? results/labviz_v2_phase1_design_review.md
-?? tools/c10w_p2_evaluator_A1.diff
-?? tools/c10w_p2_rerun.py
-?? tools/labviz/
+?? results/labviz_v2_phase1_design_review_r2.md
+?? results/labviz_v2_phase1_design_review_r3.md
+?? results/labviz_v2_phase1_design_review_r4.md
+?? results/labviz_v2_phase1_design_review_r5.md
 ?? tools/labviz_serve.sh
-?? tools/run_c10z_attempt.sh
```

The complete R5 before=after table is in the appendix. Required protected-path `git diff --quiet` exited **0**, both initially and at final collection.

## Numbered test mapping

Rows 1–36 reproduce the numbered plan written into this report **before production code existed**. Rows 37–63 are later integration, adversarial-admission and program-steering tests. Required boundaries in the original plan were tested before implementation; additional no-sampling, cache-cleanup, reader-admission and Amendment P regressions have separately recorded assertion-level RED evidence. The process-combination row now follows binding P4.

All test references below are in `experiments/track_c/c10x_enginepath_selftest.py`; production references are exact current file:line locations.

| # | Authority | Test name and line | Implemented seam |
|---|---|---|---|
| 1 | prereg :130–132; brief §6 | `test_reader_law3_boundaries` · selftest:296 | `experiments/track_c/c10x_enginepath_read.py:234` |
| 2 | prereg :134 | `test_reader_control_boundaries` · selftest:311 | `experiments/track_c/c10x_enginepath_read.py:418` |
| 3 | prereg :136–147, :155 | `test_reader_count_classes` · selftest:319 | `experiments/track_c/c10x_enginepath_read.py:418` |
| 4 | prereg :138 | `test_reader_locality_boundaries` · selftest:328 | `experiments/track_c/c10x_enginepath_read.py:379` |
| 5 | prereg :149 | `test_reader_qualifier_boundaries` · selftest:342 | `experiments/track_c/c10x_enginepath_read.py:418` |
| 6 | prereg :151–153 | `test_reader_replication` · selftest:350 | `experiments/track_c/c10x_enginepath_read.py:464` |
| 7 | prereg :157–178 | `test_reader_interpretation_and_null_table` · selftest:364 | `experiments/track_c/c10x_enginepath_read.py:402`, `experiments/track_c/c10x_enginepath_read.py:396` |
| 8 | prereg :124, :130 | `test_reader_validity` · selftest:376 | `experiments/track_c/c10x_enginepath_read.py:249` |
| 9 | prereg :130 | `test_reader_flags_denominators_nulls` · selftest:393 | `experiments/track_c/c10x_enginepath_read.py:135`, `experiments/track_c/c10x_enginepath_read.py:111` |
| 10 | prereg :124; T9; superseded by P4 :620–624 | `test_reader_process_combination` · selftest:407 | `experiments/track_c/c10x_enginepath_read.py:464` |
| 11 | prereg :44, :69, :82 | `test_dispatch_call_time_flag` · selftest:436 | `experiments/track_c/c10x_enginepath_arms.py:568` |
| 12 | prereg :43–44 | `test_fe_modes_and_keys` · selftest:447 | `experiments/track_c/c10x_enginepath_arms.py:441`, `experiments/track_c/c10x_enginepath_arms.py:458` |
| 13 | prereg :43; brief §6 | `test_fe_ast_three_changes` · selftest:456 | `experiments/track_c/c10x_enginepath_arms.py:499` |
| 14 | prereg :81 | `test_active_null_negative_controls` · selftest:459 | `experiments/track_c/c10x_enginepath_inertness.py:146` |
| 15 | prereg :66 | `test_tolerance_and_finiteness` · selftest:465 | `experiments/track_c/c10x_enginepath_inertness.py:48` |
| 16 | prereg :68 | `test_pristine_hash_restore_hooks` · selftest:476 | `experiments/track_c/c10x_enginepath_inertness.py:84` |
| 17 | Amendment M2 :546–565 | `test_capture_bindings_identity_attribution` · selftest:492 | `experiments/track_c/c10x_enginepath_inertness.py:117` |
| 18 | prereg :82, :104 | `test_recipe_states_counters` · selftest:505 | `experiments/track_c/c10x_enginepath_arms.py:599` |
| 19 | prereg :100 | `test_baseline_miss_stops_candidates` · selftest:521 | `experiments/track_c/c10x_enginepath_arms.py:1089` |
| 20 | prereg :124, :188; brief §10 Q7 | `test_launch_refusals` · selftest:536 | `experiments/track_c/c10x_enginepath_arms.py:210`, `experiments/track_c/c10x_enginepath_arms.py:143` |
| 21 | prereg :118 | `test_watchdog_and_projection` · selftest:544 | `experiments/track_c/c10x_enginepath_arms.py:246`, `experiments/track_c/c10x_enginepath_arms.py:268`, `experiments/track_c/c10x_enginepath_arms.py:753` |
| 22 | prereg :106; brief §4.1 | `test_process2_requires_eligibility` · selftest:556 | `experiments/track_c/c10x_enginepath_arms.py:174` |
| 23 | prereg :99; brief §10 Q4 | `test_knobs_and_frame_subjects` · selftest:561 | `experiments/track_c/c10x_enginepath_arms.py:150` |
| 24 | prereg :51–60, :75 | `test_solver_ast_and_gradients` · selftest:571 | `experiments/track_c/c10x_overtone_z.py:8`, `experiments/track_c/c10x_overtone_z.py:227` |
| 25 | prereg :73 | `test_independent_full_vocabulary_audit` · selftest:594 | `experiments/track_c/c10x_enginepath_read.py:511` |
| 26 | T1 :283–294; T4 | `test_telemetry_switch_admission` · selftest:621 | `experiments/track_c/c10x_enginepath_arms.py:182` |
| 27 | T2–T7 :295–409 | `test_telemetry_code_path_equality` · selftest:628 | `experiments/track_c/c10x_enginepath_arms.py:367`, `experiments/track_c/c10x_enginepath_arms.py:599` |
| 28 | T5 :368–382 | `test_telemetry_failure_boundaries` · selftest:639 | `experiments/track_c/c10x_enginepath_arms.py:285` |
| 29 | T7 :389–409 | `test_telemetry_state_unchanged` · selftest:661 | `experiments/track_c/c10x_enginepath_arms.py:345` |
| 30 | T8 :410–447 | `test_telemetry_inertness_schedule` · selftest:674 | `experiments/track_c/c10x_enginepath_arms.py:707`, `experiments/track_c/c10x_enginepath_telemetry_check.py:343` |
| 31 | T11 :480–503 | `test_post_run_answer_audit` · selftest:683 | `experiments/track_c/c10x_enginepath_telemetry_check.py:248`, `experiments/track_c/c10x_enginepath_telemetry_check.py:396` |
| 32 | T3 :305–329; T10 :459–478 | `test_telemetry_line_volume` · selftest:697 | `experiments/track_c/c10x_enginepath_arms.py:285` |
| 33 | brief §6 round-trips | `test_strict_json_roundtrips` · selftest:713 | `experiments/track_c/c10x_enginepath_arms.py:74`, `experiments/track_c/c10x_enginepath_read.py:95` |
| 34 | brief §5.5 | `test_isolation_positive_control_children_meta` · selftest:720 | `experiments/track_c/c10x_enginepath_selftest.py:27`, `experiments/track_c/c10x_enginepath_selftest.py:272`, `experiments/track_c/c10x_enginepath_arms.py:143` |
| 35 | brief §5.6; M3 :567–577 | `test_float64_dense_reference` · selftest:610 | `experiments/track_c/c10x_enginepath_inertness.py:30`, `experiments/track_c/c10x_enginepath_inertness.py:41` |
| 36 | brief R5, §7; explicit program Amendment P exception | `test_frozen_bytes_and_imports` · selftest:739 | `experiments/track_c/c10x_enginepath_selftest.py:272` |
| 37 | prereg :43, :94, :104; T7 | `test_three_recipe_telemetry_probe_and_file_equality` · selftest:750 | `experiments/track_c/c10x_enginepath_arms.py:599`, `experiments/track_c/c10x_enginepath_arms.py:1009` |
| 38 | prereg :78, :81 | `test_actual_fe_writes_and_null_solve_observer` · selftest:797 | `experiments/track_c/c10x_enginepath_arms.py:458`, `experiments/track_c/c10x_enginepath_inertness.py:159` |
| 39 | prereg :80; M2 | `test_actual_singleton_reduction_and_resolved_capture` · selftest:816 | `experiments/track_c/c10x_enginepath_arms.py:865`, `experiments/track_c/c10x_enginepath_inertness.py:117` |
| 40 | T1, T8; brief §5.4 | `test_telemetry_valid_admission_and_runner_no_writes` · selftest:828 | `experiments/track_c/c10x_enginepath_arms.py:182`, `experiments/track_c/c10x_enginepath_telemetry_check.py:343` |
| 41 | T7, T10; prereg :104 | `test_telemetry_recipe_records_and_counts_equal` · selftest:851 | `experiments/track_c/c10x_enginepath_arms.py:599` |
| 42 | prereg :59–60, :75 | `test_solver_masked_gradient_clip_filter_and_tie` · selftest:886 | `experiments/track_c/c10x_overtone_z.py:8` |
| 43 | prereg :118 | `test_projection_uses_remaining_units_and_setup_clock` · selftest:904 | `experiments/track_c/c10x_enginepath_arms.py:753` |
| 44 | prereg :124 | `test_complete_stub_run_persists_every_record` · selftest:999 | `experiments/track_c/c10x_enginepath_arms.py:1089` |
| 45 | prereg :118 | `test_deadline_completion_and_previous_overhead` · selftest:1028 | `experiments/track_c/c10x_enginepath_arms.py:753`, `experiments/track_c/c10x_enginepath_arms.py:268` |
| 46 | prereg :66–81, :124, :130 | `test_detailed_admission_negative_controls` · selftest:1159 | `experiments/track_c/c10x_enginepath_read.py:972` |
| 47 | brief §5.4 verdict publication | `test_reader_publishes_invalid_with_exit_zero` · selftest:1189 | `experiments/track_c/c10x_enginepath_read.py:1210` |
| 48 | prereg :106, :124; T9; P4 | `test_admitted_process_pair_and_p2_gate` · selftest:1195 | `experiments/track_c/c10x_enginepath_arms.py:210`, `experiments/track_c/c10x_enginepath_read.py:464` |
| 49 | prereg :124; brief §6 | `test_every_science_record_roundtrip_and_reader_audit` · selftest:1214 | `experiments/track_c/c10x_enginepath_read.py:1125` |
| 50 | brief R6; prereg :118; T11 | `test_supervisor_fail_closed_and_combining_output_path` · selftest:1233 | `experiments/track_c/c10x_enginepath_arms.py:1246`, `experiments/track_c/c10x_enginepath_read.py:1125` |
| 51 | brief R1, §5.5; script/module state identity | `test_script_alias_and_preflight_refusal_in_isolated_child` · selftest:1243 | `experiments/track_c/c10x_enginepath_arms.py:1344`, `experiments/track_c/c10x_enginepath_arms.py:143` |
| 52 | program direct shell executable/git-mode requirement | `test_direct_shell_launchers_are_executable_in_git` · selftest:1255 | `experiments/track_c/c10x_enginepath_arms.py:1246` |
| 53 | prereg :66–81, :130; adversarial reader finding | `test_missing_inertness_evidence_is_refused` · selftest:991 | `experiments/track_c/c10x_enginepath_read.py:776`, `experiments/track_c/c10x_enginepath_read.py:1125` |
| 54 | program template pin; P2, P5 :614, :626–631 | `test_pinned_contexts_never_sample` · selftest:963 | `experiments/track_c/c10x_enginepath_arms.py:104`, `experiments/track_c/c10x_enginepath_arms.py:124` |
| 55 | P2 cleanup; exception regression | `test_context_binding_enter_failure_restores` · selftest:979 | `experiments/track_c/c10x_enginepath_arms.py:1089`, `experiments/track_c/c10x_enginepath_arms.py:124` |
| 56 | P1; new binding prereg SHA | `test_amendment_p_prereg_pin` · selftest:918 | `experiments/track_c/c10x_enginepath_arms.py:210`, `experiments/track_c/c10x_enginepath_read.py:249` |
| 57 | P1/P5 :605–612, :626–631 | `test_amendment_p_digest_refusals` · selftest:922 | `experiments/track_c/c10x_enginepath_arms.py:104`, `experiments/track_c/c10x_enginepath_arms.py:1089` |
| 58 | P3–P6 :616–633 | `test_pinned_processes_and_halted_context_identity` · selftest:942 | `experiments/track_c/c10x_enginepath_arms.py:1089`, `experiments/track_c/c10x_enginepath_read.py:464` |
| 59 | prereg :118; T11 :480–503 | `test_post_audit_blocks_are_killed_by_final_deadline` · selftest:1282 | `experiments/track_c/c10x_enginepath_arms.py:1201` |
| 60 | prereg :118; T11 DISABLED disposition | `test_post_audit_budget_and_disabled_disposition` · selftest:1297 | `experiments/track_c/c10x_enginepath_arms.py:1201`, `experiments/track_c/c10x_enginepath_arms.py:1246` |
| 61 | prereg :118; native startup time | `test_post_audit_startup_consumes_remaining_budget` · selftest:1328 | `experiments/track_c/c10x_enginepath_arms.py:1201` |
| 62 | T11 :480–503; strict receipt/exit/cause identity | `test_post_audit_rejects_contradictory_receipts` · selftest:1346 | `experiments/track_c/c10x_enginepath_arms.py:1201` |
| 63 | prereg :118; immutable late-HALT admission fence | `test_late_supervisor_persistence_is_unreadable` · selftest:1367 | `experiments/track_c/c10x_enginepath_arms.py:1246`, `experiments/track_c/c10x_enginepath_read.py:1125` |

The reader tests cover both sides of every brief §6 boundary: LAW#3 full 4/5/18/19, canon 4/5/10/11, first 41/42/59/60; control 67/68; class/NULL examples; below-baseline A−10/A−9; each realised frame independently; all locality equalities and one step beyond; size 1.5/1.5000001; fit 21/22 at ≥0.98; per-candidate replication and first-match interpretation. Typed nulls, nonfinite values, denominators/flags, counters and same-process/file reuse are refused. P4 additionally refuses unequal contexts/frames/hashes and jointly matching but unpinned records.

The dense test uses `torch.Generator(device='cpu').manual_seed(1008)`, a 2048×11008 tensor and a 0.013 perturbation on `[::17,::31]`. Identical distance is exactly 0 and norm ratio exactly 1; perturbed results match the dense float64 reference within 1e−12 relative. M9's fp32 replacement fails without further input hardening.


## Test-first RED and final GREEN evidence

The numbered 36-group plan was written before any production module. Step 2 ran with the modules absent (exit 1); step 3 ran real-signature stubs (exit 1). In step 3, 34 behavioral groups failed at their own assertions (46 failures including boundary subtests), **zero errors**; the guard and frozen-byte/import tests passed. Missing-module import failure is used only for step 2.

### Step 2: missing modules

Exact command (exit 1):

```sh
TMPDIR=/private/tmp/c10x_build /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python -B /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py > /private/tmp/c10x_build/red_missing.log 2>&1
```

Full 12-line output:

```text
IMPORT GUARD: c10e_bandknob/transformers/datasets absent
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 73, in <module>
    A = importlib.import_module('c10x_enginepath_arms')
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/importlib/__init__.py", line 126, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1140, in _find_and_load_unlocked
ModuleNotFoundError: No module named 'c10x_enginepath_arms'
```

### Step 3: real-signature stubs

Exact command (exit 1):

```sh
TMPDIR=/private/tmp/c10x_build /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python -B /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py > /private/tmp/c10x_build/red_stubs.log 2>&1
```

Full 476-line output, retaining every behavioral failing assertion:

```text
test_reader_control_boundaries (__main__.ReaderTests.test_reader_control_boundaries) ... FAIL
test_reader_count_classes (__main__.ReaderTests.test_reader_count_classes) ... FAIL
test_reader_flags_denominators_nulls (__main__.ReaderTests.test_reader_flags_denominators_nulls) ... FAIL
test_reader_interpretation_and_null_table (__main__.ReaderTests.test_reader_interpretation_and_null_table) ... FAIL
test_reader_law3_boundaries (__main__.ReaderTests.test_reader_law3_boundaries) ... 
  test_reader_law3_boundaries (__main__.ReaderTests.test_reader_law3_boundaries) (field='para_full_n', value=4) ... FAIL
  test_reader_law3_boundaries (__main__.ReaderTests.test_reader_law3_boundaries) (field='para_full_n', value=5) ... FAIL
  test_reader_law3_boundaries (__main__.ReaderTests.test_reader_law3_boundaries) (field='para_full_n', value=18) ... FAIL
  test_reader_law3_boundaries (__main__.ReaderTests.test_reader_law3_boundaries) (field='para_full_n', value=19) ... FAIL
  test_reader_law3_boundaries (__main__.ReaderTests.test_reader_law3_boundaries) (field='canon_full_n', value=4) ... FAIL
  test_reader_law3_boundaries (__main__.ReaderTests.test_reader_law3_boundaries) (field='canon_full_n', value=5) ... FAIL
  test_reader_law3_boundaries (__main__.ReaderTests.test_reader_law3_boundaries) (field='canon_full_n', value=10) ... FAIL
  test_reader_law3_boundaries (__main__.ReaderTests.test_reader_law3_boundaries) (field='canon_full_n', value=11) ... FAIL
  test_reader_law3_boundaries (__main__.ReaderTests.test_reader_law3_boundaries) (field='para_first_n', value=41) ... FAIL
  test_reader_law3_boundaries (__main__.ReaderTests.test_reader_law3_boundaries) (field='para_first_n', value=42) ... FAIL
  test_reader_law3_boundaries (__main__.ReaderTests.test_reader_law3_boundaries) (field='para_first_n', value=59) ... FAIL
  test_reader_law3_boundaries (__main__.ReaderTests.test_reader_law3_boundaries) (field='para_first_n', value=60) ... FAIL
test_reader_law3_boundaries (__main__.ReaderTests.test_reader_law3_boundaries) ... FAIL
test_reader_locality_boundaries (__main__.ReaderTests.test_reader_locality_boundaries) ... FAIL
test_reader_process_combination (__main__.ReaderTests.test_reader_process_combination) ... FAIL
test_reader_qualifier_boundaries (__main__.ReaderTests.test_reader_qualifier_boundaries) ... FAIL
test_reader_replication (__main__.ReaderTests.test_reader_replication) ... FAIL
test_reader_validity (__main__.ReaderTests.test_reader_validity) ... FAIL
test_active_null_negative_controls (__main__.SeamTests.test_active_null_negative_controls) ... FAIL
test_baseline_miss_stops_candidates (__main__.SeamTests.test_baseline_miss_stops_candidates) ... FAIL
test_capture_bindings_identity_attribution (__main__.SeamTests.test_capture_bindings_identity_attribution) ... FAIL
test_dispatch_call_time_flag (__main__.SeamTests.test_dispatch_call_time_flag) ... FAIL
test_fe_ast_three_changes (__main__.SeamTests.test_fe_ast_three_changes) ... FAIL
test_fe_modes_and_keys (__main__.SeamTests.test_fe_modes_and_keys) ... FAIL
test_float64_dense_reference (__main__.SeamTests.test_float64_dense_reference) ... FAIL
test_independent_full_vocabulary_audit (__main__.SeamTests.test_independent_full_vocabulary_audit) ... FAIL
test_knobs_and_frame_subjects (__main__.SeamTests.test_knobs_and_frame_subjects) ... FAIL
test_launch_refusals (__main__.SeamTests.test_launch_refusals) ... FAIL
test_pristine_hash_restore_hooks (__main__.SeamTests.test_pristine_hash_restore_hooks) ... FAIL
test_process2_requires_eligibility (__main__.SeamTests.test_process2_requires_eligibility) ... FAIL
test_recipe_states_counters (__main__.SeamTests.test_recipe_states_counters) ... FAIL
test_solver_ast_and_gradients (__main__.SeamTests.test_solver_ast_and_gradients) ... FAIL
test_tolerance_and_finiteness (__main__.SeamTests.test_tolerance_and_finiteness) ... FAIL
test_watchdog_and_projection (__main__.SeamTests.test_watchdog_and_projection) ... FAIL
test_frozen_bytes_and_imports (__main__.TelemetryTests.test_frozen_bytes_and_imports) ... IMPORT GUARD PASS: c10e_bandknob, transformers, datasets absent
ok
test_isolation_positive_control_children_meta (__main__.TelemetryTests.test_isolation_positive_control_children_meta) ... ok
test_post_run_answer_audit (__main__.TelemetryTests.test_post_run_answer_audit) ... FAIL
test_strict_json_roundtrips (__main__.TelemetryTests.test_strict_json_roundtrips) ... FAIL
test_telemetry_code_path_equality (__main__.TelemetryTests.test_telemetry_code_path_equality) ... FAIL
test_telemetry_failure_boundaries (__main__.TelemetryTests.test_telemetry_failure_boundaries) ... FAIL
test_telemetry_inertness_schedule (__main__.TelemetryTests.test_telemetry_inertness_schedule) ... FAIL
test_telemetry_line_volume (__main__.TelemetryTests.test_telemetry_line_volume) ... FAIL
test_telemetry_state_unchanged (__main__.TelemetryTests.test_telemetry_state_unchanged) ... FAIL
test_telemetry_switch_admission (__main__.TelemetryTests.test_telemetry_switch_admission) ... FAIL

======================================================================
FAIL: test_reader_control_boundaries (__main__.ReaderTests.test_reader_control_boundaries)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 296, in test_reader_control_boundaries
    self.assertEqual(out['base'], 'INVALID-CONTROLS' if n == 67 else 'LEAD')
AssertionError: 'STUB' != 'INVALID-CONTROLS'
- STUB
+ INVALID-CONTROLS


======================================================================
FAIL: test_reader_count_classes (__main__.ReaderTests.test_reader_count_classes)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 303, in test_reader_count_classes
    self.assertEqual(self.outcome(f)['arms']['I-2']['base'], label)
AssertionError: 'STUB' != 'NULL'
- STUB
+ NULL


======================================================================
FAIL: test_reader_flags_denominators_nulls (__main__.ReaderTests.test_reader_flags_denominators_nulls)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 377, in test_reader_flags_denominators_nulls
    self.assertEqual(self.outcome(f)['status'],'INVALID')
AssertionError: 'STUB' != 'INVALID'
- STUB
+ INVALID


======================================================================
FAIL: test_reader_interpretation_and_null_table (__main__.ReaderTests.test_reader_interpretation_and_null_table)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 350, in test_reader_interpretation_and_null_table
    self.assertEqual(o['null_row'],expected)
AssertionError: 'STUB' != 'NO-DEFICIT'
- STUB
+ NO-DEFICIT


======================================================================
FAIL: test_reader_law3_boundaries (__main__.ReaderTests.test_reader_law3_boundaries) (field='para_full_n', value=4)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 285, in test_reader_law3_boundaries
    self.assertEqual(R.law3(a), bounds[0] <= value <= bounds[1])
AssertionError: None != False

======================================================================
FAIL: test_reader_law3_boundaries (__main__.ReaderTests.test_reader_law3_boundaries) (field='para_full_n', value=5)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 285, in test_reader_law3_boundaries
    self.assertEqual(R.law3(a), bounds[0] <= value <= bounds[1])
AssertionError: None != True

======================================================================
FAIL: test_reader_law3_boundaries (__main__.ReaderTests.test_reader_law3_boundaries) (field='para_full_n', value=18)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 285, in test_reader_law3_boundaries
    self.assertEqual(R.law3(a), bounds[0] <= value <= bounds[1])
AssertionError: None != True

======================================================================
FAIL: test_reader_law3_boundaries (__main__.ReaderTests.test_reader_law3_boundaries) (field='para_full_n', value=19)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 285, in test_reader_law3_boundaries
    self.assertEqual(R.law3(a), bounds[0] <= value <= bounds[1])
AssertionError: None != False

======================================================================
FAIL: test_reader_law3_boundaries (__main__.ReaderTests.test_reader_law3_boundaries) (field='canon_full_n', value=4)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 285, in test_reader_law3_boundaries
    self.assertEqual(R.law3(a), bounds[0] <= value <= bounds[1])
AssertionError: None != False

======================================================================
FAIL: test_reader_law3_boundaries (__main__.ReaderTests.test_reader_law3_boundaries) (field='canon_full_n', value=5)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 285, in test_reader_law3_boundaries
    self.assertEqual(R.law3(a), bounds[0] <= value <= bounds[1])
AssertionError: None != True

======================================================================
FAIL: test_reader_law3_boundaries (__main__.ReaderTests.test_reader_law3_boundaries) (field='canon_full_n', value=10)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 285, in test_reader_law3_boundaries
    self.assertEqual(R.law3(a), bounds[0] <= value <= bounds[1])
AssertionError: None != True

======================================================================
FAIL: test_reader_law3_boundaries (__main__.ReaderTests.test_reader_law3_boundaries) (field='canon_full_n', value=11)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 285, in test_reader_law3_boundaries
    self.assertEqual(R.law3(a), bounds[0] <= value <= bounds[1])
AssertionError: None != False

======================================================================
FAIL: test_reader_law3_boundaries (__main__.ReaderTests.test_reader_law3_boundaries) (field='para_first_n', value=41)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 285, in test_reader_law3_boundaries
    self.assertEqual(R.law3(a), bounds[0] <= value <= bounds[1])
AssertionError: None != False

======================================================================
FAIL: test_reader_law3_boundaries (__main__.ReaderTests.test_reader_law3_boundaries) (field='para_first_n', value=42)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 285, in test_reader_law3_boundaries
    self.assertEqual(R.law3(a), bounds[0] <= value <= bounds[1])
AssertionError: None != True

======================================================================
FAIL: test_reader_law3_boundaries (__main__.ReaderTests.test_reader_law3_boundaries) (field='para_first_n', value=59)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 285, in test_reader_law3_boundaries
    self.assertEqual(R.law3(a), bounds[0] <= value <= bounds[1])
AssertionError: None != True

======================================================================
FAIL: test_reader_law3_boundaries (__main__.ReaderTests.test_reader_law3_boundaries) (field='para_first_n', value=60)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 285, in test_reader_law3_boundaries
    self.assertEqual(R.law3(a), bounds[0] <= value <= bounds[1])
AssertionError: None != False

======================================================================
FAIL: test_reader_law3_boundaries (__main__.ReaderTests.test_reader_law3_boundaries)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 289, in test_reader_law3_boundaries
    self.assertEqual(R.law3(a), n == 68)
AssertionError: None != False

======================================================================
FAIL: test_reader_locality_boundaries (__main__.ReaderTests.test_reader_locality_boundaries)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 313, in test_reader_locality_boundaries
    self.assertEqual(self.outcome(f)['arms']['I-2']['base'], label)
AssertionError: 'STUB' != 'LEAD'
- STUB
+ LEAD


======================================================================
FAIL: test_reader_process_combination (__main__.ReaderTests.test_reader_process_combination)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 392, in test_reader_process_combination
    with self.assertRaises(ValueError):R.combine(f,bad)
AssertionError: ValueError not raised

======================================================================
FAIL: test_reader_qualifier_boundaries (__main__.ReaderTests.test_reader_qualifier_boundaries)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 325, in test_reader_qualifier_boundaries
    self.assertEqual('-LARGE-WRITE' in self.outcome(f)['arms']['I-2']['qualifiers'],qualified)
AssertionError: False != True

======================================================================
FAIL: test_reader_replication (__main__.ReaderTests.test_reader_replication)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 335, in test_reader_replication
    self.assertEqual(out['arms']['I-2']['label'],expected)
AssertionError: 'STUB' != 'LEAD'
- STUB
+ LEAD


======================================================================
FAIL: test_reader_validity (__main__.ReaderTests.test_reader_validity)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 361, in test_reader_validity
    f=fixture();mutate(f);self.assertEqual(self.outcome(f)['status'],'INVALID')
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'STUB' != 'INVALID'
- STUB
+ INVALID


======================================================================
FAIL: test_active_null_negative_controls (__main__.SeamTests.test_active_null_negative_controls)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 428, in test_active_null_negative_controls
    self.assertTrue(I.active_null_structure(cur,cur,cur,['s0','s1'],['s0','s1'])['ok'])
AssertionError: False is not true

======================================================================
FAIL: test_baseline_miss_stops_candidates (__main__.SeamTests.test_baseline_miss_stops_candidates)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 493, in test_baseline_miss_stops_candidates
    self.assertEqual(result['status'],'HALTED')
AssertionError: 'STUB' != 'HALTED'
- STUB
+ HALTED


======================================================================
FAIL: test_capture_bindings_identity_attribution (__main__.SeamTests.test_capture_bindings_identity_attribution)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 465, in test_capture_bindings_identity_attribution
    self.assertEqual(len(records),1)
AssertionError: 0 != 1

======================================================================
FAIL: test_dispatch_call_time_flag (__main__.SeamTests.test_dispatch_call_time_flag)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 406, in test_dispatch_call_time_flag
    A.FE_STATE=None;self.assertEqual(A.dispatch(hp,reqs,P,[torch.zeros(2,2) for _ in hp.layers]),{})
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: None != {}

======================================================================
FAIL: test_fe_ast_three_changes (__main__.SeamTests.test_fe_ast_three_changes)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 424, in test_fe_ast_three_changes
    self.assertTrue(A.verify_fe_ast(REAL/'experiments/track_c/c10e_bandknob.py'))
AssertionError: False is not true

======================================================================
FAIL: test_fe_modes_and_keys (__main__.SeamTests.test_fe_modes_and_keys)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 417, in test_fe_modes_and_keys
    with self.assertRaises(I.Halt):A.fe_edit(hp,rq,P,[torch.zeros(2,2) for _ in hp.layers],mode='identity')
AssertionError: Halt not raised

======================================================================
FAIL: test_float64_dense_reference (__main__.SeamTests.test_float64_dense_reference)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 574, in test_float64_dense_reference
    self.assertEqual(I.relative64(a,a),0.);self.assertEqual(I.ratio64(a,a),1.)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 1.0 != 0.0

======================================================================
FAIL: test_independent_full_vocabulary_audit (__main__.SeamTests.test_independent_full_vocabulary_audit)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 559, in test_independent_full_vocabulary_audit
    self.assertIsInstance(a,dict)
AssertionError: None is not an instance of <class 'dict'>

======================================================================
FAIL: test_knobs_and_frame_subjects (__main__.SeamTests.test_knobs_and_frame_subjects)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 525, in test_knobs_and_frame_subjects
    self.assertEqual(A.FRAME_SUBJECTS,want)
AssertionError: Lists differ: [] != ['Vorbanth', 'Quillexa', 'Tremnok', 'Oskavel', 'Blynthar', 'Durmquist']

Second list contains 6 additional elements.
First extra element 0:
'Vorbanth'

- []
+ ['Vorbanth', 'Quillexa', 'Tremnok', 'Oskavel', 'Blynthar', 'Durmquist']

======================================================================
FAIL: test_launch_refusals (__main__.SeamTests.test_launch_refusals)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 498, in test_launch_refusals
    with self.assertRaises(ValueError):A.launch_preflight(self.out,None,1)
AssertionError: ValueError not raised

======================================================================
FAIL: test_pristine_hash_restore_hooks (__main__.SeamTests.test_pristine_hash_restore_hooks)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 445, in test_pristine_hash_restore_hooks
    self.assertNotEqual(I.tensor_sha(a),I.tensor_sha(a.double()))
AssertionError: '' == ''

======================================================================
FAIL: test_process2_requires_eligibility (__main__.SeamTests.test_process2_requires_eligibility)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 519, in test_process2_requires_eligibility
    with self.assertRaises(ValueError):A.process2_admission(f)
AssertionError: ValueError not raised

======================================================================
FAIL: test_recipe_states_counters (__main__.SeamTests.test_recipe_states_counters)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 485, in test_recipe_states_counters
    self.assertEqual([x[0] for x in seen],['A','I-2','I-1'])
AssertionError: Lists differ: [] != ['A', 'I-2', 'I-1']

Second list contains 3 additional elements.
First extra element 0:
'A'

- []
+ ['A', 'I-2', 'I-1']

======================================================================
FAIL: test_solver_ast_and_gradients (__main__.SeamTests.test_solver_ast_and_gradients)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 533, in test_solver_ast_and_gradients
    self.assertTrue(Z.verify_solver_ast(REAL/'memit_dry_run/memit/memit/compute_z.py'))
AssertionError: False is not true

======================================================================
FAIL: test_tolerance_and_finiteness (__main__.SeamTests.test_tolerance_and_finiteness)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 433, in test_tolerance_and_finiteness
    a=torch.tensor([1.]);self.assertEqual(I.parity(a,a,1e-5)['tol'],1e-4)
                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 0.0 != 0.0001

======================================================================
FAIL: test_watchdog_and_projection (__main__.SeamTests.test_watchdog_and_projection)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 506, in test_watchdog_and_projection
    self.assertTrue(A.project(2.,2.,4.,2.)['ok'])
AssertionError: False is not true

======================================================================
FAIL: test_post_run_answer_audit (__main__.TelemetryTests.test_post_run_answer_audit)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 651, in test_post_run_answer_audit
    self.assertEqual(T.audit_lines([header,line],expected)['verdict'],'PASS')
AssertionError: 'STUB' != 'PASS'
- STUB
+ PASS


======================================================================
FAIL: test_strict_json_roundtrips (__main__.TelemetryTests.test_strict_json_roundtrips)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 676, in test_strict_json_roundtrips
    self.assertTrue(p.exists());self.assertEqual(R.strict_json(p.read_bytes()),obj)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: False is not true

======================================================================
FAIL: test_telemetry_code_path_equality (__main__.TelemetryTests.test_telemetry_code_path_equality)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 593, in test_telemetry_code_path_equality
    self.assertTrue(callable(obs))
AssertionError: False is not true

======================================================================
FAIL: test_telemetry_failure_boundaries (__main__.TelemetryTests.test_telemetry_failure_boundaries)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 617, in test_telemetry_failure_boundaries
    self.assertEqual(buf.getvalue().count('C10X_TELEMETRY_DISABLED'),1)
AssertionError: 0 != 1

======================================================================
FAIL: test_telemetry_inertness_schedule (__main__.TelemetryTests.test_telemetry_inertness_schedule)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 640, in test_telemetry_inertness_schedule
    self.assertIsInstance(rec,dict);self.assertEqual(rec['verdict'],verdict)
                                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'STUB' != 'INERT'
- STUB
+ INERT


======================================================================
FAIL: test_telemetry_line_volume (__main__.TelemetryTests.test_telemetry_line_volume)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 663, in test_telemetry_line_volume
    self.assertTrue(callable(obs))
AssertionError: False is not true

======================================================================
FAIL: test_telemetry_state_unchanged (__main__.TelemetryTests.test_telemetry_state_unchanged)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 628, in test_telemetry_state_unchanged
    self.assertTrue(t.enabled)
AssertionError: False is not true

======================================================================
FAIL: test_telemetry_switch_admission (__main__.TelemetryTests.test_telemetry_switch_admission)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 583, in test_telemetry_switch_admission
    self.assertEqual(A.telemetry_admission(1,self.out),(False,None))
AssertionError: None != (False, None)

----------------------------------------------------------------------
Ran 36 tests in 1.152s

FAILED (failures=46)
LISTING: attributed-protected changes = {}
LISTING: observed/unattributed other changes = {}
SYS.MODULES PASS: c10e_bandknob/transformers/datasets absent
```

### Additional regressions, before their fixes

Each command is the same isolated absolute suite command with the indicated log destination. The following are the complete failure tails from the accepted assertion-level RED receipts. Exploratory import/fixture setup errors were corrected before these receipts and are not counted as behavioral RED evidence.

#### File reader must reject absent nested inertness evidence

```sh
TMPDIR=/private/tmp/c10x_build /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python -B /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py > /private/tmp/c10x_build/reader_hardening_red.log 2>&1
```

Exit 1:

```text
======================================================================
FAIL: test_missing_inertness_evidence_is_refused (__main__.FileAdmissionTests.test_missing_inertness_evidence_is_refused)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 891, in test_missing_inertness_evidence_is_refused
    with self.assertRaises(ValueError):R.audited_record(self.out)
AssertionError: ValueError not raised

----------------------------------------------------------------------
Ran 50 tests in 6.670s

FAILED (failures=1)
LISTING: attributed-protected changes = {}
LISTING: observed/unattributed other changes = {"results/c10z_astra/logs": [[128, 1791457560020268829], [128, 1791457568629880829]], "results/c10z_astra/logs/heartbeat.json": [[98, 1791457560019992453], [97, 1791457568629603994]], "results/c10z_build_codex_impl.md": [[61468, 1791453067883483133], [64886, 1791457564899355289]]}
SYS.MODULES PASS: c10e_bandknob/transformers/datasets absent
```

#### Recorded contexts must be pinned without template sampling

```sh
TMPDIR=/private/tmp/c10x_build /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python -B /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py > /private/tmp/c10x_build/pinned_contexts_red.log 2>&1
```

Exit 1:

```text
======================================================================
FAIL: test_pinned_contexts_never_sample (__main__.FileAdmissionTests.test_pinned_contexts_never_sample)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 892, in test_pinned_contexts_never_sample
    self.assertTrue(callable(getattr(A,'recorded_contexts',None)))
AssertionError: False is not true

----------------------------------------------------------------------
Ran 54 tests in 13.303s

FAILED (failures=1)
LISTING: attributed-protected changes = {}
LISTING: observed/unattributed other changes = {}
SYS.MODULES PASS: c10e_bandknob/transformers/datasets absent
```

#### A refused context-manager entry must not be exited

```sh
TMPDIR=/private/tmp/c10x_build /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python -B /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py > /private/tmp/c10x_build/context_cleanup_red.log 2>&1
```

Exit 1:

```text
======================================================================
FAIL: test_context_binding_enter_failure_restores (__main__.FileAdmissionTests.test_context_binding_enter_failure_restores)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 918, in test_context_binding_enter_failure_restores
    result=A.run(self.out,self.H,preflight=False)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_arms.py", line 1184, in run
    if context_binding is not None:context_binding.__exit__(None,None,None)
                                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 915, in __exit__
    def __exit__(self,*args):raise AssertionError('unentered binding exited')
                             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: unentered binding exited

----------------------------------------------------------------------
Ran 55 tests in 14.457s

FAILED (failures=1)
LISTING: attributed-protected changes = {}
LISTING: observed/unattributed other changes = {}
SYS.MODULES PASS: c10e_bandknob/transformers/datasets absent
```

#### Amendment P: new prereg pin, flat digest, and exact pinned process combination

```sh
TMPDIR=/private/tmp/c10x_build /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python -B /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py > /private/tmp/c10x_build/amendment_p_red_verified.log 2>&1
```

Exit 1:

```text
======================================================================
FAIL: test_amendment_p_digest_refusals (__main__.FileAdmissionTests.test_amendment_p_digest_refusals) (kind='flat_digest')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 938, in test_amendment_p_digest_refusals
    self.assertEqual(result['status'],'HALTED');baseline.assert_not_called()
                                                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 900, in assert_not_called
    raise AssertionError(msg)
AssertionError: Expected 'run_recipe' to not have been called. Called 1 times.
Calls: [call('A', '/private/tmp/c10x_build/roots/tmp1clj1i_h/configs/hparams/qwen25_3b_memit_hparams.json'),
 call().__setitem__('counters', [0, 0]),
 call().__setitem__('write_norms_float64', {}),
 call().__setitem__('residual_diagnostics', {}),
 call().get('detail', {}),
 call().get().items(),
 call().get().items().__iter__()].

======================================================================
FAIL: test_amendment_p_prereg_pin (__main__.FileAdmissionTests.test_amendment_p_prereg_pin)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 920, in test_amendment_p_prereg_pin
    self.assertEqual(A.PIN,pin);self.assertEqual(R.PREREG_SHA256,pin)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'd6b6701ad8c5e81d317ffdb29059addbdd83d284c1b63439735f29c3e31d855d' != '43a81103d68b953c2007e978b3ebecf11aadf66a7f121346047279845e8fc883'
- d6b6701ad8c5e81d317ffdb29059addbdd83d284c1b63439735f29c3e31d855d
+ 43a81103d68b953c2007e978b3ebecf11aadf66a7f121346047279845e8fc883


======================================================================
FAIL: test_reader_process_combination (__main__.ReaderTests.test_reader_process_combination) (key='ctx')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 423, in test_reader_process_combination
    with self.assertRaises(ValueError):R.combine(f,bad)
AssertionError: ValueError not raised

======================================================================
FAIL: test_reader_process_combination (__main__.ReaderTests.test_reader_process_combination) (key='frames')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 423, in test_reader_process_combination
    with self.assertRaises(ValueError):R.combine(f,bad)
AssertionError: ValueError not raised

======================================================================
FAIL: test_reader_process_combination (__main__.ReaderTests.test_reader_process_combination) (key='ctx_sha256')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 423, in test_reader_process_combination
    with self.assertRaises(ValueError):R.combine(f,bad)
AssertionError: ValueError not raised

======================================================================
FAIL: test_reader_process_combination (__main__.ReaderTests.test_reader_process_combination) (key='frames_sha256')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 423, in test_reader_process_combination
    with self.assertRaises(ValueError):R.combine(f,bad)
AssertionError: ValueError not raised

======================================================================
FAIL: test_reader_process_combination (__main__.ReaderTests.test_reader_process_combination)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 430, in test_reader_process_combination
    with self.assertRaises(ValueError):R.combine(same_bad,second_bad)
AssertionError: ValueError not raised

----------------------------------------------------------------------
Ran 58 tests in 14.637s

FAILED (failures=7)
LISTING: attributed-protected changes = {}
LISTING: observed/unattributed other changes = {}
SYS.MODULES PASS: c10e_bandknob/transformers/datasets absent
```

The final attempted run at the moment of the program appendix failed the old R5 prereg-hash assertion; `/private/tmp/c10x_build/final_attempt_at_program_amendment.log` preserves that observation. The original before-state was retained, Amendment P was read in full, and the expected frozen-prereg entry alone was updated to the explicit program pin. No other R5 baseline was rebased.

#### Bounded final-stage post-run audit must exist

```sh
TMPDIR=/private/tmp/c10x_build /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python -B /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py > /private/tmp/c10x_build/post_audit_deadline_red.log 2>&1
```

Exit 1; complete failure tail:

```text
======================================================================
FAIL: test_post_audit_blocks_are_killed_by_final_deadline (__main__.FileAdmissionTests.test_post_audit_blocks_are_killed_by_final_deadline)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 1283, in test_post_audit_blocks_are_killed_by_final_deadline
    self.assertTrue(callable(getattr(A,'bounded_answer_audit',None)))
AssertionError: False is not true

======================================================================
FAIL: test_post_audit_budget_and_disabled_disposition (__main__.FileAdmissionTests.test_post_audit_budget_and_disabled_disposition)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 1298, in test_post_audit_budget_and_disabled_disposition
    self.assertTrue(callable(getattr(A,'bounded_answer_audit',None)))
AssertionError: False is not true

----------------------------------------------------------------------
Ran 60 tests in 17.521s

FAILED (failures=2)
LISTING: attributed-protected changes = {}
LISTING: observed/unattributed other changes = {"results/c10z_astra_attempt2/logs": [[128, 1791462677561566618], [128, 1791462695875043598]], "results/c10z_astra_attempt2/logs/heartbeat.json": [[98, 1791462677561309615], [98, 1791462695874764927]]}
SYS.MODULES PASS: c10e_bandknob/transformers/datasets absent
```

#### Audit startup, receipt semantics and durable late-HALT fence

```sh
TMPDIR=/private/tmp/c10x_build /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python -B /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py > /private/tmp/c10x_build/final_review_deadline_red_verified2.log 2>&1
```

Exit 1; complete failure tail:

```text
======================================================================
FAIL: test_late_supervisor_persistence_is_unreadable (__main__.FileAdmissionTests.test_late_supervisor_persistence_is_unreadable)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 1383, in test_late_supervisor_persistence_is_unreadable
    self.assertEqual(A.watchdog(out,root/'go.json',1),1)
AssertionError: 0 != 1

======================================================================
FAIL: test_post_audit_rejects_contradictory_receipts (__main__.FileAdmissionTests.test_post_audit_rejects_contradictory_receipts) (code=1, change={})
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 1358, in test_post_audit_rejects_contradictory_receipts
    with self.assertRaises(I.Halt):A.bounded_answer_audit(self.out,10.,20.)
AssertionError: Halt not raised

======================================================================
FAIL: test_post_audit_rejects_contradictory_receipts (__main__.FileAdmissionTests.test_post_audit_rejects_contradictory_receipts) (code=0, change={'verdict': 'FAIL', 'causes': ['DISABLED']})
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 1358, in test_post_audit_rejects_contradictory_receipts
    with self.assertRaises(I.Halt):A.bounded_answer_audit(self.out,10.,20.)
AssertionError: Halt not raised

======================================================================
FAIL: test_post_audit_rejects_contradictory_receipts (__main__.FileAdmissionTests.test_post_audit_rejects_contradictory_receipts) (code=1, change={'verdict': 'FAIL', 'causes': ['MISMATCH']})
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 1358, in test_post_audit_rejects_contradictory_receipts
    with self.assertRaises(I.Halt):A.bounded_answer_audit(self.out,10.,20.)
AssertionError: Halt not raised

======================================================================
FAIL: test_post_audit_rejects_contradictory_receipts (__main__.FileAdmissionTests.test_post_audit_rejects_contradictory_receipts) (code=1, change={'verdict': 'FAIL', 'causes': ['MISMATCH', 'DISABLED']})
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 1358, in test_post_audit_rejects_contradictory_receipts
    with self.assertRaises(I.Halt):A.bounded_answer_audit(self.out,10.,20.)
AssertionError: Halt not raised

======================================================================
FAIL: test_post_audit_rejects_contradictory_receipts (__main__.FileAdmissionTests.test_post_audit_rejects_contradictory_receipts) (code=0, change={'causes': ['DISABLED']})
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 1358, in test_post_audit_rejects_contradictory_receipts
    with self.assertRaises(I.Halt):A.bounded_answer_audit(self.out,10.,20.)
AssertionError: Halt not raised

======================================================================
FAIL: test_post_audit_rejects_contradictory_receipts (__main__.FileAdmissionTests.test_post_audit_rejects_contradictory_receipts) (code=1, change={'verdict': 'FAIL', 'causes': ['UNKNOWN'], 'rerun_required': True})
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 1358, in test_post_audit_rejects_contradictory_receipts
    with self.assertRaises(I.Halt):A.bounded_answer_audit(self.out,10.,20.)
AssertionError: Halt not raised

======================================================================
FAIL: test_post_audit_rejects_contradictory_receipts (__main__.FileAdmissionTests.test_post_audit_rejects_contradictory_receipts) (code=1, change={'verdict': 'FAIL', 'causes': ['DISABLED', 'DISABLED']})
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 1358, in test_post_audit_rejects_contradictory_receipts
    with self.assertRaises(I.Halt):A.bounded_answer_audit(self.out,10.,20.)
AssertionError: Halt not raised

======================================================================
FAIL: test_post_audit_rejects_contradictory_receipts (__main__.FileAdmissionTests.test_post_audit_rejects_contradictory_receipts) (code=0, change={'causes': None})
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 1358, in test_post_audit_rejects_contradictory_receipts
    with self.assertRaises(I.Halt):A.bounded_answer_audit(self.out,10.,20.)
AssertionError: Halt not raised

======================================================================
FAIL: test_post_audit_rejects_contradictory_receipts (__main__.FileAdmissionTests.test_post_audit_rejects_contradictory_receipts) (code=0, change={'process': 2})
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 1358, in test_post_audit_rejects_contradictory_receipts
    with self.assertRaises(I.Halt):A.bounded_answer_audit(self.out,10.,20.)
AssertionError: Halt not raised

======================================================================
FAIL: test_post_audit_rejects_contradictory_receipts (__main__.FileAdmissionTests.test_post_audit_rejects_contradictory_receipts) (code=0, change={'run_id': 'other'})
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 1358, in test_post_audit_rejects_contradictory_receipts
    with self.assertRaises(I.Halt):A.bounded_answer_audit(self.out,10.,20.)
AssertionError: Halt not raised

======================================================================
FAIL: test_post_audit_rejects_contradictory_receipts (__main__.FileAdmissionTests.test_post_audit_rejects_contradictory_receipts) (code=0, change={'unexpected': True})
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 1358, in test_post_audit_rejects_contradictory_receipts
    with self.assertRaises(I.Halt):A.bounded_answer_audit(self.out,10.,20.)
AssertionError: Halt not raised

======================================================================
FAIL: test_post_audit_rejects_contradictory_receipts (__main__.FileAdmissionTests.test_post_audit_rejects_contradictory_receipts) (code=0, change={'expected_answers': True})
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 1358, in test_post_audit_rejects_contradictory_receipts
    with self.assertRaises(I.Halt):A.bounded_answer_audit(self.out,10.,20.)
AssertionError: Halt not raised

======================================================================
FAIL: test_post_audit_startup_consumes_remaining_budget (__main__.FileAdmissionTests.test_post_audit_startup_consumes_remaining_budget)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 1338, in test_post_audit_startup_consumes_remaining_budget
    self.assertEqual(timeouts,[7.])
AssertionError: Lists differ: [9.0] != [7.0]

First differing element 0:
9.0
7.0

- [9.0]
?  ^

+ [7.0]
?  ^


----------------------------------------------------------------------
Ran 63 tests in 15.231s

FAILED (failures=14)
LISTING: attributed-protected changes = {}
LISTING: observed/unattributed other changes = 43 entries; complete delta /private/tmp/c10x_build/listing_deltas/listing_1791463756804850000.json; sha256 d7e10d5e024f8dd5dcf705db9b4057a5648f89073599d601103b28c434e3e592
SYS.MODULES PASS: c10e_bandknob/transformers/datasets absent
```

The first deadline RED had two own assertion failures across 60 tests. The final review RED had 14 own assertion failures across three new groups and 63 tests, with zero errors. Earlier setup-error logs are preserved as exploratory diagnostics and excluded from RED evidence. Their fixture corrections preceded production fixes.

### Final restored suite

Exact command (exit **0**), run after restoring all 18 Amendment P mutants:

```sh
TMPDIR=/private/tmp/c10x_build /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python -B /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py > /private/tmp/c10x_build/final_pass63.log 2>&1
```

Full PASS output:

```text
test_admitted_process_pair_and_p2_gate (__main__.FileAdmissionTests.test_admitted_process_pair_and_p2_gate) ... ok
test_amendment_p_digest_refusals (__main__.FileAdmissionTests.test_amendment_p_digest_refusals) ... ok
test_amendment_p_prereg_pin (__main__.FileAdmissionTests.test_amendment_p_prereg_pin) ... ok
test_complete_stub_run_persists_every_record (__main__.FileAdmissionTests.test_complete_stub_run_persists_every_record) ... ok
test_context_binding_enter_failure_restores (__main__.FileAdmissionTests.test_context_binding_enter_failure_restores) ... ok
test_deadline_completion_and_previous_overhead (__main__.FileAdmissionTests.test_deadline_completion_and_previous_overhead) ... ok
test_detailed_admission_negative_controls (__main__.FileAdmissionTests.test_detailed_admission_negative_controls) ... ok
test_direct_shell_launchers_are_executable_in_git (__main__.FileAdmissionTests.test_direct_shell_launchers_are_executable_in_git) ... DIRECT SHELL ENTRY POINTS: none; all three supervised commands use sys.executable
ok
test_every_science_record_roundtrip_and_reader_audit (__main__.FileAdmissionTests.test_every_science_record_roundtrip_and_reader_audit) ... ok
test_late_supervisor_persistence_is_unreadable (__main__.FileAdmissionTests.test_late_supervisor_persistence_is_unreadable) ... ok
test_missing_inertness_evidence_is_refused (__main__.FileAdmissionTests.test_missing_inertness_evidence_is_refused) ... ok
test_pinned_contexts_never_sample (__main__.FileAdmissionTests.test_pinned_contexts_never_sample) ... ok
test_pinned_processes_and_halted_context_identity (__main__.FileAdmissionTests.test_pinned_processes_and_halted_context_identity) ... ok
test_post_audit_blocks_are_killed_by_final_deadline (__main__.FileAdmissionTests.test_post_audit_blocks_are_killed_by_final_deadline) ... ok
test_post_audit_budget_and_disabled_disposition (__main__.FileAdmissionTests.test_post_audit_budget_and_disabled_disposition) ... ok
test_post_audit_rejects_contradictory_receipts (__main__.FileAdmissionTests.test_post_audit_rejects_contradictory_receipts) ... ok
test_post_audit_startup_consumes_remaining_budget (__main__.FileAdmissionTests.test_post_audit_startup_consumes_remaining_budget) ... ok
test_reader_publishes_invalid_with_exit_zero (__main__.FileAdmissionTests.test_reader_publishes_invalid_with_exit_zero) ... ok
test_script_alias_and_preflight_refusal_in_isolated_child (__main__.FileAdmissionTests.test_script_alias_and_preflight_refusal_in_isolated_child) ... ok
test_supervisor_fail_closed_and_combining_output_path (__main__.FileAdmissionTests.test_supervisor_fail_closed_and_combining_output_path) ... ok
test_actual_fe_writes_and_null_solve_observer (__main__.IntegrationTests.test_actual_fe_writes_and_null_solve_observer) ... ok
test_actual_singleton_reduction_and_resolved_capture (__main__.IntegrationTests.test_actual_singleton_reduction_and_resolved_capture) ... ok
test_projection_uses_remaining_units_and_setup_clock (__main__.IntegrationTests.test_projection_uses_remaining_units_and_setup_clock) ... ok
test_solver_masked_gradient_clip_filter_and_tie (__main__.IntegrationTests.test_solver_masked_gradient_clip_filter_and_tie) ... ok
test_telemetry_recipe_records_and_counts_equal (__main__.IntegrationTests.test_telemetry_recipe_records_and_counts_equal) ... ok
test_telemetry_valid_admission_and_runner_no_writes (__main__.IntegrationTests.test_telemetry_valid_admission_and_runner_no_writes) ... ok
test_three_recipe_telemetry_probe_and_file_equality (__main__.IntegrationTests.test_three_recipe_telemetry_probe_and_file_equality) ... ok
test_reader_control_boundaries (__main__.ReaderTests.test_reader_control_boundaries) ... ok
test_reader_count_classes (__main__.ReaderTests.test_reader_count_classes) ... ok
test_reader_flags_denominators_nulls (__main__.ReaderTests.test_reader_flags_denominators_nulls) ... ok
test_reader_interpretation_and_null_table (__main__.ReaderTests.test_reader_interpretation_and_null_table) ... ok
test_reader_law3_boundaries (__main__.ReaderTests.test_reader_law3_boundaries) ... ok
test_reader_locality_boundaries (__main__.ReaderTests.test_reader_locality_boundaries) ... ok
test_reader_process_combination (__main__.ReaderTests.test_reader_process_combination) ... ok
test_reader_qualifier_boundaries (__main__.ReaderTests.test_reader_qualifier_boundaries) ... ok
test_reader_replication (__main__.ReaderTests.test_reader_replication) ... ok
test_reader_validity (__main__.ReaderTests.test_reader_validity) ... ok
test_active_null_negative_controls (__main__.SeamTests.test_active_null_negative_controls) ... ok
test_baseline_miss_stops_candidates (__main__.SeamTests.test_baseline_miss_stops_candidates) ... ok
test_capture_bindings_identity_attribution (__main__.SeamTests.test_capture_bindings_identity_attribution) ... ok
test_dispatch_call_time_flag (__main__.SeamTests.test_dispatch_call_time_flag) ... ok
test_fe_ast_three_changes (__main__.SeamTests.test_fe_ast_three_changes) ... ok
test_fe_modes_and_keys (__main__.SeamTests.test_fe_modes_and_keys) ... ok
test_float64_dense_reference (__main__.SeamTests.test_float64_dense_reference) ... ok
test_independent_full_vocabulary_audit (__main__.SeamTests.test_independent_full_vocabulary_audit) ... ok
test_knobs_and_frame_subjects (__main__.SeamTests.test_knobs_and_frame_subjects) ... ok
test_launch_refusals (__main__.SeamTests.test_launch_refusals) ... ok
test_pristine_hash_restore_hooks (__main__.SeamTests.test_pristine_hash_restore_hooks) ... ok
test_process2_requires_eligibility (__main__.SeamTests.test_process2_requires_eligibility) ... ok
test_recipe_states_counters (__main__.SeamTests.test_recipe_states_counters) ... ok
test_solver_ast_and_gradients (__main__.SeamTests.test_solver_ast_and_gradients) ... ok
test_tolerance_and_finiteness (__main__.SeamTests.test_tolerance_and_finiteness) ... ok
test_watchdog_and_projection (__main__.SeamTests.test_watchdog_and_projection) ... ok
test_frozen_bytes_and_imports (__main__.TelemetryTests.test_frozen_bytes_and_imports) ... IMPORT GUARD PASS: c10e_bandknob, transformers, datasets absent
ok
test_isolation_positive_control_children_meta (__main__.TelemetryTests.test_isolation_positive_control_children_meta) ... ok
test_post_run_answer_audit (__main__.TelemetryTests.test_post_run_answer_audit) ... ok
test_strict_json_roundtrips (__main__.TelemetryTests.test_strict_json_roundtrips) ... ok
test_telemetry_code_path_equality (__main__.TelemetryTests.test_telemetry_code_path_equality) ... ok
test_telemetry_failure_boundaries (__main__.TelemetryTests.test_telemetry_failure_boundaries) ... ok
test_telemetry_inertness_schedule (__main__.TelemetryTests.test_telemetry_inertness_schedule) ... ok
test_telemetry_line_volume (__main__.TelemetryTests.test_telemetry_line_volume) ... ok
test_telemetry_state_unchanged (__main__.TelemetryTests.test_telemetry_state_unchanged) ... ok
test_telemetry_switch_admission (__main__.TelemetryTests.test_telemetry_switch_admission) ... ok

----------------------------------------------------------------------
Ran 63 tests in 15.938s

OK
LISTING: attributed-protected changes = {}
LISTING: observed/unattributed other changes = {}
SYS.MODULES PASS: c10e_bandknob/transformers/datasets absent
```

The live loading paths were reviewed statically. A test's tiny CPU stub forward is not a live LAW#3, G, G8, X-check, resource or scientific PASS. Child watchdog tests invoked only allowlisted model-free stubs under temporary cwd/root, including a native blocking `/bin/sleep` killed at the 2-second stage deadline and a separate bounded-audit child killed at a 0.2-second deadline. The installed child `sitecustomize` guard marker was checked. No test launched a real experiment stage.


## Mutation verification

**18/18 rejected, zero survivors.** Each final mutant ran the full 63-test suite individually and serially. Each file was backed up under `/private/tmp/c10x_build/mut_backup/audited_closeout/`, mutated, then restored in `finally`; backup/restored SHA comparison passed each time. All mutation runs reported `LISTING: attributed-protected changes = {}` and the forbidden-module assertion PASS. The final restored GREEN is above.

Logs: `/private/tmp/c10x_build/mutations/audited_closeout/M1.log` … `M18.log`. Complete machine receipt: `/private/tmp/c10x_build/mutation_results_audited_closeout.json`. Earlier preliminary runs were preserved separately and are not substituted for these final outcomes. The two overlapped exploratory logs are `audited_closeout/M2_overlap_excluded.log` and `M3_overlap_excluded.log`; their outcomes are excluded. The accepted M2 and M3 logs are individual serial reruns. The final machine receipt SHA-256 is `ed0dfd10a938bdaa8c6ef761008fc267763b2b3b0f81ef309476b976b3b4e4cc`. Wrong semantic dispatch/index/mask mutants sometimes fail through the invalid path's exception; those are recorded as ERROR tests, not misreported as assertion failures.

| Mutant | Deliberate change | Failed tests | Exit | Restored SHA-256 |
|---|---|---|---:|---|
| M1 | floor bound 1e−5 → 1e−4 · `c10x_enginepath_inertness.py` | `test_tolerance_and_finiteness` | 1 | `665e954cc75624f44b01353e015eb55b3c61d80a87042be1d835712d663921cf` |
| M2 | cache the default-context flag instead of reading it at dispatch time · `c10x_enginepath_arms.py` | `test_dispatch_call_time_flag` | 1 | `798993b823232643575a2749ba9e9278bc8a4bae62b6b3d4d25563c615c10ed2` |
| M3 | divide the active FE residual by remaining layers · `c10x_enginepath_arms.py` | `test_fe_ast_three_changes` | 1 | `798993b823232643575a2749ba9e9278bc8a4bae62b6b3d4d25563c615c10ed2` |
| M4 | read FE cur at z_layer rather than the current layer · `c10x_enginepath_arms.py` | `test_actual_fe_writes_and_null_solve_observer`<br>`test_fe_ast_three_changes` | 1 | `798993b823232643575a2749ba9e9278bc8a4bae62b6b3d4d25563c615c10ed2` |
| M5 | index FE_TARGETS by list position · `c10x_enginepath_arms.py` | `test_actual_fe_writes_and_null_solve_observer`<br>`test_actual_singleton_reduction_and_resolved_capture`<br>`test_three_recipe_telemetry_probe_and_file_equality`<br>`test_fe_ast_three_changes` | 1 | `798993b823232643575a2749ba9e9278bc8a4bae62b6b3d4d25563c615c10ed2` |
| M6 | LAW#3 first lower bound 42 → 41 · `c10x_enginepath_read.py` | `test_reader_law3_boundaries (field='para_first_n', value=41)` | 1 | `b9543fc18961feb505dfa76a393c94a0438ea6081d1a9559148ff50134e40978` |
| M7 | large-write > → >= · `c10x_enginepath_read.py` | `test_reader_qualifier_boundaries` | 1 | `b9543fc18961feb505dfa76a393c94a0438ea6081d1a9559148ff50134e40978` |
| M8 | NULL I-2 deficit edge 10 → 9 · `c10x_enginepath_read.py` | `test_reader_interpretation_and_null_table` | 1 | `b9543fc18961feb505dfa76a393c94a0438ea6081d1a9559148ff50134e40978` |
| M9 | CPU float64 helper → fp32 · `c10x_enginepath_inertness.py` | `test_float64_dense_reference` | 1 | `665e954cc75624f44b01353e015eb55b3c61d80a87042be1d835712d663921cf` |
| M10 | telemetry on with variable absent · `c10x_enginepath_arms.py` | `test_admitted_process_pair_and_p2_gate`<br>`test_telemetry_switch_admission` | 1 | `798993b823232643575a2749ba9e9278bc8a4bae62b6b3d4d25563c615c10ed2` |
| M11 | telemetry mutates a scientific record · `c10x_enginepath_arms.py` | `test_telemetry_recipe_records_and_counts_equal`<br>`test_three_recipe_telemetry_probe_and_file_equality` | 1 | `798993b823232643575a2749ba9e9278bc8a4bae62b6b3d4d25563c615c10ed2` |
| M12 | install observed scorer while telemetry is off · `c10x_enginepath_arms.py` | `test_complete_stub_run_persists_every_record`<br>`test_pinned_processes_and_halted_context_identity`<br>`test_telemetry_recipe_records_and_counts_equal`<br>`test_three_recipe_telemetry_probe_and_file_equality`<br>`test_baseline_miss_stops_candidates`<br>`test_recipe_states_counters` | 1 | `798993b823232643575a2749ba9e9278bc8a4bae62b6b3d4d25563c615c10ed2` |
| M13 | telemetry calls watchdog clock · `c10x_enginepath_arms.py` | `test_telemetry_recipe_records_and_counts_equal`<br>`test_three_recipe_telemetry_probe_and_file_equality` | 1 | `798993b823232643575a2749ba9e9278bc8a4bae62b6b3d4d25563c615c10ed2` |
| M14 | telemetry catches BaseException · `c10x_enginepath_arms.py` | `test_telemetry_failure_boundaries` | 1 | `798993b823232643575a2749ba9e9278bc8a4bae62b6b3d4d25563c615c10ed2` |
| M15 | omit the primary audit hook · `c10x_enginepath_selftest.py` | `test_isolation_positive_control_children_meta` | 1 | `2e617a787bff334c20ead6f73d1518b474a85c762058f30f2e8a407d05f909f4` |
| M16 | accept non-temp selftest ROOT · `c10x_enginepath_arms.py` | `test_launch_refusals` | 1 | `798993b823232643575a2749ba9e9278bc8a4bae62b6b3d4d25563c615c10ed2` |
| M17 | clip > → >= · `c10x_overtone_z.py` | `test_solver_ast_and_gradients` | 1 | `70ad3d1b57db5ced0c6b69eb9ea40b50aed0773b8c0e04e9bad086c84f0d8664` |
| M18 | drop mask before token filtering · `c10x_overtone_z.py` | `test_solver_masked_gradient_clip_filter_and_tie`<br>`test_solver_ast_and_gradients` | 1 | `70ad3d1b57db5ced0c6b69eb9ea40b50aed0773b8c0e04e9bad086c84f0d8664` |

## Engine fingerprint and frozen source evidence

Exact command (read-only; exit 0):

```sh
LLMDB_ROOT=/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a TMPDIR=/private/tmp/c10x_build /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python -B /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/engine_fingerprint.py > /private/tmp/c10x_build/fingerprint_worktree_final.log 2>&1
```

Full output:

```text
engine fingerprint PASS: /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/memit_dry_run/memit/memit/memit_main.py
  sha256   d941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65  (expected d941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65; pod-era 5c0c706a…)
  _cov_cpu 3  (expected 3)
```

```sh
git -C /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a diff --quiet -- memit_dry_run docs/C10X_ENGINEPATH_PREREG.md experiments/track_c/c10e_bandknob.py
```

Exit **0**. The original and final byte hashes, rather than an untracked-file-insensitive git diff alone, establish preservation.

## Binding decisions, implemented seams and verbatim-copy evidence

**Unresolved PROVISIONAL scientific decisions: none.** No Q1–Q7 default remains provisional: brief §10 answers and prereg T/M rule. Amendment P supplies the later input/replication rule. Source search of all six files found no leftover `PROVISIONAL` marker. Schema names, lossless CPU audit serialization, exclusive publication, parser strictness and the profiler used to observe the original solver are implementation choices; they do not relax or add scientific thresholds.

| Ruling | Exact implementation / evidence |
|---|---|
| Q1 | Driver and reader pin the new §12 prereg SHA; T/M retained unchanged. `experiments/track_c/c10x_enginepath_arms.py:210`, `experiments/track_c/c10x_enginepath_read.py:249`. |
| Q2 / T4 | Observed scorer adds only `sink(prompt,target_ids,gen)` before the unchanged return. Original scoring inputs, return values and decode count are retained; off restores the original object. `experiments/track_c/c10x_enginepath_arms.py:367`, `experiments/track_c/c10x_enginepath_arms.py:401`. |
| Q3 / T9 | Initial P1 **and P2 have telemetry unset**. T8 is built and CPU-stub tested; actual MPS check NOT RUN. Telemetry-on is only for a fresh later attempt with an admitted live proof; its cost still counts against caps. `experiments/track_c/c10x_enginepath_arms.py:182`, `experiments/track_c/c10x_enginepath_arms.py:707`, `experiments/track_c/c10x_enginepath_telemetry_check.py:343`. |
| Q4 | c10p/c10m are never imported. FRAME_SUBJECTS is a literal copy verified by AST against c10p :30. The probe is generalised over all realised frames. `experiments/track_c/c10x_enginepath_arms.py:1009`; selftest:561. |
| Q5 / M1–M4 | Complete pre-cast updates captured through each actual writer's resolved globals, including FE; one attributed capture per expected layer, correct layer/order checked, identical returned object, finally restore. CPU fp64 reductions gate the named write comparisons and qualifier; fp32 and applied fp16 differences are beside them as report-only. `experiments/track_c/c10x_enginepath_inertness.py:117`, `experiments/track_c/c10x_enginepath_inertness.py:236`, `experiments/track_c/c10x_enginepath_arms.py:1068`, `experiments/track_c/c10x_enginepath_read.py:619`. |
| Q6 / T12 | Required absolute `--out`, fresh process/output/log identities, frozen first names and `_rerun<k>` names. Re-run predecessor and cause are required and recorded; earlier directories are preserved. `experiments/track_c/c10x_enginepath_arms.py:210`, `experiments/track_c/c10x_enginepath_arms.py:1246`. |
| Q7 | Required absolute `--go`; exact five-key JSON, experiment/process, nonempty decision ID, exact runbook location and timezone-bearing timestamp validated before model load. The program owns creation after reconsideration. `experiments/track_c/c10x_enginepath_arms.py:210`, `experiments/track_c/c10x_enginepath_arms.py:1344`. |
| Brief §10 diagnostic override | Exclusive UTC-named `architecture_profile/c10x_halt_diagnostic_<UTC>.json`; no fixed-path overwrite. `experiments/track_c/c10x_enginepath_arms.py:253`. |
| P1 | Benchmark parsed by AST without import; six strings, identity first, one placeholder each; both exact nested/flat digests compared before A. Source file is declared in start/end hashes. `experiments/track_c/c10x_enginepath_arms.py:104`, `experiments/track_c/c10x_enginepath_arms.py:88`. |
| P2/P3/P6 | Original engine cache set before the first getter, stimulus checks or A; pre-A context artifact and run-state identity persist on a LAW#3 miss; no redraw. Finally restores the prior cache, including refused-enter cleanup. `experiments/track_c/c10x_enginepath_arms.py:124`, `experiments/track_c/c10x_enginepath_arms.py:1089`. |
| P4 | Equal pinned ctx/frames and their hashes required even when two wrong lists agree. Targets may independently recompute under all existing checks; same process/file is still refused. `experiments/track_c/c10x_enginepath_read.py:464`, `experiments/track_c/c10x_enginepath_read.py:1125`. |

**Three different context digests.** Historical nested engine form via default `json.dumps`: `c7dabbe7c25a7e58653621d9cc66e37b35c865ae09b73b6a96073a184c6c98da`. Compact flat list via the benchmark's serializer: `d6c7c70026dced37bddc6adf316a3487d70227dae80a6e0ed5cdabe50caedfa0`. Compact nested context record: `eff10db6a89aabf7d67fa0c66e4cc1ac727b795c0bf756d3f8b53d0f6cd05aeb`. The first two are compared to the binding P1 constants; the third is the recomputed record hash. This is the C10Q source P1 names, not an alternate prereg template set.

The pin goes into `H.get_context_templates.__globals__['CONTEXT_TEMPLATES_CACHE']`. The original harness getter and original engine entry point resolve this same namespace (c10e :15, :182; memit_main :100, :304–323). No engine function/body/file is replaced. The no-sampling test compiles the unchanged getter AST, starts with cache None, installs a raising `generate_fast`, then calls both getter and the copied original writer. Any sampling raises. All target/X/probe/recipe calls receive the checked ctx.

**Numeric precedence.** Brief R3 :92 explicitly exempts dtype-fixed prereg arithmetic. M :540–544 preserves the other §2.4 predicates, including updated-cache parity; M :580 identifies the original :66 arithmetic as fp32. Those comparisons retain their frozen fp32 arithmetic. M1's pre-cast ΔW inputs and the large-write gate use CPU fp64, as do model-sized norm/ratio diagnostics and telemetry norms outside the explicit exemptions. The original OverTone casts, X1-(iii) casts and verbatim FE/harness delta_norms remain fixed. The initial apparent conflict was withdrawn after applying that exemption; no gate or threshold was weakened. `reject_mps_double` and stub-device tests refuse MPS float64.

Verbatim/AST evidence (all PASS in the final suite):

| Source seam | Copy and checked allowance |
|---|---|
| c10e :181–221 my_edit | FE writer `experiments/track_c/c10x_enginepath_arms.py:458`; `experiments/track_c/c10x_enginepath_arms.py:499` compares AST after normalising only the declared key/mode check and three replacements: target zs, cur at each current layer, and undivided active residual. Identity mode restores original behavior and is refused inside recipes. CPU rho observations do not change the writer arithmetic. M3–M5 mutations fail this check. |
| engine compute_z :28–140, :151–185 | `experiments/track_c/c10x_overtone_z.py:44`; `experiments/track_c/c10x_overtone_z.py:227` compares original structure after accounting for explicit objective replacement and diagnostic observations. Imports are lazy; original stopping/clamping/KL/weight-decay structure is retained. `experiments/track_c/c10x_overtone_z.py:8` supplies the independent torch-only test seam. |
| c10e :108–117 full_seq_match | `experiments/track_c/c10x_enginepath_arms.py:367`; `experiments/track_c/c10x_enginepath_arms.py:401` removes exactly the one sink handoff and compares the remaining statement AST to the original; no extra decode/forward. The test stub also compiles the original scorer directly from source. |
| c10p :30 FRAME_SUBJECTS | Literal list AST-compared without importing the side-effectful precedent (selftest:561). |
| memit_main :304–323 getter | Unchanged getter AST compiled into the CPU stub (S:244); sampled branch raises; source bytes remain frozen. |
| benchmark :34–40 TEMPLATES | Exactly one literal assignment parsed, never executed; P1's two digests checked before A. |

Read-only seam sources: compute_z :14–21, :41–101, :104–180, :234–267; compute_ks :11–50; memit_main :100–206 and :256–323; repr_tools :135–147; c10e :25–61, :96–143, :146–221, :224–355, :358–400, :403–509. The file hashes in the appendix bind those reads.

The driver runs recipe A and its LAW#3 envelope before any candidate solve/replay/injection/write. G sees no candidate seam; G8 uses the active FE path. X checks observe actual pre-solve residuals and captures, preserve matched padded batches/order/dtype, restore W0 and hooks in finally, and retain nonzero singleton and exact-zero multi-layer-null witnesses. The 72-entry tables retain identities, native-fit/stop evidence, target hashes and replay metadata. Full-vocabulary initial/final Zorbland A1/A7 snapshots are losslessly serialized on CPU and independently audited by `experiments/track_c/c10x_enginepath_read.py:511` under the frozen keep/mix/loss predicate; no top-64 approximation or extra target-distribution gate is used.

File admission through `experiments/track_c/c10x_enginepath_read.py:1125` requires complete companion manifests, nested X/G8 evidence, all target/probe populations and flags, recorded hashes, W0/counter identities, stage/unit timing and a COMPLETE supervisor record with matching run identity. The pure classifier's small synthetic fixtures are not a CLI/file-admission bypass. Scientific input JSONs are `context_templates.json`, `targets.json`, `inertness.json`, `inject.json`, `pass1.json` and `run.json`, plus binary full-logit audit files and supervisor/proof identities. The scientific reader does not inspect telemetry.

**Telemetry volume.** Each completed scored recipe has three arms: `3×24×4 = 288` answer lines, three aggregate write_norms lines, two recipe phase markers and one A7 post-arm lens line: **294 recipe lines**. Header is once per process. Three scored recipes contribute 882 lines, 864 of them answers; with the header, 883 before stage/target/X-check telemetry. Setup adds the pristine lens; target-probability and other declared phase/check lines are additional, not silently counted as answers. The one-recipe wrapper-only fixture omits the probe/lens and counts its header instead, also totaling 294; the integrated three-recipe fixture separately verifies 864 answers, 9 write records and 3 lenses. Every line is strict JSON, flushed and fsynced.

T8's CPU stubs execute uncompared warm-up then P1/T/P2, 96 scored A7 calls per pass, 48 lens forwards only in T and same-batch layer-4…8 science reads. Deterministic, lens-sensitive and baseline-drifting stubs yield INERT, NOT-INERT and NONDETERMINISTIC-BASELINE respectively; writer methods that raise are never invoked. CPU proofs are recorded as CPU and **cannot admit a live telemetry run**.

**Executable-launch requirement.** The actual watchdog launches Python preflight, worker and bounded-audit argv starting with `sys.executable`; it executes **zero shell scripts** directly. The inventory test checks all three argv constructions, rejects shell=True, and contains `os.access(path, os.X_OK)` plus `git ls-files -s` mode `100755` assertions for any future declared direct shell launcher. No shell-mode change or commit is applicable to this launch path.


The final audit helper recomputes allowance after child startup, validates exact schema/process/run/exit/cause disposition, and kills/reaps blocked native calls. Supervisor persistence is checked after the exclusive write. A late receipt is preserved with a separate immutable `_logs/supervisor_halt.json` fence; the reader refuses that fence before and after the full-logit audit. Rows 59–63 cover the boundary and disabled-only disposition.

## Objections, review and handoff

No unresolved implementation blocker remains in the authorised model-free scope. The static approach, core implementation, reader-admission, template-pin, Amendment P and final supervisor/audit reviews were read from their actual scratch artifacts, rather than accepted from a success message.

- `design_review.md`: PROCEED for the bounded model-free approach.
- `reader_review.md`: initial FIX-FIRST on missing nested gate evidence, target/fit authenticity, frame/probe populations and timing admission. Each finding was implemented with negative controls; the final admitted-file tests require those records and reject their omission or corruption.
- `implementation_review.md`, `pinned_context_review.md`, `amendment_p_review.md`: the concrete findings were addressed. Each review binds its then-current source hashes; later changes are covered by the respective delta review, rather than treating old hashes as current.
- `final_deadline_review.md`: PROCEED on the final A/R/S hashes in the file table. The initial stale post-spawn timeout, contradictory audit dispositions and late receipt persistence findings are closed by rows 61–63 and their assertion-level RED/GREEN evidence. T11 has its own bounded child; a late immutable COMPLETE receipt is fenced by `<out>_logs/supervisor_halt.json`, checked before and after full science admission. Earlier artifacts are retained.

These are GPT-family fallback reviews with weaker independence. The design reviewer originally authored the reader, so its core ownership review excluded its own implementation; the telemetry-check author separately challenged the reader. Neither same-family review nor the program's Astra GO on the amendment text establishes authenticated out-of-family code review. **Actual out-of-family code review: NOT RUN; host Claude authentication and exact reviewer backend/effort: UNVERIFIABLE.** A scratch-only auth observation does not prove the user's host session unavailable. No review here authorizes model/GPU execution.

**Practical limits remain explicit:** no live LAW#3 envelope, LAW#5, G8, X1/X2, injection qualifier, T8 MPS inertness, target-fit outcome, eligible candidate, LEAD or scientific NULL is established by this build. Full runtime and the peak unified/device-memory requirement of prereg :120 remain UNVERIFIED. The code records peak process RSS; that is not a complete unified-memory/device peak. Those measurements must be checked by the program before treating the planning estimate as validated. The changed template rule makes every later scientific result conditional on the selected C10Q set and describes replication as fixed-template regeneration.

The build complied with R2/R9: no canonical ledger, frozen engine, prereg, config, context-save file or memory file was written. The named report is the constrained handoff. Source byte hashes and complete scope receipts provide the build boundary; concurrent unrelated program changes are recorded as unattributed. The two briefly overlapped exploratory mutation logs are explicitly excluded; the final accepted 18-mutation run is individually serial, with one restore/hash check before the next mutation.

## Exact launch commands for the program session — NOT RUN

The program must first record the reconsideration of step 6 under D-C10r-rulings-4 (3), then supply its own absolute GO records. This build creates no GO record and grants no launch approval. The launcher requires exactly `decision_id`, `experiment` = `C10X`, integer `process` = 1 or 2, `recorded_in` = `EXPERIMENT_RUNBOOK.md §5.2`, and a timezone-bearing `at`; the decision ID must name the recorded program decision. Commands below name concrete expected GO paths without manufacturing their contents.

Every command below sets LLMDB_ROOT to W explicitly. W is expanded in full in every command; it is not a shell variable. Use the applicable output only while it is absent. The T8 example names a fresh UTC directory `20261008T140000Z`; if already present, the program must choose a different fresh UTC name and propagate that absolute inertness path. These commands have **not** been executed.

1. Read-only engine fingerprint:

```sh
LLMDB_ROOT=/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a TMPDIR=/private/tmp/c10x_build /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python -B /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/engine_fingerprint.py
```

2. T8 inertness check, only under the program's separate T8 spend authorization. This check loads the live model and cannot be represented by this build's CPU proof. The first telemetry-off science attempt does not depend on running it.

```sh
/usr/bin/env -u C10X_TELEMETRY -u C10X_TELEMETRY_INERTNESS LLMDB_ROOT=/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a TMPDIR=/private/tmp/c10x_build /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python -B /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_telemetry_check.py --out /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/c10x_enginepath_telemetry_inertness/20261008T140000Z
```

3. Initial process 1 through the independent watchdog, telemetry unset as binding T9 requires:

```sh
/usr/bin/env -u C10X_TELEMETRY -u C10X_TELEMETRY_INERTNESS LLMDB_ROOT=/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a TMPDIR=/private/tmp/c10x_build /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python -B /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_arms.py --out /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/c10x_enginepath --go /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/c10x_enginepath_go_p1.json --process 1
```

4. Process-1 reader, only after the watchdog succeeds. Publication of an INVALID reader verdict has exit 0 under brief §5.4; the program must inspect the verdict and eligibility fields.

```sh
/usr/bin/env -u C10X_TELEMETRY -u C10X_TELEMETRY_INERTNESS LLMDB_ROOT=/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a TMPDIR=/private/tmp/c10x_build /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python -B /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_read.py --out /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/c10x_enginepath
```

5. Initial process 2 through the watchdog. It independently refuses model loading/writes unless process 1 has a matching, valid persisted reader and an eligible candidate; it retains telemetry off.

```sh
/usr/bin/env -u C10X_TELEMETRY -u C10X_TELEMETRY_INERTNESS LLMDB_ROOT=/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a TMPDIR=/private/tmp/c10x_build /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python -B /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_arms.py --out /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/c10x_enginepath_r2 --go /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/c10x_enginepath_go_p2.json --process 2 --process1 /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/c10x_enginepath
```

6. Combining reader after process 2 succeeds. It publishes in process 2's fresh directory and preserves the process-1 reader.

```sh
/usr/bin/env -u C10X_TELEMETRY -u C10X_TELEMETRY_INERTNESS LLMDB_ROOT=/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a TMPDIR=/private/tmp/c10x_build /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python -B /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_read.py --out /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/c10x_enginepath --process2 /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/c10x_enginepath_r2
```

**Later telemetry-on variant:** only after a live T8 INERT record with matching current sources/environment, fresh rerun names and valid earlier predecessor directories exist. It is never a variant of either initial command. The watchdog automatically executes the bounded T11 audit before allowing the science reader; do not overwrite an existing audit receipt. Any MISMATCH, DUPLICATE, MISSING, MALFORMED or UNEXPECTED cause demands a fresh telemetry-off rerun. DISABLED-only FAIL is reported, and its science can remain readable. A timeout is HALTED/incomplete. A change in telemetry setting requires regeneration of the matching replication pair under T9.

```sh
LLMDB_ROOT=/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a TMPDIR=/private/tmp/c10x_build C10X_TELEMETRY=1 C10X_TELEMETRY_INERTNESS=/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/c10x_enginepath_telemetry_inertness/20261008T140000Z/inertness.json /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python -B /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_arms.py --out /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/c10x_enginepath_rerun1 --go /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/c10x_enginepath_go_p1_rerun1.json --process 1 --predecessor /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/c10x_enginepath --cause 'later telemetry-on attempt after T8 INERT'
```

```sh
/usr/bin/env -u C10X_TELEMETRY -u C10X_TELEMETRY_INERTNESS LLMDB_ROOT=/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a TMPDIR=/private/tmp/c10x_build /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python -B /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_read.py --out /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/c10x_enginepath_rerun1
```

Only if the later process-1 reader is VALID with an eligible candidate and the earlier process-2 predecessor exists:

```sh
LLMDB_ROOT=/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a TMPDIR=/private/tmp/c10x_build C10X_TELEMETRY=1 C10X_TELEMETRY_INERTNESS=/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/c10x_enginepath_telemetry_inertness/20261008T140000Z/inertness.json /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python -B /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_arms.py --out /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/c10x_enginepath_r2_rerun1 --go /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/c10x_enginepath_go_p2_rerun1.json --process 2 --process1 /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/c10x_enginepath_rerun1 --predecessor /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/c10x_enginepath_r2 --cause 'matching later telemetry-on replication after T8 INERT'
```

```sh
/usr/bin/env -u C10X_TELEMETRY -u C10X_TELEMETRY_INERTNESS LLMDB_ROOT=/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a TMPDIR=/private/tmp/c10x_build /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python -B /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_read.py --out /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/c10x_enginepath_rerun1 --process2 /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/c10x_enginepath_r2_rerun1
```

**Expected wall clock and hard limits (prereg :108–120).** The planning subtotal is 158–217 minutes (2.6–3.6 hours), excluding unmeasured full-logit audit/hashing overhead. Three recipes contribute 78–102 minutes; 216 target solves plus replay 25–40; inertness/audits 35–50; injections 20–25. The prereg calls 3–3.5 hours plausible, unvalidated. LAW#3 failure stops after A, roughly 30 minutes, before candidate spend.

Stage caps are exactly 10 / 34 / 40 / 50 / 25 / 34 / 34 / 13 minutes for setup, A, targets, inertness/audits, injection, I-2, I-1, final. Their sum is 240 minutes; process cap is 250, pair cap 500. Setup includes preflight/import/load/snapshot; final includes serialization, the telemetry audit and supervisor persistence. Projections initially reserve the frozen caps and later use the slowest measured comparable units plus overhead, including process-1 measurements for process 2. Telemetry, restoration, hashing and diagnostics are not subtracted. Refusal or timeout HALTs and never becomes a scientific NULL. Unified-memory validation remains open until measured by the program.

## Appendix: all R5 files, before and after

The first column of hashes is the original before-state. The final column is the actual final collection. For all 187 non-prereg files these are identical. The sole differing prereg row is the explicitly program-authored append of §12 Amendment P; its post-amendment baseline and final hash are both `43a81103d68b953c2007e978b3ebecf11aadf66a7f121346047279845e8fc883`. The original first 585 lines independently retain `d6b6701ad8c5e81d317ffdb29059addbdd83d284c1b63439735f29c3e31d855d`. All 188 post-amendment-baseline hashes equal final hashes. No table entry was omitted, and `memit_dry_run/**` is listed file by file.

| R5 path | Original before SHA-256 | Final SHA-256 |
|---|---|---|
| `configs/hparams/anyedit_alphaedit_are_qwen25_3b.json` | `b7c8635b5ae876bb8a346ac2bc36d1ec438c2639021faebbdc838a046257f41e` | `b7c8635b5ae876bb8a346ac2bc36d1ec438c2639021faebbdc838a046257f41e` |
| `configs/hparams/anyedit_memit_are_qwen25_3b.json` | `c0774c602a28ece1425c83edc9f4da243b7908efdac1642a54e093fd26f16c8b` | `c0774c602a28ece1425c83edc9f4da243b7908efdac1642a54e093fd26f16c8b` |
| `configs/hparams/cfb-v4-highAKD-v0_1-draft.yaml` | `495415f88ebc0882bbe28ed8b11a3e6f2e76884fec3f2d485975093e984aae9c` | `495415f88ebc0882bbe28ed8b11a3e6f2e76884fec3f2d485975093e984aae9c` |
| `configs/hparams/cfb-v4-highAKD.yaml` | `e3ce9cb8690f70ba4d7335cf1a11679a8d79fa9563c3ef9ffca9840e9fb1e30f` | `e3ce9cb8690f70ba4d7335cf1a11679a8d79fa9563c3ef9ffca9840e9fb1e30f` |
| `configs/hparams/llama32_3b_memit_hparams.json` | `24a22192538cc9092925f78b6e93f3e3129cdc5513b1e0034c43386ead8ffb26` | `24a22192538cc9092925f78b6e93f3e3129cdc5513b1e0034c43386ead8ffb26` |
| `configs/hparams/probe-set-v4-highAKD.yaml` | `b99b5d9b8ed1d093869aed902be8464e41677d83a1c988ca3ae2150a1338d1fd` | `b99b5d9b8ed1d093869aed902be8464e41677d83a1c988ca3ae2150a1338d1fd` |
| `configs/hparams/qwen25_3b_memit_hparams.json` | `4225cc6aabc3eb9fa62d2bb2cac68b1238de3a39c5e469da635e6e1464aa3bb4` | `4225cc6aabc3eb9fa62d2bb2cac68b1238de3a39c5e469da635e6e1464aa3bb4` |
| `configs/hparams/qwen25_3b_memit_hparams_band412.json` | `7bdfae32d16f7cd8a53bc901642f6377476ebfa5c10d4d37fd69494c8cb2e618` | `7bdfae32d16f7cd8a53bc901642f6377476ebfa5c10d4d37fd69494c8cb2e618` |
| `configs/hparams/qwen25_3b_memit_hparams_band41218.json` | `191e6283056a6914c51ab0f8bf5629c72faf0bb84cff5ee25207f6b63e7705d5` | `191e6283056a6914c51ab0f8bf5629c72faf0bb84cff5ee25207f6b63e7705d5` |
| `configs/hparams/qwen25_3b_memit_hparams_band412_lowcov2500.json` | `df16866eb68327f465b0beee43b0b1b0a0c6dea5aa7a0c4f5700e864c2705f2b` | `df16866eb68327f465b0beee43b0b1b0a0c6dea5aa7a0c4f5700e864c2705f2b` |
| `configs/hparams/qwen25_3b_memit_hparams_band412_strength150.json` | `31337200e25891391427d21009829ef8d253c4fd384eedeeb5d2d9bfbd605dcd` | `31337200e25891391427d21009829ef8d253c4fd384eedeeb5d2d9bfbd605dcd` |
| `configs/hparams/qwen25_3b_memit_hparams_band812.json` | `f9a8ee42e5cd91937d3fdab852e19e971c554da3a383d6dc4c9f305a2192d546` | `f9a8ee42e5cd91937d3fdab852e19e971c554da3a383d6dc4c9f305a2192d546` |
| `configs/hparams/qwen25_3b_memit_hparams_mom2w25.json` | `afb77fe8ab5241d7a33fd183121715d1b1389de905de741ad3cef6f98a197083` | `afb77fe8ab5241d7a33fd183121715d1b1389de905de741ad3cef6f98a197083` |
| `configs/hparams/qwen25_3b_memit_hparams_mom2w50.json` | `6d171a27d1c6dbaf6240c7e715be96caff954dd9f2958dd17b8b054c5dc85272` | `6d171a27d1c6dbaf6240c7e715be96caff954dd9f2958dd17b8b054c5dc85272` |
| `configs/hparams/qwen25_3b_memit_hparams_mom2w500.json` | `797d53e19889353eb57d122e8d54f1d3d22b46142658baa1858b3e43e755f8f9` | `797d53e19889353eb57d122e8d54f1d3d22b46142658baa1858b3e43e755f8f9` |
| `configs/hparams/qwen25_3b_memit_hparams_set48.json` | `73c075619c2b9c43d870adae0d55c1e488f3a016b3e9ccc96dec71d8e7198be2` | `73c075619c2b9c43d870adae0d55c1e488f3a016b3e9ccc96dec71d8e7198be2` |
| `configs/hparams/qwen25_3b_memit_hparams_set78.json` | `93ce4befc96526da4fa2a85ce7f94c521927c83295bf850dd5ac9e84dc2ab256` | `93ce4befc96526da4fa2a85ce7f94c521927c83295bf850dd5ac9e84dc2ab256` |
| `configs/hparams/qwen25_3b_memit_hparams_smoke.json` | `bd11f757196eeebeda2c2eb597d449e1626882441036831c606ccd0f0428faac` | `bd11f757196eeebeda2c2eb597d449e1626882441036831c606ccd0f0428faac` |
| `configs/hparams/qwen25_3b_memit_hparams_steps50.json` | `f7a10f00eb1f7e37764aba0f6a231b3b0d316066f7f734f1e418a339acaeff33` | `f7a10f00eb1f7e37764aba0f6a231b3b0d316066f7f734f1e418a339acaeff33` |
| `configs/hparams/qwen25_3b_relkey_memit_hparams.json` | `343c54cd2d95c20990c56c15b90a9ac36cb45ef0c12a9a264166ff06a10d3bbf` | `343c54cd2d95c20990c56c15b90a9ac36cb45ef0c12a9a264166ff06a10d3bbf` |
| `configs/hparams/qwen25_7b_memit_hparams.json` | `81b2ccc7bddfd607ca1894efd5ef4bba9fb073f51b68024125307db65374e128` | `81b2ccc7bddfd607ca1894efd5ef4bba9fb073f51b68024125307db65374e128` |
| `configs/hparams/qwen3_06b_memit_hparams.json` | `c22468894e3e2f20ae389f59342e5163f6894fb584486d8dced719c392a76aa7` | `c22468894e3e2f20ae389f59342e5163f6894fb584486d8dced719c392a76aa7` |
| `configs/probes/b3_probes.json` | `9471d33901a042de842a99d1c84bd904ec2e6a24a2ee994630b7df34649d8a9b` | `9471d33901a042de842a99d1c84bd904ec2e6a24a2ee994630b7df34649d8a9b` |
| `configs/screens/g6_screen_qwen3b.json` | `a51813340571f6c68908ac4310cca197ebac9884939f58e5c33fb75833a3ca05` | `a51813340571f6c68908ac4310cca197ebac9884939f58e5c33fb75833a3ca05` |
| `configs/screens/g6_screen_qwen3b_v2.json` | `482c05f8f33c59d3e469566fe6f3c48eb183d3cb2fbb791f31dcad7102517c5c` | `482c05f8f33c59d3e469566fe6f3c48eb183d3cb2fbb791f31dcad7102517c5c` |
| `configs/screens/g6_screen_qwen7b.json` | `7c5a63282d8b815393e0a5dc3641dbfb61c5a0e95e530e4446f163816d75b43c` | `7c5a63282d8b815393e0a5dc3641dbfb61c5a0e95e530e4446f163816d75b43c` |
| `docs/C10X_ENGINEPATH_PREREG.md` | `d6b6701ad8c5e81d317ffdb29059addbdd83d284c1b63439735f29c3e31d855d` | `43a81103d68b953c2007e978b3ebecf11aadf66a7f121346047279845e8fc883` |
| `experiments/track_c/c10e_bandknob.py` | `1f6be5811d7e58f3ebda16867a4a174b1cf24d47f9a2514cf9c3f9d29f18e695` | `1f6be5811d7e58f3ebda16867a4a174b1cf24d47f9a2514cf9c3f9d29f18e695` |
| `experiments/track_c/c10l_covgeom_p6_zinject.py` | `b2b94563628a16c63c74733a63a95783a1f0536fc0ca6800d97b409d2f86b43b` | `b2b94563628a16c63c74733a63a95783a1f0536fc0ca6800d97b409d2f86b43b` |
| `experiments/track_c/c10l_covgeom_step0.py` | `5999d8714b7282e01f04b0292dc2c381d383f2a7ff90a2430b6e503aa7f2a557` | `5999d8714b7282e01f04b0292dc2c381d383f2a7ff90a2430b6e503aa7f2a557` |
| `experiments/track_c/c10m_diag_arms.py` | `77efc1bd358fb34728ec46616ffa983f0bf890294a61789c29989749d2252eee` | `77efc1bd358fb34728ec46616ffa983f0bf890294a61789c29989749d2252eee` |
| `experiments/track_c/c10p_twopass_arms.py` | `c34ecbe17c86d8f2803efc5520f4cf090dcb23bcc21ef0c3c28a12bfdaeb820f` | `c34ecbe17c86d8f2803efc5520f4cf090dcb23bcc21ef0c3c28a12bfdaeb820f` |
| `experiments/track_c/c10q_stacked_arms.py` | `9dec3185fd5dbcb08651023fba123b2238f761e7cb21ccb5033301054ef13731` | `9dec3185fd5dbcb08651023fba123b2238f761e7cb21ccb5033301054ef13731` |
| `memit_dry_run/memit/.gitattributes` | `0d8fc1b86a58cb959c95bc6d62652b6a06ec8a1161d0fab6af1bcabbde43b630` | `0d8fc1b86a58cb959c95bc6d62652b6a06ec8a1161d0fab6af1bcabbde43b630` |
| `memit_dry_run/memit/.gitignore` | `8d0aba79068af0ed4093807588d236cfe576a1e7c08993549f65ec2e1cbc931b` | `8d0aba79068af0ed4093807588d236cfe576a1e7c08993549f65ec2e1cbc931b` |
| `memit_dry_run/memit/CITATION.cff` | `974adb58a9fd1e6a2375244d22c8601a3a614257b006c534863ade12056a9514` | `974adb58a9fd1e6a2375244d22c8601a3a614257b006c534863ade12056a9514` |
| `memit_dry_run/memit/LICENSE` | `46c273d5a0a7f8bc3889863398e1bb20493e256f38033dfd637ec46bf654c531` | `46c273d5a0a7f8bc3889863398e1bb20493e256f38033dfd637ec46bf654c531` |
| `memit_dry_run/memit/README.md` | `e14b1c0aff11f1ebb5b427115cdd660892e0305bb868102c1330299017b69b13` | `e14b1c0aff11f1ebb5b427115cdd660892e0305bb868102c1330299017b69b13` |
| `memit_dry_run/memit/baselines/README.md` | `e44248aeb435f44301544b39c92195baa1367552978f9f20060a186c1c223e95` | `e44248aeb435f44301544b39c92195baa1367552978f9f20060a186c1c223e95` |
| `memit_dry_run/memit/baselines/ft/__init__.py` | `19646aa4d3c5b6fd8dc0032aab1cee6afc7ab24e7404c5c657cadbdd077ea0fd` | `19646aa4d3c5b6fd8dc0032aab1cee6afc7ab24e7404c5c657cadbdd077ea0fd` |
| `memit_dry_run/memit/baselines/ft/ft_hparams.py` | `fdd83bbc0cb87ebc1b6aae238a38798aab6e2b8b1723e666e797c1c5df851ab1` | `fdd83bbc0cb87ebc1b6aae238a38798aab6e2b8b1723e666e797c1c5df851ab1` |
| `memit_dry_run/memit/baselines/ft/ft_main.py` | `ce8bffb4716a6ec97c5690a10b7be585da6d009028f6d77c9ac7907caaea378a` | `ce8bffb4716a6ec97c5690a10b7be585da6d009028f6d77c9ac7907caaea378a` |
| `memit_dry_run/memit/baselines/mend/README.md` | `43f8919beb3498934f0282763523db4f1b0825d98c103bbd4230fce52e756076` | `43f8919beb3498934f0282763523db4f1b0825d98c103bbd4230fce52e756076` |
| `memit_dry_run/memit/baselines/mend/__init__.py` | `ce6f24b656aa412ba07c893dd6fa37001d0a148312c9fd5b823ac27c83e145b0` | `ce6f24b656aa412ba07c893dd6fa37001d0a148312c9fd5b823ac27c83e145b0` |
| `memit_dry_run/memit/baselines/mend/algs/enn.py` | `fcde13387249220bf8ccde0c8bf174f6444a956806f86aee0c4c1a0c062e3a90` | `fcde13387249220bf8ccde0c8bf174f6444a956806f86aee0c4c1a0c062e3a90` |
| `memit_dry_run/memit/baselines/mend/algs/ft.py` | `c60355576cac69dbca0816a4747cbb7bbba7a2352d0e7edb2191d870450eeff7` | `c60355576cac69dbca0816a4747cbb7bbba7a2352d0e7edb2191d870450eeff7` |
| `memit_dry_run/memit/baselines/mend/algs/mend.py` | `3d94e338ff9efe07815d9d4d339485e9abaa17af555f88d0adacb0a3ad19eca5` | `3d94e338ff9efe07815d9d4d339485e9abaa17af555f88d0adacb0a3ad19eca5` |
| `memit_dry_run/memit/baselines/mend/config/alg/efk.yaml` | `6d8a009b23a6d15971f0fd3f41f446e55f9f439ddd4f37f37e003a9ba39c3d4b` | `6d8a009b23a6d15971f0fd3f41f446e55f9f439ddd4f37f37e003a9ba39c3d4b` |
| `memit_dry_run/memit/baselines/mend/config/alg/enn.yaml` | `5d57b48f592317500c828b93650db753917781cacae4b72afbaf6af7bcdfff96` | `5d57b48f592317500c828b93650db753917781cacae4b72afbaf6af7bcdfff96` |
| `memit_dry_run/memit/baselines/mend/config/alg/ft.yaml` | `f2ed848825e236de2073930e6bea4faf2ca1f6c828a7f84d79fad54a0b7e607d` | `f2ed848825e236de2073930e6bea4faf2ca1f6c828a7f84d79fad54a0b7e607d` |
| `memit_dry_run/memit/baselines/mend/config/alg/mend.yaml` | `bce5e203d627552b2caf8d1a3b185ccaf28773b285a17a9f27538a86fe9eea87` | `bce5e203d627552b2caf8d1a3b185ccaf28773b285a17a9f27538a86fe9eea87` |
| `memit_dry_run/memit/baselines/mend/config/config.yaml` | `d46810afd50bf9dc19b443df22f7c77ee88ae03f7540bb7939b6eeaba4079d96` | `d46810afd50bf9dc19b443df22f7c77ee88ae03f7540bb7939b6eeaba4079d96` |
| `memit_dry_run/memit/baselines/mend/config/experiment/fc.yaml` | `678a899a35e0840de77f5fea74236c9f0d8b9ea4f0b8e1a05b981cfac131a043` | `678a899a35e0840de77f5fea74236c9f0d8b9ea4f0b8e1a05b981cfac131a043` |
| `memit_dry_run/memit/baselines/mend/config/experiment/gen.yaml` | `c208288115ae91d8cd47dfcc6c157e94d41657eebef327700363ed288f9dbee3` | `c208288115ae91d8cd47dfcc6c157e94d41657eebef327700363ed288f9dbee3` |
| `memit_dry_run/memit/baselines/mend/config/experiment/qa.yaml` | `038666cff47e927cc70891afcc2efd0f62898274d0287f1ab0719c3771394027` | `038666cff47e927cc70891afcc2efd0f62898274d0287f1ab0719c3771394027` |
| `memit_dry_run/memit/baselines/mend/config/model/bart-base.yaml` | `25eac9c87259e197ecf587413f4660098b779c6b21fa1cc6584e7d64b1479475` | `25eac9c87259e197ecf587413f4660098b779c6b21fa1cc6584e7d64b1479475` |
| `memit_dry_run/memit/baselines/mend/config/model/bert-base.yaml` | `49ff1dc40a3306dd7649f697c134e6ed0f83e5382038f18962793f3eca410e01` | `49ff1dc40a3306dd7649f697c134e6ed0f83e5382038f18962793f3eca410e01` |
| `memit_dry_run/memit/baselines/mend/config/model/distilgpt2.yaml` | `ba77ac0a70e92efac417a8f9b2aa25872f4c0152ae7e6bcb7a1a1c394e88a0d7` | `ba77ac0a70e92efac417a8f9b2aa25872f4c0152ae7e6bcb7a1a1c394e88a0d7` |
| `memit_dry_run/memit/baselines/mend/config/model/gpt2.yaml` | `6c9ac030faea26cfa57a21d10713298b5b05e2acfcda057db9ef8b7797e0182d` | `6c9ac030faea26cfa57a21d10713298b5b05e2acfcda057db9ef8b7797e0182d` |
| `memit_dry_run/memit/baselines/mend/config/model/gpt2large.yaml` | `feeab1704c76f5917876da5c631940dfde806dfdf0bf37f704ae29e8081c016c` | `feeab1704c76f5917876da5c631940dfde806dfdf0bf37f704ae29e8081c016c` |
| `memit_dry_run/memit/baselines/mend/config/model/gpt2medium.yaml` | `a943050f9ad67b30e16e312d0a63b8dff6518a582e5c49d4f36475931dee5dc6` | `a943050f9ad67b30e16e312d0a63b8dff6518a582e5c49d4f36475931dee5dc6` |
| `memit_dry_run/memit/baselines/mend/config/model/gpt2xl.yaml` | `5eb704b1c06b3636eb62db43614f87650412d08c2c6f374555187c194f031429` | `5eb704b1c06b3636eb62db43614f87650412d08c2c6f374555187c194f031429` |
| `memit_dry_run/memit/baselines/mend/config/model/gptj.yaml` | `0f3fe0caa24560fc62ffe7c2752cc23b5216bf99291d0fe969a55026982e4868` | `0f3fe0caa24560fc62ffe7c2752cc23b5216bf99291d0fe969a55026982e4868` |
| `memit_dry_run/memit/baselines/mend/config/model/gptneo27.yaml` | `809ce5da7d801f0b9c7ffc1b4b53632b23c7c8544f5dd1a401b8be4d3f17a46a` | `809ce5da7d801f0b9c7ffc1b4b53632b23c7c8544f5dd1a401b8be4d3f17a46a` |
| `memit_dry_run/memit/baselines/mend/config/model/t5large.yaml` | `109cf49c1cb32333e492e79d9974fa3e75f8c9a0459d40c872571e4eb13c85d5` | `109cf49c1cb32333e492e79d9974fa3e75f8c9a0459d40c872571e4eb13c85d5` |
| `memit_dry_run/memit/baselines/mend/config/model/t5small.yaml` | `cee5cfbb9295137f1ecf154949c55f0f76254941d9cb48ecdd66bc6decd1a929` | `cee5cfbb9295137f1ecf154949c55f0f76254941d9cb48ecdd66bc6decd1a929` |
| `memit_dry_run/memit/baselines/mend/config/model/t5xl.yaml` | `e9611b81bd40bb80c21f462b195095deabab3d3d6ac344165ba16a3ec45bc5a6` | `e9611b81bd40bb80c21f462b195095deabab3d3d6ac344165ba16a3ec45bc5a6` |
| `memit_dry_run/memit/baselines/mend/config/model/t5xxl.yaml` | `690ee1486411befec7312a0e37ed4ef615a57e1c74e4f7bea39ed6f87530d427` | `690ee1486411befec7312a0e37ed4ef615a57e1c74e4f7bea39ed6f87530d427` |
| `memit_dry_run/memit/baselines/mend/data_classes/fever.py` | `098397ce1214eb8cce6b90c8ba6ebd67024afcbc2f58ccaf887b5a365732308a` | `098397ce1214eb8cce6b90c8ba6ebd67024afcbc2f58ccaf887b5a365732308a` |
| `memit_dry_run/memit/baselines/mend/data_classes/nq.py` | `f8d8dfaadf866e82c50e4c5bfef14a9b54aa5799aca3cea8f403f0461ba61f69` | `f8d8dfaadf866e82c50e4c5bfef14a9b54aa5799aca3cea8f403f0461ba61f69` |
| `memit_dry_run/memit/baselines/mend/data_classes/wiki.py` | `60ea3f99dcb4386f38454fdda9b7a65963df76240ce516d093e396a969576627` | `60ea3f99dcb4386f38454fdda9b7a65963df76240ce516d093e396a969576627` |
| `memit_dry_run/memit/baselines/mend/data_classes/zsre.py` | `2acb707212802d65a55f46ada4381af330ff1cc9842ed9c56326de14b0711581` | `2acb707212802d65a55f46ada4381af330ff1cc9842ed9c56326de14b0711581` |
| `memit_dry_run/memit/baselines/mend/editable_model.py` | `34330a12b9864001ea46ecae794df1ea85cedb38082df783b31d67cc8939e245` | `34330a12b9864001ea46ecae794df1ea85cedb38082df783b31d67cc8939e245` |
| `memit_dry_run/memit/baselines/mend/hooks.py` | `b6037d8f9778f2d74952dafe3acc76f761df6884d85e9b5b57559cd08f7d2d6f` | `b6037d8f9778f2d74952dafe3acc76f761df6884d85e9b5b57559cd08f7d2d6f` |
| `memit_dry_run/memit/baselines/mend/losses.py` | `271a10d9e995ffd92c2de239f652928d651013f8a0889bd4205ffca1469127e8` | `271a10d9e995ffd92c2de239f652928d651013f8a0889bd4205ffca1469127e8` |
| `memit_dry_run/memit/baselines/mend/mend_hparams.py` | `071bc2c833cd1362906eee12b081c272650f909e9c93389bb05be86ae8626eb3` | `071bc2c833cd1362906eee12b081c272650f909e9c93389bb05be86ae8626eb3` |
| `memit_dry_run/memit/baselines/mend/mend_main.py` | `7e72af6f626798696f50c81ad72276f4807422bd365d5d6f130ca7e2852f53b5` | `7e72af6f626798696f50c81ad72276f4807422bd365d5d6f130ca7e2852f53b5` |
| `memit_dry_run/memit/baselines/mend/models.py` | `2e94d797f3813d57a532c676ba6609a91e89eb36bdfb8479bc092dccc5ce4420` | `2e94d797f3813d57a532c676ba6609a91e89eb36bdfb8479bc092dccc5ce4420` |
| `memit_dry_run/memit/baselines/mend/nn.py` | `ffca4fb48675c4c6cf56bb9cbbff8ce50f2c46eb8fdbfc6a7e1b6308acddab92` | `ffca4fb48675c4c6cf56bb9cbbff8ce50f2c46eb8fdbfc6a7e1b6308acddab92` |
| `memit_dry_run/memit/baselines/mend/oracle.py` | `d3657df3b292a4c78564c59b9a07ccdb8e6ff74b111cd489e38c5e5112ad4b1b` | `d3657df3b292a4c78564c59b9a07ccdb8e6ff74b111cd489e38c5e5112ad4b1b` |
| `memit_dry_run/memit/baselines/mend/requirements.txt` | `17082daf26c99220b8bfff81f282ca445e19b6ee69835f31009a4ce0d0ed20cd` | `17082daf26c99220b8bfff81f282ca445e19b6ee69835f31009a4ce0d0ed20cd` |
| `memit_dry_run/memit/baselines/mend/run.py` | `2e57976fb507bc5bc27f88ea8a7bacd7b2a75d6b45170ed4870643ae5ce74765` | `2e57976fb507bc5bc27f88ea8a7bacd7b2a75d6b45170ed4870643ae5ce74765` |
| `memit_dry_run/memit/baselines/mend/trainer.py` | `91c9d6378c0cbe6340cf4591618a68aa70f805059a01881f43c71859e001dcb1` | `91c9d6378c0cbe6340cf4591618a68aa70f805059a01881f43c71859e001dcb1` |
| `memit_dry_run/memit/baselines/mend/utils.py` | `bb981c845c07709efa4e81610ec575be7e3f3b909a42b79610a47044c04c0554` | `bb981c845c07709efa4e81610ec575be7e3f3b909a42b79610a47044c04c0554` |
| `memit_dry_run/memit/dsets/__init__.py` | `a2e1c9d7a56af0b091a48cb313a356cdb1a923e1bb046d73bd0d1e10c7b0d907` | `a2e1c9d7a56af0b091a48cb313a356cdb1a923e1bb046d73bd0d1e10c7b0d907` |
| `memit_dry_run/memit/dsets/attr_snippets.py` | `bf78972d9914919e0a0b7d7d93623b3f51b8684f691e909793b5cd5471d6f01a` | `bf78972d9914919e0a0b7d7d93623b3f51b8684f691e909793b5cd5471d6f01a` |
| `memit_dry_run/memit/dsets/counterfact.py` | `7848e935a578c40e187167a2894601b0dbf42d2334b5289a012276ea1eb672b5` | `7848e935a578c40e187167a2894601b0dbf42d2334b5289a012276ea1eb672b5` |
| `memit_dry_run/memit/dsets/knowns.py` | `e2428c36d17b0dec1f390888a98334bd0fd1f64168bffae7566ef8a8606f361e` | `e2428c36d17b0dec1f390888a98334bd0fd1f64168bffae7566ef8a8606f361e` |
| `memit_dry_run/memit/dsets/tfidf_stats.py` | `34f03d97b0b1aaad33e75a211a3d6b502cfb9eace1c172320df6ceb713d600c9` | `34f03d97b0b1aaad33e75a211a3d6b502cfb9eace1c172320df6ceb713d600c9` |
| `memit_dry_run/memit/dsets/zsre.py` | `a6281375afd9983337c154095fe9aba59c74c36fa34ecfb12838c7b5c341670e` | `a6281375afd9983337c154095fe9aba59c74c36fa34ecfb12838c7b5c341670e` |
| `memit_dry_run/memit/experiments/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `memit_dry_run/memit/experiments/causal_trace.py` | `9436fd596a39e240a01121da601359bea5d0b3a350c0faa34aa8b0ccac05560b` | `9436fd596a39e240a01121da601359bea5d0b3a350c0faa34aa8b0ccac05560b` |
| `memit_dry_run/memit/experiments/evaluate.py` | `4ef8e138bb8003c8486935ad0eae86d9ccd84bb61cfa1f88b63f0ed06c2d1760` | `4ef8e138bb8003c8486935ad0eae86d9ccd84bb61cfa1f88b63f0ed06c2d1760` |
| `memit_dry_run/memit/experiments/py/demo.py` | `268c16a1c2c4e8642b7641739c2cd0808c08be80f36f280d1e5bef4944733772` | `268c16a1c2c4e8642b7641739c2cd0808c08be80f36f280d1e5bef4944733772` |
| `memit_dry_run/memit/experiments/py/eval_utils_counterfact.py` | `b00d9810305580dddfeb5e65129db4d56bcbfee1edf020605e21bf4f5033aeb7` | `b00d9810305580dddfeb5e65129db4d56bcbfee1edf020605e21bf4f5033aeb7` |
| `memit_dry_run/memit/experiments/py/eval_utils_zsre.py` | `e4f18c84a813d0a2fb9a5c9426726844117fe365cae72107d51f304a264d77a8` | `e4f18c84a813d0a2fb9a5c9426726844117fe365cae72107d51f304a264d77a8` |
| `memit_dry_run/memit/experiments/summarize.py` | `7de8f5eec86243807825cf9f62923535f853cce07d2d3248534f86320f229372` | `7de8f5eec86243807825cf9f62923535f853cce07d2d3248534f86320f229372` |
| `memit_dry_run/memit/experiments/sweep.py` | `bfc7a91e9abb526814f7d975a81ff0333e930b452e2da58b31dc2ae8a10cce74` | `bfc7a91e9abb526814f7d975a81ff0333e930b452e2da58b31dc2ae8a10cce74` |
| `memit_dry_run/memit/globals.yml` | `86ab5194b3cddc19c14173a3b8f13563c554d252666eb563a4ac2f919e087459` | `86ab5194b3cddc19c14173a3b8f13563c554d252666eb563a4ac2f919e087459` |
| `memit_dry_run/memit/globals.yml.upstream_default.20260430T035736Z` | `f05226b5d0b64a25106fbfa2da3b4de3b69d8e6797c7757f8a6679756820845c` | `f05226b5d0b64a25106fbfa2da3b4de3b69d8e6797c7757f8a6679756820845c` |
| `memit_dry_run/memit/hparams/FT/EleutherAI_gpt-j-6B_constr.json` | `018e27089431ed3632aa0b8f2f1b4aa51daa81ba39f24952a400a92df84fa28b` | `018e27089431ed3632aa0b8f2f1b4aa51daa81ba39f24952a400a92df84fa28b` |
| `memit_dry_run/memit/hparams/FT/EleutherAI_gpt-j-6B_unconstr.json` | `1d605b748ed9709efb19d3f04c82de2d1ff12c81144c1d6621e72408f838d098` | `1d605b748ed9709efb19d3f04c82de2d1ff12c81144c1d6621e72408f838d098` |
| `memit_dry_run/memit/hparams/FT/EleutherAI_gpt-j-6B_wd.json` | `5161e47c66580d13524abc1bbbb42b146163ff2f51121a4c74f23679bbad8254` | `5161e47c66580d13524abc1bbbb42b146163ff2f51121a4c74f23679bbad8254` |
| `memit_dry_run/memit/hparams/FT/gpt2-large_constr.json` | `48298eec3688c393dcf610e114b30a521fa3d8b5fc7fb5d5e938f61996f93d19` | `48298eec3688c393dcf610e114b30a521fa3d8b5fc7fb5d5e938f61996f93d19` |
| `memit_dry_run/memit/hparams/FT/gpt2-medium_constr.json` | `fd1b7a80dff0e6d1c8e32c38b0ab620505ed1668d366d292a5776a49d2d7e23d` | `fd1b7a80dff0e6d1c8e32c38b0ab620505ed1668d366d292a5776a49d2d7e23d` |
| `memit_dry_run/memit/hparams/FT/gpt2-xl_attn.json` | `28348947fe372113c6fc9d0a1b851121dbf8e198311ae7d573b4b6f8173a477b` | `28348947fe372113c6fc9d0a1b851121dbf8e198311ae7d573b4b6f8173a477b` |
| `memit_dry_run/memit/hparams/FT/gpt2-xl_constr.json` | `6f1a26e915b2fc5a203443322aa224f4dd47150117f1cc5d1ee7f8026108047f` | `6f1a26e915b2fc5a203443322aa224f4dd47150117f1cc5d1ee7f8026108047f` |
| `memit_dry_run/memit/hparams/FT/gpt2-xl_unconstr.json` | `484393773f7a18844dd7c7f212673e4a8113515f0dfcc29c9d02c494f13bb137` | `484393773f7a18844dd7c7f212673e4a8113515f0dfcc29c9d02c494f13bb137` |
| `memit_dry_run/memit/hparams/MEMIT/EleutherAI_gpt-j-6B.json` | `ac1c641470c003032f15cf3f3db088e215f289535b7ea8c171ccb1235cd7bf43` | `ac1c641470c003032f15cf3f3db088e215f289535b7ea8c171ccb1235cd7bf43` |
| `memit_dry_run/memit/hparams/MEMIT/Llama-3.1-8B.json` | `bea608d313845440ebe5a3887034b271bca431dff10a6d09a8237c3256f894f2` | `bea608d313845440ebe5a3887034b271bca431dff10a6d09a8237c3256f894f2` |
| `memit_dry_run/memit/hparams/MEMIT/gpt2-xl.json` | `2c2ff7e8f3ff8b33cca2966a628f92f8b56bba72af51ca9af57d6c30a1c342d4` | `2c2ff7e8f3ff8b33cca2966a628f92f8b56bba72af51ca9af57d6c30a1c342d4` |
| `memit_dry_run/memit/hparams/MEMIT/meta-llama_Llama-3.1-8B.json` | `61007b61dd2119cbd281ba10d89fb3d34bdcfe03cfce4da542a0729e261caf12` | `61007b61dd2119cbd281ba10d89fb3d34bdcfe03cfce4da542a0729e261caf12` |
| `memit_dry_run/memit/hparams/MEND/EleutherAI_gpt-j-6B.json` | `d1e7bbd8a8486cda08af026c7cfdcc12b3a4fac3fab738a528e11adb8e52d97b` | `d1e7bbd8a8486cda08af026c7cfdcc12b3a4fac3fab738a528e11adb8e52d97b` |
| `memit_dry_run/memit/hparams/MEND/EleutherAI_gpt-j-6B_CF.json` | `b30a5f403fa4972201d1ca994c70b3c6dbd396d7163bd502bc1cbe571e87d44c` | `b30a5f403fa4972201d1ca994c70b3c6dbd396d7163bd502bc1cbe571e87d44c` |
| `memit_dry_run/memit/hparams/MEND/gpt2-xl.json` | `fe1a786ca540a3dee435621a56659d070b52b0354f85d08f9c0874f2e3d8fb79` | `fe1a786ca540a3dee435621a56659d070b52b0354f85d08f9c0874f2e3d8fb79` |
| `memit_dry_run/memit/hparams/MEND/gpt2-xl_CF.json` | `5691b370fc2b8540d2c28d608d53e2328005ce5b933ab9e04726bde7cf93f44e` | `5691b370fc2b8540d2c28d608d53e2328005ce5b933ab9e04726bde7cf93f44e` |
| `memit_dry_run/memit/hparams/MEND/gpt2-xl_zsRE.json` | `f6b0cc610281f474f702075064fe5eef83e0e7925d7f7d51036ee1fbc03a999a` | `f6b0cc610281f474f702075064fe5eef83e0e7925d7f7d51036ee1fbc03a999a` |
| `memit_dry_run/memit/hparams/ROME/EleutherAI_gpt-j-6B.json` | `85e44438c5a6bcd7769d73efadd10507f2b7ec7eeaa0330a310e351d2676fdff` | `85e44438c5a6bcd7769d73efadd10507f2b7ec7eeaa0330a310e351d2676fdff` |
| `memit_dry_run/memit/hparams/ROME/EleutherAI_gpt-neox-20b.json` | `fadf233859d46cf02ef219f74bced47652d277cd392de51c7c1ce6585d1d60b9` | `fadf233859d46cf02ef219f74bced47652d277cd392de51c7c1ce6585d1d60b9` |
| `memit_dry_run/memit/hparams/ROME/gpt2-large.json` | `2c5cb903948c6e261d2bb9aa2e9dfbd20ac30d38a2669054a25defcaed4a13ed` | `2c5cb903948c6e261d2bb9aa2e9dfbd20ac30d38a2669054a25defcaed4a13ed` |
| `memit_dry_run/memit/hparams/ROME/gpt2-medium.json` | `3a6b72ddf9e0b859e6909a1e144c5bb6958852a0e4fef36db0e4424c424c1913` | `3a6b72ddf9e0b859e6909a1e144c5bb6958852a0e4fef36db0e4424c424c1913` |
| `memit_dry_run/memit/hparams/ROME/gpt2-xl.json` | `81a98b788b8fbb89718288a8831441200e7d824fd057f62cb7d913ae4da5cf42` | `81a98b788b8fbb89718288a8831441200e7d824fd057f62cb7d913ae4da5cf42` |
| `memit_dry_run/memit/memit/__init__.py` | `911cc037562a368ca7017ea66f4821c5a848f286a55b7d624c242209afcd01df` | `911cc037562a368ca7017ea66f4821c5a848f286a55b7d624c242209afcd01df` |
| `memit_dry_run/memit/memit/__pycache__/__init__.cpython-311.pyc` | `29e09585ec894fc0109aa73db6f1de88df5087ac3e70069f069c7dba782a4287` | `29e09585ec894fc0109aa73db6f1de88df5087ac3e70069f069c7dba782a4287` |
| `memit_dry_run/memit/memit/__pycache__/compute_ks.cpython-311.pyc` | `9acefffad173c67f9d03a1c0705145f2ee6b5aef1679f0fbd7cd0c49495d544e` | `9acefffad173c67f9d03a1c0705145f2ee6b5aef1679f0fbd7cd0c49495d544e` |
| `memit_dry_run/memit/memit/__pycache__/compute_z.cpython-311.pyc` | `f3c78b5d8be2df307cc3bde53fc02a878469fc8f5c3473bf3a415b0dca3bd156` | `f3c78b5d8be2df307cc3bde53fc02a878469fc8f5c3473bf3a415b0dca3bd156` |
| `memit_dry_run/memit/memit/__pycache__/memit_hparams.cpython-311.pyc` | `d869204c04046a2ba2bc9e519fb324757b2bdad306d9365a6ce861ad687760f6` | `d869204c04046a2ba2bc9e519fb324757b2bdad306d9365a6ce861ad687760f6` |
| `memit_dry_run/memit/memit/__pycache__/memit_main.cpython-311.pyc` | `4432d0eb89db771924edde06dd958544f8f598c74297aa38e5250f713e12aeff` | `4432d0eb89db771924edde06dd958544f8f598c74297aa38e5250f713e12aeff` |
| `memit_dry_run/memit/memit/compute_ks.py` | `0b039be47c548f046b71cad4efce63414f53edbaa657bde868a20cdd35a2f5c7` | `0b039be47c548f046b71cad4efce63414f53edbaa657bde868a20cdd35a2f5c7` |
| `memit_dry_run/memit/memit/compute_z.py` | `d94af7fa14e5a4a20d5fa6361e0cbb30da0ff957db31922557ff809c34205dea` | `d94af7fa14e5a4a20d5fa6361e0cbb30da0ff957db31922557ff809c34205dea` |
| `memit_dry_run/memit/memit/memit_hparams.py` | `1b229b882b031ddbb59f06ad6ba58d5c33b17826bbfddf80f767e96931b595b2` | `1b229b882b031ddbb59f06ad6ba58d5c33b17826bbfddf80f767e96931b595b2` |
| `memit_dry_run/memit/memit/memit_main.py` | `d941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65` | `d941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65` |
| `memit_dry_run/memit/memit/memit_main.py.pre_p7_backup` | `4b5c6478da463bb174036a3a0495d7786f8e4d207ee7021a7e9afb6aef977168` | `4b5c6478da463bb174036a3a0495d7786f8e4d207ee7021a7e9afb6aef977168` |
| `memit_dry_run/memit/notebooks/average_causal_effects.ipynb` | `35598748d8ce10af976c8f2be331fdf5eb6081dcd1d564f4ec753258c0c2cafb` | `35598748d8ce10af976c8f2be331fdf5eb6081dcd1d564f4ec753258c0c2cafb` |
| `memit_dry_run/memit/notebooks/causal_trace.ipynb` | `755a31d3d4a34b56e253e21b4171f944e31a4e57fa8a9c38440f6e6731ab2711` | `755a31d3d4a34b56e253e21b4171f944e31a4e57fa8a9c38440f6e6731ab2711` |
| `memit_dry_run/memit/notebooks/causal_trace_frozen_mlp_attn.ipynb` | `0b3837b24d70939e44b2fbba5757f4f19e888bf858445714c0bcb574170d4fe0` | `0b3837b24d70939e44b2fbba5757f4f19e888bf858445714c0bcb574170d4fe0` |
| `memit_dry_run/memit/notebooks/globals.yml` | `86ab5194b3cddc19c14173a3b8f13563c554d252666eb563a4ac2f919e087459` | `86ab5194b3cddc19c14173a3b8f13563c554d252666eb563a4ac2f919e087459` |
| `memit_dry_run/memit/notebooks/memit.ipynb` | `dc79c89862a9ef57dd6cdf46715c716ef60103f97314b1f9fb5fff3be88f7235` | `dc79c89862a9ef57dd6cdf46715c716ef60103f97314b1f9fb5fff3be88f7235` |
| `memit_dry_run/memit/notebooks/vis/globals.yml` | `86ab5194b3cddc19c14173a3b8f13563c554d252666eb563a4ac2f919e087459` | `86ab5194b3cddc19c14173a3b8f13563c554d252666eb563a4ac2f919e087459` |
| `memit_dry_run/memit/notebooks/vis/table_population.ipynb` | `a5b6eb40955acbf7b37068ea782b04cfcb56794c6738b4eefbc3f38daff03ced` | `a5b6eb40955acbf7b37068ea782b04cfcb56794c6738b4eefbc3f38daff03ced` |
| `memit_dry_run/memit/notebooks/vis/table_population_zsre.ipynb` | `c34799ceafdcad5220b5d871989cda93de581419741c861c38bd62f63d0cac85` | `c34799ceafdcad5220b5d871989cda93de581419741c861c38bd62f63d0cac85` |
| `memit_dry_run/memit/notebooks/vis/visualize_multi_results.ipynb` | `05d42e5d00021f4a435c23ffc88dcc919597c744136be2607f86e1a94d71304e` | `05d42e5d00021f4a435c23ffc88dcc919597c744136be2607f86e1a94d71304e` |
| `memit_dry_run/memit/notebooks/vis/visualize_sweep_results.ipynb` | `58ae1129dd40e1f6620e77ae24f1f74417ed3e1c2487ebcec552025c6313f008` | `58ae1129dd40e1f6620e77ae24f1f74417ed3e1c2487ebcec552025c6313f008` |
| `memit_dry_run/memit/rome/README.md` | `4711e2605517fe1308cccd59748761e19342b4c0b0b26d2a9a32bbf3a93f94a6` | `4711e2605517fe1308cccd59748761e19342b4c0b0b26d2a9a32bbf3a93f94a6` |
| `memit_dry_run/memit/rome/__init__.py` | `87e6bd462753e8a86b84b2461da6067762cb0d5c9b7061b1b0598adb6f550a7a` | `87e6bd462753e8a86b84b2461da6067762cb0d5c9b7061b1b0598adb6f550a7a` |
| `memit_dry_run/memit/rome/__pycache__/__init__.cpython-311.pyc` | `174f5c000e030c096a7b21ec71e06661f3f348de8f2e3ad608fae32c8b8b5fe5` | `174f5c000e030c096a7b21ec71e06661f3f348de8f2e3ad608fae32c8b8b5fe5` |
| `memit_dry_run/memit/rome/__pycache__/compute_u.cpython-311.pyc` | `e70218d4d08afdabbc8d1ae688ec4024b13175bbf2d822f1f79fb7087b063035` | `e70218d4d08afdabbc8d1ae688ec4024b13175bbf2d822f1f79fb7087b063035` |
| `memit_dry_run/memit/rome/__pycache__/compute_v.cpython-311.pyc` | `b0da9115e983294a3b570dee6ebec70f40de5b41aa0205420857b5a8b55f90ef` | `b0da9115e983294a3b570dee6ebec70f40de5b41aa0205420857b5a8b55f90ef` |
| `memit_dry_run/memit/rome/__pycache__/layer_stats.cpython-311.pyc` | `440de9a4e69c8f72a3a6c32cdf88808d9ba2b3b5fb433c702d68b08af2e93e6c` | `440de9a4e69c8f72a3a6c32cdf88808d9ba2b3b5fb433c702d68b08af2e93e6c` |
| `memit_dry_run/memit/rome/__pycache__/repr_tools.cpython-311.pyc` | `7bc5434b08f4c6af21441c85d4715e5af2239dce3233f3f1aa7ca363068fd972` | `7bc5434b08f4c6af21441c85d4715e5af2239dce3233f3f1aa7ca363068fd972` |
| `memit_dry_run/memit/rome/__pycache__/rome_hparams.cpython-311.pyc` | `7f48846aa72e1a408396ba4d7f5f2c7d6f1e77ae3d96a936b47347c232e22148` | `7f48846aa72e1a408396ba4d7f5f2c7d6f1e77ae3d96a936b47347c232e22148` |
| `memit_dry_run/memit/rome/__pycache__/rome_main.cpython-311.pyc` | `68472f450355954b30697accbc0bd931633dc4335eea51ef5632347ab1d04e81` | `68472f450355954b30697accbc0bd931633dc4335eea51ef5632347ab1d04e81` |
| `memit_dry_run/memit/rome/__pycache__/tok_dataset.cpython-311.pyc` | `0131138a2f4c2e647c345a854f9aa4cd11b882b09ab9f9a92dadaca667e37a32` | `0131138a2f4c2e647c345a854f9aa4cd11b882b09ab9f9a92dadaca667e37a32` |
| `memit_dry_run/memit/rome/compute_u.py` | `06a73593171eecdd03ab90d45daa2c6096b4335847f0c73bda9d834cdfb1d72d` | `06a73593171eecdd03ab90d45daa2c6096b4335847f0c73bda9d834cdfb1d72d` |
| `memit_dry_run/memit/rome/compute_v.py` | `07f35ecec4b2a20a33318d75b040ae6c1fc5fd2122a90c92e32e361ef730d9eb` | `07f35ecec4b2a20a33318d75b040ae6c1fc5fd2122a90c92e32e361ef730d9eb` |
| `memit_dry_run/memit/rome/layer_stats.py` | `43693c64b061f3cdaa087447e47ddc10fb26fd597dd405eb0644d71ede2fe2d5` | `43693c64b061f3cdaa087447e47ddc10fb26fd597dd405eb0644d71ede2fe2d5` |
| `memit_dry_run/memit/rome/repr_tools.py` | `d4c2324ba20cbcce7f4ccfcf58ad002912edf0ad2fc72ab4e9bf46cc9dfed336` | `d4c2324ba20cbcce7f4ccfcf58ad002912edf0ad2fc72ab4e9bf46cc9dfed336` |
| `memit_dry_run/memit/rome/rome_hparams.py` | `1037cd56d2cfc92db212f5f4344477c5732a809dfd745c04e8e5742e925c98a5` | `1037cd56d2cfc92db212f5f4344477c5732a809dfd745c04e8e5742e925c98a5` |
| `memit_dry_run/memit/rome/rome_main.py` | `44ff978bd0d68839ff2f94f475a71fdac19a53a4ef263c1d74693ebfd5b40ba5` | `44ff978bd0d68839ff2f94f475a71fdac19a53a4ef263c1d74693ebfd5b40ba5` |
| `memit_dry_run/memit/rome/tok_dataset.py` | `37f775943d5040702ae21252db579f6aa116dacc4dd93c227c44cf9b3481a1a0` | `37f775943d5040702ae21252db579f6aa116dacc4dd93c227c44cf9b3481a1a0` |
| `memit_dry_run/memit/scaling_curves.sh` | `4c89f3d257f67b3e9a1ae40fe81192bfc48c0a2f40b7f2dba9adc4f2bd97efa4` | `4c89f3d257f67b3e9a1ae40fe81192bfc48c0a2f40b7f2dba9adc4f2bd97efa4` |
| `memit_dry_run/memit/scripts/causal_trace.sh` | `87bdd627bb58c82bf0f67841705bb95317d49f59eb1beab9d405126fd4d54600` | `87bdd627bb58c82bf0f67841705bb95317d49f59eb1beab9d405126fd4d54600` |
| `memit_dry_run/memit/scripts/colab_reqs/additional.txt` | `3d49f4e0bb2b079bb2fec81b178bb0a27ebc4f8085c496727e299f16aa852fb2` | `3d49f4e0bb2b079bb2fec81b178bb0a27ebc4f8085c496727e299f16aa852fb2` |
| `memit_dry_run/memit/scripts/colab_reqs/rome.txt` | `de3f292db754a685905c34d079d097b95e3e7de102af06aedbfba42940d29564` | `de3f292db754a685905c34d079d097b95e3e7de102af06aedbfba42940d29564` |
| `memit_dry_run/memit/scripts/collect_layer_stats.sh` | `ca9be52a8845851b9b17d8b92b0ac3d7333b3ea7bac339db4c1daa0deda7c60a` | `ca9be52a8845851b9b17d8b92b0ac3d7333b3ea7bac339db4c1daa0deda7c60a` |
| `memit_dry_run/memit/scripts/ipynb_drop_output.py` | `62a17e64c2de0448962fda6e0914a80e354361fea73b4363fc5287b92e4ca635` | `62a17e64c2de0448962fda6e0914a80e354361fea73b4363fc5287b92e4ca635` |
| `memit_dry_run/memit/scripts/memit.yml` | `28d8b635eed02cdb8d1fb36d8990a5347c1b88dfffcea71105febc8a91d98f83` | `28d8b635eed02cdb8d1fb36d8990a5347c1b88dfffcea71105febc8a91d98f83` |
| `memit_dry_run/memit/scripts/setup_clean_ipynb.sh` | `55533d28e032731eb1f0c91154ecf14092c23cf4d1f11be90a8304aa58e3338d` | `55533d28e032731eb1f0c91154ecf14092c23cf4d1f11be90a8304aa58e3338d` |
| `memit_dry_run/memit/scripts/setup_conda.sh` | `3d78078734cb1a45b0b448dafd5cc09b92496b89bcc8aabae057ee1fdb17e2f3` | `3d78078734cb1a45b0b448dafd5cc09b92496b89bcc8aabae057ee1fdb17e2f3` |
| `memit_dry_run/memit/util/__init__.py` | `0f2267e08c0c9345017c155e4d894043773f4e303958a95a3e8fe5dc3c5b341d` | `0f2267e08c0c9345017c155e4d894043773f4e303958a95a3e8fe5dc3c5b341d` |
| `memit_dry_run/memit/util/__pycache__/__init__.cpython-311.pyc` | `db80aa1f656186a86bae309617717d6958528f2d358abe0f656acf2c769704c2` | `db80aa1f656186a86bae309617717d6958528f2d358abe0f656acf2c769704c2` |
| `memit_dry_run/memit/util/__pycache__/device.cpython-311.pyc` | `b2cd7e432ddf59d90620450e3737a71784530a9f690bdca3d7156f116d603757` | `b2cd7e432ddf59d90620450e3737a71784530a9f690bdca3d7156f116d603757` |
| `memit_dry_run/memit/util/__pycache__/generate.cpython-311.pyc` | `fa2a8446bf235e811752c2db8c04050864747ce541485c9a52ab9d3dae043b50` | `fa2a8446bf235e811752c2db8c04050864747ce541485c9a52ab9d3dae043b50` |
| `memit_dry_run/memit/util/__pycache__/globals.cpython-311.pyc` | `ce42162a322e75796375c0b0ab3bb732d882cb3127e85ab0dac890588b5de55a` | `ce42162a322e75796375c0b0ab3bb732d882cb3127e85ab0dac890588b5de55a` |
| `memit_dry_run/memit/util/__pycache__/hparams.cpython-311.pyc` | `635c8abe561839a3fa9b91f7728d52899f7577c3a614a2a5b79a0736d6c41c73` | `635c8abe561839a3fa9b91f7728d52899f7577c3a614a2a5b79a0736d6c41c73` |
| `memit_dry_run/memit/util/__pycache__/logit_lens.cpython-311.pyc` | `038eea0405aab634ef32849c1c3312333297fbad3d9e25ce7d8b4960aaa0938b` | `038eea0405aab634ef32849c1c3312333297fbad3d9e25ce7d8b4960aaa0938b` |
| `memit_dry_run/memit/util/__pycache__/nethook.cpython-311.pyc` | `58527b861ba2cdb71ecd7de3380eea7e28f4c7dcbe5938a65ee7e5a00bc20c39` | `58527b861ba2cdb71ecd7de3380eea7e28f4c7dcbe5938a65ee7e5a00bc20c39` |
| `memit_dry_run/memit/util/__pycache__/runningstats.cpython-311.pyc` | `652d9894a24dbfb428ffd3de41e21b98d50d318a8581a970b100b6c81de54a0b` | `652d9894a24dbfb428ffd3de41e21b98d50d318a8581a970b100b6c81de54a0b` |
| `memit_dry_run/memit/util/device.py` | `868627783827f03763ba9c210de2ddbd607e050330eccf7757fccfd9e985cf2b` | `868627783827f03763ba9c210de2ddbd607e050330eccf7757fccfd9e985cf2b` |
| `memit_dry_run/memit/util/generate.py` | `3764cb8a0a1b3f28c17d8aab3028b33d2127ba4e02e8dbc253025791a9ab2514` | `3764cb8a0a1b3f28c17d8aab3028b33d2127ba4e02e8dbc253025791a9ab2514` |
| `memit_dry_run/memit/util/globals.py` | `ae25580435585acafce49511abbba6b545dbfb3f5865147d79bd383a050bf8c2` | `ae25580435585acafce49511abbba6b545dbfb3f5865147d79bd383a050bf8c2` |
| `memit_dry_run/memit/util/hparams.py` | `09e9fec3f476ff68009230f1251044bec21aa71797d484033f736057bbe294b0` | `09e9fec3f476ff68009230f1251044bec21aa71797d484033f736057bbe294b0` |
| `memit_dry_run/memit/util/logit_lens.py` | `0c35d203c511327e5c839ea0c06408f23dd6969402dce4be02f4e3160c88e6a4` | `0c35d203c511327e5c839ea0c06408f23dd6969402dce4be02f4e3160c88e6a4` |
| `memit_dry_run/memit/util/nethook.py` | `20e84c9413518af3aee76762071f823cbe5d75c4658e4ffa7bdab045df735f7c` | `20e84c9413518af3aee76762071f823cbe5d75c4658e4ffa7bdab045df735f7c` |
| `memit_dry_run/memit/util/perplexity.py` | `e0dc2678eb331aba94d70bddad30ce983b3a062c35d180d1f524835f2966161e` | `e0dc2678eb331aba94d70bddad30ce983b3a062c35d180d1f524835f2966161e` |
| `memit_dry_run/memit/util/runningstats.py` | `7b3a05de007733ec3243c13362d3c24b6cb9c09f32eedbcf36de02c98a49ac97` | `7b3a05de007733ec3243c13362d3c24b6cb9c09f32eedbcf36de02c98a49ac97` |
| `memit_dry_run/memit/zsre_evals.sh` | `a5f8ca93642cab1e18bdfc917255ea64323b2c3261d0cb4634e235bbbbf00d2f` | `a5f8ca93642cab1e18bdfc917255ea64323b2c3261d0cb4634e235bbbbf00d2f` |
| `tools/engine_fingerprint.py` | `450ee83ac829817299ead301c4a3d20702f431deaea4be58c77ecfd89a329162` | `450ee83ac829817299ead301c4a3d20702f431deaea4be58c77ecfd89a329162` |

Complete original, amended and final hash JSONs, full `(path,size,mtime_ns)` listings and unfiltered deltas are preserved in the scratch directories cited above. After report publication, `/private/tmp/c10x_build/after_report/` rechecks scope; `/private/tmp/c10x_build/report_receipt.json` records the final report digest and final source identities outside the report itself.

## Review fixes

**DONE — 72 model-free CPU tests PASS (17.559s), zero failures/errors.** The blocking Amendment M report-only defect and advisory disable-cutoff defect are repaired. This section also closes the program's forward-mask audit and subsequent device/dtype conversion correction. The original report's 159,745-byte prefix is preserved byte for byte; its SHA-256 is `e1f506d26a345f2c687a3502dd8bad39eb4718944a8a9a5fe6e665aca34efabc`. Its 63-test and 18-mutant results remain historical evidence for the original source identity. The 18 mutants were not rerun against the revised sources; the full 72-test result below is current.

Input review: `results/c10x_build_astra_review.md:1`, read in full, SHA-256 `1ce2c9cd623057b3308d9e8f9eb2b09e5612ff328029b72e5579ff0d29c65454`. Its requested Astra backend/effort remains UNVERIFIABLE, as the review itself states. The program's later correction supersedes the attention-mask hypothesis: **the mask hypothesis was REFUTED**. The program reports a machine-verified torch 2.8/MPS defect for nonzero-storage-offset views during a combined CPU transfer and dtype conversion. This build did not run an MPS probe and does not independently establish that runtime finding.

### Amendment M: fp32 diagnostics cannot veto science

`experiments/track_c/c10x_enginepath_inertness.py:14` encodes report-only infinities/NaNs as `{"nonfinite":"inf"}`, `{"nonfinite":"-inf"}`, or `{"nonfinite":"nan"}`. Finite numbers remain numbers. Captured update diagnostics use that encoding at `c10x_enginepath_inertness.py:133`; the captured matrix itself is still returned by identity. CPU float64 finiteness, norm, parity, floor and tolerance checks are unchanged and strict. The existing CPU-before-cast helper is `c10x_enginepath_inertness.py:33`.

The driver normalizes only report copies at `c10x_enginepath_arms.py:609` (dispatch), `:641` (recipe boundary), and `:1114` (fp32 size-ratio diagnostic). Telemetry's report-only harness norms are encoded inside its Exception boundary at `:313`. The float64 size ratio remains the scientific ratio; a nonfinite fp32 ratio is tagged and its diagnostic “opposite” boolean is false.

The reader admits those exact tags only in fp32 diagnostic fields: `c10x_enginepath_read.py:210` (legacy recipe norms), `:598` (fp32 value validator), `:608` (parity report), `:628` (attributed capture), and `:981` (file evidence/size diagnostics). The existing `NONFINITE` report string remains supported for older diagnostic representations. Ordinary JSON nonfinite numbers and malformed tags still fail strict record/schema validation. No tagged value is used to choose acceptance, eligibility, qualifiers or a verdict; scientific float64 values still go through the unchanged numeric validators.

Tests 64–66 use actual finite fp32 tensors filled with `3e37` whose fp32 norm overflows to infinity, and a nearby tensor whose fp32 relative reduction is NaN. They prove update-object identity, finite float64 comparisons, strict JSON round trips, unchanged reader labels/qualifiers/eligibility, and unchanged complete-file admission after substituting inf/NaN tags throughout the diagnostic fields. Companion records and saved CPU tensors are audited through the actual file reader. Nonfinite float64 norms/ratios, nonfinite gate relative distances, and over-tolerance float64 values still refuse admission.

### T11: disable excuses only subsequent omissions

`c10x_enginepath_arms.py:296` retains the original single `C10X_TELEMETRY_DISABLED <ExcType>: <msg>` prefix and appends `C10X_ANSWER_CUTOFF` plus JSON containing `answer_cutoff`, `process` and `run_id`. The cutoff is the number of answer attempts preceding the failed answer; an initialization failure has cutoff zero. `answer()` records the pre-attempt cutoff at `:325`. Public telemetry methods still catch Exception, disable later calls, and never catch BaseException.

`c10x_enginepath_telemetry_check.py:250` requires every expected answer before that cutoff. Earlier omissions produce MISSING and require a rerun; omissions from the failed answer onward may receive the DISABLED-only disposition. Expected answer order follows the actual A → I-2 → I-1 recipe order, fixed arm order, recorded rows and canonical/held-out template order (`:357`), regardless of JSON object-member order. `audit()` at `:407` requires one well-formed marker with the matching process/run identity and a strict integer cutoff in range. Legacy markers without a cutoff, booleans, malformed/duplicate markers and wrong identities cannot excuse missing answers. Duplicate/unexpected/mismatched/malformed answer lines retain their rerun dispositions.

Tests 67–69 cover an earlier omission with cutoff 2, later-only omissions, initialization failure, invalid ordinal, wrong identity, legacy marker, exactly one disable marker, the failed-answer cutoff and fixed recipe order. The scientific reader still never reads telemetry.

### Forward-mask audit retained after the refutation

The following C10X call sites now pass an explicit mask:

| Current call site | Mask supplied |
|---|---|
| `c10x_enginepath_arms.py:365` — logit lens | Original tokenizer mask through `forward_tokens()` at `:351`. |
| `c10x_enginepath_arms.py:387` — observed scorer | `torch.ones_like(cur)` for each unpadded single sequence. |
| `c10x_enginepath_arms.py:404` — reference/calibration scorer | `torch.ones_like(cur)` for each unpadded single sequence. |
| `c10x_enginepath_arms.py:743` — padded canonical replay | Original padded tokenizer mask through `forward_tokens()`. |
| `c10x_enginepath_arms.py:1044` — pristine/frame/relation top-1 probes | Original tokenizer mask through `forward_tokens()`. |
| `c10x_enginepath_arms.py:1086` — teacher-forced probe curve | `torch.ones_like(cur)`. |
| `c10x_overtone_z.py:145` — OverTone solve | Explicit `input_tok['attention_mask']`, preserving the rest of the tokenizer batch. |

`forward_tokens()` removes only the mask from a copied tokenizer mapping and supplies that identical mask as an explicit keyword; all other inputs and requested lens options are preserved. Projection/norm/lm-head module calls do not consume token attention masks and are not language-model forward calls.

The unchanged frozen harness has four input-ID-only calls: `c10e_bandknob.py:114` (full-sequence scorer), `:127` (string scorer), `:141` (teacher-forced per-token scorer), and `:306` (sentence NLL/locality). A top-level science setup pre-hook at `c10x_enginepath_arms.py:430` supplies explicit all-ones kwargs before those unpadded single-sequence forwards. It refuses an unmasked multi-row batch instead of guessing a padding mask, and leaves a supplied mask object unchanged. `configure()` installs it before the pristine snapshot (`:445`); `release()` removes it (`:466`). This is a science setup guard, not a telemetry observation hook. Direct T8 helper entry also establishes it before its warmup (`:755`); the real calibration entry configures H at `c10x_enginepath_telemetry_check.py:321`. The frozen harness predictor (`c10e_bandknob.py:103`), engine `compute_z.py:122`, and `rome/repr_tools.py:147` already unpack tokenizer batches containing their masks.

Test 70 scans all direct language-model calls in the five production modules and records the actual forward kwargs on tiny CPU models. It exercises all four inherited harness scorers, the lens, padded replay and a standalone calibration helper after removing its previous setup guard, with more than 400 recorded forwards. Test 71 rejects unmasked batches, preserves a supplied padding mask by identity and verifies guard removal. The frozen harness file is never imported in a test; its function ASTs are compiled into the CPU stub namespace.

### Device/dtype audit and safe transfers

Every combined device-plus-dtype conversion in the C10X production modules was rewritten. Both transfers and casts are now separate calls, with CPU transfer before the dtype cast:

| Current site | Replacement |
|---|---|
| `c10x_enginepath_arms.py:526` — FE update before weight addition | `upd.cpu().to(dtype=weight.dtype).to(weight.device)` (the code resolves the same weight through `npd[weight_name(...)]`). |
| `c10x_enginepath_arms.py:737` — replay overwrite row | `overwrite[row].cpu().to(dtype=hid.dtype).to(hid.device)`. |
| `c10x_enginepath_arms.py:1029` — injection overwrite | `vector.cpu().to(dtype=hidden.dtype).to(hidden.device)`. |

No combined device/dtype `.to(...)` remains in the five C10X production modules. The existing reporting/capture paths already transfer to CPU before upcasting: lens `c10x_enginepath_arms.py:369`, target observation via `cpu_copy()`, update capture `c10x_enginepath_inertness.py:133`, and independent loss audit `c10x_enginepath_read.py:521–524`. OverTone's MPS-side dtype-only casts and its separate CPU snapshots were also audited. They contain no combined device/dtype transfer.

Test 72 rejects keyword, positional and mixed forms, including `to(device='cpu', dtype=...)`, `to('cpu', dtype)` and `to(torch.device('cpu'), dtype=...)`. Its positive controls accept separate CPU/cast calls. It also scans every Python file under the vendored `memit/`, `rome/` and `util/` helper directories and finds no unsafe transfer form in those helpers.

The frozen harness contains one combined conversion at `c10e_bandknob.py:217`. It takes `upd` from `torch.linalg.solve(A, B).T`, where A/B are formed from CPU K/residual tensors, a CPU projector/cache and CPU identity. Its shape matcher (`memit_dry_run/memit/memit/memit_main.py:287`) only returns that tensor or its transpose. It therefore cannot receive an MPS view on this path. Test 72 pins that sole call and the CPU solve expressions; R5 protects the source bytes. This safe CPU-origin frozen call was retained. No frozen helper capable of receiving an MPS view has a combined CPU/dtype conversion.


The program's expanded audit `results/mps_offset_conversion_audit.md` was read in full, SHA-256 `d0fc6624972f56cb2b5201f56f510260e2545e40883ce65675ab49cf00c5d25d`. It supersedes the initial “clone first” advice: **clone() first and contiguous() are not safe alternatives.** The only adopted transfer sequences are same-dtype CPU transfer followed by a CPU dtype cast, or a same-device dtype cast followed by same-dtype CPU transfer. Float64 casts stay on CPU. The audit also reports narrowing/same-width MPS→CPU casts can corrupt the MPS source, even when the returned CPU result appears correct; that finding is program evidence, not an MPS measurement by this build.

The expanded test 72 now rejects tensor-target `.to(cpu_tensor)` (including the `other=` form and subscript targets), `.type()`/`.type_as()`, raw `cpu_buf.copy_(v)`, `torch.tensor/as_tensor(v, device='cpu', dtype=X)`, and assignments from untransferred tensors into named/declared CPU buffers. Clone-first and contiguous-first combined transfers are explicit negative controls. The scanner allows only audited device/dtype descriptors for a single positional `.to(...)` target and tracks CPU buffers declared by an explicit CPU factory/CPU-transfer binding. Python literals and NumPy interpolation outputs are recognized CPU constructor inputs. Separate CPU-first copies are positive controls.

The retained `copy_` at `c10x_enginepath_inertness.py:114` restores model parameters from pristine CPU snapshots. Its new source guard at `:112` requires `value.device.type == 'cpu'` **before** hashing or copying. The AST test pins that guard before exempting this one CPU-origin call; no other unguarded copy is exempted. A fake MPS-device metadata object (no MPS tensor or backend call) proves restoration raises `PRISTINE_SNAPSHOT_NOT_CPU` before any copy or tensor access. Thus the current C10X paths have no MPS→CPU copy-with-cast constructor, tensor-target conversion, type conversion or CPU-buffer assignment. The frozen helper constructor exceptions are CPU NumPy arrays (`util/runningstats.py:1105/:1142`), and the frozen writer remains the CPU-origin solve described above. The guard stays within the authorized C10X and vendored-helper scope; the audit's wider C10Z remediation belongs to the program.

The same test exercises a nonzero-offset, noncontiguous CPU view through `cpu_copy()` and `norm64()`, asserting exact copied values and the independent float64 norm. This validates the audited copy order on CPU; it is not a runtime MPS reproduction.

The program's explicit forward-mask and transfer corrections add narrow exceptions to the copied-expression checks. `verify_scorer_ast()` (`c10x_enginepath_arms.py:412`) accepts exactly the explicit all-ones mask, removes only that keyword for comparison, and still pins the original loop and return. `verify_solver_ast()` (`c10x_overtone_z.py:227`) accepts exactly the masked tokenizer call before comparing the frozen solver outside the declared objective replacement. `verify_fe_ast()` (`c10x_enginepath_arms.py:533`) accepts exactly the split CPU/dtype/device transfer before comparing the original writer with its three preregistered FE substitutions. Other changes still fail those structural checks. The FE solve/update formulas, engine/harness bytes, float64 gates, pinned contexts and prereg thresholds remain unchanged. The prereg itself was not amended by this build.

### Test-first evidence

The nine regression groups are at `experiments/track_c/c10x_enginepath_selftest.py`:

| ID | Test and current line | Result |
|---|---|---|
| 64 | `test_fp32_overflow_capture_and_parity_remain_report_only:1404` | RED → GREEN |
| 65 | `test_tagged_fp32_diagnostics_preserve_file_admission:1422` | RED → GREEN |
| 66 | `test_recipe_fp32_overflow_does_not_halt_or_change_labels:1457` | RED → GREEN |
| 67 | `test_disable_cutoff_never_excuses_earlier_omissions:1476` | RED → GREEN |
| 68 | `test_disable_marker_records_failed_answer_cutoff:1507` | RED → GREEN |
| 69 | `test_answer_audit_uses_runtime_recipe_order:1519` | RED → GREEN |
| 70 | `test_every_c10x_forward_has_explicit_attention_mask:1524` | RED → GREEN |
| 71 | `test_mask_guard_refuses_unmasked_batches_and_restores:1549` | RED → GREEN |
| 72 | `test_no_combined_device_dtype_conversions:1559` | RED → GREEN |

The test plan was appended before the production edits. Initial full-suite RED: 71 tests, 11 own assertion failures, zero errors; all original 63 tests passed. Saved as `/private/tmp/c10x_build/astra_review_fixes_red.log`, SHA-256 `d82d286744b38c610aa89fa45985b446a1d13f0ffc68a9f0de950a6c56cf7c6f`. Verbatim summary:

~~~text
Ran 71 tests in 16.780s

FAILED (failures=11)
LISTING: attributed-protected changes = {}
LISTING: observed/unattributed other changes = {}
SYS.MODULES PASS: c10e_bandknob/transformers/datasets absent
~~~

After the fp32 fix, its three new regression groups passed; the remaining eight assertions failed in the cutoff/mask groups (`astra_review_fp32_green.log`). After the cutoff fix, the remaining two failures were the mask tests (`astra_review_cutoff_green.log`). An intermediate mask run recorded two test-fixture errors (`astra_review_mask_green.log`): a pristine hook snapshot included the setup guard that run cleanup then correctly removed, and the decorated scorer's wrapper globals lacked torch for compiling another harness function. The failed-pin fixture now snapshots a released harness, matching live run entry, and also asserts guard cleanup; copied functions use the unwrapped original namespace. The separate first targeted invocation lacked the module search path (`astra_review_standalone_mask_red.log`) and is **not** counted as assertion-level RED evidence.

After the program's device/dtype correction, test 72 was written before the three transfer edits. A corrected targeted RED run also strengthened test 70 to exercise standalone calibration entry. It produced two own assertion failures and zero errors (`/private/tmp/c10x_build/astra_review_conversion_red.log`, SHA-256 `6d529ae6c6a02f7bc7580ba0e5ee52cae8a15cbc32bc8b6bd1bcf534bdd25dcf`):

~~~text
FAIL: test_every_c10x_forward_has_explicit_attention_mask
AssertionError: unexpectedly None
FAIL: test_no_combined_device_dtype_conversions
AssertionError: Lists differ: [('c10x_enginepath_arms.py', 522), ('c10x_[56 chars]726)] != []

Ran 2 tests in 0.177s

FAILED (failures=2)
~~~


The later expanded-copy-form regression was also written before the CPU-source guard and scanner extension. Its corrected assertion-level RED is `/private/tmp/c10x_build/astra_review_all_copy_forms_red_assertions.log`, SHA-256 `e4e6154ed1537d306852f715ac88c2441e66e87b67168c1da3525eaa4212f1b4`: **14 own assertion failures, zero errors**. It rejects the incomplete old detector and proves the missing restore source guard. An earlier intermediate run (`astra_review_all_copy_forms_red_full.log`) had 13 failures plus an AttributeError from the fake metadata object; the corrected test asserts that the caught exception is Halt with the required code, so that error is not counted as assertion-level RED. The focused GREEN (`astra_review_all_copy_forms_green.log`) passed in 0.140s before the final full-suite rerun.

~~~text
AssertionError: False is not true : v.to(cpu_tensor)
Ran 1 test in 0.114s

FAILED (failures=14)
~~~

Final GREEN command (absolute paths, one light serial suite):

~~~sh
/opt/homebrew/bin/rtk proxy env TMPDIR=/private/tmp/c10x_build /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python -B /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py > /private/tmp/c10x_build/astra_review_fixes_final_green.log 2>&1
~~~

Exit 0. The selftest keeps torch CPU threads at one, fixtures and allowlisted stub children under `/private/tmp/c10x_build/roots/`, and the live-tree write guard active. No model/tokenizer load, GPU/MPS tensor, transformers/datasets/harness import or real training/inertness dispatch occurred. No direct shell wrapper is launched; the executable/git-mode assertions remain in the suite and the current launch paths use `sys.executable`.

Complete final output, SHA-256 `3fef0b175510e24ddc91769925f06e24940d5ab1f244e03165bb0af357fc12a2`:

~~~text
test_admitted_process_pair_and_p2_gate (__main__.FileAdmissionTests.test_admitted_process_pair_and_p2_gate) ... ok
test_amendment_p_digest_refusals (__main__.FileAdmissionTests.test_amendment_p_digest_refusals) ... ok
test_amendment_p_prereg_pin (__main__.FileAdmissionTests.test_amendment_p_prereg_pin) ... ok
test_answer_audit_uses_runtime_recipe_order (__main__.FileAdmissionTests.test_answer_audit_uses_runtime_recipe_order) ... ok
test_complete_stub_run_persists_every_record (__main__.FileAdmissionTests.test_complete_stub_run_persists_every_record) ... ok
test_context_binding_enter_failure_restores (__main__.FileAdmissionTests.test_context_binding_enter_failure_restores) ... ok
test_deadline_completion_and_previous_overhead (__main__.FileAdmissionTests.test_deadline_completion_and_previous_overhead) ... ok
test_detailed_admission_negative_controls (__main__.FileAdmissionTests.test_detailed_admission_negative_controls) ... ok
test_direct_shell_launchers_are_executable_in_git (__main__.FileAdmissionTests.test_direct_shell_launchers_are_executable_in_git) ... DIRECT SHELL ENTRY POINTS: none; all three supervised commands use sys.executable
ok
test_disable_cutoff_never_excuses_earlier_omissions (__main__.FileAdmissionTests.test_disable_cutoff_never_excuses_earlier_omissions) ... ok
test_disable_marker_records_failed_answer_cutoff (__main__.FileAdmissionTests.test_disable_marker_records_failed_answer_cutoff) ... ok
test_every_c10x_forward_has_explicit_attention_mask (__main__.FileAdmissionTests.test_every_c10x_forward_has_explicit_attention_mask) ... ok
test_every_science_record_roundtrip_and_reader_audit (__main__.FileAdmissionTests.test_every_science_record_roundtrip_and_reader_audit) ... ok
test_fp32_overflow_capture_and_parity_remain_report_only (__main__.FileAdmissionTests.test_fp32_overflow_capture_and_parity_remain_report_only) ... ok
test_late_supervisor_persistence_is_unreadable (__main__.FileAdmissionTests.test_late_supervisor_persistence_is_unreadable) ... ok
test_mask_guard_refuses_unmasked_batches_and_restores (__main__.FileAdmissionTests.test_mask_guard_refuses_unmasked_batches_and_restores) ... ok
test_missing_inertness_evidence_is_refused (__main__.FileAdmissionTests.test_missing_inertness_evidence_is_refused) ... ok
test_no_combined_device_dtype_conversions (__main__.FileAdmissionTests.test_no_combined_device_dtype_conversions) ... ok
test_pinned_contexts_never_sample (__main__.FileAdmissionTests.test_pinned_contexts_never_sample) ... ok
test_pinned_processes_and_halted_context_identity (__main__.FileAdmissionTests.test_pinned_processes_and_halted_context_identity) ... ok
test_post_audit_blocks_are_killed_by_final_deadline (__main__.FileAdmissionTests.test_post_audit_blocks_are_killed_by_final_deadline) ... ok
test_post_audit_budget_and_disabled_disposition (__main__.FileAdmissionTests.test_post_audit_budget_and_disabled_disposition) ... ok
test_post_audit_rejects_contradictory_receipts (__main__.FileAdmissionTests.test_post_audit_rejects_contradictory_receipts) ... ok
test_post_audit_startup_consumes_remaining_budget (__main__.FileAdmissionTests.test_post_audit_startup_consumes_remaining_budget) ... ok
test_reader_publishes_invalid_with_exit_zero (__main__.FileAdmissionTests.test_reader_publishes_invalid_with_exit_zero) ... ok
test_recipe_fp32_overflow_does_not_halt_or_change_labels (__main__.FileAdmissionTests.test_recipe_fp32_overflow_does_not_halt_or_change_labels) ... ok
test_script_alias_and_preflight_refusal_in_isolated_child (__main__.FileAdmissionTests.test_script_alias_and_preflight_refusal_in_isolated_child) ... ok
test_supervisor_fail_closed_and_combining_output_path (__main__.FileAdmissionTests.test_supervisor_fail_closed_and_combining_output_path) ... ok
test_tagged_fp32_diagnostics_preserve_file_admission (__main__.FileAdmissionTests.test_tagged_fp32_diagnostics_preserve_file_admission) ... ok
test_actual_fe_writes_and_null_solve_observer (__main__.IntegrationTests.test_actual_fe_writes_and_null_solve_observer) ... ok
test_actual_singleton_reduction_and_resolved_capture (__main__.IntegrationTests.test_actual_singleton_reduction_and_resolved_capture) ... ok
test_projection_uses_remaining_units_and_setup_clock (__main__.IntegrationTests.test_projection_uses_remaining_units_and_setup_clock) ... ok
test_solver_masked_gradient_clip_filter_and_tie (__main__.IntegrationTests.test_solver_masked_gradient_clip_filter_and_tie) ... ok
test_telemetry_recipe_records_and_counts_equal (__main__.IntegrationTests.test_telemetry_recipe_records_and_counts_equal) ... ok
test_telemetry_valid_admission_and_runner_no_writes (__main__.IntegrationTests.test_telemetry_valid_admission_and_runner_no_writes) ... ok
test_three_recipe_telemetry_probe_and_file_equality (__main__.IntegrationTests.test_three_recipe_telemetry_probe_and_file_equality) ... ok
test_reader_control_boundaries (__main__.ReaderTests.test_reader_control_boundaries) ... ok
test_reader_count_classes (__main__.ReaderTests.test_reader_count_classes) ... ok
test_reader_flags_denominators_nulls (__main__.ReaderTests.test_reader_flags_denominators_nulls) ... ok
test_reader_interpretation_and_null_table (__main__.ReaderTests.test_reader_interpretation_and_null_table) ... ok
test_reader_law3_boundaries (__main__.ReaderTests.test_reader_law3_boundaries) ... ok
test_reader_locality_boundaries (__main__.ReaderTests.test_reader_locality_boundaries) ... ok
test_reader_process_combination (__main__.ReaderTests.test_reader_process_combination) ... ok
test_reader_qualifier_boundaries (__main__.ReaderTests.test_reader_qualifier_boundaries) ... ok
test_reader_replication (__main__.ReaderTests.test_reader_replication) ... ok
test_reader_validity (__main__.ReaderTests.test_reader_validity) ... ok
test_active_null_negative_controls (__main__.SeamTests.test_active_null_negative_controls) ... ok
test_baseline_miss_stops_candidates (__main__.SeamTests.test_baseline_miss_stops_candidates) ... ok
test_capture_bindings_identity_attribution (__main__.SeamTests.test_capture_bindings_identity_attribution) ... ok
test_dispatch_call_time_flag (__main__.SeamTests.test_dispatch_call_time_flag) ... ok
test_fe_ast_three_changes (__main__.SeamTests.test_fe_ast_three_changes) ... ok
test_fe_modes_and_keys (__main__.SeamTests.test_fe_modes_and_keys) ... ok
test_float64_dense_reference (__main__.SeamTests.test_float64_dense_reference) ... ok
test_independent_full_vocabulary_audit (__main__.SeamTests.test_independent_full_vocabulary_audit) ... ok
test_knobs_and_frame_subjects (__main__.SeamTests.test_knobs_and_frame_subjects) ... ok
test_launch_refusals (__main__.SeamTests.test_launch_refusals) ... ok
test_pristine_hash_restore_hooks (__main__.SeamTests.test_pristine_hash_restore_hooks) ... ok
test_process2_requires_eligibility (__main__.SeamTests.test_process2_requires_eligibility) ... ok
test_recipe_states_counters (__main__.SeamTests.test_recipe_states_counters) ... ok
test_solver_ast_and_gradients (__main__.SeamTests.test_solver_ast_and_gradients) ... ok
test_tolerance_and_finiteness (__main__.SeamTests.test_tolerance_and_finiteness) ... ok
test_watchdog_and_projection (__main__.SeamTests.test_watchdog_and_projection) ... ok
test_frozen_bytes_and_imports (__main__.TelemetryTests.test_frozen_bytes_and_imports) ... IMPORT GUARD PASS: c10e_bandknob, transformers, datasets absent
ok
test_isolation_positive_control_children_meta (__main__.TelemetryTests.test_isolation_positive_control_children_meta) ... ok
test_post_run_answer_audit (__main__.TelemetryTests.test_post_run_answer_audit) ... ok
test_strict_json_roundtrips (__main__.TelemetryTests.test_strict_json_roundtrips) ... ok
test_telemetry_code_path_equality (__main__.TelemetryTests.test_telemetry_code_path_equality) ... ok
test_telemetry_failure_boundaries (__main__.TelemetryTests.test_telemetry_failure_boundaries) ... ok
test_telemetry_inertness_schedule (__main__.TelemetryTests.test_telemetry_inertness_schedule) ... ok
test_telemetry_line_volume (__main__.TelemetryTests.test_telemetry_line_volume) ... ok
test_telemetry_state_unchanged (__main__.TelemetryTests.test_telemetry_state_unchanged) ... ok
test_telemetry_switch_admission (__main__.TelemetryTests.test_telemetry_switch_admission) ... ok

----------------------------------------------------------------------
Ran 72 tests in 17.559s

OK
LISTING: attributed-protected changes = {}
LISTING: observed/unattributed other changes = {}
SYS.MODULES PASS: c10e_bandknob/transformers/datasets absent
~~~

### Revised identities and scope

These are the hashes of the six source files tested by that final run. “Before” is the original reviewed 63-test build, not an intermediate fix state.

| File | Before SHA-256 | Revised SHA-256 |
|---|---|---|
| `experiments/track_c/c10x_enginepath_arms.py` | `798993b823232643575a2749ba9e9278bc8a4bae62b6b3d4d25563c615c10ed2` | `3415e9c093c04ea6e6aaf580605760fd3924e926454fc7186d6d6b5364cd9b80` |
| `experiments/track_c/c10x_enginepath_inertness.py` | `665e954cc75624f44b01353e015eb55b3c61d80a87042be1d835712d663921cf` | `c0c19b97cfeac03a5c12176e33b63a10d06489ca56f7b365a6e03ef1e4ba56e9` |
| `experiments/track_c/c10x_enginepath_read.py` | `b9543fc18961feb505dfa76a393c94a0438ea6081d1a9559148ff50134e40978` | `0c22b6b222e37b2d1a81ed649836f8fb6297a8440d0b2f833389cba1a25ff21a` |
| `experiments/track_c/c10x_overtone_z.py` | `70ad3d1b57db5ced0c6b69eb9ea40b50aed0773b8c0e04e9bad086c84f0d8664` | `8b32ca840c1451624ba5f46143a6e65a03ae69e968dd0e6180d04fa5683dac42` |
| `experiments/track_c/c10x_enginepath_telemetry_check.py` | `f0d55574c3a23908b34c4f4081d11f4270a92314eedfbe81432ebe0024eace4f` | `e95beb2cef310fa1050ccb4a2b60ac8224f493ea4d513d97868f3b9a9c99fe80` |
| `experiments/track_c/c10x_enginepath_selftest.py` | `2e617a787bff334c20ead6f73d1518b474a85c762058f30f2e8a407d05f909f4` | `1ba5289d047889417cba0a2135fcc12b3405ef056fe72d0435caf6290b7600dd` |

The unchanged Amendment P prereg pin is `43a81103d68b953c2007e978b3ebecf11aadf66a7f121346047279845e8fc883`. The C10Q context identity remains `c7dabbe7c25a7e58653621d9cc66e37b35c865ae09b73b6a96073a184c6c98da`; no alternative source, sampling, seed-dependent context draw or frame substitution was introduced. The existing fixed-template regeneration and process context/frame matching tests pass.

Current scope snapshot: `/private/tmp/c10x_build/after_review_fixes_final/`. All 188 R5 files match the expected amended baseline; the only difference from the original pre-build baseline is the already authorized program-authored Amendment P SHA. Protected git diff exits 0. The original results/architecture listing has 7,086 entries; the current snapshot has 7,856. Differences are explicitly classified as one authorized report, one program-supplied Astra review (the exact input SHA above), 2,907 observed/unattributed entries from the shared workspace, and **zero unexplained protected changes**. This is not a claim that the shared global tree is unchanged. The final selftest's own before/after listing is unchanged.

| Current receipt | SHA-256 |
|---|---|
| `after_review_fixes_final/summary.json` | `6a81a10c66236a05a140076fee5679154665aae708521e5d0817d87fe937e07d` |
| `after_review_fixes_final/r5_sha256.json` | `c149cf6006ca120a28d3ec505c1768c10d2485082c8729e0f5640fe8c414d190` |
| `after_review_fixes_final/listing.json` | `80d0ab36cd7c3c03ff0f217967d0c992454fd54a68b2ea207e8e4d2bc6e05e62` |
| `after_review_fixes_final/listing_difference.json` | `29b44c5b8ccde68f20fd6e0936abc31ddb1862783b17395f41a06cee04319e60` |

After publication, `/private/tmp/c10x_build/after_review_report/` repeats the protected-byte/listing check. `/private/tmp/c10x_build/review_fixes_receipt.json` binds the final report SHA, retained original prefix, six revised source hashes, final 72-test log and post-publication scope. The original `report_receipt.json` remains historical and is not overwritten.

Live LAW#3/LAW#5/G8, MPS tensor behavior, memory/timing feasibility and write-arm scientific results remain **UNVERIFIED**. The program's instruction to skip the separately authorized T8 launch is retained; only its tiny CPU stub path was tested here. First attempts remain telemetry off and supervisor mediated. No launch/GO record, experiment output, prereg, engine/harness/config/precedent, ledger or git state was written by these fixes.


## Mask revert

**COMPLETE: all 72 model-free CPU tests PASS (17.689s), exit 0, zero failures/errors.** The program confirmed the attention-mask hypothesis was REFUTED and instructed removal of its single-sequence intervention. The frozen harness scorer forwards again receive their historical positional tensors with no injected kwargs. This section supersedes only the mask intervention and mask-test requirements described in the preceding Review fixes section. Amendment M, T11 and the safe device/dtype changes remain in force.

The complete previous report is preserved byte-for-byte: 190,334 bytes, SHA-256 `c92811392c9bbacc8016e1639d357f8cbb0a5804cbf5c6854b26b4f4e554bc8f`. Its earlier original-build and Review fixes receipts remain historical records.

### Reverted sites and retained tokenizer calls

| Site | Final behavior |
|---|---|
| `experiments/track_c/c10x_enginepath_arms.py:425` and `experiments/track_c/c10x_enginepath_arms.py:445` | Remove the science setup mask pre-hook, both helper functions and its release cleanup. Configuration/release register no mask hook. |
| `experiments/track_c/c10x_enginepath_arms.py:729` | Remove the same hook installation from standalone calibration. Its warmup and plain/reference/observed passes use the original single-sequence arguments. |
| `experiments/track_c/c10x_enginepath_arms.py:378`, `experiments/track_c/c10x_enginepath_arms.py:395`; forward statements at A:387 and A:404 | Restore `model(cur)`. The only AST-permitted scorer additions remain the exact sink/capture statement immediately before the unchanged return and the function-name normalization. |
| `experiments/track_c/c10x_enginepath_arms.py:412` | Remove the exception that stripped an added attention_mask before comparison. The scorer AST comparison is strict again; an all-ones-mask mutant is rejected. |
| `experiments/track_c/c10x_enginepath_arms.py:1062` | Restore the teacher-forced probe to `harness.model(cur)` with no mask keyword. |
| `experiments/track_c/c10x_enginepath_selftest.py:979` | Remove the mask-only prerequisite release and mask-hook-attribute assertion; the pristine restoration test passes without that scaffolding. |

**KEEP the explicit tokenizer masks** allowed by program item (3): the logit lens at `experiments/track_c/c10x_enginepath_arms.py:365`, batch replay at `experiments/track_c/c10x_enginepath_arms.py:720`, top1 at `experiments/track_c/c10x_enginepath_arms.py:1020`, and overtone at `experiments/track_c/c10x_overtone_z.py:145`. The shared token-mapping helper is at `experiments/track_c/c10x_enginepath_arms.py:351`. Each forwards the tokenizer mapping's existing attention_mask; none supplies an all-ones mask to a historical single-sequence call. The overtone AST allowance for spelling out that existing tokenizer mask is retained.

The correct CPU-before-dtype conversions are unchanged at `experiments/track_c/c10x_enginepath_arms.py:503`, `experiments/track_c/c10x_enginepath_arms.py:714`, and `experiments/track_c/c10x_enginepath_arms.py:1005`. Test 72, `experiments/track_c/c10x_enginepath_selftest.py:1602`, still bans the unsafe combined/device-target/type/constructor/copy forms, including clone-first variants, and retains the pristine CPU-snapshot guard. Inertness, reader, overtone and telemetry-check source bytes are unchanged from the accepted Review fixes build, as the six-source table below proves.

### Test-first RED and GREEN

The plan was recorded at `/private/tmp/c10x_build/mask_revert_plan.md` before production changes. Tests were revised first; the full selftest was run RED while production A still had SHA-256 `3415e9c093c04ea6e6aaf580605760fd3924e926454fc7186d6d6b5364cd9b80`. The RED selftest source SHA was `3db338182aff25f0d3444ae982f6fa3fd9214e63e452f342bb82bdcc30ee1162`, saved in `after_review_mask_before/r2_sha256.json`.

| Test | Regression and evidence |
|---|---|
| Revised test 70, `experiments/track_c/c10x_enginepath_selftest.py:1522` | Positional single-sequence calls require one original tensor and zero kwargs; tokenizer-mapping calls retain their existing mask. The AST check caught the three added all-ones arguments at former A:387, :404, :1086 in RED. GREEN records both masked tokenizer and unmasked single-sequence forwards through the frozen scorers, lens, calibration and batch replay, with more than 400 calls. |
| Replacement test 71, `experiments/track_c/c10x_enginepath_selftest.py:1554` | The obsolete mask-guard test is replaced by the requested historical-call regression. Capture the four unchanged harness functions before configuration, then compare actual tensors, keyword sets, results and hook registration after configuring twice. Forward counts are 2/4/1/1 for full_seq_match, string_match, teacher_forced_pertok and sentence_nll; all kwargs are empty. Both scorer copies must match the original full_seq_match, including captured generated IDs. The mask-mutant negative control verifies strict Amendment T4 AST rejection. |

RED: **72 tests ran in 17.842s; exit 1; 9 expected assertion failures across these two tests, zero errors**. The eight test-71 subcases failed on hook registration, the four frozen scorer kwargs, both scorer copies, and mask-mutant rejection. Test 70 failed on the three changed forward AST sites. All other tests passed. Relevant verbatim failure blocks:

~~~text
FAIL: test_frozen_scorer_forwards_have_no_injected_kwargs (__main__.FileAdmissionTests.test_frozen_scorer_forwards_have_no_injected_kwargs) (case='configuration preserves hook registry')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 1582, in test_frozen_scorer_forwards_have_no_injected_kwargs
    self.assertEqual(dict(self.H.model._forward_pre_hooks),before)
AssertionError: {17: <function require_attention_mask at 0x10ab9d8a0>} != {}
- {17: <function require_attention_mask at 0x10ab9d8a0>}
+ {}

======================================================================
FAIL: test_frozen_scorer_forwards_have_no_injected_kwargs (__main__.FileAdmissionTests.test_frozen_scorer_forwards_have_no_injected_kwargs) (case='full_seq_match')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 1584, in test_frozen_scorer_forwards_have_no_injected_kwargs
    with self.subTest(case=name):compare(record(function,args),baseline[name])
                                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 1578, in compare
    self.assertEqual(kwargs,old_kwargs);self.assertEqual(len(inputs),len(old_inputs))
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: Tuples differ: ('attention_mask',) != ()

First tuple contains 1 additional elements.
First extra element 0:
'attention_mask'

- ('attention_mask',)
+ ()

======================================================================
FAIL: test_frozen_scorer_forwards_have_no_injected_kwargs (__main__.FileAdmissionTests.test_frozen_scorer_forwards_have_no_injected_kwargs) (case='AST rejects single-sequence mask')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 1600, in test_frozen_scorer_forwards_have_no_injected_kwargs
    self.assertFalse(A.verify_scorer_ast(frozen))
AssertionError: True is not false

======================================================================
FAIL: test_tokenizer_forwards_preserve_attention_mask (__main__.FileAdmissionTests.test_tokenizer_forwards_preserve_attention_mask)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 1533, in test_tokenizer_forwards_preserve_attention_mask
    self.assertEqual(missing,[])
AssertionError: Lists differ: [('c10x_enginepath_arms.py', 387), ('c10x_[56 chars]086)] != []

First list contains 3 additional elements.
First extra element 0:
('c10x_enginepath_arms.py', 387)

+ []
- [('c10x_enginepath_arms.py', 387),
-  ('c10x_enginepath_arms.py', 404),
-  ('c10x_enginepath_arms.py', 1086)]

Ran 72 tests in 17.842s

FAILED (failures=9)
LISTING: attributed-protected changes = {}
LISTING: observed/unattributed other changes = {}
SYS.MODULES PASS: c10e_bandknob/transformers/datasets absent
~~~

Only after this RED run were the mask intervention and its AST exception removed. The mask-specific restoration scaffolding was then removed from the existing context-binding test. The full selftest was rerun with no subsequent source edits.

Both full-suite commands used this light serial configuration, with the relevant log destination (RED or GREEN):

~~~sh
/opt/homebrew/bin/rtk proxy env TMPDIR=/private/tmp/c10x_build PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python -B /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py > /private/tmp/c10x_build/mask_revert_green.log 2>&1
~~~

GREEN: **72 tests ran in 17.689s; exit 0; zero failures/errors**. All Amendment M fp32 report-only overflow regressions, strict float64 checks, T11 cutoff negatives, context-template pin/regeneration/process checks, executable-entrypoint check, safe-conversion AST test 72 and earlier scientific-plumbing controls pass. The two replaced/updated mask groups keep the total at 72. Full GREEN output:

~~~text
test_admitted_process_pair_and_p2_gate (__main__.FileAdmissionTests.test_admitted_process_pair_and_p2_gate) ... ok
test_amendment_p_digest_refusals (__main__.FileAdmissionTests.test_amendment_p_digest_refusals) ... ok
test_amendment_p_prereg_pin (__main__.FileAdmissionTests.test_amendment_p_prereg_pin) ... ok
test_answer_audit_uses_runtime_recipe_order (__main__.FileAdmissionTests.test_answer_audit_uses_runtime_recipe_order) ... ok
test_complete_stub_run_persists_every_record (__main__.FileAdmissionTests.test_complete_stub_run_persists_every_record) ... ok
test_context_binding_enter_failure_restores (__main__.FileAdmissionTests.test_context_binding_enter_failure_restores) ... ok
test_deadline_completion_and_previous_overhead (__main__.FileAdmissionTests.test_deadline_completion_and_previous_overhead) ... ok
test_detailed_admission_negative_controls (__main__.FileAdmissionTests.test_detailed_admission_negative_controls) ... ok
test_direct_shell_launchers_are_executable_in_git (__main__.FileAdmissionTests.test_direct_shell_launchers_are_executable_in_git) ... DIRECT SHELL ENTRY POINTS: none; all three supervised commands use sys.executable
ok
test_disable_cutoff_never_excuses_earlier_omissions (__main__.FileAdmissionTests.test_disable_cutoff_never_excuses_earlier_omissions) ... ok
test_disable_marker_records_failed_answer_cutoff (__main__.FileAdmissionTests.test_disable_marker_records_failed_answer_cutoff) ... ok
test_every_science_record_roundtrip_and_reader_audit (__main__.FileAdmissionTests.test_every_science_record_roundtrip_and_reader_audit) ... ok
test_fp32_overflow_capture_and_parity_remain_report_only (__main__.FileAdmissionTests.test_fp32_overflow_capture_and_parity_remain_report_only) ... ok
test_frozen_scorer_forwards_have_no_injected_kwargs (__main__.FileAdmissionTests.test_frozen_scorer_forwards_have_no_injected_kwargs) ... ok
test_late_supervisor_persistence_is_unreadable (__main__.FileAdmissionTests.test_late_supervisor_persistence_is_unreadable) ... ok
test_missing_inertness_evidence_is_refused (__main__.FileAdmissionTests.test_missing_inertness_evidence_is_refused) ... ok
test_no_combined_device_dtype_conversions (__main__.FileAdmissionTests.test_no_combined_device_dtype_conversions) ... ok
test_pinned_contexts_never_sample (__main__.FileAdmissionTests.test_pinned_contexts_never_sample) ... ok
test_pinned_processes_and_halted_context_identity (__main__.FileAdmissionTests.test_pinned_processes_and_halted_context_identity) ... ok
test_post_audit_blocks_are_killed_by_final_deadline (__main__.FileAdmissionTests.test_post_audit_blocks_are_killed_by_final_deadline) ... ok
test_post_audit_budget_and_disabled_disposition (__main__.FileAdmissionTests.test_post_audit_budget_and_disabled_disposition) ... ok
test_post_audit_rejects_contradictory_receipts (__main__.FileAdmissionTests.test_post_audit_rejects_contradictory_receipts) ... ok
test_post_audit_startup_consumes_remaining_budget (__main__.FileAdmissionTests.test_post_audit_startup_consumes_remaining_budget) ... ok
test_reader_publishes_invalid_with_exit_zero (__main__.FileAdmissionTests.test_reader_publishes_invalid_with_exit_zero) ... ok
test_recipe_fp32_overflow_does_not_halt_or_change_labels (__main__.FileAdmissionTests.test_recipe_fp32_overflow_does_not_halt_or_change_labels) ... ok
test_script_alias_and_preflight_refusal_in_isolated_child (__main__.FileAdmissionTests.test_script_alias_and_preflight_refusal_in_isolated_child) ... ok
test_supervisor_fail_closed_and_combining_output_path (__main__.FileAdmissionTests.test_supervisor_fail_closed_and_combining_output_path) ... ok
test_tagged_fp32_diagnostics_preserve_file_admission (__main__.FileAdmissionTests.test_tagged_fp32_diagnostics_preserve_file_admission) ... ok
test_tokenizer_forwards_preserve_attention_mask (__main__.FileAdmissionTests.test_tokenizer_forwards_preserve_attention_mask) ... ok
test_actual_fe_writes_and_null_solve_observer (__main__.IntegrationTests.test_actual_fe_writes_and_null_solve_observer) ... ok
test_actual_singleton_reduction_and_resolved_capture (__main__.IntegrationTests.test_actual_singleton_reduction_and_resolved_capture) ... ok
test_projection_uses_remaining_units_and_setup_clock (__main__.IntegrationTests.test_projection_uses_remaining_units_and_setup_clock) ... ok
test_solver_masked_gradient_clip_filter_and_tie (__main__.IntegrationTests.test_solver_masked_gradient_clip_filter_and_tie) ... ok
test_telemetry_recipe_records_and_counts_equal (__main__.IntegrationTests.test_telemetry_recipe_records_and_counts_equal) ... ok
test_telemetry_valid_admission_and_runner_no_writes (__main__.IntegrationTests.test_telemetry_valid_admission_and_runner_no_writes) ... ok
test_three_recipe_telemetry_probe_and_file_equality (__main__.IntegrationTests.test_three_recipe_telemetry_probe_and_file_equality) ... ok
test_reader_control_boundaries (__main__.ReaderTests.test_reader_control_boundaries) ... ok
test_reader_count_classes (__main__.ReaderTests.test_reader_count_classes) ... ok
test_reader_flags_denominators_nulls (__main__.ReaderTests.test_reader_flags_denominators_nulls) ... ok
test_reader_interpretation_and_null_table (__main__.ReaderTests.test_reader_interpretation_and_null_table) ... ok
test_reader_law3_boundaries (__main__.ReaderTests.test_reader_law3_boundaries) ... ok
test_reader_locality_boundaries (__main__.ReaderTests.test_reader_locality_boundaries) ... ok
test_reader_process_combination (__main__.ReaderTests.test_reader_process_combination) ... ok
test_reader_qualifier_boundaries (__main__.ReaderTests.test_reader_qualifier_boundaries) ... ok
test_reader_replication (__main__.ReaderTests.test_reader_replication) ... ok
test_reader_validity (__main__.ReaderTests.test_reader_validity) ... ok
test_active_null_negative_controls (__main__.SeamTests.test_active_null_negative_controls) ... ok
test_baseline_miss_stops_candidates (__main__.SeamTests.test_baseline_miss_stops_candidates) ... ok
test_capture_bindings_identity_attribution (__main__.SeamTests.test_capture_bindings_identity_attribution) ... ok
test_dispatch_call_time_flag (__main__.SeamTests.test_dispatch_call_time_flag) ... ok
test_fe_ast_three_changes (__main__.SeamTests.test_fe_ast_three_changes) ... ok
test_fe_modes_and_keys (__main__.SeamTests.test_fe_modes_and_keys) ... ok
test_float64_dense_reference (__main__.SeamTests.test_float64_dense_reference) ... ok
test_independent_full_vocabulary_audit (__main__.SeamTests.test_independent_full_vocabulary_audit) ... ok
test_knobs_and_frame_subjects (__main__.SeamTests.test_knobs_and_frame_subjects) ... ok
test_launch_refusals (__main__.SeamTests.test_launch_refusals) ... ok
test_pristine_hash_restore_hooks (__main__.SeamTests.test_pristine_hash_restore_hooks) ... ok
test_process2_requires_eligibility (__main__.SeamTests.test_process2_requires_eligibility) ... ok
test_recipe_states_counters (__main__.SeamTests.test_recipe_states_counters) ... ok
test_solver_ast_and_gradients (__main__.SeamTests.test_solver_ast_and_gradients) ... ok
test_tolerance_and_finiteness (__main__.SeamTests.test_tolerance_and_finiteness) ... ok
test_watchdog_and_projection (__main__.SeamTests.test_watchdog_and_projection) ... ok
test_frozen_bytes_and_imports (__main__.TelemetryTests.test_frozen_bytes_and_imports) ... IMPORT GUARD PASS: c10e_bandknob, transformers, datasets absent
ok
test_isolation_positive_control_children_meta (__main__.TelemetryTests.test_isolation_positive_control_children_meta) ... ok
test_post_run_answer_audit (__main__.TelemetryTests.test_post_run_answer_audit) ... ok
test_strict_json_roundtrips (__main__.TelemetryTests.test_strict_json_roundtrips) ... ok
test_telemetry_code_path_equality (__main__.TelemetryTests.test_telemetry_code_path_equality) ... ok
test_telemetry_failure_boundaries (__main__.TelemetryTests.test_telemetry_failure_boundaries) ... ok
test_telemetry_inertness_schedule (__main__.TelemetryTests.test_telemetry_inertness_schedule) ... ok
test_telemetry_line_volume (__main__.TelemetryTests.test_telemetry_line_volume) ... ok
test_telemetry_state_unchanged (__main__.TelemetryTests.test_telemetry_state_unchanged) ... ok
test_telemetry_switch_admission (__main__.TelemetryTests.test_telemetry_switch_admission) ... ok

----------------------------------------------------------------------
Ran 72 tests in 17.689s

OK
LISTING: attributed-protected changes = {}
LISTING: observed/unattributed other changes = {}
SYS.MODULES PASS: c10e_bandknob/transformers/datasets absent
~~~

### Final source identities and protected scope

“Before” is the accepted 72-test Review fixes build at the start of this request. Only arms and selftest changed in this Mask revert.

| File | Before SHA-256 | Final SHA-256 |
|---|---|---|
| `experiments/track_c/c10x_enginepath_arms.py` | `3415e9c093c04ea6e6aaf580605760fd3924e926454fc7186d6d6b5364cd9b80` | `eea47ea72d071c6e9dfd5b301dfa8073c50aa0e3d02149de9660aae837f182db` |
| `experiments/track_c/c10x_enginepath_inertness.py` | `c0c19b97cfeac03a5c12176e33b63a10d06489ca56f7b365a6e03ef1e4ba56e9` | `c0c19b97cfeac03a5c12176e33b63a10d06489ca56f7b365a6e03ef1e4ba56e9` |
| `experiments/track_c/c10x_enginepath_read.py` | `0c22b6b222e37b2d1a81ed649836f8fb6297a8440d0b2f833389cba1a25ff21a` | `0c22b6b222e37b2d1a81ed649836f8fb6297a8440d0b2f833389cba1a25ff21a` |
| `experiments/track_c/c10x_enginepath_selftest.py` | `1ba5289d047889417cba0a2135fcc12b3405ef056fe72d0435caf6290b7600dd` | `ba2133b18c84d8f092efe67f39cf8512b8e4ae6871a26684e7af7fb93f5eedcc` |
| `experiments/track_c/c10x_enginepath_telemetry_check.py` | `e95beb2cef310fa1050ccb4a2b60ac8224f493ea4d513d97868f3b9a9c99fe80` | `e95beb2cef310fa1050ccb4a2b60ac8224f493ea4d513d97868f3b9a9c99fe80` |
| `experiments/track_c/c10x_overtone_z.py` | `8b32ca840c1451624ba5f46143a6e65a03ae69e968dd0e6180d04fa5683dac42` | `8b32ca840c1451624ba5f46143a6e65a03ae69e968dd0e6180d04fa5683dac42` |

The unchanged prereg SHA-256 is `43a81103d68b953c2007e978b3ebecf11aadf66a7f121346047279845e8fc883`; C10Q context identity remains `c7dabbe7c25a7e58653621d9cc66e37b35c865ae09b73b6a96073a184c6c98da`. This revert changes no template source, contexts, frames, scientific thresholds or report-only fp32 eligibility rules.

Scope before production and after GREEN was checked in `after_review_mask_before/` and `after_review_mask_green/`. All **188 protected R5 files** match the expected Amendment P baseline; protected git diff exits **0**. Both complete selftest runs show empty before/after protected and other listing deltas. Relative to the original pre-build workspace snapshot, the after-GREEN listing has 7,856 entries versus 7,086; it classifies 1 authorized report, 1 program-supplied review, 2,907 observed/unattributed shared-workspace entries, and **0 unexplained protected changes**. This is a protected-scope claim, not a claim of global tree stability.

| Evidence artifact | SHA-256 |
|---|---|
| `/private/tmp/c10x_build/mask_revert_plan.md` | `4bdadef9d661a19b5336142a8cb380c445961c817ef0f62fdfeae5c0d9c1d3fc` |
| `/private/tmp/c10x_build/mask_revert_before.json` | `1f1e054f4c1c4e6cab5de147dca508fc37fc04f24048fe8c3be90bb935183c75` |
| `/private/tmp/c10x_build/mask_revert_red.log` | `2cbe4290588d3546593a06965e046309a4c4b602e6ed3b593d9c3c7f74fd4c77` |
| `/private/tmp/c10x_build/mask_revert_green.log` | `4e9580ada9dd7c3a2e10c016865a0aedf68a14101b164ed619790dd772171008` |
| `/private/tmp/c10x_build/after_review_mask_before/r2_sha256.json` | `a36710c1717929109d0e4d7978877cc8ea5c7eda29d6c8c8ddf2a0fae8cff1d4` |
| `/private/tmp/c10x_build/after_review_mask_green/summary.json` | `d9918bc885f88fda817422dd6ed6c7d9fbec42aa99d41d5de9a2aa807ca0b393` |
| `/private/tmp/c10x_build/after_review_mask_green/r5_sha256.json` | `c149cf6006ca120a28d3ec505c1768c10d2485082c8729e0f5640fe8c414d190` |
| `/private/tmp/c10x_build/after_review_mask_green/listing.json` | `c6b9c5de115e47d089bcbd148c2a5aaf76358ea8155169fc7b9c832b6925aca6` |
| `/private/tmp/c10x_build/after_review_mask_green/listing_difference.json` | `ceae8f806691aa9ce5478eddf1d1926463afdd2bc971d19873f521a0541ad4c7` |

After publication, `/private/tmp/c10x_build/after_review_mask_report/` repeats the protected-byte/listing check. `/private/tmp/c10x_build/mask_revert_receipt.json` binds the final report SHA-256, unchanged entire prior-report prefix, final six-source hashes, RED/GREEN logs and post-publication scope. Previous receipts and logs are retained.

Verification used tiny CPU stubs and AST-copied frozen functions under `/private/tmp`; no frozen harness module, transformers or datasets was imported. Live LAW#3/LAW#5/G8, model/MPS behavior, timing/resource feasibility and write-arm scientific results remain **UNVERIFIED**. No T8 live launch was run; the prior instruction to skip it remains binding. The first launch remains telemetry off and supervisor mediated. No experiment/GO output, prereg, engine/harness/config, ledger or git state was written by this revert.


## X2-vii halt probe

**DONE — diagnostic build only.** Added `experiments/track_c/c10x_x2_probe.py`; all **13 tiny CPU tests PASS in 0.866s**, exit 0. The existing **72-test model-free selftest PASS in 17.633s**, exit 0, with empty protected/other result-listing deltas. **No real model/tokenizer, MPS/GPU probe, covariance SVD or science run was executed. The historical halt's cause and magnitudes remain UNVERIFIED.** This is the requested measure-before-fix handoff: the driver, reader, harness, engine and prereg were not edited. The Amendment M/T11 fixes, safe device/dtype rewrites and completed mask revert remain in force.

The entire preceding report is retained byte for byte: **213,486 bytes**, SHA-256 `6dc3e916465db889848d6e41cf2be73d06010d4ece39117bb0d3d795ee2bcf71`. This section is an append; it does not replace any historical build or review evidence.

### Halt evidence and scope

`results/c10x_enginepath/run.json:1` records process 1, `status=HALTED`, `code="W0 X2-vii exact zero"`, the pinned context identity and the completed recipe-A records. `architecture_profile/c10x_halt_diagnostic_20261008T160002_759184Z.json:1` contains that W0 halt; `architecture_profile/c10x_halt_diagnostic_20261008T160004_981087Z.json:1` records the supervisor's subsequent `worker exit 1`. None includes the X2-vii residual/update magnitudes, the offending layer, a W0 snapshot or an inertness record. Their complete JSON was parsed for the input audit at `/private/tmp/c10x_build/x2_probe/halt_inputs.json`.

| Historical input | SHA-256, unchanged |
| --- | --- |
| `architecture_profile/c10x_halt_diagnostic_20261008T160002_759184Z.json` | `e01cdf8336656e11eed50b6a6bc2cc36e728f9209157da934ab6f9f5c35f464a` |
| `architecture_profile/c10x_halt_diagnostic_20261008T160004_981087Z.json` | `05740cfbe35af746023ce9072347e7a265804dcb0161d7d5666a3a6d58f56387` |
| `results/c10x_enginepath/run.json` | `a26d39cd9a32ec05174741d6d3ebfbf5a940565f81d3a76e1500e3b991d5b348` |

Prereg `docs/C10X_ENGINEPATH_PREREG.md:78` fixes the matching 24-row padded shape for X2-(iv)(a); `:81` requires exact-zero residuals/updates and pristine hashes and states that any non-zero (iv)(a) distance makes that exact-zero requirement unmeetable. The original gate checks actual residuals and captured updates before `pristine.verify("X2-vii exact zero")` (`c10x_enginepath_inertness.py:408–439`). This code order is evidence about the path to the W0 assertion; it is not a recovered measurement of the missing magnitudes.

One hypothesis justified for measurement is a signed-zero byte change: adding numeric zero can change `-0` to `+0`, while `count_nonzero` still reports zero and `I.tensor_sha` distinguishes raw bytes. The CPU signed-zero positive control demonstrates that possibility on the tiny fixture. **It does not establish the real halt's cause.** Reader/replay mismatch, wrong layer/column and conversion/observation effects also remain measurable alternatives; no tolerance or science path has been changed.

### Exact gate machinery and read-only boundary

The probe imports and calls **the existing** `A.recorded_contexts`, `A.pinned_contexts`, `A.canonical_read`, `A.batch_replay`, `A.fe_edit`, `I.relative_fixed`, `I.parity`, `I.active_null_structure`, `I.capture_updates`, `I.Pristine` and `I.tensor_sha`. It contains no copied solve equation and calls the original `fe_edit(..., mode="fe")` with the gate's real projectors and fresh zero caches (`c10x_x2_probe.py:142`, `:247`). `sys.settrace` is limited to the actual writer code object and its actual `torch.linalg.solve` source line (`:126`); it observes the writer's native `zs`, `cur`, `tgt`, `resid` and `rf` immediately before that solve. The strict gate helpers are used for diagnostic checks; a recorded mismatch does not update any acceptance, eligibility or scientific verdict.

Before any forward, raw template SHA, schema, canonical context SHA and the complete recorded-source identity are checked against `A.recorded_contexts` (`c10x_x2_probe.py:20`). The source is exactly the requested C10Q set: no alternate source, template sampling or seed-based regeneration. The artifact is `results/c10x_enginepath/context_templates.json`, raw SHA `0c6d90ee5e90e19c0174c6d2e085f3cf4454dfcd85c0f935fb1cc107afac2bfe`; canonical engine context SHA `eff10db6a89aabf7d67fa0c66e4cc1ac727b795c0bf756d3f8b53d0f6cd05aeb`; C10Q historical SHA `c7dabbe7c25a7e58653621d9cc66e37b35c865ae09b73b6a96073a184c6c98da`; flat-template SHA `d6c7c70026dced37bddc6adf316a3487d70227dae80a6e0ed5cdabe50caedfa0`. The amended prereg pin remains `43a81103d68b953c2007e978b3ebecf11aadf66a7f121346047279845e8fc883`.

X2-(iv)(a) repeats the original gate's two canonical reader calls on each of all three ordered 24-row arms and records per-layer reader/replay and reader-repeat distances in frozen CPU fp32 arithmetic, including the unchanged `REPLAY_FLOOR <= 1e-5` predicate. X2-vii then rebuilds A7's plain and block-4 identity replay exactly through `A.batch_replay`; input IDs, attention masks, padding side, subject indices and exact request identities are retained. Its checked-reader callback performs the independent same-batch replay before calling the writer's actual resolved engine reader, in the original order (`c10x_x2_probe.py:197–227`). Tokenizer mappings and historical scorer behavior are untouched.

To execute the writer while making **zero live-weight writes**, `ShadowModel.named_parameters` substitutes independent, detached, same-device/same-dtype clones of the five rewrite tensors; every forward and module lookup delegates to the pristine model (`c10x_x2_probe.py:97`). The unchanged writer's `+=` executes only on those copies. The copies are restored and hash-verified through the original `I.Pristine.cell`. The live five-weight hashes, all live parameter version counters and hook identities are checked before/after measurement and again after binding restoration (`:285–301`). An emergency live restore exists only for an unexpected integrity failure and refuses a successful measurement; ordinary execution makes no live restoration writes.

The first **shadow applied-weight byte change**, including a signed-zero change, is recorded as `gate_equivalence_cutoff_layer`; later layers have `gate_equivalent_before_write=false`. After that point their forwards remain pristine diagnostics, so the probe does not claim to reproduce the gate's altered subsequent state. Structural or residual violations are retained as diagnostic failures; they never relax exact-zero acceptance.

### JSON measurements and safe-copy audit

For each layer 4–8, the JSON contains 24 `request_rows`, each with actual gate-residual `max_abs_M_minus_cur` and `nonzero_elements`, plus `max_abs_update`. The latter explicitly refers to the **joint layer weight matrix** (`update_scope="joint_layer_weight_matrix"`), not an invented per-fact contribution. Actual update-matrix row maxima are separately recorded in `weight_matrix_row_max_abs_update`.

Each layer also records native solve-operand SHA-256s, complete pre-cast update SHA, native/CPU tensor dtype, device, shape, strides and storage offset; live versus shadow weight metadata; shadow before/after hashes, changed-byte count and signed-zero changes. The first row retains its exact request identity and the first eight values of independent observer, writer capture and identity target (all available values in the two-dimensional tiny fixture). The original full-vector `active_null_structure` comparison remains visible separately; a wrong-layer or wrong-column discrepancy is not hidden behind a norm.

`read_only_guard` uses `TorchDispatchMode` over all live parameter storages (`c10x_x2_probe.py:61`). It refuses mutable aliases and `out=` writes **before** dispatch. It also records actual MPS-to-CPU `_to_copy`/`copy_` transfers and refuses every dtype-changing one before executing it, including a nominally non-mutating transfer whose source aliases a live weight. This covers lowered combined `.to`, destination-tensor `.to`, `.type`, constructors and cross-dtype `copy_` forms. All reporting transfers use same-dtype `.cpu()` before CPU casts; no clone-first CPU-cast workaround is used. `mps_to_cpu_copies` records stage/source/device/dtype/offset and whether the transfer executed; `unsafe_mps_to_cpu_copies` explicitly isolates refused attempts. The program audit `results/mps_offset_conversion_audit.md` is hashed into runtime provenance. **Actual MPS copy observations are UNVERIFIED because only CPU tests ran.**

At runtime the probe writes only a fresh absolute `ROOT/results/c10x_x2_probe/<UTC>/`, rejects any existing path, and publishes `probe.json` exclusively; `probe.log` is in that same directory (`c10x_x2_probe.py:34`, `:587`). A filesystem audit hook refuses writes elsewhere and subprocess/network launch paths (`:304`, `:617`). Bytecode suppression precedes local imports; launch uses `-B`. The model loader is cache-only with offline library constants captured before the unchanged harness resets its environment flag. A missing cached model/covariance fails the diagnostic; cache population is not permitted. Telemetry must be unset and remains off. No real `results/c10x_x2_probe/` output was created during the build; tiny JSON round-trip publication occurred only in disposable `/private/tmp` fixtures.

The output records current source/model/environment/projector provenance. Historical `run.json` lacks W0 and model-identity records, so **historical W0/model equality cannot be independently established from that artifact**. Current pristine hash checks are not retroactive historical identity evidence.

### Test-first RED/GREEN and review

All Python used the existing venv, `-B`, one thread and serial CPU execution, with fixtures and logs below `/private/tmp/c10x_build`. No real science module, transformers or datasets was imported by either selftest. The original mandatory tests existed and failed against placeholders before the writer/guard implementation.

| Evidence file under `/private/tmp/c10x_build/x2_probe/` | Result |
| --- | --- |
| `red.log` | Seven initial groups, eight assertion failures, exit 1; no errors. Covers no live writes, wrong SHA before forwards, original-gate residual identity, signed-zero copy behavior, alias/out write refusal, unsafe-copy predicate and existing-output refusal. |
| `red_validated.log` | Eight groups, six assertion failures, exit 1, no errors; includes the perturbed native-operand control before writer implementation. |
| `red_boundaries_validated.log` | Eleven groups, six assertion failures, exit 1, no errors; adds dispatch-before-copy refusal, file-write policy and CLI template refusal before loading. |
| `red_floor_review.log` | Twelve groups, one assertion failure, exit 1; reviewer-proposed large-floor negative control fails before the threshold-label fix. |
| `red_json_roundtrip.log` | Thirteen groups, one assertion failure, exit 1; publishing exposed tuple/list normalization. The result is now converted to JSON-native values after final verification. |
| `green_final_after_cleanup.log` | Thirteen groups, PASS in 0.867s, exit 0, zero failures/errors; before final AST controls. |
| `red_ast_device_forms.log` | Thirteen groups, two assertion subcase failures, exit 1; positional CPU-device-plus-dtype and attribute CPU-tensor destination controls fail before AST tightening. |
| `green_sealed.log` | Thirteen groups, PASS in 0.866s, exit 0, zero failures/errors; sealed probe SHA below. |
| `regression72.log` | Existing seventy-two groups, PASS in 17.633s, exit 0, empty protected/other listing deltas, forbidden science imports absent. |

Two intermediate test drafts had construction errors (missing result-presence assertion and missing CLI flag declarations); `red_extended.log` and `red_boundaries.log` retain them. They were corrected and rerun as assertion-only RED before the respective implementation. Those drafts are not counted as valid RED evidence. Earlier GREEN logs are retained as intermediate source identities.

The exact and perturbed controls compare **all five actual writer operand SHA-256s** (`zs`, `cur`, `tgt`, `resid`, `rf`) with the original `I.observe_null_solve` gate, not an independent reimplementation of its subtraction. The exact case accepts zero residuals; the perturbed case changes layer-8 identity targets by 0.25, reproduces the same actual residual/solve operands, and the strict gate rejects it (`c10x_x2_probe.py:417`, `:442`). The no-write control checks byte hashes and `_version` for **every** live tiny-model parameter, hook and resolved reader identity, then verifies strict JSON round-trip equality (`:399`). The signed-zero control changes only shadow bytes and checks the equivalence cutoff (`:460`). Positive controls reject detached-alias and `out=` writes (`:474`), and a CPU-only dispatch control proves unsafe-copy classification raises before the actual conversion (`:495`). No MPS tensor is created. The probe's AST test rejects all combined/device-target/type/constructor/copy forms, including clone-first forms (`:538`), complementing unchanged test 72 on the established code paths.

Final probe GREEN output:

```text
test_cli_wrong_template_refuses_before_loader (__main__.selftest.<locals>.ProbeTests.test_cli_wrong_template_refuses_before_loader) ... ok
test_copy_guard_refuses_before_operator (__main__.selftest.<locals>.ProbeTests.test_copy_guard_refuses_before_operator) ... ok
test_existing_output_refused (__main__.selftest.<locals>.ProbeTests.test_existing_output_refused) ... ok
test_file_write_policy (__main__.selftest.<locals>.ProbeTests.test_file_write_policy) ... ok
test_guard_blocks_alias_and_out_writes_before_execution (__main__.selftest.<locals>.ProbeTests.test_guard_blocks_alias_and_out_writes_before_execution) ... ok
test_no_live_weight_writes (__main__.selftest.<locals>.ProbeTests.test_no_live_weight_writes) ... ok
test_nonzero_residual_matches_rejecting_gate (__main__.selftest.<locals>.ProbeTests.test_nonzero_residual_matches_rejecting_gate) ... ok
test_probe_bans_unsafe_copy_forms (__main__.selftest.<locals>.ProbeTests.test_probe_bans_unsafe_copy_forms) ... ok
test_residual_matches_actual_gate_fixed_input (__main__.selftest.<locals>.ProbeTests.test_residual_matches_actual_gate_fixed_input) ... ok
test_signed_zero_only_changes_shadow_bytes (__main__.selftest.<locals>.ProbeTests.test_signed_zero_only_changes_shadow_bytes) ... ok
test_unsafe_copy_predicate_without_mps (__main__.selftest.<locals>.ProbeTests.test_unsafe_copy_predicate_without_mps) ... ok
test_wrong_template_hash_refuses_before_forward (__main__.selftest.<locals>.ProbeTests.test_wrong_template_hash_refuses_before_forward) ... ok
test_x2_iv_floor_threshold_matches_gate (__main__.selftest.<locals>.ProbeTests.test_x2_iv_floor_threshold_matches_gate) ... ok

----------------------------------------------------------------------
Ran 13 tests in 0.866s

OK
CPU ONLY; no frozen harness/transformers/datasets imported
```

Existing full selftest GREEN output:

```text
test_admitted_process_pair_and_p2_gate (__main__.FileAdmissionTests.test_admitted_process_pair_and_p2_gate) ... ok
test_amendment_p_digest_refusals (__main__.FileAdmissionTests.test_amendment_p_digest_refusals) ... ok
test_amendment_p_prereg_pin (__main__.FileAdmissionTests.test_amendment_p_prereg_pin) ... ok
test_answer_audit_uses_runtime_recipe_order (__main__.FileAdmissionTests.test_answer_audit_uses_runtime_recipe_order) ... ok
test_complete_stub_run_persists_every_record (__main__.FileAdmissionTests.test_complete_stub_run_persists_every_record) ... ok
test_context_binding_enter_failure_restores (__main__.FileAdmissionTests.test_context_binding_enter_failure_restores) ... ok
test_deadline_completion_and_previous_overhead (__main__.FileAdmissionTests.test_deadline_completion_and_previous_overhead) ... ok
test_detailed_admission_negative_controls (__main__.FileAdmissionTests.test_detailed_admission_negative_controls) ... ok
test_direct_shell_launchers_are_executable_in_git (__main__.FileAdmissionTests.test_direct_shell_launchers_are_executable_in_git) ... DIRECT SHELL ENTRY POINTS: none; all three supervised commands use sys.executable
ok
test_disable_cutoff_never_excuses_earlier_omissions (__main__.FileAdmissionTests.test_disable_cutoff_never_excuses_earlier_omissions) ... ok
test_disable_marker_records_failed_answer_cutoff (__main__.FileAdmissionTests.test_disable_marker_records_failed_answer_cutoff) ... ok
test_every_science_record_roundtrip_and_reader_audit (__main__.FileAdmissionTests.test_every_science_record_roundtrip_and_reader_audit) ... ok
test_fp32_overflow_capture_and_parity_remain_report_only (__main__.FileAdmissionTests.test_fp32_overflow_capture_and_parity_remain_report_only) ... ok
test_frozen_scorer_forwards_have_no_injected_kwargs (__main__.FileAdmissionTests.test_frozen_scorer_forwards_have_no_injected_kwargs) ... ok
test_late_supervisor_persistence_is_unreadable (__main__.FileAdmissionTests.test_late_supervisor_persistence_is_unreadable) ... ok
test_missing_inertness_evidence_is_refused (__main__.FileAdmissionTests.test_missing_inertness_evidence_is_refused) ... ok
test_no_combined_device_dtype_conversions (__main__.FileAdmissionTests.test_no_combined_device_dtype_conversions) ... ok
test_pinned_contexts_never_sample (__main__.FileAdmissionTests.test_pinned_contexts_never_sample) ... ok
test_pinned_processes_and_halted_context_identity (__main__.FileAdmissionTests.test_pinned_processes_and_halted_context_identity) ... ok
test_post_audit_blocks_are_killed_by_final_deadline (__main__.FileAdmissionTests.test_post_audit_blocks_are_killed_by_final_deadline) ... ok
test_post_audit_budget_and_disabled_disposition (__main__.FileAdmissionTests.test_post_audit_budget_and_disabled_disposition) ... ok
test_post_audit_rejects_contradictory_receipts (__main__.FileAdmissionTests.test_post_audit_rejects_contradictory_receipts) ... ok
test_post_audit_startup_consumes_remaining_budget (__main__.FileAdmissionTests.test_post_audit_startup_consumes_remaining_budget) ... ok
test_reader_publishes_invalid_with_exit_zero (__main__.FileAdmissionTests.test_reader_publishes_invalid_with_exit_zero) ... ok
test_recipe_fp32_overflow_does_not_halt_or_change_labels (__main__.FileAdmissionTests.test_recipe_fp32_overflow_does_not_halt_or_change_labels) ... ok
test_script_alias_and_preflight_refusal_in_isolated_child (__main__.FileAdmissionTests.test_script_alias_and_preflight_refusal_in_isolated_child) ... ok
test_supervisor_fail_closed_and_combining_output_path (__main__.FileAdmissionTests.test_supervisor_fail_closed_and_combining_output_path) ... ok
test_tagged_fp32_diagnostics_preserve_file_admission (__main__.FileAdmissionTests.test_tagged_fp32_diagnostics_preserve_file_admission) ... ok
test_tokenizer_forwards_preserve_attention_mask (__main__.FileAdmissionTests.test_tokenizer_forwards_preserve_attention_mask) ... ok
test_actual_fe_writes_and_null_solve_observer (__main__.IntegrationTests.test_actual_fe_writes_and_null_solve_observer) ... ok
test_actual_singleton_reduction_and_resolved_capture (__main__.IntegrationTests.test_actual_singleton_reduction_and_resolved_capture) ... ok
test_projection_uses_remaining_units_and_setup_clock (__main__.IntegrationTests.test_projection_uses_remaining_units_and_setup_clock) ... ok
test_solver_masked_gradient_clip_filter_and_tie (__main__.IntegrationTests.test_solver_masked_gradient_clip_filter_and_tie) ... ok
test_telemetry_recipe_records_and_counts_equal (__main__.IntegrationTests.test_telemetry_recipe_records_and_counts_equal) ... ok
test_telemetry_valid_admission_and_runner_no_writes (__main__.IntegrationTests.test_telemetry_valid_admission_and_runner_no_writes) ... ok
test_three_recipe_telemetry_probe_and_file_equality (__main__.IntegrationTests.test_three_recipe_telemetry_probe_and_file_equality) ... ok
test_reader_control_boundaries (__main__.ReaderTests.test_reader_control_boundaries) ... ok
test_reader_count_classes (__main__.ReaderTests.test_reader_count_classes) ... ok
test_reader_flags_denominators_nulls (__main__.ReaderTests.test_reader_flags_denominators_nulls) ... ok
test_reader_interpretation_and_null_table (__main__.ReaderTests.test_reader_interpretation_and_null_table) ... ok
test_reader_law3_boundaries (__main__.ReaderTests.test_reader_law3_boundaries) ... ok
test_reader_locality_boundaries (__main__.ReaderTests.test_reader_locality_boundaries) ... ok
test_reader_process_combination (__main__.ReaderTests.test_reader_process_combination) ... ok
test_reader_qualifier_boundaries (__main__.ReaderTests.test_reader_qualifier_boundaries) ... ok
test_reader_replication (__main__.ReaderTests.test_reader_replication) ... ok
test_reader_validity (__main__.ReaderTests.test_reader_validity) ... ok
test_active_null_negative_controls (__main__.SeamTests.test_active_null_negative_controls) ... ok
test_baseline_miss_stops_candidates (__main__.SeamTests.test_baseline_miss_stops_candidates) ... ok
test_capture_bindings_identity_attribution (__main__.SeamTests.test_capture_bindings_identity_attribution) ... ok
test_dispatch_call_time_flag (__main__.SeamTests.test_dispatch_call_time_flag) ... ok
test_fe_ast_three_changes (__main__.SeamTests.test_fe_ast_three_changes) ... ok
test_fe_modes_and_keys (__main__.SeamTests.test_fe_modes_and_keys) ... ok
test_float64_dense_reference (__main__.SeamTests.test_float64_dense_reference) ... ok
test_independent_full_vocabulary_audit (__main__.SeamTests.test_independent_full_vocabulary_audit) ... ok
test_knobs_and_frame_subjects (__main__.SeamTests.test_knobs_and_frame_subjects) ... ok
test_launch_refusals (__main__.SeamTests.test_launch_refusals) ... ok
test_pristine_hash_restore_hooks (__main__.SeamTests.test_pristine_hash_restore_hooks) ... ok
test_process2_requires_eligibility (__main__.SeamTests.test_process2_requires_eligibility) ... ok
test_recipe_states_counters (__main__.SeamTests.test_recipe_states_counters) ... ok
test_solver_ast_and_gradients (__main__.SeamTests.test_solver_ast_and_gradients) ... ok
test_tolerance_and_finiteness (__main__.SeamTests.test_tolerance_and_finiteness) ... ok
test_watchdog_and_projection (__main__.SeamTests.test_watchdog_and_projection) ... ok
test_frozen_bytes_and_imports (__main__.TelemetryTests.test_frozen_bytes_and_imports) ... IMPORT GUARD PASS: c10e_bandknob, transformers, datasets absent
ok
test_isolation_positive_control_children_meta (__main__.TelemetryTests.test_isolation_positive_control_children_meta) ... ok
test_post_run_answer_audit (__main__.TelemetryTests.test_post_run_answer_audit) ... ok
test_strict_json_roundtrips (__main__.TelemetryTests.test_strict_json_roundtrips) ... ok
test_telemetry_code_path_equality (__main__.TelemetryTests.test_telemetry_code_path_equality) ... ok
test_telemetry_failure_boundaries (__main__.TelemetryTests.test_telemetry_failure_boundaries) ... ok
test_telemetry_inertness_schedule (__main__.TelemetryTests.test_telemetry_inertness_schedule) ... ok
test_telemetry_line_volume (__main__.TelemetryTests.test_telemetry_line_volume) ... ok
test_telemetry_state_unchanged (__main__.TelemetryTests.test_telemetry_state_unchanged) ... ok
test_telemetry_switch_admission (__main__.TelemetryTests.test_telemetry_switch_admission) ... ok

----------------------------------------------------------------------
Ran 72 tests in 17.633s

OK
LISTING: attributed-protected changes = {}
LISTING: observed/unattributed other changes = {}
SYS.MODULES PASS: c10e_bandknob/transformers/datasets absent
```

The advisor-review skill was applied before the initial tests. `tools/claude_advisor.sh` refused the call (exit 3): `FATAL: Claude CLI is not logged in.` A cheap direct auth probe also returned `loggedIn=false`; no successful out-of-family review is claimed. Its log is retained at `/private/tmp/c10x_build/x2_probe/advisor_design.log`. The authorized fresh read-only GPT-family fallback is **weaker independence**. Its initial FIX-FIRST recommendations were accepted: byte-based equivalence cutoff, explicit request/update row domains and unsafe-copy refusal before dispatch. Its implementation review also caught the floor-label and early-bytecode gaps; both were fixed. Its production-review confirmation, before final test-only AST strengthening, is preserved at `/private/tmp/c10x_build/x2_probe/final_fallback_review.txt`:

```text
PROCEED. Verified final SHA-256:

b78c2f2892408b6fd9619066ca98418fb81e33256b07fd70f7d5cbf35a2e5223

Live/shadow metadata is recorded at experiments/track_c/c10x_x2_probe.py:262–263; JSON conversion now follows final verification at :285–301.

The cleanup log records 13 CPU tests PASS in 0.867s (/private/tmp/c10x_build/x2_probe/green_final_after_cleanup.log:16–19).

Real-model/MPS behavior remains UNVERIFIED. Same-family fallback; weaker independence. No tests, Python or edits performed by this reviewer.
```

The final test-only AST refinement also rejects positional `torch.device("cpu")` plus dtype and attribute CPU-tensor destinations. Safe CPU-then-dtype, dtype-then-CPU and same-dtype CPU copies remain admitted. The sealed source was read-only re-reviewed with **PROCEED**, weaker same-family independence; exact confirmation is `/private/tmp/c10x_build/x2_probe/final_ast_review.md`:

```text
**PROCEED.** Sealed source SHA verified:

`fd20ac97cf24ff57624b712a060cc3ad9422d24db3b2a29e63f7bf7e89149010`

The expanded AST controls match the stated unsafe and safe forms (`experiments/track_c/c10x_x2_probe.py:538–573`). The latest log records **13 CPU groups PASS in 0.866s** (`/private/tmp/c10x_build/x2_probe/green_sealed.log:16–19`).

Real-model/MPS behavior remains **UNVERIFIED**. Read-only confirmation; no tests, Python or edits performed.
```

### Final identities and protected-scope verification

| File | SHA-256 |
| --- | --- |
| `experiments/track_c/c10x_x2_probe.py` — new | `fd20ac97cf24ff57624b712a060cc3ad9422d24db3b2a29e63f7bf7e89149010` |
| `docs/C10X_ENGINEPATH_PREREG.md` — unchanged | `43a81103d68b953c2007e978b3ebecf11aadf66a7f121346047279845e8fc883` |
| `experiments/track_c/c10x_enginepath_arms.py` — unchanged | `eea47ea72d071c6e9dfd5b301dfa8073c50aa0e3d02149de9660aae837f182db` |
| `experiments/track_c/c10x_enginepath_inertness.py` — unchanged | `c0c19b97cfeac03a5c12176e33b63a10d06489ca56f7b365a6e03ef1e4ba56e9` |
| `experiments/track_c/c10x_enginepath_read.py` — unchanged | `0c22b6b222e37b2d1a81ed649836f8fb6297a8440d0b2f833389cba1a25ff21a` |
| `experiments/track_c/c10x_enginepath_selftest.py` — unchanged | `ba2133b18c84d8f092efe67f39cf8512b8e4ae6871a26684e7af7fb93f5eedcc` |
| `experiments/track_c/c10x_enginepath_telemetry_check.py` — unchanged | `e95beb2cef310fa1050ccb4a2b60ac8224f493ea4d513d97868f3b9a9c99fe80` |
| `experiments/track_c/c10x_overtone_z.py` — unchanged | `8b32ca840c1451624ba5f46143a6e65a03ae69e968dd0e6180d04fa5683dac42` |

All **188 protected R5 files** match the current Amendment P baseline, and all nine current-task held files match their before hashes. Read-only protected `git diff --exit-code` exits 0. No git mutation or commit occurred. The results/architecture listing had 7,891 entries before and before report append; no C10X protected listing changed. One observed/unattributed other directory-metadata change (`results/labviz/site/runs`) is retained in `listing_delta_before_report.json`; no global shared-tree stability claim is made. The final check permits only the authorized append to this report. No historical result, diagnostic, source file, engine file or prereg bytes were repaired or rewritten.

This launch executes Python directly and adds no shell wrapper; unchanged executable-entrypoint and git-mode regression checks pass in the seventy-two-test suite. The real-model path, model/covariance cache availability, MPS guard routing and actual timing remain UNVERIFIED. CPU plumbing PASS does not lift the HALT, qualify a write arm, relax LAW#5 or establish a null/mechanism result.

### Exact launch command — NOT RUN

Run from the program's separately scheduled measurement window. This loads the same frozen harness/model/device as the gate. It has **not** been executed under this build's no-GPU instruction. The default output is an absolute, microsecond-UTC directory under `results/c10x_x2_probe/`; reuse is refused. An optional `--out` may only name a fresh absolute directory of that same form.

```sh
/usr/bin/env -u C10X_TELEMETRY \
  LLMDB_ROOT='/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a' \
  PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  '/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python' -B \
  '/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_x2_probe.py' \
  --source-run '/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/c10x_enginepath/run.json' \
  --templates '/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/c10x_enginepath/context_templates.json' \
  --templates-sha256 0c6d90ee5e90e19c0174c6d2e085f3cf4454dfcd85c0f935fb1cc107afac2bfe
```

The resulting paths are `results/c10x_x2_probe/<UTC>/probe.json` and `probe.log`. Runtime status is `MEASURED` for a completed diagnostic or `INCOMPLETE` with an explicit error; neither changes science acceptance. An unsafe copy aborts before execution and records the attempted transfer. No GPU launch, rerun authorization or scientific fix is implied by this command listing.

Evidence manifest: `/private/tmp/c10x_build/x2_probe/evidence_manifest.json`, SHA-256 `7e3ed73c81f824aa7e49da93f6d22ab844946df7e36f4f6ab526bd5ab8b0a910`. Final report/probe/protected-file receipt: `/private/tmp/c10x_build/x2_probe/final_receipt.json`.


## X2 probe file-policy correction

**DONE — test-first CPU policy repair.** Final probe SHA-256 `23bdf070c66f8af02bb4d38d22eaecdfffa04782339f500ce1572080d6a2b614`. The sealed probe selftest passes **17 groups in 1.078s**; the new real cached tokenizer/config CPU test passes **1 test in 2.134s**; the existing C10X model-free suite passes **72 tests in 20.544s**, all exit 0. The failed `results/c10x_x2_probe/20261008T171001_323402Z/` is preserved. **No model weights were loaded, no MPS/GPU measurement was run, and the missing historical X2 magnitudes/cause remain UNVERIFIED.**

This append replaces the earlier probe section's description of an all-output-only filesystem policy. The preceding **243,428 bytes** remain byte for byte, SHA-256 `f7411306e41a207128bbd7cdc59326c04224e15876e7dddfa48f9ed025fee6a9`. Earlier tests and policy descriptions remain historical evidence for their recorded source hashes.

### Failure and corrected scope

The program's failed `probe.json` has `status=INCOMPLETE` and `PermissionError: PROBE_READ_ONLY open ['/dev/null']`. Its SHA-256 remains `45b1fa22f234a7169664d562aab703cae82c2d9ddbc4c71113dd34c829443064`; the empty `probe.log` remains `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. The prior probe source was `fd20ac97cf24ff57624b712a060cc3ad9422d24db3b2a29e63f7bf7e89149010`. This startup refusal supplied no X2 measurement.

`c10x_x2_probe.py:306` now records protected lexical and resolved project trees: `ROOT/results` with the current output-directory exception, `ROOT/architecture_profile`, `ROOT/experiments`, `ROOT/tools`, `ROOT/docs`, `ROOT/CORPUS`, `ROOT/memit_dry_run/memit`, and `ROOT/covariance_caches`. It also protects every cached HF repository's snapshot tree under `ROOT/hf_cache/hub/*/snapshots` and the exact resolved files those snapshots reference. Cache metadata is collected through directory/stat/readlink operations; weight contents are not read for policy construction. The actual `hf_cache` and covariance symlink targets receive the same protection.

The policy (`:330`) refuses protected writes, creation, rename/link destinations, removal, chmod/chown, truncate and utime. Rename checks both endpoints and rejects moving directories containing protected trees or snapshot targets. Snapshot symlink entries and their referenced blob files are protected; an unrelated blob or `.incomplete` file remains writable. An external runtime symlink may point to protected data and may be removed, while opening that protected target for mutation is refused. A symlink inside the allowed output directory does not grant permission to mutate another protected path. Physical resolution precedes lexical `..` normalization, preserving the actual target of a directory-symlink traversal.

Unlisted paths are allowed, including `os.devnull`, ordinary home-cache and temporary directories, HF locks/refs outside snapshots, unreferenced blobs and incomplete downloads. JSON/log publication still uses the same exclusive fresh absolute `results/c10x_x2_probe/<UTC>/` output directory; existing output directories are refused.

Descriptor mutations are resolved with macOS `F_GETPATH` (`:320`). The observed CPython `open` audit event omits `dir_fd`; `install_file_policy` (`:370`) therefore supplies the actual absolute descriptor-relative target to `os.open`, so the audit hook checks the same target the operation uses. Tests cover both a refused protected target and allowed external runtime targets from the protected engine cwd, using string, bytes and Path arguments.

The real cache test exposed three policy refusals that dependencies caught internally: `urllib3/util/connection.py`'s IPv6 availability bind check, and `platform.py`'s processor/architecture subprocess probes. `socket.bind` and `subprocess.Popen` are now allowed as the program's conditional instruction requires. Unused `socket.connect` and `os.system` refusals remain. The test records policy exceptions before re-raising them and requires an empty record, preventing a swallowed startup refusal from passing unnoticed. Traces are in `/private/tmp/c10x_build/x2_probe_policy_fix/red_startup_traced.log`.

### Test-first evidence

Tests and evidence are in `/private/tmp/c10x_build/x2_probe_policy_fix/`; all Python runs were serial, with CPU thread limits and bytecode disabled. Test-first source snapshot SHA-256 was `97e1f250f6bcada8de7cf9882a1179fd5e53b8f12dab1c45a1d3ba2225d7ceec`. Extracting the unchanged audit installation into `install_file_policy` preceded RED; the original policy was still in force.

| Evidence | Observed result |
| --- | --- |
| `red_core.log` | Exit 1: integer descriptor write-open not refused; allowed `/dev/null` write refused. All protected-path negative controls passed. |
| `red_cache.log` | Exit 1: explicit `CACHE_LOAD_FALSE_REFUSAL PROBE_READ_ONLY open ['/dev/null']`. |
| `event_shapes.json`, `red_dirfd.log` | `open` lacks `dir_fd`; after narrowing the policy, a protected descriptor-relative open bypassed it. Exit 1. |
| `red_subprocess.log`, `red_startup_traced.log` | Exit 1: cache/metadata startup had three swallowed policy refusals, recorded before any restriction was removed. |
| `red_runtime_dirfd.log` | Exit 1: external runtime descriptor open falsely refused from protected engine cwd; reviewer finding reproduced before the wrapper correction. |
| `red_alias_traversal.log` | Exit 1: symlink-directory plus `..` path reached protected data without refusal; physical-resolution order corrected after RED. |
| `green_sealed_core.log` | Exit 0: 17 groups PASS, including all existing scientific/weight negative controls and new filesystem controls. |
| `green_sealed_cache.log` | Exit 0: real cached config/tokenizer CPU test PASS with no caught policy refusals. |
| `green_sealed_full_selftest.log` | Exit 0: 72 existing C10X tests PASS; both listing deltas empty; frozen harness/transformers/datasets absent in this separate model-free process. |

One intermediate cache-test observation (`red_startup_subprocess.log`) incorrectly expected Python's audit hook to observe the Rust tokenizer's native `tokenizer.json` read. It is retained as a test-observation correction and is **not** counted as policy RED evidence. The corrected positive controls observe the Python `config.json` and `tokenizer_config.json` reads and assert tokenizer output is nonempty CPU tensors within the configured vocabulary. The tokenizer/config API calls use `local_files_only=True`, the actual `ROOT/hf_cache/hub` cache, and revision `3aab1f1954e9cc14eb9509a215f9e5ca08227a9b`. Small snapshot JSON hashes match before/after. No model loader is invoked. Audited weight-shard reads are refused; Python audit observations alone do not establish absence of native I/O.

The real-cache test is a separate `--cache-selftest` mode (`c10x_x2_probe.py:760`). The original model-free suite's import boundary remains unchanged. Exact CPU verification commands:

```sh
/usr/bin/env TMPDIR=/private/tmp/c10x_build PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  '/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python' -B '/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_x2_probe.py' --selftest
/usr/bin/env TMPDIR=/private/tmp/c10x_build PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  '/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python' -B '/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_x2_probe.py' --cache-selftest
/usr/bin/env TMPDIR=/private/tmp/c10x_build PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  '/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python' -B '/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py'
```

Sealed output excerpts:

```text
Ran 17 tests in 1.078s
OK
CPU ONLY; no frozen harness/transformers/datasets imported

Ran 1 test in 2.134s
OK
REAL CACHED TOKENIZER/CONFIG CPU ONLY; no model loader invoked; no audited weight-shard reads

Ran 72 tests in 20.544s
OK
LISTING: attributed-protected changes = {}
LISTING: observed/unattributed other changes = {}
SYS.MODULES PASS: c10e_bandknob/transformers/datasets absent
```

### Scope, review and sealed hashes

Only the probe and this report were edited in the real tree. All **188 R5 frozen-file hashes** match the pre-fix baseline. The six C10X driver/reader/inertness/selftest/telemetry/overtone modules, prereg, original HALTED run, pinned template artifact and failed probe JSON/log hashes match. The **11 pre-existing scientific/helper AST hashes** match, including `probe`, `read_only_guard`, `ShadowModel`, `trace_solve`, `gate_call`, `load_templates`, `fresh_output`, `distance`, `tensor_meta`, `storage_key` and `unsafe_copy`. The parameter-storage `TorchDispatchMode` guard, template/weight checks, gate machinery and safe MPS-copy policy were not changed. Amendment M/T11, Amendment P and the mask revert remain intact. The prereg SHA remains `43a81103d68b953c2007e978b3ebecf11aadf66a7f121346047279845e8fc883`; the template file SHA remains `0c6d90ee5e90e19c0174c6d2e085f3cf4454dfcd85c0f935fb1cc107afac2bfe`.

[advisor-review](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.codex/skills/advisor-review/SKILL.md) used a fresh read-only `/root/x2_policy_refute` fallback after the local Claude auth probe returned exit 1, `loggedIn=false`, `authMethod=none`. The reviewer found the allowed-direction descriptor false refusal, which was fixed after RED, and then returned **PROCEED for the sealed source, no blocking findings**. This same-family fallback has weaker independence. The review covers CPU policy repair; full-weight loading, MPS behavior and native/child-process I/O protection remain UNVERIFIED. No GPU measurement or scientific verdict is inferred.

| Sealed artifact | SHA-256 |
| --- | --- |
| `experiments/track_c/c10x_x2_probe.py` | `23bdf070c66f8af02bb4d38d22eaecdfffa04782339f500ce1572080d6a2b614` |
| `green_sealed_core.log` | `abe9600faa39f0531d81dce628c98cdd37a6896c7123c76d3ff6327b134d7f40` |
| `green_sealed_cache.log` | `1e5f87776a2b5a086771ce1a492cf1236bd3852b8d666dd3f04e8421e082f64b` |
| `green_sealed_full_selftest.log` | `4cb43139dd9fb8e1639c9eba9182b65b07101a3ef43aff20992b66ff581994d1` |
| `final_review.md` | `b91194ad50863c0e2b15aa566662ac93baf1f96a05746b3033c3948d6d467869` |
| `sealed_evidence.json` | `7eb5b6c35fcb121e6fea572fa83bca751448d364f0d41daf2d43640d0c4d0ecd` |

### Fresh probe launch command — NOT RUN

The program may use the same launch command in its separately scheduled measurement window. Omitting `--out` selects a new absolute microsecond-UTC directory, preserving the failed `20261008T171001_323402Z` output. This command was **not run** during the repair:

```sh
/usr/bin/env -u C10X_TELEMETRY \
  LLMDB_ROOT='/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a' \
  PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  '/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python' -B \
  '/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_x2_probe.py' \
  --source-run '/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/c10x_enginepath/run.json' \
  --templates '/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/c10x_enginepath/context_templates.json' \
  --templates-sha256 0c6d90ee5e90e19c0174c6d2e085f3cf4454dfcd85c0f935fb1cc107afac2bfe
```

Final append/source/protected-file receipt: `/private/tmp/c10x_build/x2_probe_policy_fix/final_receipt.json`.


## Amendment Z — D-C10x-signedzero implementation (2026-10-08T19:16:51.477897+00:00)

**Build status: PASS, CPU code validation only.** Implemented the program-authorized §13 exactly after reading :637–802 in full and both `results/c10x_signedzero_amend_astra{,_delta}.md` reviews. The authoritative delta review is GO. Model and effort for this Codex execution: **UNVERIFIABLE**. Current frozen prereg SHA-256: `d3dfdc8bd8a9c04894b63da9b51ead164e7667e40d8f08b29b11606078f92899`. Its historical pre-§13 identity at prereg :642 remains historical data. No prereg text was edited.

### Predicate and diagnostic changes

Only the in-cell X2-(vii) weight predicate changes. `x2_weight_measurements` (`c10x_enginepath_inertness.py:95`) first collects all five live rewrite tensors with native-dtype `.detach().cpu()` and their pristine CPU snapshots, before restoration or the first weight-predicate failure. `x2_weight_identity` (`c10x_enginepath_inertness.py:123`) checks shape and `live.dtype == snap.dtype == torch.float16` as separate predicates, then CPU `torch.equal`. It has no tolerance. A failure is `X2-vii WEIGHT_VALUE <layer>` and names the offending layer (prereg :705–712).

Each layer's `weight_diagnostics_report_only` object is labelled `report_only: true` and carries `pristine_sha256`, `after_sha256`, `raw_bytes_identical`, `changed_bytes`, `changed_elements`, and `signed_zero_changes` (prereg :714–721). Hashes use the unchanged `tensor_sha`. `changed_elements` compares **contiguous CPU int16 views** of the binary16 bits, so a signed-zero flip counts even though float `!=` finds no change. `signed_zero_changes` uses both values zero and differing `signbit`, without direction splitting. Shape/dtype and maximum absolute value-difference measurements are included in that same report-only object. Incompatible shape/dtype has explicitly unavailable counts (`null` plus a reason); nonfinite diagnostic magnitudes use tagged JSON such as `{"nonfinite":"nan"}`.

No diagnostic field supplies a gate or a consistency veto. The reader retains the mandatory `weight_identity: true`, update-zero, residual-zero and all genuine W0 checks; it removes only the obsolete `X2-vii exact zero` checkpoint requirement (`c10x_enginepath_read.py:983`). Its narrow null exception covers only `inertness.X2-vii.weight_diagnostics_report_only`, including the manifest prefix (`c10x_enginepath_read.py:111`). Tests perturb hashes and counts, make them inconsistent or unavailable, and add a tagged nonfinite magnitude without changing acceptance, labels, qualifiers, eligibility or interpretation. False weight identity and altered before/after W0 hashes still fail.

The existing `NULL_NONZERO_UPDATE` predicate remains before the weight comparison. The real writer, observer's full-vector/request/column checks, actual residual predicates, negative controls, X2-(iv) distance/floor rules, all tolerances, and G8 remain unchanged (prereg :723–734). All `Pristine` methods, including native byte hashing/restoration and the before/after X2-vii cell checks, are AST-identical. T8's before/after byte identity and the T4 statement-identical scorer remain unchanged. Amendment M report-only diagnostics, T11 cutoff, Amendment P template pinning, mask revert and MPS copy corrections remain in place; their tests still pass. There is no new MPS dtype-changing copy: native CPU copies precede any CPU diagnostic cast.

For X2-vii halts, residual/update maxima and nonzero-element counts are captured alongside all five weight reports and observer differences. `x2_primary_halt` (`c10x_enginepath_inertness.py:136`) preserves the primary measured halt when strict restoration also raises, while recording secondary cleanup failures. The driver's existing HALT path copies those measurements into both `run.json` and the fresh diagnostic (`c10x_enginepath_arms.py:1112`). A HALT from the cell's exit verification retains the already measured pre-restoration hashes/counts and all captured updates. It does not replace them with restored weights.

**Bounded cleanup behavior:** injected incompatible dtype/shape may still make the final strict restoration raise after the primary HALT has been persisted. The process remains fail-closed. This build does not claim graceful cleanup/return for that corruption case, and does not weaken W0 to obtain it.

### Numbered regression mapping

Tests were added before changing production modules. Their gate fixture compiles the existing production X2-vii AST block from `run_checks`; it does not copy or reimplement the predicates. The unchanged real `A.fe_edit` performs the identity write on a CPU fp16 tiny model, with 24 canonical requests. The tiny fixture's input cast permits fp16 execution; it changes no production forward/scorer.

| # | Binding rule | Test and source | Implementation seam |
| --- | --- | --- | --- |
| 1 | §13 Z2–Z3, Z6(a); prereg :705–721, :786 | `test_signed_zero_write_passes_and_counts_binary16_bits` (`c10x_enginepath_selftest.py:1777`) | `c10x_enginepath_inertness.py:95, c10x_enginepath_inertness.py:123` |
| 2 | §13 Z2(3), Z6(b); :708–712, :787 | `test_one_ulp_value_change_halts_with_all_layer_measurements` (`c10x_enginepath_selftest.py:1793`) | `c10x_enginepath_inertness.py:123` |
| 3 | §13 Z2(3), Z6(c); :708–712, :788 | `test_nan_value_halts` (`c10x_enginepath_selftest.py:1801`) | `c10x_enginepath_inertness.py:123` |
| 4 | §13 Z2(1), Z6(d); :706–707, :789 | `test_equal_values_wrong_dtype_halt` (`c10x_enginepath_selftest.py:1805`) | `c10x_enginepath_inertness.py:123` |
| 5 | §13 Z2(1), Z6(e); :706–707, :790 | `test_wrong_shape_halts` (`c10x_enginepath_selftest.py:1811`) | `c10x_enginepath_inertness.py:123, c10x_enginepath_inertness.py:136` |
| 6 | §13 Z4, Z6(f); :723–732, :791 | `test_nonzero_update_halts_before_weight_comparison` (`c10x_enginepath_selftest.py:1816`) | `c10x_enginepath_inertness.py:382` |
| 7 | §13 Z1, Z4, Z6(g); :691–703, :731, :792 | `test_w0_byte_identity_stays_strict_before_and_after_null_cell` (`c10x_enginepath_selftest.py:1822`) | `c10x_enginepath_inertness.py:169` |
| 8 | §13 Z2(4), Z3; :712–721; measured values in HALT | `test_driver_halt_serializes_measured_x2_values` (`c10x_enginepath_selftest.py:1845`) | `c10x_enginepath_arms.py:1112` |
| 9 | §13 Z3; :714–721; pre-restoration evidence survives exit HALT | `test_after_cell_halt_keeps_pre_restoration_measurements` (`c10x_enginepath_selftest.py:1830`) | `c10x_enginepath_inertness.py:382` |
| 10 | §13 Z3 report-only; :714–721; acceptance/eligibility/verdict unchanged | `test_signed_zero_reader_keeps_reports_out_of_admission` (`c10x_enginepath_selftest.py:919`) | `c10x_enginepath_read.py:111, c10x_enginepath_read.py:983` |
| 11 | Program-supplied replacement SHA; §13 Z6 :784–797 | `test_amendment_z_prereg_pin` (`c10x_enginepath_selftest.py:1861`) | `c10x_enginepath_arms.py:29, c10x_enginepath_read.py:16; synthetic fixture and R5 expected pin` |

The signed-zero positive control measures one -0 → +0 bit-pattern/byte change per layer, five layers total; each layer reports `changed_bytes=1`, `changed_elements=1`, `signed_zero_changes=1`, unequal raw hashes, and exact value identity. Float `!=` counts zero changes. Residuals and updates remain exactly zero. A one-ULP change at layer 6, a NaN at layer 5, equal-valued fp32 at layer 4, and a shape mismatch at layer 8 all HALT. A nonzero update HALTs at `NULL_NONZERO_UPDATE` before the weight comparison. This synthetic regression instantiates the measured mechanism; it does not claim to reproduce the historical layer-4 count of 21.

### RED before implementation

Evidence directory: `/private/tmp/c10x_build/signedzero_amendment/`. Initial production sources are copied there by basename and hashed in `before.json`. Only tests/the tiny fixture were changed before this first run. From `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c`:

```sh
/usr/bin/env TMPDIR=/private/tmp/c10x_build PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 '/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python' -B -m unittest -v \
  c10x_enginepath_selftest.SignedZeroTests \
  c10x_enginepath_selftest.FileAdmissionTests.test_signed_zero_reader_keeps_reports_out_of_admission
```

Exit **1**, 10 tests, 5 failures and 4 errors. The scientific positive-control RED is the old `W0 X2-vii exact zero` halt after the actual zero write; reader RED is its old checkpoint requirement. Wrong dtype/shape also expose secondary cleanup failures masking the expected primary code. Nonzero-update already halted at its correct old code; its RED reflects absent measured diagnostics, not a weakened exact-zero predicate. Full original output:

```text
test_amendment_z_prereg_pin (c10x_enginepath_selftest.SignedZeroTests.test_amendment_z_prereg_pin) ... FAIL
test_driver_halt_serializes_measured_x2_values (c10x_enginepath_selftest.SignedZeroTests.test_driver_halt_serializes_measured_x2_values) ... FAIL
test_equal_values_wrong_dtype_halt (c10x_enginepath_selftest.SignedZeroTests.test_equal_values_wrong_dtype_halt) ... FAIL
test_nan_value_halts (c10x_enginepath_selftest.SignedZeroTests.test_nan_value_halts) ... FAIL
test_nonzero_update_halts_before_weight_comparison (c10x_enginepath_selftest.SignedZeroTests.test_nonzero_update_halts_before_weight_comparison) ... ERROR
test_one_ulp_value_change_halts_with_all_layer_measurements (c10x_enginepath_selftest.SignedZeroTests.test_one_ulp_value_change_halts_with_all_layer_measurements) ... FAIL
test_signed_zero_write_passes_and_counts_binary16_bits (c10x_enginepath_selftest.SignedZeroTests.test_signed_zero_write_passes_and_counts_binary16_bits) ... ERROR
test_w0_byte_identity_stays_strict_before_and_after_null_cell (c10x_enginepath_selftest.SignedZeroTests.test_w0_byte_identity_stays_strict_before_and_after_null_cell) ... ok
test_wrong_shape_halts (c10x_enginepath_selftest.SignedZeroTests.test_wrong_shape_halts) ... ERROR
test_signed_zero_reader_keeps_reports_out_of_admission (c10x_enginepath_selftest.FileAdmissionTests.test_signed_zero_reader_keeps_reports_out_of_admission) ... ERROR

======================================================================
ERROR: test_nonzero_update_halts_before_weight_comparison (c10x_enginepath_selftest.SignedZeroTests.test_nonzero_update_halts_before_weight_comparison)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 1816, in test_nonzero_update_halts_before_weight_comparison
    measured=self.failed_gate(change,'NULL_NONZERO_UPDATE')
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 1769, in failed_gate
    measured=caught.exception.x2_vii_diagnostic
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: 'Halt' object has no attribute 'x2_vii_diagnostic'

======================================================================
ERROR: test_signed_zero_write_passes_and_counts_binary16_bits (c10x_enginepath_selftest.SignedZeroTests.test_signed_zero_write_passes_and_counts_binary16_bits)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 1775, in test_signed_zero_write_passes_and_counts_binary16_bits
    record=self.run_gate()
           ^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 1765, in run_gate
    return self.gate(self.H,self.hp,self.requests,[torch.eye(2) for _ in self.hp.layers],self.pristine)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<production X2-vii AST>", line 112, in gate
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_inertness.py", line 118, in verify
    require(actual == self.hashes, 'W0 '+label)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_inertness.py", line 12, in require
    raise Halt(code)
c10x_enginepath_inertness.Halt: W0 X2-vii exact zero

======================================================================
ERROR: test_wrong_shape_halts (c10x_enginepath_selftest.SignedZeroTests.test_wrong_shape_halts)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_inertness.py", line 127, in cell
    yield
  File "<production X2-vii AST>", line 112, in gate
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_inertness.py", line 118, in verify
    require(actual == self.hashes, 'W0 '+label)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_inertness.py", line 12, in require
    raise Halt(code)
c10x_enginepath_inertness.Halt: W0 X2-vii exact zero

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 1809, in test_wrong_shape_halts
    measured=self.failed_gate(lambda records:setattr(self.weight(8),'data',self.weight(8).detach().reshape(1,4)),
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 1767, in failed_gate
    with self.assertRaises(I.Halt) as caught:self.run_gate(change)
                                             ^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 1765, in run_gate
    return self.gate(self.H,self.hp,self.requests,[torch.eye(2) for _ in self.hp.layers],self.pristine)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<production X2-vii AST>", line 86, in gate
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/contextlib.py", line 158, in __exit__
    self.gen.throw(typ, value, traceback)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_inertness.py", line 129, in cell
    self.restore()
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_inertness.py", line 114, in restore
    npd[self.H.weight_name(self.hp, l)].copy_(value)
RuntimeError: The size of tensor a (4) must match the size of tensor b (2) at non-singleton dimension 1

======================================================================
ERROR: test_signed_zero_reader_keeps_reports_out_of_admission (c10x_enginepath_selftest.FileAdmissionTests.test_signed_zero_reader_keeps_reports_out_of_admission)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 927, in test_signed_zero_reader_keeps_reports_out_of_admission
    R._file_evidence(f,{'elapsed_seconds':8.})
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_read.py", line 1021, in _file_evidence
    _need(required <= set(names) and names.count('before recipe A') >= 2 and
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_read.py", line 38, in _need
    raise ValueError(message)
ValueError: W0 checkpoint coverage is incomplete

======================================================================
FAIL: test_amendment_z_prereg_pin (c10x_enginepath_selftest.SignedZeroTests.test_amendment_z_prereg_pin)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 1845, in test_amendment_z_prereg_pin
    self.assertEqual(A.PIN,pin);self.assertEqual(R.PREREG_SHA256,pin)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: '43a81103d68b953c2007e978b3ebecf11aadf66a7f121346047279845e8fc883' != 'd3dfdc8bd8a9c04894b63da9b51ead164e7667e40d8f08b29b11606078f92899'
- 43a81103d68b953c2007e978b3ebecf11aadf66a7f121346047279845e8fc883
+ d3dfdc8bd8a9c04894b63da9b51ead164e7667e40d8f08b29b11606078f92899


======================================================================
FAIL: test_driver_halt_serializes_measured_x2_values (c10x_enginepath_selftest.SignedZeroTests.test_driver_halt_serializes_measured_x2_values)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 1835, in test_driver_halt_serializes_measured_x2_values
    self.assertEqual(result['status'],'HALTED');self.assertEqual(result['code'],'X2-vii WEIGHT_VALUE 7')
                                                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'W0 X2-vii exact zero' != 'X2-vii WEIGHT_VALUE 7'
- W0 X2-vii exact zero
+ X2-vii WEIGHT_VALUE 7


======================================================================
FAIL: test_equal_values_wrong_dtype_halt (c10x_enginepath_selftest.SignedZeroTests.test_equal_values_wrong_dtype_halt)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 1806, in test_equal_values_wrong_dtype_halt
    measured=self.failed_gate(change,'X2-vii WEIGHT_VALUE 4')
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 1768, in failed_gate
    self.assertEqual(str(caught.exception),code)
AssertionError: 'W0 after X2-vii null' != 'X2-vii WEIGHT_VALUE 4'
- W0 after X2-vii null
+ X2-vii WEIGHT_VALUE 4


======================================================================
FAIL: test_nan_value_halts (c10x_enginepath_selftest.SignedZeroTests.test_nan_value_halts)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 1799, in test_nan_value_halts
    measured=self.failed_gate(lambda records:self.weight(5).__setitem__((0,1),float('nan')),'X2-vii WEIGHT_VALUE 5')
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 1768, in failed_gate
    self.assertEqual(str(caught.exception),code)
AssertionError: 'W0 X2-vii exact zero' != 'X2-vii WEIGHT_VALUE 5'
- W0 X2-vii exact zero
+ X2-vii WEIGHT_VALUE 5


======================================================================
FAIL: test_one_ulp_value_change_halts_with_all_layer_measurements (c10x_enginepath_selftest.SignedZeroTests.test_one_ulp_value_change_halts_with_all_layer_measurements)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 1792, in test_one_ulp_value_change_halts_with_all_layer_measurements
    measured=self.failed_gate(change,'X2-vii WEIGHT_VALUE 6')
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 1768, in failed_gate
    self.assertEqual(str(caught.exception),code)
AssertionError: 'W0 X2-vii exact zero' != 'X2-vii WEIGHT_VALUE 6'
- W0 X2-vii exact zero
+ X2-vii WEIGHT_VALUE 6


----------------------------------------------------------------------
Ran 10 tests in 0.530s

FAILED (failures=5, errors=4)
```

Two additional diagnostic defects were reproduced before their fixes:

- `red_report_unavailable.log`: exit 1; replacing report-only counts with explicit unavailable values made `read_record` INVALID instead of the unchanged VALID result. Fixed by the narrow report-only null exception. Scientific fields retain their null/type/finiteness checks.
- `red_after_cell.log`: exit 1; after a successful signed-zero write, an injected strict after-cell verification halt lost all five updates (`0 != 5`) and re-measured restored weights. Fixed by retaining the pre-restoration evidence.

### GREEN, serial CPU verification

All Python ran serially, with bytecode disabled and CPU thread limits. Outputs and test roots are under `/private/tmp/c10x_build/`. No real model/tokenizer, transformer/dataset import, MPS tensor, GPU run, stage launch or real-tree driver run was used.

- `green_targeted_final.log`: exit **0**, all **11** Amendment Z focused tests PASS (1.289 s).
- `green_full_selftest.log`: exit **0**, all **83** C10X selftests PASS (19.568 s).
- `green_probe_compatibility.log`: exit **0**, existing **17** model-free probe groups PASS (0.991 s), confirming the unchanged probe remains compatible with the enriched observer records. Its separate real-cache test was not invoked in this amendment build.
- `engine_fingerprint_worktree.log`: exit **0**, explicit `LLMDB_ROOT=W`, expected engine hash and `_cov_cpu=3`.
- Frozen-tree `git diff --quiet -- memit_dry_run docs/C10X_ENGINEPATH_PREREG.md experiments/track_c/c10e_bandknob.py`: exit **0**. Scoped `git diff --check`: exit **0**.

Exact full-suite command:

```sh
/usr/bin/env TMPDIR=/private/tmp/c10x_build PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 '/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python' -B '/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py'
```

Full PASS output, including both listing backstops and import assertions:

```text
test_admitted_process_pair_and_p2_gate (__main__.FileAdmissionTests.test_admitted_process_pair_and_p2_gate) ... ok
test_amendment_p_digest_refusals (__main__.FileAdmissionTests.test_amendment_p_digest_refusals) ... ok
test_amendment_p_prereg_pin (__main__.FileAdmissionTests.test_amendment_p_prereg_pin) ... ok
test_answer_audit_uses_runtime_recipe_order (__main__.FileAdmissionTests.test_answer_audit_uses_runtime_recipe_order) ... ok
test_complete_stub_run_persists_every_record (__main__.FileAdmissionTests.test_complete_stub_run_persists_every_record) ... ok
test_context_binding_enter_failure_restores (__main__.FileAdmissionTests.test_context_binding_enter_failure_restores) ... ok
test_deadline_completion_and_previous_overhead (__main__.FileAdmissionTests.test_deadline_completion_and_previous_overhead) ... ok
test_detailed_admission_negative_controls (__main__.FileAdmissionTests.test_detailed_admission_negative_controls) ... ok
test_direct_shell_launchers_are_executable_in_git (__main__.FileAdmissionTests.test_direct_shell_launchers_are_executable_in_git) ... DIRECT SHELL ENTRY POINTS: none; all three supervised commands use sys.executable
ok
test_disable_cutoff_never_excuses_earlier_omissions (__main__.FileAdmissionTests.test_disable_cutoff_never_excuses_earlier_omissions) ... ok
test_disable_marker_records_failed_answer_cutoff (__main__.FileAdmissionTests.test_disable_marker_records_failed_answer_cutoff) ... ok
test_every_science_record_roundtrip_and_reader_audit (__main__.FileAdmissionTests.test_every_science_record_roundtrip_and_reader_audit) ... ok
test_fp32_overflow_capture_and_parity_remain_report_only (__main__.FileAdmissionTests.test_fp32_overflow_capture_and_parity_remain_report_only) ... ok
test_frozen_scorer_forwards_have_no_injected_kwargs (__main__.FileAdmissionTests.test_frozen_scorer_forwards_have_no_injected_kwargs) ... ok
test_late_supervisor_persistence_is_unreadable (__main__.FileAdmissionTests.test_late_supervisor_persistence_is_unreadable) ... ok
test_missing_inertness_evidence_is_refused (__main__.FileAdmissionTests.test_missing_inertness_evidence_is_refused) ... ok
test_no_combined_device_dtype_conversions (__main__.FileAdmissionTests.test_no_combined_device_dtype_conversions) ... ok
test_pinned_contexts_never_sample (__main__.FileAdmissionTests.test_pinned_contexts_never_sample) ... ok
test_pinned_processes_and_halted_context_identity (__main__.FileAdmissionTests.test_pinned_processes_and_halted_context_identity) ... ok
test_post_audit_blocks_are_killed_by_final_deadline (__main__.FileAdmissionTests.test_post_audit_blocks_are_killed_by_final_deadline) ... ok
test_post_audit_budget_and_disabled_disposition (__main__.FileAdmissionTests.test_post_audit_budget_and_disabled_disposition) ... ok
test_post_audit_rejects_contradictory_receipts (__main__.FileAdmissionTests.test_post_audit_rejects_contradictory_receipts) ... ok
test_post_audit_startup_consumes_remaining_budget (__main__.FileAdmissionTests.test_post_audit_startup_consumes_remaining_budget) ... ok
test_reader_publishes_invalid_with_exit_zero (__main__.FileAdmissionTests.test_reader_publishes_invalid_with_exit_zero) ... ok
test_recipe_fp32_overflow_does_not_halt_or_change_labels (__main__.FileAdmissionTests.test_recipe_fp32_overflow_does_not_halt_or_change_labels) ... ok
test_script_alias_and_preflight_refusal_in_isolated_child (__main__.FileAdmissionTests.test_script_alias_and_preflight_refusal_in_isolated_child) ... ok
test_signed_zero_reader_keeps_reports_out_of_admission (__main__.FileAdmissionTests.test_signed_zero_reader_keeps_reports_out_of_admission) ... ok
test_supervisor_fail_closed_and_combining_output_path (__main__.FileAdmissionTests.test_supervisor_fail_closed_and_combining_output_path) ... ok
test_tagged_fp32_diagnostics_preserve_file_admission (__main__.FileAdmissionTests.test_tagged_fp32_diagnostics_preserve_file_admission) ... ok
test_tokenizer_forwards_preserve_attention_mask (__main__.FileAdmissionTests.test_tokenizer_forwards_preserve_attention_mask) ... ok
test_actual_fe_writes_and_null_solve_observer (__main__.IntegrationTests.test_actual_fe_writes_and_null_solve_observer) ... ok
test_actual_singleton_reduction_and_resolved_capture (__main__.IntegrationTests.test_actual_singleton_reduction_and_resolved_capture) ... ok
test_projection_uses_remaining_units_and_setup_clock (__main__.IntegrationTests.test_projection_uses_remaining_units_and_setup_clock) ... ok
test_solver_masked_gradient_clip_filter_and_tie (__main__.IntegrationTests.test_solver_masked_gradient_clip_filter_and_tie) ... ok
test_telemetry_recipe_records_and_counts_equal (__main__.IntegrationTests.test_telemetry_recipe_records_and_counts_equal) ... ok
test_telemetry_valid_admission_and_runner_no_writes (__main__.IntegrationTests.test_telemetry_valid_admission_and_runner_no_writes) ... ok
test_three_recipe_telemetry_probe_and_file_equality (__main__.IntegrationTests.test_three_recipe_telemetry_probe_and_file_equality) ... ok
test_reader_control_boundaries (__main__.ReaderTests.test_reader_control_boundaries) ... ok
test_reader_count_classes (__main__.ReaderTests.test_reader_count_classes) ... ok
test_reader_flags_denominators_nulls (__main__.ReaderTests.test_reader_flags_denominators_nulls) ... ok
test_reader_interpretation_and_null_table (__main__.ReaderTests.test_reader_interpretation_and_null_table) ... ok
test_reader_law3_boundaries (__main__.ReaderTests.test_reader_law3_boundaries) ... ok
test_reader_locality_boundaries (__main__.ReaderTests.test_reader_locality_boundaries) ... ok
test_reader_process_combination (__main__.ReaderTests.test_reader_process_combination) ... ok
test_reader_qualifier_boundaries (__main__.ReaderTests.test_reader_qualifier_boundaries) ... ok
test_reader_replication (__main__.ReaderTests.test_reader_replication) ... ok
test_reader_validity (__main__.ReaderTests.test_reader_validity) ... ok
test_active_null_negative_controls (__main__.SeamTests.test_active_null_negative_controls) ... ok
test_baseline_miss_stops_candidates (__main__.SeamTests.test_baseline_miss_stops_candidates) ... ok
test_capture_bindings_identity_attribution (__main__.SeamTests.test_capture_bindings_identity_attribution) ... ok
test_dispatch_call_time_flag (__main__.SeamTests.test_dispatch_call_time_flag) ... ok
test_fe_ast_three_changes (__main__.SeamTests.test_fe_ast_three_changes) ... ok
test_fe_modes_and_keys (__main__.SeamTests.test_fe_modes_and_keys) ... ok
test_float64_dense_reference (__main__.SeamTests.test_float64_dense_reference) ... ok
test_independent_full_vocabulary_audit (__main__.SeamTests.test_independent_full_vocabulary_audit) ... ok
test_knobs_and_frame_subjects (__main__.SeamTests.test_knobs_and_frame_subjects) ... ok
test_launch_refusals (__main__.SeamTests.test_launch_refusals) ... ok
test_pristine_hash_restore_hooks (__main__.SeamTests.test_pristine_hash_restore_hooks) ... ok
test_process2_requires_eligibility (__main__.SeamTests.test_process2_requires_eligibility) ... ok
test_recipe_states_counters (__main__.SeamTests.test_recipe_states_counters) ... ok
test_solver_ast_and_gradients (__main__.SeamTests.test_solver_ast_and_gradients) ... ok
test_tolerance_and_finiteness (__main__.SeamTests.test_tolerance_and_finiteness) ... ok
test_watchdog_and_projection (__main__.SeamTests.test_watchdog_and_projection) ... ok
test_after_cell_halt_keeps_pre_restoration_measurements (__main__.SignedZeroTests.test_after_cell_halt_keeps_pre_restoration_measurements) ... ok
test_amendment_z_prereg_pin (__main__.SignedZeroTests.test_amendment_z_prereg_pin) ... ok
test_driver_halt_serializes_measured_x2_values (__main__.SignedZeroTests.test_driver_halt_serializes_measured_x2_values) ... ok
test_equal_values_wrong_dtype_halt (__main__.SignedZeroTests.test_equal_values_wrong_dtype_halt) ... ok
test_nan_value_halts (__main__.SignedZeroTests.test_nan_value_halts) ... ok
test_nonzero_update_halts_before_weight_comparison (__main__.SignedZeroTests.test_nonzero_update_halts_before_weight_comparison) ... ok
test_one_ulp_value_change_halts_with_all_layer_measurements (__main__.SignedZeroTests.test_one_ulp_value_change_halts_with_all_layer_measurements) ... ok
test_signed_zero_write_passes_and_counts_binary16_bits (__main__.SignedZeroTests.test_signed_zero_write_passes_and_counts_binary16_bits) ... ok
test_w0_byte_identity_stays_strict_before_and_after_null_cell (__main__.SignedZeroTests.test_w0_byte_identity_stays_strict_before_and_after_null_cell) ... ok
test_wrong_shape_halts (__main__.SignedZeroTests.test_wrong_shape_halts) ... ok
test_frozen_bytes_and_imports (__main__.TelemetryTests.test_frozen_bytes_and_imports) ... IMPORT GUARD PASS: c10e_bandknob, transformers, datasets absent
ok
test_isolation_positive_control_children_meta (__main__.TelemetryTests.test_isolation_positive_control_children_meta) ... ok
test_post_run_answer_audit (__main__.TelemetryTests.test_post_run_answer_audit) ... ok
test_strict_json_roundtrips (__main__.TelemetryTests.test_strict_json_roundtrips) ... ok
test_telemetry_code_path_equality (__main__.TelemetryTests.test_telemetry_code_path_equality) ... ok
test_telemetry_failure_boundaries (__main__.TelemetryTests.test_telemetry_failure_boundaries) ... ok
test_telemetry_inertness_schedule (__main__.TelemetryTests.test_telemetry_inertness_schedule) ... ok
test_telemetry_line_volume (__main__.TelemetryTests.test_telemetry_line_volume) ... ok
test_telemetry_state_unchanged (__main__.TelemetryTests.test_telemetry_state_unchanged) ... ok
test_telemetry_switch_admission (__main__.TelemetryTests.test_telemetry_switch_admission) ... ok

----------------------------------------------------------------------
Ran 83 tests in 19.568s

OK
LISTING: attributed-protected changes = {}
LISTING: observed/unattributed other changes = {}
SYS.MODULES PASS: c10e_bandknob/transformers/datasets absent
```

Probe compatibility output:

```text
test_cli_wrong_template_refuses_before_loader (__main__.selftest.<locals>.ProbeTests.test_cli_wrong_template_refuses_before_loader) ... ok
test_copy_guard_refuses_before_operator (__main__.selftest.<locals>.ProbeTests.test_copy_guard_refuses_before_operator) ... ok
test_descriptor_relative_writes_and_fd_mutations (__main__.selftest.<locals>.ProbeTests.test_descriptor_relative_writes_and_fd_mutations) ... ok
test_descriptor_runtime_open_from_protected_cwd (__main__.selftest.<locals>.ProbeTests.test_descriptor_runtime_open_from_protected_cwd) ... ok
test_existing_output_refused (__main__.selftest.<locals>.ProbeTests.test_existing_output_refused) ... ok
test_file_write_policy (__main__.selftest.<locals>.ProbeTests.test_file_write_policy) ... ok
test_guard_blocks_alias_and_out_writes_before_execution (__main__.selftest.<locals>.ProbeTests.test_guard_blocks_alias_and_out_writes_before_execution) ... ok
test_no_live_weight_writes (__main__.selftest.<locals>.ProbeTests.test_no_live_weight_writes) ... ok
test_nonzero_residual_matches_rejecting_gate (__main__.selftest.<locals>.ProbeTests.test_nonzero_residual_matches_rejecting_gate) ... ok
test_probe_bans_unsafe_copy_forms (__main__.selftest.<locals>.ProbeTests.test_probe_bans_unsafe_copy_forms) ... ok
test_protected_aliases_and_directory_moves (__main__.selftest.<locals>.ProbeTests.test_protected_aliases_and_directory_moves) ... ok
test_residual_matches_actual_gate_fixed_input (__main__.selftest.<locals>.ProbeTests.test_residual_matches_actual_gate_fixed_input) ... ok
test_runtime_files_are_writable_under_installed_policy (__main__.selftest.<locals>.ProbeTests.test_runtime_files_are_writable_under_installed_policy) ... ok
test_signed_zero_only_changes_shadow_bytes (__main__.selftest.<locals>.ProbeTests.test_signed_zero_only_changes_shadow_bytes) ... ok
test_unsafe_copy_predicate_without_mps (__main__.selftest.<locals>.ProbeTests.test_unsafe_copy_predicate_without_mps) ... ok
test_wrong_template_hash_refuses_before_forward (__main__.selftest.<locals>.ProbeTests.test_wrong_template_hash_refuses_before_forward) ... ok
test_x2_iv_floor_threshold_matches_gate (__main__.selftest.<locals>.ProbeTests.test_x2_iv_floor_threshold_matches_gate) ... ok

----------------------------------------------------------------------
Ran 17 tests in 0.991s

OK
CPU ONLY; no frozen harness/transformers/datasets imported
```

Worktree fingerprint output:

```text
engine fingerprint PASS: /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/memit_dry_run/memit/memit/memit_main.py
  sha256   d941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65  (expected d941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65; pod-era 5c0c706a…)
  _cov_cpu 3  (expected 3)
```

No prior mutation campaign was rerun: this narrow amendment's tests cover the new signed-zero/value/dtype/shape/report-only boundaries. The earlier mutation evidence remains historical evidence, not new execution.

### Preservation, review and final SHAs

Only four C10X source files changed in this amendment build, plus this append to the named report. All **188 R5 file hashes** equal this task's before snapshot, including the program-authored §13 prereg; the other **187** continue matching the earlier frozen baseline. The full before/after tables are `before.json/protected_R5` and `sealed_evidence.json/protected_R5`, not a truncated scan. All **five held artifact hashes** match, including the original HALTED run, its pinned template JSON, the failed 17:10 probe JSON/log and the measured 18:05 probe JSON. The prior **255,636 report bytes** are preserved exactly (prefix SHA `e2a931c2d3595dd48af16e830dc233ced2814d69b828b8eae16213eaff538b28`). No old run, probe, diagnostic or historical report section was repaired or rewritten.

The preservation audit compares saved source ASTs: all four `Pristine` methods; `tensor_sha`, `active_null_structure`, parity/floor helpers and `write_cell`; every original `require` in `run_checks` and `observe_null_solve`; the observer call; all checks before X2-vii and G8 after it; and the final inertness cleanup remain unchanged. The only removed `pristine.verify` call is the superseded in-cell weight criterion. In the driver, the only changed function is `run`; all writer/scorer/lens/T8 ASTs are unchanged. In the reader, only `_nulls` and `_file_evidence` change besides the SHA constant.

Current git porcelain (the pre-existing `.gitignore` modification is unowned by this task):

```text
 M .gitignore
 M experiments/track_c/c10x_enginepath_arms.py
 M experiments/track_c/c10x_enginepath_inertness.py
 M experiments/track_c/c10x_enginepath_read.py
 M experiments/track_c/c10x_enginepath_selftest.py
```

Scoped diff summary:

```text
 experiments/track_c/c10x_enginepath_arms.py      |   6 +-
 experiments/track_c/c10x_enginepath_inertness.py | 150 +++++++++++++++-----
 experiments/track_c/c10x_enginepath_read.py      |   8 +-
 experiments/track_c/c10x_enginepath_selftest.py  | 171 ++++++++++++++++++++++-
 4 files changed, 293 insertions(+), 42 deletions(-)
```

| Source artifact | Final SHA-256 | Amendment delta |
| --- | --- | --- |
| `experiments/track_c/c10x_enginepath_arms.py` | `ffcf5200c81c2c860f8b7741d19545b88f66b68f546ce4e11c52adff6ea609fc` | changed |
| `experiments/track_c/c10x_enginepath_inertness.py` | `c1c964da94513b29138677f637bf70f55cdb35f3f07d39d7b0d1a05d26b4c7e4` | changed |
| `experiments/track_c/c10x_enginepath_read.py` | `b17e588a8c8f6ff3d8ee5f3dc118fd8837bd9e26b7bdf33e343599ce671c2057` | changed |
| `experiments/track_c/c10x_enginepath_selftest.py` | `5d172baf3694619f04bd33e226dab641cdf1b985f86d8e59022c9f6e2a2252f0` | changed |
| `experiments/track_c/c10x_enginepath_telemetry_check.py` | `e95beb2cef310fa1050ccb4a2b60ac8224f493ea4d513d97868f3b9a9c99fe80` | unchanged |
| `experiments/track_c/c10x_overtone_z.py` | `8b32ca840c1451624ba5f46143a6e65a03ae69e968dd0e6180d04fa5683dac42` | unchanged |
| `experiments/track_c/c10x_x2_probe.py` | `23bdf070c66f8af02bb4d38d22eaecdfffa04782339f500ce1572080d6a2b614` | unchanged |
| `docs/C10X_ENGINEPATH_PREREG.md` | `d3dfdc8bd8a9c04894b63da9b51ead164e7667e40d8f08b29b11606078f92899` | program-authored §13, unchanged by build |

Active pins in the driver, reader, synthetic fixture, prereg-pin tests and frozen-byte test now use `d3dfdc8bd8a9c04894b63da9b51ead164e7667e40d8f08b29b11606078f92899`. Exhaustive search of `experiments/`, `tools/` and `configs/` finds no old `43a81103…` pin. The full old SHA remains only as the deliberately historical prereg :642 identity in that search scope. Original historical records and report hashes are preserved.

The [advisor-review](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.codex/skills/advisor-review/SKILL.md) design and implementation checks used a fresh read-only `/root/signedzero_refute` fallback after Claude subscription auth returned exit 1, `loggedIn=false`, `authMethod=none`. The implementation review first returned FIX-FIRST for the after-cell evidence loss, reproduced above, then **PROCEED with no remaining static blocker** after the fix. This fallback has weaker independence. Reviewer runtime results are UNVERIFIED because it ran no Python/tests; the author’s CPU PASS evidence is given above. The supplied Astra amendment delta remains GO. This is implementation verification, not the program's later live-build admission/dispatch decision.

| Private evidence artifact (under `/private/tmp/c10x_build/signedzero_amendment/`) | SHA-256 |
| --- | --- |
| `engine_fingerprint_worktree.log` | `15aef4acf47eb374ea93cf4f949a0022a287f56b646ac2b139f599af98b355e3` |
| `green_full_selftest.log` | `546bb57f51afe21546ed1f9d50e776ca8e4a7ce357966164afac5aded8f60fdd` |
| `green_probe_compatibility.log` | `6c5108b59b17619acb530c44bf81bf68aebbcfaecbcd58cf51c99a4e4b4d0ae6` |
| `green_targeted_final.log` | `2a028c6737637ec35284a2be3f451ff06cd8954321058574db60a36b2aec729a` |
| `red.log` | `808e139c885838bddc9ce3704b757e9110c897b0a47b1210b068104a16aa162a` |
| `red_after_cell.log` | `19362dd33602a7d0f97418aa3ba024f0d3cac36cd479f3006ace6b215c28c2e8` |
| `red_report_unavailable.log` | `31e8e816a9d6fa3a007022042f07ca067a49f11973ffe5448b27327314023beb` |
| `final_review.md` | `b596d5d8ca43a1c6089ac6e166234882fb3a3b426fef8833ca0c81b86b1096e1` |
| `sealed_evidence.json` | `0fe94858c7e3d73cbc14a512423151555e8320d04f1c39fa04fd57451399bc25` |
| `final_patch.diff` | `77f23f088fad2a4a5c3c280b3f87d8fe25ad2f3e186f2d73edce55889878004d` |

**Live evidence remains UNVERIFIED.** No scientific result, injection/candidate success or universal MPS equivalence follows from these CPU tests. Process 1 in `results/c10x_enginepath/` remains HALTED/incomplete and INVALID, with no scientific classification. The authorized §13 rerun requires the full sequence, fresh `results/c10x_enginepath_rerun1/` and matching logs, current source/prereg pins, program build review and operator GO (prereg :776–797). No dispatch was performed. No new PROVISIONAL decision was made.

Final append/source/held-artifact receipt: `/private/tmp/c10x_build/signedzero_amendment/final_receipt.json`. Final handoff in the context-save format is under the same authorized scratch directory; home/global context or publication state is outside this brief's write scope.


## Scorer JSON ingress and stage-boundary repair — 2026-10-08T21:54:50.486481+00:00

**Build outcome: CPU PASS; read-only final review GO.** The final full selftest passes **96 tests**, including **13 new regressions**. This repairs record conversion and failure reporting after rerun1's final-record HALT. It supplies no new live scientific result. `results/c10x_enginepath_rerun1/run.json` remains **HALTED / incomplete**; the prior run must be repeated in a fresh namespace. Its measured arms are not read around, admitted, or classified by this build.

Author: Codex. Actual model/effort receipt: **UNVERIFIABLE**. Prereg pin, unchanged throughout this repair: **`d3dfdc8bd8a9c04894b63da9b51ead164e7667e40d8f08b29b11606078f92899`** (Amendments T/M/P/Z). No new PROVISIONAL decision. The current program instruction authorizes light, serial CPU work while ASTRA is live; all Python commands used the existing worktree venv with bytecode disabled, one at a time. All test driver/output/child roots were under `/private/tmp/c10x_build/roots/`. No model/tokenizer load, frozen harness import, GPU dispatch, MPS tensor, or heavy parallel job was performed.

### Failure and record-entry audit

The operator's named failure is confirmed from status and error metadata only: `record.inertness.X2-vi.flags_reference[0] is not JSON data`. The historical diagnostic is `architecture_profile/c10x_halt_diagnostic_20261008T212435_844926Z.json` (SHA `785c9909a578f8be53b809c438663bf65dc4d264e023736b3b223fff88be448b`). It and the historical run have no recorded phase/traceback. No historical arm results were evaluated. The frozen `full_seq_match` at `experiments/track_c/c10e_bandknob.py:109–118` returns a tuple; with tensor target IDs its first-token result is a scalar `torch.bool`, and with NumPy integer target IDs it is `numpy.bool_`. The new test compiles that exact source function against the tiny CPU model, runs it, then exercises the production writer capture. Container conversion alone would leave the scalar wrappers intact.

`scorer_record` (`experiments/track_c/c10x_enginepath_arms.py:254–269`) materializes native booleans/integers/floats, numeric/boolean NumPy scalars, and zero-dimensional numeric/boolean torch scalars, and changes scorer tuples into lists. Torch scalar extraction uses `detach().cpu().item()`; no dtype-changing device copy is introduced. Other arrays/tensors/complex or unsupported values fail with their ingress path. Dictionary keys remain unchanged for strict validation. This helper is called only where a known scorer result enters the driver record; accumulated state is never normalized or passed through a permissive JSON fallback. Non-finite floats stay available for existing Amendment M report-only tagging; untagged non-finite gate values remain strictly rejected.

| Scorer-fed record | Frozen producer / binding | Record entry and conversion | Verification |
| --- | --- | --- | --- |
| X2-vi `flags_reference` / `flags_candidate`; X2-ii flag-derived differences | Frozen `full_seq_match` (`c10e_bandknob.py:109–118`); program request (1) | `c10x_enginepath_inertness.py:301–305`: `[bool(full), bool(first)]` at writer record entry. X2-vi still records those same two lists at `:463–465`; X2-ii sums plain flags at `:425–426`. Calls, ordering, inputs and scientific comparisons unchanged. | Actual frozen scorer produces tuple + torch/NumPy boolean; 96 pairs become lists of Python booleans; sums are Python ints, values preserved. |
| Recipe LAW#5 gate, all arm summaries, detail rows, locality axes and probe extras | `c10e_bandknob.py:326–338`, `:354–399`, `:440–446`, `:458–508` | `c10x_enginepath_arms.py:666`: materialize the returned harness tree before enrichment/count derivation (`:724–733`). Covers canonical/full/first/string flags, percentages, exact counts, denominators, continuation counts/ratios, per-fact/per-template counts, L1/L3/perplexity and probe fields. | Every boolean/integer/float leaf in the complete scorer-field inventory is wrapped as a torch scalar and separately as a NumPy scalar; exact Python type and value equality is checked recursively. Integer `2**53+1` survives both ingress conversions exactly. |
| Pristine baseline report: base, mean token count and token range | `c10e_bandknob.py:449–455`; existing stimulus-leak rule | `c10x_enginepath_arms.py:1182–1184`: normalize immediately on receipt, attach to state, validate JSON before the unchanged exact-int/leak check. | Real torch/NumPy scalar types in all report numeric fields; driver completes with unchanged values and Python types. |
| Injection row flags and canonical/paraphrase/template counts | Same frozen scorer; existing injection screen | `c10x_enginepath_arms.py:1041–1047`: cast each recorded hit with `bool()` before aggregation. | Torch/NumPy boolean hits yield 24 canonical, 72 paraphrase and exact per-template Python-int counts. |
| Frame rows, relation-label top1/flips/pristine arrays, teacher-forced curve | Existing read-only probe; `c10e_bandknob.py:137–145` supplies its scorer pattern | `c10x_enginepath_arms.py:1074`, `:1084–1086`, `:1096`: `int(top1)`, `bool(flip)`, integer relation counts/IDs and `int(pred == gold)` before accumulating recorded correct counts. | NumPy top1 plus torch/NumPy target IDs; plain JSON and 72/72 at both teacher-forced positions. Input set membership and forward/concatenation logic remain unchanged. This proves record types/counts, not frame-flip equivalence for artificial tensor-valued tokenizer outputs. |
| Telemetry target/generated token IDs and full/first flags | Amendment T4 observed scorer sink; `c10e_bandknob.py:109–118` | `c10x_enginepath_arms.py:366–370`: convert scalar IDs to Python ints at telemetry entry, then record Python-bool equality results. | Actual torch/NumPy integer IDs produce an enabled writer and an answer line with exact IDs/flags; serialization no longer disables telemetry. |
| Direct G8 locality and locality top1 observer fields | Existing G8 observer; frozen predict/locpct | `c10x_enginepath_inertness.py:364–367`: `float(locality)` and `int(locality_top1)`; probability, distribution and other top1 were already materialized. | Torch/NumPy numeric observer scalars; plain JSON in both engine/candidate views. |
| Raw LAW#5 locality-delta diagnostic | Original harness gate and its six predict observations | `c10x_enginepath_arms.py:709`: materialize the recorded locality delta with `float()` after the unchanged subtraction. | Both torch/NumPy locality scalar returns become native floats; original gate return and observation schedule retained. |
| Padded replay provenance lookup indices | Existing harness lookup helper, not a scored verdict | `c10x_enginepath_arms.py:758`: exported index list uses `int(i)`; live indexing arithmetic is unchanged. | Existing actual replay/injection input-identity integration tests pass; no tensor/device/dtype/shape changes. |

Other scorer-adjacent outputs were audited: logit-lens token/probability outputs and target-fit/per-position records already materialize their scalars; write norms use the existing float64 captures and Amendment M fp32 report tagging. T8's temporary raw generated flags are not exported; its exported equality/weight/control results were already native booleans/integers, and its body remains AST-identical. Internal writer update/cache/weight tensors remain tensors for scientific comparison and are not treated as JSON record trees.

### Every stage validates before proceeding

`validate_record_json` (`c10x_enginepath_arms.py:272–276`) first applies the unchanged reader `_finite_tree(state, 'record')` (`c10x_enginepath_read.py:81–92`) and only then encodes with `allow_nan=False` and checks equality after the existing strict JSON parser. Therefore tuples, foreign scalar types, non-string keys and non-finite floats cannot vanish through an encoding roundtrip. The reader/writer remain strict; `diagnostic_json` is still a diagnostic representation only.

`run`'s stage boundary at `c10x_enginepath_arms.py:1161–1174` checks the accumulated record at entry and exit for **setup → A → targets → inertness → injection → I-2 → I-1 → final**. Setup base/frames, target record portions/audits, inertness and injection products are attached as soon as produced (`:1182–1206`); live target tensors remain local. W0 checkpoints and timing/work-unit records are included at each boundary. Recipes also validate before LAW#3/G consumption (`:1194`, `:1210`), preserving the field-path error instead of converting it into a generic baseline miss. Final JSON validates before scientific `_validate` and publication and again after final timing capture (`:1240–1249`). Scientific `_validate` still runs only against the complete record.

The final reviewer found a real attribution defect in the first implementation: `StageBudget.enter(next)` still leaves the preceding stage, so switching the local label first could report its deadline failure as the next stage. Test `test_previous_stage_deadline_keeps_exit_phase` reproduced **`targets != A`**. The correction calls the original `BUDGET.leave()` while the prior `stage:exit` label remains current, then switches/enters the next stage (`:1170–1174`). The StageBudget class, caps, projections, deadline predicates and telemetry timing rules remain AST-identical.

The independent stage-contamination test injects non-JSON values **after** normalized producers return, at all eight stages; it checks the field path, HALTED record, originating stage/phase, complete traceback and absence of any next-stage execution. Additional strict controls cover tuples, non-string keys, multi-element tensors, complex values, NaN and Inf. A native integer above `2**53` retains exact roundtrip value. Valid records complete under the actual driver, validator and exclusive JSON writer in isolated temporary roots.

### Halt diagnostics

The worker captures `traceback.format_exc()` **before** primary-X2 exception selection (`c10x_enginepath_arms.py:1254–1258`). The HALTED run and diagnostic include `stage`, `phase`, `traceback`, and `traceback_source`; the existing measured X2-vii exception payload remains preserved. `halt_diagnostic` (`:279–288`) publishes those fields at top level as well as in diagnostic state, and can extract a supplied exception's traceback when not already provided.

The supervisor propagates a recorded worker traceback/phase (`:1394–1404`). Timeout/kill and other non-exception halts explicitly record `traceback: null` with its absence provenance; it does not fabricate a Python worker exception. A preflight `TimeoutExpired` and answer-audit Python exceptions retain their actual parent traceback (`:1343–1344`, `:1414`); final deadline/persistence and compromised-audit halts carry an explicit absence reason (`:1420–1435`). Tests cover worker propagation and timeout absence. These guarantees apply to exceptions handled inside `run()` and supervisor diagnostics. Existing bootstrap/preflight refusal behavior before `run()` is unchanged; no claim is made that all earlier child exceptions produce a recorded worker traceback.

### Numbered new regression mapping

Every regression is in `experiments/track_c/c10x_enginepath_selftest.py`, derives from `IsolatedCase`, and uses the existing real-tree mutation/dispatch guard. All are GREEN in the final full suite. Numbers continue the earlier 83-test build.

| Test | Binding requirement | Test method / current line |
| --- | --- | --- |
| 84 | Program (1), X2-vi/X2-ii record-only conversion | `test_actual_harness_flags_are_plain_in_writer_record` `:1754` |
| 85 | Program (1)/(3), frozen scorer and all recipe scalar fields; Amendment M | `test_every_recipe_scorer_field_is_plain_before_enrichment` `:1771` |
| 86 | Program (1)/(3), injection flags/counts | `test_injection_flags_and_counts_use_plain_scalars` `:1795` |
| 87 | Program (1)/(3), calibration/probe output scalars | `test_probe_tensor_targets_and_numpy_top1_are_plain` `:1805` |
| 88 | Program (1)/(3), Amendment T4 telemetry sink record | `test_telemetry_scalar_ids_and_flags_do_not_disable_writer` `:1817` |
| 89 | Program (1)/(3), direct G8 observer | `test_direct_g8_observer_materializes_scalars` `:1830` |
| 90 | Program (1)/(3), original LAW#5 observation diagnostic | `test_raw_law5_locality_diagnostic_is_plain` `:1843` |
| 91 | Program (1)–(3), baseline report and genuine driver completion | `test_driver_normalizes_pristine_report_and_completes` `:1894` |
| 92 | Program (2)/(4), strict JSON at every stage, traceback/phase/no next stage | `test_every_stage_rejects_non_json_before_next_stage` `:1904` |
| 93 | Program (2), strict type/numeric negative controls and large-int roundtrip | `test_boundary_keeps_strict_types_and_numeric_limits` `:1920` |
| 94 | Program (2)/(4), previous stage's exit-deadline attribution | `test_previous_stage_deadline_keeps_exit_phase` `:1932` |
| 95 | Program (4), killed/timeout worker traceback provenance | `test_supervisor_timeout_has_phase_and_explicit_traceback_absence` `:1945` |
| 96 | Program (4), worker exception propagated by supervisor | `test_supervisor_propagates_worker_traceback_and_phase` `:1957` |

The prior signed-zero HALT fixture now supplies the actual target-producer record contract (`records` and `audits`), so it still reaches and proves the measured X2-vii halt. It no longer supplies an impossible empty producer mapping. All prior 83 tests remain in the full suite.

### RED / GREEN evidence

Initial focused RED ran before any production changes; `red_receipt.json` proves that only the selftest source changed relative to `before.json`. **12 tests ran; 17 failing assertions/subtests and 14 errors**. The errors include strict-JSON rejection of the genuine scorer tuple/scalar types, torch locality rounding on the unmaterialized observer value, and absent new diagnostic fields; failing assertions show telemetry disablement, baseline scalar refusal and next-stage execution before JSON rejection. No missing helper/import was used as the intended RED signal. The later deadline regression separately ran **1 test, 1 failing assertion** before its production fix.

Focused invocation (initial captured runner uses this same test class; its exact runner is described after the log):

```sh
cd /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a
env TMPDIR=/private/tmp/c10x_build PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONPATH=experiments/track_c .venv/bin/python -B -m unittest c10x_enginepath_selftest.ScorerJsonTests
```

Initial RED runner imported `c10x_enginepath_selftest`, used `unittest.defaultTestLoader.loadTestsFromTestCase(S.ScorerJsonTests)` and `TextTestRunner(verbosity=2)`, redirected runner stdout/stderr to `red.log`, asserted the before/after live listing and forbidden-module guard, then returned exit 1. The stderr telemetry-disable markers were also returned by that command. The full captured RED output is below; each behavioral failing assertion is retained.

```text
test_actual_harness_flags_are_plain_in_writer_record (c10x_enginepath_selftest.ScorerJsonTests.test_actual_harness_flags_are_plain_in_writer_record) ... 
  test_actual_harness_flags_are_plain_in_writer_record (c10x_enginepath_selftest.ScorerJsonTests.test_actual_harness_flags_are_plain_in_writer_record) (kind='torch') ... ERROR
  test_actual_harness_flags_are_plain_in_writer_record (c10x_enginepath_selftest.ScorerJsonTests.test_actual_harness_flags_are_plain_in_writer_record) (kind='numpy') ... ERROR
test_boundary_keeps_strict_types_and_numeric_limits (c10x_enginepath_selftest.ScorerJsonTests.test_boundary_keeps_strict_types_and_numeric_limits) ... 
  test_boundary_keeps_strict_types_and_numeric_limits (c10x_enginepath_selftest.ScorerJsonTests.test_boundary_keeps_strict_types_and_numeric_limits) (i=0) ... FAIL
  test_boundary_keeps_strict_types_and_numeric_limits (c10x_enginepath_selftest.ScorerJsonTests.test_boundary_keeps_strict_types_and_numeric_limits) (i=1) ... FAIL
  test_boundary_keeps_strict_types_and_numeric_limits (c10x_enginepath_selftest.ScorerJsonTests.test_boundary_keeps_strict_types_and_numeric_limits) (i=2) ... FAIL
  test_boundary_keeps_strict_types_and_numeric_limits (c10x_enginepath_selftest.ScorerJsonTests.test_boundary_keeps_strict_types_and_numeric_limits) (i=3) ... FAIL
  test_boundary_keeps_strict_types_and_numeric_limits (c10x_enginepath_selftest.ScorerJsonTests.test_boundary_keeps_strict_types_and_numeric_limits) (i=4) ... FAIL
  test_boundary_keeps_strict_types_and_numeric_limits (c10x_enginepath_selftest.ScorerJsonTests.test_boundary_keeps_strict_types_and_numeric_limits) (i=5) ... FAIL
test_direct_g8_observer_materializes_scalars (c10x_enginepath_selftest.ScorerJsonTests.test_direct_g8_observer_materializes_scalars) ... ERROR
test_driver_normalizes_pristine_report_and_completes (c10x_enginepath_selftest.ScorerJsonTests.test_driver_normalizes_pristine_report_and_completes) ... 
  test_driver_normalizes_pristine_report_and_completes (c10x_enginepath_selftest.ScorerJsonTests.test_driver_normalizes_pristine_report_and_completes) (kind='torch') ... FAIL
  test_driver_normalizes_pristine_report_and_completes (c10x_enginepath_selftest.ScorerJsonTests.test_driver_normalizes_pristine_report_and_completes) (kind='numpy') ... FAIL
test_every_recipe_scorer_field_is_plain_before_enrichment (c10x_enginepath_selftest.ScorerJsonTests.test_every_recipe_scorer_field_is_plain_before_enrichment) ... 
  test_every_recipe_scorer_field_is_plain_before_enrichment (c10x_enginepath_selftest.ScorerJsonTests.test_every_recipe_scorer_field_is_plain_before_enrichment) (kind='torch') ... ERROR
  test_every_recipe_scorer_field_is_plain_before_enrichment (c10x_enginepath_selftest.ScorerJsonTests.test_every_recipe_scorer_field_is_plain_before_enrichment) (kind='numpy') ... ERROR
test_every_stage_rejects_non_json_before_next_stage (c10x_enginepath_selftest.ScorerJsonTests.test_every_stage_rejects_non_json_before_next_stage) ... 
  test_every_stage_rejects_non_json_before_next_stage (c10x_enginepath_selftest.ScorerJsonTests.test_every_stage_rejects_non_json_before_next_stage) (stage='setup') ... FAIL
  test_every_stage_rejects_non_json_before_next_stage (c10x_enginepath_selftest.ScorerJsonTests.test_every_stage_rejects_non_json_before_next_stage) (stage='A') ... FAIL
  test_every_stage_rejects_non_json_before_next_stage (c10x_enginepath_selftest.ScorerJsonTests.test_every_stage_rejects_non_json_before_next_stage) (stage='targets') ... FAIL
  test_every_stage_rejects_non_json_before_next_stage (c10x_enginepath_selftest.ScorerJsonTests.test_every_stage_rejects_non_json_before_next_stage) (stage='inertness') ... FAIL
  test_every_stage_rejects_non_json_before_next_stage (c10x_enginepath_selftest.ScorerJsonTests.test_every_stage_rejects_non_json_before_next_stage) (stage='injection') ... FAIL
  test_every_stage_rejects_non_json_before_next_stage (c10x_enginepath_selftest.ScorerJsonTests.test_every_stage_rejects_non_json_before_next_stage) (stage='I-2') ... FAIL
  test_every_stage_rejects_non_json_before_next_stage (c10x_enginepath_selftest.ScorerJsonTests.test_every_stage_rejects_non_json_before_next_stage) (stage='I-1') ... FAIL
  test_every_stage_rejects_non_json_before_next_stage (c10x_enginepath_selftest.ScorerJsonTests.test_every_stage_rejects_non_json_before_next_stage) (stage='final') ... ERROR
test_injection_flags_and_counts_use_plain_scalars (c10x_enginepath_selftest.ScorerJsonTests.test_injection_flags_and_counts_use_plain_scalars) ... 
  test_injection_flags_and_counts_use_plain_scalars (c10x_enginepath_selftest.ScorerJsonTests.test_injection_flags_and_counts_use_plain_scalars) (kind='torch') ... ERROR
  test_injection_flags_and_counts_use_plain_scalars (c10x_enginepath_selftest.ScorerJsonTests.test_injection_flags_and_counts_use_plain_scalars) (kind='numpy') ... ERROR
test_probe_tensor_targets_and_numpy_top1_are_plain (c10x_enginepath_selftest.ScorerJsonTests.test_probe_tensor_targets_and_numpy_top1_are_plain) ... 
  test_probe_tensor_targets_and_numpy_top1_are_plain (c10x_enginepath_selftest.ScorerJsonTests.test_probe_tensor_targets_and_numpy_top1_are_plain) (kind='torch') ... ERROR
  test_probe_tensor_targets_and_numpy_top1_are_plain (c10x_enginepath_selftest.ScorerJsonTests.test_probe_tensor_targets_and_numpy_top1_are_plain) (kind='numpy') ... ERROR
test_raw_law5_locality_diagnostic_is_plain (c10x_enginepath_selftest.ScorerJsonTests.test_raw_law5_locality_diagnostic_is_plain) ... 
  test_raw_law5_locality_diagnostic_is_plain (c10x_enginepath_selftest.ScorerJsonTests.test_raw_law5_locality_diagnostic_is_plain) (kind='torch') ... ERROR
  test_raw_law5_locality_diagnostic_is_plain (c10x_enginepath_selftest.ScorerJsonTests.test_raw_law5_locality_diagnostic_is_plain) (kind='numpy') ... ERROR
test_supervisor_propagates_worker_traceback_and_phase (c10x_enginepath_selftest.ScorerJsonTests.test_supervisor_propagates_worker_traceback_and_phase) ... ERROR
test_supervisor_timeout_has_phase_and_explicit_traceback_absence (c10x_enginepath_selftest.ScorerJsonTests.test_supervisor_timeout_has_phase_and_explicit_traceback_absence) ... ERROR
test_telemetry_scalar_ids_and_flags_do_not_disable_writer (c10x_enginepath_selftest.ScorerJsonTests.test_telemetry_scalar_ids_and_flags_do_not_disable_writer) ... 
  test_telemetry_scalar_ids_and_flags_do_not_disable_writer (c10x_enginepath_selftest.ScorerJsonTests.test_telemetry_scalar_ids_and_flags_do_not_disable_writer) (kind='torch') ... FAIL
  test_telemetry_scalar_ids_and_flags_do_not_disable_writer (c10x_enginepath_selftest.ScorerJsonTests.test_telemetry_scalar_ids_and_flags_do_not_disable_writer) (kind='numpy') ... FAIL

======================================================================
ERROR: test_actual_harness_flags_are_plain_in_writer_record (c10x_enginepath_selftest.ScorerJsonTests.test_actual_harness_flags_are_plain_in_writer_record) (kind='torch')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 1766, in test_actual_harness_flags_are_plain_in_writer_record
    self.assertEqual(len(cell['flags']),96);self.plain(cell['flags'])
                                            ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 1743, in plain
    R._finite_tree(value)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_read.py", line 88, in _finite_tree
    _finite_tree(child, path + '[' + str(i) + ']')
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_read.py", line 92, in _finite_tree
    _need(value is None or type(value) in (str, bool, int), path + ' is not JSON data')
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_read.py", line 38, in _need
    raise ValueError(message)
ValueError: record[0] is not JSON data

======================================================================
ERROR: test_actual_harness_flags_are_plain_in_writer_record (c10x_enginepath_selftest.ScorerJsonTests.test_actual_harness_flags_are_plain_in_writer_record) (kind='numpy')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 1766, in test_actual_harness_flags_are_plain_in_writer_record
    self.assertEqual(len(cell['flags']),96);self.plain(cell['flags'])
                                            ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 1743, in plain
    R._finite_tree(value)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_read.py", line 88, in _finite_tree
    _finite_tree(child, path + '[' + str(i) + ']')
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_read.py", line 92, in _finite_tree
    _need(value is None or type(value) in (str, bool, int), path + ' is not JSON data')
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_read.py", line 38, in _need
    raise ValueError(message)
ValueError: record[0] is not JSON data

======================================================================
ERROR: test_direct_g8_observer_materializes_scalars (c10x_enginepath_selftest.ScorerJsonTests.test_direct_g8_observer_materializes_scalars)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 1837, in test_direct_g8_observer_materializes_scalars
    rec=I.direct_g8(self.H,self.H.hp,[torch.eye(2) for _ in self.H.hp.layers],[['{}']],pristine)
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_inertness.py", line 379, in direct_g8
    return behaviour_gate(engine,candidate)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_inertness.py", line 262, in behaviour_gate
    require(round(expr, 4) < .05 and round(loc, 2) < 3., 'G8_NOT_INERT')
                                     ^^^^^^^^^^^^^
TypeError: type Tensor doesn't define __round__ method

======================================================================
ERROR: test_every_recipe_scorer_field_is_plain_before_enrichment (c10x_enginepath_selftest.ScorerJsonTests.test_every_recipe_scorer_field_is_plain_before_enrichment) (kind='torch')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 1791, in test_every_recipe_scorer_field_is_plain_before_enrichment
    with self.subTest(kind=kind):self.plain(observed);self.same_types(observed,wanted)
                                 ^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 1743, in plain
    R._finite_tree(value)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_read.py", line 85, in _finite_tree
    _finite_tree(child, path + '.' + key)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_read.py", line 85, in _finite_tree
    _finite_tree(child, path + '.' + key)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_read.py", line 92, in _finite_tree
    _need(value is None or type(value) in (str, bool, int), path + ' is not JSON data')
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_read.py", line 38, in _need
    raise ValueError(message)
ValueError: record.law5_gate.ok is not JSON data

======================================================================
ERROR: test_every_recipe_scorer_field_is_plain_before_enrichment (c10x_enginepath_selftest.ScorerJsonTests.test_every_recipe_scorer_field_is_plain_before_enrichment) (kind='numpy')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 1791, in test_every_recipe_scorer_field_is_plain_before_enrichment
    with self.subTest(kind=kind):self.plain(observed);self.same_types(observed,wanted)
                                 ^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 1743, in plain
    R._finite_tree(value)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_read.py", line 85, in _finite_tree
    _finite_tree(child, path + '.' + key)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_read.py", line 85, in _finite_tree
    _finite_tree(child, path + '.' + key)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_read.py", line 92, in _finite_tree
    _need(value is None or type(value) in (str, bool, int), path + ' is not JSON data')
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_read.py", line 38, in _need
    raise ValueError(message)
ValueError: record.law5_gate.ok is not JSON data

======================================================================
ERROR: test_every_stage_rejects_non_json_before_next_stage (c10x_enginepath_selftest.ScorerJsonTests.test_every_stage_rejects_non_json_before_next_stage) (stage='final')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 1915, in test_every_stage_rejects_non_json_before_next_stage
    self.assertEqual(result['stage'],stage);self.assertTrue(result['phase'].startswith(stage+':'))
                     ~~~~~~^^^^^^^^^
KeyError: 'stage'

======================================================================
ERROR: test_injection_flags_and_counts_use_plain_scalars (c10x_enginepath_selftest.ScorerJsonTests.test_injection_flags_and_counts_use_plain_scalars) (kind='torch')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 1801, in test_injection_flags_and_counts_use_plain_scalars
    self.plain(rec);self.assertIs(type(rec['canon_n']),int);self.assertEqual(rec['canon_n'],24)
    ^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 1743, in plain
    R._finite_tree(value)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_read.py", line 85, in _finite_tree
    _finite_tree(child, path + '.' + key)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_read.py", line 92, in _finite_tree
    _need(value is None or type(value) in (str, bool, int), path + ' is not JSON data')
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_read.py", line 38, in _need
    raise ValueError(message)
ValueError: record.canon_n is not JSON data

======================================================================
ERROR: test_injection_flags_and_counts_use_plain_scalars (c10x_enginepath_selftest.ScorerJsonTests.test_injection_flags_and_counts_use_plain_scalars) (kind='numpy')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 1801, in test_injection_flags_and_counts_use_plain_scalars
    self.plain(rec);self.assertIs(type(rec['canon_n']),int);self.assertEqual(rec['canon_n'],24)
    ^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 1743, in plain
    R._finite_tree(value)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_read.py", line 85, in _finite_tree
    _finite_tree(child, path + '.' + key)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_read.py", line 92, in _finite_tree
    _need(value is None or type(value) in (str, bool, int), path + ' is not JSON data')
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_read.py", line 38, in _need
    raise ValueError(message)
ValueError: record.canon_n is not JSON data

======================================================================
ERROR: test_probe_tensor_targets_and_numpy_top1_are_plain (c10x_enginepath_selftest.ScorerJsonTests.test_probe_tensor_targets_and_numpy_top1_are_plain) (kind='torch')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 1811, in test_probe_tensor_targets_and_numpy_top1_are_plain
    self.plain(rec)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 1743, in plain
    R._finite_tree(value)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_read.py", line 85, in _finite_tree
    _finite_tree(child, path + '.' + key)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_read.py", line 85, in _finite_tree
    _finite_tree(child, path + '.' + key)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_read.py", line 85, in _finite_tree
    _finite_tree(child, path + '.' + key)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_read.py", line 88, in _finite_tree
    _finite_tree(child, path + '[' + str(i) + ']')
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_read.py", line 85, in _finite_tree
    _finite_tree(child, path + '.' + key)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_read.py", line 92, in _finite_tree
    _need(value is None or type(value) in (str, bool, int), path + ' is not JSON data')
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_read.py", line 38, in _need
    raise ValueError(message)
ValueError: record.frames.The capital of {} is the city of.rows[0].top1 is not JSON data

======================================================================
ERROR: test_probe_tensor_targets_and_numpy_top1_are_plain (c10x_enginepath_selftest.ScorerJsonTests.test_probe_tensor_targets_and_numpy_top1_are_plain) (kind='numpy')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 1811, in test_probe_tensor_targets_and_numpy_top1_are_plain
    self.plain(rec)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 1743, in plain
    R._finite_tree(value)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_read.py", line 85, in _finite_tree
    _finite_tree(child, path + '.' + key)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_read.py", line 85, in _finite_tree
    _finite_tree(child, path + '.' + key)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_read.py", line 85, in _finite_tree
    _finite_tree(child, path + '.' + key)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_read.py", line 88, in _finite_tree
    _finite_tree(child, path + '[' + str(i) + ']')
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_read.py", line 85, in _finite_tree
    _finite_tree(child, path + '.' + key)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_read.py", line 92, in _finite_tree
    _need(value is None or type(value) in (str, bool, int), path + ' is not JSON data')
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_read.py", line 38, in _need
    raise ValueError(message)
ValueError: record.frames.The capital of {} is the city of.rows[0].top1 is not JSON data

======================================================================
ERROR: test_raw_law5_locality_diagnostic_is_plain (c10x_enginepath_selftest.ScorerJsonTests.test_raw_law5_locality_diagnostic_is_plain) (kind='torch')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 1849, in test_raw_law5_locality_diagnostic_is_plain
    with self.subTest(kind=kind):self.plain(audit);self.assertIs(type(audit['raw_loc_delta']),float)
                                 ^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 1743, in plain
    R._finite_tree(value)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_read.py", line 85, in _finite_tree
    _finite_tree(child, path + '.' + key)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_read.py", line 92, in _finite_tree
    _need(value is None or type(value) in (str, bool, int), path + ' is not JSON data')
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_read.py", line 38, in _need
    raise ValueError(message)
ValueError: record.raw_loc_delta is not JSON data

======================================================================
ERROR: test_raw_law5_locality_diagnostic_is_plain (c10x_enginepath_selftest.ScorerJsonTests.test_raw_law5_locality_diagnostic_is_plain) (kind='numpy')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 1849, in test_raw_law5_locality_diagnostic_is_plain
    with self.subTest(kind=kind):self.plain(audit);self.assertIs(type(audit['raw_loc_delta']),float)
                                 ^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 1743, in plain
    R._finite_tree(value)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_read.py", line 85, in _finite_tree
    _finite_tree(child, path + '.' + key)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_read.py", line 92, in _finite_tree
    _need(value is None or type(value) in (str, bool, int), path + ' is not JSON data')
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_read.py", line 38, in _need
    raise ValueError(message)
ValueError: record.raw_loc_delta is not JSON data

======================================================================
ERROR: test_supervisor_propagates_worker_traceback_and_phase (c10x_enginepath_selftest.ScorerJsonTests.test_supervisor_propagates_worker_traceback_and_phase)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 1950, in test_supervisor_propagates_worker_traceback_and_phase
    self.assertEqual(diag['traceback'],result['traceback']);self.assertEqual(diag['phase'],result['phase'])
                     ~~~~^^^^^^^^^^^^^
KeyError: 'traceback'

======================================================================
ERROR: test_supervisor_timeout_has_phase_and_explicit_traceback_absence (c10x_enginepath_selftest.ScorerJsonTests.test_supervisor_timeout_has_phase_and_explicit_traceback_absence)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 1941, in test_supervisor_timeout_has_phase_and_explicit_traceback_absence
    self.assertEqual(diag['stage'],'inertness');self.assertIn('inertness',diag['phase'])
                     ~~~~^^^^^^^^^
KeyError: 'stage'

======================================================================
FAIL: test_boundary_keeps_strict_types_and_numeric_limits (c10x_enginepath_selftest.ScorerJsonTests.test_boundary_keeps_strict_types_and_numeric_limits) (i=0)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 1926, in test_boundary_keeps_strict_types_and_numeric_limits
    self.assertEqual(entered,list(A.CAPS)[:4])
AssertionError: Lists differ: ['setup', 'A', 'targets', 'inertness', 'injection', 'I-2', 'I-1', 'final'] != ['setup', 'A', 'targets', 'inertness']

First list contains 4 additional elements.
First extra element 4:
'injection'

- ['setup', 'A', 'targets', 'inertness', 'injection', 'I-2', 'I-1', 'final']
+ ['setup', 'A', 'targets', 'inertness']

======================================================================
FAIL: test_boundary_keeps_strict_types_and_numeric_limits (c10x_enginepath_selftest.ScorerJsonTests.test_boundary_keeps_strict_types_and_numeric_limits) (i=1)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 1926, in test_boundary_keeps_strict_types_and_numeric_limits
    self.assertEqual(entered,list(A.CAPS)[:4])
AssertionError: Lists differ: ['setup', 'A', 'targets', 'inertness', 'injection', 'I-2', 'I-1', 'final'] != ['setup', 'A', 'targets', 'inertness']

First list contains 4 additional elements.
First extra element 4:
'injection'

- ['setup', 'A', 'targets', 'inertness', 'injection', 'I-2', 'I-1', 'final']
+ ['setup', 'A', 'targets', 'inertness']

======================================================================
FAIL: test_boundary_keeps_strict_types_and_numeric_limits (c10x_enginepath_selftest.ScorerJsonTests.test_boundary_keeps_strict_types_and_numeric_limits) (i=2)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 1926, in test_boundary_keeps_strict_types_and_numeric_limits
    self.assertEqual(entered,list(A.CAPS)[:4])
AssertionError: Lists differ: ['setup', 'A', 'targets', 'inertness', 'injection', 'I-2', 'I-1', 'final'] != ['setup', 'A', 'targets', 'inertness']

First list contains 4 additional elements.
First extra element 4:
'injection'

- ['setup', 'A', 'targets', 'inertness', 'injection', 'I-2', 'I-1', 'final']
+ ['setup', 'A', 'targets', 'inertness']

======================================================================
FAIL: test_boundary_keeps_strict_types_and_numeric_limits (c10x_enginepath_selftest.ScorerJsonTests.test_boundary_keeps_strict_types_and_numeric_limits) (i=3)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 1926, in test_boundary_keeps_strict_types_and_numeric_limits
    self.assertEqual(entered,list(A.CAPS)[:4])
AssertionError: Lists differ: ['setup', 'A', 'targets', 'inertness', 'injection', 'I-2', 'I-1', 'final'] != ['setup', 'A', 'targets', 'inertness']

First list contains 4 additional elements.
First extra element 4:
'injection'

- ['setup', 'A', 'targets', 'inertness', 'injection', 'I-2', 'I-1', 'final']
+ ['setup', 'A', 'targets', 'inertness']

======================================================================
FAIL: test_boundary_keeps_strict_types_and_numeric_limits (c10x_enginepath_selftest.ScorerJsonTests.test_boundary_keeps_strict_types_and_numeric_limits) (i=4)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 1926, in test_boundary_keeps_strict_types_and_numeric_limits
    self.assertEqual(entered,list(A.CAPS)[:4])
AssertionError: Lists differ: ['setup', 'A', 'targets', 'inertness', 'injection', 'I-2', 'I-1', 'final'] != ['setup', 'A', 'targets', 'inertness']

First list contains 4 additional elements.
First extra element 4:
'injection'

- ['setup', 'A', 'targets', 'inertness', 'injection', 'I-2', 'I-1', 'final']
+ ['setup', 'A', 'targets', 'inertness']

======================================================================
FAIL: test_boundary_keeps_strict_types_and_numeric_limits (c10x_enginepath_selftest.ScorerJsonTests.test_boundary_keeps_strict_types_and_numeric_limits) (i=5)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 1926, in test_boundary_keeps_strict_types_and_numeric_limits
    self.assertEqual(entered,list(A.CAPS)[:4])
AssertionError: Lists differ: ['setup', 'A', 'targets', 'inertness', 'injection', 'I-2', 'I-1', 'final'] != ['setup', 'A', 'targets', 'inertness']

First list contains 4 additional elements.
First extra element 4:
'injection'

- ['setup', 'A', 'targets', 'inertness', 'injection', 'I-2', 'I-1', 'final']
+ ['setup', 'A', 'targets', 'inertness']

======================================================================
FAIL: test_driver_normalizes_pristine_report_and_completes (c10x_enginepath_selftest.ScorerJsonTests.test_driver_normalizes_pristine_report_and_completes) (kind='torch')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 1898, in test_driver_normalizes_pristine_report_and_completes
    self.assertEqual(result['status'],'COMPLETE',result.get('code'))
AssertionError: 'HALTED' != 'COMPLETE'
- HALTED
+ COMPLETE
 : STIMULUS_LEAK

======================================================================
FAIL: test_driver_normalizes_pristine_report_and_completes (c10x_enginepath_selftest.ScorerJsonTests.test_driver_normalizes_pristine_report_and_completes) (kind='numpy')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 1898, in test_driver_normalizes_pristine_report_and_completes
    self.assertEqual(result['status'],'COMPLETE',result.get('code'))
AssertionError: 'HALTED' != 'COMPLETE'
- HALTED
+ COMPLETE
 : STIMULUS_LEAK

======================================================================
FAIL: test_every_stage_rejects_non_json_before_next_stage (c10x_enginepath_selftest.ScorerJsonTests.test_every_stage_rejects_non_json_before_next_stage) (stage='setup')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 1914, in test_every_stage_rejects_non_json_before_next_stage
    self.assertEqual(entered,list(A.CAPS)[:list(A.CAPS).index(stage)+1])
AssertionError: Lists differ: ['setup', 'A', 'targets', 'inertness', 'injection', 'I-2', 'I-1', 'final'] != ['setup']

First list contains 7 additional elements.
First extra element 1:
'A'

- ['setup', 'A', 'targets', 'inertness', 'injection', 'I-2', 'I-1', 'final']
+ ['setup']

======================================================================
FAIL: test_every_stage_rejects_non_json_before_next_stage (c10x_enginepath_selftest.ScorerJsonTests.test_every_stage_rejects_non_json_before_next_stage) (stage='A')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 1913, in test_every_stage_rejects_non_json_before_next_stage
    self.assertEqual(result['status'],'HALTED');self.assertIn(path,result['code'])
                                                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'record.recipes.A.bad_json' not found in 'LAW3_BASELINE_MISS'

======================================================================
FAIL: test_every_stage_rejects_non_json_before_next_stage (c10x_enginepath_selftest.ScorerJsonTests.test_every_stage_rejects_non_json_before_next_stage) (stage='targets')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 1913, in test_every_stage_rejects_non_json_before_next_stage
    self.assertEqual(result['status'],'HALTED');self.assertIn(path,result['code'])
                                                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'record.targets.bad_json' not found in 'invalid index to scalar variable.'

======================================================================
FAIL: test_every_stage_rejects_non_json_before_next_stage (c10x_enginepath_selftest.ScorerJsonTests.test_every_stage_rejects_non_json_before_next_stage) (stage='inertness')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 1914, in test_every_stage_rejects_non_json_before_next_stage
    self.assertEqual(entered,list(A.CAPS)[:list(A.CAPS).index(stage)+1])
AssertionError: Lists differ: ['setup', 'A', 'targets', 'inertness', 'injection', 'I-2', 'I-1', 'final'] != ['setup', 'A', 'targets', 'inertness']

First list contains 4 additional elements.
First extra element 4:
'injection'

- ['setup', 'A', 'targets', 'inertness', 'injection', 'I-2', 'I-1', 'final']
+ ['setup', 'A', 'targets', 'inertness']

======================================================================
FAIL: test_every_stage_rejects_non_json_before_next_stage (c10x_enginepath_selftest.ScorerJsonTests.test_every_stage_rejects_non_json_before_next_stage) (stage='injection')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 1914, in test_every_stage_rejects_non_json_before_next_stage
    self.assertEqual(entered,list(A.CAPS)[:list(A.CAPS).index(stage)+1])
AssertionError: Lists differ: ['setup', 'A', 'targets', 'inertness', 'injection', 'I-2', 'I-1', 'final'] != ['setup', 'A', 'targets', 'inertness', 'injection']

First list contains 3 additional elements.
First extra element 5:
'I-2'

- ['setup', 'A', 'targets', 'inertness', 'injection', 'I-2', 'I-1', 'final']
?                                                   -----------------------

+ ['setup', 'A', 'targets', 'inertness', 'injection']

======================================================================
FAIL: test_every_stage_rejects_non_json_before_next_stage (c10x_enginepath_selftest.ScorerJsonTests.test_every_stage_rejects_non_json_before_next_stage) (stage='I-2')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 1914, in test_every_stage_rejects_non_json_before_next_stage
    self.assertEqual(entered,list(A.CAPS)[:list(A.CAPS).index(stage)+1])
AssertionError: Lists differ: ['setup', 'A', 'targets', 'inertness', 'injection', 'I-2', 'I-1', 'final'] != ['setup', 'A', 'targets', 'inertness', 'injection', 'I-2']

First list contains 2 additional elements.
First extra element 6:
'I-1'

- ['setup', 'A', 'targets', 'inertness', 'injection', 'I-2', 'I-1', 'final']
?                                                          ----------------

+ ['setup', 'A', 'targets', 'inertness', 'injection', 'I-2']

======================================================================
FAIL: test_every_stage_rejects_non_json_before_next_stage (c10x_enginepath_selftest.ScorerJsonTests.test_every_stage_rejects_non_json_before_next_stage) (stage='I-1')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 1914, in test_every_stage_rejects_non_json_before_next_stage
    self.assertEqual(entered,list(A.CAPS)[:list(A.CAPS).index(stage)+1])
AssertionError: Lists differ: ['setup', 'A', 'targets', 'inertness', 'injection', 'I-2', 'I-1', 'final'] != ['setup', 'A', 'targets', 'inertness', 'injection', 'I-2', 'I-1']

First list contains 1 additional elements.
First extra element 7:
'final'

- ['setup', 'A', 'targets', 'inertness', 'injection', 'I-2', 'I-1', 'final']
?                                                                 ---------

+ ['setup', 'A', 'targets', 'inertness', 'injection', 'I-2', 'I-1']

======================================================================
FAIL: test_telemetry_scalar_ids_and_flags_do_not_disable_writer (c10x_enginepath_selftest.ScorerJsonTests.test_telemetry_scalar_ids_and_flags_do_not_disable_writer) (kind='torch')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 1824, in test_telemetry_scalar_ids_and_flags_do_not_disable_writer
    self.assertTrue(writer.enabled);answer=[r for r in writer.lines if r['kind']=='answer']
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: False is not true

======================================================================
FAIL: test_telemetry_scalar_ids_and_flags_do_not_disable_writer (c10x_enginepath_selftest.ScorerJsonTests.test_telemetry_scalar_ids_and_flags_do_not_disable_writer) (kind='numpy')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 1824, in test_telemetry_scalar_ids_and_flags_do_not_disable_writer
    self.assertTrue(writer.enabled);answer=[r for r in writer.lines if r['kind']=='answer']
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: False is not true

----------------------------------------------------------------------
Ran 12 tests in 0.601s

FAILED (failures=17, errors=14)
```

Additional review regression RED:

```sh
cd /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a
env TMPDIR=/private/tmp/c10x_build PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONPATH=experiments/track_c .venv/bin/python -B -m unittest c10x_enginepath_selftest.ScorerJsonTests.test_previous_stage_deadline_keeps_exit_phase
```

```text
F
======================================================================
FAIL: test_previous_stage_deadline_keeps_exit_phase (c10x_enginepath_selftest.ScorerJsonTests.test_previous_stage_deadline_keeps_exit_phase)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py", line 1939, in test_previous_stage_deadline_keeps_exit_phase
    self.assertEqual(result['stage'],'A');self.assertEqual(result['phase'],'A:exit')
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'targets' != 'A'
- targets
+ A


----------------------------------------------------------------------
Ran 1 test in 0.042s

FAILED (failures=1)
```

The first corrected focused suite passed 12; the reviewed transition fix's focused suite passed 13. After adding the wrapped large-integer sentinel, the final full suite was run against the final hashes below. An intermediate 95-test full suite also passed before the attribution regression/correction; it is not the final-source receipt.

Final full-suite command (exit **0**; full PASS stdout/stderr follows):

```sh
cd /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a
env TMPDIR=/private/tmp/c10x_build PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 .venv/bin/python -B experiments/track_c/c10x_enginepath_selftest.py > /private/tmp/c10x_build/scorer_json_fix/full_selftest_final.log 2>&1
```

```text
test_admitted_process_pair_and_p2_gate (__main__.FileAdmissionTests.test_admitted_process_pair_and_p2_gate) ... ok
test_amendment_p_digest_refusals (__main__.FileAdmissionTests.test_amendment_p_digest_refusals) ... ok
test_amendment_p_prereg_pin (__main__.FileAdmissionTests.test_amendment_p_prereg_pin) ... ok
test_answer_audit_uses_runtime_recipe_order (__main__.FileAdmissionTests.test_answer_audit_uses_runtime_recipe_order) ... ok
test_complete_stub_run_persists_every_record (__main__.FileAdmissionTests.test_complete_stub_run_persists_every_record) ... ok
test_context_binding_enter_failure_restores (__main__.FileAdmissionTests.test_context_binding_enter_failure_restores) ... ok
test_deadline_completion_and_previous_overhead (__main__.FileAdmissionTests.test_deadline_completion_and_previous_overhead) ... ok
test_detailed_admission_negative_controls (__main__.FileAdmissionTests.test_detailed_admission_negative_controls) ... ok
test_direct_shell_launchers_are_executable_in_git (__main__.FileAdmissionTests.test_direct_shell_launchers_are_executable_in_git) ... DIRECT SHELL ENTRY POINTS: none; all three supervised commands use sys.executable
ok
test_disable_cutoff_never_excuses_earlier_omissions (__main__.FileAdmissionTests.test_disable_cutoff_never_excuses_earlier_omissions) ... ok
test_disable_marker_records_failed_answer_cutoff (__main__.FileAdmissionTests.test_disable_marker_records_failed_answer_cutoff) ... ok
test_every_science_record_roundtrip_and_reader_audit (__main__.FileAdmissionTests.test_every_science_record_roundtrip_and_reader_audit) ... ok
test_fp32_overflow_capture_and_parity_remain_report_only (__main__.FileAdmissionTests.test_fp32_overflow_capture_and_parity_remain_report_only) ... ok
test_frozen_scorer_forwards_have_no_injected_kwargs (__main__.FileAdmissionTests.test_frozen_scorer_forwards_have_no_injected_kwargs) ... ok
test_late_supervisor_persistence_is_unreadable (__main__.FileAdmissionTests.test_late_supervisor_persistence_is_unreadable) ... ok
test_missing_inertness_evidence_is_refused (__main__.FileAdmissionTests.test_missing_inertness_evidence_is_refused) ... ok
test_no_combined_device_dtype_conversions (__main__.FileAdmissionTests.test_no_combined_device_dtype_conversions) ... ok
test_pinned_contexts_never_sample (__main__.FileAdmissionTests.test_pinned_contexts_never_sample) ... ok
test_pinned_processes_and_halted_context_identity (__main__.FileAdmissionTests.test_pinned_processes_and_halted_context_identity) ... ok
test_post_audit_blocks_are_killed_by_final_deadline (__main__.FileAdmissionTests.test_post_audit_blocks_are_killed_by_final_deadline) ... ok
test_post_audit_budget_and_disabled_disposition (__main__.FileAdmissionTests.test_post_audit_budget_and_disabled_disposition) ... ok
test_post_audit_rejects_contradictory_receipts (__main__.FileAdmissionTests.test_post_audit_rejects_contradictory_receipts) ... ok
test_post_audit_startup_consumes_remaining_budget (__main__.FileAdmissionTests.test_post_audit_startup_consumes_remaining_budget) ... ok
test_reader_publishes_invalid_with_exit_zero (__main__.FileAdmissionTests.test_reader_publishes_invalid_with_exit_zero) ... ok
test_recipe_fp32_overflow_does_not_halt_or_change_labels (__main__.FileAdmissionTests.test_recipe_fp32_overflow_does_not_halt_or_change_labels) ... ok
test_script_alias_and_preflight_refusal_in_isolated_child (__main__.FileAdmissionTests.test_script_alias_and_preflight_refusal_in_isolated_child) ... ok
test_signed_zero_reader_keeps_reports_out_of_admission (__main__.FileAdmissionTests.test_signed_zero_reader_keeps_reports_out_of_admission) ... ok
test_supervisor_fail_closed_and_combining_output_path (__main__.FileAdmissionTests.test_supervisor_fail_closed_and_combining_output_path) ... ok
test_tagged_fp32_diagnostics_preserve_file_admission (__main__.FileAdmissionTests.test_tagged_fp32_diagnostics_preserve_file_admission) ... ok
test_tokenizer_forwards_preserve_attention_mask (__main__.FileAdmissionTests.test_tokenizer_forwards_preserve_attention_mask) ... ok
test_actual_fe_writes_and_null_solve_observer (__main__.IntegrationTests.test_actual_fe_writes_and_null_solve_observer) ... ok
test_actual_singleton_reduction_and_resolved_capture (__main__.IntegrationTests.test_actual_singleton_reduction_and_resolved_capture) ... ok
test_projection_uses_remaining_units_and_setup_clock (__main__.IntegrationTests.test_projection_uses_remaining_units_and_setup_clock) ... ok
test_solver_masked_gradient_clip_filter_and_tie (__main__.IntegrationTests.test_solver_masked_gradient_clip_filter_and_tie) ... ok
test_telemetry_recipe_records_and_counts_equal (__main__.IntegrationTests.test_telemetry_recipe_records_and_counts_equal) ... ok
test_telemetry_valid_admission_and_runner_no_writes (__main__.IntegrationTests.test_telemetry_valid_admission_and_runner_no_writes) ... ok
test_three_recipe_telemetry_probe_and_file_equality (__main__.IntegrationTests.test_three_recipe_telemetry_probe_and_file_equality) ... ok
test_reader_control_boundaries (__main__.ReaderTests.test_reader_control_boundaries) ... ok
test_reader_count_classes (__main__.ReaderTests.test_reader_count_classes) ... ok
test_reader_flags_denominators_nulls (__main__.ReaderTests.test_reader_flags_denominators_nulls) ... ok
test_reader_interpretation_and_null_table (__main__.ReaderTests.test_reader_interpretation_and_null_table) ... ok
test_reader_law3_boundaries (__main__.ReaderTests.test_reader_law3_boundaries) ... ok
test_reader_locality_boundaries (__main__.ReaderTests.test_reader_locality_boundaries) ... ok
test_reader_process_combination (__main__.ReaderTests.test_reader_process_combination) ... ok
test_reader_qualifier_boundaries (__main__.ReaderTests.test_reader_qualifier_boundaries) ... ok
test_reader_replication (__main__.ReaderTests.test_reader_replication) ... ok
test_reader_validity (__main__.ReaderTests.test_reader_validity) ... ok
test_actual_harness_flags_are_plain_in_writer_record (__main__.ScorerJsonTests.test_actual_harness_flags_are_plain_in_writer_record) ... ok
test_boundary_keeps_strict_types_and_numeric_limits (__main__.ScorerJsonTests.test_boundary_keeps_strict_types_and_numeric_limits) ... ok
test_direct_g8_observer_materializes_scalars (__main__.ScorerJsonTests.test_direct_g8_observer_materializes_scalars) ... ok
test_driver_normalizes_pristine_report_and_completes (__main__.ScorerJsonTests.test_driver_normalizes_pristine_report_and_completes) ... ok
test_every_recipe_scorer_field_is_plain_before_enrichment (__main__.ScorerJsonTests.test_every_recipe_scorer_field_is_plain_before_enrichment) ... ok
test_every_stage_rejects_non_json_before_next_stage (__main__.ScorerJsonTests.test_every_stage_rejects_non_json_before_next_stage) ... ok
test_injection_flags_and_counts_use_plain_scalars (__main__.ScorerJsonTests.test_injection_flags_and_counts_use_plain_scalars) ... ok
test_previous_stage_deadline_keeps_exit_phase (__main__.ScorerJsonTests.test_previous_stage_deadline_keeps_exit_phase) ... ok
test_probe_tensor_targets_and_numpy_top1_are_plain (__main__.ScorerJsonTests.test_probe_tensor_targets_and_numpy_top1_are_plain) ... ok
test_raw_law5_locality_diagnostic_is_plain (__main__.ScorerJsonTests.test_raw_law5_locality_diagnostic_is_plain) ... ok
test_supervisor_propagates_worker_traceback_and_phase (__main__.ScorerJsonTests.test_supervisor_propagates_worker_traceback_and_phase) ... ok
test_supervisor_timeout_has_phase_and_explicit_traceback_absence (__main__.ScorerJsonTests.test_supervisor_timeout_has_phase_and_explicit_traceback_absence) ... ok
test_telemetry_scalar_ids_and_flags_do_not_disable_writer (__main__.ScorerJsonTests.test_telemetry_scalar_ids_and_flags_do_not_disable_writer) ... ok
test_active_null_negative_controls (__main__.SeamTests.test_active_null_negative_controls) ... ok
test_baseline_miss_stops_candidates (__main__.SeamTests.test_baseline_miss_stops_candidates) ... ok
test_capture_bindings_identity_attribution (__main__.SeamTests.test_capture_bindings_identity_attribution) ... ok
test_dispatch_call_time_flag (__main__.SeamTests.test_dispatch_call_time_flag) ... ok
test_fe_ast_three_changes (__main__.SeamTests.test_fe_ast_three_changes) ... ok
test_fe_modes_and_keys (__main__.SeamTests.test_fe_modes_and_keys) ... ok
test_float64_dense_reference (__main__.SeamTests.test_float64_dense_reference) ... ok
test_independent_full_vocabulary_audit (__main__.SeamTests.test_independent_full_vocabulary_audit) ... ok
test_knobs_and_frame_subjects (__main__.SeamTests.test_knobs_and_frame_subjects) ... ok
test_launch_refusals (__main__.SeamTests.test_launch_refusals) ... ok
test_pristine_hash_restore_hooks (__main__.SeamTests.test_pristine_hash_restore_hooks) ... ok
test_process2_requires_eligibility (__main__.SeamTests.test_process2_requires_eligibility) ... ok
test_recipe_states_counters (__main__.SeamTests.test_recipe_states_counters) ... ok
test_solver_ast_and_gradients (__main__.SeamTests.test_solver_ast_and_gradients) ... ok
test_tolerance_and_finiteness (__main__.SeamTests.test_tolerance_and_finiteness) ... ok
test_watchdog_and_projection (__main__.SeamTests.test_watchdog_and_projection) ... ok
test_after_cell_halt_keeps_pre_restoration_measurements (__main__.SignedZeroTests.test_after_cell_halt_keeps_pre_restoration_measurements) ... ok
test_amendment_z_prereg_pin (__main__.SignedZeroTests.test_amendment_z_prereg_pin) ... ok
test_driver_halt_serializes_measured_x2_values (__main__.SignedZeroTests.test_driver_halt_serializes_measured_x2_values) ... ok
test_equal_values_wrong_dtype_halt (__main__.SignedZeroTests.test_equal_values_wrong_dtype_halt) ... ok
test_nan_value_halts (__main__.SignedZeroTests.test_nan_value_halts) ... ok
test_nonzero_update_halts_before_weight_comparison (__main__.SignedZeroTests.test_nonzero_update_halts_before_weight_comparison) ... ok
test_one_ulp_value_change_halts_with_all_layer_measurements (__main__.SignedZeroTests.test_one_ulp_value_change_halts_with_all_layer_measurements) ... ok
test_signed_zero_write_passes_and_counts_binary16_bits (__main__.SignedZeroTests.test_signed_zero_write_passes_and_counts_binary16_bits) ... ok
test_w0_byte_identity_stays_strict_before_and_after_null_cell (__main__.SignedZeroTests.test_w0_byte_identity_stays_strict_before_and_after_null_cell) ... ok
test_wrong_shape_halts (__main__.SignedZeroTests.test_wrong_shape_halts) ... ok
test_frozen_bytes_and_imports (__main__.TelemetryTests.test_frozen_bytes_and_imports) ... IMPORT GUARD PASS: c10e_bandknob, transformers, datasets absent
ok
test_isolation_positive_control_children_meta (__main__.TelemetryTests.test_isolation_positive_control_children_meta) ... ok
test_post_run_answer_audit (__main__.TelemetryTests.test_post_run_answer_audit) ... ok
test_strict_json_roundtrips (__main__.TelemetryTests.test_strict_json_roundtrips) ... ok
test_telemetry_code_path_equality (__main__.TelemetryTests.test_telemetry_code_path_equality) ... ok
test_telemetry_failure_boundaries (__main__.TelemetryTests.test_telemetry_failure_boundaries) ... ok
test_telemetry_inertness_schedule (__main__.TelemetryTests.test_telemetry_inertness_schedule) ... ok
test_telemetry_line_volume (__main__.TelemetryTests.test_telemetry_line_volume) ... ok
test_telemetry_state_unchanged (__main__.TelemetryTests.test_telemetry_state_unchanged) ... ok
test_telemetry_switch_admission (__main__.TelemetryTests.test_telemetry_switch_admission) ... ok

----------------------------------------------------------------------
Ran 96 tests in 22.098s

OK
LISTING: attributed-protected changes = {}
LISTING: observed/unattributed other changes = {}
SYS.MODULES PASS: c10e_bandknob/transformers/datasets absent
```

**96 tests in 22.098 s; zero failures/errors.** Attributed protected listing changes: **0**. Other observed listing changes during the final selftest: **0**. `c10e_bandknob`, `transformers`, and `datasets` absent from `sys.modules`. Model/forward work is exclusively the tiny CPU fixture; dispatch stubs and outputs are under private temporary roots. The final suite includes the earlier M non-finite report-only, T11 cutoff, safe MPS-conversion AST bans, scorer/mask revert, deadline, pinned-context regeneration and signed-zero regressions. No historical mutation campaign or live experiment was rerun; existing mutation evidence remains historical.

Read-only engine fingerprint command (exit **0**):

```sh
env LLMDB_ROOT=/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a TMPDIR=/private/tmp/c10x_build PYTHONDONTWRITEBYTECODE=1 /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python -B /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/engine_fingerprint.py
```

```text
engine fingerprint PASS: /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/memit_dry_run/memit/memit/memit_main.py
  sha256   d941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65  (expected d941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65; pod-era 5c0c706a…)
  _cov_cpu 3  (expected 3)
```

### Scope, immutable science and byte preservation

Only **three existing C10X sources** change in this arc: arms, inertness, selftest; this report is appended. No new project source file. The named driver/reader/harness/engine are not replaced wholesale. Source AST comparison confirms all scientific `require` calls in arms/inertness are unchanged, every inertness function except record-only `write_cell`/`direct_g8` is AST-identical (including all of `run_checks`, null observer, signed-zero/value/dtype/shape checks, thresholds, negative controls and Pristine), and driver writer/target/context/scorer/lens/T8/StageBudget functions are AST-identical. All forward call sites/arguments, original and observed scorer bodies, actual target construction, weight restoration and W0/T8 byte checks are preserved. The only `batch_replay` change is exported index scalar materialization. Amendments M, T11, P, Z and prior safe conversion/mask-revert fixes remain intact. The reader, telemetry checker, overtone solver, X2 probe and prereg are byte-identical to this task's snapshot.

**All 188 R5 hashes equal before and after.** `git diff --quiet -- <all 188 frozen R5 paths>` returns **0**. Complete before/current tables are also stored in `before.json` and `sealed_evidence.json`; this is the full R5 table, with the single listed SHA being both the before and after value:

| Protected R5 path | Before SHA-256 = after SHA-256 |
| --- | --- |
| `configs/hparams/anyedit_alphaedit_are_qwen25_3b.json` | `b7c8635b5ae876bb8a346ac2bc36d1ec438c2639021faebbdc838a046257f41e` |
| `configs/hparams/anyedit_memit_are_qwen25_3b.json` | `c0774c602a28ece1425c83edc9f4da243b7908efdac1642a54e093fd26f16c8b` |
| `configs/hparams/cfb-v4-highAKD-v0_1-draft.yaml` | `495415f88ebc0882bbe28ed8b11a3e6f2e76884fec3f2d485975093e984aae9c` |
| `configs/hparams/cfb-v4-highAKD.yaml` | `e3ce9cb8690f70ba4d7335cf1a11679a8d79fa9563c3ef9ffca9840e9fb1e30f` |
| `configs/hparams/llama32_3b_memit_hparams.json` | `24a22192538cc9092925f78b6e93f3e3129cdc5513b1e0034c43386ead8ffb26` |
| `configs/hparams/probe-set-v4-highAKD.yaml` | `b99b5d9b8ed1d093869aed902be8464e41677d83a1c988ca3ae2150a1338d1fd` |
| `configs/hparams/qwen25_3b_memit_hparams.json` | `4225cc6aabc3eb9fa62d2bb2cac68b1238de3a39c5e469da635e6e1464aa3bb4` |
| `configs/hparams/qwen25_3b_memit_hparams_band412.json` | `7bdfae32d16f7cd8a53bc901642f6377476ebfa5c10d4d37fd69494c8cb2e618` |
| `configs/hparams/qwen25_3b_memit_hparams_band41218.json` | `191e6283056a6914c51ab0f8bf5629c72faf0bb84cff5ee25207f6b63e7705d5` |
| `configs/hparams/qwen25_3b_memit_hparams_band412_lowcov2500.json` | `df16866eb68327f465b0beee43b0b1b0a0c6dea5aa7a0c4f5700e864c2705f2b` |
| `configs/hparams/qwen25_3b_memit_hparams_band412_strength150.json` | `31337200e25891391427d21009829ef8d253c4fd384eedeeb5d2d9bfbd605dcd` |
| `configs/hparams/qwen25_3b_memit_hparams_band812.json` | `f9a8ee42e5cd91937d3fdab852e19e971c554da3a383d6dc4c9f305a2192d546` |
| `configs/hparams/qwen25_3b_memit_hparams_mom2w25.json` | `afb77fe8ab5241d7a33fd183121715d1b1389de905de741ad3cef6f98a197083` |
| `configs/hparams/qwen25_3b_memit_hparams_mom2w50.json` | `6d171a27d1c6dbaf6240c7e715be96caff954dd9f2958dd17b8b054c5dc85272` |
| `configs/hparams/qwen25_3b_memit_hparams_mom2w500.json` | `797d53e19889353eb57d122e8d54f1d3d22b46142658baa1858b3e43e755f8f9` |
| `configs/hparams/qwen25_3b_memit_hparams_set48.json` | `73c075619c2b9c43d870adae0d55c1e488f3a016b3e9ccc96dec71d8e7198be2` |
| `configs/hparams/qwen25_3b_memit_hparams_set78.json` | `93ce4befc96526da4fa2a85ce7f94c521927c83295bf850dd5ac9e84dc2ab256` |
| `configs/hparams/qwen25_3b_memit_hparams_smoke.json` | `bd11f757196eeebeda2c2eb597d449e1626882441036831c606ccd0f0428faac` |
| `configs/hparams/qwen25_3b_memit_hparams_steps50.json` | `f7a10f00eb1f7e37764aba0f6a231b3b0d316066f7f734f1e418a339acaeff33` |
| `configs/hparams/qwen25_3b_relkey_memit_hparams.json` | `343c54cd2d95c20990c56c15b90a9ac36cb45ef0c12a9a264166ff06a10d3bbf` |
| `configs/hparams/qwen25_7b_memit_hparams.json` | `81b2ccc7bddfd607ca1894efd5ef4bba9fb073f51b68024125307db65374e128` |
| `configs/hparams/qwen3_06b_memit_hparams.json` | `c22468894e3e2f20ae389f59342e5163f6894fb584486d8dced719c392a76aa7` |
| `configs/probes/b3_probes.json` | `9471d33901a042de842a99d1c84bd904ec2e6a24a2ee994630b7df34649d8a9b` |
| `configs/screens/g6_screen_qwen3b.json` | `a51813340571f6c68908ac4310cca197ebac9884939f58e5c33fb75833a3ca05` |
| `configs/screens/g6_screen_qwen3b_v2.json` | `482c05f8f33c59d3e469566fe6f3c48eb183d3cb2fbb791f31dcad7102517c5c` |
| `configs/screens/g6_screen_qwen7b.json` | `7c5a63282d8b815393e0a5dc3641dbfb61c5a0e95e530e4446f163816d75b43c` |
| `docs/C10X_ENGINEPATH_PREREG.md` | `d3dfdc8bd8a9c04894b63da9b51ead164e7667e40d8f08b29b11606078f92899` |
| `experiments/track_c/c10e_bandknob.py` | `1f6be5811d7e58f3ebda16867a4a174b1cf24d47f9a2514cf9c3f9d29f18e695` |
| `experiments/track_c/c10l_covgeom_p6_zinject.py` | `b2b94563628a16c63c74733a63a95783a1f0536fc0ca6800d97b409d2f86b43b` |
| `experiments/track_c/c10l_covgeom_step0.py` | `5999d8714b7282e01f04b0292dc2c381d383f2a7ff90a2430b6e503aa7f2a557` |
| `experiments/track_c/c10m_diag_arms.py` | `77efc1bd358fb34728ec46616ffa983f0bf890294a61789c29989749d2252eee` |
| `experiments/track_c/c10p_twopass_arms.py` | `c34ecbe17c86d8f2803efc5520f4cf090dcb23bcc21ef0c3c28a12bfdaeb820f` |
| `experiments/track_c/c10q_stacked_arms.py` | `9dec3185fd5dbcb08651023fba123b2238f761e7cb21ccb5033301054ef13731` |
| `memit_dry_run/memit/.gitattributes` | `0d8fc1b86a58cb959c95bc6d62652b6a06ec8a1161d0fab6af1bcabbde43b630` |
| `memit_dry_run/memit/.gitignore` | `8d0aba79068af0ed4093807588d236cfe576a1e7c08993549f65ec2e1cbc931b` |
| `memit_dry_run/memit/CITATION.cff` | `974adb58a9fd1e6a2375244d22c8601a3a614257b006c534863ade12056a9514` |
| `memit_dry_run/memit/LICENSE` | `46c273d5a0a7f8bc3889863398e1bb20493e256f38033dfd637ec46bf654c531` |
| `memit_dry_run/memit/README.md` | `e14b1c0aff11f1ebb5b427115cdd660892e0305bb868102c1330299017b69b13` |
| `memit_dry_run/memit/baselines/README.md` | `e44248aeb435f44301544b39c92195baa1367552978f9f20060a186c1c223e95` |
| `memit_dry_run/memit/baselines/ft/__init__.py` | `19646aa4d3c5b6fd8dc0032aab1cee6afc7ab24e7404c5c657cadbdd077ea0fd` |
| `memit_dry_run/memit/baselines/ft/ft_hparams.py` | `fdd83bbc0cb87ebc1b6aae238a38798aab6e2b8b1723e666e797c1c5df851ab1` |
| `memit_dry_run/memit/baselines/ft/ft_main.py` | `ce8bffb4716a6ec97c5690a10b7be585da6d009028f6d77c9ac7907caaea378a` |
| `memit_dry_run/memit/baselines/mend/README.md` | `43f8919beb3498934f0282763523db4f1b0825d98c103bbd4230fce52e756076` |
| `memit_dry_run/memit/baselines/mend/__init__.py` | `ce6f24b656aa412ba07c893dd6fa37001d0a148312c9fd5b823ac27c83e145b0` |
| `memit_dry_run/memit/baselines/mend/algs/enn.py` | `fcde13387249220bf8ccde0c8bf174f6444a956806f86aee0c4c1a0c062e3a90` |
| `memit_dry_run/memit/baselines/mend/algs/ft.py` | `c60355576cac69dbca0816a4747cbb7bbba7a2352d0e7edb2191d870450eeff7` |
| `memit_dry_run/memit/baselines/mend/algs/mend.py` | `3d94e338ff9efe07815d9d4d339485e9abaa17af555f88d0adacb0a3ad19eca5` |
| `memit_dry_run/memit/baselines/mend/config/alg/efk.yaml` | `6d8a009b23a6d15971f0fd3f41f446e55f9f439ddd4f37f37e003a9ba39c3d4b` |
| `memit_dry_run/memit/baselines/mend/config/alg/enn.yaml` | `5d57b48f592317500c828b93650db753917781cacae4b72afbaf6af7bcdfff96` |
| `memit_dry_run/memit/baselines/mend/config/alg/ft.yaml` | `f2ed848825e236de2073930e6bea4faf2ca1f6c828a7f84d79fad54a0b7e607d` |
| `memit_dry_run/memit/baselines/mend/config/alg/mend.yaml` | `bce5e203d627552b2caf8d1a3b185ccaf28773b285a17a9f27538a86fe9eea87` |
| `memit_dry_run/memit/baselines/mend/config/config.yaml` | `d46810afd50bf9dc19b443df22f7c77ee88ae03f7540bb7939b6eeaba4079d96` |
| `memit_dry_run/memit/baselines/mend/config/experiment/fc.yaml` | `678a899a35e0840de77f5fea74236c9f0d8b9ea4f0b8e1a05b981cfac131a043` |
| `memit_dry_run/memit/baselines/mend/config/experiment/gen.yaml` | `c208288115ae91d8cd47dfcc6c157e94d41657eebef327700363ed288f9dbee3` |
| `memit_dry_run/memit/baselines/mend/config/experiment/qa.yaml` | `038666cff47e927cc70891afcc2efd0f62898274d0287f1ab0719c3771394027` |
| `memit_dry_run/memit/baselines/mend/config/model/bart-base.yaml` | `25eac9c87259e197ecf587413f4660098b779c6b21fa1cc6584e7d64b1479475` |
| `memit_dry_run/memit/baselines/mend/config/model/bert-base.yaml` | `49ff1dc40a3306dd7649f697c134e6ed0f83e5382038f18962793f3eca410e01` |
| `memit_dry_run/memit/baselines/mend/config/model/distilgpt2.yaml` | `ba77ac0a70e92efac417a8f9b2aa25872f4c0152ae7e6bcb7a1a1c394e88a0d7` |
| `memit_dry_run/memit/baselines/mend/config/model/gpt2.yaml` | `6c9ac030faea26cfa57a21d10713298b5b05e2acfcda057db9ef8b7797e0182d` |
| `memit_dry_run/memit/baselines/mend/config/model/gpt2large.yaml` | `feeab1704c76f5917876da5c631940dfde806dfdf0bf37f704ae29e8081c016c` |
| `memit_dry_run/memit/baselines/mend/config/model/gpt2medium.yaml` | `a943050f9ad67b30e16e312d0a63b8dff6518a582e5c49d4f36475931dee5dc6` |
| `memit_dry_run/memit/baselines/mend/config/model/gpt2xl.yaml` | `5eb704b1c06b3636eb62db43614f87650412d08c2c6f374555187c194f031429` |
| `memit_dry_run/memit/baselines/mend/config/model/gptj.yaml` | `0f3fe0caa24560fc62ffe7c2752cc23b5216bf99291d0fe969a55026982e4868` |
| `memit_dry_run/memit/baselines/mend/config/model/gptneo27.yaml` | `809ce5da7d801f0b9c7ffc1b4b53632b23c7c8544f5dd1a401b8be4d3f17a46a` |
| `memit_dry_run/memit/baselines/mend/config/model/t5large.yaml` | `109cf49c1cb32333e492e79d9974fa3e75f8c9a0459d40c872571e4eb13c85d5` |
| `memit_dry_run/memit/baselines/mend/config/model/t5small.yaml` | `cee5cfbb9295137f1ecf154949c55f0f76254941d9cb48ecdd66bc6decd1a929` |
| `memit_dry_run/memit/baselines/mend/config/model/t5xl.yaml` | `e9611b81bd40bb80c21f462b195095deabab3d3d6ac344165ba16a3ec45bc5a6` |
| `memit_dry_run/memit/baselines/mend/config/model/t5xxl.yaml` | `690ee1486411befec7312a0e37ed4ef615a57e1c74e4f7bea39ed6f87530d427` |
| `memit_dry_run/memit/baselines/mend/data_classes/fever.py` | `098397ce1214eb8cce6b90c8ba6ebd67024afcbc2f58ccaf887b5a365732308a` |
| `memit_dry_run/memit/baselines/mend/data_classes/nq.py` | `f8d8dfaadf866e82c50e4c5bfef14a9b54aa5799aca3cea8f403f0461ba61f69` |
| `memit_dry_run/memit/baselines/mend/data_classes/wiki.py` | `60ea3f99dcb4386f38454fdda9b7a65963df76240ce516d093e396a969576627` |
| `memit_dry_run/memit/baselines/mend/data_classes/zsre.py` | `2acb707212802d65a55f46ada4381af330ff1cc9842ed9c56326de14b0711581` |
| `memit_dry_run/memit/baselines/mend/editable_model.py` | `34330a12b9864001ea46ecae794df1ea85cedb38082df783b31d67cc8939e245` |
| `memit_dry_run/memit/baselines/mend/hooks.py` | `b6037d8f9778f2d74952dafe3acc76f761df6884d85e9b5b57559cd08f7d2d6f` |
| `memit_dry_run/memit/baselines/mend/losses.py` | `271a10d9e995ffd92c2de239f652928d651013f8a0889bd4205ffca1469127e8` |
| `memit_dry_run/memit/baselines/mend/mend_hparams.py` | `071bc2c833cd1362906eee12b081c272650f909e9c93389bb05be86ae8626eb3` |
| `memit_dry_run/memit/baselines/mend/mend_main.py` | `7e72af6f626798696f50c81ad72276f4807422bd365d5d6f130ca7e2852f53b5` |
| `memit_dry_run/memit/baselines/mend/models.py` | `2e94d797f3813d57a532c676ba6609a91e89eb36bdfb8479bc092dccc5ce4420` |
| `memit_dry_run/memit/baselines/mend/nn.py` | `ffca4fb48675c4c6cf56bb9cbbff8ce50f2c46eb8fdbfc6a7e1b6308acddab92` |
| `memit_dry_run/memit/baselines/mend/oracle.py` | `d3657df3b292a4c78564c59b9a07ccdb8e6ff74b111cd489e38c5e5112ad4b1b` |
| `memit_dry_run/memit/baselines/mend/requirements.txt` | `17082daf26c99220b8bfff81f282ca445e19b6ee69835f31009a4ce0d0ed20cd` |
| `memit_dry_run/memit/baselines/mend/run.py` | `2e57976fb507bc5bc27f88ea8a7bacd7b2a75d6b45170ed4870643ae5ce74765` |
| `memit_dry_run/memit/baselines/mend/trainer.py` | `91c9d6378c0cbe6340cf4591618a68aa70f805059a01881f43c71859e001dcb1` |
| `memit_dry_run/memit/baselines/mend/utils.py` | `bb981c845c07709efa4e81610ec575be7e3f3b909a42b79610a47044c04c0554` |
| `memit_dry_run/memit/dsets/__init__.py` | `a2e1c9d7a56af0b091a48cb313a356cdb1a923e1bb046d73bd0d1e10c7b0d907` |
| `memit_dry_run/memit/dsets/attr_snippets.py` | `bf78972d9914919e0a0b7d7d93623b3f51b8684f691e909793b5cd5471d6f01a` |
| `memit_dry_run/memit/dsets/counterfact.py` | `7848e935a578c40e187167a2894601b0dbf42d2334b5289a012276ea1eb672b5` |
| `memit_dry_run/memit/dsets/knowns.py` | `e2428c36d17b0dec1f390888a98334bd0fd1f64168bffae7566ef8a8606f361e` |
| `memit_dry_run/memit/dsets/tfidf_stats.py` | `34f03d97b0b1aaad33e75a211a3d6b502cfb9eace1c172320df6ceb713d600c9` |
| `memit_dry_run/memit/dsets/zsre.py` | `a6281375afd9983337c154095fe9aba59c74c36fa34ecfb12838c7b5c341670e` |
| `memit_dry_run/memit/experiments/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `memit_dry_run/memit/experiments/causal_trace.py` | `9436fd596a39e240a01121da601359bea5d0b3a350c0faa34aa8b0ccac05560b` |
| `memit_dry_run/memit/experiments/evaluate.py` | `4ef8e138bb8003c8486935ad0eae86d9ccd84bb61cfa1f88b63f0ed06c2d1760` |
| `memit_dry_run/memit/experiments/py/demo.py` | `268c16a1c2c4e8642b7641739c2cd0808c08be80f36f280d1e5bef4944733772` |
| `memit_dry_run/memit/experiments/py/eval_utils_counterfact.py` | `b00d9810305580dddfeb5e65129db4d56bcbfee1edf020605e21bf4f5033aeb7` |
| `memit_dry_run/memit/experiments/py/eval_utils_zsre.py` | `e4f18c84a813d0a2fb9a5c9426726844117fe365cae72107d51f304a264d77a8` |
| `memit_dry_run/memit/experiments/summarize.py` | `7de8f5eec86243807825cf9f62923535f853cce07d2d3248534f86320f229372` |
| `memit_dry_run/memit/experiments/sweep.py` | `bfc7a91e9abb526814f7d975a81ff0333e930b452e2da58b31dc2ae8a10cce74` |
| `memit_dry_run/memit/globals.yml` | `86ab5194b3cddc19c14173a3b8f13563c554d252666eb563a4ac2f919e087459` |
| `memit_dry_run/memit/globals.yml.upstream_default.20260430T035736Z` | `f05226b5d0b64a25106fbfa2da3b4de3b69d8e6797c7757f8a6679756820845c` |
| `memit_dry_run/memit/hparams/FT/EleutherAI_gpt-j-6B_constr.json` | `018e27089431ed3632aa0b8f2f1b4aa51daa81ba39f24952a400a92df84fa28b` |
| `memit_dry_run/memit/hparams/FT/EleutherAI_gpt-j-6B_unconstr.json` | `1d605b748ed9709efb19d3f04c82de2d1ff12c81144c1d6621e72408f838d098` |
| `memit_dry_run/memit/hparams/FT/EleutherAI_gpt-j-6B_wd.json` | `5161e47c66580d13524abc1bbbb42b146163ff2f51121a4c74f23679bbad8254` |
| `memit_dry_run/memit/hparams/FT/gpt2-large_constr.json` | `48298eec3688c393dcf610e114b30a521fa3d8b5fc7fb5d5e938f61996f93d19` |
| `memit_dry_run/memit/hparams/FT/gpt2-medium_constr.json` | `fd1b7a80dff0e6d1c8e32c38b0ab620505ed1668d366d292a5776a49d2d7e23d` |
| `memit_dry_run/memit/hparams/FT/gpt2-xl_attn.json` | `28348947fe372113c6fc9d0a1b851121dbf8e198311ae7d573b4b6f8173a477b` |
| `memit_dry_run/memit/hparams/FT/gpt2-xl_constr.json` | `6f1a26e915b2fc5a203443322aa224f4dd47150117f1cc5d1ee7f8026108047f` |
| `memit_dry_run/memit/hparams/FT/gpt2-xl_unconstr.json` | `484393773f7a18844dd7c7f212673e4a8113515f0dfcc29c9d02c494f13bb137` |
| `memit_dry_run/memit/hparams/MEMIT/EleutherAI_gpt-j-6B.json` | `ac1c641470c003032f15cf3f3db088e215f289535b7ea8c171ccb1235cd7bf43` |
| `memit_dry_run/memit/hparams/MEMIT/Llama-3.1-8B.json` | `bea608d313845440ebe5a3887034b271bca431dff10a6d09a8237c3256f894f2` |
| `memit_dry_run/memit/hparams/MEMIT/gpt2-xl.json` | `2c2ff7e8f3ff8b33cca2966a628f92f8b56bba72af51ca9af57d6c30a1c342d4` |
| `memit_dry_run/memit/hparams/MEMIT/meta-llama_Llama-3.1-8B.json` | `61007b61dd2119cbd281ba10d89fb3d34bdcfe03cfce4da542a0729e261caf12` |
| `memit_dry_run/memit/hparams/MEND/EleutherAI_gpt-j-6B.json` | `d1e7bbd8a8486cda08af026c7cfdcc12b3a4fac3fab738a528e11adb8e52d97b` |
| `memit_dry_run/memit/hparams/MEND/EleutherAI_gpt-j-6B_CF.json` | `b30a5f403fa4972201d1ca994c70b3c6dbd396d7163bd502bc1cbe571e87d44c` |
| `memit_dry_run/memit/hparams/MEND/gpt2-xl.json` | `fe1a786ca540a3dee435621a56659d070b52b0354f85d08f9c0874f2e3d8fb79` |
| `memit_dry_run/memit/hparams/MEND/gpt2-xl_CF.json` | `5691b370fc2b8540d2c28d608d53e2328005ce5b933ab9e04726bde7cf93f44e` |
| `memit_dry_run/memit/hparams/MEND/gpt2-xl_zsRE.json` | `f6b0cc610281f474f702075064fe5eef83e0e7925d7f7d51036ee1fbc03a999a` |
| `memit_dry_run/memit/hparams/ROME/EleutherAI_gpt-j-6B.json` | `85e44438c5a6bcd7769d73efadd10507f2b7ec7eeaa0330a310e351d2676fdff` |
| `memit_dry_run/memit/hparams/ROME/EleutherAI_gpt-neox-20b.json` | `fadf233859d46cf02ef219f74bced47652d277cd392de51c7c1ce6585d1d60b9` |
| `memit_dry_run/memit/hparams/ROME/gpt2-large.json` | `2c5cb903948c6e261d2bb9aa2e9dfbd20ac30d38a2669054a25defcaed4a13ed` |
| `memit_dry_run/memit/hparams/ROME/gpt2-medium.json` | `3a6b72ddf9e0b859e6909a1e144c5bb6958852a0e4fef36db0e4424c424c1913` |
| `memit_dry_run/memit/hparams/ROME/gpt2-xl.json` | `81a98b788b8fbb89718288a8831441200e7d824fd057f62cb7d913ae4da5cf42` |
| `memit_dry_run/memit/memit/__init__.py` | `911cc037562a368ca7017ea66f4821c5a848f286a55b7d624c242209afcd01df` |
| `memit_dry_run/memit/memit/__pycache__/__init__.cpython-311.pyc` | `29e09585ec894fc0109aa73db6f1de88df5087ac3e70069f069c7dba782a4287` |
| `memit_dry_run/memit/memit/__pycache__/compute_ks.cpython-311.pyc` | `9acefffad173c67f9d03a1c0705145f2ee6b5aef1679f0fbd7cd0c49495d544e` |
| `memit_dry_run/memit/memit/__pycache__/compute_z.cpython-311.pyc` | `f3c78b5d8be2df307cc3bde53fc02a878469fc8f5c3473bf3a415b0dca3bd156` |
| `memit_dry_run/memit/memit/__pycache__/memit_hparams.cpython-311.pyc` | `d869204c04046a2ba2bc9e519fb324757b2bdad306d9365a6ce861ad687760f6` |
| `memit_dry_run/memit/memit/__pycache__/memit_main.cpython-311.pyc` | `4432d0eb89db771924edde06dd958544f8f598c74297aa38e5250f713e12aeff` |
| `memit_dry_run/memit/memit/compute_ks.py` | `0b039be47c548f046b71cad4efce63414f53edbaa657bde868a20cdd35a2f5c7` |
| `memit_dry_run/memit/memit/compute_z.py` | `d94af7fa14e5a4a20d5fa6361e0cbb30da0ff957db31922557ff809c34205dea` |
| `memit_dry_run/memit/memit/memit_hparams.py` | `1b229b882b031ddbb59f06ad6ba58d5c33b17826bbfddf80f767e96931b595b2` |
| `memit_dry_run/memit/memit/memit_main.py` | `d941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65` |
| `memit_dry_run/memit/memit/memit_main.py.pre_p7_backup` | `4b5c6478da463bb174036a3a0495d7786f8e4d207ee7021a7e9afb6aef977168` |
| `memit_dry_run/memit/notebooks/average_causal_effects.ipynb` | `35598748d8ce10af976c8f2be331fdf5eb6081dcd1d564f4ec753258c0c2cafb` |
| `memit_dry_run/memit/notebooks/causal_trace.ipynb` | `755a31d3d4a34b56e253e21b4171f944e31a4e57fa8a9c38440f6e6731ab2711` |
| `memit_dry_run/memit/notebooks/causal_trace_frozen_mlp_attn.ipynb` | `0b3837b24d70939e44b2fbba5757f4f19e888bf858445714c0bcb574170d4fe0` |
| `memit_dry_run/memit/notebooks/globals.yml` | `86ab5194b3cddc19c14173a3b8f13563c554d252666eb563a4ac2f919e087459` |
| `memit_dry_run/memit/notebooks/memit.ipynb` | `dc79c89862a9ef57dd6cdf46715c716ef60103f97314b1f9fb5fff3be88f7235` |
| `memit_dry_run/memit/notebooks/vis/globals.yml` | `86ab5194b3cddc19c14173a3b8f13563c554d252666eb563a4ac2f919e087459` |
| `memit_dry_run/memit/notebooks/vis/table_population.ipynb` | `a5b6eb40955acbf7b37068ea782b04cfcb56794c6738b4eefbc3f38daff03ced` |
| `memit_dry_run/memit/notebooks/vis/table_population_zsre.ipynb` | `c34799ceafdcad5220b5d871989cda93de581419741c861c38bd62f63d0cac85` |
| `memit_dry_run/memit/notebooks/vis/visualize_multi_results.ipynb` | `05d42e5d00021f4a435c23ffc88dcc919597c744136be2607f86e1a94d71304e` |
| `memit_dry_run/memit/notebooks/vis/visualize_sweep_results.ipynb` | `58ae1129dd40e1f6620e77ae24f1f74417ed3e1c2487ebcec552025c6313f008` |
| `memit_dry_run/memit/rome/README.md` | `4711e2605517fe1308cccd59748761e19342b4c0b0b26d2a9a32bbf3a93f94a6` |
| `memit_dry_run/memit/rome/__init__.py` | `87e6bd462753e8a86b84b2461da6067762cb0d5c9b7061b1b0598adb6f550a7a` |
| `memit_dry_run/memit/rome/__pycache__/__init__.cpython-311.pyc` | `174f5c000e030c096a7b21ec71e06661f3f348de8f2e3ad608fae32c8b8b5fe5` |
| `memit_dry_run/memit/rome/__pycache__/compute_u.cpython-311.pyc` | `e70218d4d08afdabbc8d1ae688ec4024b13175bbf2d822f1f79fb7087b063035` |
| `memit_dry_run/memit/rome/__pycache__/compute_v.cpython-311.pyc` | `b0da9115e983294a3b570dee6ebec70f40de5b41aa0205420857b5a8b55f90ef` |
| `memit_dry_run/memit/rome/__pycache__/layer_stats.cpython-311.pyc` | `440de9a4e69c8f72a3a6c32cdf88808d9ba2b3b5fb433c702d68b08af2e93e6c` |
| `memit_dry_run/memit/rome/__pycache__/repr_tools.cpython-311.pyc` | `7bc5434b08f4c6af21441c85d4715e5af2239dce3233f3f1aa7ca363068fd972` |
| `memit_dry_run/memit/rome/__pycache__/rome_hparams.cpython-311.pyc` | `7f48846aa72e1a408396ba4d7f5f2c7d6f1e77ae3d96a936b47347c232e22148` |
| `memit_dry_run/memit/rome/__pycache__/rome_main.cpython-311.pyc` | `68472f450355954b30697accbc0bd931633dc4335eea51ef5632347ab1d04e81` |
| `memit_dry_run/memit/rome/__pycache__/tok_dataset.cpython-311.pyc` | `0131138a2f4c2e647c345a854f9aa4cd11b882b09ab9f9a92dadaca667e37a32` |
| `memit_dry_run/memit/rome/compute_u.py` | `06a73593171eecdd03ab90d45daa2c6096b4335847f0c73bda9d834cdfb1d72d` |
| `memit_dry_run/memit/rome/compute_v.py` | `07f35ecec4b2a20a33318d75b040ae6c1fc5fd2122a90c92e32e361ef730d9eb` |
| `memit_dry_run/memit/rome/layer_stats.py` | `43693c64b061f3cdaa087447e47ddc10fb26fd597dd405eb0644d71ede2fe2d5` |
| `memit_dry_run/memit/rome/repr_tools.py` | `d4c2324ba20cbcce7f4ccfcf58ad002912edf0ad2fc72ab4e9bf46cc9dfed336` |
| `memit_dry_run/memit/rome/rome_hparams.py` | `1037cd56d2cfc92db212f5f4344477c5732a809dfd745c04e8e5742e925c98a5` |
| `memit_dry_run/memit/rome/rome_main.py` | `44ff978bd0d68839ff2f94f475a71fdac19a53a4ef263c1d74693ebfd5b40ba5` |
| `memit_dry_run/memit/rome/tok_dataset.py` | `37f775943d5040702ae21252db579f6aa116dacc4dd93c227c44cf9b3481a1a0` |
| `memit_dry_run/memit/scaling_curves.sh` | `4c89f3d257f67b3e9a1ae40fe81192bfc48c0a2f40b7f2dba9adc4f2bd97efa4` |
| `memit_dry_run/memit/scripts/causal_trace.sh` | `87bdd627bb58c82bf0f67841705bb95317d49f59eb1beab9d405126fd4d54600` |
| `memit_dry_run/memit/scripts/colab_reqs/additional.txt` | `3d49f4e0bb2b079bb2fec81b178bb0a27ebc4f8085c496727e299f16aa852fb2` |
| `memit_dry_run/memit/scripts/colab_reqs/rome.txt` | `de3f292db754a685905c34d079d097b95e3e7de102af06aedbfba42940d29564` |
| `memit_dry_run/memit/scripts/collect_layer_stats.sh` | `ca9be52a8845851b9b17d8b92b0ac3d7333b3ea7bac339db4c1daa0deda7c60a` |
| `memit_dry_run/memit/scripts/ipynb_drop_output.py` | `62a17e64c2de0448962fda6e0914a80e354361fea73b4363fc5287b92e4ca635` |
| `memit_dry_run/memit/scripts/memit.yml` | `28d8b635eed02cdb8d1fb36d8990a5347c1b88dfffcea71105febc8a91d98f83` |
| `memit_dry_run/memit/scripts/setup_clean_ipynb.sh` | `55533d28e032731eb1f0c91154ecf14092c23cf4d1f11be90a8304aa58e3338d` |
| `memit_dry_run/memit/scripts/setup_conda.sh` | `3d78078734cb1a45b0b448dafd5cc09b92496b89bcc8aabae057ee1fdb17e2f3` |
| `memit_dry_run/memit/util/__init__.py` | `0f2267e08c0c9345017c155e4d894043773f4e303958a95a3e8fe5dc3c5b341d` |
| `memit_dry_run/memit/util/__pycache__/__init__.cpython-311.pyc` | `db80aa1f656186a86bae309617717d6958528f2d358abe0f656acf2c769704c2` |
| `memit_dry_run/memit/util/__pycache__/device.cpython-311.pyc` | `b2cd7e432ddf59d90620450e3737a71784530a9f690bdca3d7156f116d603757` |
| `memit_dry_run/memit/util/__pycache__/generate.cpython-311.pyc` | `fa2a8446bf235e811752c2db8c04050864747ce541485c9a52ab9d3dae043b50` |
| `memit_dry_run/memit/util/__pycache__/globals.cpython-311.pyc` | `ce42162a322e75796375c0b0ab3bb732d882cb3127e85ab0dac890588b5de55a` |
| `memit_dry_run/memit/util/__pycache__/hparams.cpython-311.pyc` | `635c8abe561839a3fa9b91f7728d52899f7577c3a614a2a5b79a0736d6c41c73` |
| `memit_dry_run/memit/util/__pycache__/logit_lens.cpython-311.pyc` | `038eea0405aab634ef32849c1c3312333297fbad3d9e25ce7d8b4960aaa0938b` |
| `memit_dry_run/memit/util/__pycache__/nethook.cpython-311.pyc` | `58527b861ba2cdb71ecd7de3380eea7e28f4c7dcbe5938a65ee7e5a00bc20c39` |
| `memit_dry_run/memit/util/__pycache__/runningstats.cpython-311.pyc` | `652d9894a24dbfb428ffd3de41e21b98d50d318a8581a970b100b6c81de54a0b` |
| `memit_dry_run/memit/util/device.py` | `868627783827f03763ba9c210de2ddbd607e050330eccf7757fccfd9e985cf2b` |
| `memit_dry_run/memit/util/generate.py` | `3764cb8a0a1b3f28c17d8aab3028b33d2127ba4e02e8dbc253025791a9ab2514` |
| `memit_dry_run/memit/util/globals.py` | `ae25580435585acafce49511abbba6b545dbfb3f5865147d79bd383a050bf8c2` |
| `memit_dry_run/memit/util/hparams.py` | `09e9fec3f476ff68009230f1251044bec21aa71797d484033f736057bbe294b0` |
| `memit_dry_run/memit/util/logit_lens.py` | `0c35d203c511327e5c839ea0c06408f23dd6969402dce4be02f4e3160c88e6a4` |
| `memit_dry_run/memit/util/nethook.py` | `20e84c9413518af3aee76762071f823cbe5d75c4658e4ffa7bdab045df735f7c` |
| `memit_dry_run/memit/util/perplexity.py` | `e0dc2678eb331aba94d70bddad30ce983b3a062c35d180d1f524835f2966161e` |
| `memit_dry_run/memit/util/runningstats.py` | `7b3a05de007733ec3243c13362d3c24b6cb9c09f32eedbcf36de02c98a49ac97` |
| `memit_dry_run/memit/zsre_evals.sh` | `a5f8ca93642cab1e18bdfc917255ea64323b2c3261d0cb4634e235bbbbf00d2f` |
| `tools/engine_fingerprint.py` | `450ee83ac829817299ead301c4a3d20702f431deaea4be58c77ecfd89a329162` |

All **21 held artifact hashes** equal before/after, including both HALTED C10X output trees and logs, pinned templates, prior probes, and the operator's named rerun1 diagnostic. No old result, diagnostic or log was repaired. The prior **298,809 report bytes** are retained exactly as a prefix (SHA `c422274b68affcda4c01ec8b48264b8958552d8773dde4d123eb054214fcf2d5`). Full held-artifact evidence:

| Held artifact | Before SHA-256 = after SHA-256 |
| --- | --- |
| `architecture_profile/c10x_halt_diagnostic_20261008T212435_844926Z.json` | `785c9909a578f8be53b809c438663bf65dc4d264e023736b3b223fff88be448b` |
| `results/c10x_enginepath/audit_A1_single.pt` | `5e93b31e01b1ea5fbabce97b12c2963302ce20bc58c1e7ebad4cf76e7d2eccc5` |
| `results/c10x_enginepath/audit_A7_coined_coined.pt` | `342102323aee4a008da4f2e45db4997dfb35b5c74a4c66db2b851ddee7317329` |
| `results/c10x_enginepath/context_templates.json` | `0c6d90ee5e90e19c0174c6d2e085f3cf4454dfcd85c0f935fb1cc107afac2bfe` |
| `results/c10x_enginepath/run.json` | `a26d39cd9a32ec05174741d6d3ebfbf5a940565f81d3a76e1500e3b991d5b348` |
| `results/c10x_enginepath/stage.json` | `1f355edd4687c38ba921d8ce2909b0093f6eb52ed2642fe15d6b38402c62270e` |
| `results/c10x_enginepath_logs/preflight.json` | `b68e525278166ca71d4ddd64c95e28210540c0f7733dac18ee9d8eb054cdf0ac` |
| `results/c10x_enginepath_logs/process.log` | `7597d7b3f1ce1f221bf652cb2cd522fe8bf1b62c7ec99757ffb5c2fc1dfc59cf` |
| `results/c10x_enginepath_logs/supervisor.json` | `fcea2adb5d1a50497d921e7667c5bec9908a8eb7be2194a789a69ad6e7110242` |
| `results/c10x_enginepath_rerun1/audit_A1_single.pt` | `5e93b31e01b1ea5fbabce97b12c2963302ce20bc58c1e7ebad4cf76e7d2eccc5` |
| `results/c10x_enginepath_rerun1/audit_A7_coined_coined.pt` | `342102323aee4a008da4f2e45db4997dfb35b5c74a4c66db2b851ddee7317329` |
| `results/c10x_enginepath_rerun1/context_templates.json` | `0c6d90ee5e90e19c0174c6d2e085f3cf4454dfcd85c0f935fb1cc107afac2bfe` |
| `results/c10x_enginepath_rerun1/run.json` | `ebe34272e2828928905b9e191f62d091798616f2c3f31ac58e3fc737beb2d0aa` |
| `results/c10x_enginepath_rerun1/stage.json` | `0611609535ae6d4ab9110e724061f16da796ac8ebe9e8785dbc0905be000e165` |
| `results/c10x_enginepath_rerun1_logs/preflight.json` | `3fce00c7762c6e508aab734096dca1d40ba2426820ab96eba30504700753a222` |
| `results/c10x_enginepath_rerun1_logs/process.log` | `578f0c3ad03c455b177ff51dc5bb95e69907e86c0dbe8277969db44002a606d7` |
| `results/c10x_enginepath_rerun1_logs/supervisor.json` | `74a9ae6f2c63ff0c9d65216040ae072810af6a07c8be530034d8b2ce48de0b8a` |
| `results/c10x_x2_probe/20261008T171001_323402Z/probe.json` | `45b1fa22f234a7169664d562aab703cae82c2d9ddbc4c71113dd34c829443064` |
| `results/c10x_x2_probe/20261008T171001_323402Z/probe.log` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `results/c10x_x2_probe/20261008T180513_659317Z/probe.json` | `77598ef8f4082f9f5ed6f2c6f69b97e33d61117465be75f21c08c1970e6a1da9` |
| `results/c10x_x2_probe/20261008T180513_659317Z/probe.log` | `26fe6dbbbf8df59c4692b1a1ee86824d08dc305f7abd4a8cea4747d1aca8eb2f` |

Post-build porcelain below includes unowned live/historical paths and configuration entries. It is not a global clean-tree claim; these entries were not modified or cleaned up by this arc. The full capture is in `git_status.txt`.

```text
 M .gitignore
 M experiments/track_c/c10x_enginepath_arms.py
 M experiments/track_c/c10x_enginepath_inertness.py
 M experiments/track_c/c10x_enginepath_selftest.py
?? .ignore
?? architecture_profile/c10w_oracle_halt_diagnostic_20261008T060601_334913Z.json
?? architecture_profile/c10x_halt_diagnostic_20261008T160002_759184Z.json
?? architecture_profile/c10x_halt_diagnostic_20261008T160004_981087Z.json
?? architecture_profile/c10x_halt_diagnostic_20261008T212435_844926Z.json
?? architecture_profile/c10x_halt_diagnostic_20261008T212438_817160Z.json
?? architecture_profile/c10y_halt_diagnostic_20261008T160340Z_CALIB.json
?? architecture_profile/c10y_halt_diagnostic_20261008T172204Z_CALIB2.json
?? architecture_profile/c10y_halt_diagnostic_20261008T174209Z_CALIB3.json
?? architecture_profile/c10z_astra_halt_diagnostic.json
?? architecture_profile/c10z_astra_halt_diagnostic_20261008T124710.311412Z.json
?? external_prior_art
?? results/autoresearch_c10_equivalence_2026-10-06T0815.json
?? results/autoresearch_reaim/
?? results/c10w_oracle/p2_20261008T034226_086980Z/attempt1_halted/HALT.json
?? results/c10w_oracle/p2_20261008T034226_086980Z/attempt1_halted/eval.json
?? results/c10w_oracle/p2_20261008T034226_086980Z/attempt1_halted/eval_halt.json
?? results/c10w_oracle/p2_20261008T034226_086980Z/eval.json
?? results/c10w_oracle/p2_20261008T034226_086980Z/preflight.json
?? results/c10w_oracle/p2_20261008T034226_086980Z/reattempt2_dispatch.json
?? results/c10w_oracle/p2_20261008T034226_086980Z/reattempt2_dispatch_entered.json
?? results/c10w_oracle/p2_20261008T034226_086980Z/reattempt2_eval_started.json
?? results/c10w_oracle/p2_20261008T034226_086980Z/train/
?? results/c10w_oracle_logs/attempt1_halted/
?? results/c10w_oracle_logs/p2-a1-s1.gate.20261007T220211.50811.json
?? results/c10w_oracle_logs/p2-a7-rt.gate.20261007T220753.90179.json
?? results/c10w_oracle_logs/p2-a7-s1.gate.20261007T214226.17018.json
?? results/c10w_oracle_logs/p2-canon-s1.gate.20261007T215636.11061.json
?? results/c10w_oracle_logs/p2-eval.gate.20261008T030455.59962.json
?? results/c10w_oracle_logs/p2-read-attempt2.json
?? results/c10w_oracle_logs/p2-shuf-rt.gate.20261007T221517.41222.json
?? results/c10w_oracle_logs/p2-shuf-s1.gate.20261007T214924.63725.json
?? results/c10w_oracle_logs/p2_launch_fingerprint.txt
?? results/c10x_enginepath/
?? results/c10x_enginepath_logs/
?? results/c10x_enginepath_rerun1/
?? results/c10x_enginepath_rerun1_logs/
?? results/c10y_directdw_calib1/
?? results/c10y_directdw_calib2/
?? results/c10y_directdw_calib3/
?? results/c10z_astra/
?? results/c10z_astra_attempt2/
?? results/c10z_astra_benchmark/20261008T104535Z/heartbeat.json
?? results/c10z_astra_benchmark/20261008T104535Z/run.json
?? results/c10z_astra_benchmark/20261008T104535Z/svd_child.json
?? results/c10z_astra_benchmark/20261008T121345Z/heartbeat.json
?? results/c10z_astra_benchmark/20261008T121345Z/run.json
?? results/c10z_astra_benchmark/20261008T121345Z/svd_child.json
?? results/infranodus_research_arc_2026-10-05/fulltext/
?? results/infranodus_research_arc_2026-10-05/operator_chat_inbox/round3_20261005/infranodus-transcend-corpus-topics-C10.txt.rtf
?? results/infranodus_research_arc_2026-10-05/operator_chat_inbox/round3_20261005/infranodus-transcend-corpus-topics-C10_2.txt.rtf
?? results/infranodus_research_arc_2026-10-05/operator_chat_inbox/round3_20261005/infranodus_blanthycolino_science_261005T1207.json
?? results/infranodus_research_arc_2026-10-05/operator_chat_inbox/round3_20261005/infranodus_blanthycolino_science_261005T1215.json
?? results/infranodus_research_arc_2026-10-05/operator_chat_inbox/round3_20261005/infranodus_blanthycolino_science_261005T1217.json
?? results/infranodus_research_arc_2026-10-05/operator_chat_inbox/round3_20261005/infranodus_blanthycolino_science_261005T1219.json
?? results/infranodus_research_arc_2026-10-05/operator_chat_inbox/round3_20261005/infranodus_blanthycolino_science_261005T1220.json
?? results/infranodus_research_arc_2026-10-05/operator_chat_inbox/round3_20261005/infranodus_blanthycolino_science_261005T1222.json
?? results/infranodus_research_arc_2026-10-05/operator_chat_inbox/round3_20261005/infranodus_blanthycolino_science_261005T1223.json
?? results/infranodus_research_arc_2026-10-05/operator_chat_inbox/round3_20261005/infranodus_blanthycolino_science_261005T1228.json
?? results/infranodus_research_arc_2026-10-05/operator_chat_inbox/round3_20261005/infranodus_blanthycolino_science_261005T1230.json
?? results/infranodus_research_arc_2026-10-05/operator_chat_inbox/round3_20261005/infranodus_blanthycolino_science_261005T1233.json
?? results/infranodus_research_arc_2026-10-05/operator_chat_inbox/round3_20261005/infranodus_blanthycolino_science_261005T1235.json
?? results/infranodus_research_arc_2026-10-05/operator_chat_inbox/round3_20261005/infranodus_blanthycolino_science_261005T1238.json
?? results/infranodus_research_arc_2026-10-05/operator_chat_inbox/round3_20261005/infranodus_blanthycolino_science_261005T1240.json
?? results/infranodus_research_arc_2026-10-05/part2/q10_layer_selection_residual.txt
?? results/infranodus_research_arc_2026-10-05/part2/q11_nullspace_generalization_tradeoff.txt
?? results/infranodus_research_arc_2026-10-05/part2/q12_oov_entity_editing.txt
?? results/infranodus_research_arc_2026-10-05/part2/q14_rephrase_robustness_weight_editing.txt
?? results/infranodus_research_arc_2026-10-05/part2/q15_fictional_entity_weight_update.txt
?? results/infranodus_research_arc_2026-10-05/part2/q1_subject_embedding_editing.txt
?? results/infranodus_research_arc_2026-10-05/part2/q4_key_collinearity_interference.txt
?? results/infranodus_research_arc_2026-10-05/part2/q5_novel_entity_continued_pretraining.txt
?? results/infranodus_research_arc_2026-10-05/part2/q7_frame_vs_subject_recall.txt
?? results/infranodus_research_arc_2026-10-05/part2/q8_editing_overfit_paraphrase.txt
?? results/infranodus_research_arc_2026-10-05/part2/q9_covariance_regularization_editing.txt
?? results/infranodus_research_arc_2026-10-05/segments/
?? results/labviz/
?? results/labviz_codex_brief.md
?? results/labviz_codex_impl.md
?? results/labviz_v2_codex_impl.md
?? tools/labviz_serve.sh
```

Scoped git diff summary (relative to git baseline; task-relative patch is `final_patch.diff`):

```text
 experiments/track_c/c10x_enginepath_arms.py      | 125 +++++++++---
 experiments/track_c/c10x_enginepath_inertness.py |   9 +-
 experiments/track_c/c10x_enginepath_selftest.py  | 236 ++++++++++++++++++++++-
 3 files changed, 339 insertions(+), 31 deletions(-)
```

### Review and final source identities

The [advisor-review](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.codex/skills/advisor-review/SKILL.md) contract and [test-driven-development](/Users/robertrhu/.agents/skills/superpowers/test-driven-development/SKILL.md) were applied. A current Claude auth probe returned exit 1, `loggedIn=false`, `authMethod=none`, so the before/after review used a fresh, read-only `/root/json_boundary_refute` fallback. Its weaker same-family independence is retained. The implementation review first returned FIX-FIRST for previous-stage deadline attribution, then **GO, no remaining static blocker** after the test-first correction. The reviewer executed no workloads; its runtime status is UNVERIFIED. The author's final 96-test CPU execution is separate evidence. Design and corrected final review artifacts are linked by their hashes below.

Objections remaining against this repair: **none blocking**. Live/model/MPS scientific behavior is **UNVERIFIED**. Numeric/boolean coercion is scoped to the actual frozen scorer's scalar domain; this build does not change scientific input semantics or claim arbitrary malformed scorer-value equivalence. Existing bootstrap-refusal behavior is preserved as stated above. No program launch admission or dispatch is inferred from CPU PASS or the fallback review.

| Source | Final SHA-256 | This arc |
| --- | --- | --- |
| `experiments/track_c/c10x_enginepath_arms.py` | `469c92ec8a606e4f5a4b61b17ee16d28284c6b2d21e8eeaa8b9b6383b84e98bb` | changed |
| `experiments/track_c/c10x_enginepath_inertness.py` | `cb722d0bfe844361859dbabcb4c0f10cd86f10f72a4fb075a6a667b04d3dabe2` | changed |
| `experiments/track_c/c10x_enginepath_read.py` | `b17e588a8c8f6ff3d8ee5f3dc118fd8837bd9e26b7bdf33e343599ce671c2057` | unchanged |
| `experiments/track_c/c10x_enginepath_selftest.py` | `65fceeefaa14e78ecb93a31edfc8c19bb22924143c9dba984a34a26785a37b35` | changed |
| `experiments/track_c/c10x_enginepath_telemetry_check.py` | `e95beb2cef310fa1050ccb4a2b60ac8224f493ea4d513d97868f3b9a9c99fe80` | unchanged |
| `experiments/track_c/c10x_overtone_z.py` | `8b32ca840c1451624ba5f46143a6e65a03ae69e968dd0e6180d04fa5683dac42` | unchanged |
| `experiments/track_c/c10x_x2_probe.py` | `23bdf070c66f8af02bb4d38d22eaecdfffa04782339f500ce1572080d6a2b614` | unchanged |
| `docs/C10X_ENGINEPATH_PREREG.md` | `d3dfdc8bd8a9c04894b63da9b51ead164e7667e40d8f08b29b11606078f92899` | unchanged |

| Private evidence (`/private/tmp/c10x_build/scorer_json_fix/`) | SHA-256 |
| --- | --- |
| `before.json` | `b94f069732cb4a973dd395f1829ffa86172bcebb0b1e93a5a40eebb5b6170a63` |
| `design_review.md` | `84f3ff0bcc9e868f86b12d6579262c3e253c07cc8ca0cb3cad992dd911f1d440` |
| `engine_fingerprint.log` | `15aef4acf47eb374ea93cf4f949a0022a287f56b646ac2b139f599af98b355e3` |
| `final_patch.diff` | `406a31080fd78eae204632dea4ec56cc7c37c88e77e1fc8d46a90bfc4187134e` |
| `final_review.md` | `e2090abef6a4f3bfc80f5bf6eba96342b2c4bee9e822059de6e503a65b2a38d1` |
| `full_selftest.log` | `d13d28f890a715c2fed5ed3f44299891f7e6ea3a1bce24515209f086ddfe1541` |
| `full_selftest_final.log` | `f5c88ccb1609be301422821a87251d87cbe0328f9c1d931528ef660d6bff1810` |
| `git_diff_stat.txt` | `c3cb456480acd1763471aabd3cd25001e52c7edca44adfee61719a6cb62f93a1` |
| `git_status.txt` | `17e9156737559a0a46c23088427aed190f080c15da82f630de9ced608fe5940f` |
| `green_focused.log` | `94f4500e5dc3e9a494e883221fa6914dff0fa01a7d5b13ea410817474c6b94b9` |
| `green_focused_final.log` | `0336920799e8ff6cc8207f1a0a78863a52235a9505dd361f51867f20aac58c56` |
| `halt_observation.json` | `b16cb5b628ea5d8b87be33d450a884a9b974ece0c7e25cf36c81f49e06180f13` |
| `red.log` | `fa5d2328e23f322ab21e13da983a3b2de9299e762c4f75fc83bf1c710cb67a16` |
| `red_previous_deadline.log` | `9518ca32d01b8e34e878216bfff3082b9580fce944d002d00b3582a8e6560e2d` |
| `red_receipt.json` | `4df200e7a91dbd4322b4e3a8d4036b550fecd0b1fe5ed7de52672469003ce97a` |
| `sealed_evidence.json` | `d8cd2b79ac69b898ecbfff7d1e04f593331524aafe1ee9b56557ce36ab569188` |

**Handoff:** preserve rerun1 as HALTED/incomplete; require a complete fresh process-1 rerun (`results/c10x_enginepath_rerun2/` plus matching logs), current source receipts, and the program's review/admission/GO before any live launch. The historical launch recipes earlier in this report describe their respective source versions; use the new source hashes for the next admitted run. No reader bypass, partial result admission or live command was executed in this build. Original frozen constraints and stage budgets are unchanged. The final preservation/report receipt and context handoff are in this arc's authorized private scratch directory.

Graft: 78,300 tokens saved (~$0.04), two successful graph calls; the initial missing-Node availability failure saved none. Only the subprocess PATH was repaired; no package upgrade/install was performed.

## Projection refusal diagnosis (re-run 2; 2026-10-08)

**Disposition: diagnostic repair complete; frozen projection rule and all caps unchanged.** The recorded refusal necessarily exceeded the target-stage cap. Its exact solve samples and projected duration were not persisted, so the proposed first-solve warm-up cause is **UNVERIFIABLE**. This work diagnosed the saved records before editing production code, then added failure-input capture test-first. No GPU/model/science dispatch or rerun occurred; the failed runs remain HALTED/incomplete and cannot supply a scientific result. Evidence was captured in `/private/tmp/c10x_build/projection_halt_diag/{observations_initial.json,diagnosis_before_fix.json,diagnosis_plan_before_edits.md}` before production edits. The pinned prereg is still `d3dfdc8bd8a9c04894b63da9b51ead164e7667e40d8f08b29b11606078f92899` (`docs/C10X_ENGINEPATH_PREREG.md:118`; `experiments/track_c/c10x_enginepath_arms.py:30,36`).

### What can be recovered from this HALT

`results/c10x_enginepath_rerun2_logs/preflight.json` records `process=1`, `process1=null` and `admitted.process1=null`. `--predecessor` adds only a replacement-provenance record; it does not load timings. `launch_preflight` loads timing-bearing process-1 data only for process 2. The failed process therefore had **`self.first={}`, `previous={}`, `previous_overhead=0.0`**, irrespective of the predecessor path (`experiments/track_c/c10x_enginepath_arms.py:211–244,814–818,1188–1189,1392–1400`).

The empty `run.json.timings.work_units.targets` was a **stale stage-entry snapshot**, not a measurement of zero completed units. Before this repair, `validate_boundary` copied `BUDGET.units` at stage boundaries, while `done()` appended samples only to the budget object; the exception handler never refreshed the copy. Thus the empty field does not establish a first/second-solve refusal. The saved runtime source is `/private/tmp/c10x_build/projection_halt_diag/c10x_enginepath_arms.py` (SHA `469c92ec8a606e4f5a4b61b17ee16d28284c6b2d21e8eeaa8b9b6383b84e98bb`:808–852,1161–1166,1253–1263).

The target-stage checkpoint records `started_monotonic=1309215.10258325`; the preflight receipt records process start `1307557.828709041`; the supervisor records elapsed `1815.1408845419064 s`. Targets therefore began after `1657.2738742090296 s` of process time. Even using the later supervisor observation as an upper bound, target elapsed at worker refusal was **less than `157.86701033287682 s`**. The traceback ends in the first arm's engine8 loop: saved `construct_targets:967`. The directory contains only `context_templates.json`, `run.json`, and `stage.json`, with no `audit_A1_single.pt`; that audit would have been written after the first arm's engine8/engine4 solves and first OverTone solve. Under the preserved artifacts, **1–23 solve samples completed, so the refused attempt was solve 2–24 in the first engine8 group**. Exact count is not recorded (`results/c10x_enginepath_rerun2_logs/{preflight,supervisor}.json`; `results/c10x_enginepath_rerun2/stage.json`; `architecture_profile/c10x_halt_diagnostic_20261008T222923_839355Z.json`; saved arms source:958–1015).

| Refusal input | Historical evidence / limit |
|---|---|
| `stage` / phase | `targets` / `targets:body` |
| `cap` | Exactly `2400.0 s` |
| `first` / `previous` | Exactly `{}` / `{}`; predecessor supplies no timing history |
| `previous_overhead` | Exactly `0.0 s` |
| `reserve` | Exactly `9360.0 s` for all later stage caps |
| `elapsed` | Exact value **UNRECORDED**; `0 < elapsed < 157.86701033287682 s` |
| units so far, per kind | Saved copy `{}` is stale; actual `solve` count 1–23, durations **UNRECORDED** |
| `predicted` | `m × (216 − n)`, with `m` the slowest completed solve and `n` completed solves; exact value **UNRECORDED**, necessarily `>2242.132989667123 s` |
| `projected` | `max(2400, elapsed + predicted)`; exact value **UNRECORDED**, necessarily `>2400 s` |
| `remaining` | Exact failed-call value **UNRECORDED**; conservative comparison-budget bounds `[13184.859115458094, 13342.72612579097] s` |
| `within_stage_cap` | Necessarily **false** |
| `within_reserved_process_budget` | **UNRECORDED**; may also be false |

The exact stage-entry receipt was `projected=2400.0`, `cap=2400.0`, `remaining=13342.726131415926`, `reserve=9360.0`, `ok=true` (`results/c10x_enginepath_rerun2/stage.json:1`). At a unit recheck the code compares total projected stage duration against **`15000 − (now − process_start) + elapsed`**, not current process remainder alone. From the supervisor bound, this comparison budget is at least `13184.859115458094 s`; `2400+9360=11760` would pass. A refusal with a successful cap predicate is therefore impossible here. With no historical samples and zero completed units, prediction would be zero and elapsed below158 s, so the initial unit would also pass. At least one completed sample caused prediction above the cap. The lower bound on prediction implies the slowest completed solve was **greater than `10.428525533335456 s`** (`2242.132989667123 / 215`); its exact cost is unavailable. These are algebraic bounds from recorded times, not newly measured solve durations (`diagnosis_before_fix.json`; saved arms source:829–838).

### Warm-up hypothesis and frozen-rule fidelity

**The multiplication mechanism is present; its live cause is unresolved.** Once a completed solve takes `m` seconds, the target plan uses that maximum for every remaining solve. A one-time cost inside that timed work unit is consequently multiplied, with no trim/exclusion. The timed unit includes request/token preparation, instrumentation, the solver, CPU copying and diagnostic construction; it is not a timer around `compute_z` alone (`experiments/track_c/c10x_enginepath_arms.py:896–944`). A synthetic first sample of60 s, with elapsed61 s and215 solves remaining, yields `predicted=12900 s`, `projected=12961 s` and refusal. That regression demonstrates policy behavior; it **does not establish** that the historical first sample contained warm-up (`experiments/track_c/c10x_enginepath_selftest.py:2030–2034,2065–2082`).

Re-run 1 records72 engine8,72 engine4 and72 OverTone target diagnostics, consistent with216 completed solves, but its HALTED record has **no `timings` field or unit samples**. The roughly2100 s duration is the program's observation, not an exact timing series recoverable from that record. Its approximate mean (`2100/216 ≈9.72 s`) cannot recover or bound the slowest sample. The actual `project()` and entire `StageBudget` ASTs are identical in the two runtime sources: rerun1 arms SHA `ffcf5200c81c2c860f8b7741d19545b88f66b68f546ce4e11c52adff6ea609fc`, saved at `/private/tmp/c10x_build/scorer_json_fix/c10x_enginepath_arms.py`, versus rerun2 SHA `469c92…`. The JSON repair did not change projection policy (`results/c10x_enginepath_rerun1/run.json`, `targets.*.diagnostics`; `diagnosis_before_fix.json`).

**Faithful to frozen §2.7:** prereg:118 requires the larger of the allowance and a projection using the slowest measured comparable work units, with overhead, refusal above the stage cap or reserved process budget, rechecks before work units, independent deadlines, and HALTED/incomplete rather than NULL. The implemented caps are exactly setup600/A2040/targets2400/inertness3000/injection1500/I-2 2040/I-1 2040/final780 seconds; each process remains15000 seconds. The text provides no warm-up exclusion or averaging rule. The all-solve target plan remains216, with the existing grouping of solves unchanged. Planning estimates at prereg:108/:120 are expressly unvalidated wall time and do not override:118. No cap, multiplier, history source, overhead allowance, grouping, deadline, eligibility rule, or scientific path was changed. Any future cap or comparability/warm-up exemption is a program amendment decision; the old exact projection cannot be supplied as a measured number (`docs/C10X_ENGINEPATH_PREREG.md:108–120`; `experiments/track_c/c10x_enginepath_arms.py:36,54–56,829–876`).

### Diagnostic-only implementation

`project()` now attaches the four actual comparison arguments and both predicate outcomes to `Halt.budget_inputs`. `StageBudget` enriches the payload on refusal with attempted stage, entry/unit boundary, kind, cap, elapsed, per-kind completed samples/counts, remaining counts, `first`, `previous`, measured previous duration, `predicted`, `previous_overhead`, `projected`, `remaining`, `reserve`, and the process-time observation used for projection. At entry, `predicted` retains the existing inclusion of previous overhead; at a unit it is remaining-work prediction, with overhead separately added. `previous_overhead` means the **existing whole prior-stage overhead allowance**; this repair does not reinterpret it. Snapshot/count metadata is copied on failure and does not alter acceptance (`experiments/track_c/c10x_enginepath_arms.py:247–257,819–876`).

For `WORKER_DEADLINE`, the payload records whether the stage predicate failed and whether the process clock was actually sampled. If `elapsed>=cap`, the original short-circuit remains: the process-deadline clock is unsampled, and its value/outcome are explicit `null`. A handler never invents a replacement clock reading. Successful return values and clock sequences are preserved (`experiments/track_c/c10x_enginepath_arms.py:850–876`; `experiments/track_c/c10x_enginepath_selftest.py:2043–2064`).

The worker saves the budget payload before selecting an X2 primary exception, refreshes the completed unit ledger before HALT publication, and writes the same inputs to `run.json` and both the top level and state of its diagnostic. It does not invent a completed duration for the active stage. The supervisor copies a recorded worker payload even if later cleanup causes a supervisor timeout; `worker_halt` keeps the originating code/stage/phase separate from the supervisor disposition. Stage/phase/traceback discipline and strict JSON are retained (`experiments/track_c/c10x_enginepath_arms.py:284–294,1286–1304,1435–1452`; `experiments/track_c/c10x_enginepath_selftest.py:2072–2124`).

### RED / GREEN and verification

- **Diagnosis/pre-test review before production edits:** `/private/tmp/c10x_build/projection_halt_diag/diagnosis_plan_before_edits.md`; existing same-family reviewer returned PROCEED. Claude auth probe returned `loggedIn=false`, `authMethod=none`, so no out-of-family review was completed. The reviewer ran no workloads or edits.
- **RED:**14 focused methods,14 failure assertions including three subtest failures,0 errors,0.268 s, exit1. Missing payloads, stale ledger, and supervisor omissions reproduced while arms SHA remained the exact rerun2 SHA above (`red.log`, `red_gate.json`). Two control methods already passed.
- **Additional RED:** the completed-kind count regression failed once in0.027 s because the diagnostic omitted an `audit` kind outside the remaining plan. The count map now includes the union of completed and planned kinds; remaining counts and prediction are unchanged (`counts_red.log`; arms:823).
- **Focused GREEN:** all16 focused tests passed in0.318 s, exit0. These cover cap-only/reserve-only/both refusals, exact equality/BAD_PROJECTION controls, entry history/attribution, remaining-count/max-unit/overhead inputs, immutable snapshots, both deadline short-circuits, completed kinds outside the plan, unchanged successful clocks, actual tiny-driver worker HALTs for both codes, primary-exception selection, and supervisor timeout after worker refusal (`green_final.log`).
- **Full GREEN:** all112 selftests passed in22.507 s, exit0. Attribution and observed/unattributed protected listing changes were both `{}`; `c10e_bandknob`, `transformers` and `datasets` were absent. Tiny CPU fixtures and all child roots remained under `/private/tmp/c10x_build/roots`; no GPU, MPS, pretrained model/tokenizer or scientific run was exercised (`full_selftest_final.log`).
- **Frozen-policy comparison:**50 direct projection cases,432 work-unit cases and18 stage-entry cases (**500 total**) against the saved rerun2 source yielded identical outcomes, successful receipts, HALT codes, clock-read sequences and ledgers. Caps/unit plans, `done`/`leave` ASTs,61 other top-level definitions, and the run's scientific body/finally ASTs are unchanged (`frozen_budget_verification.{py,json,log}`).
- **Frozen bytes:**188 R5 files and28 held artifacts (original/rerun1/rerun2 outputs/logs, both latest diagnostics and probe outputs) match the before SHA tables exactly. Only arms.py and selftest.py changed within the seven C10X source files. The engine fingerprint passed (`d941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65`, `_cov_cpu=3`); frozen-path `git diff --quiet` exited0. This is the specified protected-file scope, not a claim that the shared worktree has no unrelated changes (`before.json`, `frozen_budget_verification.json`, `engine_fingerprint.log`).
- **Final review:** PROCEED, read-only same-family fallback; no remaining static blocker after the count correction. Reviewer inspected the16-test focused log and independently checked the historical bounds and source delta. Final112-test/500-case evidence arrived after it finalized and is parent-verified, not reviewer-attested (`final_review.md`).

Final full selftest command (executed serially):

```sh
env TMPDIR=/private/tmp/c10x_build PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python -B /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_selftest.py
```

Focused and frozen-policy commands (executed serially):

```sh
env TMPDIR=/private/tmp/c10x_build PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONPATH=/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python -B -m unittest -v c10x_enginepath_selftest.ProjectionDiagnosticTests
env TMPDIR=/private/tmp/c10x_build PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python -B /private/tmp/c10x_build/projection_halt_diag/verify_frozen_budget.py
```

The private parity script refuses an existing parity-root path; its recorded run is retained and should not be replayed into that existing namespace. Its result JSON stores the complete frozen/held SHA comparisons. The report's original413000-byte prefix (SHA `44fa04d491b903e04fabd90aa40df76d22b00edfb92ac00046a39e9eb70f3a23`) is preserved; only this section is appended. Final source SHAs:

| File | Final SHA-256 | Change in this repair |
|---|---|---|
| `experiments/track_c/c10x_enginepath_arms.py` | `2979c99f4331b988333ec30f79788d2c070c50bfb4f221f46aa8c247c5dc9226` | Diagnostic capture/persistence only |
| `experiments/track_c/c10x_enginepath_selftest.py` | `ebbe628bf8fe8d278a8be9183041a4bf95694ebc48889f53f180b18ed03b8b82` |16 projection/deadline regressions and test-only producer callback |
| `experiments/track_c/c10x_enginepath_inertness.py` | `cb722d0bfe844361859dbabcb4c0f10cd86f10f72a4fb075a6a667b04d3dabe2` | Unchanged |
| `experiments/track_c/c10x_enginepath_read.py` | `b17e588a8c8f6ff3d8ee5f3dc118fd8837bd9e26b7bdf33e343599ce671c2057` | Unchanged |
| `experiments/track_c/c10x_enginepath_telemetry_check.py` | `e95beb2cef310fa1050ccb4a2b60ac8224f493ea4d513d97868f3b9a9c99fe80` | Unchanged |
| `experiments/track_c/c10x_overtone_z.py` | `8b32ca840c1451624ba5f46143a6e65a03ae69e968dd0e6180d04fa5683dac42` | Unchanged |
| `experiments/track_c/c10x_x2_probe.py` | `23bdf070c66f8af02bb4d38d22eaecdfffa04782339f500ce1572080d6a2b614` | Unchanged |
| `docs/C10X_ENGINEPATH_PREREG.md` | `d3dfdc8bd8a9c04894b63da9b51ead164e7667e40d8f08b29b11606078f92899` | Unchanged; no amendment applied |

The runtime claim is limited to CPU diagnostics and frozen-policy parity. The real failed unit's magnitudes, exact projection and cause remain **UNVERIFIABLE**, and no new MPS timing or scientific outcome is claimed. Completion/context evidence is saved only under the authorized private scratch root; no git, canonical ledger, engine, harness, prereg, historical record or global memory write was performed.
