# C1 true-scale — substrate-feasibility DIAGNOSTIC (city→country) — NOT a corruption datapoint

**Date:** 2026-06-25. **Class:** DIAGNOSTIC (harness/substrate feasibility; advisor-directed). **NOT** a C1 corruption result, **NOT** a promoted node, **NO** D-ID-as-corruption (the N=2000 collapse is weight-destruction, not compaction corruption — see below). **Operator scope:** "pilot first" (chosen 2026-06-25). **Artifacts:** `results/c1_scale_city_country_screen.json`, `results/c1_truescale_N2000_diag.json`, `results/c1_conditioning_diag_fixed.json`, `results/c1_diag_singletoksubj.log`, `results/c1_truescale_substrate_diagnostic.json`. **Pre-reg (pilot):** `docs/C1_TRUESCALE_PILOT_PREREG.md`.

## Goal
Take the true-scale C1 fork (B3N condition 3: does compaction stay clean at the spec's ≥2,000-edit drift regime?). The long-standing gate is the **stimulus pool**: C1-(a)'s real-country pool caps at 78 entities. Advisor-mandated constraints: **real native knowledge** (not fictional — phenomenon-swap) and a **single high-cardinality relation** (not multi-domain — would dilute per-relation concentration, the false-negative trap). Candidate: **city→country** (single-token country values, thousands of cities).

## What happened (cheap-gates-expensive sequence, advisor-steered)
1. **Screen (CPU/GPU-light):** Qwen2.5-3B natively knows **2,631** city→country facts single-token + confident (3,642/6,000 correct), 725 conf≥0.8, 107 countries. Looked like N→2,000 was unblocked. **But native-knowledge is necessary-not-sufficient for an EDIT substrate.**
2. **Pilot N=2,000 single-joint-solve:** **total collapse** — edit-expr 0%, held-out 100%→0%, model emits **"!" for every input**, ΔW blow-up. Cost anchor: **62 min/run, 8.4 GB VRAM**. The validity gate (expr≥85%) failed → not a corruption datapoint.
3. **Discriminating ladder (advisor's split):**

| subject | N | ΔW_norm | expr% | held-out% | garbage% | read |
|---|---|---|---|---|---|---|
| multi-token | 2000 | blow-up | 0 | 100→0 | all "!" | COLLAPSE |
| multi-token | 100 | **8900** | 0 | 0 | 64.5 | COLLAPSE |
| single-token | 50 | **207** | 42 | **100** | 0 | clean, under-expressed |
| single-token | 100 | 294 | 27 | 86.7 | 0 | clean, expr falling |

## Two independent walls (both confirmed)
- **Wall 1 — multi-token subjects break the solve.** Most cities tokenize to 3–4 tokens (census: only **115/2,631 single-token**, 731 ≤2-token). Multi-token subjects → key collinearity → ill-conditioned AlphaEdit closed-form → **ΔW blow-up (8900 vs 207)** → model emits garbage "!". The N=2,000 collapse is this, at scale — **weight destruction, not knowledge corruption** (C1-(a) corruption looks like held-out flipping to *wrong-but-real* countries at 73%, never 0%/garbage). So it is **not** a "single-solve-doesn't-scale" or spec-validating finding.
- **Wall 2 — strong-prior counterfactual under-expression.** Even clean single-token-subject edits express only **27–42%** (falling with N) — city→country counterfactuals (overwriting Tokyo→Japan with a false country) fight an entrenched pretrained prior (the **R5/R13 counterfactual-over-prior fragility**, CORPUS/28–29). Below the ≥85% expression anchor → under-editing confound → invalid for a corruption study regardless of subject cleanliness.

## Conclusion (for F1 condition C1)
**city→country is NOT a viable C1 true-scale substrate.** The native-knowledge screen was necessary but far from sufficient: an edit-corruption substrate must *simultaneously* satisfy **single-token value + clean (≤2-tok) subject + EXPRESSIBLE counterfactual + cardinality ≥2,000 + native knowledge**. Clean-subject single-token relations cap low (country→capital 78; element→symbol ~118); high-cardinality relations carry multi-token subjects + strong priors. **True-2,000-scale single-relation high-concentration C1 with real native knowledge remains substrate-gated** — the 78-entity country pool (C1-(a), N≤100) stays the clean evidence ceiling. This tightens *why* B3N condition 3 is hard to falsify empirically, and means the C5 Prediction-B′ livelock (routed here) stays a **prediction**, not empirically resolvable with this recipe + available substrates.

## Value / process
The **pilot-first + cheap-diagnostic discipline (advisor-steered) prevented a 4–10-day GPU grid on a broken substrate** — the correct outcome of "verify the substrate before committing GPU." Negative-but-informative: the gate isn't GPU hours, it's substrate editability.

## Options surfaced to the operator (NOT auto-chosen — substrate strategy is the reserved call)
1. **Accept the ceiling:** C1-(a) (N≤100) is the evidence ceiling; route 2,000-scale to *prediction* status (B3N cond-3 + C5 B′ stay open-untested). No further GPU.
2. **≤2-token-subject extension:** test whether the ~731 ≤2-token cities give a usable N (likely still expression-limited by Wall 2 — cheap to check, ~1 run).
3. **Build a clean-subject pool across a few single-token relations** (country→capital/language/currency/continent + element→symbol …) — risks the concentration-dilution trap (advisor); needs an expression-rescue (novel-insert framing loses the native-corruption phenomenon).
4. **Recipe work to lift expression / condition the multi-token solve** (more steps, scaled ridge / diagonal-add per `[[wide-intermediate-7b-editing-vram]]`, relation-balanced keys) — a research detour with uncertain payoff.
