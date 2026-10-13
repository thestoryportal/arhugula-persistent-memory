RECOMMENDATION: Do not fix the ASTRA ceilings by arithmetic. First run a ≤ 10-minute MPS speed benchmark (§B). Then set all three ceilings from one formula (§C): stage 0–1 C01 ∈ [7,200, 10,800] s, stage 2 C2 = max(12,600, formula), stage 3 C3 = C01 + C2 + 60. Close the unbounded stage-1→2 idle gap with a one-rule driver fix (§D): the stage 0–1 clock keeps running until stage 2 actually starts. If the benchmark is not run, use 9,600 / 14,400 / 24,060 s (§E). The operator answers one D-C10z-budget question (§F) before anything is written or launched.

Author: Claude Opus 5.5 subagent, 2026-10-07. Status: DRAFT v2 of `results/c10z_astra_budget_proposal.md` (v1). Drafting only. No prereg, code, tracker or runbook has been edited, and nothing has run.
Reviews folded: GPT-6-Astra `results/c10z_astra_budget_astra.md` (FIX-FIRST, 4 BLOCKING) and Opus advisor `results/c10z_astra_budget_advisor.md` (FIX-FIRST, 2 BLOCKING).
Abbreviations: `arms` = `experiments/track_c/c10z_astra_arms.py`, `read` = `experiments/track_c/c10z_astra_read.py`, `selftest` = `experiments/track_c/c10z_astra_selftest.py`, `c10e` = `experiments/track_c/c10e_bandknob.py`, `prereg` = `docs/C10Z_ASTRA_PREREG.md` (SHA-256 `38f8b68c…b072` = `read:14`).

## A. Fold table: every BLOCKING item

| # | review item (file:line) | defect, verified against code | how v2 resolves it |
|---|---|---|---|
| Astra-1 | stage-2 derivation bounds the wrong timing window (`astra.md:7–14`) | **True.** The stage-2 entry projection is `elapsed + 3,600 + 3·V + 180 ≤ C2` (`arms:1264–1265`). V is the sum of the *last three* probe and evaluation timings at the call (`arms:762–763`). By stage-2 entry those are deferred p2, deferred p7 and the Z-A7 p7 probe sets, plus three A7 evaluations (advisor `:42`). v1's pre-write bound V ≤ 2,910 (`proposal.md:67`) does not cover this window. | **§C.** C2 is sized from V at stage-2 entry: N_V2 = 27,960 forwards × t* (advisor `:42`), not from the pre-write argument. v1 `:67–68` is withdrawn. Astra's wording is adopted verbatim: *"12,600 seconds is a discretionary stage-2 resource cap. It does not guarantee admission after K1: admission additionally requires elapsed_stage2 + 3,780 + 3×V_entry ≤ C2 … Approval accepts a possible HALTED-BUDGET after a clean K1 observation."* (`astra.md:14`). |
| Astra-2 | "11.0 h worst case" and "stage-3 ceiling can never be reached" are false (`astra.md:16–21`) | **True.** After a K1 survivor, stage 1 calls `complete01()` (`arms:1259`). That removes stage01 from `active` (`arms:112`). `deadline()` then returns `None` (`arms:96–97`), and the resident waits in `budget.check(); … time.sleep(.1)` (`arms:1435–1441`) until a stage-2 request arrives. The stage-2 origin is set only at `enter(2)` (`arms:109`, `:1264`). Nothing bounds this interval. In process 2 the inner stage-2 deadline can exceed the outer stage-3 deadline (Astra's 7,199 / 7,201 case). | **§D.** New rule: the stage 0–1 deadline stays in force until stage 2 is entered (`enter(2)` performs the stage 0–1 check, then completes stage 0–1). Every live interval is then inside a scope, so process 1 ≤ C01 + C2. C3 = C01 + C2 + 60, so process 2's inner deadlines always govern (proof in §D). Regression tests fail on today's code and pass after the fix. v1 `:74` and `:76` are withdrawn. |
| Astra-3 | 7,200 s needs an honest basis (`astra.md:23–28`) | **True.** v1's basis was allowance arithmetic: 5,340 + 1,380 + 480 (`proposal.md:43`). The work is also not "double counting": stage-0 probes and post-write probes are distinct required work (`arms:813`, `:844` vs `:709`). | **§B–C.** C01 is derived from the work the code performs: 26,680 stage-0 step-4 forwards (advisor `:40`) and V_P2 = 15,798 forwards (advisor `:41`), times a measured per-forward time. 7,200 survives only as the floor that the formula returns when t* ≤ 0.0517 s. The double-count language is withdrawn. Astra's framing is kept: a ceiling is "a prospective resource cap … not a measured completion estimate. HALTED-BUDGET remains possible" (`astra.md:26`). The 480 s pad is relabelled UNMEASURED (§C). |
| Astra-4a | launch exit handling: `; echo` masks failure; stage 2 dispatched after a K1 terminal (`astra.md:32`) | **True.** v1's chain ends `; echo "STAGE_EXIT=$?"` (`proposal.md:123`), so the outer shell exits 0. `&&` also runs stage 2 after a clean K1, because stage 1 returns 0 (`arms:1505–1507`), and stage 2 then refuses (`arms:1489–1490`). | **§G.** A reviewed wrapper logs every stage's exit code, exits with the first non-zero one, and calls stage 2 only when the published stage-1 reading says `next_stage == 2` (`arms:1443`, `:1505–1507`). Stage 3 is a separate `nohup caffeinate` call with its own log and exit code. |
| Astra-4b | approval provenance: decision "1" must cite the row that records it; the budget yes is prospective (`astra.md:33`) | **True.** D-C10r-rulings-10 item (2) is only "ASTRA (C10Z) go, with the program proposing its time budget" (`EXPERIMENT_RUNBOOK.md:351`). `go_record` checks only the ID format (`arms:1352–1355`). | **§F, §G.** Decisions 1 and 2 go to the operator in the same D-C10z-budget question. The go record is written only after that answer, as `{"0":"D-C10r-rulings-10","1":"D-C10z-budget","2":"D-C10z-budget"}`, with the real ISO `recorded_at`. **Operator.** |
| Adv-B1 | 7,200 rests on allowance arithmetic; step 4 is about 26,700 forwards, so 7,200 holds only at 52–87 ms per forward, while the anchor allows up to about 117 ms (`advisor.md:60–92`) | **Verified.** `greedy` makes one batch-1, no-cache, `logits_to_keep=0` forward per remaining target token (`arms:550–558`). The F1 population is 6 views × Σ(T−1) depths × 6 subjects (`arms:563–572`). A7 has ntok mean 5.5, range [4, 6] (`results/c10q_stacked/logs_run.log:15`). The anchor is 174 s for about 1,482 forwards, i.e. ≤ 0.117 s (`logs_run.log:71`). | **§B** benchmark (≤ 10 min) → **§C** formula for all three ceilings → **§E** fallback 9,600 / 14,400 / 24,060 (13.35 GPU-h). C01 > 7,200 breaks prereg row 6's "cheap early-kill stage (≈ 1–2 h)" (`prereg:18`). **Operator** rules on that in §F. |
| Adv-B2 | go record decision "1" cites D-C10r-rulings-10, which never answered it (`advisor.md:94–104`) | Same as Astra-4b. | Same as Astra-4b. **Operator.** |

Advisories folded:
- Advisor A2 (`advisor.md:109`): child start-up is not on the clock (`arms:1392`), so the pad is relabelled.
- Advisor A3 (`:110`): "5,400" occurs three times at prereg `:196` (grep), and the amendment uses `## 9.`, since the last top-level section is `## 8` at `:367`.
- Advisor A5 (`:112`): the expected cost is restated as I-INFER.
- Advisor A6 and A7 (`:113–114`): see §G.
- Advisor A8 (`:115`): the +60 s in C3.
- Advisor A9 (`:116`): the selftest `:1020` clock moves to C01 − 1.
- Astra advisory (`astra.md:37`): "all 79 tests plus budget-transition regressions" (§D).
- Astra advisory (`astra.md:38`): 120 s in the round projection is a fallback, `max(round_times or [120.])` (`arms:714`), not a floor.
- Astra advisory (`astra.md:39`): every forecast is UNVERIFIABLE until measured.

## B. Benchmark (what to time; the build brief is `results/c10z_astra_benchmark_spec.md`)

Purpose: measure the one quantity every ceiling depends on, the wall time of one probe-shaped forward on this Mac. It is infra, not an ASTRA observation. It writes nothing under `results/c10z_astra/` and needs the GPU idle (one GPU job at a time, `EXPERIMENT_RUNBOOK.md:351`).

- **Model, dtype and device are exactly the driver's.** Import `c10e_bandknob` with `LLMDB_ROOT=<worktree>`, `LLMDB_DEVICE=mps` and `HF_HOME=<root>/hf_cache`, as the driver does (`arms:339–342`). That gives Qwen/Qwen2.5-3B at rev `3aab1f19…` in fp16 on MPS (`c10e:25–26`, `:48`). Assert `DEV == mps` and dtype fp16 (`arms:344`), set `model.config.use_cache=False` (`arms:345`), and seed `torch.manual_seed(0)` (`arms:341`). `entry_preflight` refuses inherited `C10_*`/`N_EDIT` knobs (`arms:28–29`, `:65–70`).
- **Prompt shape is exactly stage-0 step 4's.** Build the A7 probe population with the driver's own construction (`arms:560–582`):
  - F0: `template.format(CANON).format(subject)`;
  - prefix: that string's IDs + `target[:depth]`;
  - subject-free: `"The name is"` + `target[:depth]`;
  - relations: `"{} is a"` and `"{} is associated with"`.

  It uses the six frozen-view templates logged by the last run of this harness and model (`results/c10q_stacked/logs_run.log:9`; the engine samples fresh 10-token templates per attempt, `memit_main.py:304–320`, so these are length-representative, not identical), `FRAME_SUBJECTS` (`arms:26`), A7 values (`c10e:246–248`) and `CANON` (`c10e:51`).
- **The timed unit is one greedy iteration, byte-for-byte `arms:555–557`:** `torch.tensor([cur], device=DEV)` → `model(…, use_cache=False, logits_to_keep=0).logits` → `int(logits[0,-1].argmax())`. The `int()` forces the MPS sync, so the timer stops after the work is done. Single-forward items (F0, relations) use the same call (`arms:594–595`).
- **Counts.**
  - 20 warm-up forwards, discarded.
  - Then ≥ 400 timed forwards, taken by running whole population items in a seed-0 shuffled order until 400 are reached (finish the current item). The run is valid only with ≥ 200 timed.
  - Also: 2 warm-up + 5 timed batched forwards at the A7 identity-batch shape (144 rows × T_pad, padded as `arms:433–446`), which stands in for the 10 stage-0 step-4 `observe` calls (`arms:817`, `:820`, `:839`, `:844`; hooks not reproduced).
  - Then, if time remains, one `eval_arm(A7)` cross-check (1,392 forwards, advisor `:39`) on pristine weights.
  - Then one CPU float32 SVD of an 11,008 × 11,008 matrix, the unit of `compute_P` (`c10e:166–178`) over band [4..8] (`configs/hparams/qwen25_3b_memit_hparams.json`), which every recipe repeats (`c10e:462`).
  - Model load and the pin hashing (`arms:356–364`) are timed too.
- **Output record.** `results/c10z_astra_benchmark/<UTC>/benchmark.json`, created once and replaced atomically per phase. It holds, per phase: status, raw per-forward seconds and sequence lengths, median/p90/p95/max/mean, environment, template and population digests, and a weights-unchanged check (36 `down_proj` hashes before = after, `arms:293`). Schema: see the build brief.
- **Wall cap.** The cap is 600 s from process start, before the torch import. A forward may start only while elapsed < 570 s (30 s reserve). Each optional phase starts only if its declared need fits. A hard watchdog exits at 600 s, and the record keeps the completed phases.

## C. Formula: measured time → three ceilings (one source of truth: the benchmark's pure `ceilings()` function)

**Statistic: p95, not max.** Each ceiling multiplies one per-forward time by about 15,800–28,000 forwards, so what matters is the *sum*, which the mean governs. The p95 sits above the mean for any right-skewed timing distribution, so it over-covers the sum by construction. The max is one sample and is dominated by one-off stalls (first-shape compile, allocator growth, a disk burst) that do not repeat 26,000 times. Using it would make the ceiling hostage to one outlier. The max is recorded for audit.

**Safety factor s = 1.25.** It covers what a 10-minute test cannot see: sustained slowdowns over hours (thermal throttling, the 6-hourly backup job on the same disk, which is `/Volumes/memit` per CLAUDE.md), the 1-second fsync heartbeat (`arms:1410–1413`), Python overhead in the evaluator, and hook overhead in `observe`.

Definitions (seconds):
- t* = s × max(p95 of timed probe forwards, eval_A7 seconds / 1,392)
- I_pin = max(120, s × (load + pin)): `ALLOWANCES["import_and_pin"]` = 120 (`arms:32`)
- O = s × 2 × 10 × p95(batched forward): 10 step-4 observes; the ×2 for hook capture is UNMEASURED
- Q = max(480, s × 5 × t_svd + 300): post-P2 work with no allowance. This is the stage-1 Z-recipe preamble (`compute_P` 5 SVDs, LAW#5's two edits `c10e:415–439`, `cov_cache_sha256`, `axes_pre`, 24 predicts `c10e:462–476`), Z1–Z7 verification beyond the 420 s D+G allowances (`arms:32`, `:849–851`) and the stage-1→2 hand-off. The 300 is UNMEASURED.
- R(x) = 300·⌈x/300⌉

**C01** = R( I_pin + 2,040 + 26,680·t* + O + 1,800 + max(1,380, 15,798·t*) + Q ).
- This is the P2 projection (`arms:847–848`: 300 + 120 + V + 1,200 + 180 = 1,800 + V after stage-0 step 4) plus the post-P2 pad.
- 2,040 is `ALLOWANCES["recipe_A"]` (`arms:32`). The c10q recipe-A-only pass is ≈ 1,650–1,700 s (I-INFER, advisor `:27`).
- 26,680 and 15,798 are the advisor's forward counts (`advisor.md:40–41`).
- **STOP if C01 > 10,800 s:** do not launch; return to the operator. That happens at t* ≳ 0.150 s with the minimum I_pin, O and Q.

**C2** = max(12,600, R(3,780 + 3·max(1,380, 27,960·t*) + 600)).
- 3,780 + 3V is the stage-2 entry projection (`arms:1265`). Under §D, stage-2 elapsed at entry is ≈ 0, because the origin is set inside `enter(2)` (`arms:109`).
- The 600 covers recomputation of the entry projection.
- The 12,600 floor is discretionary, in Astra's words (§A), and not derived.
- Admission after K1 is still not guaranteed.

**C3** = C01 + C2 + 60. The +60 exceeds the watchdog's 0.1 s poll (`arms:1408`) many times over, so C3 never governs (§D).

Values at I_pin = 120, O = 0 and Q = 480. Measured O, Q or I_pin above these minima raise C01.

| t* (s/forward) | C01 | C2 | C3 | worst case s | GPU-h |
|---|---|---|---|---|---|
| 0.050 | 7,200 | 12,600 | 19,860 | 39,660 | 11.0 |
| 0.070 | 7,800 | 12,600 | 20,460 | 40,860 | 11.3 |
| 0.090 | 8,400 | 12,600 | 21,060 | 42,060 | 11.7 |
| 0.100 | 8,700 | 12,900 | 21,660 | 43,260 | 12.0 |
| 0.117 | 9,600 | 14,400 | 24,060 | 48,060 | 13.35 |
| 0.149 | 10,800 | 17,100 | 27,960 | 55,860 | 15.5 |

C01 stays 7,200 only for t* ≤ 0.0517 s. That is p95 ≤ 41 ms, about the bandwidth floor (I-INFER, advisor `:47`). **Expect C01 > 7,200**, so the operator question in §F is needed in practice, not in theory.

## D. Closing the gap: rule, code, proof, worst case

**Rule.** The stage 0–1 deadline remains in force until stage 2 is entered. Prereg `:196` already says "the stage-2 clock starts on entry to stage 2". It never says the stage 0–1 clock ends early, so the stage-2 clock semantics are unchanged.

**Code** (proposal; test-first; a delta review by the advisor and GPT-6-Astra):
- `arms:106–110` `Budget.enter`: when `key == "stage2"`, first `self.check()` while stage01 is still active (an expired stage 0–1 refuses), then `self.complete01()`, then set the origin and add the scope as today.
- `arms:1259`: delete the `complete01()` call and keep `else: self.budget.future_stage2_s = 0.` as `if reading["next_stage"] != 2: …`.
- Existing selftest uses (`selftest:646`, `:650`, `:1286`) still hold, because `discard` is idempotent.

**Regression tests (each fails on today's code):**
- (i) Process 1: the stage-1 reading has `next_stage = 2` at C01 − 10, and no stage-2 call arrives. `check()` at C01 + 1 raises HALTED-BUDGET. Today it passes forever, because `deadline()` is None (`arms:96–97`).
- (ii) Astra's case: stage 1 done at 7,199, `enter(2)` at 7,201 with C01 = 7,200 → HALTED-BUDGET.
- (iii) Sampling the clock from origin to process close, `deadline()` is never None for a K1 survivor.
- (iv) Process 2 with C3 = C01 + C2 + 60: for every entry time e < C01, `deadline()` equals the inner deadline, never origin + C3.

**Proof (with the fix).** Origins are in `arms:87`, `:93` and `:109`. The only scope removal is `complete01` (`arms:112`), and after the fix it is called only from `enter(2)`.
- **Process 1, resident origin S₁** (`arms:1392`). Stage01 is active on [S₁, tₑ). `enter(2)` succeeds only if `clock < S₁ + C01` (strict, `arms:104`), so tₑ < S₁ + C01. Stage2 is active from tₑ to exit and is never removed, so exit ≤ tₑ + C2 + ε. A K1 terminal keeps stage01 to exit (`arms:1260`, `:1444–1445`).
- **Process 2, origin S₂** = the stage-3 call (`arms:1463`, `:1488`). Stage3 is active throughout (`arms:93`). By the same argument an inner scope is always active, with deadline < S₂ + C01 + C2 = S₂ + C3 − 60. So min() never selects stage3.
- ε = watchdog latency (≤ 0.1 s poll, `arms:1408`) + halt diagnostic writes before `os._exit` (`arms:1419–1423`). It is UNMEASURED but involves only file writes.

**Closed-form worst case.** GPU-resident time is T_max = (C01 + C2) + C3 + 2ε = 2·(C01 + C2) + 60 + 2ε.
- The model loads only after each origin (`Session` at `arms:1426`, torch import at `:340`), so pre-origin interpreter start-up holds no GPU.
- Between process 1's exit (`arms:1450–1451`) and the stage-3 call, no process holds the model. That is calendar time, not GPU time.
- The stage-0→1 hand-off was already inside C01 (`arms:1414–1416`), and after the fix the stage-1→2 hand-off is too.

**Expected cost (I-INFER, unmeasured).** At t = 0.1 s, a K1-killed attempt is ≈ 2.0–2.3 h (advisor `:112`). That is not a bound.

## E. Fallback if the benchmark is not run

C01 = **9,600**, C2 = **14,400**, C3 = **24,060**. Worst case = 2·(9,600 + 14,400) + 60 = **48,060 s = 13.35 GPU-h**.
- The values cover the repo's upper anchor, t = 0.117 s (`logs_run.log:71`). The formula needs 9,410 s there with O = 0 and Q = 480, so 190 s remain for unmeasured observe and preamble overrun.
- At 9,600, the P2 projection alone admits t ≤ 0.1215 s with the pad consumed (advisor `:83`).
- C3 is the advisor's 24,000 + 60 (advisory 8).

**Code and test changes for the ceiling (any value):**
- `arms:88` `5400.` → C01.
- `read:500` `==5400.` → `==C01`.
- `read:14` and `selftest:19` → the new prereg SHA.
- `selftest:223–224` fixture → C01.
- `selftest:633–639` `5500`/`5499`/`5501` → C01 + 100 / C01 + 99 / C01 + 101.
- `selftest:1020` `5399.` → C01 − 1.
- Plus the §D edits and the regression tests.

Gate: all 79 existing tests plus the new ones pass on CPU, then the advisor and GPT-6-Astra delta review.

**Prereg amendment** (append `## 9.`; frozen lines untouched): "Amendment B-1 (pre-observation, D-C10z-budget). Every statement of the 5,400-second stage 0–1 ceiling (`:18`, `:125`, `:127`, `:133`, `:196` three times, `:344`) reads C01 seconds, with C01 from [benchmark record path + SHA-256] by the stated formula. The stage 0–1 deadline remains in force until stage 2 is entered. Row 6's '≈ 1–2 h' is not met by this ceiling; the operator accepted the larger bound under D-C10z-budget. Nothing else changes: no gate, label, K1/K2 rule, projection, probe, round cap (V13) or never-zero rule. Ceilings never increase during an attempt. HALTED-BUDGET remains possible."

## F. Operator question (one D-C10z-budget row; plain words; recommendation first)

> **ASTRA time limits: three yes/no answers. I recommend yes to all three.**
>
> **1. A longer first phase.** The plan said ASTRA's first phase, the cheap check that can stop the experiment early, would take about 1 to 2 hours. Counting the work the code actually does, it needs more: probably 2 to 2½ hours, at most 3. Before starting, we would run a 10-minute speed test on the Mac and set the limit from its result, never above 3 hours. If the test says more than 3 hours, we stop and come back to you. If you prefer to skip the test, the limit would be 2 hours 40 minutes. *May the first phase run longer than 2 hours, up to 3 hours?*
>
> **2. The overall time limits (plan decision 2).** If ASTRA passes its early check and every later phase ran to its limit, it could keep the GPU busy for about 11 to 13½ hours in total, split over two separate runs, and never more than about 15½ hours. These are upper limits, not expected times. If it stops at the early check, it should take about 2 to 2½ hours, but that is an estimate, not yet measured. Nothing else uses the GPU while it runs. This includes a small fix so the program can no longer sit idle holding the GPU between phases. *Do you accept these limits and the fix?*
>
> **3. What a success would mean (plan decision 1).** If ASTRA works, we would recommend counting its method as an acceptable way to write facts into the model. That is a statement about the method only. It would not settle speed in real use, exact repeatability, storage fit or rule compliance, which all stay open. Calling it "just a measurement" instead changes no test and no result label. *Recommend "write-qualifies"?*

Recording: one runbook §5 row, D-C10z-budget, quoting the operator's words for 1–3, the chosen path (benchmark or fallback) and the resulting C01/C2/C3. The go record follows only after that row exists:

```json
{"decisions":{"0":"D-C10r-rulings-10","1":"D-C10z-budget","2":"D-C10z-budget"},
 "operator_yes":true,"one_gpu_job":true,
 "recorded_by":"program session relaying operator answers recorded under D-C10z-budget (EXPERIMENT_RUNBOOK.md §5)",
 "recorded_at":"<real ISO-8601 time at write>"}
```

The record goes at `results/c10z_astra_go_record.json`, outside OUT_DIR. `arms:1342–1361` checks only its format, so grep §5 for both IDs by hand.

## G. Launch (after amendment, code, selftest, reviews, operator yes, go record, engine fingerprint PASS, GPU idle, clean env)

Wrapper `tools/run_c10z_attempt.sh`, added with the code change and reviewed with it. Each stage is still a separate invocation of `run_c10z_stage.sh` (`run_c10z_stage.sh:2`).

```bash
#!/bin/bash
set -u
W="$(cd "$(dirname "$0")/.." && pwd)" || exit 2
S="$W/tools/run_c10z_stage.sh"; OUT="${C10Z_OUT_DIR:?C10Z_OUT_DIR required}"
step(){ "$S" "$1"; rc=$?; echo "STAGE_${1}_EXIT=$rc"; return "$rc"; }
step 0 || exit $?
step 1 || exit $?
next=$("$W/.venv/bin/python" -I -c 'import json,sys;r=json.load(open(sys.argv[1]));print((r.get("reading") or {}).get("next_stage"))' "$OUT/run.json") || { echo "STAGE1_READ_FAILED"; exit 3; }
echo "STAGE1_NEXT=$next"
[ "$next" = "2" ] || exit 0
step 2; exit $?
```

- **Process 1:** `nohup caffeinate -i env LLMDB_ROOT="$W" C10Z_OUT_DIR="$W/results/c10z_astra" C10Z_GO_RECORD="$W/results/c10z_astra_go_record.json" C10Z_STAGE2_CEILING_S=<C2> C10Z_STAGE3_CEILING_S=<C3> "$W/tools/run_c10z_attempt.sh" > "$W/results/c10z_astra_chain.log" 2>&1 &`
- **Stage 3**, only if the stage-2 reading has `next_stage == 3` (`arms:1480–1483`): the same `env`, `nohup caffeinate -i bash -c '"$1" 3; rc=$?; echo "STAGE_3_EXIT=$rc"; exit "$rc"' _ "$W/tools/run_c10z_stage.sh" > "$W/results/c10z_astra_stage3.log" 2>&1 &`. Process 2 runs inside this caller (`arms:1488`), so it must be `nohup`.

Launch risks carried from v1 (`proposal.md:104–112`), unchanged:
- wrong tree;
- inherited env;
- fresh OUT_DIR (`arms:1465`);
- heartbeat ≤ 15 s (`arms:1513–1515`): start right after a backup;
- a second MPS job: confirm the GPU is idle.
