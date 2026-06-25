# R5 — Native-knowing paraphrase-robustness: usable in-weight knowledge? (pre-registration)

**Date:** 2026-06-25 (frozen before build). **Decision-ID:** D-R5-1 (pending). **CORPUS:** 29 (pending).
**Matrix/condition:** F1 **C3 / R5** (native-knowing = the paradigm payoff). **Builds on:** R13 (D-R13-1, trained-prompt 100%→~22% paraphrase against priors) + R9 (fictional 79%). **Motivation:** R13 surfaced the sharpest in-weight threat — edits may be trained-prompt parrots, not usable knowledge. R13's native-competitor bound was *consistent-with, not isolated* (R9-vs-R13 cross-domain confound). This isolates it within one protocol AND tests whether a recipe rescues it.

## Question
Does in-weight editing produce **usable (paraphrase-robust) knowledge** — or only firing on the trained phrasing? Two variables, isolated within ONE protocol:
1. **Native-competitor strength** — does editing a fact with NO native competitor (fictional subject) generalize to paraphrase better than a counterfactual over a dense prior (real subject)?
2. **Recipe** — does a **generalization-aware recipe** (training on multiple paraphrases) close the gap?

## Design — 4 arms, intensity-controlled (advisor reallocation; same cost as 2×2)
Qwen2.5-3B / band[4-8] / single joint AlphaEdit per arm / engine UNMODIFIED / LAW#5 gate first. **N ≈ 16 facts per arm.** Recipe axis placed where generalization fails (PRIOR), with an **intensity control** so "train on paraphrases" isn't confounded with "train each fact 3× harder":

| arm | subject (competitor) | training prompts/fact | isolates |
|---|---|---|---|
| **NOVEL-single** | fictional country (no competitor) | canonical ×1 | — |
| **PRIOR-single** | real country → counterfactual (strong competitor) | canonical ×1 | — |
| **PRIOR-multi-same** | real country → counterfactual | canonical ×**3** (no diversity) | training **intensity** |
| **PRIOR-multi-para** | real country → counterfactual | canonical + 2 **P_train** | paraphrase **diversity** |

**Clean contrasts:** (1) competitor = **NOVEL-single vs PRIOR-single**; (2) recipe-rescue, intensity-controlled = **PRIOR-single → PRIOR-multi-same → PRIOR-multi-para** (multi-para > multi-same ⇒ diversity is active; ≈ ⇒ just intensity). *(Dropped NOVEL-multi — NOVEL-single likely already generalizes.)* NOVEL HALT-gate: pre-edit fictional-capital base ≈ 0.

⚠ **NOVEL co-varies competitor-absence with subject-richness** (a fictional token is both no-competitor AND thinly-represented) → NOVEL≫PRIOR shows "novel facts generalize better" (the realistic project-fact condition: novel + thin), **not pure competitor-isolation**.

## Metric (the usable-knowledge metric)
- **PRIMARY = held-out paraphrase firing**: top-1 = target across **TEST paraphrases (P_test)**, which are **DISJOINT from P_train** (so MULTI is not graded on what it trained on). Mean firing rate across P_test + per-paraphrase.
- **L1 took (control):** canonical top-1 = target (edit installed).
- R14 oracle: `exact_substring` on target first-token, top-1, frozen here.
- Templates (frozen): canonical `"The capital of {} is the city of"`; **P_train** = [`"{}'s capital is the city named"`, `"The capital city of {} is"`]; **P_test** = [`"{}'s capital city is called"`, `"If you visit {}, its capital city is"`, `"The main city and seat of government of {} is"`].

## Controls
- **NOVEL HALT-gate:** pre-edit fictional-capital base rate ≈ 0 (clean headroom; else the fictional subject has a spurious prior).
- **P_test target-base ≈ 0 in BOTH arms (pre-edit):** the target must NOT already win the held-out paraphrases before editing (PRIOR pre-edit paraphrase fires the *true* capital so target-base ~0; confirm, don't assume).
- **PRIOR native-paraphrase validity:** unedited real countries fire on P_test natively (probes valid) — R13-style check.
- **L1 took ≥ ~90% all arms** (else an arm's low paraphrase = failed edit, not failed generalization → flag).
- **Mechanism diagnostic (PRIOR-only, R13 gap now closed):** log what PRIOR paraphrase-failures output — % revert-to-TRUE-capital vs other. (No "true" capital for NOVEL → runner must not choke on NOVEL here.)
- **Stats:** per-arm CIs (N≈16 → wide binomial); the competitor contrast is huge (~22 vs ~79) but the rescue contrast may be smaller → frame rescue **directionally**, not as a point estimate.

## Pre-committed reads (able-to-fail; this CAN fail the thesis)
- **NOVEL ≫ PRIOR (single recipe):** confirms R13's native-competitor mechanism (isolated within-protocol) → "editing against priors is the problem, novel facts generalize." Reassures the thesis *for novel facts*.
- **⚠ NOVEL also low (single):** then edit-overfit is **generic**, not competitor-driven — a STRONGER threat to the paradigm payoff (even novel in-weight facts are trained-prompt parrots).
- **MULTI rescues (esp. PRIOR+MULTI ≈ high):** a generalization-aware recipe **produces usable in-weight knowledge** → the deployment recipe can be fixed → reassuring; concrete recipe amendment for F1.
- **⚠ MULTI does NOT rescue:** in-weight edits can't be made paraphrase-robust by training on paraphrases → sharp threat to in-weight serving of *usable* reads → strengthens side-store delegation (B3N).
- Degenerate (NOVEL HALT base≠0, or L1-took low) → HALT/flag.

## Scope
band[4-8]/3B/N≈16-per-arm/capital/single-batch/1-seed. NOT promoted without close-out + advisor + cross-family. The mechanism diagnostic (do PRIOR paraphrase-failures revert to the TRUE capital?) **will be logged this time** (R13 gap).

## Artifacts
Runner `experiments/track_c/r5_paraphrase_robustness.py` (adapts r13); result `results/r5_paraphrase_robustness.json`.
