**FIX-FIRST.** The most important next change is a **pre-start budget refusal plus an independent watchdog for every stage**. The post-baseline smoke is too late to serve that purpose.

References below: **P** = [docs/C10Y_DIRECTDW_PREREG.md](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/C10Y_DIRECTDW_PREREG.md), reviewed SHA-256 `a6028bdf86c59cbc3ed44caf2e267accedad55806c855292ec6243a42baa2151`; **H** = [experiments/track_c/c10e_bandknob.py](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10e_bandknob.py).

**BLOCKING**

1. **Budget control starts too late; stages 2–3 lack hard deadlines.** P:90–91,157–158 permit spending on baseline/proofs before discovering infeasibility; P:366 explicitly accepts that outcome. Replace the budget rule and §8 item 4, and make §2.6/§6 reference this text:

   > **Pre-start budget gate, every stage.** Before launching the model-bearing process, record a phase-by-phase duration forecast using the best available measured timings on this Mac. Cite each timing artifact, workload, repetition count and scaling assumption. Include loading, context/target preparation, all baseline and inertness runs, repeated projectors/capture solves, parity checks, smoke, the full remaining 100-update budget, permitted overflow retries, merge, readouts and shutdown. Do not assume early convergence. Use conservative upper estimates; an unmeasured component without a defensible bound makes the forecast UNVERIFIED and dispatch is refused.
   >
   > Stage 1 has cap C₁ = 7,200 seconds. Stages 2 and 3 each require a finite numeric cap recorded in their spending decision before launch; an absent cap refuses dispatch. If the projected total exceeds the stage cap, record HALTED-BUDGET with `launched=false`; equality passes. The existing 110–165-minute inference is not a measured feasibility certificate.
   >
   > An independent supervisor starts the deadline before worker launch and enforces it throughout loading, baseline, proofs, optimisation and evaluation, including blocked calls. It owns only this stage’s worker/process group. Its bounded termination allowance is inside the cap, with forced termination at the deadline if necessary. A model-free hanging-worker test must verify enforcement before dispatch.
   >
   > Retain in-run projections before every expensive phase and at optimiser-step boundaries. Use synchronised measurements and reserve at least 23 minutes for stage-1 final readout, increased when measured evidence requires it. Exceeding the projected budget stops work without changing T_max, batching or optimiser settings. A deadline stop before write completion is HALTED-BUDGET; after write completion but before required readout completion it is INCOMPLETE-BUDGET. Neither earns a scientific label. Obtaining missing calibration timings is separately budgeted work and cannot bypass LAW#3.

2. **V13 rejects legitimate null diagnostics; the screen has no general incomplete-record row.** A1’s single-token values yield `tf_total=0`, so H:134–136,382–392 legitimately returns `tf_pertok_cont=null`. `cond_full_given_first` is also nullable. P:125 requires both fields, while P:181 requires every metric finite. P:191–197 can misclassify incomplete records.

   Replace V13 and add the following before the screen table:

   > **V13 — typed metric validity.** Required fields must be present. Applicable numeric values must be finite. `tf_pertok_cont=null` is valid exactly when the recorded continuation-token denominator is zero; `cond_full_given_first=null` is valid exactly when `para_first_n=0`. Preserve their denominators and an explicit undefined reason. These diagnostic nulls neither invalidate an arm nor count as passed scientific gates. An unjustified null, NaN or infinity fails V13. Explicit zero-update/not-applicable cases follow their named rules.
   >
   > Read recorded halt/invalid/budget outcomes first; missing records caused by a halt do not manufacture another validity failure. If required stage records are otherwise missing, return INCOMPLETE before testing fit or counts. Stage-1 candidate A1/A2 and later-stage records are deliberately NOT-RUN and are not required screen records. Only complete, valid screen records reach S4–S7.

3. **Size controls are forbidden in the very replication that requires them.** P:80–81 and D-10 at P:299 say “stage 2 only”; P:223,239 requires attribution in both processes. Their conditional arm coverage also conflicts with V5 unless identity cases are specified.

   Replace those “stage 2 only” clauses and add to §2.6:

   > NM-total and ENV are conditional controls in **both stages 2 and 3**, never stage 1. Derive each arm’s scale from that process’s corresponding recipe-A and B-e2e actual updates. A triggered control recipe supplies A1/A2/A7 records; an arm requiring no downscale uses scale 1 and may reference its identical, fully evaluated B-e2e artifact with explicit provenance. It is not NOT-RUN.
   >
   > Stage 3 independently regenerates B-e2e, B-z and the required controls. For cross-process comparison, a control untriggered in one process uses that process’s scale-1 candidate counterpart. No stage-2 tensor substitutes for stage-3 regeneration. Both processes must independently satisfy attribution.
   >
   > Stored updates use the explicit arithmetic `W_post = fp16(W0 + fp16(s·D_B))`, with `s·D_B` computed in float32; geometry and matching use the resulting actual D.

4. **Anchor attribution still has an uncovered case, and the interpretation reintroduces causality.** With `a=12`, `n_eff=22`, `n_z=13`, T1 adds no qualifier because B-z lacks a “sized gain,” but H-Y1 cannot be credited because the difference is only 9 (P:238–239). P:270 additionally says TRADEOFF/LARGE-WRITE/SIZE-NOT-EXCLUDED means the objective “buys recall with write size,” contradicting P:237’s explicit non-causal interpretation.

   Replace T1:

   > For an otherwise eligible e2e positive: missing, invalid or unfit B-z gives ANCHOR-UNTESTED. Otherwise, `n_eff−n_z<10` gives ANCHOR-NOT-EXCLUDED, regardless of whether B-z itself has a sized gain. A difference ≥10 passes this comparison. Neither outcome establishes a unique causal mechanism. Add the boundary cases `(a,n_eff,n_z)=(12,22,13)` → ANCHOR-NOT-EXCLUDED and `(12,23,13)` → comparison passes.

   Replace the corresponding sentences in “What each buys”:

   > A replicated attributed positive shows that this fixed weight-space optimisation configuration outperformed recipe A under the named gates. It does not identify closed-form allocation as the unique cause.
   >
   > TRADEOFF, LARGE-WRITE or SIZE-NOT-EXCLUDED reports the observed gain and failed condition. It does not establish that increased size caused the gain; any norm-constrained follow-up requires separate preregistration and authorisation.

5. **The check applicability is contradictory and cannot be built literally.** P:111 puts *every* check after LAW#3, although standing check (i) necessarily precedes LAW#3 in P:89. V3 demands (ii)–(ix) for every mode/arm, but (vi) and (ix) explicitly specify A7, and `apply_stored` has neither Adam nor an AB optimisation graph (P:115–121,171).

   Replace P:111’s ordering sentence and V3:

   > Standing check (i) precedes LAW#3 for recipe A; all new-path checks follow LAW#3. Checks (ii), (iii), (iii-b), (iv), (v) and (viii) apply to each optimised mode/arm before its substantive result is trusted. Check (vi)’s NLL/KL construction audit is e2e/A7; its accumulation comparison applies separately to each optimised objective on the fixed A7 subset. Check (vii) applies to each optimised mode/arm. Check (ix) is the e2e/A7 smoke once per process.
   >
   > `apply_stored` instead requires scale-1 reference reproduction, restoration/hook checks, planned stored-update and actual-update geometry, and complete merged-model readouts. Optimiser, gradient and train–deploy-hook checks are explicitly NOT-APPLICABLE to this mode. Final-state checks run after optimisation/merge and before classification, not before the state exists. Reduced LAW#5 writes are not substantive fit-tested candidates.

6. **Two numerical gates remain implementer-dependent.** P:166 requires unrounded comparisons, but H:162–163,315,337,492 returns rounded `described_as` and perplexity. R1 lost the denominator explicitly supplied by the prior reviewer (`results/c10y_directdw_codex_design_v1.md:151`); P:226 only says “relative L2.”

   Add to the locality/readout contract:

   > The driver records unrounded `described_as` and generic perplexity using the harness’s same distributions, prompts and reductions, before final presentation rounding. G3/G5 use these raw fields exclusively. Preserve legacy rounded fields for display. A rounded value cannot substitute for a missing raw gate input.

   Replace R1’s distance phrase and clarify R3:

   > `distance = ||D_p1−D_p2||_F / max(||D_p1||_F, ||D_p2||_F) ≤ 0.10`, retaining the stated zero-norm cases. R3 counts unequal `para_full_hits` booleans for identical `(subject, PTEST_index)` pairs; it does not count differences between two incorrect generated strings.

7. **B-z’s zero-denominator rule is only specified before optimisation.** A zero initial residual can become nonzero after other facts’ updates; P:52 does not prescribe what subsequent objective evaluations do. Fit scope across A1/A2/A7 is also unstated at P:183–185.

   Add:

   > Evaluate the zero-denominator rule at every B-z objective and fit evaluation. For `||δ_i||=0`, a zero residual contributes zero; any nonzero residual immediately yields INVALID-ANCHOR-NORMALISATION. Do not evaluate a masked 0/0 expression.
   >
   > Record fit separately for every substantive arm. A recipe passes FIT-E2E or FIT-Z only when all its required arms pass; stage 1 requires A7 only. Recipe A and reduced inertness checks are exempt from candidate fit gates.

**ADVISORY**

- **Fold audit:** every v1 BLOCKING item has a substantive body change; none is merely logged. Advisor #3–6 and Codex #3–6/#18 remain partly resolved through the integration defects above. Codex #1–2/#9/#15–17/#19–21 are incorporated in substance. The omitted R1 denominator additionally makes the logged advisory #11a fold incomplete.
- **LAW#3 is correctly transcribed:** all three inclusive A7 intervals and A1/A2 ≥68 appear at P:172, matching `CORPUS/44_C10L_COVGEOM_SPARSEBAND.md:39`; candidate operations follow the gate at P:89. Preserve that order.
- **MEASUREMENT-ONLY is consistent in the operative classification:** P:97–107,233,274,286 grants no route status. The remaining overclaim is causal interpretation, addressed above.
- **Minor LAW#4 corrections:** P:31’s “25 Adam steps” should say “at most 25 loss evaluations and 24 Adam updates” (`compute_z.py:108,164–172`). P:32 should specify that `compute_ks` averages within context groups, then equally across groups—here identity weight ½ and each sampled context weight ¹⁄₁₀ (`compute_ks.py:39–49`). P:45/47 should consistently describe factorisation and zero-step identity as exact-arithmetic identities subject to the numerical reduction gates.
- The core integer label partition is complete; I checked all 2,044 combinations of baseline 5–18, candidate 0–72 and locality pass/fail. That does **not** resolve the missing-record and attribution gaps above. Runtime, memory feasibility and new-path inertness remain unverified. No files or models were changed.

Graft-reported savings: ~28,421 tokens ($0.02), one successful query.

