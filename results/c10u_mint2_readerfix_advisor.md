FIX-FIRST

# D-C10u-mint2 reader/classification fix: independent adversarial review (delta, before r3)

Reviewer: Claude subagent, read-only. Scratch scripts are in `/Users/robertrhu/.claude/jobs/8ac4cacf/tmp/advisor_readerfix/` (`real_check.py`, `diffcheck.py`, `v2_noncomp.py`). No torch, no GPU.

**Verdict: FIX-FIRST, 1 BLOCKING.** The required fix from the prior Astra review is complete for block F, and it holds up on the real r2 data. One path is still open. In block V2, a non-admitted arm drops the prereg's -NOT-COMPARABLE arm qualifier.

**Most important next step:** in `block_reading`, run the V2 comparability screen before the non-admitted early return, so that NOT-COMPARABLE keeps precedence over ROUTING-BLOCKED-UNDERFIT (B1 below).

## Verified (evidence)

- **The packet diff matches the working tree.** I extracted the +/- lines from `git diff` for arms.py, read.py and selftest.py and compared them with the packet's fenced diff. `diff` printed `SAME`.
- **Selftest:** `.venv/bin/python -B experiments/track_c/c10u_mint2_selftest.py` gives `Ran 75 tests ... OK`.
- **(a) Real r2 data, using the new driver's record shape.** `real_check.py` builds the record the way `behavior_job` does (`c10u_mint2_arms.py:770-779`) from `results/c10u_mint2/r2/step0/F_r0_modifier_s0.json`:
  - `admission = {**step["admission"], "P2": step["P2"]}`
  - `step0 = step["probe"]`
  - `provenance = step["provenance"]`
  - `identity` and `fingerprint` come from the r2 record. These are equal to the sidecar's (`identity old==sidecar True fp old==sidecar True`).

  Results:
  - The sidecar has `outcome UNDERFIT`, P3 `n_ge_0.98: 17` with 24 fits, `P2.ok True`, and probe keys `minted_inventory, n_cannibal, recall_n, recall_rows, ...`.
  - `nonadmitted_validity(new) == []`, `_record_validity(new) == []`, `_population([new],"F",0)["reasons"] == []`.
  - After a JSON round trip the result is still `[]`.
  - **A valid record does not false-INVALID.**
  - The old r2 record fails closed: `["incomplete/malformed/invalid non-admitted record: 'P2'"]`, which is the expected result.
  - With the real r2 F records (multi plus mint1 s0–s2, each `run_validity == []`) plus the new UNDERFIT record, the block reads `INCOMPLETE`, as expected for 5 of 7 records. Positive-block coverage with 7 replicate-F jobs exists only on fixtures (`selftest test_nonadmitted_real_producer_record_retains_seven_replication_jobs`). A real-data positive block is UNVERIFIABLE because r2 halted at 5 records.
- **(b) The completed-run gate is not weakened.**
  - The `_material_validity` extraction is a verbatim move (the diff hunks are identical). Grepping `run_validity`'s remaining body (`c10u_mint2_read.py:219-280`) finds no orphaned `identity/provenance/hashes/pairing/context/fp` reference.
  - Differential test (`diffcheck.py`): HEAD `run_validity` against the new `run_validity` and `_record_validity`, over 3408 key-deletion and None mutations of the four real r2 DONE records. Result: `mismatch 0`.
  - An unknown or non-string outcome dispatches to `run_validity`, which requires `DONE` (`read.py:317-321`, `:214`).
  - Each UNDERFIT relaxation (pid freshness in `_replica_matches` `:333-335`, the executed-only PID set in `_population` `:449-451`) only applies when `nonadmitted_validity` holds. That function enforces `pid is None` and forbids the `arm/recipe/inertness/wrapper/values/minted_*` keys (`:288-289`). So a DONE run cannot reach these relaxations.
- **(c) No invented count.**
  - An UNDERFIT arm returns `{"label":"UNDERFIT","reasons":[],"replication_pending":False,"replica":...}` with no binding, raw or gain (`read.py:374-376`).
  - A block with a non-admitted arm skips `_range_direction` and leaves `raw_direction None` with no `ranges` (`:524-530`). The LEAD/PARTIAL replication and LARGE-WRITE paths short-circuit on `replica["candidate"]["outcome"] == "DONE"` (`:385`, `:398`). P4 selection skips UNDERFIT originals (`arms.py:950`).
- **(d) Prereg compliance.**
  - **:115 ("P3 screen < 22/24 → UNDERFIT, no behavioural run"):** met. `behavior_job` returns before `_started.json` or `load_harness` (`arms.py:770-779`). `nonadmitted_validity` recomputes P3 with `admission_reading` and requires it to fail (`read.py:296-297`).
  - **:72 (any mint arm underfit → block ROUTING-BLOCKED-UNDERFIT, no direction label):** met (`read.py:543-544`).
  - **:78 replication (any LEAD/PARTIAL is replicated):** met for F. `replication_pending` is taken from the executed arms (`:536`), consistent with §8 change 5 (`PREREG:179`).
  - **:78 V2 comparability clause:** NOT met. See B1.

## BLOCKING

**B1. A V2 block with a non-admitted arm skips the comparability screen, so its arm labels lose -NOT-COMPARABLE.**
- **Location:** `experiments/track_c/c10u_mint2_read.py:543-544`, where the `if nonadmitted: return ROUTING-BLOCKED-UNDERFIT` sits before the comparability check at `:545-550`.
- **Prereg requirement:** `docs/C10U_MINT2_PREREG.md:78` (scope as amended by §8 change 1, `:175`) says that on a comparability failure "its arm labels carry **-NOT-COMPARABLE**".
- **Scenario, reproduced by `v2_noncomp.py`:** a V2 block with mint-1 median 22 < 30 (a screen failure).
  - All DONE: the result is `NOT-COMPARABLE`, and every arm is `...-NOT-COMPARABLE`, e.g. `'mint2_s1': 'PARTIAL-NOT-REPLICATED-NOT-COMPARABLE'`.
  - Same block with mint2 s0 non-admitted: the result is `ROUTING-BLOCKED-UNDERFIT`, the arms are `'mint1_s1': 'PARTIAL-NOT-REPLICATED'` and `'mint2_s1': 'PARTIAL-NOT-REPLICATED'` with no qualifier, and `comparability_ok` is absent.
  - The pre-existing DONE per-position-underfit path checks comparability first (`:545-550` precede `:556-557`), so precedence is now inconsistent between the two underfit causes. This over-claims the V2 arm labels in the stage-complete record that the verdict is read from. It is reachable in r3's `v2` stage, since mint-2 is a 2-id target (UNDERFIT plausible) and V2 has no known baseline.
- **Sub-case:** when a V2 **mint-1** seed is non-admitted, the median-of-three screen cannot be evaluated. The reader silently returns ROUTING-BLOCKED-UNDERFIT, again without the qualifier (`v2_noncomp.py`: `'mint1_s0': 'UNDERFIT'`, the others are unqualified). Calling `_comparability` directly would raise KeyError on `["arm"]` (`:477-480`), so the fix must handle this case explicitly.
- **Exact fix:**
  1. Before `if nonadmitted:` (`:543`), compute `comparable`:
     - For block F, it is `True`.
     - For V2, use `all(_comparability(p) for p in (a, b) if p is not None)` when every `multi`/`mint1` record in those populations has `outcome == "DONE"`.
     - Otherwise set it `False` (unevaluable, fail-closed) and add a reason, e.g. `"comparability screen unevaluable: non-admitted mint-1"`.
  2. Set `out["comparability_ok"] = comparable`.
  3. If it is not comparable, append `-NOT-COMPARABLE` to every arm label and return `NOT-COMPARABLE`, matching the DONE-path precedence. Then let the non-admitted return follow.
  4. Keep `replication_pending` as it is. Both directions are already in the `control` blocked set (`:592`).
  5. Add selftests: a V2 block with m1=(20,22,24) and a non-admitted mint2 expects `NOT-COMPARABLE` with every arm label ending in `-NOT-COMPARABLE`; a non-admitted V2 mint1 expects `NOT-COMPARABLE` with the unevaluable reason.
  6. Record the unevaluable-median treatment as an interpretation in the decision ledger, because the prereg is silent on it.

## ADVISORY

1. **Prereg internal tension, to disclose.** `PREREG:90` (§3 Validity, "any failure → INVALID") lists "P3 admission screen", while `:115` and `:72` route a P3 failure to UNDERFIT and ROUTING-BLOCKED-UNDERFIT. The implementation follows :115/:72, as the prior review required. Cite this reconciliation in the D-C10u-mint2 ledger entry so the verdict is not read against :90. The I-11 case is consistent with :90: UNDERFIT plus I-11 exclusion leads to INVALID (`read.py:290`, `:296`).
2. **Published admission fields are not cross-checked.** `nonadmitted_validity` recomputes P3 from `fits` but does not require `admission["P3"]["ok"]`, `["n_ge_0.98"]`, `["underfit"]`, `admission["outcome"]` or `admission["excluded"]` to equal the recomputation (`read.py:293-298`). The record also does not embed the step0 sidecar's sha256, so a later change to the record's `fits` cannot be tied back to the sidecar. DONE records have the same gap, so the two are on par. Suggested fix: add `step0_sha256` in `behavior_job` (`arms.py:774`) and require `admission == admission_reading(p2, fits, step)` minus P2.
3. **Legibility.** A ROUTING-BLOCKED-UNDERFIT caused by an admission UNDERFIT returns `reasons: []`, and so does one caused by a per-position underfit. Suggest adding `"non-admitted: <arm>"` to `reasons` so the stage-complete JSON says which arm and which cause.
4. **P4 from a routing-blocked block (pre-existing, unchanged).** `p4_configurations` (`arms.py:945`) does not skip `ROUTING-BLOCKED-UNDERFIT`, so a replicated LEAD/PARTIAL DONE modifier or mint2 seed in a blocked block can go to P4. That is consistent with per-arm labels being per-configuration (`PREREG:92`). Confirm this is intended.
5. **UNVERIFIABLE on real data:** the V2 mint2 and mint1_48 non-admitted records (the `_p2_record_validity` bigram-720 path, `read.py:177-178`). No V2 step0 sidecar exists yet, and only fixture coverage exists (`selftest test_nonadmitted_v2_keeps_replication_and_blocks_control`).
6. **Mint-1 UNDERFIT in block F leads to HALT.** The driver halts through `reproduction_or_halt` (`arms.py:923-932`), and the reader returns HALT-LAW3 (`read.py:538-542`). This is consistent with LAW#3 (`PREREG:77`, §8 `:172`). Note that under §8 `:172` ("r2 is the last attempt") any r3 needs a recorded operator ruling. UNVERIFIABLE here whether that ruling exists.
