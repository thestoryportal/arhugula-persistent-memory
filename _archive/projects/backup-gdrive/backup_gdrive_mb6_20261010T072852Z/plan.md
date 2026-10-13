MB6 authorized backup fix; no Drive calls, live backup, installation, launchd mutation, Git mutation, or shared-file edits.
Disk budget: under 20 MiB for receipts, applet compilation, and isolated local fixtures.
1. Retry/history: changing source after first partial sync; archive v0 must survive.
2. Configuration isolation: reject behavior-changing RCLONE_* and remote global overrides; explicit safety flags; reject simulated/skipped operations.
3. Ownership: start/terminal heartbeat under lock; held-lock refusal receipt separately; force admitted newer-run schedule.
4. Dead-PID heartbeat: stale/failed, with live-PID positive controls.
5. Per-attempt suppression: remove both first-attempt records and each individual suppression boundary.
6. Launcher: compile stub-exit-1 variant and run via osascript; require prompt exit 0; real denial UNVERIFIED.
Every new/tightened test is run RED before the matching production fix.
Context directive: at approximately 20 percent context remaining, stop starting new work, write done/in-flight/exact-paths/next-step/risks handoff in the build report, and notify MAESTRO4; carry this directive through every handoff.
