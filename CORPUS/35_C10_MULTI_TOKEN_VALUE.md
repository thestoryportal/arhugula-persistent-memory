# CORPUS/35 — C10: multi-token VALUE expression at the batch path (FALSIFIER FIRES, scoped)

**Decision-ID:** `D-C10-1`. **Date:** 2026-06-25. **Pre-reg:** `docs/C10_MULTI_TOKEN_VALUE_PREREG.md` (frozen + 2026-06-25 addendum). **Runners:** `experiments/track_c/c10_multitoken_value.py` (Run 1) · `experiments/track_c/c10b_novel_multitoken.py` (Runs 2+3). **Results:** `results/c10_multitoken_value.json` · `results/c10b_novel_multitoken.json`.
**E2e-map cell:** §8.9 write/firing (multi-token value robustness); F1 condition **C10**; on the critical path for the fixed deployment target (`local Intel CPU + batch writes`). **Class:** **FALSIFIER — fired (can-fail; decisive).** NOT promotable as a universal law (scope below); a scoped write-robustness falsifier for the fixed target. **Verdict: C10 FALSIFIER FIRES — arbitrary (non-prior-coherent) multi-token values do NOT generalize to held-out prompts.**

## One arc, three runs (lead with the binding one)
| run | regime | binding metric (held-out-paraphrase FULL-SEQ) | role |
|---|---|---|---|
| **3 — novel INCOHERENT** (the binding test) | fictional subjects; value = 2 unrelated single-tokens ("Amsterdam Ankara") — continuation NOT prior-predictable (code/identifier-representative) | **36.1%** (first-token 70.8%; **P(full\|first)=0.51**) | **THE FINDING** |
| 2 — novel COHERENT (positive control) | fictional subjects; value = real city ("Cape Town", 2.38 tok) — continuation IS a pretrained bigram | **97.2%** (P(full\|first)=1.00) | shows the prior masks fragility |
| 1 — counterfactual (floored, unrepresentative) | real countries; counterfactual capital | SINGLE 12.5% / MULTI 4.2% (both floored) | underpowered; the R13/R5 counterfactual-over-prior effect, NOT token-length |
| (control) novel SINGLE-token | fictional subjects; 1-token value | **97.2%** (P(full\|first)=1.00) | off-floor robustness baseline |

**Mechanism (de-confounded — the conditional is the key number):** single 97.2 ≈ coherent 97.2 ≫ incoherent 36.1. The coherent **positive control** rules out a weak-edit artifact: the *same* recipe hits 97% on prior-coherent values one arm over. **Conditional P(full\|first-token-correct): coherent 1.00 vs incoherent 0.51** — even when the first value-token lands, the arbitrary continuation completes only ~half the time (addresses the cross-family critique that arm C's first-token is *also* degraded, 97→71: the fragility is on BOTH axes — first-token generalization 97→71 AND continuation-given-first 100→51 — net 97→36). LAW#5 gate clean (|Δexpr|=0.0003, |Δloc|=0.53, fuller p-delta+locality gate). Pre-edit base 0/24 all arms.

## Scoped claim (what the contrast licenses — advisor + cross-family calibrated)
**The edit can be FIT but does not GENERALIZE for arbitrary multi-token continuations.** Trained-canonical full-match holds (incoherent 95.8%) — the AlphaEdit solve *can* bind the full 2-token target on the trained prompt — but it does **not transfer to held-out paraphrases** (36.1%). This is the **multi-token instance of the R13/R5 storage-vs-behavior (trained-prompt-parrot) axis** (`[[in-weight-knowing-insert-robust-update-fragile]]`), not a separate surprise: beyond the first token, arbitrary continuations are trained-prompt parrots. The clean framing is *"arbitrary multi-token values don't generalize,"* NOT *"can't store multi-token values."*

## Cross-family review (Perplexity/Sonar — standing rule for a decisive falsifier; codex auth-expired)
Surfaced the central de-confounder (arm-C first-token also degraded → need conditional P(full|first); computed = 0.51, claim survives) and these honestly-carried scope limits:
- **"two cities" ≠ literal code identifiers** — arm C is a CONTROLLED proxy for *non-prior-coherent continuation*, not literal `snake_case`/`paths`. Real code values vary: some carry strong priors (`__init__.py`), some are arbitrary (random IDs). A literal-code-token follow-up would tighten the deployment mapping.
- **N=24 / 1-seed** — the WITHIN-experiment contrast is valid at 1 seed (`[[single-seed-limits-generality-not-significance]]`; full-match 70/72 vs 26/72 is astronomically significant; 61pp ≫ noise); GENERALITY across seeds/models needs replication.
- **prompt-shape overfitting?** — REBUTTED by the coherent control: arms single/coherent generalize fine under the *same* paraphrase set, so the failure is the VALUE, not the prompt form.
- **greedy/tokenization** — same target tokenization across prompts (prompts vary only the prefix); greedy exact-match is a strict-but-standard usability proxy; logprob/forced-decoding would add nuance.
- **algorithm/layer-specific** — scoped to this recipe (AlphaEdit, band[4-8], 3B); a different editor (AnyEdit per-token) is the candidate fix, not a tested escape.

## F1 impact (moves the determination for the fixed target)
- **C10 = OPEN MUST-FIX for `local Intel CPU + batch writes`.** This is the **first condition both on the critical path for the fixed target AND failing.** A fresh code/project DB whose values are arbitrary multi-token strings (file paths, identifiers, multi-word concepts without bigram priors) cannot reliably hold them in-weight via this batch-genesis recipe — they express on the trained prompt but don't fire on natural reads.
- **Named candidate fix:** AnyEdit-style **per-token multi-token editing** (edit every value token, not just the first) — flagged ready-to-port in the prior-art sweep (`[[editing-memory-eval-prior-art-landscape]]`, G7). Single-token + prior-coherent multi-token values ARE robust (97%), so the batch+CPU DB is fine for those value-classes today.
- Composes with the read-contract slice (R13/R5): the multi-token instance of trained-prompt-over-reports.
- Scope tuple: Qwen2.5-3B / band[4-8] / AlphaEdit / N≤100 / single-batch / 1-seed / HF-fp16 / capital-relation. **Q4_K_M survival of multi-token values** (B3 covered single-token only) + **batch-genesis-at-scale** (gated on target fact-count) are downstream follow-ups.

## Honesty / process
Three advisor gates fired and each caught a real error: (1) pre-build design; (2) Run 1 mechanical "SATISFIED" was canonical-only (mis-specified vs my own R13-citation) → corrected to the held-out-paraphrase binding metric; (3) Run 2's 97% was prior-coherence-masked → the incoherent arm flipped the verdict. The session lesson held: run the arm that separates the flattering reading from the real one (`[[spec-coherence-audit-is-circular]]` #4 generalized: name the confound and TEST it, don't caveat it). NOT promoted as a universal law; a scoped, de-confounded falsifier for the fixed target.
