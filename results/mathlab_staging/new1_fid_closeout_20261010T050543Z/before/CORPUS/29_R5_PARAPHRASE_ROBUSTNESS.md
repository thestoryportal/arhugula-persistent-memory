# CORPUS/29 — R5: Usable in-weight knowledge IS achievable (novel facts robust; counterfactual-over-prior recipe-rescuable)

**Decision-ID:** `D-R5-1`. **Date:** 2026-06-25. **Pre-reg:** `docs/R5_PARAPHRASE_ROBUSTNESS_PREREG.md` (advisor-checked; intensity-control arm added pre-build). **Runner:** `experiments/track_c/r5_paraphrase_robustness.py` (adapts r13; engine UNMODIFIED, primitives verbatim/inert). **Result:** `results/r5_paraphrase_robustness.json` (+ `results/r5_stats.json`).
**E2e-map cell:** §8.9 L2 native-knowing / the paradigm payoff (§1); F1 condition **C3/R5**; follows **R13** (D-R13-1). **Label:** **CHARACTERIZATION**, **NOT promoted** (N=16/arm, 1 seed, 1 relation).

## Question
R13 found counterfactual-over-prior edits fire 100% on the trained prompt but ~22% under paraphrase, with a *consistent-with* (not isolated) native-competitor bound. R5 isolates the competitor variable **within one protocol** and tests whether a **generalization-aware recipe** rescues it — i.e. can in-weight editing produce **usable (paraphrase-robust) knowledge**, or only trained-prompt parrots?

## Design — 4 arms, intensity-controlled (advisor reallocation)
Qwen2.5-3B / band[4-8] / single joint AlphaEdit / N=16 facts/arm. Metric = firing on **held-out P_test paraphrases** (disjoint from any training paraphrase). The 3 PRIOR arms edit the **same 16 facts** (paired). Controls all clean: NOVEL canonical base 0/16; P_test target-base 0/16 both arms; native P_test validity 16/16; **L1-took 16/16 all arms** (every edit installed).

| arm | training/fact | mean-rate | **all-3-hit (usable)** | any-hit | per-paraphrase | revert-to-true |
|---|---|---|---|---|---|---|
| **NOVEL-single** (no competitor) | canonical ×1 | **100%** | **16/16** | 16/16 | [100,100,100] | n/a |
| **PRIOR-single** (counterfactual over prior) | canonical ×1 | **25%** | **0/16** | 9/16 | [0,19,56] | 27/36 (75%) |
| PRIOR-multi-same (intensity control) | canonical ×3 | 31% | 0/16 | 12/16 | [0,19,75] | 28/33 |
| **PRIOR-multi-para** (paraphrase diversity) | canonical+2 paraphrases | **65%** | **3/16** | 15/16 | [38,69,88] | 12/17 |

**Per-fact hit-count distribution [0/3, 1/3, 2/3, 3/3]:** NOVEL [0,0,0,**16**] · PRIOR-single [7,6,3,0] · multi-same [4,9,3,0] · multi-para [1,2,**10**,3]. The recipe shifts mass from 0–1 hits → 2–3 hits (a large distributional improvement) even though full all-3 stays rare.

*(Metric framing, cross-family-corrected: **mean hit-rate is the PRIMARY usable metric** (≈ P(a random natural phrasing works)); **all-3-hit = a stringent robustness indicator** (brittle at 3 paraphrases — don't use as the sole pass/fail; the 0→3/16 n.s. is largely a power issue); **any-hit = diagnostic only** (1-of-3 isn't usable). NOVEL "16/16" = fully robust **on these 3 paraphrases** — true robustness lower bound is <100%.)*

## Findings (stats: `results/r5_stats.json`; significance bound to the usable-knowledge metric, not lenient any-hit)
1. **⭐ In-weight editing CAN produce usable, paraphrase-robust knowledge — for NOVEL facts.** NOVEL: **16/16 all-3-hit (100%)**. The R13 fragility is **NOT generic.**
2. **The fragility is COMPETITOR-SPECIFIC** (isolated within-protocol), and **decisive on every metric**: NOVEL vs PRIOR-single = **16/16 vs 0/16 all-3-hit** (Fisher p≈0; any-hit 16/16 vs 9/16 p=0.0068; mean 100% vs 25%). **Mechanism confirmed (R13's unlogged gap closed): 75% of PRIOR paraphrase-failures output the TRUE capital** — the dense native prior reasserts; the edit is a narrow trained-template attractor that fails to override it.
3. **A generalization-aware recipe lifts PARTIAL generalization significantly, but rarely achieves FULL robustness for overwriting priors:** PRIOR-single→multi-para mean 25%→65% (continuous per-fact rate **13 up / 0 down, sign-test p≈0.0002**; any-hit 9→15/16, McNemar p=0.031). **But strict all-3-hit only 0→3/16 (p=0.25, n.s.)** — the recipe roughly doubles partial firing yet leaves most counterfactual-over-prior edits NOT fully paraphrase-robust.
4. **The rescue is paraphrase DIVERSITY, not training INTENSITY — directional** (intensity-control worked): multi-same (3× same prompt) mean 31% (+6pp, n.s.) vs multi-para 65% (+34pp). Isolated diversity/intensity steps underpowered at N=16 (all-hit p=0.25 / 1.0) → directional, not proven. **Lexical-leakage check:** P_test1 ("…capital city is called") shares "capital city" with a P_train item yet is multi-para's WORST cell (38%) → leakage is NOT inflating the rescue (strengthens it).

## Verdict / F1 impact — INSERT path improved; UPDATE path bracketed + unresolved
- **INSERT path (new project facts = novel + thin = NOVEL arm) — MATERIALLY IMPROVED:** in-weight native-knowing is **robust (16/16 all-hit)**. The paradigm payoff holds for the fact class deployment most needs (inserting new code/project facts with no entrenched competitor).
- **⚠ UPDATE path (the spec REQUIRES it — §8 incremental, §11.12 pruning/staleness, compaction re-runs overwrite known facts) — FRAGILE, partially-rescuable, with an UNMEASURED neighbor cell:** overwriting maps to the PRIOR cell. **PRIOR-vs-pretraining is itself a real, important update case** (correcting post-training-cutoff facts / pretraining errors pits the edit against entrenched pretraining) — fragile on single-prompt (mean 25%, 0/16 robust), partially rescued by the diverse recipe (65% mean, still 3/16 robust). ⚠ **A DIFFERENT update sub-case — overwriting a prior `.vindex` EDIT (not pretrained knowledge) — is a SEPARATE, UNMEASURED cell** (cross-family-flagged): a prior edit may have *localized* the representation (easier to retarget) OR *entangled* it (harder) — its difficulty is **not assumed to lie between NOVEL and PRIOR**. Conjecture + planned follow-up (two-step overwrite: edit→re-edit, same metrics), not a result.
- **B3N qualifier (two-sided):** weights serve *usable* forward reads for **inserts** (robust on this benchmark); for **updates vs pretraining**, fragile-but-partially-recipe-rescuable; for **update-over-prior-edit**, unmeasured → may require the paraphrase-diverse recipe and/or side-store delegation.
- **Recipe amendment = CANDIDATE pending a powered run:** train edits on **paraphrase-diverse prompts** (the diversity-vs-intensity isolation is p=0.25, not yet powered) — and note the recipe lifts partial but not full robustness for overwriting priors. Do NOT hard-code yet.

## Scope / caveats
band[4-8]/3B/N=16-per-arm/capital/single-batch/1-seed. **NOVEL co-varies competitor-absence with subject-richness** (fictional token = no-competitor AND thin) → "novel facts generalize" not "pure competitor isolation" (but novel+thin = the realistic project-fact condition). Diversity-vs-intensity decomposition **directional, underpowered** (N=16 any-hit). 3 P_test paraphrases → a small probe set. NOT promoted.

## Process
Pre-registered (intensity-control arm added on advisor catch — else "recipe helps" would confound diversity with intensity); smoke-verified end-to-end (all gates, N=3); inertness INERT (|Δexpr|=0.0026). **Advisor done-gate: PASS** — caught the metric-mismatch (significance on any-hit vs mean-rate headline → bind to usable metric) + the INSERT-vs-UPDATE calibration (don't over-rotate to reassurance; updates required + untested at the right competitor-strength). **Cross-family = Perplexity Sonar DONE** (codex auth-expired) — converged + sharpened: mean-rate is the right PRIMARY metric (all-3 too brittle; report distribution); softened the overwrite-prior-edit "bracket" to a separate unmeasured cell (prior-edit may localize OR entangle); flagged "robust on 3 paraphrases" caveat; recommended the two-step-overwrite follow-up. All applied. **Next: the overwrite-prior-edit follow-up + a powered diversity-vs-intensity run before any recipe amendment.**
