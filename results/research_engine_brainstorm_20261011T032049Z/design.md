# Research engine — design for MAESTRO

Design date: 2026-10-11 UTC. Prepared by BRAIN1 with the operator.
Status: sections and phases agreed; final written-design approval requested. This document does not authorize implementation, installations, service provisioning, experiments, or launches. MAESTRO owns the next build brief and commits.

## One-page summary for the operator

The engine will help us understand the research we already have, discover possible solutions, and choose experiments that can settle important questions. It serves the whole LLM-as-Database program and its central buildability question, F1. It can develop original ideas from our results, connect methods across fields, and use outside papers without being limited to published answers.

Git keeps the authoritative research record. We add a written vocabulary for the things we track and their connections. Two searchable copies serve different purposes: DuckDB compares measurements; Neo4j follows connections among hypotheses, experiments, findings, decisions, papers and spec requirements. Both use the same dated source snapshot and can be rebuilt. Raw model files and tensors stay outside these databases, referenced by their identities and locations.

People use conversation, an explorable research map and regular briefings through the existing LabViz workspace. Agents have direct tools for every feature and share the same records, evidence rules and task history. They investigate and prepare work autonomously. Each experiment needs its separate go-ahead. Work that could block your own use of the GPU, CPU, memory or disks requires human approval unless an existing management system already covers that particular workload. An approval already covering the work is reused; resource availability alone is not permission.

You can add a paper, idea, question or direction change at any point. The engine acknowledges it and shows how it affected the investigation. It keeps the history and does not silently rewrite a frozen experiment. Agents can save progress, continue other authorized investigation while waiting, and hand work to a fresh agent without losing the sources or approvals.

Existing features join the loop: InfraNodus suggests possible bridges in research text; MathLab examines approved mathematical questions and displays them in Marimo notebooks; AutoResearch supplies candidate recipes. The current isolated AutoResearch loop keeps its restrictions. A separately reviewed guided mode can receive approved starting ideas. All optimizer results remain candidates for independent scientific confirmation. MathLab's stopped prediction-and-ranking path stays stopped until its documented restart conditions are met.

The engine shows where evidence comes from, what it applies to, and what remains unknown. Machine-suggested links stay visibly separate from checked connections. Gap reports explain incomplete indexing. Mathematical estimates, software checks and model experiments keep their different meanings.

We build in five phases. The first is deliberately small: roughly five hand-checked evidence chains, a vocabulary, both database views and direct agent queries, under an approved resource budget, with no model experiment. Later phases cover the full program, connect LabViz and agents, integrate discovery tools, and verify approved follow-through. Success means trustworthy, useful research work; a negative experiment result is welcome when it resolves uncertainty.

## Operator goals, in their words

> "I've been pondering methods and features to add to our science stack that will give us the ability to effectively manage and connect all of our experiments and data in order to powerfully reason, ideate, hypothesize, experiment effectively and efficiently with it. What tool and framework integrations can we leverage to build a first-class scientific engine that is able to reason across our data beyond existing research papers, with the intent of finding our own solutions that existing research may not already cover? Or connecting existing research together for solves? Or surfacing new novel creative experiments in order to solve...etc, etc, etc. My first thoughts are developing an Ontology system for the FULL CORPUS and data and also integrating a queryable database framework. The idea being that the two together provide a robust system for exploring, ideating and managing all of our research, experiments, hypothesis, data, findings, etc without any gaps."

## Decisions and exact operator words

The entries below preserve the operator's responses and dates. Option letters are interpreted in decisions_log.md, which contains the corresponding choice text and approval scope. Approval of sections does not authorize execution.

### 2026-10-11 03:25 UTC — Include all three outcomes

> All - A, B and C

### 2026-10-11 03:26 UTC — Manage follow-through

> C

### 2026-10-11 03:28 UTC — All human views and agents as first-class users

> A, B and C. And the engine must treat agents as first class citizens for autonomous work as well.

### 2026-10-11 03:32 UTC — Autonomous investigation; human approval for experiments and resource contention

> C. And any work that impacts GPU/CPU/SSD/HDD resources that block other work, ask for me to not run my own other work on my system, etc require HIL UNLESS already managed by our autonomous management systems such a gdrive back, etc.

### 2026-10-11 03:32 UTC — Operator can interject into the research loop

> And of course if I surface research or ideas I am able to interject into the loop

### 2026-10-11 03:38 UTC — Use DuckDB and Neo4j with the proposed division

> Both with that division

### 2026-10-11 03:40 UTC — Approve records and trust section

> Yes

### 2026-10-11 03:50 UTC — Approve MathLab and InfraNodus roles; request AutoResearch and LabViz integration

> It does fit my intent. Additionally, how might the AutoResearch feature fit into the research engine stack and loop? Also, integration with the existing LabViz dashboard?

### 2026-10-11 04:00 UTC — Approve LabViz integration; clarify AutoResearch routing

> LabViz integrations approved. One clarification about AutoResearch: so the engine would never send possible experiments to it to test? Even after an experiment is run through the scientific loop? How would the loop determine when to invoke AutoResearch?

### 2026-10-11 04:06 UTC — Guided AutoResearch mode and autonomous agent access across all features

> I choose A. One more clarification/requirement: all of this must treat agents as first class citizens so they are able to work autonomously with all features.

### 2026-10-11 04:08 UTC — Approve agent workflow

> Yes

### 2026-10-11 04:10 UTC — Approve phases and first test slice

> Yes

## Alternatives considered and selected direction

| Approach | Benefit | Cost or limitation | Decision |
|---|---|---|---|
| Git-backed vocabulary and DuckDB only | Small foundation; strong measurement queries; relationship chains are possible with recursive queries. | More work to express complex connection questions; fewer purpose-built graph exploration tools. | Useful baseline for comparisons, but insufficient as the selected target by itself. |
| Shared cloud copy through Neon from the start | Convenient shared access; query computation can happen away from the Mac. | Service/access costs and network dependence; ingestion still consumes local resources; adds another copy to maintain. | Deferred until a concrete shared-serving need is established. |
| Neo4j-centered foundation with a measurement path | Purpose-built relationship queries and optional graph algorithms. | Numerical analysis still needs an appropriate measurement system; more operational work. | Combined with DuckDB rather than used as the sole foundation. |
| DuckDB and Neo4j together, backed by Git | Measurement comparisons and connection exploration share one checked record model and source snapshot. | Two rebuildable copies need consistent publication and testing. | Selected: Git authority; DuckDB measurements; Neo4j connections; engine combines answers. |

Neo4j does not create scientific understanding by itself or guarantee a speed advantage. DuckDB can also traverse graphs. The value to verify is clearer relationship queries and useful exploration on this program's questions. A visible map alone does not require a graph database, but the operator selected Neo4j for the broader connection work.

Additional possibilities considered beyond the original suggestions:

| Capability | Value and trade-off | Design treatment |
|---|---|---|
| Questions answered with evidence | Makes the record usable; persuasive prose can conceal missing evidence. | Include exact sources, scope and missing-information statements. |
| Trace a number and its downstream consequences | Helps audit claims and reconsider conclusions when an input changes. | Include source measurements, calculation recipes and dependency paths. |
| History of changing beliefs | Explains reversals and reopening a route; dates and revisions can be ambiguous. | Preserve superseding decisions and dated source versions, with ambiguity reported. |
| Competing explanations and counterexamples | Moves beyond retrieving documents to designing informative tests. | Include skeptical critique and cheap tests that separate explanations. |
| Transfer ideas across fields and papers | Helps develop solutions absent from our existing methods; superficial analogies can mislead. | State the proposed mechanism, differences, evidence and testable prediction. |
| Estimate the value of an experiment | Helps spend scarce time on uncertainty reduction; uncalibrated numerical scores can mislead. | Start with explained reasoning about value, cost and readiness. Learned ranking requires separate validation. |
| Similarity search and graph analysis | Can suggest less obvious connections; requires resources and can confuse similarity with support. | Optional tested enhancements; inferred links remain proposals. |
| General-purpose agent platforms | Could coordinate agents; may duplicate MAESTRO and existing managers. | Provide direct tools and resumable tasks first; choose a framework only for a demonstrated missing capability. |

## Foundation and ownership

1. **Authoritative records:** existing CORPUS, program_state, decisions, preregistrations, registries, review receipts and their Git revisions remain authoritative. Add reviewed structured links in Git, pointing to those sources rather than restating evolving conclusions across files. A link cannot override the meaning of its cited finding.
2. **Vocabulary and checks:** one versioned definition describes kinds of records, required information and allowed connections. LinkML is the recommended starting tool; its generated record-shape checks do not replace scientific review or checks that a link means what it claims. This research vocabulary does not silently amend the product spec.
3. **Measurement copy:** DuckDB reads admitted result families through explicit adapters and stores normalized measurements, scope information and source pointers. It retains enough IDs/links for independent joins and consistency checks.
4. **Connection copy:** Neo4j represents hypotheses, scoped claims, runs, findings, decisions, papers, tasks and their links. It stores selected measurement summaries and pointers, avoiding a second copy of all raw measurements or tensors.
5. **Research service:** combines queries, evidence retrieval, proposal tools and task/approval information for agents and people. Scientific answers use both stores at one source snapshot. Runtime ownership/admission remains with existing managers.
6. **Human workspace:** LabViz reads published views and uses the shared service for conversation, submissions and requests. Published evidence remains available if the interactive service is down.

Both databases are disposable read/analysis copies. Agents submit staged proposals and changes through the authorized workflow; they receive no unrestricted direct science-database writes. Accepted corrections return to the authoritative Git-owned sources or reviewed-link record before rebuilding. Live task state and locks belong to the existing manager; finalized scientific records and their source identities belong in Git. A dashboard or database cache cannot overrule either authority.

Publish the two views as one generation. Its manifest names the Git revision, exact source-file hashes, artifact references, importer/schema versions, reviewed-link set, coverage and both database generations. Build new generations separately, validate them, then publish one manifest selecting the pair. Pin that selection for the entire combined request. A failed build keeps the last complete generation visible with its age; a mixed-generation query refuses a complete answer or explicitly returns a partial one. Ongoing files are identified as live/uncommitted and captured by exact immutable snapshots before supporting a scientific claim.

Git may pin large artifacts stored outside Git. A source manifest records their identities, storage references and retrieval requirements. Missing or archived data is reported explicitly. Retrieval through Drive or another service uses approved scope and management; the engine does not silently fetch bulk data. Rebuilding only from available sources must state its coverage.

## What we track and how we trust it

| Group | Record kinds | Example connections |
|---|---|---|
| Questions and ideas | Question, hypothesis, scoped claim, competing explanation, proposed idea | tests, supports, refutes, alternative-to, builds-on |
| Tests and evidence | Preregistration, experiment definition, run, arm, measurement, finding | registered-by, produced-by, measured-in, derived-from |
| Direction and history | Decision, review verdict, spec obligation/cell, lesson, paper claim | supersedes, qualifies, reviewed-by, bears-on, cites, blocked-by |
| Work and responsibility | Agent, assigned task, approval, source/artifact version | assigned-to, requires-approval, uses-source, requests-analysis, halted-by |

These are a starting vocabulary, not an arbitrary ten-kind limit. Preserve existing IDs and use explicit aliases for new normalized records. Separate an enduring record identity from a particular source version. Ambiguous old names require review; text similarity alone cannot merge two records. A paper and a specific claim inside it are distinct, as are a planned experiment and one run of it.

Every evidential link records its source span or JSON location, source revision/hash, scope and review history. Whether a link was explicitly stated, machine-inferred, checked, rejected or superseded is separate from whether the underlying experiment passed, failed, halted, was invalid or was not run. Retain original program outcome labels and caveats. Checked attribution does not automatically make a claim scientifically proven.

Measurements retain the value, unit, metric definition, numerator/denominator when relevant, evaluation split, model/setup, seed, run and arm. Derived numbers retain their source measurements and calculation recipe. Missing denominators are marked missing, never guessed. Comparison rules must verify compatible meanings, evaluation exposure, scope and units before pooling or ranking results. Differences across scopes are not automatically contradictions.

Keep software/fixture checks, mathematical estimates, exploratory optimizer outputs, paper claims and real scientific observations distinguishable. Halted runs may contain legitimate partial measurements; they cannot appear as full passing tests. Preserve replaced evidence in the history. A chain of support links is not a transitive proof of causation or generalization.

Import explicit structured links deterministically when possible. Extracted links from prose become source-cited suggestions awaiting review. A semantic support check must reject unsupported meaning even when a link's ID and syntax are valid. Changes to relevant source content mark its reviewed links stale for reconsideration.

Full coverage means an accountable inventory, not a promise that every relevant fact has already been understood. Report indexed items, deliberate exclusions, missing artifacts, unsupported formats and links awaiting review. Distinguish a genuinely untested hypothesis from a part of the record not yet inspected. Show suspected contradictions and missing links as questions until their scope and source coverage are checked.

## Research loop and proposal contract

An investigation begins with an open F1 question, operator input, surprising outcome, suspected contradiction, or possible missing connection. Retrieve relevant sources, measurements, limitations, previous attempts and superseding decisions before generating ideas. Prior rejection is not permanent: show new evidence or changed scope when proposing to reopen a route.

Generate possibilities through several routes: explain a result that missed its registered expectation; connect similar effects across method families; propose mechanisms; transfer relevant methods from another field; combine compatible ideas; challenge the problem framing; or identify a missing control that would separate explanations. The engine can invent new methods suggested by observations; it need not find an existing paper containing the answer. Graph/text patterns suggest where to look and do not constitute evidence.

Develop several competing explanations and use a separate skeptical pass. Failure/surprise investigations honor DISCIPLINE's minimum three explanations, including a possible confound, and its independent-review requirements. Report actual reviewer model/role and strength of independence. Exploratory critique is separate from Astra's binding promotion gates.

Every proposal card includes:

- Question and the F1/spec obligation it would advance.
- Supporting/opposing source claims, measurements, limits and previous attempts.
- What is new relative to the local and outside material actually searched; uncertainty about wider novelty.
- Competing explanations, explicit predicted differences and possible confounds.
- Cheapest informative test, controls and what would disprove the idea or separate explanations.
- Proposed measurement, expected outcomes, and what each would change. Scientific criteria need review and freeze before execution.
- Time, memory, GPU/CPU/disk use, source/storage access, likely interference and required approvals.
- Dependencies, assigned work, review state and source identities.

Initially rank recommendations through visible reasoning about uncertainty reduced, ability to distinguish explanations, cost, readiness and operator priorities. Do not claim calibrated probabilities or an objective best-experiment score. New learned/proxy ranking needs separate calibration and prospective usefulness evidence; it cannot quietly reactivate the shelved MathLab policy.

Route work according to its purpose:

| Need | Appropriate route |
|---|---|
| Test a particular explanation or intervention | A separately preregistered scientific experiment. |
| Examine a mathematical consequence | An approved MathLab analysis under its own method and execution gates. |
| Find a better recipe within fixed conditions | An approved AutoResearch optimization mission. |

After applicable review and operator approval, execution uses the existing authorized manager. Collect durable outcomes, preserve negative/invalid/partial states, stage the closeout and complete canonical scientific recording through MAESTRO. Existing ALL GREEN closeout remains required before declaring scientific closure. The next investigation can then use the reviewed record. Novel suggestions or optimizer wins do not bypass this path.

## Agents, operator steering and authority

Every feature has direct structured agent operations. Agents can query both stores, inspect coverage/history, submit sources and proposed links, investigate explanations, critique and prepare experiments, draft MathLab analyses and optimization missions, read outputs, request approvals, carry authorized work forward, stage closeouts and produce briefings. They do not need browser automation to access core capabilities. Human conversation and LabViz use the same operations and records. A documented service with agent adapters, including MCP where appropriate, is recommended; the exact runtime framework is a later bounded implementation choice.

An operation returns stable IDs, source snapshot/evidence, status, missing information and the next required action or blocker. A work item records role/owner, authorized scope, exact input identities, expected output, prerequisites, progress, approvals, checkpoint and handoff. Repeat submissions after disconnects must identify the same request rather than create another run. Use existing MAESTRO/managers for execution ownership and resource locks.

Agents autonomously investigate and prepare proposals within assigned authority. Each experiment needs its separate go-ahead. Work that could contend with other work through GPU, CPU, memory, SSD/HDD or require the operator to keep the machine quiet requires human approval unless an existing autonomous manager is verified to cover that exact workload. This includes database/graph rebuilds, large queries, embeddings, graph algorithms, bulk reads, local model jobs and notebook calculations. Read-only work can still be expensive. Host observation being unavailable cannot be treated as idle.

Existing management coverage is specific, not a general exemption for any installed tool. Drive backup was the operator's example; this session did not establish its current activation or coverage. A resource exemption does not approve a new experiment or override a feature's operator-launched contract. Paid-service/credential and corpus-export permissions remain applicable.

Approval requests explain the action, bound source/code identities, review prerequisites, expected duration/resource footprint, interference, stop conditions and exact coverage. Reuse valid authorization for work already covered. Relevant changes require rechecking its coverage; unrelated repository edits need not invalidate everything. Waiting, denial or timeout is not approval. An agent saves progress and may continue other independently authorized investigation. Resume requires valid permission and gates with matching relevant inputs.

Operator ideas/papers/questions enter a shared inbox with original wording, provenance and acknowledgment. Show adoption, changed priorities, a follow-up task or an approval/amendment requirement. Explicit stop requests stop work. Suggestions do not silently alter frozen criteria or hijack a live run. Operator direction controls scope and priorities; source claims still require evidence.

## Integration contracts

### MathLab and Marimo

MathLab is an integrated but independently gated workbench. Agents draft source-linked analysis requests and examine published outputs; approved calculations produce durable manifests and inspectable formulas, assumptions and plots. Marimo provides the human notebook view. Reuse existing MathLab JSON pointers, source hashes, derived index and authoritative event reader/fold. Index specific admitted records; do not import all tensors into either database. Completion/verdict claims require durable terminal state, not merely readable bytes or an exit code.

The core engine works while MathLab is stopped or irrelevant. Its original calibration failed and proposal-ranking step 4 remains shelved. Import its history and stop faithfully. Restart needs the documented written amendment and new calibration on unused arms; proxy-driven queue influence additionally needs prospective usefulness evidence. Other diagnostics retain their own independent approvals. A mathematical result can constrain an explanation within its scope but cannot establish model recall improvement.

Publish existing notebook outputs by default. Marimo can rerun dependent cells after interactions; viewing a notebook is not a resource permission boundary. Heavy controls go through admitted execution/approval checks. Forms/lazy or disabled cells help avoid accidental reruns but are not substitutes for the external gate. Agents receive the same calculation/result access through structured tools.

### InfraNodus, papers and extracted connections

InfraNodus examines topic connections in selected research text and can suggest bridges between underconnected discussions. Neo4j holds our recorded/checked scientific connections; InfraNodus supplies leads about where to investigate. Use it for cross-mechanism questions, comparisons with outside work and broader exploration when stuck. Text gaps may arise from wording, omissions or irrelevant relationships.

Record the exact export, input hashes, identifiers, caveats, included/excluded sources, request/tool identity and saved response. New transmissions require applicable authorization for the corpus/export and service scope. Reuse authorized saved responses when adequate. Retrieve complete underlying findings and check whether a suggestion is already known before developing its test. Never turn service confidence, text centrality or generated questions into accepted evidence or queue authority.

The saved trial used 25 condensed findings: its three generated questions were already known; local reading sharpened one then-new testable adapter-geometry question. That is modest trial-specific value, not proof of a general novelty yield. Evaluate added value against the existing agent/Neo4j workflow without InfraNodus. Zero useful new leads is a valid result.

Use arXiv search and Perplexity for named outside gaps after checking local research. External claims need primary sources, scope and verification before scientific reliance. graphify is a candidate extractor of provisional document links; MAESTRO must identify the exact package/interface and establish accuracy before integration. Text search is baseline; resource-approved semantic search is optional. All extraction tools use the same checked-versus-inferred rules.

### AutoResearch: independent and guided search

The current C10 AutoResearch remains isolated, operator-launched and sealed under its existing contract. The research engine can collect its candidate histories from outside: recipe/source revisions, search conditions, seed, scores, guards, failures and baseline. Capture exact stable candidate exports rather than treat an appending results table as a frozen scientific record. No integration changes the current launch/stop rules, evaluation guards or sandbox context.

The engine can recommend invoking this existing mission when optimization is appropriate, but cannot feed it CORPUS, papers, scientific explanations or selected seed experiments. A reviewed idea instead gets its direct scientific proposal. Scientific results may also motivate a separately reviewed new optimization mission. Completing an experiment alone does not authorize that search.

The operator chose an additional guided mode for future missions. It can receive approved ideas or starting recipes, with the allowed context explicitly declared in a new reviewed mission contract. It must be distinguishable from the isolated search in sources, results and UI. Preserve fixed search measurements/controls, instrument validity, source/context boundaries and independent scientific confirmation. Search feedback and confirmation exposure must remain separate. This is a new capability to build and review, not an already available launch mode.

An optimization request states why search is useful, the mission/mode, mutable and fixed parts, measurement/control validity, candidate contract, exposure limits, resources, launch/stop rules and the separate confirming experiment. Agents prepare it; HIL and scientific/resource gates authorize execution through the existing permitted manager. Kept optimizer recipes are candidates, not scientific verdicts.

### LabViz

Extend the existing dashboard with research connections, investigations/proposals, conversation, briefings, operator inputs and links to notebooks/candidate histories. Preserve existing views and their evidence rules. Each question can link to supporting/opposing findings, run cards, exact measurements, decisions, tasks and proposals. Whole-program research coverage extends beyond the existing C10-centered views.

Reuse existing source/metric definitions and MathLab event ingestion; do not invent another run-state or score authority. Keep accepted scientific records, exploratory optimizer outputs and mathematical estimates visibly distinct. Show missing fields, exclusions and stale snapshots in human and agent views.

Recorded pages consume small published views, not unbounded database queries or model jobs on page open. An authenticated research service handles submissions, conversation and requests. Approval controls use existing authorized managers and cannot directly bypass them to launch a model. New services or heavier builds do not inherit the current builder/server resource exemption. Actual mobile/browser and host acceptance must be demonstrated during implementation; no such check was performed in this session.

## Delivery phases and acceptance

These are engineering acceptance checks, not scientific preregistrations or F1 closure. MAESTRO freezes each build brief, independent expected answers, allowed files, dependencies and resource budget before implementation. All core, human and agent features remain in the target design.

| Phase | Deliverable | Check before expansion |
|---|---|---|
| 1. Small end-to-end slice | Roughly five hand-checked chains spanning scoped positive, negative, halted/incomplete, superseding and mathematical records; vocabulary; both database views; minimal agent queries. | Exact agreement with independent expected answers; source hashes/locations resolve; original scope/outcome tiers preserved; same snapshot; rebuild reproduces normalized records. Invalid links, incompatible comparisons, stale/missing/malformed sources and duplicate IDs are caught. Agent queries work without a browser. No model experiment or bulk tensor loading. |
| 2. Full-program inventory and connections | CORPUS/masters, program state/decisions, hypotheses/registry, full spec/maps, fingerprints/reproducibility, lessons, reviews, prior art and result/artifact families; gap reports. | Every inventory item accounted for; reproduce current proven/open/qualified picture with zero unexplained mismatch; cover six spec layers and agreed F1 obligations. Seeded missing links are detected and a scope-incompatible apparent contradiction is handled correctly. Machine extraction cannot promote evidence. |
| 3. Shared human/agent workflow | LabViz views, direct tools, resumable investigations, submissions, briefings and approval requests. | Views agree on IDs, source records and status. Agent investigation-to-proposal and successor handoff work. Operator input is acknowledged and visible. Duplicate requests create one task; denied/missing/stale approvals block execution. Viewing published pages starts no heavy job. Actual browser/mobile acceptance receives its own approved check. |
| 4. Discovery and existing-tool adapters | Proposal/explanation/critique workflow; outside sources, InfraNodus, MathLab history, AutoResearch histories and isolated/guided requests. | Predetermined question set and review rubric check source correctness, alternatives, novelty bounds, controls, resources and usefulness versus existing workflow. Known ideas are recognized. No useful idea is an acceptable outcome. Preserve MathLab stop/tier and optimizer isolation; guided contract independently reviewed. |
| 5. Approved follow-through | Existing-manager adapters, durable outcome collection, staged closeouts and the next investigation. | Harmless fixtures exercise denial, contention, unavailable host observation, crash/reconnect, repeated callbacks, stop/replan and undurable/corrupt outcomes. No duplicate run or false completion. Then one separately approved real end-to-end task, with its actual outcome honestly retained and applicable canonical closeout complete. |

Phase 1 is the first implementation brief: approximately five independently checked source chains, the vocabulary, two rebuildable copies and a small agent interface. Collect expected answers from original sources before importer development. Compare Neo4j and DuckDB connection answers on this slice, recording query complexity and approved resource use. No speed or novelty benefit is assumed. The pilot can use existing data and negative-path fixtures; it does not require new science.

Phase 2 inventory does not indiscriminately decode every JSON file. Use per-family adapters, bounded scans and approved incremental builds. Every exclusion has a reason. All selected scientific records are followed through their relevant source chains, with full-program status independently checked before the engine is relied on.

For phase 4, freeze the workload/rubric before inspecting evaluation outputs. Compare optional integrations with a no-integration baseline; record reviewer judgments as judgments, alongside source accuracy, time, service cost and locally nonduplicative actionable proposals. Automated suggestion volume is not success.

For phase 5, fixture success cannot establish host/scientific operation. A negative, halted or inconclusive scientific outcome may still demonstrate correct engine handling. A no-model host control can prove orchestration within its own scope, but cannot substitute for an actual science path if claiming that path works. This document authorizes no live test.

## Risks and implementation choices still to settle

| Risk | Required response |
|---|---|
| Machine-invented or misunderstood links | Source spans, inferred status, reviewed promotion and semantic negative controls. |
| Database views disagree or lag | One source manifest/published generation; explicit partial/stale answers; rebuild and parity checks. |
| Incomplete indexing looks like a scientific gap | Accountable inventory, coverage reports, missing/excluded states and source-specific adapters. |
| Different setups look contradictory | Compare scope, metric meaning, controls, seed and evaluation exposure first. |
| Plausible ideas or search wins appear proven | Separate proposal/search/math/science statuses and independent preregistered confirmation. |
| Heavy computation interferes with operator work | Specific resource approval or verified manager coverage, actual admission and stop behavior. |
| Guided integration contaminates isolated discovery | Separate contracts/context modes; checked export and access boundaries; no silent seeding. |
| Two new databases create maintenance burden | Small pilot, shared model, disposable views, reproducibility and measured utility. |
| Graph/topic popularity biases ideas | Multiple proposal routes, skeptical critique, baseline comparison and honest no-yield outcomes. |
| Agent retries or handoffs duplicate work | Stable request identity, existing ownership/locks, saved progress and approval/source rechecks. |

MAESTRO must settle these implementation choices in reviewed briefs:

- Neo4j hosting/edition and whether its optional analysis library is useful; current prices/account limits/access were not checked. Off-Mac hosting may reduce local query contention but adds service/access decisions.
- First exact five chains, expected-answer set, schema fields/link checks and importer scope. LinkML remains the recommended vocabulary tool; dependency provisioning is unapproved.
- Approved CPU/memory/disk/time budgets, concurrency and refresh schedule for each job. Apply the repo's projected-writes-plus-20-GiB disk rule where relevant.
- Exact agent-service/manager adapters, authentication, operation vocabulary and runtime ownership receipts. Preserve existing manager authority rather than build another scheduler.
- Guided AutoResearch mission context, editable scope, evaluation exposure and independent confirmation protocol. The capability is selected; no mission is runnable from this design.
- Exact graphify identity/interface and MAESTRO connector access to arXiv/InfraNodus/Neon. Corpus exports and service scope require applicable permission.
- Proposal-quality rubric, independent evaluation set and criteria for optional similarity, graph algorithms, ranking or cloud serving.

These are deliberately deferred implementation decisions. They do not reopen the operator's chosen scope or authority model. There is no guaranteed globally complete ontology, worldwide novelty detector or calibrated experiment-ranking model in this design. The engine makes gaps and uncertainty visible and progressively closes them through checked work.

## Grounding and capability checks

Read-only checks were made in worktree-c10k-route-a, beginning at inspected commit d06fe43e. The shared checkout can advance; a later builder must pin its own current sources.

- docs/program_state.json already supplies structured program state and generated status. docs/experiment_registry.json already links scripts, results, findings and decisions, with some early blank decision IDs. Existing structure is reused, not discarded.
- tools/closeout_check.py and DISCIPLINE.md describe presence and fingerprint-currency checks. The engine adds checks that connections mean what they claim; it does not replace closeout.
- docs/SPEC_EXPERIMENT_OVERLAY.md and docs/SPEC_E2E_GROUND_TRUTH.md provide spec coverage and six-layer context.
- Metadata-only counts: 66 top-level CORPUS Markdown files, 62 numbered; 187 top-level memory_mirror Markdown files. These definitions differ from the brief's approximate 67 evidence documents. No bulk result scan was performed; the brief's result count/size and decision count were not independently verified.
- mathlab/m2_solve_repro.py and mathlab/index.py verify notebook and source-linked index patterns. CORPUS/60_MATHLAB_HARVEST_REPLAY.md:74–137 and docs/MATHLAB_STEP4_PREREG.md:3 verify the current calibration stop/shelving.
- results/mathlab_staging/infranodus_trial/SUMMARY.md supplies the modest historical trial observation, not a new inference about today's novelty.
- docs/AUTORESEARCH.md:3–5,53–70 records optimizer isolation, candidates and independent confirmation. Its current entry describes v13; later historical launch instructions must not override that entry.
- tools/labviz/README.md, tools/labviz/build.py:507–510 and tools/labviz/app.js MathLab branches verify existing evidence views and shared-event integration. No build, browser check, notebook execution, model load or experiment was performed.
- The live BRAIN1 callable-tool list exposed Perplexity; it did not expose arXiv, InfraNodus, graphify or Neon. This says nothing about MAESTRO's separately reported tool access, which must be verified before implementation relies on it.

Official documentation consulted for capability checks, rather than implementation validation:

- [LinkML: record vocabulary and generated checks](https://linkml.io/linkml/intro/overview.html).
- [DuckDB: JSON loading](https://duckdb.org/docs/lts/data/json/loading_json) and [relationship traversal](https://duckdb.org/docs/current/sql/query_syntax/with).
- [Neo4j: relationship model](https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/), [variable-length connection paths](https://neo4j.com/docs/cypher-manual/current/patterns/variable-length-paths/) and [optional graph-analysis algorithms](https://neo4j.com/docs/graph-data-science/current/algorithms/).
- [Neon architecture](https://neon.com/blog/architecture-decisions-in-neon): hosted Postgres capability, without checking current pricing or provisioning.
- [InfraNodus tool descriptions](https://infranodus.com/mcp/tools).
- [Marimo execution controls](https://docs.marimo.io/faq/) and [SQL integration](https://docs.marimo.io/guides/working_with_data/sql/).

## Self-review and handoff contract

Inline self-review reconciled the selected two-database foundation, agent access versus execution authority, current isolated versus future guided optimization, MathLab stop conditions, shared snapshots, source coverage, and fixture versus live acceptance. Earlier alternatives are retained as considered options, not competing selected designs. The exact decisions log remains alongside this file. BRAIN1 self-review is not Astra review.

Next step: operator review of this final written document. On approval, BRAIN1 records it and returns the exact MAESTRO-ready token and path. MAESTRO takes the next steps: independent review and a narrow phase-1 brief before any build or resource use. No writing-plans transition, implementation, installs or commits occur in this session.

Binding context directive: watch Context N% left. Start new work only at >=60% left. At <=40% left, or on any Context compacted, stop new topics; update design.md and decisions_log.md; write handoff.md with done, open questions, latest preferences and one next step; restate this directive; tell the operator a fresh partner will continue; reply BRAIN1 HANDOFF. Every successor and team session must preserve this directive.
