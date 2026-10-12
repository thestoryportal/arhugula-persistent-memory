

## 2026-10-09 — D-ML-2 implementation

Recorded UTC: 2026-10-09T17:57:31.018332+00:00. **Outcome: accepted — CPU fixture/tooling build acceptance.** Both former blockers are now covered by the preserved MAESTRO evidence below. Production completion within the provisional 6,540-second cap remains **UNVERIFIED**, as frozen §14 requires.

Authority: `docs/MATHLAB_PREREG.md` §14 Amendment M2-BUDGET, D-ML-2, frozen in commit `de561958769cb27514c319f5a77d61ea482b71b6`. Read §14 in full and verified the amended prereg hash before edits:

~~~text
4852d1a229e186c1d054c6f1849f3c130f333738aa9dfc297bedac8cd44ad507  docs/MATHLAB_PREREG.md
~~~

| Frozen requirement | Implementation | Verification |
|---|---|---|
| Step-2 hard deadline 2,700 → 6,540 seconds | `tools/run_mathlab_cpu.sh:8,13`, `tools/mathlab_cpu_runner.py:17`, `mathlab/core.py:385` | Real shell case-table exercise (relative and absolute notebook paths), validator acceptance/refusal, actual notebook `stage_started.cap_s == 6540` |
| SVD pre-cell reserve 4 → 5 GiB, named beside solve reserve | `mathlab/core.py:16` defines `SVD_RESERVE_GIB = 5`; `:240` uses it before the projector | Tiny CPU fixture wraps the real projector and verifies the preceding admission reserve is 5 GiB for every layer |
| Solve reserve remains 9 GiB | `mathlab/core.py:17,252,270` | Real solve and clean-key-alternative call paths verify the preceding reserve is exactly 9 GiB |
| Repin the exact frozen SHA, preserve verification | `tools/mathlab_runtime.py:17`; `verify_prereg` at `:48` unchanged | Exact new hash accepts; altered prereg bytes and the old pin refuse; [runtime_guard_and_dependencies.json](dml2_impl_20261009T174802.238815Z/runtime_guard_and_dependencies.json) |
| Step 3 remains 1,800 seconds; index remains 300 | Validator/shell step-3 cases unchanged; `mathlab/core.py:385,408` retain these caps | Step-3 runner/shell checks and source/snapshot review; preserved fixture events independently record 1800/300 |
| Watchdog, 8 GiB floor, 300-second memory wait, abort policy, niceness/timeout command unchanged | No edits to these contracts or scientific arithmetic | Full suite plus reviewed [implementation.diff](dml2_impl_20261009T174802.238815Z/implementation.diff) |

All 15 step-2 fixture/test uses of the prior deadline were updated. An exhaustive search of active `mathlab/` and `tools/` Python/shell files leaves 2,700 only in deliberate old-deadline refusal controls and `tools/test_dashboard_mathlab.py:64`, an unrelated historical event fixture. Frozen docs and historical evidence/helpers retain their original values. No old output was rerun, relabelled or repinned under D-ML-2.

**Test-first evidence.** Only tests were edited before RED. Five amended contract tests failed with seven assertion failures (shell subtests account for the extra failures): old runner deadline, old shell cases, old SHA pin, 4 GiB SVD admission, and actual notebook stage cap 2700. After the minimal four-production-file patch, the same five tests passed. Full outputs: [tests_red.txt](dml2_impl_20261009T174802.238815Z/tests_red.txt), [tests_green_targeted.txt](dml2_impl_20261009T174802.238815Z/tests_green_targeted.txt), [tests_green_full.txt](dml2_impl_20261009T174802.238815Z/tests_green_full.txt).

| Requested check | Result | Full evidence |
|---|---|---|
| Full `mathlab.test_mathlab` suite, CPU tensors, eight threads | **62 tests PASS**, exit 0 | [tests_green_full.txt](dml2_impl_20261009T174802.238815Z/tests_green_full.txt) |
| Real DuckDB provenance/rebuild test, DuckDB 1.5.6 | **1 test PASS**, exit 0 | [index_green.txt](dml2_impl_20261009T174802.238815Z/index_green.txt) |
| marimo 0.25.1 `check --strict`, both notebooks | **PASS**, exit 0, no diagnostics | [marimo_check.txt](dml2_impl_20261009T174802.238815Z/marimo_check.txt) |
| `bash -n`, CPU and harvest launchers | **PASS**, exit 0 | [bash_syntax.txt](dml2_impl_20261009T174802.238815Z/bash_syntax.txt) |

Exact commands (executed through `rtk proxy`; no dependency installation):

~~~sh
env LLMDB_DEVICE=cpu CUDA_VISIBLE_DEVICES= OMP_NUM_THREADS=8 MKL_NUM_THREADS=8 .venv/bin/python -B -m unittest mathlab.test_mathlab -v
/private/tmp/mathlab_uv_cache/environments-v2/m2-solve-repro-da15e0fd897e5e61/bin/python -B -m unittest mathlab.test_index -v
env LLMDB_DEVICE=cpu CUDA_VISIBLE_DEVICES= PYTHONDONTWRITEBYTECODE=1 /private/tmp/mathlab_uv_cache/environments-v2/m2-solve-repro-da15e0fd897e5e61/bin/python -B -m marimo check --strict mathlab/m2_solve_repro.py mathlab/m3_calibration.py
/bin/bash -n tools/run_mathlab_cpu.sh tools/run_mathlab_harvest.sh
~~~

Structured check/exit records: [validation_results.json](dml2_impl_20261009T174802.238815Z/validation_results.json). The existing uv PEP 723 environment contains torch **2.8.0**, marimo **0.25.1**, duckdb **1.5.6**, psutil **7.2.2**, numpy **2.4.6**, and pydantic **2.14.0**; current metadata and exact-pin refusal evidence are in [runtime_guard_and_dependencies.json](dml2_impl_20261009T174802.238815Z/runtime_guard_and_dependencies.json). No model was loaded.

**Former blocker 1 — complete full-production-shape RSS: cleared by recorded evidence.**

| CPU cell | Completion | Wall time basis | Measured peak RSS | D-ML-2 reserve | Sources |
|---|---|---|---|---|---|
| Projector / SVD | PASS, exit 0 | Supervisor 78.9521 s; worker 77.7116 s | Native 4.6087799 GiB; sampled 4.6087646 GiB | **5 GiB** | [peak_svd_full.json](peak_svd_full.json), [peak_svd_full.txt](peak_svd_full.txt) |
| Solve, fp64 solve and condition diagnostics | PASS, exit 0 | Worker 146.1312 s; supervisor 146.8385 s | Native 8.0843353 GiB; sampled 8.0843048 GiB | **9 GiB** | [peak_solve_full.json](peak_solve_full.json), [peak_solve_full.txt](peak_solve_full.txt) |

Both JSON records and terminal worker completion records were read and checked. These are completed synthetic full-shape cells, superseding the earlier capped lower bounds for build acceptance. The historical probe JSON `reserve_gib: 4` annotation is preserved; implemented reserves follow §14 and the measured peaks, rounded upward to whole GiB. The unchanged pre-cell free-memory floor remains 8 GiB above each reserve.

The §14 arithmetic is unchanged: partial workload estimate 5,636.30 seconds × 1.15 = 6,481.745 seconds, rounded to a whole minute gives 6,540. One contended sample, synthetic spectra/conditioning, probe scheduling that did not reproduce nice-10, untimed hashing/I/O/comparisons/saves and memory waits, and an unvalidated 1.15 factor leave production completion feasibility **UNVERIFIED**. This is the frozen spending cap, not a demonstrated production bound.

**Former blocker 2 — frozen-runtime headless path: cleared by recorded evidence.**

| Notebook | Recorded real runner/uv result | Preserved sources |
|---|---|---|
| Step 2 | Runner exit **0**, terminal `run_finished` **PASS**, gate 2a PASS; fixture-only | [fixture_attempt.json](fixture_20261009T025921.171236Z/runner_uv_m2_20261009T173552.166039Z/fixture_attempt.json), [events.jsonl](fixture_20261009T025921.171236Z/runner_uv_m2_20261009T173552.166039Z/events.jsonl), [output manifest](fixture_20261009T025921.171236Z/runner_uv_outputs/m2_20261009T173600.219909Z/manifest.json) |
| Step 3 | Runner exit **0**, terminal `run_finished` **PASS**, calibration and index-provenance PASS; fixture-only | [fixture_attempt.json](fixture_20261009T025921.171236Z/runner_uv_m3_20261009T173601.489001Z/fixture_attempt.json), [events.jsonl](fixture_20261009T025921.171236Z/runner_uv_m3_20261009T173601.489001Z/events.jsonl), [output manifest](fixture_20261009T025921.171236Z/runner_uv_outputs/m3_20261009T173609.612844Z/manifest.json) |

These newer attempts are the MAESTRO-provided successes through the unchanged real CPU runner command (`nice -n 10 /opt/homebrew/bin/timeout -k 30 <cap> uv run --script <notebook> ...`). Their event files match the attempt closeouts. The older `m2_runner_uv_headless.txt` / `m3_runner_uv_headless.txt` are prior DNS-failed attempts and remain untouched. The successful manifests retain the original `33e5aa4e…` prereg identity and old step-2 cap; their evidence establishes the notebook/runtime path before this amendment. They have not been reinterpreted as amended production runs or reused as an amended harvest. The fixture harness explicitly stubs dispatch admission, process sampling and diagnostic root, so live admission/watchdog/niceness and scientific calibration are **UNVERIFIED**.

**Review and scope.** GPT-6-Astra (high) returned **GO**, no blocking implementation findings: [astra_implementation_review.md](dml2_impl_20261009T174802.238815Z/astra_implementation_review.md). All changed source lines are in five files: the four production files above and `mathlab/test_mathlab.py`. As these MathLab build files are still untracked, [implementation.diff](dml2_impl_20261009T174802.238815Z/implementation.diff) compares saved pre-edit bytes with final source; empty ordinary git diff is not used as evidence of no change. Protected-file hashes (171 files, including prereg, event module, engine Python sources, harness, CORPUS, runbook/checkpoint and the cited prior evidence) remained identical: [initial_hashes.json](dml2_impl_20261009T174802.238815Z/initial_hashes.json); final audit is [final_verification.json](dml2_impl_20261009T174802.238815Z/final_verification.json). Existing other-owner worktree changes were left intact. No GPU/MPS, model load, harvest dispatch, commits, dashboard restart or package installation occurred.

This acceptance verification emits shared events at [dml2_build_acceptance_20261009T175517.460160Z/events.jsonl](runs/dml2_build_acceptance_20261009T175517.460160Z/events.jsonl), titled “D-ML-2 implementation acceptance; CPU fixture/tooling evidence only”; the shared event fold reports PASS. `tools/mathlab_events.py` is unchanged. Evidence inventory: [acceptance_evidence.json](dml2_impl_20261009T174802.238815Z/acceptance_evidence.json). Earlier report text is preserved except the explicitly authorized Status line update.
