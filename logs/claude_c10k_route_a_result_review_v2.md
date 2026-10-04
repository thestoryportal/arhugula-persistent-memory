# Advisor review: C10K Route A result (`D-C10k-route-a`)

**Verdict: FIX-FIRST.** The halt itself is correct and I'd keep it: the prereg control gate failed at upstream's settings and failed again after the one allowed fix, as Amendment 3 predicted. What needs fixing is a set of numbers that don't agree with each other, one causal claim that the controls don't isolate, and an F6 mechanism that the document's own arithmetic argues against.

**Limits of this review.** Both graft calls were denied in don't-ask mode, and this session has no file tools. So I could not open any JSON artifact or `compute_z.py`. Every artifact citation below is **UNVERIFIABLE by me**. This is a review of the document's internal consistency and inference only. The skill loading the hook asked for also wasn't possible, because there is no Skill tool here.

## The single most important next step

**Run a single-variable keying ablation in the vendored MEMIT engine.** Use the R0 setup with the same 24 subjects and paraphrases, in a 2×2:
- `fact_token: subject_last` vs `last`
- context templates on vs off

**Why this comes first.** F3 is the finding the forward options and the new memory rule both rest on. The document currently says the keying locus "is the variable that differs" (§3.3). It is one of at least six differences between R0 and Route A:
1. keying locus
2. context templates
3. MEMIT's z-objective (template averaging, KL term, clamp)
4. null-space projector vs covariance ridge
5. L2 ridge vs `mom2_update_weight`
6. fp16 vs fp32

The F6 paragraph already admits this kind of confounding ("not separated by this run"); F3 does not. The ablation uses existing machinery and leaves the science path untouched, since `last` is a native engine option.

**What the outcome would mean.** If `last` + no templates collapses A1 `para_full` to near 0, F3's causal attribution becomes EVIDENCE-SHOWS. If it stays high, F3 is overturned and option (ii) loses its rationale.

## Issues, in priority order

1. **The numbers that are supposed to be the same quantity disagree. Reconcile them before committing.**
   - **Fraction of residual written at L2 = 10:** F2 says "5–13 %". The §3.3 table says 0.17 / 0.14 / 0.12 / 0.17 / 0.28, which is 12–28 %. §3.1 says update norms 4.2…51 against residuals ≈ 100, which is 4–51 %. That is three different values.
   - **Final z error at L2 = 10:** §3.1 says "98 → 87". §3.3 says 65.935. If the back-test and R1 differ in some setting, say so; otherwise one of them is wrong.
   - **F1 removal range:** a survival of 0.473 at L5 means 52.7 % removed, not 56 %. The range is 53–76 %.

2. **F4 ("write magnitude costs locality") is confounded with where the edit is keyed.**
   - The fp64 control separates magnitude from precision. It does not separate magnitude from keying. The edit key is the template's final token ("of") after the prompt. That is a very common context in generic text, and F1 already shows the projector does not protect at L8 for these last-token keys (interference ratio 1.03).
   - Damage to generic NLL from writing at a high-traffic key is the obvious alternative explanation.
   - **Check:** report R0's locality numbers. R0 makes a subject-keyed write that fits fully, so if its generic NLL and JS are clean, F4 must be scoped to "for prompt-last-token keys".
   - Also, "monotone cost, not a threshold artefact" rests on two points (0.01 and 0.03). Generic NLL at L2 = 10 is "n/r". Two points can't distinguish monotone from threshold, so say "decreases from 0.01 to 0.03".
   - "The attention-sink key dominates L4's preservation term" is I-INFER inside an EVIDENCE-SHOWS finding. Label it.

3. **F6's mechanism is probably mis-described, and the document's own numbers contradict it.**
   - The claim is that `15000·C` "vanishes" in the directions where C's eigenvalues are below 0.005. But 15000 × 0.005 = 75, which is larger than the key energies cited elsewhere (7–33, though those are projected keys). Those directions are still dominated by the ridge.
   - A more consistent reading: the ridge dominates the high-variance directions that real keys occupy, so the update under-fits. That is the F2 failure in the covariance metric, not "the opposite direction". The huge update norms come from the small part of each key that lies in the eigenvalue tail, amplified by about 1/(15000λ). That part is a symptom, not the cause of the non-fit.
   - "Unsolvable" is the wrong word. An exact solve that under-fits is over-regularised, not degenerate.
   - "Reproduces the degeneracy exactly" over-claims. The fp64 band norms are 16049 / 227 / 397 / 498 / 14 against fp32's 6844 / 656 / 591 / 3565 / 13, so they differ by up to 7× per layer. The behaviour matches; the norms only match qualitatively.
   - **Check (pure linear algebra on the saved C and K):** decompose the key energy along C's eigenvectors and compare λ·15000 against ‖k‖² per band. That would show whether the fit is limited by ridge dominance or by something else, such as keys and targets being taken at mismatched positions. If neither explains it, consider a harness bug before calling it a model property.

4. **Gate "PASS" sits next to "non-protective at L8".** State explicitly whether the interference control was a pre-registered bound. If it was, the projector gate did not pass. If it wasn't, say "diagnostic, not gated".

5. **Option (i) is untested as a predictor.** LRE faithfulness measures whether a relation can be linearly decoded for facts the base model already knows. Whether it predicts the edit-time split across value classes (A1/A2 vs A7) is I-INFER. Its prereg must first reproduce the known R0 split (94 / 98 / 14) after the fact, before it is used to gate option (ii).

6. **Drift check.** This run does not advance C10. A7 stays at 13.9, which §5 states plainly; good. The durable contribution is a design constraint (where edits are keyed), which is exactly why the ablation in the next-step section matters before that constraint is written to memory as a rule.

7. **Housekeeping.**
   - The pasted item contains the whole document twice. Check that `CORPUS/42` and the docs file aren't duplicated on disk; the network FS has a history of write anomalies.
   - §3.5 comes before §3.4, and F5 is listed after F6.
   - The process-learning rule is sound. Keep it, but its premise is F3's causal claim, so make it conditional on the ablation.
   - Per CLAUDE.md, the gpt-5.5 cross-family review is still owed at the promote gate.

**What holds up:** the halt verdict, the scoping in §1 and §6, the pre-registered readings in §3.5 and their (a)–(c) calls, F3's observation-level claim (0/72 at three ridges, independent of precision), and §5's refusal to claim anything about AnyEdit's own benchmarks.

**Unrelated:** the claude.ai Gmail and Google Calendar connectors need authorising in your claude.ai connector settings before they can be used.
