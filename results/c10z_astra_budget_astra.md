**FIX-FIRST**

**Next:** revise the budget justification and launch wrapper before approval. I support **7,200 / 12,600 / 19,800 seconds as proposed spending caps**, but the latter two are **not proven conservative completion budgets**. No evidence justifies a more precise replacement.

**BLOCKING**

1. **The stage-2 derivation bounds the wrong timing window.** `V≤2,910` concerns the pre-write window; stage 2 uses timings updated by the Z-A7 evaluation and probes. Its actual admission condition is:

   `elapsed_stage2 + 3,780 + 3×V_entry ≤ 12,600`

   Thus `V_entry` must be approximately **≤2,940 seconds**, not merely satisfy the earlier bound. I exercised the actual budget methods with a synthetic clock: pre-write `elapsed=3,500, V=2,000` passes at **6,880**; after subsequent timings, `V_entry=4,100` requires **16,080**, and stage 2 refuses. This is a scheduling counterexample, not an observed ASTRA runtime. [Timing window and stage transitions](</Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py:762>), [stage-2 projection](</Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py:1263>).

   **Replace the derivation with:**
   > “12,600 seconds is a discretionary stage-2 resource cap. It does not guarantee admission after K1: admission additionally requires elapsed_stage2 + 3,780 + 3×V_entry ≤12,600. V_entry is not bounded by the pre-write 2,910-second argument. Approval accepts a possible HALTED-BUDGET after a clean K1 observation.”

2. **“11.0 GPU-hours worst case” and “a larger stage-3 ceiling can never be reached” are false as written.** Stage 1 removes its deadline before stage 2 establishes a new origin. Process 1 can wait indefinitely there. Process 2 also has a transition interval between its inner scopes, although its outer stage-3 deadline remains active. A synthetic check with stage 1 completing at **7,199** and stage 2 entering at **7,201** produces inner deadline **19,801**, versus outer deadline **19,800**. [Budget scope implementation](</Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py:95>), [scope removal](</Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py:1259>).

   **Replace those claims with:**
   > “19,800 seconds independently caps process 2 and may bind before its inner stage-2 deadline. The nominal covered-scope sum is 39,600 seconds (11 hours), excluding process-1 launch overhead and its unbounded stage-1→2 resident interval. This is not an end-to-end compute-slot bound.”

   If **11 hours must be a hard operational maximum**, an enforced outer deadline is an additional implementation change requiring review. Chaining commands alone does not establish that bound.

3. **The 7,200-second amendment needs an honest basis.** The arithmetic `5,340+1,380+480=7,200` is correct; the component coverage is unverified. Stage-0 probes and later post-write probes are distinct required work, so recurrence of a validation allowance does not establish erroneous double counting. The proposed `≤120/300/60` overhead bounds have no measurements; process-1 interpreter startup precedes its resident clock. [Stage-0 work](</Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py:810>), [clock origin](</Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py:1390>).

   **Replace the amendment’s basis with:**
   > “7,200 seconds is a prospective two-hour resource cap, consistent with requirement 6, not a measured completion estimate. At the 1,380-second validation floor, the post-baseline projection permits 4,020 seconds elapsed, versus 2,220 previously. Additional validation and overhead costs remain UNMEASURED; HALTED-BUDGET remains possible. No projection, probe, validity check, round limit, scientific threshold or stage gate is removed.”

   Raising this ceiling **relaxes the resource gate**, but the listed constant-only change need not weaken scientific gates. The existing prereg explicitly forbids dropping checks to meet deadlines. [Prereg §2.11](</Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/C10Z_ASTRA_PREREG.md:196>).

4. **Repair launch exit handling and approval provenance.**
   
   - The proposed final `echo` masks command failure: I reproduced printed `STAGE_EXIT=1` with shell exit **0**. Replace its suffix with `rc=$?; echo "STAGE_EXIT=$rc"; exit "$rc"`. Record each invoked stage’s status, and dispatch stage 2 only when the persisted reading requests it; a normal K1 terminal result otherwise provokes an unnecessary stage-call refusal. [Proposed command](</Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/c10z_astra_budget_proposal.md:123>), [dispatch requirements](</Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py:1489>).
   - The JSON/env shape matches the parser. However, decision `"1"` should cite the row actually recording **WRITE-QUALIFIES or measurement-only**, rather than imply that the general GO explicitly settled it. Use `"1":"D-C10z-budget"` if that new row records the ruling. Budget approval is still prospective; do not write it as already obtained. [GO ruling](</Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/EXPERIMENT_RUNBOOK.md:351>), [required decisions](</Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/C10Z_ASTRA_PREREG.md:341>).

**ADVISORY**

- The listed constant, reader, SHA-pin and fixture edits cover the literal ceiling migration. Require **all existing 79 tests plus budget-transition regressions**, not “stay 79/79.” The cheapest overturning controls are the synthetic timing-window and transition cases above; they already falsify the stronger budget claims.
- Correct the round projection formula: the implementation uses `max(round_times or [120.])`; **120 is a fallback**, not a permanent floor. [Actual expression](</Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py:714>).
- Verified the prereg hash and absent named ASTRA output paths. The cited C10Q modification-time intervals are **1,825.568 seconds** and **1,876.820 seconds**; these support whole-pass anchors, not ASTRA component estimates. “Almost certainly P2 at about 40 minutes” and the expected **5.8-hour** total remain **UNVERIFIABLE forecasts**.
- This advances the C10 write-path investigation; it establishes neither runtime feasibility nor F1 readiness. The prereg preserves that distinction. [Scope limits](</Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/C10Z_ASTRA_PREREG.md:319>).

Read-only review completed. No model loaded; full selftest suite not rerun.

🌱 graft saved ~108,602 tokens (~$0.07) this turn, 1 call.