# NEW-1 identity diagnostic — predeclared scope (D-NEW1-b, MB4)

**BUILD ONLY; real diagnostic NOT RUN.** Frozen arithmetic and interpretation below are predeclared before any real diagnostic normalization, decomposition or probe comparison. Operator authorization: `results/mathlab_staging/new1_b_identity_diag_authorization.md` (2026-10-10T05:56Z); Astra design: `results/mathlab_staging/new1_b_halt_astra.md`, option (a). Diagnostic permission is not NEW-1 launch permission. MAESTRO3 launches this diagnostic only after review. No retry, adapter energies, prediction verdict, tolerance amendment or dense tensor persistence. This tests one blocking provenance hypothesis relevant to F1, not the in-weight memory or locality contract.

## Arithmetic paths and native capture recipe

Use only the pinned **L4** moment cache and pinned historical capture/manifest listed below. Raw `mom2.mom2` must be finite square CPU-compatible NumPy float32; `mom2.count` must be positive scalar NumPy int64. No centering or new covariance normalization precision.

- **A — NEW1 arithmetic:** `torch.from_numpy(np.divide(moment, count, dtype=np.float32))`, exactly `tools/new1_geometry.py:138–147`.
- **B — producer arithmetic:** `torch.from_numpy(moment) / int(count)`, exactly the loaded-state combination of `SecondMoment.load_state_dict` and `moment` at `memit_dry_run/memit/util/runningstats.py:499–511`. Importing the engine/model package is unnecessary; this reproduces those two operations directly. Neither path mutates the raw moment.

Before decompositions, record row-major normalized-C byte SHA-256 for A and B (reuse `new1_geometry.tensor_sha`) and blocked float64 `max(abs(A-B))` on the exact fp32 normalized values. There are **at most two** native decompositions, in order **A then B**, one per path, even if the normalized hashes agree. Each uses `torch.linalg.svd(C, full_matrices=False)` on **CPU fp32**, excludes `S >= 0.005`, selects `idx=(S < 0.005).nonzero(as_tuple=True)[0]`, and constructs `P=U[:,idx] @ U[:,idx].T` in fp32, matching `experiments/track_c/c10e_bandknob.py:166–175`. Release each dense decomposition/projector before the next path; never retain or serialize dense tensors. No float64 SVD or geometric/update-energy calculation.

For every path, record excluded count, allowed count, projector byte SHA-256, captured count/hash agreement, and **every** seeded probe even on exact projector hash agreement. Probes are CPU fp32 `P @ torch.randn(d, generator=torch.Generator().manual_seed(j))`, `j=0,1,2,3`, as in `tools/mathlab_harvest.py:52–67` at commit **6ea8e7c** (historical full-source SHA `9dbc58afef1aa290d5e01622d3324b052e3f19169bfeb8d38ad19148cfe869bb`). Compare each with captured `l4.Pi_probe{j}` using `||actual.double()-captured.double()||2 / ||captured.double()||2`, retaining absolute L2 residual, maximum absolute coordinate residual, actual/reference L2 norms and `MATCH` iff relative error **<=1e-6**, otherwise `NO-MATCH`. Zero reference norm, nonfinite data, wrong dtype/shape, missing probes or invalid count/hash metadata abort as INVALID.

Record all four probes' threshold outcomes separately, their maximum relative error, and the unchanged native identity gate: allowed count agrees and (projector SHA agrees **or** all four probes agree at 1e-6). Equal counts or four probes do not certify equal subspaces or full operator distance. Probe discrepancies are sampled discrepancies only.

## Provenance, input pins and enforcement

Record torch version, `torch.get_num_threads()`, NumPy version, CPU/default SVD driver, `torch.__config__.show()` backend string (including reported MKL/Accelerate/OpenMP build information), own/worker nice values, source/input/scope/code SHA-256s, and captured torch-version metadata if present. Historical capture thread count is **UNKNOWN**; do not infer it.

| Input used | Required SHA-256, imported from `new1_geometry.PINNED` |
|---|---|
| `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/covariance_caches/Qwen_Qwen2.5-3B/wikipedia_stats/model.layers.4.mlp.down_proj_float32_mom2_t100_100000.npz` | `f6ae787454e5bae9eff52155ac699386351246b03e60ab68d728335b0c9a5b58` |
| `results/mathlab/harvest_20261009T184950.056951Z/manifest.json` | `bb9a6f9ad76678ae2289151c9fa64fb0033a6b8b2d7aff0b9a03150180f1ba7e` |
| `results/mathlab/harvest_20261009T184950.056951Z/inloop_A7_coined_coined.pt` | `abb882982f406ddd5d6536529ce49dee8f31ad3b3243495e93687266e7c6582f` |

| Source/authorization | Required SHA-256 |
|---|---|
| `tools/new1_geometry.py` | `018ce4d97f817ecd816a4fd3fb47316e78fda7007984449e93f423d0eb1f4a5e` |
| `tools/new1_supervisor.py` | `a69d410724b65a5dbacaf8e34fc45b73c9f545daf54eda9b6cfeb150e344557b` |
| `memit_dry_run/memit/util/runningstats.py` | `7b3a05de007733ec3243c13362d3c24b6cb9c09f32eedbcf36de02c98a49ac97` |
| `experiments/track_c/c10e_bandknob.py` | `1f6be5811d7e58f3ebda16867a4a174b1cf24d47f9a2514cf9c3f9d29f18e695` |
| `results/mathlab_staging/new1_b_identity_diag_authorization.md` | `daa41ea90df6a1ed1a73c4f03289f6f384dc97756f6b4ba93d4766535aad05c1` |
| `results/mathlab_staging/new1_b_halt_astra.md` | `9b4c5e90079bb52f7aef6824d2ace3fae292e6a0cf91d5ba62000589c5f2b5be` |

The historical harvest source is read from commit 6ea8e7c, with the full-source SHA above; no current harvest source is substituted. Launch also requires the final exact scope SHA and diagnostic-script SHA. Verify all pins before arithmetic; recheck each input's hash/stat identity around consumption via `new1_geometry.bound_input`. Every changed/missing input/source/scope/code pin produces a visible message and nonzero exit; no fallback. Only these three data inputs are used; no adapter files or update tensors are analyzed. Capture loading uses CPU `weights_only=True, mmap=True`; clone only L4 count/hash/four probes.

**Caps:** total deadline **600 s**, observed process-family RSS **11 GiB**, fixed **8 CPU threads**, parent and worker **nice 10**, CPU environment with CUDA visibility empty. A stdlib parent performs fresh shared `mathlab_admit.probe('cpu')` before any numerical import, then starts one isolated worker. A one-second parent watchdog samples its own process family RSS with a complete `/bin/ps` inventory and aborts above 11 GiB; denied, empty, malformed or incomplete inventories abort. The parent enforces the deadline while the worker is blocked in SVD, kills/reaps the isolated worker group on any abort, and never retries. Admission refusal cannot dispatch arithmetic. Deadline includes admission, pin checks, imports and all arithmetic; after an abort only bounded terminal error recording is permitted. The runtime caps/admission/nice/backend on real inputs remain **UNVERIFIED** by a fixture build.

**Disk:** diagnostic outputs total **strictly less than 1,000,000 bytes**, including all receipts. Exactly `result.json` plus `receipt.jsonl`, created exclusively in one fresh timestamped directory under `results/mathlab_staging/new1_identity_diag/`. Small scalar/provenance/probe reports only; no tensor outputs, logs, images or update summaries. Writer enforces the combined byte budget before each write; receipts include admission, lifecycle, bounded resource samples and terminal result binding. Failed diagnostics still write an INVALID scalar report where output IO permits and exit nonzero. Never reuse a directory.

## Predeclared interpretation

- **B matches; A does not:** if normalized bytes also differ and both used the recorded common thread/backend setup, normalization arithmetic explains reproducibility in this process configuration. The pair supports the normalization-path cause of the sampled identity halt; it does not prove historical runtime provenance, full subspace equality, projector fidelity, update leakage or behavioral locality. If normalized bytes are equal but SVD outcomes differ, this is numerical/runtime variation, not evidence for a normalization cause.
- **Neither matches:** cause remains OPEN. Normalization is not sufficient to reproduce the capture under this runtime. Thread/backend differences, SVD/cutoff sensitivity and other runtime-state confounds remain possible; do not change tolerance or replace capture.
- **Both match:** the sampled identity halt was not reproduced under this configuration; investigate original runtime state/provenance. This does not validate NEW-1 predictions or authorize a retry.
- **A matches; B does not:** producer-shaped division alone does not recover the historical capture here; investigate provenance/runtime/SVD variation. Do not choose a convenient arithmetic path as a repair from this outcome.

No outcome is a prediction verdict or a finding about adapter geometry. Real scalar results, thread/backend/runtime enforcement and outcome are **NOT RUN / UNVERIFIED** during this build.

## Build evidence and handoff

Build evidence: `results/mathlab_staging/new1_identity_diag_build_20261010T060316.539886Z/`. Initial scope is written before the tests and implementation. RED/GREEN receipts, exact build hashes, scope-preservation checks and launch command will be appended here after CPU fixture verification.

**BINDING context directive (operator 2026-10-09):** watch `Context N% left` in every root/team session; before approximately **20%**, stop starting new work, write done/in-flight/exact paths/next step/open risks into this scope doc, notify MAESTRO3 and request a fresh successor. Every handoff restates this rule; never approach full-window compaction.

### Enforcement clarifications frozen before real diagnostic execution

The RSS watchdog stops **at or above 11 GiB**. Computation, admission and pin checking retain the 600-second cap. After stopping the isolated worker, terminal error IO has its own **5-second** bound; kill/reap cleanup is separately bounded to **5 seconds**, with pipe closure on every exit including interruption. These cleanup bounds permit recording a halt, not further arithmetic or a retry.

The commit condition is **exit 0 plus a final `terminal` receipt with status `MEASURED` binding the exact `result.json` SHA**. A result file alone never commits the diagnostic. If failure occurs after result creation, preserve its original scalar bytes and append a **`halted`, `INVALID`, `result_committed:false`** receipt when IO permits; do not attempt an exclusive rewrite. A partial JSON or missing/mismatched/non-MEASURED terminal receipt is unaccepted. Disk budgeting reserves 8 KiB for error recording during nonterminal receipts; all actual files still total strictly below 1,000,000 bytes. Denied or blocked output IO yields a visible error and nonzero exit, never a successful run.

### MB4 final build closeout — CPU fixtures only

**NEW1 IDENTITY DIAG BUILD DONE; real diagnostic NOT RUN.** Final CPU verification: **122 tests PASS in 5.510 s** (27 diagnostic + 34 existing geometry + 61 existing supervisor; zero failures/errors/skips), command wall time 5.835 s. Exact command, exit code and frozen candidate hashes are in `results/mathlab_staging/new1_identity_diag_build_20261010T060316.539886Z/green_r3.json`; complete output is `green_r3.log`. Synthetic fixtures validate arithmetic, all-probe classification, pin refusal, admission refusal, disk limits, blocked-worker/admission deadline and RSS supervision, terminal-output failure, interruption and cleanup. They do not validate full-size native SVD resource use or real runtime admission.

RED first: `red.log` records 22 failures before the diagnostic implementation existed. Initial `green.log` records 22 passes but also leaked-pipe ResourceWarnings; that was not the accepted final build. `red_r2.log` records 5 failing regressions among 26 tests for pipe closure, output/commit failure, bounded terminal recording, interruption and inclusive 11-GiB rejection; `green_r2.log` then records 121 passes without the warning. The additional `red_r3.log` reproduces repeat cleanup masking the original error; `green_r3.log` records the final 122 passes without ResourceWarnings. RED receipts preserve before/after source identity; no implementation change was made during any RED execution.

| Frozen build artifact | SHA-256 |
|---|---|
| `tools/new1_identity_diag.py` | `93a7b317f8078c63c3c0d40d35fb419dfd24132a10577387af93c3790d461cb1` |
| `tests/test_new1_identity_diag.py` | `22bfcca9f90054b6ad9cd71d7ca4bf5f67738f8d6ee284d91b106bc946e5c699` |
| Original preimplementation scope, `scope_prebuild.md` | `547f577041e72baba462c0392befff7a29a4cdc7e40def905eb1664a4223d5a1` |
| Reviewed normative scope including enforcement clarifications, `scope_reviewed.md` | `dfabee181a135c6426f710de247d82fa9f174985e81c48b02bed59d7f055783d` |
| Unchanged NEW-1 preregistration | `1616c860c38b65acbabb7ec472a1233b30291337e86a7739271df0c4bd1c9d0f` |

The final scope hash includes this documentation-only appendix and is recorded in `results/mathlab_staging/new1_identity_diag_build_20261010T060316.539886Z/final_manifest.json` and `launch_command.txt`, avoiding a self-referential hash. The reviewed normative scope and original preimplementation scope remain exact byte prefixes. Source/input/historical pins above are unchanged; real input pin checking is deferred to the separately authorized launch. No real covariance was opened or diagnostic admission performed by the builder. No real output namespace was created, no dense tensors persisted, and no commits or deletions were performed by MB4.

Actual static review: `results/mathlab_staging/new1_identity_diag_build_20261010T060316.539886Z/astra_build_review.md`, **PROCEED — BUILD ONLY** on the exact code/test hashes above. The reviewer inspected the complete code, tests, scope and builder-run test receipts; it did not independently run tests or real inputs. Claude authentication was explicitly probed and returned `loggedIn:false`, `authMethod:none`; Astra provided the declared GPT-family fallback, with weaker family independence. The final scope changes after review only append build evidence and this handoff. No code/tests changed after that review.

Final scope audit compares all **545 protected files** with the build-start baseline; zero drift is required in `final_manifest.json`. This includes geometry/supervisor and their tests, NEW-1 preregistration/report, MathLab files, halt artifacts and `tools/test_dashboard_mathlab.py`. Concurrent unrelated git modifications and orchestrator HEAD changes are preserved; MB4 performed no git mutation. Full read-only git state is saved under this evidence directory.

**Handoff to MAESTRO3:** done — predeclared scope, bounded diagnostic, RED/GREEN CPU evidence, exact pins/hashes, reviewed candidate and launch handoff. In flight — none. Exact deliverables are `results/mathlab_staging/new1_identity_diag_scope.md`, `tools/new1_identity_diag.py`, `tests/test_new1_identity_diag.py`; evidence/review/launch/checkpoint are under `results/mathlab_staging/new1_identity_diag_build_20261010T060316.539886Z/`. Next — MAESTRO3 reviews the handoff and launches `launch_command.txt` once with fresh fail-closed admission; MB4 does not launch it. Open risks — real 600-s/11-GiB/nice-10/thread/backend enforcement and full-size numerical outcomes remain **NOT RUN / UNVERIFIED**; historical capture threads are UNKNOWN, and sampled probes cannot certify full operator equality. No diagnostic outcome authorizes a NEW-1 retry, amended tolerance, adapter-energy inspection or prediction verdict. Session context is saved locally in `results/mathlab_staging/new1_identity_diag_build_20261010T060316.539886Z/checkpoints/new1_identity_diag.md` within the authorized writable scope; no global memory or protected ledger was changed.

**BINDING context directive (operator 2026-10-09):** watch `Context N% left` in every root/team session; before approximately **20%**, stop starting new work, write done/in-flight/exact paths/next step/open risks into this scope doc, notify MAESTRO3 and request a fresh successor. Every handoff restates this rule; never approach full-window compaction.
