# Anthropic "Demystifying evals for AI agents" (equip research, 2026-10-17, Sonnet 5.5)

Source article: [1] https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents, published 2026-01-09 (authors: Mikaela Grace, Jeremy Hadfield, Rodrigo Olivares, Jiri De Jonghe). Fetched with WebFetch on 2026-10-17. Method note: WebFetch returns a small-model digest of the page, not raw HTML (a raw curl was denied by the permission system and not retried). Quotes marked [verbatim] were re-requested as exact sentences in a second fetch; quotes marked [truncated] were cut by the fetcher mid-sentence; everything else is paraphrase. Section names below are the article's own (some headings are as the fetcher reported them).

## What the article says, in its order

### Introduction
- Evals let teams ship agents with confidence and avoid "reactive loops" where fixing one failure creates another. Claim: "Evals make problems and behavioral changes visible before they affect users" [digest, not re-verified verbatim].
- Agents run many turns, call tools, change state; the autonomy that makes them useful makes them harder to evaluate.

### The structure of an evaluation
- Eval: give an AI an input, grade its output. The article's focus is automated evals run during development, without real users.
- Single-turn eval: one prompt, one response, grading logic (earlier LLMs). Multi-turn: e.g. a coding agent builds an MCP server, unit tests grade it.
- Agent evals: mistakes propagate and compound. Example: Opus 4.5 found a policy loophole in a tau2-bench flight-booking task, "failed" as written but gave the user a better outcome (a warning that a rigid grader can mark a better result as failure).
- Definitions [verbatim unless marked]:
  - Task: "A task (a.k.a problem or test case) is a single test with defined inputs and success criteria."
  - Trial: "Each attempt at a task is a trial." (Several trials are run because outputs vary.)
  - Grader: "A grader is logic that scores some aspect of the agent's performance." A task can have several graders, each with several assertions (checks).
  - Transcript: "A transcript (also called a trace or trajectory) is the complete record of a trial, including outputs, tool calls," [truncated] reasoning and intermediate results; for the Anthropic API it is the full messages array.
  - Outcome: "The outcome is the final state in the environment at the end of the trial." Flight example: the outcome is whether a reservation exists in the database, not what the agent says.
  - Evaluation harness: "An evaluation harness is the infrastructure that runs evals end-to-end." (instructions, tools, concurrency, recording, grading, aggregation).
  - Agent harness (scaffold): the system that lets a model act as an agent; evaluating "an agent" means evaluating harness and model together (examples named: Claude Code, Agent SDK).
  - Evaluation suite: "An evaluation suite is a collection of tasks designed to measure specific capabilities or behaviors."

### Why build evaluations?
- Early on, manual testing and intuition go far. Without evals "the team is 'flying blind' with no way to verify except to guess and check" [verbatim]. Teams cannot separate real regressions from noise, test hundreds of scenarios, or measure gains.
- Case notes: Claude Code started with user feedback, then added evals for concision, file edits, later over-engineering, combined with production monitoring, A/B tests, user research. Descript judges "don't break things, do what I asked, do it well", moved from manual grading to LLM graders with human calibration, runs separate quality and regression suites. Bolt built evals after wide use; in 3 months added static analysis, browser-agent app tests, LLM judges for instruction following.
- Evals can start at the beginning (encode expected behaviour) or later at scale. Benefits: faster adoption of new models; baselines and regression tests for latency, token use, cost, error rate; "Evals can also become the highest-bandwidth communication channel between product and research teams," [verbatim, trailing comma as fetched].

### How to evaluate AI agents (types of agent)
Four deployed types: coding, conversational, research, computer use. Advice: start from proven techniques, extend to your domain.

#### Types of graders for agents
- Code-based: string match (exact, regex, fuzzy), binary fail-to-pass and pass-to-pass tests, static analysis (lint, type, security), outcome verification, tool-call verification, transcript analysis. Strengths: fast, cheap, objective, reproducible, easy to debug. Weaknesses: brittle to valid variation, lacks nuance, limited for subjective tasks.
- Model-based: rubric scoring, natural-language assertions, pairwise comparison, reference-based evaluation, multi-judge consensus. Strengths: flexible, scalable, captures nuance, handles open-ended output. Weaknesses: non-deterministic, more expensive, needs calibration against human graders.
- Human: SME review, crowdsourced judgment, spot-check sampling, A/B testing, inter-annotator agreement. Strengths: gold standard, calibrates model graders. Weaknesses: expensive, slow, needs experts at scale.
- Scoring [verbatim]: "scoring can be weighted (combined grader scores must hit a threshold), binary (all graders must pass), or a hybrid."

#### Capability versus regression evals
- "Capability or 'quality' evals ask, 'What can this agent do well?'" [verbatim]. Should start at a low pass rate, "a hill to climb" (paraphrase; the phrase was not confirmed verbatim).
- "Regression evals ask, 'Does the agent still handle all the tasks it used to?'" [verbatim]. Should sit near 100%.
- "capability evals with high pass rates can 'graduate' to become a regression suite that is run continuously" [verbatim, truncated].

#### Coding agents
- Deterministic graders fit: does the code run, do tests pass. Benchmarks: SWE-bench Verified (about 40% to over 80% in one year), Terminal-Bench (end-to-end tasks).
- Grading the transcript can add code-quality heuristics; rubric graders can assess tool use and user interaction.
- Worked example (auth-bypass fix): deterministic tests, LLM rubric, static analysis (ruff, mypy, bandit), security-log state check, required tool calls; tracked turns, tool calls, tokens, latency. Note: in practice unit tests plus an LLM rubric often suffice.

#### Conversational agents
- Interaction quality is itself evaluated; success is multidimensional; a second LLM often simulates the user. Benchmarks: tau-Bench, tau2-Bench.
- Refund example: rubric (empathy, clear explanation, grounded in policy tool results), state checks (ticket resolved, refund processed), tool-call checks (identity verified, refund <= 100, confirmation sent), 10-turn limit.

#### Research agents
- Quality is context-dependent; experts disagree; ground truth shifts; long outputs have more room for error. Benchmark: BrowseComp.
- Combine groundedness (claims supported by sources), coverage (required facts present), source-quality checks; exact match for objective questions, LLMs for coherence and completeness; LLM rubrics need frequent expert calibration.

#### Computer use agents
- GUI via screenshots, clicks, keys. WebArena (URL, page state, backend state e.g. order placed), OSWorld (file system, configs, databases, UI properties).
- DOM-based interaction is fast but token-heavy; screenshots slower but token-efficient (tradeoff to measure).

#### Non-determinism: pass@k and pass^k
- "pass@k measures the likelihood that an agent gets at least one correct solution in k attempts." [verbatim] Rises with k; fits cases where one success suffices (pass@1 for coding first try).
- "pass^k measures the probability that all k trials succeed." [verbatim] Falls with k; example 75% per trial over 3 trials gives (0.75)^3 = 42% (arithmetic from the digest; 0.75^3 = 0.4219). Fits customer-facing consistency.
- At k=1 both equal per-trial success; by k=10 pass@k nears 100% and pass^k nears 0%. Choose by product need.

### Going from zero to one: a roadmap
Collect tasks:
- Step 0, start early: "In reality, 20-50 simple tasks drawn from real failures is a great start." [verbatim] Early changes have large effects so small samples work; waiting makes evals harder.
- Step 1, start with manual checks you already do: pre-release checks, common user tasks; in production use the bug tracker and support queue, prioritised by user impact.
- Step 2, unambiguous tasks with reference solutions: "A good task is one where two domain experts would independently reach the same pass/fail verdict." [verbatim] A reference solution proves solvability. Terminal-Bench audit: an unspecified script filepath caused failures not the agent's fault. "a 0% pass rate across many trials (i.e. 0% pass@100) is most often a signal of a broken task, not an incapable agent" [verbatim, truncated].
- Step 3, balanced problem sets: test where a behaviour should AND should not occur. Claude.ai web-search evals covered searching (weather) and answering from knowledge ("who founded Apple?"); balancing under- and over-triggering took many rounds. Links the class-imbalance ML course.

Design the harness and graders:
- Step 4, robust harness, stable environment: the eval agent should behave like the production agent; each trial starts clean. "in some internal evals we observed Claude gaining an unfair advantage on some tasks by examining the git history from previous trials." [verbatim] "Unnecessary shared state between runs (leftover files, cached data, resource exhaustion) can cause correlated failures" [verbatim, truncated]; shared CPU/memory limits make trials "not independent because they're affected by the same factor" [truncated].
- Step 5, design graders thoughtfully:
  - Deterministic where possible, LLM where needed, human to validate.
  - "it's often better to grade what the agent produced, not the path it took." [verbatim] Avoid rigid step-sequence checks.
  - Partial credit for multi-part tasks.
  - Calibrate LLM judges with human experts; "give the LLM a way out, like providing an instruction to return 'Unknown' when it doesn't have enough information." [verbatim]; structured rubrics; isolated judge per dimension.
  - Watch for grading bugs: Opus 4.5 scored 42% on CORE-Bench until fixes (rigid numeric matching, ambiguous specs) raised it to 95% (digest figures; source is an X post, not fetched); METR found misconfigured tasks that penalised following instructions (X post, not fetched).
  - "Make your graders resistant to bypasses or hacks." [verbatim] Passing should require solving the problem.

Maintain long term:
- Step 6, check the transcripts: tells you whether failures are agent or grader errors. "Failures should seem fair: it's clear what the agent got wrong and why." [verbatim]
- Step 7, monitor capability eval saturation: "Eval saturation occurs when an agent passes all of the solvable tasks, leaving no room for improvement." [verbatim] SWE-bench Verified went about 30% to over 80%. Qodo's one-shot evals missed Opus 4.5 gains on longer tasks, so they built an agentic eval. Do not take scores at face value.
- Step 8, keep suites healthy through ownership: dedicated evals team owns core infrastructure; domain experts and product teams contribute most tasks; owning evals should be as routine as unit tests. "We recommend practicing eval-driven development: build evals to define planned capabilities before agents can fulfill them" [verbatim, truncated]. Non-engineers can contribute tasks as PRs with Claude Code.

### How evals fit with other methods
Six methods with pros/cons (digest): automated evals (fast, reproducible, every commit; costly to build, false confidence); production monitoring (real behaviour; reactive, noisy, no ground truth); A/B testing (real outcomes; slow, little "why"); user feedback (unanticipated problems; sparse, self-selected, skews severe); manual transcript review (intuition; does not scale); systematic human studies (gold standard, calibrates graders; expensive). Timing: automated evals for pre-launch and CI/CD; monitoring post-launch; A/B for significant changes; feedback and transcript review ongoing; human studies to calibrate. "Like the Swiss Cheese Model from safety engineering, no single evaluation layer catches every issue." [verbatim]

### Conclusion
Teams without evals get stuck in reactive loops. Principles: start early, source tasks from real failures, define unambiguous criteria, combine grader types, keep tasks hard enough, improve signal-to-noise. "Read the transcripts!" [verbatim]

### Appendix: eval frameworks (digest only)
Harbor (containerised runs at scale, Terminal-Bench 2.0), Braintrust (offline evals, observability, `autoevals` scorers), LangSmith, Langfuse (self-hosted OSS), Arize (Phoenix OSS, AX SaaS). Advice: pick one that fits, then invest in the evals themselves. Promptfoo and marimo are not mentioned.

### Links the article relies on (not followed; see Open questions)
Building effective agents; Effective harnesses for long-running agents; Automated alignment auditing; Opus 4.5 announcement; Agent SDK overview (URLs in Sources).

## Practices as a checklist
Each line is testable; (S) = article section.
1. Tasks come from real failures (bug tracker, support queue, manual checks), starting with 20-50. (Step 0, Step 1)
2. Each task is unambiguous: two domain experts would independently reach the same pass/fail verdict. (Step 2)
3. Each task has a reference solution that passes its graders (proves solvable). (Step 2)
4. Any task at 0% over many trials is audited as a probable broken task before it counts against the agent. (Step 2)
5. The suite tests both when a behaviour should and should not occur (balanced set). (Step 3)
6. The eval agent runs in the same harness as the production agent. (Step 4)
7. Every trial starts from a clean environment; no leftover files, caches, or git history from earlier trials. (Step 4)
8. Trials do not share resource limits that correlate failures. (Step 4)
9. Graders are deterministic where possible; LLM graders only where needed; humans validate. (Step 5)
10. Graders check the outcome (final environment state), not the exact path taken. (Definitions; Step 5)
11. Multi-part tasks get partial credit. (Step 5)
12. LLM judges are calibrated against human experts, have an "Unknown" exit, use structured rubrics, one judge per dimension. (Step 5)
13. Graders cannot be passed by bypass or hack; passing requires solving the problem. (Step 5)
14. Grader bugs are hunted (rigid matching, ambiguous specs, misconfigured tasks) when scores look wrong. (Step 5)
15. Transcripts of failures are read; each failure is classifiable as agent error or grader error and "seems fair". (Step 6)
16. Saturation is monitored; saturated capability evals graduate to regression suites and harder capability tasks are added. (Step 7, Capability vs regression)
17. Capability evals start with a low pass rate; regression evals sit near 100%. (Capability vs regression)
18. Metrics choice is explicit: pass@k when one success suffices, pass^k when consistency matters; multiple trials per task. (Non-determinism)
19. Cost and latency metrics (turns, tool calls, tokens, latency) are tracked beside correctness. (Coding agents; Why build evals)
20. Someone owns the eval infrastructure; task contributions come through normal PRs; evals are defined before the capability exists. (Step 8)
21. Evals are one layer among several (monitoring, transcript review, human studies); no single layer is trusted alone. (How evals fit)

## Mapping to our program
All entries are INFERENCE: the article never mentions our belt, ICM, Codex, or multi-agent roles. Phases per the charter (1 ideal roster/role cards, 2 baseline, 3 differential and causes, 4 design incl. memory, 5 implement, 6 lasting evals).

| # | Practice | Phase(s) | How it bears (INFERENCE) |
|---|---|---|---|
| 1 | Tasks from real failures | 2, 6 | Gaps G1-G41 and incident records in `_system/governance/tickets/gaps.md` and handoffs are our "support queue"; seed cases from them (20-50 start). Phase 1 role-card "known failure modes" feed the same pool. |
| 2 | Unambiguous task | 6 (2) | Each case needs a cited ground truth at a pinned commit (charter phase 6 already says so); the two-expert test is a review rule for case authors. |
| 3 | Reference solution | 6 | For a belt role, a reference = a recorded correct run or a hand-built correct artefact (e.g. a ticket that lands cleanly) proving the case is solvable under the roster's context. |
| 4 | 0% audit | 2, 6 | When baseline agents fail a case 100%, check the case and the context supplied before blaming the agent; a context gap (phase 3) and a broken case look identical. |
| 5 | Balanced set | 6 | Include cases where the correct behaviour is to halt, refuse or do nothing (DISCIPLINE.md "halted session is a SUCCESS") as well as cases that should proceed. |
| 6 | Same harness as production | 2, 6 | Evals must run agents through the real Claude Code / Codex launch path with the real CLAUDE.md, hooks, permission mode; agent = model + harness (article definition), so a harness or hook change is a changed agent. |
| 7 | Clean environment | 2, 6 | Fresh worktree per trial; agents here can read git history, memory files (`~/.claude` MEMORY.md), prior handoffs, so those are leak channels exactly like the article's git-history example. Pin or sandbox what memory a trial may see. |
| 8 | No correlated resources | 2, 6 | Parallel lanes on one M3 share CPU/disk (memory notes on disk fill, check_gpu); concurrent trials are not independent. Record load. |
| 9-10 | Deterministic, outcome graders | 1, 2, 6 | Many belt outcomes are mechanically checkable (tests green, gate passes, ledger row, file in correct home, hash pin). Phase 1 automation analysis (operator concept 1) overlaps: a station checkable by script may not need an agent. Grade state, not narration. |
| 11 | Partial credit | 6 | Role success metrics decomposed per exit criterion. |
| 12 | Calibrated LLM judges | 2, 6 | Where judging is needed (Astra-style review quality, brief clarity), use human-labelled examples first, a cross-family judge (Claude vs Codex), an Unknown exit. Charter phase 6 already asks for cross-family grading. |
| 13 | Anti-hack graders | 6 | Agents on this belt can edit tests, ledgers, receipts; graders must read from pinned/hashed sources outside the agent's write reach. |
| 14-15 | Grader bugs, read transcripts | 2, 3 | Phase 2 reads transcripts anyway; add a per-failure label agent/grader/case/context. |
| 16-17 | Saturation, capability vs regression | 6 | Split suites: regression (must stay ~100% after any governance/tool/skill change, matches "rerun on every change") vs capability (new roles/cases). |
| 18 | pass@k / pass^k | 2, 6 | For the belt, pass^k (consistency across repeated trials) likely matters more than pass@k since a fresh builder must succeed each time; report both. Pre-register k. |
| 19 | Cost/latency | 2, 6 | Matches the 15-minute dispatch-to-merged goal and context-budget fields in role cards; track tokens, turns, wall time per role. |
| 20 | Ownership, eval-first | 4, 5, 6 | Evals defined before the fix is implemented (phase order 2 before 5 already does this); decide who owns the suite after the program. |
| 21 | Swiss cheese | 3, 4 | History, evals, monitoring (METRICS.md, ledger) and Astra review are separate layers; do not let evals replace them. |

## What the article does not cover
All INFERENCE (absence in a single fetched digest; the article body was not read raw, so treat "not covered" as likely, not certain).
- Multi-agent orchestration (MAESTRO delegating to builders, fixers, reviewers, subagents) and handoff correctness between roles. The article evaluates a single agent per task. Needed: per-role and end-to-end belt evals, and attribution of a failure to the right role.
- Codex CLI / non-Claude agents and cross-family grading; the article is Claude-centric.
- Context and memory evaluation: whether an agent got the right files, governance and memory for its task (our core hypothesis in the operator request). The article grades outputs and transcripts, not context sufficiency, retrieval precision, or drift of CLAUDE.md/CONTEXT.md routing. Needs separate measures (e.g. did the transcript read the one home file; did it apply a rule from memory instead of the file).
- Governance/process compliance as an outcome (halting correctly, following Stage gates) beyond tool-call checks.
- Evaluation of sessions across time: resets, handoffs, context-window management, memory consolidation (phase 4).
- Statistical design: sample sizes, confidence intervals, significance of pass-rate changes, seeds, model-version pinning, pre-registration. The article gives 20-50 tasks and pass@k/pass^k but no inference procedure; our phase 6 asks for "scientifically durable".
- Cost of evals themselves and budgets (operator has finite Claude/Codex weekly usage).
- Environment fidelity for repo-level work on macOS with sandbox/permission-mode differences (hooks, classifier denials) that change agent behaviour.
- Effect of changing the model underneath a role (version drift) on baselines.

## MAESTRO verification against the raw article (2026-10-17, Opus 5.5)
Method: MAESTRO read the full article text in Chrome (`get_page_text` on [1], 2026-10-17; curl from the MAESTRO shell was denied). Result: every [verbatim] quote above matches the article. The [truncated] quotes are complete sentences in the article. Corrections and additions:
- "a hill to climb" is verbatim: "They should start at a low pass rate, targeting tasks the agent struggles with and giving teams a hill to climb."
- The CORE-Bench (42% to 95%) and METR facts are in the article body, not only in X posts. Open question 3 is closed.
- Not in the digest, verbatim: "Each task should be passable by an agent that follows instructions correctly." / "Everything the grader checks should be clear from the task description; agents shouldn't fail due to ambiguous specs." / "As a rule, we do not take eval scores at face value until someone digs into the details of the eval and reads some transcripts." / "sample transcripts to read weekly" / "grade each dimension with an isolated LLM-as-judge rather than using one to grade all dimensions" / "Once the system is robust, it's sufficient to use human review only occasionally."
- Tool-selection eval: "In our Claude for Chrome product, we developed evals to check that the agent was selecting the right tool for each context." (This is the nearest the article comes to a context or routing eval.)
- The article names multi-agent work as open: "As agents take on longer tasks, collaborate in multi-agent systems, and handle increasingly subjective work, we will need to adapt our techniques." This confirms the first item of "What the article does not cover".
- Open question 2 is closed. Open question 1 (the linked posts) stays open.

## Open questions for MAESTRO
1. Follow the article's linked posts ("Effective harnesses for long-running agents", "Building effective agents") in a separate equip task? They are likely relevant to handoff/reset design; not fetched here.
2. Fetch the raw page (curl was denied by the permission system) to confirm that the two truncated quotes and the "hill to climb" wording are exact? The fetcher also can paraphrase silently; verbatim tags rely on a second pass.
3. CORE-Bench 42% to 95% and METR claims are from X posts; fetch if used as evidence.
4. Does the program adopt pass^k as the primary belt metric (INFERENCE above), and which k?
5. Which belt outcomes are mechanically gradable today, and which need a judge (links Phase 1 automation analysis)?

## Sources
1. https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents (2026-01-09), main source; WebFetch 2026-10-17, two passes.
2. https://www.anthropic.com/engineering/building-effective-agents (date not checked; linked, not fetched).
3. https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents (date not checked; linked, not fetched).
4. https://alignment.anthropic.com/2025/automated-auditing/ (linked, not fetched).
5. https://www.anthropic.com/news/claude-opus-4-5 (linked, not fetched).
6. https://platform.claude.com/docs/en/agent-sdk/overview (linked, not fetched).
7. tau-Bench arXiv 2406.12045; tau2-Bench arXiv 2506.07982; BrowseComp arXiv 2504.12516; WebArena arXiv 2307.13854 (benchmark citations from the article; not read).
8. Charter: /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/projects/agent-workflow/brief/charter.md (phases, operator text) and brief/equip-common.md (rules).
