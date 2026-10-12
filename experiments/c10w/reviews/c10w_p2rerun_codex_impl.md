# D-C10w-p2rerun — implementation and verification

Implementation is ready for program review. The final CPU-only selftest is **PASS: 108 tests, 107 passed, 1 skipped**, with the real-artifact guard PASS. All 79 original test names remain; 78 ran successfully and the existing real-tokenizer smoke was intentionally skipped under the brief's no-tokenizer rule. The 29 added tests passed. **The GPU re-evaluation, live gate, live amendment preparation and live archive were not run. Scientific execution and conclusions remain UNRUN/UNVERIFIED.**

Model/effort: Codex, described by the system as GPT-6. The exact runtime model identifier and configured reasoning-effort value are not exposed to this session and are **UNVERIFIABLE**; no more specific identifier or effort level is asserted. Worktree: `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a`; branch `worktree-c10k-route-a`. No commits were made.

## Final behavior and source boundaries

The evaluator change consists exclusively of the two `.double()` additions after the existing fp32 matrix multiplication and flatten, at `experiments/track_c/c10w_oracle_eval.py:436–437`. Dot and norms consequently accumulate in float64 on the already merged CPU deltas. No other evaluator byte changed relative to the saved pre-build source. The full-size CPU regression observed old fp32 cosine **1.0069566194439687**, corrected cosine **0.9999999999994128**, device `cpu`, shape `[2048, 11008]`, dtype `torch.float32`; the corrected value passes the original reader's validity check and the 1e-9 regression bound. This establishes the numerical fix on CPU, not a new model measurement.

The frozen reader and step0 dispatcher source are themselves SHA-bound by step0. Editing either would violate the requirement that every other frozen source retain its original hash. They therefore remain byte-identical. `tools/c10w_p2_rerun.py:81` installs a scoped runtime `load_frozen` overlay: the old evaluator still follows the unmodified verifier; the new evaluator is accepted only through the separately pinned A1 record and exact evaluator/diff/step0 identities. Every other source and frozen file is still checked by the original verifier. The override is restored in `finally`, including after refusal. The program must use the sealed helper/coordinator commands below; the ordinary standalone frozen reader still correctly refuses a changed evaluator without the overlay.

`prepare` creates only `step0_20261007T223638_531381Z/amendment_A1_evaluator.json`, using exclusive creation and canonical, pinned JSON bytes. Expected A1 SHA-256: `4791183ab5ddc68cbecff1653a1f80508fb4806d5e957fde63a25a498037d17f`. It records decision D-C10w-p2rerun, old/new evaluator hashes, unified-diff path/hash, diagnostic path, reason, original step0 hash and the single bound P2 directory. Repeated preparation verifies the existing record without replacing it. No live amendment was created by this build.

`archive` validates the complete six-file original bundle against independently captured SHA-256 pins before moving anything. The exact four inner files are `HALT.json`, `eval.json`, `eval_halt.json`, `p2-eval.log`; the outer files are `p2-eval.log` and its original `p2-eval.gate.20261007T222229.91288.json`. Missing files, unexpected eval/verdict files, different original bytes, symlinks and partial archives refuse before moves. The manifest records source, destination, size, SHA, reason, A1 reference and the failed eval's actual wall seconds. Repeated archive calls verify the completed manifest and change nothing, even after new active eval files exist. Train records, adapters, preflight and the six training logs are never moved. A filesystem error halfway through moves leaves a refused partial archive for the program to inspect; the tool does not silently roll it forward or overwrite it.

The retry admission requires the bound latest step0/P1/P2 directories, verified A1 and archive, no active P2 HALT, and all six original outer training logs ending exactly `STAGE_EXIT=0`. The stage gate still executes the original fingerprint, GPU inventory, frozen-source, authorization, training/preflight and projection checks; its GPU exemption tuple is unchanged. The projection also charges the archived failed eval's **6209.1800138338 s** against the unchanged **448-minute** P2 authorization. Boundary tests pass at 448 and refuse an additional second. No authorization file or budget was changed.

After admission, exclusive `reattempt2.json` reserves the one attempt. Exclusive `reattempt2_dispatch_entered.json` refuses duplicate dispatch outside the frozen dispatcher's HALT-writing exception handler. The original dispatcher performs its guards before writing the exclusive `reattempt2_dispatch.json` child-launch receipt. Child entry verifies receipt hash, exact phase/directory/step0 arguments, claim, amendment, parent PID and exclusive inner log, then exclusively creates `reattempt2_eval_started.json` **before evaluator/model entry**. A concurrent or repeated entry cannot reach the backend. A failed admitted attempt stays consumed; nothing is deleted to permit another attempt.

The coordinator verifies the retry prerequisites, skips the six completed training stages, runs only P2 eval, then the original scientific reader through the overlay. Fresh timestamp/PID coordinator invocation logs allow a transient pre-gate refusal to be retried without consuming the scientific claim. Outer eval logs and readings use exclusive creation. `eval.json`, `verdict.json`, the reading, and other JSON records written through the retry overlay carry `evaluator_amendment: {path, sha256}`. Archive and claim records also retain that reference; gate evidence contains it in the retry proof. Label, fit, LAW#3, LAW#5 and routing checks are not relaxed.

## Stop-and-fix incident and exact tests

The initial legacy baseline was unsafe despite reporting 79 tests OK. **`OracleTests.test_pure_P1_reprojection_and_real_launcher_refusal`** (original selftest lines 677–689; current entry at line 683) invoked the actual `tools/run_c10w_stage.sh` while `ROOT` referenced the live worktree. Newly available P2 authorization allowed its P2 training dispatch to create a fresh phase/preflight before the environment refused MPS. This baseline is not accepted as safe CPU-only verification. I stopped running it and corrected isolation before the next selftest.

That dispatch created the three files originally under `results/c10w_oracle/p2_20261008T075056_661871Z/` and `architecture_profile/c10w_oracle_halt_diagnostic_20261008T075101_137852Z.json`. The program quarantined them under `results/c10w_oracle/_quarantine_selftest_leak_20261008/`; I did not move, delete or rewrite them. The incident artifact hashes are included below. The MPS-required HALT is evidence of the refused environment, not a successful training run.

**`DupDevTests.test_real_cached_acquisition_and_tokenizer_exercise_every_require`** also loaded the cached real tokenizer during that initial baseline. It is now opt-in and skipped by the default isolated, no-tokenizer suite. The isolated root has no live HF cache link. I do not claim that smoke was freshly validated under the CPU-only hard rules, or that all 79 legacy cases executed successfully in the final run.

The selftest main now copies all runtime sources, launcher/gate scripts, prereg and screen fixtures into `/private/tmp/c10w_selftest_*`, imports R/S/T/E from those copies, binds `LLMDB_ROOT` and function defaults there, and creates temporary results/profile trees. It links only the existing interpreter environment, not live results, adapters, model or dataset caches. Copies of P2 shell scripts explicitly bind their temporary root. The legacy launcher-refusal test also forces an inherited forbidden model knob and asserts that refusal, so it cannot advance to a model load or training dispatch.

The live snapshot runs before setup and again in `finally`, including when a test or setup fails. It tracks creation, deletion, replacement, rename and metadata/content-write changes without following symlinks. As explicitly directed by the program's later note, **only the `results/labviz/` directory subtree is excluded** because the program's Node/Playwright browser review writes there concurrently. All other `results/` paths and every `architecture_profile/` path remain guarded. Earlier snapshots did fail on concurrent C10Z report/Lab View writes; those logs are not called final GREEN, and a snapshot alone cannot attribute a write to this selftest.

Exact isolation/guard cases:

- `IsolationTests.test_every_runtime_module_and_default_root_is_temporary`: verifies copied module paths, temporary defaults and absent live cache/results links.
- `IsolationTests.test_artifact_guard_detects_create_change_delete_and_rename`: positive controls for changes in both guarded artifact trees.
- `IsolationTests.test_selftest_does_not_change_live_artifact_trees`: compares the real before/after snapshots; main repeats the comparison in `finally`.
- `IsolationTests.test_artifact_guard_excludes_only_operator_labviz_subtree`: Lab View fixture writes are ignored while leaks into both other artifact trees are detected.

The P2 rerun cases include the full-size production cosine, original/amended frozen loader and verifier restoration, exact/pinned/idempotent archive, all missing/tampered prerequisites, gate refusal without claim consumption, unchanged budget boundary, once-only stage/child entry and permanent failed-attempt consumption, coordinator training skips/refusal-resume, newer-directory refusal, and A1 propagation into records/readings. In particular:

- `P2RerunTests.test_public_eval_requires_dispatch_and_consumes_entry_once` and `test_public_eval_cli_race_starts_backend_once` reject direct entry, wrong parent, concurrency and replay before the backend.
- `P2RerunTests.test_public_dispatch_cli_race_and_replay_never_halt_winner` checks two public dispatch processes plus replay: one backend start, losing refusal, no HALT/diagnostic or successful-output changes.
- `P2RerunTests.test_production_dispatch_eval_and_read_with_cpu_backend` exercises the production helper, original dispatcher, child entry, exclusive writers, linked disk reader and final read; only heavy backend/transport and environment, preflight-certificate and git-tracking boundaries are stubbed. It also checks harmless dispatch replay.
- `P2RerunTests.test_real_eval_writer_and_verdict_reading_carry_amendment` executes the existing evaluator with its model-free P1 fake backend and checks actual writer/read metadata. P2 scoring itself remains unrun.

## Verification and independent review

Test-first evidence is included verbatim in the appendices, with complete selftest counts:

- Initial isolated RED, before evaluator/helper implementation: **96 tests, failures=28, skipped=1**; old production cosine fails; absent helper fails; live guard PASS.
- Runner/gate RED, before those changes: **101 tests, failures=4, skipped=1**; live guard PASS.
- Adversarial retry/archive RED: **106 tests, failures=6, skipped=1**; replay/concurrency, archive identity/verdict and coordinator resume defects reproduced; live guard PASS. One integrated fixture additionally exposed a Path/string transport issue in the new shim; the integrated fixture's later training-provenance mismatch was corrected in the fixture, without changing the evaluator.
- Public-dispatch replay RED: **2 selected tests, failures=2**; the racing loser HALTed the winner; live guard PASS.
- Authorized Lab View exclusion RED: **1 selected test, failure=1** before the exclusion was implemented; live guard PASS.
- Final full suite: **108 tests in 10.581 s, OK (skipped=1)**; guard PASS with the explicit Lab View exclusion. The final command was `.venv/bin/python -B experiments/track_c/c10w_oracle_selftest.py`, with output redirected only under `/private/tmp`.

`bash -n tools/run_c10w_p2_stage.sh tools/run_c10w_p2.sh` passed. AST/source checks confirmed the exact two-cast evaluator delta and unchanged GPU exemption tuple. The before/after SHA snapshot of **46 protected existing files** matches: original step0 directory files, prereg, frozen step0/trainer sources, original P2 records/adapters/preflight and protected stage artifacts. Separate read-only hashing also verifies every original non-evaluator source reference (including the frozen reader) against unchanged step0 and the original P2 authorization against its reference in the protected preflight record. This is a bounded protected-file claim, not a global clean-tree claim; other authorized sessions have their own changes in this shared worktree.

A fresh subagent performed read-only adversarial implementation review and returned **PROCEED, no remaining implementation blocker** after the retry-entry, dispatch-replay, coordinator-resume and archive findings were corrected. It independently inspected the final 108-test output and exact guard exclusion. This is a **same-family fallback** with weaker independence, not an out-of-family scientific review. The prescribed Claude advisor could not be used: `/Users/robertrhu/.local/bin/claude auth status` returned exit 1, `loggedIn: false`, `authMethod: none` on the latest read-only probe. No Claude result or external review completion is fabricated. The program's review and actual run remain its next steps.

No live A1, archive directory, retry reservation or eval-start marker exists as a result of this implementation. After the unsafe initial legacy baseline, all operational-path tests ran only against temporary copies/fixtures. No engine, prereg, original step0, training record, adapter, CORPUS or ledger edit was made; no c10z_* or tools/labviz source was edited by this build.

## Exact program-session commands, in order

Run these from the program session after its build review, in its normal GPU-capable environment. The incident files have already been quarantined by that session. The helper deliberately refuses if a different newer phase appears; do not weaken that selection or remove consumption markers. `prepare` and `archive` below are the authorized real-tree operations that this build did not execute.

```bash
cd /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a
export LLMDB_ROOT="$PWD"
C10W_P2_REATTEMPT_DIR="$LLMDB_ROOT/results/c10w_oracle/p2_20261008T034226_086980Z"
set -e

# Creates the one separately pinned amendment; no frozen record is rewritten.
.venv/bin/python -B tools/c10w_p2_rerun.py prepare

# Moves only the original halted eval artifacts and writes/verifies the manifest.
.venv/bin/python -B tools/c10w_p2_rerun.py archive

# Read-only archive/amendment/training-log/selection/no-HALT/no-prior-retry checks.
.venv/bin/python -B tools/c10w_p2_rerun.py verify

# Same inherited-knob clearing already performed by the original stage wrapper.
unset C10_KEY_LOCUS C10_CTX_TEMPLATES C10_ARMS N_EDIT C10_SUBJECT_OFFSET HP_CANDIDATE C10_PROJECTOR C10_RECIPES MODEL_ID MODEL_REV LLMDB_DEVICE

# Read-only complete existing fingerprint/GPU/authorization/projection gate.
.venv/bin/python -B tools/c10w_p2_gate.py p2-eval --reattempt "$C10W_P2_REATTEMPT_DIR"

# One coordinator, no training re-run; the stage wrapper repeats the complete gate.
C10W_REATTEMPT_LAUNCH_LOG="$LLMDB_ROOT/results/c10w_oracle_logs/p2-reattempt-launch.$(date '+%Y%m%dT%H%M%S').$$.log"
(set -C; nohup /bin/bash tools/run_c10w_p2.sh --reattempt-eval "$C10W_P2_REATTEMPT_DIR" > "$C10W_REATTEMPT_LAUNCH_LOG" 2>&1 < /dev/null &)
```

The coordinator records the six `SKIP` lines and runs only `p2-eval`. Its new invocation log is `results/c10w_oracle_logs/p2-reattempt-coordinator.<timestamp>.<pid>.log`. Expected outputs, if admitted and completed, are the active P2 `eval.json`, `verdict.json`, inner/outer `p2-eval.log`, the retry/dispatch/start receipts, and `results/c10w_oracle_logs/p2-read-attempt2.json`. A nonzero admitted child consumes the sole attempt and remains a HALT; no further reattempt is authorized by this tool. A pre-gate refusal consumes no claim and permits another coordinator invocation after the blocker clears.

## Open issues and limits

- **UNRUN/UNVERIFIED:** actual GPU re-evaluation, same-seed model behavior, scientific LAW#3/LAW#5, live inventory/fingerprint/projection admission, measured runtime, budget completion and final scientific reading. Fixture PASS and static review cannot establish these.
- **Legacy tokenizer smoke:** 79 tests retained, but the real cached-tokenizer case is intentionally skipped. The brief's literal all-79-executed-green condition is not claimed; executing that smoke here would breach the simultaneous no-tokenizer hard rule. The complete cached tokenizer/data smoke is outside this build's authorized validation.
- **Independent review:** Claude authentication was unavailable on the probed CLI; same-family fallback PROCEED covers implementation only. Program review remains required by the brief's handoff, not granted by this report.
- **Original unsafe baseline:** four leaked artifacts and a real tokenizer load occurred before correction. They are disclosed above; the baseline's OK line is excluded from safe verification evidence. The program owns quarantine, and the subsequent final guard passes under the expressly authorized Lab View exclusion.
- The sealed helper is bound to this original worktree/step0/P1/P2 and exact reviewed source/artifact hashes. Another evaluator change, source drift, newer phase, partial archive, or failed consumed retry is refused and requires a separate program decision.

## Changed/new implementation files and SHA-256

The following table is generated from the final on-disk bytes. The report itself is the additional named output; its own hash is emitted by the final read-back verification outside its body, avoiding a self-referential hash. Scratch logs and their hashes are embedded below; no extra permanent report or checksum file was created.

| File | SHA-256 | Purpose |
|---|---|---|
| `experiments/track_c/c10w_oracle_eval.py` | `45f2839d0fd576bd131072c0ae8b009a0cb371ddca49b1edadb062944a775f1e` | The sole evaluator fix: two CPU float64 casts before cosine dot/norms. |
| `experiments/track_c/c10w_oracle_selftest.py` | `9d9319e35315e4f9168fb920429598d46707c697589b10a8371d023281731e36` | Temporary-root isolation, protected-tree snapshots, 29 new CPU/fixture regressions and explicit tokenizer skip. |
| `tools/c10w_p2_gate.py` | `fb6568a6e159e84b22971aa893c3a83bcaaa16085f4abd9c76ca50b4a3362a26` | Keep the original gate checks and GPU exemptions; add sealed P2 retry admission through the A1 overlay. |
| `tools/c10w_p2_rerun.py` | `67d48282810314892dbf4c6de24e79a91c773bb1e507e5b16cc63178077c6ebe` | Pinned A1 preparation/verifier overlay, exact historical archive, one claim/dispatch/child start, provenance and reader entry. |
| `tools/c10w_p2_evaluator_A1.diff` | `ca0e00df578f535bff2b5c8a878dfc9138b88e4c7c357e156a65b177a2fe06ff` | Canonical unified diff of exactly the permitted evaluator casts, pinned by A1. |
| `tools/run_c10w_p2_stage.sh` | `cc15a516b01d6a4c7334d56b5dffc3498652457e463bee99187a2b0c484a4944` | Explicit retry flag, unchanged full gate, exclusive claim/log and bound eval dispatch. |
| `tools/run_c10w_p2.sh` | `29743d62d0e781d5fe15938f88396d617faeb26ecc58a2a76c5b92cdeeb78874` | Resume eval only, skip six training logs, preserve coordinator invocation logs and write the amended reading. |

### Existing frozen identities verified unchanged

| File | SHA-256 |
|---|---|
| `docs/C10W_ORACLE_PREREG.md` | `d2aa240eede4556395373678e4fab757e0e55d5491a7d4105ef765c1eb35d2f0` |
| `experiments/track_c/c10w_oracle_read.py` | `162966119cf49967f39c402c73e63ebc9c673401c74f335154696eb5ab859b0b` |
| `experiments/track_c/c10w_oracle_step0.py` | `c0ec236cad0d2f824616f8d5e9e29244f9604168dd5555540f2867ba1f333834` |
| `experiments/track_c/c10w_oracle_train.py` | `64a01fbcbbd8e836f67e623bc50f66ecff8dd59a29d7c82db3bba287d76ea463` |
| `results/c10w_oracle/step0_20261007T223638_531381Z/step0.json` | `82ef86437b5ba00fa78a1b55cfe64e4d85baaceb37aa0726f3015c2b2f7d673e` |
| `results/c10w_oracle/p1_20261007T223707_598959Z/authorization_P2.json` | `1a35ace1e18e544a30aebbe5ac1074526b41abb5073fdecbd13b3ae1409fce43` |

### Incident artifacts created by the initial unsafe baseline

These are read-only hashes at the program-owned quarantine destinations; each maps to the original live path described above. The program quarantine README and Lab View copies are not artifacts created by this implementation.

| Current quarantine artifact | SHA-256 | Purpose / incident role |
|---|---|---|
| `results/c10w_oracle/_quarantine_selftest_leak_20261008/c10w_oracle_halt_diagnostic_20261008T075101_137852Z.json` | `b3af96deb8eda65aa60dd1dd7a63275c782e577f7b88b3d87e0c4e035103c1ff` | Unintended original architecture_profile stage diagnostic. |
| `results/c10w_oracle/_quarantine_selftest_leak_20261008/p2_20261008T075056_661871Z/HALT.json` | `b3af96deb8eda65aa60dd1dd7a63275c782e577f7b88b3d87e0c4e035103c1ff` | Unintended stage HALT record. |
| `results/c10w_oracle/_quarantine_selftest_leak_20261008/p2_20261008T075056_661871Z/p2-a7-s1.log` | `d6f619bd94138484f8e27886efdd0fb889ed532f8ae123eca99aedde0a9da808` | Unintended training-stage log; MPS-required refusal. |
| `results/c10w_oracle/_quarantine_selftest_leak_20261008/p2_20261008T075056_661871Z/preflight.json` | `12b0c539786dada7a46665cc351ad79a8746f0f8073665243ed1e6eefbb8f3a3` | Unintended copied P2 preflight from the real launcher-refusal test. |

## Verbatim test-output appendices

These logs are embedded in full so the report remains usable after the scratch directory is removed. Log hashes below refer to the original raw UTF-8 bytes. The first three full RED runs used the same `.venv/bin/python -B experiments/track_c/c10w_oracle_selftest.py` command with their then-current test/implementation source state. The two small RED runs selected their named cases through the same isolated `main()` using a unittest loader patch; they did not import or run live R/S/T/E. All final sources are hashed above.

### RED before evaluator/helper implementation

Raw log: `/private/tmp/c10w_p2rerun_ly_5udgv/red.log`; SHA-256 `86fb4c892cd178d02d51ede53576a1a282ed8e05d689e472882c78a8b6f3eced`.

<details>
<summary>Complete raw test output</summary>

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
test_real_cached_acquisition_and_tokenizer_exercise_every_require (__main__.DupDevTests.test_real_cached_acquisition_and_tokenizer_exercise_every_require) ... skipped 'tokenizer loading requires explicit C10W_SELFTEST_ALLOW_TOKENIZER=1'
test_report_only_198_sensitivity_keeps_full_200_gate_and_label (__main__.DupDevTests.test_report_only_198_sensitivity_keeps_full_200_gate_and_label) ... ok
test_six_dev_rows_refused_as_invalid_instrument (__main__.DupDevTests.test_six_dev_rows_refused_as_invalid_instrument) ... ok
test_whole_dev_summary_includes_exactly_low_distinct_subjects (__main__.DupDevTests.test_whole_dev_summary_includes_exactly_low_distinct_subjects) ... ok
test_zero_to_three_dev_rows_refused_as_invalid_instrument (__main__.DupDevTests.test_zero_to_three_dev_rows_refused_as_invalid_instrument) ... ok
test_amended_evaluator_requires_valid_pinned_amendment (__main__.P2RerunTests.test_amended_evaluator_requires_valid_pinned_amendment) ... FAIL
test_amendment_diff_and_evaluator_tampering_fail_closed (__main__.P2RerunTests.test_amendment_diff_and_evaluator_tampering_fail_closed) ... 
  test_amendment_diff_and_evaluator_tampering_fail_closed (__main__.P2RerunTests.test_amendment_diff_and_evaluator_tampering_fail_closed) (which='amendment') ... FAIL
  test_amendment_diff_and_evaluator_tampering_fail_closed (__main__.P2RerunTests.test_amendment_diff_and_evaluator_tampering_fail_closed) (which='diff') ... FAIL
  test_amendment_diff_and_evaluator_tampering_fail_closed (__main__.P2RerunTests.test_amendment_diff_and_evaluator_tampering_fail_closed) (which='evaluator') ... FAIL
test_archive_idempotent_even_after_new_eval_files_exist (__main__.P2RerunTests.test_archive_idempotent_even_after_new_eval_files_exist) ... FAIL
test_archive_manifest_and_archived_file_tampering_refused (__main__.P2RerunTests.test_archive_manifest_and_archived_file_tampering_refused) ... 
  test_archive_manifest_and_archived_file_tampering_refused (__main__.P2RerunTests.test_archive_manifest_and_archived_file_tampering_refused) (defect='manifest') ... FAIL
  test_archive_manifest_and_archived_file_tampering_refused (__main__.P2RerunTests.test_archive_manifest_and_archived_file_tampering_refused) (defect='archived') ... FAIL
test_archive_moves_exact_set_hashes_and_preserves_training (__main__.P2RerunTests.test_archive_moves_exact_set_hashes_and_preserves_training) ... FAIL
test_archive_refuses_missing_unexpected_symlink_and_partial_without_moves (__main__.P2RerunTests.test_archive_refuses_missing_unexpected_symlink_and_partial_without_moves) ... 
  test_archive_refuses_missing_unexpected_symlink_and_partial_without_moves (__main__.P2RerunTests.test_archive_refuses_missing_unexpected_symlink_and_partial_without_moves) (defect='missing') ... FAIL
  test_archive_refuses_missing_unexpected_symlink_and_partial_without_moves (__main__.P2RerunTests.test_archive_refuses_missing_unexpected_symlink_and_partial_without_moves) (defect='unexpected') ... FAIL
  test_archive_refuses_missing_unexpected_symlink_and_partial_without_moves (__main__.P2RerunTests.test_archive_refuses_missing_unexpected_symlink_and_partial_without_moves) (defect='symlink') ... FAIL
  test_archive_refuses_missing_unexpected_symlink_and_partial_without_moves (__main__.P2RerunTests.test_archive_refuses_missing_unexpected_symlink_and_partial_without_moves) (defect='partial') ... FAIL
test_every_other_frozen_source_remains_strict_and_verifier_restored (__main__.P2RerunTests.test_every_other_frozen_source_remains_strict_and_verifier_restored) ... 
  test_every_other_frozen_source_remains_strict_and_verifier_restored (__main__.P2RerunTests.test_every_other_frozen_source_remains_strict_and_verifier_restored) (which='reader') ... FAIL
  test_every_other_frozen_source_remains_strict_and_verifier_restored (__main__.P2RerunTests.test_every_other_frozen_source_remains_strict_and_verifier_restored) (which='trainer') ... FAIL
  test_every_other_frozen_source_remains_strict_and_verifier_restored (__main__.P2RerunTests.test_every_other_frozen_source_remains_strict_and_verifier_restored) (which='step0_source') ... FAIL
  test_every_other_frozen_source_remains_strict_and_verifier_restored (__main__.P2RerunTests.test_every_other_frozen_source_remains_strict_and_verifier_restored) (which='harness') ... FAIL
test_gate_failure_never_consumes_reattempt (__main__.P2RerunTests.test_gate_failure_never_consumes_reattempt) ... FAIL
test_identical_full_size_fp32_delta_uses_production_float64_cosine (__main__.P2RerunTests.test_identical_full_size_fp32_delta_uses_production_float64_cosine) ... C10W_COSINE_CPU {"old": 1.0069566194439687, "new": 1.0069566194439687, "device": "cpu", "shape": [2048, 11008], "dtype": "torch.float32"}
FAIL
test_newer_eval_directory_cannot_enter_reading (__main__.P2RerunTests.test_newer_eval_directory_cannot_enter_reading) ... FAIL
test_original_evaluator_passes_without_amendment (__main__.P2RerunTests.test_original_evaluator_passes_without_amendment) ... FAIL
test_real_eval_writer_and_verdict_reading_carry_amendment (__main__.P2RerunTests.test_real_eval_writer_and_verdict_reading_carry_amendment) ... FAIL
test_reattempt_admitted_once_and_claim_kept (__main__.P2RerunTests.test_reattempt_admitted_once_and_claim_kept) ... FAIL
test_reattempt_refuses_each_missing_or_changed_prerequisite (__main__.P2RerunTests.test_reattempt_refuses_each_missing_or_changed_prerequisite) ... 
  test_reattempt_refuses_each_missing_or_changed_prerequisite (__main__.P2RerunTests.test_reattempt_refuses_each_missing_or_changed_prerequisite) (defect='manifest') ... FAIL
  test_reattempt_refuses_each_missing_or_changed_prerequisite (__main__.P2RerunTests.test_reattempt_refuses_each_missing_or_changed_prerequisite) (defect='halt') ... FAIL
  test_reattempt_refuses_each_missing_or_changed_prerequisite (__main__.P2RerunTests.test_reattempt_refuses_each_missing_or_changed_prerequisite) (defect='training') ... FAIL
  test_reattempt_refuses_each_missing_or_changed_prerequisite (__main__.P2RerunTests.test_reattempt_refuses_each_missing_or_changed_prerequisite) (defect='amendment') ... FAIL
  test_reattempt_refuses_each_missing_or_changed_prerequisite (__main__.P2RerunTests.test_reattempt_refuses_each_missing_or_changed_prerequisite) (defect='wrong_directory') ... FAIL
  test_reattempt_refuses_each_missing_or_changed_prerequisite (__main__.P2RerunTests.test_reattempt_refuses_each_missing_or_changed_prerequisite) (defect='newer_directory') ... FAIL
test_artifact_guard_detects_create_change_delete_and_rename (__main__.IsolationTests.test_artifact_guard_detects_create_change_delete_and_rename) ... ok
test_every_runtime_module_and_default_root_is_temporary (__main__.IsolationTests.test_every_runtime_module_and_default_root_is_temporary) ... ok
test_selftest_does_not_change_live_artifact_trees (__main__.IsolationTests.test_selftest_does_not_change_live_artifact_trees) ... ok

======================================================================
FAIL: test_amended_evaluator_requires_valid_pinned_amendment (__main__.P2RerunTests.test_amended_evaluator_requires_valid_pinned_amendment)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1747, in test_amended_evaluator_requires_valid_pinned_amendment
    with self.tree(amended=False) as (A,root,step0,p2,logs,evaluator,new):
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/contextlib.py", line 137, in __enter__
    return next(self.gen)
           ^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1643, in tree
    A=self.module()
      ^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1638, in module
    self.assertTrue((ROOT/"tools/c10w_p2_rerun.py").is_file(),"sealed P2 rerun implementation absent (test-first RED)")
AssertionError: False is not true : sealed P2 rerun implementation absent (test-first RED)

======================================================================
FAIL: test_amendment_diff_and_evaluator_tampering_fail_closed (__main__.P2RerunTests.test_amendment_diff_and_evaluator_tampering_fail_closed) (which='amendment')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1757, in test_amendment_diff_and_evaluator_tampering_fail_closed
    with self.subTest(which=which),self.tree() as (A,root,step0,p2,logs,evaluator,new):
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/contextlib.py", line 137, in __enter__
    return next(self.gen)
           ^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1643, in tree
    A=self.module()
      ^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1638, in module
    self.assertTrue((ROOT/"tools/c10w_p2_rerun.py").is_file(),"sealed P2 rerun implementation absent (test-first RED)")
AssertionError: False is not true : sealed P2 rerun implementation absent (test-first RED)

======================================================================
FAIL: test_amendment_diff_and_evaluator_tampering_fail_closed (__main__.P2RerunTests.test_amendment_diff_and_evaluator_tampering_fail_closed) (which='diff')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1757, in test_amendment_diff_and_evaluator_tampering_fail_closed
    with self.subTest(which=which),self.tree() as (A,root,step0,p2,logs,evaluator,new):
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/contextlib.py", line 137, in __enter__
    return next(self.gen)
           ^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1643, in tree
    A=self.module()
      ^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1638, in module
    self.assertTrue((ROOT/"tools/c10w_p2_rerun.py").is_file(),"sealed P2 rerun implementation absent (test-first RED)")
AssertionError: False is not true : sealed P2 rerun implementation absent (test-first RED)

======================================================================
FAIL: test_amendment_diff_and_evaluator_tampering_fail_closed (__main__.P2RerunTests.test_amendment_diff_and_evaluator_tampering_fail_closed) (which='evaluator')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1757, in test_amendment_diff_and_evaluator_tampering_fail_closed
    with self.subTest(which=which),self.tree() as (A,root,step0,p2,logs,evaluator,new):
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/contextlib.py", line 137, in __enter__
    return next(self.gen)
           ^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1643, in tree
    A=self.module()
      ^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1638, in module
    self.assertTrue((ROOT/"tools/c10w_p2_rerun.py").is_file(),"sealed P2 rerun implementation absent (test-first RED)")
AssertionError: False is not true : sealed P2 rerun implementation absent (test-first RED)

======================================================================
FAIL: test_archive_idempotent_even_after_new_eval_files_exist (__main__.P2RerunTests.test_archive_idempotent_even_after_new_eval_files_exist)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1799, in test_archive_idempotent_even_after_new_eval_files_exist
    with self.tree(archived=True) as (A,root,step0,p2,logs,evaluator,new):
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/contextlib.py", line 137, in __enter__
    return next(self.gen)
           ^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1643, in tree
    A=self.module()
      ^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1638, in module
    self.assertTrue((ROOT/"tools/c10w_p2_rerun.py").is_file(),"sealed P2 rerun implementation absent (test-first RED)")
AssertionError: False is not true : sealed P2 rerun implementation absent (test-first RED)

======================================================================
FAIL: test_archive_manifest_and_archived_file_tampering_refused (__main__.P2RerunTests.test_archive_manifest_and_archived_file_tampering_refused) (defect='manifest')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1809, in test_archive_manifest_and_archived_file_tampering_refused
    with self.subTest(defect=defect),self.tree(archived=True) as (A,root,step0,p2,logs,evaluator,new):
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/contextlib.py", line 137, in __enter__
    return next(self.gen)
           ^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1643, in tree
    A=self.module()
      ^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1638, in module
    self.assertTrue((ROOT/"tools/c10w_p2_rerun.py").is_file(),"sealed P2 rerun implementation absent (test-first RED)")
AssertionError: False is not true : sealed P2 rerun implementation absent (test-first RED)

======================================================================
FAIL: test_archive_manifest_and_archived_file_tampering_refused (__main__.P2RerunTests.test_archive_manifest_and_archived_file_tampering_refused) (defect='archived')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1809, in test_archive_manifest_and_archived_file_tampering_refused
    with self.subTest(defect=defect),self.tree(archived=True) as (A,root,step0,p2,logs,evaluator,new):
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/contextlib.py", line 137, in __enter__
    return next(self.gen)
           ^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1643, in tree
    A=self.module()
      ^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1638, in module
    self.assertTrue((ROOT/"tools/c10w_p2_rerun.py").is_file(),"sealed P2 rerun implementation absent (test-first RED)")
AssertionError: False is not true : sealed P2 rerun implementation absent (test-first RED)

======================================================================
FAIL: test_archive_moves_exact_set_hashes_and_preserves_training (__main__.P2RerunTests.test_archive_moves_exact_set_hashes_and_preserves_training)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1772, in test_archive_moves_exact_set_hashes_and_preserves_training
    with self.tree() as (A,root,step0,p2,logs,evaluator,new):
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/contextlib.py", line 137, in __enter__
    return next(self.gen)
           ^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1643, in tree
    A=self.module()
      ^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1638, in module
    self.assertTrue((ROOT/"tools/c10w_p2_rerun.py").is_file(),"sealed P2 rerun implementation absent (test-first RED)")
AssertionError: False is not true : sealed P2 rerun implementation absent (test-first RED)

======================================================================
FAIL: test_archive_refuses_missing_unexpected_symlink_and_partial_without_moves (__main__.P2RerunTests.test_archive_refuses_missing_unexpected_symlink_and_partial_without_moves) (defect='missing')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1788, in test_archive_refuses_missing_unexpected_symlink_and_partial_without_moves
    with self.subTest(defect=defect),self.tree() as (A,root,step0,p2,logs,evaluator,new):
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/contextlib.py", line 137, in __enter__
    return next(self.gen)
           ^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1643, in tree
    A=self.module()
      ^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1638, in module
    self.assertTrue((ROOT/"tools/c10w_p2_rerun.py").is_file(),"sealed P2 rerun implementation absent (test-first RED)")
AssertionError: False is not true : sealed P2 rerun implementation absent (test-first RED)

======================================================================
FAIL: test_archive_refuses_missing_unexpected_symlink_and_partial_without_moves (__main__.P2RerunTests.test_archive_refuses_missing_unexpected_symlink_and_partial_without_moves) (defect='unexpected')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1788, in test_archive_refuses_missing_unexpected_symlink_and_partial_without_moves
    with self.subTest(defect=defect),self.tree() as (A,root,step0,p2,logs,evaluator,new):
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/contextlib.py", line 137, in __enter__
    return next(self.gen)
           ^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1643, in tree
    A=self.module()
      ^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1638, in module
    self.assertTrue((ROOT/"tools/c10w_p2_rerun.py").is_file(),"sealed P2 rerun implementation absent (test-first RED)")
AssertionError: False is not true : sealed P2 rerun implementation absent (test-first RED)

======================================================================
FAIL: test_archive_refuses_missing_unexpected_symlink_and_partial_without_moves (__main__.P2RerunTests.test_archive_refuses_missing_unexpected_symlink_and_partial_without_moves) (defect='symlink')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1788, in test_archive_refuses_missing_unexpected_symlink_and_partial_without_moves
    with self.subTest(defect=defect),self.tree() as (A,root,step0,p2,logs,evaluator,new):
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/contextlib.py", line 137, in __enter__
    return next(self.gen)
           ^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1643, in tree
    A=self.module()
      ^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1638, in module
    self.assertTrue((ROOT/"tools/c10w_p2_rerun.py").is_file(),"sealed P2 rerun implementation absent (test-first RED)")
AssertionError: False is not true : sealed P2 rerun implementation absent (test-first RED)

======================================================================
FAIL: test_archive_refuses_missing_unexpected_symlink_and_partial_without_moves (__main__.P2RerunTests.test_archive_refuses_missing_unexpected_symlink_and_partial_without_moves) (defect='partial')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1788, in test_archive_refuses_missing_unexpected_symlink_and_partial_without_moves
    with self.subTest(defect=defect),self.tree() as (A,root,step0,p2,logs,evaluator,new):
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/contextlib.py", line 137, in __enter__
    return next(self.gen)
           ^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1643, in tree
    A=self.module()
      ^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1638, in module
    self.assertTrue((ROOT/"tools/c10w_p2_rerun.py").is_file(),"sealed P2 rerun implementation absent (test-first RED)")
AssertionError: False is not true : sealed P2 rerun implementation absent (test-first RED)

======================================================================
FAIL: test_every_other_frozen_source_remains_strict_and_verifier_restored (__main__.P2RerunTests.test_every_other_frozen_source_remains_strict_and_verifier_restored) (which='reader')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1764, in test_every_other_frozen_source_remains_strict_and_verifier_restored
    with self.subTest(which=which),self.tree() as (A,root,step0,p2,logs,evaluator,new):
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/contextlib.py", line 137, in __enter__
    return next(self.gen)
           ^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1643, in tree
    A=self.module()
      ^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1638, in module
    self.assertTrue((ROOT/"tools/c10w_p2_rerun.py").is_file(),"sealed P2 rerun implementation absent (test-first RED)")
AssertionError: False is not true : sealed P2 rerun implementation absent (test-first RED)

======================================================================
FAIL: test_every_other_frozen_source_remains_strict_and_verifier_restored (__main__.P2RerunTests.test_every_other_frozen_source_remains_strict_and_verifier_restored) (which='trainer')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1764, in test_every_other_frozen_source_remains_strict_and_verifier_restored
    with self.subTest(which=which),self.tree() as (A,root,step0,p2,logs,evaluator,new):
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/contextlib.py", line 137, in __enter__
    return next(self.gen)
           ^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1643, in tree
    A=self.module()
      ^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1638, in module
    self.assertTrue((ROOT/"tools/c10w_p2_rerun.py").is_file(),"sealed P2 rerun implementation absent (test-first RED)")
AssertionError: False is not true : sealed P2 rerun implementation absent (test-first RED)

======================================================================
FAIL: test_every_other_frozen_source_remains_strict_and_verifier_restored (__main__.P2RerunTests.test_every_other_frozen_source_remains_strict_and_verifier_restored) (which='step0_source')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1764, in test_every_other_frozen_source_remains_strict_and_verifier_restored
    with self.subTest(which=which),self.tree() as (A,root,step0,p2,logs,evaluator,new):
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/contextlib.py", line 137, in __enter__
    return next(self.gen)
           ^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1643, in tree
    A=self.module()
      ^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1638, in module
    self.assertTrue((ROOT/"tools/c10w_p2_rerun.py").is_file(),"sealed P2 rerun implementation absent (test-first RED)")
AssertionError: False is not true : sealed P2 rerun implementation absent (test-first RED)

======================================================================
FAIL: test_every_other_frozen_source_remains_strict_and_verifier_restored (__main__.P2RerunTests.test_every_other_frozen_source_remains_strict_and_verifier_restored) (which='harness')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1764, in test_every_other_frozen_source_remains_strict_and_verifier_restored
    with self.subTest(which=which),self.tree() as (A,root,step0,p2,logs,evaluator,new):
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/contextlib.py", line 137, in __enter__
    return next(self.gen)
           ^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1643, in tree
    A=self.module()
      ^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1638, in module
    self.assertTrue((ROOT/"tools/c10w_p2_rerun.py").is_file(),"sealed P2 rerun implementation absent (test-first RED)")
AssertionError: False is not true : sealed P2 rerun implementation absent (test-first RED)

======================================================================
FAIL: test_gate_failure_never_consumes_reattempt (__main__.P2RerunTests.test_gate_failure_never_consumes_reattempt)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1838, in test_gate_failure_never_consumes_reattempt
    with self.tree(archived=True) as (A,root,step0,p2,logs,evaluator,new):
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/contextlib.py", line 137, in __enter__
    return next(self.gen)
           ^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1643, in tree
    A=self.module()
      ^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1638, in module
    self.assertTrue((ROOT/"tools/c10w_p2_rerun.py").is_file(),"sealed P2 rerun implementation absent (test-first RED)")
AssertionError: False is not true : sealed P2 rerun implementation absent (test-first RED)

======================================================================
FAIL: test_identical_full_size_fp32_delta_uses_production_float64_cosine (__main__.P2RerunTests.test_identical_full_size_fp32_delta_uses_production_float64_cosine)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1738, in test_identical_full_size_fp32_delta_uses_production_float64_cosine
    self.assertLessEqual(abs(result["new"]-1.),1e-9)
AssertionError: 0.006956619443968748 not less than or equal to 1e-09

======================================================================
FAIL: test_newer_eval_directory_cannot_enter_reading (__main__.P2RerunTests.test_newer_eval_directory_cannot_enter_reading)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1845, in test_newer_eval_directory_cannot_enter_reading
    with self.tree(archived=True) as (A,root,step0,p2,logs,evaluator,new):
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/contextlib.py", line 137, in __enter__
    return next(self.gen)
           ^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1643, in tree
    A=self.module()
      ^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1638, in module
    self.assertTrue((ROOT/"tools/c10w_p2_rerun.py").is_file(),"sealed P2 rerun implementation absent (test-first RED)")
AssertionError: False is not true : sealed P2 rerun implementation absent (test-first RED)

======================================================================
FAIL: test_original_evaluator_passes_without_amendment (__main__.P2RerunTests.test_original_evaluator_passes_without_amendment)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1743, in test_original_evaluator_passes_without_amendment
    with self.tree(amended=False) as (A,root,step0,p2,logs,evaluator,new):
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/contextlib.py", line 137, in __enter__
    return next(self.gen)
           ^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1643, in tree
    A=self.module()
      ^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1638, in module
    self.assertTrue((ROOT/"tools/c10w_p2_rerun.py").is_file(),"sealed P2 rerun implementation absent (test-first RED)")
AssertionError: False is not true : sealed P2 rerun implementation absent (test-first RED)

======================================================================
FAIL: test_real_eval_writer_and_verdict_reading_carry_amendment (__main__.P2RerunTests.test_real_eval_writer_and_verdict_reading_carry_amendment)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1850, in test_real_eval_writer_and_verdict_reading_carry_amendment
    with self.tree(archived=True) as (A,root,step0,p2,logs,evaluator,new):
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/contextlib.py", line 137, in __enter__
    return next(self.gen)
           ^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1643, in tree
    A=self.module()
      ^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1638, in module
    self.assertTrue((ROOT/"tools/c10w_p2_rerun.py").is_file(),"sealed P2 rerun implementation absent (test-first RED)")
AssertionError: False is not true : sealed P2 rerun implementation absent (test-first RED)

======================================================================
FAIL: test_reattempt_admitted_once_and_claim_kept (__main__.P2RerunTests.test_reattempt_admitted_once_and_claim_kept)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1816, in test_reattempt_admitted_once_and_claim_kept
    with self.tree(archived=True) as (A,root,step0,p2,logs,evaluator,new):
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/contextlib.py", line 137, in __enter__
    return next(self.gen)
           ^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1643, in tree
    A=self.module()
      ^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1638, in module
    self.assertTrue((ROOT/"tools/c10w_p2_rerun.py").is_file(),"sealed P2 rerun implementation absent (test-first RED)")
AssertionError: False is not true : sealed P2 rerun implementation absent (test-first RED)

======================================================================
FAIL: test_reattempt_refuses_each_missing_or_changed_prerequisite (__main__.P2RerunTests.test_reattempt_refuses_each_missing_or_changed_prerequisite) (defect='manifest')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1825, in test_reattempt_refuses_each_missing_or_changed_prerequisite
    with self.subTest(defect=defect),self.tree(archived=True) as (A,root,step0,p2,logs,evaluator,new):
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/contextlib.py", line 137, in __enter__
    return next(self.gen)
           ^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1643, in tree
    A=self.module()
      ^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1638, in module
    self.assertTrue((ROOT/"tools/c10w_p2_rerun.py").is_file(),"sealed P2 rerun implementation absent (test-first RED)")
AssertionError: False is not true : sealed P2 rerun implementation absent (test-first RED)

======================================================================
FAIL: test_reattempt_refuses_each_missing_or_changed_prerequisite (__main__.P2RerunTests.test_reattempt_refuses_each_missing_or_changed_prerequisite) (defect='halt')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1825, in test_reattempt_refuses_each_missing_or_changed_prerequisite
    with self.subTest(defect=defect),self.tree(archived=True) as (A,root,step0,p2,logs,evaluator,new):
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/contextlib.py", line 137, in __enter__
    return next(self.gen)
           ^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1643, in tree
    A=self.module()
      ^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1638, in module
    self.assertTrue((ROOT/"tools/c10w_p2_rerun.py").is_file(),"sealed P2 rerun implementation absent (test-first RED)")
AssertionError: False is not true : sealed P2 rerun implementation absent (test-first RED)

======================================================================
FAIL: test_reattempt_refuses_each_missing_or_changed_prerequisite (__main__.P2RerunTests.test_reattempt_refuses_each_missing_or_changed_prerequisite) (defect='training')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1825, in test_reattempt_refuses_each_missing_or_changed_prerequisite
    with self.subTest(defect=defect),self.tree(archived=True) as (A,root,step0,p2,logs,evaluator,new):
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/contextlib.py", line 137, in __enter__
    return next(self.gen)
           ^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1643, in tree
    A=self.module()
      ^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1638, in module
    self.assertTrue((ROOT/"tools/c10w_p2_rerun.py").is_file(),"sealed P2 rerun implementation absent (test-first RED)")
AssertionError: False is not true : sealed P2 rerun implementation absent (test-first RED)

======================================================================
FAIL: test_reattempt_refuses_each_missing_or_changed_prerequisite (__main__.P2RerunTests.test_reattempt_refuses_each_missing_or_changed_prerequisite) (defect='amendment')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1825, in test_reattempt_refuses_each_missing_or_changed_prerequisite
    with self.subTest(defect=defect),self.tree(archived=True) as (A,root,step0,p2,logs,evaluator,new):
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/contextlib.py", line 137, in __enter__
    return next(self.gen)
           ^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1643, in tree
    A=self.module()
      ^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1638, in module
    self.assertTrue((ROOT/"tools/c10w_p2_rerun.py").is_file(),"sealed P2 rerun implementation absent (test-first RED)")
AssertionError: False is not true : sealed P2 rerun implementation absent (test-first RED)

======================================================================
FAIL: test_reattempt_refuses_each_missing_or_changed_prerequisite (__main__.P2RerunTests.test_reattempt_refuses_each_missing_or_changed_prerequisite) (defect='wrong_directory')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1825, in test_reattempt_refuses_each_missing_or_changed_prerequisite
    with self.subTest(defect=defect),self.tree(archived=True) as (A,root,step0,p2,logs,evaluator,new):
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/contextlib.py", line 137, in __enter__
    return next(self.gen)
           ^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1643, in tree
    A=self.module()
      ^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1638, in module
    self.assertTrue((ROOT/"tools/c10w_p2_rerun.py").is_file(),"sealed P2 rerun implementation absent (test-first RED)")
AssertionError: False is not true : sealed P2 rerun implementation absent (test-first RED)

======================================================================
FAIL: test_reattempt_refuses_each_missing_or_changed_prerequisite (__main__.P2RerunTests.test_reattempt_refuses_each_missing_or_changed_prerequisite) (defect='newer_directory')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1825, in test_reattempt_refuses_each_missing_or_changed_prerequisite
    with self.subTest(defect=defect),self.tree(archived=True) as (A,root,step0,p2,logs,evaluator,new):
  File "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/lib/python3.11/contextlib.py", line 137, in __enter__
    return next(self.gen)
           ^^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1643, in tree
    A=self.module()
      ^^^^^^^^^^^^^
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1638, in module
    self.assertTrue((ROOT/"tools/c10w_p2_rerun.py").is_file(),"sealed P2 rerun implementation absent (test-first RED)")
AssertionError: False is not true : sealed P2 rerun implementation absent (test-first RED)

----------------------------------------------------------------------
Ran 96 tests in 8.251s

FAILED (failures=28, skipped=1)
C10W_SELFTEST_LIVE_ARTIFACT_GUARD PASS: results/ and architecture_profile/ unchanged
```

</details>

### RED before stage/gate/coordinator implementation

Raw log: `/private/tmp/c10w_p2rerun_ly_5udgv/red_runners.log`; SHA-256 `fd622db736c99950759729c12e39622ce823687e67bca749be3a97b399d841be`.

<details>
<summary>Complete raw test output</summary>

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
test_real_cached_acquisition_and_tokenizer_exercise_every_require (__main__.DupDevTests.test_real_cached_acquisition_and_tokenizer_exercise_every_require) ... skipped 'tokenizer loading requires explicit C10W_SELFTEST_ALLOW_TOKENIZER=1'
test_report_only_198_sensitivity_keeps_full_200_gate_and_label (__main__.DupDevTests.test_report_only_198_sensitivity_keeps_full_200_gate_and_label) ... ok
test_six_dev_rows_refused_as_invalid_instrument (__main__.DupDevTests.test_six_dev_rows_refused_as_invalid_instrument) ... ok
test_whole_dev_summary_includes_exactly_low_distinct_subjects (__main__.DupDevTests.test_whole_dev_summary_includes_exactly_low_distinct_subjects) ... ok
test_zero_to_three_dev_rows_refused_as_invalid_instrument (__main__.DupDevTests.test_zero_to_three_dev_rows_refused_as_invalid_instrument) ... ok
test_amended_evaluator_requires_valid_pinned_amendment (__main__.P2RerunTests.test_amended_evaluator_requires_valid_pinned_amendment) ... ok
test_amendment_diff_and_evaluator_tampering_fail_closed (__main__.P2RerunTests.test_amendment_diff_and_evaluator_tampering_fail_closed) ... ok
test_archive_idempotent_even_after_new_eval_files_exist (__main__.P2RerunTests.test_archive_idempotent_even_after_new_eval_files_exist) ... ok
test_archive_manifest_and_archived_file_tampering_refused (__main__.P2RerunTests.test_archive_manifest_and_archived_file_tampering_refused) ... ok
test_archive_moves_exact_set_hashes_and_preserves_training (__main__.P2RerunTests.test_archive_moves_exact_set_hashes_and_preserves_training) ... ok
test_archive_refuses_missing_unexpected_symlink_and_partial_without_moves (__main__.P2RerunTests.test_archive_refuses_missing_unexpected_symlink_and_partial_without_moves) ... ok
test_coordinator_skips_six_trainings_then_eval_and_amended_reader (__main__.P2RerunTests.test_coordinator_skips_six_trainings_then_eval_and_amended_reader) ... FAIL
test_every_other_frozen_source_remains_strict_and_verifier_restored (__main__.P2RerunTests.test_every_other_frozen_source_remains_strict_and_verifier_restored) ... ok
test_failed_child_consumes_retry_permanently (__main__.P2RerunTests.test_failed_child_consumes_retry_permanently) ... FAIL
test_gate_failure_never_consumes_reattempt (__main__.P2RerunTests.test_gate_failure_never_consumes_reattempt) ... ok
test_gate_retains_original_guards_and_adds_retry_admission (__main__.P2RerunTests.test_gate_retains_original_guards_and_adds_retry_admission) ... FAIL
test_identical_full_size_fp32_delta_uses_production_float64_cosine (__main__.P2RerunTests.test_identical_full_size_fp32_delta_uses_production_float64_cosine) ... C10W_COSINE_CPU {"old": 1.0069566194439687, "new": 0.9999999999994128, "device": "cpu", "shape": [2048, 11008], "dtype": "torch.float32"}
ok
test_newer_eval_directory_cannot_enter_reading (__main__.P2RerunTests.test_newer_eval_directory_cannot_enter_reading) ... ok
test_original_evaluator_passes_without_amendment (__main__.P2RerunTests.test_original_evaluator_passes_without_amendment) ... ok
test_real_eval_writer_and_verdict_reading_carry_amendment (__main__.P2RerunTests.test_real_eval_writer_and_verdict_reading_carry_amendment) ... ok
test_reattempt_admitted_once_and_claim_kept (__main__.P2RerunTests.test_reattempt_admitted_once_and_claim_kept) ... ok
test_reattempt_refuses_each_missing_or_changed_prerequisite (__main__.P2RerunTests.test_reattempt_refuses_each_missing_or_changed_prerequisite) ... ok
test_retry_projection_charges_halted_eval_at_unchanged_boundary (__main__.P2RerunTests.test_retry_projection_charges_halted_eval_at_unchanged_boundary) ... ok
test_stage_runner_race_starts_exactly_one_eval_and_never_truncates_log (__main__.P2RerunTests.test_stage_runner_race_starts_exactly_one_eval_and_never_truncates_log) ... FAIL
test_artifact_guard_detects_create_change_delete_and_rename (__main__.IsolationTests.test_artifact_guard_detects_create_change_delete_and_rename) ... ok
test_every_runtime_module_and_default_root_is_temporary (__main__.IsolationTests.test_every_runtime_module_and_default_root_is_temporary) ... ok
test_selftest_does_not_change_live_artifact_trees (__main__.IsolationTests.test_selftest_does_not_change_live_artifact_trees) ... ok

======================================================================
FAIL: test_coordinator_skips_six_trainings_then_eval_and_amended_reader (__main__.P2RerunTests.test_coordinator_skips_six_trainings_then_eval_and_amended_reader)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1963, in test_coordinator_skips_six_trainings_then_eval_and_amended_reader
    self.assertEqual(proc.returncode,0,proc.stdout+proc.stderr)
AssertionError: 4 != 0 : /private/tmp/tmp8aoids46/tools/run_c10w_p2.sh: line 19: /bin/ps: Operation not permitted
grep: /private/tmp/tmp8aoids46/results/c10w_oracle/p2_20261008T034226_086980Z: Is a directory


======================================================================
FAIL: test_failed_child_consumes_retry_permanently (__main__.P2RerunTests.test_failed_child_consumes_retry_permanently)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1952, in test_failed_child_consumes_retry_permanently
    self.assertEqual(proc.returncode,2,proc.stdout+proc.stderr)
AssertionError: 99 != 2 : 

======================================================================
FAIL: test_gate_retains_original_guards_and_adds_retry_admission (__main__.P2RerunTests.test_gate_retains_original_guards_and_adds_retry_admission)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1881, in test_gate_retains_original_guards_and_adds_retry_admission
    self.assertIn("reattempt_directory",inspect.signature(G.check_dispatch_guards).parameters,
AssertionError: 'reattempt_directory' not found in mappingproxy(OrderedDict([('stage', <Parameter "stage">)])) : gate has no sealed retry path (test-first RED)

======================================================================
FAIL: test_stage_runner_race_starts_exactly_one_eval_and_never_truncates_log (__main__.P2RerunTests.test_stage_runner_race_starts_exactly_one_eval_and_never_truncates_log)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1939, in test_stage_runner_race_starts_exactly_one_eval_and_never_truncates_log
    self.assertEqual(sum(p.returncode==0 for p in processes),1,outputs)
AssertionError: 0 != 1 : [('', ''), ('', '')]

----------------------------------------------------------------------
Ran 101 tests in 9.650s

FAILED (failures=4, skipped=1)
C10W_SELFTEST_LIVE_ARTIFACT_GUARD PASS: results/ and architecture_profile/ unchanged
```

</details>

### RED of independent-review retry/archive findings

Raw log: `/private/tmp/c10w_p2rerun_ly_5udgv/red_review.log`; SHA-256 `0a4975b32cb3131cc7bca7a18faa7b17c8b7af7b10d518bbcf074ceeb48e56d5`.

<details>
<summary>Complete raw test output</summary>

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
test_real_cached_acquisition_and_tokenizer_exercise_every_require (__main__.DupDevTests.test_real_cached_acquisition_and_tokenizer_exercise_every_require) ... skipped 'tokenizer loading requires explicit C10W_SELFTEST_ALLOW_TOKENIZER=1'
test_report_only_198_sensitivity_keeps_full_200_gate_and_label (__main__.DupDevTests.test_report_only_198_sensitivity_keeps_full_200_gate_and_label) ... ok
test_six_dev_rows_refused_as_invalid_instrument (__main__.DupDevTests.test_six_dev_rows_refused_as_invalid_instrument) ... ok
test_whole_dev_summary_includes_exactly_low_distinct_subjects (__main__.DupDevTests.test_whole_dev_summary_includes_exactly_low_distinct_subjects) ... ok
test_zero_to_three_dev_rows_refused_as_invalid_instrument (__main__.DupDevTests.test_zero_to_three_dev_rows_refused_as_invalid_instrument) ... ok
test_amended_evaluator_requires_valid_pinned_amendment (__main__.P2RerunTests.test_amended_evaluator_requires_valid_pinned_amendment) ... ok
test_amendment_diff_and_evaluator_tampering_fail_closed (__main__.P2RerunTests.test_amendment_diff_and_evaluator_tampering_fail_closed) ... ok
test_archive_idempotent_even_after_new_eval_files_exist (__main__.P2RerunTests.test_archive_idempotent_even_after_new_eval_files_exist) ... ok
test_archive_is_bound_to_reviewed_original_bytes (__main__.P2RerunTests.test_archive_is_bound_to_reviewed_original_bytes) ... FAIL
test_archive_manifest_and_archived_file_tampering_refused (__main__.P2RerunTests.test_archive_manifest_and_archived_file_tampering_refused) ... ok
test_archive_moves_exact_set_hashes_and_preserves_training (__main__.P2RerunTests.test_archive_moves_exact_set_hashes_and_preserves_training) ... ok
test_archive_refuses_missing_unexpected_symlink_and_partial_without_moves (__main__.P2RerunTests.test_archive_refuses_missing_unexpected_symlink_and_partial_without_moves) ... 
  test_archive_refuses_missing_unexpected_symlink_and_partial_without_moves (__main__.P2RerunTests.test_archive_refuses_missing_unexpected_symlink_and_partial_without_moves) (defect='verdict') ... FAIL
test_coordinator_gate_refusal_then_resume_consumes_one_retry (__main__.P2RerunTests.test_coordinator_gate_refusal_then_resume_consumes_one_retry) ... FAIL
test_coordinator_skips_six_trainings_then_eval_and_amended_reader (__main__.P2RerunTests.test_coordinator_skips_six_trainings_then_eval_and_amended_reader) ... ok
test_every_other_frozen_source_remains_strict_and_verifier_restored (__main__.P2RerunTests.test_every_other_frozen_source_remains_strict_and_verifier_restored) ... ok
test_failed_child_consumes_retry_permanently (__main__.P2RerunTests.test_failed_child_consumes_retry_permanently) ... ok
test_gate_failure_never_consumes_reattempt (__main__.P2RerunTests.test_gate_failure_never_consumes_reattempt) ... ok
test_gate_retains_original_guards_and_adds_retry_admission (__main__.P2RerunTests.test_gate_retains_original_guards_and_adds_retry_admission) ... ok
test_identical_full_size_fp32_delta_uses_production_float64_cosine (__main__.P2RerunTests.test_identical_full_size_fp32_delta_uses_production_float64_cosine) ... C10W_COSINE_CPU {"old": 1.0069566194439687, "new": 0.9999999999994128, "device": "cpu", "shape": [2048, 11008], "dtype": "torch.float32"}
ok
test_newer_eval_directory_cannot_enter_reading (__main__.P2RerunTests.test_newer_eval_directory_cannot_enter_reading) ... ok
test_original_evaluator_passes_without_amendment (__main__.P2RerunTests.test_original_evaluator_passes_without_amendment) ... ok
test_production_dispatch_eval_and_read_with_cpu_backend (__main__.P2RerunTests.test_production_dispatch_eval_and_read_with_cpu_backend) ... HALT: 'PosixPath' object is not subscriptable
FAIL
test_public_eval_cli_race_starts_backend_once (__main__.P2RerunTests.test_public_eval_cli_race_starts_backend_once) ... FAIL
test_public_eval_requires_dispatch_and_consumes_entry_once (__main__.P2RerunTests.test_public_eval_requires_dispatch_and_consumes_entry_once) ... FAIL
test_real_eval_writer_and_verdict_reading_carry_amendment (__main__.P2RerunTests.test_real_eval_writer_and_verdict_reading_carry_amendment) ... ok
test_reattempt_admitted_once_and_claim_kept (__main__.P2RerunTests.test_reattempt_admitted_once_and_claim_kept) ... ok
test_reattempt_refuses_each_missing_or_changed_prerequisite (__main__.P2RerunTests.test_reattempt_refuses_each_missing_or_changed_prerequisite) ... ok
test_retry_projection_charges_halted_eval_at_unchanged_boundary (__main__.P2RerunTests.test_retry_projection_charges_halted_eval_at_unchanged_boundary) ... ok
test_stage_runner_race_starts_exactly_one_eval_and_never_truncates_log (__main__.P2RerunTests.test_stage_runner_race_starts_exactly_one_eval_and_never_truncates_log) ... ok
test_artifact_guard_detects_create_change_delete_and_rename (__main__.IsolationTests.test_artifact_guard_detects_create_change_delete_and_rename) ... ok
test_every_runtime_module_and_default_root_is_temporary (__main__.IsolationTests.test_every_runtime_module_and_default_root_is_temporary) ... ok
test_selftest_does_not_change_live_artifact_trees (__main__.IsolationTests.test_selftest_does_not_change_live_artifact_trees) ... ok

======================================================================
FAIL: test_archive_is_bound_to_reviewed_original_bytes (__main__.P2RerunTests.test_archive_is_bound_to_reviewed_original_bytes)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1823, in test_archive_is_bound_to_reviewed_original_bytes
    with self.assertRaises(R.Halt): A.archive()
AssertionError: Halt not raised

======================================================================
FAIL: test_archive_refuses_missing_unexpected_symlink_and_partial_without_moves (__main__.P2RerunTests.test_archive_refuses_missing_unexpected_symlink_and_partial_without_moves) (defect='verdict')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1799, in test_archive_refuses_missing_unexpected_symlink_and_partial_without_moves
    with self.assertRaises(R.Halt): A.archive()
AssertionError: Halt not raised

======================================================================
FAIL: test_coordinator_gate_refusal_then_resume_consumes_one_retry (__main__.P2RerunTests.test_coordinator_gate_refusal_then_resume_consumes_one_retry)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 2103, in test_coordinator_gate_refusal_then_resume_consumes_one_retry
    self.assertEqual(second.returncode,0,second.stdout+second.stderr)
AssertionError: 2 != 0 : {
  "archive_manifest": {
    "path": "/private/tmp/tmpqokq99qq/results/c10w_oracle/p2_20261008T034226_086980Z/attempt1_halted/manifest.json",
    "sha256": "cbae92b4cea53af63b1075dcdd2d699f6fcc32f84567fe27341f03ef4f2a8904"
  },
  "evaluator_amendment": {
    "path": "/private/tmp/tmpqokq99qq/results/c10w_oracle/step0_20261007T223638_531381Z/amendment_A1_evaluator.json",
    "sha256": "6df9e24d2f4e3b93a576e1a10d052dd11972729342291d71972ebd916f21cd1d"
  },
  "training_logs": [
    {
      "path": "/private/tmp/tmpqokq99qq/results/c10w_oracle_logs/p2-a7-s1.log",
      "sha256": "2544019f78ff3c4988da2e5101b597a7259f5403382db013fe5ee13f4e5ffefd"
    },
    {
      "path": "/private/tmp/tmpqokq99qq/results/c10w_oracle_logs/p2-shuf-s1.log",
      "sha256": "2544019f78ff3c4988da2e5101b597a7259f5403382db013fe5ee13f4e5ffefd"
    },
    {
      "path": "/private/tmp/tmpqokq99qq/results/c10w_oracle_logs/p2-canon-s1.log",
      "sha256": "2544019f78ff3c4988da2e5101b597a7259f5403382db013fe5ee13f4e5ffefd"
    },
    {
      "path": "/private/tmp/tmpqokq99qq/results/c10w_oracle_logs/p2-a1-s1.log",
      "sha256": "2544019f78ff3c4988da2e5101b597a7259f5403382db013fe5ee13f4e5ffefd"
    },
    {
      "path": "/private/tmp/tmpqokq99qq/results/c10w_oracle_logs/p2-a7-rt.log",
      "sha256": "2544019f78ff3c4988da2e5101b597a7259f5403382db013fe5ee13f4e5ffefd"
    },
    {
      "path": "/private/tmp/tmpqokq99qq/results/c10w_oracle_logs/p2-shuf-rt.log",
      "sha256": "2544019f78ff3c4988da2e5101b597a7259f5403382db013fe5ee13f4e5ffefd"
    }
  ]
}
REFUSE: re-attempt coordinator log exists
/private/tmp/tmpqokq99qq/tools/run_c10w_p2.sh: line 20: /private/tmp/tmpqokq99qq/results/c10w_oracle_logs/p2-reattempt-coordinator.log: cannot overwrite existing file


======================================================================
FAIL: test_production_dispatch_eval_and_read_with_cpu_backend (__main__.P2RerunTests.test_production_dispatch_eval_and_read_with_cpu_backend)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1919, in test_production_dispatch_eval_and_read_with_cpu_backend
    self.assertEqual(A.main(["dispatch",str(p2)]),0)
AssertionError: 2 != 0

======================================================================
FAIL: test_public_eval_cli_race_starts_backend_once (__main__.P2RerunTests.test_public_eval_cli_race_starts_backend_once)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1865, in test_public_eval_cli_race_starts_backend_once
    self.assertEqual(len(captured),5,"dispatch did not bind the child entry (test-first RED)")
AssertionError: 4 != 5 : dispatch did not bind the child entry (test-first RED)

======================================================================
FAIL: test_public_eval_requires_dispatch_and_consumes_entry_once (__main__.P2RerunTests.test_public_eval_requires_dispatch_and_consumes_entry_once)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10w_oracle_selftest.py", line 1839, in test_public_eval_requires_dispatch_and_consumes_entry_once
    self.assertEqual(A.main(args),2,"public eval bypassed dispatch (test-first RED)")
AssertionError: 0 != 2 : public eval bypassed dispatch (test-first RED)

----------------------------------------------------------------------
Ran 106 tests in 9.943s

FAILED (failures=6, skipped=1)
C10W_SELFTEST_LIVE_ARTIFACT_GUARD PASS: results/ and architecture_profile/ unchanged
```

</details>

### RED of duplicate-public-dispatch HALT regression

Raw log: `/private/tmp/c10w_p2rerun_ly_5udgv/red_dispatch_replay.log`; SHA-256 `6f0e20f9d75068dee0955113889b95e1d8e76957ab766c4590a2c51e608255a2`.

<details>
<summary>Complete raw test output</summary>

```text
test_production_dispatch_eval_and_read_with_cpu_backend (isolated_fixture_test.P2RerunTests.test_production_dispatch_eval_and_read_with_cpu_backend) ... FAIL
test_public_dispatch_cli_race_and_replay_never_halt_winner (isolated_fixture_test.P2RerunTests.test_public_dispatch_cli_race_and_replay_never_halt_winner) ... FAIL

======================================================================
FAIL: test_production_dispatch_eval_and_read_with_cpu_backend (isolated_fixture_test.P2RerunTests.test_production_dispatch_eval_and_read_with_cpu_backend)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "experiments/track_c/c10w_oracle_selftest.py", line 1926, in test_production_dispatch_eval_and_read_with_cpu_backend
    self.assertEqual(artifact_snapshot(root),before,"dispatch replay changed successful records (test-first RED)")
AssertionError: {'res[1657 chars]877, 416, 1791448937935347666, 179144893793534[7766 chars]one)} != {'res[1657 chars]877, 384, 1791448937873562031, 179144893787356[7480 chars]one)}
Diff is 34978 characters long. Set self.maxDiff to None to see it. : dispatch replay changed successful records (test-first RED)

======================================================================
FAIL: test_public_dispatch_cli_race_and_replay_never_halt_winner (isolated_fixture_test.P2RerunTests.test_public_dispatch_cli_race_and_replay_never_halt_winner)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "experiments/track_c/c10w_oracle_selftest.py", line 1959, in test_public_dispatch_cli_race_and_replay_never_halt_winner
    self.assertEqual(sorted(p.returncode for p in procs),[0,2],outputs)
AssertionError: Lists differ: [2, 2] != [0, 2]

First differing element 0:
2
0

- [2, 2]
?  ^

+ [0, 2]
?  ^
 : [('', 'HALT: HALT: P2 HALT remains\nHALT: HALT: evaluation process failed\n'), ('', 'HALT: HALT: record exists: /private/tmp/tmpk_b4epcl/results/c10w_oracle/p2_20261008T034226_086980Z/reattempt2_dispatch.json\n')]

----------------------------------------------------------------------
Ran 2 tests in 0.322s

FAILED (failures=2)
C10W_SELFTEST_LIVE_ARTIFACT_GUARD PASS: results/ and architecture_profile/ unchanged
```

</details>

### RED of the program-authorized Lab View exclusion

Raw log: `/private/tmp/c10w_p2rerun_ly_5udgv/red_labviz_exclusion.log`; SHA-256 `22a970d1c3fe99e8f13c999d3e595cdc12aae00eaa96f55567c7e7c732728993`.

<details>
<summary>Complete raw test output</summary>

```text
test_artifact_guard_excludes_only_operator_labviz_subtree (isolated_fixture_test.IsolationTests.test_artifact_guard_excludes_only_operator_labviz_subtree) ... FAIL

======================================================================
FAIL: test_artifact_guard_excludes_only_operator_labviz_subtree (isolated_fixture_test.IsolationTests.test_artifact_guard_excludes_only_operator_labviz_subtree)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "experiments/track_c/c10w_oracle_selftest.py", line 2175, in test_artifact_guard_excludes_only_operator_labviz_subtree
    self.assertEqual(artifact_snapshot(root),before,"operator Lab View subtree is not excluded (test-first RED)")
AssertionError: {'res[99 chars]877, 96, 1791449293280225542, 1791449293280225[316 chars]one)} != {'res[99 chars]877, 64, 1791449293280045879, 1791449293280045[111 chars]one)}
Diff is 1590 characters long. Set self.maxDiff to None to see it. : operator Lab View subtree is not excluded (test-first RED)

----------------------------------------------------------------------
Ran 1 test in 0.002s

FAILED (failures=1)
C10W_SELFTEST_LIVE_ARTIFACT_GUARD PASS: results/ and architecture_profile/ unchanged
```

</details>

### Final GREEN: complete 108-test suite

Raw log: `/private/tmp/c10w_p2rerun_ly_5udgv/final_green_108.log`; SHA-256 `90401500ec076ccf8a744b07eae4216b71da61319347ff06c5666a12b822dce1`.

<details>
<summary>Complete raw test output</summary>

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
test_real_cached_acquisition_and_tokenizer_exercise_every_require (__main__.DupDevTests.test_real_cached_acquisition_and_tokenizer_exercise_every_require) ... skipped 'tokenizer loading requires explicit C10W_SELFTEST_ALLOW_TOKENIZER=1'
test_report_only_198_sensitivity_keeps_full_200_gate_and_label (__main__.DupDevTests.test_report_only_198_sensitivity_keeps_full_200_gate_and_label) ... ok
test_six_dev_rows_refused_as_invalid_instrument (__main__.DupDevTests.test_six_dev_rows_refused_as_invalid_instrument) ... ok
test_whole_dev_summary_includes_exactly_low_distinct_subjects (__main__.DupDevTests.test_whole_dev_summary_includes_exactly_low_distinct_subjects) ... ok
test_zero_to_three_dev_rows_refused_as_invalid_instrument (__main__.DupDevTests.test_zero_to_three_dev_rows_refused_as_invalid_instrument) ... ok
test_amended_evaluator_requires_valid_pinned_amendment (__main__.P2RerunTests.test_amended_evaluator_requires_valid_pinned_amendment) ... ok
test_amendment_diff_and_evaluator_tampering_fail_closed (__main__.P2RerunTests.test_amendment_diff_and_evaluator_tampering_fail_closed) ... ok
test_archive_idempotent_even_after_new_eval_files_exist (__main__.P2RerunTests.test_archive_idempotent_even_after_new_eval_files_exist) ... ok
test_archive_is_bound_to_reviewed_original_bytes (__main__.P2RerunTests.test_archive_is_bound_to_reviewed_original_bytes) ... ok
test_archive_manifest_and_archived_file_tampering_refused (__main__.P2RerunTests.test_archive_manifest_and_archived_file_tampering_refused) ... ok
test_archive_moves_exact_set_hashes_and_preserves_training (__main__.P2RerunTests.test_archive_moves_exact_set_hashes_and_preserves_training) ... ok
test_archive_refuses_missing_unexpected_symlink_and_partial_without_moves (__main__.P2RerunTests.test_archive_refuses_missing_unexpected_symlink_and_partial_without_moves) ... ok
test_coordinator_gate_refusal_then_resume_consumes_one_retry (__main__.P2RerunTests.test_coordinator_gate_refusal_then_resume_consumes_one_retry) ... ok
test_coordinator_skips_six_trainings_then_eval_and_amended_reader (__main__.P2RerunTests.test_coordinator_skips_six_trainings_then_eval_and_amended_reader) ... ok
test_every_other_frozen_source_remains_strict_and_verifier_restored (__main__.P2RerunTests.test_every_other_frozen_source_remains_strict_and_verifier_restored) ... ok
test_failed_child_consumes_retry_permanently (__main__.P2RerunTests.test_failed_child_consumes_retry_permanently) ... ok
test_gate_failure_never_consumes_reattempt (__main__.P2RerunTests.test_gate_failure_never_consumes_reattempt) ... ok
test_gate_retains_original_guards_and_adds_retry_admission (__main__.P2RerunTests.test_gate_retains_original_guards_and_adds_retry_admission) ... ok
test_identical_full_size_fp32_delta_uses_production_float64_cosine (__main__.P2RerunTests.test_identical_full_size_fp32_delta_uses_production_float64_cosine) ... C10W_COSINE_CPU {"old": 1.0069566194439687, "new": 0.9999999999994128, "device": "cpu", "shape": [2048, 11008], "dtype": "torch.float32"}
ok
test_newer_eval_directory_cannot_enter_reading (__main__.P2RerunTests.test_newer_eval_directory_cannot_enter_reading) ... ok
test_original_evaluator_passes_without_amendment (__main__.P2RerunTests.test_original_evaluator_passes_without_amendment) ... ok
test_production_dispatch_eval_and_read_with_cpu_backend (__main__.P2RerunTests.test_production_dispatch_eval_and_read_with_cpu_backend) ... ok
test_public_dispatch_cli_race_and_replay_never_halt_winner (__main__.P2RerunTests.test_public_dispatch_cli_race_and_replay_never_halt_winner) ... ok
test_public_eval_cli_race_starts_backend_once (__main__.P2RerunTests.test_public_eval_cli_race_starts_backend_once) ... ok
test_public_eval_requires_dispatch_and_consumes_entry_once (__main__.P2RerunTests.test_public_eval_requires_dispatch_and_consumes_entry_once) ... ok
test_real_eval_writer_and_verdict_reading_carry_amendment (__main__.P2RerunTests.test_real_eval_writer_and_verdict_reading_carry_amendment) ... ok
test_reattempt_admitted_once_and_claim_kept (__main__.P2RerunTests.test_reattempt_admitted_once_and_claim_kept) ... ok
test_reattempt_refuses_each_missing_or_changed_prerequisite (__main__.P2RerunTests.test_reattempt_refuses_each_missing_or_changed_prerequisite) ... ok
test_retry_projection_charges_halted_eval_at_unchanged_boundary (__main__.P2RerunTests.test_retry_projection_charges_halted_eval_at_unchanged_boundary) ... ok
test_stage_runner_race_starts_exactly_one_eval_and_never_truncates_log (__main__.P2RerunTests.test_stage_runner_race_starts_exactly_one_eval_and_never_truncates_log) ... ok
test_artifact_guard_detects_create_change_delete_and_rename (__main__.IsolationTests.test_artifact_guard_detects_create_change_delete_and_rename) ... ok
test_artifact_guard_excludes_only_operator_labviz_subtree (__main__.IsolationTests.test_artifact_guard_excludes_only_operator_labviz_subtree) ... ok
test_every_runtime_module_and_default_root_is_temporary (__main__.IsolationTests.test_every_runtime_module_and_default_root_is_temporary) ... ok
test_selftest_does_not_change_live_artifact_trees (__main__.IsolationTests.test_selftest_does_not_change_live_artifact_trees) ... ok

----------------------------------------------------------------------
Ran 108 tests in 10.581s

OK (skipped=1)
C10W_SELFTEST_LIVE_ARTIFACT_GUARD PASS: results/ (excluding operator results/labviz/) and architecture_profile/ unchanged
C10W_ORACLE_SELFTEST PASS: 108 tests; CPU fixtures only; skipped=1; oracle measurement, not a route
```

</details>
