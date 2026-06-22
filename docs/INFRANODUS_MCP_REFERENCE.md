# InfraNodus MCP — Capability Reference & Deep Dive

_A complete reference for the InfraNodus MCP server wired into this repo: what it is, the graph-theory engine behind it, all 32 tools, cross-cutting mechanics, workflow patterns, repo integration, and limits. Grounded in the live tool schemas, the official `infranodus.com/docs`, Paranyushkin's papers, and live tool calls (2026-06-22)._

> **Repo fence (binding — read first).** InfraNodus outputs are **LEADS → the hypothesis register, NEVER `CORPUS/` evidence** (`SESSION_BOOTSTRAP.md §5`, [[research-first-and-verify-tool-availability]]). It is an ideation / discourse-structure aid: excellent for surfacing gaps, framing research questions, and mapping a topic — but any finding must be proven by a pre-registered falsifier in the main workflow before it counts. See `docs/WORKFLOWS_OVERVIEW.md §4.4`.

---

## 1. What it is

**InfraNodus** (by **Nodus Labs** / Dmitry Paranyushkin) is a **text-network-analysis + knowledge-graph engine**. It converts any text / URL / search-corpus into a graph of concepts, then applies **graph theory** to reveal the *structure* of a discourse: its main topics, its most influential concepts, and — its signature capability — the **structural gaps** between topics that represent blind spots, research questions, or content opportunities.

- **Academic grounding:** Paranyushkin, *"Identifying the Pathways for Meaning Circulation using Text Network Analysis"* (2011) and *"InfraNodus: Generating Insight Using Text Network Analysis"* (2019). Also draws on Firth ("know a word by the company it keeps"), social-network structural-holes theory, and Foucault/Deleuze (dispositif / rhizome).
- **MCP server:** v1.1.0, **32 tools** (confirmed complete via the `get_more_tools` meta-tool).
- **Account context (this repo):** graphs persist under the logged-in account `robertrhu`.

---

## 2. The engine (the theory needed to read outputs)

### 2.1 Text → graph
1. Remove stopwords / auxiliary words → 2. **lemmatize** (e.g. "laboratories" → "laboratory") → 3. each unique lemma becomes a **node** → 4. a **4-lemma sliding window** (adjustable) moved one step at a time creates **edges** between co-occurring lemmas. Edge weight encodes proximity + frequency: **adjacent = 3, one apart = 2, two apart = 1**, accumulated over repeats. Edges are stored directed (order preserved) but most metrics treat the graph as undirected.

### 2.2 Metrics
| Metric | Meaning | Used for |
|---|---|---|
| **Betweenness centrality (BC)** | "Discursive influence" — nodes on many shortest paths between clusters | **Conceptual gateways**; node size in the viz. *High BC ≠ high frequency.* |
| **Community detection (Louvain modularity)** | Partitions the graph into communities | **Topical clusters** (each colored); **Force-Atlas** layout separates them spatially |
| **Degree** | Local connectivity | Discourse-state diagnostics |

### 2.3 The two kinds of gaps (key distinction)
- **Structural gap** — *within one text*: two clusters both present but barely connected (low inter-cluster edge density). Connecting them = a new idea/question.
- **Content gap** — *across graphs* (SEO): topics present in one graph (e.g. what people **search** for = demand) but absent in another (e.g. existing **results** = supply). Framed around Google's "informational gain" concept.

### 2.4 Discourse-structure states (drives the `optimize_*` tools)
Classified by **modularity × concentration × degree distribution**:

| State | Modularity | Concentration | Meaning → recommended action |
|---|---|---|---|
| **Biased** | low | high (few hubs) | fixated / redundant → *develop under-represented topics* |
| **Focused** | high | high | well-defined topics → *bridge the content gaps* |
| **Diversified** | high | low | many clusters + hubs → *bridge the gaps* |
| **Dispersed** | low | low | scattered, no structure → *focus the common gap topics* |

A second axis — *narrative variability* (uniform / regular / fractal / complex) — is derived by detrended fluctuation analysis (DFA) over the betweenness sequence.

### 2.5 Conceptual bridges
The specific nodes/edges that would connect a gapped cluster pair (shortest-path / community-boundary / high-BC nodes). Writing about a suggested bridge literally adds edges and integrates the clusters. *Gateways* = high influence-per-occurrence entry points; *bridges* = the connectors that fill a gap.

---

## 3. Live proof (real output, 2026-06-22)

`analyze_text` on a paragraph about MEMIT / AlphaEdit returned:
- **modularity 0.54 (high)**, discourse state **`diversified`**, **5 clusters**
- top concept `knowledge` (**BC 0.58, degree 17**)
- **3 content gaps**, e.g. *"Database Editing → Catastrophic Forgetting"*, *"Language Model → Catastrophic Forgetting"*
- conceptual gateways: `editable, store, factual, method, space, database, correct`

`generate_research_questions` then turned those gaps into questions, e.g.:
> *"How can null-space-constrained sequential editing (AlphaEdit) make a model behave as a durable, queryable database — preserving correct reads while minimizing catastrophic forgetting and cross-entity corruption under quantized updates?"*

→ The core InfraNodus loop: **text → graph → gap → question.**

---

## 4. The 32 tools, by function

### A. Core analysis (text → graph + metrics)
| Tool | Purpose |
|---|---|
| `analyze_text` | The workhorse: graph + stats (modularity, BC, diversity state) + topics + gaps + gateways + relations. Input: text / URL / YouTube / saved graph. |
| `generate_knowledge_graph` | Full graph incl. nodes/edges + clusters + gaps (`includeGraph` defaults **true**). |
| `generate_topical_clusters` | Topics/clusters + optional AI summary per cluster (SEO-friendly). |
| `generate_content_gaps` | Just the structural gaps between clusters. |
| `generate_contextual_hint` | Lightweight topic overview to **augment RAG** prompts. |
| `analyze_existing_graph_by_name` | Run analysis on a saved graph. |

### B. Develop / ideate (gap → insight, LLM-backed)
| Tool | Purpose |
|---|---|
| `develop_text_tool` | One-shot combo: research questions + latent topics + content gaps (progress-tracked). Knobs: `gapDepth`, `useSeveralGaps`, `transcendDiscourse`. |
| `develop_latent_topics` | Under-developed topics + how to expand them. |
| `develop_conceptual_bridges` | Connect the text to a **broader discourse** (`question` vs `transcend` mode). |
| `generate_research_questions` | Gaps → research questions. |
| `generate_research_ideas` | Gaps → ideas / business ideas (`responseType`, `shouldTranscend`). |
| `generate_responses_from_graph` | Answer a prompt **grounded in the graph**. |
| `optimize_text_structure` | Diagnose bias/coherence → recommend develop-vs-focus (`response`/`idea`/`question`/`transcend`). |
| `optimize_reasoning` | ⭐ Same analysis applied to **the model's own reasoning / the chat** — steers toward balanced diversity + coherence. A self-reflection tool. |

### C. Graph creation / persistence / knowledge base
| Tool | Purpose |
|---|---|
| `create_knowledge_graph` | Build + **save** a named graph from text/URL. |
| `generate_ontology_graph` | AI-generated **entity-relation ontology** (`saveGraph`, `modelToUse`). |
| `list_graphs` | List saved graphs; filter by type/date/lang/favorite. |
| `search` | Find concepts/terms across your saved graphs. |
| `fetch` | Retrieve a specific search result by id (`username:graph:query`). |
| `retrieve_from_knowledge_base` | **GraphRAG** retrieval from a saved graph (prompt + graphName). |

### D. Comparison / multi-text
| Tool | Purpose |
|---|---|
| `difference_between_texts` | What's in the *other* texts but **missing from the first**. |
| `overlap_between_texts` | Shared concepts across texts. |
| `merged_graph_from_texts` | Combined graph + its topics/gaps. |

### E. Persistent memory (entity-relation, `[[wikilink]]`-based)
| Tool | Purpose |
|---|---|
| `memory_add_relations` | Add relations to a named memory graph (the MCP "memory" backend). |
| `memory_get_relations` | Retrieve relations for an entity. |

### F. Search-engine / SEO / external-corpus analysis
| Tool | Purpose |
|---|---|
| `analyze_google_search_results` | Graph from Google SERPs for queries (the **supply**). |
| `analyze_related_search_queries` | Graph from related/AdWords suggestions (the **demand**). |
| `search_queries_vs_search_results` | **Demand − supply**: what people search but don't find. |
| `generate_seo_report` | Compare your content's graph vs SERPs + queries → SEO gaps (**slow, ~90 s**). |
| `analyze_youtube_results` | YouTube search / comments / channel / playlist / **subtitles** → graph. |
| `analyze_llm_results` | ⭐ Probe **how an LLM frames a topic** (bias detection); compare models. |

### G. Meta
| Tool | Purpose |
|---|---|
| `get_more_tools` | Discover additional tools. *(Confirmed 2026-06-22: 32 is the full set.)* |

---

## 5. Cross-cutting mechanics (the gotchas)

- **Every tool requires a `context` param** — a **15–25-word, third-person, no-secrets** description of *why* you're calling it (analytics/intent tracking). Mis-formatting it fails the call.
- **Three input modes** on analysis tools: `text` · `url` (auto-fetches a webpage **or YouTube transcript**) · `graphName` (a saved graph).
- **`modifyAnalyzedText`**: `none` (word co-occurrence — default for topic/gap work) · `detectEntities` (mix entities + words) · `extractEntitiesOnly` (**use for ontologies / knowledge graphs / entity extraction**).
- **`modelToUse`** on LLM-backed tools selects the engine (claude-opus-4.6, claude-sonnet-4.6, gpt-5.4(-mini), gemini-2.5-pro/flash/lite, grok-4.1, gpt-4o(-mini)).
- **`requestMode` / `responseType` / `transcend`**: `question` = stay inside the text; `transcend` = go beyond to the broader discourse. `responseType` adds `response` / `idea`.
- **`gapDepth` + `useSeveralGaps`**: control how deep / how many gaps drive question/idea generation.
- **Output-size knobs** (default **false** to protect context budget): `includeGraph`, `includeStatements`, `includeGraphSummary`, `addNodesAndEdges`, `showExtendedGraphInfo`, `compactStatements`. Pull the heavy ones only when you'll use them.
- **Graph types** (persisted): STANDARD, MINDMAP, WORDCLOUD, SCIENCE, GOOGLE, SEO, ONTOLOGY, MEMORY, WIKILINKS, PDF, CSV, RSS, EVERNOTE, TWITTER, KWRDS…

---

## 6. Documented workflow patterns

1. **Quick overview** → `generate_knowledge_graph` / `generate_topical_clusters`.
2. **Deep text development** → `develop_text_tool` (optimize + latent topics + bridges in one).
3. **Research ideation** → `generate_content_gaps` → `generate_research_questions` / `_ideas` (`useSeveralGaps`, `gapDepth`).
4. **Self-steering** → `optimize_reasoning` on the model's own chain-of-thought.
5. **Outside-the-box** → `develop_conceptual_bridges` / `transcend` modes.
6. **RAG / GraphRAG** → `generate_contextual_hint` or `retrieve_from_knowledge_base`.
7. **Compare texts** → `overlap_between_texts` / `difference_between_texts` / `merged_graph_from_texts`.
8. **SEO** → `generate_seo_report`, or the chain `analyze_google_search_results` → `analyze_related_search_queries` → `search_queries_vs_search_results`.
9. **Memory** → `memory_add_relations` / `memory_get_relations`.

---

## 7. Integration in this repo

- **Registration:** a **global-scope** stdio MCP server in `~/.claude.json` (`mcpServers.infranodus`), running `/workspace/node-v20/bin/npx -y infranodus-mcp-server` with `INFRANODUS_API_KEY` in `env`. Tools surface as deferred `mcp__infranodus__*` names → load schemas via ToolSearch before calling.
- **Durability:** `~/.claude.json` is on the ephemeral overlay, so a pod restart wipes the registration. Node persists at `/workspace/node-v20`. Rebuilt by **`bash /workspace/tools/restore_pod_tools.sh`** (merges the config + key back); MCP tools register on the next **session reload**. See `SESSION_BOOTSTRAP.md §5` + `docs/WORKFLOWS_OVERVIEW.md §4.4–4.5`.
- **Fence:** see the banner at the top — leads, not evidence.

---

## 8. Limits / caveats

- The **support help-center blocks automated fetches** (HTTP 403, Zendesk). Grounding came from `infranodus.com/docs`, the 2019 paper, and live tool calls.
- **LLM-backed tools** (`develop_*`, `generate_research_*`, `optimize_*`, `analyze_llm_results`, `generate_ontology_graph`) add latency + a model choice; `generate_seo_report` is the slowest (~90 s).
- The **4-gram window / 3-2-1 weights are defaults**, adjustable in the app; directed edges are stored but most metrics treat the graph as undirected.
- Responses can be **large** — prefer summary/compact flags; the live compact graph output above was already sizeable.
- The **`context` param is mandatory** on nearly every tool (easy to forget when scripting).

---

## 9. Pointers (official sources)

- `https://infranodus.com/docs/text-network-analysis` — methodology
- `https://infranodus.com/docs/content-gap-analysis` — gap analysis
- `https://infranodus.com/docs/knowledge-graphs-for-llms` — GraphRAG
- `https://infranodus.com/mcp/tools` — MCP tool catalog
- `https://noduslabs.com/research/pathways-meaning-circulation-text-network-analysis/` — 2011 paper
- `https://support.noduslabs.com/hc/en-us` — help center (bot-blocked; open in a browser)

---

_Document type: process/reference (no experiment D-ID; not subject to `closeout_check`). Captured 2026-06-22 from live MCP schemas + grounded research. Update if the server version or tool set changes (re-run `get_more_tools` to re-confirm completeness)._
