# LLM as Database: Agent Harness Architecture
## Gap Backlog v1.0

> **Source document:** `llm-as-database-v1_0-integrated-spec.md` (v1.0 Integrated Specification)
> **Session:** Framework Council — Post-Session 7 Gap Analysis
> **Scope:** All locations in the integrated spec containing TBD language, undecided approaches,
> undefined interface contracts, unresolved tensions, explicitly deferred open questions,
> or decisions marked as requiring implementation experience.
> **Total gaps identified:** 19 — 3 Critical, 5 High, 7 Medium, 4 Low

---

## Priority Definitions

| Priority | Criteria |
|----------|----------|
| **Critical** | Blocks 3 or more other gaps |
| **High** | Blocks 1–2 other gaps or is a load-bearing architectural decision |
| **Medium** | Self-contained gap with no downstream spec dependencies |
| **Low** | Refinement detail; does not affect other components |

---

## 🔴 Critical — Blocks 3 or More Other Gaps

---

### GAP-1

**Domain(s):** MEMIT Specialist

**Description:** All drift-from-anchor and compaction threshold values are provisionally
specified but empirically unvalidated. This includes:

- Drift warning: 1,500 edges since last anchor (§11.14, §8.7)
- Drift hard trigger: 8,000 edges (§11.14)
- MEMIT internal sub-batch ceiling: 2,000 edges (§8.8)
- Overlay file count trigger: 50+ files (§11.14)
- p95 inference latency trigger: 2× baseline (§11.14)
- `stale_urgent` backpressure ceiling: 1,000 edges (§11.12)
- 24-hour Pruning floor (§17.5) — rationale is architectural, but the floor value is heuristic

The spec marks all of these with "provisional pending empirical validation against target
model" (OQ-W1). They propagate into circuit-breaker logic, compaction scheduling, Pruning
backpressure, and write engine capacity planning.

**Blocked by:** Target model selection + at least one implementation-phase write volume stress
test against that model's FFN architecture.

**Blocks:**
- GAP-5 (OQ-OC3: compaction verification sample size cannot be tuned until compaction
  frequency is empirically understood)
- Concrete backpressure policy (the 1,000 `stale_urgent` cap appears in multiple spec
  sections and is unjustified without a write-volume baseline)
- Meaningful circuit-breaker threshold rationale (current values are starting heuristics
  with no anchor in model behavior data)
- Any write-budget SLA spec for real task volumes

**Priority:** 🔴 Critical

---

### GAP-2

**Domain(s):** MEMIT Specialist

**Description:** MEMIT's compatibility with the target model architecture has not been
verified (OQ-W2). The spec designates MEMIT as the write engine (D12) and specifies that
it targets middle-to-late FFN layers — L15–L25 for a 32-layer model (§8.2, C15). These
layer coordinates are not universal constants; they are specific to the architectural depth
and attention-head configuration of the target model. If the target model has a different
layer count, different FFN width, or uses an architecture variant (e.g., MoE, Mamba-family,
grouped-query attention) that MEMIT's covariance-update math does not model correctly, the
entire write engine spec is built on an unverified assumption.

Two downstream claims are also contingent on this:

- The orthogonal projection and covariance balancer safeguards (D20, §8.2) assume MEMIT's
  mathematical guarantees hold for the chosen architecture.
- The `declared_importance` ↔ `attention_weight` divergence check thresholds (0.5 and 0.9
  in §8.6) are calibrated against MEMIT's expected output distribution. If the architecture
  changes how MEMIT computes weights, these thresholds lose meaning.

**Blocked by:** Explicit target model specification + MEMIT compatibility test run on that
model. The spec intentionally omits model selection (see Appendix A), but some specification
work cannot proceed until the model family is known.

**Blocks:**
- Layer targeting spec correctness (the L15–L25 range is a placeholder)
- Edge cap justification (security caps of 500/10,000 are authoritative; the MEMIT-recommended
  2,000 sub-batch is derived from MEMIT behavior on unspecified architecture)
- GAP-1 resolution (all drift thresholds are model-architecture-dependent)
- The `attention_weight` divergence check (§8.6) being meaningful

**Priority:** 🔴 Critical

---

### GAP-3

**Domain(s):** MEMIT Specialist, Graph Data Architect

**Description:** The `.larql` schema versioning strategy is deferred to v2 (OQ-W6, §18.3).
The spec notes that "the v1 → v2 migration path has its first-use case via the T1 `.larql`
format change" — meaning the Session 7 decision to split `attention_weight` into a two-number
model (T1) already represents a schema version change to the `.larql` patch format. The spec
does not define:

- How the Validator handles `.larql` patches authored under an older schema version than
  the current spec.
- Whether `.larql` patches carry a schema version header field, and if so, what the Gate
  and Validator do when the declared version does not match the current active version.
- How the superseded-patch archive (§8.10) handles patches from prior schema versions during
  compaction (the full MEMIT re-run strategy requires re-parsing old patches).
- The migration path for active `.larql` patches when the schema version advances.

This matters because the `.larql` format is the interface through which all agents author
writes. A version mismatch between an agent's YAML-defined expectations and the current schema
is not currently covered by the Gate's pre-checks (§10.2 lists seven pre-checks; schema
version is not among them).

> **Security note (Warden):** If the Gate's pre-check list does not include a schema version
> check, an attacker who can replay a patch authored under an older schema version might bypass
> Validator checks that were added in the newer version. This makes GAP-3 not just a
> correctness gap but potentially a trust-boundary gap.

**Blocked by:** A decision on whether `.larql` patches carry an explicit schema version field
(one new header field in the format) and what the Gate does with mismatches.

**Blocks:**
- Complete Gate pre-check spec (the seven pre-checks in §10.2 may be incomplete without a
  schema version check)
- Validator L1 static analysis completeness (§9.3): is version conformance part of L1?
- The compaction re-run strategy for superseded patches across version boundaries (§8.10
  does not address this)
- v2 planning generally: the first v2 migration cannot be specced without a versioning strategy

**Priority:** 🔴 Critical

---

## 🟠 High — Blocks 1–2 Gaps or Load-Bearing Architectural Decisions

---

### GAP-4

**Domain(s):** Orchestration Comparativist

**Description:** Orchestration path selection (Path A — LangGraph alone; Path B — Claude
Agent SDK alone; Path C — Hybrid) is explicitly operator-decided and carries no recommendation
in the spec (D72, §12.3). This is a deliberate design choice, but it leaves two significant
items underspecified:

**(a) Nested sub-agent delegation token design.** The spec notes (§6, Category 3) that
"delegation tokens for nested sub-agent invocations (Path B/C nested cases)" are deferred
to v2. Without knowing which path is selected, the shape of this v2 feature cannot be
outlined. Path A (LangGraph) uses a different concurrency and subgraph model than Path B
(SDK sub-agents). The token design is structurally different in each.

**(b) Human-in-the-loop interface spec.** The review queues are defined (§15) but the
mechanism by which the human returns a decision to the Orchestrator is defined only at the
conceptual level (signed abort request, `approve_as_is`, etc.). The actual interface —
webhook, CLI, API endpoint, message queue — is path-dependent and fully unspecced.

**Blocked by:** Operator selection of Path A, B, or C.

**Blocks:**
- Delegation token v2 spec shape
- Human-in-the-loop interface spec (the two review queues in §15 have decision semantics
  defined but no delivery mechanism spec)

**Priority:** 🟠 High

---

### GAP-5

**Domain(s):** Security (Warden), MEMIT Specialist

**Description:** The Write Scope Definition update ceremony for long-running projects is only
partially addressed (OQ-S4, §18.2). The spec establishes the YAML ↔ Write Scope Definition
binding (§10.9) and states that changes affecting prompt content require a signed ceremony
plus `expected_yaml_hash` update. What is not defined is the behavior when a scope update
occurs while there are active in-flight invocation tokens or open Write Locks.

Specifically:

- A token carries `write_scope_hash` and `expected_yaml_hash` bound at issuance time (§10.4).
  If the Write Scope Definition is updated while that token is in its 10-minute TTL window,
  the Gate will reject the token at the `write_scope_hash` pre-check (step 4 of §10.2).
- The spec classifies this as an "infrastructure failure" class token rejection (§14.3),
  which means it re-issues a fresh token and does not consume retry budget. But the ceremony
  for a scope update is not atomic with token issuance — there is a window where old tokens
  are invalid and the agent has not yet received a new one.
- No spec for how the Orchestrator serializes scope updates against in-flight invocations.

**Blocked by:** A decision on scope-update serialization semantics — does the Orchestrator
drain in-flight invocations before accepting a scope update, or does it accept mid-flight
update with the token-rejection recovery path as the intended mechanism?

**Blocks:**
- Complete token lifecycle spec for the mid-flight update case
- Long-running project governance spec (the Sealed Corpus update ceremony for Write Scope
  Definitions is defined; the serialization protocol is not)

**Priority:** 🟠 High

---

### GAP-6

**Domain(s):** State Consistency Theorist

**Description:** The circuit breaker reset authority is labeled "operational policy" and left
unspecced (OQ-TC1, §11.8). The spec defines when the circuit breaker trips (3 consecutive
2PC failures in one task; 5 across tasks in 10 minutes; immediate on diverged state) and what
happens when it trips (systemwide write suspension until human reset). What is not defined:

- Who constitutes "human" for reset authority? Any human with machine access? A named
  operator role? A specific sealed-corpus entry?
- What verification must accompany a reset request? Is a reset a signed operation (like a
  schema migration token) or an out-of-band action?
- What Ledger entry does a reset produce? There is no `CIRCUIT_RESET` entry type in
  Appendix C.
- Can the Orchestrator partially resume (allow reads, block writes) before full human reset,
  or is it binary (fully suspended / fully operational)?

This matters because the circuit breaker is the last line of defense against cascading 2PC
failures. An underspecced reset path is a gap in the safety model.

**Blocked by:** A policy decision on reset authority scope and the reset ceremony.

**Blocks:**
- Appendix C Ledger entry type catalog completeness (`CIRCUIT_RESET` is missing)
- Complete Transaction Controller spec (TC owns compensation authority; reset authority is
  adjacent but currently unowned)

**Priority:** 🟠 High

---

### GAP-7

**Domain(s):** State Consistency Theorist

**Description:** The PREPARED-state timeout value is unspecced (OQ-TPC1, §18.1). The spec
sets the PREPARED-state timeout at a "2-hour working starting value" explicitly decoupled
from the invocation token TTL (per T7, §11.5). This matters because:

- A Genesis compile — a single atomic 2PC event across four tier files (D45, §11.6) — may
  take considerably longer than 2 hours on a large Architect Agent patch (up to 10,000 edges,
  internally sub-batched at 2,000).
- The spec does not define what happens if a PREPARED transaction times out: does the
  Transaction Controller auto-compensate (and in which direction?), or does it trip the
  circuit breaker?
- There is no spec for how a PREPARED-state timeout interacts with the Dependency Hold
  (which is placed at task declaration, before `PREPARED` is written). If the 2PC times out
  and compensates, does the Hold persist?

**Blocked by:** Implementation experience with MEMIT compile times on representative patch
sizes, or a decision to set Genesis PREPARED timeout separately from incremental PREPARED
timeout.

**Blocks:**
- Complete Transaction Controller behavior spec for long-running compiles
- Genesis 2PC behavior when compile time exceeds timeout (a gap that is particularly
  consequential given Genesis is a single non-restartable event)

**Priority:** 🟠 High

---

### GAP-8

**Domain(s):** Validation Contract Architect

**Description:** The held-out corpus authorship cadence and authority for Meta-Validator and
Meta-TGA is only partially specced (OQ-V5, §18.2). The mechanism is defined: Tier 2 sealed
corpus with versioned additive directories, operator-signed manifests, and per-case audit
reporting (T3, §13.3). What is not defined:

- Who has authority to author new corpus cases? Any operator? A designated test authority
  role? Is this role defined anywhere?
- How frequently must the corpus be extended? The Meta-Validator fires every 50 commits or
  weekly (§9.11) — if the corpus stagnates, the Health Score becomes meaningless as the
  model overfits to held-out cases.
- What constitutes a held-out case? The spec names "cases" but does not define the format:
  is it `(input, expected_pass/fail)`? `(prompt, expected_output, assertion_set)`?
- What is the minimum corpus size before a Meta-Validator run is valid? Running
  Meta-Validator against 3 cases is not a meaningful health signal.

Without these answers, the Meta-Validator and Meta-TGA are health monitors that can be
instantiated but not meaningfully operated.

**Blocked by:** A policy decision on corpus authorship role, cadence, and minimum viable
corpus size.

**Blocks:**
- Meta-Validator and Meta-TGA operational readiness (both components are specced but cannot
  be correctly initialized without corpus guidance)
- The 95% / 85% health thresholds become nominal without knowing what the corpus tests

**Priority:** 🟠 High

---

## 🟡 Medium — Self-Contained, No Downstream Spec Dependencies

---

### GAP-9

**Domain(s):** Validation Contract Architect, MEMIT Specialist

**Description:** Behavioral probe generalization beyond code domains is unspecced (OQ-W8,
§18.1). The spec's behavioral probe (§8.9 L2, §9.3 L2) is described in terms of "generation
tests" and "inference probes" — language that implies a code-execution or code-fact retrieval
framing. The Validation Layer (§9.3) specifies "inference probe" as a mandatory gate for
`CORE` and `SUPPORTING` edges, but does not define what a behavioral probe looks like for
non-code domains (e.g., a `domain_concept` edge asserting a legal constraint, a business
rule, or an architectural invariant that does not correspond to runnable code).

Without a domain-general probe spec, the Validator's L2 check is only fully defined for
code-domain deployments.

**Blocked by:** A decision on probe format generalization — likely requires defining a
domain-agnostic probe protocol (e.g., prompt templates that test semantic activation of the
written fact regardless of domain).

**Blocks:** Nothing in v1 code domain. Blocks non-code deployment planning.

**Priority:** 🟡 Medium

---

### GAP-10

**Domain(s):** Validation Contract Architect

**Description:** The constitutional test failure classification policy is labeled "operational
policy" rather than a spec decision (OQ-V1, §18.2). The spec states "Constitutional test
suite failures are treated as Tier 3 regardless of the error's surface appearance (C25)" —
this is the constraint. But the mechanism by which the Validator knows it is running a
constitutional test versus a task-specific test is not defined. The constitutional suite
lives in Tier 2 sealed corpora (§13.3) and the Validator has persistent read access. What
is missing:

- How does the Validator distinguish constitutional tests from task-generated tests at
  runtime? Are they tagged? In a separate test namespace?
- Who decides what "constitutional" means — what criteria qualify a test for promotion to
  the sealed constitutional suite?
- Is there a promotion ceremony, or does the operator directly add to the sealed corpus?

**Blocked by:** A policy decision on constitutional test tagging and the promotion ceremony
from task-generated tests to constitutional status.

**Blocks:** Nothing in current spec. Affects operational clarity.

**Priority:** 🟡 Medium

---

### GAP-11

**Domain(s):** State Consistency Theorist, MEMIT Specialist

**Description:** Layer 4 domain knowledge recovery when the originating external document is
unavailable is only partially addressed (OQ-SC2, §18.2). The spec notes this is "partially
addressed by Layer4_domain project-lifetime retention" — meaning the `.larql` patch and its
Ledger record survive. What is not defined:

- If a Layer 4 fact is written from an external document (e.g., a reference spec, a
  third-party API description) and that document later changes or disappears, the fact in
  `.vindex` may become stale. The Pruning Agent cannot catch this because the external
  document is not in Git (it's out-of-band).
- There is no mechanism for the harness to detect that the authoritative source for a
  Layer 4 fact has changed.
- The spec says "no auto-compile" for out-of-band changes — but out-of-band changes to
  external documents are not even detectable by the Pruning Agent, which monitors Git commits.

**Blocked by:** A decision on whether the harness tracks external document provenance for
Layer 4 facts, and if so, how (URL pinning? hash of source at write time?).

**Blocks:** Nothing in current spec. Affects long-running project correctness.

**Priority:** 🟡 Medium

---

### GAP-12

**Domain(s):** State Consistency Theorist

**Description:** The full Ledger epoch retention policy is only mechanism-specced, not
policy-specced (OQ-SL1, §18.2, §16.7). The spec defines:

- Default: project-lifetime retention.
- Epochs containing `INTEGRITY_VIOLATION` entries: indefinite.
- The archival mechanism and restore path.

What is not defined:

- What "project-lifetime" means operationally. When does a project end? Is there an explicit
  project-close ceremony that seals the final epoch?
- Can operators override the default retention period downward (shorter)? The spec doesn't
  say operators can't, but also provides no governance around retention policy changes.
- The archival storage format is unspecced beyond "compressed, manifest-sealed bundles" —
  this matters for forensic readability across long time horizons.

**Blocked by:** Operational policy decision on project lifecycle definition and retention
override governance.

**Blocks:** Nothing architecturally. Affects long-running project operations.

**Priority:** 🟡 Medium

---

### GAP-13

**Domain(s):** Security (Warden), Orchestration Comparativist

**Description:** The Genesis security model for fully automated pipelines is deferred
(OQ-S5, §18.2 and §19). v1 mandates human review of the Architect Agent output patch before
write engine execution (§10.6 step 1). The v2 target mentions "secondary LLM reviewer as
human-review proxy" — but no spec language defines:

- What properties this proxy must have.
- What its trust level would be relative to the Warden's trust model.
- How it would be authorized (would it require its own Write Scope Definition and agent YAML?).

This is genuinely a v2 item, but the current spec provides no outline that would allow v2
specification to begin without reopening architectural decisions.

**Blocked by:** v2 initiation and a policy decision on whether an LLM reviewer can be
granted Warden-level trust for Genesis authorization.

**Blocks:** v2 Genesis automation spec planning.

**Priority:** 🟡 Medium

---

### GAP-14

**Domain(s):** State Consistency Theorist, Orchestration Comparativist

**Description:** The async WAL flush cadence, Ledger verification intervals, and
Reconciliation Queue backlog thresholds are all listed as "starting heuristics" (§18.1,
T5/T11 thresholds). Specifically:

- WAL flush cadence before acknowledgment — unspecified; affects durability guarantee during
  the async write window.
- Light verification interval: every 100 entries (§16.4) — a starting heuristic with no
  justification for the 100-entry number.
- Full verification interval: 10,000 entries OR 24 hours (§16.4) — similarly provisional.
- Reconciliation backlog thresholds: 10 items / 7 days for warning; 50 items / 30 days for
  critical (§15.2) — no empirical basis stated.

**Blocked by:** Implementation experience with Ledger write volumes under realistic task
throughput and out-of-band Git commit rates.

**Blocks:** Nothing architecturally. All thresholds are tunable without spec changes.

**Priority:** 🟡 Medium

---

### GAP-15

**Domain(s):** Validation Contract Architect, MEMIT Specialist

**Description:** The compaction verification sample size is labeled a starting heuristic
(OQ-OC3, §18.1): "100% CORE + 10% random sample of others." What is not defined:

- How the 10% sample is drawn — random seed? Stratified by `declared_importance`? By age?
  By namespace?
- If compaction verification fails, the spec says "existing overlays retained" — but the
  failure report format (what the Behavioral Probe returns to the Transaction Controller to
  justify abort) is unspecced.

**Blocked by:** GAP-1 (OQ-W1 — empirical understanding of compaction frequency and total
edge volumes determines whether 10% is a meaningful sample or noise).

**Blocks:** Nothing independently; the mechanism is specced, only the sampling protocol
detail is missing.

**Priority:** 🟡 Medium

---

## 🟢 Low — Refinement Details, No Architectural Dependencies

---

### GAP-16

**Domain(s):** Security (Warden), Orchestration Comparativist

**Description:** Notification channels for integrity violations are explicitly out-of-spec
(OQ-S8, §18.2). The spec produces `INTEGRITY_VIOLATION` and `INTEGRITY_VIOLATION_EMERGENCY`
Ledger entries and triggers write suspension — but defines no mechanism for alerting the
human operator who must investigate. Email, Slack, logging sidecar, PagerDuty — all are
"not spec." In an unattended deployment, write suspension with no human notification is a
silent failure that could go undetected for extended periods.

**Blocked by:** Operational environment decision (notification infrastructure is
deployment-specific and rightly out-of-spec for a single-machine reference implementation).

**Blocks:** Nothing in the spec. A deployment concern only.

**Priority:** 🟢 Low

---

### GAP-17

**Domain(s):** Orchestration Comparativist, State Consistency Theorist

**Description:** Voluntary scope-lock release and inter-agent negotiation are deferred to v2
(OQ-CW1, §18.3). In the current spec, Write Lock TTL is 60 minutes with auto-release. There
is no mechanism for an agent to voluntarily release a lock before TTL expiry (e.g., because
it has completed its work early and wants to free the region). Similarly, there is no
negotiation protocol for two agents that need overlapping write regions — the current spec
simply rejects the second lock acquisition. In high-throughput scenarios, this could create
unnecessary sequentialization.

**Blocked by:** v2 initiation.

**Blocks:** Nothing in v1. Affects throughput in multi-agent concurrent deployments.

**Priority:** 🟢 Low

---

### GAP-18

**Domain(s):** State Consistency Theorist

**Description:** Multi-machine harness Ledger replication is deferred to v2 (OQ-SL2, §18.3).
The append-only JSONL Ledger with Merkle-chain-lite integrity is explicitly designed for
single-machine deployment. No replication protocol, consistency model for distributed Ledger
reads, or leader-election mechanism for multi-machine Orchestrators is outlined. The v2 scope
target lists "distributed consensus" without further specification.

**Blocked by:** v2 initiation and a distributed systems architecture decision.

**Blocks:** Nothing in v1.

**Priority:** 🟢 Low

---

### GAP-19

**Domain(s):** Security (Warden)

**Description:** Orchestrator signing key rotation is deferred to v2 (§10.5). The current
Orchestrator key is generated at first boot and never rotated in v1. The spec notes that
"full PKI" is v2 — but provides no outline of what a rotation event would require
(re-signing all active tokens? re-anchoring the public half in both Ledger and `.harness/`?
invalidating in-flight operations?). Without even an outline, the v2 rotation spec will need
to re-examine every component that binds on the Orchestrator key.

**Blocked by:** v2 initiation.

**Blocks:** Nothing in v1. Affects v2 spec planning effort.

**Priority:** 🟢 Low

---

## Summary Table

| GAP | Domain(s) | Priority | Root Open Question | Blocks |
|-----|-----------|----------|--------------------|--------|
| GAP-1 | MEMIT Specialist | 🔴 Critical | OQ-W1 — drift/compaction thresholds | GAP-5, backpressure spec, circuit-breaker rationale |
| GAP-2 | MEMIT Specialist | 🔴 Critical | OQ-W2 — MEMIT architecture compatibility | GAP-1, layer targeting, edge cap justification |
| GAP-3 | MEMIT + Graph | 🔴 Critical | OQ-W6 — `.larql` schema versioning | Gate pre-check spec, Validator L1, v2 migration |
| GAP-4 | Orchestration | 🟠 High | D72 — path selection deferred | Delegation token shape, HIL interface mechanism |
| GAP-5 | Warden + MEMIT | 🟠 High | OQ-S4 — scope version management | Token lifecycle during mid-project scope update |
| GAP-6 | State Consistency | 🟠 High | OQ-TC1 — circuit breaker reset authority | Ledger entry catalog, TC spec completeness |
| GAP-7 | State Consistency | 🟠 High | OQ-TPC1 — PREPARED-state timeout | TC behavior for long compiles, Genesis 2PC gap |
| GAP-8 | Validation | 🟠 High | OQ-V5 — corpus authorship cadence | Meta-Validator / Meta-TGA operational readiness |
| GAP-9 | Validation + MEMIT | 🟡 Medium | OQ-W8 — behavioral probe generalization | Non-code deployment planning |
| GAP-10 | Validation | 🟡 Medium | OQ-V1 — constitutional test classification | Operational clarity |
| GAP-11 | State Consistency + MEMIT | 🟡 Medium | OQ-SC2 — Layer 4 external doc unavailability | Long-running project correctness |
| GAP-12 | State Consistency | 🟡 Medium | OQ-SL1 — ledger retention policy | Long-running project ops |
| GAP-13 | Warden + Orchestration | 🟡 Medium | OQ-S5 — Genesis automation | v2 spec planning |
| GAP-14 | State Consistency + Orchestration | 🟡 Medium | T5/T11 async threshold suite | Nothing architecturally |
| GAP-15 | Validation + MEMIT | 🟡 Medium | OQ-OC3 — compaction sample size | Nothing independently |
| GAP-16 | Warden + Orchestration | 🟢 Low | OQ-S8 — notification channels | Nothing in spec |
| GAP-17 | Orchestration + State Consistency | 🟢 Low | OQ-CW1 — voluntary lock release | Nothing in v1 |
| GAP-18 | State Consistency | 🟢 Low | OQ-SL2 — multi-machine replication | Nothing in v1 |
| GAP-19 | Warden | 🟢 Low | Key rotation — v2 | v2 spec planning effort |

---

## Council Observations — Cross-Gap Patterns

Three structural patterns surface across the gap set:

**Write Engine Foundation (GAP-1, GAP-2, GAP-3)**
The three Critical gaps form a dependency chain. GAP-2 (architecture compatibility) must be
resolved before GAP-1 (threshold suite) can be meaningfully tuned, and GAP-3 (schema
versioning) is a prerequisite for any multi-version deployment or migration planning. These
three represent the write engine's unresolved foundation — everything else builds on them.

**Transaction Controller Completeness (GAP-6, GAP-7)**
The circuit breaker reset authority and PREPARED-state timeout are the two places where the
Transaction Controller's behavior is most underspecced. The TC is the safety floor of the
whole system. Both of these should be resolved before any implementation planning begins.

**Health Monitor Readiness (GAP-8)**
The Meta-Validator fires every 50 commits. If the corpus authorship policy is not established
before the first 50 commits, the first Health Score is meaningless. This gap should be
resolved at deployment setup, not deferred to operations.

---

*Gap Backlog v1.0 — 19 gaps catalogued across 6 specialist domains*
*Ready for prioritization and session assignment*
