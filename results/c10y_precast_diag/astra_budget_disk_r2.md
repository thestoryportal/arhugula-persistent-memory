ACCEPT

Acceptance is for the **conditional draft**, not freeze or dispatch.

Notation: **B** = `results/c10y_precast_diag/amendment_budget_draft.md`; **D** = `experiments/track_c/c10y_precast_diag.py`; **S** = `results/c10y_precast_diag/20261009T225619Z/OPERANDS_MANIFEST_sizes.txt`.

1. **Reference option: satisfied; no inherently unsafe B1/B4 substitution found.** The four proposals retain both actual observer observations, all individual pre-cast updates, and all realizations. Control-input references correctly select the **matched recipe-A X**, replacing the transient native X before controls consume it (B:290–310; D:429–432,455–480,505–508,558–584).

   Safety remains conditional on verified immutable payload resolution and durable reference publication before predicates. The existing reader cannot implement this proposal unchanged (D:56–60,89–106). References that merely retain hashes, assume observer equality, or substitute realized weights for pre-cast updates would violate the stated contract; Y4 explicitly excludes them.

   Reexecuting Y4’s inspected C1 JavaScript through `/opt/homebrew/bin/rtk proxy /opt/homebrew/bin/node -e …` reproduced savings of **62,406,322,066 B** and conditional floors of **248,769,839,507 B** for three changes and **231,030,551,257 B** for all four, before new overhead (B:314–333).

2. **Last-use schedule: arithmetic and source dependencies hold; operational qualification remains open.** An independent Node audit parsed S, checked checksum-manifest filename membership, reconciled retained-file sizes, and reconstructed:

   - F = **8,596,403,387 B**
   - N_A = **19,712,227,255 B**
   - N_Y = **31,869,805,550 B**
   - A/Y snapshot pairs = **5,297,937,034 / 6,214,223,634 B**
   - C = 11,413,009,617 − 3,938,200,155 = **7,474,809,462 B**

   Consequently:

   ```text
   Native peak = F + N_A + N_Y + Y snapshots
               = 66,392,659,826 B

   Controls peak = F + N_A + N_Y + C
                 = 67,653,245,654 B

   Archive total = F + 2×(N_A + N_Y + A snapshots + Y snapshots) + 10×C
                 = 209,532,884,953 B, across 2,049 packets
   ```

   These independently match B:399–417. Adding estimated metadata and reserve produces **89,150,911,958 B**.

   Snapshot archival follows their last predicate; native operands/factors/batches remain through their arm’s controls; completed cells have no subsequent cross-cell tensor reads (D:432–448,558–607,664–676). Y4 correctly requires a new durable cell-completion receipt because D:670 currently retains the returned summary only in memory.

   **Measured overhead and executable failure/replay/time bounds are still absent.** Thus my round-1 measurement requirement remains an adoption gate, not an empirically completed qualification. B:424–430 states this accurately and requires failed transfers to retain local evidence and stop progression.

3. **Recommendation: appropriately qualified.** B:420,434 preserves the distinction between cumulative writes required by `EXPERIMENT_RUNBOOK.md:263` and proposed peak occupancy. Larger storage is the unchanged-writer option; archival merely **may fit**.

   The UNMEASURED items are genuine dispatch blockers: scratch/allocation bounds, remote durability, replay, interruption behavior, and archive-inclusive timing. Y4 already makes them blockers. They do not justify rejecting the conditional candidate or claiming a larger volume is unavoidable. Its **2,661,149,226 B** snapshot headroom is not admission evidence (B:432).

**New required fixes: none for this draft.** Existing qualification gates remain mandatory. Verification here was source/metadata/arithmetic only; no tensor decoding, remote verification, or runtime qualification.

🌱 graft saved ~115,882 tokens (~$0.07), 1 successful call.