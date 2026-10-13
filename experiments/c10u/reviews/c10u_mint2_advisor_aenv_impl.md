Verdict: PROCEED

Single most important fix: none blocking. Before launching r2, commit the reader, selftest and wrapper as they are now, and record one ruling: a driver refusal that is not a §2 condition does not close r2 (see A1). An unnecessary conditional stage, source-identity drift or an operator mistake ends in `halt()` and writes a HALT diagnostic, so the ruling has to exist before r2 starts.

Reviewer: Claude (independent adversarial implementation review), 2026-10-07. Scope: §8 of `docs/C10U_MINT2_PREREG.md` (sha256 `c54f443c…`, committed, unmodified) against the uncommitted diff of `experiments/track_c/c10u_mint2_read.py` (sha256 `2367394b…`) and `experiments/track_c/c10u_mint2_selftest.py` (`86256991…`), plus the new `tools/run_c10u_stage_r2.sh` (`091c1b7b…`). All three hashes match Codex's report table.

## Evidence I produced (not taken from the Codex report)

- `.venv/bin/python -B experiments/track_c/c10u_mint2_selftest.py`: 60 tests, OK, exit 0, and the no-torch/transformers/bandknob guard passed.
- Independent oracle sweep. I wrote §8 changes 3 and 4 from the prereg text (positive check first, then negative, otherwise MIXED) and compared the real `R._range_direction` against it over S 0–24, five M1 triples and every sorted candidate triple in 0–49. That is 5,525,000 inputs across both blocks, with 0 mismatches. The positive and negative conditions cannot overlap: positive requires min > 18 and min − S ≥ 10, which rules out both negative disjuncts.
- Persistence sweep. I built 312 block states through the real `R.block_reading`: F and V2, S ∈ {4, 5, 11, 19}, six candidate triples, with and without replicas, partial blocks and controls. Each reading went through the real `A.write_json` inside a stage-completion record, followed by a recursive scan for tuples, sets, non-string keys and non-finite floats. Result: 0 failures. The states covered every direction: INCOMPLETE 144, NOT-COMPARABLE 60, MIXED 47, HALT-LAW3 24, PENDING-REPLICATION 16, PAIR 9, NO-MODIFIER-GAIN 3, MODIFIER-RECOVERY 3, SPAN 2, SPAN-CONFOUNDED 2, PENDING-CONTROL 2. The fixed `stage_plan` outputs also persist.
- `tools/engine_fingerprint.py`: memit_main sha256 `d941a9fb…` matches, `_cov_cpu` = 3. `git diff` is empty for `c10u_mint2_arms.py`, `memit_dry_run/` and `c10e_bandknob.py`.

## Check 1: §8 to test mapping (all tests go through the real functions)

| §8 item | Test (selftest line) | Through real function |
|---|---|---|
| Change 1, A4 window in F (block + replica) and V2 comparability | `test_aenv_baseline_boundaries_in_both_blocks_and_replicates` :666; `test_aenv_halt_stops_both_blocks…` :783 | `reproduction_gate`, `_comparability`, `block_reading`, `A.stages` (the real orchestration with child processes mocked) |
| Change 1, r1's 10/8/55 passes A4 and fails the old window | `test_aenv_r1_counts_pass_a4…` :813 | `reproduction_gate`; uses a fixture, does not read r1 |
| Change 2, NULL_BAND 10/11/18/19, initial label and replication exclusion | `test_aenv_null_boundaries_and_replication_exclusion` :688 | `_single_label`, `run_reading` with replica |
| Changes 3 and 4, all seven truth-table rows, run in block and replica | `test_aenv_truth_table_verbatim…` :697 | `_range_direction`, `block_reading` (`raw_direction`, `replica_ranges`, `direction`) |
| Changes 3 and 4, Codex counterexamples | :717 | `_range_direction`, `stage_plan("control")` |
| Change 5, all-NULL gets no control; reference and negative directions still replicate; positive V2 triggers the 3-run control | :729 | `block_reading`, `stage_plan` |
| Change 5, a replica can overturn positive routing | :750 | `block_reading(a, b)` |
| Change 6, list pairs; `missing` and `replication_missing` round-trip; a tuple still raises | :761 | real `A.write_json` and `block_reading` |
| r2 procedure, source pin covers the amended prereg, reader and driver | :821 | `A.source_hashes`, `A.assert_sources` |

Every truth-table row is copied exactly; I re-derived each by hand and got the same label. Items with no automated test: the wrapper (checked by reading it, below) and the obligation to report the old-window counterfactual (a reporting duty with no code; see A4). Neither needs a test before launch.

## Check 2: diff against §8

The reader diff has 9 added and 8 removed lines, and every one traces to §8:
- `BASELINE_WINDOW` (read.py:21) is used exactly at :378 (block-F LAW#3 multi check, which serves block and replica because `block_reading` calls `reproduction_gate` per population at :491, and the driver calls it per replicate at arms.py:1023–1025) and at :422 (`_comparability`). There is no other use, and no leftover `ENVELOPE`. I grepped the reader, arms and p4_probe for `ENVELOPE` and for the literals 11, 18, 48, 62, 59 and 42; no stale window value remains.
- `NULL_BAND` (read.py:22) is used exactly at :291 (`_single_label`) and :334 (replication exclusion), plus inside `_range_direction` :413/:415 as changes 3 and 4 require.
- Direction rules at :413/:415: the positive check is `min(m2) > NULL_BAND[1]` (strictly > 18), and the negative check is `max(m2) - s < GAIN_MIN or max(m2) <= NULL_BAND[1]` (≤ 18). Both match §8:177–178 exactly, boundaries included.
- `missing` at :403 is `sorted([str(k), str(s)] …)`, and `replication_missing` at :457 reuses `b["missing"]`. `write_json` (arms.py:45–54) is unchanged and still strict.

## Check 3: boundaries re-derived by hand

| Bound | Fail | Pass | Pass | Fail | Test asserts |
|---|---|---|---|---|---|
| para_full [5, 18] | 4 | 5 | 18 | 19 | F, T, T, F in F and V2, r0 and r1 |
| canon [5, 10] | 4 | 5 | 10 | 11 | same |
| para_first [42, 59] | 41 | 42 | 59 | 60 | same |
| NULL (11, 18) | 10 → PARTIAL (gain 10) | 11 → NULL | 18 → NULL | 19 → PARTIAL | `_single_label`, plus the replica giving PARTIAL vs PARTIAL-NOT-REPLICATED |

The test's `multi()` helper rewrites the detail rows so that `run_validity` is `[]` for every boundary value (asserted at :662). The fail cases therefore fail on the window itself, not on a validity error.

## Check 4: persistence

`missing` and `replication_missing` are now lists of lists. I traced every `write_json` callsite in the driver: arms.py:71 (halt), 147 (identity), 632 (P4 hf reference), 664/683 (contexts), 699/714/742 (step0), 777/779/864 (behavior), 974 (p4 admitted), 1014/1031 (stage start and complete), 1053/1057 (step0 stage).

Runtime record paths that r1 never exercised are step0 and behavior for modifier, mint2, mint1_48 and V2, plus `bigram_probe` and the P4 records. Reading them, every payload builds lists or dicts with string keys: `rank_prob` tuples are unpacked into dicts (arms.py step0_probe), `ids_of` returns `list(...)`, `bigram_probe` rows are dicts, and quota keys are str-cast. The model-dependent fields are the same functions r1 already persisted for mint1 and multi.

The reader-produced stage readings are covered by the 312-state sweep above, with no residual tuple or int-key source. The one residual risk I cannot test without a model is a float NaN or inf inside a model-derived field (for example `piv_stats` or `write_ratio`) on a kind r1 never ran. `allow_nan=False` would then HALT. That would be a true data anomaly, not the r1 bookkeeping class.

## Check 5: run identity and isolation

- Source identity is content hashes of `SOURCE_FILES` (arms.py:23–26), which include the prereg, reader, driver, selftest and v2 wordlist, plus all engine `.py` files. It is created fresh in `out/identity.json` (arms.py:136–148). r2's `--out-dir` is new (`results/c10u_mint2/r2` does not exist), so r2 gets a new identity, and r1's identity is never loaded.
- The selftest pins the prereg sha `c54f443c…` (selftest:824), which equals the file on disk.
- r2 never reads r1 records. `read_records` uses the non-recursive `out.glob("*.json")` (arms.py:873). Contexts, step0, inits, zs and logs are all `out`-relative. The P4 chain derives `out` from the admitted record's parent (p4_probe.py:101–113). The reverse also holds: the reader CLI on r1's directory uses `iterdir()` with a filename regex, so it cannot pool `r2/`.
- The only file read from r1's directory is the frozen stimulus `results/c10u_mint2/v2_wordlist.json`. It was committed in `fd5bb49` before r1, it is clean in git and hash-pinned, and it is an input, not an r1 output. `out.relative_to(root/"results/c10u_mint2")` (arms.py:1081) accepts `r2`.
- HALT diagnostics go to `architecture_profile/`, where r1's diagnostic already exists, so r2's diagnostic gets a uuid name (arms.py:65–67). It cannot overwrite r1's.

## Check 6: wrapper

`diff` against the original `/Users/robertrhu/.claude/jobs/4d71207f/tmp/run_c10u_stage.sh` shows exactly two changes: `LOGS=…/c10u_mint2_logs/r2` and `--out-dir "$W/results/c10u_mint2/r2"`. r1's logs (`results/c10u_mint2_logs/{reproduce,frozen}.log`, `reproduce_law3_gate.json`) cannot be reached. The script runs `rc=$?` directly after python, appends `STAGE_EXIT`, then `exit $rc`, so the exit code propagates. The driver exits non-zero on every halt (a `SystemExit` with a string).

## Items

1. ADVISORY (A1, highest; procedure, not code). An unnecessary or misordered conditional stage becomes a HALT diagnostic. `stages()` raises `ValueError("conditional stage is unnecessary…")` (arms.py:991), and `main()` turns any exception into `halt()` (arms.py:1104–1105). The result is an `architecture_profile/c10u_mint2_halt_diagnostic_<uuid>.json` and exit 1. The same happens if any `SOURCE_FILES` entry is edited during the ~28-run schedule (`assert_sources`, arms.py:94). That covers the prereg, reader, selftest, hparams, engine, bandknob and wordlist; a mid-run edit to the prereg for close-out notes would trigger it. Codex's command sheet puts the conditional stages under `set -e` in one block. §8:172 says "any other §2 halt condition" closes r2, so r2 is the last attempt under these rules. Exact fix: before launch, record in the runbook §5 or the prereg (before the identity is created) that driver refusals outside §2 do not close r2: an unnecessary conditional stage, source drift, an occupied output, or a preflight or fingerprint failure. Run conditional stages only after reading `controls_pending` and `replication_pending` from the previous `<stage>_complete.json`. Freeze every `SOURCE_FILES` entry until r2 closes.
2. ADVISORY (A2). Commit before launch. r2's `identity.json` will pin the hashes of the currently uncommitted reader and selftest (`2367394b…`, `86256991…`). Git is the durable tier, so commit those two files and `tools/run_c10u_stage_r2.sh` before the `reproduce` stage. Committing does not change the content hashes.
3. ADVISORY (A3). The wrapper truncates its own log on a rerun. `> "$LOGS/$STAGE.log"` (run_c10u_stage_r2.sh:11) would overwrite r2's earlier log if the same stage name is invoked twice, for example after a preflight refusal. It cannot touch r1. Exact fix, optional: change the line to `LOG="$LOGS/$STAGE.$(date -u +%Y%m%dT%H%M%SZ).log"` and use `"$LOG"` in both redirects. Alternatively, keep the wrapper and never rerun a stage name.
4. ADVISORY (A4). The old-window counterfactual has no tooling. §8:186 requires reporting "whether r2's blocks would have passed the original window", but the reader no longer carries the old constant. The F and V2 multi counts (`arm.para_full_n`, `canon_full_n`, `para_first_n`) are in r2's `F_r0_multi_snone.json` and `V2_r0_multi_snone.json`, so the close-out must compute it by hand against para_full [11, 18], canon [5, 10] and para_first [48, 62]. No code change is needed now.
5. ADVISORY (A5, residual risk, not testable model-free). A NaN or inf in a model-derived field on a kind r1 never ran (modifier, mint2, mint1_48) would HALT in `write_json` (`allow_nan=False`). That would be a true anomaly, reported as such, not a bookkeeping false HALT. Watch the first V2 step0 and behavior record.

BLOCKING count: 0.
