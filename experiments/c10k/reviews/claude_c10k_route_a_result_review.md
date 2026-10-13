# Adversarial review: C10K Route A, HALTED (CONTROLS_NOT_RECOVERED)

**Verdict: FIX-FIRST.** The halt itself holds up: the controls missed `para_full ≥ 80` at both ridge values, and the prereg's one-fix rule was followed. But two of the findings the document calls "promotable" (F4 and F6) blame the model for something that may be fp32-on-MPS solve precision. One provenance problem also blocks close-out.

**I could not read any artifact.** This session has no shell or file-read tool, and graft was denied. Every number below comes from the document itself. Any claim about file contents that the document does not show is marked **UNVERIFIABLE**. The one outside fact I do have is the session-start git status.

## Single most important next step

**Re-run the R3 (`memit_ARE`) and R1-A1 (L2 = 0.01) solves in fp64 on CPU from the saved z, keys and covariance, before promoting F4 or F6.** No forward pass is needed. It is a linear solve.

Why this test overturns F6 cheaply:
- With a near-singular `λC + KKᵀ`, an *exact* solve should still write the edit keys almost perfectly. In the directions where λC is negligible, `ΔW·k ≈ R·Kᵀ(KKᵀ)⁺k ≈ R`.
- The document instead reports update norms of 5.7e5 while z error barely moves (98 → 91), and canon stays at 2/24.
- Huge norm with no fit points to the solve failing numerically (condition number around 1e9–1e12 in fp32), not to the update landing "where no real input looks".
- The program already knows this failure: CLAUDE.md's `_cov_cpu == 3` P-VRAM-CPU-SOLVE check is "required for Qwen / wide-intermediate arms". The port solves fp32 on MPS. Whether the port had any equivalent is **UNVERIFIABLE** here, and the document doesn't say.

If the fp64 re-solve brings z error down and canon up, F6 changes from "covariance ridge doesn't transfer across models" to "the fp32 solve fails at this conditioning". That is a different finding, and one the program already knew.

## Issues in priority order

1. **The cited artifacts are dirty after the result commit.** At session start, `results/c10k_route_a/R1_w1_A1_single.json`, `R1_w1_A2_coherent2.json` and `anchor.json` all showed uncommitted modifications on top of `a0bb025`, the result commit. The document cites all three: §3.2's A1/A2 rows and the D5 L2 = 0.01 norm ratios. Run `git diff a0bb025 -- results/c10k_route_a/` before close-out. Then either commit with a reason or restore, and re-check every number taken from those files. As things stand, the evidence trail and the document can disagree, and nothing detects it.

2. **F6 is over-claimed** (see above). There is a second confound: the covariance was accumulated from fp16 activations (D4-b), and the sample count isn't stated. An eigenvalue floor of 1e-7–1e-9, with 1,583–8,645 directions below 0.005, could be partly an accumulation or sample-size artifact rather than a property of Qwen. The "fp32 gate reproduced to 0.001" check doesn't cover the small-eigenvalue tail. Until the fp64 control runs, F6 should be labelled I-INFER for its mechanism and EVIDENCE-SHOWS only for "this configuration produced degenerate updates".

3. **F4 is confounded with solve precision.** At L2 = 0.01 the fp32/fp64 relative difference is up to 5.7e-02 (§3.3). That error lands in exactly the arms whose locality damage F4 attributes to restored write magnitude. The attention-sink explanation for L4's 3.6× growth is an inference, not something measured, so label it I-INFER. Two further limits:
   - F4 rests on one ridge point. L2 = 0.03 was only back-tested and never run behaviourally.
   - The same fp64 re-solve control can separate "magnitude costs locality" from "solve error costs locality". Run A1 at L2 = 0.01 and 0.03 in fp64 and compare generic-NLL Δ against +0.25861.

4. **F3 is correct but its mechanism sentence overstates.** "The paraphrases end on other tokens and never read it" is mechanistic wording. What was measured is 0.8–1.8 % hidden-state transfer and 0/72 behaviourally. Paraphrases may end on the same surface token ("is") with a different context, so the key is a different vector, not a different token. Two other gaps:
   - **State the positive control explicitly.** If R0's A1 94.4 / A2 98.6 are `para_full` under subject-last-token keying on the *same stimuli*, that is the strongest evidence for F3. It shows the stimuli allow paraphrase transfer and that keying position is the variable. The document lists R0 only as a LAW#3 reproduction and never says what it measured, which is **UNVERIFIABLE** here. Add one sentence.
   - **Confirm the keying citation.** The claim that the keying comes from upstream at `compute_z.py:91` (last prompt token, not `subject_last`) has to be read from source and quoted. LAW#4 requires that, and I couldn't check it.

5. **Lesson for the prereg.** If F3's mechanism can be read off `compute_z.py:91`, then the control gate (`para_full ≥ 80` for an edit keyed at the last prompt token) could have been predicted unreachable at prereg time. Amendment 3 did predict it, but only after R1 at L2 = 10. Record this as a process learning: for single- and two-token answers, AnyEdit's ARE collapses to a single window keyed at the last token, which falls outside AnyEdit's long-form regime. The halt is still valid. This is about catching it before compute is spent next time.

6. **F1's L8 call.** An interference ratio of 1.0305 at N = 24 with one seed is "≈ neutral", and the document gives no CI. "Non-protective" is acceptable wording. Anything stronger is not.

7. **Drift check, and how the forward options are ordered.** The result advances F1 by closing Route A. But C10's blocking question is the coined multi-word values (A7, where R0 gets 13.9), and this halt leaves A7 *exactly* where R0 left it. Option (i), the LRE-faithfulness test, is a predictor. Option (ii), subject keying plus per-window targets, is the direct test of C10. The document should say plainly that (i) only gates whether (ii) is worth building, and that neither has evidence yet. "Re-running the port is not a live option" is fine as I-INFER from F3. It is not EVIDENCE-SHOWS "at any ridge", since only three ridge values were back-tested.

8. **Minor.** The item as I received it contains the whole document twice, which looks like a paste duplication. Check that `CORPUS/42` and the result doc aren't actually duplicated on disk.

## What holds

- The prereg discipline: amendments were reviewed and committed before each run they governed, and only one fix was spent.
- The scope boundary in §1/§6, and the explicit statement that AnyEdit's own benchmarks aren't addressed.
- F2: an ridge of L2 = 10 realises 5–13 % of the residual. It is consistent with the back-test, and its precision error (7.1e-05) is negligible.
- The behavioural 0/72 paraphrase result across every arm.

Separately: the claude.ai Gmail and Google Calendar connectors need authorizing in your claude.ai connector settings before they can be used. They weren't needed for this review.
