FIX-FIRST
Reviewer: GPT-6-Astra (high)

**BLOCKING**

- **False “free” with a lone legacy worker:** `tools/dashboard_live.py:502–503` excludes `_job` from `running` even when `jobs` is nonempty. MathLab consequently reports GPU free (`tools/dashboard_mathlab.py:161–165`), while the bar reports busy. **Fix:** prefer a coordinator, then fall back to any detected GPU job. Add a worker-only control across all three consumers.
- **Concurrent CPU activity removes legacy experiment details:** `tools/dashboard_experiment.py:241–273` returns the generic panel whenever CPU activity or CPU-record errors exist, suppressing the running C10 stage, progress, results and logs. **Fix:** retain the legacy GPU detail path and compose CPU/error summaries into its available space. Add a legacy-C10-plus-CPU render control; the existing legacy test only checks `running()` (`tools/test_dashboard_gpu_detector.py:514–523`).

**ADVISORY**

- Shared detector and requested aliases are present. Failed/empty/malformed inventory explicitly reports unavailable. Detector paths inspected perform reads, without launching science jobs.
- **114 tests PASS**, after temporary-fixture access was allowed. Tests are substantive, but miss both cases above. Source hashes match the report.
- One **110×40 render PASS**, approximately **0.10 s**: GPU unavailable; CPU recorded, process unverified. Successful native inventory timing and interactive tmux remain **UNVERIFIED**.
- Refresh work is unbounded: `gpu_state()` rereads every MathLab event stream and invokes `ps` without a timeout (`tools/dashboard_live.py:287,482`). Consider incremental reads and an explicit timeout-to-unavailable result.
- No source edits, commit or rebuild performed.

🌱 graft saved 0 tokens; 1 failed call (Node absent from PATH).

