# Top three — research pass 2026-10-06, ordered cheapest test first

All three run on this Mac with the existing C10 harness and model; none is a model change. Each is one page: the hypothesis, why it could cross the bar where the program's own knob sweeps did not, the test as a pre-registration stub (hypothesis, binding count, controls, gates), and what a pass or a fail would change. Full entries are in `hypotheses.md`; thresholds follow its conventions.

---

## 1. H-1 — Shared value objective across prompt formats (one harness pass, about 35 minutes plus the LAW#5 check)

**Hypothesis.** The `compute_z` target for each coined fact is optimised jointly over the canonical prompt and two training paraphrase forms (one subject key, one z per fact), not on the canonical prompt alone.

**Why it could cross where the sweeps did not.** Every knob the program swept (band placement and width, strength, layer count, projector, sparse sets, two-pass and stacked re-solves; CORPUS/37–39, 44, 49–50) changed how the same canonical-frame target is realised. The one arm that changed what the target must satisfy (c10c, CORPUS/35) did it by adding paraphrases as extra requests and was swamped by interference at 3× the request count. MEMIT-XF (`CheongWoong/mf-memit`, EMNLP 2026 Findings) and RoSE's hierarchical integration show that a single value vector fit against several formats carries across formats where a single-format value does not. That is the untested half of the program's own result: 24 requests, 24 keys, each z fit to three frames.

**Pre-registration stub.**
- *Binding count:* A7 `para_full` on the three sealed held-out templates, 24 subjects × 3 = 72.
- *Arms:* A (canonical z, same run) vs B (shared z over canonical + two training forms disjoint from the held-out set); A1 and A2 under both.
- *Gates:* fingerprint `d941a9fb`; LAW#5 inertness of the `compute_z` prompt-set seam at its default; A1, A2 ≥ 68/72; L1 ≤ A + 1; `described_as` ≥ A − 3; L3 ≥ 29/30; same-frame ≤ A + 1; perplexity rise ≤ 0.5; ΔW ratio ≤ 1.5.
- *Labels:* LEAD ≥ 30/72; PARTIAL gain ≥ 10 with a gate miss = TRADEOFF; NULL otherwise. Route-level pass ≥ 61/72.
- *Pre-registered prediction to beat:* the identical-baseline envelope [5, 18]/72.

**Pass changes:** the wall is partly the frame the target was fit in; the engine-path arms I-1/I-2 are re-ordered behind a cheaper fix and the shared-z becomes the default target for every later arm. **Fail changes:** the frame account is closed on this harness and the realisation account (H-3, I-2) is the only live engine-side route.

---

## 2. H-18 — Minted token written by embedding-only tuning (minutes of training plus one mint pass, under an hour)

**Hypothesis.** For the minted value token of CORPUS/45, training only the minted row by gradient descent on paraphrase-diverse text with the rest of the model frozen gives a higher held-out count than the closed-form MEMIT write of the same row.

**Why it could cross where the sweeps did not.** The mint arm is the only coined-value arm above 30/72 (34–46 across five replicates), and its residual gap to A1 (68–72) did not move with row initialisation (G ≈ N) and was seed-sensitive. Every mint arm wrote the row through the solve, which fits one canonical frame at one position. Memory as a Markov Matrix shows a new token's embedding can be tuned with zero change to transitions among old tokens and with sample complexity linear in the tokens it maps to; neologism learning and Concept Tokens show one row's d parameters, trained frozen-model, carry a concept across phrasings. Here the new token is the value, not the subject, which sidesteps Concept Tokens' warning about novel factual detail.

**Pre-registration stub.**
- *Binding count:* post-write top-1 minted id at the value slot on the 72 held-out prompts, minus step-0 recall (0/72), as in CORPUS/45.
- *Arms:* A7-mint-N (MEMIT write, same run) vs A7-mint-N-tuned (row trained on 24 × ≈ 20 generated phrasings; held-out templates sealed; a few hundred steps; model frozen); A1 under both. Two N seeds, since CORPUS/46 showed seed sensitivity.
- *Gates:* fingerprint; P2 registration inert (233/233 tokenisations unchanged); P3 admission; sibling 0 and cannibal 0; A1 ≥ 68; L1 0/12; L3 ≥ 29; `described_as` ≥ A − 3; P4 GGUF chain: minted id tokenises 24/24 in both GGUFs.
- *Labels:* pass ≥ 56/72 (best mint replicate plus the 10/72 rule) on both seeds; route pass ≥ 61/72; NULL inside [34, 46].

**Pass changes:** the residual gap was in how the row was written, not in the novel pair; the mint route becomes the lead in-weight route and F-M4 is answered. **Fail changes:** the gap is the pair (H-C10l-pair-novelty), and the predictors (I-4/I-4b) move up.

---

## 3. H-13 — Merged band-LoRA write on paraphrase-diverse synthetic QA (two to three hours; a write-engine replacement, labelled so)

**Hypothesis.** A rank-16 LoRA delta on `down_proj` L4–8, trained with a token-level loss on the coined value across about 20 generated phrasings per fact and merged into the weights, reaches the held-out bar.

**Why it could cross where the sweeps did not.** The closed-form write has no direct objective on value tokens 2 … N (CORPUS/36); a fine-tuning loss has one at every position in every phrasing. The nearest published metric to the program's bar is in this class: exact match on held-out surface templates for anonymised entity identifiers on Qwen3-4B / 1.7B, rising from 76 % to 86 % with LoRA rank while unrelated capability falls (2608.25677); FT-UKE beats locate-then-edit editors with locality tests (2506.09672); paraphrase augmentation lifts new-fact QA toward the open-book bound (2508.06178). The spec excluded fine-tuning as "destructive and not overlayable"; a LoRA delta confined to the band is additive and overlay-representable exactly as ΔW is, which is why this is a challenger and not a side store.

**Pre-registration stub.**
- *Binding count:* A7 `para_full` /72 after merge, greedy, string readout equal to id readout.
- *Arms:* A (closed-form baseline, same run) vs B (merged LoRA r = 16, band only, value-token loss, early stop on training-phrasing EM); A1 and A2 under both; r ∈ {8, 32} only if B is PARTIAL.
- *Gates:* fingerprint on the unmodified engine (the LoRA path is a separate writer; the engine is not touched); A1, A2 ≥ 68; L1, `described_as`, L3, same-frame, perplexity as above; plus a generic-capability probe (the forgetting axis the source measured) with a pre-set floor; ΔW ratio ≤ 1.5 of the closed-form write.
- *Labels:* as H-1. Any pass is recorded as "write-engine replacement" and carries the §8.2 D12 amendment flag; F1 cannot count it as MEMIT.

**Pass changes:** C10 is closable in-weight only by changing the write engine; the spec's D12 and the compaction model (§8.10) go to the operator as amendments, and the genesis question "at what volume is fine-tuning more appropriate" has a first number (N = 24). **Fail changes:** the continuation wall is not a missing-objective problem but a storage one on this model, which strengthens the model-change leads (H-21, H-23) and the mint route.
