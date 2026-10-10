**BINDING CONTEXT RULE:** Watch “Context N% left”. Before approximately 20%, stop starting new work, write a handoff in the task report covering done / in flight / exact paths / next step / risks, and say so in the reply so MAESTRO can start a fresh successor. Every handoff must restate this rule. This note is the requested session checkpoint.

# Codex ML handoff — 2026-10-09

**Operator stop honored:** NEW1 DRAFT v2 fold is complete. Supervisor/computation build work is stopped; implementation exists but build closeout is incomplete. No real NEW1 geometry was run. No commits or service/dashboard restarts. Resume build work only on a fresh operator instruction; real geometry requires separate authorization and review/freeze.

Workspace: `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a`. Verified branch: `worktree-c10k-route-a`. Other builders share this checkout; preserve their changes. Commands below are receipts or successor instructions, not work launched after the stop directive. After the interrupt, only the already-running shared-test process was collected; subsequent work read documentation/evidence and wrote this handoff.

## Completed: MathLab dashboard and shared event contract

Report: `results/mathlab_staging/observability_report.md`, SHA-256 `bc96fba2eddc1a4a627dcd6d3c10fb55bbc741a690f004955803932318e0db20`.

| Source | Current SHA-256 |
|---|---|
| `tools/mathlab_events.py` | `1c0780d42e3cfd794b68ba742fedb0307c2992bd737507cda65bdd8a864d27a5` |
| `tools/dashboard_mathlab.py` | `ba5235dd5ffd13af7f7c04e58dc0fd8b8f76302fc40a89c0247fb52114297fc7` |

`events.jsonl` is the sole run-state authority, consumed by `read_events()` and the shared pure `fold()`. The dashboard derives waiting reasons from live GPU/job/probe facts, disk presence and the prereg status line. Failed/empty process inventories mean unavailable, never GPU-free. The shared detector recognizes `mathlab_harvest.py`.

The Astra five-blocker fix preserved calibration PASS/FAIL/INVALID, restricted cheap-stop prose to actual aggregate FAIL in its step-3 scope, interpreted producer-shaped context/law3/law5/observer-parity and stage-specific budget/memory gates, and separated admission completion from experiment completion. Layout reserves section space, pins the MATH-PROXY disclaimer, shows failures first and summarizes/paginates checks with thresholds. Run-selection policy and other-active-run count are visible. Builder-sized 63-check streams and the actual CLI were rendered at 110×40.

Producer-side requests are staged in `results/mathlab_staging/producer_changes_for_mb.md`; this task did not apply them to MB's files. The dashboard report records the original RED and final 53 dashboard / 27 live-dashboard passing checks, plus the 110×40 renders. Historical commands:

```sh
/usr/bin/python3 -B -m unittest tools/test_dashboard_mathlab.py -v
/usr/bin/python3 -B -m unittest tools/test_dashboard_live.py -v
/usr/bin/python3 -B tools/dashboard_mathlab.py --once 110 40
```

Original fix proof directory: `/private/tmp/mathlab-astra-fix-ko6gcs3_`; the durable report embeds the renders. Current broader isolated shared checks also passed, as recorded below.

## Completed: LabViz integration and both follow-up fixes

Report: `results/mathlab_staging/labviz_integration_report.md`, SHA-256 `a1f6bd4b6f1e9d9535fa103ce794d60fa338a9e06487ba9cf9fe2d867d402655`. Read its dated closeouts: the initial report status retains historical failures that were subsequently fixed.

| Source | Current SHA-256 |
|---|---|
| `tools/labviz/cards.py` | `4eb680cead0b2eedfd452f223accf2b7365d8885ea9a651d7e542a4455089133` |
| `tools/labviz/build.py` | `b6ad3c4f9dcfee1d328ada41b2402335eb71c50f6116535814fa84b39db0c68d` |
| `tools/labviz/app.js` | `d4a3c3704c10f92d4c9ba40347018e883ca7cc845142f1b67c9d0df59db9a15b` |

Additional owned paths: `tools/labviz/test_mathlab.py`, `test_mathlab.cjs`, `test_labviz.py`, `README.md`; label/context-table edits and citations are detailed in the report and `docs/LABVIZ_V2_SPEC.md`.

Integration consumes only shared `read_events()` + `fold()` and shows runs, stages, gates, halts, resources, staged findings and parse errors. Every MathLab route retains **MATH-PROXY / math estimate, not evidence**; candidate questions are ideas to test. There is no score/evidence promotion. Tests cover torn final lines, halted/empty runs and source-bound snapshots.

The stale tables were fixed against sources, preserving assertions: the live step-6 label is exactly `INVALID-CONTROLS`, with CORPUS/58 cited for its `INVALID-CONTROLS-UNDERFIT` erratum wording. The genuine 55th context is C10X; registry/spec/table counts and source citations were updated consistently. Do not rewrite the live raw label to the erratum.

Astra R1 fixes exclude **both** `results/mathlab_staging/**` and `results/mathlab/**` from generic JSON/log/label/scale ingestion. Actual harvest manifest/admission/launch-log/terminal layouts are fixture-covered. **Do not add RECONSTRUCTED to the verdict table.** The warm build refreshes index/chunks/cards/cited evidence together and retires obsolete generated MathLab outputs. Capture accepts shared parsing plus bytes/SHA only when source bytes agree before/after reading, retries at most three times, and fails visibly if unstable. Later appends produce an older coherent snapshot, not contradictory card/mirror state.

Final historical verification: **79/79 Python, 111/111 Node, live build, seven-card snapshot verification and real generated harvest rendering PASS**. The generated site then contained 2,350 cards / seven MathLab cards. The harvest card `run-33210915fe8228a8` showed terminal PASS, three mint-norm FAIL gates (all 15 layer norm checks failed), zero of three mint arms replay-eligible, the staged finding and the proxy boundary. Step-2 running status was correct **at that publication cut**, not a claim about today's live state. Browser geometry remains UNVERIFIED.

```sh
.venv/bin/python -B -m unittest tools.labviz.test_labviz tools.labviz.test_mathlab
node --test tools/labviz/test_*.cjs
.venv/bin/python -B tools/labviz/build.py
```

Durable proof: `results/mathlab_staging/labviz_astra_r1_fix_evidence_20261009/`. Its `artifact_sha256_manifest.json` SHA is `30dcf53031d2e5a5100ef53014a68845b9726d5e29710d1cdd3778ba87d62c3e`; `publication_inventory.json` records generated snapshots. Harvest event SHA at publication was `18c415e06af4a14afe30000ffea65fc6fcf41168d2127512723ce038c283a3b7`. The report records concurrent producer/prereg/test changes; do not revert them or claim the whole checkout stayed unchanged.

## Completed: NEW1 DRAFT v1 → DRAFT v2 fold

Current document: `docs/NEW1_ADAPTER_GEOMETRY_PREREG.md`, **DRAFT v2 / NOT FROZEN / real geometry NOT RUN**, SHA-256 `ec6e2e65720fe39ae18a40cbfbd5188df99ea76187557181422c227e1d801236`.

Original delivered v1 SHA: `de909d2e046edf3db634d3019c44962c8b26f746ca1c54255ed354929e6104cd`. Pre-fold snapshot: `results/mathlab_staging/new1_v2_build_evidence/prereg_v1_before_fold.md`. V1 metadata-only proof/checkpoint: `/private/tmp/new1-prereg-ux4bb37p/`; current durable evidence is preferable to depending on tmp retention.

Astra source `results/mathlab_staging/new1_prereg_astra_r1.md` was read in full. Its exact B1 quoted replacement is verbatim in §6. All requested advisories are folded: harvest-1-only identity, descriptive M16 truncation with retained energy/effective rank/covariance fractions and boundary rule, secondary spectrum-matched orientation controls, removal of the undefined random-like veto, retained budget-UNVERIFIED disclosure. §9 contains the item → FOLDED/verbatim log. Secondary analyses never replace primary endpoints or the flat-spectrum q95 baseline.

The prereg pins 20 inputs/provenance records, layers 4–8, seed-0 rank-16 adapters, exact statistics/validity cutoffs and predictions before geometry. S-3 locality and held-out generalization remain separate; offline weight geometry establishes neither behavioral axis or F1 readiness. No queue action is currently eligible without calibration/prospective utility.

Important immutable identities:

| Input | Identity |
|---|---|
| Oracle adapters | `results/c10w_oracle/p1_20261007T223707_598959Z/adapters/*_s0_r16.safetensors`; every exact SHA is in prereg §2 and worker pins |
| Harvest 1 A7 fp32 pre-cast update | `results/mathlab/harvest_20261009T184950.056951Z/inloop_A7_coined_coined.pt`; SHA `abb882982f406ddd5d6536529ce49dee8f31ad3b3243495e93687266e7c6582f`; only `l4.upd_precast` … `l8.upd_precast` |
| Harvest 1 manifest | Same directory, `manifest.json`; SHA `bb9a6f9ad76678ae2289151c9fa64fb0033a6b8b2d7aff0b9a03150180f1ba7e` |
| Historical harvest-1 parent prereg | SHA `4852d1a229e186c1d054c6f1849f3c130f333738aa9dfc297bedac8cd44ad507` |
| Later observed parent prereg | `docs/MATHLAB_PREREG.md`; SHA `85b389ec92248dbccf61d4ecc1de65f47bedf5ce99f88f17866f0db29d3e4bf8` — concurrent advancement, not a reason to repin harvest 1 |

Never combine harvest identities/admissions/tensors/source maps or substitute a fresh solve/weight subtraction. Covariance paths are shared absolute/symlinked operands; use the complete exact inventory in §2. No pinned numerical payload was decoded for this work. The final static receipt confirms B1 verbatim, 20 pins and ten protected files byte-identical.

## In flight at interruption: NEW1 supervisor/computation implementation

**Started and implemented; closeout incomplete.** These files exist; do not describe them as “not started” or claim final build acceptance:

| File | Current SHA-256 |
|---|---|
| `tools/new1_supervisor.py` | `1fe8bac6c86a3cc92b4b62f318d92513c8eee35af467c90b7917b19b2bcaf4b4` |
| `tools/new1_geometry.py` | `505660836864bb754025379269c178be0b64f86037998da204035f966121354c` |
| `tests/test_new1_supervisor.py` | `eaf523ad6d02f00fb0ed7904583e8808a532341b788a46c4cf70e9f4136bc866` |
| `tests/test_new1_geometry.py` | `979a72695715342f87eb48fce4445173e166cad6fcb4ffc4ba530318eaaa69e1` |

`results/mathlab_staging/new1_v2_build_report.md` is an **unfinished scaffold**, SHA `d290823dfe86294e0e6d01879bd0bb881b1cafaae3c173b9b6f8f78e1f28cb14`. This handoff supersedes its incomplete status; the final report/evidence closeout was interrupted. No tool session or review agent remains running.

Implemented supervisor: stdlib boundary before imports; same-PID CPU admission/stop-policy checks; immutable 1,800-s deadline; worker-family RSS >6 GiB / available <6 GiB / monitoring failure kill/refusal; explicit phase reserve allowlist; SVD requires 8+5=13 GiB and waits at most 300 s within the deadline. Bounded vm_stat/ps probes and a periodic SIGALRM watchdog cover blocked admission/persistence. Observed breach kills the worker process group before recording diagnostics, with cleanup avoiding a second stale group kill. Monitoring is periodic observation, not a promise to catch every transient peak.

Private inherited Unix-socket handshake prevents bare-env/direct-worker numerical execution. Artifacts and parent directory are fsynced before referenced gates/events. Supervisor alone emits shared MathLab events. INVALID is represented as an INVALID stage, not a false Boolean FAIL/calibration gate. CLI refuses DRAFT before dispatch; only `--help` was used against the real CLI. CPU-only/nice/thread limits are configured; no real supervisor geometry launch occurred.

Implemented worker: producer-shaped manifest/source/order/revision/gate validation; before/after identity checks; CPU weights-only mmap loading; one covariance decomposition per layer; blocked validity checks; primary covariance energy/rank/overlap/angle/cosine/norm statistics; M16 and both seeded random control families; all-layer frozen prediction logic. Complement checks cover all families, and random controls include per-draw statistics and mean/q95 summaries. Factor/source artifacts are persisted before statistics/gates. Tiny synthetic fixture arithmetic used existing torch/numpy; no real matrices, model or GPU were run. Full-size time/RSS feasibility and real-input end-to-end dispatch remain **UNVERIFIED**.

Build review artifacts:

- `results/mathlab_staging/new1_v2_build_design_review.md`, SHA `307071c20c1547ca055ed26b4110dc3eaf07448f2aba9171027763be1eaf1819`.
- `results/mathlab_staging/new1_v2_build_final_review.md`, SHA `4df63f4ba8374a165b4370acba5329ddf2dece90defdeb080eb6a44330b8cbe2`. Initial four blockers were fixed regression-first: real gate-dict schema, watchdog during blocking operations, all-family complement checks, complete random summaries. Appended bounded delta review says PROCEED **for build delivery only**.

Claude auth probe returned `loggedIn=false`; reviews used independent same-family agents, with weaker independence. Reviews did not certify full-size execution.

## Exact test/evidence state

Directory: `results/mathlab_staging/new1_v2_build_evidence/`.

| Receipt | Result |
|---|---|
| `red_new1_tests.txt`, `red_new1_tests_updated.txt`, `red_geometry_extended.txt` | Missing implementation RED: 34, 36, then 20 geometry cases |
| `green_attempt1.txt` | 39 PASS |
| `red_integration_edge.txt` → `green_new1_tests.txt` | Breach-before-persistence regression: 42 tests / one error → 42 PASS |
| `red_review_blockers.txt` | 46 tests, two failures / two errors before blocker fixes |
| `green_review_fixes.txt` | Historical failed intermediate: two cleanup errors before stale-group-kill repair; filename is not a PASS claim |
| `green_full_tests.txt` | **46 tests, 2.556 s, OK**, current NEW1 source |
| `green_shared_mathlab_tests.txt` | **FAILED: 205 tests, 6.776 s, two failures / one error**; misleading filename retained as evidence |
| `green_stdlib_dashboard_tests.txt` | **127 tests, 3.087 s, OK**, isolated fresh process; already-running command collected after interrupt |
| `live_metadata_check.json` | Actual harvest-1 metadata contract PASS; numeric imports false, tensor payloads decoded false, geometry run false |
| `final_static_check.json`, `protected_before.json`, `protected_after.json` | B1 exact, 20 pins, ten protected files unchanged, no real geometry/commits |

Commands that produced those final receipts:

```sh
# NEW1 fixture suite: PASS, 46 tests
.venv/bin/python -B -m unittest discover -s tests -v

# Combined shared run: FAILED, 205 tests; do not present as green
.venv/bin/python -B -m unittest mathlab.test_mathlab mathlab.test_index tools.test_dashboard_mathlab tools.test_dashboard_live tools.test_c10w_p2_gate tools.test_dashboard_gpu_detector -v

# Correctly isolated stdlib shared run: PASS, 127 tests
.venv/bin/python -B -m unittest tools.test_dashboard_mathlab tools.test_dashboard_live tools.test_c10w_p2_gate tools.test_dashboard_gpu_detector -v
```

The combined run's error is `mathlab.test_index`: `.venv` cannot import `duckdb`. Its two GPU-detector failures assert torch is absent from `sys.modules`; the earlier numerical module in the same process had imported torch. Both assertions pass in the separate stdlib process. **Do not weaken these assertions.** The isolated numerical/provenance rerun remains outstanding; the combined log lists no other failures, but this is not a full isolated PASS receipt.

A cheap read-only provisioning probe found an existing DuckDB cache at `/Users/robertrhu/.cache/uv/archive-v0/waLE3HFo0DjN44MZ/duckdb`. Interpreter/ABI compatibility was **not checked** before the stop. No install was attempted. Check compatible existing provisioning before claiming unavailable; do not perform a global or network install without applicable authorization.

## Next steps for a fresh successor, after operator resumes build

1. Read this note, current AGENTS/context directive, DRAFT v2, the full Astra review and both build reviews. Verify cwd/branch and current source hashes; preserve concurrent changes. Use `PATH=/opt/homebrew/bin:$PATH rtk proxy ...` for shell commands. Do not rerun completed LabViz work to fill time.
2. Inspect the actual supervisor/worker/tests and resolve only concrete remaining build gaps. A real stub-grandchild process-group termination fixture is not yet independently verified; existing direct-worker group fixtures and source inspection do not prove that case. Cover this with tiny synthetic subprocesses if resuming build verification.
3. Finish isolated shared numerical/provenance checks. Validate the existing DuckDB cache/interpreter ABI and use compatible existing dependencies. Keep torch-using tests and stdlib forbidden-import tests in separate processes. Preserve all original assertions and report any remaining failure honestly.
4. Finish `new1_v2_build_report.md`: record RED/GREEN/failed intermediate logs, final counts/commands, weaker review independence, metadata-only live check, exact source SHAs, protected audit and every UNVERIFIED boundary. Seal or inventory the evidence packet; this handoff does not claim it is sealed. Read back durable writes.
5. Deliver build acceptance only after those checks/closeout. The CLI must continue to reject DRAFT. Review/freeze plus separate operator authorization precede **any** real adapter/covariance/harvest geometry. Do not run a full-shape probe as an incidental build test.

## Traps and evidence boundaries

- **Ownership:** do not edit `mathlab/*`, MB's admission/runtime/CPU runner/harvest/launcher/notebooks, the parent MathLab prereg, or shared/dashboard sources to accommodate NEW1. Read their live contract and stage producer requests instead. Dashboard remains under its own review ownership.
- **Fail closed:** denied/empty ps means unavailable, never GPU idle; broken monitoring is refusal. Preserve same-PID admission semantics and a watchdog independent of blocking I/O. Killing before durability is essential on breach; persist-before-gate still governs normal records.
- **Budgets:** 79 s / 4.6 GiB covariance-SVD references are one-sample/synthetic measurements, not complete NEW1 feasibility. Additive 5-GiB SVD reserve requires 13 GiB available. Do not raise the fixed deadline/RSS caps or treat missing layers as FAIL.
- **Science:** harvest is later than the P1 scoring process; its PASS is operand-harvest completion, not mint admission or predictive evidence. Actual solve uses the AlphaEdit P projection; closed-form excluded-energy behavior can be structurally forced. Do not call it a new causal discovery about a nominal ridge solve.
- **Frozen endpoints:** all five layers must be valid; no favorable subset. Secondary M16/spectrum null cannot rescue or replace primary results. Fixed q95 is the 19th of 20 draws. A run-finished PASS denotes execution completion; per-prediction scientific outcomes remain separate.
- **Publication:** LabViz index/chunks/evidence are derived coherent snapshots of accepted event bytes. Recorded step-2 “running” is historical; do not hand-copy it into UI prose or claim it is current without observing the sole event source.
- **Verification:** fixture PASS proves fixture behavior only. Full-size memory/time, real-input computation, calibration/prospective queue utility, browser geometry and F1 closure remain UNVERIFIED. No NEW1 geometry, inference/training, GPU job or queue promotion happened.
- **Logs:** failed `assertNotIn('torch', sys.modules)` output is enormous. Read bounded lines/summary markers rather than dumping the full module dictionary. Historical files named `green_*` may contain failures; trust their actual exit/result.

**Stopped for context handoff.** No further build, testing, geometry, commits or restarts are authorized by this checkpoint.
