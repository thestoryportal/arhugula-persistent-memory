# D-NEW1-b second attempt — binding ONE-INVOCATION authorization

Source: operator answer "Authorize; launch when ready" (MAESTRO26 AskUserQuestion, 2026-10-10 ~22:50Z),
recorded in `results/mathlab_staging/new1_b2_operator_authorization_20261010.md`. Completed by MAESTRO28
on 2026-10-11 from that record, after the C4 launch manifest (`launch_manifest.md`, same directory) existed.

This file authorizes EXACTLY ONE dispatch of the endorsed command (Astra readiness verdict Q9,
`results/mathlab_staging/new1_launch_readiness_astra.md:117-127`) through `tools/new1_dispatch.sh`
from the niceness-0 `tmux -L new1` server, prereg pin
`1616c860c38b65acbabb7ec472a1233b30291337e86a7739271df0c4bd1c9d0f` unchanged.

- Expected run namespace: `results/mathlab_staging/runs/new1_YYYYMMDDTHHMMSS.ffffffZ`.
- Consumed when the recorder writes `invocation.json` — even if admission then refuses.
- Budget (supervisor-enforced): 2,700 s wall; observed family RSS > 11 GiB stops; 8 threads; worker nice +10
  from a niceness-0 origin (absolute 10). Free space >= 21 GiB at dispatch; projected writes <= 1 GiB.
- No retry loop, second invocation, resume or cap increase. STOPPED-RESOURCE / STOPPED-DEADLINE = no geometry
  verdict, no queue change, counts toward the third-abort rule (`docs/MATHLAB_PREREG.md:284`).
- This sole full five-layer attempt also serves as complete-workload resource validation (Astra C2 + Q7).
