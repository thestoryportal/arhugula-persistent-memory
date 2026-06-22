# External Claude-Skill Repos — Granular Usage-Scope Audit

_Audit of external Claude-skill repos for the **exact granular usage scope** of each skill — **10 distinct repos** (the original 8 + `obra/superpowers` §8a + `anthropics/knowledge-work-plugins` data+bio-research §8b, all added 2026-06-22). Captured 2026-06-22 by cloning/fetching each and extracting every skill's verbatim `description:` (the trigger = the granular scope), dependencies, and boundaries. For the large collections (K-Dense 147, Jeffallan 66, awesome-list ~60) the high-fit skills are quoted verbatim and the rest are grouped — the source repos hold the full per-skill text._
> (Note: `rizinorg/cutter` was also requested but is **not a skills repo** — a reverse-engineering GUI, GPL-3, GUI-only/unusable headless, off-domain — so it is intentionally excluded from this audit.)

> **Framing for this repo.** Forward-tooling evaluation (operator's scaffolding phase). "Fit" = usefulness for the **LLM-as-Database** falsification-first program (knowledge editing, evals on Qwen, spec validation, literature review, rigorous experiment design/stats). The InfraNodus fence generalizes: any adopted skill's output is a **lead/aid, not `CORPUS/` evidence**.

---

## 0. Repo summary

| Repo | What it is | # skills | License | Activity | Top fit |
|---|---|---|---|---|---|
| **Isoform/yansu-skill** | CLI bridge to the *Yansu* desktop "proactive AI" (activity capture/recall) | 1 | MIT | 162★ | 🔴 Low (personal-productivity) |
| **alirezarezvani/claude-skills** `research/` `research-ops/` `compliance-os/` | Research + enterprise-R&D-ops + regulatory-audit skill families | 22 | MIT | active | 🟡 `litreview`, `research` router |
| **K-Dense-AI/scientific-agent-skills** | 147 "scientific agent" skills (bio/chem/clinical/ML/stats/lit) | 147 | MIT (mixed per-skill) | v2.50, daily CI | 🟢 **arbor**, stats/DOE, lit-review |
| **firecrawl/firecrawl** | Web-data API (scrape/crawl/map/search/extract) + official MCP & skills | n/a (API) | AGPL-3 core | 137k★ | 🟢 clean bulk source acquisition |
| **BehiSecc/awesome-claude-skills** (4 sections) | Curated index of external skills | ~60 listed | none | 9.6k★ | 🟡 `paper-search`, `Junshi` |
| **Jeffallan/claude-skills** (fullstack-dev-skills) | 66 software-eng persona skills + workflow cmds | 66 | MIT | 10k★ | 🟡 `the-fool`, `prompt-engineer` |
| **thananon/9arm-skills** | Personal eng-process discipline skills | 6 | **none** | 2.9k★ | 🟢 `debug-mantra`, `scrutinize` |
| **virgiliojr94/book-to-skill** | Meta-skill: convert books/docs/paper-clusters → an Agent Skill | 1 (meta) | MIT | 6.5k★ | 🟢 fold spec+corpus into a skill |
| **obra/superpowers** (§8a) | Agentic skills + SW-dev methodology framework (TDD/verify/debug/review pipeline) | 14 | MIT | 236k★ | 🟢🟢 **highest discipline-fit** (verify/debug/TDD/review) |
| **anthropics/knowledge-work-plugins** `data` + `bio-research` (§8b) | Official Anthropic role plugins (MCP-connector + markdown) | 10 + 6 | Apache-2.0 | 21.7k★ | 🟢 `scientific-problem-selection`; 🟡 data stats/viz |

---

## 1. Isoform/yansu-skill — `yansu` (1 skill)
**Scope (verbatim):** *"Collaborate with Yansu — the proactive AI that observes how the user actually works and crystallizes it into knowledge. Use this skill whenever the user asks for a digest of their recent activity, wants to find workflow inefficiencies or recurring blockers, needs to retrieve a past insight, configuration, or memory, or wants to hand off a job to Yansu… Triggers on 'what did I do today', 'summarize my week', 'catch me up', 'yansu digest', 'where am I inefficient', 'have I solved this before', 'find that note about X'…"*
**Deps/boundaries:** hard-requires the **Yansu desktop app** running locally; thin Bash bridge to the bundled `yansu` CLI; **read-only by design** (never writes memory/machine; never sends memory to external tools). 🔴 **Low fit** — personal-continuity layer, no research/editing/eval value.

---

## 2. alirezarezvani/claude-skills (MIT; 22 skills across 3 dirs)
Build pattern: `Path B` direct-conversion from `megaprompts/*.md`; no `allowed-tools` declared (ambient WebSearch/WebFetch + bundled Python).

### `research/` (8) — external knowledge gathering, most output an editable `.docx`
- **research** (router) — *"Default entry point for any research request — a hybrid router that classifies the question deterministically and either delegates to a specialist (pulse/grants/litreview/syllabus/patent/dossier) or runs its own plan-decompose-multi-source-search-synthesize-cite fallback… Always surfaces the routing decision."* 🟢
- **litreview** — *"Academic literature orientation skill that searches papers via **Consensus**, builds a strategic search plan using **PICO** (default) or SPIDER/Decomposition… synthesizes into a formatted Word (.docx) research guide… Output is a 'launching pad'… Do NOT use for single one-off paper searches."* 🟢 (lit-review for editing methods)
- **grants** — *"NIH grant research skill… Runs a 5-facet Consensus positioning analysis… maps to NIH institutes/study sections via **RePORTER**… **NIH-only scope.**"* 🔴
- **patent** — *"Patent prior-art and landscape intelligence… five sub-use-cases (novelty / freedom-to-operate / competitive landscape / acquisition diligence / litigation prior-art)… searches Google Patents, Espacenet, USPTO, optionally Lens.org… search signal, not legal advice."* 🟡 (only if IP-landscape on editing ever matters)
- **dossier** — *"Decision-grade entity research… forcing intake makes the user state their hypothesis upfront… tests it rather than confirms it… WebSearch + WebFetch + free APIs (SEC EDGAR, GitHub, ProPublica)."* 🔴
- **pulse** — *"Multi-source recency research across Reddit, Hacker News, the open web, and optionally X/Twitter within a configurable window (default 30 days)…"* 🟡 (practitioner discourse on tooling)
- **syllabus** — *"Generates a curated supplementary reading list from any course syllabus using Consensus…"* 🔴
- **notebooklm** — *"Browser automation skill for controlling Google's NotebookLM… reading/querying notebooks, adding sources, generating Studio outputs… Requires browser automation environment."* 🟡 (overlaps your headless NotebookLM CLI)

### `research-ops/` (5) — enterprise R&D ops (estimate-and-named-owner discipline)
Orchestrator + **clinical-research** (study design, endpoint selection, **sample-size/power for two-arm designs**, GO/NO-GO phase-gate), **market-research** (TAM/SAM/SOM, survey sizing), **product-research** (method selection, saturation/sample size), **research-finance** (R&D budget/burn/capex-vs-opex). 🟡 *only* `clinical-research`'s power/sample-size math is a loose analog to eval statistics; tuned for clinical trials, low transfer.

### `compliance-os/` (9) — regulatory audit-prep
Meta-orchestrator + 8 per-framework "6-question forcing interrogations" (ISO 27001/13485/42001, GDPR, SOC 2, FDA QSR, EU AI Act, AIMS). 🔴 **Off-domain** (governance, not experiments) — adjacency only if a *deployed product* ever needs AI-Act/AIMS compliance.

---

## 3. K-Dense-AI/scientific-agent-skills — 147 skills (the big one) 🟢
MIT (per-skill licenses vary; 4 Anthropic doc skills `docx/pptx/xlsx/pdf` are Proprietary, vendored). v2.50, daily CI. Org goal: "AI co-scientist on your desktop." Pattern: most `allowed-tools: Read Write Edit Bash`; many report skills want optional `OPENROUTER_API_KEY`.

### ⭐ Highest-fit (verbatim scopes)
- **arbor** — *"Autonomously improve a real artifact (code, training recipe, agent harness, data pipeline, prompt) against an objective and an evaluator, using **Hypothesis Tree Refinement (HTR)**… whenever someone wants to iteratively optimize something over many experiments **without overfitting** — 'get my model's eval score up', 'beat the baseline on this benchmark', 'run a search over approaches and keep the best'… Runs Claude as coordinator with subagent executors in **isolated git worktrees**."* `allowed-tools: Read Write Edit Bash Agent`. **Mechanism:** persistent hypothesis tree; one-hypothesis-per executor; admits changes only via a **held-out test merge gate the search never optimizes against**. ⭐⭐⭐ *The single best structural fit for the program's falsification + dev/test-gap discipline.*
- **experimental-design** — *"Design experiments and studies BEFORE data is collected — choosing a design, randomizing, blocking… factorial/fractional-factorial (DOE), screening factors, response-surface, crossover/repeated-measures/split-plot, cluster randomization… replication vs pseudoreplication, sequential/adaptive designs."* Hands off to → statistical-power / statistical-analysis. ⭐⭐⭐
- **statistical-power** — *"Sample-size and statistical power calculations… a priori power analysis, minimum detectable effect (MDE), power curves… closed-form (t/ANOVA/proportions/correlation/chi-square/regression) + simulation-based Monte-Carlo power for mixed models, cluster-randomized, survival, interactions."* ⭐⭐⭐ (pre-registration / MDE)
- **scientific-critical-thinking** — *"Evaluate scientific claims and evidence quality… experimental design validity, identifying biases and confounders, applying evidence grading frameworks (**GRADE, Cochrane Risk of Bias**)."* ⭐⭐⭐ (maps to your bias-ablation / pass-label-≠-promotable lessons)
- **hypothesis-generation** — structured testable-hypothesis formulation (scientific-method). **hypogenic** — automated LLM-driven hypothesis gen+test on tabular data. **statistical-analysis** — guided test selection + assumption checks + APA reporting. ⭐⭐
- **ML/runtime substrate:** **statsmodels** (OLS/GLM/mixed/ARIMA), **pymc** (Bayesian, MCMC/NUTS, LOO/WAIC — useful for distributional eval), **scikit-learn**, **shap**, **transformers** (HF Hub load/inference/Trainer fine-tune), **pytorch-lightning** (multi-GPU/FSDP/DeepSpeed + W&B/MLflow), **modal** (serverless GPUs), **get-available-resources** (CPU/GPU/RAM/disk probe → strategy), **optimize-for-gpu** (CuPy/Numba/RAPIDS). ⭐⭐ (your GPU-edit / CPU-deploy substrate)

### Literature/paper search (relevant)
**literature-review** (PubMed/arXiv/bioRxiv/Semantic Scholar → md/PDF, verified citations), **paper-lookup** (10 DBs incl. arXiv/OpenAlex/Crossref/Semantic Scholar/CORE/Unpaywall, no key), **citation-management** (→validated BibTeX), **exa-search** / **parallel-web** / **research-lookup** (⚠ send query text to api.parallel.ai/openrouter), **pyzotero**, **bgpt-paper-search**, **hugging-science** (HF scientific catalog).

### Grouped remainder (off-domain for this program)
- **Writing/publishing:** peer-review (CONSORT/STROBE), scientific-writing (IMRAD/PRISMA), venue-templates (NeurIPS/ICML/CVPR LaTeX), scientific-visualization, slides/posters/schematics/infographics.
- **Data/viz/compute:** exploratory-data-analysis, matplotlib/seaborn, polars/dask/vaex/zarr (big data), networkx, umap-learn, torch-geometric (GNN), sympy, time-series (aeon/timesfm), pymoo, simpy, RL (stable-baselines3/pufferlib).
- **Bio/genomics (~30):** biopython, scanpy, anndata, scvi-tools, pysam, pydeseq2, esm, phylogenetics… **Chem/materials/physics (~25):** rdkit, deepchem, diffdock, pymatgen, astropy, qiskit, pennylane… **Clinical/imaging (~12):** pydicom, pyhealth, pathml… **DB/integrations (~25):** database-lookup (78 DBs), depmap, benchling/latchbio/dnanexus, nextflow…
- **Caution:** "consciousness-council / what-if-oracle / dhdna-profiler" (3rd-party, low rigor — ignore). Several integrations exfiltrate query text to 3rd-party APIs.

---

## 4. firecrawl/firecrawl — web-data API 🟢
AGPL-3 (SDKs/UI MIT), ~137k★, very active. *"The API to search, scrape, and interact with the web at scale"* → clean Markdown/HTML/JSON/structured extracts; renders JS ("96% of the web").
**Operations (granular):** `/scrape` (1 URL → clean content), `/crawl` (follow links across a site, async, depth/path limits), `/map` (list all URLs on a domain, optionally ranked), `/search` (web search returning **full page content**, not snippets), `/agent`+extract (schema-structured JSON via `spark-1-mini/pro`; browser interact — click/fill/login/paginate).
**Consumed via:** hosted REST (`FIRECRAWL_API_KEY`), self-host Docker, SDKs (Py/Node/Go/Rust), and **official Claude integration**: `firecrawl-mcp` server + two skill repos — **firecrawl/cli** (10 SKILL.md skills: scrape/search/crawl/map/agent/monitor/interact/parse/download/orchestrator; *"Use this instead of WebFetch"*) and **firecrawl/skills** (plugin marketplace incl. **firecrawl-research-index**: *"Find the papers that answer a research query… semantic + structural expansion, in-body verification. Always use this skill for any literature-finding task."*).
**Fit:** 🟢 reliable bulk acquisition of clean source text (a WebFetch upgrade for JS-rendered spec/model-card/docs pages) + literature pull. Complements Perplexity (synthesized answers), NotebookLM (fixed corpus Q&A), InfraNodus (gap analysis). Caveat: API key / paid hosted or Docker self-host; AGPL only matters if you embed/redistribute the server.

---

## 5. BehiSecc/awesome-claude-skills — curated index (no license; 4 requested sections)
Entries = `name · verbatim list description · source link`.

**📊 Data & Analysis** (high-signal only; rest are crypto/marketing): **csv-data-summarizer** *"Automatically analyzes CSVs: columns, distributions, missing data, correlations"* (coffeefuelbump). **postgres / mysql / mssql** *"safe read-only SQL queries"* (sanjay3290/ai-skills). **notebooklm** (sanjay3290), **kaggle-skill** (shepsci). [Noise: octav/coinpaprika/dexpaprika/chainaware crypto, x-twitter-scraper, claude-ecom, recommendations, elicitation, crowdcast.]

**🔬 Scientific & Research Tools:** **claude-scientific-skills** *"125+ scientific skills…"* (= K-Dense, §3 — duplicate). **paper-search** *"Search academic papers via **OpenAlex** (250M+ works, free, no API key)… by keyword/DOI."* (ykdojo) 🟢. **Junshi** *"Personalized research strategist… reads your papers, tracks relevant literature, and proposes **ranked research ideas with suggested first experiments**."* (junshi-research) 🟢. **materials-simulation-skills** (HeshamFS — numerical stability/solvers/validation). **deep-research** (Gemini Deep Research agent), **manus** (delegate to Manus agent).

**✍️ Writing & Research:** **article-extractor** (full article text+metadata). **content-research-writer** (research+citations+outlines). **brainstorming** *"Transform rough ideas into fully-formed designs through structured questioning"* (obra/superpowers). **avoid-ai-writing** *"Audits and rewrites content to remove 21 categories of AI writing patterns with a 43-entry replacement table and two-pass detection"* (conorbronsdon) 🟡. [Niche: internal-comms, family-history, naming, ru-text, md2wechat, buyer-eval.]

**🔧 Utility & Automation:** **skill-creator** + **template-skill** (anthropics — build new skills). **SkillCheck-Free** *"Free SKILL.md validator with 30+ checks across structure, naming, and semantics. Catches errors before deploying"* (olgasafonova) 🟢. **task-observer** *"A meta-skill that builds and improves all your skills, including itself"* (rebelytics). **review-claudemd** *"Review recent conversations to find improvements for CLAUDE.md files"* (ykdojo) 🟡. **Imprint** (portable AI collaboration profile). **pua** *"pushes AI agents to exhaust options before giving up"*. **file-organizer / invoice-organizer**. [Noise: linkedin, hubspot, sequenzy, tweetclaw, moodtrip, agentfund, pinme.]

---

## 6. Jeffallan/claude-skills (fullstack-dev-skills) — 66 skills, MIT, 10k★
A software-engineering **persona pack** (router + MUST/MUST-NOT constraint prompts). `SKILLS_GUIDE.md` = a catalog+router, not an authoring guide. **Authoring convention worth noting:** progressive disclosure — light `SKILL.md` (frontmatter `name/description/license/allowed-tools/metadata{triggers,role,scope}`) + on-demand `references/*.md` with "Load When" conditions + `## Constraints` (MUST DO / MUST NOT DO). `allowed-tools` declared on only 3 read-only skills (code-reviewer, security-reviewer, spec-miner).

**Program-relevant skills:**
- **the-fool** — *"challenging ideas, plans, decisions… play devil's advocate, run a pre-mortem, red team, or audit evidence and assumptions."* 🟡 (a falsification *reasoning persona* — tests control-flow, not contracts)
- **prompt-engineer** (v1.2) — *"Writes, refactors, and evaluates prompts… optimized templates, structured output schemas, **evaluation rubrics, and test suites**… prompt evaluation frameworks."* 🟡
- **fine-tuning-expert** — *"fine-tuning LLMs… **LoRA/QLoRA** adapters, JSONL datasets… HF PEFT… quantizing and deploying."* · **ml-pipeline** (MLflow/W&B, Kubeflow/Airflow, DVC) · **rag-architect** (chunking/embeddings/rerank/eval). 🟡 MEMIT-adjacent **recipe-level** guidance, not empirical harnesses.
- **spec-miner** (Read/Grep/Glob/Bash) — *"Reverse-engineering specialist that extracts specifications from existing codebases… code archaeology."* · **code-reviewer** (read-only diff review) · **pandas-pro** (DataFrame analysis). 🟡
- **Remainder (off-domain):** 12 language-pros (python/rust/cpp/go…), 7 backend + 8 frontend frameworks, k8s/terraform/cloud, API/GraphQL/microservices design, testing, devops/SRE/chaos, security, platform (salesforce/shopify/wordpress), embedded/game. Useful only as coding-persona scaffolding.

---

## 7. thananon/9arm-skills — 6 skills (⚠ **no license**, 2.9k★) 🟢 methodology
Personal eng-process discipline; install `npx skills add thananon/9arm-skills`. (Author env shows Qwen/JIRA/NVIDIA.)
- **debug-mantra** — *"Four-mantra debugging discipline — reproduce, trace the fail path, **falsify the hypothesis**, cross-reference every breadcrumb… apply the four steps in order before proposing any fix."* **Refuses to proceed without a repro.** ⭐⭐ (pure falsification discipline)
- **scrutinize** — *"Outsider-perspective end-to-end review… **First questions intent and whether a simpler/more elegant approach** would achieve the same goal, then **traces the actual code path (not just the diff)** to verify the change does what it claims."* No rubber-stamps; cite-or-it-didn't-happen. ⭐⭐
- **post-mortem** — engineer-audience RCA (root cause/mechanism/fix/validation/how-it-slipped). Refuses without repro+rootcause+fix+validation. 🟡
- **qwenchance** — *"Keeps a long Claude Code task on-track — breaks out of looping/circular thinking, watches the context budget… clean handoff before the window fills."* 🟡 (long-run agent hygiene)
- **qwen-agent** — delegate menial coding to a cheap Qwen subagent — ⚠ **hard-wired to the author's private `claude-9arm` gateway**, not portable. **management-talk** — leadership comms (🔴 off-domain).
> ⚠ **No LICENSE** = all-rights-reserved by default; safe to *read/learn from* the discipline, but don't vendor/redistribute as-is.

---

## 8. virgiliojr94/book-to-skill — meta-skill, MIT, 6.5k★ 🟢
**Scope (verbatim):** *"Converts books and documents (PDF, EPUB, DOCX, HTML, Markdown, plain text, RTF, MOBI/AZW with Calibre) into structured agent skills, extracting frameworks, mental models, principles, techniques, and anti-patterns. Use when the user wants to study a document… apply an author's frameworks while working, or **build a reusable knowledge base from a file.**"*
**Pipeline:** `/book-to-skill <paths>` → content-type prompt (technical→`docling`; text→`pdftotext/pypdf`) → merge to `full_text.txt` → **cost pre-flight** (token/USD estimate, waits for confirm) → the **host agent** (no extra API key) writes per-chapter summaries + glossary + patterns + cheatsheet + master `SKILL.md` → output to `~/.claude/skills/<slug>/`. **4 modes** incl. **Mode 4 Update/Fold-in** (merge new sources into an existing skill — new chapters numbered after the highest `chNN`).
**Boundaries:** wins **narrow-and-deep** (one book / tight cluster), not wide-and-shallow (use RAG/NotebookLM for "search 80 books"); needs explicit `Chapter N` headings for auto-segment; **always synthesizes, never copies raw passages** (lossy by design); ~$1/book one-time on Sonnet.
**Fit:** 🟢 Mode 4 is purpose-built to fold the spec + months of CORPUS/runbook into one navigable, updatable skill. Caveat: synthesized (not verbatim) → a *framework layer over* the corpus, **not** a replacement for verbatim spec re-grounding.

---

## 8a. obra/superpowers — agentic skills + SW-dev methodology (MIT, 236k★) 🟢🟢
_Added 2026-06-22. The **highest discipline-fit** repo audited — its testing/verification/debugging/review skills are near-isomorphic to this program's falsification discipline._

**What it is:** *"An agentic skills framework & software development methodology that works"* (obra / Jesse Vincent). MIT, v6.0.3, ~236k★/21k forks, daily-active. Philosophy (verbatim): *"Test-Driven Development — Write tests first, always; Systematic over ad-hoc; Complexity reduction; **Evidence over claims — Verify before declaring success.**"* Skills = *"Mandatory workflows, not suggestions."*

**Structure (adoption-relevant):** multi-harness plugin/marketplace (`.claude-plugin/` + Codex/Cursor/Gemini/Kimi/Pi configs). A **`SessionStart` hook auto-injects** the full `using-superpowers` dispatcher into context every session, wrapped in `<EXTREMELY_IMPORTANT>`; dispatcher rule: *"If you think there is even a 1% chance a skill might apply… you ABSOLUTELY MUST invoke the skill."* → **opinionated, mandatory-by-design.** 14 skills, progressive-disclosure, zero third-party runtime deps.

**The 14 skills (verbatim scope):**
- **using-superpowers** — *"Use when starting any conversation - establishes how to find and use skills, requiring skill invocation before ANY response including clarifying questions"* · **writing-skills** — *"…creating new skills, editing existing skills, or verifying skills work before deployment"*
- **brainstorming** — *"You MUST use this before any creative work… Explores user intent, requirements and design before implementation."* (`<HARD-GATE>`: no code until an approved written design) · **writing-plans** — *"…a spec or requirements for a multi-step task, before touching code"* · **executing-plans** — *"…execute in a separate session with review checkpoints"* · **subagent-driven-development** — *"…implementation plans with independent tasks in the current session"* · **dispatching-parallel-agents** — *"…2+ independent tasks… without shared state or sequential dependencies"* · **using-git-worktrees** — *"…feature work that needs isolation…"* · **finishing-a-development-branch** — *"…implementation complete, all tests pass… decide how to integrate"*
- **requesting-code-review** — *"…before merging to verify work meets requirements"* · **receiving-code-review** — *"…requires technical rigor and verification, not performative agreement or blind implementation"* (forbids "You're absolutely right!")
- ⭐ **test-driven-development** — *"…before writing implementation code."* Iron Law: *"NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST."* · ⭐ **systematic-debugging** — *"…before proposing fixes."* Iron Law: *"NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST."* · ⭐ **verification-before-completion** — *"…before committing or creating PRs… running verification commands and confirming output before making any success claims; evidence before assertions always."* *"Skip any step = lying."*

They **chain**: using-superpowers → brainstorming(gate) → worktree → writing-plans → subagent-dev/executing → TDD per task → request/receive review → verification-before-completion → finish; systematic-debugging fires on any failure.

**Why highest discipline-fit:** verification-before-completion = your *pass-label ≠ promotable-claim* / *verify-edits-persist*; systematic-debugging (root-cause-first) = *bias-ablation = causal attribution*; TDD + `testing-anti-patterns.md` (a test you *watched fail*) = directly counters the **prototype-tautology trap**; receiving-code-review (technical pushback) = adversarial review without confirmation-amplification; brainstorming→writing-plans = pre-register design/criteria. Adoptable **authoring patterns** too: Iron-Law gates as pre-registered stop conditions, "Red Flags/rationalization" tables as confirmation-bias tripwires, **eval-gated skill changes** (a workflow change needs falsifiable before/after evidence).

**Caveats:** (1) **Fence** — process/reasoning aids → LEADS, never `CORPUS/` evidence; a passing self-critique is same-model confirmation-amplification. (2) **Adoption risk — mandatory-by-design + hook-injected**: installing the plugin injects a strong opinionated methodology into *every* session and could clash with the repo's own runbook/CLAUDE.md/closeout-gate. → **extract specific skills repo-local, don't install wholesale.** (3) **Telemetry:** `brainstorming`'s visual companion phones home a version ping by default (`SUPERPOWERS_DISABLE_TELEMETRY` opts out).

---

## 8b. anthropics/knowledge-work-plugins — `data` + `bio-research` (Apache-2.0, 21.7k★)
_Added 2026-06-22. Official Anthropic role plugins (Claude Cowork/Code marketplace): *"Plugins that turn Claude into a specialist for your role… file-based — markdown and JSON, no code."* Both are **MCP-connector + markdown** plugins (tool-agnostic via `~~category` placeholders); neither ships code engines. **Apache-2.0 = cleanest license audited → freely extractable.**_

### `data` plugin (v1.1.0) — 10 skills 🟡
*"Write SQL, explore datasets, and generate insights faster. Build visualizations and dashboards…"* `.mcp.json` = 8 enterprise-warehouse connector stubs (Snowflake/BigQuery/Databricks/Hex/Amplitude/Atlassian/Definite — off-domain). No commands/agents.
- **analyze** — *"Answer data questions — from quick lookups to full analyses…"* · **explore-data** — *"Profile and explore a dataset to understand its shape, quality, and patterns… checking null rates and column distributions, spotting data quality issues…"* 🟡 · **write-query** — *"Write optimized SQL for your dialect…"* · **create-viz** — *"Create publication-quality visualizations with Python…"* (matplotlib/seaborn/plotly) 🟡 · **build-dashboard** — *"Build an interactive HTML dashboard…"* (Chart.js, CDN-pinned) · **validate-data** — *"QA an analysis before sharing — methodology, accuracy, and bias checks… assessing whether conclusions are actually supported by the data."* 🟡 · **data-context-extractor** — meta-skill that authors a company-specific data skill.
- Helpers (auto-fire): **sql-queries** (dialect reference) · **data-visualization** (chart-selection reference) · **statistical-analysis** — *"Apply statistical methods including descriptive stats, trend analysis, outlier detection, and hypothesis testing… testing for significance, detecting anomalies, computing correlations…"* 🟡

### `bio-research` plugin (v1.2.0) — 6 skills
*"Connect to preclinical research tools and databases (literature search, genomics analysis, target prioritization)…"* 11 biomedical MCP connectors (PubMed, bioRxiv, Consensus, ClinicalTrials.gov, ChEMBL, Open Targets, Benchling…).
- ⭐ **scientific-problem-selection** — *"…research problem selection, project ideation, troubleshooting stuck projects, or strategic scientific decisions… pitch a new research idea, work through a project problem, evaluate project risks, plan research strategy, navigate decision trees…"* A **9-step framework** (intuition pumps → risk assessment → optimization function → parameter strategy → decision tree → adversity planning → **problem inversion** → synthesis → meta-framework), based on **Fischbach & Walsh, *Cell* (2024)**. Domain-agnostic. 🟢
- **start** (orientation) · **single-cell-rna-qc** · **scvi-tools** · **nextflow-development** · **instrument-data-to-allotrope** — all wet-lab/omics. 🔴 off-domain.

**Relevance:** 🟢 **`scientific-problem-selection`** is the standout — its risk-assessment / optimization-function / **problem-inversion** / decision-tree / **adversity-planning** modules map directly onto *pre-register-falsifiable-criteria* and *"design a test that can fail."* Apache-2.0 + domain-agnostic → safe to extract repo-local (the 9 reference files = a gate-framing checklist; Fischbach & Walsh *Cell* 2024 = a citable lead). 🟡 The `data` stats/viz/validate skills are convenience aids but **K-Dense's `experimental-design`/`statistical-power` dominate them** — these are *methodology prompts* (LLM-driven), not verified engines, and `validate-data` is an LLM **self-review** (a review starting point, not proof). 🔴 The warehouse connectors + omics skills are off-domain. **Fence:** all outputs are LEADS, never `CORPUS/` evidence.

---

## 9. Cross-repo shortlist — highest fit for the LLM-as-Database program

| Rank | Skill / tool | Repo | Why it fits |
|---|---|---|---|
| ⭐⭐⭐ | **arbor** | K-Dense | HTR experiment loop with a **held-out merge gate the search never optimizes** — directly answers the prototype-tautology / dev-test-gap traps; could coordinate G6/G7 edit-eval runs |
| ⭐⭐⭐ | **experimental-design + statistical-power** | K-Dense | Pre-registration, MDE, paired/within-unit designs, simulation power for mixed/clustered evals |
| ⭐⭐⭐ | **scientific-critical-thinking** | K-Dense | GRADE/Cochrane bias+confounder auditing of claims (your bias-ablation / pass-label≠promotable discipline) |
| ⭐⭐⭐ | **verification-before-completion · systematic-debugging · test-driven-development · receiving-code-review** | obra/superpowers (§8a) | The closest **discipline** match: evidence-before-claims, root-cause-first, a test you *watched fail* (counters prototype-tautology), adversarial review without confirmation-amplification. ⚠ extract repo-local — don't install the auto-injecting framework |
| ⭐⭐ | **statistical-analysis / statsmodels / pymc** | K-Dense | Eval stats incl. distributional (KL/JS via posterior checks) |
| ⭐⭐ | **debug-mantra + scrutinize** | 9arm | Falsification + cold-outsider-review discipline (⚠ no license — learn, don't vendor) |
| ⭐⭐ | **the-fool** | Jeffallan | Built-in pre-mortem / red-team reasoning persona |
| ⭐⭐ | **paper-search (OpenAlex, free) · litreview (Consensus) · firecrawl-research-index** | awesome / alireza / firecrawl | Literature/prior-art pull (+ verifying arXiv/DOI existence — a known trap) |
| ⭐⭐ | **firecrawl scrape/crawl** | firecrawl | Clean bulk source acquisition; WebFetch upgrade for JS pages |
| ⭐⭐ | **book-to-skill (Mode 4)** | virgiliojr94 | Fold spec + corpus into a navigable, updatable skill |
| ⭐ | **transformers / pytorch-lightning / modal / get-available-resources** | K-Dense | GPU-edit / CPU-deploy runtime substrate |
| ⭐ | **SkillCheck-Free · skill-creator · the progressive-disclosure convention** | awesome / anthropics / Jeffallan | Authoring/validating *our own* skills going forward |

---

## 10. Cross-cutting caveats (before adopting anything)

1. **Licenses:** `thananon/9arm-skills` and the `awesome-claude-skills` list itself have **no LICENSE** (all-rights-reserved) → safe to learn from, do not vendor/redistribute. K-Dense is MIT but individual skills carry their own (some GPL/`Unknown`/4 Proprietary). Firecrawl core is AGPL-3 (matters only if embedded).
2. **Data exfiltration:** several skills POST your query/content to third-party APIs — `research-lookup`/`parallel-web`/`exa-search`/`bgpt` (K-Dense), `litreview`/`grants` (Consensus), Firecrawl hosted, the Gemini/Manus delegators. **Flag for any sensitive-spec work** (the fence + secret-safety discipline).
3. **Paid / keyed:** firecrawl hosted, Consensus, OpenRouter, Modal, many `*_API_KEY` skills.
4. **Duplication:** the awesome-list's "claude-scientific-skills" = K-Dense (§3); don't double-count.
5. **Side-effects:** book-to-skill and skill-builders **write to `~/.claude/skills/`**; arbor spawns worktree subagents — same control-system-state caution as `actionize`/`llm-wiki` (`INFRANODUS_SKILLS_REFERENCE.md §5`).
6. **"Reasoning persona" ≠ measurement:** `the-fool`, `debug-mantra`, `scrutinize`, `scientific-critical-thinking` improve *process*, but a critique that passes is **not** evidence — they test control-flow, not contracts. Reserve confidence for runs that can falsify (arbor's merge gate, statistical-power's MDE).

---

## 11. Reconciled adoption order (Advisor + Codex out-of-family review, 2026-06-22)

§9 was reviewed by an in-family advisor **and** an out-of-family reviewer (Codex / gpt-5.5). The ⭐ ratings stand with **two surgical changes**, both of which are repo law (`AUTONOMY.md`: optimizer-style "make the number go up" is *the opposite of* falsification) rather than a reviewer flip:

- **`arbor` demoted** ⭐⭐⭐ → **"fenced, later, verify-first."** It is an *optimizer*; the program's north star is to *falsify*, not raise a score (Goodhart risk). Net-positive only as a fenced candidate-generator.
- **The stats lead is runnable CODE, not a persona-skill.** The bottleneck is valid inference under tiny/noisy/clustered samples — so extract *formulas/code* runnable on result JSONs, not a SKILL.md that "reminds you to do a power analysis."

**Adoption order (no adoption taken here — operator directs):**

| Priority | What | How to adopt |
|---|---|---|
| **1 — lead** | Stats/DOE from K-Dense (`experimental-design`, `statistical-power`, `statsmodels`) | **Extract as runnable code** on result JSONs: power/MDE, cluster-bootstrap over (held-out-set × edit-order), paired within-unit diffs, JS/KL with CIs. ⚠ check each source skill's license before lifting. NOT a persona-skill. |
| **2 — methodology** | `scientific-critical-thinking`, `debug-mantra`, `scrutinize`, `the-fool`, obra/superpowers `verification-before-completion` / `systematic-debugging` / `test-driven-development` / `receiving-code-review`, **+ knowledge-work `scientific-problem-selection` (§8b, Apache-2.0, problem-inversion/decision-tree/adversity-planning for gate framing)** | **Read → extract best checklists** into repo-local form (superpowers' Iron-Law gates + Red-Flag tripwires + the Fischbach-Walsh problem-selection steps map directly onto pre-registration + falsifier framing + confirmation-bias guards). ⚠ **do NOT install the superpowers framework** (its SessionStart hook auto-injects a mandatory methodology that would clash with the runbook/CLAUDE.md); don't vendor unlicensed (9arm) code. "Passed critique ≠ evidence." |
| **3 — wire as tool (low-risk first)** | `paper-search` (OpenAlex, free, no key) → then `firecrawl scrape` if needed | Tool/API, not a reasoning layer. Firecrawl: exfiltration labels + source snapshots/hashes; AGPL only matters if embedded. |
| **4 — trial later, fenced + verify-first** | `arbor` | Only after the measurement frame is stable **and** after source-verifying the "held-out merge gate the search never optimizes against" (currently a subagent paraphrase — that property is the whole case for arbor). Candidate-generator only; never writes CORPUS / revises criteria / touches held-out / picks the verdict / runs unbounded. |
| **5 — skip / defer** | `book-to-skill` for canonical docs; unlicensed vendoring; the awesome-list | book-to-skill "synthesizes, never verbatim" is a near-dealbreaker for precise spec provenance — only as a citation-first navigation helper pointing back to exact files. Awesome-list = discovery index only. |

**Review caveats folded in:**
- **Codex reviewed a pasted summary in a broken read-only sandbox** (couldn't load files) → weight it as a *reasoning* check, not source-verified. Verify adoption-critical specifics (esp. arbor's merge gate) from source before acting.
- **"Derive a repo-local skill from K-Dense" inherits the vendoring license question** — K-Dense per-skill licenses are mixed (GPL/Unknown/Proprietary); check the specific source skill before lifting text.
- **Firecrawl's need is concrete, not hypothetical** — this session WebFetch 403'd on `support.noduslabs.com` and `/api` was JS-thin/unreadable; `scrape` is the fix.

**Missed risks (both reviewers):** installing many third-party skills expands the **prompt-injection attack surface**, adds **trigger-collision / auto-activation noise**, **maintenance burden**, risk of **dependency conflicts** with the pinned ML stack, and **leaking unpublished spec** to external APIs. Because the operator is learning ML, over-tooling can **outsource the exact judgment the program must build** (what's a valid falsifier, what's a confound). → bias toward **fewer, repo-local, reference-extracted**.

**Meta-conclusion (both agree):** external skills are **not** the bottleneck — disciplined experimental design, clean evidence interpretation, and resisting optimizer pressure are. Favor measurement scaffolding over autonomous search.

---

_Document type: process/reference (no experiment D-ID; not subject to `closeout_check`). Captured 2026-06-22 by cloning/fetching all 10 repos (8 original + obra/superpowers §8a + anthropics/knowledge-work-plugins §8b); §11 adds the Advisor + Codex (gpt-5.5) out-of-family review. The full per-skill verbatim text for the large collections (K-Dense 147, Jeffallan 66) lives in the source repos; this audit quotes the high-fit subset verbatim and groups the rest._
