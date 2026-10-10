GO

1. **Amendment scope is faithful.** `docs/NEW1_ADAPTER_GEOMETRY_PREREG.md:178–188` appends only the permitted precision clarification. I verified the original 31,931-byte prefix still hashes to `eaf7bc21…`; the complete document matches the supplied `216e8cfa…cf771`. Native SVD/Q/P, cutoffs, tolerances and caps remain unchanged. Line 188 preserves INVALID and predictions NOT COMPUTED, consistent with the halted run’s `worker_failure.json:4–6`.

2. **Blocked arithmetic is correct.** `tools/new1_geometry.py:156–174` computes, for output columns J and inner blocks K:
   - SVD: Σₖ U[:,K] diag(s[K]) Vh[K,J].
   - PSD: Σₖ U[:,K] diag(s[K]) U[J,K]ᵀ.
   - Orthogonality rows K: U[:,K]ᵀU[:,J], followed by the correct identity subtraction.

   Promotion precedes scaling/products; residuals and reductions remain float64. Normalizations are unchanged. Lines 178–183 return the original native U and s; subsets remain integer lists selected from native-fp32 s. Tests at `tests/test_new1_geometry.py:63–134` check object identity, unchanged bytes and native projector parity.

3. **Runtime remains a material uncertainty, not a demonstrated deadline violation.** `tools/new1_geometry.py:162–168` performs **1,849 block pairs × three GEMMs = 5,547 GEMMs/layer**, or 27,735 across five layers: approximately **40 trillion floating-point operations**. Reserving approximately 395 seconds for covariance SVDs leaves 1,405 seconds—requiring approximately **28.5 GFLOP/s for checks alone**, before other work. The old run reached checks at approximately 83 seconds (`results/mathlab_staging/runs/new1_20261010T022922.650234Z/events.jsonl:95`); that does not establish amended throughput.

   M3 Pro/eight-thread completion is **UNVERIFIED**. The geometry fixtures explicitly use one thread (`tests/test_new1_geometry.py:16`). A cheaper scheduling formulation is one full-inner-dimension GEMM per output block per check, caching promoted factors: `(U64*s64)@Vh64[:,J]`, `(U64*s64)@U64[J,:].T`, and `U64.T@U64[:,J]`. This preserves formulas and avoids full float64 C, but requires revisiting the test’s full-basis-allocation prohibition (`:122–123`) and validating RSS. It reduces dispatch/conversion overhead, not cubic arithmetic. Current uncertainty is explicitly allowed by prereg §6; this GO does **not** certify runtime.

4. **No stale executable SHA pin found.** `tools/new1_supervisor.py:432–442` requires the CLI hash, verifies complete bytes, forwards it and records it in the criteria receipt; `tools/new1_geometry.py:423,476` rechecks/records it. Tests compute fixture hashes (`tests/test_new1_supervisor.py:183–220`). Historical receipts correctly retain their old hash. I inspected the 84-test receipts; I did not rerun tests.

🌱 graft reported ~108,767 tokens saved (~$0.06), one successful call.