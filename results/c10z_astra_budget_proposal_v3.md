RECOMMENDATION: First run a ≤ 10-minute MPS speed benchmark (§B; build brief `results/c10z_astra_benchmark_spec_v2.md`). Then set the three ASTRA ceilings from one stated formula (§C):
- stage 0–1: C01 = max(7,200, R(…)), launched only if C01 ≤ 10,800;
- stage 2: C2 = max(12,600, R(…));
- stage 3: C3 = C01 + C2 + 60.

Close the stage-1→2 idle gap with a locked, install-before-remove deadline transition (§D). Treat every ceiling as a *nominal* deadline: the program stops itself, and stopping takes an extra, unmeasured amount of time. The no-benchmark caps 9,600 / 14,400 / 24,060 s are discretionary and used only if the operator chooses that path (§E). One D-C10z-budget operator answer (§F) comes before anything is written or launched.

Author: Claude Opus 5.5 subagent, 2026-10-07. Status: DRAFT v3. It supersedes `results/c10z_astra_budget_proposal_v2.md`, which is left unchanged. Drafting only: no prereg, code, tracker or runbook has been edited, and nothing has run.
Reviews folded:
- v2 re-reviews: GPT-6-Astra `results/c10z_astra_budget_v2_astra.md` (FIX-FIRST, 7 BLOCKING) and Opus advisor `results/c10z_astra_budget_v2_advisor.md` (FIX-FIRST, 4 BLOCKING). Where they overlap, both are satisfied; where they conflict, the stricter option is taken (the conflict is noted in the table).
- v1 reviews (`results/c10z_astra_budget_astra.md`, `results/c10z_astra_budget_advisor.md`): folded in v2 §A. The v2 advisor confirms all six resolved or correctly routed (`v2_advisor.md:23–30`). Astra-2 is re-opened by v2-Astra-2/3 and is closed here.

Abbreviations: `arms` = `experiments/track_c/c10z_astra_arms.py`, `read` = `experiments/track_c/c10z_astra_read.py`, `selftest` = `experiments/track_c/c10z_astra_selftest.py`, `c10e` = `experiments/track_c/c10e_bandknob.py`, `prereg` = `docs/C10Z_ASTRA_PREREG.md` (SHA-256 `38f8b68c…b072` = `read:14`). Runbook rows are cited by Decision-ID (runbook §5), not by line.

## A. Fold table: every BLOCKING item of both v2 reviews

| # | item (review file:line) | verified | v3 resolution |
|---|---|---|---|
| Astra-v2-1 | benchmark omits `torch.no_grad()`; generated tokens must be appended as `arms:557` (`v2_astra.md:5`) | Yes. `greedy` runs under `torch.no_grad()` (`arms:553`), as does the single-token probe (`arms:593`). Each step appends the model's own argmax token (`arms:557`). | Spec v2 §2 step 5: every warm-up and timed forward (probe, batch, eval) runs under `torch.no_grad()`. Each item runs the `arms:552–558` loop exactly (`cur.append(token)`), and stub test 2b asserts `torch.is_grad_enabled() is False` inside every forward. |
| Astra-v2-2 | deadline transition still has a gap: removal before install, second clock read, unsynchronized access (`v2_astra.md:7–9`) | Yes. v2's order is check, discard stage01, then `origins["stage2"]=clock()` (`arms:109`), which reads the clock twice and leaves `deadline()` = None in between (`arms:96–97`). The watchdog thread reads `deadline()` concurrently (`arms:1414`). Astra and the advisor both report that v2's test (iv) already passes today. | §D code: one captured `now`, validated against stage01; stage2 is installed before stage01 is removed; all of this sits under a `Budget` lock that `deadline()` also takes. This also satisfies advisor A3 (`v2_advisor.md:215–223`). Tests (i)–(iv) are rewritten to fail today (advisor B1 text), and the old (iv) is kept as invariant (vii). New tests: (vi) mutation-point sampling (never None) and (viii) clock crossing at exactly C01. |
| Astra-v2-3 | hard worst case not established: heartbeat I/O and `publication_lock` precede exit (`v2_astra.md:11–13`) | Yes. The watchdog writes the heartbeat before testing expiry (`arms:1410–1416`), then takes `publication_lock` and writes diagnostics before `os._exit` (`arms:1419–1423`). | §D: ceilings are called **nominal deadlines with an unmeasured termination overrun**. No hard bound is claimed, and independent termination is not proposed (it would need another reviewed change). The nominal GPU-resident supremum is **2·(C01 + C2)**. C3's +60 is slack, not attained. "Never more than" is withdrawn, and the idle wording is replaced (§F Q2, with advisor B4's text). |
| Astra-v2-4 | "p95 ≥ mean" is false (`v2_astra.md:15`) | Yes. Astra's counterexample: 99 samples of 1 and one of 10,000 give p95 = 1 and mean = 100.99. | §C: t* = 1.25 × max(p95, mean, eval_s/1,392), called a **prospective sizing heuristic**. The 1.25 proves no coverage, and HALTED-BUDGET remains possible. |
| Astra-v2-5 | formula lacks the 7,200 floor; fallback treats raw 0.117 as t* (`v2_astra.md:17–19`) | Yes. t* = 0.030 gives a pre-round sum of 6,620 → 6,900 without a floor. At t* = 1.25 × 0.117 = 0.14625, the formula gives 10,800 / 16,800 / 27,660. | §C: C01 = max(7,200, R(…)). §E: 9,600 / 14,400 / 24,060 are **discretionary caps, not formula-derived**. The 0.117 anchor carries no safety factor and is itself an upper bound (`logs_run.log:71` includes a second edit; advisor A8). The amendment gets a fallback branch (§E (c)). |
| Astra-v2-6 | a CAPPED benchmark silently becomes the smaller fallback (`v2_astra.md:21`) | Yes, at spec v1 `:56` vs `:70`/`:116`. | Spec v2: `ceilings()` returns BENCHMARK numbers for COMPLETE and CAPPED records, and **REFUSED** (no numbers) for INVALID, INTERRUPTED or incomplete mandatory evidence. The fallback is a separate constant used **only** when D-C10z-budget records the operator's no-benchmark choice. The final status is set before `derived` is computed. **Conflict with advisor B2's test 11** (INVALID → fallback): the stricter Astra rule is taken. A refused benchmark is rerun once in a new directory, or the question goes back to the operator. |
| Astra-v2-7 | benchmark lifecycle: supervision after preflight, optional before-hash, no reserve, interrupted runs (`v2_astra.md:23`) | Yes (spec v1 `:62`, `:64`, `:73`). | Spec v2 §2: a parent **supervisor** process starts first (no torch) and SIGKILLs the worker's process group at 600 s, independent of worker I/O. A real-process CPU test proves the kill. Before and after hashes are **mandatory**. The reserve is sized from the measured before-hash time. An interrupted run is INTERRUPTED and unusable. |
| Adv-v2-B1 | regression tests would not fail today; drive the real `Session.stage1`; structural test; drop `complete01` calls in selftest (`v2_advisor.md:97–112`) | Yes. `Session` is never built in selftests (`arms:323`). Selftest `:646`, `:650` and `:1286` call `complete01()` themselves. | §D adopts the advisor's replacement text verbatim, adjusted to the locked transition, plus (v) the structural test: `complete01` is referenced only in `Budget.enter`. Order: run on today's code, record the failures, then fix. |
| Adv-v2-B2 | spec: CAPPED/FALLBACK contradiction, overlapping statuses, watchdog trip discards a completed measurement (`v2_advisor.md:114–147`) | Yes. | Spec v2 adopts the exact non-overlapping statuses (COMPLETE iff n ≥ 400; CAPPED iff the guard stopped it with 200 ≤ n < 400; INVALID iff n < 200). `derived` and the top-level status are written after every phase. The SVD runs in a killable child stopped at 565 s (TIMEOUT, labelled lower bound). Optional phases never change the top-level status. Test 11 is corrected, with the fallback replaced by REFUSED per Astra-v2-6. §3 requires `derived` to be present. |
| Adv-v2-B3 | the amendment never states its formula, has no fallback branch, and its row-6 sentence is unconditional (`v2_advisor.md:149–181`) | Yes (v2 `:138`). | §E: the advisor's amendment text, updated for Astra-v2-4/5 (the mean term, the 7,200 floor, a discretionary fallback branch that only the operator selects, nominal deadlines) and Astra-v2-2 (install-before-remove). |
| Adv-v2-B4 | operator wording: the idle claim and decision 1's framing (`v2_advisor.md:183–203`) | Yes. | §F uses the advisor's Q2 sentence and Q3 verbatim, Astra's "allowed up to three hours" (`v2_astra.md:30`), and the recording note. "Never more than" is withdrawn (Astra-v2-3). |

Advisories adopted (text only):
- Runbook rows are cited by Decision-ID (advisor A2, `:214`).
- Exact transition ordering (advisor A3), folded into Astra-v2-2.
- `Path.resolve().is_relative_to(...)` for the out-path refusal, with a prefix test (advisor A4, `:224`).
- `logits_to_keep=0` passed explicitly in the batched forward, and the batch built by unbound `Session.make_batch` (advisor A5, `:225`).
- `minima_used` recorded for skipped phases, and `worst_case_s` defined (advisor A6, `:226`).
- C2's +600 relabelled as forced by the code's entry projection, not by work (advisor A7, `:227`).
- The fallback anchor carries no safety factor (advisor A8, `:228`).
- `C10Z_OUT_DIR` must be absolute (advisor A9, `:229`).
- Strict `next_stage` validation: only `null` or integer 2, otherwise a non-zero exit (Astra advisory `:29`).
- "Allowed up to" wording (Astra advisory `:30`).
- The per-forward `run.json` read and the 1 Hz heartbeat are reproduced inside the timed interval (advisor A1, `:209–213`); this also removes v2's false "byte-for-byte" claim.

## B. Benchmark: what is timed (build brief: `results/c10z_astra_benchmark_spec_v2.md`)

It is infra, not an ASTRA observation. It writes nothing under `results/c10z_astra/`, and the GPU must be idle (one GPU run at a time, D-C10r-rulings-10).

- **Model.** The model, dtype and device are the driver's: import `c10e_bandknob` with `LLMDB_ROOT`, `LLMDB_DEVICE=mps` and `HF_HOME` set as in `arms:339–342`. Assert MPS and fp16 (`arms:344`), set `use_cache=False` (`arms:345`), seed 0 (`arms:341`), and run `entry_preflight` (`arms:65–70`).
- **Prompts.** The probe set is built by the driver's own `Session.probe_population` (`arms:560–582`), called unbound. It uses the six templates logged at `results/c10q_stacked/logs_run.log:9`. These are length-representative only: the engine resamples templates per attempt (`memit_main.py:304–320`).
- **Timed unit: one greedy iteration.**
  - Inside the timed interval: a `Path.exists()` plus `json.loads(read_text())` of a run.json-shaped file on the same volume, standing in for `budget.check()` → `terminal_probe` (`arms:555`, `:1397`).
  - Under `torch.no_grad()`: `torch.tensor([cur])` → `model(…, use_cache=False, logits_to_keep=0).logits` → `int(logits[0,-1].argmax())` → `cur.append(token)` (`arms:553–557`).
  - A 1 Hz fsync heartbeat thread runs throughout (`arms:1408–1413`).
- **Counts.**
  - 20 warm-up forwards, then ≥ 400 timed (COMPLETE); 200–399 is CAPPED; fewer than 200 is INVALID.
  - Optional: a batched forward at the A7 identity-batch shape with `logits_to_keep=0` (`arms:433–446`, `:484–485`); one `eval_A7` cross-check of 1,392 forwards (`v1 advisor:39`); one CPU fp32 SVD of 11,008 × 11,008 (`c10e:166–178`) in a killable child.
  - Load and pin hashing are timed (`arms:356–364`).
  - The 36 `down_proj` hashes are taken before and after, and both are mandatory (`arms:293`).
- **Cap.** A supervisor process enforces 600 s from its own first statement. The worker starts forwards only within an internal 590 s, minus a reserve sized from the measured before-hash time.

## C. Formula: measured time → ceilings (single source of truth: `ceilings()` in the benchmark script)

**A sizing heuristic, not a guarantee.** The ceilings scale a sum of about 15,800–28,000 forwards. t* takes the largest of the p95, the mean and the evaluator's per-forward time, then multiplies by s = 1.25. That allows for what a 10-minute test cannot see: hours-long slowdowns (thermal, the 6-hourly backup on the same disk), evaluator overhead and `observe` hook overhead. Neither the statistic nor the factor proves coverage. **HALTED-BUDGET remains possible**, and it stays a clean halt, never a wrong label.

- t* = 1.25 × max(p95_probe, mean_probe, eval_A7_s / 1,392)
- I_pin = max(120, 1.25 × (load + pin)), with 120 = `ALLOWANCES["import_and_pin"]` (`arms:32`)
- O = 1.25 × 2 × 10 × p95_batch. These are the 10 step-4 `observe` calls (`arms:817`, `:820`, `:839`, `:844`). The ×2 hook factor is UNMEASURED, and O = 0 if skipped, which is recorded in `minima_used`.
- Q = max(480, 1.25 × 5 × t_svd + 300). This covers the post-P2 work that has no allowance: the stage-1 Z-recipe preamble (`c10e:462–476`, LAW#5 `:415–439`), Z1–Z7 verification beyond the D+G allowances (`arms:32`, `:849–851`) and the stage-1→2 hand-off. The 300 is UNMEASURED. A TIMEOUT SVD contributes its lower bound, labelled as such.
- R(x) = 300·⌈x/300⌉

**C01 = max(7,200, R(I_pin + 2,040 + 26,680·t* + O + 1,800 + max(1,380, 15,798·t*) + Q)).**
- This is the P2 projection (`arms:847–848`) plus the post-P2 pad.
- 2,040 = `ALLOWANCES["recipe_A"]` (`arms:32`). 26,680 and 15,798 are forward counts (`results/c10z_astra_budget_advisor.md:40–41`, recomputed at `v2_advisor.md:50–53`).
- The 7,200 floor is the top of row 6's "≈ 1–2 h" (`prereg:18`).
- **STOP if C01 > 10,800:** do not launch; return to the operator.

**C2 = max(12,600, R(3,780 + 3·max(1,380, 27,960·t*) + 600)).**
- C2 is **forced by the code's stage-2 entry projection** (`arms:1265`), not by the work stage 2 is expected to do. 3·V reserves about 83,900 forwards, while stage 2's actual validation is about 14,500 (`v2_advisor.md:227`).
- The +600 and the 12,600 floor are discretionary margin. Admission after K1 is still not guaranteed (Astra's v1 wording, kept).

**C3 = C01 + C2 + 60.** The +60 is slack: with §D in place, process 2's inner deadlines govern.

Values at I_pin = 120, O = 0 and Q = 480. Measured terms above these minima raise C01.

| t* (s) | pre-round C01 sum | C01 | C2 | C3 | nominal supremum 2·(C01+C2), s | h |
|---|---|---|---|---|---|---|
| 0.030 | 6,620.4 | 7,200 (floor) | 12,600 | 19,860 | 39,600 | 11.00 |
| 0.050 | 7,154.0 | 7,200 | 12,600 | 19,860 | 39,600 | 11.00 |
| 0.070 | 7,687.6 | 7,800 | 12,600 | 20,460 | 40,800 | 11.33 |
| 0.090 | 8,263.0 | 8,400 | 12,600 | 21,060 | 42,000 | 11.67 |
| 0.100 | 8,687.8 | 8,700 | 12,900 | 21,660 | 43,200 | 12.00 |
| 0.117 | 9,409.9 | 9,600 | 14,400 | 24,060 | 48,000 | 13.33 |
| 0.14625 (= 1.25 × 0.117) | 10,652.4 | 10,800 | 16,800 | 27,660 | 55,200 | 15.33 |
| 0.149 | 10,769.2 | 10,800 | 17,100 | 27,960 | 55,800 | 15.50 |

C01 > 7,200 once t* > 0.0517 (p95 or mean > 41.4 ms; `v2_advisor.md:57`). STOP begins at t* > 0.1497.

## D. Deadline transition: rule, code, tests, nominal worst case

**Rule.** The stage 0–1 deadline stays in force until stage 2 is entered. Entry captures one timestamp, validates it against stage 0–1, installs the stage-2 scope, and only then removes stage 0–1, all under one lock. Prereg `:196` ("the stage-2 clock starts on entry to stage 2") is unchanged.

**Code** (proposal; test-first; advisor + GPT-6-Astra delta review). `threading` is already imported (`arms:14`).

```python
# Budget.__init__ (arms:84-93): add
        self.lock=threading.RLock()
# arms:95-97
    def deadline(self):
        with self.lock:
            active=tuple(self.active)
            return min(self.origins[k]+self.durations[k] for k in active) if active else None
# arms:106-110
    def enter(self,stage):
        key="stage"+str(stage)
        R.require(self.durations.get(key) is not None,"HALTED-BUDGET","absent "+key+" ceiling")
        with self.lock:
            now=self.clock()
            if key=="stage2" and "stage01" in self.active:
                R.require(now<self.origins["stage01"]+self.durations["stage01"],"HALTED-BUDGET",
                          "stage 0-1 deadline expired before stage-2 entry")
            if key not in self.origins:self.origins[key]=now
            self.active.add(key)
            if key=="stage2":self.complete01()
        self.check()
# arms:1259-1260 becomes
        if reading["next_stage"]!=2:self.budget.future_stage2_s=0.
```

`complete01` (`arms:112`) is unchanged but is called only from `enter`. The other readers of `active` are `check` through `deadline` and `project` (`arms:118–124`). `project` runs on the main thread, the same thread as `enter`, so it needs no lock.

**Regression tests.** Each must fail on today's code; run them on today's code first and record the failures. This is the advisor's text (`v2_advisor.md:105–112`), adjusted:
- **Harness.** Each test drives the real `Session.stage1` (`arms:1252–1261`) unbound on a stub `self` with a fake-clock `Budget`. In the stub, `run_recipe`, `complete_recipe_readouts`, `write_checks` and `record` are no-ops, `remaining_validation` is bound from `Session`, `out` is a temp dir, and `R.read_process` is patched to return a K1-survivor reading `{"scientific_verdict": True, "next_stage": 2, …}`. Each test then calls `Budget.enter(2)`. No test calls `complete01()` itself.
- (i) Process 1, C01 = 7,200: stage 1 returns at 7,190, and there is no `enter(2)`. At clock 7,201, `budget.check()` raises HALTED-BUDGET. (Today `deadline()` is None.)
- (ii) Process 1, C01 = 7,200: stage 1 returns at 7,199, and `enter(2)` at 7,201 raises HALTED-BUDGET with `"stage2" not in origins`. (Today it succeeds.)
- (iii) Process 1: sample `deadline()` at every clock step through stage-1 return, the idle wait and `enter(2)`. It is never None, it equals origin + C01 before entry, and it equals entry + C2 after.
- (iv) Process 2 with C3 = C01 + C2 + 60: after stage-1 return and before `enter(2)`, `deadline()` equals origin + C01. After entry it equals entry + C2. It never equals origin + C3. (Today the pre-entry sample equals origin + C3.)
- (v) Structural: `complete01` is referenced only inside `Budget.enter` (AST check over `arms`).
- (vi) Mutation points: replace `budget.active` with a set subclass whose `add`/`discard` record `deadline()` after each mutation. During `enter(2)`, no recorded value is None. (Today's discard-then-add order records None.)
- (vii) Invariant (v2's old (iv), which passes today): for every entry time e < C01, `deadline()` after entry is e + C2 < origin + C3.
- (viii) Clock crossing: `enter(2)` with `now` = origin + C01 exactly refuses (strict `<`). `now` = origin + C01 − 0.001 is accepted, with `origins["stage2"]` equal to that same `now`: one read, so the clock stub counts exactly one call inside the lock.
- (ix) Concurrency: a thread calls `deadline()` in a tight loop while the main thread performs `enter(2)` 1,000 times on fresh Budgets. It never sees None and never raises `KeyError`.
- **Selftest edits.** Selftest `:646` and `:650` drop their explicit `b.complete01()`, and `SessionStub.stage1` (`:1286`) drops its `self.budget.complete01()`. All 79 existing tests plus (i)–(ix) pass.

**Nominal deadlines (Astra-v2-3).**
- **Process 1** (origin S₁, `arms:1392`). stage01 is active on [S₁, tₑ), and tₑ < S₁ + C01, validated on the single captured `now`. stage2 is active from tₑ until exit, and nothing removes it. A K1 terminal keeps stage01 until exit (`arms:1260`, `:1444–1445`). Process 2 (S₂ = the stage-3 call, `arms:1463`, `:1488`) behaves the same, inside stage3 (`arms:93`).
- **Stopping is not instantaneous.** At expiry, the watchdog has already done heartbeat I/O (`arms:1410–1413`). It then takes `publication_lock` and writes diagnostics before `os._exit` (`arms:1419–1423`). The main thread's own halt path also writes diagnostics (`arms:1452–1457`). These overruns are **UNMEASURED and not bounded**.
- **Nominal GPU-resident supremum: 2·(C01 + C2)**, plus an unmeasured termination overrun per process. C3 = C01 + C2 + 60 is slack, not attained. The model loads after each origin (`arms:1426`, `:340`). Between process 1's exit (`arms:1450–1451`) and the stage-3 call, no process holds the model. That is calendar time.
- **Not proposed:** an independent external kill of the resident. That would be a further reviewed change; the operator may ask for it.

**Expected cost (I-INFER).** About 2.0–2.3 h for a K1-killed attempt at t = 0.1 (`results/c10z_astra_budget_advisor.md:112`). Not a bound.

## E. Fallback, code changes, prereg amendment

**Fallback (operator-chosen only).** C01 = **9,600**, C2 = **14,400**, C3 = **24,060**, with a nominal supremum of 2·(9,600 + 14,400) = **48,000 s = 13.33 GPU-h**.
- These are **discretionary caps, not formula-derived.**
- The anchor t = 0.117 s (`logs_run.log:71`, 174 s over about 1,482 forwards) is raw: it carries no safety factor, and it is an upper bound, because those 174 s included a second edit.
- Applying s = 1.25 to it (t* = 0.14625) would give 10,800 / 16,800 / 27,660.
- At 9,600, the P2 projection admits a raw t ≤ 0.1215 s with the 480 pad consumed (`results/c10z_astra_budget_advisor.md:83`). HALTED-BUDGET is more likely on this path than on the benchmark path.
- A REFUSED or INTERRUPTED benchmark never selects the fallback.

**Code and test changes (any C01):**
- `arms:88` `5400.` → C01; `read:500` `==5400.` → `==C01`.
- `read:14` and `selftest:19` → the new prereg SHA.
- `selftest:223–224` → C01.
- `selftest:633–639` `5500`/`5499`/`5501` → C01 + 100 / C01 + 99 / C01 + 101; `selftest:1020` `5399.` → C01 − 1. These complete the grep set at `v2_advisor.md:46`.
- The §D edits and tests (i)–(ix).
- The new `tools/run_c10z_attempt.sh` (§G).

**Prereg amendment** (append `## 9.`; frozen lines untouched). This is the advisor's B3 text (`v2_advisor.md:159–181`), with the v3 changes in (a)–(c) and (e):

> ## 9. Amendment B-1 (pre-observation, D-C10z-budget)
>
> Written before any ASTRA process has started; `results/c10z_astra/` is absent.
>
> (a) **Ceiling.** Every statement of the 5,400-second stage 0–1 ceiling (`:18`, `:125`, `:127`, `:133`, `:196` three times, `:344`) reads C01 seconds. C01 is a prospective resource cap, not a measured completion estimate. Deadlines are nominal: the driver stops itself, and stopping overruns by an unmeasured amount. HALTED-BUDGET remains possible.
>
> (b) **Basis (benchmark path).** C01 = max(7,200, 300·⌈(I_pin + 2,040 + 26,680·t* + O + 1,800 + max(1,380, 15,798·t*) + Q)/300⌉), where:
> - t* = 1.25 × max(p95 s per probe-shaped forward, mean s per probe-shaped forward, eval_A7 s / 1,392), a prospective sizing heuristic;
> - I_pin = max(120, 1.25 × (load + pin s));
> - O = 1.25 × 20 × p95 of the A7 identity-batch forward (0 if skipped);
> - Q = max(480, 1.25 × 5 × SVD s + 300).
>
> All inputs come from benchmark record [path], SHA-256 [sha], whose status is COMPLETE or CAPPED, computed by `ceilings()` in `experiments/track_c/c10z_astra_benchmark.py` at SHA-256 [sha]. 26,680 and 15,798 are the stage-0 step-4 and P2-validation forward counts (`results/c10z_astra_budget_advisor.md:40–41`). If C01 > 10,800, the attempt is not launched.
>
> (c) **Fallback (only if D-C10z-budget records the operator's choice to skip the benchmark).** C01 = 9,600, a discretionary cap that is not derived from (b). A refused or interrupted benchmark does not select this branch.
>
> (d) **Launch inputs** (not prereg values; recorded for audit). C2 = max(12,600, 300·⌈(3,780 + 3·max(1,380, 27,960·t*) + 600)/300⌉), or 14,400 on the fallback. C3 = C01 + C2 + 60.
>
> (e) **Deadline scope.** The stage 0–1 deadline remains in force until stage 2 is entered. Entry captures one timestamp, refuses if it is not before the stage 0–1 deadline, and installs the stage-2 deadline before removing the stage 0–1 deadline. A K1 survivor whose stage-1 → stage-2 hand-off crosses C01 ends HALTED-BUDGET.
>
> (f) **Row 6.** If C01 > 7,200, row 6's '≈ 1–2 h' is not met by this ceiling; the operator accepted the larger bound under D-C10z-budget.
>
> Nothing else changes: no gate, label, K1/K2 rule, projection, probe, round cap (V13) or never-zero rule. Ceilings never increase during an attempt.

## F. Operator question (one D-C10z-budget row; recommendation first)

> **ASTRA time limits and one ruling: three yes/no answers. I recommend yes to all three.**
>
> **1. A longer first phase.** The plan said ASTRA's first phase, the cheap check that can stop the experiment early, would take about 1 to 2 hours. Counting the work the code actually does, it will likely need more. I ask that it be allowed up to 3 hours. Before starting, we would run a 10-minute speed test on the Mac and set the limit from its result: at least 2 hours, never above 3. If the test says more than 3 hours, we stop and come back to you. If you prefer to skip the test, the limit would be a fixed 2 hours 40 minutes, a judgement call rather than a measured figure. *May the first phase be allowed more than 2 hours, up to 3 hours?*
>
> **2. The overall time limits.** If ASTRA passes its early check and every later phase ran to its limit, its limits add up to about 11 to 13⅓ hours of GPU time in total, split over two separate runs. With the 3-hour first phase they could reach about 15½ hours. The program enforces these limits itself, and stopping takes a little extra time that we have not measured, so they are limits the program aims to stop at, not a guaranteed hard maximum. If it stops at the early check, it should take about 2 to 2½ hours, but that is an estimate, not yet measured. Nothing else uses the GPU while it runs. This includes a small fix: today, after the first phase passes, the program can sit idle holding the GPU for as long as no one starts the second phase. With the fix, that idle time counts against the first phase's limit. One side effect: if the second phase starts after that limit, the attempt stops as out of time. *Do you accept these limits and the fix?*
>
> **3. Does ASTRA's method count as a way of writing facts?** Before the run, the plan asks you to rule whether ASTRA's fixed, bounded calculation counts as a legitimate way to write facts into the model, or only as a measurement. Your answer changes no test and no result label. It only decides how a positive result is described afterwards. It would not settle speed in real use, exact repeatability, storage fit or compliance with the designated engine, which all stay open. I recommend that it counts. *Does it count as a way of writing facts?*

**Recording** (advisor B4 note, `v2_advisor.md:203`):
- Questions 1–2 approve bounds, not numbers that are still unknown: C01 ≤ 10,800 s and a nominal total ≤ 15.5 GPU-h, or the fallback 9,600 / 14,400 / 24,060.
- The D-C10z-budget row first quotes the yes. It then appends the chosen path, the benchmark path, its SHA-256, the computed C01/C2/C3 and any `minima_used`, before the go record is written.
- A STOP, or a benchmark refused twice, returns to the operator.

Go record (written only after that row exists; `arms:1342–1361` checks only the format, so grep runbook §5 for both IDs by hand):

```json
{"decisions":{"0":"D-C10r-rulings-10","1":"D-C10z-budget","2":"D-C10z-budget"},
 "operator_yes":true,"one_gpu_job":true,
 "recorded_by":"program session relaying operator answers recorded under D-C10z-budget (runbook §5)",
 "recorded_at":"<real ISO-8601 time at write>"}
```

## G. Launch (after the amendment, code change, selftest, reviews, operator yes, go record, engine fingerprint PASS, idle GPU and clean env)

Wrapper `tools/run_c10z_attempt.sh` (new, reviewed with the code change). Each stage stays a separate invocation (`run_c10z_stage.sh:2`).

```bash
#!/bin/bash
set -u
W="$(cd "$(dirname "$0")/.." && pwd)" || exit 2
S="$W/tools/run_c10z_stage.sh"; OUT="${C10Z_OUT_DIR:?C10Z_OUT_DIR required}"
case "$OUT" in /*) ;; *) echo "C10Z_OUT_DIR must be absolute"; exit 2 ;; esac
step(){ "$S" "$1"; rc=$?; echo "STAGE_${1}_EXIT=$rc"; return "$rc"; }
step 0 || exit $?
step 1 || exit $?
next=$("$W/.venv/bin/python" -I -c '
import json,sys
r=json.load(open(sys.argv[1])).get("reading")
if not isinstance(r,dict) or "next_stage" not in r: sys.exit(4)
n=r["next_stage"]
if n is None: print("null")
elif type(n) is int and n==2: print("2")
else: sys.exit(4)' "$OUT/run.json") || { rc=$?; echo "STAGE1_READING_INVALID rc=$rc"; exit 4; }
echo "STAGE1_NEXT=$next"
[ "$next" = "2" ] || exit 0
step 2; exit $?
```

- **Process 1:** `nohup caffeinate -i env LLMDB_ROOT="$W" C10Z_OUT_DIR="$W/results/c10z_astra" C10Z_GO_RECORD="$W/results/c10z_astra_go_record.json" C10Z_STAGE2_CEILING_S=<C2> C10Z_STAGE3_CEILING_S=<C3> "$W/tools/run_c10z_attempt.sh" > "$W/results/c10z_astra_chain.log" 2>&1 &`
- **The hand-off now spends C01 time.** Under §D the stage-1→2 hand-off counts against C01, so the wrapper must not pause between steps.
- **Stage 3,** only if the stage-2 reading's `next_stage` is exactly 3 (`arms:1480–1483` also checks): the same `env`, `nohup caffeinate -i bash -c '"$1" 3; rc=$?; echo "STAGE_3_EXIT=$rc"; exit "$rc"' _ "$W/tools/run_c10z_stage.sh" > "$W/results/c10z_astra_stage3.log" 2>&1 &`.
- **Launch risks carried from v1** (`results/c10z_astra_budget_proposal.md:104–112`):
  - wrong tree;
  - inherited env;
  - fresh OUT_DIR (`arms:1465`);
  - heartbeat ≤ 15 s (`arms:1513–1515`): start right after a backup;
  - a second MPS job: confirm the GPU is idle.
