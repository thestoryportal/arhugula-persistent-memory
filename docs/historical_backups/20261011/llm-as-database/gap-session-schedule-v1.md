# LLM as Database: Agent Harness Architecture
## Gap Session Schedule v1.0

> **Source:** `gap-backlog-v1.md` (19 gaps, prioritized post-Session 7 council)
> **Produced by:** Framework Spec Writer (framework-spec-writer skill)
> **Specialist provenance:** Framework Council (cross-domain scheduling analysis)
> **Status:** Draft — pending operator ratification before gap sessions begin
> **Basis:** Sessions 1–7 integrated spec (v1.0); gap-backlog-v1.md

---

## Scheduling Methodology

### Step 1 — Dependency Classification

Each gap was classified along two axes before sequencing:

**Blocker axis:** What must be resolved before this gap can close?
- **No spec-level blockers** — resolves via a spec decision made in session.
- **Externally blocked** — requires target model selection, empirical data, operator path selection, or v2 initiation. Session can produce *preparatory spec work* (test protocol, validation framework, contingent path spec) but cannot close the gap.
- **Blocked by another gap** — must wait for that gap's session output.

**Domain axis:** Which specialist skill(s) own the content?
- Single-specialist: one skill is primary, all content lives in that domain.
- Two-specialist: two skills share ownership; neither can close the gap alone.
- Full council: three or more domains implicated; cross-domain tensions are the primary content.

### Step 2 — Dependency Graph Summary

```
GAP-2 (MEMIT compat — external)
  └─ blocks ──► GAP-1 (thresholds — external)
                  └─ blocks ──► GAP-5 (scope serialization — spec-decidable,
                  |              partially informed by GAP-1 resolution)
                  └─ blocks ──► GAP-15 (compaction sample — threshold value
                                deferred; mechanism specced in session)

GAP-3 (schema versioning — spec-decidable)
  └─ informs ──► GAP-5 (token carries schema-version hash; versioning
                 decisions affect in-flight token content)

GAP-6 (circuit breaker reset — spec-decidable)
GAP-7 (PREPARED timeout — spec-decidable)
  Both ──► State Consistency TC completeness cluster (no upstream deps)

GAP-8 (corpus authorship — spec-decidable)
GAP-10 (constitutional test tagging — spec-decidable)
  Both ──► Validation operational policy cluster (no upstream deps)

GAP-4 (orchestration path — external: operator decision)
  └─ blocks ──► delegation token v2 shape (path-specific)
  └─ blocks ──► HIL interface mechanism (path-specific)
  Addressed via contingent path specs (all three paths specced conditionally)

GAP-13, 16, 17, 18, 19 ──► v2-deferred; session produces outline spec blocks only
```

### Step 3 — Council vs. Specialist Flags

| Requires Full Council | Rationale |
|-----------------------|-----------|
| GAP SESSION 7 (GAP-2 + GAP-1 + GAP-4) | MEMIT architecture decisions cascade to Security (token cap justification), Validation (divergence thresholds), and State Consistency (compaction scheduling); GAP-4 path shapes require all specialists to mark their path-conditional contracts. |
| GAP SESSION 8 (v2 deferred gaps) | Multi-domain v2 scoping requires each specialist to contribute their v2 requirements before a coherent outline emerges. |

All other sessions use one or two specialist skills.

---

## Gap Session Schedule

---

### GAP SESSION 1: GAP-3
**Gaps:** GAP-3
**Primary skill:** MEMIT Specialist + Graph Data Architect
**Council required:** No — two-specialist session
**Estimated length:** Long

**Why first:** GAP-3 is Critical priority and has no spec-level blockers. A decision on
schema versioning is required before GAP-5 can be fully addressed (token content carries
`expected_yaml_hash`; a schema version field would also live in the token). Resolving GAP-3
also fixes an identified security gap: the Gate's seven pre-check list (§10.2) does not
include a schema version check, which is a replay-attack surface.

**Content:**
- Decide whether `.larql` patches carry an explicit `schema_version` header field.
- Define Gate pre-check behavior on version mismatch (reject / quarantine / downgrade path).
- Define Validator L1 static analysis inclusion of version conformance.
- Define compaction re-run strategy for superseded patches across version boundaries (§8.10 gap).
- Define migration path for active `.larql` patches when schema version advances.

**Produces:**
- Spec block: `.larql` Schema Version Field
- Spec block: Gate Pre-Check List (revised — adding check 8: schema version)
- Spec block: Validator L1 Static Analysis (version conformance clause)
- Spec block: Superseded-Patch Archive compaction policy across version boundaries
- Interface contract: Gate ↔ Validator (version conformance handoff)
- Open question dispositions: OQ-W6 (targeting resolution or partial)

---

### GAP SESSION 2: GAP-6 + GAP-7
**Gaps:** GAP-6, GAP-7
**Primary skill:** State Consistency Theorist (with Warden consult on GAP-6 reset authorization)
**Council required:** No — single-specialist domain; Warden provides authorization policy input
**Estimated length:** Medium

**Why second:** Both gaps address Transaction Controller completeness — the TC is the safety
floor of the entire system. Neither gap has upstream spec blockers. They are tightly coupled:
the circuit breaker reset ceremony (GAP-6) and the PREPARED-state timeout behavior (GAP-7)
both define what the TC does at its edges. Resolving them together prevents contradictions
between the reset path and the timeout compensation path.

**Content (GAP-6):**
- Define the reset authority role: named operator role vs. any machine-access holder.
- Define the reset ceremony: signed operation, out-of-band action, or both.
- Define partial resume semantics (read-allowed / write-blocked intermediate state vs. binary).
- Add `CIRCUIT_RESET` entry type to Appendix C Ledger catalog.

**Content (GAP-7):**
- Decide whether Genesis PREPARED timeout is set separately from incremental PREPARED timeout.
- Define TC behavior on PREPARED-state timeout: auto-compensate (and direction) vs. circuit-breaker trip.
- Define Dependency Hold fate when PREPARED-state timeout triggers compensation.
- Produce a worked scenario: large Architect Agent patch (10,000 edges, sub-batched at 2,000) approaching timeout.

**Produces:**
- Spec block: Transaction Controller — Circuit Breaker Reset Authority
- Spec block: Transaction Controller — PREPARED-State Timeout Behavior
- Ledger entry type: `CIRCUIT_RESET` (added to Appendix C catalog)
- Open question dispositions: OQ-TC1, OQ-TPC1 (targeting resolution)

---

### GAP SESSION 3: GAP-5
**Gaps:** GAP-5
**Primary skill:** AISecOps Specialist + MEMIT Specialist
**Council required:** No — two-specialist session
**Estimated length:** Medium

**Why third (after GAP SESSION 1):** GAP-5 addresses scope-update serialization when
in-flight invocation tokens are live. A token carries `write_scope_hash` and
`expected_yaml_hash`. GAP SESSION 1's resolution of the schema version field determines
whether tokens also carry `schema_version` — adding a third hash the scope-update ceremony
must manage. Sequencing GAP SESSION 3 after GAP SESSION 1 prevents a double-revision of the
token spec.

**Content:**
- Decide scope-update serialization semantics: drain-first vs. mid-flight-with-recovery.
- Define Orchestrator's serialization protocol for scope updates against in-flight invocations.
- Spec the token lifecycle for the mid-flight update case: token rejection → re-issuance →
  retry without consuming retry budget (§14.3 "infrastructure failure" class).
- Define the update ceremony atomicity contract: what constitutes a complete scope update?
- Extend the long-running project governance spec: Write Scope Definition update ceremony
  currently defines what triggers signing; this session defines the sequencing guarantee.

**Produces:**
- Spec block: Write Scope Definition — Update Ceremony Serialization Protocol
- Spec block: Token Lifecycle — Mid-Flight Scope Update Recovery Path
- Interface contract: Orchestrator ↔ Gate (scope update serialization guarantee)
- Open question disposition: OQ-S4 (targeting resolution or partial)

---

### GAP SESSION 4: GAP-8 + GAP-10
**Gaps:** GAP-8, GAP-10
**Primary skill:** Validation Contract Architect
**Council required:** No — single-specialist domain
**Estimated length:** Medium

**Why fourth:** Both gaps are Validation operational policy decisions with no upstream spec
blockers. They are grouped because they share a concern: who has authority to write tests into
the sealed corpus, and how does the system distinguish test categories at runtime. Resolving
them together produces a coherent sealed corpus governance model.

**Content (GAP-8 — Corpus Authorship):**
- Define corpus authorship authority role: any operator vs. designated test authority vs. operator-
  signed submission with role declaration.
- Define minimum viable corpus size before a Meta-Validator run is considered meaningful.
- Define held-out case format: `(input, expected_pass/fail)` structure or `(prompt,
  expected_output, assertion_set)` or other schema.
- Define corpus extension cadence relative to Meta-Validator firing schedule (every 50 commits
  or weekly — §9.11).

**Content (GAP-10 — Constitutional Test Classification):**
- Define how Validator distinguishes constitutional tests from task-generated tests at runtime
  (tag in test metadata? separate test namespace?).
- Define criteria for constitutional status: what qualifies a test for promotion to sealed
  constitutional suite.
- Define the promotion ceremony: operator-direct addition vs. a formal promotion request with
  review window.

**Produces:**
- Spec block: Sealed Corpus — Authorship Authority and Governance
- Spec block: Held-Out Case Format Definition
- Spec block: Constitutional Test — Classification and Promotion Ceremony
- Open question dispositions: OQ-V5, OQ-V1 (targeting resolution)

---

### GAP SESSION 5: GAP-9 + GAP-11 + GAP-15
**Gaps:** GAP-9, GAP-11, GAP-15
**Primary skill:** MEMIT Specialist (secondary: Validation Contract Architect, State Consistency Theorist)
**Council required:** No — two-to-three specialist session; MEMIT is the shared domain across all three
**Estimated length:** Medium

**Why grouped:** All three gaps have MEMIT as a primary or secondary domain. GAP-9 (behavioral
probe generalization) and GAP-15 (compaction sample protocol) both concern Validator behavior
during MEMIT operations. GAP-11 (Layer 4 external doc provenance) concerns how `.larql` patches
track the source of Layer 4 writes. Handling them together surfaces any conflicts between probe
generalization requirements and compaction verification requirements before they are separately
specced into incompatibility.

Note on GAP-15: GAP-15 is nominally blocked by GAP-1 (the 10% compaction sample size is
unjustified without empirical write volume data). However, the *mechanism* — how the sample is
drawn, how a compaction verification failure is reported back to the Transaction Controller —
can be specced independently of the threshold value. The threshold remains provisional pending
GAP-1 resolution.

**Content (GAP-9 — Probe Generalization):**
- Define a domain-agnostic behavioral probe protocol that does not presuppose code execution.
- Define how probe templates adapt across domains: code-fact retrieval, legal constraint
  assertion, business rule activation, architectural invariant recall.
- Define what "inference probe passes" means outside a code-execution context.

**Content (GAP-11 — Layer 4 External Doc Provenance):**
- Decide whether the harness tracks external document provenance for Layer 4 facts.
- If yes: define the provenance record structure (URL pinning? content hash at write time?
  last-known-good timestamp?).
- Define what happens when a provenance check detects source document change or unavailability.
- Define whether the Pruning Agent's scope expands to monitor pinned external document hashes.

**Content (GAP-15 — Compaction Sample Protocol):**
- Define sampling strategy for the compaction verification 10% sample: random seed,
  stratified by `declared_importance`, by age, or by namespace.
- Define the failure report format returned by the Behavioral Probe to the Transaction Controller
  when compaction verification fails.
- Mark threshold value (10%) as provisional pending GAP-1 resolution (OQ-W1).

**Produces:**
- Spec block: Behavioral Probe — Domain-Agnostic Protocol
- Spec block: Layer 4 Write Provenance Record
- Spec block: Compaction Verification — Sampling Protocol and Failure Report Format
- Open question dispositions: OQ-W8, OQ-SC2, OQ-OC3 (targeting partial or full resolution)

---

### GAP SESSION 6: GAP-12 + GAP-14
**Gaps:** GAP-12, GAP-14
**Primary skill:** State Consistency Theorist (with Orchestration Comparativist on GAP-14 WAL/async thresholds)
**Council required:** No — single-specialist domain with light cross-specialist input
**Estimated length:** Short–Medium

**Why grouped:** Both gaps are State Consistency operational policy items with no architectural
dependencies. GAP-12 addresses Ledger retention policy; GAP-14 addresses the async threshold
suite for WAL flush cadence, Ledger verification intervals, and Reconciliation Queue backlog.
They do not block each other, but both produce policy decisions that belong in the same
operational governance section of the spec.

**Content (GAP-12 — Ledger Retention):**
- Define "project-lifetime" operationally: is there an explicit project-close ceremony?
- Define whether operators can override the default retention period downward, and if so,
  what governance applies.
- Define archival storage format beyond "compressed, manifest-sealed bundles" — sufficient for
  forensic readability across multi-year horizons.
- Define the project-close ceremony if one is required (sealed final epoch, final Merkle root
  commitment).

**Content (GAP-14 — Async Threshold Suite):**
- Produce a rationale framework for each provisional threshold rather than replacing numbers
  (numbers remain provisional pending empirical data per the external blocker):
  - WAL flush cadence: define the durability guarantee it is intended to satisfy.
  - Light verification interval (every 100 entries): define the detection-window guarantee.
  - Full verification interval (10,000 entries / 24 hours): define the audit-completeness
    guarantee.
  - Reconciliation Queue backlog thresholds (10/7d warning; 50/30d critical): define the
    SLA they are proxies for.
- All values remain flagged as provisional pending implementation experience.

**Produces:**
- Spec block: Ledger Epoch Retention Policy
- Spec block: Project Lifecycle — Project-Close Ceremony
- Spec block: Async Threshold Suite — Rationale Framework (values provisional)
- Open question dispositions: OQ-SL1 (targeting resolution), T5/T11 (partial — framework
  defined, values deferred)

---

### GAP SESSION 7: GAP-2 + GAP-1 + GAP-4
**Gaps:** GAP-2, GAP-1, GAP-4
**Primary skill:** Full Framework Council
**Council required:** YES — see rationale below
**Estimated length:** Long

**Why council required:**
GAP-2 (MEMIT architecture compatibility) cascades into every domain: the Security model
(token edge-cap justification depends on MEMIT batch math), the Validation layer (divergence
check thresholds are calibrated against MEMIT's expected output distribution), and the State
Consistency layer (compaction scheduling assumes MEMIT compile-time behavior). A MEMIT
architecture finding cannot be specced by the MEMIT Specialist alone without other specialists
committing to the conditional branches in their own specs.

GAP-4 (orchestration path selection) is similarly cross-domain: the delegation token shape
for Path B/C nested sub-agents is a Security domain decision; the HIL interface delivery
mechanism is an Orchestration + State Consistency decision; the compaction scheduling behavior
differs by path.

Note on scope: GAP-2 and GAP-1 are externally blocked and cannot be closed in session. The
session produces *preparatory spec work* — conditional spec blocks and test protocols that
activate when external decisions are made. GAP-4 is similarly externally blocked; the session
produces contingent path specs for all three paths (A, B, C) so that when the operator selects
a path, the relevant spec block activates with no further council work required.

**Content (GAP-2 — MEMIT Compatibility Test Protocol):**
- Define the compatibility test protocol: what tests must pass against the chosen model
  architecture before the write engine spec is considered verified.
- Define the compatibility criteria: layer targeting correctness, covariance-update math
  validity, orthogonal projection safeguard behavior on the target architecture.
- Define what happens if the target model uses an architecture variant (MoE, Mamba-family,
  grouped-query attention) — which spec sections must be revised and by which specialist.
- Produce conditional spec blocks: "If MEMIT compatibility confirmed: [spec text]. If MEMIT
  incompatible: [alternative write engine evaluation criteria]."

**Content (GAP-1 — Threshold Validation Framework):**
- Define the empirical validation protocol for all provisional thresholds (drift warning,
  drift hard trigger, sub-batch ceiling, overlay file count, p95 latency trigger,
  `stale_urgent` ceiling, 24-hour Pruning floor).
- Define the target write-volume stress test: what scenario, what model, what measurement
  instruments, what pass/fail criteria for each threshold.
- Define the spec update ceremony when empirical data replaces provisional values: which
  sections update, which IDs are marked resolved, which constraints are promoted from
  provisional to authoritative.
- All current threshold values remain flagged provisional.

**Content (GAP-4 — Contingent Path Specs):**
Produce three conditional spec blocks — one per orchestration path. Each block is marked
"activates on operator selection of Path [X]" and remains dormant until that selection is made.

- **Path A (LangGraph alone):** delegation token shape for subgraph delegation, HIL interface
  delivery mechanism in LangGraph's concurrency model, compaction scheduling within LangGraph's
  execution graph.
- **Path B (Claude Agent SDK alone):** delegation token shape for nested sub-agent invocations,
  HIL interface delivery mechanism via SDK callback or interrupt, sub-agent write scope
  inheritance model.
- **Path C (Hybrid):** delegation token handoff protocol at the LangGraph ↔ SDK boundary, HIL
  delivery in a hybrid concurrency model, scope inheritance when an SDK sub-agent is spawned
  from a LangGraph node.

Each path block carries its own interface contract stubs (marked provisional until path is
selected).

**Produces:**
- Spec block: MEMIT Compatibility Test Protocol (conditional — three architecture outcomes)
- Spec block: Threshold Validation Framework (all values remain provisional)
- Spec block: Path A — Contingent Delegation Token + HIL Interface Spec
- Spec block: Path B — Contingent Delegation Token + HIL Interface Spec
- Spec block: Path C — Contingent Delegation Token + HIL Interface Spec
- Open question status updates: OQ-W2 (test protocol defined; gap remains open pending
  external test), OQ-W1 (validation framework defined; gap remains open pending data),
  D72 (path selection remains operator-decided; contingent specs complete)

---

### GAP SESSION 8: GAP-13 + GAP-16 + GAP-17 + GAP-18 + GAP-19
**Gaps:** GAP-13, GAP-16, GAP-17, GAP-18, GAP-19
**Primary skill:** Full Framework Council
**Council required:** YES — multi-domain v2 scoping requires all specialists to contribute v2 requirements
**Estimated length:** Short

**Why council required:** Each deferred gap belongs to a different domain or pair of domains.
No single specialist can produce a complete v2 outline without the others declaring their
domain's v2 requirements. The session is short because each gap produces an *outline spec
block* — a structured statement of what v2 must define — not a full spec.

**Note:** None of these gaps can be closed in v1. The session outputs are inputs to the v2
planning phase, not resolutions of the gaps themselves.

**Content:**
- **GAP-13 (Genesis automation — Warden + Orchestration):** Define the properties a
  secondary LLM reviewer must satisfy to act as a human-review proxy; define its required
  trust level relative to the Warden's trust model; outline what authorization mechanism
  (agent YAML? separate Write Scope Definition?) it would require.
- **GAP-16 (Notification channels — Warden + Orchestration):** Define the interface contract
  the notification subsystem must satisfy (inputs: `INTEGRITY_VIOLATION` and
  `INTEGRITY_VIOLATION_EMERGENCY` Ledger entries; outputs: operator-alerting signal);
  mark channel selection as deployment-specific.
- **GAP-17 (Voluntary lock release — Orchestration + State Consistency):** Define the
  negotiation protocol requirements for overlapping write regions; define what a voluntary
  release ceremony must guarantee (Lock Registry update atomicity, in-progress operation
  safety); outline the sequentialization concern to be relaxed.
- **GAP-18 (Multi-machine Ledger replication — State Consistency):** Define the consistency
  model requirements for a distributed Ledger (linearizable? eventual? what SLA?); outline
  leader-election requirements; flag Merkle-chain-lite as single-machine-only in v1.
- **GAP-19 (Orchestrator key rotation — Warden):** Define what a key rotation event must
  guarantee (active token validity window, in-flight operation safety, public-key re-anchoring
  in Ledger and `.harness/`); outline PKI requirements for v2.

**Produces:**
- Five v2 outline spec blocks (one per gap), each structured as: What v2 must define /
  What v1 leaves as boundary / What architectural decisions v2 must not reopen without council.
- Open question status updates: OQ-S5, OQ-S8, OQ-CW1, OQ-SL2 all marked
  Deferred-to-v2 with outline reference.

---

## Session Schedule Summary

```
GAP SESSION 1:  GAP-3               Primary: MEMIT Specialist + Graph Data Architect    Est: Long
GAP SESSION 2:  GAP-6, GAP-7        Primary: State Consistency Theorist                 Est: Medium
GAP SESSION 3:  GAP-5               Primary: AISecOps Specialist + MEMIT Specialist     Est: Medium
GAP SESSION 4:  GAP-8, GAP-10       Primary: Validation Contract Architect              Est: Medium
GAP SESSION 5:  GAP-9, GAP-11, 15   Primary: MEMIT Specialist (+ Validation, State)    Est: Medium
GAP SESSION 6:  GAP-12, GAP-14      Primary: State Consistency Theorist                 Est: Short–Medium
GAP SESSION 7:  GAP-2, GAP-1, GAP-4 Primary: Full Framework Council                    Est: Long
GAP SESSION 8:  GAP-13, 16–19       Primary: Full Framework Council                    Est: Short
```

**Total sessions estimated:** 8
**Full council sessions:** 2 (Sessions 7 and 8)
**Two-specialist sessions:** 3 (Sessions 1, 3, 5)
**Single-specialist sessions:** 3 (Sessions 2, 4, 6)

---

## Gaps Not Closeable in Gap Sessions

The following gaps cannot be fully resolved through spec work alone. Their session outputs
are test protocols, threshold validation frameworks, and contingent path specs — not closures.

| Gap | External Blocker | Session Output |
|-----|------------------|----------------|
| GAP-1 | Target model selection + write-volume stress test | Threshold validation framework (Session 7) |
| GAP-2 | Target model selection + MEMIT compatibility test run | Compatibility test protocol (Session 7) |
| GAP-4 | Operator orchestration path selection (A/B/C) | Contingent path specs — all three (Session 7) |
| GAP-13 | v2 initiation | v2 outline spec block (Session 8) |
| GAP-16 | Operational environment / deployment decision | v2 outline spec block (Session 8) |
| GAP-17 | v2 initiation | v2 outline spec block (Session 8) |
| GAP-18 | v2 initiation + distributed systems architecture decision | v2 outline spec block (Session 8) |
| GAP-19 | v2 initiation | v2 outline spec block (Session 8) |

GAP-15 is partially closeable: its mechanism (sampling strategy, failure report format) is
specced in Session 5. Its threshold value (10%) remains provisional pending GAP-1 resolution.

---

## Session Dependency Diagram

```
Session 1 (GAP-3: schema versioning)
    │
    └──► informs ──► Session 3 (GAP-5: scope serialization — token carries schema version)
    
Session 2 (GAP-6, GAP-7: TC completeness)
    │  [independent — no upstream or downstream session deps within this schedule]
    
Session 4 (GAP-8, GAP-10: validation policy)
    │  [independent]
    
Session 5 (GAP-9, GAP-11, GAP-15: MEMIT-adjacent medium gaps)
    │  [independent of Sessions 1–4; GAP-15 threshold value deferred to Session 7]
    
Session 6 (GAP-12, GAP-14: State Consistency operational policy)
    │  [independent]
    
Sessions 1–6 (all)
    └──► informs ──► Session 7 (GAP-2, GAP-1, GAP-4: council + preparatory/contingent)
                         [architecture decisions from Sessions 1–6 determine which
                          conditional branches in Session 7 spec blocks are load-bearing]
    
Session 7
    └──► informs ──► Session 8 (v2 deferred gaps — council outline)
                         [Session 7's contingent path specs define what v2 must not
                          reopen without council; Session 8 references them]
```

---

*Gap Session Schedule v1.0 — 8 sessions across 19 gaps*
*Produced post-Session 7 council for Phase 2 gap resolution planning*
