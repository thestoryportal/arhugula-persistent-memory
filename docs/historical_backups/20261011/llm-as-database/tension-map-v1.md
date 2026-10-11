# LLM as Database: Agent Harness Architecture
## Session 7 — Cross-Domain Tension Resolution Map v1.0

> **Source document:** `llm-as-database-v1_0-integrated-spec.md`
> **Session:** Session 7 — Full Council Synthesis (cross-domain tension resolution)
> **Tensions identified and worked:** 12 (T1–T12 per Appendix F)
> **Tensions fully resolved:** 6
> **Tensions partially resolved:** 5
> **Tensions deferred / unlocatable:** 1

---

## Reading Guide

Tensions in this document are drawn from two sources:

1. **Session 7 spec resolutions (T1–T11)** — decisions the council worked to resolution during
   Session 7, each producing one or more Interface Contracts and decisions (D-numbers).
2. **Pre-mapped structural tensions** — the six tensions baked into the council skill before
   Session 1. A cross-reference section at the end maps how each was addressed.

Tension numbering follows the spec's T1–T12 Appendix F cross-reference. Status labels:

| Status | Meaning |
|--------|---------|
| **Resolved** | Fully specced; no open questions remain |
| **Partial** | Core decision made; one or more policy/empirical questions remain open |
| **Deferred** | No decision made; reason documented |

---

## Session 7 Tension Resolutions (T1–T12)

---

### TENSION-T1: `attention_weight` Authority
**Graph Data Architect vs. MEMIT Specialist**

**Status:** ✅ Resolved

**The conflict:** The original `.larql` format had `attention_weight` as an agent-authored
field — the agent declared how much weight a given edge should carry. The Graph Data Architect
wanted this as a schema-layer declaration (the agent's semantic intent about edge importance).
The MEMIT Specialist objected: `attention_weight` is computed by MEMIT's covariance balancer
math during compile. Letting agents author this number means agents are claiming to know what
MEMIT will produce — a category error that could produce incorrect validation gating.

**Resolution:** Split into two separate concepts (§8.6, closes OQ-W5):

- **`declared_importance`** — agent-authored enum: `CORE` / `SUPPORTING` / `INCIDENTAL`.
  Reference mappings: 0.9 / 0.7 / 0.4. Used *pre-commit* by the Validator to gate
  verification intensity (L2 inference probe is mandatory for CORE and SUPPORTING).
- **`attention_weight`** — engine-computed during MEMIT compile via covariance balancer math.
  Not authored by any agent. Emitted to the State Ledger entry for audit and post-compile
  analysis only.

A post-compile **divergence check** runs: if `declared_importance = CORE` yields engine-computed
`attention_weight < 0.5`, or `declared_importance = INCIDENTAL` yields `> 0.9`, the Validator
flags the write as a soft signal for human review. Not a hard rejection.

**Remaining open question:** None. OQ-W5 closed.

**New interface contracts:** `.larql` format extended (IC-SC1 `CONTENT_CLASSIFICATION` directive
added in same session). `attention_weight` field becomes engine-output-only.

---

### TENSION-T2: TGA Independence vs. Correctness Depth
**Validation Contract Architect vs. Orchestration Comparativist**

**Status:** ✅ Resolved

**The conflict:** The Validation Contract Architect required the Test-Generation Agent (TGA)
to never see the Coder Agent's code before writing tests — independence enforced by sequencing.
The Orchestration Comparativist noted that this structural independence produces a scalability
problem: human-authored test suites become a bottleneck, and TGA tests written blind may have
poor coverage. The Comparativist wanted a hybrid authorship model. The Validation Architect
resisted any mechanism that let the Coder's output influence the test.

**Resolution:** Four-layer TGA validation cascade (§9.4, closes OQ-V3):

- **L1 — Structural check** (all outputs, mandatory): ≥2 assertions per test, no bare `pass`
  or `assert True`, every assertion references spec-declared symbols.
- **L2 — Stub probe** (all outputs, mandatory): TGA tests run against an empty stub
  implementation. Any substantive test that passes against the stub is a false-positive gate;
  TGA is re-invoked. This catches tests that assert nothing meaningful.
- **L3 — Dual-TGA** (`CORE` tasks only): two independent TGA invocations on the same spec;
  only behaviors asserted by *both* count as active gates. Deep coverage without Coder
  influence.
- **L4 — Meta-TGA** (periodic, every 50 commits or weekly): held-out `(spec, gold_test_set)`
  corpus per Sealed Corpus pattern. Health Score thresholds mirror Meta-Validator's.

Independence is enforced by sequencing *and* the stub probe, not policy alone. The
Orchestration Comparativist's scale concern is addressed by dual-TGA only for CORE tasks.

**Remaining open question:** None at the structural level. OQ-V5 (corpus authorship cadence
for Meta-TGA held-out corpus) remains open — this is addressed separately in T3.

**New interface contracts:** IC-V-TGA1, IC-V-TGA2.

---

### TENSION-T3: Meta-* Audit Completeness vs. Corpus Integrity
**Warden vs. Validation Contract Architect**

**Status:** 🔶 Partial

**The conflict:** The Warden needed complete audit visibility into Meta-Validator and Meta-TGA
health monitoring behavior — specifically, the ability to audit individual test case outcomes,
not just aggregate health scores. The Validation Contract Architect needed the held-out corpora
protected from normal Validator/TGA access (exposure during normal operation would allow the
agents to overfit to the held-out cases, corrupting the health signal).

**Resolution:** Sealed Corpus pattern applied to both Meta-* corpora (§13.3):

- Held-out corpora are Tier 2 sealed artifacts: versioned additive directories, operator-signed
  manifests, dual-store integrity verification.
- Access is **time-bounded**: corpora are only accessible during scheduled Meta-* runs, never
  during normal Validator/TGA operation.
- **Per-case audit reporting is mandatory** for Meta-* runs. Aggregate-only reporting is
  explicitly forbidden. Each test case result is individually logged to the Ledger.

The corpus is protected; the audit trail is complete. Both requirements are satisfied.

**Remaining open question (OQ-V5):** Who has authority to author new corpus cases? At what
cadence must the corpus be extended to prevent Health Score overfitting? What constitutes a
held-out case (format: `(input, expected_pass/fail)`? `(prompt, expected_output, assertion_set)`)?
What is the minimum corpus size before a Meta-* run produces a meaningful score? Mechanism is
specced; authorship policy is deferred.

**New interface contracts:** IC-SL7, IC-SL8, IC-SL9.

---

### TENSION-T4: Configuration Authority Fragmentation
**Warden vs. State Consistency Theorist vs. Orchestration Comparativist**

**Status:** ✅ Resolved

**The conflict:** Three separate sessions had specced three different storage patterns for
configuration artifacts, each with different trust requirements and integrity mechanisms:

- The Warden specced a permanently immutable Genesis seal (D49, dual-store).
- The State Consistency Theorist specced path-classification as an anchored Git artifact (D76).
- The Orchestration Comparativist specced agent YAMLs as Git-committed operational config.
- The Write Scope Definitions (Warden's domain) needed to be agent-runtime-immutable but
  operator-updatable.

These four different patterns had no unified governance model, making boot-time verification
and integrity reasoning inconsistent across artifact types.

**Resolution:** Three-tier `.harness/` model (§13, closes OQ-GOC1 via D76):

- **Tier 1 — Immutable Anchor:** Mint-once, verify-forever. `genesis-seal.json` and
  `orchestrator-key-anchor.json`. Dual-stored (Ledger primary + `.harness/` secondary).
  Boot-time hash comparison. Mismatch suspends boot.
- **Tier 2 — Sealed Artifacts:** Evolving human-authored integrity-critical artifacts.
  Versioned additive directories, operator-signed manifests. Includes: meta-validator suite,
  meta-TGA corpus, constitutional suite, write-scope-definitions, reconciliation-reviewers.
- **Tier 3 — Anchored Git Config:** Git-committed operational config with Ledger anchoring.
  `path-classification.json`, agent YAMLs. Detect-at-boot integrity enforcement.

Agent YAML is bound to its Write Scope Definition via hash — the Write Scope Definition is
the source of truth; the YAML is operationally subordinate. Update ceremony scales with
blast radius.

**Remaining open question:** None at the structural level. Stronger Tier 3 enforcement
(pre-receive server-side Git hooks, prevent-at-write) is deferred to v2.

**New interface contracts:** IC-CFG1, IC-CFG2, IC-CFG3.

---

### TENSION-T5: Token Revocation vs. In-Flight Write Continuity
**Warden vs. Orchestration Comparativist**

**Status:** 🔶 Partial

**The conflict:** The Warden needed immediate bulk revocation capability for compromised
agents. The Orchestration Comparativist needed agent invocations to complete without
mid-flight interruption — a token that can be revoked mid-operation creates an
indeterminate state where the agent has started work but may not be able to complete it.
Short TTLs alone don't solve this: a token can expire or be revoked after Phase 1 of 2PC
but before Phase 2 completes.

**Resolution:** Two mechanisms combined (§10.4, §10.5, closes OQ-S2, OQ-S6):

- **Agent suspension model:** `suspended_agents` in-memory set on Orchestrator. Suspended
  agents cannot receive new tokens; any existing token presented by a suspended agent is
  rejected at the Gate with `TOKEN_AGENT_SUSPENDED`. Suspension is immediate without waiting
  for TTL expiry.
- **Governance-state binding:** Tokens carry hash-bindings to the Write Scope Definition
  version and Agent YAML version at issuance time. Stealing a token is insufficient if any
  bound governance document changes within the TTL window — a stolen token becomes invalid
  the moment the operator updates the scope definition.
- **Orchestrator signing key dual-store:** Public half stored in both the Ledger
  (`ORCHESTRATOR_KEY_ANCHOR`, immutable) and `<repo_root>/.harness/orchestrator-key-anchor.json`
  (Git-committed). Boot-time hash comparison; mismatch suspends boot.

**Remaining open question (OQ-S4):** The behavior when a Write Scope Definition is updated
while in-flight invocation tokens are within their 10-minute TTL window. The spec classifies
the resulting Gate rejection as an "infrastructure failure" (re-issue token, no retry budget
consumed) — but does not define how the Orchestrator serializes scope updates against
in-flight invocations. Full PKI (mass revocation lists, Orchestrator key rotation,
multi-Orchestrator trust) is deferred to v2.

**New interface contracts:** IC-CFG3 (YAML binding check), boot-time verification
sequence extended (§13.5 steps 3 and 6).

---

### TENSION-T6: Genesis Completeness vs. Catastrophic Forgetting Risk
**Graph Data Architect vs. MEMIT Specialist**

**Status:** 🔶 Partial

**The conflict:** The Graph Data Architect wanted Genesis to be comprehensive — bake in all
foundational knowledge upfront so that agents operate from a rich semantic foundation. The
MEMIT Specialist warned that over-encoding at Genesis is expensive to correct (Genesis
modification requires schema migration token + elevated review) and that high edit volumes at
Genesis degrade MEMIT's locality guarantees. Too much in Genesis creates brittleness; too
little forces agents to repeatedly reconstruct missing foundations during normal operation.

**Resolution:** Three-part model (§8.7, §8.8):

- **Genesis scope test:** "Is the harness broken without this fact? If no, it does not belong
  in Genesis." L4 (foundational domain knowledge) is updatable via the standard pipeline; only
  facts that genuinely require the Genesis write path should use it.
- **Drift-from-anchor model:** Drift is measured relative to the most recent anchor event
  (Genesis compile OR successful compaction), not as cumulative totals. After an anchor,
  drift resets to zero. This makes correction costs explicit and bounded.
- **Architect capacity model:** Hard security cap of 10,000 edges per patch; MEMIT-recommended
  sub-batch of 2,000 edges (sub-batching is transparent to the Ledger). Both ceilings enforce
  the MEMIT Specialist's locality constraint without preventing the Graph Data Architect from
  encoding comprehensive L4 knowledge over multiple patches.

**Remaining open question (OQ-W1):** All threshold values (drift warning 1,500, drift hard
trigger 8,000, sub-batch 2,000) are provisional heuristics pending empirical validation
against the target model architecture. The structure is resolved; the values are not.

**New interface contracts:** IC-MEMIT-3 (`ANCHOR_ESTABLISHED` flag on qualifying Ledger entries).

---

### TENSION-T7: Schema Migration Token Timing
**Warden vs. State Consistency Theorist**

**Status:** ✅ Resolved

**The conflict:** The original D27 schema migration token had a 30-minute TTL measured from
issuance to completion of the entire Genesis compile. The State Consistency Theorist observed
that a large Genesis patch (up to 10,000 edges, internally sub-batched at 2,000) running on
GPU could easily exceed 30 minutes. A TTL expiry mid-compile produces an indeterminate state:
the 2PC Phase 1 `PREPARED` entry has been written, but the token is now invalid — which
authority does the compile now operate under? The Warden could not accept a compile proceeding
without valid authorization; the State Consistency Theorist could not accept a PREPARED state
that might auto-abort due to token expiry.

**Resolution:** Admission-time TTL model (§10.6, §14.1, revises D27):

- Schema migration token TTL is **10 minutes** (reduced from D27's 30 minutes, but measured
  differently).
- The token is consumed at **2PC Phase 1 admission** — the moment the Commit Executor accepts
  the package and writes the `PREPARED` Ledger entry.
- Once admitted to the 2PC window, the compile proceeds **independent of subsequent token
  state**. The token is a witness to the governance state at the moment of admission, not an
  ongoing authorization credential.
- If governance state changes after admission (e.g., scope definition update), it cannot
  affect the in-progress compile.

**Remaining open question (OQ-TPC1):** The PREPARED-state timeout value (2-hour working
starting value, explicitly decoupled from token TTL). If a Genesis compile exceeds 2 hours,
the Transaction Controller's behavior is underspecced: does it auto-compensate, and in which
direction? Does it trip the circuit breaker?

---

### TENSION-T8: Write Lock Semantics Conflation
**State Consistency Theorist vs. Orchestration Comparativist**

**Status:** ✅ Resolved

**The conflict:** The original D59/D60 scope lock was conflating three distinct concerns
into a single 60-minute TTL lock: concurrent write prevention, dependency preservation across
long escalation chains, and Pruning exclusion. The Orchestration Comparativist observed that
this created unnecessary contention: Agent B cannot write novel facts unrelated to Agent A's
work region, even though Agent A only needs protection for the edges it is *reading*, not all
writes to its declared region. The State Consistency Theorist needed dependency preservation
across 72-hour human escalation windows — far longer than a 60-minute write lock is useful.

**Resolution:** Lock/Hold split into two distinct Orchestrator-managed mechanisms (§11.9, §17):

- **Write Lock** (60-minute TTL, auto-release): Concurrent write prevention only. Acquired
  at task declaration. Blocks other agents from writing to the declared region. Released on
  task completion, abort, or TTL expiry.
- **Dependency Hold** (72-hour TTL, renewable on escalation): Placed on specific edges the
  task is *reading* (its dependency set). Blocks Pruning operations on held edges only. Does
  NOT block other agents' Write Locks or novel-fact writes to non-conflicting edges.

Task resume re-verification protocol: on escalated task resumption, Orchestrator compares
current state of held edges against the escalation-entry snapshot. `context_stale` (edge
changed) → task repackaged with current state. `context_lost` (hold expired before resume)
→ `dependency_reconstruction_required` escalation.

**Remaining open question (OQ-CW1):** Voluntary scope-lock release before TTL expiry. Agents
that complete work early cannot release their Write Lock; the region remains locked until
TTL. Inter-agent negotiation for overlapping write regions is deferred to v2.

**New interface contracts:** IC-PA7 (Pruning → Orchestrator: Hold-state query).

---

### TENSION-T9: Compaction Correctness vs. Efficiency
**MEMIT Specialist vs. Validation Contract Architect**

**Status:** 🔶 Partial

**The conflict:** The MEMIT Specialist preferred delta composition for compaction efficiency —
re-running MEMIT only on patches added since the last compaction, rather than re-processing
the entire `.larql` archive. The Validation Contract Architect objected: MEMIT's correctness
guarantees (orthogonal projection, covariance balancer) are applied *during* a compile run.
Delta composition skips these steps for already-compiled layers, weakening the mathematical
guarantees that the write engine's safety properties depend on. There is no specification of
what "delta composition" even means at the MEMIT mathematical level — it was not a formally
studied technique.

**Resolution:** Full MEMIT re-run mandated (§11.14, §8.10):

- Delta composition is **rejected on correctness grounds**. Every compaction is a Genesis-Mode
  MEMIT recompile on all active `.larql` patches.
- **Epoch bundling** for storage management: superseded patches (older than the most recent
  anchor) moved to `.larql-archive/superseded/{epoch_bundle_N}/` as compressed
  manifest-sealed bundles. Classification-differentiated retention: structural-classified
  superseded patches 90-day default; Layer4_domain-classified patches project-lifetime.
- Compaction trigger set revised to five triggers: drift warning (1,500 edges), drift hard
  (8,000 edges), time-based (30 days), overlay file count (50+), p95 latency (2× baseline).
- Compaction is a single atomic 2PC event (C-OC2). Genesis tiers never compacted (C-OC1).

**Remaining open question (OQ-OC3):** Compaction verification sample size ("100% CORE + 10%
random others" is a starting heuristic). Sampling methodology (random seed? stratified by
`declared_importance`? by age? by namespace?) is unspecced. The failure report format — what
the Behavioral Probe returns to the Transaction Controller to justify a compaction abort — is
also unspecced.

**New interface contracts:** IC-OC6, IC-OC7, IC-OC8.

---

### TENSION-T10: Out-of-Band Git Commit Handling
**State Consistency Theorist vs. Warden**

**Status:** ✅ Resolved

**The conflict:** Humans and external tools can commit to Git outside the harness pipeline.
The State Consistency Theorist needed these to be detected and reconciled — otherwise
`.vindex` silently diverges from Git. The Warden could not allow auto-compilation of catch-up
patches generated from unauthenticated state changes; every write to the parametric layer
requires human-authorized, Validator-verified content. These two requirements were in direct
conflict: detect-and-reconcile (State Consistency) vs. never-auto-compile (Warden).

**Resolution:** Two-queue model with distinct semantics (§15):

- Out-of-band commits are detected by the Pruning Agent and generate catch-up patches flagged
  `requires_human_review` — **no auto-compile under any condition**.
- Catch-up patches route to the **Reconciliation Review Queue** (distinct from the Correctness
  Review Queue used for failed Reflexion escalations). Reviewer question: "Should we update
  parametric memory to match this out-of-band state change?"
- **Decisions available:** `approve_patch` | `reject_patch` | `modify_patch` | `defer_with_reason`.
  `modify_patch` outputs re-enter the standard Validator cascade — reviewer-authored patches
  are not exempt from validation.
- **Default on neglect differs by queue type:** Correctness Review → task times out into
  logged suspension (work lost, no state change). Reconciliation Review → items accumulate;
  backlog signals escalate via Ledger and Consistency Status API. No silent default in either
  direction.
- Consistency Status API extended with `RECONCILIATION_BACKLOG` as a sixth state.

**Remaining open question:** None at the structural level. Backlog threshold values
(10 items/7 days → warning; 50 items/30 days → critical) are starting heuristics.

**New interface contracts:** IC-PA8, IC-OR10, IC-OR11, IC-OR12, IC-OR13, IC-OR14.

---

### TENSION-T11: Audit Trail vs. State Ledger Consolidation
**Warden vs. State Consistency Theorist**

**Status:** 🔶 Partial

**The conflict:** The Warden had specced a separate, cryptographically immutable audit trail
(D28) as a security artifact — a record of every write operation for forensic and compliance
purposes. The State Consistency Theorist had separately specced a State Ledger as the primary
consistency record — mapping Git commit hashes to `.vindex` snapshot hashes, logging 2PC
phases, and recording compensation events. These were two append-only Merkle-chain integrity
logs doing substantially overlapping work. Both needed tamper-evidence; both needed post-hoc
queryability. Maintaining two separate infrastructure components doubled complexity and
created questions about which was authoritative for any given event type.

**Resolution:** Unified Ledger — one artifact, two query lenses (§16):

- **One append-only JSONL file** at `<harness_root>/.state-ledger/ledger.jsonl`. Merkle-chain-lite
  integrity. Outside Git and outside `.vindex`.
- "Audit trail" becomes an `audit_category` tag on Ledger entries (SECURITY, CONSISTENCY,
  VALIDATION, GOVERNANCE, LIFECYCLE), not a separate store.
- **Three-tier writer model:** W1 (all components via Orchestrator mediation, default), W2
  (bootstrap only, one-time), W3 (emergency path for compromised-Orchestrator scenarios —
  Gate, Transaction Controller, and Boot-verifier only; rate-limited, strict schema, forces
  immediate write suspension).
- **Sync/async write mode split** resolves the audit-completeness vs. throughput sub-tension:
  security-critical entries (`TOKEN_CONSUMED`, `PREPARED`, `COMMITTED`, `INTEGRITY_VIOLATION`)
  are **synchronous** (blocking). Observation entries are **async** via WAL — durable delivery
  guaranteed, never lossy, but not on the commit critical path.
- **Tiered read access:** Agents restricted to own-identity entries only. Humans: Orchestrator-
  mediated query API with filtering. Orchestrator: direct read access.

**Remaining open question (OQ-SL1):** Full ledger retention policy. Default is project-lifetime;
epochs containing `INTEGRITY_VIOLATION` entries are indefinite. What "project-lifetime" means
operationally (is there a project-close ceremony?) is deferred. WAL flush cadence before
acknowledgment is an unspecified heuristic. Operator retention override governance is unspecced.

**New interface contracts:** IC-LDG1 through IC-LDG5.

---

### TENSION-T12: Referenced in Appendix F — Body Text Reference Not Located
**Specialists unknown**

**Status:** ⚠️ Unlocatable

**The conflict:** Appendix F states "T1–T12: Session 7 (Integration — cross-domain resolutions)"
and the spec header confirms "twelve integration tensions." Eleven tensions (T1–T11) are
traceable to named spec sections, interface contracts, and decision closures. T12 does not
appear with an explicit label in any spec body section reviewed.

**Possible interpretation:** The spec header may count the six pre-mapped structural tensions
(from the council skill design) plus six tensions that emerged during Session 7 (T7–T12), with
T1–T6 resolving the pre-mapped tensions and T7–T11 being new emergent tensions. Under this
reading, T12 may be the resolution of a tension that was subsumed into an existing decision
number (D73–D80) without receiving its own standalone T-number in the body text.

**Recommended action:** Flag as a spec inconsistency. During the next council review checkpoint,
request explicit identification of the T12 tension and its resolution. Candidate tensions that
might account for T12 include:

- The peer agent review authorization model (how a second Coder Agent is invoked and tokenized
  during D37 Step 2 escalation — agent-to-agent trust is not explicitly resolved).
- The W3 emergency writer scope (Warden vs. State Consistency Theorist on how narrow the
  emergency Ledger write path must be).
- The `CONTENT_CLASSIFICATION mixed` rejection protocol — who tells the Coder Agent to split
  a patch that contains both structural and domain content?

---

## Pre-Mapped Structural Tensions — Session 7 Disposition

The following six tensions were identified during skill design as structural to the framework.
This section records how each was addressed in Session 7.

---

### Pre-T1: Immutability vs. Mutability Window
**Warden vs. State Consistency Theorist**

**Session 7 resolution:** Addressed primarily by **T5** (signing key dual-store + token model)
and **T11** (sync/async Ledger write mode). The mutability lifecycle is now fully defined:

- Tier 1 artifacts: immutable from mint. Never modified.
- Active `.vindex` overlay: mutable during Phase 1 prepare window (the 2PC `PREPARED` state).
- `.vindex` post-Phase 2: effectively immutable — superseding it requires a new 2PC `COMMITTED`
  entry; the prior overlay is archived, not overwritten.
- Genesis tiers L1–L2: frozen post-mint via `IMMUTABLE_ANCHOR` Ledger entry. L3 requires
  elevated review. L4 is updatable via standard pipeline.

**Status:** ✅ Fully resolved in Session 7.

---

### Pre-T2: Write Volume vs. Edit Locality
**Graph Data Architect vs. MEMIT Specialist**

**Session 7 resolution:** Addressed by **T6** (drift-from-anchor model + Architect capacity
model). The MEMIT Specialist's locality protection is the Architect capacity ceiling (10,000
edge hard cap, 2,000 sub-batch recommendation) and the drift-from-anchor triggers. The Graph
Data Architect's schema expressivity is preserved: there is no ceiling on total knowledge
encoded over time, only on per-patch volume and rate-of-change since the last anchor.

**Status:** 🔶 Structurally resolved. All threshold values (1,500 / 8,000 / 2,000) remain
provisional pending empirical validation (OQ-W1 open — carried into gap backlog as GAP-1).

---

### Pre-T3: Validator Independence vs. Test Coverage at Scale
**Validation Contract Architect vs. Orchestration Comparativist**

**Session 7 resolution:** Addressed by **T2** (TGA four-layer cascade). Independence is
enforced by sequencing (TGA never sees Coder's code before writing tests) and the stub probe
(false positives caught before Coder is invoked). Coverage depth is achieved through dual-TGA
for CORE-importance tasks only — the Orchestration Comparativist's scale concern is addressed
by scoping the expensive dual-invocation to the highest-importance edges.

**Status:** ✅ Fully resolved in Session 7.

---

### Pre-T4: Audit Completeness vs. Write Throughput
**Warden vs. State Consistency Theorist + MEMIT Specialist**

**Session 7 resolution:** Addressed by **T11** (unified Ledger with sync/async write mode
split). Security-critical entries are synchronous (blocking); observation entries are async
via WAL with guaranteed delivery. The Warden's requirement — never lossy audit — is satisfied.
The State Consistency Theorist and MEMIT Specialist's concern — don't add latency to the 2PC
commit critical path for observation entries — is satisfied by the WAL async path.

**Status:** 🔶 Structurally resolved. WAL flush cadence is an unspecified heuristic (part
of GAP-14 in the gap backlog).

---

### Pre-T5: Schema Stability vs. Agent Autonomy
**Graph Data Architect vs. Orchestration Comparativist**

**Session 7 resolution:** Partially addressed by **T4** (three-tier config governance). The
Gate's scope check enforces declared vocabulary at runtime — agents cannot write edges using
relation labels not declared in the schema. Write Scope Definitions in Tier 2 seal the
per-agent relation authority.

**Status:** ⚠️ Partially resolved. The schema extension protocol — the mechanism by which
agents could *propose* new relation types for Warden/human approval — is described in the
council skill as the resolution path but is not explicitly specced as a protocol in the
integrated document. Agents are *prevented* from using undeclared relations, but the pathway
for authorized schema extension (beyond schema migration tokens for L1–L3) is not
contractually defined for the normal pipeline. Carried into the gap backlog as a sub-gap
within GAP-3 (`.larql` schema versioning).

---

### Pre-T6: Genesis Completeness vs. Genesis Lock-in
**Graph Data Architect vs. MEMIT Specialist**

**Session 7 resolution:** Addressed by **T6** (minimal viable Genesis scope test + four-tier
structure + drift-from-anchor model). The authoritative scope test: *"Is the harness broken
without this fact? If no, it does not belong in Genesis."* The four-tier structure allows the
Graph Data Architect to encode comprehensive domain knowledge in L4 (updatable via standard
pipeline) while protecting the MEMIT Specialist's locality guarantees by keeping frozen tiers
(L1–L2) minimal and rarely modified.

**Status:** 🔶 Structurally resolved. Threshold values remain provisional (OQ-W1).

---

## Summary Table

| Tension | Specialists | Status | Primary Resolution | Remaining Gap |
|---------|-------------|--------|--------------------|---------------|
| T1 — `attention_weight` authority | Graph Data Architect vs. MEMIT Specialist | ✅ Resolved | Two-number model (declared_importance + engine-computed weight) | None |
| T2 — TGA independence vs. depth | Validation vs. Orchestration | ✅ Resolved | Four-layer TGA cascade (structural + stub probe + dual-TGA + Meta-TGA) | None |
| T3 — Meta-* audit vs. corpus integrity | Warden vs. Validation | 🔶 Partial | Sealed Corpus + per-case audit reporting | OQ-V5 (corpus authorship policy) |
| T4 — Config authority fragmentation | Warden vs. State Consistency vs. Orchestration | ✅ Resolved | Three-tier `.harness/` model | None (v2: pre-receive hooks) |
| T5 — Token revocation vs. continuity | Warden vs. Orchestration | 🔶 Partial | Agent suspension model + governance-state binding | OQ-S4 (scope update serialization) |
| T6 — Genesis completeness vs. forgetting | Graph Data Architect vs. MEMIT Specialist | 🔶 Partial | Drift-from-anchor + capacity model + scope test | OQ-W1 (thresholds provisional) |
| T7 — Schema migration token timing | Warden vs. State Consistency | ✅ Resolved | Admission-time TTL; compile proceeds independently of token state | OQ-TPC1 (PREPARED timeout) |
| T8 — Write lock semantics conflation | State Consistency vs. Orchestration | ✅ Resolved | Lock/Hold split (Write Lock 60 min; Dependency Hold 72 hr renewable) | OQ-CW1 (v2: voluntary release) |
| T9 — Compaction correctness vs. efficiency | MEMIT Specialist vs. Validation | 🔶 Partial | Full MEMIT re-run mandated; epoch bundling for storage | OQ-OC3 (sample size protocol) |
| T10 — Out-of-band Git handling | State Consistency vs. Warden | ✅ Resolved | Two-queue model; no auto-compile; distinct neglect defaults | None (thresholds heuristic) |
| T11 — Audit trail vs. State Ledger | Warden vs. State Consistency | 🔶 Partial | Unified Ledger; audit_category tagging; sync/async write split | OQ-SL1 (retention policy) |
| T12 — Unlocatable | Unknown | ⚠️ Unlocatable | Not traceable in spec body | Flag for council review |
| Pre-T1 — Immutability vs. mutability | Warden vs. State Consistency | ✅ Resolved (via T5, T11) | Mutability lifecycle fully defined per tier | None |
| Pre-T2 — Write volume vs. locality | Graph Data Architect vs. MEMIT | 🔶 Partial (via T6) | Capacity model + drift anchoring | OQ-W1 (GAP-1) |
| Pre-T3 — Validator independence vs. scale | Validation vs. Orchestration | ✅ Resolved (via T2) | Four-layer cascade + scope-bounded dual-TGA | None |
| Pre-T4 — Audit completeness vs. throughput | Warden vs. State Consistency + MEMIT | 🔶 Partial (via T11) | Sync/async Ledger split | WAL cadence heuristic (GAP-14) |
| Pre-T5 — Schema stability vs. autonomy | Graph Data Architect vs. Orchestration | ⚠️ Partial (via T4) | Gate scope enforcement; extension protocol unspecced | Schema extension pathway (sub-gap in GAP-3) |
| Pre-T6 — Genesis completeness vs. lock-in | Graph Data Architect vs. MEMIT | 🔶 Partial (via T6) | Scope test + four-tier structure | OQ-W1 (GAP-1) |

---

*Tension Map v1.0 — 12 Session 7 tensions catalogued (11 traceable, 1 unlocatable)*
*6 pre-mapped structural tensions cross-referenced*
*Ready for gap session scheduling and council review checkpoint*
