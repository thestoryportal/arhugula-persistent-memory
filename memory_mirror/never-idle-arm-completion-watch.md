---
name: never-idle-arm-completion-watch
description: As orchestrator, every dispatched build/review must have an armed completion watch; never end a turn with work in flight and no wake signal
metadata:
  type: feedback
---

2026-10-08→09: four Codex builders finished ~21:30–22:15 MDT and sat idle until 11:26 the next morning (~13 h, GPU idle) because MAESTRO ended its turn without a wake-up mechanism. Operator (on waking): "I don't understand why you and all sessions are just sitting idle all night. Giddy up…orchestrate the work."

**Why:** nohup'd Astra reviews and tmux Codex sessions are not harness-tracked, so nothing re-invokes the orchestrator when they finish. Overnight mode exists precisely so work continues while the operator sleeps ([[operator-overnight-autonomy-2026-10-06]]).

**How to apply:** before ending any turn with work in flight, arm a Monitor (poll loop: Astra `-o` output file non-empty / process gone; tmux pane `Working (` → idle) and re-arm it on each 30-min expiry; or run reviews via Bash run_in_background. On each event immediately route the next step (review → fix round → commit → GPU dispatch). Idle builders get the next queued task at once; a session under ~45% context gets a fresh successor (e.g. codexy2) rather than a big new build.
