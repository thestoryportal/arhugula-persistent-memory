# audits/context

**Status:** Candidate only. This guide is not authoritative and publishes no report.
MAESTRO alone installs or updates the authoritative guide and its report pointers.

**Scope:** The context audit of this repository: roots and branches, copy signatures, scope overlaps, views and twins, queue and link locators, model locators, loaders and handoff contents.
**Owner:** MAESTRO owns this folder, the authoritative guide and every report in it. A builder may author only this candidate in its own lane.
**Method:** `audit(root, mode, config)` in `code/state/icm21_check.py` runs read-only and returns an AuditReport as JSON. It writes no guide and no report. MAESTRO's writer then saves one exclusive report per run at `audits/context/<UTC date>/<check_id>/`, holding `report.json` and `REPORT.md`. The `check_id` comes from the one captured UTC instant and the mode, so a second run never overwrites a first.

## Reading a report

- **complete:** `overall_status` is PASS or FAIL, and every required check has a result. Only a complete report answers "is the context sound".
- **partial:** some required checks have no full result. The report states what it inspected and what it excluded. A newer partial report does not replace the latest complete one; read both.
- **UNVERIFIED:** a check could not be proven, for example because custody or an admitted automation is missing. Treat UNVERIFIED as "not known", never as PASS. Nightly runs stay UNVERIFIED until an admitted automation actually runs at 02:00 UTC.

## Report pointers

None yet. No report has been published, so the latest complete report and the newer partial report are both UNVERIFIED. MAESTRO adds a pointer only when its report file exists.

## Context management (BINDING, operator directive 2026-10-09; copy this section into every handoff you write)

Operator: "Do not forget to manage context usage for yours and every team session you are orchestrating. Memento provides some tools to assist with this." "This context directive must be made durable through any and all handoffs."

- Watch your own context. Start a new piece of work only at 60% or more context left.
- At 45% or less left, with a long step pending: stop, and write the handoff file.
- At 40% or less left, or at once on any "Context compacted": stop starting work. Write `HANDOFF.md` in your lane folder (what is done, what is in flight, exact file paths, the next step, open risks, and this section verbatim). Then reply with your lane's HANDOFF token.
