# External-Evidence Verification Notes

CORPUS-style verification of external repos *before* the program leans on them (per `[[verify-external-artifacts-before-effort]]`). Each note records what the repo **actually** is (cloned + read, not described), the real numbers, and an honest verdict on whether it supports the hypothesis it was filed under in `docs/HYPOTHESIS_REGISTER_2026-06-18.md` §H. **These are external, single-author, unvetted-by-us repos — verdicts are about *relevance to our work*, not peer-review of their claims.**

---

## EV-1 — ELLMTrees-paper → filed under C2 / D2/D3 — **VERDICT: DOWNGRADE (tangential; not corroboration)**

_Verified 2026-06-19. Source: `skgallagher/ELLMTrees-paper` (TeX paper, 0★, ICLR-2026 format), cloned to `external_prior_art/ELLMTrees-paper`. Extracted from `paper_v2.tex` (abstract; §results, lines ~534–576)._

**Claimed relevance (the register lead):** "signal concentrated in attention KEY matrices → independent corroboration of our key-geometry framing of cross-entity interference (C2)."

**What it actually is:** A model-**phylogeny** paper — recovering a model's *fine-tuning lineage* (who descended from whom) from **weight-space distance**, scored against a known ground-truth tree with **Robinson–Foulds (RF) distance** under a 1,000-random-tree permutation null. Models: Flan-T5-base (250M), Pythia-160M, Llama-3.2-1B, Llama-3.1-8B. Nothing about knowledge editing, MEMIT, or read-correctness.

**Actual numbers:** Lineage signal concentrates in the attention **key projection matrices**: encoder `SelfAttention.k` misses only **4% of true clades (false-negative rate) vs ~9% elsewhere**; replicated — Flan-T5 k-matrices 10% vs 14%, Pythia-160M 13% vs 20%, Llama-3.2-1B `SelfAttention.k` again the carrier (FN 8% in blocks 0–1). Held-out behavioral probe tracks the null (behavior alone is a weak lineage signal). Rigorous methodology (cosine distance, permutation null, significance rising with tree size).

**Verdict — DOWNGRADE.** The repo's "key matrices" are the **attention W_k weight matrices**; our C2 "keys" are the **down_proj-input activation vectors** at the subject-last token (the MEMIT key→value sense) and their *collinearity*. **Same word, different object, different part of the transformer.** This is a *nominal coincidence*, **not** independent corroboration of our key-collinearity mechanism. Do not cite it as support for C2.
- **Residual (weak) value:** (a) its RF-distance / permutation-null **phylogeny method** could be a *tool* for D2 — quantifying the structure/separability of our edit-deltas against a random-relabel null; (b) the general theme "model-identity signal is low-dimensional and concentrates in attention" is loosely adjacent. Neither is load-bearing.
- **Caveats:** single author; provenance/auditing motivation, not editing; the 4%-vs-9% gap is modest and clade-FN-based, not a parameter-importance claim about where *facts* live.

**Register action:** §H C2/D2 entry corrected to "different sense of 'key'; methodology possibly reusable for D2; NOT C2 corroboration."

---

## EV-2 — xai-knowledge-graph → filed under B2 / B3 / E3 — **VERDICT: CONFIRMED but SCOPED (weak, real)**

_Verified 2026-06-19. Source: `Pra0809/xai-knowledge-graph` (0★, Python/Jupyter, full pipeline + trained models), cloned to `external_prior_art/xai-knowledge-graph`. Extracted from `README.md` (Headline results, §4) + `models/*/results.json`._

**Claimed relevance (the register lead):** "concrete GraphRAG-vs-RAG study → direct input to the 'is L2 in-weight even needed vs retrieval + external query index' decision (B2/B3) and the reverse-lookup/aggregation read-contract (E3)."

**What it actually is:** A genuine end-to-end KG over **3,907 arXiv XAI papers** — Neo4j property graph + RDF/OWL + PyKEEN embeddings (TransE/RotatE) + a **GraphRAG pipeline (NL → Cypher → graph → LLM answer)** benchmarked against **vanilla vector RAG**. Real code, trained models, and saved results.

**Actual numbers:**
- KG embeddings: TransE baseline **MRR 0.220 / Hits@10 0.414**; citation link-prediction **precision@10 = 0.90** (RotatE+NSSALoss, 9/10).
- **GraphRAG vs vanilla RAG: win rate 6/10; completeness gap +1.9 of 5.** **GraphRAG wins on STRUCTURAL questions (counts, multi-hop, rankings); RAG wins on conceptual synthesis.** Author flags the LLM-as-judge has a **verification bias** (penalized correct DB-verified answers it couldn't confirm from retrieved abstracts).

**Verdict — CONFIRMED but SCOPED.** Unlike EV-1, the connection is **real**: this *is* a head-to-head of a **structured-graph query index vs vector retrieval** for reads — the exact tradeoff in our **B2** (external triple-index over a served model) and **E3** (reverse-lookup / aggregation / multi-hop read-contract). The finding **"structured KG query beats vector RAG on structural / multi-hop / aggregation reads"** is the right shape of evidence that an external **structured** index (not plain L1-KNN retrieval) is what recovers the relational read-contract — useful input to **B3** (whether in-weight L2 is needed).
- **How to use:** as a *directional prior* that the external-index path should be a **structured KG / GraphRAG**, not vector RAG, if we pursue B2. Worth a closer read of `notebooks/graphrag.ipynb` + `vanilla_rag.ipynb` if B2 becomes active.
- **How NOT to use:** not as a quantitative result for our setting. **Scope limits: n=10 questions (noisy 6/10), domain is research-paper QA (not entity–attribute facts like ours), single LLM-as-judge with admitted bias, single author.** Do not transport the win-rate.

**Register action:** §H B2/B3/E3 entry annotated "VERIFIED — structured KG query > vector RAG on structural/multi-hop reads (n=10, paper domain, judge-biased); directional prior for B2, not a transportable number."

---

## EV-3 — NeuralDB (arXiv 2507.18028) → filed under D9 / B3 / C1 — **VERDICT: REAL, HIGH-RELEVANCE LEAD (paper confirmed; repo unverified; not yet read in full)**

_Verified 2026-06-21 (abstract only). Source: ConnectedPapers AlphaEdit-graph node; arXiv abstract fetched via WebFetch (`arxiv.org/abs/2507.18028`). NOT cloned/read in full yet._

**Claimed relevance (the graph lead D9):** closest prior art to the LLM-as-database spec — frames linear locate-and-edit as **KV-database queries** and solves general-ability degradation with a **gated retrieval overlay that only fires on edited facts**.

**What it is (abstract-confirmed):** *NeuralDB: Scaling Knowledge Editing in LLMs to 100,000 Facts with Neural KV Database.* Authors Weizhi Fei, Hao Shi, Jing Xu, Jingchen Peng, Jiazheng Li, Jingzhao Zhang, Bo Bai, Wei Han, Zhenyuan Chen, Xueyan Niu (Huawei-affiliated). Models the existing linear L&E family as querying a KV database, then represents edited facts as a **neural KV database with a non-linear gated retrieval module** that "only operates when inference involves the edited facts," preserving general abilities. Tested **10,000 edits** on ZsRE + CounterFact with **GPT2-XL, GPT-J (6B), Llama-3 (8B)**; claims effectiveness scaling to **100,000 facts** (50× prior work).

**Verdict — REAL, HIGH-RELEVANCE LEAD (not yet load-bearing).** This is the nearest published instantiation of the spec's core "edited knowledge = a queryable KV store on a frozen base" idea, and its **gated overlay (route-only-edited-facts)** is exactly the structural-corruption-avoidance our G6.1/D1 cross-entity finding motivates (cf. WISE/GRACE; our C1/B3). 
- **How to use:** input to **B3** (is diffuse in-weight L2 even needed, vs a gated side-store?) and **D9/C1**. If B3/side-store becomes active, **read the paper + locate the repo first** (the abstract's gating mechanism — *how* it decides edited-vs-base at inference — was NOT in the fetched content and is the load-bearing detail).
- **How NOT to use:** do not assume a repo exists or that it serves on our CPU/llama.cpp deployment path — **no code link surfaced**; GitHub-check before any port ([[verify-external-artifacts-before-effort]]). Abstract-only; numbers unverified by us; not a benchmark we've reproduced.

**Register action:** §J D9 carries the "VERIFY REPO BEFORE PORT" flag; this note is the provenance.

---


## EV-4 — AnyEdit / FABLE / AnyEdit++ C10 triage → filed under C10 / G7 — **VERDICT: ANYEDIT FIRST, FABLE FALLBACK, ANYEDIT++ RISK NOTE**

_Verified 2026-06-26. Sources: `jianghoucheng/AnyEdit` cloned to `/tmp/AnyEdit`; `caskcsg/FABLE` cloned to `/tmp/FABLE`; arXiv pages for AnyEdit (`2502.05628`), FABLE (`2604.12559`), and AnyEdit++ (`2606.01053`). This is prior-art/implementation triage, not CORPUS evidence._

**Claimed relevance:** C10 needs a post-MEMIT rescue for project-coined multi-word semantic values after later/wider/strength/layer MEMIT knobs failed. The candidate family is autoregressive/per-token model editing.

**What the code actually shows:** AnyEdit ships `AlphaEdit_ARE/`, `memit_ARE/`, and `unke_ARE/`. Its relevant loop tokenizes `data["answer"]`, slices the target into windows (`window_size`/`overlap`), optimizes per-window target vectors while carrying previous deltas, then stacks targets into the MEMIT/AlphaEdit solve. It has Qwen2.5-7B hparams, but the repo assumes old deps (`transformers==4.23.1`, PyTorch 1.12-era stack) and A100 80G-class environment; its Qwen hparams are not a drop-in match for the local Qwen2.5-3B harness (`lm_head` vs local `model.embed_tokens`, different clamp/cov settings).

FABLE is real and relevant, but heavier: EasyEdit/UnKE-style code updates whole layer modules with optimizer steps, preservation examples, `sub_layers`/`target_layers`, and Qwen/Llama mask special cases. It is a fallback if AnyEdit is infeasible or fails cleanly, not the first port.

AnyEdit++ appears as a paper from quick search, but no runnable public repo surfaced in the quick GitHub/code search. It should inform risks around fixed-window/chunk crosstalk and Bayes-chunk ideas, not gate the current port.

**Verdict — ANYEDIT FIRST, VIABILITY-GATED.** This supports D-C10h-anyedit-triage: proceed with AnyEdit only through a code-level transplant audit into the local Qwen2.5-3B / `transformers==4.51.0` harness, preserving the science-path MEMIT primitives and LAW#5 inertness. The pilot criterion remains our science criterion, not AnyEdit's headline benchmark: A7 held-out paraphrase full-sequence with A1/A2 controls. Review/triage is decision support, not a result.

**Register action:** `docs/HYPOTHESIS_REGISTER_2026-06-18.md` gains `C10-ANYEDIT-PORT`; runbook §5.2 gains `D-C10h-anyedit-triage`.

---


## EV-5 — AnyEdit ConnectedPapers graph review → filed under C10 / G7 — **VERDICT: PLAN UNCHANGED; ADD TWO DIAGNOSTICS**

_Verified 2026-06-26. Sources: `research_and_specs/ConnectedPapers-for-AnyEdit%3A-Edit-Any-Knowledge-Encoded-in-Language-Models.bib` and `research_and_specs/ConnectedPapers-for-Connected-Papers-%7C-anyedit-paper-2.bib`. This is graph-neighborhood context / lead generation, not empirical evidence._

**Claimed relevance:** one final prior-art context pass before committing to the AnyEdit C10 path.

**What the files actually show:** the first graph is the relevant LLM knowledge-editing neighborhood around *AnyEdit: Edit Any Knowledge Encoded in Language Models* (`2502.05628`). It reinforces known leads: AnyEdit's autoregressive chunk/key-token paradigm, evaluation critiques (Built on Sand, Mirage/QAEdit, locality-metric critiques, superficial editing), preservation/scale risks (LyapLock, ReFEdit, NMKE, DeltaEdit), side-memory alternatives (WISE, NeuralDB, MindBridge), and successor/fallback ideas such as μKE. The second graph is a false-positive name collision: *AnyEdit: Mastering Unified High-Quality Image Editing for Any Idea* (`2411.15738`) and its neighbors are image/diffusion editing papers, not LLM knowledge editing.

**New practical value:** the graph does not alter the D-C10h route, but it adds two concrete diagnostics to the AnyEdit prereg/advisor packet:

1. **Context-reliance diagnostic.** `Uncovering Context Reliance in Unstructured Knowledge Editing` warns that unstructured/NTP-style edits can bind knowledge to the training context. If AnyEdit improves A7, test whether the gain survives a held-out paraphrase without canonical/context prefix. A context-prefix-only rescue is not a DB-like win.
2. **Chunk/window dependency logging.** μKE flags that window-based autoregressive methods can disrupt dependencies between earlier and later output tokens. The pilot should log target token length, AnyEdit window size/overlap, whether the target crosses a window boundary, and per-token continuation success.

**Verdict — PLAN UNCHANGED.** AnyEdit remains the first port target, still viability-gated by local transplant + LAW#5 + A7/A1/A2 held-out full-sequence. The new graph context adds prereg diagnostics and later fallback awareness; it does not promote AnyEdit, prove necessity, or justify running upstream as-is.

**Register action:** add `C10-ANYEDIT-DIAGNOSTICS` to the hypothesis register and update runbook/checkpoint context.

---


## EV-6 — Supplied AnyEdit-neighborhood research sweep → filed under C10 / G7 / B3 / C1 / C2 — **VERDICT: ANYEDIT STILL FIRST, BUT UPGRADE THE GATE; NEURALDB/SIDE-STORE PRESSURE INCREASES**

_Verified 2026-06-26. Sources reviewed: user-supplied GitHub/arXiv links plus targeted adjacent searches. This is prior-art / implementation triage and F1 architecture context, not CORPUS evidence and not a local run._

**Claimed relevance:** before committing engineering effort to the C10 AnyEdit path, review all supplied science around AnyEdit, AlphaEdit/EasyEdit successors, long-form editing, locality/regularization, and anything bearing on the LLM-as-Database spec.

**Name-collision / non-LLM filters (do not route into C10):**
- `DCDmllm/AnyEdit` (`arXiv:2411.15738`) is the CVPR image-editing AnyEdit, not the LLM knowledge-editing AnyEdit. It is only a name-collision warning.
- `bimsarapathiraja/refedit` / `arXiv:2506.03448` is also image-editing / diffusion-model work, not LLM parametric knowledge editing.

**C10-direct cluster (long/multi-token value realization):**
- **LLM AnyEdit remains the first code target:** `jianghoucheng/AnyEdit` (`arXiv:2502.05628`) is the relevant repo. Local `/tmp/AnyEdit` points to this repo. Code inspection confirms `AlphaEdit_ARE/`, `memit_ARE/`, Qwen2.5-7B hparams, and an autoregressive `compute_z` loop that tokenizes `data["answer"]`, slices by `window_size`/`overlap`, carries previous deltas, and returns multiple target vectors. It is mechanistically matched to C10's W-realization failure, but it assumes old deps (`transformers==4.23.1`) and A100-class headroom.
- **μKE / Matryoshka Unstructured Knowledge Editing** (`PurCL/muke`, `arXiv:2504.01196`) is highly relevant. It argues AnyEdit-style window-by-window updates can miss dependencies between early memory updates and later output tokens; it proposes a Matryoshka objective so earlier working-memory shifts contribute to later target tokens. This does not replace the first AnyEdit audit, but it upgrades the pilot diagnostics and becomes the first fallback if fixed-window AnyEdit partially works or fails by window-boundary / later-token collapse.
- **AnyEdit++** (`arXiv:2606.01053`) strengthens the same risk: fixed-window chunking can disregard semantic/logical structure; Bayes-Chunk / surprisal boundaries are a paper-level lead unless runnable code appears. Treat as prereg risk context, not a first port.
- **COIN / context reliance** (`arXiv:2602.19043`) is a false-positive guard: unstructured/NTP-style edits can bind recall to the training context. The AnyEdit pilot must test held-out paraphrase alone vs canonical/context-prefix; a context-prefix-only rescue is not database-like.
- **SUIT** (`holi-lab/SUIT`, `arXiv:2509.24502`) is a serious same-family fallback/diagnostic: it constrains key/value computation to edit-critical subspaces, supports Qwen2.5, and uses a modern `transformers==4.51.3`-era stack. It targets specificity/preservation more than long continuation realization, so it is not first for C10, but it is a better fallback than broad full-module optimization if AnyEdit over-edits.

**Scale / sequential / preservation cluster (important, not first C10 moves):**
- **NSE** (`jianghoucheng/NSE`, `arXiv:2410.04045`) targets sequential forgetting with neuron-level weights updating and original-weight value computation. Relevant to incremental/lifelong edits, not the immediate batch C10 long-value rescue.
- **ENCORE / lifelong regularization** (`scalable-model-editing/knowledge-editing-regularization`, `arXiv:2502.01636`) identifies over-optimized activations and norm growth as sequential-edit degradation drivers; relevant to later C1/C3/sequential health, not a direct C10 continuation fix.
- **LyapLock** (`caskcsg/LyapLock`, `arXiv:2505.15702`) frames sequential editing as constrained stochastic programming with long-term preservation constraints. Relevant to incremental mode / drift governance; not a first C10 port.
- **ECE** (`tianyuzhangterry/ECE`) uses explainability-driven adaptive neuron identification and clustering for efficient batch optimization. Relevant to scaling/edit batching; heavier and not as directly matched to the C10 failure.
- **SetKE** (`weiyifan1023/SetKE`, `arXiv:2504.20972`) explicitly studies Knowledge Element Overlap, especially same subject+relation with multiple objects. It is close to our relation-concentration / overwrite concerns and useful C2/C1 context, but not a C10 long-value rescue.
- **LocFT-BF** (`ICT-STAR/LocFT`, `arXiv:2509.22072`) argues model-editing fine-tuning failures often come from depth-first per-sample pipelines; breadth-first minibatch localized fine-tuning can scale much better, including Qwen2.5. This is a regime-change candidate if locate-and-edit keeps failing, but it changes the science path more than an AnyEdit transplant.
- **MALMEN** (`ChenmienTan/malmen`, `arXiv:2311.04661`) and **MetaKE** (`arXiv:2603.12677`) are meta-learning / bi-level optimization paths for massive editing or alignment between target-representation and downstream realization. They are real but heavier fallback families.
- **NMKE** (`LiuJinzhe-Keepgoing/NMKE`) appears to be a rough AlphaEdit/EasyEdit-derived repo that requires replacing `modeling_llama.py` in a conda environment and swapping AlphaEdit core files. It is not a clean first transplant target under our pinned local harness.

**Evaluation / query / architecture cluster (F1-wide relevance):**
- **NeuralDB** (`arXiv:2507.18028`) is now upgraded from abstract-only to high-relevance architecture context. It explicitly reframes MEMIT/AlphaEdit-like locate-and-edit as querying a KV database, then replaces the linear perturbation with a gated neural KV retrieval module that returns a residual only for matched edited facts and zero otherwise. It claims 10k-100k edit scalability and easier add/delete/modify operations. This is not a C10 fix under the current in-weight `.vindex` target, but it strongly pressures the B3 / side-store / gated-overlay alternative and should be carried into F1 architecture discussion.
- **SCR / Selective Contextual Reasoning** (`arXiv:2503.05212`) is a direct counter-prior to pure model editing: it argues external contextual updating beats ten editing methods across reliability/generalization/locality/portability. It reinforces that accepting C10-bounded hybrid is scientifically serious, not a failure to find a method.
- **MindBridge** (`arXiv:2503.02701`) and WISE/GRACE-style memory approaches keep the memory-augmented / model-agnostic side-store branch live for cross-model and high-volume updates.
- **Locality-evaluation critique** (`arXiv:2601.17343`) warns that common specificity/locality metrics are insensitive and can be dominated by fixed-answer or fluency biases. For AnyEdit/SUIT/side-store comparisons, keep exact held-out read metrics for C10 but also add distributional/logit-delta locality or bystander behavior where side effects matter.
- **KELE / knowledge erasure for multi-hop** (`arXiv:2408.12456`) is relevant to old-knowledge residue and multi-hop reasoning after edits, mainly C8/C9/R9/C2 read-contract context.
- **ConceptEdit/ConKE** (`arXiv:2412.11418`) is commonsense-concept editing context; useful for F1 coverage but not directly matched to the project-coined multi-token value wall.

**Verdict — ANYEDIT FIRST, UPGRADED GATE.** The new sweep does **not** justify pivoting away from the AnyEdit code-level viability audit. It **does** change the audit from "AnyEdit only" to "AnyEdit with explicit μKE/AnyEdit++/COIN/SUIT-derived guards." The first science path remains: transplant the official AnyEdit ARE target-vector/window loop into the local Qwen2.5-3B / `transformers==4.51.0` harness, preserve local MEMIT/AlphaEdit primitives, define/pass LAW#5 inertness, then pilot A7 + A1/A2. The prereg/advisor packet must include: target token length, window size/overlap, boundary crossing, per-token continuation by window, held-out paraphrase alone vs canonical/context-prefix, A1/A2 controls, and locality/bystander deltas. If AnyEdit is viable but fails by dependency/window behavior, μKE is the next most targeted fallback. If it over-edits, SUIT is the cleaner specificity-preserving fallback. NeuralDB/SCR/MindBridge remain broader F1 architecture alternatives, not C10 in-weight rescue evidence.

**Register action:** update C10-ANYEDIT-PORT / C10-ANYEDIT-DIAGNOSTICS, add a side-store/gated-overlay pointer for B3/F1 architecture, and update runbook/checkpoint/program-state/memory with thin EV-6 pointers.

---

### Method
Repos cloned shallow into `external_prior_art/` when repo-backed; key files (paper TeX, README, `results.json`) read directly. ConnectedPapers BibTeX exports live in `research_and_specs/` and are treated as lead-generation context only. Verdicts judge **relevance to our hypotheses**, applying the discipline that a lead's headline (and a triage summary) can mis-map to our work — EV-1 is a concrete example (the "key matrices" naming collision). EV-3 is abstract-only (paper existence confirmed, repo + mechanism detail NOT yet verified) — flagged accordingly.
