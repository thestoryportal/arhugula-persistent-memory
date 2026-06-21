---
name: background-monitor-no-premature-read
description: "When monitoring a long detached run, DON'T launch a background sleep then immediately Read its output file — it's empty until done (\"Wasted call\"). Use foreground sleep+check, or background + wait for the task-notification."
metadata: 
  node_type: memory
  type: reference
  originSessionId: f4d82a89-8dda-448d-8fc0-cf79fc2d6af9
---

Monitoring long detached experiment runs (setsid+disown GPU jobs, common in this program) this session wasted ~6–8 turns on the **anti-pattern**: launch `Bash("sleep N; grep log", run_in_background=true)` → then immediately `Read` the background task's output file → "**Wasted call — file unchanged**" (the file is empty until the sleep finishes).

**Do instead, one of:**
- **Foreground** `Bash("sleep N; <check commands>")` (no `run_in_background`) — it blocks for N seconds and returns the check output **directly** in one call. Simplest for a single timed check. (Foreground `sleep` may be blocked by some harnesses; if so, use the next option.)
- **Background sleep + WAIT for the `<task-notification>`** before reading. The runtime re-invokes you when the background command exits; only then read the result. Do **not** poll-Read the output file in between.
- For a condition that may finish early, prefer the **Monitor** tool (until-loop) over fixed sleeps.

**Pacing for GPU runs:** these jobs are minutes–hours; check on a ~15–30 min cadence (one sleep per check), not tight loops. The detached run itself is NOT harness-tracked (it's setsid'd), so you only get notified about your own sleep timers — size the sleep to the expected next milestone (gate ~8 min, per-arm ~5–10 min). See [[runpod-durable-experiment-launch]].
