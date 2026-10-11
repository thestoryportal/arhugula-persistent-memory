# Skill Friction Analysis — `memit-specialist`
## Session Analyzed: Session 2 — MEMIT Implementation Specification and Design

```
Artifact type:   Skill Friction Log
Skill:           memit-specialist
Session:         2 — Write Engine, .vindex overlay, .larql format, MEMIT selection
Evidence base:   transcript-session-2-engine.md
                 memit-specialist-spec-design.md (session summary)
                 gap-backlog-v1.md
                 tension-map-v1.md
                 skill-design-decisions.md (pre-mapped tensions)
Analyst:         Post-session friction review
Status:          Draft
```

---

## Evidence Index

| Source | Referenced As |
|--------|--------------|
| Session 2 transcript | `transcript` |
| Session 2 summary (memit-specialist-spec-design.md) | `S2-summary` |
| Gap Backlog v1 (gap-backlog-v1.md) | `gap-backlog` |
| Tension Map v1 (tension-map-v1.md) | `tension-map` |
| Skill Design Decisions (skill-design-decisions.md) | `skill-design` |
| MEMIT Specialist SKILL.md | `SKILL.md` |

---

## Friction Entries

---

### SKILL-FRICTION-1

```
Skill:      memit-specialist
Session:    2 — Write Engine Design
Type:       Missed Question
Confidence: High
```

**Evidence:** The transcript shows the skill specced `attention_weight` as an agent-declared
numeric field (`[0.0, 1.0]`, constraint C13, `S2-summary`) and deferred the authority question
as OQ-W5 ("attention_weight: agent-declared vs. engine-computed") without probing it as a
potential category error during Phase 1. In Session 7, this became TENSION-T1 — the skill's
most expensive revision. The `attention_weight` field was not merely reassigned; it was split
into two conceptually distinct things: `declared_importance` (agent-authored enum: CORE /
SUPPORTING / INCIDENTAL) and `attention_weight` (engine-computed, never agent-authored). The
resolution also required extending IC-SC1, revising D18's behavioral probe trigger threshold,
and producing a post-compile divergence check protocol (`tension-map`, T1).

**Description:** The skill's Phase 1 inquiry (transcript, three questions before spec
synthesis) asked about permanence, edit volume, and behavioral verification — all correct.
It did not ask: *"Should agents be allowed to declare the injection weight for an edge, or is
that a MEMIT engine concern?"* This question is the logical follow-on to the Verification
Gap explanation the skill itself provided: the skill correctly explained that MEMIT's
covariance balancer controls injection math, then produced a spec that let agents override
that math via an agent-declared float. The skill's own domain knowledge made this a
proachable question in Phase 1. The `SKILL.md` lists six Socratic probes in the Phase 1
section; none target weight authority. This is a systematic gap in the inquiry protocol.

**Proposed fix:** Add one probe to the Phase 1 inquiry list in `SKILL.md`:

> *"MEMIT's covariance balancer computes injection weight during compilation. Do you want
> agents to be able to declare how much weight an edge should carry, or should injection
> strength be an engine-internal concern derived from metadata the agent can set (like
> importance level)? These are different architectures with different security and
> correctness implications."*

Also add to the **Spec Output Checklist**:

> `[ ] Injection weight authority decided: engine-computed vs. agent-declared — confirmed with
>     reasoning. If agent-declared: attack surface and override risk documented.`

---

### SKILL-FRICTION-2

```
Skill:      memit-specialist
Session:    2 — Write Engine Design
Type:       Spec Output Gap
Confidence: High
```

**Evidence:** Decision D18 (S2-summary) reads: "Post-write verification is two-level:
Level 1 storage probe (SELECT read-back, mandatory for all writes) + Level 2 behavioral probe
(generation test, mandatory for high-weight edges ≥ 0.85)." The trigger threshold `≥ 0.85` is
a numeric threshold on `attention_weight`. TENSION-T1 (tension-map, T1) established that
`attention_weight` is not an agent-authored field at all — it is engine-computed post-compile
and not available *pre-commit* when the Validator must decide whether to run the L2 behavioral
probe. D18's threshold was therefore built on a concept that the skill's own domain should
have recognized as architecturally misplaced: you cannot gate a pre-commit Validator decision
on a post-compile engine output.

**Description:** The Post-Write Verification Protocol spec block (transcript) defines the
behavioral probe trigger as `attention_weight >= 0.85` without noticing that this creates a
circular dependency: the behavioral probe must run *before* commit, but its trigger condition
(`attention_weight`) is only available *after* MEMIT compiles. The Session 7 resolution
replaced this with `declared_importance = CORE or SUPPORTING` — a pre-compile, agent-authored
signal that the Validator can act on. The D18 spec block as written would have blocked the
Validation session (Session 4) from completing its probe trigger spec without surfacing this
circularity. The MEMIT Specialist owns both the compile sequence and the post-write
verification protocol; this contradiction is fully internal to the skill's domain and should
have been caught before the spec block was finalized.

**Proposed fix:** Add to the **Spec Output Checklist** in `SKILL.md`:

> `[ ] Behavioral probe trigger: confirmed that trigger condition is available at pre-commit
>     Validator time (not post-compile only). Engine-computed outputs cannot gate pre-commit
>     decisions.`

Add to the **Key Risks** section a sixth risk:

> **6. Verification Sequencing Conflict** — Post-write verification decisions (which probe to
> run, whether to require it) must be gateable by the Validator *before* MEMIT compiles. Any
> probe trigger condition based on MEMIT-computed outputs creates a circular dependency. When
> speccing the verification protocol, confirm each trigger is a *pre-compile* signal.

---

### SKILL-FRICTION-3

```
Skill:      memit-specialist
Session:    2 — Write Engine Design
Type:       Backlog Attribution
Confidence: High
```

**Evidence:** OQ-W6 (`.larql` schema versioning strategy) was deferred in Session 2 with
the label "Deferred" (S2-summary). GAP-3 in the gap backlog (`gap-backlog`, GAP-3) classifies
this as **🔴 Critical** — one of the three highest-priority gaps in the entire framework spec.
The gap note further observes that the Session 7 T1 resolution (splitting `attention_weight`
into `declared_importance` + engine-computed weight) immediately creates the first v1 → v2
`.larql` schema migration use case: the `attention_weight` field in existing patches must be
handled when the new schema takes effect. The gap blocks: Gate pre-check spec completeness,
Validator L1 static analysis completeness, the compaction re-run strategy for superseded
patches across version boundaries, and all v2 migration planning.

**Description:** OQ-W6 was deferred without probing. The Session 2 `.larql` format spec
block defines the canonical format in detail — four sections, field constraints, compiler
directives — without raising the question: *"What happens when this format needs to change?"*
The SKILL.md checklist item reads: "`.larql` as the exclusive agent-facing interface —
confirmed or alternative specified." This confirms the interface exists but does not require
the skill to probe what happens when that interface evolves. For any format that is defined
as the *exclusive* agent-facing interface and that is committed to Git alongside code, schema
versioning is not a deferred refinement — it is a load-bearing requirement that must be
addressed before the format is finalized. The Session 2 summary acknowledges OQ-W5
("MUST RESOLVE before `.larql` format is final") but OQ-W6 carries no such flag, even though
it is equally a prerequisite for finalizing the format.

**Proposed fix:** Add OQ-W6 to the same must-resolve bucket as OQ-W5 in the skill's
understanding of what blocks format finalization. Specifically, add to the **Spec Output
Checklist**:

> `[ ] .larql schema versioning addressed: is there a schema version header field?
>     What does the write engine do with patches authored under an older schema version?
>     NOTE: This must be resolved before the .larql format is declared final — it is
>     load-bearing for Gate pre-checks, Validator L1 static analysis, and compaction.`

---

### SKILL-FRICTION-4

```
Skill:      memit-specialist
Session:    2 — Write Engine Design
Type:       Tension Attribution
Confidence: Medium
```

**Evidence:** `skill-design-decisions.md` pre-maps six structural tensions baked into the
council skill before Session 1. Two of these directly name the MEMIT Specialist as a party:
Pre-T2 (Write volume vs. edit locality guarantees — Graph Data Architect vs. MEMIT Specialist)
and Pre-T6 (Genesis comprehensiveness vs. Genesis brittleness — Graph Data Architect vs. MEMIT
Specialist). Both were first surfaced as explicitly cross-domain tensions in Session 7 (T6 for
Pre-T6; T6 for Pre-T2, `tension-map`, Pre-T2, Pre-T6). The Session 2 summary block lists
interface contracts with the Validator, State Ledger, and Orchestrator, but no interface
contract or cross-domain flag is directed toward the Graph Data Architect.

**Description:** The MEMIT Specialist was a named party in two of the six pre-mapped tensions.
The individual `SKILL.md` contains no reference to these pre-mapped tensions, no instruction
to proactively flag them as cross-domain concerns in the session summary, and no prompt to
produce an interface contract stub for the Graph Data Architect. As a result, the Genesis
comprehensiveness vs. brittleness tension and the write volume vs. locality tension were
handled inside Session 2 as MEMIT-internal thresholding problems (D21, OQ-W1) rather than
flagged as requiring negotiation with the schema layer. When T6 surfaced in Session 7, it
required a three-part resolution — Genesis scope test, drift-from-anchor model, and Architect
capacity model — none of which were pre-positioned by Session 2's output. The tensions were
resolvable but required Session 7 to reconstruct the Graph Data Architect's requirements from
scratch rather than building on a carried-forward framing.

**Proposed fix:** Add a **Pre-Mapped Tensions** section to the MEMIT specialist `SKILL.md`,
immediately after the Operating Mode section:

> ## Pre-Mapped Cross-Domain Tensions
>
> The following tensions are structural to this skill's domain and will arise in almost every
> session where the MEMIT Specialist produces spec output. Flag these explicitly — do not
> resolve them unilaterally.
>
> - **Write Volume vs. Edit Locality (Pre-T2):** Every edit volume estimate or drift threshold
>   produced by this skill is in tension with the Graph Data Architect's schema expressivity
>   requirements. Flag threshold decisions as "pending Graph Data Architect alignment" in the
>   session summary. Produce an interface contract stub addressing this tension.
>
> - **Genesis Completeness vs. Genesis Lock-in (Pre-T6):** Genesis scope decisions are jointly
>   owned with the Graph Data Architect. Any Genesis tier structure, modification policy, or
>   edit volume ceiling proposed in a MEMIT session must be flagged as "requires Graph Data
>   Architect input" rather than resolved as a MEMIT-internal decision.
>
> - **Audit Completeness vs. Write Throughput (Pre-T4):** Write engine latency decisions are
>   in tension with the Warden's audit trail completeness requirement. Flag when write engine
>   design choices affect commit critical path latency.

---

### SKILL-FRICTION-5

```
Skill:      memit-specialist
Session:    2 — Write Engine Design
Type:       Tension Attribution
Confidence: Medium
```

**Evidence:** OQ-W10 in the Session 2 summary reads: "Overlay compaction: full MEMIT re-run
vs. delta composition → INPUT REQUIRED: Session 5 (State Consistency)." The question is
framed as neutral — a decision deferred for input from another session. In Session 7, this
became TENSION-T9 (Compaction correctness vs. efficiency, `tension-map` T9). The resolution
rejected delta composition on correctness grounds: "MEMIT's correctness guarantees
(orthogonal projection, covariance balancer) are applied *during* a compile run. Delta
composition skips these steps for already-compiled layers." The objection came from the
Validation Contract Architect, not from the MEMIT Specialist.

**Description:** The MEMIT Specialist owns both MEMIT's mathematical correctness properties
(described in detail in `SKILL.md` under "Where it breaks down") and the `.vindex` overlay
architecture. OQ-W10 asked the right question but answered it neutrally ("full re-run vs.
delta composition — deferred") when the MEMIT domain knowledge available in the same
`SKILL.md` already implies the answer: delta composition is not a formally studied MEMIT
technique, and the orthogonal projection and covariance balancer steps that the skill mandated
in D20 are *compile-time operations* — they cannot be retroactively applied to already-compiled
deltas. The specialist deferred a question it had the domain knowledge to foreclose, leaving
the Validation Contract Architect to carry the correctness argument into Session 7. The MEMIT
Specialist should have stated: "Delta composition is not mathematically well-defined for MEMIT.
Full re-run is the only approach with correctness guarantees. This is not a design choice —
it is a constraint."

**Proposed fix:** Add to the **Key Risks** section of `SKILL.md`:

> **Compaction Correctness:** Delta composition for compaction is not a formally studied MEMIT
> technique. MEMIT's locality and correctness properties (orthogonal projection, covariance
> balancer) are applied during a compile run on the full fact set. Composing pre-compiled
> deltas skips these steps and has undefined correctness behavior. When compaction strategy
> is raised, foreclose delta composition as a MEMIT constraint, not a design choice. Full
> re-run is mandatory.

Also update OQ-W10's wording recommendation — rather than being a neutral "A vs. B", the
skill should produce this as a one-way constraint: "Compaction MUST be a full MEMIT re-run.
Delta composition is excluded on correctness grounds (D20). Interface contract with Pruning
Agent must specify full re-run trigger conditions."

---

### SKILL-FRICTION-6

```
Skill:      memit-specialist
Session:    2 — Write Engine Design
Type:       Spec Output Gap
Confidence: Medium
```

**Evidence:** IC5 (Write Engine ← Validator, S2-summary) specifies seven things the Validator
confirms before a patch reaches the write engine: base_type declared, relation labels in
vocabulary, `violates` absent, TIER declared, `attention_weight` in range, transaction
bracketed, and schema-validated. Schema version conformance is not listed. GAP-3
(`gap-backlog`, GAP-3) specifically calls out that "the seven pre-checks in §10.2 may be
incomplete without a schema version check" and that the Warden flagged this as a potential
trust-boundary gap: "an attacker who can replay a patch authored under an older schema version
might bypass Validator checks added in the newer version." This security note was added in
Session 7; it traces back to IC5's omission.

**Description:** IC5 is the contract that defines what "pre-validated" means when a patch
reaches the write engine. Schema version conformance is a pre-commit, format-level check —
it belongs in this contract. Its absence meant the Gate's pre-check list was produced without
a schema version slot, the Validator's L1 static analysis was produced without a version
conformance gate, and GAP-3 ended up Critical. Since OQ-W6 was deferred without probing,
the IC5 contract was finalized without the version check that OQ-W6 would have motivated.
The two gaps (OQ-W6 deferral and IC5 omission) are causally linked.

**Proposed fix:** Add to the IC section of the **Spec Output Checklist** in `SKILL.md`:

> `[ ] IC5 (Write Engine ← Validator) includes schema version conformance as a pre-check.
>     If schema versioning is deferred (OQ-W6), mark schema version check as a TBD slot in
>     IC5 rather than omitting it — the slot must exist so downstream Gate and Validator specs
>     can be written correctly.`

---

### SKILL-FRICTION-7

```
Skill:      memit-specialist
Session:    2 — Write Engine Design
Type:       Missed Cross-Domain Implication
Confidence: Medium
```

**Evidence:** The Session 2 summary (S2-summary) correctly flags: "OQ-W5 (attention_weight
authority) has security implications — Warden should weigh in before this is closed." This
is a credit. However, the specific attack vector was not articulated: an agent declaring
`attention_weight = 1.0` on a target edge can use the write engine as a vehicle to overpower
adjacent knowledge — effectively a denial-of-service on a knowledge cluster. The Warden's
security session (Session 3) would have needed this framing to design the write engine's
pre-MEMIT filter correctly. The Warden's supply chain integrity work (`.larql` patch
integrity, trust boundary between Coder Agent and write engine) was scoped without a
concrete injection-weight manipulation threat model.

**Description:** The cross-domain implication the skill needed to surface was: *"Agent-declared
`attention_weight` is not merely an accuracy risk — it is a write-layer attack surface. An
agent with the ability to declare injection weights can amplify injection of any edge to
suppress competing knowledge. The write engine's pre-MEMIT filter should treat out-of-range
weights as hard rejections (C13, correctly specced) but should also flag suspiciously high
weights on edges that already have competing signals. This threat model should be handed to
the Warden as a concrete scenario for the security session."* Without this framing, C13 (range
check) was specced but the qualitative threat (weight manipulation as an adversarial input)
was not.

**Proposed fix:** Add to the **Interface contract** template in the SKILL.md operating mode:
when handing off a security-adjacent open question to the Warden, include a threat scenario
framing, not just a flag. Suggested addition to the "Key Risks" section under item 3
(Concurrent Write Conflicts):

> **Injection Weight Manipulation:** Agent-declared injection weights (if permitted) create
> an adversarial input surface. An agent can use high `attention_weight` values to suppress
> competing knowledge by overpowering existing feature vectors. When passing `attention_weight`
> authority questions to the Warden, include this as a concrete threat scenario — not just a
> flag that security implications exist.

---

### SKILL-FRICTION-8

```
Skill:      memit-specialist
Session:    2 — Write Engine Design
Type:       Spec Output Gap
Confidence: Medium
```

**Evidence:** The transcript's thought process (transcript, internal reasoning block before
spec synthesis) references the L1 Cache concept twice: "The L1 Cache concept from earlier
(batching small patches before triggering MEMIT) fits naturally here" and "the L1 Cache
batches individual `.larql` patches (5-20 facts each) before batch processing." Decision D13
(S2-summary) references Incremental Mode as "buffered via L1 Cache before MEMIT compile."
No L1 Cache spec block was produced. The cache's hard constraints — maximum buffer size,
flush trigger conditions, failure behavior when the cache is full or a buffered patch is
invalidated before flush — are entirely absent from Session 2's output.

**Description:** The L1 Cache is a component with behavioral requirements that affect the
write engine's correctness guarantees. If a buffered patch is invalidated (e.g., a
conflicting patch is committed while the original is in the cache), the cache must either
flush immediately, reject the new patch, or apply merge logic. None of these behaviors are
specced. The L1 Cache concept was introduced in the transcript's reasoning as a natural fit
but was then incorporated into D13 as a decision without receiving its own spec block. The
Spec Output Checklist in `SKILL.md` lists "Concurrent write strategy defined" but this refers
to write-level concurrency; the L1 Cache's buffer-level behavior is a separate concern that
the checklist does not require.

**Proposed fix:** Add to the **Spec Output Checklist** in `SKILL.md`:

> `[ ] If L1 Cache / buffering layer is introduced: a spec block MUST be produced covering:
>     (a) maximum buffer capacity, (b) flush trigger conditions (size threshold? time? external
>     signal?), (c) behavior when a buffered patch becomes invalid before flush,
>     (d) ordering guarantees for patches flushed in a single MEMIT compile.`

---

### SKILL-FRICTION-9

```
Skill:      memit-specialist
Session:    2 — Write Engine Design
Type:       Backlog Attribution
Confidence: Medium
```

**Evidence:** GAP-11 (`gap-backlog`, GAP-11) is jointly attributed to State Consistency
Theorist and MEMIT Specialist. It describes a scenario where Layer 4 domain knowledge is
written from external documents (third-party API descriptions, reference specs) and those
documents later change or disappear. The `.larql` patch and Ledger record survive, but the
harness has no mechanism to detect that the authoritative source has changed. The Session 2
spec work produced the `.vindex` tier architecture (spec block in transcript) describing L4
as "foundational domain facts, patchable" — but never probed what happens when the source
of a Layer 4 fact is an external document that can change independently of Git.

**Description:** The MEMIT Specialist owns the `.vindex` overlay architecture and the L4
tier semantics. The question "when a Layer 4 fact was written from an external source, can
that source's hash be pinned at write time?" is a MEMIT-domain question about what metadata
the `.larql` format should carry and whether the `.vindex` overlay should record provenance.
It was never asked. The L4 tier spec block does not mention external document provenance.
GAP-11 is self-contained (blocks nothing in v1) but reflects a blind spot in how the skill
probed L4 write-time data: the skill asked about edit volume, not about what backs the facts
being injected.

**Proposed fix:** Add to the Phase 1 **Framing Questions** section of `SKILL.md`:

> *"For Layer 4 (updatable domain knowledge): will any Layer 4 facts be sourced from external
>  documents — API specifications, third-party reference materials, documents outside the Git
>  repository? If so, should the `.larql` patch record the source URL or document hash at
>  write time, so that the system can detect when a Layer 4 fact's source has changed?"*

---

### SKILL-FRICTION-10

```
Skill:      memit-specialist
Session:    2 — Write Engine Design
Type:       Missed Question
Confidence: Medium
```

**Evidence:** OQ-W6 (`.larql` schema versioning strategy) is listed in the Session 2 deferred
questions as simply "Deferred" with no probe record in the transcript. GAP-3's description
(`gap-backlog`, GAP-3) notes that the v1 → v2 migration has its first concrete use case in T1
(the `attention_weight` → `declared_importance` split), meaning the Session 7 T1 resolution
immediately required the versioning strategy that OQ-W6 deferred. A probing question in
Phase 1 about format evolution would have surfaced this dependency during Session 2, before
four spec blocks using the `attention_weight` field were written.

**Description:** The `.larql` format spec block produced in Session 2 defines a concrete
four-section format including `attention_weight` as a required field. Any format that (a) is
declared the exclusive agent-facing interface, (b) is committed to Git, and (c) is consumed
by multiple downstream components (Gate, Validator, Write Engine, compaction re-run) needs a
versioning strategy before the format is finalized — not after. The skill deferred OQ-W6
without asking: *"If we need to change this format — say, add a field, remove a field, or
rename one — what does the write engine do with patches authored against the old format?
Does the patch carry a schema version number?"* This question could have been asked in Phase 1
before the format spec was written. It was not.

**Proposed fix:** Add to the **Phase 1 Socratic Inquiry** section of `SKILL.md`, after the
current six questions:

> - Does the `.larql` format need to support multiple versions? If an agent generates a patch
>   under schema v1 and the format has evolved to v2, what should the write engine do —
>   reject, auto-migrate, or escalate? NOTE: This must be decided before the format is
>   finalized, because it determines whether the format carries a version header field and
>   whether the Gate and Validator need schema version conformance checks.

---

## Performance Summary

The `memit-specialist` skill performed well on the structural work it was most explicitly
prepared for. It correctly ran Phase 1 Socratic inquiry before spec synthesis; it surfaced the
behavioral probe gap (the MEMIT reporting vs. behavioral use distinction) proactively and named
`storage-pass / behavior-fail` as a first-class failure mode; it produced well-structured spec
blocks in the required format; it resolved two Session 1 open questions (OQ1 and OQ4) cleanly;
and it correctly identified that several deferred questions required input from specific
downstream sessions, routing them appropriately. These are genuine strengths.

The skill's systematic weakness is a pattern of *treating its own internal decisions as
domain-local when they had cross-domain reach*. Two pre-mapped tensions — Pre-T2 (write
volume vs. edit locality, involving the Graph Data Architect) and Pre-T6 (Genesis
completeness vs. brittleness, jointly owned with the Graph Data Architect) — were handled
inside Session 2 as MEMIT-internal thresholding problems rather than flagged as requiring
negotiation with the schema layer. The `SKILL.md` does not list these pre-mapped tensions
or instruct the skill to carry them forward as explicit interface stubs. Similarly, the
`attention_weight` authority question (SKILL-FRICTION-1, the most expensive single friction
item) was left as a deferred open question rather than probed in Phase 1, despite the skill's
own domain knowledge making it a natural inquiry target. And the `.larql` format spec was
finalized without a schema versioning slot, producing a Critical gap (GAP-3) because a
format declared as the exclusive interface was shipped without an evolution strategy. In short:
the skill does its domain work correctly when focused on a component in isolation, but
consistently underinvests in surfacing the load-bearing assumptions that adjacent skills
and future sessions will need to carry.

---

## Friction Summary Table

| ID | Type | Confidence | Evidence Root | Downstream Impact |
|----|------|------------|---------------|-------------------|
| SKILL-FRICTION-1 | Missed Question | High | T1 (attention_weight authority — Session 7 revision) | Most expensive single revision in spec; revised D18, IC5, IC-SC1 |
| SKILL-FRICTION-2 | Spec Output Gap | High | T1 / D18 threshold built on post-compile concept | D18 behaviorally inconsistent; blocked Validator probe trigger spec |
| SKILL-FRICTION-3 | Backlog Attribution | High | GAP-3 (🔴 Critical — .larql schema versioning) | Blocks Gate pre-check, Validator L1, compaction re-run, v2 planning |
| SKILL-FRICTION-4 | Tension Attribution | Medium | Pre-T2, Pre-T6 not surfaced in S2 | Both required Session 7 resolution from scratch |
| SKILL-FRICTION-5 | Tension Attribution | Medium | T9 (delta composition correctness — should have been foreclosed) | Validation Architect carried argument the MEMIT Specialist owned |
| SKILL-FRICTION-6 | Spec Output Gap | Medium | GAP-3 / IC5 missing schema version conformance | Gate pre-check spec incomplete; security gap noted by Warden |
| SKILL-FRICTION-7 | Cross-Domain Miss | Medium | IC8 / Warden handoff missing threat scenario | Warden's filter spec written without weight manipulation attack model |
| SKILL-FRICTION-8 | Spec Output Gap | Medium | L1 Cache in D13 without spec block | Buffer behavior, flush triggers, invalidation behavior unspecced |
| SKILL-FRICTION-9 | Backlog Attribution | Medium | GAP-11 (Layer 4 external doc provenance) | No provenance mechanism in .larql format or .vindex tier spec |
| SKILL-FRICTION-10 | Missed Question | Medium | OQ-W6 deferred without probing | First v2 migration use case created by T1 before versioning strategy existed |

---

*Skill Friction Log v1.0 — memit-specialist — Session 2*
*10 friction entries: 3 High confidence, 7 Medium confidence*
*0 instances invented — all evidenced in transcript, gap backlog, or tension map*
