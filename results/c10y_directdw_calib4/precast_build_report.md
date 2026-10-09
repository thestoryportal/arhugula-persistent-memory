# C10Y pre-cast diagnostic build report

**C10Y PRECAST BUILD DONE — CPU build verification only. Diagnostic NOT-RUN. Implementation review and any live admission remain GATED.**

Generated 2026-10-09T18:39:03.559133+00:00 in `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a` on branch `worktree-c10k-route-a`. No commit was made by this builder. The shared checkout was already dirty. A read-only HEAD sample during closeout was `36b275a8ba5b5706951db37fd3e9fa642c6c8473`; concurrent team commits are preserved.

## Binding scope and reads

The scope SHA was verified before its full read: `097c662803a94a897dd588c9e1f09c6af7b17a25019c1439ea39844c65f0a9a8`. Current bytes and `git show 4f7b22c:docs/C10Y_PRECAST_DIAG_SCOPE.md` matched. The full scope, preregistration §12 Amendment ZERO-STEP-DISPOSITION (`docs/C10Y_DIRECTDW_PREREG.md:975`), `zero_step_ruling_astra.md`, both `precast_scope_astra*.md` reviews, `zero_step_diagnosis.md`, and the record-fix report/source from `27c6adb` were read before authoring. Recipe A (`c10e_bandknob.py:189–221`) and the actual driver capture/factor/stored-weight paths were read first.

This is D-C10y-precast staging instrumentation. It does not resume, re-label or backfill calibration 4. It performs no behavioral readout, optimization, corrective execution, calibration 5 or stage-1. The target set is explicitly NEW COMPUTATION; calibration-4 placeholder tensors are never inputs. Scope freeze is design approval only. No new independent implementation review or live LAW#3/LAW#5 qualification is claimed.

## Delivered files and implementation

- `experiments/track_c/c10y_precast_diag.py` — model-free module, exclusive journal, original-code-object observer, saved-operand arithmetic controls, measurements, ordered reader, worker and model-free supervisor terminal writer.
- `experiments/track_c/c10y_precast_diag_selftest.py` — 49 CPU contract tests and temporary CPU stubs.
- `tools/run_c10y_precast_diag.sh` — external Bash deadline, fixed 2,820 s cap, owned process-group cleanup and publication recovery.
- `results/c10y_directdw_calib4/precast_build_report.md` — this exclusive report and session handoff.

The journal directly reuses the committed record-fix `_record_value` (`c10y_directdw_arms.py:1307`), `save_tensors` (`:1299`) and `write_json` (`:125`) primitives. It adds directory fsync, sidecar verification, durable input reload before predicates and immutable started/complete/failed phase records. The original `_prefix_snapshot` (`:1321`) path also supplies resource-gate inputs through `_C10Y_PREFIX_SAVE` before the unchanged memory gate. The engine, harness and C10Y science driver were not edited.

Native traces match original code objects and observe locals/tensor dispatch without rewriting solve functions. Each original native path runs with the observer off and on from restored weights and fresh zero cache. Both paths use the one persisted projector set and one persisted NEW COMPUTATION target set. Native packets retain pre-layer weights/globals, requests, tokenized batches and actual solve operands; factor M/Q/R are compared back to the native capture. Coverage gaps halt and preserve available fields. The device product is observed in original `effective_weight`. All arithmetic variants start from the saved recipe-A packet; native C10Y measurements remain separately named. No controlled update feeds a subsequent native layer.

Per cell, `updates_<arm>_L<layer>.pt` holds 16 named captured/control updates, including native direct/device/CPU products and their repeats. The 120 distinct pairs each have an exclusive record with CPU-fp64 distance, max-abs, quantiles, differing fraction and per-column distributions. Realizations retain fp16 weights and CPU-promoted realized updates, cast/add order, distances to recipe A and differing fp16 counts. Both actual matrices receive spectral condition numbers, normalized residuals against their respective systems and errors to the four fp64 controls. Numbers are descriptive; no magnitude threshold drives classification.

The external timer is armed before the first Python process/import. `SECONDS` starts before shell setup; elapsed setup is subtracted from the sleep. At 2,810 s it marks timeout and sends TERM, then KILL after 2 s. The remaining reserve belongs to restoration/terminal publication; at 2,820 s it kills the owned child/group and supervisor. There is no runtime cap override. The supervisor is Bash so it does not introduce an extra resident Python process that would fail the unchanged GPU inventory gate. The owned worker establishes its own session before the handshake. The last committed fingerprint/GPU results precede the load-on-import harness call immediately.

A timeout during terminal publication has fresh supervisor authority: `supervisor_timeout.json` states INCONCLUSIVE and references `reading.json`/`run.json` if still absent, or fresh `timeout_reading.json`/`timeout_run.json` when partial earlier bytes exist. Earlier files are never overwritten. A prepublished reading is not admitted after supervisor failure; read the fresh timeout authority first. Normal finalization refuses existing terminal artifacts.

## Requirement → test → implementation

All tests below passed on CPU. Native tests execute the original AST function bodies with CPU `nn.Linear` fixtures and stub model/tokenizer/representation leaves. The actual original representation batching function is exercised with CPU stubs. This validates capture/persistence/classification plumbing; it is not live MPS evidence. Source/input/cache/tokenizer/context hashing and the fixed model identity have been inspected statically and are checked again in the future worker before load. Actual model-cache content, runtime GPU inventory, MPS observer inertness and full-size solves remain UNVERIFIED.

| Frozen requirement / acceptance behavior | CPU test (file:line) | Implementation (file:line) |
|---|---|---|
| FROZEN v2 SHA; refuse drift before admission | `test_scope_SHA_drift_refused` (`experiments/track_c/c10y_precast_diag_selftest.py:255`) | `verify_scope` (`experiments/track_c/c10y_precast_diag.py:115`)<br>`source_identity` (`experiments/track_c/c10y_precast_diag.py:421`)<br>`worker` (`experiments/track_c/c10y_precast_diag.py:511`) |
| Fresh exclusive UTC directory; existing directory, traversal and symlink refusal | `test_fresh_namespace_existing_directory_and_symlink_refused` (`experiments/track_c/c10y_precast_diag_selftest.py:261`)<br>`test_real_shell_existing_namespace_refused_without_finalizer` (`experiments/track_c/c10y_precast_diag_selftest.py:524`) | `claim_namespace` (`experiments/track_c/c10y_precast_diag.py:120`)<br>`main` (`experiments/track_c/c10y_precast_diag.py:616`) |
| GPU gate and original engine fingerprint committed immediately before load, fail-closed | `test_fail_closed_gpu_and_fingerprint_records_precede_loader` (`experiments/track_c/c10y_precast_diag_selftest.py:269`) | `preload` (`experiments/track_c/c10y_precast_diag.py:413`)<br>`worker` (`experiments/track_c/c10y_precast_diag.py:511`) |
| One NEW COMPUTATION target set: 24 requests per arm, 48 solves total; persisted and reloaded; both original paths consume it | `test_48_targets_computed_once_saved_reloaded_and_shared_by_original_paths` (`experiments/track_c/c10y_precast_diag_selftest.py:456`) | `compute_targets` (`experiments/track_c/c10y_precast_diag.py:498`)<br>`native_capture` (`experiments/track_c/c10y_precast_diag.py:305`) |
| Target interruption retains completed prefix; unreached arm is NOT-RUN; mutation gate retains offending target and restores weights | `test_target_failure_retains_completed_prefix_and_NOT_RUN_arm` (`experiments/track_c/c10y_precast_diag_selftest.py:475`)<br>`test_target_mutation_halt_retains_offending_value_and_restores_weights` (`experiments/track_c/c10y_precast_diag_selftest.py:493`) | `compute_targets` (`experiments/track_c/c10y_precast_diag.py:498`)<br>`restored` (`experiments/track_c/c10y_precast_diag.py:168`)<br>`phase_summary` (`experiments/track_c/c10y_precast_diag.py:107`) |
| Read-only observation of original recipe-A and original C10Y code; actual K/cur/residual/P/C/M/Q/B/direct solution/factors and pre-layer identity | `test_observer_original_code_coverage_off_on_and_native_operands` (`experiments/track_c/c10y_precast_diag_selftest.py:220`)<br>`test_native_factor_actual_matrix_and_Q_are_compared` (`experiments/track_c/c10y_precast_diag_selftest.py:367`) | `NativeObserver` (`experiments/track_c/c10y_precast_diag.py:197`)<br>`native_capture` (`experiments/track_c/c10y_precast_diag.py:305`) |
| Actual native tokenized batches, order, padding and lookup indices; no object-id deduplication | `test_actual_representation_batch_padding_and_indices_captured_without_id_assumption` (`experiments/track_c/c10y_precast_diag_selftest.py:320`) | `NativeObserver` (`experiments/track_c/c10y_precast_diag.py:197`) |
| Coverage failure stops rather than substituting a solve; available operands retained even when native Q is missing | `test_missing_capture_refuses_instead_of_reimplementing` (`experiments/track_c/c10y_precast_diag_selftest.py:249`)<br>`test_missing_reference_Q_retains_available_operands_before_coverage_halt` (`experiments/track_c/c10y_precast_diag_selftest.py:346`)<br>`test_native_missing_factor_Q_is_inconclusive_capture_failure` (`experiments/track_c/c10y_precast_diag_selftest.py:379`) | `NativeObserver` (`experiments/track_c/c10y_precast_diag.py:197`)<br>`native_capture` (`experiments/track_c/c10y_precast_diag.py:305`) |
| Observer-off/on weight/cache/result equivalence; tensor inertness independently checked | `test_observer_tensor_inertness_catches_discarded_cur_mutation` (`experiments/track_c/c10y_precast_diag_selftest.py:334`)<br>`test_observer_original_code_coverage_off_on_and_native_operands` (`experiments/track_c/c10y_precast_diag_selftest.py:220`) | `NativeObserver` (`experiments/track_c/c10y_precast_diag.py:197`)<br>`native_capture` (`experiments/track_c/c10y_precast_diag.py:305`)<br>`exact` (`experiments/track_c/c10y_precast_diag.py:298`) |
| Forced native halt retains layer-4 packet and restores weights, globals, tracing, optional recorder and preexisting hooks | `test_forced_native_halt_preserves_capture_and_cleans_weights_globals` (`experiments/track_c/c10y_precast_diag_selftest.py:233`)<br>`test_restores_optional_recorder_and_preexisting_hook_on_halt` (`experiments/track_c/c10y_precast_diag_selftest.py:389`) | `restored` (`experiments/track_c/c10y_precast_diag.py:168`)<br>`NativeObserver` (`experiments/track_c/c10y_precast_diag.py:197`) |
| Native device product captured inside original effective_weight before cast/add | `test_device_product_observed_from_original_effective_weight` (`experiments/track_c/c10y_precast_diag_selftest.py:214`) | `device_product` (`experiments/track_c/c10y_precast_diag.py:379`) |
| Distinct CPU-fp32 product, promoted solved-fp32 factor product, promoted-before-assembly genuine fp64 solves, saved-assembled32 fp64 solves, and exact-input repeats | `test_float64_solve_and_promoted_product_are_distinct` (`experiments/track_c/c10y_precast_diag_selftest.py:177`)<br>`test_repeat_factor_compared_to_original_native_solution` (`experiments/track_c/c10y_precast_diag_selftest.py:427`) | `controls` (`experiments/track_c/c10y_precast_diag.py:340`)<br>`compare_cell` (`experiments/track_c/c10y_precast_diag.py:444`) |
| Every completed solution/product survives a later control halt | `test_completed_float64_direct_solution_survives_next_solve_failure` (`experiments/track_c/c10y_precast_diag_selftest.py:436`)<br>`test_completed_native_CPU_product_survives_later_control_halt` (`experiments/track_c/c10y_precast_diag_selftest.py:408`) | `controls` (`experiments/track_c/c10y_precast_diag.py:340`)<br>`compare_cell` (`experiments/track_c/c10y_precast_diag.py:444`) |
| All captured/control updates, including the actual native direct update, have all-pairs statistics | `test_native_direct_update_included_in_all_pair_measurements` (`experiments/track_c/c10y_precast_diag_selftest.py:417`) | `compare_cell` (`experiments/track_c/c10y_precast_diag.py:444`)<br>`distance_stats` (`experiments/track_c/c10y_precast_diag.py:400`) |
| CPU-fp64 Frobenius/max/quantiles/differing fraction; per-column weight coordinates; full 2048 x 11008 quantiles | `test_difference_metrics_and_weight_coordinate_columns` (`experiments/track_c/c10y_precast_diag_selftest.py:205`)<br>`test_full_weight_coordinate_quantiles_exceed_torch_limit` (`experiments/track_c/c10y_precast_diag_selftest.py:360`) | `distance_stats` (`experiments/track_c/c10y_precast_diag.py:400`) |
| fp16 realization uses native fp32 merge; true fp64 update rounds on CPU directly to fp16 before transfer/add, without fp32 demotion | `test_float64_realization_cannot_demote_to_float32` (`experiments/track_c/c10y_precast_diag_selftest.py:187`)<br>`test_float64_realization_casts_on_CPU_before_device_transfer` (`experiments/track_c/c10y_precast_diag_selftest.py:195`) | `realize` (`experiments/track_c/c10y_precast_diag.py:372`)<br>`compare_cell` (`experiments/track_c/c10y_precast_diag.py:444`) |
| Native saved C10Y factors drive R; both actual coefficient matrices, respective normalized residuals, method/norm and errors to four fp64 controls retained | `test_realized_native_saved_factors_drive_R_predicate` (`experiments/track_c/c10y_precast_diag_selftest.py:397`)<br>`test_native_factor_actual_matrix_and_Q_are_compared` (`experiments/track_c/c10y_precast_diag_selftest.py:367`) | `compare_cell` (`experiments/track_c/c10y_precast_diag.py:444`) |
| Exclusive fsynced JSON/PT writes; dependent predicates consume reloaded durable records; binary sidecar SHA checked | `test_gate_inputs_fsynced_and_reloaded_before_predicate` (`experiments/track_c/c10y_precast_diag_selftest.py:142`)<br>`test_packet_tamper_refused_before_downstream_consumption` (`experiments/track_c/c10y_precast_diag_selftest.py:315`) | `Journal` (`experiments/track_c/c10y_precast_diag.py:40`)<br>`load_record` (`experiments/track_c/c10y_precast_diag.py:86`) |
| JSON/PT sibling collision refusal, terminal overwrite refusal, and exclusive worker.log creation | `test_exclusive_JSON_and_tensor_collision_have_no_sibling` (`experiments/track_c/c10y_precast_diag_selftest.py:154`)<br>`test_finalizer_overwrite_refusal_keeps_terminal_bytes` (`experiments/track_c/c10y_precast_diag_selftest.py:291`)<br>`test_real_shell_worker_log_collision_refused_without_overwrite` (`experiments/track_c/c10y_precast_diag_selftest.py:527`) | `Journal` (`experiments/track_c/c10y_precast_diag.py:40`)<br>`finalize` (`experiments/track_c/c10y_precast_diag.py:573`) |
| Nonfinite operand retained before halt; interrupted serialization leaves INCOMPLETE and explicit NOT-RUN | `test_nonfinite_operand_persisted_before_halt` (`experiments/track_c/c10y_precast_diag_selftest.py:172`)<br>`test_interrupted_serialization_is_incomplete_and_retains_previous_values` (`experiments/track_c/c10y_precast_diag_selftest.py:163`) | `Journal` (`experiments/track_c/c10y_precast_diag.py:40`)<br>`phase_summary` (`experiments/track_c/c10y_precast_diag.py:107`) |
| Ordered threshold-free INCONCLUSIVE / R / S / UNCLASSIFIED; K never emitted; all ten cells and an A7 device difference required for R | `test_INCONCLUSIVE_precedes_every_other_reading` (`experiments/track_c/c10y_precast_diag_selftest.py:127`)<br>`test_R_requires_every_cell_and_A7_device_difference` (`experiments/track_c/c10y_precast_diag_selftest.py:118`)<br>`test_S_needs_direct_trace_evidence_and_K_never_emitted` (`experiments/track_c/c10y_precast_diag_selftest.py:134`)<br>`test_malformed_classification_capture_is_INCONCLUSIVE` (`experiments/track_c/c10y_precast_diag_selftest.py:507`) | `classify` (`experiments/track_c/c10y_precast_diag.py:133`) |
| Worker success is insufficient if any planned phase is incomplete or malformed; only completed phases permit R | `test_finalizer_incomplete_worker_cannot_publish_R` (`experiments/track_c/c10y_precast_diag_selftest.py:286`)<br>`test_finalizer_rejects_completed_claim_with_incomplete_phases` (`experiments/track_c/c10y_precast_diag_selftest.py:297`)<br>`test_finalizer_malformed_worker_preserves_exception_and_inconclusive` (`experiments/track_c/c10y_precast_diag_selftest.py:302`)<br>`test_valid_complete_phases_publish_threshold_free_R` (`experiments/track_c/c10y_precast_diag_selftest.py:308`) | `finalize` (`experiments/track_c/c10y_precast_diag.py:573`)<br>`phase_summary` (`experiments/track_c/c10y_precast_diag.py:107`) |
| Supervisor timeout overrides worker success and retains committed tensors | `test_supervisor_timeout_overrides_worker_success_and_preserves_commits` (`experiments/track_c/c10y_precast_diag_selftest.py:277`) | `finalize` (`experiments/track_c/c10y_precast_diag.py:573`) |
| Actual Bash supervisor bounded before Python imports; setup hang, worker hang/early exit and publication hang are diagnosed | `test_real_shell_supervisor_setup_timeout_retains_owned_namespace_diagnostic` (`experiments/track_c/c10y_precast_diag_selftest.py:521`)<br>`test_real_shell_supervisor_hanging_stub_preserves_timeout_and_kills_worker` (`experiments/track_c/c10y_precast_diag_selftest.py:515`)<br>`test_real_shell_supervisor_worker_exit_before_start_is_diagnosed` (`experiments/track_c/c10y_precast_diag_selftest.py:518`)<br>`test_real_shell_finalizer_timeout_has_fresh_supervisor_diagnostic` (`experiments/track_c/c10y_precast_diag_selftest.py:530`) | `main` (`experiments/track_c/c10y_precast_diag.py:616`)<br>`finalize` (`experiments/track_c/c10y_precast_diag.py:573`)<br>`timeout_terminal` (`experiments/track_c/c10y_precast_diag.py:600`) |
| Publication interruption preserves prior bytes and writes a fresh terminal INCONCLUSIVE authority | `test_timeout_publication_preserves_previous_bytes_and_has_terminal_INCONCLUSIVE` (`experiments/track_c/c10y_precast_diag_selftest.py:533`) | `timeout_terminal` (`experiments/track_c/c10y_precast_diag.py:600`) |
| Model-free fresh import; CPU-only test isolation; no live dispatch | `test_fresh_import_is_model_and_torch_free` (`experiments/track_c/c10y_precast_diag_selftest.py:584`) | `main` (`experiments/track_c/c10y_precast_diag.py:616`) |


Deadline/log/namespace details are in `tools/run_c10y_precast_diag.sh:4`, `:33`, `:61`, `:80` and the exclusive worker-log creation at `:94`. Runtime source/input identity and model/covariance manifests are in `experiments/track_c/c10y_precast_diag.py:421` and `experiments/track_c/c10y_precast_diag.py:429`. Fixed arm/layer/request contracts and projector persistence are in `experiments/track_c/c10y_precast_diag.py:511`. These runtime checks were not launched.

## Test commands and evidence boundary

Executed from the worktree root, serially, with no bytecode writes and one CPU thread:

```sh
env C10Y_ALLOWED_CHILD_TESTS=1 PYTHONDONTWRITEBYTECODE=1 \
  OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
  .venv/bin/python -B experiments/track_c/c10y_precast_diag_selftest.py

env C10Y_ALLOWED_CHILD_TESTS=1 PYTHONDONTWRITEBYTECODE=1 \
  OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
  .venv/bin/python -B experiments/track_c/c10y_directdw_selftest.py

/bin/bash -n tools/run_c10y_precast_diag.sh
```

Final new suite: **49 tests PASS, 0 failures, 0 errors, 0 skips**. Existing record-fix/driver suite: **285 tests PASS, 0 failures, 0 errors, 0 skips**. Total: **334 CPU tests PASS**. Bash syntax and in-memory Python `compile()` checks passed. The existing regression emits one warning from its preexisting requires-grad scalar assertion; its final isolation and forbidden-module checks are empty. Its UNVERIFIED JSON is an intentional refusal fixture, not a live launch.

The new audit hook refuses live-worktree file writes and non-stub child scripts. Accelerator synchronization/cache calls are replaced by assertion failures; model-library/harness imports are denied. All test outputs and subprocess fixtures live below `/private/tmp/c10y_build`. CPU child tests require `C10Y_ALLOWED_CHILD_TESTS=1`. The shell timeout tests copy the actual launcher to a temporary root, change only the cap/reserve to 6/4 s and use stdlib CPU stubs. They exercise setup timeout, a TERM-ignoring worker, publication timeout, pre-handshake exit, existing namespace and log collision; these prove the shell/persistence behavior at that scale, not a measured 2,820 s production run. No production diagnostic mode, real model/tokenizer load, GPU/MPS computation, live fingerprint/gate or science launch was run.

RED came first: the initial 20 tests failed with the implementation absent; each later persistence, precision, observer, repeat, timeout, target and log-collision test was observed failing before its production correction. Intermediate candidate failures are retained below and are not claimed as GREEN. The complete outputs of every captured run are embedded, including the final GREEN and existing regression.

## Exact future launch command — NOT EXECUTED

Requires the scope-mandated Astra implementation review and separate team admission first. The command creates a new exclusive UTC child; any existing child is refused. Do not call the worker directly or alter the cap.

```sh
/bin/bash '/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/run_c10y_precast_diag.sh' \
  --utc "$(/bin/date -u +%Y%m%dT%H%M%SZ)"
```

Output namespace: `results/c10y_precast_diag/<UTC>/`. The exclusive `worker.log` is inside that namespace. All tensor-bearing records have binary `.pt` sidecars and JSON dtype/shape/SHA references. `manifest.json`, shared `targets.pt`, path-suffixed native operand/factor packets, update packets, pair/realization/numeric records, `compare.json`, `reading.json`, `run.json` and phase/resource diagnostics remain staging artifacts. Arm/path suffixes preserve both actual native packet families; they do not share or overwrite a calibration output.

## Projected runtime and limitations

| Frozen estimate | Seconds | Evidence status |
|---|---:|---|
| Setup, imports, pins, fingerprint, GPU gate and model load | 600 | Frozen planning allowance; live UNVERIFIED |
| 48 target solves plus native captures for the two arms | 1,360 | Frozen estimate; ≈800 s target allowance and ≈560 s capture allowance, UNVERIFIED |
| Factors, CPU/device products, genuine fp64 controls/repeats, conditioning, realizations and comparisons | 300 | Frozen estimate; live feasibility UNVERIFIED |
| Serialization/restoration | 180 | Frozen allowance; actual bytes/time UNVERIFIED |
| Projected total | **2,440 (40 min 40 s)** | Planning estimate only |
| Fixed external cap | **2,820 (47 min)** | No in-run increase; timeout is INCONCLUSIVE |

The exact build adds the scope-required observer-off/on repetitions, original-code packet retention, full pristine-model snapshot and per-target full-model byte checks, model-shard/cache hashing, all-pairs/per-column records, dense fp64 solves and spectral SVD conditioning. These costs have not been measured on the live model. A single 11,008-square fp32 matrix is 484,704,256 bytes (about 0.451 GiB); multiple P/C/M/native/control copies can produce many tens of GiB of staging data. CPU full-coordinate quantile testing validates the statistic implementation at the real update shape, not full native solve size, RSS, disk throughput or MPS parity. The original resource gate remains unchanged and its inputs are retained before validation. This build does not establish that the frozen spend/resource envelope is sufficient.

Forced-kill tests prove committed artifacts and fresh terminal diagnostics survive on the working CPU fixture filesystem. Live model restoration after TERM is UNVERIFIED; KILL cannot perform in-process restoration and is explicitly diagnosed that way. A filesystem that cannot accept/fsync new records or a supervisor/finalizer killed at the absolute cap may leave only its already-committed phase/control evidence; such an incomplete invocation has no admitted classification and must be treated as INCONCLUSIVE. There is no silent overwrite, fallback arithmetic, timeout extension or retry into the same namespace.

The classifier emits only ordered INCONCLUSIVE/R/S/UNCLASSIFIED. R requires equal native operands/states, byte-stable exact-input repeats, recipe-A-identical realized CPU products from the actual saved C10Y factors in all ten cells and a differing native device realization in an A7 cell. S requires direct validated operand/state/orientation/formula evidence. Conditioning, precision improvements and column concentration never produce K or S by magnitude. Every result concerns NEW COMPUTATION inputs and cannot establish calibration-4 causation, authorize a product redesign, dispatch calibration 5 or close F1.

The old C10Y calibration/stage launch pins were not edited or repinned. This diagnostic imports reusable primitives and independently pins the current preregistration containing §12. It does not invoke the original driver main/preflight or make any halted run eligible. Existing Astra rulings and scope reviews are design inputs; the new implementation remains for Astra review. The local Claude CLI read-only auth probe reported `loggedIn: false`; no external CLI implementation review was performed or claimed.

## Protected-file audit and handoff

Beginning/end SHA audit covered **155 preexisting protected files**: all recorded CORPUS files, engine Python sources, existing C10Y files, calibration-4 contents, scope/preregistration, fingerprint/gate, runbook and checkpoint. **153 retained their starting hashes**. Observed concurrent drift is listed below: the shared runbook changed with team commit `de56195` (D-ML-2 MathLab Amendment M2-BUDGET), and the checkpoint also changed during closeout. This builder did not edit or revert either file. All C10Y/engine/harness/frozen-prereg/calibration protected hashes match. This is a protected-scope statement, not a global clean-worktree claim. Unrelated Lab View/MathLab work and derived graft cache activity are preserved.

No engine/harness science source, frozen scope/preregistration, CORPUS, ledgers, runbook, checkpoint or existing result was authored by this builder. Only the three new implementation/test files and this new report were delivered in the worktree; scratch evidence is under the temporary build root. No GPU/MPS/model dispatch and no git mutation/commit occurred. The report is the scoped session handoff; protected checkpoint/ledger/memory writes were not performed.

Next handoff: MAESTRO supplies these files/report to the scope-mandated Astra implementation review. No launch was performed.

Observed protected drift (retained):
```json
{
  "EXPERIMENT_RUNBOOK.md": {
    "after": "24ad49597a7b9643ccff0005e437f26b02271fece3f04f4567f4e48a1a04bb85",
    "before": "85b8f0383638b8da1dd948eaa63a5bd94f5f4b48efadd447f5495ee894a39425"
  },
  "SESSION_CHECKPOINT.md": {
    "after": "f08800b10e06cc4f8dc1f720e3de192874ce616a3eb3b98076228094d9447140",
    "before": "d738d75b36dca0c1c26f422c187472c35773af7c95384fb3deb66a17509c6a19"
  }
}
```

## File SHA-256

These are the exact delivered source bytes and verified frozen/supporting input bytes at report creation. The report cannot contain its own self-referential SHA; its SHA is computed after the exclusive fsynced write and recorded in the temporary final verification audit. Model/cache/shard hashes are future-run manifest data, not claimed as executed build evidence.

| File | SHA-256 |
|---|---|
| `experiments/track_c/c10y_precast_diag.py` | `1442b35b38744b84184b57cfafdcbcda31d94b726da6d6c9378806ddaf935b22` |
| `experiments/track_c/c10y_precast_diag_selftest.py` | `acbafa518218e333daaf4dc9164851f22174dec55418bbeab6d6a34946107b9f` |
| `tools/run_c10y_precast_diag.sh` | `430c1b92806d0397142ceb0f5ea48b93758d3bbdf14b593fc19ba22e78e351a0` |
| `docs/C10Y_PRECAST_DIAG_SCOPE.md` | `097c662803a94a897dd588c9e1f09c6af7b17a25019c1439ea39844c65f0a9a8` |
| `docs/C10Y_DIRECTDW_PREREG.md` | `005391a39e31d8174419de3e39078a42209ded1b7ab8caaf098d5d8a4f755004` |
| `experiments/track_c/c10y_directdw_arms.py` | `ead3cef2266a7c81035e5acb6c3a97b42f83da556ba093a9fd28ec403f7e158c` |
| `experiments/track_c/c10e_bandknob.py` | `1f6be5811d7e58f3ebda16867a4a174b1cf24d47f9a2514cf9c3f9d29f18e695` |
| `experiments/track_c/c10z_astra_benchmark.py` | `9b25a207f630fbfa0d60c80a74f22289ad3bb2cc160d0fc72d7e0367f9a47a1a` |
| `configs/hparams/qwen25_3b_memit_hparams.json` | `4225cc6aabc3eb9fa62d2bb2cac68b1238de3a39c5e469da635e6e1464aa3bb4` |
| `configs/screens/g6_screen_qwen3b_v2.json` | `482c05f8f33c59d3e469566fe6f3c48eb183d3cb2fbb791f31dcad7102517c5c` |
| `memit_dry_run/memit/memit/compute_z.py` | `d94af7fa14e5a4a20d5fa6361e0cbb30da0ff957db31922557ff809c34205dea` |
| `memit_dry_run/memit/memit/compute_ks.py` | `0b039be47c548f046b71cad4efce63414f53edbaa657bde868a20cdd35a2f5c7` |
| `memit_dry_run/memit/rome/repr_tools.py` | `d4c2324ba20cbcce7f4ccfcf58ad002912edf0ad2fc72ab4e9bf46cc9dfed336` |
| `memit_dry_run/memit/memit/memit_main.py` | `d941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65` |
| `tools/engine_fingerprint.py` | `450ee83ac829817299ead301c4a3d20702f431deaea4be58c77ecfd89a329162` |
| `tools/c10w_p2_gate.py` | `fb6568a6e159e84b22971aa893c3a83bcaaa16085f4abd9c76ca50b4a3362a26` |
| `results/c10y_directdw_calib4/context_templates_calib.json` | `9472b663a34cfd9c0bb5448087ae0c2c333b1988b70f211fb2d90baaf8b560b7` |
| `results/c10y_directdw_calib4/zero_step_ruling_astra.md` | `dac92008ae4830b2b8493af1f67f4adcf7643a43d4776438a9967961a3aef5b3` |
| `results/c10y_directdw_calib4/precast_scope_astra.md` | `92e90484f4200a6981709e1231a847911b8bb1564d953f98c9918fb7d11a44c0` |
| `results/c10y_directdw_calib4/precast_scope_astra_r2.md` | `7e6552e32e174ce8b3a8faf42bbbc97dd90b4e217c1fffb68b673f1ee191c331` |
| `results/c10y_directdw_calib4/zero_step_diagnosis.md` | `f630108e6e9105eba4b7b8acf8558572a8e7bc93cdc73bbde602d222ceccd388` |
| `results/c10y_directdw_calib4/recordfix_build_report.md` | `6bf63a752d50d3b1c2f048e7135155461e1d66c3b351d35d77f14f83ff857ac4` |
| `experiments/track_c/c10y_directdw_selftest.py` | `81f3c07ec36fe1aa10bf31526f712cb3b015b0a86f714ba7aa3123a81875dd25` |


## Complete test-output archive

Raw original logs: `/private/tmp/c10y_build/precast_20261009T173245Z`. All logs below are included byte-for-byte as text. The first missing-implementation RED and each subsequent failing regression snapshot precede their implementation correction. Failed candidate logs remain failed; only the final 49-test GREEN and unchanged 285-test regression establish the delivered CPU result.

| Captured run | Bytes | Result | SHA-256 |
|---|---:|---|---|
| `red.log` | 15909 | Ran 20 tests in 0.001s; FAILED (failures=20) | `1d555521e4196f510968553c63eadfa52c9ba34846cac5c9016775e0febec048` |
| `green_initial.log` | 6001 | Ran 20 tests in 0.140s; FAILED (failures=1, errors=2) | `7c48fbbba9b742d35b424b836203bf0f45b469f3bb4b46cf6831c5887ede849d` |
| `green_contracts.log` | 2885 | Ran 20 tests in 0.252s; OK | `da43a3e4db29c6a6bc92c50de1db83ffeae827f23ff49ae3ce87abf260110ad3` |
| `red_extended.log` | 11964 | Ran 31 tests in 8.904s; FAILED (failures=5, errors=2) | `c9323276920f1daeaae37c425aeaa44189536e2e8e6c6ca70dc36d5f8ea91ff5` |
| `green_extended.log` | 6073 | Ran 31 tests in 5.535s; FAILED (failures=1) | `2a26ce99fc325ea69f41699e795bff86123089b115634b8b485c84f8e1ae8a9b` |
| `red_precision.log` | 3132 | Ran 2 tests in 0.331s; FAILED (failures=1, errors=1) | `a26c1a56d430b647838ac1b9574fa5fb18c3973ce1951d0e948ee876cee6e2af` |
| `green_precision.log` | 4641 | Ran 32 tests in 5.739s; OK | `d14ed35bcd7c330c93ec5b46f54e1ca6ef124da94f5921f02ffe2b28485d7291` |
| `red_observer.log` | 5418 | Ran 3 tests in 0.101s; FAILED (failures=1, errors=2) | `afb0e73ce17487931d8f799c0a38369af7d7543ab7a9f5fb53480501b12b0e09` |
| `green_observer.log` | 6020 | Ran 36 tests in 6.546s; FAILED (failures=1) | `7df4c3f797e0c61eaae64930338deac084c7fd2f07b11d780fd4b1c2f0c2ed7d` |
| `green_final.log` | 5305 | Ran 36 tests in 6.560s; OK | `8d9796a4ab54d3c30474af60efc0680e1ab6f325c25f3d86c2fd7387be71ec4f` |
| `directdw_regression.log` | 41188 | Ran 285 tests in 22.740s; OK | `ec1e75ad0e392e8e9f49a2839eb0ba0a6bf26bc42abe078b6f36b37b1cfc5653` |
| `red_audit.log` | 24347 | Ran 5 tests in 0.892s; FAILED (failures=2, errors=5) | `004d9ad393e0e8371e171cd4070939084abca2361bf9ee469438ed5344ffe6b8` |
| `green_audit.log` | 6043 | Ran 41 tests in 7.580s; OK | `26715dd604bffd02c9a4bf4be437e7431ac55f289236e624e61415b3890d3766` |
| `red_setup_timeout.log` | 1377 | Ran 1 test in 4.039s; FAILED (failures=1) | `79f4ebd38f3d8dd98f2ede8ccb555a64406cf1f2b684387a75f4ad15cfbc0dd9` |
| `green_release.log` | 6224 | Ran 42 tests in 11.850s; OK | `bd4ab394f7b6b28840e2cfbf26093117726e5948ecc74b537a55782f8a768770` |
| `red_namespace_shell.log` | 2474 | Ran 1 test in 0.395s; FAILED (failures=1) | `5496f6a09c5f156526f512d873b966b883970d4cd49cf6ac4bc26fddc92c792c` |
| `green_delivery.log` | 6374 | Ran 43 tests in 11.878s; OK | `0d1ba89ac89765c4e9ff0102df41918bcbfe56e3d2ab75352bbb6bf17d05ae92` |
| `red_finalizer_timeout.log` | 2900 | Ran 2 tests in 4.040s; FAILED (failures=1, errors=1) | `6e513550e02ce83ea61aedfa33bb2d46195d37b853b34b4df4fcca0cc3522128` |
| `green_acceptance.log` | 6722 | Ran 45 tests in 18.114s; OK | `ba29d442e7b37f78673810365e61e18a5bf3170886abebf0c1b353db8b1cb3f3` |
| `red_targets.log` | 2894 | Ran 3 tests in 0.002s; FAILED (failures=3) | `9ab184fd5d977f7eb3dec880f718833208d6b60c90b5e09d45b949dee38ba111` |
| `green_final_48.log` | 7218 | Ran 48 tests in 19.963s; OK | `257a5715e60e9b9075155a03d4e0e04c749ef36157b3a27cf6a1cf7cc765864c` |
| `red_log_collision.log` | 1298 | Ran 1 test in 0.642s; FAILED (failures=1) | `27e800c3951314ffb26a9c171d1b9a8ebb4506a0898ecf3da53439519ea67d72` |
| `green_final_49.log` | 7372 | Ran 49 tests in 17.146s; OK | `32d9b68da0bde656cf592650d09ca25a4c54705dbb9cb2ece9fb8b389f21ab15` |


### red.log

```text
test_INCONCLUSIVE_precedes_every_other_reading (__main__.Contracts.test_INCONCLUSIVE_precedes_every_other_reading) ... FAIL
test_R_requires_every_cell_and_A7_device_difference (__main__.Contracts.test_R_requires_every_cell_and_A7_device_difference) ... FAIL
test_S_needs_direct_trace_evidence_and_K_never_emitted (__main__.Contracts.test_S_needs_direct_trace_evidence_and_K_never_emitted) ... FAIL
test_device_product_observed_from_original_effective_weight (__main__.Contracts.test_device_product_observed_from_original_effective_weight) ... FAIL
test_difference_metrics_and_weight_coordinate_columns (__main__.Contracts.test_difference_metrics_and_weight_coordinate_columns) ... FAIL
test_exclusive_JSON_and_tensor_collision_have_no_sibling (__main__.Contracts.test_exclusive_JSON_and_tensor_collision_have_no_sibling) ... FAIL
test_fail_closed_gpu_and_fingerprint_records_precede_loader (__main__.Contracts.test_fail_closed_gpu_and_fingerprint_records_precede_loader) ... FAIL
test_finalizer_incomplete_worker_cannot_publish_R (__main__.Contracts.test_finalizer_incomplete_worker_cannot_publish_R) ... FAIL
test_finalizer_overwrite_refusal_keeps_terminal_bytes (__main__.Contracts.test_finalizer_overwrite_refusal_keeps_terminal_bytes) ... FAIL
test_float64_realization_cannot_demote_to_float32 (__main__.Contracts.test_float64_realization_cannot_demote_to_float32) ... FAIL
test_float64_solve_and_promoted_product_are_distinct (__main__.Contracts.test_float64_solve_and_promoted_product_are_distinct) ... FAIL
test_forced_native_halt_preserves_capture_and_cleans_weights_globals (__main__.Contracts.test_forced_native_halt_preserves_capture_and_cleans_weights_globals) ... FAIL
test_fresh_namespace_existing_directory_and_symlink_refused (__main__.Contracts.test_fresh_namespace_existing_directory_and_symlink_refused) ... FAIL
test_gate_inputs_fsynced_and_reloaded_before_predicate (__main__.Contracts.test_gate_inputs_fsynced_and_reloaded_before_predicate) ... FAIL
test_interrupted_serialization_is_incomplete_and_retains_previous_values (__main__.Contracts.test_interrupted_serialization_is_incomplete_and_retains_previous_values) ... FAIL
test_missing_capture_refuses_instead_of_reimplementing (__main__.Contracts.test_missing_capture_refuses_instead_of_reimplementing) ... FAIL
test_nonfinite_operand_persisted_before_halt (__main__.Contracts.test_nonfinite_operand_persisted_before_halt) ... FAIL
test_observer_original_code_coverage_off_on_and_native_operands (__main__.Contracts.test_observer_original_code_coverage_off_on_and_native_operands) ... FAIL
test_scope_SHA_drift_refused (__main__.Contracts.test_scope_SHA_drift_refused) ... FAIL
test_supervisor_timeout_overrides_worker_success_and_preserves_commits (__main__.Contracts.test_supervisor_timeout_overrides_worker_success_and_preserves_commits) ... FAIL

======================================================================
FAIL: test_INCONCLUSIVE_precedes_every_other_reading (__main__.Contracts.test_INCONCLUSIVE_precedes_every_other_reading)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 92, in setUp
    self.assertIsNotNone(D, 'precast diagnostic implementation is missing')
AssertionError: unexpectedly None : precast diagnostic implementation is missing

======================================================================
FAIL: test_R_requires_every_cell_and_A7_device_difference (__main__.Contracts.test_R_requires_every_cell_and_A7_device_difference)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 92, in setUp
    self.assertIsNotNone(D, 'precast diagnostic implementation is missing')
AssertionError: unexpectedly None : precast diagnostic implementation is missing

======================================================================
FAIL: test_S_needs_direct_trace_evidence_and_K_never_emitted (__main__.Contracts.test_S_needs_direct_trace_evidence_and_K_never_emitted)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 92, in setUp
    self.assertIsNotNone(D, 'precast diagnostic implementation is missing')
AssertionError: unexpectedly None : precast diagnostic implementation is missing

======================================================================
FAIL: test_device_product_observed_from_original_effective_weight (__main__.Contracts.test_device_product_observed_from_original_effective_weight)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 92, in setUp
    self.assertIsNotNone(D, 'precast diagnostic implementation is missing')
AssertionError: unexpectedly None : precast diagnostic implementation is missing

======================================================================
FAIL: test_difference_metrics_and_weight_coordinate_columns (__main__.Contracts.test_difference_metrics_and_weight_coordinate_columns)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 92, in setUp
    self.assertIsNotNone(D, 'precast diagnostic implementation is missing')
AssertionError: unexpectedly None : precast diagnostic implementation is missing

======================================================================
FAIL: test_exclusive_JSON_and_tensor_collision_have_no_sibling (__main__.Contracts.test_exclusive_JSON_and_tensor_collision_have_no_sibling)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 92, in setUp
    self.assertIsNotNone(D, 'precast diagnostic implementation is missing')
AssertionError: unexpectedly None : precast diagnostic implementation is missing

======================================================================
FAIL: test_fail_closed_gpu_and_fingerprint_records_precede_loader (__main__.Contracts.test_fail_closed_gpu_and_fingerprint_records_precede_loader)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 92, in setUp
    self.assertIsNotNone(D, 'precast diagnostic implementation is missing')
AssertionError: unexpectedly None : precast diagnostic implementation is missing

======================================================================
FAIL: test_finalizer_incomplete_worker_cannot_publish_R (__main__.Contracts.test_finalizer_incomplete_worker_cannot_publish_R)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 92, in setUp
    self.assertIsNotNone(D, 'precast diagnostic implementation is missing')
AssertionError: unexpectedly None : precast diagnostic implementation is missing

======================================================================
FAIL: test_finalizer_overwrite_refusal_keeps_terminal_bytes (__main__.Contracts.test_finalizer_overwrite_refusal_keeps_terminal_bytes)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 92, in setUp
    self.assertIsNotNone(D, 'precast diagnostic implementation is missing')
AssertionError: unexpectedly None : precast diagnostic implementation is missing

======================================================================
FAIL: test_float64_realization_cannot_demote_to_float32 (__main__.Contracts.test_float64_realization_cannot_demote_to_float32)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 92, in setUp
    self.assertIsNotNone(D, 'precast diagnostic implementation is missing')
AssertionError: unexpectedly None : precast diagnostic implementation is missing

======================================================================
FAIL: test_float64_solve_and_promoted_product_are_distinct (__main__.Contracts.test_float64_solve_and_promoted_product_are_distinct)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 92, in setUp
    self.assertIsNotNone(D, 'precast diagnostic implementation is missing')
AssertionError: unexpectedly None : precast diagnostic implementation is missing

======================================================================
FAIL: test_forced_native_halt_preserves_capture_and_cleans_weights_globals (__main__.Contracts.test_forced_native_halt_preserves_capture_and_cleans_weights_globals)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 92, in setUp
    self.assertIsNotNone(D, 'precast diagnostic implementation is missing')
AssertionError: unexpectedly None : precast diagnostic implementation is missing

======================================================================
FAIL: test_fresh_namespace_existing_directory_and_symlink_refused (__main__.Contracts.test_fresh_namespace_existing_directory_and_symlink_refused)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 92, in setUp
    self.assertIsNotNone(D, 'precast diagnostic implementation is missing')
AssertionError: unexpectedly None : precast diagnostic implementation is missing

======================================================================
FAIL: test_gate_inputs_fsynced_and_reloaded_before_predicate (__main__.Contracts.test_gate_inputs_fsynced_and_reloaded_before_predicate)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 92, in setUp
    self.assertIsNotNone(D, 'precast diagnostic implementation is missing')
AssertionError: unexpectedly None : precast diagnostic implementation is missing

======================================================================
FAIL: test_interrupted_serialization_is_incomplete_and_retains_previous_values (__main__.Contracts.test_interrupted_serialization_is_incomplete_and_retains_previous_values)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 92, in setUp
    self.assertIsNotNone(D, 'precast diagnostic implementation is missing')
AssertionError: unexpectedly None : precast diagnostic implementation is missing

======================================================================
FAIL: test_missing_capture_refuses_instead_of_reimplementing (__main__.Contracts.test_missing_capture_refuses_instead_of_reimplementing)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 92, in setUp
    self.assertIsNotNone(D, 'precast diagnostic implementation is missing')
AssertionError: unexpectedly None : precast diagnostic implementation is missing

======================================================================
FAIL: test_nonfinite_operand_persisted_before_halt (__main__.Contracts.test_nonfinite_operand_persisted_before_halt)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 92, in setUp
    self.assertIsNotNone(D, 'precast diagnostic implementation is missing')
AssertionError: unexpectedly None : precast diagnostic implementation is missing

======================================================================
FAIL: test_observer_original_code_coverage_off_on_and_native_operands (__main__.Contracts.test_observer_original_code_coverage_off_on_and_native_operands)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 92, in setUp
    self.assertIsNotNone(D, 'precast diagnostic implementation is missing')
AssertionError: unexpectedly None : precast diagnostic implementation is missing

======================================================================
FAIL: test_scope_SHA_drift_refused (__main__.Contracts.test_scope_SHA_drift_refused)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 92, in setUp
    self.assertIsNotNone(D, 'precast diagnostic implementation is missing')
AssertionError: unexpectedly None : precast diagnostic implementation is missing

======================================================================
FAIL: test_supervisor_timeout_overrides_worker_success_and_preserves_commits (__main__.Contracts.test_supervisor_timeout_overrides_worker_success_and_preserves_commits)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 92, in setUp
    self.assertIsNotNone(D, 'precast diagnostic implementation is missing')
AssertionError: unexpectedly None : precast diagnostic implementation is missing

----------------------------------------------------------------------
Ran 20 tests in 0.001s

FAILED (failures=20)
```


### green_initial.log

```text
test_INCONCLUSIVE_precedes_every_other_reading (__main__.Contracts.test_INCONCLUSIVE_precedes_every_other_reading) ... ok
test_R_requires_every_cell_and_A7_device_difference (__main__.Contracts.test_R_requires_every_cell_and_A7_device_difference) ... ok
test_S_needs_direct_trace_evidence_and_K_never_emitted (__main__.Contracts.test_S_needs_direct_trace_evidence_and_K_never_emitted) ... ok
test_device_product_observed_from_original_effective_weight (__main__.Contracts.test_device_product_observed_from_original_effective_weight) ... ok
test_difference_metrics_and_weight_coordinate_columns (__main__.Contracts.test_difference_metrics_and_weight_coordinate_columns) ... ok
test_exclusive_JSON_and_tensor_collision_have_no_sibling (__main__.Contracts.test_exclusive_JSON_and_tensor_collision_have_no_sibling) ... ok
test_fail_closed_gpu_and_fingerprint_records_precede_loader (__main__.Contracts.test_fail_closed_gpu_and_fingerprint_records_precede_loader) ... ERROR
test_finalizer_incomplete_worker_cannot_publish_R (__main__.Contracts.test_finalizer_incomplete_worker_cannot_publish_R) ... ok
test_finalizer_overwrite_refusal_keeps_terminal_bytes (__main__.Contracts.test_finalizer_overwrite_refusal_keeps_terminal_bytes) ... ok
test_float64_realization_cannot_demote_to_float32 (__main__.Contracts.test_float64_realization_cannot_demote_to_float32) ... ok
test_float64_solve_and_promoted_product_are_distinct (__main__.Contracts.test_float64_solve_and_promoted_product_are_distinct) ... ok
test_forced_native_halt_preserves_capture_and_cleans_weights_globals (__main__.Contracts.test_forced_native_halt_preserves_capture_and_cleans_weights_globals) ... FAIL
test_fresh_namespace_existing_directory_and_symlink_refused (__main__.Contracts.test_fresh_namespace_existing_directory_and_symlink_refused) ... ok
test_gate_inputs_fsynced_and_reloaded_before_predicate (__main__.Contracts.test_gate_inputs_fsynced_and_reloaded_before_predicate) ... ok
test_interrupted_serialization_is_incomplete_and_retains_previous_values (__main__.Contracts.test_interrupted_serialization_is_incomplete_and_retains_previous_values) ... ok
test_missing_capture_refuses_instead_of_reimplementing (__main__.Contracts.test_missing_capture_refuses_instead_of_reimplementing) ... ok
test_nonfinite_operand_persisted_before_halt (__main__.Contracts.test_nonfinite_operand_persisted_before_halt) ... ok
test_observer_original_code_coverage_off_on_and_native_operands (__main__.Contracts.test_observer_original_code_coverage_off_on_and_native_operands) ... ERROR
test_scope_SHA_drift_refused (__main__.Contracts.test_scope_SHA_drift_refused) ... ok
test_supervisor_timeout_overrides_worker_success_and_preserves_commits (__main__.Contracts.test_supervisor_timeout_overrides_worker_success_and_preserves_commits) ... ok

======================================================================
ERROR: test_fail_closed_gpu_and_fingerprint_records_precede_loader (__main__.Contracts.test_fail_closed_gpu_and_fingerprint_records_precede_loader)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 243, in test_fail_closed_gpu_and_fingerprint_records_precede_loader
    self.assertTrue((self.root/'preload_'+bad+'.json').exists())
                     ~~~~~~~~~~~~~~~~~~~~^~~~
TypeError: unsupported operand type(s) for +: 'PosixPath' and 'str'

======================================================================
ERROR: test_observer_original_code_coverage_off_on_and_native_operands (__main__.Contracts.test_observer_original_code_coverage_off_on_and_native_operands)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 192, in test_observer_original_code_coverage_off_on_and_native_operands
    result=D.native_capture(h,requests,p,self.j,'A7_coined_coined')
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag.py", line 300, in native_capture
    if on:observer.validate()
          ^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag.py", line 275, in validate
    self.j.gate('coverage_'+self.arm+'_'+self.path,{'layers':self.layers,'returns':self.returns,'factor_count':self.factor_count,
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag.py", line 61, in gate
    if not passed: raise A.Halt(code,inputs)
                   ^^^^^^^^^^^^^^^^^^^^^^^^^
c10y_directdw_arms.Halt: OBSERVER-COVERAGE: {'layers': [], 'returns': 1, 'factor_count': 0, 'batches': {4: [], 5: [], 6: [], 7: [], 8: []}, 'passed': False}

======================================================================
FAIL: test_forced_native_halt_preserves_capture_and_cleans_weights_globals (__main__.Contracts.test_forced_native_halt_preserves_capture_and_cleans_weights_globals)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 214, in test_forced_native_halt_preserves_capture_and_cleans_weights_globals
    self.assertTrue((self.root/'operands_A7_coined_coined_L4_A.pt').exists())
AssertionError: False is not true

----------------------------------------------------------------------
Ran 20 tests in 0.140s

FAILED (failures=1, errors=2)
```


### green_contracts.log

```text
test_INCONCLUSIVE_precedes_every_other_reading (__main__.Contracts.test_INCONCLUSIVE_precedes_every_other_reading) ... ok
test_R_requires_every_cell_and_A7_device_difference (__main__.Contracts.test_R_requires_every_cell_and_A7_device_difference) ... ok
test_S_needs_direct_trace_evidence_and_K_never_emitted (__main__.Contracts.test_S_needs_direct_trace_evidence_and_K_never_emitted) ... ok
test_device_product_observed_from_original_effective_weight (__main__.Contracts.test_device_product_observed_from_original_effective_weight) ... ok
test_difference_metrics_and_weight_coordinate_columns (__main__.Contracts.test_difference_metrics_and_weight_coordinate_columns) ... ok
test_exclusive_JSON_and_tensor_collision_have_no_sibling (__main__.Contracts.test_exclusive_JSON_and_tensor_collision_have_no_sibling) ... ok
test_fail_closed_gpu_and_fingerprint_records_precede_loader (__main__.Contracts.test_fail_closed_gpu_and_fingerprint_records_precede_loader) ... ok
test_finalizer_incomplete_worker_cannot_publish_R (__main__.Contracts.test_finalizer_incomplete_worker_cannot_publish_R) ... ok
test_finalizer_overwrite_refusal_keeps_terminal_bytes (__main__.Contracts.test_finalizer_overwrite_refusal_keeps_terminal_bytes) ... ok
test_float64_realization_cannot_demote_to_float32 (__main__.Contracts.test_float64_realization_cannot_demote_to_float32) ... ok
test_float64_solve_and_promoted_product_are_distinct (__main__.Contracts.test_float64_solve_and_promoted_product_are_distinct) ... ok
test_forced_native_halt_preserves_capture_and_cleans_weights_globals (__main__.Contracts.test_forced_native_halt_preserves_capture_and_cleans_weights_globals) ... ok
test_fresh_namespace_existing_directory_and_symlink_refused (__main__.Contracts.test_fresh_namespace_existing_directory_and_symlink_refused) ... ok
test_gate_inputs_fsynced_and_reloaded_before_predicate (__main__.Contracts.test_gate_inputs_fsynced_and_reloaded_before_predicate) ... ok
test_interrupted_serialization_is_incomplete_and_retains_previous_values (__main__.Contracts.test_interrupted_serialization_is_incomplete_and_retains_previous_values) ... ok
test_missing_capture_refuses_instead_of_reimplementing (__main__.Contracts.test_missing_capture_refuses_instead_of_reimplementing) ... ok
test_nonfinite_operand_persisted_before_halt (__main__.Contracts.test_nonfinite_operand_persisted_before_halt) ... ok
test_observer_original_code_coverage_off_on_and_native_operands (__main__.Contracts.test_observer_original_code_coverage_off_on_and_native_operands) ... ok
test_scope_SHA_drift_refused (__main__.Contracts.test_scope_SHA_drift_refused) ... ok
test_supervisor_timeout_overrides_worker_success_and_preserves_commits (__main__.Contracts.test_supervisor_timeout_overrides_worker_success_and_preserves_commits) ... ok

----------------------------------------------------------------------
Ran 20 tests in 0.252s

OK
```


### red_extended.log

```text
test_INCONCLUSIVE_precedes_every_other_reading (__main__.Contracts.test_INCONCLUSIVE_precedes_every_other_reading) ... ok
test_R_requires_every_cell_and_A7_device_difference (__main__.Contracts.test_R_requires_every_cell_and_A7_device_difference) ... ok
test_S_needs_direct_trace_evidence_and_K_never_emitted (__main__.Contracts.test_S_needs_direct_trace_evidence_and_K_never_emitted) ... ok
test_device_product_observed_from_original_effective_weight (__main__.Contracts.test_device_product_observed_from_original_effective_weight) ... ok
test_difference_metrics_and_weight_coordinate_columns (__main__.Contracts.test_difference_metrics_and_weight_coordinate_columns) ... ok
test_exclusive_JSON_and_tensor_collision_have_no_sibling (__main__.Contracts.test_exclusive_JSON_and_tensor_collision_have_no_sibling) ... ok
test_fail_closed_gpu_and_fingerprint_records_precede_loader (__main__.Contracts.test_fail_closed_gpu_and_fingerprint_records_precede_loader) ... ok
test_finalizer_incomplete_worker_cannot_publish_R (__main__.Contracts.test_finalizer_incomplete_worker_cannot_publish_R) ... ok
test_finalizer_malformed_worker_preserves_exception_and_inconclusive (__main__.Contracts.test_finalizer_malformed_worker_preserves_exception_and_inconclusive) ... ERROR
test_finalizer_overwrite_refusal_keeps_terminal_bytes (__main__.Contracts.test_finalizer_overwrite_refusal_keeps_terminal_bytes) ... ok
test_finalizer_rejects_completed_claim_with_incomplete_phases (__main__.Contracts.test_finalizer_rejects_completed_claim_with_incomplete_phases) ... FAIL
test_float64_realization_cannot_demote_to_float32 (__main__.Contracts.test_float64_realization_cannot_demote_to_float32) ... ok
test_float64_solve_and_promoted_product_are_distinct (__main__.Contracts.test_float64_solve_and_promoted_product_are_distinct) ... ok
test_forced_native_halt_preserves_capture_and_cleans_weights_globals (__main__.Contracts.test_forced_native_halt_preserves_capture_and_cleans_weights_globals) ... ok
test_fresh_import_is_model_and_torch_free (__main__.Contracts.test_fresh_import_is_model_and_torch_free) ... ok
test_fresh_namespace_existing_directory_and_symlink_refused (__main__.Contracts.test_fresh_namespace_existing_directory_and_symlink_refused) ... ok
test_gate_inputs_fsynced_and_reloaded_before_predicate (__main__.Contracts.test_gate_inputs_fsynced_and_reloaded_before_predicate) ... ok
test_interrupted_serialization_is_incomplete_and_retains_previous_values (__main__.Contracts.test_interrupted_serialization_is_incomplete_and_retains_previous_values) ... ok
test_missing_capture_refuses_instead_of_reimplementing (__main__.Contracts.test_missing_capture_refuses_instead_of_reimplementing) ... ok
test_native_factor_actual_matrix_and_Q_are_compared (__main__.Contracts.test_native_factor_actual_matrix_and_Q_are_compared) ... FAIL
test_native_missing_factor_Q_is_inconclusive_capture_failure (__main__.Contracts.test_native_missing_factor_Q_is_inconclusive_capture_failure) ... FAIL
test_nonfinite_operand_persisted_before_halt (__main__.Contracts.test_nonfinite_operand_persisted_before_halt) ... ok
test_observer_original_code_coverage_off_on_and_native_operands (__main__.Contracts.test_observer_original_code_coverage_off_on_and_native_operands) ... ok
test_packet_tamper_refused_before_downstream_consumption (__main__.Contracts.test_packet_tamper_refused_before_downstream_consumption) ... ok
test_real_shell_supervisor_hanging_stub_preserves_timeout_and_kills_worker (__main__.Contracts.test_real_shell_supervisor_hanging_stub_preserves_timeout_and_kills_worker) ... ok
test_real_shell_supervisor_worker_exit_before_start_is_diagnosed (__main__.Contracts.test_real_shell_supervisor_worker_exit_before_start_is_diagnosed) ... FAIL
test_realized_native_saved_factors_drive_R_predicate (__main__.Contracts.test_realized_native_saved_factors_drive_R_predicate) ... ERROR
test_restores_optional_recorder_and_preexisting_hook_on_halt (__main__.Contracts.test_restores_optional_recorder_and_preexisting_hook_on_halt) ... FAIL
test_scope_SHA_drift_refused (__main__.Contracts.test_scope_SHA_drift_refused) ... ok
test_supervisor_timeout_overrides_worker_success_and_preserves_commits (__main__.Contracts.test_supervisor_timeout_overrides_worker_success_and_preserves_commits) ... ok
test_valid_complete_phases_publish_threshold_free_R (__main__.Contracts.test_valid_complete_phases_publish_threshold_free_R) ... ok

======================================================================
ERROR: test_finalizer_malformed_worker_preserves_exception_and_inconclusive (__main__.Contracts.test_finalizer_malformed_worker_preserves_exception_and_inconclusive)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 272, in test_finalizer_malformed_worker_preserves_exception_and_inconclusive
    D.finalize(self.root,0,timed_out=False,elapsed_s=1.)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag.py", line 538, in finalize
    worker_record=A.strict_load(out/'worker.json') if (out/'worker.json').is_file() else {'status':'NOT-RUN'}
                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_arms.py", line 122, in strict_load
    def strict_load(path): return strict_json(Path(path).read_bytes())
                                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_arms.py", line 119, in strict_json
    return json.loads(raw,parse_constant=reject,parse_float=floating,object_pairs_hook=pairs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/json/__init__.py", line 359, in loads
    return cls(**kw).decode(s)
           ^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/json/decoder.py", line 337, in decode
    obj, end = self.raw_decode(s, idx=_w(s, 0).end())
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/json/decoder.py", line 353, in raw_decode
    obj, end = self.scan_once(s, idx)
               ^^^^^^^^^^^^^^^^^^^^^^
json.decoder.JSONDecodeError: Expecting property name enclosed in double quotes: line 1 column 2 (char 1)

======================================================================
ERROR: test_realized_native_saved_factors_drive_R_predicate (__main__.Contracts.test_realized_native_saved_factors_drive_R_predicate)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 320, in test_realized_native_saved_factors_drive_R_predicate
    result=D.compare_cell(h,self.j,dict(arm='A7_coined_coined',layer=4,operands_equal=True,states_equal=True,discrepancies=[]))
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag.py", line 444, in compare_cell
    path=journal.finite(prefix+'_compare_'+key,value);pairs[key]=path.name
                                                                 ^^^^^^^^^
AttributeError: 'dict' object has no attribute 'name'

======================================================================
FAIL: test_finalizer_rejects_completed_claim_with_incomplete_phases (__main__.Contracts.test_finalizer_rejects_completed_claim_with_incomplete_phases)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 268, in test_finalizer_rejects_completed_claim_with_incomplete_phases
    self.assertEqual(json.loads((self.root/'reading.json').read_text())['label'],'INCONCLUSIVE')
AssertionError: 'R' != 'INCONCLUSIVE'
- R
+ INCONCLUSIVE


======================================================================
FAIL: test_native_factor_actual_matrix_and_Q_are_compared (__main__.Contracts.test_native_factor_actual_matrix_and_Q_are_compared)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 297, in test_native_factor_actual_matrix_and_Q_are_compared
    self.assertTrue(all(not c['operands_equal'] for c in result['cells']))
AssertionError: False is not true

======================================================================
FAIL: test_native_missing_factor_Q_is_inconclusive_capture_failure (__main__.Contracts.test_native_missing_factor_Q_is_inconclusive_capture_failure)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 307, in test_native_missing_factor_Q_is_inconclusive_capture_failure
    with self.assertRaisesRegex(A.Halt,'OBSERVER-COVERAGE'):
AssertionError: Halt not raised

======================================================================
FAIL: test_real_shell_supervisor_worker_exit_before_start_is_diagnosed (__main__.Contracts.test_real_shell_supervisor_worker_exit_before_start_is_diagnosed)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 330, in test_real_shell_supervisor_worker_exit_before_start_is_diagnosed
    self.run_shell_stub('early_exit')
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 347, in run_shell_stub
    self.assertEqual(child.returncode,2,(child.stdout,child.stderr))
AssertionError: 1 != 2 : ('', 'rm: /private/tmp/c10y_precast_deadline.R0hs28Dw/session: No such file or directory\n')

======================================================================
FAIL: test_restores_optional_recorder_and_preexisting_hook_on_halt (__main__.Contracts.test_restores_optional_recorder_and_preexisting_hook_on_halt)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 316, in test_restores_optional_recorder_and_preexisting_hook_on_halt
    self.assertIs(h._C10Y_PREFIX_SAVE,sentinel);self.assertIs(registry[999],sentinel)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: <function Contracts.test_restores_optional_recorder_and_preexisting_hook_on_halt.<locals>.<lambda> at 0x106a0bce0> is not <object object at 0x10b7b0f20>

----------------------------------------------------------------------
Ran 31 tests in 8.904s

FAILED (failures=5, errors=2)
```


### green_extended.log

```text
test_INCONCLUSIVE_precedes_every_other_reading (__main__.Contracts.test_INCONCLUSIVE_precedes_every_other_reading) ... ok
test_R_requires_every_cell_and_A7_device_difference (__main__.Contracts.test_R_requires_every_cell_and_A7_device_difference) ... ok
test_S_needs_direct_trace_evidence_and_K_never_emitted (__main__.Contracts.test_S_needs_direct_trace_evidence_and_K_never_emitted) ... ok
test_device_product_observed_from_original_effective_weight (__main__.Contracts.test_device_product_observed_from_original_effective_weight) ... ok
test_difference_metrics_and_weight_coordinate_columns (__main__.Contracts.test_difference_metrics_and_weight_coordinate_columns) ... ok
test_exclusive_JSON_and_tensor_collision_have_no_sibling (__main__.Contracts.test_exclusive_JSON_and_tensor_collision_have_no_sibling) ... ok
test_fail_closed_gpu_and_fingerprint_records_precede_loader (__main__.Contracts.test_fail_closed_gpu_and_fingerprint_records_precede_loader) ... ok
test_finalizer_incomplete_worker_cannot_publish_R (__main__.Contracts.test_finalizer_incomplete_worker_cannot_publish_R) ... ok
test_finalizer_malformed_worker_preserves_exception_and_inconclusive (__main__.Contracts.test_finalizer_malformed_worker_preserves_exception_and_inconclusive) ... ok
test_finalizer_overwrite_refusal_keeps_terminal_bytes (__main__.Contracts.test_finalizer_overwrite_refusal_keeps_terminal_bytes) ... ok
test_finalizer_rejects_completed_claim_with_incomplete_phases (__main__.Contracts.test_finalizer_rejects_completed_claim_with_incomplete_phases) ... ok
test_float64_realization_cannot_demote_to_float32 (__main__.Contracts.test_float64_realization_cannot_demote_to_float32) ... ok
test_float64_solve_and_promoted_product_are_distinct (__main__.Contracts.test_float64_solve_and_promoted_product_are_distinct) ... ok
test_forced_native_halt_preserves_capture_and_cleans_weights_globals (__main__.Contracts.test_forced_native_halt_preserves_capture_and_cleans_weights_globals) ... ok
test_fresh_import_is_model_and_torch_free (__main__.Contracts.test_fresh_import_is_model_and_torch_free) ... ok
test_fresh_namespace_existing_directory_and_symlink_refused (__main__.Contracts.test_fresh_namespace_existing_directory_and_symlink_refused) ... ok
test_gate_inputs_fsynced_and_reloaded_before_predicate (__main__.Contracts.test_gate_inputs_fsynced_and_reloaded_before_predicate) ... ok
test_interrupted_serialization_is_incomplete_and_retains_previous_values (__main__.Contracts.test_interrupted_serialization_is_incomplete_and_retains_previous_values) ... ok
test_missing_capture_refuses_instead_of_reimplementing (__main__.Contracts.test_missing_capture_refuses_instead_of_reimplementing) ... ok
test_native_factor_actual_matrix_and_Q_are_compared (__main__.Contracts.test_native_factor_actual_matrix_and_Q_are_compared) ... ok
test_native_missing_factor_Q_is_inconclusive_capture_failure (__main__.Contracts.test_native_missing_factor_Q_is_inconclusive_capture_failure) ... ok
test_nonfinite_operand_persisted_before_halt (__main__.Contracts.test_nonfinite_operand_persisted_before_halt) ... ok
test_observer_original_code_coverage_off_on_and_native_operands (__main__.Contracts.test_observer_original_code_coverage_off_on_and_native_operands) ... ok
test_packet_tamper_refused_before_downstream_consumption (__main__.Contracts.test_packet_tamper_refused_before_downstream_consumption) ... ok
test_real_shell_supervisor_hanging_stub_preserves_timeout_and_kills_worker (__main__.Contracts.test_real_shell_supervisor_hanging_stub_preserves_timeout_and_kills_worker) ... ok
test_real_shell_supervisor_worker_exit_before_start_is_diagnosed (__main__.Contracts.test_real_shell_supervisor_worker_exit_before_start_is_diagnosed) ... FAIL
test_realized_native_saved_factors_drive_R_predicate (__main__.Contracts.test_realized_native_saved_factors_drive_R_predicate) ... ok
test_restores_optional_recorder_and_preexisting_hook_on_halt (__main__.Contracts.test_restores_optional_recorder_and_preexisting_hook_on_halt) ... ok
test_scope_SHA_drift_refused (__main__.Contracts.test_scope_SHA_drift_refused) ... ok
test_supervisor_timeout_overrides_worker_success_and_preserves_commits (__main__.Contracts.test_supervisor_timeout_overrides_worker_success_and_preserves_commits) ... ok
test_valid_complete_phases_publish_threshold_free_R (__main__.Contracts.test_valid_complete_phases_publish_threshold_free_R) ... ok

======================================================================
FAIL: test_real_shell_supervisor_worker_exit_before_start_is_diagnosed (__main__.Contracts.test_real_shell_supervisor_worker_exit_before_start_is_diagnosed)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 330, in test_real_shell_supervisor_worker_exit_before_start_is_diagnosed
    self.run_shell_stub('early_exit')
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 347, in run_shell_stub
    self.assertEqual(child.returncode,2,(child.stdout,child.stderr))
AssertionError: 0 != 2 : ('', '/private/tmp/c10y_build/tmpg2yuprjz/tools/run_c10y_precast_diag.sh: line 64: kill: (70710) - No such process\n/private/tmp/c10y_build/tmpg2yuprjz/tools/run_c10y_precast_diag.sh: line 70: TIMED[@]: unbound variable\n/private/tmp/c10y_build/tmpg2yuprjz/tools/run_c10y_precast_diag.sh: line 48: kill: (-70675) - No such process\nDeadline timer group already exited.\n/private/tmp/c10y_build/tmpg2yuprjz/tools/run_c10y_precast_diag.sh: line 50: 70675 Terminated: 15          ( sleep "$((CAP_SECONDS-CLEANUP_RESERVE-SECONDS))"; : > "$CONTROL/timeout"; stop_owned TERM; sleep 2; stop_owned KILL; sleep "$((CLEANUP_RESERVE-2))"; stop_owned KILL; kill -KILL "$PARENT_PID" )\n')

----------------------------------------------------------------------
Ran 31 tests in 5.535s

FAILED (failures=1)
```


### red_precision.log

```text
test_float64_realization_casts_on_CPU_before_device_transfer (__main__.Contracts.test_float64_realization_casts_on_CPU_before_device_transfer) ... FAIL
test_realized_native_saved_factors_drive_R_predicate (__main__.Contracts.test_realized_native_saved_factors_drive_R_predicate) ... ERROR

======================================================================
ERROR: test_realized_native_saved_factors_drive_R_predicate (__main__.Contracts.test_realized_native_saved_factors_drive_R_predicate)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 336, in test_realized_native_saved_factors_drive_R_predicate
    self.assertEqual(set(numeric['condition_numbers']),{'recipe_A','C10Y'})
                         ~~~~~~~^^^^^^^^^^^^^^^^^^^^^
KeyError: 'condition_numbers'

======================================================================
FAIL: test_float64_realization_casts_on_CPU_before_device_transfer (__main__.Contracts.test_float64_realization_casts_on_CPU_before_device_transfer)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 181, in test_float64_realization_casts_on_CPU_before_device_transfer
    self.assertEqual(float(D.realize(w,u)[0,0]),1.+2.**-10)
                           ^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag.py", line 358, in realize
    return (W0.detach().half()+A.to_like(update,W0.detach().half())).half()
                               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1124, in __call__
    return self._mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1128, in _mock_call
    return self._execute_mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1189, in _execute_mock_call
    result = effect(*args, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 177, in transfer
    self.assertEqual(t.dtype,torch.float16,'float64 must not be transferred to MPS')
AssertionError: torch.float64 != torch.float16 : float64 must not be transferred to MPS

----------------------------------------------------------------------
Ran 2 tests in 0.331s

FAILED (failures=1, errors=1)
```


### green_precision.log

```text
test_INCONCLUSIVE_precedes_every_other_reading (__main__.Contracts.test_INCONCLUSIVE_precedes_every_other_reading) ... ok
test_R_requires_every_cell_and_A7_device_difference (__main__.Contracts.test_R_requires_every_cell_and_A7_device_difference) ... ok
test_S_needs_direct_trace_evidence_and_K_never_emitted (__main__.Contracts.test_S_needs_direct_trace_evidence_and_K_never_emitted) ... ok
test_device_product_observed_from_original_effective_weight (__main__.Contracts.test_device_product_observed_from_original_effective_weight) ... ok
test_difference_metrics_and_weight_coordinate_columns (__main__.Contracts.test_difference_metrics_and_weight_coordinate_columns) ... ok
test_exclusive_JSON_and_tensor_collision_have_no_sibling (__main__.Contracts.test_exclusive_JSON_and_tensor_collision_have_no_sibling) ... ok
test_fail_closed_gpu_and_fingerprint_records_precede_loader (__main__.Contracts.test_fail_closed_gpu_and_fingerprint_records_precede_loader) ... ok
test_finalizer_incomplete_worker_cannot_publish_R (__main__.Contracts.test_finalizer_incomplete_worker_cannot_publish_R) ... ok
test_finalizer_malformed_worker_preserves_exception_and_inconclusive (__main__.Contracts.test_finalizer_malformed_worker_preserves_exception_and_inconclusive) ... ok
test_finalizer_overwrite_refusal_keeps_terminal_bytes (__main__.Contracts.test_finalizer_overwrite_refusal_keeps_terminal_bytes) ... ok
test_finalizer_rejects_completed_claim_with_incomplete_phases (__main__.Contracts.test_finalizer_rejects_completed_claim_with_incomplete_phases) ... ok
test_float64_realization_cannot_demote_to_float32 (__main__.Contracts.test_float64_realization_cannot_demote_to_float32) ... ok
test_float64_realization_casts_on_CPU_before_device_transfer (__main__.Contracts.test_float64_realization_casts_on_CPU_before_device_transfer) ... ok
test_float64_solve_and_promoted_product_are_distinct (__main__.Contracts.test_float64_solve_and_promoted_product_are_distinct) ... ok
test_forced_native_halt_preserves_capture_and_cleans_weights_globals (__main__.Contracts.test_forced_native_halt_preserves_capture_and_cleans_weights_globals) ... ok
test_fresh_import_is_model_and_torch_free (__main__.Contracts.test_fresh_import_is_model_and_torch_free) ... ok
test_fresh_namespace_existing_directory_and_symlink_refused (__main__.Contracts.test_fresh_namespace_existing_directory_and_symlink_refused) ... ok
test_gate_inputs_fsynced_and_reloaded_before_predicate (__main__.Contracts.test_gate_inputs_fsynced_and_reloaded_before_predicate) ... ok
test_interrupted_serialization_is_incomplete_and_retains_previous_values (__main__.Contracts.test_interrupted_serialization_is_incomplete_and_retains_previous_values) ... ok
test_missing_capture_refuses_instead_of_reimplementing (__main__.Contracts.test_missing_capture_refuses_instead_of_reimplementing) ... ok
test_native_factor_actual_matrix_and_Q_are_compared (__main__.Contracts.test_native_factor_actual_matrix_and_Q_are_compared) ... ok
test_native_missing_factor_Q_is_inconclusive_capture_failure (__main__.Contracts.test_native_missing_factor_Q_is_inconclusive_capture_failure) ... ok
test_nonfinite_operand_persisted_before_halt (__main__.Contracts.test_nonfinite_operand_persisted_before_halt) ... ok
test_observer_original_code_coverage_off_on_and_native_operands (__main__.Contracts.test_observer_original_code_coverage_off_on_and_native_operands) ... ok
test_packet_tamper_refused_before_downstream_consumption (__main__.Contracts.test_packet_tamper_refused_before_downstream_consumption) ... ok
test_real_shell_supervisor_hanging_stub_preserves_timeout_and_kills_worker (__main__.Contracts.test_real_shell_supervisor_hanging_stub_preserves_timeout_and_kills_worker) ... ok
test_real_shell_supervisor_worker_exit_before_start_is_diagnosed (__main__.Contracts.test_real_shell_supervisor_worker_exit_before_start_is_diagnosed) ... ok
test_realized_native_saved_factors_drive_R_predicate (__main__.Contracts.test_realized_native_saved_factors_drive_R_predicate) ... ok
test_restores_optional_recorder_and_preexisting_hook_on_halt (__main__.Contracts.test_restores_optional_recorder_and_preexisting_hook_on_halt) ... ok
test_scope_SHA_drift_refused (__main__.Contracts.test_scope_SHA_drift_refused) ... ok
test_supervisor_timeout_overrides_worker_success_and_preserves_commits (__main__.Contracts.test_supervisor_timeout_overrides_worker_success_and_preserves_commits) ... ok
test_valid_complete_phases_publish_threshold_free_R (__main__.Contracts.test_valid_complete_phases_publish_threshold_free_R) ... ok

----------------------------------------------------------------------
Ran 32 tests in 5.739s

OK
```


### red_observer.log

```text
test_actual_representation_batch_padding_and_indices_captured_without_id_assumption (__main__.Contracts.test_actual_representation_batch_padding_and_indices_captured_without_id_assumption) ... ERROR
test_observer_tensor_inertness_catches_discarded_cur_mutation (__main__.Contracts.test_observer_tensor_inertness_catches_discarded_cur_mutation) ... FAIL
test_missing_reference_Q_retains_available_operands_before_coverage_halt (__main__.Contracts.test_missing_reference_Q_retains_available_operands_before_coverage_halt) ... ERROR

======================================================================
ERROR: test_actual_representation_batch_padding_and_indices_captured_without_id_assumption (__main__.Contracts.test_actual_representation_batch_padding_and_indices_captured_without_id_assumption)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 323, in test_actual_representation_batch_padding_and_indices_captured_without_id_assumption
    result=D.native_capture(h,requests,[torch.eye(3) for _ in range(5)],self.j,'A7_coined_coined')
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag.py", line 306, in native_capture
    if on:observer.validate()
          ^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag.py", line 281, in validate
    self.j.gate('coverage_'+self.arm+'_'+self.path,{'layers':self.layers,'returns':self.returns,'factor_count':self.factor_count,
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag.py", line 61, in gate
    if not passed: raise A.Halt(code,inputs)
                   ^^^^^^^^^^^^^^^^^^^^^^^^^
c10y_directdw_arms.Halt: OBSERVER-COVERAGE: {'layers': [4, 5, 6, 7, 8], 'returns': 1, 'factor_count': 0, 'batches': {4: ['batch_A7_coined_coined_L4_A_0.json'], 5: [], 6: [], 7: [], 8: []}, 'passed': False}

======================================================================
ERROR: test_missing_reference_Q_retains_available_operands_before_coverage_halt (__main__.Contracts.test_missing_reference_Q_retains_available_operands_before_coverage_halt)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 356, in test_missing_reference_Q_retains_available_operands_before_coverage_halt
    partial=D.load_packet(self.root/'operands_A1_single_L4_A_incomplete.pt')
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag.py", line 105, in load_packet
    def load_packet(path): return load_record(Path(path).with_suffix('.json'))
                                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag.py", line 87, in load_record
    path=Path(path);payload=A.strict_load(path);tensors={}
                            ^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_arms.py", line 122, in strict_load
    def strict_load(path): return strict_json(Path(path).read_bytes())
                                              ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/pathlib.py", line 1050, in read_bytes
    with self.open(mode='rb') as f:
         ^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/pathlib.py", line 1044, in open
    return io.open(self, mode, buffering, encoding, errors, newline)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
FileNotFoundError: [Errno 2] No such file or directory: '/private/tmp/c10y_build/tmpv3nqlahr/operands_A1_single_L4_A_incomplete.json'

======================================================================
FAIL: test_observer_tensor_inertness_catches_discarded_cur_mutation (__main__.Contracts.test_observer_tensor_inertness_catches_discarded_cur_mutation)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 341, in test_observer_tensor_inertness_catches_discarded_cur_mutation
    with self.assertRaisesRegex(A.Halt,'OBSERVER-TENSOR-INERTNESS'):
AssertionError: Halt not raised

----------------------------------------------------------------------
Ran 3 tests in 0.101s

FAILED (failures=1, errors=2)
```


### green_observer.log

```text
test_INCONCLUSIVE_precedes_every_other_reading (__main__.Contracts.test_INCONCLUSIVE_precedes_every_other_reading) ... ok
test_R_requires_every_cell_and_A7_device_difference (__main__.Contracts.test_R_requires_every_cell_and_A7_device_difference) ... ok
test_S_needs_direct_trace_evidence_and_K_never_emitted (__main__.Contracts.test_S_needs_direct_trace_evidence_and_K_never_emitted) ... ok
test_actual_representation_batch_padding_and_indices_captured_without_id_assumption (__main__.Contracts.test_actual_representation_batch_padding_and_indices_captured_without_id_assumption) ... FAIL
test_device_product_observed_from_original_effective_weight (__main__.Contracts.test_device_product_observed_from_original_effective_weight) ... ok
test_difference_metrics_and_weight_coordinate_columns (__main__.Contracts.test_difference_metrics_and_weight_coordinate_columns) ... ok
test_exclusive_JSON_and_tensor_collision_have_no_sibling (__main__.Contracts.test_exclusive_JSON_and_tensor_collision_have_no_sibling) ... ok
test_fail_closed_gpu_and_fingerprint_records_precede_loader (__main__.Contracts.test_fail_closed_gpu_and_fingerprint_records_precede_loader) ... ok
test_finalizer_incomplete_worker_cannot_publish_R (__main__.Contracts.test_finalizer_incomplete_worker_cannot_publish_R) ... ok
test_finalizer_malformed_worker_preserves_exception_and_inconclusive (__main__.Contracts.test_finalizer_malformed_worker_preserves_exception_and_inconclusive) ... ok
test_finalizer_overwrite_refusal_keeps_terminal_bytes (__main__.Contracts.test_finalizer_overwrite_refusal_keeps_terminal_bytes) ... ok
test_finalizer_rejects_completed_claim_with_incomplete_phases (__main__.Contracts.test_finalizer_rejects_completed_claim_with_incomplete_phases) ... ok
test_float64_realization_cannot_demote_to_float32 (__main__.Contracts.test_float64_realization_cannot_demote_to_float32) ... ok
test_float64_realization_casts_on_CPU_before_device_transfer (__main__.Contracts.test_float64_realization_casts_on_CPU_before_device_transfer) ... ok
test_float64_solve_and_promoted_product_are_distinct (__main__.Contracts.test_float64_solve_and_promoted_product_are_distinct) ... ok
test_forced_native_halt_preserves_capture_and_cleans_weights_globals (__main__.Contracts.test_forced_native_halt_preserves_capture_and_cleans_weights_globals) ... ok
test_fresh_import_is_model_and_torch_free (__main__.Contracts.test_fresh_import_is_model_and_torch_free) ... ok
test_fresh_namespace_existing_directory_and_symlink_refused (__main__.Contracts.test_fresh_namespace_existing_directory_and_symlink_refused) ... ok
test_full_weight_coordinate_quantiles_exceed_torch_limit (__main__.Contracts.test_full_weight_coordinate_quantiles_exceed_torch_limit) ... ok
test_gate_inputs_fsynced_and_reloaded_before_predicate (__main__.Contracts.test_gate_inputs_fsynced_and_reloaded_before_predicate) ... ok
test_interrupted_serialization_is_incomplete_and_retains_previous_values (__main__.Contracts.test_interrupted_serialization_is_incomplete_and_retains_previous_values) ... ok
test_missing_capture_refuses_instead_of_reimplementing (__main__.Contracts.test_missing_capture_refuses_instead_of_reimplementing) ... ok
test_missing_reference_Q_retains_available_operands_before_coverage_halt (__main__.Contracts.test_missing_reference_Q_retains_available_operands_before_coverage_halt) ... ok
test_native_factor_actual_matrix_and_Q_are_compared (__main__.Contracts.test_native_factor_actual_matrix_and_Q_are_compared) ... ok
test_native_missing_factor_Q_is_inconclusive_capture_failure (__main__.Contracts.test_native_missing_factor_Q_is_inconclusive_capture_failure) ... ok
test_nonfinite_operand_persisted_before_halt (__main__.Contracts.test_nonfinite_operand_persisted_before_halt) ... ok
test_observer_original_code_coverage_off_on_and_native_operands (__main__.Contracts.test_observer_original_code_coverage_off_on_and_native_operands) ... ok
test_observer_tensor_inertness_catches_discarded_cur_mutation (__main__.Contracts.test_observer_tensor_inertness_catches_discarded_cur_mutation) ... ok
test_packet_tamper_refused_before_downstream_consumption (__main__.Contracts.test_packet_tamper_refused_before_downstream_consumption) ... ok
test_real_shell_supervisor_hanging_stub_preserves_timeout_and_kills_worker (__main__.Contracts.test_real_shell_supervisor_hanging_stub_preserves_timeout_and_kills_worker) ... ok
test_real_shell_supervisor_worker_exit_before_start_is_diagnosed (__main__.Contracts.test_real_shell_supervisor_worker_exit_before_start_is_diagnosed) ... ok
test_realized_native_saved_factors_drive_R_predicate (__main__.Contracts.test_realized_native_saved_factors_drive_R_predicate) ... ok
test_restores_optional_recorder_and_preexisting_hook_on_halt (__main__.Contracts.test_restores_optional_recorder_and_preexisting_hook_on_halt) ... ok
test_scope_SHA_drift_refused (__main__.Contracts.test_scope_SHA_drift_refused) ... ok
test_supervisor_timeout_overrides_worker_success_and_preserves_commits (__main__.Contracts.test_supervisor_timeout_overrides_worker_success_and_preserves_commits) ... ok
test_valid_complete_phases_publish_threshold_free_R (__main__.Contracts.test_valid_complete_phases_publish_threshold_free_R) ... ok

======================================================================
FAIL: test_actual_representation_batch_padding_and_indices_captured_without_id_assumption (__main__.Contracts.test_actual_representation_batch_padding_and_indices_captured_without_id_assumption)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 328, in test_actual_representation_batch_padding_and_indices_captured_without_id_assumption
    self.assertEqual(len(value['batches']),2)
AssertionError: 4 != 2

----------------------------------------------------------------------
Ran 36 tests in 6.546s

FAILED (failures=1)
```


### green_final.log

```text
test_INCONCLUSIVE_precedes_every_other_reading (__main__.Contracts.test_INCONCLUSIVE_precedes_every_other_reading) ... ok
test_R_requires_every_cell_and_A7_device_difference (__main__.Contracts.test_R_requires_every_cell_and_A7_device_difference) ... ok
test_S_needs_direct_trace_evidence_and_K_never_emitted (__main__.Contracts.test_S_needs_direct_trace_evidence_and_K_never_emitted) ... ok
test_actual_representation_batch_padding_and_indices_captured_without_id_assumption (__main__.Contracts.test_actual_representation_batch_padding_and_indices_captured_without_id_assumption) ... ok
test_device_product_observed_from_original_effective_weight (__main__.Contracts.test_device_product_observed_from_original_effective_weight) ... ok
test_difference_metrics_and_weight_coordinate_columns (__main__.Contracts.test_difference_metrics_and_weight_coordinate_columns) ... ok
test_exclusive_JSON_and_tensor_collision_have_no_sibling (__main__.Contracts.test_exclusive_JSON_and_tensor_collision_have_no_sibling) ... ok
test_fail_closed_gpu_and_fingerprint_records_precede_loader (__main__.Contracts.test_fail_closed_gpu_and_fingerprint_records_precede_loader) ... ok
test_finalizer_incomplete_worker_cannot_publish_R (__main__.Contracts.test_finalizer_incomplete_worker_cannot_publish_R) ... ok
test_finalizer_malformed_worker_preserves_exception_and_inconclusive (__main__.Contracts.test_finalizer_malformed_worker_preserves_exception_and_inconclusive) ... ok
test_finalizer_overwrite_refusal_keeps_terminal_bytes (__main__.Contracts.test_finalizer_overwrite_refusal_keeps_terminal_bytes) ... ok
test_finalizer_rejects_completed_claim_with_incomplete_phases (__main__.Contracts.test_finalizer_rejects_completed_claim_with_incomplete_phases) ... ok
test_float64_realization_cannot_demote_to_float32 (__main__.Contracts.test_float64_realization_cannot_demote_to_float32) ... ok
test_float64_realization_casts_on_CPU_before_device_transfer (__main__.Contracts.test_float64_realization_casts_on_CPU_before_device_transfer) ... ok
test_float64_solve_and_promoted_product_are_distinct (__main__.Contracts.test_float64_solve_and_promoted_product_are_distinct) ... ok
test_forced_native_halt_preserves_capture_and_cleans_weights_globals (__main__.Contracts.test_forced_native_halt_preserves_capture_and_cleans_weights_globals) ... ok
test_fresh_import_is_model_and_torch_free (__main__.Contracts.test_fresh_import_is_model_and_torch_free) ... ok
test_fresh_namespace_existing_directory_and_symlink_refused (__main__.Contracts.test_fresh_namespace_existing_directory_and_symlink_refused) ... ok
test_full_weight_coordinate_quantiles_exceed_torch_limit (__main__.Contracts.test_full_weight_coordinate_quantiles_exceed_torch_limit) ... ok
test_gate_inputs_fsynced_and_reloaded_before_predicate (__main__.Contracts.test_gate_inputs_fsynced_and_reloaded_before_predicate) ... ok
test_interrupted_serialization_is_incomplete_and_retains_previous_values (__main__.Contracts.test_interrupted_serialization_is_incomplete_and_retains_previous_values) ... ok
test_missing_capture_refuses_instead_of_reimplementing (__main__.Contracts.test_missing_capture_refuses_instead_of_reimplementing) ... ok
test_missing_reference_Q_retains_available_operands_before_coverage_halt (__main__.Contracts.test_missing_reference_Q_retains_available_operands_before_coverage_halt) ... ok
test_native_factor_actual_matrix_and_Q_are_compared (__main__.Contracts.test_native_factor_actual_matrix_and_Q_are_compared) ... ok
test_native_missing_factor_Q_is_inconclusive_capture_failure (__main__.Contracts.test_native_missing_factor_Q_is_inconclusive_capture_failure) ... ok
test_nonfinite_operand_persisted_before_halt (__main__.Contracts.test_nonfinite_operand_persisted_before_halt) ... ok
test_observer_original_code_coverage_off_on_and_native_operands (__main__.Contracts.test_observer_original_code_coverage_off_on_and_native_operands) ... ok
test_observer_tensor_inertness_catches_discarded_cur_mutation (__main__.Contracts.test_observer_tensor_inertness_catches_discarded_cur_mutation) ... ok
test_packet_tamper_refused_before_downstream_consumption (__main__.Contracts.test_packet_tamper_refused_before_downstream_consumption) ... ok
test_real_shell_supervisor_hanging_stub_preserves_timeout_and_kills_worker (__main__.Contracts.test_real_shell_supervisor_hanging_stub_preserves_timeout_and_kills_worker) ... ok
test_real_shell_supervisor_worker_exit_before_start_is_diagnosed (__main__.Contracts.test_real_shell_supervisor_worker_exit_before_start_is_diagnosed) ... ok
test_realized_native_saved_factors_drive_R_predicate (__main__.Contracts.test_realized_native_saved_factors_drive_R_predicate) ... ok
test_restores_optional_recorder_and_preexisting_hook_on_halt (__main__.Contracts.test_restores_optional_recorder_and_preexisting_hook_on_halt) ... ok
test_scope_SHA_drift_refused (__main__.Contracts.test_scope_SHA_drift_refused) ... ok
test_supervisor_timeout_overrides_worker_success_and_preserves_commits (__main__.Contracts.test_supervisor_timeout_overrides_worker_success_and_preserves_commits) ... ok
test_valid_complete_phases_publish_threshold_free_R (__main__.Contracts.test_valid_complete_phases_publish_threshold_free_R) ... ok

----------------------------------------------------------------------
Ran 36 tests in 6.560s

OK
```


### directdw_regression.log

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
Ran 285 tests in 22.740s

OK
{"launched": false, "reasons": ["missing/unknown/duplicate phases"], "status": "UNVERIFIED"}
ISOLATION OWNED LISTING DRIFT: []
ISOLATION OTHER OBSERVED UNATTRIBUTED: []
SYS_MODULES_FORBIDDEN: []
C10Y_DIRECTDW_SELFTEST PASS — CPU ONLY; LIVE LAW#3/LAW#5 UNVERIFIED
```


### red_audit.log

```text
test_completed_native_CPU_product_survives_later_control_halt (__main__.Contracts.test_completed_native_CPU_product_survives_later_control_halt) ... ERROR
test_native_direct_update_included_in_all_pair_measurements (__main__.Contracts.test_native_direct_update_included_in_all_pair_measurements) ... FAIL
test_repeat_factor_compared_to_original_native_solution (__main__.Contracts.test_repeat_factor_compared_to_original_native_solution) ... FAIL
test_completed_float64_direct_solution_survives_next_solve_failure (__main__.Contracts.test_completed_float64_direct_solution_survives_next_solve_failure) ... ERROR
test_malformed_classification_capture_is_INCONCLUSIVE (__main__.Contracts.test_malformed_classification_capture_is_INCONCLUSIVE) ... 
  test_malformed_classification_capture_is_INCONCLUSIVE (__main__.Contracts.test_malformed_classification_capture_is_INCONCLUSIVE) (value={'requirements': None, 'cells': [{'arm': 'A7_coined_coined', 'layer': 4, 'operands_equal': True, 'states_equal': True, 'repeats_stable': True, 'cpu_realized_identical': True, 'mps_realized_identical': False, 'discrepancies': []}, {'arm': 'A7_coined_coined', 'layer': 5, 'operands_equal': True, 'states_equal': True, 'repeats_stable': True, 'cpu_realized_identical': True, 'mps_realized_identical': True, 'discrepancies': []}, {'arm': 'A7_coined_coined', 'layer': 6, 'operands_equal': True, 'states_equal': True, 'repeats_stable': True, 'cpu_realized_identical': True, 'mps_realized_identical': True, 'discrepancies': []}, {'arm': 'A7_coined_coined', 'layer': 7, 'operands_equal': True, 'states_equal': True, 'repeats_stable': True, 'cpu_realized_identical': True, 'mps_realized_identical': True, 'discrepancies': []}, {'arm': 'A7_coined_coined', 'layer': 8, 'operands_equal': True, 'states_equal': True, 'repeats_stable': True, 'cpu_realized_identical': True, 'mps_realized_identical': True, 'discrepancies': []}, {'arm': 'A1_single', 'layer': 4, 'operands_equal': True, 'states_equal': True, 'repeats_stable': True, 'cpu_realized_identical': True, 'mps_realized_identical': True, 'discrepancies': []}, {'arm': 'A1_single', 'layer': 5, 'operands_equal': True, 'states_equal': True, 'repeats_stable': True, 'cpu_realized_identical': True, 'mps_realized_identical': True, 'discrepancies': []}, {'arm': 'A1_single', 'layer': 6, 'operands_equal': True, 'states_equal': True, 'repeats_stable': True, 'cpu_realized_identical': True, 'mps_realized_identical': True, 'discrepancies': []}, {'arm': 'A1_single', 'layer': 7, 'operands_equal': True, 'states_equal': True, 'repeats_stable': True, 'cpu_realized_identical': True, 'mps_realized_identical': True, 'discrepancies': []}, {'arm': 'A1_single', 'layer': 8, 'operands_equal': True, 'states_equal': True, 'repeats_stable': True, 'cpu_realized_identical': True, 'mps_realized_identical': True, 'discrepancies': []}]}) ... ERROR
  test_malformed_classification_capture_is_INCONCLUSIVE (__main__.Contracts.test_malformed_classification_capture_is_INCONCLUSIVE) (value={'requirements': {'capture': True, 'source_identity': True, 'observer': True, 'persistence': True, 'finiteness': True, 'resource': True, 'deadline': True, 'cleanup': True}, 'cells': [None, {'arm': 'A7_coined_coined', 'layer': 5, 'operands_equal': True, 'states_equal': True, 'repeats_stable': True, 'cpu_realized_identical': True, 'mps_realized_identical': True, 'discrepancies': []}, {'arm': 'A7_coined_coined', 'layer': 6, 'operands_equal': True, 'states_equal': True, 'repeats_stable': True, 'cpu_realized_identical': True, 'mps_realized_identical': True, 'discrepancies': []}, {'arm': 'A7_coined_coined', 'layer': 7, 'operands_equal': True, 'states_equal': True, 'repeats_stable': True, 'cpu_realized_identical': True, 'mps_realized_identical': True, 'discrepancies': []}, {'arm': 'A7_coined_coined', 'layer': 8, 'operands_equal': True, 'states_equal': True, 'repeats_stable': True, 'cpu_realized_identical': True, 'mps_realized_identical': True, 'discrepancies': []}, {'arm': 'A1_single', 'layer': 4, 'operands_equal': True, 'states_equal': True, 'repeats_stable': True, 'cpu_realized_identical': True, 'mps_realized_identical': True, 'discrepancies': []}, {'arm': 'A1_single', 'layer': 5, 'operands_equal': True, 'states_equal': True, 'repeats_stable': True, 'cpu_realized_identical': True, 'mps_realized_identical': True, 'discrepancies': []}, {'arm': 'A1_single', 'layer': 6, 'operands_equal': True, 'states_equal': True, 'repeats_stable': True, 'cpu_realized_identical': True, 'mps_realized_identical': True, 'discrepancies': []}, {'arm': 'A1_single', 'layer': 7, 'operands_equal': True, 'states_equal': True, 'repeats_stable': True, 'cpu_realized_identical': True, 'mps_realized_identical': True, 'discrepancies': []}, {'arm': 'A1_single', 'layer': 8, 'operands_equal': True, 'states_equal': True, 'repeats_stable': True, 'cpu_realized_identical': True, 'mps_realized_identical': True, 'discrepancies': []}]}) ... ERROR
  test_malformed_classification_capture_is_INCONCLUSIVE (__main__.Contracts.test_malformed_classification_capture_is_INCONCLUSIVE) (value={'requirements': {'capture': True, 'source_identity': True, 'observer': True, 'persistence': True, 'finiteness': True, 'resource': True, 'deadline': True, 'cleanup': True}, 'cells': [{'arm': 'A7_coined_coined', 'layer': 4, 'operands_equal': False, 'states_equal': True, 'repeats_stable': True, 'cpu_realized_identical': True, 'mps_realized_identical': False, 'discrepancies': [None]}, {'arm': 'A7_coined_coined', 'layer': 5, 'operands_equal': True, 'states_equal': True, 'repeats_stable': True, 'cpu_realized_identical': True, 'mps_realized_identical': True, 'discrepancies': []}, {'arm': 'A7_coined_coined', 'layer': 6, 'operands_equal': True, 'states_equal': True, 'repeats_stable': True, 'cpu_realized_identical': True, 'mps_realized_identical': True, 'discrepancies': []}, {'arm': 'A7_coined_coined', 'layer': 7, 'operands_equal': True, 'states_equal': True, 'repeats_stable': True, 'cpu_realized_identical': True, 'mps_realized_identical': True, 'discrepancies': []}, {'arm': 'A7_coined_coined', 'layer': 8, 'operands_equal': True, 'states_equal': True, 'repeats_stable': True, 'cpu_realized_identical': True, 'mps_realized_identical': True, 'discrepancies': []}, {'arm': 'A1_single', 'layer': 4, 'operands_equal': True, 'states_equal': True, 'repeats_stable': True, 'cpu_realized_identical': True, 'mps_realized_identical': True, 'discrepancies': []}, {'arm': 'A1_single', 'layer': 5, 'operands_equal': True, 'states_equal': True, 'repeats_stable': True, 'cpu_realized_identical': True, 'mps_realized_identical': True, 'discrepancies': []}, {'arm': 'A1_single', 'layer': 6, 'operands_equal': True, 'states_equal': True, 'repeats_stable': True, 'cpu_realized_identical': True, 'mps_realized_identical': True, 'discrepancies': []}, {'arm': 'A1_single', 'layer': 7, 'operands_equal': True, 'states_equal': True, 'repeats_stable': True, 'cpu_realized_identical': True, 'mps_realized_identical': True, 'discrepancies': []}, {'arm': 'A1_single', 'layer': 8, 'operands_equal': True, 'states_equal': True, 'repeats_stable': True, 'cpu_realized_identical': True, 'mps_realized_identical': True, 'discrepancies': []}]}) ... ERROR

======================================================================
ERROR: test_completed_native_CPU_product_survives_later_control_halt (__main__.Contracts.test_completed_native_CPU_product_survives_later_control_halt)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 413, in test_completed_native_CPU_product_survives_later_control_halt
    value=D.load_record(self.root/'controls_A7_coined_coined_L4_native_cpu32_product.json')
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag.py", line 87, in load_record
    path=Path(path);payload=A.strict_load(path);tensors={}
                            ^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_arms.py", line 122, in strict_load
    def strict_load(path): return strict_json(Path(path).read_bytes())
                                              ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/pathlib.py", line 1050, in read_bytes
    with self.open(mode='rb') as f:
         ^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/pathlib.py", line 1044, in open
    return io.open(self, mode, buffering, encoding, errors, newline)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
FileNotFoundError: [Errno 2] No such file or directory: '/private/tmp/c10y_build/tmpq8un1cu0/controls_A7_coined_coined_L4_native_cpu32_product.json'

======================================================================
ERROR: test_completed_float64_direct_solution_survives_next_solve_failure (__main__.Contracts.test_completed_float64_direct_solution_survives_next_solve_failure)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 445, in test_completed_float64_direct_solution_survives_next_solve_failure
    value=D.load_record(self.root/'test_direct_solution64.json')
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag.py", line 87, in load_record
    path=Path(path);payload=A.strict_load(path);tensors={}
                            ^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_arms.py", line 122, in strict_load
    def strict_load(path): return strict_json(Path(path).read_bytes())
                                              ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/pathlib.py", line 1050, in read_bytes
    with self.open(mode='rb') as f:
         ^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/pathlib.py", line 1044, in open
    return io.open(self, mode, buffering, encoding, errors, newline)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
FileNotFoundError: [Errno 2] No such file or directory: '/private/tmp/c10y_build/tmpozl0ymft/test_direct_solution64.json'

======================================================================
ERROR: test_malformed_classification_capture_is_INCONCLUSIVE (__main__.Contracts.test_malformed_classification_capture_is_INCONCLUSIVE) (value={'requirements': None, 'cells': [{'arm': 'A7_coined_coined', 'layer': 4, 'operands_equal': True, 'states_equal': True, 'repeats_stable': True, 'cpu_realized_identical': True, 'mps_realized_identical': False, 'discrepancies': []}, {'arm': 'A7_coined_coined', 'layer': 5, 'operands_equal': True, 'states_equal': True, 'repeats_stable': True, 'cpu_realized_identical': True, 'mps_realized_identical': True, 'discrepancies': []}, {'arm': 'A7_coined_coined', 'layer': 6, 'operands_equal': True, 'states_equal': True, 'repeats_stable': True, 'cpu_realized_identical': True, 'mps_realized_identical': True, 'discrepancies': []}, {'arm': 'A7_coined_coined', 'layer': 7, 'operands_equal': True, 'states_equal': True, 'repeats_stable': True, 'cpu_realized_identical': True, 'mps_realized_identical': True, 'discrepancies': []}, {'arm': 'A7_coined_coined', 'layer': 8, 'operands_equal': True, 'states_equal': True, 'repeats_stable': True, 'cpu_realized_identical': True, 'mps_realized_identical': True, 'discrepancies': []}, {'arm': 'A1_single', 'layer': 4, 'operands_equal': True, 'states_equal': True, 'repeats_stable': True, 'cpu_realized_identical': True, 'mps_realized_identical': True, 'discrepancies': []}, {'arm': 'A1_single', 'layer': 5, 'operands_equal': True, 'states_equal': True, 'repeats_stable': True, 'cpu_realized_identical': True, 'mps_realized_identical': True, 'discrepancies': []}, {'arm': 'A1_single', 'layer': 6, 'operands_equal': True, 'states_equal': True, 'repeats_stable': True, 'cpu_realized_identical': True, 'mps_realized_identical': True, 'discrepancies': []}, {'arm': 'A1_single', 'layer': 7, 'operands_equal': True, 'states_equal': True, 'repeats_stable': True, 'cpu_realized_identical': True, 'mps_realized_identical': True, 'discrepancies': []}, {'arm': 'A1_single', 'layer': 8, 'operands_equal': True, 'states_equal': True, 'repeats_stable': True, 'cpu_realized_identical': True, 'mps_realized_identical': True, 'discrepancies': []}]})
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 454, in test_malformed_classification_capture_is_INCONCLUSIVE
    with self.subTest(value=value):self.assertEqual(D.classify(value)['label'],'INCONCLUSIVE')
                                                    ^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag.py", line 138, in classify
    if not valid or any(req.get(k) is not True for k in REQUIREMENTS):
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag.py", line 138, in <genexpr>
    if not valid or any(req.get(k) is not True for k in REQUIREMENTS):
                        ^^^^^^^
AttributeError: 'NoneType' object has no attribute 'get'

======================================================================
ERROR: test_malformed_classification_capture_is_INCONCLUSIVE (__main__.Contracts.test_malformed_classification_capture_is_INCONCLUSIVE) (value={'requirements': {'capture': True, 'source_identity': True, 'observer': True, 'persistence': True, 'finiteness': True, 'resource': True, 'deadline': True, 'cleanup': True}, 'cells': [None, {'arm': 'A7_coined_coined', 'layer': 5, 'operands_equal': True, 'states_equal': True, 'repeats_stable': True, 'cpu_realized_identical': True, 'mps_realized_identical': True, 'discrepancies': []}, {'arm': 'A7_coined_coined', 'layer': 6, 'operands_equal': True, 'states_equal': True, 'repeats_stable': True, 'cpu_realized_identical': True, 'mps_realized_identical': True, 'discrepancies': []}, {'arm': 'A7_coined_coined', 'layer': 7, 'operands_equal': True, 'states_equal': True, 'repeats_stable': True, 'cpu_realized_identical': True, 'mps_realized_identical': True, 'discrepancies': []}, {'arm': 'A7_coined_coined', 'layer': 8, 'operands_equal': True, 'states_equal': True, 'repeats_stable': True, 'cpu_realized_identical': True, 'mps_realized_identical': True, 'discrepancies': []}, {'arm': 'A1_single', 'layer': 4, 'operands_equal': True, 'states_equal': True, 'repeats_stable': True, 'cpu_realized_identical': True, 'mps_realized_identical': True, 'discrepancies': []}, {'arm': 'A1_single', 'layer': 5, 'operands_equal': True, 'states_equal': True, 'repeats_stable': True, 'cpu_realized_identical': True, 'mps_realized_identical': True, 'discrepancies': []}, {'arm': 'A1_single', 'layer': 6, 'operands_equal': True, 'states_equal': True, 'repeats_stable': True, 'cpu_realized_identical': True, 'mps_realized_identical': True, 'discrepancies': []}, {'arm': 'A1_single', 'layer': 7, 'operands_equal': True, 'states_equal': True, 'repeats_stable': True, 'cpu_realized_identical': True, 'mps_realized_identical': True, 'discrepancies': []}, {'arm': 'A1_single', 'layer': 8, 'operands_equal': True, 'states_equal': True, 'repeats_stable': True, 'cpu_realized_identical': True, 'mps_realized_identical': True, 'discrepancies': []}]})
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 454, in test_malformed_classification_capture_is_INCONCLUSIVE
    with self.subTest(value=value):self.assertEqual(D.classify(value)['label'],'INCONCLUSIVE')
                                                    ^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag.py", line 136, in classify
    valid=isinstance(cells,list) and len(cells)==10 and {(c.get('arm'),c.get('layer')) for c in cells}==expected
                                                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag.py", line 136, in <setcomp>
    valid=isinstance(cells,list) and len(cells)==10 and {(c.get('arm'),c.get('layer')) for c in cells}==expected
                                                          ^^^^^
AttributeError: 'NoneType' object has no attribute 'get'

======================================================================
ERROR: test_malformed_classification_capture_is_INCONCLUSIVE (__main__.Contracts.test_malformed_classification_capture_is_INCONCLUSIVE) (value={'requirements': {'capture': True, 'source_identity': True, 'observer': True, 'persistence': True, 'finiteness': True, 'resource': True, 'deadline': True, 'cleanup': True}, 'cells': [{'arm': 'A7_coined_coined', 'layer': 4, 'operands_equal': False, 'states_equal': True, 'repeats_stable': True, 'cpu_realized_identical': True, 'mps_realized_identical': False, 'discrepancies': [None]}, {'arm': 'A7_coined_coined', 'layer': 5, 'operands_equal': True, 'states_equal': True, 'repeats_stable': True, 'cpu_realized_identical': True, 'mps_realized_identical': True, 'discrepancies': []}, {'arm': 'A7_coined_coined', 'layer': 6, 'operands_equal': True, 'states_equal': True, 'repeats_stable': True, 'cpu_realized_identical': True, 'mps_realized_identical': True, 'discrepancies': []}, {'arm': 'A7_coined_coined', 'layer': 7, 'operands_equal': True, 'states_equal': True, 'repeats_stable': True, 'cpu_realized_identical': True, 'mps_realized_identical': True, 'discrepancies': []}, {'arm': 'A7_coined_coined', 'layer': 8, 'operands_equal': True, 'states_equal': True, 'repeats_stable': True, 'cpu_realized_identical': True, 'mps_realized_identical': True, 'discrepancies': []}, {'arm': 'A1_single', 'layer': 4, 'operands_equal': True, 'states_equal': True, 'repeats_stable': True, 'cpu_realized_identical': True, 'mps_realized_identical': True, 'discrepancies': []}, {'arm': 'A1_single', 'layer': 5, 'operands_equal': True, 'states_equal': True, 'repeats_stable': True, 'cpu_realized_identical': True, 'mps_realized_identical': True, 'discrepancies': []}, {'arm': 'A1_single', 'layer': 6, 'operands_equal': True, 'states_equal': True, 'repeats_stable': True, 'cpu_realized_identical': True, 'mps_realized_identical': True, 'discrepancies': []}, {'arm': 'A1_single', 'layer': 7, 'operands_equal': True, 'states_equal': True, 'repeats_stable': True, 'cpu_realized_identical': True, 'mps_realized_identical': True, 'discrepancies': []}, {'arm': 'A1_single', 'layer': 8, 'operands_equal': True, 'states_equal': True, 'repeats_stable': True, 'cpu_realized_identical': True, 'mps_realized_identical': True, 'discrepancies': []}]})
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 454, in test_malformed_classification_capture_is_INCONCLUSIVE
    with self.subTest(value=value):self.assertEqual(D.classify(value)['label'],'INCONCLUSIVE')
                                                    ^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag.py", line 143, in classify
    direct=[d for c in cells for d in c['discrepancies'] if d.get('kind') in ('operand','state','orientation','formula') and all(d.get(k) for k in ('field','left','right'))]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag.py", line 143, in <listcomp>
    direct=[d for c in cells for d in c['discrepancies'] if d.get('kind') in ('operand','state','orientation','formula') and all(d.get(k) for k in ('field','left','right'))]
                                                            ^^^^^
AttributeError: 'NoneType' object has no attribute 'get'

======================================================================
FAIL: test_native_direct_update_included_in_all_pair_measurements (__main__.Contracts.test_native_direct_update_included_in_all_pair_measurements)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 421, in test_native_direct_update_included_in_all_pair_measurements
    self.assertIn('native_direct',updates)
AssertionError: 'native_direct' not found in {'assembled32_direct64': tensor([[0.0250, 0.1250, 0.1500],
        [0.1250, 0.0250, 0.1500]], dtype=torch.float64), 'assembled32_factored64': tensor([[0.0250, 0.1250, 0.1500],
        [0.1250, 0.0250, 0.1500]], dtype=torch.float64), 'common_device': tensor([[0.0250, 0.1250, 0.1500],
        [0.1250, 0.0250, 0.1500]]), 'cpu32_product': tensor([[0.0250, 0.1250, 0.1500],
        [0.1250, 0.0250, 0.1500]]), 'cpu32_product_repeat': tensor([[0.0250, 0.1250, 0.1500],
        [0.1250, 0.0250, 0.1500]]), 'device_repeat': tensor([[0.0250, 0.1250, 0.1500],
        [0.1250, 0.0250, 0.1500]]), 'direct32_repeat': tensor([[0.0250, 0.1250, 0.1500],
        [0.1250, 0.0250, 0.1500]]), 'factor32_repeat_product': tensor([[0.0250, 0.1250, 0.1500],
        [0.1250, 0.0250, 0.1500]]), 'native_cpu32_product': tensor([[0.0250, 0.1250, 0.1500],
        [0.1250, 0.0250, 0.1500]]), 'native_device': tensor([[0.0250, 0.1250, 0.1500],
        [0.1250, 0.0250, 0.1500]]), 'promoted32_product': tensor([[0.0250, 0.1250, 0.1500],
        [0.1250, 0.0250, 0.1500]], dtype=torch.float64), 'recipe_A': tensor([[0.0250, 0.1250, 0.1500],
        [0.1250, 0.0250, 0.1500]]), 'solve64_direct': tensor([[0.0250, 0.1250, 0.1500],
        [0.1250, 0.0250, 0.1500]], dtype=torch.float64), 'solve64_factored': tensor([[0.0250, 0.1250, 0.1500],
        [0.1250, 0.0250, 0.1500]], dtype=torch.float64)}

======================================================================
FAIL: test_repeat_factor_compared_to_original_native_solution (__main__.Contracts.test_repeat_factor_compared_to_original_native_solution)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 434, in test_repeat_factor_compared_to_original_native_solution
    self.assertFalse(value['repeats_stable'])
AssertionError: True is not false

----------------------------------------------------------------------
Ran 5 tests in 0.892s

FAILED (failures=2, errors=5)
```


### green_audit.log

```text
test_INCONCLUSIVE_precedes_every_other_reading (__main__.Contracts.test_INCONCLUSIVE_precedes_every_other_reading) ... ok
test_R_requires_every_cell_and_A7_device_difference (__main__.Contracts.test_R_requires_every_cell_and_A7_device_difference) ... ok
test_S_needs_direct_trace_evidence_and_K_never_emitted (__main__.Contracts.test_S_needs_direct_trace_evidence_and_K_never_emitted) ... ok
test_actual_representation_batch_padding_and_indices_captured_without_id_assumption (__main__.Contracts.test_actual_representation_batch_padding_and_indices_captured_without_id_assumption) ... ok
test_completed_float64_direct_solution_survives_next_solve_failure (__main__.Contracts.test_completed_float64_direct_solution_survives_next_solve_failure) ... ok
test_completed_native_CPU_product_survives_later_control_halt (__main__.Contracts.test_completed_native_CPU_product_survives_later_control_halt) ... ok
test_device_product_observed_from_original_effective_weight (__main__.Contracts.test_device_product_observed_from_original_effective_weight) ... ok
test_difference_metrics_and_weight_coordinate_columns (__main__.Contracts.test_difference_metrics_and_weight_coordinate_columns) ... ok
test_exclusive_JSON_and_tensor_collision_have_no_sibling (__main__.Contracts.test_exclusive_JSON_and_tensor_collision_have_no_sibling) ... ok
test_fail_closed_gpu_and_fingerprint_records_precede_loader (__main__.Contracts.test_fail_closed_gpu_and_fingerprint_records_precede_loader) ... ok
test_finalizer_incomplete_worker_cannot_publish_R (__main__.Contracts.test_finalizer_incomplete_worker_cannot_publish_R) ... ok
test_finalizer_malformed_worker_preserves_exception_and_inconclusive (__main__.Contracts.test_finalizer_malformed_worker_preserves_exception_and_inconclusive) ... ok
test_finalizer_overwrite_refusal_keeps_terminal_bytes (__main__.Contracts.test_finalizer_overwrite_refusal_keeps_terminal_bytes) ... ok
test_finalizer_rejects_completed_claim_with_incomplete_phases (__main__.Contracts.test_finalizer_rejects_completed_claim_with_incomplete_phases) ... ok
test_float64_realization_cannot_demote_to_float32 (__main__.Contracts.test_float64_realization_cannot_demote_to_float32) ... ok
test_float64_realization_casts_on_CPU_before_device_transfer (__main__.Contracts.test_float64_realization_casts_on_CPU_before_device_transfer) ... ok
test_float64_solve_and_promoted_product_are_distinct (__main__.Contracts.test_float64_solve_and_promoted_product_are_distinct) ... ok
test_forced_native_halt_preserves_capture_and_cleans_weights_globals (__main__.Contracts.test_forced_native_halt_preserves_capture_and_cleans_weights_globals) ... ok
test_fresh_import_is_model_and_torch_free (__main__.Contracts.test_fresh_import_is_model_and_torch_free) ... ok
test_fresh_namespace_existing_directory_and_symlink_refused (__main__.Contracts.test_fresh_namespace_existing_directory_and_symlink_refused) ... ok
test_full_weight_coordinate_quantiles_exceed_torch_limit (__main__.Contracts.test_full_weight_coordinate_quantiles_exceed_torch_limit) ... ok
test_gate_inputs_fsynced_and_reloaded_before_predicate (__main__.Contracts.test_gate_inputs_fsynced_and_reloaded_before_predicate) ... ok
test_interrupted_serialization_is_incomplete_and_retains_previous_values (__main__.Contracts.test_interrupted_serialization_is_incomplete_and_retains_previous_values) ... ok
test_malformed_classification_capture_is_INCONCLUSIVE (__main__.Contracts.test_malformed_classification_capture_is_INCONCLUSIVE) ... ok
test_missing_capture_refuses_instead_of_reimplementing (__main__.Contracts.test_missing_capture_refuses_instead_of_reimplementing) ... ok
test_missing_reference_Q_retains_available_operands_before_coverage_halt (__main__.Contracts.test_missing_reference_Q_retains_available_operands_before_coverage_halt) ... ok
test_native_direct_update_included_in_all_pair_measurements (__main__.Contracts.test_native_direct_update_included_in_all_pair_measurements) ... ok
test_native_factor_actual_matrix_and_Q_are_compared (__main__.Contracts.test_native_factor_actual_matrix_and_Q_are_compared) ... ok
test_native_missing_factor_Q_is_inconclusive_capture_failure (__main__.Contracts.test_native_missing_factor_Q_is_inconclusive_capture_failure) ... ok
test_nonfinite_operand_persisted_before_halt (__main__.Contracts.test_nonfinite_operand_persisted_before_halt) ... ok
test_observer_original_code_coverage_off_on_and_native_operands (__main__.Contracts.test_observer_original_code_coverage_off_on_and_native_operands) ... ok
test_observer_tensor_inertness_catches_discarded_cur_mutation (__main__.Contracts.test_observer_tensor_inertness_catches_discarded_cur_mutation) ... ok
test_packet_tamper_refused_before_downstream_consumption (__main__.Contracts.test_packet_tamper_refused_before_downstream_consumption) ... ok
test_real_shell_supervisor_hanging_stub_preserves_timeout_and_kills_worker (__main__.Contracts.test_real_shell_supervisor_hanging_stub_preserves_timeout_and_kills_worker) ... ok
test_real_shell_supervisor_worker_exit_before_start_is_diagnosed (__main__.Contracts.test_real_shell_supervisor_worker_exit_before_start_is_diagnosed) ... ok
test_realized_native_saved_factors_drive_R_predicate (__main__.Contracts.test_realized_native_saved_factors_drive_R_predicate) ... ok
test_repeat_factor_compared_to_original_native_solution (__main__.Contracts.test_repeat_factor_compared_to_original_native_solution) ... ok
test_restores_optional_recorder_and_preexisting_hook_on_halt (__main__.Contracts.test_restores_optional_recorder_and_preexisting_hook_on_halt) ... ok
test_scope_SHA_drift_refused (__main__.Contracts.test_scope_SHA_drift_refused) ... ok
test_supervisor_timeout_overrides_worker_success_and_preserves_commits (__main__.Contracts.test_supervisor_timeout_overrides_worker_success_and_preserves_commits) ... ok
test_valid_complete_phases_publish_threshold_free_R (__main__.Contracts.test_valid_complete_phases_publish_threshold_free_R) ... ok

----------------------------------------------------------------------
Ran 41 tests in 7.580s

OK
```


### red_setup_timeout.log

```text
test_real_shell_supervisor_setup_timeout_retains_owned_namespace_diagnostic (__main__.Contracts.test_real_shell_supervisor_setup_timeout_retains_owned_namespace_diagnostic) ... FAIL

======================================================================
FAIL: test_real_shell_supervisor_setup_timeout_retains_owned_namespace_diagnostic (__main__.Contracts.test_real_shell_supervisor_setup_timeout_retains_owned_namespace_diagnostic)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 463, in test_real_shell_supervisor_setup_timeout_retains_owned_namespace_diagnostic
    self.run_shell_stub('prepare_hang')
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 482, in run_shell_stub
    self.assertEqual(child.returncode,2,(child.stdout,child.stderr))
AssertionError: 3 != 2 : ('', '/private/tmp/c10y_build/tmpj8c5csq6/tools/run_c10y_precast_diag.sh: line 63: 18012 Killed: 9               "$PY" -B "$DRIVER" --utc "$UTC" --prepare\n')

----------------------------------------------------------------------
Ran 1 test in 4.039s

FAILED (failures=1)
```


### green_release.log

```text
test_INCONCLUSIVE_precedes_every_other_reading (__main__.Contracts.test_INCONCLUSIVE_precedes_every_other_reading) ... ok
test_R_requires_every_cell_and_A7_device_difference (__main__.Contracts.test_R_requires_every_cell_and_A7_device_difference) ... ok
test_S_needs_direct_trace_evidence_and_K_never_emitted (__main__.Contracts.test_S_needs_direct_trace_evidence_and_K_never_emitted) ... ok
test_actual_representation_batch_padding_and_indices_captured_without_id_assumption (__main__.Contracts.test_actual_representation_batch_padding_and_indices_captured_without_id_assumption) ... ok
test_completed_float64_direct_solution_survives_next_solve_failure (__main__.Contracts.test_completed_float64_direct_solution_survives_next_solve_failure) ... ok
test_completed_native_CPU_product_survives_later_control_halt (__main__.Contracts.test_completed_native_CPU_product_survives_later_control_halt) ... ok
test_device_product_observed_from_original_effective_weight (__main__.Contracts.test_device_product_observed_from_original_effective_weight) ... ok
test_difference_metrics_and_weight_coordinate_columns (__main__.Contracts.test_difference_metrics_and_weight_coordinate_columns) ... ok
test_exclusive_JSON_and_tensor_collision_have_no_sibling (__main__.Contracts.test_exclusive_JSON_and_tensor_collision_have_no_sibling) ... ok
test_fail_closed_gpu_and_fingerprint_records_precede_loader (__main__.Contracts.test_fail_closed_gpu_and_fingerprint_records_precede_loader) ... ok
test_finalizer_incomplete_worker_cannot_publish_R (__main__.Contracts.test_finalizer_incomplete_worker_cannot_publish_R) ... ok
test_finalizer_malformed_worker_preserves_exception_and_inconclusive (__main__.Contracts.test_finalizer_malformed_worker_preserves_exception_and_inconclusive) ... ok
test_finalizer_overwrite_refusal_keeps_terminal_bytes (__main__.Contracts.test_finalizer_overwrite_refusal_keeps_terminal_bytes) ... ok
test_finalizer_rejects_completed_claim_with_incomplete_phases (__main__.Contracts.test_finalizer_rejects_completed_claim_with_incomplete_phases) ... ok
test_float64_realization_cannot_demote_to_float32 (__main__.Contracts.test_float64_realization_cannot_demote_to_float32) ... ok
test_float64_realization_casts_on_CPU_before_device_transfer (__main__.Contracts.test_float64_realization_casts_on_CPU_before_device_transfer) ... ok
test_float64_solve_and_promoted_product_are_distinct (__main__.Contracts.test_float64_solve_and_promoted_product_are_distinct) ... ok
test_forced_native_halt_preserves_capture_and_cleans_weights_globals (__main__.Contracts.test_forced_native_halt_preserves_capture_and_cleans_weights_globals) ... ok
test_fresh_import_is_model_and_torch_free (__main__.Contracts.test_fresh_import_is_model_and_torch_free) ... ok
test_fresh_namespace_existing_directory_and_symlink_refused (__main__.Contracts.test_fresh_namespace_existing_directory_and_symlink_refused) ... ok
test_full_weight_coordinate_quantiles_exceed_torch_limit (__main__.Contracts.test_full_weight_coordinate_quantiles_exceed_torch_limit) ... ok
test_gate_inputs_fsynced_and_reloaded_before_predicate (__main__.Contracts.test_gate_inputs_fsynced_and_reloaded_before_predicate) ... ok
test_interrupted_serialization_is_incomplete_and_retains_previous_values (__main__.Contracts.test_interrupted_serialization_is_incomplete_and_retains_previous_values) ... ok
test_malformed_classification_capture_is_INCONCLUSIVE (__main__.Contracts.test_malformed_classification_capture_is_INCONCLUSIVE) ... ok
test_missing_capture_refuses_instead_of_reimplementing (__main__.Contracts.test_missing_capture_refuses_instead_of_reimplementing) ... ok
test_missing_reference_Q_retains_available_operands_before_coverage_halt (__main__.Contracts.test_missing_reference_Q_retains_available_operands_before_coverage_halt) ... ok
test_native_direct_update_included_in_all_pair_measurements (__main__.Contracts.test_native_direct_update_included_in_all_pair_measurements) ... ok
test_native_factor_actual_matrix_and_Q_are_compared (__main__.Contracts.test_native_factor_actual_matrix_and_Q_are_compared) ... ok
test_native_missing_factor_Q_is_inconclusive_capture_failure (__main__.Contracts.test_native_missing_factor_Q_is_inconclusive_capture_failure) ... ok
test_nonfinite_operand_persisted_before_halt (__main__.Contracts.test_nonfinite_operand_persisted_before_halt) ... ok
test_observer_original_code_coverage_off_on_and_native_operands (__main__.Contracts.test_observer_original_code_coverage_off_on_and_native_operands) ... ok
test_observer_tensor_inertness_catches_discarded_cur_mutation (__main__.Contracts.test_observer_tensor_inertness_catches_discarded_cur_mutation) ... ok
test_packet_tamper_refused_before_downstream_consumption (__main__.Contracts.test_packet_tamper_refused_before_downstream_consumption) ... ok
test_real_shell_supervisor_hanging_stub_preserves_timeout_and_kills_worker (__main__.Contracts.test_real_shell_supervisor_hanging_stub_preserves_timeout_and_kills_worker) ... ok
test_real_shell_supervisor_setup_timeout_retains_owned_namespace_diagnostic (__main__.Contracts.test_real_shell_supervisor_setup_timeout_retains_owned_namespace_diagnostic) ... ok
test_real_shell_supervisor_worker_exit_before_start_is_diagnosed (__main__.Contracts.test_real_shell_supervisor_worker_exit_before_start_is_diagnosed) ... ok
test_realized_native_saved_factors_drive_R_predicate (__main__.Contracts.test_realized_native_saved_factors_drive_R_predicate) ... ok
test_repeat_factor_compared_to_original_native_solution (__main__.Contracts.test_repeat_factor_compared_to_original_native_solution) ... ok
test_restores_optional_recorder_and_preexisting_hook_on_halt (__main__.Contracts.test_restores_optional_recorder_and_preexisting_hook_on_halt) ... ok
test_scope_SHA_drift_refused (__main__.Contracts.test_scope_SHA_drift_refused) ... ok
test_supervisor_timeout_overrides_worker_success_and_preserves_commits (__main__.Contracts.test_supervisor_timeout_overrides_worker_success_and_preserves_commits) ... ok
test_valid_complete_phases_publish_threshold_free_R (__main__.Contracts.test_valid_complete_phases_publish_threshold_free_R) ... ok

----------------------------------------------------------------------
Ran 42 tests in 11.850s

OK
```


### red_namespace_shell.log

```text
test_real_shell_existing_namespace_refused_without_finalizer (__main__.Contracts.test_real_shell_existing_namespace_refused_without_finalizer) ... FAIL

======================================================================
FAIL: test_real_shell_existing_namespace_refused_without_finalizer (__main__.Contracts.test_real_shell_existing_namespace_refused_without_finalizer)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 466, in test_real_shell_existing_namespace_refused_without_finalizer
    self.run_shell_stub('existing')
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 488, in run_shell_stub
    self.assertEqual(child.returncode,3,(child.stdout,child.stderr))
AssertionError: 2 != 3 : ('', 'Traceback (most recent call last):\n  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag.py", line 126, in claim_namespace\n    try: out.mkdir()\n         ^^^^^^^^^^^\n  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/pathlib.py", line 1116, in mkdir\n    os.mkdir(self, mode)\nFileExistsError: [Errno 17] File exists: \'/private/tmp/c10y_build/tmpw8rb3w0k/results/c10y_precast_diag/20261009T000000Z\'\n\nThe above exception was the direct cause of the following exception:\n\nTraceback (most recent call last):\n  File "/private/tmp/c10y_build/tmpw8rb3w0k/experiments/track_c/c10y_precast_diag.py", line 7, in <module>\n    D.claim_namespace(root,utc,int(os.environ["C10Y_PRECAST_SUPERVISOR"]))\n  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag.py", line 127, in claim_namespace\n    except FileExistsError as error: raise A.Halt(\'EXISTING-NAMESPACE\',str(out)) from error\n                                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\nc10y_directdw_arms.Halt: EXISTING-NAMESPACE: /private/tmp/c10y_build/tmpw8rb3w0k/results/c10y_precast_diag/20261009T000000Z\n')

----------------------------------------------------------------------
Ran 1 test in 0.395s

FAILED (failures=1)
```


### green_delivery.log

```text
test_INCONCLUSIVE_precedes_every_other_reading (__main__.Contracts.test_INCONCLUSIVE_precedes_every_other_reading) ... ok
test_R_requires_every_cell_and_A7_device_difference (__main__.Contracts.test_R_requires_every_cell_and_A7_device_difference) ... ok
test_S_needs_direct_trace_evidence_and_K_never_emitted (__main__.Contracts.test_S_needs_direct_trace_evidence_and_K_never_emitted) ... ok
test_actual_representation_batch_padding_and_indices_captured_without_id_assumption (__main__.Contracts.test_actual_representation_batch_padding_and_indices_captured_without_id_assumption) ... ok
test_completed_float64_direct_solution_survives_next_solve_failure (__main__.Contracts.test_completed_float64_direct_solution_survives_next_solve_failure) ... ok
test_completed_native_CPU_product_survives_later_control_halt (__main__.Contracts.test_completed_native_CPU_product_survives_later_control_halt) ... ok
test_device_product_observed_from_original_effective_weight (__main__.Contracts.test_device_product_observed_from_original_effective_weight) ... ok
test_difference_metrics_and_weight_coordinate_columns (__main__.Contracts.test_difference_metrics_and_weight_coordinate_columns) ... ok
test_exclusive_JSON_and_tensor_collision_have_no_sibling (__main__.Contracts.test_exclusive_JSON_and_tensor_collision_have_no_sibling) ... ok
test_fail_closed_gpu_and_fingerprint_records_precede_loader (__main__.Contracts.test_fail_closed_gpu_and_fingerprint_records_precede_loader) ... ok
test_finalizer_incomplete_worker_cannot_publish_R (__main__.Contracts.test_finalizer_incomplete_worker_cannot_publish_R) ... ok
test_finalizer_malformed_worker_preserves_exception_and_inconclusive (__main__.Contracts.test_finalizer_malformed_worker_preserves_exception_and_inconclusive) ... ok
test_finalizer_overwrite_refusal_keeps_terminal_bytes (__main__.Contracts.test_finalizer_overwrite_refusal_keeps_terminal_bytes) ... ok
test_finalizer_rejects_completed_claim_with_incomplete_phases (__main__.Contracts.test_finalizer_rejects_completed_claim_with_incomplete_phases) ... ok
test_float64_realization_cannot_demote_to_float32 (__main__.Contracts.test_float64_realization_cannot_demote_to_float32) ... ok
test_float64_realization_casts_on_CPU_before_device_transfer (__main__.Contracts.test_float64_realization_casts_on_CPU_before_device_transfer) ... ok
test_float64_solve_and_promoted_product_are_distinct (__main__.Contracts.test_float64_solve_and_promoted_product_are_distinct) ... ok
test_forced_native_halt_preserves_capture_and_cleans_weights_globals (__main__.Contracts.test_forced_native_halt_preserves_capture_and_cleans_weights_globals) ... ok
test_fresh_import_is_model_and_torch_free (__main__.Contracts.test_fresh_import_is_model_and_torch_free) ... ok
test_fresh_namespace_existing_directory_and_symlink_refused (__main__.Contracts.test_fresh_namespace_existing_directory_and_symlink_refused) ... ok
test_full_weight_coordinate_quantiles_exceed_torch_limit (__main__.Contracts.test_full_weight_coordinate_quantiles_exceed_torch_limit) ... ok
test_gate_inputs_fsynced_and_reloaded_before_predicate (__main__.Contracts.test_gate_inputs_fsynced_and_reloaded_before_predicate) ... ok
test_interrupted_serialization_is_incomplete_and_retains_previous_values (__main__.Contracts.test_interrupted_serialization_is_incomplete_and_retains_previous_values) ... ok
test_malformed_classification_capture_is_INCONCLUSIVE (__main__.Contracts.test_malformed_classification_capture_is_INCONCLUSIVE) ... ok
test_missing_capture_refuses_instead_of_reimplementing (__main__.Contracts.test_missing_capture_refuses_instead_of_reimplementing) ... ok
test_missing_reference_Q_retains_available_operands_before_coverage_halt (__main__.Contracts.test_missing_reference_Q_retains_available_operands_before_coverage_halt) ... ok
test_native_direct_update_included_in_all_pair_measurements (__main__.Contracts.test_native_direct_update_included_in_all_pair_measurements) ... ok
test_native_factor_actual_matrix_and_Q_are_compared (__main__.Contracts.test_native_factor_actual_matrix_and_Q_are_compared) ... ok
test_native_missing_factor_Q_is_inconclusive_capture_failure (__main__.Contracts.test_native_missing_factor_Q_is_inconclusive_capture_failure) ... ok
test_nonfinite_operand_persisted_before_halt (__main__.Contracts.test_nonfinite_operand_persisted_before_halt) ... ok
test_observer_original_code_coverage_off_on_and_native_operands (__main__.Contracts.test_observer_original_code_coverage_off_on_and_native_operands) ... ok
test_observer_tensor_inertness_catches_discarded_cur_mutation (__main__.Contracts.test_observer_tensor_inertness_catches_discarded_cur_mutation) ... ok
test_packet_tamper_refused_before_downstream_consumption (__main__.Contracts.test_packet_tamper_refused_before_downstream_consumption) ... ok
test_real_shell_existing_namespace_refused_without_finalizer (__main__.Contracts.test_real_shell_existing_namespace_refused_without_finalizer) ... ok
test_real_shell_supervisor_hanging_stub_preserves_timeout_and_kills_worker (__main__.Contracts.test_real_shell_supervisor_hanging_stub_preserves_timeout_and_kills_worker) ... ok
test_real_shell_supervisor_setup_timeout_retains_owned_namespace_diagnostic (__main__.Contracts.test_real_shell_supervisor_setup_timeout_retains_owned_namespace_diagnostic) ... ok
test_real_shell_supervisor_worker_exit_before_start_is_diagnosed (__main__.Contracts.test_real_shell_supervisor_worker_exit_before_start_is_diagnosed) ... ok
test_realized_native_saved_factors_drive_R_predicate (__main__.Contracts.test_realized_native_saved_factors_drive_R_predicate) ... ok
test_repeat_factor_compared_to_original_native_solution (__main__.Contracts.test_repeat_factor_compared_to_original_native_solution) ... ok
test_restores_optional_recorder_and_preexisting_hook_on_halt (__main__.Contracts.test_restores_optional_recorder_and_preexisting_hook_on_halt) ... ok
test_scope_SHA_drift_refused (__main__.Contracts.test_scope_SHA_drift_refused) ... ok
test_supervisor_timeout_overrides_worker_success_and_preserves_commits (__main__.Contracts.test_supervisor_timeout_overrides_worker_success_and_preserves_commits) ... ok
test_valid_complete_phases_publish_threshold_free_R (__main__.Contracts.test_valid_complete_phases_publish_threshold_free_R) ... ok

----------------------------------------------------------------------
Ran 43 tests in 11.878s

OK
```


### red_finalizer_timeout.log

```text
test_real_shell_finalizer_timeout_has_fresh_supervisor_diagnostic (__main__.Contracts.test_real_shell_finalizer_timeout_has_fresh_supervisor_diagnostic) ... ERROR
test_timeout_publication_preserves_previous_bytes_and_has_terminal_INCONCLUSIVE (__main__.Contracts.test_timeout_publication_preserves_previous_bytes_and_has_terminal_INCONCLUSIVE) ... FAIL

======================================================================
ERROR: test_real_shell_finalizer_timeout_has_fresh_supervisor_diagnostic (__main__.Contracts.test_real_shell_finalizer_timeout_has_fresh_supervisor_diagnostic)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 469, in test_real_shell_finalizer_timeout_has_fresh_supervisor_diagnostic
    self.run_shell_stub('finalizer_hang')
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 509, in run_shell_stub
    run=json.loads((out/'run.json').read_text());self.assertEqual(run['status'],'INCONCLUSIVE')
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/pathlib.py", line 1058, in read_text
    with self.open(mode='r', encoding=encoding, errors=errors) as f:
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/pathlib.py", line 1044, in open
    return io.open(self, mode, buffering, encoding, errors, newline)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
FileNotFoundError: [Errno 2] No such file or directory: '/private/tmp/c10y_build/tmpet9p6jyg/results/c10y_precast_diag/20261009T000000Z/run.json'

======================================================================
FAIL: test_timeout_publication_preserves_previous_bytes_and_has_terminal_INCONCLUSIVE (__main__.Contracts.test_timeout_publication_preserves_previous_bytes_and_has_terminal_INCONCLUSIVE)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 474, in test_timeout_publication_preserves_previous_bytes_and_has_terminal_INCONCLUSIVE
    self.assertTrue(hasattr(D,'timeout_terminal'),'missing supervisor publication-timeout writer')
AssertionError: False is not true : missing supervisor publication-timeout writer

----------------------------------------------------------------------
Ran 2 tests in 4.040s

FAILED (failures=1, errors=1)
```


### green_acceptance.log

```text
test_INCONCLUSIVE_precedes_every_other_reading (__main__.Contracts.test_INCONCLUSIVE_precedes_every_other_reading) ... ok
test_R_requires_every_cell_and_A7_device_difference (__main__.Contracts.test_R_requires_every_cell_and_A7_device_difference) ... ok
test_S_needs_direct_trace_evidence_and_K_never_emitted (__main__.Contracts.test_S_needs_direct_trace_evidence_and_K_never_emitted) ... ok
test_actual_representation_batch_padding_and_indices_captured_without_id_assumption (__main__.Contracts.test_actual_representation_batch_padding_and_indices_captured_without_id_assumption) ... ok
test_completed_float64_direct_solution_survives_next_solve_failure (__main__.Contracts.test_completed_float64_direct_solution_survives_next_solve_failure) ... ok
test_completed_native_CPU_product_survives_later_control_halt (__main__.Contracts.test_completed_native_CPU_product_survives_later_control_halt) ... ok
test_device_product_observed_from_original_effective_weight (__main__.Contracts.test_device_product_observed_from_original_effective_weight) ... ok
test_difference_metrics_and_weight_coordinate_columns (__main__.Contracts.test_difference_metrics_and_weight_coordinate_columns) ... ok
test_exclusive_JSON_and_tensor_collision_have_no_sibling (__main__.Contracts.test_exclusive_JSON_and_tensor_collision_have_no_sibling) ... ok
test_fail_closed_gpu_and_fingerprint_records_precede_loader (__main__.Contracts.test_fail_closed_gpu_and_fingerprint_records_precede_loader) ... ok
test_finalizer_incomplete_worker_cannot_publish_R (__main__.Contracts.test_finalizer_incomplete_worker_cannot_publish_R) ... ok
test_finalizer_malformed_worker_preserves_exception_and_inconclusive (__main__.Contracts.test_finalizer_malformed_worker_preserves_exception_and_inconclusive) ... ok
test_finalizer_overwrite_refusal_keeps_terminal_bytes (__main__.Contracts.test_finalizer_overwrite_refusal_keeps_terminal_bytes) ... ok
test_finalizer_rejects_completed_claim_with_incomplete_phases (__main__.Contracts.test_finalizer_rejects_completed_claim_with_incomplete_phases) ... ok
test_float64_realization_cannot_demote_to_float32 (__main__.Contracts.test_float64_realization_cannot_demote_to_float32) ... ok
test_float64_realization_casts_on_CPU_before_device_transfer (__main__.Contracts.test_float64_realization_casts_on_CPU_before_device_transfer) ... ok
test_float64_solve_and_promoted_product_are_distinct (__main__.Contracts.test_float64_solve_and_promoted_product_are_distinct) ... ok
test_forced_native_halt_preserves_capture_and_cleans_weights_globals (__main__.Contracts.test_forced_native_halt_preserves_capture_and_cleans_weights_globals) ... ok
test_fresh_import_is_model_and_torch_free (__main__.Contracts.test_fresh_import_is_model_and_torch_free) ... ok
test_fresh_namespace_existing_directory_and_symlink_refused (__main__.Contracts.test_fresh_namespace_existing_directory_and_symlink_refused) ... ok
test_full_weight_coordinate_quantiles_exceed_torch_limit (__main__.Contracts.test_full_weight_coordinate_quantiles_exceed_torch_limit) ... ok
test_gate_inputs_fsynced_and_reloaded_before_predicate (__main__.Contracts.test_gate_inputs_fsynced_and_reloaded_before_predicate) ... ok
test_interrupted_serialization_is_incomplete_and_retains_previous_values (__main__.Contracts.test_interrupted_serialization_is_incomplete_and_retains_previous_values) ... ok
test_malformed_classification_capture_is_INCONCLUSIVE (__main__.Contracts.test_malformed_classification_capture_is_INCONCLUSIVE) ... ok
test_missing_capture_refuses_instead_of_reimplementing (__main__.Contracts.test_missing_capture_refuses_instead_of_reimplementing) ... ok
test_missing_reference_Q_retains_available_operands_before_coverage_halt (__main__.Contracts.test_missing_reference_Q_retains_available_operands_before_coverage_halt) ... ok
test_native_direct_update_included_in_all_pair_measurements (__main__.Contracts.test_native_direct_update_included_in_all_pair_measurements) ... ok
test_native_factor_actual_matrix_and_Q_are_compared (__main__.Contracts.test_native_factor_actual_matrix_and_Q_are_compared) ... ok
test_native_missing_factor_Q_is_inconclusive_capture_failure (__main__.Contracts.test_native_missing_factor_Q_is_inconclusive_capture_failure) ... ok
test_nonfinite_operand_persisted_before_halt (__main__.Contracts.test_nonfinite_operand_persisted_before_halt) ... ok
test_observer_original_code_coverage_off_on_and_native_operands (__main__.Contracts.test_observer_original_code_coverage_off_on_and_native_operands) ... ok
test_observer_tensor_inertness_catches_discarded_cur_mutation (__main__.Contracts.test_observer_tensor_inertness_catches_discarded_cur_mutation) ... ok
test_packet_tamper_refused_before_downstream_consumption (__main__.Contracts.test_packet_tamper_refused_before_downstream_consumption) ... ok
test_real_shell_existing_namespace_refused_without_finalizer (__main__.Contracts.test_real_shell_existing_namespace_refused_without_finalizer) ... ok
test_real_shell_finalizer_timeout_has_fresh_supervisor_diagnostic (__main__.Contracts.test_real_shell_finalizer_timeout_has_fresh_supervisor_diagnostic) ... ok
test_real_shell_supervisor_hanging_stub_preserves_timeout_and_kills_worker (__main__.Contracts.test_real_shell_supervisor_hanging_stub_preserves_timeout_and_kills_worker) ... ok
test_real_shell_supervisor_setup_timeout_retains_owned_namespace_diagnostic (__main__.Contracts.test_real_shell_supervisor_setup_timeout_retains_owned_namespace_diagnostic) ... ok
test_real_shell_supervisor_worker_exit_before_start_is_diagnosed (__main__.Contracts.test_real_shell_supervisor_worker_exit_before_start_is_diagnosed) ... ok
test_realized_native_saved_factors_drive_R_predicate (__main__.Contracts.test_realized_native_saved_factors_drive_R_predicate) ... ok
test_repeat_factor_compared_to_original_native_solution (__main__.Contracts.test_repeat_factor_compared_to_original_native_solution) ... ok
test_restores_optional_recorder_and_preexisting_hook_on_halt (__main__.Contracts.test_restores_optional_recorder_and_preexisting_hook_on_halt) ... ok
test_scope_SHA_drift_refused (__main__.Contracts.test_scope_SHA_drift_refused) ... ok
test_supervisor_timeout_overrides_worker_success_and_preserves_commits (__main__.Contracts.test_supervisor_timeout_overrides_worker_success_and_preserves_commits) ... ok
test_timeout_publication_preserves_previous_bytes_and_has_terminal_INCONCLUSIVE (__main__.Contracts.test_timeout_publication_preserves_previous_bytes_and_has_terminal_INCONCLUSIVE) ... ok
test_valid_complete_phases_publish_threshold_free_R (__main__.Contracts.test_valid_complete_phases_publish_threshold_free_R) ... ok

----------------------------------------------------------------------
Ran 45 tests in 18.114s

OK
```


### red_targets.log

```text
test_48_targets_computed_once_saved_reloaded_and_shared_by_original_paths (__main__.Contracts.test_48_targets_computed_once_saved_reloaded_and_shared_by_original_paths) ... FAIL
test_target_failure_retains_completed_prefix_and_NOT_RUN_arm (__main__.Contracts.test_target_failure_retains_completed_prefix_and_NOT_RUN_arm) ... FAIL
test_target_mutation_halt_retains_offending_value_and_restores_weights (__main__.Contracts.test_target_mutation_halt_retains_offending_value_and_restores_weights) ... FAIL

======================================================================
FAIL: test_48_targets_computed_once_saved_reloaded_and_shared_by_original_paths (__main__.Contracts.test_48_targets_computed_once_saved_reloaded_and_shared_by_original_paths)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 457, in test_48_targets_computed_once_saved_reloaded_and_shared_by_original_paths
    self.assertTrue(hasattr(D,'compute_targets'),'missing isolated target persistence boundary')
AssertionError: False is not true : missing isolated target persistence boundary

======================================================================
FAIL: test_target_failure_retains_completed_prefix_and_NOT_RUN_arm (__main__.Contracts.test_target_failure_retains_completed_prefix_and_NOT_RUN_arm)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 476, in test_target_failure_retains_completed_prefix_and_NOT_RUN_arm
    self.assertTrue(hasattr(D,'compute_targets'),'missing isolated target persistence boundary')
AssertionError: False is not true : missing isolated target persistence boundary

======================================================================
FAIL: test_target_mutation_halt_retains_offending_value_and_restores_weights (__main__.Contracts.test_target_mutation_halt_retains_offending_value_and_restores_weights)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 494, in test_target_mutation_halt_retains_offending_value_and_restores_weights
    self.assertTrue(hasattr(D,'compute_targets'),'missing isolated target persistence boundary')
AssertionError: False is not true : missing isolated target persistence boundary

----------------------------------------------------------------------
Ran 3 tests in 0.002s

FAILED (failures=3)
```


### green_final_48.log

```text
test_48_targets_computed_once_saved_reloaded_and_shared_by_original_paths (__main__.Contracts.test_48_targets_computed_once_saved_reloaded_and_shared_by_original_paths) ... ok
test_INCONCLUSIVE_precedes_every_other_reading (__main__.Contracts.test_INCONCLUSIVE_precedes_every_other_reading) ... ok
test_R_requires_every_cell_and_A7_device_difference (__main__.Contracts.test_R_requires_every_cell_and_A7_device_difference) ... ok
test_S_needs_direct_trace_evidence_and_K_never_emitted (__main__.Contracts.test_S_needs_direct_trace_evidence_and_K_never_emitted) ... ok
test_actual_representation_batch_padding_and_indices_captured_without_id_assumption (__main__.Contracts.test_actual_representation_batch_padding_and_indices_captured_without_id_assumption) ... ok
test_completed_float64_direct_solution_survives_next_solve_failure (__main__.Contracts.test_completed_float64_direct_solution_survives_next_solve_failure) ... ok
test_completed_native_CPU_product_survives_later_control_halt (__main__.Contracts.test_completed_native_CPU_product_survives_later_control_halt) ... ok
test_device_product_observed_from_original_effective_weight (__main__.Contracts.test_device_product_observed_from_original_effective_weight) ... ok
test_difference_metrics_and_weight_coordinate_columns (__main__.Contracts.test_difference_metrics_and_weight_coordinate_columns) ... ok
test_exclusive_JSON_and_tensor_collision_have_no_sibling (__main__.Contracts.test_exclusive_JSON_and_tensor_collision_have_no_sibling) ... ok
test_fail_closed_gpu_and_fingerprint_records_precede_loader (__main__.Contracts.test_fail_closed_gpu_and_fingerprint_records_precede_loader) ... ok
test_finalizer_incomplete_worker_cannot_publish_R (__main__.Contracts.test_finalizer_incomplete_worker_cannot_publish_R) ... ok
test_finalizer_malformed_worker_preserves_exception_and_inconclusive (__main__.Contracts.test_finalizer_malformed_worker_preserves_exception_and_inconclusive) ... ok
test_finalizer_overwrite_refusal_keeps_terminal_bytes (__main__.Contracts.test_finalizer_overwrite_refusal_keeps_terminal_bytes) ... ok
test_finalizer_rejects_completed_claim_with_incomplete_phases (__main__.Contracts.test_finalizer_rejects_completed_claim_with_incomplete_phases) ... ok
test_float64_realization_cannot_demote_to_float32 (__main__.Contracts.test_float64_realization_cannot_demote_to_float32) ... ok
test_float64_realization_casts_on_CPU_before_device_transfer (__main__.Contracts.test_float64_realization_casts_on_CPU_before_device_transfer) ... ok
test_float64_solve_and_promoted_product_are_distinct (__main__.Contracts.test_float64_solve_and_promoted_product_are_distinct) ... ok
test_forced_native_halt_preserves_capture_and_cleans_weights_globals (__main__.Contracts.test_forced_native_halt_preserves_capture_and_cleans_weights_globals) ... ok
test_fresh_import_is_model_and_torch_free (__main__.Contracts.test_fresh_import_is_model_and_torch_free) ... ok
test_fresh_namespace_existing_directory_and_symlink_refused (__main__.Contracts.test_fresh_namespace_existing_directory_and_symlink_refused) ... ok
test_full_weight_coordinate_quantiles_exceed_torch_limit (__main__.Contracts.test_full_weight_coordinate_quantiles_exceed_torch_limit) ... ok
test_gate_inputs_fsynced_and_reloaded_before_predicate (__main__.Contracts.test_gate_inputs_fsynced_and_reloaded_before_predicate) ... ok
test_interrupted_serialization_is_incomplete_and_retains_previous_values (__main__.Contracts.test_interrupted_serialization_is_incomplete_and_retains_previous_values) ... ok
test_malformed_classification_capture_is_INCONCLUSIVE (__main__.Contracts.test_malformed_classification_capture_is_INCONCLUSIVE) ... ok
test_missing_capture_refuses_instead_of_reimplementing (__main__.Contracts.test_missing_capture_refuses_instead_of_reimplementing) ... ok
test_missing_reference_Q_retains_available_operands_before_coverage_halt (__main__.Contracts.test_missing_reference_Q_retains_available_operands_before_coverage_halt) ... ok
test_native_direct_update_included_in_all_pair_measurements (__main__.Contracts.test_native_direct_update_included_in_all_pair_measurements) ... ok
test_native_factor_actual_matrix_and_Q_are_compared (__main__.Contracts.test_native_factor_actual_matrix_and_Q_are_compared) ... ok
test_native_missing_factor_Q_is_inconclusive_capture_failure (__main__.Contracts.test_native_missing_factor_Q_is_inconclusive_capture_failure) ... ok
test_nonfinite_operand_persisted_before_halt (__main__.Contracts.test_nonfinite_operand_persisted_before_halt) ... ok
test_observer_original_code_coverage_off_on_and_native_operands (__main__.Contracts.test_observer_original_code_coverage_off_on_and_native_operands) ... ok
test_observer_tensor_inertness_catches_discarded_cur_mutation (__main__.Contracts.test_observer_tensor_inertness_catches_discarded_cur_mutation) ... ok
test_packet_tamper_refused_before_downstream_consumption (__main__.Contracts.test_packet_tamper_refused_before_downstream_consumption) ... ok
test_real_shell_existing_namespace_refused_without_finalizer (__main__.Contracts.test_real_shell_existing_namespace_refused_without_finalizer) ... ok
test_real_shell_finalizer_timeout_has_fresh_supervisor_diagnostic (__main__.Contracts.test_real_shell_finalizer_timeout_has_fresh_supervisor_diagnostic) ... ok
test_real_shell_supervisor_hanging_stub_preserves_timeout_and_kills_worker (__main__.Contracts.test_real_shell_supervisor_hanging_stub_preserves_timeout_and_kills_worker) ... ok
test_real_shell_supervisor_setup_timeout_retains_owned_namespace_diagnostic (__main__.Contracts.test_real_shell_supervisor_setup_timeout_retains_owned_namespace_diagnostic) ... ok
test_real_shell_supervisor_worker_exit_before_start_is_diagnosed (__main__.Contracts.test_real_shell_supervisor_worker_exit_before_start_is_diagnosed) ... ok
test_realized_native_saved_factors_drive_R_predicate (__main__.Contracts.test_realized_native_saved_factors_drive_R_predicate) ... ok
test_repeat_factor_compared_to_original_native_solution (__main__.Contracts.test_repeat_factor_compared_to_original_native_solution) ... ok
test_restores_optional_recorder_and_preexisting_hook_on_halt (__main__.Contracts.test_restores_optional_recorder_and_preexisting_hook_on_halt) ... ok
test_scope_SHA_drift_refused (__main__.Contracts.test_scope_SHA_drift_refused) ... ok
test_supervisor_timeout_overrides_worker_success_and_preserves_commits (__main__.Contracts.test_supervisor_timeout_overrides_worker_success_and_preserves_commits) ... ok
test_target_failure_retains_completed_prefix_and_NOT_RUN_arm (__main__.Contracts.test_target_failure_retains_completed_prefix_and_NOT_RUN_arm) ... ok
test_target_mutation_halt_retains_offending_value_and_restores_weights (__main__.Contracts.test_target_mutation_halt_retains_offending_value_and_restores_weights) ... ok
test_timeout_publication_preserves_previous_bytes_and_has_terminal_INCONCLUSIVE (__main__.Contracts.test_timeout_publication_preserves_previous_bytes_and_has_terminal_INCONCLUSIVE) ... ok
test_valid_complete_phases_publish_threshold_free_R (__main__.Contracts.test_valid_complete_phases_publish_threshold_free_R) ... ok

----------------------------------------------------------------------
Ran 48 tests in 19.963s

OK
```


### red_log_collision.log

```text
test_real_shell_worker_log_collision_refused_without_overwrite (__main__.Contracts.test_real_shell_worker_log_collision_refused_without_overwrite) ... FAIL

======================================================================
FAIL: test_real_shell_worker_log_collision_refused_without_overwrite (__main__.Contracts.test_real_shell_worker_log_collision_refused_without_overwrite)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 528, in test_real_shell_worker_log_collision_refused_without_overwrite
    self.run_shell_stub('log_collision')
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 582, in run_shell_stub
    if mode=='log_collision':self.assertEqual((out/'worker.log').read_bytes(),b'preexisting-log')
                             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: b'' != b'preexisting-log'

----------------------------------------------------------------------
Ran 1 test in 0.642s

FAILED (failures=1)
```


### green_final_49.log

```text
test_48_targets_computed_once_saved_reloaded_and_shared_by_original_paths (__main__.Contracts.test_48_targets_computed_once_saved_reloaded_and_shared_by_original_paths) ... ok
test_INCONCLUSIVE_precedes_every_other_reading (__main__.Contracts.test_INCONCLUSIVE_precedes_every_other_reading) ... ok
test_R_requires_every_cell_and_A7_device_difference (__main__.Contracts.test_R_requires_every_cell_and_A7_device_difference) ... ok
test_S_needs_direct_trace_evidence_and_K_never_emitted (__main__.Contracts.test_S_needs_direct_trace_evidence_and_K_never_emitted) ... ok
test_actual_representation_batch_padding_and_indices_captured_without_id_assumption (__main__.Contracts.test_actual_representation_batch_padding_and_indices_captured_without_id_assumption) ... ok
test_completed_float64_direct_solution_survives_next_solve_failure (__main__.Contracts.test_completed_float64_direct_solution_survives_next_solve_failure) ... ok
test_completed_native_CPU_product_survives_later_control_halt (__main__.Contracts.test_completed_native_CPU_product_survives_later_control_halt) ... ok
test_device_product_observed_from_original_effective_weight (__main__.Contracts.test_device_product_observed_from_original_effective_weight) ... ok
test_difference_metrics_and_weight_coordinate_columns (__main__.Contracts.test_difference_metrics_and_weight_coordinate_columns) ... ok
test_exclusive_JSON_and_tensor_collision_have_no_sibling (__main__.Contracts.test_exclusive_JSON_and_tensor_collision_have_no_sibling) ... ok
test_fail_closed_gpu_and_fingerprint_records_precede_loader (__main__.Contracts.test_fail_closed_gpu_and_fingerprint_records_precede_loader) ... ok
test_finalizer_incomplete_worker_cannot_publish_R (__main__.Contracts.test_finalizer_incomplete_worker_cannot_publish_R) ... ok
test_finalizer_malformed_worker_preserves_exception_and_inconclusive (__main__.Contracts.test_finalizer_malformed_worker_preserves_exception_and_inconclusive) ... ok
test_finalizer_overwrite_refusal_keeps_terminal_bytes (__main__.Contracts.test_finalizer_overwrite_refusal_keeps_terminal_bytes) ... ok
test_finalizer_rejects_completed_claim_with_incomplete_phases (__main__.Contracts.test_finalizer_rejects_completed_claim_with_incomplete_phases) ... ok
test_float64_realization_cannot_demote_to_float32 (__main__.Contracts.test_float64_realization_cannot_demote_to_float32) ... ok
test_float64_realization_casts_on_CPU_before_device_transfer (__main__.Contracts.test_float64_realization_casts_on_CPU_before_device_transfer) ... ok
test_float64_solve_and_promoted_product_are_distinct (__main__.Contracts.test_float64_solve_and_promoted_product_are_distinct) ... ok
test_forced_native_halt_preserves_capture_and_cleans_weights_globals (__main__.Contracts.test_forced_native_halt_preserves_capture_and_cleans_weights_globals) ... ok
test_fresh_import_is_model_and_torch_free (__main__.Contracts.test_fresh_import_is_model_and_torch_free) ... ok
test_fresh_namespace_existing_directory_and_symlink_refused (__main__.Contracts.test_fresh_namespace_existing_directory_and_symlink_refused) ... ok
test_full_weight_coordinate_quantiles_exceed_torch_limit (__main__.Contracts.test_full_weight_coordinate_quantiles_exceed_torch_limit) ... ok
test_gate_inputs_fsynced_and_reloaded_before_predicate (__main__.Contracts.test_gate_inputs_fsynced_and_reloaded_before_predicate) ... ok
test_interrupted_serialization_is_incomplete_and_retains_previous_values (__main__.Contracts.test_interrupted_serialization_is_incomplete_and_retains_previous_values) ... ok
test_malformed_classification_capture_is_INCONCLUSIVE (__main__.Contracts.test_malformed_classification_capture_is_INCONCLUSIVE) ... ok
test_missing_capture_refuses_instead_of_reimplementing (__main__.Contracts.test_missing_capture_refuses_instead_of_reimplementing) ... ok
test_missing_reference_Q_retains_available_operands_before_coverage_halt (__main__.Contracts.test_missing_reference_Q_retains_available_operands_before_coverage_halt) ... ok
test_native_direct_update_included_in_all_pair_measurements (__main__.Contracts.test_native_direct_update_included_in_all_pair_measurements) ... ok
test_native_factor_actual_matrix_and_Q_are_compared (__main__.Contracts.test_native_factor_actual_matrix_and_Q_are_compared) ... ok
test_native_missing_factor_Q_is_inconclusive_capture_failure (__main__.Contracts.test_native_missing_factor_Q_is_inconclusive_capture_failure) ... ok
test_nonfinite_operand_persisted_before_halt (__main__.Contracts.test_nonfinite_operand_persisted_before_halt) ... ok
test_observer_original_code_coverage_off_on_and_native_operands (__main__.Contracts.test_observer_original_code_coverage_off_on_and_native_operands) ... ok
test_observer_tensor_inertness_catches_discarded_cur_mutation (__main__.Contracts.test_observer_tensor_inertness_catches_discarded_cur_mutation) ... ok
test_packet_tamper_refused_before_downstream_consumption (__main__.Contracts.test_packet_tamper_refused_before_downstream_consumption) ... ok
test_real_shell_existing_namespace_refused_without_finalizer (__main__.Contracts.test_real_shell_existing_namespace_refused_without_finalizer) ... ok
test_real_shell_finalizer_timeout_has_fresh_supervisor_diagnostic (__main__.Contracts.test_real_shell_finalizer_timeout_has_fresh_supervisor_diagnostic) ... ok
test_real_shell_supervisor_hanging_stub_preserves_timeout_and_kills_worker (__main__.Contracts.test_real_shell_supervisor_hanging_stub_preserves_timeout_and_kills_worker) ... ok
test_real_shell_supervisor_setup_timeout_retains_owned_namespace_diagnostic (__main__.Contracts.test_real_shell_supervisor_setup_timeout_retains_owned_namespace_diagnostic) ... ok
test_real_shell_supervisor_worker_exit_before_start_is_diagnosed (__main__.Contracts.test_real_shell_supervisor_worker_exit_before_start_is_diagnosed) ... ok
test_real_shell_worker_log_collision_refused_without_overwrite (__main__.Contracts.test_real_shell_worker_log_collision_refused_without_overwrite) ... ok
test_realized_native_saved_factors_drive_R_predicate (__main__.Contracts.test_realized_native_saved_factors_drive_R_predicate) ... ok
test_repeat_factor_compared_to_original_native_solution (__main__.Contracts.test_repeat_factor_compared_to_original_native_solution) ... ok
test_restores_optional_recorder_and_preexisting_hook_on_halt (__main__.Contracts.test_restores_optional_recorder_and_preexisting_hook_on_halt) ... ok
test_scope_SHA_drift_refused (__main__.Contracts.test_scope_SHA_drift_refused) ... ok
test_supervisor_timeout_overrides_worker_success_and_preserves_commits (__main__.Contracts.test_supervisor_timeout_overrides_worker_success_and_preserves_commits) ... ok
test_target_failure_retains_completed_prefix_and_NOT_RUN_arm (__main__.Contracts.test_target_failure_retains_completed_prefix_and_NOT_RUN_arm) ... ok
test_target_mutation_halt_retains_offending_value_and_restores_weights (__main__.Contracts.test_target_mutation_halt_retains_offending_value_and_restores_weights) ... ok
test_timeout_publication_preserves_previous_bytes_and_has_terminal_INCONCLUSIVE (__main__.Contracts.test_timeout_publication_preserves_previous_bytes_and_has_terminal_INCONCLUSIVE) ... ok
test_valid_complete_phases_publish_threshold_free_R (__main__.Contracts.test_valid_complete_phases_publish_threshold_free_R) ... ok

----------------------------------------------------------------------
Ran 49 tests in 17.146s

OK
```


## Closeout

C10Y PRECAST BUILD DONE. 334 CPU tests passed (49 new + 285 existing); diagnostic NOT-RUN. C10Y frozen source and calibration bytes preserved; concurrent runbook/checkpoint drift is recorded separately. Scope-mandated implementation review/live admission remains GATED. No result or this build report authorizes corrective science execution.


## Fix round 1 — 2026-10-09

Appended at 2026-10-09T19:32:53.442098+00:00. Builder: Codex Y2. One CPU fix round responding to MAESTRO and GPT-6-Astra high's `precast_impl_astra_r1.md` (FIX-FIRST, three BLOCKING). **65/65 diagnostic + 285/285 existing C10Y tests PASS: 350 total, no failures, errors or skips in the final suites.** No GPU/MPS, model load, production diagnostic invocation, science launch or commit occurred. The original report is preserved as history; this section supersedes its implementation-specific test counts, source line references and code SHAs. Implementation re-review remains required.

**Current launch status: GATED on a source-pin mismatch.** `experiments/track_c/c10z_astra_benchmark.py` currently hashes to `3703d8b9c363bb06eab0ca66f38f4b01114363ae75a9d0397701e75aa2520041`, while the preserved diagnostic pin is `9b25a207f630fbfa0d60c80a74f22289ad3bb2cc160d0fc72d7e0367f9a47a1a`. Twelve of thirteen pins match. The read-only diff shows an addition to that program's CLI main (`import c10z_astra_read as R; R.require_a1_freeze(ROOT)`). This builder did not edit that dependency or repin it. Inference from the observed hashes and the existing `worker` setup gate at `c10y_precast_diag.py:628`: the present worktree would halt SOURCE-IDENTITY before model load. That gate was not bypassed, and no production invocation was used to test it. This is separate from the three fixed implementation blockers.

### Requirement → test → implementation

| Requirement / review item | CPU evidence in final diagnostic suite | Implementation |
|---|---|---|
| B1: completed native K/cur/residual/P/C/M/RHS retained before direct solve, both original paths | `test_native_direct_solve_failure_retains_inputs_and_original_exception`; `test_actual_native_solve_inputs_are_fsynced_before_execution` | `NativeObserver.trace` at the AST-derived original solve line; `direct_fields` and `retain`; exclusive `solve_inputs_<arm>_L<l>_<A|Y>_direct.{json,pt}` |
| B1: actual factor M and inline Q retained before factor solve | `test_native_factor_solve_failure_retains_inputs_and_original_exception`; fsync callback test | Original `factor_solve` code object and actual dispatched `p @ k` result; `NativeObserver.mm` persists `solve_inputs_<arm>_L<l>_Y_factor.{json,pt}` with M/RHS and factor operands |
| B1: original exception, available locals, incomplete phase, restoration | Both solve-failure tests assert the identical exception object, retained exception detail/type/matrix, pristine weights, override counter and cleared trace; existing forced-halt/recorder restoration tests | `NativeObserver.failed`, exceptional return handling, `Journal.phase`, existing `restored`; exceptional return never unpacks None or fabricates successful factors |
| B1: secondary failure-record error cannot replace primary exception | `test_phase_failure_publication_preserves_original_exception` | `Journal.phase` adds the secondary publication error as an exception note; its durable started record remains INCOMPLETE |
| B1: later observer-off failure retains earlier actual captures | `test_observer_off_failure_retains_prior_native_input_capture` | `native_capture` runs the observed original path first, restores, then the unobserved control; off/on identities and original functions remain the validation inputs |
| B1/B2: actual solve-input bytes and file/directory fsync completed at entry | `test_actual_native_solve_inputs_are_fsynced_before_execution`: 30 original solve callbacks (15 observed + 15 unobserved controls), exact M/RHS and file/directory inode fsync evidence | `retain` → existing recordfix encoder/exclusive binary + JSON writers → directory fsync; `solve_event` validates actual ATen solve arguments against the pre-solve byte snapshot |
| B2: identity through observation, execution and return, including factor M/Q | `test_native_factor_actual_matrix_and_Q_are_compared`; `test_observer_factor_Q_copy_mutation_invalidates_evidence`; `test_observer_direct_M_mutation_at_return_invalidates_evidence` | `check_inputs`, `check_q`, actual solve dispatch before/after checkpoints, shape/factor return checkpoints; changed bytes halt OBSERVER-SOLVE-INPUT |
| B2: observer-induced corruption gives INCONCLUSIVE, never S | Changed factor-M fixture exercises both arms, retains INCOMPLETE, restores, then finalizes invalid observer evidence as INCONCLUSIVE; ordered-classifier tests | Observer HALT cannot return `observer_validated=True`; worker requirements remain false and finalizer rejects incomplete capture; classifier order unchanged |
| B2: genuine native discrepancy remains valid S evidence | `test_genuine_native_operand_discrepancy_remains_valid_S_evidence`: all ten cells, stable off/on native key discrepancy | Genuine CPU leaf K difference precedes capture and is identical off/on; original native paths and saved packet comparison directly establish the discrepancy; no distance threshold |
| B3: TERM/INT/HUP cleanup and fresh terminal authority | `test_real_shell_supervisor_TERM_cleans_owned_worker_and_publishes_INCONCLUSIVE`, corresponding INT/HUP tests | Shell signal traps → EXIT `closeout` → bounded group TERM/KILL + direct-child wait → model-free `--interrupted`; `interrupted_terminal` publishes fresh INCONCLUSIVE |
| B3: abnormal supervisor/finalizer exits | `test_real_shell_supervisor_abnormal_exit_cleans_owned_worker_and_publishes_INCONCLUSIVE`; `test_real_shell_finalizer_abnormal_exit_has_fresh_INCONCLUSIVE_diagnostic` | EXIT status saved before cleanup; unfinished publication uses ABNORMAL_EXIT; `FINALIZED` requires a completed terminal record and expected writer return code |
| B3: process group can outlive leader | `test_real_shell_owned_process_group_is_stopped_after_leader_exit`: TERM-ignoring descendant, stopped heartbeat, descendant PID gone | `stop_owned` checks the negative worker group independently of its leader; direct children are reaped; group/PID signals are not duplicated for a live group leader |
| B3: deadline armed until cleanup/publication ends; timeout recovery | All interruption stubs verify timer PID alive during terminal publication; `test_real_shell_interrupted_publisher_timeout_remains_armed_and_is_diagnosed`; existing setup/worker/finalizer timeout tests | 2,820 s external timer armed before Python imports; cleanup uses 2 s TERM grace then KILL/wait; hanging interruption publisher is killed and a fresh timeout authority published; `finish_timer` is last cleanup action |
| B3: preserve previous S/R bytes; exclusive terminal writes | `test_interrupted_publication_preserves_prior_bytes_and_is_fresh_INCONCLUSIVE`; existing timeout/overwrite tests | New `supervisor_interruption.json`, `interrupted_reading_inputs.json`, and fresh reading/run names; prior publication SHA references; collisions raise EXISTING-ARTIFACT |
| Refused namespace cannot enter publication/cleanup ownership | `test_real_shell_existing_namespace_refused_without_finalizer`; worker-log collision regression | `PREPARE_STARTED=0` until the early namespace check passes; existing namespace exits 3 before imports; output owner is independently checked by original CLI |
| Frozen scope, classifier and existing C10Y behavior preserved | Scope SHA, ordered classifier, fp64 controls, original-code coverage, forced-halt, interrupted serialization and restoration regressions; all 285 existing C10Y tests | No engine/harness/prereg/scope edits; original math/solve/merge functions called; Journal reuses the recordfix primitives; cap remains 2,820 s and K is never emitted |

Current implementation references: `c10y_precast_diag.py:75` (phase), `:226` (durable capture), `:235`/`:241` (input/Q identity), `:256` (actual solve dispatch), `:271` (exception locals), `:311` (original trace), `:415` (native on/off), `:727` (fresh interruption authority), `:745` (CLI ownership/modes). Shell: `:25` (owned group), `:55` (bounded cleanup), `:65` (armed timer), `:92` (timeout publisher), `:101` (closeout, deadline cancelled last), `:121` (signal traps), `:126` (finalizer), `:144` (namespace refusal).

### RED before GREEN

Before production fixes, Astra's seven selected probes ran against the original three code files: direct failure lacked M/RHS; factor failure was replaced by `TypeError`; observer factor-M mutation did not halt; TERM/HUP left a live worker; INT had no interruption authority. The genuine discrepancy control passed. Result: seven tests, five failures and one error. The five added corruption/phase/abnormal/publication probes also ran RED (four failures, one error). Production changes followed those observations.

The first full candidate ran 60 tests and caught a namespace-closeout defect introduced in this fix; it was corrected without changing the refusal expectation. Its other failed assertion expected a post-solve packet after a newly earlier corruption halt; the fixture now requires the retained pre-solve packet. Additional RED tests then exposed missing earlier capture on observer-off failure and missing finalizer-failure publication. The 62-test candidate passed after those corrections. The later supervisor-boundary run verified fsync ordering, exposed interrupted-publisher timeout recovery, and also had an over-specific descendant-fixture expectation (HALT rather than the possible timeout authority under its shortened timer); the fixture now accepts either terminal INCONCLUSIVE authority and independently proves descendant termination. All intermediate outputs remain below; only the final 65/285 runs constitute final GREEN.

A small CPU dispatch probe, performed before writing the dispatch adapter, observed `aten._linalg_solve_ex.default` with M `(3,3)` and RHS `(3,2)`. Coverage requires one observed solve per native solve site, so an unsupported dispatch path fails closed. Completed input references/copies are released after each successful return validation rather than retaining dense matrices across layers.

### Exact final test commands

From the verified worktree root, through `rtk proxy`:

```sh
env C10Y_ALLOWED_CHILD_TESTS=1 PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 .venv/bin/python -B experiments/track_c/c10y_precast_diag_selftest.py > /private/tmp/c10y_build/precast_fix1_20261009T185431Z/precast_full_GREEN_final.log 2>&1
env C10Y_ALLOWED_CHILD_TESTS=1 PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 .venv/bin/python -B experiments/track_c/c10y_directdw_selftest.py > /private/tmp/c10y_build/precast_fix1_20261009T185431Z/c10y_full_GREEN_final.log 2>&1
/bin/bash -n tools/run_c10y_precast_diag.sh
```

65 tests: **43.331 s**, 0 failures/errors/skips. Existing 285 tests: **24.825 s**, 0 failures/errors/skips. Bash syntax and in-memory Python `compile()` PASS. CPU tests block live-tree writes, model/harness imports, accelerator calls and non-stub children. The existing suite ended with `ISOLATION OWNED LISTING DRIFT: []` and `SYS_MODULES_FORBIDDEN: []`; it observed unrelated, unattributed changes to `results/mathlab/harvest_launch_20261009T184919Z.log` and `results/mathlab_staging/runs/harvest_20261009T184932Z_95961/events.jsonl`. Those paths were not edited or reverted by this builder. Its UNVERIFIED JSON is a refusal fixture.

Shell integration tests copy the actual launcher into temporary roots, reduce only the cap/reserve to 6/4 s, add fixture-only timer observation or an injected abnormal exit, and use stdlib fake workers/publishers. The descendant fixture uses a stdlib child in the owned worker group. Stub sources/results stay below `/private/tmp/c10y_build`; the copied launcher also retains its own `/private/tmp/c10y_precast_deadline.*` control evidence. No copied fixture is a production launcher. The normal 2,820/10 values are unchanged in the delivered shell.

### File SHAs and protected audit

Reviewed Astra artifact SHA-256: `07ec28907fa086636570cca17f15a98170dcf776a80c29ad3de54c9708708885`. Frozen scope file and `git show 4f7b22c:docs/C10Y_PRECAST_DIAG_SCOPE.md` both hash to `097c662803a94a897dd588c9e1f09c6af7b17a25019c1439ea39844c65f0a9a8`.

| Owned implementation/test file | Before round | After round |
|---|---|---|
| `experiments/track_c/c10y_precast_diag.py` | `1442b35b38744b84184b57cfafdcbcda31d94b726da6d6c9378806ddaf935b22` | `520939b5c49376d5ebfa7c219d905e617881851d6c569071eee3523d0fa91ee9` |
| `experiments/track_c/c10y_precast_diag_selftest.py` | `acbafa518218e333daaf4dc9164851f22174dec55418bbeab6d6a34946107b9f` | `af562e602fdbaeab48a7a897a3f823cd763f5282c9dc2c7a004b5ef221254b88` |
| `tools/run_c10y_precast_diag.sh` | `430c1b92806d0397142ceb0f5ea48b93758d3bbdf14b593fc19ba22e78e351a0` | `a2f4c05cfc62af32d5645115b635d6b4330faeca72d34e3a6d9737267aa15396` |

Source/input SHA inventory (current observed bytes; source mismatch retained explicitly):

| File | Observed SHA-256 | Pin status |
|---|---|---|
| `configs/hparams/qwen25_3b_memit_hparams.json` | `4225cc6aabc3eb9fa62d2bb2cac68b1238de3a39c5e469da635e6e1464aa3bb4` | MATCH |
| `configs/screens/g6_screen_qwen3b_v2.json` | `482c05f8f33c59d3e469566fe6f3c48eb183d3cb2fbb791f31dcad7102517c5c` | MATCH |
| `docs/C10Y_DIRECTDW_PREREG.md` | `005391a39e31d8174419de3e39078a42209ded1b7ab8caaf098d5d8a4f755004` | MATCH |
| `docs/C10Y_PRECAST_DIAG_SCOPE.md` | `097c662803a94a897dd588c9e1f09c6af7b17a25019c1439ea39844c65f0a9a8` | MATCH |
| `experiments/track_c/c10e_bandknob.py` | `1f6be5811d7e58f3ebda16867a4a174b1cf24d47f9a2514cf9c3f9d29f18e695` | MATCH |
| `experiments/track_c/c10y_directdw_arms.py` | `ead3cef2266a7c81035e5acb6c3a97b42f83da556ba093a9fd28ec403f7e158c` | MATCH |
| `experiments/track_c/c10y_directdw_selftest.py` | `81f3c07ec36fe1aa10bf31526f712cb3b015b0a86f714ba7aa3123a81875dd25` | Observed; no repin |
| `experiments/track_c/c10y_precast_diag.py` | `520939b5c49376d5ebfa7c219d905e617881851d6c569071eee3523d0fa91ee9` | Observed; no repin |
| `experiments/track_c/c10z_astra_benchmark.py` | `3703d8b9c363bb06eab0ca66f38f4b01114363ae75a9d0397701e75aa2520041` | MISMATCH; existing pin retained |
| `memit_dry_run/memit/globals.yml` | `86ab5194b3cddc19c14173a3b8f13563c554d252666eb563a4ac2f919e087459` | Observed; no repin |
| `memit_dry_run/memit/memit/compute_ks.py` | `0b039be47c548f046b71cad4efce63414f53edbaa657bde868a20cdd35a2f5c7` | MATCH |
| `memit_dry_run/memit/memit/compute_z.py` | `d94af7fa14e5a4a20d5fa6361e0cbb30da0ff957db31922557ff809c34205dea` | MATCH |
| `memit_dry_run/memit/memit/memit_hparams.py` | `1b229b882b031ddbb59f06ad6ba58d5c33b17826bbfddf80f767e96931b595b2` | Observed; no repin |
| `memit_dry_run/memit/memit/memit_main.py` | `d941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65` | MATCH |
| `memit_dry_run/memit/rome/repr_tools.py` | `d4c2324ba20cbcce7f4ccfcf58ad002912edf0ad2fc72ab4e9bf46cc9dfed336` | MATCH |
| `memit_dry_run/memit/util/device.py` | `868627783827f03763ba9c210de2ddbd607e050330eccf7757fccfd9e985cf2b` | Observed; no repin |
| `memit_dry_run/memit/util/nethook.py` | `20e84c9413518af3aee76762071f823cbe5d75c4658e4ffa7bdab045df735f7c` | Observed; no repin |
| `results/c10y_directdw_calib4/context_templates_calib.json` | `9472b663a34cfd9c0bb5448087ae0c2c333b1988b70f211fb2d90baaf8b560b7` | Observed; no repin |
| `results/c10y_directdw_calib4/recordfix_build_report.md` | `6bf63a752d50d3b1c2f048e7135155461e1d66c3b351d35d77f14f83ff857ac4` | Observed; no repin |
| `results/c10y_directdw_calib4/targets_calib.pt` | `1d95c75a2aa0abb80d2ab5324b54cf58fcb1bbc3249e8f1f19a3b84ada838078` | Observed; no repin |
| `tools/c10w_p2_gate.py` | `fb6568a6e159e84b22971aa893c3a83bcaaa16085f4abd9c76ca50b4a3362a26` | MATCH |
| `tools/engine_fingerprint.py` | `450ee83ac829817299ead301c4a3d20702f431deaea4be58c77ecfd89a329162` | MATCH |
| `tools/run_c10y_precast_diag.sh` | `a2f4c05cfc62af32d5645115b635d6b4330faeca72d34e3a6d9737267aa15396` | Observed; no repin |

All **156** before-round protected-file hashes match at audit: scope/prereg, all snapshotted engine sources and CORPUS files, C10Y source/results, Astra review, recordfix report, runbook and checkpoint. No protected drift was observed in that set. The unrelated C10Z benchmark source is audited separately above; it was not in the before-round 156-file snapshot, so no claim is made about its exact modification time during this round. Read-only audit observed HEAD `a226f3e5b845480e18fd7dbcab24978d65f2f571`, branch `worktree-c10k-route-a`, and the same worktree root. No git mutation was issued; the shared tree contains other team work and is not claimed globally clean.

The report's first **219,023 bytes** remain byte-identical, SHA-256 `e48c4c7507151027f7efb0d788a540586249ffda01941dd174fa0ae00caa117d`. Only this dated section is appended. Full protected hashes are retained in `/private/tmp/c10y_build/precast_fix1_20261009T185431Z/audit_before_append.json`; the final report SHA and append-only verification are retained in `/private/tmp/c10y_build/precast_fix1_20261009T185431Z/final_verification.json` after writing (a report cannot embed its own full-file SHA without changing it). The report is the scoped session handoff; no checkpoint/ledger/memory context file was authored.

### Exact future launch command and runtime boundary — NOT EXECUTED

The source mismatch must be resolved by the team without bypassing the identity gate, and scope-mandated Astra implementation re-review and separate team admission remain required. This command is recorded for review only:

```sh
/bin/bash '/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/run_c10y_precast_diag.sh' \
  --utc "$(/bin/date -u +%Y%m%dT%H%M%SZ)"
```

Fresh exclusive namespace: `results/c10y_precast_diag/<UTC>/`. The source audit confirms that no such live namespace was created. Gate/fingerprint immediately-before-load behavior remains unchanged and is covered by the CPU preload rejection fixture; neither real GPU gate nor fingerprint subprocess was launched.

The frozen planning total remains **2,440 s** (600 setup + 1,360 targets/native + 300 controls/comparisons + 180 serialization), with a fixed **2,820 s** setup-through-cleanup hard cap and a 10 s cleanup reserve. No in-run increase is allowed. Live feasibility remains **UNVERIFIED**: additional pre-solve packets, byte checks, fsyncs, fp64 solves/conditioning and native off/on controls were not timed at the real model/solve shape. The new packets add dense-M I/O; a 11,008-square fp32 matrix alone is 484,704,256 bytes. The small CPU solve fixtures and full update-coordinate quantile test do not establish native RSS, filesystem capacity/throughput, device parity or production inertness.

The interrupted shell fixtures empirically prove TERM/KILL, reaping of direct children, descendant termination and fresh publication at reduced caps. KILL cannot restore model state; fresh supervisor records explicitly retain that UNVERIFIED boundary. Filesystem failure or an unresponsive publisher at the absolute cap can leave only committed partial/control evidence; no incomplete invocation admits R or S. Classification stays ordered INCONCLUSIVE/R/S/UNCLASSIFIED, K never emitted, with no numerical-magnitude threshold. All diagnostic science remains unrun and concerns NEW COMPUTATION inputs only; calibration 4 remains terminal.

### Complete captured output for this fix round

| Evidence file | Bytes | SHA-256 |
|---|---:|---|
| `astra_probes_RED.log` | 8658 | `c150d39d5f89bcd92da39e5e1d2d63db8cc4328821ebfc1452930eabad954be6` |
| `expanded_RED.log` | 7430 | `3edfa4bfb944cd1d96bacee55184f02428e7790c111a61a74aa90502843fdcc6` |
| `native_GREEN_attempt1.log` | 1174 | `e10af2dca27ba749bdc6a8bdbd7eadd98a9194a8fe89d227e998f29db72e3a76` |
| `supervisor_GREEN_attempt1.log` | 1038 | `92d36985ee3a20bfa75129a86ceafa6bf36cdf1a5bcd16593b53ada4d92ca7f7` |
| `precast_full_GREEN_attempt1.log` | 11210 | `ec813cce22aeb4c021aa971bba73e7093b23b52a332f7b38bea2b1cb9be21b87` |
| `failure_boundary_RED.log` | 2782 | `a7774971f7c83b146d07bb206851612ddfb892ac8bace12c15da5630ecabb24c` |
| `precast_full_GREEN_attempt2.log` | 9582 | `a13e60f4cb13473a1d614ac4f565278ae1f090932167e6b173139a6c4e62be69` |
| `supervisor_boundary_RED.log` | 3401 | `224665606fcabf37318189d77a992923eae0f15d0053af0b67997de88b51174d` |
| `supervisor_boundary_GREEN_attempt1.log` | 588 | `a772e0390a51db26176e64ffa57b5f8c44475154d0f47242046de5d19c373136` |
| `precast_full_GREEN_final.log` | 10072 | `8bdf1dc0f21f48d11aabb98c05f0d639a5f01b12f64c11fa3327e48f9267fde1` |
| `c10y_full_GREEN_final.log` | 41317 | `a61aa2dbf19ce929c7bfbf09f2c103c9aca3fbc7ddedeba576c479cdf71e1165` |
| `source_pin_audit_initial_fail.log` | 3095 | `2f36024ccb865d76c0e5d4915a927538f3357a30fecc723b61546f4e71bc976d` |
| `audit_before_append.log` | 1828 | `e96ad704c7450de39d25c69d00a7a5b0e12adf02a02cbaac04194be33284b2c0` |

#### Astra CPU probes RED — `astra_probes_RED.log`

Captured command: `env C10Y_ALLOWED_CHILD_TESTS=1 PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 .venv/bin/python -B experiments/track_c/c10y_precast_diag_selftest.py Contracts.test_native_direct_solve_failure_retains_inputs_and_original_exception Contracts.test_native_factor_solve_failure_retains_inputs_and_original_exception Contracts.test_native_factor_actual_matrix_and_Q_are_compared Contracts.test_genuine_native_operand_discrepancy_remains_valid_S_evidence Contracts.test_real_shell_supervisor_TERM_cleans_owned_worker_and_publishes_INCONCLUSIVE Contracts.test_real_shell_supervisor_INT_cleans_owned_worker_and_publishes_INCONCLUSIVE Contracts.test_real_shell_supervisor_HUP_cleans_owned_worker_and_publishes_INCONCLUSIVE > /private/tmp/c10y_build/precast_fix1_20261009T185431Z/astra_probes_RED.log 2>&1`

```text
test_native_direct_solve_failure_retains_inputs_and_original_exception (__main__.Contracts.test_native_direct_solve_failure_retains_inputs_and_original_exception) ... FAIL
test_native_factor_solve_failure_retains_inputs_and_original_exception (__main__.Contracts.test_native_factor_solve_failure_retains_inputs_and_original_exception) ... FAIL
test_native_factor_actual_matrix_and_Q_are_compared (__main__.Contracts.test_native_factor_actual_matrix_and_Q_are_compared) ... FAIL
test_genuine_native_operand_discrepancy_remains_valid_S_evidence (__main__.Contracts.test_genuine_native_operand_discrepancy_remains_valid_S_evidence) ... ok
test_real_shell_supervisor_TERM_cleans_owned_worker_and_publishes_INCONCLUSIVE (__main__.Contracts.test_real_shell_supervisor_TERM_cleans_owned_worker_and_publishes_INCONCLUSIVE) ... FAIL
test_real_shell_supervisor_INT_cleans_owned_worker_and_publishes_INCONCLUSIVE (__main__.Contracts.test_real_shell_supervisor_INT_cleans_owned_worker_and_publishes_INCONCLUSIVE) ... ERROR
test_real_shell_supervisor_HUP_cleans_owned_worker_and_publishes_INCONCLUSIVE (__main__.Contracts.test_real_shell_supervisor_HUP_cleans_owned_worker_and_publishes_INCONCLUSIVE) ... FAIL

======================================================================
ERROR: test_real_shell_supervisor_INT_cleans_owned_worker_and_publishes_INCONCLUSIVE (__main__.Contracts.test_real_shell_supervisor_INT_cleans_owned_worker_and_publishes_INCONCLUSIVE)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 606, in test_real_shell_supervisor_INT_cleans_owned_worker_and_publishes_INCONCLUSIVE
    self.run_shell_stub('interrupt_INT')
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 658, in run_shell_stub
    value=json.loads((out/'supervisor_interruption.json').read_text())
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/pathlib.py", line 1058, in read_text
    with self.open(mode='r', encoding=encoding, errors=errors) as f:
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/pathlib.py", line 1044, in open
    return io.open(self, mode, buffering, encoding, errors, newline)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
FileNotFoundError: [Errno 2] No such file or directory: '/private/tmp/c10y_build/tmp7u0_223g/results/c10y_precast_diag/20261009T000000Z/supervisor_interruption.json'

======================================================================
FAIL: test_native_direct_solve_failure_retains_inputs_and_original_exception (__main__.Contracts.test_native_direct_solve_failure_retains_inputs_and_original_exception)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 398, in test_native_direct_solve_failure_retains_inputs_and_original_exception
    self.assertIs(caught.exception,error);self.assertTrue(at_call['durable'],'M/RHS absent before direct solve')
                                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: False is not true : M/RHS absent before direct solve

======================================================================
FAIL: test_native_factor_solve_failure_retains_inputs_and_original_exception (__main__.Contracts.test_native_factor_solve_failure_retains_inputs_and_original_exception)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 423, in test_native_factor_solve_failure_retains_inputs_and_original_exception
    A.capture_solve(h,h.hp,requests,[torch.eye(3) for _ in range(5)],[torch.zeros(3,3) for _ in range(5)])
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_arms.py", line 280, in capture_solve
    captured=factor_solve(K,rf,Pi,ca,getattr(H,'L2',1.))
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag.py", line 265, in trace
    self.j.finite('factors_'+self.arm+'_L%d_Y'%l,{**arg,'M':v['matrix'],'Q':self.q.get((l,'factor_Q'))})
                                                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
TypeError: 'NoneType' object is not a mapping

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 424, in test_native_factor_solve_failure_retains_inputs_and_original_exception
    except BaseException as caught:self.assertIs(caught,error,'native factor failure was replaced')
                                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: TypeError("'NoneType' object is not a mapping") is not RuntimeError('ASTRA-FACTOR-SOLVE-FAIL') : native factor failure was replaced

======================================================================
FAIL: test_native_factor_actual_matrix_and_Q_are_compared (__main__.Contracts.test_native_factor_actual_matrix_and_Q_are_compared)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 376, in test_native_factor_actual_matrix_and_Q_are_compared
    with self.assertRaisesRegex(A.Halt,'OBSERVER-SOLVE-INPUT'):
AssertionError: Halt not raised

======================================================================
FAIL: test_real_shell_supervisor_TERM_cleans_owned_worker_and_publishes_INCONCLUSIVE (__main__.Contracts.test_real_shell_supervisor_TERM_cleans_owned_worker_and_publishes_INCONCLUSIVE)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 603, in test_real_shell_supervisor_TERM_cleans_owned_worker_and_publishes_INCONCLUSIVE
    self.run_shell_stub('interrupt_TERM')
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 657, in run_shell_stub
    self.assertFalse(live,'interrupted supervisor abandoned owned worker (exit '+str(rc)+')')
AssertionError: True is not false : interrupted supervisor abandoned owned worker (exit -15)

======================================================================
FAIL: test_real_shell_supervisor_HUP_cleans_owned_worker_and_publishes_INCONCLUSIVE (__main__.Contracts.test_real_shell_supervisor_HUP_cleans_owned_worker_and_publishes_INCONCLUSIVE)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 609, in test_real_shell_supervisor_HUP_cleans_owned_worker_and_publishes_INCONCLUSIVE
    self.run_shell_stub('interrupt_HUP')
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 657, in run_shell_stub
    self.assertFalse(live,'interrupted supervisor abandoned owned worker (exit '+str(rc)+')')
AssertionError: True is not false : interrupted supervisor abandoned owned worker (exit -1)

----------------------------------------------------------------------
Ran 7 tests in 6.910s

FAILED (failures=5, errors=1)
```

#### Expanded corruption/phase/supervisor RED — `expanded_RED.log`

Captured command: `env C10Y_ALLOWED_CHILD_TESTS=1 PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 .venv/bin/python -B experiments/track_c/c10y_precast_diag_selftest.py Contracts.test_observer_factor_Q_copy_mutation_invalidates_evidence Contracts.test_observer_direct_M_mutation_at_return_invalidates_evidence Contracts.test_phase_failure_publication_preserves_original_exception Contracts.test_real_shell_supervisor_abnormal_exit_cleans_owned_worker_and_publishes_INCONCLUSIVE Contracts.test_interrupted_publication_preserves_prior_bytes_and_is_fresh_INCONCLUSIVE > /private/tmp/c10y_build/precast_fix1_20261009T185431Z/expanded_RED.log 2>&1`

```text
test_observer_factor_Q_copy_mutation_invalidates_evidence (__main__.Contracts.test_observer_factor_Q_copy_mutation_invalidates_evidence) ... FAIL
test_observer_direct_M_mutation_at_return_invalidates_evidence (__main__.Contracts.test_observer_direct_M_mutation_at_return_invalidates_evidence) ... FAIL
test_phase_failure_publication_preserves_original_exception (__main__.Contracts.test_phase_failure_publication_preserves_original_exception) ... FAIL
test_real_shell_supervisor_abnormal_exit_cleans_owned_worker_and_publishes_INCONCLUSIVE (__main__.Contracts.test_real_shell_supervisor_abnormal_exit_cleans_owned_worker_and_publishes_INCONCLUSIVE) ... FAIL
test_interrupted_publication_preserves_prior_bytes_and_is_fresh_INCONCLUSIVE (__main__.Contracts.test_interrupted_publication_preserves_prior_bytes_and_is_fresh_INCONCLUSIVE) ... ERROR

======================================================================
ERROR: test_interrupted_publication_preserves_prior_bytes_and_is_fresh_INCONCLUSIVE (__main__.Contracts.test_interrupted_publication_preserves_prior_bytes_and_is_fresh_INCONCLUSIVE)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 650, in test_interrupted_publication_preserves_prior_bytes_and_is_fresh_INCONCLUSIVE
    D.interrupted_terminal(self.root,143,3.,'TERM')
    ^^^^^^^^^^^^^^^^^^^^^^
AttributeError: module 'c10y_precast_diag' has no attribute 'interrupted_terminal'

======================================================================
FAIL: test_observer_factor_Q_copy_mutation_invalidates_evidence (__main__.Contracts.test_observer_factor_Q_copy_mutation_invalidates_evidence)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 436, in test_observer_factor_Q_copy_mutation_invalidates_evidence
    with self.assertRaisesRegex(A.Halt,'OBSERVER-SOLVE-INPUT'):
AssertionError: Halt not raised

======================================================================
FAIL: test_observer_direct_M_mutation_at_return_invalidates_evidence (__main__.Contracts.test_observer_direct_M_mutation_at_return_invalidates_evidence)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 448, in test_observer_direct_M_mutation_at_return_invalidates_evidence
    with self.assertRaisesRegex(A.Halt,'OBSERVER-SOLVE-INPUT'):
AssertionError: Halt not raised

======================================================================
FAIL: test_phase_failure_publication_preserves_original_exception (__main__.Contracts.test_phase_failure_publication_preserves_original_exception)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag.py", line 77, in phase
    try: yield
         ^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 460, in test_phase_failure_publication_preserves_original_exception
    with self.j.phase('native_A1_single'):raise error
                                          ^^^^^^^^^^^
RuntimeError: ORIGINAL-PHASE-FAILURE

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 460, in test_phase_failure_publication_preserves_original_exception
    with self.j.phase('native_A1_single'):raise error
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/contextlib.py", line 158, in __exit__
    self.gen.throw(typ, value, traceback)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag.py", line 81, in phase
    self.record('phase_'+name+'_failed',{'phase':name,'status':'INCOMPLETE','code':getattr(error,'code','INSTRUMENT-ERROR'),
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1124, in __call__
    return self._mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1128, in _mock_call
    return self._execute_mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1189, in _execute_mock_call
    result = effect(*args, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 456, in failed_sink
    if name.endswith('_failed'):raise OSError('CPU-SINK-FAILURE')
                                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
OSError: CPU-SINK-FAILURE

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 461, in test_phase_failure_publication_preserves_original_exception
    except BaseException as caught:self.assertIs(caught,error)
                                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: OSError('CPU-SINK-FAILURE') is not RuntimeError('ORIGINAL-PHASE-FAILURE')

======================================================================
FAIL: test_real_shell_supervisor_abnormal_exit_cleans_owned_worker_and_publishes_INCONCLUSIVE (__main__.Contracts.test_real_shell_supervisor_abnormal_exit_cleans_owned_worker_and_publishes_INCONCLUSIVE)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 645, in test_real_shell_supervisor_abnormal_exit_cleans_owned_worker_and_publishes_INCONCLUSIVE
    self.run_shell_stub('abnormal')
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 709, in run_shell_stub
    self.assertFalse(live,'interrupted supervisor abandoned owned worker (exit '+str(rc)+')')
AssertionError: True is not false : interrupted supervisor abandoned owned worker (exit 1)

----------------------------------------------------------------------
Ran 5 tests in 1.048s

FAILED (failures=4, errors=1)
```

#### Focused native candidate GREEN — `native_GREEN_attempt1.log`

Captured command: `env C10Y_ALLOWED_CHILD_TESTS=1 PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 .venv/bin/python -B experiments/track_c/c10y_precast_diag_selftest.py Contracts.test_native_direct_solve_failure_retains_inputs_and_original_exception Contracts.test_native_factor_solve_failure_retains_inputs_and_original_exception Contracts.test_native_factor_actual_matrix_and_Q_are_compared Contracts.test_observer_factor_Q_copy_mutation_invalidates_evidence Contracts.test_observer_direct_M_mutation_at_return_invalidates_evidence Contracts.test_phase_failure_publication_preserves_original_exception Contracts.test_genuine_native_operand_discrepancy_remains_valid_S_evidence > /private/tmp/c10y_build/precast_fix1_20261009T185431Z/native_GREEN_attempt1.log 2>&1`

```text
test_native_direct_solve_failure_retains_inputs_and_original_exception (__main__.Contracts.test_native_direct_solve_failure_retains_inputs_and_original_exception) ... ok
test_native_factor_solve_failure_retains_inputs_and_original_exception (__main__.Contracts.test_native_factor_solve_failure_retains_inputs_and_original_exception) ... ok
test_native_factor_actual_matrix_and_Q_are_compared (__main__.Contracts.test_native_factor_actual_matrix_and_Q_are_compared) ... ok
test_observer_factor_Q_copy_mutation_invalidates_evidence (__main__.Contracts.test_observer_factor_Q_copy_mutation_invalidates_evidence) ... ok
test_observer_direct_M_mutation_at_return_invalidates_evidence (__main__.Contracts.test_observer_direct_M_mutation_at_return_invalidates_evidence) ... ok
test_phase_failure_publication_preserves_original_exception (__main__.Contracts.test_phase_failure_publication_preserves_original_exception) ... ok
test_genuine_native_operand_discrepancy_remains_valid_S_evidence (__main__.Contracts.test_genuine_native_operand_discrepancy_remains_valid_S_evidence) ... ok

----------------------------------------------------------------------
Ran 7 tests in 4.071s

OK
```

#### Focused interruption candidate GREEN — `supervisor_GREEN_attempt1.log`

Captured command: `env C10Y_ALLOWED_CHILD_TESTS=1 PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 .venv/bin/python -B experiments/track_c/c10y_precast_diag_selftest.py Contracts.test_real_shell_supervisor_TERM_cleans_owned_worker_and_publishes_INCONCLUSIVE Contracts.test_real_shell_supervisor_INT_cleans_owned_worker_and_publishes_INCONCLUSIVE Contracts.test_real_shell_supervisor_HUP_cleans_owned_worker_and_publishes_INCONCLUSIVE Contracts.test_real_shell_supervisor_abnormal_exit_cleans_owned_worker_and_publishes_INCONCLUSIVE Contracts.test_interrupted_publication_preserves_prior_bytes_and_is_fresh_INCONCLUSIVE > /private/tmp/c10y_build/precast_fix1_20261009T185431Z/supervisor_GREEN_attempt1.log 2>&1`

```text
test_real_shell_supervisor_TERM_cleans_owned_worker_and_publishes_INCONCLUSIVE (__main__.Contracts.test_real_shell_supervisor_TERM_cleans_owned_worker_and_publishes_INCONCLUSIVE) ... ok
test_real_shell_supervisor_INT_cleans_owned_worker_and_publishes_INCONCLUSIVE (__main__.Contracts.test_real_shell_supervisor_INT_cleans_owned_worker_and_publishes_INCONCLUSIVE) ... ok
test_real_shell_supervisor_HUP_cleans_owned_worker_and_publishes_INCONCLUSIVE (__main__.Contracts.test_real_shell_supervisor_HUP_cleans_owned_worker_and_publishes_INCONCLUSIVE) ... ok
test_real_shell_supervisor_abnormal_exit_cleans_owned_worker_and_publishes_INCONCLUSIVE (__main__.Contracts.test_real_shell_supervisor_abnormal_exit_cleans_owned_worker_and_publishes_INCONCLUSIVE) ... ok
test_interrupted_publication_preserves_prior_bytes_and_is_fresh_INCONCLUSIVE (__main__.Contracts.test_interrupted_publication_preserves_prior_bytes_and_is_fresh_INCONCLUSIVE) ... ok

----------------------------------------------------------------------
Ran 5 tests in 8.702s

OK
```

#### First full candidate, 60 tests; failed — `precast_full_GREEN_attempt1.log`

Captured command: `env C10Y_ALLOWED_CHILD_TESTS=1 PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 .venv/bin/python -B experiments/track_c/c10y_precast_diag_selftest.py > /private/tmp/c10y_build/precast_fix1_20261009T185431Z/precast_full_GREEN_attempt1.log 2>&1`

```text
test_48_targets_computed_once_saved_reloaded_and_shared_by_original_paths (__main__.Contracts.test_48_targets_computed_once_saved_reloaded_and_shared_by_original_paths) ... ok
test_INCONCLUSIVE_precedes_every_other_reading (__main__.Contracts.test_INCONCLUSIVE_precedes_every_other_reading) ... ok
test_R_requires_every_cell_and_A7_device_difference (__main__.Contracts.test_R_requires_every_cell_and_A7_device_difference) ... ok
test_S_needs_direct_trace_evidence_and_K_never_emitted (__main__.Contracts.test_S_needs_direct_trace_evidence_and_K_never_emitted) ... ok
test_actual_representation_batch_padding_and_indices_captured_without_id_assumption (__main__.Contracts.test_actual_representation_batch_padding_and_indices_captured_without_id_assumption) ... ok
test_completed_float64_direct_solution_survives_next_solve_failure (__main__.Contracts.test_completed_float64_direct_solution_survives_next_solve_failure) ... ok
test_completed_native_CPU_product_survives_later_control_halt (__main__.Contracts.test_completed_native_CPU_product_survives_later_control_halt) ... ok
test_device_product_observed_from_original_effective_weight (__main__.Contracts.test_device_product_observed_from_original_effective_weight) ... ok
test_difference_metrics_and_weight_coordinate_columns (__main__.Contracts.test_difference_metrics_and_weight_coordinate_columns) ... ok
test_exclusive_JSON_and_tensor_collision_have_no_sibling (__main__.Contracts.test_exclusive_JSON_and_tensor_collision_have_no_sibling) ... ok
test_fail_closed_gpu_and_fingerprint_records_precede_loader (__main__.Contracts.test_fail_closed_gpu_and_fingerprint_records_precede_loader) ... ok
test_finalizer_incomplete_worker_cannot_publish_R (__main__.Contracts.test_finalizer_incomplete_worker_cannot_publish_R) ... ok
test_finalizer_malformed_worker_preserves_exception_and_inconclusive (__main__.Contracts.test_finalizer_malformed_worker_preserves_exception_and_inconclusive) ... ok
test_finalizer_overwrite_refusal_keeps_terminal_bytes (__main__.Contracts.test_finalizer_overwrite_refusal_keeps_terminal_bytes) ... ok
test_finalizer_rejects_completed_claim_with_incomplete_phases (__main__.Contracts.test_finalizer_rejects_completed_claim_with_incomplete_phases) ... ok
test_float64_realization_cannot_demote_to_float32 (__main__.Contracts.test_float64_realization_cannot_demote_to_float32) ... ok
test_float64_realization_casts_on_CPU_before_device_transfer (__main__.Contracts.test_float64_realization_casts_on_CPU_before_device_transfer) ... ok
test_float64_solve_and_promoted_product_are_distinct (__main__.Contracts.test_float64_solve_and_promoted_product_are_distinct) ... ok
test_forced_native_halt_preserves_capture_and_cleans_weights_globals (__main__.Contracts.test_forced_native_halt_preserves_capture_and_cleans_weights_globals) ... ok
test_fresh_import_is_model_and_torch_free (__main__.Contracts.test_fresh_import_is_model_and_torch_free) ... ok
test_fresh_namespace_existing_directory_and_symlink_refused (__main__.Contracts.test_fresh_namespace_existing_directory_and_symlink_refused) ... ok
test_full_weight_coordinate_quantiles_exceed_torch_limit (__main__.Contracts.test_full_weight_coordinate_quantiles_exceed_torch_limit) ... ok
test_gate_inputs_fsynced_and_reloaded_before_predicate (__main__.Contracts.test_gate_inputs_fsynced_and_reloaded_before_predicate) ... ok
test_genuine_native_operand_discrepancy_remains_valid_S_evidence (__main__.Contracts.test_genuine_native_operand_discrepancy_remains_valid_S_evidence) ... ok
test_interrupted_publication_preserves_prior_bytes_and_is_fresh_INCONCLUSIVE (__main__.Contracts.test_interrupted_publication_preserves_prior_bytes_and_is_fresh_INCONCLUSIVE) ... ok
test_interrupted_serialization_is_incomplete_and_retains_previous_values (__main__.Contracts.test_interrupted_serialization_is_incomplete_and_retains_previous_values) ... ok
test_malformed_classification_capture_is_INCONCLUSIVE (__main__.Contracts.test_malformed_classification_capture_is_INCONCLUSIVE) ... ok
test_missing_capture_refuses_instead_of_reimplementing (__main__.Contracts.test_missing_capture_refuses_instead_of_reimplementing) ... ok
test_missing_reference_Q_retains_available_operands_before_coverage_halt (__main__.Contracts.test_missing_reference_Q_retains_available_operands_before_coverage_halt) ... ok
test_native_direct_solve_failure_retains_inputs_and_original_exception (__main__.Contracts.test_native_direct_solve_failure_retains_inputs_and_original_exception) ... ok
test_native_direct_update_included_in_all_pair_measurements (__main__.Contracts.test_native_direct_update_included_in_all_pair_measurements) ... ok
test_native_factor_actual_matrix_and_Q_are_compared (__main__.Contracts.test_native_factor_actual_matrix_and_Q_are_compared) ... ok
test_native_factor_solve_failure_retains_inputs_and_original_exception (__main__.Contracts.test_native_factor_solve_failure_retains_inputs_and_original_exception) ... ok
test_native_missing_factor_Q_is_inconclusive_capture_failure (__main__.Contracts.test_native_missing_factor_Q_is_inconclusive_capture_failure) ... ok
test_nonfinite_operand_persisted_before_halt (__main__.Contracts.test_nonfinite_operand_persisted_before_halt) ... ok
test_observer_direct_M_mutation_at_return_invalidates_evidence (__main__.Contracts.test_observer_direct_M_mutation_at_return_invalidates_evidence) ... ok
test_observer_factor_Q_copy_mutation_invalidates_evidence (__main__.Contracts.test_observer_factor_Q_copy_mutation_invalidates_evidence) ... ok
test_observer_original_code_coverage_off_on_and_native_operands (__main__.Contracts.test_observer_original_code_coverage_off_on_and_native_operands) ... ok
test_observer_tensor_inertness_catches_discarded_cur_mutation (__main__.Contracts.test_observer_tensor_inertness_catches_discarded_cur_mutation) ... FAIL
test_packet_tamper_refused_before_downstream_consumption (__main__.Contracts.test_packet_tamper_refused_before_downstream_consumption) ... ok
test_phase_failure_publication_preserves_original_exception (__main__.Contracts.test_phase_failure_publication_preserves_original_exception) ... ok
test_real_shell_existing_namespace_refused_without_finalizer (__main__.Contracts.test_real_shell_existing_namespace_refused_without_finalizer) ... FAIL
test_real_shell_finalizer_timeout_has_fresh_supervisor_diagnostic (__main__.Contracts.test_real_shell_finalizer_timeout_has_fresh_supervisor_diagnostic) ... ok
test_real_shell_supervisor_HUP_cleans_owned_worker_and_publishes_INCONCLUSIVE (__main__.Contracts.test_real_shell_supervisor_HUP_cleans_owned_worker_and_publishes_INCONCLUSIVE) ... ok
test_real_shell_supervisor_INT_cleans_owned_worker_and_publishes_INCONCLUSIVE (__main__.Contracts.test_real_shell_supervisor_INT_cleans_owned_worker_and_publishes_INCONCLUSIVE) ... ok
test_real_shell_supervisor_TERM_cleans_owned_worker_and_publishes_INCONCLUSIVE (__main__.Contracts.test_real_shell_supervisor_TERM_cleans_owned_worker_and_publishes_INCONCLUSIVE) ... ok
test_real_shell_supervisor_abnormal_exit_cleans_owned_worker_and_publishes_INCONCLUSIVE (__main__.Contracts.test_real_shell_supervisor_abnormal_exit_cleans_owned_worker_and_publishes_INCONCLUSIVE) ... ok
test_real_shell_supervisor_hanging_stub_preserves_timeout_and_kills_worker (__main__.Contracts.test_real_shell_supervisor_hanging_stub_preserves_timeout_and_kills_worker) ... ok
test_real_shell_supervisor_setup_timeout_retains_owned_namespace_diagnostic (__main__.Contracts.test_real_shell_supervisor_setup_timeout_retains_owned_namespace_diagnostic) ... ok
test_real_shell_supervisor_worker_exit_before_start_is_diagnosed (__main__.Contracts.test_real_shell_supervisor_worker_exit_before_start_is_diagnosed) ... ok
test_real_shell_worker_log_collision_refused_without_overwrite (__main__.Contracts.test_real_shell_worker_log_collision_refused_without_overwrite) ... ok
test_realized_native_saved_factors_drive_R_predicate (__main__.Contracts.test_realized_native_saved_factors_drive_R_predicate) ... ok
test_repeat_factor_compared_to_original_native_solution (__main__.Contracts.test_repeat_factor_compared_to_original_native_solution) ... ok
test_restores_optional_recorder_and_preexisting_hook_on_halt (__main__.Contracts.test_restores_optional_recorder_and_preexisting_hook_on_halt) ... ok
test_scope_SHA_drift_refused (__main__.Contracts.test_scope_SHA_drift_refused) ... ok
test_supervisor_timeout_overrides_worker_success_and_preserves_commits (__main__.Contracts.test_supervisor_timeout_overrides_worker_success_and_preserves_commits) ... ok
test_target_failure_retains_completed_prefix_and_NOT_RUN_arm (__main__.Contracts.test_target_failure_retains_completed_prefix_and_NOT_RUN_arm) ... ok
test_target_mutation_halt_retains_offending_value_and_restores_weights (__main__.Contracts.test_target_mutation_halt_retains_offending_value_and_restores_weights) ... ok
test_timeout_publication_preserves_previous_bytes_and_has_terminal_INCONCLUSIVE (__main__.Contracts.test_timeout_publication_preserves_previous_bytes_and_has_terminal_INCONCLUSIVE) ... ok
test_valid_complete_phases_publish_threshold_free_R (__main__.Contracts.test_valid_complete_phases_publish_threshold_free_R) ... ok

======================================================================
FAIL: test_observer_tensor_inertness_catches_discarded_cur_mutation (__main__.Contracts.test_observer_tensor_inertness_catches_discarded_cur_mutation)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 344, in test_observer_tensor_inertness_catches_discarded_cur_mutation
    self.assertTrue((self.root/'operands_A1_single_L4_A.pt').exists())
AssertionError: False is not true

======================================================================
FAIL: test_real_shell_existing_namespace_refused_without_finalizer (__main__.Contracts.test_real_shell_existing_namespace_refused_without_finalizer)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 627, in test_real_shell_existing_namespace_refused_without_finalizer
    self.run_shell_stub('existing')
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 724, in run_shell_stub
    self.assertEqual(child.returncode,3,(child.stdout,child.stderr))
AssertionError: 2 != 3 : ('', 'Existing diagnostic namespace refused before imports.\n/private/tmp/c10y_build/tmpuw560ry6/tools/run_c10y_precast_diag.sh: line 36: kill: (39362) - No such process\n/private/tmp/c10y_build/tmpuw560ry6/tools/run_c10y_precast_diag.sh: line 48: kill: (39362) - No such process\n/private/tmp/c10y_build/tmpuw560ry6/tools/run_c10y_precast_diag.sh: line 48: kill: (39362) - No such process\n')

----------------------------------------------------------------------
Ran 60 tests in 41.124s

FAILED (failures=2)
```

#### Observer-off/finalizer boundary RED — `failure_boundary_RED.log`

Captured command: `env C10Y_ALLOWED_CHILD_TESTS=1 PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 .venv/bin/python -B experiments/track_c/c10y_precast_diag_selftest.py Contracts.test_observer_off_failure_retains_prior_native_input_capture Contracts.test_real_shell_finalizer_abnormal_exit_has_fresh_INCONCLUSIVE_diagnostic > /private/tmp/c10y_build/precast_fix1_20261009T185431Z/failure_boundary_RED.log 2>&1`

```text
test_observer_off_failure_retains_prior_native_input_capture (__main__.Contracts.test_observer_off_failure_retains_prior_native_input_capture) ... FAIL
test_real_shell_finalizer_abnormal_exit_has_fresh_INCONCLUSIVE_diagnostic (__main__.Contracts.test_real_shell_finalizer_abnormal_exit_has_fresh_INCONCLUSIVE_diagnostic) ... ERROR

======================================================================
ERROR: test_real_shell_finalizer_abnormal_exit_has_fresh_INCONCLUSIVE_diagnostic (__main__.Contracts.test_real_shell_finalizer_abnormal_exit_has_fresh_INCONCLUSIVE_diagnostic)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 667, in test_real_shell_finalizer_abnormal_exit_has_fresh_INCONCLUSIVE_diagnostic
    self.run_shell_stub('finalizer_fail')
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 752, in run_shell_stub
    run=json.loads((out/'run.json').read_text());self.assertEqual(run['status'],'INCONCLUSIVE')
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/pathlib.py", line 1058, in read_text
    with self.open(mode='r', encoding=encoding, errors=errors) as f:
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/pathlib.py", line 1044, in open
    return io.open(self, mode, buffering, encoding, errors, newline)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
FileNotFoundError: [Errno 2] No such file or directory: '/private/tmp/c10y_build/tmp11ys2d66/results/c10y_precast_diag/20261009T000000Z/run.json'

======================================================================
FAIL: test_observer_off_failure_retains_prior_native_input_capture (__main__.Contracts.test_observer_off_failure_retains_prior_native_input_capture)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 444, in test_observer_off_failure_retains_prior_native_input_capture
    self.assertTrue((self.root/'solve_inputs_A1_single_L4_A_direct.json').exists())
AssertionError: False is not true

----------------------------------------------------------------------
Ran 2 tests in 1.689s

FAILED (failures=1, errors=1)
```

#### 62-test candidate GREEN — `precast_full_GREEN_attempt2.log`

Captured command: `env C10Y_ALLOWED_CHILD_TESTS=1 PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 .venv/bin/python -B experiments/track_c/c10y_precast_diag_selftest.py > /private/tmp/c10y_build/precast_fix1_20261009T185431Z/precast_full_GREEN_attempt2.log 2>&1`

```text
test_48_targets_computed_once_saved_reloaded_and_shared_by_original_paths (__main__.Contracts.test_48_targets_computed_once_saved_reloaded_and_shared_by_original_paths) ... ok
test_INCONCLUSIVE_precedes_every_other_reading (__main__.Contracts.test_INCONCLUSIVE_precedes_every_other_reading) ... ok
test_R_requires_every_cell_and_A7_device_difference (__main__.Contracts.test_R_requires_every_cell_and_A7_device_difference) ... ok
test_S_needs_direct_trace_evidence_and_K_never_emitted (__main__.Contracts.test_S_needs_direct_trace_evidence_and_K_never_emitted) ... ok
test_actual_representation_batch_padding_and_indices_captured_without_id_assumption (__main__.Contracts.test_actual_representation_batch_padding_and_indices_captured_without_id_assumption) ... ok
test_completed_float64_direct_solution_survives_next_solve_failure (__main__.Contracts.test_completed_float64_direct_solution_survives_next_solve_failure) ... ok
test_completed_native_CPU_product_survives_later_control_halt (__main__.Contracts.test_completed_native_CPU_product_survives_later_control_halt) ... ok
test_device_product_observed_from_original_effective_weight (__main__.Contracts.test_device_product_observed_from_original_effective_weight) ... ok
test_difference_metrics_and_weight_coordinate_columns (__main__.Contracts.test_difference_metrics_and_weight_coordinate_columns) ... ok
test_exclusive_JSON_and_tensor_collision_have_no_sibling (__main__.Contracts.test_exclusive_JSON_and_tensor_collision_have_no_sibling) ... ok
test_fail_closed_gpu_and_fingerprint_records_precede_loader (__main__.Contracts.test_fail_closed_gpu_and_fingerprint_records_precede_loader) ... ok
test_finalizer_incomplete_worker_cannot_publish_R (__main__.Contracts.test_finalizer_incomplete_worker_cannot_publish_R) ... ok
test_finalizer_malformed_worker_preserves_exception_and_inconclusive (__main__.Contracts.test_finalizer_malformed_worker_preserves_exception_and_inconclusive) ... ok
test_finalizer_overwrite_refusal_keeps_terminal_bytes (__main__.Contracts.test_finalizer_overwrite_refusal_keeps_terminal_bytes) ... ok
test_finalizer_rejects_completed_claim_with_incomplete_phases (__main__.Contracts.test_finalizer_rejects_completed_claim_with_incomplete_phases) ... ok
test_float64_realization_cannot_demote_to_float32 (__main__.Contracts.test_float64_realization_cannot_demote_to_float32) ... ok
test_float64_realization_casts_on_CPU_before_device_transfer (__main__.Contracts.test_float64_realization_casts_on_CPU_before_device_transfer) ... ok
test_float64_solve_and_promoted_product_are_distinct (__main__.Contracts.test_float64_solve_and_promoted_product_are_distinct) ... ok
test_forced_native_halt_preserves_capture_and_cleans_weights_globals (__main__.Contracts.test_forced_native_halt_preserves_capture_and_cleans_weights_globals) ... ok
test_fresh_import_is_model_and_torch_free (__main__.Contracts.test_fresh_import_is_model_and_torch_free) ... ok
test_fresh_namespace_existing_directory_and_symlink_refused (__main__.Contracts.test_fresh_namespace_existing_directory_and_symlink_refused) ... ok
test_full_weight_coordinate_quantiles_exceed_torch_limit (__main__.Contracts.test_full_weight_coordinate_quantiles_exceed_torch_limit) ... ok
test_gate_inputs_fsynced_and_reloaded_before_predicate (__main__.Contracts.test_gate_inputs_fsynced_and_reloaded_before_predicate) ... ok
test_genuine_native_operand_discrepancy_remains_valid_S_evidence (__main__.Contracts.test_genuine_native_operand_discrepancy_remains_valid_S_evidence) ... ok
test_interrupted_publication_preserves_prior_bytes_and_is_fresh_INCONCLUSIVE (__main__.Contracts.test_interrupted_publication_preserves_prior_bytes_and_is_fresh_INCONCLUSIVE) ... ok
test_interrupted_serialization_is_incomplete_and_retains_previous_values (__main__.Contracts.test_interrupted_serialization_is_incomplete_and_retains_previous_values) ... ok
test_malformed_classification_capture_is_INCONCLUSIVE (__main__.Contracts.test_malformed_classification_capture_is_INCONCLUSIVE) ... ok
test_missing_capture_refuses_instead_of_reimplementing (__main__.Contracts.test_missing_capture_refuses_instead_of_reimplementing) ... ok
test_missing_reference_Q_retains_available_operands_before_coverage_halt (__main__.Contracts.test_missing_reference_Q_retains_available_operands_before_coverage_halt) ... ok
test_native_direct_solve_failure_retains_inputs_and_original_exception (__main__.Contracts.test_native_direct_solve_failure_retains_inputs_and_original_exception) ... ok
test_native_direct_update_included_in_all_pair_measurements (__main__.Contracts.test_native_direct_update_included_in_all_pair_measurements) ... ok
test_native_factor_actual_matrix_and_Q_are_compared (__main__.Contracts.test_native_factor_actual_matrix_and_Q_are_compared) ... ok
test_native_factor_solve_failure_retains_inputs_and_original_exception (__main__.Contracts.test_native_factor_solve_failure_retains_inputs_and_original_exception) ... ok
test_native_missing_factor_Q_is_inconclusive_capture_failure (__main__.Contracts.test_native_missing_factor_Q_is_inconclusive_capture_failure) ... ok
test_nonfinite_operand_persisted_before_halt (__main__.Contracts.test_nonfinite_operand_persisted_before_halt) ... ok
test_observer_direct_M_mutation_at_return_invalidates_evidence (__main__.Contracts.test_observer_direct_M_mutation_at_return_invalidates_evidence) ... ok
test_observer_factor_Q_copy_mutation_invalidates_evidence (__main__.Contracts.test_observer_factor_Q_copy_mutation_invalidates_evidence) ... ok
test_observer_off_failure_retains_prior_native_input_capture (__main__.Contracts.test_observer_off_failure_retains_prior_native_input_capture) ... ok
test_observer_original_code_coverage_off_on_and_native_operands (__main__.Contracts.test_observer_original_code_coverage_off_on_and_native_operands) ... ok
test_observer_tensor_inertness_catches_discarded_cur_mutation (__main__.Contracts.test_observer_tensor_inertness_catches_discarded_cur_mutation) ... ok
test_packet_tamper_refused_before_downstream_consumption (__main__.Contracts.test_packet_tamper_refused_before_downstream_consumption) ... ok
test_phase_failure_publication_preserves_original_exception (__main__.Contracts.test_phase_failure_publication_preserves_original_exception) ... ok
test_real_shell_existing_namespace_refused_without_finalizer (__main__.Contracts.test_real_shell_existing_namespace_refused_without_finalizer) ... ok
test_real_shell_finalizer_abnormal_exit_has_fresh_INCONCLUSIVE_diagnostic (__main__.Contracts.test_real_shell_finalizer_abnormal_exit_has_fresh_INCONCLUSIVE_diagnostic) ... ok
test_real_shell_finalizer_timeout_has_fresh_supervisor_diagnostic (__main__.Contracts.test_real_shell_finalizer_timeout_has_fresh_supervisor_diagnostic) ... ok
test_real_shell_supervisor_HUP_cleans_owned_worker_and_publishes_INCONCLUSIVE (__main__.Contracts.test_real_shell_supervisor_HUP_cleans_owned_worker_and_publishes_INCONCLUSIVE) ... ok
test_real_shell_supervisor_INT_cleans_owned_worker_and_publishes_INCONCLUSIVE (__main__.Contracts.test_real_shell_supervisor_INT_cleans_owned_worker_and_publishes_INCONCLUSIVE) ... ok
test_real_shell_supervisor_TERM_cleans_owned_worker_and_publishes_INCONCLUSIVE (__main__.Contracts.test_real_shell_supervisor_TERM_cleans_owned_worker_and_publishes_INCONCLUSIVE) ... ok
test_real_shell_supervisor_abnormal_exit_cleans_owned_worker_and_publishes_INCONCLUSIVE (__main__.Contracts.test_real_shell_supervisor_abnormal_exit_cleans_owned_worker_and_publishes_INCONCLUSIVE) ... ok
test_real_shell_supervisor_hanging_stub_preserves_timeout_and_kills_worker (__main__.Contracts.test_real_shell_supervisor_hanging_stub_preserves_timeout_and_kills_worker) ... ok
test_real_shell_supervisor_setup_timeout_retains_owned_namespace_diagnostic (__main__.Contracts.test_real_shell_supervisor_setup_timeout_retains_owned_namespace_diagnostic) ... ok
test_real_shell_supervisor_worker_exit_before_start_is_diagnosed (__main__.Contracts.test_real_shell_supervisor_worker_exit_before_start_is_diagnosed) ... ok
test_real_shell_worker_log_collision_refused_without_overwrite (__main__.Contracts.test_real_shell_worker_log_collision_refused_without_overwrite) ... ok
test_realized_native_saved_factors_drive_R_predicate (__main__.Contracts.test_realized_native_saved_factors_drive_R_predicate) ... ok
test_repeat_factor_compared_to_original_native_solution (__main__.Contracts.test_repeat_factor_compared_to_original_native_solution) ... ok
test_restores_optional_recorder_and_preexisting_hook_on_halt (__main__.Contracts.test_restores_optional_recorder_and_preexisting_hook_on_halt) ... ok
test_scope_SHA_drift_refused (__main__.Contracts.test_scope_SHA_drift_refused) ... ok
test_supervisor_timeout_overrides_worker_success_and_preserves_commits (__main__.Contracts.test_supervisor_timeout_overrides_worker_success_and_preserves_commits) ... ok
test_target_failure_retains_completed_prefix_and_NOT_RUN_arm (__main__.Contracts.test_target_failure_retains_completed_prefix_and_NOT_RUN_arm) ... ok
test_target_mutation_halt_retains_offending_value_and_restores_weights (__main__.Contracts.test_target_mutation_halt_retains_offending_value_and_restores_weights) ... ok
test_timeout_publication_preserves_previous_bytes_and_has_terminal_INCONCLUSIVE (__main__.Contracts.test_timeout_publication_preserves_previous_bytes_and_has_terminal_INCONCLUSIVE) ... ok
test_valid_complete_phases_publish_threshold_free_R (__main__.Contracts.test_valid_complete_phases_publish_threshold_free_R) ... ok

----------------------------------------------------------------------
Ran 62 tests in 47.947s

OK
```

#### Fsync/descendant/publication boundary probes — `supervisor_boundary_RED.log`

Captured command: `env C10Y_ALLOWED_CHILD_TESTS=1 PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 .venv/bin/python -B experiments/track_c/c10y_precast_diag_selftest.py Contracts.test_actual_native_solve_inputs_are_fsynced_before_execution Contracts.test_real_shell_owned_process_group_is_stopped_after_leader_exit Contracts.test_real_shell_interrupted_publisher_timeout_remains_armed_and_is_diagnosed > /private/tmp/c10y_build/precast_fix1_20261009T185431Z/supervisor_boundary_RED.log 2>&1`

```text
test_actual_native_solve_inputs_are_fsynced_before_execution (__main__.Contracts.test_actual_native_solve_inputs_are_fsynced_before_execution) ... ok
test_real_shell_owned_process_group_is_stopped_after_leader_exit (__main__.Contracts.test_real_shell_owned_process_group_is_stopped_after_leader_exit) ... FAIL
test_real_shell_interrupted_publisher_timeout_remains_armed_and_is_diagnosed (__main__.Contracts.test_real_shell_interrupted_publisher_timeout_remains_armed_and_is_diagnosed) ... ERROR

======================================================================
ERROR: test_real_shell_interrupted_publisher_timeout_remains_armed_and_is_diagnosed (__main__.Contracts.test_real_shell_interrupted_publisher_timeout_remains_armed_and_is_diagnosed)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 698, in test_real_shell_interrupted_publisher_timeout_remains_armed_and_is_diagnosed
    self.run_shell_stub('interrupt_publication_hang')
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 770, in run_shell_stub
    value=json.loads((out/('supervisor_timeout.json' if mode=='interrupt_publication_hang' else 'supervisor_interruption.json')).read_text())
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/pathlib.py", line 1058, in read_text
    with self.open(mode='r', encoding=encoding, errors=errors) as f:
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/pathlib.py", line 1044, in open
    return io.open(self, mode, buffering, encoding, errors, newline)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
FileNotFoundError: [Errno 2] No such file or directory: '/private/tmp/c10y_build/tmp77h0bthg/results/c10y_precast_diag/20261009T000000Z/supervisor_timeout.json'

======================================================================
FAIL: test_real_shell_owned_process_group_is_stopped_after_leader_exit (__main__.Contracts.test_real_shell_owned_process_group_is_stopped_after_leader_exit)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 695, in test_real_shell_owned_process_group_is_stopped_after_leader_exit
    self.run_shell_stub('leader_exit')
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 801, in run_shell_stub
    else:self.assertTrue((out/'supervisor_halt.json').exists())
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: False is not true

----------------------------------------------------------------------
Ran 3 tests in 7.478s

FAILED (failures=1, errors=1)
```

#### Boundary candidate GREEN — `supervisor_boundary_GREEN_attempt1.log`

Captured command: `env C10Y_ALLOWED_CHILD_TESTS=1 PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 .venv/bin/python -B experiments/track_c/c10y_precast_diag_selftest.py Contracts.test_actual_native_solve_inputs_are_fsynced_before_execution Contracts.test_real_shell_owned_process_group_is_stopped_after_leader_exit Contracts.test_real_shell_interrupted_publisher_timeout_remains_armed_and_is_diagnosed > /private/tmp/c10y_build/precast_fix1_20261009T185431Z/supervisor_boundary_GREEN_attempt1.log 2>&1`

```text
test_actual_native_solve_inputs_are_fsynced_before_execution (__main__.Contracts.test_actual_native_solve_inputs_are_fsynced_before_execution) ... ok
test_real_shell_owned_process_group_is_stopped_after_leader_exit (__main__.Contracts.test_real_shell_owned_process_group_is_stopped_after_leader_exit) ... ok
test_real_shell_interrupted_publisher_timeout_remains_armed_and_is_diagnosed (__main__.Contracts.test_real_shell_interrupted_publisher_timeout_remains_armed_and_is_diagnosed) ... ok

----------------------------------------------------------------------
Ran 3 tests in 7.713s

OK
```

#### FINAL diagnostic GREEN — `precast_full_GREEN_final.log`

Captured command: `env C10Y_ALLOWED_CHILD_TESTS=1 PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 .venv/bin/python -B experiments/track_c/c10y_precast_diag_selftest.py > /private/tmp/c10y_build/precast_fix1_20261009T185431Z/precast_full_GREEN_final.log 2>&1`

```text
test_48_targets_computed_once_saved_reloaded_and_shared_by_original_paths (__main__.Contracts.test_48_targets_computed_once_saved_reloaded_and_shared_by_original_paths) ... ok
test_INCONCLUSIVE_precedes_every_other_reading (__main__.Contracts.test_INCONCLUSIVE_precedes_every_other_reading) ... ok
test_R_requires_every_cell_and_A7_device_difference (__main__.Contracts.test_R_requires_every_cell_and_A7_device_difference) ... ok
test_S_needs_direct_trace_evidence_and_K_never_emitted (__main__.Contracts.test_S_needs_direct_trace_evidence_and_K_never_emitted) ... ok
test_actual_native_solve_inputs_are_fsynced_before_execution (__main__.Contracts.test_actual_native_solve_inputs_are_fsynced_before_execution) ... ok
test_actual_representation_batch_padding_and_indices_captured_without_id_assumption (__main__.Contracts.test_actual_representation_batch_padding_and_indices_captured_without_id_assumption) ... ok
test_completed_float64_direct_solution_survives_next_solve_failure (__main__.Contracts.test_completed_float64_direct_solution_survives_next_solve_failure) ... ok
test_completed_native_CPU_product_survives_later_control_halt (__main__.Contracts.test_completed_native_CPU_product_survives_later_control_halt) ... ok
test_device_product_observed_from_original_effective_weight (__main__.Contracts.test_device_product_observed_from_original_effective_weight) ... ok
test_difference_metrics_and_weight_coordinate_columns (__main__.Contracts.test_difference_metrics_and_weight_coordinate_columns) ... ok
test_exclusive_JSON_and_tensor_collision_have_no_sibling (__main__.Contracts.test_exclusive_JSON_and_tensor_collision_have_no_sibling) ... ok
test_fail_closed_gpu_and_fingerprint_records_precede_loader (__main__.Contracts.test_fail_closed_gpu_and_fingerprint_records_precede_loader) ... ok
test_finalizer_incomplete_worker_cannot_publish_R (__main__.Contracts.test_finalizer_incomplete_worker_cannot_publish_R) ... ok
test_finalizer_malformed_worker_preserves_exception_and_inconclusive (__main__.Contracts.test_finalizer_malformed_worker_preserves_exception_and_inconclusive) ... ok
test_finalizer_overwrite_refusal_keeps_terminal_bytes (__main__.Contracts.test_finalizer_overwrite_refusal_keeps_terminal_bytes) ... ok
test_finalizer_rejects_completed_claim_with_incomplete_phases (__main__.Contracts.test_finalizer_rejects_completed_claim_with_incomplete_phases) ... ok
test_float64_realization_cannot_demote_to_float32 (__main__.Contracts.test_float64_realization_cannot_demote_to_float32) ... ok
test_float64_realization_casts_on_CPU_before_device_transfer (__main__.Contracts.test_float64_realization_casts_on_CPU_before_device_transfer) ... ok
test_float64_solve_and_promoted_product_are_distinct (__main__.Contracts.test_float64_solve_and_promoted_product_are_distinct) ... ok
test_forced_native_halt_preserves_capture_and_cleans_weights_globals (__main__.Contracts.test_forced_native_halt_preserves_capture_and_cleans_weights_globals) ... ok
test_fresh_import_is_model_and_torch_free (__main__.Contracts.test_fresh_import_is_model_and_torch_free) ... ok
test_fresh_namespace_existing_directory_and_symlink_refused (__main__.Contracts.test_fresh_namespace_existing_directory_and_symlink_refused) ... ok
test_full_weight_coordinate_quantiles_exceed_torch_limit (__main__.Contracts.test_full_weight_coordinate_quantiles_exceed_torch_limit) ... ok
test_gate_inputs_fsynced_and_reloaded_before_predicate (__main__.Contracts.test_gate_inputs_fsynced_and_reloaded_before_predicate) ... ok
test_genuine_native_operand_discrepancy_remains_valid_S_evidence (__main__.Contracts.test_genuine_native_operand_discrepancy_remains_valid_S_evidence) ... ok
test_interrupted_publication_preserves_prior_bytes_and_is_fresh_INCONCLUSIVE (__main__.Contracts.test_interrupted_publication_preserves_prior_bytes_and_is_fresh_INCONCLUSIVE) ... ok
test_interrupted_serialization_is_incomplete_and_retains_previous_values (__main__.Contracts.test_interrupted_serialization_is_incomplete_and_retains_previous_values) ... ok
test_malformed_classification_capture_is_INCONCLUSIVE (__main__.Contracts.test_malformed_classification_capture_is_INCONCLUSIVE) ... ok
test_missing_capture_refuses_instead_of_reimplementing (__main__.Contracts.test_missing_capture_refuses_instead_of_reimplementing) ... ok
test_missing_reference_Q_retains_available_operands_before_coverage_halt (__main__.Contracts.test_missing_reference_Q_retains_available_operands_before_coverage_halt) ... ok
test_native_direct_solve_failure_retains_inputs_and_original_exception (__main__.Contracts.test_native_direct_solve_failure_retains_inputs_and_original_exception) ... ok
test_native_direct_update_included_in_all_pair_measurements (__main__.Contracts.test_native_direct_update_included_in_all_pair_measurements) ... ok
test_native_factor_actual_matrix_and_Q_are_compared (__main__.Contracts.test_native_factor_actual_matrix_and_Q_are_compared) ... ok
test_native_factor_solve_failure_retains_inputs_and_original_exception (__main__.Contracts.test_native_factor_solve_failure_retains_inputs_and_original_exception) ... ok
test_native_missing_factor_Q_is_inconclusive_capture_failure (__main__.Contracts.test_native_missing_factor_Q_is_inconclusive_capture_failure) ... ok
test_nonfinite_operand_persisted_before_halt (__main__.Contracts.test_nonfinite_operand_persisted_before_halt) ... ok
test_observer_direct_M_mutation_at_return_invalidates_evidence (__main__.Contracts.test_observer_direct_M_mutation_at_return_invalidates_evidence) ... ok
test_observer_factor_Q_copy_mutation_invalidates_evidence (__main__.Contracts.test_observer_factor_Q_copy_mutation_invalidates_evidence) ... ok
test_observer_off_failure_retains_prior_native_input_capture (__main__.Contracts.test_observer_off_failure_retains_prior_native_input_capture) ... ok
test_observer_original_code_coverage_off_on_and_native_operands (__main__.Contracts.test_observer_original_code_coverage_off_on_and_native_operands) ... ok
test_observer_tensor_inertness_catches_discarded_cur_mutation (__main__.Contracts.test_observer_tensor_inertness_catches_discarded_cur_mutation) ... ok
test_packet_tamper_refused_before_downstream_consumption (__main__.Contracts.test_packet_tamper_refused_before_downstream_consumption) ... ok
test_phase_failure_publication_preserves_original_exception (__main__.Contracts.test_phase_failure_publication_preserves_original_exception) ... ok
test_real_shell_existing_namespace_refused_without_finalizer (__main__.Contracts.test_real_shell_existing_namespace_refused_without_finalizer) ... ok
test_real_shell_finalizer_abnormal_exit_has_fresh_INCONCLUSIVE_diagnostic (__main__.Contracts.test_real_shell_finalizer_abnormal_exit_has_fresh_INCONCLUSIVE_diagnostic) ... ok
test_real_shell_finalizer_timeout_has_fresh_supervisor_diagnostic (__main__.Contracts.test_real_shell_finalizer_timeout_has_fresh_supervisor_diagnostic) ... ok
test_real_shell_interrupted_publisher_timeout_remains_armed_and_is_diagnosed (__main__.Contracts.test_real_shell_interrupted_publisher_timeout_remains_armed_and_is_diagnosed) ... ok
test_real_shell_owned_process_group_is_stopped_after_leader_exit (__main__.Contracts.test_real_shell_owned_process_group_is_stopped_after_leader_exit) ... ok
test_real_shell_supervisor_HUP_cleans_owned_worker_and_publishes_INCONCLUSIVE (__main__.Contracts.test_real_shell_supervisor_HUP_cleans_owned_worker_and_publishes_INCONCLUSIVE) ... ok
test_real_shell_supervisor_INT_cleans_owned_worker_and_publishes_INCONCLUSIVE (__main__.Contracts.test_real_shell_supervisor_INT_cleans_owned_worker_and_publishes_INCONCLUSIVE) ... ok
test_real_shell_supervisor_TERM_cleans_owned_worker_and_publishes_INCONCLUSIVE (__main__.Contracts.test_real_shell_supervisor_TERM_cleans_owned_worker_and_publishes_INCONCLUSIVE) ... ok
test_real_shell_supervisor_abnormal_exit_cleans_owned_worker_and_publishes_INCONCLUSIVE (__main__.Contracts.test_real_shell_supervisor_abnormal_exit_cleans_owned_worker_and_publishes_INCONCLUSIVE) ... ok
test_real_shell_supervisor_hanging_stub_preserves_timeout_and_kills_worker (__main__.Contracts.test_real_shell_supervisor_hanging_stub_preserves_timeout_and_kills_worker) ... ok
test_real_shell_supervisor_setup_timeout_retains_owned_namespace_diagnostic (__main__.Contracts.test_real_shell_supervisor_setup_timeout_retains_owned_namespace_diagnostic) ... ok
test_real_shell_supervisor_worker_exit_before_start_is_diagnosed (__main__.Contracts.test_real_shell_supervisor_worker_exit_before_start_is_diagnosed) ... ok
test_real_shell_worker_log_collision_refused_without_overwrite (__main__.Contracts.test_real_shell_worker_log_collision_refused_without_overwrite) ... ok
test_realized_native_saved_factors_drive_R_predicate (__main__.Contracts.test_realized_native_saved_factors_drive_R_predicate) ... ok
test_repeat_factor_compared_to_original_native_solution (__main__.Contracts.test_repeat_factor_compared_to_original_native_solution) ... ok
test_restores_optional_recorder_and_preexisting_hook_on_halt (__main__.Contracts.test_restores_optional_recorder_and_preexisting_hook_on_halt) ... ok
test_scope_SHA_drift_refused (__main__.Contracts.test_scope_SHA_drift_refused) ... ok
test_supervisor_timeout_overrides_worker_success_and_preserves_commits (__main__.Contracts.test_supervisor_timeout_overrides_worker_success_and_preserves_commits) ... ok
test_target_failure_retains_completed_prefix_and_NOT_RUN_arm (__main__.Contracts.test_target_failure_retains_completed_prefix_and_NOT_RUN_arm) ... ok
test_target_mutation_halt_retains_offending_value_and_restores_weights (__main__.Contracts.test_target_mutation_halt_retains_offending_value_and_restores_weights) ... ok
test_timeout_publication_preserves_previous_bytes_and_has_terminal_INCONCLUSIVE (__main__.Contracts.test_timeout_publication_preserves_previous_bytes_and_has_terminal_INCONCLUSIVE) ... ok
test_valid_complete_phases_publish_threshold_free_R (__main__.Contracts.test_valid_complete_phases_publish_threshold_free_R) ... ok

----------------------------------------------------------------------
Ran 65 tests in 43.331s

OK
```

#### FINAL existing C10Y GREEN — `c10y_full_GREEN_final.log`

Captured command: `env C10Y_ALLOWED_CHILD_TESTS=1 PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 .venv/bin/python -B experiments/track_c/c10y_directdw_selftest.py > /private/tmp/c10y_build/precast_fix1_20261009T185431Z/c10y_full_GREEN_final.log 2>&1`

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
Ran 285 tests in 24.825s

OK
{"launched": false, "reasons": ["missing/unknown/duplicate phases"], "status": "UNVERIFIED"}
ISOLATION OWNED LISTING DRIFT: []
ISOLATION OTHER OBSERVED UNATTRIBUTED: ["results/mathlab/harvest_launch_20261009T184919Z.log", "results/mathlab_staging/runs/harvest_20261009T184932Z_95961/events.jsonl"]
SYS_MODULES_FORBIDDEN: []
C10Y_DIRECTDW_SELFTEST PASS — CPU ONLY; LIVE LAW#3/LAW#5 UNVERIFIED
```

#### Initial audit surfaces source mismatch — `source_pin_audit_initial_fail.log`

Read-only audit command: `env PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B /private/tmp/c10y_build/precast_fix1_20261009T185431Z/audit_fix1.py` (initial audit asserted all pins; final audit records the explicit mismatch).

```text
Traceback (most recent call last):
  File "/private/tmp/c10y_build/precast_fix1_20261009T185431Z/audit_fix1.py", line 15, in <module>
    assert all(value['matched'] for value in pins.values()),pins
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: {'docs/C10Y_PRECAST_DIAG_SCOPE.md': {'expected': '097c662803a94a897dd588c9e1f09c6af7b17a25019c1439ea39844c65f0a9a8', 'actual': '097c662803a94a897dd588c9e1f09c6af7b17a25019c1439ea39844c65f0a9a8', 'matched': True}, 'docs/C10Y_DIRECTDW_PREREG.md': {'expected': '005391a39e31d8174419de3e39078a42209ded1b7ab8caaf098d5d8a4f755004', 'actual': '005391a39e31d8174419de3e39078a42209ded1b7ab8caaf098d5d8a4f755004', 'matched': True}, 'experiments/track_c/c10y_directdw_arms.py': {'expected': 'ead3cef2266a7c81035e5acb6c3a97b42f83da556ba093a9fd28ec403f7e158c', 'actual': 'ead3cef2266a7c81035e5acb6c3a97b42f83da556ba093a9fd28ec403f7e158c', 'matched': True}, 'experiments/track_c/c10e_bandknob.py': {'expected': '1f6be5811d7e58f3ebda16867a4a174b1cf24d47f9a2514cf9c3f9d29f18e695', 'actual': '1f6be5811d7e58f3ebda16867a4a174b1cf24d47f9a2514cf9c3f9d29f18e695', 'matched': True}, 'experiments/track_c/c10z_astra_benchmark.py': {'expected': '9b25a207f630fbfa0d60c80a74f22289ad3bb2cc160d0fc72d7e0367f9a47a1a', 'actual': '3703d8b9c363bb06eab0ca66f38f4b01114363ae75a9d0397701e75aa2520041', 'matched': False}, 'configs/hparams/qwen25_3b_memit_hparams.json': {'expected': '4225cc6aabc3eb9fa62d2bb2cac68b1238de3a39c5e469da635e6e1464aa3bb4', 'actual': '4225cc6aabc3eb9fa62d2bb2cac68b1238de3a39c5e469da635e6e1464aa3bb4', 'matched': True}, 'configs/screens/g6_screen_qwen3b_v2.json': {'expected': '482c05f8f33c59d3e469566fe6f3c48eb183d3cb2fbb791f31dcad7102517c5c', 'actual': '482c05f8f33c59d3e469566fe6f3c48eb183d3cb2fbb791f31dcad7102517c5c', 'matched': True}, 'memit_dry_run/memit/memit/compute_z.py': {'expected': 'd94af7fa14e5a4a20d5fa6361e0cbb30da0ff957db31922557ff809c34205dea', 'actual': 'd94af7fa14e5a4a20d5fa6361e0cbb30da0ff957db31922557ff809c34205dea', 'matched': True}, 'memit_dry_run/memit/memit/compute_ks.py': {'expected': '0b039be47c548f046b71cad4efce63414f53edbaa657bde868a20cdd35a2f5c7', 'actual': '0b039be47c548f046b71cad4efce63414f53edbaa657bde868a20cdd35a2f5c7', 'matched': True}, 'memit_dry_run/memit/rome/repr_tools.py': {'expected': 'd4c2324ba20cbcce7f4ccfcf58ad002912edf0ad2fc72ab4e9bf46cc9dfed336', 'actual': 'd4c2324ba20cbcce7f4ccfcf58ad002912edf0ad2fc72ab4e9bf46cc9dfed336', 'matched': True}, 'memit_dry_run/memit/memit/memit_main.py': {'expected': 'd941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65', 'actual': 'd941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65', 'matched': True}, 'tools/engine_fingerprint.py': {'expected': '450ee83ac829817299ead301c4a3d20702f431deaea4be58c77ecfd89a329162', 'actual': '450ee83ac829817299ead301c4a3d20702f431deaea4be58c77ecfd89a329162', 'matched': True}, 'tools/c10w_p2_gate.py': {'expected': 'fb6568a6e159e84b22971aa893c3a83bcaaa16085f4abd9c76ca50b4a3362a26', 'actual': 'fb6568a6e159e84b22971aa893c3a83bcaaa16085f4abd9c76ca50b4a3362a26', 'matched': True}}
```

#### Final audit, CPU checks PASS; source-pin GATED explicitly — `audit_before_append.log`

Read-only audit command: `env PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B /private/tmp/c10y_build/precast_fix1_20261009T185431Z/audit_fix1.py` (initial audit asserted all pins; final audit records the explicit mismatch).

```text
{
  "branch_observed": "worktree-c10k-route-a",
  "checks": [
    "12 of 13 source pins match; C10Z benchmark mismatch explicitly retained",
    "Scope matches frozen commit 4f7b22c",
    "Python compile in memory PASS",
    "Bash syntax PASS",
    "Report prefix retained",
    "No live diagnostic namespace",
    "Deadline cap unchanged; armed before imports; cancelled after cleanup"
  ],
  "diag_count": 65,
  "existing_count": 285,
  "forbidden_modules": [],
  "head_observed": "a226f3e5b845480e18fd7dbcab24978d65f2f571",
  "live_diag_namespace_exists": false,
  "original_report_prefix_bytes": 219023,
  "original_report_prefix_sha256": "e48c4c7507151027f7efb0d788a540586249ffda01941dd174fa0ae00caa117d",
  "owned_code": {
    "experiments/track_c/c10y_precast_diag.py": "520939b5c49376d5ebfa7c219d905e617881851d6c569071eee3523d0fa91ee9",
    "experiments/track_c/c10y_precast_diag_selftest.py": "af562e602fdbaeab48a7a897a3f823cd763f5282c9dc2c7a004b5ef221254b88",
    "tools/run_c10y_precast_diag.sh": "a2f4c05cfc62af32d5645115b635d6b4330faeca72d34e3a6d9737267aa15396"
  },
  "protected_count": 156,
  "protected_drift": {},
  "review_sha256": "07ec28907fa086636570cca17f15a98170dcf776a80c29ad3de54c9708708885",
  "scope_blob_sha256": "097c662803a94a897dd588c9e1f09c6af7b17a25019c1439ea39844c65f0a9a8",
  "source_pin_mismatches": {
    "experiments/track_c/c10z_astra_benchmark.py": {
      "actual": "3703d8b9c363bb06eab0ca66f38f4b01114363ae75a9d0397701e75aa2520041",
      "expected": "9b25a207f630fbfa0d60c80a74f22289ad3bb2cc160d0fc72d7e0367f9a47a1a",
      "matched": false
    }
  },
  "source_pin_status": "GATED: C10Z benchmark source mismatch; existing pin retained",
  "total_count": 350,
  "worktree_observed": "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a"
}
```

Fix round 1 builder status: **PRECAST FIX DONE**. Three implementation blockers addressed with retained RED/GREEN CPU evidence; source identity remains fail-closed and launch is GATED. No production execution performed.

## Fix round 2 — 2026-10-09

Recorded 2026-10-09T20:01:38Z by Codex Y2. Read Astra r2 in full:
`results/c10y_directdw_calib4/precast_impl_astra_r2.md`, SHA-256 `1879bacc7660dfc48c59741451b779b93ce4b54188cb3a082fc42b9a6416a7d4`.
Scope SHA was reverified before edits: `097c662803a94a897dd588c9e1f09c6af7b17a25019c1439ea39844c65f0a9a8` (FROZEN v2 unchanged).

**Build result: FIX2 CPU PASS; 68/68 diagnostic and 285/285 existing C10Y tests. Production NOT-RUN.**
This addresses the remaining B3 finding with Astra's explicitly permitted fail-closed option. The shell installs TERM/INT/HUP handlers, verifies the actual `trap -p` commands, and refuses unavailable handlers before creating control state or starting any owned deadline, preparation, or worker process. Refusal returns 3 and prints `INCONCLUSIVE: SIGNAL-TRAP-UNAVAILABLE <signal>; phases NOT-RUN; no owned child launched.` No diagnostic namespace is created on this early refusal. It does not reset the caller's inherited signal dispositions.

Cleanup registration now precedes the first owned child: the unchanged deadline body starts after the EXIT handler is registered. `TIMER_PID` starts empty so early closeout safely handles a deadline that has not started. The cap remains 2,820 seconds; SECONDS starts before the trap guard and the initial deadline sleep subtracts setup elapsed time. The deadline remains armed through TERM→KILL, reap, and terminal publication, and is cancelled last. It starts before the first Python import/preparation child. B1/B2 implementation bytes remain unchanged.

Requirement → test → implementation:

| Requirement | CPU evidence | Implementation |
|---|---|---|
| Inherited ignored HUP refuses before owned timer/prepare/worker | `Contracts.test_inherited_ignored_HUP_refused_before_owned_children` (`experiments/track_c/c10y_precast_diag_selftest.py:688`) | `tools/run_c10y_precast_diag.sh:7`, `:13`: verify installed trap command; exit 3 with INCONCLUSIVE/NOT-RUN on failure |
| Inherited ignored INT refuses before owned timer/prepare/worker | `Contracts.test_inherited_ignored_INT_refused_before_owned_children` (`experiments/track_c/c10y_precast_diag_selftest.py:691`) | `tools/run_c10y_precast_diag.sh:7`, `:13`: verify installed trap command; exit 3 with INCONCLUSIVE/NOT-RUN on failure |
| Inherited ignored TERM refuses before owned timer/prepare/worker | `Contracts.test_inherited_ignored_TERM_refused_before_owned_children` (`experiments/track_c/c10y_precast_diag_selftest.py:694`) | `tools/run_c10y_precast_diag.sh:7`, `:13`: verify installed trap command; exit 3 with INCONCLUSIVE/NOT-RUN on failure |
| Test inheritance rather than merely reset the normal fixture | `run_shell_stub` at `experiments/track_c/c10y_precast_diag_selftest.py:729` executes a temporary stdlib controller which writes the selected SIG_IGN disposition, then execs the actual copied Bash supervisor with that disposition intact. Each new control asserts it inherited SIG_IGN, return code 3, matching refusal reason, no namespace/timer/prepare marker, and completion under 2 seconds. | Production trap verification above; these controls failed on the prior production shell and passed after its change. |
| Preserve actual default-disposition interruption handling | Existing real-shell TERM, INT, HUP interruption tests, abnormal exit, finalizer failure, and process-group cleanup after leader exit all pass in the 68-test suite. Normal fixtures explicitly set all three dispositions to SIG_DFL before exec, then send the tested signal to the same supervisor PID. | `on_signal` at shell `:8`; `closeout` at `:96`; `cleanup_owned` at `:68`. |
| Deadline armed through cleanup/publication; cancellation last | Existing hanging-worker, preparation, finalizer, and interrupted-publication controls pass; publication checks that the timer PID is still alive. Static ordering check PASS. | `trap closeout EXIT` at `:116`, deadline at `:135`, first Python child at `:160`, cancellation at `:113`. |
| Keep B1/B2 fixed and prevent observer changes from becoming S | Direct/factor solve failures, pre-solve fsync, original-exception preservation, observer mutation rejection, and genuine native discrepancy controls all rerun and pass. | `c10y_precast_diag.py` remains `520939b5c49376d5ebfa7c219d905e617881851d6c569071eee3523d0fa91ee9`; no Python diagnostic edit this round. |
| No benchmark repin until the specified handoff | Exact diagnostic file SHA and SOURCE_PINS AST check unchanged. | Benchmark pin remains `9b25a207f630fbfa0d60c80a74f22289ad3bb2cc160d0fc72d7e0367f9a47a1a`. No pin or source-identity gate changes. |
| CPU isolation; no protected science edits | Existing suite reports `ISOLATION OWNED LISTING DRIFT: []` and `SYS_MODULES_FORBIDDEN: []`; temporary shell workers only. 158 protected files compared: 157 unchanged, one shared runbook drift preserved and recorded below. | Only the launcher, diagnostic selftest, and this report changed for Fix round 2; no model/GPU/MPS, production launch, engine/harness edit, or commit performed by this builder. |

Test-first evidence: tests and controlled fixtures were added before changing the production launcher. RED ran four controls: all three ignored-signal controls failed (HUP/INT returned 2 and had already started namespace/timer/prepare; ignored TERM returned -9); the default HUP control passed. This demonstrates the bug independently of a test environment reset. The same four controls passed after the fix. Complete raw outputs appear below, including RED exceptions and the existing suite's CPU warning.

| Run | Exit | Result | Measured unittest runtime |
|---|---:|---|---:|
| Inherited-signal RED + HUP positive control | 1 | 3 failures / 4 controls | 17.324 s |
| Same focused GREEN | 0 | 4/4 PASS | 2.389 s |
| Full diagnostic GREEN | 0 | 68/68 PASS | 45.717 s |
| Existing C10Y GREEN | 0 | 285/285 PASS | 25.675 s |
| Bash syntax | 0 | PASS | — |
| Python source compile without bytecode/model imports | 0 | PASS | — |

Exact executed test commands (serial CPU suites):

```sh
# Run from /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a
# RED: added regression tests and controlled fixture; production shell still at r1 SHA.
/opt/homebrew/bin/rtk proxy env C10Y_ALLOWED_CHILD_TESTS=1 PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 .venv/bin/python -B experiments/track_c/c10y_precast_diag_selftest.py Contracts.test_inherited_ignored_HUP_refused_before_owned_children Contracts.test_inherited_ignored_INT_refused_before_owned_children Contracts.test_inherited_ignored_TERM_refused_before_owned_children Contracts.test_real_shell_supervisor_HUP_cleans_owned_worker_and_publishes_INCONCLUSIVE > /private/tmp/c10y_build/precast_fix2_20261009T194529Z/inherited_RED.log 2>&1
# GREEN: same four controls after the shell fix.
/opt/homebrew/bin/rtk proxy env C10Y_ALLOWED_CHILD_TESTS=1 PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 .venv/bin/python -B experiments/track_c/c10y_precast_diag_selftest.py Contracts.test_inherited_ignored_HUP_refused_before_owned_children Contracts.test_inherited_ignored_INT_refused_before_owned_children Contracts.test_inherited_ignored_TERM_refused_before_owned_children Contracts.test_real_shell_supervisor_HUP_cleans_owned_worker_and_publishes_INCONCLUSIVE > /private/tmp/c10y_build/precast_fix2_20261009T194529Z/inherited_GREEN.log 2>&1
/opt/homebrew/bin/rtk proxy env C10Y_ALLOWED_CHILD_TESTS=1 PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 .venv/bin/python -B experiments/track_c/c10y_precast_diag_selftest.py > /private/tmp/c10y_build/precast_fix2_20261009T194529Z/precast_full_GREEN_final.log 2>&1
/opt/homebrew/bin/rtk proxy env C10Y_ALLOWED_CHILD_TESTS=1 PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 .venv/bin/python -B experiments/track_c/c10y_directdw_selftest.py > /private/tmp/c10y_build/precast_fix2_20261009T194529Z/c10y_full_GREEN_final.log 2>&1
/opt/homebrew/bin/rtk proxy bash -n tools/run_c10y_precast_diag.sh
/opt/homebrew/bin/rtk proxy env PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B /private/tmp/c10y_build/precast_fix2_20261009T194529Z/audit_fix2.py
```

File SHA-256 values:

| File | Before Fix round 2 | After Fix round 2 |
|---|---|---|
| `experiments/track_c/c10y_precast_diag.py` | `520939b5c49376d5ebfa7c219d905e617881851d6c569071eee3523d0fa91ee9` | `520939b5c49376d5ebfa7c219d905e617881851d6c569071eee3523d0fa91ee9` |
| `experiments/track_c/c10y_precast_diag_selftest.py` | `af562e602fdbaeab48a7a897a3f823cd763f5282c9dc2c7a004b5ef221254b88` | `2f66f89e250013ee4d0cffb0627f93652a8dee2ab56c6d0385f999a4a1ad99a7` |
| `tools/run_c10y_precast_diag.sh` | `a2f4c05cfc62af32d5645115b635d6b4330faeca72d34e3a6d9737267aa15396` | `2f34a35aab954ae442d4e812208a1d0b5a79e072f590df119dc0ac7e44c34c37` |

The prior report's complete 349,415-byte prefix is preserved, SHA-256 `55b917b4ed1c521b6272a35b05a2c6c1bd4521ab73791c25b68b1ebad6cfdbb4`. This section is append-only. The frozen scope, preregistration, recordfix primitives, engine/fingerprint, calibration artifacts, CORPUS, ledgers, and checkpoint match the before snapshot. The current working benchmark file hashes to `3703d8b9c363bb06eab0ca66f38f4b01114363ae75a9d0397701e75aa2520041`; its pinned value remains `9b25a207f630fbfa0d60c80a74f22289ad3bb2cc160d0fc72d7e0367f9a47a1a`. Consequently production remains gated by source identity. Benchmark repinning is intentionally deferred until the ASTRA A1 commit and MAESTRO's explicit next step; no acceptance proof or repin is claimed here.

Shared-worktree observation: `EXPERIMENT_RUNBOOK.md` changed from `24ad49597a7b9643ccff0005e437f26b02271fece3f04f4567f4e48a1a04bb85` to `7da856979ea0501e770d0234b2d0bcbd09c64f577b87f2934fa6bbab56a3bd37` during this round. Its working tree diff was empty at audit; the latest path commit was `ed6cdf4` (`D-ML-3: math-lab §15 NORM-CONTRACT FROZEN`). This builder did not edit, revert, or commit it. The existing selftest separately observed unattributed `results/mathlab_staging/runs/m2_20261009T192821Z_82233/events.jsonl` drift while reporting zero owned listing drift. Neither observation is omitted or treated as a global clean-tree claim.

Exact future production launch command — **recorded only, NOT executed**:

```sh
/bin/bash '/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/run_c10y_precast_diag.sh' --utc "$(/bin/date -u +%Y%m%dT%H%M%SZ)"
```

The command requires installable TERM/INT/HUP traps, a fresh exclusive UTC namespace, and the unchanged GPU/source/fingerprint gates. An inherited SIG_IGN causes refusal before owned children. Planned wall-clock ceiling remains 2,820 seconds (47 minutes), including cleanup; real model runtime, MPS arithmetic, and runtime observer inertness remain UNVERIFIED. CPU fixtures use the copied real launcher with a 6-second cap and 4-second cleanup reserve to verify process supervision; their timing does not establish production feasibility. No live diagnostic namespace exists. B3 build behavior is empirically fixed for this fail-closed option; Astra acceptance review and the separate benchmark handoff remain external next steps.

Raw evidence directory: `/private/tmp/c10y_build/precast_fix2_20261009T194529Z`. All four complete test outputs are embedded here so temporary-file retention is not required to review the evidence.

| Raw log | Bytes | SHA-256 |
|---|---:|---|
| `inherited_RED.log` | 14531 | `353c44510af1ddb3ac750db3364a9426705cc2943483a89fbfd84c2bfbef19e3` |
| `inherited_GREEN.log` | 1171 | `4b69e0278891b69876bc9d00e29b1cc593b85d34c6b4f2758fe3dd0882698441` |
| `precast_full_GREEN_final.log` | 10961 | `9613eb95dea75969c7fa754ddc56d6a4abd86f90e99532d03df745b63ce8d481` |
| `c10y_full_GREEN_final.log` | 41257 | `0b23f26f935ad0c6b52f84bdd082454bdd8463efcb3720622c8dbc38574f808b` |

Static/preservation audit:

```json
{
  "benchmark_pin_unchanged": "9b25a207f630fbfa0d60c80a74f22289ad3bb2cc160d0fc72d7e0367f9a47a1a",
  "benchmark_repin": "NOT PERFORMED; waiting for ASTRA A1 commit and MAESTRO handoff",
  "benchmark_working_sha256": "3703d8b9c363bb06eab0ca66f38f4b01114363ae75a9d0397701e75aa2520041",
  "cleanup_reserve_seconds": 10,
  "deadline_cancelled_last": true,
  "deadline_precedes_python": true,
  "deadline_seconds": 2820,
  "owned_sha256": {
    "experiments/track_c/c10y_precast_diag.py": "520939b5c49376d5ebfa7c219d905e617881851d6c569071eee3523d0fa91ee9",
    "experiments/track_c/c10y_precast_diag_selftest.py": "2f66f89e250013ee4d0cffb0627f93652a8dee2ab56c6d0385f999a4a1ad99a7",
    "tools/run_c10y_precast_diag.sh": "2f34a35aab954ae442d4e812208a1d0b5a79e072f590df119dc0ac7e44c34c37"
  },
  "protected_count": 158,
  "protected_unchanged_count": 157,
  "python_compile": "PASS",
  "report_prefix_bytes": 349415,
  "report_prefix_sha256": "55b917b4ed1c521b6272a35b05a2c6c1bd4521ab73791c25b68b1ebad6cfdbb4",
  "review_sha256": "1879bacc7660dfc48c59741451b779b93ce4b54188cb3a082fc42b9a6416a7d4",
  "science_output_namespace": "ABSENT",
  "scope_sha256": "097c662803a94a897dd588c9e1f09c6af7b17a25019c1439ea39844c65f0a9a8",
  "trap_check_precedes_owned_children": true,
  "unowned_observed_drift_preserved": {
    "EXPERIMENT_RUNBOOK.md": {
      "after": "7da856979ea0501e770d0234b2d0bcbd09c64f577b87f2934fa6bbab56a3bd37",
      "before": "24ad49597a7b9643ccff0005e437f26b02271fece3f04f4567f4e48a1a04bb85"
    }
  }
}
```

Full output — `inherited_RED.log`:

```text
test_inherited_ignored_HUP_refused_before_owned_children (__main__.Contracts.test_inherited_ignored_HUP_refused_before_owned_children) ... FAIL
test_inherited_ignored_INT_refused_before_owned_children (__main__.Contracts.test_inherited_ignored_INT_refused_before_owned_children) ... FAIL
test_inherited_ignored_TERM_refused_before_owned_children (__main__.Contracts.test_inherited_ignored_TERM_refused_before_owned_children) ... FAIL
test_real_shell_supervisor_HUP_cleans_owned_worker_and_publishes_INCONCLUSIVE (__main__.Contracts.test_real_shell_supervisor_HUP_cleans_owned_worker_and_publishes_INCONCLUSIVE) ... ok

======================================================================
FAIL: test_inherited_ignored_HUP_refused_before_owned_children (__main__.Contracts.test_inherited_ignored_HUP_refused_before_owned_children)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 689, in test_inherited_ignored_HUP_refused_before_owned_children
    self.run_shell_stub('inherited_ignore','HUP')
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 777, in run_shell_stub
    self.assertEqual(child.returncode,3,(child.stdout,child.stderr))
AssertionError: 2 != 3 : ('', '/private/tmp/c10y_build/tmpsdat13rs/tools/run_c10y_precast_diag.sh: line 172: 28382 Killed: 9               "$PY" -B "$DRIVER" --utc "$UTC" --worker > "$OUT/worker.log" 2>&1\n/private/tmp/c10y_build/tmpsdat13rs/tools/run_c10y_precast_diag.sh: line 31: kill: (-28382) - No such process\n/private/tmp/c10y_build/tmpsdat13rs/tools/run_c10y_precast_diag.sh: line 33: kill: (28382) - No such process\n/private/tmp/c10y_build/tmpsdat13rs/tools/run_c10y_precast_diag.sh: line 39: kill: (28382) - No such process\n/private/tmp/c10y_build/tmpsdat13rs/tools/run_c10y_precast_diag.sh: line 47: kill: (-28382) - No such process\n/private/tmp/c10y_build/tmpsdat13rs/tools/run_c10y_precast_diag.sh: line 51: kill: (28382) - No such process\n/private/tmp/c10y_build/tmpsdat13rs/tools/run_c10y_precast_diag.sh: line 47: kill: (-28382) - No such process\n/private/tmp/c10y_build/tmpsdat13rs/tools/run_c10y_precast_diag.sh: line 51: kill: (28382) - No such process\n/private/tmp/c10y_build/tmpsdat13rs/tools/run_c10y_precast_diag.sh: line 31: kill: (-28382) - No such process\n/private/tmp/c10y_build/tmpsdat13rs/tools/run_c10y_precast_diag.sh: line 33: kill: (28382) - No such process\n/private/tmp/c10y_build/tmpsdat13rs/tools/run_c10y_precast_diag.sh: line 39: kill: (28476) - No such process\n/private/tmp/c10y_build/tmpsdat13rs/tools/run_c10y_precast_diag.sh: line 47: kill: (-28382) - No such process\n/private/tmp/c10y_build/tmpsdat13rs/tools/run_c10y_precast_diag.sh: line 51: kill: (28476) - No such process\n/private/tmp/c10y_build/tmpsdat13rs/tools/run_c10y_precast_diag.sh: line 47: kill: (-28382) - No such process\n/private/tmp/c10y_build/tmpsdat13rs/tools/run_c10y_precast_diag.sh: line 51: kill: (28476) - No such process\n')

======================================================================
FAIL: test_inherited_ignored_INT_refused_before_owned_children (__main__.Contracts.test_inherited_ignored_INT_refused_before_owned_children)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 692, in test_inherited_ignored_INT_refused_before_owned_children
    self.run_shell_stub('inherited_ignore','INT')
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 777, in run_shell_stub
    self.assertEqual(child.returncode,3,(child.stdout,child.stderr))
AssertionError: 2 != 3 : ('', '/private/tmp/c10y_build/tmp47asnoei/tools/run_c10y_precast_diag.sh: line 172: 28530 Killed: 9               "$PY" -B "$DRIVER" --utc "$UTC" --worker > "$OUT/worker.log" 2>&1\n/private/tmp/c10y_build/tmp47asnoei/tools/run_c10y_precast_diag.sh: line 31: kill: (-28530) - No such process\n/private/tmp/c10y_build/tmp47asnoei/tools/run_c10y_precast_diag.sh: line 33: kill: (28530) - No such process\n/private/tmp/c10y_build/tmp47asnoei/tools/run_c10y_precast_diag.sh: line 39: kill: (28530) - No such process\n/private/tmp/c10y_build/tmp47asnoei/tools/run_c10y_precast_diag.sh: line 47: kill: (-28530) - No such process\n/private/tmp/c10y_build/tmp47asnoei/tools/run_c10y_precast_diag.sh: line 51: kill: (28530) - No such process\n/private/tmp/c10y_build/tmp47asnoei/tools/run_c10y_precast_diag.sh: line 47: kill: (-28530) - No such process\n/private/tmp/c10y_build/tmp47asnoei/tools/run_c10y_precast_diag.sh: line 51: kill: (28530) - No such process\n/private/tmp/c10y_build/tmp47asnoei/tools/run_c10y_precast_diag.sh: line 31: kill: (-28530) - No such process\n/private/tmp/c10y_build/tmp47asnoei/tools/run_c10y_precast_diag.sh: line 33: kill: (28530) - No such process\n/private/tmp/c10y_build/tmp47asnoei/tools/run_c10y_precast_diag.sh: line 39: kill: (28707) - No such process\n/private/tmp/c10y_build/tmp47asnoei/tools/run_c10y_precast_diag.sh: line 47: kill: (-28530) - No such process\n/private/tmp/c10y_build/tmp47asnoei/tools/run_c10y_precast_diag.sh: line 51: kill: (28707) - No such process\n/private/tmp/c10y_build/tmp47asnoei/tools/run_c10y_precast_diag.sh: line 47: kill: (-28530) - No such process\n/private/tmp/c10y_build/tmp47asnoei/tools/run_c10y_precast_diag.sh: line 51: kill: (28707) - No such process\n')

======================================================================
FAIL: test_inherited_ignored_TERM_refused_before_owned_children (__main__.Contracts.test_inherited_ignored_TERM_refused_before_owned_children)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 695, in test_inherited_ignored_TERM_refused_before_owned_children
    self.run_shell_stub('inherited_ignore','TERM')
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py", line 777, in run_shell_stub
    self.assertEqual(child.returncode,3,(child.stdout,child.stderr))
AssertionError: -9 != 3 : ('', '/private/tmp/c10y_build/tmphfp7iace/tools/run_c10y_precast_diag.sh: line 172: 28717 Killed: 9               "$PY" -B "$DRIVER" --utc "$UTC" --worker > "$OUT/worker.log" 2>&1\n/private/tmp/c10y_build/tmphfp7iace/tools/run_c10y_precast_diag.sh: line 31: kill: (-28717) - No such process\n/private/tmp/c10y_build/tmphfp7iace/tools/run_c10y_precast_diag.sh: line 33: kill: (28717) - No such process\n/private/tmp/c10y_build/tmphfp7iace/tools/run_c10y_precast_diag.sh: line 39: kill: (28717) - No such process\n/private/tmp/c10y_build/tmphfp7iace/tools/run_c10y_precast_diag.sh: line 47: kill: (-28717) - No such process\n/private/tmp/c10y_build/tmphfp7iace/tools/run_c10y_precast_diag.sh: line 51: kill: (28717) - No such process\n/private/tmp/c10y_build/tmphfp7iace/tools/run_c10y_precast_diag.sh: line 47: kill: (-28717) - No such process\n/private/tmp/c10y_build/tmphfp7iace/tools/run_c10y_precast_diag.sh: line 51: kill: (28717) - No such process\n/private/tmp/c10y_build/tmphfp7iace/tools/run_c10y_precast_diag.sh: line 31: kill: (-28717) - No such process\n/private/tmp/c10y_build/tmphfp7iace/tools/run_c10y_precast_diag.sh: line 33: kill: (28717) - No such process\n/private/tmp/c10y_build/tmphfp7iace/tools/run_c10y_precast_diag.sh: line 39: kill: (28792) - No such process\n/private/tmp/c10y_build/tmphfp7iace/tools/run_c10y_precast_diag.sh: line 47: kill: (-28717) - No such process\n/private/tmp/c10y_build/tmphfp7iace/tools/run_c10y_precast_diag.sh: line 51: kill: (28792) - No such process\n/private/tmp/c10y_build/tmphfp7iace/tools/run_c10y_precast_diag.sh: line 47: kill: (-28717) - No such process\n/private/tmp/c10y_build/tmphfp7iace/tools/run_c10y_precast_diag.sh: line 51: kill: (28792) - No such process\n/private/tmp/c10y_build/tmphfp7iace/tools/run_c10y_precast_diag.sh: line 31: kill: (-28717) - No such process\n/private/tmp/c10y_build/tmphfp7iace/tools/run_c10y_precast_diag.sh: line 33: kill: (28717) - No such process\n/private/tmp/c10y_build/tmphfp7iace/tools/run_c10y_precast_diag.sh: line 39: kill: (28792) - No such process\n')

----------------------------------------------------------------------
Ran 4 tests in 17.324s

FAILED (failures=3)
INHERITED_SIG_IGN HUP rc=2 namespace=True timer=True prepare=True
/private/tmp/c10y_build/tmpsdat13rs/tools/run_c10y_precast_diag.sh: line 172: 28382 Killed: 9               "$PY" -B "$DRIVER" --utc "$UTC" --worker > "$OUT/worker.log" 2>&1
/private/tmp/c10y_build/tmpsdat13rs/tools/run_c10y_precast_diag.sh: line 31: kill: (-28382) - No such process
/private/tmp/c10y_build/tmpsdat13rs/tools/run_c10y_precast_diag.sh: line 33: kill: (28382) - No such process
/private/tmp/c10y_build/tmpsdat13rs/tools/run_c10y_precast_diag.sh: line 39: kill: (28382) - No such process
/private/tmp/c10y_build/tmpsdat13rs/tools/run_c10y_precast_diag.sh: line 47: kill: (-28382) - No such process
/private/tmp/c10y_build/tmpsdat13rs/tools/run_c10y_precast_diag.sh: line 51: kill: (28382) - No such process
/private/tmp/c10y_build/tmpsdat13rs/tools/run_c10y_precast_diag.sh: line 47: kill: (-28382) - No such process
/private/tmp/c10y_build/tmpsdat13rs/tools/run_c10y_precast_diag.sh: line 51: kill: (28382) - No such process
/private/tmp/c10y_build/tmpsdat13rs/tools/run_c10y_precast_diag.sh: line 31: kill: (-28382) - No such process
/private/tmp/c10y_build/tmpsdat13rs/tools/run_c10y_precast_diag.sh: line 33: kill: (28382) - No such process
/private/tmp/c10y_build/tmpsdat13rs/tools/run_c10y_precast_diag.sh: line 39: kill: (28476) - No such process
/private/tmp/c10y_build/tmpsdat13rs/tools/run_c10y_precast_diag.sh: line 47: kill: (-28382) - No such process
/private/tmp/c10y_build/tmpsdat13rs/tools/run_c10y_precast_diag.sh: line 51: kill: (28476) - No such process
/private/tmp/c10y_build/tmpsdat13rs/tools/run_c10y_precast_diag.sh: line 47: kill: (-28382) - No such process
/private/tmp/c10y_build/tmpsdat13rs/tools/run_c10y_precast_diag.sh: line 51: kill: (28476) - No such process
INHERITED_SIG_IGN INT rc=2 namespace=True timer=True prepare=True
/private/tmp/c10y_build/tmp47asnoei/tools/run_c10y_precast_diag.sh: line 172: 28530 Killed: 9               "$PY" -B "$DRIVER" --utc "$UTC" --worker > "$OUT/worker.log" 2>&1
/private/tmp/c10y_build/tmp47asnoei/tools/run_c10y_precast_diag.sh: line 31: kill: (-28530) - No such process
/private/tmp/c10y_build/tmp47asnoei/tools/run_c10y_precast_diag.sh: line 33: kill: (28530) - No such process
/private/tmp/c10y_build/tmp47asnoei/tools/run_c10y_precast_diag.sh: line 39: kill: (28530) - No such process
/private/tmp/c10y_build/tmp47asnoei/tools/run_c10y_precast_diag.sh: line 47: kill: (-28530) - No such process
/private/tmp/c10y_build/tmp47asnoei/tools/run_c10y_precast_diag.sh: line 51: kill: (28530) - No such process
/private/tmp/c10y_build/tmp47asnoei/tools/run_c10y_precast_diag.sh: line 47: kill: (-28530) - No such process
/private/tmp/c10y_build/tmp47asnoei/tools/run_c10y_precast_diag.sh: line 51: kill: (28530) - No such process
/private/tmp/c10y_build/tmp47asnoei/tools/run_c10y_precast_diag.sh: line 31: kill: (-28530) - No such process
/private/tmp/c10y_build/tmp47asnoei/tools/run_c10y_precast_diag.sh: line 33: kill: (28530) - No such process
/private/tmp/c10y_build/tmp47asnoei/tools/run_c10y_precast_diag.sh: line 39: kill: (28707) - No such process
/private/tmp/c10y_build/tmp47asnoei/tools/run_c10y_precast_diag.sh: line 47: kill: (-28530) - No such process
/private/tmp/c10y_build/tmp47asnoei/tools/run_c10y_precast_diag.sh: line 51: kill: (28707) - No such process
/private/tmp/c10y_build/tmp47asnoei/tools/run_c10y_precast_diag.sh: line 47: kill: (-28530) - No such process
/private/tmp/c10y_build/tmp47asnoei/tools/run_c10y_precast_diag.sh: line 51: kill: (28707) - No such process
INHERITED_SIG_IGN TERM rc=-9 namespace=True timer=True prepare=True
/private/tmp/c10y_build/tmphfp7iace/tools/run_c10y_precast_diag.sh: line 172: 28717 Killed: 9               "$PY" -B "$DRIVER" --utc "$UTC" --worker > "$OUT/worker.log" 2>&1
/private/tmp/c10y_build/tmphfp7iace/tools/run_c10y_precast_diag.sh: line 31: kill: (-28717) - No such process
/private/tmp/c10y_build/tmphfp7iace/tools/run_c10y_precast_diag.sh: line 33: kill: (28717) - No such process
/private/tmp/c10y_build/tmphfp7iace/tools/run_c10y_precast_diag.sh: line 39: kill: (28717) - No such process
/private/tmp/c10y_build/tmphfp7iace/tools/run_c10y_precast_diag.sh: line 47: kill: (-28717) - No such process
/private/tmp/c10y_build/tmphfp7iace/tools/run_c10y_precast_diag.sh: line 51: kill: (28717) - No such process
/private/tmp/c10y_build/tmphfp7iace/tools/run_c10y_precast_diag.sh: line 47: kill: (-28717) - No such process
/private/tmp/c10y_build/tmphfp7iace/tools/run_c10y_precast_diag.sh: line 51: kill: (28717) - No such process
/private/tmp/c10y_build/tmphfp7iace/tools/run_c10y_precast_diag.sh: line 31: kill: (-28717) - No such process
/private/tmp/c10y_build/tmphfp7iace/tools/run_c10y_precast_diag.sh: line 33: kill: (28717) - No such process
/private/tmp/c10y_build/tmphfp7iace/tools/run_c10y_precast_diag.sh: line 39: kill: (28792) - No such process
/private/tmp/c10y_build/tmphfp7iace/tools/run_c10y_precast_diag.sh: line 47: kill: (-28717) - No such process
/private/tmp/c10y_build/tmphfp7iace/tools/run_c10y_precast_diag.sh: line 51: kill: (28792) - No such process
/private/tmp/c10y_build/tmphfp7iace/tools/run_c10y_precast_diag.sh: line 47: kill: (-28717) - No such process
/private/tmp/c10y_build/tmphfp7iace/tools/run_c10y_precast_diag.sh: line 51: kill: (28792) - No such process
/private/tmp/c10y_build/tmphfp7iace/tools/run_c10y_precast_diag.sh: line 31: kill: (-28717) - No such process
/private/tmp/c10y_build/tmphfp7iace/tools/run_c10y_precast_diag.sh: line 33: kill: (28717) - No such process
/private/tmp/c10y_build/tmphfp7iace/tools/run_c10y_precast_diag.sh: line 39: kill: (28792) - No such process
```

Full output — `inherited_GREEN.log`:

```text
test_inherited_ignored_HUP_refused_before_owned_children (__main__.Contracts.test_inherited_ignored_HUP_refused_before_owned_children) ... ok
test_inherited_ignored_INT_refused_before_owned_children (__main__.Contracts.test_inherited_ignored_INT_refused_before_owned_children) ... ok
test_inherited_ignored_TERM_refused_before_owned_children (__main__.Contracts.test_inherited_ignored_TERM_refused_before_owned_children) ... ok
test_real_shell_supervisor_HUP_cleans_owned_worker_and_publishes_INCONCLUSIVE (__main__.Contracts.test_real_shell_supervisor_HUP_cleans_owned_worker_and_publishes_INCONCLUSIVE) ... ok

----------------------------------------------------------------------
Ran 4 tests in 2.389s

OK
INHERITED_SIG_IGN HUP rc=3 namespace=False timer=False prepare=False
INCONCLUSIVE: SIGNAL-TRAP-UNAVAILABLE HUP; phases NOT-RUN; no owned child launched.
INHERITED_SIG_IGN INT rc=3 namespace=False timer=False prepare=False
INCONCLUSIVE: SIGNAL-TRAP-UNAVAILABLE INT; phases NOT-RUN; no owned child launched.
INHERITED_SIG_IGN TERM rc=3 namespace=False timer=False prepare=False
INCONCLUSIVE: SIGNAL-TRAP-UNAVAILABLE TERM; phases NOT-RUN; no owned child launched.
```

Full output — `precast_full_GREEN_final.log`:

```text
test_48_targets_computed_once_saved_reloaded_and_shared_by_original_paths (__main__.Contracts.test_48_targets_computed_once_saved_reloaded_and_shared_by_original_paths) ... ok
test_INCONCLUSIVE_precedes_every_other_reading (__main__.Contracts.test_INCONCLUSIVE_precedes_every_other_reading) ... ok
test_R_requires_every_cell_and_A7_device_difference (__main__.Contracts.test_R_requires_every_cell_and_A7_device_difference) ... ok
test_S_needs_direct_trace_evidence_and_K_never_emitted (__main__.Contracts.test_S_needs_direct_trace_evidence_and_K_never_emitted) ... ok
test_actual_native_solve_inputs_are_fsynced_before_execution (__main__.Contracts.test_actual_native_solve_inputs_are_fsynced_before_execution) ... ok
test_actual_representation_batch_padding_and_indices_captured_without_id_assumption (__main__.Contracts.test_actual_representation_batch_padding_and_indices_captured_without_id_assumption) ... ok
test_completed_float64_direct_solution_survives_next_solve_failure (__main__.Contracts.test_completed_float64_direct_solution_survives_next_solve_failure) ... ok
test_completed_native_CPU_product_survives_later_control_halt (__main__.Contracts.test_completed_native_CPU_product_survives_later_control_halt) ... ok
test_device_product_observed_from_original_effective_weight (__main__.Contracts.test_device_product_observed_from_original_effective_weight) ... ok
test_difference_metrics_and_weight_coordinate_columns (__main__.Contracts.test_difference_metrics_and_weight_coordinate_columns) ... ok
test_exclusive_JSON_and_tensor_collision_have_no_sibling (__main__.Contracts.test_exclusive_JSON_and_tensor_collision_have_no_sibling) ... ok
test_fail_closed_gpu_and_fingerprint_records_precede_loader (__main__.Contracts.test_fail_closed_gpu_and_fingerprint_records_precede_loader) ... ok
test_finalizer_incomplete_worker_cannot_publish_R (__main__.Contracts.test_finalizer_incomplete_worker_cannot_publish_R) ... ok
test_finalizer_malformed_worker_preserves_exception_and_inconclusive (__main__.Contracts.test_finalizer_malformed_worker_preserves_exception_and_inconclusive) ... ok
test_finalizer_overwrite_refusal_keeps_terminal_bytes (__main__.Contracts.test_finalizer_overwrite_refusal_keeps_terminal_bytes) ... ok
test_finalizer_rejects_completed_claim_with_incomplete_phases (__main__.Contracts.test_finalizer_rejects_completed_claim_with_incomplete_phases) ... ok
test_float64_realization_cannot_demote_to_float32 (__main__.Contracts.test_float64_realization_cannot_demote_to_float32) ... ok
test_float64_realization_casts_on_CPU_before_device_transfer (__main__.Contracts.test_float64_realization_casts_on_CPU_before_device_transfer) ... ok
test_float64_solve_and_promoted_product_are_distinct (__main__.Contracts.test_float64_solve_and_promoted_product_are_distinct) ... ok
test_forced_native_halt_preserves_capture_and_cleans_weights_globals (__main__.Contracts.test_forced_native_halt_preserves_capture_and_cleans_weights_globals) ... ok
test_fresh_import_is_model_and_torch_free (__main__.Contracts.test_fresh_import_is_model_and_torch_free) ... ok
test_fresh_namespace_existing_directory_and_symlink_refused (__main__.Contracts.test_fresh_namespace_existing_directory_and_symlink_refused) ... ok
test_full_weight_coordinate_quantiles_exceed_torch_limit (__main__.Contracts.test_full_weight_coordinate_quantiles_exceed_torch_limit) ... ok
test_gate_inputs_fsynced_and_reloaded_before_predicate (__main__.Contracts.test_gate_inputs_fsynced_and_reloaded_before_predicate) ... ok
test_genuine_native_operand_discrepancy_remains_valid_S_evidence (__main__.Contracts.test_genuine_native_operand_discrepancy_remains_valid_S_evidence) ... ok
test_inherited_ignored_HUP_refused_before_owned_children (__main__.Contracts.test_inherited_ignored_HUP_refused_before_owned_children) ... ok
test_inherited_ignored_INT_refused_before_owned_children (__main__.Contracts.test_inherited_ignored_INT_refused_before_owned_children) ... ok
test_inherited_ignored_TERM_refused_before_owned_children (__main__.Contracts.test_inherited_ignored_TERM_refused_before_owned_children) ... ok
test_interrupted_publication_preserves_prior_bytes_and_is_fresh_INCONCLUSIVE (__main__.Contracts.test_interrupted_publication_preserves_prior_bytes_and_is_fresh_INCONCLUSIVE) ... ok
test_interrupted_serialization_is_incomplete_and_retains_previous_values (__main__.Contracts.test_interrupted_serialization_is_incomplete_and_retains_previous_values) ... ok
test_malformed_classification_capture_is_INCONCLUSIVE (__main__.Contracts.test_malformed_classification_capture_is_INCONCLUSIVE) ... ok
test_missing_capture_refuses_instead_of_reimplementing (__main__.Contracts.test_missing_capture_refuses_instead_of_reimplementing) ... ok
test_missing_reference_Q_retains_available_operands_before_coverage_halt (__main__.Contracts.test_missing_reference_Q_retains_available_operands_before_coverage_halt) ... ok
test_native_direct_solve_failure_retains_inputs_and_original_exception (__main__.Contracts.test_native_direct_solve_failure_retains_inputs_and_original_exception) ... ok
test_native_direct_update_included_in_all_pair_measurements (__main__.Contracts.test_native_direct_update_included_in_all_pair_measurements) ... ok
test_native_factor_actual_matrix_and_Q_are_compared (__main__.Contracts.test_native_factor_actual_matrix_and_Q_are_compared) ... ok
test_native_factor_solve_failure_retains_inputs_and_original_exception (__main__.Contracts.test_native_factor_solve_failure_retains_inputs_and_original_exception) ... ok
test_native_missing_factor_Q_is_inconclusive_capture_failure (__main__.Contracts.test_native_missing_factor_Q_is_inconclusive_capture_failure) ... ok
test_nonfinite_operand_persisted_before_halt (__main__.Contracts.test_nonfinite_operand_persisted_before_halt) ... ok
test_observer_direct_M_mutation_at_return_invalidates_evidence (__main__.Contracts.test_observer_direct_M_mutation_at_return_invalidates_evidence) ... ok
test_observer_factor_Q_copy_mutation_invalidates_evidence (__main__.Contracts.test_observer_factor_Q_copy_mutation_invalidates_evidence) ... ok
test_observer_off_failure_retains_prior_native_input_capture (__main__.Contracts.test_observer_off_failure_retains_prior_native_input_capture) ... ok
test_observer_original_code_coverage_off_on_and_native_operands (__main__.Contracts.test_observer_original_code_coverage_off_on_and_native_operands) ... ok
test_observer_tensor_inertness_catches_discarded_cur_mutation (__main__.Contracts.test_observer_tensor_inertness_catches_discarded_cur_mutation) ... ok
test_packet_tamper_refused_before_downstream_consumption (__main__.Contracts.test_packet_tamper_refused_before_downstream_consumption) ... ok
test_phase_failure_publication_preserves_original_exception (__main__.Contracts.test_phase_failure_publication_preserves_original_exception) ... ok
test_real_shell_existing_namespace_refused_without_finalizer (__main__.Contracts.test_real_shell_existing_namespace_refused_without_finalizer) ... ok
test_real_shell_finalizer_abnormal_exit_has_fresh_INCONCLUSIVE_diagnostic (__main__.Contracts.test_real_shell_finalizer_abnormal_exit_has_fresh_INCONCLUSIVE_diagnostic) ... ok
test_real_shell_finalizer_timeout_has_fresh_supervisor_diagnostic (__main__.Contracts.test_real_shell_finalizer_timeout_has_fresh_supervisor_diagnostic) ... ok
test_real_shell_interrupted_publisher_timeout_remains_armed_and_is_diagnosed (__main__.Contracts.test_real_shell_interrupted_publisher_timeout_remains_armed_and_is_diagnosed) ... ok
test_real_shell_owned_process_group_is_stopped_after_leader_exit (__main__.Contracts.test_real_shell_owned_process_group_is_stopped_after_leader_exit) ... ok
test_real_shell_supervisor_HUP_cleans_owned_worker_and_publishes_INCONCLUSIVE (__main__.Contracts.test_real_shell_supervisor_HUP_cleans_owned_worker_and_publishes_INCONCLUSIVE) ... ok
test_real_shell_supervisor_INT_cleans_owned_worker_and_publishes_INCONCLUSIVE (__main__.Contracts.test_real_shell_supervisor_INT_cleans_owned_worker_and_publishes_INCONCLUSIVE) ... ok
test_real_shell_supervisor_TERM_cleans_owned_worker_and_publishes_INCONCLUSIVE (__main__.Contracts.test_real_shell_supervisor_TERM_cleans_owned_worker_and_publishes_INCONCLUSIVE) ... ok
test_real_shell_supervisor_abnormal_exit_cleans_owned_worker_and_publishes_INCONCLUSIVE (__main__.Contracts.test_real_shell_supervisor_abnormal_exit_cleans_owned_worker_and_publishes_INCONCLUSIVE) ... ok
test_real_shell_supervisor_hanging_stub_preserves_timeout_and_kills_worker (__main__.Contracts.test_real_shell_supervisor_hanging_stub_preserves_timeout_and_kills_worker) ... ok
test_real_shell_supervisor_setup_timeout_retains_owned_namespace_diagnostic (__main__.Contracts.test_real_shell_supervisor_setup_timeout_retains_owned_namespace_diagnostic) ... ok
test_real_shell_supervisor_worker_exit_before_start_is_diagnosed (__main__.Contracts.test_real_shell_supervisor_worker_exit_before_start_is_diagnosed) ... ok
test_real_shell_worker_log_collision_refused_without_overwrite (__main__.Contracts.test_real_shell_worker_log_collision_refused_without_overwrite) ... ok
test_realized_native_saved_factors_drive_R_predicate (__main__.Contracts.test_realized_native_saved_factors_drive_R_predicate) ... ok
test_repeat_factor_compared_to_original_native_solution (__main__.Contracts.test_repeat_factor_compared_to_original_native_solution) ... ok
test_restores_optional_recorder_and_preexisting_hook_on_halt (__main__.Contracts.test_restores_optional_recorder_and_preexisting_hook_on_halt) ... ok
test_scope_SHA_drift_refused (__main__.Contracts.test_scope_SHA_drift_refused) ... ok
test_supervisor_timeout_overrides_worker_success_and_preserves_commits (__main__.Contracts.test_supervisor_timeout_overrides_worker_success_and_preserves_commits) ... ok
test_target_failure_retains_completed_prefix_and_NOT_RUN_arm (__main__.Contracts.test_target_failure_retains_completed_prefix_and_NOT_RUN_arm) ... ok
test_target_mutation_halt_retains_offending_value_and_restores_weights (__main__.Contracts.test_target_mutation_halt_retains_offending_value_and_restores_weights) ... ok
test_timeout_publication_preserves_previous_bytes_and_has_terminal_INCONCLUSIVE (__main__.Contracts.test_timeout_publication_preserves_previous_bytes_and_has_terminal_INCONCLUSIVE) ... ok
test_valid_complete_phases_publish_threshold_free_R (__main__.Contracts.test_valid_complete_phases_publish_threshold_free_R) ... ok

----------------------------------------------------------------------
Ran 68 tests in 45.717s

OK
INHERITED_SIG_IGN HUP rc=3 namespace=False timer=False prepare=False
INCONCLUSIVE: SIGNAL-TRAP-UNAVAILABLE HUP; phases NOT-RUN; no owned child launched.
INHERITED_SIG_IGN INT rc=3 namespace=False timer=False prepare=False
INCONCLUSIVE: SIGNAL-TRAP-UNAVAILABLE INT; phases NOT-RUN; no owned child launched.
INHERITED_SIG_IGN TERM rc=3 namespace=False timer=False prepare=False
INCONCLUSIVE: SIGNAL-TRAP-UNAVAILABLE TERM; phases NOT-RUN; no owned child launched.
```

Full output — `c10y_full_GREEN_final.log`:

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
Ran 285 tests in 25.675s

OK
{"launched": false, "reasons": ["missing/unknown/duplicate phases"], "status": "UNVERIFIED"}
ISOLATION OWNED LISTING DRIFT: []
ISOLATION OTHER OBSERVED UNATTRIBUTED: ["results/mathlab_staging/runs/m2_20261009T192821Z_82233/events.jsonl"]
SYS_MODULES_FORBIDDEN: []
C10Y_DIRECTDW_SELFTEST PASS — CPU ONLY; LIVE LAW#3/LAW#5 UNVERIFIED
```
