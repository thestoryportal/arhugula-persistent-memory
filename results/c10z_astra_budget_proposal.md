RECOMMENDATION: Amend the frozen stage 0–1 ceiling from 5,400 s to 7,200 s before anything runs (one code constant, one reader check, the prereg SHA pin, three selftest spots), then launch with C10Z_STAGE2_CEILING_S=12600 and C10Z_STAGE3_CEILING_S=19800, a worst case of 39,600 s (11.0 GPU-hours over both processes); the operator says yes to these numbers under a new D-C10z-budget row.
Author: Claude Opus 5.5 subagent, 2026-10-07

Scope: read-only analysis. Nothing in ASTRA has run: `results/c10z_astra/` and `architecture_profile/c10z_astra_halt_diagnostic.json` are absent (ls, 2026-10-07). Selftest rerun on CPU only: `C10Z_ASTRA_SELFTEST_PASS tests=79`. Prereg SHA-256 = `38f8b68c…` = `c10z_astra_read.py:14`. No MPS measurement of any ASTRA component exists, so every ASTRA cost below is UNVERIFIABLE unless it comes from a cited anchor.

## 1. How the stage 0–1 budget works in the code

- **Ceiling.** `Budget.__init__` hard-codes `"stage01":5400.` (`c10z_astra_arms.py:88`). The stage-2 and stage-3 values come from env at the stage-0 call only (`:1469–1470`). They are frozen into `run.json` and later env changes are ignored (`:1495`). `future_stage2_s=7920.` is the stage-2 allowance that process 2's stage-3 scope sees before stage 2 starts (`:90`, `:118`).
- **Clock origin.** The origin is `time.monotonic()` at `resident()` entry in the child (`:1392`). It is never restarted (`:83`). The watchdog raises HALTED-BUDGET at the deadline even while idle (`:1414–1416`).
- **Projection.** `project(costs)` (`:114–126`) requires `(now − origin) + Σcosts ≤ ceiling` for every active scope. It prints `C10Z_PROJECTION {…}` to `logs/resident_p1.log` (`:123`, `:1473`) and raises `HALTED-BUDGET "published elapsed + remaining work exceeds ceiling"` (`:124–125`).
- **Constants.** `ALLOWANCES` (`:32–33`) sum to 120 + 2,040 + 300 + 120 + 1,380 + 1,200 + 180 = **5,340 s**, which leaves 60 s of slack under 5,400. `remaining_validation()` = V = max(1,380, Σ last-3 `locality_probes` + Σ last-3 `binding_evaluation`) (`:762–763`). Both timing lists fill from `probe_hits` (`:599`) and `eval_guard` (`:409–413`, installed at `:372`, before recipe A).

| # | where | projected remaining | passes iff elapsed ≤ (V = 1,380) |
|---|---|---|---|
| P0 | `Session.__init__` `:337`, before torch import | 5,340 | 60 s |
| P1 | `stage0` start `:796`, after import + pin | 5,220 | 180 s |
| P2 | after recipe A, LAW#3, step 4 `:847` | 300 + 120 + V + 1,200 + 180 = 1,800 + V | **2,220 s** |
| P3 | end of stage 0 `:857` | 1,200 + V + 180 | 2,640 s |
| P4/P5 | stage-1 entry `:1253`, write start `:709` | 1,380 + V | 2,640 s |
| rounds | `:714` | (10−r)·max(round s, 120) + V + 180 | ≈ 2,640 s |

- **Why P2 almost certainly refuses.** P2 adds the whole validation allowance again after stage 0 has already spent part of it. A run whose import, pin and recipe A take their allowances (2,160 s) has 60 s left for stage-0 step 4. Step 4 contains:
  - a full pristine A7 evaluator call (`:823`);
  - six probe sets (`:813`, `:844`), where A7's F1 alone is 6 × Σ(T_i−1) × 6 = 1,728–4,320 greedy probes (prereg `:163`; T_i ∈ [3, 6] UNVERIFIED, `:77`), each generating every target token with a full no-cache forward (`:550–557`);
  - Z0's per-prefix forwards (`:862–870`).
- **The anchor makes it worse.** The measured three-arm harness passes took ≈ 30–31 min each: c10q `passSsham.json` 02:52:40 → 03:23:05 and `passSperm.json` → 03:54:22 (`ls -T results/c10q_stacked/`; run window 02:15–03:54, `CORPUS/50_C10Q_STACKED_SOLVE.md:3`). The prereg cites 34 min (`:194`). That leaves roughly 3–7 min for import + pin + step 4.
- **V can be larger than the floor.** V is the sum of three evaluator calls and three probe sets. If that exceeds 1,380, every later projection grows with it.
- **Verdict.** I agree with the implementation-review advisory (`results/c10z_astra_advisor_impl.md:49–53`). A normal run is very likely refused at P2, about 40 min into the GPU slot.
- **What a refusal writes.** `resident` catches the Halt (`:1452–1457`), restores and verifies PRISTINE, and calls `diagnostic()` (`:1364–1387`). That writes `halt_p1.json` (code, detail, recipes, checks, memory, restores, `budget_history`), closes `run.json` with `halt` and `reading=null`, writes `architecture_profile/c10z_astra_halt_diagnostic.json`, and returns rc 2. The parent re-raises the Halt (`:1504`). The reader labels the directory HALTED-BUDGET (`c10z_astra_read.py:673–676`). The attempt is spent, so a retry needs a fresh OUT_DIR (`arms:1465`).

## 2. Is 5,400 frozen? Yes: an amendment is needed

- **The number is frozen in the prereg** at `:18` (requirement row 6), `:125`, `:127`, `:133`, `:196` (twice) and `:344` (decision 2).
- **It is also enforced in code.** The driver hard-codes it (`arms:88`). The reader rejects any record whose `ceilings["stage01"] != 5400.` (`read:500`). The driver HALTs V12 if the prereg's SHA differs from `R.PREREG_SHA` (`arms:329`, `read:14`).
- **The stage-2 and stage-3 ceilings are launch inputs** (prereg `:196`, `:199`): no amendment is needed for them.
- **The allowances live in code only** (`arms:30–33`). Lowering them would weaken a safeguard without any measurement, and this proposal does not do it.

**Draft amendment** (append as a new final section of `docs/C10Z_ASTRA_PREREG.md`; do not edit the frozen lines):

> ### 9. Amendment B-1: stage 0–1 ceiling 5,400 s → 7,200 s (2026-10-07, pre-observation; Decision-ID D-C10z-budget)
> Written before any ASTRA process has started. No ASTRA output, timing or reading exists (`results/c10z_astra/` absent). One number changes. Every statement of the stage 0–1 hard elapsed-time ceiling as 5,400 seconds (:18, :125, :127, :133, :196, :344) reads **7,200 seconds**. Nothing else changes: the clock origin, the scopes, the projection rule, the recorded allowances, the never-zero rule, the 120-second round halt (V13), the stage order, every gate, label, K1/K2 and the rule that ceilings never increase during an attempt.
> **Reason.** The driver publishes elapsed time plus projected remaining work (§2.11). Its post-baseline projection adds the full validation allowance (≥ 1,380 s) on top of the elapsed time, which already includes the stage-0 evaluation and probe work. Its recorded allowances sum to 5,340 s. So a run whose every component lands at its allowance is refused whenever stage-0 step 4 takes more than 60 s, and step 4 contains a full evaluator call and six probe sets.
> **Basis for 7,200 s.** 5,340 (allowance sum) + 1,380 (the validation allowance counted again) + 480. The 480 s covers three items, none of which has an allowance and all of which are UNMEASURED: the hand-off between the stage-0 and stage-1 calls (≤ 120 s), the stage-1 recipe's covariance load, LAW#5 edit and pre-axes (≤ 300 s), and child start-up (≤ 60 s).
> 7,200 s is the top of requirement row 6's "cheap early-kill stage (≈ 1–2 h)", which stands unchanged. The ceiling remains a proposed resource bound, not a demonstrated cost or approval to run. ":315 any budget change is a new pre-registration" concerns changes after an UNDERFIT reading and does not apply before observation.

Code and test changes that come with the amendment (proposal only, test-first, then advisor + GPT-6-Astra delta review per D-C10r-rulings-10, `EXPERIMENT_RUNBOOK.md:351`):

| file | line | change |
|---|---|---|
| `c10z_astra_arms.py` | `:88` | `"stage01":5400.` → `7200.` |
| `c10z_astra_read.py` | `:500` | `==5400.` → `==7200.` |
| `c10z_astra_read.py` | `:14` | `PREREG_SHA` → the new prereg SHA |
| `c10z_astra_selftest.py` | `:19` | `PREREG` → the new SHA (checked at `:776`) |
| `c10z_astra_selftest.py` | `:223–224` | fixture `5400` → `7200` (twice) |
| `c10z_astra_selftest.py` | `:633–639` | docstring, plus `5500`/`5499`/`5501` → `7300`/`7299`/`7301` in `test_budget_origins_prestart_deadlines_round_memory` |

The selftest must stay 79/79. The launcher is unchanged.

**Alternatives considered.**
- **(a) Run at 5,400 knowingly.** This spends about 40 min to get the first measured elapsed times (P0–P2 `C10Z_PROJECTION` lines) and ends HALTED-BUDGET.
- **(b) Fix only the double count in code.** This touches reviewed projection logic and still leaves 60 s for work that has no allowance.

## 3. Stage-2 and stage-3 ceilings

- **Stage 2: 12,600 s (3.5 h).**
  - Entry projection: elapsed + 3,600 + 3V + 180 (`arms:1264–1265`). The bare minimum is therefore > 7,920 s. Exactly 7,920 refuses, because elapsed > 0 and the test is `≤` (`:124`).
  - A run that passed stage 1's write projection satisfies e_w + 1,380 + V ≤ C01. Every interval summed in V precedes the write, so e_w ≥ V, which gives V ≤ (7,200 − 1,380)/2 = 2,910.
  - 3,780 + 3 × 2,910 = 12,510, rounded to 12,600 so that the near-zero elapsed time at entry cannot sit on the boundary.
  - **Why not the minimum.** A refusal at stage-2 entry turns a clean K1 survivor into an attempt labelled HALTED-BUDGET, with the K1 record kept only as an observation (`read:673–676`). An absent ceiling would at least close `-STAGE1` (`read:586–590`). An undersized ceiling is therefore worse than none.
  - **UNVERIFIABLE.** V at stage-2 entry swaps the recipe-A A2 evaluation and the A1 deferred probes for the Z-A7 evaluation and probe set, which are larger. V can therefore exceed 2,910 there.
  - **Expected cost.** Work actually done at allowance ≈ 3 × 1,200 + 1,380 + 180 + 2 recipe overheads ≈ 5,200 s. The ceiling caps time; it is not spent.
- **Stage 3: 19,800 s (5.5 h) = C01 + C2.**
  - Process 2 enforces its own stage 0–1 and stage-2 deadlines (prereg `:196`; `arms:91–93`, `:1264`). Its close and final publish also check the stage-2 deadline (`:1289`, `:1400`).
  - So process 2 can never legitimately need more than C01 + C2. A smaller value could cut a process 2 that its inner deadlines admit, and a larger one can never be reached.
  - First projection check: 5,340 + 7,920 = 13,260 ≤ 19,800 (`:337`, `:118`).
- **Worst-case GPU time.** Process 1 ≤ 7,200 + 12,600 = 19,800 s, and process 2 ≤ 19,800 s, for **39,600 s = 11.0 h**. The gap between stage 1 and the stage-2 call is outside this figure (§5).
- **Expected GPU time (arithmetic, unmeasured).** About 1.5–2 h if K1 kills, about 2.9 h per process at allowance, and about 5.8 h if both processes run.

## 4. Go record (`C10Z_GO_RECORD`), checked at `arms:1342–1361`

- **The check.** The record must have exactly the decision keys {"0", "1", "2"}, each a string beginning `D-` with a non-empty remainder (`:1352–1355`), plus `operator_yes` and `one_gpu_job` both `true` (`:1356–1357`), non-empty `recorded_by` and `recorded_at` (`:1358–1359`), and finite JSON only (`:1348`, `:1360`).
- **Where it is used.** Its SHA is bound into H_in (`:1163`), and the record is copied into `run.json` via `launch` (`:1468–1470`, `:1402`).
- **Where to put it.** `results/c10z_astra_go_record.json`, outside OUT_DIR.

```json
{
  "decisions": {"0": "D-C10r-rulings-10", "1": "D-C10r-rulings-10", "2": "D-C10z-budget"},
  "operator_yes": true,
  "one_gpu_job": true,
  "recorded_by": "program session (Claude Opus 5.5) relaying operator ruling D-C10r-rulings-10, EXPERIMENT_RUNBOOK.md:351, item (2)",
  "recorded_at": "2026-10-07T00:00:00-06:00"
}
```

Notes on the record:
- **Fill in the real `recorded_at`** when the file is written. The code accepts any non-empty string, so a placeholder would pass.
- **`"2"` points at D-C10z-budget**, a row that does not exist yet. It records the operator's yes to these numbers and the amendment. Precedent: D-C10w-p1budget, where the program does not authorize its own raise (`EXPERIMENT_RUNBOOK.md:350`). D-C10r-rulings-10 only says "the program proposing its time budget" (`:351`).
- **`"1"` (write qualification)** is not separately recorded at `:351`. State in the D-C10z-budget row that the go covers it. A "measurement" ruling changes no gate or label (prereg `:343`).
- **The code does not check that the IDs exist** (`:1354`). Grep §5.2 for each one by hand.

## 5. What can still refuse or false-HALT a legitimate run, and the launch plan

Risks:
1. **Wrong tree.** The launcher derives `W` from its own path and runs `$W/.venv` (`run_c10z_stage.sh:6`, `:12`), so invoke the worktree's launcher by absolute path. Put `LLMDB_ROOT=<worktree>` on every command, as D-C10w-p1budget B1 requires (`EXPERIMENT_RUNBOOK.md:350`). The launcher also re-exports it (`:7`), and the driver resets it (`arms:339`).
2. **Inherited environment.** Any `C10_*` knob, `N_EDIT`, a mismatched `MODEL_ID`/`MODEL_REV`, or `LLMDB_DEVICE≠mps` → HALT (`arms:28–29`, `:65–70`). Check that `env | grep -E '^(C10_|N_EDIT=|MODEL_ID=|MODEL_REV=|LLMDB_DEVICE=)'` prints nothing.
3. **Launch inputs.** Ceilings and the go record are read only at stage 0 (`:1467–1470`). `C10Z_OUT_DIR` must be the same absolute path on every call (`:1524`) and fresh at stage 0 (`:1465`).
4. **Stage 0 → 1 gap.** It consumes C01, because the origin is the resident start and the watchdog runs while idle (`:1392`, `:1414–1416`). Chain the calls.
5. **Stage 1 → 2 gap.** There is no deadline, because no scope is active (`:95–97`, `:1259`; advisor ADVISORY 7). The resident holds the model indefinitely, so chain this call too. `stage_call(2)` refuses harmlessly, with no files written, if K1 did not survive (`:1489–1494`).
6. **Stage 2 → 3 gap.** It is free: the stage-3 clock starts at the stage-3 call (`:1463`, `:1488`), and stage 3 is code-gated on a clean K2 (`:1480–1483`).
7. **Heartbeat false HALT-V12.** The parent requires a heartbeat ≤ 15 s old (`:1513–1515`). The resident writes and fsyncs one every second on `/Volumes/memit` (`:51`, `:1411`). That disk is shared with the model snapshot (5.8 GB, via the `hf_cache` symlink) and with the six-hourly `com.rhu.memit-backup` launchd job, which is loaded. Start right after a backup completes, run under `caffeinate -i`, and use `nohup`.
8. **GPU sharing.** Another MPS job slows the rounds, and a stage-1 round over 120 s halts HALTED-BUDGET (`:78–79`, `:740`). Confirm the current job has exited and the autoresearch loop is paused (D-C10r-rulings-4 (1), `:331`).
9. **Unexpected V.** A measured V above the allowance raises every later projection, and ceilings cannot be raised mid-attempt (prereg `:196`). Watch the `C10Z_PROJECTION` lines in `results/c10z_astra/logs/resident_p1.log`. A refusal is a clean HALTED-BUDGET, never a wrong label.

**Launch order:**
1. Amendment, code/test change, selftest 79/79, advisor + GPT-6-Astra delta review.
2. Operator yes, recorded as the D-C10z-budget row.
3. Write the go record.
4. Hand checks: `python3 tools/engine_fingerprint.py` PASS; GPU idle; backup timing; env clean; OUT_DIR absent; go JSON parses.
5. Then, with `W=<worktree absolute path>`:

```
nohup caffeinate -i env LLMDB_ROOT="$W" C10Z_OUT_DIR="$W/results/c10z_astra" C10Z_GO_RECORD="$W/results/c10z_astra_go_record.json" \
  C10Z_STAGE2_CEILING_S=12600 C10Z_STAGE3_CEILING_S=19800 bash -c '"$1/tools/run_c10z_stage.sh" 0 && "$1/tools/run_c10z_stage.sh" 1 && "$1/tools/run_c10z_stage.sh" 2; echo "STAGE_EXIT=$?"' _ "$W" > "$W/results/c10z_astra_chain.log" 2>&1 &
```

Stage 3 runs as a separate call with the same env after the stage-2 reading (`"$W/tools/run_c10z_stage.sh" 3`). Keep every outer log and exit status, and never repeat a stage within an attempt.
