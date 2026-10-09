FIX-FIRST

Reviewer: GPT-6-Astra (high)

**BLOCKING**

- **Computed `m` can still disappear.** [c10z_v7_diag.py:330](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag.py:330) checks provenance before saving. CPU control reproduced INCONCLUSIVE with computed `m` absent. **Fix:** exclusively save/fsync the returned statistic and provenance immediately, then validate; retain mismatch details.

- **Forced termination produces no fresh halt diagnostic.** [c10z_v7_diag.py:69](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag.py:69) uses default SIGALRM termination; the launcher `execve`s away its supervisor. CPU control exited −14, leaving only the provisional verdict. **Fix:** retain a supervisor that records abnormal termination in an exclusive, fsynced, UTC-suffixed diagnostic, identifying active/incomplete phases and retained artifacts.

- **Cleanup escapes the deadline.** [c10z_v7_diag.py:75](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_v7_diag.py:75) cancels the timer before `run()` releases its model/statistic references. **Fix:** cover explicit cleanup and worker exit with the original 3,060-second deadline; publish successful completion only after cleanup.

- **“Every gate input” remains unmet for `G`.** [c10z_astra_arms.py:1100](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py:1100) validates before persistence. Forced V8 failure retained `dstats` but lost computed `G`. The brief explicitly leaves this save late, so this is a requirement conflict, not builder deviation. **Fix:** record a bounded persistence-only extension moving G’s exclusive save/byte-copy before V8; update retention tests.

**ADVISORY**

- Independently passed: **33 probe tests; 207 ASTRA tests, 2 MPS skips; engine fingerprint**. RED transcripts contain substantive assertions, but current tests miss the blockers above.
- Statistic identity, frozen routing, namespace isolation, pre-load GPU/fingerprint gates, and prereg SHA match. Arms/read changes are record-only; engine and `c10e_bandknob.py` have no HEAD diff.
- The report’s launch command correctly invokes the first probe with a fresh UTC namespace. Dispatch remains blocked above. GPU/MPS behavior and runtime remain **UNVERIFIED**.
- No source edits, model loads, GPU work, or live-results writes performed.

🌱 graft reported ~228,114 tokens saved, 1 successful call.

