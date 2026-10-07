**FIX-FIRST.** Next: pin the later-stage clocks’ origins. The five requested body changes landed, but the budget replacement still permits two implementations.

**BLOCKING**

1. **Stage-2/3 elapsed time lacks a defined origin.** [§2.11, line 195](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/C10Z_ASTRA_PREREG.md:195) fixes ceiling values before launch but does not say whether stage-2 elapsed time includes stages 0–1. That changes whether expansion runs or yields HALTED-BUDGET. This omission was also in the prior review’s proposed replacement.

   Replace its stage-2/3 ceiling sentence with:

   > Stage-2 and stage-3 ceilings are positive durations in seconds, fixed and recorded before process 1 starts; an absent ceiling refuses that expansion. The stage-2 clock starts on entry to stage 2, separately in each process, using the same fixed duration. The stage-3 clock starts before process 2’s model import and covers all of process 2. Process 2 additionally enforces its stage-0–1 and stage-2 deadlines. Each elapsed-time/projection comparison uses the corresponding clock origin and remaining work within that scope; the earliest applicable deadline governs.

**ADVISORY**

- **Memory arithmetic passes.** The added snapshots occupy **676,331,520 bytes = 0.67633152 GB = 0.6298828125 GiB**. The displayed peak terms sum to **15.80 GiB**, versus **15.17 GiB** without snapshots. Both rounded figures are consistent with the [memory table](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/C10Z_ASTRA_PREREG.md:169); neither is a measured peak.
- The five fixes appear in operative text: Z7/Z1 (§2.8), deferred baseline probes (§2.6), deadlines (§2.11/V13), integer/median conventions (§3), and incomplete replication records (§3.4/V12/R1). Old calibration/budget wording remains only in the explicitly historical v1→v2 fold log (§8), superseded by §8.2.

Read-only; no model run or edits.

🌱 graft reported ~19,585 tokens saved (~$0.01), 1 successful call.

