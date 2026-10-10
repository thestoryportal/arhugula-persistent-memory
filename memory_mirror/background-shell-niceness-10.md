---
name: background-shell-niceness-10
description: Claude's background Bash shell already runs at niceness 10 — a script that requires nice exactly 10 needs increment 10 minus current
metadata:
  type: feedback
---
2026-10-10: the first NEW-1 identity-diagnostic launch (`run_in_background` Bash, `nice -n 10 …`) ran at niceness 20 and the script's `nice 10 required` precondition refused it 34 ms in — a non-run, no arithmetic (results/mathlab_staging/new1_identity_diag/identity_20261010T063122.532923Z/NONRUN.md).

**Why:** the harness's background shell inherits niceness 10, and `nice -n` is an increment, not an absolute value.

**How to apply:** compute the increment from the current value: `CUR=$(python3 -c 'import os;print(os.getpriority(os.PRIO_PROCESS,0))'); nice -n $((10-CUR)) …`. Related: [[gpu-gate-refuses-any-venv-python]] (another precondition non-run class).
