# Hypotheses — research pass 2026-10-06 (D-C10r-rulings-2)

Leads, never evidence. Nothing here was run. Every arXiv id, repository and checkpoint named below was opened in this pass or is carried from the inventory's already-verified list (marked *inv*). The bar is the program's: held-out full-sequence recall of the coined value on 24 subjects × 3 unseen paraphrases (out of 72), with locality scored on the separate axes of CORPUS/44 (L1 real-country flips out of 12, `described_as` JS, L3 unedited-capital top-1 out of 30, same-frame fictional probe out of 6, generic perplexity). A source's "generalization" on CounterFact or zsRE is not that bar and is labelled so in each entry.

## Conventions used in every entry

- **class**: the plan's §1a taxonomy (E1–E9, M1–M5).
- **cheapest test**: what would run on this Mac (M3 Pro, 48 GB, MPS), on which arms, how long, with pre-registerable numbers. Shared thresholds taken from the harness after CORPUS/44–50: identical-baseline envelope for A7 `para_full` [5, 18]/72 and canon [5, 10]/24; LEAD ≥ 30/72; PARTIAL or TRADEOFF needs a gain ≥ 10/72 over the same-run baseline; route bar ≥ 61/72 (85 %); controls A1 and A2 ≥ 68/72; locality gates L1 ≤ baseline + 1, `described_as` ≥ baseline − 3, L3 ≥ 29/30, same-frame ≤ baseline + 1, perplexity rise ≤ 0.5; write-size qualifier ΔW ratio ≤ 1.5× the single edit (CORPUS/50). Timing anchors: one full harness pass (A1 + A2 + A7, N = 24, band 4–8) ≈ 33 min (CORPUS/50: three passes in 02:15–03:54); one injection cell ≈ 40 min (CORPUS/47); the GGUF chain ≈ 2 min (CORPUS/45). Covariance for a new model band took about 70 min on the lost 4090 (CORPUS/04:33); no M3 Pro timing exists, so every model-change test carries "covariance time unmeasured".
- **would-advance**: the F1 condition or spec obligation moved. C10 is the OPEN/BLOCKING multi-token value condition; §C is the write path; §F / §8.9 is the L2 behavioural probe; Part V open questions are OQ-W1 (thresholds) and OQ-W2 (MEMIT / architecture compatibility).
- **spec-amendment**: none, or the section that would change. A continued-pretraining or fine-tuning route replaces the §8.2 D12 write engine and the entry says so.
- **feasibility**: `static` (prefilter arithmetic only) or `empirical` (an existing run on this Mac, cited). The prefilter uses the edited matrix: the harness edits `down_proj`, whose input dimension is the MLP intermediate size, so one fp32 covariance or projector is intermediate² × 4 bytes (Qwen2.5-7B: 18,944² ≈ 1.34 GiB each, CORPUS/41; Qwen2.5-3B: 11,008² ≈ 462 MiB).
- **source-metric**: what the source reports and its distance from our bar.
- **disposition**: `candidate` / `candidate-needs-C10-eval` / `lead` / `fallback` / `empty` as the plan's §4 defines them. This pass runs nothing, so a new model is at most `lead`.

Entries are grouped by class. H-numbers are stable; the ledger nodes in the OpenResearch project carry the same numbers.

## E1 — locate-then-edit, closed form (the current engine's class)

### H-1 Shared value objective across prompt formats
- **class** E1. **claim** One `compute_z` target optimised jointly over several prompt formats of the same fact (one subject key, one z per fact) transfers to held-out phrasings better than the canonical-prompt target, without the request-count interference that sank the program's paraphrase-diverse arm.
- **mechanism** Today z is fit on one canonical prompt under random context prefixes, so the continuation tokens are fit to one frame. MEMIT-XF fits one value vector against a shared objective over six task formats and reports that single-format edits do not carry across formats; RoSE's hierarchical knowledge integration does the same over linguistic forms. The program's c10c arm (CORPUS/35, follow-up) added paraphrases as extra requests (72 instead of 24) and degraded everything through interference. A shared-z arm keeps 24 requests and 24 keys and changes only what each z must satisfy; that half was never run.
- **sources** `CheongWoong/mf-memit` (MIT, pushed 2026-08-28; README read: MEMIT-XF, six formats, CounterFact-1K, Llama-3.2-3B-Instruct, CUDA required; paper "Beyond Paraphrases: Generalization Across Task Formats in Parametric Knowledge Editing", EMNLP 2026 Findings, not on arXiv). RoSE 2603.15518 §5.1–5.3 (*inv*).
- **builds on / contradicts** Builds on CORPUS/35 c10c (interference at 3× requests) and CORPUS/29 R5 (diversity, not intensity, partially rescues). Contradicts nothing.
- **cheapest test** One harness pass, A1 + A2 + A7: `compute_z` prompt set = canonical plus two training paraphrase forms (disjoint from the three sealed held-out templates), one z per fact; same-run canonical baseline. About 35 min plus the LAW#5 inertness check (the change touches `compute_z` inputs, so it is science-path and runs isolated). Pass: A7 ≥ 30/72 with controls ≥ 68 and all locality gates; route pass ≥ 61/72. Fail: ≤ 18/72 or any locality gate miss.
- **would-advance** C10; §8.9 L2. A pass says the wall is partly the frame the target was fit in.
- **spec-amendment** none. **feasibility** empirical (harness, model and caches exist, CORPUS/44–50).
- **source-metric** MEMIT-XF: cross-format accuracy on real CounterFact entities, first-token; RoSE: paraphrase top-1 on same-subject real facts. The design transfers; the numbers do not.
- **disposition** candidate-needs-C10-eval.

### H-2 Robust-key adapter (REP)
- **class** E1 (keying). **claim** A small gated projection trained to pull same-subject paraphrase keys toward the injected key makes the subject key phrasing-invariant and raises held-out transfer.
- **mechanism** The paper shows whitened key similarity of one subject under rephrasing drops below 0.4 (random level) and that locate-then-edit keys cannot be both robust and specific; REP adds a gated projection on the MLP input, trained with a contrastive aggregation loss plus a target-consistency loss, then edits as usual. On Llama2-7B CounterFact, MEMIT's rephrased-subject success rose 73.3 → 89.9 with a 0.4 locality cost.
- **sources** 2410.09338 §5, §7.2, §8, §9, §11 (read). Code `ElliottYan/RobustKeyEdit` (pushed 2025-05-26; `memit_main.py` hard-codes `cuda:` device strings at lines 50, 63, 140, 314).
- **builds on / contradicts** Builds on CORPUS/43 (subject keying transfers single-token values) and closes inventory gap item 8 (this paper is now read). It does not address the continuation wall.
- **cheapest test** Step 0, no write, about 20 min: whitened cosine of each A7 subject's key at band layers under the three held-out templates against the canonical key (REP §7.2's measurement, on the keys the harness already caches); if coined subjects already sit above 0.8 the hypothesis is dead for this stimulus. Step 1 only if step 0 is live: train the adapter on training paraphrases, one harness pass, gates as H-1. The adapter is an inference-time module on the key path and cannot be folded into the `down_proj` overlay; flag for the operator.
- **would-advance** C10 addressing side; OQ-W2. **spec-amendment** §8.2 would have to admit a parametric key adapter beside MEMIT if step 1 is adopted.
- **feasibility** empirical for step 0 (CORPUS/43 `keygram.json` machinery); step 1 is a small MPS training loop.
- **source-metric** first-token success under subject rephrase, shuffle and long context on real entities; single edits. Not the bar.
- **disposition** lead.

### H-3 Direct end-to-end ΔW optimisation over the band
- **class** E1. **claim** Optimising the band's ΔW directly against the target, instead of spreading a last-layer residual through per-layer closed-form solves, realises the target at the keyed position and carries the continuation.
- **mechanism** CORPUS/44 step 0 found the edit realises its own z to about 3 % at the keyed position while injecting that z gives 49/72; CORPUS/47–50 found the edited model decodes a rotated, longer target. DOW-KE names the same defect in anchor-based pipelines (a reported gap of about a third of the residual left unrealised) and replaces anchor targets with direct multi-layer weight optimisation under spectral projections (Llama-3-8B CounterFact efficacy 99.85, generalization 96.64, specificity 78.86).
- **sources** 2608.16932 (*inv*, read in the 2026-10-04 sweep §1.2). No code located by `gh search` in this pass.
- **builds on / contradicts** Builds on CORPUS/44 F-A3, CORPUS/46 H1, CORPUS/48 DIRECTION; it is the engine-path counterpart of the re-aim family (CORPUS/49–50, 24/72).
- **cheapest test** Implement direct ΔW optimisation on `down_proj` L4–8 for the 24 requests with the AlphaEdit projector applied as a constraint and the same locality battery; backprop through the 3B model on MPS (fp16 weights, fp32 ΔW). About one day of code, one pass ≈ 1–2 h. Gates as H-1 plus the write-size qualifier. Science path: LAW#5 isolation against the K1 ceiling (CORPUS/43) first.
- **would-advance** C10; the sharpest test of the realisation account. **spec-amendment** none.
- **feasibility** empirical for model and probes; the optimiser is new code.
- **source-metric** CounterFact first-token metrics on real entities. Not the bar.
- **disposition** lead (no code; strongest mechanistic match in the pass).

### H-4 Covariance from model-generated text (Moir)
- **class** E1. **claim** Covariance from the model's own generations instead of Wikipedia changes which key directions the projector protects and lifts transfer for coined subjects, which lie outside the Wikipedia distribution.
- **sources** 2607.20433 (*inv*). **builds on** REG:300 and CORPUS/43 ("neither motivated nor excluded"); the harness solve ignores `mom2_update_weight` but uses C through the projector (ARC §12).
- **cheapest test** Generate about 2 h of model text on MPS, recompute the five band covariances (70 min on the 4090; unmeasured here), rebuild the projector with its SHA in the manifest, one harness pass, gates as H-1.
- **would-advance** C10 addressing side; OQ-W1. **spec-amendment** none. **feasibility** empirical (pipeline exists; time unmeasured).
- **source-metric** capability retention under thousands of sequential edits on 7–8B models. Not the bar.
- **disposition** candidate-needs-C10-eval (low prior for the continuation wall).

### H-5 Leverage-score pivot key inside the value (ManiEdit) as a second key beside the subject key
- **class** E1/E3. **claim** Adding one more key per fact at the value-internal position with the largest leverage score kᵀΣ⁻¹k (a position the covariance protects least) gives the continuation a direct write without the collinearity of frame tokens.
- **mechanism** ManiEdit chooses "semantic pivot" keys by leverage against Σ and reports the strongest sequential unstructured results on Qwen2.5-7B-Instruct; the program's CORPUS/43 keygram showed frame keys are near-collinear (cosine ≥ 0.985) while subject keys are not, and leverage against Σ is the rule that would pick a non-frame position inside the value.
- **sources** 2609.33534 (*inv*, abstract and eval read in the 2026-10-04 sweep); `Areyliu/ManiEdit` (Apache-2.0, pushed 2026-09-28; 48 GB GPU stated).
- **cheapest test** Step 0 offline (minutes): leverage scores of every A7 value-token position under the band covariance; if the maximum falls on the subject itself the hypothesis adds nothing. Step 1: one harness pass with two keys per fact (subject-last and the pivot), 48 keys; gates as H-1 plus the same-frame probe, since value-internal keys are the frame-bleed risk CORPUS/43 measured.
- **would-advance** C10. **spec-amendment** none. **feasibility** empirical (keys and covariance cached).
- **source-metric** BERTScore and ROUGE on paraphrase questions of long passages. Not the bar.
- **disposition** lead.

### H-6 Per-position-per-layer value write with gated application (GenRecEdit)
- **class** E1/E3. **claim** Writing token p of the value at its own layer with one-one triggering (position p activates only layer l_p's edit) avoids the annihilation of concurrent per-position edits and carries 4–6-token values.
- **mechanism** GenRecEdit's ablation: without one-one triggering, IID Ratio@10 falls 0.7359 → 0.0030; its cold-start items are unseen 4-token codes written by the MEMIT closed form into a frozen model.
- **sources** 2603.14259 (*inv*); `Starrylay/GenRecEdit` (pushed 2026-04-29; T5-based).
- **builds on** PAS §9.2 option (ii-a), never run. **cheapest test** A7 with the value's tokens 2…k written at layers 5…8 under subject keying with a position-indexed gate in the harness (a scheduler around the vendored solve), one pass; gates as H-1. About two days of harness work.
- **would-advance** C10. **spec-amendment** none (gate is harness-side at compile; inference-time gating would need §8 wording). **feasibility** empirical for the solve; the scheduler is new code.
- **source-metric** recommendation ranking on item codes; paraphrase never tested. Not the bar.
- **disposition** lead.

## E2 — sequential / lifelong null-space editors

### H-7 BetaEdit as the engine for the incremental write path, with a C10 arm first
- **class** E2. **claim** BetaEdit's history-aware null space (projector over pretrained and all previously edited keys, refreshed every τ edits, plus a leakage penalty λ₁) keeps A1/A2 clean over many sequential writes on Qwen2.5-3B; on A7 it behaves like the current engine, because its key is the same subject token and its target the same z.
- **mechanism** §6 of the paper: Δ = R Kᵀ P (λ₂ I + (K Kᵀ + C) P)⁻¹ with C = λ₁ K₀K₀ᵀ + Σ previous K_i K_iᵀ; §8 (Limitations): anchoring at the last token "drastically reduces" effectiveness (Table 3: efficacy 22–39 % at 300 edits vs 80–96 % subject-anchored), which is the program's CORPUS/43 finding in the authors' own words. The method changes protection, not what the continuation tokens receive.
- **sources** 2605.09285 §6, §7.1, §7.2, §8 (read); `lbq8942/BetaEdit` (pushed 2026-09-29; no licence; `configs/llms/qwen2.5-3b.yaml` = Qwen2.5-3B-Instruct, `subject_last`, layers 4–8, `mlp.down_proj`, mom2 15000, wikipedia 100k; `betaedit.yaml` λ₁ 3000, λ₂ 10, τ 1000, null-space threshold 0.02; device = `cuda if available else cpu` in `betaedit_main.py:156`, `compute_z.py:25`, `load.py:18`, so a one-line MPS device string is the port).
- **builds on / contradicts** Resolves inventory contradiction 1 (see `contradictions.md`); builds on REG:33 (A3 port parked) and CORPUS/16. The config is for the Instruct model; the program's line is base.
- **cheapest test** Single batch, A1 + A2 + A7 through BetaEdit's solve as an alternative harness engine (base model, program's covariance, λ₁ swept {0, 3000}), one pass ≈ 40 min after a half-day port. Expectation: A7 inside the baseline envelope; the informative readout is A1/A2 under 24 → 96 sequential singles against the program's sequential collapse (CORPUS/13: 100 → 41.7 %). Pass for C10: A7 ≥ 30; pass for C1: sequential A1 held-out ≥ 90 % at 96 edits.
- **would-advance** C1 (incremental path) more than C10; OQ-W2.
- **spec-amendment** none (null-space MEMIT family). **feasibility** empirical (model, caches; code read).
- **source-metric** CounterFact and ZsRE efficacy / generality (paraphrase top-1) / specificity over 300–10,000 sequential edits on Qwen3-4B-Instruct, GPT-J, Llama3-8B-Instruct. Not the bar.
- **disposition** candidate-needs-C10-eval (for C1 it is a candidate; for C10 a control).

### H-8 Dynamic per-edit layer selection (LOKI) on the C10 harness
- **class** E2. **claim** Choosing the edited layer per fact by a dependence criterion between key and target (LOKI uses HSIC) instead of a fixed band places coined-value writes where they realise, which the fixed-band sweeps (CORPUS/37–39, 44) never tested.
- **sources** 2606.19679 (abstract read; no code located). Related in the corpus: WilKE per-edit layer selection 2402.10987 (REG:306 H-C10l-wilke-layer).
- **cheapest test** Step 0 (no write): per-subject HSIC between band-layer keys and the target logits for A7 vs A1; if the maximiser is the same layer for all 24, the hypothesis is dead. Step 1: per-fact layer choice in the harness (one hparam file per fact), one pass, gates as H-1.
- **would-advance** C10. **spec-amendment** none. **feasibility** empirical.
- **source-metric** average accuracy over lifelong editing benchmarks; not the bar.
- **disposition** lead.

## E3 — long-form / autoregressive-position editors

### H-9 Subject-anchored per-sentence residual with a temporary carrier (FOVEATED stage 1)
- **class** E3. **claim** One residual per target written at query anchors that exclude the final prompt position, kept distinct across facts by a temporary per-target carrier token, gives the closed-form solve a continuation target that is subject-side and non-collinear.
- **sources** 2610.02772 (*inv*; PDF read in the 2026-10-04 sweep §10.1; no code located by `gh search` in this pass). **builds on** PAS §10.2 option (ii-b), never run; relates to the minted-token arm (CORPUS/45), whose minted row is a permanent carrier.
- **cheapest test** Harness wrapper: anchors = subject tokens, one carrier per value, L4–8 closed-form write, carrier removed after the write; one pass, gates as H-1 plus same-frame. About two days of harness work.
- **would-advance** C10. **spec-amendment** none. **feasibility** empirical for the solve; new code for anchors and carriers.
- **source-metric** ROUGE-L on atomic questions and rephrased queries for counterfactual passages on 7–8B Instruct models. Not the bar.
- **disposition** lead.

### H-10 Surprisal-boundary second key (AnyEdit++) under subject keying
- **class** E3. **claim** The token preceding the highest-surprisal boundary inside the coined value is the strongest control channel for the continuation (the paper's Theorem 5.2); used as a second key beside the subject key, it writes the continuation without losing paraphrase transfer.
- **sources** 2606.01053 (*inv*); `TianSuya/Bayes-Chunk` (verified in this pass: created 2026-01-29, one release commit 2026-05-26, no licence, 2 stars; `memit_ARE_main.py`, `compute_z.py`, `layer_stats.py` hard-code `.to("cuda")`; configs for Qwen2.5-7B-Instruct and Llama3; segmentation module is pure PyTorch and device-agnostic).
- **builds on / contradicts** Resolves inventory contradiction 2 (see `contradictions.md`). The lineage's own key is never the subject (CORPUS/42 F3); this hypothesis keeps the subject key and adds the boundary key.
- **cheapest test** Step 0 (minutes): surprisal profile of each A7 value under the base model; if boundaries fall at the first value token for most subjects, the second key coincides with H-5's pivot and the arms merge. Step 1: one pass with two keys per fact, gates as H-1 plus same-frame.
- **would-advance** C10. **spec-amendment** none. **feasibility** empirical.
- **source-metric** BLEU and BERTScore of the edited passage on the edited prompt; no paraphrase, no locality. Not the bar.
- **disposition** lead.

### H-11 Token-level target reweighting and forward replay (the program's queued I-1 and I-2)
- **class** E3. These two arms (OverTone 2502.00602, forward replay 2605.00358, both *inv*) are already pre-registration-selected (ARC §8; CORPUS/50 "next = research pass, then I-1 / I-2"). This pass found no paper that supersedes them; H-1 and H-3 are cheaper or mechanistically sharper siblings and should be sequenced before them only if the operator accepts that ordering. No new test is proposed here.
- **disposition** candidate-needs-C10-eval (unchanged from the register).

## E4 — hypernetwork editors emitting real weight deltas

### H-12 Hypernetwork that emits a fixed LoRA delta for the fact set
- **class** E4. **claim** A hypernetwork trained on a corpus of facts to emit one LoRA adapter that answers questions about those facts generalises out of distribution better than LoRA fine-tuning and scales predictably; a merged delta for the program's 24 facts is an in-weight write.
- **sources** 2607.19604 (abstract read; MegaWikiQA; no code located). PropMEND 2506.08920 (*inv*; `leo-liuzy/propmend`, MIT, configs for Qwen2.5-1.5B and Llama-3.2-1B; OOD-entity 34.7 % on Qwen2.5-1.5B base).
- **builds on / contradicts** PAS §8.1 (PropMEND's unseen-entity cliff mirrors the program's 19–31 %). A hypernetwork needs training on thousands of facts before it can emit a delta for 24 coined ones; the program has 24 facts.
- **cheapest test** None that is cheap: training even PropMEND's editor is a multi-hour GPU job and MPS support is unverified. Static: lead only. If ever run, the delta is merged into `down_proj` and judged by the standard pass.
- **would-advance** C10; §8.2 (a trained editor is a different engine). **spec-amendment** §8.2 D12.
- **feasibility** static. **source-metric** propagation-question accuracy on real and synthetic entities; not the bar.
- **disposition** lead (fallback if the emitted delta is applied at inference instead of merged).

## E5 — LoRA / merged-adapter writes

### H-13 Merged band-LoRA write trained on paraphrase-diverse synthetic QA for the 24 facts
- **class** E5. **claim** A low-rank delta on `down_proj` L4–8 (or on the band's MLPs), trained with a token-level loss on the coined value across many generated phrasings and merged into the weights, reaches the held-out bar where the closed-form solve reaches 12–24/72, because the loss acts on every value token at every position in every phrasing, which is exactly what the closed-form write lacks (CORPUS/36: no direct objective on tokens 2…N).
- **mechanism** The QLoRA fact-acquisition paper trains Qwen3-4B on 1,938 QA items whose entity names are replaced by synthetic identifiers and scores exact match on 900 held-out items "expressed with disjoint surface templates"; its unquantised Qwen3-1.7B control reaches paraphrase EM 76 % at rank 8, 79 % at 16 and 86 % at 32 while average out-of-domain score falls 57.0 → 52.0 → 40.2. FT-UKE finds a tuned fine-tuning recipe beats locate-then-edit editors on unstructured benchmarks with locality tests. The knowledge-injection comparison finds paraphrase and multi-prompt rewriting augmentation lifts new-fact QA toward the open-book bound, and that models can generate their own augmentation. Model Merging for KE merges a one-layer SFT into the base at α 0.8 on Qwen2.5-7B-Instruct with ZsRE generalization 91.6.
- **sources** 2608.25677 §3.1, §6.2, §7 (read; code `zhngstl/new_facts_forgetting`, pushed 2026-08-31: `training/train_sft.py`, data with `val_paraphrase.jsonl`; QLoRA path needs bitsandbytes/CUDA, plain LoRA does not). 2506.09672 (abstract). 2508.06178 §5 (read; code `hugoabonizio/knowledge-injection-methods`). 2506.12384 (*inv*). 2502.14502 (abstract, LoRA knowledge capacity). RoseLoRA 2406.10777 (abstract; row/column-sparse LoRA for editing).
- **builds on / contradicts** Builds on CORPUS/29 R5 (paraphrase-diverse recipe partially rescues within MEMIT) and the register's Model-Merging fallback (PAS §1.1). Contradicts the spec's reason for excluding fine-tuning ("destructive and cannot be overlaid", genesis transcript): a LoRA delta restricted to the band is additive and overlay-representable exactly as ΔW is.
- **cheapest test** Harness arm: LoRA rank 16 on `down_proj` L4–8 (five matrices 11,008 × 2,048; fp16 base on MPS), 24 facts × about 20 generated phrasings (held-out templates sealed), token-level loss on the value only, early stop on training-phrasing EM, merge, then the standard A1 + A2 + A7 pass and locality battery plus a generic-capability probe (the paper's forgetting axis: a small MMLU subset or the harness perplexity set). About 2–3 h including the generation of phrasings by the model itself. Pass ≥ 61/72 with controls ≥ 68 and all gates; LEAD ≥ 30/72; rank is swept {8, 16, 32} only if rank 16 is PARTIAL. A pass is a write-engine replacement claim and is labelled so.
- **would-advance** C10 and §C write path; it also answers the genesis open question "at what edit volume would fine-tuning be more appropriate than MEMIT" at N = 24.
- **spec-amendment** §8.2 D12 (MEMIT designated; fine-tuning excluded) and §8.4/§8.10 (overlays and compaction would be LoRA deltas re-trained, not MEMIT re-solved). F1 would have to say the write engine changed.
- **feasibility** empirical for the model and harness; the LoRA loop is new but routine (PEFT runs on MPS; CORPUS/04 pins transformers 4.51).
- **source-metric** exact match on held-out templates over anonymised identifiers (Qwen3-4B / 1.7B), the closest published metric to the bar this pass found; still real-ish relation structure, 2-token identifiers, and a 900-item split, not 24 coined 5-token values.
- **disposition** candidate-needs-C10-eval (spec-amendment challenger).

### H-14 Sparse LoRA restricted to the rows the edit touches (RoseLoRA) as the merged write
- **class** E5. Variant of H-13: the LoRA product is constrained to row/column sparsity so the merged delta touches only the `down_proj` rows and columns the facts need, bounding collateral change at non-keyed positions (CORPUS/46 H1 bucket).
- **sources** 2406.10777 (abstract). **cheapest test** same arm as H-13 with the sparsity constraint; compare collateral by the CORPUS/46 edit-plus-inject diagnostic.
- **disposition** lead (runs only if H-13 is PARTIAL with a locality miss). **spec-amendment** as H-13.

## E6 — continued pretraining / fine-tuning on the coined facts

### H-15 Full-parameter fine-tuning of the band on augmented text (continued pretraining at N = 24)
- **class** E6. **claim** Full fine-tuning of the band's MLPs on paraphrase-augmented text about the 24 facts installs the coined values with held-out recall at the bar, at a forgetting cost the QLoRA frontier paper found smaller than high-rank LoRA.
- **sources** 2508.06178 §5 (read): continued pretraining alone gives modest gains; rewriting with multiple prompts approaches document-level RAG; all CPT variants cost control-task accuracy as variations grow. 2609.23916 (abstract): time-incremental CPT on OLMo2 / Llama-3 / Gemma-3 acquires post-cutoff knowledge "without catastrophic forgetting" at 1B–8B and "LoRA at sufficient rank matches full CPT". 2609.00082 KItCAT (abstract; code "coming soon"): random input-token corruption with unchanged labels replaces paraphrase generation. 2411.00686 LaPael (abstract): input-dependent noise on early layers as latent paraphrasing. 2608.25243 GRIN (abstract): mixed-policy RL beats SFT on paraphrase and reasoning for novel facts. 2509.14223 "Fresh in memory" (*inv*): fine-tuning on 16,000 entities with coined 3- and 5-token aliases, probed on held-out entities and an unseen template. 2409.07431 EntiGraph and 2504.05571 Knowledge-Instruct (titles and abstracts): synthetic augmentation for small corpora.
- **builds on / contradicts** Builds on H-13's harness; contradicts §8.2 D12 as H-13 does. "Fresh in memory" is the one source whose targets are coined multi-token strings, and it scores probes, not generation.
- **cheapest test** The H-13 arm with full-parameter updates on the band instead of LoRA, with KItCAT-style corruption as the augmentation (no generation step), ≈ 2 h; gates as H-13 including the forgetting probe. Pass as H-13.
- **would-advance** C10, §C. **spec-amendment** §8.2 D12; §8.10 compaction becomes retraining.
- **feasibility** empirical (3B fp16 on MPS; five matrices trainable).
- **source-metric** QA accuracy on post-cutoff news (TiEBe) and probe accuracy on held-out entities; not full-sequence exact match on coined values.
- **disposition** candidate-needs-C10-eval (spec-amendment challenger; sequenced after H-13).

### H-16 Preference-objective injection (RL or DPO over synthetic preference pairs)
- **class** E6. GRIN 2608.25243 and Style-Debiased DPO 2609.16532 (*inv*) report that preference or mixed-policy objectives generalise new facts across paraphrases where SFT memorises the format. **cheapest test** only after H-13/H-15: swap the loss for a DPO pair (correct value vs the base model's completion) on the same data; ≈ 3 h.
- **disposition** lead. **spec-amendment** as H-15.

## E7 — parametric memory layers / value slots without external lookup

### H-17 Sparse memory-layer slots as the write site
- **class** E7. **claim** A product-key memory layer written by sparse finetuning of only the slots a fact activates would hold coined values with little forgetting (the sparse-memory-finetuning paper reports an 11 % NaturalQuestions drop against 89 % for full finetuning and 71 % for LoRA).
- **sources** 2412.09764 Memory Layers at Scale; 2510.15103, 2604.05248, 2605.03229 sparse memory finetuning (abstracts); `facebookresearch/memory` (reference implementation, licence NOASSERTION, pushed 2024-12-12). Perplexity check: no pretrained memory-layer checkpoints were identified as released for either paper.
- **builds on / contradicts** PAS addendum 3 (MemoryLLM) and register D18. Without a released memory-layer model, the route needs pretraining a memory layer into Qwen2.5-3B, which is outside this Mac.
- **cheapest test** none locally. Static prefilter: not applicable (no checkpoint).
- **would-advance** C10 and §8 (a memory layer is a new write site). **spec-amendment** §8.1–§8.2 (the FFN is no longer the store).
- **feasibility** static. **source-metric** QA F1 retention; not the bar.
- **disposition** lead (effectively unrunnable here); the pool and lookup designs in the same class (MemoryLLM 2402.04624, M+ 2502.00592, Larimar 2403.11901, MemLLM 2404.11672, Kformer 2201.05742, Memory Decoder at Scale 2607.27919, the per-entity LoRA bank 2608.25489) are `fallback`, because recall goes through a pool, a retriever or an adapter selection step.

## E8 — vocabulary extension / tokenizer families

### H-18 Minted token written by embedding-only tuning instead of the MEMIT solve
- **class** E8. **claim** For a minted value token (CORPUS/45: 34–46/72 under the MEMIT write), training only the minted row (input embedding, which on this tied model is also the output row) by gradient descent on paraphrase-diverse text with the rest of the model frozen reaches a higher held-out count than the closed-form write, because the row is fit to every phrasing and every position at once and nothing else moves.
- **mechanism** Memory as a Markov Matrix formalises new tokens as new states of the token Markov chain: transitions among old tokens are untouched by construction (zero forgetting), and the sample complexity of a new token scales with the number of existing tokens it maps to; its embedding-tuning experiments show zero forgetting where other methods forget. Neologism learning trains one new token's d parameters with an APO-style preference loss and beats LoRA under matched data. Concept Tokens learns one new token's embedding from definitions with the model frozen; its fictional "Austral Tower" token captured the theme but was "unreliable for novel factual details", a warning that applies when the new token is the subject, not the value as here.
- **sources** 2605.04308 §3.2, §6.1, §10 (read); 2512.18551 §4.1, §8 (read); 2601.04465 §4, §6.1 (read); tokenizer transplantation by orthogonal matching pursuit 2506.06607 (abstract) as a constructed-init control.
- **builds on / contradicts** Builds directly on CORPUS/45–46 (mint PARTIAL ×5; init G vs N unsupported; seed-sensitive). Contradicts nothing; the mint arms only ever wrote the token through the solve.
- **cheapest test** On the existing mint harness (`c10l_mint_lib.py`, inits N seeds 0–2): freeze the model, train the 24 minted rows on 24 × about 20 generated phrasings of the value (held-out templates sealed), token-level loss on the minted id, a few hundred steps on MPS (minutes), then the standard A7-mint readout and locality battery; same-run MEMIT-mint arm as the comparator. Pass: held-out ≥ 56/72 (the best mint replicate 46 plus the 10/72 gain rule) and A1 ≥ 68 with locality gates; route pass ≥ 61/72. Fail: within the mint envelope [34, 46]. The P4 GGUF chain (2 min) confirms the trained row survives the compile.
- **would-advance** C10; it also decides the F-M4/F-M7 question (is the residual gap the row or the pair) with a different instrument.
- **spec-amendment** none (a minted token is a Git/.vindex artefact under D-C10k-rulings-1 ruling 3).
- **feasibility** empirical (mint harness, inits and GGUF chain exist, CORPUS/45).
- **source-metric** synthetic-vocabulary test loss and forgetting curves; steering-concept adherence; qualitative fictional-landmark recall. None is the bar.
- **disposition** candidate-needs-C10-eval.

### H-19 Two minted tokens per value (one per coined word) to halve the span
- **class** E8. **claim** If the span and not the pair is the wall (CORPUS/45 F-M4 left this open), writing the value as two minted tokens (one per word) lands between the one-token mint (34–46) and the full string (11–15), tracing the length curve the inventory's I-10 ladder asks for.
- **sources** GS-Quant 2604.21649 (*inv*; fixed 4-code token sequences per entity with LoRA-trained code embeddings); CORPUS/45 per-position curve (the string fails at the fourth token).
- **cheapest test** Mint harness with 48 rows, one pass ≈ 40 min; readout per position. A monotone 1-token > 2-token > string ordering supports the span account; 2-token ≈ string supports the pair account.
- **would-advance** C10 mechanism; F-M4. **spec-amendment** none. **feasibility** empirical.
- **source-metric** link-prediction ranking; not the bar. **disposition** candidate-needs-C10-eval (diagnostic value).

### H-20 Constructed embedding for the minted row (tokenizer-transplant init)
- **class** E8. A third init for the mint arm, built from the constituent tokens by orthogonal matching pursuit rather than mean (P-iv showed mean collapses) or random. CORPUS/45's G ≈ N result makes this low-prior; it costs one mint pass. **sources** 2506.06607 (abstract); 2604.02324 (*inv*). **disposition** candidate-needs-C10-eval (low prior).

## E9 — side stores (fallback by ruling; logged, never ranked)

Logged in this pass, all `fallback`: WISE 2405.14768, GRACE 2211.11031, MELO 2312.11795, P-Tokens 2601.16781, OnceEdit 2506.00817, HoReN 2605.08143, RILKE 2511.20892, NeuralDB 2507.18028 (all *inv*); new to the pass: TokenMem 2607.22625 (cross-attention injection channel for frozen Qwen3/Llama/OLMo-3), MemSFT 2607.25614 (external parametric memory), RRDA 2606.14668 (retrieved edit memory plus dual adapters), LightEdit 2604.19089 (retrieval plus decoding suppression), INLAY (`Aditya-PS-05/INLAY`, external addressable memory), TimeROME-DLM 2606.12841 (inference-time low-rank memory for diffusion LMs), RING 2608.01630 (mixture-of-memory experts trained by RL), the per-entity LoRA adapter bank 2608.25489 (knowledge stored but not retrievable by similarity). None is a route; they are the engineering fallback the operator has already ruled on (runbook row 307).

## M1 — untied-embedding models within the prefilter

Static prefilter (configs read from the Hub in this pass; fp16 size = 2 bytes × parameters; projector = intermediate² × 4 bytes; five band layers):

| checkpoint | tied? | hidden / intermediate / layers | fp16 weights | fp32 projector × 5 | prefilter |
|---|---|---|---|---|---|
| Qwen/Qwen2.5-3B (current) | yes | 2048 / 11008 / 36 | 6.2 GB | 2.3 GiB | in use |
| Qwen/Qwen2.5-7B | no | 3584 / 18944 / 28 | 15.2 GB | 6.7 GiB | passes |
| Qwen/Qwen3-8B-Base | no | 4096 / 12288 / 36 | 16.4 GB | 2.8 GiB | passes |
| Qwen/Qwen3-4B-Base | yes | 2560 / 9728 / 36 | 8 GB | 1.8 GiB | passes, but tied |
| Qwen/Qwen3-14B-Base | no | 5120 / 17408 / 40 | 29.5 GB | 5.6 GiB | fails (fp16 > 28 GB) |
| meta-llama/Llama-3.1-8B | no | 4096 / 14336 / 32 | 16.1 GB | 3.8 GiB | passes (gated; readable with this account) |
| mistralai/Mistral-7B-v0.3 | no | 4096 / 14336 / 32 | 14.5 GB | 3.8 GiB | passes |
| allenai/OLMo-2-1124-7B | no | 4096 / 11008 / 32 | 14.6 GB | 2.3 GiB | passes (Hub weights are fp32, 29 GB download) |
| allenai/OLMo-2-1124-13B | no | 5120 / 13824 / 40 | 27.4 GB | 3.6 GiB | borderline (fp16 at the ceiling) |
| EleutherAI/pythia-6.9b | no | 4096 / 16384 / 32 | 14 GB | 5 GiB | passes |
| EleutherAI/pythia-12b | no | 5120 / 20480 / 36 | 24 GB | 7.8 GiB | passes narrowly |
| XiaomiMiMo/MiMo-7B-Base | no | 4096 / 11008 / 36 (+1 MTP layer) | 15.2 GB | 2.3 GiB | passes |
| GSAI-ML/LLaDA-8B-Base | no (`weight_tying: false`) | 4096 / 12288 / 32 | 16 GB | 2.8 GiB | passes (custom code) |
| Dream-org/Dream-v0-Base-7B | no | 3584 / 18944 / 28 | 15.2 GB | 6.7 GiB | passes (custom code) |
| microsoft/Phi-3-medium-4k-instruct | no | 5120 / 17920 / 40 | 27.9 GB | 6 GiB | borderline; Instruct only |
| google/gemma-2-9b | — | — | — | — | gated, no access with this account; Gemma ties embeddings (G4 note) |

### H-21 Qwen2.5-7B (untied) as the model line for the coined-value arms
- **class** M1. **claim** On an untied model the minted-token route (CORPUS/45) separates the input row (what the key sees) from the output row (what the decoder emits), so a minted value's output row can be optimised for decoding without moving its key, and the larger hidden size (3584) and intermediate (18,944) give the solve more separable key directions; the program's own 7B runs showed cleaner single edits (CORPUS/00:18, 99.86 %).
- **mechanism (I-INFER)** The mint arm's residual gap to A1 varied with the random init of one shared row (CORPUS/46 seed-sensitive); untying lets the two roles of that row be fit separately. Suresh et al. report 90–96 % paraphrase generalization for subject-keyed AlphaEdit on Qwen family models with hand-derived hyperparameters.
- **sources** Hub config read (this pass); CORPUS/19, /22 (7B runs on the pod; 18,944-dim solve moved to CPU); 2606.26783 (*inv*).
- **builds on / contradicts** RB:316 lists untied embeddings as a design-diversity axis; D-C10k-rulings-2 gates any model change behind the Qwen3-3B ceiling rule, which the operator may override.
- **cheapest test** Smoke first (a run, so pending): load fp16 on MPS, compute one band-layer covariance, one `_cov_cpu` null-space solve, record wall-clock and peak memory. Then A1 + A2 + A7-multi and A7-mint on 7B with the program's existing 7B hparams (`b1_7b` lineage) after LAW#3 reproduction of the 7B batch result (CORPUS/19 91.7 %). Covariance ≈ 70 min per band on the 4090, unmeasured here. Pass as the standard bar.
- **would-advance** C10; OQ-W1 (7B numeric transfer, already open). **spec-amendment** none.
- **feasibility** static (prefilter passes; 7B ran on the pod, never on this Mac).
- **source-metric** program's own 7B single-token metrics; the external paper's zsRE paraphrase top-1.
- **disposition** lead ("static prefilter passed; empirical feasibility pending").

### H-22 Qwen3-8B-Base, OLMo-2-7B, Pythia-6.9b, Llama-3.1-8B, Mistral-7B-v0.3 as alternative untied lines
- **class** M1 (OLMo-2 and Pythia also M4). Same hypothesis as H-21 with a different tokenizer; Qwen3-8B keeps the Qwen2 tokenizer and has a late value band in the AcE results (PAS §12) and existing covariance work in Moir and AcE (`yjywdzh/ACE` ships `qwen3_8b.json`, *inv*). Llama-3.1-8B and Mistral-7B were eliminated pre-C10 (RB:279) on single-token locality grounds, so they carry a prior. OLMo-2 and Pythia: see H-25.
- **cheapest test** as H-21 per model; each needs hand-derived hparams (2606.26783 says they do not transfer).
- **disposition** lead for each.

## M2 — multi-token-prediction pretrained checkpoints

### H-23 MiMo-7B-Base: a pretraining objective that already asks the residual stream to carry the next k tokens
- **class** M2. **claim** In a model trained with a multi-token-prediction objective, the hidden state at the subject position must encode tokens t+1 … t+k, so a single z written there carries more of a multi-token value's continuation than in a next-token-only model; the MTP layer also offers a second, trainable readout for scoring the continuation during `compute_z`.
- **sources** `XiaomiMiMo/MiMo-7B-Base` (config read: untied, 4096/11008/36 layers, `num_nextn_predict_layers 1`, Qwen2 tokenizer, MIT; `modeling_mimo.py` read: the MTP layer is a Qwen2 attention + MLP block on `[hidden ; input_embeds]`, and the model subclasses `Qwen2ForCausalLM`, so the vendored engine's Qwen2 module paths apply); `XiaomiMiMo/MiMo-7B-MTPs` (README read: two further pretrained MTP layers, 843 MB); 2505.07608 §3.2 (read: one MTP layer during pretraining, "no further improvement" from more; acceptance ≈ 90 %). Perplexity check: Meta's MTP research checkpoints were never released; DeepSeek-V3 is 671B.
- **builds on / contradicts** Inventory row 9 ("MTP-pretrained models should be more editable; no concrete checkpoint"): this is the checkpoint. The operator's inbox transcend note made the same prediction. No editing paper on an MTP model exists in anything searched (inventory gap item 5 stands).
- **cheapest test** Smoke (pending): load with `trust_remote_code` on MPS, one covariance layer, one solve. Then A1 + A2 + A7 with hparams derived as for 7B; the comparison that matters is A7 on MiMo vs A7 on Qwen2.5-7B (H-21), since MiMo shares Qwen2's tokenizer and architecture, isolating the pretraining objective. Pass as the standard bar; the decisive contrast is MiMo A7 − Qwen2.5-7B A7 ≥ 10/72.
- **would-advance** C10; OQ-W2. **spec-amendment** none.
- **feasibility** static (prefilter passes; custom code untested on MPS; MiMo's own README says only vLLM and SGLang were verified).
- **source-metric** reasoning benchmarks and speculative-decoding acceptance; nothing on editing.
- **disposition** lead.

### H-24 Post-training MTP heads on Qwen2.5-3B itself as a continuation loss for `compute_z`
- **class** M2 (applied to the current model). **claim** A small MTP head trained post hoc on the frozen Qwen2.5-3B gives a differentiable loss on value tokens 2 … k at the subject position, so the z-target can be optimised against the continuation directly — the engine-path idea of I-1 realised through a head rather than a reweighting — without changing the base model or the tokenizer.
- **sources** 2610.00888 (abstract: post-training K = 3 chained heads on frozen Qwen3-8B with 2.5B tokens reaches jointly-pretrained MiMo's draft quality; 10³–10⁴× fewer MTP tokens than joint pretraining); 2602.06019 (abstract: self-distillation converts a pretrained model to multi-token prediction with the same implementation).
- **builds on / contradicts** I-1 OverTone (ARC §1) and CORPUS/46 F-D2 (first-token targeting is not the residual). A head trained on 2.5B tokens is weeks on this Mac; a head good enough to be a loss signal for 24 facts may need far less, which is the unknown.
- **cheapest test** Step 0: train one MTP head (one Qwen2 block, as MiMo's) on ≈ 50M tokens of the covariance corpus on MPS (hours; unmeasured) and report its acceptance on the harness prompts; if under 50 % the loss is noise and the hypothesis stops. Step 1: `compute_z` with the head's loss on tokens 2 … k added, one pass, gates as H-1, LAW#5.
- **would-advance** C10. **spec-amendment** none (the head is a compile-time instrument, not part of the served model).
- **feasibility** static for the head; empirical for the pass.
- **source-metric** decoding throughput; nothing on editing.
- **disposition** lead.

## M3 — diffusion language models

### H-25 LLaDA-8B-Base or Dream-7B as the diagnostic for whether the continuation wall is autoregressive
- **class** M3. **claim** Under bidirectional denoising the value's later tokens are predicted with the whole value as context, so a subject-keyed edit at the shared early-mid MLP locus should realise a multi-token value more completely than in the autoregressive model; MDM-KE's own numbers cut the other way for N = 4 (0.27 raw, 0.73 with partial-mask augmentation on LLaDA, against 0.95 for the autoregressive Qwen2.5-7B pair, PAS §13 C2), so the diagnostic may falsify the premise.
- **sources** 2606.03924 (*inv*); 2606.12841 TimeROME-DLM (abstract; inference-time memory, fallback); 2505.12306 (abstract: bidirectional LMs memorise injected facts better under continued pretraining, 23 % reliability gap). Hub configs read: LLaDA-8B-Base untied, 4096/12288/32, custom code; Dream-v0-Base-7B untied, 3584/18944/28, Qwen2.5-7B-derived. Perplexity check found no verified MPS serving evidence; one MLX 4-bit Dream conversion exists. The MDM-KE code named in PAS §4 (`holi-lab/MDM-KE`) does not exist on GitHub (404; the organisation's repositories are listed in `contradictions.md`).
- **cheapest test** Smoke (pending): LLaDA-8B-Base generation on MPS; then a subject-keyed MEMIT write at the MDM-KE locus with the program's A1/A2/A7 stimuli, scoring full-sequence recall by greedy remasking. Hparams hand-derived; covariance time unmeasured.
- **would-advance** C10 mechanism (autoregressive artefact or not), OQ-W2. **spec-amendment** §8.1 if the served model is not autoregressive (the §G read path assumes generation).
- **feasibility** static. **source-metric** Kamel substring efficacy and paraphrase on real counterfactuals. Not the bar.
- **disposition** lead.

## M4 — open-data models

### H-26 OLMo-2-7B with a covariance drawn from its own pretraining mixture
- **class** M4 (also M1). **claim** With the pretraining data public (`allenai/olmo-mix-1124`, `dolmino-mix-1124`), the preservation covariance can be sampled from the true training distribution rather than a Wikipedia proxy, which H-4 argues is the knob; OLMo-2-7B is untied and inside the prefilter; Moir, TokenMem and the time-incremental CPT study all use OLMo-2-7B, so external anchors exist.
- **sources** Hub config read; 2607.20433, 2607.22625, 2609.23916 (abstracts). Pythia-6.9b/12b (Pile) is the second open-data line (2402.06155 edits Pythia with canonical examples).
- **cheapest test** as H-21 plus the in-distribution covariance; pass as the standard bar; the contrast is Wikipedia-C vs Dolma-C on the same model.
- **would-advance** C10 addressing side; OQ-W1. **spec-amendment** none. **feasibility** static (fp32 Hub weights, 29 GB download).
- **disposition** lead.

## M5 — hybrid / SSM / MoE

### H-27 OLMoE-1B-7B with the MoE-aware closed form
- **class** M5. **claim** In a mixture-of-experts FFN the keys a fact activates are expert-specific, so batched writes of 24 facts collide less than in a dense `down_proj`; closed-form MoE editing now exists (per-expert objective solved with the Woodbury identity).
- **sources** 2605.16686 (abstract); MoEEdit 2602.10965 (*inv*); `allenai/OLMoE-1B-7B-0125` config read (untied, 64 experts top-8, hidden 2048, expert intermediate 1024, 16 layers; fp16 ≈ 14 GB; per-expert covariance 1024² ≈ 4 MiB).
- **cheapest test** Smoke (pending), then A1/A2/A7 with per-expert statistics; hparams from scratch.
- **would-advance** C10; OQ-W2. **spec-amendment** §8.2 wording ("FFN pathways" still holds). **feasibility** static.
- **source-metric** standard KE metrics on MoE models; not the bar. **disposition** lead (the class is not empty).

### H-28 Mamba-2.8B or Falcon3-Mamba-7B with ROME-style editing
- **class** M5. Sen Sharma, Atkinson and Bau locate and edit factual associations in Mamba-2.8B at a subject-token mid-layer locus (2404.03646, abstract); Falcon3-Mamba-7B (untied, 4096, 64 layers) and `state-spaces/mamba-2.8b-hf` (2560, 64 layers) are on the Hub. MPS: the fast selective-scan kernels are CUDA; transformers' slow path runs on CPU/MPS.
- **cheapest test** smoke, then single-token A1 only (the locus must first be shown to transfer paraphrases at all), then A7.
- **disposition** lead. **spec-amendment** §8.1 (no FFN `down_proj` in the same sense).

## Diagnostics that cost minutes and sharpen any arm above

### H-29 Entity-lens readout at the keyed position (storage vs decoding)
- **class** mechanism (harness-only). **claim** A task-vector decoder trained to reconstruct multi-token mentions from hidden states (the "Entity Lens") can read the coined value out of the post-edit hidden state at the subject position even when greedy generation fails, separating "not stored" from "stored but not decoded" — the question CORPUS/46 could only partition by constrained decoding.
- **sources** 2510.09421 §4.3 (read: mentions of unseen entities decodable from middle-layer representations with task vectors; frequency, not length, drives decodability); `VictorMorand/EntityRepresentations` (pushed 2025-10-22).
- **cheapest test** Train the lens on the base model's own entity mentions (minutes on MPS), apply to the A7 post-edit states at L8 for the 72 held-out prompts, report exact-mention reconstruction alongside `para_full`. No write. ≈ 1 h.
- **would-advance** C10 mechanism routing (H1 vs H2, CORPUS/46). **spec-amendment** none. **disposition** candidate-needs-C10-eval (diagnostic).

### H-30 Weight grafting to localise where a fine-tuned coined value lives
- **class** mechanism. If H-13 or H-15 passes, graft the band's fine-tuned weights onto the base model layer by layer (dynamic weight grafting, 2506.20746 abstract: enrichment at entity tokens vs recall at the final position) to learn which component carried the value, and whether a closed-form write could reproduce it. ≈ 1 h after an H-13 pass. **disposition** lead (conditional).

---

## Addendum after the council critique (2026-10-06)

The six council lenses (`council_critique.md`) did not change any disposition. One labelling correction is recorded: **H-18 spec-amendment** should read "§8.1 / §8.4 / §8.10 — an embedding-side write outside the FFN compile, whose survival through a compaction re-run is undefined", not "none". The cross-cutting amendments every pre-registration must carry before a run (second process per arm, published and hashed training phrasings with an overlap audit against the sealed templates, per-frame bystander probes, per-fact 24-vectors, the §21.4 judgment tuple, a named forgetting instrument for H-13, free-generation readout and row-norm ceiling for H-18) are listed in the synthesis of that file.
