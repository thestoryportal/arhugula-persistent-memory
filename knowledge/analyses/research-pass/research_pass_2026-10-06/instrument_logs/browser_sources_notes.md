# Browser-instrument notes — research pass 2026-10-06

Instrument: `browser-harness` driving the operator's open Chrome over CDP (existing tabs reused for Semantic Scholar, Google Scholar, Connected Papers, NotebookLM; no tabs created or closed; no `activate_tab`). Companion JSON: `browser_sources.json` (26 entries: 8 S2 queries + 3 S2 paper pages + 8 Google Scholar queries + 1 InfraNodus entry + 4 Connected Papers graphs + 2 NotebookLM questions). Raw captures: `browser_raw/`.

## Reachability

- semanticscholar.org — reached; all 8 queries returned 10 results; 3 paper pages opened. No login/captcha.
- scholar.google.com — reached; all 8 queries returned 10 results; no captcha encountered.
- connectedpapers.com — reached, logged in as "Robert" (Premium banner visible). 4 graphs built, 4 BibTeX exports downloaded via More → Download.
- notebooklm.google.com — reached, signed in; both notebooks opened and answered.
- **InfraNodus Chrome extension — NOT reachable/not present.** On the Google Scholar results page for "multi-token object knowledge editing" there was no infranodus-named element in the DOM, and CDP `Target.getTargets` listed only one unrelated extension (a screen-recorder service worker) and "Gemini in Chrome". The extension was therefore not triggered; no cluster/gap output exists from it.
- Mechanics note: CDP mouse events time out on background tabs for some sites (Connected Papers), so menu clicks there were dispatched through JS (`element.click()`); NotebookLM card clicks required real CDP clicks (synthetic JS clicks did not navigate).

## Semantic Scholar — paper pages opened (scorecards copied from page)

1. **Locating and Editing Factual Associations in Mamba** — S2 `5664f7f52264ff656faa3671d83e2009f4f390fd`, DOI 10.48550/arXiv.2404.03646, Corpus ID 268889738. Scorecard: 48 Citations; Highly Influential Citations 1; Background 8; Methods 2. Top citing papers (page order): Mamba Knockout for Unraveling Factual Information Flow; Timesteps of Mamba Align with Human Reading Times; Representation Shattering in Transformers: A Synthetic Study with Knowledge Editing; From RAGs to rich parameters; The Quest for the Right Mediator (survey, two versions); Understanding Information Storage and Transfer in Multi-modal LLMs; Understanding and Enhancing Mamba-Transformer Hybrids for Memory Recall; LLMs Process Lists With General Filter Heads.
2. **Massive Editing for Large Language Models Based on Dynamic Weight Generation (MeG)** — S2 `1b61cde6c4af087724f99851175d5f6dd7c42f4e`, arXiv 2512.14395, Corpus ID 283909249. Scorecard: 1 Citation (no highly-influential count shown). Citing paper: HyperFix: Combinatorial Nonlinear Correction for Task Vector Merging.
3. **Latent Knowledge Scalpel: Precise and Massive Knowledge Editing for Large Language Models (LKS)** — S2 `05354809332ef3c8c94a90dde8fd4b3413088abc`, arXiv 2508.03741, Corpus ID 280536640, venue "European Conference on…" (ECAI), 1 Aug 2025. Scorecard: 1 Citation; Highly Influential Citations 1. Citing paper: TISKE: Two-Stage Incremental and Scalable Knowledge Editing for LLM-Based Intelligent Services.

## Connected Papers — graphs built and exports

None of the four seeds had a .bib in `/Volumes/memit/llm-database-poc-mirror/connected-papers-knowledge-graphs/` (checked with `ls | grep -iE "Keys|BetaEdit|Markov|LOKI"` → empty). Files were downloaded with the site's own filename (URL-encoded, matching the existing collection convention) into INBOX with `cp -n`; md5 verified equal to the download. "Most connected" is approximated by the site's default list-panel order (Connected Papers exposes no numeric connectivity); the .bib holds all nodes.

### Keys to Robust Edits: from Theoretical Insights to Practical Advances (arXiv 2410.09338)
Graph: https://www.connectedpapers.com/main/db65032344b8712da92f33e23618e22282d7bfea/graph — 40 nodes; .bib (40 entries): `/Volumes/memit/llm-database-poc-mirror/connected-papers-knowledge-graphs/INBOX/ConnectedPapers-for-Keys-to-Robust-Edits%3A-from-Theoretical-Insights-to-Practical-Advances.bib`
Top-10 (panel order after origin):
  1. Perturbation-Restrained Sequential Model Editing (2024)
  2. InstructEdit: Instruction-based Knowledge Editing for Large Language Models (2024)
  3. Evaluating the Reversal Curse in Model Editing (2023)
  4. Lifelong Knowledge Editing requires Better Regularization (2025)
  5. SetKE: Knowledge Editing for Knowledge Elements Overlap (2025)
  6. Knowledge in Superposition: Unveiling the Failures of Lifelong Knowledge Editing for Large Language Models (2024)
  7. Revealing the Deceptiveness of Knowledge Editing: A Mechanistic Analysis of Superficial Editing (2025)
  8. Cross-Lingual Knowledge Editing in Large Language Models (2023)
  9. Resolving UnderEdit & OverEdit with Iterative & Neighbor-Assisted Model Editing (2025)
  10. Context-Robust Knowledge Editing for Language Models (2025)

### BetaEdit: Null-Space Constrained Sequential Model Editing (2605.09285)
Graph: https://www.connectedpapers.com/main/3960ef01c971ac19ad5d9eae6078f6f4de9fd1e1/graph — 41 nodes; .bib (41 entries): `/Volumes/memit/llm-database-poc-mirror/connected-papers-knowledge-graphs/INBOX/ConnectedPapers-for-BetaEdit%3A-Null%20Space-Constrained-Sequential-Model-Editing.bib`
  1. Is Model Editing Built on Sand? Revealing Its Illusory Success and Fragile Foundation (2025)
  2. Are We Evaluating the Edit Locality of LLM Model Editing Properly? (2026)
  3. From Backward Spreading to Forward Replay: Revisiting Target Construction in LLM Parameter Editing (2026)
  4. Neuron-Level Sequential Editing for Large Language Models (2024)
  5. AlphaEdit: Null-Space Constrained Knowledge Editing for Language Models (2024)
  6. Orthogonal Representation Editing: Decoupling Semantic Entanglement in Batch Knowledge Editing of LLMs (2026)
  7. ReFEdit: Rehearsal-Free Lifelong Knowledge Editing for Large Language Models (2025)
  8. Relaxing the Constraints: A Dual-Importance Projection Mechanism for Lifelong Model Editing (2026)
  9. Beyond Binary Edits Robust Multimodal Knowledge Editing with Adversarial Subspace Alignment (2026)
  10. MetaKE: Meta-learning Aligned Knowledge Editing via Bi-level Optimization (2026)

### Memory as a Markov Matrix (2605.04308)
Graph: https://www.connectedpapers.com/main/88761096f076be123e5a0e43c5b000e020924c73/graph — 41 nodes; .bib (41 entries): `/Volumes/memit/llm-database-poc-mirror/connected-papers-knowledge-graphs/INBOX/ConnectedPapers-for-Memory-as-a-Markov-Matrix%3A-Sample-Efficient-Knowledge-Expansion-via-Token%20to%20Dictionary-Mapping.bib`
Note: this graph's neighbourhood is PEFT/continual-finetuning (DoRA, adapters, catastrophic-forgetting), not the editing literature — Connected Papers places the paper outside the locate-then-edit cluster.
  1. Popular Knowledge Propagates More Errors in LLM Knowledge Updating (2026)
  2. MAPLE: Multilingual Evaluation of Parameter Efficient Finetuning of Large Language Models (2024)
  3. StatLLaMA: Multi-stage training for domain-optimized statistical large language models (2025)
  4. StatLLaMA: A multi-stage training framework for building a domain-optimized statistical language model (2026)
  5. DoRA: Enhancing Parameter-Efficient Fine-Tuning with Dynamic Rank Distribution (2024)
  6. Improving Language Plasticity via Pretraining with Active Forgetting (2023)
  7. Generation-Augmented Generation: A Plug-and-Play Framework for Private Knowledge Injection in Large Language Models (2026)
  8. Parameter Efficient Quasi-Orthogonal Fine-Tuning via Givens Rotation (2024)
  9. ConStruct-VL: Data-Free Continual Structured VL Concepts Learning* (2022)
  10. Mechanistic Analysis of Catastrophic Forgetting in Large Language Models During Continual Fine-tuning (2026)

### LOKI: Memory-Free Null-Space Constrained Lifelong Knowledge Editing (2606.19679)
Graph: https://www.connectedpapers.com/main/15a4b9d5418b5ae0e6cd4f03bbaeb3a495d86e78/graph — 39 nodes; .bib (39 entries): `/Volumes/memit/llm-database-poc-mirror/connected-papers-knowledge-graphs/INBOX/ConnectedPapers-for-LOKI%3A-Memory%20Free-Null%20Space-Constrained-Lifelong-Knowledge-Editing.bib`
  1. MEMOIR: Lifelong Model Editing with Minimal Overwrite and Informed Retention for LLMs (2025)
  2. MetaKE: Meta-learning Aligned Knowledge Editing via Bi-level Optimization (2026)
  3. When to Write and When to Suppress: Route-Specialized Dual Adapters for Memory-Assisted Knowledge Editing (2026)
  4. Evaluating the Reversal Curse in Model Editing (2023)
  5. Relaxing the Constraints: A Dual-Importance Projection Mechanism for Lifelong Model Editing (2026)
  6. A Dual-Axis Taxonomy of Knowledge Editing for LLMs: From Mechanisms to Functions (2025)
  7. Beyond Local Edits: Embedding-Virtualized Knowledge for Broader Evaluation and Preservation of Model Editing (2026)
  8. Is Model Editing Built on Sand? Revealing Its Illusory Success and Fragile Foundation (2025)
  9. UnKE: Unstructured Knowledge Editing in Large Language Models (2024)
  10. Benchmarking and Rethinking Knowledge Editing for Large Language Models (2025)

## InfraNodus extension output

Not available — extension not present in this Chrome (see Reachability). Nothing was triggered.

## NotebookLM answers (verbatim; "Thoughts / expand_more" UI chrome and inline citation-number markers are retained as captured)

### Notebook "The Model as a Graph: Querying LLM Weights with Larco" (https://notebooklm.google.com/notebook/23ba5f2d-8317-4412-bb8a-f7c30af4c017; 50 sources)
Question: "Which sources discuss editing or inserting multi-token or multi-word values into model weights, and what do they report about paraphrase or held-out recall?"

Sources the answer names: "MASS-EDITING MEMORY IN A TRANSFORMER" (MEMIT paper); "Understanding Parametric Knowledge Injection in Retrieval-Augmented Generation" (P-RAG / PT-RAG); "ROME vs. MEMIT: The Evolution of Mass-Editing Transformer Memory"; "Neural Architecture for Persistent Agentic Systems" (Deep Research Report). Numeric citation chips were not resolvable to source names from the DOM.

```
Thoughts
expand_more
Several sources in your notebook directly address the challenge of editing or inserting multi-token and multi-word values into model weights, evaluating both paraphrase recall (recalling the value when asked via rephrased prompts) and held-out recall / logical propagation (generalizing to related, unedited facts or reverse relations)
1
more_horiz
.
1. Key Sources Discussing Multi-Token Weight Editing
"MASS-EDITING MEMORY IN A TRANSFORMER" (MEMIT Paper): Explores inserting multi-token target objects o into transformer Feed-Forward Networks (MLPs) as (subject,relation,object) triplets
1
4
. It calculates target vectors (δ
i
	​

) by optimizing the negative log-likelihood across all tokens of the multi-word target across diverse prompt prefixes
5
6
.
"Understanding Parametric Knowledge Injection in Retrieval-Augmented Generation" (P-RAG / PT-RAG): Investigates encoding multi-word passages and multi-sentence documents directly into model weights via lightweight LoRA adapters (Parametric RAG) using gradient optimization on augmented question-answer pairs and rewritten text variants
3
more_horiz
.
"ROME vs. MEMIT: The Evolution of Mass-Editing Transformer Memory": Compares single-fact (ROME) and mass-fact (MEMIT) weight updates, analyzing how multi-word factual updates generalize across prompt phrasings and languages
2
10
.
"Neural Architecture for Persistent Agentic Systems": Discusses hardwiring multi-word foundational schemas, SEO entity structures, and proprietary API logic directly into model MLP weights via key-value parameter updates
11
12
.
2. Reported Findings on Paraphrase Recall
Paraphrase recall measures whether the model correctly retrieves the inserted multi-token value when prompted with rephrased versions of the training statement
13
14
:
High Paraphrase Success at Scale (MEMIT): Single-fact updates via ROME generalize well for isolated edits (even across different languages or creative formats like poetry)
2
, but collapse under sequential editing
15
16
. MEMIT solves this sequential bottleneck, achieving 89.7% Paraphrase Accuracy on 10,000 edits in the zsRE benchmark and 88.6% Paraphrase Success (PS) on COUNTERFACT in GPT-J (6B), compared to ROME's drop to ~19.6% and 50.4% under mass edits
17
18
.
Lossy Fidelity in Parametric RAG (P-RAG): LoRA-based parameterization captures document-level semantics and successfully answers rephrased queries
19
20
. However, compared to explicit text context (T-RAG), purely in-weight LoRA updates suffer from "lossy" information fidelity, occasionally losing fine-grained multi-word entity details
21
22
. Combining parametric injection with explicit text tokens (PT-RAG) yields the highest paraphrase and exact-answer accuracy
22
23
.
3. Reported Findings on Held-Out Recall and Logical Propagation
Held-out recall examines whether inserting a multi-token value propagates logically to connected facts or reverse relations that were not explicitly included in the edit payload
24
25
:
Directional Limitation of In-Weight Edits: The MEMIT authors explicitly report that direct parameter edits are strictly directional (subject,relation,object) representations
24
. For instance, updating the association "Tim Cook is the CEO of Apple" does not automatically update the held-out reverse query "The CEO of Apple is Tim Cook", which must be processed as a separate edit
24
.
The "Ripple Effect" Bottleneck: Model editing struggles with multi-step logical deduction on held-out facts
25
. For example, using an in-weight edit to update "The Prime Minister of the UK is Keir Starmer" enables the model to answer direct questions and paraphrases about the Prime Minister, but it fails to update held-out logical consequences (e.g., asking "Who is the Prime Minister's wife?" may still yield the un-edited answer "Carrie Johnson")
25
.
Cross-Task Generalization in P-RAG: Parametric LoRA adapters trained on QA-style objectives demonstrate solid transferability to held-out non-QA tasks with distinct prompt structures—such as Fact Verification (FEVER) and Slot Filling (Zero-Shot-RE)
26
27
. This confirms that in-weight LoRA injections store generalized, abstract document priors rather than rigid, prompt-specific templates
27
28
.
💡 Next Step Suggestion: Would you like to explore how hybrid architectures (like PT-RAG) combine in-weight edits with token-based retrieval to overcome these held-out recall and logical propagation limits?
```

### Notebook "LLM as Database Agent Harness Integrated Specification v1.2" (https://notebooklm.google.com/notebook/f667f1f2-7624-4039-b521-6ca37b437b6b; 25 sources)
Question: "Which spec sections forbid a read-time lookup for domain_concept values, and what would have to change in the spec if the write engine were continued pretraining or a merged LoRA adapter instead of MEMIT?"

Notebook source set (panel): llm-as-database-v1_2-integrated-spec.md; llm-as-database-agent-harness-framework.md; memit-research-paper.pdf; Quantitative Thresholds and Capacity Ceilings in Model Editing; gap-backlog-v4.md; tension-map-v4.md; llm-memory-layer.md; 2512.13564v2.pdf; 2601.11653v1.pdf; GitHub chrishayuk/larql; plus general web/background sources. Citation chips (numbers 1–24) could not be mapped to individual sources from the DOM; the answer cites spec sections by number.

```
Thoughts
expand_more
1. Spec Sections Forbidding Read-Time Lookups for domain_concept Values
The specification explicitly replaces read-time lookups (such as RAG, vector similarity search, or context-window prompt injection) with in-weight parametric learning for domain knowledge
1
2
.
The primary sections enforcing this boundary include:
Part I, §1 (Purpose and Paradigm): Establishes the foundational paradigm shift from in-context learning (retrieval-augmented generation, transient context windows) to in-weight learning (permanent semantic memory physically compiled into model weights)
1
. It mandates that validated semantic state is compiled directly into the model's Feed-Forward Network (.vindex), eliminating prompt reconstruction and read-time retrieval for agent workflows
1
2
.
Part III, §11.2 (Content-Scoped Authoritative Medium — D42): Formally assigns authoritative media by content type
3
. While Git is designated as the authoritative medium for structural_entity knowledge (code syntax), the .vindex model weights are strictly authoritative for Layer 4 domain_concept and constraint_rule knowledge
3
. Storing or fetching domain_concept data via external text lookups or transient context bypasses this authoritative assignment
3
.
Part IV, §13.1 (Native State Awareness): Forbids read-time semantic search when agents access domain state
4
. It mandates that agents query the LLM as a zero-latency graph database through native weight activation rather than context window injection, explicitly stating that "the model has the project's entire history baked into its FFN"
4
.
Framework Overview, §2.1 & §15.1: Directly contrasts temporary context retrieval with permanent weight injection, noting that domain_concept triples bypass token limits and retrieval latency because they are hardcoded into feature slots via INSERT INTO EDGES statements
2
more_horiz
.
2. Changes Required if the Write Engine Used Continued Pretraining or Merged LoRA Adapters
Section 8.2 (D12) explicitly designates MEMIT as the write engine, ruling out ROME, GRACE, and full fine-tuning
7
8
. If the write engine were replaced with continued pretraining (gradient-based fine-tuning) or merged LoRA adapters (e.g., CoLoR or ELDER), significant structural modifications across the specification would be required:
A. Write Engine Directives and Safeguards (§8.2, §8.5, §17)
Compiler Directives: MEMIT-specific directives like SET TARGET_LAYERS (L15–L25 FFN targeting)
7
9
, SET ORTHOGONAL_PROJECTION = TRUE
10
, and engine-computed attention_weight (derived from MEMIT covariance matrix inversion C
0
	​

=λE[kk
T
])
7
11
 would become obsolete.
Safeguard Replacement: MEMIT’s orthogonal projection and covariance balancing
7
 would need to be replaced by gradient-based anti-forgetting mechanisms (e.g., KL-divergence regularization, replay buffers, or weight-decay penalties for pretraining) or low-rank projection bounds (r,α) for LoRA adapters
12
more_horiz
.
B. Patch Format, Patch Sizes, and Capacity Caps (§8.4, §8.8, §10.3)
Overlay Artifacts (.vlp / .vindex Tiers): MEMIT writes lightweight, closed-form matrix overlays (~10 KB per fact patch)
15
16
. Continued pretraining modifies full model weights directly, eliminating file-level overlay swapping
14
. Merged LoRA adapters require tracking adapter rank matrices (A and B) and executing tensor addition (W
0
	​

+ΔW)
14
.
Volumetric Caps and Sub-Batching (T6, GAP-1): The 2,000-edge sub-batch ceiling, 1,500-edge drift warning, and 8,000-edge hard trigger
17
 are calibrated specifically around MEMIT's closed-form batch matrix inversion limits
8
18
. Continued pretraining would redefine batching around dataset epoch iterations, gradient accumulation steps, and learning rate schedules
14
.
C. Rollback, Compaction, and 2PC Synchronization (§6.3, §8.4, §11.4)
Rollback Mechanics: With MEMIT, rolling back an invalid transaction simply requires unloading a .vindex overlay file
19
. With continued pretraining, rollback is non-trivial and requires restoring full model checkpoint snapshots
14
. Merged LoRA adapters would require explicit tensor subtraction (W
merged
	​

−A×B) or an adaptive routing layer (such as WISE or ELDER) at inference time rather than static weight merges
20
.
Compile Latency & L1 Cache (§18.1): MEMIT computes closed-form updates in seconds without GPU backpropagation loops
15
21
. Continued pretraining requires multi-pass gradient descent, substantially increasing L1 cache compile times, extending Two-Phase Commit (2PC) timeout bounds, and increasing compute overhead
14
22
.
💡 Next Step: Would you like to explore how the L2 Probe Family (§21) and Semantic Assertion Criterion verify whether newly compiled facts fire correctly in inference after a write operation
23
24
?
```

Caveat for the operator: the answer's §8.2 "L15–L25 FFN targeting" and "~10 KB per fact patch" are the notebook's readings of the spec sources; the program's actual Qwen2.5-3B edit uses layers 4–8. Check against the spec text before relying on them.

## Side stores met (logged, not ranked — operator ruling)
WISE (in LKS reference list); MEMOIR (LOKI graph); NeuralDB: Scaling Knowledge Editing in LLMs to 100,000 Facts with Neural KV Database (BetaEdit graph); "When to Write and When to Suppress: Route-Specialized Dual Adapters for Memory-Assisted Knowledge Editing" (LOKI graph); Knowledge Externalization: Reversible Unlearning and Modular Retrieval in MLLMs (Google Scholar); P-RAG / PT-RAG (NotebookLM answer); Generation-Augmented Generation: private knowledge injection (Markov graph; title only).

## New to the pass

Papers not in the known list that, from what the page showed, write multi-token / new-entity knowledge into weights (or expand vocabulary to carry it). "Opened" = S2 TLDR or abstract read on the page; "title only" = seen only as a title in a results list or graph panel, content not verified.

Opened (TLDR/abstract seen):
- **Latent Knowledge Scalpel (LKS)** — arXiv 2508.03741, S2 05354809332ef3c8c94a90dde8fd4b3413088abc, ECAI 2025. TLDR: edits the latent knowledge of specific *entities* via a lightweight hypernetwork for precise, large-scale editing. Entity-level (not token-level) editing is the closest hypernetwork analogue to our coined-value write.
- **MeG: Massive Editing for LLMs Based on Dynamic Weight Generation** — arXiv 2512.14395, S2 1b61cde6c4af087724f99851175d5f6dd7c42f4e. TLDR: generates weight updates dynamically for large-scale KE, reporting Reliability/Generality/Locality gains. Hypernetwork alternative to closed-form MEMIT.
- **Locating and Editing Factual Associations in Mamba** — arXiv 2404.03646, S2 5664f7f52264ff656faa3671d83e2009f4f390fd, 48 S2 cites / 51 GS. TLDR: causal tracing of factual recall in the Mamba SSM (middle-layer components at last subject token). The only "knowledge editing Mamba" hit; relevant if a non-transformer write target is ever considered.
- **Consistency-Aware Editing for Entity-level Unlearning** — arXiv 2601.08840 (corpus-seen by id, listed because it is entity-level editing; it is *deletion*, not insertion).

Title only (not opened; verify before use):
- **KAMEL: Knowledge Analysis with Multitoken Entities in Language Models** (AKBC 2022; GS cited-by 38) — the multi-token-entity probing benchmark; directly about recall of multi-token objects.
- **Can LMs learn new entities from descriptions? Challenges in propagating injected knowledge** (ACL 2023; GS cited-by 91) — new-entity injection into weights with propagation tests.
- **TISKE: Two-Stage Incremental and Scalable Knowledge Editing for LLM-Based Intelligent Services** (2026; S2 8067e571c67eba175113e0e5619bed8a49730aab; no arXiv id shown) — the one highly-influential citer of LKS.
- **Defragmenting Language Models: An Interpretability-based Approach for Vocabulary Expansion** (arXiv 2604.16656) — vocabulary expansion; bears on the minted-token arm.
- **Beyond Initialization Loss: A Systematic Study of Token Embedding Initialization Strategies** (arXiv 2608.03494) — new-token embedding init; bears on the minted-token arm.
- **Medical knowledge representation enhancement in LLMs through clinical tokens** (Sci. Rep. 2026; GS cited-by 4) — new vocabulary tokens carrying domain knowledge.
- **TokAlign / TokAlign++** (arXiv 2506.03523 / 2605.13429) — vocabulary adaptation via token alignment (adjacent).
- **Precise Localization of Memories: fine-grained neuron-level KE** (arXiv 2503.01090; 27 S2 cites) — adjacent locate-then-edit.
- **Reinforced Lifelong Editing (RLEdit)** (arXiv 2502.05759; 43 S2 cites) and **PropMEND** (known) — hypernetwork editors from the "hypernetwork knowledge editing" query.
- **HiEdit / CaPEdit / TamEdit** (ACL 2026 main/findings; GS) — lifelong/meta-learned editing; title only.
- **Match the Distribution, Not the Compute: Post-Training Multi-Token Prediction Heads** (arXiv 2610.00888) — post-training MTP heads; adjacent to a multi-token readout.
- Connected Papers graph nodes (title only): UltraEdit (training-, subject-, memory-free lifelong editing); OrthoEdit (orthogonal subspace projection); LyapLock; Knowledge Decoupling via Orthogonal Projection; Relaxing the Constraints (dual-importance projection); Edit Less, Achieve More (dynamic sparse neuron masking); EvoEdit (lifelong free-text KE); REACT; A^3E compositional editing; Context-Robust Knowledge Editing; Uncovering Context Reliance in Unstructured KE; Perturbation-Restrained Sequential Model Editing; Neuron-Level Sequential Editing; MetaKE (two variants); Popular Knowledge Propagates More Errors in LLM Knowledge Updating; Reliable Batch-Sequential Model Editing via Enhanced Editing Anchor Compression (2026).

Not new / already in corpus (seen in results, skipped per brief): AlphaEdit, AnyEdit, AnyEdit++, GenRecEdit, MDM-KE 2606.03924, TimeROME-DLM, The Tokens Remember, Grounded Token Init 2604.02324, Memory as a Markov Matrix, CaseEdit 2505.19383 (inventory-seen), WikiBigEdit, SAKE, Norm Growth 2502.19416, Basis-Level Representation FT 2503.00306, Representation Shattering 2410.17194, KE-via-KL-self-distillation 2508.15807, PropMEND.
