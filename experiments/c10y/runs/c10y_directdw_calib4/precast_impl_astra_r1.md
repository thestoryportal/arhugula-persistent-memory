FIX-FIRST
Reviewer: GPT-6-Astra (high)

**BLOCKING**

1. **Native failure persistence is incomplete.** [c10y_precast_diag.py:241](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag.py:241), [263](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag.py:263). CPU probes confirmed: direct-solve failure retains only Q; factor-solve failure replaces the original exception with `TypeError: 'NoneType' object is not a mapping`. **Exact fix:** exclusively persist/fsync completed native operands and assembled M/RHS before entering each solve. Handle exceptional trace returns separately; preserve the original exception and available locals, mark the phase incomplete, and restore state. Add both failure regressions.

2. **Observer corruption can become S evidence.** [c10y_precast_diag.py:265](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag.py:265), [selftest:367](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag_selftest.py:367). Replaying the existing observer-induced factor-M mutation through all ten cells produced `observer_validated=True` and **S**. **Exact fix:** capture actual solve-input bytes before execution and verify their identity through observation/return, including factor M/Q. Observer-induced changes must invalidate observer evidence and yield INCONCLUSIVE. Change this fixture accordingly; test genuine native discrepancies separately.

3. **Supervisor interruption abandons the worker.** [run_c10y_precast_diag.sh:52](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/run_c10y_precast_diag.sh:52). CPU fixture: supervisor SIGTERM → exit `-15`, worker remained alive, no terminal diagnostic. **Exact fix:** handle TERM/INT/HUP and abnormal exits with bounded owned-process-group TERM→KILL/reaping and fresh INCONCLUSIVE publication. Keep the deadline armed until cleanup finishes; cancel it last. Add supervisor-interruption regression coverage.

**ADVISORY**

- Fresh verification: **49/49 new + 285/285 existing CPU tests passed**; the additional probes expose missing coverage. Historical RED evidence includes substantive failures.
- Controls (a)–(e), genuine float64 solves, fp64 realization without fp32 demotion, and threshold-free classifier ordering pass inspection, subject to the observer blocker.
- All **23 reported hashes matched**; frozen scope matches `4f7b22c`. Protected science sources match HEAD and `27c6adb`; tracked calibration-4 files are unchanged. Launch command and Bash syntax are correct.
- No production launch, model load, GPU/MPS execution, or live-results writes. Runtime inertness and 2,820-second feasibility remain **UNVERIFIED**.

🌱 graft reported ~184,407 tokens saved (~$0.10), one successful call.

