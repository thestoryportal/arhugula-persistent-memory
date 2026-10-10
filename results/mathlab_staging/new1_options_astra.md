RECOMMEND-C

Shelve NEW-1 as **HALTED-INVALID, predictions NOT COMPUTED**: repairing an uncalibrated MATH-PROXY now adds numerical and resource work without enabling queue action while D-ML-4 is stopped ([prereg:135](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/NEW1_ADAPTER_GEOMETRY_PREREG.md:135), [disposition:128–134](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/CORPUS/60_MATHLAB_HARVEST_REPLAY.md:128)). This is a spending recommendation, not falsification of NEW-1.

The A1 residuals confirm a faithful numerical-gate failure; predictions remain uncomputed ([diagnostic:16–25](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/architecture_profile/s_new1_a1_halt_diagnostic.json:16)).

**A — tolerance amendment: not defensible on the available justification.**

The affected frozen text is “SVD and PSD reconstruction relative errors **≤1e-5**; orthogonality error **≤1e-5**” and “**no tolerance relaxation**” ([prereg:186](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/NEW1_ADAPTER_GEOMETRY_PREREG.md:186)); §3:51 duplicates those gates.

With fp32 unit roundoff \(u=2^{-24}\), \(du=6.5613×10^{-4}\) and \(\gamma_d=du/(1-du)=6.5656×10^{-4}\). These exceed the observation **without fitting it**, but \(\gamma_d\) is not automatically a bound for these SVD, PSD, and normalized orthogonality residuals. [LAPACK’s analysis](https://www.netlib.org/lapack/lug/node97.html) supplies an unspecified dimension-dependent \(p(m,n)\), chiefly in spectral norm—not the required backend-specific constants and Frobenius conversions. SVD backward stability also does not independently certify PSD.

Thus **no justified numerical replacement is presently available**; substituting \(2×10^{-4}\), \(10^{-3}\), or \(\gamma_d\) would not constitute the requested derivation. Exact defensible disposition text:

> “Tolerance amendment A is NOT ADOPTED. All numerical gates remain unchanged pending an independently derived, backend-applicable bound for each registered residual.”

If such bounds were established, A would retain native-basis descriptive geometry, with weaker numerical certification. Required checks: actual complement identities, residual-to-gap subspace bounds, cutoff stability, unchanged projector parity, and prediction-margin sensitivity. Small reconstruction error alone cannot certify the selected subspaces.

Runtime remains approximately **400 s for five fp32 SVDs**, plus at least roughly **56 s** of check GEMMs at the supplied throughput, plus untimed remaining work. The measured synthetic peak is **4.609 GiB**; complete-workload RSS and completion within **1,800 s / 6 GiB remain UNVERIFIED** ([prereg:111–131](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/NEW1_ADAPTER_GEOMETRY_PREREG.md:111)).

**B — mathematically preferable repair, resource-blocked under current assumptions.**

Append an amendment explicitly superseding §3:51, §6:128 and A1:182–186, including “exactly one full … native-fp32” and “Q is the unmodified native U”:

> “Per layer, compute one native-fp32 covariance SVD solely for captured-projector identity, then one float64 SVD of the unchanged fp32-normalized covariance promoted to float64. Define every geometry basis and subset from the float64 decomposition. Apply the existing reconstruction, PSD, orthogonality, complement, cutoff and tie gates to that geometry. Retain native projector parity ≤1e-6 separately; native reconstruction residuals are diagnostic. No symmetrization or clipping is permitted.”

Add:

> “Require equal cutoff counts and a certified cross-projector operator-error bound ≤1e-5, sufficient to bound normalized energy differences by 1e-5; failure invalidates projector-based interpretation. Full float64 covariance allocation is permitted. Execution remains blocked until complete-shape resource validation establishes compliant reserves and RSS.”

B establishes higher-accuracy geometry of the **stored covariance**, not reproduction of native geometry or behavioral causation. Cutoff crossings and unstable boundary subspaces remain risks.

For \(n=11008\), \(n^3=1.334×10^{12}\). A **planning assumption** of \(10–20n^3\) operations gives 19–37 s at GEMM throughput; assuming 10–30% effective throughput gives **62–375 s per double SVD**, not a benchmark. Five double-plus-native decompositions therefore consume approximately **710–2,275 s before other work**: fitting 1,800 s is unproven.

Memory is worse: one double matrix is **0.903 GiB**. Standard [DGESDD workspace](https://www.netlib.org/lapack/explore-html/df/d22/group__gesdd_ga8941e5ff50de36580dae8940015e9cb0.html) plus input/U/V totals approximately **6.32 GiB**, before wrapper copies and other operands; plan **8–10 GiB**, UNVERIFIED. B therefore needs a separately justified memory amendment or validated lower-memory algorithm.

Preserve both halted attempts; any future amendment needs a fresh namespace and prereg hash.

🌱 graft saved ~110,192 tokens (~$0.06), 1 successful call.

