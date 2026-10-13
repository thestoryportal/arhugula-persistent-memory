reviewer: Claude advisor subagent, model Opus 5.5 — effort: high — date: 2026-10-06 — scope: §7 A2 v2 + uncommitted diff of the prereg, c10s_sharedz_{arms,inertness,read,selftest}.py (no model loaded; selftest run: C10S_SELFTEST_PASS, 11 tests)

**Verdict: PROCEED**

No blocking items. A2 v2 replaces the tolerance draft with a stronger test: the unmodified engine builds the same batch, and the two results must agree at the (i) tolerance. That supersedes all three of my round-1 blockers. I checked the batch equivalence against `compute_z.py:14-73` and on the context templates actually recorded in the halt run. The twin in the driver pairs correctly and leaves nothing else changed. Three advisory items follow; the first is the most useful and costs about 20 s.

---

## 1. Round-1 blocking items

**B1, sum instead of mean: SUPERSEDED, resolved by parity.** The (iii) gate is now `dist(engine(rq, R.ctx_triplicate(ctx)), compute_z_shared([CANON]*3))["rel_l2"] <= tol` (`c10s_sharedz_inertness.py`, diff +188–193). A `.sum()` at `c10s_sharedz_arms.py:272` would change three things: the NLL weight against KL and weight decay, the loss compared with the 0.05 stop, and the Adam gradient direction. The engine on the same 18 rewriting rows keeps `.mean()` (`compute_z.py:150`). In this regime any arithmetic difference grows to the percent scale over 25 steps on the clamp sphere: the halt run turned a 0.0026 step-0 gap into a rel L2 of 0.122. A sum bug therefore fails a 1e-4 parity gate by orders of magnitude. The same reasoning covers (iv) on the 19-row frames batch, which is the production shape.

**B2, rounding flipping the stop step: SUPERSEDED.** No stop-reason or step-count gate remains. Both sides of the parity check run the same arithmetic on the same input tensor, so rounding cannot separate their stop steps. The only way they can diverge is nondeterminism at the 19-row shape (see item 3).

**B3, the twin's wording about context templates: RESOLVED.** The twin now runs inside `injection_cell` (`c10s_sharedz_arms.py`, diff +414, +423–430), on the driver's own `ctx` and in the screen's process. The A2 text now says "same process and same `ctx` as the screen". The reader's line says "this process's templates" (`c10s_sharedz_read.py`, diff +379–381), which is now true. My round-1 A3 is adopted as `ok = abs(gain) < SCREEN_GAIN_MIN`, regardless of spread (`noise_twin_verdict`). The selftest covers +6 CONCENTRATED as a veto, −6 as a veto, and +5 as admissible.

My other round-1 advisories: A4 (plan guards) is covered by `plan_matches` plus parity. A1 and A2 (grad mode against the edit hook; the positive control) no longer apply; I agree with "not adopted". A6(a) is fixed: A1's sentence is back verbatim, and A2 no longer ends with a stale hook line.

## 2. Q2 — Is the engine-built reference truly the same batch?

Yes. Evidence:
- **The prompt list.** `compute_z.py:46-50` builds `context.format(request["prompt"]) + tok.decode(target_ids[:-1])` over every context template, then `["{} is a"]`. That is the engine's only read of `request["prompt"]`; lines 14-45 read only `target_new`, and `find_fact_lookup_idx` gets the built prompt. So a `{**rq, "prompt": "{}"}` request is safe. For (iv), `c.format(f).format("{}")` gives back `c.format(f)`, and `compute_z_shared` builds `c.format(f)` (via `build_prompt_plan`). For (iii), each `c` repeated three times in place gives the template-major triplets `build_prompt_plan(ctx, [CANON]*3)` makes.
- **Checked on real data.** On the `ctx` recorded in `results/c10s_sharedz/inertness.json`, I compared three lists: `build_prompt_plan`, `R.engine_plan`, and a literal re-statement of `compute_z.py:46-50`. They are equal for both het and trip, 19 rows each. Every row has exactly one brace pair (`{}`), and no ctx entry has a stray brace. One template contains `$\sqrt`; a backslash is harmless to `str.format`. `memit_main.py:310` replaces `{`/`}` with spaces in the generated text before appending `. {}`, so a brace in a sampled template is ruled out at the source.
- **Padding and targets.** The two sides tokenize the same 19 strings with `padding=True`, so `input_ids` and `attention_mask` are identical. The targets come from the same `ex_len - len(target)` rule (`compute_z.py:60-65`, `arms.py:218-223`).
- **Lookup indices.** `find_fact_lookup_idx(prompt, subject, …)` (`compute_z.py:234-256`) runs on identical prompt strings, so the indices are identical.
- **target_init and the KL row.** Row 0 is `"{}"→CANON` on both sides, so `target_init = cur_out[0][0, lookup_idxs[0]]` reads the same activation. The KL row is the same `"{} is a"`, last on both sides.

## 3. Q3 — Is parity at the (i) tolerance safe from a false halt? Is any source of difference left?

No input-level difference is left: same strings, same tensors, same indices, same `target_init`, same KL row. The two code paths are already shown to be arithmetically identical at 7 rows, where (ii) gave rel L2 0.0 and max-abs 0.0. The remaining extra operations in `compute_z_shared` work on detached copies (`float(...)`, `.cpu()` lists) or print `.item()` on the engine side. Neither touches the graph.

The one residual risk is **run-to-run nondeterminism at the 19-row shape**. (i) measured the floor only at 7 rows (0.0). If an MPS kernel were nondeterministic at 19 rows, parity would fail by the same percent-scale amplification. That would be a correct HALT, but one the record could not attribute.

- **A1 (ADVISORY, recommended): measure the floor at the parity shape.** Solve `engine_solve(rq, R.ctx_triplicate(ctx))` twice in (iii) (`c10s_sharedz_inertness.py` (iii) block, diff +190) and record `floor_19 = dist(eng_trip_a, eng_trip_b)["rel_l2"]`. Gate (iii) and (iv) at `max(10 × max(floor_7, floor_19), 1e-4)`, or at least record `floor_19` so a parity HALT can be attributed from the JSON. Cost: one extra 19-row solve, about 20 s.

## 4. Q4 — The driver change

- **Pairing is correct.** `twin_hits` is built over `PTEST` in order, with `Inject(subject_idx(t, c), z_twin)` and `decode(t.format(c), len(tids)) == tids`. These are the same calls the canonical/shared loop uses (`arms.py:433-439`). `twin_rows[-1]["canon"]` is filled in the same loop iteration from `per_t[1:]`, which is `[CANON] + PTEST` minus CANON, i.e. PTEST order, key `canonical_full`. So each fact's twin hits sit beside that fact's canonical hits, template by template. `noise_twin_verdict` treats "shared" as the twin, so forward gain = twin − canonical, and the reverse screen is recorded.
- **Nothing else is disturbed.** `R.ctx_triplicate` builds new lists and does not mutate the `get_context_templates` cache object; `ctx` is stored unchanged in `inject.json`. The engine solve changes no weights (`set_requires_grad(False)`, already in force). It sits outside `CaptureTargetInit`, which wraps only `z_c`. `Inject` hooks are removed on exit. `run_pass` rebinds `H.compute_z` only later, and the twin calls `_engine_compute_z` directly. The solves are deterministic at a fixed shape (see A1), so their order does not matter. `INERTNESS_CHECKS` is back to the five checks, and the reader stops at any non-PROCEED outcome, NOISE-NON-DISCRIMINATING included (`read.py:382-384`). The driver prints the twin gain and stops the same way.
- **Cost.** One 19-row engine solve plus three greedy decodes per fact, × 24. The quoted +8 min is consistent with the 19-row solve time in the halt run.
- **A2 (ADVISORY): wording on "batch shape".** The twin matches the shared batch in row count (19). Padded length is likely equal but not guaranteed: CANON is the longest phrasing, so the longest row in both batches is probably the same CANON row. Write "the shared solve's row count (19) and, by construction, very likely its padded length". Optionally record `input_ids.shape` for both solves; the engine does not expose it, but the shared `diag` can.
- **A3 (ADVISORY): record twin vs shared too.** `twin_dist` records only `rel_l2_vs_canonical`. Also recording `rel_l2_vs_shared` per fact puts the rounding-only distance (twin vs canonical) beside the objective-change distance (shared vs canonical) for the cell-1 reading. Record only.

## 5. Q5 — New blocking issues

None. Also checked:
- The (iv) `target_prefix` used by `plan_matches` is derived exactly as in `compute_z_shared` (`tok.decode(target_ids[:-1])`).
- The halt diagnostic now carries `parts` and `parity_vs_engine`.
- The A2 text, the code and the selftest agree on the precedence UNDERFIT → NOISE-NON-DISCRIMINATING → screen.
- `SOURCE_FILES` still hashes every edited file, the driver and the prereg included. Run the inertness rerun in a new `OUT_DIR` only after the last edit to any of them, and write the log to a new filename.
- The engine `compute_z.py` is untouched by the diff.
