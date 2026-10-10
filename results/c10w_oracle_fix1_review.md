VERDICT: PROCEED

# D-C10w-oracle fix round 1: independent implementation review

Reviewer: Claude Opus 5.5 (independent; not the implementer, not the prior advisor). Date: 2026-10-07.
Code under review: the uncommitted diff against HEAD f3a9a8a of `experiments/track_c/c10w_oracle_{step0,train,eval,read,selftest}.py`, plus the new `c10w_oracle_torchcheck.py`.
Spec: `docs/C10W_ORACLE_PREREG.md`, FROZEN v2.2.
Inputs: `results/c10w_oracle_advisor_impl.md` (prior review: B1–B4, A1–A4), `results/c10w_oracle_codex_fix1.md` (implementer report), and the two briefs.
I edited only this file in the worktree. All mutation work ran in `/Users/robertrhu/.claude/jobs/8ac4cacf/tmp/c10w_mut_r2/`.

## BLOCKING

None. Each of B1–B4 is fixed, and a test fails when the fix is reverted (table below). I found no new false-HALT or false-INVALID path for a legitimate run, and no weakened gate. The implementer's counts match my reproduction: 63 selftests, 3 torchcheck tests, and 48/49 for the original mutant set.

## Item-by-item (fix → enforcing test → revert mutant result)

| Item | Fix (file:line) | Enforcing test(s) | Revert in mirror |
|---|---|---|---|
| B1 signed zeros | `eval.py:113–114`: `d16=delta.to(...)`; `weight.copy_(torch.where(d16==0,weight,weight+d16))` | `torchcheck.py:29,35,41`, which exec the production statements AST-extracted from `eval.py` | N02 (`add_` restored), N01 (guard dropped) and N03 (guard inverted) are all KILLED by torchcheck, but **not** by the selftest (see A-5) |
| B2 G3 float boundary | `read.py:264`, in integer hundredths | `selftest.py:981` (DefectTests), `:994` | N06 (old float rule restored), M07, N04 and N05 all KILLED |
| B3 eval-stage projection | `step0.py:303–312` (shared `guard_phase_projection`), `:393–394` (before `run_child`) | `selftest.py:1039`, `:1049` (516 > 465 refuses; 465.00 proceeds; failed attempts are charged) | N07 (guard dropped), N08 (spent ignored), N12 (guard after child), N09 and N10 all KILLED |
| B4 evidence on HALT/INVALID | `eval.py:368–465` (try/except writes `eval_halt.json`), `:456–457` (`eval.json` written before `validate_phase`), `:466–469` (`my_edit`/hooks restored); `step0.py:399–406` (p1-project uses the reader; INVALID → rc 2, no projection) | `selftest.py:1151,1172,1189,1205,1219,1231,1244` | N13 (validate before write), N14, N15, N17–N20, N22–N27 KILLED; **N16 and N21 SURVIVE** (test gaps, see A-1 and A-2) |
| A1 tracer cost | `eval.py:319–320` | `selftest.py:1253` | N28, N29 and N30 KILLED |
| A2 null "after" hash | `eval.py:240` (hash taken before `assert_base`/restore), `:248` | `selftest.py:1276`; ProposedTests null tests | N31 (vacuous `after_hash`) and M40 (re-anchored) KILLED |
| A3 HF env before import | `train.py:148–151` | `selftest.py:1298` | N32 and N33 KILLED |
| A4 P1 ruling identity | `step0.py:309–311` | `selftest.py:1053,1068` | N34, N35, N36 and N37 KILLED |

**Settled fact, checked against the code on the real checkpoint (CPU, no MPS).** I loaded `down_proj` for L4–L8 from the pinned snapshot (`3aab1f19…`, bf16) and cast it to fp16, then ran the **production merge statements**, imported through `torchcheck.merge`, which AST-extracts them from `eval.py`.
- `-0.0` counts are L4 21, L5 9, L6 2, L7 4, L8 0. This matches the settled fact.
- Old `add_` with zeros: SHA changes on L4–L7 and is unchanged on L8. This is the positive control.
- Production merge with a zero delta: SHA is byte-identical on all five layers.
- A nonzero delta entry (0.5) is applied bit-exactly. A sub-half-subnormal delta (−2⁻²⁶) rounds to fp16 zero and leaves the weight bits unchanged.

The P1 preflight therefore no longer false-HALTs at LAW#5(ii). The change is behaviourally inert for trained adapters, because the only entries it treats differently are those where the fp16 delta is exactly ±0.

## New false-HALT / false-INVALID / weakened-gate check

- **A3 `HF_HUB_OFFLINE=1` (a new trainer environment) cannot false-HALT.** With `HF_HOME=<worktree>/hf_cache` and offline mode, `AutoTokenizer` and `AutoConfig` load at `MODEL_REV`. `config._commit_hash == MODEL_REV` is True, so the check at `train.py:169` holds. `cached_file` resolves the index, both safetensors shards and the generation config. The cache has no `refs/` directory; offline resolution works because the revision is a full commit hash.
- **The B2 rule is exact.** I swept every reference value from 3.00 to 100.00 in hundredths, with the arm at A−3−0.01, A−3 and A−3+0.01: 29,103 cases. The new rule has 0 errors; the old rule had 413. Its input is already rounded to 2 dp at source (`c10e_bandknob.py:163`), so `round(x*100)` is exact.
- **B3 does not false-HALT a within-budget run.** At the eval stage, pending is empty once every unit is fitted. The projection is preflight + spent (retries charged in full) + the phase eval constant. This matches §2.9:312–314. Equality to 465, 448 or 327 passes, and +0.01 refuses (`selftest.py:1039`). For P2/P3, the limit comes from the same `authorization_P{2,3}.json` that `ensure_authorized` validated.
- **B4 / p1-project leaves no route to P2 from an INVALID P1.** An INVALID `verdict.json` has no `projection`, so `ensure_authorized` (`step0.py:328`) raises on `verdict["projection"]` before any P2 directory is created.
- **No gate was weakened.** Every reader check (`validate_phase`, `read_measurement`) is unchanged apart from the G3 arithmetic. `eval.json` is now written before validation, but the reader re-runs `validate_phase` on whatever it loads (`read.py:414`).

## ADVISORY

- **A-1. Test gap (N16 survives): a failure inside `null()` is not tested for preserving the null evidence.** `eval.py:463` records `law5_null=getattr(e,"null_evidence",null)`. Replacing it with `null` passes every test, because once `null()` returns, `null` *is* `e.null_evidence`. The two differ only when `null()` raises mid-way, which is exactly the B1/A2 scenario: the zero application changes the band, and `assert_base` at `eval.py:241` raises. That is the case where `after_hash` is the "offending output" CLAUDE.md requires in the diagnostic. The code is correct; only the test is missing. Suggested test: a FakeEvaluator whose `null()` sets `null_evidence={"base_hash":X,"after_hash":Y}` and then raises. Assert that `eval_halt.json["law5_null"]["after_hash"]==Y`. This does not change any gate outcome.
- **A-2. Test gap (N21 survives), plus a misleading on-disk status.**
  - No test asserts `eval_halt.json["status"]=="HALT"`.
  - Separately, `eval.json` is written at `eval.py:456` with `"status":"PASS"` and every `validity` flag True *before* `validate_phase`. A validity failure therefore leaves a PASS-labelled `eval.json` in a HALTed directory.
  - `disk_phases` (`read.py:583`) selects the latest P2/P3 directory that has an `eval.json` and does not check `HALT.json`. A HALTed P2/P3 eval is therefore now pulled into the final read.
  - Outcome: the reader re-validates and returns INVALID, so there is no false label. It is a new on-disk state nonetheless.
  - Suggested fixes: assert the halt status, and either write `eval.json` with `"status":"UNVALIDATED"` and record the validation result in `eval_halt.json`/`verdict.json`, or have `disk_phases` refuse HALTed directories.
- **A-3. The reader's INVALID label is unreachable through the dispatcher for eval-stage validity failures.** For example, a positive control at 67/72 (`selftest.py:1172` asserts that the eval process *raises*). The sequence is: the eval child exits 2, then `step0.py:397` raises, then `HALT.json` is written. After that, both `p1-project` and `read` refuse the directory through `latest_directory` (`read.py:479`). The evidence survives in `eval.json` and `eval_halt.json`, and the terminal outcome matches §3 (no label, no routing), but the pipeline reports these as HALT, never as a reader-computed INVALID verdict. The `p1-project` INVALID branch (`step0.py:402–406`) is reachable only when a record passes the in-process `validate_phase` but fails a later reader check. Worth one line in the operator runbook.
- **A-4. A budget refusal at `p1-eval` permanently blocks the P1 directory.** `guard_phase_projection` raises inside `dispatch_stage`, which writes `HALT.json` (`step0.py:411`), and `latest_directory` refuses that directory from then on. A budget ruling recorded *after* the refusal can therefore never resume it; all five trainings would have to be redone in a fresh P1. The ruling works only if it is pre-placed as `<p1>/authorization_P1.json` before `p1-eval`. This was already true of the training guard. B3 extends it to the most expensive point. Recommendation: if the measured projection approaches 465 after the trainings, the operator should record the P1 ruling before dispatching `p1-eval`.
- **A-5. The torchcheck is not wired in.** `c10w_oracle_torchcheck.py` is referenced by no launcher, selftest or tool (`grep -rln torchcheck experiments tools docs` finds nothing). It is the *only* test that kills N01, N02 and N03 (the selftest's `NoModelImports` forbids torch). Run it in the pre-run checklist next to the selftest.
- **A-6. The P2/P3 `budget_minutes` path at the eval stage is tested only through P1.** N11 (budget ignored) is killed only by the P1 identity test. A P2 case with a recorded budget above 448 and a projection between the two would pin it.
- **A-7. M49 still survives.** It is the equivalent mutant from the prior review: the trainer's in-process LAW#3 recheck is redundant with `read.py:553`.

## Mutation testing

Harness: `/Users/robertrhu/.claude/jobs/8ac4cacf/tmp/c10w_mut_r2/mutate.py`.
- It is a copy of `c10w_mut/mutate.py` (that directory was not modified), with `BASE` set to the new directory and `SELFTEST_SRC` set to `pristine/c10w_oracle_selftest.py`, the current suite.
- `pristine/` and `root/` were populated from the current worktree files by `c10w_mut_r2_setup.sh`. The layout mirrors the old root: 43 top-level entries; real copies of the six `c10w_oracle_*.py` files and `run_c10w_stage.sh`; everything else is a symlink.
- **Anchor hardening.** The harness pre-validates every mutant before running any of them. It raises `RuntimeError` if any `old` string does not occur exactly once, or if the mutated file equals pristine.
  - Positive control: an old-code M07 anchor raised `occurs 0 times`.
- Exactly two old anchors had gone stale. I re-anchored each with the same semantic mutation:
  - M07: G3 `>=` → `>` on the new hundredths expression.
  - M40: drop the `assert_base()` that now follows the new `null_evidence` line, at `eval.py:241`.
- The other 47 matched once each, at lines that hold the intended code; the line numbers are printed per mutant in `run_r2.tsv`.
- Each mutant runs both the selftest and the torchcheck.

| Set | Total | Killed | Survived |
|---|---|---|---|
| Prior review, original suite (for reference) | 49 | 24 | 25 |
| Old 49, current suite (M07/M40 re-anchored) | 49 | 48 | 1 (M49: equivalent, A-7) |
| New N01–N37 (B1–B4, A1–A4 paths) | 37 | 35 | 2 (N16, N21: real test gaps on diagnostic content only; A-1, A-2) |
| **All** | **86** | **83** | **3** |

BASELINE passed before and after (`BASELINE_POST SURVIVED`, meaning the unmutated suite passes). No survivor changes a gate, label, routing or HALT outcome.

## Evidence (commands → short outputs)

- **Selftest:** `LLMDB_ROOT=$PWD .venv/bin/python -B experiments/track_c/c10w_oracle_selftest.py` → `Ran 63 tests … OK — C10W_ORACLE_SELFTEST PASS: 63 tests`.
- **Torchcheck:** `.venv/bin/python -B experiments/track_c/c10w_oracle_torchcheck.py` → `Ran 3 tests … OK`.
- **Mirror identity:** the setup script prints `<stem> identical to worktree` for read, step0, train, eval, selftest and torchcheck.
- **Mutation run:** `.venv/bin/python -I -B c10w_mut_r2/mutate.py > run_r2.tsv` → `ANCHORS_OK 86` … `RESULT killed=83 survived=3 total=86`.
- **Real-checkpoint B1 output** (production merge via `torchcheck.merge`; hash prefixes are fp16 SHA-256):
  ```
  L4 -0.0=21 base=93ea6623ddba add_zero=608e28667d15 same=False | prod_merge_zero=93ea6623ddba same=True | nonzero_applied_exact=True
  L5 -0.0=9  base=5c4426a94f4d add_zero=904da891be21 same=False | prod_merge_zero=5c4426a94f4d same=True | nonzero_applied_exact=True
  L6 -0.0=2  base=eaede89b0795 add_zero=72112d09f499 same=False | prod_merge_zero=eaede89b0795 same=True | nonzero_applied_exact=True
  L7 -0.0=4  base=6c058e06ac76 add_zero=ac23cb056c15 same=False | prod_merge_zero=6c058e06ac76 same=True | nonzero_applied_exact=True
  L8 -0.0=0  base=c0e9868081ca add_zero=c0e9868081ca same=True  | prod_merge_zero=c0e9868081ca same=True | nonzero_applied_exact=True
  ```
- **A3 offline load:** `HF_HOME=$PWD/hf_cache HF_HUB_OFFLINE=1` with AutoTokenizer, AutoConfig and `cached_file` → `tok ok Qwen2TokenizerFast`, `config _commit_hash == REV: True`, and all four weight/config files resolved.
- **G3 sweep:** `cases 29103 new_rule_errors 0 old_rule_errors 413`.
- **Scratch:** `/Users/robertrhu/.claude/jobs/8ac4cacf/tmp/c10w_mut_r2/`, containing `mutate.py`, `mutate_old_copy.py`, `run_r2.tsv`, `pristine/` and `root/`; the setup script is `/Users/robertrhu/.claude/jobs/8ac4cacf/tmp/c10w_mut_r2_setup.sh`.
