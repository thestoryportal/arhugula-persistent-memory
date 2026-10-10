# GPT-6-Astra (high) — r7 ruling: NEW-1 FIX5 post-qualification launch readiness (real construction diagnostic)

Read-only. Worktree = current dir. Do not run tests, launches or edits.

## Where we are
- r5 (`results/mathlab_staging/new1_construction_diag_astra_r5.md`, VERDICT: FIX5) set qualification §3 steps 1–5. r6 (`…_astra_r6.md`, VERDICT: GO-QUALIFY) cleared step 3 on the committed FIX5 bytes (7b547d1).
- MAESTRO21 ran steps 3–5 on the host. All passed. Commits 602faf5 (step 3), 2970a78 (step 4), f846509 (step 5). The receipts README is at `results/mathlab_staging/new1_construction_diag_fix5_20261010T193454.432828Z/host_prequal_maestro21/README.md`.
- The real diagnostic has never run. Its operator authorization (06:40Z, before FIX1–FIX5) is `results/mathlab_staging/new1_construction_diag_authorization.md`: ONE run on one pinned native L4 fp32 SVD, four constructions, unchanged `projector_matches`, caps of 600 s, 11 GiB family RSS, 8 threads and nice 10, fresh fail-closed admission, < 1 MB scalar output, no retry, plus Astra's outcome rule. r4 (`…_astra_r4.md:54`) and r5 §3 item 5 both say real-diagnostic approval is separate from host qualification.

## Candidate (`RECEIPT/candidate_sha256.txt`; RECEIPT = `results/mathlab_staging/new1_construction_diag_fix5_20261010T193454.432828Z`)
tools/new1_construction_diag.py 744f063374a766efbfffc5a1ede73be04a323210e6b4dad48e569e5a41545ec3
tools/new1_identity_diag.py 919b3a11a836973ea4c0d2abdd2514634ea62792e6009e828a63d81f297c3d0d
results/mathlab_staging/new1_construction_diag_scope.md 19dda1126da0f2df2fa5418583cbcd1ba6a4be8411fcb52965b7396e369b9217
tools/new1_supervisor.py a69d410724b65a5dbacaf8e34fc45b73c9f545daf54eda9b6cfeb150e344557b (unchanged; skipped-wait issue at `:411–428` open per r5/r6)
The remaining entries are tests, the geometry module, the runner, the controls and the launcher. Verify all 14 with `shasum -a 256 -c RECEIPT/candidate_sha256.txt`.

## Evidence for steps 3–5 (read raw receipts, not only the README)
- Step 3: `RECEIPT/host_prequal_solo_20/` (21 files), `RECEIPT/host_prequal_full_3/` (130 files), logs `host_prequal_maestro21/step3_*.log`.
- Step 4: `RECEIPT/fix5_inherited_mask_launch_01/` (5 files), `host_prequal_maestro21/step4_stdout.log`. Operator authorized exactly one run (~20:09Z).
- Step 5: `RECEIPT/host_solo_100/` (101 files), `RECEIPT/host_full_10/` (431 files), logs `host_prequal_maestro21/step5_*.log`.
Do not list these directories in full; glob or count. They hold 100+ long filenames.

## Proposed real launch command (MAESTRO's derivation, not yet reviewed)
FIX5 left no release manifest or launch command. MAESTRO took FIX4's `results/mathlab_staging/new1_construction_diag_fix4_20261010T104024.648040Z/launch_command.txt` and substituted only the FIX5 scope and source SHAs:
```
new1_nice_increment=$(LLMDB_ROOT="$PWD" .venv/bin/python -B -c 'import os,sys;current=os.getpriority(os.PRIO_PROCESS,0);sys.exit("starting niceness exceeds 10") if current>10 else None;print(10-current)') || exit "$?"
LLMDB_ROOT="$PWD" LLMDB_DEVICE=cpu CUDA_VISIBLE_DEVICES='' OMP_NUM_THREADS=8 MKL_NUM_THREADS=8 PYTHONDONTWRITEBYTECODE=1 /usr/bin/nice -n "$new1_nice_increment" .venv/bin/python -B tools/new1_construction_diag.py --scope-sha 19dda1126da0f2df2fa5418583cbcd1ba6a4be8411fcb52965b7396e369b9217 --source-sha 744f063374a766efbfffc5a1ede73be04a323210e6b4dad48e569e5a41545ec3
```
Main entry is `tools/new1_construction_diag.py:217–257`. Free space on memit is 80 GiB.

## Rule on each, separately
1. **Steps 3–5 conformance.** Do the raw receipts meet r5 §3 steps 3–5 as written? Check complete expected counts (205 per full run), stop-on-first-failure, no ResourceWarnings or ignored exceptions, no abrupt exits, timeouts or cleanup leakage, and candidate hashes OK before and after. Is any receipt inconsistent with its log?
2. **Open supervisor issue.** Does the skipped `process.wait()` at `tools/new1_supervisor.py:411–428` block the real launch? r5 noted that construction main uses `I.supervise`, not `S.supervise`. Confirm that from source.
3. **Authorization scope.** Does the 06:40Z authorization still describe the FIX5 run exactly (caps, constructions, outcome rule, no retry)? Or did FIX1–FIX5 change anything the operator approved, so the operator must see a revised description? Name each difference.
4. **Launch command.** Is the derived command correct for these bytes? Check the pins `--scope-sha` and `--source-sha`, and whether the scope or identity source pins any other hash that FIX5 changed. If the command is wrong or incomplete, give the exact corrected command and every precondition (engine fingerprint, admission quiet window, disk, receipts the run must leave).
5. **Readiness.** May MAESTRO bring this ONE real run to the operator for go/no-go now?

A passing host bar is the floor. It is not the ruling. Do NOT answer in the shape "100/100 and 10/10 passed, therefore launch-ready." Rule on items 2–4 from source and documents, each with file:line.

## Verdict
End with exactly one line:
- `VERDICT: GO-OPERATOR`: ready to put the one real run to the operator. List numbered preconditions and the exact command.
- `VERDICT: FIX6`: give each defect as a numbered criterion with its RED, and say which receipts survive.
- `VERDICT: NO-GO`: stop iterating on this diagnostic; say why.
