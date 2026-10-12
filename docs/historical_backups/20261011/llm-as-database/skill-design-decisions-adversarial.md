# skill-design-decisions-adversarial.md

Companion to `skill-design-decisions.md`. Governs the design, ownership boundaries, tension structure, and modification rules for the **Adversarial Stress-Test Team** introduced for Workstream 1.5 (Chaos & Economics Phase). Existing constructive skills (validation-contract-architect, state-consistency-theorist, aiSecOps-specialist, memit-specialist, graph-data-architect, orchestration-comparativist, framework-council, framework-spec-writer) remain governed by `skill-design-decisions.md` and are unaffected by this document except where pre-mapped tensions explicitly cross the boundary.

---

## 1. Purpose of the Adversarial Team

The constructive skills ask: *what must the framework do, guarantee, enforce?* They produce contracts, invariants, and spec blocks. They are biased toward feasibility; their failure mode is over-specifying happy paths and under-specifying breakage.

The adversarial skills ask the inverse: *under what conditions does the framework fail, become uneconomical, lose semantic coherence, get compromised, or exceed acceptable latency?* They produce failure-mode registers, cost-bound surfaces, drift-accumulation models, threat refinements, and latency budgets. Their failure mode is over-pessimism (declaring the framework non-viable on speculative grounds) and proposing remediation that is operator-impractical.

The team is sized at **five** specialists, each owning one stress axis. The team is intentionally bounded; sixth-and-beyond axes are out of scope unless the operator authorizes a v2 adversarial-team expansion.

| ID | Skill | Stress axis |
|---|---|---|
| ADV-1 | chaos-engineer | Component failure under unexpected combinations |
| ADV-2 | finops-tokenomics-auditor | Cost and resource economics at scale |
| ADV-3 | semantic-degradation-analyst | Polysemantic noise, knowledge cluster fracturing, edit interference |
| ADV-4 | adversarial-pen-tester | Hostile actors, attack surfaces, trust subversion |
| ADV-5 | context-latency-profiler | End-to-end timing, scalability cliffs, human-meaningful latency |

---

## 2. Why a Separate Adversarial Team Rather Than Augmenting Existing Skills

### 2.1 Constructive vs. adversarial perspectives are structurally different

A skill that holds both perspectives at once tends to soften adversarial findings to maintain its own constructive recommendations, or vice versa. Empirically the framework already exhibits this: `state-consistency-theorist` proposes the two-phase commit; without an external adversarial counterpart, no skill is structurally positioned to ask *what happens when Phase 1 succeeds and Phase 2 hangs forever?* The Theorist could ask this question, but the role's primary commitment is to design the protocol that makes such failures rare. Asking "rare enough?" is a different role.

### 2.2 Pre-mapped tension is the integration mechanism

Adversarial skills are not designed to "win" arguments with constructive skills. They are designed to surface tensions that the framework should resolve via spec amendment, accepted-tradeoff documentation, or v2 routing. Tensions between ADV-* skills and the constructive team are pre-mapped in §6 of this document. New tensions surfaced during sessions are tracked using the existing tension-map register.

### 2.3 Skill independence preserves session integrity

Adversarial skills do not depend on each other for findings. Each can run a session independently against the spec. Findings may overlap (e.g., a Chaos Engineer failure mode that creates a FinOps cost spike), but the skills do not co-author conclusions; they file findings separately and the spec writer or council synthesizes.

---

## 3. Ownership Boundaries

Each adversarial skill owns one stress axis exclusively. Crossing the boundary into another skill's axis is forbidden in primary findings, though acknowledgment of cross-axis implications is permitted in cross-references.

### 3.1 chaos-engineer — failure-mode ownership

**Owns:** Component-level and system-level failure modes; partial commits; network partitions; agent crashes mid-transaction; storage corruption; clock skew; race conditions; deadlocks; livelocks; cascade failures; recovery procedures; failure-injection methodology.

**Does NOT own:** Cost analysis (ADV-2); semantic effects (ADV-3); attacker models (ADV-4); latency impact of failures (ADV-5); the *design* of resilience mechanisms (constructive team — state-consistency-theorist, orchestration-comparativist).

**Output class:** Failure-mode register entries (FMR-*) with reproduction conditions, blast radius, current spec mitigation status, and severity classification.

### 3.2 finops-tokenomics-auditor — economic-model ownership

**Owns:** Per-operation token costs (LLM API, MEMIT compute, storage); GPU-hour burn rates; cost amortization across cache lifecycles; total cost of ownership (TCO) projections; cost-per-edit, cost-per-query, cost-per-cycle metrics; cost-scaling curves vs. edit count, query rate, agent fan-out; cost cliff identification (where small workload changes produce large cost changes); operator budget envelope vs. spec assumptions.

**Does NOT own:** Whether failures cause cost spikes (cross-reference ADV-1); whether attackers can induce cost (cross-reference ADV-4); latency-cost tradeoffs (cross-reference ADV-5); cost-of-correctness (constructive team).

**Output class:** Cost-model entries (CME-*) with formula, input variables, sensitivity analysis, and budget-bound assertions.

### 3.3 semantic-degradation-analyst — knowledge-coherence ownership

**Owns:** Polysemantic noise accumulation across edit sequences; knowledge cluster fracturing; edit interference patterns; long-horizon semantic drift; the LLM's continued reliability as a graph-database substrate after N edits; KNN-graph-walk degradation; covariance contamination from successive MEMIT applications; the model's ability to "still know what it knows" as a measurable property.

**Does NOT own:** Whether MEMIT correctly applies a single edit (constructive team — memit-specialist, validation-contract-architect); whether the schema is well-formed (graph-data-architect); whether cost grows with edit count (cross-reference ADV-2); whether attackers exploit semantic drift (cross-reference ADV-4).

**Output class:** Degradation-model entries (DME-*) with edit-count-vs-coherence curves, breakdown thresholds, monitoring proposals, and graceful-degradation requirements.

### 3.4 adversarial-pen-tester — threat-model ownership

**Owns:** Attacker models (insider, compromised agent, supply-chain, prompt-injection-author, operator-impostor, malicious LLM provider); attack surfaces; subversion paths; audit-log tampering; trust-boundary violations; malicious `.larql` patches; CAK compromise scenarios beyond the Warden's current model; covert channel risks; data exfiltration paths.

**Does NOT own:** Defensive contracts (constructive — aisecops-specialist / Warden owns these); cost of compromise (cross-reference ADV-2); latency of detection (cross-reference ADV-5); semantic poisoning is shared with ADV-3 (see §6 tension T-ADV-3-vs-ADV-4).

**Output class:** Threat-model amendments (TMA-*) with attacker capability assumptions, attack chain, current spec countermeasure status, and proposed Warden-contract refinements.

### 3.5 context-latency-profiler — timing-model ownership

**Owns:** End-to-end latency for full Coder→Validator→Write cycles; per-component latency budgets; query response time as `.vindex` grows; agent-harness coordination overhead; idle-window-detection accuracy; human-in-the-loop wait times; scalability cliffs (where latency degrades non-linearly); context-window pressure on agents; round-trip multipliers across multi-agent workflows.

**Does NOT own:** Whether latency causes incorrectness (constructive team); whether latency causes cost (cross-reference ADV-2); whether attackers exploit timing (cross-reference ADV-4 — timing oracles); whether failures cause latency (cross-reference ADV-1).

**Output class:** Latency-budget entries (LBE-*) with measured/estimated p50/p95/p99 latencies, budget violations, scalability projections, and human-acceptability bounds.

---

## 4. Skill Authorship Conventions

Each adversarial skill MUST follow the existing skill structure to integrate cleanly with the framework-council mechanism and the spec writer's output pipeline.

### 4.1 Required SKILL.md sections

Each skill's `SKILL.md` MUST contain these sections in the following order:

1. **`# {Skill Name}`** — H1 heading with the skill's full name and "(The {Persona Title})" subtitle for human readability.
2. **Activation triggers** — Bullet list of phrases or conditions that should activate this skill. Used by the operator to know when to invoke and by Claude to recognize relevance during framework-council sessions.
3. **What this skill does** — One paragraph (3-5 sentences) describing the role, distinct from constructive skills, with explicit "produces ... not ..." disclaimers.
4. **What this skill does NOT do** — Bullet list of out-of-scope concerns, each with cross-reference to the skill that owns it.
5. **Methodology** — Numbered list of how the skill conducts an adversarial review (e.g., "1. Read the spec section under review. 2. Enumerate assumptions implicit in the section. 3. For each assumption, construct an adversarial case violating it. 4. Classify each adversarial case by severity. 5. Propose remediation.").
6. **Output format** — Specification of the structured findings the skill emits (FMR-*, CME-*, DME-*, TMA-*, or LBE- with field definitions).
7. **Severity classification** — Rubric for how the skill rates findings (e.g., Critical / High / Medium / Low / Informational, with explicit criteria for each).
8. **Pre-mapped tensions** — Reference to §6 of this document with the tension IDs the skill participates in.
9. **Stop conditions** — When the skill declines to continue (out of scope; insufficient information; constructive remediation needed before further adversarial review can proceed).

### 4.2 Style requirements

- **Adversarial framing without antagonism.** Skills should be sharp but not hostile. The goal is finding real failure modes, not winning rhetorical points against constructive skills.
- **Concrete over speculative.** Adversarial cases should reference specific spec sections, IC contracts, or invariants. "What if the network is unreliable?" is too vague; "What happens when Phase 2 of the IC-2PC commit times out at minute 119 of a 120-minute TTL?" is the right granularity.
- **Acknowledge accepted tradeoffs.** When the constructive team has knowingly accepted a risk (📋 in the tension map), the adversarial skill should note the existing acceptance before proposing escalation. "T-S-RP-1 already accepts dry-run-store ownership as operator-side; my finding extends this to ..." is correct framing.
- **Severity discipline.** Calibrated severity ratings prevent finding inflation. A skill that declares everything Critical loses operator trust.

### 4.3 Forbidden patterns

- **Cross-axis findings in primary output.** The chaos-engineer cannot file a Cost finding. Cross-axis observations belong in a separate "Cross-axis cross-reference" subsection that explicitly hands off to the appropriate owner.
- **Constructive remediation as primary output.** Adversarial skills surface findings; they do not author the fixes. "Operator should ..." or "Spec amendment should ..." may appear as suggestions, but the canonical authorship of remediation is the constructive team's spec writer or council.
- **Speculative attacker capabilities.** Adversarial-pen-tester findings must state attacker capability assumptions explicitly. "An attacker who can rewrite the State Ledger" is a different threat from "An attacker with read-only access to the State Ledger." Both are valid; conflating them is not.
- **Linear projections beyond data.** FinOps and Latency findings must explicitly note when projections extrapolate beyond measured ranges. "Cost grows linearly to 1M edits" is acceptable if the largest measurement is at 10K edits AND the extrapolation is flagged with confidence bounds.

---

## 5. Adversarial Session Structure

### 5.1 Single-skill adversarial session

```
Session opens
  └── Operator invokes skill (e.g., /chaos-engineer)
  └── Skill reads target spec section(s)
  └── Skill enumerates assumptions
  └── Skill constructs adversarial cases per methodology §4.1.5
  └── Skill files findings in standard output format
  └── Skill's findings handed to spec writer or council
Session closes
```

### 5.2 Adversarial-vs-constructive council session

The framework-council skill is extended (per §7 below) to support adversarial-vs-constructive sessions. In these sessions, an adversarial skill files a finding and the corresponding constructive skill responds with one of:

| Response | Effect |
|---|---|
| Accept finding; spec amendment required | Spec writer drafts amendment cluster; finding closes on amendment ratification |
| Accept finding; mitigation already in spec | Adversarial skill verifies; finding closes if mitigation matches; otherwise re-escalates |
| Accept finding as informational tradeoff | 📋 entry in tension map; finding closes with documented acceptance |
| Reject finding as out-of-scope speculation | Adversarial skill either provides additional evidence or withdraws |
| Defer to v2 | 🔴 entry in tension map; finding remains open against v2 |

Council session output: tension-map updates, spec amendment proposals, or accepted-tradeoff entries. Council session does NOT produce remediation code or runtime artifacts.

### 5.3 Multi-adversarial concurrent session

The framework-council can invoke multiple adversarial skills concurrently against a single target (e.g., "review the IC-2PC contract from chaos, finops, and latency angles simultaneously"). Findings from each axis remain segregated by output class; cross-axis observations are pre-mapped per §6.

---

## 6. Pre-Mapped Tensions

These are the tensions the adversarial team is expected to surface or participate in. Each is listed with the skills involved, the constructive counterpart most likely to be in dialogue, and an initial disposition. New tensions discovered during sessions are added to this register using the same notation as the v1.2 cross-domain tension register (T-ID format).

### 6.1 Adversarial-internal tensions (between adversarial skills)

| Tension ID | Description | Skills involved | Resolution path |
|---|---|---|---|
| T-ADV-1-vs-ADV-2 | Resilience mechanisms increase cost. Chaos Engineer wants more retries, redundancy, dual-store; FinOps Auditor wants fewer | ADV-1 + ADV-2 | Council to set resilience-budget tradeoff explicitly |
| T-ADV-1-vs-ADV-5 | Resilience mechanisms increase latency. More retries = longer wall time | ADV-1 + ADV-5 | Council to set resilience-latency budget |
| T-ADV-3-vs-ADV-4 | Semantic poisoning attacks span both domains. Are they ADV-3 (degradation-by-malicious-edit) or ADV-4 (attack-via-edit)? | ADV-3 + ADV-4 | Pre-resolved: ADV-4 owns the attacker model and intent; ADV-3 owns the resulting semantic damage. Joint findings allowed |
| T-ADV-2-vs-ADV-5 | Faster usually means more compute (parallelism, prefetch). Cheaper means less | ADV-2 + ADV-5 | Council to set per-operation latency-cost frontier |
| T-ADV-2-vs-ADV-3 | More edits per session improves operator throughput economics; more edits accelerate semantic degradation | ADV-2 + ADV-3 | Council to set edit-rate budget vs. degradation-tolerance |

### 6.2 Adversarial-vs-constructive tensions (cross-team)

| Tension ID | Description | Skills involved | Resolution path |
|---|---|---|---|
| T-ADV-1-vs-SCT | Chaos Engineer surfaces failure modes the State Consistency Theorist's two-phase commit doesn't fully cover | ADV-1 + SCT | Spec amendment OR documented accepted tradeoff |
| T-ADV-1-vs-OC | Chaos Engineer surfaces orchestrator-coordination failures; Orchestration Comparativist's path selection assumes happy-path coordination | ADV-1 + OC | Resolves at GAP-4 path selection time |
| T-ADV-2-vs-MEMIT | FinOps Auditor surfaces MEMIT compute cost as a scaling barrier; MEMIT Specialist's covariance cache amortization assumes operator can pay | ADV-2 + MEMIT | Spec amendment to bound MEMIT operations OR documented operator-budget assumption |
| T-ADV-3-vs-MEMIT | Semantic Degradation Analyst surfaces edit-interference patterns; MEMIT Specialist's edit isolation contract assumes per-edit independence | ADV-3 + MEMIT | Empirical (Stage 2 sweep) + spec amendment if confirmed |
| T-ADV-3-vs-GDA | Semantic Degradation Analyst surfaces polysemantic noise; Graph Data Architect's KNN graph-walk inference assumes manageable polysemy | ADV-3 + GDA | Spec amendment on graph-walk reliability bounds |
| T-ADV-4-vs-WARDEN | Adversarial Pen-Tester surfaces threats outside Warden's current model | ADV-4 + AISecOps (Warden) | Warden contract amendment OR documented risk acceptance |
| T-ADV-4-vs-VCA | Adversarial Pen-Tester surfaces validation-pipeline subversion paths; Validation Contract Architect's Reflexion loop assumes honest agents | ADV-4 + VCA | Spec amendment on validator independence |
| T-ADV-5-vs-OC | Context-Latency Profiler surfaces orchestration overhead exceeding human-acceptable bounds | ADV-5 + OC | Resolves at GAP-4 path selection time; or spec amendment on latency budget |
| T-ADV-5-vs-VCA | Latency Profiler surfaces validator-cascade depth exceeding latency budget | ADV-5 + VCA | Spec amendment to bound validator cascade or accept latency cost |

### 6.3 Pre-mapped acceptance posture

Some adversarial findings are expected to be resolved as 📋 Accepted rather than via amendment. Operators should not feel pressure to amend the spec for every finding; principled acceptance (with documented reasoning) is a valid resolution. Candidates likely to be 📋:

- Cost findings where operator budget genuinely permits the cost (FinOps reports the truth, operator accepts).
- Latency findings where the operation is asynchronous and human-meaningful latency is not a constraint.
- Threat findings where the attacker capability is below operator's threat model (e.g., nation-state attackers may be out of scope for a specific deployment).
- Degradation findings where the edit count required to reach the breakdown threshold exceeds the operator's projected operational lifetime.

---

## 7. Council Integration

The framework-council skill is extended (in its own SKILL.md) to support adversarial review modes:

### 7.1 Adversarial review session type

The council supports a new session type: **Adversarial Review**. Invoked by `/framework-council adversarial-review {target_spec_section}`. The council facilitator:

1. Identifies which adversarial skill(s) own the relevant stress axis.
2. Invokes those skills against the target.
3. Identifies the constructive counterpart skill(s) most likely involved in tensions per §6.
4. Facilitates dialogue per §5.2.
5. Produces structured output per the standard council output convention plus the adversarial-output classes (FMR/CME/DME/TMA/LBE).

### 7.2 Multi-axis review

For sections that span multiple stress axes, the council can invoke multiple adversarial skills concurrently. Output is segregated by axis but a synthesis section identifies cross-axis implications.

### 7.3 Adversarial review is bounded

A council session is not a full Workstream 1.5 phase. The phase-level structure (per §8 of this document) is owned by the operator's session-planning workflow, not by the council itself.

---

## 8. Workstream 1.5 Phase Structure

The Adversarial Stress-Test team is purpose-built for Workstream 1.5, which sits between Workstream 1 closure (Stage 4 POC packet acceptance) and Workstream 3 implementation planning entry. The phase structure:

```
                ┌──────────────────────────────────────────────┐
                │ Pre-condition: Workstream 1 Stage 4 PASS     │
                │ Spec version: v1.2 (sealed)                  │
                └────────────────────┬─────────────────────────┘
                                     │
                ┌────────────────────▼─────────────────────────┐
                │ Session 1.5.1   Skill authorship: ADV-1..5   │
                │   Output: 5 SKILL.md files                   │
                │   Council extension: adversarial review type │
                │   Estimated wall time: 1 session             │
                └────────────────────┬─────────────────────────┘
                                     │
                ┌────────────────────▼─────────────────────────┐
                │ Session 1.5.2   Chaos Engineer adversarial   │
                │   pass against v1.2                          │
                │   Output: FMR register                       │
                └────────────────────┬─────────────────────────┘
                                     │
                ┌────────────────────▼─────────────────────────┐
                │ Session 1.5.3   FinOps Auditor adversarial   │
                │   pass against v1.2                          │
                │   Output: CME register                       │
                └────────────────────┬─────────────────────────┘
                                     │
                ┌────────────────────▼─────────────────────────┐
                │ Session 1.5.4   Semantic Degradation Analyst │
                │   adversarial pass against v1.2 + Stage 2    │
                │   sweep results                              │
                │   Output: DME register                       │
                └────────────────────┬─────────────────────────┘
                                     │
                ┌────────────────────▼─────────────────────────┐
                │ Session 1.5.5   Adversarial Pen-Tester pass  │
                │   against v1.2 + Warden contract             │
                │   Output: TMA register                       │
                └────────────────────┬─────────────────────────┘
                                     │
                ┌────────────────────▼─────────────────────────┐
                │ Session 1.5.6   Context-Latency Profiler     │
                │   pass against v1.2                          │
                │   Output: LBE register                       │
                └────────────────────┬─────────────────────────┘
                                     │
                ┌────────────────────▼─────────────────────────┐
                │ Session 1.5.7   Synthesis council session    │
                │   Cross-axis tension resolution              │
                │   Output: spec v1.3 amendment cluster OR     │
                │   accepted-tradeoff register                 │
                └────────────────────┬─────────────────────────┘
                                     │
                ┌────────────────────▼─────────────────────────┐
                │ Workstream 1.5 closure                       │
                │ Authorize Workstream 3 entry                 │
                └──────────────────────────────────────────────┘
```

Estimated total: 7 sessions. Compress to 5-6 if findings are minimal in any axis. Expand to 8-10 if Stage 2 sweep reveals empirical degradation patterns that demand deeper Semantic-Degradation analysis.

### 8.1 Mid-Workstream-3 light-touch reviews

After Workstream 1.5 closes, adversarial skills remain available for invocation during Workstream 3 implementation milestones. Each major component completion (Transaction Controller, Pruning Agent, Validator pipeline, etc.) should trigger a focused adversarial review by the relevant skill(s). These are NOT full Workstream-1.5-style passes; they are targeted reviews scoped to the new component.

---

## 9. Skill Modification Rules

The adversarial team is bounded at five skills. Modifications follow these rules:

### 9.1 Authorized modifications

Permitted at any time without operator escalation:

- Methodology refinement within an existing skill (e.g., improving how chaos-engineer enumerates assumptions).
- Output format additions (new fields in FMR/CME/etc.) that are backward-compatible.
- Severity rubric refinement (e.g., adding sub-criteria to "Critical").
- Pre-mapped tension additions (new tensions discovered during sessions are appended to §6).

### 9.2 Operator-escalation modifications

Require explicit operator authorization:

- Adding a sixth (or beyond) adversarial skill. The team is bounded at five for a reason: skill proliferation dilutes per-skill ownership and makes council sessions unwieldy.
- Removing an adversarial skill (e.g., merging ADV-3 into ADV-4 or vice versa).
- Renaming an existing skill in a way that changes its scope.
- Merging skill responsibilities across the constructive/adversarial boundary.

### 9.3 Forbidden modifications

- Changing the team's mandate from "adversarial review" to "implementation review" (the latter is Workstream 3's job, not the adversarial team's).
- Authorizing adversarial skills to author remediation as primary output (violates §4.3).
- Extending the adversarial team into runtime monitoring (the adversarial team is a *spec-time* tool; runtime monitoring is a Workstream 3 component).
- Allowing adversarial skills to gate Workstream 1 stage transitions (Workstream 1 is bounded by its own stage criteria; adversarial review is a separate phase).

### 9.4 Skill retirement

If an adversarial skill is judged unnecessary after Workstream 1.5 closes (e.g., the skill produced zero findings worth amending), the operator may retire it. Retirement is documented in `skill-design-decisions-adversarial.md` itself (this document) with a rationale. Retired skills remain in the project history and can be reactivated if a future workstream surfaces relevance.

---

## 10. Relationship to skill-design-decisions.md

This document is a companion, not a replacement. The constructive team's design rules in `skill-design-decisions.md` remain authoritative for those skills. Where the two documents disagree, the disagreement is itself a tension to be resolved (likely indicating that the boundary between teams has shifted and one or both documents need amendment).

### 10.1 Consistency requirements

Both documents share the following invariants:

- Single-domain ownership per skill.
- Pre-mapped tensions documented in advance.
- Skill output uses structured registers, not freeform prose.
- Skills do not produce runtime code or runtime artifacts.
- Skills are invoked by `/skill-name` syntax and integrate with framework-council.

### 10.2 Documented divergences

The adversarial team diverges from the constructive team's conventions in these specific ways:

- **Authorship class.** Adversarial skills file findings; they do not author spec amendments. Constructive skills both file recommendations and contribute to spec authorship.
- **Severity rubric requirement.** Adversarial skills MUST have a severity rubric; constructive skills typically do not.
- **Pre-mapped opposition.** Adversarial skills are designed with explicit tensions against constructive counterparts. Constructive skills have tensions against each other but not designed-in opposition.

These divergences are deliberate and reflect the different role of the adversarial team.

---

## 11. Verification of This Document

Before any adversarial skill is authored, the operator should:

1. Read this document end-to-end.
2. Read `skill-design-decisions.md` (the constructive companion).
3. Confirm the team mandate (5 skills, bounded, advisory-not-authoritative).
4. Confirm the Workstream 1.5 phase structure (per §8).
5. Confirm pre-mapped tensions (per §6) align with the operator's mental model of the framework.

If any of the above confirmations fail, the operator should either amend this document or defer adversarial team authorship until the design is settled.

---

## 12. Closure

This document seals at v1.0 upon operator review. Subsequent versions track via standard semver: minor versions for §6 tension-register additions and §4 methodology refinement; major versions for team-size changes or mandate revisions.

Authored: 2026-04-28 (Session 2.3 close handoff)
Companion to: `skill-design-decisions.md`
Governs: chaos-engineer, finops-tokenomics-auditor, semantic-degradation-analyst, adversarial-pen-tester, context-latency-profiler

End of document.
