# D-C10z-astra v1 design review — gpt-6.1-sol, max effort

Actual reviewer metadata: `model=gpt-6.1-sol`, `effort=max`, from `/Users/robertrhu/.codex/sessions/2026/10/07/rollout-2026-10-07T07-08-24-01a1167a-b9ba-7312-af9a-082459d4e2ce.jsonl:8`. Record this identity accurately in the fold log; this review must not be entered as the draft's named GPT-6-Astra/high review (`docs/C10Z_ASTRA_PREREG.md:300,304`). Review date: 2026-10-07.

Verdict: FIX-FIRST

**Single most important fix:** add an independent check of the captured key positions/layers and a nonzero, known-answer check of the production solve/write path before candidate output is trusted. Z3 is useful identity plumbing, but Z4 can pass with a shared wrong key capture; the advisor's proposed active check also needs its finite RMSNorm prediction corrected (`docs/C10Z_ASTRA_PREREG.md:141–147`; `results/c10z_astra_advisor_v1.md:98–114`).

Review basis: prereg v1 SHA-256 `dc32630a3eda333f3c9f6aadf51499f11932a085d7f69681eb76aabd8688eedd`; advisor v1 SHA-256 `5e7917f9ab5e3ddb311208c817b2112bdee0c7dca9f737c75ecc067b58e4db9d`. The advisor appeared during this review and all fourteen numbered items below reconcile it. These hashes identify the bytes read, rather than a claim about later edits. Recommendations and arithmetic deductions are **I-INFER**; runtime behavior of the proposed driver is **UNVERIFIABLE** because the draft says no implementation/run exists (`docs/C10Z_ASTRA_PREREG.md:3`). This review used file reads, online paper reads and standard-library predicate/arithmetic checks only.

The F1 location is the Write Engine/Commit Executor compile cell, with the C10 multi-token L2 behavioral condition still OPEN/BLOCKING; a scoped candidate does not close governance, deployment or Incremental writes (`docs/SPEC_E2E_GROUND_TRUTH.md:22–34,64–65`; `docs/SPEC_EXPERIMENT_OVERLAY.md:22`; `docs/C10Z_ASTRA_PREREG.md:25,296`). The paper was readable: [ASTRA v1, methods §3.1–3.5 and experiments §4](https://arxiv.org/html/2610.05277v1). Its SemCon, covectors/directions, joint-system and column-update formulas support the draft's core construction. Its protocol repairs individual samples with four renderings; the declared batch, views, domain, statistics and precision adaptations remain adaptations (`docs/C10Z_ASTRA_PREREG.md:73–81,323–339`). Paper fidelity is verified at the method level, rather than UNVERIFIABLE; transfer to this machine/task remains untested.

**Write-only adjudication: WRITE-QUALIFIES for the bounded analytic compiler described, subject to the fixes and open route gates below.** This is a recommendation about the method class, not an operator ruling or deployment approval. The criterion allows a per-commit solve regenerable from the patch and excludes a training set or training loop (`EXPERIMENT_RUNBOOK.md:330`; `results/research_pass_2026-10-06/recommended_sequence.md:13`). Here the patch and frozen artifacts specify the constraints, each weight update follows a direct linear solve, and the fixed carrier set/ten-round cap bounds the procedure (`docs/C10Z_ASTRA_PREREG.md:37–40,73–81`). Iteration alone cannot be the discriminator: accepted recipe A already writes one layer, then re-reads keys/current activations for the next solve (`experiments/track_c/c10e_bandknob.py:194–217`). Step 7 instead back-propagates an LM loss into weight factors, the recorded reason for MEASUREMENT-ONLY (`results/c10y_directdw_advisor_v1.md:6,41–51`; `EXPERIMENT_RUNBOOK.md:343`).

I agree with advisor Q1's classification, but reject its statement that ASTRA has already passed real-time, audit and compaction fitness (`results/c10z_astra_advisor_v1.md:23–35`). Those are empirical gates. Neither absence of gradients nor the number of `compute_z` steps proves cheap compaction. `compute_z` optimizes an activation on frozen weights, which is a different variable (`memit_dry_run/memit/memit/compute_z.py:83,104–105`). Also, ASTRA would replace the designated engine and its mandatory safeguards; §8.2 amendment remains required regardless of WRITE-QUALIFIES (`research_and_specs/llm-as-database-v1_2-integrated-spec.md:309–317`; `docs/C10Z_ASTRA_PREREG.md:42,296`).

**Checks requested in the brief:** the baseline envelope is correctly copied as A7 full [5,18], canonical [5,10], first-token [42,59], with A1/A2 ≥68; moving Z0 resolves the remaining ordering defect (`CORPUS/44_C10L_COVGEOM_SPARSEBAND.md:39`; `docs/C10Z_ASTRA_PREREG.md:119–122,205`). Both factual corrections are already correct: ρ is the remaining residual, and `compute_z` scores every target token while the weight solve gathers subject-last keys (`docs/C10Z_ASTRA_PREREG.md:28–29`; `CORPUS/44_C10L_COVGEOM_SPARSEBAND.md:43`; `memit_dry_run/memit/memit/compute_z.py:60–65,141–150`; `memit_dry_run/memit/memit/compute_ks.py:19–37`). The band-only snapshot/restore claim is correct; the full 36-layer restore must occur before the next arm's pre-edit probes, not merely at wrapper entry (`experiments/track_c/c10e_bandknob.py:150–159,461,473–476,489–506`). Memory feasibility is plausible by arithmetic; the runtime budget is UNVERIFIABLE as currently decomposed, not established by the advisor's FEASIBLE verdict (`docs/C10Z_ASTRA_PREREG.md:159–190`; `results/c10z_astra_advisor_v1.md:62–74`).

1. **BLOCKING — advisor item 1: AGREE-WITH-CHANGE. Independent active-path verification is missing, but its proposed frozen-scale test can reject correct code.**

   Z3's zero right-hand side cannot establish the active algebra; it does establish that the write plumbing executes inertly. Z4 checks two assemblies consuming the same keys, so shared position/layer mistakes remain possible (`docs/C10Z_ASTRA_PREREG.md:143–144`; advisor `:101–106`). The advisor's Z7 predicts finite last-layer lead changes with the old scale and also demands approximately one logit from γ=1 (`results/c10z_astra_advisor_v1.md:110`). **I-INFER:** even at layer 35, RMSNorm changes the scale; ridge and fp16 rounding also intervene. With x=(1,0), v=(0.5,0.2), c=(1,0), eps=1e-6, the frozen-scale prediction is +0.707106 while the finite normalized change is −0.012405. This is a mathematical counterexample to treating that prediction as an exact active-path answer, using the norm implemented at `.venv/lib/python3.11/site-packages/transformers/models/qwen2/modeling_qwen2.py:220–225` and the draft's scale at `docs/C10Z_ASTRA_PREREG.md:73`.

   **Exact replacement/addition to §2.8:**

   > **Z7 — independent key locus and active known-answer control.** On the identical 144-row batch, independently retain each selected layer's full `down_proj` input with the unmodified `util.nethook.TraceDict` API. Recompute row identities and zero-based requirement indices as `len(prompt_ids)+q−1`, q=0..T_i−1, directly from the recorded ID sequences, without the production gather table. Assert that every index is unpadded and that layer/module identities are exact. For the identity views of facts 1–4, compare every selected layer/position against the production keys; same-forward copies must be equal. Cross-shape comparisons are diagnostics, not tolerances calibrated on layer 35 and applied to other layers.
   >
   > Separately select up to eight actually failing identity-view requirements in deterministic (fact, position) order and run the production single-requirement solve/write on layer 35, restoring PRISTINE between controls. Independently calculate the scalar A and its ridge solution, and compare the production coefficients/columns with that answer using Z4's CPU tolerances. For the forward check, hold the original competitor fixed, use the realised fp16 column changes, and predict the finite normalized lead with the updated scale: `c·(x+v)/sqrt(mean((x+v)^2)+eps) − c·x/s`, where v uses independently retained keys. Reproduce the native norm/head cast order in the numerical reference; calibrate its rounding error at the same shape before gating, with a 0.25-logit ceiling. Record frozen-scale linearization error separately. Do not require the finite lead increase to equal γ: ridge, changed normalization and deployed rounding are included in the independent reference. Require at least one active control. A reference mismatch halts; a correct reference with poor objective improvement is not relabeled a code defect.
   >
   > Z3 is the identity plumbing check; Z4 is the assembly identity; Z7 verifies independent keys and the nonzero path. V5 requires all three. Add Z7 to the requirement map and named halt list.

   The API cited above supports independent retention (`memit_dry_run/memit/util/nethook.py:117–145`). The recommended control is prospective, not a performed model test. Extend Z3 to force two zero-deficit rounds in both Z and Z-band modes, so the carrier-reuse/final-observation path also executes before that mode is trusted; this follows the repeated path specified at `docs/C10Z_ASTRA_PREREG.md:81`.

2. **BLOCKING — advisor item 2: AGREE. Z0 precedes the templates it needs and the claimed LAW#3 barrier.**

   Stage 0 step 2 uses the 144-row observation before step 3 first samples its contexts; the engine cache is initialized on first use (`docs/C10Z_ASTRA_PREREG.md:117–122`; `memit_dry_run/memit/memit/memit_main.py:304–323`). This is an execution dependency error. The existing numeric LAW#3 window is correct and must remain unchanged.

   **Exact replacement for stage 0 steps 2–5:**

   > 2. Run untouched recipe A on A1/A2/A7, retaining raw post-write probe hits; freeze its context templates and their hash in process 1, or load that same file before recipe A in process 2. Restore PRISTINE.
   > 3. Check LAW#3: A7 `para_full_n` in [5,18]/72, `canon_full_n` in [5,10]/24, `para_first_n` in [42,59]/72; A1/A2 `para_full_n` ≥68/72. A miss writes the baseline-only record and HALTED-V4 diagnostic and exits. No candidate or new-writer observation/check runs.
   > 4. Check all 36 pristine hashes, then obtain pristine probe hits, the pristine lead distribution and Z0 using the frozen templates. Derive newly induced baseline hits from the stored raw baseline hits and these pristine hits.
   > 5. Prepare D and G, check V7/V8, then execute Z0–Z7 before any candidate output is trusted.

   Replace the stage heading with: “No new-writer observation, instrument preparation or candidate runs before the LAW#3 gate in step 3.” Keep the same gate in process 2.

3. **BLOCKING — advisor item 3: AGREE-WITH-CHANGE. Gate every trained prefix depth and use prompt-level induction, including full remainders.**

   A requirement exists at every value position, while F1 currently tests only depth 1 (`docs/C10Z_ASTRA_PREREG.md:74–75,153,230`). The advisor extends next-token gates to all depths but full-remainder gates only at j=1, leaving induction of longer continuations insufficiently checked (`results/c10z_astra_advisor_v1.md:139–147`). A newly completed remainder can occur with an unchanged already-correct next token; totals alone do not identify new hits. The existing definition is prompt-level post-hit absent on base (`docs/C10T_SECONDKEY_PREREG.md:48`).

   **Exact replacement for the F1/G7 and subject-free clauses:**

   > For every fact i and prefix depth j=1..T_i−1, record next-token and full-remainder booleans on each of the six unedited subjects, under every fitted frame as specified below. Build probe inputs from prompt IDs concatenated with `V_ids[:j]`; decoded strings are display fields. A newly induced hit is `post_hit AND NOT pristine_hit` on that exact prompt. G7 requires, separately for each (frame,i,j), newly induced next-token hits ≤ recipe A +1/6 and newly induced full-remainder hits ≤ recipe A +1/6. Equality passes.
   >
   > Subject-free prompts use the neutral frame “The name is” and all depths. Count a fact once if any depth has a newly induced full-remainder hit. Add -SUBJECT-FREE iff that /24 count exceeds recipe A's +1. Preserve raw hits and matched prompt IDs. A1 is not applicable; A2 has one depth.

   This replaces the depth-1 exception rather than adding a second, conflicting gate. Apply the identical probe population to pristine, A and each candidate.

4. **BLOCKING — advisor item 4: AGREE-WITH-CHANGE. Z-band fit is necessary, but clean objective/site attribution also needs the additional fixes in item 15.**

   The current rule can call an unsuccessful band solve SITE-DEPENDENT (`docs/C10Z_ASTRA_PREREG.md:220,268`). The same problem applies if Z itself is UNDERFIT or Z-band obtains its count with locality damage.

   **Exact addition at the start of the attribution rule:**

   > Apply the final-observation fit rule to both Z and Z-band. If either is UNDERFIT, report ATTRIBUTION-UNINFORMATIVE with the arm and failing fit fields. If Z-band fails its A7 locality/subject-free/size gates, report ATTRIBUTION-TRADEOFF; do not call the gain retained cleanly. Only otherwise apply the capacity-matched descriptive comparisons below. These are attribution statuses and do not alter Z's primary label.

   Add the advisor's Z-band φ_μ=0.61 example as ATTRIBUTION-UNINFORMATIVE (`results/c10z_astra_advisor_v1.md:159`); also include a fit-but-locality-failing band example. The primary label's validity and attribution's informativeness are separate.

5. **ADVISORY — advisor item 5: AGREE-WITH-CHANGE. Reproduce native cast order; do not replace one unmeasured tolerance with 0.05.**

   The installed norm converts to float32, normalizes, then converts back before gain multiplication; native head outputs are not automatically upcast for this loss-free call (`.venv/lib/python3.11/site-packages/transformers/models/qwen2/modeling_qwen2.py:220–225,836–843`). The advisor's fp32 two-row dot is therefore still different from the native fp16 full head, and its 0.05 floor is not measured on this model (`results/c10z_astra_advisor_v1.md:163–167`).

   **Exact replacement for Z1:**

   > Reconstruct final norm/head output using the installed modules' native cast order and the same full tensor shapes, comparing captured positions against native output. Independently record the float32 analytic lead used by the solver. Calibrate its reconstruction error σ_head on the pristine batch; use τ_head=max(2σ_head,0.02), halting if τ_head>0.25. Apply that fixed bound after writes. Keep τ_shape from Z0 separate; a cross-shape floor is not a head-reconstruction calibration.

6. **ADVISORY — advisor item 6: AGREE-WITH-CHANGE. A source-scale guard is reasonable; it is not a validated safety threshold for this batch.**

   The source's SemCon medians are 0.07–0.24, versus 0.09–0.55 for the alternatives ([ASTRA v1 §4.2, Table 2](https://arxiv.org/html/2610.05277v1#S4.SS2)). Those observations do not establish a safe cutoff on this different joint-batch/domain configuration (`docs/C10Z_ASTRA_PREREG.md:325,327,329`; advisor `:169–183`).

   **Exact replacement for W1 and §6(g):**

   > W1 is a prospective conservative guard: add -LARGE-WRITE when the median realised final carrier-column relative change exceeds 0.55; equality passes. This is anchored to a reported source range, not a proven safe/unsafe boundary for Qwen fact editing. Report median, IQR, p95, maximum and carrier count; note values above 0.24 separately. A zero original column has ratio 0 if unchanged and +∞ if changed; do not silently divide by an arbitrary denominator. Replace the UNVERIFIED paper-range question with this rationale. No norm threshold substitutes for locality gates.

7. **BLOCKING — advisor item 7: AGREE-WITH-CHANGE. Correct the inference from same-process noise; preserve artifact identity instead of silently loosening the certificate.**

   A same-process floor does not prove cross-process reproduction (`results/c10s_sharedz_halt_analysis_2026-10-06.md:11,25`; `REPRODUCIBILITY.md:26`). I disagree with replacing R1 by Jaccard≥0.98, rounds±1 and error≤1e-2 merely because strict regeneration might fail (advisor `:193`). The draft explicitly proposes ownership by output hash while allowing a nonzero output discrepancy as “the same write” (`docs/C10Z_ASTRA_PREREG.md:130–132,261–266`). The ledger still owns a concrete overlay hash (`research_and_specs/llm-as-database-v1_2-integrated-spec.md:671`).

   **Exact replacement for the regeneration claim/certificate:**

   > The measured zero floor is same-process, same-shape evidence only; cross-process MPS regeneration is UNVERIFIABLE until process 2. Distinguish `artifact_identity` from `numeric_behavioral_reproduction`. Artifact identity is EXACT only when canonical output bytes and their H_out match; different hashes remain different artifacts even when behavior agrees. R1–R3 test numerical/behavioral reproduction and cannot replace the ledger's stored overlay hash. Retain the preregistered R1 thresholds: identical carriers, identical write-round count and relative per-layer error≤1e-3. If both layer deltas are zero, error=0; if only one is zero, reproduction fails. Rank carriers with a fixed score/layer/neuron tie order. Failure reports the failed field; no after-the-fact tolerance relaxation. The certificate records both hashes and both statuses.

   Behavioral verification remains legitimate under `REPRODUCIBILITY.md:26`; claiming identical artifact ownership from it does not follow. Route replay semantics stay OPEN if artifact identity fails.

8. **ADVISORY — advisor item 8: AGREE-WITH-CHANGE. Replicate the common claim, while retaining the numerical and locality checks.**

   LEAD/PARTIAL at counts 30/29 supports a common PARTIAL under the draft's lower-rank rule, but the current suffix says it did not replicate (`docs/C10Z_ASTRA_PREREG.md:261,281`). The advisor's exception should not bypass R1–R3 or process-2 qualifiers (`results/c10z_astra_advisor_v1.md:198–200`).

   **Exact replacement for the cross-process label clause:**

   > Compute the lower base label and union of substantive qualifiers. When both processes have clean PARTIAL-or-LEAD evidence and R1–R3 pass, the common lower label is replicated, including LEAD/PARTIAL→PARTIAL. Record `lead_replicated=false` for that boundary case. Otherwise preserve -NOT-REPLICATED for incompatible positive claims and -NOT-REPRODUCIBLE for any R1–R3 failure. The scheduling marker -SINGLE-PROCESS is removed only after a valid required second process completes; -STAGE1 never means G0 passed.

   Worked row 8 should say “PARTIAL replicated if all R1–R3 and both processes' gates pass; LEAD not replicated,” rather than declaring reproduction from R2 alone.

9. **ADVISORY — advisor item 9: AGREE-WITH-CHANGE. Add the omitted shared-contract records without using held-out text to select inputs.**

   The shared contract requires non-written relation probes and an overlap audit for non-triple inputs, including statistics; the advisor's replacement audits templates only (`results/research_pass_2026-10-06/prereg_stubs.md:10–12`; `results/c10z_astra_advisor_v1.md:204–212`).

   **Exact additions to stage 0 and readouts:**

   > Freeze context/reference inputs without using PTEST to select or rewrite them. Then record normalized-overlap audits against PTEST for both the frozen view strings and the D reference texts, with the normalization/score definition fixed in the prereg. Audits are reported diagnostics, not a reason to select a more favorable input after inspection. Hash the input population and audit implementation. Record “{s} is a” and “{s} is associated with” pre/post top-1 changes and flips to edited values on all 24 subjects, alongside described_as. Report the per-edge behavior-pass vector, true iff all three held-out templates succeed.

   The per-edge rule is also part of the shared contract (`results/research_pass_2026-10-06/prereg_stubs.md:7`); it must accompany aggregate /72 counts.

10. **ADVISORY — advisor item 10: AGREE. Correct attribution/quotation hygiene, keeping absolute GPU timing out of the Mac estimate.**

    Its proposed source qualifications are supported ([ASTRA v1 §3.3, §4.3–4.4](https://arxiv.org/html/2610.05277v1)); use paraphrases rather than additional quotations.

    **Exact replacements:**

    > At line 31: “Each failing token adds a patch requirement (§3.3).” At line 40: “The reported 2.7-second average excludes answer generation and came from shared-GPU measurements; it is not a Mac or 24-fact-batch estimate (§4.3).” At line 77: “The reported neuron shares are 0.76–0.95% for 1B and 0.22–0.52% for 8B/9B (§4 Configuration).” At line 52: “The paper associates unseen-phrasing robustness with both its differently worded views and its margin (§4.4); their effects on this fact-writing adaptation are untested.”

11. **ADVISORY — advisor item 11: AGREE-WITH-CHANGE. Specify the head path, but use the native full head for v1.**

    A loss-free native call still projects all positions when `logits_to_keep=0` (`.venv/lib/python3.11/site-packages/transformers/models/qwen2/modeling_qwen2.py:836–843`; advisor `:222–230`). The proposed chunked vocabulary head adds another shape/rounding seam. **I-INFER:** the draft's illustrative 144×28×151936 fp16 logits occupy 1.225 GB; full-head projection costs about 2.509 TFLOP, rather than the requirement-only 0.5 TFLOP. This arithmetic uses `docs/C10Z_ASTRA_PREREG.md:170,173,184` and the pinned config's vocabulary/hidden sizes (`hf_cache/hub/models--Qwen--Qwen2.5-3B/snapshots/3aab1f1954e9cc14eb9509a215f9e5ca08227a9b/config.json:9,27`).

    **Exact replacement for the observation/head and memory clauses:**

    > V1 uses the native `model(...)` head with no labels, `logits_to_keep=0`, and a frozen recorded `use_cache` setting; no vocabulary-chunked head is introduced. Gather only valid requirement positions for target/competitor analysis, then release full logits. Budget B×T_pad×V×2 bytes for the fp16 logits, plus any actual conversion copies; record T_pad, peak and head time. At the illustrative T_pad=28 this tensor alone is 1.225 GB. A later compact-head variant needs its own numeric parity check. No float64 operation occurs until its operands have moved to CPU.

    This is a memory correction, not a finding that the 48 GB machine cannot fit the job (`docs/C10Z_ASTRA_PREREG.md:177–179`).

12. **ADVISORY — advisor item 12: AGREE. Make the last observation and budget-halt status unambiguous.**

    The draft refers to a final observation but does not explicitly schedule an extra one after a tenth update; its round-time halt lacks a named validity label (`docs/C10Z_ASTRA_PREREG.md:81,190,200–220,300`).

    **Exact replacements/addition:**

    > Fit and stop diagnostics come from one additional observation after the last weight update, at the same recorded 144-row shape, with no solve/write. `rounds_used` counts writes, not observations. `stop_reason` distinguishes objective met, round cap, and instrument/budget halt. Add V13: a synchronized stage-1 round wall-clock>120 seconds yields HALTED-BUDGET, never NULL or UNDERFIT. Equality at 120 seconds passes. Record time already spent and the incomplete observation fields; do not lower the round cap inside the run.

13. **ADVISORY — advisor item 13: AGREE-WITH-CHANGE. Stop automatic expansion on a disqualified survivor; do not add a routine operator decision.**

    A7's fit/locality/size qualifiers cannot be repaired by running separate A1/A2 and Z-band writes (`docs/C10Z_ASTRA_PREREG.md:123–127,247,251–260`). The advisor is right that TRADEOFF expansion buys attribution only (`results/c10z_astra_advisor_v1.md:238–242`); the same applies to positive UNDERFIT or other adoption-blocking qualifiers.

    **Exact replacement for K1's expansion rule:**

    > Count survival is exactly `n≥19 AND n−a≥10`. Automatic stage 2 additionally requires A7 FIT, all measured side gates passing and no -LARGE-WRITE, -SUBJECT-FREE or -EXCEEDS-TTL. Otherwise close stage 1 with the correct base label/qualifiers and -STAGE1, recording G0 and attribution as not run. A diagnostic expansion of a disqualified survivor is separate named work with a separate budget, not an automatic continuation. K2 remains conditional on an unqualified stage-2 PARTIAL or LEAD.

    The count threshold stays fixed: first survivors are n=19 for a=5 or 9, n=20 for a=10, and n=28 for a=18. Those are deductions from the existing K1 predicates (`docs/C10Z_ASTRA_PREREG.md:224,251`), not alternative thresholds.

14. **ADVISORY — advisor item 14: DISAGREE with moving 5b immediately after the oracle; AGREE that its queue position must be explicit.**

    The advisor's replacement silently skips queued step 4 (`results/c10z_astra_advisor_v1.md:248–250`). The integrated queue puts step 5 ahead of step 4, with steps 6/7 and 5b later; the standing step-7 demotion is unchanged (`docs/INTEGRATED_QUEUE_2026-10-07.md:18–23`; `EXPERIMENT_RUNBOOK.md:331,342–343`). An oracle in the band is not a proven upper bound on a different late-layer writer, so its failure must not mechanically kill ASTRA (`docs/C10Z_ASTRA_PREREG.md:64,77,108`; `results/c10y_directdw_advisor_v1.md:9` already calls the comparison a prior).

    **Exact replacement for §6 decision 0:**

    > Recommend considering 5b as step 7's replacement in the existing integrated-queue slot, after the prior queued steps, including the step-5 oracle and step 4. Reviews do not themselves move it to the next GPU job. Any changed ordering is recorded explicitly under the standing program/operator authority. Report the oracle as context, not an upper bound or an automatic ASTRA kill. Run one GPU job at a time; this design review authorizes no model run.

**Additional findings the advisor missed or did not resolve:**

15. **BLOCKING — the attribution comparison changes capacity, and OBJECTIVE-CARRIES can be issued when the band has no qualifying gain.**

    Z allocates `9·ceil(16T/9)` carriers; Z-band allocates `5·min(ceil(16T/5),440)` (`docs/C10Z_ASTRA_PREREG.md:77,90,108`). **I-INFER:** for T=72 those counts are 1152/1155; for T=144 they are 2304/2200. Counts differ at 65 of the 73 integer T values in the stated range. More importantly, a=12, n=22, n_b=17 satisfies the current OBJECTIVE-CARRIES test, although 17 remains inside the baseline envelope and band gain=5 is below +10 (`docs/C10Z_ASTRA_PREREG.md:268`). Even a clean band gain would show the whole ASTRA package working in-band, not isolate its objective from selection, preservation statistics or repeated solves (`:73–85,108`).

    **Exact replacement for the Z-band budget and remaining attribution tests:**

    > Z-band keeps the five band layers and matches Z's total carrier count B_Z exactly, distributing `floor(B_Z/5)` per layer plus one to the first `B_Z mod 5` layers in ascending layer order. If B_Z>5×440, run the capped band control only as a diagnostic and report ATTRIBUTION-UNMATCHED-CAPACITY; it cannot decide the site question. Publish counts, parameter counts and final patch norms for both arms.
    >
    > After the fit/locality guards: BAND-RETAINS-QUALIFIED-GAIN iff `n_b≥19 AND n_b−a≥10 AND n_b≥n−5`; BAND-NO-QUALIFIED-GAIN iff `n_b≤18 OR n_b−a≤9`; otherwise BAND-PARTIAL-RETENTION. Tests are ordered and exhaustive. These describe this matched solver package and do not identify objective causality or prove that late layers are necessary. Replace OBJECTIVE-CARRIES/SITE-DEPENDENT/MIXED wording throughout and update the worked rows.

16. **BLOCKING — FIT can coexist with zero actual canonical matches, because Z2 can exempt every fact.**

    The fit gate counts identity leads>0, whereas Z2 excludes every fact with any |lead|≤τ (`docs/C10Z_ASTRA_PREREG.md:140–142,217–220`). **I-INFER, explicit predicate counterexample:** take 24 four-token facts and six views, M=576 requirements. Give each identity view one +0.001 lead and all other requirements leads≥5. Then φ_μ=552/576=0.95833 and φ_0^id=24, so FIT holds. All 24 identity facts are Z2-ambiguous at τ=0.02; actual `canon_full_n=0` is not rejected by those rules. This is a permitted record configuration, not a claim that a model produced it. Furthermore Z0's single unpadded full-sequence reference still differs in shape from the per-prefix calls the actual greedy evaluator makes (`experiments/track_c/c10e_bandknob.py:109–117`).

    **Exact replacements for Z0/Z2 and U:**

    > At each identity-view value position q, Z0's single-sequence reference uses exactly `prompt_ids + target_ids[:q]`, the prefix shape used by the binding evaluator if earlier targets matched. Record the original full-sequence comparison separately. Z2 reports checked and ambiguous fact counts explicitly; zero checked facts is not evidence of observation/evaluator agreement.
    >
    > Let M be the integer number of requirements and m the integer number with lead≥5. FIT requires `20m≥19M`, φ_0^id≥23, and the unmodified evaluator's actual `canon_full_n≥23/24`. Otherwise U holds. Keep the existing NULL→UNDERFIT and positive-label -UNDERFIT rules. φ_0^id remains a diagnostic of the observation batch, not a substitute for deployed canonical success. Freeze these comparisons before launch.

    Equality at 95%, 23 canonical facts and 23 positive-lead identity facts passes; lead=0 does not count positive, lead=5 does count margin-met. This closes the fit/generation inference without changing K1's held-out threshold.

17. **BLOCKING — locality probes omit five fitted frames, so prefix-conditioned spillover can receive a clean label.**

    ASTRA fits six prefix/context views, but F0/F1 are currently CANON-only; the shared contract demands same-frame probes separately in every fitted frame (`docs/C10Z_ASTRA_PREREG.md:74,153`; `results/research_pass_2026-10-06/prereg_stubs.md:10`). Expanding prefix depth as advisor item 3 proposes does not fix the omitted frame dimension. **I-INFER:** a patch can leave bare CANON bystanders unchanged while inducing values on another fitted context; those records satisfy the current S definition.

    **Exact additions to G2/G7:**

    > For each of the six frozen context templates, form that template's CANON view for every unedited FRAME_SUBJECT. Record F0 separately for each view and require its flips≤recipe A+1/6 in every view. Apply the every-depth F1 gates separately in every fitted view. No pooling of flips across views or substitution of a mean for an individual gate. Count and publish the full probe population before launch; baseline and candidates use identical IDs.

    The enlarged population must enter the runtime budget; it is not justified by an assumed two-minute allowance.

18. **BLOCKING — H_in does not yet bind all inputs that determine the write or its comparator.**

    The manifest lists strings/model revision/context/D/G/settings/driver/reader, but omits tokenizer artifacts and actual input IDs, the prereg hash, source screens/hparams, full engine identity and baseline covariance hashes (`docs/C10Z_ASTRA_PREREG.md:132,202,212`). The harness constructs targets/stimuli from the tokenizer/screens and loads hparams/covariances (`experiments/track_c/c10e_bandknob.py:45,67–68,224–250,342–354,459–470`). Those dependencies can change a or token positions without changing the current manifest fields. “Fixed shape” also needs actual IDs, masks, padding and model-forward settings; model config enables caching by default (`hf_cache/hub/models--Qwen--Qwen2.5-3B/snapshots/3aab1f1954e9cc14eb9509a215f9e5ca08227a9b/config.json:24`).

    **Exact addition to §2.7/§2.12/V12:**

    > H_in additionally binds prereg SHA-256; complete engine source identity; hparams and stimulus/locality screen hashes; every band covariance hash used by recipe A/V7; tokenizer JSON/config/special-token hashes; the ordered per-arm prompt/target IDs, attention masks, padding side and padded lengths; model-forward/cache/attention settings; actual device/dtype; installed torch/transformers versions and CPU solver/backend metadata. Pin the D dataset revision, row IDs/text hashes, tokenizer/truncation policy and actual nonpadding token count. Process 2 loads and validates the complete same manifest before baseline or candidate work. Requests and input artifacts are immutable; an attempt uses a fresh OUT_DIR and refuses existing manifest/pass files.

    This is provenance for the proposed certificate, not a demand for another science run.

19. **BLOCKING for the budget/go decision — the claimed 62-minute early stage rests on an unsupported decomposition and omits the revised verification costs.**

    The draft reinterprets 34 minutes per three-arm harness pass and 23 minutes per behavior run as “23 minutes evaluation for three arms,” then divides by three to obtain 7.7 minutes per arm (`docs/C10Z_ASTRA_PREREG.md:183–188`). The cited queue calls 23 minutes a whole run (`docs/INTEGRATED_QUEUE_2026-10-07.md:18`); it supplies no edit/evaluation split. The step-3 review already found that behavior-only accounting missed precursor and repeated projector/proof work (`results/c10u_mint2_advisor_impl.md:88–94`). Native `run_recipe` computes five projectors and runs LAW#5 every call, and its evaluator contains several independent generation passes (`experiments/track_c/c10e_bandknob.py:166–178,358–365,461–463`). Neither the advisor's added 2–4-minute probes nor its seconds-to-minute G claim is a measured Mac bound (`results/c10z_astra_advisor_v1.md:67,73–74`).

    **I-INFER:** 48 GB capacity remains plausible with CPU-only float64; the new native-logit accounting does not exhaust it. But dense A storage scales as F² and dense solve work as F³, so matrix bytes alone do not establish compaction throughput. First-1000 Wikipedia rows contain at most 100,000 truncated tokens, not necessarily exactly that number; mask padding and short rows (`docs/C10Z_ASTRA_PREREG.md:78`; `memit_dry_run/memit/rome/layer_stats.py:101–104,142–165`). No live timing or memory validation was performed in this review.

    **Exact replacement for §2.11 and §6 decision 2:**

    > Measured anchors are approximately 34 minutes for the cited three-arm harness pass and 23 minutes for the cited behavior run. Their evaluation-only components are UNVERIFIABLE; they are not divided into per-arm evaluation estimates. The ASTRA, D, G, new-control, all-frame/all-depth-probe and hashing costs on this Mac are UNMEASURED. Stage 0–1 has a provisional 90-minute hard budget, not a demonstrated 62-minute cost or guaranteed completion window. After LAW#3, separately time D, G, verification, candidate rounds, binding evaluation, all locality probes and restoration/hashing with synchronization at MPS timing boundaries. Publish cumulative projected total before starting the candidate and stop HALTED-BUDGET if the fixed budget cannot accommodate the remaining required checks. Do not drop gates to fit the clock. Stage-2/3 budgets are recomputed from those measured components before expansion; the previous 4.1-hour maximum is withdrawn as UNVERIFIABLE. Report per-write solve-only time separately from validation/serialization/end-to-end compile time. W2>60 minutes is a disqualifier; W2≤60 does not prove the declaration-to-completion Write Lock TTL or compaction fit.

    A 90-minute cap is a proposed resource bound, not approval to run. The Write Lock starts at task declaration and has a 60-minute TTL; the separate incremental PREPARED default is two hours (`research_and_specs/llm-as-database-v1_2-integrated-spec.md:678,781–785`).

20. **ADVISORY — tighten the review answers and status fields so algorithm qualification, route fitness and scientific labels cannot collapse.**

    The draft calls its two write qualifications “neither ... a ruling issue,” and proposes a certificate as how a ledger could own the write (`docs/C10Z_ASTRA_PREREG.md:42,132,318`). That overstates what a method-class adjudication settles. The advisor also treats a first-order held-out transfer proxy as the cheapest overturning test; the actual binding observation is free greedy recall, not the proxy (`results/c10z_astra_advisor_v1.md:254`; `experiments/track_c/c10e_bandknob.py:109–117,396`).

    **Exact replacements/additions:**

    > Write-only recommendation: WRITE-QUALIFIES for this fixed-input, bounded analytic solve. This does not establish real-time use, artifact-identical regeneration, compaction fitness or designated-engine compliance; those remain OPEN and can prevent route adoption. Record the actual reviewer model/effort and report path in §8. Review results are advisory, not empirical evidence.
    >
    > Keep six engine-derived views, joint T=ΣT_i and μ=5 fixed for v1; record pristine and recipe-A lead distributions without tuning μ to the observed result. Keep the stacked writer out of v1. V7 uses all available cached layers 4–12 with the preregistered ≥0.80 sanity bound, while explicitly leaving late-layer statistical fidelity unverified by that comparison. Margin/fit/norm cutoffs are operational candidate criteria, not validated field-wide constants.
    >
    > The cheapest binding falsifier is stage 1 after valid instruments: a FIT, correctly restored Z A7 write that fails `n≥19 AND n−a≥10` ends this configuration. The held-out first-order transfer diagnostic is reported after the final write and cannot stop, select rounds or tune a later update. Near-zero predicted transfer does not falsify a nonlinear multi-round writer before it finishes.

    Those replacements answer §6(a)–(h) with determinate v1 choices rather than additional routine operator questions (`docs/C10Z_ASTRA_PREREG.md:307–314`). Any follow-up configuration receives a new prereg; no design review or proxy closes C10.

Verification of the review's label analysis: Table T's five predicates are disjoint and cover all 2,044 valid integer (a,n,S) combinations with a=5..18, n=0..72 and S∈{false,true}; its base-label partition is sound (`docs/C10Z_ASTRA_PREREG.md:224–245`). NULL deliberately includes a positive count outside the historical envelope when gain≤9; it means “no qualifying gain,” not evidence of zero change. Rule U and the additional attribution/replication fixes above carry the necessary distinctions. Non-finite, malformed or missing mandatory records must halt rather than enter that partition (`docs/C10Z_ASTRA_PREREG.md:200–212`). Boundary tests for the eventual reader must cover a=5/18; n=18/19/29/30; g=9/10; exact fit equality; exact side-gate equality; W1 and W2 equality; an all-ambiguous Z2 population; Z-band UNDERFIT/cap mismatch; and the LEAD/PARTIAL process pair.

Restore closeout to add before implementation: “Wrap each recipe/check in a driver `try/finally` restoring all 36 down projections and checking Z6. Remove this driver's capture hooks before evaluator calls, on normal return and exceptions; assert return to the recorded initial hook registry. A hook/restore failure is a halt and no later arm runs.” `run_recipe` has no exception-protected full-model restore, and hooks execute before its normal restore (`experiments/track_c/c10e_bandknob.py:489–509`). This agrees with advisor Q4 (`results/c10z_astra_advisor_v1.md:76–84`); checking registry equality is more precise than assuming every pre-existing registry must be empty.

This file is the completed read-only design review. No proposed scientific gate was run; implementation parity, MPS runtime, regeneration and route performance remain UNVERIFIABLE. FIX-FIRST applies to freezing/building the reviewed design as written, not to the fact that this review deliverable exists.
