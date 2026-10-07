**FIX-FIRST.** Before relaunch, fix the reader’s handling of legitimate non-admitted records; the logging fix alone leaves required replication suppressed.

**BLOCKING**

- **UNDERFIT poisons the block and cancels replication.** `experiments/track_c/c10u_mint2_read.py:190–191` requires every record to have a positive PID and outcome `DONE`. `_population:395–396` applies this to the deliberately skipped record (`pid=None`, `UNDERFIT`); `block_reading:453–455` consequently returns `INVALID`, empty arm readings and `replication_pending=False`; `stage_plan:544–546` returns no replication jobs.

  **Verified without torch:** r2’s three mint-1 records individually read `LEAD-NOT-REPLICATED`, counts **34/35/37**, but adding its UNDERFIT record produces that invalid-block result. A synthetic **complete seven-record** positive control schedules **7** replication jobs; replacing one modifier result with the legitimate UNDERFIT record shape reduces this to **0**. This contradicts replication of any LEAD/PARTIAL configuration (`docs/C10U_MINT2_PREREG.md:78`).

  **Exact fix:** distinguish validated non-admitted records from completed behavioral runs throughout population validation, block reading and replication matching. Preserve their admission/provenance checks, apply behavioral/PID checks only to executed runs, block direction inference on UNDERFIT, and retain replication obligations from eligible completed arms. Add the seven-record regression above. Do not invent behavioral counts or weaken completed-run validity gates.

**ADVISORY**

- **Immediate r2 diagnosis confirmed.** Diagnostic `architecture_profile/c10u_mint2_halt_diagnostic_6508cfa1c1c945f294ad8e8115404dfa.json:118` records exit **0**; the referenced child log is **0 bytes**; its result exists and no behavioral-start marker exists. Recomputed admission is **UNDERFIT, 17/24**, with P2 and I-11 passing (`results/c10u_mint2/r2/step0/F_r0_modifier_s0.json:2826`). No behavioral run is prereg-correct (`docs/C10U_MINT2_PREREG.md:115`). The empty-log guard fully explains this particular HALT.

- **No other normal successful child path lacks its result/log.** In `c10u_mint2_arms.py`, contexts write at **683** and obtain output from the fresh harness import (`c10e_bandknob.py:49`); step0 writes/prints at **742–743**; admitted behavior at **865–869**; non-admitted behavior at **777–779**. Replication and P4-save reuse these paths (**969–970, 1022**). Empty conditional plans are explicit pre-start refusals (**991–992**), not successful children. Context logging depends on the harness’s import print.

- **Fix scope is logging-only.** Verified the current driver equals r2’s pinned source plus exactly the print at **778**. Arithmetic, record payload, labels and gates are unchanged; launcher differences are only lines **2/9/11**. The test exercises the real non-admitted branch, but **never calls `spawn_job`** (`c10u_mint2_selftest.py:572–588`); “parent accepts” overstates its coverage. Historical RED→GREEN/61-test execution is **UNVERIFIABLE here**; the write-producing suite was not rerun.

- **r2 remains separately citable evidence**, including reproduction PASS and multi **10/9/52**, A1 **69**. Preserve its HALTED-HARNESS status and original provenance; do not splice its records into r3 or count them as r3 replication. The recorded ruling requires r3 to rerun them (`EXPERIMENT_RUNBOOK.md:347`). This supports the C10 representation diagnostic, not F1 closure (`docs/C10U_MINT2_PREREG.md:9–11`).

🌱 graft reported ~50,535 tokens saved (~$0.03), 1 successful call.

