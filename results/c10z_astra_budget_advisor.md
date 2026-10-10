FIX-FIRST

# ASTRA (D-C10z-astra) budget proposal: independent advisor review

**Reviewer:** Claude Opus 5.5 advisor subagent (not the author), 2026-10-07.
**Under review:** `results/c10z_astra_budget_proposal.md` (proposed C01 = 7,200 s amendment; C2 = 12,600 s; C3 = 19,800 s; go record; launch plan).
**Scope:** read-only. No GPU, no model load. I re-read every cited line in `experiments/track_c/c10z_astra_arms.py`, `c10z_astra_read.py` and `c10z_astra_selftest.py`, plus `tools/run_c10z_stage.sh`, `docs/C10Z_ASTRA_PREREG.md`, `experiments/track_c/c10e_bandknob.py` and the c10q logs. I recomputed every number from the code's constants.
**State checks:** `results/c10z_astra/` is absent (ls, 2026-10-07). The prereg SHA-256 is `38f8b68c…b072` (shasum), which equals `c10z_astra_read.py:14` and `c10z_astra_selftest.py:19`. The CPU selftest reran here with `C10Z_ASTRA_SELFTEST_PASS tests=79` (65.6 s).

## Verdict and the single most important next step

The diagnosis is right, and it is stronger than the proposal states: 5,400 s cannot pass the post-baseline projection on this Mac, even in the best physical case. The fix is also the right kind of fix: a pre-observation amendment that changes one number and drops no gate. **The number 7,200 is not grounded, though.** It comes from allowance arithmetic. The code's own work count for stage-0 step 4 is about 26,200–26,700 sequential batch-1 forwards, and 7,200 passes the arms:847 projection only if one forward takes ≤ 52–87 ms. The only repo anchor allows up to ≈ 117 ms. So 7,200 may still end HALTED-BUDGET about 1.5–2.3 h into the GPU slot.

**Next step:** before fixing the number, run the cheapest falsifier. That is a ≤ 10-min MPS micro-benchmark of one batch-1 `use_cache=False`, `logits_to_keep=0` Qwen2.5-3B forward at probe-prompt length. Then set C01, C2 and C3 from the formula in B1. If the operator declines the benchmark, use the anchor-covering values in B1 (9,600 / 14,400 / 24,000).

## Arithmetic I recomputed (agrees with the proposal unless noted)

- **Allowances.** 120 + 2,040 + 300 + 120 + 1,380 + 1,200 + 180 = 5,340 (`arms:32–33`). Slack under 5,400 = 60. ✔
- **P0 (`arms:337`).** Elapsed ≤ 5,400 − 5,340 = 60. ✔
- **P1 (`arms:796`).** Remaining 5,220; elapsed ≤ 180. ✔
- **P2 (`arms:847–848`).** Remaining 300 + 120 + V + 1,200 + 180 = 1,800 + V; elapsed ≤ 3,600 − V = 2,220 at V = 1,380. ✔
- **P3 (`arms:857`), stage-1 entry (`:1253`), write start (`:709`) and round 0 (`:714`).** Remaining 1,380 + V; elapsed ≤ 2,640. ✔
- **V.** max(1,380, Σ last-3 `locality_probes` + Σ last-3 `binding_evaluation`) (`arms:762–763`). ✔
- **Stage-2 entry minimum (`arms:1265`).** 3,600 + 3·1,380 + 180 = 7,920 = `future_stage2_s` (`arms:90`). A ceiling of exactly 7,920 refuses, because elapsed > 0 and the test is `≤` (`arms:124`). ✔
- **Stage-3 first projection, process 2.** 5,340 + 7,920 = 13,260 (`arms:337`, `:118`). ✔
- **Worst case as proposed.** (7,200 + 12,600) + 19,800 = 39,600 s = 11.0 h. ✔
- **The c10q anchor (passS → passSsham → passSperm).** 02:52:40 → 03:23:05 → 03:54:22 (`ls -lT results/c10q_stacked/`), which is 1,825 s and 1,877 s. The log agrees: `(1826s)` and `(1877s)` (`results/c10q_stacked/logs_run.log:82`, `:112`). ✔ Those passes include the stacked hook (174 s in sham, `logs_run.log:71`), so a recipe-A-only pass is ≈ 1,650–1,700 s. That is I-INFER, and it is slightly *better* than the proposal assumes.

### What the proposal did not compute: the work in stage-0 step 4

The work is deterministic in the code, so I counted forwards rather than leaving the cost as a range.

- **A7 token lengths are measured, not [3, 6].** `A7_coined_coined … ntok=5.5 range=[4, 6]` (`results/c10q_stacked/logs_run.log:15`). The harness has not changed since that run: last commit `b3c21ae`, 2026-10-06 00:46, before the 02:12 start (`git log -- experiments/track_c/c10e_bandknob.py`). So ΣT = 132, Σ(T−1) = 108 → **3,888 F1 prefix probes**, not "1,728–4,320". With T ∈ {4, 5, 6} and mean 5.5, Σ T(T−1)/2 = 300–306.
- **Each probe costs (T − depth) forwards, not one.** `greedy` runs one batch-1, no-cache forward per remaining target token (`arms:550–558`). The population is 6 views (`arms:428–431`) × 24 facts × depths × 6 `FRAME_SUBJECTS` (`arms:26`, `:560–579`). Forwards per probe set:
  - p7 = 36·(300..306) + (300..306) + 36 F0 + 48 relations = **11,184–11,406**;
  - p2 = 864 + 24 + 84 = **972**;
  - p1 = **84**;
  - P = p1 + p2 + p7 = **12,240–12,462**.
- **Evaluator forwards** (`c10e_bandknob.py:358–375`). Per fact: T (canon) + 3T (`full_seq_match`, `:109–117`) + 3(T−1) (`teacher_forced_pertok`, `:134ff`) + 3(T+2) (`string_match`, `:121–130`) = 10T + 3, with 3 PTEST prompts (`:52–55`). That gives e7 = **1,392**, e2 = 552 and e1 = 312.
- **Stage-0 step 4** (`arms:811–845`). It runs pristine probes for all arms (P) and deferred probes for all arms (P), plus e7 (`:823`), Z0 (24 + 132 forwards, `:862–870`), four L1/L3/generic axes passes and about 10 batched observes. Total ≈ **26,200–26,700 batch-1 forwards**.
- **V at P2.** The last three probe sets are the deferred p1, p2 and p7. The last three evaluations are recipe-A A2, recipe-A A7 and pristine A7 (`eval_guard` is installed at `:372`, before recipe A; the harness calls `eval_arm` at `c10e:491`). V = P + e2 + 2·e7 ≈ **15,576–15,798 forwards × t**.
- **V at stage-2 entry.** The last three probe sets become p2, deferred p7 and Z-A7 p7 (`:668`); the last three evaluations become three A7 evaluations. V₂ = p2 + 2·p7 + 3·e7 ≈ **27,516–27,960 forwards × t**, ≈ 1.77 × V_P2.

**Per-forward time t.**
- *UNMEASURED for ASTRA.*
- *Upper anchor:* the c10q sham hook ran a second edit plus about 1,482 forwards (e7 1,392 + 24 `described_as` + 12 frame + about 54 axes) in 174 s (`logs_run.log:71`; hook body `c10q_stacked_arms.py:36–60`). So t ≤ 0.117 s.
- *Physical floor (I-INFER, UNVERIFIABLE in repo):* about 6.2 GB of fp16 weights must be read per batch-1 forward, at the public M3 Pro bandwidth of 150 GB/s, so t ≥ ≈ 0.041 s.

**P2 under C01 = 7,200.** The projection passes iff 120 + t_A + 26,680·t + 1,800 + max(1,380, 15,798·t) ≤ 7,200.
- With t_A = 2,040 (the allowance) and the 480 s pad consumed after P2: t ≤ **0.052 s**.
- With no pad consumed: t ≤ **0.070 s**.
- With t_A = 1,650 (the c10q-derived value): t ≤ **0.069 s** with the pad consumed, or **0.087 s** without it.

The break-even therefore sits in the middle of the plausible range [0.041, 0.117]. **7,200 is a coin flip, not a bound.**

Under 5,400, P2 needs 26,680·t ≤ 2,220 − t_A − 120 < 400 s, so t < 0.015 s, which is below the bandwidth floor. **5,400 cannot pass**, which confirms the proposal's §1 verdict with certainty rather than "very likely".

## BLOCKING

### B1 — The 7,200 s ceiling is not justified by the work the code will do; measure t, then size C01, C2 and C3 from it

**Defect.** The amendment's "Basis for 7,200 s" (5,340 + 1,380 + 480) budgets about 1,440 s (1,380 + 60) of slack for stage-0 step 4. Step 4 is ≈ 26,700 sequential forwards: about 1,100 s at the physical floor and ≈ 2,700 s at t = 0.1 s. In practice, that "1,380 counted again" term is the only room step 4 has, and it is sized from an allowance, not from the code's work. The proposal states "No MPS measurement of any ASTRA component exists" but then fixes a number that depends on exactly that measurement. The implementation advisory it cites asked for a measurement first ("measure recipe A and one F1 probe pass on the Mac … before granting the go", `results/c10z_astra_advisor_impl.md:51–53`).

**Replacement (preferred).** Insert a step 0 in the launch order, before the amendment's number is written:

> 0. **MPS forward benchmark (infra, not an ASTRA observation; GPU idle; ≤ 10 min; its own results path, never `results/c10z_astra/`).** Load the harness model as `c10e_bandknob` does (fp16, MPS, `use_cache=False`). Time ≥ 200 synchronized batch-1 forwards with `logits_to_keep=0` on F1-shaped inputs: a frozen-view CANON prompt for a `FRAME_SUBJECT` plus 1–5 A7 target tokens. Record the median and p90. Optionally time one `eval_arm(A7)` (1,392 forwards) as a cross-check. Set t* = 1.15 × p90.

Then the amendment reads, in place of "Basis for 7,200 s":

> **Basis.** C01 = 300·⌈(4,440 + 26,680·t* + max(1,380, 15,798·t*)) / 300⌉, where 4,440 = import/pin 120 + recipe A 2,040 + post-baseline projection 1,800 + 480 for the unallowanced stage-0→1 hand-off and stage-1 recipe preamble. 26,680 and 15,798 are the stage-0 step-4 and P2-validation forward counts derived from `c10z_astra_arms.py:550–600`, `:811–845` and `c10e_bandknob.py:358–375`, with A7 ntok = 5.5, range [4, 6] (`results/c10q_stacked/logs_run.log:15`). t* = 1.15 × the p90 measured s/forward, from [benchmark artifact path]. C2 = max(12,600, 300·⌈(3,780 + 3·max(1,380, 27,960·t*)) / 300⌉). C3 = C01 + C2.

Resulting values:

| t* (s/forward) | C01 | C2 | C3 | worst case |
|---|---|---|---|---|
| ≤ 0.052 | 7,200 | 12,600 | 19,800 | 11.0 h (the proposal stands) |
| ≤ 0.070 | 7,800 | 12,600 | 20,400 | 11.3 h |
| ≤ 0.090 | 8,400 | 12,600 | 21,000 | 11.7 h |
| ≤ 0.120 | 9,600 | 14,400 | 24,000 | 13.3 h |
| > 0.120 | STOP: stage 0–1 is not a cheap early-kill; return to the operator | | | |

**Replacement if the operator declines the benchmark.** Use C01 = **9,600**, C2 = **14,400** and C3 = **24,000**: worst case 48,000 s = 13.3 h. These cover the repo's upper anchor, t = 0.117.
- At C01 = 9,600 the P2 projection admits t ≤ 0.1215. Then V₂ ≤ 27,960 × 0.1215 ≈ 3,397, and the stage-2 entry needs ≤ 3,780 + 10,191 = 13,971 ≤ 14,400.
- Replace the code/test change list's `7200.`/`7300`/`7299`/`7301` with `9600.`/`9700`/`9699`/`9701` (or with the benchmark-derived C01 + 100, C01 + 99 and C01 + 101).

**Row-6 consequence (must be stated in the amendment and put to the operator).** At any C01 > 7,200 the ceiling exceeds requirement row 6's "cheap early-kill stage (≈ 1–2 h)" (prereg `:18`). Add to the amendment:

> Row 6's "≈ 1–2 h" is not met by this ceiling; the F1 all-view/all-depth probe population (§2.9, `:163`) makes stage 0 alone ≈ 2·12,4xx + 1,392 forwards. The operator accepts the larger bound under D-C10z-budget, or rules on re-scoping the probe population as a separate pre-registration.

I do not recommend re-scoping: that is a science change. The choice belongs to the operator.

**Consistency check.** The proposal's C2 = 12,600 *is* adequate for C01 = 7,200 under the forward model. Any run that passes P2 at 7,200 has t ≤ 0.087, so V₂ ≤ ≈ 2,430 and the stage-2 entry needs ≤ ≈ 11,070. So C2 changes only if C01 rises above ≈ 8,400.

### B2 — The go record's decision "1" must cite an explicit operator answer, not an inferred one

**Defect.** The draft record sets `"1": "D-C10r-rulings-10"`. The proposal concedes that rulings-10 does not record an answer to decision 1 (write qualification, prereg `:343`): the row's item (2) is only "ASTRA (C10Z) go, with the program proposing its time budget" (`EXPERIMENT_RUNBOOK.md:351`). `go_record` checks only the format of the Decision-ID, not its existence or content (`arms:1352–1355`). So a record that asserts `operator_yes: true` against a decision the operator did not explicitly answer would pass the code. The program must not author operator consent by inference.

**Replacement.** Put decisions 1 and 2 to the operator in the same D-C10z-budget question, then write:

```json
"decisions": {"0": "D-C10r-rulings-10", "1": "D-C10z-budget", "2": "D-C10z-budget"}
```

The D-C10z-budget row must quote the operator's yes to (a) decision 1 (WRITE-QUALIFIES recommendation; "a measurement ruling changes no gate or label", prereg `:343`), (b) the amended C01 and its basis, and (c) the C2/C3 numbers and the worst case in GPU-hours. Write `recorded_at` as the real ISO time the file is written, never the `T00:00:00` placeholder.

## ADVISORY

1. **Raising the ceiling drops no gate (verified).** The stage-01 value enters only `Budget.durations`, `deadline` and `project` (`arms:88`, `:95–126`), the reader's provenance equality (`read:500`), and presence-only tests (`read:501–505`, `:574`, `:589`). The other limits are fixed constants that do not depend on any ceiling: -EXCEEDS-TTL is 3,600 s (`read:571`), the V13 round halt is 120 s (`arms:78–79`, `read:538`), and the memory guard is fixed (`arms:73–75`). The recorded-projection audit (`read:519–524`) checks each projection against its own recorded ceiling.
2. **Child start-up is not on the clock.** The origin is `time.monotonic()` at `resident()` entry (`arms:1392`), after the child's interpreter and module import. The torch import and model load are inside `Session.__init__` (`arms:340–342`), which `import_and_pin` covers. The "child start-up (≤ 60 s)" part of the 480 is therefore mis-attributed. The real stage-0→1 hand-off (parent poll at 0.1 s, `arms:1500–1519`; new interpreter; `requested` write, `:1496`) takes seconds, not 120. Keep 480 as an unattributed pad, but describe it as "stage-1 recipe preamble (`compute_P`, LAW#5 with two single-request edits, `cov_cache_sha256`, `axes_pre`, 24 pre-locality predicts; `c10e_bandknob.py:459–477`), Z1–Z7 verification beyond the 420 s D+G allowance, and hand-off". All of these are UNMEASURED.
3. **Count fix in the amendment.** "5,400-second" occurs **three** times at `:196`, not twice (grep). The blanket "every statement … reads 7,200" covers it, but the citation list should say ":196 (three times)". Also use `## 9.` rather than `### 9.`: the last top-level section is `## 8` (`:367`), with `### 8.2` at `:433`.
4. **Replace the V ≤ 2,910 argument** in proposal §3 with the forward-ratio bound V₂ ≈ 1.77 × V_P2 (counts above). The e_w ≥ V argument is valid (the intervals are disjoint and precede the write), but it is loose, and the proposal itself flags it as UNVERIFIABLE at stage-2 entry.
5. **Restate the expected-cost line with the forward count.** At t = 0.1, a K1-killed attempt is ≈ 60 + 1,650 + 2,650 + D/G + verification + stage 1 (≈ 200 + ≤ 1,200 + p7 + e7 ≈ 1,260) ≈ 2.0–2.3 h, not "1.5–2 h". Expected costs are I-INFER until the benchmark exists.
6. **The launch chain prints `STAGE_EXIT=2` after a clean K1 kill.** Stage 1 returns 0 on a K1 verdict (`arms:1505–1507`), so `&&` runs stage 2. Stage 2 then refuses at `:1489–1490`, because `run.closed` is true, and the refusal writes no files (`arms:1527–1529`). This is harmless but misleading. Either document "rc 2 from the stage-2 call after a K1 verdict is expected", or gate stage 2 on the stage-1 printout's `next_stage == 2`. (The proposal's note cites `:1489–1494`; the K1 refusal path is `:1489–1490`.)
7. **Stage 3 runs the model in the foreground caller process** (`resident(p2, 2, …)` inside `stage_call(3)`, `arms:1488`), with no child and no heartbeat parent. Launch it with the same `nohup caffeinate -i env …` wrapper and its own log, or a closed terminal kills process 2.
8. **C3 = C01 + C2 can bind by milliseconds.** In process 2 the stage-2 origin is taken at `enter(2)` (`arms:109`, `:1264`), after the last stage-01 check (`:1258`). So the stage-2 deadline can sit ε past start + C3. Add 60 s (C3 = C01 + C2 + 60) if C3 must never be the governing deadline. Otherwise this is immaterial.
9. **Selftest intent.** `test_review_write_prestart_projection_refuses_before_observation` uses `clock=lambda: 5399.` (`selftest:1020`). It still passes at a larger C01, because the projection exceeds the ceiling either way, but it no longer tests "just under the deadline". Move it to C01 − 1 alongside the `:633–639` edits. The other ceiling fixtures (`12000.`/`24000.` at `:223`, `:262`, `:1147`, `:1170`) need no change. Besides `read:14` and `selftest:19`, no other code pins the prereg SHA (grep `38f8b68c`: only those two code files plus three results reviews). The driver and reader SHAs are bound at run time in H_in (`arms:1162`), not pinned, so the code edits need only the selftest plus the advisor and GPT-6-Astra delta reviews.
10. **Verified as cited:**
    - go-record checks (`arms:1342–1361`);
    - H_in binding of `go_sha256` (`arms:1163`);
    - launch inputs read only at stage 0 (`arms:1467–1470`) and frozen against later env (`:1495`);
    - fresh OUT_DIR (`:1465`);
    - heartbeat ≤ 15 s (`:1513–1515`) with 1 s fsync'd writes (`:51–55`, `:1410–1413`);
    - idle watchdog deadline (`:1414–1416`);
    - no deadline between stage 1 and stage 2 (`:95–97`, `:1259`);
    - stage-3 clock at the call (`:1463`, `:1488`);
    - env preflight (`:28–29`, `:65–70`);
    - launcher derives W from its own path and execs `$W/.venv` (`run_c10z_stage.sh:6`, `:12`).

    The disk contention from `com.rhu.memit-backup` and the "loaded" state of that launchd job are UNVERIFIABLE here (not checked).

## Overturning test (prereg review item 4)

The cheapest experiment that could falsify the budget is the B1 step-0 benchmark: ≤ 10 GPU-minutes, versus ≈ 1.5–2.3 GPU-hours lost if 7,200 refuses at P2. If p90 × 1.15 ≤ 0.052 s/forward, the proposal's numbers stand unchanged. Otherwise they are refuted in advance.

## Drift check

This is on-path. ASTRA is the operator-authorized next C10 falsifier (D-C10r-rulings-10 (2), `EXPERIMENT_RUNBOOK.md:351`). Budget sizing is a prerequisite for a run that can produce a verdict instead of HALTED-BUDGET. It changes no gate, label or K1/K2 rule.
