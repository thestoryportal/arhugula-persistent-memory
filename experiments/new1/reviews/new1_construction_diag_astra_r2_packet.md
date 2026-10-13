# GPT-6-Astra (high) — pre-launch re-review r2: NEW-1 four-construction diagnostic

Read-only. Worktree = current dir. Your r1 verdict (`results/mathlab_staging/new1_construction_diag_astra_r1.md`) was NO-GO on one blocking finding (3): a SIGALRM between `Popen` returning and handle assignment left a live worker after `STOPPED-DEADLINE`. Your findings 1, 2 and 4–7 were clean. The operator authorized exactly one real run (`results/mathlab_staging/new1_construction_diag_authorization.md`); a defect found after launch costs it.

The builder revised:
- `tools/new1_identity_diag.py` 93a7b317… → c4601c6d…
- `tools/new1_construction_diag.py` 8949d220… → 87a4f542…
- `tests/test_new1_construction_diag.py` 11a127ee… → 40e2cd29…
- scope `results/mathlab_staging/new1_construction_diag_scope.md` b199b2e1… → 9b3f7ddd…, append-only: the section "Scope revision — 2026-10-10" describes the correction, and the prior 20,101 bytes are an exact prefix.

The evidence is in `results/mathlab_staging/new1_construction_diag_fix_20261010T074908.035652Z/`; the exact launch command is in `launch_command.txt` there. I reran the four NEW-1 suites on these hashes: 165 tests, OK (43 construction + 27 identity + 34 geometry + 61 supervisor). A GPT-family helper review said PROCEED; it is not binding.

`git diff -- tools/new1_identity_diag.py tools/new1_construction_diag.py` shows the full code change (uncommitted).

## Check against the code (cite file:line)
1. Finding 3 closed: no schedule (SIGALRM, SIGINT, or a slow or stalled `Popen` at any point from creation to registration) leaves a live or unreaped worker after the parent returns any terminal status. Construct at least one adversarial schedule beyond the builder's.
2. No arithmetic before release: neither worker entry can reach launch verification, numerical imports or `measure()` without a valid explicit release written after registration, RSS and deadline checks. A late, duplicate or forged release, writer EOF, or parent death before release all make the worker exit.
3. After release: the daemon guard ends the worker within ~0.1 s of parent death or the original absolute deadline, even while the main thread is blocked in native code. Say whether `os._exit` from a Python thread is reliable while the main thread holds the GIL inside a long native SVD call; if it is not, name the bound that actually holds.
4. The 600 s cap still holds end to end: the 5 s launch sub-bound and the 5 s cleanup bounds cannot add to it, and no path waits unboundedly on the launch thread.
5. Frozen science unchanged: arithmetic, inputs, gate, caps, output contract and outcome table match r1's reviewed versions byte-for-byte except the release-guard call, as the scope revision claims. The construction script's identity pin binds c4601c6d….
6. Launch command: `launch_command.txt` pins the revised scope and source SHAs; the nice computation is unchanged (my shell is at nice 10).

## Output
Under 600 words. The first line is exactly `VERDICT: GO` | `GO-WITH-CONDITIONS` | `NO-GO`. Then numbered findings, each with file:line, the concrete failing input or schedule, and the exact fix. For a check with no finding, write `N. none found — <what you inspected>`.

Not acceptable: restating the scope or the builder's report, or generic advice with no named failing input.
