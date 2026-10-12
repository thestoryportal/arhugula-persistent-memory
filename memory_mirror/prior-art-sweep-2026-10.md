---
name: prior-art-sweep-2026-10
description: "Prior-art sweep (Oct 2026): 2026-10-04 search found no coined multi-word locate-then-edit match; keying-locus support; Super Weight trap"
metadata:
  type: reference
---

**Repo doc:** `docs/PRIOR_ART_SWEEP_2026-10-04.md` (full tags, repo table, synthesis §3, reading queue). Companions: [[prior-art-lre-hernandez-2024]], [[prior-art-anyeditpp-2026]].

**What to recall:**
- **Keying locus (Q1):** PRISM Edit (2607.11327): subject-last-token MLP input invariant across contexts, cos ≥ 0.97. ALOE (2609.29269): paraphrase failure is address-side (gate fires 0.057 on rephrasings vs 0.860 originals). Suresh et al. AlphaEdit reproducibility (2606.26783): **subject-keyed AlphaEdit on Qwen2.5-3B = 99.8 % efficacy, 90–96 % ZsRE paraphrase generalisation; hyperparameters "required manual derivation" per architecture.** External support for Route A's F3/F5 (CORPUS/42–43).
- **Hparam non-transfer (Q5):** Anand et al. (2609.29587): AlphaEdit at published settings collapses Qwen2.5-7B-Instruct MMLU to chance at 1k edits while locality passes.
- **Covariance corpus (Q4/Q5):** Moir (2607.20433): self-generated-text covariance instead of Wikipedia; Qwen3-8B GSM8K 79.9 % vs 10.9 % after 20k AlphaEdit edits. Cheap local knob for the program's own cov cache.
- **Metrics:** KLOD strict multi-token reliability (= full-sequence criterion); HPSE decomposition probes; GLIME TF-vs-AD caution; ForgetBench half-life/paraphrase gap.
- **Lifecycle (Q6):** PRISM (update w/o overwrite), edit reversal 2609.02091 (forget), Pitfalls Round-Edit (integrity, data-only, MIT), ForgetBench (Apache-2.0, runs offline), Awesome-AI-Memory taxonomy ("parametric memory … not directly editable" = the claim F1 contests).
- Only Suresh et al. test a 3B base model with locate-then-edit; no local-faithful long-form editor exists; EasyEdit bundles AnyEdit without MPS. `HvSytvg3Jh` (OpenReview) unfetched (challenge wall).

**Addenda 1–10 (same day, 2026-10-04; full text in the repo doc §4–§13). What still steers work:**
- **The 2026-10-04 search found no matching method** after five keyword passes (~90 items, doc §12) for writing coined multi-word values into weights by locate-then-edit and reading them back from held-out paraphrases; this is a bounded search result. A Gemini summary claiming otherwise was checked against sources and NOT SUPPORTED (doc §13).
- **Super Weight trap (doc §7):** Qwen2.5-3B L2 `down_proj[318,3189]` = −0.55; zeroing it → ppl 7.11→15.72. Band [4–8] excludes L2, but the L4 first-token key (norm 98) that dominated Route A's preservation term IS this super activation (`results/superweight_qwen3b*.json`). Before trusting any quantized-survival number, check the GGUF export preserves that scalar.
- **C10 candidate-solution map** (routes ii subject-keyed / iii side-store / iv mint-a-token): doc §9.2 and §10.2.
- **Connected Papers corpus index:** `docs/CONNECTED_PAPERS_GRAPH_INDEX_2026-10-04.md` (88 graphs / 2,123 papers at the last addendum).
