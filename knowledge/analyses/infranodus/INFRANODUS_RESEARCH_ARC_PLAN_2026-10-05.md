# InfraNodus research arc — plan (2026-10-05; mandated by D-C10k-rulings-1)

**Why this exists.** The operator ruled (D-C10k-rulings-1, 2026-10-05) that a side store is not F1 closure for C10 and that, before any in-weight route is committed, the program exhausts the literature it already holds and the literature it has not yet reached, using InfraNodus to find what close reading missed and what has not yet converged. The target is the C10 blocker first (a coined multi-word value written into weights and read back from held-out paraphrases), then every other open condition, then the spec as a whole. This is a knowledge-base arc, not a science result: it writes no CORPUS entry; its outputs are candidate solutions with a pre-registrable falsifier each, or logged dead ends. Fence unchanged: InfraNodus outputs are leads, never evidence.

**Standing facts that shape the mechanics.** The official MCP server exposes forty tools and no scientific-paper search; `get_more_tools` only completes the list for clients that load a reduced set, and this client already has the full set (checked 2026-10-05 against the npm readme, the repository source and `infranodus.com/mcp/tools`). The web app's Scientific Research import (Google Scholar, PubMed, arXiv results) saves graphs of type SCIENCE that the MCP tools can then read by name. So part 2 is driven from the operator's logged-in browser session; parts 1 and 3 run from the MCP alone. The Connected Papers exports (94 `.bib` files, outside git) carry 2,040 abstracts, so part 1 works on abstracts, not titles.

## Part 1 — mine what we already hold

**Sources** (`results/infranodus_research_arc_2026-10-05/segments/`, one paper per line: title, year, abstract):

| graph | file | contents |
|---|---|---|
| `llmdb-arc1-uncited-A-20261005` | `uncited_central_A_to2024.txt` | papers in ≥ 3 seed neighbourhoods, never cited in the repo, ≤ 2024 |
| `llmdb-arc1-uncited-B-20261005` | `uncited_central_B_2025on.txt` | same, 2025–2026 |
| `llmdb-arc1-repo-cited-20261005` | `repo_cited.txt` | papers the repo already cites (what we know) |
| `llmdb-arc1-uncited-two-20261005` | `uncited_two_graphs.txt` | papers in exactly 2 neighbourhoods, never cited (the second ring) |

**Calls.** `create_knowledge_graph` × 4 (`detectEntities` so method names survive); `difference_between_texts` with repo-cited first against the three uncited graphs (what our corpus lacks relative to the central literature); `merged_graph_from_texts` over the four; `generate_research_ideas` (`useSeveralGaps`) and `develop_latent_topics` (`question`) on the merged set; `search` across all `llmdb-*` graphs for the mechanism terms below; targeted reads of the abstracts the graphs point at.

**Pre-stated questions.**
- P1-Q1. Which uncited central papers describe a write mechanism for multi-token or novel targets: per-token target construction, embedding-side edits (subject word embedding, padding/right-embedding retrieval, token biasing), carrier or placeholder tokens, joint multi-layer target enrichment? Candidates visible from titles alone: SWEA, "Retrieving Padding Right Embedding", "Adaptive Token Biaser", "Joint Knowledge Editing for Information Enrichment and Probability Promotion", "From Backward Spreading to Forward Replay: Revisiting Target Construction", "Uncovering Overfitting in LLM Editing".
- P1-Q2. Which address key interference and superposition in batched or sequential solves (Q7): "Knowledge in Superposition", "Superimposed Noise Accumulation", "Neuron-Level Sequential Editing", "Subspace-Aware Key-Value Mappings", "Semantic Sparse Space"?
- P1-Q3. Which bear on the continuation objective, the W-realization wall of CORPUS/36 (no direct objective on tokens 2..N)?
- P1-Q4. Structurally, what does the difference graph say the repo-cited literature lacks relative to the uncited central literature?

## Part 2 — reach what we have not (operator's browser session)

Keyword passes in the Scientific Research app, each saved as a SCIENCE graph named `llmdb-sci-<slug>-20261005`, then analyzed by name from the MCP (`analyze_existing_graph_by_name`, `difference_between_texts` against part-1 graphs, `generate_research_questions`). First keyword set, each a separate graph:

1. subject word embedding editing language model
2. vocabulary expansion new token embedding initialization knowledge injection
3. multi-token target construction knowledge editing
4. key collinearity interference batched model editing superposition
5. novel entity injection continued pretraining unseen entities recall
6. carrier token placeholder token knowledge editing
7. frame-bound versus subject-bound factual recall localization
8. editing overfit paraphrase generalization locate-then-edit

Pre-stated question for each pass: does any item write a never-seen multi-token value into weights and score held-out paraphrase recall (the empty cell of sweep §12), and if not, which mechanism is closest and what is its falsifier here.

## Part 3 — convergence

`merged_graph_from_texts` over part-1, part-2 and the existing `llmdb-prior-art-*-20261004` graphs; `develop_conceptual_bridges` in `transcend` mode (creative reach is wanted here, labelled as such); `generate_research_ideas` with `useSeveralGaps` and `gapDepth` 1; `overlap_between_texts` between the uncited-central graphs and the program's C10 evidence graph (`llmdb-c10-knobs-20261004`, `llmdb-c10-anyedit-keying-20261004`) to find fragments that touch our own findings.

**Pre-stated questions.** P3-Q1: which pairs of mechanisms from different papers have never been combined and would, together, address the three C10 walls at once (subject keying, per-token continuation, key distinctness)? P3-Q2: which fragment, if true, changes the route decision (ii-b / ii-c / iv / i)? P3-Q3: which fragments bear on other open conditions (C1 scale, C3 firing under quantization, C5 compaction gate, C8 adversarial firing, C9 deletion)?

## Amendment 1 (2026-10-05, after advisor review FIX-FIRST and the first four graphs)

The advisor's review (`$CLAUDE_JOB_DIR/tmp/advisor_arc_plan.md`, verdict FIX-FIRST) and the first graphs agree on one thing: the question that decides the route is in papers' evaluation sections, and co-occurrence over abstracts cannot see it. The first two uncited-central graphs came back `biased` and `focused` with "editing" and "knowledge" carrying 60–72 % of betweenness even after generic vocabulary was stripped from the abstracts, because the titles carry the same words. The plan changes as follows; everything above stays as the map of sources.

1. **Exit condition and current default.** The arc closes when (a) the evaluation sections of the named candidates have been read against the empty cell (a coined, never-seen multi-word value written into weights by locate-then-edit and scored on held-out paraphrases) and (b) two consecutive part-2 passes add no new mechanism class to the table. Time box: this session plus one. If the arc finds nothing, the route taken is the standing recommendation of sweep §10.2/§12.1: pre-register (iv) mint-a-token as the cheap span-versus-novelty test, (ii-c) shallow-key/deep-value as the cheap attribution-guided variant, (ii-b) FOVEATED-style subject-anchored write as the heavy test, with (i) AKEW WikiUpdate calibration in parallel. That ranking is the prior P3-Q2 is measured against.
2. **The deciding check is full-text reading, not graphs.** For each named candidate (SWEA, Retrieving Padding Right Embedding, Forward Replay target construction, Joint Knowledge Editing for information enrichment, Adaptive Token Biaser, Knowledge in Superposition, Subspace-Aware Key-Value Mappings, Semantic Sparse Space, Editing Overfit, Heterogeneous Token Overfitting, Latent Knowledge Scalpel, DOW-KE) the evaluation section is read and the row records `eval-checked: full-text` with the section number. No row reaches ADOPT-TO-PREREG or DEAD-END from an abstract.
3. **Graphs keep one job: finding papers nobody has named**, with a calibration test. A planted positive (a paper known to matter and absent from every query term) must surface unprompted from the uncited graphs or the method is a summariser here and part 1 shrinks to retrieval plus reading. Graph creation uses `maxNodes` 500 and, where traceability matters, `statements` with a bibkey category per paper. P1-Q1–Q3 are answered by retrieval over the stored abstracts and by the full-text reads, not by gap structure.
4. **The difference call is run size-matched and in both directions**; a "lack" counts only if it survives both.
5. **Part 2 is logged**: for every pass, the query, date, result count and paper list are written to `results/infranodus_research_arc_2026-10-05/part2/`. Two channels: the Scientific Research import in the operator's logged-in InfraNodus session (SCIENCE graphs read back by name) and the arXiv export API over HTTPS (repeatable, logged). The arXiv MCP server the operator pointed to (`blazickjp/arxiv-mcp-server`) can be added later with `claude mcp add`; it wraps the same API.
6. **Verdict classes.** ADOPT-TO-PREREG / READ-NEXT / DEAD-END as before, plus SPECULATIVE-COMBINATION for anything produced by `transcend`-mode bridges: each part cites its own paper, and such a row cannot reach ADOPT until every part is checked in full text.
7. **Every row names the law it touches**: harness-only; embedding or vocabulary artefact (admissible as a `.vindex`-tracked artefact under D-C10k-rulings-1); or science path (`compute_z`, `execute_memit`, the solve), which needs isolation and an inertness proof under LAW#5 before any verdict is promoted.
8. **Premise checks recorded here.** 2,039 of 3,854 bib entries carry an abstract longer than 80 characters (2,124 distinct titles); "in repo" is a title-prefix match (presence, not depth of reading), so a loose match can leak and the uncited sets are read as leads only; the ≥ 3-neighbourhood filter biases toward what the program already reads, which part 2 is meant to offset. The three C10 walls are the ones named in `CORPUS/36_C10_RESIDUAL_COINED_VALUES.md` (length-realization), `CORPUS/43_C10K_KEYING_ABLATION.md` (keying locus, key distinctness) and sweep §12 (the empty cell).

## Resolve-or-log protocol

Every candidate → one row in `docs/INFRANODUS_RESEARCH_ARC_2026-10-05.md`: mechanism (one sentence, in the paper's words), what it would do for which wall, runs locally with the engine untouched (yes / plausible / no), route it informs, the falsifier to pre-register, and a verdict: ADOPT-TO-PREREG / READ-NEXT / DEAD-END (with the reason). Advisor review before any ADOPT verdict; gpt-5.5 cross-family at the end of the arc. Output also carries the graph table (name, diagnosis, modularity, URL) and a convergence map. Nothing moves to CORPUS, program_state next-actions carry a one-line pointer only.
