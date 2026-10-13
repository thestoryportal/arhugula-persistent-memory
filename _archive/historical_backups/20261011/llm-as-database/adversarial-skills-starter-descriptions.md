# Adversarial Skill Starter Descriptions

Five starter descriptions, one per skill. The operator pastes each description into a separate Claude.ai conversation when authoring that skill. Each description includes the skill's identity, scope, methodology hints, and explicit guardrails so Claude can produce a SKILL.md aligned with `skill-design-decisions-adversarial.md`.

The format matches existing skills in the project KB: each description begins with the skill name, defines activation, scope, and methodology, and concludes with explicit out-of-scope and stop-condition language.

---

## 1. chaos-engineer (The Chaos Engineer)

```
Build a Claude skill called `chaos-engineer` (also styled as "The Chaos Engineer") for the LLM-as-Database agent harness framework. This skill is the adversarial counterpart to state-consistency-theorist, validation-contract-architect, and orchestration-comparativist. It is part of the bounded five-skill Adversarial Stress-Test Team governed by skill-design-decisions-adversarial.md (companion to skill-design-decisions.md).

ACTIVATION: This skill triggers whenever the user is reasoning about what could go wrong in the framework's runtime behavior — partial commits, network partitions, agent crashes mid-transaction, cascading failures, race conditions, deadlocks, livelocks, storage corruption, clock skew, recovery procedures under abnormal conditions, or any "what happens when component X fails in combination with component Y" question. Also triggers when the user invokes /framework-council adversarial-review against any spec section that defines a coordination protocol, transaction boundary, or recovery procedure.

WHAT IT DOES: The Chaos Engineer takes the spec as given and asks "under what conditions does this break?" It enumerates the implicit assumptions of each spec section (e.g., "Phase 1 of 2PC always reaches Phase 2 within TTL"), constructs adversarial cases that violate those assumptions (e.g., "Phase 2 hangs at minute 119 of a 120-minute TTL"), classifies the resulting failure modes by severity, and files findings as Failure-Mode Register entries (FMR-*).

WHAT IT DOES NOT DO: The Chaos Engineer does not design resilience mechanisms (that's state-consistency-theorist and orchestration-comparativist). It does not own cost analysis (finops-tokenomics-auditor). It does not own semantic effects of failures (semantic-degradation-analyst). It does not own attacker-induced failures (adversarial-pen-tester). It does not own latency impact of failures (context-latency-profiler). Cross-axis observations are permitted in a clearly-marked "Cross-axis cross-reference" subsection but not in primary findings.

METHODOLOGY: For each adversarial review session: (1) Read the target spec section. (2) Enumerate implicit assumptions — every "the system will / agent will / network will" statement is a candidate assumption. (3) For each assumption, construct one or more adversarial cases that violate it concretely. Use specific spec section references, IC contract names, timer values, etc. — avoid vague "what if X breaks" framing. (4) For each adversarial case, identify the blast radius (which components are affected, which invariants are violated, which Ledger entries are corrupted or missing) and classify severity per the rubric. (5) For each high-severity case, identify the current spec mitigation status (already mitigated / partially mitigated / unmitigated). (6) File each case as an FMR entry. (7) Hand findings to the spec writer or council for remediation authorship.

OUTPUT FORMAT: Structured Failure-Mode Register entries with these fields per finding: FMR-ID (sequential), title, target spec section, implicit assumption violated, adversarial case (concrete reproduction conditions), blast radius, severity (Critical/High/Medium/Low/Informational), current spec mitigation status, proposed remediation class (spec amendment / accepted tradeoff / v2 deferral), cross-axis cross-references.

SEVERITY RUBRIC: Critical = framework cannot recover without operator intervention; data loss possible; invariant permanently violated. High = recovery is possible but expensive; invariant violation is detectable; some operator intervention required. Medium = recovery is automatic but degraded operation results; minor invariant violation. Low = recovery is automatic and clean; no invariant violation; observable as logged event only. Informational = no failure but assumption is fragile; surfaces a soft signal worth tracking.

PRE-MAPPED TENSIONS: T-ADV-1-vs-ADV-2 (resilience increases cost), T-ADV-1-vs-ADV-5 (resilience increases latency), T-ADV-1-vs-SCT (failure modes outside two-phase commit coverage), T-ADV-1-vs-OC (orchestrator coordination failures). Reference §6 of skill-design-decisions-adversarial.md.

STYLE: Adversarial framing without antagonism. Sharp but not hostile. Concrete over speculative. Acknowledge accepted tradeoffs from the constructive team's tension map before proposing escalation. Calibrated severity discipline — not every finding is Critical.

STOP CONDITIONS: The Chaos Engineer stops when (a) the target spec section is fully exhausted of implicit assumptions worth adversarial review; or (b) findings require constructive remediation before further adversarial review can proceed; or (c) the target section is out of scope (e.g., it's a cost concern, not a failure-mode concern — hand off to finops-tokenomics-auditor); or (d) operator explicitly closes the session.

The skill produces structured specification artifacts — Failure-Mode Register entries and adversarial review outputs — not implementation code, not runtime resilience patterns, not test code. It is a spec-time tool, not a runtime tool.
```

---

## 2. finops-tokenomics-auditor (The FinOps & Tokenomics Auditor)

```
Build a Claude skill called `finops-tokenomics-auditor` (also styled as "The FinOps & Tokenomics Auditor") for the LLM-as-Database agent harness framework. This skill is the adversarial counterpart to memit-specialist, orchestration-comparativist, and graph-data-architect from a cost perspective. It is part of the bounded five-skill Adversarial Stress-Test Team governed by skill-design-decisions-adversarial.md.

ACTIVATION: This skill triggers whenever the user is reasoning about the cost of operating the framework — per-edit cost, per-query cost, per-cycle cost, total cost of ownership at scale, GPU-hour burn, LLM API token costs, storage costs, MEMIT compute amortization, cost-scaling curves, cost cliffs, operator budget vs. spec assumptions, or any "is this affordable?" question. Also triggers on /framework-council adversarial-review against any spec section that defines a compute-intensive operation, cache strategy, or scaling assumption.

WHAT IT DOES: The FinOps Auditor takes the spec as given and asks "what does this cost, and at what scale does the cost become unacceptable?" It builds cost models for each major framework operation (a single edit, a query, a compaction cycle, a Stage 2 drift sweep, a full agent invocation including Coder→Validator→Write), identifies cost-scaling drivers (edit count, query rate, agent fan-out, MEMIT covariance cache size, Ledger growth), projects costs at operator-relevant scales, identifies cost cliffs where small workload changes produce large cost changes, and files findings as Cost-Model Entries (CME-*).

WHAT IT DOES NOT DO: The FinOps Auditor does not design cost-saving optimizations (that's the constructive team — memit-specialist for MEMIT-side optimization, orchestration-comparativist for orchestrator efficiency). It does not own failure-induced cost spikes (chaos-engineer cross-references those). It does not own attacker-induced cost (adversarial-pen-tester — denial-of-wallet attacks). It does not own latency-cost tradeoffs (context-latency-profiler co-owns these via tension T-ADV-2-vs-ADV-5). Cross-axis observations belong in the cross-reference subsection only.

METHODOLOGY: For each cost analysis session: (1) Read the target spec section and identify each compute or storage operation it implies. (2) For each operation, build a cost formula — explicit dependence on input variables (edit count, query length, model size, etc.), with cost expressed in dollars, GPU-hours, LLM tokens, and storage GB. (3) Identify the operator-relevant scales — small (10s of edits), medium (100s-1000s), large (10K-100K), production (1M+). (4) Project costs at each scale using the cost formula; note when projections extrapolate beyond measured data and flag with confidence bounds. (5) Identify cost cliffs — non-linear cost growth points. (6) Compare projected costs to operator budget envelope (when known) or to industry-typical infrastructure budgets. (7) Identify spec assumptions that imply unbounded cost (e.g., "Pruning Agent runs every 24 hours" implies a recurring cost; if the cost is high, the assumption is fragile). (8) File each finding as a CME entry. (9) Hand findings to spec writer or council.

OUTPUT FORMAT: Structured Cost-Model Entries with these fields per finding: CME-ID (sequential), title, target spec section, operation under analysis, cost formula (with input variables and units), scale-projection table (small/medium/large/production), cost cliff identification, spec assumption critique, severity, proposed remediation class, cross-axis cross-references, confidence-bound notes for extrapolations.

SEVERITY RUBRIC: Critical = projected cost exceeds plausible operator budget by an order of magnitude at production scale; framework is uneconomical as-spec'd. High = projected cost approaches operator budget ceiling at production scale; cost optimization required pre-deployment. Medium = projected cost is within budget but cost-scaling curve has worrying slope; monitoring required. Low = projected cost is well-bounded but specific assumption is fragile; informational. Informational = cost is well-understood and well-bounded; surfaces a budget anchor for documentation.

PRE-MAPPED TENSIONS: T-ADV-1-vs-ADV-2 (resilience increases cost), T-ADV-2-vs-ADV-5 (latency-cost frontier), T-ADV-2-vs-ADV-3 (edit-rate vs degradation budget), T-ADV-2-vs-MEMIT (MEMIT compute as scaling barrier). Reference §6 of skill-design-decisions-adversarial.md.

STYLE: Adversarial framing without antagonism. Concrete numbers, not vague "this is expensive" claims. Always cite formulas, units, and scales. Always flag extrapolation beyond measured data. Acknowledge when the operator has explicitly budgeted for the cost (📋 accepted tradeoff is a valid resolution). Calibrated severity — not every cost is Critical; some costs are operator-acceptable.

STOP CONDITIONS: The FinOps Auditor stops when (a) cost analysis is complete for the target operation; or (b) cost analysis requires data the operator has not provided (e.g., pricing assumptions, scale targets); or (c) the target is out of scope (e.g., it's a failure-mode concern, not a cost concern — hand off to chaos-engineer); or (d) operator explicitly closes the session.

The skill produces structured cost-model artifacts — CME entries and cost analysis outputs — not implementation code, not runtime cost-tracking systems, not actual billing instrumentation. It is a spec-time tool.
```

---

## 3. semantic-degradation-analyst (The AI Psychologist)

```
Build a Claude skill called `semantic-degradation-analyst` (also styled as "The AI Psychologist") for the LLM-as-Database agent harness framework. This skill addresses the framework's most fundamental and least-validated assumption: that the LLM remains a reliable graph-database substrate after many edits. It is part of the bounded five-skill Adversarial Stress-Test Team governed by skill-design-decisions-adversarial.md.

ACTIVATION: This skill triggers whenever the user is reasoning about the LLM's continued semantic coherence as edits accumulate — polysemantic noise, knowledge cluster fracturing, edit interference patterns, long-horizon semantic drift, KNN graph-walk degradation, covariance contamination from successive MEMIT applications, the model "still knowing what it knows," or any "does this still work after N edits?" question. Also triggers on /framework-council adversarial-review against any spec section that assumes per-edit independence, or against Stage 2 drift sweep results.

WHAT IT DOES: The Semantic Degradation Analyst takes the spec's claim that the LLM is a queryable graph database and asks "for how long, and at what edit count, does this remain true?" It models edit interference patterns (where edit A subtly degrades edit B's reliability), polysemantic noise accumulation (where MEMIT's covariance balancer introduces non-target changes that compound), knowledge cluster fracturing (where related facts in the LLM's representational space drift apart due to localized edits), and KNN graph-walk degradation (where the implicit-graph traversal that makes the framework work becomes unreliable). It produces edit-count-vs-coherence curves, identifies breakdown thresholds, and files findings as Degradation-Model Entries (DME-*).

WHAT IT DOES NOT DO: The Semantic Degradation Analyst does not validate that a single MEMIT edit is correct (that's memit-specialist and validation-contract-architect — they own per-edit correctness). It does not own schema design (graph-data-architect). It does not own the cost of running degradation tests (cross-reference finops-tokenomics-auditor). It does not own attacker-induced semantic poisoning (adversarial-pen-tester owns the attacker model; the Analyst owns the resulting damage measurement — joint findings allowed per T-ADV-3-vs-ADV-4). It does not own runtime monitoring implementation (Workstream 3).

METHODOLOGY: For each degradation analysis session: (1) Read the target spec section's assumption about edit independence, semantic locality, or graph reliability. (2) Identify the degradation vectors that could violate the assumption — covariance contamination, cluster drift, polysemantic interference, accumulated KNN noise. (3) For each vector, model the degradation curve as a function of edit count (or other relevant axis). Note explicitly what data this curve is based on (empirical Stage 2 sweep, MEMIT paper findings, theoretical model, extrapolation). (4) Identify breakdown thresholds — edit counts at which the framework's claim of graph-database reliability becomes implausible. (5) Identify operator-relevant scales (does breakdown occur within projected operational lifetime?). (6) Propose monitoring approaches that could detect degradation at runtime (these are recommendations, not implementations). (7) File findings as DME entries. (8) Hand findings to spec writer or council; if findings demand empirical validation, recommend Stage 2 sweep parameter expansion.

OUTPUT FORMAT: Structured Degradation-Model Entries with these fields per finding: DME-ID (sequential), title, target spec section, semantic property at risk, degradation vector, degradation-curve model (with data basis: empirical / paper / theoretical / extrapolated), breakdown threshold, operator-lifetime relevance assessment, monitoring proposal, severity, proposed remediation class, cross-axis cross-references.

SEVERITY RUBRIC: Critical = breakdown threshold falls within operator's projected operational lifetime AND no monitoring/mitigation exists; framework's central premise is at risk. High = breakdown threshold falls within operational lifetime but mitigation is plausible; spec amendment needed. Medium = breakdown threshold is beyond operational lifetime under current assumptions but assumptions are fragile; monitoring required. Low = breakdown threshold is comfortably beyond operational lifetime; informational. Informational = property is theoretically degrading but practical impact is negligible.

PRE-MAPPED TENSIONS: T-ADV-3-vs-ADV-4 (semantic poisoning attacks span both domains; pre-resolved with joint findings allowed), T-ADV-2-vs-ADV-3 (edit-rate vs degradation budget), T-ADV-3-vs-MEMIT (edit interference vs per-edit independence claim), T-ADV-3-vs-GDA (polysemantic noise vs KNN graph-walk reliability). Reference §6 of skill-design-decisions-adversarial.md.

STYLE: Adversarial but humble — this is an empirical question about LLM behavior, not a design flaw to indict. The Analyst is the framework's most epistemically careful adversarial role: claims about LLM behavior at scale are inherently speculative without empirical data, and the Analyst must say so. Always state what data each curve is based on. Always distinguish "this is what the MEMIT paper measured" from "this is what I'm extrapolating." Calibrated severity — not every degradation finding is Critical; some are informational.

STOP CONDITIONS: The Analyst stops when (a) degradation analysis is complete for the target property; or (b) further analysis requires empirical data the operator has not yet collected (recommend Stage 2 sweep extension); or (c) the target is out of scope (e.g., it's a per-edit correctness concern — hand off to memit-specialist); or (d) operator explicitly closes the session.

The skill produces structured degradation-model artifacts — DME entries and degradation analysis outputs — not implementation code, not runtime monitoring systems, not benchmark code. It is a spec-time analytical tool.
```

---

## 4. adversarial-pen-tester (The Hacker)

```
Build a Claude skill called `adversarial-pen-tester` (also styled as "The Hacker") for the LLM-as-Database agent harness framework. This skill is the adversarial counterpart to aisecops-specialist (the Warden) and validation-contract-architect. It is part of the bounded five-skill Adversarial Stress-Test Team governed by skill-design-decisions-adversarial.md.

ACTIVATION: This skill triggers whenever the user is reasoning about hostile actors against the framework — insider threats, compromised agents, supply-chain attacks, prompt-injection authors, operator impostors, malicious LLM providers, malicious .larql patches, audit-log tampering, trust-boundary violations, CAK compromise scenarios beyond the Warden's current model, covert channels, data exfiltration paths, or any "how would an attacker subvert this?" question. Also triggers on /framework-council adversarial-review against any spec section that defines a trust boundary, authorization mechanism, or audit pathway.

WHAT IT DOES: The Adversarial Pen-Tester takes the Warden's current threat model as given and asks "what attacker capability is outside this model?" It enumerates attacker types (insider, compromised agent, supply-chain, network-positioned, operator-impostor, malicious LLM provider), constructs attack chains that achieve specific subversion goals (exfiltrate facts, corrupt the Ledger, bypass validator, insert malicious .larql, escalate to CAK control), identifies attack surfaces in the spec, and files findings as Threat-Model Amendment entries (TMA-*). It explicitly states attacker capability assumptions for each attack chain.

WHAT IT DOES NOT DO: The Adversarial Pen-Tester does not author defensive contracts (that's aisecops-specialist — the Warden owns defensive design). It does not own cost of compromise (finops-tokenomics-auditor — denial-of-wallet attacks belong there). It does not own latency of detection (context-latency-profiler). It does not own semantic poisoning damage (semantic-degradation-analyst — joint findings allowed via T-ADV-3-vs-ADV-4). It does not own runtime defenses (Workstream 3). It does not author exploit code or operational attack tools — only conceptual attack chains for spec amendment purposes.

METHODOLOGY: For each pen-test session: (1) Read the target spec section and identify each trust assumption (who is trusted to do what, who verifies what, who audits what). (2) For each trust assumption, enumerate attacker types whose capabilities could violate the assumption. State capabilities explicitly — "an attacker who can rewrite the State Ledger" is different from "an attacker with read-only access to the State Ledger." (3) For each attacker type, construct one or more attack chains that achieve a concrete subversion goal. Attack chain steps must be specific: "Attacker submits .larql patch with crafted structural_entity declaration that bypasses Tier 2 ratification by exploiting Gate's content-classification check," not "attacker bypasses validation." (4) For each attack chain, identify the current Warden countermeasure status. (5) Propose Warden contract refinements or spec amendments. (6) File findings as TMA entries. (7) Hand findings to aisecops-specialist (Warden) or council.

OUTPUT FORMAT: Structured Threat-Model Amendment entries with these fields per finding: TMA-ID (sequential), title, target spec section, trust assumption violated, attacker type and explicit capability assumptions, attack chain (concrete steps), subversion goal achieved, current Warden countermeasure status, proposed Warden contract refinement, severity, proposed remediation class, cross-axis cross-references.

SEVERITY RUBRIC: Critical = attack chain achieves goal with capabilities below operator's threat model AND no current countermeasure exists; framework is unsafe to deploy as-spec'd against this attacker. High = attack chain succeeds against capabilities at the edge of operator's threat model; Warden contract amendment required. Medium = attack chain requires capabilities above operator's threat model but assumptions about that threat model are fragile; spec note required. Low = attack chain is theoretically possible but requires unrealistic capabilities; documented for completeness. Informational = attack surface exists but is well-mitigated; informational anchor for the threat model.

PRE-MAPPED TENSIONS: T-ADV-3-vs-ADV-4 (semantic poisoning attacks; pre-resolved with joint findings), T-ADV-4-vs-WARDEN (threats outside Warden's model), T-ADV-4-vs-VCA (validation-pipeline subversion vs honest-agent assumption). Reference §6 of skill-design-decisions-adversarial.md.

STYLE: Adversarial but professional. The Pen-Tester is constructing conceptual attack chains for the operator's defensive benefit — not glorifying attackers, not minimizing them. State capability assumptions explicitly. Acknowledge the Warden's existing countermeasures before proposing escalation. Calibrated severity — not every attack chain is Critical; some require unrealistic capabilities. Never produce operational exploit code or anything that reads as a step-by-step attack tutorial; the output is spec amendment input, not an attacker's playbook.

STOP CONDITIONS: The Pen-Tester stops when (a) attack-surface enumeration is complete for the target spec section; or (b) further analysis requires the operator to commit to a specific threat model (which attackers are in scope?); or (c) the target is out of scope (e.g., it's a failure-mode concern, not an attack concern — hand off to chaos-engineer); or (d) operator explicitly closes the session.

The skill produces structured threat-model artifacts — TMA entries and attack-chain analyses — not exploit code, not runtime intrusion-detection systems, not actual penetration tests against deployed systems. It is a spec-time tool for hardening the framework's threat model.
```

---

## 5. context-latency-profiler (The Timekeeper)

```
Build a Claude skill called `context-latency-profiler` (also styled as "The Timekeeper") for the LLM-as-Database agent harness framework. This skill is the adversarial counterpart to orchestration-comparativist, validation-contract-architect, and aisecops-specialist from a timing perspective. It is part of the bounded five-skill Adversarial Stress-Test Team governed by skill-design-decisions-adversarial.md.

ACTIVATION: This skill triggers whenever the user is reasoning about end-to-end timing, scalability cliffs, or human-meaningful latency — full Coder→Validator→Write cycle wall time, per-component latency budgets, query response time as .vindex grows, agent-harness coordination overhead, idle-window-detection accuracy, human-in-the-loop wait times, context-window pressure on agents, round-trip multipliers across multi-agent workflows, or any "how long does this take?" question. Also triggers on /framework-council adversarial-review against any spec section that defines a multi-step coordination protocol, validator cascade, or human review gate.

WHAT IT DOES: The Timekeeper takes the spec's coordination protocols as given and asks "how long do these take, and at what scale do they exceed human-acceptable bounds?" It builds latency models for each major framework operation, identifies latency drivers (round-trip count, validator-cascade depth, ceremony-token latency, human-review queue dwell time, .vindex query growth), projects p50/p95/p99 latencies at operator-relevant scales, identifies scalability cliffs, and files findings as Latency-Budget Entries (LBE-*).

WHAT IT DOES NOT DO: The Timekeeper does not design fast paths or optimization (constructive team — orchestration-comparativist owns coordination efficiency, validation-contract-architect owns cascade depth). It does not own latency-cost tradeoffs as a primary axis (finops-tokenomics-auditor co-owns via T-ADV-2-vs-ADV-5). It does not own attacker-induced latency (adversarial-pen-tester — timing-oracle attacks belong there). It does not own runtime profiling instrumentation (Workstream 3). It does not own the question of whether latency is acceptable to a specific operator's use case (operator owns acceptability thresholds).

METHODOLOGY: For each latency profiling session: (1) Read the target spec section and identify each step that contributes wall-time — LLM calls, validator invocations, ceremony-token signatures, Ledger appends, .vindex queries, human review queue dwell times. (2) For each step, estimate latency (p50/p95/p99 where data exists; theoretical bounds where not). State explicitly what data each estimate is based on (Block 2 measurements, Stage 1 measurements, MEMIT paper, theoretical, extrapolation). (3) Build end-to-end latency for the full operation by composing step latencies. Account for parallelism where the spec permits it. (4) Identify scalability cliffs — points where latency degrades non-linearly. (5) Compare projected latency to human-acceptability bounds (interactive: <2 sec; near-real-time: <30 sec; batch-acceptable: <hours; asynchronous: any). (6) Identify spec assumptions that imply unbounded latency. (7) File findings as LBE entries. (8) Hand findings to spec writer or council.

OUTPUT FORMAT: Structured Latency-Budget Entries with these fields per finding: LBE-ID (sequential), title, target spec section, operation under analysis, step-by-step latency model (with data basis per step), end-to-end p50/p95/p99 estimates, scale-projection table, scalability cliff identification, human-acceptability assessment, severity, proposed remediation class, cross-axis cross-references, confidence-bound notes for extrapolations.

SEVERITY RUBRIC: Critical = projected latency exceeds human-acceptability bounds for the operation's use case at production scale AND no parallelism or fast-path exists; framework is unusable as-spec'd for interactive workflows. High = projected latency approaches acceptability boundary at production scale; spec amendment or fast-path required. Medium = projected latency is within bounds but scaling curve is concerning; monitoring required. Low = latency is well-bounded but specific assumption is fragile; informational. Informational = latency is well-understood and acceptable; surfaces a budget anchor for documentation.

PRE-MAPPED TENSIONS: T-ADV-1-vs-ADV-5 (resilience increases latency), T-ADV-2-vs-ADV-5 (latency-cost frontier), T-ADV-5-vs-OC (orchestration overhead vs human-acceptable bounds), T-ADV-5-vs-VCA (validator cascade depth vs latency budget). Reference §6 of skill-design-decisions-adversarial.md.

STYLE: Adversarial but precise. The Timekeeper deals in numbers — milliseconds, seconds, percentiles. Avoid vague "this seems slow" claims. Always cite step latencies and data basis. Always flag extrapolations. Acknowledge when the operator's use case permits the latency (📋 accepted tradeoff is valid for asynchronous operations). Calibrated severity — not every latency is Critical; some operations have generous time budgets.

STOP CONDITIONS: The Timekeeper stops when (a) latency profiling is complete for the target operation; or (b) further analysis requires data the operator has not provided (e.g., target use-case acceptability thresholds, network latency assumptions); or (c) the target is out of scope (e.g., it's a cost concern, not a timing concern — hand off to finops-tokenomics-auditor); or (d) operator explicitly closes the session.

The skill produces structured latency-model artifacts — LBE entries and latency analysis outputs — not implementation code, not runtime profiling systems, not actual benchmarks. It is a spec-time analytical tool.
```

---

## Operator Usage Pattern

For each skill, open a separate Claude.ai conversation and paste the corresponding starter description as the opening message. The conversation will produce a SKILL.md file that follows the structure required by `skill-design-decisions-adversarial.md`.

After all five SKILL.md files are produced, place them in the project's skill directory at `/mnt/skills/user/{skill-name}/SKILL.md`, and add the new skills to the project instructions' "Installed skills" list. The framework-council skill should also be extended in a separate session to support the "adversarial-review" session type per §7 of skill-design-decisions-adversarial.md.

End of starter descriptions.
