# D-NEW1-b — FIX5 real construction diagnostic: operator authorization (2026-10-10, MAESTRO22)

Asked via AskUserQuestion after Astra r7 `VERDICT: GO-OPERATOR` (`new1_construction_diag_astra_r7.md`, commit 67de91e). The question named FIX5 and its operational changes (r7 §3): more reliable cleanup, refusal of an unenforceable signal mask before work starts, possible fail-closed stop without a complete terminal report when time runs out. Caps restated: 600 s, family RSS < 11 GiB, 8 CPU threads, ~1 MB output; no fixes, no verdict, no retry.

Operator answer: **"Yes, run it once (Recommended)"** — exactly ONE FIX5 attempt, unchanged outcome rule, no automatic retry. Supersedes nothing: the 06:40Z authorization (`new1_construction_diag_authorization.md`) remains the scientific scope; this is the separate real-run approval r4/r5 reserved.

Dispatch preconditions are r7 §5 items 1–5, and the command is r7's exact command. Dispatch waits for a quiet admission window: the MB25 Drive builder's tests and any other non-exempt Python must be idle.
