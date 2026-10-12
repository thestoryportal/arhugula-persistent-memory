# Perplexity Deep Research Prompt — Cross-Entity Read Corruption in MEMIT-Class Knowledge Editing at Scale
_Authored 2026-06-18 for the LLM-as-Database program. Paste the block below into Perplexity (Deep Research / "Pro Search" with reasoning). Goal: surface current SOTA, the mechanistic reasoning, and novel/frontier approaches to the specific cross-entity-bleed-at-scale blocker we hit in G6.1._

---

## PROMPT (paste from here down)

**Role:** You are a research expert in mechanistic interpretability and knowledge editing of large language models (model editing, locate-and-edit methods, superposition/polysemanticity, sparse autoencoders, and lifelong/sequential editing). I need a deep, citation-backed survey of how to solve a specific, well-characterized failure mode. Prioritize peer-reviewed and arXiv work from 2023–2026; clearly distinguish established results from speculative/early-stage ideas; give arXiv IDs, venues, and dates.

### The exact problem I need solved

I am building a system that uses a transformer's FFN as an editable, queryable knowledge database: facts are stored **in-weight** as (entity, relation, value) triples via MEMIT-class **locate-and-edit** editing, on a frozen base model, so the edited model can be served on CPU. The write engine is **in-solve AlphaEdit**: a closed-form least-squares update to the MLP **down-projection** weights across a small band of layers, with a **null-space projection P** (built from the SVD of the layer input covariance, keeping low-singular-value directions, threshold ~0.005) and an **accumulated preserved-key term** (cache_c) so previously written facts are protected. Base model: small **dense** transformers (Qwen2.5-3B, 36 layers; targets generalize to Qwen3 1.7B/8B). Edit band is currently **early** (layers ~4–8).

**The failure (empirically measured):** When I store **many facts that share a relation** (e.g., the capitals of 50 different countries, written sequentially), the edits progressively **corrupt the top-1 reads of *other, un-edited* entities at that same relation.** Concretely, held-out (never-edited) entities' top-1 correctness on the shared relation degrades **monotonically with the number of edits**: ~100% → 92% → 58% → 42% at N = 0 → 26 → 50 → 100 edits. Key properties:
- It is **relation-specific**: an *unedited* relation on the same held-out entities stays ~100% stable. Only the relation being mass-edited bleeds.
- **Write-side is fine**: the edited facts themselves are retained (~98%) and every edit expresses when written.
- **Same-entity multi-field is fine**: editing entity X's capital does not corrupt entity X's other attributes.
- **Global capability is fine**: unrelated facts and general fluency are preserved.
- It is therefore specifically a **cross-entity, same-relation specificity/locality failure that amplifies with edit count** — the "ripple effect" / catastrophic interference, but in the cross-entity direction and growing with scale.

**My current mechanistic hypothesis:** the *shared relation direction* in activation space is **high-variance**, so it lies in the **editable** subspace rather than the low-singular-value null-space that the projection protects. Each edit at that relation nudges the relation-general representation, and the perturbations **accumulate** across edits, eventually flipping other entities' reads at that relation. The preserved-key term only protects the *specific edited* facts, not the un-edited entities that share the relation.

### What I have already tried (do NOT just re-recommend these — tell me what's better or why they're inherently limited)
- **Subject-keyed editing** (key at the entity token): causes within-entity bleed when storing multiple fields per entity.
- **Relation-inclusive keying** (key at the relation token): fixes same-entity, but *worsens* cross-entity bleed (the shared relation token collides across entities).
- **Post-hoc null-space projection onto other entities' keys**: insufficient (partial recovery only).
- **In-solve AlphaEdit with accumulated preserved keys**: fixes same-entity sequential accumulation, but does NOT prevent the cross-entity-at-scale corruption above.

### Questions I need answered (be specific and comparative)

1. **Current SOTA on cross-entity specificity / ripple-effect under MASS and SEQUENTIAL editing.** Which methods (2023–2026) most effectively preserve un-edited, same-relation facts when editing many facts that share a relation? Give measured results on relevant benchmarks (RippleEdits, KnowEdit, ConflictEdit, sequential/lifelong-editing suites). Cover at minimum: **AlphaEdit, RECT, PRUNE, O-Edit, EMMET, PMET, MEMIT-variants, WISE, GRACE, MELO, DAFNet, and any newer null-space/orthogonalization or lifelong-editing methods.** For each: the precise interference it targets and how it does numerically on cross-entity/specificity at scale.

2. **The mechanism / theory.** Why do locate-and-edit methods bleed across entities that share a relation? What does the literature say about: superposition/polysemanticity of relation directions; key (k-vector) collision at shared relation tokens; the limits of covariance-null-space protection when the interfering direction is high-variance; and whether there is a proven or conjectured **capacity ceiling** for in-weight editing before specificity collapses (as a function of edits-per-relation)? Is my high-variance-shared-direction hypothesis consistent with the literature, and what work formalizes it?

3. **Novel / frontier directions (most important).** What are the most promising recent or emerging approaches specifically aimed at *disentangling* entity-specific from relation-shared structure during editing? In particular:
   - **Sparse-autoencoder (SAE) / dictionary-learning guided editing** — editing or constraining updates in a monosemantic feature basis. Note: practical SAEs (e.g., Qwen-Scope, May 2026) are trained on the **residual stream**, while MEMIT edits **down_proj/MLP output** — has anyone bridged SAE features to MLP-weight edits, and how?
   - **Entity-disentangled or per-entity-subspace key construction** (so the "address" is genuinely relation + entity, not a shared relation direction).
   - **MoE-routing-aware editing** for sparse models.
   - **Hybrid parameter-preserving + parameter-modifying** schemes (e.g., route high-fan-out relations to an external/codebook memory while keeping low-fan-out facts in-weight).
   - Anything attacking *shared-relation interference* as an explicit objective.

4. **Batch vs sequential.** How does cross-entity interference differ between writing N shared-relation facts in a single batched solve versus sequentially one at a time? Is batching known to mitigate or worsen shared-relation collision, and why?

5. **Parameter-preserving vs parameter-modifying tradeoff for THIS failure.** For cross-entity specificity at scale specifically, do parameter-preserving methods (GRACE/codebook/retrieval-style) categorically avoid the failure, and at what cost (robustness, generalization, CPU-inference overhead)? What do hybrid architectures look like?

### Constraints (use to filter recommendations)
- Must be **in-weight** (the value proposition is parametric recall on CPU; pure external RAG defeats the purpose — but hybrids that keep most facts in-weight are in scope).
- **CPU-deployable inference**, edits stored as overlays on a **frozen base**, no full retraining of the base model.
- Small **dense** models (1.7B–8B), Qwen family preferred.
- Must preserve the wins we already have: same-entity multi-field storage and global capability.
- The target is to hold **both** same-entity multi-field **and** cross-entity same-relation isolation as the number of stored facts grows into the hundreds/thousands.

### Output format
Produce: (a) a ranked shortlist of the **most promising approaches** for our exact setup, each with mechanism, the interference it targets, measured cross-entity/specificity evidence, and concrete applicability/limitations for closed-form down_proj editing on a small dense CPU-served model; (b) a separate section on **mechanism/theory** answering whether a specificity ceiling is established; (c) a section flagging the **2–3 highest-upside novel directions** worth prototyping, with the specific papers/techniques to start from; (d) a list of **open research questions** the literature has NOT resolved. Cite everything (arXiv IDs, venues, dates) and flag any claim that is speculative or based only on an abstract.
