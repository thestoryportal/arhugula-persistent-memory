# Scout 2026-10-07 — C10 realisation wall (new evidence only)

Scope: items not in `docs/PRIOR_ART_SWEEP_2026-10-04.md`, `docs/INFRANODUS_RESEARCH_ARC_2026-10-05.md`, `results/research_pass_2026-10-06/*`, `external_prior_art/`, `CORPUS/`, `memory_mirror/`. Novelty test: every arXiv id was checked against the 1,104 distinct ids grepped from those places (`/tmp/known_ids.txt`, built 2026-10-07; an id counted "new" only if absent). Papers were read through the arXiv MCP (download to its own cache, then outline / section / text search). No model or GPU job was run, no repo file other than this one was edited, no git state was changed.

Headline: the locate-then-edit literature from 2026-07 onward is already saturated in the program's records (nearly every id my queries returned was known). The one new, directly on-point item is an output-margin joint closed-form solve (ASTRA, 2610.05277). The rest are weak or adjacent.

Ranked by relevance. "Read" says what I actually read; anything marked ABSTRACT ONLY I did not open past the abstract.

---

## 1. ASTRA — "Mind the Gaps: From Failure Attribution to Closed-Form Repair of Code Language Models"
- **id / date:** arXiv 2610.05277 (v1), 2026-10-04. Authors Gu, Zhang, Chen, Aleti.
- **Read:** abstract; §3.4 "Tailoring Joint Patches" (Algorithm 1 and the linear system, in full); §5.3 ablation paragraph; §5 Discussion; method overview in §1/§3. Section numbers are the paper's own (the MCP outline labels them 4.x/5.x).
- **Claim relevant to the problem.** The patch is not solved against a hidden-state target. It is solved against an *output constraint*: the logit lead of the reference token over the produced token must grow by its deficit plus a margin, at every failing token of the answer. One small linear system `A λ = γ` (one row per failing token, entries `A_tu` couple tokens that share carrier neurons) is solved directly, with a small ridge term, and written into selected columns of `W_down` in late layers. The update is exact only to first order, so the observe-and-solve step is repeated up to 10 rounds ("re-linearising"). Null-space protection is a diagonal form of AlphaEdit's constraint (weight = inverse mean squared key activation on reference prompts). Four rendered "views" of the prompt are fitted together.
- **Ablation numbers (§5.3).** Replacing the joint solve with a token-by-token solve costs 34.2 Pass@1 points pooled (27.9 to 47.0 per setting, significant in all 6 settings; 85 to 293 failing tokens per sample); the stated reason is that tokens share carriers, so sequential corrections undo each other. A margin of 1 logit instead of 5 costs 31.4 points ("a lead of one logit does not survive" the change from teacher-forced views to free generation from another prompt). Fitting one view instead of four costs 6.5 points. Headline: 66.7 % Pass@1 against 48.4 % for the best of AlphaEdit/STAR/LoRA; +22.0 points over the best baseline under an unseen prompt phrasing; 2.7 s per sample; the patch needs forward passes only, "no optimizer, no step size and no backward pass".
- **Code / CUDA:** I found no code link in the paper text (searched "github", "available"; one WebSearch found nothing). The paper says models run in bfloat16 on "one GPU"; the algorithm itself is forward passes plus a k-by-k solve, so nothing in the method is CUDA-specific. MPS portability is my inference, not tested.
- **Diagnostic addressed:** (b) strongly (every value token gets a constraint, solved jointly); (a) partly (it never needs a z-to-weight conversion, because it constrains the output directly and iterates on the residual shortfall).
- **Caveats I could verify from the text:** domain is code repair (API-evolution benchmarks), three code models of 1B, 8B, 9B; no fact-editing result; "side effects on unrelated code are small on the large models and larger on the small one" (abstract), which matters for a 3B model; first-order only.
- **Would change the queue?** Yes. No queued item (H-1…H-30, E1–E9, M1–M5; I grepped `hypotheses.md` for margin / re-linearise / Jacobian and found none) writes a per-commit closed-form solve with an output-logit-margin constraint on every value token. Suggested pre-reg stub: replace the hidden-state target `z` by margin constraints on value tokens 1..n (margin of order 5 logits, since 1 logit was the failing setting), several paraphrase views in the solve, joint solve across tokens, 3 to 10 re-linearisation rounds, existing LAW#5 null-space weights. Test it on the A7-multi arm against the 12–15/72 baseline and the 61/72 bar.

### 1b. STAR — "A Semantic-based Optimization Approach for Repairing LLMs" (ASTRA's predecessor)
- **id / date:** arXiv 2503.12899 (v4), 2025-03-17. **ABSTRACT ONLY.**
- **Claim:** neuron patches come from an analytical formula that "directly bridges the changes to logits with the deltas of neurons", and the method "may solve multiple failures together". Same lineage as ASTRA; useful only to find code, which I did not locate.
- **Diagnostic:** (b). **Queue:** none on its own; chase it only if ASTRA has no code.

---

## 2. EAMET — "Robust Massive Model Editing via Embedding Alignment Optimization"
- **id / date:** arXiv 2505.11876 (v4), first posted 2025-05-17 (outside the 2026-07 window, but absent from every program record).
- **Read:** abstract, Introduction, §"Motivation 4.1" (partial passages), Table 3 caption and "Finding 1" (partial), Appendix E heading. I did not read the objective in full.
- **Claim:** the stated cause of edit failure is "embedding misalignment, which reflects the structural inconsistency between key and residual embedding spaces"; when parameters are updated jointly from a batch, "they fail to accurately reconstruct an individual factual association", and the loss grows with batch size. They define a per-method "misalignment score" (Table 3: 10,000 facts; EAMET 374 to 520 on CounterFact against 8,564 to 18,498 for MEMIT) and fix it by optimising the target memory under a similarity-alignment loss (MSE on the top-M key cosine similarities).
- **Code / CUDA:** repo `github.com/ybdai7/EAMET-massive-editing` (URL printed in the abstract; not opened). CUDA dependence not checked.
- **Diagnostic:** (a), by analogy only. Their failure is batch-scale cross-talk (10k facts); the program's is a single-key shortfall (3 % realised). The misalignment score could be computed on the C10 key set as a cheap extra diagnostic, but the paper does not claim to explain a 3 % realisation.
- **Would change the queue?** Marginally: add the misalignment score to an existing diagnostic run; no new arm.

---

## 3. "MLPs are Hebbians: Constructing Efficient Fact-Storing MLPs for Transformers"
- **id / date:** arXiv 2607.10034, 2026-07-10. Garcia, Liu, Junkins, Eyuboglu, Rudra, Re.
- **Read:** abstract; Introduction; §3.2 "Margins Govern Transformer Usability"; §5.2 "Fact Editing via MLP Swapping" (start); Discussion.
- **Claim:** "positive margin at stored keys is not enough for a Transformer block to use a fact-storing MLP reliably"; because attention perturbs the query before it reaches the MLP, the decoding margin must be bounded away from zero, and the usable-key fraction inferred from per-key margins "closely tracks end-to-end Transformer accuracy" (Appendix, Figure 7). They give a closed-form (Hebbian-kernel) construction with a provable margin for arbitrary key/value geometry.
- **Code / CUDA:** code stated at `github.com/HazyResearch/hebbian-mlps` (from the paper text; a WebSearch could not confirm the repo; CUDA unchecked).
- **Diagnostic:** neither exactly; it is a theory-side account of why a write that satisfies the stored key can still fail on perturbed (paraphrase) queries, i.e. the held-out paraphrase gap. The paper itself says the analysis "currently applies to constructed MLPs in a single-layer Transformer setting" and extension to pretrained LLMs is open.
- **Would change the queue?** No. It supports adding a per-key decoding-margin readout, and reinforces item 1's point that a margin, not just stored-key accuracy, is the quantity to solve for.

---

## 4. Weak or adjacent items (abstract only unless noted)

| item | id / date | one claim | diag | queue? |
|---|---|---|---|---|
| MEGA, "The Anatomy of an Edit: Mechanism-Guided Activation Steering for Knowledge Editing" (ABSTRACT ONLY; my WebFetch of the PDF returned nothing usable) | 2603.20795, 2026-03-21 | post-edit attribution across several editors: mid-to-late attention mainly promotes the new target, attention and FFN together suppress the old fact; a weight-free attention-residual steering method (GPT2-XL, LLaMA2-7B) matches the editors | (a) as a hypothesis only: part of what a weight edit "realises" may happen downstream in attention, not at the keyed MLP | No. Possible explanation to test if item 1 fails. |
| CoRE, "Context-Robust Knowledge Editing" (ABSTRACT ONLY) | 2505.23026, 2025-05-29 | minimises context-sensitive variance of hidden states for the edited fact; editing success drops when a preceding context is present | key-side robustness (relates to the held-out paraphrase gap) | No; the program already has the robust-key work (2410.09338). |
| "In-Place Tokenizer Expansion for Pre-trained LLMs" (ABSTRACT ONLY) | 2607.15232, 2026-07-16 | new vocabulary rows initialised as the mean of their source sub-token embeddings, then embedding-only training, then full continued pre-training | vocabulary route | No; the mint harness already tests mean (M), de-meaned (G), random (N) inits (`docs/C10L_MINT_TOKEN_PREREG.md` §4). Training is outside the constraint. |
| CellFill / "In-Cell Learning" (ABSTRACT ONLY) | 2608.20873, 2026-08-21 | writes facts inside frozen 4-bit quantisation cells; paraphrase and composition generalise; training-based | none | No (needs a training loop). |
| "Can a Language Model Learn Facts Continually in Its Weights?" (ABSTRACT ONLY) | 2607.11020, 2026-07-13 | after 20 sequential writes, 1 % retention with repeated statements vs 46 % with 24 varied restatements | paraphrase data | No (SFT/LoRA/distillation; supports the program's existing E5/E6 reading). |
| HeadEdit (ABSTRACT ONLY) | 2610.01170, 2026-10-01 | gradient-free calibration through the unembedding matrix; behaviour, not facts | none | No. |

Also not new in substance, listed so nobody re-chases them: EAMET-like and CoRE-like key/target repairs above; `2601.07873` MOSE (sequential-edit stability, ABSTRACT ONLY); `2603.12677` MetaKE (training); `2605.13919` multilingual merging; `2603.14343` audio-language editing; `2606.10820` K-Forcing and `2608.17325`/`2609.33816` tokenizer papers (decoding / tokenisation, not editing).

---

## 5. What I looked for and did not find
- No 2026-07+ paper that gives value tokens two onward an objective inside a locate-then-edit write on an autoregressive LM. The only multi-token breakdown papers returned were already known: masked-diffusion editing (2606.03924, 2606.12841), AnyEdit, FOVEATED 2610.02772, ManiEdit 2609.33534.
- No paper that measures "fraction of the target residual realised by the weight update" the way diagnostic (a) does. EAMET's misalignment score and ASTRA's lead-deficit accounting are the nearest.
- No new editor that runs without CUDA with code in hand. ASTRA and Hebbian-MLP code links were not verified.
- Vocabulary extension for entity names: only tokenizer-expansion and init papers, nothing about editing a fact into a new token row.

---

## 6. Queries run and hit counts

arXiv MCP `search_papers` (hits returned; "of N" where the server reported a total):
1. `"knowledge editing" AND ("multi-token" OR "multi-token objects" OR "long-form")`, 2026-07+: 1
2. `"model editing" AND ("closed-form" OR "null-space" OR "least squares")`, 2026-07+: 5
3. `"locate-then-edit" OR "MEMIT" OR "AlphaEdit"`, 2026-07+: 7
4. `"knowledge editing" AND ("paraphrase" OR "generalization" OR "efficacy")`, 2026-07+: 15
5. `abs:"closed-form" AND abs:"repair" AND abs:"language model" AND abs:"edit"`: 0
6. `"vocabulary expansion" OR "new tokens" OR "added tokens" AND ("entity" OR "knowledge injection")`, 2026-07+: 17
7. `"fact editing" OR "factual editing" AND "representation" AND ("weight update" OR "weight edit")`: 1
8. `"rank-one" AND ("editing" OR "edit") AND "language model"`: 1
9. `editing multi-token facts language model`, 2026-07+: 20 of 56,085
10. `knowledge editing weight update fails to realize target activation`, 2026-07+: 20 of 41,106
11. `model editing generalization paraphrase key-value memory MLP` (cs.CL/LG/AI): 30 of 26,815
12. `editing facts with multi-token answers per-token objective target`: 30 of 13,225
13. `parametric knowledge injection new entities without training closed-form weight update`: 30 of 21,823
14. `associative memory ridge regression layer write fact subject last token residual`: 30 of 13,086
15. `"knowledge editing" AND "multi-token"`, 2025+: 2
16. `"model editing" AND ("target representation" OR "target vector" OR "residual") AND "closed-form" AND "layer"`, 2025-06+: 0
17. `"locate-then-edit" OR "locating-then-editing" OR "locate-and-edit"`, 2026+: 18
18. `unembedding OR "output embedding" OR "lm head" editing facts language model closed-form`, 2026-05+: 15 of 29,687
19. `knowledge editing value vector regularization shrinkage under-realized edit magnitude`, 2026-03+: 15 of 63,663
20. `equality-constrained model editing exact memorization EMMET`, 2025-06+: 15 of 250,009
21. `editing novel entity names or fictional entities in LLM weights, tokenization fragmentation hurts editing`, 2026+: 15 of 86,004
22. `"logit margin" OR "output margin" knowledge editing closed-form linear system Jacobian first-order edit`, 2026+: 15 of 116,422
23. `gradient-free analytic patch language model factual error teacher forcing multiple tokens jointly`, 2026+: 15 of 183,476
24. `"key-value" memory editing "paraphrase" OR "rephrase" robustness key variance averaging ...`, 2026-04+: 15 of 93,817

Hugging Face papers (`hf_fs search hf://papers`, 15 each, all truncated at the limit): `multi-token knowledge editing locate-then-edit`; `closed-form model editing null-space MEMIT`; `edit realization weight update target representation gap knowledge editing`; `new entity names vocabulary token embedding knowledge editing`. Results were old papers or already known (checked: 2601.15686, 2602.03696, 2512.04753, 2510.02392, 2406.11263, 2504.01196, 2403.14236, 2502.01636 known; 2601.17086 SonoEdit and 2505.23026 CoRE and 2505.11876 EAMET not in records, of which only the last two are kept above).

WebSearch: 3 topical or code lookups (extended multi-token-editing search; ASTRA code; Hebbian-MLP code). The extended search returned only known papers (AnyEdit, KLOD, masked-diffusion editing, MOSE, TokenMem 2607.22625, 2605.16686).

arXiv `get_abstract`: 2610.05277, 2607.10034, 2607.15232, 2607.11020, 2608.20873, 2603.20795, 2610.01170, 2601.07873, 2505.11876, 2505.23026, 2503.12899. Full-text sections read: 2610.05277, 2607.10034, 2505.11876 (partial).

Not verified (state plainly): ASTRA code existence; EAMET and Hebbian-MLP CUDA dependence; whether ASTRA's first-order solve transfers from code-model repair to coined-name facts on Qwen2.5-3B.
