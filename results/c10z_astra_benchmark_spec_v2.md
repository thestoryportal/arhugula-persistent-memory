# C10Z ASTRA MPS forward benchmark: test-first build brief for Codex, v2 (D-C10z-budget)

Supersedes `results/c10z_astra_benchmark_spec.md` (left unchanged).
Spec source: `results/c10z_astra_budget_proposal_v3.md` §B (what to time) and §C (formula). If this brief and v3 disagree, stop and report; do not choose between them.
Folds: `results/c10z_astra_budget_v2_astra.md` items 1, 6, 7 and `results/c10z_astra_budget_v2_advisor.md` B2 and A1/A4/A5/A6.
Abbreviations: `arms` = `experiments/track_c/c10z_astra_arms.py`, `c10e` = `experiments/track_c/c10e_bandknob.py`.

## 0. Goal and hard limits

Build a ≤ 600-second MPS micro-benchmark under an independent supervisor process. It measures the wall time of one probe-shaped greedy iteration, plus optional secondary timings. It writes one JSON record, and a pure `ceilings()` maps that record to the ASTRA ceilings.

**MUST NOT:**
- edit or write `memit_dry_run/**`, `c10e_bandknob.py`, `c10z_astra_arms.py`, `c10z_astra_read.py`, `c10z_astra_selftest.py`, `docs/C10Z_ASTRA_PREREG.md`, `configs/**`, `tools/run_c10z_stage.sh`, any tracker, or anything under `results/c10z_astra/`;
- call `my_edit`, `run_recipe`, `run_law5`, `apply_memit_to_model`, `compute_z`, `compute_P` or `get_cov`;
- write to any model parameter.

**Allowed:** importing `c10e_bandknob` (it loads the model) and `c10z_astra_arms` (model-free, `arms:3`), and reusing their helpers, including unbound `Session.probe_population` and `Session.make_batch`.

**New files only:**
- `experiments/track_c/c10z_astra_benchmark.py`: supervisor, worker and pure core.
- `experiments/track_c/c10z_astra_benchmark_selftest.py`: CPU-only `unittest`. It may import CPU torch, but must never import `c10e_bandknob` or touch MPS.

## 1. Tests first (write, see fail, implement)

Stubs: a fake tokenizer, a fake model, an injected clock and a fake exit, except where a test needs a real process. The suite must take < 90 s and print `C10Z_BENCH_SELFTEST_PASS tests=<n>` last.

1. **Population equals the driver's.**
   - The benchmark builds the A7 population by calling unbound `Session.probe_population` (`arms:560–582`) on a `SimpleNamespace(H=<fake H: tok, CANON, FICTION>, batches={arm: {"target_ids": …}}, templates=<6>)`. The `batches` come from unbound `Session.make_batch` (`arms:433–446`).
   - Assert that the benchmark's population digest equals `R.json_digest` of the driver call.
   - Counts: F0 36; prefix 36·Σ(T−1); subject_free Σ(T−1); relations 48.
2. **Greedy loop and forward schedule.**
   - (a) A prefix item at depth d costs T − d forwards. The full A7 set costs 37·S + 84: S = 300 for twelve 5s and twelve 6s → 11,184; S = 306 for six 4s and eighteen 6s → 11,406.
   - (b) The stub forward asserts `torch.is_grad_enabled() is False`, for every probe, batch and eval forward.
   - (c) The loop appends the model's own argmax each step (`cur.append(token)`, `arms:557`). A stub model that returns token k at step k yields a `cur` equal to `prompt + [k0, k1, …]`, not the target.
   - (d) Inside every timed interval, the per-forward `run.json`-shaped read happens exactly once (`Path.exists` and `json.loads(read_text())`), and the 1 Hz heartbeat thread is alive.
3. **Statistics.**
   - The q-quantile uses linear interpolation at (n−1)·q, as `arms:1295–1297`.
   - Median, p90, p95, max and mean on [1..100], on n = 1, on all-equal data, and on Astra's case of 99 ones plus 10,000: p95 = 1 and mean = 100.99.
   - `t_star` uses the max of p95, mean and eval/1,392.
   - NaN or inf input raises.
4. **Worker start guard** (worker soft cap 590 s; reserve = max(30, 3 × measured before-hash s + 10)):
   - With a reserve of 30: `may_start(559.999) is True` and `may_start(560.0) is False`.
   - `phase_fits(elapsed, need)` is True iff elapsed + need ≤ 590 − reserve. Test both sides at exact equality, and at +0.001.
5. **Timed loop stops at the guard.** Each fake forward costs 2.0 s. The loop times only forwards that started while `may_start` held, finishing the current item, and then stops. The 20 warm-up forwards are excluded. Status follows §2 exactly (test all three bands, at n = 199, 200, 399 and 400).
6. **Supervisor hard kill: a real process.**
   - Run with cap = 1.5 s and a worker stand-in that sleeps forever in its own process group. The supervisor sends SIGKILL to the group at ≥ 1.5 s.
   - The child is confirmed dead within cap + 1.0 s.
   - The record on disk gets top-level `"status": "INTERRUPTED"`. Phases completed before the kill keep their statuses, and the in-flight phase reads `"STARTED"`.
   - `ceilings()` on that record returns REFUSED.
   - A second case: a worker that exits 0 before the cap is not killed, and its record is untouched.
7. **SVD child timeout.** A stand-in SVD child that sleeps forever is killed when worker elapsed reaches 565 s (fake clock). The phase is `"TIMEOUT"` with `seconds_at_least`, the top-level status is unchanged, and the worker exits 0.
8. **Record round-trip and schema.**
   - The write uses `sort_keys=True` and `allow_nan=False`, through a temp file, fsync and `os.replace` (as `arms:43–56`). Reading the record back returns an equal dict.
   - NaN raises before writing, and an interrupted write leaves the previous file intact.
   - The schema rejects: missing keys; wrong types; probe `"COMPLETE"` with n < 400; `"CAPPED"` outside 200–399; device ≠ `"mps"` in GPU mode; and a COMPLETE or CAPPED top level without both `weights_before` and `weights_after`.
9. **Out-path refusals.**
   - Use `Path(out).resolve().is_relative_to((ROOT/"results/c10z_astra").resolve())`.
   - `results/c10z_astra/x` is refused, and `results/c10z_astra_benchmark/<UTC>` is accepted (the prefix trap).
   - A directory that already holds `benchmark.json` is refused.
10. **No mutation.**
    - With a stub H whose `my_edit`, `run_recipe`, `run_law5` and `apply_memit_to_model` raise if called, a full stub run completes.
    - A stub forward that changes a `down_proj` weight makes the top level `INVALID` with `weights_unchanged: false`, and `ceilings()` returns REFUSED.
11. **Env preflight.** Any `arms:28–29` key raises through `arms.entry_preflight`, and `LLMDB_DEVICE=cpu` in GPU mode raises.
12. **`ceilings(record)`: the v3 §C formula, which lives only here.**
    - With I_pin = 120, O = 0 and Q = 480, it reproduces the v3 §C table exactly:
      - t* = 0.030 → (7,200 floor, 12,600, 19,860);
      - 0.050 → (7,200, 12,600, 19,860);
      - 0.117 → (9,600, 14,400, 24,060);
      - 0.14625 → (10,800, 16,800, 27,660);
      - 0.149 → (10,800, 17,100, 27,960).
    - The C2 floor holds; C3 = C01 + C2 + 60.
    - `worst_case_s` = `nominal_supremum_s` = 2·(C01 + C2), with `c3_sum_s` = C01 + C2 + C3 recorded beside it.
    - Exact multiples of 300 stay; injected pre-round sums of 10,800.0 → C01 10,800 with `stop` False, and 10,800.001 → C01 11,100 with `stop` True.
    - COMPLETE and CAPPED records give `"source":"BENCHMARK"`. INVALID, INTERRUPTED, a missing mandatory phase, or a missing hash gives `{"source":"REFUSED","reason":…}` with no numbers. **Never the fallback.**
    - The fallback is a separate constant, `FALLBACK = {"C01":9600,"C2":14400,"C3":24060,"source":"FALLBACK-OPERATOR-CHOSEN","discretionary":True}`. `ceilings()` never returns it.
    - Skipped or TIMEOUT optional phases put their term into `derived.minima_used`, e.g. `["O"]`, or `["Q:lower-bound"]` for a TIMEOUT SVD.
    - The eval term enters t* only when eval_A7 is COMPLETE.

## 2. Behaviour

**Processes.**
- **Supervisor (no torch import).** `T0 = time.monotonic()` is its first statement. It spawns the worker (`--worker --t0 <T0>`, `start_new_session=True`) before any preflight, polls every 0.25 s, and at T0 + 600 s sends SIGKILL to the worker's process group. It then marks the record INTERRUPTED (it is the only writer, because the worker is dead) and exits 3. Otherwise it exits with the worker's code.
- **Cross-process clock.** The worker computes elapsed from the supervisor's T0. Add a CPU test that a spawned child's `time.monotonic()` is ≥ the parent's T0 and within 5 s of it, i.e. that the clock is system-wide.

**Worker, in order. Write the record (atomic replace) after every phase. From step 7 on, also recompute the top-level status first and then `derived`.**
1. **preflight** (mandatory):
   - `entry_preflight(os.environ)`;
   - `tools/engine_fingerprint.py` main() == 0 (as `arms:330–332`);
   - the out-path refusals;
   - set `LLMDB_ROOT`, `LLMDB_DEVICE=mps` and `HF_HOME` (`arms:339`).
2. **load** (mandatory):
   - `torch.manual_seed(0)`; import `c10e_bandknob`;
   - assert MPS and fp16 (`arms:344`); `use_cache=False` (`arms:345`);
   - INVALID if load exceeds 300 s.
3. **pin** (mandatory):
   - time the parameter hash and the safetensors hash as in `arms:356–364`;
   - take `weights_before`, the 36 `down_proj` via `tensor_hash` (`arms:293`), and time it as `before_hash_s`;
   - set reserve = max(30, 3 × before_hash_s + 10).
4. **population** (mandatory): build it per test 1 from the six literal templates of `results/c10q_stacked/logs_run.log:9` (assert there are 6 and entry 0 is `"{}"`). Record the counts, the digest and the seq-length range.
5. **probe_forward** (mandatory):
   - Start the 1 Hz fsync heartbeat thread.
   - Write a ~2 KB `run.json`-shaped file in the out dir.
   - Run whole items in `random.Random(0)` shuffled order: 20 warm-up forwards, then timed forwards until ≥ 400 or until `may_start` fails.
   - Each timed interval: `t0 = perf_counter()`; `Path.exists()` + `json.loads(read_text())` of that file; under `torch.no_grad()`: `torch.tensor([cur], device=H.DEV)` → `H.model(…, use_cache=False, logits_to_keep=0).logits` → `token = int(logits[0,-1].argmax())`; `cur.append(token)`; `t1`. Single-forward items use `arms:594–595` under `no_grad`.
   - Store the seconds and `len(cur)` at each forward.
   - **Status:** COMPLETE iff n_timed ≥ 400; CAPPED iff the start guard stopped the loop with 200 ≤ n_timed < 400; INVALID iff n_timed < 200.
6. **weights_after_probe** (mandatory, reserved): re-hash the 36 `down_proj`. A mismatch makes the top level INVALID → exit 2.
7. **Status and derived.** The top level is INVALID if any of preflight, load, pin, population, probe_forward or a weights check is INVALID or failed; otherwise CAPPED if probe_forward is CAPPED; otherwise COMPLETE. Optional phases never change the top-level status. Then write `derived = ceilings(record)`.
8. **batch_forward** (optional):
   - Build the A7 identity batch by unbound `Session.make_batch` with frames `[t.format(H.CANON) for t in templates]` (`arms:449`).
   - Under `torch.no_grad()`: `H.model(input_ids, attention_mask=…, use_cache=False, logits_to_keep=0)`, with `torch.mps.synchronize()` before and after.
   - Time one forward first. Continue to 1 warm-up + 5 timed only if `phase_fits(elapsed, 2 × 6 × first)`.
   - Then re-hash as in step 6.
   - Skipped → `"SKIPPED-NO-TIME"`.
9. **eval_A7** (optional; need = 2 × 1,392 × max(p95, mean) from step 5): `H.eval_arm(H.ARMS["A7_coined_coined"])` once, synchronized and timed, then re-hash.
10. **svd** (optional; CPU only):
    - Run in a spawned child: `torch.manual_seed(0)`; A = (X + Xᵀ)/2 with X an 11,008 × 11,008 float32 matrix; time `torch.linalg.svd(A, full_matrices=False)` (matches `c10e:173`).
    - The worker kills the child at worker elapsed 565 s and records `"TIMEOUT","seconds_at_least"`.
11. Final status, then `derived`, then write; exit 0 (or 2 if INVALID).

**Flags (report only; the program decides).** `"suspect": true` if probe p95 < 0.030 s. `"outliers": true` if max > 5 × p95. Optional-phase statuses ∈ {COMPLETE, SKIPPED-NO-TIME, TIMEOUT (svd only)}.

**Record** (`results/c10z_astra_benchmark/<UTC>/benchmark.json` plus `benchmark.log`):

```json
{"schema":"c10z_astra_benchmark/v2","decision_id":"D-C10z-budget",
 "status":"COMPLETE|CAPPED|INVALID|INTERRUPTED",
 "started_at":"<ISO>","finished_at":"<ISO>","wall_cap_s":600,"worker_soft_cap_s":590,"reserve_s":0.0,
 "env":{"model_id":"Qwen/Qwen2.5-3B","model_rev":"3aab1f1954e9cc14eb9509a215f9e5ca08227a9b","device":"mps","dtype":"float16",
        "torch":"<ver>","transformers":"<ver>","engine_fingerprint_ok":true,"script_sha256":"<sha>","supervisor_pid":0,"worker_pid":0},
 "inputs":{"templates_source":"results/c10q_stacked/logs_run.log:9","templates":["{}","…"],"templates_sha256":"<sha>",
           "population_sha256":"<sha>","population_counts":{"F0":36,"prefix":0,"subject_free":0,"relations":48},"seq_len_range":[0,0]},
 "phases":{"preflight":{"status":"…"},"load":{"status":"…","seconds":0.0},
           "pin":{"status":"…","param_hash_s":0.0,"safetensors_hash_s":0.0,"before_hash_s":0.0},
           "population":{"status":"…"},
           "probe_forward":{"status":"…","warmup":20,"n_timed":0,"seconds":[],"seq_len":[],
                            "median":0.0,"p90":0.0,"p95":0.0,"max":0.0,"mean":0.0,"includes_runjson_read":true,"heartbeat_thread":true},
           "batch_forward":{"status":"…","shape":[144,0],"seconds":[],"p95":0.0},
           "eval_A7":{"status":"…","seconds":0.0,"forwards":1392},
           "svd":{"status":"…","n":11008,"seconds":0.0,"seconds_at_least":null}},
 "weights_before":{"0":"<sha>","…":"…"},"weights_after":[{"after":"probe_forward","match":true}],
 "weights_unchanged":true,"suspect":false,"outliers":false,
 "derived":{"source":"BENCHMARK|REFUSED","reason":null,"safety_factor":1.25,"t_star":0.0,"I_pin":0.0,"O":0.0,"Q":0.0,
            "C01":0,"C2":0,"C3":0,"nominal_supremum_s":0,"worst_case_s":0,"c3_sum_s":0,"stop":false,"minima_used":[]}}
```

## 3. Acceptance

1. `.venv/bin/python -B experiments/track_c/c10z_astra_benchmark_selftest.py` prints `C10Z_BENCH_SELFTEST_PASS`, and `"c10e_bandknob" not in sys.modules` at the end.
2. `git diff --stat` shows only the two new files.
3. Do not run the GPU step yourself. Report this command for the program:
   `LLMDB_ROOT=<worktree> <worktree>/.venv/bin/python -B <worktree>/experiments/track_c/c10z_astra_benchmark.py --out <worktree>/results/c10z_astra_benchmark/<UTC>`
   The program runs it once, with the GPU idle. **Usable** means:
   - exit 0;
   - top level COMPLETE or CAPPED;
   - `weights_unchanged` true;
   - `derived` present with `source` BENCHMARK.

   REFUSED or INTERRUPTED is unusable. The program may rerun once in a new directory; after that, the question goes back to the operator. It never falls back silently.

**Bad output, rejected on review:**
- re-implementing the population or the batch instead of calling the driver's methods;
- any forward outside `torch.no_grad()`;
- appending target tokens instead of argmax tokens;
- timing without the `int(argmax)` sync or the run.json read;
- a mean-only or p95-only t*;
- `ceilings()` returning numbers for an INVALID or INTERRUPTED record;
- any write outside the out directory.
