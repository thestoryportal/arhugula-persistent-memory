**FREEZE**

Verified v4 SHA-256 matches `257e064c703b54a6d2af0c8a854bcbef227770c2f3fb36174b687010a44197c8`, including at completion.

**BLOCKING: none. B2 is RESOLVED.**

Check 3(c) now uses `audit_prompts(H, M, W)` and the original `p2_audit`, matching the historical caller. The source-identity gate covers all five relevant files; their current hashes match `/identity/source_sha256` in **all three** mint records. Evidence: [prereg:96–101](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/MATHLAB_PREREG.md:96), [inventory builder:273–282](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_arms.py:273), [writer caller:791–794](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_arms.py:791).

**Empirical tokenizer replay passed:** using the pinned local `AutoTokenizer`, source-extracted original registration/inventory/audit functions, and frozen record inputs, every field returned by `p2_audit` matched all three saved audits:

- **396 plain / 2,376 contextual strings**, unchanged.
- Exact minted IDs, all checks and `changed == []`.
- All **24 target rows × six templates**, including target IDs, expected IDs and contextual booleans.

**ADVISORY**

- **Whole-object comparison nuance:** saved `/admission/P2` additionally contains `wordlist_replay`, appended by the step-0 writer at [arms.py:711–712](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_arms.py:711) and persisted at [arms.py:857](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_arms.py:857). I separately reproduced that field exactly for all three records. Thus the complete saved object is reproducible, but raw `p2_audit(...) == saved_P2` would fail on the extra key. V4’s explicitly enumerated comparison avoids this; **non-blocking**.
- **Round-3 folds confirmed:** ≤2/30 caveat and admission independent of proxy scores at [prereg:251](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/MATHLAB_PREREG.md:251); expanded registration citation at [:95](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/MATHLAB_PREREG.md:95); v4 editorial correction at [:314](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/MATHLAB_PREREG.md:314).
- **No previously resolved item regressed:** B1 observer identity/coverage, B3 safe conversion, B4 fixed proxy/bootstrap rules and B5 fail-closed admission remain intact. Fresh/historical separation, norm-only caveat, A2 floor, baseline-before-mint ordering and MATH-PROXY restrictions also survive.
- Freeze approves the **design**. Tensor/behavioral inertness, replay norms, resource bounds and calibration remain **UNVERIFIED until execution**.

Read-only review; CPU tokenizer execution only. No torch import, model load or GPU execution.

🌱 graft reported ~210,853 tokens saved, 1 successful call.

