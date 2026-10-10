# NEW-1 FIX5 real construction diagnostic — the one authorized attempt (MAESTRO23, 2026-10-10)

Authorization: `../new1_construction_diag_fix5_real_authorization.md` (f5dbab5) after Astra r7 GO-OPERATOR (67de91e). One attempt, no retry.

Preconditions (r7 §5), checked immediately before dispatch:
1. Operator approval for exactly one attempt — f5dbab5.
2. 14-file manifest `../new1_construction_diag_fix5_20261010T193454.432828Z/candidate_sha256.txt`: 14/14 OK.
3. `LLMDB_ROOT="$PWD" .venv/bin/python -B tools/engine_fingerprint.py`: PASS, `d941a9fb…`, `_cov_cpu 3`. Dry `mathlab_admit.probe('cpu')`: allowed, no blocking processes/tmux, 28.6 GiB free memory. Launched after no `--gpu-summary` poll was running; MB25 builder idle.
4. Disk: 80 GiB free on memit (needs < 1 MB + 20 GiB).
5. Fresh namespace: `results/mathlab_staging/new1_construction_diag/` did not exist before dispatch.

Command: `dispatch.sh` (r7's exact two lines, wrapped with timestamps and exit capture). Stdout: `dispatch_stdout.txt`.

Outcome: started 20:31:00Z, exit 0 at 20:32:32Z (92 s of 600 s). Namespace `../new1_construction_diag/construction_20261010T203101.002212Z/` holds only `result.json` (19,293 B) and `receipt.jsonl` (1,301 B). Final receipt: `terminal` / `MEASURED`, `result_sha256` 7e03238c2f6d135d5f1409b1a10f5b4e92dcdb394bcd8a129a11ba58c007d7a7 = `shasum -a 256 result.json`. All r7 §5 item-5 acceptance checks hold. `MEASURED` means a valid diagnostic, not a science PASS; the authorization's outcome rule is applied separately with Astra.

## Outcome ruling — Astra NEW-1 r8 `VERDICT: BRANCH-1-FIX` (`../new1_construction_diag_astra_r8.md`)

Accepted as `MEASURED` (a valid diagnostic; no geometry or scientific PASS). Gather style alone separates failure from capture agreement. Both separate-gather constructions reproduce the captured projector SHA `0281d02c…` exactly with zero probe residual. Both shared-gather constructions give `0fff6d76…` and fail all four probes at 2.96e-6–3.19e-6 against the 1e-6 gate. Index representation has no effect; counts 8645/2363 agree in all four. Production `native_projector` (`tools/new1_geometry.py:200-202`) is the shared form; the capture (`experiments/track_c/c10e_bandknob.py:173-175`) gathers twice.

Limitations: this does not establish the original worker's historical cause. The worker's float64 SVD/check interval and allocation history were not exercised, and its count, projector SHA and residuals were never logged. D-NEW1-b stays **INVALID-WORKER / predictions NOT COMPUTED**; F1 status is unchanged.

Next gates, in order (Astra r8 conditions):
1. Preserve this diagnostic and every historical HALT.
2. One failing-first construction fix: `native_projector` builds from two independent gathers of the same native U and unchanged indices. Acceptance stays count AND (SHA OR all four probes ≤ 1e-6); no threshold change. `tools/new1_identity_diag.py:105` already gathers twice.
3. Separately scoped lifecycle fix for `tools/new1_supervisor.py:411-424` (the exception path can skip `process.wait()`), reviewed. This blocks any full-worker launch.
4. Astra launch-readiness review, then fresh operator approval for ONE capped, fresh-namespace, full five-layer Amendment-B attempt (2,700 s, 11 GiB family RSS, 8 threads, nice 10, no retry).
5. Close-out with this README as fingerprint source; `closeout_check.py D-NEW1-b` ALL GREEN.
