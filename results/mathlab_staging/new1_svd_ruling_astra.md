FAITHFUL-GATE-FAILURE

1. **The implemented gate matches the frozen formulas.** `denom` is \(\|C\|_F^2\); the code sums squared residuals over nonoverlapping column blocks, then takes \(\sqrt{\text{sum}/\text{denom}}\). Orthogonality subtracts the correct identity columns and computes \(\sqrt{\text{sum}/d}=\|U^TU-I\|_F/\sqrt d\). No missing square root, denominator error, or extra dimension factor appears. See [implementation:150–168](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/new1_geometry.py:150) against [prereg:51](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/NEW1_ADAPTER_GEOMETRY_PREREG.md:51).

   **Precision caveat:** scaling and matrix products happen in fp32, followed by float64 residual arithmetic/reductions. That satisfies the literal “blocked products/float64 reductions”; these are not wholly float64 checks. Consequently, the reported errors combine decomposition and product-rounding error. The [failure record:5–6](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/mathlab_staging/runs/new1_20261010T022922.650234Z/worker_failure.json:5) correctly leaves predictions NOT COMPUTED.

2. **Not logically contradictory, but not demonstrated feasible for these inputs/backend.** Some fp32 matrices satisfy these tolerances exactly; this execution does not. A \(10^{-4}\) residual is plausible, but calling it *expected for this spectrum* is unsupported. LAPACK supplies dimension-dependent backward-error bounds, not a universal \(10^{-5}\) guarantee. Poor conditioning chiefly threatens small singular values and subspaces; it does not alone establish this reconstruction-error magnitude. [LAPACK analysis](https://www.netlib.org/lapack/lug/node97.html).

   **I found no earlier measurement of these covariance-SVD residuals.** The same-harvest [step-2 manifest:5–34](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/mathlab/m2_20261009T192823.926873Z/manifest.json:5) reports projector parity and update errors, including zero replay error—not SVD accuracy. [core.py:44–48](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/mathlab/core.py:44) discards the reconstruction operands; [step 3:294–320](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/mathlab/core.py:294) consumes replayed updates. The earlier full-shape SVD record is a **synthetic resource probe**, not numerical validation ([record:3–14](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/mathlab_staging/peak_svd_full.json:3)).

3. **Amendments, in increasing invasiveness:**

   **First choice:** explicitly amend §3:51 to require promotion **before scaling and blocked products**, retaining native-fp32 SVD, \(Q=U\), and existing tolerances. This isolates factorization error without changing the basis or native P. I would accept this diagnostic clarification; passing remains UNVERIFIED.

   **Tolerance relaxation:** least invasive to the mathematical objects, but changes §3:51’s numerical acceptance thresholds. Accept only with independently justified, frozen bounds—not a threshold chosen merely above this observation. Orthogonality has a useful explicit consequence:
   \[
   |E_{\rm all}(Z)-1|\le\|QQ^T-I\|_2\le\sqrt d\,e_{\rm orth}.
   \]
   The observed value permits approximately **0.00203**, not \(10^{-5}\), so retain §3:59’s actual complement checks and assess residual-to-gap bounds for selected subspaces.

   **Float64 refinement of U:** changes §3:51’s \(Q=U_{\rm native}\). Checking a refined basis while computing energies with unrefined U is unacceptable. Using refinement throughout changes the estimand and requires projector/subspace parity checks.

   **Separate float64 SVD:** changes “exactly one,” the prohibition on full float64 decomposition, \(Q\)’s definition, and §6’s resource assumptions. I would accept only with separately preserved native-fp32 P identity, explicit cross-basis projector-error bounds, cutoff stability, and resource validation.

   Preserve this INVALID run; any amendment remains **MATH-PROXY**, not evidence.

Graft: one failed call; savings unavailable.

