# NEW-1 (D-NEW1-b second attempt) — C4 launch manifest

Written by MAESTRO28, 2026-10-11 (UTC). Code HEAD at manifest time: `c1a06ea56ac85b2abb009e244d1d6d4fa83b7160`
(recorder host fix c1a06ea). The launch HEAD is the commit that contains this manifest or a later
tracker-only commit; the recorder checks it at dispatch (check 2c) and records it in `invocation.json`.

## Pinned files
`hashes.sha256` (this directory, shasum format, verified 11/11 OK): the 8 readiness-packet files
(`results/mathlab_staging/new1_launch_readiness_astra_packet.md:18-25`, all unchanged —
supervisor 3144949d…, geometry ce43a26d…, prereg 1616c860…) + the recorder trio
(tools/new1_dispatch.sh 287aa59f…, tools/new1_dispatch_report.py 95507923…, tests/test_new1_dispatch.py).

## Fix commits and reviews
- Fix commits: 57420ab (projector), ec7561d (supervisor reap).
- Astra verdicts: r9 `results/mathlab_staging/new1_projector_fix_astra_r9.md`; r13
  `results/mathlab_staging/new1_supervisor_reap_astra_r13.md`; launch readiness
  `results/mathlab_staging/new1_launch_readiness_astra.md` (GO-WITH-CONDITIONS, C1–C5).

## Conditions
- C1 (worker absolute niceness 10): the main tmux server runs at niceness 10, so a launch from it would put
  the worker at 20 (supervisor hard-codes `nice -n 10`, :640). Resolved by dispatching from the
  operator-started niceness-0 server `tmux -L new1`; the recorder refuses unless its own niceness is 0 and
  SIGINTs the supervisor if the observed worker niceness != 10.
- C3 (external dispatch capture + abort accounting): `tools/new1_dispatch.sh` + `tools/new1_dispatch_report.py`
  (MB33 c99b475, host fix MB36 c1a06ea). Host GREEN 42/42 OK at niceness 0
  (`results/mathlab_staging/new1_recorder_build_20261010T225651Z/maestro_green_02/`); host RED 42/42 fail.
- C4: this manifest + `hashes.sha256` + `new1_b2_one_invocation_authorization.md` + tracker propagation + closeout.
- C5 (at launch): pause the dashboard `--gpu-summary` poll; no other Python (incl. builders' tests);
  the recorder runs a read-only admission dry probe before consuming; free >= 21 GiB
  (`NEW1_DISPATCH_MIN_FREE_KIB` must be UNSET — test override; default 22020096 KiB).
- Engine fingerprint at manifest time: PASS (memit_main d941a9fb…, _cov_cpu 3). memit free: 80 GiB of 419.

## Endorsed command (verdict Q9, verbatim; reproduced by tools/new1_dispatch.sh:193,216-221)
```sh
cd /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a &&
/usr/bin/env PATH=/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin \
  TMPDIR=/private/tmp LLMDB_ROOT="$PWD" \
  LLMDB_DEVICE=cpu CUDA_VISIBLE_DEVICES= \
  OMP_NUM_THREADS=8 MKL_NUM_THREADS=8 PYTHONDONTWRITEBYTECODE=1 \
  "$PWD/.venv/bin/python" -B "$PWD/tools/new1_supervisor.py" \
  --prereg-sha 1616c860c38b65acbabb7ec472a1233b30291337e86a7739271df0c4bd1c9d0f
```

## Dispatch (C5), once, from tmux -L new1
`cd <worktree> && tools/new1_dispatch.sh results/mathlab_staging/new1_launch_c4_20261011/hashes.sha256 <launch HEAD> results/mathlab_staging/new1_launch_c4_20261011/new1_b2_one_invocation_authorization.md`
Budget: 2,700 s wall (~45 min), 11 GiB RSS, projected writes <= 1 GiB.
