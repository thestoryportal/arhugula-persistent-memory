Verdict: FIX-FIRST

# D-C10z-astra — implementation review of build 6ec1da6 (advisor, Claude Opus 5.5)

**Scope.** Independent review of `experiments/track_c/c10z_astra_{arms,read,selftest}.py` and `tools/run_c10z_stage.sh` (commit 6ec1da6; SHA-256 `a652306f…`, `97a46b56…`, `96dd8e99…`, `64edcae5…`, re-hashed 2026-10-07 and equal to the builder's table) against `docs/C10Z_ASTRA_PREREG.md` FROZEN v2.2 (`38f8b68c…`, unchanged). Nothing loaded a model, tokenizer or MPS. All runs were CPU selftests in scratch mirrors under `/Users/robertrhu/.claude/jobs/8ac4cacf/tmp/c10z_mut/`. No build, spec or tracked file was edited. Line citations are `arms` = `c10z_astra_arms.py`, `read` = `c10z_astra_read.py`, `prereg` = the frozen spec.

## Single most important fix

**Add the §6 go gate before anything launches.** `stage_call(0)` (arms:1436–1452) and `tools/run_c10z_stage.sh:1–17` start the resident model-loading process with no check that the operator's go (decisions 0–2; prereg :3 "running needs the operator's go (§6, decisions 0–2)", :341–344) exists. Today, `bash tools/run_c10z_stage.sh 0` on a fresh `results/c10z_astra/` loads Qwen on MPS while another GPU job may be running. Fix: in `stage_call(0)`, before `subprocess.Popen` (arms:1448), require a go record and refuse otherwise, for example a `C10Z_GO_RECORD` JSON naming the runbook §5 Decision-IDs for decisions 0, 1 and 2 with the operator's yes. Validate it, copy it into `run.json["launch"]`, and bind its SHA-256 into `H_in` (`input_parts`, arms:1151). Add the test `test_B1_stage0_refuses_without_recorded_go_decision` (below). It currently fails: `launched == ['p1']`.

## BLOCKING

**B1 — No recorded go decision gates stage 0–1.** (arms:1436–1452; run_c10z_stage.sh:3–14; grep for `decision|approv|operator|GO` in all three build files finds only `R.classify_candidate`'s `decision` variable, arms:1242/1248.)
- *Scenario:* fresh OUT_DIR with no go recorded → `run_c10z_stage.sh 0` → `stage_call(0)` passes `entry_preflight` and the fresh-dir check, then `Popen`s the resident. The resident imports `c10e_bandknob` and loads the model at arms:342. The spec gates this on decisions 0–2 (prereg :3, :341–344), and the brief requires refusal.
- *Fix:* the single most important fix above. Stage 2 and 3 are already refused without their launch ceilings (arms:108, :1458, :1466), which covers decision 2's expansion budgets. Optionally, the go record can also carry a one-GPU-job assertion (D-C10r-rulings-4 (1)).
- *Evidence:* `proposed/blocking_demos.py::test_B1` FAILS on the unmodified build (`['p1'] != []`).

**B2 — Refusals and halts overwrite completed pass records; a stray call turns a finished verdict into a halt.** `diagnostic()` (arms:1342–1363) always rewrites `pass_p{n}.json` (arms:1357–1358, `replace=passpath.exists()`) and marks `run.json` halted (arms:1359–1361). Every `stage_call` refusal reaches it through `main()` (arms:1497–1499), and so do the watchdog (arms:1392–1398, called with `session=None`, so even the recipes are dropped) and the resident's exception path (arms:1427–1432).
- *Scenario 1 (reachable through the launcher):* a K1 kill completes cleanly (`run.json` closed, `pass_p1.json` = NULL-STAGE1, a scientific verdict). The operator then runs `bash tools/run_c10z_stage.sh 2`. `stage_2.log` does not exist, so the shell's log guard (run_c10z_stage.sh:13) does not stop it. `stage_call(2)` refuses with "closed stage call" (arms:1463) → `diagnostic()` replaces `pass_p1.json` with a 300-byte HALTED record → `read_directory` now returns **HALTED-V12**. The same happens with `run_c10z_stage.sh 3` after any non-K2 stage-2 result.
- *Scenario 2:* a stage-2 or stage-3 elapsed deadline fires in the watchdog → `diagnostic(out,code,…)` with no session → the complete stage-1 record, its manifest binding and all recipes are replaced by a stub. Prereg :267 requires "retain completed observations as non-binding", and :123/:323 require "the runs made are kept as data".
- *Scenario 3 (direct `python … arms.py 0`, bypassing the shell's log guard):* the "attempt needs fresh OUT_DIR" refusal (arms:1440–1441) overwrites the very `pass_p1.json` it exists to protect (prereg :137 "refuses existing manifest/pass files").
- *Fix:*
  1. A refusal raised by `stage_call` before it changes the attempt's state must not touch the attempt: print and exit 2, with no `diagnostic(out, …)`.
  2. `diagnostic()` must never replace an existing `pass_p{n}.json`. Write the halt to `halt_p{n}.json` and the architecture_profile file, and keep the completed record beside it.
  3. The watchdog must embed the last published record, not a stub.
  4. `read_directory` should then read the halt file to set the label (HALT still governs the verdict, per prereg :267), while the completed observations survive.
- *Evidence:* `blocking_demos.py::test_B2` FAILS (`'HALTED-V12' != 'NULL-STAGE1'` after one refused stage-2 call).

**B3 — A clean K1 survivor without a stage-2 ceiling has no terminal path.** It either holds the GPU indefinitely or ends HALTED-BUDGET with its record destroyed. `classify_candidate` sets `next_stage=2` for every clean stage-1 survivor whatever the launch ceilings are (read:573). `stage_omissions` records the reason `ABSENT-CEILING` (read:585), yet the stage-1 record still schedules stage 2. After stage 1 the resident calls `complete01()` (arms:1259), so no deadline stays active (`Budget.deadline()` returns `None` with an empty active set, arms:95–97). It then loops waiting for a stage-2 request (arms:1409–1416) that `stage_call(2)` must refuse for the absent ceiling (arms:1466).
- *Scenario:* the builder's own handoff launches stage 0 with no ceilings (`results/c10z_astra_codex_build.md:261`). Stage 1 yields n = 26, a = 12, FIT, gates clean. The reading is PARTIAL, next_stage 2, and the resident stays resident with the model loaded and no deadline. If the operator then asks for stage 2, it is refused with HALTED-BUDGET → `diagnostic()` overwrites the 7.7 MB stage-1 pass record (B2) → final verdict HALTED-BUDGET. Prereg :196 says "an absent ceiling refuses that expansion", which is a refused expansion, not a refused or erased stage-1 result. Prereg :265 says "Otherwise close stage 1 … with -STAGE1, recording G0 and attribution as not run".
- *Fix:* pass the launch ceilings into the classifier. When stage == 1, the survivor is clean and `ceilings["stage2"] is None`, set `next_stage=None`, add `-STAGE1`, and record G0/Z-band `NOT-RUN: ABSENT-CEILING`. The resident then closes as on a K1 stop (arms:1419). Apply the same at stage 2 for an absent stage-3 ceiling: `-SINGLE-PROCESS` is already attached and only `next_stage` must become `None`. The exact marker for "clean survivor, expansion unbudgeted" is the operator's call: `-STAGE1` is the conservative reading of :265 and does not claim G0 passed (:266).
- *Evidence:* `blocking_demos.py::test_B3` FAILS (the stage-1 pass record is replaced by a HALTED stub). The same test asserts the paradox directly: `read_process` returns `("PARTIAL", 2, "ABSENT-CEILING")`.

**B4 — The runtime driver's gates are untested: 28 of 71 single-point mutants survive the builder's 50 tests.** The selftest never constructs `Session`: the build report says so at `results/c10z_astra_codex_build.md:17`, and `grep -c Session experiments/track_c/c10z_astra_selftest.py` returns 0. So the stage-0 LAW#3 ordering, Z5 footprint, Z6 restore/verify, the standing-LAW#5 delegation, the 10-round cap, the in-run V13 round halt, the pre-start projection refusal, every `stage_call` refusal and 12 reader re-checks can be deleted or flipped without a red test. Each survivor below changes a gate, halt or label outcome, for example:
- A09: a LAW#3 miss no longer raises, and stage 0 continues into templates and probes.
- A19: a write outside the selected columns passes Z5.
- A23: `run_law5` runs ASTRA instead of the engine path.
- A25: 11 rounds.
- A27: process 2 launches without a clean K2.
- R26: τ_head up to 0.5 accepted.
- R29: the recorded Z5 footprint is not re-checked.
- R37: NOT-REPLICATED is never attached.

*Fix:* adopt the 10 proposed tests (`proposed/review_additions.py`, already merged into `proposed/c10z_astra_selftest.py`). They pass on the unmodified build (60/60) and kill 27 of the 28 survivors (table below). The one remaining survivor, A32, is outcome-neutral (ADVISORY 10).

## ADVISORY

1. **Row 22 vs Z2 (prereg :149, :208, :311).** The builder's objection is correct. A record with 24 positive identity-view facts and evaluator `canon_full_n = 0` fails the post-write Z2 (read:551–552) on any non-empty checked population, and an all-ambiguous population is not a pass. So the full reader must return HALTED-V5 (selftest `test_worked22_validity_precedes_conditional_label`), while the literal row 22 label survives only in the conditional classifier. This is a prereg inconsistency. Record it as an erratum note beside the frozen file; do not change code.
2. **The stage-0 projection will very likely refuse before the candidate (arms:32–33, :847).**
   - The allowances sum to 5,340 s of the 5,400 s ceiling, and `recipe_A` alone is budgeted at the whole 34-min anchor (2,040 s).
   - The projection at arms:847 adds ≥ 3,180 s (D 300 + G 120 + validation ≥ 1,380 + rounds 1,200 + serialization 180) to the elapsed time after recipe A, pristine probes, Z0, the evaluation signature and three deferred baseline evaluations. It therefore passes only if everything up to that point takes ≤ 2,220 s.
   - The A7 F1 population alone is 6 views × Σ(T_i−1) × 6 subjects = 1,728–4,320 greedy probes, each re-run without a KV cache. It is run twice in stage 0 (pristine and deferred A).
   - This is spec-compliant, because a refusal is HALTED-BUDGET (prereg :196, :225). It is a near-certain waste of a GPU slot, though: measure recipe A and one F1 probe pass on the Mac (or re-scope the probe population through a prereg amendment) before granting the go.
3. **The 7,920 s `future_stage2_s` allowance is unrecorded (arms:90, :118).** Process 2's first projection needs a stage-3 ceiling ≥ 5,340 + 7,920 s plus elapsed time. This constant appears in no `components_s` entry and in no record of allowances. Put it in `ALLOWANCES` so that the operator choosing stage-3 ceilings sees it.
4. **W2 measures more than the write (arms:687, :695).** `wall_seconds` runs from write start to `restore_hook`, so it includes `eval_arm`, all F0/F1/subject-free probes and the held-out reads. That is conservative, since -EXCEEDS-TTL fires earlier, but it is not the "Z write wall-clock" of prereg :274. Gate on compile time (write start → post-loop observation and serialization), and report the end-to-end time separately as :200 asks.
5. **The stage-01 clock starts in the child, not before the parent's launch (arms:1368 vs :1438).** The parent's `start` is not passed to the resident in stage 0, as it is for stage 3 (arms:1462). The interpreter start-up and import of the child are uncounted. This is sub-second to seconds. Pass the parent's origin through `C10Z_LAUNCH`.
6. **A relative `C10Z_OUT_DIR` splits the records.** The harness `chdir`s to the engine root on import (c10e_bandknob.py:8). After that, `Session` writes (`pristine_hash.json` onward) resolve under `memit_dry_run/memit/<OUT_DIR>`, while `run.json` stays at the original relative path. Resolve OUT_DIR to an absolute path in `main()` (arms:1494) and in the shell.
7. **Stage 2 is not "automatic" (prereg :131).** It needs a second external call, and between the calls the resident holds the model with no active deadline (arms:95–97, :1259). This is intended by the build brief, but record it as a deviation and add an idle limit.
8. **The stage-2 merge drops stage-1 provenance (arms:1266–1270).** The merged `Z` recipe keeps only the stage-2 `law5_gate` and `delta_norms` (A7's are lost from the final record). V2 was enforced at the time (arms:651), but the final record no longer shows Z's stage-1 standing-gate readout.
9. **A comment contradicts the code (arms:674).** It says "Pristine held-out reads are obtained only after the solve has ended", but stage 0 reads pristine held-out leads before any candidate write (arms:814–819). They never enter the solve, so prereg :166 is not violated. Fix the comment.
10. **Outcome-neutral survivors, each backstopped:**
    - A32: the driver's Z0 σ > 0.125 halt is re-checked by `Gates.instruments → check_instruments` (read:196) before any candidate.
    - A26: the in-run round halt is re-checked post hoc by the reader (read:537). The proposed test still pins the in-run halt (prereg :198 places it in the run).
    - A31: a Z-band capacity taken from the wrong arm is caught by read:544–546 as HALTED-V12, not a wrong label. The proposed test pins it.

## What was checked and found correct (each cites its implementation line and the killing test)

| Spec item | Implementation | Exercised by (mutant killed) |
|---|---|---|
| LAW#3 envelope inclusive [5,18]/[5,10]/[42,59], A1/A2 ≥ 68 (prereg :123, :217) | read:183–189; driver gate arms:131, :797–802 | R01, R02 → `test_law3_both_sides`; stage-0 ordering → proposed `test_review_stage0…` (A09, A10) |
| FIT `20m ≥ 19M`, ≥ 23, ≥ 23 (prereg :234) | read:74–79, :82–86 | R03, R04 |
| Table T rows and rule U (prereg :249–261) | read:314–317, :571 | R05, R06, R14 |
| G1–G5, G7 per cell, G2 per view (prereg :239–245) | read:296–311 | R07–R10 |
| W1 > 0.55, SUBJECT-FREE > A+1, W2 > 3600 (prereg :272–274) | read:323–328, :570 | R11–R13 |
| K1/K2 clean-survivor rules (prereg :265–266) | read:572–575 | R15, R16 |
| Attribution order and boundaries (prereg :284) | read:332–342 | R17–R19 |
| R1 ≤ 1e-3, R2 ≤ 2, R3 ≤ 3, aggregation (prereg :277–280) | read:150–180, :614–637 | R21, R22; R20/R37 → proposed |
| Z2 zero-checked is not a pass (prereg :149) | read:242–245 | R24; ambiguity boundary R23 → proposed |
| V5 requires Z3; V7 ≥ 0.80; stage-1 round ≤ 120 (prereg :198, :218, :158) | read:193–194, :238, :537 | R25, R32, R33 |
| Memory ≤ 40/32 GiB; round ≤ 120; projection ≤ ceiling; deadline; 5,400 s (prereg :190, :196–198) | arms:73–79, :82–126 | A01–A06 |
| Gates: no observation/candidate before LAW#3/instruments | arms:129–141 | A07, A08 |
| SemCon 9 layers, tie order, n_L, band split, cap 2,200 (prereg :77, :112) | arms:249–261 | A11–A15 |
| Joint solve (nonsymmetric A, ridge 1e-3 × mean diagonal, float64 CPU), competitor excludes target, fp32-add/fp16-store (prereg :75–80) | arms:194–218, :264–272 | A16–A18 |
| Write-once JSON; inherited knobs refused | arms:43–56, :65–70 | A33, A34 |

**Forward-only and column-only write (the brief's proof request).**
- *No gradient anywhere:* `grep -n -i "backward\|optim\|requires_grad\|enable_grad\|\.grad"` on arms finds nothing. Every model call the driver makes is under `torch.no_grad()` (arms:483, :553, :593, :864/:868, :889, :957, :1129).
- *Writes:* the only weight writes are `write_columns` (arms:264–272), which assigns `weight[:,columns]` from one fp32 add and one fp16 store; `restore` (arms:396–399); and the reinstatement of saved snapshots (arms:685, :834).
- *Byte checks:* after every write, `footprint` (arms:535–548) checks two things. First, the columns that differ from PRISTINE in all 36 layers must be ⊆ S. Second, every non-`down_proj` parameter must keep its import-time SHA-256.
- *Tests:* the builder's suite did not test footprint (A19, A20 survived). `test_review_Z5_footprint…` now proves both halts on CPU tensors, and `test_review_write_round_cap_columns_and_capacity` shows a 10-round write leaves the unselected columns byte-identical.

**Engine called unmodified (LAW#4 read, 2026-10-07).**
- *Seams match the build's use of them:*
  - `memit_main.py:21` (`CONTEXT_TEMPLATES_CACHE`), `:100` (templates fetched before any weight change), `:191–194` (float64 only on CPU), `:240–284` (`get_cov`; `t100` because `max_position_embeddings > 8192`, `:267`), `:304–323` (identity + 5 sampled templates).
  - `rome/layer_stats.py:102–121` (cache name `…_float32_mom2_t100_100000.npz`, as used at arms:1141–1142).
  - `util/nethook.py:117–146` (`TraceDict(module, layers, retain_output, retain_input, clone, detach, …)`, as called at arms:481).
  - Harness `c10e_bandknob.py:181` (`my_edit(hp, requests, P, cache_c)` = wrapper signature, arms:698), `:358–400` (`eval_arm`, delegated unchanged at arms:411), `:403–446` (`_LAW5_DEFAULT_CTX`, `run_law5`), `:458–509` (`run_recipe`: hooks after evaluation, :494–495; band-only restore, :473/:506 — the restore trap the driver covers).
  - transformers 4.51.0 `modeling_qwen2.py:58–59` (down_proj input = act(gate)·up), `:220–225` (RMSNorm cast order), `:276–279` (`post_attention_layernorm` input = pre-MLP residual, used by Z7 at arms:480, :506).
- *Rebinding only:* the driver rebinds module globals (`H.my_edit`, `H.eval_arm`, `H.axes_post`, `H.ARMS`, `H.ARM_HOOKS`, `M.CONTEXT_TEMPLATES_CACHE`) and writes no engine file.
- *Hashes:* V1 hashes the engine, harness, driver, reader and prereg at start and end (arms:296–301, :1234–1236). The engine `memit_main.py` hash is `d941a9fb…` and the harness hash `1f6be581…`, both unchanged.

## Evidence

**Selftest (unmodified build, run by this reviewer).** `.venv/bin/python -B experiments/track_c/c10z_astra_selftest.py` → `Ran 50 tests in 25.591s`, `OK`, `C10Z_ASTRA_SELFTEST_PASS tests=50`, exit 0. Log: `c10z_mut/selftest_baseline.log`.

**Mutation run.** Harness: `c10z_mut/mutate.py`. It applies exact-string single substitutions and asserts that each target occurs exactly once. All 71 targets were checked once before running (`mutate.py --check`), so no mutant was a no-op. The full selftest ran against each mutant in a copied mirror root (`c10z_mut/root`). BASELINE passed before and after the run. Logs: `run_pristine_suite.log` (builder's 50 tests) and `run_proposed_suite.log` (60 tests, survivors only).

71 mutants: **43 killed, 28 survived** the builder's suite; the proposed suite kills **27 of the 28**. The remaining survivor, A32, is outcome-neutral.

| mutant | target (file:line) | builder's 50 tests | proposed 60 tests |
|---|---|---|---|
| R01_law3_lower_exclusive | read:187 | killed by test_law3_both_sides | (killed already) |
| R02_law3_A1A2_67 | read:189 | killed by test_law3_both_sides | (killed already) |
| R03_fit_strict_95 | read:79 | killed by test_band_boundaries_ordered, test_fit_count_boundaries, test_k1_k2_omissions_and_replication, test_law3_both_sides, test_side_gate_boundaries_and_populations, test_ttl_every_Z_arm_and_incomplete_actual_repro_failure, test_worked_01, test_worked_03, test_worked_04, test_worked_05, test_worked_06, test_worked_07, test_worked_08, test_worked_11, test_worked_12, test_worked_15, test_worked_16, test_worked_17, test_worked_19, test_worked_20, test_worked_23 | (killed already) |
| R04_fit_positive_22 | read:79 | killed by test_fit_count_boundaries, test_worked_09 | (killed already) |
| R05_tableT_gain_8 | read:315 | killed by test_table_T_exhaustive_and_integer_boundaries, test_worked_03, test_worked_04 | (killed already) |
| R06_tableT_lead_30 | read:317 | killed by test_table_T_exhaustive_and_integer_boundaries | (killed already) |
| R07_G1_plus2 | read:305 | killed by test_side_gate_boundaries_and_populations | (killed already) |
| R08_G2_any_view | read:306 | killed by test_side_gate_boundaries_and_populations | (killed already) |
| R09_G7_plus2 | read:310 | killed by test_side_gate_boundaries_and_populations, test_worked_06, test_worked_19 | (killed already) |
| R10_G4_28 | read:308 | killed by test_side_gate_boundaries_and_populations | (killed already) |
| R11_W1_ge | read:324 | killed by test_w1_even_median_w2_subject_free, test_worked_23 | (killed already) |
| R12_subject_free_ge | read:327 | killed by test_w1_even_median_w2_subject_free | (killed already) |
| R13_ttl_ge | read:328 | killed by test_w1_even_median_w2_subject_free | (killed already) |
| R14_ruleU_dropped | read:571 | killed by test_worked_02, test_worked_10 | (killed already) |
| R15_K1_clean_ignores_qualifiers | read:572 | killed by test_ttl_every_Z_arm_and_incomplete_actual_repro_failure, test_worked_09, test_worked_11, test_worked_12, test_worked_22 | (killed already) |
| R16_K2_next_stage_any | read:573 | killed by test_ttl_every_Z_arm_and_incomplete_actual_repro_failure | (killed already) |
| R17_attr_capacity_ge | read:335 | killed by test_band_boundaries_ordered | (killed already) |
| R18_attr_retains_strict | read:340 | killed by test_band_boundaries_ordered | (killed already) |
| R19_attr_locality_dropped | read:336 | killed by test_worked_19 | (killed already) |
| R20_aggregate_clean_ignores_q | read:628 | **SURVIVED** | killed by test_review_cross_process_replication_needs_clean_pair |
| R21_R1_threshold_1e-2 | read:615 | killed by test_k1_k2_omissions_and_replication | (killed already) |
| R22_R2_le3 | read:627 | killed by test_k1_k2_omissions_and_replication | (killed already) |
| R23_z2_ambiguity_strict | read:243 | **SURVIVED** | killed by test_review_reader_instrument_ceilings_audits_and_capacity |
| R24_z2_empty_passes | read:244 | killed by test_z2_ambiguous_and_all_validity_gates | (killed already) |
| R25_V5_Z3_dropped | read:193 | killed by test_worked_14 | (killed already) |
| R26_Z7_tau_ceiling_05 | read:201 | **SURVIVED** | killed by test_review_reader_instrument_ceilings_audits_and_capacity |
| R27_Z0_sigma_ceiling_025 | read:196 | **SURVIVED** | killed by test_review_reader_instrument_ceilings_audits_and_capacity |
| R28_Z4_loop_tol_1e-6 | read:223 | **SURVIVED** | killed by test_review_reader_instrument_ceilings_audits_and_capacity |
| R29_Z5_footprint_unchecked | read:233 | **SURVIVED** | killed by test_review_reader_instrument_ceilings_audits_and_capacity |
| R30_V9_override_hits_unchecked | read:478 | **SURVIVED** | killed by test_review_reader_instrument_ceilings_audits_and_capacity |
| R31_V2_expr_le | read:467 | **SURVIVED** | killed by test_review_reader_instrument_ceilings_audits_and_capacity |
| R32_V7_strict | read:238 | killed by test_z2_ambiguous_and_all_validity_gates | (killed already) |
| R33_stage1_round_121 | read:537 | killed by test_completed_stage2_keeps_stage1_round_ceiling, test_worked_24 | (killed already) |
| R34_SemCon_capacity_unchecked | read:542 | **SURVIVED** | killed by test_review_reader_instrument_ceilings_audits_and_capacity |
| R35_band_distribution_unchecked | read:545 | **SURVIVED** | killed by test_review_reader_instrument_ceilings_audits_and_capacity |
| R36_p2_origin_unchecked | read:503 | **SURVIVED** | killed by test_review_reader_instrument_ceilings_audits_and_capacity |
| R37_not_replicated_dropped | read:632 | **SURVIVED** | killed by test_review_cross_process_replication_needs_clean_pair |
| A01_memory_strict | arms:74 | killed by test_budget_origins_prestart_deadlines_round_memory | (killed already) |
| A02_round_strict | arms:79 | killed by test_budget_origins_prestart_deadlines_round_memory | (killed already) |
| A03_projection_strict | arms:124 | killed by test_budget_origins_prestart_deadlines_round_memory | (killed already) |
| A04_projection_dropped | arms:124 | killed by test_budget_origins_prestart_deadlines_round_memory | (killed already) |
| A05_deadline_check_dropped | arms:104 | killed by test_budget_origins_prestart_deadlines_round_memory | (killed already) |
| A06_stage01_ceiling_7200 | arms:88 | killed by test_budget_origins_prestart_deadlines_round_memory | (killed already) |
| A07_gate_observe_no_law3 | arms:133 | killed by test_ordering_and_stage_transport | (killed already) |
| A08_gate_candidate_no_ready | arms:140 | killed by test_ordering_and_stage_transport | (killed already) |
| A09_stage0_law3_halt_swallowed | arms:801 | **SURVIVED** | killed by test_review_stage0_law3_gate_precedes_all_new_work |
| A10_stage0_probes_before_law3 | arms:797 | **SURVIVED** | killed by test_review_stage0_law3_gate_precedes_all_new_work |
| A11_select_10_layers | arms:256 | killed by test_cpu_null_weight_margin_fp16_selection | (killed already) |
| A12_select_layer_tie_desc | arms:256 | killed by test_cpu_null_weight_margin_fp16_selection | (killed already) |
| A13_select_neuron_widened | arms:261 | killed by test_cpu_null_weight_margin_fp16_selection | (killed already) |
| A14_band_remainder_le | arms:251 | killed by test_band_boundaries_ordered | (killed already) |
| A15_band_uncapped | arms:250 | killed by test_band_boundaries_ordered | (killed already) |
| A16_ridge_1e-2 | arms:202 | killed by test_cpu_joint_algebra_independent_reference, test_known_answer_scalar_and_native_fp16_reference | (killed already) |
| A17_competitor_not_excluded | arms:216 | killed by test_cpu_null_weight_margin_fp16_selection | (killed already) |
| A18_write_double_rounding | arms:269 | killed by test_known_answer_scalar_and_native_fp16_reference | (killed already) |
| A19_footprint_column_check_dropped | arms:540 | **SURVIVED** | killed by test_review_Z5_footprint_rejects_any_write_outside_selected_columns |
| A20_footprint_other_params_dropped | arms:544 | **SURVIVED** | killed by test_review_Z5_footprint_rejects_any_write_outside_selected_columns |
| A21_verify_restore_weakened | arms:403 | **SURVIVED** | killed by test_review_Z6_restore_covers_all_36_and_verify_detects_drift |
| A22_restore_skips_layer35 | arms:399 | **SURVIVED** | killed by test_review_Z6_restore_covers_all_36_and_verify_detects_drift |
| A23_wrapper_law5_runs_astra | arms:699 | **SURVIVED** | killed by test_review_wrapper_delegates_under_standing_law5 |
| A24_write_prestart_projection_dropped | arms:708 | **SURVIVED** | killed by test_review_write_prestart_projection_refuses_before_observation |
| A25_round_cap_11 | arms:713 | **SURVIVED** | killed by test_review_write_round_cap_columns_and_capacity |
| A26_stage1_round_guard_dropped | arms:740 | **SURVIVED** | killed by test_review_stage1_round_over_120s_halts_in_run |
| A27_stage3_K2_check_dropped | arms:1456 | **SURVIVED** | killed by test_review_stage_call_refusals |
| A28_stage3_ceiling_check_dropped | arms:1458 | **SURVIVED** | killed by test_review_stage_call_refusals |
| A29_stage0_fresh_outdir_dropped | arms:1440 | **SURVIVED** | killed by test_review_stage_call_refusals |
| A30_stage2_K1_survivor_check_dropped | arms:1468 | **SURVIVED** | killed by test_review_stage_call_refusals |
| A31_Z_capacity_from_any_arm | arms:754 | **SURVIVED** | killed by test_review_write_round_cap_columns_and_capacity |
| A32_z0_sigma_halt_dropped | arms:876 | **SURVIVED** | SURVIVED (outcome-neutral, see ADVISORY 10) |
| A33_write_json_overwrite_allowed | arms:50 | killed by test_json_real_writer_and_frozen_sources | (killed already) |
| A34_inherited_knob_unchecked | arms:66 | killed by test_ordering_and_stage_transport | (killed already) |

**Proposed tests.** `c10z_mut/proposed/c10z_astra_selftest.py` = the builder's selftest plus `proposed/review_additions.py` (10 tests). On the unmodified build: `Ran 60 tests`, `C10Z_ASTRA_SELFTEST_PASS tests=60`, exit 0 (`proposed/proposed_on_pristine.log`). The tests use `Session.__new__` with stubbed collaborators and tiny CPU tensors, and never import the harness, transformers or datasets (the build's import guard is kept).
- `test_review_stage0_law3_gate_precedes_all_new_work`: on a LAW#3 miss, HALTED-V4 is raised, `pass_p1.json` holds recipe A only, and nothing runs after `run_recipe`. On a pass, every later step sees `law3=True`.
- `test_review_Z5_footprint_rejects_any_write_outside_selected_columns`: an unselected column, an unselected layer or a non-down parameter each give HALTED-V5.
- `test_review_Z6_restore_covers_all_36_and_verify_detects_drift`
- `test_review_wrapper_delegates_under_standing_law5`
- `test_review_write_round_cap_columns_and_capacity`: 10 writes then "round cap"; unselected columns byte-identical; B_Z from Z's A7 only.
- `test_review_write_prestart_projection_refuses_before_observation`
- `test_review_stage1_round_over_120s_halts_in_run`
- `test_review_stage_call_refusals`: fresh OUT_DIR; stage 2 only for a K1 survivor; stage 3 only after clean K2 with a stage-3 ceiling; each has a positive control.
- `test_review_reader_instrument_ceilings_audits_and_capacity`: τ_head > 0.25, σ_shape > 0.125, Z4 loop > 1e-10, recorded Z5 footprint, `Z_OVERRIDE_HITS`, V2 equality at 0.05, SemCon capacity, band distribution, process-2 clock origin, Z2 ambiguity at |lead| = τ.
- `test_review_cross_process_replication_needs_clean_pair`

**BLOCKING demonstrations (expected to fail now).** `c10z_mut/proposed/blocking_demos.py`, run in `c10z_mut/root2` with Popen/resident stubbed → `FAILED (failures=3)` (`proposed/blocking_demos_on_pristine.log`):
- B1: `['p1'] != []`
- B2: `'HALTED-V12' != 'NULL-STAGE1'`
- B3: pass record replaced

Each should pass once its fix lands.
