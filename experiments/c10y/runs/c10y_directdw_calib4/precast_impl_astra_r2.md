FIX-FIRST
Reviewer: GPT-6-Astra (high)

**BLOCKING**

1. **r1 B1 — RESOLVED.** Pre-solve persistence and exceptional-return handling: [c10y_precast_diag.py:226](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag.py:226), `:271`, `:303`, `:315`, `:328`. Direct/factor failure controls pass: exact M/RHS retained before execution, original exception object preserved, phase INCOMPLETE, weights/globals/trace restored. File/directory fsync control passes.

2. **r1 B2 — RESOLVED.** Input identity checks: [c10y_precast_diag.py:235](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag.py:235), `:256`, `:352`, `:370`. Observer-induced factor-M, factor-Q and direct-M mutations halt; invalid observation finalizes INCONCLUSIVE. Separate genuine native-discrepancy control produces validated **S** across ten cells.

3. **r1 B3 — NOT RESOLVED for inherited ignored signals.** [run_c10y_precast_diag.sh:123](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/run_c10y_precast_diag.sh:123)–`:125` assumes Bash can install every handler. Here SIGHUP is inherited as `SIG_IGN`; `trap -p HUP` is empty, and HUP is ignored. The HUP test failed repeatedly; worker termination and INCONCLUSIVE came from the later deadline, not interruption handling. Resetting HUP **before starting Bash** makes the same control pass.

   **Exact fix:** establish default TERM/INT/HUP dispositions before supervisor Bash starts, or fail closed before launching children when required traps cannot install. Add an inherited-`SIG_IGN` regression; resetting only the test environment is insufficient. TERM/INT, process-group cleanup after leader exit, fresh publication, and deadline-cancelled-last controls otherwise pass.

**ADVISORY**

- Fresh results: diagnostic **64/65**, existing C10Y **285/285**; isolated HUP with explicit pre-exec reset **1/1**. Implementation hashes match the fix report. No model/GPU/MPS or production launch.
- **Single-entry whole-file repin is acceptable; a templates-only pin is not required.** At [c10y_precast_diag.py:24](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10y_precast_diag.py:24), acceptance requires:
  - A1 review and commit completed; record commit ID and SHA-256 of that committed file; working bytes must match.
  - Record old/new `TEMPLATES` definition byte equality, AST equality, and literal-value equality.
  - Preserve flat digest `d6c7c700…`, engine digest `c7dabbe7…`, calibration-context equality and file pin `9472b663…`.
  - Change only that source-pin entry; all other pins and source-drift checks remain intact.

  Current working bytes satisfy the template proofs; only this source pin mismatches. Commitment and repinning remain pending. Runtime inertness and 2,820-second feasibility remain UNVERIFIED.

🌱 graft reported ~224,939 tokens saved this turn, one successful call.

