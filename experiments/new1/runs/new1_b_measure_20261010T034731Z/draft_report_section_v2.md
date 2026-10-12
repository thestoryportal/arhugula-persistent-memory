

## Amendment B (D-NEW1-b) — DRAFT (2026-10-10 UTC; Codex MB3)

**NEW1 B MEASURE DONE; B remains BLOCKED on its required equal-cutoff-count check.** The operator's 2026-10-10 decision authorizes measurement FIRST for Astra option B. Exactly one real L4 native-fp32 comparison SVD and one full-shape float64 SVD were measured on CPU with eight threads. The float64 SVD took **159.296147042 s**; the complete profile took **258.023897875 s**, with process high-water RSS **8.056793213 GiB**. Its four frozen covariance checks pass; V orthogonality also passes as an additional diagnostic. However, native fp32 selects **8,645 allowed / 2,363 excluded**, whereas float64 selects **8,644 allowed / 2,364 excluded**. Equal cutoff counts **FAIL at L4**. Numerical validity does not remove that blocker. This is an append-only proposal in this report, **NOT an adopted prereg amendment, implementation authorization or real NEW1 run**.

Read the complete `results/mathlab_staging/new1_options_astra.md` and `architecture_profile/s_new1_a1_halt_diagnostic.json`. Astra's RECOMMEND-C is its spending recommendation; the operator separately chose to collect option-B resource evidence. No tolerance amendment A was adopted. Map cell: Write Engine / C10, descriptive stored-covariance geometry; this measurement establishes no behavioral result, calibration, queue utility or F1 closure. MathLab remains stopped.

### Measurement receipt, identity and execution boundary

The durable JSONL receipt is **`results/mathlab_staging/new1_b_measure_20261010T034731Z/receipt.jsonl`**; `summary.json` is a derived summary, and `profile.log`, `command.txt`, `baseline.json`, `profile_l4.py`, `verify_profile.py`, `smoke.json`, `watchdog_smoke.log`, `pre_measurement_review.md` and `harness_review.md` provide its provenance and fixture/review evidence. The measured child ran from **2026-10-10T03:47:49Z through 03:52:07Z**, exited **0**, and completed well within the 900-second spending limit. The parent initiates process-group SIGTERM at 900 s, with at most two seconds before SIGKILL escalation; that grace is explicit. The profile deliberately spawns no worker descendants. The native-call timeout fixture verifies SIGTERM termination, not every escalation/descendant case.

The receipt stream parses cleanly, contains exactly one start/finish pair per precision and one measurement_complete, contains no timeout/failure, and ends with a parent-observed child exit **0**. Every phase was flushed/fsynced before acknowledgment. Acceptance requires that complete sequence and successful process exit; a merely readable completion line does not establish fsync success. This is profiling evidence, not `events.jsonl` run-state authority; no NEW1 supervisor/worker dispatch or prediction events were emitted.

Input was only the pinned **11008×11008 L4** cache:

```text
/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/covariance_caches/Qwen_Qwen2.5-3B/wikipedia_stats/model.layers.4.mlp.down_proj_float32_mom2_t100_100000.npz
SHA-256: f6ae787454e5bae9eff52155ac699386351246b03e60ab68d728335b0c9a5b58
```

`tools/new1_geometry.py:134–143` supplied the unchanged normalization: positive scalar int64 moment count, `np.divide(mom2.mom2, mom2.count, dtype=np.float32)`, then C64 = C32.double(). Thus promotion occurs **after the registered fp32 division**, with no recentering, trace normalization, symmetrization, clipping or refinement. Hash/stat identity was verified before and after use. The native SVD used C32 once; the double SVD used that unchanged normalized C promoted to float64 once. No other covariance layer, model, adapter or harvest payload was computed or loaded. Native U32 remained live through the double/check phases; native Vh32 was released after its SVD, and C32 after promotion. The measurement did not materialize or validate captured native P, and did not compute cross-projector certification.

Environment: **Python 3.11.16, torch 2.8.0, NumPy 2.4.6, Darwin arm64**. The driver was **`torch.linalg.svd(..., full_matrices=False)` on CPU**, default CPU driver, no driver override/retry; the recorded build reports BLAS_INFO/LAPACK_INFO **accelerate**. Torch intra-op threads = **8**, inter-op = **1**; OMP/MKL/OpenBLAS/VECLIB/BLIS thread-limit environment values were 8. `LLMDB_ROOT="$PWD"` explicitly selected this worktree rather than the inherited main checkout. The exact command is preserved in `command.txt`.

Two sandbox limitations are preserved, not treated as admission passes. The optional shared admission probe raised `PermissionError` reading `/bin/ps`; real-study fail-closed admission is **UNVERIFIED**. The first namespace, `results/mathlab_staging/new1_b_measure_20261010T033955Z`, preserves an exit-1 receipt for an `os.nice(10)` refusal **before torch import, covariance load or any SVD**. The successful fresh namespace removes that denied scheduling syscall and explicitly records `nice_applied=False`; it is a standalone operator-authorized CPU measurement, not validation of the real study's nice-10 launch conditions. Neither denied operation was retried. The preflight read-only memory snapshot reported 48 GiB total and 88% free; that snapshot is not a workload peak measurement.

### Measured time, process high-water and five errors

| Phase | Wall time | Cumulative child high-water RSS at completion |
|---|---:|---:|
| Native-fp32 L4 comparison SVD | 76.273775500 s | 3.707580566 GiB |
| Full-shape float64 L4 SVD | 159.296147042 s | 7.908477783 GiB |
| Five blocked float64 validity checks | 21.215224875 s | 8.056793213 GiB |
| Sum of timed SVD/check phases | 256.785147417 s | — |
| Entire parent profile through successful exit | 258.023897875 s | **8.056793213 GiB** |

Peak RSS is **8,650,915,840 bytes**, from Darwin `resource.getrusage(...).ru_maxrss` in **bytes**. Child self high-water and parent RUSAGE_CHILDREN agree. These are kernel process high-water observations, not sampled RSS. Each phase number is cumulative; subtracting high-water observations would not establish an independent allocation/phase peak. Retained U32, imports and check operands are included; complete-study adapters, saved updates, native P construction/probes, cross-projector certificates and other work are not. The observed profile already exceeds the frozen **6-GiB** study cap.

All products/reductions used float64, with inner/output covariance-column blocks at most **256**. Denominators remain the frozen covariance Frobenius norm or sqrt(11008), as appropriate:

| Error | Measured value | Comparison threshold | Result |
|---|---:|---:|---|
| Symmetry, &#124;&#124;C−C.T&#124;&#124;F / &#124;&#124;C&#124;&#124;F | 0.0e+00 | 1e-6, unchanged frozen gate | PASS |
| SVD reconstruction, &#124;&#124;C−U diag(s) Vh&#124;&#124;F / &#124;&#124;C&#124;&#124;F | 1.373273220410387e-13 | 1e-5, unchanged frozen gate | PASS |
| PSD reconstruction, &#124;&#124;C−U diag(s) U.T&#124;&#124;F / &#124;&#124;C&#124;&#124;F | 2.733106641216668e-10 | 1e-5, unchanged frozen gate | PASS |
| U orthogonality, &#124;&#124;U.T U−I&#124;&#124;F / sqrt(d) | 1.207481948206866e-14 | 1e-5, unchanged frozen gate | PASS |
| V orthogonality, &#124;&#124;Vh Vh.T−I&#124;&#124;F / sqrt(d) | 1.225789475935223e-14 | 1e-5, additional diagnostic only | PASS |

There are **four frozen covariance checks**, including symmetry; V orthogonality supplies the requested fifth recorded error without inventing a fifth frozen acceptance rule. These checks validate this L4 float64 decomposition of stored C only. They do not turn the native/A1 halted attempts into valid outcomes.

### Cutoff comparison: B's required gate fails

| Decomposition | Allowed s < 0.005 | Excluded s >= 0.005 | Nearest absolute distance to real 0.005 |
|---|---:|---:|---:|
| Native fp32 | 8,645 | 2,363 | 4.351716489e-6 |
| Float64 | 8,644 | 2,364 | 7.845050470e-7 |

The native mask uses the original dtype's scalar comparison; the float64 mask uses float64. Exactly one sorted-index classification changes: **zero-based index 2363, one-based rank 2364**. Its native value is **0.0049956482835114** (<0.005), whereas the double value is **0.00500721146627674** (>=0.005). This is a comparison at sorted singular-value indices, not a claim of tracked eigenvector identity. The top-bin gap passes in both decompositions. The native bottom-bin gap is zero and fails; the float64 bottom gap is **0.0003054789133344472** and passes the unchanged rule. The numerical precision change therefore changes some registered subset behavior; it cannot be called native-geometry reproduction.

**Required equal cutoff counts: FAIL.** No cap proposal, reconstruction pass or missing cross-projector calculation repairs that failure. Do not force counts, drop the changed mode, change the cutoff or relabel the original runs. B as quoted below remains blocked before a real study. Cross-projector certification is separately **UNVERIFIED**, rather than reported as a measured norm failure.

Failure reflection: (1) native factorization error may shift a near-cutoff singular value; this is plausible with the recorded same-input/native-versus-double discrepancy, but not an independently isolated backend error bound; (2) B changes the basis precision/estimand, so equal-count parity can fail even when the double covariance gates pass; (3) an input, normalization or observation mistake could manufacture a count discrepancy—pin checks, unchanged loader, exact one-call receipts, reviewed formulas and small controls refute the obvious variants, without proving full-study parity. No further layer, driver, SVD retry or threshold search is authorized by this measurement task. The source-faithful stopping point is the recorded count FAIL, with any future method/scope decision belonging to the operator.

### Proposed append-only frozen-text changes — NOT ADOPTED

If ever adopted, Amendment B must explicitly supersede the affected clauses of **§3 line 51** (one full native-fp32 decomposition / Q = native U / prohibition of double covariance decomposition), **§6 line 128** (no full float64 C), and **A1 lines 182–186** (native geometry basis, exactly one decomposition, prohibition of double SVD and unchanged resource caps). Preserve all original frozen v2/A1 bytes and old-hash receipts. The following two paragraphs are quoted exactly from Astra's option B in `results/mathlab_staging/new1_options_astra.md`:

> “Per layer, compute one native-fp32 covariance SVD solely for captured-projector identity, then one float64 SVD of the unchanged fp32-normalized covariance promoted to float64. Define every geometry basis and subset from the float64 decomposition. Apply the existing reconstruction, PSD, orthogonality, complement, cutoff and tie gates to that geometry. Retain native projector parity ≤1e-6 separately; native reconstruction residuals are diagnostic. No symmetrization or clipping is permitted.”

> “Require equal cutoff counts and a certified cross-projector operator-error bound ≤1e-5, sufficient to bound normalized energy differences by 1e-5; failure invalidates projector-based interpretation. Full float64 covariance allocation is permitted. Execution remains blocked until complete-shape resource validation establishes compliant reserves and RSS.”

This proposes **one native and one double covariance SVD per layer**, each reused across all arms/controls. Q/s and geometry bins come from the double decomposition; the native U32/s32 mask constructs the original native-fp32 P for its separate captured count/hash or four frozen probes. Preserve all **1e-6 / 1e-5** tolerances, cutoff 0.005, k=1024, bin/tie rules, complement gates, excluded-energy parity control, ca/update/hash identity, controls and prediction logic. Native reconstruction residuals become diagnostic; captured-projector identity remains gated. No refinement, float64 normalization of raw moments, tolerance relaxation or retrospective reclassification is proposed. B establishes more accurate geometry of **stored covariance**, not behavioral causation or reproduction of the native geometry. The measured count FAIL prevents adopting these paragraphs as a runnable repair on the present L4 input.

### Cross-projector bound: exact required meaning and implementation gate

For each valid registered subset S in top/bottom/allowed/excluded, define the energy operators **G64,S = U64,S U64,S.T** and **G32,S = double(U32,S) double(U32,S).T**, interpreted as exact real products of the stored basis values. Require the equal cutoff counts first, then a **certified upper bound** eta_S >= ||G64,S−G32,S||2 with **eta_S <= 1e-5**. For every nonzero Z,

```text
|E64,S(Z) − E32,S(Z)|
 = |trace((Z.T Z / ||Z||F^2) (G64,S−G32,S))|
 <= ||G64,S−G32,S||2 <= eta_S.
```

The normalized Z.T Z is PSD with trace one, so that bound controls every registered normalized energy without testing a convenient finite set of updates. Native U32 is imperfectly orthogonal; exact-orthogonal-projector shortcuts may not be assumed. A possible sufficient certificate uses blocked Frobenius evaluation plus a rigorously bounded product/reduction roundoff allowance delta, accepting only **||computed difference||F + delta <= 1e-5**. Its backend-applicable roundoff bound must be established before claiming certification. A computed Frobenius estimate without delta or a power-iteration estimate is not such an upper certificate; failure of a sufficient Frobenius test does not by itself prove the operator norm exceeds the gate.

Keep the energy operator distinct from **Pnative = fl32(U32,N U32,N.T)**. The latter is the rounded native projector used for captured-source identity. A bound on rounded P alone does not certify the registered native-basis energies; conversely a basis-energy bound does not establish parity with the captured P without including native multiplication rounding. Any claim comparing to that actual P must name that target and include its rounding in the <=1e-5 certificate, while retaining the separate frozen native count/hash/probe parity <=1e-6. This certificate and captured-P checks were **not measured** here. Equal counts already fail, so the current DRAFT is blocked regardless of how a later certificate is implemented.

### Proposed time/memory amendment sized from the measurement — NOT ADOPTED

The sequential five-layer planning calculation is:

```text
5 × (native SVD + double SVD + five blocked checks)
= 5 × 256.785147417 s
= 1283.925737087 s.
Time proposal = round up to 300 s [1.50 × 1283.925737087 + 600 s]
              = 2,700 s (45 min), from before admission/hashing/imports.
Memory proposal = ceil_GiB[1.25 × 8.056793213 GiB] = 11 GiB.
```

The **50% time margin**, **600-s allowance for untimed work** and **25% memory margin rounded upward** are explicit planning assumptions, not measured upper bounds. The two SVDs alone scale to **1,177.849612711 s** for five L4-equivalent pairs; the measured checks add **106.076124376 s**. Other layers can differ, and other workload components, source parity and cross-projector certification remain unmeasured. Memory is **not multiplied by five**: stream one layer, release covariance workspace/check temporaries before update SVDs, reuse its basis for all arms/controls and release it before loading the next layer. Keep 256-column blocking and no materialized random dense controls.

Proposed future text, subject to review/adoption and actual complete-workload validation:

> Replace the 1,800-second spending cap with **2,700 seconds**, including admission, hashing, imports, all ten sequential covariance decompositions, check/certification work, controls, waits and serialization. Replace the **6-GiB observed worker-process-family RSS cap with 11 GiB**. Retain fail-closed CPU admission, one CPU worker/eight threads/nice 10, monitoring failure refusal, sampling cadence, the **6-GiB available-memory abort floor**, **8-GiB admission floor** and **300-second maximum wait within the total deadline**. Deadline/resource/I/O refusal yields STOPPED with no prediction verdict. Do not automatically raise any cap.

> Keep the native covariance-SVD reserve **5 GiB**, requiring **13 GiB** available. Add a float64 covariance-SVD cell reserve **11 GiB**, requiring **19 GiB** available, and raise the covariance-validity/cross-projector-check reserve to **11 GiB**, requiring **19 GiB** available. Retain the other declared reserves provisionally; validate every complete-shape cell with the actual retained operands before execution. Full float64 normalized C is permitted for the double decomposition only under these reviewed resource gates. Preserve flushing/fsync before gate acknowledgment and `events.jsonl` as the sole real-study state authority.

This would also supersede the numerical resource amounts in **§6 lines 113–128** and **A1 line 186**, with all failure semantics retained. The present one-layer high-water motivates an amendment; it does **not** validate the entire process-family RSS, all cell reserves, nice-10 timing or 2,700-second completion. Those remain **UNVERIFIED**. None of these proposals changes the current supervisor or preregistration. A real run would remain blocked by the measured equal-count FAIL, unimplemented certified cross-projector gate, complete-workload validation, amendment adoption/review and separate execution authorization.

### Verification, hashes, preservation and handoff

Small fixture verification passed before the real pair: a rotated positive PSD example yields all five errors zero; an indefinite covariance reconstructs exactly but fails PSD with error **0.3651483716701107**. No SVD or real input was used in those fixtures. A separate fixture stopped a child blocked in a native ctypes sleep in approximately **0.503 s**, returned 124, observed SIGTERM exit -15 and preserved two parseable fsynced receipts. The existing production/test/prereg files were not edited; therefore no production test rerun is claimed for this measurement-only task. The prior NEW1 synthetic-suite evidence remains its own evidence.

| Artifact | SHA-256 |
|---|---|
| Real L4 JSONL receipt | `9461275cb091469ee3ffda3af8c51e62ba75e361c93133d4100ded522cb7637a` |
| Profile source | `fd6c6516d63a0994c51b22939fa5fc2ebbd59eac6046b588684a8041643f1e25` |
| Derived summary | `ee6d7be4189a63abcae7a4a27baa64c7d4ef418caadd686142d2072e2d02f585` |
| Current prereg, **unchanged** | `216e8cfab513f0b555d8ae7908bd629e99e3b848cd2b43c054690962572cf771` |
| Geometry production source, **unchanged** | `3234b7f16b25d151d86ec508577abd42c1163a5b2b5318761b11b28675c2df67` |
| External Astra options, **unchanged** | `09b9fd139d6a032dbf4d85c64786a1457c6b36d6a7eed1403a0a1badc6b28817` |
| A1 halt diagnostic, **unchanged** | `cc85ae4e2e9821f92e8b655a7cd15b93003984d421e4aa90924579333e81a24f` |
| Preserved report prefix, 82,639 bytes | `e28aaaa9ed9eeb3786988c0539e159d72d202f552d92e3865cd02eda6c8cfc40` |

All original frozen v2/A1 prereg bytes and both halted attempts remain preserved; no past INVALID result, prediction status or criteria receipt is reclassified. No commits, real NEW1 study, other-layer arithmetic or code/prereg amendment was performed. Read-only reviewer identity is **GPT-6/Codex family, not Astra**; the primary Astra text is the separately recorded options ruling. Final receipt/draft review and scope audit are recorded alongside the measurement.

**Handoff:** Done: one L4 native-plus-double CPU pair, five errors/counts/time/high-water receipts, small formula/watchdog controls, append-only DRAFT B with quoted changes, certified-bound requirement and explicit budget assumptions. In flight: none after final review/audit. Exact paths: this report; successful `results/mathlab_staging/new1_b_measure_20261010T034731Z/`; preserved pre-numerical refusal `results/mathlab_staging/new1_b_measure_20261010T033955Z/`; unchanged `docs/NEW1_ADAPTER_GEOMETRY_PREREG.md` and `architecture_profile/s_new1_a1_halt_diagnostic.json`. Next: MAESTRO2/operator review the **equal-count FAIL** before any method decision; do not relaunch or implement this DRAFT as a passed repair. Open risks: cross-projector certification/captured identity uncomputed, full-study reserves/RSS/time unvalidated, scheduling/admission limitations. Numerical L4 PASS is not B acceptance.

**Binding context rule restated:** Watch `Context N% left` for this session and every team session. Before approximately **20%** remains, stop starting new work, write a handoff in the task report with done/in-flight work, exact paths, next steps and open risks, and notify the orchestrator for a fresh successor. Never approach full-window compaction. Every future handoff must restate this rule.
