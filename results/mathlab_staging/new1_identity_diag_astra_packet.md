# GPT-6-Astra (high) — NEW-1 identity diagnostic result: ruling + next step

Read-only. Worktree = current dir, HEAD a0047f4.

## Facts
- Real D-NEW1-b run halted INVALID-WORKER at `tools/new1_geometry.py:258` (`projector identity/probes mismatch`, L4) — `architecture_profile/s_new1_b_halt_diagnostic.json`, run dir `results/mathlab_staging/runs/new1_20261010T053945.884468Z/`.
- Operator-authorized diagnostic (`results/mathlab_staging/new1_b_identity_diag_authorization.md`, scope `results/mathlab_staging/new1_identity_diag_scope.md`, code `tools/new1_identity_diag.py`) result: `results/mathlab_staging/new1_identity_diag/identity_20261010T063237.614949Z/result.json` — MEASURED. Paths A and B: byte-identical normalized C (SHA ec2d803b…), each native projector byte-identical to the captured one (SHA 0281d02c…), 4/4 probes relative error 0.0, counts 8645. torch 2.8.0, 8 threads, 159 s, 5.1 GiB. The predeclared reading for "both match" is: halt not reproduced; investigate run-time state.
- Orchestrator code read: the worker's native recipe (`tools/new1_geometry.py:138–147, 150–161, 200–202, 526–542`) is algebraically the same as the diagnostic's (`tools/new1_identity_diag.py:98–104`): same np.divide, one fp32 `torch.linalg.svd(C, full_matrices=False)`, mask `s<0.005`, `Q[:,allowed] @ Q[:,allowed].T`, same `tensor_sha`, same probes; worker sets `torch.set_num_threads(8)` (`:507`), supervisor env OMP/MKL=8 (`tools/new1_supervisor.py:331`). Differences noticed: worker indexes with a Python list (`.tolist()`), diagnostic with a LongTensor; worker computes `denom` from C first; worker loaded adapters (safetensors) and the bundle with `mmap=True` before the SVD; the worker ran under the supervisor (nice 10 via supervisor, different allocation history → possible alignment-dependent BLAS/LAPACK results).
- The worker did not log which of count / SHA / probes failed, nor probe magnitudes.

## Decide
1. What does this result establish and not establish? Is the halt now best classified as a build/runtime defect in the worker path rather than a capture or fp32-reproducibility problem? Cite.
2. Rank candidate causes with how each would be discriminated.
3. Recommend the smallest next measurement that discriminates them (e.g. run the worker's exact functions — `load_covariance` → `covariance_basis` → `native_projector` → `projector_matches` — standalone on L4 with per-check logging, and/or inside the supervisor with added logging that is LAW#5-inert). State caps, whether it needs a new operator authorization, and what result would justify which single fix. Remember halt discipline: at most one speculative fix after a source read; rerun-never-patch; any new real attempt needs a new operator authorization.

## Output
Under 600 words. First line: `RULING: <one sentence>`. Then Q1–Q3 with file:line. Flag every item needing operator approval.
