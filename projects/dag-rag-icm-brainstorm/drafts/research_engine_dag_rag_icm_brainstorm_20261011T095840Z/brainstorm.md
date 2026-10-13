# DAG, RAG and ICM for the research engine

## Operator summary

Start by testing a short answer sheet that points to the original records.
The approved engine already plans connected records, evidence lookup and clear handoffs. (D:108–142,177–185)
A separate graph system would mostly repeat those plans; small checks on dependencies may help.
Better search is useful if it reliably includes corrections, limits and unanswered questions.
A saved lesson shows one builder used 36% of its context before its first edit. (TB:7–11)
Clear reading instructions may reduce that waste; shorter instructions must still carry the rules.
Helping researchers find facts does not prove that the proposed system can keep facts inside its model. (F:7–20)
Keep this work behind the other builds, as requested; the Intel setup still appears in the queue. (Q:35–65)
Test each small addition against the approved engine and the short answer sheet.
Drop it if it adds errors, another source of truth, or too little benefit to justify its upkeep.
This is a finished evaluation, with proposed tests; none of those tests has been run.

## Purpose, assumptions and evidence limits

BRD2 continues BRD's document-only brainstorming. The question is whether DAG, RAG or ICM removes a demonstrated research problem beyond the approved foundation. The recommendation below is an evaluation judgment, not a design freeze, build plan, engineering acceptance or scientific finding. The operator requested deferral until other build work is complete. This report accepts that timing.

Source keys such as D:108–121 resolve to exact file paths and line ranges in [sources.md](sources.md). Statements marked **General knowledge** explain concepts; statements marked **Judgment** are prospective assessments. Scores, effort ranges and pilot thresholds are proposals, not measurements or approved preregistrations.

The hardware boundary for this evaluation is the operator's M3 Pro with 48 GB unified memory and the Intel support Mac, with no cloud GPU. The newer hardware direction places Neo4j/DuckDB on Intel-local copies and forbids local model inference, training, editing and model-based embeddings on Intel. Model work on owned Macs belongs on M3. Shared-disk operations have a separate coordination requirement. These are design constraints, not commissioning evidence. (H:226–247)

The refreshed queue's edited timestamp is 2026-10-11T10:21:37Z. It lists the Intel first-build rewrite as in_review and reports a raised 2 GB setup allowance, with pilot plus setup totaling 7 GB. Its latest note says install-freeze v2 is written, three Intel checks remain unsettled, and Astra round 2 is reviewing it. This is a read of the queue, not proof of installation or the latest review disposition. The older phase-1 v5 is used below for unchanged evidence/interface/role contracts; its old same-host provisioning and science-reservation mechanics are not assumed to govern Intel. (Q:31–66; H:239–247)

**F1 contribution is indirect.** The north star asks whether the in-weight LLM-as-Database contract is implementable. External retrieval for the research team can help assess that question. It cannot replace the contract or count as proof that the product stores, edits or retrieves facts correctly inside weights. None of the options below closes an F1 condition merely by organizing or finding evidence. (F:7–20)

## What the approved design already provides

This is the comparison baseline, not a claim that all planned features are operational:

- Git-owned findings, program state, decisions, preregistrations and review receipts retain authority. Reviewed structured links also belong in Git. DuckDB and Neo4j are disposable analysis copies, and runtime state/locks remain with existing managers. (D:108–121)
- Neo4j already represents claims, hypotheses, runs, findings, decisions, papers and tasks. The vocabulary already includes evidence, derivation, qualification, supersession and work dependencies. A pair of database views shares a manifest naming source revisions, hashes, coverage and reviewed links. (D:110–142)
- Traceable metrics retain definitions, denominators, scope and run identity. Link review state, execution state, scientific outcome, evidence tier and source currency remain separate. A checked support path is not a transitive scientific proof. (D:134–142; V:102–122)
- The research loop already asks for relevant evidence, limitations, previous attempts, counterarguments, separate skeptical review and a cheap disconfirming test. Tasks already carry exact inputs, authorized scope, prerequisites, checkpoints and handoffs. (D:146–163,175–185)
- Similarity search and graph analysis are already optional enhancements. Text search is the baseline. Whole-program coverage, shared human/agent workflow and discovery adapters belong to later phases. Renaming these planned capabilities does not add a feature. (D:95–106,199–207,227–245)

Phase 1 is narrower: exact records, bounded chains, measurements, comparisons, history, coverage and fixed question IDs. It excludes paper/search/optimizer workflows and arbitrary queries, online fetching, model work and execution authority. An exact record/chain interface is not yet a general conversational search system. Broad retrieval should not be added to that frozen slice through this brainstorm. (V:98–122,157–185)

## Concrete problems worth testing against

| Problem | Cited record | What an addition would have to improve |
|---|---|---|
| Corrected conclusions spread through copied trackers. | A saved lesson describes a retracted gap reused in about eight trackers; it also describes the k≤2 to k≤1 drift. The existing cure is de-duplication and registered currency checks. (AR:8–17; F:48–50) | Locate affected references or missing reviewed dependencies beyond what existing pointers/checks already catch. It must not generate more copied verdicts. |
| A completion label can hide a failed scientific or mathematical gate. | The MathLab addendum distinguishes step-2 PASS and stage completion from terminal calibration FAIL, and shelves step 4. (ML:91,124–132) | Return the terminal outcome, prerequisite failure, tier and stop consequence together. It must preserve the separately gated NEW-1 distinction. |
| An interim answer can become stale; a final answer can still be qualified. | C10W's interim entry forbids final routing before replication; its final entry remains qualified, supplies no gate-clean reference and claims no write-engine route. (W0:7–11; W1:7–16,48–56) | Select the proper version and keep its caveats. “Final” or “closed” must not become “the research goal passed.” |
| A number can be interpreted backwards. | The saved remaining-residual lesson records a reversed interpretation that affected later research rationale. (RR:8–12) | Retrieve the definition, scope and correction with the number. Finding the same digits is insufficient. |
| Reading consumes the context needed for doing the work. | MB23 went from 100% to 64% context before its first edit. This is one documented case, not an average. (TB:7–11) | Reduce unnecessary reading while retaining current rules, stop conditions and counterevidence. |
| Generated “new” questions may already be known. | The saved InfraNodus trial classified all three generated questions as already known; underlying reading sharpened one testable lead. (IN:3,7–19) | Improve a test or find a locally nonduplicative lead. Question count and impressive summaries are poor substitutes. |

These are historical examples and test candidates. They do not establish today's error rates, typical reading cost, search quality or likely savings.

## DAG: where acyclic relationships help, and where they do not

**General knowledge (G1–G3 in sources.md):** a DAG is a directed graph without directed cycles. It can express ancestry and prerequisite order. Git commit ancestry is already a DAG. Neo4j holds general graphs; using Neo4j does not automatically make selected relationships acyclic. Scientific lineage is not the same relation as commit ancestry.

**Judgment:** use acyclicity as a rule for particular relationships, if a missing check is demonstrated. A new DAG database offers little justified incremental value when the selected connection copy is already Neo4j. (Baseline: D:108–142)

| Concrete application | What it could contribute here | Existing coverage and limits |
|---|---|---|
| Experiment/data lineage | Follow a result to its run, admitted input versions, metric definition and calculation operands; identify what must be reconsidered after an input correction. | This is already required provenance. Only a missing checked relation or impact query is incremental. Missing lineage must remain missing. (D:125–142; V:116–122) |
| Claim → evidence chains | Find supporting, refuting and qualifying evidence for a scoped claim. | Central to the existing graph and phase-1 chains. Support links do not compose into automatic proof; mutually qualifying claims need not be acyclic. (D:125–142,233; V:116–122,165) |
| Hypothesis dependencies | Separate an assumption, a prerequisite test, a competing explanation and a merely related topic. Detect an impossible prerequisite loop. | Proposal cards already include dependencies; typed links already exist. A new constraint might help only on a reviewed prerequisite subset. Related hypotheses can legitimately refer back to each other. (D:125–142,154–163) |
| Build/run pipeline | Describe which reviewed artifact must precede another; expose a missing freeze or review before a proposed next action. | Existing roles/managers own execution, locks and approvals. An ordering picture cannot enforce readiness, admission or cancellation. A second scheduler would duplicate that authority. (V:71–80,174–185; D:177–185) |
| Decision ledger | Show a decision's source version, scoped replacement and the history of a reopened route. | Supersession and history are already planned. Commit time alone cannot identify which scientific scope changed. Preserve old decisions rather than overwriting them. (D:101,117–140; V:120,168) |
| Correction impact | Show reviewed claims/decisions that directly or indirectly use a changed source, with uncertainty where links are incomplete. | This addresses the copied-tracker pain, but fingerprints/de-duplication already catch registered references. Evaluate additional coverage, not a second correction ledger. (AR:10–17; F:48–50; D:140–142) |
| F1 prerequisite/coverage view | Point from a spec obligation to admitted findings and unmet prerequisite evidence. | Phase 2 already includes coverage of spec layers/F1 obligations. A missing imported edge does not prove an experiment was never done. (D:140–142,234) |
| Reproducible analysis dependencies | Describe operands → derived measurement → interpretation, and what is stale after an operand changes. | Calculation recipes and immutable source identities are already required. Recalculation is an execution action, not something a graph link authorizes. (D:117–121,136,181,191–197) |

**Judgment on structure:** if retained, acyclicity should apply to explicitly ordered, versioned relations such as calculation prerequisites or validated supersession. Citation, alternative-to, related-to, feedback and refutation relations can contain valid cycles. Do not force the entire research graph into a DAG. For a prerequisite cycle, report a reviewed-link problem; do not break the loop silently or infer which task should run.

**Value and limits:** the strongest candidate is a correction-impact or missing-prerequisite check tied to the tracker-drift example. It could help F1 by exposing a conclusion resting on stale or unavailable evidence. It does not discover causal mechanisms from graph paths. If the approved chain/history/coverage operations already answer those questions correctly and quickly, DAG adds only a name. (AR:10–17; F:48–50; V:165–169)

**Recommendation for this idea:** retain only the question of whether a typed prerequisite/impact check earns a place inside the existing reviewed links and graph copy. Pilot P1 must show incremental value. Reject a separate DAG store, global acyclicity requirement or replacement scheduler.

## RAG: evidence finding for agents and the operator

**General knowledge (G4–G6):** in broad usage, RAG means retrieving material and giving it to a model to help write an answer. Exact IDs, keyword search, database results and graph neighborhoods can supply material; embeddings are optional. Retrieval can return a relevant but outdated or misinterpreted passage.

The original RAG paper combines model memory with retrieved external memory. Its abstract reports NLP benchmark benefits; it does not test this research engine or its F1 contract. This evaluation borrows the retrieval-before-answering idea, not its training recipe. [Lewis et al., abstract](https://arxiv.org/abs/2005.11401)

| Material or use | Concrete use here | Boundary and existing coverage |
|---|---|---|
| CORPUS for agents | Find a finding together with its correction, tier, scope, caveats and superseding entry before proposing a test. | Evidence retrieval/history is already planned. Test failures to retrieve the MathLab stop or qualified C10W final reading. (D:134–146; ML:124–132; W0:7–11; W1:7–16,48–56) |
| Papers/prior art for agents | Find a possible mechanism, control or method relevant to a named local gap; compare what the paper claims with what local evidence actually shows. | Local research first and primary-source verification already required. Abstract-only coverage can suggest a lead, not validate a detailed method or transfer. (D:199–207; F:35–42) |
| Results/measurements | Answer “what was measured, under what definition, on which run?” and trace a derived number. | DuckDB/measurement adapters already supply admitted typed facts. Arbitrary JSON, logs and tensors are not interchangeable search chunks. Unknown denominator or scope must remain unknown. (D:112,136–138; V:116–122,166–169) |
| Memory/lessons | Bring applicable traps and operating constraints to an agent's task. | Use lessons as routing aids, then check governing sources. The residual-definition and reading-budget lessons illustrate why. Memory cannot override a current amendment or finding. (F:23–50; RR:8–12; TB:7–11) |
| Operator questions | Give a short plain answer, exact source locations, the source date and what is unknown; allow inspection of the original passages. | Shared human/agent operations and conversation are already selected. Intel answers may use a dated local source generation and must reveal age/coverage. (D:175–179; H:232–234) |
| Contradiction/counterevidence search | Retrieve the best apparent counterexample as well as support; distinguish true disagreement from incompatible scopes. | Scoped comparison, qualification and suspected-contradiction handling already belong to the design. Text similarity is not evidential compatibility. (D:134–142,146–163) |
| “What should we test next?” | Gather prior attempts, constraints and competing explanations before drafting an informative test. | Proposal development already requires this. Retrieved arguments suggest a candidate; current queue and approvals remain elsewhere. (D:146–163,177–185; IN:7–19) |
| Whole-program briefing | Assemble an answer about unresolved obligations across several findings instead of searching for one phrase. | Full inventory/coverage and briefings are already phases 2–3. A partial index cannot support an unqualified “whole program” answer. (D:140–142,234–235) |

**Judgment on the first useful form:** exact-ID and keyword retrieval, enriched by checked connections, is the sensible baseline. Fetch original passages with their mandatory correction/qualification, rather than treating a generated summary as accepted evidence. Use the existing paired source generation, record identities and currency/coverage fields. This is an extension of the selected service when permitted, not another facts database. (D:117–142,207; V:102–122,157–172)

The empirical target is **correct evidence selection**, not more fluent prose. In the MathLab case, an earlier PASS alone omits the failed prerequisite. In C10W, a final record alone still needs its locality and routing limits. In the residual example, a number alone omits its definition. These failures would be material to research decisions even if the wording were polished. (ML:91,124–132; W1:7–16,48–56; RR:8–12)

**Semantic retrieval:** it could help when a question uses different words for a known source. That is a plausible benefit, not a measured local failure. It adds index preparation, model/version provenance, update work and resource use. Intel's model ban rules out local model-based embeddings there. M3 model work could contend with science; hosted processing carries its own cost/export scope. Retain this only as a later conditional comparison if the non-model baseline repeatedly misses admitted evidence for vocabulary reasons. (G4–G7; H:226–237; D:181–185,203,207)

**Graph-guided retrieval versus Microsoft GraphRAG:** walking this engine's reviewed Neo4j links is compatible with the selected baseline. The GraphRAG abstract instead describes model-extracted entities and generated community summaries for broad corpus questions. Its reported gains concern comprehensiveness/diversity on its global-summary datasets. That supports considering a future briefing experiment; it does not show local scientific correctness, useful novelty or better F1 decisions. [Edge et al., abstract](https://arxiv.org/abs/2404.16130)

**Judgment:** a separate extracted graph of “accepted” facts would duplicate the checked connection authority and violate the selected contract. A strictly provisional theme index is conceptually possible, but it would add extraction, summary refresh, model work and review without a demonstrated gap here. The saved discovery trial's known-question result is a reason to demand incremental usefulness rather than adopt such a layer now. (D:108–142,199–207; IN:7–19)

**Recommendation for this idea:** test ordinary source retrieval against the evidence-packet baseline in P2. Keep embeddings conditional on P5's entry condition. Do not recommend a second GraphRAG truth graph, unattended generation of scientific verdicts or a model added to Intel.

## ICM: scoped context and staged research

The local skill names the method **Interpreted Context Methodology**. This report treats the operator's “Interpretable Context Methodology” as that supplied method, rather than assuming a different interpretability technique. The skill describes numbered stages, markdown Inputs/Process/Outputs contracts, stable references separated from working artifacts, selective reading, and one agent replacing framework orchestration. (I:19–24,55–69; IC:14–62)

| Concrete use | Potential gain | Existing coverage or needed limit |
|---|---|---|
| Task entry and scoped reading | Explain the question, exact source versions/sections and why each is needed, before the agent reads broadly. | Existing task records already require exact inputs and scope. The incremental question is whether better routing reduces the documented reading loss. (D:177–185; TB:7–11; IC:14–47,53–62) |
| Stable rules versus current task material | Make it clear which text governs the work and which text is evidence to examine. | A useful convention. Stable does not mean immutable: current amendments still govern. ICM's own small-root-file budgets expressly exclude this repo's governance files. (I:31–53,55–69) |
| Paper → local relevance → possible test | Keep a paper's claim, local applicability, differences and test prediction inspectable. | Existing proposal cards already require these distinctions. An additional folder hierarchy is unnecessary unless it measurably improves the work. (D:146–163; IC:53–62,105–121) |
| Proposal → skeptical review | Give a reviewer specific assumptions and counterarguments to inspect without another broad reading pass. | Independence remains separate: one agent cannot substitute for independent expected-answer author, builder and binding reviewer roles. (D:150–163; V:71–80; I:19–24) |
| Analysis → staged writeup | Carry source identities, calculations, caveats and unresolved checks into a draft. | A draft artifact is not a promoted finding. The phase contract distinguishes engineering delivery, review and canonical closeout. (D:136–138,191–197; V:71–80) |
| Fresh-agent continuation | Carry what is done, what remains, exact next action, stop conditions and current authorization into a successor session. | Already in the task/handoff contract. Test the quality of the handoff, not whether it uses the ICM name. (D:177–185; TB:7–11) |
| Operator steering at a meaningful stage | Make a real choice or checkpoint visible while avoiding repeated permission requests for already-covered work. | Operator steering and reuse of valid authorization already belong to the design. Numbered folders confer no permission. (D:183–187; IC:105–121) |

**Judgment on conflicts:** adopt useful reading conventions only if they improve the existing task contract. Do not install an ICM workspace, reorganize the repository or replace MAESTRO.

The local ICM status rule declares a stage COMPLETE when its output folder contains a file. That may describe artifact presence; it is incompatible with using COMPLETE to mean scientific acceptance or reviewed closeout here. The independent phase roles and currency-active closeout must remain intact. (I:146–147; IC:136–139; V:71–80)

The ICM convention allows a human to edit a previous stage's output before the next stage reads it. That is useful for ordinary drafts. It cannot silently revise frozen inputs or a reviewed expected-answer packet: the phase contract requires a new version, reasons/diff and renewed review. (IC:58–62; V:73–76)

Selective reading must preserve the governing rules, current amendment, relevant opposing evidence and stop condition. The documented reading loss justifies trying better selection; it does not justify shaving rules indiscriminately. A long-context paper reports position sensitivity in the tasks/models it studied, which motivates measuring context use but establishes no defect in today's agents. (TB:7–11; I:37–53) [Liu et al., abstract](https://arxiv.org/abs/2307.03172)

**Recommendation for this idea:** evaluate ICM-inspired reading/handoff contracts inside existing task records in P3. Keep separate agents/reviewers and existing outcome/authority fields. Adopting the whole filesystem-driven orchestration method is not justified.

## Comparative scores

**Judgment; not calibrated or measured.** Value scores concern help with making an F1 determination and daily research, not proof of the product's in-weight contract. Value/deferral fit: 1 = little, 5 = strong. Build/run burden and authority/science risk: 1 = low, 5 = high. Risks describe the option as stated; preserving source ownership lowers them. Scores are not added into an “objective winner.”

| Option | F1 support | Daily value | Build / run burden | Authority / science risk | Fit after other builds | Named pain and disposition |
|---|---:|---:|---:|---:|---:|---|
| Approved foundation + compact evidence packet | 4 | 4 | 1 / 1 | 1 / 1 | 5 | Correction/tier/caveat errors and reading waste. First comparison baseline; P0. (ML:124–132; RR:8–12; TB:7–11) |
| Typed prerequisite/impact checks in the existing graph | 3 | 3 | 2 / 1 | 2 / 1 | 5 | Tracker correction fan-out and missing prerequisites. Retain only if P1 beats existing trace/history/coverage. (AR:10–17; V:165–169) |
| Separate DAG store or global DAG rewrite | 1 | 1 | 4 / 3 | 4 / 3 | 2 | No uncovered pain justifying another store; overlaps the selected graph/provenance. Reject. (D:108–142) |
| New DAG execution scheduler | 1 | 2 | 5 / 3 | 5 / 5 | 1 | Ordering alone does not address the existing resource/authority contract. Reject. (D:177–185; V:174–185) |
| Exact/keyword + checked-link retrieval for evidence answers | 4 | 4 | 2 / 1 | 2 / 1 | 5 | Stale/interim records, missing caveats and definitions. Conditional addition; P2. (ML:124–132; W0:7–11; W1:48–56; RR:8–12) |
| Dense semantic retrieval as a later supplement | 2 | 3 | 3 / 3 | 2 / 3 | 4 | Vocabulary mismatch is plausible but not measured; local model embeddings cannot run on Intel. P5 only after demonstrated misses. (H:226; D:207; G4–G7) |
| Extracted GraphRAG graph + community summaries | 2 | 2 | 4 / 4 | 4 / 3 | 4 | Could aid broad briefings, but novelty/value is unproven and checked connections already exist. Do not adopt now. (D:199–207; IN:7–19; Edge abstract) |
| ICM-inspired reading and handoff contracts | 3 | 4 | 1 / 1 | 2 / 1 | 5 | The recorded pre-edit context loss. Conditional adaptation; P3. (TB:7–11; D:177–185) |
| Full ICM orchestration/status replacement | 1 | 2 | 3 / 1 | 4 / 4 | 2 | Repeats task contracts and weakens independent review/completion meaning. Reject. (I:19–24,146–147; V:71–80) |
| Retained checks + retrieval + scoped context together | 4 | 4 | 3 / 2 | 3 / 2 | 5 | Could address the same pains together; each layer adds upkeep. P4 must beat the best simpler option. (AR:10–17; ML:124–132; TB:7–11) |

### Estimated effort and hardware cost

These are rough planning judgments for a bounded text-only evaluation slice of at most 200 documents, 20 MiB of admitted text and 80 reviewed records/200 links. They exclude the already-authorized foundation, full-program importing and scientific compute. One person-day means roughly one working day including documentation/review. These ranges are not quotes, host measurements or a build plan.

| Option | Incremental effort estimate if later justified | Running/storage implication |
|---|---|---|
| Evidence packet using existing answers | 0–1 person-day to standardize presentation/evaluate; potentially zero new software | Source excerpts and pointers; no model index. Preparation and refreshing packets are real recurring labor. |
| Typed dependency/impact checks | 1–3 person-days, plus any missing-link review | Small graph traversals/checks on the bounded slice. Full-corpus impact queries may cost more; no automatic rerun. |
| Exact/keyword evidence retrieval | 2–5 person-days, excluding importer work | Text index/lookup and checked-link expansion on Intel; response generation uses the existing authorized agent path. Source refresh/coverage upkeep remains. |
| ICM-inspired task presentation | 0.5–2 person-days | Markdown/task presentation; no database or resident model added. Contract preparation and source-staleness checks still count. |
| Dense semantic supplement | 3–10 person-days | Embedding preparation/query compatibility, storage and re-indexing. Model-based local embedding work belongs on M3, not Intel; no measured RAM/time/throughput estimate is available. |
| Extracted GraphRAG/global summaries | 1–3 person-weeks or more | Extraction/summarization model calls, generated artifacts and review/refresh. The cost grows with the collection; no local fit or service-cost claim is supported. |
| New DAG store/scheduler or full ICM replacement | 1–3 person-weeks or more | Migration, consistency and ownership work dominate. A low-memory text layout does not make the governance migration cheap. |
| Combination of retained narrow additions | Roughly the component effort; avoid treating it as one new platform | Shared source capture may reduce duplicate work, but combined retrieval/context and upkeep must be measured separately. |

The published Intel starting limits include a 5 GB pilot-data allowance, Neo4j ≤2 GB RSS, engine aggregate ≤3 GB and one active builder test job. The hardware design's old ≤1 GB setup line is superseded in the queue notes by 2 GB; aggregate support-memory targets in that design were still proposed commissioning limits. Do not convert any of these written limits into a claim that host capacity has been verified. (H:237–247; Q:64–65)

For these proposed small pilots, target no more than 256 MiB additional working memory and 100 MiB additional disk while preserving the applicable engine limit. This is a proposed ceiling, not proof of fit. Intel-local work can use dated immutable copies; touching M3/memit remains separately coordinated. No new model job, download, corpus export, cloud GPU or database provision is needed for the manual first comparisons. A later automated/model variant requires its actual workload to be covered; this document grants no execution scope. (H:226–247; D:181–185)

## Combinations and the simpler alternative

**Judgment:** the simplest candidate is a compact evidence packet produced from the approved foundation. It states the question, original source identities/locations, current and historical scope, essential counterevidence/caveats, missing coverage and the next permissible action. Its contents are already largely required by the evidence/proposal/task contracts. It is a presentation of existing authority, not a new maintained verdict ledger. (D:117–163,177–185)

| Combination | Potential benefit | How it can fail; comparison to use |
|---|---|---|
| DAG checks + retrieval | A changed source or blocked prerequisite selects the sources that need inspection. | A false/missing dependency can hide material evidence. Compare against checked trace/history plus ordinary search; keep uncertainty explicit. |
| Retrieval + ICM-style routing | An agent receives the right evidence and knows the bounded question to answer. | Compression can omit the correction or freeze rule. Compare against the same evidence packet with an ordinary task brief. |
| DAG checks + ICM-style routing | A successor sees prerequisites, exact inputs and what still awaits review. | A neat pipeline can make blocked/unreviewed work look ready. Compare against existing task/handoff fields. |
| All three narrow adaptations | Dependency scope, original evidence and task instructions serve different purposes. | Shared errors and upkeep can grow together. P4 compares with the best single adaptation, not an artificially weak empty-context baseline. |
| Semantic search + global summaries | Could help unfamiliar terminology and broad thematic questions. | Adds model preparation and lossy generated intermediates before a missing capability has been shown. Test vocabulary/coverage failures first; no current adoption recommendation. |

These are mechanisms to investigate, not completed behavior. None authorizes a run, updates program_state, promotes a claim or turns a proposal into evidence. That remains the approved ownership contract. (D:108–121,177–185; V:174–185)

A different approach may beat all of them: improve the questions and checked source inventory, use existing exact queries/text search, and standardize only the answer/handoff presentation. If those changes already make answers correct and economical, do not add a DAG, RAG or ICM “integration” project. The saved drift lesson warns that an infrastructure arc consumed about 15 turns while displacing science; that is a concrete reason to cap further process work. (AR:15–17; D:234–245)

## Recommendation

**Keep the approved foundation. Recommend bounded evaluations after the other builds, rather than adopting three frameworks.**

1. Use the compact evidence packet as the first baseline and test it with P0. Even it must earn any extra maintenance beyond the already-required source-linked answers.
2. Consider a typed dependency/impact check only if P1 exposes a missing capability beyond existing graph queries and currency checks.
3. Consider exact/keyword evidence retrieval only if P2 improves source selection or reduces answer-preparation cost over that baseline.
4. Consider ICM-inspired reading/handoff presentation only if P3 reduces reading/recovery cost with every material rule preserved.
5. Retain a combination only if P4 demonstrates further benefit over the best simpler option. Semantic retrieval remains conditional on P5's documented vocabulary failures.

Do not recommend a new DAG database/scheduler, a second GraphRAG accepted-fact graph, Intel model embeddings, full ICM orchestration, or changes to the science path. These choices follow the overlap, role and hardware constraints above. (D:108–142,177–185,207; V:71–80,174–185; H:226–247; I:19–24,146–147)

The recommendation would change if a frozen comparison showed the approved baseline repeatedly fails an important class of question and a bounded addition corrects it without new authority, omitted caveats or material interference. A more elaborate system is not valuable merely because it makes the same answers look organized.

## Cheap falsifiable pilots — proposed, not authorized or run

These are evaluation protocols, not implementation tasks. A manual comparison on frozen source copies can establish usefulness of selected information/presentation; it cannot establish production query speed, native resource fit, scheduler safety or scientific improvement.

**Common rules:** after the other builds are complete, a person/session independent of the candidate author selects questions, freezes source versions and writes expected evidence/answers before seeing candidate output. Use the commissioned approved foundation as baseline where available; if it is unavailable, report that limitation rather than simulate an operational pass. No science runs, tensor decoding or canonical edits. Fix all cases, thresholds and resource ceilings before evaluation; a repair/rerun is a new version, not replacement of a failed receipt. Expected answers come from originals, not the candidate's summaries or database output. This preserves the existing independent-key and outcome-tier contracts. (V:71–80,102–122; D:229–245)

For scored answers, a **critical error** is any wrong source version, outcome/tier, scope, metric meaning, missing stop condition, unwarranted complete/known/unknown claim, or action outside the task's authority. Exact cited passages must support the answer. Missing evidence must be stated; refusing an answer whose required evidence is admitted and available is also an error. A “fully correct” answer also includes all noncritical facts required by the independent key. Measure critical correctness separately from retrieval recall, readability and time.

Pilot size/resource ceilings are proposals: at most one person-day of preparation/evaluation per pilot; bounded text/graph slice as above; no additional paid service or local model needed for P0–P4. Include preparation, review and refresh time in the cost record. If the proposed information can be assessed manually, do that before contemplating engineering work. Failing to fit the ceiling is a failed cheap pilot, not permission to expand it.

### P0 — Does a compact evidence packet beat ordinary reading?

- **Cases/baseline:** 24 questions: six current-versus-historical outcomes, six tiers/limits, four metric definitions, four prerequisites and four missing/out-of-coverage cases. Include MathLab, C10W and the residual correction; the independent key supplies the other cases. Compare existing exact queries/text reading plus an ordinary brief against a packet drawn from the same admitted sources. (Candidate examples: ML:91,124–132; W0:7–11; W1:7–16,48–56; RR:8–12)
- **Measure:** critical correctness, all-required-fact accuracy, citation support, time to an acceptable answer, and packet preparation/refresh cost. Evaluate agent answers and human plain-language reading separately. Use matched case variants and fresh answer contexts; do not let a respondent learn the key in an earlier condition.
- **Pass bar:** zero critical errors in all 24; every factual citation supports its claim; at least 22/24 fully correct; median answer time at least 25% lower than baseline. Counting preparation/refresh, the saving must repay the extra work within 20 comparable uses. The independent reader can locate the original evidence from every packet.
- **Drop:** any critical error or unsupported citation fails. Also drop a separately maintained packet layer if it misses the speed/cost bar; keep the source-linked answers already required by the approved design. A pass establishes bounded usability only.

### P1 — Do typed dependency checks add anything to the existing graph?

- **Cases/baseline:** 12 frozen scenarios over ≤80 records/200 reviewed links: four correction-impact cases, four prerequisite cases and four boundary cases. Boundaries include two valid general-graph cycles, an invalid true-prerequisite cycle, and incomplete/ambiguous dependencies. Compare with existing trace/history/coverage and currency information. Changes are hypothetical changes in copies, never live corrections. (Baseline: D:134–142; V:165–169; historical pain: AR:10–17)
- **Measure:** exact affected-source sets, correct ready/blocked/unknown interpretation, invalid-cycle detection, false alarms on valid cycles, and time to the checked answer. “Unknown” is correct when coverage is missing; a picture cannot certify the absence of additional dependents.
- **Pass bar:** 12/12 match the independent answers; both valid cycles remain allowed; the invalid prerequisite cycle is identified; missing coverage is explicit. It must either correct at least three baseline scenario errors or cut median answering time by at least 30% at equal perfect accuracy.
- **Drop:** any wrong ready/complete interpretation, unsupported dependency, rejected valid cycle or hidden coverage gap fails. If existing queries already do the job and the time bar is missed, retain the existing graph without an extra DAG feature. If reviewed links cannot be assembled within the pilot budget, record the coverage problem and drop this pilot's feature claim.

### P2 — Does source retrieval improve evidence selection?

- **Cases/baseline:** P0's frozen 24 cases, each in its original wording and one independently frozen rewording (48 questions total). Compare ordinary exact/keyword lookup and manual packet preparation with keyword retrieval expanded through existing checked links. All conditions use the same agent model/settings if an already-authorized agent is used. No dense model or community summaries. A returned evidence bundle includes mandatory corrections/qualifiers, not a lone convenient passage.
- **Measure:** recall of required original spans within at most eight returned bundles, critical evidence omission, final-answer correctness, elapsed preparation/answer time, and preparation/index-refresh cost. Measure current/historical and out-of-coverage behavior separately. Do not reward more text.
- **Pass bar:** every critical correction, tier, definition and stop span is returned or its absence correctly refused; required-span recall ≥95%; zero critical answer errors/unsupported citations; ≥44/48 fully correct, including ≥22/24 in each wording set. Median preparation-plus-answer time must be ≥25% lower than the best accurate P0-style baseline on these same questions, with added preparation/refresh repaid within 20 uses.
- **Drop:** any critical omission or answer promotion fails. Also drop the extra retrieval layer if it misses the benefit/cost bar. Correct “not indexed” answers are not evidence of successful semantic finding. A manual pass does not establish automated service latency; that needs later testing on the actual path.

### P3 — Does scoped context improve successor recovery?

- **Cases/baseline:** ten document-only successor tasks, two each involving an unfinished handoff, a newer amendment, a failed prerequisite, an output awaiting review and a measurement with a correction. The independent key states the next permissible action and all mandatory constraints. Compare the ordinary existing brief plus the same evidence packet with an ICM-inspired Inputs/Process/Outputs reading contract. Both conditions can access the same originals. (Motivation: TB:7–11; safeguards: V:71–80; I:146–147)
- **Measure:** correctness of next action, source/version/authority constraints recalled, words or directly recorded tokens read before that answer, recovery time, and contract preparation time. Record actual context-use observations only if available; words read are a cost proxy, not a measured percentage of an agent's context.
- **Pass bar:** all ten next actions and every material constraint are correct; output existence never becomes review/scientific completion. In at least eight tasks, reading before the answer is ≤75% of baseline; median recovery time improves ≥25%; preparation is repaid within 20 handoffs. Both conditions retain the binding context stop rule.
- **Drop:** any omitted amendment, caveat, prerequisite, scope or stop rule fails. Drop the new wrapper if existing briefs perform equally well or its preparation erases the gain. A prettier folder layout is not a pass.

### P4 — Does a combination beat the best single addition?

- **Entry:** only components that separately pass P0–P3 are eligible. This is a conditional recommendation, not a reason to build all three.
- **Cases/baseline:** 12 new, independently frozen matched tasks from the same problem classes; compare the best accurate simple condition with adding the other retained components. Keep sources, agent settings, answer limits and scoring fixed.
- **Measure/pass bar:** 12/12 critical requirements correct, no unsupported claims/actions, no loss of mandatory evidence, and median end-to-end time ≥15% better than the best simpler condition. All combined preparation/refresh must repay within 20 uses. No separate verdict/state store may be needed to obtain the gain.
- **Drop:** any critical regression or missed incremental gain rejects the combination; keep only the simpler passing component. No clean small comparison supports a whole-program benefit claim.

### P5 — Conditional semantic retrieval: is vocabulary mismatch a real gap?

- **Entry:** P2 must first document at least four distinct question cases where required evidence was admitted and available, but ordinary retrieval failed because of wording. Missing imports, stale sources, unclear questions or absent evidence do not qualify.
- **Cases/baseline:** freeze ten fresh vocabulary-variant queries plus ten previously correct/boundary queries. Compare the best ordinary retrieval with a semantic supplement using the same accepted sources. It cannot change link review state or write canonical facts.
- **Measure/pass bar:** the fresh wording variants must resolve at least three of the four independently demonstrated miss cases; return every critical qualifier; zero critical regressions or unsupported citations on the ten controls; overall final-answer accuracy cannot fall. Median end-to-end time, including preparation amortized over 20 uses, must improve ≥15%.
- **Resources/drop:** no Intel local model embeddings. A later comparison would use only separately covered M3 or hosted resources after the other work, without cloud GPU or displacing pending science. Freeze its actual cost/memory/runtime ceiling before evaluation; none is measured here. Drop it if no qualifying misses exist, if it cannot fit an approved bounded workload, or if cost/accuracy/critical-evidence conditions fail. A hypothetical model advantage is insufficient. (H:226–247; D:181–185,207)

GraphRAG extraction/community summaries and full ICM/DAG replacements are not recommended, so no adoption pilot is proposed for them. Reconsideration requires a new named gap, a cheaper-baseline comparison and prospective failure criteria; it cannot use these small pilots as their acceptance.

## When and where it would integrate

These are evaluation destinations within the approved phases, not a new build sequence or an amendment to a frozen brief. The operator's deferral controls timing.

| Retained question | Existing integration location if its pilot passes | Timing boundary |
|---|---|---|
| Missing lineage/prerequisite/impact check | Reviewed Git links, vocabulary validation and existing Neo4j chain/coverage view | Revisit with phase-2 inventory after other builds. No new source or scheduler. (D:110–142,234) |
| Better evidence finding/answers | Shared research service over the paired generation; human and agent answer presentation | Revisit in phase-3 workflow after commissioned inventory. Broad search remains outside frozen phase 1. (D:117–142,175–179,235; V:98–122,157–172) |
| Scoped reading and handoffs | Existing work-item inputs/checkpoint/handoff presentation | Revisit in phase-3 acceptance, with current review roles intact. No repository restructuring. (D:177–185,235; V:71–80) |
| Semantic discovery supplement | Existing optional discovery/search adapter; same sources and reviewed-link rules | Phase 4 only, after demonstrated baseline misses and covered resources. (D:203–207,236,242–243; H:226–247) |
| Passing combination | Same locations and managers; no extra authority | Only after separate and incremental comparisons pass. (D:108–121,177–185,227–245) |

If a baseline comparison finds an already-approved capability missing or a correctness defect, report it to that build's owner. Do not expand this brainstorm into a competing fix or accelerate optional work into a frozen phase. An improvement in source presentation does not amend a scientific preregistration.

## Open questions for the operator

These are preferences or method identification, not blockers to this report:

1. When the other builds finish, is the first priority faster answers about what is actually known, or less reading and easier handoffs for agents? My default is answer correctness/currency first, then reading cost.
2. Does the local “Interpreted Context Methodology” match what you meant by ICM? This evaluation uses that exact local method. A different named method would need its own assessment.
3. For a later small test, is a 25% time saving with no material errors worth keeping an extra layer? That is a proposed usefulness bar, not an agreed target; the simpler existing workflow remains the default if the benefit is marginal.

No decision about database ownership, Intel model work or current launch permission is reopened here; those boundaries already exist in the cited design/contracts. (D:108–121,177–185; H:226–247; V:174–185)

## BRD2 completion context

**Done:** full application/overlap analysis, explicit comparison scores and unmeasured cost estimates, conditional recommendation, six falsifiable pilot protocols, integration timing and optional operator questions. sources.md identifies relied-on originals, general knowledge, abstract-only outside evidence and snapshot limits. BRD's handoff is preserved verbatim below as historical context, not the final recommendation.

**Still unverified:** all pilot outcomes; real savings/search accuracy; native host resource fit; completeness of imported dependencies; current install/promote status beyond the queue snapshot; scientific benefit. Nothing here authorizes implementation or execution.

**Next single step for MAESTRO:** read the operator summary and pilot/drop conditions, retain this evaluation, and revisit only after the other builds. Any later build requires its own named scope and reviewed acceptance; this report does not supply that build plan.

**Work scope:** only the requested brainstorm.md continuation and new sources.md in results/research_engine_dag_rag_icm_brainstorm_20261011T095840Z/. BRD2 used bounded reads/source hashes and paper abstracts. No graft, tmux, experiments, commits, installs, package/repository downloads, new services or edits to unrelated files. Shared-checkout changes were preserved. Detailed observation/hashes are recorded in sources.md.

**Reflection for a successor:** the strongest question is whether a correction and its consequence reach the answer, not whether the system has a new graph/search/context label. Existing source-linked answers and scoped briefs must be the comparison baseline. This lesson is saved here; no global or repository memory was edited.

**Binding context rule:** watch your own and every team/successor session's context. Start a new step only with at least 60% left. At 40% or less, or on any context compaction, stop starting work, append a BRD2 HANDOFF with done, remaining, exact paths, the next single step and this rule, then reply BRD2 HANDOFF. Preserve the rule through every handoff. MAESTRO's explicit stop instruction overrides numeric thresholds.

## Preserved BRD handoff — historical

The following is BRD's exact saved handoff. Its “remaining work,” queue timestamp and provisional judgments describe the predecessor session; the completed evaluation above supersedes those draft judgments.

## BRD HANDOFF

### Why this handoff exists

MAESTRO explicitly reported that BRD was at or below 45% context and directed it to finish only the command in progress, start nothing new, create the output folder, write this partial brainstorm with a handoff, and reply BRD HANDOFF. No command was still running when that instruction arrived. Work stopped at evidence gathering; no pilot or scoring work started afterward.

### What was read

All source reads used bounded line ranges or targeted searches; no *_exec.log file was opened. File names shortened elsewhere in this document resolve as follows:

| Short name / source | Exact path and relevant read spans |
|---|---|
| Approved design.md | results/research_engine_brainstorm_20261011T032049Z/design.md:1–155,155–303; later clean numbered reads covered 85–155 and 155–303. |
| Decisions / prior handoff | results/research_engine_brainstorm_20261011T032049Z/decisions_log.md:1–117; results/research_engine_brainstorm_20261011T032049Z/handoff.md:1–39. |
| phase1_spec_v5.md | results/research_engine_phase1_20261011/phase1_spec_v5.md:1–150,151–291; clean follow-up for 207–217. Section list also inspected. Some long command outputs were truncated; do not assume every late budget sentence was fully inspected. |
| Framework snapshot | docs/SPEC_E2E_GROUND_TRUTH.md:1–98. Snapshot date is 2026-06-21, not current program-state authority. |
| North star / authority | DISCIPLINE.md:1–100, with clean numbered read 1–58. |
| ICM definition | /Users/robertrhu/.claude/skills/icm-workspace/SKILL.md:1–159, with numbered reads 16–72,133–176. |
| ICM reference contracts | /Users/robertrhu/.claude/skills/icm-workspace/references/conventions.md:1–174; /Users/robertrhu/.claude/skills/icm-workspace/references/templates.md:1–220,222–end. No linter or workspace was run. |
| Index / historical and current qualifications | CORPUS/README.md:1–84; CORPUS/55_C10W_ORACLE_P1_INTERIM.md:1–44; CORPUS/57_C10W_ORACLE_FINAL.md:1–59; CORPUS/60_MATHLAB_HARVEST_REPLAY.md:73–137. |
| Program state / queue | docs/program_state.json:1–112 attempted, with a clean follow-up for 31–67; work_queue edited timestamp observed as 2026-10-11T09:58:52Z. Large historical string values truncated the first output. Queue rows 85–105 were visible. |
| Runbook §0.3 | EXPERIMENT_RUNBOOK.md:105–121 read cleanly; section boundaries and line shapes inspected. The whole long §0.3 was not read end-to-end. Line 119 supersedes the historical M3-host statement at 118. |
| Hardware design.md | results/compute_storage_brainstorm_20261011T054507Z/design.md:97–132,226–250,407–426, plus targeted search. No live hardware or remote-host checks. |
| Repository memory index | memory_mirror/MEMORY.md:1–76,77–144; first output had minor truncation. |
| Concrete pain records | memory_mirror/trim-builder-reading-lists.md:1–11; memory_mirror/anti-drift-enforce-not-autowrite.md:1–17; memory_mirror/corpus44-rho-is-remaining-residual.md:1–12. |
| Saved discovery trial | results/mathlab_staging/infranodus_trial/SUMMARY.md:1–19. |
| Prior-run guidance | /Users/robertrhu/.codex/memories/MEMORY.md:144–170 guided the MathLab event-authority check; current conclusions were grounded in the approved design and CORPUS rather than old test counts. Associated rollout ID: 01a11e59-9e98-7e50-a7fa-5a72edfd72ff. |
| Operating skills | /Users/robertrhu/.codex/RTK.md:1–end; brainstorming skill at /Users/robertrhu/.codex/plugins/cache/openai-curated-remote/superpowers/6.4.2/skills/brainstorming/SKILL.md:1–210. Context-save skill preamble and selected sections were read, but its outside-folder/session/telemetry/Git actions were not run. Context is saved here within BRD's write scope. |

General-knowledge subjects used: DAG/commit ancestry; general versus acyclic graphs; lineage versus causality; lexical, semantic and graph retrieval; retrieval versus generation and evidence validation; index/model/maintenance costs in principle. These must be explicitly marked as general knowledge in sources.md. No local timing, cost, memory, search-accuracy or novelty measurements were made.

Three primary-source abstract pages were opened:

- [Lewis et al., Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401), abstract: parametric and retrieved non-parametric memory. Its benchmark findings do not validate this engine.
- [Edge et al., From Local to Global: A Graph RAG Approach to Query-Focused Summarization](https://arxiv.org/abs/2404.16130), abstract: model-extracted graph, community summaries and global question evaluation. Only the abstract was inspected.
- [Liu et al., Lost in the Middle: How Language Models Use Long Contexts](https://arxiv.org/abs/2307.03172), abstract: position sensitivity in the models/tasks studied. Do not claim a measured defect in today's agents from this paper.

### Done and draft direction

The source-grounded overlap check and the specific pains above are saved. Draft findings favor small additions to the approved foundation: typed lineage/prerequisite checks, evidence retrieval with source currency/caveats, and ICM-inspired context routing. Separate DAG infrastructure, a second GraphRAG truth graph, local embeddings on Intel, and filesystem-based scientific completion are poor fits under the sources read. These are provisional judgments, not final scored recommendations.

### Remaining work

1. Complete the comparative assessment of value to F1 and daily research, build/run cost on M3 Pro 48 GB plus Intel, authority/science risks and deferral fit. Distinguish each narrow adaptation from a full new framework. No comparison scores or build-cost estimates have been completed.
2. Specify cheap, falsifiable engineering pilots for every retained recommendation: independent question/task set, baseline, measurements, pass/fail thresholds fixed in advance, resource limits and explicit drop conditions. No pilot is authorized or run; the directions above lack those required details.
3. Evaluate combinations against the simpler evidence-packet baseline, including whether semantic retrieval or global summaries earn any incremental cost. Do not assume that better organization yields novel science.
4. Finish the recommendation, integration timing/locations and genuine open operator questions. Do not reopen the selected Git/DuckDB/Neo4j foundation or the Intel model ban.
5. Create sources.md with every relied-on file:line, the general-knowledge register, primary-paper links and snapshot/currency limits. Check citations and summarize shared-worktree drift without reverting it. The initial turn did not capture source-file hash pins.
6. Verify the two requested documents against the brief. Keep the operator summary to 15 lines, preserve source-backed pains and distinguish proposed tests from completed results. No build plan, implementation code or install instructions.

### Exact paths and next single step

Current output: results/research_engine_dag_rag_icm_brainstorm_20261011T095840Z/brainstorm.md.
Still missing: results/research_engine_dag_rag_icm_brainstorm_20261011T095840Z/sources.md.

**Next single step:** a fresh successor reads this handoff and completes the comparison table from these grounded draft findings, using the existing approved design as the baseline and explicitly labelling costs/scores as estimates. It should refresh only the current Intel-host/queue authority it needs before making a current-state claim; do not repeat the broad reading pass. Then continue the remaining deliverables inside this same BRD output folder under MAESTRO's successor brief.

### Binding context rule

Watch context usage for this session and every team/successor session. Start a new step only with at least 60% context left. At 40% or less, or on any context compaction, stop starting new work, append a BRD HANDOFF section to brainstorm.md with done, remaining, exact paths, the next single step and this rule, and reply BRD HANDOFF. MAESTRO's explicit earlier stop overrides the numeric trigger. Never continue through compaction. Preserve this rule in every successor handoff.
