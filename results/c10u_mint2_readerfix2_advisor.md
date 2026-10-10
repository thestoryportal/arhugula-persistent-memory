VERDICT: PROCEED

# D-C10u-mint2 reader fix, round 2: independent delta review (Claude advisor, read-only)

Scope: the round-2 change to `experiments/track_c/c10u_mint2_read.py`, plus `c10u_mint2_arms.py` and `c10u_mint2_selftest.py` (uncommitted, compared with HEAD `f3a9a8a`). The only file written is this report. Throwaway scripts are in `/private/tmp/claude-501/advisor_c10u_r2/`: `real_producer.py`, `scenarios.py`, `mutdiff.py`, `underfit_sweep.py`, plus `read_head.py`, which is `git show HEAD:` of the reader. No torch, model or GPU was used.

**Most important next step:** none of the findings block r3. Before launch, write the "unestablished mint-1 median leads to NOT-COMPARABLE" interpretation into the D-C10u-mint2 decision ledger (ADVISORY A1), because the prereg is silent on it.

## BLOCKING

None.

The round-1 BLOCKING item, B1 (an UNDERFIT routing return placed before the V2 comparability gate), is closed. The evidence is under Q1 below.

## ADVISORY

- **A1. Ledger the interpretation (carried over from round-1 B1 step 6; not done).**
  - `_comparability` (`c10u_mint2_read.py:476`) returns False when any multi or mint-1 record is not DONE. A legitimately non-admitted V2 mint-1 seed therefore makes the block NOT-COMPARABLE.
  - That is fail-closed and consistent with the wording of `PREREG:78` ("not a halt, not a claim the stimuli are invalid"). But `:78` defines the screen as the "median of the three", and it does not cover the case where one of the three has no count. Record this as a declared interpretation in runbook §5, under the D-C10u-mint2 entry.
  - The implementer's report does not mention a ledger entry. A grep for "unestablished/unevaluable" across `EXPERIMENT_RUNBOOK.md`, `SESSION_CHECKPOINT.md` and the prereg finds nothing.

- **A2. Some published admission fields are still not cross-checked (partial A2).**
  - The fields that are now checked hold, both on the real-producer record and on fixtures:
    - `P3.ok is False` (`:299`)
    - `n_ge_0.98` must be an int equal to the recomputed value (`:300`); floats and `True` are rejected
    - `admission.outcome == "UNDERFIT"` (`:301`)
  - Still not checked on the real-producer record (deleting or nulling each one leaves `nonadmitted_validity == []`):
    - `admission.P3.underfit`
    - `admission.excluded`
    - `admission.reasons`
    - `step0.no_i11_exclusion`
    - `admission.P2.wordlist_replay`
    - `provenance.row_pairing.{applied_rows_sha256,n_rows,seed}`
    - `step0_file`
    - `decision_id`
  - None of these feeds a count or a gate. The P3 count and I-11 are recomputed from `fits`, `recall_rows` and `minted_inventory`.
  - There is still no `step0_sha256` that would tie the record's `fits` back to the sidecar. This is the same gap DONE records have, as noted in round 1.

- **A3. Legibility is still incomplete (partial A3).**
  - ROUTING-BLOCKED-UNDERFIT now names every arm and cause. Verified: `['mint2_s0 r0: admission UNDERFIT n_ge_0.98=17/24', 'mint2_s0 r1: ...']` and `['mint1_s1 r0: per-position underfit']`.
  - Two other paths still give no specific reason:
    - (a) NOT-COMPARABLE from a **DONE** screen miss (multi envelope or mint-1 median) has `reasons == []`. `scenarios.py` Q1b and Q1c both print `reasons=[]`. The failing quantity (the multi window key, or the median value) is not reported.
    - (b) A legitimately non-admitted F mint-1 gives HALT-LAW3 with the generic reason `"LAW#3 seed runs invalid or source/context/data/process differs"` (`:420`). It does not name `mint1_s1 r0: admission UNDERFIT`. The HALT itself is correct under `PREREG:77/:172`. Only the diagnostic text is generic.

- **A4. A non-admitted control drops the main block's raw ranges.**
  - `nonadmitted` (`:529`) is computed over `(a, b, ctl)`, but `_range_direction` only reads `a` and `b`.
  - Case: a V2 block that is all-DONE and SPAN-DIRECTION, plus a `mint1_48 s1` UNDERFIT control. The result is `ROUTING-BLOCKED-UNDERFIT` (the correct precedence, the same as HEAD's per-position control underfit), but `raw_direction=None` and `ranges` is absent (`scenarios.py` Q1d).
  - HEAD's DONE per-position path keeps `raw_direction=SPAN-DIRECTION` and the ranges. The measurement is computable, and dropping it from the durable `*_complete.json` loses the "measurements are retained" record (`:78`).
  - Suggested fix: compute `nonadmitted` over `(a, b)` only.
  - This does not change any verdict. The control stage can only be reached after a comparable SPAN reading.

- **A5. A mixed DONE/UNDERFIT replication pair for the same seed is accepted as legitimate.**
  - `_replica_matches` (`:337`) relaxes the pid-freshness check when either side is UNDERFIT. `test_nonadmitted_replication_pairs_record_underfit_done_in_both_directions` asserts that this mix reads cleanly: original DONE plus replica UNDERFIT gives `LEAD-NOT-REPLICATED` with a count.
  - The real producer cannot produce this mix. The original and the replica both resolve to the same `step0/<block>_r0_<kind>_s<seed>.json` (`arms.py:770`, `require_step0`), so their outcomes must agree. A mix therefore means a changed sidecar or a swapped record.
  - Both resulting labels are conservative (NOT-REPLICATED, or no count), so this is not blocking. Requiring `a["outcome"] == b["outcome"]` would turn the mix into INVALID ("replication material differs"), which would be more faithful.

- **A6. P4 selection from a comparable ROUTING-BLOCKED-UNDERFIT block (carried over from round 1, item 4; now asserted by a test).**
  - V2 with mint2 s0 UNDERFIT and comparable selects `('V2','mint2',1), ('V2','mint2',2)` for P4 (`scenarios.py` Q1a). F with modifier s0 UNDERFIT selects modifier 1 and 2 (Q1e).
  - This is consistent with per-configuration labels (`PREREG:86`, `:92`), and these seeds carry unqualified replicated LEAD labels. They are not "unqualified seeds".
  - The operator should still confirm that P4 on a direction-blocked block is intended.

## Q1. Is the BLOCKING item closed? Yes.

- **Precedence.**
  - `block_reading` now runs the gates in this order:
    1. population validity
    2. completeness
    3. pairing / replica match / control pairing
    4. LAW#3 for F (`:542-546`)
    5. comparability (`:548-556`)
    6. underfit routing (`:559-567`)
    7. locality
  - This is the same order HEAD used for DONE per-position underfit. So every gate that came before the routing return in HEAD still comes before it for UNDERFIT-routed blocks.
  - `_comparability` fails closed before it reads any count (`:476`).
- **-NOT-COMPARABLE is never dropped.** `scenarios.py` covers:
  - Q1b: mint-1 median 21 with mint2 UNDERFIT in r0 and r1. Result `NOT-COMPARABLE`, all labels `...-NOT-COMPARABLE` (`'mint2_s0': 'UNDERFIT-NOT-COMPARABLE'`), `all qualified: True`.
  - Q1c: multi ref 19 (outside the envelope) with mint2 UNDERFIT in the replica only. `NOT-COMPARABLE`, `all qualified: True`.
  - The only V2 paths that return before the comparability gate are INVALID and INCOMPLETE, and both carry no arm labels.
- **No unqualified seed reaches P4.**
  - `p4_configurations` skips a NOT-COMPARABLE block (`arms.py:945`). In Q1b, P4 selected only the F modifier seeds and no V2 seed. In Q2a, V2 alone was refused: `P4 requires replicated LEAD/PARTIAL ...`.
  - UNDERFIT originals are skipped (`arms.py:950`).
- **UNDERFIT-record mutation sweep (`underfit_sweep.py`).**
  - Ran 489 + 470 + 454 leaf mutations on the UNDERFIT record inside a V2 mint2 block, an F modifier block and a V2 mint1 block. 0 raised exceptions.
  - The only fields whose mutation did not lead to INVALID were the unchecked bookkeeping fields listed in A2, plus fields not required for that kind (for example `bigram_rows` for non-mint2) or fits mutations that legitimately keep n<22.
  - Material, P2, pairing, replica, row-pairing and context mutations all gave INVALID. These are also covered by the selftest tests `test_nonadmitted_keeps_material_and_p2_audits` and `..._replication_still_rejects_material_and_init_mismatches`.

## Q2. Does the fail-closed path cause a false HALT or INVALID on a legitimate r3? No.

I constructed a **legitimately non-admitted V2 mint-1 s0** (`scenarios.py` Q2a, with the screen otherwise passing):

- **v2 stage reading:**
  - The result is `NOT-COMPARABLE`, which is not INVALID or HALT.
  - `reasons=['comparability screen unestablished: mint1_s0 r0 is not DONE']`.
  - The labels are `UNDERFIT-NOT-COMPARABLE` and `LEAD-NOT-REPLICATED-NOT-COMPARABLE`.
  - `replication_pending=True`.
  - `stage_plan` sizes: `replicate-V2: 7`, `control: 0`.
- **replicate-V2:** the replica mint1 s0 is also UNDERFIT (shared sidecar). The result is `NOT-COMPARABLE` with both replicates named in `reasons`, and no INVALID. The pid check covers executed runs only (`:449-451`), and the pid relaxation in `_replica_matches` applies.
- **p4-save:** the V2 seeds are skipped and the F seeds are still selected. With no F candidates, `ValueError` is raised before any marker is written. That is the existing "stage unnecessary" refusal, not a halt.
- **Q2b:** the same case but with the other mint-1 seeds NULL. `replicate-V2` plan = 0, so the stage is refused as unnecessary. That is correct: no LEAD/PARTIAL, and no direction label to replicate (`:179`).
- **Other stages checked:**
  - `frozen`: an F modifier UNDERFIT gives ROUTING-BLOCKED-UNDERFIT and 7 replicate-F jobs.
  - `control`: the `mint1_48` UNDERFIT case raised nothing (no NameError on `raw`, Q1d).
  - An F mint-1 UNDERFIT gives HALT-LAW3. That is correct under LAW#3 and `PREREG:77/:172`, not a false halt (see A3b for the reason text).
- The driver's `stages()` (`arms.py:980-1033`) only halts through `reproduction_or_halt` (F mint-1/multi) and `spawn_job` failures. The non-admitted child prints a log line (`arms.py:778`), which the selftest confirms. No new halt path was introduced.

## Q3. Did any completed-run (DONE) gate weaken? No.

- **Differential against HEAD (`mutdiff.py 2500`).**
  - Ran 14,971 random leaf mutations (delete, None, ±1, bool flip, string change, outcome set to UNDERFIT/DONE) across 6 all-DONE scenarios: V2 comparable a and a+b, V2 median-fail, V2 span+control, F LEAD a+b, and F null.
  - Results: **0 verdict-level differences.** The comparison covered direction, every arm label, `comparability_ok`, `replication_pending`, `controls_pending`, `raw_direction` and `ranges`. There were also 0 `stage_plan` differences (replicate-F, replicate-V2, control) and 0 sampled `p4_configurations` differences (HEAD's reader against the new one, driving the same selector).
  - All 47 differences were reasons-text only, in two expected kinds:
    - the A3 naming, e.g. `[] -> ['mint2_s0 r0: per-position underfit']`
    - a DONE record with `outcome` set to UNDERFIT, which is still INVALID but now through `nonadmitted_validity`
- **No invented count.**
  - UNDERFIT arms carry no `binding/raw/gain/masked_binding`. Blocks with an UNDERFIT record skip `_range_direction` (`:529-536`).
  - The LEAD replication and LARGE-WRITE checks short-circuit on `outcome == "DONE"`.
  - The NOT-COMPARABLE reason strings contain arm names only, no counts.

## Q4. Are A2/A3 correct, and does the real producer's record still pass? Yes.

- **Real producer.** `real_producer.py` patches `read_context`, `require_step0` and `IDENTITY` to return the **real r2 sidecar** `results/c10u_mint2/r2/step0/F_r0_modifier_s0.json`, then runs the actual `behavior_job` non-admitted branch.
  - Unlike the selftest, it does not feed `behavior_job` a fixture-shaped `step`. The selftest's `test_nonadmitted_real_producer_record_retains_seven_replication_jobs` does run the real branch, but with fixture admission and probe dicts.
  - The sidecar shows `outcome UNDERFIT`, `P3 ok False`, `n 17`, `adm.outcome UNDERFIT`.
  - The producer logged `BEHAVIOR F_r0_modifier_s0: no behavioral run; step0 outcome=UNDERFIT`.
  - `nonadmitted_validity(rec) == []` and `_population([rec],"F",0)["reasons"] == []`.
- **A2 mutations on that real record:**
  - n−1, `ok=True`, `outcome=ADMITTED`, n as a float, n as `True`, a missing `ok`, and one fit raised from 0.97 to 0.99 all give INVALID.
  - `underfit=[]` and `excluded=True` pass. These are the unchecked fields listed in A2.
- **Not testable on real data:** a real-data positive 7-record block. r2 halted at 5 records, as in round 1. A real fixture-mixed block correctly gives INVALID ("block source/context/data hashes differ") with no crash.

## Evidence run

```
$ .venv/bin/python -B experiments/track_c/c10u_mint2_selftest.py
Ran 83 tests in 2.069s
OK

# The packet diff matches the working tree (+/- lines of arms/read/selftest)
cmp wt.txt pk.txt -> SAME (468 lines each)

$ .venv/bin/python -B /private/tmp/claude-501/advisor_c10u_r2/real_producer.py
sidecar outcome UNDERFIT P3 ok False n 17 adm.outcome UNDERFIT
log: BEHAVIOR F_r0_modifier_s0: no behavioral run; step0 outcome=UNDERFIT
nonadmitted_validity(real-producer rec) = []
_population = []
mutate n-1 -> published non-admitted P3 count differs
mutate ok True -> published non-admitted P3 gate differs
mutate outcome ADMITTED -> published admission outcome differs
mutate underfit list wrong -> []      (A2)
mutate excluded True -> []            (A2)

$ .venv/bin/python -B /private/tmp/claude-501/advisor_c10u_r2/scenarios.py   (excerpt)
Q2a V2 r0 only: dir=NOT-COMPARABLE comp=False repl_pending=True
    reasons=['comparability screen unestablished: mint1_s0 r0 is not DONE']
    stage_plan sizes={'replicate-F': 0, 'replicate-V2': 7, 'control': 0}
Q1a V2 r0+r1: dir=ROUTING-BLOCKED-UNDERFIT comp=True; reasons name mint2_s0 r0 and r1
Q1b V2 r0+r1: dir=NOT-COMPARABLE, all qualified: True; P4 selected only F seeds; reasons=[] (A3a)
Q1c V2: dir=NOT-COMPARABLE, all qualified: True
Q1d V2 + control mint1_48 s1 UNDERFIT: dir=ROUTING-BLOCKED-UNDERFIT raw=None (A4)
Q2c F r0 mint1 UNDERFIT: dir=HALT-LAW3 reasons=['LAW#3 seed runs invalid or ...'] (A3b)
Q1e F: dir=ROUTING-BLOCKED-UNDERFIT; P4 selected [('F','modifier',1), ('F','modifier',2)]

$ .venv/bin/python -B /private/tmp/claude-501/advisor_c10u_r2/mutdiff.py 2500
total 14971 mutations; VERDICT-LEVEL diffs: 0; reason-only diffs: 47 (expected kinds);
stage_plan diffs: 0; p4 diffs (sampled): 0

$ .venv/bin/python -B /private/tmp/claude-501/advisor_c10u_r2/underfit_sweep.py
V2 mint2 UNDERFIT: 489 mutations, 0 raised; non-INVALID only for unchecked bookkeeping/benign fits
F modifier UNDERFIT: 470 mutations, 0 raised; same
V2 mint1 UNDERFIT: 454 mutations, 0 raised; same (stays NOT-COMPARABLE)
```
