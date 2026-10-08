# C10Y direct-ΔW build — D-C10y-directdw

**Status: SOURCE BUILD COMPLETE; VERIFICATION PARTIAL / DISPATCH GATED.** Final static review is GO for code only. The final light suite ran 226 tests: 225 passed, with the protected-byte assertion failing on three externally changed files. Three required tests remain unrun: two full-size CPU reduction cases and the native child deadline test. M14 remains UNVERIFIED. This report does not claim a complete suite PASS or authorise a model-bearing launch.

Builder model/effort: exact runtime identity **UNVERIFIABLE**. Independent reviewer: configured GPT-6-Astra/high; final artifact `/private/tmp/c10y_build/astra_final_delta2.md`, SHA-256 `9a0c290d1b1262977614007d40f99d7ba6c171310a0d54218d95d9439eff3ef0`. Its advisor-contract verdict is PROCEED for static code only. Claude authentication was probed: exit 1, `loggedIn=false`, `authMethod=none`. The GPT-family fallback is weaker independence than an out-of-family Claude review; no external Claude scientific review is claimed.

Authoritative prereg pin: `e069b358c362b2a05e3b668e8a29f33061e15a24306e321452e6fa46a4e83331`. Read the complete frozen body and Amendments T/C/P, including all binding brief §10 answers and prereg §11. The later Program message replacing c68a358b with this §11 digest overrides the brief’s stale §1/Q1 hash. No prereg or engine file was edited by this build. Q1–Q8 are binding answers, not open defaults.

The build is CPU-only and model-free. No real worker, model/tokenizer, transformers/datasets/harness import, MPS tensor or operation, or GPU job was run. Torch was used only for tiny hand-built CPU models and explicit fixtures. Tests were serial, one Python process at a time, under `/private/tmp/c10y_build`. During GPU-LIVE benchmark restrictions there was no Python/heavy CPU execution; after BENCH-DONE only light serial work resumed. The two full-size checks and child test were left pending the requested resource/process-count decisions. No git writes, dependency installation, CORPUS/ledger/runbook edits or memory writes were made.

The experiment remains **MEASUREMENT-ONLY** (prereg:3,105–119). CPU plumbing and static review establish neither live LAW#3/LAW#5 nor MPS arithmetic/backward, edited-output telemetry/resource inertness, factual learning, timing feasibility, reproducibility on MPS, compaction or F1 closure. The actual deployment route remains unqualified.

## Files and exact source identity

| File | SHA-256 |
|---|---|
| `experiments/track_c/c10y_directdw_arms.py` | `206710d02c6cc8580a14391cc94c5280db63bc1a9de0177bb3b6a15951c29416` |
| `experiments/track_c/c10y_directdw_telemetry_check.py` | `e79f0532ac674a0cb8a3d21c838c15710ee0ed3e94f7fa88e65d722105c1c03f` |
| `experiments/track_c/c10y_directdw_read.py` | `f8d2598b01956be3ad390c76b2336ae1398e77d05045fb8870a3ae6e42cb2e78` |
| `experiments/track_c/c10y_directdw_selftest.py` | `02977e73ea0a6d70b642112d025a2e274060d3334a339baad149a799916db3c1` |
| `results/c10y_directdw_codex_build.md` | Its final byte SHA is in `/private/tmp/c10y_build/after/r2_sha256.json`, refreshed after writing; a report cannot embed its own byte hash without changing it. |

The four sources above were independently rehashed by the final reviewer. Mutation source writes were limited to an explicit lease on these allowed paths, backed up under `/private/tmp/c10y_build/mut_backup`, restored in `finally`, and byte-SHA checked. No cache/bytecode was used for mutation imports; fresh source was compiled in process.

## Binding choices and remaining provisional interpretations

Q1: amendments T/C/P implemented with the final pin. Q2: statement-identical observed scorer with a single sink insertion; absent subject/template attribution disables telemetry. Q3: first attempt has telemetry unset at every stage; memory telemetry remains required. T8 is built and unrun, with its own recorded Program/operator spend authorisation before future dispatch. Q4: calibration is built through the stage-1 prefix and smoke, gated by go/spend/authorisation, and contributes only timing evidence to stage 1. Q5: B-z uses the full backbone forward with no truncation path. Q6: explicit new diagnostic path, Program naming `architecture_profile/c10y_halt_diagnostic_<UTC>.json`. Q7: canonical first-attempt directory and fresh `c10y_directdw_s<s>_rerun<k>` directories, with pinned stage-1 contexts and replacement provenance. Q8: every process needs go; calibration and stages 2–3 need positive finite capped spend records authored by the Program. No operator decision was invented.

PROVISIONAL artifact ownership (prereg:179; T12:674–685): stage 1 creates unsuffixed common files; stages 2/3 leave those bytes unchanged and embed their own manifest/run/ledger/overlap metadata in `pass_p1.json`/`pass_p2.json`. Proof/target tags are `s1`, `p1`, `p2`; calibration tags are `calib`. Reruns use a new directory and never repair prior records. Tests verify earlier common-file hashes across all three stages. This resolves the collision between a shared first-attempt directory and immutable prior records without relaxing gates.

PROVISIONAL serialized overlay representation (prereg:117,179): use the already named immutable `targets_<tag>.pt` bundle, containing `targets` and `actual_updates`, rather than invent a separate output family. Each H_out binds the byte SHA of that bundle and exact member `[actual_updates, recipe, arm]`; named tensor-content hashes, their certificate digest, and actual committed band digest are separate. Reader admission verifies bundle/member/certificate against the manifest; file loading verifies actual bundle bytes. The driver’s regeneration reader loads actual CPU tensors and computes R1 from them. It cannot substitute a metadata digest for the serialized SHA.

PROVISIONAL zero rules: W1 with zero baseline and nonzero candidate size is INVALID-SIZE-NORMALISATION; both zero gives ratio 1 and cannot receive positive credit (prereg:252; reader `_size`). Remaining-ratio 0/0 is 0 only when the already realised residual stays zero; nonzero/zero HALTs INVALID-REMAINING-NORMALISATION (prereg:145). Telemetry’s undefined nonzero/zero norm ratio disables the optional writer; it never invents a scientific scalar. These are conservative explicit rules, not hidden fallbacks.

PROVISIONAL shutdown/diagnostic records: the supervisor finalises `calibration.json` only after worker exit, from immutable `calibration_worker.json`, recording last-record-to-exit time. The extra worker handoff file is needed to measure C2 shutdown without overwriting completed evidence. Before template-file publication, a HALT records the expected engine-form SHA with `hash_basis=expected_engine_form_default_json`; after publication it names exact file-byte SHA with `hash_basis=file_bytes` (§11 P3).

Prerequisite/forecast bounds are textual scientific justifications supplied by the Program, not authorisations manufactured by code. The gate checks identity, types, repetitions, workloads, the strict C3 mapping and numerical lower/reserve bounds. A string that claims an independent bound does not empirically prove that bound; feasibility stays UNVERIFIED until separately authorised calibration/timings exist.

## Implementation seams and source-faithful copies

Every path is absolute and ROOT is read at call time. Source/hparams/model/revision/knob/engine identity is checked before harness import; runtime source/input and pristine-band hashes are rechecked. New-path execution is guarded before capture, hook forwards and optimisation; the original engine path remains unchanged under mode None and the dynamic LAW#5 flag. The baseline precedes every candidate proof, smoke/write and control. A LAW#3 miss persists the schedule-wide halt and later launches refuse it.

Context source is exactly the C10Q TEMPLATES literal in `experiments/track_c/c10z_astra_benchmark.py:34–40`, parsed with AST without importing the benchmark. Engine-form default-JSON SHA is `c7dabbe7c25a7e58653621d9cc66e37b35c865ae09b73b6a96073a184c6c98da`; flat canonical SHA is `d6c7c70026dced37bddc6adf316a3487d70227dae80a6e0ed5cdabe50caedfa0`. The cache is installed before any get_context_templates, overlap audit, target solve or LAW#5. Every stage/calibration/T8 file is written before its baseline gate. Stages 2/3 verify the source namespace, file SHA and exact pinned contents. A leak or pin mismatch HALTs without sampling/redraw. The benchmark source joins H_in. The process/write seed 0 is retained and never governs template sampling.

Capture solve follows frozen `c10e_bandknob.py:194–217`, with the mandated float32 CPU solve and exact sequential layer order. Prompt/label/lookup construction follows `compute_z.py:41–73`; head evaluation is target-only, KL coefficient is applied once, and 4×6 micro-batches are weighted by request count. B-e2e deploys `F.linear(input, fp16(W0 + fp16(AB)))`, AB/A/B float32, and the detached routing mask leaves forward values identical while restricting gradients. B-z uses the full forward to the top band representation. Adam rollback/overflow, threshold-before-update, fixed lr/T_max and exact fp16 merge follow prereg:51–73.

AST evidence: `TelemetryTests.test_scorer_ast_and_exact_inputs` strips only the inserted sink/capture statement and compares the remaining AST to text-read `c10e_bandknob.py:108–117`; it also verifies the exact model-input sequence and captured IDs. A separate read-only AST/literal comparison in `/private/tmp/c10y_build/verify_report.py` confirms FRAME_SUBJECTS at `c10y_directdw_arms.py:1583` equals `c10p_twopass_arms.py:30` exactly; the JSON certificate is `/private/tmp/c10y_build/frame_subjects_ast_evidence.json`. Production `frame_subjects_ast_check` at arms.py:1586 performs the same literal comparison before prefix probes. `FinalReviewRegressionTests.test_recorded_contexts_never_sample_even_after_seeding` checks only recorded-file installation without sampling after seed 0. `PinnedTemplateTests` check both literal digests, no generate_fast draw, and cache/file ordering at stage 1, calibration, stages 2/3 and T8. The named tests passed in the final light suite. No source-only precedent or harness module was imported. Engine/harness statements whose reductions are explicitly exempt remain engine arithmetic; diagnostic gates and telemetry use CPU float64.

The actual scientific hook and reader both use inclusive multiplicative NM intervals at 0.99/1.01, avoiding subtraction cancellation. Production size sums use math.fsum on CPU64 norm scalars, matching the reader. Full compile accounting includes the arm’s target solve, capture/optimisation/merge, norms, cleanup/ledger handoff, and all production harness+scientific readout work; excluded setup and experimental controls are named separately. Actual merge completion is durable before required readout, so both worker projections and supervisor classify post-merge stops as INCOMPLETE-BUDGET.

Tiny CPU F.linear fp16 forward/backward executed successfully here, including the deployed expression, gradients, routing, forced-lr0 iterations and telemetry trajectory equality. The exact Qwen/MPS F.linear, float32 factor matmul→fp16 merge, backward, MPS scheduling/synchronisation and graph-live allocation peaks are implementation-reviewed only and remain UNVERIFIED; no CPU success certifies those MPS kernels.

Read-only FRAME_SUBJECTS comparison output:

```json
{
  "copy": "experiments/track_c/c10y_directdw_arms.py:1583",
  "copy_file_sha256": "206710d02c6cc8580a14391cc94c5280db63bc1a9de0177bb3b6a15951c29416",
  "method": "ast.parse plus ast.literal_eval; no module imports or model execution",
  "source": "experiments/track_c/c10p_twopass_arms.py:30",
  "source_sha256": "c34ecbe17c86d8f2803efc5520f4cf090dcb23bcc21ef0c3c28a12bfdaeb820f",
  "subjects": [
    "Vorbanth",
    "Quillexa",
    "Tremnok",
    "Oskavel",
    "Blynthar",
    "Durmquist"
  ],
  "verdict": "IDENTICAL"
}
```

Report consistency check: `/private/tmp/c10y_build/verify_report.py` verified all four final production hashes and all 229 test/source-line mappings. The ten Program command blocks were extracted to scratch and `/opt/homebrew/bin/rtk proxy /bin/sh -n /private/tmp/c10y_build/report_launch_syntax.sh` exited 0. This is source/syntax validation only; none of those launch commands was executed.

### Production symbol index

Each entry points to the final source; the governing sources above and the registered family list below specify the requirement. Class entries include their complete callable seams.

| Symbol | Final source |
|---|---|
| `A.Budget.__init__` | `experiments/track_c/c10y_directdw_arms.py:649` |
| `A.Budget.configure` | `experiments/track_c/c10y_directdw_arms.py:653` |
| `A.Budget.consume` | `experiments/track_c/c10y_directdw_arms.py:657` |
| `A.Budget.project` | `experiments/track_c/c10y_directdw_arms.py:661` |
| `A.Halt.__init__` | `experiments/track_c/c10y_directdw_arms.py:52` |
| `A.Telemetry.__init__` | `experiments/track_c/c10y_directdw_arms.py:939` |
| `A.Telemetry.close` | `experiments/track_c/c10y_directdw_arms.py:1014` |
| `A.Telemetry.disable` | `experiments/track_c/c10y_directdw_arms.py:947` |
| `A.Telemetry.emit` | `experiments/track_c/c10y_directdw_arms.py:951` |
| `A.Telemetry.logit_lens` | `experiments/track_c/c10y_directdw_arms.py:982` |
| `A.Telemetry.opt_step` | `experiments/track_c/c10y_directdw_arms.py:964` |
| `A.Telemetry.phase` | `experiments/track_c/c10y_directdw_arms.py:960` |
| `A.Telemetry.sink` | `experiments/track_c/c10y_directdw_arms.py:1000` |
| `A.Telemetry.target_probs` | `experiments/track_c/c10y_directdw_arms.py:968` |
| `A.Telemetry.write_norms` | `experiments/track_c/c10y_directdw_arms.py:976` |
| `A.Writer.__call__` | `experiments/track_c/c10y_directdw_arms.py:433` |
| `A.Writer.__init__` | `experiments/track_c/c10y_directdw_arms.py:428` |
| `A.Writer._write_call` | `experiments/track_c/c10y_directdw_arms.py:450` |
| `A.Writer.anchor_components` | `experiments/track_c/c10y_directdw_arms.py:483` |
| `A.Writer.arm` | `experiments/track_c/c10y_directdw_arms.py:470` |
| `A.Writer.mark_merge` | `experiments/track_c/c10y_directdw_arms.py:474` |
| `A.Writer.norms` | `experiments/track_c/c10y_directdw_arms.py:480` |
| `A.Writer.write` | `experiments/track_c/c10y_directdw_arms.py:500` |
| `A._OverrideReads.__getitem__` | `experiments/track_c/c10y_directdw_arms.py:1638` |
| `A._OverrideReads.__init__` | `experiments/track_c/c10y_directdw_arms.py:1636` |
| `A._accumulation_check` | `experiments/track_c/c10y_directdw_arms.py:2309` |
| `A._actual_updates` | `experiments/track_c/c10y_directdw_arms.py:1671` |
| `A._all_registries` | `experiments/track_c/c10y_directdw_arms.py:2354` |
| `A._anchor_diagnostics` | `experiments/track_c/c10y_directdw_arms.py:1745` |
| `A._anchor_rows` | `experiments/track_c/c10y_directdw_arms.py:1728` |
| `A._calibration_phase` | `experiments/track_c/c10y_directdw_arms.py:753` |
| `A._calibration_timings` | `experiments/track_c/c10y_directdw_arms.py:700` |
| `A._check_record` | `experiments/track_c/c10y_directdw_arms.py:2359` |
| `A._counts` | `experiments/track_c/c10y_directdw_arms.py:2388` |
| `A._covariances` | `experiments/track_c/c10y_directdw_arms.py:1688` |
| `A._decode_ids` | `experiments/track_c/c10y_directdw_arms.py:1787` |
| `A._directed_distance` | `experiments/track_c/c10y_directdw_arms.py:1663` |
| `A._engine_batch_reference` | `experiments/track_c/c10y_directdw_arms.py:2187` |
| `A._fixed_padding` | `experiments/track_c/c10y_directdw_arms.py:2261` |
| `A._forecast_workload` | `experiments/track_c/c10y_directdw_arms.py:683` |
| `A._gradient_check` | `experiments/track_c/c10y_directdw_arms.py:2337` |
| `A._gradient_evaluations` | `experiments/track_c/c10y_directdw_arms.py:2271` |
| `A._js64` | `experiments/track_c/c10y_directdw_arms.py:1676` |
| `A._key_records` | `experiments/track_c/c10y_directdw_arms.py:1631` |
| `A._ledger_call` | `experiments/track_c/c10y_directdw_arms.py:1642` |
| `A._locpct64` | `experiments/track_c/c10y_directdw_arms.py:1684` |
| `A._objective_audit` | `experiments/track_c/c10y_directdw_arms.py:2200` |
| `A._pristine_anchor` | `experiments/track_c/c10y_directdw_arms.py:1759` |
| `A._probe_pristine` | `experiments/track_c/c10y_directdw_arms.py:1863` |
| `A._remaining_readout` | `experiments/track_c/c10y_directdw_arms.py:1880` |
| `A._request_keys` | `experiments/track_c/c10y_directdw_arms.py:1627` |
| `A._stored_reference_checks` | `experiments/track_c/c10y_directdw_arms.py:1894` |
| `A._unit` | `experiments/track_c/c10y_directdw_arms.py:1592` |
| `A._workload` | `experiments/track_c/c10y_directdw_arms.py:1610` |
| `A._write_proof` | `experiments/track_c/c10y_directdw_arms.py:2363` |
| `A.accepted_step` | `experiments/track_c/c10y_directdw_arms.py:368` |
| `A.anchor_loss` | `experiments/track_c/c10y_directdw_arms.py:351` |
| `A.apply_stored` | `experiments/track_c/c10y_directdw_arms.py:418` |
| `A.assert_no_mps_double` | `experiments/track_c/c10y_directdw_arms.py:150` |
| `A.band_hashes` | `experiments/track_c/c10y_directdw_arms.py:212` |
| `A.budget_gate` | `experiments/track_c/c10y_directdw_arms.py:810` |
| `A.calibrate` | `experiments/track_c/c10y_directdw_arms.py:1302` |
| `A.calibration_forecast` | `experiments/track_c/c10y_directdw_arms.py:1190` |
| `A.calibration_identity` | `experiments/track_c/c10y_directdw_arms.py:1184` |
| `A.calibration_timing_tags` | `experiments/track_c/c10y_directdw_arms.py:1615` |
| `A.capture_solve` | `experiments/track_c/c10y_directdw_arms.py:220` |
| `A.compile_accounting` | `experiments/track_c/c10y_directdw_arms.py:1941` |
| `A.context_evidence` | `experiments/track_c/c10y_directdw_arms.py:908` |
| `A.control_match` | `experiments/track_c/c10y_directdw_arms.py:412` |
| `A.cosine` | `experiments/track_c/c10y_directdw_arms.py:163` |
| `A.cpu64` | `experiments/track_c/c10y_directdw_arms.py:155` |
| `A.deployed_hook` | `experiments/track_c/c10y_directdw_arms.py:254` |
| `A.diagnostic_path` | `experiments/track_c/c10y_directdw_arms.py:1237` |
| `A.digest` | `experiments/track_c/c10y_directdw_arms.py:68` |
| `A.edit_components` | `experiments/track_c/c10y_directdw_arms.py:318` |
| `A.effective_weight` | `experiments/track_c/c10y_directdw_arms.py:251` |
| `A.environment_identity` | `experiments/track_c/c10y_directdw_arms.py:113` |
| `A.factor_solve` | `experiments/track_c/c10y_directdw_arms.py:199` |
| `A.fingerprint_record` | `experiments/track_c/c10y_directdw_arms.py:119` |
| `A.frame_subjects_ast_check` | `experiments/track_c/c10y_directdw_arms.py:1586` |
| `A.freeze_contexts` | `experiments/track_c/c10y_directdw_arms.py:892` |
| `A.gram_norm` | `experiments/track_c/c10y_directdw_arms.py:184` |
| `A.hook_snapshot` | `experiments/track_c/c10y_directdw_arms.py:266` |
| `A.input_identity` | `experiments/track_c/c10y_directdw_arms.py:1338` |
| `A.instrument_prefix` | `experiments/track_c/c10y_directdw_arms.py:2393` |
| `A.launch_documents` | `experiments/track_c/c10y_directdw_arms.py:671` |
| `A.main` | `experiments/track_c/c10y_directdw_arms.py:1523` |
| `A.make_scorer` | `experiments/track_c/c10y_directdw_arms.py:1024` |
| `A.memory_gate` | `experiments/track_c/c10y_directdw_arms.py:620` |
| `A.merged_fit` | `experiments/track_c/c10y_directdw_arms.py:1766` |
| `A.microbatch_indices` | `experiments/track_c/c10y_directdw_arms.py:363` |
| `A.norm` | `experiments/track_c/c10y_directdw_arms.py:160` |
| `A.norm_ratio` | `experiments/track_c/c10y_directdw_arms.py:176` |
| `A.normalize_recipe` | `experiments/track_c/c10y_directdw_arms.py:2050` |
| `A.null_share` | `experiments/track_c/c10y_directdw_arms.py:189` |
| `A.output_path` | `experiments/track_c/c10y_directdw_arms.py:1224` |
| `A.overlap_audit` | `experiments/track_c/c10y_directdw_arms.py:925` |
| `A.owned_launch` | `experiments/track_c/c10y_directdw_arms.py:1215` |
| `A.packed_batches` | `experiments/track_c/c10y_directdw_arms.py:300` |
| `A.persist_prefix` | `experiments/track_c/c10y_directdw_arms.py:1252` |
| `A.pinned_templates` | `experiments/track_c/c10y_directdw_arms.py:881` |
| `A.preflight` | `experiments/track_c/c10y_directdw_arms.py:129` |
| `A.projector_gate` | `experiments/track_c/c10y_directdw_arms.py:194` |
| `A.record_manifest` | `experiments/track_c/c10y_directdw_arms.py:1351` |
| `A.refuse_schedule_halt` | `experiments/track_c/c10y_directdw_arms.py:876` |
| `A.relative_distance` | `experiments/track_c/c10y_directdw_arms.py:171` |
| `A.reproduction_record` | `experiments/track_c/c10y_directdw_arms.py:1268` |
| `A.request_batch` | `experiments/track_c/c10y_directdw_arms.py:281` |
| `A.request_weights` | `experiments/track_c/c10y_directdw_arms.py:364` |
| `A.rerun_provenance` | `experiments/track_c/c10y_directdw_arms.py:1290` |
| `A.restore` | `experiments/track_c/c10y_directdw_arms.py:215` |
| `A.run` | `experiments/track_c/c10y_directdw_arms.py:1368` |
| `A.sample_memory` | `experiments/track_c/c10y_directdw_arms.py:628` |
| `A.save_tensors` | `experiments/track_c/c10y_directdw_arms.py:1244` |
| `A.schedule_halt` | `experiments/track_c/c10y_directdw_arms.py:871` |
| `A.scientific_readouts` | `experiments/track_c/c10y_directdw_arms.py:1952` |
| `A.scored_recipe` | `experiments/track_c/c10y_directdw_arms.py:2081` |
| `A.scorer_ast_check` | `experiments/track_c/c10y_directdw_arms.py:1040` |
| `A.selftest_root` | `experiments/track_c/c10y_directdw_arms.py:101` |
| `A.sha` | `experiments/track_c/c10y_directdw_arms.py:61` |
| `A.size_scales` | `experiments/track_c/c10y_directdw_arms.py:405` |
| `A.source_hashes` | `experiments/track_c/c10y_directdw_arms.py:109` |
| `A.stage_context_source` | `experiments/track_c/c10y_directdw_arms.py:914` |
| `A.stored_weight` | `experiments/track_c/c10y_directdw_arms.py:248` |
| `A.strict_json` | `experiments/track_c/c10y_directdw_arms.py:72` |
| `A.strict_load` | `experiments/track_c/c10y_directdw_arms.py:87` |
| `A.supervise` | `experiments/track_c/c10y_directdw_arms.py:1477` |
| `A.sync` | `experiments/track_c/c10y_directdw_arms.py:614` |
| `A.telemetry_admission` | `experiments/track_c/c10y_directdw_arms.py:1090` |
| `A.telemetry_bound` | `experiments/track_c/c10y_directdw_arms.py:1063` |
| `A.telemetry_factory` | `experiments/track_c/c10y_directdw_arms.py:1020` |
| `A.telemetry_mps_inertness_check` | `experiments/track_c/c10y_directdw_arms.py:1105` |
| `A.telemetry_workload` | `experiments/track_c/c10y_directdw_arms.py:1057` |
| `A.tensor_sha` | `experiments/track_c/c10y_directdw_arms.py:207` |
| `A.threshold_stop` | `experiments/track_c/c10y_directdw_arms.py:365` |
| `A.total_loss` | `experiments/track_c/c10y_directdw_arms.py:348` |
| `A.train_deploy_parity` | `experiments/track_c/c10y_directdw_arms.py:1800` |
| `A.utc` | `experiments/track_c/c10y_directdw_arms.py:57` |
| `A.validate_inertness` | `experiments/track_c/c10y_directdw_arms.py:1052` |
| `A.weight_hooks` | `experiments/track_c/c10y_directdw_arms.py:271` |
| `A.write_geometry` | `experiments/track_c/c10y_directdw_arms.py:1704` |
| `A.write_json` | `experiments/track_c/c10y_directdw_arms.py:90` |
| `C._LineError.__init__` | `experiments/track_c/c10y_directdw_telemetry_check.py:150` |
| `C._bounded_path` | `experiments/track_c/c10y_directdw_telemetry_check.py:44` |
| `C._check` | `experiments/track_c/c10y_directdw_telemetry_check.py:91` |
| `C._disabled_markers` | `experiments/track_c/c10y_directdw_telemetry_check.py:374` |
| `C._expected_answers` | `experiments/track_c/c10y_directdw_telemetry_check.py:314` |
| `C._fields` | `experiments/track_c/c10y_directdw_telemetry_check.py:155` |
| `C._integer` | `experiments/track_c/c10y_directdw_telemetry_check.py:174` |
| `C._matrix` | `experiments/track_c/c10y_directdw_telemetry_check.py:199` |
| `C._new_file` | `experiments/track_c/c10y_directdw_telemetry_check.py:56` |
| `C._norms` | `experiments/track_c/c10y_directdw_telemetry_check.py:188` |
| `C._number` | `experiments/track_c/c10y_directdw_telemetry_check.py:178` |
| `C._prepare` | `experiments/track_c/c10y_directdw_telemetry_check.py:79` |
| `C._publish` | `experiments/track_c/c10y_directdw_telemetry_check.py:60` |
| `C._require` | `experiments/track_c/c10y_directdw_telemetry_check.py:19` |
| `C._strict_json` | `experiments/track_c/c10y_directdw_telemetry_check.py:28` |
| `C._text` | `experiments/track_c/c10y_directdw_telemetry_check.py:170` |
| `C._typed` | `experiments/track_c/c10y_directdw_telemetry_check.py:165` |
| `C._utc` | `experiments/track_c/c10y_directdw_telemetry_check.py:24` |
| `C._validate_line` | `experiments/track_c/c10y_directdw_telemetry_check.py:207` |
| `C.audit` | `experiments/track_c/c10y_directdw_telemetry_check.py:397` |
| `C.main` | `experiments/track_c/c10y_directdw_telemetry_check.py:479` |
| `C.run` | `experiments/track_c/c10y_directdw_telemetry_check.py:142` |
| `R._Refusal.__init__` | `experiments/track_c/c10y_directdw_read.py:33` |
| `R._attribute` | `experiments/track_c/c10y_directdw_read.py:678` |
| `R._base` | `experiments/track_c/c10y_directdw_read.py:602` |
| `R._baseline` | `experiments/track_c/c10y_directdw_read.py:197` |
| `R._check_names` | `experiments/track_c/c10y_directdw_read.py:352` |
| `R._checks` | `experiments/track_c/c10y_directdw_read.py:363` |
| `R._complete` | `experiments/track_c/c10y_directdw_read.py:112` |
| `R._control_fidelity` | `experiments/track_c/c10y_directdw_read.py:657` |
| `R._current_identity` | `experiments/track_c/c10y_directdw_read.py:856` |
| `R._digest` | `experiments/track_c/c10y_directdw_read.py:87` |
| `R._disagreement` | `experiments/track_c/c10y_directdw_read.py:716` |
| `R._file_sha` | `experiments/track_c/c10y_directdw_read.py:847` |
| `R._finite_tree` | `experiments/track_c/c10y_directdw_read.py:76` |
| `R._fit` | `experiments/track_c/c10y_directdw_read.py:500` |
| `R._flags` | `experiments/track_c/c10y_directdw_read.py:288` |
| `R._geometry` | `experiments/track_c/c10y_directdw_read.py:224` |
| `R._identity` | `experiments/track_c/c10y_directdw_read.py:131` |
| `R._input_path` | `experiments/track_c/c10y_directdw_read.py:125` |
| `R._integer` | `experiments/track_c/c10y_directdw_read.py:61` |
| `R._layers` | `experiments/track_c/c10y_directdw_read.py:213` |
| `R._ledger` | `experiments/track_c/c10y_directdw_read.py:463` |
| `R._locality` | `experiments/track_c/c10y_directdw_read.py:271` |
| `R._locality_failures` | `experiments/track_c/c10y_directdw_read.py:554` |
| `R._map` | `experiments/track_c/c10y_directdw_read.py:43` |
| `R._matrix` | `experiments/track_c/c10y_directdw_read.py:492` |
| `R._metrics` | `experiments/track_c/c10y_directdw_read.py:252` |
| `R._mode` | `experiments/track_c/c10y_directdw_read.py:348` |
| `R._norms` | `experiments/track_c/c10y_directdw_read.py:569` |
| `R._number` | `experiments/track_c/c10y_directdw_read.py:48` |
| `R._override_keys` | `experiments/track_c/c10y_directdw_read.py:451` |
| `R._recipe_validity` | `experiments/track_c/c10y_directdw_read.py:519` |
| `R._recorded` | `experiments/track_c/c10y_directdw_read.py:100` |
| `R._repro_layers` | `experiments/track_c/c10y_directdw_read.py:722` |
| `R._reproduction` | `experiments/track_c/c10y_directdw_read.py:737` |
| `R._require` | `experiments/track_c/c10y_directdw_read.py:38` |
| `R._required_arms` | `experiments/track_c/c10y_directdw_read.py:108` |
| `R._result` | `experiments/track_c/c10y_directdw_read.py:91` |
| `R._sha` | `experiments/track_c/c10y_directdw_read.py:71` |
| `R._size` | `experiments/track_c/c10y_directdw_read.py:576` |
| `R._strict_json` | `experiments/track_c/c10y_directdw_read.py:827` |
| `R._sum` | `experiments/track_c/c10y_directdw_read.py:594` |
| `R._supervisor` | `experiments/track_c/c10y_directdw_read.py:879` |
| `R._text` | `experiments/track_c/c10y_directdw_read.py:66` |
| `R._trace` | `experiments/track_c/c10y_directdw_read.py:306` |
| `R._train_deploy` | `experiments/track_c/c10y_directdw_read.py:436` |
| `R.classify` | `experiments/track_c/c10y_directdw_read.py:711` |
| `R.cross_process` | `experiments/track_c/c10y_directdw_read.py:769` |
| `R.load` | `experiments/track_c/c10y_directdw_read.py:894` |
| `R.main` | `experiments/track_c/c10y_directdw_read.py:939` |

## Registered test list and final mapping

## Test list registered before production code

The following list was written before any production module existed. Every family includes its failing and passing boundaries where applicable; individual test names and implementation line mappings will be filled from the final source. Tests use the real production entry points with injected CPU-only `H`, not reimplementations of their gate decisions.

Supplemental families (registered before the corresponding review fix or amendment implementation; their RED/GREEN logs will be reported separately): 66 strict C3 calibration-to-forecast map and producer metadata (§10 C2/C3/C5); 67 Amendment P pin/no sampling/all halt identities (§11 P1–P6); 68 per-kind T10 measured bounds and bytes-read-once admission; 69 real driver→saved JSON/PT→reader stage transport, synthetic science explicitly labelled; 70 requested-stage forecast and telemetry-pair refusal before dispatch (§2.6:91–98,T9); 71 independent supervisor's pinned-context halt records (§11 P3); 72 T8 overlap audit before its first batch/forward (§11 P2); 73 serialized overlay bundle SHA/member and committed band identity (§2.7:117,V11); 74 complete wrapper/norms→readout compile accounting (§2.9:146,W2). Existing families were not replaced; stronger review regressions are additional evidence.

1. Fixed reader decision order, named halt/invalid/budget outcomes before missing records — prereg:183,204,293; brief §6 Reader.
2. Own-recipe and V5 completeness; missing size/anchor comparators remain attribution qualifiers; stage-1 NOT-RUN arms exempt — prereg:204,224,232.
3. V1 fingerprint hash/site-count/full output failures individually — prereg:186.
4. V2 every scored recipe's standing LAW#5 verdict — prereg:187.
5. V3 scoped checks and required substitutions for stored-update paths — prereg:123–127,188.
6. V4 all inclusive A7 windows, denominators, A1/A2 67/68 boundaries — prereg:189.
7. V5 candidate A1/A2 67/68 in full stages — prereg:190.
8. V6 declared/consumed override ledger and NOT-RUN states — prereg:87,191.
9. V7 planned and actual null shares 0.999/0.9989999; zero updates explicit — prereg:133,192.
10. V8 string count must cover whole-sequence count — prereg:193.
11. V9 initial/final train–deploy parity, total and every component tolerance, stored-update exemption — prereg:132,194.
12. V10 retry count 5/6; accepted steps counted separately — prereg:70,195.
13. V11 full input/output/artifact identities and complete trace fields — prereg:115–117,179,196.
14. V12 clean frozen-input overlap audit; source/input drift — prereg:85–86,197.
15. V13 finite required values and justified diagnostic nulls with denominators/reasons — prereg:198.
16. FIT-E2E minimum 0.90/0.8999999 and canon 20/19, every required arm and every stop — prereg:200.
17. FIT-Z mean 1e-3/1.000001e-3 and max ratio 0.05/0.0500001, per-arm and zero-denominator rule — prereg:52,202.
18. All S1–S7 rows; screen threshold max(19,a+10); baseline endpoints a=5/18 — prereg:206–218.
19. All P1–P7 rows, n=18/19/29/30 and gain=9/10 — prereg:220–232,291.
20. All X1–X3 rows; real absent/halted second process; blocking-qualifier union — prereg:234–242.
21. R1 cosine 0.99/0.9899999, distance 0.10/0.1000001, both/one zero, baseline-instrument failure — prereg:245.
22. R2 count differences 5/6 and R3 keyed boolean disagreements d_A+3/+4 — prereg:246–247.
23. G1 and each G2 frame A+1/A+2 without pooling — prereg:250.
24. Raw G3 A−3/A−3.01, G4 29/28, raw G5 A+0.5/A+0.51; rounded substitutes refused — prereg:142,250.
25. W1 1.5/1.5000001 and W2 3599.999/3600; EXCEEDS-TTL alone nonblocking — prereg:232,252.
26. Control-positive validity/fit/locality/actual-size, required NM/ENV, n_eff — prereg:255–256.
27. T1 anchor differences 9/10 including (12,22,13)/(12,23,13), and missing/unfit sham — prereg:257–258.
28. ANCHOR-SHAM-INERT ratio 0.8/1.25 and count difference 5/6, descriptor only — prereg:259.
29. Every authored truth-table row and every freeze case including exact 7200-second projection — prereg:263–291.
30. Preflight refusal of every inherited knob/model/revision/device override before harness import — prereg:85; brief §4.1.
31. Go/spend identity and finite positive caps; stage-2 screen and stage-3 attributed-survivor eligibility — prereg:91,309; brief §10 Q8.
32. Frozen contexts sampled once, hashed and installed before later LAW#5; leakage HALT without redraw — prereg:86; brief §6 Driver.
33. Wrapper mode None and dynamically read LAW5 flag delegate; stage-1 ARMS/scorer restoration on exceptions — prereg:88; Amendment T:488–502.
34. Sequential capture algebra and protected-span response; zero-step and exactly three forced zero-lr iterations — prereg:41–47,125–131.
35. Effective fp16 arithmetic, F.linear hook, routing-forward identity and causal gradients; absent base grads — prereg:51,70,73.
36. Engine-shaped prompt/label/lookup construction; target-only head, per-request means and single KL coefficient, including nonzero intervention — prereg:51,134.
37. Four-by-six full-batch weighting; fixed 12-request parity with 6+6/5+7; guard-before-reference allocation — prereg:71,134.
38. Overflow transaction rollback, scale halves, no Adam-state/counter mutation; sixth retry HALT — prereg:70,195.
39. Strict e2e stop L<0.05, inclusive anchor stop ≤1e−4, unchanged T_max=100 — prereg:63–64,98.
40. Anchor zero/zero contributes zero; nonzero/zero INVALID without masked division — prereg:52,202.
41. NM/ENV trigger/scale/zero-reference/equality/direction and stored-update arithmetic; never scale up — prereg:80–81,99–103,255.
42. Unknown hook registries preserved and writer handles removed; pristine restore hashes verified — prereg:85,136.
43. Actual run order has no candidate forward/backward/optimizer/smoke/size/lens before LAW#3; persistent schedule halt across rerun directories — prereg:89,189,458–461,688.
44. Complete phase forecast with evidence SHA/workload/repetitions/scaling; UNVERIFIED refusal; equality at cap — prereg:92–94; brief §10 Q4.
45. Independent supervisor kills isolated blocking workers at deadline, owns only its group, and distinguishes before/after completed write — prereg:96–98; brief §5.5.
46. In-run phase/step projections and ≥1380-second stage-1 readout reserve; unchanged optimizer/batch — prereg:98.
47. Every memory threshold at equality and one byte outside; combined driver+RSS; missing samples — prereg:169.
48. CPU-first float64 helpers, full 2048×11008 regression, perturbed dense references and Gram identity; fp32 mutant killed — brief R3,§5.6; prereg:70,544–548.
49. Telemetry default off, no object/directory/scorer rebind; exact switch and strict INERT/source/env/path admission before writes — Amendment T:426–436,609,618–625.
50. Exact scorer/reference-capture AST and generated IDs/model-input sequence — Amendment T:497–501,562–563,582–586.
51. Every telemetry kind/schema/placement, 96 answers per evaluated arm, accepted-step line formula and stage volumes — Amendment T:438–479,503–519,570.
52. Telemetry preserves parameter/buffer values and pointers, RNG/mode/hooks/grad mode/A.grad, trajectory, records, ledger, file set and operational call counts — Amendment T:526–569.
53. Init/write/flush/fsync failure emits exactly one stderr disable marker; KeyboardInterrupt propagates — Amendment T:535–542; brief §6 T5.
54. Stub P1/T/P2 INERT/NOT-INERT/NONDETERMINISTIC/INVALID; IDs and incomplete telemetry; runner invokes no writer/recipe/LAW5/edit function — Amendment T:573–610; brief §6 T8.
55. Full-size per-kind timing evidence and telemetry forecast refusal; no borrowed bound; reader never reads telemetry — Amendment T:597–609,628–646,671.
56. Model-free answer audit detects mismatch/duplicate/missing/malformed/unexpected/disabled and exact round-trips — Amendment T:648–670.
57. Audit guard before imports, positive control, test-base meta-check, child guard marker/identity/path escapes, listing backstop, launcher SELFTEST refusal — brief §5.5; Amendment T:551.
58. End-to-end injected-H stage 1→2→3 persistence and real reader; earlier artifact hashes preserved; all mandatory proofs/readouts through edited-state hooks — prereg:89–91,123–147,179,674–685.
59. Strict JSON round-trips of every required persisted record, inertness record and telemetry line — brief §6 Round-trips.
60. Final sys.modules assertions and protected SHA table equal before/after — brief R1,R5,§7.

61. Calibration strict stage-1 prefix through (ix), no substantive candidate recipe/write/readout, mandatory merged diagnostic evaluations retained — Amendment C:711–737,890–902.

62. Calibration timing/workload/repetition/padded-length/peaks records and synchronized per-unit measurements — Amendment C:737–775.

63. Calibration namespaces and immutable artifacts, required go/spend/authorization, cap (0,7200], no own forecast, telemetry variables refused — Amendment C:822–889.

64. Forecast cites COMPLETE/current calibration timings only, never contexts/targets/weights/memory, all repetitions and scaling justification; calibration contexts rejected by stages/reader — Amendment C:774–822,879–884.

65. Every directly executed shell dependency must be executable and tracked as mode 100755; the present launch graph directly executes the Python interpreter and driver only. Static launch-graph assertion plus `os.access(X_OK)` and `git ls-files -s` for any shell dependency — program requirement from ASTRA exit 126, received during the build.

75. Inclusive NM one-percent equality through the actual scientific hook and real reader, including total 1.0 versus 1.01 and both sides — prereg:80,255; independent final-review regression registered before fixing those two production comparisons.

Family 32’s original sampled-once wording is superseded by §11: the completed mechanism pins the recorded set without sampling. Supplemental families 66–74 were registered before their respective amendment/review fixes; family 75 was registered before the final actual-path boundary/summation fixes. Fixture/schema repairs are distinguished from production defects in the logs below. The original list is preserved under `/private/tmp/c10y_build/report_registration.md`.

| Family | Tests (all have source lines in the index below) |
|---|---|
| 1 | `ReaderOrderTests.test_recorded_halt_invalid_and_budget_first`; `ReaderOrderTests.test_validity_precedes_fit_and_fit_precedes_counts` |
| 2 | `ReaderOrderTests.test_missing_comparators_qualify_without_incomplete`; `ReaderOrderTests.test_own_record_and_v5_missing_precede_validity_and_fit`; `ReaderOrderTests.test_stage1_not_run_controls_and_later_records_not_required` |
| 3 | `ReaderValidityTests.test_v10_overflow_retries_five_six`; `ReaderValidityTests.test_v11_hin_hashes_and_write_trace_required`; `ReaderValidityTests.test_v12_leakage_named_halt`; `ReaderValidityTests.test_v13_every_applicable_numeric_family_nonfinite`; `ReaderValidityTests.test_v13_nonfinite_unjustified_null_and_typed_integer`; `ReaderValidityTests.test_v13_typed_nulls_and_reasons`; `ReaderValidityTests.test_v1_fingerprint_sha_sites_and_full_output` |
| 4 | `ReaderValidityTests.test_v2_each_recipe_standing_law5` |
| 5 | `ReaderValidityTests.test_v3_accumulation_raw_cosine_distance_finiteness_and_scope`; `ReaderValidityTests.test_v3_apply_stored_substitutions_not_optimiser_checks`; `ReaderValidityTests.test_v3_capture_zero_step_and_executed_loop_raw_values`; `ReaderValidityTests.test_v3_check_failure_order_and_scope`; `ReaderValidityTests.test_v3_gradient_halvings_hooks_and_smoke_raw_values`; `ReaderValidityTests.test_v3_missing_required_check_invalid`; `ReaderValidityTests.test_v3_objective_nll_and_nonzero_kl_raw_boundaries` |
| 6 | `ReaderValidityTests.test_v4_a1_a2_and_exact_denominators`; `ReaderValidityTests.test_v4_all_inclusive_baseline_endpoints`; `ReaderValidityTests.test_v4_before_candidates_required` |
| 7 | `ReaderValidityTests.test_v5_candidate_controls_67_68_each_arm` |
| 8 | `ReaderValidityTests.test_v6_overrides_are_exact_sets_not_counts` |
| 9 | `ReaderValidityTests.test_v7_initial_projector_raw_share_cannot_hide_behind_passed`; `ReaderValidityTests.test_v7_planned_actual_each_layer_boundary_and_zero`; `ReaderValidityTests.test_v7_untouched_reference_miss_halts_precision_diagnosis` |
| 10 | `ReaderValidityTests.test_v8_string_full_equality_and_one_below_every_arm` |
| 11 | `ReaderValidityTests.test_v9_init_final_tokens_and_each_loss_component` |
| 12 | `ReaderValidityTests.test_v10_overflow_retries_five_six` |
| 13 | `ReaderValidityTests.test_v11_hin_hashes_and_write_trace_required`; `TransportTests.test_saved_overlay_hash_is_the_immutable_serialized_bundle` |
| 14 | `ReaderOrderTests.test_source_and_prereg_identity_refused`; `ReaderValidityTests.test_v12_leakage_named_halt` |
| 15 | `ReaderValidityTests.test_v13_every_applicable_numeric_family_nonfinite`; `ReaderValidityTests.test_v13_nonfinite_unjustified_null_and_typed_integer`; `ReaderValidityTests.test_v13_typed_nulls_and_reasons` |
| 16 | `ReaderFitAndScreenTests.test_fit_e2e_minimum_canonical_and_every_stop`; `ReaderFitAndScreenTests.test_fit_per_required_arm_and_apply_stored` |
| 17 | `ReaderFitAndScreenTests.test_fit_z_mean_and_maximum_boundaries`; `ReaderFitAndScreenTests.test_fit_z_zero_denominator_named_rule` |
| 18 | `ReaderFitAndScreenTests.test_s1_named_halts_without_screen_label`; `ReaderFitAndScreenTests.test_s2_s3_budget_write_boundary`; `ReaderFitAndScreenTests.test_s4_fit_precedes_high_count_locality_and_size`; `ReaderFitAndScreenTests.test_s5_s7_envelope_and_gain_boundaries`; `ReaderFitAndScreenTests.test_s6_size_boundary_and_null_first_match` |
| 19 | `ReaderProcessLocalityTests.test_p1_p2_p3`; `ReaderProcessLocalityTests.test_p4_p5_p7_count_and_gain_boundaries`; `ReaderProcessLocalityTests.test_p6_tradeoff_and_p7_null_first_match` |
| 20 | `ReaderCrossProcessTests.test_x1_not_run_halted_and_incomplete_never_fabricated_null`; `ReaderCrossProcessTests.test_x2_identical_labels_and_union_qualifiers`; `ReaderCrossProcessTests.test_x3_mixed_labels_store_actual_counts` |
| 21 | `ReaderCrossProcessTests.test_r1_cosine_and_distance_every_layer_boundaries`; `ReaderCrossProcessTests.test_r1_required_controls_and_all_arms_independent`; `ReaderCrossProcessTests.test_r1_zero_norm_rules_and_baseline_instrument` |
| 22 | `ReaderCrossProcessTests.test_r2_count_spread_five_six`; `ReaderCrossProcessTests.test_r3_incorrect_strings_do_not_count_as_disagreement`; `ReaderCrossProcessTests.test_r3_keyed_boolean_disagreement_da_plus_three_four` |
| 23 | `ReaderProcessLocalityTests.test_g1_g2_each_frame_both_sides` |
| 24 | `ReaderProcessLocalityTests.test_g3_g4_g5_unrounded_boundaries`; `ReaderProcessLocalityTests.test_g3_g5_display_rounding_cannot_substitute` |
| 25 | `ReaderProcessLocalityTests.test_w1_actual_size_boundary_qualifier_preserves_base`; `ReaderProcessLocalityTests.test_w2_ttl_warning_equality_nonblocking` |
| 26 | `ReaderAttributionTests.test_control_positive_requires_envelope_gain_fit_locality_and_validity`; `ReaderAttributionTests.test_neff_minimum_and_anchor_gap_nine_ten`; `ReaderAttributionTests.test_no_downscale_controls_required_at_actual_ratio_one`; `ReaderAttributionTests.test_size_control_matching_and_direction_boundaries`; `ReaderAttributionTests.test_total_and_per_layer_growth_trigger_independent_controls` |
| 27 | `ReaderAttributionTests.test_anchor_comparison_does_not_require_bz_sized_gain`; `ReaderAttributionTests.test_anchor_missing_invalid_and_unfit_untested`; `ReaderAttributionTests.test_neff_minimum_and_anchor_gap_nine_ten` |
| 28 | `ReaderAttributionTests.test_anchor_sham_descriptor_windows_not_fit_or_validity` |
| 29 | `ReaderFitAndScreenTests.test_stage1_recorded_projection_exactly_120_minutes_fits`; `ReaderTruthTableTests.test_authored_full_truth_rows_277_289`; `ReaderTruthTableTests.test_authored_stage1_truth_rows_265_276` |
| 30 | `IntegrationTests.test_actual_launcher_refuses_missing_calibration_before_import`; `LaunchTests.test_every_inherited_preflight_knob_refused` |
| 31 | `CalibrationTests.test_calibration_go_spend_caps`; `LaunchTests.test_go_spend_and_stage_eligibility`; `TransportTests.test_wrong_stage3_predecessor_refuses_in_main_before_harness_or_supervisor` |
| 32 | `LaunchTests.test_context_freeze_and_leakage`; `PinnedTemplateTests.test_changed_template_source_or_stage1_content_halts`; `PinnedTemplateTests.test_stage1_and_calibration_pin_before_first_engine_call`; `PinnedTemplateTests.test_stages2_3_install_stage1_bytes_before_first_engine_use`; `PinnedTemplateTests.test_t8_digest_failure_has_halt_diagnostic_before_scoring`; `PinnedTemplateTests.test_t8_installs_pin_and_writes_context_before_any_pass` |
| 33 | `FinalReviewRegressionTests.test_off_scorer_is_original_during_actual_recipe_call`; `LaunchTests.test_wrapper_delegate_dynamic_and_arm_restore` |
| 34 | `IntegrationTests.test_sequential_capture_matches_original`; `IntegrationTests.test_three_forced_zero_lr_iterations_and_telemetry_trajectory`; `NumericTests.test_capture_factorization` |
| 35 | `IntegrationTests.test_three_forced_zero_lr_iterations_and_telemetry_trajectory`; `OptimizerTests.test_effective_weight_and_routing_gradient` |
| 36 | `OptimizerTests.test_kl_coefficient_once`; `OptimizerTests.test_request_batch_and_target_only_objective` |
| 37 | `FinalReviewRegressionTests.test_live_objective_graph_guard_precedes_backward_and_adam`; `OptimizerTests.test_microbatch_request_weighting`; `ReaderValidityTests.test_v3_accumulation_raw_cosine_distance_finiteness_and_scope` |
| 38 | `OptimizerTests.test_loss_scale_transaction`; `OptimizerTests.test_sixth_overflow_halts_without_mutation` |
| 39 | `OptimizerTests.test_stopping_boundaries` |
| 40 | `NumericTests.test_anchor_zero_denominator`; `ReaderFitAndScreenTests.test_fit_z_zero_denominator_named_rule` |
| 41 | `IntegrationTests.test_stored_control_scale1_identity`; `NumericTests.test_control_boundaries`; `NumericTests.test_size_scales_and_stored_arithmetic`; `ReaderAttributionTests.test_size_control_matching_and_direction_boundaries` |
| 42 | `LaunchTests.test_wrapper_delegate_dynamic_and_arm_restore`; `OptimizerTests.test_unknown_hooks_preserved` |
| 43 | `CalibrationTests.test_calibration_v4_halt_persists_schedule`; `IntegrationTests.test_candidate_operations_require_baseline`; `IntegrationTests.test_stage_runner_artifacts_feed_real_reader_and_halt_before_candidates` |
| 44 | `CalibrationForecastContractTests.test_all_three_targets_and_baseline_arm_timings_required`; `CalibrationForecastContractTests.test_bad_bound_records_return_unverified`; `CalibrationForecastContractTests.test_calibration_schema_and_c5_completeness`; `CalibrationForecastContractTests.test_cap_types_stage1_limit_and_later_stage_spend`; `CalibrationForecastContractTests.test_each_phase_rejects_wrong_measured_mapping`; `CalibrationForecastContractTests.test_full_c3_measured_map_and_every_repetition`; `CalibrationForecastContractTests.test_independent_bound_requires_explicit_justification`; `CalibrationForecastContractTests.test_input_identity_drift_and_padded_max_are_invalid`; `CalibrationForecastContractTests.test_merge_uses_larger_of_two_timed_merges`; `CalibrationForecastContractTests.test_missing_c3_unit_is_not_complete_support`; `CalibrationForecastContractTests.test_noncalibration_measured_flag_cannot_replace_supported_bound`; `CalibrationForecastContractTests.test_optimisation_comparable_shape_and_iteration_flags`; `CalibrationForecastContractTests.test_optimisation_full_105_attempt_stage_workload`; `CalibrationForecastContractTests.test_optimisation_requires_three_accepted_rows_in_each_check`; `CalibrationForecastContractTests.test_optimisation_uses_slowest_iteration_not_mean`; `CalibrationForecastContractTests.test_original_my_edit_requires_two_distinct_repetitions`; `CalibrationForecastContractTests.test_overflow_attempt_is_cited_in_addition_to_six_accepted_rows`; `CalibrationForecastContractTests.test_prestart_gate_rechecks_schema_and_staleness`; `CalibrationForecastContractTests.test_prestart_gate_rejects_forged_or_omitted_measurement`; `CalibrationForecastContractTests.test_raw_seconds_sync_status_and_workload_are_typed`; `CalibrationForecastContractTests.test_readout_1380_reserve_and_larger_measured_bound`; `LaunchTests.test_forecast_unverified_and_cap` |
| 45 | `IntegrationTests.test_native_hanging_worker_deadline_before_and_after_write`; `LaunchDeltaTests.test_supervisor_timeout_records_observed_template_hash_without_child` |
| 46 | `FinalReviewRegressionTests.test_each_telemetry_method_preserves_every_state_and_A_grad`; `FinalReviewRegressionTests.test_forecast_aware_first_expensive_action_is_not_entered`; `FinalReviewRegressionTests.test_premerge_parity_cannot_spend_postmerge_reserve`; `LaunchTests.test_step_projection_reserves_readout` |
| 47 | `FinalReviewRegressionTests.test_live_objective_graph_guard_precedes_backward_and_adam`; `LaunchTests.test_memory_boundaries` |
| 48 | `NumericTests.test_full_size_float64_reductions`; `NumericTests.test_gram_norm_dense_reference`; `NumericTests.test_mps_double_refused` |
| 49 | `TelemetryForecastTests.test_inertness_bytes_once_and_duplicate_nonfinite_refused`; `TelemetryTests.test_invalid_switches_refused_before_write`; `TelemetryTests.test_off_has_no_object_or_directory` |
| 50 | `TelemetryTests.test_scorer_ast_and_exact_inputs` |
| 51 | `FinalReviewRegressionTests.test_real_writer_per_write_line_formula`; `TelemetryForecastTests.test_full_stage_counts_and_payload_not_smaller`; `TelemetryTests.test_every_kind_state_preservation_and_volume` |
| 52 | `FinalReviewRegressionTests.test_each_telemetry_method_preserves_every_state_and_A_grad`; `IntegrationTests.test_three_forced_zero_lr_iterations_and_telemetry_trajectory`; `TransportTests.test_telemetry_off_on_transport_changes_only_T1_fields_at_every_stage` |
| 53 | `TelemetryTests.test_io_failures_disable_once_and_baseexception_propagates` |
| 54 | `TelemetryCheckContract.test_T8_runner_inert_pristine_stub_never_calls_writer_or_recipe`; `TelemetryCheckContract.test_T8_runner_other_verdicts_exit_zero_and_preserve_verdict`; `TelemetryCheckContract.test_T8_runner_preflight_refuses_knob_before_output_creation`; `TelemetryCheckContract.test_T8_runner_preserves_existing_record`; `TelemetryCheckContract.test_T8_runner_records_complete_current_identity_and_strict_roundtrip`; `TelemetryCheckContract.test_T8_runner_rejects_namespace_itself_and_nested_subdirectories`; `TelemetryCheckContract.test_T8_runner_rejects_output_outside_namespace`; `TelemetryCheckContract.test_T8_runner_rejects_relative_output_before_writes`; `TelemetryCheckContract.test_T8_runner_rejects_symlink_escape`; `TelemetryCheckContract.test_T8_runner_weight_change_is_invalid_exit_two`; `TelemetryTests.test_inertness_and_drifting_baseline`; `TelemetryTests.test_t8_serialized_wrong_answer_is_not_inert` |
| 55 | `TelemetryCheckContract.test_T11_reader_does_not_open_telemetry_or_use_audit_as_gate`; `TelemetryForecastTests.test_full_stage_counts_and_payload_not_smaller`; `TelemetryForecastTests.test_inertness_bytes_once_and_duplicate_nonfinite_refused`; `TelemetryForecastTests.test_on_requires_separate_phase_before_dispatch`; `TelemetryForecastTests.test_per_kind_measurements_workload_and_sum_enforced` |
| 56 | `TelemetryCheckContract.test_T11_audit_accepts_every_kind_with_only_kind_specific_fields`; `TelemetryCheckContract.test_T11_audit_checks_payload_types_for_every_non_answer_kind`; `TelemetryCheckContract.test_T11_audit_complete_answer_keys_pass_and_roundtrip`; `TelemetryCheckContract.test_T11_audit_declared_disabled_missing_output_keeps_science_record`; `TelemetryCheckContract.test_T11_audit_disabled_marker_does_not_excuse_a_gap_before_later_answers`; `TelemetryCheckContract.test_T11_audit_disabled_marker_does_not_excuse_mismatching_existing_line`; `TelemetryCheckContract.test_T11_audit_duplicate_answer_key_compromises_stage`; `TelemetryCheckContract.test_T11_audit_header_must_be_present_initial_and_unique`; `TelemetryCheckContract.test_T11_audit_mismatch_compromises_stage_and_requires_telemetry_off_rerun`; `TelemetryCheckContract.test_T11_audit_missing_answer_field_is_malformed`; `TelemetryCheckContract.test_T11_audit_missing_expected_key_compromises_stage`; `TelemetryCheckContract.test_T11_audit_missing_file_is_missing_output`; `TelemetryCheckContract.test_T11_audit_model_free_entrypoint_never_loads_driver_or_harness`; `TelemetryCheckContract.test_T11_audit_never_mutates_science_records_or_reader_output`; `TelemetryCheckContract.test_T11_audit_refuses_existing_audit_without_rewriting_evidence`; `TelemetryCheckContract.test_T11_audit_rejects_unknown_field_on_every_known_kind`; `TelemetryCheckContract.test_T11_audit_strict_json_rejects_nonfinite_and_duplicate_json_fields`; `TelemetryCheckContract.test_T11_audit_unknown_key_or_kind_or_field_is_unexpected`; `TelemetryCheckContract.test_T11_audit_uses_stage_two_and_three_tags_and_record_paths`; `TelemetryCheckContract.test_T11_audit_wrong_types_and_nulls_are_malformed`; `TelemetryCheckContract.test_T11_reader_does_not_open_telemetry_or_use_audit_as_gate` |
| 57 | `IntegrationTests.test_native_hanging_worker_deadline_before_and_after_write`; `IsolationTests.test_all_cases_use_base`; `IsolationTests.test_live_write_positive_control`; `IsolationTests.test_real_dispatch_denied_with_temp_environment`; `IsolationTests.test_relative_and_symlink_guard`; `IsolationTests.test_selftest_root_refusal` |
| 58 | `TransportTests.test_actual_cpu_update_direction_changes_fail_real_reader_repro_gate`; `TransportTests.test_completed_stage1_runner_to_reader_and_cpu_pt_transport`; `TransportTests.test_completed_three_stages_preserve_common_files_and_compute_real_repro`; `TransportTests.test_tampered_stage2_pt_refuses_stage3_before_scientific_callbacks` |
| 59 | `IntegrationTests.test_strict_json_and_immutable_records`; `TelemetryCheckContract.test_T11_audit_complete_answer_keys_pass_and_roundtrip`; `TelemetryCheckContract.test_T8_runner_records_complete_current_identity_and_strict_roundtrip` |
| 60 | `CalibrationTests.test_frozen_bytes_suite_end`; `IsolationTests.test_all_cases_use_base` |
| 61 | `CalibrationTests.test_calibration_prefix_only_and_required_records`; `CalibrationTests.test_calibration_v4_halt_persists_schedule` |
| 62 | `CalibrationForecastContractTests.test_raw_seconds_sync_status_and_workload_are_typed`; `FinalReviewRegressionTests.test_calibration_callsite_persists_complete_timing_tags`; `LaunchDeltaTests.test_real_iteration_producer_passes_c2_timing_validator` |
| 63 | `CalibrationTests.test_calibration_go_spend_caps`; `CalibrationTests.test_calibration_telemetry_variables_and_existing_directory_refused`; `CalibrationTests.test_calibration_wrong_namespace_refused` |
| 64 | `CalibrationForecastContractTests.test_all_three_targets_and_baseline_arm_timings_required`; `CalibrationForecastContractTests.test_bad_bound_records_return_unverified`; `CalibrationForecastContractTests.test_calibration_schema_and_c5_completeness`; `CalibrationForecastContractTests.test_cap_types_stage1_limit_and_later_stage_spend`; `CalibrationForecastContractTests.test_each_phase_rejects_wrong_measured_mapping`; `CalibrationForecastContractTests.test_full_c3_measured_map_and_every_repetition`; `CalibrationForecastContractTests.test_independent_bound_requires_explicit_justification`; `CalibrationForecastContractTests.test_input_identity_drift_and_padded_max_are_invalid`; `CalibrationForecastContractTests.test_merge_uses_larger_of_two_timed_merges`; `CalibrationForecastContractTests.test_missing_c3_unit_is_not_complete_support`; `CalibrationForecastContractTests.test_noncalibration_measured_flag_cannot_replace_supported_bound`; `CalibrationForecastContractTests.test_optimisation_comparable_shape_and_iteration_flags`; `CalibrationForecastContractTests.test_optimisation_full_105_attempt_stage_workload`; `CalibrationForecastContractTests.test_optimisation_requires_three_accepted_rows_in_each_check`; `CalibrationForecastContractTests.test_optimisation_uses_slowest_iteration_not_mean`; `CalibrationForecastContractTests.test_original_my_edit_requires_two_distinct_repetitions`; `CalibrationForecastContractTests.test_overflow_attempt_is_cited_in_addition_to_six_accepted_rows`; `CalibrationForecastContractTests.test_prestart_gate_rechecks_schema_and_staleness`; `CalibrationForecastContractTests.test_prestart_gate_rejects_forged_or_omitted_measurement`; `CalibrationForecastContractTests.test_raw_seconds_sync_status_and_workload_are_typed`; `CalibrationForecastContractTests.test_readout_1380_reserve_and_larger_measured_bound`; `CalibrationTests.test_calibration_forecast_rejects_partial_and_stale`; `CalibrationTests.test_calibration_forecast_uses_all_repetitions_no_memory_or_inputs`; `CalibrationTests.test_calibration_reader_and_context_source_refused` |
| 65 | `LaunchTests.test_direct_launch_shell_dependencies_are_executable_and_git_100755` |
| 66 | `CalibrationForecastContractTests.test_all_three_targets_and_baseline_arm_timings_required`; `CalibrationForecastContractTests.test_bad_bound_records_return_unverified`; `CalibrationForecastContractTests.test_calibration_schema_and_c5_completeness`; `CalibrationForecastContractTests.test_cap_types_stage1_limit_and_later_stage_spend`; `CalibrationForecastContractTests.test_each_phase_rejects_wrong_measured_mapping`; `CalibrationForecastContractTests.test_full_c3_measured_map_and_every_repetition`; `CalibrationForecastContractTests.test_independent_bound_requires_explicit_justification`; `CalibrationForecastContractTests.test_input_identity_drift_and_padded_max_are_invalid`; `CalibrationForecastContractTests.test_merge_uses_larger_of_two_timed_merges`; `CalibrationForecastContractTests.test_missing_c3_unit_is_not_complete_support`; `CalibrationForecastContractTests.test_noncalibration_measured_flag_cannot_replace_supported_bound`; `CalibrationForecastContractTests.test_optimisation_comparable_shape_and_iteration_flags`; `CalibrationForecastContractTests.test_optimisation_full_105_attempt_stage_workload`; `CalibrationForecastContractTests.test_optimisation_requires_three_accepted_rows_in_each_check`; `CalibrationForecastContractTests.test_optimisation_uses_slowest_iteration_not_mean`; `CalibrationForecastContractTests.test_original_my_edit_requires_two_distinct_repetitions`; `CalibrationForecastContractTests.test_overflow_attempt_is_cited_in_addition_to_six_accepted_rows`; `CalibrationForecastContractTests.test_prestart_gate_rechecks_schema_and_staleness`; `CalibrationForecastContractTests.test_prestart_gate_rejects_forged_or_omitted_measurement`; `CalibrationForecastContractTests.test_raw_seconds_sync_status_and_workload_are_typed`; `CalibrationForecastContractTests.test_readout_1380_reserve_and_larger_measured_bound`; `LaunchDeltaTests.test_real_iteration_producer_passes_c2_timing_validator` |
| 67 | `FinalReviewRegressionTests.test_recorded_contexts_never_sample_even_after_seeding`; `PinnedTemplateTests.test_changed_template_source_or_stage1_content_halts`; `PinnedTemplateTests.test_stage1_and_calibration_pin_before_first_engine_call`; `PinnedTemplateTests.test_stages2_3_install_stage1_bytes_before_first_engine_use`; `PinnedTemplateTests.test_t8_digest_failure_has_halt_diagnostic_before_scoring`; `PinnedTemplateTests.test_t8_installs_pin_and_writes_context_before_any_pass` |
| 68 | `TelemetryForecastTests.test_full_stage_counts_and_payload_not_smaller`; `TelemetryForecastTests.test_inertness_bytes_once_and_duplicate_nonfinite_refused`; `TelemetryForecastTests.test_on_requires_separate_phase_before_dispatch`; `TelemetryForecastTests.test_per_kind_measurements_workload_and_sum_enforced` |
| 69 | `TransportTests.test_completed_stage1_runner_to_reader_and_cpu_pt_transport`; `TransportTests.test_completed_three_stages_preserve_common_files_and_compute_real_repro`; `TransportTests.test_telemetry_off_on_transport_changes_only_T1_fields_at_every_stage` |
| 70 | `LaunchDeltaTests.test_later_stage_cannot_consume_stage1_calibration_measurements`; `TransportTests.test_requested_stage_forecast_is_checked_before_dispatch_and_worker`; `TransportTests.test_stage3_pair_mismatch_is_refused_in_parent_before_any_launch_write`; `TransportTests.test_stage3_telemetry_setting_cannot_change_after_stage2` |
| 71 | `LaunchDeltaTests.test_supervisor_timeout_records_observed_template_hash_without_child` |
| 72 | `LaunchDeltaTests.test_t8_overlap_audit_precedes_first_forward_and_never_redraws` |
| 73 | `TransportTests.test_saved_overlay_hash_is_the_immutable_serialized_bundle`; `TransportTests.test_tampered_stage2_pt_refuses_stage3_before_scientific_callbacks` |
| 74 | `FinalReviewRegressionTests.test_complete_compile_accounting_drives_ttl_equality`; `FinalReviewRegressionTests.test_complete_compile_at_actual_scientific_hook_boundary`; `LaunchDeltaTests.test_norm_readouts_are_inside_writer_wall_clock`; `TransportTests.test_real_scored_recipe_accounts_for_scientific_hook_readout_time` |
| 75 | `LaunchDeltaTests.test_nm_decimal_boundary_through_real_reader`; `LaunchDeltaTests.test_nm_decimal_boundary_through_scientific_hook`; `LaunchDeltaTests.test_stored_scale_sum_matches_reader_float64_sum` |

### Every final test name → source line

| Test | Source |
|---|---|
| `CalibrationForecastContractTests.test_all_three_targets_and_baseline_arm_timings_required` | `experiments/track_c/c10y_directdw_selftest.py:2874` |
| `CalibrationForecastContractTests.test_bad_bound_records_return_unverified` | `experiments/track_c/c10y_directdw_selftest.py:3070` |
| `CalibrationForecastContractTests.test_calibration_schema_and_c5_completeness` | `experiments/track_c/c10y_directdw_selftest.py:2996` |
| `CalibrationForecastContractTests.test_cap_types_stage1_limit_and_later_stage_spend` | `experiments/track_c/c10y_directdw_selftest.py:3062` |
| `CalibrationForecastContractTests.test_each_phase_rejects_wrong_measured_mapping` | `experiments/track_c/c10y_directdw_selftest.py:2855` |
| `CalibrationForecastContractTests.test_full_c3_measured_map_and_every_repetition` | `experiments/track_c/c10y_directdw_selftest.py:2841` |
| `CalibrationForecastContractTests.test_independent_bound_requires_explicit_justification` | `experiments/track_c/c10y_directdw_selftest.py:3048` |
| `CalibrationForecastContractTests.test_input_identity_drift_and_padded_max_are_invalid` | `experiments/track_c/c10y_directdw_selftest.py:3008` |
| `CalibrationForecastContractTests.test_merge_uses_larger_of_two_timed_merges` | `experiments/track_c/c10y_directdw_selftest.py:2951` |
| `CalibrationForecastContractTests.test_missing_c3_unit_is_not_complete_support` | `experiments/track_c/c10y_directdw_selftest.py:2862` |
| `CalibrationForecastContractTests.test_noncalibration_measured_flag_cannot_replace_supported_bound` | `experiments/track_c/c10y_directdw_selftest.py:3056` |
| `CalibrationForecastContractTests.test_optimisation_comparable_shape_and_iteration_flags` | `experiments/track_c/c10y_directdw_selftest.py:2906` |
| `CalibrationForecastContractTests.test_optimisation_full_105_attempt_stage_workload` | `experiments/track_c/c10y_directdw_selftest.py:2926` |
| `CalibrationForecastContractTests.test_optimisation_requires_three_accepted_rows_in_each_check` | `experiments/track_c/c10y_directdw_selftest.py:2897` |
| `CalibrationForecastContractTests.test_optimisation_uses_slowest_iteration_not_mean` | `experiments/track_c/c10y_directdw_selftest.py:2933` |
| `CalibrationForecastContractTests.test_original_my_edit_requires_two_distinct_repetitions` | `experiments/track_c/c10y_directdw_selftest.py:2886` |
| `CalibrationForecastContractTests.test_overflow_attempt_is_cited_in_addition_to_six_accepted_rows` | `experiments/track_c/c10y_directdw_selftest.py:2940` |
| `CalibrationForecastContractTests.test_prestart_gate_rechecks_schema_and_staleness` | `experiments/track_c/c10y_directdw_selftest.py:3019` |
| `CalibrationForecastContractTests.test_prestart_gate_rejects_forged_or_omitted_measurement` | `experiments/track_c/c10y_directdw_selftest.py:3036` |
| `CalibrationForecastContractTests.test_raw_seconds_sync_status_and_workload_are_typed` | `experiments/track_c/c10y_directdw_selftest.py:2977` |
| `CalibrationForecastContractTests.test_readout_1380_reserve_and_larger_measured_bound` | `experiments/track_c/c10y_directdw_selftest.py:2961` |
| `CalibrationTests.test_calibration_forecast_rejects_partial_and_stale` | `experiments/track_c/c10y_directdw_selftest.py:833` |
| `CalibrationTests.test_calibration_forecast_uses_all_repetitions_no_memory_or_inputs` | `experiments/track_c/c10y_directdw_selftest.py:2798` |
| `CalibrationTests.test_calibration_go_spend_caps` | `experiments/track_c/c10y_directdw_selftest.py:791` |
| `CalibrationTests.test_calibration_prefix_only_and_required_records` | `experiments/track_c/c10y_directdw_selftest.py:807` |
| `CalibrationTests.test_calibration_reader_and_context_source_refused` | `experiments/track_c/c10y_directdw_selftest.py:827` |
| `CalibrationTests.test_calibration_telemetry_variables_and_existing_directory_refused` | `experiments/track_c/c10y_directdw_selftest.py:797` |
| `CalibrationTests.test_calibration_v4_halt_persists_schedule` | `experiments/track_c/c10y_directdw_selftest.py:820` |
| `CalibrationTests.test_calibration_wrong_namespace_refused` | `experiments/track_c/c10y_directdw_selftest.py:803` |
| `CalibrationTests.test_frozen_bytes_suite_end` | `experiments/track_c/c10y_directdw_selftest.py:851` |
| `FinalReviewRegressionTests.test_calibration_callsite_persists_complete_timing_tags` | `experiments/track_c/c10y_directdw_selftest.py:3360` |
| `FinalReviewRegressionTests.test_complete_compile_accounting_drives_ttl_equality` | `experiments/track_c/c10y_directdw_selftest.py:3350` |
| `FinalReviewRegressionTests.test_complete_compile_at_actual_scientific_hook_boundary` | `experiments/track_c/c10y_directdw_selftest.py:3268` |
| `FinalReviewRegressionTests.test_each_telemetry_method_preserves_every_state_and_A_grad` | `experiments/track_c/c10y_directdw_selftest.py:3223` |
| `FinalReviewRegressionTests.test_forecast_aware_first_expensive_action_is_not_entered` | `experiments/track_c/c10y_directdw_selftest.py:3296` |
| `FinalReviewRegressionTests.test_live_objective_graph_guard_precedes_backward_and_adam` | `experiments/track_c/c10y_directdw_selftest.py:3309` |
| `FinalReviewRegressionTests.test_merged_fit_reduces_vocabulary_on_cpu_float64` | `experiments/track_c/c10y_directdw_selftest.py:3333` |
| `FinalReviewRegressionTests.test_off_scorer_is_original_during_actual_recipe_call` | `experiments/track_c/c10y_directdw_selftest.py:3259` |
| `FinalReviewRegressionTests.test_phase_markers_cover_units_without_changing_operational_calls` | `experiments/track_c/c10y_directdw_selftest.py:3369` |
| `FinalReviewRegressionTests.test_premerge_parity_cannot_spend_postmerge_reserve` | `experiments/track_c/c10y_directdw_selftest.py:3285` |
| `FinalReviewRegressionTests.test_real_writer_durable_merge_precedes_postmerge_readout` | `experiments/track_c/c10y_directdw_selftest.py:3322` |
| `FinalReviewRegressionTests.test_real_writer_per_write_line_formula` | `experiments/track_c/c10y_directdw_selftest.py:3242` |
| `FinalReviewRegressionTests.test_recorded_contexts_never_sample_even_after_seeding` | `experiments/track_c/c10y_directdw_selftest.py:3377` |
| `IntegrationTests.test_actual_launcher_refuses_missing_calibration_before_import` | `experiments/track_c/c10y_directdw_selftest.py:698` |
| `IntegrationTests.test_candidate_operations_require_baseline` | `experiments/track_c/c10y_directdw_selftest.py:676` |
| `IntegrationTests.test_native_hanging_worker_deadline_before_and_after_write` | `experiments/track_c/c10y_directdw_selftest.py:734` |
| `IntegrationTests.test_sequential_capture_matches_original` | `experiments/track_c/c10y_directdw_selftest.py:647` |
| `IntegrationTests.test_stage_runner_artifacts_feed_real_reader_and_halt_before_candidates` | `experiments/track_c/c10y_directdw_selftest.py:710` |
| `IntegrationTests.test_stored_control_scale1_identity` | `experiments/track_c/c10y_directdw_selftest.py:682` |
| `IntegrationTests.test_strict_json_and_immutable_records` | `experiments/track_c/c10y_directdw_selftest.py:688` |
| `IntegrationTests.test_three_forced_zero_lr_iterations_and_telemetry_trajectory` | `experiments/track_c/c10y_directdw_selftest.py:659` |
| `IsolationTests.test_all_cases_use_base` | `experiments/track_c/c10y_directdw_selftest.py:325` |
| `IsolationTests.test_live_write_positive_control` | `experiments/track_c/c10y_directdw_selftest.py:314` |
| `IsolationTests.test_real_dispatch_denied_with_temp_environment` | `experiments/track_c/c10y_directdw_selftest.py:328` |
| `IsolationTests.test_relative_and_symlink_guard` | `experiments/track_c/c10y_directdw_selftest.py:320` |
| `IsolationTests.test_selftest_root_refusal` | `experiments/track_c/c10y_directdw_selftest.py:333` |
| `LaunchDeltaTests.test_later_stage_cannot_consume_stage1_calibration_measurements` | `experiments/track_c/c10y_directdw_selftest.py:4042` |
| `LaunchDeltaTests.test_nm_decimal_boundary_through_real_reader` | `experiments/track_c/c10y_directdw_selftest.py:4008` |
| `LaunchDeltaTests.test_nm_decimal_boundary_through_scientific_hook` | `experiments/track_c/c10y_directdw_selftest.py:4020` |
| `LaunchDeltaTests.test_norm_readouts_are_inside_writer_wall_clock` | `experiments/track_c/c10y_directdw_selftest.py:4074` |
| `LaunchDeltaTests.test_real_iteration_producer_passes_c2_timing_validator` | `experiments/track_c/c10y_directdw_selftest.py:4084` |
| `LaunchDeltaTests.test_stored_scale_sum_matches_reader_float64_sum` | `experiments/track_c/c10y_directdw_selftest.py:4001` |
| `LaunchDeltaTests.test_supervisor_timeout_records_observed_template_hash_without_child` | `experiments/track_c/c10y_directdw_selftest.py:4057` |
| `LaunchDeltaTests.test_t8_overlap_audit_precedes_first_forward_and_never_redraws` | `experiments/track_c/c10y_directdw_selftest.py:4049` |
| `LaunchTests.test_context_freeze_and_leakage` | `experiments/track_c/c10y_directdw_selftest.py:521` |
| `LaunchTests.test_direct_launch_shell_dependencies_are_executable_and_git_100755` | `experiments/track_c/c10y_directdw_selftest.py:463` |
| `LaunchTests.test_every_inherited_preflight_knob_refused` | `experiments/track_c/c10y_directdw_selftest.py:486` |
| `LaunchTests.test_forecast_unverified_and_cap` | `experiments/track_c/c10y_directdw_selftest.py:2782` |
| `LaunchTests.test_go_spend_and_stage_eligibility` | `experiments/track_c/c10y_directdw_selftest.py:494` |
| `LaunchTests.test_memory_boundaries` | `experiments/track_c/c10y_directdw_selftest.py:513` |
| `LaunchTests.test_schedule_halt_survives_new_directory` | `experiments/track_c/c10y_directdw_selftest.py:542` |
| `LaunchTests.test_step_projection_reserves_readout` | `experiments/track_c/c10y_directdw_selftest.py:546` |
| `LaunchTests.test_wrapper_delegate_dynamic_and_arm_restore` | `experiments/track_c/c10y_directdw_selftest.py:530` |
| `NumericTests.test_anchor_zero_denominator` | `experiments/track_c/c10y_directdw_selftest.py:367` |
| `NumericTests.test_capture_factorization` | `experiments/track_c/c10y_directdw_selftest.py:359` |
| `NumericTests.test_control_boundaries` | `experiments/track_c/c10y_directdw_selftest.py:379` |
| `NumericTests.test_full_size_float64_reductions` | `experiments/track_c/c10y_directdw_selftest.py:338` |
| `NumericTests.test_gram_norm_dense_reference` | `experiments/track_c/c10y_directdw_selftest.py:351` |
| `NumericTests.test_mps_double_refused` | `experiments/track_c/c10y_directdw_selftest.py:356` |
| `NumericTests.test_null_share_boundaries` | `experiments/track_c/c10y_directdw_selftest.py:385` |
| `NumericTests.test_size_scales_and_stored_arithmetic` | `experiments/track_c/c10y_directdw_selftest.py:371` |
| `OptimizerTests.test_effective_weight_and_routing_gradient` | `experiments/track_c/c10y_directdw_selftest.py:394` |
| `OptimizerTests.test_kl_coefficient_once` | `experiments/track_c/c10y_directdw_selftest.py:406` |
| `OptimizerTests.test_loss_scale_transaction` | `experiments/track_c/c10y_directdw_selftest.py:430` |
| `OptimizerTests.test_microbatch_request_weighting` | `experiments/track_c/c10y_directdw_selftest.py:419` |
| `OptimizerTests.test_request_batch_and_target_only_objective` | `experiments/track_c/c10y_directdw_selftest.py:408` |
| `OptimizerTests.test_sixth_overflow_halts_without_mutation` | `experiments/track_c/c10y_directdw_selftest.py:444` |
| `OptimizerTests.test_stopping_boundaries` | `experiments/track_c/c10y_directdw_selftest.py:425` |
| `OptimizerTests.test_unknown_hooks_preserved` | `experiments/track_c/c10y_directdw_selftest.py:450` |
| `PinnedTemplateTests.test_changed_template_source_or_stage1_content_halts` | `experiments/track_c/c10y_directdw_selftest.py:3119` |
| `PinnedTemplateTests.test_stage1_and_calibration_pin_before_first_engine_call` | `experiments/track_c/c10y_directdw_selftest.py:3088` |
| `PinnedTemplateTests.test_stages2_3_install_stage1_bytes_before_first_engine_use` | `experiments/track_c/c10y_directdw_selftest.py:3112` |
| `PinnedTemplateTests.test_t8_digest_failure_has_halt_diagnostic_before_scoring` | `experiments/track_c/c10y_directdw_selftest.py:3140` |
| `PinnedTemplateTests.test_t8_installs_pin_and_writes_context_before_any_pass` | `experiments/track_c/c10y_directdw_selftest.py:3133` |
| `ReaderAttributionTests.test_anchor_comparison_does_not_require_bz_sized_gain` | `experiments/track_c/c10y_directdw_selftest.py:1826` |
| `ReaderAttributionTests.test_anchor_missing_invalid_and_unfit_untested` | `experiments/track_c/c10y_directdw_selftest.py:1815` |
| `ReaderAttributionTests.test_anchor_sham_descriptor_windows_not_fit_or_validity` | `experiments/track_c/c10y_directdw_selftest.py:1832` |
| `ReaderAttributionTests.test_control_positive_requires_envelope_gain_fit_locality_and_validity` | `experiments/track_c/c10y_directdw_selftest.py:1791` |
| `ReaderAttributionTests.test_hy1_credit_requires_both_processes_attributed` | `experiments/track_c/c10y_directdw_selftest.py:1844` |
| `ReaderAttributionTests.test_neff_minimum_and_anchor_gap_nine_ten` | `experiments/track_c/c10y_directdw_selftest.py:1808` |
| `ReaderAttributionTests.test_no_downscale_controls_required_at_actual_ratio_one` | `experiments/track_c/c10y_directdw_selftest.py:1747` |
| `ReaderAttributionTests.test_size_control_matching_and_direction_boundaries` | `experiments/track_c/c10y_directdw_selftest.py:1771` |
| `ReaderAttributionTests.test_total_and_per_layer_growth_trigger_independent_controls` | `experiments/track_c/c10y_directdw_selftest.py:1761` |
| `ReaderAttributionTests.test_zero_reference_size_normalisation_conservative_provisional` | `experiments/track_c/c10y_directdw_selftest.py:1753` |
| `ReaderCrossProcessTests.test_cross_shared_hin_and_telemetry_pair_identity` | `experiments/track_c/c10y_directdw_selftest.py:1945` |
| `ReaderCrossProcessTests.test_r1_cosine_and_distance_every_layer_boundaries` | `experiments/track_c/c10y_directdw_selftest.py:1890` |
| `ReaderCrossProcessTests.test_r1_required_controls_and_all_arms_independent` | `experiments/track_c/c10y_directdw_selftest.py:1915` |
| `ReaderCrossProcessTests.test_r1_zero_norm_rules_and_baseline_instrument` | `experiments/track_c/c10y_directdw_selftest.py:1899` |
| `ReaderCrossProcessTests.test_r2_count_spread_five_six` | `experiments/track_c/c10y_directdw_selftest.py:1922` |
| `ReaderCrossProcessTests.test_r3_incorrect_strings_do_not_count_as_disagreement` | `experiments/track_c/c10y_directdw_selftest.py:1939` |
| `ReaderCrossProcessTests.test_r3_keyed_boolean_disagreement_da_plus_three_four` | `experiments/track_c/c10y_directdw_selftest.py:1930` |
| `ReaderCrossProcessTests.test_regenerated_target_hashes_need_not_match_shared_hin` | `experiments/track_c/c10y_directdw_selftest.py:1955` |
| `ReaderCrossProcessTests.test_x1_not_run_halted_and_incomplete_never_fabricated_null` | `experiments/track_c/c10y_directdw_selftest.py:1858` |
| `ReaderCrossProcessTests.test_x2_identical_labels_and_union_qualifiers` | `experiments/track_c/c10y_directdw_selftest.py:1868` |
| `ReaderCrossProcessTests.test_x3_mixed_labels_store_actual_counts` | `experiments/track_c/c10y_directdw_selftest.py:1874` |
| `ReaderFitAndScreenTests.test_fit_e2e_minimum_canonical_and_every_stop` | `experiments/track_c/c10y_directdw_selftest.py:1558` |
| `ReaderFitAndScreenTests.test_fit_per_required_arm_and_apply_stored` | `experiments/track_c/c10y_directdw_selftest.py:1568` |
| `ReaderFitAndScreenTests.test_fit_requires_full_merged_matrix` | `experiments/track_c/c10y_directdw_selftest.py:1578` |
| `ReaderFitAndScreenTests.test_fit_z_mean_and_maximum_boundaries` | `experiments/track_c/c10y_directdw_selftest.py:1591` |
| `ReaderFitAndScreenTests.test_fit_z_zero_denominator_named_rule` | `experiments/track_c/c10y_directdw_selftest.py:1600` |
| `ReaderFitAndScreenTests.test_s1_named_halts_without_screen_label` | `experiments/track_c/c10y_directdw_selftest.py:1610` |
| `ReaderFitAndScreenTests.test_s2_s3_budget_write_boundary` | `experiments/track_c/c10y_directdw_selftest.py:1616` |
| `ReaderFitAndScreenTests.test_s4_fit_precedes_high_count_locality_and_size` | `experiments/track_c/c10y_directdw_selftest.py:1631` |
| `ReaderFitAndScreenTests.test_s5_s7_envelope_and_gain_boundaries` | `experiments/track_c/c10y_directdw_selftest.py:1640` |
| `ReaderFitAndScreenTests.test_s6_size_boundary_and_null_first_match` | `experiments/track_c/c10y_directdw_selftest.py:1647` |
| `ReaderFitAndScreenTests.test_stage1_recorded_projection_exactly_120_minutes_fits` | `experiments/track_c/c10y_directdw_selftest.py:1623` |
| `ReaderLoadTests.test_load_calibration_directory_refused_before_read` | `experiments/track_c/c10y_directdw_selftest.py:2096` |
| `ReaderLoadTests.test_load_does_not_read_telemetry` | `experiments/track_c/c10y_directdw_selftest.py:2070` |
| `ReaderLoadTests.test_load_later_self_contained_record_uses_own_outcome` | `experiments/track_c/c10y_directdw_selftest.py:2080` |
| `ReaderLoadTests.test_load_saved_halt_first_with_missing_science_artifacts` | `experiments/track_c/c10y_directdw_selftest.py:2061` |
| `ReaderLoadTests.test_load_strict_json_nonfinite_refused` | `experiments/track_c/c10y_directdw_selftest.py:2089` |
| `ReaderOrderTests.test_existing_arm_missing_metric_is_v13_invalid` | `experiments/track_c/c10y_directdw_selftest.py:1262` |
| `ReaderOrderTests.test_missing_comparators_qualify_without_incomplete` | `experiments/track_c/c10y_directdw_selftest.py:1253` |
| `ReaderOrderTests.test_own_record_and_v5_missing_precede_validity_and_fit` | `experiments/track_c/c10y_directdw_selftest.py:1222` |
| `ReaderOrderTests.test_recorded_halt_invalid_and_budget_first` | `experiments/track_c/c10y_directdw_selftest.py:1213` |
| `ReaderOrderTests.test_source_and_prereg_identity_refused` | `experiments/track_c/c10y_directdw_selftest.py:1267` |
| `ReaderOrderTests.test_stage1_not_run_controls_and_later_records_not_required` | `experiments/track_c/c10y_directdw_selftest.py:1246` |
| `ReaderOrderTests.test_validity_precedes_fit_and_fit_precedes_counts` | `experiments/track_c/c10y_directdw_selftest.py:1234` |
| `ReaderProcessLocalityTests.test_g1_g2_each_frame_both_sides` | `experiments/track_c/c10y_directdw_selftest.py:1678` |
| `ReaderProcessLocalityTests.test_g3_g4_g5_unrounded_boundaries` | `experiments/track_c/c10y_directdw_selftest.py:1693` |
| `ReaderProcessLocalityTests.test_g3_g5_display_rounding_cannot_substitute` | `experiments/track_c/c10y_directdw_selftest.py:1702` |
| `ReaderProcessLocalityTests.test_g6_relation_flips_report_only` | `experiments/track_c/c10y_directdw_selftest.py:1712` |
| `ReaderProcessLocalityTests.test_p1_p2_p3` | `experiments/track_c/c10y_directdw_selftest.py:1660` |
| `ReaderProcessLocalityTests.test_p4_p5_p7_count_and_gain_boundaries` | `experiments/track_c/c10y_directdw_selftest.py:1671` |
| `ReaderProcessLocalityTests.test_p6_tradeoff_and_p7_null_first_match` | `experiments/track_c/c10y_directdw_selftest.py:1717` |
| `ReaderProcessLocalityTests.test_w1_actual_size_boundary_qualifier_preserves_base` | `experiments/track_c/c10y_directdw_selftest.py:1724` |
| `ReaderProcessLocalityTests.test_w2_ttl_warning_equality_nonblocking` | `experiments/track_c/c10y_directdw_selftest.py:1734` |
| `ReaderTruthTableTests.test_authored_full_truth_rows_277_289` | `experiments/track_c/c10y_directdw_selftest.py:2001` |
| `ReaderTruthTableTests.test_authored_stage1_truth_rows_265_276` | `experiments/track_c/c10y_directdw_selftest.py:1966` |
| `ReaderValidityTests.test_v10_overflow_retries_five_six` | `experiments/track_c/c10y_directdw_selftest.py:1484` |
| `ReaderValidityTests.test_v11_hin_hashes_and_write_trace_required` | `experiments/track_c/c10y_directdw_selftest.py:1490` |
| `ReaderValidityTests.test_v12_leakage_named_halt` | `experiments/track_c/c10y_directdw_selftest.py:1506` |
| `ReaderValidityTests.test_v13_every_applicable_numeric_family_nonfinite` | `experiments/track_c/c10y_directdw_selftest.py:1532` |
| `ReaderValidityTests.test_v13_nonfinite_unjustified_null_and_typed_integer` | `experiments/track_c/c10y_directdw_selftest.py:1526` |
| `ReaderValidityTests.test_v13_typed_nulls_and_reasons` | `experiments/track_c/c10y_directdw_selftest.py:1511` |
| `ReaderValidityTests.test_v1_fingerprint_sha_sites_and_full_output` | `experiments/track_c/c10y_directdw_selftest.py:1282` |
| `ReaderValidityTests.test_v2_each_recipe_standing_law5` | `experiments/track_c/c10y_directdw_selftest.py:1289` |
| `ReaderValidityTests.test_v3_accumulation_raw_cosine_distance_finiteness_and_scope` | `experiments/track_c/c10y_directdw_selftest.py:1349` |
| `ReaderValidityTests.test_v3_apply_stored_substitutions_not_optimiser_checks` | `experiments/track_c/c10y_directdw_selftest.py:1314` |
| `ReaderValidityTests.test_v3_capture_zero_step_and_executed_loop_raw_values` | `experiments/track_c/c10y_directdw_selftest.py:1323` |
| `ReaderValidityTests.test_v3_check_failure_order_and_scope` | `experiments/track_c/c10y_directdw_selftest.py:1295` |
| `ReaderValidityTests.test_v3_gradient_halvings_hooks_and_smoke_raw_values` | `experiments/track_c/c10y_directdw_selftest.py:1365` |
| `ReaderValidityTests.test_v3_missing_required_check_invalid` | `experiments/track_c/c10y_directdw_selftest.py:1304` |
| `ReaderValidityTests.test_v3_objective_nll_and_nonzero_kl_raw_boundaries` | `experiments/track_c/c10y_directdw_selftest.py:1337` |
| `ReaderValidityTests.test_v4_a1_a2_and_exact_denominators` | `experiments/track_c/c10y_directdw_selftest.py:1394` |
| `ReaderValidityTests.test_v4_all_inclusive_baseline_endpoints` | `experiments/track_c/c10y_directdw_selftest.py:1384` |
| `ReaderValidityTests.test_v4_before_candidates_required` | `experiments/track_c/c10y_directdw_selftest.py:1405` |
| `ReaderValidityTests.test_v5_candidate_controls_67_68_each_arm` | `experiments/track_c/c10y_directdw_selftest.py:1410` |
| `ReaderValidityTests.test_v6_overrides_are_exact_sets_not_counts` | `experiments/track_c/c10y_directdw_selftest.py:1418` |
| `ReaderValidityTests.test_v7_initial_projector_raw_share_cannot_hide_behind_passed` | `experiments/track_c/c10y_directdw_selftest.py:1454` |
| `ReaderValidityTests.test_v7_planned_actual_each_layer_boundary_and_zero` | `experiments/track_c/c10y_directdw_selftest.py:1437` |
| `ReaderValidityTests.test_v7_untouched_reference_miss_halts_precision_diagnosis` | `experiments/track_c/c10y_directdw_selftest.py:1449` |
| `ReaderValidityTests.test_v8_string_full_equality_and_one_below_every_arm` | `experiments/track_c/c10y_directdw_selftest.py:1462` |
| `ReaderValidityTests.test_v9_init_final_tokens_and_each_loss_component` | `experiments/track_c/c10y_directdw_selftest.py:1471` |
| `TelemetryCheckContract.test_T11_audit_accepts_every_kind_with_only_kind_specific_fields` | `experiments/track_c/c10y_directdw_selftest.py:2430` |
| `TelemetryCheckContract.test_T11_audit_checks_payload_types_for_every_non_answer_kind` | `experiments/track_c/c10y_directdw_selftest.py:2502` |
| `TelemetryCheckContract.test_T11_audit_complete_answer_keys_pass_and_roundtrip` | `experiments/track_c/c10y_directdw_selftest.py:2404` |
| `TelemetryCheckContract.test_T11_audit_declared_disabled_missing_output_keeps_science_record` | `experiments/track_c/c10y_directdw_selftest.py:2577` |
| `TelemetryCheckContract.test_T11_audit_disabled_marker_does_not_excuse_a_gap_before_later_answers` | `experiments/track_c/c10y_directdw_selftest.py:2598` |
| `TelemetryCheckContract.test_T11_audit_disabled_marker_does_not_excuse_mismatching_existing_line` | `experiments/track_c/c10y_directdw_selftest.py:2588` |
| `TelemetryCheckContract.test_T11_audit_duplicate_answer_key_compromises_stage` | `experiments/track_c/c10y_directdw_selftest.py:2460` |
| `TelemetryCheckContract.test_T11_audit_header_must_be_present_initial_and_unique` | `experiments/track_c/c10y_directdw_selftest.py:2559` |
| `TelemetryCheckContract.test_T11_audit_mismatch_compromises_stage_and_requires_telemetry_off_rerun` | `experiments/track_c/c10y_directdw_selftest.py:2452` |
| `TelemetryCheckContract.test_T11_audit_missing_answer_field_is_malformed` | `experiments/track_c/c10y_directdw_selftest.py:2494` |
| `TelemetryCheckContract.test_T11_audit_missing_expected_key_compromises_stage` | `experiments/track_c/c10y_directdw_selftest.py:2466` |
| `TelemetryCheckContract.test_T11_audit_missing_file_is_missing_output` | `experiments/track_c/c10y_directdw_selftest.py:2472` |
| `TelemetryCheckContract.test_T11_audit_model_free_entrypoint_never_loads_driver_or_harness` | `experiments/track_c/c10y_directdw_selftest.py:2607` |
| `TelemetryCheckContract.test_T11_audit_never_mutates_science_records_or_reader_output` | `experiments/track_c/c10y_directdw_selftest.py:2419` |
| `TelemetryCheckContract.test_T11_audit_refuses_existing_audit_without_rewriting_evidence` | `experiments/track_c/c10y_directdw_selftest.py:2618` |
| `TelemetryCheckContract.test_T11_audit_rejects_unknown_field_on_every_known_kind` | `experiments/track_c/c10y_directdw_selftest.py:2520` |
| `TelemetryCheckContract.test_T11_audit_strict_json_rejects_nonfinite_and_duplicate_json_fields` | `experiments/track_c/c10y_directdw_selftest.py:2549` |
| `TelemetryCheckContract.test_T11_audit_unknown_key_or_kind_or_field_is_unexpected` | `experiments/track_c/c10y_directdw_selftest.py:2477` |
| `TelemetryCheckContract.test_T11_audit_uses_stage_two_and_three_tags_and_record_paths` | `experiments/track_c/c10y_directdw_selftest.py:2412` |
| `TelemetryCheckContract.test_T11_audit_wrong_types_and_nulls_are_malformed` | `experiments/track_c/c10y_directdw_selftest.py:2538` |
| `TelemetryCheckContract.test_T11_reader_does_not_open_telemetry_or_use_audit_as_gate` | `experiments/track_c/c10y_directdw_selftest.py:2627` |
| `TelemetryCheckContract.test_T8_runner_inert_pristine_stub_never_calls_writer_or_recipe` | `experiments/track_c/c10y_directdw_selftest.py:2338` |
| `TelemetryCheckContract.test_T8_runner_other_verdicts_exit_zero_and_preserve_verdict` | `experiments/track_c/c10y_directdw_selftest.py:2390` |
| `TelemetryCheckContract.test_T8_runner_preflight_refuses_knob_before_output_creation` | `experiments/track_c/c10y_directdw_selftest.py:2331` |
| `TelemetryCheckContract.test_T8_runner_preserves_existing_record` | `experiments/track_c/c10y_directdw_selftest.py:2322` |
| `TelemetryCheckContract.test_T8_runner_records_complete_current_identity_and_strict_roundtrip` | `experiments/track_c/c10y_directdw_selftest.py:2352` |
| `TelemetryCheckContract.test_T8_runner_rejects_namespace_itself_and_nested_subdirectories` | `experiments/track_c/c10y_directdw_selftest.py:2303` |
| `TelemetryCheckContract.test_T8_runner_rejects_output_outside_namespace` | `experiments/track_c/c10y_directdw_selftest.py:2296` |
| `TelemetryCheckContract.test_T8_runner_rejects_relative_output_before_writes` | `experiments/track_c/c10y_directdw_selftest.py:2290` |
| `TelemetryCheckContract.test_T8_runner_rejects_symlink_escape` | `experiments/track_c/c10y_directdw_selftest.py:2311` |
| `TelemetryCheckContract.test_T8_runner_weight_change_is_invalid_exit_two` | `experiments/track_c/c10y_directdw_selftest.py:2375` |
| `TelemetryForecastTests.test_full_stage_counts_and_payload_not_smaller` | `experiments/track_c/c10y_directdw_selftest.py:3195` |
| `TelemetryForecastTests.test_inertness_bytes_once_and_duplicate_nonfinite_refused` | `experiments/track_c/c10y_directdw_selftest.py:3207` |
| `TelemetryForecastTests.test_on_requires_separate_phase_before_dispatch` | `experiments/track_c/c10y_directdw_selftest.py:3174` |
| `TelemetryForecastTests.test_per_kind_measurements_workload_and_sum_enforced` | `experiments/track_c/c10y_directdw_selftest.py:3181` |
| `TelemetryTests.test_every_kind_state_preservation_and_volume` | `experiments/track_c/c10y_directdw_selftest.py:599` |
| `TelemetryTests.test_frozen_hparams_lens_uses_actual_linear_head` | `experiments/track_c/c10y_directdw_selftest.py:554` |
| `TelemetryTests.test_inertness_and_drifting_baseline` | `experiments/track_c/c10y_directdw_selftest.py:637` |
| `TelemetryTests.test_invalid_switches_refused_before_write` | `experiments/track_c/c10y_directdw_selftest.py:585` |
| `TelemetryTests.test_io_failures_disable_once_and_baseexception_propagates` | `experiments/track_c/c10y_directdw_selftest.py:624` |
| `TelemetryTests.test_off_has_no_object_or_directory` | `experiments/track_c/c10y_directdw_selftest.py:580` |
| `TelemetryTests.test_scorer_ast_and_exact_inputs` | `experiments/track_c/c10y_directdw_selftest.py:589` |
| `TelemetryTests.test_t8_serialized_wrong_answer_is_not_inert` | `experiments/track_c/c10y_directdw_selftest.py:572` |
| `TelemetryTests.test_telemetry_never_calls_operational_clock_or_writes_input_record` | `experiments/track_c/c10y_directdw_selftest.py:560` |
| `TransportTests.test_actual_cpu_update_direction_changes_fail_real_reader_repro_gate` | `experiments/track_c/c10y_directdw_selftest.py:3752` |
| `TransportTests.test_completed_stage1_runner_to_reader_and_cpu_pt_transport` | `experiments/track_c/c10y_directdw_selftest.py:3688` |
| `TransportTests.test_completed_three_stages_preserve_common_files_and_compute_real_repro` | `experiments/track_c/c10y_directdw_selftest.py:3709` |
| `TransportTests.test_real_scored_recipe_accounts_for_scientific_hook_readout_time` | `experiments/track_c/c10y_directdw_selftest.py:3935` |
| `TransportTests.test_requested_stage_forecast_is_checked_before_dispatch_and_worker` | `experiments/track_c/c10y_directdw_selftest.py:3894` |
| `TransportTests.test_saved_overlay_hash_is_the_immutable_serialized_bundle` | `experiments/track_c/c10y_directdw_selftest.py:3920` |
| `TransportTests.test_stage3_pair_mismatch_is_refused_in_parent_before_any_launch_write` | `experiments/track_c/c10y_directdw_selftest.py:3909` |
| `TransportTests.test_stage3_telemetry_setting_cannot_change_after_stage2` | `experiments/track_c/c10y_directdw_selftest.py:3879` |
| `TransportTests.test_tampered_stage2_pt_refuses_stage3_before_scientific_callbacks` | `experiments/track_c/c10y_directdw_selftest.py:3769` |
| `TransportTests.test_telemetry_off_on_transport_changes_only_T1_fields_at_every_stage` | `experiments/track_c/c10y_directdw_selftest.py:3817` |
| `TransportTests.test_wrong_stage3_predecessor_refuses_in_main_before_harness_or_supervisor` | `experiments/track_c/c10y_directdw_selftest.py:3786` |

## Failing-first and final verification evidence

Commands used the absolute venv interpreter with `-B`, `TMPDIR=/private/tmp/c10y_build`, `PYTHONDONTWRITEBYTECODE=1`, `OMP_NUM_THREADS=1`, `VECLIB_MAXIMUM_THREADS=1`, serially. RTK proxy wrapped shell invocations. The neutral-stub step used real signatures and data-shaped neutral outputs, then implementation started only after its 400 behavioral assertion failures with no test errors. The first earlier neutral-stub run had two fixture errors; those were corrected before the accepted 400-assertion RED, not counted as behavioral failures or GREEN evidence.

```sh
/opt/homebrew/bin/rtk proxy env TMPDIR=/private/tmp/c10y_build PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python -B /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py > /private/tmp/c10y_build/red_missing.log 2>&1
```

Evidence: `/private/tmp/c10y_build/red_missing.log`; SHA-256 `cffa117b5930de8d4d55f8d76374bdb4d64cb68bdfa3246b1f9faf086b15ae4a`.

```text
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 78, in <module>
    import c10y_directdw_arms as A
ModuleNotFoundError: No module named 'c10y_directdw_arms'
```

Real-signature neutral-stub command: same absolute selftest invocation, stdout/stderr saved as `red_stubs_assertions.log`; exit 1. The complete output below includes every behavioral failure’s own assertion, rather than counting import/TypeError/KeyError/AttributeError failures as RED. 163 tests, 400 failures, no errors, empty forbidden-module and owned-listing drift checks.

Evidence: `/private/tmp/c10y_build/red_stubs_assertions.log`; SHA-256 `78fc84fe54e7e6ab746a88c9d576c613078828b275ff3d3a57211bfda5ab53aa`.

```text
test_calibration_forecast_rejects_partial_and_stale (__main__.CalibrationTests.test_calibration_forecast_rejects_partial_and_stale) ... FAIL
test_calibration_forecast_uses_all_repetitions_no_memory_or_inputs (__main__.CalibrationTests.test_calibration_forecast_uses_all_repetitions_no_memory_or_inputs) ... FAIL
test_calibration_go_spend_caps (__main__.CalibrationTests.test_calibration_go_spend_caps) ... FAIL
test_calibration_prefix_only_and_required_records (__main__.CalibrationTests.test_calibration_prefix_only_and_required_records) ... FAIL
test_calibration_reader_and_context_source_refused (__main__.CalibrationTests.test_calibration_reader_and_context_source_refused) ... FAIL
test_calibration_telemetry_variables_and_existing_directory_refused (__main__.CalibrationTests.test_calibration_telemetry_variables_and_existing_directory_refused) ... FAIL
test_calibration_v4_halt_persists_schedule (__main__.CalibrationTests.test_calibration_v4_halt_persists_schedule) ... FAIL
test_calibration_wrong_namespace_refused (__main__.CalibrationTests.test_calibration_wrong_namespace_refused) ... 
  test_calibration_wrong_namespace_refused (__main__.CalibrationTests.test_calibration_wrong_namespace_refused) (out=PosixPath('/private/tmp/c10y_build/roots/tmpi1vgfog9/results/c10y_directdw')) ... FAIL
  test_calibration_wrong_namespace_refused (__main__.CalibrationTests.test_calibration_wrong_namespace_refused) (out=PosixPath('/private/tmp/c10y_build/roots/tmpi1vgfog9/results/c10y_directdw_s1_rerun1')) ... FAIL
  test_calibration_wrong_namespace_refused (__main__.CalibrationTests.test_calibration_wrong_namespace_refused) (out=PosixPath('/private/tmp/c10y_build/roots/tmpi1vgfog9/results/c10y_directdw_calib0')) ... FAIL
test_frozen_bytes_suite_end (__main__.CalibrationTests.test_frozen_bytes_suite_end) ... ok
test_actual_launcher_refuses_missing_calibration_before_import (__main__.IntegrationTests.test_actual_launcher_refuses_missing_calibration_before_import) ... FAIL
test_candidate_operations_require_baseline (__main__.IntegrationTests.test_candidate_operations_require_baseline) ... FAIL
test_native_hanging_worker_deadline_before_and_after_write (__main__.IntegrationTests.test_native_hanging_worker_deadline_before_and_after_write) ... FAIL
test_sequential_capture_matches_original (__main__.IntegrationTests.test_sequential_capture_matches_original) ... FAIL
test_stage_runner_artifacts_feed_real_reader_and_halt_before_candidates (__main__.IntegrationTests.test_stage_runner_artifacts_feed_real_reader_and_halt_before_candidates) ... FAIL
test_stored_control_scale1_identity (__main__.IntegrationTests.test_stored_control_scale1_identity) ... FAIL
test_strict_json_and_immutable_records (__main__.IntegrationTests.test_strict_json_and_immutable_records) ... FAIL
test_three_forced_zero_lr_iterations_and_telemetry_trajectory (__main__.IntegrationTests.test_three_forced_zero_lr_iterations_and_telemetry_trajectory) ... FAIL
test_all_cases_use_base (__main__.IsolationTests.test_all_cases_use_base) ... ok
test_live_write_positive_control (__main__.IsolationTests.test_live_write_positive_control) ... ok
test_real_dispatch_denied_with_temp_environment (__main__.IsolationTests.test_real_dispatch_denied_with_temp_environment) ... ok
test_relative_and_symlink_guard (__main__.IsolationTests.test_relative_and_symlink_guard) ... ok
test_selftest_root_refusal (__main__.IsolationTests.test_selftest_root_refusal) ... FAIL
test_context_freeze_and_leakage (__main__.LaunchTests.test_context_freeze_and_leakage) ... FAIL
test_every_inherited_preflight_knob_refused (__main__.LaunchTests.test_every_inherited_preflight_knob_refused) ... 
  test_every_inherited_preflight_knob_refused (__main__.LaunchTests.test_every_inherited_preflight_knob_refused) (knob='C10_PROJECTOR') ... FAIL
  test_every_inherited_preflight_knob_refused (__main__.LaunchTests.test_every_inherited_preflight_knob_refused) (knob='N_EDIT') ... FAIL
  test_every_inherited_preflight_knob_refused (__main__.LaunchTests.test_every_inherited_preflight_knob_refused) (knob='C10_SUBJECT_OFFSET') ... FAIL
  test_every_inherited_preflight_knob_refused (__main__.LaunchTests.test_every_inherited_preflight_knob_refused) (knob='C10_CTX_TEMPLATES') ... FAIL
  test_every_inherited_preflight_knob_refused (__main__.LaunchTests.test_every_inherited_preflight_knob_refused) (knob='C10_ARMS') ... FAIL
  test_every_inherited_preflight_knob_refused (__main__.LaunchTests.test_every_inherited_preflight_knob_refused) (knob='C10_KEY_LOCUS') ... FAIL
  test_every_inherited_preflight_knob_refused (__main__.LaunchTests.test_every_inherited_preflight_knob_refused) (knob='HP_CANDIDATE') ... FAIL
  test_every_inherited_preflight_knob_refused (__main__.LaunchTests.test_every_inherited_preflight_knob_refused) (knob='C10_RECIPES') ... FAIL
  test_every_inherited_preflight_knob_refused (__main__.LaunchTests.test_every_inherited_preflight_knob_refused) (knob='CANDIDATE_NAME') ... FAIL
  test_every_inherited_preflight_knob_refused (__main__.LaunchTests.test_every_inherited_preflight_knob_refused) (knob='OUT') ... FAIL
  test_every_inherited_preflight_knob_refused (__main__.LaunchTests.test_every_inherited_preflight_knob_refused) (knob='DECISION_ID') ... FAIL
  test_every_inherited_preflight_knob_refused (__main__.LaunchTests.test_every_inherited_preflight_knob_refused) (knob='PREREG') ... FAIL
  test_every_inherited_preflight_knob_refused (__main__.LaunchTests.test_every_inherited_preflight_knob_refused) (knob='RUN_LABEL') ... FAIL
  test_every_inherited_preflight_knob_refused (__main__.LaunchTests.test_every_inherited_preflight_knob_refused) (knob='LLMDB_DEVICE') ... FAIL
  test_every_inherited_preflight_knob_refused (__main__.LaunchTests.test_every_inherited_preflight_knob_refused) (name='MODEL_ID') ... FAIL
  test_every_inherited_preflight_knob_refused (__main__.LaunchTests.test_every_inherited_preflight_knob_refused) (name='MODEL_REV') ... FAIL
test_forecast_unverified_and_cap (__main__.LaunchTests.test_forecast_unverified_and_cap) ... FAIL
test_go_spend_and_stage_eligibility (__main__.LaunchTests.test_go_spend_and_stage_eligibility) ... FAIL
test_memory_boundaries (__main__.LaunchTests.test_memory_boundaries) ... FAIL
test_schedule_halt_survives_new_directory (__main__.LaunchTests.test_schedule_halt_survives_new_directory) ... FAIL
test_step_projection_reserves_readout (__main__.LaunchTests.test_step_projection_reserves_readout) ... FAIL
test_wrapper_delegate_dynamic_and_arm_restore (__main__.LaunchTests.test_wrapper_delegate_dynamic_and_arm_restore) ... FAIL
test_anchor_zero_denominator (__main__.NumericTests.test_anchor_zero_denominator) ... FAIL
test_capture_factorization (__main__.NumericTests.test_capture_factorization) ... FAIL
test_control_boundaries (__main__.NumericTests.test_control_boundaries) ... 
  test_control_boundaries (__main__.NumericTests.test_control_boundaries) (error=0.01) ... FAIL
  test_control_boundaries (__main__.NumericTests.test_control_boundaries) (candidate=1.01) ... FAIL
test_full_size_float64_reductions (__main__.NumericTests.test_full_size_float64_reductions) ... FAIL
test_gram_norm_dense_reference (__main__.NumericTests.test_gram_norm_dense_reference) ... FAIL
test_mps_double_refused (__main__.NumericTests.test_mps_double_refused) ... FAIL
test_null_share_boundaries (__main__.NumericTests.test_null_share_boundaries) ... FAIL
test_size_scales_and_stored_arithmetic (__main__.NumericTests.test_size_scales_and_stored_arithmetic) ... FAIL
test_effective_weight_and_routing_gradient (__main__.OptimizerTests.test_effective_weight_and_routing_gradient) ... FAIL
test_kl_coefficient_once (__main__.OptimizerTests.test_kl_coefficient_once) ... FAIL
test_loss_scale_transaction (__main__.OptimizerTests.test_loss_scale_transaction) ... FAIL
test_microbatch_request_weighting (__main__.OptimizerTests.test_microbatch_request_weighting) ... FAIL
test_request_batch_and_target_only_objective (__main__.OptimizerTests.test_request_batch_and_target_only_objective) ... FAIL
test_sixth_overflow_halts_without_mutation (__main__.OptimizerTests.test_sixth_overflow_halts_without_mutation) ... FAIL
test_stopping_boundaries (__main__.OptimizerTests.test_stopping_boundaries) ... FAIL
test_unknown_hooks_preserved (__main__.OptimizerTests.test_unknown_hooks_preserved) ... FAIL
test_anchor_comparison_does_not_require_bz_sized_gain (__main__.ReaderAttributionTests.test_anchor_comparison_does_not_require_bz_sized_gain) ... FAIL
test_anchor_missing_invalid_and_unfit_untested (__main__.ReaderAttributionTests.test_anchor_missing_invalid_and_unfit_untested) ... FAIL
test_anchor_sham_descriptor_windows_not_fit_or_validity (__main__.ReaderAttributionTests.test_anchor_sham_descriptor_windows_not_fit_or_validity) ... FAIL
test_control_positive_requires_envelope_gain_fit_locality_and_validity (__main__.ReaderAttributionTests.test_control_positive_requires_envelope_gain_fit_locality_and_validity) ... FAIL
test_hy1_credit_requires_both_processes_attributed (__main__.ReaderAttributionTests.test_hy1_credit_requires_both_processes_attributed) ... FAIL
test_neff_minimum_and_anchor_gap_nine_ten (__main__.ReaderAttributionTests.test_neff_minimum_and_anchor_gap_nine_ten) ... FAIL
test_no_downscale_controls_required_at_actual_ratio_one (__main__.ReaderAttributionTests.test_no_downscale_controls_required_at_actual_ratio_one) ... FAIL
test_size_control_matching_and_direction_boundaries (__main__.ReaderAttributionTests.test_size_control_matching_and_direction_boundaries) ... FAIL
test_total_and_per_layer_growth_trigger_independent_controls (__main__.ReaderAttributionTests.test_total_and_per_layer_growth_trigger_independent_controls) ... FAIL
test_zero_reference_size_normalisation_conservative_provisional (__main__.ReaderAttributionTests.test_zero_reference_size_normalisation_conservative_provisional) ... FAIL
test_cross_shared_hin_and_telemetry_pair_identity (__main__.ReaderCrossProcessTests.test_cross_shared_hin_and_telemetry_pair_identity) ... FAIL
test_r1_cosine_and_distance_every_layer_boundaries (__main__.ReaderCrossProcessTests.test_r1_cosine_and_distance_every_layer_boundaries) ... FAIL
test_r1_required_controls_and_all_arms_independent (__main__.ReaderCrossProcessTests.test_r1_required_controls_and_all_arms_independent) ... FAIL
test_r1_zero_norm_rules_and_baseline_instrument (__main__.ReaderCrossProcessTests.test_r1_zero_norm_rules_and_baseline_instrument) ... FAIL
test_r2_count_spread_five_six (__main__.ReaderCrossProcessTests.test_r2_count_spread_five_six) ... FAIL
test_r3_incorrect_strings_do_not_count_as_disagreement (__main__.ReaderCrossProcessTests.test_r3_incorrect_strings_do_not_count_as_disagreement) ... FAIL
test_r3_keyed_boolean_disagreement_da_plus_three_four (__main__.ReaderCrossProcessTests.test_r3_keyed_boolean_disagreement_da_plus_three_four) ... FAIL
test_regenerated_target_hashes_need_not_match_shared_hin (__main__.ReaderCrossProcessTests.test_regenerated_target_hashes_need_not_match_shared_hin) ... FAIL
test_x1_not_run_halted_and_incomplete_never_fabricated_null (__main__.ReaderCrossProcessTests.test_x1_not_run_halted_and_incomplete_never_fabricated_null) ... FAIL
test_x2_identical_labels_and_union_qualifiers (__main__.ReaderCrossProcessTests.test_x2_identical_labels_and_union_qualifiers) ... FAIL
test_x3_mixed_labels_store_actual_counts (__main__.ReaderCrossProcessTests.test_x3_mixed_labels_store_actual_counts) ... FAIL
test_fit_e2e_minimum_canonical_and_every_stop (__main__.ReaderFitAndScreenTests.test_fit_e2e_minimum_canonical_and_every_stop) ... FAIL
test_fit_per_required_arm_and_apply_stored (__main__.ReaderFitAndScreenTests.test_fit_per_required_arm_and_apply_stored) ... FAIL
test_fit_requires_full_merged_matrix (__main__.ReaderFitAndScreenTests.test_fit_requires_full_merged_matrix) ... FAIL
test_fit_z_mean_and_maximum_boundaries (__main__.ReaderFitAndScreenTests.test_fit_z_mean_and_maximum_boundaries) ... FAIL
test_fit_z_zero_denominator_named_rule (__main__.ReaderFitAndScreenTests.test_fit_z_zero_denominator_named_rule) ... FAIL
test_s1_named_halts_without_screen_label (__main__.ReaderFitAndScreenTests.test_s1_named_halts_without_screen_label) ... FAIL
test_s2_s3_budget_write_boundary (__main__.ReaderFitAndScreenTests.test_s2_s3_budget_write_boundary) ... FAIL
test_s4_fit_precedes_high_count_locality_and_size (__main__.ReaderFitAndScreenTests.test_s4_fit_precedes_high_count_locality_and_size) ... FAIL
test_s5_s7_envelope_and_gain_boundaries (__main__.ReaderFitAndScreenTests.test_s5_s7_envelope_and_gain_boundaries) ... FAIL
test_s6_size_boundary_and_null_first_match (__main__.ReaderFitAndScreenTests.test_s6_size_boundary_and_null_first_match) ... FAIL
test_stage1_recorded_projection_exactly_120_minutes_fits (__main__.ReaderFitAndScreenTests.test_stage1_recorded_projection_exactly_120_minutes_fits) ... FAIL
test_load_calibration_directory_refused_before_read (__main__.ReaderLoadTests.test_load_calibration_directory_refused_before_read) ... FAIL
test_load_does_not_read_telemetry (__main__.ReaderLoadTests.test_load_does_not_read_telemetry) ... FAIL
test_load_later_self_contained_record_uses_own_outcome (__main__.ReaderLoadTests.test_load_later_self_contained_record_uses_own_outcome) ... FAIL
test_load_saved_halt_first_with_missing_science_artifacts (__main__.ReaderLoadTests.test_load_saved_halt_first_with_missing_science_artifacts) ... FAIL
test_load_strict_json_nonfinite_refused (__main__.ReaderLoadTests.test_load_strict_json_nonfinite_refused) ... FAIL
test_existing_arm_missing_metric_is_v13_invalid (__main__.ReaderOrderTests.test_existing_arm_missing_metric_is_v13_invalid) ... FAIL
test_missing_comparators_qualify_without_incomplete (__main__.ReaderOrderTests.test_missing_comparators_qualify_without_incomplete) ... FAIL
test_own_record_and_v5_missing_precede_validity_and_fit (__main__.ReaderOrderTests.test_own_record_and_v5_missing_precede_validity_and_fit) ... 
  test_own_record_and_v5_missing_precede_validity_and_fit (__main__.ReaderOrderTests.test_own_record_and_v5_missing_precede_validity_and_fit) (missing='recipe') ... FAIL
  test_own_record_and_v5_missing_precede_validity_and_fit (__main__.ReaderOrderTests.test_own_record_and_v5_missing_precede_validity_and_fit) (missing='A1_single') ... FAIL
  test_own_record_and_v5_missing_precede_validity_and_fit (__main__.ReaderOrderTests.test_own_record_and_v5_missing_precede_validity_and_fit) (missing='A2_coherent2') ... FAIL
  test_own_record_and_v5_missing_precede_validity_and_fit (__main__.ReaderOrderTests.test_own_record_and_v5_missing_precede_validity_and_fit) (missing='A7_coined_coined') ... FAIL
test_recorded_halt_invalid_and_budget_first (__main__.ReaderOrderTests.test_recorded_halt_invalid_and_budget_first) ... 
  test_recorded_halt_invalid_and_budget_first (__main__.ReaderOrderTests.test_recorded_halt_invalid_and_budget_first) (status='HALTED') ... FAIL
  test_recorded_halt_invalid_and_budget_first (__main__.ReaderOrderTests.test_recorded_halt_invalid_and_budget_first) (status='INVALID') ... FAIL
  test_recorded_halt_invalid_and_budget_first (__main__.ReaderOrderTests.test_recorded_halt_invalid_and_budget_first) (status='HALTED-BUDGET') ... FAIL
  test_recorded_halt_invalid_and_budget_first (__main__.ReaderOrderTests.test_recorded_halt_invalid_and_budget_first) (status='INCOMPLETE-BUDGET') ... FAIL
test_source_and_prereg_identity_refused (__main__.ReaderOrderTests.test_source_and_prereg_identity_refused) ... 
  test_source_and_prereg_identity_refused (__main__.ReaderOrderTests.test_source_and_prereg_identity_refused) (field='prereg') ... FAIL
  test_source_and_prereg_identity_refused (__main__.ReaderOrderTests.test_source_and_prereg_identity_refused) (field='source') ... FAIL
  test_source_and_prereg_identity_refused (__main__.ReaderOrderTests.test_source_and_prereg_identity_refused) (field='input') ... FAIL
test_stage1_not_run_controls_and_later_records_not_required (__main__.ReaderOrderTests.test_stage1_not_run_controls_and_later_records_not_required) ... FAIL
test_validity_precedes_fit_and_fit_precedes_counts (__main__.ReaderOrderTests.test_validity_precedes_fit_and_fit_precedes_counts) ... FAIL
test_g1_g2_each_frame_both_sides (__main__.ReaderProcessLocalityTests.test_g1_g2_each_frame_both_sides) ... 
  test_g1_g2_each_frame_both_sides (__main__.ReaderProcessLocalityTests.test_g1_g2_each_frame_both_sides) (axis='L1', excess=1) ... FAIL
  test_g1_g2_each_frame_both_sides (__main__.ReaderProcessLocalityTests.test_g1_g2_each_frame_both_sides) (axis='L1', excess=2) ... FAIL
  test_g1_g2_each_frame_both_sides (__main__.ReaderProcessLocalityTests.test_g1_g2_each_frame_both_sides) (axis='CANON', excess=1) ... FAIL
  test_g1_g2_each_frame_both_sides (__main__.ReaderProcessLocalityTests.test_g1_g2_each_frame_both_sides) (axis='CANON', excess=2) ... FAIL
  test_g1_g2_each_frame_both_sides (__main__.ReaderProcessLocalityTests.test_g1_g2_each_frame_both_sides) (axis='frame0', excess=1) ... FAIL
  test_g1_g2_each_frame_both_sides (__main__.ReaderProcessLocalityTests.test_g1_g2_each_frame_both_sides) (axis='frame0', excess=2) ... FAIL
  test_g1_g2_each_frame_both_sides (__main__.ReaderProcessLocalityTests.test_g1_g2_each_frame_both_sides) (axis='frame1', excess=1) ... FAIL
  test_g1_g2_each_frame_both_sides (__main__.ReaderProcessLocalityTests.test_g1_g2_each_frame_both_sides) (axis='frame1', excess=2) ... FAIL
  test_g1_g2_each_frame_both_sides (__main__.ReaderProcessLocalityTests.test_g1_g2_each_frame_both_sides) (axis='frame2', excess=1) ... FAIL
  test_g1_g2_each_frame_both_sides (__main__.ReaderProcessLocalityTests.test_g1_g2_each_frame_both_sides) (axis='frame2', excess=2) ... FAIL
  test_g1_g2_each_frame_both_sides (__main__.ReaderProcessLocalityTests.test_g1_g2_each_frame_both_sides) (axis='frame3', excess=1) ... FAIL
  test_g1_g2_each_frame_both_sides (__main__.ReaderProcessLocalityTests.test_g1_g2_each_frame_both_sides) (axis='frame3', excess=2) ... FAIL
  test_g1_g2_each_frame_both_sides (__main__.ReaderProcessLocalityTests.test_g1_g2_each_frame_both_sides) (axis='frame4', excess=1) ... FAIL
  test_g1_g2_each_frame_both_sides (__main__.ReaderProcessLocalityTests.test_g1_g2_each_frame_both_sides) (axis='frame4', excess=2) ... FAIL
  test_g1_g2_each_frame_both_sides (__main__.ReaderProcessLocalityTests.test_g1_g2_each_frame_both_sides) (axis='frame5', excess=1) ... FAIL
  test_g1_g2_each_frame_both_sides (__main__.ReaderProcessLocalityTests.test_g1_g2_each_frame_both_sides) (axis='frame5', excess=2) ... FAIL
test_g3_g4_g5_unrounded_boundaries (__main__.ReaderProcessLocalityTests.test_g3_g4_g5_unrounded_boundaries) ... FAIL
test_g3_g5_display_rounding_cannot_substitute (__main__.ReaderProcessLocalityTests.test_g3_g5_display_rounding_cannot_substitute) ... FAIL
test_g6_relation_flips_report_only (__main__.ReaderProcessLocalityTests.test_g6_relation_flips_report_only) ... FAIL
test_p1_p2_p3 (__main__.ReaderProcessLocalityTests.test_p1_p2_p3) ... FAIL
test_p4_p5_p7_count_and_gain_boundaries (__main__.ReaderProcessLocalityTests.test_p4_p5_p7_count_and_gain_boundaries) ... FAIL
test_p6_tradeoff_and_p7_null_first_match (__main__.ReaderProcessLocalityTests.test_p6_tradeoff_and_p7_null_first_match) ... FAIL
test_w1_actual_size_boundary_qualifier_preserves_base (__main__.ReaderProcessLocalityTests.test_w1_actual_size_boundary_qualifier_preserves_base) ... FAIL
test_w2_ttl_warning_equality_nonblocking (__main__.ReaderProcessLocalityTests.test_w2_ttl_warning_equality_nonblocking) ... FAIL
test_authored_full_truth_rows_277_289 (__main__.ReaderTruthTableTests.test_authored_full_truth_rows_277_289) ... 
  test_authored_full_truth_rows_277_289 (__main__.ReaderTruthTableTests.test_authored_full_truth_rows_277_289) (prereg_line=277, case='controls24') ... FAIL
  test_authored_full_truth_rows_277_289 (__main__.ReaderTruthTableTests.test_authored_full_truth_rows_277_289) (prereg_line=278, case='controls20') ... FAIL
  test_authored_full_truth_rows_277_289 (__main__.ReaderTruthTableTests.test_authored_full_truth_rows_277_289) (prereg_line=279, case='nm17') ... FAIL
  test_authored_full_truth_rows_277_289 (__main__.ReaderTruthTableTests.test_authored_full_truth_rows_277_289) (prereg_line=280, case='anchor24') ... FAIL
  test_authored_full_truth_rows_277_289 (__main__.ReaderTruthTableTests.test_authored_full_truth_rows_277_289) (prereg_line=281, case='anchor_unfit') ... FAIL
  test_authored_full_truth_rows_277_289 (__main__.ReaderTruthTableTests.test_authored_full_truth_rows_277_289) (prereg_line=282, case='anchor_gap9') ... FAIL
  test_authored_full_truth_rows_277_289 (__main__.ReaderTruthTableTests.test_authored_full_truth_rows_277_289) (prereg_line=283, case='anchor_gap10') ... FAIL
  test_authored_full_truth_rows_277_289 (__main__.ReaderTruthTableTests.test_authored_full_truth_rows_277_289) (prereg_line=284, case='count18') ... FAIL
  test_authored_full_truth_rows_277_289 (__main__.ReaderTruthTableTests.test_authored_full_truth_rows_277_289) (prereg_line=285, case='counts30_22') ... FAIL
  test_authored_full_truth_rows_277_289 (__main__.ReaderTruthTableTests.test_authored_full_truth_rows_277_289) (prereg_line=286, case='baseline5_nm18') ... FAIL
  test_authored_full_truth_rows_277_289 (__main__.ReaderTruthTableTests.test_authored_full_truth_rows_277_289) (prereg_line=287, case='lead_tradeoff') ... FAIL
  test_authored_full_truth_rows_277_289 (__main__.ReaderTruthTableTests.test_authored_full_truth_rows_277_289) (prereg_line=287, case='lead_underfit') ... FAIL
  test_authored_full_truth_rows_277_289 (__main__.ReaderTruthTableTests.test_authored_full_truth_rows_277_289) (prereg_line=288, case='p2_halted') ... FAIL
  test_authored_full_truth_rows_277_289 (__main__.ReaderTruthTableTests.test_authored_full_truth_rows_277_289) (prereg_line=289, case='a1_67') ... FAIL
  test_authored_full_truth_rows_277_289 (__main__.ReaderTruthTableTests.test_authored_full_truth_rows_277_289) (prereg_line=289, case='nonfinite') ... FAIL
test_authored_stage1_truth_rows_265_276 (__main__.ReaderTruthTableTests.test_authored_stage1_truth_rows_265_276) ... 
  test_authored_stage1_truth_rows_265_276 (__main__.ReaderTruthTableTests.test_authored_stage1_truth_rows_265_276) (prereg_line=265, case='baseline') ... FAIL
  test_authored_stage1_truth_rows_265_276 (__main__.ReaderTruthTableTests.test_authored_stage1_truth_rows_265_276) (prereg_line=266, case='forecast130') ... FAIL
  test_authored_stage1_truth_rows_265_276 (__main__.ReaderTruthTableTests.test_authored_stage1_truth_rows_265_276) (prereg_line=267, case='deadline_afterwrite') ... FAIL
  test_authored_stage1_truth_rows_265_276 (__main__.ReaderTruthTableTests.test_authored_stage1_truth_rows_265_276) (prereg_line=268, case='projection_afterwrite') ... FAIL
  test_authored_stage1_truth_rows_265_276 (__main__.ReaderTruthTableTests.test_authored_stage1_truth_rows_265_276) (prereg_line=269, case='underfit25') ... FAIL
  test_authored_stage1_truth_rows_265_276 (__main__.ReaderTruthTableTests.test_authored_stage1_truth_rows_265_276) (prereg_line=270, case='count21') ... FAIL
  test_authored_stage1_truth_rows_265_276 (__main__.ReaderTruthTableTests.test_authored_stage1_truth_rows_265_276) (prereg_line=271, case='count22') ... FAIL
  test_authored_stage1_truth_rows_265_276 (__main__.ReaderTruthTableTests.test_authored_stage1_truth_rows_265_276) (prereg_line=272, case='large31') ... FAIL
  test_authored_stage1_truth_rows_265_276 (__main__.ReaderTruthTableTests.test_authored_stage1_truth_rows_265_276) (prereg_line=273, case='described25') ... FAIL
  test_authored_stage1_truth_rows_265_276 (__main__.ReaderTruthTableTests.test_authored_stage1_truth_rows_265_276) (prereg_line=274, case='frame27') ... FAIL
  test_authored_stage1_truth_rows_265_276 (__main__.ReaderTruthTableTests.test_authored_stage1_truth_rows_265_276) (prereg_line=275, case='baseline18_count27') ... FAIL
  test_authored_stage1_truth_rows_265_276 (__main__.ReaderTruthTableTests.test_authored_stage1_truth_rows_265_276) (prereg_line=275, case='baseline18_count28') ... FAIL
  test_authored_stage1_truth_rows_265_276 (__main__.ReaderTruthTableTests.test_authored_stage1_truth_rows_265_276) (prereg_line=276, case='baseline5_count19') ... FAIL
test_v10_overflow_retries_five_six (__main__.ReaderValidityTests.test_v10_overflow_retries_five_six) ... FAIL
test_v11_hin_hashes_and_write_trace_required (__main__.ReaderValidityTests.test_v11_hin_hashes_and_write_trace_required) ... 
  test_v11_hin_hashes_and_write_trace_required (__main__.ReaderValidityTests.test_v11_hin_hashes_and_write_trace_required) (missing='H_in') ... FAIL
  test_v11_hin_hashes_and_write_trace_required (__main__.ReaderValidityTests.test_v11_hin_hashes_and_write_trace_required) (missing='source_hash') ... FAIL
  test_v11_hin_hashes_and_write_trace_required (__main__.ReaderValidityTests.test_v11_hin_hashes_and_write_trace_required) (missing='artifact_hash') ... FAIL
  test_v11_hin_hashes_and_write_trace_required (__main__.ReaderValidityTests.test_v11_hin_hashes_and_write_trace_required) (missing='stop_reason') ... FAIL
  test_v11_hin_hashes_and_write_trace_required (__main__.ReaderValidityTests.test_v11_hin_hashes_and_write_trace_required) (missing='accepted_steps') ... FAIL
  test_v11_hin_hashes_and_write_trace_required (__main__.ReaderValidityTests.test_v11_hin_hashes_and_write_trace_required) (missing='overflow_retries') ... FAIL
  test_v11_hin_hashes_and_write_trace_required (__main__.ReaderValidityTests.test_v11_hin_hashes_and_write_trace_required) (missing='H_out') ... FAIL
test_v12_leakage_named_halt (__main__.ReaderValidityTests.test_v12_leakage_named_halt) ... FAIL
test_v13_every_applicable_numeric_family_nonfinite (__main__.ReaderValidityTests.test_v13_every_applicable_numeric_family_nonfinite) ... 
  test_v13_every_applicable_numeric_family_nonfinite (__main__.ReaderValidityTests.test_v13_every_applicable_numeric_family_nonfinite) (family='raw_described', value=None) ... FAIL
  test_v13_every_applicable_numeric_family_nonfinite (__main__.ReaderValidityTests.test_v13_every_applicable_numeric_family_nonfinite) (family='raw_described', value=nan) ... FAIL
  test_v13_every_applicable_numeric_family_nonfinite (__main__.ReaderValidityTests.test_v13_every_applicable_numeric_family_nonfinite) (family='raw_described', value=inf) ... FAIL
  test_v13_every_applicable_numeric_family_nonfinite (__main__.ReaderValidityTests.test_v13_every_applicable_numeric_family_nonfinite) (family='raw_described', value=-inf) ... FAIL
  test_v13_every_applicable_numeric_family_nonfinite (__main__.ReaderValidityTests.test_v13_every_applicable_numeric_family_nonfinite) (family='raw_ppl', value=None) ... FAIL
  test_v13_every_applicable_numeric_family_nonfinite (__main__.ReaderValidityTests.test_v13_every_applicable_numeric_family_nonfinite) (family='raw_ppl', value=nan) ... FAIL
  test_v13_every_applicable_numeric_family_nonfinite (__main__.ReaderValidityTests.test_v13_every_applicable_numeric_family_nonfinite) (family='raw_ppl', value=inf) ... FAIL
  test_v13_every_applicable_numeric_family_nonfinite (__main__.ReaderValidityTests.test_v13_every_applicable_numeric_family_nonfinite) (family='raw_ppl', value=-inf) ... FAIL
  test_v13_every_applicable_numeric_family_nonfinite (__main__.ReaderValidityTests.test_v13_every_applicable_numeric_family_nonfinite) (family='actual_norm', value=None) ... FAIL
  test_v13_every_applicable_numeric_family_nonfinite (__main__.ReaderValidityTests.test_v13_every_applicable_numeric_family_nonfinite) (family='actual_norm', value=nan) ... FAIL
  test_v13_every_applicable_numeric_family_nonfinite (__main__.ReaderValidityTests.test_v13_every_applicable_numeric_family_nonfinite) (family='actual_norm', value=inf) ... FAIL
  test_v13_every_applicable_numeric_family_nonfinite (__main__.ReaderValidityTests.test_v13_every_applicable_numeric_family_nonfinite) (family='actual_norm', value=-inf) ... FAIL
  test_v13_every_applicable_numeric_family_nonfinite (__main__.ReaderValidityTests.test_v13_every_applicable_numeric_family_nonfinite) (family='planned_norm', value=None) ... FAIL
  test_v13_every_applicable_numeric_family_nonfinite (__main__.ReaderValidityTests.test_v13_every_applicable_numeric_family_nonfinite) (family='planned_norm', value=nan) ... FAIL
  test_v13_every_applicable_numeric_family_nonfinite (__main__.ReaderValidityTests.test_v13_every_applicable_numeric_family_nonfinite) (family='planned_norm', value=inf) ... FAIL
  test_v13_every_applicable_numeric_family_nonfinite (__main__.ReaderValidityTests.test_v13_every_applicable_numeric_family_nonfinite) (family='planned_norm', value=-inf) ... FAIL
  test_v13_every_applicable_numeric_family_nonfinite (__main__.ReaderValidityTests.test_v13_every_applicable_numeric_family_nonfinite) (family='null_share', value=None) ... FAIL
  test_v13_every_applicable_numeric_family_nonfinite (__main__.ReaderValidityTests.test_v13_every_applicable_numeric_family_nonfinite) (family='null_share', value=nan) ... FAIL
  test_v13_every_applicable_numeric_family_nonfinite (__main__.ReaderValidityTests.test_v13_every_applicable_numeric_family_nonfinite) (family='null_share', value=inf) ... FAIL
  test_v13_every_applicable_numeric_family_nonfinite (__main__.ReaderValidityTests.test_v13_every_applicable_numeric_family_nonfinite) (family='null_share', value=-inf) ... FAIL
  test_v13_every_applicable_numeric_family_nonfinite (__main__.ReaderValidityTests.test_v13_every_applicable_numeric_family_nonfinite) (family='fit_probability', value=None) ... FAIL
  test_v13_every_applicable_numeric_family_nonfinite (__main__.ReaderValidityTests.test_v13_every_applicable_numeric_family_nonfinite) (family='fit_probability', value=nan) ... FAIL
  test_v13_every_applicable_numeric_family_nonfinite (__main__.ReaderValidityTests.test_v13_every_applicable_numeric_family_nonfinite) (family='fit_probability', value=inf) ... FAIL
  test_v13_every_applicable_numeric_family_nonfinite (__main__.ReaderValidityTests.test_v13_every_applicable_numeric_family_nonfinite) (family='fit_probability', value=-inf) ... FAIL
  test_v13_every_applicable_numeric_family_nonfinite (__main__.ReaderValidityTests.test_v13_every_applicable_numeric_family_nonfinite) (family='compile_time', value=None) ... FAIL
  test_v13_every_applicable_numeric_family_nonfinite (__main__.ReaderValidityTests.test_v13_every_applicable_numeric_family_nonfinite) (family='compile_time', value=nan) ... FAIL
  test_v13_every_applicable_numeric_family_nonfinite (__main__.ReaderValidityTests.test_v13_every_applicable_numeric_family_nonfinite) (family='compile_time', value=inf) ... FAIL
  test_v13_every_applicable_numeric_family_nonfinite (__main__.ReaderValidityTests.test_v13_every_applicable_numeric_family_nonfinite) (family='compile_time', value=-inf) ... FAIL
  test_v13_every_applicable_numeric_family_nonfinite (__main__.ReaderValidityTests.test_v13_every_applicable_numeric_family_nonfinite) (family='capture_distance', value=None) ... FAIL
  test_v13_every_applicable_numeric_family_nonfinite (__main__.ReaderValidityTests.test_v13_every_applicable_numeric_family_nonfinite) (family='capture_distance', value=nan) ... FAIL
  test_v13_every_applicable_numeric_family_nonfinite (__main__.ReaderValidityTests.test_v13_every_applicable_numeric_family_nonfinite) (family='capture_distance', value=inf) ... FAIL
  test_v13_every_applicable_numeric_family_nonfinite (__main__.ReaderValidityTests.test_v13_every_applicable_numeric_family_nonfinite) (family='capture_distance', value=-inf) ... FAIL
test_v13_nonfinite_unjustified_null_and_typed_integer (__main__.ReaderValidityTests.test_v13_nonfinite_unjustified_null_and_typed_integer) ... FAIL
test_v13_typed_nulls_and_reasons (__main__.ReaderValidityTests.test_v13_typed_nulls_and_reasons) ... FAIL
test_v1_fingerprint_sha_sites_and_full_output (__main__.ReaderValidityTests.test_v1_fingerprint_sha_sites_and_full_output) ... 
  test_v1_fingerprint_sha_sites_and_full_output (__main__.ReaderValidityTests.test_v1_fingerprint_sha_sites_and_full_output) (field='sha256', value='2222222222222222222222222222222222222222222222222222222222222222') ... FAIL
  test_v1_fingerprint_sha_sites_and_full_output (__main__.ReaderValidityTests.test_v1_fingerprint_sha_sites_and_full_output) (field='cov_cpu_sites', value=2) ... FAIL
  test_v1_fingerprint_sha_sites_and_full_output (__main__.ReaderValidityTests.test_v1_fingerprint_sha_sites_and_full_output) (field='cov_cpu_sites', value=4) ... FAIL
  test_v1_fingerprint_sha_sites_and_full_output (__main__.ReaderValidityTests.test_v1_fingerprint_sha_sites_and_full_output) (field='output', value='') ... FAIL
test_v2_each_recipe_standing_law5 (__main__.ReaderValidityTests.test_v2_each_recipe_standing_law5) ... FAIL
test_v3_accumulation_raw_cosine_distance_finiteness_and_scope (__main__.ReaderValidityTests.test_v3_accumulation_raw_cosine_distance_finiteness_and_scope) ... FAIL
test_v3_apply_stored_substitutions_not_optimiser_checks (__main__.ReaderValidityTests.test_v3_apply_stored_substitutions_not_optimiser_checks) ... FAIL
test_v3_capture_zero_step_and_executed_loop_raw_values (__main__.ReaderValidityTests.test_v3_capture_zero_step_and_executed_loop_raw_values) ... FAIL
test_v3_check_failure_order_and_scope (__main__.ReaderValidityTests.test_v3_check_failure_order_and_scope) ... 
  test_v3_check_failure_order_and_scope (__main__.ReaderValidityTests.test_v3_check_failure_order_and_scope) (arm='A1_single', failure='passed') ... FAIL
  test_v3_check_failure_order_and_scope (__main__.ReaderValidityTests.test_v3_check_failure_order_and_scope) (arm='A1_single', failure='before_result') ... FAIL
  test_v3_check_failure_order_and_scope (__main__.ReaderValidityTests.test_v3_check_failure_order_and_scope) (arm='A1_single', failure='scope') ... FAIL
  test_v3_check_failure_order_and_scope (__main__.ReaderValidityTests.test_v3_check_failure_order_and_scope) (arm='A2_coherent2', failure='passed') ... FAIL
  test_v3_check_failure_order_and_scope (__main__.ReaderValidityTests.test_v3_check_failure_order_and_scope) (arm='A2_coherent2', failure='before_result') ... FAIL
  test_v3_check_failure_order_and_scope (__main__.ReaderValidityTests.test_v3_check_failure_order_and_scope) (arm='A2_coherent2', failure='scope') ... FAIL
  test_v3_check_failure_order_and_scope (__main__.ReaderValidityTests.test_v3_check_failure_order_and_scope) (arm='A7_coined_coined', failure='passed') ... FAIL
  test_v3_check_failure_order_and_scope (__main__.ReaderValidityTests.test_v3_check_failure_order_and_scope) (arm='A7_coined_coined', failure='before_result') ... FAIL
  test_v3_check_failure_order_and_scope (__main__.ReaderValidityTests.test_v3_check_failure_order_and_scope) (arm='A7_coined_coined', failure='scope') ... FAIL
test_v3_gradient_halvings_hooks_and_smoke_raw_values (__main__.ReaderValidityTests.test_v3_gradient_halvings_hooks_and_smoke_raw_values) ... FAIL
test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) ... 
  test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-e2e', arm='A1_single', check='capture') ... FAIL
  test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-e2e', arm='A1_single', check='zero_step') ... FAIL
  test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-e2e', arm='A1_single', check='executed_loop') ... FAIL
  test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-e2e', arm='A1_single', check='projector') ... FAIL
  test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-e2e', arm='A1_single', check='hooks') ... FAIL
  test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-e2e', arm='A1_single', check='train_deploy') ... FAIL
  test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-e2e', arm='A1_single', check='gradient') ... FAIL
  test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-e2e', arm='A2_coherent2', check='capture') ... FAIL
  test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-e2e', arm='A2_coherent2', check='zero_step') ... FAIL
  test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-e2e', arm='A2_coherent2', check='executed_loop') ... FAIL
  test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-e2e', arm='A2_coherent2', check='projector') ... FAIL
  test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-e2e', arm='A2_coherent2', check='hooks') ... FAIL
  test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-e2e', arm='A2_coherent2', check='train_deploy') ... FAIL
  test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-e2e', arm='A2_coherent2', check='gradient') ... FAIL
  test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-e2e', arm='A7_coined_coined', check='capture') ... FAIL
  test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-e2e', arm='A7_coined_coined', check='zero_step') ... FAIL
  test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-e2e', arm='A7_coined_coined', check='executed_loop') ... FAIL
  test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-e2e', arm='A7_coined_coined', check='projector') ... FAIL
  test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-e2e', arm='A7_coined_coined', check='hooks') ... FAIL
  test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-e2e', arm='A7_coined_coined', check='train_deploy') ... FAIL
  test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-e2e', arm='A7_coined_coined', check='gradient') ... FAIL
  test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-e2e', arm='A7_coined_coined', check='accumulation') ... FAIL
  test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-e2e', arm='A7_coined_coined', check='objective') ... FAIL
  test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-e2e', arm='A7_coined_coined', check='smoke') ... FAIL
  test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-z', arm='A1_single', check='capture') ... FAIL
  test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-z', arm='A1_single', check='zero_step') ... FAIL
  test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-z', arm='A1_single', check='executed_loop') ... FAIL
  test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-z', arm='A1_single', check='projector') ... FAIL
  test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-z', arm='A1_single', check='hooks') ... FAIL
  test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-z', arm='A1_single', check='train_deploy') ... FAIL
  test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-z', arm='A1_single', check='gradient') ... FAIL
  test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-z', arm='A2_coherent2', check='capture') ... FAIL
  test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-z', arm='A2_coherent2', check='zero_step') ... FAIL
  test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-z', arm='A2_coherent2', check='executed_loop') ... FAIL
  test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-z', arm='A2_coherent2', check='projector') ... FAIL
  test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-z', arm='A2_coherent2', check='hooks') ... FAIL
  test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-z', arm='A2_coherent2', check='train_deploy') ... FAIL
  test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-z', arm='A2_coherent2', check='gradient') ... FAIL
  test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-z', arm='A7_coined_coined', check='capture') ... FAIL
  test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-z', arm='A7_coined_coined', check='zero_step') ... FAIL
  test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-z', arm='A7_coined_coined', check='executed_loop') ... FAIL
  test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-z', arm='A7_coined_coined', check='projector') ... FAIL
  test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-z', arm='A7_coined_coined', check='hooks') ... FAIL
  test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-z', arm='A7_coined_coined', check='train_deploy') ... FAIL
  test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-z', arm='A7_coined_coined', check='gradient') ... FAIL
  test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-z', arm='A7_coined_coined', check='accumulation') ... FAIL
test_v3_objective_nll_and_nonzero_kl_raw_boundaries (__main__.ReaderValidityTests.test_v3_objective_nll_and_nonzero_kl_raw_boundaries) ... FAIL
test_v4_a1_a2_and_exact_denominators (__main__.ReaderValidityTests.test_v4_a1_a2_and_exact_denominators) ... FAIL
test_v4_all_inclusive_baseline_endpoints (__main__.ReaderValidityTests.test_v4_all_inclusive_baseline_endpoints) ... 
  test_v4_all_inclusive_baseline_endpoints (__main__.ReaderValidityTests.test_v4_all_inclusive_baseline_endpoints) (field='para_full_n', value=4) ... FAIL
  test_v4_all_inclusive_baseline_endpoints (__main__.ReaderValidityTests.test_v4_all_inclusive_baseline_endpoints) (field='para_full_n', value=5) ... FAIL
  test_v4_all_inclusive_baseline_endpoints (__main__.ReaderValidityTests.test_v4_all_inclusive_baseline_endpoints) (field='para_full_n', value=18) ... FAIL
  test_v4_all_inclusive_baseline_endpoints (__main__.ReaderValidityTests.test_v4_all_inclusive_baseline_endpoints) (field='para_full_n', value=19) ... FAIL
  test_v4_all_inclusive_baseline_endpoints (__main__.ReaderValidityTests.test_v4_all_inclusive_baseline_endpoints) (field='canon_full_n', value=4) ... FAIL
  test_v4_all_inclusive_baseline_endpoints (__main__.ReaderValidityTests.test_v4_all_inclusive_baseline_endpoints) (field='canon_full_n', value=5) ... FAIL
  test_v4_all_inclusive_baseline_endpoints (__main__.ReaderValidityTests.test_v4_all_inclusive_baseline_endpoints) (field='canon_full_n', value=10) ... FAIL
  test_v4_all_inclusive_baseline_endpoints (__main__.ReaderValidityTests.test_v4_all_inclusive_baseline_endpoints) (field='canon_full_n', value=11) ... FAIL
  test_v4_all_inclusive_baseline_endpoints (__main__.ReaderValidityTests.test_v4_all_inclusive_baseline_endpoints) (field='para_first_n', value=41) ... FAIL
  test_v4_all_inclusive_baseline_endpoints (__main__.ReaderValidityTests.test_v4_all_inclusive_baseline_endpoints) (field='para_first_n', value=42) ... FAIL
  test_v4_all_inclusive_baseline_endpoints (__main__.ReaderValidityTests.test_v4_all_inclusive_baseline_endpoints) (field='para_first_n', value=59) ... FAIL
  test_v4_all_inclusive_baseline_endpoints (__main__.ReaderValidityTests.test_v4_all_inclusive_baseline_endpoints) (field='para_first_n', value=60) ... FAIL
test_v4_before_candidates_required (__main__.ReaderValidityTests.test_v4_before_candidates_required) ... FAIL
test_v5_candidate_controls_67_68_each_arm (__main__.ReaderValidityTests.test_v5_candidate_controls_67_68_each_arm) ... 
  test_v5_candidate_controls_67_68_each_arm (__main__.ReaderValidityTests.test_v5_candidate_controls_67_68_each_arm) (arm='A1_single', value=67) ... FAIL
  test_v5_candidate_controls_67_68_each_arm (__main__.ReaderValidityTests.test_v5_candidate_controls_67_68_each_arm) (arm='A1_single', value=68) ... FAIL
  test_v5_candidate_controls_67_68_each_arm (__main__.ReaderValidityTests.test_v5_candidate_controls_67_68_each_arm) (arm='A2_coherent2', value=67) ... FAIL
  test_v5_candidate_controls_67_68_each_arm (__main__.ReaderValidityTests.test_v5_candidate_controls_67_68_each_arm) (arm='A2_coherent2', value=68) ... FAIL
test_v6_overrides_are_exact_sets_not_counts (__main__.ReaderValidityTests.test_v6_overrides_are_exact_sets_not_counts) ... 
  test_v6_overrides_are_exact_sets_not_counts (__main__.ReaderValidityTests.test_v6_overrides_are_exact_sets_not_counts) (failure='missing') ... FAIL
  test_v6_overrides_are_exact_sets_not_counts (__main__.ReaderValidityTests.test_v6_overrides_are_exact_sets_not_counts) (failure='undeclared') ... FAIL
  test_v6_overrides_are_exact_sets_not_counts (__main__.ReaderValidityTests.test_v6_overrides_are_exact_sets_not_counts) (failure='wrong_same_count') ... FAIL
  test_v6_overrides_are_exact_sets_not_counts (__main__.ReaderValidityTests.test_v6_overrides_are_exact_sets_not_counts) (failure='not_run_consumed') ... FAIL
  test_v6_overrides_are_exact_sets_not_counts (__main__.ReaderValidityTests.test_v6_overrides_are_exact_sets_not_counts) (failure='check_not_separate') ... FAIL
test_v7_initial_projector_raw_share_cannot_hide_behind_passed (__main__.ReaderValidityTests.test_v7_initial_projector_raw_share_cannot_hide_behind_passed) ... FAIL
test_v7_planned_actual_each_layer_boundary_and_zero (__main__.ReaderValidityTests.test_v7_planned_actual_each_layer_boundary_and_zero) ... 
  test_v7_planned_actual_each_layer_boundary_and_zero (__main__.ReaderValidityTests.test_v7_planned_actual_each_layer_boundary_and_zero) (field='planned_null_share', layer=0, value=0.999) ... FAIL
  test_v7_planned_actual_each_layer_boundary_and_zero (__main__.ReaderValidityTests.test_v7_planned_actual_each_layer_boundary_and_zero) (field='planned_null_share', layer=0, value=0.9989999) ... FAIL
  test_v7_planned_actual_each_layer_boundary_and_zero (__main__.ReaderValidityTests.test_v7_planned_actual_each_layer_boundary_and_zero) (field='planned_null_share', layer=1, value=0.999) ... FAIL
  test_v7_planned_actual_each_layer_boundary_and_zero (__main__.ReaderValidityTests.test_v7_planned_actual_each_layer_boundary_and_zero) (field='planned_null_share', layer=1, value=0.9989999) ... FAIL
  test_v7_planned_actual_each_layer_boundary_and_zero (__main__.ReaderValidityTests.test_v7_planned_actual_each_layer_boundary_and_zero) (field='planned_null_share', layer=2, value=0.999) ... FAIL
  test_v7_planned_actual_each_layer_boundary_and_zero (__main__.ReaderValidityTests.test_v7_planned_actual_each_layer_boundary_and_zero) (field='planned_null_share', layer=2, value=0.9989999) ... FAIL
  test_v7_planned_actual_each_layer_boundary_and_zero (__main__.ReaderValidityTests.test_v7_planned_actual_each_layer_boundary_and_zero) (field='planned_null_share', layer=3, value=0.999) ... FAIL
  test_v7_planned_actual_each_layer_boundary_and_zero (__main__.ReaderValidityTests.test_v7_planned_actual_each_layer_boundary_and_zero) (field='planned_null_share', layer=3, value=0.9989999) ... FAIL
  test_v7_planned_actual_each_layer_boundary_and_zero (__main__.ReaderValidityTests.test_v7_planned_actual_each_layer_boundary_and_zero) (field='planned_null_share', layer=4, value=0.999) ... FAIL
  test_v7_planned_actual_each_layer_boundary_and_zero (__main__.ReaderValidityTests.test_v7_planned_actual_each_layer_boundary_and_zero) (field='planned_null_share', layer=4, value=0.9989999) ... FAIL
  test_v7_planned_actual_each_layer_boundary_and_zero (__main__.ReaderValidityTests.test_v7_planned_actual_each_layer_boundary_and_zero) (field='actual_null_share', layer=0, value=0.999) ... FAIL
  test_v7_planned_actual_each_layer_boundary_and_zero (__main__.ReaderValidityTests.test_v7_planned_actual_each_layer_boundary_and_zero) (field='actual_null_share', layer=0, value=0.9989999) ... FAIL
  test_v7_planned_actual_each_layer_boundary_and_zero (__main__.ReaderValidityTests.test_v7_planned_actual_each_layer_boundary_and_zero) (field='actual_null_share', layer=1, value=0.999) ... FAIL
  test_v7_planned_actual_each_layer_boundary_and_zero (__main__.ReaderValidityTests.test_v7_planned_actual_each_layer_boundary_and_zero) (field='actual_null_share', layer=1, value=0.9989999) ... FAIL
  test_v7_planned_actual_each_layer_boundary_and_zero (__main__.ReaderValidityTests.test_v7_planned_actual_each_layer_boundary_and_zero) (field='actual_null_share', layer=2, value=0.999) ... FAIL
  test_v7_planned_actual_each_layer_boundary_and_zero (__main__.ReaderValidityTests.test_v7_planned_actual_each_layer_boundary_and_zero) (field='actual_null_share', layer=2, value=0.9989999) ... FAIL
  test_v7_planned_actual_each_layer_boundary_and_zero (__main__.ReaderValidityTests.test_v7_planned_actual_each_layer_boundary_and_zero) (field='actual_null_share', layer=3, value=0.999) ... FAIL
  test_v7_planned_actual_each_layer_boundary_and_zero (__main__.ReaderValidityTests.test_v7_planned_actual_each_layer_boundary_and_zero) (field='actual_null_share', layer=3, value=0.9989999) ... FAIL
  test_v7_planned_actual_each_layer_boundary_and_zero (__main__.ReaderValidityTests.test_v7_planned_actual_each_layer_boundary_and_zero) (field='actual_null_share', layer=4, value=0.999) ... FAIL
  test_v7_planned_actual_each_layer_boundary_and_zero (__main__.ReaderValidityTests.test_v7_planned_actual_each_layer_boundary_and_zero) (field='actual_null_share', layer=4, value=0.9989999) ... FAIL
test_v7_planned_actual_each_layer_boundary_and_zero (__main__.ReaderValidityTests.test_v7_planned_actual_each_layer_boundary_and_zero) ... FAIL
test_v7_untouched_reference_miss_halts_precision_diagnosis (__main__.ReaderValidityTests.test_v7_untouched_reference_miss_halts_precision_diagnosis) ... FAIL
test_v8_string_full_equality_and_one_below_every_arm (__main__.ReaderValidityTests.test_v8_string_full_equality_and_one_below_every_arm) ... FAIL
test_v9_init_final_tokens_and_each_loss_component (__main__.ReaderValidityTests.test_v9_init_final_tokens_and_each_loss_component) ... FAIL
test_T11_audit_accepts_every_kind_with_only_kind_specific_fields (__main__.TelemetryCheckContract.test_T11_audit_accepts_every_kind_with_only_kind_specific_fields) ... FAIL
test_T11_audit_checks_payload_types_for_every_non_answer_kind (__main__.TelemetryCheckContract.test_T11_audit_checks_payload_types_for_every_non_answer_kind) ... 
  test_T11_audit_checks_payload_types_for_every_non_answer_kind (__main__.TelemetryCheckContract.test_T11_audit_checks_payload_types_for_every_non_answer_kind) (kind='phase') ... FAIL
  test_T11_audit_checks_payload_types_for_every_non_answer_kind (__main__.TelemetryCheckContract.test_T11_audit_checks_payload_types_for_every_non_answer_kind) (kind='opt_step') ... FAIL
  test_T11_audit_checks_payload_types_for_every_non_answer_kind (__main__.TelemetryCheckContract.test_T11_audit_checks_payload_types_for_every_non_answer_kind) (kind='target_probs') ... FAIL
  test_T11_audit_checks_payload_types_for_every_non_answer_kind (__main__.TelemetryCheckContract.test_T11_audit_checks_payload_types_for_every_non_answer_kind) (kind='write_norms') ... FAIL
  test_T11_audit_checks_payload_types_for_every_non_answer_kind (__main__.TelemetryCheckContract.test_T11_audit_checks_payload_types_for_every_non_answer_kind) (kind='logit_lens') ... FAIL
test_T11_audit_complete_answer_keys_pass_and_roundtrip (__main__.TelemetryCheckContract.test_T11_audit_complete_answer_keys_pass_and_roundtrip) ... FAIL
test_T11_audit_declared_disabled_missing_output_keeps_science_record (__main__.TelemetryCheckContract.test_T11_audit_declared_disabled_missing_output_keeps_science_record) ... FAIL
test_T11_audit_disabled_marker_does_not_excuse_a_gap_before_later_answers (__main__.TelemetryCheckContract.test_T11_audit_disabled_marker_does_not_excuse_a_gap_before_later_answers) ... FAIL
test_T11_audit_disabled_marker_does_not_excuse_mismatching_existing_line (__main__.TelemetryCheckContract.test_T11_audit_disabled_marker_does_not_excuse_mismatching_existing_line) ... FAIL
test_T11_audit_duplicate_answer_key_compromises_stage (__main__.TelemetryCheckContract.test_T11_audit_duplicate_answer_key_compromises_stage) ... FAIL
test_T11_audit_header_must_be_present_initial_and_unique (__main__.TelemetryCheckContract.test_T11_audit_header_must_be_present_initial_and_unique) ... 
  test_T11_audit_header_must_be_present_initial_and_unique (__main__.TelemetryCheckContract.test_T11_audit_header_must_be_present_initial_and_unique) (variant='absent') ... FAIL
  test_T11_audit_header_must_be_present_initial_and_unique (__main__.TelemetryCheckContract.test_T11_audit_header_must_be_present_initial_and_unique) (variant='not_first') ... FAIL
  test_T11_audit_header_must_be_present_initial_and_unique (__main__.TelemetryCheckContract.test_T11_audit_header_must_be_present_initial_and_unique) (variant='repeated') ... FAIL
  test_T11_audit_header_must_be_present_initial_and_unique (__main__.TelemetryCheckContract.test_T11_audit_header_must_be_present_initial_and_unique) (variant='wrong_schema') ... FAIL
  test_T11_audit_header_must_be_present_initial_and_unique (__main__.TelemetryCheckContract.test_T11_audit_header_must_be_present_initial_and_unique) (variant='telemetry_not_bool') ... FAIL
test_T11_audit_mismatch_compromises_stage_and_requires_telemetry_off_rerun (__main__.TelemetryCheckContract.test_T11_audit_mismatch_compromises_stage_and_requires_telemetry_off_rerun) ... 
  test_T11_audit_mismatch_compromises_stage_and_requires_telemetry_off_rerun (__main__.TelemetryCheckContract.test_T11_audit_mismatch_compromises_stage_and_requires_telemetry_off_rerun) (field='full') ... FAIL
  test_T11_audit_mismatch_compromises_stage_and_requires_telemetry_off_rerun (__main__.TelemetryCheckContract.test_T11_audit_mismatch_compromises_stage_and_requires_telemetry_off_rerun) (field='first') ... FAIL
test_T11_audit_missing_answer_field_is_malformed (__main__.TelemetryCheckContract.test_T11_audit_missing_answer_field_is_malformed) ... 
  test_T11_audit_missing_answer_field_is_malformed (__main__.TelemetryCheckContract.test_T11_audit_missing_answer_field_is_malformed) (field='val') ... FAIL
  test_T11_audit_missing_answer_field_is_malformed (__main__.TelemetryCheckContract.test_T11_audit_missing_answer_field_is_malformed) (field='target_ids') ... FAIL
  test_T11_audit_missing_answer_field_is_malformed (__main__.TelemetryCheckContract.test_T11_audit_missing_answer_field_is_malformed) (field='first') ... FAIL
  test_T11_audit_missing_answer_field_is_malformed (__main__.TelemetryCheckContract.test_T11_audit_missing_answer_field_is_malformed) (field='process') ... FAIL
  test_T11_audit_missing_answer_field_is_malformed (__main__.TelemetryCheckContract.test_T11_audit_missing_answer_field_is_malformed) (field='run_id') ... FAIL
test_T11_audit_missing_expected_key_compromises_stage (__main__.TelemetryCheckContract.test_T11_audit_missing_expected_key_compromises_stage) ... FAIL
test_T11_audit_missing_file_is_missing_output (__main__.TelemetryCheckContract.test_T11_audit_missing_file_is_missing_output) ... FAIL
test_T11_audit_model_free_entrypoint_never_loads_driver_or_harness (__main__.TelemetryCheckContract.test_T11_audit_model_free_entrypoint_never_loads_driver_or_harness) ... FAIL
test_T11_audit_never_mutates_science_records_or_reader_output (__main__.TelemetryCheckContract.test_T11_audit_never_mutates_science_records_or_reader_output) ... FAIL
test_T11_audit_refuses_existing_audit_without_rewriting_evidence (__main__.TelemetryCheckContract.test_T11_audit_refuses_existing_audit_without_rewriting_evidence) ... FAIL
test_T11_audit_rejects_unknown_field_on_every_known_kind (__main__.TelemetryCheckContract.test_T11_audit_rejects_unknown_field_on_every_known_kind) ... 
  test_T11_audit_rejects_unknown_field_on_every_known_kind (__main__.TelemetryCheckContract.test_T11_audit_rejects_unknown_field_on_every_known_kind) (kind='phase') ... FAIL
  test_T11_audit_rejects_unknown_field_on_every_known_kind (__main__.TelemetryCheckContract.test_T11_audit_rejects_unknown_field_on_every_known_kind) (kind='opt_step') ... FAIL
  test_T11_audit_rejects_unknown_field_on_every_known_kind (__main__.TelemetryCheckContract.test_T11_audit_rejects_unknown_field_on_every_known_kind) (kind='target_probs') ... FAIL
  test_T11_audit_rejects_unknown_field_on_every_known_kind (__main__.TelemetryCheckContract.test_T11_audit_rejects_unknown_field_on_every_known_kind) (kind='write_norms') ... FAIL
  test_T11_audit_rejects_unknown_field_on_every_known_kind (__main__.TelemetryCheckContract.test_T11_audit_rejects_unknown_field_on_every_known_kind) (kind='logit_lens') ... FAIL
test_T11_audit_strict_json_rejects_nonfinite_and_duplicate_json_fields (__main__.TelemetryCheckContract.test_T11_audit_strict_json_rejects_nonfinite_and_duplicate_json_fields) ... 
  test_T11_audit_strict_json_rejects_nonfinite_and_duplicate_json_fields (__main__.TelemetryCheckContract.test_T11_audit_strict_json_rejects_nonfinite_and_duplicate_json_fields) (text='{bad json}\n') ... FAIL
  test_T11_audit_strict_json_rejects_nonfinite_and_duplicate_json_fields (__main__.TelemetryCheckContract.test_T11_audit_strict_json_rejects_nonfinite_and_duplicate_json_fields) (text='{"kind":"answer","elapsed_s":NaN}\n') ... FAIL
  test_T11_audit_strict_json_rejects_nonfinite_and_duplicate_json_fields (__main__.TelemetryCheckContract.test_T11_audit_strict_json_rejects_nonfinite_and_duplicate_json_fields) (text='{"kind":"answer","elapsed_s":Infinity}\n') ... FAIL
  test_T11_audit_strict_json_rejects_nonfinite_and_duplicate_json_fields (__main__.TelemetryCheckContract.test_T11_audit_strict_json_rejects_nonfinite_and_duplicate_json_fields) (text='{"kind":"answer","kind":"phase"}\n') ... FAIL
test_T11_audit_unknown_key_or_kind_or_field_is_unexpected (__main__.TelemetryCheckContract.test_T11_audit_unknown_key_or_kind_or_field_is_unexpected) ... 
  test_T11_audit_unknown_key_or_kind_or_field_is_unexpected (__main__.TelemetryCheckContract.test_T11_audit_unknown_key_or_kind_or_field_is_unexpected) (variant='recipe') ... FAIL
  test_T11_audit_unknown_key_or_kind_or_field_is_unexpected (__main__.TelemetryCheckContract.test_T11_audit_unknown_key_or_kind_or_field_is_unexpected) (variant='arm') ... FAIL
  test_T11_audit_unknown_key_or_kind_or_field_is_unexpected (__main__.TelemetryCheckContract.test_T11_audit_unknown_key_or_kind_or_field_is_unexpected) (variant='subj') ... FAIL
  test_T11_audit_unknown_key_or_kind_or_field_is_unexpected (__main__.TelemetryCheckContract.test_T11_audit_unknown_key_or_kind_or_field_is_unexpected) (variant='template') ... FAIL
  test_T11_audit_unknown_key_or_kind_or_field_is_unexpected (__main__.TelemetryCheckContract.test_T11_audit_unknown_key_or_kind_or_field_is_unexpected) (variant='unknown_kind') ... FAIL
  test_T11_audit_unknown_key_or_kind_or_field_is_unexpected (__main__.TelemetryCheckContract.test_T11_audit_unknown_key_or_kind_or_field_is_unexpected) (variant='unknown_field') ... FAIL
  test_T11_audit_unknown_key_or_kind_or_field_is_unexpected (__main__.TelemetryCheckContract.test_T11_audit_unknown_key_or_kind_or_field_is_unexpected) (variant='header_field') ... FAIL
test_T11_audit_uses_stage_two_and_three_tags_and_record_paths (__main__.TelemetryCheckContract.test_T11_audit_uses_stage_two_and_three_tags_and_record_paths) ... 
  test_T11_audit_uses_stage_two_and_three_tags_and_record_paths (__main__.TelemetryCheckContract.test_T11_audit_uses_stage_two_and_three_tags_and_record_paths) (stage=2) ... FAIL
  test_T11_audit_uses_stage_two_and_three_tags_and_record_paths (__main__.TelemetryCheckContract.test_T11_audit_uses_stage_two_and_three_tags_and_record_paths) (stage=3) ... FAIL
test_T11_audit_wrong_types_and_nulls_are_malformed (__main__.TelemetryCheckContract.test_T11_audit_wrong_types_and_nulls_are_malformed) ... 
  test_T11_audit_wrong_types_and_nulls_are_malformed (__main__.TelemetryCheckContract.test_T11_audit_wrong_types_and_nulls_are_malformed) (field='full', value=1) ... FAIL
  test_T11_audit_wrong_types_and_nulls_are_malformed (__main__.TelemetryCheckContract.test_T11_audit_wrong_types_and_nulls_are_malformed) (field='first', value='true') ... FAIL
  test_T11_audit_wrong_types_and_nulls_are_malformed (__main__.TelemetryCheckContract.test_T11_audit_wrong_types_and_nulls_are_malformed) (field='subj', value=None) ... FAIL
  test_T11_audit_wrong_types_and_nulls_are_malformed (__main__.TelemetryCheckContract.test_T11_audit_wrong_types_and_nulls_are_malformed) (field='template', value=None) ... FAIL
  test_T11_audit_wrong_types_and_nulls_are_malformed (__main__.TelemetryCheckContract.test_T11_audit_wrong_types_and_nulls_are_malformed) (field='val', value=None) ... FAIL
  test_T11_audit_wrong_types_and_nulls_are_malformed (__main__.TelemetryCheckContract.test_T11_audit_wrong_types_and_nulls_are_malformed) (field='target_ids', value=[True]) ... FAIL
  test_T11_audit_wrong_types_and_nulls_are_malformed (__main__.TelemetryCheckContract.test_T11_audit_wrong_types_and_nulls_are_malformed) (field='generated_ids', value=[3.0]) ... FAIL
  test_T11_audit_wrong_types_and_nulls_are_malformed (__main__.TelemetryCheckContract.test_T11_audit_wrong_types_and_nulls_are_malformed) (field='elapsed_s', value='0') ... FAIL
  test_T11_audit_wrong_types_and_nulls_are_malformed (__main__.TelemetryCheckContract.test_T11_audit_wrong_types_and_nulls_are_malformed) (field='cumulative_s', value=None) ... FAIL
  test_T11_audit_wrong_types_and_nulls_are_malformed (__main__.TelemetryCheckContract.test_T11_audit_wrong_types_and_nulls_are_malformed) (field='t_utc', value=1) ... FAIL
  test_T11_audit_wrong_types_and_nulls_are_malformed (__main__.TelemetryCheckContract.test_T11_audit_wrong_types_and_nulls_are_malformed) (field='run_id', value=None) ... FAIL
test_T11_reader_does_not_open_telemetry_or_use_audit_as_gate (__main__.TelemetryCheckContract.test_T11_reader_does_not_open_telemetry_or_use_audit_as_gate) ... FAIL
test_T8_runner_inert_pristine_stub_never_calls_writer_or_recipe (__main__.TelemetryCheckContract.test_T8_runner_inert_pristine_stub_never_calls_writer_or_recipe) ... FAIL
test_T8_runner_other_verdicts_exit_zero_and_preserve_verdict (__main__.TelemetryCheckContract.test_T8_runner_other_verdicts_exit_zero_and_preserve_verdict) ... 
  test_T8_runner_other_verdicts_exit_zero_and_preserve_verdict (__main__.TelemetryCheckContract.test_T8_runner_other_verdicts_exit_zero_and_preserve_verdict) (verdict='NOT-INERT') ... FAIL
  test_T8_runner_other_verdicts_exit_zero_and_preserve_verdict (__main__.TelemetryCheckContract.test_T8_runner_other_verdicts_exit_zero_and_preserve_verdict) (verdict='NONDETERMINISTIC-BASELINE') ... FAIL
  test_T8_runner_other_verdicts_exit_zero_and_preserve_verdict (__main__.TelemetryCheckContract.test_T8_runner_other_verdicts_exit_zero_and_preserve_verdict) (verdict='INVALID') ... FAIL
test_T8_runner_preflight_refuses_knob_before_output_creation (__main__.TelemetryCheckContract.test_T8_runner_preflight_refuses_knob_before_output_creation) ... FAIL
test_T8_runner_preserves_existing_record (__main__.TelemetryCheckContract.test_T8_runner_preserves_existing_record) ... FAIL
test_T8_runner_records_complete_current_identity_and_strict_roundtrip (__main__.TelemetryCheckContract.test_T8_runner_records_complete_current_identity_and_strict_roundtrip) ... FAIL
test_T8_runner_rejects_namespace_itself_and_nested_subdirectories (__main__.TelemetryCheckContract.test_T8_runner_rejects_namespace_itself_and_nested_subdirectories) ... 
  test_T8_runner_rejects_namespace_itself_and_nested_subdirectories (__main__.TelemetryCheckContract.test_T8_runner_rejects_namespace_itself_and_nested_subdirectories) (out='/private/tmp/c10y_build/roots/tmpbjtwthq3/results/c10y_directdw_telemetry_inertness') ... FAIL
  test_T8_runner_rejects_namespace_itself_and_nested_subdirectories (__main__.TelemetryCheckContract.test_T8_runner_rejects_namespace_itself_and_nested_subdirectories) (out='/private/tmp/c10y_build/roots/tmpbjtwthq3/results/c10y_directdw_telemetry_inertness/one/two') ... FAIL
test_T8_runner_rejects_output_outside_namespace (__main__.TelemetryCheckContract.test_T8_runner_rejects_output_outside_namespace) ... FAIL
test_T8_runner_rejects_relative_output_before_writes (__main__.TelemetryCheckContract.test_T8_runner_rejects_relative_output_before_writes) ... FAIL
test_T8_runner_rejects_symlink_escape (__main__.TelemetryCheckContract.test_T8_runner_rejects_symlink_escape) ... FAIL
test_T8_runner_weight_change_is_invalid_exit_two (__main__.TelemetryCheckContract.test_T8_runner_weight_change_is_invalid_exit_two) ... FAIL
test_every_kind_state_preservation_and_volume (__main__.TelemetryTests.test_every_kind_state_preservation_and_volume) ... FAIL
test_inertness_and_drifting_baseline (__main__.TelemetryTests.test_inertness_and_drifting_baseline) ... FAIL
test_invalid_switches_refused_before_write (__main__.TelemetryTests.test_invalid_switches_refused_before_write) ... 
  test_invalid_switches_refused_before_write (__main__.TelemetryTests.test_invalid_switches_refused_before_write) (value='0') ... FAIL
  test_invalid_switches_refused_before_write (__main__.TelemetryTests.test_invalid_switches_refused_before_write) (value='true') ... FAIL
  test_invalid_switches_refused_before_write (__main__.TelemetryTests.test_invalid_switches_refused_before_write) (value='') ... FAIL
  test_invalid_switches_refused_before_write (__main__.TelemetryTests.test_invalid_switches_refused_before_write) (value=' 1') ... FAIL
  test_invalid_switches_refused_before_write (__main__.TelemetryTests.test_invalid_switches_refused_before_write) (value='1') ... FAIL
test_io_failures_disable_once_and_baseexception_propagates (__main__.TelemetryTests.test_io_failures_disable_once_and_baseexception_propagates) ... FAIL
test_off_has_no_object_or_directory (__main__.TelemetryTests.test_off_has_no_object_or_directory) ... FAIL
test_scorer_ast_and_exact_inputs (__main__.TelemetryTests.test_scorer_ast_and_exact_inputs) ... FAIL

======================================================================
FAIL: test_calibration_forecast_rejects_partial_and_stale (__main__.CalibrationTests.test_calibration_forecast_rejects_partial_and_stale)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 782, in test_calibration_forecast_rejects_partial_and_stale
    self.assertEqual(A.calibration_forecast(path,[])['status'],'UNVERIFIED')
AssertionError: 'UNIMPLEMENTED' != 'UNVERIFIED'
- UNIMPLEMENTED
+ UNVERIFIED


======================================================================
FAIL: test_calibration_forecast_uses_all_repetitions_no_memory_or_inputs (__main__.CalibrationTests.test_calibration_forecast_uses_all_repetitions_no_memory_or_inputs)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 790, in test_calibration_forecast_uses_all_repetitions_no_memory_or_inputs
    self.assertEqual(forecast.get('status'),'READY')
AssertionError: 'UNIMPLEMENTED' != 'READY'
- UNIMPLEMENTED
+ READY


======================================================================
FAIL: test_calibration_go_spend_caps (__main__.CalibrationTests.test_calibration_go_spend_caps)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 738, in test_calibration_go_spend_caps
    self.assertEqual(A.launch_documents('calibration',go,spend,None),7200.)
AssertionError: 0.0 != 7200.0

======================================================================
FAIL: test_calibration_prefix_only_and_required_records (__main__.CalibrationTests.test_calibration_prefix_only_and_required_records)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 759, in test_calibration_prefix_only_and_required_records
    self.assertEqual(record.get('outcome'),'COMPLETE');self.assertEqual(calls,[True])
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'UNIMPLEMENTED' != 'COMPLETE'
- UNIMPLEMENTED
+ COMPLETE


======================================================================
FAIL: test_calibration_reader_and_context_source_refused (__main__.CalibrationTests.test_calibration_reader_and_context_source_refused)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 775, in test_calibration_reader_and_context_source_refused
    with self.assertRaises((ValueError,RuntimeError)): R.load(out)
AssertionError: (<class 'ValueError'>, <class 'RuntimeError'>) not raised

======================================================================
FAIL: test_calibration_telemetry_variables_and_existing_directory_refused (__main__.CalibrationTests.test_calibration_telemetry_variables_and_existing_directory_refused)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 745, in test_calibration_telemetry_variables_and_existing_directory_refused
    with mock.patch.dict(os.environ,{name:''}),self.assertRaises(A.Halt): A.calibrate(out,make_h(),go=go,spend=spend,diagnostic=self.diagnostic)
AssertionError: Halt not raised

======================================================================
FAIL: test_calibration_v4_halt_persists_schedule (__main__.CalibrationTests.test_calibration_v4_halt_persists_schedule)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 769, in test_calibration_v4_halt_persists_schedule
    self.assertEqual(record.get('outcome'),'LAW#3')
AssertionError: 'UNIMPLEMENTED' != 'LAW#3'
- UNIMPLEMENTED
+ LAW#3


======================================================================
FAIL: test_calibration_wrong_namespace_refused (__main__.CalibrationTests.test_calibration_wrong_namespace_refused) (out=PosixPath('/private/tmp/c10y_build/roots/tmpi1vgfog9/results/c10y_directdw'))
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 751, in test_calibration_wrong_namespace_refused
    with self.subTest(out=out),self.assertRaises(A.Halt): A.calibrate(out,make_h(),go=go,spend=spend,diagnostic=self.diagnostic)
AssertionError: Halt not raised

======================================================================
FAIL: test_calibration_wrong_namespace_refused (__main__.CalibrationTests.test_calibration_wrong_namespace_refused) (out=PosixPath('/private/tmp/c10y_build/roots/tmpi1vgfog9/results/c10y_directdw_s1_rerun1'))
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 751, in test_calibration_wrong_namespace_refused
    with self.subTest(out=out),self.assertRaises(A.Halt): A.calibrate(out,make_h(),go=go,spend=spend,diagnostic=self.diagnostic)
AssertionError: Halt not raised

======================================================================
FAIL: test_calibration_wrong_namespace_refused (__main__.CalibrationTests.test_calibration_wrong_namespace_refused) (out=PosixPath('/private/tmp/c10y_build/roots/tmpi1vgfog9/results/c10y_directdw_calib0'))
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 751, in test_calibration_wrong_namespace_refused
    with self.subTest(out=out),self.assertRaises(A.Halt): A.calibrate(out,make_h(),go=go,spend=spend,diagnostic=self.diagnostic)
AssertionError: Halt not raised

======================================================================
FAIL: test_actual_launcher_refuses_missing_calibration_before_import (__main__.IntegrationTests.test_actual_launcher_refuses_missing_calibration_before_import)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 654, in test_actual_launcher_refuses_missing_calibration_before_import
    self.assertNotEqual(code,0);self.assertNotIn('c10e_bandknob',calls)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 0 == 0

======================================================================
FAIL: test_candidate_operations_require_baseline (__main__.IntegrationTests.test_candidate_operations_require_baseline)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 625, in test_candidate_operations_require_baseline
    with self.assertRaises(A.Halt): writer(H.hp,[H.req(H.CANON,H.FICTION[0],'Echo Echo')],H.compute_P(H.hp),[torch.zeros(4,4) for _ in H.hp.layers])
AssertionError: Halt not raised

======================================================================
FAIL: test_native_hanging_worker_deadline_before_and_after_write (__main__.IntegrationTests.test_native_hanging_worker_deadline_before_and_after_write)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 681, in test_native_hanging_worker_deadline_before_and_after_write
    self.assertEqual(os.environ.get('C10Y_ALLOWED_CHILD_TESTS'),'1','prescribed child test authorization pending')
AssertionError: None != '1' : prescribed child test authorization pending

======================================================================
FAIL: test_sequential_capture_matches_original (__main__.IntegrationTests.test_sequential_capture_matches_original)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 601, in test_sequential_capture_matches_original
    self.assertEqual(set(capture),set(hp.layers))
AssertionError: Items in the second set but not the first:
4
5
6
7
8

======================================================================
FAIL: test_stage_runner_artifacts_feed_real_reader_and_halt_before_candidates (__main__.IntegrationTests.test_stage_runner_artifacts_feed_real_reader_and_halt_before_candidates)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 668, in test_stage_runner_artifacts_feed_real_reader_and_halt_before_candidates
    self.assertEqual(result['run']['status'],'HALTED')
AssertionError: 'UNIMPLEMENTED' != 'HALTED'
- UNIMPLEMENTED
+ HALTED


======================================================================
FAIL: test_stored_control_scale1_identity (__main__.IntegrationTests.test_stored_control_scale1_identity)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 631, in test_stored_control_scale1_identity
    self.assertEqual(set(actual),set(H.hp.layers))
AssertionError: Items in the second set but not the first:
4
5
6
7
8

======================================================================
FAIL: test_strict_json_and_immutable_records (__main__.IntegrationTests.test_strict_json_and_immutable_records)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 636, in test_strict_json_and_immutable_records
    self.assertEqual(A.strict_load(path),{'tuple':[1,2],'null':None,'nested':[True,0.1]})
AssertionError: {} != {'tuple': [1, 2], 'null': None, 'nested': [True, 0.1]}
- {}
+ {'nested': [True, 0.1], 'null': None, 'tuple': [1, 2]}

======================================================================
FAIL: test_three_forced_zero_lr_iterations_and_telemetry_trajectory (__main__.IntegrationTests.test_three_forced_zero_lr_iterations_and_telemetry_trajectory)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 615, in test_three_forced_zero_lr_iterations_and_telemetry_trajectory
    self.assertEqual(writer.last_trace['accepted_steps'],3)
AssertionError: -1 != 3

======================================================================
FAIL: test_selftest_root_refusal (__main__.IsolationTests.test_selftest_root_refusal)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 331, in test_selftest_root_refusal
    with self.assertRaises(A.Halt): A.selftest_root(W)
AssertionError: Halt not raised

======================================================================
FAIL: test_context_freeze_and_leakage (__main__.LaunchTests.test_context_freeze_and_leakage)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 498, in test_context_freeze_and_leakage
    self.assertEqual(first['sha256'],hashlib.sha256(path.read_bytes()).hexdigest())
AssertionError: 'UNIMPLEMENTED' != '44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a'
- UNIMPLEMENTED
+ 44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a


======================================================================
FAIL: test_every_inherited_preflight_knob_refused (__main__.LaunchTests.test_every_inherited_preflight_knob_refused) (knob='C10_PROJECTOR')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 465, in test_every_inherited_preflight_knob_refused
    with self.subTest(knob=knob),self.assertRaises(A.Halt): A.preflight({knob:'override'})
AssertionError: Halt not raised

======================================================================
FAIL: test_every_inherited_preflight_knob_refused (__main__.LaunchTests.test_every_inherited_preflight_knob_refused) (knob='N_EDIT')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 465, in test_every_inherited_preflight_knob_refused
    with self.subTest(knob=knob),self.assertRaises(A.Halt): A.preflight({knob:'override'})
AssertionError: Halt not raised

======================================================================
FAIL: test_every_inherited_preflight_knob_refused (__main__.LaunchTests.test_every_inherited_preflight_knob_refused) (knob='C10_SUBJECT_OFFSET')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 465, in test_every_inherited_preflight_knob_refused
    with self.subTest(knob=knob),self.assertRaises(A.Halt): A.preflight({knob:'override'})
AssertionError: Halt not raised

======================================================================
FAIL: test_every_inherited_preflight_knob_refused (__main__.LaunchTests.test_every_inherited_preflight_knob_refused) (knob='C10_CTX_TEMPLATES')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 465, in test_every_inherited_preflight_knob_refused
    with self.subTest(knob=knob),self.assertRaises(A.Halt): A.preflight({knob:'override'})
AssertionError: Halt not raised

======================================================================
FAIL: test_every_inherited_preflight_knob_refused (__main__.LaunchTests.test_every_inherited_preflight_knob_refused) (knob='C10_ARMS')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 465, in test_every_inherited_preflight_knob_refused
    with self.subTest(knob=knob),self.assertRaises(A.Halt): A.preflight({knob:'override'})
AssertionError: Halt not raised

======================================================================
FAIL: test_every_inherited_preflight_knob_refused (__main__.LaunchTests.test_every_inherited_preflight_knob_refused) (knob='C10_KEY_LOCUS')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 465, in test_every_inherited_preflight_knob_refused
    with self.subTest(knob=knob),self.assertRaises(A.Halt): A.preflight({knob:'override'})
AssertionError: Halt not raised

======================================================================
FAIL: test_every_inherited_preflight_knob_refused (__main__.LaunchTests.test_every_inherited_preflight_knob_refused) (knob='HP_CANDIDATE')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 465, in test_every_inherited_preflight_knob_refused
    with self.subTest(knob=knob),self.assertRaises(A.Halt): A.preflight({knob:'override'})
AssertionError: Halt not raised

======================================================================
FAIL: test_every_inherited_preflight_knob_refused (__main__.LaunchTests.test_every_inherited_preflight_knob_refused) (knob='C10_RECIPES')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 465, in test_every_inherited_preflight_knob_refused
    with self.subTest(knob=knob),self.assertRaises(A.Halt): A.preflight({knob:'override'})
AssertionError: Halt not raised

======================================================================
FAIL: test_every_inherited_preflight_knob_refused (__main__.LaunchTests.test_every_inherited_preflight_knob_refused) (knob='CANDIDATE_NAME')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 465, in test_every_inherited_preflight_knob_refused
    with self.subTest(knob=knob),self.assertRaises(A.Halt): A.preflight({knob:'override'})
AssertionError: Halt not raised

======================================================================
FAIL: test_every_inherited_preflight_knob_refused (__main__.LaunchTests.test_every_inherited_preflight_knob_refused) (knob='OUT')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 465, in test_every_inherited_preflight_knob_refused
    with self.subTest(knob=knob),self.assertRaises(A.Halt): A.preflight({knob:'override'})
AssertionError: Halt not raised

======================================================================
FAIL: test_every_inherited_preflight_knob_refused (__main__.LaunchTests.test_every_inherited_preflight_knob_refused) (knob='DECISION_ID')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 465, in test_every_inherited_preflight_knob_refused
    with self.subTest(knob=knob),self.assertRaises(A.Halt): A.preflight({knob:'override'})
AssertionError: Halt not raised

======================================================================
FAIL: test_every_inherited_preflight_knob_refused (__main__.LaunchTests.test_every_inherited_preflight_knob_refused) (knob='PREREG')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 465, in test_every_inherited_preflight_knob_refused
    with self.subTest(knob=knob),self.assertRaises(A.Halt): A.preflight({knob:'override'})
AssertionError: Halt not raised

======================================================================
FAIL: test_every_inherited_preflight_knob_refused (__main__.LaunchTests.test_every_inherited_preflight_knob_refused) (knob='RUN_LABEL')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 465, in test_every_inherited_preflight_knob_refused
    with self.subTest(knob=knob),self.assertRaises(A.Halt): A.preflight({knob:'override'})
AssertionError: Halt not raised

======================================================================
FAIL: test_every_inherited_preflight_knob_refused (__main__.LaunchTests.test_every_inherited_preflight_knob_refused) (knob='LLMDB_DEVICE')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 465, in test_every_inherited_preflight_knob_refused
    with self.subTest(knob=knob),self.assertRaises(A.Halt): A.preflight({knob:'override'})
AssertionError: Halt not raised

======================================================================
FAIL: test_every_inherited_preflight_knob_refused (__main__.LaunchTests.test_every_inherited_preflight_knob_refused) (name='MODEL_ID')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 467, in test_every_inherited_preflight_knob_refused
    with self.subTest(name=name),self.assertRaises(A.Halt): A.preflight({name:'mismatch'})
AssertionError: Halt not raised

======================================================================
FAIL: test_every_inherited_preflight_knob_refused (__main__.LaunchTests.test_every_inherited_preflight_knob_refused) (name='MODEL_REV')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 467, in test_every_inherited_preflight_knob_refused
    with self.subTest(name=name),self.assertRaises(A.Halt): A.preflight({name:'mismatch'})
AssertionError: Halt not raised

======================================================================
FAIL: test_forecast_unverified_and_cap (__main__.LaunchTests.test_forecast_unverified_and_cap)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 482, in test_forecast_unverified_and_cap
    self.assertEqual(A.budget_gate(forecast(7200.),7200.)['status'],'READY')
AssertionError: 'UNIMPLEMENTED' != 'READY'
- UNIMPLEMENTED
+ READY


======================================================================
FAIL: test_go_spend_and_stage_eligibility (__main__.LaunchTests.test_go_spend_and_stage_eligibility)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 471, in test_go_spend_and_stage_eligibility
    with self.assertRaises(A.Halt): A.launch_documents(2,go,None,None)
AssertionError: Halt not raised

======================================================================
FAIL: test_memory_boundaries (__main__.LaunchTests.test_memory_boundaries)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 490, in test_memory_boundaries
    self.assertEqual(A.memory_gate(valid),valid)
AssertionError: {} != {'current_bytes': 0, 'driver_bytes': 34359[58 chars]4592}
- {}
+ {'available_bytes': 8589934592,
+  'current_bytes': 0,
+  'driver_bytes': 34359738368,
+  'rss_bytes': 8589934592}

======================================================================
FAIL: test_schedule_halt_survives_new_directory (__main__.LaunchTests.test_schedule_halt_survives_new_directory)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 518, in test_schedule_halt_survives_new_directory
    with self.assertRaises(A.Halt): A.refuse_schedule_halt(self.root)
AssertionError: Halt not raised

======================================================================
FAIL: test_step_projection_reserves_readout (__main__.LaunchTests.test_step_projection_reserves_readout)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 522, in test_step_projection_reserves_readout
    with self.assertRaises(A.Halt): budget.project(30.,write_complete=False)
AssertionError: Halt not raised

======================================================================
FAIL: test_wrapper_delegate_dynamic_and_arm_restore (__main__.LaunchTests.test_wrapper_delegate_dynamic_and_arm_restore)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 509, in test_wrapper_delegate_dynamic_and_arm_restore
    self.assertEqual(wrapper(H.hp,[],[],[]),{'original':True})
AssertionError: {} != {'original': True}
- {}
+ {'original': True}

======================================================================
FAIL: test_anchor_zero_denominator (__main__.NumericTests.test_anchor_zero_denominator)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 366, in test_anchor_zero_denominator
    self.assertEqual(float(A.anchor_loss(zeros,zeros,torch.zeros(2,4))),0.)
AssertionError: 1.0 != 0.0

======================================================================
FAIL: test_capture_factorization (__main__.NumericTests.test_capture_factorization)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 362, in test_capture_factorization
    self.assertLess(A.relative_distance(got['R']@got['B'],reference),1e-6)
AssertionError: 1.0 not less than 1e-06

======================================================================
FAIL: test_control_boundaries (__main__.NumericTests.test_control_boundaries) (error=0.01)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 378, in test_control_boundaries
    with self.subTest(error=error): self.assertEqual(A.control_match('NM',1+error,1,{4:1.0},{4:1.0},{4:0.999}),expected)
                                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: False != True

======================================================================
FAIL: test_control_boundaries (__main__.NumericTests.test_control_boundaries) (candidate=1.01)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 380, in test_control_boundaries
    with self.subTest(candidate=candidate): self.assertEqual(A.control_match('ENV',candidate,1,{4:candidate},{4:1.0},{4:0.999}),expected)
                                            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: False != True

======================================================================
FAIL: test_full_size_float64_reductions (__main__.NumericTests.test_full_size_float64_reductions)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 340, in test_full_size_float64_reductions
    self.assertEqual(A.cosine(x,x),1.0)
AssertionError: 0.0 != 1.0

======================================================================
FAIL: test_gram_norm_dense_reference (__main__.NumericTests.test_gram_norm_dense_reference)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 352, in test_gram_norm_dense_reference
    self.assertAlmostEqual(A.gram_norm(a,b),reference,delta=reference*1e-12)
AssertionError: 0.0 != 8216.622961334953 within 8.216622961334953e-09 delta (8216.622961334953 difference)

======================================================================
FAIL: test_mps_double_refused (__main__.NumericTests.test_mps_double_refused)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 355, in test_mps_double_refused
    with self.assertRaises(A.Halt): A.assert_no_mps_double(tensor)
AssertionError: Halt not raised

======================================================================
FAIL: test_null_share_boundaries (__main__.NumericTests.test_null_share_boundaries)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 386, in test_null_share_boundaries
    self.assertAlmostEqual(A.null_share(x,P),share,delta=1e-14)
AssertionError: 0.0 != 0.999 within 1e-14 delta (0.999 difference)

======================================================================
FAIL: test_size_scales_and_stored_arithmetic (__main__.NumericTests.test_size_scales_and_stored_arithmetic)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 370, in test_size_scales_and_stored_arithmetic
    self.assertEqual(A.size_scales(a,b),{'NM':0.5,'ENV':0.5})
AssertionError: {'NM': None, 'ENV': None} != {'NM': 0.5, 'ENV': 0.5}
- {'ENV': None, 'NM': None}
+ {'ENV': 0.5, 'NM': 0.5}

======================================================================
FAIL: test_effective_weight_and_routing_gradient (__main__.OptimizerTests.test_effective_weight_and_routing_gradient)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 399, in test_effective_weight_and_routing_gradient
    self.assertTrue(torch.equal(actual,expected))
AssertionError: False is not true

======================================================================
FAIL: test_kl_coefficient_once (__main__.OptimizerTests.test_kl_coefficient_once)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 404, in test_kl_coefficient_once
    self.assertEqual(float(A.total_loss(torch.tensor(2.),torch.tensor(8.))),2.5)
AssertionError: 2.0 != 2.5

======================================================================
FAIL: test_loss_scale_transaction (__main__.OptimizerTests.test_loss_scale_transaction)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 436, in test_loss_scale_transaction
    self.assertEqual(result['retries'],1)
AssertionError: -1 != 1

======================================================================
FAIL: test_microbatch_request_weighting (__main__.OptimizerTests.test_microbatch_request_weighting)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 418, in test_microbatch_request_weighting
    self.assertEqual(groups,[list(range(i,i+6)) for i in range(0,24,6)])
AssertionError: Lists differ: [] != [[0, 1, 2, 3, 4, 5], [6, 7, 8, 9, 10, 11],[47 chars] 23]]

Second list contains 4 additional elements.
First extra element 0:
[0, 1, 2, 3, 4, 5]

- []
+ [[0, 1, 2, 3, 4, 5],
+  [6, 7, 8, 9, 10, 11],
+  [12, 13, 14, 15, 16, 17],
+  [18, 19, 20, 21, 22, 23]]

======================================================================
FAIL: test_request_batch_and_target_only_objective (__main__.OptimizerTests.test_request_batch_and_target_only_objective)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 408, in test_request_batch_and_target_only_objective
    self.assertEqual(batch['rewriting_targets'].shape[0],6)
AssertionError: 0 != 6

======================================================================
FAIL: test_sixth_overflow_halts_without_mutation (__main__.OptimizerTests.test_sixth_overflow_halts_without_mutation)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 444, in test_sixth_overflow_halts_without_mutation
    with self.assertRaises(A.Halt):
AssertionError: Halt not raised

======================================================================
FAIL: test_stopping_boundaries (__main__.OptimizerTests.test_stopping_boundaries)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 423, in test_stopping_boundaries
    self.assertTrue(A.threshold_stop('e2e',0.049999))
AssertionError: False is not true

======================================================================
FAIL: test_unknown_hooks_preserved (__main__.OptimizerTests.test_unknown_hooks_preserved)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 453, in test_unknown_hooks_preserved
    self.assertNotEqual(A.hook_snapshot(H.model),before)
AssertionError: {} == {}

======================================================================
FAIL: test_anchor_comparison_does_not_require_bz_sized_gain (__main__.ReaderAttributionTests.test_anchor_comparison_does_not_require_bz_sized_gain)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1757, in test_anchor_comparison_does_not_require_bz_sized_gain
    self.result(record, "PARTIAL", include=("ANCHOR-NOT-EXCLUDED",) if n == 22 else (), exclude=() if n == 22 else ("ANCHOR-NOT-EXCLUDED",))
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'PARTIAL'
- UNIMPLEMENTED
+ PARTIAL


======================================================================
FAIL: test_anchor_missing_invalid_and_unfit_untested (__main__.ReaderAttributionTests.test_anchor_missing_invalid_and_unfit_untested)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1751, in test_anchor_missing_invalid_and_unfit_untested
    self.result(record, "PARTIAL", include=("ANCHOR-UNTESTED",), advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'PARTIAL'
- UNIMPLEMENTED
+ PARTIAL


======================================================================
FAIL: test_anchor_sham_descriptor_windows_not_fit_or_validity (__main__.ReaderAttributionTests.test_anchor_sham_descriptor_windows_not_fit_or_validity)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1765, in test_anchor_sham_descriptor_windows_not_fit_or_validity
    result = self.result(record, "NULL", recipe="B-z")
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'NULL'
- UNIMPLEMENTED
+ NULL


======================================================================
FAIL: test_control_positive_requires_envelope_gain_fit_locality_and_validity (__main__.ReaderAttributionTests.test_control_positive_requires_envelope_gain_fit_locality_and_validity)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1733, in test_control_positive_requires_envelope_gain_fit_locality_and_validity
    self.result(record, "PARTIAL", include=("SIZE-UNTESTED" if failure == "invalid" else "SIZE-NOT-EXCLUDED",), advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'PARTIAL'
- UNIMPLEMENTED
+ PARTIAL


======================================================================
FAIL: test_hy1_credit_requires_both_processes_attributed (__main__.ReaderAttributionTests.test_hy1_credit_requires_both_processes_attributed)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1776, in test_hy1_credit_requires_both_processes_attributed
    result = self.pair(p1, p2, "LEAD", advance=True)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1128, in pair
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'LEAD'
- UNIMPLEMENTED
+ LEAD


======================================================================
FAIL: test_neff_minimum_and_anchor_gap_nine_ten (__main__.ReaderAttributionTests.test_neff_minimum_and_anchor_gap_nine_ten)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1739, in test_neff_minimum_and_anchor_gap_nine_ten
    result = self.result(record, "LEAD", include=expected, exclude=("ANCHOR-NOT-EXCLUDED",) if effective == 23 else ())
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'LEAD'
- UNIMPLEMENTED
+ LEAD


======================================================================
FAIL: test_no_downscale_controls_required_at_actual_ratio_one (__main__.ReaderAttributionTests.test_no_downscale_controls_required_at_actual_ratio_one)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1676, in test_no_downscale_controls_required_at_actual_ratio_one
    self.result(record, "PARTIAL", exclude=("SIZE-UNTESTED", "SIZE-NOT-EXCLUDED"))
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'PARTIAL'
- UNIMPLEMENTED
+ PARTIAL


======================================================================
FAIL: test_size_control_matching_and_direction_boundaries (__main__.ReaderAttributionTests.test_size_control_matching_and_direction_boundaries)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1716, in test_size_control_matching_and_direction_boundaries
    self.result(record, "PARTIAL", include=() if value == boundary else ("SIZE-UNTESTED",), exclude=("SIZE-UNTESTED",) if value == boundary else ())
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'PARTIAL'
- UNIMPLEMENTED
+ PARTIAL


======================================================================
FAIL: test_total_and_per_layer_growth_trigger_independent_controls (__main__.ReaderAttributionTests.test_total_and_per_layer_growth_trigger_independent_controls)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1691, in test_total_and_per_layer_growth_trigger_independent_controls
    self.result(record, "PARTIAL", include=("SIZE-UNTESTED",), advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'PARTIAL'
- UNIMPLEMENTED
+ PARTIAL


======================================================================
FAIL: test_zero_reference_size_normalisation_conservative_provisional (__main__.ReaderAttributionTests.test_zero_reference_size_normalisation_conservative_provisional)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1686, in test_zero_reference_size_normalisation_conservative_provisional
    self.result(record, "INVALID-SIZE-NORMALISATION", advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID-SIZE-NORMALISATION'
- UNIMPLEMENTED
+ INVALID-SIZE-NORMALISATION


======================================================================
FAIL: test_cross_shared_hin_and_telemetry_pair_identity (__main__.ReaderCrossProcessTests.test_cross_shared_hin_and_telemetry_pair_identity)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1880, in test_cross_shared_hin_and_telemetry_pair_identity
    self.pair(p1, p2, "PARTIAL", include=("NOT-REPRODUCIBLE",), advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1128, in pair
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'PARTIAL'
- UNIMPLEMENTED
+ PARTIAL


======================================================================
FAIL: test_r1_cosine_and_distance_every_layer_boundaries (__main__.ReaderCrossProcessTests.test_r1_cosine_and_distance_every_layer_boundaries)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1824, in test_r1_cosine_and_distance_every_layer_boundaries
    self.pair(p1, p2, "PARTIAL", repro, include=() if value == inside else ("NOT-REPRODUCIBLE",), exclude=("NOT-REPRODUCIBLE",) if value == inside else (), advance=value == inside)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1128, in pair
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'PARTIAL'
- UNIMPLEMENTED
+ PARTIAL


======================================================================
FAIL: test_r1_required_controls_and_all_arms_independent (__main__.ReaderCrossProcessTests.test_r1_required_controls_and_all_arms_independent)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1847, in test_r1_required_controls_and_all_arms_independent
    self.pair(p1, p2, "PARTIAL", repro, include=("NOT-REPRODUCIBLE",), advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1128, in pair
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'PARTIAL'
- UNIMPLEMENTED
+ PARTIAL


======================================================================
FAIL: test_r1_zero_norm_rules_and_baseline_instrument (__main__.ReaderCrossProcessTests.test_r1_zero_norm_rules_and_baseline_instrument)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1834, in test_r1_zero_norm_rules_and_baseline_instrument
    self.pair(p1, p2, "PARTIAL", repro, include=() if success else ("NOT-REPRODUCIBLE",), exclude=("NOT-REPRODUCIBLE",) if success else ())
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1128, in pair
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'PARTIAL'
- UNIMPLEMENTED
+ PARTIAL


======================================================================
FAIL: test_r2_count_spread_five_six (__main__.ReaderCrossProcessTests.test_r2_count_spread_five_six)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1855, in test_r2_count_spread_five_six
    self.pair(p1, p2, "PARTIAL", include=() if spread == 5 else ("NOT-REPRODUCIBLE",), exclude=("NOT-REPRODUCIBLE",) if spread == 5 else ())
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1128, in pair
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'PARTIAL'
- UNIMPLEMENTED
+ PARTIAL


======================================================================
FAIL: test_r3_incorrect_strings_do_not_count_as_disagreement (__main__.ReaderCrossProcessTests.test_r3_incorrect_strings_do_not_count_as_disagreement)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1870, in test_r3_incorrect_strings_do_not_count_as_disagreement
    self.pair(p1, p2, "PARTIAL", exclude=("NOT-REPRODUCIBLE",))
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1128, in pair
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'PARTIAL'
- UNIMPLEMENTED
+ PARTIAL


======================================================================
FAIL: test_r3_keyed_boolean_disagreement_da_plus_three_four (__main__.ReaderCrossProcessTests.test_r3_keyed_boolean_disagreement_da_plus_three_four)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1862, in test_r3_keyed_boolean_disagreement_da_plus_three_four
    self.pair(p1, p2, "PARTIAL", exclude=("NOT-REPRODUCIBLE",))
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1128, in pair
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'PARTIAL'
- UNIMPLEMENTED
+ PARTIAL


======================================================================
FAIL: test_regenerated_target_hashes_need_not_match_shared_hin (__main__.ReaderCrossProcessTests.test_regenerated_target_hashes_need_not_match_shared_hin)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1887, in test_regenerated_target_hashes_need_not_match_shared_hin
    self.pair(p1, p2, "PARTIAL", exclude=("NOT-REPRODUCIBLE",))
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1128, in pair
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'PARTIAL'
- UNIMPLEMENTED
+ PARTIAL


======================================================================
FAIL: test_x1_not_run_halted_and_incomplete_never_fabricated_null (__main__.ReaderCrossProcessTests.test_x1_not_run_halted_and_incomplete_never_fabricated_null)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1787, in test_x1_not_run_halted_and_incomplete_never_fabricated_null
    self.pair(p1, None, "PARTIAL", include=("SINGLE-PROCESS",), advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1128, in pair
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'PARTIAL'
- UNIMPLEMENTED
+ PARTIAL


======================================================================
FAIL: test_x2_identical_labels_and_union_qualifiers (__main__.ReaderCrossProcessTests.test_x2_identical_labels_and_union_qualifiers)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1797, in test_x2_identical_labels_and_union_qualifiers
    self.pair(p1, p2, "PARTIAL", advance=True)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1128, in pair
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'PARTIAL'
- UNIMPLEMENTED
+ PARTIAL


======================================================================
FAIL: test_x3_mixed_labels_store_actual_counts (__main__.ReaderCrossProcessTests.test_x3_mixed_labels_store_actual_counts)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1805, in test_x3_mixed_labels_store_actual_counts
    result = self.pair(p1, p2, "MIXED-NOT-REPLICATED", exclude=("NOT-REPRODUCIBLE",), advance=False)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1128, in pair
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'MIXED-NOT-REPLICATED'
- UNIMPLEMENTED
+ MIXED-NOT-REPLICATED


======================================================================
FAIL: test_fit_e2e_minimum_canonical_and_every_stop (__main__.ReaderFitAndScreenTests.test_fit_e2e_minimum_canonical_and_every_stop)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1496, in test_fit_e2e_minimum_canonical_and_every_stop
    self.result(record, expected)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'SCREEN-PASS'
- UNIMPLEMENTED
+ SCREEN-PASS


======================================================================
FAIL: test_fit_per_required_arm_and_apply_stored (__main__.ReaderFitAndScreenTests.test_fit_per_required_arm_and_apply_stored)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1502, in test_fit_per_required_arm_and_apply_stored
    self.result(record, "UNDERFIT", advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'UNDERFIT'
- UNIMPLEMENTED
+ UNDERFIT


======================================================================
FAIL: test_fit_requires_full_merged_matrix (__main__.ReaderFitAndScreenTests.test_fit_requires_full_merged_matrix)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1519, in test_fit_requires_full_merged_matrix
    self.result(record, "INVALID", advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_fit_z_mean_and_maximum_boundaries (__main__.ReaderFitAndScreenTests.test_fit_z_mean_and_maximum_boundaries)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1528, in test_fit_z_mean_and_maximum_boundaries
    self.result(record, expected, recipe="B-z")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'NULL'
- UNIMPLEMENTED
+ NULL


======================================================================
FAIL: test_fit_z_zero_denominator_named_rule (__main__.ReaderFitAndScreenTests.test_fit_z_zero_denominator_named_rule)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1536, in test_fit_z_zero_denominator_named_rule
    self.result(record, "NULL", recipe="B-z")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'NULL'
- UNIMPLEMENTED
+ NULL


======================================================================
FAIL: test_s1_named_halts_without_screen_label (__main__.ReaderFitAndScreenTests.test_s1_named_halts_without_screen_label)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1544, in test_s1_named_halts_without_screen_label
    self.result(record, "HALTED", advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'HALTED'
- UNIMPLEMENTED
+ HALTED


======================================================================
FAIL: test_s2_s3_budget_write_boundary (__main__.ReaderFitAndScreenTests.test_s2_s3_budget_write_boundary)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1551, in test_s2_s3_budget_write_boundary
    self.result(record, status, advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'HALTED-BUDGET'
- UNIMPLEMENTED
+ HALTED-BUDGET


======================================================================
FAIL: test_s4_fit_precedes_high_count_locality_and_size (__main__.ReaderFitAndScreenTests.test_s4_fit_precedes_high_count_locality_and_size)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1568, in test_s4_fit_precedes_high_count_locality_and_size
    self.result(record, "SCREEN-UNDERFIT", advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'SCREEN-UNDERFIT'
- UNIMPLEMENTED
+ SCREEN-UNDERFIT


======================================================================
FAIL: test_s5_s7_envelope_and_gain_boundaries (__main__.ReaderFitAndScreenTests.test_s5_s7_envelope_and_gain_boundaries)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1575, in test_s5_s7_envelope_and_gain_boundaries
    self.result(record, label)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'SCREEN-NULL'
- UNIMPLEMENTED
+ SCREEN-NULL


======================================================================
FAIL: test_s6_size_boundary_and_null_first_match (__main__.ReaderFitAndScreenTests.test_s6_size_boundary_and_null_first_match)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1581, in test_s6_size_boundary_and_null_first_match
    self.result(record, "SCREEN-PASS" if ratio == 1.5 else "SCREEN-NOT-ADVANCED")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'SCREEN-PASS'
- UNIMPLEMENTED
+ SCREEN-PASS


======================================================================
FAIL: test_stage1_recorded_projection_exactly_120_minutes_fits (__main__.ReaderFitAndScreenTests.test_stage1_recorded_projection_exactly_120_minutes_fits)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1557, in test_stage1_recorded_projection_exactly_120_minutes_fits
    self.result(record, "SCREEN-PASS")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'SCREEN-PASS'
- UNIMPLEMENTED
+ SCREEN-PASS


======================================================================
FAIL: test_load_calibration_directory_refused_before_read (__main__.ReaderLoadTests.test_load_calibration_directory_refused_before_read)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2044, in test_load_calibration_directory_refused_before_read
    with self.assertRaises((ValueError, RuntimeError)):
AssertionError: (<class 'ValueError'>, <class 'RuntimeError'>) not raised

======================================================================
FAIL: test_load_does_not_read_telemetry (__main__.ReaderLoadTests.test_load_does_not_read_telemetry)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2004, in test_load_does_not_read_telemetry
    self.result(loaded, "HALTED", advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'HALTED'
- UNIMPLEMENTED
+ HALTED


======================================================================
FAIL: test_load_later_self_contained_record_uses_own_outcome (__main__.ReaderLoadTests.test_load_later_self_contained_record_uses_own_outcome)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2013, in test_load_later_self_contained_record_uses_own_outcome
    self.result(loaded, "INCOMPLETE-BUDGET", advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INCOMPLETE-BUDGET'
- UNIMPLEMENTED
+ INCOMPLETE-BUDGET


======================================================================
FAIL: test_load_saved_halt_first_with_missing_science_artifacts (__main__.ReaderLoadTests.test_load_saved_halt_first_with_missing_science_artifacts)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1994, in test_load_saved_halt_first_with_missing_science_artifacts
    self.result(loaded, "HALTED-BUDGET", advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'HALTED-BUDGET'
- UNIMPLEMENTED
+ HALTED-BUDGET


======================================================================
FAIL: test_load_strict_json_nonfinite_refused (__main__.ReaderLoadTests.test_load_strict_json_nonfinite_refused)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2019, in test_load_strict_json_nonfinite_refused
    with self.assertRaises((ValueError, RuntimeError)):
AssertionError: (<class 'ValueError'>, <class 'RuntimeError'>) not raised

======================================================================
FAIL: test_existing_arm_missing_metric_is_v13_invalid (__main__.ReaderOrderTests.test_existing_arm_missing_metric_is_v13_invalid)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1195, in test_existing_arm_missing_metric_is_v13_invalid
    self.result(record, "INVALID", advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_missing_comparators_qualify_without_incomplete (__main__.ReaderOrderTests.test_missing_comparators_qualify_without_incomplete)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1187, in test_missing_comparators_qualify_without_incomplete
    self.result(record, "LEAD", include=("SIZE-UNTESTED",), advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'LEAD'
- UNIMPLEMENTED
+ LEAD


======================================================================
FAIL: test_own_record_and_v5_missing_precede_validity_and_fit (__main__.ReaderOrderTests.test_own_record_and_v5_missing_precede_validity_and_fit) (missing='recipe')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1162, in test_own_record_and_v5_missing_precede_validity_and_fit
    self.result(record, "INCOMPLETE", advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INCOMPLETE'
- UNIMPLEMENTED
+ INCOMPLETE


======================================================================
FAIL: test_own_record_and_v5_missing_precede_validity_and_fit (__main__.ReaderOrderTests.test_own_record_and_v5_missing_precede_validity_and_fit) (missing='A1_single')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1162, in test_own_record_and_v5_missing_precede_validity_and_fit
    self.result(record, "INCOMPLETE", advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INCOMPLETE'
- UNIMPLEMENTED
+ INCOMPLETE


======================================================================
FAIL: test_own_record_and_v5_missing_precede_validity_and_fit (__main__.ReaderOrderTests.test_own_record_and_v5_missing_precede_validity_and_fit) (missing='A2_coherent2')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1162, in test_own_record_and_v5_missing_precede_validity_and_fit
    self.result(record, "INCOMPLETE", advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INCOMPLETE'
- UNIMPLEMENTED
+ INCOMPLETE


======================================================================
FAIL: test_own_record_and_v5_missing_precede_validity_and_fit (__main__.ReaderOrderTests.test_own_record_and_v5_missing_precede_validity_and_fit) (missing='A7_coined_coined')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1162, in test_own_record_and_v5_missing_precede_validity_and_fit
    self.result(record, "INCOMPLETE", advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INCOMPLETE'
- UNIMPLEMENTED
+ INCOMPLETE


======================================================================
FAIL: test_recorded_halt_invalid_and_budget_first (__main__.ReaderOrderTests.test_recorded_halt_invalid_and_budget_first) (status='HALTED')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1150, in test_recorded_halt_invalid_and_budget_first
    self.result(record, status, advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'HALTED'
- UNIMPLEMENTED
+ HALTED


======================================================================
FAIL: test_recorded_halt_invalid_and_budget_first (__main__.ReaderOrderTests.test_recorded_halt_invalid_and_budget_first) (status='INVALID')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1150, in test_recorded_halt_invalid_and_budget_first
    self.result(record, status, advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_recorded_halt_invalid_and_budget_first (__main__.ReaderOrderTests.test_recorded_halt_invalid_and_budget_first) (status='HALTED-BUDGET')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1150, in test_recorded_halt_invalid_and_budget_first
    self.result(record, status, advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'HALTED-BUDGET'
- UNIMPLEMENTED
+ HALTED-BUDGET


======================================================================
FAIL: test_recorded_halt_invalid_and_budget_first (__main__.ReaderOrderTests.test_recorded_halt_invalid_and_budget_first) (status='INCOMPLETE-BUDGET')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1150, in test_recorded_halt_invalid_and_budget_first
    self.result(record, status, advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INCOMPLETE-BUDGET'
- UNIMPLEMENTED
+ INCOMPLETE-BUDGET


======================================================================
FAIL: test_source_and_prereg_identity_refused (__main__.ReaderOrderTests.test_source_and_prereg_identity_refused) (field='prereg')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1207, in test_source_and_prereg_identity_refused
    self.result(record, "INVALID", advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_source_and_prereg_identity_refused (__main__.ReaderOrderTests.test_source_and_prereg_identity_refused) (field='source')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1207, in test_source_and_prereg_identity_refused
    self.result(record, "INVALID", advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_source_and_prereg_identity_refused (__main__.ReaderOrderTests.test_source_and_prereg_identity_refused) (field='input')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1207, in test_source_and_prereg_identity_refused
    self.result(record, "INVALID", advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_stage1_not_run_controls_and_later_records_not_required (__main__.ReaderOrderTests.test_stage1_not_run_controls_and_later_records_not_required)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1178, in test_stage1_not_run_controls_and_later_records_not_required
    self.result(record, "SCREEN-PASS", exclude=("SIZE-UNTESTED", "ANCHOR-UNTESTED"))
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'SCREEN-PASS'
- UNIMPLEMENTED
+ SCREEN-PASS


======================================================================
FAIL: test_validity_precedes_fit_and_fit_precedes_counts (__main__.ReaderOrderTests.test_validity_precedes_fit_and_fit_precedes_counts)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1170, in test_validity_precedes_fit_and_fit_precedes_counts
    self.result(record, "INVALID", advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_g1_g2_each_frame_both_sides (__main__.ReaderProcessLocalityTests.test_g1_g2_each_frame_both_sides) (axis='L1', excess=1)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1618, in test_g1_g2_each_frame_both_sides
    self.result(record, "PARTIAL" if excess == 1 else "TRADEOFF")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'PARTIAL'
- UNIMPLEMENTED
+ PARTIAL


======================================================================
FAIL: test_g1_g2_each_frame_both_sides (__main__.ReaderProcessLocalityTests.test_g1_g2_each_frame_both_sides) (axis='L1', excess=2)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1618, in test_g1_g2_each_frame_both_sides
    self.result(record, "PARTIAL" if excess == 1 else "TRADEOFF")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'TRADEOFF'
- UNIMPLEMENTED
+ TRADEOFF


======================================================================
FAIL: test_g1_g2_each_frame_both_sides (__main__.ReaderProcessLocalityTests.test_g1_g2_each_frame_both_sides) (axis='CANON', excess=1)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1618, in test_g1_g2_each_frame_both_sides
    self.result(record, "PARTIAL" if excess == 1 else "TRADEOFF")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'PARTIAL'
- UNIMPLEMENTED
+ PARTIAL


======================================================================
FAIL: test_g1_g2_each_frame_both_sides (__main__.ReaderProcessLocalityTests.test_g1_g2_each_frame_both_sides) (axis='CANON', excess=2)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1618, in test_g1_g2_each_frame_both_sides
    self.result(record, "PARTIAL" if excess == 1 else "TRADEOFF")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'TRADEOFF'
- UNIMPLEMENTED
+ TRADEOFF


======================================================================
FAIL: test_g1_g2_each_frame_both_sides (__main__.ReaderProcessLocalityTests.test_g1_g2_each_frame_both_sides) (axis='frame0', excess=1)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1618, in test_g1_g2_each_frame_both_sides
    self.result(record, "PARTIAL" if excess == 1 else "TRADEOFF")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'PARTIAL'
- UNIMPLEMENTED
+ PARTIAL


======================================================================
FAIL: test_g1_g2_each_frame_both_sides (__main__.ReaderProcessLocalityTests.test_g1_g2_each_frame_both_sides) (axis='frame0', excess=2)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1618, in test_g1_g2_each_frame_both_sides
    self.result(record, "PARTIAL" if excess == 1 else "TRADEOFF")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'TRADEOFF'
- UNIMPLEMENTED
+ TRADEOFF


======================================================================
FAIL: test_g1_g2_each_frame_both_sides (__main__.ReaderProcessLocalityTests.test_g1_g2_each_frame_both_sides) (axis='frame1', excess=1)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1618, in test_g1_g2_each_frame_both_sides
    self.result(record, "PARTIAL" if excess == 1 else "TRADEOFF")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'PARTIAL'
- UNIMPLEMENTED
+ PARTIAL


======================================================================
FAIL: test_g1_g2_each_frame_both_sides (__main__.ReaderProcessLocalityTests.test_g1_g2_each_frame_both_sides) (axis='frame1', excess=2)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1618, in test_g1_g2_each_frame_both_sides
    self.result(record, "PARTIAL" if excess == 1 else "TRADEOFF")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'TRADEOFF'
- UNIMPLEMENTED
+ TRADEOFF


======================================================================
FAIL: test_g1_g2_each_frame_both_sides (__main__.ReaderProcessLocalityTests.test_g1_g2_each_frame_both_sides) (axis='frame2', excess=1)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1618, in test_g1_g2_each_frame_both_sides
    self.result(record, "PARTIAL" if excess == 1 else "TRADEOFF")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'PARTIAL'
- UNIMPLEMENTED
+ PARTIAL


======================================================================
FAIL: test_g1_g2_each_frame_both_sides (__main__.ReaderProcessLocalityTests.test_g1_g2_each_frame_both_sides) (axis='frame2', excess=2)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1618, in test_g1_g2_each_frame_both_sides
    self.result(record, "PARTIAL" if excess == 1 else "TRADEOFF")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'TRADEOFF'
- UNIMPLEMENTED
+ TRADEOFF


======================================================================
FAIL: test_g1_g2_each_frame_both_sides (__main__.ReaderProcessLocalityTests.test_g1_g2_each_frame_both_sides) (axis='frame3', excess=1)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1618, in test_g1_g2_each_frame_both_sides
    self.result(record, "PARTIAL" if excess == 1 else "TRADEOFF")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'PARTIAL'
- UNIMPLEMENTED
+ PARTIAL


======================================================================
FAIL: test_g1_g2_each_frame_both_sides (__main__.ReaderProcessLocalityTests.test_g1_g2_each_frame_both_sides) (axis='frame3', excess=2)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1618, in test_g1_g2_each_frame_both_sides
    self.result(record, "PARTIAL" if excess == 1 else "TRADEOFF")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'TRADEOFF'
- UNIMPLEMENTED
+ TRADEOFF


======================================================================
FAIL: test_g1_g2_each_frame_both_sides (__main__.ReaderProcessLocalityTests.test_g1_g2_each_frame_both_sides) (axis='frame4', excess=1)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1618, in test_g1_g2_each_frame_both_sides
    self.result(record, "PARTIAL" if excess == 1 else "TRADEOFF")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'PARTIAL'
- UNIMPLEMENTED
+ PARTIAL


======================================================================
FAIL: test_g1_g2_each_frame_both_sides (__main__.ReaderProcessLocalityTests.test_g1_g2_each_frame_both_sides) (axis='frame4', excess=2)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1618, in test_g1_g2_each_frame_both_sides
    self.result(record, "PARTIAL" if excess == 1 else "TRADEOFF")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'TRADEOFF'
- UNIMPLEMENTED
+ TRADEOFF


======================================================================
FAIL: test_g1_g2_each_frame_both_sides (__main__.ReaderProcessLocalityTests.test_g1_g2_each_frame_both_sides) (axis='frame5', excess=1)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1618, in test_g1_g2_each_frame_both_sides
    self.result(record, "PARTIAL" if excess == 1 else "TRADEOFF")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'PARTIAL'
- UNIMPLEMENTED
+ PARTIAL


======================================================================
FAIL: test_g1_g2_each_frame_both_sides (__main__.ReaderProcessLocalityTests.test_g1_g2_each_frame_both_sides) (axis='frame5', excess=2)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1618, in test_g1_g2_each_frame_both_sides
    self.result(record, "PARTIAL" if excess == 1 else "TRADEOFF")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'TRADEOFF'
- UNIMPLEMENTED
+ TRADEOFF


======================================================================
FAIL: test_g3_g4_g5_unrounded_boundaries (__main__.ReaderProcessLocalityTests.test_g3_g4_g5_unrounded_boundaries)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1626, in test_g3_g4_g5_unrounded_boundaries
    self.result(record, label)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'PARTIAL'
- UNIMPLEMENTED
+ PARTIAL


======================================================================
FAIL: test_g3_g5_display_rounding_cannot_substitute (__main__.ReaderProcessLocalityTests.test_g3_g5_display_rounding_cannot_substitute)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1636, in test_g3_g5_display_rounding_cannot_substitute
    self.result(record, "TRADEOFF")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'TRADEOFF'
- UNIMPLEMENTED
+ TRADEOFF


======================================================================
FAIL: test_g6_relation_flips_report_only (__main__.ReaderProcessLocalityTests.test_g6_relation_flips_report_only)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1643, in test_g6_relation_flips_report_only
    self.result(record, "PARTIAL")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'PARTIAL'
- UNIMPLEMENTED
+ PARTIAL


======================================================================
FAIL: test_p1_p2_p3 (__main__.ReaderProcessLocalityTests.test_p1_p2_p3)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1593, in test_p1_p2_p3
    self.result(record, "INCOMPLETE")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INCOMPLETE'
- UNIMPLEMENTED
+ INCOMPLETE


======================================================================
FAIL: test_p4_p5_p7_count_and_gain_boundaries (__main__.ReaderProcessLocalityTests.test_p4_p5_p7_count_and_gain_boundaries)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1606, in test_p4_p5_p7_count_and_gain_boundaries
    self.result(record, label)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'NULL'
- UNIMPLEMENTED
+ NULL


======================================================================
FAIL: test_p6_tradeoff_and_p7_null_first_match (__main__.ReaderProcessLocalityTests.test_p6_tradeoff_and_p7_null_first_match)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1650, in test_p6_tradeoff_and_p7_null_first_match
    self.result(record, "TRADEOFF" if n >= 22 else "NULL")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'TRADEOFF'
- UNIMPLEMENTED
+ TRADEOFF


======================================================================
FAIL: test_w1_actual_size_boundary_qualifier_preserves_base (__main__.ReaderProcessLocalityTests.test_w1_actual_size_boundary_qualifier_preserves_base)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1656, in test_w1_actual_size_boundary_qualifier_preserves_base
    self.result(record, "LEAD", include=() if ratio == 1.5 else ("LARGE-WRITE",), exclude=("LARGE-WRITE",) if ratio == 1.5 else (), advance=None if ratio == 1.5 else False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'LEAD'
- UNIMPLEMENTED
+ LEAD


======================================================================
FAIL: test_w2_ttl_warning_equality_nonblocking (__main__.ReaderProcessLocalityTests.test_w2_ttl_warning_equality_nonblocking)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1666, in test_w2_ttl_warning_equality_nonblocking
    self.result(record, "PARTIAL", include=("EXCEEDS-TTL",) if seconds == 3600.0 else (), exclude=() if seconds == 3600.0 else ("EXCEEDS-TTL",))
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'PARTIAL'
- UNIMPLEMENTED
+ PARTIAL


======================================================================
FAIL: test_authored_full_truth_rows_277_289 (__main__.ReaderTruthTableTests.test_authored_full_truth_rows_277_289) (prereg_line=277, case='controls24')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1974, in test_authored_full_truth_rows_277_289
    self.pair(p1, p2, label, include=qualifiers)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1128, in pair
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'LEAD'
- UNIMPLEMENTED
+ LEAD


======================================================================
FAIL: test_authored_full_truth_rows_277_289 (__main__.ReaderTruthTableTests.test_authored_full_truth_rows_277_289) (prereg_line=278, case='controls20')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1974, in test_authored_full_truth_rows_277_289
    self.pair(p1, p2, label, include=qualifiers)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1128, in pair
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'LEAD'
- UNIMPLEMENTED
+ LEAD


======================================================================
FAIL: test_authored_full_truth_rows_277_289 (__main__.ReaderTruthTableTests.test_authored_full_truth_rows_277_289) (prereg_line=279, case='nm17')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1974, in test_authored_full_truth_rows_277_289
    self.pair(p1, p2, label, include=qualifiers)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1128, in pair
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'PARTIAL'
- UNIMPLEMENTED
+ PARTIAL


======================================================================
FAIL: test_authored_full_truth_rows_277_289 (__main__.ReaderTruthTableTests.test_authored_full_truth_rows_277_289) (prereg_line=280, case='anchor24')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1974, in test_authored_full_truth_rows_277_289
    self.pair(p1, p2, label, include=qualifiers)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1128, in pair
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'PARTIAL'
- UNIMPLEMENTED
+ PARTIAL


======================================================================
FAIL: test_authored_full_truth_rows_277_289 (__main__.ReaderTruthTableTests.test_authored_full_truth_rows_277_289) (prereg_line=281, case='anchor_unfit')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1974, in test_authored_full_truth_rows_277_289
    self.pair(p1, p2, label, include=qualifiers)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1128, in pair
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'PARTIAL'
- UNIMPLEMENTED
+ PARTIAL


======================================================================
FAIL: test_authored_full_truth_rows_277_289 (__main__.ReaderTruthTableTests.test_authored_full_truth_rows_277_289) (prereg_line=282, case='anchor_gap9')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1974, in test_authored_full_truth_rows_277_289
    self.pair(p1, p2, label, include=qualifiers)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1128, in pair
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'PARTIAL'
- UNIMPLEMENTED
+ PARTIAL


======================================================================
FAIL: test_authored_full_truth_rows_277_289 (__main__.ReaderTruthTableTests.test_authored_full_truth_rows_277_289) (prereg_line=283, case='anchor_gap10')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1974, in test_authored_full_truth_rows_277_289
    self.pair(p1, p2, label, include=qualifiers)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1128, in pair
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'PARTIAL'
- UNIMPLEMENTED
+ PARTIAL


======================================================================
FAIL: test_authored_full_truth_rows_277_289 (__main__.ReaderTruthTableTests.test_authored_full_truth_rows_277_289) (prereg_line=284, case='count18')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1974, in test_authored_full_truth_rows_277_289
    self.pair(p1, p2, label, include=qualifiers)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1128, in pair
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'NULL'
- UNIMPLEMENTED
+ NULL


======================================================================
FAIL: test_authored_full_truth_rows_277_289 (__main__.ReaderTruthTableTests.test_authored_full_truth_rows_277_289) (prereg_line=285, case='counts30_22')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1974, in test_authored_full_truth_rows_277_289
    self.pair(p1, p2, label, include=qualifiers)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1128, in pair
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'MIXED-NOT-REPLICATED'
- UNIMPLEMENTED
+ MIXED-NOT-REPLICATED


======================================================================
FAIL: test_authored_full_truth_rows_277_289 (__main__.ReaderTruthTableTests.test_authored_full_truth_rows_277_289) (prereg_line=286, case='baseline5_nm18')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1974, in test_authored_full_truth_rows_277_289
    self.pair(p1, p2, label, include=qualifiers)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1128, in pair
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'PARTIAL'
- UNIMPLEMENTED
+ PARTIAL


======================================================================
FAIL: test_authored_full_truth_rows_277_289 (__main__.ReaderTruthTableTests.test_authored_full_truth_rows_277_289) (prereg_line=287, case='lead_tradeoff')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1974, in test_authored_full_truth_rows_277_289
    self.pair(p1, p2, label, include=qualifiers)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1128, in pair
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'MIXED-NOT-REPLICATED'
- UNIMPLEMENTED
+ MIXED-NOT-REPLICATED


======================================================================
FAIL: test_authored_full_truth_rows_277_289 (__main__.ReaderTruthTableTests.test_authored_full_truth_rows_277_289) (prereg_line=287, case='lead_underfit')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1974, in test_authored_full_truth_rows_277_289
    self.pair(p1, p2, label, include=qualifiers)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1128, in pair
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'MIXED-NOT-REPLICATED'
- UNIMPLEMENTED
+ MIXED-NOT-REPLICATED


======================================================================
FAIL: test_authored_full_truth_rows_277_289 (__main__.ReaderTruthTableTests.test_authored_full_truth_rows_277_289) (prereg_line=288, case='p2_halted')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1974, in test_authored_full_truth_rows_277_289
    self.pair(p1, p2, label, include=qualifiers)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1128, in pair
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'PARTIAL'
- UNIMPLEMENTED
+ PARTIAL


======================================================================
FAIL: test_authored_full_truth_rows_277_289 (__main__.ReaderTruthTableTests.test_authored_full_truth_rows_277_289) (prereg_line=289, case='a1_67')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1971, in test_authored_full_truth_rows_277_289
    self.result(p1, label)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_authored_full_truth_rows_277_289 (__main__.ReaderTruthTableTests.test_authored_full_truth_rows_277_289) (prereg_line=289, case='nonfinite')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1971, in test_authored_full_truth_rows_277_289
    self.result(p1, label)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_authored_stage1_truth_rows_265_276 (__main__.ReaderTruthTableTests.test_authored_stage1_truth_rows_265_276) (prereg_line=265, case='baseline')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1925, in test_authored_stage1_truth_rows_265_276
    self.result(record, label)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'HALTED'
- UNIMPLEMENTED
+ HALTED


======================================================================
FAIL: test_authored_stage1_truth_rows_265_276 (__main__.ReaderTruthTableTests.test_authored_stage1_truth_rows_265_276) (prereg_line=266, case='forecast130')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1925, in test_authored_stage1_truth_rows_265_276
    self.result(record, label)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'HALTED-BUDGET'
- UNIMPLEMENTED
+ HALTED-BUDGET


======================================================================
FAIL: test_authored_stage1_truth_rows_265_276 (__main__.ReaderTruthTableTests.test_authored_stage1_truth_rows_265_276) (prereg_line=267, case='deadline_afterwrite')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1925, in test_authored_stage1_truth_rows_265_276
    self.result(record, label)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INCOMPLETE-BUDGET'
- UNIMPLEMENTED
+ INCOMPLETE-BUDGET


======================================================================
FAIL: test_authored_stage1_truth_rows_265_276 (__main__.ReaderTruthTableTests.test_authored_stage1_truth_rows_265_276) (prereg_line=268, case='projection_afterwrite')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1925, in test_authored_stage1_truth_rows_265_276
    self.result(record, label)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INCOMPLETE-BUDGET'
- UNIMPLEMENTED
+ INCOMPLETE-BUDGET


======================================================================
FAIL: test_authored_stage1_truth_rows_265_276 (__main__.ReaderTruthTableTests.test_authored_stage1_truth_rows_265_276) (prereg_line=269, case='underfit25')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1925, in test_authored_stage1_truth_rows_265_276
    self.result(record, label)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'SCREEN-UNDERFIT'
- UNIMPLEMENTED
+ SCREEN-UNDERFIT


======================================================================
FAIL: test_authored_stage1_truth_rows_265_276 (__main__.ReaderTruthTableTests.test_authored_stage1_truth_rows_265_276) (prereg_line=270, case='count21')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1925, in test_authored_stage1_truth_rows_265_276
    self.result(record, label)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'SCREEN-NULL'
- UNIMPLEMENTED
+ SCREEN-NULL


======================================================================
FAIL: test_authored_stage1_truth_rows_265_276 (__main__.ReaderTruthTableTests.test_authored_stage1_truth_rows_265_276) (prereg_line=271, case='count22')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1925, in test_authored_stage1_truth_rows_265_276
    self.result(record, label)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'SCREEN-PASS'
- UNIMPLEMENTED
+ SCREEN-PASS


======================================================================
FAIL: test_authored_stage1_truth_rows_265_276 (__main__.ReaderTruthTableTests.test_authored_stage1_truth_rows_265_276) (prereg_line=272, case='large31')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1925, in test_authored_stage1_truth_rows_265_276
    self.result(record, label)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'SCREEN-NOT-ADVANCED'
- UNIMPLEMENTED
+ SCREEN-NOT-ADVANCED


======================================================================
FAIL: test_authored_stage1_truth_rows_265_276 (__main__.ReaderTruthTableTests.test_authored_stage1_truth_rows_265_276) (prereg_line=273, case='described25')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1925, in test_authored_stage1_truth_rows_265_276
    self.result(record, label)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'SCREEN-NOT-ADVANCED'
- UNIMPLEMENTED
+ SCREEN-NOT-ADVANCED


======================================================================
FAIL: test_authored_stage1_truth_rows_265_276 (__main__.ReaderTruthTableTests.test_authored_stage1_truth_rows_265_276) (prereg_line=274, case='frame27')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1925, in test_authored_stage1_truth_rows_265_276
    self.result(record, label)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'SCREEN-NOT-ADVANCED'
- UNIMPLEMENTED
+ SCREEN-NOT-ADVANCED


======================================================================
FAIL: test_authored_stage1_truth_rows_265_276 (__main__.ReaderTruthTableTests.test_authored_stage1_truth_rows_265_276) (prereg_line=275, case='baseline18_count27')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1925, in test_authored_stage1_truth_rows_265_276
    self.result(record, label)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'SCREEN-NULL'
- UNIMPLEMENTED
+ SCREEN-NULL


======================================================================
FAIL: test_authored_stage1_truth_rows_265_276 (__main__.ReaderTruthTableTests.test_authored_stage1_truth_rows_265_276) (prereg_line=275, case='baseline18_count28')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1925, in test_authored_stage1_truth_rows_265_276
    self.result(record, label)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'SCREEN-PASS'
- UNIMPLEMENTED
+ SCREEN-PASS


======================================================================
FAIL: test_authored_stage1_truth_rows_265_276 (__main__.ReaderTruthTableTests.test_authored_stage1_truth_rows_265_276) (prereg_line=276, case='baseline5_count19')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1925, in test_authored_stage1_truth_rows_265_276
    self.result(record, label)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'SCREEN-PASS'
- UNIMPLEMENTED
+ SCREEN-PASS


======================================================================
FAIL: test_v10_overflow_retries_five_six (__main__.ReaderValidityTests.test_v10_overflow_retries_five_six)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1418, in test_v10_overflow_retries_five_six
    self.result(record, "SCREEN-PASS" if retries == 5 else "INVALID")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'SCREEN-PASS'
- UNIMPLEMENTED
+ SCREEN-PASS


======================================================================
FAIL: test_v11_hin_hashes_and_write_trace_required (__main__.ReaderValidityTests.test_v11_hin_hashes_and_write_trace_required) (missing='H_in')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1434, in test_v11_hin_hashes_and_write_trace_required
    self.result(record, "INVALID", advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v11_hin_hashes_and_write_trace_required (__main__.ReaderValidityTests.test_v11_hin_hashes_and_write_trace_required) (missing='source_hash')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1434, in test_v11_hin_hashes_and_write_trace_required
    self.result(record, "INVALID", advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v11_hin_hashes_and_write_trace_required (__main__.ReaderValidityTests.test_v11_hin_hashes_and_write_trace_required) (missing='artifact_hash')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1434, in test_v11_hin_hashes_and_write_trace_required
    self.result(record, "INVALID", advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v11_hin_hashes_and_write_trace_required (__main__.ReaderValidityTests.test_v11_hin_hashes_and_write_trace_required) (missing='stop_reason')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1434, in test_v11_hin_hashes_and_write_trace_required
    self.result(record, "INVALID", advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v11_hin_hashes_and_write_trace_required (__main__.ReaderValidityTests.test_v11_hin_hashes_and_write_trace_required) (missing='accepted_steps')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1434, in test_v11_hin_hashes_and_write_trace_required
    self.result(record, "INVALID", advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v11_hin_hashes_and_write_trace_required (__main__.ReaderValidityTests.test_v11_hin_hashes_and_write_trace_required) (missing='overflow_retries')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1434, in test_v11_hin_hashes_and_write_trace_required
    self.result(record, "INVALID", advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v11_hin_hashes_and_write_trace_required (__main__.ReaderValidityTests.test_v11_hin_hashes_and_write_trace_required) (missing='H_out')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1434, in test_v11_hin_hashes_and_write_trace_required
    self.result(record, "INVALID", advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v12_leakage_named_halt (__main__.ReaderValidityTests.test_v12_leakage_named_halt)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1439, in test_v12_leakage_named_halt
    self.result(record, "INVALID-LEAKAGE", advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID-LEAKAGE'
- UNIMPLEMENTED
+ INVALID-LEAKAGE


======================================================================
FAIL: test_v13_every_applicable_numeric_family_nonfinite (__main__.ReaderValidityTests.test_v13_every_applicable_numeric_family_nonfinite) (family='raw_described', value=None)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1483, in test_v13_every_applicable_numeric_family_nonfinite
    self.result(record, "INVALID", advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v13_every_applicable_numeric_family_nonfinite (__main__.ReaderValidityTests.test_v13_every_applicable_numeric_family_nonfinite) (family='raw_described', value=nan)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1483, in test_v13_every_applicable_numeric_family_nonfinite
    self.result(record, "INVALID", advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v13_every_applicable_numeric_family_nonfinite (__main__.ReaderValidityTests.test_v13_every_applicable_numeric_family_nonfinite) (family='raw_described', value=inf)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1483, in test_v13_every_applicable_numeric_family_nonfinite
    self.result(record, "INVALID", advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v13_every_applicable_numeric_family_nonfinite (__main__.ReaderValidityTests.test_v13_every_applicable_numeric_family_nonfinite) (family='raw_described', value=-inf)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1483, in test_v13_every_applicable_numeric_family_nonfinite
    self.result(record, "INVALID", advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v13_every_applicable_numeric_family_nonfinite (__main__.ReaderValidityTests.test_v13_every_applicable_numeric_family_nonfinite) (family='raw_ppl', value=None)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1483, in test_v13_every_applicable_numeric_family_nonfinite
    self.result(record, "INVALID", advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v13_every_applicable_numeric_family_nonfinite (__main__.ReaderValidityTests.test_v13_every_applicable_numeric_family_nonfinite) (family='raw_ppl', value=nan)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1483, in test_v13_every_applicable_numeric_family_nonfinite
    self.result(record, "INVALID", advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v13_every_applicable_numeric_family_nonfinite (__main__.ReaderValidityTests.test_v13_every_applicable_numeric_family_nonfinite) (family='raw_ppl', value=inf)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1483, in test_v13_every_applicable_numeric_family_nonfinite
    self.result(record, "INVALID", advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v13_every_applicable_numeric_family_nonfinite (__main__.ReaderValidityTests.test_v13_every_applicable_numeric_family_nonfinite) (family='raw_ppl', value=-inf)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1483, in test_v13_every_applicable_numeric_family_nonfinite
    self.result(record, "INVALID", advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v13_every_applicable_numeric_family_nonfinite (__main__.ReaderValidityTests.test_v13_every_applicable_numeric_family_nonfinite) (family='actual_norm', value=None)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1483, in test_v13_every_applicable_numeric_family_nonfinite
    self.result(record, "INVALID", advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v13_every_applicable_numeric_family_nonfinite (__main__.ReaderValidityTests.test_v13_every_applicable_numeric_family_nonfinite) (family='actual_norm', value=nan)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1483, in test_v13_every_applicable_numeric_family_nonfinite
    self.result(record, "INVALID", advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v13_every_applicable_numeric_family_nonfinite (__main__.ReaderValidityTests.test_v13_every_applicable_numeric_family_nonfinite) (family='actual_norm', value=inf)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1483, in test_v13_every_applicable_numeric_family_nonfinite
    self.result(record, "INVALID", advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v13_every_applicable_numeric_family_nonfinite (__main__.ReaderValidityTests.test_v13_every_applicable_numeric_family_nonfinite) (family='actual_norm', value=-inf)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1483, in test_v13_every_applicable_numeric_family_nonfinite
    self.result(record, "INVALID", advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v13_every_applicable_numeric_family_nonfinite (__main__.ReaderValidityTests.test_v13_every_applicable_numeric_family_nonfinite) (family='planned_norm', value=None)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1483, in test_v13_every_applicable_numeric_family_nonfinite
    self.result(record, "INVALID", advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v13_every_applicable_numeric_family_nonfinite (__main__.ReaderValidityTests.test_v13_every_applicable_numeric_family_nonfinite) (family='planned_norm', value=nan)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1483, in test_v13_every_applicable_numeric_family_nonfinite
    self.result(record, "INVALID", advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v13_every_applicable_numeric_family_nonfinite (__main__.ReaderValidityTests.test_v13_every_applicable_numeric_family_nonfinite) (family='planned_norm', value=inf)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1483, in test_v13_every_applicable_numeric_family_nonfinite
    self.result(record, "INVALID", advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v13_every_applicable_numeric_family_nonfinite (__main__.ReaderValidityTests.test_v13_every_applicable_numeric_family_nonfinite) (family='planned_norm', value=-inf)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1483, in test_v13_every_applicable_numeric_family_nonfinite
    self.result(record, "INVALID", advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v13_every_applicable_numeric_family_nonfinite (__main__.ReaderValidityTests.test_v13_every_applicable_numeric_family_nonfinite) (family='null_share', value=None)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1483, in test_v13_every_applicable_numeric_family_nonfinite
    self.result(record, "INVALID", advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v13_every_applicable_numeric_family_nonfinite (__main__.ReaderValidityTests.test_v13_every_applicable_numeric_family_nonfinite) (family='null_share', value=nan)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1483, in test_v13_every_applicable_numeric_family_nonfinite
    self.result(record, "INVALID", advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v13_every_applicable_numeric_family_nonfinite (__main__.ReaderValidityTests.test_v13_every_applicable_numeric_family_nonfinite) (family='null_share', value=inf)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1483, in test_v13_every_applicable_numeric_family_nonfinite
    self.result(record, "INVALID", advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v13_every_applicable_numeric_family_nonfinite (__main__.ReaderValidityTests.test_v13_every_applicable_numeric_family_nonfinite) (family='null_share', value=-inf)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1483, in test_v13_every_applicable_numeric_family_nonfinite
    self.result(record, "INVALID", advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v13_every_applicable_numeric_family_nonfinite (__main__.ReaderValidityTests.test_v13_every_applicable_numeric_family_nonfinite) (family='fit_probability', value=None)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1483, in test_v13_every_applicable_numeric_family_nonfinite
    self.result(record, "INVALID", advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v13_every_applicable_numeric_family_nonfinite (__main__.ReaderValidityTests.test_v13_every_applicable_numeric_family_nonfinite) (family='fit_probability', value=nan)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1483, in test_v13_every_applicable_numeric_family_nonfinite
    self.result(record, "INVALID", advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v13_every_applicable_numeric_family_nonfinite (__main__.ReaderValidityTests.test_v13_every_applicable_numeric_family_nonfinite) (family='fit_probability', value=inf)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1483, in test_v13_every_applicable_numeric_family_nonfinite
    self.result(record, "INVALID", advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v13_every_applicable_numeric_family_nonfinite (__main__.ReaderValidityTests.test_v13_every_applicable_numeric_family_nonfinite) (family='fit_probability', value=-inf)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1483, in test_v13_every_applicable_numeric_family_nonfinite
    self.result(record, "INVALID", advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v13_every_applicable_numeric_family_nonfinite (__main__.ReaderValidityTests.test_v13_every_applicable_numeric_family_nonfinite) (family='compile_time', value=None)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1483, in test_v13_every_applicable_numeric_family_nonfinite
    self.result(record, "INVALID", advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v13_every_applicable_numeric_family_nonfinite (__main__.ReaderValidityTests.test_v13_every_applicable_numeric_family_nonfinite) (family='compile_time', value=nan)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1483, in test_v13_every_applicable_numeric_family_nonfinite
    self.result(record, "INVALID", advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v13_every_applicable_numeric_family_nonfinite (__main__.ReaderValidityTests.test_v13_every_applicable_numeric_family_nonfinite) (family='compile_time', value=inf)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1483, in test_v13_every_applicable_numeric_family_nonfinite
    self.result(record, "INVALID", advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v13_every_applicable_numeric_family_nonfinite (__main__.ReaderValidityTests.test_v13_every_applicable_numeric_family_nonfinite) (family='compile_time', value=-inf)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1483, in test_v13_every_applicable_numeric_family_nonfinite
    self.result(record, "INVALID", advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v13_every_applicable_numeric_family_nonfinite (__main__.ReaderValidityTests.test_v13_every_applicable_numeric_family_nonfinite) (family='capture_distance', value=None)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1483, in test_v13_every_applicable_numeric_family_nonfinite
    self.result(record, "INVALID", advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v13_every_applicable_numeric_family_nonfinite (__main__.ReaderValidityTests.test_v13_every_applicable_numeric_family_nonfinite) (family='capture_distance', value=nan)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1483, in test_v13_every_applicable_numeric_family_nonfinite
    self.result(record, "INVALID", advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v13_every_applicable_numeric_family_nonfinite (__main__.ReaderValidityTests.test_v13_every_applicable_numeric_family_nonfinite) (family='capture_distance', value=inf)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1483, in test_v13_every_applicable_numeric_family_nonfinite
    self.result(record, "INVALID", advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v13_every_applicable_numeric_family_nonfinite (__main__.ReaderValidityTests.test_v13_every_applicable_numeric_family_nonfinite) (family='capture_distance', value=-inf)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1483, in test_v13_every_applicable_numeric_family_nonfinite
    self.result(record, "INVALID", advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v13_nonfinite_unjustified_null_and_typed_integer (__main__.ReaderValidityTests.test_v13_nonfinite_unjustified_null_and_typed_integer)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1460, in test_v13_nonfinite_unjustified_null_and_typed_integer
    self.result(record, "INVALID", advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v13_typed_nulls_and_reasons (__main__.ReaderValidityTests.test_v13_typed_nulls_and_reasons)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1443, in test_v13_typed_nulls_and_reasons
    self.result(record, "PARTIAL")  # A1 has zero continuation denominator.
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'PARTIAL'
- UNIMPLEMENTED
+ PARTIAL


======================================================================
FAIL: test_v1_fingerprint_sha_sites_and_full_output (__main__.ReaderValidityTests.test_v1_fingerprint_sha_sites_and_full_output) (field='sha256', value='2222222222222222222222222222222222222222222222222222222222222222')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1217, in test_v1_fingerprint_sha_sites_and_full_output
    self.result(record, "HALTED", advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'HALTED'
- UNIMPLEMENTED
+ HALTED


======================================================================
FAIL: test_v1_fingerprint_sha_sites_and_full_output (__main__.ReaderValidityTests.test_v1_fingerprint_sha_sites_and_full_output) (field='cov_cpu_sites', value=2)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1217, in test_v1_fingerprint_sha_sites_and_full_output
    self.result(record, "HALTED", advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'HALTED'
- UNIMPLEMENTED
+ HALTED


======================================================================
FAIL: test_v1_fingerprint_sha_sites_and_full_output (__main__.ReaderValidityTests.test_v1_fingerprint_sha_sites_and_full_output) (field='cov_cpu_sites', value=4)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1217, in test_v1_fingerprint_sha_sites_and_full_output
    self.result(record, "HALTED", advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'HALTED'
- UNIMPLEMENTED
+ HALTED


======================================================================
FAIL: test_v1_fingerprint_sha_sites_and_full_output (__main__.ReaderValidityTests.test_v1_fingerprint_sha_sites_and_full_output) (field='output', value='')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1217, in test_v1_fingerprint_sha_sites_and_full_output
    self.result(record, "HALTED", advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'HALTED'
- UNIMPLEMENTED
+ HALTED


======================================================================
FAIL: test_v2_each_recipe_standing_law5 (__main__.ReaderValidityTests.test_v2_each_recipe_standing_law5)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1221, in test_v2_each_recipe_standing_law5
    self.result(record, "PARTIAL")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'PARTIAL'
- UNIMPLEMENTED
+ PARTIAL


======================================================================
FAIL: test_v3_accumulation_raw_cosine_distance_finiteness_and_scope (__main__.ReaderValidityTests.test_v3_accumulation_raw_cosine_distance_finiteness_and_scope)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1285, in test_v3_accumulation_raw_cosine_distance_finiteness_and_scope
    self.result(record, "SCREEN-PASS" if value == inside else "INVALID")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'SCREEN-PASS'
- UNIMPLEMENTED
+ SCREEN-PASS


======================================================================
FAIL: test_v3_apply_stored_substitutions_not_optimiser_checks (__main__.ReaderValidityTests.test_v3_apply_stored_substitutions_not_optimiser_checks)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1246, in test_v3_apply_stored_substitutions_not_optimiser_checks
    self.result(record, "PARTIAL", recipe="B-e2e-NM")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'PARTIAL'
- UNIMPLEMENTED
+ PARTIAL


======================================================================
FAIL: test_v3_capture_zero_step_and_executed_loop_raw_values (__main__.ReaderValidityTests.test_v3_capture_zero_step_and_executed_loop_raw_values)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1261, in test_v3_capture_zero_step_and_executed_loop_raw_values
    self.result(record, "SCREEN-PASS" if allowed else "INVALID")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'SCREEN-PASS'
- UNIMPLEMENTED
+ SCREEN-PASS


======================================================================
FAIL: test_v3_check_failure_order_and_scope (__main__.ReaderValidityTests.test_v3_check_failure_order_and_scope) (arm='A1_single', failure='passed')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1232, in test_v3_check_failure_order_and_scope
    self.result(record, "INVALID", advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v3_check_failure_order_and_scope (__main__.ReaderValidityTests.test_v3_check_failure_order_and_scope) (arm='A1_single', failure='before_result')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1232, in test_v3_check_failure_order_and_scope
    self.result(record, "INVALID", advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v3_check_failure_order_and_scope (__main__.ReaderValidityTests.test_v3_check_failure_order_and_scope) (arm='A1_single', failure='scope')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1232, in test_v3_check_failure_order_and_scope
    self.result(record, "INVALID", advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v3_check_failure_order_and_scope (__main__.ReaderValidityTests.test_v3_check_failure_order_and_scope) (arm='A2_coherent2', failure='passed')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1232, in test_v3_check_failure_order_and_scope
    self.result(record, "INVALID", advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v3_check_failure_order_and_scope (__main__.ReaderValidityTests.test_v3_check_failure_order_and_scope) (arm='A2_coherent2', failure='before_result')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1232, in test_v3_check_failure_order_and_scope
    self.result(record, "INVALID", advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v3_check_failure_order_and_scope (__main__.ReaderValidityTests.test_v3_check_failure_order_and_scope) (arm='A2_coherent2', failure='scope')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1232, in test_v3_check_failure_order_and_scope
    self.result(record, "INVALID", advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v3_check_failure_order_and_scope (__main__.ReaderValidityTests.test_v3_check_failure_order_and_scope) (arm='A7_coined_coined', failure='passed')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1232, in test_v3_check_failure_order_and_scope
    self.result(record, "INVALID", advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v3_check_failure_order_and_scope (__main__.ReaderValidityTests.test_v3_check_failure_order_and_scope) (arm='A7_coined_coined', failure='before_result')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1232, in test_v3_check_failure_order_and_scope
    self.result(record, "INVALID", advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v3_check_failure_order_and_scope (__main__.ReaderValidityTests.test_v3_check_failure_order_and_scope) (arm='A7_coined_coined', failure='scope')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1232, in test_v3_check_failure_order_and_scope
    self.result(record, "INVALID", advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v3_gradient_halvings_hooks_and_smoke_raw_values (__main__.ReaderValidityTests.test_v3_gradient_halvings_hooks_and_smoke_raw_values)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1300, in test_v3_gradient_halvings_hooks_and_smoke_raw_values
    self.result(record, "SCREEN-PASS" if halvings == 3 else "INVALID")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'SCREEN-PASS'
- UNIMPLEMENTED
+ SCREEN-PASS


======================================================================
FAIL: test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-e2e', arm='A1_single', check='capture')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1242, in test_v3_missing_required_check_invalid
    self.result(invalid, "INVALID", recipe=recipe, advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-e2e', arm='A1_single', check='zero_step')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1242, in test_v3_missing_required_check_invalid
    self.result(invalid, "INVALID", recipe=recipe, advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-e2e', arm='A1_single', check='executed_loop')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1242, in test_v3_missing_required_check_invalid
    self.result(invalid, "INVALID", recipe=recipe, advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-e2e', arm='A1_single', check='projector')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1242, in test_v3_missing_required_check_invalid
    self.result(invalid, "INVALID", recipe=recipe, advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-e2e', arm='A1_single', check='hooks')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1242, in test_v3_missing_required_check_invalid
    self.result(invalid, "INVALID", recipe=recipe, advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-e2e', arm='A1_single', check='train_deploy')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1242, in test_v3_missing_required_check_invalid
    self.result(invalid, "INVALID", recipe=recipe, advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-e2e', arm='A1_single', check='gradient')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1242, in test_v3_missing_required_check_invalid
    self.result(invalid, "INVALID", recipe=recipe, advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-e2e', arm='A2_coherent2', check='capture')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1242, in test_v3_missing_required_check_invalid
    self.result(invalid, "INVALID", recipe=recipe, advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-e2e', arm='A2_coherent2', check='zero_step')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1242, in test_v3_missing_required_check_invalid
    self.result(invalid, "INVALID", recipe=recipe, advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-e2e', arm='A2_coherent2', check='executed_loop')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1242, in test_v3_missing_required_check_invalid
    self.result(invalid, "INVALID", recipe=recipe, advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-e2e', arm='A2_coherent2', check='projector')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1242, in test_v3_missing_required_check_invalid
    self.result(invalid, "INVALID", recipe=recipe, advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-e2e', arm='A2_coherent2', check='hooks')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1242, in test_v3_missing_required_check_invalid
    self.result(invalid, "INVALID", recipe=recipe, advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-e2e', arm='A2_coherent2', check='train_deploy')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1242, in test_v3_missing_required_check_invalid
    self.result(invalid, "INVALID", recipe=recipe, advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-e2e', arm='A2_coherent2', check='gradient')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1242, in test_v3_missing_required_check_invalid
    self.result(invalid, "INVALID", recipe=recipe, advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-e2e', arm='A7_coined_coined', check='capture')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1242, in test_v3_missing_required_check_invalid
    self.result(invalid, "INVALID", recipe=recipe, advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-e2e', arm='A7_coined_coined', check='zero_step')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1242, in test_v3_missing_required_check_invalid
    self.result(invalid, "INVALID", recipe=recipe, advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-e2e', arm='A7_coined_coined', check='executed_loop')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1242, in test_v3_missing_required_check_invalid
    self.result(invalid, "INVALID", recipe=recipe, advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-e2e', arm='A7_coined_coined', check='projector')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1242, in test_v3_missing_required_check_invalid
    self.result(invalid, "INVALID", recipe=recipe, advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-e2e', arm='A7_coined_coined', check='hooks')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1242, in test_v3_missing_required_check_invalid
    self.result(invalid, "INVALID", recipe=recipe, advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-e2e', arm='A7_coined_coined', check='train_deploy')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1242, in test_v3_missing_required_check_invalid
    self.result(invalid, "INVALID", recipe=recipe, advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-e2e', arm='A7_coined_coined', check='gradient')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1242, in test_v3_missing_required_check_invalid
    self.result(invalid, "INVALID", recipe=recipe, advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-e2e', arm='A7_coined_coined', check='accumulation')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1242, in test_v3_missing_required_check_invalid
    self.result(invalid, "INVALID", recipe=recipe, advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-e2e', arm='A7_coined_coined', check='objective')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1242, in test_v3_missing_required_check_invalid
    self.result(invalid, "INVALID", recipe=recipe, advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-e2e', arm='A7_coined_coined', check='smoke')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1242, in test_v3_missing_required_check_invalid
    self.result(invalid, "INVALID", recipe=recipe, advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-z', arm='A1_single', check='capture')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1242, in test_v3_missing_required_check_invalid
    self.result(invalid, "INVALID", recipe=recipe, advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-z', arm='A1_single', check='zero_step')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1242, in test_v3_missing_required_check_invalid
    self.result(invalid, "INVALID", recipe=recipe, advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-z', arm='A1_single', check='executed_loop')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1242, in test_v3_missing_required_check_invalid
    self.result(invalid, "INVALID", recipe=recipe, advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-z', arm='A1_single', check='projector')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1242, in test_v3_missing_required_check_invalid
    self.result(invalid, "INVALID", recipe=recipe, advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-z', arm='A1_single', check='hooks')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1242, in test_v3_missing_required_check_invalid
    self.result(invalid, "INVALID", recipe=recipe, advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-z', arm='A1_single', check='train_deploy')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1242, in test_v3_missing_required_check_invalid
    self.result(invalid, "INVALID", recipe=recipe, advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-z', arm='A1_single', check='gradient')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1242, in test_v3_missing_required_check_invalid
    self.result(invalid, "INVALID", recipe=recipe, advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-z', arm='A2_coherent2', check='capture')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1242, in test_v3_missing_required_check_invalid
    self.result(invalid, "INVALID", recipe=recipe, advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-z', arm='A2_coherent2', check='zero_step')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1242, in test_v3_missing_required_check_invalid
    self.result(invalid, "INVALID", recipe=recipe, advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-z', arm='A2_coherent2', check='executed_loop')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1242, in test_v3_missing_required_check_invalid
    self.result(invalid, "INVALID", recipe=recipe, advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-z', arm='A2_coherent2', check='projector')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1242, in test_v3_missing_required_check_invalid
    self.result(invalid, "INVALID", recipe=recipe, advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-z', arm='A2_coherent2', check='hooks')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1242, in test_v3_missing_required_check_invalid
    self.result(invalid, "INVALID", recipe=recipe, advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-z', arm='A2_coherent2', check='train_deploy')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1242, in test_v3_missing_required_check_invalid
    self.result(invalid, "INVALID", recipe=recipe, advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-z', arm='A2_coherent2', check='gradient')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1242, in test_v3_missing_required_check_invalid
    self.result(invalid, "INVALID", recipe=recipe, advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-z', arm='A7_coined_coined', check='capture')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1242, in test_v3_missing_required_check_invalid
    self.result(invalid, "INVALID", recipe=recipe, advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-z', arm='A7_coined_coined', check='zero_step')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1242, in test_v3_missing_required_check_invalid
    self.result(invalid, "INVALID", recipe=recipe, advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-z', arm='A7_coined_coined', check='executed_loop')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1242, in test_v3_missing_required_check_invalid
    self.result(invalid, "INVALID", recipe=recipe, advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-z', arm='A7_coined_coined', check='projector')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1242, in test_v3_missing_required_check_invalid
    self.result(invalid, "INVALID", recipe=recipe, advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-z', arm='A7_coined_coined', check='hooks')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1242, in test_v3_missing_required_check_invalid
    self.result(invalid, "INVALID", recipe=recipe, advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-z', arm='A7_coined_coined', check='train_deploy')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1242, in test_v3_missing_required_check_invalid
    self.result(invalid, "INVALID", recipe=recipe, advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-z', arm='A7_coined_coined', check='gradient')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1242, in test_v3_missing_required_check_invalid
    self.result(invalid, "INVALID", recipe=recipe, advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v3_missing_required_check_invalid (__main__.ReaderValidityTests.test_v3_missing_required_check_invalid) (recipe='B-z', arm='A7_coined_coined', check='accumulation')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1242, in test_v3_missing_required_check_invalid
    self.result(invalid, "INVALID", recipe=recipe, advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v3_objective_nll_and_nonzero_kl_raw_boundaries (__main__.ReaderValidityTests.test_v3_objective_nll_and_nonzero_kl_raw_boundaries)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1277, in test_v3_objective_nll_and_nonzero_kl_raw_boundaries
    self.result(record, "SCREEN-PASS" if error == 0.002 else "INVALID")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'SCREEN-PASS'
- UNIMPLEMENTED
+ SCREEN-PASS


======================================================================
FAIL: test_v4_a1_a2_and_exact_denominators (__main__.ReaderValidityTests.test_v4_a1_a2_and_exact_denominators)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1329, in test_v4_a1_a2_and_exact_denominators
    self.result(record, "SCREEN-PASS" if value == 68 else "HALTED")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'HALTED'
- UNIMPLEMENTED
+ HALTED


======================================================================
FAIL: test_v4_all_inclusive_baseline_endpoints (__main__.ReaderValidityTests.test_v4_all_inclusive_baseline_endpoints) (field='para_full_n', value=4)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1322, in test_v4_all_inclusive_baseline_endpoints
    self.result(record, "SCREEN-PASS" if value in allowed else "HALTED")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'HALTED'
- UNIMPLEMENTED
+ HALTED


======================================================================
FAIL: test_v4_all_inclusive_baseline_endpoints (__main__.ReaderValidityTests.test_v4_all_inclusive_baseline_endpoints) (field='para_full_n', value=5)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1322, in test_v4_all_inclusive_baseline_endpoints
    self.result(record, "SCREEN-PASS" if value in allowed else "HALTED")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'SCREEN-PASS'
- UNIMPLEMENTED
+ SCREEN-PASS


======================================================================
FAIL: test_v4_all_inclusive_baseline_endpoints (__main__.ReaderValidityTests.test_v4_all_inclusive_baseline_endpoints) (field='para_full_n', value=18)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1322, in test_v4_all_inclusive_baseline_endpoints
    self.result(record, "SCREEN-PASS" if value in allowed else "HALTED")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'SCREEN-PASS'
- UNIMPLEMENTED
+ SCREEN-PASS


======================================================================
FAIL: test_v4_all_inclusive_baseline_endpoints (__main__.ReaderValidityTests.test_v4_all_inclusive_baseline_endpoints) (field='para_full_n', value=19)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1322, in test_v4_all_inclusive_baseline_endpoints
    self.result(record, "SCREEN-PASS" if value in allowed else "HALTED")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'HALTED'
- UNIMPLEMENTED
+ HALTED


======================================================================
FAIL: test_v4_all_inclusive_baseline_endpoints (__main__.ReaderValidityTests.test_v4_all_inclusive_baseline_endpoints) (field='canon_full_n', value=4)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1322, in test_v4_all_inclusive_baseline_endpoints
    self.result(record, "SCREEN-PASS" if value in allowed else "HALTED")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'HALTED'
- UNIMPLEMENTED
+ HALTED


======================================================================
FAIL: test_v4_all_inclusive_baseline_endpoints (__main__.ReaderValidityTests.test_v4_all_inclusive_baseline_endpoints) (field='canon_full_n', value=5)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1322, in test_v4_all_inclusive_baseline_endpoints
    self.result(record, "SCREEN-PASS" if value in allowed else "HALTED")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'SCREEN-PASS'
- UNIMPLEMENTED
+ SCREEN-PASS


======================================================================
FAIL: test_v4_all_inclusive_baseline_endpoints (__main__.ReaderValidityTests.test_v4_all_inclusive_baseline_endpoints) (field='canon_full_n', value=10)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1322, in test_v4_all_inclusive_baseline_endpoints
    self.result(record, "SCREEN-PASS" if value in allowed else "HALTED")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'SCREEN-PASS'
- UNIMPLEMENTED
+ SCREEN-PASS


======================================================================
FAIL: test_v4_all_inclusive_baseline_endpoints (__main__.ReaderValidityTests.test_v4_all_inclusive_baseline_endpoints) (field='canon_full_n', value=11)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1322, in test_v4_all_inclusive_baseline_endpoints
    self.result(record, "SCREEN-PASS" if value in allowed else "HALTED")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'HALTED'
- UNIMPLEMENTED
+ HALTED


======================================================================
FAIL: test_v4_all_inclusive_baseline_endpoints (__main__.ReaderValidityTests.test_v4_all_inclusive_baseline_endpoints) (field='para_first_n', value=41)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1322, in test_v4_all_inclusive_baseline_endpoints
    self.result(record, "SCREEN-PASS" if value in allowed else "HALTED")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'HALTED'
- UNIMPLEMENTED
+ HALTED


======================================================================
FAIL: test_v4_all_inclusive_baseline_endpoints (__main__.ReaderValidityTests.test_v4_all_inclusive_baseline_endpoints) (field='para_first_n', value=42)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1322, in test_v4_all_inclusive_baseline_endpoints
    self.result(record, "SCREEN-PASS" if value in allowed else "HALTED")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'SCREEN-PASS'
- UNIMPLEMENTED
+ SCREEN-PASS


======================================================================
FAIL: test_v4_all_inclusive_baseline_endpoints (__main__.ReaderValidityTests.test_v4_all_inclusive_baseline_endpoints) (field='para_first_n', value=59)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1322, in test_v4_all_inclusive_baseline_endpoints
    self.result(record, "SCREEN-PASS" if value in allowed else "HALTED")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'SCREEN-PASS'
- UNIMPLEMENTED
+ SCREEN-PASS


======================================================================
FAIL: test_v4_all_inclusive_baseline_endpoints (__main__.ReaderValidityTests.test_v4_all_inclusive_baseline_endpoints) (field='para_first_n', value=60)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1322, in test_v4_all_inclusive_baseline_endpoints
    self.result(record, "SCREEN-PASS" if value in allowed else "HALTED")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'HALTED'
- UNIMPLEMENTED
+ HALTED


======================================================================
FAIL: test_v4_before_candidates_required (__main__.ReaderValidityTests.test_v4_before_candidates_required)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1338, in test_v4_before_candidates_required
    self.result(record, "HALTED", advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'HALTED'
- UNIMPLEMENTED
+ HALTED


======================================================================
FAIL: test_v5_candidate_controls_67_68_each_arm (__main__.ReaderValidityTests.test_v5_candidate_controls_67_68_each_arm) (arm='A1_single', value=67)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1346, in test_v5_candidate_controls_67_68_each_arm
    self.result(record, "PARTIAL" if value == 68 else "INVALID")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v5_candidate_controls_67_68_each_arm (__main__.ReaderValidityTests.test_v5_candidate_controls_67_68_each_arm) (arm='A1_single', value=68)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1346, in test_v5_candidate_controls_67_68_each_arm
    self.result(record, "PARTIAL" if value == 68 else "INVALID")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'PARTIAL'
- UNIMPLEMENTED
+ PARTIAL


======================================================================
FAIL: test_v5_candidate_controls_67_68_each_arm (__main__.ReaderValidityTests.test_v5_candidate_controls_67_68_each_arm) (arm='A2_coherent2', value=67)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1346, in test_v5_candidate_controls_67_68_each_arm
    self.result(record, "PARTIAL" if value == 68 else "INVALID")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v5_candidate_controls_67_68_each_arm (__main__.ReaderValidityTests.test_v5_candidate_controls_67_68_each_arm) (arm='A2_coherent2', value=68)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1346, in test_v5_candidate_controls_67_68_each_arm
    self.result(record, "PARTIAL" if value == 68 else "INVALID")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'PARTIAL'
- UNIMPLEMENTED
+ PARTIAL


======================================================================
FAIL: test_v6_overrides_are_exact_sets_not_counts (__main__.ReaderValidityTests.test_v6_overrides_are_exact_sets_not_counts) (failure='missing')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1365, in test_v6_overrides_are_exact_sets_not_counts
    self.result(record, "INVALID", advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v6_overrides_are_exact_sets_not_counts (__main__.ReaderValidityTests.test_v6_overrides_are_exact_sets_not_counts) (failure='undeclared')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1365, in test_v6_overrides_are_exact_sets_not_counts
    self.result(record, "INVALID", advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v6_overrides_are_exact_sets_not_counts (__main__.ReaderValidityTests.test_v6_overrides_are_exact_sets_not_counts) (failure='wrong_same_count')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1365, in test_v6_overrides_are_exact_sets_not_counts
    self.result(record, "INVALID", advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v6_overrides_are_exact_sets_not_counts (__main__.ReaderValidityTests.test_v6_overrides_are_exact_sets_not_counts) (failure='not_run_consumed')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1365, in test_v6_overrides_are_exact_sets_not_counts
    self.result(record, "INVALID", advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v6_overrides_are_exact_sets_not_counts (__main__.ReaderValidityTests.test_v6_overrides_are_exact_sets_not_counts) (failure='check_not_separate')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1365, in test_v6_overrides_are_exact_sets_not_counts
    self.result(record, "INVALID", advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v7_initial_projector_raw_share_cannot_hide_behind_passed (__main__.ReaderValidityTests.test_v7_initial_projector_raw_share_cannot_hide_behind_passed)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1390, in test_v7_initial_projector_raw_share_cannot_hide_behind_passed
    self.result(record, "SCREEN-PASS" if share == 0.999 else "INVALID")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'SCREEN-PASS'
- UNIMPLEMENTED
+ SCREEN-PASS


======================================================================
FAIL: test_v7_planned_actual_each_layer_boundary_and_zero (__main__.ReaderValidityTests.test_v7_planned_actual_each_layer_boundary_and_zero) (field='planned_null_share', layer=0, value=0.999)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1374, in test_v7_planned_actual_each_layer_boundary_and_zero
    self.result(record, "SCREEN-PASS" if value == 0.999 else "INVALID")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'SCREEN-PASS'
- UNIMPLEMENTED
+ SCREEN-PASS


======================================================================
FAIL: test_v7_planned_actual_each_layer_boundary_and_zero (__main__.ReaderValidityTests.test_v7_planned_actual_each_layer_boundary_and_zero) (field='planned_null_share', layer=0, value=0.9989999)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1374, in test_v7_planned_actual_each_layer_boundary_and_zero
    self.result(record, "SCREEN-PASS" if value == 0.999 else "INVALID")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v7_planned_actual_each_layer_boundary_and_zero (__main__.ReaderValidityTests.test_v7_planned_actual_each_layer_boundary_and_zero) (field='planned_null_share', layer=1, value=0.999)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1374, in test_v7_planned_actual_each_layer_boundary_and_zero
    self.result(record, "SCREEN-PASS" if value == 0.999 else "INVALID")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'SCREEN-PASS'
- UNIMPLEMENTED
+ SCREEN-PASS


======================================================================
FAIL: test_v7_planned_actual_each_layer_boundary_and_zero (__main__.ReaderValidityTests.test_v7_planned_actual_each_layer_boundary_and_zero) (field='planned_null_share', layer=1, value=0.9989999)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1374, in test_v7_planned_actual_each_layer_boundary_and_zero
    self.result(record, "SCREEN-PASS" if value == 0.999 else "INVALID")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v7_planned_actual_each_layer_boundary_and_zero (__main__.ReaderValidityTests.test_v7_planned_actual_each_layer_boundary_and_zero) (field='planned_null_share', layer=2, value=0.999)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1374, in test_v7_planned_actual_each_layer_boundary_and_zero
    self.result(record, "SCREEN-PASS" if value == 0.999 else "INVALID")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'SCREEN-PASS'
- UNIMPLEMENTED
+ SCREEN-PASS


======================================================================
FAIL: test_v7_planned_actual_each_layer_boundary_and_zero (__main__.ReaderValidityTests.test_v7_planned_actual_each_layer_boundary_and_zero) (field='planned_null_share', layer=2, value=0.9989999)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1374, in test_v7_planned_actual_each_layer_boundary_and_zero
    self.result(record, "SCREEN-PASS" if value == 0.999 else "INVALID")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v7_planned_actual_each_layer_boundary_and_zero (__main__.ReaderValidityTests.test_v7_planned_actual_each_layer_boundary_and_zero) (field='planned_null_share', layer=3, value=0.999)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1374, in test_v7_planned_actual_each_layer_boundary_and_zero
    self.result(record, "SCREEN-PASS" if value == 0.999 else "INVALID")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'SCREEN-PASS'
- UNIMPLEMENTED
+ SCREEN-PASS


======================================================================
FAIL: test_v7_planned_actual_each_layer_boundary_and_zero (__main__.ReaderValidityTests.test_v7_planned_actual_each_layer_boundary_and_zero) (field='planned_null_share', layer=3, value=0.9989999)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1374, in test_v7_planned_actual_each_layer_boundary_and_zero
    self.result(record, "SCREEN-PASS" if value == 0.999 else "INVALID")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v7_planned_actual_each_layer_boundary_and_zero (__main__.ReaderValidityTests.test_v7_planned_actual_each_layer_boundary_and_zero) (field='planned_null_share', layer=4, value=0.999)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1374, in test_v7_planned_actual_each_layer_boundary_and_zero
    self.result(record, "SCREEN-PASS" if value == 0.999 else "INVALID")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'SCREEN-PASS'
- UNIMPLEMENTED
+ SCREEN-PASS


======================================================================
FAIL: test_v7_planned_actual_each_layer_boundary_and_zero (__main__.ReaderValidityTests.test_v7_planned_actual_each_layer_boundary_and_zero) (field='planned_null_share', layer=4, value=0.9989999)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1374, in test_v7_planned_actual_each_layer_boundary_and_zero
    self.result(record, "SCREEN-PASS" if value == 0.999 else "INVALID")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v7_planned_actual_each_layer_boundary_and_zero (__main__.ReaderValidityTests.test_v7_planned_actual_each_layer_boundary_and_zero) (field='actual_null_share', layer=0, value=0.999)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1374, in test_v7_planned_actual_each_layer_boundary_and_zero
    self.result(record, "SCREEN-PASS" if value == 0.999 else "INVALID")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'SCREEN-PASS'
- UNIMPLEMENTED
+ SCREEN-PASS


======================================================================
FAIL: test_v7_planned_actual_each_layer_boundary_and_zero (__main__.ReaderValidityTests.test_v7_planned_actual_each_layer_boundary_and_zero) (field='actual_null_share', layer=0, value=0.9989999)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1374, in test_v7_planned_actual_each_layer_boundary_and_zero
    self.result(record, "SCREEN-PASS" if value == 0.999 else "INVALID")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v7_planned_actual_each_layer_boundary_and_zero (__main__.ReaderValidityTests.test_v7_planned_actual_each_layer_boundary_and_zero) (field='actual_null_share', layer=1, value=0.999)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1374, in test_v7_planned_actual_each_layer_boundary_and_zero
    self.result(record, "SCREEN-PASS" if value == 0.999 else "INVALID")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'SCREEN-PASS'
- UNIMPLEMENTED
+ SCREEN-PASS


======================================================================
FAIL: test_v7_planned_actual_each_layer_boundary_and_zero (__main__.ReaderValidityTests.test_v7_planned_actual_each_layer_boundary_and_zero) (field='actual_null_share', layer=1, value=0.9989999)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1374, in test_v7_planned_actual_each_layer_boundary_and_zero
    self.result(record, "SCREEN-PASS" if value == 0.999 else "INVALID")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v7_planned_actual_each_layer_boundary_and_zero (__main__.ReaderValidityTests.test_v7_planned_actual_each_layer_boundary_and_zero) (field='actual_null_share', layer=2, value=0.999)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1374, in test_v7_planned_actual_each_layer_boundary_and_zero
    self.result(record, "SCREEN-PASS" if value == 0.999 else "INVALID")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'SCREEN-PASS'
- UNIMPLEMENTED
+ SCREEN-PASS


======================================================================
FAIL: test_v7_planned_actual_each_layer_boundary_and_zero (__main__.ReaderValidityTests.test_v7_planned_actual_each_layer_boundary_and_zero) (field='actual_null_share', layer=2, value=0.9989999)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1374, in test_v7_planned_actual_each_layer_boundary_and_zero
    self.result(record, "SCREEN-PASS" if value == 0.999 else "INVALID")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v7_planned_actual_each_layer_boundary_and_zero (__main__.ReaderValidityTests.test_v7_planned_actual_each_layer_boundary_and_zero) (field='actual_null_share', layer=3, value=0.999)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1374, in test_v7_planned_actual_each_layer_boundary_and_zero
    self.result(record, "SCREEN-PASS" if value == 0.999 else "INVALID")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'SCREEN-PASS'
- UNIMPLEMENTED
+ SCREEN-PASS


======================================================================
FAIL: test_v7_planned_actual_each_layer_boundary_and_zero (__main__.ReaderValidityTests.test_v7_planned_actual_each_layer_boundary_and_zero) (field='actual_null_share', layer=3, value=0.9989999)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1374, in test_v7_planned_actual_each_layer_boundary_and_zero
    self.result(record, "SCREEN-PASS" if value == 0.999 else "INVALID")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v7_planned_actual_each_layer_boundary_and_zero (__main__.ReaderValidityTests.test_v7_planned_actual_each_layer_boundary_and_zero) (field='actual_null_share', layer=4, value=0.999)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1374, in test_v7_planned_actual_each_layer_boundary_and_zero
    self.result(record, "SCREEN-PASS" if value == 0.999 else "INVALID")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'SCREEN-PASS'
- UNIMPLEMENTED
+ SCREEN-PASS


======================================================================
FAIL: test_v7_planned_actual_each_layer_boundary_and_zero (__main__.ReaderValidityTests.test_v7_planned_actual_each_layer_boundary_and_zero) (field='actual_null_share', layer=4, value=0.9989999)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1374, in test_v7_planned_actual_each_layer_boundary_and_zero
    self.result(record, "SCREEN-PASS" if value == 0.999 else "INVALID")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID'
- UNIMPLEMENTED
+ INVALID


======================================================================
FAIL: test_v7_planned_actual_each_layer_boundary_and_zero (__main__.ReaderValidityTests.test_v7_planned_actual_each_layer_boundary_and_zero)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1377, in test_v7_planned_actual_each_layer_boundary_and_zero
    self.result(record, "SCREEN-PASS")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'SCREEN-PASS'
- UNIMPLEMENTED
+ SCREEN-PASS


======================================================================
FAIL: test_v7_untouched_reference_miss_halts_precision_diagnosis (__main__.ReaderValidityTests.test_v7_untouched_reference_miss_halts_precision_diagnosis)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1382, in test_v7_untouched_reference_miss_halts_precision_diagnosis
    self.result(record, "HALTED", advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'HALTED'
- UNIMPLEMENTED
+ HALTED


======================================================================
FAIL: test_v8_string_full_equality_and_one_below_every_arm (__main__.ReaderValidityTests.test_v8_string_full_equality_and_one_below_every_arm)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1397, in test_v8_string_full_equality_and_one_below_every_arm
    self.result(record, "PARTIAL")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'PARTIAL'
- UNIMPLEMENTED
+ PARTIAL


======================================================================
FAIL: test_v9_init_final_tokens_and_each_loss_component (__main__.ReaderValidityTests.test_v9_init_final_tokens_and_each_loss_component)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1407, in test_v9_init_final_tokens_and_each_loss_component
    self.result(record, "INVALID-TRAIN-DEPLOY-GAP", recipe=recipe, advance=False)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 1113, in result
    self.assertEqual(result.get("label"), label)
AssertionError: 'UNIMPLEMENTED' != 'INVALID-TRAIN-DEPLOY-GAP'
- UNIMPLEMENTED
+ INVALID-TRAIN-DEPLOY-GAP


======================================================================
FAIL: test_T11_audit_accepts_every_kind_with_only_kind_specific_fields (__main__.TelemetryCheckContract.test_T11_audit_accepts_every_kind_with_only_kind_specific_fields)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2352, in test_T11_audit_accepts_every_kind_with_only_kind_specific_fields
    self._audit_result(fixture)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2174, in _audit_result
    self.assertEqual(result.get("verdict"), "PASS" if cause is None else "FAIL")
AssertionError: 'UNIMPLEMENTED' != 'PASS'
- UNIMPLEMENTED
+ PASS


======================================================================
FAIL: test_T11_audit_checks_payload_types_for_every_non_answer_kind (__main__.TelemetryCheckContract.test_T11_audit_checks_payload_types_for_every_non_answer_kind) (kind='phase')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2420, in test_T11_audit_checks_payload_types_for_every_non_answer_kind
    self._audit_result(fixture, "MALFORMED")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2174, in _audit_result
    self.assertEqual(result.get("verdict"), "PASS" if cause is None else "FAIL")
AssertionError: 'UNIMPLEMENTED' != 'FAIL'
- UNIMPLEMENTED
+ FAIL


======================================================================
FAIL: test_T11_audit_checks_payload_types_for_every_non_answer_kind (__main__.TelemetryCheckContract.test_T11_audit_checks_payload_types_for_every_non_answer_kind) (kind='opt_step')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2420, in test_T11_audit_checks_payload_types_for_every_non_answer_kind
    self._audit_result(fixture, "MALFORMED")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2174, in _audit_result
    self.assertEqual(result.get("verdict"), "PASS" if cause is None else "FAIL")
AssertionError: 'UNIMPLEMENTED' != 'FAIL'
- UNIMPLEMENTED
+ FAIL


======================================================================
FAIL: test_T11_audit_checks_payload_types_for_every_non_answer_kind (__main__.TelemetryCheckContract.test_T11_audit_checks_payload_types_for_every_non_answer_kind) (kind='target_probs')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2420, in test_T11_audit_checks_payload_types_for_every_non_answer_kind
    self._audit_result(fixture, "MALFORMED")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2174, in _audit_result
    self.assertEqual(result.get("verdict"), "PASS" if cause is None else "FAIL")
AssertionError: 'UNIMPLEMENTED' != 'FAIL'
- UNIMPLEMENTED
+ FAIL


======================================================================
FAIL: test_T11_audit_checks_payload_types_for_every_non_answer_kind (__main__.TelemetryCheckContract.test_T11_audit_checks_payload_types_for_every_non_answer_kind) (kind='write_norms')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2420, in test_T11_audit_checks_payload_types_for_every_non_answer_kind
    self._audit_result(fixture, "MALFORMED")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2174, in _audit_result
    self.assertEqual(result.get("verdict"), "PASS" if cause is None else "FAIL")
AssertionError: 'UNIMPLEMENTED' != 'FAIL'
- UNIMPLEMENTED
+ FAIL


======================================================================
FAIL: test_T11_audit_checks_payload_types_for_every_non_answer_kind (__main__.TelemetryCheckContract.test_T11_audit_checks_payload_types_for_every_non_answer_kind) (kind='logit_lens')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2420, in test_T11_audit_checks_payload_types_for_every_non_answer_kind
    self._audit_result(fixture, "MALFORMED")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2174, in _audit_result
    self.assertEqual(result.get("verdict"), "PASS" if cause is None else "FAIL")
AssertionError: 'UNIMPLEMENTED' != 'FAIL'
- UNIMPLEMENTED
+ FAIL


======================================================================
FAIL: test_T11_audit_complete_answer_keys_pass_and_roundtrip (__main__.TelemetryCheckContract.test_T11_audit_complete_answer_keys_pass_and_roundtrip)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2308, in test_T11_audit_complete_answer_keys_pass_and_roundtrip
    result = self._audit_result(fixture)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2174, in _audit_result
    self.assertEqual(result.get("verdict"), "PASS" if cause is None else "FAIL")
AssertionError: 'UNIMPLEMENTED' != 'PASS'
- UNIMPLEMENTED
+ PASS


======================================================================
FAIL: test_T11_audit_declared_disabled_missing_output_keeps_science_record (__main__.TelemetryCheckContract.test_T11_audit_declared_disabled_missing_output_keeps_science_record)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2486, in test_T11_audit_declared_disabled_missing_output_keeps_science_record
    result = self._audit_result(fixture, "DISABLED", disabled=True)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2174, in _audit_result
    self.assertEqual(result.get("verdict"), "PASS" if cause is None else "FAIL")
AssertionError: 'UNIMPLEMENTED' != 'FAIL'
- UNIMPLEMENTED
+ FAIL


======================================================================
FAIL: test_T11_audit_disabled_marker_does_not_excuse_a_gap_before_later_answers (__main__.TelemetryCheckContract.test_T11_audit_disabled_marker_does_not_excuse_a_gap_before_later_answers)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2507, in test_T11_audit_disabled_marker_does_not_excuse_a_gap_before_later_answers
    self._audit_result(fixture, "MISSING")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2174, in _audit_result
    self.assertEqual(result.get("verdict"), "PASS" if cause is None else "FAIL")
AssertionError: 'UNIMPLEMENTED' != 'FAIL'
- UNIMPLEMENTED
+ FAIL


======================================================================
FAIL: test_T11_audit_disabled_marker_does_not_excuse_mismatching_existing_line (__main__.TelemetryCheckContract.test_T11_audit_disabled_marker_does_not_excuse_mismatching_existing_line)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2498, in test_T11_audit_disabled_marker_does_not_excuse_mismatching_existing_line
    self._audit_result(fixture, "MISMATCH")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2174, in _audit_result
    self.assertEqual(result.get("verdict"), "PASS" if cause is None else "FAIL")
AssertionError: 'UNIMPLEMENTED' != 'FAIL'
- UNIMPLEMENTED
+ FAIL


======================================================================
FAIL: test_T11_audit_duplicate_answer_key_compromises_stage (__main__.TelemetryCheckContract.test_T11_audit_duplicate_answer_key_compromises_stage)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2366, in test_T11_audit_duplicate_answer_key_compromises_stage
    self._audit_result(fixture, "DUPLICATE")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2174, in _audit_result
    self.assertEqual(result.get("verdict"), "PASS" if cause is None else "FAIL")
AssertionError: 'UNIMPLEMENTED' != 'FAIL'
- UNIMPLEMENTED
+ FAIL


======================================================================
FAIL: test_T11_audit_header_must_be_present_initial_and_unique (__main__.TelemetryCheckContract.test_T11_audit_header_must_be_present_initial_and_unique) (variant='absent')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2477, in test_T11_audit_header_must_be_present_initial_and_unique
    self._audit_result(fixture, "MALFORMED")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2174, in _audit_result
    self.assertEqual(result.get("verdict"), "PASS" if cause is None else "FAIL")
AssertionError: 'UNIMPLEMENTED' != 'FAIL'
- UNIMPLEMENTED
+ FAIL


======================================================================
FAIL: test_T11_audit_header_must_be_present_initial_and_unique (__main__.TelemetryCheckContract.test_T11_audit_header_must_be_present_initial_and_unique) (variant='not_first')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2477, in test_T11_audit_header_must_be_present_initial_and_unique
    self._audit_result(fixture, "MALFORMED")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2174, in _audit_result
    self.assertEqual(result.get("verdict"), "PASS" if cause is None else "FAIL")
AssertionError: 'UNIMPLEMENTED' != 'FAIL'
- UNIMPLEMENTED
+ FAIL


======================================================================
FAIL: test_T11_audit_header_must_be_present_initial_and_unique (__main__.TelemetryCheckContract.test_T11_audit_header_must_be_present_initial_and_unique) (variant='repeated')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2477, in test_T11_audit_header_must_be_present_initial_and_unique
    self._audit_result(fixture, "MALFORMED")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2174, in _audit_result
    self.assertEqual(result.get("verdict"), "PASS" if cause is None else "FAIL")
AssertionError: 'UNIMPLEMENTED' != 'FAIL'
- UNIMPLEMENTED
+ FAIL


======================================================================
FAIL: test_T11_audit_header_must_be_present_initial_and_unique (__main__.TelemetryCheckContract.test_T11_audit_header_must_be_present_initial_and_unique) (variant='wrong_schema')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2477, in test_T11_audit_header_must_be_present_initial_and_unique
    self._audit_result(fixture, "MALFORMED")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2174, in _audit_result
    self.assertEqual(result.get("verdict"), "PASS" if cause is None else "FAIL")
AssertionError: 'UNIMPLEMENTED' != 'FAIL'
- UNIMPLEMENTED
+ FAIL


======================================================================
FAIL: test_T11_audit_header_must_be_present_initial_and_unique (__main__.TelemetryCheckContract.test_T11_audit_header_must_be_present_initial_and_unique) (variant='telemetry_not_bool')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2477, in test_T11_audit_header_must_be_present_initial_and_unique
    self._audit_result(fixture, "MALFORMED")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2174, in _audit_result
    self.assertEqual(result.get("verdict"), "PASS" if cause is None else "FAIL")
AssertionError: 'UNIMPLEMENTED' != 'FAIL'
- UNIMPLEMENTED
+ FAIL


======================================================================
FAIL: test_T11_audit_mismatch_compromises_stage_and_requires_telemetry_off_rerun (__main__.TelemetryCheckContract.test_T11_audit_mismatch_compromises_stage_and_requires_telemetry_off_rerun) (field='full')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2360, in test_T11_audit_mismatch_compromises_stage_and_requires_telemetry_off_rerun
    self._audit_result(fixture, "MISMATCH")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2174, in _audit_result
    self.assertEqual(result.get("verdict"), "PASS" if cause is None else "FAIL")
AssertionError: 'UNIMPLEMENTED' != 'FAIL'
- UNIMPLEMENTED
+ FAIL


======================================================================
FAIL: test_T11_audit_mismatch_compromises_stage_and_requires_telemetry_off_rerun (__main__.TelemetryCheckContract.test_T11_audit_mismatch_compromises_stage_and_requires_telemetry_off_rerun) (field='first')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2360, in test_T11_audit_mismatch_compromises_stage_and_requires_telemetry_off_rerun
    self._audit_result(fixture, "MISMATCH")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2174, in _audit_result
    self.assertEqual(result.get("verdict"), "PASS" if cause is None else "FAIL")
AssertionError: 'UNIMPLEMENTED' != 'FAIL'
- UNIMPLEMENTED
+ FAIL


======================================================================
FAIL: test_T11_audit_missing_answer_field_is_malformed (__main__.TelemetryCheckContract.test_T11_audit_missing_answer_field_is_malformed) (field='val')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2402, in test_T11_audit_missing_answer_field_is_malformed
    self._audit_result(fixture, "MALFORMED")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2174, in _audit_result
    self.assertEqual(result.get("verdict"), "PASS" if cause is None else "FAIL")
AssertionError: 'UNIMPLEMENTED' != 'FAIL'
- UNIMPLEMENTED
+ FAIL


======================================================================
FAIL: test_T11_audit_missing_answer_field_is_malformed (__main__.TelemetryCheckContract.test_T11_audit_missing_answer_field_is_malformed) (field='target_ids')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2402, in test_T11_audit_missing_answer_field_is_malformed
    self._audit_result(fixture, "MALFORMED")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2174, in _audit_result
    self.assertEqual(result.get("verdict"), "PASS" if cause is None else "FAIL")
AssertionError: 'UNIMPLEMENTED' != 'FAIL'
- UNIMPLEMENTED
+ FAIL


======================================================================
FAIL: test_T11_audit_missing_answer_field_is_malformed (__main__.TelemetryCheckContract.test_T11_audit_missing_answer_field_is_malformed) (field='first')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2402, in test_T11_audit_missing_answer_field_is_malformed
    self._audit_result(fixture, "MALFORMED")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2174, in _audit_result
    self.assertEqual(result.get("verdict"), "PASS" if cause is None else "FAIL")
AssertionError: 'UNIMPLEMENTED' != 'FAIL'
- UNIMPLEMENTED
+ FAIL


======================================================================
FAIL: test_T11_audit_missing_answer_field_is_malformed (__main__.TelemetryCheckContract.test_T11_audit_missing_answer_field_is_malformed) (field='process')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2402, in test_T11_audit_missing_answer_field_is_malformed
    self._audit_result(fixture, "MALFORMED")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2174, in _audit_result
    self.assertEqual(result.get("verdict"), "PASS" if cause is None else "FAIL")
AssertionError: 'UNIMPLEMENTED' != 'FAIL'
- UNIMPLEMENTED
+ FAIL


======================================================================
FAIL: test_T11_audit_missing_answer_field_is_malformed (__main__.TelemetryCheckContract.test_T11_audit_missing_answer_field_is_malformed) (field='run_id')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2402, in test_T11_audit_missing_answer_field_is_malformed
    self._audit_result(fixture, "MALFORMED")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2174, in _audit_result
    self.assertEqual(result.get("verdict"), "PASS" if cause is None else "FAIL")
AssertionError: 'UNIMPLEMENTED' != 'FAIL'
- UNIMPLEMENTED
+ FAIL


======================================================================
FAIL: test_T11_audit_missing_expected_key_compromises_stage (__main__.TelemetryCheckContract.test_T11_audit_missing_expected_key_compromises_stage)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2372, in test_T11_audit_missing_expected_key_compromises_stage
    self._audit_result(fixture, "MISSING")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2174, in _audit_result
    self.assertEqual(result.get("verdict"), "PASS" if cause is None else "FAIL")
AssertionError: 'UNIMPLEMENTED' != 'FAIL'
- UNIMPLEMENTED
+ FAIL


======================================================================
FAIL: test_T11_audit_missing_file_is_missing_output (__main__.TelemetryCheckContract.test_T11_audit_missing_file_is_missing_output)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2377, in test_T11_audit_missing_file_is_missing_output
    self._audit_result(fixture, "MISSING")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2174, in _audit_result
    self.assertEqual(result.get("verdict"), "PASS" if cause is None else "FAIL")
AssertionError: 'UNIMPLEMENTED' != 'FAIL'
- UNIMPLEMENTED
+ FAIL


======================================================================
FAIL: test_T11_audit_model_free_entrypoint_never_loads_driver_or_harness (__main__.TelemetryCheckContract.test_T11_audit_model_free_entrypoint_never_loads_driver_or_harness)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2518, in test_T11_audit_model_free_entrypoint_never_loads_driver_or_harness
    self._audit_result(fixture)
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2174, in _audit_result
    self.assertEqual(result.get("verdict"), "PASS" if cause is None else "FAIL")
AssertionError: 'UNIMPLEMENTED' != 'PASS'
- UNIMPLEMENTED
+ PASS


======================================================================
FAIL: test_T11_audit_never_mutates_science_records_or_reader_output (__main__.TelemetryCheckContract.test_T11_audit_never_mutates_science_records_or_reader_output)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2327, in test_T11_audit_never_mutates_science_records_or_reader_output
    self.assertEqual(reader_before.get("label"), "SCREEN-PASS")
AssertionError: 'UNIMPLEMENTED' != 'SCREEN-PASS'
- UNIMPLEMENTED
+ SCREEN-PASS


======================================================================
FAIL: test_T11_audit_refuses_existing_audit_without_rewriting_evidence (__main__.TelemetryCheckContract.test_T11_audit_refuses_existing_audit_without_rewriting_evidence)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2525, in test_T11_audit_refuses_existing_audit_without_rewriting_evidence
    with self.assertRaises(ValueError):
AssertionError: ValueError not raised

======================================================================
FAIL: test_T11_audit_rejects_unknown_field_on_every_known_kind (__main__.TelemetryCheckContract.test_T11_audit_rejects_unknown_field_on_every_known_kind) (kind='phase')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2438, in test_T11_audit_rejects_unknown_field_on_every_known_kind
    self._audit_result(fixture, "UNEXPECTED")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2174, in _audit_result
    self.assertEqual(result.get("verdict"), "PASS" if cause is None else "FAIL")
AssertionError: 'UNIMPLEMENTED' != 'FAIL'
- UNIMPLEMENTED
+ FAIL


======================================================================
FAIL: test_T11_audit_rejects_unknown_field_on_every_known_kind (__main__.TelemetryCheckContract.test_T11_audit_rejects_unknown_field_on_every_known_kind) (kind='opt_step')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2438, in test_T11_audit_rejects_unknown_field_on_every_known_kind
    self._audit_result(fixture, "UNEXPECTED")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2174, in _audit_result
    self.assertEqual(result.get("verdict"), "PASS" if cause is None else "FAIL")
AssertionError: 'UNIMPLEMENTED' != 'FAIL'
- UNIMPLEMENTED
+ FAIL


======================================================================
FAIL: test_T11_audit_rejects_unknown_field_on_every_known_kind (__main__.TelemetryCheckContract.test_T11_audit_rejects_unknown_field_on_every_known_kind) (kind='target_probs')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2438, in test_T11_audit_rejects_unknown_field_on_every_known_kind
    self._audit_result(fixture, "UNEXPECTED")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2174, in _audit_result
    self.assertEqual(result.get("verdict"), "PASS" if cause is None else "FAIL")
AssertionError: 'UNIMPLEMENTED' != 'FAIL'
- UNIMPLEMENTED
+ FAIL


======================================================================
FAIL: test_T11_audit_rejects_unknown_field_on_every_known_kind (__main__.TelemetryCheckContract.test_T11_audit_rejects_unknown_field_on_every_known_kind) (kind='write_norms')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2438, in test_T11_audit_rejects_unknown_field_on_every_known_kind
    self._audit_result(fixture, "UNEXPECTED")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2174, in _audit_result
    self.assertEqual(result.get("verdict"), "PASS" if cause is None else "FAIL")
AssertionError: 'UNIMPLEMENTED' != 'FAIL'
- UNIMPLEMENTED
+ FAIL


======================================================================
FAIL: test_T11_audit_rejects_unknown_field_on_every_known_kind (__main__.TelemetryCheckContract.test_T11_audit_rejects_unknown_field_on_every_known_kind) (kind='logit_lens')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2438, in test_T11_audit_rejects_unknown_field_on_every_known_kind
    self._audit_result(fixture, "UNEXPECTED")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2174, in _audit_result
    self.assertEqual(result.get("verdict"), "PASS" if cause is None else "FAIL")
AssertionError: 'UNIMPLEMENTED' != 'FAIL'
- UNIMPLEMENTED
+ FAIL


======================================================================
FAIL: test_T11_audit_strict_json_rejects_nonfinite_and_duplicate_json_fields (__main__.TelemetryCheckContract.test_T11_audit_strict_json_rejects_nonfinite_and_duplicate_json_fields) (text='{bad json}\n')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2459, in test_T11_audit_strict_json_rejects_nonfinite_and_duplicate_json_fields
    self._audit_result(fixture, "MALFORMED")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2174, in _audit_result
    self.assertEqual(result.get("verdict"), "PASS" if cause is None else "FAIL")
AssertionError: 'UNIMPLEMENTED' != 'FAIL'
- UNIMPLEMENTED
+ FAIL


======================================================================
FAIL: test_T11_audit_strict_json_rejects_nonfinite_and_duplicate_json_fields (__main__.TelemetryCheckContract.test_T11_audit_strict_json_rejects_nonfinite_and_duplicate_json_fields) (text='{"kind":"answer","elapsed_s":NaN}\n')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2459, in test_T11_audit_strict_json_rejects_nonfinite_and_duplicate_json_fields
    self._audit_result(fixture, "MALFORMED")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2174, in _audit_result
    self.assertEqual(result.get("verdict"), "PASS" if cause is None else "FAIL")
AssertionError: 'UNIMPLEMENTED' != 'FAIL'
- UNIMPLEMENTED
+ FAIL


======================================================================
FAIL: test_T11_audit_strict_json_rejects_nonfinite_and_duplicate_json_fields (__main__.TelemetryCheckContract.test_T11_audit_strict_json_rejects_nonfinite_and_duplicate_json_fields) (text='{"kind":"answer","elapsed_s":Infinity}\n')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2459, in test_T11_audit_strict_json_rejects_nonfinite_and_duplicate_json_fields
    self._audit_result(fixture, "MALFORMED")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2174, in _audit_result
    self.assertEqual(result.get("verdict"), "PASS" if cause is None else "FAIL")
AssertionError: 'UNIMPLEMENTED' != 'FAIL'
- UNIMPLEMENTED
+ FAIL


======================================================================
FAIL: test_T11_audit_strict_json_rejects_nonfinite_and_duplicate_json_fields (__main__.TelemetryCheckContract.test_T11_audit_strict_json_rejects_nonfinite_and_duplicate_json_fields) (text='{"kind":"answer","kind":"phase"}\n')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2459, in test_T11_audit_strict_json_rejects_nonfinite_and_duplicate_json_fields
    self._audit_result(fixture, "MALFORMED")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2174, in _audit_result
    self.assertEqual(result.get("verdict"), "PASS" if cause is None else "FAIL")
AssertionError: 'UNIMPLEMENTED' != 'FAIL'
- UNIMPLEMENTED
+ FAIL


======================================================================
FAIL: test_T11_audit_unknown_key_or_kind_or_field_is_unexpected (__main__.TelemetryCheckContract.test_T11_audit_unknown_key_or_kind_or_field_is_unexpected) (variant='recipe')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2394, in test_T11_audit_unknown_key_or_kind_or_field_is_unexpected
    self._audit_result(fixture, "UNEXPECTED")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2174, in _audit_result
    self.assertEqual(result.get("verdict"), "PASS" if cause is None else "FAIL")
AssertionError: 'UNIMPLEMENTED' != 'FAIL'
- UNIMPLEMENTED
+ FAIL


======================================================================
FAIL: test_T11_audit_unknown_key_or_kind_or_field_is_unexpected (__main__.TelemetryCheckContract.test_T11_audit_unknown_key_or_kind_or_field_is_unexpected) (variant='arm')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2394, in test_T11_audit_unknown_key_or_kind_or_field_is_unexpected
    self._audit_result(fixture, "UNEXPECTED")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2174, in _audit_result
    self.assertEqual(result.get("verdict"), "PASS" if cause is None else "FAIL")
AssertionError: 'UNIMPLEMENTED' != 'FAIL'
- UNIMPLEMENTED
+ FAIL


======================================================================
FAIL: test_T11_audit_unknown_key_or_kind_or_field_is_unexpected (__main__.TelemetryCheckContract.test_T11_audit_unknown_key_or_kind_or_field_is_unexpected) (variant='subj')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2394, in test_T11_audit_unknown_key_or_kind_or_field_is_unexpected
    self._audit_result(fixture, "UNEXPECTED")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2174, in _audit_result
    self.assertEqual(result.get("verdict"), "PASS" if cause is None else "FAIL")
AssertionError: 'UNIMPLEMENTED' != 'FAIL'
- UNIMPLEMENTED
+ FAIL


======================================================================
FAIL: test_T11_audit_unknown_key_or_kind_or_field_is_unexpected (__main__.TelemetryCheckContract.test_T11_audit_unknown_key_or_kind_or_field_is_unexpected) (variant='template')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2394, in test_T11_audit_unknown_key_or_kind_or_field_is_unexpected
    self._audit_result(fixture, "UNEXPECTED")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2174, in _audit_result
    self.assertEqual(result.get("verdict"), "PASS" if cause is None else "FAIL")
AssertionError: 'UNIMPLEMENTED' != 'FAIL'
- UNIMPLEMENTED
+ FAIL


======================================================================
FAIL: test_T11_audit_unknown_key_or_kind_or_field_is_unexpected (__main__.TelemetryCheckContract.test_T11_audit_unknown_key_or_kind_or_field_is_unexpected) (variant='unknown_kind')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2394, in test_T11_audit_unknown_key_or_kind_or_field_is_unexpected
    self._audit_result(fixture, "UNEXPECTED")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2174, in _audit_result
    self.assertEqual(result.get("verdict"), "PASS" if cause is None else "FAIL")
AssertionError: 'UNIMPLEMENTED' != 'FAIL'
- UNIMPLEMENTED
+ FAIL


======================================================================
FAIL: test_T11_audit_unknown_key_or_kind_or_field_is_unexpected (__main__.TelemetryCheckContract.test_T11_audit_unknown_key_or_kind_or_field_is_unexpected) (variant='unknown_field')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2394, in test_T11_audit_unknown_key_or_kind_or_field_is_unexpected
    self._audit_result(fixture, "UNEXPECTED")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2174, in _audit_result
    self.assertEqual(result.get("verdict"), "PASS" if cause is None else "FAIL")
AssertionError: 'UNIMPLEMENTED' != 'FAIL'
- UNIMPLEMENTED
+ FAIL


======================================================================
FAIL: test_T11_audit_unknown_key_or_kind_or_field_is_unexpected (__main__.TelemetryCheckContract.test_T11_audit_unknown_key_or_kind_or_field_is_unexpected) (variant='header_field')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2394, in test_T11_audit_unknown_key_or_kind_or_field_is_unexpected
    self._audit_result(fixture, "UNEXPECTED")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2174, in _audit_result
    self.assertEqual(result.get("verdict"), "PASS" if cause is None else "FAIL")
AssertionError: 'UNIMPLEMENTED' != 'FAIL'
- UNIMPLEMENTED
+ FAIL


======================================================================
FAIL: test_T11_audit_uses_stage_two_and_three_tags_and_record_paths (__main__.TelemetryCheckContract.test_T11_audit_uses_stage_two_and_three_tags_and_record_paths) (stage=2)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2318, in test_T11_audit_uses_stage_two_and_three_tags_and_record_paths
    result = self._audit_result(fixture)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2174, in _audit_result
    self.assertEqual(result.get("verdict"), "PASS" if cause is None else "FAIL")
AssertionError: 'UNIMPLEMENTED' != 'PASS'
- UNIMPLEMENTED
+ PASS


======================================================================
FAIL: test_T11_audit_uses_stage_two_and_three_tags_and_record_paths (__main__.TelemetryCheckContract.test_T11_audit_uses_stage_two_and_three_tags_and_record_paths) (stage=3)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2318, in test_T11_audit_uses_stage_two_and_three_tags_and_record_paths
    result = self._audit_result(fixture)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2174, in _audit_result
    self.assertEqual(result.get("verdict"), "PASS" if cause is None else "FAIL")
AssertionError: 'UNIMPLEMENTED' != 'PASS'
- UNIMPLEMENTED
+ PASS


======================================================================
FAIL: test_T11_audit_wrong_types_and_nulls_are_malformed (__main__.TelemetryCheckContract.test_T11_audit_wrong_types_and_nulls_are_malformed) (field='full', value=1)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2449, in test_T11_audit_wrong_types_and_nulls_are_malformed
    self._audit_result(fixture, "MALFORMED")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2174, in _audit_result
    self.assertEqual(result.get("verdict"), "PASS" if cause is None else "FAIL")
AssertionError: 'UNIMPLEMENTED' != 'FAIL'
- UNIMPLEMENTED
+ FAIL


======================================================================
FAIL: test_T11_audit_wrong_types_and_nulls_are_malformed (__main__.TelemetryCheckContract.test_T11_audit_wrong_types_and_nulls_are_malformed) (field='first', value='true')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2449, in test_T11_audit_wrong_types_and_nulls_are_malformed
    self._audit_result(fixture, "MALFORMED")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2174, in _audit_result
    self.assertEqual(result.get("verdict"), "PASS" if cause is None else "FAIL")
AssertionError: 'UNIMPLEMENTED' != 'FAIL'
- UNIMPLEMENTED
+ FAIL


======================================================================
FAIL: test_T11_audit_wrong_types_and_nulls_are_malformed (__main__.TelemetryCheckContract.test_T11_audit_wrong_types_and_nulls_are_malformed) (field='subj', value=None)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2449, in test_T11_audit_wrong_types_and_nulls_are_malformed
    self._audit_result(fixture, "MALFORMED")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2174, in _audit_result
    self.assertEqual(result.get("verdict"), "PASS" if cause is None else "FAIL")
AssertionError: 'UNIMPLEMENTED' != 'FAIL'
- UNIMPLEMENTED
+ FAIL


======================================================================
FAIL: test_T11_audit_wrong_types_and_nulls_are_malformed (__main__.TelemetryCheckContract.test_T11_audit_wrong_types_and_nulls_are_malformed) (field='template', value=None)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2449, in test_T11_audit_wrong_types_and_nulls_are_malformed
    self._audit_result(fixture, "MALFORMED")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2174, in _audit_result
    self.assertEqual(result.get("verdict"), "PASS" if cause is None else "FAIL")
AssertionError: 'UNIMPLEMENTED' != 'FAIL'
- UNIMPLEMENTED
+ FAIL


======================================================================
FAIL: test_T11_audit_wrong_types_and_nulls_are_malformed (__main__.TelemetryCheckContract.test_T11_audit_wrong_types_and_nulls_are_malformed) (field='val', value=None)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2449, in test_T11_audit_wrong_types_and_nulls_are_malformed
    self._audit_result(fixture, "MALFORMED")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2174, in _audit_result
    self.assertEqual(result.get("verdict"), "PASS" if cause is None else "FAIL")
AssertionError: 'UNIMPLEMENTED' != 'FAIL'
- UNIMPLEMENTED
+ FAIL


======================================================================
FAIL: test_T11_audit_wrong_types_and_nulls_are_malformed (__main__.TelemetryCheckContract.test_T11_audit_wrong_types_and_nulls_are_malformed) (field='target_ids', value=[True])
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2449, in test_T11_audit_wrong_types_and_nulls_are_malformed
    self._audit_result(fixture, "MALFORMED")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2174, in _audit_result
    self.assertEqual(result.get("verdict"), "PASS" if cause is None else "FAIL")
AssertionError: 'UNIMPLEMENTED' != 'FAIL'
- UNIMPLEMENTED
+ FAIL


======================================================================
FAIL: test_T11_audit_wrong_types_and_nulls_are_malformed (__main__.TelemetryCheckContract.test_T11_audit_wrong_types_and_nulls_are_malformed) (field='generated_ids', value=[3.0])
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2449, in test_T11_audit_wrong_types_and_nulls_are_malformed
    self._audit_result(fixture, "MALFORMED")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2174, in _audit_result
    self.assertEqual(result.get("verdict"), "PASS" if cause is None else "FAIL")
AssertionError: 'UNIMPLEMENTED' != 'FAIL'
- UNIMPLEMENTED
+ FAIL


======================================================================
FAIL: test_T11_audit_wrong_types_and_nulls_are_malformed (__main__.TelemetryCheckContract.test_T11_audit_wrong_types_and_nulls_are_malformed) (field='elapsed_s', value='0')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2449, in test_T11_audit_wrong_types_and_nulls_are_malformed
    self._audit_result(fixture, "MALFORMED")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2174, in _audit_result
    self.assertEqual(result.get("verdict"), "PASS" if cause is None else "FAIL")
AssertionError: 'UNIMPLEMENTED' != 'FAIL'
- UNIMPLEMENTED
+ FAIL


======================================================================
FAIL: test_T11_audit_wrong_types_and_nulls_are_malformed (__main__.TelemetryCheckContract.test_T11_audit_wrong_types_and_nulls_are_malformed) (field='cumulative_s', value=None)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2449, in test_T11_audit_wrong_types_and_nulls_are_malformed
    self._audit_result(fixture, "MALFORMED")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2174, in _audit_result
    self.assertEqual(result.get("verdict"), "PASS" if cause is None else "FAIL")
AssertionError: 'UNIMPLEMENTED' != 'FAIL'
- UNIMPLEMENTED
+ FAIL


======================================================================
FAIL: test_T11_audit_wrong_types_and_nulls_are_malformed (__main__.TelemetryCheckContract.test_T11_audit_wrong_types_and_nulls_are_malformed) (field='t_utc', value=1)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2449, in test_T11_audit_wrong_types_and_nulls_are_malformed
    self._audit_result(fixture, "MALFORMED")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2174, in _audit_result
    self.assertEqual(result.get("verdict"), "PASS" if cause is None else "FAIL")
AssertionError: 'UNIMPLEMENTED' != 'FAIL'
- UNIMPLEMENTED
+ FAIL


======================================================================
FAIL: test_T11_audit_wrong_types_and_nulls_are_malformed (__main__.TelemetryCheckContract.test_T11_audit_wrong_types_and_nulls_are_malformed) (field='run_id', value=None)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2449, in test_T11_audit_wrong_types_and_nulls_are_malformed
    self._audit_result(fixture, "MALFORMED")
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2174, in _audit_result
    self.assertEqual(result.get("verdict"), "PASS" if cause is None else "FAIL")
AssertionError: 'UNIMPLEMENTED' != 'FAIL'
- UNIMPLEMENTED
+ FAIL


======================================================================
FAIL: test_T11_reader_does_not_open_telemetry_or_use_audit_as_gate (__main__.TelemetryCheckContract.test_T11_reader_does_not_open_telemetry_or_use_audit_as_gate)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2533, in test_T11_reader_does_not_open_telemetry_or_use_audit_as_gate
    self.assertEqual(before.get("label"), "SCREEN-PASS")
AssertionError: 'UNIMPLEMENTED' != 'SCREEN-PASS'
- UNIMPLEMENTED
+ SCREEN-PASS


======================================================================
FAIL: test_T8_runner_inert_pristine_stub_never_calls_writer_or_recipe (__main__.TelemetryCheckContract.test_T8_runner_inert_pristine_stub_never_calls_writer_or_recipe)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2246, in test_T8_runner_inert_pristine_stub_never_calls_writer_or_recipe
    self.assertEqual(self._run_check(out, h), 0)
AssertionError: {'schema': 'c10y_directdw_telemetry_inert[409 chars]IED'} != 0

======================================================================
FAIL: test_T8_runner_other_verdicts_exit_zero_and_preserve_verdict (__main__.TelemetryCheckContract.test_T8_runner_other_verdicts_exit_zero_and_preserve_verdict) (verdict='NOT-INERT')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2300, in test_T8_runner_other_verdicts_exit_zero_and_preserve_verdict
    self.assertEqual(self._run_check(out), 0)
AssertionError: {'schema': 'c10y_directdw_telemetry_inert[409 chars]IED'} != 0

======================================================================
FAIL: test_T8_runner_other_verdicts_exit_zero_and_preserve_verdict (__main__.TelemetryCheckContract.test_T8_runner_other_verdicts_exit_zero_and_preserve_verdict) (verdict='NONDETERMINISTIC-BASELINE')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2300, in test_T8_runner_other_verdicts_exit_zero_and_preserve_verdict
    self.assertEqual(self._run_check(out), 0)
AssertionError: {'schema': 'c10y_directdw_telemetry_inert[409 chars]IED'} != 0

======================================================================
FAIL: test_T8_runner_other_verdicts_exit_zero_and_preserve_verdict (__main__.TelemetryCheckContract.test_T8_runner_other_verdicts_exit_zero_and_preserve_verdict) (verdict='INVALID')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2300, in test_T8_runner_other_verdicts_exit_zero_and_preserve_verdict
    self.assertEqual(self._run_check(out), 0)
AssertionError: {'schema': 'c10y_directdw_telemetry_inert[409 chars]IED'} != 0

======================================================================
FAIL: test_T8_runner_preflight_refuses_knob_before_output_creation (__main__.TelemetryCheckContract.test_T8_runner_preflight_refuses_knob_before_output_creation)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2236, in test_T8_runner_preflight_refuses_knob_before_output_creation
    with self.assertRaises(ValueError):
AssertionError: ValueError not raised

======================================================================
FAIL: test_T8_runner_preserves_existing_record (__main__.TelemetryCheckContract.test_T8_runner_preserves_existing_record)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2229, in test_T8_runner_preserves_existing_record
    with self.assertRaises(ValueError):
AssertionError: ValueError not raised

======================================================================
FAIL: test_T8_runner_records_complete_current_identity_and_strict_roundtrip (__main__.TelemetryCheckContract.test_T8_runner_records_complete_current_identity_and_strict_roundtrip)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2256, in test_T8_runner_records_complete_current_identity_and_strict_roundtrip
    self.assertEqual(self._run_check(out), 0)
AssertionError: {'schema': 'c10y_directdw_telemetry_inert[409 chars]IED'} != 0

======================================================================
FAIL: test_T8_runner_rejects_namespace_itself_and_nested_subdirectories (__main__.TelemetryCheckContract.test_T8_runner_rejects_namespace_itself_and_nested_subdirectories) (out='/private/tmp/c10y_build/roots/tmpbjtwthq3/results/c10y_directdw_telemetry_inertness')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2209, in test_T8_runner_rejects_namespace_itself_and_nested_subdirectories
    with self.subTest(out=str(out)), self.assertRaises(ValueError):
AssertionError: ValueError not raised

======================================================================
FAIL: test_T8_runner_rejects_namespace_itself_and_nested_subdirectories (__main__.TelemetryCheckContract.test_T8_runner_rejects_namespace_itself_and_nested_subdirectories) (out='/private/tmp/c10y_build/roots/tmpbjtwthq3/results/c10y_directdw_telemetry_inertness/one/two')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2209, in test_T8_runner_rejects_namespace_itself_and_nested_subdirectories
    with self.subTest(out=str(out)), self.assertRaises(ValueError):
AssertionError: ValueError not raised

======================================================================
FAIL: test_T8_runner_rejects_output_outside_namespace (__main__.TelemetryCheckContract.test_T8_runner_rejects_output_outside_namespace)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2201, in test_T8_runner_rejects_output_outside_namespace
    with self.assertRaises(ValueError):
AssertionError: ValueError not raised

======================================================================
FAIL: test_T8_runner_rejects_relative_output_before_writes (__main__.TelemetryCheckContract.test_T8_runner_rejects_relative_output_before_writes)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2194, in test_T8_runner_rejects_relative_output_before_writes
    with self.assertRaises(ValueError):
AssertionError: ValueError not raised

======================================================================
FAIL: test_T8_runner_rejects_symlink_escape (__main__.TelemetryCheckContract.test_T8_runner_rejects_symlink_escape)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2220, in test_T8_runner_rejects_symlink_escape
    with self.assertRaises(ValueError):
AssertionError: ValueError not raised

======================================================================
FAIL: test_T8_runner_weight_change_is_invalid_exit_two (__main__.TelemetryCheckContract.test_T8_runner_weight_change_is_invalid_exit_two)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 2287, in test_T8_runner_weight_change_is_invalid_exit_two
    self.assertEqual(self._run_check(out, h), 2)
AssertionError: {'schema': 'c10y_directdw_telemetry_inert[409 chars]IED'} != 2

======================================================================
FAIL: test_every_kind_state_preservation_and_volume (__main__.TelemetryTests.test_every_kind_state_preservation_and_volume)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 564, in test_every_kind_state_preservation_and_volume
    self.assertGreater(len(lines),0)
AssertionError: 0 not greater than 0

======================================================================
FAIL: test_inertness_and_drifting_baseline (__main__.TelemetryTests.test_inertness_and_drifting_baseline)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 587, in test_inertness_and_drifting_baseline
    self.assertEqual(result['verdict'],'INERT');self.assertEqual(result['answer_calls'],96);self.assertEqual(result['lens_forwards'],48)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'UNIMPLEMENTED' != 'INERT'
- UNIMPLEMENTED
+ INERT


======================================================================
FAIL: test_invalid_switches_refused_before_write (__main__.TelemetryTests.test_invalid_switches_refused_before_write) (value='0')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 535, in test_invalid_switches_refused_before_write
    with self.subTest(value=value),self.assertRaises(A.Halt): A.telemetry_admission({'C10Y_TELEMETRY':value},1,self.out)
AssertionError: Halt not raised

======================================================================
FAIL: test_invalid_switches_refused_before_write (__main__.TelemetryTests.test_invalid_switches_refused_before_write) (value='true')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 535, in test_invalid_switches_refused_before_write
    with self.subTest(value=value),self.assertRaises(A.Halt): A.telemetry_admission({'C10Y_TELEMETRY':value},1,self.out)
AssertionError: Halt not raised

======================================================================
FAIL: test_invalid_switches_refused_before_write (__main__.TelemetryTests.test_invalid_switches_refused_before_write) (value='')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 535, in test_invalid_switches_refused_before_write
    with self.subTest(value=value),self.assertRaises(A.Halt): A.telemetry_admission({'C10Y_TELEMETRY':value},1,self.out)
AssertionError: Halt not raised

======================================================================
FAIL: test_invalid_switches_refused_before_write (__main__.TelemetryTests.test_invalid_switches_refused_before_write) (value=' 1')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 535, in test_invalid_switches_refused_before_write
    with self.subTest(value=value),self.assertRaises(A.Halt): A.telemetry_admission({'C10Y_TELEMETRY':value},1,self.out)
AssertionError: Halt not raised

======================================================================
FAIL: test_invalid_switches_refused_before_write (__main__.TelemetryTests.test_invalid_switches_refused_before_write) (value='1')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 535, in test_invalid_switches_refused_before_write
    with self.subTest(value=value),self.assertRaises(A.Halt): A.telemetry_admission({'C10Y_TELEMETRY':value},1,self.out)
AssertionError: Halt not raised

======================================================================
FAIL: test_io_failures_disable_once_and_baseexception_propagates (__main__.TelemetryTests.test_io_failures_disable_once_and_baseexception_propagates)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 576, in test_io_failures_disable_once_and_baseexception_propagates
    self.assertEqual(stream.getvalue().count('C10Y_TELEMETRY_DISABLED OSError: init'),1)
AssertionError: 0 != 1

======================================================================
FAIL: test_off_has_no_object_or_directory (__main__.TelemetryTests.test_off_has_no_object_or_directory)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 529, in test_off_has_no_object_or_directory
    self.assertEqual(A.telemetry_admission({},1,self.out),{'telemetry':False,'telemetry_inertness':None})
AssertionError: {'telemetry': True, 'telemetry_inertness': None} != {'telemetry': False, 'telemetry_inertness': None}
- {'telemetry': True, 'telemetry_inertness': None}
?               ^^^

+ {'telemetry': False, 'telemetry_inertness': None}
?               ^^^^


======================================================================
FAIL: test_scorer_ast_and_exact_inputs (__main__.TelemetryTests.test_scorer_ast_and_exact_inputs)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 544, in test_scorer_ast_and_exact_inputs
    self.assertEqual(observed,original);self.assertEqual(capture[0][2],[9,9])
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: False != (True, True)

----------------------------------------------------------------------
Ran 163 tests in 2.611s

FAILED (failures=400)
ISOLATION OWNED LISTING DRIFT: []
ISOLATION OTHER OBSERVED UNATTRIBUTED: []
SYS_MODULES_FORBIDDEN: []
```

Amendment/review RED evidence was also recorded before the corresponding production fix. Exact scratch `run_selected.py <Class-or-Class.test...>` commands selected the classes/tests named in each output. Primary defect regressions are reproduced below; supplemental historical logs remain hashed by the evidence index. No historical partial GREEN is represented as the final full suite.

Evidence: `/private/tmp/c10y_build/pinned_templates_red_assertions.log`; SHA-256 `b1acbf1f9625466ebaeb7fb3bb42b7b02cad2ff9f6fa6e14211013cd660bd050`.

```text
test_changed_template_source_or_stage1_content_halts (c10y_directdw_selftest.PinnedTemplateTests.test_changed_template_source_or_stage1_content_halts) ... FAIL
test_stage1_and_calibration_pin_before_first_engine_call (c10y_directdw_selftest.PinnedTemplateTests.test_stage1_and_calibration_pin_before_first_engine_call) ... FAIL
test_stages2_3_install_stage1_bytes_before_first_engine_use (c10y_directdw_selftest.PinnedTemplateTests.test_stages2_3_install_stage1_bytes_before_first_engine_use) ... ok
test_t8_installs_pin_and_writes_context_before_any_pass (c10y_directdw_selftest.PinnedTemplateTests.test_t8_installs_pin_and_writes_context_before_any_pass) ... FAIL

======================================================================
FAIL: test_changed_template_source_or_stage1_content_halts (c10y_directdw_selftest.PinnedTemplateTests.test_changed_template_source_or_stage1_content_halts)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 3098, in test_changed_template_source_or_stage1_content_halts
    helper=getattr(A,'pinned_templates',None);self.assertTrue(callable(helper),'missing P1 digest checks')
                                              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: False is not true : missing P1 digest checks

======================================================================
FAIL: test_stage1_and_calibration_pin_before_first_engine_call (c10y_directdw_selftest.PinnedTemplateTests.test_stage1_and_calibration_pin_before_first_engine_call)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 3085, in test_stage1_and_calibration_pin_before_first_engine_call
    self.assertEqual(calls,[True]);self.assertEqual(scope['sampled'],[]);self.assertEqual(scope['calls'],[1])
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: Lists differ: [False] != [True]

First differing element 0:
False
True

- [False]
+ [True]

======================================================================
FAIL: test_t8_installs_pin_and_writes_context_before_any_pass (c10y_directdw_selftest.PinnedTemplateTests.test_t8_installs_pin_and_writes_context_before_any_pass)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 3113, in test_t8_installs_pin_and_writes_context_before_any_pass
    try: value=A.telemetry_mps_inertness_check(out,H)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_arms.py", line 1020, in telemetry_mps_inertness_check
    requests=H._ARM_STATE['requests'];batches=[request_batch(H,r,H.get_context_templates(H.model,H.tok)) for r in requests[:6]]
                                              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_arms.py", line 1020, in <listcomp>
    requests=H._ARM_STATE['requests'];batches=[request_batch(H,r,H.get_context_templates(H.model,H.tok)) for r in requests[:6]]
                                                                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<string>", line 6, in get_context_templates
AssertionError: template generation attempted

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 3114, in test_t8_installs_pin_and_writes_context_before_any_pass
    except AssertionError as error: self.fail(str(error))
                                    ^^^^^^^^^^^^^^^^^^^^^
AssertionError: template generation attempted

----------------------------------------------------------------------
Ran 4 tests in 0.088s

FAILED (failures=3)
ISOLATION OWNED LISTING DRIFT: []
ISOLATION OTHER OBSERVED UNATTRIBUTED: []
SYS_MODULES_FORBIDDEN: []
```

Evidence: `/private/tmp/c10y_build/t10_red.log`; SHA-256 `d69601d11279eb7c5372723bdf641feda768d4fd18cd0247003b3b0d7921d28d`.

```text
test_full_stage_counts_and_payload_not_smaller (c10y_directdw_selftest.TelemetryForecastTests.test_full_stage_counts_and_payload_not_smaller) ... FAIL
test_inertness_bytes_once_and_duplicate_nonfinite_refused (c10y_directdw_selftest.TelemetryForecastTests.test_inertness_bytes_once_and_duplicate_nonfinite_refused) ... FAIL
test_on_requires_separate_phase_before_dispatch (c10y_directdw_selftest.TelemetryForecastTests.test_on_requires_separate_phase_before_dispatch) ... FAIL
test_per_kind_measurements_workload_and_sum_enforced (c10y_directdw_selftest.TelemetryForecastTests.test_per_kind_measurements_workload_and_sum_enforced) ... FAIL

======================================================================
FAIL: test_full_stage_counts_and_payload_not_smaller (c10y_directdw_selftest.TelemetryForecastTests.test_full_stage_counts_and_payload_not_smaller)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 3102, in test_full_stage_counts_and_payload_not_smaller
    try: valid=A.budget_gate(forecast,9000.,admission)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
TypeError: budget_gate() takes 2 positional arguments but 3 were given

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 3103, in test_full_stage_counts_and_payload_not_smaller
    except TypeError: self.fail('missing T10 validation')
                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: missing T10 validation

======================================================================
FAIL: test_inertness_bytes_once_and_duplicate_nonfinite_refused (c10y_directdw_selftest.TelemetryForecastTests.test_inertness_bytes_once_and_duplicate_nonfinite_refused)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 3119, in test_inertness_bytes_once_and_duplicate_nonfinite_refused
    try: gate=A.budget_gate(forecast,7200.,admission)
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
TypeError: budget_gate() takes 2 positional arguments but 3 were given

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 3120, in test_inertness_bytes_once_and_duplicate_nonfinite_refused
    except TypeError: self.fail('missing cached verified bytes seam')
                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: missing cached verified bytes seam

======================================================================
FAIL: test_on_requires_separate_phase_before_dispatch (c10y_directdw_selftest.TelemetryForecastTests.test_on_requires_separate_phase_before_dispatch)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 3082, in test_on_requires_separate_phase_before_dispatch
    try: value=A.budget_gate(forecast,7200.,admission)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
TypeError: budget_gate() takes 2 positional arguments but 3 were given

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 3083, in test_on_requires_separate_phase_before_dispatch
    except TypeError: self.fail('budget gate has no telemetry admission seam')
                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: budget gate has no telemetry admission seam

======================================================================
FAIL: test_per_kind_measurements_workload_and_sum_enforced (c10y_directdw_selftest.TelemetryForecastTests.test_per_kind_measurements_workload_and_sum_enforced)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 3088, in test_per_kind_measurements_workload_and_sum_enforced
    try: valid=A.budget_gate(forecast,7200.,admission)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
TypeError: budget_gate() takes 2 positional arguments but 3 were given

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 3089, in test_per_kind_measurements_workload_and_sum_enforced
    except TypeError: self.fail('missing T10 validation')
                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: missing T10 validation

----------------------------------------------------------------------
Ran 4 tests in 0.031s

FAILED (failures=4)
ISOLATION OWNED LISTING DRIFT: []
ISOLATION OTHER OBSERVED UNATTRIBUTED: []
SYS_MODULES_FORBIDDEN: []
```

Evidence: `/private/tmp/c10y_build/transport_launch_delta_red.log`; SHA-256 `783753a9534209b4a47a540ec7c46c814943238d69765114cc7a9e71ef19adcf`.

```text
test_actual_cpu_update_direction_changes_fail_real_reader_repro_gate (c10y_directdw_selftest.TransportTests.test_actual_cpu_update_direction_changes_fail_real_reader_repro_gate) ... ok
test_completed_stage1_runner_to_reader_and_cpu_pt_transport (c10y_directdw_selftest.TransportTests.test_completed_stage1_runner_to_reader_and_cpu_pt_transport) ... ok
test_completed_three_stages_preserve_common_files_and_compute_real_repro (c10y_directdw_selftest.TransportTests.test_completed_three_stages_preserve_common_files_and_compute_real_repro) ... ok
test_real_scored_recipe_accounts_for_scientific_hook_readout_time (c10y_directdw_selftest.TransportTests.test_real_scored_recipe_accounts_for_scientific_hook_readout_time) ... ok
test_requested_stage_forecast_is_checked_before_dispatch_and_worker (c10y_directdw_selftest.TransportTests.test_requested_stage_forecast_is_checked_before_dispatch_and_worker) ... FAIL
test_saved_overlay_hash_is_the_immutable_serialized_bundle (c10y_directdw_selftest.TransportTests.test_saved_overlay_hash_is_the_immutable_serialized_bundle) ... FAIL
test_stage3_pair_mismatch_is_refused_in_parent_before_any_launch_write (c10y_directdw_selftest.TransportTests.test_stage3_pair_mismatch_is_refused_in_parent_before_any_launch_write) ... FAIL
test_stage3_telemetry_setting_cannot_change_after_stage2 (c10y_directdw_selftest.TransportTests.test_stage3_telemetry_setting_cannot_change_after_stage2) ... ok
test_tampered_stage2_pt_refuses_stage3_before_scientific_callbacks (c10y_directdw_selftest.TransportTests.test_tampered_stage2_pt_refuses_stage3_before_scientific_callbacks) ... ok
test_telemetry_off_on_transport_changes_only_T1_fields_at_every_stage (c10y_directdw_selftest.TransportTests.test_telemetry_off_on_transport_changes_only_T1_fields_at_every_stage) ... ok
test_wrong_stage3_predecessor_refuses_in_main_before_harness_or_supervisor (c10y_directdw_selftest.TransportTests.test_wrong_stage3_predecessor_refuses_in_main_before_harness_or_supervisor) ... ok
test_later_stage_cannot_consume_stage1_calibration_measurements (c10y_directdw_selftest.LaunchDeltaTests.test_later_stage_cannot_consume_stage1_calibration_measurements) ... 
  test_later_stage_cannot_consume_stage1_calibration_measurements (c10y_directdw_selftest.LaunchDeltaTests.test_later_stage_cannot_consume_stage1_calibration_measurements) (stage=2) ... FAIL
  test_later_stage_cannot_consume_stage1_calibration_measurements (c10y_directdw_selftest.LaunchDeltaTests.test_later_stage_cannot_consume_stage1_calibration_measurements) (stage=3) ... FAIL
test_norm_readouts_are_inside_writer_wall_clock (c10y_directdw_selftest.LaunchDeltaTests.test_norm_readouts_are_inside_writer_wall_clock) ... FAIL
test_real_iteration_producer_passes_c2_timing_validator (c10y_directdw_selftest.LaunchDeltaTests.test_real_iteration_producer_passes_c2_timing_validator) ... ok
test_supervisor_timeout_records_observed_template_hash_without_child (c10y_directdw_selftest.LaunchDeltaTests.test_supervisor_timeout_records_observed_template_hash_without_child) ... FAIL
test_t8_overlap_audit_precedes_first_forward_and_never_redraws (c10y_directdw_selftest.LaunchDeltaTests.test_t8_overlap_audit_precedes_first_forward_and_never_redraws) ... FAIL

======================================================================
FAIL: test_requested_stage_forecast_is_checked_before_dispatch_and_worker (c10y_directdw_selftest.TransportTests.test_requested_stage_forecast_is_checked_before_dispatch_and_worker)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 3880, in test_requested_stage_forecast_is_checked_before_dispatch_and_worker
    self.assertEqual(ctx.exception.code,'FORECAST-STAGE');prefix.assert_not_called();self.assertFalse(out.exists())
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'UNVERIFIED' != 'FORECAST-STAGE'
- UNVERIFIED
+ FORECAST-STAGE


======================================================================
FAIL: test_saved_overlay_hash_is_the_immutable_serialized_bundle (c10y_directdw_selftest.TransportTests.test_saved_overlay_hash_is_the_immutable_serialized_bundle)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 3905, in test_saved_overlay_hash_is_the_immutable_serialized_bundle
    h=data['H_out'];self.assertEqual(h['overlay_sha256'],A.sha(path))
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: '1111111111111111111111111111111111111111111111111111111111111111' != '7957e694e146e7db6b7e42382f2bf32015b7113fe1f10ca7cb38a6c40a1e3ee2'
- 1111111111111111111111111111111111111111111111111111111111111111
+ 7957e694e146e7db6b7e42382f2bf32015b7113fe1f10ca7cb38a6c40a1e3ee2


======================================================================
FAIL: test_stage3_pair_mismatch_is_refused_in_parent_before_any_launch_write (c10y_directdw_selftest.TransportTests.test_stage3_pair_mismatch_is_refused_in_parent_before_any_launch_write)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 3896, in test_stage3_pair_mismatch_is_refused_in_parent_before_any_launch_write
    code=A.main(['--stage','3','--out',str(out),'--halt-diagnostic',str(self.diagnostic),'--go',str(go),'--spend',str(spend),
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_arms.py", line 1518, in main
    result=supervise(command,args.out,args.halt_diagnostic,cap,stage,env=dict(os.environ,LLMDB_ROOT=str(Path(ROOT).resolve())))
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1124, in __call__
    return self._mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1128, in _mock_call
    return self._execute_mock_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/unittest/mock.py", line 1183, in _execute_mock_call
    raise effect
AssertionError: mismatched pair dispatched

======================================================================
FAIL: test_later_stage_cannot_consume_stage1_calibration_measurements (c10y_directdw_selftest.LaunchDeltaTests.test_later_stage_cannot_consume_stage1_calibration_measurements) (stage=2)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 3986, in test_later_stage_cannot_consume_stage1_calibration_measurements
    with self.subTest(stage=stage): self.assertEqual(A.budget_gate(bad,9000.)['status'],'UNVERIFIED')
                                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'READY' != 'UNVERIFIED'
- READY
+ UNVERIFIED


======================================================================
FAIL: test_later_stage_cannot_consume_stage1_calibration_measurements (c10y_directdw_selftest.LaunchDeltaTests.test_later_stage_cannot_consume_stage1_calibration_measurements) (stage=3)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 3986, in test_later_stage_cannot_consume_stage1_calibration_measurements
    with self.subTest(stage=stage): self.assertEqual(A.budget_gate(bad,9000.)['status'],'UNVERIFIED')
                                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'READY' != 'UNVERIFIED'
- READY
+ UNVERIFIED


======================================================================
FAIL: test_norm_readouts_are_inside_writer_wall_clock (c10y_directdw_selftest.LaunchDeltaTests.test_norm_readouts_are_inside_writer_wall_clock)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 4021, in test_norm_readouts_are_inside_writer_wall_clock
    self.assertEqual(writer.last_trace['wall_clock_s'],3.)
AssertionError: 0.0 != 3.0

======================================================================
FAIL: test_supervisor_timeout_records_observed_template_hash_without_child (c10y_directdw_selftest.LaunchDeltaTests.test_supervisor_timeout_records_observed_template_hash_without_child)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 4011, in test_supervisor_timeout_records_observed_template_hash_without_child
    self.assertEqual(A.strict_load(file).get('context_templates',{}).get('sha256'),A.sha(actual))
AssertionError: None != '9472b663a34cfd9c0bb5448087ae0c2c333b1988b70f211fb2d90baaf8b560b7'

======================================================================
FAIL: test_t8_overlap_audit_precedes_first_forward_and_never_redraws (c10y_directdw_selftest.LaunchDeltaTests.test_t8_overlap_audit_precedes_first_forward_and_never_redraws)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 3992, in test_t8_overlap_audit_precedes_first_forward_and_never_redraws
    self.assertEqual(code,2);self.assertEqual(H.model.forward_inputs,[])
    ^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 0 != 2

----------------------------------------------------------------------
Ran 16 tests in 5.252s

FAILED (failures=8)
ISOLATION OWNED LISTING DRIFT: []
ISOLATION OTHER OBSERVED UNATTRIBUTED: ["results/c10z_astra_attempt2/logs/heartbeat.json", "results/c10z_astra_attempt2/logs"]
SYS_MODULES_FORBIDDEN: []
```

Evidence: `/private/tmp/c10y_build/nm_actual_paths_red.log`; SHA-256 `6286d043e9e207e53b46ccc2ff06d2856d3c3e81c6d3374dacf19b4254527b6d`.

```text
test_nm_decimal_boundary_through_real_reader (c10y_directdw_selftest.LaunchDeltaTests.test_nm_decimal_boundary_through_real_reader) ... 
  test_nm_decimal_boundary_through_real_reader (c10y_directdw_selftest.LaunchDeltaTests.test_nm_decimal_boundary_through_real_reader) (value=0.99) ... FAIL
  test_nm_decimal_boundary_through_real_reader (c10y_directdw_selftest.LaunchDeltaTests.test_nm_decimal_boundary_through_real_reader) (value=1.01) ... FAIL
test_nm_decimal_boundary_through_scientific_hook (c10y_directdw_selftest.LaunchDeltaTests.test_nm_decimal_boundary_through_scientific_hook) ... 
  test_nm_decimal_boundary_through_scientific_hook (c10y_directdw_selftest.LaunchDeltaTests.test_nm_decimal_boundary_through_scientific_hook) (value=0.99) ... FAIL
  test_nm_decimal_boundary_through_scientific_hook (c10y_directdw_selftest.LaunchDeltaTests.test_nm_decimal_boundary_through_scientific_hook) (value=1.01) ... FAIL

======================================================================
FAIL: test_nm_decimal_boundary_through_real_reader (c10y_directdw_selftest.LaunchDeltaTests.test_nm_decimal_boundary_through_real_reader) (value=0.99)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 4011, in test_nm_decimal_boundary_through_real_reader
    with self.subTest(value=value): self.assertEqual('SIZE-UNTESTED' in result['qualifiers'],value not in (0.99,1.01))
                                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: True != False

======================================================================
FAIL: test_nm_decimal_boundary_through_real_reader (c10y_directdw_selftest.LaunchDeltaTests.test_nm_decimal_boundary_through_real_reader) (value=1.01)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 4011, in test_nm_decimal_boundary_through_real_reader
    with self.subTest(value=value): self.assertEqual('SIZE-UNTESTED' in result['qualifiers'],value not in (0.99,1.01))
                                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: True != False

======================================================================
FAIL: test_nm_decimal_boundary_through_scientific_hook (c10y_directdw_selftest.LaunchDeltaTests.test_nm_decimal_boundary_through_scientific_hook) (value=0.99)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 4033, in test_nm_decimal_boundary_through_scientific_hook
    with self.subTest(value=value): self.assertEqual(result['checks']['stored_geometry']['size_match'],value in (0.99,1.01))
                                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: False != True

======================================================================
FAIL: test_nm_decimal_boundary_through_scientific_hook (c10y_directdw_selftest.LaunchDeltaTests.test_nm_decimal_boundary_through_scientific_hook) (value=1.01)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 4033, in test_nm_decimal_boundary_through_scientific_hook
    with self.subTest(value=value): self.assertEqual(result['checks']['stored_geometry']['size_match'],value in (0.99,1.01))
                                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: False != True

----------------------------------------------------------------------
Ran 2 tests in 0.102s

FAILED (failures=4)
ISOLATION OWNED LISTING DRIFT: []
ISOLATION OTHER OBSERVED UNATTRIBUTED: []
SYS_MODULES_FORBIDDEN: []
```

Evidence: `/private/tmp/c10y_build/nm_sum_red_boundary_green.log`; SHA-256 `68236d77a3e106d20819103931043bcd3610eb055a37947b6d8a46acca5332e5`.

```text
test_stored_scale_sum_matches_reader_float64_sum (c10y_directdw_selftest.LaunchDeltaTests.test_stored_scale_sum_matches_reader_float64_sum) ... FAIL
test_nm_decimal_boundary_through_real_reader (c10y_directdw_selftest.LaunchDeltaTests.test_nm_decimal_boundary_through_real_reader) ... ok
test_nm_decimal_boundary_through_scientific_hook (c10y_directdw_selftest.LaunchDeltaTests.test_nm_decimal_boundary_through_scientific_hook) ... ok

======================================================================
FAIL: test_stored_scale_sum_matches_reader_float64_sum (c10y_directdw_selftest.LaunchDeltaTests.test_stored_scale_sum_matches_reader_float64_sum)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 4006, in test_stored_scale_sum_matches_reader_float64_sum
    self.assertEqual(scale,expected)
AssertionError: 0.8333333333333334 != 0.8333333333333333

----------------------------------------------------------------------
Ran 3 tests in 0.189s

FAILED (failures=1)
ISOLATION OWNED LISTING DRIFT: []
ISOLATION OTHER OBSERVED UNATTRIBUTED: []
SYS_MODULES_FORBIDDEN: []
```

The first NM reader fixture used literal `1/1.2` while the recorded norm sum is `math.fsum([.4,.2,.2,.2,.2]) == 1.2000000000000002`. Its initial RED therefore does not independently isolate the reader comparison. After correcting that fixture, both actual boundary paths passed; a separate producer regression exposed the genuine summation mismatch. Final production sums and reader sums now agree. Other fixture corrections changed only synthetic metadata to match stricter production schemas, never weakened gates.

Final light command (no child/full-size tests):

```sh
/opt/homebrew/bin/rtk proxy env TMPDIR=/private/tmp/c10y_build PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python -B /private/tmp/c10y_build/run_light.py > /private/tmp/c10y_build/light_suite_final_2.log 2>&1
```

Evidence: `/private/tmp/c10y_build/light_suite_final_2.log`; SHA-256 `d2095ba9555ce19e453cba086202b7aea28455aebf9fa59d0f09bf3f59303f2b`.

```text
test_all_three_targets_and_baseline_arm_timings_required (c10y_directdw_selftest.CalibrationForecastContractTests.test_all_three_targets_and_baseline_arm_timings_required) ... ok
test_bad_bound_records_return_unverified (c10y_directdw_selftest.CalibrationForecastContractTests.test_bad_bound_records_return_unverified) ... ok
test_calibration_schema_and_c5_completeness (c10y_directdw_selftest.CalibrationForecastContractTests.test_calibration_schema_and_c5_completeness) ... ok
test_cap_types_stage1_limit_and_later_stage_spend (c10y_directdw_selftest.CalibrationForecastContractTests.test_cap_types_stage1_limit_and_later_stage_spend) ... ok
test_each_phase_rejects_wrong_measured_mapping (c10y_directdw_selftest.CalibrationForecastContractTests.test_each_phase_rejects_wrong_measured_mapping) ... ok
test_full_c3_measured_map_and_every_repetition (c10y_directdw_selftest.CalibrationForecastContractTests.test_full_c3_measured_map_and_every_repetition) ... ok
test_independent_bound_requires_explicit_justification (c10y_directdw_selftest.CalibrationForecastContractTests.test_independent_bound_requires_explicit_justification) ... ok
test_input_identity_drift_and_padded_max_are_invalid (c10y_directdw_selftest.CalibrationForecastContractTests.test_input_identity_drift_and_padded_max_are_invalid) ... ok
test_merge_uses_larger_of_two_timed_merges (c10y_directdw_selftest.CalibrationForecastContractTests.test_merge_uses_larger_of_two_timed_merges) ... ok
test_missing_c3_unit_is_not_complete_support (c10y_directdw_selftest.CalibrationForecastContractTests.test_missing_c3_unit_is_not_complete_support) ... ok
test_noncalibration_measured_flag_cannot_replace_supported_bound (c10y_directdw_selftest.CalibrationForecastContractTests.test_noncalibration_measured_flag_cannot_replace_supported_bound) ... ok
test_optimisation_comparable_shape_and_iteration_flags (c10y_directdw_selftest.CalibrationForecastContractTests.test_optimisation_comparable_shape_and_iteration_flags) ... ok
test_optimisation_full_105_attempt_stage_workload (c10y_directdw_selftest.CalibrationForecastContractTests.test_optimisation_full_105_attempt_stage_workload) ... ok
test_optimisation_requires_three_accepted_rows_in_each_check (c10y_directdw_selftest.CalibrationForecastContractTests.test_optimisation_requires_three_accepted_rows_in_each_check) ... ok
test_optimisation_uses_slowest_iteration_not_mean (c10y_directdw_selftest.CalibrationForecastContractTests.test_optimisation_uses_slowest_iteration_not_mean) ... ok
test_original_my_edit_requires_two_distinct_repetitions (c10y_directdw_selftest.CalibrationForecastContractTests.test_original_my_edit_requires_two_distinct_repetitions) ... ok
test_overflow_attempt_is_cited_in_addition_to_six_accepted_rows (c10y_directdw_selftest.CalibrationForecastContractTests.test_overflow_attempt_is_cited_in_addition_to_six_accepted_rows) ... ok
test_prestart_gate_rechecks_schema_and_staleness (c10y_directdw_selftest.CalibrationForecastContractTests.test_prestart_gate_rechecks_schema_and_staleness) ... ok
test_prestart_gate_rejects_forged_or_omitted_measurement (c10y_directdw_selftest.CalibrationForecastContractTests.test_prestart_gate_rejects_forged_or_omitted_measurement) ... ok
test_raw_seconds_sync_status_and_workload_are_typed (c10y_directdw_selftest.CalibrationForecastContractTests.test_raw_seconds_sync_status_and_workload_are_typed) ... ok
test_readout_1380_reserve_and_larger_measured_bound (c10y_directdw_selftest.CalibrationForecastContractTests.test_readout_1380_reserve_and_larger_measured_bound) ... ok
test_calibration_forecast_rejects_partial_and_stale (c10y_directdw_selftest.CalibrationTests.test_calibration_forecast_rejects_partial_and_stale) ... ok
test_calibration_forecast_uses_all_repetitions_no_memory_or_inputs (c10y_directdw_selftest.CalibrationTests.test_calibration_forecast_uses_all_repetitions_no_memory_or_inputs) ... ok
test_calibration_go_spend_caps (c10y_directdw_selftest.CalibrationTests.test_calibration_go_spend_caps) ... ok
test_calibration_prefix_only_and_required_records (c10y_directdw_selftest.CalibrationTests.test_calibration_prefix_only_and_required_records) ... ok
test_calibration_reader_and_context_source_refused (c10y_directdw_selftest.CalibrationTests.test_calibration_reader_and_context_source_refused) ... ok
test_calibration_telemetry_variables_and_existing_directory_refused (c10y_directdw_selftest.CalibrationTests.test_calibration_telemetry_variables_and_existing_directory_refused) ... ok
test_calibration_v4_halt_persists_schedule (c10y_directdw_selftest.CalibrationTests.test_calibration_v4_halt_persists_schedule) ... ok
test_calibration_wrong_namespace_refused (c10y_directdw_selftest.CalibrationTests.test_calibration_wrong_namespace_refused) ... ok
test_frozen_bytes_suite_end (c10y_directdw_selftest.CalibrationTests.test_frozen_bytes_suite_end) ... FAIL
test_calibration_callsite_persists_complete_timing_tags (c10y_directdw_selftest.FinalReviewRegressionTests.test_calibration_callsite_persists_complete_timing_tags) ... ok
test_complete_compile_accounting_drives_ttl_equality (c10y_directdw_selftest.FinalReviewRegressionTests.test_complete_compile_accounting_drives_ttl_equality) ... ok
test_complete_compile_at_actual_scientific_hook_boundary (c10y_directdw_selftest.FinalReviewRegressionTests.test_complete_compile_at_actual_scientific_hook_boundary) ... ok
test_each_telemetry_method_preserves_every_state_and_A_grad (c10y_directdw_selftest.FinalReviewRegressionTests.test_each_telemetry_method_preserves_every_state_and_A_grad) ... ok
test_forecast_aware_first_expensive_action_is_not_entered (c10y_directdw_selftest.FinalReviewRegressionTests.test_forecast_aware_first_expensive_action_is_not_entered) ... ok
test_live_objective_graph_guard_precedes_backward_and_adam (c10y_directdw_selftest.FinalReviewRegressionTests.test_live_objective_graph_guard_precedes_backward_and_adam) ... /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py:3320: UserWarning: Converting a tensor with requires_grad=True to a scalar may lead to unexpected behavior.
Consider using tensor.detach() first. (Triggered internally at /Users/runner/work/pytorch/pytorch/pytorch/torch/csrc/autograd/generated/python_variable_methods.cpp:836.)
  self.assertEqual(opt.state,{});self.assertIsNone(p.grad);self.assertEqual(float(p[0]),1.)
ok
test_merged_fit_reduces_vocabulary_on_cpu_float64 (c10y_directdw_selftest.FinalReviewRegressionTests.test_merged_fit_reduces_vocabulary_on_cpu_float64) ... ok
test_off_scorer_is_original_during_actual_recipe_call (c10y_directdw_selftest.FinalReviewRegressionTests.test_off_scorer_is_original_during_actual_recipe_call) ... ok
test_phase_markers_cover_units_without_changing_operational_calls (c10y_directdw_selftest.FinalReviewRegressionTests.test_phase_markers_cover_units_without_changing_operational_calls) ... ok
test_premerge_parity_cannot_spend_postmerge_reserve (c10y_directdw_selftest.FinalReviewRegressionTests.test_premerge_parity_cannot_spend_postmerge_reserve) ... ok
test_real_writer_durable_merge_precedes_postmerge_readout (c10y_directdw_selftest.FinalReviewRegressionTests.test_real_writer_durable_merge_precedes_postmerge_readout) ... ok
test_real_writer_per_write_line_formula (c10y_directdw_selftest.FinalReviewRegressionTests.test_real_writer_per_write_line_formula) ... ok
test_recorded_contexts_never_sample_even_after_seeding (c10y_directdw_selftest.FinalReviewRegressionTests.test_recorded_contexts_never_sample_even_after_seeding) ... ok
test_actual_launcher_refuses_missing_calibration_before_import (c10y_directdw_selftest.IntegrationTests.test_actual_launcher_refuses_missing_calibration_before_import) ... ok
test_candidate_operations_require_baseline (c10y_directdw_selftest.IntegrationTests.test_candidate_operations_require_baseline) ... ok
test_sequential_capture_matches_original (c10y_directdw_selftest.IntegrationTests.test_sequential_capture_matches_original) ... ok
test_stage_runner_artifacts_feed_real_reader_and_halt_before_candidates (c10y_directdw_selftest.IntegrationTests.test_stage_runner_artifacts_feed_real_reader_and_halt_before_candidates) ... ok
test_stored_control_scale1_identity (c10y_directdw_selftest.IntegrationTests.test_stored_control_scale1_identity) ... ok
test_strict_json_and_immutable_records (c10y_directdw_selftest.IntegrationTests.test_strict_json_and_immutable_records) ... ok
test_three_forced_zero_lr_iterations_and_telemetry_trajectory (c10y_directdw_selftest.IntegrationTests.test_three_forced_zero_lr_iterations_and_telemetry_trajectory) ... ok
test_all_cases_use_base (c10y_directdw_selftest.IsolationTests.test_all_cases_use_base) ... ok
test_live_write_positive_control (c10y_directdw_selftest.IsolationTests.test_live_write_positive_control) ... ok
test_real_dispatch_denied_with_temp_environment (c10y_directdw_selftest.IsolationTests.test_real_dispatch_denied_with_temp_environment) ... ok
test_relative_and_symlink_guard (c10y_directdw_selftest.IsolationTests.test_relative_and_symlink_guard) ... ok
test_selftest_root_refusal (c10y_directdw_selftest.IsolationTests.test_selftest_root_refusal) ... ok
test_later_stage_cannot_consume_stage1_calibration_measurements (c10y_directdw_selftest.LaunchDeltaTests.test_later_stage_cannot_consume_stage1_calibration_measurements) ... ok
test_nm_decimal_boundary_through_real_reader (c10y_directdw_selftest.LaunchDeltaTests.test_nm_decimal_boundary_through_real_reader) ... ok
test_nm_decimal_boundary_through_scientific_hook (c10y_directdw_selftest.LaunchDeltaTests.test_nm_decimal_boundary_through_scientific_hook) ... ok
test_norm_readouts_are_inside_writer_wall_clock (c10y_directdw_selftest.LaunchDeltaTests.test_norm_readouts_are_inside_writer_wall_clock) ... ok
test_real_iteration_producer_passes_c2_timing_validator (c10y_directdw_selftest.LaunchDeltaTests.test_real_iteration_producer_passes_c2_timing_validator) ... ok
test_stored_scale_sum_matches_reader_float64_sum (c10y_directdw_selftest.LaunchDeltaTests.test_stored_scale_sum_matches_reader_float64_sum) ... ok
test_supervisor_timeout_records_observed_template_hash_without_child (c10y_directdw_selftest.LaunchDeltaTests.test_supervisor_timeout_records_observed_template_hash_without_child) ... ok
test_t8_overlap_audit_precedes_first_forward_and_never_redraws (c10y_directdw_selftest.LaunchDeltaTests.test_t8_overlap_audit_precedes_first_forward_and_never_redraws) ... ok
test_context_freeze_and_leakage (c10y_directdw_selftest.LaunchTests.test_context_freeze_and_leakage) ... ok
test_direct_launch_shell_dependencies_are_executable_and_git_100755 (c10y_directdw_selftest.LaunchTests.test_direct_launch_shell_dependencies_are_executable_and_git_100755) ... ok
test_every_inherited_preflight_knob_refused (c10y_directdw_selftest.LaunchTests.test_every_inherited_preflight_knob_refused) ... ok
test_forecast_unverified_and_cap (c10y_directdw_selftest.LaunchTests.test_forecast_unverified_and_cap) ... ok
test_go_spend_and_stage_eligibility (c10y_directdw_selftest.LaunchTests.test_go_spend_and_stage_eligibility) ... ok
test_memory_boundaries (c10y_directdw_selftest.LaunchTests.test_memory_boundaries) ... ok
test_schedule_halt_survives_new_directory (c10y_directdw_selftest.LaunchTests.test_schedule_halt_survives_new_directory) ... ok
test_step_projection_reserves_readout (c10y_directdw_selftest.LaunchTests.test_step_projection_reserves_readout) ... ok
test_wrapper_delegate_dynamic_and_arm_restore (c10y_directdw_selftest.LaunchTests.test_wrapper_delegate_dynamic_and_arm_restore) ... ok
test_anchor_zero_denominator (c10y_directdw_selftest.NumericTests.test_anchor_zero_denominator) ... ok
test_capture_factorization (c10y_directdw_selftest.NumericTests.test_capture_factorization) ... ok
test_control_boundaries (c10y_directdw_selftest.NumericTests.test_control_boundaries) ... ok
test_mps_double_refused (c10y_directdw_selftest.NumericTests.test_mps_double_refused) ... ok
test_null_share_boundaries (c10y_directdw_selftest.NumericTests.test_null_share_boundaries) ... ok
test_size_scales_and_stored_arithmetic (c10y_directdw_selftest.NumericTests.test_size_scales_and_stored_arithmetic) ... ok
test_effective_weight_and_routing_gradient (c10y_directdw_selftest.OptimizerTests.test_effective_weight_and_routing_gradient) ... ok
test_kl_coefficient_once (c10y_directdw_selftest.OptimizerTests.test_kl_coefficient_once) ... ok
test_loss_scale_transaction (c10y_directdw_selftest.OptimizerTests.test_loss_scale_transaction) ... ok
test_microbatch_request_weighting (c10y_directdw_selftest.OptimizerTests.test_microbatch_request_weighting) ... ok
test_request_batch_and_target_only_objective (c10y_directdw_selftest.OptimizerTests.test_request_batch_and_target_only_objective) ... ok
test_sixth_overflow_halts_without_mutation (c10y_directdw_selftest.OptimizerTests.test_sixth_overflow_halts_without_mutation) ... ok
test_stopping_boundaries (c10y_directdw_selftest.OptimizerTests.test_stopping_boundaries) ... ok
test_unknown_hooks_preserved (c10y_directdw_selftest.OptimizerTests.test_unknown_hooks_preserved) ... ok
test_changed_template_source_or_stage1_content_halts (c10y_directdw_selftest.PinnedTemplateTests.test_changed_template_source_or_stage1_content_halts) ... ok
test_stage1_and_calibration_pin_before_first_engine_call (c10y_directdw_selftest.PinnedTemplateTests.test_stage1_and_calibration_pin_before_first_engine_call) ... ok
test_stages2_3_install_stage1_bytes_before_first_engine_use (c10y_directdw_selftest.PinnedTemplateTests.test_stages2_3_install_stage1_bytes_before_first_engine_use) ... ok
test_t8_digest_failure_has_halt_diagnostic_before_scoring (c10y_directdw_selftest.PinnedTemplateTests.test_t8_digest_failure_has_halt_diagnostic_before_scoring) ... ok
test_t8_installs_pin_and_writes_context_before_any_pass (c10y_directdw_selftest.PinnedTemplateTests.test_t8_installs_pin_and_writes_context_before_any_pass) ... ok
test_anchor_comparison_does_not_require_bz_sized_gain (c10y_directdw_selftest.ReaderAttributionTests.test_anchor_comparison_does_not_require_bz_sized_gain) ... ok
test_anchor_missing_invalid_and_unfit_untested (c10y_directdw_selftest.ReaderAttributionTests.test_anchor_missing_invalid_and_unfit_untested) ... ok
test_anchor_sham_descriptor_windows_not_fit_or_validity (c10y_directdw_selftest.ReaderAttributionTests.test_anchor_sham_descriptor_windows_not_fit_or_validity) ... ok
test_control_positive_requires_envelope_gain_fit_locality_and_validity (c10y_directdw_selftest.ReaderAttributionTests.test_control_positive_requires_envelope_gain_fit_locality_and_validity) ... ok
test_hy1_credit_requires_both_processes_attributed (c10y_directdw_selftest.ReaderAttributionTests.test_hy1_credit_requires_both_processes_attributed) ... ok
test_neff_minimum_and_anchor_gap_nine_ten (c10y_directdw_selftest.ReaderAttributionTests.test_neff_minimum_and_anchor_gap_nine_ten) ... ok
test_no_downscale_controls_required_at_actual_ratio_one (c10y_directdw_selftest.ReaderAttributionTests.test_no_downscale_controls_required_at_actual_ratio_one) ... ok
test_size_control_matching_and_direction_boundaries (c10y_directdw_selftest.ReaderAttributionTests.test_size_control_matching_and_direction_boundaries) ... ok
test_total_and_per_layer_growth_trigger_independent_controls (c10y_directdw_selftest.ReaderAttributionTests.test_total_and_per_layer_growth_trigger_independent_controls) ... ok
test_zero_reference_size_normalisation_conservative_provisional (c10y_directdw_selftest.ReaderAttributionTests.test_zero_reference_size_normalisation_conservative_provisional) ... ok
test_cross_shared_hin_and_telemetry_pair_identity (c10y_directdw_selftest.ReaderCrossProcessTests.test_cross_shared_hin_and_telemetry_pair_identity) ... ok
test_r1_cosine_and_distance_every_layer_boundaries (c10y_directdw_selftest.ReaderCrossProcessTests.test_r1_cosine_and_distance_every_layer_boundaries) ... ok
test_r1_required_controls_and_all_arms_independent (c10y_directdw_selftest.ReaderCrossProcessTests.test_r1_required_controls_and_all_arms_independent) ... ok
test_r1_zero_norm_rules_and_baseline_instrument (c10y_directdw_selftest.ReaderCrossProcessTests.test_r1_zero_norm_rules_and_baseline_instrument) ... ok
test_r2_count_spread_five_six (c10y_directdw_selftest.ReaderCrossProcessTests.test_r2_count_spread_five_six) ... ok
test_r3_incorrect_strings_do_not_count_as_disagreement (c10y_directdw_selftest.ReaderCrossProcessTests.test_r3_incorrect_strings_do_not_count_as_disagreement) ... ok
test_r3_keyed_boolean_disagreement_da_plus_three_four (c10y_directdw_selftest.ReaderCrossProcessTests.test_r3_keyed_boolean_disagreement_da_plus_three_four) ... ok
test_regenerated_target_hashes_need_not_match_shared_hin (c10y_directdw_selftest.ReaderCrossProcessTests.test_regenerated_target_hashes_need_not_match_shared_hin) ... ok
test_x1_not_run_halted_and_incomplete_never_fabricated_null (c10y_directdw_selftest.ReaderCrossProcessTests.test_x1_not_run_halted_and_incomplete_never_fabricated_null) ... ok
test_x2_identical_labels_and_union_qualifiers (c10y_directdw_selftest.ReaderCrossProcessTests.test_x2_identical_labels_and_union_qualifiers) ... ok
test_x3_mixed_labels_store_actual_counts (c10y_directdw_selftest.ReaderCrossProcessTests.test_x3_mixed_labels_store_actual_counts) ... ok
test_fit_e2e_minimum_canonical_and_every_stop (c10y_directdw_selftest.ReaderFitAndScreenTests.test_fit_e2e_minimum_canonical_and_every_stop) ... ok
test_fit_per_required_arm_and_apply_stored (c10y_directdw_selftest.ReaderFitAndScreenTests.test_fit_per_required_arm_and_apply_stored) ... ok
test_fit_requires_full_merged_matrix (c10y_directdw_selftest.ReaderFitAndScreenTests.test_fit_requires_full_merged_matrix) ... ok
test_fit_z_mean_and_maximum_boundaries (c10y_directdw_selftest.ReaderFitAndScreenTests.test_fit_z_mean_and_maximum_boundaries) ... ok
test_fit_z_zero_denominator_named_rule (c10y_directdw_selftest.ReaderFitAndScreenTests.test_fit_z_zero_denominator_named_rule) ... ok
test_s1_named_halts_without_screen_label (c10y_directdw_selftest.ReaderFitAndScreenTests.test_s1_named_halts_without_screen_label) ... ok
test_s2_s3_budget_write_boundary (c10y_directdw_selftest.ReaderFitAndScreenTests.test_s2_s3_budget_write_boundary) ... ok
test_s4_fit_precedes_high_count_locality_and_size (c10y_directdw_selftest.ReaderFitAndScreenTests.test_s4_fit_precedes_high_count_locality_and_size) ... ok
test_s5_s7_envelope_and_gain_boundaries (c10y_directdw_selftest.ReaderFitAndScreenTests.test_s5_s7_envelope_and_gain_boundaries) ... ok
test_s6_size_boundary_and_null_first_match (c10y_directdw_selftest.ReaderFitAndScreenTests.test_s6_size_boundary_and_null_first_match) ... ok
test_stage1_recorded_projection_exactly_120_minutes_fits (c10y_directdw_selftest.ReaderFitAndScreenTests.test_stage1_recorded_projection_exactly_120_minutes_fits) ... ok
test_load_calibration_directory_refused_before_read (c10y_directdw_selftest.ReaderLoadTests.test_load_calibration_directory_refused_before_read) ... ok
test_load_does_not_read_telemetry (c10y_directdw_selftest.ReaderLoadTests.test_load_does_not_read_telemetry) ... ok
test_load_later_self_contained_record_uses_own_outcome (c10y_directdw_selftest.ReaderLoadTests.test_load_later_self_contained_record_uses_own_outcome) ... ok
test_load_saved_halt_first_with_missing_science_artifacts (c10y_directdw_selftest.ReaderLoadTests.test_load_saved_halt_first_with_missing_science_artifacts) ... ok
test_load_strict_json_nonfinite_refused (c10y_directdw_selftest.ReaderLoadTests.test_load_strict_json_nonfinite_refused) ... ok
test_existing_arm_missing_metric_is_v13_invalid (c10y_directdw_selftest.ReaderOrderTests.test_existing_arm_missing_metric_is_v13_invalid) ... ok
test_missing_comparators_qualify_without_incomplete (c10y_directdw_selftest.ReaderOrderTests.test_missing_comparators_qualify_without_incomplete) ... ok
test_own_record_and_v5_missing_precede_validity_and_fit (c10y_directdw_selftest.ReaderOrderTests.test_own_record_and_v5_missing_precede_validity_and_fit) ... ok
test_recorded_halt_invalid_and_budget_first (c10y_directdw_selftest.ReaderOrderTests.test_recorded_halt_invalid_and_budget_first) ... ok
test_source_and_prereg_identity_refused (c10y_directdw_selftest.ReaderOrderTests.test_source_and_prereg_identity_refused) ... ok
test_stage1_not_run_controls_and_later_records_not_required (c10y_directdw_selftest.ReaderOrderTests.test_stage1_not_run_controls_and_later_records_not_required) ... ok
test_validity_precedes_fit_and_fit_precedes_counts (c10y_directdw_selftest.ReaderOrderTests.test_validity_precedes_fit_and_fit_precedes_counts) ... ok
test_g1_g2_each_frame_both_sides (c10y_directdw_selftest.ReaderProcessLocalityTests.test_g1_g2_each_frame_both_sides) ... ok
test_g3_g4_g5_unrounded_boundaries (c10y_directdw_selftest.ReaderProcessLocalityTests.test_g3_g4_g5_unrounded_boundaries) ... ok
test_g3_g5_display_rounding_cannot_substitute (c10y_directdw_selftest.ReaderProcessLocalityTests.test_g3_g5_display_rounding_cannot_substitute) ... ok
test_g6_relation_flips_report_only (c10y_directdw_selftest.ReaderProcessLocalityTests.test_g6_relation_flips_report_only) ... ok
test_p1_p2_p3 (c10y_directdw_selftest.ReaderProcessLocalityTests.test_p1_p2_p3) ... ok
test_p4_p5_p7_count_and_gain_boundaries (c10y_directdw_selftest.ReaderProcessLocalityTests.test_p4_p5_p7_count_and_gain_boundaries) ... ok
test_p6_tradeoff_and_p7_null_first_match (c10y_directdw_selftest.ReaderProcessLocalityTests.test_p6_tradeoff_and_p7_null_first_match) ... ok
test_w1_actual_size_boundary_qualifier_preserves_base (c10y_directdw_selftest.ReaderProcessLocalityTests.test_w1_actual_size_boundary_qualifier_preserves_base) ... ok
test_w2_ttl_warning_equality_nonblocking (c10y_directdw_selftest.ReaderProcessLocalityTests.test_w2_ttl_warning_equality_nonblocking) ... ok
test_authored_full_truth_rows_277_289 (c10y_directdw_selftest.ReaderTruthTableTests.test_authored_full_truth_rows_277_289) ... ok
test_authored_stage1_truth_rows_265_276 (c10y_directdw_selftest.ReaderTruthTableTests.test_authored_stage1_truth_rows_265_276) ... ok
test_v10_overflow_retries_five_six (c10y_directdw_selftest.ReaderValidityTests.test_v10_overflow_retries_five_six) ... ok
test_v11_hin_hashes_and_write_trace_required (c10y_directdw_selftest.ReaderValidityTests.test_v11_hin_hashes_and_write_trace_required) ... ok
test_v12_leakage_named_halt (c10y_directdw_selftest.ReaderValidityTests.test_v12_leakage_named_halt) ... ok
test_v13_every_applicable_numeric_family_nonfinite (c10y_directdw_selftest.ReaderValidityTests.test_v13_every_applicable_numeric_family_nonfinite) ... ok
test_v13_nonfinite_unjustified_null_and_typed_integer (c10y_directdw_selftest.ReaderValidityTests.test_v13_nonfinite_unjustified_null_and_typed_integer) ... ok
test_v13_typed_nulls_and_reasons (c10y_directdw_selftest.ReaderValidityTests.test_v13_typed_nulls_and_reasons) ... ok
test_v1_fingerprint_sha_sites_and_full_output (c10y_directdw_selftest.ReaderValidityTests.test_v1_fingerprint_sha_sites_and_full_output) ... ok
test_v2_each_recipe_standing_law5 (c10y_directdw_selftest.ReaderValidityTests.test_v2_each_recipe_standing_law5) ... ok
test_v3_accumulation_raw_cosine_distance_finiteness_and_scope (c10y_directdw_selftest.ReaderValidityTests.test_v3_accumulation_raw_cosine_distance_finiteness_and_scope) ... ok
test_v3_apply_stored_substitutions_not_optimiser_checks (c10y_directdw_selftest.ReaderValidityTests.test_v3_apply_stored_substitutions_not_optimiser_checks) ... ok
test_v3_capture_zero_step_and_executed_loop_raw_values (c10y_directdw_selftest.ReaderValidityTests.test_v3_capture_zero_step_and_executed_loop_raw_values) ... ok
test_v3_check_failure_order_and_scope (c10y_directdw_selftest.ReaderValidityTests.test_v3_check_failure_order_and_scope) ... ok
test_v3_gradient_halvings_hooks_and_smoke_raw_values (c10y_directdw_selftest.ReaderValidityTests.test_v3_gradient_halvings_hooks_and_smoke_raw_values) ... ok
test_v3_missing_required_check_invalid (c10y_directdw_selftest.ReaderValidityTests.test_v3_missing_required_check_invalid) ... ok
test_v3_objective_nll_and_nonzero_kl_raw_boundaries (c10y_directdw_selftest.ReaderValidityTests.test_v3_objective_nll_and_nonzero_kl_raw_boundaries) ... ok
test_v4_a1_a2_and_exact_denominators (c10y_directdw_selftest.ReaderValidityTests.test_v4_a1_a2_and_exact_denominators) ... ok
test_v4_all_inclusive_baseline_endpoints (c10y_directdw_selftest.ReaderValidityTests.test_v4_all_inclusive_baseline_endpoints) ... ok
test_v4_before_candidates_required (c10y_directdw_selftest.ReaderValidityTests.test_v4_before_candidates_required) ... ok
test_v5_candidate_controls_67_68_each_arm (c10y_directdw_selftest.ReaderValidityTests.test_v5_candidate_controls_67_68_each_arm) ... ok
test_v6_overrides_are_exact_sets_not_counts (c10y_directdw_selftest.ReaderValidityTests.test_v6_overrides_are_exact_sets_not_counts) ... ok
test_v7_initial_projector_raw_share_cannot_hide_behind_passed (c10y_directdw_selftest.ReaderValidityTests.test_v7_initial_projector_raw_share_cannot_hide_behind_passed) ... ok
test_v7_planned_actual_each_layer_boundary_and_zero (c10y_directdw_selftest.ReaderValidityTests.test_v7_planned_actual_each_layer_boundary_and_zero) ... ok
test_v7_untouched_reference_miss_halts_precision_diagnosis (c10y_directdw_selftest.ReaderValidityTests.test_v7_untouched_reference_miss_halts_precision_diagnosis) ... ok
test_v8_string_full_equality_and_one_below_every_arm (c10y_directdw_selftest.ReaderValidityTests.test_v8_string_full_equality_and_one_below_every_arm) ... ok
test_v9_init_final_tokens_and_each_loss_component (c10y_directdw_selftest.ReaderValidityTests.test_v9_init_final_tokens_and_each_loss_component) ... ok
test_T11_audit_accepts_every_kind_with_only_kind_specific_fields (c10y_directdw_selftest.TelemetryCheckContract.test_T11_audit_accepts_every_kind_with_only_kind_specific_fields) ... ok
test_T11_audit_checks_payload_types_for_every_non_answer_kind (c10y_directdw_selftest.TelemetryCheckContract.test_T11_audit_checks_payload_types_for_every_non_answer_kind) ... ok
test_T11_audit_complete_answer_keys_pass_and_roundtrip (c10y_directdw_selftest.TelemetryCheckContract.test_T11_audit_complete_answer_keys_pass_and_roundtrip) ... ok
test_T11_audit_declared_disabled_missing_output_keeps_science_record (c10y_directdw_selftest.TelemetryCheckContract.test_T11_audit_declared_disabled_missing_output_keeps_science_record) ... ok
test_T11_audit_disabled_marker_does_not_excuse_a_gap_before_later_answers (c10y_directdw_selftest.TelemetryCheckContract.test_T11_audit_disabled_marker_does_not_excuse_a_gap_before_later_answers) ... ok
test_T11_audit_disabled_marker_does_not_excuse_mismatching_existing_line (c10y_directdw_selftest.TelemetryCheckContract.test_T11_audit_disabled_marker_does_not_excuse_mismatching_existing_line) ... ok
test_T11_audit_duplicate_answer_key_compromises_stage (c10y_directdw_selftest.TelemetryCheckContract.test_T11_audit_duplicate_answer_key_compromises_stage) ... ok
test_T11_audit_header_must_be_present_initial_and_unique (c10y_directdw_selftest.TelemetryCheckContract.test_T11_audit_header_must_be_present_initial_and_unique) ... ok
test_T11_audit_mismatch_compromises_stage_and_requires_telemetry_off_rerun (c10y_directdw_selftest.TelemetryCheckContract.test_T11_audit_mismatch_compromises_stage_and_requires_telemetry_off_rerun) ... ok
test_T11_audit_missing_answer_field_is_malformed (c10y_directdw_selftest.TelemetryCheckContract.test_T11_audit_missing_answer_field_is_malformed) ... ok
test_T11_audit_missing_expected_key_compromises_stage (c10y_directdw_selftest.TelemetryCheckContract.test_T11_audit_missing_expected_key_compromises_stage) ... ok
test_T11_audit_missing_file_is_missing_output (c10y_directdw_selftest.TelemetryCheckContract.test_T11_audit_missing_file_is_missing_output) ... ok
test_T11_audit_model_free_entrypoint_never_loads_driver_or_harness (c10y_directdw_selftest.TelemetryCheckContract.test_T11_audit_model_free_entrypoint_never_loads_driver_or_harness) ... ok
test_T11_audit_never_mutates_science_records_or_reader_output (c10y_directdw_selftest.TelemetryCheckContract.test_T11_audit_never_mutates_science_records_or_reader_output) ... ok
test_T11_audit_refuses_existing_audit_without_rewriting_evidence (c10y_directdw_selftest.TelemetryCheckContract.test_T11_audit_refuses_existing_audit_without_rewriting_evidence) ... ok
test_T11_audit_rejects_unknown_field_on_every_known_kind (c10y_directdw_selftest.TelemetryCheckContract.test_T11_audit_rejects_unknown_field_on_every_known_kind) ... ok
test_T11_audit_strict_json_rejects_nonfinite_and_duplicate_json_fields (c10y_directdw_selftest.TelemetryCheckContract.test_T11_audit_strict_json_rejects_nonfinite_and_duplicate_json_fields) ... ok
test_T11_audit_unknown_key_or_kind_or_field_is_unexpected (c10y_directdw_selftest.TelemetryCheckContract.test_T11_audit_unknown_key_or_kind_or_field_is_unexpected) ... ok
test_T11_audit_uses_stage_two_and_three_tags_and_record_paths (c10y_directdw_selftest.TelemetryCheckContract.test_T11_audit_uses_stage_two_and_three_tags_and_record_paths) ... ok
test_T11_audit_wrong_types_and_nulls_are_malformed (c10y_directdw_selftest.TelemetryCheckContract.test_T11_audit_wrong_types_and_nulls_are_malformed) ... ok
test_T11_reader_does_not_open_telemetry_or_use_audit_as_gate (c10y_directdw_selftest.TelemetryCheckContract.test_T11_reader_does_not_open_telemetry_or_use_audit_as_gate) ... ok
test_T8_runner_inert_pristine_stub_never_calls_writer_or_recipe (c10y_directdw_selftest.TelemetryCheckContract.test_T8_runner_inert_pristine_stub_never_calls_writer_or_recipe) ... ok
test_T8_runner_other_verdicts_exit_zero_and_preserve_verdict (c10y_directdw_selftest.TelemetryCheckContract.test_T8_runner_other_verdicts_exit_zero_and_preserve_verdict) ... ok
test_T8_runner_preflight_refuses_knob_before_output_creation (c10y_directdw_selftest.TelemetryCheckContract.test_T8_runner_preflight_refuses_knob_before_output_creation) ... ok
test_T8_runner_preserves_existing_record (c10y_directdw_selftest.TelemetryCheckContract.test_T8_runner_preserves_existing_record) ... ok
test_T8_runner_records_complete_current_identity_and_strict_roundtrip (c10y_directdw_selftest.TelemetryCheckContract.test_T8_runner_records_complete_current_identity_and_strict_roundtrip) ... ok
test_T8_runner_rejects_namespace_itself_and_nested_subdirectories (c10y_directdw_selftest.TelemetryCheckContract.test_T8_runner_rejects_namespace_itself_and_nested_subdirectories) ... ok
test_T8_runner_rejects_output_outside_namespace (c10y_directdw_selftest.TelemetryCheckContract.test_T8_runner_rejects_output_outside_namespace) ... ok
test_T8_runner_rejects_relative_output_before_writes (c10y_directdw_selftest.TelemetryCheckContract.test_T8_runner_rejects_relative_output_before_writes) ... ok
test_T8_runner_rejects_symlink_escape (c10y_directdw_selftest.TelemetryCheckContract.test_T8_runner_rejects_symlink_escape) ... ok
test_T8_runner_weight_change_is_invalid_exit_two (c10y_directdw_selftest.TelemetryCheckContract.test_T8_runner_weight_change_is_invalid_exit_two) ... ok
test_full_stage_counts_and_payload_not_smaller (c10y_directdw_selftest.TelemetryForecastTests.test_full_stage_counts_and_payload_not_smaller) ... ok
test_inertness_bytes_once_and_duplicate_nonfinite_refused (c10y_directdw_selftest.TelemetryForecastTests.test_inertness_bytes_once_and_duplicate_nonfinite_refused) ... ok
test_on_requires_separate_phase_before_dispatch (c10y_directdw_selftest.TelemetryForecastTests.test_on_requires_separate_phase_before_dispatch) ... ok
test_per_kind_measurements_workload_and_sum_enforced (c10y_directdw_selftest.TelemetryForecastTests.test_per_kind_measurements_workload_and_sum_enforced) ... ok
test_every_kind_state_preservation_and_volume (c10y_directdw_selftest.TelemetryTests.test_every_kind_state_preservation_and_volume) ... ok
test_frozen_hparams_lens_uses_actual_linear_head (c10y_directdw_selftest.TelemetryTests.test_frozen_hparams_lens_uses_actual_linear_head) ... ok
test_inertness_and_drifting_baseline (c10y_directdw_selftest.TelemetryTests.test_inertness_and_drifting_baseline) ... ok
test_invalid_switches_refused_before_write (c10y_directdw_selftest.TelemetryTests.test_invalid_switches_refused_before_write) ... ok
test_io_failures_disable_once_and_baseexception_propagates (c10y_directdw_selftest.TelemetryTests.test_io_failures_disable_once_and_baseexception_propagates) ... ok
test_off_has_no_object_or_directory (c10y_directdw_selftest.TelemetryTests.test_off_has_no_object_or_directory) ... ok
test_scorer_ast_and_exact_inputs (c10y_directdw_selftest.TelemetryTests.test_scorer_ast_and_exact_inputs) ... ok
test_t8_serialized_wrong_answer_is_not_inert (c10y_directdw_selftest.TelemetryTests.test_t8_serialized_wrong_answer_is_not_inert) ... ok
test_telemetry_never_calls_operational_clock_or_writes_input_record (c10y_directdw_selftest.TelemetryTests.test_telemetry_never_calls_operational_clock_or_writes_input_record) ... ok
test_actual_cpu_update_direction_changes_fail_real_reader_repro_gate (c10y_directdw_selftest.TransportTests.test_actual_cpu_update_direction_changes_fail_real_reader_repro_gate) ... ok
test_completed_stage1_runner_to_reader_and_cpu_pt_transport (c10y_directdw_selftest.TransportTests.test_completed_stage1_runner_to_reader_and_cpu_pt_transport) ... ok
test_completed_three_stages_preserve_common_files_and_compute_real_repro (c10y_directdw_selftest.TransportTests.test_completed_three_stages_preserve_common_files_and_compute_real_repro) ... ok
test_real_scored_recipe_accounts_for_scientific_hook_readout_time (c10y_directdw_selftest.TransportTests.test_real_scored_recipe_accounts_for_scientific_hook_readout_time) ... ok
test_requested_stage_forecast_is_checked_before_dispatch_and_worker (c10y_directdw_selftest.TransportTests.test_requested_stage_forecast_is_checked_before_dispatch_and_worker) ... ok
test_saved_overlay_hash_is_the_immutable_serialized_bundle (c10y_directdw_selftest.TransportTests.test_saved_overlay_hash_is_the_immutable_serialized_bundle) ... ok
test_stage3_pair_mismatch_is_refused_in_parent_before_any_launch_write (c10y_directdw_selftest.TransportTests.test_stage3_pair_mismatch_is_refused_in_parent_before_any_launch_write) ... ok
test_stage3_telemetry_setting_cannot_change_after_stage2 (c10y_directdw_selftest.TransportTests.test_stage3_telemetry_setting_cannot_change_after_stage2) ... ok
test_tampered_stage2_pt_refuses_stage3_before_scientific_callbacks (c10y_directdw_selftest.TransportTests.test_tampered_stage2_pt_refuses_stage3_before_scientific_callbacks) ... ok
test_telemetry_off_on_transport_changes_only_T1_fields_at_every_stage (c10y_directdw_selftest.TransportTests.test_telemetry_off_on_transport_changes_only_T1_fields_at_every_stage) ... ok
test_wrong_stage3_predecessor_refuses_in_main_before_harness_or_supervisor (c10y_directdw_selftest.TransportTests.test_wrong_stage3_predecessor_refuses_in_main_before_harness_or_supervisor) ... ok

======================================================================
FAIL: test_frozen_bytes_suite_end (c10y_directdw_selftest.CalibrationTests.test_frozen_bytes_suite_end)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py", line 854, in test_frozen_bytes_suite_end
    self.assertEqual(actual,table)
AssertionError: {'.ve[3578 chars]d': '7c6e52e274e3dbc30cd5123d6b56ae8c9b1dca8c5[19659 chars]162'} != {'.ve[3578 chars]d': '87fe3d5d28c9a51eab4eadfd82cc7175f1a94f723[19659 chars]162'}
Diff is 24189 characters long. Set self.maxDiff to None to see it.

----------------------------------------------------------------------
Ran 226 tests in 22.687s

FAILED (failures=1)
EXCLUDED IntegrationTests.test_native_hanging_worker_deadline_before_and_after_write child process authorization pending
EXCLUDED NumericTests.test_full_size_float64_reductions full-sized CPU work deferred during ASTRA live
EXCLUDED NumericTests.test_gram_norm_dense_reference full-sized CPU work deferred during ASTRA live
{"launched": false, "reasons": ["missing/unknown/duplicate phases"], "status": "UNVERIFIED"}
ISOLATION OWNED LISTING DRIFT: []
ISOLATION OTHER OBSERVED UNATTRIBUTED: ["results/c10z_astra_attempt2/logs/heartbeat.json", "results/c10z_astra_attempt2/logs"]
SYS_MODULES_FORBIDDEN: []
LIGHT_COUNTS {"all": 229, "run": 226, "exclusions": {"NumericTests.test_full_size_float64_reductions": "full-sized CPU work deferred during ASTRA live", "NumericTests.test_gram_norm_dense_reference": "full-sized CPU work deferred during ASTRA live", "IntegrationTests.test_native_hanging_worker_deadline_before_and_after_write": "child process authorization pending"}}
```

**No full final-suite PASS exists.** The 226-case command above exits 1 solely on the literal protected-byte test, which remains enabled. 225 cases passed. All 229 test methods remain in the selftest; only the scratch light selector explicitly excludes the three pending tests. The full selftest refuses its native child test unless `C10Y_ALLOWED_CHILD_TESTS=1`; this flag was never set here. No timeout or elapsed silence was treated as permission.

Final focused production NM/compile/transport evidence:

Evidence: `/private/tmp/c10y_build/transport_launch_delta_green_1.log`; SHA-256 `5192da6f17312f92e43b1bc60f1e88c6a1606c9123f415957df267252d8e3ccf`.

```text
test_actual_cpu_update_direction_changes_fail_real_reader_repro_gate (c10y_directdw_selftest.TransportTests.test_actual_cpu_update_direction_changes_fail_real_reader_repro_gate) ... ok
test_completed_stage1_runner_to_reader_and_cpu_pt_transport (c10y_directdw_selftest.TransportTests.test_completed_stage1_runner_to_reader_and_cpu_pt_transport) ... ok
test_completed_three_stages_preserve_common_files_and_compute_real_repro (c10y_directdw_selftest.TransportTests.test_completed_three_stages_preserve_common_files_and_compute_real_repro) ... ok
test_real_scored_recipe_accounts_for_scientific_hook_readout_time (c10y_directdw_selftest.TransportTests.test_real_scored_recipe_accounts_for_scientific_hook_readout_time) ... ok
test_requested_stage_forecast_is_checked_before_dispatch_and_worker (c10y_directdw_selftest.TransportTests.test_requested_stage_forecast_is_checked_before_dispatch_and_worker) ... ok
test_saved_overlay_hash_is_the_immutable_serialized_bundle (c10y_directdw_selftest.TransportTests.test_saved_overlay_hash_is_the_immutable_serialized_bundle) ... ok
test_stage3_pair_mismatch_is_refused_in_parent_before_any_launch_write (c10y_directdw_selftest.TransportTests.test_stage3_pair_mismatch_is_refused_in_parent_before_any_launch_write) ... ok
test_stage3_telemetry_setting_cannot_change_after_stage2 (c10y_directdw_selftest.TransportTests.test_stage3_telemetry_setting_cannot_change_after_stage2) ... ok
test_tampered_stage2_pt_refuses_stage3_before_scientific_callbacks (c10y_directdw_selftest.TransportTests.test_tampered_stage2_pt_refuses_stage3_before_scientific_callbacks) ... ok
test_telemetry_off_on_transport_changes_only_T1_fields_at_every_stage (c10y_directdw_selftest.TransportTests.test_telemetry_off_on_transport_changes_only_T1_fields_at_every_stage) ... ok
test_wrong_stage3_predecessor_refuses_in_main_before_harness_or_supervisor (c10y_directdw_selftest.TransportTests.test_wrong_stage3_predecessor_refuses_in_main_before_harness_or_supervisor) ... ok
test_later_stage_cannot_consume_stage1_calibration_measurements (c10y_directdw_selftest.LaunchDeltaTests.test_later_stage_cannot_consume_stage1_calibration_measurements) ... ok
test_norm_readouts_are_inside_writer_wall_clock (c10y_directdw_selftest.LaunchDeltaTests.test_norm_readouts_are_inside_writer_wall_clock) ... ok
test_real_iteration_producer_passes_c2_timing_validator (c10y_directdw_selftest.LaunchDeltaTests.test_real_iteration_producer_passes_c2_timing_validator) ... ok
test_supervisor_timeout_records_observed_template_hash_without_child (c10y_directdw_selftest.LaunchDeltaTests.test_supervisor_timeout_records_observed_template_hash_without_child) ... ok
test_t8_overlap_audit_precedes_first_forward_and_never_redraws (c10y_directdw_selftest.LaunchDeltaTests.test_t8_overlap_audit_precedes_first_forward_and_never_redraws) ... ok

----------------------------------------------------------------------
Ran 16 tests in 5.262s

OK
ISOLATION OWNED LISTING DRIFT: []
ISOLATION OTHER OBSERVED UNATTRIBUTED: ["results/c10z_astra_attempt2/logs", "results/c10z_astra_attempt2/logs/heartbeat.json"]
SYS_MODULES_FORBIDDEN: []
```

Evidence: `/private/tmp/c10y_build/nm_actual_paths_green_final.log`; SHA-256 `a7629bad2b6e7b4e048ccf9519fdea9cf818dd6a4940222ddd29233fa28f74c1`.

```text
test_stored_scale_sum_matches_reader_float64_sum (c10y_directdw_selftest.LaunchDeltaTests.test_stored_scale_sum_matches_reader_float64_sum) ... ok
test_nm_decimal_boundary_through_real_reader (c10y_directdw_selftest.LaunchDeltaTests.test_nm_decimal_boundary_through_real_reader) ... ok
test_nm_decimal_boundary_through_scientific_hook (c10y_directdw_selftest.LaunchDeltaTests.test_nm_decimal_boundary_through_scientific_hook) ... ok
test_size_control_matching_and_direction_boundaries (c10y_directdw_selftest.ReaderAttributionTests.test_size_control_matching_and_direction_boundaries) ... ok
test_control_boundaries (c10y_directdw_selftest.NumericTests.test_control_boundaries) ... ok
test_size_scales_and_stored_arithmetic (c10y_directdw_selftest.NumericTests.test_size_scales_and_stored_arithmetic) ... ok

----------------------------------------------------------------------
Ran 6 tests in 0.429s

OK
ISOLATION OWNED LISTING DRIFT: []
ISOLATION OTHER OBSERVED UNATTRIBUTED: []
SYS_MODULES_FORBIDDEN: []
```

Evidence: `/private/tmp/c10y_build/pin_t10_compile_green_2.log`; SHA-256 `6e39976f7416f8b44cbd38fabdcc24f9ee2a3fe8ea195d72295a794187bd3773`.

```text
test_full_stage_counts_and_payload_not_smaller (c10y_directdw_selftest.TelemetryForecastTests.test_full_stage_counts_and_payload_not_smaller) ... ok
test_inertness_bytes_once_and_duplicate_nonfinite_refused (c10y_directdw_selftest.TelemetryForecastTests.test_inertness_bytes_once_and_duplicate_nonfinite_refused) ... ok
test_on_requires_separate_phase_before_dispatch (c10y_directdw_selftest.TelemetryForecastTests.test_on_requires_separate_phase_before_dispatch) ... ok
test_per_kind_measurements_workload_and_sum_enforced (c10y_directdw_selftest.TelemetryForecastTests.test_per_kind_measurements_workload_and_sum_enforced) ... ok
test_changed_template_source_or_stage1_content_halts (c10y_directdw_selftest.PinnedTemplateTests.test_changed_template_source_or_stage1_content_halts) ... ok
test_stage1_and_calibration_pin_before_first_engine_call (c10y_directdw_selftest.PinnedTemplateTests.test_stage1_and_calibration_pin_before_first_engine_call) ... ok
test_stages2_3_install_stage1_bytes_before_first_engine_use (c10y_directdw_selftest.PinnedTemplateTests.test_stages2_3_install_stage1_bytes_before_first_engine_use) ... ok
test_t8_digest_failure_has_halt_diagnostic_before_scoring (c10y_directdw_selftest.PinnedTemplateTests.test_t8_digest_failure_has_halt_diagnostic_before_scoring) ... ok
test_t8_installs_pin_and_writes_context_before_any_pass (c10y_directdw_selftest.PinnedTemplateTests.test_t8_installs_pin_and_writes_context_before_any_pass) ... ok
test_calibration_callsite_persists_complete_timing_tags (c10y_directdw_selftest.FinalReviewRegressionTests.test_calibration_callsite_persists_complete_timing_tags) ... ok
test_complete_compile_accounting_drives_ttl_equality (c10y_directdw_selftest.FinalReviewRegressionTests.test_complete_compile_accounting_drives_ttl_equality) ... ok
test_complete_compile_at_actual_scientific_hook_boundary (c10y_directdw_selftest.FinalReviewRegressionTests.test_complete_compile_at_actual_scientific_hook_boundary) ... ok
test_forecast_aware_first_expensive_action_is_not_entered (c10y_directdw_selftest.FinalReviewRegressionTests.test_forecast_aware_first_expensive_action_is_not_entered) ... ok
test_live_objective_graph_guard_precedes_backward_and_adam (c10y_directdw_selftest.FinalReviewRegressionTests.test_live_objective_graph_guard_precedes_backward_and_adam) ... /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_selftest.py:3264: UserWarning: Converting a tensor with requires_grad=True to a scalar may lead to unexpected behavior.
Consider using tensor.detach() first. (Triggered internally at /Users/runner/work/pytorch/pytorch/pytorch/torch/csrc/autograd/generated/python_variable_methods.cpp:836.)
  self.assertEqual(opt.state,{});self.assertIsNone(p.grad);self.assertEqual(float(p[0]),1.)
ok
test_merged_fit_reduces_vocabulary_on_cpu_float64 (c10y_directdw_selftest.FinalReviewRegressionTests.test_merged_fit_reduces_vocabulary_on_cpu_float64) ... ok
test_off_scorer_is_original_during_actual_recipe_call (c10y_directdw_selftest.FinalReviewRegressionTests.test_off_scorer_is_original_during_actual_recipe_call) ... ok
test_phase_markers_cover_units_without_changing_operational_calls (c10y_directdw_selftest.FinalReviewRegressionTests.test_phase_markers_cover_units_without_changing_operational_calls) ... ok
test_premerge_parity_cannot_spend_postmerge_reserve (c10y_directdw_selftest.FinalReviewRegressionTests.test_premerge_parity_cannot_spend_postmerge_reserve) ... ok
test_real_writer_durable_merge_precedes_postmerge_readout (c10y_directdw_selftest.FinalReviewRegressionTests.test_real_writer_durable_merge_precedes_postmerge_readout) ... ok
test_recorded_contexts_never_sample_even_after_seeding (c10y_directdw_selftest.FinalReviewRegressionTests.test_recorded_contexts_never_sample_even_after_seeding) ... ok

----------------------------------------------------------------------
Ran 20 tests in 1.055s

OK
ISOLATION OWNED LISTING DRIFT: []
ISOLATION OTHER OBSERVED UNATTRIBUTED: []
SYS_MODULES_FORBIDDEN: []
```

Evidence: `/private/tmp/c10y_build/telemetry_state_volume_green.log`; SHA-256 `42ca3ee9f488faf456cbcc58ae2938f4b6afcefa280abd94d3b76e81f46093e4`.

```text
test_each_telemetry_method_preserves_every_state_and_A_grad (c10y_directdw_selftest.FinalReviewRegressionTests.test_each_telemetry_method_preserves_every_state_and_A_grad) ... ok
test_real_writer_per_write_line_formula (c10y_directdw_selftest.FinalReviewRegressionTests.test_real_writer_per_write_line_formula) ... ok

----------------------------------------------------------------------
Ran 2 tests in 0.859s

OK
ISOLATION OWNED LISTING DRIFT: []
ISOLATION OTHER OBSERVED UNATTRIBUTED: []
SYS_MODULES_FORBIDDEN: []
```

Transport scope: the real driver `run`, file persistence, source binding, target/actual-update PT serialisation, model-free reader, stage predecessor/rerun rules and actual tensor R1 are exercised. The tiny CPU update payloads are real; scientific gate/metric records and the declared MPS environment in these fixtures are explicitly synthetic (`fixture_scope`). They are code transport evidence only. The native supervisor regression above uses a mocked process; it is not evidence that an actual blocked child was killed.

## Mutation table

Final serial light mutation command:

```sh
/opt/homebrew/bin/rtk proxy env TMPDIR=/private/tmp/c10y_build PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python -B /private/tmp/c10y_build/mutations.py > /private/tmp/c10y_build/mutations_light_final.log 2>&1
```

Evidence: `/private/tmp/c10y_build/mutations_light_final.log`; SHA-256 `d35d60e272d9bec70d0dd7b37681c77e81d61c4755f587953f82c45b7b11f55d`.

```text
M1 KILLED_ASSERTION
M2 KILLED_ASSERTION
M3 KILLED_ASSERTION
M4 KILLED_ASSERTION
M5 KILLED_ASSERTION
M6 KILLED_ASSERTION
M7 KILLED_ASSERTION
M8 KILLED_ASSERTION
M9 KILLED_ASSERTION
M10 KILLED_ASSERTION
M11 KILLED_ASSERTION
M12 KILLED_ASSERTION
M13 KILLED_ASSERTION
M15 KILLED_ASSERTION
M16 KILLED_ASSERTION
M17 KILLED_ASSERTION
M18 KILLED_ASSERTION
M19 KILLED_ASSERTION
M20 KILLED_ASSERTION
M21 KILLED_ASSERTION
M22 KILLED_ASSERTION
MUTATION_RESULTS /private/tmp/c10y_build/mutations_20261008T124348096906Z_11180/results.json
SOURCE_SHA_RESTORED True
```

| Mutant | Final outcome | Failing tests | Restored source SHA |
|---|---|---|---|
| M1 V4 first lower bound 42 to 41 | KILLED_ASSERTION | `ReaderValidityTests.test_v4_all_inclusive_baseline_endpoints` | `f8d2598b01956be3ad390c76b2336ae1398e77d05045fb8870a3ae6e42cb2e78` |
| M2 screen floor 19 to 18 | KILLED_ASSERTION | `ReaderFitAndScreenTests.test_s5_s7_envelope_and_gain_boundaries` | `f8d2598b01956be3ad390c76b2336ae1398e77d05045fb8870a3ae6e42cb2e78` |
| M3 FIT-E2E equality fails | KILLED_ASSERTION | `ReaderFitAndScreenTests.test_fit_e2e_minimum_canonical_and_every_stop` | `f8d2598b01956be3ad390c76b2336ae1398e77d05045fb8870a3ae6e42cb2e78` |
| M4 W1 equality becomes large | KILLED_ASSERTION | `ReaderFitAndScreenTests.test_s6_size_boundary_and_null_first_match`; `ReaderProcessLocalityTests.test_w1_actual_size_boundary_qualifier_preserves_base` | `f8d2598b01956be3ad390c76b2336ae1398e77d05045fb8870a3ae6e42cb2e78` |
| M5 R1 distance 0.10 to 0.11 | KILLED_ASSERTION | `ReaderCrossProcessTests.test_r1_cosine_and_distance_every_layer_boundaries` | `f8d2598b01956be3ad390c76b2336ae1398e77d05045fb8870a3ae6e42cb2e78` |
| M6 T1 anchor gap 10 to 9 | KILLED_ASSERTION | `ReaderAttributionTests.test_neff_minimum_and_anchor_gap_nine_ten` | `f8d2598b01956be3ad390c76b2336ae1398e77d05045fb8870a3ae6e42cb2e78` |
| M7 EXCEEDS-TTL blocks advancement | KILLED_ASSERTION | `ReaderProcessLocalityTests.test_w2_ttl_warning_equality_nonblocking` | `f8d2598b01956be3ad390c76b2336ae1398e77d05045fb8870a3ae6e42cb2e78` |
| M8 NM also applied when NB <= NA | KILLED_ASSERTION | `NumericTests.test_size_scales_and_stored_arithmetic` | `206710d02c6cc8580a14391cc94c5280db63bc1a9de0177bb3b6a15951c29416` |
| M9 overflow increments Adam counter without updating parameter/moment values | KILLED_ASSERTION | `OptimizerTests.test_loss_scale_transaction`; `OptimizerTests.test_sixth_overflow_halts_without_mutation` | `206710d02c6cc8580a14391cc94c5280db63bc1a9de0177bb3b6a15951c29416` |
| M10 routing mask removed | KILLED_ASSERTION | `OptimizerTests.test_effective_weight_and_routing_gradient` | `206710d02c6cc8580a14391cc94c5280db63bc1a9de0177bb3b6a15951c29416` |
| M11 KL coefficient applied twice | KILLED_ASSERTION | `OptimizerTests.test_kl_coefficient_once` | `206710d02c6cc8580a14391cc94c5280db63bc1a9de0177bb3b6a15951c29416` |
| M12 unverified budget support passes | KILLED_ASSERTION | `LaunchTests.test_forecast_unverified_and_cap`; `CalibrationForecastContractTests.test_independent_bound_requires_explicit_justification` | `206710d02c6cc8580a14391cc94c5280db63bc1a9de0177bb3b6a15951c29416` |
| M13 candidate path falsely admitted before LAW#3 | KILLED_ASSERTION | `IntegrationTests.test_candidate_operations_require_baseline` | `206710d02c6cc8580a14391cc94c5280db63bc1a9de0177bb3b6a15951c29416` |
| M14 float64 helper uses fp32 | SKIPPED_HEAVY | `NumericTests.test_full_size_float64_reductions` | `UNRUN` |
| M15 telemetry on when absent | KILLED_ASSERTION | `TelemetryTests.test_off_has_no_object_or_directory` | `206710d02c6cc8580a14391cc94c5280db63bc1a9de0177bb3b6a15951c29416` |
| M16 telemetry adds record key | KILLED_ASSERTION | `TelemetryTests.test_telemetry_never_calls_operational_clock_or_writes_input_record` | `206710d02c6cc8580a14391cc94c5280db63bc1a9de0177bb3b6a15951c29416` |
| M17 observed scorer installed while off | KILLED_ASSERTION | `FinalReviewRegressionTests.test_off_scorer_is_original_during_actual_recipe_call` | `206710d02c6cc8580a14391cc94c5280db63bc1a9de0177bb3b6a15951c29416` |
| M18 telemetry uses supervisor/stage clock | KILLED_ASSERTION | `TelemetryTests.test_telemetry_never_calls_operational_clock_or_writes_input_record` | `206710d02c6cc8580a14391cc94c5280db63bc1a9de0177bb3b6a15951c29416` |
| M19 telemetry catches BaseException | KILLED_ASSERTION | `TelemetryTests.test_io_failures_disable_once_and_baseexception_propagates` | `206710d02c6cc8580a14391cc94c5280db63bc1a9de0177bb3b6a15951c29416` |
| M20 selftest audit installation omitted | KILLED_ASSERTION | `IsolationTests.test_live_write_positive_control` | `02977e73ea0a6d70b642112d025a2e274060d3334a339baad149a799916db3c1` |
| M21 selftest accepts non-temp root | KILLED_ASSERTION | `IsolationTests.test_selftest_root_refusal` | `206710d02c6cc8580a14391cc94c5280db63bc1a9de0177bb3b6a15951c29416` |
| M22 G3 accepts rounded described_as | KILLED_ASSERTION | `ReaderProcessLocalityTests.test_g3_g5_display_rounding_cannot_substitute` | `f8d2598b01956be3ad390c76b2336ae1398e77d05045fb8870a3ae6e42cb2e78` |

21/21 executed mutants died at behavioral assertions on the final source and were SHA-restored. M14 was explicitly SKIPPED_HEAVY, not a kill. Initial M13 survived because the test accepted any HALT, including a later ARM-ATTRIBUTION failure; strengthening it to require LAW#3-BEFORE-CANDIDATES killed M13. Original survivor evidence is retained. The mutation harness initially rejected dill’s `/dev/null` open; its explicit null-device exception permits no persistent filesystem write and does not loosen the real-tree/source-lease guards. That infrastructure error was not counted as a kill. No mutations imported transformers/datasets/harness, spawned children, or ran MPS.

## Scope evidence

The embedded status/listing snapshots were taken during shared live activity before the report's final publication. A post-publication repeat is retained in `/private/tmp/c10y_build/after/`, including the report byte SHA in `r2_sha256.json`. Live heartbeat/log listing changes are observed and unattributed; these snapshots do not assert a globally idle tree.

Before-state: git porcelain; all five R2 paths absent; 192 initial protected-file hashes; 7089 results/architecture-profile listing entries. Original table `/private/tmp/c10y_build/before/r5_sha256.json` is retained. Amendment C and then P were explicit Program pin changes, retained in separate post-amendment tables. The latest table adds the benchmark source required by P and contains 193 files. Final comparison: **190/193 byte-identical; 3 differ.** Core engine, C10Y prereg under its authorised pin, frozen harness, hparams/configs, engine fingerprint tool and benchmark source all match. R5’s literal whole-table equality remains FAILED; Program attribution/rebaseline permission was requested and not received. Do not mistake a clean core git diff for whole protected-table equality.

```json
{
  "docs/C10Z_ASTRA_PREREG.md": {
    "after": "7c6e52e274e3dbc30cd5123d6b56ae8c9b1dca8c5e7507ff7be15d57e845059d",
    "before": "87fe3d5d28c9a51eab4eadfd82cc7175f1a94f723f25f31658c5e1aeaf628b87"
  },
  "experiments/track_c/c10z_astra_arms.py": {
    "after": "ab6f5c809d8187f4e5eb39e9cc6fbf40b6e357b2ecf5b18ecc887e05de7adebc",
    "before": "806a9b4d417261945359d45db8c2f8513e4f5a2f3fafaf0b7cefe3a8d5ec3304"
  },
  "tools/dashboard_experiment.py": {
    "after": "3e0685b7ddf3801d6c85801bc9f4969206dcfb18787b6fc76195d98cfdd82dbc",
    "before": "59648b47a48e2f0afd8a00166d3c77199157bc78e13454eaa5bea768055cdfd7"
  }
}
```

Those three files were not written by this build. Concurrent Program ownership is plausible from the live ASTRA/dashboard activity but independently UNVERIFIED until the Program answers. Their original/current hashes are retained; no historical record or baseline was silently repaired. Other global status/listing changes are observed and unattributed. The in-process suite guards and independent mutation guard had no permitted write path to those files.

Protected core command, before and after:

```sh
/opt/homebrew/bin/rtk proxy git -C /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a diff --quiet -- memit_dry_run docs/C10Y_DIRECTDW_PREREG.md experiments/track_c/c10e_bandknob.py
# exit 0
```

Read-only engine command, with ROOT explicitly set (an earlier environment-inherited probe addressed the outer clone; identical bytes were observed there, but the command below verifies W):

```sh
/opt/homebrew/bin/rtk proxy env LLMDB_ROOT=/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a TMPDIR=/private/tmp/c10y_build PYTHONDONTWRITEBYTECODE=1 /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python -B /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/engine_fingerprint.py
```

Evidence: `/private/tmp/c10y_build/after/engine_fingerprint_root.log`; SHA-256 `15aef4acf47eb374ea93cf4f949a0022a287f56b646ac2b139f599af98b355e3`.

```text
engine fingerprint PASS: /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/memit_dry_run/memit/memit/memit_main.py
  sha256   d941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65  (expected d941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65; pod-era 5c0c706a…)
  _cov_cpu 3  (expected 3)
```

Current git worktree root remained `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a`, branch `worktree-c10k-route-a`. Read-only status diff:

```diff
--- before/git_status.txt
+++ after/git_status.txt
@@ -1,33 +1,51 @@
  M .gitignore
- M experiments/track_c/c10w_oracle_eval.py
- M experiments/track_c/c10w_oracle_selftest.py
- M experiments/track_c/c10z_astra_arms.py
- M experiments/track_c/c10z_astra_read.py
- M experiments/track_c/c10z_astra_selftest.py
- M tools/c10w_p2_gate.py
- M tools/run_c10w_p2.sh
- M tools/run_c10w_p2_stage.sh
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
@@ -61,8 +79,8 @@
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

Whole-session listing is different from each test-run backstop: the one authorised C10Y report is new; test-run owned drift was always `[]`. No real C10Y run/calibration/T8 directory or diagnostic was created. Whole-session other changes are printed below without attribution; full size/mtime data is in `/private/tmp/c10y_build/after/listing_diff.json`.

```json
{
  "c10y_report_and_owned_observed": {
    "results/c10y_calib_amend_astra.md": {
      "after": [
        4551,
        1791453907087508359
      ],
      "before": null
    },
    "results/c10y_calib_amend_astra_delta.md": {
      "after": [
        1690,
        1791454245738108549
      ],
      "before": null
    },
    "results/c10y_directdw_codex_build.md": {
      "after": [
        13179,
        1791463018011140757
      ],
      "before": null
    }
  },
  "other_observed_unattributed_paths": [
    "architecture_profile/c10z_astra_halt_diagnostic.json",
    "architecture_profile/c10z_astra_halt_diagnostic_20261008T124710.311412Z.json",
    "results/c10w_oracle/p2_20261008T034226_086980Z",
    "results/c10w_oracle/p2_20261008T034226_086980Z/eval.json",
    "results/c10w_oracle/p2_20261008T034226_086980Z/p2-eval.log",
    "results/c10w_oracle/p2_20261008T034226_086980Z/verdict.json",
    "results/c10w_oracle_logs",
    "results/c10w_oracle_logs/p2-eval.log",
    "results/c10w_oracle_logs/p2-read-attempt2.json",
    "results/c10w_oracle_logs/p2-reattempt-coordinator.20261008T030455.59886.log",
    "results/c10w_p2_reading_astra.md",
    "results/c10x_enginepath_codex_build.md",
    "results/c10z_astra",
    "results/c10z_astra/halt_p1.json",
    "results/c10z_astra/logs",
    "results/c10z_astra/logs/heartbeat.json",
    "results/c10z_astra/logs/resident_p1.log",
    "results/c10z_astra/pass_p1.json",
    "results/c10z_astra/pristine_hash.json",
    "results/c10z_astra/run.json",
    "results/c10z_astra_attempt2",
    "results/c10z_astra_attempt2/context_templates.json",
    "results/c10z_astra_attempt2/halt_p1.json",
    "results/c10z_astra_attempt2/logs",
    "results/c10z_astra_attempt2/logs/heartbeat.json",
    "results/c10z_astra_attempt2/logs/resident_p1.log",
    "results/c10z_astra_attempt2/pristine_hash.json",
    "results/c10z_astra_attempt2/run.json",
    "results/c10z_astra_attempt2_chain.log",
    "results/c10z_astra_benchmark",
    "results/c10z_astra_benchmark/20261008T104535Z",
    "results/c10z_astra_benchmark/20261008T104535Z/benchmark.json",
    "results/c10z_astra_benchmark/20261008T104535Z/benchmark.log",
    "results/c10z_astra_benchmark/20261008T104535Z/heartbeat.json",
    "results/c10z_astra_benchmark/20261008T104535Z/run.json",
    "results/c10z_astra_benchmark/20261008T104535Z/svd_child.json",
    "results/c10z_astra_benchmark/20261008T121345Z",
    "results/c10z_astra_benchmark/20261008T121345Z/benchmark.json",
    "results/c10z_astra_benchmark/20261008T121345Z/benchmark.log",
    "results/c10z_astra_benchmark/20261008T121345Z/heartbeat.json",
    "results/c10z_astra_benchmark/20261008T121345Z/run.json",
    "results/c10z_astra_benchmark/20261008T121345Z/svd_child.json",
    "results/c10z_astra_benchmark_20261008T104535Z.log",
    "results/c10z_astra_benchmark_20261008T121345Z.log",
    "results/c10z_astra_chain.launchfail126.log",
    "results/c10z_astra_chain.log",
    "results/c10z_astra_go_record.json",
    "results/c10z_astra_go_record_attempt2.json",
    "results/c10z_astra_v4_diagnosis.md",
    "results/c10z_build_codex_impl.md",
    "results/c10z_v4pin_code_astra.md",
    "results/labviz",
    "results/labviz/images_manifest.json",
    "results/labviz/review",
    "results/labviz/review/20261008T102337237Z",
    "results/labviz/review/20261008T102337237Z/browser-tests.json",
    "results/labviz/review/20261008T102337237Z/chromium-desktop-200pct-compare.png",
    "results/labviz/review/20261008T102337237Z/chromium-desktop-200pct-evaluations.png",
    "results/labviz/review/20261008T102337237Z/chromium-desktop-200pct-learn.png",
    "results/labviz/review/20261008T102337237Z/chromium-desktop-200pct-line-c10.png",
    "results/labviz/review/20261008T102337237Z/chromium-desktop-200pct-line-d1.png",
    "results/labviz/review/20261008T102337237Z/chromium-desktop-200pct-line-f1-conditions.png",
    "results/labviz/review/20261008T102337237Z/chromium-desktop-200pct-line-t-branch.png",
    "results/labviz/review/20261008T102337237Z/chromium-desktop-200pct-line-viability.png",
    "results/labviz/review/20261008T102337237Z/chromium-desktop-200pct-map-c10-focus.png",
    "results/labviz/review/20261008T102337237Z/chromium-desktop-200pct-map-c10-greyscale.png",
    "results/labviz/review/20261008T102337237Z/chromium-desktop-200pct-map.png",
    "results/labviz/review/20261008T102337237Z/chromium-desktop-200pct-model-2d.png",
    "results/labviz/review/20261008T102337237Z/chromium-desktop-200pct-model-3d.png",
    "results/labviz/review/20261008T102337237Z/chromium-desktop-200pct-model-mistral.png",
    "results/labviz/review/20261008T102337237Z/chromium-desktop-200pct-run-c10v-b-a7.png",
    "results/labviz/review/20261008T102337237Z/chromium-desktop-200pct-run-g6.1.png",
    "results/labviz/review/20261008T102337237Z/chromium-desktop-compare.png",
    "results/labviz/review/20261008T102337237Z/chromium-desktop-evaluations.png",
    "results/labviz/review/20261008T102337237Z/chromium-desktop-learn.png",
    "results/labviz/review/20261008T102337237Z/chromium-desktop-line-c10.png",
    "results/labviz/review/20261008T102337237Z/chromium-desktop-line-d1.png",
    "results/labviz/review/20261008T102337237Z/chromium-desktop-line-f1-conditions.png",
    "results/labviz/review/20261008T102337237Z/chromium-desktop-line-t-branch.png",
    "results/labviz/review/20261008T102337237Z/chromium-desktop-line-viability.png",
    "results/labviz/review/20261008T102337237Z/chromium-desktop-map-c10-focus.png",
    "results/labviz/review/20261008T102337237Z/chromium-desktop-map-c10-greyscale.png",
    "results/labviz/review/20261008T102337237Z/chromium-desktop-map.png",
    "results/labviz/review/20261008T102337237Z/chromium-desktop-model-2d.png",
    "results/labviz/review/20261008T102337237Z/chromium-desktop-model-3d.png",
    "results/labviz/review/20261008T102337237Z/chromium-desktop-model-mistral.png",
    "results/labviz/review/20261008T102337237Z/chromium-desktop-run-c10v-b-a7.png",
    "results/labviz/review/20261008T102337237Z/chromium-desktop-run-g6.1.png",
    "results/labviz/review/20261008T102337237Z/chromium-landscape-compare.png",
    "results/labviz/review/20261008T102337237Z/chromium-landscape-evaluations.png",
    "results/labviz/review/20261008T102337237Z/chromium-landscape-learn.png",
    "results/labviz/review/20261008T102337237Z/chromium-landscape-line-c10.png",
    "results/labviz/review/20261008T102337237Z/chromium-landscape-line-d1.png",
    "results/labviz/review/20261008T102337237Z/chromium-landscape-line-f1-conditions.png",
    "results/labviz/review/20261008T102337237Z/chromium-landscape-line-t-branch.png",
    "results/labviz/review/20261008T102337237Z/chromium-landscape-line-viability.png",
    "results/labviz/review/20261008T102337237Z/chromium-landscape-map-c10-focus.png",
    "results/labviz/review/20261008T102337237Z/chromium-landscape-map-c10-greyscale.png",
    "results/labviz/review/20261008T102337237Z/chromium-landscape-map.png",
    "results/labviz/review/20261008T102337237Z/chromium-landscape-model-2d.png",
    "results/labviz/review/20261008T102337237Z/chromium-landscape-model-3d.png",
    "results/labviz/review/20261008T102337237Z/chromium-landscape-model-mistral.png",
    "results/labviz/review/20261008T102337237Z/chromium-landscape-run-c10v-b-a7.png",
    "results/labviz/review/20261008T102337237Z/chromium-landscape-run-g6.1.png",
    "results/labviz/review/20261008T102337237Z/chromium-narrow-compare.png",
    "results/labviz/review/20261008T102337237Z/chromium-narrow-evaluations.png",
    "results/labviz/review/20261008T102337237Z/chromium-narrow-learn.png",
    "results/labviz/review/20261008T102337237Z/chromium-narrow-line-c10.png",
    "results/labviz/review/20261008T102337237Z/chromium-narrow-line-d1.png",
    "results/labviz/review/20261008T102337237Z/chromium-narrow-line-f1-conditions.png",
    "results/labviz/review/20261008T102337237Z/chromium-narrow-line-t-branch.png",
    "results/labviz/review/20261008T102337237Z/chromium-narrow-line-viability.png",
    "results/labviz/review/20261008T102337237Z/chromium-narrow-map-c10-focus.png",
    "results/labviz/review/20261008T102337237Z/chromium-narrow-map-c10-greyscale.png",
    "results/labviz/review/20261008T102337237Z/chromium-narrow-map.png",
    "results/labviz/review/20261008T102337237Z/chromium-narrow-model-2d.png",
    "results/labviz/review/20261008T102337237Z/chromium-narrow-model-3d.png",
    "results/labviz/review/20261008T102337237Z/chromium-narrow-model-mistral.png",
    "results/labviz/review/20261008T102337237Z/chromium-narrow-run-c10v-b-a7.png",
    "results/labviz/review/20261008T102337237Z/chromium-narrow-run-g6.1.png",
    "results/labviz/review/20261008T102337237Z/chromium-phone-compare.png",
    "results/labviz/review/20261008T102337237Z/chromium-phone-evaluations.png",
    "results/labviz/review/20261008T102337237Z/chromium-phone-learn.png",
    "results/labviz/review/20261008T102337237Z/chromium-phone-line-c10.png",
    "results/labviz/review/20261008T102337237Z/chromium-phone-line-d1.png",
    "results/labviz/review/20261008T102337237Z/chromium-phone-line-f1-conditions.png",
    "results/labviz/review/20261008T102337237Z/chromium-phone-line-t-branch.png",
    "results/labviz/review/20261008T102337237Z/chromium-phone-line-viability.png",
    "results/labviz/review/20261008T102337237Z/chromium-phone-map-c10-focus.png",
    "results/labviz/review/20261008T102337237Z/chromium-phone-map-c10-greyscale.png",
    "results/labviz/review/20261008T102337237Z/chromium-phone-map.png",
    "results/labviz/review/20261008T102337237Z/chromium-phone-model-2d.png",
    "results/labviz/review/20261008T102337237Z/chromium-phone-model-3d.png",
    "results/labviz/review/20261008T102337237Z/chromium-phone-model-mistral.png",
    "results/labviz/review/20261008T102337237Z/chromium-phone-run-c10v-b-a7.png",
    "results/labviz/review/20261008T102337237Z/chromium-phone-run-g6.1.png",
    "results/labviz/review/20261008T102337237Z/measure.json",
    "results/labviz/review/20261008T102337237Z/webkit-desktop-200pct-compare.png",
    "results/labviz/review/20261008T102337237Z/webkit-desktop-200pct-evaluations.png",
    "results/labviz/review/20261008T102337237Z/webkit-desktop-200pct-learn.png",
    "results/labviz/review/20261008T102337237Z/webkit-desktop-200pct-line-c10.png",
    "results/labviz/review/20261008T102337237Z/webkit-desktop-200pct-line-d1.png",
    "results/labviz/review/20261008T102337237Z/webkit-desktop-200pct-line-f1-conditions.png",
    "results/labviz/review/20261008T102337237Z/webkit-desktop-200pct-line-t-branch.png",
    "results/labviz/review/20261008T102337237Z/webkit-desktop-200pct-line-viability.png",
    "results/labviz/review/20261008T102337237Z/webkit-desktop-200pct-map-c10-focus.png",
    "results/labviz/review/20261008T102337237Z/webkit-desktop-200pct-map-c10-greyscale.png",
    "results/labviz/review/20261008T102337237Z/webkit-desktop-200pct-map.png",
    "results/labviz/review/20261008T102337237Z/webkit-desktop-200pct-model-2d.png",
    "results/labviz/review/20261008T102337237Z/webkit-desktop-200pct-model-3d.png",
    "results/labviz/review/20261008T102337237Z/webkit-desktop-200pct-model-mistral.png",
    "results/labviz/review/20261008T102337237Z/webkit-desktop-200pct-run-c10v-b-a7.png",
    "results/labviz/review/20261008T102337237Z/webkit-desktop-200pct-run-g6.1.png",
    "results/labviz/review/20261008T102337237Z/webkit-desktop-compare.png",
    "results/labviz/review/20261008T102337237Z/webkit-desktop-evaluations.png",
    "results/labviz/review/20261008T102337237Z/webkit-desktop-learn.png",
    "results/labviz/review/20261008T102337237Z/webkit-desktop-line-c10.png",
    "results/labviz/review/20261008T102337237Z/webkit-desktop-line-d1.png",
    "results/labviz/review/20261008T102337237Z/webkit-desktop-line-f1-conditions.png",
    "results/labviz/review/20261008T102337237Z/webkit-desktop-line-t-branch.png",
    "results/labviz/review/20261008T102337237Z/webkit-desktop-line-viability.png",
    "results/labviz/review/20261008T102337237Z/webkit-desktop-map-c10-focus.png",
    "results/labviz/review/20261008T102337237Z/webkit-desktop-map-c10-greyscale.png",
    "results/labviz/review/20261008T102337237Z/webkit-desktop-map.png",
    "results/labviz/review/20261008T102337237Z/webkit-desktop-model-2d.png",
    "results/labviz/review/20261008T102337237Z/webkit-desktop-model-3d.png",
    "results/labviz/review/20261008T102337237Z/webkit-desktop-model-mistral.png",
    "results/labviz/review/20261008T102337237Z/webkit-desktop-run-c10v-b-a7.png",
    "results/labviz/review/20261008T102337237Z/webkit-desktop-run-g6.1.png",
    "results/labviz/review/20261008T102337237Z/webkit-landscape-compare.png",
    "results/labviz/review/20261008T102337237Z/webkit-landscape-evaluations.png",
    "results/labviz/review/20261008T102337237Z/webkit-landscape-learn.png",
    "results/labviz/review/20261008T102337237Z/webkit-landscape-line-c10.png",
    "results/labviz/review/20261008T102337237Z/webkit-landscape-line-d1.png",
    "results/labviz/review/20261008T102337237Z/webkit-landscape-line-f1-conditions.png",
    "results/labviz/review/20261008T102337237Z/webkit-landscape-line-t-branch.png",
    "results/labviz/review/20261008T102337237Z/webkit-landscape-line-viability.png",
    "results/labviz/review/20261008T102337237Z/webkit-landscape-map-c10-focus.png",
    "results/labviz/review/20261008T102337237Z/webkit-landscape-map-c10-greyscale.png",
    "results/labviz/review/20261008T102337237Z/webkit-landscape-map.png",
    "results/labviz/review/20261008T102337237Z/webkit-landscape-model-2d.png",
    "results/labviz/review/20261008T102337237Z/webkit-landscape-model-3d.png",
    "results/labviz/review/20261008T102337237Z/webkit-landscape-model-mistral.png",
    "results/labviz/review/20261008T102337237Z/webkit-landscape-run-c10v-b-a7.png",
    "results/labviz/review/20261008T102337237Z/webkit-landscape-run-g6.1.png",
    "results/labviz/review/20261008T102337237Z/webkit-narrow-compare.png",
    "results/labviz/review/20261008T102337237Z/webkit-narrow-evaluations.png",
    "results/labviz/review/20261008T102337237Z/webkit-narrow-learn.png",
    "results/labviz/review/20261008T102337237Z/webkit-narrow-line-c10.png",
    "results/labviz/review/20261008T102337237Z/webkit-narrow-line-d1.png",
    "results/labviz/review/20261008T102337237Z/webkit-narrow-line-f1-conditions.png",
    "results/labviz/review/20261008T102337237Z/webkit-narrow-line-t-branch.png",
    "results/labviz/review/20261008T102337237Z/webkit-narrow-line-viability.png",
    "results/labviz/review/20261008T102337237Z/webkit-narrow-map-c10-focus.png",
    "results/labviz/review/20261008T102337237Z/webkit-narrow-map-c10-greyscale.png",
    "results/labviz/review/20261008T102337237Z/webkit-narrow-map.png",
    "results/labviz/review/20261008T102337237Z/webkit-narrow-model-2d.png",
    "results/labviz/review/20261008T102337237Z/webkit-narrow-model-3d.png",
    "results/labviz/review/20261008T102337237Z/webkit-narrow-model-mistral.png",
    "results/labviz/review/20261008T102337237Z/webkit-narrow-run-c10v-b-a7.png",
    "results/labviz/review/20261008T102337237Z/webkit-narrow-run-g6.1.png",
    "results/labviz/review/20261008T102337237Z/webkit-phone-compare.png",
    "results/labviz/review/20261008T102337237Z/webkit-phone-evaluations.png",
    "results/labviz/review/20261008T102337237Z/webkit-phone-learn.png",
    "results/labviz/review/20261008T102337237Z/webkit-phone-line-c10.png",
    "results/labviz/review/20261008T102337237Z/webkit-phone-line-d1.png",
    "results/labviz/review/20261008T102337237Z/webkit-phone-line-f1-conditions.png",
    "results/labviz/review/20261008T102337237Z/webkit-phone-line-t-branch.png",
    "results/labviz/review/20261008T102337237Z/webkit-phone-line-viability.png",
    "results/labviz/review/20261008T102337237Z/webkit-phone-map-c10-focus.png",
    "results/labviz/review/20261008T102337237Z/webkit-phone-map-c10-greyscale.png",
    "results/labviz/review/20261008T102337237Z/webkit-phone-map.png",
    "results/labviz/review/20261008T102337237Z/webkit-phone-model-2d.png",
    "results/labviz/review/20261008T102337237Z/webkit-phone-model-3d.png",
    "results/labviz/review/20261008T102337237Z/webkit-phone-model-mistral.png",
    "results/labviz/review/20261008T102337237Z/webkit-phone-run-c10v-b-a7.png",
    "results/labviz/review/20261008T102337237Z/webkit-phone-run-g6.1.png",
    "results/labviz/review/20261008T114734498Z",
    "results/labviz/review/20261008T114734498Z/browser-tests.json",
    "results/labviz/review/20261008T114734498Z/chromium-desktop-200pct-compare.png",
    "results/labviz/review/20261008T114734498Z/chromium-desktop-200pct-evaluations.png",
    "results/labviz/review/20261008T114734498Z/chromium-desktop-200pct-learn.png",
    "results/labviz/review/20261008T114734498Z/chromium-desktop-200pct-line-c10.png",
    "results/labviz/review/20261008T114734498Z/chromium-desktop-200pct-line-d1.png",
    "results/labviz/review/20261008T114734498Z/chromium-desktop-200pct-line-f1-conditions.png",
    "results/labviz/review/20261008T114734498Z/chromium-desktop-200pct-line-t-branch.png",
    "results/labviz/review/20261008T114734498Z/chromium-desktop-200pct-line-viability.png",
    "results/labviz/review/20261008T114734498Z/chromium-desktop-200pct-map-c10-focus.png",
    "results/labviz/review/20261008T114734498Z/chromium-desktop-200pct-map-c10-greyscale.png",
    "results/labviz/review/20261008T114734498Z/chromium-desktop-200pct-map.png",
    "results/labviz/review/20261008T114734498Z/chromium-desktop-200pct-model-2d.png",
    "results/labviz/review/20261008T114734498Z/chromium-desktop-200pct-model-3d.png",
    "results/labviz/review/20261008T114734498Z/chromium-desktop-200pct-model-mistral.png",
    "results/labviz/review/20261008T114734498Z/chromium-desktop-200pct-run-c10v-b-a7.png",
    "results/labviz/review/20261008T114734498Z/chromium-desktop-200pct-run-g6.1.png",
    "results/labviz/review/20261008T114734498Z/chromium-desktop-compare.png",
    "results/labviz/review/20261008T114734498Z/chromium-desktop-evaluations.png",
    "results/labviz/review/20261008T114734498Z/chromium-desktop-learn.png",
    "results/labviz/review/20261008T114734498Z/chromium-desktop-line-c10.png",
    "results/labviz/review/20261008T114734498Z/chromium-desktop-line-d1.png",
    "results/labviz/review/20261008T114734498Z/chromium-desktop-line-f1-conditions.png",
    "results/labviz/review/20261008T114734498Z/chromium-desktop-line-t-branch.png",
    "results/labviz/review/20261008T114734498Z/chromium-desktop-line-viability.png",
    "results/labviz/review/20261008T114734498Z/chromium-desktop-map-c10-focus.png",
    "results/labviz/review/20261008T114734498Z/chromium-desktop-map-c10-greyscale.png",
    "results/labviz/review/20261008T114734498Z/chromium-desktop-map.png",
    "results/labviz/review/20261008T114734498Z/chromium-desktop-model-2d.png",
    "results/labviz/review/20261008T114734498Z/chromium-desktop-model-3d.png",
    "results/labviz/review/20261008T114734498Z/chromium-desktop-model-mistral.png",
    "results/labviz/review/20261008T114734498Z/chromium-desktop-run-c10v-b-a7.png",
    "results/labviz/review/20261008T114734498Z/chromium-desktop-run-g6.1.png",
    "results/labviz/review/20261008T114734498Z/chromium-landscape-compare.png",
    "results/labviz/review/20261008T114734498Z/chromium-landscape-evaluations.png",
    "results/labviz/review/20261008T114734498Z/chromium-landscape-learn.png",
    "results/labviz/review/20261008T114734498Z/chromium-landscape-line-c10.png",
    "results/labviz/review/20261008T114734498Z/chromium-landscape-line-d1.png",
    "results/labviz/review/20261008T114734498Z/chromium-landscape-line-f1-conditions.png",
    "results/labviz/review/20261008T114734498Z/chromium-landscape-line-t-branch.png",
    "results/labviz/review/20261008T114734498Z/chromium-landscape-line-viability.png",
    "results/labviz/review/20261008T114734498Z/chromium-landscape-map-c10-focus.png",
    "results/labviz/review/20261008T114734498Z/chromium-landscape-map-c10-greyscale.png",
    "results/labviz/review/20261008T114734498Z/chromium-landscape-map.png",
    "results/labviz/review/20261008T114734498Z/chromium-landscape-model-2d.png",
    "results/labviz/review/20261008T114734498Z/chromium-landscape-model-3d.png",
    "results/labviz/review/20261008T114734498Z/chromium-landscape-model-mistral.png",
    "results/labviz/review/20261008T114734498Z/chromium-landscape-run-c10v-b-a7.png",
    "results/labviz/review/20261008T114734498Z/chromium-landscape-run-g6.1.png",
    "results/labviz/review/20261008T114734498Z/chromium-narrow-compare.png",
    "results/labviz/review/20261008T114734498Z/chromium-narrow-evaluations.png",
    "results/labviz/review/20261008T114734498Z/chromium-narrow-learn.png",
    "results/labviz/review/20261008T114734498Z/chromium-narrow-line-c10.png",
    "results/labviz/review/20261008T114734498Z/chromium-narrow-line-d1.png",
    "results/labviz/review/20261008T114734498Z/chromium-narrow-line-f1-conditions.png",
    "results/labviz/review/20261008T114734498Z/chromium-narrow-line-t-branch.png",
    "results/labviz/review/20261008T114734498Z/chromium-narrow-line-viability.png",
    "results/labviz/review/20261008T114734498Z/chromium-narrow-map-c10-focus.png",
    "results/labviz/review/20261008T114734498Z/chromium-narrow-map-c10-greyscale.png",
    "results/labviz/review/20261008T114734498Z/chromium-narrow-map.png",
    "results/labviz/review/20261008T114734498Z/chromium-narrow-model-2d.png",
    "results/labviz/review/20261008T114734498Z/chromium-narrow-model-3d.png",
    "results/labviz/review/20261008T114734498Z/chromium-narrow-model-mistral.png",
    "results/labviz/review/20261008T114734498Z/chromium-narrow-run-c10v-b-a7.png",
    "results/labviz/review/20261008T114734498Z/chromium-narrow-run-g6.1.png",
    "results/labviz/review/20261008T114734498Z/chromium-phone-compare.png",
    "results/labviz/review/20261008T114734498Z/chromium-phone-evaluations.png",
    "results/labviz/review/20261008T114734498Z/chromium-phone-learn.png",
    "results/labviz/review/20261008T114734498Z/chromium-phone-line-c10.png",
    "results/labviz/review/20261008T114734498Z/chromium-phone-line-d1.png",
    "results/labviz/review/20261008T114734498Z/chromium-phone-line-f1-conditions.png",
    "results/labviz/review/20261008T114734498Z/chromium-phone-line-t-branch.png",
    "results/labviz/review/20261008T114734498Z/chromium-phone-line-viability.png",
    "results/labviz/review/20261008T114734498Z/chromium-phone-map-c10-focus.png",
    "results/labviz/review/20261008T114734498Z/chromium-phone-map-c10-greyscale.png",
    "results/labviz/review/20261008T114734498Z/chromium-phone-map.png",
    "results/labviz/review/20261008T114734498Z/chromium-phone-model-2d.png",
    "results/labviz/review/20261008T114734498Z/chromium-phone-model-3d.png",
    "results/labviz/review/20261008T114734498Z/chromium-phone-model-mistral.png",
    "results/labviz/review/20261008T114734498Z/chromium-phone-run-c10v-b-a7.png",
    "results/labviz/review/20261008T114734498Z/chromium-phone-run-g6.1.png",
    "results/labviz/review/20261008T114734498Z/measure.json",
    "results/labviz/review/20261008T114734498Z/webkit-desktop-200pct-compare.png",
    "results/labviz/review/20261008T114734498Z/webkit-desktop-200pct-evaluations.png",
    "results/labviz/review/20261008T114734498Z/webkit-desktop-200pct-learn.png",
    "results/labviz/review/20261008T114734498Z/webkit-desktop-200pct-line-c10.png",
    "results/labviz/review/20261008T114734498Z/webkit-desktop-200pct-line-d1.png",
    "results/labviz/review/20261008T114734498Z/webkit-desktop-200pct-line-f1-conditions.png",
    "results/labviz/review/20261008T114734498Z/webkit-desktop-200pct-line-t-branch.png",
    "results/labviz/review/20261008T114734498Z/webkit-desktop-200pct-line-viability.png",
    "results/labviz/review/20261008T114734498Z/webkit-desktop-200pct-map-c10-focus.png",
    "results/labviz/review/20261008T114734498Z/webkit-desktop-200pct-map-c10-greyscale.png",
    "results/labviz/review/20261008T114734498Z/webkit-desktop-200pct-map.png",
    "results/labviz/review/20261008T114734498Z/webkit-desktop-200pct-model-2d.png",
    "results/labviz/review/20261008T114734498Z/webkit-desktop-200pct-model-3d.png",
    "results/labviz/review/20261008T114734498Z/webkit-desktop-200pct-model-mistral.png",
    "results/labviz/review/20261008T114734498Z/webkit-desktop-200pct-run-c10v-b-a7.png",
    "results/labviz/review/20261008T114734498Z/webkit-desktop-200pct-run-g6.1.png",
    "results/labviz/review/20261008T114734498Z/webkit-desktop-compare.png",
    "results/labviz/review/20261008T114734498Z/webkit-desktop-evaluations.png",
    "results/labviz/review/20261008T114734498Z/webkit-desktop-learn.png",
    "results/labviz/review/20261008T114734498Z/webkit-desktop-line-c10.png",
    "results/labviz/review/20261008T114734498Z/webkit-desktop-line-d1.png",
    "results/labviz/review/20261008T114734498Z/webkit-desktop-line-f1-conditions.png",
    "results/labviz/review/20261008T114734498Z/webkit-desktop-line-t-branch.png",
    "results/labviz/review/20261008T114734498Z/webkit-desktop-line-viability.png",
    "results/labviz/review/20261008T114734498Z/webkit-desktop-map-c10-focus.png",
    "results/labviz/review/20261008T114734498Z/webkit-desktop-map-c10-greyscale.png",
    "results/labviz/review/20261008T114734498Z/webkit-desktop-map.png",
    "results/labviz/review/20261008T114734498Z/webkit-desktop-model-2d.png",
    "results/labviz/review/20261008T114734498Z/webkit-desktop-model-3d.png",
    "results/labviz/review/20261008T114734498Z/webkit-desktop-model-mistral.png",
    "results/labviz/review/20261008T114734498Z/webkit-desktop-run-c10v-b-a7.png",
    "results/labviz/review/20261008T114734498Z/webkit-desktop-run-g6.1.png",
    "results/labviz/review/20261008T114734498Z/webkit-landscape-compare.png",
    "results/labviz/review/20261008T114734498Z/webkit-landscape-evaluations.png",
    "results/labviz/review/20261008T114734498Z/webkit-landscape-learn.png",
    "results/labviz/review/20261008T114734498Z/webkit-landscape-line-c10.png",
    "results/labviz/review/20261008T114734498Z/webkit-landscape-line-d1.png",
    "results/labviz/review/20261008T114734498Z/webkit-landscape-line-f1-conditions.png",
    "results/labviz/review/20261008T114734498Z/webkit-landscape-line-t-branch.png",
    "results/labviz/review/20261008T114734498Z/webkit-landscape-line-viability.png",
    "results/labviz/review/20261008T114734498Z/webkit-landscape-map-c10-focus.png",
    "results/labviz/review/20261008T114734498Z/webkit-landscape-map-c10-greyscale.png",
    "results/labviz/review/20261008T114734498Z/webkit-landscape-map.png",
    "results/labviz/review/20261008T114734498Z/webkit-landscape-model-2d.png",
    "results/labviz/review/20261008T114734498Z/webkit-landscape-model-3d.png",
    "results/labviz/review/20261008T114734498Z/webkit-landscape-model-mistral.png",
    "results/labviz/review/20261008T114734498Z/webkit-landscape-run-c10v-b-a7.png",
    "results/labviz/review/20261008T114734498Z/webkit-landscape-run-g6.1.png",
    "results/labviz/review/20261008T114734498Z/webkit-narrow-compare.png",
    "results/labviz/review/20261008T114734498Z/webkit-narrow-evaluations.png",
    "results/labviz/review/20261008T114734498Z/webkit-narrow-learn.png",
    "results/labviz/review/20261008T114734498Z/webkit-narrow-line-c10.png",
    "results/labviz/review/20261008T114734498Z/webkit-narrow-line-d1.png",
    "results/labviz/review/20261008T114734498Z/webkit-narrow-line-f1-conditions.png",
    "results/labviz/review/20261008T114734498Z/webkit-narrow-line-t-branch.png",
    "results/labviz/review/20261008T114734498Z/webkit-narrow-line-viability.png",
    "results/labviz/review/20261008T114734498Z/webkit-narrow-map-c10-focus.png",
    "results/labviz/review/20261008T114734498Z/webkit-narrow-map-c10-greyscale.png",
    "results/labviz/review/20261008T114734498Z/webkit-narrow-map.png",
    "results/labviz/review/20261008T114734498Z/webkit-narrow-model-2d.png",
    "results/labviz/review/20261008T114734498Z/webkit-narrow-model-3d.png",
    "results/labviz/review/20261008T114734498Z/webkit-narrow-model-mistral.png",
    "results/labviz/review/20261008T114734498Z/webkit-narrow-run-c10v-b-a7.png",
    "results/labviz/review/20261008T114734498Z/webkit-narrow-run-g6.1.png",
    "results/labviz/review/20261008T114734498Z/webkit-phone-compare.png",
    "results/labviz/review/20261008T114734498Z/webkit-phone-evaluations.png",
    "results/labviz/review/20261008T114734498Z/webkit-phone-learn.png",
    "results/labviz/review/20261008T114734498Z/webkit-phone-line-c10.png",
    "results/labviz/review/20261008T114734498Z/webkit-phone-line-d1.png",
    "results/labviz/review/20261008T114734498Z/webkit-phone-line-f1-conditions.png",
    "results/labviz/review/20261008T114734498Z/webkit-phone-line-t-branch.png",
    "results/labviz/review/20261008T114734498Z/webkit-phone-line-viability.png",
    "results/labviz/review/20261008T114734498Z/webkit-phone-map-c10-focus.png",
    "results/labviz/review/20261008T114734498Z/webkit-phone-map-c10-greyscale.png",
    "results/labviz/review/20261008T114734498Z/webkit-phone-map.png",
    "results/labviz/review/20261008T114734498Z/webkit-phone-model-2d.png",
    "results/labviz/review/20261008T114734498Z/webkit-phone-model-3d.png",
    "results/labviz/review/20261008T114734498Z/webkit-phone-model-mistral.png",
    "results/labviz/review/20261008T114734498Z/webkit-phone-run-c10v-b-a7.png",
    "results/labviz/review/20261008T114734498Z/webkit-phone-run-g6.1.png",
    "results/labviz/review/20261008T121855879Z",
    "results/labviz/review/20261008T121855879Z/browser-tests.json",
    "results/labviz/review/20261008T121855879Z/chromium-desktop-200pct-compare.png",
    "results/labviz/review/20261008T121855879Z/chromium-desktop-200pct-evaluations.png",
    "results/labviz/review/20261008T121855879Z/chromium-desktop-200pct-line-f1-conditions.png",
    "results/labviz/review/20261008T121855879Z/chromium-desktop-200pct-map.png",
    "results/labviz/review/20261008T121855879Z/chromium-desktop-evaluations.png",
    "results/labviz/review/20261008T121855879Z/chromium-desktop-line-c10.png",
    "results/labviz/review/20261008T121855879Z/chromium-desktop-map.png",
    "results/labviz/review/20261008T121855879Z/chromium-desktop-model-mistral.png",
    "results/labviz/review/20261008T121855879Z/chromium-desktop-run-c10v-b-a7.png",
    "results/labviz/review/20261008T121855879Z/chromium-landscape-compare.png",
    "results/labviz/review/20261008T121855879Z/chromium-landscape-evaluations.png",
    "results/labviz/review/20261008T121855879Z/chromium-landscape-line-f1-conditions.png",
    "results/labviz/review/20261008T121855879Z/chromium-landscape-map.png",
    "results/labviz/review/20261008T121855879Z/chromium-narrow-compare.png",
    "results/labviz/review/20261008T121855879Z/chromium-narrow-evaluations.png",
    "results/labviz/review/20261008T121855879Z/chromium-narrow-line-f1-conditions.png",
    "results/labviz/review/20261008T121855879Z/chromium-narrow-map.png",
    "results/labviz/review/20261008T121855879Z/chromium-phone-compare.png",
    "results/labviz/review/20261008T121855879Z/chromium-phone-evaluations.png",
    "results/labviz/review/20261008T121855879Z/chromium-phone-line-f1-conditions.png",
    "results/labviz/review/20261008T121855879Z/chromium-phone-map.png",
    "results/labviz/review/20261008T121855879Z/measure.json",
    "results/labviz/review/20261008T121855879Z/webkit-desktop-200pct-map.png",
    "results/labviz/review/20261008T121855879Z/webkit-desktop-evaluations.png",
    "results/labviz/review/20261008T121855879Z/webkit-desktop-line-c10.png",
    "results/labviz/review/20261008T121855879Z/webkit-desktop-line-viability.png",
    "results/labviz/review/20261008T121855879Z/webkit-desktop-map.png",
    "results/labviz/review/20261008T121855879Z/webkit-desktop-run-c10v-b-a7.png",
    "results/labviz/review/20261008T121855879Z/webkit-desktop-run-g6.1.png",
    "results/labviz/review/20261008T121855879Z/webkit-landscape-compare.png",
    "results/labviz/review/20261008T121855879Z/webkit-landscape-line-c10.png",
    "results/labviz/review/20261008T121855879Z/webkit-landscape-line-viability.png",
    "results/labviz/review/20261008T121855879Z/webkit-landscape-map.png",
    "results/labviz/review/20261008T121855879Z/webkit-narrow-line-c10.png",
    "results/labviz/review/20261008T121855879Z/webkit-narrow-line-viability.png",
    "results/labviz/review/20261008T121855879Z/webkit-narrow-map.png",
    "results/labviz/review/20261008T121855879Z/webkit-phone-evaluations.png",
    "results/labviz/review/20261008T121855879Z/webkit-phone-line-c10.png",
    "results/labviz/review/20261008T121855879Z/webkit-phone-line-viability.png",
    "results/labviz/review/20261008T121855879Z/webkit-phone-map.png",
    "results/labviz/review/20261008T121855879Z/webkit-phone-model-mistral.png",
    "results/labviz/review/20261008T121855879Z/webkit-phone-run-c10v-b-a7.png",
    "results/labviz/review/20261008T124926101Z",
    "results/labviz/review/20261008T124926101Z/browser-tests.json",
    "results/labviz/review/20261008T124926101Z/chromium-desktop-200pct-evaluations.png",
    "results/labviz/review/20261008T124926101Z/chromium-desktop-200pct-line-d1.png",
    "results/labviz/review/20261008T124926101Z/chromium-desktop-200pct-line-f1-conditions.png",
    "results/labviz/review/20261008T124926101Z/chromium-desktop-200pct-line-t-branch.png",
    "results/labviz/review/20261008T124926101Z/chromium-desktop-200pct-map.png",
    "results/labviz/review/20261008T124926101Z/chromium-desktop-200pct-model-2d.png",
    "results/labviz/review/20261008T124926101Z/chromium-desktop-200pct-model-3d.png",
    "results/labviz/review/20261008T124926101Z/chromium-desktop-200pct-model-mistral.png",
    "results/labviz/review/20261008T124926101Z/chromium-desktop-200pct-run-g6.1.png",
    "results/labviz/review/20261008T124926101Z/chromium-desktop-evaluations.png",
    "results/labviz/review/20261008T124926101Z/chromium-desktop-line-d1.png",
    "results/labviz/review/20261008T124926101Z/chromium-desktop-line-f1-conditions.png",
    "results/labviz/review/20261008T124926101Z/chromium-desktop-line-t-branch.png",
    "results/labviz/review/20261008T124926101Z/chromium-desktop-map-c10-greyscale.png",
    "results/labviz/review/20261008T124926101Z/chromium-desktop-map.png",
    "results/labviz/review/20261008T124926101Z/chromium-desktop-model-2d.png",
    "results/labviz/review/20261008T124926101Z/chromium-desktop-model-3d.png",
    "results/labviz/review/20261008T124926101Z/chromium-desktop-model-mistral.png",
    "results/labviz/review/20261008T124926101Z/chromium-desktop-run-g6.1.png",
    "results/labviz/review/20261008T124926101Z/chromium-landscape-evaluations.png",
    "results/labviz/review/20261008T124926101Z/chromium-landscape-line-d1.png",
    "results/labviz/review/20261008T124926101Z/chromium-landscape-line-f1-conditions.png",
    "results/labviz/review/20261008T124926101Z/chromium-landscape-line-t-branch.png",
    "results/labviz/review/20261008T124926101Z/chromium-landscape-map.png",
    "results/labviz/review/20261008T124926101Z/chromium-landscape-model-2d.png",
    "results/labviz/review/20261008T124926101Z/chromium-landscape-model-3d.png",
    "results/labviz/review/20261008T124926101Z/chromium-landscape-model-mistral.png",
    "results/labviz/review/20261008T124926101Z/chromium-landscape-run-g6.1.png",
    "results/labviz/review/20261008T124926101Z/chromium-narrow-evaluations.png",
    "results/labviz/review/20261008T124926101Z/chromium-narrow-line-d1.png",
    "results/labviz/review/20261008T124926101Z/chromium-narrow-line-f1-conditions.png",
    "results/labviz/review/20261008T124926101Z/chromium-narrow-line-t-branch.png",
    "results/labviz/review/20261008T124926101Z/chromium-narrow-map.png",
    "results/labviz/review/20261008T124926101Z/chromium-narrow-model-2d.png",
    "results/labviz/review/20261008T124926101Z/chromium-narrow-model-3d.png",
    "results/labviz/review/20261008T124926101Z/chromium-narrow-model-mistral.png",
    "results/labviz/review/20261008T124926101Z/chromium-narrow-run-g6.1.png",
    "results/labviz/review/20261008T124926101Z/chromium-phone-evaluations.png",
    "results/labviz/review/20261008T124926101Z/chromium-phone-line-d1.png",
    "results/labviz/review/20261008T124926101Z/chromium-phone-line-f1-conditions.png",
    "results/labviz/review/20261008T124926101Z/chromium-phone-line-t-branch.png",
    "results/labviz/review/20261008T124926101Z/chromium-phone-map.png",
    "results/labviz/review/20261008T124926101Z/chromium-phone-model-2d.png",
    "results/labviz/review/20261008T124926101Z/chromium-phone-model-3d.png",
    "results/labviz/review/20261008T124926101Z/chromium-phone-model-mistral.png",
    "results/labviz/review/20261008T124926101Z/chromium-phone-run-g6.1.png",
    "results/labviz/review/20261008T124926101Z/measure.json",
    "results/labviz/review/20261008T124926101Z/webkit-desktop-200pct-compare.png",
    "results/labviz/review/20261008T124926101Z/webkit-desktop-200pct-evaluations.png",
    "results/labviz/review/20261008T124926101Z/webkit-desktop-200pct-learn.png",
    "results/labviz/review/20261008T124926101Z/webkit-desktop-200pct-line-c10.png",
    "results/labviz/review/20261008T124926101Z/webkit-desktop-200pct-line-d1.png",
    "results/labviz/review/20261008T124926101Z/webkit-desktop-200pct-line-f1-conditions.png",
    "results/labviz/review/20261008T124926101Z/webkit-desktop-200pct-line-t-branch.png",
    "results/labviz/review/20261008T124926101Z/webkit-desktop-200pct-line-viability.png",
    "results/labviz/review/20261008T124926101Z/webkit-desktop-200pct-map-c10-focus.png",
    "results/labviz/review/20261008T124926101Z/webkit-desktop-200pct-map-c10-greyscale.png",
    "results/labviz/review/20261008T124926101Z/webkit-desktop-200pct-map.png",
    "results/labviz/review/20261008T124926101Z/webkit-desktop-200pct-model-2d.png",
    "results/labviz/review/20261008T124926101Z/webkit-desktop-200pct-model-3d.png",
    "results/labviz/review/20261008T124926101Z/webkit-desktop-200pct-model-mistral.png",
    "results/labviz/review/20261008T124926101Z/webkit-desktop-200pct-run-c10v-b-a7.png",
    "results/labviz/review/20261008T124926101Z/webkit-desktop-200pct-run-g6.1.png",
    "results/labviz/review/20261008T124926101Z/webkit-desktop-compare.png",
    "results/labviz/review/20261008T124926101Z/webkit-desktop-evaluations.png",
    "results/labviz/review/20261008T124926101Z/webkit-desktop-learn.png",
    "results/labviz/review/20261008T124926101Z/webkit-desktop-line-c10.png",
    "results/labviz/review/20261008T124926101Z/webkit-desktop-line-d1.png",
    "results/labviz/review/20261008T124926101Z/webkit-desktop-line-f1-conditions.png",
    "results/labviz/review/20261008T124926101Z/webkit-desktop-line-t-branch.png",
    "results/labviz/review/20261008T124926101Z/webkit-desktop-line-viability.png",
    "results/labviz/review/20261008T124926101Z/webkit-desktop-map-c10-focus.png",
    "results/labviz/review/20261008T124926101Z/webkit-desktop-map-c10-greyscale.png",
    "results/labviz/review/20261008T124926101Z/webkit-desktop-map.png",
    "results/labviz/review/20261008T124926101Z/webkit-desktop-model-2d.png",
    "results/labviz/review/20261008T124926101Z/webkit-desktop-model-3d.png",
    "results/labviz/review/20261008T124926101Z/webkit-desktop-model-mistral.png",
    "results/labviz/review/20261008T124926101Z/webkit-desktop-run-c10v-b-a7.png",
    "results/labviz/review/20261008T124926101Z/webkit-desktop-run-g6.1.png",
    "results/labviz/review/20261008T124926101Z/webkit-landscape-compare.png",
    "results/labviz/review/20261008T124926101Z/webkit-landscape-evaluations.png",
    "results/labviz/review/20261008T124926101Z/webkit-landscape-learn.png",
    "results/labviz/review/20261008T124926101Z/webkit-landscape-line-c10.png",
    "results/labviz/review/20261008T124926101Z/webkit-landscape-line-d1.png",
    "results/labviz/review/20261008T124926101Z/webkit-landscape-line-f1-conditions.png",
    "results/labviz/review/20261008T124926101Z/webkit-landscape-line-t-branch.png",
    "results/labviz/review/20261008T124926101Z/webkit-landscape-line-viability.png",
    "results/labviz/review/20261008T124926101Z/webkit-landscape-map-c10-focus.png",
    "results/labviz/review/20261008T124926101Z/webkit-landscape-map-c10-greyscale.png",
    "results/labviz/review/20261008T124926101Z/webkit-landscape-map.png",
    "results/labviz/review/20261008T124926101Z/webkit-landscape-model-2d.png",
    "results/labviz/review/20261008T124926101Z/webkit-landscape-model-3d.png",
    "results/labviz/review/20261008T124926101Z/webkit-landscape-model-mistral.png",
    "results/labviz/review/20261008T124926101Z/webkit-landscape-run-c10v-b-a7.png",
    "results/labviz/review/20261008T124926101Z/webkit-landscape-run-g6.1.png",
    "results/labviz/review/20261008T124926101Z/webkit-narrow-compare.png",
    "results/labviz/review/20261008T124926101Z/webkit-narrow-evaluations.png",
    "results/labviz/review/20261008T124926101Z/webkit-narrow-learn.png",
    "results/labviz/review/20261008T124926101Z/webkit-narrow-line-c10.png",
    "results/labviz/review/20261008T124926101Z/webkit-narrow-line-d1.png",
    "results/labviz/review/20261008T124926101Z/webkit-narrow-line-f1-conditions.png",
    "results/labviz/review/20261008T124926101Z/webkit-narrow-line-t-branch.png",
    "results/labviz/review/20261008T124926101Z/webkit-narrow-line-viability.png",
    "results/labviz/review/20261008T124926101Z/webkit-narrow-map-c10-focus.png",
    "results/labviz/review/20261008T124926101Z/webkit-narrow-map-c10-greyscale.png",
    "results/labviz/review/20261008T124926101Z/webkit-narrow-map.png",
    "results/labviz/review/20261008T124926101Z/webkit-narrow-model-2d.png",
    "results/labviz/review/20261008T124926101Z/webkit-narrow-model-3d.png",
    "results/labviz/review/20261008T124926101Z/webkit-narrow-model-mistral.png",
    "results/labviz/review/20261008T124926101Z/webkit-narrow-run-c10v-b-a7.png",
    "results/labviz/review/20261008T124926101Z/webkit-narrow-run-g6.1.png",
    "results/labviz/review/20261008T124926101Z/webkit-phone-compare.png",
    "results/labviz/review/20261008T124926101Z/webkit-phone-evaluations.png",
    "results/labviz/review/20261008T124926101Z/webkit-phone-learn.png",
    "results/labviz/review/20261008T124926101Z/webkit-phone-line-c10.png",
    "results/labviz/review/20261008T124926101Z/webkit-phone-line-d1.png",
    "results/labviz/review/20261008T124926101Z/webkit-phone-line-f1-conditions.png",
    "results/labviz/review/20261008T124926101Z/webkit-phone-line-t-branch.png",
    "results/labviz/review/20261008T124926101Z/webkit-phone-line-viability.png",
    "results/labviz/review/20261008T124926101Z/webkit-phone-map-c10-focus.png",
    "results/labviz/review/20261008T124926101Z/webkit-phone-map-c10-greyscale.png",
    "results/labviz/review/20261008T124926101Z/webkit-phone-map.png",
    "results/labviz/review/20261008T124926101Z/webkit-phone-model-2d.png",
    "results/labviz/review/20261008T124926101Z/webkit-phone-model-3d.png",
    "results/labviz/review/20261008T124926101Z/webkit-phone-model-mistral.png",
    "results/labviz/review/20261008T124926101Z/webkit-phone-run-c10v-b-a7.png",
    "results/labviz/review/20261008T124926101Z/webkit-phone-run-g6.1.png",
    "results/labviz/review/fix-round1",
    "results/labviz/review/fix-round1/files-sha256.json",
    "results/labviz/review/fix-round1/generated-render-proof-final.txt",
    "results/labviz/review/fix-round1/generated-render-proof-verified.txt",
    "results/labviz/review/fix-round1/generated-render-proof.json",
    "results/labviz/review/fix-round1/generated-render-proof.txt",
    "results/labviz/review/fix-round1/jq-leaves.json",
    "results/labviz/review/fix-round1/live-log-validation.json",
    "results/labviz/review/fix-round1/node-tests-final.txt",
    "results/labviz/review/fix-round1/node-tests-verified.txt",
    "results/labviz/review/fix-round1/payload-source-snapshot-red.txt",
    "results/labviz/review/fix-round1/provenance-build.txt",
    "results/labviz/review/fix-round1/python-tests-final-source.txt",
    "results/labviz/review/fix-round1/python-tests-final.txt",
    "results/labviz/review/fix-round1/python-tests-verified.txt",
    "results/labviz/review/fix-round1/python-tests.txt",
    "results/labviz/review/fix-round1/report-append-verification.json",
    "results/labviz/review/fix-round1/report.sha256",
    "results/labviz/review/fix-round1/snapshot-integrity-final.json",
    "results/labviz/review/fix-round1/snapshot-integrity.json",
    "results/labviz/review/fix-round1/validation-snapshots",
    "results/labviz/review/fix-round1/validation-snapshots/97dcdfb63279d21279f6d642a811586c4474362fff340350a95fd92c7f63f79c",
    "results/labviz/review/fix-round1/validation-snapshots/97dcdfb63279d21279f6d642a811586c4474362fff340350a95fd92c7f63f79c/p2-eval.log",
    "results/labviz/review/fix-round1/warm-build.txt",
    "results/labviz/review/fix-round1/warm-check.json",
    "results/labviz/review/fix-round1/warm-fixture-check.json",
    "results/labviz/review/fix-round1/warm-live-check.json",
    "results/labviz/review/fix-round1/warm-verification.txt",
    "results/labviz/review/v2-build/browser-tests.json",
    "results/labviz/runs",
    "results/labviz/runs/run-03d0c5336cc98da1.png",
    "results/labviz/runs/run-03d0c5336cc98da1.svg",
    "results/labviz/runs/run-04283bfb5608161b.png",
    "results/labviz/runs/run-04283bfb5608161b.svg",
    "results/labviz/runs/run-042f290769681523.png",
    "results/labviz/runs/run-042f290769681523.svg",
    "results/labviz/runs/run-06e28c3be121ef9a.png",
    "results/labviz/runs/run-06e28c3be121ef9a.svg",
    "results/labviz/runs/run-077d152e025d6ab6.png",
    "results/labviz/runs/run-077d152e025d6ab6.svg",
    "results/labviz/runs/run-07c039cc39f8757d.png",
    "results/labviz/runs/run-07c039cc39f8757d.svg",
    "results/labviz/runs/run-07c587c4bdb35954.png",
    "results/labviz/runs/run-07c587c4bdb35954.svg",
    "results/labviz/runs/run-098916ef291d3366.png",
    "results/labviz/runs/run-098916ef291d3366.svg",
    "results/labviz/runs/run-0a704f7bb1c8dcfa.png",
    "results/labviz/runs/run-0a704f7bb1c8dcfa.svg",
    "results/labviz/runs/run-0bf3bb74f178ad2d.png",
    "results/labviz/runs/run-0bf3bb74f178ad2d.svg",
    "results/labviz/runs/run-0d192c20dad8c49a.png",
    "results/labviz/runs/run-0d192c20dad8c49a.svg",
    "results/labviz/runs/run-0d490ae58f9e4a5a.png",
    "results/labviz/runs/run-0d490ae58f9e4a5a.svg",
    "results/labviz/runs/run-0ed655b78359d8d9.png",
    "results/labviz/runs/run-0ed655b78359d8d9.svg",
    "results/labviz/runs/run-0ee99f7aae9f29e3.png",
    "results/labviz/runs/run-0ee99f7aae9f29e3.svg",
    "results/labviz/runs/run-0fde991b54e0fea7.png",
    "results/labviz/runs/run-0fde991b54e0fea7.svg",
    "results/labviz/runs/run-100cbd881005c455.png",
    "results/labviz/runs/run-100cbd881005c455.svg",
    "results/labviz/runs/run-10f688e36146a5a9.png",
    "results/labviz/runs/run-10f688e36146a5a9.svg",
    "results/labviz/runs/run-129ba4ccd9031738.png",
    "results/labviz/runs/run-129ba4ccd9031738.svg",
    "results/labviz/runs/run-13abdbc1c5f878e1.png",
    "results/labviz/runs/run-13abdbc1c5f878e1.svg",
    "results/labviz/runs/run-1480f2da402485a4.png",
    "results/labviz/runs/run-1480f2da402485a4.svg",
    "results/labviz/runs/run-1488caac4424d130.png",
    "results/labviz/runs/run-1488caac4424d130.svg",
    "results/labviz/runs/run-1525d0579f653938.png",
    "results/labviz/runs/run-1525d0579f653938.svg",
    "results/labviz/runs/run-156e8085aaa3c148.png",
    "results/labviz/runs/run-156e8085aaa3c148.svg",
    "results/labviz/runs/run-159688685f0094f5.png",
    "results/labviz/runs/run-159688685f0094f5.svg",
    "results/labviz/runs/run-1780b43a950f7124.png",
    "results/labviz/runs/run-1780b43a950f7124.svg",
    "results/labviz/runs/run-17cc2d709c661119.png",
    "results/labviz/runs/run-17cc2d709c661119.svg",
    "results/labviz/runs/run-17d812e126d3e452.png",
    "results/labviz/runs/run-17d812e126d3e452.svg",
    "results/labviz/runs/run-18b938480782d157.png",
    "results/labviz/runs/run-18b938480782d157.svg",
    "results/labviz/runs/run-18cb7113a3a7cbef.png",
    "results/labviz/runs/run-18cb7113a3a7cbef.svg",
    "results/labviz/runs/run-195feca845e80895.png",
    "results/labviz/runs/run-195feca845e80895.svg",
    "results/labviz/runs/run-19e7b569d2fdbda7.png",
    "results/labviz/runs/run-19e7b569d2fdbda7.svg",
    "results/labviz/runs/run-1e118c16a06a59b8.png",
    "results/labviz/runs/run-1e118c16a06a59b8.svg",
    "results/labviz/runs/run-206dfdbc6d3daa46.png",
    "results/labviz/runs/run-206dfdbc6d3daa46.svg",
    "results/labviz/runs/run-20916d080a77e482.png",
    "results/labviz/runs/run-20916d080a77e482.svg",
    "results/labviz/runs/run-23c2cf3632e87f07.png",
    "results/labviz/runs/run-23c2cf3632e87f07.svg",
    "results/labviz/runs/run-2409bf429b5bf10a.png",
    "results/labviz/runs/run-2409bf429b5bf10a.svg",
    "results/labviz/runs/run-243d5104a32669ea.png",
    "results/labviz/runs/run-243d5104a32669ea.svg",
    "results/labviz/runs/run-250b0fca1fcef494.png",
    "results/labviz/runs/run-250b0fca1fcef494.svg",
    "results/labviz/runs/run-282365426e143f59.png",
    "results/labviz/runs/run-282365426e143f59.svg",
    "results/labviz/runs/run-2865c5fcabaf41d9.png",
    "results/labviz/runs/run-2865c5fcabaf41d9.svg",
    "results/labviz/runs/run-2943a18096b6d8b4.png",
    "results/labviz/runs/run-2943a18096b6d8b4.svg",
    "results/labviz/runs/run-2b10dd6763225b36.png",
    "results/labviz/runs/run-2b10dd6763225b36.svg",
    "results/labviz/runs/run-2d815e84ff37c5b8.png",
    "results/labviz/runs/run-2d815e84ff37c5b8.svg",
    "results/labviz/runs/run-2df3f0f6577b96ad.png",
    "results/labviz/runs/run-2df3f0f6577b96ad.svg",
    "results/labviz/runs/run-2e3ac3c4e83e6637.png",
    "results/labviz/runs/run-2e3ac3c4e83e6637.svg",
    "results/labviz/runs/run-2ed5d194be072bab.png",
    "results/labviz/runs/run-2ed5d194be072bab.svg",
    "results/labviz/runs/run-3005727130989007.png",
    "results/labviz/runs/run-3005727130989007.svg",
    "results/labviz/runs/run-314338272fc1e445.png",
    "results/labviz/runs/run-314338272fc1e445.svg",
    "results/labviz/runs/run-332ee993771e35e6.png",
    "results/labviz/runs/run-332ee993771e35e6.svg",
    "results/labviz/runs/run-37fd2fd78e12a157.png",
    "results/labviz/runs/run-37fd2fd78e12a157.svg",
    "results/labviz/runs/run-39731f41ac2a830e.png",
    "results/labviz/runs/run-39731f41ac2a830e.svg",
    "results/labviz/runs/run-3cc50f1a0ccc7fa8.png",
    "results/labviz/runs/run-3cc50f1a0ccc7fa8.svg",
    "results/labviz/runs/run-40376027cddf3ef7.png",
    "results/labviz/runs/run-40376027cddf3ef7.svg",
    "results/labviz/runs/run-418bffcd3a539beb.png",
    "results/labviz/runs/run-418bffcd3a539beb.svg",
    "results/labviz/runs/run-41f8b56bde5ff7fd.png",
    "results/labviz/runs/run-41f8b56bde5ff7fd.svg",
    "results/labviz/runs/run-46ae8accb93433f9.png",
    "results/labviz/runs/run-46ae8accb93433f9.svg",
    "results/labviz/runs/run-47ed645ddea37da8.png",
    "results/labviz/runs/run-47ed645ddea37da8.svg",
    "results/labviz/runs/run-4803852fcfeed0bd.png",
    "results/labviz/runs/run-4803852fcfeed0bd.svg",
    "results/labviz/runs/run-48088694b246db13.png",
    "results/labviz/runs/run-48088694b246db13.svg",
    "results/labviz/runs/run-4897514ce6063de6.png",
    "results/labviz/runs/run-4897514ce6063de6.svg",
    "results/labviz/runs/run-48e03328246f9258.png",
    "results/labviz/runs/run-48e03328246f9258.svg",
    "results/labviz/runs/run-4bdff984858c2ba8.png",
    "results/labviz/runs/run-4bdff984858c2ba8.svg",
    "results/labviz/runs/run-4c1d29ec9ac69b95.png",
    "results/labviz/runs/run-4c1d29ec9ac69b95.svg",
    "results/labviz/runs/run-4c70a54f27c618fc.png",
    "results/labviz/runs/run-4c70a54f27c618fc.svg",
    "results/labviz/runs/run-4d05048106f21a80.png",
    "results/labviz/runs/run-4d05048106f21a80.svg",
    "results/labviz/runs/run-4dc966d9634f8b8d.png",
    "results/labviz/runs/run-4dc966d9634f8b8d.svg",
    "results/labviz/runs/run-4e945abe0e71d16b.png",
    "results/labviz/runs/run-4e945abe0e71d16b.svg",
    "results/labviz/runs/run-4f0f8866f4f04d39.png",
    "results/labviz/runs/run-4f0f8866f4f04d39.svg",
    "results/labviz/runs/run-50e4a103cb7c64bf.png",
    "results/labviz/runs/run-50e4a103cb7c64bf.svg",
    "results/labviz/runs/run-514dc519197fadfe.png",
    "results/labviz/runs/run-514dc519197fadfe.svg",
    "results/labviz/runs/run-5231342e030b9c6a.png",
    "results/labviz/runs/run-5231342e030b9c6a.svg",
    "results/labviz/runs/run-53a57577a2ff8e5c.png",
    "results/labviz/runs/run-53a57577a2ff8e5c.svg",
    "results/labviz/runs/run-55276acfcd8fc702.png",
    "results/labviz/runs/run-55276acfcd8fc702.svg",
    "results/labviz/runs/run-576a0e430ed19f7e.png",
    "results/labviz/runs/run-576a0e430ed19f7e.svg",
    "results/labviz/runs/run-5838a23408eadd25.png",
    "results/labviz/runs/run-5838a23408eadd25.svg",
    "results/labviz/runs/run-58815beae4b5b969.png",
    "results/labviz/runs/run-58815beae4b5b969.svg",
    "results/labviz/runs/run-596083a0fa1e21d5.png",
    "results/labviz/runs/run-596083a0fa1e21d5.svg",
    "results/labviz/runs/run-59e93f4fd4eaf860.png",
    "results/labviz/runs/run-59e93f4fd4eaf860.svg",
    "results/labviz/runs/run-5c48804edd914547.png",
    "results/labviz/runs/run-5c48804edd914547.svg",
    "results/labviz/runs/run-5e89b93884495469.png",
    "results/labviz/runs/run-5e89b93884495469.svg",
    "results/labviz/runs/run-5ea0f8b79ab08484.png",
    "results/labviz/runs/run-5ea0f8b79ab08484.svg",
    "results/labviz/runs/run-5eb0df689c1a876f.png",
    "results/labviz/runs/run-5eb0df689c1a876f.svg",
    "results/labviz/runs/run-5fde551914151c96.png",
    "results/labviz/runs/run-5fde551914151c96.svg",
    "results/labviz/runs/run-60ddcdc217a67c1a.png",
    "results/labviz/runs/run-60ddcdc217a67c1a.svg",
    "results/labviz/runs/run-614952bc08deca86.png",
    "results/labviz/runs/run-614952bc08deca86.svg",
    "results/labviz/runs/run-6180715a00449191.png",
    "results/labviz/runs/run-6180715a00449191.svg",
    "results/labviz/runs/run-618b6d5aed16642d.png",
    "results/labviz/runs/run-618b6d5aed16642d.svg",
    "results/labviz/runs/run-61a69ab8ccca7808.png",
    "results/labviz/runs/run-61a69ab8ccca7808.svg",
    "results/labviz/runs/run-6293909f7061fe2b.png",
    "results/labviz/runs/run-6293909f7061fe2b.svg",
    "results/labviz/runs/run-63aa2b1d6d90b0da.png",
    "results/labviz/runs/run-63aa2b1d6d90b0da.svg",
    "results/labviz/runs/run-64a3a5db925f284f.png",
    "results/labviz/runs/run-64a3a5db925f284f.svg",
    "results/labviz/runs/run-67024ac3823a93d6.png",
    "results/labviz/runs/run-67024ac3823a93d6.svg",
    "results/labviz/runs/run-6792dcbf44fa656b.png",
    "results/labviz/runs/run-6792dcbf44fa656b.svg",
    "results/labviz/runs/run-67ef21f3b72f2d0f.png",
    "results/labviz/runs/run-67ef21f3b72f2d0f.svg",
    "results/labviz/runs/run-6815a950dfb195d0.png",
    "results/labviz/runs/run-6815a950dfb195d0.svg",
    "results/labviz/runs/run-681d1059bdff9666.png",
    "results/labviz/runs/run-681d1059bdff9666.svg",
    "results/labviz/runs/run-684bc3e3bdbb57b7.png",
    "results/labviz/runs/run-684bc3e3bdbb57b7.svg",
    "results/labviz/runs/run-689cf09befa057c0.png",
    "results/labviz/runs/run-689cf09befa057c0.svg",
    "results/labviz/runs/run-68c27a3b1ae45f29.png",
    "results/labviz/runs/run-68c27a3b1ae45f29.svg",
    "results/labviz/runs/run-68f78f3967614c47.png",
    "results/labviz/runs/run-68f78f3967614c47.svg",
    "results/labviz/runs/run-6968f20829c393cc.png",
    "results/labviz/runs/run-6968f20829c393cc.svg",
    "results/labviz/runs/run-6c69c836960d1688.png",
    "results/labviz/runs/run-6c69c836960d1688.svg",
    "results/labviz/runs/run-6f5164a0e1ef4e34.png",
    "results/labviz/runs/run-6f5164a0e1ef4e34.svg",
    "results/labviz/runs/run-701cc50d91b01eff.png",
    "results/labviz/runs/run-701cc50d91b01eff.svg",
    "results/labviz/runs/run-70332d7ed4adbc51.png",
    "results/labviz/runs/run-70332d7ed4adbc51.svg",
    "results/labviz/runs/run-70b281545f807852.png",
    "results/labviz/runs/run-70b281545f807852.svg",
    "results/labviz/runs/run-71f4c53b49ffa63a.png",
    "results/labviz/runs/run-71f4c53b49ffa63a.svg",
    "results/labviz/runs/run-758cd628190fc564.png",
    "results/labviz/runs/run-758cd628190fc564.svg",
    "results/labviz/runs/run-76ac1e389e9a7453.png",
    "results/labviz/runs/run-76ac1e389e9a7453.svg",
    "results/labviz/runs/run-76dea29ff62dde28.png",
    "results/labviz/runs/run-76dea29ff62dde28.svg",
    "results/labviz/runs/run-78b96144be65b6bf.png",
    "results/labviz/runs/run-78b96144be65b6bf.svg",
    "results/labviz/runs/run-79ad38d4bbe65a40.png",
    "results/labviz/runs/run-79ad38d4bbe65a40.svg",
    "results/labviz/runs/run-79ca1fdb6f53f401.png",
    "results/labviz/runs/run-79ca1fdb6f53f401.svg",
    "results/labviz/runs/run-7e68369c4dc96827.png",
    "results/labviz/runs/run-7e68369c4dc96827.svg",
    "results/labviz/runs/run-7e7cb9e8c09c6d9b.png",
    "results/labviz/runs/run-7e7cb9e8c09c6d9b.svg",
    "results/labviz/runs/run-7f23f492f7dbf497.png",
    "results/labviz/runs/run-7f23f492f7dbf497.svg",
    "results/labviz/runs/run-7f4e1e3fe661dfa9.png",
    "results/labviz/runs/run-7f4e1e3fe661dfa9.svg",
    "results/labviz/runs/run-7f69ff75ef0d9659.png",
    "results/labviz/runs/run-7f69ff75ef0d9659.svg",
    "results/labviz/runs/run-7f9f33a2008a7b4c.png",
    "results/labviz/runs/run-7f9f33a2008a7b4c.svg",
    "results/labviz/runs/run-7fe9d393c27767c1.png",
    "results/labviz/runs/run-7fe9d393c27767c1.svg",
    "results/labviz/runs/run-81d23feade439e8b.png",
    "results/labviz/runs/run-81d23feade439e8b.svg",
    "results/labviz/runs/run-831b90bb0c34c7f9.png",
    "results/labviz/runs/run-831b90bb0c34c7f9.svg",
    "results/labviz/runs/run-850a2065af8974c3.png",
    "results/labviz/runs/run-850a2065af8974c3.svg",
    "results/labviz/runs/run-8a4321450d52de1a.png",
    "results/labviz/runs/run-8a4321450d52de1a.svg",
    "results/labviz/runs/run-8af9c4a63d0d5f11.png",
    "results/labviz/runs/run-8af9c4a63d0d5f11.svg",
    "results/labviz/runs/run-8e383f99576b8dda.png",
    "results/labviz/runs/run-8e383f99576b8dda.svg",
    "results/labviz/runs/run-8e7690da6f453876.png",
    "results/labviz/runs/run-8e7690da6f453876.svg",
    "results/labviz/runs/run-8edb73566408cd68.png",
    "results/labviz/runs/run-8edb73566408cd68.svg",
    "results/labviz/runs/run-91768e4006b31f76.png",
    "results/labviz/runs/run-91768e4006b31f76.svg",
    "results/labviz/runs/run-934fab911faf5c3a.png",
    "results/labviz/runs/run-934fab911faf5c3a.svg",
    "results/labviz/runs/run-95832719e6277e7f.png",
    "results/labviz/runs/run-95832719e6277e7f.svg",
    "results/labviz/runs/run-9a3dfe073910dd61.png",
    "results/labviz/runs/run-9a3dfe073910dd61.svg",
    "results/labviz/runs/run-9ac05aa31538ec5f.png",
    "results/labviz/runs/run-9ac05aa31538ec5f.svg",
    "results/labviz/runs/run-9f715621a7034e43.png",
    "results/labviz/runs/run-9f715621a7034e43.svg",
    "results/labviz/runs/run-a024e0f0eff105d8.png",
    "results/labviz/runs/run-a024e0f0eff105d8.svg",
    "results/labviz/runs/run-a0853da94bd7c617.png",
    "results/labviz/runs/run-a0853da94bd7c617.svg",
    "results/labviz/runs/run-a0ec42076261d76f.png",
    "results/labviz/runs/run-a0ec42076261d76f.svg",
    "results/labviz/runs/run-a284dac660eab39e.png",
    "results/labviz/runs/run-a284dac660eab39e.svg",
    "results/labviz/runs/run-a28aebf87ee8f95c.png",
    "results/labviz/runs/run-a28aebf87ee8f95c.svg",
    "results/labviz/runs/run-a2ee9b8ef6028b34.png",
    "results/labviz/runs/run-a2ee9b8ef6028b34.svg",
    "results/labviz/runs/run-a38fd82a450ac972.png",
    "results/labviz/runs/run-a38fd82a450ac972.svg",
    "results/labviz/runs/run-a3b3d69efee1394a.png",
    "results/labviz/runs/run-a3b3d69efee1394a.svg",
    "results/labviz/runs/run-a4dabd9fe5348493.png",
    "results/labviz/runs/run-a4dabd9fe5348493.svg",
    "results/labviz/runs/run-a574ad833abfb561.png",
    "results/labviz/runs/run-a574ad833abfb561.svg",
    "results/labviz/runs/run-a9d467d440c7c561.png",
    "results/labviz/runs/run-a9d467d440c7c561.svg",
    "results/labviz/runs/run-a9da9b408945ee50.png",
    "results/labviz/runs/run-a9da9b408945ee50.svg",
    "results/labviz/runs/run-aa7bc35701d13255.png",
    "results/labviz/runs/run-aa7bc35701d13255.svg",
    "results/labviz/runs/run-aca72696ed16875d.png",
    "results/labviz/runs/run-aca72696ed16875d.svg",
    "results/labviz/runs/run-ae178e3090e66454.png",
    "results/labviz/runs/run-ae178e3090e66454.svg",
    "results/labviz/runs/run-aeb152d5b75144d2.png",
    "results/labviz/runs/run-aeb152d5b75144d2.svg",
    "results/labviz/runs/run-b1f39a3c84509ca0.png",
    "results/labviz/runs/run-b1f39a3c84509ca0.svg",
    "results/labviz/runs/run-b331931306979d74.png",
    "results/labviz/runs/run-b331931306979d74.svg",
    "results/labviz/runs/run-b7bfc47f47897317.png",
    "results/labviz/runs/run-b7bfc47f47897317.svg",
    "results/labviz/runs/run-b83c7ad11203ea3c.png",
    "results/labviz/runs/run-b83c7ad11203ea3c.svg",
    "results/labviz/runs/run-b9bdd55162c352af.png",
    "results/labviz/runs/run-b9bdd55162c352af.svg",
    "results/labviz/runs/run-b9f9582dc94ece34.png",
    "results/labviz/runs/run-b9f9582dc94ece34.svg",
    "results/labviz/runs/run-ba3644665a5aca4c.png",
    "results/labviz/runs/run-ba3644665a5aca4c.svg",
    "results/labviz/runs/run-bbdd2fcf5e4d6cf7.png",
    "results/labviz/runs/run-bbdd2fcf5e4d6cf7.svg",
    "results/labviz/runs/run-bcd9b42e0c384189.png",
    "results/labviz/runs/run-bcd9b42e0c384189.svg",
    "results/labviz/runs/run-c0c567423af19bba.png",
    "results/labviz/runs/run-c0c567423af19bba.svg",
    "results/labviz/runs/run-c0e48344dc1c01dc.png",
    "results/labviz/runs/run-c0e48344dc1c01dc.svg",
    "results/labviz/runs/run-c12d6088fbd6ab45.png",
    "results/labviz/runs/run-c12d6088fbd6ab45.svg",
    "results/labviz/runs/run-c1ff0ae6cc13cdb9.png",
    "results/labviz/runs/run-c1ff0ae6cc13cdb9.svg",
    "results/labviz/runs/run-c4349ee7defd4519.png",
    "results/labviz/runs/run-c4349ee7defd4519.svg",
    "results/labviz/runs/run-c7d8d89370c3a9de.png",
    "results/labviz/runs/run-c7d8d89370c3a9de.svg",
    "results/labviz/runs/run-c8fea4c436406c1f.png",
    "results/labviz/runs/run-c8fea4c436406c1f.svg",
    "results/labviz/runs/run-cec8c16e53bfc95c.png",
    "results/labviz/runs/run-cec8c16e53bfc95c.svg",
    "results/labviz/runs/run-d04c87911e0ee39e.png",
    "results/labviz/runs/run-d04c87911e0ee39e.svg",
    "results/labviz/runs/run-d0cc333916d7ce21.png",
    "results/labviz/runs/run-d0cc333916d7ce21.svg",
    "results/labviz/runs/run-d111b73f540d3ec7.png",
    "results/labviz/runs/run-d111b73f540d3ec7.svg",
    "results/labviz/runs/run-d1862f92fa0e241d.png",
    "results/labviz/runs/run-d1862f92fa0e241d.svg",
    "results/labviz/runs/run-d1a0b58778e3bd8c.png",
    "results/labviz/runs/run-d1a0b58778e3bd8c.svg",
    "results/labviz/runs/run-d1abfafd812c4358.png",
    "results/labviz/runs/run-d1abfafd812c4358.svg",
    "results/labviz/runs/run-d35d3a20fe0650e2.png",
    "results/labviz/runs/run-d35d3a20fe0650e2.svg",
    "results/labviz/runs/run-d4d73416cabd0b8f.png",
    "results/labviz/runs/run-d4d73416cabd0b8f.svg",
    "results/labviz/runs/run-d5fd42235c9dd6a9.png",
    "results/labviz/runs/run-d5fd42235c9dd6a9.svg",
    "results/labviz/runs/run-d797fe1ed03533e1.png",
    "results/labviz/runs/run-d797fe1ed03533e1.svg",
    "results/labviz/runs/run-d7f750d20231000f.png",
    "results/labviz/runs/run-d7f750d20231000f.svg",
    "results/labviz/runs/run-d7ff518c41b30ec2.png",
    "results/labviz/runs/run-d7ff518c41b30ec2.svg",
    "results/labviz/runs/run-d82ca184cb546756.png",
    "results/labviz/runs/run-d82ca184cb546756.svg",
    "results/labviz/runs/run-da02571b0b7a5590.png",
    "results/labviz/runs/run-da02571b0b7a5590.svg",
    "results/labviz/runs/run-da9128a7be140025.png",
    "results/labviz/runs/run-da9128a7be140025.svg",
    "results/labviz/runs/run-e07f346e787ff92f.png",
    "results/labviz/runs/run-e07f346e787ff92f.svg",
    "results/labviz/runs/run-e16e9f9e55fec2c4.png",
    "results/labviz/runs/run-e16e9f9e55fec2c4.svg",
    "results/labviz/runs/run-e18dd25e152daf29.png",
    "results/labviz/runs/run-e18dd25e152daf29.svg",
    "results/labviz/runs/run-e1ee39f7330c513c.png",
    "results/labviz/runs/run-e1ee39f7330c513c.svg",
    "results/labviz/runs/run-e2976b8f120f454d.png",
    "results/labviz/runs/run-e2976b8f120f454d.svg",
    "results/labviz/runs/run-e34409c9194fa26a.png",
    "results/labviz/runs/run-e34409c9194fa26a.svg",
    "results/labviz/runs/run-e6ecac0d47609afe.png",
    "results/labviz/runs/run-e6ecac0d47609afe.svg",
    "results/labviz/runs/run-e798a3b8f9961e9b.png",
    "results/labviz/runs/run-e798a3b8f9961e9b.svg",
    "results/labviz/runs/run-ec0f366754fff788.png",
    "results/labviz/runs/run-ec0f366754fff788.svg",
    "results/labviz/runs/run-ecd823e5ba0b973c.png",
    "results/labviz/runs/run-ecd823e5ba0b973c.svg",
    "results/labviz/runs/run-f03029fdfb5c3d4d.png",
    "results/labviz/runs/run-f03029fdfb5c3d4d.svg",
    "results/labviz/runs/run-f10ae2bd12476af0.png",
    "results/labviz/runs/run-f10ae2bd12476af0.svg",
    "results/labviz/runs/run-f2545c68e2461fa3.png",
    "results/labviz/runs/run-f2545c68e2461fa3.svg",
    "results/labviz/runs/run-f6948d5116e11c3d.png",
    "results/labviz/runs/run-f6948d5116e11c3d.svg",
    "results/labviz/runs/run-f82f542ccc4132b7.png",
    "results/labviz/runs/run-f82f542ccc4132b7.svg",
    "results/labviz/runs/run-f9ed47400bcc37b7.png",
    "results/labviz/runs/run-f9ed47400bcc37b7.svg",
    "results/labviz/runs/run-fa48eb972041dbf5.png",
    "results/labviz/runs/run-fa48eb972041dbf5.svg",
    "results/labviz/runs/run-fbc98ba338e833b8.png",
    "results/labviz/runs/run-fbc98ba338e833b8.svg",
    "results/labviz/runs/run-fd6b94281d61637a.png",
    "results/labviz/runs/run-fd6b94281d61637a.svg",
    "results/labviz/runs/run-ffcb76f44711b00e.png",
    "results/labviz/runs/run-ffcb76f44711b00e.svg",
    "results/labviz/site",
    "results/labviz/site/app.js",
    "results/labviz/site/cards",
    "results/labviz/site/cards/index.js",
    "results/labviz/site/cards/index.json",
    "results/labviz/site/cards/line-057590f474bb.js",
    "results/labviz/site/cards/line-09dc0a36dcc1.js",
    "results/labviz/site/cards/line-0d32c51d392b.js",
    "results/labviz/site/cards/line-1068ae5488ec.js",
    "results/labviz/site/cards/line-10dffc008d23.js",
    "results/labviz/site/cards/line-11126b623c7d.js",
    "results/labviz/site/cards/line-13e534b8ac11.js",
    "results/labviz/site/cards/line-19926ca7b879.js",
    "results/labviz/site/cards/line-199cb29c877b.js",
    "results/labviz/site/cards/line-1b8836453960.js",
    "results/labviz/site/cards/line-2027ace4c1ba.js",
    "results/labviz/site/cards/line-22aac2ed59af.js",
    "results/labviz/site/cards/line-22e07b72f61f.js",
    "results/labviz/site/cards/line-2323d191c5bf.js",
    "results/labviz/site/cards/line-234bcabfb6ca.js",
    "results/labviz/site/cards/line-2364c1e02e70.js",
    "results/labviz/site/cards/line-2aa15c9b7a31.js",
    "results/labviz/site/cards/line-31af4fc9c12b.js",
    "results/labviz/site/cards/line-3360ca73bc74.js",
    "results/labviz/site/cards/line-347c6cbdeb8f.js",
    "results/labviz/site/cards/line-36464eec2097.js",
    "results/labviz/site/cards/line-371a86fb46c4.js",
    "results/labviz/site/cards/line-39e85bace320.js",
    "results/labviz/site/cards/line-3bf1a64c32c7.js",
    "results/labviz/site/cards/line-3ef478167886.js",
    "results/labviz/site/cards/line-3f012f034c57.js",
    "results/labviz/site/cards/line-3ff36e069004.js",
    "results/labviz/site/cards/line-4017fb181c52.js",
    "results/labviz/site/cards/line-408baeb828d9.js",
    "results/labviz/site/cards/line-416b7c8699e5.js",
    "results/labviz/site/cards/line-43dd095cbc30.js",
    "results/labviz/site/cards/line-445e118d03a6.js",
    "results/labviz/site/cards/line-44b246d9a85e.js",
    "results/labviz/site/cards/line-479356ac626f.js",
    "results/labviz/site/cards/line-4b8e274df40b.js",
    "results/labviz/site/cards/line-4d03d48ce9b3.js",
    "results/labviz/site/cards/line-4f4a6e040028.js",
    "results/labviz/site/cards/line-552f137fa73e.js",
    "results/labviz/site/cards/line-59fcd5f4fb58.js",
    "results/labviz/site/cards/line-5a016b9f7de9.js",
    "results/labviz/site/cards/line-5d3d9b0a5d61.js",
    "results/labviz/site/cards/line-5de3fe169e00.js",
    "results/labviz/site/cards/line-60043b3775f8.js",
    "results/labviz/site/cards/line-6157f3935f08.js",
    "results/labviz/site/cards/line-63b5cc7a0df5.js",
    "results/labviz/site/cards/line-67bf773c4dba.js",
    "results/labviz/site/cards/line-680f305cf85c.js",
    "results/labviz/site/cards/line-689575085c2d.js",
    "results/labviz/site/cards/line-6d2885c0d082.js",
    "results/labviz/site/cards/line-6dafce1749e3.js",
    "results/labviz/site/cards/line-6ed002342cb7.js",
    "results/labviz/site/cards/line-74ceef54da8e.js",
    "results/labviz/site/cards/line-76dcc6488418.js",
    "results/labviz/site/cards/line-77de02d37aa4.js",
    "results/labviz/site/cards/line-7ae0875d4ebe.js",
    "results/labviz/site/cards/line-7e23be9f0068.js",
    "results/labviz/site/cards/line-7ed1e734b59f.js",
    "results/labviz/site/cards/line-7ef3cd07ba59.js",
    "results/labviz/site/cards/line-801e7ead6403.js",
    "results/labviz/site/cards/line-80b13df7a12f.js",
    "results/labviz/site/cards/line-81761cacc31c.js",
    "results/labviz/site/cards/line-81d9e0aa82d2.js",
    "results/labviz/site/cards/line-81eb631e9ec2.js",
    "results/labviz/site/cards/line-83f562983c70.js",
    "results/labviz/site/cards/line-83f974f1c140.js",
    "results/labviz/site/cards/line-8bb07ad28fcb.js",
    "results/labviz/site/cards/line-920b64e12728.js",
    "results/labviz/site/cards/line-980a93d97fd6.js",
    "results/labviz/site/cards/line-99d651ff16a8.js",
    "results/labviz/site/cards/line-9a18cde5f47d.js",
    "results/labviz/site/cards/line-9bed6eddc4dd.js",
    "results/labviz/site/cards/line-9ff3a24b7c64.js",
    "results/labviz/site/cards/line-a544b2876561.js",
    "results/labviz/site/cards/line-a69f50eee46e.js",
    "results/labviz/site/cards/line-a90c0eb8f965.js",
    "results/labviz/site/cards/line-a9825ab12def.js",
    "results/labviz/site/cards/line-a9fffc8f54e8.js",
    "results/labviz/site/cards/line-abef3e803a40.js",
    "results/labviz/site/cards/line-b0468608869e.js",
    "results/labviz/site/cards/line-b1f5c8b8db64.js",
    "results/labviz/site/cards/line-b2eefd16a74e.js",
    "results/labviz/site/cards/line-b34bdfb02699.js",
    "results/labviz/site/cards/line-b370e2ce0e58.js",
    "results/labviz/site/cards/line-b56bb9e9052b.js",
    "results/labviz/site/cards/line-be77ba707981.js",
    "results/labviz/site/cards/line-beb081806638.js",
    "results/labviz/site/cards/line-c0c938480d94.js",
    "results/labviz/site/cards/line-c1e632fcaec3.js",
    "results/labviz/site/cards/line-c86ca729bc2c.js",
    "results/labviz/site/cards/line-cae5a5029146.js",
    "results/labviz/site/cards/line-cb62a502e337.js",
    "results/labviz/site/cards/line-cd297ea32cc1.js",
    "results/labviz/site/cards/line-ceb394158026.js",
    "results/labviz/site/cards/line-cf0ef617695d.js",
    "results/labviz/site/cards/line-cfc33750397f.js",
    "results/labviz/site/cards/line-d493c471d408.js",
    "results/labviz/site/cards/line-d498d02a1aa0.js",
    "results/labviz/site/cards/line-d5e66e9f0f18.js",
    "results/labviz/site/cards/line-de67ce97ab2d.js",
    "results/labviz/site/cards/line-e06befaf00c3.js",
    "results/labviz/site/cards/line-e3bf5ac891fc.js",
    "results/labviz/site/cards/line-e3e7d2a86de4.js",
    "results/labviz/site/cards/line-e93d7fa1c05c.js",
    "results/labviz/site/cards/line-ed275bc22c83.js",
    "results/labviz/site/cards/line-f177c8e3c8c6.js",
    "results/labviz/site/cards/line-f232ae200b40.js",
    "results/labviz/site/cards/line-f2d698e20304.js",
    "results/labviz/site/cards/line-f51d849aad02.js",
    "results/labviz/site/cards/line-fa1d386b1738.js",
    "results/labviz/site/cards/line-fb3092fa0128.js",
    "results/labviz/site/cards/line-fb6c52d58cbd.js",
    "results/labviz/site/cards/line-fba42b4bf7ce.js",
    "results/labviz/site/cards/line-fc64ee47cd2c.js",
    "results/labviz/site/cards/run-000b8a50c8bd985b.json",
    "results/labviz/site/cards/run-001ea8b2c8ff1cd9.json",
    "results/labviz/site/cards/run-0027ca18bb8f04b0.json",
    "results/labviz/site/cards/run-003a35dab15dfc58.json",
    "results/labviz/site/cards/run-00775362d03d71cf.json",
    "results/labviz/site/cards/run-00864542c0baaa42.json",
    "results/labviz/site/cards/run-010957e136eb8c16.json",
    "results/labviz/site/cards/run-012b3a3091931977.json",
    "results/labviz/site/cards/run-017de0cf187df8cf.json",
    "results/labviz/site/cards/run-017eca6a9878371f.json",
    "results/labviz/site/cards/run-01c431546e2e723c.json",
    "results/labviz/site/cards/run-021115ec1b3b422b.json",
    "results/labviz/site/cards/run-022467df1b9eb7e8.json",
    "results/labviz/site/cards/run-028d548cd3531eb5.json",
    "results/labviz/site/cards/run-0293df9fb8ed60c2.json",
    "results/labviz/site/cards/run-02a22d7438026392.json",
    "results/labviz/site/cards/run-030b1a9a7459c31b.json",
    "results/labviz/site/cards/run-030d26014ba10c5f.json",
    "results/labviz/site/cards/run-0318122267c18565.json",
    "results/labviz/site/cards/run-033c704af28316e7.json",
    "results/labviz/site/cards/run-0375b74061d17d44.json",
    "results/labviz/site/cards/run-03bf760c9c7083cf.json",
    "results/labviz/site/cards/run-03d0c5336cc98da1.json",
    "results/labviz/site/cards/run-03eabb4d9f750946.json",
    "results/labviz/site/cards/run-04283bfb5608161b.json",
    "results/labviz/site/cards/run-042f290769681523.json",
    "results/labviz/site/cards/run-0446db1d0b918305.json",
    "results/labviz/site/cards/run-04cfc461edc154b7.json",
    "results/labviz/site/cards/run-05082f1bab95d192.json",
    "results/labviz/site/cards/run-0512300f00cb6c4f.json",
    "results/labviz/site/cards/run-05124ed3fa5565b1.json",
    "results/labviz/site/cards/run-052f4ad60a3709c4.json",
    "results/labviz/site/cards/run-058c34feb510381c.json",
    "results/labviz/site/cards/run-05cf4d3060a37608.json",
    "results/labviz/site/cards/run-06220cefdc77cecc.json",
    "results/labviz/site/cards/run-0640f8f5b942e32b.json",
    "results/labviz/site/cards/run-064e5a92031fce01.json",
    "results/labviz/site/cards/run-06e28c3be121ef9a.json",
    "results/labviz/site/cards/run-06e8e6f3d5c8cbb4.json",
    "results/labviz/site/cards/run-072b076b47972edd.json",
    "results/labviz/site/cards/run-07370c0df8f575b5.json",
    "results/labviz/site/cards/run-073b4044c070c777.json",
    "results/labviz/site/cards/run-077d152e025d6ab6.json",
    "results/labviz/site/cards/run-078059ae1062f499.json",
    "results/labviz/site/cards/run-07b18151791028b9.json",
    "results/labviz/site/cards/run-07c039cc39f8757d.json",
    "results/labviz/site/cards/run-07c587c4bdb35954.json",
    "results/labviz/site/cards/run-07e2a0df70a2536f.json",
    "results/labviz/site/cards/run-08166f4f204d2b09.json",
    "results/labviz/site/cards/run-089c87e8e0c1613f.json",
    "results/labviz/site/cards/run-08c9db7335f6b266.json",
    "results/labviz/site/cards/run-08f50083ad201292.json",
    "results/labviz/site/cards/run-090183641a4a1876.json",
    "results/labviz/site/cards/run-0967542ddf449f01.json",
    "results/labviz/site/cards/run-0975201813152b72.json",
    "results/labviz/site/cards/run-098916ef291d3366.json",
    "results/labviz/site/cards/run-09e482db520f49b0.json",
    "results/labviz/site/cards/run-0a351ec2d8abb60b.json",
    "results/labviz/site/cards/run-0a55bc864bde5c17.json",
    "results/labviz/site/cards/run-0a704f7bb1c8dcfa.json",
    "results/labviz/site/cards/run-0a9984c936cd5622.json",
    "results/labviz/site/cards/run-0ab99dc9069bf958.json",
    "results/labviz/site/cards/run-0b3303655dfb92fa.json",
    "results/labviz/site/cards/run-0b5e5d3bc8bcb9f9.json",
    "results/labviz/site/cards/run-0b6d0e30ad95c607.json",
    "results/labviz/site/cards/run-0b7911ad790662f5.json",
    "results/labviz/site/cards/run-0b9b937fd906b246.json",
    "results/labviz/site/cards/run-0bf3bb74f178ad2d.json",
    "results/labviz/site/cards/run-0bfe075f6994562d.json",
    "results/labviz/site/cards/run-0c46d2c506354856.json",
    "results/labviz/site/cards/run-0c80fcad8ec0bbe0.json",
    "results/labviz/site/cards/run-0c9040012390bc95.json",
    "results/labviz/site/cards/run-0cbaf90c45148626.json",
    "results/labviz/site/cards/run-0cbbb373bc5c0c02.json",
    "results/labviz/site/cards/run-0cf1152a5361cae3.json",
    "results/labviz/site/cards/run-0d192c20dad8c49a.json",
    "results/labviz/site/cards/run-0d490ae58f9e4a5a.json",
    "results/labviz/site/cards/run-0d81b0dea7e955b1.json",
    "results/labviz/site/cards/run-0e034e9833084bf2.json",
    "results/labviz/site/cards/run-0ecc292f4bd3a1b1.json",
    "results/labviz/site/cards/run-0ed655b78359d8d9.json",
    "results/labviz/site/cards/run-0ee99f7aae9f29e3.json",
    "results/labviz/site/cards/run-0ef400f8332b1f98.json",
    "results/labviz/site/cards/run-0fde991b54e0fea7.json",
    "results/labviz/site/cards/run-100cbd881005c455.json",
    "results/labviz/site/cards/run-1011eb488a5a586e.json",
    "results/labviz/site/cards/run-1012f1faf0c76ec1.json",
    "results/labviz/site/cards/run-1026d60afc20ec5f.json",
    "results/labviz/site/cards/run-103acdedc6d567ca.json",
    "results/labviz/site/cards/run-105a40d99d386e30.json",
    "results/labviz/site/cards/run-107a30899809640f.json",
    "results/labviz/site/cards/run-10f688e36146a5a9.json",
    "results/labviz/site/cards/run-110846b58034161b.json",
    "results/labviz/site/cards/run-1139253c98251e1a.json",
    "results/labviz/site/cards/run-115ce94483720f3c.json",
    "results/labviz/site/cards/run-120791b7a622b412.json",
    "results/labviz/site/cards/run-121b29c2cafd5153.json",
    "results/labviz/site/cards/run-1221d67513459aa2.json",
    "results/labviz/site/cards/run-1230250a33890f9c.json",
    "results/labviz/site/cards/run-12700b1ed61d5f87.json",
    "results/labviz/site/cards/run-12806431ba1fc690.json",
    "results/labviz/site/cards/run-129ba4ccd9031738.json",
    "results/labviz/site/cards/run-12ced5aa80e35086.json",
    "results/labviz/site/cards/run-132df0c34f36dcb8.json",
    "results/labviz/site/cards/run-1375caadd449caf7.json",
    "results/labviz/site/cards/run-1386e9ed8ef32558.json",
    "results/labviz/site/cards/run-138b0e3dd16b7af1.json",
    "results/labviz/site/cards/run-13abdbc1c5f878e1.json",
    "results/labviz/site/cards/run-14160914ceb733dc.json",
    "results/labviz/site/cards/run-1480f2da402485a4.json",
    "results/labviz/site/cards/run-1488caac4424d130.json",
    "results/labviz/site/cards/run-148a3930f4cdf6cc.json",
    "results/labviz/site/cards/run-14a1bc3e826d3008.json",
    "results/labviz/site/cards/run-14ab5d66ae4eb067.json",
    "results/labviz/site/cards/run-14d58bfdb37f4031.json",
    "results/labviz/site/cards/run-14d695c0859c8bac.json",
    "results/labviz/site/cards/run-14ed988cd2f1e45d.json",
    "results/labviz/site/cards/run-14f85941af0d3420.json",
    "results/labviz/site/cards/run-1523eb7135e5a103.json",
    "results/labviz/site/cards/run-1525d0579f653938.json",
    "results/labviz/site/cards/run-152fabeec091f581.json",
    "results/labviz/site/cards/run-156e8085aaa3c148.json",
    "results/labviz/site/cards/run-159688685f0094f5.json",
    "results/labviz/site/cards/run-15b3a91c981efa41.json",
    "results/labviz/site/cards/run-15e873cf4b090d45.json",
    "results/labviz/site/cards/run-15fa7000670ab18a.json",
    "results/labviz/site/cards/run-1655ac9b7ed354a4.json",
    "results/labviz/site/cards/run-165d5760d883ebfb.json",
    "results/labviz/site/cards/run-165fdfe3649f3f30.json",
    "results/labviz/site/cards/run-166cd58f7e5a2f84.json",
    "results/labviz/site/cards/run-16a262a3d66876e4.json",
    "results/labviz/site/cards/run-16e287086ca728f2.json",
    "results/labviz/site/cards/run-1732b89259611960.json",
    "results/labviz/site/cards/run-1759b45b66a34344.json",
    "results/labviz/site/cards/run-1780b43a950f7124.json",
    "results/labviz/site/cards/run-17880b2a513376c2.json",
    "results/labviz/site/cards/run-17b5daad61c15f99.json",
    "results/labviz/site/cards/run-17c0464ae5a15892.json",
    "results/labviz/site/cards/run-17cc2d709c661119.json",
    "results/labviz/site/cards/run-17d812e126d3e452.json",
    "results/labviz/site/cards/run-1836a44eab3dc183.json",
    "results/labviz/site/cards/run-184aac7af2e941d2.json",
    "results/labviz/site/cards/run-1884aaf15214553a.json",
    "results/labviz/site/cards/run-18918bd01e9c5bac.json",
    "results/labviz/site/cards/run-18b938480782d157.json",
    "results/labviz/site/cards/run-18cb7113a3a7cbef.json",
    "results/labviz/site/cards/run-18f8b5a3bf572ee8.json",
    "results/labviz/site/cards/run-19427ddb1c97ec73.json",
    "results/labviz/site/cards/run-195308407b9dc08c.json",
    "results/labviz/site/cards/run-195feca845e80895.json",
    "results/labviz/site/cards/run-19671058b1ba3c48.json",
    "results/labviz/site/cards/run-1971a8b5526f0898.json",
    "results/labviz/site/cards/run-199246b5b161eb4c.json",
    "results/labviz/site/cards/run-19a9e444de7fdbcd.json",
    "results/labviz/site/cards/run-19e7b569d2fdbda7.json",
    "results/labviz/site/cards/run-1a6971617c0ff058.json",
    "results/labviz/site/cards/run-1a82e999a4042311.json",
    "results/labviz/site/cards/run-1a8e9354a95fa0fe.json",
    "results/labviz/site/cards/run-1aa2d4b93f23b417.json",
    "results/labviz/site/cards/run-1abbee197dcfed9a.json",
    "results/labviz/site/cards/run-1af8c217bce01a94.json",
    "results/labviz/site/cards/run-1b36e692189233ef.json",
    "results/labviz/site/cards/run-1b5a2c56343c383a.json",
    "results/labviz/site/cards/run-1ba4f486a5c562f5.json",
    "results/labviz/site/cards/run-1bdf5df42746b91e.json",
    "results/labviz/site/cards/run-1c07fb3a7d44d3fa.json",
    "results/labviz/site/cards/run-1c580c9279ce0892.json",
    "results/labviz/site/cards/run-1cf0af4528572d10.json",
    "results/labviz/site/cards/run-1d018b6517787ba1.json",
    "results/labviz/site/cards/run-1d0d48508e9260a6.json",
    "results/labviz/site/cards/run-1d443e1a14b28ca0.json",
    "results/labviz/site/cards/run-1d50b819054445dd.json",
    "results/labviz/site/cards/run-1d71fd35ce51155d.json",
    "results/labviz/site/cards/run-1d9e480c60497a34.json",
    "results/labviz/site/cards/run-1dbbf925a6596134.json",
    "results/labviz/site/cards/run-1de61a4724e80b65.json",
    "results/labviz/site/cards/run-1e118c16a06a59b8.json",
    "results/labviz/site/cards/run-1e4c6a7d07a3913f.json",
    "results/labviz/site/cards/run-1e6c34eacebc9247.json",
    "results/labviz/site/cards/run-1e84fa50bd607ad7.json",
    "results/labviz/site/cards/run-1ec7cdc8693d2dde.json",
    "results/labviz/site/cards/run-1f3c502a40fe4b02.json",
    "results/labviz/site/cards/run-1f477ab47b3f640e.json",
    "results/labviz/site/cards/run-1f5d8a2a1d18fdbb.json",
    "results/labviz/site/cards/run-1f766e2184924420.json",
    "results/labviz/site/cards/run-1fa9fec2e2590973.json",
    "results/labviz/site/cards/run-1fe10ab1b650c1f8.json",
    "results/labviz/site/cards/run-200e5c3f23c722fc.json",
    "results/labviz/site/cards/run-2024afd165d7b088.json",
    "results/labviz/site/cards/run-2064b99d4d0b0ffc.json",
    "results/labviz/site/cards/run-206dfdbc6d3daa46.json",
    "results/labviz/site/cards/run-2082342ebcf5a4d2.json",
    "results/labviz/site/cards/run-208d53a2f6c4b888.json",
    "results/labviz/site/cards/run-20916d080a77e482.json",
    "results/labviz/site/cards/run-20abfd9555e201da.json",
    "results/labviz/site/cards/run-20b9a887d1cb1184.json",
    "results/labviz/site/cards/run-2105890879225bbf.json",
    "results/labviz/site/cards/run-2150c6789b17b3cb.json",
    "results/labviz/site/cards/run-21616de08599d17d.json",
    "results/labviz/site/cards/run-2164129a0dd83c69.json",
    "results/labviz/site/cards/run-2191ee5c123578cd.json",
    "results/labviz/site/cards/run-21950a9bbdff45c3.json",
    "results/labviz/site/cards/run-21bebb6ceae89cc8.json",
    "results/labviz/site/cards/run-224bca2b4a1afe58.json",
    "results/labviz/site/cards/run-22628f0ff993f7c6.json",
    "results/labviz/site/cards/run-22762ebf85b0e154.json",
    "results/labviz/site/cards/run-22f0b194ba18b152.json",
    "results/labviz/site/cards/run-22fd8cfe86666f04.json",
    "results/labviz/site/cards/run-2341c5234644733a.json",
    "results/labviz/site/cards/run-23c2cf3632e87f07.json",
    "results/labviz/site/cards/run-23d3548ccc79e5e9.json",
    "results/labviz/site/cards/run-23e7c6a82dfe2c29.json",
    "results/labviz/site/cards/run-2409bf429b5bf10a.json",
    "results/labviz/site/cards/run-241e4b9bb3c53ec7.json",
    "results/labviz/site/cards/run-243d5104a32669ea.json",
    "results/labviz/site/cards/run-247473f57527d44f.json",
    "results/labviz/site/cards/run-2477e80783edea78.json",
    "results/labviz/site/cards/run-248a3aa7cb38c2e9.json",
    "results/labviz/site/cards/run-2494d4a233bcb306.json",
    "results/labviz/site/cards/run-24b681ca2f25038a.json",
    "results/labviz/site/cards/run-24c02c8cb1f1c4d3.json",
    "results/labviz/site/cards/run-24f24b9a17b12422.json",
    "results/labviz/site/cards/run-250b0fca1fcef494.json",
    "results/labviz/site/cards/run-2599a0418717c9b1.json",
    "results/labviz/site/cards/run-25b60e9b362d5f55.json",
    "results/labviz/site/cards/run-25ecb2a28407bdd3.json",
    "results/labviz/site/cards/run-26146ddee32f7636.json",
    "results/labviz/site/cards/run-267a2daeb26089dd.json",
    "results/labviz/site/cards/run-2695e4e9d37f29ac.json",
    "results/labviz/site/cards/run-26ad440ac25a9712.json",
    "results/labviz/site/cards/run-26f305ac139ba5ef.json",
    "results/labviz/site/cards/run-26fff87d0c1b4317.json",
    "results/labviz/site/cards/run-2735a7d153c8e0e6.json",
    "results/labviz/site/cards/run-27b14ccc73385fdd.json",
    "results/labviz/site/cards/run-27c79539bf054441.json",
    "results/labviz/site/cards/run-282365426e143f59.json",
    "results/labviz/site/cards/run-284cd0d8d188d6ed.json",
    "results/labviz/site/cards/run-2850c7b826921b56.json",
    "results/labviz/site/cards/run-2865c5fcabaf41d9.json",
    "results/labviz/site/cards/run-287c749e2f5cd15c.json",
    "results/labviz/site/cards/run-28b6e8ee6a696128.json",
    "results/labviz/site/cards/run-28c7f6dcec6e73dc.json",
    "results/labviz/site/cards/run-290c71c6ce8c64f9.json",
    "results/labviz/site/cards/run-291d697ba59cef08.json",
    "results/labviz/site/cards/run-2943a18096b6d8b4.json",
    "results/labviz/site/cards/run-2957dd3a3c0e9596.json",
    "results/labviz/site/cards/run-295edca214720c35.json",
    "results/labviz/site/cards/run-2986d64dd5ba8ddd.json",
    "results/labviz/site/cards/run-299a9eb1126b8c63.json",
    "results/labviz/site/cards/run-29e25b2df10390e5.json",
    "results/labviz/site/cards/run-2a14084739982b04.json",
    "results/labviz/site/cards/run-2a2326090c060dd4.json",
    "results/labviz/site/cards/run-2a8f7059e486d4e0.json",
    "results/labviz/site/cards/run-2b00093b73eed15d.json",
    "results/labviz/site/cards/run-2b10dd6763225b36.json",
    "results/labviz/site/cards/run-2b73715bc313783e.json",
    "results/labviz/site/cards/run-2b78dd9a620a13ba.json",
    "results/labviz/site/cards/run-2c01a281ab77654d.json",
    "results/labviz/site/cards/run-2c78f4733aa56bb8.json",
    "results/labviz/site/cards/run-2c8554658a38ecea.json",
    "results/labviz/site/cards/run-2cd6e52cce0ad8e5.json",
    "results/labviz/site/cards/run-2d086aa7b38b059c.json",
    "results/labviz/site/cards/run-2d1da434d83536f9.json",
    "results/labviz/site/cards/run-2d2aba1bdd8df287.json",
    "results/labviz/site/cards/run-2d2bb5f7514627b0.json",
    "results/labviz/site/cards/run-2d449b7ab5fc735b.json",
    "results/labviz/site/cards/run-2d815e84ff37c5b8.json",
    "results/labviz/site/cards/run-2d83cde47f5606d6.json",
    "results/labviz/site/cards/run-2d9306e86da51fe0.json",
    "results/labviz/site/cards/run-2da2ae1bc7232e8f.json",
    "results/labviz/site/cards/run-2dbbb91e126e312e.json",
    "results/labviz/site/cards/run-2df3f0f6577b96ad.json",
    "results/labviz/site/cards/run-2e2ad795c36a10ab.json",
    "results/labviz/site/cards/run-2e2c13765b6fc4dd.json",
    "results/labviz/site/cards/run-2e3ac3c4e83e6637.json",
    "results/labviz/site/cards/run-2e957b879abb40f7.json",
    "results/labviz/site/cards/run-2ed5d194be072bab.json",
    "results/labviz/site/cards/run-2f6b185bdb9a5c3e.json",
    "results/labviz/site/cards/run-2f931c4ced3b039c.json",
    "results/labviz/site/cards/run-2fa6f33e2f5763dc.json",
    "results/labviz/site/cards/run-2fb0a140df2d8234.json",
    "results/labviz/site/cards/run-2fb47107ec79d2ec.json",
    "results/labviz/site/cards/run-2fbdcfdf51b03dba.json",
    "results/labviz/site/cards/run-2fe978e86216c626.json",
    "results/labviz/site/cards/run-3005727130989007.json",
    "results/labviz/site/cards/run-301205d9fe3d85bf.json",
    "results/labviz/site/cards/run-30627cf1aa186955.json",
    "results/labviz/site/cards/run-3066789a29260119.json",
    "results/labviz/site/cards/run-309b24a10bd32a30.json",
    "results/labviz/site/cards/run-30f36411a65218e2.json",
    "results/labviz/site/cards/run-314338272fc1e445.json",
    "results/labviz/site/cards/run-317d55d112853546.json",
    "results/labviz/site/cards/run-31c7fff7d6ed6323.json",
    "results/labviz/site/cards/run-320a5b6b2684013a.json",
    "results/labviz/site/cards/run-3241ab8a9e997d35.json",
    "results/labviz/site/cards/run-3264317a0fd53d27.json",
    "results/labviz/site/cards/run-32b620eda3d57298.json",
    "results/labviz/site/cards/run-32be289c89ffb81c.json",
    "results/labviz/site/cards/run-32f3ea4b69e5cfd8.json",
    "results/labviz/site/cards/run-331e7c7dacd3447b.json",
    "results/labviz/site/cards/run-332ee993771e35e6.json",
    "results/labviz/site/cards/run-3347a564062af517.json",
    "results/labviz/site/cards/run-334bf63ac5a5bade.json",
    "results/labviz/site/cards/run-338019a55a0b3806.json",
    "results/labviz/site/cards/run-3393931d72001f4e.json",
    "results/labviz/site/cards/run-3397cd376240bfa2.json",
    "results/labviz/site/cards/run-341aa6acdc6e5cc2.json",
    "results/labviz/site/cards/run-3425dd9bb6258de9.json",
    "results/labviz/site/cards/run-3429331b905bae04.json",
    "results/labviz/site/cards/run-342c03363049dc41.json",
    "results/labviz/site/cards/run-3468ae2336aab8ef.json",
    "results/labviz/site/cards/run-3468c95fe01e90be.json",
    "results/labviz/site/cards/run-34a254348a9854ca.json",
    "results/labviz/site/cards/run-34d003be45425d8c.json",
    "results/labviz/site/cards/run-34e27d64c38b9251.json",
    "results/labviz/site/cards/run-351a87d5f1b08ed6.json",
    "results/labviz/site/cards/run-353caf34f88c9d7b.json",
    "results/labviz/site/cards/run-3579e64a3c7f4c37.json",
    "results/labviz/site/cards/run-358c4f95eee65b33.json",
    "results/labviz/site/cards/run-35cde3e787cc4fc8.json",
    "results/labviz/site/cards/run-360a6b7795cb2c34.json",
    "results/labviz/site/cards/run-361e462fae289258.json",
    "results/labviz/site/cards/run-365648f74ed1873f.json",
    "results/labviz/site/cards/run-366783de54c80a49.json",
    "results/labviz/site/cards/run-36e719b645ff93fb.json",
    "results/labviz/site/cards/run-372eb65d592b42d9.json",
    "results/labviz/site/cards/run-376a669707ca8c22.json",
    "results/labviz/site/cards/run-3780c817f2036337.json",
    "results/labviz/site/cards/run-37813e24b45dfc80.json",
    "results/labviz/site/cards/run-3784c2fe9e46587f.json",
    "results/labviz/site/cards/run-37c81366c818a136.json",
    "results/labviz/site/cards/run-37d1522260c85256.json",
    "results/labviz/site/cards/run-37e17950be8805c1.json",
    "results/labviz/site/cards/run-37f0379987887405.json",
    "results/labviz/site/cards/run-37fd2fd78e12a157.json",
    "results/labviz/site/cards/run-38020adfae2614bc.json",
    "results/labviz/site/cards/run-3869116348e4651d.json",
    "results/labviz/site/cards/run-38ceccb089bfbb0c.json",
    "results/labviz/site/cards/run-38eac20681f3bfe1.json",
    "results/labviz/site/cards/run-38f1d7dee69414ee.json",
    "results/labviz/site/cards/run-391cc8fd555bd15b.json",
    "results/labviz/site/cards/run-392ca9c7b01962ce.json",
    "results/labviz/site/cards/run-394881173840b5fd.json",
    "results/labviz/site/cards/run-39731f41ac2a830e.json",
    "results/labviz/site/cards/run-39b47dbbab332e0e.json",
    "results/labviz/site/cards/run-39f104a913b96eee.json",
    "results/labviz/site/cards/run-39f284b5d366f3a2.json",
    "results/labviz/site/cards/run-3a711df1728d122b.json",
    "results/labviz/site/cards/run-3a7138e9a606d4c7.json",
    "results/labviz/site/cards/run-3a8de214bda658d7.json",
    "results/labviz/site/cards/run-3ac3c60a37f07bce.json",
    "results/labviz/site/cards/run-3ad2bbeb3e23d03d.json",
    "results/labviz/site/cards/run-3ad7de6186bef8c4.json",
    "results/labviz/site/cards/run-3afab089e80351c9.json",
    "results/labviz/site/cards/run-3b4a3258d041999d.json",
    "results/labviz/site/cards/run-3b74c3f4628b9fe0.json",
    "results/labviz/site/cards/run-3b92c6310ee143fa.json",
    "results/labviz/site/cards/run-3ba70d001960d844.json",
    "results/labviz/site/cards/run-3bb0761d63b69ba8.json",
    "results/labviz/site/cards/run-3bc416ab2f5d4042.json",
    "results/labviz/site/cards/run-3bfc6a4d447a2504.json",
    "results/labviz/site/cards/run-3c0403e326323f24.json",
    "results/labviz/site/cards/run-3c08c8b688787c9f.json",
    "results/labviz/site/cards/run-3c2b213b333ea777.json",
    "results/labviz/site/cards/run-3c602e0d73cf2cfd.json",
    "results/labviz/site/cards/run-3cc50f1a0ccc7fa8.json",
    "results/labviz/site/cards/run-3d03ddde898507d0.json",
    "results/labviz/site/cards/run-3d484ae7aadca0a6.json",
    "results/labviz/site/cards/run-3d4d292740f60e97.json",
    "results/labviz/site/cards/run-3d7a3f4443db8bed.json",
    "results/labviz/site/cards/run-3d8e1099342cf16e.json",
    "results/labviz/site/cards/run-3d906ca47ed5f654.json",
    "results/labviz/site/cards/run-3e057bb72f897537.json",
    "results/labviz/site/cards/run-3e6732ec9fe01e79.json",
    "results/labviz/site/cards/run-3e67c94c2fe810fa.json",
    "results/labviz/site/cards/run-3ec0d4acefd0a69a.json",
    "results/labviz/site/cards/run-3ed2342ae22ab557.json",
    "results/labviz/site/cards/run-3edf5f650db34018.json",
    "results/labviz/site/cards/run-3f5c048757f05df4.json",
    "results/labviz/site/cards/run-3f61b03542da2587.json",
    "results/labviz/site/cards/run-3f8292a1c483f16d.json",
    "results/labviz/site/cards/run-3f9f9e3cb9e9535d.json",
    "results/labviz/site/cards/run-3fb483ff0a85367f.json",
    "results/labviz/site/cards/run-3fef33337e1e91a7.json",
    "results/labviz/site/cards/run-40195b7df848f4e4.json",
    "results/labviz/site/cards/run-402cd7bfd3c34288.json",
    "results/labviz/site/cards/run-40376027cddf3ef7.json",
    "results/labviz/site/cards/run-408fe3764dc17c32.json",
    "results/labviz/site/cards/run-40a5d9bd932867d3.json",
    "results/labviz/site/cards/run-40d911e8fc2c84e3.json",
    "results/labviz/site/cards/run-40e2ecb41d6df619.json",
    "results/labviz/site/cards/run-40e5b8d28939a095.json",
    "results/labviz/site/cards/run-4161c3354a3d4fdc.json",
    "results/labviz/site/cards/run-417bc6b8b20f4395.json",
    "results/labviz/site/cards/run-418bffcd3a539beb.json",
    "results/labviz/site/cards/run-41b320498e7015c2.json",
    "results/labviz/site/cards/run-41bb716f62f67c7e.json",
    "results/labviz/site/cards/run-41de64bcc7a818f4.json",
    "results/labviz/site/cards/run-41e69c6e3ac72f45.json",
    "results/labviz/site/cards/run-41eaf9e3e5ac7529.json",
    "results/labviz/site/cards/run-41f8b56bde5ff7fd.json",
    "results/labviz/site/cards/run-42186a9ecb67bd5c.json",
    "results/labviz/site/cards/run-4227660b202a47d0.json",
    "results/labviz/site/cards/run-4237b6e6b7121606.json",
    "results/labviz/site/cards/run-423c25ab481b6cdf.json",
    "results/labviz/site/cards/run-4240e05af357126e.json",
    "results/labviz/site/cards/run-426f6001b89a0fa6.json",
    "results/labviz/site/cards/run-42704f1c09d15a4d.json",
    "results/labviz/site/cards/run-42b8e536ee83bd2c.json",
    "results/labviz/site/cards/run-42ceff7c025bb16e.json",
    "results/labviz/site/cards/run-42ebb251a7601adb.json",
    "results/labviz/site/cards/run-4309082386eb49c2.json",
    "results/labviz/site/cards/run-431c40ed4c95bef5.json",
    "results/labviz/site/cards/run-435f2b7ecc6ef3a1.json",
    "results/labviz/site/cards/run-43997ae675f8e079.json",
    "results/labviz/site/cards/run-4414f3b0641562cf.json",
    "results/labviz/site/cards/run-44179b8897640f08.json",
    "results/labviz/site/cards/run-44799173034ffc3f.json",
    "results/labviz/site/cards/run-4498ad22147d69e7.json",
    "results/labviz/site/cards/run-44acd672174bfa71.json",
    "results/labviz/site/cards/run-44fea5d906f50034.json",
    "results/labviz/site/cards/run-451ca30e4ac00237.json",
    "results/labviz/site/cards/run-452bdbd755c7e9c1.json",
    "results/labviz/site/cards/run-457f17d34a0103a4.json",
    "results/labviz/site/cards/run-45a214957132f82c.json",
    "results/labviz/site/cards/run-45e99aaba2816897.json",
    "results/labviz/site/cards/run-460797fba25947f7.json",
    "results/labviz/site/cards/run-46a507b32c1b66dc.json",
    "results/labviz/site/cards/run-46a70757eca3693e.json",
    "results/labviz/site/cards/run-46ae8accb93433f9.json",
    "results/labviz/site/cards/run-46b0a5561c1b73ce.json",
    "results/labviz/site/cards/run-46ece29c3263ee5c.json",
    "results/labviz/site/cards/run-46ee4a92ffb5a412.json",
    "results/labviz/site/cards/run-4711f67b88472b24.json",
    "results/labviz/site/cards/run-472eea29ac33d638.json",
    "results/labviz/site/cards/run-47a89b05273403ad.json",
    "results/labviz/site/cards/run-47d4708331916ca2.json",
    "results/labviz/site/cards/run-47ed645ddea37da8.json",
    "results/labviz/site/cards/run-4803852fcfeed0bd.json",
    "results/labviz/site/cards/run-48088694b246db13.json",
    "results/labviz/site/cards/run-4866cd10a4f02e86.json",
    "results/labviz/site/cards/run-487645691c5fd245.json",
    "results/labviz/site/cards/run-4897514ce6063de6.json",
    "results/labviz/site/cards/run-4898057b2c60207e.json",
    "results/labviz/site/cards/run-48be248a1d824b53.json",
    "results/labviz/site/cards/run-48e03328246f9258.json",
    "results/labviz/site/cards/run-49433dd8f4420e65.json",
    "results/labviz/site/cards/run-4952bca765b33a4d.json",
    "results/labviz/site/cards/run-495f3b3ffbca09dc.json",
    "results/labviz/site/cards/run-497384e05f0a8f27.json",
    "results/labviz/site/cards/run-49834969f3d8eca5.json",
    "results/labviz/site/cards/run-49f7a13084c81b64.json",
    "results/labviz/site/cards/run-49fc5c8d45b33ce5.json",
    "results/labviz/site/cards/run-4a1620c81e1476d2.json",
    "results/labviz/site/cards/run-4a4dbf2d30f91fbc.json",
    "results/labviz/site/cards/run-4a7deb04837833e5.json",
    "results/labviz/site/cards/run-4a9f213a0d9f52f5.json",
    "results/labviz/site/cards/run-4ad8c01d776774bd.json",
    "results/labviz/site/cards/run-4afc0b01857ad7f6.json",
    "results/labviz/site/cards/run-4b03ee2ec4f232c6.json",
    "results/labviz/site/cards/run-4b04c702abb52df9.json",
    "results/labviz/site/cards/run-4b04dd12a081d1c1.json",
    "results/labviz/site/cards/run-4b0fd99a2e0c0899.json",
    "results/labviz/site/cards/run-4b11e613c1c8fe4a.json",
    "results/labviz/site/cards/run-4b2f40049ac6408f.json",
    "results/labviz/site/cards/run-4b35cbb3a1efc66f.json",
    "results/labviz/site/cards/run-4b57aab3e2a93136.json",
    "results/labviz/site/cards/run-4b691c3165a1bf9e.json",
    "results/labviz/site/cards/run-4b8b54917ae63eb8.json",
    "results/labviz/site/cards/run-4ba81f4ed6bf6ebd.json",
    "results/labviz/site/cards/run-4ba9acdb634bcbc8.json",
    "results/labviz/site/cards/run-4babea8c5680f6b9.json",
    "results/labviz/site/cards/run-4bc2db3909d4f0ec.json",
    "results/labviz/site/cards/run-4bc925207aacd954.json",
    "results/labviz/site/cards/run-4bdff984858c2ba8.json",
    "results/labviz/site/cards/run-4bf6651764151d73.json",
    "results/labviz/site/cards/run-4c1d29ec9ac69b95.json",
    "results/labviz/site/cards/run-4c70a54f27c618fc.json",
    "results/labviz/site/cards/run-4c9254d95b58da74.json",
    "results/labviz/site/cards/run-4c9af6db82289a2f.json",
    "results/labviz/site/cards/run-4ca8a65611e8764f.json",
    "results/labviz/site/cards/run-4d05048106f21a80.json",
    "results/labviz/site/cards/run-4d59d5e6146d81ce.json",
    "results/labviz/site/cards/run-4dc5663e186f212a.json",
    "results/labviz/site/cards/run-4dc966d9634f8b8d.json",
    "results/labviz/site/cards/run-4dd3bdbdc34654c9.json",
    "results/labviz/site/cards/run-4e1352dabc60b9d3.json",
    "results/labviz/site/cards/run-4e3245cf65654724.json",
    "results/labviz/site/cards/run-4e3c184db81d9582.json",
    "results/labviz/site/cards/run-4e3cf64a9b64ac83.json",
    "results/labviz/site/cards/run-4e4b522b5a1249c9.json",
    "results/labviz/site/cards/run-4e945abe0e71d16b.json",
    "results/labviz/site/cards/run-4ec5d6243263bdcb.json",
    "results/labviz/site/cards/run-4ecdf5416af0a622.json",
    "results/labviz/site/cards/run-4ef03a3cc16b0cba.json",
    "results/labviz/site/cards/run-4ef537cb6aae5976.json",
    "results/labviz/site/cards/run-4f0f8866f4f04d39.json",
    "results/labviz/site/cards/run-4f43bfa18137fa85.json",
    "results/labviz/site/cards/run-4f73d2f7415573eb.json",
    "results/labviz/site/cards/run-4fcd7cd7d72ce841.json",
    "results/labviz/site/cards/run-4ff6ec65c7872945.json",
    "results/labviz/site/cards/run-50197c0a409ac9ce.json",
    "results/labviz/site/cards/run-50335ef007f1233c.json",
    "results/labviz/site/cards/run-50caf62ecd50638a.json",
    "results/labviz/site/cards/run-50e4a103cb7c64bf.json",
    "results/labviz/site/cards/run-510baa1c1d8e6ce8.json",
    "results/labviz/site/cards/run-514b97b9d538534e.json",
    "results/labviz/site/cards/run-514dc519197fadfe.json",
    "results/labviz/site/cards/run-516f0f7cac84f6e2.json",
    "results/labviz/site/cards/run-517ecfcaaa52f417.json",
    "results/labviz/site/cards/run-51bd013c988b613e.json",
    "results/labviz/site/cards/run-51d7357221f98d91.json",
    "results/labviz/site/cards/run-51fabec4481c09dd.json",
    "results/labviz/site/cards/run-5210de88e082f2ff.json",
    "results/labviz/site/cards/run-52249d604e01a0a1.json",
    "results/labviz/site/cards/run-52276258f2d9270e.json",
    "results/labviz/site/cards/run-5231342e030b9c6a.json",
    "results/labviz/site/cards/run-5252a8e38ce58461.json",
    "results/labviz/site/cards/run-526068d23ec911e8.json",
    "results/labviz/site/cards/run-528f9620973afb1e.json",
    "results/labviz/site/cards/run-52a45562d0abb270.json",
    "results/labviz/site/cards/run-52b39f4c311d179a.json",
    "results/labviz/site/cards/run-52d2d5280102bfaa.json",
    "results/labviz/site/cards/run-53a57577a2ff8e5c.json",
    "results/labviz/site/cards/run-53be7fa092ae5e89.json",
    "results/labviz/site/cards/run-53c137795458f04e.json",
    "results/labviz/site/cards/run-54075de0770de754.json",
    "results/labviz/site/cards/run-544a849af298aadc.json",
    "results/labviz/site/cards/run-5470d2def2831374.json",
    "results/labviz/site/cards/run-5486e0a215bf57ac.json",
    "results/labviz/site/cards/run-54983be6f8d223d4.json",
    "results/labviz/site/cards/run-54b49f917328ca7b.json",
    "results/labviz/site/cards/run-54bbdf7a49e1cc88.json",
    "results/labviz/site/cards/run-55031cb066869b9f.json",
    "results/labviz/site/cards/run-550e01dac00059a9.json",
    "results/labviz/site/cards/run-5518d0d2c277a019.json",
    "results/labviz/site/cards/run-55276acfcd8fc702.json",
    "results/labviz/site/cards/run-55b3b7b06d204449.json",
    "results/labviz/site/cards/run-561d341fa3af9b53.json",
    "results/labviz/site/cards/run-56a431e2272584f9.json",
    "results/labviz/site/cards/run-56a596d0b4e81a16.json",
    "results/labviz/site/cards/run-570b30c8cd399016.json",
    "results/labviz/site/cards/run-571287f1f831ade1.json",
    "results/labviz/site/cards/run-576a0e430ed19f7e.json",
    "results/labviz/site/cards/run-579d170522cb2082.json",
    "results/labviz/site/cards/run-57cd2cd5a241bc14.json",
    "results/labviz/site/cards/run-57e7b3ab5d2d5116.json",
    "results/labviz/site/cards/run-57f77681f7ac9dd8.json",
    "results/labviz/site/cards/run-5838a23408eadd25.json",
    "results/labviz/site/cards/run-58815beae4b5b969.json",
    "results/labviz/site/cards/run-58accb6d8e1a5e06.json",
    "results/labviz/site/cards/run-59077eecc92e68b9.json",
    "results/labviz/site/cards/run-592138ae02d2de1b.json",
    "results/labviz/site/cards/run-595c91c2a5020de0.json",
    "results/labviz/site/cards/run-595f14473ddc7ebb.json",
    "results/labviz/site/cards/run-596083a0fa1e21d5.json",
    "results/labviz/site/cards/run-597283d89b1b61a3.json",
    "results/labviz/site/cards/run-59e93f4fd4eaf860.json",
    "results/labviz/site/cards/run-5a0279876bcc9e30.json",
    "results/labviz/site/cards/run-5a426d58d13d6141.json",
    "results/labviz/site/cards/run-5a469ccfe400f219.json",
    "results/labviz/site/cards/run-5a596ae332035fa6.json",
    "results/labviz/site/cards/run-5a59d8a73252999a.json",
    "results/labviz/site/cards/run-5a65bacb8097f59c.json",
    "results/labviz/site/cards/run-5a9d0de7076f0e93.json",
    "results/labviz/site/cards/run-5aa1f7421484f80a.json",
    "results/labviz/site/cards/run-5abb5be21763e494.json",
    "results/labviz/site/cards/run-5b0f2528be65e77c.json",
    "results/labviz/site/cards/run-5b4991a3c720447c.json",
    "results/labviz/site/cards/run-5b756a2071daf82f.json",
    "results/labviz/site/cards/run-5b88a60672c46280.json",
    "results/labviz/site/cards/run-5b98b9a1e9966f9e.json",
    "results/labviz/site/cards/run-5c02222726b6fca9.json",
    "results/labviz/site/cards/run-5c0c71f18ee4ecdd.json",
    "results/labviz/site/cards/run-5c3c7c99b7f8a245.json",
    "results/labviz/site/cards/run-5c48804edd914547.json",
    "results/labviz/site/cards/run-5c71e1dadfb5ad91.json",
    "results/labviz/site/cards/run-5c7e1bd8f9ce862e.json",
    "results/labviz/site/cards/run-5c850209af059e17.json",
    "results/labviz/site/cards/run-5ca4f70766bddb1f.json",
    "results/labviz/site/cards/run-5cae247d2d477c04.json",
    "results/labviz/site/cards/run-5ccb97dc669d33f4.json",
    "results/labviz/site/cards/run-5ce671b5337af14d.json",
    "results/labviz/site/cards/run-5cf63dd7406f856f.json",
    "results/labviz/site/cards/run-5d1acea18cc594ce.json",
    "results/labviz/site/cards/run-5d5d78fe394c1213.json",
    "results/labviz/site/cards/run-5d891875797f447a.json",
    "results/labviz/site/cards/run-5d98ba367f7ae2a6.json",
    "results/labviz/site/cards/run-5dfa04fe559fd4be.json",
    "results/labviz/site/cards/run-5e1601800b3f001b.json",
    "results/labviz/site/cards/run-5e165c432f2e4853.json",
    "results/labviz/site/cards/run-5e3d574340e1decb.json",
    "results/labviz/site/cards/run-5e7ae791ce92ec00.json",
    "results/labviz/site/cards/run-5e89b93884495469.json",
    "results/labviz/site/cards/run-5e920bf0621ccc7a.json",
    "results/labviz/site/cards/run-5ea0f8b79ab08484.json",
    "results/labviz/site/cards/run-5eb0df689c1a876f.json",
    "results/labviz/site/cards/run-5ec8a1db0f492812.json",
    "results/labviz/site/cards/run-5ef75d0a9d34c4f0.json",
    "results/labviz/site/cards/run-5f8aa28bf751da4a.json",
    "results/labviz/site/cards/run-5faa9a409f24d172.json",
    "results/labviz/site/cards/run-5fdbcb32690abe42.json",
    "results/labviz/site/cards/run-5fde551914151c96.json",
    "results/labviz/site/cards/run-5fe6e89017081b60.json",
    "results/labviz/site/cards/run-5ff588271e926b62.json",
    "results/labviz/site/cards/run-601563f92d3d0786.json",
    "results/labviz/site/cards/run-604c67e8318d2976.json",
    "results/labviz/site/cards/run-60ce7b91b88550d7.json",
    "results/labviz/site/cards/run-60d48886a99d3747.json",
    "results/labviz/site/cards/run-60ddcdc217a67c1a.json",
    "results/labviz/site/cards/run-61148faf2e1df52b.json",
    "results/labviz/site/cards/run-614952bc08deca86.json",
    "results/labviz/site/cards/run-6180715a00449191.json",
    "results/labviz/site/cards/run-618b6d5aed16642d.json",
    "results/labviz/site/cards/run-61975bd65a2d0e9b.json",
    "results/labviz/site/cards/run-61a0e386079467a5.json",
    "results/labviz/site/cards/run-61a69ab8ccca7808.json",
    "results/labviz/site/cards/run-61c5cf264688320b.json",
    "results/labviz/site/cards/run-61e0e5c7a1038ffe.json",
    "results/labviz/site/cards/run-61fc12b814cf7786.json",
    "results/labviz/site/cards/run-626c1720c744299b.json",
    "results/labviz/site/cards/run-627e2fdeed71d88c.json",
    "results/labviz/site/cards/run-6293909f7061fe2b.json",
    "results/labviz/site/cards/run-62a41fb34d78471e.json",
    "results/labviz/site/cards/run-62ac128f91b35854.json",
    "results/labviz/site/cards/run-62d21f1de8326576.json",
    "results/labviz/site/cards/run-63443ca8fd697123.json",
    "results/labviz/site/cards/run-6381a0b3547fd10f.json",
    "results/labviz/site/cards/run-639369afb0a49354.json",
    "results/labviz/site/cards/run-63aa2b1d6d90b0da.json",
    "results/labviz/site/cards/run-63b1f38ce8a0ce5e.json",
    "results/labviz/site/cards/run-63c151c80071623b.json",
    "results/labviz/site/cards/run-63c5e44eb47eb4b9.json",
    "results/labviz/site/cards/run-63c8e38f6281d5dd.json",
    "results/labviz/site/cards/run-640a85c457ca0d50.json",
    "results/labviz/site/cards/run-64668b12755314f1.json",
    "results/labviz/site/cards/run-64771a19facee289.json",
    "results/labviz/site/cards/run-64a3a5db925f284f.json",
    "results/labviz/site/cards/run-64da421dc22a0141.json",
    "results/labviz/site/cards/run-64e7c4c1bbe99a73.json",
    "results/labviz/site/cards/run-6583c955f7e42753.json",
    "results/labviz/site/cards/run-65d2053ae7b3262f.json",
    "results/labviz/site/cards/run-65f96b83ab0bd3dd.json",
    "results/labviz/site/cards/run-65fb6542ac96758e.json",
    "results/labviz/site/cards/run-65ffe31a90dc1df0.json",
    "results/labviz/site/cards/run-662501d13c0e4b0a.json",
    "results/labviz/site/cards/run-663e50db65cd56d0.json",
    "results/labviz/site/cards/run-664e1e8e6fae8a9f.json",
    "results/labviz/site/cards/run-6674daafc78e3452.json",
    "results/labviz/site/cards/run-66fb88b7c8c945b4.json",
    "results/labviz/site/cards/run-67024ac3823a93d6.json",
    "results/labviz/site/cards/run-670baa05d203d58b.json",
    "results/labviz/site/cards/run-6734e771eccc264b.json",
    "results/labviz/site/cards/run-6746bef0c2e14ebe.json",
    "results/labviz/site/cards/run-677f3ccff1cfef07.json",
    "results/labviz/site/cards/run-6792dcbf44fa656b.json",
    "results/labviz/site/cards/run-67e01a577e62caf9.json",
    "results/labviz/site/cards/run-67ef21f3b72f2d0f.json",
    "results/labviz/site/cards/run-67fddd107944b36d.json",
    "results/labviz/site/cards/run-6815a950dfb195d0.json",
    "results/labviz/site/cards/run-681d1059bdff9666.json",
    "results/labviz/site/cards/run-683fb43efce6f197.json",
    "results/labviz/site/cards/run-684bc3e3bdbb57b7.json",
    "results/labviz/site/cards/run-689cf09befa057c0.json",
    "results/labviz/site/cards/run-68a3202a08b816f9.json",
    "results/labviz/site/cards/run-68a642854fd5696b.json",
    "results/labviz/site/cards/run-68c27a3b1ae45f29.json",
    "results/labviz/site/cards/run-68eb3b82a4cba371.json",
    "results/labviz/site/cards/run-68f78f3967614c47.json",
    "results/labviz/site/cards/run-68fc5a3ba0a3b9c2.json",
    "results/labviz/site/cards/run-6902ccd3a4fd9f2f.json",
    "results/labviz/site/cards/run-693e9a46d43bbf0a.json",
    "results/labviz/site/cards/run-694ff0123683b3dd.json",
    "results/labviz/site/cards/run-6968f20829c393cc.json",
    "results/labviz/site/cards/run-69a17e80d12f8783.json",
    "results/labviz/site/cards/run-6aa0d6716e639ab2.json",
    "results/labviz/site/cards/run-6adde294ad4a6296.json",
    "results/labviz/site/cards/run-6ae3104ca8355a37.json",
    "results/labviz/site/cards/run-6b0b29945f4b17c5.json",
    "results/labviz/site/cards/run-6b22b1a4ca7fd4ce.json",
    "results/labviz/site/cards/run-6b3c7a4ccecc68d0.json",
    "results/labviz/site/cards/run-6b60d2cdaf96fc5c.json",
    "results/labviz/site/cards/run-6b70567f673a2416.json",
    "results/labviz/site/cards/run-6b75c43881e24890.json",
    "results/labviz/site/cards/run-6b7bb3da3665a7c7.json",
    "results/labviz/site/cards/run-6b8bcb30474ecdef.json",
    "results/labviz/site/cards/run-6bd7bafc14ae2348.json",
    "results/labviz/site/cards/run-6c1445fd81584244.json",
    "results/labviz/site/cards/run-6c391f62842efe82.json",
    "results/labviz/site/cards/run-6c3fac7a4f9e4475.json",
    "results/labviz/site/cards/run-6c55e3d2b4f79a92.json",
    "results/labviz/site/cards/run-6c69c836960d1688.json",
    "results/labviz/site/cards/run-6c74a9d463b8105a.json",
    "results/labviz/site/cards/run-6c77ad8a742cd733.json",
    "results/labviz/site/cards/run-6c8c7d7e24064146.json",
    "results/labviz/site/cards/run-6cfe791dad1b5a18.json",
    "results/labviz/site/cards/run-6d1fd7fca8bda363.json",
    "results/labviz/site/cards/run-6dda380e48fb2f13.json",
    "results/labviz/site/cards/run-6e06b750f68f4b02.json",
    "results/labviz/site/cards/run-6e3dc75115c9d770.json",
    "results/labviz/site/cards/run-6e494b0bdeaba041.json",
    "results/labviz/site/cards/run-6ed0f6d175a56df6.json",
    "results/labviz/site/cards/run-6f322a19cc492bf0.json",
    "results/labviz/site/cards/run-6f5164a0e1ef4e34.json",
    "results/labviz/site/cards/run-6f65c4cad4d12972.json",
    "results/labviz/site/cards/run-6f7247ee181b9d8e.json",
    "results/labviz/site/cards/run-6fcbdd4d6ae0a565.json",
    "results/labviz/site/cards/run-701cc50d91b01eff.json",
    "results/labviz/site/cards/run-7020e609e290721f.json",
    "results/labviz/site/cards/run-70332d7ed4adbc51.json",
    "results/labviz/site/cards/run-704ad61a0dbee3d0.json",
    "results/labviz/site/cards/run-70720bae4c2ba293.json",
    "results/labviz/site/cards/run-70b281545f807852.json",
    "results/labviz/site/cards/run-70bdb08de39dea3e.json",
    "results/labviz/site/cards/run-7108e8c3a6d63474.json",
    "results/labviz/site/cards/run-710e0e031af1335a.json",
    "results/labviz/site/cards/run-712b0039e1e861dc.json",
    "results/labviz/site/cards/run-715ac7cb32b6c978.json",
    "results/labviz/site/cards/run-71ef8ec446ae5865.json",
    "results/labviz/site/cards/run-71f4c53b49ffa63a.json",
    "results/labviz/site/cards/run-72078ca5cae8160d.json",
    "results/labviz/site/cards/run-721ee300104d8bf2.json",
    "results/labviz/site/cards/run-724a7714215aecc8.json",
    "results/labviz/site/cards/run-728732717a1a75f2.json",
    "results/labviz/site/cards/run-72b597190a936963.json",
    "results/labviz/site/cards/run-72b9aaf4dca4d2b6.json",
    "results/labviz/site/cards/run-734fa6655a81dca0.json",
    "results/labviz/site/cards/run-7382f4034d7d92a1.json",
    "results/labviz/site/cards/run-73aa60536a2277d4.json",
    "results/labviz/site/cards/run-7405fc6247402383.json",
    "results/labviz/site/cards/run-74229cd034cb53f6.json",
    "results/labviz/site/cards/run-74f26dd1cd41910a.json",
    "results/labviz/site/cards/run-74fa161ef313f675.json",
    "results/labviz/site/cards/run-7522a8313fa798a1.json",
    "results/labviz/site/cards/run-754f43aeaf1e74c2.json",
    "results/labviz/site/cards/run-758cd628190fc564.json",
    "results/labviz/site/cards/run-75a5ef130258a27d.json",
    "results/labviz/site/cards/run-75d142058b420ecb.json",
    "results/labviz/site/cards/run-75d67cbc936763d0.json",
    "results/labviz/site/cards/run-75fe8d95905c9090.json",
    "results/labviz/site/cards/run-762c4ad2192a9241.json",
    "results/labviz/site/cards/run-7662036559fe50f0.json",
    "results/labviz/site/cards/run-76705f45ead8e5b6.json",
    "results/labviz/site/cards/run-76ac1e389e9a7453.json",
    "results/labviz/site/cards/run-76b9a870955fc84a.json",
    "results/labviz/site/cards/run-76ceb14bdf4267e3.json",
    "results/labviz/site/cards/run-76dea29ff62dde28.json",
    "results/labviz/site/cards/run-76edefaf89c629f0.json",
    "results/labviz/site/cards/run-772298573816149f.json",
    "results/labviz/site/cards/run-772e86ff4c0f08e4.json",
    "results/labviz/site/cards/run-77662233f7612389.json",
    "results/labviz/site/cards/run-77870ecf22696d94.json",
    "results/labviz/site/cards/run-778f6ee711a5b12a.json",
    "results/labviz/site/cards/run-77c89589c0ae04ae.json",
    "results/labviz/site/cards/run-77cbdfb4c29f8bfb.json",
    "results/labviz/site/cards/run-77f5460aaa04114c.json",
    "results/labviz/site/cards/run-781e41ec5c76cbf8.json",
    "results/labviz/site/cards/run-7832b34c1937143f.json",
    "results/labviz/site/cards/run-7862165248ce30c2.json",
    "results/labviz/site/cards/run-787397da30913bda.json",
    "results/labviz/site/cards/run-788d552f3a0df253.json",
    "results/labviz/site/cards/run-78b5aec05f27db60.json",
    "results/labviz/site/cards/run-78b96144be65b6bf.json",
    "results/labviz/site/cards/run-7929b7eca07aca08.json",
    "results/labviz/site/cards/run-79a181da54077260.json",
    "results/labviz/site/cards/run-79ad38d4bbe65a40.json",
    "results/labviz/site/cards/run-79b7b466befda551.json",
    "results/labviz/site/cards/run-79ca1fdb6f53f401.json",
    "results/labviz/site/cards/run-7a61b8469dcb07d9.json",
    "results/labviz/site/cards/run-7a8c85be3abaa568.json",
    "results/labviz/site/cards/run-7ab3a48ef0582c7a.json",
    "results/labviz/site/cards/run-7af3c6b69cf44a38.json",
    "results/labviz/site/cards/run-7b5e1c1fa3321232.json",
    "results/labviz/site/cards/run-7b87704a77dd5f41.json",
    "results/labviz/site/cards/run-7bdfa7a0c96bcff0.json",
    "results/labviz/site/cards/run-7c53dd9c4200cd8f.json",
    "results/labviz/site/cards/run-7c83d76df58f8d32.json",
    "results/labviz/site/cards/run-7ca7c4ae2dd4919b.json",
    "results/labviz/site/cards/run-7cc857f9344f910e.json",
    "results/labviz/site/cards/run-7d387975437c79cc.json",
    "results/labviz/site/cards/run-7d6860fb27e828ca.json",
    "results/labviz/site/cards/run-7d7e63183c5f7287.json",
    "results/labviz/site/cards/run-7d8cf8c1706c4980.json",
    "results/labviz/site/cards/run-7d9cbf1eb29a9663.json",
    "results/labviz/site/cards/run-7dbbbf98855e90b1.json",
    "results/labviz/site/cards/run-7dd16d93fda4be5a.json",
    "results/labviz/site/cards/run-7df578ab2117995e.json",
    "results/labviz/site/cards/run-7e51eb2b8ffccdd5.json",
    "results/labviz/site/cards/run-7e658c725b564391.json",
    "results/labviz/site/cards/run-7e68369c4dc96827.json",
    "results/labviz/site/cards/run-7e7754a7d4207b41.json",
    "results/labviz/site/cards/run-7e7cb9e8c09c6d9b.json",
    "results/labviz/site/cards/run-7eec7b6ca15a9c43.json",
    "results/labviz/site/cards/run-7f23f492f7dbf497.json",
    "results/labviz/site/cards/run-7f4e1e3fe661dfa9.json",
    "results/labviz/site/cards/run-7f6349455e5c54c1.json",
    "results/labviz/site/cards/run-7f69ff75ef0d9659.json",
    "results/labviz/site/cards/run-7f9f33a2008a7b4c.json",
    "results/labviz/site/cards/run-7fa21d373c5ed6f2.json",
    "results/labviz/site/cards/run-7fafd316e1a481d1.json",
    "results/labviz/site/cards/run-7fd37abfb219933d.json",
    "results/labviz/site/cards/run-7fe9d393c27767c1.json",
    "results/labviz/site/cards/run-7ffbd60c396b52d6.json",
    "results/labviz/site/cards/run-8050a59ae9bc3323.json",
    "results/labviz/site/cards/run-807611388586247e.json",
    "results/labviz/site/cards/run-8097edeb6c59d704.json",
    "results/labviz/site/cards/run-811e4a8cd23c602c.json",
    "results/labviz/site/cards/run-81a963186fc34f7e.json",
    "results/labviz/site/cards/run-81bdda8e0353a676.json",
    "results/labviz/site/cards/run-81d23feade439e8b.json",
    "results/labviz/site/cards/run-81d68e47ded41dc1.json",
    "results/labviz/site/cards/run-81fffb392ac50bd7.json",
    "results/labviz/site/cards/run-8212e4592e53f54b.json",
    "results/labviz/site/cards/run-821fc5d86ec44b91.json",
    "results/labviz/site/cards/run-82202c727f616263.json",
    "results/labviz/site/cards/run-822f2dd5e8c69ac8.json",
    "results/labviz/site/cards/run-826940a93daf22a8.json",
    "results/labviz/site/cards/run-8290f471545ac7a6.json",
    "results/labviz/site/cards/run-829bc995ce7f70ec.json",
    "results/labviz/site/cards/run-82b199eca5dd3d62.json",
    "results/labviz/site/cards/run-82b3ab79201a836c.json",
    "results/labviz/site/cards/run-82c9fd9c58e40b79.json",
    "results/labviz/site/cards/run-82e05be8cb1c1ee5.json",
    "results/labviz/site/cards/run-83102d6e34f46818.json",
    "results/labviz/site/cards/run-831b90bb0c34c7f9.json",
    "results/labviz/site/cards/run-8329a6bfea97abc5.json",
    "results/labviz/site/cards/run-832b780fdf4c80ca.json",
    "results/labviz/site/cards/run-8331259c7e578aed.json",
    "results/labviz/site/cards/run-836b58bb720d354b.json",
    "results/labviz/site/cards/run-83a1613b2307240c.json",
    "results/labviz/site/cards/run-83b5402300fd124a.json",
    "results/labviz/site/cards/run-83bf51c5672daad3.json",
    "results/labviz/site/cards/run-83de5f652f0678d2.json",
    "results/labviz/site/cards/run-83fc2ce44e02d6c4.json",
    "results/labviz/site/cards/run-8403bec9bc97c926.json",
    "results/labviz/site/cards/run-850a2065af8974c3.json",
    "results/labviz/site/cards/run-852241e637c94fdc.json",
    "results/labviz/site/cards/run-856c75ca53aff390.json",
    "results/labviz/site/cards/run-8582dbb22180c075.json",
    "results/labviz/site/cards/run-85b1edddcd17675f.json",
    "results/labviz/site/cards/run-85b7e8fb7eccb546.json",
    "results/labviz/site/cards/run-85ef0946f18b6ff9.json",
    "results/labviz/site/cards/run-8606a004e0ac1b93.json",
    "results/labviz/site/cards/run-865e1d7d06b10f41.json",
    "results/labviz/site/cards/run-86655969dd1fbd33.json",
    "results/labviz/site/cards/run-868d847fc4ed3866.json",
    "results/labviz/site/cards/run-86a892fe52e8b36b.json",
    "results/labviz/site/cards/run-86c1afdadaabd3fe.json",
    "results/labviz/site/cards/run-86d07c6f3c9292f7.json",
    "results/labviz/site/cards/run-86fe85157c3f1b54.json",
    "results/labviz/site/cards/run-871532f86ea75b0f.json",
    "results/labviz/site/cards/run-87290cda92992b6e.json",
    "results/labviz/site/cards/run-874be216977d8535.json",
    "results/labviz/site/cards/run-876219f33047c666.json",
    "results/labviz/site/cards/run-87861d0ca17308d7.json",
    "results/labviz/site/cards/run-87876e5d537f8cd2.json",
    "results/labviz/site/cards/run-878f22ed80bf712e.json",
    "results/labviz/site/cards/run-87ac919e812e2017.json",
    "results/labviz/site/cards/run-87ba7d23f4397188.json",
    "results/labviz/site/cards/run-87c4a8c338c754b4.json",
    "results/labviz/site/cards/run-87e209bef940f402.json",
    "results/labviz/site/cards/run-884f4fcccec0efaf.json",
    "results/labviz/site/cards/run-88652d192423f7c5.json",
    "results/labviz/site/cards/run-88c0e82a812b6119.json",
    "results/labviz/site/cards/run-88c909f66b60dce8.json",
    "results/labviz/site/cards/run-88fe8ded94dd57b4.json",
    "results/labviz/site/cards/run-88ff22f4f8aba883.json",
    "results/labviz/site/cards/run-894c2ba57a1f9fb5.json",
    "results/labviz/site/cards/run-896815187c6873b8.json",
    "results/labviz/site/cards/run-89947f9107df7783.json",
    "results/labviz/site/cards/run-8a2805e983a380a6.json",
    "results/labviz/site/cards/run-8a3dfa7ed2bc7dc8.json",
    "results/labviz/site/cards/run-8a4321450d52de1a.json",
    "results/labviz/site/cards/run-8a63e38867404775.json",
    "results/labviz/site/cards/run-8a7e794762beeb0d.json",
    "results/labviz/site/cards/run-8a8cfdf495a81411.json",
    "results/labviz/site/cards/run-8aaabf222e512b17.json",
    "results/labviz/site/cards/run-8ab161776ef800b3.json",
    "results/labviz/site/cards/run-8ab3bedf1439c162.json",
    "results/labviz/site/cards/run-8ac7c6bb44d03432.json",
    "results/labviz/site/cards/run-8ae9b32f301617b8.json",
    "results/labviz/site/cards/run-8af07bb30e748437.json",
    "results/labviz/site/cards/run-8af9c4a63d0d5f11.json",
    "results/labviz/site/cards/run-8b22f253049568d3.json",
    "results/labviz/site/cards/run-8b2e7c1af759036e.json",
    "results/labviz/site/cards/run-8b9914c5ef578545.json",
    "results/labviz/site/cards/run-8bd26104fceabe95.json",
    "results/labviz/site/cards/run-8c0b180b7fb2ed7d.json",
    "results/labviz/site/cards/run-8c1416cfd766c77f.json",
    "results/labviz/site/cards/run-8c72d0c86c090d8f.json",
    "results/labviz/site/cards/run-8c996ddf893648a7.json",
    "results/labviz/site/cards/run-8ca831d970d78563.json",
    "results/labviz/site/cards/run-8d63d6315c30f794.json",
    "results/labviz/site/cards/run-8d943708b568ec9d.json",
    "results/labviz/site/cards/run-8db52dbc13328882.json",
    "results/labviz/site/cards/run-8df5896bef6fa914.json",
    "results/labviz/site/cards/run-8e0880dc306b56d2.json",
    "results/labviz/site/cards/run-8e0be5107f82a53f.json",
    "results/labviz/site/cards/run-8e383f99576b8dda.json",
    "results/labviz/site/cards/run-8e591b932d419bae.json",
    "results/labviz/site/cards/run-8e7690da6f453876.json",
    "results/labviz/site/cards/run-8e7decdf390a71a5.json",
    "results/labviz/site/cards/run-8eb0668b6ae42c62.json",
    "results/labviz/site/cards/run-8eb34df34503b322.json",
    "results/labviz/site/cards/run-8edb2431e6bf7193.json",
    "results/labviz/site/cards/run-8edb73566408cd68.json",
    "results/labviz/site/cards/run-8f160fe5774b8aa8.json",
    "results/labviz/site/cards/run-8f2eaf3a14aef132.json",
    "results/labviz/site/cards/run-8f335b5fa657ab2b.json",
    "results/labviz/site/cards/run-8f4dd1e894104bec.json",
    "results/labviz/site/cards/run-8f79f59e94d8b762.json",
    "results/labviz/site/cards/run-8fe0ed1e279a6a6c.json",
    "results/labviz/site/cards/run-9019d95308bbbc75.json",
    "results/labviz/site/cards/run-907d82de1c71cb5f.json",
    "results/labviz/site/cards/run-90c0bb54b1ec11ea.json",
    "results/labviz/site/cards/run-90eaa7d907d0e63a.json",
    "results/labviz/site/cards/run-91228932e3f13ddb.json",
    "results/labviz/site/cards/run-914b03aefa090b11.json",
    "results/labviz/site/cards/run-914b3ee8beee9481.json",
    "results/labviz/site/cards/run-914fb3e7b5da2c24.json",
    "results/labviz/site/cards/run-916bfeca948dc005.json",
    "results/labviz/site/cards/run-916e99f082041fc8.json",
    "results/labviz/site/cards/run-91768e4006b31f76.json",
    "results/labviz/site/cards/run-9180e6ab75fa4d8c.json",
    "results/labviz/site/cards/run-918f5cc4280e6b9b.json",
    "results/labviz/site/cards/run-91b224ec26a6bdc4.json",
    "results/labviz/site/cards/run-91d8e27974b47c06.json",
    "results/labviz/site/cards/run-921dcd82a991148b.json",
    "results/labviz/site/cards/run-9291aa7132138b0b.json",
    "results/labviz/site/cards/run-92c590ba8c89466c.json",
    "results/labviz/site/cards/run-92fd56ba3dcc9113.json",
    "results/labviz/site/cards/run-934fab911faf5c3a.json",
    "results/labviz/site/cards/run-9367b98f11150cd1.json",
    "results/labviz/site/cards/run-9396991b19e4eb2c.json",
    "results/labviz/site/cards/run-9477a1f8d2475dc0.json",
    "results/labviz/site/cards/run-948f6ed82c6387e5.json",
    "results/labviz/site/cards/run-9490510225009881.json",
    "results/labviz/site/cards/run-9499914e21a24803.json",
    "results/labviz/site/cards/run-94b914b8b44bf4ac.json",
    "results/labviz/site/cards/run-94bf6fe203627833.json",
    "results/labviz/site/cards/run-94d6d6f594c89edb.json",
    "results/labviz/site/cards/run-94f3860361c5f1b2.json",
    "results/labviz/site/cards/run-954ddcf21b18f753.json",
    "results/labviz/site/cards/run-954df6ba8b8cedfa.json",
    "results/labviz/site/cards/run-955c466cd72be419.json",
    "results/labviz/site/cards/run-95832719e6277e7f.json",
    "results/labviz/site/cards/run-9593d118d993c0d2.json",
    "results/labviz/site/cards/run-959845f0ed491f54.json",
    "results/labviz/site/cards/run-95beece3de324e64.json",
    "results/labviz/site/cards/run-95d903d8cffb8b28.json",
    "results/labviz/site/cards/run-9624f605e6bd2bc8.json",
    "results/labviz/site/cards/run-962d6fa9d67a8498.json",
    "results/labviz/site/cards/run-964e5de8799e631a.json",
    "results/labviz/site/cards/run-96712a9bfc01950c.json",
    "results/labviz/site/cards/run-968dc1d9847c03d3.json",
    "results/labviz/site/cards/run-96950e772d09477a.json",
    "results/labviz/site/cards/run-96c9b9da8fedc03c.json",
    "results/labviz/site/cards/run-96dd21a701bb6c66.json",
    "results/labviz/site/cards/run-9732f458ff9a2497.json",
    "results/labviz/site/cards/run-976732312a958d69.json",
    "results/labviz/site/cards/run-97e08dcb6ad207f0.json",
    "results/labviz/site/cards/run-98150bf4532426b2.json",
    "results/labviz/site/cards/run-984f15d5e9523c52.json",
    "results/labviz/site/cards/run-98bd930d90672e2d.json",
    "results/labviz/site/cards/run-992736d912d66794.json",
    "results/labviz/site/cards/run-992d131cc918fe42.json",
    "results/labviz/site/cards/run-99ebcb99a2d5137d.json",
    "results/labviz/site/cards/run-9a3dfe073910dd61.json",
    "results/labviz/site/cards/run-9a46724aaf25f059.json",
    "results/labviz/site/cards/run-9a87ee7b2e87d34e.json",
    "results/labviz/site/cards/run-9ac05aa31538ec5f.json",
    "results/labviz/site/cards/run-9ad87c36bb69826a.json",
    "results/labviz/site/cards/run-9ada6bbc0564574a.json",
    "results/labviz/site/cards/run-9afac0c86d9b3aea.json",
    "results/labviz/site/cards/run-9afd134f4cf6c188.json",
    "results/labviz/site/cards/run-9b52ed489b0e831d.json",
    "results/labviz/site/cards/run-9b67d351edae38c1.json",
    "results/labviz/site/cards/run-9b7915e4f3b535b1.json",
    "results/labviz/site/cards/run-9b8aa116743df1ba.json",
    "results/labviz/site/cards/run-9bc817d50efb27e1.json",
    "results/labviz/site/cards/run-9bcb47df89527cae.json",
    "results/labviz/site/cards/run-9bf16c86745b45e8.json",
    "results/labviz/site/cards/run-9bfc8e833655505c.json",
    "results/labviz/site/cards/run-9c11b7dbbc3d9872.json",
    "results/labviz/site/cards/run-9c316ec54ffdbbf0.json",
    "results/labviz/site/cards/run-9c398d7c3bfc0dd4.json",
    "results/labviz/site/cards/run-9c562d8fc333a27c.json",
    "results/labviz/site/cards/run-9c9ddbdbf24fbfbd.json",
    "results/labviz/site/cards/run-9ca1892b851bbb06.json",
    "results/labviz/site/cards/run-9cfced6a2f7acaf7.json",
    "results/labviz/site/cards/run-9d5ca5eda5f4df8c.json",
    "results/labviz/site/cards/run-9d5d53016ab08ded.json",
    "results/labviz/site/cards/run-9d76c83f401ac98a.json",
    "results/labviz/site/cards/run-9d8871ebc0261595.json",
    "results/labviz/site/cards/run-9d99adcfe3cdc00a.json",
    "results/labviz/site/cards/run-9d9ad5bdb52c885b.json",
    "results/labviz/site/cards/run-9dfa0a5af9dfba24.json",
    "results/labviz/site/cards/run-9e00a02a044b4311.json",
    "results/labviz/site/cards/run-9e2b22cd40071654.json",
    "results/labviz/site/cards/run-9e2ee9c1cdfc9e32.json",
    "results/labviz/site/cards/run-9e6e6c0cad2b118e.json",
    "results/labviz/site/cards/run-9eb3cb79a5a201c5.json",
    "results/labviz/site/cards/run-9f0ad855e3d3eaf1.json",
    "results/labviz/site/cards/run-9f0dbeaf4a621ff4.json",
    "results/labviz/site/cards/run-9f4e4119eb7d5e7e.json",
    "results/labviz/site/cards/run-9f715621a7034e43.json",
    "results/labviz/site/cards/run-9f789513452299dc.json",
    "results/labviz/site/cards/run-9f824eb56e5cc593.json",
    "results/labviz/site/cards/run-9f84aa0a8133407b.json",
    "results/labviz/site/cards/run-9fe8a8af11f46650.json",
    "results/labviz/site/cards/run-9fec407ccbd68100.json",
    "results/labviz/site/cards/run-a01649663da696f4.json",
    "results/labviz/site/cards/run-a01a42002617db97.json",
    "results/labviz/site/cards/run-a024e0f0eff105d8.json",
    "results/labviz/site/cards/run-a025188914ffb23f.json",
    "results/labviz/site/cards/run-a02c25a8d0cdfc94.json",
    "results/labviz/site/cards/run-a03f1f5d0f840ddf.json",
    "results/labviz/site/cards/run-a0739af7c23703c2.json",
    "results/labviz/site/cards/run-a080eead59ec5852.json",
    "results/labviz/site/cards/run-a084c296716b2193.json",
    "results/labviz/site/cards/run-a0853da94bd7c617.json",
    "results/labviz/site/cards/run-a0a38bd199605a6f.json",
    "results/labviz/site/cards/run-a0a6df631eb5ae1a.json",
    "results/labviz/site/cards/run-a0cf8f6645cdd5f7.json",
    "results/labviz/site/cards/run-a0ec42076261d76f.json",
    "results/labviz/site/cards/run-a0fdcb7e5af0fb0f.json",
    "results/labviz/site/cards/run-a15f97b0a1e128b5.json",
    "results/labviz/site/cards/run-a18aa29ef6071847.json",
    "results/labviz/site/cards/run-a19b6941893c5ef2.json",
    "results/labviz/site/cards/run-a1c5750645044979.json",
    "results/labviz/site/cards/run-a1e0573577bc5498.json",
    "results/labviz/site/cards/run-a1e2dfd4cba479c6.json",
    "results/labviz/site/cards/run-a1ee7d25b24c7ea0.json",
    "results/labviz/site/cards/run-a246c2f0cfc3543a.json",
    "results/labviz/site/cards/run-a24e516b0b68768d.json",
    "results/labviz/site/cards/run-a284dac660eab39e.json",
    "results/labviz/site/cards/run-a28aebf87ee8f95c.json",
    "results/labviz/site/cards/run-a2a0e7b78a9fccfd.json",
    "results/labviz/site/cards/run-a2d58815b2b646d8.json",
    "results/labviz/site/cards/run-a2da614a4a506b05.json",
    "results/labviz/site/cards/run-a2dc63be6f1bcd27.json",
    "results/labviz/site/cards/run-a2ee9b8ef6028b34.json",
    "results/labviz/site/cards/run-a307e3f2571b5219.json",
    "results/labviz/site/cards/run-a33534098882e4da.json",
    "results/labviz/site/cards/run-a34d89270b07acc5.json",
    "results/labviz/site/cards/run-a38fd82a450ac972.json",
    "results/labviz/site/cards/run-a3b3d69efee1394a.json",
    "results/labviz/site/cards/run-a3dd1c6b22bbc8ba.json",
    "results/labviz/site/cards/run-a3fbdf5c877930fe.json",
    "results/labviz/site/cards/run-a42b97beebd12a7c.json",
    "results/labviz/site/cards/run-a4b5812588dbc7bb.json",
    "results/labviz/site/cards/run-a4c0c6b1d2d32565.json",
    "results/labviz/site/cards/run-a4d2bb40648ec1ed.json",
    "results/labviz/site/cards/run-a4dabd9fe5348493.json",
    "results/labviz/site/cards/run-a546238ac8ba609f.json",
    "results/labviz/site/cards/run-a5609d1cc227169f.json",
    "results/labviz/site/cards/run-a56bc79f6cd61fc1.json",
    "results/labviz/site/cards/run-a572e4aaa27d9194.json",
    "results/labviz/site/cards/run-a574ad833abfb561.json",
    "results/labviz/site/cards/run-a577903ccf14976e.json",
    "results/labviz/site/cards/run-a58c0850a1e8b357.json",
    "results/labviz/site/cards/run-a598746f66c6d552.json",
    "results/labviz/site/cards/run-a5ab02d5bf3e2753.json",
    "results/labviz/site/cards/run-a5c672bd52de232c.json",
    "results/labviz/site/cards/run-a5d28e0e075b4088.json",
    "results/labviz/site/cards/run-a5d2df16f461dc66.json",
    "results/labviz/site/cards/run-a60c9ce8232366c3.json",
    "results/labviz/site/cards/run-a681081169e03399.json",
    "results/labviz/site/cards/run-a6abaeffbe2b41d4.json",
    "results/labviz/site/cards/run-a6b5a0f87f754f63.json",
    "results/labviz/site/cards/run-a6f48d39b42c4738.json",
    "results/labviz/site/cards/run-a70773aded206af4.json",
    "results/labviz/site/cards/run-a7188a2841da4d45.json",
    "results/labviz/site/cards/run-a76ffe60cc4628b4.json",
    "results/labviz/site/cards/run-a778af018f6d9d19.json",
    "results/labviz/site/cards/run-a7910688512c30c3.json",
    "results/labviz/site/cards/run-a79f3256a94e4d95.json",
    "results/labviz/site/cards/run-a8211f00b54395da.json",
    "results/labviz/site/cards/run-a849c304e44a0a53.json",
    "results/labviz/site/cards/run-a853ed71a95c5c86.json",
    "results/labviz/site/cards/run-a8890c6f1615cb69.json",
    "results/labviz/site/cards/run-a88fcd0c357a5882.json",
    "results/labviz/site/cards/run-a8b101b91a30e5ac.json",
    "results/labviz/site/cards/run-a8d1e101fce26b4c.json",
    "results/labviz/site/cards/run-a9135da8c30a79d1.json",
    "results/labviz/site/cards/run-a917780c6fd5b666.json",
    "results/labviz/site/cards/run-a91e19317b2a0550.json",
    "results/labviz/site/cards/run-a9478b9d8a526217.json",
    "results/labviz/site/cards/run-a9750797bd62e436.json",
    "results/labviz/site/cards/run-a9afa55140594fcf.json",
    "results/labviz/site/cards/run-a9d467d440c7c561.json",
    "results/labviz/site/cards/run-a9da9b408945ee50.json",
    "results/labviz/site/cards/run-aa4699347f9a4952.json",
    "results/labviz/site/cards/run-aa7bc35701d13255.json",
    "results/labviz/site/cards/run-aa855ea9ca3d343d.json",
    "results/labviz/site/cards/run-aad26b44400a6333.json",
    "results/labviz/site/cards/run-ab35f93c1520854d.json",
    "results/labviz/site/cards/run-ab6eb7afb8b65070.json",
    "results/labviz/site/cards/run-abd7cfe503c64a94.json",
    "results/labviz/site/cards/run-abeb1652d93b422c.json",
    "results/labviz/site/cards/run-ac0ffe3803165e6d.json",
    "results/labviz/site/cards/run-ac7736caa0528e9c.json",
    "results/labviz/site/cards/run-aca72696ed16875d.json",
    "results/labviz/site/cards/run-ad050a887891c7d1.json",
    "results/labviz/site/cards/run-ae04f4a96cf40654.json",
    "results/labviz/site/cards/run-ae178e3090e66454.json",
    "results/labviz/site/cards/run-ae239e3aa7529c09.json",
    "results/labviz/site/cards/run-ae528980708bd79f.json",
    "results/labviz/site/cards/run-ae84d66d6efce971.json",
    "results/labviz/site/cards/run-aeb152d5b75144d2.json",
    "results/labviz/site/cards/run-aeea15adf17d4dfd.json",
    "results/labviz/site/cards/run-aeef7a4e937b5ffe.json",
    "results/labviz/site/cards/run-aef77b552f3411fe.json",
    "results/labviz/site/cards/run-aefa271565916601.json",
    "results/labviz/site/cards/run-af230f563abc3f96.json",
    "results/labviz/site/cards/run-af3a79e9a32e33b1.json",
    "results/labviz/site/cards/run-af90e5a505dfc16c.json",
    "results/labviz/site/cards/run-afde164936ff4ce6.json",
    "results/labviz/site/cards/run-b029aba91ef31e4b.json",
    "results/labviz/site/cards/run-b0509f72062a620f.json",
    "results/labviz/site/cards/run-b0e797273a22d8f1.json",
    "results/labviz/site/cards/run-b0f32eab8f9d7512.json",
    "results/labviz/site/cards/run-b157fe30f81ed0b3.json",
    "results/labviz/site/cards/run-b16bbbd3065e01fc.json",
    "results/labviz/site/cards/run-b1843b0afdc5ac83.json",
    "results/labviz/site/cards/run-b1b565706fbb2dbe.json",
    "results/labviz/site/cards/run-b1f39a3c84509ca0.json",
    "results/labviz/site/cards/run-b215944edb3789d2.json",
    "results/labviz/site/cards/run-b236ffce6da14932.json",
    "results/labviz/site/cards/run-b2444d475a18773c.json",
    "results/labviz/site/cards/run-b276e649abc5106d.json",
    "results/labviz/site/cards/run-b291e4942b211aee.json",
    "results/labviz/site/cards/run-b2dd389730cec2f0.json",
    "results/labviz/site/cards/run-b2e8a6bc678183a5.json",
    "results/labviz/site/cards/run-b32174a8ef238991.json",
    "results/labviz/site/cards/run-b331931306979d74.json",
    "results/labviz/site/cards/run-b35c599f553de2ce.json",
    "results/labviz/site/cards/run-b3a37ef4a3732a9d.json",
    "results/labviz/site/cards/run-b3c10ba8243aaa88.json",
    "results/labviz/site/cards/run-b3d786945c1a4aa4.json",
    "results/labviz/site/cards/run-b3ea8f46f744faeb.json",
    "results/labviz/site/cards/run-b3f467813b15e71b.json",
    "results/labviz/site/cards/run-b453db952f17dde4.json",
    "results/labviz/site/cards/run-b47018a0801c5231.json",
    "results/labviz/site/cards/run-b4ed0204db20204b.json",
    "results/labviz/site/cards/run-b4f2e6aeea681919.json",
    "results/labviz/site/cards/run-b5405f16233ff6d5.json",
    "results/labviz/site/cards/run-b5740b46330c3103.json",
    "results/labviz/site/cards/run-b5ac2728921c8e04.json",
    "results/labviz/site/cards/run-b5b869d1c736b684.json",
    "results/labviz/site/cards/run-b5e9b418d08f896f.json",
    "results/labviz/site/cards/run-b60e5d0a78847be3.json",
    "results/labviz/site/cards/run-b63a6d1ba3da97ba.json",
    "results/labviz/site/cards/run-b659f20a02392f7b.json",
    "results/labviz/site/cards/run-b66f76bd8fab216c.json",
    "results/labviz/site/cards/run-b6821df5ec55fd0e.json",
    "results/labviz/site/cards/run-b6a6c18744a4fddb.json",
    "results/labviz/site/cards/run-b6b3884f5ddfba26.json",
    "results/labviz/site/cards/run-b6ff10e6809fd053.json",
    "results/labviz/site/cards/run-b71c696d7ec1c30a.json",
    "results/labviz/site/cards/run-b74c66a455781638.json",
    "results/labviz/site/cards/run-b783baacb163199b.json",
    "results/labviz/site/cards/run-b7bfc47f47897317.json",
    "results/labviz/site/cards/run-b7c8abd09960b5bc.json",
    "results/labviz/site/cards/run-b80c53652dbaf1ea.json",
    "results/labviz/site/cards/run-b83c7ad11203ea3c.json",
    "results/labviz/site/cards/run-b84fec8b9b96737a.json",
    "results/labviz/site/cards/run-b8ea09113fe018f3.json",
    "results/labviz/site/cards/run-b92b64569f25e527.json",
    "results/labviz/site/cards/run-b956976e215e90bb.json",
    "results/labviz/site/cards/run-b98e3fca47c32e04.json",
    "results/labviz/site/cards/run-b9b15d5a6bc40be1.json",
    "results/labviz/site/cards/run-b9bdd55162c352af.json",
    "results/labviz/site/cards/run-b9f5193f7f5b0144.json",
    "results/labviz/site/cards/run-b9f9582dc94ece34.json",
    "results/labviz/site/cards/run-ba3644665a5aca4c.json",
    "results/labviz/site/cards/run-ba9c5f59bf868727.json",
    "results/labviz/site/cards/run-bac9123e372c5f76.json",
    "results/labviz/site/cards/run-bb59e0356d13bb60.json",
    "results/labviz/site/cards/run-bb644426025d4a91.json",
    "results/labviz/site/cards/run-bb746e131ca0ba8c.json",
    "results/labviz/site/cards/run-bba0cb3de12d266c.json",
    "results/labviz/site/cards/run-bbb9d769887d28f8.json",
    "results/labviz/site/cards/run-bbdd2fcf5e4d6cf7.json",
    "results/labviz/site/cards/run-bbec67574f14542f.json",
    "results/labviz/site/cards/run-bc00285048f79984.json",
    "results/labviz/site/cards/run-bc07ef16ad3d4313.json",
    "results/labviz/site/cards/run-bc682c745b551ab6.json",
    "results/labviz/site/cards/run-bc776817829f3854.json",
    "results/labviz/site/cards/run-bc79aefaee45050c.json",
    "results/labviz/site/cards/run-bcbf0de84c56c43a.json",
    "results/labviz/site/cards/run-bcc8c86a05d48571.json",
    "results/labviz/site/cards/run-bcd9b42e0c384189.json",
    "results/labviz/site/cards/run-bd2792f9bb94a6fa.json",
    "results/labviz/site/cards/run-bd5769c1ecf7d61a.json",
    "results/labviz/site/cards/run-bd68b0dcc76facf6.json",
    "results/labviz/site/cards/run-bd6ed90a1081bca7.json",
    "results/labviz/site/cards/run-bd7e8d040cbbdfb4.json",
    "results/labviz/site/cards/run-bd8f2a9fa9c22541.json",
    "results/labviz/site/cards/run-bdb40a04a851dddd.json",
    "results/labviz/site/cards/run-bdcc25f4830d331e.json",
    "results/labviz/site/cards/run-be199cd56af363b1.json",
    "results/labviz/site/cards/run-be38817096ececdf.json",
    "results/labviz/site/cards/run-be676f852b02d6d3.json",
    "results/labviz/site/cards/run-be93a209e2f1fadc.json",
    "results/labviz/site/cards/run-be9e8bbb8254833c.json",
    "results/labviz/site/cards/run-bea7c96d7c4948c4.json",
    "results/labviz/site/cards/run-bf896aa06ce5af7c.json",
    "results/labviz/site/cards/run-bfae55dd75b3c0d8.json",
    "results/labviz/site/cards/run-c007ad1ce2954127.json",
    "results/labviz/site/cards/run-c03cba3a54262200.json",
    "results/labviz/site/cards/run-c068d7b70920edf1.json",
    "results/labviz/site/cards/run-c069f85453b0897e.json",
    "results/labviz/site/cards/run-c0b104ae5f7c0152.json",
    "results/labviz/site/cards/run-c0c567423af19bba.json",
    "results/labviz/site/cards/run-c0e48344dc1c01dc.json",
    "results/labviz/site/cards/run-c0fee7137a05fbcd.json",
    "results/labviz/site/cards/run-c107ccf47514283f.json",
    "results/labviz/site/cards/run-c10e82967c0cb532.json",
    "results/labviz/site/cards/run-c12d6088fbd6ab45.json",
    "results/labviz/site/cards/run-c147b78cb8f6d20d.json",
    "results/labviz/site/cards/run-c182bae2502daa50.json",
    "results/labviz/site/cards/run-c1885a1074dd038b.json",
    "results/labviz/site/cards/run-c1ff0ae6cc13cdb9.json",
    "results/labviz/site/cards/run-c2173bedfe7c69d2.json",
    "results/labviz/site/cards/run-c2518a3abac0276a.json",
    "results/labviz/site/cards/run-c26a23e7395e56cb.json",
    "results/labviz/site/cards/run-c2716231bfa9b00b.json",
    "results/labviz/site/cards/run-c281a62b9e1ab2e9.json",
    "results/labviz/site/cards/run-c3329c98599396af.json",
    "results/labviz/site/cards/run-c392b39869980c06.json",
    "results/labviz/site/cards/run-c39b9834df219bad.json",
    "results/labviz/site/cards/run-c3a3df0dcffbd8b0.json",
    "results/labviz/site/cards/run-c3d86ff90ebb0fd6.json",
    "results/labviz/site/cards/run-c3ee45ab4966d921.json",
    "results/labviz/site/cards/run-c4088f932a2ded0e.json",
    "results/labviz/site/cards/run-c420aaf8af364873.json",
    "results/labviz/site/cards/run-c42dca5e7e9ea02a.json",
    "results/labviz/site/cards/run-c4349ee7defd4519.json",
    "results/labviz/site/cards/run-c4671d3adb16b185.json",
    "results/labviz/site/cards/run-c48522ff5b244504.json",
    "results/labviz/site/cards/run-c499c6c1924ce82e.json",
    "results/labviz/site/cards/run-c4ae7d62c6446e14.json",
    "results/labviz/site/cards/run-c4e2f90cc8d6f758.json",
    "results/labviz/site/cards/run-c5047f8f2cf54533.json",
    "results/labviz/site/cards/run-c53f69fb0ee2a0a1.json",
    "results/labviz/site/cards/run-c5511a219ee996f1.json",
    "results/labviz/site/cards/run-c5677a5dea0c28df.json",
    "results/labviz/site/cards/run-c5ad87e1bb5ebeb9.json",
    "results/labviz/site/cards/run-c5ef82892cb20133.json",
    "results/labviz/site/cards/run-c63ebca106b5413f.json",
    "results/labviz/site/cards/run-c65b999861e9c8d6.json",
    "results/labviz/site/cards/run-c65d63a6b87d994e.json",
    "results/labviz/site/cards/run-c6d46df3a039b700.json",
    "results/labviz/site/cards/run-c6d5806d85f8c166.json",
    "results/labviz/site/cards/run-c7130e80b123b312.json",
    "results/labviz/site/cards/run-c72254430600a4d5.json",
    "results/labviz/site/cards/run-c727be97ef75a933.json",
    "results/labviz/site/cards/run-c75b05661b5aecd3.json",
    "results/labviz/site/cards/run-c765d8ca0970a2fd.json",
    "results/labviz/site/cards/run-c7721750bff378b1.json",
    "results/labviz/site/cards/run-c7755b996ca9b5b3.json",
    "results/labviz/site/cards/run-c78b6d9b8ff855d1.json",
    "results/labviz/site/cards/run-c7d8d89370c3a9de.json",
    "results/labviz/site/cards/run-c7ed1b002f0cbeeb.json",
    "results/labviz/site/cards/run-c7f0873fc345813e.json",
    "results/labviz/site/cards/run-c81e8bb43db91c37.json",
    "results/labviz/site/cards/run-c841d1407c59048a.json",
    "results/labviz/site/cards/run-c8acba3cf772390c.json",
    "results/labviz/site/cards/run-c8f8b7a08c05e245.json",
    "results/labviz/site/cards/run-c8f95f26653f0d33.json",
    "results/labviz/site/cards/run-c8fea4c436406c1f.json",
    "results/labviz/site/cards/run-c8ff351766c4d78f.json",
    "results/labviz/site/cards/run-c90da38fbdc33359.json",
    "results/labviz/site/cards/run-c9466a2f82064d31.json",
    "results/labviz/site/cards/run-c94a48390467e2f6.json",
    "results/labviz/site/cards/run-c95409f70adb42aa.json",
    "results/labviz/site/cards/run-c981c79c1941155e.json",
    "results/labviz/site/cards/run-c996425d0c61979b.json",
    "results/labviz/site/cards/run-c9a693e58c6099b1.json",
    "results/labviz/site/cards/run-c9ad9f29520ed273.json",
    "results/labviz/site/cards/run-c9cd53f8272b42a1.json",
    "results/labviz/site/cards/run-c9d23e65848ce19f.json",
    "results/labviz/site/cards/run-c9dddc3cf8cf4443.json",
    "results/labviz/site/cards/run-c9f7ce95073f25c4.json",
    "results/labviz/site/cards/run-ca200a670eadbaa0.json",
    "results/labviz/site/cards/run-ca925a77775a8c96.json",
    "results/labviz/site/cards/run-caae4080cbe957e8.json",
    "results/labviz/site/cards/run-cae6f6bddbd8c959.json",
    "results/labviz/site/cards/run-cb0a0905d12e71d6.json",
    "results/labviz/site/cards/run-cb27938e86b426dc.json",
    "results/labviz/site/cards/run-cb364f59c4c6f66d.json",
    "results/labviz/site/cards/run-cb45e7201a38c0ca.json",
    "results/labviz/site/cards/run-cbd732017d8c5604.json",
    "results/labviz/site/cards/run-cc3c8244c944e9a8.json",
    "results/labviz/site/cards/run-ccd2d430a873062a.json",
    "results/labviz/site/cards/run-ccda68ccba7f4705.json",
    "results/labviz/site/cards/run-ccde5a7e3a4ab7b2.json",
    "results/labviz/site/cards/run-cd2336e316ec9066.json",
    "results/labviz/site/cards/run-cd292cc67d4f3b9a.json",
    "results/labviz/site/cards/run-cd95cc60da268def.json",
    "results/labviz/site/cards/run-cd984cfc8ff4d41c.json",
    "results/labviz/site/cards/run-cded79c8ffe40e3d.json",
    "results/labviz/site/cards/run-ce21e1a0f8be0413.json",
    "results/labviz/site/cards/run-ce2b747f8e2768c8.json",
    "results/labviz/site/cards/run-ce4abfce97a2813d.json",
    "results/labviz/site/cards/run-ce705781f8649a23.json",
    "results/labviz/site/cards/run-ce93edf09326c9d9.json",
    "results/labviz/site/cards/run-cebb0744f0d5bcf5.json",
    "results/labviz/site/cards/run-cec8c16e53bfc95c.json",
    "results/labviz/site/cards/run-cf11ca773bd40b8b.json",
    "results/labviz/site/cards/run-cf26ebfde2a9d401.json",
    "results/labviz/site/cards/run-cf6ebf674d29c016.json",
    "results/labviz/site/cards/run-cf8e8725f656f677.json",
    "results/labviz/site/cards/run-d01024d2305af898.json",
    "results/labviz/site/cards/run-d030404174ede815.json",
    "results/labviz/site/cards/run-d034b58d625ee6e5.json",
    "results/labviz/site/cards/run-d046379028a36e42.json",
    "results/labviz/site/cards/run-d04c87911e0ee39e.json",
    "results/labviz/site/cards/run-d0572279278e4008.json",
    "results/labviz/site/cards/run-d0a7054537c5132f.json",
    "results/labviz/site/cards/run-d0b7b420d2c44885.json",
    "results/labviz/site/cards/run-d0b7bb938dd850a7.json",
    "results/labviz/site/cards/run-d0cc333916d7ce21.json",
    "results/labviz/site/cards/run-d0e4b613e2b71696.json",
    "results/labviz/site/cards/run-d111b73f540d3ec7.json",
    "results/labviz/site/cards/run-d115650165134cf5.json",
    "results/labviz/site/cards/run-d11b619f10313ad4.json",
    "results/labviz/site/cards/run-d12bfeea34ca3962.json",
    "results/labviz/site/cards/run-d16802f4cda4385f.json",
    "results/labviz/site/cards/run-d1862f92fa0e241d.json",
    "results/labviz/site/cards/run-d1a0b58778e3bd8c.json",
    "results/labviz/site/cards/run-d1abfafd812c4358.json",
    "results/labviz/site/cards/run-d1b106d6a1bcf019.json",
    "results/labviz/site/cards/run-d1cbf554dabab36f.json",
    "results/labviz/site/cards/run-d1e1ca13d3a1fb4a.json",
    "results/labviz/site/cards/run-d23d507f1b81ab96.json",
    "results/labviz/site/cards/run-d28ff313af40fff4.json",
    "results/labviz/site/cards/run-d2962daa818e870c.json",
    "results/labviz/site/cards/run-d29efe949ef4ae63.json",
    "results/labviz/site/cards/run-d2b927be3cbb0ab8.json",
    "results/labviz/site/cards/run-d3244507b3c1abd9.json",
    "results/labviz/site/cards/run-d35d3a20fe0650e2.json",
    "results/labviz/site/cards/run-d38ce5750c44379e.json",
    "results/labviz/site/cards/run-d3caec2f755fe5bb.json",
    "results/labviz/site/cards/run-d3fe33e3df5ba06a.json",
    "results/labviz/site/cards/run-d42d40c8e0c9fab0.json",
    "results/labviz/site/cards/run-d4bafd1e2f563ff8.json",
    "results/labviz/site/cards/run-d4d5ba21c24eb670.json",
    "results/labviz/site/cards/run-d4d73416cabd0b8f.json",
    "results/labviz/site/cards/run-d50884dde8f043ad.json",
    "results/labviz/site/cards/run-d5267f6cedbf7314.json",
    "results/labviz/site/cards/run-d5539bce4e28a5a2.json",
    "results/labviz/site/cards/run-d5fd42235c9dd6a9.json",
    "results/labviz/site/cards/run-d60cbba125b08874.json",
    "results/labviz/site/cards/run-d6c4b11d5bf19606.json",
    "results/labviz/site/cards/run-d6df84a5b7e0a824.json",
    "results/labviz/site/cards/run-d73d65136af64ba6.json",
    "results/labviz/site/cards/run-d7565b052fd4ef98.json",
    "results/labviz/site/cards/run-d75e4d1f46985d6a.json",
    "results/labviz/site/cards/run-d76427cfd10b255b.json",
    "results/labviz/site/cards/run-d797fe1ed03533e1.json",
    "results/labviz/site/cards/run-d7c7919872f629c9.json",
    "results/labviz/site/cards/run-d7f750d20231000f.json",
    "results/labviz/site/cards/run-d7ff518c41b30ec2.json",
    "results/labviz/site/cards/run-d82ca184cb546756.json",
    "results/labviz/site/cards/run-d884d22ef0d7dcd4.json",
    "results/labviz/site/cards/run-d888eb9bd1a76497.json",
    "results/labviz/site/cards/run-d8abd7e429913ea8.json",
    "results/labviz/site/cards/run-d8d03517f361feab.json",
    "results/labviz/site/cards/run-d91ea1dcf0603c3f.json",
    "results/labviz/site/cards/run-d93ec9f75e9b76b8.json",
    "results/labviz/site/cards/run-d9bd42d5b3231efb.json",
    "results/labviz/site/cards/run-d9ef0f146c2e63f3.json",
    "results/labviz/site/cards/run-da02571b0b7a5590.json",
    "results/labviz/site/cards/run-da05cb56168a3095.json",
    "results/labviz/site/cards/run-da5732aafb03dce3.json",
    "results/labviz/site/cards/run-da674a1f3c97e444.json",
    "results/labviz/site/cards/run-da85708cc1644d5a.json",
    "results/labviz/site/cards/run-da9128a7be140025.json",
    "results/labviz/site/cards/run-dacf40816847fdc8.json",
    "results/labviz/site/cards/run-dad8b5e3d03d68a4.json",
    "results/labviz/site/cards/run-dadce4feb882eab3.json",
    "results/labviz/site/cards/run-daf645b8c142a8a4.json",
    "results/labviz/site/cards/run-dc02943effe945b9.json",
    "results/labviz/site/cards/run-dc5fb77f8595b9ca.json",
    "results/labviz/site/cards/run-dc663fabd3a6e8f6.json",
    "results/labviz/site/cards/run-dc8f1d8a25eaea1e.json",
    "results/labviz/site/cards/run-dcff71a23d8eeb0c.json",
    "results/labviz/site/cards/run-dd09281bc461f9ef.json",
    "results/labviz/site/cards/run-dd215e3383ea97d7.json",
    "results/labviz/site/cards/run-dd241b6b8cccc8bb.json",
    "results/labviz/site/cards/run-dd3df466ecf42461.json",
    "results/labviz/site/cards/run-dd4eb166bd89ea05.json",
    "results/labviz/site/cards/run-dd55d3bdb038d43f.json",
    "results/labviz/site/cards/run-dd74533ed02986f5.json",
    "results/labviz/site/cards/run-ddb04d3a6c467a79.json",
    "results/labviz/site/cards/run-ddd9568455a50b23.json",
    "results/labviz/site/cards/run-ddebeb226f656b17.json",
    "results/labviz/site/cards/run-de22c0945df7dd01.json",
    "results/labviz/site/cards/run-de2e1971b78da406.json",
    "results/labviz/site/cards/run-de38db013dcec26f.json",
    "results/labviz/site/cards/run-de6f318d9db36aa2.json",
    "results/labviz/site/cards/run-de7e3cf8f44ca951.json",
    "results/labviz/site/cards/run-dfbaafb1781ece60.json",
    "results/labviz/site/cards/run-dfcfaff10e8a3f4f.json",
    "results/labviz/site/cards/run-e01ecbb5cdc7a73a.json",
    "results/labviz/site/cards/run-e07f346e787ff92f.json",
    "results/labviz/site/cards/run-e0e2c3a20b743d78.json",
    "results/labviz/site/cards/run-e0e33218b29654be.json",
    "results/labviz/site/cards/run-e101629a9bb5396b.json",
    "results/labviz/site/cards/run-e13f277a799ad5b0.json",
    "results/labviz/site/cards/run-e16e9f9e55fec2c4.json",
    "results/labviz/site/cards/run-e18dd25e152daf29.json",
    "results/labviz/site/cards/run-e1ac0a4bbec4ddc5.json",
    "results/labviz/site/cards/run-e1b05b9dc1c7a859.json",
    "results/labviz/site/cards/run-e1ed9ef67b69480d.json",
    "results/labviz/site/cards/run-e1ee39f7330c513c.json",
    "results/labviz/site/cards/run-e211af5be8ba895e.json",
    "results/labviz/site/cards/run-e2187e288b870564.json",
    "results/labviz/site/cards/run-e2321695e9be7d59.json",
    "results/labviz/site/cards/run-e2976b8f120f454d.json",
    "results/labviz/site/cards/run-e2983b3895c00601.json",
    "results/labviz/site/cards/run-e2beb873ce180d89.json",
    "results/labviz/site/cards/run-e2fd4d22a74b57b6.json",
    "results/labviz/site/cards/run-e34409c9194fa26a.json",
    "results/labviz/site/cards/run-e37a2e99202ecf48.json",
    "results/labviz/site/cards/run-e3a38ec89f169bd5.json",
    "results/labviz/site/cards/run-e3e1d3af925d7423.json",
    "results/labviz/site/cards/run-e3f39e20ea6425b8.json",
    "results/labviz/site/cards/run-e3fa8f0fd004c98c.json",
    "results/labviz/site/cards/run-e42cbfab3889dc5a.json",
    "results/labviz/site/cards/run-e44db9244efb574f.json",
    "results/labviz/site/cards/run-e4a76a5e7d902a35.json",
    "results/labviz/site/cards/run-e4b783c0422318c4.json",
    "results/labviz/site/cards/run-e4b975523fc5aacb.json",
    "results/labviz/site/cards/run-e50f4ca4f8716d88.json",
    "results/labviz/site/cards/run-e54bdbd5c6db76bd.json",
    "results/labviz/site/cards/run-e5686e2f8b39c8ef.json",
    "results/labviz/site/cards/run-e6427a185594584e.json",
    "results/labviz/site/cards/run-e671564ac56f93e0.json",
    "results/labviz/site/cards/run-e6ecac0d47609afe.json",
    "results/labviz/site/cards/run-e70fe7f31424c857.json",
    "results/labviz/site/cards/run-e75aab0ba6863fd1.json",
    "results/labviz/site/cards/run-e78409da73a305a2.json",
    "results/labviz/site/cards/run-e78efecb26ef8489.json",
    "results/labviz/site/cards/run-e798a3b8f9961e9b.json",
    "results/labviz/site/cards/run-e7991e6ce5646928.json",
    "results/labviz/site/cards/run-e79b8989aa34c12c.json",
    "results/labviz/site/cards/run-e7b6dbf947c8e8f5.json",
    "results/labviz/site/cards/run-e7cc083cf7cbfd01.json",
    "results/labviz/site/cards/run-e8b7bd98e3804986.json",
    "results/labviz/site/cards/run-e8c0fce330edab61.json",
    "results/labviz/site/cards/run-e90214f1350ddbaf.json",
    "results/labviz/site/cards/run-e98136cac909136f.json",
    "results/labviz/site/cards/run-e994d588456e3358.json",
    "results/labviz/site/cards/run-e9a52f5b95a949d1.json",
    "results/labviz/site/cards/run-e9b2f35837a285db.json",
    "results/labviz/site/cards/run-e9b6328797fb8afb.json",
    "results/labviz/site/cards/run-e9c2fa440d948fcb.json",
    "results/labviz/site/cards/run-e9f73a05e937a813.json",
    "results/labviz/site/cards/run-ea004410dbf59093.json",
    "results/labviz/site/cards/run-ea15a4fcd16e147b.json",
    "results/labviz/site/cards/run-ea55eb4749cfb7dd.json",
    "results/labviz/site/cards/run-ea88a4574dc5808e.json",
    "results/labviz/site/cards/run-ead6e4308083fc36.json",
    "results/labviz/site/cards/run-eb3163a4ddc1f93a.json",
    "results/labviz/site/cards/run-eb72b11e3a0fd68f.json",
    "results/labviz/site/cards/run-eb8000730f3e92c2.json",
    "results/labviz/site/cards/run-ebd94ca49c77442a.json",
    "results/labviz/site/cards/run-ebe0b1dd974385be.json",
    "results/labviz/site/cards/run-ebe81da20e763124.json",
    "results/labviz/site/cards/run-ebf3c1cc007602c9.json",
    "results/labviz/site/cards/run-ec0f366754fff788.json",
    "results/labviz/site/cards/run-ec5ec8dae9c33460.json",
    "results/labviz/site/cards/run-ec834012bc1d5f42.json",
    "results/labviz/site/cards/run-ec9d7034b50c5780.json",
    "results/labviz/site/cards/run-eca097a64442325d.json",
    "results/labviz/site/cards/run-ecd823e5ba0b973c.json",
    "results/labviz/site/cards/run-ed9131d13afe3b95.json",
    "results/labviz/site/cards/run-eda07ad18ee5643d.json",
    "results/labviz/site/cards/run-edeb2926e3f82be1.json",
    "results/labviz/site/cards/run-edfe9319a495e148.json",
    "results/labviz/site/cards/run-ee50afa7d430845c.json",
    "results/labviz/site/cards/run-ee52a00f7b5fb65d.json",
    "results/labviz/site/cards/run-ee815af03ab0338c.json",
    "results/labviz/site/cards/run-eea45dc12a911f0a.json",
    "results/labviz/site/cards/run-eeeeb679e257ff7c.json",
    "results/labviz/site/cards/run-ef06d66db8a338bb.json",
    "results/labviz/site/cards/run-ef115f1402fa7ef0.json",
    "results/labviz/site/cards/run-ef70598b9ebbc232.json",
    "results/labviz/site/cards/run-efbd4f3c900ccd11.json",
    "results/labviz/site/cards/run-efbd7c30ce2a5b2a.json",
    "results/labviz/site/cards/run-f00aed51ddff3940.json",
    "results/labviz/site/cards/run-f00fdb5beaa5227a.json",
    "results/labviz/site/cards/run-f022c75ec169a996.json",
    "results/labviz/site/cards/run-f03029fdfb5c3d4d.json",
    "results/labviz/site/cards/run-f04eb210a68aad09.json",
    "results/labviz/site/cards/run-f088b8f0c72180a6.json",
    "results/labviz/site/cards/run-f09aefb5f366204d.json",
    "results/labviz/site/cards/run-f0b7fa12456f0d62.json",
    "results/labviz/site/cards/run-f0d4af57920368ac.json",
    "results/labviz/site/cards/run-f10ae2bd12476af0.json",
    "results/labviz/site/cards/run-f1a5a015b8274532.json",
    "results/labviz/site/cards/run-f1ae3e7e89653a8f.json",
    "results/labviz/site/cards/run-f1f1087a4f249ad2.json",
    "results/labviz/site/cards/run-f202344e0e8e96a7.json",
    "results/labviz/site/cards/run-f20d66dd86723254.json",
    "results/labviz/site/cards/run-f2545c68e2461fa3.json",
    "results/labviz/site/cards/run-f2577d5bb57d8c79.json",
    "results/labviz/site/cards/run-f27f5dc3cd0a2e08.json",
    "results/labviz/site/cards/run-f28a6ce7c6775d1b.json",
    "results/labviz/site/cards/run-f2b9757df7c8e0ac.json",
    "results/labviz/site/cards/run-f2f193c49ce6038b.json",
    "results/labviz/site/cards/run-f32d6f9c026f5f87.json",
    "results/labviz/site/cards/run-f38e8b4f27920d51.json",
    "results/labviz/site/cards/run-f3d6e63f1806c2b7.json",
    "results/labviz/site/cards/run-f47a2e659cd48db1.json",
    "results/labviz/site/cards/run-f4a28d7b690c5390.json",
    "results/labviz/site/cards/run-f4f68fff31d5d250.json",
    "results/labviz/site/cards/run-f4fadf2d772b4364.json",
    "results/labviz/site/cards/run-f525898edb5240af.json",
    "results/labviz/site/cards/run-f54a7cf41e5d41a7.json",
    "results/labviz/site/cards/run-f55aab1ea0b27769.json",
    "results/labviz/site/cards/run-f568a43a45275c5b.json",
    "results/labviz/site/cards/run-f59272bf5637b4ff.json",
    "results/labviz/site/cards/run-f5f1669f7c98b192.json",
    "results/labviz/site/cards/run-f65cef7d0353e018.json",
    "results/labviz/site/cards/run-f65f6597d1bf5d2e.json",
    "results/labviz/site/cards/run-f660d9e284c98cc4.json",
    "results/labviz/site/cards/run-f67a0763246a54dd.json",
    "results/labviz/site/cards/run-f6948d5116e11c3d.json",
    "results/labviz/site/cards/run-f6b453e7d0718a1a.json",
    "results/labviz/site/cards/run-f6cd17c20c29714c.json",
    "results/labviz/site/cards/run-f70f91a562ed9124.json",
    "results/labviz/site/cards/run-f7aa4bb86ebd1486.json",
    "results/labviz/site/cards/run-f7c555e81e782dbd.json",
    "results/labviz/site/cards/run-f82f542ccc4132b7.json",
    "results/labviz/site/cards/run-f83e7a9f2232e4dd.json",
    "results/labviz/site/cards/run-f87d9ded2de530f5.json",
    "results/labviz/site/cards/run-f87efa71907dc8eb.json",
    "results/labviz/site/cards/run-f88d71f35381daf9.json",
    "results/labviz/site/cards/run-f8c40ac4ced25120.json",
    "results/labviz/site/cards/run-f92504eb2678b34a.json",
    "results/labviz/site/cards/run-f9478bc050b12916.json",
    "results/labviz/site/cards/run-f984f0f4bbe657ae.json",
    "results/labviz/site/cards/run-f9d0f4481ba379fd.json",
    "results/labviz/site/cards/run-f9e673159c8f0ab6.json",
    "results/labviz/site/cards/run-f9ed47400bcc37b7.json",
    "results/labviz/site/cards/run-fa48eb972041dbf5.json",
    "results/labviz/site/cards/run-fa64e202fdd803fb.json",
    "results/labviz/site/cards/run-faa6c4fdab7b842c.json",
    "results/labviz/site/cards/run-fad7810d80f896f4.json",
    "results/labviz/site/cards/run-fafc6e041752ebb1.json",
    "results/labviz/site/cards/run-fba49575415b7361.json",
    "results/labviz/site/cards/run-fbc98ba338e833b8.json",
    "results/labviz/site/cards/run-fbcbe4417f5af4d9.json",
    "results/labviz/site/cards/run-fbee00aa79384064.json",
    "results/labviz/site/cards/run-fc0645186e4042b2.json",
    "results/labviz/site/cards/run-fc1f610971f94672.json",
    "results/labviz/site/cards/run-fc41d2b90b9f4d19.json",
    "results/labviz/site/cards/run-fc4f546ba0db52cf.json",
    "results/labviz/site/cards/run-fccb26d97f39476a.json",
    "results/labviz/site/cards/run-fcdcbeb5c836dde1.json",
    "results/labviz/site/cards/run-fd0a3ac2dadef062.json",
    "results/labviz/site/cards/run-fd6b94281d61637a.json",
    "results/labviz/site/cards/run-fd9edfd158b462c7.json",
    "results/labviz/site/cards/run-fdbc685fdf7cd9a7.json",
    "results/labviz/site/cards/run-fe1f4539ce818f36.json",
    "results/labviz/site/cards/run-fe1f5150f2dbf958.json",
    "results/labviz/site/cards/run-fe37318a41860d0d.json",
    "results/labviz/site/cards/run-fe679f40ffa65742.json",
    "results/labviz/site/cards/run-fe6ee1d8c94e8c7a.json",
    "results/labviz/site/cards/run-fe8bcabee408d3df.json",
    "results/labviz/site/cards/run-feb11f7ab1a4df65.json",
    "results/labviz/site/cards/run-febbb7b0d39b3112.json",
    "results/labviz/site/cards/run-fee34cc42595671c.json",
    "results/labviz/site/cards/run-fef020ba556323b9.json",
    "results/labviz/site/cards/run-fef8f8850bf54c50.json",
    "results/labviz/site/cards/run-ffcb76f44711b00e.json",
    "results/labviz/site/cards/scales.json",
    "results/labviz/site/context.json",
    "results/labviz/site/data.js",
    "results/labviz/site/evidence",
    "results/labviz/site/evidence/CORPUS",
    "results/labviz/site/evidence/CORPUS/00_MASTER_EVIDENCE.md",
    "results/labviz/site/evidence/CORPUS/01_PROVENANCE_MANIFEST.md",
    "results/labviz/site/evidence/CORPUS/02_VANDV_CHAIN.md",
    "results/labviz/site/evidence/CORPUS/03_STATUS_LEDGER.md",
    "results/labviz/site/evidence/CORPUS/55_C10W_ORACLE_P1_INTERIM.md",
    "results/labviz/site/evidence/CORPUS/56_C10V_LAYERPICK.md",
    "results/labviz/site/evidence/CORPUS/57_C10W_ORACLE_FINAL.md",
    "results/labviz/site/evidence/EXPERIMENT_RUNBOOK.md",
    "results/labviz/site/evidence/docs",
    "results/labviz/site/evidence/docs/EXPERIMENT_REGISTRY.md",
    "results/labviz/site/evidence/docs/HYPOTHESIS_REGISTER_2026-06-18.md",
    "results/labviz/site/evidence/docs/SPEC_EXPERIMENT_OVERLAY.md",
    "results/labviz/site/evidence/docs/c10_evaluations.json",
    "results/labviz/site/evidence/docs/c10_scoreboard.json",
    "results/labviz/site/evidence/results/c10w_oracle/p2_20261008T034226_086980Z",
    "results/labviz/site/evidence/results/c10w_oracle/p2_20261008T034226_086980Z/eval.json",
    "results/labviz/site/evidence/results/c10w_oracle/p2_20261008T034226_086980Z/p2-eval.log",
    "results/labviz/site/evidence/results/c10w_oracle/p2_20261008T034226_086980Z/verdict.json",
    "results/labviz/site/evidence/results/c10w_oracle_logs",
    "results/labviz/site/evidence/results/c10w_oracle_logs/p2-eval.log",
    "results/labviz/site/evidence/results/c10w_oracle_logs/p2-read-attempt2.json",
    "results/labviz/site/evidence/results/c10w_oracle_logs/p2-reattempt-coordinator.20261008T030455.59886.log",
    "results/labviz/site/evidence/tools/labviz",
    "results/labviz/site/evidence/tools/labviz/contexts.json",
    "results/labviz/site/evidence/tools/labviz/labels.json",
    "results/labviz/site/evidence/tools/labviz/links.json",
    "results/labviz/site/index.html",
    "results/labviz/site/model.js",
    "results/labviz/site/style.css",
    "results/labviz/survey.json",
    "results/labviz_v2_codex_impl.md",
    "results/labviz_v2_phase1_design_review_r2.md",
    "results/labviz_v2_phase1_design_review_r3.md",
    "results/labviz_v2_phase1_design_review_r4.md",
    "results/labviz_v2_phase1_design_review_r5.md",
    "results/templatepin_amend_astra.md",
    "results/templatepin_amend_astra_delta.md"
  ]
}
```

### Complete protected SHA table

| Protected file | Authorised before SHA | Final SHA | Equal |
|---|---|---|---|
| `.venv/lib/python3.11/site-packages/transformers/models/qwen2/modeling_qwen2.py` | `1760c628019995d3564c8572be6c5149f488b6c3aa95ceda16099c2516e146ff` | `1760c628019995d3564c8572be6c5149f488b6c3aa95ceda16099c2516e146ff` | True |
| `configs/hparams/anyedit_alphaedit_are_qwen25_3b.json` | `b7c8635b5ae876bb8a346ac2bc36d1ec438c2639021faebbdc838a046257f41e` | `b7c8635b5ae876bb8a346ac2bc36d1ec438c2639021faebbdc838a046257f41e` | True |
| `configs/hparams/anyedit_memit_are_qwen25_3b.json` | `c0774c602a28ece1425c83edc9f4da243b7908efdac1642a54e093fd26f16c8b` | `c0774c602a28ece1425c83edc9f4da243b7908efdac1642a54e093fd26f16c8b` | True |
| `configs/hparams/cfb-v4-highAKD-v0_1-draft.yaml` | `495415f88ebc0882bbe28ed8b11a3e6f2e76884fec3f2d485975093e984aae9c` | `495415f88ebc0882bbe28ed8b11a3e6f2e76884fec3f2d485975093e984aae9c` | True |
| `configs/hparams/cfb-v4-highAKD.yaml` | `e3ce9cb8690f70ba4d7335cf1a11679a8d79fa9563c3ef9ffca9840e9fb1e30f` | `e3ce9cb8690f70ba4d7335cf1a11679a8d79fa9563c3ef9ffca9840e9fb1e30f` | True |
| `configs/hparams/llama32_3b_memit_hparams.json` | `24a22192538cc9092925f78b6e93f3e3129cdc5513b1e0034c43386ead8ffb26` | `24a22192538cc9092925f78b6e93f3e3129cdc5513b1e0034c43386ead8ffb26` | True |
| `configs/hparams/probe-set-v4-highAKD.yaml` | `b99b5d9b8ed1d093869aed902be8464e41677d83a1c988ca3ae2150a1338d1fd` | `b99b5d9b8ed1d093869aed902be8464e41677d83a1c988ca3ae2150a1338d1fd` | True |
| `configs/hparams/qwen25_3b_memit_hparams.json` | `4225cc6aabc3eb9fa62d2bb2cac68b1238de3a39c5e469da635e6e1464aa3bb4` | `4225cc6aabc3eb9fa62d2bb2cac68b1238de3a39c5e469da635e6e1464aa3bb4` | True |
| `configs/hparams/qwen25_3b_memit_hparams_band412.json` | `7bdfae32d16f7cd8a53bc901642f6377476ebfa5c10d4d37fd69494c8cb2e618` | `7bdfae32d16f7cd8a53bc901642f6377476ebfa5c10d4d37fd69494c8cb2e618` | True |
| `configs/hparams/qwen25_3b_memit_hparams_band41218.json` | `191e6283056a6914c51ab0f8bf5629c72faf0bb84cff5ee25207f6b63e7705d5` | `191e6283056a6914c51ab0f8bf5629c72faf0bb84cff5ee25207f6b63e7705d5` | True |
| `configs/hparams/qwen25_3b_memit_hparams_band412_lowcov2500.json` | `df16866eb68327f465b0beee43b0b1b0a0c6dea5aa7a0c4f5700e864c2705f2b` | `df16866eb68327f465b0beee43b0b1b0a0c6dea5aa7a0c4f5700e864c2705f2b` | True |
| `configs/hparams/qwen25_3b_memit_hparams_band412_strength150.json` | `31337200e25891391427d21009829ef8d253c4fd384eedeeb5d2d9bfbd605dcd` | `31337200e25891391427d21009829ef8d253c4fd384eedeeb5d2d9bfbd605dcd` | True |
| `configs/hparams/qwen25_3b_memit_hparams_band812.json` | `f9a8ee42e5cd91937d3fdab852e19e971c554da3a383d6dc4c9f305a2192d546` | `f9a8ee42e5cd91937d3fdab852e19e971c554da3a383d6dc4c9f305a2192d546` | True |
| `configs/hparams/qwen25_3b_memit_hparams_mom2w25.json` | `afb77fe8ab5241d7a33fd183121715d1b1389de905de741ad3cef6f98a197083` | `afb77fe8ab5241d7a33fd183121715d1b1389de905de741ad3cef6f98a197083` | True |
| `configs/hparams/qwen25_3b_memit_hparams_mom2w50.json` | `6d171a27d1c6dbaf6240c7e715be96caff954dd9f2958dd17b8b054c5dc85272` | `6d171a27d1c6dbaf6240c7e715be96caff954dd9f2958dd17b8b054c5dc85272` | True |
| `configs/hparams/qwen25_3b_memit_hparams_mom2w500.json` | `797d53e19889353eb57d122e8d54f1d3d22b46142658baa1858b3e43e755f8f9` | `797d53e19889353eb57d122e8d54f1d3d22b46142658baa1858b3e43e755f8f9` | True |
| `configs/hparams/qwen25_3b_memit_hparams_set48.json` | `73c075619c2b9c43d870adae0d55c1e488f3a016b3e9ccc96dec71d8e7198be2` | `73c075619c2b9c43d870adae0d55c1e488f3a016b3e9ccc96dec71d8e7198be2` | True |
| `configs/hparams/qwen25_3b_memit_hparams_set78.json` | `93ce4befc96526da4fa2a85ce7f94c521927c83295bf850dd5ac9e84dc2ab256` | `93ce4befc96526da4fa2a85ce7f94c521927c83295bf850dd5ac9e84dc2ab256` | True |
| `configs/hparams/qwen25_3b_memit_hparams_smoke.json` | `bd11f757196eeebeda2c2eb597d449e1626882441036831c606ccd0f0428faac` | `bd11f757196eeebeda2c2eb597d449e1626882441036831c606ccd0f0428faac` | True |
| `configs/hparams/qwen25_3b_memit_hparams_steps50.json` | `f7a10f00eb1f7e37764aba0f6a231b3b0d316066f7f734f1e418a339acaeff33` | `f7a10f00eb1f7e37764aba0f6a231b3b0d316066f7f734f1e418a339acaeff33` | True |
| `configs/hparams/qwen25_3b_relkey_memit_hparams.json` | `343c54cd2d95c20990c56c15b90a9ac36cb45ef0c12a9a264166ff06a10d3bbf` | `343c54cd2d95c20990c56c15b90a9ac36cb45ef0c12a9a264166ff06a10d3bbf` | True |
| `configs/hparams/qwen25_7b_memit_hparams.json` | `81b2ccc7bddfd607ca1894efd5ef4bba9fb073f51b68024125307db65374e128` | `81b2ccc7bddfd607ca1894efd5ef4bba9fb073f51b68024125307db65374e128` | True |
| `configs/hparams/qwen3_06b_memit_hparams.json` | `c22468894e3e2f20ae389f59342e5163f6894fb584486d8dced719c392a76aa7` | `c22468894e3e2f20ae389f59342e5163f6894fb584486d8dced719c392a76aa7` | True |
| `configs/probes/b3_probes.json` | `9471d33901a042de842a99d1c84bd904ec2e6a24a2ee994630b7df34649d8a9b` | `9471d33901a042de842a99d1c84bd904ec2e6a24a2ee994630b7df34649d8a9b` | True |
| `configs/screens/g6_screen_qwen3b.json` | `a51813340571f6c68908ac4310cca197ebac9884939f58e5c33fb75833a3ca05` | `a51813340571f6c68908ac4310cca197ebac9884939f58e5c33fb75833a3ca05` | True |
| `configs/screens/g6_screen_qwen3b_v2.json` | `482c05f8f33c59d3e469566fe6f3c48eb183d3cb2fbb791f31dcad7102517c5c` | `482c05f8f33c59d3e469566fe6f3c48eb183d3cb2fbb791f31dcad7102517c5c` | True |
| `configs/screens/g6_screen_qwen7b.json` | `7c5a63282d8b815393e0a5dc3641dbfb61c5a0e95e530e4446f163816d75b43c` | `7c5a63282d8b815393e0a5dc3641dbfb61c5a0e95e530e4446f163816d75b43c` | True |
| `docs/C10U_MINT2_PREREG.md` | `2bbd7bcd9b4df869590e319c215c2f9e07fcef1cc986783e70c4632f8154e4e5` | `2bbd7bcd9b4df869590e319c215c2f9e07fcef1cc986783e70c4632f8154e4e5` | True |
| `docs/C10V_LAYERPICK_PREREG.md` | `00981bfc9cb5770ccea203f6682d953948afdba653a4bd4173bbc754130ad524` | `00981bfc9cb5770ccea203f6682d953948afdba653a4bd4173bbc754130ad524` | True |
| `docs/C10Y_DIRECTDW_PREREG.md` | `e069b358c362b2a05e3b668e8a29f33061e15a24306e321452e6fa46a4e83331` | `e069b358c362b2a05e3b668e8a29f33061e15a24306e321452e6fa46a4e83331` | True |
| `docs/C10Z_ASTRA_PREREG.md` | `87fe3d5d28c9a51eab4eadfd82cc7175f1a94f723f25f31658c5e1aeaf628b87` | `7c6e52e274e3dbc30cd5123d6b56ae8c9b1dca8c5e7507ff7be15d57e845059d` | False |
| `experiments/track_c/c10e_bandknob.py` | `1f6be5811d7e58f3ebda16867a4a174b1cf24d47f9a2514cf9c3f9d29f18e695` | `1f6be5811d7e58f3ebda16867a4a174b1cf24d47f9a2514cf9c3f9d29f18e695` | True |
| `experiments/track_c/c10l_covgeom_step0.py` | `5999d8714b7282e01f04b0292dc2c381d383f2a7ff90a2430b6e503aa7f2a557` | `5999d8714b7282e01f04b0292dc2c381d383f2a7ff90a2430b6e503aa7f2a557` | True |
| `experiments/track_c/c10p_twopass_arms.py` | `c34ecbe17c86d8f2803efc5520f4cf090dcb23bcc21ef0c3c28a12bfdaeb820f` | `c34ecbe17c86d8f2803efc5520f4cf090dcb23bcc21ef0c3c28a12bfdaeb820f` | True |
| `experiments/track_c/c10z_astra_arms.py` | `806a9b4d417261945359d45db8c2f8513e4f5a2f3fafaf0b7cefe3a8d5ec3304` | `ab6f5c809d8187f4e5eb39e9cc6fbf40b6e357b2ecf5b18ecc887e05de7adebc` | False |
| `experiments/track_c/c10z_astra_benchmark.py` | `9b25a207f630fbfa0d60c80a74f22289ad3bb2cc160d0fc72d7e0367f9a47a1a` | `9b25a207f630fbfa0d60c80a74f22289ad3bb2cc160d0fc72d7e0367f9a47a1a` | True |
| `hf_cache/hub/models--Qwen--Qwen2.5-3B/snapshots/3aab1f1954e9cc14eb9509a215f9e5ca08227a9b/config.json` | `27467e2fc311a7656c09a43ae9c3d408211e1f212bbddbc93c8596a06423826f` | `27467e2fc311a7656c09a43ae9c3d408211e1f212bbddbc93c8596a06423826f` | True |
| `memit_dry_run/memit/.gitattributes` | `0d8fc1b86a58cb959c95bc6d62652b6a06ec8a1161d0fab6af1bcabbde43b630` | `0d8fc1b86a58cb959c95bc6d62652b6a06ec8a1161d0fab6af1bcabbde43b630` | True |
| `memit_dry_run/memit/.gitignore` | `8d0aba79068af0ed4093807588d236cfe576a1e7c08993549f65ec2e1cbc931b` | `8d0aba79068af0ed4093807588d236cfe576a1e7c08993549f65ec2e1cbc931b` | True |
| `memit_dry_run/memit/CITATION.cff` | `974adb58a9fd1e6a2375244d22c8601a3a614257b006c534863ade12056a9514` | `974adb58a9fd1e6a2375244d22c8601a3a614257b006c534863ade12056a9514` | True |
| `memit_dry_run/memit/LICENSE` | `46c273d5a0a7f8bc3889863398e1bb20493e256f38033dfd637ec46bf654c531` | `46c273d5a0a7f8bc3889863398e1bb20493e256f38033dfd637ec46bf654c531` | True |
| `memit_dry_run/memit/README.md` | `e14b1c0aff11f1ebb5b427115cdd660892e0305bb868102c1330299017b69b13` | `e14b1c0aff11f1ebb5b427115cdd660892e0305bb868102c1330299017b69b13` | True |
| `memit_dry_run/memit/baselines/README.md` | `e44248aeb435f44301544b39c92195baa1367552978f9f20060a186c1c223e95` | `e44248aeb435f44301544b39c92195baa1367552978f9f20060a186c1c223e95` | True |
| `memit_dry_run/memit/baselines/ft/__init__.py` | `19646aa4d3c5b6fd8dc0032aab1cee6afc7ab24e7404c5c657cadbdd077ea0fd` | `19646aa4d3c5b6fd8dc0032aab1cee6afc7ab24e7404c5c657cadbdd077ea0fd` | True |
| `memit_dry_run/memit/baselines/ft/ft_hparams.py` | `fdd83bbc0cb87ebc1b6aae238a38798aab6e2b8b1723e666e797c1c5df851ab1` | `fdd83bbc0cb87ebc1b6aae238a38798aab6e2b8b1723e666e797c1c5df851ab1` | True |
| `memit_dry_run/memit/baselines/ft/ft_main.py` | `ce8bffb4716a6ec97c5690a10b7be585da6d009028f6d77c9ac7907caaea378a` | `ce8bffb4716a6ec97c5690a10b7be585da6d009028f6d77c9ac7907caaea378a` | True |
| `memit_dry_run/memit/baselines/mend/README.md` | `43f8919beb3498934f0282763523db4f1b0825d98c103bbd4230fce52e756076` | `43f8919beb3498934f0282763523db4f1b0825d98c103bbd4230fce52e756076` | True |
| `memit_dry_run/memit/baselines/mend/__init__.py` | `ce6f24b656aa412ba07c893dd6fa37001d0a148312c9fd5b823ac27c83e145b0` | `ce6f24b656aa412ba07c893dd6fa37001d0a148312c9fd5b823ac27c83e145b0` | True |
| `memit_dry_run/memit/baselines/mend/algs/enn.py` | `fcde13387249220bf8ccde0c8bf174f6444a956806f86aee0c4c1a0c062e3a90` | `fcde13387249220bf8ccde0c8bf174f6444a956806f86aee0c4c1a0c062e3a90` | True |
| `memit_dry_run/memit/baselines/mend/algs/ft.py` | `c60355576cac69dbca0816a4747cbb7bbba7a2352d0e7edb2191d870450eeff7` | `c60355576cac69dbca0816a4747cbb7bbba7a2352d0e7edb2191d870450eeff7` | True |
| `memit_dry_run/memit/baselines/mend/algs/mend.py` | `3d94e338ff9efe07815d9d4d339485e9abaa17af555f88d0adacb0a3ad19eca5` | `3d94e338ff9efe07815d9d4d339485e9abaa17af555f88d0adacb0a3ad19eca5` | True |
| `memit_dry_run/memit/baselines/mend/config/alg/efk.yaml` | `6d8a009b23a6d15971f0fd3f41f446e55f9f439ddd4f37f37e003a9ba39c3d4b` | `6d8a009b23a6d15971f0fd3f41f446e55f9f439ddd4f37f37e003a9ba39c3d4b` | True |
| `memit_dry_run/memit/baselines/mend/config/alg/enn.yaml` | `5d57b48f592317500c828b93650db753917781cacae4b72afbaf6af7bcdfff96` | `5d57b48f592317500c828b93650db753917781cacae4b72afbaf6af7bcdfff96` | True |
| `memit_dry_run/memit/baselines/mend/config/alg/ft.yaml` | `f2ed848825e236de2073930e6bea4faf2ca1f6c828a7f84d79fad54a0b7e607d` | `f2ed848825e236de2073930e6bea4faf2ca1f6c828a7f84d79fad54a0b7e607d` | True |
| `memit_dry_run/memit/baselines/mend/config/alg/mend.yaml` | `bce5e203d627552b2caf8d1a3b185ccaf28773b285a17a9f27538a86fe9eea87` | `bce5e203d627552b2caf8d1a3b185ccaf28773b285a17a9f27538a86fe9eea87` | True |
| `memit_dry_run/memit/baselines/mend/config/config.yaml` | `d46810afd50bf9dc19b443df22f7c77ee88ae03f7540bb7939b6eeaba4079d96` | `d46810afd50bf9dc19b443df22f7c77ee88ae03f7540bb7939b6eeaba4079d96` | True |
| `memit_dry_run/memit/baselines/mend/config/experiment/fc.yaml` | `678a899a35e0840de77f5fea74236c9f0d8b9ea4f0b8e1a05b981cfac131a043` | `678a899a35e0840de77f5fea74236c9f0d8b9ea4f0b8e1a05b981cfac131a043` | True |
| `memit_dry_run/memit/baselines/mend/config/experiment/gen.yaml` | `c208288115ae91d8cd47dfcc6c157e94d41657eebef327700363ed288f9dbee3` | `c208288115ae91d8cd47dfcc6c157e94d41657eebef327700363ed288f9dbee3` | True |
| `memit_dry_run/memit/baselines/mend/config/experiment/qa.yaml` | `038666cff47e927cc70891afcc2efd0f62898274d0287f1ab0719c3771394027` | `038666cff47e927cc70891afcc2efd0f62898274d0287f1ab0719c3771394027` | True |
| `memit_dry_run/memit/baselines/mend/config/model/bart-base.yaml` | `25eac9c87259e197ecf587413f4660098b779c6b21fa1cc6584e7d64b1479475` | `25eac9c87259e197ecf587413f4660098b779c6b21fa1cc6584e7d64b1479475` | True |
| `memit_dry_run/memit/baselines/mend/config/model/bert-base.yaml` | `49ff1dc40a3306dd7649f697c134e6ed0f83e5382038f18962793f3eca410e01` | `49ff1dc40a3306dd7649f697c134e6ed0f83e5382038f18962793f3eca410e01` | True |
| `memit_dry_run/memit/baselines/mend/config/model/distilgpt2.yaml` | `ba77ac0a70e92efac417a8f9b2aa25872f4c0152ae7e6bcb7a1a1c394e88a0d7` | `ba77ac0a70e92efac417a8f9b2aa25872f4c0152ae7e6bcb7a1a1c394e88a0d7` | True |
| `memit_dry_run/memit/baselines/mend/config/model/gpt2.yaml` | `6c9ac030faea26cfa57a21d10713298b5b05e2acfcda057db9ef8b7797e0182d` | `6c9ac030faea26cfa57a21d10713298b5b05e2acfcda057db9ef8b7797e0182d` | True |
| `memit_dry_run/memit/baselines/mend/config/model/gpt2large.yaml` | `feeab1704c76f5917876da5c631940dfde806dfdf0bf37f704ae29e8081c016c` | `feeab1704c76f5917876da5c631940dfde806dfdf0bf37f704ae29e8081c016c` | True |
| `memit_dry_run/memit/baselines/mend/config/model/gpt2medium.yaml` | `a943050f9ad67b30e16e312d0a63b8dff6518a582e5c49d4f36475931dee5dc6` | `a943050f9ad67b30e16e312d0a63b8dff6518a582e5c49d4f36475931dee5dc6` | True |
| `memit_dry_run/memit/baselines/mend/config/model/gpt2xl.yaml` | `5eb704b1c06b3636eb62db43614f87650412d08c2c6f374555187c194f031429` | `5eb704b1c06b3636eb62db43614f87650412d08c2c6f374555187c194f031429` | True |
| `memit_dry_run/memit/baselines/mend/config/model/gptj.yaml` | `0f3fe0caa24560fc62ffe7c2752cc23b5216bf99291d0fe969a55026982e4868` | `0f3fe0caa24560fc62ffe7c2752cc23b5216bf99291d0fe969a55026982e4868` | True |
| `memit_dry_run/memit/baselines/mend/config/model/gptneo27.yaml` | `809ce5da7d801f0b9c7ffc1b4b53632b23c7c8544f5dd1a401b8be4d3f17a46a` | `809ce5da7d801f0b9c7ffc1b4b53632b23c7c8544f5dd1a401b8be4d3f17a46a` | True |
| `memit_dry_run/memit/baselines/mend/config/model/t5large.yaml` | `109cf49c1cb32333e492e79d9974fa3e75f8c9a0459d40c872571e4eb13c85d5` | `109cf49c1cb32333e492e79d9974fa3e75f8c9a0459d40c872571e4eb13c85d5` | True |
| `memit_dry_run/memit/baselines/mend/config/model/t5small.yaml` | `cee5cfbb9295137f1ecf154949c55f0f76254941d9cb48ecdd66bc6decd1a929` | `cee5cfbb9295137f1ecf154949c55f0f76254941d9cb48ecdd66bc6decd1a929` | True |
| `memit_dry_run/memit/baselines/mend/config/model/t5xl.yaml` | `e9611b81bd40bb80c21f462b195095deabab3d3d6ac344165ba16a3ec45bc5a6` | `e9611b81bd40bb80c21f462b195095deabab3d3d6ac344165ba16a3ec45bc5a6` | True |
| `memit_dry_run/memit/baselines/mend/config/model/t5xxl.yaml` | `690ee1486411befec7312a0e37ed4ef615a57e1c74e4f7bea39ed6f87530d427` | `690ee1486411befec7312a0e37ed4ef615a57e1c74e4f7bea39ed6f87530d427` | True |
| `memit_dry_run/memit/baselines/mend/data_classes/fever.py` | `098397ce1214eb8cce6b90c8ba6ebd67024afcbc2f58ccaf887b5a365732308a` | `098397ce1214eb8cce6b90c8ba6ebd67024afcbc2f58ccaf887b5a365732308a` | True |
| `memit_dry_run/memit/baselines/mend/data_classes/nq.py` | `f8d8dfaadf866e82c50e4c5bfef14a9b54aa5799aca3cea8f403f0461ba61f69` | `f8d8dfaadf866e82c50e4c5bfef14a9b54aa5799aca3cea8f403f0461ba61f69` | True |
| `memit_dry_run/memit/baselines/mend/data_classes/wiki.py` | `60ea3f99dcb4386f38454fdda9b7a65963df76240ce516d093e396a969576627` | `60ea3f99dcb4386f38454fdda9b7a65963df76240ce516d093e396a969576627` | True |
| `memit_dry_run/memit/baselines/mend/data_classes/zsre.py` | `2acb707212802d65a55f46ada4381af330ff1cc9842ed9c56326de14b0711581` | `2acb707212802d65a55f46ada4381af330ff1cc9842ed9c56326de14b0711581` | True |
| `memit_dry_run/memit/baselines/mend/editable_model.py` | `34330a12b9864001ea46ecae794df1ea85cedb38082df783b31d67cc8939e245` | `34330a12b9864001ea46ecae794df1ea85cedb38082df783b31d67cc8939e245` | True |
| `memit_dry_run/memit/baselines/mend/hooks.py` | `b6037d8f9778f2d74952dafe3acc76f761df6884d85e9b5b57559cd08f7d2d6f` | `b6037d8f9778f2d74952dafe3acc76f761df6884d85e9b5b57559cd08f7d2d6f` | True |
| `memit_dry_run/memit/baselines/mend/losses.py` | `271a10d9e995ffd92c2de239f652928d651013f8a0889bd4205ffca1469127e8` | `271a10d9e995ffd92c2de239f652928d651013f8a0889bd4205ffca1469127e8` | True |
| `memit_dry_run/memit/baselines/mend/mend_hparams.py` | `071bc2c833cd1362906eee12b081c272650f909e9c93389bb05be86ae8626eb3` | `071bc2c833cd1362906eee12b081c272650f909e9c93389bb05be86ae8626eb3` | True |
| `memit_dry_run/memit/baselines/mend/mend_main.py` | `7e72af6f626798696f50c81ad72276f4807422bd365d5d6f130ca7e2852f53b5` | `7e72af6f626798696f50c81ad72276f4807422bd365d5d6f130ca7e2852f53b5` | True |
| `memit_dry_run/memit/baselines/mend/models.py` | `2e94d797f3813d57a532c676ba6609a91e89eb36bdfb8479bc092dccc5ce4420` | `2e94d797f3813d57a532c676ba6609a91e89eb36bdfb8479bc092dccc5ce4420` | True |
| `memit_dry_run/memit/baselines/mend/nn.py` | `ffca4fb48675c4c6cf56bb9cbbff8ce50f2c46eb8fdbfc6a7e1b6308acddab92` | `ffca4fb48675c4c6cf56bb9cbbff8ce50f2c46eb8fdbfc6a7e1b6308acddab92` | True |
| `memit_dry_run/memit/baselines/mend/oracle.py` | `d3657df3b292a4c78564c59b9a07ccdb8e6ff74b111cd489e38c5e5112ad4b1b` | `d3657df3b292a4c78564c59b9a07ccdb8e6ff74b111cd489e38c5e5112ad4b1b` | True |
| `memit_dry_run/memit/baselines/mend/requirements.txt` | `17082daf26c99220b8bfff81f282ca445e19b6ee69835f31009a4ce0d0ed20cd` | `17082daf26c99220b8bfff81f282ca445e19b6ee69835f31009a4ce0d0ed20cd` | True |
| `memit_dry_run/memit/baselines/mend/run.py` | `2e57976fb507bc5bc27f88ea8a7bacd7b2a75d6b45170ed4870643ae5ce74765` | `2e57976fb507bc5bc27f88ea8a7bacd7b2a75d6b45170ed4870643ae5ce74765` | True |
| `memit_dry_run/memit/baselines/mend/trainer.py` | `91c9d6378c0cbe6340cf4591618a68aa70f805059a01881f43c71859e001dcb1` | `91c9d6378c0cbe6340cf4591618a68aa70f805059a01881f43c71859e001dcb1` | True |
| `memit_dry_run/memit/baselines/mend/utils.py` | `bb981c845c07709efa4e81610ec575be7e3f3b909a42b79610a47044c04c0554` | `bb981c845c07709efa4e81610ec575be7e3f3b909a42b79610a47044c04c0554` | True |
| `memit_dry_run/memit/dsets/__init__.py` | `a2e1c9d7a56af0b091a48cb313a356cdb1a923e1bb046d73bd0d1e10c7b0d907` | `a2e1c9d7a56af0b091a48cb313a356cdb1a923e1bb046d73bd0d1e10c7b0d907` | True |
| `memit_dry_run/memit/dsets/attr_snippets.py` | `bf78972d9914919e0a0b7d7d93623b3f51b8684f691e909793b5cd5471d6f01a` | `bf78972d9914919e0a0b7d7d93623b3f51b8684f691e909793b5cd5471d6f01a` | True |
| `memit_dry_run/memit/dsets/counterfact.py` | `7848e935a578c40e187167a2894601b0dbf42d2334b5289a012276ea1eb672b5` | `7848e935a578c40e187167a2894601b0dbf42d2334b5289a012276ea1eb672b5` | True |
| `memit_dry_run/memit/dsets/knowns.py` | `e2428c36d17b0dec1f390888a98334bd0fd1f64168bffae7566ef8a8606f361e` | `e2428c36d17b0dec1f390888a98334bd0fd1f64168bffae7566ef8a8606f361e` | True |
| `memit_dry_run/memit/dsets/tfidf_stats.py` | `34f03d97b0b1aaad33e75a211a3d6b502cfb9eace1c172320df6ceb713d600c9` | `34f03d97b0b1aaad33e75a211a3d6b502cfb9eace1c172320df6ceb713d600c9` | True |
| `memit_dry_run/memit/dsets/zsre.py` | `a6281375afd9983337c154095fe9aba59c74c36fa34ecfb12838c7b5c341670e` | `a6281375afd9983337c154095fe9aba59c74c36fa34ecfb12838c7b5c341670e` | True |
| `memit_dry_run/memit/experiments/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | True |
| `memit_dry_run/memit/experiments/causal_trace.py` | `9436fd596a39e240a01121da601359bea5d0b3a350c0faa34aa8b0ccac05560b` | `9436fd596a39e240a01121da601359bea5d0b3a350c0faa34aa8b0ccac05560b` | True |
| `memit_dry_run/memit/experiments/evaluate.py` | `4ef8e138bb8003c8486935ad0eae86d9ccd84bb61cfa1f88b63f0ed06c2d1760` | `4ef8e138bb8003c8486935ad0eae86d9ccd84bb61cfa1f88b63f0ed06c2d1760` | True |
| `memit_dry_run/memit/experiments/py/demo.py` | `268c16a1c2c4e8642b7641739c2cd0808c08be80f36f280d1e5bef4944733772` | `268c16a1c2c4e8642b7641739c2cd0808c08be80f36f280d1e5bef4944733772` | True |
| `memit_dry_run/memit/experiments/py/eval_utils_counterfact.py` | `b00d9810305580dddfeb5e65129db4d56bcbfee1edf020605e21bf4f5033aeb7` | `b00d9810305580dddfeb5e65129db4d56bcbfee1edf020605e21bf4f5033aeb7` | True |
| `memit_dry_run/memit/experiments/py/eval_utils_zsre.py` | `e4f18c84a813d0a2fb9a5c9426726844117fe365cae72107d51f304a264d77a8` | `e4f18c84a813d0a2fb9a5c9426726844117fe365cae72107d51f304a264d77a8` | True |
| `memit_dry_run/memit/experiments/summarize.py` | `7de8f5eec86243807825cf9f62923535f853cce07d2d3248534f86320f229372` | `7de8f5eec86243807825cf9f62923535f853cce07d2d3248534f86320f229372` | True |
| `memit_dry_run/memit/experiments/sweep.py` | `bfc7a91e9abb526814f7d975a81ff0333e930b452e2da58b31dc2ae8a10cce74` | `bfc7a91e9abb526814f7d975a81ff0333e930b452e2da58b31dc2ae8a10cce74` | True |
| `memit_dry_run/memit/globals.yml` | `86ab5194b3cddc19c14173a3b8f13563c554d252666eb563a4ac2f919e087459` | `86ab5194b3cddc19c14173a3b8f13563c554d252666eb563a4ac2f919e087459` | True |
| `memit_dry_run/memit/globals.yml.upstream_default.20260430T035736Z` | `f05226b5d0b64a25106fbfa2da3b4de3b69d8e6797c7757f8a6679756820845c` | `f05226b5d0b64a25106fbfa2da3b4de3b69d8e6797c7757f8a6679756820845c` | True |
| `memit_dry_run/memit/hparams/FT/EleutherAI_gpt-j-6B_constr.json` | `018e27089431ed3632aa0b8f2f1b4aa51daa81ba39f24952a400a92df84fa28b` | `018e27089431ed3632aa0b8f2f1b4aa51daa81ba39f24952a400a92df84fa28b` | True |
| `memit_dry_run/memit/hparams/FT/EleutherAI_gpt-j-6B_unconstr.json` | `1d605b748ed9709efb19d3f04c82de2d1ff12c81144c1d6621e72408f838d098` | `1d605b748ed9709efb19d3f04c82de2d1ff12c81144c1d6621e72408f838d098` | True |
| `memit_dry_run/memit/hparams/FT/EleutherAI_gpt-j-6B_wd.json` | `5161e47c66580d13524abc1bbbb42b146163ff2f51121a4c74f23679bbad8254` | `5161e47c66580d13524abc1bbbb42b146163ff2f51121a4c74f23679bbad8254` | True |
| `memit_dry_run/memit/hparams/FT/gpt2-large_constr.json` | `48298eec3688c393dcf610e114b30a521fa3d8b5fc7fb5d5e938f61996f93d19` | `48298eec3688c393dcf610e114b30a521fa3d8b5fc7fb5d5e938f61996f93d19` | True |
| `memit_dry_run/memit/hparams/FT/gpt2-medium_constr.json` | `fd1b7a80dff0e6d1c8e32c38b0ab620505ed1668d366d292a5776a49d2d7e23d` | `fd1b7a80dff0e6d1c8e32c38b0ab620505ed1668d366d292a5776a49d2d7e23d` | True |
| `memit_dry_run/memit/hparams/FT/gpt2-xl_attn.json` | `28348947fe372113c6fc9d0a1b851121dbf8e198311ae7d573b4b6f8173a477b` | `28348947fe372113c6fc9d0a1b851121dbf8e198311ae7d573b4b6f8173a477b` | True |
| `memit_dry_run/memit/hparams/FT/gpt2-xl_constr.json` | `6f1a26e915b2fc5a203443322aa224f4dd47150117f1cc5d1ee7f8026108047f` | `6f1a26e915b2fc5a203443322aa224f4dd47150117f1cc5d1ee7f8026108047f` | True |
| `memit_dry_run/memit/hparams/FT/gpt2-xl_unconstr.json` | `484393773f7a18844dd7c7f212673e4a8113515f0dfcc29c9d02c494f13bb137` | `484393773f7a18844dd7c7f212673e4a8113515f0dfcc29c9d02c494f13bb137` | True |
| `memit_dry_run/memit/hparams/MEMIT/EleutherAI_gpt-j-6B.json` | `ac1c641470c003032f15cf3f3db088e215f289535b7ea8c171ccb1235cd7bf43` | `ac1c641470c003032f15cf3f3db088e215f289535b7ea8c171ccb1235cd7bf43` | True |
| `memit_dry_run/memit/hparams/MEMIT/Llama-3.1-8B.json` | `bea608d313845440ebe5a3887034b271bca431dff10a6d09a8237c3256f894f2` | `bea608d313845440ebe5a3887034b271bca431dff10a6d09a8237c3256f894f2` | True |
| `memit_dry_run/memit/hparams/MEMIT/gpt2-xl.json` | `2c2ff7e8f3ff8b33cca2966a628f92f8b56bba72af51ca9af57d6c30a1c342d4` | `2c2ff7e8f3ff8b33cca2966a628f92f8b56bba72af51ca9af57d6c30a1c342d4` | True |
| `memit_dry_run/memit/hparams/MEMIT/meta-llama_Llama-3.1-8B.json` | `61007b61dd2119cbd281ba10d89fb3d34bdcfe03cfce4da542a0729e261caf12` | `61007b61dd2119cbd281ba10d89fb3d34bdcfe03cfce4da542a0729e261caf12` | True |
| `memit_dry_run/memit/hparams/MEND/EleutherAI_gpt-j-6B.json` | `d1e7bbd8a8486cda08af026c7cfdcc12b3a4fac3fab738a528e11adb8e52d97b` | `d1e7bbd8a8486cda08af026c7cfdcc12b3a4fac3fab738a528e11adb8e52d97b` | True |
| `memit_dry_run/memit/hparams/MEND/EleutherAI_gpt-j-6B_CF.json` | `b30a5f403fa4972201d1ca994c70b3c6dbd396d7163bd502bc1cbe571e87d44c` | `b30a5f403fa4972201d1ca994c70b3c6dbd396d7163bd502bc1cbe571e87d44c` | True |
| `memit_dry_run/memit/hparams/MEND/gpt2-xl.json` | `fe1a786ca540a3dee435621a56659d070b52b0354f85d08f9c0874f2e3d8fb79` | `fe1a786ca540a3dee435621a56659d070b52b0354f85d08f9c0874f2e3d8fb79` | True |
| `memit_dry_run/memit/hparams/MEND/gpt2-xl_CF.json` | `5691b370fc2b8540d2c28d608d53e2328005ce5b933ab9e04726bde7cf93f44e` | `5691b370fc2b8540d2c28d608d53e2328005ce5b933ab9e04726bde7cf93f44e` | True |
| `memit_dry_run/memit/hparams/MEND/gpt2-xl_zsRE.json` | `f6b0cc610281f474f702075064fe5eef83e0e7925d7f7d51036ee1fbc03a999a` | `f6b0cc610281f474f702075064fe5eef83e0e7925d7f7d51036ee1fbc03a999a` | True |
| `memit_dry_run/memit/hparams/ROME/EleutherAI_gpt-j-6B.json` | `85e44438c5a6bcd7769d73efadd10507f2b7ec7eeaa0330a310e351d2676fdff` | `85e44438c5a6bcd7769d73efadd10507f2b7ec7eeaa0330a310e351d2676fdff` | True |
| `memit_dry_run/memit/hparams/ROME/EleutherAI_gpt-neox-20b.json` | `fadf233859d46cf02ef219f74bced47652d277cd392de51c7c1ce6585d1d60b9` | `fadf233859d46cf02ef219f74bced47652d277cd392de51c7c1ce6585d1d60b9` | True |
| `memit_dry_run/memit/hparams/ROME/gpt2-large.json` | `2c5cb903948c6e261d2bb9aa2e9dfbd20ac30d38a2669054a25defcaed4a13ed` | `2c5cb903948c6e261d2bb9aa2e9dfbd20ac30d38a2669054a25defcaed4a13ed` | True |
| `memit_dry_run/memit/hparams/ROME/gpt2-medium.json` | `3a6b72ddf9e0b859e6909a1e144c5bb6958852a0e4fef36db0e4424c424c1913` | `3a6b72ddf9e0b859e6909a1e144c5bb6958852a0e4fef36db0e4424c424c1913` | True |
| `memit_dry_run/memit/hparams/ROME/gpt2-xl.json` | `81a98b788b8fbb89718288a8831441200e7d824fd057f62cb7d913ae4da5cf42` | `81a98b788b8fbb89718288a8831441200e7d824fd057f62cb7d913ae4da5cf42` | True |
| `memit_dry_run/memit/memit/__init__.py` | `911cc037562a368ca7017ea66f4821c5a848f286a55b7d624c242209afcd01df` | `911cc037562a368ca7017ea66f4821c5a848f286a55b7d624c242209afcd01df` | True |
| `memit_dry_run/memit/memit/__pycache__/__init__.cpython-311.pyc` | `29e09585ec894fc0109aa73db6f1de88df5087ac3e70069f069c7dba782a4287` | `29e09585ec894fc0109aa73db6f1de88df5087ac3e70069f069c7dba782a4287` | True |
| `memit_dry_run/memit/memit/__pycache__/compute_ks.cpython-311.pyc` | `9acefffad173c67f9d03a1c0705145f2ee6b5aef1679f0fbd7cd0c49495d544e` | `9acefffad173c67f9d03a1c0705145f2ee6b5aef1679f0fbd7cd0c49495d544e` | True |
| `memit_dry_run/memit/memit/__pycache__/compute_z.cpython-311.pyc` | `f3c78b5d8be2df307cc3bde53fc02a878469fc8f5c3473bf3a415b0dca3bd156` | `f3c78b5d8be2df307cc3bde53fc02a878469fc8f5c3473bf3a415b0dca3bd156` | True |
| `memit_dry_run/memit/memit/__pycache__/memit_hparams.cpython-311.pyc` | `d869204c04046a2ba2bc9e519fb324757b2bdad306d9365a6ce861ad687760f6` | `d869204c04046a2ba2bc9e519fb324757b2bdad306d9365a6ce861ad687760f6` | True |
| `memit_dry_run/memit/memit/__pycache__/memit_main.cpython-311.pyc` | `4432d0eb89db771924edde06dd958544f8f598c74297aa38e5250f713e12aeff` | `4432d0eb89db771924edde06dd958544f8f598c74297aa38e5250f713e12aeff` | True |
| `memit_dry_run/memit/memit/compute_ks.py` | `0b039be47c548f046b71cad4efce63414f53edbaa657bde868a20cdd35a2f5c7` | `0b039be47c548f046b71cad4efce63414f53edbaa657bde868a20cdd35a2f5c7` | True |
| `memit_dry_run/memit/memit/compute_z.py` | `d94af7fa14e5a4a20d5fa6361e0cbb30da0ff957db31922557ff809c34205dea` | `d94af7fa14e5a4a20d5fa6361e0cbb30da0ff957db31922557ff809c34205dea` | True |
| `memit_dry_run/memit/memit/memit_hparams.py` | `1b229b882b031ddbb59f06ad6ba58d5c33b17826bbfddf80f767e96931b595b2` | `1b229b882b031ddbb59f06ad6ba58d5c33b17826bbfddf80f767e96931b595b2` | True |
| `memit_dry_run/memit/memit/memit_main.py` | `d941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65` | `d941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65` | True |
| `memit_dry_run/memit/memit/memit_main.py.pre_p7_backup` | `4b5c6478da463bb174036a3a0495d7786f8e4d207ee7021a7e9afb6aef977168` | `4b5c6478da463bb174036a3a0495d7786f8e4d207ee7021a7e9afb6aef977168` | True |
| `memit_dry_run/memit/notebooks/average_causal_effects.ipynb` | `35598748d8ce10af976c8f2be331fdf5eb6081dcd1d564f4ec753258c0c2cafb` | `35598748d8ce10af976c8f2be331fdf5eb6081dcd1d564f4ec753258c0c2cafb` | True |
| `memit_dry_run/memit/notebooks/causal_trace.ipynb` | `755a31d3d4a34b56e253e21b4171f944e31a4e57fa8a9c38440f6e6731ab2711` | `755a31d3d4a34b56e253e21b4171f944e31a4e57fa8a9c38440f6e6731ab2711` | True |
| `memit_dry_run/memit/notebooks/causal_trace_frozen_mlp_attn.ipynb` | `0b3837b24d70939e44b2fbba5757f4f19e888bf858445714c0bcb574170d4fe0` | `0b3837b24d70939e44b2fbba5757f4f19e888bf858445714c0bcb574170d4fe0` | True |
| `memit_dry_run/memit/notebooks/globals.yml` | `86ab5194b3cddc19c14173a3b8f13563c554d252666eb563a4ac2f919e087459` | `86ab5194b3cddc19c14173a3b8f13563c554d252666eb563a4ac2f919e087459` | True |
| `memit_dry_run/memit/notebooks/memit.ipynb` | `dc79c89862a9ef57dd6cdf46715c716ef60103f97314b1f9fb5fff3be88f7235` | `dc79c89862a9ef57dd6cdf46715c716ef60103f97314b1f9fb5fff3be88f7235` | True |
| `memit_dry_run/memit/notebooks/vis/globals.yml` | `86ab5194b3cddc19c14173a3b8f13563c554d252666eb563a4ac2f919e087459` | `86ab5194b3cddc19c14173a3b8f13563c554d252666eb563a4ac2f919e087459` | True |
| `memit_dry_run/memit/notebooks/vis/table_population.ipynb` | `a5b6eb40955acbf7b37068ea782b04cfcb56794c6738b4eefbc3f38daff03ced` | `a5b6eb40955acbf7b37068ea782b04cfcb56794c6738b4eefbc3f38daff03ced` | True |
| `memit_dry_run/memit/notebooks/vis/table_population_zsre.ipynb` | `c34799ceafdcad5220b5d871989cda93de581419741c861c38bd62f63d0cac85` | `c34799ceafdcad5220b5d871989cda93de581419741c861c38bd62f63d0cac85` | True |
| `memit_dry_run/memit/notebooks/vis/visualize_multi_results.ipynb` | `05d42e5d00021f4a435c23ffc88dcc919597c744136be2607f86e1a94d71304e` | `05d42e5d00021f4a435c23ffc88dcc919597c744136be2607f86e1a94d71304e` | True |
| `memit_dry_run/memit/notebooks/vis/visualize_sweep_results.ipynb` | `58ae1129dd40e1f6620e77ae24f1f74417ed3e1c2487ebcec552025c6313f008` | `58ae1129dd40e1f6620e77ae24f1f74417ed3e1c2487ebcec552025c6313f008` | True |
| `memit_dry_run/memit/rome/README.md` | `4711e2605517fe1308cccd59748761e19342b4c0b0b26d2a9a32bbf3a93f94a6` | `4711e2605517fe1308cccd59748761e19342b4c0b0b26d2a9a32bbf3a93f94a6` | True |
| `memit_dry_run/memit/rome/__init__.py` | `87e6bd462753e8a86b84b2461da6067762cb0d5c9b7061b1b0598adb6f550a7a` | `87e6bd462753e8a86b84b2461da6067762cb0d5c9b7061b1b0598adb6f550a7a` | True |
| `memit_dry_run/memit/rome/__pycache__/__init__.cpython-311.pyc` | `174f5c000e030c096a7b21ec71e06661f3f348de8f2e3ad608fae32c8b8b5fe5` | `174f5c000e030c096a7b21ec71e06661f3f348de8f2e3ad608fae32c8b8b5fe5` | True |
| `memit_dry_run/memit/rome/__pycache__/compute_u.cpython-311.pyc` | `e70218d4d08afdabbc8d1ae688ec4024b13175bbf2d822f1f79fb7087b063035` | `e70218d4d08afdabbc8d1ae688ec4024b13175bbf2d822f1f79fb7087b063035` | True |
| `memit_dry_run/memit/rome/__pycache__/compute_v.cpython-311.pyc` | `b0da9115e983294a3b570dee6ebec70f40de5b41aa0205420857b5a8b55f90ef` | `b0da9115e983294a3b570dee6ebec70f40de5b41aa0205420857b5a8b55f90ef` | True |
| `memit_dry_run/memit/rome/__pycache__/layer_stats.cpython-311.pyc` | `440de9a4e69c8f72a3a6c32cdf88808d9ba2b3b5fb433c702d68b08af2e93e6c` | `440de9a4e69c8f72a3a6c32cdf88808d9ba2b3b5fb433c702d68b08af2e93e6c` | True |
| `memit_dry_run/memit/rome/__pycache__/repr_tools.cpython-311.pyc` | `7bc5434b08f4c6af21441c85d4715e5af2239dce3233f3f1aa7ca363068fd972` | `7bc5434b08f4c6af21441c85d4715e5af2239dce3233f3f1aa7ca363068fd972` | True |
| `memit_dry_run/memit/rome/__pycache__/rome_hparams.cpython-311.pyc` | `7f48846aa72e1a408396ba4d7f5f2c7d6f1e77ae3d96a936b47347c232e22148` | `7f48846aa72e1a408396ba4d7f5f2c7d6f1e77ae3d96a936b47347c232e22148` | True |
| `memit_dry_run/memit/rome/__pycache__/rome_main.cpython-311.pyc` | `68472f450355954b30697accbc0bd931633dc4335eea51ef5632347ab1d04e81` | `68472f450355954b30697accbc0bd931633dc4335eea51ef5632347ab1d04e81` | True |
| `memit_dry_run/memit/rome/__pycache__/tok_dataset.cpython-311.pyc` | `0131138a2f4c2e647c345a854f9aa4cd11b882b09ab9f9a92dadaca667e37a32` | `0131138a2f4c2e647c345a854f9aa4cd11b882b09ab9f9a92dadaca667e37a32` | True |
| `memit_dry_run/memit/rome/compute_u.py` | `06a73593171eecdd03ab90d45daa2c6096b4335847f0c73bda9d834cdfb1d72d` | `06a73593171eecdd03ab90d45daa2c6096b4335847f0c73bda9d834cdfb1d72d` | True |
| `memit_dry_run/memit/rome/compute_v.py` | `07f35ecec4b2a20a33318d75b040ae6c1fc5fd2122a90c92e32e361ef730d9eb` | `07f35ecec4b2a20a33318d75b040ae6c1fc5fd2122a90c92e32e361ef730d9eb` | True |
| `memit_dry_run/memit/rome/layer_stats.py` | `43693c64b061f3cdaa087447e47ddc10fb26fd597dd405eb0644d71ede2fe2d5` | `43693c64b061f3cdaa087447e47ddc10fb26fd597dd405eb0644d71ede2fe2d5` | True |
| `memit_dry_run/memit/rome/repr_tools.py` | `d4c2324ba20cbcce7f4ccfcf58ad002912edf0ad2fc72ab4e9bf46cc9dfed336` | `d4c2324ba20cbcce7f4ccfcf58ad002912edf0ad2fc72ab4e9bf46cc9dfed336` | True |
| `memit_dry_run/memit/rome/rome_hparams.py` | `1037cd56d2cfc92db212f5f4344477c5732a809dfd745c04e8e5742e925c98a5` | `1037cd56d2cfc92db212f5f4344477c5732a809dfd745c04e8e5742e925c98a5` | True |
| `memit_dry_run/memit/rome/rome_main.py` | `44ff978bd0d68839ff2f94f475a71fdac19a53a4ef263c1d74693ebfd5b40ba5` | `44ff978bd0d68839ff2f94f475a71fdac19a53a4ef263c1d74693ebfd5b40ba5` | True |
| `memit_dry_run/memit/rome/tok_dataset.py` | `37f775943d5040702ae21252db579f6aa116dacc4dd93c227c44cf9b3481a1a0` | `37f775943d5040702ae21252db579f6aa116dacc4dd93c227c44cf9b3481a1a0` | True |
| `memit_dry_run/memit/scaling_curves.sh` | `4c89f3d257f67b3e9a1ae40fe81192bfc48c0a2f40b7f2dba9adc4f2bd97efa4` | `4c89f3d257f67b3e9a1ae40fe81192bfc48c0a2f40b7f2dba9adc4f2bd97efa4` | True |
| `memit_dry_run/memit/scripts/causal_trace.sh` | `87bdd627bb58c82bf0f67841705bb95317d49f59eb1beab9d405126fd4d54600` | `87bdd627bb58c82bf0f67841705bb95317d49f59eb1beab9d405126fd4d54600` | True |
| `memit_dry_run/memit/scripts/colab_reqs/additional.txt` | `3d49f4e0bb2b079bb2fec81b178bb0a27ebc4f8085c496727e299f16aa852fb2` | `3d49f4e0bb2b079bb2fec81b178bb0a27ebc4f8085c496727e299f16aa852fb2` | True |
| `memit_dry_run/memit/scripts/colab_reqs/rome.txt` | `de3f292db754a685905c34d079d097b95e3e7de102af06aedbfba42940d29564` | `de3f292db754a685905c34d079d097b95e3e7de102af06aedbfba42940d29564` | True |
| `memit_dry_run/memit/scripts/collect_layer_stats.sh` | `ca9be52a8845851b9b17d8b92b0ac3d7333b3ea7bac339db4c1daa0deda7c60a` | `ca9be52a8845851b9b17d8b92b0ac3d7333b3ea7bac339db4c1daa0deda7c60a` | True |
| `memit_dry_run/memit/scripts/ipynb_drop_output.py` | `62a17e64c2de0448962fda6e0914a80e354361fea73b4363fc5287b92e4ca635` | `62a17e64c2de0448962fda6e0914a80e354361fea73b4363fc5287b92e4ca635` | True |
| `memit_dry_run/memit/scripts/memit.yml` | `28d8b635eed02cdb8d1fb36d8990a5347c1b88dfffcea71105febc8a91d98f83` | `28d8b635eed02cdb8d1fb36d8990a5347c1b88dfffcea71105febc8a91d98f83` | True |
| `memit_dry_run/memit/scripts/setup_clean_ipynb.sh` | `55533d28e032731eb1f0c91154ecf14092c23cf4d1f11be90a8304aa58e3338d` | `55533d28e032731eb1f0c91154ecf14092c23cf4d1f11be90a8304aa58e3338d` | True |
| `memit_dry_run/memit/scripts/setup_conda.sh` | `3d78078734cb1a45b0b448dafd5cc09b92496b89bcc8aabae057ee1fdb17e2f3` | `3d78078734cb1a45b0b448dafd5cc09b92496b89bcc8aabae057ee1fdb17e2f3` | True |
| `memit_dry_run/memit/util/__init__.py` | `0f2267e08c0c9345017c155e4d894043773f4e303958a95a3e8fe5dc3c5b341d` | `0f2267e08c0c9345017c155e4d894043773f4e303958a95a3e8fe5dc3c5b341d` | True |
| `memit_dry_run/memit/util/__pycache__/__init__.cpython-311.pyc` | `db80aa1f656186a86bae309617717d6958528f2d358abe0f656acf2c769704c2` | `db80aa1f656186a86bae309617717d6958528f2d358abe0f656acf2c769704c2` | True |
| `memit_dry_run/memit/util/__pycache__/device.cpython-311.pyc` | `b2cd7e432ddf59d90620450e3737a71784530a9f690bdca3d7156f116d603757` | `b2cd7e432ddf59d90620450e3737a71784530a9f690bdca3d7156f116d603757` | True |
| `memit_dry_run/memit/util/__pycache__/generate.cpython-311.pyc` | `fa2a8446bf235e811752c2db8c04050864747ce541485c9a52ab9d3dae043b50` | `fa2a8446bf235e811752c2db8c04050864747ce541485c9a52ab9d3dae043b50` | True |
| `memit_dry_run/memit/util/__pycache__/globals.cpython-311.pyc` | `ce42162a322e75796375c0b0ab3bb732d882cb3127e85ab0dac890588b5de55a` | `ce42162a322e75796375c0b0ab3bb732d882cb3127e85ab0dac890588b5de55a` | True |
| `memit_dry_run/memit/util/__pycache__/hparams.cpython-311.pyc` | `635c8abe561839a3fa9b91f7728d52899f7577c3a614a2a5b79a0736d6c41c73` | `635c8abe561839a3fa9b91f7728d52899f7577c3a614a2a5b79a0736d6c41c73` | True |
| `memit_dry_run/memit/util/__pycache__/logit_lens.cpython-311.pyc` | `038eea0405aab634ef32849c1c3312333297fbad3d9e25ce7d8b4960aaa0938b` | `038eea0405aab634ef32849c1c3312333297fbad3d9e25ce7d8b4960aaa0938b` | True |
| `memit_dry_run/memit/util/__pycache__/nethook.cpython-311.pyc` | `58527b861ba2cdb71ecd7de3380eea7e28f4c7dcbe5938a65ee7e5a00bc20c39` | `58527b861ba2cdb71ecd7de3380eea7e28f4c7dcbe5938a65ee7e5a00bc20c39` | True |
| `memit_dry_run/memit/util/__pycache__/runningstats.cpython-311.pyc` | `652d9894a24dbfb428ffd3de41e21b98d50d318a8581a970b100b6c81de54a0b` | `652d9894a24dbfb428ffd3de41e21b98d50d318a8581a970b100b6c81de54a0b` | True |
| `memit_dry_run/memit/util/device.py` | `868627783827f03763ba9c210de2ddbd607e050330eccf7757fccfd9e985cf2b` | `868627783827f03763ba9c210de2ddbd607e050330eccf7757fccfd9e985cf2b` | True |
| `memit_dry_run/memit/util/generate.py` | `3764cb8a0a1b3f28c17d8aab3028b33d2127ba4e02e8dbc253025791a9ab2514` | `3764cb8a0a1b3f28c17d8aab3028b33d2127ba4e02e8dbc253025791a9ab2514` | True |
| `memit_dry_run/memit/util/globals.py` | `ae25580435585acafce49511abbba6b545dbfb3f5865147d79bd383a050bf8c2` | `ae25580435585acafce49511abbba6b545dbfb3f5865147d79bd383a050bf8c2` | True |
| `memit_dry_run/memit/util/hparams.py` | `09e9fec3f476ff68009230f1251044bec21aa71797d484033f736057bbe294b0` | `09e9fec3f476ff68009230f1251044bec21aa71797d484033f736057bbe294b0` | True |
| `memit_dry_run/memit/util/logit_lens.py` | `0c35d203c511327e5c839ea0c06408f23dd6969402dce4be02f4e3160c88e6a4` | `0c35d203c511327e5c839ea0c06408f23dd6969402dce4be02f4e3160c88e6a4` | True |
| `memit_dry_run/memit/util/nethook.py` | `20e84c9413518af3aee76762071f823cbe5d75c4658e4ffa7bdab045df735f7c` | `20e84c9413518af3aee76762071f823cbe5d75c4658e4ffa7bdab045df735f7c` | True |
| `memit_dry_run/memit/util/perplexity.py` | `e0dc2678eb331aba94d70bddad30ce983b3a062c35d180d1f524835f2966161e` | `e0dc2678eb331aba94d70bddad30ce983b3a062c35d180d1f524835f2966161e` | True |
| `memit_dry_run/memit/util/runningstats.py` | `7b3a05de007733ec3243c13362d3c24b6cb9c09f32eedbcf36de02c98a49ac97` | `7b3a05de007733ec3243c13362d3c24b6cb9c09f32eedbcf36de02c98a49ac97` | True |
| `memit_dry_run/memit/zsre_evals.sh` | `a5f8ca93642cab1e18bdfc917255ea64323b2c3261d0cb4634e235bbbbf00d2f` | `a5f8ca93642cab1e18bdfc917255ea64323b2c3261d0cb4634e235bbbbf00d2f` | True |
| `tools/dashboard_experiment.py` | `59648b47a48e2f0afd8a00166d3c77199157bc78e13454eaa5bea768055cdfd7` | `3e0685b7ddf3801d6c85801bc9f4969206dcfb18787b6fc76195d98cfdd82dbc` | False |
| `tools/engine_fingerprint.py` | `450ee83ac829817299ead301c4a3d20702f431deaea4be58c77ecfd89a329162` | `450ee83ac829817299ead301c4a3d20702f431deaea4be58c77ecfd89a329162` | True |

## Telemetry volume and budget evidence

Off means no Telemetry object/directory/scorer rebind. On admission consumes inertness bytes once, strict JSON including duplicate-key/nonfinite rejection, exact namespace/source/env/INERT/count checks, then T10 requires a separate per-kind phase. First-attempt telemetry remains unset. Later stage starts reverify admission, and stage 3 matches stage 2’s setting before any launch write. Telemetry clock is isolated from stage/supervisor/memory clocks and adds no hook, graph mutation, sync, guard, ledger or scientific record key.

Per substantive write, excluding the once-per-process header and outer phase lines: `104 + int(arm==A7) + accepted_steps*(1 + int(mode==e2e))`. For stage-1 e2e/A7 this is `105+2t`: 4 writer write/merge markers, 2 readout markers, 2 lens lines, 96 answers, 1 A norm echo, then one opt_step and target_probs per accepted step. B-z has no per-step target_probs. Fixed stage forecast upper counts include checks/smoke/outer phases: stage1 phase78,opt_step100,target_probs101,write_norms4,logit_lens2,answer384; full-stage phase274,opt_step600,target_probs312,write_norms15,logit_lens5,answer1440. Counts are conservatively bounded for every triggered full-stage control. T8 per-kind timings include preparation/detach/CPU64 reduction/JSON/fsync; no kind borrows another’s time. The full payload envelope is 24 requests×6 frames×A7 target positions, five 2048×11008 layers and vocabulary151936; tiny CPU timing records do not admit live MPS telemetry.

Stage-1 C3 optimisation support cites all six accepted hooked iterations and every overflow attempt, same padded shape, with 100 accepted plus five permitted retries. The lower bound uses the slowest observed iteration times 105, not a mean. Merge uses the larger mandated merge; readout is at least max(1380, supported measured work). Measured phase mappings cannot be forged/relabelled, and calibration timing artifacts are refused for later stages. In-run projections also carry the admitted remaining phase bounds and never let pre-merge parity consume the post-merge reserve. A deadline hit, overflow limit, memory miss, drift, leakage or failed validity proof produces a diagnostic without a scientific label.

## Objections and dispatch status

1. Full verification is OPEN: native model-free blocked-child enforcement before/after write completion and two 2048×11008 CPU tests were not executed under the current process/resource restrictions. M14 must actually fail after those checks; fp32 success requires hardening its input and recording that observation. The hanging-worker requirement (prereg:96; brief §6) conflicts with the brief’s one-Python-process rule, so its explicit child-test decision is pending. No Python child was spawned here.
2. R5 and literal §7 global equality fail on the three outside-file changes above. No external attribution or baseline refresh was silently assumed.
3. Claude’s out-of-family review was unavailable on the auth probe; GPT-6-Astra/high performed the documented weaker fallback and final static C8 review.
4. Every live gate and timing/resource/MPS behavior remains UNVERIFIED. The Program must record decision0 go, spend/authorisation, current timing forecasts and actual runtime gates before dispatch; static GO and the launch examples below grant no spend.

## Program launch commands — NOT RUN

These exact absolute commands are templates for the Program after the OPEN verification/identity requirements above are closed. The Program replaces the quoted UTC/record filenames with its recorded identities, creates new files/directories only, ensures no inherited preflight knobs are present, and records the separate T8/calibration cost authorisations. No command below was executed as part of this build. All commands explicitly set LLMDB_ROOT; no directly executed shell wrapper is needed. The executable/mode test confirms the launch graph executes Python directly, with zero shell dependencies. If a .sh is added later it must be X_OK and git100755 before dispatch.

```sh
/usr/bin/env -u C10Y_SELFTEST -u C10Y_ALLOWED_CHILD_TESTS -u C10Y_TELEMETRY -u C10Y_TELEMETRY_INERTNESS LLMDB_ROOT=/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python -B /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/engine_fingerprint.py
```

Separately authorised T8, with GPU otherwise idle and its new diagnostic (P pin/audit applies):

```sh
/usr/bin/env -u C10Y_SELFTEST -u C10Y_ALLOWED_CHILD_TESTS -u C10Y_TELEMETRY -u C10Y_TELEMETRY_INERTNESS LLMDB_ROOT=/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python -B /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_telemetry_check.py --out /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/c10y_directdw_telemetry_inertness/UTC_T8 --halt-diagnostic /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/architecture_profile/c10y_halt_diagnostic_UTC_T8.json
```

Separately authorised calibration, with go/spend cap in (0,7200] and a nonempty recorded authorisation file; no own forecast, no telemetry:

```sh
/usr/bin/env -u C10Y_SELFTEST -u C10Y_ALLOWED_CHILD_TESTS -u C10Y_TELEMETRY -u C10Y_TELEMETRY_INERTNESS LLMDB_ROOT=/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python -B /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_arms.py --stage calibration --out /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/c10y_directdw_calib1 --halt-diagnostic /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/architecture_profile/c10y_halt_diagnostic_UTC_CALIB.json --go /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/architecture_profile/c10y_program_inputs/go_calibration.json --spend /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/architecture_profile/c10y_program_inputs/spend_calibration.json --authorization /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/architecture_profile/c10y_program_inputs/calibration_authorization.txt
```

The Program authors the forecast; `calibration_forecast(abs_calibration_json, bounds)` is the strict in-process builder, not a hidden model-bearing phase. Example generation below imports only the stdlib-top driver and refuses unsupported records:

```sh
/usr/bin/env -u C10Y_SELFTEST -u C10Y_ALLOWED_CHILD_TESTS -u C10Y_TELEMETRY -u C10Y_TELEMETRY_INERTNESS LLMDB_ROOT=/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python -B -c 'import sys,json;from pathlib import Path;sys.path.insert(0,'"'"'/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c'"'"');import c10y_directdw_arms as A;value=A.calibration_forecast('"'"'/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/c10y_directdw_calib1/calibration.json'"'"',A.strict_load('"'"'/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/architecture_profile/c10y_program_inputs/stage1_bounds.json'"'"'));assert value["status"]=="READY",value;A.write_json(Path('"'"'/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/architecture_profile/c10y_program_inputs/forecast_s1.json'"'"'),value)'
```

Stage-1 pre-start gate, then supervised telemetry-off first attempt:

```sh
/usr/bin/env -u C10Y_SELFTEST -u C10Y_ALLOWED_CHILD_TESTS -u C10Y_TELEMETRY -u C10Y_TELEMETRY_INERTNESS LLMDB_ROOT=/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python -B /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_arms.py --stage 1 --out /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/c10y_directdw --halt-diagnostic /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/architecture_profile/c10y_halt_diagnostic_UTC_S1.json --go /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/architecture_profile/c10y_program_inputs/go_s1.json --forecast /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/architecture_profile/c10y_program_inputs/forecast_s1.json --budget-gate
/usr/bin/env -u C10Y_SELFTEST -u C10Y_ALLOWED_CHILD_TESTS -u C10Y_TELEMETRY -u C10Y_TELEMETRY_INERTNESS LLMDB_ROOT=/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python -B /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_arms.py --stage 1 --out /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/c10y_directdw --halt-diagnostic /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/architecture_profile/c10y_halt_diagnostic_UTC_S1.json --go /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/architecture_profile/c10y_program_inputs/go_s1.json --forecast /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/architecture_profile/c10y_program_inputs/forecast_s1.json
```

Stage-1 screen reader:

```sh
/usr/bin/env -u C10Y_SELFTEST -u C10Y_ALLOWED_CHILD_TESTS -u C10Y_TELEMETRY -u C10Y_TELEMETRY_INERTNESS LLMDB_ROOT=/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python -B /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_read.py --out /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/c10y_directdw/screen.json
```

Telemetry-on variant is a fresh stage-1 replacement rerun after a compromised prior process, never an extra first attempt. The replacement file records the immutable replaced directory and cause; both T8 identity and a T10-capable forecast are mandatory:

```sh
/usr/bin/env -u C10Y_SELFTEST -u C10Y_ALLOWED_CHILD_TESTS LLMDB_ROOT=/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a C10Y_TELEMETRY=1 C10Y_TELEMETRY_INERTNESS=/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/c10y_directdw_telemetry_inertness/UTC_T8/inertness.json /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python -B /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_arms.py --stage 1 --out /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/c10y_directdw_s1_rerun1 --halt-diagnostic /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/architecture_profile/c10y_halt_diagnostic_UTC_S1_RERUN.json --go /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/architecture_profile/c10y_program_inputs/go_s1_rerun.json --forecast /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/architecture_profile/c10y_program_inputs/forecast_s1_on.json --replacement /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/architecture_profile/c10y_program_inputs/replacement_s1.json
```

Full stages below are first-attempt telemetry-off; they use the successful canonical screen and SHA of its pinned context file. Replace `CONTEXT_FILE_SHA256` with the actual file-byte SHA (it differs from the engine-form default-json digest). Stage3 is refused unless its predecessor is a stage2 survivor; no earlier tensor substitutes for regeneration:

```sh
/usr/bin/env -u C10Y_SELFTEST -u C10Y_ALLOWED_CHILD_TESTS -u C10Y_TELEMETRY -u C10Y_TELEMETRY_INERTNESS LLMDB_ROOT=/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python -B /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_arms.py --stage 2 --out /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/c10y_directdw --halt-diagnostic /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/architecture_profile/c10y_halt_diagnostic_UTC_S2.json --go /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/architecture_profile/c10y_program_inputs/go_s2.json --spend /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/architecture_profile/c10y_program_inputs/spend_s2.json --forecast /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/architecture_profile/c10y_program_inputs/forecast_s2.json --contexts /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/c10y_directdw/context_templates.json --context-sha CONTEXT_FILE_SHA256 --predecessor /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/c10y_directdw/screen.json --budget-gate
/usr/bin/env -u C10Y_SELFTEST -u C10Y_ALLOWED_CHILD_TESTS -u C10Y_TELEMETRY -u C10Y_TELEMETRY_INERTNESS LLMDB_ROOT=/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python -B /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_arms.py --stage 2 --out /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/c10y_directdw --halt-diagnostic /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/architecture_profile/c10y_halt_diagnostic_UTC_S2.json --go /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/architecture_profile/c10y_program_inputs/go_s2.json --spend /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/architecture_profile/c10y_program_inputs/spend_s2.json --forecast /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/architecture_profile/c10y_program_inputs/forecast_s2.json --contexts /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/c10y_directdw/context_templates.json --context-sha CONTEXT_FILE_SHA256 --predecessor /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/c10y_directdw/screen.json
```

```sh
/usr/bin/env -u C10Y_SELFTEST -u C10Y_ALLOWED_CHILD_TESTS -u C10Y_TELEMETRY -u C10Y_TELEMETRY_INERTNESS LLMDB_ROOT=/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python -B /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_arms.py --stage 3 --out /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/c10y_directdw --halt-diagnostic /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/architecture_profile/c10y_halt_diagnostic_UTC_S3.json --go /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/architecture_profile/c10y_program_inputs/go_s3.json --spend /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/architecture_profile/c10y_program_inputs/spend_s3.json --forecast /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/architecture_profile/c10y_program_inputs/forecast_s3.json --contexts /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/c10y_directdw/context_templates.json --context-sha CONTEXT_FILE_SHA256 --predecessor /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/c10y_directdw/pass_p1.json --budget-gate
/usr/bin/env -u C10Y_SELFTEST -u C10Y_ALLOWED_CHILD_TESTS -u C10Y_TELEMETRY -u C10Y_TELEMETRY_INERTNESS LLMDB_ROOT=/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python -B /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_arms.py --stage 3 --out /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/c10y_directdw --halt-diagnostic /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/architecture_profile/c10y_halt_diagnostic_UTC_S3.json --go /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/architecture_profile/c10y_program_inputs/go_s3.json --spend /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/architecture_profile/c10y_program_inputs/spend_s3.json --forecast /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/architecture_profile/c10y_program_inputs/forecast_s3.json --contexts /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/c10y_directdw/context_templates.json --context-sha CONTEXT_FILE_SHA256 --predecessor /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/c10y_directdw/pass_p1.json
```

Cross-process reader, and optional model-free audit after each telemetry-on stage (an audit FAIL compromises that run and requires a fresh telemetry-off rerun, never read-around):

```sh
/usr/bin/env -u C10Y_SELFTEST -u C10Y_ALLOWED_CHILD_TESTS -u C10Y_TELEMETRY -u C10Y_TELEMETRY_INERTNESS LLMDB_ROOT=/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python -B /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_read.py --out /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/c10y_directdw/pass_p1.json --process2 /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/c10y_directdw/pass_p2.json --repro /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/c10y_directdw/repro.json
/usr/bin/env -u C10Y_SELFTEST -u C10Y_ALLOWED_CHILD_TESTS -u C10Y_TELEMETRY -u C10Y_TELEMETRY_INERTNESS LLMDB_ROOT=/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python -B /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_telemetry_check.py audit --out /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/c10y_directdw_s1_rerun1 --stage 1
```

### Forecast and decision schemas the Program must author

Go fields are `decision_id`, `experiment:"C10Y"`, exact `stage` (1/2/3 or "calibration"), `recorded_in`, `at`. Spend fields are `decision_id`, exact stage and positive finite `cap_s`; calibration cap≤7200, stage1 has fixed7200, later caps come from the recorded decision. Any cap exceeding a prereg/operator bound needs the operator. Replacement fields are absolute immutable `replaces` and nonempty `cause`; `--replacement` is only for the fresh rerun directory.

```json
{
  "stage": 1,
  "status": "READY",
  "phases": [
    {
      "name": "optimisation",
      "artifact": "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/c10y_directdw_calib1/calibration.json",
      "sha256": "ACTUAL_CALIBRATION_FILE_SHA256",
      "workload": {
        "arms": [
          "A7_coined_coined"
        ],
        "requests": 24,
        "scored_prompts": 0,
        "micro_batches": 4,
        "accepted_steps": 100,
        "retries": 5,
        "padded_lengths": [
          "T_cal",
          "T_cal",
          "T_cal",
          "T_cal"
        ]
      },
      "repetitions": 6,
      "scaling_assumption": "Program justifies complete 105-attempt upper bound from all comparable observed iterations",
      "upper_s": "FINITE_NUMERIC_SECONDS",
      "measured": true,
      "timing_names": [
        "executed_loop_step",
        "smoke_step"
      ],
      "measurements": "builder copies all exact accepted/retry timing rows"
    }
  ]
}
```

This is a schema illustration, not an admissible forecast: replace the strings with real numeric bounds, hashes and complete rows. Exactly one phase for each of `preflight, load, contexts_targets, baseline, proofs, projector_capture, optimisation, merge, readout, shutdown` is required. Proofs includes the frozen smoke; projector_capture includes the candidate recipe projector/LAW5/overhead and substantive capture. Include every observed repetition and all required operations, plus a separate telemetry phase if on. `repetitions` counts the selected measurement rows (six plus actual overflow rows for optimisation); the workload separately requires 105 attempts for the future write. If a bound is independent, use `measured:false` and explicit nonempty `justification` and scaling assumption, cite its actual artifact/hash, and cover the entire requested-stage workload; that field never proves a scientific bound by itself. COMPLETE/current-identity C3 records only, stage1 only. Stage2/3 require their own supported full schedules including both modes, all arms and controls. In-run projections do not replace a pre-start bound.

Authoritative exact FORECAST_PHASES: `('preflight', 'load', 'contexts_targets', 'baseline', 'proofs', 'projector_capture', 'optimisation', 'merge', 'readout', 'shutdown')`.

T10 phase uses the admitted immutable INERT record path+SHA and `measured:true`. Its `kinds` list has exactly six rows, each with `kind`, integer `count`, finite numeric `upper_s` (per item)≥that kind’s maximum measured time, and nonempty `scaling_assumption`. The admitted record itself must supply the full payload and repetitions. The telemetry phase’s total `upper_s` covers the sum of count×per-item bounds. Counts cover the entire stage/check/readout schedule, not just one write. The strict helper/type/negative fixtures are indexed above. Missing T10 support is UNVERIFIED before any launch write.

## Review evidence and handoff

Independent static final verdict follows verbatim; it is not a live permission or substitute for the unresolved full checks:

GO

Advisor-contract verdict: PROCEED for static code readiness only. Dispatch remains GATED. No required source correction remains from this review of the exact snapshot below.

Single most important next action: once explicitly authorized and the live-job resource restriction is cleared, run the native supervisor blocked-child timeout control, including both pre-merge HALTED-BUDGET and post-marker INCOMPLETE-BUDGET, and verify termination plus context-hash diagnostics. The current timeout regression is explicitly “without_child” (transport_launch_delta_green_1.log:15); static inspection of arms.py:1477–1520 cannot establish native termination behavior.

Scope and independence

This is the requested GPT-6-Astra/high independent implementation review under prereg §10 C8 (docs/C10Y_DIRECTDW_PREREG.md:889–899), using the advisor/objective contract reproduced verbatim below. It is the weaker GPT-family fallback for Codex-authored work allowed by .codex/skills/advisor-review/SKILL.md, not cross-family confirmation. Claude authentication unavailability is parent-reported and not independently re-probed in this no-dispatch review. No Python, tests, test or model subprocesses, tokenizer, GPU or MPS were launched by this reviewer; only static reads and this scratch report were performed.

Exact final snapshot (independently rehashed after the final repair)

- docs/C10Y_DIRECTDW_PREREG.md: e069b358c362b2a05e3b668e8a29f33061e15a24306e321452e6fa46a4e83331
- experiments/track_c/c10y_directdw_arms.py: 206710d02c6cc8580a14391cc94c5280db63bc1a9de0177bb3b6a15951c29416
- experiments/track_c/c10y_directdw_read.py: f8d2598b01956be3ad390c76b2336ae1398e77d05045fb8870a3ae6e42cb2e78
- experiments/track_c/c10y_directdw_selftest.py: 02977e73ea0a6d70b642112d025a2e274060d3334a339baad149a799916db3c1
- experiments/track_c/c10y_directdw_telemetry_check.py: e79f0532ac674a0cb8a3d21c838c15710ee0ed3e94f7fa88e65d722105c1c03f

Required issues, in priority order

1. Empirical and authorization gates remain OPEN. Native child supervision/M14, full-size reductions and live LAW#3/LAW#5, model behavior, memory/resource compliance, timing forecasts and T8 inertness remain UNVERIFIED by this review. The final whole light-suite rerun was still pending when the final snapshot was supplied; this report does not certify a full final-byte suite PASS. The model-bearing route remains MEASUREMENT-ONLY. A static GO does not authorize dispatch or satisfy its recorded go/spending/forecast requirements (prereg:91–98, :889–899).

2. Protected-file attribution remains OPEN. The parent reports external changes to docs/C10Z_ASTRA_PREREG.md, experiments/track_c/c10z_astra_arms.py and dashboard_experiment.py awaiting Program confirmation. Their cause/authorization is independently UNVERIFIED here; this review neither attributes those changes to C10Y nor waives R5. The observed live heartbeat/log drift in transport_launch_delta_green_1.log:23 is separately recorded, with owned drift [] and forbidden imports [] at :22/:24.

3. The last confirmed code blocker is now resolved. On the prior arms 2b68aa74… / reader c6b01b60… snapshot, only the test helper had received the inclusive one-percent boundary fix; the actual scientific hook and reader still used subtraction. The final producer now calls control_match at arms.py:2034, the shared interval is at :414, and the reader uses the same interval at read.py:667. size_scales (:406) and scientific totals (:2032) now use math.fsum, matching the reader's :594 reduction. Actual-path regressions are at selftest.py:4001–4041 and cover 0.99/1.01 plus just-outside values.
   Evidence: /private/tmp/c10y_build/nm_actual_paths_red.log records 2 tests / 4 failures; the initial reader fixture also had an inconsistent expected scale, so those reader failures alone do not isolate the boundary defect. nm_sum_red_boundary_green.log records both actual boundary paths GREEN after correcting that fixture and separately exposes the real producer/reader sum mismatch (0.8333333333333334 versus 0.8333333333333333). nm_actual_paths_green_final.log records all 6 targeted tests OK in 0.429 s, owned drift [] and forbidden imports []. I inspected the final production paths and tests, not just the helper or test summary.

Previous delta dispositions

- Requested-stage forecast checks exist in parent and worker (arms.py:1545/:1378), later-stage calibration reuse is refused (:849), and T9 pairing is checked before parent launch (:1542).
- H_out binds the serialized targets_<tag>.pt bundle SHA and explicit actual_updates member, with a separate tensor-certificate digest (arms.py:1454–1455; read.py:537–539).
- Timeout/calibration diagnostics carry observed or explicitly expected template hash evidence (arms.py:908–911, :1505, :1518). T8 installs and audits the pinned templates before batches/forwards (:1107–1110), without redraw. Pin shape, both digests, cache installation and stage-source equality remain explicit (:881–905), matching Amendment P (:910–972).
- Norm calculation, cleanup, ledger return and handoff are inside writer wall-clock accounting (arms.py:435–448, :605–618). Telemetry attribute presence, including an existing None, is restored at both nesting levels (:1388/:1444 and :2403/:2636).

The recorded transport regression is 16 tests, 8 failures then 16 OK (/private/tmp/c10y_build/transport_launch_delta_red.log and transport_launch_delta_green_1.log:1–24). The three-stage transport uses actual driver persistence/reader/PT plumbing with synthetic scientific data; it is not scientific/MPS validation (selftest.py TransportTests). Mutation evidence is bounded: mutations_light_driver_2.log records 20 assertion kills and M13 surviving, then mutation_m13_hardened.log records M13 killed after strengthening its assertion; both record source restoration True. M14 is absent/deferred. These earlier runs are not represented as exhaustive tests of the later final-byte snapshot.

Real criterion, confounds and F1 drift

The accepted claim is limited to source-level implementation of the frozen C10Y controls plus the cited CPU plumbing evidence. Neither mocked scientific readouts nor a declared MPS identity establish live scientific equivalence, resource safety, learned factual performance or F1 closure. The real native-timeout control above is the cheapest remaining test that can overturn this limited readiness finding. This work supports the preregistered falsifier by preventing invalid launches and misleading size-control classifications; it creates no scientific evidence or relaxed F1 claim (prereg:80–81, :91–99, :255–256).

The earlier alleged missing timing “repetition” fields remains WITHDRAWN; the producer supplied them. It is not an outstanding finding.

Verbatim advisor/objective contract follows.

# Advisor / objective-review prompt (reusable — Claude & Codex)

You are an **independent, adversarial reviewer** of a research step in the LLM-as-Database program. You are not the author. **Do not rubber-stamp.** Your job is to find where the work is wrong, over-claimed, confounded, or drifting from the goal — *before* it is leaned on.

You will be given ONE of: a **test/experiment design** (before it runs), a **finding/result** (before it is declared conclusive or written to CORPUS), or an **approach** the author is about to commit to — together with its evidence (artifact paths + numbers) and the relevant context.

Run this review and answer concisely and specifically:

1. **Real criterion.** Does this answer the question's *actual* criterion, or a flattering adjacent one? (e.g. is the metric matched to the claim — top-1 for read-correctness, distributional for distributional; is the gate's true requirement being met or a softer proxy?)
2. **Confounds & over-claims.** Hunt for confounds, leakage, Goodhart, and over-statement. Is `EVIDENCE-SHOWS` blurred with `I-INFER`? Is "the mechanism works" being passed off as "the contract is met" (**mechanics ≠ contract**)? Is design-viability being passed off as empirical evidence?
3. **Cite or flag.** Every factual claim must cite an artifact (path + exact number) or be labeled **`UNVERIFIABLE`**. Call out any claim that isn't grounded. Verify that external repos/IDs/claims were actually checked before being relied on.
4. **The overturning test.** What is the *cheapest* experiment or control that could **falsify** this finding/design? If it hasn't been run, that is the gap.
5. **Drift check.** Does this advance the F1 readiness determination (or a live §0.3 falsifier)? If not, say so.

**Output:** a short verdict — `PROCEED` / `FIX-FIRST` / `OVERTURNED-OR-RECONSIDER` — then the **single most important thing** to do next, then the specific issues in priority order. Be a skeptic; the author will weigh your input heavily but evidence remains binding over your opinion.

Session handoff is confined to this report and `/private/tmp/c10y_build`: source/fixture fixes complete, final static GO, 225/226 light cases passing with the preserved R5 failure, 21 executed mutation kills/source restoration, three pending tests and M14 unrun, no scientific or dispatch result. The project context-save/memory/ledger instructions were not allowed to create extra W artifacts beyond R2. This report and the scratch evidence are the scoped closeout.

