VERDICT: SKIP-REPLICATE-V2-WITH-CONDITIONS

1. **BLOCKING — Skip only under an explicit, recorded program ruling waiving gate A; this is a prereg deviation, not an interpretation that replication was unnecessary.**

   The prereg requires replication for LEAD/PARTIAL arms as well as direction labels; A-env explicitly preserves reference-arm replication triggers. The three mint-1 arms retain LEAD-NOT-REPLICATED beneath their NOT-COMPARABLE suffixes. Neither the comparability paragraph nor r3 rule A1 grants a replication exemption (`docs/C10U_MINT2_PREREG.md:78,92,179`; `EXPERIMENT_RUNBOOK.md:347`). I recomputed the saved readings exactly and confirmed `stage_plan("replicate-V2")` returns seven jobs (`experiments/track_c/c10u_mint2_read.py:383–392,542–555,610–620`).

   **The lead’s rationale needs narrowing:** no valid, complete replica can *restore comparability*, because the original block remains a failing conjunct. A replica can change reference-arm replication labels and measure whether the unexpectedly high multi baseline recurs in a fresh process using the same frozen contexts/inits. That contributes to the promised diagnosis, although it cannot establish the cause or rescue routing (`docs/C10U_MINT2_PREREG.md:78`; `experiments/track_c/c10u_mint2_read.py:385–390,474–479,548–555`).

   Record a new decision in runbook §5.2 and a linked **post-observation prereg-deviation note in the close-out**, without editing the pinned prereg. Suggested substance: “Waive V2 gate-A replication after the original comparability failure; seven scheduled jobs omitted to release the queue. Preserve NOT-COMPARABLE and unreplicated arm labels. Fresh-process stability of the V2 baseline remains unmeasured; diagnosis unresolved; no historical/direction/promotion claim.” The budget ruling permits operator stopping between stages, but does not make the omitted replication completed (`EXPERIMENT_RUNBOOK.md:341`).

   **Completion consequences:** with no V2 replica records, the reader stays **NOT-COMPARABLE**, not INCOMPLETE, but `replication_pending=true` remains. Preserve that field and explicitly disposition it as **waived by the ruling**; do not claim the frozen schedule finished. A partially populated replica would instead trigger INCOMPLETE (`experiments/track_c/c10u_mint2_read.py:505–512,542–555,717–725`).

   **P4 is inapplicable on these originals:** V2 is excluded by NOT-COMPARABLE; every original F modifier is UNDERFIT and skipped regardless of its replica. Thus `p4-save` refuses for lack of eligible configurations, rather than waiting for V2 replication. Record P4 as **not applicable—no eligible configuration**, not PASS (`results/c10u_mint2/r3_read_after_v2.json:1367–1383`; `experiments/track_c/c10u_mint2_arms.py:935–958,980–992`). Close-out has no reader-pending veto: it checks documentary presence/currency, so the waiver can be documented honestly; its gate must still pass before declaring close-out complete (`tools/closeout_check.py:187–238,249–256`; prereg `:115`).

2. **ADVISORY — Disclose the empty-reasons defect; do not patch the reader during r3.**

   The smallest correct disclosure names **both** failed bounds: A7-multi para_full **31/72 > 18** and canon **24/24 > 10**. Para_first **49/72** passes [42,59]; mint-1 median **46/72** passes ≥30 (`results/c10u_mint2/r3/V2_r0_multi_snone.json:4178–4181`; `V2_r0_mint1_s0.json:10776`, `V2_r0_mint1_s1.json:10776`, `V2_r0_mint1_s2.json:10776`; prereg `:175`).

   Explain that `reasons=[]` means **missing explanatory reporting**, not no screen failure: the reader appends reasons only for non-DONE references, and all four references are DONE (`experiments/track_c/c10u_mint2_read.py:474–479,551–555`; saved reading `:3349–3354`). Regardless of whether a reporting patch consumes the fix budget, source edits are forbidden during the schedule and would break the pinned identity (`EXPERIMENT_RUNBOOK.md:341,347`; `experiments/track_c/c10u_mint2_arms.py:89–94`). A close-out disclosure suffices.

3. **ADVISORY — The saved reading matches the current code; two interpretation corrections matter.**

   Mint-2 s0’s **TRADEOFF** comes from failed **described_as and sibling locality gates**, not from `all_positions_fit=false`. Its binding is 30, reference 31, gain −1; LEAD sizing uses the absolute ≥30 threshold. Per-position failure independently blocks direction routing, but NOT-COMPARABLE returns first (`results/c10u_mint2/r3_read_after_v2.json:2776–2791,3323`; `experiments/track_c/c10u_mint2_read.py:341–345,381–393,550–567`; prereg `:92,94`).

   Seeds 1/2 have admission counts **20/24 and 21/24**, below 22: their UNDERFIT records contain no behavioural count. They must not become zero-valued observations. UNDERFIT-NOT-COMPARABLE is consistent with §5’s admission disposition and comparability precedence (`results/c10u_mint2/r3/V2_r0_mint2_s1.json:98–103`; `V2_r0_mint2_s2.json:98–103`; prereg `:115`; reader `:377–379,553–555`).

   V2 stage completion is verified (`results/c10u_mint2_logs/r3/v2.log:3371`), but STAGE_EXIT=0 is not comparability success. The additional canon failure omitted from the packet strengthens the stated screen failure; it does not justify a new scientific label.

🌱 graft saved ~78,035 tokens (~$0.05) this turn, 1 successful call.

