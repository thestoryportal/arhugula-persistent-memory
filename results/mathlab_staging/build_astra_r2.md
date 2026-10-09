FIX-FIRST
Reviewer: GPT-6-Astra (high)

**BLOCKING**

- **Persist-before-gate is incomplete.** [tools/mathlab_harvest.py:127](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/mathlab_harvest.py:127) clears `self.current`, then validates coverage **before** the persistence callback. Wrong capture order/count loses that write’s captured tensors; an edit exception bypasses persistence entirely. The halt handler at `:555` retains only gates/projection. **Exact fix:** preserve partial captures before clearing state or enforcing coverage, write them as diagnostic-only artifacts, and include their paths/hashes plus coverage/error details in the halt diagnostic. Keep failed writes excluded from analysis. Add CPU fixtures for coverage failure and mid-edit exception. Completed-arm persistence before LAW#3 already holds.

**ADVISORY**

- **§14 matches:** step 2 is `6540` in shell, runner and core; SVD reserve `5 GiB`; solve `9 GiB`, step 3 `1800`, index `300` unchanged. Actual prereg SHA matches `4852d1a2…`; exact hash verification remains intact.
- **Producer contract matches:** admission/experiment purpose, legacy attachment and terminal reuse guards agree with shared `fold()`. Core’s delta contains only the authorized reserve/deadline changes; science thresholds are unchanged.
- **Harvest admission matches §2.1:** every `check_gpu` refusal blocks; both named terminal sources and `no_other_coordinator_live_or_pending=true` are required and rechecked before import. The proposed `COMPLETE` and `HALTED-V7` records satisfy the schema; ASTRA’s cited diagnostic SHA matches. This does not establish current machine clearance.
- **Harvest command is correct.** The separate CPU example at [build_report.md:205](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/mathlab_staging/build_report.md:205) still uses `2700`; update it to `6540`.
- **Fresh verification:** `bash -n` PASS. MathLab suite blocked during import by unavailable writable temporary storage; dashboard **20 PASS / 33 temporary-directory errors**. Marimo returned zero but logged temporary-directory exceptions: **UNVERIFIED**, not PASS. No dispatch or source edits.

🌱 graft reported ~22,132 tokens saved ($0.01); 1 successful call, 1 failed call.

