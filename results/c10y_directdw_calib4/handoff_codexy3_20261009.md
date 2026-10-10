# Codex Y3 handoff — 2026-10-09

**BINDING context rule:** Watch `Context N% left`. Before ~20%, stop starting new work; write a handoff with completed/in-flight work, exact paths, next step and risks into the task report, then tell the orchestrator. Every handoff restates this rule. MAESTRO requested this handoff at ~13%; Y3 stops after writing it.

## Completed

- **D-C10y-precast repin:** only the benchmark entry in `experiments/track_c/c10y_precast_diag.py` SOURCE_PINS changed from `9b25a207…` to `3703d8b9c363bb06eab0ca66f38f4b01114363ae75a9d0397701e75aa2520041`. Working benchmark bytes matched `git show 0ef326e:experiments/track_c/c10z_astra_benchmark.py` (full build commit `0ef326e5229ac449664da89ff4984603e1b2378d`). Old `93080f5` versus committed new TEMPLATES: definition bytes, AST and literal values all equal. Flat digest `d6c7c700…`, engine digest `c7dabbe7…`, calibration-context equality and file pin `9472b663a34cfd9c0bb5448087ae0c2c333b1988b70f211fb2d90baaf8b560b7` preserved; other pins and drift checks untouched. Test-first RED/GREEN proved exact committed bytes accepted and altered benchmark bytes refused. Diagnostic selftest **69 PASS**; C10Y selftest **285 PASS**, with child-test permission and TMPDIR under `/private/tmp`. Proofs: `results/c10y_directdw_calib4/precast_build_report.md:3512`; scratch logs: `/private/tmp/c10y_build/precast_repin_20261009T203316Z/`.
- **Close-out drafted and folded:** `results/closeout_drafts_20261009.md`, reviewed FOLD-OK in `results/closeout_drafts_20261009_astra.md`; canonical detail in `CORPUS/59_C10Z_V7DIAG_A1.md` and `CORPUS/60_MATHLAB_HARVEST_REPLAY.md`. Updated the authorized trackers, JSON companions and state, using the renderer for GENERATED blocks and preserving existing decision rows. **D-C10z-v7diag, D-C10z-a1pop, D-ML-1, D-ML-2 and D-ML-3: closeout_check ALL GREEN each**, with currency enabled. Logs and preservation checks: `results/closeout_fold_20261009T223920Z/`. MAESTRO committed the fold as **`70122ff2da7c860fd9c1c1e71f96cd84ef1bb92c`**. Y3 made no commits or GPU launches.
- Attempt 4 and MathLab step 3 remain **PENDING**. MathLab evidence is **MATH-PROXY**, with no behavioral or F1 closure claim; harvest-2 step-2 completion was UNVERIFIED at the reviewed cutoff. Green close-out checks certify documentation, not completion of pending science.

## Reading the pre-cast outcome when the authorized run finishes

Authority: `docs/C10Y_PRECAST_DIAG_SCOPE.md:41` and `experiments/track_c/c10y_precast_diag.py:138`; consult `precast_impl_astra_r2.md` and `precast_impl_astra_r3.md` in the calibration-4 results directory. Classification is ordered **INCONCLUSIVE → R → S → UNCLASSIFIED**; **K is never emitted**.

| Label | Meaning and permitted next proposal |
| --- | --- |
| INCONCLUSIVE | A required capture, identity, validation, persistence, finiteness, resource, cleanup or deadline gate failed. No mechanism conclusion; any repair/rerun needs a separately reviewed proposal. |
| R | Native operands/state agree and repeats are byte-stable; CPU-fp32 multiplication of saved factors gives recipe-A-identical realized fp16 weights in all ten cells, while MPS differs in at least one A7 cell. May propose CPU-fp32 product redesign; does not establish calibration-4 causation or an exclusive mechanism. Adoption needs its own amendment, LAW#5 isolation, implementation review and team admission. |
| S | Validated complete traces directly show an operative input/state/orientation/formula discrepancy. May propose a separately reviewed investigation. Numerical distance alone cannot trigger S. |
| UNCLASSIFIED | Remaining numerical, conditioning or mixed cases. Descriptive evidence for a separately reviewed investigation proposal; conditioning or precision convergence does not establish K. |

**No label authorizes corrective execution, calibration 5, stage-1 dispatch or F1 closure.** Calibration 4 remains terminal HALTED at ZERO_STEP-IDENTITY. CPU/fixture PASS and advisor GO are not live qualification or launch clearance.

## Next step and traps

Successor stays on standby, then reads the fresh diagnostic terminal record together with supervisor/cleanup evidence when MAESTRO supplies the run outcome; returns any proposal for separate review. No run outcome is asserted here. Use a fresh exclusive output namespace; preserve calibration-1–4 artifacts and exact pins. Exit 0 or a go-file alone is not scientific success or GPU clearance. Bind `LLMDB_ROOT=$PWD` for this worktree's metadata checks/rendering. Use `/private/tmp` directly: mktemp's `/var` symlink paths are intentionally refused. No further work or commits in this session.
