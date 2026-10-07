PROCEED

**Next:** advance the round-2 reader fix to the existing r3 preflight gate. No BLOCKING findings in this delta.

1. **Round-1 blocker closed.** V2 comparability now runs before either UNDERFIT route; any non-DONE reference makes it false. Every top-level arm receives `-NOT-COMPARABLE`, and P4 rejects the block. See [reader:474](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_read.py:474), [reader:548](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_read.py:548), [selector:945](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_arms.py:945).

2. **No new gate weakening or invented count found.** The three new published-admission checks agree with recomputation ([reader:296](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_read.py:296)). Independently reran **83 tests: all passed**. Also passed the actual [r2 step-0 payload](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/c10u_mint2/r2/step0/F_r0_modifier_s0.json) through current `behavior_job` with boundary I/O mocked: **17/24**, zero validity errors. All four historical DONE records validated; mutations of each new admission field were rejected.

3. **ADVISORY—test provenance needs precise wording.** These are predominantly synthetic fixtures. The historical record supplies top-level keys; the “real producer” test invokes real `behavior_job` with synthetic, mocked step-0 input ([fixture:109](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_selftest.py:109), [test:887](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_selftest.py:887)). Retain the actual-sidecar check above as a permanent regression.

The cheapest overturning checks—failed comparability combined with original/replica UNDERFIT and attempted P4 selection—pass. **Live r3 stage behavior remains UNVERIFIABLE from this CPU review.** This supports the C10 measurement path toward F1; it establishes no scientific readiness result.

🌱 graft reported ~67,443 tokens saved (~$0.06), 1 successful call.

