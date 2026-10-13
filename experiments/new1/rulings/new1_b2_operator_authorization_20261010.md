# D-NEW1-b second attempt: operator authorization in principle (2026-10-10, ~22:50Z)

Asked by MAESTRO26 through AskUserQuestion after Astra's launch-readiness verdict
(`results/mathlab_staging/new1_launch_readiness_astra.md`, VERDICT: GO-WITH-CONDITIONS):

> Do you authorize exactly one full run (all five layers, about 45 minutes, capped at 11 GB of memory)?
> It would also count as the full-size resource test. If it runs out of memory or time, we get no answer,
> it counts as one of the three allowed stops, and nothing is retried without asking you. Before launching,
> I'd build a small launch recorder, write a launch manifest, and pause the dashboard's GPU poll for the run.

Operator answer: **"Authorize; launch when ready"** — MAESTRO launches once, as soon as the conditions are
met and the Mac is quiet, possibly overnight, and pushes the result.

Scope this grants (Astra C2 + Q7):
- Exactly ONE invocation of the endorsed command (verdict Q9), prereg pin
  `1616c860c38b65acbabb7ec472a1233b30291337e86a7739271df0c4bd1c9d0f` unchanged.
- This sole full five-layer attempt also serves as complete-workload resource validation.
- The invocation consumes this authorization even if admission refuses. No retry loop, second
  invocation, resume or cap increase. STOPPED-RESOURCE/STOPPED-DEADLINE = no geometry verdict,
  no queue change, counts toward the third-abort rule (`docs/MATHLAB_PREREG.md:284`).

NOT yet satisfied (launch is blocked until each holds and is receipted):
C1 worker niceness = 10 recorded at dispatch; C3 external dispatch capture (stdout, stderr, exit,
namespace, PID/group, post-exit disposition) + abort accounting; C4 launch manifest (HEAD, 8 hashes,
57420ab/ec7561d, r9/r13/readiness verdicts, command, budget, this file) + tracker propagation +
closeout; C5 fresh admission on a quiet host (dashboard --gpu-summary poll paused); free ≥ 21 GiB.
The binding one-invocation authorization file is completed from this record once the C4 manifest exists
(expected namespace `results/mathlab_staging/runs/new1_YYYYMMDDTHHMMSS.ffffffZ`).
