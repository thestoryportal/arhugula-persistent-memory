# Astra NEW-1 r9 — review of the single numerical fix (native_projector two-gather)

You are GPT-6-Astra, the cross-family reviewer for the LLM-as-Database program. Read-only review. Repo: this worktree, branch `worktree-c10k-route-a`, subject commit **57420ab**.

## Subject
Your r8 verdict (`results/mathlab_staging/new1_construction_diag_astra_r8.md`, VERDICT: BRANCH-1-FIX) ruled one numerical fix: make the native capture-compared projector use two independent gathers from the same native U and the same allowed indices, matching the producer (`experiments/track_c/c10e_bandknob.py:173-175`). Codex MB26 built it test-first:
- Source: `tools/new1_geometry.py` `native_projector` (~:200-203). Diff vs 018ce4d9: `Q=U[:,allowed]; Q@Q.T` → `U[:,allowed]@U[:,allowed].T`. Final SHA-256 ce43a26d….
- Test: `tests/test_new1_geometry.py::GeometryTests::test_native_projector_uses_two_independent_native_gathers` (final SHA-256 dba1606f…).
- Receipts: `results/mathlab_staging/new1_projector_fix_20261010T204522Z/` (README.md, RED/GREEN/RED-again logs, exit codes, SHA files, before/after copies). Host claims: RED 34/35 on 018ce4d9 (`1 != 2 : native projector must gather twice`), GREEN 35/35 on ce43a26d, RED-again on revert. MAESTRO24 reran the suite on the host: 35 OK.

## Questions
1. Does the change satisfy r8 Q3 exactly? Two gathers, identical indices, independent storage, native values/dtype, right operand equal to the left transpose. Are normalization, decompositions, masks, execution order, thresholds, `projector_matches`, `tensor_sha` and engine bytes all unchanged? Is there any other site in the worker that still builds the capture-compared projector with one shared gather?
2. Does the test meet r8 Q3's test spec? Synthetic native-fp32 U; operands observed while delegating to real tensor operations; failing on the current code, passing on the fix, failing again on revert; comparison to an independent two-gather reference; the unchanged capture gate exercised. Are the count-mismatch, SHA-success, probe-fallback and failing-probe controls retained, in this test or in existing ones (name them)? Can the test pass vacuously, for example if the observation hook misses a real gather?
3. Is the RED evidence real: the logged SHA at each moment, and the failing assertion is the two-gather one, not an incidental error?
4. Memory and runtime: does the second gather change the full-worker peak memory projection in a way that matters for the 11 GiB worker-family RSS cap and the 13/19 GiB SVD floors (r8 Q4 asked to reassess extra-gather memory without raising caps)? Give the size arithmetic for the largest layer.
5. Anything else that blocks this fix from entering the launch-readiness review (which will also need the separate supervisor reap fix, under build now by MB27)?

## Output
Numbered findings with file:line, each marked as blocking or not. End with exactly one line: `VERDICT: GO` or `VERDICT: GO-WITH-CONDITIONS` (list the conditions) or `VERDICT: NO-GO`.
