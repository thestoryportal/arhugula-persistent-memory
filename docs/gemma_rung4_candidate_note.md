# Gemma 4 — logged RUNG-4 (model-swap) candidate for the Write-Engine Viability program
_Logged 2026-06-17. Governing plan: `write_engine_viability_determination_plan.md` (rung 4 = D12-revisit model swap → Category C / v1.3)._

## Status: LOGGED CANDIDATE — down-ladder, low prior, cheap to probe. NOT a current priority.
Rung 4 is only reached after exhausting milder rungs 0–3 (which preserve the in-weight thesis without a base-model swap). Same-entity non-locality is **model-general** (Gate A + literature + calibrated GATE-CAL v2), so the prior that Gemma 4 escapes the failure under stock MEMIT is LOW. Value = a portable, cheap model-swap data point, especially given Gemma's interpretability tooling (Gemma Scope).

## Sources (primary; verified)
- Official model card: https://ai.google.dev/gemma/docs/core/model_card_4
- Official core docs: https://ai.google.dev/gemma/docs/core
- Official JAX reference library (Gemma 2/3/3n/4): https://github.com/google-deepmind/gemma  ← read for exact MLP/attention/embedding module defs before building MEMIT hparams
- (low-trust: 2026 "complete guide" SEO blogs disagreed with the card on sizes/active-params — do not cite)

## Verified facts relevant to MEMIT
| Variant | Params | Layers | Type | Fits 24GB 4090 fp16 |
|---|---|---|---|---|
| E2B | 2.3B eff (5.1B w/emb) | 35 | dense + PLE | yes ~5GB |
| **E4B** | 4.5B eff (8B w/emb) | 42 | dense + PLE | **yes — 17.9GB BF16 (card accounting); ~6GB headroom ← best fit** |
| 12B Unified | 11.95B | 48 | dense, multimodal | tight ~24GB |
| 26B A4B | 25.2B (3.8B active) | 30 | **MoE (128 experts)** | yes but NOT MEMIT-able |
| 31B Dense | 30.7B | 60 | dense | NO (~62GB; needs quant) |
Also: 262K vocab, hybrid local-sliding+global attention, 128K/256K ctx. NOT on card (verify via HF config / deepmind repo): hidden dim, FFN intermediate, activation (Gemma lineage = gated GeGLU w/ down_proj), embedding tying.

## Assessment
- **MEMIT-compatible (dense only):** edits MLP `down_proj` at a mid-layer band — same target shape as Qwen's `down_proj` (our P-VRAM-CPU-SOLVE already handles this). E4B fits on-GPU → cov solve on GPU, no CPU-solve hack, faster than Qwen.
- **Exclude 26B MoE:** no single MLP per layer under 128-expert routing → MEMIT covariance/solve ill-defined; implicitly violates the spec's MEMIT designation.
- **Watch:** PLE (E2B/E4B per-layer embeddings) and sliding-window attention may affect how the subject representation forms at the keyed layer; logit/attn quirks in the Gemma lineage. Verify before trusting any edit.
- **Genuine plus for the disentanglement angle (rung 3 / DiKE):** DeepMind's **Gemma Scope** (open SAEs on Gemma 2) is the strongest public attribute-disentanglement tooling for any open model — directly relevant to entity-aware projection / representation disentanglement. Confirm Gemma-4 coverage.

## Cheap probe (if/when run): MODEL=gemma4_e4b branch
The calibrated GATE-CAL v2 is tokenizer-agnostic (screener auto-selects confident+correct single-token facts). To probe: add a `gemma4_e4b` branch to `s242_screen.py` + `s242_gatecal.py` (HF id, revision, MEMIT hparams JSON: layer band, `down_proj` module names from the deepmind repo, v_loss_layer, mom2 stats), download E4B (~8GB), build cov cache, run screen → GATE-CAL v2. Expect ~half a day incl. one-time cov cache. EasyEdit (`/workspace/easyedit_assets`) may already have Gemma hparams for GRACE/WISE/AlphaEdit — check first.

---

## RESEARCH INTEGRATION (from `research_and_specs/gemma4_editing_research.md`, 2026-06-17)
Deep-research report landed (well-cited, primary sources only). Key updates to this candidate:
- **VRAM (card accounting, high conf):** E4B BF16 = **17.9 GB** (NOT ~8GB — earlier error). E2B 11.4GB, 12B 26.7GB, 26B 57.7GB, 31B 69.9GB. So on 24GB: E4B fits with ~6GB headroom → cov solve may be tight; **may need CPU-solve like Qwen** (re-use P-VRAM-CPU-SOLVE), not on-GPU as first thought.
- **Exact E4B arch (HF config, high conf):** 42 layers, hidden 2560, FFN intermediate 10240, 8 heads/2 KV, head_dim 256, tied embeddings, PLE on (`hidden_size_per_layer_input=256`), `use_double_wide_mlp=false`, `final_logit_softcapping=30.0`. MEMIT target = **`model.layers.{i}.mlp.down_proj`** (HF) / `linear` in FeedForward (JAX). Gated GELU (gate/up/down). Our JS-over-softmax metric is robust to the logit soft-cap (we read output probs).
- **PLE caveat (NEW, important):** E2B/E4B inject per-layer token embeddings OUTSIDE the residual stream ROME/MEMIT tracing assumes → may confound causal tracing / the subject representation MEMIT edits. **12B Unified has PLE=0** (cleaner target) but is 26.7GB (no 24GB fit). Tension: E4B fits-but-PLE vs 12B clean-but-too-big. Consider E2B (11.4GB, also PLE) as a smaller probe.
- **EasyEdit correction:** Gemma appears only in EasyEdit2 steering / UltraEdit — NOT in classic ROME/MEMIT/GRACE/WISE/AlphaEdit hparams. Gemma 4 MEMIT needs a **fresh hparam search** (layers band, cov dataset, rewrite templates), not config reuse.
- **Use BASE not -it:** the configs studied are instruction-tuned (`-it`); for editing use the base checkpoint (cleaner factual localization), as we do for GPT-J/Qwen.
- **Only Gemma editing datapoint:** AlphaEdit Table 3 reports MEMIT on "Gemma"/CounterFact (eff 64.68, spec 46.73 — CROSS-ENTITY) improved by AlphaEdit (75.21/52.63). Variant unspecified. No same-entity Gemma evidence exists anywhere.
- **Report's predicted bottom line:** Gemma 4 likely INHERITS the model-general same-subject non-locality unless the editor explicitly separates target vs irrelevant same-subject components (DiKE-style). Decisive step = a primary E4B experiment, not more review.
- **Newly surfaced published work directly mapping to our ladder:**
  - **DiKE** (arXiv 2505.18774) — decompose subject repr into target/irrelevant, closed-form rank-one update preserving same-subject knowledge = a PUBLISHED instantiation of our **rung 3** (entity-aware projection). Read for rung 3.
  - **S2RKE** (arXiv 2502.06868) — "same-subject related knowledge editing" = our exact same-entity axis; potential external benchmark.
  - **MEMIT-Merge** (2502.07322) — same-subject batch conflict (relevant to sequential same-subject cell).
  - **MoEEdit** (arXiv 2602.10965) — routing-stable per-expert null-space editing (only path if we ever target 26B MoE).
- **Independent validation:** the report's recommended first experiment (country same-entity holdouts: currency/continent/language/demonym/…, compare MEMIT vs AlphaEdit vs DiKE) MATCHES our GATE-CAL v2 country design — our stimulus choice is corroborated.

### Reconciliation with OUR live result (important)
The report (and the S2RKE/DiKE/MEMIT-Merge literature) predicts **model-general** same-subject failure. BUT our calibrated GATE-CAL v2 (2026-06-17) found a **real model difference**: on the identical clean country stimulus, **Qwen2.5-7B is markedly same-entity-LOCAL** (counterfact capital→Cairo: 5/6 ≈ 0.002 JS, ~99.8% locality, resists even destructive edits) while **GPT-J is NOT** (≈0.19, down to 44% locality). Greece is Qwen's lone exception (0.30). If this holds in Phase 1 (more attribute types + sequential same-subject edits + more entities), it would be a NOVEL result the literature has not established — and would raise the prior that some models (possibly Gemma) can be same-entity-local in-weight. This is exactly why the cheap Gemma 4 E4B probe is now MORE interesting: we have a calibrated metric that already discriminates GPT-J (fail) from Qwen (pass).

---

## PERPLEXITY DEEP-RESEARCH PROMPT (Gemma family × our spec goal)
_(copy-paste into Perplexity; see also chat)_

> **Role & goal.** You are a research assistant for a project determining whether an *in-weight*, *MEMIT-class* (locate-and-edit, parameter-modifying), *entity-centric* knowledge-write engine can achieve **same-entity multi-attribute locality** — i.e., editing one attribute of an entity (e.g., a country's capital) must NOT corrupt that entity's OTHER attributes (its currency, continent, language). This "same-entity locality" is distinct from the usual cross-entity/neighborhood "locality" reported in editing papers. We are evaluating Google's **Gemma family (especially Gemma 4)** as a possible base model. Conduct deep research and answer with **primary sources** (peer-reviewed papers, arXiv, official model cards/tech reports, official code repos). Flag and avoid SEO/marketing blogs. For every claim, cite the source and note its strength; explicitly say when something is unknown or unverified.
>
> **1. Exact architecture (per Gemma 4 variant: E2B, E4B, 12B Unified, 26B A4B MoE, 31B dense), and Gemma 2/3 for lineage.** Number of layers, model/hidden dimension, MLP feedforward intermediate size and activation (confirm gated GeGLU with gate/up/down projections, and the exact module name of the down-projection), attention (sliding-window vs global interleave, GQA head config), normalization (RMSNorm placement), embedding tying, per-layer embeddings (PLE) mechanics, vocab/tokenizer (262K). Pull from the model card, the Gemma 2/3/4 technical reports, the HuggingFace `config.json`, and github.com/google-deepmind/gemma.
>
> **2. Knowledge-editing results ON Gemma.** Has ROME, MEMIT, AlphaEdit, PMET, EMMET, WISE, GRACE, or MEND been applied to any Gemma (2/3/4)? Report efficacy, specificity, and especially LOCALITY results — and whether any work measured *same-entity / ripple* effects (e.g., RippleEdits, MQuAKE) on Gemma. Note framework support (EasyEdit, etc.) and whether published hyperparameters exist for Gemma editing.
>
> **3. Knowledge localization & causal tracing in Gemma.** Where do factual associations live (which layers / MLP modules) per causal-tracing or related studies? Any quirks (logit soft-capping, sliding-window attention, large vocab) that complicate causal tracing or MEMIT covariance estimation on Gemma?
>
> **4. Representation disentanglement / polysemanticity (decisive for us).** What does mechanistic-interpretability work — especially DeepMind's **Gemma Scope** sparse autoencoders — show about how *entity attributes* are represented in Gemma? Is there ANY evidence that distinct attributes of the same entity occupy more separable / less polysemantic subspaces in Gemma than in GPT-J / Llama / Qwen / Mistral? Is Gemma a good substrate for disentanglement-based editing (e.g., DiKE) or null-space/orthogonal-projection editing? Does Gemma Scope cover Gemma 4?
>
> **5. Editing Mixture-of-Experts.** State of the art on applying MEMIT-class editing to MoE models — is the Gemma 4 26B (128-expert) editable in a locate-and-edit paradigm, and how is the per-expert/routing covariance problem handled, if at all?
>
> **6. Comparative amenability.** Synthesize: is Gemma more or less amenable to in-weight knowledge editing and (separately) to *same-entity* locality than GPT-J-6B, Llama-3.x, Qwen2.5-7B, Mistral-7B? Is there a mechanistic reason to expect a difference, or is same-entity non-locality model-general for subject-token MLP editing?
>
> **7. Practical.** For a single 24GB GPU: which Gemma 4 variant is the best MEMIT target (compute + clean dense MLP)? HuggingFace `transformers` support status for editing Gemma 4; tokenizer single-token behavior for short factual answers (capitals, currencies, languages).
>
> **Output:** a structured report by section (1–7), each claim cited, an explicit "what is unknown / needs primary experiment" list, and a one-paragraph bottom line on whether Gemma 4 is a promising base model for an in-weight same-entity-local write engine, or whether the evidence predicts it inherits the model-general failure.
