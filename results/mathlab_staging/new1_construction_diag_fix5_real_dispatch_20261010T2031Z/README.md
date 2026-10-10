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
