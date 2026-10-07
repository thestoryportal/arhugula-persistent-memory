# C10Z ASTRA MPS forward benchmark: test-first build brief for Codex (D-C10z-budget)

Spec source: `results/c10z_astra_budget_proposal_v2.md` §B (what to time) and §C (formula). If this brief and that file disagree, stop and report; do not choose between them.
Abbreviations: `arms` = `experiments/track_c/c10z_astra_arms.py`, `c10e` = `experiments/track_c/c10e_bandknob.py`.

## 0. Goal and hard limits

Build a ≤ 10-minute MPS micro-benchmark that measures the wall time of one probe-shaped forward, plus four secondary timings. It writes one JSON record, and a pure function maps that record to the three ASTRA ceilings.

**MUST NOT**:
- edit or write `memit_dry_run/**`, `c10e_bandknob.py`, `c10z_astra_arms.py`, `c10z_astra_read.py`, `c10z_astra_selftest.py`, `docs/C10Z_ASTRA_PREREG.md`, `configs/**`, `tools/run_c10z_stage.sh`, any tracker, or anything under `results/c10z_astra/`;
- call `my_edit`, `run_recipe`, `run_law5`, `apply_memit_to_model`, `compute_z`, `compute_P` or `get_cov`;
- write to any model parameter.

Importing `c10e_bandknob` (loads the model) and `c10z_astra_arms` (model-free, `arms:3`) is allowed, and so is reusing their helpers.

New files only:
- `experiments/track_c/c10z_astra_benchmark.py` (benchmark plus pure core)
- `experiments/track_c/c10z_astra_benchmark_selftest.py` (CPU-only `unittest`; never imports `c10e_bandknob` or touches MPS)

## 1. Tests first (write these, see them fail, then implement)

Every test runs on CPU with stubs: a fake tokenizer, a fake model whose "forward" advances an injected clock, a fake clock, and a fake `exit`. The whole suite runs in < 60 s. The final line prints `C10Z_BENCH_SELFTEST_PASS tests=<n>`.

1. **Population equals the driver's.** Build the A7 population with the benchmark's builder and with the driver's own `Session.probe_population` (`arms:560–582`), called unbound on a `SimpleNamespace(H=<fake H with tok, CANON, FICTION>, batches={arm: {"target_ids": …}}, templates=<6 templates>)`. Assert `R.json_digest` equality (the driver prints it, `arms:580`).
   - Counts: F0 = 36; prefix = 36·Σ(T−1); subject_free = Σ(T−1); relations = 48.
2. **Forward schedule.** For target lengths T, a prefix item at depth d costs T − d forwards (`arms:554`), so the full A7 set costs 37·S + 84 with S = Σ T(T−1)/2.
   - Check S = 300 for twelve 5s and twelve 6s → 11,184.
   - Check S = 306 for six 4s and eighteen 6s → 11,406.
3. **Statistics.**
   - p-quantile is linear interpolation at position (n−1)·q, the same rule as `arms:1295–1297`.
   - Test median/p90/p95/max/mean on [1..100], n = 1 and all-equal input.
   - NaN or inf input raises.
4. **Start guard boundaries** (cap = 600, reserve = 30): `may_start(569.999) is True`; `may_start(570.0) is False`. Optional-phase gate `phase_fits(elapsed, need)` is True iff elapsed + need ≤ 570:
   - `phase_fits(330.0, 240) is True`;
   - `phase_fits(330.001, 240) is False`.
5. **Timed loop stops at the guard.** With a fake forward costing 2.0 s per call, from elapsed 0, the loop times exactly the forwards that started at elapsed < 570 and then marks the phase CAPPED. The warm-up forwards (20) are excluded from `seconds`.
6. **Hard watchdog.** With a fake clock and a fake exit:
   - it calls exit(3) at elapsed ≥ 600.0 and does not call it at 599.999;
   - the record on disk afterwards keeps every phase completed before, and the in-flight phase shows `"status": "STARTED"`.
7. **Record round-trip.**
   - `write_record` → `read_record` gives an equal dict.
   - The writer uses `json.dumps(sort_keys=True, allow_nan=False)`, a temp file, fsync and `os.replace`, like `arms:43–56`.
   - NaN raises before writing, and an interrupted write leaves the previous file intact.
   - A schema check rejects: missing keys, a wrong type, `status: "COMPLETE"` with `n_timed < 200`, and a `device` other than `"mps"` in GPU mode.
8. **Output path refusals.**
   - Any out path under `results/c10z_astra/` raises.
   - An out directory that already holds `benchmark.json` raises (create-once; a rerun gets a new UTC directory).
9. **No mutation.** With a stub H whose `my_edit`, `run_recipe` and `run_law5` raise if called, a full stub run completes. With a stub forward that changes a stub `down_proj` weight, the record ends `status: "INVALID"` with `weights_unchanged: false`.
10. **Env preflight.** Inherited `C10_PROJECTOR` (or any `arms:28–29` key) raises through `arms.entry_preflight`, and `LLMDB_DEVICE=cpu` raises in GPU mode.
11. **`ceilings(record)`: the §C formula, a pure function and the only place it lives.** Inputs: `t_star`, `I_pin`, `O`, `Q` as defined in v2 §C, with R(x) = 300·⌈x/300⌉.
    - With I_pin = 120, O = 0 and Q = 480, the v2 §C table rows reproduce exactly. For example, t* = 0.117 → (9,600, 14,400, 24,060) and t* = 0.050 → (7,200, 12,600, 19,860).
    - The C2 floor 12,600 holds. C3 = C01 + C2 + 60.
    - Exact multiples of 300 do not round up.
    - `stop` is True iff C01 > 10,800 (inject the pre-round sum: 10,800.0 → C01 10,800, stop False; 10,800.001 → C01 11,100, stop True).
    - A record with `status ≠ "COMPLETE"` returns the fallback `{"C01": 9600, "C2": 14400, "C3": 24060, "source": "FALLBACK"}`.
    - t* = 1.25 × max(p95_probe, eval_s/1392) uses the eval term only when the eval phase is COMPLETE.

## 2. Behaviour to implement

**Run order** (the origin `T0 = time.monotonic()` is the first statement, before any torch import):
1. Preflight: `entry_preflight(os.environ)`; `tools/engine_fingerprint.py` main() == 0 (as `arms:330–332`); out-path refusals. Set `LLMDB_ROOT`, `LLMDB_DEVICE=mps` and `HF_HOME=<root>/hf_cache` (`arms:339`). Start the hard watchdog thread.
2. **load**: `torch.manual_seed(0)`; `H = importlib.import_module("c10e_bandknob")`. Assert `str(H.DEV) == "mps"` and fp16 (`arms:344`). Set `H.model.config.use_cache = False` (`arms:345`). Abort INVALID if load exceeds 300 s.
3. **pin** (gate need 120): time the parameter hash and the safetensors hash exactly as `arms:356–364`, reusing `tensor_bytes` and `sha256_file`. Hash the 36 `down_proj` with `tensor_hash` (`arms:293`) into `weights_before`.
4. **population**: the 6 templates are the literal list from `results/c10q_stacked/logs_run.log:9`. Store it in the script with that citation, and assert it has 6 entries with entry 0 = `"{}"`. Build the A7 population (test 1), and record the counts, digest and min/max sequence length.
5. **probe_forward**:
   - 20 warm-up forwards, then timed forwards until ≥ 400, over whole items in `random.Random(0)` shuffled order.
   - Per forward, `t0 = perf_counter()`; then `torch.tensor([cur], device=H.DEV)` → `H.model(…, use_cache=False, logits_to_keep=0).logits` → `int(logits[0,-1].argmax())` (`arms:556–557`, `:594–595`); then `t1`.
   - Store the seconds and `len(cur)`.
   - Status: COMPLETE when ≥ 200 timed; CAPPED (still usable) when stopped by the guard with ≥ 200; INVALID otherwise.
6. **batch_forward** (gate need 60): the A7 identity batch padded as `arms:433–446`, with frames `[t.format(H.CANON) for t in templates]` (`arms:449`). Run 2 warm-up + 5 timed forwards of `H.model(input_ids, attention_mask, use_cache=False)` with `torch.mps.synchronize()` before and after each.
7. **eval_A7** (gate need 240): `H.eval_arm(H.ARMS["A7_coined_coined"])` once, with sync, timed.
8. **weights_after**: re-hash the 36 `down_proj`. If they differ from `weights_before`, the status is INVALID.
9. **svd** (gate need 200; CPU only): `torch.manual_seed(0)`, an 11,008 × 11,008 float32 matrix A = (X + Xᵀ)/2, timed `torch.linalg.svd(A, full_matrices=False)`.
10. Write `derived = ceilings(record)` and the final status, then exit 0. Exit 2 if INVALID.

Write the record after every phase (atomic replace).

**Record** (`results/c10z_astra_benchmark/<UTC>/benchmark.json`, plus `benchmark.log` holding stdout):

```json
{"schema":"c10z_astra_benchmark/v1","decision_id":"D-C10z-budget","status":"COMPLETE|CAPPED|INVALID",
 "started_at":"<ISO>","finished_at":"<ISO>","wall_cap_s":600,"reserve_s":30,
 "env":{"model_id":"Qwen/Qwen2.5-3B","model_rev":"3aab1f1954e9cc14eb9509a215f9e5ca08227a9b","device":"mps","dtype":"float16",
        "torch":"<ver>","transformers":"<ver>","engine_fingerprint_ok":true,"script_sha256":"<sha>"},
 "inputs":{"templates_source":"results/c10q_stacked/logs_run.log:9","templates":["{}","…"],"templates_sha256":"<sha>",
           "population_sha256":"<sha>","population_counts":{"F0":36,"prefix":0,"subject_free":0,"relations":48},"seq_len_range":[0,0]},
 "phases":{"load":{"status":"…","seconds":0.0},
           "pin":{"status":"…","param_hash_s":0.0,"safetensors_hash_s":0.0},
           "probe_forward":{"status":"…","warmup":20,"n_timed":0,"seconds":[],"seq_len":[],
                            "median":0.0,"p90":0.0,"p95":0.0,"max":0.0,"mean":0.0},
           "batch_forward":{"status":"…","shape":[144,0],"seconds":[],"p95":0.0},
           "eval_A7":{"status":"…","seconds":0.0,"forwards":1392},
           "svd":{"status":"…","n":11008,"seconds":0.0}},
 "weights_unchanged":true,
 "derived":{"safety_factor":1.25,"t_star":0.0,"I_pin":0.0,"O":0.0,"Q":0.0,"C01":0,"C2":0,"C3":0,
            "worst_case_s":0,"stop":false,"source":"BENCHMARK|FALLBACK"}}
```

Skipped phases have `"status":"SKIPPED-NO-TIME"`, and `derived` then uses that term's minimum: I_pin 120, O 0, Q 480.

**Flag, do not act:**
- If the probe p95 < 0.030 s (below the I-INFER bandwidth floor, advisor `:47`), set `"suspect": true`.
- If max > 5 × p95, set `"outliers": true`.

The program decides what to do with either flag; the script does not.

## 3. Acceptance

1. `.venv/bin/python -B experiments/track_c/c10z_astra_benchmark_selftest.py` → `C10Z_BENCH_SELFTEST_PASS`. It must not import `c10e_bandknob` or touch MPS; assert `"c10e_bandknob" not in sys.modules` at the end.
2. `git diff --stat` shows only the two new files.
3. Do not run the GPU step yourself. Report back the exact command for the program to run:

   `LLMDB_ROOT=<worktree> <worktree>/.venv/bin/python -B <worktree>/experiments/track_c/c10z_astra_benchmark.py --out <worktree>/results/c10z_astra_benchmark/<UTC>`

   The program runs it once, with the GPU idle and no other MPS job. It needs exit 0, `status` COMPLETE or CAPPED, `weights_unchanged` true, and wall ≤ 600 s. It then reads `derived` and applies v2 §C.

**Bad output, rejected on review:**
- re-implementing the population instead of matching the driver (test 1);
- timing `model(...)` without the `int(argmax)` sync;
- reporting a mean in place of p95;
- any default that silently replaces a failed phase's measurement;
- any write outside the out directory.
