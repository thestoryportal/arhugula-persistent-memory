VERDICT: SKIP-REPLICATE-V2-WITH-CONDITIONS

Advisor review, step 3 (D-C10u-mint2) r3, `replicate-V2` run/skip. Read-only; no GPU, no process started. Line numbers are from the files as of 2026-10-07. The packet's line numbers are about 3 lines low for `block_reading` (actual :492) and `stage_plan` (actual :601). `p4_configurations` is at `c10u_mint2_arms.py:935–958`, not :980–1000.

## 1. Run or skip `replicate-V2`: SKIP, recorded as a program ruling that deviates from the prereg. It is not a reading of the existing text. (BLOCKING conditions C1–C3)

Evidence that no replica outcome can change any V2 output that is used for a decision:
- Direction. `block_reading` sets `comparable = ... all(_comparability(p) for p in (a, b) ...)` (`c10u_mint2_read.py:548`). The first block fails, and it fails on two keys, not one: V2 multi `para_full_n` 31 ∉ [5, 18] **and** `canon_full_n` 24 ∉ [5, 10] (`results/c10u_mint2/r3/V2_r0_multi_snone.json`; window at `read.py:21`). So V2 is NOT-COMPARABLE whatever block b contains (`:550–555`).
- The block is also blocked a second way. Even if comparable, mint-2 s1/s2 are admission UNDERFIT (20/24 and 21/24 at ≥ 0.98) and s0 has `all_positions_fit` false (Fluvane). That routes the block to ROUTING-BLOCKED-UNDERFIT (`read.py:559–567`). A replica cannot clear it, because replicas reuse the r0 step 0 (`arms.py:770`, `record_name(block, 0, ...)`), so the UNDERFIT outcomes recur by construction with no behavioral run (`arms.py:778`).
- Arm labels. A replica only adjusts LEAD/PARTIAL (`read.py:387–392`). V2 mint-2 is TRADEOFF/UNDERFIT, so its labels cannot move. Only mint-1 could change, from `LEAD-NOT-REPLICATED-NOT-COMPARABLE` to `LEAD-NOT-COMPARABLE`. Nothing consumes that change: P4 skips NOT-COMPARABLE blocks (`arms.py:945`) and selects only mint-2/modifier kinds (`arms.py:938`), and the prereg limits P4 to mint-2/arm-B LEAD/PARTIAL (`PREREG:86`).

Why skipping is a deviation and not a reading of the text:
- §8 change 5 says plainly: "Replication triggers are unchanged: the mint-1 reference arms (LEAD by the median ≥ 30 rule) and any direction label ... still trigger replication blocks" (`PREREG:179`). The V2 mint-1 median is 46 ≥ 30, so the letter of the prereg triggers replicate-V2. The coded schedule agrees (`read.py:620` plans it whenever `replication_pending` is true).
- :78 does not exempt a NOT-COMPARABLE block from replication. It suspends the direction reading "pending a diagnosis" and does not name a replica as that diagnosis (`PREREG:78`).
- Calling the skip "no trigger, because the labels are NOT-COMPARABLE-suffixed" would be a post-data reinterpretation. Record it as a ruling and disclose it.

Diagnostic value of the replica: low, and it is not the diagnosis :78 asks for.
- The replica would re-measure 31 and 24 in a fresh process. The prereg treats the replica as measuring the ±4–5 process envelope (`PREREG:78`). Moving into the window would need a swing of ≥ 13 on para_full and ≥ 14/24 on canon, roughly 3× that envelope.
- The diagnosis is available offline at zero GPU cost from the existing records: pre-write recall is 0, para_first is 49 (inside [42, 59]), but canon is 24/24 against block F's 8/24. The string route lands V2's multi-token values far more easily than the frozen ones.
- What the replica would actually add is the process envelope for the mint-1(V2) seeds (51/46/38) and for the 31. Nothing downstream reads either. Real cost is 5 behavioral runs (multi, mint-1 ×3, mint-2 s0), not 7, because s1/s2 make no run.

Conditions:
- **C1 (BLOCKING): do not edit `docs/C10U_MINT2_PREREG.md` or `c10u_mint2_read.py` while any r3 stage is live.**
  - Both files are in the r3 source-identity pin (`results/c10u_mint2/r3/identity.json` `source_sha256`).
  - Every `_job` child calls `initialise_identity` → `assert_sources` (`arms.py:1088`, `:140`, `:89–94`), as do the stage-level checks (`:682`, `:741`, `:864`, `:901`).
  - A deviation note appended to the prereg now would make the next replicate-F child raise "frozen source identity differs".
  - Record the ruling now in runbook §5.2/§13 as a D-ID (e.g. D-C10u-r3-skipV2), which is not pinned. Add the prereg §8 deviation note only after r3's last stage has ended, marked as written after the V2 data was seen.
- **C2 (BLOCKING): the ruling must explicitly waive V2 `replication_pending: true` and state the closed reading.**
  - Without replicate-V2 the V2 reading is terminal NOT-COMPARABLE, not INCOMPLETE: block a is complete and b is None, so the flow returns at `read.py:555`.
  - `replication_pending` stays `true` in every later `*_complete.json`, because it is computed at `:542` before that return.
  - The close-out must say "V2: NOT-COMPARABLE (also UNDERFIT-blocked); replication waived by ruling X". It must not read `replication_pending` as open work.
- **C3 (BLOCKING): state the deviation's scope.** Only V2 is skipped. replicate-F has a different role: it is the LAW#3 guard "in the block and in its replication block" (`PREREG:175`) and must complete.

Whether skipping leaves anything stuck:
- `control`: not stuck. `stage_plan` returns `[]`, because NOT-COMPARABLE is in `blocked` (`read.py:618–619`).
- `p4-save`: not stuck. V2 is skipped at `arms.py:945`, and every F modifier arm is UNDERFIT (`:950`), so it raises "P4 requires replicated LEAD/PARTIAL ..." (`:957`) before any marker is written (`arms.py:978–980`). That refusal is the prereg outcome under `PREREG:86`, not a failure. Record it as "P4 not triggered".
- Close-out: not stuck, provided C2 is followed.

## 2. Empty `reasons` on a value-based screen failure: disclose it in the close-out and change nothing. (ADVISORY)

- `read.py:551–552` only lists reference arms that are not DONE. A failed window or median produces `reasons: []` (confirmed in `r3_read_after_v2.json` and `r3/v2_complete.json`).
- A reader change is not available mid-attempt. It breaks the source pin (C1) and so HALTs the running replicate-F stage. It would also be a second source change in r3, after the one-fix budget was spent on the reader fix of D-C10u-r3go (5).
- Smallest correct handling: the close-out and the CORPUS note state the failing screen components by value:
  - multi `para_full_n` 31 ∉ [5, 18];
  - `canon_full_n` 24 ∉ [5, 10];
  - `para_first_n` 49 ∈ [42, 59];
  - mint-1(V2) median 46 ≥ 30 (passes).
- Add one line: "reader `reasons` is empty for value-based comparability failures (`read.py:551–552`); a reporting gap, not a verdict change". Queue the reasons fix for any future attempt's reader, not r3's.

## 3. Contradictions between the v2 reading and the prereg or code (ADVISORY unless noted)

- **3a. The packet understates the screen failure (ADVISORY, correct before the close-out).** V2 multi also fails canon: 24 against the upper bound of 10. The close-out must cite both failing keys, not only 31.
- **3b. mint2_s0 TRADEOFF.** Count 30 ≥ LEAD_MIN with `described_as` and `sibling` false gives TRADEOFF (`read.py:341–345`). This matches `PREREG:92` if "LEAD-sized" means the absolute count, which is how LEAD is defined there. Its gain over the same-block multi is −1, though. The close-out should not present it as a gain over the string route. Its per-position underfit (Fluvane) would also have blocked direction routing.
- **3c. mint1_s2(V2) is labelled LEAD on 38/72 with gain +7.** This is consistent with LEAD being absolute (`PREREG:92`), but disclose that the gain over the V2 multi is below the +10 PARTIAL margin for s2 (s1 is +15, s0 is +20).
- **3d. NOT-COMPARABLE taking precedence over ROUTING-BLOCKED-UNDERFIT** is intended (D-C10u-r3go (5), round 2 "put the V2 comparability gate ahead of UNDERFIT routing"). Report both blocking reasons in the close-out.
- **3e. Counts check.** mint-1 seeds 51/46/38 (median 46), mint-2 s0 30, s1/s2 UNDERFIT, F multi 14/8/53 inside the A4 window: all match the records. I found no gate or label error in the code path.

Bottom line: the lead's lean is confirmed on evidence. Skip replicate-V2 by a recorded ruling and disclose the empty `reasons` instead of changing the reader. That holds with conditions C1–C3, mainly: no prereg or reader edit while r3 stages run, because the identity pin covers both files.
