**BINDING CONTEXT RULE:** Watch “Context N% left.” Before approximately 20%, stop starting new work, write a handoff into the report with done / in flight / exact paths / next step / risks, and tell MAESTRO so a fresh successor can start. Every handoff must restate this rule. This handoff closes Codex Z2’s work at MAESTRO’s approximately 24% interrupt; stop after writing and verifying it.

# Codex Z2 handoff — 2026-10-09

Recorded UTC: 2026-10-09T22:26:39.364484+00:00. Workspace: /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a; branch worktree-c10k-route-a. The workspace and branch were rechecked at closeout. No commits or mutating git operations were made. Preserve other sessions’ changes.

## Current live state and immediate priority

MAESTRO reports that the **live go record is published**, and attempt 4 process 1 **will launch from the operator’s queue chain after the C10Y pre-cast diagnostic**, using tools/run_c10z_attempt.sh. Do not launch a second copy, advance the queue, rerun the probe, or rerun the benchmark.

Read-only closeout verifies that results/c10z_astra_attempt4_go_record.json and results/c10z_astra_attempt4_prep/go_record_draft.json are byte-identical, 1,475 bytes, SHA-256 **850988a5df22446d1f456c2ce270e2bffcd988c6f118bcb14d77f4f1ae9ca04f**. The draft’s recorded_by/decision_notes still describe draft preparation; those exact approved bytes were published by the operator. Do not “correct” those strings or rewrite the go.

At this closeout, results/c10z_astra_attempt4/, results/c10z_astra_attempt4_chain.log and results/c10z_astra_attempt4_stage3.log do not yet exist. Queue scheduling is an operator-provided fact; it is not verified process liveness. Native /bin/ps is denied in this sandbox, so GPU inventory remains UNVERIFIED. Do not infer clearance from absent files, a coordinator’s exit, CPU activity, or denied process inspection.

Astra’s current approvals are results/c10z_astra_attempt4_prep/a1_astra_r2.md (**FREEZE+GO**) and results/c10z_astra_attempt4_prep/go4_astra.md (**ADMIT+GO**, no admission/go-draft blockers). Their “live go absent” and DRAFT SHA statements are dated review snapshots superseded by the published live go and the current frozen pins below. User instructions prohibit commits even where an older review recommends one. Any new Astra FIX-FIRST interrupt takes priority.

## What was built

### V7-DIAG and its one fix round

Authority: docs/C10Z_V7DIAG_BUILD_BRIEF.md, including the team-approved persistence-only G addendum; docs/C10Z_ASTRA_PREREG.md §11. The original prereg SHA was checked before implementation. The first **156,213 bytes** remain SHA-256 **7aedd4ace95d2611bf398768df63cb60df6fce5afc23cf23209497bcd1d17a29**, rechecked at this handoff. Earlier prereg sections were preserved.

Built experiments/track_c/c10z_v7_diag.py, tools/run_c10z_v7_diag.py and experiments/track_c/c10z_v7_diag_selftest.py, with the full requirement → test → implementation and RED/GREEN evidence in results/c10z_astra_attempt3/v7diag_build_report.md. The probe is a forward-only, pinned diagnostic, with no solve, edit or candidate search.

The CPU equivalence fixture uses mixed lengths including 101/137 tokens, nonzero padding activations, distinct 36 layers, 62 full sixteen-row batches and a final eight-row batch. Independent token IDs/counts and normalization checks sit outside the AST-compared loop. **CPU agreement does not establish MPS equivalence.**

Astra’s four blockers were reproduced as RED, then fixed:
- Returned m and provenance are exclusively saved, flushed and fsynced immediately, before provenance validation; mismatch details survive subsequent exception reporting.
- A retained supervisor, rather than execve-away, records exclusive, fsynced UTC-suffixed halt diagnostics for signal/timeout/crash, naming active/incomplete phases and retained artifacts.
- The original **3,060 s** deadline includes explicit cleanup and worker exit. Success is published only after cleanup and observed normal worker exit; a provisional verdict alone is incomplete.
- Fresh and process-2 G are saved/copied exclusively before V8; this changes persistence only. A forced V8 failure retains the original evidence.

Additional CPU controls cover supervisor-parent classification, cleanup/worker-exit stalls, post-cleanup abnormal exits and fsync on actual diagnostic inodes. Final fix-round verification was **41 V7 +209 ASTRA +47 benchmark =297 tests;295 passed,2 optional MPS tests skipped**, plus engine fingerprint PASS. Full output and intermediate REDs are retained in the report and /private/tmp/c10z_v7diag_fix1/.

The operator subsequently ran the diagnostic, producing **A1** in results/c10z_v7_diagnostic/20261009T182427Z/verdict.json. results/c10z_v7_diagnostic/reading_astra.md confirms that result. This is diagnostic population evidence; the earlier attempt 3 remains HALTED-V7, historical population provenance remains UNVERIFIABLE, and late-layer fidelity remains UNVERIFIED. Diagnostic m must never replace fresh baseline/LAW/V7 gates.

### A1 population amendment and validator fix round

Appended only §12 Amendment A1-POPULATION, Decision ID D-C10z-a1pop, initially DRAFT pending Astra. It is now **FROZEN**, whole-file SHA **5ad59d2c960b44d18b5d1c5410028b969aab93298eed5d42c527bd81a4d18eac**; see docs/C10Z_ASTRA_PREREG.md:821–872. Never restore the initial DRAFT SHA 526c48b0… or edit frozen sources to append an admission outcome.

The normative population is results/c10z_astra_attempt4_prep/reference_R1000.json, SHA **a477f1c4917de988682da097d460c3d70b4c3bd33856d83c1d0c7714f78aab68**. It binds the exact diagnostic R1000: wikimedia/wikipedia, config 20231101.en, train split, revision b04c8d1ceb2f5cd4588862100d08de323dccfbaa; 6,407,814 source rows, 41 Arrow files/order, full seed-1 permutation and its first 1,000 rows, ordered indices/row IDs/text hashes/text/token IDs/counts, model/tokenizer/cache pins. The population has 95,610 nonpadding tokens. Qwen/Qwen2.5-3B revision is 3aab1f1954e9cc14eb9509a215f9e5ca08227a9b. The artifact, rather than a regenerated sample, is normative; see §12(c) and a1_build_report.md.

Driver, reader and manifest validators reject every other population, including another otherwise-valid 1,000-row set with a recomputed H_in. Model/tokenizer/cache identities are bound. Arithmetic, precision, masking, 100-token truncation and sixteen-row batching are unchanged. Fresh statistics are persisted before validation; process 2 copies exact statistics/G bytes before semantic validation, with exclusive/fsynced writes and byte-identity checks. Forced mismatch/V8 failures preserve artifacts.

Astra r1’s two blockers were reproduced before production edits:
1. Resident now calls verify_launch_binding(launch, os.environ), then validates go_record(os.environ) and binds its full canonical contents and raw SHA to launch, **before first publication, budget/watchdog or Session**: experiments/track_c/c10z_astra_arms.py:1734–1740.
2. Reader validates three go pins (population/prereg/amendment), two benchmark pins (population/prereg) and manifest go SHA == launch go SHA: experiments/track_c/c10z_astra_read.py:729–735. All six mutations reject through both entry paths, with no scientific_verdict.

Boolean true/1 aliasing and raw-byte-only go drift controls also reject. DRAFT-negative fixtures use isolated prereg/status fixtures, so later repository freeze cannot silently convert the negatives into positives. The original report’s resident-revalidation claim was explicitly corrected at a1_build_report.md:1065.

The final A1 fix suite was **28 A1 +209 ASTRA +47 benchmark +41 V7 =325;323 passed,2 optional MPS skipped**, engine fingerprint PASS. Astra r2 independently reports the same count. Complete RED/GREEN/interim output is in results/c10z_astra_attempt4_prep/a1_build_report.md, especially “Fix round 1” at line1061, and /private/tmp/c10z_a1_fix1/. These are historical recorded runs, not a new scientific-suite execution at this handoff. The report’s pre-freeze reader/test/DRAFT hashes are dated; use current hashes below and the admitted benchmark’s bindings.

### Drift rerun #3 admission and approved go draft

The operator completed results/c10z_astra_benchmark/20261009T202713Z_drift3_a1/. Record SHA **facebb52c2300c5af785e63f4f85af09f222a15e4673ba53b93da11314e8d669**; benchmark script SHA **3703d8b9c363bb06eab0ca66f38f4b01114363ae75a9d0397701e75aa2520041**. COMPLETE; suspect=false, outliers=false, weights_unchanged=true, stop=false; 401 timed items and20 warmups,266.589375 s under600 s.

Mechanical verdict **ADMISSIBLE**. The external receipt results/c10z_astra_attempt4_prep/admission_receipt_drift3.md records exact source/environment/record/script identity, original prior-go/launch binding, refusal history and recomputed arithmetic. Selected ceilings: **C01=9900, C2=14100, C3=24060 s**. The frozen bounds hold: **7200≤9900≤10800** and nominal supremum **2(9900+14100)=48000≤55800 s**. C01+C2+C3=48060 is a distinct reservation sum, not the §9 nominal-supremum calculation. Previous admitted ceilings were8100/12600/20760; O rose53.3956→103.1373 s. There is no frozen ratio-based refusal for that increase. See prereg:453–457,489–517,665–671 and866–870; runbook D-C10z-budget:372, D-C10z-driftcap:376, D-C10z-drift3:399. Preserve all retained refusals/outcomes; this named #3 does **not** authorize #4.

The receipt was written exclusively/fsynced before the draft go. The draft retains decisions0/1/2, operator_yes=true, one_gpu_job=true, recorder/time, selected raw benchmark/script hashes and exact ceilings; it adds D-C10z-a1pop, population a477… and frozen prereg5ad…. Real CPU go/benchmark/launch/freeze validators accepted it without Session/model import. Mutation controls fail closed; Astra ADMIT+GO reports28 rejection controls including a coherent alternative population. Evidence: /private/tmp/c10z_drift3_go_prep/mechanical_admission.json, validate_draft.py and retained validation logs; complete output is embedded in the receipt.

No hashed prereg/driver/reader/benchmark/engine/c10e sources were changed to record admission. The external receipt is the D-C10z-budget row content. The live go was published later by MAESTRO from the approved draft.

## Current SHA-256 inventory

Computed from current raw bytes at this closeout. Reports contain dated historical hashes; this table distinguishes those snapshots from the current freeze and live binding. The seven benchmark source identities are the hparams, c10e, driver, reader, benchmark, engine and fingerprint rows. Treat any subsequent drift in them as an admission failure; do not “resync” around it.

| File | Current SHA-256 |
|---|---|
| docs/C10Z_ASTRA_PREREG.md | 5ad59d2c960b44d18b5d1c5410028b969aab93298eed5d42c527bd81a4d18eac |
| docs/C10Z_V7DIAG_BUILD_BRIEF.md | c49540704f20af2c3b7507592535e7ef35656a72427ba803303fb8253bb192a5 |
| experiments/track_c/c10z_v7_diag.py | f39da78b026bbab0d0c89f879d4e45762bca0f8ea342dd7477ed00f128dca917 |
| tools/run_c10z_v7_diag.py | 85d41cce96699576a521340beff978e69e3c563aa51b2fb450f9e299af86ee93 |
| experiments/track_c/c10z_v7_diag_selftest.py | 5778e9e84b12e580927fd399ed893ea5fe68095fb6cc09916f968a4ff50823ac |
| experiments/track_c/c10z_astra_arms.py | d723819a921d3374351237903a7646c7765160cb0ae38e9e949dc10924ea7126 |
| experiments/track_c/c10z_astra_read.py | f00e81ff4b3daa653ccd10f35d738c3dbd8419570a4ddb2ad2f537f477150a66 |
| experiments/track_c/c10z_astra_selftest.py | fdba61b7b948a88cc368c419625fd733f581a870237cad8ee56a93b00c7349fa |
| experiments/track_c/c10z_a1pop_selftest.py | abacda6012396d46131070bf4fd70830abd9718b850e20bff29b1f1781bfefc1 |
| experiments/track_c/c10z_astra_benchmark.py | 3703d8b9c363bb06eab0ca66f38f4b01114363ae75a9d0397701e75aa2520041 |
| experiments/track_c/c10z_astra_benchmark_selftest.py | 1f9cdb5f7200e91a9157b2dda29e836e524554097c80f0913d5ccbaa6bfb9f4a |
| configs/hparams/qwen25_3b_memit_hparams.json | 4225cc6aabc3eb9fa62d2bb2cac68b1238de3a39c5e469da635e6e1464aa3bb4 |
| experiments/track_c/c10e_bandknob.py | 1f6be5811d7e58f3ebda16867a4a174b1cf24d47f9a2514cf9c3f9d29f18e695 |
| memit_dry_run/memit/memit/memit_main.py | d941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65 |
| tools/engine_fingerprint.py | 450ee83ac829817299ead301c4a3d20702f431deaea4be58c77ecfd89a329162 |
| tools/run_c10z_attempt.sh | 613b6eb41e8a532fe4105f9dd3e737ee3fd242313cc2e6a029e1537448eee61e |
| tools/run_c10z_stage.sh | bd40e0f57282ca468a43f1c5e81d3f6e134562af4def9ce99b274f73d25414b9 |
| results/c10z_astra_attempt3/v7diag_build_report.md | ea059ecb12daa64d6adcef693ee533e6ab5dd4d47f6af34e4511c0e1486faf5f |
| results/c10z_v7_diagnostic/reading_astra.md | b176d38bc68e8f8dfd37f6edf8ca53b6c0b6bc02e44aecd3e064eb7e501842f8 |
| results/c10z_v7_diagnostic/20261009T182427Z/verdict.json | 1a8c63c918a920970317dc523ac3b001342d3335d45d8851da8e5b31e8f09c9e |
| results/c10z_v7_diagnostic/20261009T182427Z/pins.json | 4b9dfca558a988fce932cbb4f227d92cd431e8638300a5829ee53de809478821 |
| results/c10z_v7_diagnostic/20261009T182427Z/m_R1000.pt | d307b42c69b75fbd55d262490e2f922201bff9ba0f3018dcef6d34e09667de06 |
| results/c10z_astra_attempt4_prep/reference_R1000.json | a477f1c4917de988682da097d460c3d70b4c3bd33856d83c1d0c7714f78aab68 |
| results/c10z_astra_attempt4_prep/a1_build_report.md | bb6ef34a59a0c3825ee1ad322b7c41a7f3c5a4bec5d3cc61ceb2d53f344b1b12 |
| results/c10z_astra_attempt4_prep/a1_astra_r1.md | abdc7065957fccf19bd1ed968261a096d8a956d1e8fde5019e84268848241aa6 |
| results/c10z_astra_attempt4_prep/a1_astra_r2.md | fe761a78a4b6bb103f2f3828557798f12be0c2f56b1d0a1e40d75930b2846327 |
| results/c10z_astra_benchmark/20261009T202713Z_drift3_a1/benchmark.json | facebb52c2300c5af785e63f4f85af09f222a15e4673ba53b93da11314e8d669 |
| results/c10z_astra_benchmark/20261009T202713Z_drift3_a1/benchmark.log | 0dcedf65bb7eb2227bdbf03b79a6e49a8d9587590f150036757febe0fca9df9c |
| results/c10z_astra_attempt4_prep/admission_receipt_drift3.md | 83ca0886f751aab1d2fea7430c90efa5dacf05c27a40afa6c36152a3cba11df7 |
| results/c10z_astra_attempt4_prep/go_record_draft.json | 850988a5df22446d1f456c2ce270e2bffcd988c6f118bcb14d77f4f1ae9ca04f |
| results/c10z_astra_attempt4_go_record.json | 850988a5df22446d1f456c2ce270e2bffcd988c6f118bcb14d77f4f1ae9ca04f |
| results/c10z_astra_attempt4_prep/go4_astra.md | f96027ddc826b9ce4bf565b27a1761ef5a2d1002bf8113b6ea6883727df06c62 |
| tools/dashboard_live.py | 75ca7100c0f64bc3debd14e05c6e65a2109238057dfa98620f96f5082c35b572 |
| tools/dashboard_experiment.py | 933c2336c5813e3a9f444b88ee58ba0ab8a255917db051d5331dcdfbe2d7b640 |
| tools/dashboard_bar.sh | 535e04d3ea0357183e9448e95e88a673294d83aba4772208be545c2f8e3a4b0e |
| tools/test_dashboard_live.py | b9fec5d1c0eceea40e5caad6222d56447352cf79cdbeb0ac8f984ec25e9ed81d |
| tools/test_dashboard_gpu_detector.py | e2b86fad7dd00bab2c4b8a349d33c0abb91a2a4cc43cf70c6603a33128153173 |
| results/dashboard_gpu_detector_report.md | f8cf38276137d3c9526d465ab6aefa75452d4804f159be422ca5790573329eab |
| /private/tmp/c10z_a1pop_build/run_cpu_selftest.py | 67e0de86c2d06463ecd8105ce393dfc7b5f03efaa64083bf118a78203f574e21 |
| /private/tmp/c10z_drift3_go_prep/mechanical_admission.json | 6325efa0d84f9ece560e03dc4ac2705d054d3490b25ea38ea00a664a451789ad |
| /private/tmp/c10z_drift3_go_prep/validate_draft.py | 626ec729355f58e27a5fefeaa42e49257903cbd437b278d47dd8e9dccb3adce5 |
| /private/tmp/dashboard_gpu_detector_final/review_fix_green.txt | 642a1c3363024549a7899040e33c0a2328c940638f1df816eeb47ab5d70a9bd2 |
| /private/tmp/dashboard_gpu_detector_final/render_final.py | 5a4bc900540bdbf589aee60ed7e96144280b2e23b2bc7e6d1c8ba5472ac3c896 |
| /private/tmp/dashboard_gpu_detector_final/render_final_checks.json | cdb5ae144b5c277a805864e80fd5ca5b0ac3eb41e0b8ae8a8c2d6672caba8b7e |

## Exact CPU verification commands and evidence

These commands are reference instructions; **no new tests or job dispatch were run during the handoff**. Use the project .venv, not macOS Python3.9. TMPDIR and bytecode caches must be explicitly under **/private/tmp**; do not use a denied /var/folders temporary directory. The existing CPU runner was rechecked, SHA67e0de86c2d06463ecd8105ce393dfc7b5f03efaa64083bf118a78203f574e21; it forces MPS availability false, asserts on unmocked synchronize/driver-memory APIs and limits CPU threads to one. Never remove those guards to make optional MPS controls pass.

```bash
W='/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a'
cd "$W"
export LLMDB_ROOT="$W"
export TMPDIR=/private/tmp/c10z_a1_fix1
export PYTHONPYCACHEPREFIX=/private/tmp/c10z_a1_fix1/successor-pycache
/opt/homebrew/bin/rtk proxy .venv/bin/python -B /private/tmp/c10z_a1pop_build/run_cpu_selftest.py experiments/track_c/c10z_a1pop_selftest.py
/opt/homebrew/bin/rtk proxy .venv/bin/python -B /private/tmp/c10z_a1pop_build/run_cpu_selftest.py experiments/track_c/c10z_astra_selftest.py
/opt/homebrew/bin/rtk proxy .venv/bin/python -B /private/tmp/c10z_a1pop_build/run_cpu_selftest.py experiments/track_c/c10z_astra_benchmark_selftest.py
/opt/homebrew/bin/rtk proxy .venv/bin/python -B /private/tmp/c10z_a1pop_build/run_cpu_selftest.py experiments/track_c/c10z_v7_diag_selftest.py
/opt/homebrew/bin/rtk proxy .venv/bin/python -B tools/engine_fingerprint.py
```

The receipt records this exact draft-validation invocation. TMPDIR must be set as shown when reproducing it. **Do not blindly rerun it in the used evidence namespace:** the helper creates exclusive evidence/negative-fixture files; use a fresh /private/tmp namespace and adjust its evidence paths first, leaving live records and all frozen sources unchanged. Read the helper before executing an adapted version.

```bash
TMPDIR=/private/tmp/c10z_drift3_go_prep /opt/homebrew/bin/rtk proxy env \
  PYTHONPYCACHEPREFIX=/private/tmp/c10z_drift3_go_prep/fresh-pycache \
  .venv/bin/python /private/tmp/c10z_drift3_go_prep/validate_draft.py
```

Earlier helper-only errors (overbroad process-dispatch guard intercepting stdlib uname; wrong interpreter lacking torch metadata; selector errors) are retained in the reports. They were corrected without changing science/admission rules and are not benchmark refusals.

## Reading attempt-4 outcomes and the process-2 gate

When process1 has finished, use the **actual directory reader**, which reads artifacts only and does not load a model:

```bash
W='/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a'
TMPDIR=/private/tmp/c10z_a1_fix1 PYTHONPYCACHEPREFIX=/private/tmp/c10z_a1_fix1/read-pycache \
  LLMDB_ROOT="$W" /opt/homebrew/bin/rtk proxy "$W/.venv/bin/python" -B \
  "$W/experiments/track_c/c10z_astra_read.py" "$W/results/c10z_astra_attempt4"
```

The reader CLI exits0 for scientific_verdict=true and2 for a refusal/incomplete record. A partial/open directory is **not a final verdict**: read_directory requires run.closed=true, rejects halt files, checks A1 pins, ceilings, attempt/PID/go binding, every recorded artifact hash, manifest and pristine evidence. See reader:712–755. Check run.json, pass_p1.json/halt_p1.json, manifest.json, pristine_hash.json, logs/heartbeat.json, stage logs and the chain log together; logs alone do not establish admission or completion. Preserve any halt/partial artifact, including diagnostics and raw statistics/G.

Process1’s normal progression is stage0 → stage1 → conditional stage2. tools/run_c10z_attempt.sh:7–19 invokes stage2 only when stage1’s recorded next_stage is exactly2; it does not dispatch stage3. read_process validates V1–V13 before classification. NULL/UNDERFIT/TRADEOFF or any substantive qualifier does not survive K1/K2. At stage2, SINGLE-PROCESS is expected pending reproduction; it is not a replication claim.

**Process2 via tools/run_c10z_stage.sh 3 is allowed only if ALL hold:**
1. Process1 has a clean completed K2 survivor, with the real directory reading scientific_verdict=true and next_stage exactly3. Do not infer eligibility from a promising score or PARTIAL text alone.
2. run.json has closed=true, halt=null and completed exactly2; no halt_p1.json or incomplete/invalid artifact binding.
3. The process1 resident **and** its stage/queue coordinator have actually exited, established by the operator’s native process/exit evidence. closed=true is necessary but does not prove OS process exit; ps denial cannot supply that proof.
4. The approved selected stage3 ceiling is present, current frozen source/environment/go/benchmark bindings still validate, and the single-GPU queue is clear under operator control.
5. results/c10z_astra_attempt4/process2/ does not exist. It must be a fresh second process/output namespace.

Source gate: driver:1855–1865 enforces the completed/closed K2/directory-reader/ceiling/fresh-directory/launch binding requirements. The external **after-process1-exit** condition remains mandatory. Process2 must run fresh pristine import/baseline/LAW/V7 and reproduce the original byte-identical m/G input artifacts; diagnostic A1 is no exemption.

Selected binding and process1 command below are **reference only, NOT EXECUTED by Codex Z2**. MAESTRO’s queue already owns process1; do not run this again. It must use the completed #3 directory, not the historical dynamic benchmark command in a1_build_report.md:78.

```bash
W='/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a'
BENCH_OUT="$W/results/c10z_astra_benchmark/20261009T202713Z_drift3_a1"
GO="$W/results/c10z_astra_attempt4_go_record.json"
C2="$("$W/.venv/bin/python" -B -c 'import json,sys; print(json.load(open(sys.argv[1]))["ceilings"]["stage2"])' "$GO")"
C3="$("$W/.venv/bin/python" -B -c 'import json,sys; print(json.load(open(sys.argv[1]))["ceilings"]["stage3"])' "$GO")"
nohup /usr/bin/caffeinate -i env -u C10Z_TELEMETRY -u C10Z_TELEMETRY_INERTNESS \
  LLMDB_ROOT="$W" C10Z_OUT_DIR="$W/results/c10z_astra_attempt4" \
  C10Z_GO_RECORD="$GO" C10Z_BENCHMARK_RECORD="$BENCH_OUT/benchmark.json" \
  C10Z_STAGE2_CEILING_S="$C2" C10Z_STAGE3_CEILING_S="$C3" \
  "$W/tools/run_c10z_attempt.sh" > "$W/results/c10z_astra_attempt4_chain.log" 2>&1 &
```

Only after all five process2 conditions and operator queue authorization, the separately requested command is:

```bash
nohup /usr/bin/caffeinate -i env -u C10Z_TELEMETRY -u C10Z_TELEMETRY_INERTNESS \
  LLMDB_ROOT="$W" C10Z_OUT_DIR="$W/results/c10z_astra_attempt4" \
  C10Z_GO_RECORD="$GO" C10Z_BENCHMARK_RECORD="$BENCH_OUT/benchmark.json" \
  C10Z_STAGE2_CEILING_S="$C2" C10Z_STAGE3_CEILING_S="$C3" \
  "$W/tools/run_c10z_stage.sh" 3 > "$W/results/c10z_astra_attempt4_stage3.log" 2>&1 &
```

These blocks are transcribed from the approved lead interfaces and are not instructions for the successor to launch while still under the no-GPU/no-launch constraint. Set any scratch TMPDIR explicitly under /private/tmp. After process2, use the same directory reader; it binds both processes and repro.json, including fresh PID, pristine/input/attempt identity and recomputed reproduction evidence. Only its validated aggregate establishes replication. Another V7 failure stays **HALTED-V7, with no further search**. No fourth benchmark rerun or retry is authorized.

## Detector stopping state — implementation COMPLETE

Latest authority is the appended completion/handoff in **results/dashboard_gpu_detector_report.md**, not its older parked/93-test sections. Full evidence: **/private/tmp/dashboard_gpu_detector_final/**.

Done: one shared detector in tools/dashboard_live.py, consumed by the status bar tools/dashboard_bar.sh and experiment tab tools/dashboard_experiment.py. It recognizes harvest launcher/worker/admission; V7 launcher/worker; C10Y pre-cast launcher/worker; C10Z benchmark; attempt4 launcher/stage/resident; MathLab CPU launcher/runner/admission and uv run --script mathlab/m2_solve_repro.py /m3_calibration.py. CPU notebooks stay separate from GPU occupancy. Job name, elapsed versus source/recorded cap and exact known output directory are shown. Unknown output remains unavailable; events/run directory is separate provenance.

Caps: harvest3600, V73060, pre-cast2820, benchmark600, CPU step2=6540/step3=1800 s; ASTRA uses exact admitted launch/run budget scope. Active/incomplete phase or deadline enforcement cannot be inferred from a displayed cap. Records require a unique, open PID-and-age-bound run; process2/run.json is supported. Do not trust caller environment or the newest folder. Transparent wrappers and nested env clearing are covered. Per-PID age prevents an old parent from admitting a stale resident origin. --selftest/--help/prompt/module/inline/temporary-copy commands do not claim GPU occupancy.

Fresh publisher events supplement CPU visibility when ps is denied, using the existing unmodified mathlab_events reader/fold. Timestamp microseconds are supported. Stale/expired/future/finished/refused/malformed events do not claim activity. Event PID is provenance, not process-liveness proof.

Final tests: **114 PASS (34 detector/experiment/bar +27 live +53 MathLab),4.502 s**. Ten final-source **110×40** headless captures PASS, plus the real status-bar CLI. Exact final test log: review_fix_green.txt; render checks: render_final_checks.json; final render driver: render_final.py. Their hashes are included below. Full verbose output and every render are embedded in the detector report. Scope check:36 protected snapshots unchanged; the excluded MathLab/Lab View files and science sources were preserved. This is scoped hash evidence, not a global clean-tree claim.

At capture time **2026-10-09T22:13:31.082490Z**, live rendering showed MathLab step2’s fresh event in results/mathlab_staging/runs/m2_20261009T211535Z_57196, elapsed57:56/cap6540 s, CPU RECORDED/process unverified; GPU UNAVAILABLE because /bin/ps returned Operation not permitted. This is the captured state, not a claim that step2 remains running now. Harvest/CPU artifact Output is unavailable unless an exact artifact link is known; its events directory must not be substituted.

The existing review agent’s final CPU-only fallback review was PROCEED after two concrete RED controls (old-parent PID age and nested env clear) were fixed and all114 tests/ten renders passed. Claude primary auth was loggedIn=false; this fallback has weaker independence and grants no science/GPU permission.

**Remaining steps:** no detector implementation or failing test remains. Native process-inventory acceptance and interactive teamdash/tmux visibility remain **UNVERIFIED** due sandbox process denial; an operator outside this sandbox can observe the already queued pre-cast/attempt4 jobs after they start. Existing panes reload sources normally; no tmux rebuild/activation was performed. Do not launch a job to obtain this verification or edit tools/dashboard_mathlab.py, tools/mathlab_events.py or tools/labviz/**.

Reference detector checks, all with explicit private temporary roots:

```bash
mkdir -p /private/tmp/codexz2_detector_checks
TMPDIR=/private/tmp/codexz2_detector_checks PYTHONPYCACHEPREFIX=/private/tmp/codexz2_detector_checks/cache \
  /opt/homebrew/bin/rtk proxy .venv/bin/python -B -m unittest discover -s tools -p 'test_dashboard*.py' -v
TMPDIR=/private/tmp/codexz2_detector_checks /opt/homebrew/bin/rtk proxy \
  .venv/bin/python -B tools/dashboard_experiment.py --once11040
TMPDIR=/private/tmp/codexz2_detector_checks /opt/homebrew/bin/rtk proxy \
  .venv/bin/python -B tools/dashboard_mathlab.py --once11040
TMPDIR=/private/tmp/codexz2_detector_checks /opt/homebrew/bin/rtk proxy bash tools/dashboard_bar.sh
```

Do not rerun the render_final.py evidence writer against its already-used output filenames without a fresh evidence namespace. It exercises fixture jobs and the real CLIs without job dispatch.

## Successor next step and traps

Start by reading this handoff, the latest dated detector completion, current FROZEN §12, go4_astra.md and MAESTRO’s new message; do not restart completed build/fix rounds. The active work is operator-owned queue/run observation, with priority for any Astra FIX-FIRST. Wait for authorized process1 completion, validate directory outcomes, and apply the strict K2/exit gate before considering a separately authorized process2.

Keep byte identity and pre-validation persistence; never rewrite evidence to turn a halt into admission. Preserve all historical results/refusals and the original attempt3 HALTED-V7. Do not append to the frozen prereg or modify hashed sources after benchmark admission. No GPU/MPS/model load/launch/commit is authorized for this closeout or routine successor CPU checks. Engine/c10e edits remain prohibited.

CPU fixtures prove plumbing, gates and preservation only; native MPS equivalence, live deadline sufficiency and scientific success require their own admitted evidence. Science-path one-fix-then-halt and no-fourth-rerun rules remain binding. A missing output/process snapshot is not GPU clearance, and a provisional/closed record is not OS-exit proof.

Reusable lesson: check the PID/time origin at the same process that owns a budget; retain raw evidence before validating it; bind every public entry and reader path independently; keep historical report status separate from live immutable records. This lesson is saved here, not in home memory.

**Done / in flight / next / risks:** all Z2 builds, requested fix rounds, mechanical admission/go preparation and detector implementation are complete; MAESTRO owns the published go and queued process1; next is authorized read-only outcome validation and external native dashboard acceptance; principal risks are source drift, duplicate dispatch, premature process2, treating CPU evidence as MPS equivalence and stale historical SHA/status text.

**BINDING CONTEXT RULE (restated):** Watch Context N% left. Before approximately20%, stop starting new work; write done / in flight / exact paths / next step / risks into the report, tell MAESTRO so a fresh successor can start, and restate this rule in every handoff. Codex Z2 stops after this handoff.
