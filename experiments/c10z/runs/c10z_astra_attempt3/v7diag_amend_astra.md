**FREEZE — amendment and builder brief. BLOCKING: none.** Implementation review remains required before dispatch.

Verified prereg SHA-256: `7aedd4ace95d2611bf398768df63cb60df6fce5afc23cf23209497bcd1d17a29`.

1. **Skeleton and authority: faithful.** Mechanical comparison found only the declared substitutions. Both decision IDs, delegation, budget authority, and bounded drift-3 exception are recorded; driftcap and refusal rules remain binding. [Prereg:707](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/C10Z_ASTRA_PREREG.md:707), [authority:800](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/C10Z_ASTRA_PREREG.md:800).

2. **Budget: sound as a bounded authorization.** `120+120+300+300+1500+120+180 = 2640`; ×1.15 = 3036, rounded up to **3060 seconds**. This includes conditional R5000. Sources distinguish inherited allowances from new estimates; timeout/incompletion routes to INCONCLUSIVE without an increase. [Budget:802](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/C10Z_ASTRA_PREREG.md:802), [timeout:772](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/C10Z_ASTRA_PREREG.md:772).

3. **Dataset provenance: correctly qualified.** Attempt-3 identity remains UNVERIFIABLE; F1000 is explicitly a new measurement. The pinned revision `b04c8d1ceb2f5cd4588862100d08de323dccfbaa` matches the local reference and Arrow cache directory. [Prereg:801](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/C10Z_ASTRA_PREREG.md:801).

4. **Equivalence strategy: adequate for build acceptance.** Requiring both AST identity and bit-identical output against the driver’s actual `compute_dstats` is a reasonable accommodation for its hard-coded loader. The brief additionally binds tokenization, initialization/precision, masking, hooks, batching, normalization and final cast. Together these preserve the specified computation; **CPU agreement alone would not establish MPS equivalence**. [Brief:12](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/C10Z_V7DIAG_BUILD_BRIEF.md:12).

5. **Persistence: matches ruling 5.** Immediate persistence, exclusive creation, flush/fsync, process-2 byte preservation, removal of the duplicate save, unchanged arithmetic and forced-failure retention tests are specified. [Brief:21](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/C10Z_V7DIAG_BUILD_BRIEF.md:21).

6. **Routing and qualification: faithful.** INCONCLUSIVE precedes A1/A2/D; R5000 is conditional and independently computed; C and searches remain prohibited. Negative examples agree with the table. The appended qualification appropriately retracts causal certainty. [Brief:14](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/C10Z_V7DIAG_BUILD_BRIEF.md:14), [negative examples:28](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/C10Z_V7DIAG_BUILD_BRIEF.md:28), [qualification:56](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/c10z_astra_attempt3/v7_diagnosis.md:56).

**ADVISORY**

- Make the CPU fixture nontrivial: mixed lengths, >100-token inputs, nonzero padding activations, distinct layers, and the final eight-row batch. Check token IDs/counts and normalization outside the AST-compared loop.
- The primary delegation timestamp is **2026-10-09 01:43:41.034 UTC**, or October 8 **19:43:41 MDT**, rather than approximately 20:00. Authority is verified; tighten the citation when next updating provenance. [Transcript:6451](/Users/robertrhu/.claude/projects/-Volumes-memit-llm-database-poc-mirror-arhugula-persistent-memory--claude-worktrees-c10k-route-a/b756c87a-ea8d-4e4a-b2af-c10e1bff4a7d.jsonl:6451).
- “Fits with margin” is a projection, not measured R5000 runtime. Preserve that distinction and verify actual deadline enforcement during implementation review.

Read-only review; no implementation tests or model execution performed.

🌱 graft reported ~190,782 tokens saved (~$0.10), 1 successful call.

