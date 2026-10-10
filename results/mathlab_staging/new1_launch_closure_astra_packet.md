# Astra — NEW-1 launch condition-closure check (C1–C5), D-NEW1-b second attempt

You issued GO-WITH-CONDITIONS (`results/mathlab_staging/new1_launch_readiness_astra.md`). The operator has
authorized exactly one run. Before MAESTRO dispatches, check whether each condition is CLOSED by committed
evidence at the live HEAD (`git rev-parse HEAD`; branch worktree-c10k-route-a). Read-only. Do not run the
supervisor, worker, .venv Python, or the test suites.

## Evidence to check
- **C1 (worker absolute niceness 10).** Your Q2 concern was real: the main tmux server (and every pane on it)
  runs at niceness 10, so a launch from there would have put the worker at 20 (`tools/new1_supervisor.py:640`
  requests +10). Resolution: dispatch only from a separate operator-started tmux server `tmux -L new1` at
  niceness 0. The recorder refuses unless its own niceness is 0 and SIGINTs the supervisor if the observed
  worker niceness != 10 — read `tools/new1_dispatch.sh` (own-niceness check after "Absolute worker nice 10",
  worker check near `/bin/ps -o nice=`).
- **C3 (external dispatch capture + abort accounting).** `tools/new1_dispatch.sh`, `tools/new1_dispatch_report.py`,
  `tests/test_new1_dispatch.py` (c99b475 + host fix c1a06ea). Host GREEN run by MAESTRO from the niceness-0
  server: `results/mathlab_staging/new1_recorder_build_20261010T225651Z/maestro_green_02/` (test.log: Ran 42, OK;
  command.json own_niceness 0); host RED `maestro_red_02/` 42/42 fail. Pre-checks refuse without consuming the
  authorization; `invocation.json` is the consumption boundary.
- **C4 (manifest + trackers + closeout).** `results/mathlab_staging/new1_launch_c4_20261011/`:
  `launch_manifest.md`, `hashes.sha256` (8 readiness files + recorder trio), `new1_b2_one_invocation_authorization.md`.
  Closeout: `LLMDB_ROOT=$PWD /usr/bin/python3 -B tools/closeout_check.py D-NEW1-b` (you may run this).
  Verify `shasum -a 256 -c results/mathlab_staging/new1_launch_c4_20261011/hashes.sha256`.
- **C2 (single attempt = full-workload resource validation)** — recorded in the authorization file.
- **C5 (fresh admission on a quiet host)** — happens at dispatch: dashboard `--gpu-summary` poll paused, no other
  Python, the recorder's read-only admission dry probe before consumption, free >= 21 GiB
  (`NEW1_DISPATCH_MIN_FREE_KIB` unset). Judge whether the recorder's pre-checks make C5 enforceable.

## Questions
1. For each of C1–C5: CLOSED / CLOSED-AT-DISPATCH / OPEN, with file:line.
2. Does the recorder's launched command equal your Q9 endorsed command exactly (`tools/new1_dispatch.sh:193,216-221`)?
3. Any path where a pre-check failure would consume the authorization, or a launch could proceed with the
   worker at niceness != 10 undetected?
4. Anything else blocking one dispatch.

End with exactly one line: `VERDICT: GO` or `VERDICT: GO-WITH-CONDITIONS` or `VERDICT: NO-GO`.
