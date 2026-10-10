---
name: never-idle-arm-completion-watch
description: As orchestrator, every dispatched build/review needs an armed completion watch; never end a turn with work in flight and no wake signal
metadata:
  type: feedback
---

2026-10-08→09: four Codex builders finished ~21:30–22:15 MDT and sat idle until 11:26 the next morning (~13 h, GPU idle) because MAESTRO ended its turn without a wake-up mechanism. Operator (on waking): "I don't understand why you and all sessions are just sitting idle all night. Giddy up…orchestrate the work."

**Why:** nohup'd Astra reviews and tmux Codex sessions are not harness-tracked, so nothing re-invokes the orchestrator when they finish. Overnight mode exists precisely so work continues while the operator sleeps ([[operator-overnight-autonomy-2026-10-06]]).

**How to apply:** before ending any turn with work in flight, arm a Monitor (poll loop: Astra `-o` output file non-empty / process gone; tmux pane `Working (` → idle) and re-arm it on each 30-min expiry; or run reviews via Bash run_in_background. On each event immediately route the next step (review → fix round → commit → GPU dispatch). Idle builders get the next queued task at once; a session under ~45% context gets a fresh successor (e.g. codexy2) rather than a big new build.

**Push rule (2026-10-09, operator asked "Have all commits been getting pushed?" — 87 were not, last push 2026-10-08 02:25):** after every commit, `git push origin <branch>` (authorized by D-C10r-rulings-10; never merge). Check `git rev-list --count origin/<branch>..HEAD` = 0 at every status report. Files >50 MB push with a GitHub warning; >100 MB would be refused — check before committing large artifacts.

**Re-arm trap (2026-10-09):** sessions that finish between an expiring watcher and its re-arm are invisible if the new watcher only looks for new events — on every re-arm, first report every pane that is already idle, then watch busy→idle transitions; also alert on low context (<25%).

**Background tasks (merged from a 2026-06 note):** never Read a background task's output file before its completion notification arrives — it is empty until the command exits ("wasted call"). Foreground `sleep` is blocked in this harness; for timed or conditional waits use Monitor (until-loop) or `run_in_background` and wait for the notification.
