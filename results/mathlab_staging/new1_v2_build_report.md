# NEW1 DRAFT v2 and CPU build — 2026-10-09

Scope: fold `results/mathlab_staging/new1_prereg_astra_r1.md` into `docs/NEW1_ADAPTER_GEOMETRY_PREREG.md`, build NEW1-specific supervisor and computation worker tests first. Real geometry NOT RUN; no GPU/model/engine import, commits, restarts or producer/shared-file edits authorized.

DRAFT v2 folds B1 verbatim, harvest 1 only, descriptive M16 and spectrum-matched random controls, removes the undefined random-like veto and retains complete-workload budget UNVERIFIED. Fold log is in prereg §9.

Build in flight. Intended owned files: `tools/new1_supervisor.py`, `tools/new1_geometry.py`, `tests/test_new1_supervisor.py`, `tests/test_new1_geometry.py`. Evidence: `results/mathlab_staging/new1_v2_build_evidence/`. Design review: `results/mathlab_staging/new1_v2_build_design_review.md`; Claude auth exit 1 loggedIn=false, so same-family fallback has weaker independence.

Context rule: watch Context N% left; before ~20%, stop starting new work, write done/in-flight/exact paths/next step/risks in this report, and say so for a fresh successor. Every handoff restates this rule.

## 2026-10-09 — Codex MB2 build closeout (D-NEW1-1)

**Status: NEW1 BUILD DONE · fixture checks PASS · Astra PROCEED FOR BUILD ONLY · real geometry NOT RUN.** This dated closeout supersedes the scaffold's historical “Build in flight” statement. The governing document is now **FROZEN v2**, SHA-256 `eaf7bc21e1ac2cabc5f16703ce5b712debfdad80163f170fe20c99969c024741`; its bytes were preserved. The frozen authorization covers the CPU build and small synthetic fixtures, with separate authorization still required for pinned-input geometry (`docs/NEW1_ADAPTER_GEOMETRY_PREREG.md:3,15–19,109–131`). Build delivery does not promote a claim, admit a GPU experiment, or close F1.

Read Codex ML's handoff, this scaffold, the frozen prereg, and the existing design/final reviews before changing the build. ML's previous receipts remain intact. MB2's fresh evidence namespace is `results/mathlab_staging/new1_v2_build_evidence/mb2_20261009_closeout/` (abbreviated **E/** below). No commits, real geometry, model execution, GPU/MPS work, full-shape probes, producer/shared-module edits, or canonical evidence/queue edits were performed.

### Enforcement repairs and retained contract

| Boundary | Final implementation and verification |
|---|---|
| Freeze and source identity before numerical imports | One stdlib verifier hashes exactly the bytes it parses and checks the authoritative first title/status paragraph. Historical “NOT FROZEN” prose cannot veto the frozen header, and quoted “FROZEN” prose cannot admit a draft. Both supervisor and worker use it (`tools/new1_supervisor.py:66–73,382–387`; `tools/new1_geometry.py:414–417`). Positive, draft, hash-mismatch, and pre-import boundary fixtures are in `tests/test_new1_supervisor.py:121–168`. The actual frozen document also passed the metadata-only verifier. |
| Fail-closed parent CPU admission | The existing MathLab CPU probe and stop policy remain decisive in the supervisor PID; refusal prevents worker dispatch (`tools/new1_supervisor.py:159–163,273–292`). Direct-worker and bare-environment bypasses remain refused by the private inherited-socket handshake. No real admission was treated as granted by these fixture receipts. |
| Heavy-cell reserves and waits | The fixed allowlist retains the 8-GiB base plus each declared reserve: covariance SVD requires **13 GiB**, imports 9, loads/checks/update SVD/projections 10, random controls/output 9. Each cell waits at most **300 s**, inside the unchanged **1,800-s** monotonic spending cap (`tools/new1_supervisor.py:24–30,171–175,203–220`). Fixtures exercise 12.9 versus 13 GiB, the 300-s wait, and deadline truncation. |
| Process-family RSS and emergency floor | Inventory includes PGID, verifies the worker's isolated group, and sums same-group members plus descendants, including reparented grandchildren. Missing/malformed/failed monitoring refuses. Observed worker-family RSS **>6 GiB** or available memory **<6 GiB** stops computation; equality remains allowed (`tools/new1_supervisor.py:124–154,176–201`). Thresholds use simulated resource values; no 6-GiB fixture allocation was made. Real tiny stub processes independently verify grandchild shutdown. |
| Whole-group teardown | Leader exit kills the isolated group before draining inherited IPC. Both top-poll and bottom EOF/exit schedules clean up exactly once; the kill receipt prevents stale second group kills (`tools/new1_supervisor.py:260–271,295–341`). Real IPC-holding-grandchild fixtures and a deterministic successful-exit race fixture cover both paths (`tests/test_new1_supervisor.py:323–361,380–397`). |
| Deadline through failure closeout | Reaping and halt persistence consume only the original remaining budget, after the worker group is stopped. A blocked halt write cannot add a fresh timeout. If closeout cannot finish, stderr preserves the original refusal and says **closeout incomplete / no prediction verdict**; no fabricated halt, finding, or successful-completion event is emitted (`tools/new1_supervisor.py:351–371`; fixture `tests/test_new1_supervisor.py:363–378`). Such a stream remains incomplete and requires review; it is not a successful or scientifically failed prediction. |
| Persist before gate; one state authority | Existing exclusive artifact writes flush/fsync the file and parent directory before referenced events. Supervisor emits through the unchanged `tools/mathlab_events.py`; resource/criteria/artifact/prediction receipts precede their events. INVALID predictions retain INVALID stages rather than false Boolean FAIL gates. Successful fixture streams fold through the shared reader without calibration promotion (`tools/new1_supervisor.py:76–91,194–218,232–251,309–350`). DuckDB remains a derived index; no production index was rebuilt. |

The worker's 20 operand/source pins, numerical helpers, controls, primary/secondary endpoints, and run body after the freeze guard are unchanged from ML's committed WIP. AST comparison and before/after hashes establish that boundary; `tests/test_new1_geometry.py` is byte-identical. Geometry fixtures remain small synthetic CPU arrays. The shared MathLab suite also uses an in-memory two-entry WordLevel tokenizer and recorded JSON metadata fixtures; no live model/tokenizer, engine runtime, or real geometry was executed.

### RED → GREEN receipts

| Receipt under E/ | Exact outcome |
|---|---|
| `mb2_red_supervisor.txt` | **RED**, 32 tests / 4.624 s, three failures and five errors, exit 1, before production changes. Reproduced frozen-footer rejection, draft acceptance, missing PGID schema/accounting, leader-exit IPC stall, and halt persistence extending an 80-ms cap to ≈2 s. |
| `mb2_green_new1_attempt1_FAILED.txt` | Historical failed intermediate: 55 tests / 2.784 s, one failure/one cleanup error, exit 1. A stale duplicate kill prevented reaping; the kill receipt and fixture cleanup were corrected. Retained as failure evidence. |
| `mb2_green_new1_before_delta_55.txt` | Historical GREEN: 55 tests / 2.837 s, exit 0. Subsequently strengthened by Astra's exit-race regression. |
| `mb2_red_exit_race.txt` | **RED**, one deterministic test / 0.014 s, exit 1: successful EOF/exit expected one group kill but observed zero. Recorded before the conditional bottom-branch cleanup. |
| `mb2_green_new1.txt` | **GREEN**, all **56 NEW1 tests / 2.915 s**, exit 0, final code. |
| `mb2_shared_stdlib.txt` | **GREEN**, **133 dashboard/CPU-detector tests / 3.950 s**, exit 0, fresh process. Existing file-handle ResourceWarnings are retained; they did not fail the suite. No shared assertions were weakened. |
| `mb2_shared_numeric_provenance_attempt1_FAILED.txt` | Historical provisioning failure: 78 tests / 5.828 s, one missing `tokenizers` dependency in the cached interpreter, exit 1. Retained; not claimed as PASS. |
| `mb2_shared_numeric_provenance.txt` | **GREEN**, **78 MathLab numerical/provenance tests / 4.339 s**, exit 0, separate fresh process using compatible existing local packages. DuckDB ABI passed a tiny in-memory `SELECT 1` probe. No dependency installation. |
| `mb2_final_static_audit.json` | **PASS**: eight protected files unchanged; 20 pins unchanged; numerical functions and post-guard run body unchanged; actual frozen SHA/header accepted; no numerical/model/tokenizer imports from importing the NEW1 entry modules. |

Final passing suites total **267 checks**. The inherited combined 205-test failure (`green_shared_mathlab_tests.txt`, two failures/one error) is preserved as historical evidence. Its missing DuckDB and same-process torch contamination are resolved by the isolated receipts above, without weakening the detector's no-torch assertion. Per-run argument vectors, exit codes, and the local-package search path are recorded in the corresponding `*_command.json` receipts. `mb2_build.diff` records the source/test delta; `mb2_git_state.json` captures the shared worktree state without changing git.

Exact underlying test commands, run with `TMPDIR=/private/tmp`, `LLMDB_DEVICE=cpu`, empty `CUDA_VISIBLE_DEVICES`, `OMP_NUM_THREADS=8`, `MKL_NUM_THREADS=8`, and `PYTHONDONTWRITEBYTECODE=1`:

```sh
.venv/bin/python -B -m unittest discover -s tests -p test_new1_supervisor.py -v
PYTHONPATH=tests .venv/bin/python -B -m unittest test_new1_supervisor.SupervisorTests.test_successful_exit_at_loop_bottom_still_terminates_group -v
.venv/bin/python -B -m unittest discover -s tests -v
.venv/bin/python -B -m unittest tools.test_dashboard_mathlab tools.test_dashboard_live tools.test_c10w_p2_gate tools.test_dashboard_gpu_detector -v
PYTHONPATH=/private/tmp/mathlab_uv_cache/environments-v2/m2-solve-repro-da15e0fd897e5e61/lib/python3.11/site-packages .venv/bin/python -B -m unittest mathlab.test_mathlab mathlab.test_index -v
```

### Review, exact future launch, and limits

Astra's actual source review is `E/astra_mb2_delta_review.md`: initial **FIX-FIRST** identified the successful EOF/exit teardown race; the appended final review is **PROCEED FOR BUILD ONLY**, after inspecting the conditional cleanup, deterministic RED and final 56-test GREEN. The reviewer ran no computation. This GPT-6-Astra review is same-family and has weaker independence; MAESTRO's Claude orchestration does not change that fact. ML's earlier Claude auth probe was `loggedIn=false`; no new external-auth claim is made.

**Recorded command only — NOT EXECUTED; requires separate real-run authorization and fresh fail-closed CPU admission.** The existing worktree interpreter's metadata is Python **3.11.16**, torch **2.8.0**, NumPy **2.4.6**, safetensors **0.8.0**. `tools/new1_supervisor.py --help` exited 0; no real supervisor launch occurred. The supervisor launches one CPU worker with `nice -n 10`, eight threads, and a fresh timestamped namespace.

```sh
cd /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a
/usr/bin/env PATH=/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin \
  TMPDIR=/private/tmp \
  LLMDB_ROOT=/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a \
  LLMDB_DEVICE=cpu CUDA_VISIBLE_DEVICES= OMP_NUM_THREADS=8 MKL_NUM_THREADS=8 \
  PYTHONDONTWRITEBYTECODE=1 \
  /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python -B \
  /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/new1_supervisor.py \
  --prereg-sha eaf7bc21e1ac2cabc5f16703ce5b712debfdad80163f170fe20c99969c024741
```

This command supplies no lead override. The parent CPU probe must refuse whenever its default admission cannot establish the required facts; a GPU-coexistence launch would need the applicable fresh lead record through the existing `--admission` interface. Build PASS does not establish live admission or authorize such a launch.

**Limits kept flush:** all resource/deadline proofs use small fixtures, simulated memory inventories, and injected short deadlines. Real pinned-input end-to-end dispatch, native full-workload timing/RSS, production I/O behavior, and complete-workload feasibility under 1,800 s / 6 GiB remain **NOT RUN / UNVERIFIED**. Sampling is at most one second plus bounded probe latency and cannot certify absence of intervening transient peaks. No prediction or queue action follows from these build receipts.

### Ownership and saved handoff

| NEW1 file | Final SHA-256 |
|---|---|
| `tools/new1_supervisor.py` | `b5fc97ab4cc15663fcae86f2971ddd5ac2129bce38c00d3a7c4ad2b6631d36fb` |
| `tools/new1_geometry.py` | `b63f1cc2fd34b6c46da6f42044943fb36c633bf0125cfa8c7c7ad5e590630a5a` |
| `tests/test_new1_supervisor.py` | `18cf073337682867dfb2187d2e42d395ba6ad11046f4d1876921c24f4e549e4e` |
| `tests/test_new1_geometry.py` (unchanged) | `979a72695715342f87eb48fce4445173e166cad6fcb4ffc4ba530318eaaa69e1` |

Protected sources: both preregs, `tools/mathlab_events.py`, `tools/mathlab_runtime.py`, `tools/mathlab_admit.py`, `tools/mathlab_harvest.py`, `mathlab/index.py`, and `tools/dashboard_mathlab.py`; complete before/after hashes are in `E/before_sha256.json` and `E/mb2_final_static_audit.json`. Other lanes' worktree changes were preserved. MB2 also completed the separately authorized `docs/MATHLAB_STEP4_PREREG.md` **DRAFT v2** fold: both formal BLOCKING paragraphs verbatim and all three ADVISORY items adapted with reasons. Its status remains contingent on step-3 harvest-2 PASS; FAIL or INVALID shelves that draft. It is not frozen or run.

**Handoff:** build and STEP4 v2 drafting are complete; no build work, tool session, or review is in flight. Exact files/evidence/launch command are above. Next action belongs to MAESTRO: review this build-only delivery; any real geometry requires a new explicit execution instruction and fresh admission. Do not infer execution permission from build acceptance, reuse a run namespace, silently raise caps, or promote MATH-PROXY output. A workspace-local context snapshot is saved under E/ for a successor. Findings learned here: read freeze authority from the pinned status paragraph, retain PGID accounting after reparenting, cover both exit-poll schedules, and never give halt persistence a new budget.

**Context rule, binding through every handoff:** watch Context N% left; before approximately **20%**, stop starting new work, write what is done / in flight / exact paths / next step / open risks into the task report, and say so for a fresh successor session. Every handoff restates this rule.

## 2026-10-09 — Fix round (independent review)

**Status: NEW1 FIX DONE · one implementation fix round · B1/B2/B3 RED → GREEN · real geometry NOT RUN · no commits.** Read `results/mathlab_staging/new1_build_astra_r1.md` fully; its independent **FIX-FIRST** verdict supersedes the earlier build-only review. This section reports author-run repairs and verification, not a post-fix independent approval or real-run authorization. Frozen v2 / D-NEW1-1 remains unchanged, SHA `eaf7bc21e1ac2cabc5f16703ce5b712debfdad80163f170fe20c99969c024741`.

Fresh evidence: `results/mathlab_staging/new1_v2_build_evidence/mb2_20261009_independent_fix_r1/` (**F/** below). The pre-fix source/test copies and hashes are in `F/before/` and `F/before_sha256.json`; production sources were verified unchanged before recording RED. Earlier closeout receipts and report sections are preserved as history.

| Review item | RED reproduction | Repair and GREEN evidence |
|---|---|---|
| **B1 — late 300-s admission** | A fake-clock memory probe finishes at **301 s** with 13 GiB and the old code grants admission. Separate resource/cell receipt fixtures advance the clock to 301 s; blocked probe/persistence fixtures hit the outer deadline instead of the cell deadline (`tests/test_new1_supervisor.py:70–130`). | Each cell now carries an absolute deadline. `remaining()` uses the earlier cell/whole-run budget; probes, persistence and the final grant recheck it. The existing supervisor alarm uses that dynamic remaining budget, so blocked resource probes are interrupted at the cell deadline. The cell deadline is cleared in `finally`, preserving the original budget for bounded halt closeout (`tools/new1_supervisor.py:95–126,177–241,285`). The maximum wait remains **300 s**, covariance-SVD admission **13 GiB**, and the total cap **1,800 s**. |
| **B2 — verdicts survived failed closeout** | Injected `finding.json` failure yields a halted stream with all four primary PASS/FAIL gates exposed. I/O failures after primary stage/gate writes, finding publication and terminal publication reproduce exposure; deadline fixtures interrupt the prediction receipt, stage/gate publication, finding write/event, and the terminal call. Stream-prefix checks also expose verdicts before completion (`tests/test_new1_supervisor.py:451–524`). | Prediction events explicitly declare their outcomes **provisional**. The shared pure `fold()` exposes NEW1 primary gates, prediction-stage outcomes and the finding only with successful `run_finished` PASS and no halt; a later halt removes their current visibility. Raw history remains available for diagnosis. The gate definition, schema, validator, emitter and reader are unchanged; this narrow NEW1 visibility guard also recognizes historical NEW1 streams (`tools/new1_supervisor.py:246–263`; `tools/mathlab_events.py:223–241`). A positive completed fixture still exposes H-COV FAIL and the other registered outcomes. Ordinary calibration/admission gates retain their previous visibility, including calibration FAIL after a halt. |
| **B3 — registered top/bottom contrasts missing** | The synthetic complete-layer and serialized-layer fixtures fail on absent `energy_minus_M` fields (`tests/test_new1_geometry.py:186–231`). | Each adapter/control row persists `energy_minus_M.top` and `.bottom`, each with **difference** and the respective **valid** flag. The primary D−M contrast is under `row.D.energy_minus_M`; other adapter arms retain their corresponding contrasts (`tools/new1_geometry.py:370–376`). The synthetic D top contrast is **1**, bottom contrast **−204/4900**; serialization preserves top-invalid/bottom-valid flags without turning the invalid bin into a valid statistic. Primary prediction rules remain unchanged. |
| **ADVISORY — whole-basis float64 promotion** | A 513×513 fp32 basis with two selected columns records a full 513×513 promotion. | `energy()` now selects each block of at most **256 covariance columns before** conversion to float64 (`tools/new1_geometry.py:109–124`). The fixture records exactly one **513×2** conversion and the same expected fraction **2/513** (`tests/test_new1_geometry.py:44–53`). No full-shape probe was run. |

The B2 fix necessarily changes the shared **derived visibility in `tools/mathlab_events.py::fold`**, in addition to the four NEW1 files. It preserves the event schema and append/flush/fsync emitter contract and changes no dashboard source, producer, pinned input, frozen prereg or other study's gate policy. The earlier eight-file protected-hash statement applies to the historical build closeout; this round deliberately includes `mathlab_events.py` in its changed-file audit. Source-hashed consumers must use the current reader when rebuilding derived views.

### Exact verification receipts

| Receipt under F/ | Result |
|---|---|
| `red_new1.txt`, `red_command.json` | **RED**, 66 tests / **5.965 s**, **20 failures / two errors**, exit **1**; production unchanged at dispatch. Subtest failures reproduce B1/B2; missing registered payloads reproduce B3; the allocation advisory has its own failing witness. |
| `green_new1.txt`, `green_command.json` | **GREEN**, all **66 tests / 6.991 s**, exit **0**, after the single fix round. |
| `green_shared_consumers.txt`, `shared_consumers_command.json` | **GREEN**, **150 tests / 26.407 s**, exit **0**, separate fresh process: shared event contract, teamdash/dashboard-live/CPU detector and LabViz MathLab consumers. Existing ResourceWarnings remain in the log; no shared assertions were weakened. |
| `final_static_audit.json` | **PASS**: seven remaining protected source/prereg files unchanged; formal review unchanged; all **20 pins** unchanged; frozen caps/reserves unchanged; every event-module AST node outside `fold()` unchanged; geometry functions outside the reviewed `energy()` / layer-output changes unchanged, including `run()` and primary predictions. Importing NEW1 entry modules still imports no numerical/model/tokenizer dependency before admission. |

Both NEW1 test modules were rerun together exactly as requested. Commands below ran with `TMPDIR=/private/tmp`, `LLMDB_DEVICE=cpu`, empty `CUDA_VISIBLE_DEVICES`, `OMP_NUM_THREADS=8`, `MKL_NUM_THREADS=8`, and `PYTHONDONTWRITEBYTECODE=1`; supervisor fixture roots are also explicitly under `/private/tmp`.

```sh
.venv/bin/python -B -m unittest tests.test_new1_supervisor tests.test_new1_geometry -v
.venv/bin/python -B -m unittest tools.test_dashboard_mathlab tools.test_dashboard_live tools.test_c10w_p2_gate tools.test_dashboard_gpu_detector tools.labviz.test_mathlab -v
```

The consumer run additionally used `PATH=/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin`. These are CPU/synthetic/static checks, **216 final passing tests**, not a real geometry or production admission receipt. Publication tests cover both unfinished streams and post-terminal I/O failure followed by a halt; deadline injection covers the steps leading to terminal publication. No empirical claim about full-workload/native production I/O is made.

| Changed file | Post-fix SHA-256 |
|---|---|
| `tools/new1_supervisor.py` | `5a7b8ea2a86c74d8d57946275ebe1c362a9013c1f89f715405ce1c57019a11e7` |
| `tools/new1_geometry.py` | `ca51ab89d3b2003107fc04da8c8297bb360c58b6751c514a93a5761a7d2e6523` |
| `tests/test_new1_supervisor.py` | `30d49c56add81a7df9696d6907b6f44f3999259bd2587140001890e8d8bf91d2` |
| `tests/test_new1_geometry.py` | `ad79af6e3db8aa6d2aad9b58b3306fa555876353c57fc20b567d5d8447db21eb` |
| `tools/mathlab_events.py` | `c14d3e6d58e3895573b0d7c4047d89252c43d050af4191350220c6529c623cab` |

**Limits:** no real adapters/covariance/harvest operands were used for geometry; no model/tokenizer/engine runtime, GPU/MPS, real admission, full-size SVD or production derived-index/dashboard build was run. No dependencies were installed. Real-input execution, full-workload timing/RSS and production I/O remain **NOT RUN / UNVERIFIED**. Numeric prediction rules, tier boundaries and queue gates are unchanged; STOPPED/refused/incomplete publication supplies no current prediction verdict. The recorded future launch command in the previous dated section retains its arguments and frozen SHA; it remains unexecuted and requires separate authorization and fresh admission.

**Handoff:** this requested fix round is complete; no test, review or implementation is in flight. Exact sources, receipts and limits are above; `F/context_20261009_independent_fix.md` preserves the workspace-local successor snapshot. MAESTRO owns any subsequent independent review or execution instruction. Preserve the independent r1 and every historical failed receipt; do not infer a post-fix FREEZE or execution permission from these GREEN fixtures. Other lanes' worktree changes were preserved. No commits or canonical evidence/ledger/runbook/checkpoint edits were made.

**Context rule, binding through every handoff:** watch Context N% left; before approximately **20%**, stop starting new work, write done / in-flight / exact paths / next step / open risks into the task report, and say so for a fresh successor session. Every handoff restates this rule.

## 2026-10-09 — Context handoff: NEW1 B2 OPEN (Astra r2)

**Status: FIX-FIRST · B2 NOT RESOLVED · B1/B3 RESOLVED per Astra r2 · shared-contract repair NOT STARTED · no new RED/GREEN run · real geometry NOT RUN · no commits.** This dated section supersedes the previous section's B2 completion claim. Read `results/mathlab_staging/new1_build_astra_r2.md` fully. The earlier 66 NEW1 / 150 shared-consumer GREEN receipts do not cover terminal durability and do not establish B2 acceptance.

Astra's controls expose the missing boundary: `tools/mathlab_events.py:132–134` writes the terminal line before fsync; `:232` accepts a readable PASS as committed. A terminal-fsync timeout returned **STOPPED-DEADLINE**, while `fold()` showed **finished/PASS, all four prediction verdicts and the finding**. Persistent terminal I/O failure combined with failed halt persistence produces the same false completion (`tools/new1_supervisor.py:363–380`). The existing terminal deadline fixture sleeps before append (`tests/test_new1_supervisor.py:510`) and cannot prove durability. B1's 300-s cell deadline, B3's persisted contrasts and the selected-column allocation advisory are resolved in r2.

**Next step for a fresh successor:** reproduce both actual append→fsync failure controls as RED before editing production, then implement the smallest shared event-publication protocol that requires durable terminal commitment. An uncommitted/torn terminal must fold as INCOMPLETE/INVALID, with no PASS, prediction verdicts or NEW1 finding; failed halt persistence must not be required to retract a false PASS. A commit-marker design is explicitly authorized, but merely moving the same readable-before-fsync race into its marker is insufficient. Preserve the pure fold / sole stream authority contract and backward compatibility: existing committed harvest, m2 and m3 streams must retain their recorded outcomes. No implementation design has been selected or applied in this request.

Exact repair surface: `tools/mathlab_events.py`, `tools/new1_supervisor.py`, `tests/test_new1_supervisor.py`, plus necessary shared-contract tests. Existing geometry sources/tests are `tools/new1_geometry.py` and `tests/test_new1_geometry.py`. Keep frozen `docs/NEW1_ADAPTER_GEOMETRY_PREREG.md` §6 byte-identical (SHA `eaf7bc21e1ac2cabc5f16703ce5b712debfdad80163f170fe20c99969c024741`): admission, 13-GiB pre-SVD, 300-s waits, 1,800-s total deadline, 6-GiB worker/floor limits, monitoring refusals and persist-before-gate semantics remain binding. Latest user authorization explicitly includes the **SHARED** contract; it supersedes the earlier narrow fold-only repair scope.

Rerun all requested modules: `tools.test_dashboard_mathlab`, `tools.labviz.test_mathlab`, `mathlab.test_mathlab`, `tests.test_new1_supervisor` and `tests.test_new1_geometry`. Use CPU/synthetic fixtures, `TMPDIR=/private/tmp`, a fresh evidence namespace, separate fresh processes for stdlib detector/consumer tests and numerical tests. Preserve r1/r2 reviews and every old failed receipt. No real geometry, model/engine runtime, GPU/MPS, full-shape probe, queue action, dependency installation or commit is authorized. Actual runtime feasibility remains UNVERIFIED.

No B2 implementation, test, tool session or review is in flight. Saved successor state, exact test commands, current source hashes and observed git state are in [handoff_codexmb2_new1_b2_20261009T232855Z.md](handoff_codexmb2_new1_b2_20261009T232855Z.md). Previous evidence remains at `results/mathlab_staging/new1_v2_build_evidence/mb2_20261009_independent_fix_r1/`. Worktree/root and branch were reverified; other lanes advanced HEAD to `c1091991544b1936b58bd5f1516b5576143b5de0`. Current `docs/MATHLAB_STEP4_PREREG.md:3` explicitly says **SHELVED** after step-3 calibration FAIL / Astra CONFIRM; do not resume step 4 from the older contingent-draft snapshot.

**Context rule, binding through every handoff:** watch **Context N% left**; before approximately **20%**, stop starting new work, write done / in-flight / exact paths / next step / open risks into the task report, and say so for a fresh successor session. Never approach full-window compaction. Every handoff restates this rule. This session has stopped new work and hands B2 to a fresh successor; do not report NEW1 B2 DONE.

## 2026-10-09 — MB3: NEW1 B2 terminal durability repair

**Status: NEW1 B2 DONE · test-first shared-contract repair · 222 final CPU/fixture tests PASS · Astra final delta PROCEED · real geometry NOT RUN · no commits.** This section closes the B2 implementation work left open in the preceding handoff. B1/B3 remain RESOLVED per `results/mathlab_staging/new1_build_astra_r2.md`; this repair adds no scientific acceptance or execution authorization. MathLab remains STOPPED after step-3 calibration FAIL / D-ML-4; NEW-1 remains the separate frozen D-NEW1-1 study. Frozen §6 is byte-identical: SHA-256 `eaf7bc21e1ac2cabc5f16703ce5b712debfdad80163f170fe20c99969c024741`.

Fresh receipts: `results/mathlab_staging/new1_v2_build_evidence/mb3_20261009T233356Z_b2/` (**G/** below). **G/ is a workspace symlink to `/private/tmp/new1_mb3_20261009T233356Z_b2_evidence/`.** The workspace volume hit ENOSPC during editing; sources were rechecked intact, and only MB3's new receipts were copied with matching hashes, then moved off that volume. Older MB2/Astra artifacts were preserved. The physical temporary directory must be retained or archived before system cleanup; the symlink alone is not an archive.

### Committed terminal contract

`tools/mathlab_events.py:145` retains schema 1 and the sole `events.jsonl` authority. All cooperating emitters take an exclusive lock on the stable run-directory inode, so an append cannot be lost during stream replacement. A terminal attempt first appends/fsyncs the outcome-free `run_finishing` event. It then copies the exact prior stream into a same-directory private file, rejects every short prefix/terminal write, appends `run_finished`, fsyncs that complete file, syncs the directory, and atomically replaces the public stream (`:160–197`). Prior bytes remain an identical prefix; the stream inode changes. No persistence operation follows the file-content commit point.

`fold()` clears outcome/finished time at `run_finishing` and treats an unmatched attempt as **invalid: no verdict / INVALID** (`tools/mathlab_events.py:280–282,323–327`). Existing NEW1 suppression removes provisional primary gates, prediction-stage outcomes, and the finding until a committed successful terminal; failed halt persistence is not needed to hide them (`:288–303`). A torn private terminal, refused terminal fsync, refused directory sync/replacement, malformed existing stream, or short prefix copy cannot expose a terminal outcome. Legacy committed terminals keep their meaning without requiring the new event; historical gate visibility remains unchanged.

The supervisor prepares the fsynced stream's device/inode/size identity before replacement and rechecks the existing deadline then (`tools/new1_supervisor.py:275–278,368–385`; `tools/mathlab_events.py:132–141`). If interruption lands after replacement but before Python returns, it compares that prepared identity with the public file and returns the already recorded outcome with an explicit postcommit diagnostic. This closes the success-return race without another persistence budget or derived outcome file. An actual precommit terminal-fsync timeout still returns STOPPED-DEADLINE and exposes no prediction verdict. Frozen admission, 13-GiB pre-SVD, 300-s waits, 1,800-s total deadline, 6-GiB limits, and Controller logic are unchanged.

**Durability boundary:** the committed terminal contains successfully fsynced file content when it becomes readable. Power-loss persistence of the renamed pathname is **UNVERIFIED**: the directory sync precedes replacement, and no post-replacement directory sync is claimed. Arbitrary postcommit inability to stat the public file is also **UNVERIFIED**; an observed verification error is reported, not silently accepted. These limits do not establish full-workload or crash-recovery acceptance.

### RED → GREEN receipts

| Control | RED receipt | Repair evidence |
|---|---|---|
| Actual terminal-bearing fd fsync timeout; persistent terminal fsync failure plus failed halt persistence | `G/red_complete.txt`: **7 tests, 10 failure cases**, exit 1, before production edits. Both Astra controls exposed finished/PASS, predictions and finding with the old readable-before-fsync terminal. Shared PASS/FAIL/INVALID, torn terminal, malformed prefix, publication boundary and round-trip controls also failed. Pre-fix sources/hashes are in `G/before/`, `G/before_hashes.json`. | `G/green_b2_initial.txt`: **7 PASS**. Timeout/failure snapshots and final streams have no terminal outcome, prediction verdicts or NEW1 finding; the directory-sync/replacement controls also cover failed halt persistence. |
| Exception/alarm immediately after successful replacement | `G/red_postcommit.txt`: **2 tests, 3 failure cases**, exit 1. An already committed outcome was incorrectly returned as INVALID-WORKER/STOPPED-DEADLINE. | `G/green_postcommit.txt`: **5 PASS**, including the original precommit controls. Prepared identity reconciles actual commitment. The prior I/O fixture now distinguishes a failure before commitment from an exception after successful terminal emission; it explicitly checks the postcommit diagnostic. |
| Lost concurrent append if publication is unlocked | `G/red_lock_mutation.txt`: a fresh-process negative mutation that removes flock loses the real racing progress event; **1 expected failure**. Production was not edited for this mutation. | `G/green_short_prefix.txt`: the real locked append is retained, the old prefix is retained, and the completed fold remains PASS. |
| Short unbuffered write while copying the prior stream | `G/red_short_prefix.txt`: **1 failure**, exit 1; the original copy routine ignored its write count and published the terminal. | `G/green_short_prefix.txt`: **2 PASS** for checked prefix copying and concurrent append. Publication aborts on a short write while the public pending stream supplies no verdict. |

The initial system-Python consumer run in `G/green_stdlib_initial.txt` failed with **6 PIL import errors / 118 tests**; no dependency was installed. The final runs use the existing `.venv`. The first historical comparator also tripped on integer dictionary keys becoming strings in JSON; its empty redirected receipt is preserved. The corrected verifier normalizes JSON representation and compares the complete state, rather than interpreting that observation-layer mismatch as a reader regression.

### Final requested verification

| Module | Final tests | Receipt |
|---|---:|---|
| `tools.test_dashboard_mathlab` | 58 PASS | `G/green_stdlib_final.txt` |
| `tools.labviz.test_mathlab` | 17 PASS | same fresh-process receipt |
| `tests.test_new1_supervisor` | 45 PASS | same fresh-process receipt |
| `mathlab.test_mathlab` | 77 PASS | `G/green_numerical_final.txt` |
| `tests.test_new1_geometry` | 25 PASS | same separate CPU-process receipt |
| **Total** | **222 PASS** | consumer/supervisor **120 / 15.115 s**; synthetic numerical **102 / 2.395 s**; both exit 0 |

From the worktree root, the exact final dispatches were:

```sh
/opt/homebrew/bin/rtk proxy env TMPDIR=/private/tmp LLMDB_DEVICE=cpu CUDA_VISIBLE_DEVICES= OMP_NUM_THREADS=8 MKL_NUM_THREADS=8 PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B -m unittest tools.test_dashboard_mathlab tools.labviz.test_mathlab tests.test_new1_supervisor -v
/opt/homebrew/bin/rtk proxy env TMPDIR=/private/tmp LLMDB_DEVICE=cpu CUDA_VISIBLE_DEVICES= OMP_NUM_THREADS=8 MKL_NUM_THREADS=8 PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B -m unittest mathlab.test_mathlab tests.test_new1_geometry -v
```

The numerical process uses synthetic CPU tensors only. No real adapter/covariance/harvest operand was decoded or evaluated for geometry; no model/tokenizer/engine runtime, GPU/MPS, real admission, full-shape probe, queue action, dependency installation or commit occurred.

`G/historical_before.json` and `G/historical_full_after.json` are complete **byte-identical** snapshots, SHA-256 `628d634b301c62383b8d6df2c41e418209448646d68bf4746dd8a07b4b1525ea`. `G/verify_compatibility.py` verifies every source-stream hash, event count and complete normalized fold; `G/historical_full_compatibility.txt` records **10 unchanged streams**. These include both harvest PASS streams, both m2 PASS streams, and the m3 calibration **FAIL / stopped: check failed** stream, plus five historical admission/acceptance streams. No recorded event file was rewritten.

The independent GPT-6-Astra fallback review is preserved in `G/final_advisor_review.md` (FIX-FIRST on short copying) and `G/final_advisor_review_r2.md` (**PROCEED**, resolved short-copy and complete-snapshot concerns). The reviewer read the source and actual receipts and independently compared the snapshots; it did not rerun tests. Fresh Claude auth reported logged out, so this is GPT-family fallback review with weaker family independence, not a completed out-of-family Claude review.

### Scope, hashes and handoff

| Changed implementation/test | Final SHA-256 |
|---|---|
| `tools/mathlab_events.py` | `53b2ea18ea8a363136e967c25bb0e8a94f88a63070f3921a3b996e2287459f5f` |
| `tools/new1_supervisor.py` | `9f316f5613c0ed32c8f53ad8a4a209b0f1097bc45007d49b46cd2c5854cf2505` |
| `tests/test_new1_supervisor.py` | `b024ed17015fca7b193840d01bd5c3db8ed4a4a2d17b487f698b3b8805b97317` |
| `tools/test_dashboard_mathlab.py` | `b46d9c852706e20e8dca40cca8f56793559f3441cf30f5b9e8257a0ea0dab02e` |

`G/final_verification.json`, `G/finalize_audit.py`, and `G/implementation.diff` record the final scope: the frozen NEW1 prereg, geometry implementation/tests, MathLab tests and LabViz tests remain byte-identical to the MB3 baseline; top-level supervisor constants and the entire Controller AST are unchanged; the original report prefix is retained; `git diff --check` passes. Worktree/root and `worktree-c10k-route-a` branch are unchanged. HEAD remains `87468b66ecaab76b10da5296c99cd586ec7d18f1`, the MB3 starting HEAD; other lanes' untracked artifacts were preserved. No mutating git operation occurred.

**Limits kept flush:** fixtures validate event publication and consumer plumbing only. Real NEW1 execution, production workload I/O, full-workload timing/RSS, 1,800-s / 6-GiB feasibility, power-loss pathname persistence, and arbitrary postcommit stat-unavailability remain **NOT RUN / UNVERIFIED**. No prediction or F1 scientific closure follows from this build repair.

**Handoff:** B2 implementation and all requested verification are complete; no test, implementation or reviewer is in flight. Exact sources, evidence location, commands, current hashes and limits are above. Workspace-local `/context-save` snapshot: `results/mathlab_staging/new1_v2_build_evidence/mb3_20261009T233356Z_b2/checkpoints/20261009-235859-new1-b2-complete.md`. MAESTRO owns any formal follow-up review and separately authorized real execution with fresh admission. Preserve all historical RED/failure receipts and the physical `/private/tmp` evidence directory. Do not resume MathLab/step 4 from an older snapshot or infer permission to execute NEW1 from build completion.

**Context rule, binding through every handoff:** watch **Context N% left**; before approximately **20%**, stop starting new work, write done / in-flight / exact paths / next step / open risks into the task report, and say so for a fresh successor session. Never approach full-window compaction. Every handoff restates this rule.
