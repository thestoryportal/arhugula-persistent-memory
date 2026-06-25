# CORPUS/28 — R13: Paraphrase-generalization (editing-overfit) — trained-prompt 100% → ~22% under paraphrase

**Decision-ID:** `D-R13-1`. **Date:** 2026-06-25. **Pre-reg:** `docs/R13_STORAGE_BEHAVIOR_SPLIT_PREREG.md`. **Runner:** `experiments/track_c/r13_storage_behavior_split.py` (adapts r2; engine UNMODIFIED, primitives verbatim/inert). **Result:** `results/r13_storage_behavior_split.json`.
**E2e-map cell:** §8.9 post-write verification / §F (`docs/SPEC_E2E_GROUND_TRUTH.md`); F1 condition **C2** read-contract leg (matrix **R13**); bears on **R5/C3** native-knowing. **Label:** **CHARACTERIZATION**, **NOT promoted** (1 seed / 1 relation / counterfactual-over-prior).

## ⚠ What this is (relabeled after cross-review) — and isn't
Pre-registered as the spec's L1-storage vs L2-behavior split (§8.9). **It is NOT that:** both probes are forward-pass generations — "canonical top-1" is *firing on the trained string*, not a structured store read-back. CP2 already established a true L1 `SELECT` is **index-delegated, not weight-native**. So what was actually measured is **trained-prompt expression vs natural-paraphrase generalization = the editing-overfit / "Mirage" phenomenon**, quantified under controls. *(Result-JSON interpretation corrected accordingly.)*

## Result (24 counterfactual capital edits, single joint AlphaEdit, band[4-8]/3B)
| probe | fires |
|---|---|
| **L1 trained prompt** ("The capital of {C} is the city of") | **24/24 (100%)** |
| L2 paraphrase P1 ("{C}'s capital city is called") | 2/24 (8%) |
| L2 paraphrase P2 ("The city that serves as the capital of {C} is") | 4/24 (17%) |
| L2 paraphrase P3 ("If you visit {C}, its capital city is") | 10/24 (42%) |
| **L2 any-of-3 paraphrases** | **11/24 (46%)** |
| **L2 all-3 fail (fully silent)** | **13/24 (54%)** |
| **mean per-edit paraphrase-fire rate** | **~22%** |
| trained-prompt-fail / paraphrase-success cases | **0/24** (no edit failed its trained prompt yet fired on a paraphrase — i.e. all successes are captured by the trained template; **NB: this is not a "storage" measurement — both probes are behavioral**) |

Controls valid: native L1 10/10, native L2 primary 8/10, native L2 any 10/10 (paraphrase probes fire on real capitals → a paraphrase-fail on an edit is a real generalization gap, not a dead probe). N=24 → binomial uncertainty is wide (±~10–20pp per cell); read the pattern, not precise rates.

## Headline (distribution, not the worst phrasing)
**A counterfactual edit fires 100% on its trained prompt but only ~22% on average across natural paraphrases (range 8–42% by phrasing; 54% silent on all three, 46% fire on ≥1).** Measuring the trained prompt alone **massively over-reports usable knowledge** (24/24 → ~22%). *(Leading with the worst single paraphrase, 22/24=92%, would be the asymmetric-metric trap — [[fixed-budget-sweep-couples-iv-with-complement]] / [[match-metric-to-the-claim]]; the distribution is the honest headline.)*

## Bound — native-competitor strength (CONSISTENT-WITH, not isolated)
The edits here are **counterfactuals over dense native facts** (France→Oslo vs the entrenched France→Paris). Contrast **R9** (fictional secrets, *no* native competitor): write generalized to ≥1 held-out paraphrase **79%**. **R13** (counterfactual over a strong prior): **~22%**. → **Consistent with** a "native-competitor strength" story — edits generalize well in low-prior settings and much worse against dense priors — but **NOT a clean isolation** (cross-family-flagged confounds: different domains (fictional secrets vs countries), possibly different paraphrase-set/protocol, small N + entity-selection variance). State as "supports," not "isolates." Mechanism (corrected): the edit creates a **narrow attractor around the trained template that fails to robustly OVERRIDE** the strong pre-existing attractor (France→Paris), which still dominates many paraphrases — *not* a clean overwrite. ⚠ **The confirming diagnostic — do paraphrase-failures revert to the TRUE capital (native dominance) vs a random city (instability)? — was NOT logged** → the revert-to-native mechanism is plausible, not measured (next-step).

## Verdict / F1 impact
- **Legitimate §8.9 contribution:** the L2 behavioral probe **must use held-out paraphrases** — trained-prompt firing is not evidence of usable in-weight knowledge. (The spec's *structured* L1/L2 split itself needs the index, per CP2.)
- **⭐ Consequence for the paradigm payoff (R5/C3, B3N) — NARROWED:** **counterfactual overwrites of strong in-weight priors are fragile to paraphrase at small N** (reliably expressed on the trained template, often lost under paraphrase). This qualifies the B3N read "weights carry forward native-knowing": demonstrated **on the trained phrasing; paraphrase-firing degrades sharply when competing with dense priors.** ⚠ Do NOT generalize to "native-knowing is fragile" broadly — UNTESTED here: neutral/novel facts (R9 suggests they generalize far better), larger N, generalization-aware recipes, other knowledge types. Potentially a sharper threat to the in-weight thesis than compaction *if* it persists for usable (neutral/novel) facts — which is the open question, not a settled result.
- **The real F1 falsifier it sets up (next, not run here):** can a **neutral/novel fact** or a **generalization-aware recipe** (multi-paraphrase training, preserve-style) close the 22% gap → produce *usable* in-weight knowledge, not trained-prompt parrots? That is the R5/native-knowing thread.

## Scope / caveats
band[4-8]/3B/N=24/capital/single-batch/1-seed/**counterfactual-over-native-prior**. The ~22% is recipe- and competitor-specific (basic joint AlphaEdit, no multi-paraphrase training). **Only 3 hand-designed paraphrases → ~22% is a LOWER BOUND on a small probe set, not a full estimate over natural phrasings.** Per-paraphrase variance large (8–42%) → report the distribution, crown no single phrasing. N=24 → wide binomial uncertainty. Failure-output breakdown (revert-to-native vs random) not logged. Both probes behavioral (no storage channel measured). NOT promoted.

## Process
Pre-registered; inertness gate INERT (|Δexpr|=0.0003). **Advisor pre-write** (relabeled storage/behavior→paraphrase-generalization/editing-overfit; headline = distribution not 91.7%; required the R9-contrast bound; calibrated the consequence into R5/C3). **Cross-family review = Perplexity Sonar Reasoning Pro DONE** (codex auth-expired) — converged + tightened: (1) both probes behavioral, no storage measured (fixed the consistency-check line); (2) R9-vs-R13 = "consistent with" not "isolates" (+confounds listed); (3) mechanism = "fails to override" not "overwrites"; (4) narrowed claim to counterfactual-over-priors, not native-knowing broadly; (5) flagged the unlogged failure-output diagnostic + 3-paraphrase lower-bound. All applied. **Next-step (converts consistent-with → confirmed):** re-run logging paraphrase-failure outputs (% revert-to-true-capital) + test neutral/novel facts and a generalization-aware recipe (the R5/native-knowing thread).
