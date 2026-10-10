# Astra r8 packet — NEW-1 FIX5 real construction diagnostic: acceptance + outcome-rule ruling (MAESTRO23, 2026-10-10)

You are the binding cross-family reviewer. Read the repo yourself; cite file:line. Read-only.

## Subject
The ONE operator-authorized FIX5 real construction diagnostic ran (commit 0c550ae).
- Evidence/README: `results/mathlab_staging/new1_construction_diag_fix5_real_dispatch_20261010T2031Z/README.md` (preconditions, command, stdout).
- Output namespace: `results/mathlab_staging/new1_construction_diag/construction_20261010T203101.002212Z/` — `result.json` (sha256 7e03238c2f6d135d5f1409b1a10f5b4e92dcdb394bcd8a129a11ba58c007d7a7) and `receipt.jsonl`.
- Your r7 verdict that set the acceptance terms: `results/mathlab_staging/new1_construction_diag_astra_r7.md` §5.
- Scientific scope and outcome rule: `results/mathlab_staging/new1_construction_diag_authorization.md`; scope `results/mathlab_staging/new1_construction_diag_scope.md`.

## MAESTRO's reading (verify or refute each)
1. Acceptance (r7 §5 item 5) holds: exit 0; only the two files, 20,594 B total; final receipt `terminal`/`MEASURED` with `result_sha256` equal to the file hash; 91.5 s of 600 s; peak family RSS 4.22 GiB < 11; 8 threads; nice 10; native U/s/mask/indices hashes identical before and after.
2. Result: the two `*_separate` constructions (two gathers, `right = U[:, index].T`; `tools/new1_construction_diag.py:117`) reproduce the captured projector SHA `0281d02c…` exactly with zero residual on all four probes. The two `*_shared` constructions (one gather, `right = left.T`) give projector `0fff6d76…`, all four probes NO-MATCH at relative error 2.96e-6–3.19e-6 against the 1e-6 gate. List vs LongTensor indexing has no effect. Allowed/excluded counts (8645/2363) match capture in all four.
3. Mapping to code: production `native_projector` (`tools/new1_geometry.py:200-202`) is the shared form (`Q=U[:,allowed]; Q@Q.T`), checked by the unchanged `projector_matches` via `validate_capture` (`tools/new1_geometry.py:243-261`, call at :542). The historical capture (`experiments/track_c/c10e_bandknob.py:175`) is the separate form (`U[:, idx] @ U[:, idx].T`).
4. Therefore the outcome rule's first branch applies: construction alone separates failure from capture agreement. The single reviewed, failing-first fix would change `native_projector` to build from two separate gathers to match the capture's construction. It would make no tolerance change and leave `projector_matches` and the engine unchanged. The fix goes to the operator together with any new real attempt.

## Questions
Q1. Do the acceptance checks hold, and is `MEASURED` valid for this run? Is anything in result.json or the receipt inconsistent?
Q2. Does the outcome rule's first branch apply? Weigh the stated limitations (four sampled probes; the original worker's float64/check interval and allocation history untested). Could the shared-vs-separate difference in this diagnostic differ from what actually failed in the halted D-NEW1-b worker (`architecture_profile/s_new1_b_halt_diagnostic.json`, prereg `docs/NEW1_ADAPTER_GEOMETRY_PREREG.md` Amendment B)?
Q3. Is the proposed fix the right single fix? Specify the failing-first test: what must fail on the current `native_projector` and pass after. Should the test be a small synthetic case where shared and separate gathers produce different bytes, or something else? Must the projector be bit-exact with the capture (SHA path in `projector_matches`), or is the 1e-6 probe path the intended acceptance? Is any other site that reuses a single gather for a capture-compared projector in scope (`tools/new1_geometry.py`, `tools/new1_identity_diag.py`)?
Q4. What exactly should go to the operator after the fix: which real attempt (the full D-NEW1-b worker re-run under the prereg?), with which caps, and does it need a fresh prereg amendment or Astra launch-readiness review first?
Q5. Any condition that blocks propagating this result into the trackers now (close-out of D-NEW1-b with this run's README as source)?

End with one line: `VERDICT: <BRANCH-1-FIX | BRANCH-2-NO-FIX | NO-GO>` and a numbered list of conditions.
