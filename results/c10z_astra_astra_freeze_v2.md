**FIX-FIRST.** Next: repair Z7’s numerical reference before implementation. It can currently misclassify correct fp16 execution as a science-path defect.

All prior blockers received operative body changes, not merely §8 entries. However, advisor/Codex **#1 and #2 remain partly resolved**; Codex **#19 does not satisfy this freeze check’s requirement for bounded later stages**. The following replacements are needed.

**BLOCKING**

1. **Z7 still omits rounding before the final norm.** [v2:154–155](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/C10Z_ASTRA_PREREG.md:154) substitutes `x+v` for the deployed residual. But the installed model performs a full `down_proj`, followed by residual addition, before normalization ([implementation:275–279](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/lib/python3.11/site-packages/transformers/models/qwen2/modeling_qwen2.py:275)). **I-INFER:** rounding those operations is not equivalent to adding `ΔWk` to an already-rounded `x`; Z1’s head-only calibration does not bound that discrepancy.

   Replace Z7’s forward-reference clause with:

   > Independently retain the full layer-35 down-projection input K and its pre-MLP residual R. Construct W_ref from PRISTINE using the independently calculated scalar solution and the specified fp32-add/fp16-store rule. Recompute the full native-shape fp16 projection `linear(K,W_ref)`, native residual addition to R, final norm and full head, using the recorded device and cast order. Compare reference and production leads separately before and after the write at every valid requirement position, holding each original competitor fixed. Define σ_head explicitly as the maximum native-reference versus native-output lead error on the pristine batch; freeze τ_head=max(2σ_head,0.02), halting above 0.25. The `x+ΔWk` formula is diagnostic only. Require at least one control with a nonzero realised weight change. Audit the production requirement map before filtering to failing positions.

   Also replace the stale “new writer’s inertness is Z1–Z6” at line 157 with “V5 requires Z0–Z5 and Z7; Z6 governs restoration.”

2. **The LAW#3 barrier remains internally contradictory.** Stage 0 step 2 explicitly collects new identity-view leads before step 3, despite the heading prohibiting new-writer observation. A builder can implement those leads through ASTRA’s observer or a separate baseline path. [v2:120–125](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/C10Z_ASTRA_PREREG.md:120)

   Replace the step-2 probe clause and add to step 4:

   > Before LAW#3 passes, run only recipe A’s existing evaluations. The arm hook saves each baseline arm’s edited band weights without additional forwards, then restores PRISTINE. After the complete LAW#3 gate passes, temporarily reinstall each saved baseline snapshot to collect the additional §2.9 probes and identity-view leads, then restore and verify PRISTINE. No baseline solve is repeated. Include these snapshots and deferred evaluations in memory and runtime accounting.

   Keep the existing **inclusive** A7 windows `[5,18]`, `[5,10]`, `[42,59]` and A1/A2 integer counts `≥68` unchanged; they correctly reproduce [CORPUS/44:39](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/CORPUS/44_C10L_COVGEOM_SPARSEBAND.md:39).

3. **Later-stage estimates are being called budgets; actual deadline enforcement is unspecified.** “Budgets are recomputed” gives stages 2–3 no independent ceiling. V13 names projected overrun and slow rounds, but not actual total-time expiration. [v2:195–198,221](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/C10Z_ASTRA_PREREG.md:195)

   Replace with:

   > Stage 0–1 has a 5,400-second hard elapsed-time ceiling, starting before model import. Stage-2 and stage-3 ceilings are mandatory positive launch-budget inputs, fixed and recorded before process 1 starts; an absent ceiling refuses that expansion. Ceilings never increase during an attempt. Only cost projections are recomputed. Before each stage and candidate write, publish elapsed time plus projected remaining work, including all checks, probes, serialization and restoration; refuse to start when this exceeds the applicable ceiling. Unknown required costs must receive a recorded conservative allowance, never zero. Independently enforce elapsed-time deadlines: expiration yields HALTED-BUDGET even when the earlier projection passed. Process 2 also retains the 5,400-second stage-0–1 ceiling. No gate may be dropped to meet a deadline.

4. **Several numerical rules permit different labels from identical records.** G7 says a *count* may increase by `1/6`; intended count slack appears to be **one hit**. Likewise executable-looking `canon_full_n ≥23/24` mixes count and rate. W1 leaves the even-population median convention unspecified. [v2:230,240,267](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/C10Z_ASTRA_PREREG.md:230)

   Replace/add:

   > Count fields are integers; denominators describe populations and are never included in count comparisons. FIT requires `20*m >= 19*M`, `positive_identity_fact_n >=23`, and `canon_full_n >=23`. For each G7 cell and each hit type, let h_Z and h_A be newly induced integer counts in [0,6]; pass iff `h_Z <= h_A+1`. G4 requires integer `L3_top1_agree >=29`. Every median, including D and W1, uses the arithmetic mean of the two central sorted values for an even population.

   **I-INFER, checked:** with baseline hits `1` and candidate hits `2`, `+1` passes while literal `+1/6` fails. Central W1 ratios `0.54,0.58` similarly yield a passing lower median versus a failing arithmetic median.

5. **Early stopping in process 2 has no complete certificate rule.** K1 can legitimately omit A1/A2, while R1 requires comparison for every Z arm and V12 rejects missing mandatory records. That permits either a valid negative replication or HALTED-V12 for the same run. [v2:220,260–272](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/C10Z_ASTRA_PREREG.md:260)

   Add:

   > Required records depend on completed stages. K1/K2 omissions are explicit NOT-RUN records with reasons, not malformed records. Before process 2, certificate fields are NOT-EVALUATED and do not invalidate process 1. If process 2 validly stops at K1, retain its measured A7 label and apply the lower-label aggregation; R1 for omitted arms is NOT-EVALUATED and the aggregate receives -REPRO-INCOMPLETE, which blocks adoption and gate A. Do not infer numerical reproduction failure from an unrun arm. An actual validity halt in either process prevents an aggregate scientific verdict; retain completed observations as non-binding.

**ADVISORY**

- **Own write-only verdict: WRITE-QUALIFIES as a method class.** The specified updates persist in `W_down`; the binding evaluator generates from the edited model without supplied answer prefixes, retrieval, or observation hooks. Fixed patch-derived constraints and at most **10 analytic updates** make this a bounded weight compiler. Absence of gradients alone would not establish that conclusion. Actual storage success, regeneration, latency and compaction remain **UNVERIFIABLE until run**. [v2:74–81,114,130](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/C10Z_ASTRA_PREREG.md:74)
- **The base truth table is sound.** I exhaustively checked all **2,044** valid `(a,n,S)` combinations: exactly one T-row matches each. The attribution’s descriptive count branches are also disjoint; its preceding fit/capacity/locality checks must be implemented as ordered first-match rules. [v2:244–278](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/C10Z_ASTRA_PREREG.md:244)
- Replace “final patch is the sum of all rounds” with “the authoritative patch is final fp16 weights minus PRISTINE; summed intended updates are diagnostic.” Repeated rounding makes those different quantities. [v2:80–81](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/C10Z_ASTRA_PREREG.md:80)
- **No F1 drift:** this targets the Write Engine/C10 behavioral gap, not whole-system readiness. The cheapest binding falsifier remains a valid, FIT stage-1 write failing `n≥19 AND n−a≥10`. [queue:23](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/INTEGRATED_QUEUE_2026-10-07.md:23), [v2:260](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/C10Z_ASTRA_PREREG.md:260)
- Independently opened the [ASTRA source](https://arxiv.org/html/2610.05277v1#S3): its weight-update mechanism supports this classification; it does not establish this adaptation’s success. Read-only review; no model run or file edits.

🌱 graft reported ~37,888 tokens saved (~$0.02), 1 successful call.

