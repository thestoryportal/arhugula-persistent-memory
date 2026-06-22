# InfraNodus Official Documentation — Library Review & Durable Reference

_Full-depth review of the official InfraNodus documentation at **infranodus.com/docs** (~40 pages across 6 categories + the API + the methodology page), read 2026-06-22 via 7 parallel readers. Third in the InfraNodus trilogy: `INFRANODUS_MCP_REFERENCE.md` (the MCP **tools**) · `INFRANODUS_SKILLS_REFERENCE.md` (the Claude **skills**) · **this** (the official **product documentation, methodology & API**)._

> **Authoritative-source note.** Where this doc states method mechanics or API details, they are quoted/derived from the official docs and **supersede** any looser phrasing in the other two reference docs. The text-network method here is the ground truth. The repo fence still applies: InfraNodus is an analysis/ideation aid → leads, not `CORPUS/` evidence (`SESSION_BOOTSTRAP.md §5`).

---

## 1. Documentation map (the full library)

The docs are a tutorial hub at `/docs` organized into 6 categories. Index with one-line each:

**A. Knowledge Graphs for LLMs** — the AI-engineering core
- `knowledge-graphs-for-llms` · GraphRAG + reasoning ontologies + MCP, the 3-mode overview
- `graph-rag-knowledge-graph` · GraphRAG vs vector RAG; 5 use cases; competitor comparison
- `knowledge-graphs-llm-reasoning` · reasoning ontologies (concept types/constraints/paths)
- `mcp-vs-rag-vs-ai-agents` · how MCP, RAG, agents compose; gap-driven tool-chaining
- `n8n-workflow-templates-automations` · no-code "Panel of Experts" GraphRAG templates

**B. AI-Enhanced Ideation & PKM**
- `ai-ideation-tutorials` (hub) · `personal-knowledge-management` · `creative-thinking-writers-tool` · `generate-insight` · `overview-summarize-books-articles` · `dream-analysis-interpretation` · `diary-journaling-app`

**C. Search Engine / LLM Optimization (SEO/GEO/LLMO)**
- `seo-llm-optimization` (hub) · `keyword-research` · `search-engine-optimization` · `keyword-clustering-seo` · `seo-clusters`

**D. Market Research**
- `market-research-tutorials` (hub) · `customer-product-reviews-sentiment` · `competitive-intelligence` · `innovation-strategy` · `content-gap-analysis` (flagship)

**E. Data Analysis**
- `data-analysis-tutorials` (hub) · `text-network-analysis` (the method) · `network-visualization-text-mining` · `ai-text-analysis` · `qualitative-thematic-analysis` · `thematic-analysis-steps-framework` · `visual-search`

**F. Text Visualization**
- `text-visualization-tutorials` (hub) · `mind-map-tool` · `word-cloud-generator` · `network-analysis` · `text-art-sculpting`

**+ Reviews & Recommendations** (marketing/SEO comparison pages, not technical): `network-visualization-software`, `gephi-alternative-network-analysis`, `voyant-alternative-tools`, `survey-analysis-tools`, `text-analyzer-tools`, etc.
**+ API:** `infranodus.com/api/docs` (canonical), `/api`, `/docs/api`. **+ Methodology:** `about/how-it-works`.

---

## 2. The authoritative method (text → graph → insight) — ground truth

Quoted/derived from `text-network-analysis` + `about/how-it-works` (the most precise pages):

1. **Preprocess:** remove auxiliary words via "**stopwords and / or tf-idf models**"; reduce words to **lemmas** ("laboratories" → "laboratory").
2. **Nodes:** each unique lemma is a node.
3. **Edges:** built from a "**4-gram (a sliding window containing 4 words)**" advanced one word at a time, so windows overlap.
4. **Edge weights by proximity:** adjacent words = **3**; one word between = **2**; two between = **1** ("the closer they are, the higher the weight"), accumulated over repeats.
5. **Layout:** "**Force-Atlas layout algorithm**" — hubs pushed apart, less-connected nodes pulled toward their hubs.
6. **Node ranking:** "**betweenness centrality (BC)**" = "discoursive influence"; higher BC → bigger node. (BC ≠ frequency; high-BC nodes are the **conceptual gateways** bridging clusters.)
7. **Topical clusters:** "**modularity algorithm (Blondel et al, based on Louvain)**" — densely co-occurring lemmas get a shared color.
8. **Structural gap:** "topical clusters on the graph that are **distinct from one another and have a high distance**" — topics that *could* connect but don't. Highlighted as discourse blind spots → seed for LLM-generated research questions / bridging ideas.
9. **"Reveal underlying ideas":** hide top-BC nodes to expose latent/peripheral concepts.

**Discourse diversity** is measured from this structure (modularity + concentration + entropy) → the **biased / focused / diversified / dispersed** states (the spine of the skills library; see `INFRANODUS_SKILLS_REFERENCE.md §2`).

**Provenance / stack (durable):** method from **Paranyushkin (2019), "InfraNodus: Generating Insight Using Network Analysis"** (ACM), built on the **Textexture** algorithm. Stack: **NestJS / Prisma / PostgreSQL / Sigma.js** (+ Cytoscape, Graphology). By **Nodus Labs / InfraNodus SAS (France), since 2011**; core tools **AGPL** open-source. Thematic-analysis pages map the method onto **Braun & Clarke's 6 steps** (inductive + deductive, reflexive TA).

> ⚠ **Caveat (observed):** the `visual-search` page describes a **within-sentence** co-occurrence window rather than the 4-gram default — the window is configurable and some apps differ. Treat 4-gram/3-2-1 as the documented *default*, not an invariant.

---

## 3. Knowledge graphs for LLMs (most relevant to this repo)

**Three-mode stack:** (1) **GraphRAG** retrieval, (2) **reasoning ontologies**, (3) **MCP server** delivery.

- **GraphRAG vs vector RAG:** vector RAG fails on (a) **general queries** ("What is it about?" → term-matched chunks, not intent) and (b) **relational/multi-hop** queries. GraphRAG retrieves "not just similar chunks but the surrounding graph" — topical clusters, multi-hop relational context, structural gaps — and can **rewrite a vague prompt** into a concept-targeted one before retrieval. Five use cases: prompt augmentation, relational context, topical overview, **knowledge-base completeness assessment**, content-gap detection.
- **Reasoning ontologies** ("cognitive knowledge graphs") model concept *types/roles* ("principles, constraints, observations, actions"), direction of influence, and reasoning paths — "designed for reasoning, not storage." Notable claim: "**Each statement can contain multiple relations** (not only one as is the case with Neo4J graphs)." Curbs hallucination by giving "conceptual constraints that keep AI outputs anchored"; enables explainable trace-back via edges and shared reasoning structure for multi-agent systems.
- **MCP** is framed as "an open standard originally developed by Anthropic" (a connectivity layer making GraphRAG callable by any LLM client); docs cite **27+ MCP tools** (our enumeration: 32 — see `INFRANODUS_MCP_REFERENCE.md`). **Gap-driven tool-chaining** example: `analyze_google_search_results → generate_content_gaps → generate_research_questions → memory_add_relations`, where gap detection "directly informs the agent's next action."
- **n8n "Panel of Experts":** multiple HTTP nodes each bound to a saved graph/ontology, augmenting an agent node; uses the `graphAndAdvice` endpoint. Templates in the `n8n-infranodus-workflow-templates` repo.
- **Privacy:** `doNotSave` param; choice of OpenAI/Claude/Gemini providers ("none use API data for training").

> **Relevance to LLM-as-Database:** InfraNodus's "knowledge graph for LLM reasoning/retrieval" is an *external, text-derived* graph (a retrieval/ideation layer over text). It is **not** the same claim as the program's *in-weight* FFN-as-graph-database thesis — useful as an analogy and an ideation tool, but a different mechanism. Keep the distinction crisp; do not conflate InfraNodus GraphRAG with the spec's parametric store.

---

## 4. API reference (from `infranodus.com/api/docs`)

**Auth:** get a token at `infranodus.com/api-access`; header `Authorization: Bearer <token>` + `Content-Type: application/json`. A few free requests allowed at their discretion; **Advanced/Pro/Premium** tiers get higher limits. EU (AWS Ireland) processing; with AI features only top-cluster concepts (not full content) go to external LLMs.

**Endpoints** (all **POST** `https://infranodus.com/api/v1/...`):

| Endpoint | Purpose |
|---|---|
| `graphAndStatements` | Core: text → graph + statements + summary |
| `graphAndAdvice` | Graph + AI question/idea/insight |
| `graphsAndAiAdvice` | AI advice across compared graphs |
| `dotGraph` / `dotGraphFromText` | Compact **DOT** graph (+ summary) for LLM forwarding |
| `graphAiAdvice` | AI advice from a supplied Graphology graph |
| `listGraphs` | List saved graphs |
| `search` | Search saved statements + build a graph |
| `compareGraphs` | `mode: merge \| overlap \| difference` |
| `import/googleSearchResultsGraph` (+ `…AiAdvice`) | Graph/advice from Google SERPs |
| `import/googleSearchIntentGraph` (+ `…AiAdvice`) | Graph/advice from related queries (intent) |
| `import/googleSearchVsIntentGraph` (+ `…AiAdvice`) | Supply-vs-demand comparison |

**Key params:** `text`/`statements[]`/`url`; `doNotSave` (default **true**), `addStats` (true), `includeStatements` (true), `includeGraph` (true), `includeGraphSummary` (false), `extendedGraphSummary` (true), `compactGraph`, `compactStatements`, `gapDepth` (0), `stopwords[]`, `modifyAnalyzedText` (`none`|`detectEntities`|`extractEntitiesOnly`), `aiTopics`. For advice: `optimize` (`develop`|`reinforce`|`gap`|`imagine`), `requestMode` (`question`|`idea`|`fact`|`continue`|`challenge`|`response`|`summary`|…), `modelToUse`, `pinnedNodes[]`, `transcend`. Imports: `searchQuery`, `importCountry`, `importLanguage`.

**Response envelope:** `entriesAndGraphOfContext` → `graph` (Graphology nodes/edges), `statements`, `graphSummary` (text), `extendedGraphSummary` (`mainTopics`, `mainConcepts`, `contentGaps`, `conceptualGateways`, `topRelations`, `topBigrams`, `diversityStatistics`), `graphUrl`/`graphName`. Graph attrs include `top_nodes`, `top_clusters`, `gaps`, `dotGraph`, `diversity_stats`.

**Exports:** graph data **JSON / CSV / GEXF**; tagged statements **CSV / MD (Obsidian)**; original text **TXT / JSON**; analytics **TXT / Keywords-CSV / N-Grams-CSV**; images **PNG / SVG**; API returns Graphology JSON + **DOT**.

**Integrator tips:** `doNotSave=true` ⇒ not stored/logged; `compactGraph=true` + `includeStatements=false` ⇒ minimal LLM payload; `extractEntitiesOnly` ⇒ clean ontology output. Available via RapidAPI, n8n, Make.com, MCP. *(Note: `/api` and `/docs/api` are JS-thin; `/api/docs` is canonical. The support-center API mirror returns HTTP 403 to bots.)*

---

## 5. SEO / GEO / LLMO (category C)

Reframes optimization as a **graph problem**: model **demand** (Google autocomplete top-200 + Ads Keyword Planner + People-Also-Ask) and **supply** (top SERP pages, "first 4 pages") each as keyword graphs, then locate the **structural gap** between them via `search_queries_vs_search_results` / the **Difference view**. Network metrics drive content architecture: **betweenness centrality = the pillar topic** ("more specific and more defensible" than the highest-volume keyword), **community detection = the spokes**, **edge weight = internal-link prominence**. Content types by graph position: hub→pillar 3000+ words, centroid→spoke 1500–2000, bridge→comparison ~1200, gap→gap-bridge ~1500; 3–5 high-BC spokes, 5–8 contextual links/page. Core thesis: the **same entity-graph coherence wins both Google SERP and AI answer engines (GEO/AEO/LLMO)** because LLMs "retrieve passages, weigh entity relationships, and synthesize answers" and judge "how that page sits inside the entity graph." Differentiated from Ahrefs/Semrush "flat tables" by ranking via network influence; clusters are "living structures" needing quarterly re-analysis (`difference_between_texts`).

## 6. Market research (category D)

One pipeline — "import unstructured text → build a graph → run community detection → run gap analysis → query with AI" — serves four jobs:
- **Sentiment** (`customer-product-reviews-sentiment`): per-concept sentiment (not aggregate), **BERT** (ML) + **AFINN** (dictionary) models, Amazon-review import, **Filter Function** to contrast high- vs low-rating review graphs.
- **Competitive intelligence:** overlay a market "informational supply" graph (Google results) vs a competitor's site-text graph; under-bridged territory = whitespace; AI bridges the gap.
- **Innovation strategy:** cluster surveys / scientific papers (Arxiv/PLOS/Scholar import); detect disconnected clusters; AI bridges them (e.g. "Energy Sustainability" + "Manufacturing Automation" → energy-efficient automation).
- **Content gap (flagship):** build a **supply** graph (SERP) + a **demand** graph (related queries), use the **Difference view** to extract "keyword combinations… in the search query graph but not in the search results graph," then AI generates an article outline that "touches upon all the topics identified" → closes the gap for "informational gain."

## 7. Ideation & PKM (category B)

Philosophy: **structural gaps are the locus of creative potential** — InfraNodus is *diagnostic* (surfaces what's missing) not generative-from-nothing. Loop: **Capture → Connect → Detect (clusters + gaps) → Develop (AI bridges gaps)**. PKM angle: graph layer beats folders/tags ("no folder tells you you keep writing about X but never how X relates to Y"); pairs with Zettelkasten/PARA/Second-Brain + Obsidian/Roam/Logseq + Cursor + n8n; an "**LLM Wiki**" layer separates project graphs from the main base to reduce AI contamination (cf. the `llm-wiki` skill). "**Ecological thinking**" (growth/saturation/restructuring) + **cognitive variability** (explore↔focus × zoom axes) + a **diversity score** steer the user between focus and diversification. Niche pages (dream, diary) are applied templates of the same gap-bridging engine on subconscious/emotional material (BERT sentiment, "Reveal Underlying Ideas").

## 8. Text visualization + reviews (category E/F, brief)

Four output modes of one engine: **mind map** (`#hashtags`/`[[wikilinks]]`/`@mentions` → graph), **word cloud** (relationship-aware, clustered), **network analysis** (Force-Atlas + Blondel modularity + the proprietary "**Diversivity**" metric = influence-per-connection; Gephi/Pajek export), **text art** ("Abstract Visualization," unlabeled edge-only art, voice-to-text + MIDI/OP-1). The **Reviews & Recommendations** pages are **marketing/SEO** comparison content (not technical docs) positioning InfraNodus #1 vs Gephi, Voyant, NVivo/ATLAS.ti/MAXQDA, NodeXL, etc. — differentiators: no-code, native text-to-network, automatic gap detection, GPT cluster-naming, built-in GraphRAG, ~€19/mo.

---

## 9. How this refines our other InfraNodus docs

- **Confirms & sharpens the methodology** in `INFRANODUS_MCP_REFERENCE.md §2` with verbatim authoritative mechanics (4-gram, 3/2/1 weights, Force-Atlas, Blondel/Louvain modularity, BC) + the `visual-search` window caveat.
- **Adds the API** (entirely new) — the REST layer behind the MCP; useful if we ever want direct/no-MCP access or n8n automation.
- **Grounds the skills' framework** (`INFRANODUS_SKILLS_REFERENCE.md §2`): the biased/focused/diversified/dispersed states + ecological thinking + cognitive variability are *official product concepts*, not skill-invented.
- **Provenance** is now firm: Paranyushkin 2019 (ACM) / Textexture / Nodus Labs 2011 / AGPL / NestJS-PostgreSQL-Sigma.js.
- **Caveat for the program:** InfraNodus "knowledge-graph-for-LLM" = an *external text-derived retrieval/ideation graph*, a different mechanism from the spec's *in-weight FFN-as-database* — keep separate.

---

## 10. Pointers

- Docs hub: `https://infranodus.com/docs` · Methodology: `https://infranodus.com/about/how-it-works` · `https://infranodus.com/about/cognitive-variability`
- API: `https://infranodus.com/api/docs` · key: `https://infranodus.com/api-access`
- Method paper: Paranyushkin (2019), "InfraNodus: Generating Insight Using Network Analysis" (ACM)
- Companion docs: `docs/INFRANODUS_MCP_REFERENCE.md`, `docs/INFRANODUS_SKILLS_REFERENCE.md`, `docs/WORKFLOWS_OVERVIEW.md`
- Help center (bot-blocked; open in browser): `https://support.noduslabs.com/hc/en-us`

---

_Document type: process/reference (no experiment D-ID; not subject to `closeout_check`). Captured 2026-06-22 from a full-depth read of infranodus.com/docs. The docs site evolves — re-fetch the methodology + API pages if mechanics are load-bearing for a decision._
