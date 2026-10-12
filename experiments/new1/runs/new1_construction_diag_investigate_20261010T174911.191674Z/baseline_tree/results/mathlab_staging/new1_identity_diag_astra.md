RULING: The capture is reproducible in the measured configuration; prioritize a worker-path implementation/runtime discrepancy, but neither a specific defect nor general fp32 reproducibility is established.

**Q1 — Established versus unresolved**

Both normalizations produced identical C bytes; both projectors matched the captured SHA, count 8645, and all four probes exactly (`results/mathlab_staging/new1_identity_diag/identity_20261010T063237.614949Z/result.json:5–109`). I verified the result SHA against its MEASURED terminal receipt.

This rejects normalization arithmetic as the explanation **in this configuration** and demonstrates capture reproducibility there. Apply the predeclared “both match → investigate original runtime state” rule (`results/mathlab_staging/new1_identity_diag_scope.md:47`).

Classify the original run as **INVALID-WORKER; cause unresolved, worker-path discrepancy suspected**. Do not promote “build defect” to established fact or exclude runtime-dependent floating-point variation. No geometry, locality, projector-fidelity, or F1 conclusion follows.

Crucially, the original count check remains unknown: `projector_matches` returns immediately on count disagreement, then accepts SHA equality, otherwise checks probes (`tools/new1_geometry.py:230–240`). The earlier inference that SHA **and** probes failed used another measurement’s count, not this worker’s logged count (`architecture_profile/s_new1_b_halt_diagnostic.json:20–23`).

**Q2 — Ranked hypotheses, all unverified**

1. **Projector construction differs operationally.** Worker gathers once, then computes `Q@Q.T`; diagnostic and producer independently gather each operand (`tools/new1_geometry.py:200–202`; `tools/new1_identity_diag.py:98–101`; `experiments/track_c/c10e_bandknob.py:173–175`). Algebraic equivalence does not establish identical floating-point execution. Discriminate shared versus separately materialized operands while holding U and indices fixed; separately vary list versus LongTensor indexing.

2. **Intervening worker computations/runtime state.** The worker performs a complete float64 SVD and blocked validity calculations **between native SVD and projector construction**, beyond the reported preliminary denominator calculation (`tools/new1_geometry.py:154–197`). Compare native U/s/mask fingerprints before and after this interval, then projector outcomes. Adapter loading/allocation history is another contextual difference (`:513–537`).

3. **Gate arguments, capture consumption, or provenance discrepancy.** Log actual/expected counts, expected SHA, probe identities, source/input hashes and exact gate result. Both diagnostic and worker use `mmap=True`; mmap alone is not a distinguishing feature (`tools/new1_identity_diag.py:127`; `tools/new1_geometry.py:527`).

4. **Residual backend/run variation.** Consider only after controlled comparisons. Diagnostic already used eight threads and nice 10; its backend reports Accelerate, so OMP/MKL settings alone do not establish identical execution (`result.json:125–135`).

**Q3 — Smallest next measurement**

**[OPERATOR APPROVAL REQUIRED: new diagnostic build/execution scope.]** First use one pinned L4 native SVD and a predeclared four-construction comparison: list/LongTensor indexing × shared/separately gathered operands. Reuse identical U/s/mask; release projectors sequentially. Invoke the unchanged `projector_matches`; independently report both counts, SHA and every probe residual, plus operand hashes/strides/storage relationships.

Proposed caps: **600 s, 11 GiB observed family RSS, eight CPU threads, nice 10, fresh fail-closed admission, <1 MB scalar output, no retries, dense persistence or adapter energies**. Previous authorization covered one already-consumed diagnostic (`new1_b_identity_diag_authorization.md:3–7`).

If construction alone separates failure from capture agreement, justify **one reviewed, failing-first construction fix**, preserving thresholds. Otherwise **no speculative fix**: request separately authorized exact-worker L4 execution, including float64/check interval and supervisor context, stopping at identity. Prove logging LAW#5-inert; unchanged code text alone is insufficient.

**[OPERATOR APPROVAL REQUIRED]** Any subsequent real attempt needs fresh authorization/processes/output namespace. Preserve the original HALT; never patch its verdict, relax tolerance, or iterate fixes (`CLAUDE.md:38–40`).