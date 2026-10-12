Advisor pass on `docs/C10Y_DIRECTDW_PREREG.md` v1 (D-C10y-directdw), reviewer Claude Opus 5.5 (`claude-opus-5-5`), 2026-10-07, read-only, method `tools/advisor_review_prompt.md`
Verdict: FIX-FIRST

**Most important:** the draft has to resolve its standing before any build or run. It omits D-C10r-rulings-4 (3), which demoted step 7 until the step-5 oracle reads. It also argues for the "write candidate" label from a `compute_z` analogy that does not hold. Both must be fixed, and the 5–11 h block replaced by a single-process A7 kill stage.

**Scope A (write or measurement):** Label the step **"measurement, not a route"** for now. The operator can re-classify it with an explicit ruling informed by this run's wall-clock and reproducibility readouts. The writer runs gradient descent on model weights: the overlay factor A^l, 245,760 numbers, with B fixed, which is structurally a frozen-B LoRA. It uses an LM loss back-propagated through layers 4–35 (draft §2.3, §2.4). That is a training loop per commit, which the research pass's criterion excludes in its own words ("a training set **or** a training loop per commit", `recommended_sequence.md:11`; `HANDOFF.md:7`); the spec also excludes fine-tuning (spec `:313`). The `compute_z` analogy fails at exactly the line the accepted engine draws: `compute_z` optimises an activation-space vector (`compute_z.py:83`, `:104`) on frozen weights (`:105`), and the weights come only from the closed-form solve (`c10e_bandknob.py:209–211`). Having no external training set is a real distinction from H-13, and it keeps the audit trail regenerable. It does not cure the compaction harm. Compaction re-runs the writer over all active patches (e2e `:54`), and the draft's own arithmetic makes per-step cost linear in facts (4,704 tokens per step at N = 24, §2.11). Compaction would therefore become a back-propagation training run over the whole fact base.

**Scope B (budget):** Not justified as a mandatory block. The draft itself expects TRADEOFF or a LARGE-WRITE gain and "LEAD … is not the expected outcome" (draft `:23`). The step is under a standing demotion (`EXPERIMENT_RUNBOOK.md:331`). The research pass and the queue costed the run at 1–2 h (`recommended_sequence.md:27`; `prereg_stubs.md:80`; `docs/INTEGRATED_QUEUE_2026-10-07.md:22`), and the draft's 3–5× growth over that rests on an unmeasured 1–3 TFLOP/s (§2.11, UNVERIFIABLE until step 0). There is a free kill and a cheap one:
- **Free kill:** the step-5 oracle, queued ahead (`INTEGRATED_QUEUE:19`). If a band-LoRA trained on about 20 phrasings per fact cannot pass 18/72, an e2e objective on the canonical frames alone is very unlikely to. This is a prior, not a bound, so it belongs in the operator's re-decision rather than as a gate.
- **Cheap kill:** Stage 1 is one process running step 0, recipe A, and B-e2e on A7 only (≈ 1.2–2.2 h by the draft's own figures). It stops on NULL-sized or UNDERFIT. Only a survivor buys A1/A2 under B-e2e, B-z, NM and process 2. A NULL can only become INVALID by running the controls, never a gain, so nothing is lost.

## Checks the task asked for

- **The "3 %" correction is stated correctly** (draft `:13`, `:20`). ρ_c is called a *remaining* ratio, which matches `CORPUS/44_C10L_COVGEOM_SPARSEBAND.md:43` and `c10l_covgeom_step0.py:134`. No hypothesis, gate or label depends on the backwards reading. H-Y2's NULL prior uses it the right way round.
- **The second false claim ("value tokens two onward have no objective") does not appear in the draft.** `grep` of the draft for "no objective" and "objective" shows no hit carrying it. The draft is silent on the fact that its source (`recommended_sequence.md:13`) carries this claim too, which is issue 8.
- **The DOW-KE factorisation (§2.2) checks out algebraically against `c10e_bandknob.py:207–211`.** From `𝒜X = PK`, `X = P(K − MX)/L2`, so X lies in range(P) and `B k = 0` whenever `Pk = 0`. `ΔW = R Xᵀ` reproduces `upd = solve(A, B)ᵀ`. The draft writes `X = P(K − MX)`, which is valid only because `L2 = 1.0` (`c10e:29`); see issue 14.
- **The engine and harness citations I spot-checked are correct:**
  - `compute_z.py:41–65, :76, :104, :137–164, :175–180`
  - `memit_main.py:49, :191–194, :256–259, :280, :304–323`. The rewriting set is 1 identity + 5 sampled templates, so 6.
  - `c10e:28–29, :155–159, :166–178, :181–221, :403–446, :458–509`
  - `tools/engine_fingerprint.py:34, :36`
  - spec `:313, :316, :671, :678, :783`; e2e `:54, :62`
  - `CORPUS/50` table `:14–15` (×1.24, total ×2.24, `described_as` 89.31 → 85.09)
- **Padding:** `tokenizer_config.json` sets no `padding_side`, so the library default (right) applies and `compute_z.py:60–65`'s placement holds. This is I-INFER from the absent key; no library source was read.
- **The DOW-KE text in the repo does not support every paper number the draft uses.** `results/infranodus_research_arc_2026-10-05/fulltext/DOWKE_2608.16932.md` confirms routing +1.02 / −1.38 (`:403`) and 96.64 (`:158`). It contains no §4.1 or closure-gap text, so the r_gap ≈ 0.33 and the §5 quotations are **UNVERIFIABLE from the repo**; the draft says it read them from LaTeX that is not stored here.

## Issues (priority order)

**1. BLOCKING: a ruling in force is omitted, and the draft schedules a demoted step.**

Defect: draft `:5` lists the rulings in force without D-C10r-rulings-4. Its item (3), `EXPERIMENT_RUNBOOK.md:331`, reads: "Steps 6–7 (… H-3 direct ΔW) are **demoted** behind steps 1–4 and the step-5 oracle, their '3 % installed' motivation having been reversed by the CORPUS/44 correction; decided again only after those results." `:913` says the same steps "are re-argued with the operator before scheduling". D-C10r-rulings-9 (3) (`:342`) authorises only building them ("Codex builds steps 6 … and 7 … model-free in parallel"); it does not lift the demotion. Draft `:3` places the run in the queue without the re-decision.

Fix: in `:5`, after "D-C10r-rulings-3 (2) (write-only, quoted in §2.7)," insert: "D-C10r-rulings-4 (3) (`EXPERIMENT_RUNBOOK.md:331`: steps 6–7 demoted behind steps 1–4 and the step-5 oracle, 'decided again only after those results'),". Replace the second sentence of `:3` with:

> "Building is authorised model-free now (D-C10r-rulings-9 (3), `EXPERIMENT_RUNBOOK.md:342`). Running is not scheduled: under D-C10r-rulings-4 (3) (`:331`) step 7 is decided again by the operator only after the results of steps 3 and 4 and the step-5 oracle (`docs/INTEGRATED_QUEUE_2026-10-07.md:18–20`). That re-decision is §6 decision 0."

In §6, before decision 1, add:

> "0. *Re-schedule after demotion (D-C10r-rulings-4 (3)):* with the step-5 oracle's A7 count in hand, run stage 1 (§2.6)? Recommendation made at that time; if the oracle's held-out count is ≤ 18/72, the recommendation is no (an end-to-end objective on the canonical frames alone has less to fit with than the oracle)."

**2. BLOCKING: the §2.7 write-qualification argument fails on its central analogy, and the recommended label is the wrong default.**

Defect: §2.7 point 2 (`:96`) says "The engine already iterates per patch". `compute_z`'s loop optimises `delta`, an activation added at the lookup index (`compute_z.py:83`, `:98–99`), with the model frozen (`:105`); the weights are written only by the closed form (`c10e:209–211`). B-e2e optimises the weights' factor A^l by back-propagation through the deployed model. That is training in the sense `recommended_sequence.md:11` excludes ("a training set or a training loop per commit"). The spec names "full fine-tuning" as excluded (`:313`). Point 4 (`:98`) measures wall-clock per write but not the compaction harm. Compaction re-runs the writer over every active patch (e2e `:54`), and the per-step cost scales with N (§2.11). §6 decision 1 (`:210`) recommends "yes, write candidate".

Fix: replace the heading "**Why this writer qualifies as a write, on this program's reading.**" and points 1–4 with:

> "**Label: measurement, not a route (until the operator rules otherwise).** What separates this writer from the H-13/H-15 oracle: its inputs are the patch and fixed artefacts only (the strings `compute_z` builds, `compute_z.py:46–50`; no paraphrase or dataset); its output is an overlay on `down_proj`, rank ≤ 24 per layer, zero on the protected span (§2.2). What makes it training rather than a solve: it updates model weights (the factor A^l) by gradient descent on an LM loss through layers 4–35, which the accepted engine never does (`compute_z` optimises an activation on frozen weights, `compute_z.py:83, :104–105`; weights come only from the closed form, `c10e:209–211`), and the research pass's criterion excludes 'a training loop per commit' independently of a training set (`recommended_sequence.md:11`). Spec §8.2 excludes full fine-tuning (spec `:313`). Under compaction (e2e `:54`) the writer would back-propagate over all active facts, with per-step cost linear in N (§2.11). The run therefore answers a diagnostic question: does an objective evaluated in the deployed model, on the patch's own prompts, lift held-out recall beyond the closed form's allocation? Route status needs an explicit operator ruling, informed by the wall-clock, scaling and reproducibility readouts below."

Replace §6 decision 1 with:

> "1. *Write-only scope:* recommend **measurement** — run under the label above; a LEAD here is reported as 'the closed form's allocation is a limit that a weight-space objective on the patch's own prompts exceeds', and route status is a separate operator ruling."

In §3 "What each buys", replace "the optimised allocation becomes a candidate engine variant" with "the optimised allocation becomes a candidate for an operator route ruling (§6 decision 1); until then it is a measurement".

**3. BLOCKING: no early-kill stage, so the default spend is 5–11 h whatever the A7 result.**

Defect: §2.6 item 5 (`:88`) runs A → B-z → B-e2e (all three arms) → NM → readouts, and process 2 is "mandatory" (`:88`, D-11 `:224`). By the draft's own rules, every non-NULL label needs B-e2e's A7 count to exceed 18 and to beat A by at least 10 (`:178`). B-z matters only for attribution when B-e2e gains (T1, `:188`), and process 2 matters only for a positive (`:177–181`).

Fix: replace §2.6 item 5 with:

> "**Stages.** Stage 1 (one process): step 0 → recipe A (all three arms, V4) → B-e2e on A7 only → readouts. Stop with **NULL (stage 1; A1/A2 under B-e2e, B-z, NM and process 2 not run)** if B-e2e's A7 `para_full_n` ≤ 18 or < recipe A's + 10, or **UNDERFIT** (§3). Otherwise Stage 2 (same process): B-e2e on A1 and A2 (V5), B-z, NM where triggered. Stage 3: process 2, the whole sequence from the same `H_in`, only if stage 2 leaves a PARTIAL- or LEAD-sized count; it is the reproducibility run and gate A."

In §2.11, replace the "Per process" bullet's last sentence with:

> "Stage 1 ≈ 33 min (A) + 28–83 min (one B-e2e write) + ≈ 25 min (step 0, evaluation, projector) ≈ 1.4–2.4 h; stages 2–3 add ≈ 4–9 h only on a stage-1 survivor."

Replace D-11 with: "Process 2 runs only on a stage-2 survivor and doubles as gate A."

Replace §6 decision 2 with: "*Budget:* stage 1 ≈ 1.4–2.4 h; stages 2–3 ≈ 4–9 h only on survival; recommend yes to stage 1 only."

**4. BLOCKING: no underfit gate, so an under-optimised writer would be read as NULL.**

Defect: T_max = 100 at `lr_l = 0.02·rms(R_l)` (`:62–64`) has never been run. The draft leaves an UNDERFIT label as an open question (`:208` (b)). The program's last two solve-budget runs were UNDERFIT, and the program read them as inconclusive, not NULL (`CORPUS/51` title; `CORPUS/52_C10S_SOLVEFEAS.md:11`). Under the current §3, a write capped at step 100 with the training prompts unfit reads "NULL — this configuration not advanced" and moves the sequence on (`:194`).

Fix: add to §3 after the validity block:

> "**Fit (read before the binding count; B-e2e and B-z):** per fact, `f_i` = mean over the six rewriting prompts of exp(−per-prompt mean target NLL) in the merged fp16 model (`compute_z`'s diagnostic, `compute_z.py:149, :162`). A write is **UNDERFIT** iff its stop reason is the cap and (any `f_i` < 0.90 or `canon_full_n` < 20/24); for B-z, iff the cap is hit with `L_z` > 1e-3. An UNDERFIT recipe with A7 `para_full_n` ≤ 18 reads **UNDERFIT — inconclusive under this optimiser budget**, never NULL; a count > 18 is read by the labels below with the -UNDERFIT qualifier. No budget increase inside this pre-registration."

Add the `f_i` vector to §2.9's optimisation trace.

**5. BLOCKING: the label rules leave reachable outcomes without a label, and the truth table relies on one of them.**

Defect: LEAD requires "no -LARGE-WRITE" (`:177`) and PARTIAL requires count < 30 (`:178`), so a count of 31/32 at ratio 1.8 falls to "NULL: otherwise" (`:180`). The truth table nevertheless reads it as "LEAD-sized count with -LARGE-WRITE" with no base label (`:192`). TRADEOFF (`:179`) does not say whether it needs both processes. The -NOT-REPLICATED rule (`:181`) covers only LEAD and PARTIAL, so "p1 TRADEOFF, p2 NULL" and "p1 LEAD, p2 TRADEOFF" have no label. Since the reader issues labels (`:151`), the implementer would decide these after the fact: the CORPUS/50 prose/code divergence again (`CORPUS/50_C10Q_STACKED_SOLVE.md:19`).

Fix: replace `:177–181` with:

> "Per process: **LEAD** count ≥ 30/72, every locality gate holding; **PARTIAL** count > 18/72 and count − A ≥ 10 and < 30, every gate holding; **TRADEOFF** count > 18 and count − A ≥ 10 with a locality gate miss; **NULL** otherwise (UNDERFIT per the fit rule takes precedence). **-LARGE-WRITE** (W1) attaches to any label and blocks adoption and gate A; it never changes the base label. **Step label** = the lower of the two processes' labels in the order NULL < TRADEOFF < PARTIAL < LEAD, with the union of qualifiers; if they differ, add **-NOT-REPLICATED**; R1–R3 failure adds **-NOT-REPRODUCIBLE**. Without process 2 (stages 1–2 only) the label carries **-SINGLE-PROCESS** and is non-binding (`prereg_stubs.md:11`)."

Re-derive the truth table under this rule: row 2 becomes LEAD-LARGE-WRITE; row 7 becomes PARTIAL-NOT-REPLICATED-NOT-REPRODUCIBLE, because p2 = 22 is PARTIAL-sized at A = 12.

**6. BLOCKING: the LAW#5 reduction leaves the optimisation code path unexercised.**

Defect: check (iii) (`:108`) runs with T_max = 0, so the hook install and removal, gradient routing, micro-batch accumulation, loss scaling and the post-loop merge never execute. A hook left on `down_proj` after the merge would double-apply ΔW during evaluation and pass (iii) unseen. Check (i)/V2 carries no evidence about the new writer: `run_law5` sets `_LAW5_DEFAULT_CTX` (`c10e:430–433`), and the wrapper delegates every such call to the original (`:87` of the draft). So "ALL INERT" in every recipe would over-state.

Fix: append to §2.8:

> "**(iii-b) Loop-path identity.** Each B mode with T = 3 steps at lr = 0 (hooks, routing, accumulation and scaling all executed; Adam with lr 0 moves nothing) gives weights within (ii)'s tolerance of recipe A's and identical `canon_full_n`, `para_full_n`, `para_first_n`. **(viii) No residual hooks:** after every write, every hooked `down_proj` has `len(_forward_hooks) == 0` and `len(_forward_pre_hooks) == 0`, asserted and recorded."

Add to (i): "Check (i) is inert by construction for B modes (the wrapper delegates under `_LAW5_DEFAULT_CTX`, `c10e:430–433`) and is reported as the harness/engine parity only; the new writer's inertness is (ii), (iii) and (iii-b)."

Add (iii-b) and (viii) to V3.

**7. ADVISORY: the closure-gap comparison is mis-scoped, and the in-harness value already exists.**

Defect: `:13` says "On this harness the canonical-position closure gap is about one twelfth of the paper's (0.028 vs 0.33)". 0.028 comes from step 0's offline float64 reconstruction; CORPUS/44:43 says whether it "holds in the behavioural run remains unmeasured" and marks the paraphrase proxy "uninformative behaviourally". The in-harness value was since measured at 0.032650 / 0.233728 (`CORPUS/53_C10T_SECONDKEY.md:62`). The 0.33 cannot be checked from the repo (see Checks), and §2.9 calls the in-harness ratio still "owed since CORPUS/44:43" (`:119`).

Fix: replace the sentence with:

> "In-harness, the single-key reference leaves 0.0327 of the canonical residual norm and 0.234 on held-out prompts (`CORPUS/53:62`; step 0's offline reconstruction gave 0.028 / 0.232, `CORPUS/44:25`). DOW-KE reports r_gap ≈ 0.33 for AlphaEdit on Llama-3-8B (§4.1, read from the LaTeX source, not stored in this repo; definitions may differ). The canonical gap here is an order of magnitude smaller; the held-out one is of the paper's order."

In §2.9, replace "(the in-harness ratio owed since `CORPUS/44:43`)" with "(comparable to `CORPUS/53:62`)".

**8. ADVISORY: the second inherited false premise is not named.**

Fix: append to the `:13` correction paragraph:

> "The same criterion (`recommended_sequence.md:13`) also says 'the later words of the value have no objective'; that is withdrawn too: `compute_z` scores every target token (`compute_z.py:60–65, :141–150`); what lacks an objective at value positions is the closed-form weight solve, which reads only the subject-last key (`c10e:196–211`). B-e2e's `L_edit` is `compute_z`'s own loss; the arm changes where it is evaluated (the edited model) and what it moves (weights), not which tokens it scores."

**9. ADVISORY: the memory ceiling uses an instrument that cannot see half the budget.**

Defect: §2.10's peak (`:138`) adds CPU covariance and projectors (≈ 4.5 GiB, `memit_main.py:280`; `c10e:175` `.cpu()`). The readout `torch.mps.driver_allocated_memory()` (`:120`) excludes them, but the 36 GiB HALT compares against it (`:141`).

Fix: replace "**Ceiling:** measured peak > 36 GiB at step 0 → HALT" with:

> "**Ceiling:** step-0 peak of `torch.mps.driver_allocated_memory()` + process RSS (`psutil`) > 40 GiB, or MPS driver memory alone > 32 GiB → HALT; both recorded."

**10. ADVISORY: the spec-fit wall-clock is stated but never gated.**

Defect: §4 notes that "a write longer than 60 min does not fit the Write Lock TTL" (`:198`), but no label carries it, and the 60 s/step budget HALT allows writes of 100 min (`:147`).

Fix: add to §3 "Write size":

> "**W2:** wall-clock of any B-e2e write > 60 min (spec `:783`) adds **-EXCEEDS-TTL**, reported beside the label; with stages 1–3 it also records per-step time versus N for the compaction scaling note."

**11. ADVISORY: the reproducibility floor, the NM rescale and the sham citation each need tightening.**

- **(a) R1 floor.** With `c_A` low, R1's floor `c_A − 0.01` (`:171`) passes almost anything; add "and ≥ 0.95". That answers the draft's question (e).
- **(b) NM rescale.** The per-layer rescale (`:80`) can scale individual layers *up* even when the summed ratio exceeds 1.0, which contradicts D-10 (`:223`). Replace with: "`ΔW^l_NM = ΔW^l_B · s`, one scalar `s = Σ_l‖ΔW^l_A‖_F / Σ_l‖ΔW^l_B‖_F` < 1 for all layers."
- **(c) Sham citation.** ANCHOR-SHAM-INERT cites "the CORPUS/50 sham form, `:19`" (`:190`), but that sham's rule was a second-write ratio ≤ 0.25 (`CORPUS/50:19`), not [0.8, 1.25]. Change to "(window set here; CORPUS/50's sham rule, `:19`, was for a second write and does not transfer)".

**12. ADVISORY: no overlap audit for the frozen context templates against the held-out templates.**

Defect: the shared contract requires an overlap audit against the held-out templates for every write input that is not the triple (`prereg_stubs.md:12`). B-e2e trains on the frozen context-template continuations more directly than the closed form does.

Fix: add to §2.6 item 2: "The frozen templates' normalised overlap with the three `PTEST` templates (`c10e:51–61`) is computed and recorded before any write."

**13. ADVISORY: answers to the draft's review questions (§6 (a)–(e)).**

- **(a)** The zero-step identity plus the loop-path identity (issue 6), plus V4 on in-process recipe A, are the right LAW#5 reduction. A separate K1 re-run adds nothing that V4 does not already pin.
- **(b)** Adopt the fit rule of issue 4. The `0.02·rms` bound permits about ×3 (`:62`), which covers ×2.24, so a capped stop with unfit prompts is underfit, not a ceiling.
- **(c)** Keep the per-prompt anchor `h⁰_{i,j} + δ_i`: it is exactly the state `compute_z` optimised, since one `delta` is added at every prompt's lookup index (`compute_z.py:98–99`).
- **(d)** Run routing off only as a stage-2 secondary, if B-e2e survives stage 1.
- **(e)** See issue 11a.

**14. ADVISORY: the derivation states an identity that holds only at L2 = 1.**

Fix: in §2.2, replace "`X_l = P_l (K_l − M_l X_l)`" with "`X_l = P_l (K_l − M_l X_l) / L2` (L2 = 1.0, `c10e:29`)".

## Drift check and cheapest overturning test

Under the measurement label, the step bears on C10, the §C write path and the §8.9 L2 bar. It asks whether the closed form's residual allocation is the limit. The cheapest test that could falsify the H-Y1 premise is stage 1's single B-e2e A7 write against same-process recipe A, gated by the fit rule. If that does not clear 18/72 while fit, the step ends at about 2 h.
