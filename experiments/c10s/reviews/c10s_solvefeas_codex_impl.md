# D-C10s-solvefeas implementation report

Implemented `docs/C10S_SOLVEFEAS_PREREG.md` v2 §1–§4. Model-free verification: **28 selftests PASS**, all four Python files compile, and the targeted diff whitespace check passes. This is an implementation report, not an experiment finding or an F1 verdict.

## Limits observed

No model loaded; no GPU/MPS computation; no inertness or driver main executed; no external advisor/model invocation; no commit or push. Selftests import the pure reader, use fixed CPU tensors, and extract isolated definitions/settings initialization from the driver's AST for callback and persistence fixtures. Fixtures write only temporary directories. `memit_dry_run/`, `c10e_bandknob.py`, the autoresearch trees/clones, `CORPUS/`, and step-1 results were not edited by this task. The pre-existing work of the other agent was left in place.

Worktree: `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a`; branch: `worktree-c10k-route-a`.

## Files changed

| File | Change |
| --- | --- |
| `experiments/track_c/c10s_sharedz_arms.py` | Closed arm initialization; selected settings and assertions; settings provenance; read-only engine counters including nested LAW#5 calls; per-evaluation NLL; pre-update evaluation-25 snapshot and held-out injection; first/second-stage binding; reference-shift halt. |
| `experiments/track_c/c10s_sharedz_inertness.py` | Uses the driver's rebound settings, counted engine calls and nested LAW#5 bindings; carries selected settings and counts in the solvefeas record. |
| `experiments/track_c/c10s_sharedz_read.py` | Immutable arm tuples, binding checks, pure solve-budget and classification rules, qualified fit labels, reference-shift handling, and reader output. Existing sharedz rules remain intact. |
| `experiments/track_c/c10s_sharedz_selftest.py` | 17 additional model-free tests, including negative cases, boundary cases, real reader record access, hook cleanup, and equality against `1169794`. CPU tensor allocation is explicit. |
| `configs/hparams/qwen25_3b_memit_hparams_steps50.json` | New file; byte-for-byte the baseline file except `v_num_grad_steps: 25` becomes `50`. |
| `results/c10s_solvefeas_codex_impl.md` | This report and session handoff. |

Settings SHA-256: `f7a10f00eb1f7e37764aba0f6a231b3b0d316066f7f734f1e418a339acaeff33`.

## Every settings route and record boundary

Paths below are relative to the verified worktree. Harness/engine references describe inspected, unchanged code; they were not executed.

| Route | File:line |
| --- | --- |
| Closed `sharedz`/`solvefeas` tuple: Decision-ID, prereg, halt path, settings path, expected steps, output namespace | `experiments/track_c/c10s_sharedz_read.py:62`; `experiments/track_c/c10s_sharedz_read.py:72` |
| Selected absolute settings path, digest and four-field binding | `experiments/track_c/c10s_sharedz_arms.py:105`; `experiments/track_c/c10s_sharedz_arms.py:108`; `experiments/track_c/c10s_sharedz_arms.py:111` |
| `HP_CANDIDATE` set before the harness import; captured by the harness as `HP_BAND` | `experiments/track_c/c10s_sharedz_arms.py:126`; `experiments/track_c/c10e_bandknob.py:31` |
| Driver `hp` rebound from selected file; expected steps and harness path asserted | `experiments/track_c/c10s_sharedz_arms.py:146`; `experiments/track_c/c10s_sharedz_arms.py:147`; `experiments/track_c/c10s_sharedz_arms.py:148` |
| Shared target in cell 1 and the fresh second process; the shared loop and final budget break use this `hp` | `experiments/track_c/c10s_sharedz_arms.py:445`; `experiments/track_c/c10s_sharedz_arms.py:327`; `experiments/track_c/c10s_sharedz_arms.py:374`; `experiments/track_c/c10s_sharedz_arms.py:728` |
| Cell-1 canonical and noise-twin engine targets, same selected `hp` | `experiments/track_c/c10s_sharedz_arms.py:510`; `experiments/track_c/c10s_sharedz_arms.py:517` |
| Counted engine entry asserts actual steps and records settings and observed evaluations for every engine target | `experiments/track_c/c10s_sharedz_arms.py:213`; `experiments/track_c/c10s_sharedz_arms.py:216`; `experiments/track_c/c10s_sharedz_arms.py:219` |
| Inertness inherits `A.hp`; floor, triplicate and heterogeneous engine solves go through the counter; shared checks use the same object | `experiments/track_c/c10s_sharedz_inertness.py:35`; `experiments/track_c/c10s_sharedz_inertness.py:55`; `experiments/track_c/c10s_sharedz_inertness.py:60`; `experiments/track_c/c10s_sharedz_inertness.py:178`; `experiments/track_c/c10s_sharedz_inertness.py:192`; `experiments/track_c/c10s_sharedz_inertness.py:120` |
| Standalone inertness projector/snapshot and LAW#5 use selected `hp`; both engine and harness compute-z names temporarily counted | `experiments/track_c/c10s_sharedz_inertness.py:207`; `experiments/track_c/c10s_sharedz_inertness.py:208`; `experiments/track_c/c10s_sharedz_arms.py:228` |
| Harness candidate recipe loads `HP_BAND`; its LAW#5, A1, A2 and reference A7 therefore get the same file | `experiments/track_c/c10e_bandknob.py:582`; `experiments/track_c/c10e_bandknob.py:459`; `experiments/track_c/c10e_bandknob.py:463` |
| Both harness passes retain target capture while counting nested engine calls | `experiments/track_c/c10s_sharedz_arms.py:598`; `experiments/track_c/c10s_sharedz_arms.py:660` |
| Shared A7 write uses the harness's selected recipe object and already-solved shared targets through the existing override seam | `experiments/track_c/c10s_sharedz_arms.py:628` |
| Layer/key, residual-position and base-snapshot readouts use the selected settings too | `experiments/track_c/c10s_sharedz_arms.py:471`; `experiments/track_c/c10s_sharedz_arms.py:486`; `experiments/track_c/c10s_sharedz_arms.py:654` |
| Settings fields on every solvefeas persisted output, halt diagnostic, identity, shared diagnostic, injection record and inertness record | `experiments/track_c/c10s_sharedz_arms.py:90`; `experiments/track_c/c10s_sharedz_arms.py:80`; `experiments/track_c/c10s_sharedz_arms.py:195`; `experiments/track_c/c10s_sharedz_arms.py:385`; `experiments/track_c/c10s_sharedz_arms.py:573`; `experiments/track_c/c10s_sharedz_inertness.py:171` |
| Pass solve records, per-arm captured targets and first-stage run retain actual settings, not `H.HP_BASE` | `experiments/track_c/c10s_sharedz_arms.py:653`; `experiments/track_c/c10s_sharedz_arms.py:617`; `experiments/track_c/c10s_sharedz_arms.py:749` |
| Inertness record and identity refused on any arm/path/digest/budget mismatch, before source-hash comparison | `experiments/track_c/c10s_sharedz_arms.py:695`; `experiments/track_c/c10s_sharedz_arms.py:709`; `experiments/track_c/c10s_sharedz_arms.py:710` |
| Second stage binds run, identity, pass 1 and pass-1 identity before solving; permanent second-process record is stamped | `experiments/track_c/c10s_sharedz_arms.py:784`; `experiments/track_c/c10s_sharedz_arms.py:785`; `experiments/track_c/c10s_sharedz_arms.py:796`; `experiments/track_c/c10s_sharedz_arms.py:797`; `experiments/track_c/c10s_sharedz_arms.py:805` |
| Reader checks settings across injection, inertness, passes and terminal second-process records | `experiments/track_c/c10s_sharedz_read.py:49`; `experiments/track_c/c10s_sharedz_read.py:163`; `experiments/track_c/c10s_sharedz_read.py:406`; `experiments/track_c/c10s_sharedz_read.py:476` |
| Both preregs and the new settings file hashed for solvefeas; original source list retained for sharedz | `experiments/track_c/c10s_sharedz_arms.py:163`; `experiments/track_c/c10s_sharedz_arms.py:168`; `experiments/track_c/c10s_sharedz_arms.py:188` |

## Snapshot, rules and defaults

Each solvefeas history entry contains its evaluation number and per-prompt NLL. Evaluation 25 captures the frame fits, full saved optimizer delta, and shared-z digest/norm before the update (`experiments/track_c/c10s_sharedz_arms.py:369`). Held-out evaluation uses that saved z, not the final z, and records per-pair and aggregate full-sequence hits (`experiments/track_c/c10s_sharedz_arms.py:546`; `experiments/track_c/c10s_sharedz_arms.py:588`). Snapshot injection is never a gate.

The reader derives fits from the NLL history. Its rules are `underfit_class` at `experiments/track_c/c10s_sharedz_read.py:98`, `solvefeas_reading` at `experiments/track_c/c10s_sharedz_read.py:108`, `solve_budget` at `experiments/track_c/c10s_sharedz_read.py:137`, `solvefeas_cell1_outcome` at `experiments/track_c/c10s_sharedz_read.py:155`, and `reference_shift` at `experiments/track_c/c10s_sharedz_read.py:179`. They implement BUDGET-BINDING, FIT-PASSES-AT-25, qualified UNDERFIT-AT-50, NOISE-NON-DISCRIMINATING and REFERENCE-SHIFT. Underfit output prints each failing frame's evaluation-25 and final fit and keeps all applicable qualifications. Injection counts appear beside CORPUS/51's 51/69/54 canonical/shared/twin counts, explicitly labelled as a different template draw.

**Default equality against `1169794`:** the unset selector uses the original 25-step file and defaults; no extra snapshot forwards or engine-count hooks run; record schemas and the source-list membership are unchanged. Tests compare all 43,800 label combinations, representative whole verdicts/second-process states, settings bytes, identities, persisted records, halt diagnostics and source-list membership. The default shared-solver computational AST is identical after removing unreachable solvefeas diagnostics and empty provenance expansion. This verifies the model-free default path; model output equivalence was not run under the hard limit.

## Decisions where v2 was silent

1. **Output namespace:** `solvefeas` defaults to `results/c10s_solvefeas`, while `sharedz` retains `results/c10s_sharedz`. Existing `OUT_DIR` override and occupied-output refusals remain. This avoids touching step-1 output records.
2. **Default compatibility:** the new provenance fields, new hashed inputs and new observation hooks are emitted only for `solvefeas`. This preserves the default record schema as well as its numerical path. Every new-arm output, identity and solve diagnostic carries the selected path, SHA-256 and configured step count.
3. **Early objective stopping:** if a solve ends before evaluation 25, its returned state is also what a 25-step solve would have returned. The snapshot records the actual evaluation and `carried_forward: true`; no fictitious evaluations or extra optimization are performed. A run in which every solve ends at or below 25 is still INVALID.
4. **Plateau change:** interpret “fit changed by less than 0.002” as `abs(fit50 - fit40) < 0.002`. Equality is still-descending under the frozen otherwise rule. Objective stopping takes precedence, including at evaluation 50. Mixed underfit classes retain every qualification.
5. **Positive-control scope:** validate the cell-1 record and each completed harness process using their engine counts plus shared histories. An underfit second process checks its own observed solves before recording its permanent terminal outcome. Invalid or over-budget counts cannot satisfy validity.
6. **Nested engine counting:** temporarily rebind `memit_main.compute_z` as well as the harness entry inside LAW#5, because the reference engine edit bypasses the harness name. Preserve the existing harness target-capture wrapper and restore both bindings on every exit. The forward hook returns nothing and never replaces an activation or target.
7. **Reference shift:** persist REFERENCE-SHIFT in the pass and run, then halt nonzero using the arm's own halt path. A second-process shift is a permanent named outcome with its pass record; it is read as a finding rather than an INVALID. A1/A2 failures or missing/mismatched records remain INVALID. Replication and -LARGE-WRITE keep the original rules for otherwise valid write results.

## Verification

Run from the verified worktree; only the selftest/reader and isolated fixtures execute:

```sh
/opt/homebrew/bin/rtk proxy env LLMDB_ROOT="$PWD" CUDA_VISIBLE_DEVICES= PYTHONDONTWRITEBYTECODE=1 .venv/bin/python experiments/track_c/c10s_sharedz_selftest.py
```

Exit status **0**. The following output is copied verbatim from the final run:

```text
ok  test_overlap_table
ok  test_prompt_plan
ok  test_nll_reduction
ok  test_fit
ok  test_screen
ok  test_label
ok  test_gates
ok  test_verdict
ok  test_second_process_record
ok  test_a2_engine_parity_plans
ok  test_noise_twin
ok  test_arm_selector_and_config
ok  test_settings_before_import_and_hp_rebinding
ok  test_inertness_settings_binding
ok  test_second_process_settings_binding
ok  test_forward_counting_and_cleanup
ok  test_evaluation25_snapshot
ok  test_solvefeas_fit_labels
ok  test_underfit_class_boundaries
ok  test_solve_budget_positive_control
ok  test_solvefeas_noise_precedence
ok  test_reference_shift_boundaries
ok  test_solvefeas_replication_and_qualifiers
ok  test_source_hash_inputs
ok  test_injection_record_binding
ok  test_reader_record_interface
ok  test_default_records_1169794
ok  test_default_equality_1169794
C10S_SELFTEST_PASS (28 tests)
```

Compile command (exit **0**, no output; bytecode written under `/private/tmp`):

```sh
/opt/homebrew/bin/rtk proxy env LLMDB_ROOT="$PWD" PYTHONPYCACHEPREFIX=/private/tmp/c10s_solvefeas_compile .venv/bin/python -m py_compile experiments/track_c/c10s_sharedz_arms.py experiments/track_c/c10s_sharedz_inertness.py experiments/track_c/c10s_sharedz_read.py experiments/track_c/c10s_sharedz_selftest.py
```

The targeted `/usr/bin/git diff --check` returned **0** with no output. Read-only git checks reconfirmed the worktree and branch and showed no tracked changes in the protected engine, harness, CORPUS or step-1 results paths.

Session handoff: implementation and the requested model-free checks are complete. The preregistration's implementation advisor review and any subsequent model/inertness/driver run remain outside this brief and were not invoked. No experiment label has been promoted and no canonical tracker was changed by this task.
