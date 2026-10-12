# Prior art — "AnyEdit++: Adaptive Long-Form Knowledge Editing via Bayesian Surprise" (2026), and what it says about Route A

**Paper:** Tian, He, Wu, Wang, Chen, Li, Yue (HKUST-Guangzhou, Southeast U., Knowin AI, CUHK, JITRI Wuxi). arXiv 2606.01053v1, 31 May 2026. Code: `https://github.com/TianSuya/Bayes-Chunk`. Added to context by the operator 2026-10-04 during the Route A close-out, with a Connected Papers export (`~/Downloads/ConnectedPapers-for-AnyEdit++…bib`, 41 entries). The repo's June sweep (EV-6) named AnyEdit++ (14 files) but had not read it; this note grounds it.

**Source read:** the arXiv HTML v1 via fetch summary (not the PDF text); numbers below are as reported by that summary and should be re-checked against the PDF before any of them is leaned on in a prereg.

## 1. What the paper does (EVIDENCE-SHOWS, from the paper)

- **Problem it names.** AnyEdit's fixed-size sliding window "is oblivious to the distribution of information density within the text, leading to rigid truncations at critical semantic dependencies" (code, maths, logical chains).
- **Method (Bayes-Chunk).** Token surprisal `S(y_t) ≈ −log P(y_t | y_<t; θ)` under the unedited model; segment the target text at the top-M local maxima of surprisal, with `k = ⌈L/40⌉` segments; **inject each edit at position `b_j − 1`, the token immediately preceding a high-surprisal boundary** ("the immediate predecessor state offers a strictly superior control channel", Theorem 5.2). Per-segment objective is the MEMIT-style least squares `W_out* = W_out + δ* kᵀ (C + k kᵀ)⁻¹` with a preservation term `λ·E_x∼K ‖W k_x − f_old(k_x)‖²`; Adam, lr 0.05, 20 steps, λ = 0.5. Theorem 5.1 bounds cross-talk between segments by the cosine between anchor keys (Bayes-Chunk 0.509 vs fixed window 0.594).
- **Models and data.** Llama-3.1-8B-Instruct, Llama-2-7B, Qwen2.5-7B-Instruct; EditEverything (7 domains), CounterFact, UnKE, and a new QwQ-Edit (300 logically dense samples). **Metrics: BLEU and BERTScore of the edited model's generation against the target text.**
- **Headline numbers.** EditEverything, Llama-3.1-8B: BLEU 77.74 vs AnyEdit 74.19; BERTScore 96.49 vs 95.84. CounterFact BLEU 90.69 vs 86.27; UnKE 81.57 vs 79.02. Largest gains on code and on long, logically dense text; fine-tuning comparison gains are small (+0.05 BLEU).
- **Not reported (by the summary's reading):** paraphrase generalisation, locality/specificity, compute cost, ablation on the `L/40` density.

## 2. Bearing on Route A and C10 (I-INFER unless marked)

**2.1 It confirms where the long-form lineage keys its writes, and why that cannot help our gate.** AnyEdit keys at the last prompt token and at answer-internal window positions; AnyEdit++ keeps that family and moves the key to the predecessor of a surprisal boundary inside the target text. Both key on **positions inside or at the end of the context being written**, never at the subject token. The repo's Route A back-test measured what that does on Qwen2.5-3B base: hidden-state transfer 1.00 on the trained prompt, 0.01–0.02 on paraphrases (`results/c10k_route_a/solve_backtest.json`; Amendment 3 §6e). AnyEdit++'s own Theorem 5.2 argues the predecessor position gives the *strongest control over the next token*, which is precisely a statement about fitting the trained continuation, not about reading the fact back from a different prompt. Taken with the LRE lineage (`docs/PRIOR_ART_LRE_HERNANDEZ_ICLR2024.md` §2.1: the relation is decoded linearly from the subject's last token), the two literatures describe the same mechanism from opposite ends.

**2.2 The lineage's metrics do not measure the program's criterion.** AnyEdit and AnyEdit++ report BLEU/BERTScore of the generation against the target text on the edited prompt; that is the program's **canonical** read (which Route A achieved: 24/24 on every arm once the ridge was rescaled). The program's binding criterion is **held-out-paraphrase full-sequence correctness** (`para_full`), which the Route A port scored 0/72 on every arm, and which this lineage does not report. So the HALTED result does not contradict AnyEdit's or AnyEdit++'s claims; it shows that their claims, even if they transferred perfectly to a 3B base model, would not reach the gate the F1 determination needs. This is the clearest statement yet of why "port the long-form editors" was not going to close C10, and it should be carried into the close-out verdict's scope.

**2.3 What is still worth taking from it.** (a) Surprisal-located anchors are a cheap, model-derived way to choose write positions *within* a value; for the program's multi-token coined values this is a candidate for where in the value to put a second key, if subject-token keying is kept for generalisation. (b) The cross-talk bound by anchor-key cosine (Theorem 5.1) is a usable diagnostic: the Amendment 1 controls already compute per-key cosines on this model. (c) Their preservation term uses the covariance ridge `C` (MEMIT-style), not AlphaEdit's null-space projector; Route A's L2-dominance finding (Amendment 3 §2) is specific to the AlphaEdit_ARE variant and would not arise in this formulation.

**2.4 What not to over-read.** Instruct models only, 7B–8B; BLEU on generations is a soft metric (a 2-point BLEU gain on EditEverything is small); no locality numbers, so nothing about the collateral damage Route A saw under the rescaled ridge.

## 3. Connected Papers neighbourhood (41 entries; triaged against the repo by title search)

**Already in context:** AnyEdit++ (named in EV-6), FABLE (11 files), BetaEdit (21; `memory_mirror/betaedit-official-repo.md`), COIN / "Uncovering Context Reliance in Unstructured Knowledge Editing" (9), SUIT (8), UnKE (7), μKE (13), "Is Model Editing Built on Sand?" (4), SetKE (3), EvoEdit (2), LyapLock, REACT, In-Context Editing (1 each).

**New and relevant:**
1. **"Keys to Robust Edits: from Theoretical Insights to Practical Advances" (2024).** Title says it is about key design for robust (generalising) edits; directly on the Route A keying question. **Action:** read before any next keying decision.
2. **ManiEdit (2026) — sequential unstructured editing from a manifold perspective;** and **"Spectral Characterization and Mitigation of Sequential Knowledge Editing Collapse" (2026).** Both on sequential long-form editing stability; relevant to the program's batch-vs-sequential and capacity questions (D1 line), not to C10 directly.
3. **"Beyond Local Edits: Embedding-Virtualized Knowledge for Broader Evaluation and Preservation" (2026).** An evaluation/preservation framework; possible source for a stronger locality battery (same need as Hoelscher-Obermaier in the LRE note).
4. **"A Dual-Axis Taxonomy of Knowledge Editing for LLMs: From Mechanisms to Functions" (2025)** and **ThinkEval (2025).** Survey/eval; background.
5. **StruEdit (2024), "Evaluating the Reversal Curse in Model Editing" (2023), Adaptive Token Biaser (2024).** The reversal-curse paper is the one most likely to matter for the program's R2 reverse-lookup line (`docs/R2_REVERSE_LOOKUP_PREREG.md`).

**What the neighbourhood confirms:** this is the unstructured/long-form editing lineage (UnKE, AnyEdit, FABLE, COIN, SUIT, ManiEdit, EvoEdit); it does not overlap the LRE recall-mechanism graph except through the ROME/MEMIT roots. The program's C10 question sits between them.

## 4. Where this goes

- Cited in the Route A close-out (`CORPUS/42`) for §2.2: the long-form lineage's metrics (BLEU/BERTScore on the edited prompt) do not measure held-out-paraphrase correctness, which is the program's binding criterion.
- "Keys to Robust Edits" queued with Christ 2025 and Choe 2025 (LRE note §4) as the three reads before any next keying/admission-test prereg.
