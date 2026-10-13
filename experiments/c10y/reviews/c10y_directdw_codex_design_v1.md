# D-C10y-directdw v1 design review — gpt-6.1-sol, effort max

Actual reviewer: **gpt-6.1-sol; reasoning effort max**, recorded in `/Users/robertrhu/.codex/sessions/2026/10/07/rollout-2026-10-07T06-39-31-01a11660-487b-77d2-8ee4-a3c9f4a4ab88.jsonl:8`. This is a GPT-family review of the Claude-family draft and advisor report, not the preregistration's named GPT-6-Astra/high review (`docs/C10Y_DIRECTDW_PREREG.md:202,206`). Record the actual identity when folding this review. Date: 2026-10-07. Method: `tools/advisor_review_prompt.md:1–15`.

**Verdict: FIX-FIRST.**

**Single most important fix:** replace §2.7's WRITE-QUALIFIES argument with **MEASUREMENT-ONLY** under the existing operator ruling. Training the weight-update factors per commit is a training loop; patch-only inputs do not exempt it. Separately, no candidate optimisation, including the discarded timing smoke, may precede LAW#3 baseline reproduction (`EXPERIMENT_RUNBOOK.md:330,343`; `docs/C10Y_DIRECTDW_PREREG.md:88,94–99,147`).

This review concerns C10 in the Write Engine cell and the §8.9 behavioural obligation, not whole-system readiness (`docs/SPEC_E2E_GROUND_TRUTH.md:14,22–30,64–65`). The proposed replacements below are design choices to freeze before execution, not empirical findings. Runtime, convergence, peak memory and new-path inertness are **UNVERIFIABLE until measured**; the draft itself records that nothing has run (`docs/C10Y_DIRECTDW_PREREG.md:3,143–147`). No model, tokenizer, torch or accelerator job was run for this review.

## Advisor reconciliation

The numbered items 1–14 correspond to `results/c10y_directdw_advisor_v1.md:29–157`. Items 15 onward are additional defects.

### 1. BLOCKING — AGREE-WITH-CHANGE: demotion remains; the oracle is not a mathematical bound

The omission is real: the draft lists standing rulings without D-C10r-rulings-4, while that ruling demotes steps 6–7 and requires reconsideration after the earlier results (`docs/C10Y_DIRECTDW_PREREG.md:3,5`; `EXPERIMENT_RUNBOOK.md:331`). Model-free building is authorised, and the current program ruling retains demotion and provisionally classifies step 7 as measurement (`EXPERIMENT_RUNBOOK.md:342–343`). The overnight standing approval also exists; a fresh permission request is not automatically required to make a program recommendation (`EXPERIMENT_RUNBOOK.md:338,342`).

I disagree with using oracle ≤18 as a binding kill. The oracle and this writer have different objectives and parameter constraints; an unsuccessful finite training configuration is not an upper bound on another configuration. The advisor itself calls this a prior (`results/c10y_directdw_advisor_v1.md:9`).

**Replacement for the run-scheduling text in §0 and §6:**

> Building is authorised model-free under D-C10r-rulings-9 (3). Execution remains GATED on the recorded reconsideration required by D-C10r-rulings-4 (3), after steps 3, 4 and the step-5 oracle have been read. That reconsideration may be made under the existing D-C10r-rulings-8/9 standing approval and must be recorded before dispatch. Step 7 is MEASUREMENT-ONLY under D-C10u-Aenv (2). A low oracle result informs the spending recommendation; it is not a proved capacity bound and does not mechanically invalidate this different writer. No mandatory two-process block is authorised by the queue's build instruction. (`EXPERIMENT_RUNBOOK.md:331,338,342–343`; `docs/INTEGRATED_QUEUE_2026-10-07.md:18–22`.)

### 2. BLOCKING — AGREE-WITH-CHANGE: MEASUREMENT-ONLY; distinguish the operator ruling from the spec's narrower wording

**Answer to the specific question: MEASUREMENT-ONLY.** `compute_z` creates a trainable activation vector, freezes the model, and optimises that vector (`memit_dry_run/memit/memit/compute_z.py:83,98–105,170–172`). The accepted harness writes weights through a linear solve and an addition (`experiments/track_c/c10e_bandknob.py:209–217`). C10Y instead optimises A, which determines the effective deployed weights through AB, using Adam and an LM loss (`docs/C10Y_DIRECTDW_PREREG.md:43,51,58–73`). That is per-commit parameter training even if the base parameter objects remain frozen and no external dataset is used. The exclusion says training set **or** training loop (`results/research_pass_2026-10-06/recommended_sequence.md:13`); the operator ruling and the current provisional ruling resolve the program's interpretation (`EXPERIMENT_RUNBOOK.md:330,343`).

The spec expressly excludes **full fine-tuning**, not every use of gradients. Do not infer the broader prohibition from that sentence alone (`research_and_specs/llm-as-database-v1_2-integrated-spec.md:309–317`). The binding broader restriction here is the operator's ruling. Compaction requires a full recompile over active patches, not merely replaying this N=24 example (`research_and_specs/llm-as-database-v1_2-integrated-spec.md:413,837–855`). A small-batch regeneration test does not validate compaction cost or cleanliness.

**Replacement for §2.7's heading, argument and §6 decision 1:**

> **Classification: MEASUREMENT-ONLY, not a write route.** This experiment trains the effective weight-update factors A by gradient steps on the patch's own prompts. Frozen base parameter objects, a low-rank overlay and dataset-free inputs do not remove that training loop. This differs from the accepted engine's activation-vector optimisation on frozen weights followed by a closed-form weight solve. Under D-C10r-rulings-3 (2) and D-C10u-Aenv (2), any positive result is diagnostic evidence about this objective and parameterisation only. It neither qualifies the deployment route nor relaxes the operator's criterion. Route status would require an explicit superseding scope ruling; wall-clock or regeneration success alone does not supply one. The spec's exclusion of full fine-tuning is cited narrowly, not as a prohibition on the existing compute_z activation solve. (`EXPERIMENT_RUNBOOK.md:330,343`; `memit_dry_run/memit/memit/compute_z.py:83,104–105,170–172`; `experiments/track_c/c10e_bandknob.py:209–217`; spec §8.2, `research_and_specs/llm-as-database-v1_2-integrated-spec.md:313`.)

> A replicated positive measurement may motivate a separately authorised method experiment. It does not automatically become a candidate engine variant, close C10, justify a model-axis ceiling claim, or amend the spec.

### 3. BLOCKING — AGREE-WITH-CHANGE: a concrete two-hour screen, not an unconditional 5–11-hour block

A staged A7 screen is appropriate. However, the advisor's proposed stage 1 cannot issue a fully valid NULL without the candidate A1/A2 controls, and it does not test H-Y2 when B-z is skipped (`results/c10y_directdw_advisor_v1.md:10,61`; `docs/C10Y_DIRECTDW_PREREG.md:20–21,162`). An UNDERFIT kill saves spending but can discard a configuration that would benefit from a different budget; it cannot falsify the objective family.

The measured anchors support **approximately 33–34 minutes per historical three-arm pass**, not 10-minute substitutions for every evaluation/control. CORPUS/50 records three passes in approximately 99 minutes; the research inventory derives approximately 33 minutes from it (`CORPUS/50_C10Q_STACKED_SOLVE.md:3,6`; `results/research_pass_2026-10-06/hypotheses.md:8`). The C10P chain is 69 minutes 32 seconds for three passes, approximately 23.2 minutes per pass (`results/c10p_twopass/logs_c10p_chain.log:1–6`). The queue separately records approximately 23 minutes per behaviour run (`docs/INTEGRATED_QUEUE_2026-10-07.md:18`). These are workload anchors, not measurements of C10Y's backward pass.

At the draft's assumed 17–50 seconds/step, one 100-step A7 optimisation takes 28–83 minutes. Adding a 34-minute baseline, even 25 minutes of proof/setup work and a conservative 23-minute final-readout reservation gives **110–165 minutes**. That arithmetic is I-INFER, not a measured stage-1 duration (`docs/C10Y_DIRECTDW_PREREG.md:145–147`). The upper case is not two hours; capture identities and repeated SVDs can add further cost (`experiments/track_c/c10e_bandknob.py:166–175,209–211,458–474`).

**Replacement for §2.6 item 5, §2.11, D-11 and §6 budget decision:**

> **Stage 1: single-process A7 spending screen; maximum 120 minutes elapsed from process start, including loading, target solves, projector construction, all proofs, timing smoke, optimisation, merge and readout.** First run untouched recipe A on A1/A2/A7 and pass LAW#3. Then prove the new e2e path inert on A7, including the executed-loop identity and deployment checks. Only after those gates run the three-step timing smoke; discard its state and restore the pristine band. Time all expensive stages with MPS synchronisation. Preserve T_max=100 and the frozen optimiser settings. Before beginning the substantive write, and at step boundaries, require that measured elapsed time plus the projected remaining work plus a 23-minute readout reservation fits 120 minutes. If not, stop HALTED-BUDGET; do not silently reduce T_max, change micro-batching, or issue NULL. The 23 minutes is a conservative budget reservation, not a measured evaluation-only cost; if readout cannot complete inside the budget, report INCOMPLETE-BUDGET. No partially scored result earns a scientific label.

> Run **B-e2e on A7 only**. With a=recipe A's A7 count and n=B-e2e's count, the exact screen threshold is **n ≥ max(19, a+10)**, together with FIT-E2E, the applicable numerical/deployment checks, G1–G5, the per-training-frame G2 checks and summed actual-write ratio ≤1.5. A complete, fit screen below the count threshold is SCREEN-NULL. A fit screen with a sized gain but a locality/size miss is SCREEN-NOT-ADVANCED, with the observed reason. A failed fit is SCREEN-UNDERFIT. A failed instrument check is INVALID/HALTED. Missing candidate A1/A2 or replication remains explicitly NOT-RUN; SCREEN-PASS is provisional and non-binding. H-Y2 is NOT-TESTED if B-z is not run; never conclude H-Y0, 'neither objective works', from this screen.

> **Stage 2, conditional:** only a SCREEN-PASS buys B-e2e A1/A2, B-z with its own preceding inertness/fit checks, and the required size controls. Run the same positive configuration without retuning. Only a valid, fit, clean positive surviving attribution earns a request to spend on stage 3. **Stage 3:** a fresh-process regeneration from the same declared inputs, including its own baseline gate before candidates, only for that survivor. A second process is not mandatory after a screen kill. Stages 2–3 require a separate measured cost forecast and recorded spending decision; the draft's total 5–11 hours remains UNVERIFIABLE, not an approved upper bound.

A7-only optimisation is the cheapest direct overturning test of H-Y1 here. Its diagnostic kill closes this screened configuration/spending decision, not DOW-KE, H-Y2, model capacity or C10.

### 4. BLOCKING — AGREE-WITH-CHANGE: fit must be tested regardless of the stopping reason

The advisor correctly distinguishes inadequate optimisation from a negative behavioural result. Its proposed rule only checks fit when the cap is hit, so the averaged loss can stop early while an individual request/frame remains unfit. That exact type of averaged-stop failure already appears in the solve-feasibility record (`results/c10y_directdw_advisor_v1.md:77`; `EXPERIMENT_RUNBOOK.md:344`). Also, mean probability over six frames can hide one bad frame; the engine's diagnostic is exp of mean token log-probability, not full-sequence probability (`memit_dry_run/memit/memit/compute_z.py:149–162`).

**Replacement fit block, before behavioural classification:**

> Compute final **merged-model** f_ij=exp(−mean target-token NLL) for each of 24 requests i and all six rewriting frames j, and record the entire 24×6 matrix. This is a geometric mean of teacher-forced token probabilities, not sequence probability. **FIT-E2E** means min_ij f_ij ≥0.90 and canon_full_n ≥20/24. Equality passes. Test it at every termination, including threshold stops. Otherwise base fit status is UNDERFIT, regardless of held-out count; report the held-out count and any sized gain alongside it, but do not issue a clean LEAD/PARTIAL or a conclusive NULL. State the stop reason separately; no budget increase occurs within this preregistration.

> **FIT-Z** means merged L_z ≤1e−3 and max_ij r_ij ≤0.05, where r_ij=||h_ij−(h0_ij+delta_i)||/||delta_i||. Equality passes. The optimiser's stricter mean stopping threshold 1e−4 remains unchanged, but cannot excuse a failed maximum-entry fit check. A zero denominator must be handled explicitly before optimisation: a zero target delta with zero residual contributes zero; a nonzero residual with zero target delta is INVALID-ANCHOR-NORMALISATION. An unfit B-z is not usable to exclude anchor closure.

These are newly proposed diagnostic fit thresholds, not inherited empirical calibration. Freeze them before the screen; retain counts even on UNDERFIT.

### 5. BLOCKING — AGREE-WITH-CHANGE: mutually exclusive labels and an explicit mixed-process result

The LARGE-WRITE hole and ambiguous replication rules are real (`docs/C10Y_DIRECTDW_PREREG.md:177–192`). The advisor's total ordering NULL<TRADEOFF<PARTIAL<LEAD introduces an unnecessary inference: a clean low-count process and a damaged high-count process need not form one ordered scientific result (`results/c10y_directdw_advisor_v1.md:87`). Preserve both results and say when the label did not replicate.

**Replacement for §3's decision order and labels:**

> Decision order: completion of required records → instrument/validity gates → fit → per-process count and locality label → write/deployment qualifiers → cross-process comparison → attribution. Missing planned controls give INCOMPLETE, not NULL and not an assumed pass. Failed validity gives INVALID (named halt gates stop dispatch); fit failure gives UNDERFIT. Neither is a negative mechanism result. A stage-1 record is a SCREEN result under §2.6, not a complete scientific verdict.

> For a complete valid recipe meeting its appropriate fit rule (FIT-Z for B-z; FIT-E2E for B-e2e and size controls) in one process, let a be its same-process A7 baseline and n its merged A7 held-out count. Define sized := n>18 AND n−a≥10. Exactly one base label applies: **LEAD** iff sized AND n≥30 AND G1–G5 pass; **PARTIAL** iff sized AND n<30 AND G1–G5 pass; **TRADEOFF** iff sized AND any G1–G5 fails; **NULL** otherwise. G6 is reported, not silently treated as a passed locality gate. Qualifiers never change the base label: ratio>1.5 adds LARGE-WRITE to every applicable label; reproduction failure adds NOT-REPRODUCIBLE; failed attribution blocks H-Y1 credit. Positive-looking labels with blocking qualifiers do not advance.

> In two completed processes, identical base labels produce that base label; different base labels produce **MIXED-NOT-REPLICATED**, storing both per-process labels/counts. Use the union of blocking qualifiers. Any R1–R3 failure adds NOT-REPRODUCIBLE. A positive is replicated only if its base label and all required validity, fit, locality, size and attribution conditions hold in both processes. One completed process is SINGLE-PROCESS and non-binding. A halted/incomplete second process remains HALTED/INCOMPLETE, never a fabricated NULL.

**Replacement truth table** (proposed deterministic cases; assume complete controls/FIT and R1–R3 pass unless specified, a=12 and B-z=13):

| Observation | Reading |
|---|---|
| n=33/33, clean, ratio 1.2, valid clean NM=26 | LEAD; size control is positive (26−12=14) |
| n=31/32, clean, ratio 1.8 | LEAD-LARGE-WRITE; no advancement |
| n=25/24, described_as −4 | TRADEOFF |
| n=24/25, clean, ratio 1.3, NM=17 | PARTIAL-SIZE-NOT-EXCLUDED |
| B-z=24/24, n=27/27, both fit/valid | PARTIAL-ANCHOR-NOT-EXCLUDED; see item 18 |
| n=18/18 | NULL regardless of baseline-relative gain |
| n=30/22 | MIXED-NOT-REPLICATED-NOT-REPRODUCIBLE; per-process LEAD/PARTIAL; difference 8>5 |
| a=18, n=27 / n=28, clean | NULL / PARTIAL (gain 9 / 10) |
| a=5, n=19, clean | PARTIAL; NM=18 would still not exclude size |
| p1=LEAD, p2=TRADEOFF or UNDERFIT | MIXED-NOT-REPLICATED, with the actual two statuses |
| Any required metric non-finite, or A1=67 | INVALID; no positive or negative mechanism label |

Freeze reader cases for both sides of every boundary: n=18/19/29/30; gain=9/10; A1/A2=67/68; write ratio=1.0 and 1.5 (equality passes those limits); G1/G2 at A+1; G3 at A−3; G4=28/29; G5 at A+0.5; R2 difference=5/6; R3 disagreement=d_A+3/+4. Compare unrounded finite metrics, not formatted strings (`docs/C10Y_DIRECTDW_PREREG.md:161–190`; `experiments/track_c/c10e_bandknob.py:395–399`).

### 6. BLOCKING — AGREE-WITH-CHANGE: execute the loop at lr=0 and prove restoration

The standing LAW#5 check delegates the B modes to the original implementation; it cannot certify the new optimiser (`docs/C10Y_DIRECTDW_PREREG.md:87,106`; `experiments/track_c/c10e_bandknob.py:430–435`). T=0 alone does not prove the loop. The advisor's T=3 proposal also needs an explicit override of early stopping, otherwise the loop can still be skipped (`docs/C10Y_DIRECTDW_PREREG.md:64,108`; `results/c10y_directdw_advisor_v1.md:97`).

**Replacement additions to §2.8 and V3:**

> Standing run_law5 certifies original engine/harness parity only. New-path LAW#5 consists of the capture reduction, T=0 identity and **exactly three forced iterations at lr=0**, with early stopping disabled for this check. Run hooks, routing, four-way accumulation, loss scaling/unscaling, Adam.step, cleanup and merge. Both B modes must reproduce the original reference's merged weights within the frozen reduction tolerance and identical canon_full_n/para_full_n/para_first_n. Check each mode before trusting that mode's substantive output; stage 1 checks e2e/A7, later stages check their additional modes/arms before use. apply_stored must separately reproduce a stored reference at scale 1 before any NM result is trusted.

> Snapshot hook registrations before the writer; afterwards require exactly the original registrations and no writer-owned hook handles. If the initial registries are empty, final forward/pre-hook registries must be empty. Confirm the pristine band, optimiser/global wrapper state and override counters are restored between checks/arms. A failed restoration or reduction is HALTED/INVALID, not TRADEOFF. Do not erase unknown pre-existing hooks to make the assertion pass.

### 7. ADVISORY — AGREE-WITH-CHANGE: distinguish offline, in-harness and unavailable paper numbers

The draft correctly reverses the 3% premise, but overstates comparability and says the in-harness measurement remains owed (`docs/C10Y_DIRECTDW_PREREG.md:13,119`). CORPUS/44's 0.028/0.232 is an offline reconstruction, with the paraphrase proxy explicitly uninformative behaviourally; CORPUS/53 later records 0.032650/0.233728 in-harness (`CORPUS/44_C10L_COVGEOM_SPARSEBAND.md:25,43`; `CORPUS/53_C10T_SECONDKEY.md:62`). The local paper extract supplies experiment/ablation text but no body for the closure-gap analysis; its approximately 0.33 and exact §5 quotations are **UNVERIFIABLE from the retained source**, as the advisor also reports (`results/infranodus_research_arc_2026-10-05/fulltext/DOWKE_2608.16932.md:5–33,396–403`; `results/c10y_directdw_advisor_v1.md:25`).

**Replacement in §0 and §2.9:**

> ρ is a remaining-residual norm ratio, not the percentage of facts installed. Offline reconstruction reported ρ_c≈0.028 and ρ_p≈0.232, with a behaviourally uninformative paraphrase proxy (CORPUS/44:25,43). A subsequent single-key in-harness reference reported 0.032650/0.233728 (CORPUS/53:62). The paper's approximately 0.33 and exact method quotations remain UNVERIFIABLE until their source/version is retained. They do not set a threshold or justify a quantitative cross-model comparison. This run records its own merged-model residuals, comparable in scope to CORPUS/53; it is not fulfilling an as-yet-unmeasured obligation.

### 8. ADVISORY — AGREE: explicitly withdraw the later-token premise too

The draft already describes all-token NLL, but does not explicitly name the inherited error (`docs/C10Y_DIRECTDW_PREREG.md:13,31,51`). The source sequence now has a correction note; its original rationale remains below it (`results/research_pass_2026-10-06/recommended_sequence.md:1,15`).

**Replacement addition to §0:**

> The inherited statement 'later value tokens have no objective' is withdrawn. compute_z labels every target token and averages their NLL (`memit_dry_run/memit/memit/compute_z.py:60–65,141–150`). The closed-form weight solve reads subject-last keys and a keyed block-output residual; it has no direct value-position loss (`experiments/track_c/c10e_bandknob.py:196–211`). B-e2e changes the optimisation variable and the model in which the loss is evaluated, not the target-token coverage of compute_z.

### 9. BLOCKING — AGREE-WITH-CHANGE: feasibility needs the right memory accounting and an affordable parity check

The adopted micro-batch makes feasibility plausible, not verified. The table omits at least the live arm cache: five zero matrices at 11008² float32 add approximately **2.26 GiB**, before solve/SVD temporaries and retained updates (`docs/C10Y_DIRECTDW_PREREG.md:128–138`; `experiments/track_c/c10e_bandknob.py:209–211,474`; arithmetic I-INFER). Covariance is retained on CPU; P is constructed on CPU (`memit_dry_run/memit/memit/memit_main.py:280`; `experiments/track_c/c10e_bandknob.py:173–175`). The Metal-driver metric measures Metal allocations and cache/framework allocations, not a documented total process footprint (`.venv/lib/python3.11/site-packages/torch/mps/__init__.py:124–141`). Adding RSS to driver bytes as an exact unified-memory total is unjustified; their overlap is **UNVERIFIABLE from these APIs**.

Also, the supposedly unadopted full batch is nevertheless required by the gradient-parity check (`docs/C10Y_DIRECTDW_PREREG.md:111,139`). A parity gate must not itself require an unproven memory envelope.

**Replacement for §2.10 and the memory/gradient check:**

> Memory feasibility is UNVERIFIED. Charge model, covariance, projectors, live arm caches, snapshots, solve/SVD temporaries, stored updates, head tensors, activations and optimiser state to the one unified pool. Record synchronised current/driver MPS allocation, process RSS and host available memory separately; do not sum overlapping metrics and call the sum measured physical usage. Before and during every heavy phase, HALT if driver allocation>32 GiB, RSS>40 GiB, or host available memory<8 GiB. Equality is allowed. Missing required telemetry is a preflight failure, not a silent assumption. Record peak values through projector construction, capture solves, parity checks, backward, merge and evaluation; a single init sample is not a peak. fp16 model and float32 A/B stay on MPS; every float64 diagnostic/solve must first move its tensors to CPU. No CUDA operation or new covariance job is part of this screen.

> For gradient accumulation parity, use a fixed 12-request A7 subset, selected by published indices before execution, with identical padded token tensors and a one-batch reference only after its measured headroom passes. Compare that reference with splits 6+6 and 5+7, weighted by request count. Require finite nonzero layer gradients, cosine≥0.999 **and relative L2 error≤0.01** for every layer. Test the 24-request weighting/index logic separately without allocating a 24-request autograd graph. State the scope as accumulation parity on the subset; do not claim empirical full-24 parity. Failure to fit the reference within the guard is HALTED-RESOURCE, not a licence to loosen the gate after seeing results.

These safety/measurement thresholds are review proposals to freeze, not measurements of this machine. The hardware and fp16 MPS path are established; this new backward path is not (`CLAUDE.md:3`; `experiments/track_c/c10e_bandknob.py:48`; `docs/C10Y_DIRECTDW_PREREG.md:143–147`).

### 10. ADVISORY — AGREE-WITH-CHANGE: time the entire compiler; TTL starts before the compiler

The lock is acquired at task declaration and auto-releases after 60 minutes; the two-hour default is specifically for non-Genesis PREPARED transactions (`research_and_specs/llm-as-database-v1_2-integrated-spec.md:677–682,781–785`). Timing gradient steps alone understates a per-commit compile and cannot prove lock fit. The draft is Genesis-shaped (`docs/C10Y_DIRECTDW_PREREG.md:11`).

**Replacement W2/readout:**

> Report complete per-patch compile time, including target solves, capture, optimisation, merge and mandatory production probes; report one-time setup and experimental controls separately. Compile duration≥3600 seconds adds EXCEEDS-TTL as a necessary lock-fit warning, including equality at expiry. A duration below 3600 is not sufficient for lock compliance: the lock begins at task declaration, so remaining TTL at actual commit must be positive. The two-hour PREPARED default is an incremental compatibility comparison, not this Genesis-shaped batch's configured timeout. Neither a timing pass nor a timeout qualifier changes MEASUREMENT-ONLY status. N=24 timings are not a measured compaction scaling result.

### 11. ADVISORY — AGREE-WITH-CHANGE: regeneration, norm matching and sham wording

**(a) R1.** The adaptive floor can accept a very low cosine if the reference itself scatters (`docs/C10Y_DIRECTDW_PREREG.md:171`). The shared stub actually specified cosine≥0.99; the advisor's 0.95 floor is a new relaxation, not restoration of that contract (`results/research_pass_2026-10-06/prereg_stubs.md:77`; `results/c10y_directdw_advisor_v1.md:137`). Cosine alone also permits a scaled write.

**Replacement R1:**

> For nonzero updates, per-layer cross-process cosine≥0.99 **and relative L2 distance≤0.10**, where distance=||D_p1−D_p2||_F/max(||D_p1||_F,||D_p2||_F), on actual applied updates, for every completed arm/recipe required for the positive. Equality passes. Record baseline distances too. Baseline cosine<0.99 or relative distance>0.10 is a failed baseline regeneration instrument, not permission to lower the candidate threshold. Zero norms are represented explicitly: two exactly zero updates are identical; one zero and one nonzero fails. Keep R2 difference≤5 and R3 disagreement≤d_A+3 unchanged. These gates certify this fixed-input regeneration only.

**(b) NM.** Per-layer matching can increase smaller layers and changes relative layer direction, conflicting with D-10 and a direction-only comparison (`docs/C10Y_DIRECTDW_PREREG.md:80,223`). A uniform downscale is the clean total-norm control. It does not, by itself, rule out concentrating more of the write in one layer; item 18 addresses that.

**Replacement NM-total:**

> Let D_B,l be the actual effective candidate update and N_B=Σ_l||D_B,l||_F; define N_A analogously. If N_B>N_A, use one scalar s=N_A/N_B<1 for all layers and apply sD_B,l to the same pristine band. No layer is scaled up. Measure the merged control's actual updates: the summed norm must match N_A within 1%, with per-layer direction cosine to D_B,l≥0.999 for nonzero updates. Otherwise the size control is SIZE-UNTESTED. All readout/validity/locality/fit checks applicable to this stored-update path still apply. If N_B≤N_A, no NM-total is required, but do not call the per-layer size question moot.

**(c) Sham.** CORPUS/50 used a second-write ratio≤0.25, not a total-write interval [0.8,1.25] (`CORPUS/50_C10Q_STACKED_SOLVE.md:19`). B-z is an active alternative objective, not a null intervention.

**Replacement sham text:**

> B-z is an anchor-objective comparator and H-Y2 test. Its ANCHOR-SHAM-INERT descriptor means |n_z−a|≤5 and total actual-write ratio in [0.8,1.25], a window newly set here; CORPUS/50's second-write rule does not transfer. The descriptor is not a validity or fit gate and does not replace B-z's scientific status. The actual inertness controls are the reduced/no-change paths in §2.8.

### 12. ADVISORY — AGREE-WITH-CHANGE: overlap audit must have an outcome, not just a record

The shared contract requires input provenance and a held-out overlap audit; the draft freezes templates but does not prescribe that audit (`results/research_pass_2026-10-06/prereg_stubs.md:12`; `docs/C10Y_DIRECTDW_PREREG.md:85,95`).

**Replacement addition to §2.6 item 2:**

> Before writing, publish and hash every frozen context template and the instantiated canonical-rewrite/target-prefix/KL inputs. Normalise using case folding, punctuation removal and whitespace collapse while preserving a subject placeholder; report exact and held-out-frame containment matches against PTEST. A held-out frame inside a write input is INVALID-LEAKAGE and HALTs before candidate optimisation. Generate inputs without using held-out scores; do not redraw a leaking context set until it happens to pass. Store the audit and the fixed rule in H_in. Held-out prompts may be used for prescribed evaluation, never for gradients, checkpoint selection, timing-smoke selection or stopping.

### 13. ADVISORY — AGREE-WITH-CHANGE: answers to review questions, without the alleged threefold bound

K1 was an A1/A2 keying reference; CORPUS/43 explicitly did not test A7 (`CORPUS/43_C10K_KEYING_ABLATION.md:6,12–17,52`). The appropriate A7 reproduction envelope is CORPUS/44. The learning-rate rationale does not bound ||AB||/||RB||: Adam normalises moments, and even an entrywise A displacement bound would not control a potentially cancelling product's relative norm (I-INFER from the factorisation and update rule; `docs/C10Y_DIRECTDW_PREREG.md:43,62`; `.venv/lib/python3.11/site-packages/torch/optim/adam.py:519–535`).

**Replacement for §6 reviewer answers and the lr rationale:**

> (a) Use untouched same-process recipe A, its CORPUS/44 A7 envelope, the established A1/A2 controls, and the capture/zero-step/executed-loop reductions. A separate K1 rerun is not required; K1 is not an A7 ceiling. (b) lr_l=0.02·rms(R_l) and T_max=100 are unmeasured fixed heuristics, not a proved fair optimisation budget or a bound on write growth. Record actual norms each step and apply the fit rule at every stop; remove 'at most roughly triple'. (c) Keep h0_ij+delta_i: compute_z adds the same activation delta at each prompt's lookup index (`memit_dry_run/memit/memit/compute_z.py:95–99,180–185`). (d) Routing-off is not part of the default spend; if it is needed for attribution, freeze it as a separately budgeted secondary experiment before running it. (e) Use the fixed R1 contract in item 11, not a progressively permissive baseline-derived floor.

### 14. ADVISORY — AGREE: make L2 explicit and qualify the exact-arithmetic derivation

The factorisation follows the harness solve, and the omitted division happens to equal one under current L2 (`experiments/track_c/c10e_bandknob.py:29,209–211`). It is an algebraic statement, not an empirical proof of exact protection after fp16 merging.

**Replacement in §2.2:**

> From (PM+L2·I)X=PK, obtain X=P(K−MX)/L2, with L2=1.0 here. In exact arithmetic, for an orthogonal P, X lies in range(P), so Bk=Xᵀk=0 whenever Pk=0. ΔW=AB has rank≤24 before finite-precision materialisation. The implementation tests numerical factorisation and projector tolerances; it does not assert bit-exact factorisation or exact preservation of the quantised deployed update.

## Additional defects the advisor missed

### 15. BLOCKING — LAW#3 is written correctly but bypassed by the execution order

V4 specifies the right envelope and says no B runs on a miss. Yet execution puts step 0 before recipe A, and step 0 includes candidate backward/timing steps and hooked/merged B evaluations (`docs/C10Y_DIRECTDW_PREREG.md:88,109–112,147,161`). Checking V4 after those steps violates the requested before-any-candidate gate even when the smoke is discarded. The advisor's replacement retains that order (`results/c10y_directdw_advisor_v1.md:61`).

**Replacement execution-order/V4 text:**

> Fingerprint and read-only input audit → initialise/freeze contexts and solve pristine targets → untouched recipe A and its standing LAW#5 gate → **LAW#3** → new-path reduction/inertness/objective/deployment checks → candidate timing/backward smoke → substantive B-e2e. No new-path candidate hook forward, backward, optimiser iteration, closure arm or NM evaluation occurs before the baseline gate. Static arithmetic and untouched-engine target solves are permitted beforehand. LAW#3 requires all three A7 integer counts simultaneously: para_full_n∈[5,18], canon_full_n∈[5,10], para_first_n∈[42,59], with denominators 72/24/72 respectively and baseline A1/A2≥68/72. Every endpoint is inclusive (`CORPUS/44_C10L_COVGEOM_SPARSEBAND.md:39`; shared controls `results/research_pass_2026-10-06/prereg_stubs.md:10`). Any miss HALTs the entire planned schedule, including future processes, before candidates. Do not use this reproduction interval as a candidate positive threshold or widen it after observing the baseline.

### 16. BLOCKING — the loss is not evaluated through the deployed fp16 arithmetic

The optimiser uses a float32 low-rank product added to a separately rounded fp16 module output, whereas deployment rounds AB to fp16 and adds it to an fp16 weight before the module's matrix multiplication (`docs/C10Y_DIRECTDW_PREREG.md:51,70,73`). These are different arithmetic graphs. The actual module is a linear down projection (`.venv/lib/python3.11/site-packages/transformers/models/qwen2/modeling_qwen2.py:53–59`); the baseline performs the in-place fp16 weight addition (`experiments/track_c/c10e_bandknob.py:216–217`). Init allows one and final allows two mismatched prompts, with logit/loss differences merely recorded (`docs/C10Y_DIRECTDW_PREREG.md:109,120,166`). Two held-out mismatches are enough to cross 18/19 or a 9/10 gain boundary. Scoring the merged model protects the reported count, but does not establish the central 'optimise exactly what is deployed' premise.

**Replacement objective/deployment gate:**

> Optimisation forwards use the deployed effective weight arithmetic: W_eff=fp16(W0+fp16(AB)), with the same module input dtype/kernel path as final deployment. Implement this functionally/differentiably in the harness, with W0 detached and frozen; do not train through the sum of a base output and a separately evaluated low-rank output and call it exact deployed optimisation. Cast backward and subject routing are explicitly surrogate-gradient choices; forward values must match deployment. At init and at the final state, require identical generated target-length token-id sequences, hence identical full-sequence hit vectors, on all 24 canonical plus 72 held-out A7 prompts. Require teacher-forced loss difference≤max(1e−4,1e−3·|L_merged|), for the total and each component separately. Record loss components and logit differences. A miss is INVALID-TRAIN-DEPLOY-GAP, before any positive interpretation. Held-out parity evaluation never selects a checkpoint. The merged model remains the scored artifact.

The proposed functional path and tolerances themselves need LAW#5 validation; no claim that they have already passed is made.

### 17. BLOCKING — KL is ambiguously weighted twice; gradient finiteness/cosine do not prove correct optimisation

The draft writes L=L_edit+kl_factor·L_KL and defines L_KL as the engine's call, which already multiplies by kl_factor (`docs/C10Y_DIRECTDW_PREREG.md:51`; `memit_dry_run/memit/memit/compute_z.py:151–153`). Literal implementations can therefore use 0.0625 or 0.00390625, a 16-fold difference. The existing check compares only NLL, and gradient cosine alone cannot detect missing normalisation or loss-unscaling factors (`docs/C10Y_DIRECTDW_PREREG.md:111–112`). The local KL formula also fixes direction: with log_target=True, the target distribution weights target−input (`.venv/lib/python3.11/site-packages/torch/nn/modules/loss.py:474–486`).

**Replacement objective and optimisation audit:**

> Define KL_raw=F.kl_div(log_p_pristine, log_q_current, log_target=True, reduction='batchmean') over the 24 KL rows, i.e. KL(q_current||p_pristine), unweighted. L=L_edit+0.0625·KL_raw, with the coefficient applied exactly once. The pristine log distribution is detached; record raw and weighted KL separately. Validate both components against the engine at delta=0 and at a fixed nonzero intervention; matching a zero KL at init alone is insufficient. The new objective deliberately has no activation-vector weight-decay term; state that departure rather than calling the total loss identical to compute_z.

> Freeze all base parameters, require their gradients absent, and optimise A only. Explicitly use eval mode, no inference/no_grad context around the differentiable forward, and use_cache=False. Zero accumulated gradients at every accepted step; scale the loss, backpropagate, unscale the A gradients exactly once, then test finiteness and call Adam.step. An overflow discards all micro-batch gradients and changes neither A nor Adam moments/step counters before retrying. Bound and record retry attempts separately from successful updates. Verify gradient magnitude as well as direction under the accumulation check. The post-LAW#3 three-step smoke must include nonzero-lr A changes and finite gradients on every layer; record fixed-input loss before/after, base-weight invariance and restoration. Mere finite gradients or a successful lr=0 loop do not prove the real update works.

### 18. BLOCKING — attribution can credit a NULL control; total size does not settle layer redistribution

T2 only tests NM−A≥10, so **A=5, NM=18** is credited despite NM being inside the NULL envelope. It also omits the control's locality/fit and other validity failures. T1 assigns an anchor cause from a small count difference instead of reporting that anchor closure remains an explanation (`docs/C10Y_DIRECTDW_PREREG.md:188–190`). The claimed size question is 'moot' for total ratio≤1 even if one layer grows (`docs/C10Y_DIRECTDW_PREREG.md:80`). Existing evidence explicitly shows per-layer concentration matters to describing the write (`CORPUS/50_C10Q_STACKED_SOLVE.md:25`).

**Replacement attribution rules:**

> Define size-control-positive in each process using the **same** complete validity, FIT-E2E, n≥max(19,a+10), G1–G5 and actual-size requirements as the candidate. A norm control inside [5,18], or with any failed locality/fit condition, does not exclude size even if its baseline-relative gain is 10. A failed instrument/control requirement gives SIZE-UNTESTED; a valid tested control without a clean positive gives SIZE-NOT-EXCLUDED. Neither qualifier proves that size caused the gain.

> Record every per-layer actual-write ratio. If any layer grows while the total does not, size redistribution remains a confound. For a clean size attribution, additionally use a uniform downscale s_env=min(1,min_l ||D_A,l||/||D_B,l||), taking the inner minimum only over nonzero candidate layers, preserving candidate layer directions while bringing every such layer within the baseline envelope. A zero reference with a nonzero candidate forces s_env=0; an all-zero candidate needs no rescaling and cannot be credited as a positive on unchanged base predictions. Check actual merged layer norms≤1.01×reference and direction cosine≥0.999 on nonzero control layers; a miss is SIZE-UNTESTED. This is an envelope control, not an exactly total-norm-matched control. It is conditional stage-2 work, not part of the cheap screen.

> A valid FIT-Z B-z with a sized gain and e2e−B-z<10 yields **ANCHOR-NOT-EXCLUDED**, not ANCHOR-ATTRIBUTED. A missing, invalid or unfit B-z yields ANCHOR-UNTESTED. To credit H-Y1, both processes must show a valid fit clean positive after the required size control(s), and that resulting e2e control must beat the valid fit B-z by≥10. A positive raw B-e2e difference that disappears after size matching is insufficient. Credit is scoped to this objective/parameterisation; it does not establish that closed-form allocation is the unique limit.

### 19. BLOCKING — locality omits the frames actually used by the writer

The writing objective uses six context-prefixed rewriting frames; the proposed frame probe only uses CANON (`docs/C10Y_DIRECTDW_PREREG.md:51,117,134`). The shared contract explicitly requires a separate same-frame gate in **every fitted frame**, not a pooled canonical-only number (`results/research_pass_2026-10-06/prereg_stubs.md:10`). The protected-subspace argument also cannot make this behavioural check redundant: projection preserves a linear subspace, while the forward keys can change with earlier writes (`docs/C10Y_DIRECTDW_PREREG.md:45,47`).

**Replacement G2/locality scope:**

> For each of the six frozen rewriting frames, independently probe the six never-edited FRAME_SUBJECTS for edited-value first-token flips, before/after recipe A and the candidate. Require candidate flips≤A+1 separately in every frame; do not pool away a failing frame. Retain canonical L1, L3, described_as and generic perplexity gates. The '{s} is a' distribution is an objective-anchored preservation readout, not an independent bystander. associated_with remains a reported non-objective probe. A clean label means clean on these named gated axes only; it does not mean all neighbouring facts or relation labels were preserved.

### 20. BLOCKING — theoretical rank/projection is not automatically the applied fp16 update's property

The draft calls the constraint exact for every A and gates the **float32** update's null-space share (`docs/C10Y_DIRECTDW_PREREG.md:45,110`). The applied modification includes casting and addition to the fp16 baseline (`experiments/track_c/c10e_bandknob.py:216–217`). I-INFER: rounding can change both rank and protected-span leakage, so a pre-merge projector check cannot establish the exact physical claim.

**Replacement geometry/V7 language:**

> Report two objects: planned float32 AB and actual D=W_post.float()−W_pristine.float(). All write-size, NM matching and regeneration gates use D. Report null-space share and covariance-weighted energy for both; require share≥0.999 per layer for the planned and actual nonzero update, including init and final states. If the untouched reference cannot meet the proposed deployed tolerance, HALT for a precision diagnosis before candidate interpretation; do not weaken it after a candidate result. Treat zero updates explicitly. Rank≤24 and zero response on ker(P) are exact-arithmetic properties of AB, not asserted exact properties of D. Behavioural locality remains binding.

### 21. BLOCKING — input identity is incomplete, and regeneration does not replace the committed overlay hash

H_in lists 24 requests despite three distinct 24-request arms; it includes driver/reader hashes but not the harness, other engine primitives, tokenizer or backend identity (`docs/C10Y_DIRECTDW_PREREG.md:86,101`). The fingerprint tool pins memit_main only, not compute_z/compute_ks/repr_tools (`tools/engine_fingerprint.py:31–43`). The harness also accepts MODEL_ID/MODEL_REV and resolves defaults at import; pinning a document is not refusing those overrides (`experiments/track_c/c10e_bandknob.py:25–26,45–48`). The input/output certificate proposal wrongly makes replacing the spec's overlay hash seem necessary: the spec requires the actual committed overlay hash, not bit-identical hashes from a future recompile (`research_and_specs/llm-as-database-v1_2-integrated-spec.md:671`; `docs/C10Y_DIRECTDW_PREREG.md:101,198`).

**Replacement manifest/regeneration/spec-amendment block:**

> Common H_in binds the ordered request lists for **all three arms**, model ID/revision and base-weight artifact identity, tokenizer artifacts/settings, covariance/hparams/context hashes, preregistration and complete objective/optimiser/stage table, harness/driver/reader and every used engine primitive source hash, library/backend versions, resolved MPS device, dtypes, seed, routing and batching settings. Refuse mismatched model/revision/device/knob overrides before harness import. Store pristine-band hashes and verify them at every restore boundary. Recheck source/input identity at each stage; source drift HALTs, without overwriting prior records.

> Recompute targets independently from the same pristine inputs in process 2; store each process's target hashes as intermediate outputs, not an expectation that potentially nonidentical regenerated targets share one content hash. Within a process, share each arm's pinned targets and capture inputs across its comparators. Store hashes of the named/dtyped/shaped update tensors, the actual applied band state and the immutable serialized overlay. Preserve the **actual committed overlay hash** required by §11.5; H_in and a regeneration certificate are supplementary audit metadata. Do not replace artifact identity with behavioural similarity or conclude that a failed similarity gate means no ledger could record the artifact.

> R1–R3 certify fixed-input cross-process regeneration under this experiment. Same seed, frozen contexts and the same 24 facts are not independent-seed robustness or compaction-at-scale evidence. Report that scope explicitly. This experiment proposes no automatic §11.5 hash amendment and grants no route status.

## Source snapshot and handoff

Review inputs at writing: `docs/C10Y_DIRECTDW_PREREG.md` SHA-256 `f95c6f64e0c45c000bb001985ff0343cc6822b673757fdd627d0ec8ce7554773` (228 lines); `results/c10y_directdw_advisor_v1.md` `e6d0d08a68af404d0d670adb1062814a2f56e39788973c5f390898f81b8e3511` (161 lines); `memit_dry_run/memit/memit/compute_z.py` `d94af7fa14e5a4a20d5fa6361e0cbb30da0ff957db31922557ff809c34205dea`; harness `experiments/track_c/c10e_bandknob.py` `1f6be5811d7e58f3ebda16867a4a174b1cf24d47f9a2514cf9c3f9d29f18e695`. These hashes identify the text/code reviewed, not a runtime validation.

The review deliverable is complete; the design remains FIX-FIRST. Fold the replacements into a single consistent v2 before freezing: stage-aware completion/counters, gates before candidates, fit before negative interpretation, controls before attribution, and measured budgets before additional spending. In particular, replace the hard-coded nine override hits with a stage/arm execution ledger: completed writes/checks must consume exactly their declared overrides, and NOT-RUN arms cannot be counted as completed (`docs/C10Y_DIRECTDW_PREREG.md:86,163`). No scientific run, promotion, canonical-tracker closeout or preregistration edit is performed by this review.

Tool provenance: one successful read-only Graft query with refresh disabled; reported savings approximately 22,125 tokens, $0.02. Evidence and citations above were checked against the actual source rather than the ranked graph excerpts.
