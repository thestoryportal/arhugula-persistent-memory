# Attempt 1: non-run (environment), 2026-10-11T03:47:48Z

MAESTRO33 launched `run_candidate.sh` in a tmux session on the main server (pid 21268), which runs at niceness 10 (`memory_mirror/background-shell-niceness-10.md`). `host_commands_r13.sh candidate` stopped at its host preflight (`validate_host`: "requires niceness 0") before any git operation: no candidate worktree, branch, index or commit was created. The fetch and identity capture (`identity.txt`, base a424085f) ran but nothing consumed them.

The preflight receipt was moved here from `operational_checks/commands/r13_host_preflight_candidate/` (capture labels are single-use) so that attempt 2 can use the reviewed entry point unchanged. Nothing from this attempt is reused: attempt 2 refetches, recaptures identity and uses a fresh candidate path, on the operator-started niceness-0 server `tmux -L new1`.
