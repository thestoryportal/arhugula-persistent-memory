FIX-FIRST

**BLOCKING**

1. **Tmux probe still fails open.** At [tools/c10w_p2_gate.py:80](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/c10w_p2_gate.py:80), `error connecting` exempts permission and connection failures. Model-free mocked probes reproduced `ok: true` for both **Permission denied** and **Connection refused**. This leaves B1 unresolved.

   **Exact change:** replace the condition with:
   ```python
   if trc != 0 and not re.fullmatch(r"no server running on [^\n]+", terr.strip()):
   ```
   Add regression cases requiring refusal for both errors while retaining admission for the recognized no-server response. No frozen-source change is needed.

**Non-blocking**

- Independently reran all **12 tests: PASS**; both shell syntax checks passed. Saved T3–T5 logs confirm the reported coordinator stops; no `p2_*` directory exists.
- Watch `results/c10w_oracle_logs/p2-coordinator.log`: coordinator status goes there, not the nohup `.out`. On resume, require a completion marker **after the current START**, since the log appends.
- Resume’s `SKIP` branch bypasses the subsequent HALT checks (`tools/run_c10w_p2.sh:25–27`); recheck HALT state before any resumed run.
- The 448-minute limit and disclosed first-pair retry risk remain unchanged. No other launch blocker found in the fold; live GPU availability was not independently verified.
- 🌱 graft reported ~42,942 tokens saved; 1 successful lookup, 1 failed attempt.

