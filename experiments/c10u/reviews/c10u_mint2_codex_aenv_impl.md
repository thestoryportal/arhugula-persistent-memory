# D-C10u-mint2 Amendment A-env — implementation

Model: **gpt-6.1-sol (Codex)**. Effort: **max**. Verified from this session's latest `turn_context` (thread `01a11659-80b8-7c13-ad7d-043497c8d9d6`). Date: 2026-10-07T12:53:18.173519+00:00.

**DONE for the requested implementation: 60/60 model-free selftests PASS, including all 50 original tests.** Ten A-env tests were added before the reader edit and observed failing; one reader implementation round made the suite green. The r2 wrapper is prepared and syntax-checked. No experiment, tokenizer, model, torch/MPS or GPU job ran; r2 has no output or log directory. Runtime scientific gates and outcomes remain UNVERIFIED.

This repairs the instrument and routing for the C10 write-layer representation diagnostic (§C and post-write readout §F of `docs/SPEC_E2E_GROUND_TRUTH.md`), following the already frozen amendment. It supplies no new empirical finding or F1 closure. The experiment close-out gate remains a requirement of the eventual scientific run, as [docs/C10U_MINT2_PREREG.md:115](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/C10U_MINT2_PREREG.md:115) states.

## §8 item → test → code

| Binding item | Test and covered behavior | Code |
|---|---|---|
| Change 1, [§8:175](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/C10U_MINT2_PREREG.md:175): A4 in F and V2, original and replica | [experiments/track_c/c10u_mint2_selftest.py:666](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_selftest.py:666): para_full 4/5/18/19, canon 4/5/10/11, para_first 41/42/59/60 in both blocks and both replicates; [experiments/track_c/c10u_mint2_selftest.py:813](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_selftest.py:813): synthetic 10/8/55 passes A4 and fails the old window | [experiments/track_c/c10u_mint2_read.py:21](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_read.py:21) `BASELINE_WINDOW`; [experiments/track_c/c10u_mint2_read.py:378](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_read.py:378) F LAW#3; [experiments/track_c/c10u_mint2_read.py:422](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_read.py:422) V2 comparability. Mint-1 seed windows and median threshold remain unchanged. |
| Change 2, [§8:176](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/C10U_MINT2_PREREG.md:176): one frozen NULL band | [experiments/track_c/c10u_mint2_selftest.py:688](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_selftest.py:688): 10/11/18/19 through `_single_label` and real `run_reading` replication exclusion | [experiments/track_c/c10u_mint2_read.py:22](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_read.py:22) `NULL_BAND`; [experiments/track_c/c10u_mint2_read.py:291](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_read.py:291) initial label; [experiments/track_c/c10u_mint2_read.py:334](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_read.py:334) replication exclusion |
| Change 3, [§8:177](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/C10U_MINT2_PREREG.md:177): positive compatibility | [experiments/track_c/c10u_mint2_selftest.py:697](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_selftest.py:697): every §8 truth-table row; [experiments/track_c/c10u_mint2_selftest.py:717](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_selftest.py:717): both envelope-review counterexamples; [experiments/track_c/c10u_mint2_selftest.py:750](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_selftest.py:750): a replica can overturn positive routing | [experiments/track_c/c10u_mint2_read.py:413](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_read.py:413) V2 positive clause and [experiments/track_c/c10u_mint2_read.py:415](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_read.py:415) F positive clause require `min(candidate) > NULL_BAND[1]` |
| Change 4, [§8:178](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/C10U_MINT2_PREREG.md:178): negative mirror | [experiments/track_c/c10u_mint2_selftest.py:697](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_selftest.py:697) and [experiments/track_c/c10u_mint2_selftest.py:729](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_selftest.py:729): all-NULL negative labels at S=5; a seed at 19 is not absorbed into the all-NULL clause; old gain-only negative row at S=12 | [experiments/track_c/c10u_mint2_read.py:413](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_read.py:413) and [experiments/track_c/c10u_mint2_read.py:415](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_read.py:415): `max(candidate) - S < GAIN_MIN or max(candidate) <= NULL_BAND[1]` |
| Change 5, [§8:179](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/C10U_MINT2_PREREG.md:179): real raw and replicated directions; unchanged replication triggers | [experiments/track_c/c10u_mint2_selftest.py:729](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_selftest.py:729): NULL-containing blocks get no 48-row control, negative/all-NULL blocks still get seven-run replication plans through reference arms and negative routing; mixed blocks still replicate via their references; a positive V2 block gets three control runs. [experiments/track_c/c10u_mint2_selftest.py:750](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_selftest.py:750) verifies replica-direction disagreement. | Both clauses are inside [experiments/track_c/c10u_mint2_read.py:406](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_read.py:406) `_range_direction`; existing [experiments/track_c/c10u_mint2_read.py:472](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_read.py:472) applies it to both blocks; existing [experiments/track_c/c10u_mint2_read.py:482](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_read.py:482), [experiments/track_c/c10u_mint2_read.py:503](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_read.py:503), [experiments/track_c/c10u_mint2_read.py:505](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_read.py:505) and [experiments/track_c/c10u_mint2_read.py:550](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_read.py:550) retain pending/spending behavior |
| Change 6, [§8:180](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/C10U_MINT2_PREREG.md:180): JSON list pairs and strict writer | [experiments/track_c/c10u_mint2_selftest.py:761](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_selftest.py:761): partial F; complete F + partial replica; HALT-LAW3 stage readings, all through real `write_json` → persisted JSON → equality; tuple-bearing negative case still raises | [experiments/track_c/c10u_mint2_read.py:403](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_read.py:403) emits lists; unchanged [experiments/track_c/c10u_mint2_read.py:457](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_read.py:457) copies the same lists into `replication_missing`; unchanged strict writer [experiments/track_c/c10u_mint2_arms.py:45](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_arms.py:45) |
| Last-attempt/HALT discipline, [§8:172](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/C10U_MINT2_PREREG.md:172) | [experiments/track_c/c10u_mint2_selftest.py:783](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_selftest.py:783): F multi para_full 19 and para_first 60 halt real synthetic `frozen` and `replicate-F` orchestration before any modifier child; the initial miss also prevents any V2 child or V2 marker | Existing [experiments/track_c/c10u_mint2_arms.py:922](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_arms.py:922) and [experiments/track_c/c10u_mint2_arms.py:979](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_arms.py:979) consume the amended reproduction gate; no driver edit |
| r2 namespace/source identity, [§8:186](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/C10U_MINT2_PREREG.md:186) | [experiments/track_c/c10u_mint2_selftest.py:821](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_selftest.py:821) pins the amended prereg hash, verifies reader/driver inclusion, and rejects a stale prereg identity. Exact wrapper comparison and `bash -n` PASS. | Existing [experiments/track_c/c10u_mint2_arms.py:24](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_arms.py:24), [experiments/track_c/c10u_mint2_arms.py:77](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_arms.py:77), [experiments/track_c/c10u_mint2_arms.py:89](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_arms.py:89) and [experiments/track_c/c10u_mint2_arms.py:135](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_arms.py:135) already hash/pin the prereg, reader, driver and selftest; [tools/run_c10u_stage_r2.sh:9](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/run_c10u_stage_r2.sh:9) isolates logs and [tools/run_c10u_stage_r2.sh:11](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/run_c10u_stage_r2.sh:11) supplies `--out-dir` |

The two counterexamples are the exact counts from `results/c10u_mint2_codex_envelope.md:75–76`: V2 S=5, M1={34,36,46}, M2={15,16,18} now reads PAIR-DIRECTION with three NULL seeds; F S=5, M1F={40,36,41}, MO={15,25,36} now reads MIXED with NULL/PARTIAL/LEAD per-seed labels. These are synthetic logic checks, not r2 observations.

## LAW#4 reads and implementation decisions

Before editing, I read the full numbered bodies in the original `experiments/track_c/c10u_mint2_read.py`: `_single_label` at 289–293, `run_reading` at 309–358, `reproduction_gate` at 361–383, `_population` at 386–402, `_range_direction` at 405–415, and `_comparability` at 418–421. I also read their real consumers `block_reading` at 434–523 and `stage_plan` at 531–550; the unchanged driver's `write_json` at 45–54, source identity at 77–94/135–148, reproduction HALT at 922–931, and `stages` at 979–1032; and all 14 lines of the original stage wrapper. The table above cites the final code lines. Existing selftest functions were left unchanged; the new class starts at [experiments/track_c/c10u_mint2_selftest.py:650](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_selftest.py:650).

- V2 uses A4 exactly as [docs/C10U_MINT2_PREREG.md:175](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/C10U_MINT2_PREREG.md:175) requires, including the tighter para_first ceiling of 59. The earlier recommendation to retain the old V2 window was not carried into this implementation.
- The full decision is positive condition → negative condition → MIXED. A candidate set entirely within the NULL band gets the negative label, as [docs/C10U_MINT2_PREREG.md:178](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/C10U_MINT2_PREREG.md:178) and the explicit rows at [docs/C10U_MINT2_PREREG.md:182](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/C10U_MINT2_PREREG.md:182) require; the positive-rule sentence's “otherwise MIXED” is read together with the following negative amendment.
- Where §8's count-only truth table omits M1, tests use the existing valid fixture default {34,36,46}; the relevant negative/MIXED result does not depend on changing that reference set ([docs/C10U_MINT2_PREREG.md:182](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/C10U_MINT2_PREREG.md:182)).
- There is no runtime literal prereg SHA to update: the existing dynamic identity pin includes the amended document. The new selftest fixes its current SHA explicitly and exercises stale-source rejection. The driver and writer therefore need no changes ([experiments/track_c/c10u_mint2_arms.py:24](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_arms.py:24), [experiments/track_c/c10u_mint2_arms.py:77](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_arms.py:77), [experiments/track_c/c10u_mint2_arms.py:89](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_arms.py:89)).
- r1's named counts are copied only into synthetic fixtures for the required old-versus-A4 assertion. No r1 behavior record was evaluated with the amended reader; r1 remains HALTED ([docs/C10U_MINT2_PREREG.md:170](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/C10U_MINT2_PREREG.md:170)).

## Diff summary and preservation

- `experiments/track_c/c10u_mint2_read.py`: 9 added lines / 8 removed lines, exclusively the two constants, their four consumers, direction clauses, and JSON-list emission.
- `experiments/track_c/c10u_mint2_selftest.py`: 186 added lines, ten new A-env tests plus a valid-record helper; all 50 existing tests unchanged.
- `tools/run_c10u_stage_r2.sh`: 14-line copy of the original wrapper, with exactly two textual changes: r2 log directory and the r2 `--out-dir` argument. Original mode 0644 retained; commands below invoke bash explicitly. Existing usage/error text is preserved.
- This report is the only new authored result artifact. No prereg, engine, bandknob, driver, canonical ledger, checkpoint or Git-state mutation was performed.

SHA-256, mode and mtime checks PASS for 198 protected files. This includes all 35 files under r1's `results/c10u_mint2/`, all three r1 log files, all 154 engine files, the halt diagnostics, bandknob, the amended prereg, the unchanged driver and `.gitignore`. Directory-file inventories also match the starting snapshot. The original 10/8/55 r1 data remains untouched; synthetic comparisons do not relabel it. Evidence: [preservation check](/private/tmp/c10u-aenv-5u2crp1x/preservation.txt) and [initial snapshot](/private/tmp/c10u-aenv-5u2crp1x/before.json).

Tooling note: the ignored generated `graft/.cache/ask-index.json` refreshed during the tooling session; it is outside the scientific source pin and the 198-file preservation claim. Its observed SHA-256 was `012e577eec8523b194f203c80b4a5bd4f8de50b97aee6d45c6772f767706278d`. No tracked Graft or ignore-file change remains.

## Test-first evidence and verification

Exact authorized selftest command, run with RTK's unfiltered proxy:

```bash
.venv/bin/python -B experiments/track_c/c10u_mint2_selftest.py
# Actual invocation: /opt/homebrew/bin/rtk proxy .venv/bin/python -B experiments/track_c/c10u_mint2_selftest.py
```

1. Unmodified original suite: exit 0, 50 tests, OK ([full baseline output](/private/tmp/c10u-aenv-5u2crp1x/baseline.log)).
2. New tests added while reader and driver still matched their saved starting SHA-256. Initial RED: exit 1, 60 tests, 31 failures and two errors ([output](/private/tmp/c10u-aenv-5u2crp1x/red.log)). Before any reader edit, the round-trip test was arranged to call the real writer before inspecting list shape. Final RED: exit 1, 60 tests, 29 failures and four errors ([full RED output](/private/tmp/c10u-aenv-5u2crp1x/red-roundtrip.log)). Both partial-F and partial-replica records fail with `RuntimeError: JSON did not persist exactly`; other failures show old boundaries and obsolete directions. Two errors also identify the not-yet-created named constants.
3. One reader amendment round, then GREEN: exit 0, 60 tests, OK. All 50 original tests remain green. Full output is pasted below verbatim.
4. `/opt/homebrew/bin/rtk proxy /bin/bash -n tools/run_c10u_stage_r2.sh`: exit 0. Exact comparison against the old wrapper plus the two requested replacements: PASS. `git diff --check` on the changed Python files: exit 0.

The suite's final guard confirms no `torch`, `transformers` or `c10e_bandknob` module was imported. HALT orchestration tests replace context/step0/child execution with synthetic records in temporary directories; they verify the real gate, stage stop and diagnostic writer, and supply no live model evidence.

```text
test_aenv_baseline_boundaries_in_both_blocks_and_replicates (__main__.AenvTests.test_aenv_baseline_boundaries_in_both_blocks_and_replicates) ... ok
test_aenv_envelope_review_counterexamples_keep_null_precedence (__main__.AenvTests.test_aenv_envelope_review_counterexamples_keep_null_precedence) ... ok
test_aenv_halt_stops_both_blocks_in_initial_and_replication_stages (__main__.AenvTests.test_aenv_halt_stops_both_blocks_in_initial_and_replication_stages) ... ok
test_aenv_null_boundaries_and_replication_exclusion (__main__.AenvTests.test_aenv_null_boundaries_and_replication_exclusion) ... ok
test_aenv_r1_counts_pass_a4_and_fail_original_window_without_reading_r1 (__main__.AenvTests.test_aenv_r1_counts_pass_a4_and_fail_original_window_without_reading_r1) ... ok
test_aenv_replica_compatibility_can_overturn_positive_routing (__main__.AenvTests.test_aenv_replica_compatibility_can_overturn_positive_routing) ... ok
test_aenv_schedule_keeps_reference_and_negative_direction_replication (__main__.AenvTests.test_aenv_schedule_keeps_reference_and_negative_direction_replication) ... ok
test_aenv_source_identity_pins_amended_prereg_reader_and_driver (__main__.AenvTests.test_aenv_source_identity_pins_amended_prereg_reader_and_driver) ... ok
test_aenv_stage_completion_round_trips_missing_and_replication_missing (__main__.AenvTests.test_aenv_stage_completion_round_trips_missing_and_replication_missing) ... ok
test_aenv_truth_table_verbatim_through_range_and_replication (__main__.AenvTests.test_aenv_truth_table_verbatim_through_range_and_replication) ... ok
test_a1_68_boundary_and_missing_shape_fail_closed (__main__.ReaderTests.test_a1_68_boundary_and_missing_shape_fail_closed) ... ok
test_admission_22_values_and_per_position_underfit_remain_distinct (__main__.ReaderTests.test_admission_22_values_and_per_position_underfit_remain_distinct) ... ok
test_bigram_shape_rejects_missing_duplicate_or_invalid_fraction (__main__.ReaderTests.test_bigram_shape_rejects_missing_duplicate_or_invalid_fraction) ... ok
test_bigram_uses_fact_union_and_zero_correct_is_no_continuation (__main__.ReaderTests.test_bigram_uses_fact_union_and_zero_correct_is_no_continuation) ... ok
test_block_rejects_changed_context_data_and_pairing (__main__.ReaderTests.test_block_rejects_changed_context_data_and_pairing) ... ok
test_blocked_direction_has_no_pending_control (__main__.ReaderTests.test_blocked_direction_has_no_pending_control) ... ok
test_blocks_never_pool_or_recover_missing_seed (__main__.ReaderTests.test_blocks_never_pool_or_recover_missing_seed) ... ok
test_cli_reads_only_records_and_excludes_context_bootstrap (__main__.ReaderTests.test_cli_reads_only_records_and_excludes_context_bootstrap) ... ok
test_complete_record_and_raw_minus_pre_binding (__main__.ReaderTests.test_complete_record_and_raw_minus_pre_binding) ... ok
test_contains_allows_alternative_ids_and_startswith_is_separate (__main__.ReaderTests.test_contains_allows_alternative_ids_and_startswith_is_separate) ... ok
test_control_spending_requires_a_routable_valid_span_block (__main__.ReaderTests.test_control_spending_requires_a_routable_valid_span_block) ... ok
test_control_uses_the_registered_initial_comparison_not_an_extra_replica_control (__main__.ReaderTests.test_control_uses_the_registered_initial_comparison_not_an_extra_replica_control) ... ok
test_direction_keeps_candidate_large_write_and_bigram_qualifiers (__main__.ReaderTests.test_direction_keeps_candidate_large_write_and_bigram_qualifiers) ... ok
test_full_fourteen_schedule_and_conditional_stages (__main__.ReaderTests.test_full_fourteen_schedule_and_conditional_stages) ... ok
test_geometry_collapse_boundaries_are_diagnostic (__main__.ReaderTests.test_geometry_collapse_boundaries_are_diagnostic) ... ok
test_hashes_context_and_row_counts_are_recomputed (__main__.ReaderTests.test_hashes_context_and_row_counts_are_recomputed) ... ok
test_i11_admission_boundaries_and_geometry_is_diagnostic (__main__.ReaderTests.test_i11_admission_boundaries_and_geometry_is_diagnostic) ... ok
test_inertness_fingerprint_and_override_audits_reject_tampering (__main__.ReaderTests.test_inertness_fingerprint_and_override_audits_reject_tampering) ... ok
test_inertness_precision_gate (__main__.ReaderTests.test_inertness_precision_gate) ... ok
test_large_write_is_qualifier_not_gate (__main__.ReaderTests.test_large_write_is_qualifier_not_gate) ... ok
test_law3_miss_suspends_frozen_block (__main__.ReaderTests.test_law3_miss_suspends_frozen_block) ... ok
test_law3_seed_envelopes_median_and_multi_envelope (__main__.ReaderTests.test_law3_seed_envelopes_median_and_multi_envelope) ... ok
test_locality_boundaries_and_falsefires (__main__.ReaderTests.test_locality_boundaries_and_falsefires) ... ok
test_malformed_block_objects_fail_closed_without_raising (__main__.ReaderTests.test_malformed_block_objects_fail_closed_without_raising) ... ok
test_mechanism_curve_respects_first_position_loss_without_a_percentage_cutoff (__main__.ReaderTests.test_mechanism_curve_respects_first_position_loss_without_a_percentage_cutoff) ... ok
test_missing_norm_layer_and_empty_p2_rows_are_invalid (__main__.ReaderTests.test_missing_norm_layer_and_empty_p2_rows_are_invalid) ... ok
test_modifier_recovery_truth_table_frozen_at_v3 (__main__.ReaderTests.test_modifier_recovery_truth_table_frozen_at_v3) ... ok
test_not_comparable_and_underfit_precede_direction (__main__.ReaderTests.test_not_comparable_and_underfit_precede_direction) ... ok
test_null_band_precedes_gain_and_tradeoff_uses_binding (__main__.ReaderTests.test_null_band_precedes_gain_and_tradeoff_uses_binding) ... ok
test_p4_full_sequences_gate_and_q4_correctness_is_report_only (__main__.ReaderTests.test_p4_full_sequences_gate_and_q4_correctness_is_report_only) ... ok
test_p4_reports_fp16_gguf_to_q4_survival_with_its_own_denominator (__main__.ReaderTests.test_p4_reports_fp16_gguf_to_q4_survival_with_its_own_denominator) ... ok
test_p4_tokenizer_population_and_subject_specific_ids_fail_closed (__main__.ReaderTests.test_p4_tokenizer_population_and_subject_specific_ids_fail_closed) ... ok
test_pair_nonoverlap_rule_and_seed_range (__main__.ReaderTests.test_pair_nonoverlap_rule_and_seed_range) ... ok
test_public_readings_round_trip_as_strict_json (__main__.ReaderTests.test_public_readings_round_trip_as_strict_json) ... ok
test_reference_and_i11_helpers_keep_known_baseline_and_whole_recall (__main__.ReaderTests.test_reference_and_i11_helpers_keep_known_baseline_and_whole_recall) ... ok
test_replica_locality_miss_prevents_replication (__main__.ReaderTests.test_replica_locality_miss_prevents_replication) ... ok
test_replication_uses_same_seed_context_rows_and_fresh_pid (__main__.ReaderTests.test_replication_uses_same_seed_context_rows_and_fresh_pid) ... ok
test_reproduction_provenance_is_checked_before_any_new_arm (__main__.ReaderTests.test_reproduction_provenance_is_checked_before_any_new_arm) ... ok
test_span_requires_replication_and_matched48_control (__main__.ReaderTests.test_span_requires_replication_and_matched48_control) ... ok
test_string_below_full_invalid_even_when_binding_is_lead (__main__.ReaderTests.test_string_below_full_invalid_even_when_binding_is_lead) ... ok
test_underfit_mask_is_reported_without_changing_binding (__main__.ReaderTests.test_underfit_mask_is_reported_without_changing_binding) ... ok
test_conditional_empty_stage_refuses_before_any_marker (__main__.SafetyTests.test_conditional_empty_stage_refuses_before_any_marker) ... ok
test_import_does_not_load_runtime (__main__.SafetyTests.test_import_does_not_load_runtime) ... ok
test_p2_audits_the_engine_default_tokenizer_call (__main__.SafetyTests.test_p2_audits_the_engine_default_tokenizer_call) ... ok
test_p2_audits_two_ids_and_all_720_bigram_prompts (__main__.SafetyTests.test_p2_audits_two_ids_and_all_720_bigram_prompts) ... ok
test_p2_checks_the_whole_modifier_target_even_when_last_id_matches (__main__.SafetyTests.test_p2_checks_the_whole_modifier_target_even_when_last_id_matches) ... ok
test_p2_detects_runtime_context_retokenization (__main__.SafetyTests.test_p2_detects_runtime_context_retokenization) ... ok
test_p4_selection_requires_replication_and_comparability (__main__.SafetyTests.test_p4_selection_requires_replication_and_comparability) ... ok
test_preflight_rejects_inherited_knobs_before_external_calls (__main__.SafetyTests.test_preflight_rejects_inherited_knobs_before_external_calls) ... ok
test_write_json_is_exclusive_and_rereads_exact_payload (__main__.SafetyTests.test_write_json_is_exclusive_and_rereads_exact_payload) ... ok

----------------------------------------------------------------------
Ran 60 tests in 1.619s

OK
C10U_MINT2_SELFTEST_DONE (stdlib only; no model/torch/GPU/driver)
```

## SHA-256

| Changed or new implementation file | SHA-256 |
|---|---|
| `experiments/track_c/c10u_mint2_read.py` | `2367394bd9d96fb077f5a4233edc6ff74de47f7310c4f55cdece9e25561de4e7` |
| `experiments/track_c/c10u_mint2_selftest.py` | `862569914eb7b4b3db828738010ed67c5a1fa4e76fbd144a2801b0621100f872` |
| `tools/run_c10u_stage_r2.sh` | `091c1b7bda44aa4ceb9883d085d16932a0fe9441a9bd2b7c3e5ca513e0714749` |

Amended prereg, read but not modified: `c54f443c70fecd12dce5440cbe7d606587ed1c8384542345f0411cfd0ba15a76`. The final report's own hash, together with all three implementation file hashes, is stored in the [final SHA-256 manifest](/private/tmp/c10u-aenv-5u2crp1x/changed-files.sha256). Keeping that checksum outside this report avoids a self-referential digest.

## Advisor input and context save

Read the existing independent Claude review `results/c10u_mint2_advisor_aenv.md`, including its counterexamples, four blocking issues and schedule correction; §8 explicitly folds that review. A fresh read-only `claude auth status` probe exited 1 with `loggedIn: false` and `authMethod: none`, so no fresh Claude review was obtained or claimed. Completion here is supported by the frozen §8 contract and the observed tests, not a new advisor verdict.

Context saved through the context-save workflow at [handoff](/private/tmp/c10u-aenv-5u2crp1x/checkpoints/20261007-124957-c10u-amendment-aenv.md); the default home-directory state path is outside this session's writable roots, so this scoped snapshot is kept with verification logs under `/private/tmp`. It records the branch, working state, decisions, verification and remaining authorized-run work. No durable memory file was modified.

## Objections

**none.** I find no remaining positive-routing/NULL-seed counterexample to the declared V2 A4 departure: the two original examples are explicitly rejected as positive directions, and the negative mirror, replica checks and conditional control behavior are tested. This is a statement about the implemented routing semantics. It does not establish comparability of different stimuli, causality, calibrated false-positive rates or live scientific success; the prereg's scoped caveats at [docs/C10U_MINT2_PREREG.md:11](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/C10U_MINT2_PREREG.md:11) and [docs/C10U_MINT2_PREREG.md:23](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/C10U_MINT2_PREREG.md:23) remain binding.

## Exact r2 stage commands in order

Prepared commands only; none was executed here. Keep stages serial and stop on any real stage failure. r2 is the last attempt under [docs/C10U_MINT2_PREREG.md:172](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/C10U_MINT2_PREREG.md:172). The wrapper supplies `--out-dir "$W/results/c10u_mint2/r2"` and redirects every stage log into `$W/results/c10u_mint2_logs/r2/`.

```bash
set -e
W=/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a
export LLMDB_ROOT="$W"

/opt/homebrew/bin/rtk proxy /bin/bash "$W/tools/run_c10u_stage_r2.sh" reproduce
/opt/homebrew/bin/rtk proxy /bin/bash "$W/tools/run_c10u_stage_r2.sh" frozen
/opt/homebrew/bin/rtk proxy /bin/bash "$W/tools/run_c10u_stage_r2.sh" v2

# Conditional: only when the real reader's V2 controls_pending is true.
/opt/homebrew/bin/rtk proxy /bin/bash "$W/tools/run_c10u_stage_r2.sh" control

# Conditional: only when the corresponding initial-block replication_pending is true.
/opt/homebrew/bin/rtk proxy /bin/bash "$W/tools/run_c10u_stage_r2.sh" replicate-F
/opt/homebrew/bin/rtk proxy /bin/bash "$W/tools/run_c10u_stage_r2.sh" replicate-V2

# Conditional: only for replicated eligible LEAD/PARTIAL mint2 or modifier configurations.
/opt/homebrew/bin/rtk proxy /bin/bash "$W/tools/run_c10u_stage_r2.sh" p4-save
```

Read pending/eligibility fields between stages and omit unnecessary conditional commands; the driver refuses empty conditional plans. The stage order and those refusals are the existing protocol, not a newly automated runner. All-NULL candidate blocks still trigger their replicas through mint-1 references and negative routing. No r1 context, init, source identity or record is copied into r2.

The model-free reader command after any completed stage is:

```bash
/opt/homebrew/bin/rtk proxy "$W/.venv/bin/python" -B "$W/experiments/track_c/c10u_mint2_read.py" "$W/results/c10u_mint2/r2"
```

After `p4-save`, run the existing P4 chain separately for each actual emitted eligible admitted record, using its **r2** path. For example, the following is exact for V2 seed 0 **only if that admitted record exists**; use the emitted F/V2 kind and seed for other eligible records:

```bash
/opt/homebrew/bin/rtk proxy /bin/bash "$W/tools/c10u_mint2_p4.sh" \
  --record "$W/results/c10u_mint2/r2/p4save_V2_r0_mint2_s0_admitted.json" \
  --source /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/llama_cpp_src \
  --bin /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/llama_cpp_src/prebuilt/llama-b11382
```

Scientific close-out subsequently reports both attempts and original-window counterfactual decisions for r2, including counts and context/source/init identities, as [docs/C10U_MINT2_PREREG.md:186](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/C10U_MINT2_PREREG.md:186) requires; it is not fabricated by this implementation report.
