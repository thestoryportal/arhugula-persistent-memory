GO
Reviewer: GPT-6-Astra (high)

**BLOCKING**

- **RESOLVED — lone legacy worker falsely free.** `tools/dashboard_live.py:502–503` now selects a worker when no coordinator exists. Fresh control at `tools/test_dashboard_gpu_detector.py:551` passes across shared state, real bar, experiment and MathLab: busy, never free.
- **RESOLVED — CPU activity hides legacy details.** `tools/dashboard_experiment.py:259,317` preserves legacy rendering and composes CPU summaries. Controls at `tools/test_dashboard_gpu_detector.py:588,597,605` pass for live CPU, recorded CPU and malformed records, retaining stage, progress, results and log text.

**ADVISORY**

- One shared **active** detector confirmed: bar `:4`, experiment `:257`, MathLab `:157`. No silent idle fallback on tested denied/empty/malformed inventories (`dashboard_live.py:481–490`). Unused legacy `dashboard_report.py:27` remains.
- **120 tests PASS**, zero failures/errors/skips; no regression observed. Fix-report source hashes match; scoped diff check passes.
- One **110×40 render PASS**: 8 lines, maximum width 110, 0.223 s. GPU explicitly unavailable; CPU recorded/process unverified. Native inventory and interactive tmux remain **UNVERIFIED**.
- R1 performance advisory remains: full event scans and no `ps` timeout (`dashboard_live.py:287,482`). No source edits.

🌱 graft saved ~36,192 tokens (~$0.02); 1 successful call, 1 failed call.

