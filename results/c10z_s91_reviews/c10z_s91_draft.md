## 9.1 Revision of Amendment A (2026-10-07, pre-observation, D-C10z-budget / D-C10r-rulings-11 / D-C10z-c01input)

Written before any ASTRA process, benchmark run or build against §9 has started; `results/c10z_astra/` and `results/c10z_astra_benchmark/` are absent. §9 and all text above it are unchanged. Where §9.1 conflicts with §9, §9.1 governs; where a §9 sentence is replaced, it is quoted exactly below. Sources: GPT-6-Astra review `results/c10z_amend_review_astra.md` (FIX-FIRST, blocking 1–5) and Opus advisor review `results/c10z_amend_review_advisor.md` (PROCEED-WITH-CHANGES, B1–B4, A1–A7). Line references to §9 are to this file as it stood with §9 as its last section (`:449`–`:478`).

(a′) **C01 is a launch input (D-C10z-c01input).** Production driver and reader code must obtain the selected C01 from validated launch provenance; they must not hard-code the benchmark-selected value. Literal contractual bounds and numeric synthetic test fixtures, including C01_FIX and boundary cases, are permitted. Tests must not treat a fixture value as the selected live ceiling. The driver's `Budget` takes C01 as an argument and refuses (HALTED-BUDGET) any value that is not a finite real number with 7,200 ≤ C01 ≤ 10,800. At stage 0, C01 is read from the benchmark record selected under (b′) and checked there against 7,200 ≤ C01 ≤ 10,800 and 2·(C01 + C2) ≤ 55,800 s. v3 §E's "`arms:88` `5400.` → C01" and "`read:500` `==5400.` → `==C01`" are implemented by (a′), (b′) and (e′), not by editing in a number after the benchmark.

(b′) **Benchmark identity and the go binding.** §9(b) sentence "At stage-0 launch the driver recomputes `ceilings()` on that record, requires `source` BENCHMARK and agreement with the record's own `derived`, and writes the record path, the record SHA-256 and the benchmark script SHA-256 into the launch record." is superseded by (b′1)–(b′4).

- (b′1) **The record carries its identity.** Besides the spec v2 fields, the benchmark record's `env` holds:
  - `sources`: the SHA-256 of exactly these files, by path relative to the worktree: `experiments/track_c/c10z_astra_benchmark.py`, `experiments/track_c/c10z_astra_arms.py`, `experiments/track_c/c10z_astra_read.py`, `experiments/track_c/c10e_bandknob.py`, `configs/hparams/qwen25_3b_memit_hparams.json`, `tools/engine_fingerprint.py`, `memit_dry_run/memit/memit/memit_main.py`;
  - `python` (`platform.python_version()`), `machine` (`platform.machine()`), `platform` (`platform.platform()`), and `torch` and `transformers` taken from `importlib.metadata.version(...)`.

  `ceilings()` computes t* from the raw `seconds` arrays, not from the recorded summary statistics. The benchmark module's `validate_record()` recomputes every recorded summary statistic from those arrays and checks the spec v2 schema and status bands, so a record whose summaries disagree with its raw data is invalid.
- (b′2) **The go record names the selected benchmark.** The go record (v3 §F, `arms:1342–1361`) gains three required keys, validated in format before anything else is read (HALTED-V12):
  - `"benchmark_sha256"`: the SHA-256 of the selected record file's bytes;
  - `"benchmark_script_sha256"`: that record's `env.script_sha256`;
  - `"ceilings": {"stage01": C01, "stage2": C2, "stage3": C3}`: the values `ceilings()` computed for it.

  The program writes these only after appending the same SHA-256s and numbers to the D-C10z-budget row (§9(b)'s last two sentences are unchanged). Before writing the go record, the program greps that row for both SHA-256 strings and the three numbers; the driver checks the go record, not the runbook.
- (b′3) **Stage-0 admission**, in this order, all before any attempt write (before `out.mkdir` and `run.json`). The first failing step halts with the code shown, and nothing is written:
  1. The existing fresh-OUT_DIR check and go-record check (`arms:1465–1467`), now including (b′2)'s fields. → HALTED-V12.
  2. The telemetry switch under (h′1). → HALTED-V12.
  3. `C10Z_BENCHMARK_RECORD` is present, absolute, and resolves to `<ROOT>/results/c10z_astra_benchmark/<one directory>/benchmark.json`, an existing file. → HALTED-V12.
  4. Its bytes are read once. The SHA-256 of those bytes must equal the go record's `benchmark_sha256`. The same bytes are parsed as strict JSON with no non-finite number. → HALTED-V12.
  5. The current SHA-256 of the benchmark script equals the record's `env.script_sha256` and the go record's `benchmark_script_sha256`. Every file in (b′1) `sources` has its recorded SHA-256 now. The current `python`, `machine`, `platform`, `torch` and `transformers` values equal the record's. → HALTED-V12.
  6. `validate_record(record)` passes. → HALTED-V12.
  7. `ceilings(record)` recomputed: `source` is BENCHMARK, or HALTED-BUDGET. The result equals the record's `derived` exactly, or HALTED-V12.
  8. `stop` is false; 7,200 ≤ C01 ≤ 10,800; 2·(C01 + C2) ≤ 55,800. Each is a separate check. → HALTED-BUDGET.
  9. The go record's `ceilings` equal the recomputed C01/C2/C3. → HALTED-V12.
  10. `C10Z_STAGE2_CEILING_S` and `C10Z_STAGE3_CEILING_S`, when present, equal C2 and C3 (§9(d), unchanged). → HALTED-BUDGET.
  11. If telemetry is on, the inertness record under (h′3). → HALTED-V12.

  The launch record then gains:
  - `"stage01": C01`;
  - `"benchmark": {"path", "sha256", "script_sha256", "sources", "env", "ceilings"}`;
  - `"telemetry": true|false`;
  - `"telemetry_inertness": {"path", "sha256"}` or `null`.
- (b′4) **Staleness** is defined by identity, not by age. A record is usable while (b′3) steps 3–9 pass. If a file in (b′1) `sources`, or the environment, changes after the benchmark ran, the record becomes unusable. A fresh benchmark is then run in a new directory, followed by a new D-C10z-budget append and a new go record. Such a re-run replaces a record made stale by drift. Identity drift itself is not a §9(c) refusal and does not consume §9(c)'s one-rerun allowance. At most one such drift-forced re-run is made on the program's own call; a second drift-forced re-run returns to the operator, as a refusal would (D-C10z-driftcap). Only a record that was usable before the change (it passed (b′3) steps 3–9 against the go record that names it) can be replaced this way. A record that drifts before any go record names it is simply not selected; a fresh run in its place is a drift-forced re-run under the same cap. A prior REFUSED or INTERRUPTED record remains subject to §9(c)'s one-rerun allowance and cumulative refusal count; identity changes neither reset that count nor grant a drift replacement. A prior STOP returns to the operator regardless of later changes. The replacement benchmark's outcome remains subject to §9(c): REFUSED or INTERRUPTED increments the cumulative refusal count, a second refusal returns to the operator, and STOP returns to the operator. §9(c)'s bounds and STOP rule apply to every record.

(d′) **Carrying the binding through the attempt.**
- The process-1 resident builds `Budget(start, launch["stage01"], launch["stage2"], launch["stage3"], process=1)` and takes the telemetry switch from `launch["telemetry"]`. It does not re-read the benchmark record, because its launch comes from the stage-0 call that verified it, through the child's environment.
- Process-2 admission (stage 3) re-verifies the binding from `run.json`'s launch, after the existing stage-3 checks (`arms:1480–1486`) and before `process2/` is created or the model is imported. The record bytes at `launch["benchmark"]["path"]` must hash to `launch["benchmark"]["sha256"]`, which equals `launch["go"]["benchmark_sha256"]`. The script, `sources` and `env` identities must still match. `ceilings()` recomputed on those bytes must equal `launch["benchmark"]["ceilings"]` and the go record's `ceilings`, and `launch["stage01"]` must equal C01. If telemetry is on, the inertness record must still hash to `launch["telemetry_inertness"]["sha256"]` and its sources must still match. Any failure → HALTED-V12. Process 2 builds its `Budget` from `launch["stage01"]`.

(e′) **Reader: range check plus exact provenance.** v3 §E's "`read:500` `==5400.` → `==C01`" is superseded by the following, which keeps the exact-equality invariant that the 5,400 constant used to give.
- `read_process` (validation):
  - `ceilings["stage01"]` is a finite number, not a boolean, with 7,200 ≤ stage01 ≤ 10,800 (HALTED-V12, "phase01 clock provenance").
  - Every projection in `budget.history` has `ceilings` equal to the record's `budget.ceilings`, and each scope's `ceiling_s` equals the matching ceiling (HALTED-V12).
- `read_directory`, for each closed, non-halted process directory:
  - The pass record's `budget.ceilings[k]` equals `run.json`'s `launch[k]` for k = stage01, stage2, stage3.
  - `launch["stage01"]` equals `launch["go"]["ceilings"]["stage01"]`.
  - `launch["stage2"]` and `launch["stage3"]` are each either null, meaning the expansion was not launched, or equal to the go record's value.
  - `launch["benchmark"]["sha256"]` equals `launch["go"]["benchmark_sha256"]`.
  - Each failure → HALTED-V12.
- `read_run`: process 1's and process 2's `budget.ceilings` are equal (HALTED-V12).
- Reader tests include in-range mismatches (for example, launch 7,200 against pass 10,800), not only out-of-range values.

(f′) **Idle-time fix: test definitions.** §9(e) sentence "Build requirement: v3 §D tests (i)–(ix) are written first and recorded failing on the pre-fix code, except invariant (vii), which already passes." is superseded by the following. The rest of §9(e) is unchanged. In particular, `enter` follows v3 `:113–124` exactly, including `if key not in self.origins`.
- **Harness and adapter.**
  - Every idle-fix test builds its `Budget` through one test helper, `_budget(start, c01, c2, c3, process, clock)`. When `Budget` has a `stage01` parameter (checked by signature inspection, not by catching `TypeError`), the helper uses the new signature. Otherwise it uses the old one and sets `durations["stage01"] = c01`.
  - Tests that drive stage 1 run the real `Session.stage1` unbound on a stub, as v3 §D describes. The stub's `run_recipe` advances the fake clock from stage-1 start, where `project()` fits, to the test's stage-1 return time, so no test fails early in `project()`.
  - On the pre-fix code, each of (i)–(vi), (viii) and (ix) must fail at its named behavioural assertion. A `TypeError`, `KeyError`, `AttributeError` or failure in `project()` does not count as the red step.
- (i)–(v) and (vii): as in v3 §D.
- (vi), restated:
  - The test installs a recording `set` subclass as `budget.active` before it drives `Session.stage1`. After every `add` and `discard`, it records `deadline()`.
  - It covers stage 1's return, the idle interval and `enter(2)`. No recorded value may be None (process 1).
  - Today, the failure comes from the discard in `Session.stage1` (`arms:1259`), not from `enter` (`arms:106–110`).
- (viii), restated: the clock stub returns origin + C01 on its first call and origin + C01 − 0.5 on every later call. `enter(2)` must refuse with "stage 0-1 deadline expired before stage-2 entry". Today it does not refuse, because its decision uses a second clock read. A second case, with every call at origin + C01 − 0.001, is accepted, and `origins["stage2"]` equals that value exactly.
- (ix), restated as a barrier test:
  - Thread E runs `enter(2)`, and its first clock call blocks on an event.
  - While E is blocked, thread T calls `deadline()`.
  - T must still be running after 0.2 s, with the assertion message "deadline() returned while enter(2) held the transition lock". After release, T returns entry + C2.
  - Today, and with `deadline()`'s lock removed, T returns immediately.
  - The 1,000-iteration stress test is not required.

(h′) **Telemetry, corrected.**
- (h′1) **Switch.** §9(h) sentence "Telemetry is on only when `C10Z_TELEMETRY=1` at launch." is superseded by: "Telemetry is on only when `C10Z_TELEMETRY=1` at stage-0 launch and (h′3)'s inertness record is valid. The choice is recorded in `launch["telemetry"]`, and both processes of the attempt follow it. At stage 3, a `C10Z_TELEMETRY` value that differs from `launch["telemetry"]` is refused (HALTED-V12)." The rest of the Switch bullet is unchanged.
- (h′2) **What telemetry can change.** §9(h) sentences "Its own elapsed time counts against the nominal deadlines and is not projected. Timing fields may therefore differ by that time, which the telemetry file records. No count, lead, hit, label, hash or reading may differ." are superseded by:
  - "Its own elapsed time counts against the nominal deadlines and against each write's `wall_seconds`, and is not projected. It is never subtracted from W2, a deadline or a projection.
  - Each telemetry line records its own `elapsed_s`, the time from entering the telemetry call to just before that line is written, and `cumulative_s`, the full time of all earlier lines, writes included.
  - With telemetry on, these fields may differ:
    - timing fields: `wall_seconds`, `round_seconds`, trace `seconds` and `head_seconds`, `solve_seconds`, `timings`, and budget-history `elapsed_s`, `remaining_s` and the time-derived `components_s`;
    - memory observations: `rss_bytes` and `driver_bytes`.
  - So a run near a deadline, the 3,600-s TTL (W2, `read:328`, `:571`) or the V11 ceiling can end HALTED-BUDGET, gain EXCEEDS-TTL (and with it lose K1/K2 continuation), or end HALTED-V11 where the telemetry-off run would not. Such an attempt is not an identical-reading run.
  - Under the controlled stub proof (h′4), every other count, lead, hit, hash and reading is identical. On MPS, INERT establishes equality only for the pristine A7 probe tokens and gathered batch logits specified in (h′3), under the recorded source/environment identity. It is the required admission screen for telemetry-on attempts; it does not establish resource inertness or universal equality of edited-arm outputs and records. Those broader claims remain UNVERIFIED. The timing/resource exceptions and description rule remain binding."

  **Description rule** (like §9(g), it changes no gate or label): if a telemetry-on attempt ends HALTED-BUDGET or HALTED-V11, or carries EXCEEDS-TTL on any write, the program reports it as possibly affected by telemetry. It does not treat that attempt as evidence about ASTRA's time or memory cost until a telemetry-off attempt says the same.
- (h′3) **MPS inertness check (LAW#5) and the first attempt.**
  - The first ASTRA attempt runs with telemetry off: `C10Z_TELEMETRY` absent.
  - A telemetry-on attempt requires an inertness record, `results/c10z_astra_telemetry_inertness/<UTC>/inertness.json`. It is written by `experiments/track_c/c10z_astra_telemetry_check.py`, which runs `telemetry_mps_inertness_check()` from the driver once on MPS with the GPU otherwise idle.
  - Method:
    - In one process, on the pristine model, it runs three passes: P1 plain, T interleaved, P2 plain.
    - Before P1, a short warm-up (one probe forward and one batch forward) runs and is not compared, so that a cold-start difference between P1 and P2 cannot give NONDETERMINISTIC-BASELINE.
    - Each pass runs every A7 probe forward in driver order (greedy items as `arms:550–558`, single-forward items as `arms:594–595`), then one A7 identity-batch forward as `arms:484–486`, keeping `logits[rows, positions]`.
    - Pass T also runs the driver's own `logit_lens` on the A7 F0 prompts before the probes and again between the probes and the batch forward. The second call reproduces the on-run position of both call sites (after a probe loop, before an observe-shaped forward); the first exposes probe forwards that follow a lens call.
  - Verdict:
    - NONDETERMINISTIC-BASELINE unless P1 and P2 have identical tokens and `torch.equal` gathered logits;
    - otherwise INERT if T matches P1 the same way, and NOT-INERT if it does not.
    - Only INERT admits telemetry. Any other verdict keeps telemetry off for this prereg.
  - The record holds the verdict, `device: "mps"`, the SHA-256s of the driver, reader, check script, benchmark script, harness, hparams and `memit_main.py`, and (b′1)'s environment fields. Stage 0 requires all of these to match the current files and environment.
  - Cost (I-INFER): three passes of about 11,200–11,400 probe forwards each, roughly 17–85 GPU-minutes at t = 0.03–0.15 s. It is not part of the 2·(C01 + C2) ≤ 55,800 s attempt bound and is not covered by D-C10z-budget's approved GPU time. It runs only if the program wants telemetry on, and only after the operator says yes to its stated GPU cost (asked in plain words, recorded with a D-ID in runbook §5.2); its measured GPU time is then recorded in that row.
- (h′4) **Proof.** §9(h) sentence "With a stub model and an injected clock, every record and reading is identical (JSON-normalised) with telemetry on and off, and the on-run file contains all four snapshot kinds." is superseded by:
  - "With a stub model and injected clocks, every record, reading and out-directory file except `telemetry/` is identical (JSON-normalised) with telemetry on and off. The only exceptions are `run.json`'s `launch.telemetry` and `launch.telemetry_inertness`.
  - The counts of budget-clock, `time.monotonic`, `project`, `check`, `hooks_check` and `sync` calls are identical too.
  - The on-run file contains all four snapshot kinds.
  - CPU tests show that a telemetry call leaves model parameters and buffers, RNG state, train/eval mode, the hook registry, grad mode and the next science forward's output unchanged.
  - This proves the code path only. It does not prove live inertness, which is (h′3)'s job."
- (h′5) **Fields and placement.**
  - §9(h) item "(1) phase markers: stage, recipe, arm and round start/end, and the halt code on a halt;" is superseded by: "(1) phase markers:
    - stage start/end, written by the resident around each stage;
    - recipe start/end;
    - a write-start marker, written before the write's clock starts (`arms:706`);
    - one round-end marker per round, written after `round_guard` (`arms:740`) and carrying that round's already-measured `seconds`;
    - the halt code on the resident's halt path (`arms:1452–1457`; not from the watchdog thread)."

    No marker is written inside a round's timed interval.
  - Volume: one line per event and per round:
    - one `write_norms` line per round;
    - one `target_probs` line per round from that round's `post` (`arms:725`), with parallel arrays (row, fact, view, q, p), plus one for the final `post` (`arms:743`);
    - one `logit_lens` line per pristine baseline and per candidate write.

    Each line is flushed and fsynced. There is never one line per requirement.
  - Logit lens:
    - the residual after band layer l is `hidden_states[l+1][:, -1, :]` (installed transformers 4.51.0, `modeling_qwen2.py:532–570`; valid for l ≤ 34);
    - the whole calculation, the forward, `model.model.norm` and `lm_head`, runs under `torch.no_grad()`;
    - telemetry catches `Exception`, not `BaseException`.

(i′) **Closing sentence.** §9 sentence "Nothing else changes: no gate, label, K1/K2 rule, projection, probe, round cap (V13) or never-zero rule." is superseded by: "Nothing else changes: no gate, label, K1/K2 rule, projection, probe, round cap (V13) or never-zero rule, other than the declared `read:500` bound and provenance checks of (e′) and the (e) deadline scope." §9's last sentence, "Ceilings never increase during an attempt.", is unchanged.

(j′) **Launch lines** (they correct v3 §G `:245` and `:247`; telemetry stays off for the first attempt, so it is removed explicitly in case it is inherited):
- Process 1: `nohup caffeinate -i env -u C10Z_TELEMETRY -u C10Z_TELEMETRY_INERTNESS LLMDB_ROOT="$W" C10Z_OUT_DIR="$W/results/c10z_astra" C10Z_GO_RECORD="$W/results/c10z_astra_go_record.json" C10Z_BENCHMARK_RECORD="$W/results/c10z_astra_benchmark/<UTC>/benchmark.json" C10Z_STAGE2_CEILING_S=<C2> C10Z_STAGE3_CEILING_S=<C3> "$W/tools/run_c10z_attempt.sh" > "$W/results/c10z_astra_chain.log" 2>&1 &`
- Stage 3, only if the stage-2 reading's `next_stage` is exactly 3 (v3 §G `:247`): `nohup caffeinate -i env -u C10Z_TELEMETRY -u C10Z_TELEMETRY_INERTNESS LLMDB_ROOT="$W" C10Z_OUT_DIR="$W/results/c10z_astra" C10Z_GO_RECORD="$W/results/c10z_astra_go_record.json" C10Z_BENCHMARK_RECORD="$W/results/c10z_astra_benchmark/<UTC>/benchmark.json" C10Z_STAGE2_CEILING_S=<C2> C10Z_STAGE3_CEILING_S=<C3> bash -c '"$1" 3; rc=$?; echo "STAGE_3_EXIT=$rc"; exit "$rc"' _ "$W/tools/run_c10z_stage.sh" > "$W/results/c10z_astra_stage3.log" 2>&1 &`. Stage 3 re-verifies the binding from `run.json` (d′), so `C10Z_BENCHMARK_RECORD` and the two ceiling variables are optional there; they are kept so the variables match process 1.
