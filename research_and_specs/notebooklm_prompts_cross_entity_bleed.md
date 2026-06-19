# NotebookLM Prompts — Cross-Entity Read Corruption Blocker (corpus mining)
_Authored 2026-06-18. 10 prompts to run against the NotebookLM corpus (initial LLM-as-DB research + broad relevant sources + references). Companion to `perplexity_prompt_cross_entity_bleed.md` (open-web SOTA). NotebookLM answers ONLY from the corpus and cites sources — these are engineered to mine what the corpus already holds, including OUR spec/council material that Perplexity cannot see._

**The blocker (shared context for all prompts):** We store facts in-weight in a small dense transformer's FFN via MEMIT-class locate-and-edit (in-solve AlphaEdit: closed-form down_proj update + covariance null-space projection + preserved-key term), on a frozen base for CPU serving. Storing MANY facts that share a relation (e.g., 50 capitals) progressively corrupts the top-1 reads of OTHER, un-edited entities at that same relation — and it WORSENS with the number of edits (held-out correctness 100→92→58→42% at N=0→26→50→100). Write-side, same-entity multi-field, and global capability are all fine; the failure is specifically cross-entity, same-relation specificity collapsing with scale.

**Usage notes:** run each prompt separately (NotebookLM handles one focused question best). All prompts end by asking for source citations + quoted passages + an explicit "not covered in the corpus" flag where applicable. P7 mines OUR own spec/council docs specifically.

---

### Prompt 1 — Map every discussion of the phenomenon
Across all sources, find every discussion of knowledge editing damaging facts that were NOT the target of the edit — i.e., loss of "locality" or "specificity," the "ripple effect," or interference with unrelated or related-but-unedited facts. For each instance: quote the passage, cite the source, and classify it as (a) same-entity bleed (the edited entity's other attributes), (b) cross-entity bleed (other entities sharing the relation), or (c) general capability loss. Explicitly flag which sources, if any, address CROSS-ENTITY interference (different entities that share a relation) as a distinct problem.

### Prompt 2 — The mechanism (why does it happen)
Synthesize what the sources say about the MECHANISM behind editing interference: superposition, polysemanticity, knowledge neurons, shared/distributed feature directions, key (k-vector) collision at shared tokens, and the limits of covariance/null-space protection. Specifically: why would editing many facts that share a single relation degrade OTHER entities' facts at that same relation? Is the idea that a "shared relation direction" is high-variance (and thus hard to protect) supported anywhere? Quote and cite; note where sources agree and where they conflict.

### Prompt 3 — Methods that preserve unrelated knowledge during editing
List and compare every method or technique in the corpus aimed at PRESERVING untouched knowledge during editing: locality regularizers, KL/essence constraints, null-space or orthogonal projection, AlphaEdit, preserved-key/covariance terms, RECT/PRUNE/O-Edit or similar. For each: the precise interference it targets, how it works, and any reported limitation at high edit volume or under sequential editing. Cite sources and quote the key claims.

### Prompt 4 — Scaling, sequential/lifelong editing, and a capacity ceiling
What do the sources say about how editing quality degrades as the NUMBER of edits grows — sequential editing, lifelong editing, mass editing, error accumulation, catastrophic forgetting? Is there any discussion of a capacity CEILING (how many edits before locality/specificity collapses), or of error bounds that grow with edit count, batch size, or residual distance? Quote the specific claims, cite sources, and note any quantitative thresholds mentioned.

### Prompt 5 — Disentanglement, sparse autoencoders, monosemantic features
Surface any corpus content on DISENTANGLING knowledge representations: sparse autoencoders (SAEs), dictionary learning, monosemantic vs polysemantic features, feature steering, or separating entity-specific from relation-shared structure. Could any of these be used to make a weight edit touch only entity-specific and relation-specific features instead of a shared relation direction? Note specifically whether any source connects sparse/dictionary features (often trained on the residual stream) to editing the MLP/down-projection weights. Cite and quote; clearly flag if the corpus does not cover this.

### Prompt 6 — Parameter-preserving vs parameter-modifying, and hybrids
Compare what the sources say about PARAMETER-PRESERVING editing (GRACE, codebooks, adapters, external/retrieval memory) versus PARAMETER-MODIFYING editing (ROME/MEMIT/AlphaEdit) with respect to locality/specificity and cross-fact interference. Do any sources report that parameter-preserving methods avoid cross-fact bleed by construction, and at what cost (robustness, generalization, inference/CPU overhead)? Do any propose HYBRID designs (some facts in-weight, some in an external store)? Cite, quote, and lay out the tradeoffs.

### Prompt 7 — What OUR spec and council material assume and require (corpus-unique)
Using OUR own specification and framework-council documents specifically: extract everything about (a) cross-entity isolation / specificity, (b) the "write volume vs edit locality" tension, (c) polysemantic risk and "disambiguation anchors," (d) the batched "Project Genesis" write, and (e) any "maximum safe write volume with locality still holding" requirement. Quote the exact contracts, constraints, and open questions. Then state plainly: what does our spec ASSUME about edit locality that an empirical cross-entity-at-scale failure would violate?

### Prompt 8 — Batched vs sequential editing
Do any sources distinguish BATCHED editing (many facts solved together in one update) from SEQUENTIAL editing (one fact at a time)? Which is reported as safer for preserving unrelated facts, and why? Is there any claim that solving many shared-relation facts together balances the interference, or conversely concentrates it? Quote, cite, and flag if the corpus is silent on this.

### Prompt 9 — Measuring cross-entity locality correctly
What do the sources say about how to MEASURE locality/specificity properly — e.g., RippleEdits or similar cross-entity benchmarks, distributional/behavioral (logit-based) metrics, or critiques that simple token-match specificity metrics overstate locality? Identify the recommended metrics, benchmarks, and any methodological warnings about false-positive "high specificity." Cite and quote.

### Prompt 10 — Gap analysis and best leads (meta)
Given the specific problem — cross-entity, same-relation top-1 read corruption that AMPLIFIES with the number of in-weight edits on a small dense transformer served on CPU — do the following across ALL sources: (1) name the single most directly relevant idea and its source; (2) identify the most important angle on this problem that the corpus does NOT address (the gaps); (3) surface any contradictory claims between sources; (4) list the 3 most promising leads to prototype, each tied to the source it comes from and to whether it keeps facts in-weight. Be explicit about what is well-supported vs thinly-sourced in the corpus.
