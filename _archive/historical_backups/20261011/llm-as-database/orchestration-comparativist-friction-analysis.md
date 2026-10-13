# Skill Friction Analysis — Session 6
## Skill: `orchestration-comparativist`
## Analyzed by: Post-session friction review process

> **Prompt discrepancy notice:** The opening prompt header reads
> *"This session analyzes: state-consistency-theorist"* but the body of the
> prompt asks to evaluate the **`orchestration-comparativist`** skill, and the
> uploaded transcript is `transcript-session-6-orchestration.md` — the
> orchestration session. This report analyzes `orchestration-comparativist`
> as the body of the prompt specifies. If a separate `state-consistency-theorist`
> friction analysis is needed, that session should reference
> `transcript-session-5-consistency.md`.

---

## Source Documents

| Document | Role |
|---|---|
| `transcript-session-6-orchestration.md` | Primary evidence source |
| `orchestration-tools-requirements-matrix.md` | Session 6 summary |
| `gap-backlog-v1.md` | Post-Session-7 gap extraction |
| `tension-map-v1.md` | Post-Session-7 tension resolution map |

---

## Friction Entries (sorted: Confidence descending, then Type)

---

### SKILL-FRICTION-[N]:

```
SKILL-FRICTION-1:
  Skill: orchestration-comparativist
  Session: Session 6 — Orchestration Requirements Matrix
  Type: Missed Question
  Evidence: IC-OR6 (Human Review Queue) and IC-OR8 (Human → Orchestrator
    abort) in the Session Summary Block define WHAT is communicated (full
    task package, signed abort request with ledger entry ID) but specify no
    transport mechanism — webhook, CLI endpoint, API call, message queue,
    Slack callback. GAP-4(b) in the gap backlog names this directly:
    "the actual interface — webhook, CLI, API endpoint, message queue —
    is path-dependent and fully unspecced."
  Description: The skill catalogued all 16 HIL triggers exhaustively and
    produced IC-OR6 and IC-OR8, but both contracts define only the payload
    structure — they never ask the critical follow-up: HOW does the human
    communicate their decision back? This is a different question from "what
    is in the review package" (well-specced) and "what does a signed abort
    request contain" (well-specced). The return-path mechanism is the
    gap — and because it is path-dependent (LangGraph interrupt() vs. SDK
    hooks vs. external webhook), it cannot be filled in after path selection
    without revising the HIL interface contracts. The skill had all the
    information to flag this in Session 6 and did not.
  Confidence: High
    Evidence is direct: GAP-4(b) traces to IC-OR6/IC-OR8; both contracts
    are present in the transcript with the payload defined but the transport
    mechanism absent.
  Proposed fix: Add a mandatory checklist item to the SKILL.md Spec Output
    Checklist: "For every HIL trigger defined, confirm the interface contract
    specifies BOTH the outbound payload (what the Orchestrator delivers to
    the human) AND the inbound mechanism (how the human's decision returns
    to the Orchestrator — webhook URL, CLI command, API endpoint, message
    queue pull — and what authenticates the return signal)." The framing
    question "what does the human use to interact with this system?" should
    be added to the Useful Framing Questions list.
```

---

```
SKILL-FRICTION-2:
  Skill: orchestration-comparativist
  Session: Session 6 — Orchestration Requirements Matrix
  Type: Cross-Domain Miss
  Evidence: Pre-T5 (Schema Stability vs. Agent Autonomy) in tension-map-v1.md
    is listed as "⚠️ Partially resolved" with status: "the pathway for
    authorized schema extension is not contractually defined for the normal
    pipeline." In the transcript, HS-7 (Schema migration token issuance —
    sub-second — orchestrator-local — S3 IC14) appears in Dimension 3
    (Heterogeneous Step Types) as a step the orchestrator must run. The skill
    treated this as an orchestration scheduling requirement only, never asking:
    what if an agent needs a relation type not yet declared in the schema?
    Who can propose extensions, via what path, and how does the Gate handle
    a patch that uses a new relation type pending approval?
  Description: The Orchestration Comparativist co-owns Pre-T5 with the Graph
    Data Architect. The skill's domain responsibility was to flag schema
    extension as a workflow question — if an agent needs a new relation type,
    that triggers a schema change event that itself requires orchestration
    (token issuance, review, approval, Gate update). By treating HS-7 purely
    as "the orchestrator runs this step type," the skill missed the upstream
    trigger question: how does the need for HS-7 get initiated? The extension
    pathway ended up unspecced and carried into the backlog as a sub-gap
    within GAP-3 — a Critical-priority gap.
  Confidence: High
    The HS-7 entry is visible in the transcript (Dimension 3 table, line ~155).
    Pre-T5 in the tension map is explicitly attributed to "Graph Data Architect
    vs. Orchestration Comparativist" and left partially unresolved.
  Proposed fix: Add to the Phase 1 Requirements Harvesting section of SKILL.md:
    "Ask the Graph Data Architect domain: what is the workflow when an agent
    needs a relation type not declared in the current schema? Who initiates
    a schema extension request, through what channel, and how does the
    Orchestrator gate further writes until it is approved or rejected? This is
    an orchestration event, not a schema authorship question." Add this to
    the mandatory cross-domain checklist run before the evaluation grid.
```

---

```
SKILL-FRICTION-3:
  Skill: orchestration-comparativist
  Session: Session 6 — Orchestration Requirements Matrix
  Type: Cross-Domain Miss
  Evidence: T4 (Configuration Authority Fragmentation — Warden vs. State
    Consistency vs. Orchestration Comparativist) in tension-map-v1.md. The
    Session 6 transcript introduces ".harness/path-classification.json"
    (OQ-GOC1 resolution block, transcript lines ~812-826) as a new Git-committed
    config file without cross-referencing the Warden's config file governance
    patterns from Session 3. T4 is described as a conflict between "three
    separate sessions [that] had specced three different storage patterns for
    configuration artifacts, each with different trust requirements."
  Description: By Session 6, three config-file governance patterns existed
    across sessions: (1) Warden-owned per-agent YAML files (Session 3),
    (2) State Consistency Theorist's `.harness/genesis-seal.json` (Session 5),
    and (3) the Orchestration Comparativist's new `.harness/path-
    classification.json` (Session 6). The skill introduced the third without
    asking whether it conflicted with existing governance patterns, triggering
    the T4 fragmentation that the council had to resolve in Session 7. The
    skill's SKILL.md lists "Spec Output Checklist" items but contains no prompt
    to cross-check new config artifacts against Warden-owned governance.
    This is squarely within the skill's synthesis-layer responsibility —
    the skill is supposed to be the integration layer, and integration of
    config governance is a canonical synthesis-layer concern.
  Confidence: High
    OQ-GOC1 resolution block is directly present in the transcript. T4 is
    attributed to "Warden vs. State Consistency vs. Orchestration Comparativist"
    in the tension map.
  Proposed fix: Add a cross-domain check to Phase 1 of the SKILL.md operating
    mode: "Before introducing any new config file, registry, or persistent
    store, ask: does the Warden already own a governance model for this class
    of artifact? Does the State Consistency Theorist's tier structure cover
    this? If a new storage artifact is required, name the tier it belongs to
    and the governance authority, explicitly reconciling with existing patterns
    from Sessions 3 and 5." Add to the Spec Output Checklist: "Every new
    persistent artifact introduced this session has a named governance tier
    and authority from the existing multi-session config model."
```

---

```
SKILL-FRICTION-4:
  Skill: orchestration-comparativist
  Session: Session 6 — Orchestration Requirements Matrix
  Type: Format Failure
  Evidence: Three OQ-resolution spec blocks in the session transcript are
    missing the "Tradeoffs decided:" field required by the canonical spec
    block format defined in the project system prompt:
    - OQ-TC3 block (transcript lines ~795-809): has What/Hard constraints/
      Open questions/Interface contract — no "Tradeoffs decided."
    - OQ-GOC1 block (transcript lines ~812-826): same omission.
    - OQ-OC1 block (transcript lines ~846-856): missing both "Tradeoffs
      decided" AND "Open questions (deferred)" — only has What/Hard
      constraints/Interface contract.
    By contrast, OQ-V2 and OQ-TPC2 (resolved earlier in the session) do
    include "Tradeoffs decided" fields.
  Description: The canonical spec format requires five fields: What it must
    do / Hard constraints / Tradeoffs decided / Open questions (deferred) /
    Interface contract. Three of the six OQ-resolution blocks produced in
    this session are missing at least one required field. The inconsistency
    is within the session — earlier resolution blocks (OQ-V2, OQ-TPC2) are
    complete; later blocks (OQ-TC3, OQ-GOC1, OQ-OC1) are truncated. This
    pattern suggests the skill compressed its output as the session
    progressed, treating "no tradeoff" as license to omit the field rather
    than writing "None — this decision is unambiguous" or similar. The
    missing fields were not flagged in Session 7, but they represent an
    incomplete spec record.
  Confidence: High
    The format failures are directly visible in the transcript. The missing
    fields are verifiable by inspection against the five-field canonical format.
  Proposed fix: Add to the SKILL.md Spec Output Checklist: "Every OQ
    resolution block produced in this session contains all five canonical
    fields. 'Tradeoffs decided: None — this decision is unambiguous' is
    acceptable; omitting the field is not. Do not compress spec blocks as
    the session progresses." Add an explicit reminder that the five-field
    format applies even to short resolutions.
```

---

```
SKILL-FRICTION-5:
  Skill: orchestration-comparativist
  Session: Session 6 — Orchestration Requirements Matrix
  Type: Backlog Attribution
  Evidence: GAP-4 in gap-backlog-v1.md (Priority: High). "(a) Nested
    sub-agent delegation token design. The spec notes that 'delegation tokens
    for nested sub-agent invocations (Path B/C nested cases) are deferred
    to v2. Without knowing which path is selected, the shape of this v2
    feature cannot be outlined. Path A uses a different concurrency and
    subgraph model than Path B. The token design is structurally different
    in each.'" The three path spec blocks (Path A, B, C) are present in the
    transcript (lines ~863-1017); none contain any content about delegation
    token shape.
  Description: The decision to defer path selection was appropriate — it is
    an operator decision. However, the skill missed an adjacent deliverable
    that it could have produced without resolving path selection: conditional
    delegation token shape stubs, one per path. Path A's token would be
    a LangGraph graph-state field with subgraph scope. Path B's token would
    be an SDK subagent authority declaration. Path C would compose both.
    These are short, unambiguous derivations from the path specs already
    written. Producing them would have closed GAP-4(a) at the time of its
    parent decision (D72), rather than leaving it open as a high-priority
    blocking gap. The skill's SKILL.md Phase 4 instructions say "document
    the orchestration decision as a spec artifact" — this implies following
    a decision to its downstream implications, which includes the v2 token
    design per path.
  Confidence: Medium
    Inferred from gap backlog. The path spec blocks are in the transcript
    and visibly contain no delegation token content. The derivation is
    straightforward enough that the skill's omission is attributable to
    scope compression rather than genuine complexity.
  Proposed fix: Add to Phase 4 of the SKILL.md operating mode: "For every
    path option specced without a selection, produce at minimum a stub
    interface contract for each path-dependent downstream component (e.g.,
    delegation token design, agent identity model). Label stubs as
    'Path-conditional — resolve after path selection.' This prevents path
    deferral from cascading into opaque downstream blockers."
```

---

```
SKILL-FRICTION-6:
  Skill: orchestration-comparativist
  Session: Session 6 — Orchestration Requirements Matrix
  Type: Backlog Attribution
  Evidence: GAP-16 in gap-backlog-v1.md (Priority: Low). "The spec produces
    INTEGRITY_VIOLATION and INTEGRITY_VIOLATION_EMERGENCY Ledger entries and
    triggers write suspension — but defines no mechanism for alerting the human
    operator who must investigate... write suspension with no human notification
    is a silent failure that could go undetected for extended periods." IC-OR7
    in the Session Summary Block defines the five-state /consistency-status
    API (NORMAL | COMPACTION_IN_PROGRESS | CIRCUIT_TRIPPED | DIVERGED |
    GENESIS_LOCKED) — but notification channels are absent from every IC.
  Description: The skill defined write suspension semantics thoroughly (IC-OR7,
    IC-OR4, and the CIRCUIT_TRIPPED / DIVERGED states). The missing question
    is: in an unattended deployment, how does the operator learn the harness
    has suspended writes? The /consistency-status API is agent-polling-facing,
    not human-notification-facing. The skill's own SKILL.md lists "Observability
    and Audit" as one of the eight requirement dimensions, yet the dimension
    6 requirements in the matrix (OA-1 through OA-7) cover event emission to
    agents and the State Ledger — not human operator alerting. This is a scoping
    omission: the skill treated observability as agent-facing and never asked
    whether the human operator has a notification path. Even a brief "notification
    mechanism is deployment-specific and out of spec" note would have closed
    this with an explicit scope decision rather than leaving it as a silent gap.
  Confidence: Medium
    Inferred from gap backlog. IC-OR7 is directly in the transcript; the
    notification question is absent by inspection.
  Proposed fix: Add to Dimension 6 (Observability and Audit) in the SKILL.md:
    "Ask: when a circuit breaker trips or an integrity violation is detected,
    how does the human operator who must respond actually find out? If the
    deployment is unattended, is notification out-of-spec? If so, document
    that explicitly as an operational policy non-requirement." Add to the
    Spec Output Checklist: "Every suspension/escalation event has either a
    defined human-notification path or an explicit 'out of spec — deployment
    concern' note."
```

---

```
SKILL-FRICTION-7:
  Skill: orchestration-comparativist
  Session: Session 6 — Orchestration Requirements Matrix
  Type: Backlog Attribution
  Evidence: GAP-13 in gap-backlog-v1.md (Priority: Medium). "The current spec
    provides no outline that would allow v2 specification to begin without
    reopening architectural decisions" regarding Genesis automation. IC-OR6
    in the Session Summary Block defines the Human Review Queue for HIL-1
    (Genesis write approval — Architect Agent output), but contains no
    discussion of the v2 path to automation. The integrated spec's v2 target
    mentions "secondary LLM reviewer as human-review proxy" without further
    definition.
  Description: When the skill specced the HIL-1 gate (Genesis write approval),
    it correctly made human review mandatory for v1. But because it was
    producing the orchestration interface for that gate — and the framework
    spec mentions a v2 automation target — the skill was in the right position
    to ask: what would an LLM proxy reviewer need to satisfy the Warden's
    trust model? This doesn't require speccing the v2 feature; it only requires
    noting the trust model preconditions (e.g., "a v2 LLM reviewer proxy would
    require its own Write Scope Definition, a distinct ledger entry type
    distinguishing proxy approval from human approval, and Warden-level trust
    certification"). That note would have given the v2 planning team something
    to build on. Without it, GAP-13 now blocks v2 spec planning entirely.
  Confidence: Medium
    Inferred from gap backlog. The HIL-1 entry and IC-OR6 are present in
    the transcript; the v2 outline is absent by inspection.
  Proposed fix: Add to the SKILL.md Phase 4 section: "For every HIL gate
    that the spec identifies as 'mandatory human review — v1,' ask whether
    the framework has a v2 automation target for this gate. If so, sketch
    the trust model preconditions for automation (what would an automated
    approver need to satisfy?) as a stub. Label it 'v2 planning target —
    not a v1 requirement.' This prevents HIL deferral from blocking v2
    planning."
```

---

```
SKILL-FRICTION-8:
  Skill: orchestration-comparativist
  Session: Session 6 — Orchestration Requirements Matrix
  Type: Tension Attribution
  Evidence: T8 (Write Lock Semantics Conflation — State Consistency vs.
    Orchestration Comparativist) in tension-map-v1.md. Status: "✅ Resolved"
    via Lock/Hold split in Session 7: Write Lock = 60 minutes (I am about
    to write); Dependency Hold = 72 hours renewable (I am waiting on
    someone else's output before I can write). In the Session 6 transcript,
    CM-3 and CM-4 treat all scope locks identically with a 60-minute TTL.
    The Dependency Hold concept is entirely absent from the Session 6 output.
  Description: The Scope Lock Registry was a primary first-class deliverable
    of Session 6 — the skill produced IC-OR4 (Orchestrator → Scope Lock
    Registry) and resolved OQ-CW1 and OQ-CW2. Yet the skill never asked:
    are there two distinct kinds of scope-related locking? A "write lock"
    says "I am actively writing to this scope right now — block others."
    A "dependency hold" says "I am waiting on another agent's output before
    I can begin writing — reserve this scope but don't consume my write TTL."
    These have different semantics, different TTLs, and different release
    triggers. The skill had the session's full lock architecture in front of
    it (escalation logic, task decomposition, retry budgets) and never
    surfaced this semantic distinction. It took Session 7's council session
    to identify and resolve it. Given that the Orchestration Comparativist
    co-owns T8, this should have been a Session 6 question.
  Confidence: Medium
    Inferred from tension map. T8 is attributed to "State Consistency vs.
    Orchestration" in the tension map; CM-3 and CM-4 are directly in the
    transcript showing uniform lock semantics.
  Proposed fix: Add to Dimension 7 (Concurrency Model) in the SKILL.md:
    "Ask: is 'I hold a scope lock to prevent writes by others' the same
    concept as 'I am waiting for a dependency in this scope before I can
    begin'? If agents can be in a pending-dependency state that blocks their
    scope region before they begin writing, a Dependency Hold with a longer
    TTL may be required as a separate lock type from the active Write Lock.
    Conflating them means active writers are penalized with TTLs designed
    for passive waiters, or vice versa."
```

---

```
SKILL-FRICTION-9:
  Skill: orchestration-comparativist
  Session: Session 6 — Orchestration Requirements Matrix
  Type: Tension Attribution
  Evidence: Pre-T3 (Validator Independence vs. Test Coverage at Scale —
    Validation Contract Architect vs. Orchestration Comparativist) in the
    pre-mapped tension section of tension-map-v1.md. Session 7 resolution
    was T2 (four-layer TGA cascade). In the Session 6 transcript, CF-5
    is listed as a non-negotiable requirement: "Enforce the 4-level validation
    cascade... with Level 3 triggered only when attention_weight ≥ 0.90 or
    Genesis-adjacent." The skill treated this as an inherited requirement
    rather than a live tension.
  Description: Pre-T3 was one of the six pre-mapped structural tensions
    explicitly built into the specialist team before Session 1 — the
    orchestration-comparativist co-owns it. The tension is: requiring TGA
    tests to be written before the Coder's output is visible (independence)
    creates a coverage problem at scale (human-authored test corpus becomes
    a bottleneck). The skill had the Session 4 Validation outputs in hand
    when building the Session 6 requirements matrix, and CF-5 is directly
    derived from Session 4. The skill had the domain responsibility to ask:
    "The validation cascade is specified, but does the independence requirement
    create a throughput ceiling? What happens when the TGA test volume
    outpaces the human corpus?" Instead, it absorbed CF-5 as a constraint
    and moved on. The pre-mapped tension should have been surfaced for
    council resolution in Session 6, not left for Session 7.
  Confidence: Medium
    Pre-T3 is a pre-mapped tension with explicit orchestration co-ownership.
    CF-5 appears in the transcript without a tension flag. Resolved in
    Session 7 via T2.
  Proposed fix: Add to the SKILL.md Phase 1 (Requirements Harvesting):
    "For requirements inherited from Session 4 (Validation), explicitly
    ask: does this requirement create a throughput or scale concern at the
    orchestration layer? The TGA independence requirement is a known tension
    point — flag it explicitly when absorbing S4 requirements rather than
    inheriting it silently." Add a cross-reference to the six pre-mapped
    tensions from skill-design-decisions.md as a mandatory review checklist
    item before Phase 2.
```

---

## Summary Table

| # | Type | Confidence | Evidence |
|---|---|---|---|
| 1 | Missed Question | High | GAP-4(b); IC-OR6/IC-OR8 missing return-path mechanism |
| 2 | Cross-Domain Miss | High | Pre-T5; HS-7 in transcript; schema extension pathway unspecced |
| 3 | Cross-Domain Miss | High | T4; OQ-GOC1 block introduces config file without governance reconciliation |
| 4 | Format Failure | High | OQ-TC3, OQ-GOC1, OQ-OC1 blocks missing "Tradeoffs decided:" field |
| 5 | Backlog Attribution | Medium | GAP-4(a); path blocks present but no conditional delegation token stubs |
| 6 | Backlog Attribution | Medium | GAP-16; IC-OR7 defines suspension states but no operator notification path |
| 7 | Backlog Attribution | Medium | GAP-13; IC-OR6 covers HIL-1 gate but no v2 trust-model preconditions sketched |
| 8 | Tension Attribution | Medium | T8; CM-3/CM-4 treat write locks and dependency holds identically |
| 9 | Tension Attribution | Medium | Pre-T3; CF-5 absorbed as requirement without surfacing TGA-independence tension |

---

## Overall Performance Summary

The `orchestration-comparativist` performed at a **high baseline** for its
primary deliverables. The requirements matrix is the most thorough artifact
of the six sessions: all eight dimensions are sourced to specific session IDs,
elimination criteria are crisply stated, all four (then five) candidates are
evaluated against a shared rubric, and the three path decision blocks are
complete, comparable, and internally consistent. The session also resolved
six of seven inherited open questions from Sessions 1–5 — a strong closure
rate. The orchestrator-owned interface contracts (IC-OR1 through IC-OR9)
are structurally sound.

The skill's systematic weakness is **integration blindness at the boundary
of its synthesis role**. As the declared synthesis layer — the skill that
connects all five peer domains — the orchestration-comparativist should
naturally surface tensions and gaps that live at domain edges. Instead,
it consistently absorbed inputs from peer sessions as fixed constraints and
moved toward evaluation rather than pausing to ask whether the constraints
themselves implied cross-domain tensions. Three of the four High-confidence
friction items (FRICTION-1, FRICTION-2, FRICTION-3) are failures of this
kind: the HIL return mechanism (a boundary between orchestration and human
interaction design), the schema extension pathway (a boundary between
orchestration and schema governance), and config file authority fragmentation
(a boundary between orchestration and security governance) — all were visible
in the session material but were not flagged. The format failures (FRICTION-4)
reveal a secondary pattern: the skill compresses its output quality as a
session progresses, producing complete spec blocks early and truncated ones
late. Together, these patterns suggest the skill would benefit from an
explicit cross-domain synthesis pass at the end of Phase 2 (before producing
the evaluation grid) and a spec block format self-check at the end of the
session.

---

*Friction analysis generated against: transcript-session-6-orchestration.md,
gap-backlog-v1.md, tension-map-v1.md, orchestration-comparativist SKILL.md*

*Entries are evidence-grounded. No friction items were invented.*
