# Advisor pass on amendments A2/A3/A4 (Codex gpt-5.5, 2026-10-05, before arm C was read)

Disposition: FIX-FIRST item 1 folded (reader envelope); A3 note kept; run 3 arm A declared the overturning control.

## Review text (verbatim)

**A4 verdict: `FIX-FIRST`.**  
The statistical derivation is acceptable for a reproduction envelope: min..max ±3 over the five same-baseline observations is a transparent descriptive guard, not an inferential confidence interval. But the committed reader still hard-codes the old envelope, so the amendment is not mechanically true yet.

**Single most important thing:** update `ENVELOPE` in [c10l_covgeom_read.py](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10l_covgeom_read.py:9) to A4’s `[5,18]` and `[42,59]` before reading run 2’s arm C result.

**Issues**

1. **Blocking: A4 says the reader takes the amended envelope, but it does not.**  
A4 declares `para_full [5,18]` and `para_first [42,59]` at [docs/C10L_COVGEOM_SPARSEBAND_PREREG.md](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/C10L_COVGEOM_SPARSEBAND_PREREG.md:119), while the reader still has `A7_para_full: (11,18)` and `A7_para_first: (48,62)` at [c10l_covgeom_read.py](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10l_covgeom_read.py:9). This would make run 2 arm A invalid despite A4.

2. **A4’s five observations are grounded enough; min..max ±3 is the right kind of statistic for this purpose.**  
This is a validity/reproduction envelope, not an empirical claim about the population. The historical baselines include 10/72, 8/72, and 15/72 in CORPUS lines [37:23](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/CORPUS/37_C10_BANDKNOB.md:23), [38:23](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/CORPUS/38_C10_BAND412.md:23), and [39:25](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/CORPUS/39_C10_STRENGTH_LAYER_SWEEP.md:25). Run 1 supplies 13/72 and 54/72 at [run1_armB_identity.json](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/c10l_covgeom/run1_armB_identity.json:327); run 2 supplies 10/72 and 45/72 in [logs_run2_armC.log](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/c10l_covgeom/logs_run2_armC.log:34).

3. **A3 does not need a margin, but it does need the “not a margin” note kept prominent.**  
The discriminator records max six-run spread `0.043532256174184214` at [a2_discriminator_preknob.json](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/c10l_covgeom/a2_discriminator_preknob.json:102), and A3 correctly says this is an observed bound, not a margin, at [docs/C10L_COVGEOM_SPARSEBAND_PREREG.md](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/C10L_COVGEOM_SPARSEBAND_PREREG.md:113). Run 1’s A2 miss is close to the bound, so do not describe it as comfortably passing.

4. **Post-hoc risk: acceptable, but label it carefully.**  
A4 is post-freeze and triggered by seeing run 2 arm A, but it changes only the P2 reproduction envelope, not §5’s candidate-read thresholds; §5’s PASS/LEAD/NULL criteria remain fixed at [docs/C10L_COVGEOM_SPARSEBAND_PREREG.md](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/C10L_COVGEOM_SPARSEBAND_PREREG.md:63). That is not post-hoc relative to the candidate arm, provided the reader is fixed before arm C is read.

**Cheapest overturning control:** run one more baseline-only fresh process, then apply the amended reader before any candidate read. If it falls outside `[5,18]` or `[42,59]`, A4’s “known spread” story is itself unstable.