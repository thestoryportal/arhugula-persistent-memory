**The numerical fix at `57420ab` is ready to enter launch-readiness review.** This was a read-only source, hash, and receipt audit; I did not rerun tests or numerical workloads.

1. **Not blocking — r8 Q3’s production change is satisfied exactly.**  
   [tools/new1_geometry.py:200](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/new1_geometry.py:200) performs two independent advanced-index gathers from the same native U and unchanged allowed indices, then multiplies the first by the second’s transpose. This matches the producer’s construction at [c10e_bandknob.py:173](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10e_bandknob.py:173).

   The commit contains exactly this production hunk, one added test, and receipts. Normalization, decompositions, masks, surrounding execution order, thresholds, `projector_matches`, and `tensor_sha` are unchanged. The engine Git tree is identical before/after: `677576d053f4e7eeb38c8023e607c3e82da81cb0`.

   The worker’s sole capture-compared construction calls this function at [geometry:541](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/new1_geometry.py:541). No shared-gather alternative remains on that path. The identity diagnostic already gathers twice; the construction diagnostic correctly retains its shared-gather experimental controls.

2. **Not blocking — the regression meets the requested test contract without a vacuous observation pass.**  
   [test_native_projector_uses_two_independent_native_gathers:188](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tests/test_new1_geometry.py:188) directly calls production code with nonempty synthetic CPU-fp32 U and fixed `[3,1]` indices. Hooks delegate to the original tensor indexing/matmul methods. Assertions check exactly two gathers, source/index identity, native values/dtypes, distinct operand storage, second-gather storage provenance, transpose equality, unchanged inputs, independent reference bytes, and the real capture gate.

   A missed required gather produces a count failure; a missed matmul produces a product-count failure. The reference and gate run outside the observation context.

   Existing controls remain unchanged:
   - **Count mismatch and SHA success:** `test_native_parity_is_retained_when_float64_excluded_energy_is_large`, [line 441](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tests/test_new1_geometry.py:441).
   - **Four-probe fallback and failing fourth probe:** `test_projector_matches_all_four_frozen_probes_and_update_parity`, [line 229](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tests/test_new1_geometry.py:229).

   Acceptance remains **matching count AND (matching SHA OR all four probe errors ≤1e-6)**.

3. **Not blocking — the preserved RED/GREEN/RED-again evidence supports the claimed regression.**  
   I recomputed the before/after snapshot hashes and subject-commit hashes; they agree with the per-run SHA sidecars:

   | Run | Production SHA prefix | Saved result |
   |---|---|---|
   | RED | `018ce4d9…` | 34/35; exit 1 |
   | GREEN | `ce43a26d…` | 35/35; exit 0 |
   | RED-again | `018ce4d9…` | 34/35; exit 1 |

   All three sidecars record test SHA `dba1606f…`. Both failures are specifically **`1 != 2 : native projector must gather twice from native U`**, rather than import, environment, or incidental errors: [RED.log:43](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/mathlab_staging/new1_projector_fix_20261010T204522Z/RED.log:43), [RED-again.log:43](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/mathlab_staging/new1_projector_fix_20261010T204522Z/RED-again.log:43). GREEN records 35 tests and OK at [GREEN.log:38](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/mathlab_staging/new1_projector_fix_20261010T204522Z/GREEN.log:38).

   These are audited saved execution receipts, not an independently repeated execution in this review.

4. **Not blocking — extra-gather memory does not justify increasing caps; complete-worker feasibility remains unverified.**  
   Every production layer has dimension **11,008** ([geometry:534](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/new1_geometry.py:534)). The incremental allocation is one fp32 `11,008 × n_allowed` gather; `.T` adds no second data buffer.

   - Measured L4 count 8,645: `11,008 × 8,645 × 4 = 380,656,640 bytes` = **363.022 MiB / 0.354514 GiB**.
   - Conservative maximum, `n_allowed ≤ 11,008`: **484,704,256 bytes = 462.25 MiB / 0.451416 GiB**.

   Gathers are temporary; layers run sequentially. Do **not** multiply this peak increment by five. Construction occurs after both SVDs/checks, under the **19-GiB covariance-check admission gate** ([geometry:536](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/new1_geometry.py:536)).

   As a planning sensitivity calculation, adding the worst-case increment to the existing 8.056793-GiB profile gives **8.508209 GiB**; applying its 25% margin gives **10.635262 GiB**, still rounding to **11 GiB**. This is **not a full-worker RSS bound**: allocator retention, backend workspace, and other resident data remain relevant. Preserve the **11-GiB cap, 13/19-GiB floors, and 2,700-second deadline** from [prereg:218](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/NEW1_ADAPTER_GEOMETRY_PREREG.md:218). The additional copy has no measured full-worker timing here; saved-output volume is unchanged.

5. **Blocking for launch only; not blocking this fix’s advancement — existing readiness gates remain.**  
   No additional numerical blocker was found. Before launch, separately review MB27’s supervisor reap fix, pin the combined final implementation, and obtain readiness review plus fresh operator authorization for one capped, fresh-namespace attempt with no automatic retry, as required by [r8:53–57](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/mathlab_staging/new1_construction_diag_astra_r8.md:53). This regression proves the construction contract; it does not establish full-worker recovery, historical HALT causation, or scientific success.

🌱 graft reported ~107,183 tokens saved (~$0.07), one successful call.

VERDICT: GO