**FIX-FIRST — 1 BLOCKING issue.**

**Next:** preserve V2 comparability independently of UNDERFIT routing, and require established comparability before P4 selection.

1. **BLOCKING: UNDERFIT bypasses an existing comparability gate.** [c10u_mint2_read.py:543](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_read.py:543) returns before checking comparability or attaching `-NOT-COMPARABLE`. [c10u_mint2_arms.py:945](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_arms.py:945) then permits P4 selection.

   **CPU counterexample verified:** using the existing fixtures, V2 multi **19/72**, mint-1 **34/36/46**, mint-2 **30/31/32**, with matching replicas:
   - All DONE: `NOT-COMPARABLE`; P4 refuses.
   - Replace mint-2 seed 0 with valid UNDERFIT: `ROUTING-BLOCKED-UNDERFIT`; seeds **1 and 2** retain unqualified `LEAD` and enter P4.
   - Reproduces with UNDERFIT in the original, replica, or both. Also reproduces with passing multi but mint-1 **20/21/22**, median **21 < 30**.

   This violates the comparability requirement in [prereg:78](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/C10U_MINT2_PREREG.md:78). Add these intersection regressions; handle a non-admitted mint-1 reference as **unestablished comparability**, without inventing its count. Preserve replication obligations and eligible F-arm P4 selection.

2. **The original blocker is fixed.** Independently reran **75/75 tests**, including the real producer regression at [selftest:765](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_selftest.py:765). The seven-record F counterexample now retains **7 replication jobs**, reports UNDERFIT without behavioral counts, and blocks direction inference. Inspection found no weakened per-run DONE checks; the remaining weakening is the block-level gate above.

3. **Verification boundary:** no additional false-HALT/false-INVALID path identified in the inspected stages. Live r3 execution remains **UNVERIFIABLE** from these CPU checks; the producer regression does not exercise `spawn_job`. This repairs the C10 instrument, not F1 readiness itself—consistent with [prereg:111](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/C10U_MINT2_PREREG.md:111).

🌱 graft reported ~54,645 tokens saved (~$0.03), 1 successful call.