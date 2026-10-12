---
name: decision-id-check-before-assigning
description: Before assigning a new D-<TRACK><n> Decision ID, git grep it — 6fb1e49 reused D-C10r-rulings-16, already the 09:50Z Drive go-live ruling
metadata:
  type: feedback
---
2026-10-10: MAESTRO27 recorded the operator's "C10Y deferred" ruling as D-C10r-rulings-16 (6fb1e49), but -16 was already the 09:50Z "Drive backup on with known limits" ruling (runbook §5.3/§13, b6564de) and is cited by D-C10r-gitmerge-1. MAESTRO28 caught it while propagating and renumbered the new ruling D-C10r-rulings-17 (436c507), with a correction note on the record rather than a rewrite.

**Why:** a reused ID makes the closeout gate and every pointer ambiguous — two rulings answer to one name, and propagation silently attaches to the wrong one.

**How to apply:** before writing any new Decision ID, run `git grep -ohE 'D-<TRACK>-<stem>-[0-9]+' | sort -V | uniq | tail -3` as a tracked-record check, then check the runbook and authorized untracked/in-flight records and coordinate the proposed ID with other writers before reserving it; do not infer globally unused from git grep alone. When you find a collision, add an ID-correction note to the newer record; never edit the older ruling. Related: [[context-management-every-session]].
