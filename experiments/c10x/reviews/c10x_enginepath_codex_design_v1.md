# D-C10x-enginepath v1 — independent Codex design review

Reviewer model: **GPT-6 / Codex** (the session's system description). **Exact runtime model ID and configured effort: UNVERIFIABLE; neither is exposed to this reviewer.** I cannot certify the draft's recorded designation “GPT-6-Astra high.” Date: 2026-10-07.

**Verdict: FIX-FIRST**

**Single most important fix:** replace the FE identity-only check with an active-path reduction through the real target builder and writer, with matched batch shapes and an explicit reference. The current identity branch disables every FE-specific change, so passing it cannot validate the proposed intervention (`docs/C10X_ENGINEPATH_PREREG.md:43–44,71`; advisor item 3, `results/c10x_enginepath_advisor_v1.md:71–89`). Item 3 below gives the configuration, quantities and tolerances. Enforce the baseline gate before starting that candidate work (item 1).

This is a design review, not an implementation or runtime result. The binding behavioural readout is appropriate: the harness greedily generates every target token and requires the full ID sequence, over three held-out templates for each of 24 subjects (`experiments/track_c/c10e_bandknob.py:108–117,358–399`). The work concerns the Write Engine and post-write behavioural verification cells, advancing the live C10 question rather than closing F1 (`docs/SPEC_E2E_GROUND_TRUTH.md:14,22–30,64–65`; `docs/INTEGRATED_QUEUE_2026-10-07.md:21`; `docs/C10X_ENGINEPATH_PREREG.md:141`). All replacement blocks below are **proposed pre-run text**, not observed results or permission to dispatch a job.

## Responses to every advisor item

### 1. BLOCKING — advisor item 1: AGREE — LAW#3 must stop the driver before candidate work

The draft orders candidate targets, inertness and injection before recipe A, then runs both candidates, while making the reader the sole labeller (`docs/C10X_ENGINEPATH_PREREG.md:90–103,111`). LAW#3 explicitly requires reproduction before a new arm runs (`CLAUDE.md:30`). The envelope is correctly quoted; its enforcement point is wrong (`CORPUS/44_C10L_COVGEOM_SPARSEBAND.md:39`). The baseline recipe can execute independently because it solves its own targets when the override is unset (`experiments/track_c/c10e_bandknob.py:185–191`).

**Replacement for §2.7 Process 1 and §3 LAW#3:**

> After fingerprint, knob refusal, import/state validation and the stimulus leak check, run recipe A first with `FE_STATE=None` and `H.Z_OVERRIDE=None`. Its standing G gate must pass. Immediately apply the shared LAW#3 predicate in the driver: A7 `5 <= para_full_n <= 18`, `5 <= canon_full_n <= 10`, `42 <= para_first_n <= 59`; A1 and A2 each `para_full_n >= 68`. Denominators must be 72, 24 and 72 respectively. These endpoints are inclusive and come from `CORPUS/44_C10L_COVGEOM_SPARSEBAND.md:39`. On failure, record A and a HALTED/INVALID diagnostic, exit non-zero, and execute no candidate target solve, replay, candidate injection or candidate write. The reader independently rechecks the same predicate. Only after this gate passes: construct the targets; run W0 and every X1/X2 gate; perform the injection screens; run I-2 then I-1. Apply the same ordering in process 2. Baseline-only halted records do not become candidate NULLs.

### 2. BLOCKING — advisor item 2: AGREE — restore to one verified pristine snapshot

`run_recipe` snapshots the weights it finds at entry, uses that snapshot as the per-arm baseline and restores it at exit (`experiments/track_c/c10e_bandknob.py:458–476,506–509`). The standalone parity checks also write weights (`docs/C10X_ENGINEPATH_PREREG.md:69–71`). Therefore a leaked edit can redefine both the next recipe's baseline and its locality reference; a later `run_recipe` restore does not repair that premise. This is the concrete defect named by the advisor (`results/c10x_enginepath_advisor_v1.md:57–69`).

**Replacement addition to §2.4 and validity:**

> **W0.** Immediately after loading the unedited model, take one immutable `PRISTINE` snapshot of the five `down_proj.weight` tensors for layers 4–8. Hash each tensor's dtype, shape and contiguous raw bytes. Every standalone write check restores those tensors from `PRISTINE` in a `finally` block and uses a fresh zero cache. Remove replay/injection hooks in `finally` blocks as well. Verify pristine hashes before recipe A, target construction, injection, every standalone write check and each candidate recipe; verify them after every restoration and after the final recipe. A mismatch or leftover intervention hook HALTs before the next cell. Record all checkpoints and the offending layer/cell. A recipe-local entry snapshot is not a second authority for “pristine.”

### 3. BLOCKING — advisor item 3: AGREE-WITH-CHANGE — active FE reduction, with the engine/harness distinction explicit

The proposed singleton `[8]` reduction is useful: the local layer and final layer coincide, division by the number of remaining layers becomes division by one, and the target table can contain the unchanged engine's `z_8` (`docs/C10X_ENGINEPATH_PREREG.md:43–44`; `experiments/track_c/c10e_bandknob.py:184,197–204`). However, manually supplying that table bypasses the new target builder, and comparing residual **norms** cannot detect equal-norm vector permutations. The advisor's structure gate also compares different batch shapes unless item 10 is repaired (`results/c10x_enginepath_advisor_v1.md:85–86`; `docs/C10X_ENGINEPATH_PREREG.md:42`).

A necessary distinction: the harness solves a projected ridge-1 system in CPU fp32, whereas unmodified `execute_memit` solves the covariance-regularised system in CPU float64 (`experiments/track_c/c10e_bandknob.py:205–217`; `memit_dry_run/memit/memit/memit_main.py:191–206`; `configs/hparams/qwen25_3b_memit_hparams.json:12`). Consequently singleton FE does **not** algebraically promise bitwise equality to the full engine's weight update. Claim exact reduction to the unchanged target primitive and harness writer; retain the separate engine-versus-harness behavioural gate. Do not present these different comparisons as one exact engine-weight equivalence.

**Replacement addition to §2.4, superseding the advisor's X2-(vi)/(vii):**

> **X2-(vi), nonzero active singleton reduction.** In-memory `hp1` differs only by `layers=[8]`; use the layer-8 projector from the same verified covariance, a zero cache and the same ordered 24 A7 requests. Run the **actual FE target builder** with first/last layer both 8, using unmodified `compute_z(..., layer=8, ctx)`. The builder must retain the returned fp32 `z_8` as `FE_TARGETS[(subject,target_string)][8]`; do not replace it with its rounded fp16 hook output. With no later layer, replay contributes no additional target. Compare every built target vector against an independently obtained engine `z_8` with identical request, prompt/context list, padding shape, dtype and stopping rule. Then, from `PRISTINE`, compare the actual `fe_edit(mode="fe")` against the saved original `my_edit` with `Z_OVERRIDE` pinned to those same engine targets. Exercise the active table lookup, layer-local reader and undivided residual; do not call the identity branch. Compare the **complete pre-cast ΔW_8 tensor**, the applied fp16 weight tensor and the updated cache, not just their Frobenius norms. A nonzero reference update is required. Target and pre-cast ΔW relative-L2 errors must be <=1e-4 under the bounded same-shape floor rule in item 9; record max-absolute errors. Applied weights and greedy correctness flags must agree exactly. Evaluate the same 24 canonical and 72 held-out prompts on both results; equal aggregate counts alone are insufficient. Restore and verify W0 between sides.
>
> **X2-(vii), active multi-layer null and structure check.** For the production band [4,5,6,7,8], build identity replay targets by replacing the first-layer output with its own pristine output in the same 24-row padded canonical batch used by the writer. Use the resulting per-subject, per-layer vectors in actual `mode="fe"`, from `PRISTINE`. Each residual and update must be zero (relative error is undefined for a zero reference; require zero tensors), and the five applied-weight hashes must remain pristine. Targets are dictionaries keyed by actual layer integers, with exact `(subject,target_string)` request identities. An independent same-batch block-output observer checks the full `cur_l` vector at every layer, not merely its norm or a self-reported layer number. Also check the exact request/column order and `resid = M_l - cur_l` before the float32 CPU solve. A wrong-layer read or permuted target table must fail the model-free negative controls. No candidate target is substituted until these gates pass.
>
> **G and G8, direct engine references.** Keep the original five-layer `run_law5` comparison with unmodified `apply_memit_to_model`: `|Δexpr| < 0.05` and `|Δloc| < 3`, the existing behavioural thresholds (`experiments/track_c/c10e_bandknob.py:423–444`). In addition, G8 compares **active singleton FE** directly against unmodified `apply_memit_to_model` on `hp1.layers=[8]`, the same pristine state, context list and single canonical Zorbland→Cairo request. Restore W0 between sides. Run the real FE builder/writer on the FE side; do not use `run_law5`'s default-dispatch bypass for this comparison. Compare the Cairo next-token probability and described-as locality score using those same behavioural limits, and record complete distributions/top-1 IDs. G/G8 follow the standing source's rounding (expression difference to four decimals, locality difference to two) before their strict comparison; record raw differences too. Equality at the stored 0.05 or 3 fails. This is a direct **behavioural** engine-output check, not an assertion of exact engine ΔW equality. X2-(vi) separately validates exact target-primitive reduction and the FE writer against the unchanged harness reference. G, G8, X2-(vi) and X2-(vii) must all pass before candidate output is trusted; a G8 failure HALTs rather than being excused by the different regularizers.

The 1e-4 bar here is deliberately **same-shape**, not an excuse to raise the bar to 0.122: C10S's matched-shape reduction was exactly zero, while changing the batch from 7 to 19 rows produced relative distance 0.122 (`results/c10s_sharedz_halt_analysis_2026-10-06.md:11–25`). Item 10 makes the multi-layer null check achievable without importing that known confound. The singleton and null checks remain unrun in this review.

### 4. BLOCKING — advisor item 4: AGREE-WITH-CHANGE — one total classification and one replication trigger

The draft's qualifier/replication interaction and injection gap are real (`docs/C10X_ENGINEPATH_PREREG.md:97,116–137`). The advisor's replacement itself overlaps: its row 5 admits injection greater than `reference-9`, while row 6 covers deficits 6–9, so deficits 6–8 satisfy both (`results/c10x_enginepath_advisor_v1.md:103`). Also, “spreading is not the wall” is stronger than a NULL of this one package can show; the draft explicitly limits a miss to non-advancement of this configuration (`docs/C10X_ENGINEPATH_PREREG.md:15,132,141`).

**Replacement for §3 and the process-2 trigger:**

> **Validity and priority.** Missing/non-finite data, a fingerprint, W0, G, X1/X2, counter, provenance or LAW#3 failure gives INVALID/HALT before scientific classification. Validate exact denominators and that counts equal their per-prompt flags and per-fact sums. A candidate with A1<68 or A2<68 is INVALID-CONTROLS regardless of its A7 count. It never triggers replication. Otherwise let `A` and `C` be the same-process baseline and candidate A7 counts.
>
> **Count classes.** Define `lead_size = C >= 30`, `partial_size = 18 < C < 30 and C-A >= 10`, and `sized = lead_size or partial_size`. With all locality gates passing: LEAD for `lead_size`, PARTIAL for `partial_size`, NULL otherwise. With a locality failure: TRADEOFF only for `sized`, NULL otherwise, recording the failed locality axes beside that NULL. A count <=18 is always NULL. Append BELOW-BASELINE only to NULL when `C <= A-10`.
>
> **Qualifiers and eligibility.** LARGE-WRITE means the finite A7 summed-layer ΔW norm ratio is strictly >1.5; equality passes. UNDERFIT applies only to I-2 when fewer than 22 of its 24 A7 targets have fit >=0.98; both equalities pass. Record all applicable qualifiers. An arm is replication-eligible iff its base class is LEAD or PARTIAL and neither LARGE-WRITE nor UNDERFIT applies. Eligibility is evaluated before launching process 2; no qualified result is adopted. UNDERFIT and LARGE-WRITE are not instrument-invalidity labels.
>
> **Replication.** Run a fresh process only if at least one arm is eligible. To retain the draft's “everything rerun” schedule, both recipes may be recorded in process 2, but only arms eligible in process 1 may be advanced; a newly favourable process-2-only arm is exploratory. Process 2 independently passes all validity, LAW#3, control, locality and qualifier gates. Rank its unqualified scientific class as LEAD=2, PARTIAL=1, other=0. The replicated class is the lower of the two nonzero ranks: LEAD/LEAD gives LEAD; LEAD/PARTIAL, PARTIAL/LEAD and PARTIAL/PARTIAL give PARTIAL. Otherwise append NOT-REPLICATED to the process-1 provisional class and adopt nothing. Preserve both process-specific counts and classes. A process-2 LARGE-WRITE or UNDERFIT cannot replicate an eligible process-1 result.
>
> **Interpretations, first applicable category.** INVALID/HALT: instrument unvalidated, no mechanism reading. INVALID-CONTROLS: method fails a tested value class. LARGE-WRITE or TRADEOFF: non-advancement at the measured write-size/locality constraint. UNDERFIT: target-fit screen failed; no spreading conclusion. Unqualified replicated LEAD/PARTIAL: package-level lead only, as specified in items 7–8. An unqualified but unreplicated LEAD/PARTIAL: provisional observation, not adopted. For remaining NULLs use the disjoint target-screen table below; NULL never exhausts a method family.

| Arm and injection deficit `d = reference_hits - candidate_hits` | Exact NULL interpretation |
|---|---|
| I-2, `d >= 10` | NULL-TARGET-WEAKER: at least 10 fewer injected held-out hits; the tested target/intervention is weaker, so this NULL does not isolate spreading. |
| I-2, `6 <= d <= 9` | NULL; intermediate injection deficit, target-strength interpretation withheld. |
| I-2, `d <= 5` | This FE package did not advance recall despite no injection deficit above five; spreading in general is not ruled out. |
| I-1, `d >= 6` | NULL; at least six fewer injected hits for this target, without a causal claim about the objective. |
| I-1, `-5 <= d <= 5` | NULL; injection differences inside the declared non-interpreted band. |
| I-1, `d <= -6` | NULL; a target with at least six more injected hits did not advance the weight write. |

**Replacement boundary paragraph:**

> All locality endpoints pass at equality: L1 <=A+1/12; each fitted-frame fictional count <=A+1/6; described-as >=A-3; L3 >=29/30; generic perplexity <=A+0.5. The leak rate <=15% means at most 3 hits among 24; 4 fails. Relative reduction errors <=1e-4 pass. Existing G limits remain strict: equality at 0.05 or 3 fails. A=5,C=18 is NULL; A=9,C=19 is PARTIAL with clean locality; A=10,C=19 is NULL; A=18,C=27 is NULL, C=28 or 29 is PARTIAL, C=30 is LEAD. Injection deficits 5/6/9/10 take the separate branches above. None of these thresholds is changed after seeing candidate outcomes.

The count partition was checked by model-free arithmetic for all A=5..18, C=0..72 and both locality states (2,044 cases); the examples are deductions from the proposed predicates, not experiment results. These preserve the draft's count and locality endpoints (`docs/C10X_ENGINEPATH_PREREG.md:109–123`), with fitted-frame coverage corrected by item 15.

### 5. ADVISORY — advisor item 5: AGREE-WITH-CHANGE — correct residual meaning and every affected pointer

The draft corrects the reversed “3% lands” premise, but still overstates what its norm metric excludes (`docs/C10X_ENGINEPATH_PREREG.md:12,20`). The append-only correction defines a remaining-residual norm ratio and restricts its mechanistic reading (`CORPUS/44_C10L_COVGEOM_SPARSEBAND.md:43`). The later behavioural run reports remaining fractions 0.032650 canonical and 0.233728 held-out (`CORPUS/53_C10T_SECONDKEY.md:62`). These are neither recall rates nor a scalar coefficient saying exactly 97% of a target “lands.”

The advisor correctly repairs the step-6 row to line 28, but misses the header's appendix citation: step 6 is appendix line **55**, not 53, which is gate A (`results/research_pass_2026-10-06/recommended_sequence.md:28,53–55`; `results/c10x_enginepath_advisor_v1.md:108–116`). The broader incorrect rationale also remains at line 15 of that source, in addition to the step-6 row (`results/research_pass_2026-10-06/recommended_sequence.md:15,28`).

**Replacement for §0 premise 1 and H-X2-null's residual sentence:**

> `rho = ||z-cur_after|| / ||z-cur_before||` is a fraction of residual norm **remaining**. The offline reconstruction left approximately 0.028 canonical and 0.232 paraphrase residual (`CORPUS/44_C10L_COVGEOM_SPARSEBAND.md:25,43`); the later single-key behavioural run recorded 0.032650/0.233728 (`CORPUS/53_C10T_SECONDKEY.md:62`). Neither statistic measures the fraction of facts correctly recalled. **I-INFER:** these observations weaken a large keyed-position shortfall account in the measured configurations; they do not prove that residual size cannot affect greedy behaviour. FE may change target layer, layer allocation and collateral effects, which this package does not isolate.
>
> Source pointers: step 6 is `results/research_pass_2026-10-06/recommended_sequence.md:28,55`; the obsolete rationale survives at :15/:28 and `results/research_pass_2026-10-06/prereg_stubs.md:75`. The historical source is not rewritten by this preregistration.

### 6. ADVISORY — advisor item 6: AGREE — continuation already has a target-solve objective

The engine places every target ID and averages its log probability (`memit_dry_run/memit/memit/compute_z.py:60–65,141–150`). `compute_ks` instead reads rewrite-module inputs at `fact_token`, set to subject-last, and the harness uses those keys in its weight solve (`memit_dry_run/memit/memit/compute_ks.py:19–37`; `configs/hparams/qwen25_3b_memit_hparams.json:5`; `experiments/track_c/c10e_bandknob.py:196–211`). The advisor's denominator correction is exact (`CORPUS/45_C10L_MINT_TOKEN.md:24`; `results/c10x_enginepath_advisor_v1.md:118–128`).

**Replacement for §0 premise 2 and §2.5 prediction:**

> Every value token has an objective in `compute_z`; OverTone reweights that existing objective. The current weight solve directly constrains subject-last keys, without a separate value-position objective. Cite `memit_dry_run/memit/memit/compute_ks.py:19–37` and `experiments/track_c/c10e_bandknob.py:196–211` for the weight keys; `compute_z.py:68–73` describes the target-solve intervention index. A7 teacher-forced held-out position counts are 59/72, 66/72, 51/72, 19/72, 34/69 and 20/39 (`CORPUS/45_C10L_MINT_TOKEN.md:24`). Prediction: if objective reweighting changes continuation after the write, position-3-and-later teacher-forced counts may change relative to A. Record each numerator and its actual denominator; this diagnostic is not the binding free-generation metric.

### 7. ADVISORY — advisor item 7: AGREE-WITH-CHANGE — distinguish an objective package from an early-stop explanation

The package changes the token loss while retaining the total-loss stop, KL penalty and weight decay (`docs/C10X_ENGINEPATH_PREREG.md:51–59`; `memit_dry_run/memit/memit/compute_z.py:151–168`). That confounds attribution to token smoothing versus the changed optimization trajectory/stopping point. But the advisor's definite “uniformly earlier stop” and “near the point where y just leads at every position” are not established: the total includes other terms, and the branch tests the **mixture's** argmax, not simply the model's argmax (`results/c10x_enginepath_advisor_v1.md:132–137`; `docs/C10X_ENGINEPATH_PREREG.md:53,56`). Earlier stopping and lower fit are predictions, not facts about an unrun solver.

**Replacement for I-1's positive reading and fit expectation:**

> A replicated eligible gain advances the tested OverTone-inspired target package: dynamic detached token targets, filtering, clipping, retained KL/weight decay and the engine's total-loss stopping rule. It does not identify which component caused the gain. Lower fit or earlier stopping is an **I-INFER prediction**, tested by the recorded target probabilities, steps and stopping reasons; it is not assumed. Separation from ordinary CE with a comparable stopping/fit budget requires its own fixed control and pre-registration. No such extra recipe is included in the present compute estimate.

A “first step where all tokens are top-1” control would narrow the hypothesis but does not automatically match either fit, steps or write size; do not claim it fully separates the mechanisms (`results/c10x_enginepath_advisor_v1.md:138`; retention of multiple objective terms above).

### 8. ADVISORY — advisor item 8: AGREE-WITH-CHANGE — FE is a compound intervention; 97% after the band is not 97% at layer 4

I-2 changes the target-solve layer, downstream target construction, residual read layer and residual divisor (`docs/C10X_ENGINEPATH_PREREG.md:41–45`). It cannot attribute a gain uniquely to replay. However, the advisor infers almost the whole write is realised at layer 4 from a remaining ratio measured **after the five-layer band**, which does not establish single-layer realisation (`results/c10x_enginepath_advisor_v1.md:142`; `CORPUS/44_C10L_COVGEOM_SPARSEBAND.md:25,43`). The proposed shallow-only control also differs from the paper's named OneLayer baseline, which edits the **final** decisive layer (`results/infranodus_research_arc_2026-10-05/fulltext/ForwardReplay_2605.00358.md:53–55`).

**Replacement for I-2's positive reading, prediction and omitted-control note:**

> A replicated eligible gain advances this FE-inspired package: z solved at layer 4, canonical replayed targets, layer-local residuals and undivided updates under the unchanged projected-ridge harness solve. Replay, shallower target optimization and residual allocation are not separated. **I-INFER prediction:** the undivided first-layer residual may concentrate/enlarge the layer-4 write and may produce LARGE-WRITE; measure this rather than treating a band-end residual ratio as proof of single-layer realization. A `SHALLOW-ONLY-4` control using the same z_4 is omitted here; it is distinct from the FE paper's final-layer OneLayer comparator. Any causal attribution or extra control needs a separate pre-registration and budget.

### 9. ADVISORY — advisor item 9: AGREE-WITH-CHANGE — bound the tolerance itself, and define zero references

The draft's `max(10*floor,1e-4)` has no upper limit (`docs/C10X_ENGINEPATH_PREREG.md:63`). The advisor's proposed floor ceiling of 1e-4 still admits a tolerance of 1e-3 (`results/c10x_enginepath_advisor_v1.md:151–153`). The matched-shape floors reported so far are zero, not evidence for permitting that relaxation (`results/c10s_sharedz_logs/inertness.log:9,13`; `CORPUS/53_C10T_SECONDKEY.md:15`).

**Replacement for the reduction tolerance rule:**

> Measure the floor using the same inputs, batch/padding shape, context order, weights, cache, dtype and arithmetic as the quantity compared. For nonzero reference vector/tensor `a`, use `||a-b||_2 / ||a||_2`, with norms/subtraction on detached CPU fp32 copies; record max-absolute error. Set `tol=max(10*floor,1e-4)` but require `tol<=1e-4`, equivalently `floor<=1e-5`; otherwise HALT and diagnose the observation layer rather than silently widening acceptance. A zero reference is compared for exact equality; never produce a divide-by-zero NaN or let it fall through a comparison. Every finite check is explicit. Cross-batch distances and cross-process variation are diagnostics, not floors for these same-shape reduction gates. No tolerance is calibrated from a candidate result.

### 10. BLOCKING — advisor item 10: AGREE-WITH-CHANGE — match both sides' batches, not just the reference

The draft's replay is batch one, whereas the writer's canonical `cur` call is the 24-request padded batch (`docs/C10X_ENGINEPATH_PREREG.md:42–43,72`; `experiments/track_c/c10e_bandknob.py:197–201`; `memit_dry_run/memit/rome/repr_tools.py:135–147`). Merely changing the reference to 24, as the advisor proposes, leaves the replay side at one (`results/c10x_enginepath_advisor_v1.md:157–159`). That recreates the documented fp16 shape confound (`results/c10s_sharedz_halt_analysis_2026-10-06.md:19–29`).

**Replacement for §2.2 step 2 and X2-(iv):**

> Replay the 24 canonical prompts for each value-class arm as one ordered padded batch, matching the writer's canonical `cur` call exactly. Use the same token IDs, attention mask, padding side and subject-last index in each row. Overwrite row r at its own lookup index with that request's z_4 cast to the hidden dtype; capture cloned outputs at layers 5–8 in the same pass. Retain the unrounded z_4 as the layer-4 target. Hash row identities, token tensors and the layer-keyed target table.
>
> X2-(iv)(a) compares un-overwritten 24-row replay captures against the original engine reader on **those same 24 rows**, at every band layer, under the bounded reduction tolerance. X2-(iv)(b) overwrites with each row's own output captured from that exact batch and compares downstream outputs with the same un-overwritten batch. Single-request observations can be recorded separately but are never compared to 24-row outputs under a same-shape 1e-4 gate. Any later singleton diagnostic is checked against a singleton reference. Preserve this rule in X2-(vii).

### 11. BLOCKING — advisor item 11: AGREE-WITH-CHANGE — avoid invalid branches before they enter the gradient graph

The draft uses a full padded block and `tok_loss * mask`; its CE reduction gathers dummy label 0 outside scored positions (`docs/C10X_ENGINEPATH_PREREG.md:52–55`; `memit_dry_run/memit/memit/compute_z.py:141–149`). The advisor correctly identifies the mask problem (`results/c10x_enginepath_advisor_v1.md:163–165`). **I-INFER:** a final selection cannot certify that an invalid intermediate or its gradient was never evaluated; masking must start before filtering/KL arithmetic. Another reachable degeneracy follows directly from the specified strict filter: all-equal logits give std=0 and keep no entries (`docs/C10X_ENGINEPATH_PREREG.md:53`).

**Replacement addition to §2.3:**

> Construct the OverTone target and KL only for scored rewriting positions, excluding padding and the separately handled KL-prompt row. Check finite logits and nonempty filter support before softmax; empty support HALTs with the offending vector. Define zero-probability entropy contributions as zero without evaluating log(0) on those entries. Mixture-skipped positions use the original CE value with exactly zero extra term; do not evaluate the unused mixture-loss expression for them. Scatter finite scored losses back into an explicitly zero padded tensor before the mean. For `lam=1,eps=0`, use the literal engine CE arithmetic **inside the copied solver**, without delegating the entire solve to the engine or altering its graph/reduction order. Active settings remain covered by the independent value/gradient checks in items 14/16. Test padded positions, empty support, one-hot targets and mix/skip branches with model-free controls.

### 12. ADVISORY — advisor item 12: AGREE — document G's actual dispatch guard and reset counters

G runs inside `run_recipe` while the wrapper's candidate state can remain set; the protection is the live `_LAW5_DEFAULT_CTX` flag (`experiments/track_c/c10e_bandknob.py:430–435,463`; `docs/C10X_ENGINEPATH_PREREG.md:44,65`). Standalone override comparisons also increment the global counter (`experiments/track_c/c10e_bandknob.py:186–188`).

**Replacement for G and counters:**

> `dispatch` reads `H._LAW5_DEFAULT_CTX` at call time and delegates to the saved original `my_edit` throughout G; do not copy the boolean at import. G does not require unset candidate state, but it must reach no candidate seam. Reset `H.Z_OVERRIDE_HITS` and `FE_CALLS` immediately before each `H.run_recipe`; read them immediately afterwards. Required exact pairs are A=(0,0), I-2=(0,3), I-1=(3,0). Maintain separate counters for standalone X-checks. A nonzero candidate-seam call during G, a silent missing-target fallback or a final recipe counter mismatch HALTs.

### 13. ADVISORY — advisor item 13: AGREE-WITH-CHANGE — plausible hardware fit and budget, not a measured upper bound

Machine suitability is supported by the program's M3 Pro/48 GB/no-CUDA statement and the existing fp16 loader (`CLAUDE.md:3`; `experiments/track_c/c10e_bandknob.py:48`). The harness's dense solve and projector use CPU fp32; the engine moves its float64 operands to CPU before arithmetic (`experiments/track_c/c10e_bandknob.py:166–178,205–217`; `memit_dry_run/memit/memit/memit_main.py:191–203`). No proposed primitive inherently requires CUDA. **Live hardware confirmation and new-path peak memory: UNVERIFIABLE in this review**; the read-only sysctl probe was denied, and no torch/MPS job was run.

The advisor's timing arithmetic is reasonable but does not establish a seven-hour maximum (`results/c10x_enginepath_advisor_v1.md:173–192`). Exact measured differences: 2031-466=1565 s, 1826-174=1652 s and 1877-132=1745 s for the three-arm recipes after removing their logged stacked extras, or 26.1/27.5/29.1 minutes (`results/c10q_stacked/logs_run.log:41,52,71,82,101,112`). Three ordinary solves took 21 s for one inertness request; extrapolating 7 s to all value classes and the new active OverTone path is an estimate, not a measured mean (`results/c10s_sharedz_logs/inertness.log:9`). A behaviour run of approximately 23 minutes is recorded for the mint queue and is not the cost of this whole process (`docs/INTEGRATED_QUEUE_2026-10-07.md:18`).

**Replacement for §2.7 Compute:**

> Planning evidence: a three-arm recipe is approximately 26–30 minutes after removal of measured stacked extras; retain 34 minutes as a conservative planning allowance, not a new measurement. A separate behaviour run is about 23 minutes, not a complete C10X pass. At the one-request measured solve rate, 216 target solves cost 25.2 minutes and 72 reduction solves cost 8.4 minutes; class-dependent stopping, the active OverTone vocabulary operations and instrumentation are unmeasured. The cell budget below is a planning estimate, not a hard upper bound. All cells, including projectors, restoration/hashing, independent audits and injection evaluation, are timed separately. No optional mechanism-control recipe is included. A LAW#3 miss ends after recipe A, before candidate spend. Process 2 incurs a fresh full gate sequence and is launched only under the eligibility predicate in item 4.

| Cell | Planning allowance | Evidence status |
|---|---:|---|
| A, I-2 and I-1 recipes together | 78–102 min | Extrapolated from the measured 26–29 min recipes; new recipes unrun. |
| 216 target solves plus replay | 25–40 min | 25.2 min solve extrapolation; original draft allowance `docs/C10X_ENGINEPATH_PREREG.md:99`; active overhead unmeasured. |
| Reduction/identity/null gates and other inertness | 35–50 min | UNVERIFIABLE planning allowance including the added gates; 8.4 min reduction-solve component derived above. |
| Three injection screens | 20–25 min | Draft estimate `docs/C10X_ENGINEPATH_PREREG.md:99`; independently measured C10X cost UNVERIFIABLE. |
| **Subtotal** | **158–217 min (2.6–3.6 h)** | Excludes unmeasured full-logit audit/hashing overhead; not a deadline guarantee. |

**Replacement budget conclusion:**

> 3–3.5 hours per process is a plausible target, not validated wall time. “Worst case seven hours” is withdrawn: the added gates, full-logit audit and active solver overhead have not been timed. Runtime or resource exhaustion gives HALTED/incomplete, never a scientific NULL. Keep model forwards on MPS in fp16, detached objective work in explicit fp32, and any float64 analysis on CPU only; serialize model jobs. Validate actual peak unified memory before accepting the full estimate.

For scale of allocations only (**I-INFER calculation**): the pinned model has intermediate width 11008, so one square fp32 projector/cache is 462.25 MiB and five of each require approximately 4.51 GiB before model weights and solve temporaries (`hf_cache/hub/models--Qwen--Qwen2.5-3B/snapshots/3aab1f1954e9cc14eb9509a215f9e5ca08227a9b/config.json:11`; `experiments/track_c/c10e_bandknob.py:175,428,474`). This is compatible with a plausible 48 GB plan but does not prove the new solver's memory peak. Release cell-local projectors/audit buffers rather than retaining repeated copies.

## Additional defects the advisor missed

### 14. BLOCKING — top-64 logits cannot reproduce the declared OverTone calculation

X1-(iii) says top-64 logits suffice (`docs/C10X_ENGINEPATH_PREREG.md:68`). Its filter depends on the standard deviation over the whole vocabulary, and the filtered softmax/forward KL depend on all retained logits (`docs/C10X_ENGINEPATH_PREREG.md:53–55`). **I-INFER mathematical counterexample:** two vectors can have identical top 64 and different remaining logits, hence different standard deviations, keep sets, normalization, mixture decisions and KL. The model vocabulary is 151936, not 64 (`hf_cache/hub/models--Qwen--Qwen2.5-3B/snapshots/3aab1f1954e9cc14eb9509a215f9e5ca08227a9b/config.json:27`). The advertised independent acceptance check is therefore not computable from its record.

**Replacement for X1-(iii):**

> For both diagnostic requests at step zero and their final evaluated step, save detached **full-vocabulary, unrounded** pre-softmax logits for every scored rewriting position, the actual engine log-probabilities/CE values, target IDs, position/row maps, dtype and mask. Use a lossless CPU binary representation with a hash; top-64 is display-only. The independent reader recomputes filtering, detached target probabilities, mix decisions and token loss using these full inputs. Explicitly freeze standard-deviation correction=1, the strict keep inequality and first-index argmax tie rule as implementation choices. Follow the declared intermediate casts/reduction order rather than comparing an ideal fp32 KL directly with a rounded fp16 `ce+extra`. For value parity, compare the independently reproduced stored-arithmetic result at <=1e-4 relative error, with denominator `max(abs(reference_loss),eps,1e-12)`, and record absolute error. Also report the ideal fp32 KL as a diagnostic, never as an interchangeable acceptance reference. Add a model-free pair of vectors sharing top 64 but differing in the tail; the independent audit must distinguish their filter/loss results.

### 15. BLOCKING — canonical-only bystander probes violate the declared fitted-frame contract

The draft says neither arm fits another frame and therefore probes only the canonical frame (`docs/C10X_ENGINEPATH_PREREG.md:86`). In fact both target solves use the engine context templates, and `compute_z` constructs a rewriting prompt for **every** template (`docs/C10X_ENGINEPATH_PREREG.md:41,58–59`; `memit_dry_run/memit/memit/compute_z.py:46–50`). The context list includes identity plus five generated wrappers (`memit_dry_run/memit/memit/memit_main.py:308–319`). The shared contract requires a separately counted bystander gate in every fitted frame (`results/research_pass_2026-10-06/prereg_stubs.md:10`). The existing probe helper hardcodes canonical, so merely reusing it does not satisfy this obligation (`experiments/track_c/c10p_twopass_arms.py:35–42`).

**Replacement for §2.6's frame coverage and §3 locality:**

> Probe the six never-edited `FRAME_SUBJECTS` in **every realized rewriting frame** `context.format(CANON)` from the exact same-process context list, including canonical identity. Freeze/record the frame texts and their hash before candidate data. For each recipe's A7 arm and each frame separately, count top-1 membership in the frozen A7 first-token set using the existing frame-probe semantics; require candidate count <=same-process A count+1 of six in **each** frame. Preserve pristine counts and row IDs beside these counts; do not pool frames to hide one failed frame. Retain the canonical gate as one member of this family. The `is a` KL prompt remains explicitly objective-anchored and diagnostic, not a new held-out target-training frame. Use only existing context frames and never add a held-out test frame to the solve.

### 16. BLOCKING — the active-objective audit checks values but not gradients or exact boundaries

Reduction at lam=1 tests the CE configuration, and X1-(iii) checks recorded token-loss values under the active configuration; neither explicitly verifies the active loss's gradient (`docs/C10X_ENGINEPATH_PREREG.md:67–68`). The active target is intended to be detached and the clip changes which tokens drive optimization (`docs/C10X_ENGINEPATH_PREREG.md:53–56`). **I-INFER:** a solver can emit the correct scalar while differentiating through the target distribution or through the wrong clipped branch. That would pass the stated scalar audit while changing the actual science intervention.

**Replacement addition to the model-free X1 selftest and §2.3 boundary definition:**

> With fixed synthetic logits and a detached `pi_tar`, the independent analytic logit-gradient is `softmax(s)-pi_tar` for KL>eps and zero for KL<eps, scaled by the declared token/prompt means. The skip branch gives the original CE gradient. Explicitly choose zero gradient at KL=eps by selecting the constant clipped branch at equality; record this boundary convention as part of the transcription. Test these gradients in CPU fp32 at max-absolute error <=1e-6, away from filter/mix ties, and test the equality branch exactly. Verify that no gradient reaches `pi_tar` and none originates at padding/KL-prompt positions through the token objective. Synthetic controls include mix, skip, clipping, uniform-logit empty support, exact filter equality, argmax ties and different masked/variable-length rows. Keep the existing 72-request returned-z/step-count reduction test; it is not replaced by these synthetic controls.

### 17. ADVISORY — the FE prior omits the paper's AlphaEdit extension; set/add equivalence is numerically conditional

H-X2-null presents the published support as MEMIT lambda-C versus this projected solve (`docs/C10X_ENGINEPATH_PREREG.md:20,45`). The saved paper text also reports extensions to AlphaEdit, RECT and PRUNE (`results/infranodus_research_arc_2026-10-05/fulltext/ForwardReplay_2605.00358.md:56,100`). That does not validate this configuration, but it prevents treating projected-method transfer as entirely absent from the paper. Separately, the draft's “by construction” identity between the solve's additive delta and the bare-prompt absolute overwrite overlooks the different teacher-forced/padded solve batch (`docs/C10X_ENGINEPATH_PREREG.md:42`; `memit_dry_run/memit/memit/compute_z.py:46–57,95–99,180`). Shape sensitivity is observed, not hypothetical (`results/c10s_sharedz_halt_analysis_2026-10-06.md:19–29`).

**Replacement for H-X2-null's literature clause and §2.2 overwrite justification:**

> FE reports benchmark experiments on LLaMA3-8B-Instruct/GPT-J/GPT2-XL, jointly edited benchmark items, and an AlphaEdit extension (`results/infranodus_research_arc_2026-10-05/fulltext/ForwardReplay_2605.00358.md:56,59–61,100`). Its transfer to this Qwen2.5-3B, 24-fact coined-value configuration and these exact projector/cache conventions remains unvalidated. The canonical absolute overwrite is the chosen FE transcription. Equivalence to the target solve's additive intervention is mathematical only for the same underlying pre-intervention activation; equality of the different fp16 batches is not assumed. Record the solve's `target_init` versus the canonical replay's initial activation and their shape/context identity as a diagnostic. Do not widen a reduction tolerance to hide that difference.

### 18. ADVISORY — hashes must bind comparable runs, and design approval is not execution approval

The draft requires hash presence and a fresh process, but does not state which identities must match when the reader combines records (`docs/C10X_ENGINEPATH_PREREG.md:97,103,109,125`). The baseline loader does pin model/revision (`experiments/track_c/c10e_bandknob.py:25–26,45–48`); make that evidence part of the manifest instead of relying on ambient import state. The queue also authorizes a model-free build while retaining later experiment ordering (`docs/INTEGRATED_QUEUE_2026-10-07.md:19–22`; `EXPERIMENT_RUNBOOK.md:342–343`). A favourable design review cannot by itself satisfy that dependency.

**Replacement addition to §2.8, replication and §6:**

> Each run carries a distinct run/process identity, timestamps, model ID/revision, tokenizer artifact hashes, software/device/dtype identity, pristine-weight hashes, frozen preregistration hash, ordered stimuli, source-file hashes and the full target/settings manifest. Reader acceptance requires the same scientific configuration/source/weights/stimuli and unchanged preregistration across processes, with only the declared sampled context list and resulting targets permitted to differ. Same-file or same-process reuse is not replication. Refuse existing output artifacts; never overwrite earlier results or manifests. Verify scientific source/input hashes at start and end. Freeze/build review does not launch step 6 or bypass the preceding ceiling/queue gates. Record the actual reviewer model/effort, or UNVERIFIABLE when they cannot be authenticated, rather than copying an expected designation.

## Evidence and verification limits

Cheapest overturning checks, in order: reproduce A and stop immediately on its envelope miss; run the nonzero singleton FE reduction plus the same-batch multi-layer null check; run the full-vocabulary/gradient controls for the new objective; then inspect the already-planned injection screens before candidate recipes. A weak layer-4 injection or failed fit would limit the interpretation of an eventual FE NULL, not prove spreading is exhausted (`docs/C10X_ENGINEPATH_PREREG.md:78–79,141`). Candidate explanations kept distinct are weaker/lower-layer targets, changed residual allocation or stopping, collateral change in fitted frames, and an instrument/indexing defect; the proposed gates and package-scoped readings separate invalid measurement from tested non-advancement.

No model, tokenizer, torch or GPU code was imported or executed; no downloads, git mutations, implementation edits or canonical close-out writes were performed. Only the requested review file was explicitly written. Direct hardware verification was denied, so machine claims above remain attributed to the brief/repository. Graft was called with refresh/seeding disabled; `.gitignore` retained its initial hash, but `graft/.cache/ask-index.json` changed hash during the shared-workspace review. Attribution of that cache change is **UNVERIFIABLE**; it was not restored or treated as scientific evidence. Subsequent inspection used direct source reads.

Reviewed immutable inputs, checked again before writing:

- `docs/C10X_ENGINEPATH_PREREG.md`: SHA-256 `5badd9c5339635f1ce7167418a408efac9a4fc32424ccc9288eafe8f514338a4`.
- `results/c10x_enginepath_advisor_v1.md`: SHA-256 `3f0622116c96d36a99d4929a4340f16b3533598a04fe7bd2ed361af7b66a36b5`.
- `memit_dry_run/memit/memit/memit_main.py`: SHA-256 `d941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65` (static hash check only, not a dispatched runtime gate).

**FIX-FIRST remains the design verdict.** The report is complete; implementation and empirical gates are unrun.
