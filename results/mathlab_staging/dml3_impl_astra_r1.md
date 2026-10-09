FIX-FIRST
Reviewer: GPT-6-Astra (high)

**BLOCKING**

- [tools/mathlab_harvest.py:155](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/mathlab_harvest.py:155): coverage failure persists operands and raises **before** `n_native` and producer metadata are collected at lines 160–165. Persist-before-gate therefore excludes the new scalar. CPU reproduction: four returned native norms, 72 persisted operand tensors, **zero persisted native norms; producer metadata absent**.
  
  **Exact fix:** collect the returned norm mapping and producer metadata before coverage validation; preserve them in the failed-write diagnostic/sidecar before raising. Preserve duplicate capture identities without attributing an overwritten return-map value to earlier occurrences. Extend coverage-failure tests to assert scalar and metadata persistence. Keep the HALT unchanged.

**ADVISORY**

- Remaining checks pass on static/CPU evidence: same-write return values without recomputation; binary64 comparison and unchanged `1e-3` threshold; per-arm mint and reported-only A1/A7 semantics; missing/nonfinite rejection; unchanged gate-2a `upd_norm` reference.
- Exact prereg SHA `85b389ec…e4bf8` verified; verification unchanged. No scoped harness/engine/core edits.
- Fresh verification: **75 MathLab tests PASS; 53 dashboard tests PASS; strict marimo checks PASS**. Existing tests miss the blocker above.
- Live inertness and corrected harvest acceptance remain **UNVERIFIED**. No repository edits or live dispatch performed.

🌱 graft saved ~47,757 tokens this turn, 1 successful call.

