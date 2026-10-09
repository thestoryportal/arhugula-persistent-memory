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
