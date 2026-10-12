---
name: background-shell-niceness-10
description: The main tmux server was observed at niceness 10 on 2026-10-10; verify inherited niceness per launch; a pinned `nice -n 10` launch needs the operator-started `tmux -L new1` server at 0
metadata:
  type: feedback
---
2026-10-10: the first NEW-1 identity-diagnostic launch (`run_in_background` Bash, `nice -n 10 …`) ran at niceness 20 and the script's `nice 10 required` precondition refused it 34 ms in — a non-run, no arithmetic (results/mathlab_staging/new1_identity_diag/identity_20261010T063122.532923Z/NONRUN.md).

**Why:** the harness's background shell inherits niceness 10, and `nice -n` is an increment, not an absolute value.

**How to apply:** compute the increment from the current value: `CUR=$(python3 -c 'import os;print(os.getpriority(os.PRIO_PROCESS,0))'); nice -n $((10-CUR)) …`. Related: [[gpu-gate-refuses-any-venv-python]] (another precondition non-run class).

**Update 2026-10-10 (MAESTRO27, NEW-1 launch C1):** the source is the main tmux server (pid 21268, niceness 10), so every pane on it, MAESTRO's and every Codex builder's, starts at 10. The increment trick does not apply to `tools/new1_supervisor.py`: it hard-codes `nice -n 10` (:640, pinned bytes), so the supervisor itself must start at 0. A one-shot launchd job does run at 0, but macOS denies it file access on /Volumes/memit ("Operation not permitted", probe 2026-10-10), so it is not a route. What works: the operator starts a separate tmux server from a plain Terminal window (`tmux -L new1 new-session -d -s new1 -c <worktree>`). It runs at 0 with Terminal's file access, and MAESTRO drives it with `tmux -L new1 new-window/send-keys`. Codex's sandbox also denies the setuid `/bin/ps`, so process-observing tests run there too, not inside a builder.

**Update 2026-10-11 (MAESTRO33, Drive r13 candidate):** the Drive host commands (`host_commands_r13.sh`, `run_py39_coverage.validate_host`) also require niceness 0, and a new session on the main server inherits 10. Run them as `tmux -L new1 new-window -d -n <name> "/bin/sh <script>"` (check `ps -o ni` of the new1 server first). Capture labels are single-use (`mkdir exist_ok=False`), so a preflight refused at niceness 10 uses up that label: attempt 1's receipt was moved, with a NONRUN.md, into `operational_checks/maestro33_candidate_20261011T034641Z/`, and attempt 2 ran clean on new1.
