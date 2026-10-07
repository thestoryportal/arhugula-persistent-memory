Verdict: PROCEED

# D-C10u-mint2 r3 fix: independent advisor review (2026-10-07)

Scope: commit 0a6aed3 (one `print` in `behavior_job`'s non-admitted branch, plus the test `test_nonadmitted_behavior_child_logs_and_parent_accepts` and the launcher `tools/run_c10u_stage_r3.sh`). All line numbers refer to the working tree at 0a6aed3 (`c10u_mint2_arms.py` sha256 6a13d9c6…). r2 pinned bb122445…, which is `git show 0a6aed3^:experiments/track_c/c10u_mint2_arms.py | sha256sum`. Everything was checked model-free. No torch was imported, no tracked file was edited, and scratch work lives under `/Users/robertrhu/.claude/jobs/8ac4cacf/tmp/c10u_r3_mut/`.

## BLOCKING

None. The fix adds one line after the record is written (`c10u_mint2_arms.py:777` write_json, `:778` print, `:779` return). It cannot change any record, label or gate. The new line runs only after `write_json` has persisted `rec` and re-read it (`:45–54`). The test was the only other code change. It runs green in the real tree, and only the scratch copy of the deliberately mutated driver turns it red.

## ADVISORY

**A1. An admission-UNDERFIT seed is read as `INVALID`, but the prereg says `ROUTING-BLOCKED-UNDERFIT`.** This defect is in the frozen reader and was there before the fix. It does not cause a HALT and does not change any gate. Resolve it before the verdict, not before the relaunch.
- Prereg `docs/C10U_MINT2_PREREG.md:72` says that if any value in any mint arm of a block is unfit, "the block's direction reading is **ROUTING-BLOCKED-UNDERFIT**". `:115` says "P3 screen < 22/24 → UNDERFIT, no behavioural run".
- The non-admitted record has `"pid": None` (`c10u_mint2_arms.py:774`) and no `recipe` or `arm`. `run_validity` therefore rejects it (`c10u_mint2_read.py:190` → "process/replicate malformed". If pid were set, `:191` "behaviour run not complete" would reject it instead). `_population` passes that rejection into `block_reading`, which returns `INVALID` at `:453–455`. That happens before the `ROUTING-BLOCKED-UNDERFIT` branch at `:497–498`, which only ever sees DONE records.
- I ran the reader on the actual r2 records (mint1 s0–2, multi, modifier s0 UNDERFIT): `block_reading F: INVALID ['incomplete/malformed/invalid run: process/replicate malformed']`.
- What happens in r3: if any modifier seed is UNDERFIT again, `frozen_complete.json` (`c10u_mint2_arms.py:1027–1032`, write-once) records F `direction: "INVALID"` with a misleading reason, and `c10u_mint2_read.py:656` exits 2. A mint2 seed that is UNDERFIT in stage `v2` does the same to V2.
- Gating is unchanged under either label. `stage_plan('replicate-F', r2 records)` returns `[]`, from `read.py:545`. Under the prereg label it would also be `[]`, because `ROUTING-BLOCKED-UNDERFIT` returns at `:498` before `replication_pending` is set at `:506`. `control` is also refused under both labels (`:545` vs the blocked set at `:549`). `p4_configurations` skips `INVALID` (`arms.py:945`), and `run_reading` on an UNDERFIT record gives `INVALID`, so P4 never selects it either way.
- The readings are pure and can be recomputed from the raw records. The fix is a reader-side branch: treat `outcome in {"UNDERFIT","INVALID"}` non-admitted records as admission-excluded, and map an `UNDERFIT` record to `ROUTING-BLOCKED-UNDERFIT`. It needs its own test-first change and its own decision. Until then, the close-out must state the prereg label and must not copy `INVALID` from `frozen_complete.json`. Do not make this change now: it would be a second fix under halt discipline.

**A2. The new test checks stdout, but the parent's contract is stdout+stderr.** `spawn_job` merges stderr into the log (`arms.py:892`, `stderr=subprocess.STDOUT`). Mutant M2 (print to stderr) is therefore correct in production, yet the test kills it (`redirect_stdout` at `selftest.py:581`). This is harmless. Separately, the test never calls `spawn_job`, so its name ("parent_accepts") claims more than it checks. A parent-level probe exists at `/Users/robertrhu/.claude/jobs/8ac4cacf/tmp/c10u_r3_mut/parent_probe.py`. It runs the real `spawn_job` around the real `behavior_job` in-process, with stdout and stderr both going into the log file, and could be adopted as a test later.

**A3. The contexts child depends on output it does not print itself.** `context_job` (`arms.py:661–683`) has no `print`. Its log is non-empty only because of `c10e_bandknob.py:49` (`print(f"loaded {ID}")`, unconditional at import via `load_harness` `arms.py:665`) and the engine's `memit_main.py:321` ("Cached context templates", which runs on a fresh process). The r2 `logs/contexts_F_r0_multi_snone.log` is 782 B and contains both lines. The output is unconditional, so the contexts child cannot cause a false HALT in r3. But nothing pins this coupling, so it should get the same one-line status print the next time the driver is unfrozen.

**A4. Source drift during the run.** r3 runs for hours (r2 `reproduce` took 70 min, and each behaviour run takes about 23 min). Every child and the stage loop call `assert_sources` (`arms.py:682, 741, 749, 864, 901`) over the 15 `SOURCE_FILES` plus the engine (`:24–27, :77–82`). Two Codex panes are currently running with `-s workspace-write` in this same worktree (`ps`: pids 240 and 73287, C10Z design and build). Their brief forbids editing existing files (`codexi_c10z_build_brief.md:29`). Any edit to a c10u source file during r3 would still cause a correct but costly HALT. At review time `git status --porcelain` on all source files and `memit_dry_run/memit` was empty. Keep them frozen until r3 closes, and keep one GPU job at a time: no `tools/run_c10z_stage.sh` stage while r3 runs.

**A5. Trivial launcher mode difference.** The r3 launcher is mode 755 and r2 is 644 (`ls -l`). This only matters if the launcher is executed directly rather than through `bash`. The contents are covered in the evidence section.

## Evidence

### Diagnosis verified
- Halt diagnostic `architecture_profile/c10u_mint2_halt_diagnostic_6508cfa1…json`: `stage: frozen`, `reason: "child failed; no automatic retry or fix"`, `state.returncode: 0`, `state.command` = `_job --job behavior --block F --kind modifier --replicate 0 --seed 0`, `state.log` = `r2/logs/behavior_F_r0_modifier_s0.log`.
- `ls -la results/c10u_mint2/r2/logs`: `behavior_F_r0_modifier_s0.log` is **0 bytes** (08:51). `step0_F_r0_modifier_s0.log` is 1371 B and ends with `STEP0 F modifier seed=0: UNDERFIT`.
- `results/c10u_mint2/r2/F_r0_modifier_s0.json` is present and well-formed: `outcome: UNDERFIT`, `admission.P3 = {ok: false, n_ge_0.98: 17, underfit: [1,5,8,12,13,16,20]}`, lowest fit 0.1326 at index 13, `pid: null`. There is no `F_r0_modifier_s0_started.json` in r2 (listing), which matches the non-admitted branch at `arms.py:771–779`, where `_started` is written only at `:780`.
- `results/c10u_mint2_logs/r2/frozen.log` reads `completed step0_F_r0_modifier_s0` → `HALT: child failed …` → `STAGE_EXIT=1`.
- Mechanism: before the fix the branch returned without output, and the parent guard `if result.returncode != 0 or not log.stat().st_size` (`arms.py:893`, which was `:892` at bb122445) halted. The diagnosis is correct.

### Selftest
`LLMDB_ROOT=<worktree> .venv/bin/python -B experiments/track_c/c10u_mint2_selftest.py` gave `Ran 61 tests … OK` and `C10U_MINT2_SELFTEST_DONE (stdlib only; no model/torch/GPU/driver)`. The prereg hash pin `c54f443c…` passes (`selftest.py:842`).

### Mutants
Each mutant is a scratch copy of arms, read and selftest, with one change to `arms.py:778`. "Suite" means the full selftest run on the scratch copy. `test_aenv_source_identity_pins…` errors in every copy, the control included, because the scratch root has no repo files. It is excluded from the counts below.

| Mutant | New test | Rest of suite | Real `spawn_job` parent probe | Production meaning |
|---|---|---|---|---|
| M0 control (as committed) | pass | pass | ACCEPTS, log = `BEHAVIOR F_r0_modifier_s0: no behavioral run; step0 outcome=UNDERFIT` | correct |
| M1 print deleted | **KILLED** (`'UNDERFIT' not found in ''`) | pass (only the new test catches it) | **HALTS** `child failed` (reproduces r2) | the r2 bug |
| M2 print to `sys.stderr` | **KILLED** (`'UNDERFIT' not found in ''`) | pass | ACCEPTS (stderr is merged into the log, `:892`) | also correct; test over-specified (A2) |
| M3 print before `write_json` | survives | pass | ACCEPTS | equivalent: if `write_json` raises, the child exits 1 through `halt` (`:1105–1106`, `:74`), so the parent halts at `:893` whatever the print order |

The new test kills the mutant that matters (M1). The survivor (M3) has no observable difference at the parent.

### Child paths: can any exit 0 with an empty log or without its result file?
The parent's checks are returncode ≠ 0 or empty log → HALT (`arms.py:893–894`), and a missing result file → HALT (`:895–899`). The result paths are `contexts_<B>.json`, `step0/<tag>.json`, or `<artifact_tag or tag>.json`. A child halt goes through `halt` → `SystemExit(str)` → exit 1 (`:74`, `:1105–1106`).

| Child (spawned at) | Exit-0 path writes result before exit? | Guaranteed log output on exit 0 | Empty-log false HALT possible? |
|---|---|---|---|
| contexts (`ensure_context` `:909`; reproduce and v2 stages) | yes, `:683` is the last statement | `c10e_bandknob.py:49` "loaded …" (import in `load_harness` `:665`) and `memit_main.py:321` | no (incidental output; A3) |
| step0 (`ensure_step0` `:919`; every mint arm) | yes, `:742`; P2 failure halts with exit 1 at `:716` | `:464` × 24 capture lines, `:743` STEP0 line | no |
| behavior non-admitted (UNDERFIT or INVALID; `:771`) | yes, `:777` | `:778` (the fix), plus nothing else since no harness is loaded | **no longer** (r2 failure mode, fixed) |
| behavior admitted mint arm (`:1022`) | yes, `:865`; validity failure halts at `:868` | `c10e_bandknob.py:49`, `:464` not called (z from step0), `:869` | no |
| behavior multi (`:1022`) | yes, `:865` | `c10e_bandknob.py:49`, `:464` × 24 (`:819`), `:869` | no |
| behavior replicate r1 (`replicate-F` / `replicate-V2`) | same as admitted or multi (step0 precursor is r0, `:770`/`:747`, `:999`) | same | no; this stage is only planned when `replication_pending` (`read.py:551`), which requires an all-valid block, so a non-admitted r1 cannot arise |
| behavior P4 save (`p4_save_stage` `:969`, `artifact_tag`) | yes, `:865` → `<p4save_tag>.json`, which matches the parent path at `:897` | `:869` | no; only selected for LEAD/PARTIAL DONE records (`:954`) |

The only `return` before the end of `behavior_job` is `:779`, after the write at `:777`. `context_job` and `step0_job` have no early return. No exit-0 path skips writing its result file, so a "success without result" HALT (`:899`) is not reachable on any exit-0 path. HALTs that r3 can still legitimately reach: LAW#3 at `:931` (r2 multi 10/9/52 sat inside the windows), P2 at `:716`/`:796`, inertness at `:811`, LAW#5 at `:838`, validity at `:868`, source drift (A4), and the conditional-stage refusal at `:992` if `replicate-F` or `control` is launched when it is not planned.

### Launcher
`diff tools/run_c10u_stage_r2.sh tools/run_c10u_stage_r3.sh` differs on exactly three lines: line 2 (comment), line 9 (`LOGS=…/c10u_mint2_logs/r2` → `r3`) and line 11 (`--out-dir …/c10u_mint2/r2` → `r3`). Interpreter, `--law3-ref`, the env lines (`LLMDB_ROOT`, `PYTHONUNBUFFERED=1`, `unset LLMDB_DEVICE`) and `STAGE_EXIT` are identical. `bash -n` passes. `results/c10u_mint2/r3` and `results/c10u_mint2_logs/r3` do not exist yet, so `initialise_identity` (`arms.py:143–147`) will mint a fresh identity. `r3` lies under `results/c10u_mint2` as `:1082` requires, and `read_records` is non-recursive (`:874`), so r1 and r2 records cannot leak in.
