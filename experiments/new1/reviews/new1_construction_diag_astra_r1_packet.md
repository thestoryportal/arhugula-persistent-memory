# GPT-6-Astra (high) — pre-launch implementation review: NEW-1 four-construction diagnostic

Read-only. Worktree = current dir. You ruled the next step in `results/mathlab_staging/new1_identity_diag_astra.md` (Q2/Q3). The operator authorized exactly one run (`results/mathlab_staging/new1_construction_diag_authorization.md`). The builder froze the scope at `results/mathlab_staging/new1_construction_diag_scope.md` (SHA b199b2e1…) and implemented it in `tools/new1_construction_diag.py` (SHA 8949d220…), with tests in `tests/test_new1_construction_diag.py` (SHA 11a127ee…). Build evidence: `results/mathlab_staging/new1_construction_diag_build_20261010T071253.399810Z/`; the exact launch command is in `launch_command.txt` there. I reran the four NEW-1 suites: 153 tests, OK. A GPT-family helper review said PROCEED; it is not binding.

Context: the real NEW-1 run halted INVALID-WORKER at L4 (`projector identity/probes mismatch`). The identity diagnostic did not reproduce the halt. This run asks one question: does projector construction alone (Python-list vs LongTensor index × shared vs separately gathered operands, same U/s/mask) separate failure from capture agreement?

## Check against the code (cite file:line)
1. The four constructions match the scope's table exactly, in fixed order, all from one SVD with identical U/s/mask/indices. A mutation check runs before and after.
2. `new1_geometry.projector_matches` is called unchanged on every projector. Counts, both SHAs and all four probe residuals are recorded independently even when the gate short-circuits. No tolerance or gate is altered or substituted.
3. Every cap is enforced fail-closed: 600 s total; observed process-family RSS strictly < 11 GiB; 8 threads; final parent/worker nice exactly 10; CPU only; fresh `mathlab_admit.probe('cpu')`; one worker; no retry. Look for any path that does arithmetic before admission or after an abort.
4. Output: only `result.json` + `receipt.jsonl`, < 1,000,000 B together, in a never-reused directory. No dense tensor is persisted. A result without the terminal MEASURED receipt is uncommitted.
5. Inputs: only the three pinned inputs are read, hash-verified around consumption, capture loaded `weights_only=True, mmap=True`. Nothing touches adapters or updates.
6. Reporting: the result cannot state a verdict, a classification, or any outcome beyond the scope's predeclared table. Diagnostic `MEASURED` is not a science PASS.
7. Launch command: the nice-increment computation is correct when the launching shell is already at nice 10 (mine is), and refuses above 10.

## Output
Under 600 words. The first line is exactly `VERDICT: GO` | `GO-WITH-CONDITIONS` | `NO-GO`. Then numbered findings, each with file:line, the concrete failing input or schedule, and the exact fix. For a check with no finding, write `N. none found — <what you inspected>`.

Not acceptable: restating the scope or the builder's closeout, or generic advice with no named failing input. The run is one-shot; a defect found after launch costs the authorization.
