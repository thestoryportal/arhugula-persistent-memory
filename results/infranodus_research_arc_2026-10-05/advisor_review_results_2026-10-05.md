**Tooling note:** graft was denied in don't-ask mode, and this session has no Read or Bash tool, so I couldn't open `CORPUS/39`, `CORPUS/43`, the fulltext extracts or `memit_main.py`. Every claim below that depends on those files is marked **UNVERIFIABLE (by me)** and names the file to check. Separately, the Gmail and Google Calendar connectors need authorization in claude.ai connector settings; neither was needed here.

---

## Verdict: **FIX-FIRST**

The document is sound as a record of the reading. What isn't yet supported is its ranking: I-8 is placed "first in queue" on an assumed match to the program's measured failure, and on numbers that may belong to RoSE as a whole rather than to swapping C for I.

### The single most important thing

**Test I-8 offline before any write.** Take the cached A7 keys behind the "17–180× under the ridge" result (`CORPUS/43`). Rerun that separability calculation with three regularisers:
- λC, as now;
- I, as RoSE does;
- a trace-matched λ′I, with λ′ = λ·tr(C)/d.

This needs no write and takes minutes. A ridge doesn't make near-collinear keys separable. It only changes how much weight norm the solve spends fitting small differences between keys. So:
- **Discriminating directions still under the new ridge:** I-8 is predicted null. Drop it to the bottom of the queue.
- **Directions now above the ridge:** I-8 is live. Pre-register a locality loss as well, because C is the term that protects the pre-training key distribution.

Either result is worth more than the first A7 arm.

---

## Issues, in priority order

**1. I-8 may be an analogy to the program's failure, not the same failure.**
- RoSE's trap is about *same-subject* edits: one subject's key carrying several different facts (S2RKE).
- Collinearity in the program, as this document describes `CORPUS/43`, comes from *last-token keys at the frame*. Different coined subjects collapse together because the key is read at the shared frame, not at the subject.
- Those are different causes. The row's sentence "one coined subject, several paraphrased frames … the program's regime" needs checking against the actual design of `CORPUS/43`: are the 24 keys distinct subjects or one? **UNVERIFIABLE (by me).**
- If the 24 keys are distinct subjects, RoSE's same-subject result doesn't carry over directly.

**2. The RoSE gain may belong to the whole method, not to C := I.**
- The quoted figures (Efficacy 86.7 vs 75.5, Paraphrase 63.8 vs 52.8) compare **RoSE**, which is IGA plus hierarchical knowledge integration, against **MEMIT-Merge**. They don't compare C := I against MEMIT.
- Unless §5.x has an ablation row with IGA alone, the I-8 row gives the gain to the wrong component.
- The paper also used instruction-tuned models and instruction-following QA, which differs from the program's scorer.
- Check the ablation table in `fulltext/` and quote the IGA-only number, or reword the row. **UNVERIFIABLE (by me).**

**3. "C := λI at the sweep's λ" doesn't say what it means.**
- λ = 2500 multiplies C, and C's scale is the mean squared key norm. So 2500·I is a completely different regularisation strength.
- Pre-register either a trace-matched λ′ or a λ′ sweep.
- Also check `CORPUS/39` for low `mom2_update_weight` arms. As λ→0, both solves approach the same minimum-norm KKᵀ solution, so part of I-8's regime may already have been tested. "Never removed C" may be true while "never tested the limit" is not. **UNVERIFIABLE (by me).**

**4. "No code change" understates the risk under LAW#5 and LAW#3.**
- **LAW#5:** swapping the statistic changes the regulariser of the science-bearing solve. That is a science-path change carried in data. Treat it under LAW#5's isolation discipline, not as a configuration tweak.
- **Fingerprint gate:** `tools/engine_fingerprint.py` hashes `memit_main.py`, not the stats file. A substituted C would pass the gate silently. Add the stats-file SHA to the run manifest.
- **Load path:** confirm the engine reads C from a cache that can be substituted, and that the `_cov_cpu`/P-VRAM-CPU-SOLVE path doesn't recompute or recast it. Check the `cat -n` source. **UNVERIFIABLE (by me).**
- **LAW#3:** "run A1/A2 under the same substitution first" mixes two separate steps. LAW#3 means reproducing the known baselines under the **standard** C, to prove the harness. A1/A2 under C := I is a new control arm and won't reproduce those baselines, by design. Do both, in that order.

**5. I-9 isn't shown to be BLUE.**
- Setting layers to {first, last} in the unmodified engine still computes z at the last layer and spreads the residual backward. That is my reading of MEMIT's update loop; check it at the source.
- If BLUE builds targets at each boundary layer, the configuration-only arm is "MEMIT with a sparse band", not BLUE.
- That sparse-band arm may also overlap the band-width sweeps already in `CORPUS/39`, if any 2-layer band was run.
- Either establish that the two are equivalent or rename the arm. **UNVERIFIABLE (by me).**

**6. The document contradicts itself on I-1.**
- §1 says I-1 is cheap "as a harness-side target".
- The I-1 row says it is science-path (`compute_z`) and needs LAW#5.
- A target precomputed outside the engine and injected still replaces `compute_z`, so LAW#5 applies. Fix §1's count of cheap ingredients.

**7. The exit condition was met by construction.**
- (b) needs two consecutive passes that add no new mechanism class.
- The last *search* pass, q8, produced both I-8 and I-9.
- The Part 3 passes only merged or analysed papers already retrieved, so they couldn't add a class.
- The search shows no sign of saturation: the best result came last, from a query in the field's own vocabulary.
- Either run 2–3 more field-vocabulary queries next to q8, or reword §6 to say the arc closed by the operator's choice, not by saturation. Example queries: "covariance regularization editing generalization", "layer selection residual locate-then-edit", "null-space editing generalization tradeoff", "out-of-vocabulary entity editing".

**8. The status line claims a review §7 doesn't contain.**
- The header says the verdicts "carry the advisor review recorded in §7", but §7 is empty.
- Fill §7 with this review and your responses before committing, or change the header.

**9. The I-8 falsifier tests the mechanism, not the contract.**
- "Held-out recall rises from the 19–31 % band" only checks that the mechanism moved something.
- The contract is the strict held-out-paraphrase bar from D-C10k-rulings-1. Pre-register a numeric pass threshold against that bar, and a separate numeric locality criterion (the S-3 rule).
- Cite where the 19–31 % figure comes from; no `CORPUS/NN` is given.

**10. I-4b's retrospective test can't show much as planned.**
- Coined values have near-maximal perplexingness by construction, so within A7 the predictor has almost no spread to work with.
- Pooling A7 with A1/A2 confounds value type with outcome.
- Stratify the test, or state up front that a null result within A7 is expected.

**11. Phrase the "cell is empty" claim more narrowly.**
- Zero hits for "unseen" or "held-out" is weak evidence; the field says "generalization", "paraphrase" and "portability".
- State the claim as "not found in 23 papers read at the evaluation section plus the logged query hits (`part2/_arxiv_pass_log.json`)". Don't state it as a property of the literature.

**12. Make the tokenization premise check blocking.**
- The arXiv 2609.29045 check (*The Tokens Remember*) changes what the held-out scorer counts as recall.
- Settle it before the first arm, not alongside it.

**Drift:** none. The arc serves the live C10 route required by D-C10k-rulings-1, and its fences hold: leads only, no CORPUS entry, nothing promoted.
advisor exit 0
