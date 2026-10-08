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
