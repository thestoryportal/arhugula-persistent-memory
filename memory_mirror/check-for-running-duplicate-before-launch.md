---
name: check-for-running-duplicate-before-launch
description: A prior MAESTRO's background chain may already be running the same verification; count matching processes before launching another
metadata:
  type: feedback
---
Before launching a long verification (an `rclone check`, a test sweep, a hash pass), run `pgrep -f '<distinctive part of the command>' | wc -l`. If one is already running, wait on it instead of starting a second.

**Why:** 2026-10-10, MAESTRO18 launched `rclone check … --download --one-way` on the NEW-1 `events/` copy (pid 5961) while MAESTRO17's background chain was already running the same check (pid 5210). Two `--download` checks over 7,736 files doubled Drive traffic and host load for no new evidence.

**How to apply:** count first; never use `pgrep -fl` on fixture processes (their argv is a whole Perl program, ~6k tokens). Handoffs should name every background chain still running, with pid, so the successor can count against it. See [[context-management-every-session]] and [[never-idle-arm-completion-watch]].
