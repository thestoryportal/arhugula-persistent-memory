**FIX-FIRST.** The terminal boundary is sound, but the proposed measurements and classifier do not yet isolate R/K/S. Freeze the operand capture and arithmetic definitions first.

Reviewed draft SHA `f666bd01…`; prereg SHA matches `005391a39e31d8174419de3e39078a42209ded1b7ab8caaf098d5d8a4f755004`. Read-only review; no model, GPU, simulation, or tests run.

**BLOCKING 1 — “Identical inputs” needs a per-layer contract.**  
[Scope:14–22](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/C10Y_PRECAST_DIAG_SCOPE.md:14)

Shared targets, hparams and covariance files are necessary but insufficient. Recipe A reads keys and residuals after preceding layer edits; C10Y independently reconstructs that sequence. See [recipe A:194–217](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10e_bandknob.py:194) and [capture_solve:268–283](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_arms.py:268). Different sequential states would confound an arithmetic comparison.

Append after line 17:

> For each arm, restore and verify the same pristine weights, initialize a fresh zero cache, and use one saved projector set and one saved target set. Pin request order, tokenized batches, padding, lookup indices, context cache and operative harness globals.  
>   
> At each layer preserve the actual pre-layer state identity, K, cur, allocated residual R, P, cache C, L2, assembled solve matrix and right-hand sides from both original paths. Record dtype, shape, orientation and tensor-byte hashes. Compare corresponding operands exactly before attributing output differences to arithmetic. All controlled arithmetic variants consume the same saved recipe-A operand packet; no variant’s update feeds subsequent layer inputs. Separately record any disagreement in C10Y’s native capture path.  
>   
> Prove observer coverage and tensor/weight inertness with observer-off/on controls; source identity alone is insufficient. Restore weights, hooks, globals and caches between arms and on failure. No behavioral evaluation is introduced.

Retain line 16: recompute targets once, save before comparison, label **NEW COMPUTATION**. I verified the historical file’s size, **1,261 bytes**, and SHA `1d95c75a…`; the prior ruling establishes the persistence defect.

**BLOCKING 2 — The controls conflate product precision, solve precision and operation order.**  
[Scope:20–25](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/C10Y_PRECAST_DIAG_SCOPE.md:20)

Recipe A computes `solve(M, (P @ K) @ R.T).T`. C10Y computes `X = solve(M, P @ K)`, then `R @ X.T`. Multiplying existing factors cannot reproduce “recipe A’s operation order.” Moreover, the imported [factor_solve:238–243](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_arms.py:238) explicitly casts inputs to fp32: passing it doubles does not create a float64 solve.

Replace measurement 3 with:

> Preserve M32, Q32 = P32 @ K32, B32 = Q32 @ R32.T, the actual direct solution, and the actual factor solution X32. Measure separately:
>   
> (a) CPU-fp32 R32 @ X32.T, with the same factors and parenthesization as the MPS product;  
> (b) CPU-float64 multiplication of promoted, already-solved fp32 factors;  
> (c) genuine CPU-float64 direct and factored solves from the same saved operands, promoted before assembly, followed by their respective products;  
> (d) float64 solves of the saved assembled fp32 systems, to distinguish assembly rounding from solve/product effects;  
> (e) exact-input repeats of the direct solve, factor solve, CPU product and MPS product.
>   
> Controls (b) and (c) are distinct artifacts. Explicit diagnostic-only arithmetic is permitted for these controls; it never substitutes for capturing the original reference or modifies the engine, harness or driver.

Replace measurement 6 with:

> Record the condition-number norm and computation method. Both paths should use the same coefficient matrix M; preserve and compare their actual matrices. Report normalized residuals for both solves against their respective saved systems, and errors relative to the float64 controls. Condition numbers are explanatory measurements, not causal verdicts.

Also amend measurement 5:

> Preserve both realized weights and realized updates `W_post − W0`, with the subtraction performed after CPU promotion. Freeze the cast/add device and order for each control. A float64 realization must not silently pass through a helper that first demotes the update to fp32.

That last issue matters because [stored_weight:287–289](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_directdw_arms.py:287) contains an explicit `.float()`.

**BLOCKING 3 — Do not freeze the proposed numerical thresholds as causal classifiers.**  
[Scope:27–33](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/C10Y_PRECAST_DIAG_SCOPE.md:27)

- `max(10 × floor, 1e-7)` becomes more permissive as repeatability worsens.
- A small double-precision gap does not establish conditioning as the cause or prove the factored solution less accurate.
- A double-precision gap above `1e-6` does not establish different mathematics.
- Concentration in columns can arise from numerical sensitivity.
- “Scale with condition numbers” and “concentrates” have no executable definitions.
- “While P_MPS does not” leaves the failed predicate and arm aggregation ambiguous.

Numerical error analysis depends on conditioning, backward error and operation dimensions; these three constants have no supplied derivation covering those quantities. See Higham’s [Testing Linear Algebra Software](https://nhigham.com/wp-content/uploads/2023/10/high97t.pdf).

**My exact replacement removes all three magnitude thresholds from classification.** It deliberately narrows what this bounded diagnostic may conclude:

> All distances, repeat floors, precision changes and conditioning measurements are descriptive. No numerical magnitude threshold establishes K or S.
>   
> Evaluate in order:
>   
> **INCONCLUSIVE:** required capture, source identity, observer validation, persistence, finiteness, resource or deadline requirements fail.  
>   
> **R:** corresponding native operands and states agree; repeats are byte-stable; CPU-fp32 multiplication of the saved C10Y factors produces recipe-A-identical realized fp16 weights in all ten arm/layer cells; MPS multiplication of those same factors produces different realized weights in at least one A7 cell. Report every cell, including A1. Interpretation: changing product device is sufficient to remove the observed weight mismatch on these newly computed inputs. This establishes neither calibration-4 causation nor an exclusive explanation of all pre-cast differences.  
>   
> **K:** reserved; not emitted by this scope. Precision convergence, residuals and conditioning may support a conditioning hypothesis, but do not uniquely identify it. Such cases are UNCLASSIFIED with the measurements attached.  
>   
> **S:** complete, validated traces directly demonstrate a discrepancy in operative inputs, state, orientation or implemented formula. A faithfully captured discrepancy is evidence; missing or untrustworthy capture is INCONCLUSIVE. Numerical distance or concentration alone cannot trigger S.  
>   
> **UNCLASSIFIED:** all remaining cases, including unresolved CPU reassociation/conditioning and mixed mechanisms.
>   
> Only R may justify proposing a CPU-fp32 product redesign. Adoption requires its own amendment, LAW#5 isolation against the required reference, implementation review and separate team admission. No label authorizes a fix, calibration 5 or stage-1 dispatch.

This replacement is independent of calibration 4’s observed distances: it uses a controlled device substitution and exact stored-weight identity. It intentionally accepts more UNCLASSIFIED outcomes. **If an automatic positive K verdict is required, this scope needs an additional independently justified conditioning test before freeze.**

Replace line 6’s “It distinguishes mechanisms” with:

> It localizes device-product effects and records evidence bearing on reassociation, conditioning and implementation/state discrepancies; these mechanisms need not be mutually exclusive.

**BLOCKING 4 — Persist-before-gate is incomplete.**  
[Scope:47–48](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/C10Y_PRECAST_DIAG_SCOPE.md:47)

Listing exclusive output files and a halt diagnostic does not ensure partial tensors survive exceptions or watchdog termination. The governing [amendment:1002–1007](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/C10Y_DIRECTDW_PREREG.md:1002) explicitly requires that behavior.

Append:

> Persist each completed target, operand packet, factor, update and computed gate input using exclusive durable phase writes before evaluating its dependent gate. Flush/fsync records; never rely on successful function return or final serialization to retain partial work. Record incomplete and NOT-RUN phases explicitly. The supervisor preserves committed artifacts and writes a fresh terminal diagnostic on timeout. Forced-halt, interrupted-phase and overwrite-refusal tests must demonstrate retained values, unchanged gate outcomes and cleanup before implementation approval.

**ADVISORY**

- **Boundary passes:** lines 9–10 and 50–51 preserve calibration 4 and prohibit behavioral retry/admission. Replace line 32’s “one speculative fix” with “propose a separately reviewed investigation”; this measurement scope should authorize no corrective execution.
- **Cap arithmetic passes:** `600 + 1360 + 300 + 180 = 2440`; `2440 × 1.15 = 2806`; ceiling to a minute is **2,820 s**. Keep that hard cap. Feasibility remains **UNVERIFIED**, particularly after genuine float64 solves and conditioning calculations. C10X’s [CAPS:36](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10x_enginepath_arms.py:36) lists a separate target allowance, so the 1,360-second combined estimate needs workload reconciliation.
- **GPU/fresh namespace:** the stated fail-closed gate and fresh namespace are appropriate. Require exclusive directory ownership, recorded gate results immediately before model load, and an external deadline covering setup through cleanup. GPU availability was **not tested** in this review.
- **Column interpretation:** update columns are weight coordinates, not fact IDs. Replace “which facts’ directions” with a separately defined attribution statistic or omit that claim.

No files changed. This is a review of the Write Engine’s numerical instrument; it supplies no behavioral evidence or F1 closure.

🌱 graft reported ~77,727 tokens saved (~$0.04); one successful call and one failed call.

