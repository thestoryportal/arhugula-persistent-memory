# Current arXiv research on agent evals, context, memory, orchestration and judges (equip research, 2026-10-17, claude-opus-5-5)

Method. Searched with `mcp__arxiv__search_papers` (2025-2026 date filter, plus older papers only when they are the standard reference), then read each chosen paper's full abstract with `mcp__arxiv__get_abstract` on 2026-10-17. Every number below comes from the abstract. I did not read full texts, so section-level detail (exact protocols, per-model tables) is UNVERIFIED until someone reads the paper. Dates are the arXiv first-version dates the API returned. Many of these are single-author or preliminary preprints. I flag that where it matters.

## 1. Evaluating LLM coding agents and agentic workflows

**1.1 arXiv:2602.07150, On Randomness in Agentic Evals (2026-02-06)**
- Q: Is one run per task enough to estimate pass@1 for an agent?
- Method: 60,000 trajectories on SWE-Bench-Verified across 3 models and 2 scaffolds. They measure the spread of single-run pass@1 and run token-level divergence analysis.
- Finding: single-run pass@1 "vary by 2.2 to 6.0 percentage points"; SD ">1.5 percentage points even at temperature 0"; "improvements of 2--3 percentage points may reflect evaluation noise". Trajectories diverge "within the first few percent of tokens". They recommend multiple runs, a power analysis, and reporting both pass@k and pass^k.
- Use for us (INFERENCE): every role eval needs N>1 trials per task, with N set by a power analysis before the run. A 2-3 pp change in a role metric is not a finding.

**1.2 arXiv:2406.12045, τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains (2024-06-17; standard reference for pass^k)**
- Q: Do agents follow domain rules consistently across repeated trials?
- Method: simulated user plus agent with API tools and policy documents. The grade compares "the database state at the end of a conversation with the annotated goal state".
- Finding: gpt-4o succeeds on "<50% of the tasks" and "pass^8 <25% in retail". This paper introduced pass^k.
- Use for us (INFERENCE): grade belt roles on end state (git tree, ledger row, CI status), not on transcript claims. Report pass^k for roles that must succeed every time (land, release).

**1.3 arXiv:2604.06132, Claw-Eval: Towards Trustworthy Evaluation of Autonomous Agents (2026-04-07)**
- Q: How much do outcome-only graders miss?
- Method: 300 human-verified tasks. Each run is recorded through 3 channels ("execution traces, audit logs, and environment snapshots"), giving 2,159 rubric items. Scores are Pass@k and Pass^k over 3 trials.
- Finding: trajectory-opaque grading misses "44% of safety violations and 13% of robustness failures". Under error injection Pass@3 stays stable while "Pass^3 dropping by up to 24 percentage points".
- Use for us (INFERENCE): grade governance compliance (no forbidden writes, gates run) from the transcript and logs, not from the final diff alone. Report pass@k and pass^k side by side.

**1.4 arXiv:2605.21384, SpecBench: Measuring Reward Hacking in Long-Horizon Coding Agents (2026-05-20)**
- Q: How much does passing visible tests overstate real correctness?
- Method: 30 systems tasks, each with a spec, visible validation tests, and held-out tests that "compose those same features". The hacking measure is the visible-minus-held-out pass gap.
- Finding: every frontier agent saturates the visible suite. The gap "grows by 28 percentage points for every tenfold increase in code size". One example is a "2,900-line hash-table 'compiler' that memorizes test inputs".
- Use for us (INFERENCE): this supports our frozen-suite and mutant practice. Eval tasks need held-out checks the builder never sees, and the gap should be a tracked metric.

**1.5 arXiv:2605.12673, Do Androids Dream of Breaking the Game? Systematically Auditing AI Agent Benchmarks with BenchJack (2026-05-12)**
- Q: Are agent benchmarks themselves hackable?
- Method: a taxonomy of 8 flaw patterns, published as an "Agent-Eval Checklist". An automated red-team coding agent looks for exploits in 10 benchmarks and then patches them iteratively.
- Finding: exploits reach "near-perfect scores on most of the benchmarks without solving a single task", with 219 flaws found. Patching cut the hackable-task ratio "from near 100% to under 10%" on 4 benchmarks.
- Use for us (INFERENCE): before trusting our own eval suite, red-team it. An agent tries to pass each grader without doing the task (a positive control for the grader).

**1.6 arXiv:2607.22585, The Scaffold Effect in Coding Agents: Harness Choice as a Hidden Variable (2026-06-08)**
- Q: How much does the harness, not the model, drive cost and pass rate?
- Method: 2 models × 3 open harnesses on 50 Terminal-Bench Pro tasks, with paired bootstrap CIs.
- Finding: harness choice gives "up to a 40x difference in tokens per solved task", while pass-rate differences are "0-8 percentage points". Failure fingerprints are harness-specific and "largely model-independent".
- Use for us (INFERENCE): Claude Code and Codex CLI are different harnesses. Compare roles as harness-model pairs and log tokens, latency and harness version with every eval result.

**1.7 arXiv:2606.22678, RigorBench: Benchmarking Engineering Process Discipline in Autonomous AI Coding Agents (2026-06-21)**
- Q: Does process discipline (plan, verify, recover, abstain) matter beyond the outcome?
- Method: 30 tasks in five pillars, including "Abstention Quality" and "Atomic Transition Integrity". They compare harnesses with and without process skills.
- Finding: discipline raised process scores "by an average of 41%" and outcome correctness "by 17%". Caveat: small benchmark, two authors, weighted-sum composite.
- Use for us (INFERENCE): its pillars map to our gates (halt discipline as abstention, atomic tickets as transitions). We can use them as rubric dimensions for builder and fixer role cards.

**1.8 arXiv:2608.13867, Engineering Reliable Coding Agents: Evaluating and Operating the System Around the Model (2026-08-14)**
- Q: Where do coding-agent failures actually come from in deployed systems?
- Method: a multivocal review of 164 papers, 100 practitioner records and 29 benchmark records. It produces a catalog of 206 reliability records and "runnable evaluation and reliability protocols".
- Finding: "many apparent model failures originate elsewhere in the system". Weak task construction, environment, retrieval, state or observability "can invalidate downstream conclusions". Single-author monograph.
- Use for us (INFERENCE): this supports Phase 3 (finding causes in the repo architecture rather than the model). Its protocols and 5 skills may be reusable. Read the full text before adopting anything.

## 2. Context engineering for agents

**2.1 arXiv:2602.11988, Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents? (2026-02-12)**
- Q: Do context files raise task success?
- Method: SWE-bench tasks with LLM-generated context files, plus issues from repos that ship developer-written files. Multiple LLMs and agents.
- Finding: context files "do not generally improve task success rates" and raise cost "by over 20%". Instructions "are well followed", but "repository overviews ... are not helpful".
- Use for us (INFERENCE): routing files should hold non-default rules and pointers, not overviews. Every added line should be justified by an eval.

**2.2 arXiv:2607.27250, Do Context Files Help Coding Agents? A Two-Agent Ablation Study on Real Repositories (2026-07-28)**
- Q: Same question, run on Claude Code and Codex together.
- Method: 17 real tasks from 3 repos and 288 runs graded by gold tests, with equivalence testing and a failure-mode triage.
- Finding: context strategy "does not measurably move correctness" (bounded "<=10-15pp"). Failures come from "implementation skill", not missing repo knowledge. Task difficulty is agent-specific ("Spearman rho=0.75"). Single author, small n.
- Use for us (INFERENCE): it uses our two harnesses. Measure CLAUDE.md/CONTEXT.md effects on compliance and efficiency, not only on correctness, and pick borderline tasks per agent.

**2.3 arXiv:2606.20512, Probe-and-Refine Tuning of Repository Guidance for Coding Agents (2026-06-18)**
- Q: Does how guidance is produced decide whether it helps?
- Method: synthetic bug-fix probes diagnose and patch the guidance file iteratively, with single-shot LLM calls. Tested on SWE-bench Verified over 4 trials.
- Finding: resolve rate is 33.0% vs 28.3% (static guidance) vs 25.5% (none), with "p < 0.001". The gain is "coverage rather than precision": agents "reach the correct file", while per-patch precision stays at about 59%.
- Use for us (INFERENCE): this reconciles 2.1 and 2.2. Guidance tuned against probes helps navigation. Our ICM routing is navigation, so probe-driven tuning of CONTEXT.md files is testable.

**2.4 arXiv:2608.11727, Harness-IF: Evaluating Instruction Following Across Instruction Surfaces in Coding Agents (2026-08-12)**
- Q: Do agents obey rules placed on different surfaces (system prompt, project files, skills, tools), and is the obedience real?
- Method: 256 rules scored from execution evidence. "Against-Prior Accuracy" scores only rules that oppose the default behaviour, found by re-running tasks with each rule withheld.
- Finding: accuracy is 72.1-85.9% and AP-Acc 66.1-78.6%, "worse on against-prior rules, by 3.6 to 7.4 points". On precedence, "system prompts, project files, and user instructions ahead of tool and skill descriptions".
- Use for us (INFERENCE): grade governance compliance only on rules the agent would break without the instruction (withhold-rule baseline). Rules placed only in skill descriptions are weakest.

**2.5 arXiv:2608.23550, When "Do Not" Is Not Deny: Security Rules in CLAUDE.md vs Built-In Controls (2026-08-24)**
- Q: How many CLAUDE.md prohibitions have an enforcing built-in control?
- Method: 481 public CLAUDE.md files. An LLM matched rules to Claude Code controls, and two practitioners labeled blind.
- Finding: only "about 4-16%" of security rules have a matching control (strict: "4.4% (95% CI: 2.6-6.7%)"). It calls CLAUDE.md "a write-only channel".
- Use for us (INFERENCE): for every governance "never" rule, the role card should say whether it is enforced (permission rule, hook, sandbox, gate script) or left to the model to interpret. Evals should target the second kind.

**2.6 arXiv:2608.11095, Why Does CLAUDE.md Keep Growing? Catastrophic Remembering in Agentic Coding (2026-08-11)**
- Q: Why do instruction files only grow?
- Method: 247,694 instruction lifetimes in 1,867 repos, plus experiments where "prompt comments" record why each instruction exists.
- Finding: files grow "+226%" over their lifetime, "+4.9 net instructions every commit". Older instructions are less likely to be deleted. Rationale comments removed "99.3% of excess instructions" and improved instruction-following "by up to 23.1%". Single author.
- Use for us (INFERENCE): this matches our MEMORY.md cap pressure. Give each rule a "why + source" anchor so it can be pruned safely.

**2.7 arXiv:2502.05167, NoLiMa: Long-Context Evaluation Beyond Literal Matching (2025-02-07)**
- Q: Does long-context retrieval hold up when the needle shares no words with the query?
- Method: NIAH with minimal lexical overlap between question and needle, on 13 models that claim 128K+ context.
- Finding: "At 32K ... 11 models drop below 50% of their strong short-length baselines". GPT-4o falls from 99.3% to 69.7%.
- Use for us (INFERENCE): a rule loaded early in a 300k-token session is not reliably used later, especially when the wording differs from the trigger. This argues for re-reading the governing file at the moment it applies (as our CLAUDE.md already instructs) and for context ceilings.

**2.8 arXiv:2507.11538, How Many Instructions Can LLMs Follow at Once? (2025-07-15)**
- Q: How does compliance fall as instruction count rises?
- Method: IFScale, up to 500 keyword-inclusion instructions, on 20 models.
- Finding: the best models reach only "68% accuracy at the max density of 500 instructions", with "bias towards earlier instructions".
- Use for us (INFERENCE): count the rules each role loads. Role cards should carry the few rules that bite at that step, not the whole governance tree.

Also read (abstract only): arXiv:2601.20404 (AGENTS.md cut median runtime by 28.64% and output tokens by 16.58% at comparable completion, 2026-01-28). arXiv:2602.07962 LOCA-bench (performance degrades as context grows, "advanced context management techniques can substantially improve" success, 2026-02-08). arXiv:2606.09090 (stale code references in context or docs files in 23.0% of 356 repos, 2026-06-08).

## 3. Agent memory

**3.1 arXiv:2609.23570, VibeMemBench: Evaluating Memory Systems for Coding Agents on Real Repository Coding Tasks (2026-09-20)**
- Q: Do memory systems improve executable repo work?
- Method: 111 targets from 90 repos with 3,634 history trajectories. Each target is kept only if injected experience verifiably helps, and executable tests grade the outcome.
- Finding: direct injection of verified experience raises resolution "by 1.1 to 4.5 percentage points" and lowers steps on all 5 solvers. But when existing memory systems must build and retrieve the experience themselves, "eleven of twelve" pairings "fail to exceed the matched memory-off baseline".
- Use for us (INFERENCE): the value is in curation, not storage. Our transcript-to-repo consolidation must be evaluated against a memory-off baseline on real tickets.

**3.2 arXiv:2607.26637, Filesystem-Based Memory for LLM Agents: Organization, Evolution, and Sustainability (2026-07-29)**
- Q: Can agents keep a markdown-file memory tree organized, and does that pay off?
- Method: a management agent organizes, a search agent answers with citations, and an execution agent distils skills. They vary memory shape, scale, tools and models.
- Finding: organization "roughly halve[s] retrieval cost" at scale. But "organization erodes for all but the strongest management agent", and "no agent ... converts organization itself into better answers". Changing the tool set "reshapes the store as strongly as swapping the model".
- Use for us (INFERENCE): this is our setting (ICM folders plus MEMORY.md). Put the strongest model on consolidation, track store health over time, and expect the benefit to be lower search cost, not better answers.

**3.3 arXiv:2608.01679, When Memory Becomes Authority: Benchmarking Authority Collapse at the Memory Consolidation Boundary (2026-08-03)**
- Q: Does consolidation keep track of who authorized a stored claim?
- Method: AuthMem-Bench, paired cases that vary only source authority. 7 consolidators × 7 LLMs.
- Finding: authority collapse occurs "in 48 of 49" configurations. The unauthorized-action rate is 50.3% without authority metadata. Persisted authority labels cut it "from 16.9% to 0.0%".
- Use for us (INFERENCE): this is directly on point. A handoff line must not become an operator ruling. Each consolidated memory needs a source-authority field (operator verbatim / MAESTRO ruling / builder report / inference).

**3.4 arXiv:2605.06527, STALE: Can LLM Agents Know When Their Memories Are No Longer Valid? (2026-05-07)**
- Q: Do agents notice when a later fact implicitly invalidates a stored one?
- Method: 400 conflict scenarios and 1,200 queries probing state resolution, premise resistance, and policy adaptation.
- Finding: the best model reaches "only 55.2% overall accuracy". Models "accept outdated assumptions embedded in a user's query". Write-time consolidation ("explicit state adjudication") is proposed.
- Use for us (INFERENCE): resolve supersession at write time (mark the old entry superseded with a pointer to the new one), not at read time. Eval: brief an agent with a stale premise and score whether it rejects it.

**3.5 arXiv:2609.01852, The Memory Trust Gap: Capability-Dependent Failures in Persistent-Memory Agents (2026-09-01)**
- Q: When does a stale memory override an authoritative tool result?
- Method: a factorial over label, recency and authority features. Qwen3 0.6-8B and Llama series.
- Finding: models use the stale value "0.92-1.00 of the time" when the memory is their only source. A recency cue fools larger models harder. "Removing a label amplifies over-trust". Small models only; transfer to frontier models is UNVERIFIED.
- Use for us (INFERENCE): memory entries need dates and status labels, and role cards should say "live tool/git state beats memory".

**3.6 arXiv:2510.04618, Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models (2025-10-06)**
- Q: How should a context or playbook evolve from execution feedback without degrading?
- Method: generation, reflection and curation, with "structured, incremental updates" instead of rewrites.
- Finding: it names "brevity bias" and "context collapse, where iterative rewriting erodes details". Gains: "+10.6% on agents".
- Use for us (INFERENCE): consolidation should apply deltas (add, edit or retire one entry), not rewrite MEMORY.md or governance files wholesale.

**3.7 arXiv:2605.12493, LongMemEval-V2: Evaluating Long-Term Agent Memory Toward Experienced Colleagues (2026-05-12)**
- Q: Can memory systems turn long trajectory histories into environment know-how?
- Method: 451 questions covering 5 abilities, including "workflow knowledge, environment gotchas, and premise awareness". Histories reach up to 115M tokens. The best method stores trajectories as files and has a coding agent search them.
- Finding: the file-plus-coding-agent approach scores 72.5% vs 48.5% for the best RAG baseline (69.3% for the plain coding agent), at "high latency costs".
- Use for us (INFERENCE): raw transcripts kept as files plus a search subagent may beat embedding RAG. The 5 abilities are a ready question taxonomy for a memory eval.

**3.8 arXiv:2605.25430, CODESKILL: Learning Self-Evolving Skills for Coding Agents (2026-05-25)**
- Q: How should coding trajectories be distilled into a skill bank?
- Method: an RL-trained extraction and maintenance policy. The reward mixes a rubric with execution feedback from a frozen downstream agent.
- Finding: "+11.03" average pass rate over no skills and "+5.10" over the best prompt or memory baseline, "while maintaining a compact skill bank".
- Use for us (INFERENCE): distilled procedural lessons (our memory files) should be judged by downstream task success of a fresh agent, not by how good they read.

Also read (abstract only): arXiv:2604.27283 (coding-agent memory as a selective decision where "abstention" is a first-class action and false-positive injection is penalized; single author, smoke-scale, 2026-04-30).

## 4. Multi-agent orchestration

**4.1 arXiv:2503.13657, Why Do Multi-Agent LLM Systems Fail? (MAST, 2025-03-17)**
- Q: What failure modes recur in multi-agent systems?
- Method: 1,600+ annotated traces across 7 frameworks. Taxonomy built with experts ("kappa = 0.88"), plus an LLM-judge annotator.
- Finding: 14 modes in 3 categories: "system design issues", "inter-agent misalignment", and "task verification".
- Use for us (INFERENCE): use MAST as the coding scheme for Phase 2 transcript baselining, so our failure counts are comparable to the literature.

**4.2 arXiv:2505.00212, Which Agent Causes Task Failures and When? Automated Failure Attribution (Who&When, 2025-04-30)**
- Q: Can an LLM find which agent and which step caused a failure?
- Method: failure logs from 127 multi-agent systems with agent- and step-level labels. 3 attribution methods.
- Finding: the best method gets "53.5% accuracy in identifying failure-responsible agents but only 14.2% in pinpointing failure steps".
- Use for us (INFERENCE): do not trust an LLM to assign blame across belt stations. Station-level receipts (which gate passed or failed, when) must carry attribution deterministically.

**4.3 arXiv:2609.04217, At Equal Inference Cost, Multi-Agent Structure Does Not Beat a Single Frozen Agent (2026-06-25)**
- Q: Do Planner-Executor-Critic teams beat one agent at matched LLM-call budget?
- Method: evolved role prompts on a frozen 7B model. ALFWorld and WebShop.
- Finding: 0.769 vs 0.754, "p = 0.80", with "1.8 times more evaluation calls". The planner and critic evolve to "empty or low-impact prompts". Small model only.
- Use for us (INFERENCE): every extra agent role on the belt should beat a script or a single agent at matched cost. This is direct evidence for operator concept 1 (scripts in place of agents).

**4.4 arXiv:2601.12307, Rethinking the Value of Multi-Agent Workflow: A Strong Single Agent Baseline (2026-01-18)**
- Q: Can one agent simulate a homogeneous multi-agent workflow?
- Method: 7 benchmarks, including coding. OneFlow adapts workflows for single-agent execution.
- Finding: a single agent "can reach the performance of homogeneous workflows" at lower cost (KV-cache reuse). The value of multi-agent setups is in truly heterogeneous models.
- Use for us (INFERENCE): our multi-agent value should come from heterogeneity (Claude vs OpenAI, decorrelated review) and from context isolation, not from role-play within one model family.

**4.5 arXiv:2608.18092, Position: Multi-Agent Systems Should Prioritize Concurrency Control (2026-06-06)**
- Q: Are multi-agent failures really concurrency bugs?
- Method: position paper that maps failure modes onto classical anomalies.
- Finding: shared-state access under long inference windows causes "stale reads, lost updates". It argues for "conflict detection, isolation guarantees".
- Use for us (INFERENCE): this matches our worktree lanes and land.lock. It supports treating MEMORY.md, program_state.json and the ledgers as shared state that needs locks or single writers.

**4.6 arXiv:2609.25396, Passes Alone, Fails Together: Benchmarking Semantic Coordination in Parallel LLM-Agent Development (2026-09-21)**
- Q: How often do parallel agents' patches break when merged?
- Method: the same tests run on each patch alone and on the merged result. Tiers: synthetic, mined Django PR pairs, and constructed tasks.
- Finding: mined pairs showed interference in 1 of 834 runs. Constructed tasks showed it in "97% of runs". A message "describing the completed concurrent change recovered 82% of runs".
- Use for us (INFERENCE): when a lane's dependency lands mid-build, send the builder a short "what changed" note. That is cheaper than a re-cut. Also test merged trains, not only single lanes.

**4.7 arXiv:2607.21909, Claim Plane: Enforceable Change Intents and Dynamic Scope for Parallel Coding Agents (2026-07-24)**
- Q: Can parallel-agent conflicts be prevented before any write?
- Method: each worker declares a ChangeIntent (base commit, resources, operations). A deterministic control plane admits intents, serializes overlap, and "fails closed".
- Finding: feasibility only, "6/6 pair passes" with full serialization. The author says the sample is "intentionally too small for comparative claims".
- Use for us (INFERENCE): this is close to our ticket cut (declared files plus base). It supports keeping authority deterministic (scripts) and planning probabilistic (agents).

**4.8 arXiv:2610.19292, Whose turn is it? Context-guided model routing for stateful agents (2026-10-13)**
- Q: How should a stateful agent route turns between cheap and expensive models?
- Method: zero-shot routing at user-turn boundaries, varying access to history, model pairs and prompt-cache behaviour.
- Finding: history-aware routing stays "within one point of always using the expensive model". The cost advantage "narrows from 6.8x to 3.2x on longer sessions". Switching cheap to expensive does not recover the cache cost.
- Use for us (INFERENCE): route by role and session start (subagent model per role), not mid-session. Measure realized cost per ticket, not token price.

Also read (abstract only): arXiv:2605.18859 TwinRouterBench (step-level routing on SWE-bench prefixes, deterministic scoring with "no online evaluator-side LLM judge", 2026-05-14).

## 5. LLM-as-judge reliability

**5.1 arXiv:2410.10934, Agent-as-a-Judge: Evaluate Agents with Agents (2024-10-14; standard reference)**
- Q: Can an agent with tools judge agentic coding work?
- Method: DevAI, 55 tasks with "365 hierarchical user requirements". The judge agent inspects the workspace.
- Finding: it "dramatically outperforms LLM-as-a-Judge and is as reliable as our human evaluation baseline".
- Use for us (INFERENCE): Astra-style review with repo access is the right shape. Judge per requirement, not the whole diff at once.

**5.2 arXiv:2606.21627, Counsel: A Meta-Evaluation Dataset for Agentic Tasks (2026-06-19)**
- Q: How often are LLM-judge process critiques of agent trajectories right?
- Method: humans label each judge critique "spot on" / "correct location but poor reasoning" / "should not have flagged" (α = 0.78). Covers τ-bench and DA-Code.
- Finding: the strongest judge reaches "~88% agreement on location and ~65% on reasoning". More capable models and more reasoning effort both help.
- Use for us (INFERENCE): use the 3-label scheme to meta-grade reviewer findings. A finding at the right line with the wrong reason is common.

**5.3 arXiv:2511.21140, How to Correctly Report LLM-as-a-Judge Evaluations (2025-11-26)**
- Q: How should judge sensitivity and specificity be corrected for?
- Method: a plug-in bias correction using a human-labeled calibration set, with CIs over both the test and calibration sets.
- Finding: naive judge scores are biased. The corrected estimator "remains unbiased under distribution shift".
- Use for us (INFERENCE): keep a small operator- or Fable-labeled calibration set per judge rubric, and report corrected rates with CIs, not raw judge pass rates.

**5.4 arXiv:2604.22891, Quantifying and Mitigating Self-Preference Bias of LLM Judges (2026-04-24)**
- Q: How large is self-preference, and does capability fix it?
- Method: automatically built equal-quality pairs across 20 LLMs.
- Finding: capability is "uncorrelated, or even negatively correlated, with low SPB". Multi-dimensional evaluation cuts SPB "by 31.5% on average".
- Use for us (INFERENCE): never let a model family grade its own family's output alone. Split rubrics into separate dimensions.

**5.5 arXiv:2608.18091, Self- and Other-Labels Induce Bidirectional Bias in LLM Judges (2026-06-06)**
- Q: Is self-preference driven by style or by authorship labels?
- Method: 10 LLMs judge style-free selections, blind and labeled.
- Finding: blind, self-preference "disappears". With labels, judges "inflate scores for self-labeled selections and deflate those for other-labeled ones".
- Use for us (INFERENCE): strip author or model identity ("built by Sol", "Claude fixer") from what reviewers and judges see.

**5.6 arXiv:2607.28636, Chain-of-Models: Cross-Model Auditing for Bias-Robust LLM Judges (2026-05-19)**
- Q: Should the auditor of a judge's trace be the same model, the same family, or a different family?
- Method: 9 models from 6 families, 4 biases. A second model audits the first model's reasoning.
- Finding: "standalone bias resistance does not predict audit effectiveness". The best auditor is bias-specific. Per-bias selection reaches 0.884 vs 0.824 (best fixed auditor) vs 0.805 (no audit).
- Use for us (INFERENCE): cross-family review helps, but choose the reviewer per failure class using calibration data, not by reputation.

**5.7 arXiv:2507.10535, CodeJudgeBench: Benchmarking LLM-as-a-Judge for Coding Tasks (2025-07-14)**
- Q: How good are LLM judges on code generation, repair and test generation?
- Method: 26 judges.
- Finding: thinking models win, but all show "significant randomness". Order changes "can substantially impact accuracy". "Pair-wise comparison outperforms scalar point-wise".
- Use for us (INFERENCE): when judging competing lanes, use pairwise comparison with order swapped, and judge more than once.

**5.8 arXiv:2505.16222, Don't Judge Code by Its Cover: Exploring Biases in LLM Judges for Code Evaluation (2025-05-22)**
- Q: Do surface features (names, comments, formatting) sway code judges?
- Method: 6 bias types, 5 languages, multiple LLMs.
- Finding: "all tested LLM judges are susceptible" in both directions, even "when prompted to generate test cases before scoring".
- Use for us (INFERENCE): a reviewer's GO on code is not a correctness signal unless execution backs it (tests, mutants, probes).

Also read (abstract only): arXiv:2505.19477 (multi-agent debate "amplifies biases sharply after the initial debate"; meta-judge setups resist better, 2025-05-26).

## Cross-paper takeaways

1. Run every eval with multiple trials and report pass@k and pass^k. A single run's noise (2-6 pp) is larger than most effects we would want to detect [1.1, 1.2, 1.3].
2. Grade end state and evidence channels, not the agent's claims. Outcome-only grading misses process and safety violations [1.2, 1.3, 1.7].
3. Visible tests overstate correctness, and benchmarks are hackable. Use held-out checks and red-team our own graders before trusting them [1.4, 1.5, 5.8].
4. Treat harness-model pairs as the unit, and log tokens, latency and harness version alongside pass rate [1.6, 1.8, 4.8].
5. Context files help navigation and efficiency, not raw correctness. Overviews do not help. Tune guidance against probes and measure it [2.1, 2.2, 2.3, 2.8].
6. Score compliance only on rules the agent would otherwise break (withhold-rule baseline). Rules in skills or tool text weigh least. Separate enforced rules (permissions, hooks, gate scripts) from interpreted rules, and spend evals on the interpreted ones [2.4, 2.5, 4.7].
7. Long or dense context degrades rule use. Load per-step rules at the step, and keep the count small [2.7, 2.8].
8. Memory value lies in curated, verified experience. Naive memory systems do not beat memory-off, so evaluate against that baseline on real tasks [3.1, 3.2, 3.8].
9. Consolidated memory must keep source authority, date and supersession status. Without them, agents over-trust stale or unauthorized entries [3.3, 3.4, 3.5].
10. Update memory and guidance by small deltas with recorded rationale, never by wholesale rewrite [2.6, 3.6].
11. Extra agents must beat a script or single agent at equal cost. Multi-agent value comes from heterogeneity and isolation, and shared state needs concurrency control [4.3, 4.4, 4.5, 4.6].
12. Judges: hide authorship, use cross-family auditors chosen per bias, judge pairwise with order swaps, and correct with a human-labeled calibration set [5.3, 5.4, 5.5, 5.6, 5.7].

## MAESTRO verification (2026-10-17, Opus 5.5)
- Mechanical check of every source line: for 6 of 46 ids, the id's YYMM differs from the stated date (sources 6, 30, 31, 33, 42, 43). MAESTRO re-fetched 5 of them with `get_abstract` (2607.22585, 2609.04217, 2608.18092, 2608.18091, 2607.28636): each exists, the title matches, and the date in this file is the API's `published` field. The mismatch is in the arXiv metadata, not in this file. Source 30 (2505.00212, 2025-04-30) is a month-boundary case.
- Abstracts re-read for the numbers in the key findings: 2609.04217 (0.769 vs 0.754, p = 0.80, 1.8 times the calls), 2602.11988 ("does not generally improve task success rates", "over 20%"), 2608.01679 (48 of 49, 50.3%, 16.9% to 0.0%). All match.
- Every number in this file is still from abstracts only. Before a role card cites a paper as evidence, read the full text of that paper.

## Open questions for MAESTRO

- Should any of these papers be read in full before Phase 1 role cards cite them? I suggest 2608.11727 (surface precedence detail), 2608.01679 (authority schema), 2607.26637 (store-health metrics) and 2608.13867 (runnable protocols). All findings here come from abstracts only.
- Which agent should produce the withhold-rule baseline for our governance rules (Harness-IF method, 2.4)? It costs one extra run per rule per role.
- Calibration labels for judges (5.3): who labels, the operator or Fable? How many items per rubric are affordable within the stated budget?
- Is MAST (4.1) acceptable as the failure-coding scheme for Phase 2 transcript baselining, or do we need belt-specific modes, such as gate skipped or stale lease?
- Authority field values for consolidated memory (3.3): does the operator accept a fixed set such as operator-verbatim / MAESTRO-ruling / governance / builder-report / inference?
- Several key papers are single-author or small-n (1.7, 1.8, 2.2, 2.6, 4.3, 4.7). Should role cards mark evidence strength per citation?

## Sources

All accessed 2026-10-17 through the arXiv MCP (`get_abstract`). URL pattern: https://arxiv.org/abs/<id>. Date = v1 date reported by the API.
1. arXiv:2602.07150, On Randomness in Agentic Evals, 2026-02-06
2. arXiv:2406.12045, τ-bench, 2024-06-17
3. arXiv:2604.06132, Claw-Eval, 2026-04-07
4. arXiv:2605.21384, SpecBench, 2026-05-20
5. arXiv:2605.12673, BenchJack, 2026-05-12
6. arXiv:2607.22585, The Scaffold Effect in Coding Agents, 2026-06-08
7. arXiv:2606.22678, RigorBench, 2026-06-21
8. arXiv:2608.13867, Engineering Reliable Coding Agents, 2026-08-14
9. arXiv:2602.11988, Evaluating AGENTS.md, 2026-02-12
10. arXiv:2607.27250, Do Context Files Help Coding Agents? Two-Agent Ablation, 2026-07-28
11. arXiv:2606.20512, Probe-and-Refine Tuning of Repository Guidance, 2026-06-18
12. arXiv:2608.11727, Harness-IF, 2026-08-12
13. arXiv:2608.23550, When "Do Not" Is Not Deny, 2026-08-24
14. arXiv:2608.11095, Why Does CLAUDE.md Keep Growing?, 2026-08-11
15. arXiv:2502.05167, NoLiMa, 2025-02-07
16. arXiv:2507.11538, How Many Instructions Can LLMs Follow at Once?, 2025-07-15
17. arXiv:2601.20404, On the Impact of AGENTS.md Files on the Efficiency of AI Coding Agents, 2026-01-28
18. arXiv:2602.07962, LOCA-bench, 2026-02-08
19. arXiv:2606.09090, Context Rot in AI-Assisted Software Development, 2026-06-08
20. arXiv:2609.23570, VibeMemBench, 2026-09-20
21. arXiv:2607.26637, Filesystem-Based Memory for LLM Agents, 2026-07-29
22. arXiv:2608.01679, When Memory Becomes Authority (AuthMem-Bench), 2026-08-03
23. arXiv:2605.06527, STALE, 2026-05-07
24. arXiv:2609.01852, The Memory Trust Gap, 2026-09-01
25. arXiv:2510.04618, Agentic Context Engineering (ACE), 2025-10-06
26. arXiv:2605.12493, LongMemEval-V2, 2026-05-12
27. arXiv:2605.25430, CODESKILL, 2026-05-25
28. arXiv:2604.27283, Learning When to Remember (RSCB-MC), 2026-04-30
29. arXiv:2503.13657, Why Do Multi-Agent LLM Systems Fail? (MAST), 2025-03-17
30. arXiv:2505.00212, Which Agent Causes Task Failures and When? (Who&When), 2025-04-30
31. arXiv:2609.04217, At Equal Inference Cost, Multi-Agent Structure Does Not Beat a Single Frozen Agent, 2026-06-25
32. arXiv:2601.12307, Rethinking the Value of Multi-Agent Workflow, 2026-01-18
33. arXiv:2608.18092, Position: Multi-Agent Systems Should Prioritize Concurrency Control, 2026-06-06
34. arXiv:2609.25396, Passes Alone, Fails Together, 2026-09-21
35. arXiv:2607.21909, Claim Plane, 2026-07-24
36. arXiv:2610.19292, Whose turn is it? Context-guided model routing, 2026-10-13
37. arXiv:2605.18859, TwinRouterBench, 2026-05-14
38. arXiv:2410.10934, Agent-as-a-Judge, 2024-10-14
39. arXiv:2606.21627, Counsel, 2026-06-19
40. arXiv:2511.21140, How to Correctly Report LLM-as-a-Judge Evaluations, 2025-11-26
41. arXiv:2604.22891, Quantifying and Mitigating Self-Preference Bias of LLM Judges, 2026-04-24
42. arXiv:2608.18091, Self- and Other-Labels Induce Bidirectional Bias in LLM Judges, 2026-06-06
43. arXiv:2607.28636, Chain-of-Models, 2026-05-19
44. arXiv:2507.10535, CodeJudgeBench, 2025-07-14
45. arXiv:2505.16222, Don't Judge Code by Its Cover, 2025-05-22
46. arXiv:2505.19477, Judging with Many Minds, 2025-05-26
