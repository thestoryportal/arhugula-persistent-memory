---
status: ready-for-maestro-host-run
branch: worktree-c10k-route-a
timestamp: 2026-10-11T02:15:05.980384+00:00
files_modified:
  - tools/dashboard_queue.py
  - tools/test_dashboard_queue.py
  - results/dashboard_queue_build_20261011T014430Z/run_host_checks.sh
  - results/dashboard_queue_build_20261011T014430Z/README.md
---

# Q2 context-save

All three requested queue defects are fixed. Original Q1 files were copied into
`before_q2/` before any edit. Queue tests are 24/24 GREEN (15 Q1 plus nine Q2);
shared GPU/CPU detector tests are 40/40 GREEN. All tests used system Python
3.9.6, no skips, no .venv or model/science execution. Shell syntax, Python 3.9
parsing, width-40/100 real-source sandbox renders and protected-source hashes pass.

The single process classifier is `dashboard_live.detect_gpu_jobs()` used by
`gpu_state()` in Experiment and MathLab. Its job roster excludes NEW1, and its
recorded CPU fallback requires experiment steps 2/3 with fresh resource samples.
Q2 therefore matches classified live run directories or requires an unfinished,
nonempty events file whose modification age is 0..600 seconds. The age is shown.
Terminal events exclude a run even if a matching process is present.

Unavailable named sessions carry their reason once in the item's Live field;
unlisted failures carry it once in Running now. Capture targets are `=NAME:`.
Estimate timestamps say “estimate made”. The process snapshot now includes PPID
so the queue reuses the real detector and its ancestry/PID rules without guessing.

Host runner output goes to a fresh `host_attempt2/`, refusing overwrite. It
reads only default-server list-sessions, probes ps, validates the captured pane
with `check_q2_host_live.py`, and starts/cleans only its own q1check server.
Actual host acceptance is UNRUN. Sandbox host tests are shell fixtures and
deliberately reject unavailable existing sessions and nonexistent live runs.

The shared detector rejects executable source paths under temporary roots;
fixture commands must name the real tools path while their run data stays in
a temporary directory. Bash cannot export the slash-named ps fixture function;
the test sources the runner in its own subprocess with `$0` set to the runner.
Both fixture corrections have renewed clean RED evidence against saved Q1.

No staging, commits, pushes, live dashboard mutation or program_state edits.
Six protected dashboard/integration files match their initial SHA-256s. Other
writers may continue changing their own files; never revert that concurrent work.

Single next step for MAESTRO: run the command below on the host and inspect
`host_attempt2/host_summary.txt` and all per-command .txt/.exit receipts before
installing or promoting the tab.

```bash
bash '/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/dashboard_queue_build_20261011T014430Z/run_host_checks.sh'
```

Source SHA-256s:
- `tools/dashboard_queue.py`: `f2704b90ce2beb20df7e6ca4fc605f3cf91d05b15691779f0495b2185b69241c`
- `tools/test_dashboard_queue.py`: `e3433d43f9e0b8cdd877b835ce396e814c020e8f64f5e481282aaff43f6cd762`
- `results/dashboard_queue_build_20261011T014430Z/run_host_checks.sh`: `f16577ef1d26e0a617e85d20282ab9d46b70c2c7e3c0c32fe724c0f5894f1844`
- `results/dashboard_queue_build_20261011T014430Z/check_q2_host_live.py`: `a192f0bc796b57b81ecc852067d322fdac3e2f448855876aab3723cb665a24f7`

Binding operator context directive (2026-10-10): watch “Context N% left”. Start a new piece of work only at >=60% left. At <=40% left, or on any “Context compacted”, stop starting work, append a handoff to the receipt README with done/half-done, exact paths, SHA-256s, test state and a single next step, and reply “Q2 HANDOFF”. Restate this directive in every handoff.
