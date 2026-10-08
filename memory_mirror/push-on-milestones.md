---
name: push-on-milestones
description: Operator wants a phone push (PushNotification) at important program milestones, especially overnight
metadata:
  type: feedback
---
2026-10-08 ~02:40 the operator said: "Send me a push notification to my phone when any important milestones are achieved." Then: "Most importantly for milestones also, when research achieves something notable to our goals."

**Why:** the operator sleeps or steps away while the program runs autonomously and wants to know about real progress or problems without watching the dashboard.

**How to apply:** use PushNotification (one line, <200 chars, lead with the result). TOP PRIORITY: any research result notable to the F1 goal (a verdict/label reached, the 61/72 bar met or missed, a route opened or ruled out, a ceiling result) — say what it means for the goal in plain words. Also: a GPU run launched or its verdict reached; any HALT or failed gate; something awaiting operator ruling; a Codex build passing review and being admitted; recovery from an outage. Do not push routine progress (a subagent finishing, a commit, a watcher re-arm). Related: [[rerun-never-patch]], [[dashboard-live-derivation]].
