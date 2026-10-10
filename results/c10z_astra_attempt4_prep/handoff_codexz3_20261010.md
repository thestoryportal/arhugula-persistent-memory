# Codex Z3 → successor / MAESTRO2 — rotation handoff — 2026-10-10 UTC

Prepared at MAESTRO2's clean-boundary rotation request (orchestration transferred around 00:45Z). Workspace: `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a`; branch: `worktree-c10k-route-a`. Z3 made no commits, GPU/model runs, science launches or dashboard restarts. Commits mentioned below were made by the orchestrator. No work is in flight in Z3. The successor's priority is attempt-4 outcome standby when MAESTRO2 requests it; this note authorizes no launch or measurement.

**BINDING CONTEXT DIRECTIVE (operator, 2026-10-09; AGENTS.md): watch `Context N% left`. Before approximately 20% remains, STOP starting new work, write a precise handoff into the task report with done/in-flight work, exact paths, next step and open risks, then tell the orchestrator and ask for a fresh successor. Never approach full-window compaction. EVERY handoff must restate this directive. This applies to your own session and every team session you orchestrate.**

Read this note together with `results/c10z_astra_attempt4_prep/handoff_codexz2_20261009.md`, the latest detector report/reviews, and the current frozen prereg. Do not repeat completed builds or fix rounds. This handoff's current-state checks used metadata/text/hash/git reads only; no process-1 directory reader, tensor load or numerical timer was executed.

## 1. GPU-job detector: DONE, Astra ACCEPTED; no uncommitted detector delta

Authoritative report: `results/dashboard_gpu_detector_report.md`; Z3 fix-round section starts at line 1208. Reviews: `results/dashboard_gpu_detector_astra_r1.md` (FIX-FIRST) → `results/dashboard_gpu_detector_astra_r2.md` (**GO**, read in full at rotation). Orchestrator commit **`5afd2c5`**, 2026-10-09 22:47:20Z, records the shared detector and r2 GO. Fresh scoped git status is clean for all detector files listed here.

One active detector in `tools/dashboard_live.py` is reused by the status bar (`tools/dashboard_bar.sh`), experiment tab (`tools/dashboard_experiment.py`) and existing MathLab consumer. It recognizes MathLab harvest and CPU notebooks (`tools/run_mathlab_cpu.sh` / `uv run --script mathlab/m*.py`), C10Z V7 probe, benchmark, attempt launcher/stage/resident, C10Y pre-cast and legacy C10 workers. It reports name, elapsed versus bound cap and known output directory. CPU activity does not claim GPU occupancy. Recorded CPU events retain an explicit process-unverified distinction.

Z3 reproduced the two r1 BLOCKING findings as RED before production edits: a lone legacy worker falsely displayed free, and concurrent CPU activity hid legacy experiment details. The additional no-log legacy-worker case was also RED. One fix round made all six new controls GREEN. The shared detector now falls back to an observed worker when no coordinator exists, while retaining coordinator priority; the experiment panel composes CPU/error metadata with legacy progress/results/logs, including an active worker before its log exists.

Final Z3 evidence: **120 dashboard tests PASS**, zero failures/errors/skips; **16 headless captures at 110×40 PASS**, plus real status-bar calls; **46 protected files unchanged** in that round. Astra r2 independently confirmed 120 tests and a 110×40 render. Evidence directory: `/private/tmp/dashboard_gpu_detector_z3_fix1.DsEZau/` (RED/GREEN logs, source delta patches, scope receipt, `renders_corrected/`). Exact commands and hashes are in the report.

| Detector source, current hash verified at rotation | SHA-256 |
|---|---|
| `tools/dashboard_live.py` | `adab10516a889bee1227706597869693a113b7e56af5b2b6757771fd44ecb96b` |
| `tools/dashboard_experiment.py` | `40e6dd310446935e660ec81aea2aa8d0655b4218de320abff2737e224cb0d772` |
| `tools/test_dashboard_gpu_detector.py` | `7122338f12c0bc8461847301ba90bcdd0c1b3a9c4220433ef0033d83a98005ab` |

Z3's fix-round repository edits were those three files plus the report append. Z2's shared bar changes are included in the orchestrator's detector commit. **Uncommitted detector files at rotation: none.** Z3 did not edit `tools/dashboard_mathlab.py`, `tools/mathlab_events.py` or `tools/labviz/**` for detector work. A later external `mathlab_events.py` change during the MathLab fold was documented rather than reverted.

Limits/traps: native successful process inventory and interactive tmux acceptance remain **UNVERIFIED**; `/bin/ps` was denied in this sandbox. Denial must display UNAVAILABLE, never free. Fixture PASS and rendered caps do not prove GPU clearance or deadline enforcement. Bind an observed PID/age to a unique open run; do not infer the running output from the newest directory, caller environment or stale events. The r1 non-blocking full-event-scan/no-ps-timeout advisory remains; no additional fix round was requested. No dashboard restart was performed.

## 2. C10Y PRECAST-BUDGET: draft complete; timer strictly UNRUN

Deliverables:

- `results/c10y_precast_diag/amendment_budget_draft.md`: **D-C10y-precast-budget / DRAFT / NOT FROZEN / NOT APPLIED / NO RUN AUTHORIZATION**. Intended later append-only destination is `docs/C10Y_PRECAST_DIAG_SCOPE.md`; Z3 did not amend that frozen v2 scope or its 2,820 s cap.
- `results/c10y_precast_diag/measure_controls.py`: CPU-only, read-only, stdout JSONL timer for one preserved recipe-A A7 layer 4–8. **UNRUN**, including help; no import, torch load or numerical execution by Z3. Static syntax/import/device checks and packet-interface checks against JSON metadata passed. Runtime behavior remains UNVERIFIED.

The orchestrator included the initial two deliverables in **`92f2316`**, 2026-10-10 00:02:55Z. Fresh status: timer clean; draft has exactly the **uncommitted final-verification addendum dated 2026-10-10T00:03:38.291539+00:00** (six appended lines). That addendum records 27 protected scope/source/result-phase files unchanged. Evidence: `/private/tmp/c10y_precast_budget_z3.zgxis3d9/verification.json` and `snapshot.json`. The proposal itself is already in the committed draft; commit does not freeze or authorize it.

| Current deliverable, hash verified at rotation | SHA-256 |
|---|---|
| Draft including uncommitted verification receipt | `f754e58a846f4ee6889477153946773d21ee1f46e56b0f5e19af6500c0b06b0f` |
| Unrun measurement script | `223415433de6c025913d8bc4d26497b7576c83ef94a30bae589b6e18b080e82f` |

Read in full while drafting: `results/c10y_precast_diag/20261009T225619Z_diagnosis.md`, the run's `run.json`, `supervisor_timeout.json`, every `phase_*.json`, `results/c10y_directdw_calib4/handoff_codexy3_20261009.md`, and frozen v2 `docs/C10Y_PRECAST_DIAG_SCOPE.md`, especially B1/B4. The failed namespace stays **INCONCLUSIVE / SUPERVISOR-TIMEOUT** (2,812 s under cap 2,820; return 137); A7 controls/cleanup incomplete; A1 native/controls NOT-RUN. Calibration 4 remains terminal ZERO_STEP-IDENTITY. No completing or reading around that failed run.

Measured phase costs: projectors **420.800392 s**, targets **411.631268 + 363.237501 s**, A7 native **578.185085 s**; A7 controls **≥985 s unfinished**, not a completed control timing. Setup/load/pristine plus projectors/both targets total **T_fixed = 1246.254198 s**. Proposed cap:

```text
T_raw = T_fixed + T_native[A7] + T_native[A1]
        + C_ctrl[A7] + C_ctrl[A1] + T_tail
T_cap = 60 × ceil(1.15 × T_raw / 60)
```

`C_ctrl` means the full five-layer phase per arm, including numerical kernels, common factors, device products/repeats, realizations, statistics, conditioning/residuals, hashing, durable writes and validation. L4/L5 completed-cell publication estimates are about 449.628624/438.203349 s. Using 450 s × 5 per arm, A7 native as an A1 proxy, and the retained 180 s tail gives **8,160 s / 136 min**, explicitly **provisional extrapolation**, not an admitted sufficient cap. A1, remaining layers, tail and any storage changes need measurements or explicit reviewed projections. The timeout traceback was in NumPy per-column quantiles during the third A7 cell; do not attribute the whole phase to solves.

Timer input: prefer `controls_A7_coined_coined_L4_control_inputs.pt` (saved common fp32 factor X), or `operands_A7_coined_coined_L4_A.pt` (times factor preparation). Accepts a .pt/.json path; defaults search the original run and `/Users/robertrhu/Backups/memit_offload/c10y_precast_20261009T225619Z/`. Matching original JSON may supply mandatory sidecar SHA binding if only .pt was moved. It uses CPU `torch.load(..., map_location="cpu", weights_only=True)`, validates metadata/dtype/shape/hash, times (b), (c), (d), (e-CPU), and prints seconds plus process-lifetime peak RSS. **(e)'s MPS repeat is NOT_MEASURED_CPU_ONLY.** Five-layer CPU-core totals are labelled extrapolations; whole-arm C_ctrl is UNMEASURED. It writes no tensors or scientific labels. Use project Python ≥3.11 (`hashlib.file_digest`), never macOS Python3.9. Do not run even help until MAESTRO separately clears CPU contention; this draft grants no measurement permission.

### What the disk budget still needs

The operator's incident note says 131 float64 .pt packets / 105 GB filled the disk and killed attempt-4's first start. The all-file metadata inventory used for the draft found **622 .pt / 117,364,108,482 bytes**, plus 6,752,330 JSON bytes. Its JSON-described float64 subset has a different count/byte sum; **the incident note's dtype/subset definition is unreconciled**. Do not invent an explanation or substitute a float64-only subtotal for all future writes.

Provisional uncompressed family projection: fixed records 51 packets / 8,596,403,387 B; native phase 81 packets / 74,606,353,731 B per arm × 2; controls cell 189 packets / 11,413,009,617 B × 10. Total **2,103 packets / 271,939,207,019 B**, plus projected metadata **22,829,824 B**. Pre-dispatch floor = projected incremental writes + **20 GiB** = **293,436,873,323 B / 273.284 GiB**, **before additional temporary-copy allowances**. A1/remaining-cell equivalence is projected, not measured.

Before any adoption/admission: reconcile the incident subset with the exact manifest; audit every writer family/count/dtype/duplicate and remaining shapes; measure serialization/compression temporary peak; select the actual writable output filesystem; record fresh free bytes there against the final projected writes + 20 GiB. Existing retained/offloaded evidence is not free-space credit. Recompute time and disk together if storage changes. No automatic cleanup, artifact deletion or in-run cap increase is authorized.

Freshly read offload receipt: `results/c10y_precast_diag/20261009T225619Z/OFFLOADED_OPERANDS.json` records **2026-10-09T23:57:02Z**, **131 files, failures 0**, destination above and `MANIFEST_sizes.txt` there. This confirms a recorded move, not a byte-verified archive or present free-disk clearance. Z3 performed no move/deletion and did not decode or rehash those large packets during rotation. The draft's inventory was taken before the move; do not count source and archive copies twice.

Frozen B1/B4 require full unique operands/state/systems/factors/updates/realizations, required per-column results and offending gate values, durably persisted **before dependent gates**. Hash-only replacement of unique tensors is forbidden. Lossless compression may be proposed only with byte-exact decoding, original dtype/raw-byte hashes, codec identity, exclusive/fsynced partial-failure handling and measured space/time/temp cost. Hash/summary-only applies only where the scope already allows it; duplicate payload references require a complete immutable full payload and durable phase metadata, plus separate writer/reader review. Never weaken persist-before-gate or retroactively rewrite the failed run.

## 3. Attempt 4: standby; process-2 permission has NOT been assessed

Z3 has not read the relaunched process-1 scientific outcome. Latest operator status before rotation: relaunch waiting on disk recovery. Do not infer current launch, liveness, completion or outcome from that dated message or this note.

Preserved infrastructure start: `results/c10z_astra_attempt4_infrafail_20261009T234321Z/`; archived chain log: `results/c10z_astra_attempt4_infrafail_20261009T234321Z_chain.log`. Read **`relaunch_ruling_astra.md` in that directory** in full. Astra says **RELAUNCH-OK only after disk recovery and identity/exclusivity checks**, through stage 0 in fresh `results/c10z_astra_attempt4/`, reusing unchanged go/benchmark #3. The prior model did load, but there was no recorded baseline score/LAW#3/completed LAW#5/V7 scientific observation (`completed=-1`, reading null). It is an incomplete infrastructure start, not another HALTED-V7. Disk-full is consistent with the supplied facts; surviving empty log/HALT files do not independently prove the terminating exception. The review required resident PID **71309** and workers gone; present exit remains UNVERIFIED in this sandbox. Never resume the archived `closed=false` record or carry artifacts into the new attempt.

### Frozen admission identity (small-file hashes rechecked at rotation)

| Binding | Exact value |
|---|---|
| `docs/C10Z_ASTRA_PREREG.md`, §12 FROZEN | SHA `5ad59d2c960b44d18b5d1c5410028b969aab93298eed5d42c527bd81a4d18eac` |
| Normative `results/c10z_astra_attempt4_prep/reference_R1000.json` | SHA `a477f1c4917de988682da097d460c3d70b4c3bd33856d83c1d0c7714f78aab68`; exactly 1,000 recorded rows / 95,610 nonpadding tokens |
| **Actual live** `results/c10z_astra_attempt4_go_record.json` | SHA `850988a5df22446d1f456c2ce270e2bffcd988c6f118bcb14d77f4f1ae9ca04f` |
| Benchmark #3 `results/c10z_astra_benchmark/20261009T202713Z_drift3_a1/benchmark.json` | SHA `facebb52c2300c5af785e63f4f85af09f222a15e4673ba53b93da11314e8d669` |
| Benchmark script pin, as recorded in go | `3703d8b9c363bb06eab0ca66f38f4b01114363ae75a9d0397701e75aa2520041` |
| Selected ceilings, seconds | C01 **9900**, C2 **14100**, C3 **24060** |

Supporting authority: `results/c10z_astra_attempt4_prep/a1_astra_r2.md` (FREEZE+GO), `go4_astra.md` (ADMIT+GO), `admission_receipt_drift3.md`, and the Z2 handoff's full source-pin table. The driver is **`experiments/track_c/c10z_astra_arms.py`**, not a `c10z_astra_driver.py` file. Revalidate all bound source/environment/model/tokenizer/cache identities at outcome/dispatch; this rotation rechecked the small-file table, not all model caches or current environment. The approved go's `recorded_by`/`decision_notes` still describe its earlier draft preparation; **do not edit approved bytes to fix that prose**. Do not use historical `results/c10z_astra_go_record.json` or the attempt-3 go.

### Exact outcome-reading and process-2 decision procedure, only when MAESTRO asks

1. Re-read current **§12** in `docs/C10Z_ASTRA_PREREG.md` (lines 821–872), especially (e)–(g), together with original K1/K2 and process-2 reproduction rules, Z2 handoff and the latest operator message. §12 changes only to the exact recorded R1000; baseline/LAW/V7/V8/all other gates remain. No redraw/reordering, diagnostic-m substitution or late source repinning around a drift is allowed.
2. Confirm which namespace MAESTRO says is the fresh relaunch: **`results/c10z_astra_attempt4/`**, not the archived infrastructure start or attempts 1–3. Read together `run.json`, `pass_p1.json`, any `halt_p1.json`, `manifest.json`, `pristine_hash.json`, `logs/heartbeat.json`, `logs/resident_p1.log`, and `results/c10z_astra_attempt4_chain.log`. Missing, empty, malformed, partial or still-open terminal records are INCOMPLETE/non-admitted, never a scientific PASS. Keep any stage/coordinator exit receipts. Do not infer worker exit from file completion.
3. Execute the **real model-free directory reader**, not a cached `run.reading`, after authorized completion/CPU clearance. Reference invocation (not executed in this rotation):

   ```sh
   W='/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a'
   LLMDB_ROOT="$W" PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/rtk proxy \
     "$W/.venv/bin/python" -B "$W/experiments/track_c/c10z_astra_read.py" \
     "$W/results/c10z_astra_attempt4"
   ```

   Preserve stdout and exact exit code in a fresh readout receipt. Require nonempty parseable JSON with `scientific_verdict` **exactly true** and `next_stage` an integer **exactly 3** for stage-3 consideration. Reader exit 0 alone is insufficient: a valid terminal NULL/UNDERFIT/TRADEOFF can also exit 0. Exit 2 is a refusal/non-scientific result. `read_directory` (lines 712–757) checks closure, halt, A1 go/benchmark/prereg/population pins, manifest go SHA, exact selected ceilings, attempt/PID binding, every on-disk artifact hash, manifest equality and complete pristine import before `read_process` validates V1–V13 and classifies.
4. Verify actual `run.json`: **`closed is True`, `halt is None`, `completed == 2`**; no HALT record/binding failure. K1 allows stage 2 only for clean PARTIAL/LEAD; K2 permits stage 3 only for clean PARTIAL/LEAD with the selected stage-3 ceiling. Substantive qualifiers kill continuation. Stage-2 **SINGLE-PROCESS is expected** and is not a substantive failure or a replication claim. Preserve label/base/qualifiers/gates/attribution; do not make permission from a promising score or log alone. `tools/run_c10z_attempt.sh` runs stage0 → stage1 → conditional stage2 and **does not launch stage3**.
5. Obtain **operator-native evidence that process-1 resident AND its workers AND stage/queue coordinators exited**, plus single-GPU exclusivity and actual writable disk clearance. `closed=true` is not OS-exit evidence; a coordinator exit alone is insufficient; denied ps is UNVERIFIED, not free. If this external condition is missing, say process2 is **NOT YET PERMITTED**, even if K2 survives.
6. Verify the selected stage-3 ceiling is present (**24060 s**, bound in the original launch), current frozen source/environment/go/benchmark bindings still validate, and **`results/c10z_astra_attempt4/process2/` does not exist**. Source gate: `c10z_astra_arms.py:1855–1865` enforces clean closed completed2/K2, directory reader, ceiling, fresh process2 directory and `verify_launch_binding`; the separate after-process1-exit condition is still mandatory. Check for a concurrent/duplicate stage3 dispatch before deciding.
7. Report **PERMITTED only if every preceding scientific, validity, external exit/exclusivity/disk and freshness condition passes**, citing the real reader receipt and native exit evidence. Otherwise report NOT PERMITTED / NOT YET PERMITTED with the precise failed or unverified gate. Z3/successor's present authorization remains **no GPU/no launches**: MAESTRO owns any separately authorized `tools/run_c10z_stage.sh 3` dispatch. A permission judgment is not a launch instruction.

Process2 must be a fresh process/PID/output namespace, repeat pristine import/Recipe A/LAW/V7 gates, and preserve/reproduce original raw-byte m/G identities; diagnostic tensors grant no exemption. After process2, use the same directory reader on the parent and `repro.json`; it binds both processes and recomputes artifact identity separately from R1–R3 numeric/behavioral reproduction. A SINGLE-PROCESS survivor is not replicated. Another V7 failure is terminal **HALTED-V7**: no further population search/redraw/automatic retry or benchmark #4. Identity drift blocks admission and requires new operator disposition, never a silent resync.

## 4. Other completed arc and operational traps

MathLab canonical stop fold is complete and recorded in orchestrator commit **`c109199`** (2026-10-09 23:13:57Z). Full evidence is appended once in `CORPUS/60_MATHLAB_HARVEST_REPLAY.md`; report `results/mathlab_staging/m3_stop_fold_report_codexz3.md`. D-ML-1 harvest-2 step3 calibration **FAIL, designed cheap stop**, Astra CONFIRM; step2 PASS **61/61, OPERANDS-ONLY**; D-ML-4 lab stop/step4 **SHELVED**; NEW-1 continues separately. D-ML-1 and D-ML-4 closeout_check ALL GREEN; renderer and currency checks passed. Do not restart this closed calibration or duplicate the detail across trackers. See report for fingerprint/check evidence and the documented concurrent external `mathlab_events.py` drift.

Operational traps: always confirm root/branch before editing; preserve concurrent work. Use `.venv`, explicit `/private/tmp` scratch and disabled bytecode. No science tests, torch/MPS imports or timer execution while GPU-LIVE/CPU contention is uncleared. Graft lookup during this rotation failed with `env: node: No such file or directory` in the tool PATH; no graph evidence or saved-token claim resulted, and known source spans were read directly instead. Do not install/update global tools or refresh a large graph just to complete this rotation. Shell file listings can be huge; target named text/JSON records rather than dumping the entire run or hashing 100+ GB packets during ASTRA contention. Never equate a recorded offload receipt, dashboard fixture or old source hash with present dispatch clearance.

Session context checkpoints from completed arcs (temporary paths, may expire): detector `/private/tmp/dashboard_gpu_detector_z3_fix1.DsEZau/gstack/projects/c10k-route-a/checkpoints/20261009-224305-codex-z3-detector-fix1-complete-attempt4-standby.md`; MathLab `/private/tmp/mathlab_stop_fold_z3.kfzj4igl/gstack/projects/c10k-route-a/checkpoints/20261009-231308-codex-z3-mathlab-stop-fold-complete-attempt4-standby.md`; budget `/private/tmp/c10y_precast_budget_z3.zgxis3d9/gstack/projects/c10k-route-a/checkpoints/20261010-000438-codex-z3-precast-budget-draft-complete-attempt4-standby.md`. Canonical repo reports above remain the durable pointers.

**Done / in flight / next / risks:** detector done/accepted/committed by orchestrator; budget draft/script done but unfrozen and script unrun; MathLab fold done/committed; Z3 has no in-flight work. Uncommitted Z3 deliverables at rotation are the budget verification addendum and this new handoff. Next: fresh successor takes MAESTRO2's attempt-4 outcome request, performs the real reader and strict external exit/admission checks, and reports process2 eligibility without launching. Budget measurements/adoption require separate review and clearance. Open risks: stale live-state assumptions, wrong/archived namespace, source drift, unmeasured control/storage costs, incomplete disk reconciliation, denied process inspection and premature/duplicate dispatch.

**BINDING CONTEXT DIRECTIVE, restated for every successor:** watch `Context N% left`; before approximately 20%, stop new work, write done/in-flight work, exact file paths, next step and open risks into the task report, tell the orchestrator and ask for a fresh successor. Do not approach full-window compaction. Every handoff restates this rule; apply it to every team session you orchestrate.
