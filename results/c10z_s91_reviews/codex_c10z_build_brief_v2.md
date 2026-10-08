# Codex build brief v2: C10Z ASTRA benchmark + idle-time fix + C01 launch binding + telemetry + inertness check (test-first)

W = `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a`. Every path below is relative to W unless absolute.
- Run build and test commands with `W/.venv/bin/python -B`, with `TMPDIR=/private/tmp/c10z_build` (create it).
- Start only when §0's no-Python-during-a-GPU-run condition holds, and run one process at a time.
- Use absolute paths, and never `cd` in your own commands. The verbatim v3 §G wrapper contains `cd` inside a subshell; that is part of the deliverable, not a build command.

This brief supersedes the v1 brief. It implements prereg §9 as revised by **§9.1** (`docs/C10Z_ASTRA_PREREG.md`). The program appends §9.1 before you start.

## 0. Hard limits (violating any one fails the build)

- **Writes only to these paths:**
  - `experiments/track_c/c10z_astra_arms.py`, `experiments/track_c/c10z_astra_read.py` and `experiments/track_c/c10z_astra_selftest.py`;
  - new `experiments/track_c/c10z_astra_benchmark.py` and new `experiments/track_c/c10z_astra_benchmark_selftest.py`;
  - new `experiments/track_c/c10z_astra_telemetry_check.py`;
  - new `tools/run_c10z_attempt.sh`;
  - the report `results/c10z_build_codex_impl.md`;
  - scratch under `/private/tmp/c10z_build/`.

  Nothing else in W, and nothing outside W except that scratch directory.
- **FROZEN while C10W P2 runs (any edit HALTs P2).** These paths are hashed by the live run. Do not modify, move, touch, re-save or reformat them:
  - `configs/hparams/qwen25_3b_memit_hparams.json`, `configs/screens/g6_screen_qwen3b.json` and `configs/screens/g6_screen_qwen3b_v2.json`;
  - `docs/C10W_ORACLE_PREREG.md`;
  - `experiments/track_c/c10e_bandknob.py`, `experiments/track_c/c10p_twopass_arms.py`, `experiments/track_c/c10w_oracle_eval.py`, `experiments/track_c/c10w_oracle_read.py`, `experiments/track_c/c10w_oracle_step0.py` and `experiments/track_c/c10w_oracle_train.py`;
  - `memit_dry_run/memit/memit/memit_main.py` and `tools/engine_fingerprint.py`;
  - everything under `results/c10w_oracle/`.

  You may read these files, and tests may copy their bytes into a temp tree under `/private/tmp/c10z_build/`.
- **Also FROZEN until the C10V verdict is read:** `experiments/track_c/c10v_layerpick_*.py`, `docs/C10V_LAYERPICK_PREREG.md`, `tools/run_c10v_stage.sh` and everything under `results/c10v_layerpick/`.
- **Other read-only paths:**
  - `docs/C10Z_ASTRA_PREREG.md` (you only re-pin its SHA);
  - all of `memit_dry_run/**`, which stays UNMODIFIED;
  - `configs/**`, `tools/run_c10z_stage.sh`, `EXPERIMENT_RUNBOOK.md`, `CORPUS/**` and all trackers;
  - every other `c10u_*`, `c10v_*` and `c10w_*` file under `experiments/`, `docs/` and `results/`.
- **No GPU job and no model.** No Python process of any kind (the venv interpreter, `python3`, `uv`, or a test subprocess) may run while a C10W P2, a later C10W P3 or a C10V stage can be dispatched. Do not start until `COORDINATOR_EXIT=` appears in `results/c10w_oracle_logs/p2-coordinator.log` and the program confirms that no other GPU coordinator (such as a later C10W P3) and no C10V or other GPU stage is live or pending. A Python process at a stage boundary makes `tools/c10w_p2_gate.py` refuse that stage, and that stops P2 (`run_c10w_p2.sh` finish 6). The build stays model-free and GPU-free.
  - Never run the benchmark, the inertness check, any ASTRA stage, any wrapper against the real tree, or any c10v/c10w script.
  - Never import `c10e_bandknob`, `transformers` or `datasets`, never touch `torch.mps` or device `"mps"`, and never load a model.
  - Every test is CPU-only. Tests use stubs, temp trees under `/private/tmp/c10z_build/`, and real subprocesses only where a test says so.
- **No git writes:** no commit, stash, checkout, reset or add.
- **Evidence of scope.**
  - Before you start, save the following to `/private/tmp/c10z_build/before/`:
    - `git -C W status --porcelain`;
    - `shasum -a 256` of every write-list path that exists and every FROZEN source/input file (every FROZEN path except the `results/c10w_oracle/` and `results/c10v_layerpick/` trees);
    - a `find … -type f | sort` listing of `results/c10w_oracle/` and `results/c10v_layerpick/`.
  - At the end, repeat these and diff:
    - Only write-list paths may change.
    - Every FROZEN source/input file's SHA must be unchanged.
    - Report any listing change in the two frozen result directories separately, as an observed change. A listing alone cannot attribute it to a process, so do not attribute it. Do not touch those files.

## 1. Read before coding (LAW#4)

Read each item with line numbers (`cat -n`), and cite file:line in the report for every seam you change:
- `docs/C10Z_ASTRA_PREREG.md` §2.11, §2.12, §6, the whole of §9, and the whole of **§9.1**. §9 as revised by §9.1 is the spec for this build.
- `results/c10z_astra_budget_proposal_v3.md` §C, §D, §E, §F (go record) and §G.
- `results/c10z_astra_benchmark_spec_v2.md`, the whole file.
- All of `c10z_astra_arms.py`, `c10z_astra_read.py` and `c10z_astra_selftest.py`.
- `tools/run_c10z_stage.sh`.
- `.venv/lib/python3.11/site-packages/transformers/models/qwen2/modeling_qwen2.py:528–570`. This is the installed 4.51.0. `hidden_states[0]` is the embedding output, `hidden_states[l+1]` is the output of layer l for l ≤ 34, and the last entry is the final-norm output.

**Precedence.** §9.1 governs §9, and both govern v3, spec v2 and this brief. If this brief disagrees with §9.1, stop and report the disagreement. Otherwise, these exceptions are deliberate:
1. Spec v2 §0/§3.2 ("only the two new files", no edits to arms/read/selftest) applied to a benchmark-only build. Here they still bind the benchmark files: they never write parameters or call `my_edit`, `run_recipe`, `run_law5`, `apply_memit_to_model`, `compute_z`, `compute_P` or `get_cov`. The benchmark *may* call the read-only helpers spec v2 §0 allows: `entry_preflight`, unbound `Session.probe_population`, unbound `Session.make_batch` and `tensor_hash`. §0 above governs the build as a whole.
2. v3 §E's "`arms:88` `5400.` → C01" and "`read:500` `==5400.` → `==C01`" are replaced by §9.1 (a′), (b′) and (e′). Production driver and reader code must obtain the selected C01 from validated launch provenance; they must not hard-code the benchmark-selected value. Literal contractual bounds and numeric synthetic test fixtures, including C01_FIX and boundary cases, are permitted. Tests must not treat a fixture value as the selected live ceiling.
3. v3 §D tests (vi), (viii) and (ix) are replaced by §9.1 (f′).
4. Spec v2's record `env` gains §9.1 (b′1)'s fields, and `torch`/`transformers` come from `importlib.metadata.version`.
5. v3 §G's wrapper uses `-I` for its inline JSON check. Keep it verbatim. The engine fingerprint is run as `W/.venv/bin/python -B W/tools/engine_fingerprint.py`; it is read-only.

## 2. What to build (smallest code that meets §9 + §9.1; no speculative options)

### A. Idle-time fix (§9(e), §9.1 (f′); v3 §D)

Implement `Budget` exactly as v3 `results/c10z_astra_budget_proposal_v3.md:105–126`. The `enter` method is quoted verbatim here from v3 `:113–124`:

```python
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
```

The other changes:
- `Budget.__init__` adds `self.lock=threading.RLock()`.
- `deadline()` reads `active` under `with self.lock:`, as in v3 `:108–111`.
- `Session.stage1`'s tail (`arms:1259–1260`) becomes `if reading["next_stage"]!=2:self.budget.future_stage2_s=0.`.
- `complete01` (`arms:112`) is unchanged and is referenced only inside `Budget.enter`.

### B. C01 as a bound launch input (§9.1 (a′), (b′), (d′), (e′); D-C10z-c01input)

**Budget.** The signature becomes `Budget(start, stage01, stage2, stage3, process=1, clock=time.monotonic)`.
- `stage01` must be an `int` or `float`, not a `bool`, finite, with 7,200 ≤ stage01 ≤ 10,800. Otherwise raise HALTED-BUDGET `"invalid stage01 ceiling"`. `None` must also give that halt, not a `TypeError`.
- This replaces the literal `5400.` at `arms:88`.

**Seams for tests.** Evaluate all of these at call time from `D.ROOT` (module attribute `ROOT`, `arms:21`), never at import:
- the benchmark root `ROOT/"results/c10z_astra_benchmark"`;
- the script path `ROOT/"experiments/track_c/c10z_astra_benchmark.py"`;
- the inertness root `ROOT/"results/c10z_astra_telemetry_inertness"`;
- every (b′1) source path.

Existing tests already patch `ROOT` (`selftest:383`, `:1210`, `:1384`, `:1430`, `:1461`, `:1528`). Load the benchmark module lazily through one arms function, `benchmark_module()`, which imports it by path from `ROOT` at call time; the stage-0 and stage-3 functions obtain it only through that function, so that importing arms stays model-free and torch-free. Tests patch `D.benchmark_module`.

**go_record** (`arms:1342–1361`): additionally require
- `benchmark_sha256` and `benchmark_script_sha256`, each a 64-character lowercase hex string;
- `ceilings`, a dict with exactly the keys `stage01`, `stage2` and `stage3`, each a finite positive JSON number that is not a bool.

Otherwise raise HALTED-V12 `"go record requires benchmark_sha256, benchmark_script_sha256 and ceilings"`.

**stage_call(0)** (`arms:1464–1478`). Implement §9.1 (b′3) steps 1–11 in that order. All of them run after `arms:1467` and before `arms:1471` (`out.mkdir`). Every failure raises the code and the unique detail substring below, and writes nothing:

| step | check | code | detail substring |
|---|---|---|---|
| 2 | `C10Z_TELEMETRY` absent, or exactly `"1"` | V12 | `C10Z_TELEMETRY must be absent or 1` |
| 3 | env var present and non-empty | V12 | `C10Z_BENCHMARK_RECORD is required` |
| 3 | absolute | V12 | `C10Z_BENCHMARK_RECORD must be absolute` |
| 3 | `Path(p).resolve()` is `root/<one dir>/benchmark.json` (`is_relative_to`; `parent.parent == root.resolve()`) | V12 | `benchmark record outside results/c10z_astra_benchmark` |
| 3 | existing file; `OSError` on read | V12 | `benchmark record unreadable` |
| 4 | sha256(bytes) == go `benchmark_sha256` | V12 | `benchmark record differs from go selection` |
| 4 | strict JSON from those same bytes (`parse_constant` refuses NaN/±Infinity; `R.finite_json`) | V12 | `benchmark record is not strict JSON` |
| 5 | current script SHA == `env.script_sha256` == go `benchmark_script_sha256` | V12 | `benchmark script changed` |
| 5 | `B.source_identity(ROOT) == record["env"]["sources"]` | V12 | `benchmark source identity changed: <path>` |
| 5 | `B.environment_identity() ==` the record's python/machine/platform/torch/transformers | V12 | `benchmark environment changed: <key>` |
| 6 | `B.validate_record(record)`; it raises `ValueError`, and because `R.Halt` subclasses `ValueError` (`read:32`), convert only non-`R.Halt` errors | V12 | `benchmark record invalid: <reason>` |
| 7 | `c=B.ceilings(record)`; `c["source"]=="BENCHMARK"` | BUDGET | `benchmark refused: <reason>` |
| 7 | `c == record["derived"]` (JSON-normalised) | V12 | `benchmark derived disagrees with ceilings()` |
| 8 | `c["stop"] is False` | BUDGET | `benchmark STOP` |
| 8 | 7,200 ≤ C01 ≤ 10,800 | BUDGET | `C01 outside [7200, 10800]` |
| 8 | 2·(C01+C2) ≤ 55,800 | BUDGET | `nominal total above 55,800 s` |
| 9 | go `ceilings` == {stage01: C01, stage2: C2, stage3: C3} | V12 | `go ceilings differ from ceilings()` |
| 10 | `C10Z_STAGE2_CEILING_S`, when present, == C2 | BUDGET | `C10Z_STAGE2_CEILING_S differs from C2` |
| 10 | `C10Z_STAGE3_CEILING_S`, when present, == C3 | BUDGET | `C10Z_STAGE3_CEILING_S differs from C3` |
| 11 | telemetry on → inertness record valid (§2G) | V12 | `telemetry requires an INERT inertness record: <reason>` |

When the env vars are absent, keep today's meaning: that expansion is refused (`launch_duration`, `arms:1335–1339`).

The launch dict (`arms:1468–1470`) gains:
- `"stage01": float(C01)`;
- `"benchmark": {"path","sha256","script_sha256","sources","env","ceilings"}`;
- `"telemetry": bool`;
- `"telemetry_inertness": {"path","sha256"}` or `None`.

**resident** (`arms:1390–1393`):
- `Budget(start,launch["stage01"],launch["stage2"],launch["stage3"],process=process)`.
- The telemetry switch comes from `launch["telemetry"]` only.
- No re-hash in process 1 (§9.1 (d′)).

**stage_call(3)** (`arms:1480–1488`):
- After `arms:1486` and before `arms:1487` (`p2.mkdir()`), call `verify_launch_binding(run["launch"], os.environ)`. It runs §9.1 (d′)'s checks, using the same helper functions as stage 0. Every failure raises HALTED-V12 with `"launch binding changed since stage 0: <what>"`.
- Also check that the parsed `C10Z_TELEMETRY` equals `launch["telemetry"]`; otherwise raise HALTED-V12 `"C10Z_TELEMETRY differs from launch"`.
- Leave the existing order of `arms:1481–1484` unchanged.

**Reader** (§9.1 (e′)):
- `read:500`: `ceilings["stage01"]` is an `int`/`float`, not a `bool`, finite, with 7,200 ≤ x ≤ 10,800 (V12, detail `phase01 clock provenance`).
- After `read:519`: every projection `p` has `p["ceilings"]==record["budget"]["ceilings"]`, and every scope `k` has `ceiling_s==ceilings[k]` (V12, `projection ceilings differ from record ceilings`).
- In `read_directory` (`read:662–688`), for each closed, non-halted directory:
  - pass record `budget.ceilings[k]==run["launch"][k]` for stage01/stage2/stage3 (`pass ceilings differ from launch`);
  - `launch["stage01"]==launch["go"]["ceilings"]["stage01"]`, and each of `launch["stage2"]`/`launch["stage3"]` is `None` or equals the go value (`launch ceiling not the go selection`);
  - `launch["benchmark"]["sha256"]==launch["go"]["benchmark_sha256"]` (`launch benchmark differs from go`).
- In `read_run` (`read:649–656`): `p1["budget"]["ceilings"]==p2["budget"]["ceilings"]` (`process ceilings differ`).

### C. Benchmark: `c10z_astra_benchmark.py` and its selftest

Build exactly per `results/c10z_astra_benchmark_spec_v2.md`: supervisor, worker, statuses COMPLETE/CAPPED/INVALID/INTERRUPTED, and `ceilings()` returning BENCHMARK or REFUSED, never the fallback. Add these:
- The **top level imports only the standard library.** Import torch, arms and c10e inside the worker only. Otherwise, a by-path import from arms running as `__main__` would load a second copy of arms (advisor A6).
- Pure, stdlib-only, importable functions used by arms:
  - `source_identity(root)` → `{relpath: sha256}` over exactly the seven §9.1 (b′1) files, in that order;
  - `environment_identity()` → `{"python","machine","platform","torch","transformers"}`, using `platform.*` and `importlib.metadata.version`, never importing torch;
  - `validate_record(record)`: the spec v2 test-8 schema plus measurement consistency, raising `ValueError(reason)`;
  - `write_record(path, record)`: atomic, as spec v2 test 8;
  - `ceilings(record)`.
- The worker writes `env.sources` and these environment fields into the record.
- `ceilings()` computes p95, mean and t* from the raw `phases.probe_forward.seconds` (and the batch/eval/svd raw values), using the module's own quantile function, never from the recorded summaries.
- Measurement consistency, checked by `validate_record`:
  - `n_timed == len(seconds) == len(seq_len)`;
  - median/p90/p95/max/mean recomputed from `seconds` equal the recorded ones;
  - the probe status band agrees with `n_timed`;
  - `weights_before` has 36 entries, every `weights_after[*].match` is true, and `weights_unchanged` is true;
  - device is `"mps"`, dtype is `"float16"`, `model_rev` is pinned, and `engine_fingerprint_ok` is true.
- `population_and_batch(H, templates)`: the A7 population (unbound `Session.probe_population`) and the A7 identity batch (unbound `Session.make_batch`), as spec v2 test 1. It is shared with the inertness check (§2G).

### D. Telemetry (§9(h) as revised by §9.1 (h′)), inside `c10z_astra_arms.py`

- **Switch.** It is parsed at stage 0 and stage 3 (§2B) and recorded in `launch["telemetry"]`. The resident creates `Telemetry(out, process, attempt_id)` iff `launch["telemetry"] is True`, before `Session(...)` (`arms:1426`), and sets `session.telemetry` right after construction.
  - `Session` gets a class attribute `telemetry = None`, so `Session.__new__` stubs see `None`.
  - Every call site is `if self.telemetry is not None: self.telemetry.<method>(…)`. With telemetry off, no telemetry code runs past that check, and no `telemetry/` directory is created.
- **Clock.** Define a module-level alias `TELEMETRY_CLOCK = time.perf_counter`, bound at import, so tests that replace `D.time` cannot reach it. It is never the budget clock and never `time.monotonic`. UTC ISO times come from `datetime.datetime.now(datetime.timezone.utc)`.
- **Writer.**
  - At construction, create `<out>/telemetry/` and open `telemetry_p<process>.jsonl` in append mode, once.
  - The first line is a header with `kind:"header"`, the process, the attempt_id and `"telemetry": true`.
  - Every line holds `kind`, `t_utc`, `elapsed_s`, `cumulative_s`, `process` and `attempt_id`, plus its payload, serialised with `json.dumps(…, allow_nan=False, sort_keys=True, separators=(",",":"))` and a newline. After each line: `write`, `flush`, `os.fsync`.
  - `elapsed_s` is `TELEMETRY_CLOCK()` just before serialising, minus its value at method entry.
  - `cumulative_s` is the sum of every earlier line's full cost, from entry until after fsync.
- **Failure.** Every public method body is wrapped in `try … except Exception as exc`. On a failure, it prints exactly one `C10Z_TELEMETRY_DISABLED <ExcType>: <msg>` line to stdout and sets `enabled=False`, and every later call returns at once. It never propagates. Do not catch `BaseException`.
- **Lines and placement** (§9.1 (h′5)). Exactly these, and no others:

  | kind | where | payload |
  |---|---|---|
  | `phase` stage_start / stage_end | resident, around each `state.run(...)` (`arms:1428`, `:1430–1431`, `:1442`) | stage |
  | `phase` recipe_start / recipe_end | `run_recipe`: first statement; immediately before `return result` (`arms:640`, `:657`) | recipe, arms |
  | `phase` write_start | `write_arm`: the first statement, before `arms:706`; the arm is computed by the same expression as `arms:707` inside telemetry | mode, arm |
  | `phase` round_end | after `arms:740` (`if self.stage==1:round_guard(elapsed)`), before `arms:741` | round_no, arm, recipe (`self.active_recipe`), seconds (=`elapsed`), F (`len(indices)`), columns_written (`written`) |
  | `write_norms` | same place, after round_end | round_no, arm, `{str(l): {"patch_fro": ‖sol["patch"][l]‖_F, "cumulative_fro": ‖summed[l]‖_F}}` |
  | `target_probs` | same place, after write_norms, from that round's `post` (`arms:725`); plus one line right after `arms:743` from the final `post` with `round_no:"final"` | parallel arrays `rows, facts, views, qs, p` |
  | `logit_lens` | `stage0`: after `arms:813` (A7, `where:"pristine"`); `arm_hook`: after `arms:669` (`where:"post_write"`, the written arm) | layers, items `[{view, subject, prompt_ids, top:{str(l): [[id, text, prob]]×5}}]` |
  | `phase` halt | resident except path, immediately before `diagnostic(...)` at `arms:1457` (not from the watchdog thread) | code |

- **target_probs.** Use a module-level function `target_probabilities(gathered, targets, chunk_rows)`:
  - `chunk_rows = max(1, (64*2**20)//(4*V))`, where V = `gathered.shape[1]`;
  - for each row slice: `lse = torch.logsumexp(x, 1)`, then `p = exp(x[i, t_i] − lse)`, in float32 on CPU.
- **logit_lens.** Use one module-level function `logit_lens(model, items, layers, tok, device)`. Both Telemetry and the inertness check call it.
  - Under `torch.no_grad()` for the whole function, run `model(torch.tensor([ids],device=device), use_cache=False, output_hidden_states=True, logits_to_keep=1)` for each item.
  - For each `l` in `layers`: `h = out.hidden_states[l+1][:, -1, :]`, then `logits = model.lm_head(model.model.norm(h))`. Take top-5 of the float32 softmax: ids as int, text as `tok.decode([id])`, probabilities as float.
  - Raise if `max(layers) > model.config.num_hidden_layers - 2`.
  - Telemetry passes `self.H.model`, `self.population[arm]["F0"]`, `self.hp.layers`, `self.H.tok` and `self.H.DEV`.
- **Never:** write a parameter; register a hook; call `budget.clock`, `project` or `check`, `hooks_check`, `self.sync` or `time.monotonic`; write into run.json or any §2.12 record.

### E. Wrapper

`tools/run_c10z_attempt.sh`, verbatim from v3 §G, executable.

### F. Prereg pin and existing-test fixture edits

Change no assertion except where listed here. List every edit with file:line in the report.
- **Pin.** Set `read.py:14` `PREREG_SHA` and `selftest.py:19` `PREREG` to the SHA-256 of `docs/C10Z_ASTRA_PREREG.md` as it is when you start, with §9.1 already appended. Expected SHA-256: `87fe3d5d28c9a51eab4eadfd82cc7175f1a94f723f25f31658c5e1aeaf628b87`; if the file on disk differs, STOP and report 'PREREG SHA MISMATCH' before editing anything.
- **One fixture C01.** Add `C01_FIX = 7800.` to the selftest; it is in bounds and not at a bound.
  - `selftest:223`: `"stage01":5400` → `C01_FIX`.
  - `selftest:224`: `ceiling_s:5400.` → `C01_FIX`.
- **seal_schedule** (`selftest:266–274`) also sets each `budget.history[*]["ceilings"]` to a copy of the record's ceilings, and each scope's `ceiling_s` to the matching ceiling. A test that changes a ceiling after sealing re-seals:
  - `:1477–1478` already does;
  - add `seal_schedule(r)` after `:1662`.
- **Budget constructions** (new signature, with `C01_FIX` as `stage01`):
  - `:635–640`: `D.Budget(100.,C01_FIX,60.,6000.,…)`, with 5500/5499/5501 → `C01_FIX+100` / `+99` / `+101`;
  - `:642`;
  - `:644` and `:649`, also deleting `b.complete01();` at `:646` and `:650`;
  - `:881` (`_write_session` default);
  - `:1020`, with clock `5399.` → `C01_FIX-1`;
  - `:1699`.
- **Budget lambda patches:**
  - `:1299–1300` (`_mock_resident`) and `:1627` (Fix2 resident test) become `lambda start, stage01, stage2, stage3, process: real_budget(start, stage01, stage2, stage3, process=process, clock=…)`;
  - delete `self.budget.complete01()` at `:1286` (`SessionStub.stage1`).
- **Launch helper.** Add `_launch(**over)`, returning `{"attempt_id":"fixture-attempt","stage01":C01_FIX,"stage2":12000.,"stage3":24000.,"telemetry":False,"telemetry_inertness":None,"go":_go_record(),"go_sha256":"a"*64,"benchmark":{"path":"/x/results/c10z_astra_benchmark/T/benchmark.json","sha256":<go benchmark_sha256>,"script_sha256":<go script sha>,"sources":{},"env":{},"ceilings":<go ceilings>}}` updated by `over`. Use it at:
  - `:1147` (`_attempt_dir` default);
  - `:1237` and `:1249` (`_launch(stage2=None, stage3=None)`);
  - `:1451–1452`, `:1485–1486` and `:1624–1625` (keeping each test's own stage2/stage3/go values).
- **`_go_record()`** (`:1175–1178`) gains `benchmark_sha256="a"*64`, `benchmark_script_sha256="b"*64` and `ceilings={"stage01":C01_FIX,"stage2":12000.,"stage3":24000.}`. Make it `_go_record(binding=None)`; a given binding overrides those three keys.
- **Benchmark tree helper.** Add `_bench_tree(root, …)`:
  - It copies the seven (b′1) files from the real tree into `root` at the same relative paths. These are reads only.
  - It builds a COMPLETE record whose raw probe seconds give t* = 0.070 (C01 7,800, C2 12,600, C3 20,460). It must use the real benchmark module's `ceilings()`, `validate_record()` and `write_record()`, and real `source_identity(root)` and `environment_identity()`.
  - It writes the record to `root/results/c10z_astra_benchmark/20261007T000000Z/benchmark.json` and returns `(path, binding)`.
- **Stage-0 tests that reach the launch** need `_bench_tree` under the `ROOT` they run with, plus `C10Z_BENCHMARK_RECORD` and a go record built from the binding:
  - `:1181–1188` (`_review_stage_calls_with_go`, for `stage_call(0)` at `:1062`): also patch `D.ROOT` to the temp root. This is safe: verified that nothing in that test writes under `ROOT`.
  - `:1347–1365` (`D.ROOT` is `BlockingDemos`' temp root, `:1210`). `:1364` compares with the same `_go_record(binding)`.
  - `:1533–1546` (`D.ROOT=self.root`, `:1528`).

  Stage-0 tests that refuse earlier stay unchanged: `:1059`, `:1229`, `:1310–1345`, `:1413` with stage 0, `:1497`, `:1510` and `:1653`. The go record is still checked before the benchmark.
- **The one permitted assertion change.** At `:1086–1089` (`noceil`), the fixture's pass record has stage3 24000 while its launch has stage3 None. Under §9.1 (e′), `read_directory` rejects that mismatch, so `stage_call(3)` raises HALTED-V12 at `arms:1482–1483` before `arms:1484`.
  - Change the expectation to `assertRaisesRegex(R.Halt, "HALTED-V12: stage3 requires")`, keep `launched == []`, and give `noceil` `_launch(stage3=None)`. `R.Halt` renders as `"<code>: <detail>"` (`read:32–35`).
  - Report that `arms:1484` cannot be reached through any directory whose pass ceilings equal its launch. This is pre-existing; do not delete it.
- **Not required:** `:1069`. `stage_call(2)` (`arms:1489–1497`) reads only `launch["stage2"]`.
- **Successful stage-3 fixture.** Update selftest:1078–1080 to use `_bench_tree` under the patched ROOT. Populate its persisted launch with the real benchmark path, record/script hashes, source/environment identities, computed ceilings and matching go selection. Set the pass record’s ceilings to the same selected values and re-seal its schedule/history before persisting it. Retain the resident stub and the existing success assertions. Do not mock out `verify_launch_binding` in this test. New stage-3 drift tests start from this valid fixture and alter only their named condition. Placeholder bindings remain permitted in reader-only fixtures that never invoke launch admission.

### G. Telemetry MPS inertness check (§9.1 (h′3))

- In arms, add `telemetry_mps_inertness_check(model, device, population, batch, layers, tok)`, returning `{"verdict","control_equal","telemetry_equal","probe_forwards","lens_forwards"}`.
  - Every pass runs under `torch.no_grad()`.
  - Pass(lens):
    1. If `lens`, run `logit_lens(model, population["F0"], layers, tok, device)`.
    2. For each group and item in `population` order, as `probe_hits` (`arms:587–598`) but without budget or hook calls: run the greedy loop of `arms:553–557` for items with `"target"`, and the single forward of `arms:594–595` otherwise. Collect the tokens.
    3. If `lens`, run `logit_lens` again.
    4. Run the batch forward as `arms:484–486`, keeping `logits[rows,positions].detach().float().cpu()`.
  - Before P1, run one uncompared warm-up: one probe forward and one batch forward. Its forwards are not compared and not counted in `probe_forwards`.
  - Run P1 = pass(False), T = pass(True), P2 = pass(False). The verdict is NONDETERMINISTIC-BASELINE unless P1 and P2 have equal tokens and `torch.equal` logits; otherwise INERT if T equals P1 in both ways, else NOT-INERT.
- New `experiments/track_c/c10z_astra_telemetry_check.py`, the runner. Built now; it is not run.
  - Usage: `--out <abs>`. The out path must resolve under `ROOT/results/c10z_astra_telemetry_inertness/` and hold no `inertness.json`.
  - Preflight: `arms.entry_preflight`, engine fingerprint `main()==0`, and the env exactly as `arms:339`.
  - `torch.manual_seed(0)`. Import `c10e_bandknob` inside `main` only. Check MPS fp16 (`arms:344`) and `use_cache=False`.
  - Build the templates and population as the benchmark does (`population_and_batch`); `hp.layers` comes from `H.MEMITHyperParams.from_json(ROOT/HP)`.
  - Hash the 36 `down_proj` before and after (`tensor_hash`); a mismatch means INVALID and exit 2.
  - Write `inertness.json` atomically, as strict JSON: `{"schema":"c10z_astra_telemetry_inertness/v1","decision_id":"D-C10r-rulings-11","device":"mps","verdict":…,"control_equal":…,"telemetry_equal":…,"probe_forwards":…,"lens_forwards":…,"weights_unchanged":…,"sources":{arms, read, telemetry_check, benchmark, c10e_bandknob, hparams, memit_main},"env":environment_identity()+{"model_rev"},"started_at","finished_at"}`.
  - Exit 0 after writing any verdict. The top-level import is stdlib-only, and `run(out, H)` takes an injected `H` so it can be tested.
- **Stage-0 gate when telemetry is on** (step 11):
  - `C10Z_TELEMETRY_INERTNESS` is absolute and resolves to `ROOT/results/c10z_astra_telemetry_inertness/<dir>/inertness.json`.
  - Its bytes are read once and parsed as strict JSON.
  - Validate the complete inertness-record schema and internal consistency: the schema matches, device is "mps", verdict is "INERT", and control_equal, telemetry_equal and weights_unchanged are each exactly true. Require the probe/lens counts prescribed by the complete three-pass schedule. Reject missing or contradictory evidence with HALTED-V12. Test each rejection independently.
  - `sources` equals the current SHA-256s of those seven files, and `env` equals `environment_identity()` plus the pinned `model_rev`.
  - Store `{"path","sha256"}` in the launch. Stage 3 re-verifies the SHA and sources.

## 3. Order of work (each step's evidence goes in the report)

1. **Baseline.** Run `W/.venv/bin/python -B W/experiments/track_c/c10z_astra_selftest.py` on the untouched code. Save its tail and its failure count. The `:776` prereg-pin test is expected to FAIL: it is the red step for §2F.
2. **Test list first.** Before writing any production code, write the numbered test list (§4) into the report. Trace each item to its source: §9/§9.1 clause, v3 §D item, spec v2 test number, or this brief's §2 letter.
3. **Write the tests,** then run them on today's code and record which fail.
   - The idle-fix tests (i)–(vi), (viii) and (ix) MUST fail on today's code at their named behavioural assertion. Each is built through `_budget`, so a constructor `TypeError`, a `KeyError`, an `AttributeError` or a failure in `project()` never counts.
   - (vii) passes.
   - If an idle-fix test passes on today's code, or fails for the wrong reason, the test is wrong. Fix the test, not the code, and record that you did.
   - Separately, list the existing tests that fail on today's code only because of the new signature or fixtures. These are expected, and they are not red evidence.
4. **Implement** §2 A–G: the smallest code that turns the tests green.
5. **Full suites.** Run both selftests in full; both must be green. `"c10e_bandknob" not in sys.modules` must hold at the end of each. Run `W/.venv/bin/python -B W/tools/engine_fingerprint.py` (read-only) and require PASS. `git -C W diff --quiet -- memit_dry_run experiments/track_c/c10e_bandknob.py` must exit 0.
6. **Mutation check** (§5).
7. **Scope evidence** (§0), then the **report** (§6).

## 4. Required tests (minimum set; derive more where a clause needs them)

Every refusal test verifies the HALT code and the intended detail substring. For APIs that raise R.Halt, use assertRaisesRegex. For reader APIs that return a reading, assert scientific_verdict is false, label equals the expected HALT code, and detail contains the intended substring. Keep all prerequisites valid so an earlier refusal cannot substitute for the targeted check. For pre-attempt gates, it also asserts that the out directory holds no new file.

**Idle-time fix (§9.1 (f′)).** Build every Budget with `_budget(start,c01,c2,c3,process,clock)`. Detect the signature with `inspect.signature(D.Budget).parameters`; when there is no `stage01`, use the old form and set `durations["stage01"]=c01`. Run with C01 = 7,200.
- Harness: drive the real `Session.stage1` unbound on a stub, as v3 §D `:132`.
  - `run_recipe` advances the fake clock to the test's stage-1 return time.
  - `complete_recipe_readouts`, `write_checks` and `record` are no-ops; `record` returns `{}`.
  - `remaining_validation` is bound from `Session`, and `out` is a temp dir.
  - `R.read_process` is patched to return `{"scientific_verdict":True,"next_stage":2,"label":"PARTIAL"}`.
  - No test calls `complete01()` itself.
- (i)–(v) and (vii): as v3 `:133–137`, `:139`.
- (vi): install a recording `set` subclass as `budget.active` before stage 1. It records `deadline()` after every `add` and `discard` through stage-1 return, idle and `enter(2)`. Assertion: no recorded value is None (process 1).
- (viii): the clock stub returns origin+C01 on the first call and origin+C01−0.5 on every later call; `enter(2)` must raise HALTED-BUDGET `stage 0-1 deadline expired before stage-2 entry`. Second case: every call returns origin+C01−0.001; the entry is accepted and `origins["stage2"]` equals that value.
- (ix): barrier test.
  - Before starting the threads, replace `budget.lock` with an instrumented wrapper around a real `threading.RLock` that sets an event `t_attempt` when thread T calls its acquire (or `__enter__`), before delegating.
  - E and T are daemon threads. Thread E calls `enter(2)`. Its first clock call sets `inside` and waits on `release`.
  - After `inside`, thread T calls `deadline()`. Wait (bounded, for example 5 s) until `t_attempt` is set or T has finished; if the bounded wait expires with neither, fail the test explicitly (scheduling delay must not pass for blocking); then `T.join(0.2)`, and assert `T.is_alive()` with the message `deadline() returned while enter(2) held the transition lock`. On today's code T has already returned, so this assertion is the red step.
  - `release.set()` and the joins of both threads run in `finally` (or `addCleanup`), so a failing assertion cannot hang the suite. After release and join, assert that T's result equals entry+C2.
- AST check: `logit_lens` is called inside `Telemetry`, inside `telemetry_mps_inertness_check`, and nowhere else. `Session.stage0` calls `self.telemetry.logit_lens` in the statement after the pristine-probe loop, and `Session.arm_hook` calls it right after `self.current["hits"]=hits`. Real `stage0` cannot be driven under stubs (`arms:323`).

**Bounds and boundaries.** Test at each threshold, at both interior neighbours, and just outside.
- `Budget` `stage01`:
  - 7,199.999 refused; 7,200, 7,200.001, 10,799.999 and 10,800 accepted;
  - 10,800.001, NaN, inf, −inf, None and True refused.
- `ceilings()`:
  - spec v2 test 12's table;
  - injected pre-round sums of 10,800.0 → C01 10,800 with `stop` False, and 10,800.001 → C01 11,100 with `stop` True.
- Launch gates. With a consistent record, C01 ≥ 7,200 always holds, and C01 ≤ 10,800 implies total ≤ 55,800. So these gates are reachable only by **patching `D.benchmark_module`** so that the module it returns has `ceilings` replaced by a stub returning synthetic BENCHMARK dicts, with a matching `derived` and go `ceilings`:
  - C01: 7,199.999 refused; 7,200 and 10,800 accepted; 10,800.001 with `stop` False refused (the bounds gate, isolated);
  - `stop` True with C01 = 9,000 refused (the stop gate, isolated);
  - total: C01 10,800 with C2 17,099.9995 / 17,100 accepted, and with C2 17,100.001 refused.
- Benchmark `n_timed`: 199 INVALID; 200, 201, 398 and 399 CAPPED; 400 and 401 COMPLETE.
- Supervisor: no kill at T0 + 599.999, kill at T0 + 600.0 (fake clock), plus spec v2 test 6's real-process kill.
- Worker guard: `may_start(559.999)` / `(560.0)`; `phase_fits` at equality and at +0.001. SVD child killed at 565 s.
- Reader `stage01`: 7,199.999 / 7,200 / 7,200.001 / 10,799.999 / 10,800 / 10,800.001.
- Wrapper `next_stage`:
  - `null` → exit 0 with no stage 2; `2` → stage 2 runs;
  - `"2"`, `2.0`, `true`, `3` or a missing reading → exit 4;
  - a relative `C10Z_OUT_DIR` → exit 2;
  - a failing stage 0 → its own code, and stage 1 is never called.

  Use a stub tree under `/private/tmp/c10z_build/` with a stub `tools/run_c10z_stage.sh` and `.venv/bin/python` symlinked to the real interpreter.

**Launch-binding HALT tests: one per row of the §2B table.**
- They include the `stage_call(3)` re-verification: changed record bytes, changed script, changed source file (helper drift: edit the copied `c10z_astra_arms.py` in the temp tree), changed environment field (patch `environment_identity` in the module `D.benchmark_module` returns), and a changed `C10Z_TELEMETRY`.
- Substitution tests:
  - (a) a second, internally valid record in another `<run>` directory, selected by env while the go record names the first → `benchmark record differs from go selection`;
  - (b) the same record bytes with one raw `seconds` value changed and `derived` recomputed → the SHA mismatch;
  - (c) a record whose recorded p95 disagrees with its raw seconds, with the go record re-pointed at its SHA → `benchmark record invalid`.
- go-record field tests: each new key missing, wrong type, uppercase or short hex, a `ceilings` key missing or extra, a bool, NaN.
- Success test: the launch dict holds `stage01`, `benchmark`, `telemetry` False and `telemetry_inertness` None, and `run.json`'s launch round-trips.

**Reader, including in-range mismatches.**
- Launch stage01 7,200 against pass 10,800; launch stage2 12,600 against go 12,900; launch stage3 None with pass 24,000.
- A history entry with `ceilings.stage01` 9,000 against record 7,800; a scope `ceiling_s` mismatch.
- Process 1 at 7,800 against process 2 at 8,100.
- `launch.benchmark.sha256` ≠ go `benchmark_sha256`.
- A record with stage01 5,400 (out of range).

Each gives HALTED-V12 with its detail.

**Round-trips, for every persisted record.** Write it, read it back, and compare as JSON-normalised (`json.loads(json.dumps(x, sort_keys=True, allow_nan=False))`):
- `benchmark.json` (spec v2 test 8) with the new env fields;
- the go record with the new keys;
- `run.json` with the new launch keys;
- a pass record with `budget.ceilings.stage01` = C01;
- `halt_p1.json`;
- `inertness.json`;
- every telemetry JSONL line, one by one.

**Telemetry.**
- (T1) Off by default: with the variable absent, there is no `telemetry/` directory, `session.telemetry is None`, and spies on every `Telemetry` method record zero calls.
- (T2) Inertness of the code path (§9.1 (h′4)).
  - Drive the real `Session.write_arm` on the `_write_session` stub, extended with `active_recipe="Z"`, `population`, `hp.layers=[4,5,6,7,8]` and an `H` holding the T6 tiny model.
  - Drive the real `Session.arm_hook` on that stub, with stub `probe_hits`, `make_batch`, `transfer_diagnostic` and `footprint`, and `gates.law3=True`.
  - Drive the resident flow (`_mock_resident`) with `launch["telemetry"]` True and False.
  - Use injected clocks, a fixed `uuid.uuid4`, a fixed pid and a stub `check_memory` returning constants.
  - Require, telemetry on against off:
    - every return value, every record written, every reader reading, and the out-directory file set excluding `telemetry/` are identical (JSON-normalised); the only exceptions are `run.json`'s `launch.telemetry` and `launch.telemetry_inertness`;
    - the call counts of the budget clock, `D.time.monotonic`, `project`, `check`, `hooks_check` and `sync` are identical;
    - the stub model's forward count is identical, excluding telemetry-tagged forwards.
- (T3) The on-run file holds the header and all four kinds, with the §2D fields and placements, including `round_no:"final"`.
- (T4) Unit test: call each `Telemetry` method directly with spies on the budget clock, `project`, `check`, `hooks_check`, `sync` and `D.time.monotonic`. All counts must be zero.
- (T5) Separate failure tests. (T5a–d) Ordinary telemetry I/O failures each print exactly one C10Z_TELEMETRY_DISABLED line, disable later telemetry work, preserve science records and permit normal completion. (T5e) A KeyboardInterrupt raised inside telemetry propagates from the telemetry method; assert that exception directly. T5e does not require a disabled marker or normal completion.
  - (a) directory creation or open fails at initialisation;
  - (b) `write` raises;
  - (c) `flush` raises;
  - (d) `os.fsync` raises;
  - (e) a `KeyboardInterrupt` raised inside telemetry propagates (it is not caught).
- (T6) LAW#5 state checks on a tiny CPU module. It is hand-built in torch, with no transformers: embedding, ≥ 10 layers, `model.norm`, `lm_head`, `config.num_hidden_layers`, and Qwen2-style `hidden_states` (the input to each layer, then the norm of the last output).
  - Each layer l adds a distinct vector (l+1)·e_l, so the test can assert that lens layer l used `hidden_states[l+1]`, the output of layer l. A stub tokenizer `decode` lets it assert the top-5 ids, texts and probabilities.
  - Before and after each telemetry call, these are unchanged:
    - every parameter and buffer (`torch.equal` and `data_ptr`);
    - `torch.random.get_rng_state()`;
    - `model.training`;
    - every module's `_forward_hooks`, `_forward_pre_hooks` and `_backward_hooks`;
    - `torch.is_grad_enabled()`.
  - The stub's norm and head `forward` methods assert `not torch.is_grad_enabled()`; they are plain module code, not hooks.
  - A fixed science forward run after the call is `torch.equal` to one run without it.
  - The input tensors given to telemetry hash the same before and after.
- (T7) `target_probabilities` matches a dense float64 softmax on a small case to within 1e-6. A spy on the slicing shows that every slice has ≤ `chunk_rows` rows. tracemalloc cannot see torch allocations, so do not use it.
- (T8) The switch and the inertness gate:
  - `0`, `true`, the empty string and ` 1` → HALTED-V12 at stage 0 and at stage 3;
  - `1` without `C10Z_TELEMETRY_INERTNESS` → V12;
  - verdict NOT-INERT, verdict NONDETERMINISTIC-BASELINE, a changed source SHA, a changed environment field, a path outside the root, or non-strict JSON → each V12;
  - a valid INERT record → `launch["telemetry"]` True with its binding;
  - stage 3 with a different `C10Z_TELEMETRY` → V12.
- (T9) Cost bound: a write with R rounds emits exactly 1 + 3R + 1 telemetry lines, and `arm_hook` emits exactly 1 more. No line is per requirement.

**Inertness check.** On stub models:
- a deterministic stub → INERT;
- a stub whose outputs depend on a counter advanced only by `output_hidden_states=True` forwards → NOT-INERT;
- a stub that drifts every pass → NONDETERMINISTIC-BASELINE.

Also: the probe/greedy/batch forward kwargs equal the `arms:553–557`, `:594–595` and `:484–486` calls; the runner's out-path refusals work; and a stub `H` whose `my_edit`, `run_recipe`, `run_law5` and `apply_memit_to_model` raise lets the runner complete.

**Benchmark.** All of spec v2 tests 1–12, plus its cross-process clock test, plus:
- `source_identity` over a temp root;
- `environment_identity` imports no torch (`"torch" not in sys.modules` in a subprocess);
- `validate_record`'s measurement-consistency rejections;
- the top-level stdlib-only import (in a subprocess, importing the module adds no non-stdlib module).

**Pin.** The `:776` test passes against the new SHA, and fails if one byte is appended to a temp copy. Point the test at the copy through a parameter; do not edit the prereg.

## 5. Mutation check (each mutant must turn at least one named test red)

For each mutant:
1. Copy the target file to `/private/tmp/c10z_build/mut_backup/`.
2. Apply the mutant in place and run the relevant suite.
3. Restore the file from the backup **in a `finally` block**, and verify that its SHA-256 equals the pre-mutation SHA.

Record mutant → failing test names.

- M1 `enter`: `<` → `<=`.
- M2 `enter`: `complete01()` before `active.add`.
- M3 `deadline()` without the lock.
- M4 `Session.stage1` calls `complete01()` again.
- M5 Budget upper bound 10,800 → 10,800.001.
- M6 Budget lower bound removed.
- M7 the stage-0 total 55,800 check removed.
- M8 the `derived` agreement check removed.
- M9 the script-SHA check removed.
- M10 telemetry on when the variable is absent.
- M11 telemetry adds one key to the pass record.
- M12 telemetry calls `budget.clock()` once.
- M13 reader bound changed to `==5400.`.
- M14 benchmark COMPLETE threshold 400 → 399.
- M15 `ceilings()` returns `FALLBACK` for INVALID.
- M16 wrapper accepts the string `"2"`.
- M17 go `benchmark_sha256` comparison removed.
- M18 source-identity check removed.
- M19 environment-identity check removed.
- M20 `validate_record` measurement consistency removed.
- M21 stage-0 C01 bound check removed.
- M22 `stage_call(3)` re-verification removed.
- M23 reader pass-ceiling == launch removed.
- M24 reader p1 == p2 ceilings removed.
- M25 reader history-ceiling check removed.
- M26 telemetry on accepted without an INERT record.
- M27 `logit_lens` uses `hidden_states[l]`.
- M28 `logit_lens` norm/head outside `no_grad`.
- M29 telemetry catches `BaseException`.
- M30 one `target_probs` line per requirement.
- M31 telemetry calls `time.monotonic` instead of `TELEMETRY_CLOCK`.

A mutant that survives is a missing test. Add the test, then re-run the mutant.

## 6. Report: `results/c10z_build_codex_impl.md` (the only report location)

1. Files changed: each path with its SHA-256 before and after (`shasum -a 256`), and the §0 scope evidence:
   - the `git status --porcelain` diff;
   - the FROZEN source/input SHA table, before = after;
   - the frozen result-directory listings, with any change reported separately as observed, not attributed.
2. The numbered test list → test name (class.method) → source clause.
3. Idle fix before/after:
   - each red test's name and its behavioural assertion message on today's code, with no TypeError, KeyError or AttributeError;
   - the same tests passing after the fix;
   - the separate list of expected fixture-signature failures;
   - the step-1 baseline tail, and the pin red → green.
4. Every §2F fixture edit with file:line, and the one assertion change with its reason.
5. The selftest output tail of both suites: the last 15 lines, including `C10Z_ASTRA_SELFTEST_PASS tests=<n>` and `C10Z_BENCH_SELFTEST_PASS tests=<n>`.
6. The mutation table.
7. The engine fingerprint output, and the engine/harness `git diff --quiet` exit code.
8. Open issues: every place you deviated, guessed or could not satisfy a clause, with file:line. Write "none" only if there are none.
9. Not run, for the program:
   - the benchmark command (spec v2 §3);
   - the inertness-check command `LLMDB_ROOT=<W> <W>/.venv/bin/python -B <W>/experiments/track_c/c10z_astra_telemetry_check.py --out <W>/results/c10z_astra_telemetry_inertness/<UTC>`;
   - the §9.1 (j′) launch lines.

When the report is written, print `DONE` and stop.

**Rejected on review:**
- tests written after the code; idle-fix tests that pass on today's code, or that fail there with a TypeError, KeyError or AttributeError;
- any write outside the allowed paths, or any change to a FROZEN file;
- any GPU job, model load or `mps` tensor;
- telemetry that is on by default, that is on without an INERT record, or that touches a record, a clock or a hook;
- a vague "telemetry added" without the four kinds, T2 and T6;
- a hard-coded C01, or a reader that checks only the range;
- any fallback ceiling path;
- a HALT test that asserts only the code, or that passes because an earlier gate refused;
- a commit.
