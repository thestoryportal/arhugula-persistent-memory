# C10Z amendment fold map: reviews → §9.1 and brief v2

Files:
- §9.1 draft: `/Users/robertrhu/.claude/jobs/8ac4cacf/tmp/c10z_s91_draft.md` (to be appended after §9 of `docs/C10Z_ASTRA_PREREG.md`).
- Brief v2: `/Users/robertrhu/.claude/jobs/8ac4cacf/tmp/codex_c10z_build_brief_v2.md`.

Reviews:
- Astra: `results/c10z_amend_review_astra.md` (FIX-FIRST).
- Advisor: `results/c10z_amend_review_advisor.md` (PROCEED-WITH-CHANGES).

All file:line citations below were re-read for this fold.

**Citation corrections:**
- The advisor's "prereg:474/475/477" are off by one. The §9(h) Inertness bullet is at `:475`, the Proof bullet at `:476`, and the closing sentence at `:478` (`grep -n`, prereg SHA `e2d7fa10…`). Astra's `:475–476` is correct.
- The advisor's "packet:N" equals brief v1 line N−21 (checked at packet:22, :57 and :140).

## BLOCKING

| # | Reviewer item (quote) | Resolved in | How |
|---|---|---|---|
| 1 | Astra 1: "Telemetry's unchanged-reading guarantee conflicts with the frozen timing gates" | §9.1 (h′2); brief §2D, §4 T2 | (h′2) quotes and supersedes the last three sentences of §9(h) Inertness. Telemetry time counts against deadlines and `wall_seconds`, and is never subtracted from W2, a deadline or a projection. The timing and memory fields that may differ are listed. HALTED-BUDGET, EXCEEDS-TTL (W2) and HALTED-V11 may differ, and such an attempt "is not an identical-reading run". A description rule keeps such outcomes from being read as ASTRA cost evidence. |
| 2 | Astra 2: "The new reader range check loses the old exact-ceiling invariant" | §9.1 (e′); brief §2B Reader, §4 Reader | Range check plus: history `ceilings` and `ceiling_s` equal the record's; pass ceilings equal the run.json launch (stage01/2/3); launch stage01 equals the go value; stage2/3 are null or equal the go value; launch benchmark SHA equals go; p1 ceilings equal p2. In-range mismatch tests are required. Mutants M23–M25. |
| 3 | Astra 3: "Recomputation plus a newly recorded hash does not authenticate the selected benchmark" | §9.1 (b′1)–(b′4), (d′); brief §2B table, §2C, §4 | Go record carries `benchmark_sha256`, `benchmark_script_sha256` and `ceilings`. Stage 0: one read; hash and parse the same bytes; SHA equals go. The record carries a seven-file `sources` map plus python/machine/platform/torch/transformers, and stage 0 recomputes and compares them (helper drift). `validate_record` checks measurement consistency, and `ceilings()` uses raw arrays. Process-2 admission re-verifies before `process2/` exists. Substitution, helper-drift and changed-record tests are listed. Staleness is defined by identity, not age. **Partial, with reasons:** (i) the process-1 resident does not re-hash, because its launch comes from the verifying stage-0 call through the child env, a trusted handoff with the identity sources unchanged (`arms:1472–1475`), and stage 3 re-verifies; (ii) the go record ↔ runbook-row match stays a program-side grep before the go record is written, not a driver check. |
| 4 | Astra 4: "The required idle-fix RED evidence is underspecified, and the concurrency assertion cannot prove locking" | §9.1 (f′); brief §2A, §3 step 3, §4 Idle-time fix | (vi) is restated: the recording set is installed before the real `Session.stage1`, because today's discard is at `arms:1259`, not in `enter` (`:106–110`). (viii) uses a non-monotone clock stub so the decision must use the single captured timestamp. (ix) becomes a barrier test ("deadline() returned while enter(2) held the transition lock"), which also kills M3. The `_budget` adapter and a `run_recipe` clock advance prevent constructor or `project()` failures. Only the named behavioural assertion counts as RED. The 1,000-iteration stress test is dropped (Astra showed it proves nothing). |
| 5 | Astra 5: "The on/off proof is insufficient for the extra model forwards" | §9.1 (h′3), (h′4); brief §2G, §4 T6, Inertness check | T6 on a tiny CPU module checks parameters/buffers, RNG, mode, every hook dict, grad mode, the next science output, and no-grad inside norm/head. Live inertness is labelled UNVERIFIED until the MPS check (advisor B2) returns INERT. The first attempt runs with telemetry off. |
| 6 | Advisor B1: "§9(h)'s inertness sentence is false against the code" | §9.1 (h′2), (h′5); brief §2D, §4 T2/T9 | The advisor's replacement text is adopted verbatim in substance, with the addition that hashes and readings are identical "on stubs; on MPS only after (h′3)". `elapsed_s` (plus `cumulative_s`) is on every line. One `target_probs` line per round (parallel arrays) plus one for the final post; fsync per line; T9 asserts exactly 2+3R lines per write. **Deviation:** the advisor asked T2 to compare after stripping timing and memory fields. On stubs, telemetry cannot advance the injected clocks (T4) and `check_memory` is stubbed, so T2 requires **full** identity plus identical clock and call counts. That is strictly stronger. The strip list moved to (h′2) as the statement of what may differ on hardware. Correction: the replacement covers the last **three** sentences of `:475`, because the advisor's text restates "counts against the nominal deadlines". |
| 7 | Advisor B2: "The LAW#5 inertness of the extra MPS forwards is asserted, not demonstrated" | §9.1 (h′3); brief §2G, §2B step 11, §4 T8 | Both (a) and (b). First attempt off; launch lines use `env -u C10Z_TELEMETRY`. `telemetry_mps_inertness_check()` is built in arms now, so arms bytes (bound in the benchmark identity) need not change later, together with a runner file. Stage 0 refuses telemetry on unless an INERT record matches the current driver bytes. **Additions:** a third pass, P2, as a control. Without it, MPS run-to-run nondeterminism cannot be told apart from a telemetry effect; that case gives NONDETERMINISTIC-BASELINE, and telemetry stays off. **Correction:** the "≤ 10 min" estimate is wrong. All A7 probe forwards are about 11,184–11,406 per pass (spec v2 test 2a), so three passes take about 17–85 GPU-min. |
| 8 | Advisor B3: "The brief gives Codex no legal test seam for the launch binding, and silently breaks existing tests" | brief §2B Seams, §2F, §4 Launch gates | ROOT-derived paths are evaluated at call time. `_bench_tree` copies the real identity files and builds the record with the real `ceilings()`/`validate_record()`/`write_record()`. Unreachable gates are tested by patching `ceilings` to synthetic values. A verified fixture list with line numbers is in §2F. **Disputed in part:** see D1 and D2 below. |
| 9 | Advisor B4: "The red step is self-contradictory under the signature change" | brief §2A (v3 `:113–124` quoted verbatim, including `if key not in self.origins`), §4 `_budget`, §3 step 3 | `_budget(start,c01,c2,c3,process,clock)`. **Deviation:** it uses the old signature when `inspect.signature(D.Budget)` lacks `stage01`, instead of catching `TypeError`, so a real `TypeError` in the new code cannot be masked. RED must be the behavioural assertion; TypeError, KeyError and AttributeError are excluded. Expected fixture-signature failures on today's code are listed separately. |

## Advisories and design items

| # | Reviewer item (quote) | Resolved in | How |
|---|---|---|---|
| 10 | Advisor A1: "Add `benchmark_sha256` to the go record … Hash and parse the same bytes" | §9.1 (b′2), (b′3) step 4; brief §2B | Adopted, with `benchmark_script_sha256` and `ceilings` added (Astra 3). |
| 11 | Advisor A2: "require `record["budget"]["ceilings"][k] == run["launch"][k]` … p1 and p2 ceilings to be equal" | §9.1 (e′); brief §2B Reader | Adopted, and extended per Astra 2. |
| 12 | Advisor A3: "Give the halt-code mapping explicitly" | §9.1 (b′3); brief §2B table | The advisor's mapping is adopted. New steps: identity, environment, `validate_record` and go-ceiling mismatches → V12; the stop and bounds gates are split (each BUDGET). Every gate has a unique detail substring for isolated tests. |
| 13 | Advisor A4: "The launch line at v3:245 lacks `C10Z_BENCHMARK_RECORD`" | §9.1 (j′); brief §6 item 9 | Corrected process-1 and stage-3 lines; telemetry is unset explicitly for the first attempt. v3 itself is not edited. |
| 14 | Advisor A5: telemetry precision (Exception not BaseException; which `post`; T7 spy; one logit-lens method + AST; `hidden_states[l+1]`) | §9.1 (h′5); brief §2D, §4 T5(e), T7, AST test, T6 | All adopted. Rounds use `post` at `arms:725`, plus the final `post` at `arms:743`. Lens call sites are after `arms:813` and `arms:669`. Mutants M27–M29. |
| 15 | Advisor A6: "The benchmark module's top level should import only the stdlib" | brief §2C, §4 Benchmark | Adopted, with a subprocess import test. |
| 16 | Advisor A7: "Run [B2(b)] before the first telemetry-on launch" | §9.1 (h′3); brief §2B step 11 | Enforced mechanically by the stage-0 gate. |
| 17 | Advisor answer A: "§9's closing 'no gate … changes' (prereg:477) slightly overstates" | §9.1 (i′) | `:478` is quoted and superseded, with "other than the declared `read:500` bound and provenance checks of (e′) and the (e) deadline scope". |
| 18 | Advisor answer B(1)/(2): another usable record passes; process 2 takes `stage01` from p1's run.json | §9.1 (b′2), (d′), (e′) | Closed by the go SHA binding, stage-3 re-verification and reader equality. |
| 19 | Astra A: "§9(a)–(g) correctly preserves the formula, bounds …" | — | No change needed. |
| 20 | Astra B: "prefer a bound launch input over editing reviewed code after benchmarking" | §9.1 (a′) | Recorded as D-C10z-c01input. |
| 21 | Astra C: "explicitly prescribe `hidden_states[l+1][:,-1,:]` … distinguishable-layer stub test, plus top-5 ID/text/probability assertions" | §9.1 (h′5); brief §2D, §4 T6 | Adopted (installed `modeling_qwen2.py:528–570` re-read: the input to each layer is appended at `:533–534`, and the final norm at `:566–570`). |
| 22 | Astra D: "both interior neighbours … isolate each gate" | brief §4 (preamble; Bounds and boundaries) | Interior neighbours are added to every threshold. Each HALT test asserts its unique detail with all other gates passing. |
| 23 | Astra D: "M7 therefore needs an injected derived-ceiling result" | brief §4 Launch gates | Synthetic `ceilings` patching, with consistent `derived` and go ceilings. |
| 24 | Astra D: literal instruction conflicts (precedence for `==C01`; approved helpers; "never `cd`"; `-I`/interpreter) | brief §1 Precedence 1–5, header | All five are listed explicitly. |
| 25 | Astra D: "`git status --short` alone cannot detect further changes … attribute concurrent C10V changes … restoration should execute in `finally`" | brief §0 Evidence, §5, §6 item 1 | SHA tables for the write list and the FROZEN set; listings of the frozen result dirs, with changes attributed to the live runs; restoration in `finally`. |
| 26 | Astra D: "T2 must exclude telemetry files … control nondeterministic identities … Test writer initialization, append, flush and fsync failures separately. Define how round-start markers coexist" | §9.1 (h′4), (h′5); brief §4 T2, T5(a)–(d), §2D table | Adopted. There is no separate round-start line: the round_end line after `round_guard` carries the measured `seconds`, and write_start is written before the clock starts at `arms:706`. |
| 27 | Astra E: "No additional operator budget authorization is needed" | — | Agreed. Bounds are unchanged. |

## Program items

| # | Item | Resolved in | How |
|---|---|---|---|
| 28 | D-C10z-c01input: C01 is a launch input from the benchmark record, checked at stage 0 against [7,200, 10,800] and 2·(C01+C2) ≤ 55,800, not hard-coded | §9.1 (a′), (b′3) step 8; brief §2B, §1 Precedence 2 | No C01 literal anywhere. `Budget` enforces the bounds. Stage 0 enforces bounds and total separately. |
| 29 | C10W P2 freeze of the 15 hashed sources (+ `results/c10w_oracle/`) and the C10V freeze | brief §0 FROZEN bullets, Evidence, §6 item 1 | All paths are listed (existence verified). They may be read and copied into temp, and SHA before = after is required. Note: c10e, hparams, `engine_fingerprint.py` and `memit_main.py` are in the benchmark identity set; they are only hashed. |
| 30 | No GPU job while P2 runs; model-free tests only | brief §0 No GPU, header (`nice -n 19`, serial) | The benchmark, inertness check, ASTRA stages and c10v/c10w scripts are not run; no `mps` tensor is created. `nice -n 19` is added to reduce CPU contention with P2's timed run. |

## Disputed or corrected (not silently dropped)

- **D1. Advisor B3 "with no assertion changed except the ceiling numbers": not achievable.**
  - `selftest:1086–1089` (`noceil`) uses an inconsistent fixture: pass stage3 is 24,000 (`:1170`), the launch has stage3 None, and the test expects HALTED-BUDGET.
  - Under A2 (which the advisor also asks for), `read_directory` rejects that mismatch, so `stage_call(3)` raises HALTED-V12 at `arms:1482–1483` before `arms:1484`.
  - Even with a consistent fixture, stage3 None makes `next_stage` None (`read:574–575`), which also gives V12 at `:1482`. So `arms:1484` cannot be reached through any consistent directory, today included.
  - Brief §2F allows exactly this one assertion change, to `"HALTED-V12: stage3 requires"`, and asks for the dead check to be reported, not deleted.
- **D2. Advisor B3's fixture list is partly off.**
  - `:1069` does not break: `stage_call(2)` reads only `launch["stage2"]` (`arms:1489–1497`).
  - The list misses:
    - the `:1627` Budget lambda;
    - the history-ceiling fixture (`:224`, `seal_schedule` `:266–274`, re-seal after `:1662`), which Astra 2's history check requires;
    - `_go_record` (`:1175–1178`);
    - the `_review_stage_calls_with_go` ROOT/env seam (`:1181–1188`);
    - the launch dicts at `:1237`, `:1249` and `:1624`.

  The stage-0 tests that actually reach the launch are `:1062`, `:1362` and `:1546`. The rest of `:1310–1369`/`:1500–1550` refuse earlier, because the go record is checked first. All of this is in brief §2F.
- **D3. Advisor B2(b) time estimate**, corrected above (row 7).
- **D4. Advisor B1 T2 mechanism and B4(i) mechanism.** Replaced by stronger equivalents (rows 6 and 9).
- **D5. Astra 3, resident re-hash and ledger match.** Partial, with reasons (row 3).

## Needs the program lead's judgment

1. **Inertness-check scope and cost (row 7).** It takes all A7 probe forwards × 3 passes ≈ 17–85 GPU-min, after P2 frees the GPU, and only if telemetry is wanted. A subset (for example, prefix items for one subject) would cut it about sixfold, but the advisor asked for all tokens. My recommendation: keep all tokens, because the first attempt is telemetry-off regardless.
2. **Identity-drift re-runs (§9.1 (b′4)).** I ruled that a benchmark re-run forced only by a later code or environment change is not a §9(c) refusal and does not use up the one re-run. The operator's D-C10z-budget text speaks only of "a benchmark refused twice". If the lead reads it more strictly, every drift re-run needs operator sign-off.
3. **Telemetry-on attempts versus D-C10r-rulings-11.** The ruling's "must not change any computed result … off by default, or proven inert" is met by off-by-default. B1 shows that a telemetry-on attempt can change a timing-gated label even when numerically inert. The §9.1 description rule prevents misreading, but the lead may prefer to forbid telemetry-on for any attempt whose result would be promoted.
4. **Build size.** v2 adds the inertness check, its runner, the identity contract and about 15 mutants. It now needs prereg §9.1 appended (new SHA pin) before Codex starts. The frozen-P2 window means the build must be CPU-only and can only be validated by tests, not by the benchmark, until P2 finishes.

## Round 2

Reviews: Astra `/private/tmp/claude-501/reviews/c10z_s91_recheck_astra.md` (FIX-FIRST, blocking 1–4); advisor `/private/tmp/claude-501/reviews/c10z_s91_recheck_advisor.md` (PROCEED-WITH-CHANGES, N1–N2, A-1..A-10). Both accept D1–D5; B1–B4 and Astra 1–5 resolved subject to the items below. D = §9.1 draft, B = brief v2.

### BLOCKING

| # | Item | Resolved in | How |
|---|---|---|---|
| R1 | Astra 1: C01 "no numbers in test code" contradicts `C01_FIX` and the boundary fixtures | D (a′) first sentence; B §1 Precedence 2 last sentence | Both replaced with Astra's exact text (production code takes C01 from validated launch provenance; contractual bounds and numeric fixtures permitted). Round-1 row 28's "No C01 literal anywhere" is read with this scope. |
| R2 | Astra 2: successful `stage_call(3)` fixture (selftest:1078–1080) cannot pass the new binding check | B §2F, new last bullet | Astra's "Successful stage-3 fixture" text appended verbatim. |
| R3 | Astra 3: T5 "letting the run complete" vs T5e propagation; `assertRaisesRegex` vs reader HALT dicts | B §4 T5 lead line; B §4 preamble first two sentences | Both replaced with Astra's exact text; the T5 (a)–(e) case list is kept. |
| R4 | Astra 4: live INERT claim exceeds the (h′3) evidence; admission does not check the record's internal consistency | D (h′2) last bullet; B §2G stage-0 gate bullet | Both replaced with Astra's exact text; the closing quote of the (h′2) superseding quotation is kept. |
| R5 | Advisor N1: any Python process during P2 makes `tools/c10w_p2_gate.py` refuse a stage and stops P2 | B header (old `nice -n 19` line); B §0 "No GPU job and no model." first line; B §3 step 1 | Advisor's replacement text adopted, with a P3 clause added: no Python of any kind while a C10W P2, a later C10W P3 or a C10V stage can be dispatched; start only after `COORDINATOR_EXIT=` appears in `results/c10w_oracle_logs/p2-coordinator.log` and no other GPU coordinator or stage is live or pending. The `nice -n 19` instruction is removed (header and step 1). Round-1 row 30 and lead ruling 4 are restated: the build starts after P2's COORDINATOR_EXIT (and with no P3/C10V stage live or pending) and is still model-free and GPU-free. |
| R6 | Advisor N2: drift-rerun path does not exclude prior STOP/REFUSED records or count a refused drift rerun | D (b′4), right after "the record becomes unusable." | Advisor's exact text inserted; the D-C10z-driftcap sentence is unchanged. |

### Non-blocking

| # | Item | Disposition |
|---|---|---|
| R7 | Astra D5: row 3's elapsed-time claim is not guaranteed by `Popen` | Adopted: round-1 row 3 now rests on the trusted handoff and unchanged sources. |
| R8 | Astra: frozen-hash scope | Adopted: B §0 Evidence and §6 item 1 hash FROZEN sources/inputs only; result-directory listing changes are reported separately as observed, not attributed. |
| R9 | Astra: concurrency test + advisor A-4 | Adopted: B §4 (ix) uses an instrumented lock that signals T's acquisition attempt before the blocked-T assertion; E and T are daemon threads; release and joins run in `finally`/`addCleanup`. |
| R10 | A-2: lens positions | Adopted: D (h′3) Method sentence corrected with the advisor's text. |
| R11 | A-3: warm-up and GPU-time recording | Adopted: uncompared warm-up before P1 in D (h′3) and B §2G (not counted in `probe_forwards`); D (h′3) Cost records GPU time in the D-C10z-budget or D-C10r-rulings-11 row, outside the 55,800 s attempt bound. |
| R12 | A-5: `benchmark_module()` seam | Adopted: B §2B Seams, Launch gates and the environment-drift test patch `D.benchmark_module`. |
| R13 | A-6: stage-3 launch line | Adopted: D (j′) stage-3 line written out in full (same variables as process 1, per v3 §G `:247`'s "same `env`"). |
| R14 | A-1: reader checks manifest driver/reader SHAs against launch sources | Declined: not an error correction; both reviewers accept D5 within the controlled workflow, and it adds a gate to append-only text. |
| R15 | A-7: T8 asserts `process2/` absent | Declined: a test strengthening, not an error; Codex may add it under §4's "derive more". |
| R16 | A-8: pristine lens is A7-only | Declined: visualization only; no gate or claim depends on it. |
| R17 | A-9: D-C10z-c01input and D-C10z-driftcap rows missing from runbook §5 | Not in these files: program close-out action before §9.1 is appended. |
| R18 | A-10: a post-benchmark code change uses up the drift rerun | No text change: program sequencing (benchmark only after the final code review). |
