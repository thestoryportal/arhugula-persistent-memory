

## 2026-10-09 — Producer contract

Recorded UTC: 2026-10-09T18:18:22.837471+00:00. **Outcome: PASS.** Applied all four exact replacements in [producer_changes_for_mb.md](producer_changes_for_mb.md), approved as correct and sufficient by [dashboard_astra_r2.md](dashboard_astra_r2.md). No science gate, tolerance, threshold or budget changed.

| Contract change | Implementation | Integration evidence |
|---|---|---|
| Add `purpose="experiment"` to the end of `Run.__init__`; emit it on `run_started` | `tools/mathlab_runtime.py:141,158` | Actual producer → shared `emit` → `read_events` → `fold`; default experiment runs remain compatible |
| Attach only to one matching experiment start, with omitted-purpose legacy default; retain stage/terminal reuse rejection | `tools/mathlab_runtime.py:149–153` | An explicit admission receipt without a stage or closeout refuses attachment; explicit experiment and legacy starts attach without changing their event bytes |
| Standalone receipt uses `purpose="admission"`; launcher-owned run uses `"experiment"` | `tools/mathlab_admit.py:112–113` | Standalone **cpu and harvest** checks emit admission purpose and leave **all four experiment steps not started** under real `fold()` |
| Preserve admission receipt closeout and dispatched experiment lifecycle | `tools/mathlab_admit.py:133` unchanged | Launcher-owned **cpu and harvest** runs attach, keep one `run_started`, and remain running after stage completion; only experiment `run_finished` completes the step |

Added three integration tests in `mathlab/test_mathlab.py` and extended the existing probe-failure test to verify admission purpose and unstarted steps on a refused check. Admission probes are stubbed; event writing, parsing, folding, attachment and lifecycle are real. All fixtures use isolated temporary roots, and none dispatches a harvest or model.

**Test-first:** test edits preceded production edits. Four targeted tests showed **6 assertion failures RED** for missing purpose fields and incorrectly allowed receipt attachment. After the exact producer patch, the same **4 tests PASS GREEN**. Full outputs: [tests_red.txt](producer_contract_20261009T181053.740818Z/tests_red.txt) and [tests_green_targeted.txt](producer_contract_20261009T181053.740818Z/tests_green_targeted.txt).

| Requested check | Result | Full output |
|---|---|---|
| Full mathlab CPU/fixture suite | **65 tests PASS**, exit 0 | [tests_green_full.txt](producer_contract_20261009T181053.740818Z/tests_green_full.txt) |
| `tools/test_dashboard_mathlab.py` suite | **53 tests PASS**, exit 0 | [dashboard_green.txt](producer_contract_20261009T181053.740818Z/dashboard_green.txt) |
| Real DuckDB index test | **1 test PASS**, exit 0 | [index_green.txt](producer_contract_20261009T181053.740818Z/index_green.txt) |
| Both notebooks, marimo `check --strict` | **PASS**, exit 0, no diagnostics | [marimo_check.txt](producer_contract_20261009T181053.740818Z/marimo_check.txt) |

Exact check commands:

~~~sh
/opt/homebrew/bin/rtk proxy env LLMDB_DEVICE=cpu CUDA_VISIBLE_DEVICES= OMP_NUM_THREADS=8 MKL_NUM_THREADS=8 .venv/bin/python -B -m unittest mathlab.test_mathlab -v
/opt/homebrew/bin/rtk proxy env TMPDIR=/private/tmp PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B -m unittest tools.test_dashboard_mathlab -v
/opt/homebrew/bin/rtk proxy /private/tmp/mathlab_uv_cache/environments-v2/m2-solve-repro-da15e0fd897e5e61/bin/python -B -m unittest mathlab.test_index -v
/opt/homebrew/bin/rtk proxy env LLMDB_DEVICE=cpu CUDA_VISIBLE_DEVICES= PYTHONDONTWRITEBYTECODE=1 /private/tmp/mathlab_uv_cache/environments-v2/m2-solve-repro-da15e0fd897e5e61/bin/python -B -m marimo check --strict mathlab/m2_solve_repro.py mathlab/m3_calibration.py
~~~

Checks used the existing environments (torch 2.8.0, marimo 0.25.1, DuckDB 1.5.6); no dependency installation. Metadata: [check_environment.json](producer_contract_20261009T181053.740818Z/check_environment.json). Structured command/exit records: [validation_results.json](producer_contract_20261009T181053.740818Z/validation_results.json).

GPT-6-Astra (high) reviewed the implementation and tests: **GO**, no blocking findings; [astra_implementation_review.md](producer_contract_20261009T181053.740818Z/astra_implementation_review.md). A mechanical pre-edit/final-source comparison confirms the two production files contain exactly the four memo replacements, with no extra production edits: [pre_report_verification.json](producer_contract_20261009T181053.740818Z/pre_report_verification.json) and [implementation.diff](producer_contract_20261009T181053.740818Z/implementation.diff). The only other changed source is `mathlab/test_mathlab.py`. Snapshot diffs are used because these build files remain untracked.

The shared event module is unchanged and matches commit **8daf9ba**, SHA-256 `1c0780d42e3cfd794b68ba742fedb0307c2992bd737507cda65bdd8a864d27a5`. The frozen prereg hash remains `4852d1a229e186c1d054c6f1849f3c130f333738aa9dfc297bedac8cd44ad507`; exact verification is unchanged. All **141 protected files** (including core, engine/harness, notebooks, launchers, shared events/dashboard, prereg, CORPUS and canonical ledgers) retain their initial hashes. Final scope/report audit: [final_verification.json](producer_contract_20261009T181053.740818Z/final_verification.json). Earlier report bytes, including its accepted Status line and all D-ML-2 evidence, are preserved exactly. No GPU/MPS, model load, harvest dispatch, commits, dashboard restart or package installation occurred. These are CPU fixture/tooling checks; prior production-feasibility and live-runtime limitations remain as recorded above.
