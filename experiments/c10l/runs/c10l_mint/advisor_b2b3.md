# Advisor pass on amendments B2/B3 and the P4 pipeline (Codex gpt-5.5, 2026-10-05, before any run)

Disposition: B2 FIX-FIRST folded (ids not strings; HF parity reference dumped at save; paired retention; failure signatures); B3 PROCEED with the two precisions folded. Runs paused for HIL.

## Review text (verbatim)

**Verdict**

B2: **FIX-FIRST**. The deployment design is F1-relevant and the `/tokenize` check is the right overturning test for added-token preservation, but the current P4 probe does not actually measure the binding id-level parity / Q4 retention it pre-registers.

B3: **PROCEED**, narrowly. The thresholds are conservative enough for a replication readout, and a fresh-process G re-run is adequate for the stated “per-process spread” question. Do not over-read it as a full G-family replicate; no second `k` unless you explicitly reopen B1.

**Single Most Important Next Thing**

Fix `c10l_mint_p4_probe.py` so P4 records top-1 token ids, per-prompt fp16-vs-Q4 paired retention, and an explicit failure signature: tokenizer failure vs generation-id failure vs decoded-string-only mismatch.

**Issues**

1. **B2 probe scores decoded strings, not binding token ids.**  
   B2 requires `/tokenize(" "+coined) == [151665+k]` and top-1 parity/retention for the minted token ids, while the probe uses `/completion` `content` and string equality for CANON/PTEST. A decoded-string mismatch can be a probe artefact; an id mismatch is the deployment finding. See [docs/C10L_MINT_TOKEN_PREREG.md](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/C10L_MINT_TOKEN_PREREG.md:112), [c10l_mint_p4_probe.py](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10l_mint_p4_probe.py:26), [c10l_mint_p4_probe.py](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10l_mint_p4_probe.py:55).

2. **B2 does not compute CORPUS/17’s retention metric.**  
   CORPUS/17/B3 defines retention as “of prompts correct in GGUF-fp16, fraction still correct in Q4_K_M.” P4 currently emits independent `canon_hits`/`para_hits`, but no paired eligible set and no `surv/elig` retention. See [b3_verdict.py](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_b/b3_verdict.py:35), [b3_verdict.py](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_b/b3_verdict.py:54), [c10l_mint_p4_probe.py](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10l_mint_p4_probe.py:62).

3. **B2 “HF-fp16 parity” is not actually checked.**  
   The probe loads the arm JSON only for stimulus, then checks whether GGUF output matches the coined string. That is correctness, not top-1 agreement with HF-fp16 per prompt. If the conversion changes a wrong prompt into another wrong prompt, or happens to preserve correctness while changing top-1 id/string behavior, the current probe misses the stated criterion. See [docs/C10L_MINT_TOKEN_PREREG.md](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/C10L_MINT_TOKEN_PREREG.md:112), [c10l_mint_p4_probe.py](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10l_mint_p4_probe.py:41).

4. **B3 is procedurally under-specified, but not conceptually broken.**  
   The code supports seed-1 N via `MINT_INITS`, `MINT_N_SEED`, `MINT_INIT_TAG`, and `MINT_STEP0`, and the arms driver reads tagged tensors correctly. But the amendment should spell out that G-rep uses the original step0/G tensor, while N(seed1) uses `step0_probe_seed1.json`; otherwise a manual run can accidentally point G at a seed1 step0 that contains only N. See [C10L_MINT_TOKEN_PREREG.md](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/C10L_MINT_TOKEN_PREREG.md:118), [c10l_mint_step0.py](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10l_mint_step0.py:22), [c10l_mint_arms.py](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10l_mint_arms.py:27).

5. **B3 thresholds are acceptable only for scoped support.**  
   `≥5/72` for G-vs-N is just above the stated per-process spread, so it is a reasonable “support only if robust” rule, not evidence of a population effect. The minted-vs-rare rule should be mechanical: `min(mint replicates) - max(rare replicates) ≥ 10/72`. Current wording says “every mint replicate exceeds the rare replicates,” which is directionally clear but should be made exact. See [CORPUS/45_C10L_MINT_TOKEN.md](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/CORPUS/45_C10L_MINT_TOKEN.md:30), [CORPUS/45_C10L_MINT_TOKEN.md](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/CORPUS/45_C10L_MINT_TOKEN.md:39).

Overturning test: for B2, a single GGUF where `/tokenize` passes but top-1 id retention drops below the fp16 eligible set falsifies deployment viability for option (iv) as compiled. For B3, a sign flip or <5/72 G-vs-N gap, or `min(mint)-max(rare) < 10/72`, kills the directional readings while preserving CORPUS/45’s PARTIAL result.

graft saved ~16,846 tokens this turn.