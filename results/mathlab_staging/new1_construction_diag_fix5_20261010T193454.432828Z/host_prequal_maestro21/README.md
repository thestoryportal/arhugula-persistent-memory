# NEW-1 FIX5 — r5 step 3 host pre-qualification (MAESTRO21, 2026-10-10)

Cleared by Astra r6 `GO-QUALIFY` (`results/mathlab_staging/new1_construction_diag_astra_r6.md`).
Run once, 20:04–20:06Z, on a quiet host (no MB/test job competing; only the standing dashboard, powerline and harness servers, plus idle leftover Drive fixture applets).
Commands are `build_report.md:106–108`, chained with `&&` so the batch stops on the first failure.

| Step | Result |
|---|---|
| `shasum -c candidate_sha256.txt` before | 14/14 OK (`step3_sha.log`) |
| `run_checks.py solo --count 20 --label host_prequal_solo_20` | 20/20 ok, 0 warnings (`../host_prequal_solo_20/`, `step3_solo.log`) |
| `run_checks.py full --count 3 --label host_prequal_full_3` | 3/3 × 205 OK, 0 `Warning:`, 0 `Exception ignored` (`../host_prequal_full_3/`, `step3_full.log`) |
| `shasum -c candidate_sha256.txt` after | 14/14 OK |

Step 3 is complete: 20/20 solo, 3/3 full. Step 4 (`fix5_inherited_mask_launch_01`, one run) still needs new operator authorization. The 100 solo + 10 full host bar is not yet earned.

## Step 4 — `fix5_inherited_mask_launch_01` (operator-authorized once via AskUserQuestion, 2026-10-10 ~20:09Z)

One run, 20:09:30Z, rc 0, quiet host (after the Drive suite finished). Receipts are in `../fix5_inherited_mask_launch_01/`.
Before exec: mask `[2,14]`, pending `[2,14]`. The fresh interpreter entered with the same mask and pending set and never reset the mask. Construction main refused at preflight with `INVALID-ENFORCEMENT: caller blocks SIGALRM or SIGINT`, Python return 2 and native exit 2. It made no calls, took no ownership and produced no output files. Mask, pending set, handlers and timer were identical before and after. Parent time was 0.000228 s (bar < 0.3 s). The loaded source hashes `744f0633…` / `919b3a11…` match the candidate. PASS.
