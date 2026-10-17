# Ledger and metrics
Part of the tickets guide. Router: `_system/governance/TICKETS.md`. Roots (L, M, S, W, TD, MEM, HO): `00-roots-and-roles.md`.

`TD/ledger.tsv` (columns `utc ticket event rc detail`, UTC; speak MDT = UTC-6) is the trace of every ticket. Events: `dispatch` (mklane.sh); `build`, `blocked`, `verified`, `ruling`, `install` (MAESTRO by hand); `start`, `mutants`, `tests`, `close`, `wait`, `admit`, `probe`, `prereview`, `astra`, `ready`, `stop` (ship.sh); `land`, `merged`, `lane`, `branch`, `hygiene`, `done`, `wait`, `stop` (train.sh, or ship.sh with TRAIN=0). Write the hand rows too: a decision missing from the ledger is missing from every report built on it.

Two rc values mislead a reader who counts failures by rc. A fix-round close row carries the close's non-zero rc although the round succeeded, for example `close 2 fix round: open PR #95, head ... pushed` (ship.sh:382): count it as a close. A `stop` called with rc 0 is written as 1 (ship.sh:48), so every `stop` row is non-zero.

`TD/METRICS.md` (operator, 2026-10-16: "Proceed with the current workflow tracking all metrics for observability."): one row per ticket with dispatch, builder done, each fix round, gate (mutants killed/total, seconds), close, pre-review (minutes, verdict, BLOCKING), Astra (minutes, verdict, BLOCKING), ready, train minutes, merged, dispatch-to-merged minutes against 15, and the cause of each overrun. Derive the times from the ledger. Example: `L/w1opt/followup-318/METRICS.md`. Pre-review value (catches against minutes added) feeds Step 327.

- Count landed tickets from `gh pr list --state merged`, never from a running tally; a tally drifted by one across five reports to the operator [R24].
- The dashboard `tickets` tab (`M/code/apps/dashboard/dashboard_tickets_tab.sh [session]`, added by `M/code/apps/dashboard/team_dashboard.sh:35`; view `M/code/apps/dashboard/dashboard_tickets.py`, data `M/code/apps/dashboard/dashboard_tickets_data.py`) reads every LEAN folder with tickets/: TD/tickets, TD/ledger.tsv, review rounds, git, one `gh pr list`. It shows one review round per ticket [G11]. `L/metrics/tickets.csv` and `L/metrics/sessions.csv` were built by hand and have no writer; do not rely on them [G11].
- The old board `L/board.py` (recut tickets from git and gh) is superseded by the tab.

