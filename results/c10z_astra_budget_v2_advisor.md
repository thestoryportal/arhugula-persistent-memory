FIX-FIRST

# ASTRA budget proposal v2 and benchmark build spec: independent advisor review

**Reviewer:** Claude Opus 5.5 advisor subagent (not the author), 2026-10-07. Protocol: `tools/advisor_review_prompt.md`.
**Under review:** `results/c10z_astra_budget_proposal_v2.md` (v2) and `results/c10z_astra_benchmark_spec.md` (spec).
**Scope:** read-only. Nothing loaded a model or touched the GPU. I re-read every cited driver line with line numbers (`experiments/track_c/c10z_astra_arms.py`, abbreviated `arms`), plus `c10z_astra_read.py`, `c10z_astra_selftest.py`, `c10e_bandknob.py`, `tools/run_c10z_stage.sh`, `docs/C10Z_ASTRA_PREREG.md` (SHA-256 `38f8b68c…b072`, unchanged) and `results/c10q_stacked/logs_run.log`. I recomputed every number in v2 §C–§F.

## Verdict and the single most important next step

v2 is a large improvement. All six BLOCKING items from the two v1 reviews are resolved or routed to the operator correctly. Every forward count, formula, table row, fallback number and worst case recomputes exactly. The proposed deadline rule is sound, minimal and consistent with the prereg ("Stage 2 — automatic only for a clean K1 survivor (same process…)", prereg `:131`), so it removes no intended human pause.

Four things must change before it goes to the operator and Codex:
- **B1:** the regression tests as written would not all fail on today's code.
- **B2:** the benchmark spec contradicts itself on CAPPED records and on watchdog exits.
- **B3:** the prereg amendment points at a formula that it never states.
- **B4:** two sentences in the operator question are inaccurate.

**Next step:** apply the B1–B4 replacement texts below (documents only; no run needed), then send the spec to Codex.

## Check (1): earlier BLOCKING items

| item | status |
|---|---|
| Astra-1 (stage-2 window) | Resolved. C2 is sized from V at stage-2 entry. Astra's wording is adopted verbatim. V₂ = p2 + 2·p7 + 3·e7 matches the code: the stage-1 Z recipe evaluates A7 (`c10e:491` through `eval_guard`, `arms:372`) and then probes A7 (`arms:668`). So the last three probe sets at entry are deferred p2, deferred p7 and Z-A7 p7, and the last three evaluations are recipe-A A7, pristine A7 (`arms:823`) and Z-A7. |
| Astra-2 (unbounded gap; 11.0 h claim) | Resolved in design by §D, but the proof's regression tests have gaps (B1). |
| Astra-3 (honest basis) | Resolved in §B–C. The amendment text does not yet carry the basis (B3). |
| Astra-4a (exit handling) | Resolved. The wrapper logic is correct: `step 0 \|\| exit $?` propagates rc. A K1 terminal publishes `reading.next_stage = None` (`arms:1443`, `:1505`), which prints `None` → exit 0. A stage-1 halt makes `wait_stage` raise → rc 2 → exit. |
| Astra-4b / Adv-B2 (go provenance) | Correctly routed: decisions 1 and 2 → D-C10z-budget, with a real `recorded_at`. |
| Adv-B1 (7,200 ungrounded) | Resolved: benchmark → formula → fallback. Row-6 routed to the operator. |

## Check (2): driver claims against cited lines

All verified except the following:
- **`EXPERIMENT_RUNBOOK.md:351` is stale.** Line 351 is now the D-C10u-r3skipV2 row. D-C10r-rulings-10 is at `:353`, which also holds "one GPU run at a time" (commit 3316855 shifted the rows). See A2.
- **"byte-for-byte `arms:555–557`" (v2 §B, spec §2 step 5) is not byte-for-byte.** Line 555 is `self.budget.check()`, which calls `terminal_probe` (`arms:1397`). That does `Path.exists()`, `read_text()` and `json.loads()` of `run.json` on `/Volumes/memit` before **every** greedy forward. The benchmark's timed unit omits it, and it omits the concurrent 1 Hz fsync heartbeat thread (`arms:1408–1413`). The magnitude is likely < 1 % of a forward (I-INFER), so this is ADVISORY (A1), but the claim as written is false.

Verified as cited:
- `arms:87/93/109/112`, `:96–97`, `:104`, `:106–110`, `:1252–1265`, `:1392`, `:1397`, `:1408–1423`, `:1426`, `:1435–1451`, `:1463`, `:1480–1490`, `:1505–1507`, `:1513–1515`;
- `:339–345`, `:356–364`, `:433–449`, `:550–600`, `:709`, `:714`, `:762–763`, `:796`, `:811–857`;
- `c10e:25–26`, `:48`, `:51`, `:166–178` (CPU float32 `torch.linalg.svd(cov, full_matrices=False)`, so the spec's SVD matches), `:246–248`, `:358`, `:415–439`, `:458–491`;
- `read:14`, `:500`;
- selftest `:223–224`, `:633–639`, `:646`, `:650`, `:1020`, `:1286`;
- `logs_run.log:9`, `:15`, `:71`.

The §E edit list is complete. A grep for `5400|5399|5499|5500|5501` over the three code files hits exactly `read:500`, `arms:88`, selftest `:223`, `:224`, `:633`, `:636`, `:637`, `:639` and `:1020`.

## Check (3): arithmetic (all recomputed; all correct)

- **A7 targets.** ΣT = 132 over 24 facts with T ∈ {4, 5, 6} forces (#6s) = (#4s) + 12, so S = Σ T(T−1)/2 = 300 + (#4s) ∈ [300, 306].
- **p7.** p7 = 37·S + 84 = 11,184–11,406. Prefix items cost T − d forwards (`arms:554`), subject-free items the same, and F0 (36) plus relations (48) cost one forward each (`arms:594`).
- **Per-arm counts.** p2 = 972, p1 = 84, e7 = 10·132 + 72 = 1,392.
- **V and step 4.** V_P2 = 12,462 + 552 + 2,784 = 15,798. V₂ = 972 + 22,812 + 4,176 = 27,960. 26,680 ≈ 2·12,462 + 1,392 + 156 (Z0) + axes and observes.
- **Table rows.** Pre-round C01 sums: 7,153.9 / 7,687.6 / 8,263.0 / 8,687.8 / 9,409.9 / 10,769.2 → 7,200 / 7,800 / 8,400 / 8,700 / 9,600 / 10,800. ✔
- **C2.** 8,574 → floor / 10,251.6 → floor / 11,929.2 → floor / 12,768 → 12,900 / 14,194 → 14,400 / 16,878 → 17,100. ✔
- **Worst cases.** 2·(C01 + C2) + 60 = 39,660 / 40,860 / 42,060 / 43,260 / 48,060 / 55,860 s (11.02 / 11.35 / 11.68 / 12.02 / 13.35 / 15.52 h). ✔
- **Thresholds.** The 7,200 threshold is t* ≤ 1,380/26,680 = 0.05172 (p95 ≤ 41.4 ms). STOP at t* > 6,360/42,478 = 0.1497. ✔
- **Fallback.** 9,409.9 needed at t = 0.117 (190 s spare). P2 admits t ≤ 5,160/42,478 = 0.1215. ✔
- **Closed-form worst case.** Process 1 ends ≤ S₁ + C01 + C2 + ε. Process 2 ends ≤ S₂ + C01 + C2 + ε < S₂ + C3. Counting C3 for process 2 is conservative by 60 s. ✔

## Check (4): the deadline fix

**Sound.** After the fix, `active` is never empty in either process: stage01 runs from the origin to `enter(2)`, and stage2 from entry to exit. `complete01` is the only scope removal (`arms:112`; its only driver caller is `:1259`). The watchdog therefore always has a deadline (`arms:1414–1416`).

**Minimal.** The fix touches one method and one line. The reader is unaffected:
- `read:500–524` checks ceilings, origins and recorded per-scope projections.
- The stage-1 projections (`:1253`, `:709`, `:714`) run with stage01 active, as today.
- The stage-2 projection (`:1265`) runs after stage01 is discarded, as today.

Existing tests still pass, for the reason v2 gives (idempotent discard).

**Not yet shown to fail on today's code.** See B1.

## Check (5): does the benchmark time the driver's forward?

- **Matches the driver:**
  - batch 1;
  - `use_cache=False` (config and kwarg);
  - `logits_to_keep=0` (full-sequence head, as `arms:556`, `:594`, `:865`);
  - sync by `int(argmax)`;
  - population built by the driver's own `probe_population` (test 1);
  - forward-weighted sampling (whole items in shuffled order, so long items contribute proportionally);
  - fp16 MPS, rev pin;
  - SVD op, dtype and device identical to `c10e:173`.
- **Differs, acknowledged:** the templates are length-representative, not identical (the engine resamples them per attempt), and observe hooks are not reproduced (×2 UNMEASURED).
- **Differs, not acknowledged:** the per-forward `run.json` read and the heartbeat thread (A1).
- **Spec defects:** see B2.

## Check (6): the operator question

The recommendation comes first, and the numbers match §C/§E: 2 h 40 min = 9,600 s, "at most 3" = 10,800 s, 11 to 13½ h = 11.0–13.35 h, 15½ h = 15.52 h. Two sentences are inaccurate, and one decision is mis-framed (B4).

---

## BLOCKING

### B1 — Regression test (iv) passes on today's code, and (i)–(iii) fail today only if they drive the real `Session.stage1`

**Evidence.**
- **Test (iv).** Today, process 2 calls `complete01()` (`arms:1259`) and then `enter(2)` at e < C01 (`:1264`). After entry, `deadline()` = min(S + C3, e + C2) = e + C2, because e + C2 < C01 + C2 < C3. So "for every entry time e < C01, `deadline()` equals the inner deadline" **holds on today's code**. Today's defect lives only in the window *between* `complete01` and `enter(2)`, where `deadline()` = S + C3 (process 2) or `None` (process 1). The test as worded does not sample that window.
- **Tests (i)–(iii).** These are mechanical Budget-level sequences. If a test calls `complete01()` before `enter(2)` (as selftest `:646`, `:650` and the resident `SessionStub.stage1` at selftest `:1286` all do), the fixed `enter(2)` check runs with stage01 already gone. The test then passes on both old and new code, or fails on both. The driver's `Session` is never constructed by the selftests (`arms:323`). So unless the tests call the real `Session.stage1` (`arms:1252–1261`) unbound on a stub, they cannot distinguish the fix.

**Replacement text for v2 §D "Regression tests" (replace the four bullets):**

> **Regression tests (each must fail on today's code; run them on today's code first and record the failure).** Each test drives the real `Session.stage1` (`arms:1252–1261`) unbound on a stub `self` with a fake-clock `Budget`. In the stub, `run_recipe`, `complete_recipe_readouts`, `write_checks` and `record` are no-ops, `out` is a temp dir, and `R.read_process` is patched to return a K1-survivor reading `{"scientific_verdict": True, "next_stage": 2, …}`. Each test then calls the real `Session.stage2` entry or `Budget.enter(2)`. No test calls `complete01()` itself.
> - (i) Process 1, C01 = 7,200: stage 1 returns at 7,190. With no `enter(2)`, set the clock to 7,201 → `budget.check()` raises HALTED-BUDGET. (Today `deadline()` is `None` after `:1259`, so it does not raise.)
> - (ii) Process 1, C01 = 7,200: stage 1 returns at 7,199; `enter(2)` at 7,201 → HALTED-BUDGET, and `"stage2" not in origins`. (Today entry succeeds.)
> - (iii) Process 1: sample `deadline()` at every clock step from the origin through stage-1 return, the idle wait and `enter(2)`. It is never `None`, it equals origin + C01 before entry, and it equals entry + C2 after. (Today it is `None` after stage-1 return.)
> - (iv) Process 2 with C3 = C01 + C2 + 60: sample `deadline()` after stage-1 return and before `enter(2)`, then after `enter(2)`. Before entry it equals origin + C01; after entry it equals entry + C2. It never equals origin + C3. (Today the pre-entry sample equals origin + C3.)
> - (v) Structural: `complete01` is referenced only inside `Budget.enter` (AST or grep check over `c10z_astra_arms.py`). Otherwise a future caller can reopen the gap that the proof's "only scope removal" premise closes.
>
> Selftest `SessionStub.stage1` (`selftest:1286`) drops its `self.budget.complete01()` call so that the resident-level tests model the fixed driver. Selftest `:646` and `:650` drop their explicit `b.complete01()` calls, so that `enter(2)` alone performs the transition.

### B2 — Benchmark spec: CAPPED vs FALLBACK contradiction, overlapping phase statuses, and a watchdog exit that discards a completed measurement

**Evidence (spec lines).**
- **CAPPED handling contradicts itself.** §3 `:116` accepts "status COMPLETE or CAPPED". Test 11 (`:56`) returns the FALLBACK for "status ≠ COMPLETE", so a valid CAPPED benchmark silently becomes 9,600 / 14,400 / 24,060.
- **Phase statuses overlap.** In §2 step 5 (`:70`), "COMPLETE when ≥ 200 timed; CAPPED … when stopped by the guard with ≥ 200" overlap: a guard stop with 300 timed is both.
- **A watchdog trip loses a completed measurement.**
  - The optional-phase gates use fixed needs: eval 240 s and SVD 200 s (`:72`, `:74`).
  - Both are UNMEASURED. The repo has no SVD timing anywhere: a grep of `CORPUS/`, `memory_mirror/` and `results/*.md` for SVD/compute_P seconds found only this spec.
  - If an optional phase overruns, the hard watchdog exits 3 (test 6). `derived` and the final status are written only at step 10 (`:75`).
  - Acceptance requires exit 0 (`:116`). So an SVD overrun after a complete probe measurement leaves no `derived` and fails acceptance, which wastes the GPU slot.

**Replacement text.** In spec §2 step 5, replace the "Status:" bullet with:

> - Status: COMPLETE iff n_timed ≥ 400; CAPPED iff the start guard stopped the loop with 200 ≤ n_timed < 400; INVALID iff n_timed < 200.

Replace spec §2 steps 7–10 and the line "Write the record after every phase (atomic replace)." with:

> 7. **weights_after** (mandatory, immediately after batch_forward): re-hash the 36 `down_proj`; a mismatch → top-level INVALID, exit 2.
> 8. After step 7 and after every later phase, recompute and write `derived = ceilings(record)` and the top-level `status` (atomic replace). Top-level status is INVALID if any of load, pin, probe_forward or weights_after is INVALID or failed; else CAPPED if probe_forward is CAPPED; else COMPLETE. Optional phases never change the top-level status.
> 9. **eval_A7** (optional; gate need 240), then re-hash the 36 `down_proj` as in step 7.
> 10. **svd** (optional; gate need 200; CPU only). Run it in a child process (`multiprocessing` spawn, or `subprocess` of the same script with `--svd-only`). Kill the child at elapsed 565 s and record `"status":"TIMEOUT","seconds_at_least":<elapsed in child>`. For `derived`, Q then uses `s × 5 × seconds_at_least + 300`, a lower bound that is labelled as such. Exit 0.
> A watchdog exit (code 3) can then occur only inside a mandatory phase.

In test 11, replace "A record with `status ≠ "COMPLETE"` returns the fallback" with:

> A record whose top-level status is INVALID, or whose probe_forward is not COMPLETE or CAPPED, returns the fallback `{"C01": 9600, "C2": 14400, "C3": 24060, "source": "FALLBACK"}`. COMPLETE and CAPPED both return `"source": "BENCHMARK"`.

Add to test 6:

> With the record as written after step 8, a watchdog trip during eval_A7 or svd is impossible (svd runs in a killable child), and a trip during a mandatory phase leaves `derived` absent and top-level status not COMPLETE/CAPPED.

Add to §3:

> `derived` must be present.

### B3 — The prereg amendment cites "the stated formula" but never states it, has no fallback branch, and makes the row-6 sentence unconditional

**Evidence.**
- v2 §E `:138` reads "C01 from [benchmark record path + SHA-256] by the stated formula". The amendment text contains no formula, no constants and no fallback path.
- A frozen prereg that points to a formula defined only in a draft under `results/` is not pre-registered.
- Astra-3 also required the basis to say that the ceiling is a prospective cap, not a completion estimate (`astra.md:26`).
- "Row 6's '≈ 1–2 h' is not met" is false when the benchmark returns C01 = 7,200 (t* ≤ 0.0517).

**Replacement text (v2 §E, the amendment block):**

> "## 9. Amendment B-1 (pre-observation, D-C10z-budget)
>
> Written before any ASTRA process has started; `results/c10z_astra/` is absent.
>
> (a) **Ceiling.** Every statement of the 5,400-second stage 0–1 ceiling (`:18`, `:125`, `:127`, `:133`, `:196` three times, `:344`) reads C01 seconds. C01 is a prospective resource cap, not a measured completion estimate; HALTED-BUDGET remains possible.
>
> (b) **Basis.** C01 = 300·⌈(I_pin + 2,040 + 26,680·t* + O + 1,800 + max(1,380, 15,798·t*) + Q)/300⌉, where:
> - t* = 1.25 × max(p95 s per probe-shaped forward, eval_A7 s / 1,392);
> - I_pin = max(120, 1.25 × (load + pin s));
> - O = 1.25 × 20 × p95 of the A7 identity-batch forward;
> - Q = max(480, 1.25 × 5 × SVD s + 300).
>
> All inputs come from benchmark record [path], SHA-256 [sha], computed by `ceilings()` in `experiments/track_c/c10z_astra_benchmark.py` at SHA-256 [sha]. 26,680 and 15,798 are the stage-0 step-4 and P2-validation forward counts (`results/c10z_astra_budget_advisor.md:40–41`). If C01 > 10,800, the attempt is not launched.
>
> (c) **Fallback.** If no benchmark record is accepted, C01 = 9,600.
>
> (d) **Launch inputs.** These are not prereg values and are recorded here for audit. C2 = max(12,600, 300·⌈(3,780 + 3·max(1,380, 27,960·t*) + 600)/300⌉), or 14,400 on the fallback. C3 = C01 + C2 + 60.
>
> (e) **Deadline scope.** The stage 0–1 deadline remains in force until stage 2 is entered. A K1 survivor whose stage-1 → stage-2 hand-off crosses C01 ends HALTED-BUDGET.
>
> (f) **Row 6.** If C01 > 7,200, row 6's '≈ 1–2 h' is not met by this ceiling; the operator accepted the larger bound under D-C10z-budget.
>
> Nothing else changes: no gate, label, K1/K2 rule, projection, probe, round cap (V13) or never-zero rule. Ceilings never increase during an attempt."

### B4 — Operator question: one inaccurate claim, and decision 1 mis-framed as conditional and as the operator's "recommendation"

**Evidence.**
- **The idle claim is wrong.** "a small fix so the program can no longer sit idle holding the GPU between phases" overstates the fix. After it, the resident can still sit idle between phase 1 and phase 2 until the first-phase limit expires (`arms:1414–1416` with stage01 active). Only the *unbounded* idle is removed.
- **Decision 1 is mis-framed.**
  - The prereg's decision 1 is a pre-run ruling on the method class ("recommend WRITE-QUALIFIES for this fixed-input, bounded analytic solve … not a route verdict … A 'measurement' ruling changes no gate or label", prereg `:343`).
  - v2's "If ASTRA works, we would recommend…" makes it conditional on a result.
  - "*Recommend 'write-qualifies'?*" asks the operator to recommend rather than to rule.
  - "write-qualifies" and "plan decision 1/2" are jargon.

**Replacement text (v2 §F).** In question 2, replace "This includes a small fix so the program can no longer sit idle holding the GPU between phases." with:

> "This includes a small fix: today, after the first phase passes, the program can sit idle holding the GPU for as long as no one starts the second phase. With the fix, that idle time counts against the first phase's limit. One side effect: if the second phase starts after that limit, the attempt stops as out of time."

Replace question 3 with:

> **3. Does ASTRA's method count as a way of writing facts?** Before the run, the plan asks you to rule whether ASTRA's fixed, bounded calculation counts as a legitimate way to write facts into the model, or only as a measurement. Your answer changes no test and no result label. It only decides how a positive result is described afterwards. It would not settle speed in real use, exact repeatability, storage fit or compliance with the designated engine, which all stay open. I recommend that it counts. *Does it count as a way of writing facts?*

In "Recording", add:

> "Questions 1–2 approve bounds, not yet-unknown numbers: C01 ≤ 10,800 s, worst case ≤ 15.5 GPU-h, or the fallback 9,600 / 14,400 / 24,060. The D-C10z-budget row first quotes the yes, then appends the benchmark path, its SHA-256 and the computed C01/C2/C3 before the go record is written. A STOP returns to the operator."

---

## ADVISORY

1. **The per-forward overhead is not reproduced** (Check 2). Add it inside the timed interval:
   - before each forward, a `Path.exists()` plus `json.loads(read_text())` of a ~2 KB `run.json`-shaped file in the benchmark's out directory (same volume);
   - during probe_forward, a daemon thread writing and fsyncing a heartbeat file once a second.

   Or reword v2 §B and spec §2 step 5 to: "the forward of `arms:556–557`; the per-forward `run.json` read (`arms:555`, `:1397`) and the heartbeat thread (`arms:1408–1413`) are not reproduced and are covered by s".
2. **Cite runbook rows by Decision-ID, not line.** `EXPERIMENT_RUNBOOK.md:351` (v2 `:15`, `:32`) now points to D-C10u-r3skipV2. D-C10r-rulings-10 is at `:353`.
3. **Make the proof's strict inequality exact.** v2's ordering (check, then discard, then `origins["stage2"] = clock()`) takes two clock reads, so the entry origin can sit a few microseconds past S₁ + C01. Order it as below. The check then sees both scopes at a clock ≥ the entry origin, so tₑ < S₁ + C01 holds exactly.

   ```python
   if key not in self.origins:self.origins[key]=self.clock()
   self.active.add(key);self.check()
   if key=="stage2":self.complete01()
   ```

   An expired stage 0–1 still refuses. The `origins["stage2"]` written before the refusal is harmless, because the halt diagnostic records it and nothing resumes.
4. **Out-path refusal has a prefix trap.** `results/c10z_astra_benchmark/…` shares the string prefix `results/c10z_astra`. Implement the refusal as `Path(out).resolve().is_relative_to((ROOT/"results/c10z_astra").resolve())`, and add a test that accepts `results/c10z_astra_benchmark/<UTC>` and refuses `results/c10z_astra/x`.
5. **batch_forward should match the driver exactly.** Pass `logits_to_keep=0` explicitly, as `arms:484–485` does; the Qwen2 default is the same but this keeps it exact. Build A7 `target_ids` via unbound `Session.make_batch` (`arms:433–446`), not a re-implementation.
6. **Minima for skipped phases are the optimistic direction.** O = 0 and Q = 480 when a phase is skipped. Record `"minima_used": [...]` in `derived`, and have the D-C10z-budget row say so. Define `worst_case_s = C01 + C2 + C3` in the spec, since it is currently unstated.
7. **C2's +600 is mislabelled.** "Recomputation of the entry projection" is not a cost. The real unallowanced stage-2 work is two recipe preambles: Z for A1/A2, and Z-band. Either way they are covered, because 3·V reserves about 83,900 forwards at entry, while stage 2's actual validation is about e1 + p1 + e2 + p2 + e7 + p7 ≈ 14,500. C2 is forced by the code's projection, not by the work. Say so, so that nobody reads C2 as an expected cost.
8. **The fallback carries no safety factor.** t = 0.117 is itself an upper bound: 174 s included a second edit (`logs_run.log:71`). State this.
9. **Require an absolute `C10Z_OUT_DIR` in the wrapper.** For example, `case "$OUT" in /*) ;; *) echo "C10Z_OUT_DIR must be absolute"; exit 2;; esac`. Otherwise its `run.json` read and the launcher's `$W/$OUT_DIR` normalisation (`run_c10z_stage.sh:10`) can disagree.

## Overturning test (protocol item 4)

- **For the fix:** the B1 tests run on today's code. Each must fail. If any passes, the fix is not what the proof claims.
- **For the ceilings:** the benchmark itself, at ≤ 10 GPU-minutes. If 1.25 × p95 > 0.1497 s/forward, the stage-0–1 plan cannot stay under 3 h, and the operator question changes.

## Drift check

This is on-path. ASTRA is the operator-authorized C10 falsifier (D-C10r-rulings-10 (2), `EXPERIMENT_RUNBOOK.md:353`). The budget and fix determine whether the attempt can yield a verdict rather than HALTED-BUDGET. No gate, label or K1/K2 rule changes. It does not by itself advance F1 readiness beyond enabling that falsifier.
