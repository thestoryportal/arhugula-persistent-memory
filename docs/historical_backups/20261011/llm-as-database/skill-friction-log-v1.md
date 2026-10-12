# Skill Friction Analysis Report
## Skill: `graph-data-architect`
## Session Analyzed: Session 1 — Ontological Schema for LLM Database Agent Framework

> **Analysis conducted:** Post-session audit using full transcript, session summary
> (`ontological-schema-llm-databse-agent-framework.md`), gap backlog (`gap-backlog-v1.md`),
> and cross-domain tension map (`tension-map-v1.md`).
>
> **Method:** Evidence-first. Every entry is anchored to a specific location in the transcript
> or a specific gap/tension ID. No friction was invented.
>
> **Confidence key:**
> - **High** = directly evidenced in the session transcript
> - **Medium** = inferred from gap backlog or tension map attribution

---

## Friction Entries — Sorted by Confidence, then by Type

---

### SKILL-FRICTION-1

```
Skill:    graph-data-architect
Session:  Session 1 — Ontological Schema
Type:     Missed Cross-Domain Implication
```

**Evidence:**
TENSION-T1 in `tension-map-v1.md`:

> *"The original `.larql` format had `attention_weight` as an agent-authored field — the agent
> declared how much weight a given edge should carry. The MEMIT Specialist objected:
> `attention_weight` is computed by MEMIT's covariance balancer math during compile. Letting
> agents author this number means agents are claiming to know what MEMIT will produce — a
> category error."*

In the transcript, IC1 (the interface contract to the write engine) was defined without any
distinction between agent-authored fields and engine-computed fields in the `.larql` format.
The `verified_at` Namespace Relation in the Relation Vocabulary spec block confirms the skill
was thinking about edge-level metadata — but never asked who *writes* numeric metadata fields.

**Description:**
When defining the triple model and the Namespace Relations (specifically `verified_at` and
`scoped_to`), the skill introduced edge-level metadata as a concept. This was the natural
moment to ask: *"For any numeric or scored metadata on an edge — importance, confidence,
verification weight — who is the authoritative author? The agent submitting the patch, or
the write engine at compile time?"*

The skill did not ask this. The `.larql` patch format implied by IC1 left field authorship
ambiguous. The MEMIT Specialist inherited this ambiguity and the conflict surfaced as T1
in Session 7 — requiring a retroactive split into `declared_importance` (agent-authored enum)
and `attention_weight` (engine-computed float). T1 is noted as the trigger for GAP-3's first
concrete use case (a `.larql` schema version change).

**Confidence:** High

**Proposed fix:**
Add the following to the **Useful Framing Questions** section of `SKILL.md`:

> *"For any metadata field attached to an edge — importance weights, confidence scores,
> verification timestamps — who is the authoritative author: the agent writing the patch, or
> the write engine at compile time? These must be distinguished in the `.larql` field spec.
> An agent-authored field is a semantic claim; an engine-computed field is a mathematical
> result. Conflating them creates a category error the write engine cannot resolve."*

Add to **Key Risks to Surface in Spec Conversations**:

> **7. Agent-authored vs. engine-computed field conflation** — If the `.larql` patch format
> includes numeric fields (weights, scores, importance values) without specifying their
> authorship domain, the write engine spec will inherit an unresolvable ambiguity. Surface
> this boundary before the MEMIT Specialist session begins.

---

### SKILL-FRICTION-2

```
Skill:    graph-data-architect
Session:  Session 1 — Ontological Schema
Type:     Format Failure
```

**Evidence:**
The project-level required spec block format (from project system prompt) is:

```
### [Component] — Spec Block
What it must do / represent / enforce / guarantee:
Hard constraints:
Tradeoffs decided:
Open questions (deferred):
Interface contract:
```

All four spec blocks produced in Session 1 — Entity Type Taxonomy, Primary Query Patterns,
Relation Vocabulary, and Project Genesis Scope — are missing the **"Tradeoffs decided"** field
entirely. Significant tradeoff decisions were made during the session (Option 2 over Options 1
and 3 for entity taxonomy; why `violates` is ephemeral-only; synonym collision policy
rationale; the schema partition rule) but all were captured in prose discussion rather than in
the required spec format field. Session 7 had to retroactively reconstruct tradeoff rationale
for the T6 and Pre-T2 tensions.

**Description:**
The skill's `SKILL.md` defines its own internal Phase 2 format, which is richer than the
project-level format (it includes "Triple schema," "Query patterns required," "Polysemantic
risk zones"). However, the skill's internal format does *not* include "Tradeoffs decided" —
which is a mandatory field in the project's master spec format. The result is that every spec
block the skill produces is structurally missing the tradeoffs field, session after session.
This is not a one-off omission; it is a systematic gap caused by the skill's internal template
not including a field the project requires.

**Confidence:** High

**Proposed fix:**
Add "Tradeoffs decided" as an explicit field in the skill's **Phase 2: Spec Synthesis**
template in `SKILL.md`:

```
**Tradeoffs decided:**
- [Option chosen] over [Option(s) rejected] because [explicit rationale]
- ...
```

Add a note: *"This field is mandatory in the project spec format. Capture tradeoffs decided
during the Socratic Inquiry phase here — do not leave them only in prose discussion."*

---

### SKILL-FRICTION-3

```
Skill:    graph-data-architect
Session:  Session 1 — Ontological Schema
Type:     Spec Output Gap
```

**Evidence:**
Second response (transcript lines 333–349) — first Genesis layer proposal:

```
Layer 1 — The Entity Taxonomy itself
Layer 2 — The Relation Vocabulary itself
Layer 3 — Domain Knowledge (Q5 answer)
Layer 4 — Project Constraints (unnamed at that point)
```

Final Genesis Scope spec block (transcript lines 880–988) — final structure:

```
L1 — Schema Constitution (entity types + relation families combined)
L2 — Domain Extension Declarations (project-specific subtypes)
L3 — Project Constitutional Constraints (architectural rules)
L4 — Foundational Domain Knowledge (framework docs)
```

Partial session summary (transcript lines 644–681) — uses the old structure:
> *"NEXT REQUIRED: Relation Vocabulary spec block — What relation types are allowed?..."*
(still treating entity taxonomy and relation vocabulary as separate layers)

**Description:**
The Genesis layer structure was reorganized mid-session in a meaningful way: Layers 3 and 4
were swapped (project constraints moved up; domain knowledge moved down), and Layers 1 and 2
were collapsed into a single Schema Constitution. This reorganization is architecturally
significant — it changes the write order and the relative immutability of each layer. However,
no explicit decision marker was recorded for the reorganization, no tradeoff rationale was
documented (why collapse L1+L2?), and the intermediate partial session summary (lines 644–681)
was left inconsistent with the final structure. The session ended with the spec and the
summary in divergent states on this question — the Summary Block at lines 1004–1150 uses the
corrected four-layer structure, but a reader comparing the partial summary to the final spec
would find no explanation for the change.

**Confidence:** High

**Proposed fix:**
Add to the **Spec Output Checklist** in `SKILL.md`:

> - [ ] If any spec block was revised after initial drafting, a "Revision note" entry is
>       present in the spec block documenting what changed and why. No silent structural
>       reorganizations.

Add to the **Operating Mode** section:

> *"If a spec block is revised mid-session (e.g., a layer structure is reorganized), produce
> an explicit decision marker before the revised block: `> REVISED: [what changed and why].`
> Do not silently supersede draft output — the revision itself is part of the spec record."*

---

### SKILL-FRICTION-4

```
Skill:    graph-data-architect
Session:  Session 1 — Ontological Schema
Type:     Backlog Attribution
```

**Evidence:**
GAP-3 in `gap-backlog-v1.md`:

> *"Domain(s): MEMIT Specialist, Graph Data Architect — The `.larql` schema versioning
> strategy is deferred to v2. The spec does not define: How the Validator handles `.larql`
> patches authored under an older schema version than the current spec. Whether `.larql`
> patches carry a schema version header field..."*

OQ5 in session summary (the closest the skill came):
> *"Triple model vs. quad model — does `verified_at` need a fourth field per edge?"*

GAP-3 is marked **Critical** (blocks 4+ other gaps). The Graph Data Architect is named as a
joint domain owner.

**Description:**
The skill defined the schema constitution (Genesis Layer 1) as the graph's self-knowledge —
the entity types and relation families encoded as triples that the Validator reads to enforce
schema compliance. This was a correct and well-executed decision. However, the skill never
asked the next question: *"What happens when the schema constitution itself needs to change?
Does a `.larql` patch carry a schema version header? How does the Validator detect that a
patch was authored against an outdated schema version?"*

OQ5 (triple vs. quad model) touched the adjacent problem — whether individual edges need a
timestamp fourth field — but framed it as a data model granularity question, not as a schema
versioning strategy. These are different concerns. The schema version question belongs
squarely in the Graph Data Architect's domain: it is a contract on the `.larql` format, and
the `.larql` format is the interface contract this skill produces. Not raising it means the
MEMIT Specialist and Validation Contract Architect inherited an underspecified contract, and
the gap became critical.

**Confidence:** High

**Proposed fix:**
Add the following to **Useful Framing Questions** in `SKILL.md`:

> *"What happens when the schema itself needs to change after Genesis? Does a `.larql` patch
> carry a schema version header field? What does the Validator do when it receives a patch
> authored against schema version N-1? This is the schema versioning question — distinct from
> the quad model question (timestamps on individual edges). Surface it before handing off to
> the MEMIT Specialist."*

Add to **Interface contract with MEMIT Specialist** in the Spec Output Checklist:

> - [ ] Schema version header field on `.larql` patches: defined or explicitly deferred with
>       a named open question for the Validation Contract Architect session.

---

### SKILL-FRICTION-5

```
Skill:    graph-data-architect
Session:  Session 1 — Ontological Schema
Type:     Missed Cross-Domain Implication
```

**Evidence:**
Decision D4 in session summary:
> *"Bidirectional traversal required. All edges must support reverse lookup. No write-only
> edges."*

Interface Contract IC1 in session summary:
> *"Write engine (MEMIT Specialist): Receives entity base type tag to determine target FFN
> layers — Receives relation family tag to determine injection strategy — Must enforce hard
> rejection of `violates` relation at compile time — Genesis Patch (.larql) is first input —
> mints project_v1.vindex"*

IC1 contains four items. None of them mention reverse edge storage, reverse index requirements,
or bidirectional traversal implications.

**Description:**
D4 is one of the ten decisions made in Session 1 — bidirectional traversal is a hard
architectural requirement. This decision has a direct implication for the write engine: MEMIT
must be able to support lookups in the form `SELECT entity FROM EDGES WHERE target = X`.
Whether this is implemented by writing two edges per relationship (forward and reverse), by
maintaining a separate reverse lookup index, or by some other mechanism is the MEMIT
Specialist's decision — but they cannot make it without knowing the requirement exists.

IC1 (the interface contract to the write engine) is the vehicle for forwarding this
requirement. It does not mention it. The MEMIT Specialist's session would have needed to
independently re-derive this requirement, or the gap would surface as an underspecified
interface in integration.

**Confidence:** High

**Proposed fix:**
Add to the **Interface contract with MEMIT Specialist** checklist item in `SKILL.md`:

> - [ ] Bidirectional traversal requirements explicitly forwarded: if D-equivalent "all edges
>       must support reverse lookup" is established, IC1 must include a line specifying that
>       the write engine must support reverse edge retrieval. The implementation strategy
>       (dual-write vs. reverse index vs. computed reverse) is the MEMIT Specialist's decision,
>       but the requirement is the Graph Data Architect's to declare.

---

### SKILL-FRICTION-6

```
Skill:    graph-data-architect
Session:  Session 1 — Ontological Schema
Type:     Spec Output Gap
```

**Evidence:**
Project Genesis Scope spec block (transcript lines 875–988): contains "What it must represent,"
four Genesis layers with SQL examples, "What Does NOT Belong in Genesis" table, "Hard
constraints," and "Open questions." No "Interface contract" section is present in the spec
block itself.

The Genesis interface contract language appears only in the complete Session Summary Block
(transcript lines 995–1000), outside the spec block:
> *"The Architect Agent produces Genesis Layers 2–4 as a single `.larql` file — the Genesis
> Patch..."*

**Description:**
Three of the four spec blocks (Entity Type Taxonomy, Primary Query Patterns, Relation
Vocabulary) include an "Interface contract" section. The Project Genesis Scope spec block —
arguably the most consequential block because Genesis is the system's initialization event —
does not. The Genesis interface contract is present only in the free-form session summary
text, not embedded in the spec block. This means the Genesis Scope spec block is incomplete
on its own terms: a reader of that block alone has no interface contract to hand off.

**Confidence:** High

**Proposed fix:**
Add to the **Spec Output Checklist** in `SKILL.md`:

> - [ ] Project Genesis Scope spec block includes its own Interface contract section — not
>       just summary-level prose. The Genesis Patch `.larql` file, the mint event for
>       `project_v1.vindex`, and the bootstrapping authorization channel must be named
>       explicitly within the block.

---

### SKILL-FRICTION-7

```
Skill:    graph-data-architect
Session:  Session 1 — Ontological Schema
Type:     Tension Attribution
```

**Evidence:**
Pre-T5 in `skill-design-decisions.md` (pre-mapped structural tension):
> *"T5 | Schema stability vs. agent autonomy in patch generation | Graph Data Architect vs.
> Orchestration Comparativist"*

Tension map status for Pre-T5:
> *"⚠️ Partially resolved. The schema extension protocol [...] is not explicitly specced as a
> protocol in the integrated document. Agents are prevented from using undeclared relations,
> but the pathway for authorized schema extension [...] is not contractually defined for the
> normal pipeline."*

OQ6 in session summary:
> *"Mid-project vocabulary extension protocol — agent-proposed or orchestrator-only?"*

**Description:**
Pre-T5 is one of six structural tensions baked into the skill team design before Session 1.
The skill correctly surfaced the substance of this tension as OQ6 — recognizing that
mid-project vocabulary extension is an unresolved question. However, it treated this as an
open question to defer rather than as a named structural tension requiring an interface
contract stub for the Orchestration Comparativist.

The difference matters: an open question is deferred silently. A named tension requires an
explicit interface contract that the Orchestration Comparativist session must resolve. OQ6
as written gives the Orchestration Comparativist no contract to negotiate against — no
statement of the competing requirements (schema stability vs. agent autonomy). Pre-T5 is
still partially unresolved as of Session 7.

**Confidence:** Medium

**Proposed fix:**
Add to the **Operating Mode** section of `SKILL.md`:

> *"The six pre-mapped structural tensions (from `skill-design-decisions.md`) are always
> live during a schema spec session. When a topic touches one of these tensions — especially
> Pre-T5 (Schema stability vs. agent autonomy) or Pre-T6 (Genesis completeness vs. lock-in)
> — do not defer it as an open question. Name the tension explicitly, state both competing
> requirements, and produce a stub interface contract: `IC-PENDING: [Tension name] — requires
> resolution with [Specialist] in Session [N]`. This is not the same as resolving the tension;
> it is ensuring the tension arrives at the right session with the right contract language."*

---

### SKILL-FRICTION-8

```
Skill:    graph-data-architect
Session:  Session 1 — Ontological Schema
Type:     Tension Attribution
```

**Evidence:**
Pre-T2 in `skill-design-decisions.md` (pre-mapped structural tension):
> *"T2 | Write volume vs. edit locality guarantees | Graph Data Architect vs. MEMIT Specialist"*

Tension map status for Pre-T2 (resolved via T6):
> *"The MEMIT Specialist's locality protection is the Architect capacity ceiling (10,000 edge
> hard cap, 2,000 sub-batch recommendation) and the drift-from-anchor triggers."*

The Genesis Scope spec block "Hard constraints" section (transcript lines 984–988):
> *"Total Genesis write volume should be bounded — if you find yourself writing thousands of
> triples at Genesis, the scope has drifted."*

No specific volume ceiling is named. No interface contract with the MEMIT Specialist for
Genesis batch size is produced.

**Description:**
Pre-T2 is another pre-mapped structural tension. The skill correctly identified the principle
— Genesis should be bounded — but never asked the MEMIT Specialist what the ceiling actually
is. The write volume/locality tension would have been the natural thing to surface when
defining Genesis Layer 4 (Foundational Domain Knowledge), which could in principle contain
tens of thousands of triples from framework documentation ingestion. The phrase "bounded" is
not a constraint; it is a placeholder.

The tension was eventually resolved in Session 7 via T6 (10,000 edge hard cap, 2,000
sub-batch recommendation, drift-from-anchor triggers), but those numbers came from the MEMIT
Specialist's model analysis — not from a question the Graph Data Architect asked. Surfacing
the question in Session 1 would have given the MEMIT Specialist a concrete target to spec
against in Session 2.

**Confidence:** Medium

**Proposed fix:**
Add to **Useful Framing Questions** in `SKILL.md`:

> *"What is the upper bound on total edge volume for a Genesis write? The write engine will
> impose a locality ceiling on how many edges can be compiled in a single MEMIT batch. Before
> finalizing Genesis Layer 4 scope, this ceiling must be flagged as a requirement for the
> MEMIT Specialist to define. A Genesis Layer 4 that exceeds the ceiling would need to be
> staged — which changes the Genesis atomicity guarantee."*

Add a pre-mapped tension acknowledgment block to the **Project Genesis Scope** section of
the Spec Output Checklist:

> - [ ] Pre-T2 acknowledged: Genesis write volume ceiling is forwarded to MEMIT Specialist
>       as an explicit requirement. If the ceiling is unknown at this session, it must be
>       named as a blocking open question for Session 2.

---

### SKILL-FRICTION-9

```
Skill:    graph-data-architect
Session:  Session 1 — Ontological Schema
Type:     Spec Output Gap
```

**Evidence:**
Constraint C2 in session summary:
> *"All entity names must be compositionally unambiguous — polysemantic token list defined."*

Interface Contract IC2 in session summary:
> *"Validation layer: Receives declared vocabulary from graph Taxonomy Relations at project
> load — Rejects patches with undeclared types or relation labels — Class 3 epistemic query
> empty result must surface as named signal to orchestrator."*

IC2 covers constraints C4 (untyped entities) and C5 (undeclared relation labels) but does
not mention C2 (polysemantic naming constraint). The polysemantic risk register — the
enumerated forbidden token list — is not forwarded to the Validator in IC2.

**Description:**
C2 is one of the most important structural constraints the skill established — entity names
must be compositionally unambiguous, and a polysemantic risk register was defined (dangerous
tokens and their safe alternatives). But the Validator Agent cannot enforce C2 without access
to the polysemantic token list. IC2 forward-specifies what the Validator receives and enforces,
but omits C2 entirely. This means the C2 constraint is established in the spec but has no
enforcement mechanism named — a constraint without a guardian.

In practice, this means the Validator as specced would accept a patch containing `("model",
"depends_on", "schema")` even though both tokens are on the prohibited polysemantic list.

**Confidence:** Medium

**Proposed fix:**
Add to the **Interface contract with Validation layer** checklist item in `SKILL.md`:

> - [ ] Polysemantic token register is explicitly forwarded to the Validation layer as a
>       named artifact the Validator receives at project load. IC2 must state: "Rejects patches
>       containing entity or target names that appear on the polysemantic risk register without
>       disambiguation prefix." Without this, C2 is an unenforced constraint.

---

### SKILL-FRICTION-10

```
Skill:    graph-data-architect
Session:  Session 1 — Ontological Schema
Type:     Backlog Attribution
```

**Evidence:**
GAP-11 in `gap-backlog-v1.md`:
> *"Domain(s): State Consistency Theorist, MEMIT Specialist — OQ-SC2 — Layer 4 external doc
> unavailability. What happens when the authoritative external sources for Genesis Layer 4
> [...] are unavailable during initialization?"*

Genesis Layer 4 definition in transcript (lines 954–969):
```sql
INSERT INTO EDGES (entity, relation, target)
VALUES ("useActionState", "introduced_in",   "React_19"),
       ("FastAPI",        "documented_by",   "fastapi_official_docs");
```

No availability precondition or partial-Genesis fallback policy is mentioned anywhere in
the Genesis Scope spec block.

**Description:**
Genesis Layer 4 (Foundational Domain Knowledge) is defined as being sourced from external
documentation ingestion — framework docs, authoritative standards, reference materials. The
`documented_by` relation in the Namespace family points to external sources. The skill
never asked: *"What if those sources are unavailable at Genesis time? Is a partial Genesis
Layer 4 acceptable, or must Genesis be atomic — all four layers or none?"*

This is a Genesis completeness question the Graph Data Architect owns. GAP-11 surfaces it
as an open question discovered later, jointly attributed to State Consistency Theorist and
MEMIT Specialist — but it is rooted in a design gap the schema session should have named.
A partially-populated Layer 4 at Genesis creates an epistemic coverage inconsistency the
harness would not be designed to handle.

**Confidence:** Medium

**Proposed fix:**
Add to the **Project Genesis Scope** section of the Spec Output Checklist in `SKILL.md`:

> - [ ] Genesis Layer 4 availability precondition stated: is Layer 4 write atomic (all
>       external sources must be available, or Genesis fails), or is a partial Layer 4
>       acceptable with a defined fallback (e.g., agents run in degraded-coverage mode until
>       Layer 4 is completed)? This must be stated as an open question if not resolved, and
>       forwarded to the State Consistency Theorist session.

---

## Performance Summary

The `graph-data-architect` skill performed reliably in its core function: establishing a
coherent, well-structured ontological schema from a sparse and broad user brief. The session
produced ten clear architectural decisions, a relation vocabulary with enforced synonym
collision semantics, and a four-layer Genesis model that became stable enough to survive
the full seven-session arc without structural revision. The polysemantic risk analysis was
proactive and grounded in concrete examples. The Socratic inquiry phase was disciplined.

Its systematic weakness is **cross-domain forwarding failure**: the skill is excellent at
building out its own domain but consistently underspecifies the contracts it hands off to
adjacent specialists. Bidirectional traversal was established but not put in the MEMIT
interface contract. The polysemantic constraint was defined but not forwarded to the
Validator. The genesis volume ceiling was gestured at but not quantified or named as a
blocking question for the write engine. Schema versioning was never raised as a `.larql`
format contract question. The two pre-mapped tensions this skill co-owns (Pre-T2 and Pre-T5)
were not handled as tensions — Pre-T2 became a deferred open question without a volume
number, and Pre-T5 became OQ6 without a stub interface contract. The cumulative effect is
that several later sessions had to re-derive requirements the schema session should have
handed them explicitly. The proposed fixes above address this pattern by extending the
Spec Output Checklist with forwarding checkpoints for every adjacent skill interface, adding
the pre-mapped tension acknowledgment protocol, and fixing the format gap that caused
"Tradeoffs decided" to be systematically absent from all produced spec blocks.

---

*Friction analysis v1.0 — 10 entries catalogued*
*6 High confidence, 4 Medium confidence*
*Proposed fixes target: SKILL.md Phase 2 template, Spec Output Checklist, Framing Questions,
and Key Risks sections*

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

# LLM as Database: Agent Harness Architecture
## Skill Friction Log v1.0 — aiSecOps-specialist

> **Scope:** Post-session friction analysis for `aiSecOps-specialist` (The Warden)
> **Session analyzed:** Session 3 — Threat Modeling: Write Layer Access Control
> **Evidence sources:**
> - `transcript-session-3-security.md` (full session transcript)
> - `threat-modeling-write-layer-access-control.md` (session summary)
> - `gap-backlog-v1.md` (19 gaps extracted from the integrated spec)
> - `tension-map-v1.md` (12 tensions from Session 7 cross-domain synthesis)
> - `skill-design-decisions.md` (ownership boundaries and pre-mapped tensions)
> - `/mnt/skills/user/aisecops-specialist/SKILL.md` (skill definition)
>
> **Method:** Evidence-first. Friction entries are only raised where (a) a specific failure is
> directly traceable in the session transcript, or (b) a gap or tension document explicitly
> identifies Session 3 as the point of origin and the Warden's domain as the responsible
> owner. No friction is invented from general inference.
>
> **Total entries:** 12 (5 High confidence, 7 Medium confidence)
> **Entry format:** SKILL-FRICTION-[N] per `framework-spec-writer` SKILL.md conventions

---

## Friction Entries — High Confidence

---

### SKILL-FRICTION-1

```
Skill:      aiSecOps-specialist
Session:    Session 3 — Threat Modeling: Write Layer Access Control
Type:       Format Failure
Evidence:   SKILL.md §Operating Mode, Phase 1; session transcript structure (lines 22–56).
            The transcript shows the skill moved from the user's invocation directly to
            "Session 3 — AISecOps Specialist: The Warden / Scope: Write layer threat
            model…" with zero probing questions. Phase 1 of the skill definition is:
            "Before producing spec output, ask probing questions to map the trust surface."
            Six named questions are listed. None were asked.
Description: The Socratic Inquiry phase was entirely bypassed. The user's directive
             "Start with the threat model" was treated as an instruction to skip Phase 1
             entirely. The Phase 1 questions exist because they surface attack surface
             information that shapes every subsequent spec block — specifically, questions
             about how many agents have write authority, whether humans are in the loop,
             and where .vindex files live outside the harness. Without answers to these,
             the threat model must either assume or leave gaps. In Session 3, the skill
             assumed answers (the agent roster was inferred from prior session docs) rather
             than confirming them. This is architecturally acceptable in this case because
             Sessions 1 and 2 documents were uploaded and the context was rich. However,
             the Phase 1 bypass also meant no probing questions were surfaced as open
             questions in the session summary — which would have been the appropriate
             compensating behavior when inquiry is skipped by user direction.
Confidence: High — directly evidenced by transcript structure.
Proposed fix: Add a Phase 1 bypass protocol to SKILL.md: "If the user explicitly bypasses
              inquiry (e.g., 'start with the threat model'), do not silently skip Phase 1.
              Instead, (a) note in the session preamble that inquiry is being bypassed per
              user direction, (b) log each unanswered Phase 1 question as an OQ-S[N] item
              in the session summary's Open Questions section, and (c) mark each as
              'not yet confirmed — assumed from prior session documents' or equivalent.
              A skipped question is a deferred question, not a closed one."
```

---

### SKILL-FRICTION-2

```
Skill:      aiSecOps-specialist
Session:    Session 3 — Threat Modeling: Write Layer Access Control
Type:       Missed Question
Evidence:   D27 in session transcript (line 299): "expires after 30 minutes" — no analysis
            of whether 30 minutes is achievable for a Genesis compile of up to 10,000 edges
            internally sub-batched at 2,000. TENSION-T7 in tension-map-v1.md (lines 246–276)
            directly documents the revision: "a large Genesis patch running on GPU could
            easily exceed 30 minutes. A TTL expiry mid-compile produces an indeterminate
            state." T7 required Session 7 to change the model to admission-time TTL (10 min
            at admission, then compile proceeds independent of token state).
Description: The schema migration authorization token's 30-minute TTL was specced as
             a fixed expiration window without the Warden asking: "Is this window achievable
             given the maximum expected Genesis compile duration?" The MEMIT Specialist had
             already specced (by Session 2) a 10,000-edge hard cap with internal 2,000-edge
             sub-batching. The Warden had access to these figures via the uploaded Session 2
             document but did not interrogate whether a 10,000-edge MEMIT compile can
             complete in 30 minutes. This created a latent timing conflict that was only
             caught when the State Consistency Theorist examined the 2PC interaction in
             Session 5 and escalated it to the full council in Session 7 (T7). The Warden
             should have asked this question or flagged it as input required from the
             MEMIT Specialist before finalizing D27.
Confidence: High — D27 is directly in the transcript; T7 directly traces to D27 and
            documents the corrective action required.
Proposed fix: Add to SKILL.md §Useful Framing Questions: "Is the schema migration
              authorization token's TTL achievable given the maximum expected Genesis compile
              duration? What is the largest `.larql` patch the Architect Agent is expected to
              produce, and has the MEMIT Specialist confirmed a compile-time estimate for that
              patch size? A TTL that expires mid-compile creates an indeterminate 2PC state
              that the State Consistency Theorist must resolve." Also add to the Spec Output
              Checklist: "[ ] Schema migration token TTL cross-checked against MEMIT
              Specialist's compile-time estimate for maximum Architect Agent patch size."
```

---

### SKILL-FRICTION-3

```
Skill:      aiSecOps-specialist
Session:    Session 3 — Threat Modeling: Write Layer Access Control
Type:       Tension Attribution
Evidence:   TENSION-T11 in tension-map-v1.md (lines 384–420): "The Warden had specced a
            separate, cryptographically immutable audit trail (D28) as a security artifact.
            The State Consistency Theorist had separately specced a State Ledger…These were
            two append-only Merkle-chain integrity logs doing substantially overlapping work."
            Pre-T4 in skill-design-decisions.md (line 108): "Audit completeness vs. write
            throughput — Warden vs. State Consistency Theorist + MEMIT Specialist" is a
            pre-mapped structural tension baked into the skill team. Session 3's IC15 defines
            "Write Engine → Audit Log" but produces no interface contract between the Audit
            Log and the State Ledger.
Description: T11 was a foreseeable tension. Pre-T4 in the skill team's pre-mapped tension
             list identifies "Audit completeness vs. write throughput — Warden vs. State
             Consistency Theorist + MEMIT Specialist" as a structural conflict to be expected.
             The Warden specced the audit trail as a complete, standalone, append-only
             Merkle-chain artifact in Session 3 — which is exactly the description of the
             State Ledger that would be specced in Session 5. By not asking "How does this
             audit trail interact with the State Ledger the State Consistency Theorist will
             spec?" and not producing an interface contract between the two, the Warden left
             a structural overlap that required a Session 7 architectural merge. The SKILL.md
             Spec Output Checklist explicitly says "Interface contracts with MEMIT Specialist,
             Validation layer, and State Ledger defined" — the State Ledger contract was not
             produced. This is the most consequential tension the skill was positioned to
             pre-empt and did not.
Confidence: High — T11 body text explicitly names D28 as the source of the conflict;
            Pre-T4 is documented in skill-design-decisions.md as a pre-mapped tension the
            skill team was expected to hold.
Proposed fix: Add to SKILL.md §Operating Mode, Phase 2 under Spec Synthesis: "Before
              finalizing the audit trail spec block, produce a preliminary interface contract
              between the Audit Trail and the State Ledger, even if the State Consistency
              Theorist has not yet run. The preliminary contract should declare: (a) which
              events are audit-trail-owned vs. ledger-owned, (b) whether the audit trail and
              ledger are the same artifact or separate artifacts, and (c) what the storage
              delineation is. Mark this contract 'REQUIRES STATE CONSISTENCY INPUT in
              Session 5.' Producing a stub contract prevents a parallel-spec duplication
              in Session 5 from going undetected until Session 7."
```

---

### SKILL-FRICTION-4

```
Skill:      aiSecOps-specialist
Session:    Session 3 — Threat Modeling: Write Layer Access Control
Type:       Spec Output Gap
Evidence:   D28 in session transcript (line 451): "Audit trail is a mandatory, append-only
            security artifact. Canonical record format defined (12 required fields). Stored
            outside .vindex layer." The Audit Trail spec block (lines 326–370) defines 12
            fields and retention policy but specifies storage only as "outside the .vindex
            layer" and "separate from the State Ledger." No storage format (JSONL vs. DB),
            no file path, and no integrity mechanism for the audit trail itself is specified.
            TENSION-T11 traces the Session 7 merge requirement directly to this gap: the
            Unified Ledger resolution mandates "one append-only JSONL file at
            <harness_root>/.state-ledger/ledger.jsonl" with Merkle-chain-lite integrity —
            architecture that had to be invented in Session 7 because Session 3 left storage
            unspecified.
Description: The audit trail spec block defines what to record (12-field canonical format)
             and how long to retain it (project lifetime; indefinite for integrity violations)
             but does not specify where or in what format. "Stored outside the .vindex layer"
             is a security boundary description, not a storage spec. The absence of a
             format and path meant the State Consistency Theorist in Session 5 independently
             specced a Merkle-chain JSONL State Ledger with identical architectural
             properties, producing the T11 duplication. Had the Warden specced a concrete
             storage architecture (even as a placeholder: "append-only JSONL file at a
             harness-root path, with Merkle-chain-lite integrity, outside Git and outside
             .vindex"), the State Consistency Theorist would have had a surface to interface
             with rather than a second independent implementation.
Confidence: High — T11 directly traces the need for the Unified Ledger to the gap between
            D28's abstract "stored outside .vindex" and a concrete storage architecture.
Proposed fix: Add to SKILL.md §Audit Trail Requirements: "The audit trail spec block MUST
              specify: (a) storage format (append-only JSONL strongly recommended for
              portability and queryability; alternatives require explicit rationale), (b) file
              system location relative to harness root — outside both Git and .vindex,
              (c) integrity mechanism for the audit trail file itself (not just the records
              within it), and (d) whether this is a standalone file or shares infrastructure
              with the State Ledger. If storage architecture cannot be resolved in this
              session, produce an OQ-S[N] item explicitly requesting State Consistency
              Theorist input on storage design in Session 5."
```

---

### SKILL-FRICTION-5

```
Skill:      aiSecOps-specialist
Session:    Session 3 — Threat Modeling: Write Layer Access Control
Type:       Spec Output Gap
Evidence:   C17 in session transcript (line 76): "Write Scope Definitions are not modifiable
            by any agent at runtime. Scope changes require out-of-band human review event."
            Write Scope Definitions spec block (lines 213–268): "Scope definitions are
            security artifacts. They must be versioned, signed, and stored outside the
            harness's mutable layer." No storage path, file format, or governance mechanism
            is specified beyond "outside mutable layer." TENSION-T4 in tension-map-v1.md
            (lines 136–170) documents the resulting conflict: "Write Scope Definitions
            (Warden's domain) needed to be agent-runtime-immutable but operator-updatable"
            was one of four patterns from three sessions that each had "no unified governance
            model." T4's resolution required creating the three-tier .harness/ model
            (Tier 1 immutable anchor, Tier 2 sealed artifacts, Tier 3 anchored Git config)
            in Session 7.
Description: The Write Scope Definitions spec block correctly identifies that scope
             definitions are security artifacts and must be versioned, signed, and stored
             outside the mutable layer. However, it does not specify *where* they are stored
             or *how* the version-locking and signing are implemented. This left the storage
             question open for every session that followed. When the State Consistency
             Theorist (Session 5) specced Git-committed anchored artifacts, and the
             Orchestration Comparativist (Session 6) specced agent YAML as Git-committed
             operational config, there was no Warden-supplied storage contract to resolve
             against — leading to T4's fragmented governance pattern. Speccing "stored in
             a Warden-managed, operator-signed, versioned directory at .harness/
             write-scope-definitions/" in Session 3 would have given subsequent specialists
             a concrete target.
Confidence: High — T4 body text explicitly names Write Scope Definitions as one of the
            four fragmented storage patterns that required the Session 7 resolution.
Proposed fix: Add to SKILL.md §Write Scope Design: "Write Scope Definition storage must
              be specified to the level of: (a) physical location (named path relative to
              harness root, outside .vindex and outside agent process write permissions),
              (b) governance format (versioned directory, operator-signed manifest, or
              equivalent), (c) integrity mechanism (hash-sealed at version creation),
              and (d) update ceremony requirements (what constitutes a signed update event).
              'Stored outside the mutable layer' is a security boundary description, not
              a storage spec. A storage spec is required before this block is complete."
```

---

## Friction Entries — Medium Confidence

---

### SKILL-FRICTION-6

```
Skill:      aiSecOps-specialist
Session:    Session 3 — Threat Modeling: Write Layer Access Control
Type:       Missed Cross-Domain Implication
Evidence:   OQ-S2 in session summary (line 108): "Token revocation mechanism for
            compromised agent identity mid-session. → Needs operational spec before
            production deployment." No session routing, no cross-domain flag, no interface
            contract stub. TENSION-T5 in tension-map-v1.md (lines 174–208) documents the
            resulting Session 7 architecture: agent suspension model, governance-state
            binding (tokens carry hash-bindings to Write Scope Definition and Agent YAML),
            Orchestrator signing key dual-store. T5 is framed as "Warden vs. Orchestration
            Comparativist" — a conflict that required both specialists to resolve.
Description: OQ-S2 was recognized as open in Session 3 but routed as a generic operational
             deferral rather than as a cross-domain interface question requiring Orchestration
             Comparativist input. Token revocation mid-session is not purely operational: it
             requires the Orchestrator to maintain an in-memory suspended-agents set, which
             is an architectural decision. The Warden should have routed OQ-S2 explicitly to
             "INPUT REQUIRED: Session 6 (Orchestration)" and produced a preliminary interface
             contract stub: "Gate ← Orchestrator: revocation signal for suspended agent.
             Behavior: Gate rejects all tokens from suspended agent regardless of TTL state."
             Without this routing, T5 had to be surfaced from scratch in Session 7, requiring
             significant architecture (the suspension model, governance-state binding, and
             dual-store key anchor) to be worked out under cross-domain conflict rather than
             planned ahead.
Confidence: Medium — T5 directly traces to OQ-S2, but some of T5's resolution required
            Orchestration input that could not have been fully anticipated in Session 3.
Proposed fix: Add to SKILL.md §Key Risks: "Token revocation is not an operational concern
              alone — it has direct Orchestration implications. If an agent's token is
              revoked, the Orchestrator must define: (a) does suspension take effect
              immediately or at the next token presentation?, (b) what happens to an
              operation that is mid-2PC when suspension is declared?, and (c) how does
              the Gate receive the suspension signal? Any OQ regarding token revocation
              must be routed explicitly to Session 6 (Orchestration Comparativist) with
              an interface contract stub defining the revocation signal and Gate behavior."
```

---

### SKILL-FRICTION-7

```
Skill:      aiSecOps-specialist
Session:    Session 3 — Threat Modeling: Write Layer Access Control
Type:       Tension Attribution
Evidence:   TENSION-T4 in tension-map-v1.md (lines 136–170): the four fragmented storage
            patterns included "The Warden specced a permanently immutable Genesis seal
            (D49, dual-store), [and] the State Consistency Theorist specced path-
            classification as an anchored Git artifact (D76)." Upstream cause: neither
            the Warden in Session 3 nor the other specialists in Sessions 4–6 asked
            how their respective storage governance patterns would be unified. Pre-T5 in
            skill-design-decisions.md (line 109): "Schema stability vs. agent autonomy in
            patch generation" is listed as a pre-mapped structural tension, which has a
            configuration governance dimension that the Warden should have surfaced.
Description: T4 (Configuration Authority Fragmentation) was not foreseeable in full — it
             required Session 5 and 6 outputs to materialize. However, the Warden in Session
             3 specced the Genesis seal and Write Scope Definitions without asking: "How
             will these storage artifacts be governed alongside other harness configuration?"
             A Warden operating with cross-domain awareness would have recognized that
             immutable anchor artifacts, versioned operational config, and agent-runtime
             security artifacts are three different governance tiers and would have produced
             a preliminary note flagging this as an open cross-domain question — even without
             knowing Session 5's or Session 6's specific outputs. The Warden's pre-mapped
             role as "trust boundary owner across all components" implies awareness that
             configuration governance is a trust question, not just an operational one.
Confidence: Medium — T4 required multi-session input to fully materialize; the Warden
            could not have produced T4's resolution alone, but could have pre-surfaced
            the structural conflict.
Proposed fix: Add to SKILL.md §Operating Mode, Phase 2: "Before finalizing any spec block
              that establishes a new storage artifact (seal, scope definition, audit trail,
              configuration file), flag it with a cross-domain note: 'Storage governance
              for this artifact must be unified with all other harness configuration
              artifacts in a Session 5–6 synthesis. Preliminary storage pattern: [type].
              Routing: State Consistency Theorist (Session 5) and Orchestration
              Comparativist (Session 6) must confirm that this pattern is compatible with
              the broader harness configuration governance model.'"
```

---

### SKILL-FRICTION-8

```
Skill:      aiSecOps-specialist
Session:    Session 3 — Threat Modeling: Write Layer Access Control
Type:       Backlog Attribution
Evidence:   GAP-3 in gap-backlog-v1.md (lines 99–137): "The spec notes [the .larql format
            version mismatch concern] because the `.larql` format is the interface through
            which all agents author writes. A version mismatch between an agent's
            YAML-defined expectations and the current schema is not currently covered by
            the Gate's pre-checks (§10.2 lists seven pre-checks; schema version is not
            among them). Security note (Warden): If the Gate's pre-check list does not
            include a schema version check, an attacker who can replay a patch authored
            under an older schema version might bypass Validator checks added in the newer
            version." The security note in GAP-3 is attributed to the Warden but was
            produced by the council in Session 7, not by the Warden in Session 3. The
            Patch Authorization Gate spec block (lines 157–209) lists three checks
            (Identity, Scope, Integrity) with no mention of schema version verification.
Description: Schema version verification of .larql patches is a Gate concern with a
             direct security implication: a patch authored under a prior schema version
             could bypass Validator checks added to newer versions — a replay-variant attack.
             The Warden's SKILL.md Spec Output Checklist includes "Prompt injection vector
             analysis complete for write-authorized agents" and "Threat model completed for
             all five primary threats." Schema version replay falls within the spirit of
             Threat 2 (supply chain attack via tampered patch) and the prompt injection
             vector concern. GAP-3 is rated Critical (blocks 3+ other gaps) and required
             the council to add the Warden's security note in Session 7. This note should
             have been a Session 3 output, either as a Gate pre-check or as an OQ-S[N]
             item. The gap is attributable to the Warden because the Gate pre-check list
             is exclusively the Warden's spec domain.
Confidence: Medium — GAP-3's security note is attributed to "Warden" in the gap backlog
            but was produced in Session 7, not Session 3, confirming a Session 3 miss.
Proposed fix: Add to SKILL.md §Patch Authorization Gate (or the five primary threats
              section): "Threat 6 (Schema Version Replay): A patch authored under an older
              .larql schema version may bypass Validator checks added in newer versions if
              the Gate does not verify schema version compliance. The Gate pre-check list
              MUST include a schema version check OR an explicit OQ-S[N] must be produced
              noting that .larql schema versioning is required before the Gate pre-check
              list can be finalized." Add to the Spec Output Checklist: "[ ] Gate
              pre-check list addresses .larql schema version verification or explicitly
              defers it as a named open question."
```

---

### SKILL-FRICTION-9

```
Skill:      aiSecOps-specialist
Session:    Session 3 — Threat Modeling: Write Layer Access Control
Type:       Backlog Attribution
Evidence:   OQ-S4 in session summary (line 118): "Scope version management across long-
            running projects where agent capabilities evolve. → Operational concern;
            deferred to orchestration session." GAP-5 in gap-backlog-v1.md (lines 177–207),
            rated 🟠 High priority: "The Write Scope Definition update ceremony for
            long-running projects is only partially addressed (OQ-S4, §18.2). What is not
            defined is the behavior when a scope update occurs while there are active
            in-flight invocation tokens or open Write Locks." GAP-5 blocks: complete token
            lifecycle spec and long-running project governance spec.
Description: OQ-S4 was classified as an "operational concern" and deferred to the
             Orchestration session. GAP-5 shows this classification was incorrect: scope
             version management during in-flight operations is a security-bearing question
             because a scope update mid-flight creates a window where the agent briefly
             operates under either more or less authority than intended (the old token carries
             the old scope hash; the Gate will reject it as an "infrastructure failure" and
             re-issue — but the agent's in-progress work was authorized under the old scope).
             This is not an operational edge case; it is a trust boundary condition the
             Warden must characterize. Routing it to "orchestration" without flagging its
             security implications meant the Orchestration session addressed it as a
             scheduling concern rather than a trust scope concern, leaving GAP-5 open.
Confidence: Medium — GAP-5 is directly traceable to OQ-S4's misclassification;
            inferred from gap backlog rather than directly evidenced in transcript text.
Proposed fix: Revise §Key Risks in SKILL.md: "Scope changes during live operations are
              a security event, not an operational configuration update. Add to the Key
              Risks list: 'Scope update during in-flight operation: if a Write Scope
              Definition is updated while an agent holds an active token within its TTL
              window, the Gate will reject the token. This creates a window where the
              agent has started work under a scope that is no longer active. The Warden
              must spec: (a) whether the Orchestrator must drain in-flight operations
              before accepting a scope update, (b) whether the agent's partially-completed
              work is rolled back or held pending re-authorization, and (c) what Ledger
              entry is produced for a scope-update token rejection.' Any OQ about scope
              version management must be routed to Orchestration AND flagged as requiring
              Warden input on the security boundary."
```

---

### SKILL-FRICTION-10

```
Skill:      aiSecOps-specialist
Session:    Session 3 — Threat Modeling: Write Layer Access Control
Type:       Missed Question
Evidence:   The five-threat model in the transcript (lines 100–150) covers: Unauthorized
            Write (Threat 1), Patch Injection (Threat 2), Prompt Injection via Knowledge
            Poisoning (Threat 3), Cascading Corruption (Threat 4), Rollback Evasion
            (Threat 5). No threat covers human or external-tool Git commits outside the
            harness pipeline. TENSION-T10 in tension-map-v1.md (lines 349–380): "Out-of-
            Band Git Commit Handling — State Consistency Theorist vs. Warden. The Warden
            could not allow auto-compilation of catch-up patches generated from
            unauthenticated state changes; every write to the parametric layer requires
            human-authorized, Validator-verified content." T10 is framed as a Warden
            concern that required the Warden's participation to resolve but was not
            surfaced until Session 7.
Description: The Warden's threat model covers agent-originating threats and supply-chain
             attacks on agent-generated patches. It does not cover a sixth attack class:
             an external actor (human with repo access, CI system, automated script) writing
             to the Git repository outside the harness pipeline. This creates an unauthenticated
             state change: the Git layer has facts the parametric layer does not, and the
             harness has no record of who authorized the change. T10 required the Warden
             to rule that "no auto-compilation of catch-up patches from unauthenticated state
             changes" — a position that is clearly within the Warden's domain and could have
             been established as Threat 6 in Session 3. Instead, the State Consistency
             Theorist detected the issue when speccing reconciliation and had to escalate it
             as a cross-domain conflict.
Confidence: Medium — T10 is documented as a Warden-relevant conflict in Session 7, but
            it emerged from State Consistency session work, not from a direct Session 3
            evidence trail.
Proposed fix: Add to SKILL.md §Threat Model: "Threat 6 — Out-of-Band State Injection
              (Git Write Outside Harness): A human operator, CI system, or external tool
              commits directly to the project's Git repository without using the harness
              pipeline. The commit changes code state without a corresponding .larql patch
              or Ledger entry. If the harness detects this and auto-generates a catch-up
              patch, it is executing an unauthorized parametric write (no agent token, no
              Gate check, no Validator review). Defense: Out-of-band Git commits MUST
              NOT trigger automatic parametric writes. Catch-up patches generated from
              out-of-band commits require explicit human review and the standard
              authorization pipeline before reaching the write engine. The Warden must
              produce an OQ-S[N] for this threat class if the State Consistency Theorist
              has not yet specced reconciliation behavior."
```

---

### SKILL-FRICTION-11

```
Skill:      aiSecOps-specialist
Session:    Session 3 — Threat Modeling: Write Layer Access Control
Type:       Missed Cross-Domain Implication
Evidence:   TENSION-T3 in tension-map-v1.md (lines 103–130): "Meta-* Audit Completeness
            vs. Corpus Integrity — Warden vs. Validation Contract Architect. The Warden
            needed complete audit visibility into Meta-Validator and Meta-TGA health
            monitoring behavior — specifically, the ability to audit individual test case
            outcomes, not just aggregate health scores." The Session 3 Audit Trail spec
            block (lines 326–370) defines 12 mandatory fields covering write events and
            gate rejections. It does not mention periodic health monitoring events
            (Meta-Validator runs, behavioral probes, Meta-TGA runs). The per-case audit
            requirement for Meta-* runs was a Warden requirement that first appeared in
            Session 7.
Description: The audit trail spec in Session 3 correctly addressed write events and
             gate rejections. It did not address whether health monitoring events —
             Meta-Validator runs, behavioral probes, Meta-TGA health score computations —
             are auditable events. This left a gap that only became visible in Session 7
             when the Warden needed per-case (not aggregate-only) audit records from
             Meta-* runs for forensic purposes. Had the Warden asked in Session 3 "What
             does the audit trail look like for periodic health monitoring runs?", this
             requirement would have been surfaced before the Validation Contract Architect
             specced the Meta-Validator mechanism in Session 4. Instead, T3 required a
             Session 7 negotiation to add per-case audit reporting as a requirement on
             top of an already-specced health monitoring system.
Confidence: Medium — T3 directly documents the Warden's per-case audit requirement;
            the absence from Session 3's audit spec is inferred from the audit trail
            block's 12-field format, which covers only write events.
Proposed fix: Add to SKILL.md §Audit Trail Requirements: "The audit trail specification
              MUST address not only write events and gate rejections, but also periodic
              health monitoring events. Specifically: any system component that runs
              periodic behavioral verification (Meta-Validator, behavioral probe, Meta-TGA,
              or equivalent) is a security-auditable event. The Warden must specify: (a)
              whether health monitoring run results are per-case records or aggregate-only,
              (b) whether a health monitoring run that produces only an aggregate score
              satisfies the Warden's forensic investigation requirements, and (c) where
              health monitoring audit records are stored. Aggregate-only health scores
              prevent forensic investigation of individual test case failures."
```

---

### SKILL-FRICTION-12

```
Skill:      aiSecOps-specialist
Session:    Session 3 — Threat Modeling: Write Layer Access Control
Type:       Spec Output Gap
Evidence:   Genesis Bootstrapping Security spec block (lines 277–323): Step 1 describes
            a human reviewer inspecting the Architect Agent's output patch. Step 2 describes
            the schema migration authorization token. Step 3 describes the post-Genesis
            snapshot seal. No step or sub-clause describes what happens if the human
            reviewer rejects the patch at Step 1. The error path (re-invoke Architect Agent?
            halt project initialization? log rejection as security event?) is entirely
            absent. No OQ-S[N] item covers it.
Description: The Genesis Security Protocol specced the happy path (human reviews → approves
             → token issued → compile proceeds → snapshot sealed) but contains no error
             path specification. If the human reviewer at Step 1 determines the patch is
             corrupted, includes injected facts, or is otherwise unacceptable, the protocol
             provides no guidance on: (a) what system state the harness is in at the point
             of rejection (Genesis not yet started — clean; or has something already been
             written?), (b) whether the Architect Agent is re-invoked and with what
             correction context, (c) whether the rejected patch hash is logged as a
             security event in the audit trail, and (d) how many rejection cycles are
             permitted before the Genesis process is abandoned and escalated. For the
             highest-risk operation in the entire harness (the Warden's own characterization),
             the error path omission is significant. This likely requires low effort to
             address but was not flagged as an open question.
Confidence: Medium — directly evidenced by the absence of error-path language in the
            spec block; impact inferred from the block's own statement that Genesis
            bootstrapping is "the most critical security moment in the entire harness
            lifecycle."
Proposed fix: Add to SKILL.md §Genesis Security Protocol template: "For every step in
              the Genesis Security Protocol, an error path MUST be specified alongside
              the happy path. Step 1 error path minimum requirements: (a) state of the
              system on rejection (was anything written? Is a cleanup required?), (b)
              re-invocation protocol for the Architect Agent (what correction context is
              provided?), (c) whether the rejected patch hash is logged as a security
              incident, (d) maximum number of rejection-and-retry cycles before escalation
              to human halt decision. If any of these cannot be resolved in the session,
              produce an OQ-S[N] item explicitly deferring the error path design."
```

---

## Proposed SKILL.md Changes — Summary

The following changes to `/mnt/skills/user/aisecops-specialist/SKILL.md` are proposed based on
the 12 friction entries above. Each change is scoped to the minimum modification that prevents
the specific documented friction without altering the skill's ownership scope, voice, or
pre-mapped tension responsibilities (per `skill-design-decisions.md` §Skill Modification Rules).

| Entry | Section to modify | Change type |
|-------|------------------|-------------|
| SF-1 | §Operating Mode, Phase 1 | Add Phase 1 bypass protocol with OQ logging requirement |
| SF-2 | §Useful Framing Questions + Spec Output Checklist | Add TTL feasibility question and MEMIT cross-check item |
| SF-3 | §Operating Mode, Phase 2 | Add stub interface contract requirement for audit trail ↔ State Ledger |
| SF-4 | §Audit Trail Requirements | Add storage format, file path, and integrity mechanism as required fields |
| SF-5 | §Write Scope Design | Add storage path and governance mechanism as required spec fields |
| SF-6 | §Key Risks | Add token revocation as Orchestration-routing cross-domain risk |
| SF-7 | §Operating Mode, Phase 2 | Add storage governance cross-domain note for all new storage artifacts |
| SF-8 | §Patch Authorization Gate (new threat) + Spec Output Checklist | Add Threat 6 (schema version replay) and Gate pre-check item |
| SF-9 | §Key Risks | Add scope update during in-flight operation as security-bearing concern |
| SF-10 | §Threat Model | Add Threat 6 (out-of-band Git write) as a named attack class |
| SF-11 | §Audit Trail Requirements | Add health monitoring event audit coverage as a required spec topic |
| SF-12 | §Genesis Security Protocol template | Add error path specification as mandatory alongside happy path |

**Before implementing:** per `skill-design-decisions.md` §Skill Modification Rules, all
changes must be documented in `skill-refinement-log-v1.md` with rationale before reinstalling.
Changes SF-3, SF-8, and SF-10 touch interface contract definitions and require a council
interface contract review after modification.

---

## Performance Pattern Summary

The `aiSecOps-specialist` skill performed strongly within its core domain. The threat model was
thorough, concrete, and well-grounded in the specific harness architecture. The Patch
Authorization Gate, Write Scope Definitions, Genesis Security Protocol, and Audit Trail spec
blocks were all substantially correct and required no architectural revision in Sessions 4–6.
The session's interface contracts (IC10–IC16) were consistently well-formed and consumed
without conflict by downstream sessions. The skill's systematic weakness is not what it
produces within its domain — it is what it fails to flag at the domain's edges. Specifically,
the skill consistently under-specifies the physical storage architecture of the security
artifacts it introduces (audit trail, Write Scope Definitions, Genesis seal) — producing
ownership claims ("stored outside mutable layer") without storage contracts, which left
Sessions 5–7 to discover fragmented governance patterns. Equally, the skill treats several
cross-domain questions (token revocation, scope version management, out-of-band Git writes)
as operational deferrals rather than routing them explicitly to the sessions that need to
answer them — a pattern that caused multiple tensions to surface in Session 7 rather than
being pre-empted during their originating sessions. The skill knows its boundaries but does
not reliably pass information across them.

---

*Skill Friction Log v1.0 — 12 entries across 6 friction types*
*5 High confidence (directly evidenced in transcript)*
*7 Medium confidence (inferred from gap backlog or tension map)*
*Proposed fixes: 12 SKILL.md changes identified, all within existing ownership scope*
*Modification prerequisites: `skill-refinement-log-v1.md` entry required before reinstall*
*Council IC review required for: SF-3, SF-8, SF-10*


# Skill Friction Log — validation-contract-architect
## Session 4: Validation Contract Architecture and Reflexion Loop Design

```
Artifact type:    Skill Friction Log
Skill analyzed:   validation-contract-architect
Session:          Session 4 — Validation Contract Architecture and Reflexion Loop Design
Analyst:          Post-session friction analysis (post-Session 7)
Source documents: transcript-session-4-validation.md
                  validation-architecture-reflexion-loop-design.md (Session 4 summary)
                  gap-backlog-v1.md
                  tension-map-v1.md
                  skill-design-decisions.md
                  validation-contract-architect/SKILL.md
Status:           Draft
```

---

## Analysis Scope

This log identifies every instance where the `validation-contract-architect` skill
underperformed during Session 4. Friction is inferred only from evidence in the
session transcript, the Session 4 summary block, the gap backlog, and the tension map.
No friction is invented.

**Total friction instances identified:** 9
**High confidence:** 4
**Medium confidence:** 5

---

## Friction Entries — Sorted by Confidence, then Type

---

### SKILL-FRICTION-1

```
Skill:      validation-contract-architect
Session:    4 — Validation Contract Architecture and Reflexion Loop Design
Type:       Spec Output Gap
Confidence: High
```

**Evidence:**
GAP-3 (Critical priority) states: "Validator L1 static analysis completeness (§9.3): is
version conformance part of L1?" — explicitly open and unresolved. The Session 4 `.larql`
Patch Validation spec block enumerates the schema conformance criteria for the Validator's
pre-sandbox check (transcript lines 698–702):

```
- All entity base_types declared in the five-type taxonomy
- All relation labels in the approved vocabulary
- No `violates` relation present
- TIER directive present
- attention_weight in [0.0, 1.0]
```

No schema version field check is among these criteria. GAP-3 further notes that the seven
Gate pre-checks (§10.2) also omit schema version, and that a replay of an older-schema
patch could bypass Validator checks added in a newer version — making this a correctness
gap with a security footprint. The Validation domain co-owns this gap alongside MEMIT
Specialist and Graph Data Architect.

**Description:**
The L1 static analysis / schema conformance spec block was produced without asking whether
`.larql` patches carry a schema version field, or what the Validator should do when the
declared version doesn't match the active spec. The Session 4 session summary does not
include a schema version OQ. The gap was not surfaced, deferred, or forwarded to any
subsequent session. GAP-3 emerged as a Critical-priority gap in the post-Session 7 audit.

**Proposed fix:**
Add a bullet to the skill's "Domain Knowledge: Validating the `.larql` Patch" section,
under criterion 2 (Schema conformance):

> - **Schema version conformance:** Does the patch declare a schema version header? If so,
>   does it match the currently active `.larql` format version? Version mismatches must be
>   treated as schema failures, not syntactic failures.

Add to the skill's "Spec Output Checklist":

> - [ ] Schema version conformance check — is it part of L1 static analysis, or the Gate's
>       pre-checks, or both? Flag as OQ if undecided.

---

### SKILL-FRICTION-2

```
Skill:      validation-contract-architect
Session:    4 — Validation Contract Architecture and Reflexion Loop Design
Type:       Missed Cross-Domain Implication
Confidence: High
```

**Evidence:**
IC24 as defined in the Session 4 summary:

```
IC24. Meta-Validator → Audit Trail:
      validator health record: {health_score, threshold_status,
      sample_cases_reviewed, validator_version, timestamp}
```

This is aggregate-only reporting. Session 7 Tension T3 (Warden vs. Validation Contract
Architect) resolved that "aggregate-only reporting is explicitly forbidden" and that
"per-case audit reporting is mandatory for Meta-* runs" — each test case result must be
individually logged to the Ledger. The T3 resolution required defining the entire Sealed
Corpus pattern (§13.3) and introducing three new interface contracts (IC-SL7, IC-SL8,
IC-SL9) that Session 4 produced no precursor for.

The skill's own SKILL.md checklist includes: "Interface contracts with MEMIT Specialist,
Warden, State Consistency Theorist, and Orchestration layer defined." IC24 was the only
Warden-facing contract from the Validator Integrity spec block, and it was insufficient
for the Warden's audit requirements.

**Description:**
The Validator Integrity spec block (Q7, D41) specced the Meta-Validator mechanism
correctly but produced an IC24 that only exposed an aggregate health record to the Audit
Trail. The skill did not ask what the Warden needed from Meta-Validator output — a probing
question the skill's domain requires. The Warden's need for per-case visibility was not
surfaced, not deferred, and not flagged as a cross-domain interface question. T3 emerged
only in Session 7 and required a substantial revision to the Meta-Validator output contract.

**Proposed fix:**
Add a framing question to the skill's "Phase 1: Socratic Inquiry" section:

> - What does the Warden (authorization/audit layer) need from Meta-Validator output?
>   An aggregate health score may satisfy operational monitoring but not forensic audit
>   requirements. Does the Warden require per-case test results to be individually logged
>   to the Ledger?

Add to the skill's "Key Risks to Surface" list:

> 7. **Aggregate Meta-Validator reporting is insufficient for audit completeness.** The
>    Warden's audit trail requirements may demand per-case test outcome records, not just
>    aggregate health scores. Surface this as a cross-domain interface question before
>    finalizing IC for Meta-Validator → Audit Trail.

---

### SKILL-FRICTION-3

```
Skill:      validation-contract-architect
Session:    4 — Validation Contract Architecture and Reflexion Loop Design
Type:       Tension Attribution
Confidence: High
```

**Evidence:**
`skill-design-decisions.md`, §The Six Pre-Mapped Tensions:

```
| T3 | Validator independence vs. test coverage at scale |
     Validation Contract Architect vs. Orchestration Comparativist |
```

This tension was baked into the council skill before Session 1 as a known structural
tension. OQ-V3 in the Session 4 summary:

```
OQ-V3  TGA outputs: do TGA-generated tests require their own
       validation pass, or is the constitutional suite sufficient
       as a correctness floor?
       → Deferred
```

OQ-V3 was deferred with no cross-domain flag, no forward-routing to Session 6
(Orchestration), and no tension ID assigned. Session 7 had to resolve this as T2,
producing a four-layer TGA validation cascade (structural check + stub probe + dual-TGA
for CORE tasks + Meta-TGA) — a substantially more complex design than the TGA spec in
Session 4 anticipated.

**Description:**
Pre-T3 is one of the six pre-mapped structural tensions explicitly encoded in the skill
design decisions. The Session 4 spec correctly established TGA sequencing and independence
(D33, C24) but deferred OQ-V3 as a plain "Deferred" without recognizing it as the
manifestation of the pre-mapped Validation vs. Orchestration tension. As a result:

1. The tension was not flagged in the Session 4 → Session 6 handoff.
2. Session 6 (Orchestration) did not spec TGA scale behavior.
3. Session 7 had to resolve it from scratch under time pressure, producing the four-layer
   cascade that should have been at least roughed out earlier.
4. No "INPUT REQUIRED: Session 6" tag was placed on OQ-V3 (contrast: OQ-V2 received
   "INPUT REQUIRED: Session 6" correctly).

**Proposed fix:**
Add a section to the skill's "Operating Mode: Phase 1 — Socratic Inquiry":

> **Pre-mapped structural tension to surface proactively in Session 4:**
> The Validation Contract Architect vs. Orchestration Comparativist tension over TGA
> independence vs. test coverage at scale (Pre-T3 in `skill-design-decisions.md`) is a
> known structural tension. Before finalizing TGA spec decisions, surface this explicitly:
>
> - Does sequencing alone guarantee TGA independence, or does the Orchestration layer
>   need to enforce it structurally?
> - Does the TGA produce sufficient coverage for CORE-importance edges, or do those
>   require a more expensive dual-invocation approach?
>
> Flag any deferred TGA-correctness questions as requiring Orchestration Comparativist
> input, not just as "Deferred."

---

### SKILL-FRICTION-4

```
Skill:      validation-contract-architect
Session:    4 — Validation Contract Architecture and Reflexion Loop Design
Type:       Missed Cross-Domain Implication
Confidence: High
```

**Evidence:**
Session 7 Tension T9 ("Compaction correctness vs. efficiency — MEMIT Specialist vs.
Validation Contract Architect") resolved that the full MEMIT re-run strategy is mandated
for compaction, producing sample verification protocol and a compaction verification
failure report format. GAP-15 documents the residual gap: "If compaction verification
fails, the spec says 'existing overlays retained' — but the failure report format (what
the Behavioral Probe returns to the Transaction Controller to justify abort) is
unspecced."

Session 4's "INPUT REQUIRED FOR SESSION 5" block mentions compaction questions from
Session 2 (OQ-W4, OQ-W10) but frames them as State Consistency Theorist inputs — no
validation requirements for compaction output are flagged:

```
— OQ-W4 (Session 2): overlay compaction spec — State Consistency Theorist owns this
— OQ-W10 (Session 2): overlay compaction — full MEMIT re-run vs. delta composition
```

The Validation Contract Architect's behavioral consistency cascade specced L2 inference
probes for individual writes (edges ≥ 0.85). Compaction is a bulk re-write of many edges
simultaneously — its verification is a distinct problem from per-edge inference probing,
and belongs partly in the validation domain.

**Description:**
When passing compaction questions to Session 5, the skill should have noted that
compaction verification has a validation component — what does "the compaction preserved
the intended knowledge" mean, and which layer checks it? This cross-domain implication
was not flagged. T9 emerged in Session 7 specifically because neither Session 4
(Validation) nor Session 5 (State Consistency) fully owned the compaction verification
question, and it fell through the gap.

**Proposed fix:**
Add to the skill's domain knowledge section:

> **Compaction and bulk re-writes:** The behavioral consistency cascade speccs per-patch
> verification. When the overlay is compacted (a bulk re-write of many edges via full
> MEMIT re-run), per-patch L2 inference probing does not apply. Flag as a cross-domain
> interface contract with the MEMIT Specialist and State Consistency Theorist: what
> verification method applies post-compaction, what the failure report format is if
> verification fails, and which component owns that verification.

Add to the "Spec Output Checklist":

> - [ ] Compaction verification boundary — is post-compaction edge verification within
>       this skill's domain? If yes, spec it. If no, flag the interface contract
>       requirement for MEMIT Specialist and State Consistency Theorist.

---

### SKILL-FRICTION-5

```
Skill:      validation-contract-architect
Session:    4 — Validation Contract Architecture and Reflexion Loop Design
Type:       Spec Output Gap
Confidence: Medium
```

**Evidence:**
OQ-V5 in the Session 4 summary:

```
OQ-V5  Held-out suite authorship and update cadence — who
       maintains it and how often is it extended?
       → Human operational policy decision
```

GAP-8 (High priority) in the gap backlog:

```
Description: The Meta-Validator fires every 50 commits. If the corpus authorship
policy is not established before the first 50 commits, the first Health Score is
meaningless. This gap should be resolved at deployment setup, not deferred
to operations.
```

**Description:**
OQ-V5 was classified as a "Human operational policy decision" — implying it could be
resolved at any time during deployment. GAP-8 corrects this framing: the corpus
authorship policy is a deployment-blocking concern that must exist before the first
Meta-Validator run. By framing it as operational policy rather than deployment-blocking,
the Session 4 spec created a gap that could cause the first 50-commit health score to be
meaningless if left unresolved — a silent failure mode exactly like the ones the session's
own reasoning warned against.

**Proposed fix:**
Change the skill's framing for Meta-Validator deferral questions. Add to "Exit Criteria
and Failure Escalation" domain knowledge:

> When speccing the Meta-Validator, the held-out corpus authorship policy is not an
> operational afterthought — it is a deployment prerequisite. If the corpus does not
> exist before the first scheduled Meta-Validator run, the first Health Score is
> meaningless and the entire integrity monitoring mechanism fails silently. Flag any
> deferral of corpus authorship policy as deployment-blocking, not as operational policy.

---

### SKILL-FRICTION-6

```
Skill:      validation-contract-architect
Session:    4 — Validation Contract Architecture and Reflexion Loop Design
Type:       Spec Output Gap
Confidence: Medium
```

**Evidence:**
OQ-V4 in the Session 4 summary:

```
OQ-V4  Cross-agent review (Level 3): how is structural agreement
       between two independent patches scored? Exact match vs.
       semantic similarity threshold?
       → Deferred
```

The L3 Cross-Agent Review spec in the transcript (lines 716–720):

```
Level 3 — Cross-Agent Review (conditional)
  Triggers when: any edge attention_weight ≥ 0.90, OR
  patch touches Genesis-adjacent tier (L3/L4 boundary)
  Second agent independently generates patch from same code.
  Patches compared for structural agreement on entity claims.
```

"Structural agreement on entity claims" is stated with no definition. The check is named,
the trigger conditions are defined, but the pass/fail criterion has no operational
content. An implementer receiving this spec cannot build L3 without resolving OQ-V4 first.

**Description:**
Level 3 of the behavioral consistency cascade was specced with a defined trigger but a
completely undefined pass criterion. "Patches compared for structural agreement" is not a
constraint — it describes the activity but not the outcome. As written, L3 is either
always-pass (because no failure condition is defined) or always-blocked (because the
implementer must re-open the OQ before any L3 check can run). Deferring OQ-V4 without
providing even a placeholder minimum definition — such as "exact entity name match is the
minimum bar; scoring protocol TBD" — left the spec in an unimplementable state for this
level.

**Proposed fix:**
Add to the skill's behavioral consistency cascade domain knowledge:

> When speccing Level 3 Cross-Agent Review, always provide at minimum: (a) the floor
> definition for "structural agreement" (e.g., exact entity name and relation label match
> on all claimed edges), and (b) the tie-breaking rule when the two patches partially
> agree. A complete scoring protocol can be deferred, but the minimum pass criterion
> must be specced to prevent L3 from being unimplementable. Flag the full scoring
> algorithm as an OQ, not the minimum criterion.

---

### SKILL-FRICTION-7

```
Skill:      validation-contract-architect
Session:    4 — Validation Contract Architecture and Reflexion Loop Design
Type:       Missed Cross-Domain Implication
Confidence: Medium
```

**Evidence:**
D37 Step 2 in the Session 4 summary:

```
(2) Peer Agent Review — second independent Coder Agent
    receives full retry history and attempts task fresh
```

Tension map T12 (unlocatable), with the following candidate from the tension map document:

```
- The peer agent review authorization model (how a second Coder Agent is invoked
  and tokenized during D37 Step 2 escalation — agent-to-agent trust is not
  explicitly resolved).
```

The Warden's authorization model (Session 3) specced that every agent that writes to
the system must hold a valid authorization token scoped to its declared write region.
A second Coder Agent spawned mid-pipeline during escalation is a new agent instantiation
— it requires its own scoped token. The Session 4 failure escalation spec did not flag
this as a Warden interface requirement.

**Description:**
The Failure Escalation spec (D37) added a Peer Agent Review step without asking: who
authorizes this second Coder Agent, what token does it receive, and does it receive the
same scope as the original agent or a narrower one? This is squarely within the Warden's
domain and should have been flagged as a cross-domain interface contract requirement —
specifically, a new authorization interface between the Orchestrator and a dynamically
spawned Peer Agent. The gap may be the unlocatable T12.

**Proposed fix:**
Add to the skill's Failure Escalation domain knowledge:

> **Peer Agent Review authorization:** When speccing the Peer Agent Review escalation
> step, always flag the authorization question as a Warden interface contract requirement:
> How is the Peer Agent authorized? Does it receive the same scope token as the original
> agent, a narrower one, or a fresh token issued by the Orchestrator for this specific
> escalation? This is not a validation question — it is an authorization question owned
> by the Warden. Surface it as "INPUT REQUIRED: Warden" and produce a draft IC for the
> Orchestrator → Peer Agent token handoff.

---

### SKILL-FRICTION-8

```
Skill:      validation-contract-architect
Session:    4 — Validation Contract Architecture and Reflexion Loop Design
Type:       Format Failure
Confidence: Medium
```

**Evidence:**
The project-standard spec block format (system prompt):

```
### [Component] — Spec Block
What it must do / represent / enforce / guarantee:
Hard constraints:
Tradeoffs decided:
Open questions (deferred):
Interface contract:
```

The Session 4 spec blocks use the skill-internal format:

```
### [Component] — Spec Block
**What it must prove:**
**What it explicitly does NOT prove:**
**Input contract:**
**Output contract:**
**Failure behavior:**
**Hard constraints:**
**Open questions:**
**Interface contract:**
```

The "Tradeoffs decided:" field is absent from all Session 4 spec blocks. The Q1–Q7
decision rationale — which is precisely the kind of content this field should capture
(e.g., "TGA preferred over Coder-self-testing because Actor-Critic independence collapses
otherwise; cost tradeoff is TGA validation overhead") — is present only in the prose
preceding the spec workbook, not inside the spec blocks themselves. The framework-spec-
writer skill explicitly requires inline decision traceability: "every non-trivial claim
in a spec block should be traceable to at least one D, C, T, or IC ID."

**Description:**
When the Framework Council integrated Session 4 outputs into the v1.0 integrated spec,
the tradeoffs established in Q1–Q7 were not retrievable from the spec blocks alone —
they had to be reconstructed from the session prose. This is the exact integration
friction the "Tradeoffs decided" field is designed to prevent. The skill uses a
validation-specific spec format that diverges from the project standard, and that
divergence costs the Council one additional reconciliation step per block.

**Proposed fix:**
Update the spec block template in the skill's "Phase 2: Spec Synthesis" operating mode
to align with the project-standard format, while preserving the validation-specific
"What it must prove / What it does NOT prove" distinction as a sub-field of "What it
must do / enforce / guarantee:":

```
### [Validation Component] — Spec Block

What it must prove / enforce / guarantee:
  — What it must prove: ...
  — What it explicitly does NOT prove: ...

Hard constraints:
  — ...

Tradeoffs decided:
  — [e.g., TGA preferred over self-testing (D32): Actor-Critic independence;
     cost tradeoff is TGA validation overhead per task]

Open questions (deferred):
  — OQ-V[N]: ...

Input contract:
  — ...

Output contract:
  — ...

Interface contract (IC[N]):
  — ...
```

---

### SKILL-FRICTION-9

```
Skill:      validation-contract-architect
Session:    4 — Validation Contract Architecture and Reflexion Loop Design
Type:       Spec Output Gap
Confidence: Medium
```

**Evidence:**
Session 4 interface contracts IC17–IC24 include:

```
IC17. TGA ← Orchestrator: task specification + schema vocabulary.
IC18. Sandbox → Verbal Feedback Generator: {exit_code, stdout, ...}
```

IC17 defines what the TGA receives. IC18 defines what the Sandbox outputs. There is no
numbered IC defining what the Sandbox receives as input — i.e., the contract for how
gate-cleared code, TGA-generated tests, constitutional tests, and the current project
state snapshot arrive at the Sandbox for execution. The Sandbox Spec block in the
transcript (lines 588–594) lists inputs in prose:

```
**Input contract:**
- `module.py` — Coder Agent's code output
- `test_module.py` — TGA-generated tests (never Coder-authored)
- `constitutional_tests/` — human-authored suite, mounted read-only
- `run_test.sh` — polyglot execution script
- Current project state snapshot (from Orchestrator, for integration tests)
```

This is described but not formalized as a numbered IC. Without a numbered IC, the
Sandbox's input contract is not traceable in the interface contract index and cannot be
referenced by adjacent components (notably the Orchestrator, which assembles this
payload, and IC22 which speccs a similar payload for the Commit Executor).

**Description:**
The skill produced an output IC (IC18) for the Sandbox but not an input IC. The Sandbox
input is nontrivial: it includes outputs from three separate components (Coder Agent code,
TGA tests, human constitutional suite) assembled by the Orchestrator. Without a numbered
IC, the Orchestrator (Session 6) lacked a formal contract to reference when speccing the
Sandbox dispatch step, and the integration spec had to reconstruct this from prose.

**Proposed fix:**
Add to the skill's "Spec Output Checklist":

> - [ ] Sandbox input IC numbered and defined (what the Orchestrator assembles and
>       dispatches to the Sandbox: code payload, TGA tests, constitutional suite,
>       project state snapshot).

In-session, produce an IC immediately following IC17 covering the Orchestrator → Sandbox
handoff, matching the pattern established by IC22 (Orchestrator → Commit Executor).

---

## Performance Pattern Summary

The `validation-contract-architect` skill performed its core mission well: it elicited
seven structurally sound design decisions (D32–D41) through disciplined Socratic
inquiry, produced a coherent Reflexion loop design grounded in the Shinn et al. paper,
correctly closed three open items from prior sessions (OQ-S1, OQ-S3, OQ-W7), and
defined eight interface contracts that became primary inputs to Sessions 5 and 6. The
Commit Executor pattern (D40) in particular was a high-quality, unprompted architectural
contribution that correctly isolated write authority from all reasoning agents.

The skill's systematic weakness is **boundary incompleteness at cross-domain interfaces**.
It specced the validation pipeline's internal logic thoroughly — retry tiers, cascade
levels, feedback format — but consistently left the edges of that pipeline under-defined:
the input interface to the Sandbox (IC missing), the output interface from the
Meta-Validator to the Warden (IC24 aggregate-only), the authorization of dynamically
spawned Peer Agents (D37 Step 2), and the validation requirements for compaction output
(not flagged to Session 5). A related pattern: the skill deferred two questions
(OQ-V3, OQ-V4) without characterizing them as the pre-mapped tension and blocking
dependency they represent. Pre-T3 (Validation vs. Orchestration on scale) was baked into
the council skill and should have been surfaced proactively; instead, it re-emerged in
Session 7 as T2 requiring significant additional spec work. The fix across all of these
is the same: add cross-domain interface contract requirements explicitly to the skill's
Phase 1 inquiry and Spec Output Checklist, so that the edges of the validation pipeline
are as rigorously specced as its interior.

---

*Skill Friction Log — validation-contract-architect, Session 4*
*9 friction instances catalogued: 4 High confidence, 5 Medium confidence*
*Proposed fixes: all contained in SKILL.md modification recommendations above*

# Skill Friction Report — `state-consistency-theorist`
## Session 5: Syncing Git and .vindex with Two-Phase Commit

> **Analysis scope:** Full session transcript (`transcript-session-5-consistency.md`),
> session summary (`syncing-git-vindex-two-phase-commit.md`),
> gap backlog (`gap-backlog-v1.md`), and tension map (`tension-map-v1.md`).
>
> **Total friction instances:** 10
> **High confidence:** 4
> **Medium confidence:** 6
>
> **Sorted:** Confidence descending, then by Type per prompt spec ordering
> (Missed Question → Spec Output Gap → Cross-Domain Miss → Format Failure
> → Backlog Attribution → Tension Attribution).

---

## SKILL-FRICTION-1

```
Skill:    state-consistency-theorist
Session:  Session 5 — Syncing Git and .vindex with Two-Phase Commit
Type:     Cross-Domain Miss
```

**Evidence:**
IC-TC4 in the Transaction Controller spec block reads: *"Transaction Controller → Audit
Trail: compensating transaction records (integrates with Session 3 D28)."* IC-SL6 reads:
*"State Ledger → Audit Trail: integrity-violation events on chain-break or Genesis Seal
mismatch."* Both are explicit cross-references to the Warden's Session 3 Audit Trail
artifact. Additionally, the SKILL.md itself states: *"The State Ledger is a security
artifact (owned jointly with the Warden)."* The tension map entry for T11 confirms the
resolution cost: *"These were two append-only Merkle-chain integrity logs doing
substantially overlapping work. Both needed tamper-evidence; both needed post-hoc
queryability. Maintaining two separate infrastructure components doubled complexity."*

**Description:**
The skill produced a complete, standalone State Ledger specification — its own JSONL
append-only log, its own Merkle-chain-lite integrity model, its own storage location —
without raising the question of whether this duplicated Session 3's Audit Trail (D28).
Both artifacts are structurally near-identical: append-only, JSONL format, Merkle-chain
integrity, stored outside Git and `.vindex`, security-critical. The skill cross-referenced
D28 twice (IC-TC4, IC-SL6) as a downstream consumer, not as a co-owner of overlapping
infrastructure. The result was Session 7 Tension T11, which required reconstructing both
artifacts into a Unified Ledger with an `audit_category` tagging model and a three-tier
writer hierarchy. Pre-T4 ("Audit completeness vs. write throughput — Warden vs. State
Consistency Theorist") was a pre-mapped structural tension baked into the council skill
from Session 0; the State Consistency Theorist should have surfaced it independently.

**Confidence:** High — directly evidenced in transcript (IC-TC4, IC-SL6 cross-references)
and confirmed by T11 tension map entry.

**Proposed fix:**
Add a dedicated probe to the Phase 1 Socratic Inquiry section: *"Before speccing the
State Ledger, verify whether the Warden has already specced an audit trail or integrity
log. If overlap exists, raise the question of unification before finalizing the Ledger
as a standalone artifact."* Add to the Key Risks section: *"Duplicate append-only logs
— if the Warden has already specced an audit trail with identical integrity requirements,
producing a separate State Ledger doubles infrastructure complexity and creates authority
ambiguity over which log is canonical on divergence. This is a pre-mapped structural
tension (Pre-T4) and must be surfaced in every session that touches the State Ledger."*
Add to the Spec Output Checklist: *"Has the State Ledger's overlap with any Warden-owned
audit artifact been explicitly confirmed as acceptable or resolved by unification?"*

---

## SKILL-FRICTION-2

```
Skill:    state-consistency-theorist
Session:  Session 5 — Syncing Git and .vindex with Two-Phase Commit
Type:     Spec Output Gap
```

**Evidence:**
T8 in the tension map (*"Write Lock Semantics Conflation: State Consistency Theorist vs.
Orchestration Comparativist"*): *"The original D59/D60 scope lock was conflating three
distinct concerns."* The Session 5 Concurrent Write Policy spec defined a single lock
type (scope lock) with a single 60-minute TTL (D59, D60, C-CW5). The Session 7 resolution
required splitting this into two constructs: a Write Lock (60-min, entity write exclusion)
and a Dependency Hold (72-hr renewable, protecting edges the agent is reading from Pruning
operations). T8 status is Resolved — meaning the spec required structural revision, not
just clarification.

**Description:**
The Concurrent Write Policy spec block modeled a single lock primitive. The probing
questions in Phase 1 of the Socratic Inquiry ask about concurrent writes and serialization
strategy, but not about whether agents need to protect entities they are *reading* during
a task without intending to write them. This distinction — write exclusion vs. read
dependency hold — is fundamental to distributed lock design and should be within the
skill's domain knowledge. Agents that hold a Dependency Hold on edges being read (their
dependency context) have a different release condition than agents holding Write Locks.
The Pruning Agent's interaction with the lock model is also underspecified as a result:
the Pruning Agent spec (C-PA5: no deletes within 24 hours) serves as a crude proxy for
the Dependency Hold concept that was missing. The Session 7 resolution added IC-PA7
(Pruning → Orchestrator: Hold-state query) as a new interface contract.

**Confidence:** High — directly evidenced by T8 tension map entry documenting the spec
revision required.

**Proposed fix:**
Add a probing question to Phase 1: *"Does an agent need to protect entities it is reading
but not writing? If yes, the lock model requires at minimum two distinct constructs: a
write exclusion lock and a read dependency hold, with different TTLs and release conditions.
Ask this before finalizing the Concurrent Write Policy."* Add to the domain knowledge
section: *"A common underspecification in distributed write policies is defining a single
lock type for both write exclusion and read dependency protection. These have structurally
different TTL semantics: write locks expire when the agent commits; dependency holds may
need to outlive the commit to protect in-flight inference from Pruning operations."*

---

## SKILL-FRICTION-3

```
Skill:    state-consistency-theorist
Session:  Session 5 — Syncing Git and .vindex with Two-Phase Commit
Type:     Format Failure
```

**Evidence:**
The Transaction Controller spec block in the transcript defines:
- IC-TC2: *"Transaction Controller ← State Ledger: read access to PREPARED entries for
  recovery-scan detection."* (transcript line 282)
- IC-TC3: *"Transaction Controller → State Ledger: COMPENSATED and FAILED entry writes."*
  (transcript line 283)

The session summary's INTERFACE CONTRACTS DEFINED section lists IC-TC1, IC-TC4, IC-TC5,
and IC-TC6 for the Transaction Controller — silently omitting IC-TC2 and IC-TC3. IC-SL2
and IC-SL5 in the summary capture the same relationships from the State Ledger's
perspective, but they are not semantically equivalent: IC-TC2 defines the TC's read
access right as a consumer of Ledger data (a pull relationship), while IC-SL5 frames it
as the Ledger pushing orphaned-PREPARED scan results to the TC (a push relationship).
These are different interface designs with different failure-mode implications.

**Description:**
Two interface contracts produced in the spec body do not appear in the session summary's
interface contract index. The session summary is the canonical handoff artifact — it is
what downstream sessions receive, not the full spec prose. A downstream session that reads
only the summary would not know that the Transaction Controller holds a direct read path
into the State Ledger (IC-TC2) and that this read path is distinct from the Ledger's
proactive scan-results push (IC-SL5). This distinction matters: if the TC pulls from the
Ledger on startup, it needs read permissions and a defined query interface; if the Ledger
pushes, it needs an event notification mechanism. The summary presents only the push model.

**Confidence:** High — directly evidenced by comparing transcript lines 282–284 against
session summary INTERFACE CONTRACTS section (lines 332–345 of the summary file).

**Proposed fix:**
Add an explicit reconciliation step to the session summary production procedure in the
SKILL.md: *"Before finalizing the session summary, cross-check every IC-[component][N]
series defined in the spec blocks against the summary's INTERFACE CONTRACTS section.
Confirm no ICs are missing. If a contract appears only in the body but not the summary,
add it — the summary is the authoritative handoff artifact. Pay particular attention to
read-direction contracts (← arrows), which are easier to omit than write-direction ones."*

---

## SKILL-FRICTION-4

```
Skill:    state-consistency-theorist
Session:  Session 5 — Syncing Git and .vindex with Two-Phase Commit
Type:     Format Failure
```

**Evidence:**
The SKILL.md Phase 2 template specifies six named fields: `What it must guarantee`,
`Valid states (enumerated)`, `Invalid states (failure modes)`, `Transaction boundary`,
`Recovery behavior`, and `Interface contract`. The Session 5 spec blocks universally used
the generic project format instead: `What it must guarantee/do`, `Hard constraints`,
`Tradeoffs decided`, `Open questions (deferred)`, `Interface contract`. The Consistency
Model spec block has no `Valid states` or `Invalid states` enumeration — only constraint
declarations (C-SC1 through C-SC6). The compensating transaction catalog in the TC block
partially serves as recovery behavior but is inline rather than a named field.

**Description:**
The skill's own template was not followed for the most consistency-critical blocks.
The `Valid states / Invalid states` enumeration is not a stylistic preference — it is the
formal mechanism for making consistency invariants machine-checkable. The domain knowledge
section models these as a four-state table (Consistent / Git-ahead / Weights-ahead /
Diverged). The Consistency Model spec block in Session 5 does not reproduce this table;
instead, it lists constraints about how to classify patches. During Session 7, the council
working on T11 had to re-derive state boundaries when reasoning about the unified Ledger's
sync/async write split during failure conditions — work that an explicit state enumeration
in Session 5 would have anticipated. The template switch also hides the `Transaction
boundary` as a named field, folding it into `Hard constraints` (C-TPC1 through C-TPC5)
without the explicit boundary-declaration semantics the template provides.

**Confidence:** High — directly evidenced by comparing SKILL.md template against
Session 5 spec block structure throughout the transcript.

**Proposed fix:**
Add an enforcement note to Phase 2: *"For Consistency Model and Transaction Controller
spec blocks specifically, the skill-native template (with Valid states / Invalid states /
Transaction boundary / Recovery behavior as named fields) is mandatory. The generic
project format may be used for Pruning Agent, Git Operations Classification, Concurrent
Write Policy, and Overlay Compaction blocks — these do not require state enumeration for
consistency reasoning. Switching to the generic format for the core consistency components
loses the invariant-checking structure that makes consistency spec auditable."*

---

## SKILL-FRICTION-5

```
Skill:    state-consistency-theorist
Session:  Session 5 — Syncing Git and .vindex with Two-Phase Commit
Type:     Cross-Domain Miss
```

**Evidence:**
T7 in the tension map (*"Schema Migration Token Timing: Warden vs. State Consistency
Theorist"*): *"The original D27 schema migration token had a 30-minute TTL measured from
issuance to completion of the entire Genesis compile. The State Consistency Theorist
observed that a large Genesis patch (up to 10,000 edges, internally sub-batched at 2,000)
running on GPU could easily exceed 30 minutes."* The Session 5 spec session received all
four prior session documents as context, including the Session 3 security model containing
D27. C-TPC2 ("Genesis compile is a single 2PC event across all tier files") is in the
Session 5 spec, but OQ-TPC1 (PREPARED-state timeout) treats the timing concern as a
pure hardware-latency question without surfacing the D27 token TTL interaction.

**Description:**
When speccing C-TPC2 (Genesis as a single atomic transaction), the skill did not ask
whether the 30-minute token TTL from Session 3 D27 could expire mid-compile. This is
a cross-domain timing incompatibility: the State Consistency Theorist owns the 2PC
boundary duration; the Warden owns the token authorization window. A Genesis compile
that exceeds the token TTL produces an indeterminate state — the `PREPARED` entry has
been written, but the token is no longer valid. The skill noted the compile latency
uncertainty as OQ-TPC1 ("needs empirical input from MEMIT compile latency") but did
not connect it to the existing authorization constraint, which is specifiable now. The
resolution in Session 7 required the Admission-time TTL model (token consumed at Phase 1
admission, not measured to completion), a structural change to D27.

**Confidence:** Medium — inferred from T7 tension map entry; no explicit reference in
transcript to D27's TTL creating a problem during 2PC spec.

**Proposed fix:**
Add a checklist item: *"For every spec block involving a time-bounded operation (2PC
window, PREPARED timeout, compile duration, Genesis transaction), cross-check whether any
existing token TTL or authorization window from Sessions 3 and 4 could expire during that
operation window. If a compile or transaction could outlast an authorization token, raise
as a cross-domain tension requiring Warden input before finalizing the boundary spec."*

---

## SKILL-FRICTION-6

```
Skill:    state-consistency-theorist
Session:  Session 5 — Syncing Git and .vindex with Two-Phase Commit
Type:     Cross-Domain Miss
```

**Evidence:**
T10 in the tension map (*"Out-of-Band Git Commit Handling: State Consistency Theorist vs.
Warden"*): *"The Warden could not allow auto-compilation of catch-up patches generated
from unauthenticated state changes; every write to the parametric layer requires
human-authorized, Validator-verified content. These two requirements were in direct
conflict."* Session 5 specced D52/C-GOC4 (catch-up patches flagged `requires_human_review;
no auto-compile`) as a consistency reconciliation solution. The SKILL.md states: *"You
do not own the trust boundary (Warden)."* The Warden's concern was not flagged as
requiring cross-domain review in Session 5.

**Description:**
The Git Operations Classification and Pruning Agent spec blocks specced the out-of-band
commit reconciliation mechanism — detecting, generating catch-up patches, and applying a
human review flag — as a consistency problem. The security dimension (a catch-up patch
generated from an unverified commit crosses a trust boundary) was not surfaced as needing
Warden co-review. The human review flag (`requires_human_review`) was treated as
sufficient without asking whether the Warden's authorization model permits the *generation*
of a catch-up patch from unverified state, regardless of whether it auto-executes. T10
required explicit Session 7 resolution distinguishing the Consistency requirement
(detect and flag) from the Warden's requirement (never auto-compile from unauthenticated
state), and produced a distinct two-queue model with differentiated neglect defaults —
a more sophisticated architecture than the Session 5 single-flag approach.

**Confidence:** Medium — inferred from T10 tension map entry; no explicit reference in
Session 5 transcript to Warden objection to patch generation.

**Proposed fix:**
Add to the Key Risks section: *"Out-of-band Git operations that produce catch-up patches
are a cross-domain trust concern, not just a consistency reconciliation concern. The
Warden must confirm that the proposed reconciliation mechanism (flag for human review) is
a sufficient trust boundary, or specify additional authorization steps. Before finalizing
any out-of-band commit handling spec, raise it explicitly as a Warden-review item."*

---

## SKILL-FRICTION-7

```
Skill:    state-consistency-theorist
Session:  Session 5 — Syncing Git and .vindex with Two-Phase Commit
Type:     Cross-Domain Miss
```

**Evidence:**
T4 in the tension map (*"Configuration Authority Fragmentation: Warden vs. State
Consistency vs. Orchestration Comparativist"*) documents three incompatible config
governance patterns across sessions: the Warden's Genesis Seal (permanent immutable),
the State Consistency Theorist's path-classification list ("anchored Git artifact," D76
reference), and the Orchestration Comparativist's agent YAMLs (Git-committed operational
config). Session 5 deferred OQ-GOC1 (path classification list storage location) to the
orchestration session. The tension was surfaced only in Session 7.

**Description:**
The path-classification list controls which Git operations can bypass the 2PC path
(`parametric_none`). This makes it a trust-bearing configuration artifact — its values
determine whether a commit silently skips parametric memory update. When deferring
OQ-GOC1 to the orchestration session as a "storage placement question," the skill did
not flag that the Session 3 security model had already established integrity patterns
for exactly this class of artifact (operator-signed, versioned, integrity-checked). The
deferred question was not "where does this live" — it was "what governance model applies
to a config file that determines which writes skip the security pipeline." The Session 7
resolution required a Three-Tier `.harness/` model and produced IC-CFG1–IC-CFG3 as new
interface contracts covering all three incompatible storage patterns.

**Confidence:** Medium — inferred from T4 tension map entry and OQ-GOC1 deferral in
session summary.

**Proposed fix:**
Add a probing gate: *"For any configuration artifact whose values affect which operations
are permitted or required (e.g., path classification governing `parametric_none` bypass),
ask whether it requires integrity guarantees beyond operational config. If the artifact
controls which operations can bypass the 2PC path, it is trust-bearing and requires
Warden co-review of its governance model before the storage decision is deferred to the
orchestration session."*

---

## SKILL-FRICTION-8

```
Skill:    state-consistency-theorist
Session:  Session 5 — Syncing Git and .vindex with Two-Phase Commit
Type:     Backlog Attribution
```

**Evidence:**
GAP-6 in the gap backlog: *"OQ-TC1 — circuit breaker reset authority. Priority: High.
Domain: State Consistency."* Gap description: *"The TC is the safety floor of the whole
system. Both of these [GAP-6 and GAP-7] should be resolved before any implementation
planning begins."* Session 5 deferred OQ-TC1 as: *"Circuit-breaker reset protocol —
who can reset (human only? privileged orchestrator?)? Operational policy; defer."*

**Description:**
The circuit breaker reset authority was misclassified as operational policy. Operational
policy means "decidable at deployment time by the operator without spec impact." The
circuit breaker reset question is not operational — it requires an interface contract
(what component issues the reset signal, over what channel, with what authorization check)
and an architectural decision (does the Orchestrator hold reset authority, or must it be
human-only?). These are spec-level decisions that determine whether the Orchestrator has
a write path into the Transaction Controller, which affects the TC's interface contract,
the Orchestrator's capability requirements (Session 6), and the audit trail entries that
must be produced on reset. The gap backlog marks it High and notes it blocks "Ledger
entry catalog, TC spec completeness." The skill had the domain authority to resolve the
architectural component of this question in Session 5 and did not.

**Confidence:** Medium — inferred from GAP-6 high-priority classification and "operational
policy" deferral in the session summary.

**Proposed fix:**
Add a classification gate to the Spec Output Checklist: *"For every open question deferred
as 'operational policy,' confirm: does answering it require defining a new interface
contract, an authorization rule, or a component capability requirement? If yes, it is not
operational policy — it is an architectural gap. Defer only if the question requires a
deployment-time decision with no spec impact (e.g., specific timeout values, alert
notification channels)."*

---

## SKILL-FRICTION-9

```
Skill:    state-consistency-theorist
Session:  Session 5 — Syncing Git and .vindex with Two-Phase Commit
Type:     Backlog Attribution
```

**Evidence:**
GAP-7 in the gap backlog: *"OQ-TPC1 — PREPARED-state timeout. Priority: High. Blocks:
TC behavior for long compiles, Genesis 2PC gap."* Session 5 deferred OQ-TPC1 as:
*"PREPARED-state timeout before Transaction Controller treats the transaction as
abandoned. Needs empirical input from MEMIT compile latency on target hardware."* The
gap backlog notes: *"If a Genesis compile exceeds 2 hours, the Transaction Controller's
behavior is underspecced: does it auto-compensate, and in which direction? Does it trip
the circuit breaker?"*

**Description:**
OQ-TPC1 has two separable components: (a) the threshold value (empirical — requires
hardware data) and (b) the TC behavior when the threshold fires (policy — specifiable
now without hardware data). The skill deferred the entire question as empirical when only
the threshold value is blocked by hardware uncertainty. The TC's behavior on timeout is a
policy question: does it mark the entry FAILED and leave mediums unchanged? Does it
trigger auto-compensation? Does it trip the circuit breaker? Does it require human
escalation? Each answer has different downstream implications for the TC's interface
contracts and the Orchestrator's required capabilities. The Genesis 2PC gap (a Genesis
compile that times out produces an orphaned PREPARED entry that the TC spec does not
handle) is architecturally specifiable now. The gap backlog marks this High and notes it
blocks TC spec completeness.

**Confidence:** Medium — inferred from GAP-7 high-priority classification and bifurcated
nature of the question evidenced in gap description vs. session deferral rationale.

**Proposed fix:**
Add a bifurcation rule to Phase 2 operating mode: *"When an open question has both
empirical and policy components, defer the empirical part but spec the policy part
immediately. For timeout thresholds specifically: the threshold value is empirical and
may be deferred to hardware validation; but the TC behavior on timeout expiry (compensate
in which direction / trip circuit breaker / emit what Ledger entry type / alert
Orchestrator how) is a policy question that must be specced before the component is
finalized."*

---

## SKILL-FRICTION-10

```
Skill:    state-consistency-theorist
Session:  Session 5 — Syncing Git and .vindex with Two-Phase Commit
Type:     Spec Output Gap
```

**Evidence:**
GAP-12 in the gap backlog: *"OQ-SL1 — ledger retention policy. Priority: Medium. Domain:
State Consistency. The append-only JSONL Ledger... is explicitly designed for single-machine
deployment. Default is project-lifetime; epochs containing INTEGRITY_VIOLATION entries are
indefinite. What 'project-lifetime' means operationally is deferred."* Session 5 State
Ledger spec block produced C-SL1 (append-only, no deletion) and deferred OQ-SL1 as
*"Ledger compaction/archival policy — archived entries must remain verifiable → Operational
policy; defer."*

**Description:**
C-SL1 (append-only, no deletion) and the retention question are not separable at the
spec level. If entries can never be deleted but the ledger must eventually be archived,
the spec must define what "archivable" means without breaking the Merkle chain integrity —
this is a consistency constraint, not an operations preference. Minimum structural outputs
the skill should have produced: (1) a definition of verifiable archival (archived entries
remain in chain, cold storage access preserves hash verification); (2) an explicit
constraint that epochs containing `INTEGRITY_VIOLATION` or `IMMUTABLE_ANCHOR` entries
are never archivable without human review; (3) an interface contract for the archive
format (since the full-MEMIT rerun compaction in OC spec requires reading old patches from
archive). Instead, the spec produced only the append-only constraint and a deferral label.
The resulting gap (GAP-12) blocks long-running project operational planning and leaves
the compaction pipeline's archive-read interface undefined.

**Confidence:** Medium — inferred from GAP-12 medium-priority classification and the
logical dependency between C-SL1 (append-only constraint) and OQ-SL1 (retention
architecture) that the skill did not resolve.

**Proposed fix:**
Add to the State Ledger domain knowledge section: *"The append-only constraint and the
retention question are inseparable at the spec level. Any State Ledger spec block must
produce: (1) a structural definition of 'verifiable archival' — what it means to move old
entries to cold storage without breaking chain integrity; (2) explicit constraints on
which entry types can never be archived without elevated review (INTEGRITY_VIOLATION,
IMMUTABLE_ANCHOR, at minimum); (3) a note that the compaction pipeline's archive-read
path requires a defined interface contract. Deferring the entire retention question as
operational is incorrect because the retention architecture is bounded by the Merkle chain
guarantee — a spec-level decision."*

---

## Overall Performance Summary

The `state-consistency-theorist` performed at high output density in Session 5, producing
eight complete spec blocks, closing four inherited open questions (OQ-W4, OQ-W9, OQ-W10,
OQ-S6), and generating 26 decisions, 30+ constraints, and 30+ interface contracts. The
internal consistency of the spec work was strong: the 2PC boundary, Transaction Controller
compensating-transaction catalog, and State Ledger schema were detailed, well-structured,
and correctly integrated prior session outputs. Where the skill systematically
underperformed was at **domain boundaries**. It consistently produced specs that touched
the trust boundary (catch-up patch authorization, security incident detection,
trust-bearing config governance, audit-vs-ledger infrastructure overlap) without flagging
these as requiring Warden co-review — despite the SKILL.md explicitly stating "You do not
own the trust boundary." The two highest-cost friction instances (SKILL-FRICTION-1,
SKILL-FRICTION-2) both required structural spec revision in Session 7 that the skill
could have pre-empted: the Audit Trail / State Ledger unification (T11) and the single-lock
vs. two-lock model (T8). Both were within the skill's anticipation capability — the
SKILL.md notes that the State Ledger is "jointly owned with the Warden," and the domain
knowledge section models distributed lock design. The pattern is: **strong single-domain
synthesis, weak cross-domain interface hygiene**. The skill knows its domain deeply and
moves through it at high velocity, but does not pause at its own ownership boundaries to
ask which adjacent specialist needs to co-review the output.

---

*Skill Friction Report — `state-consistency-theorist` — Session 5*
*10 friction instances | 4 High confidence | 6 Medium confidence*
*Generated: Post-Session 7 debrief, Phase 0 Step 0.3*

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

# LLM as Database: Agent Harness Architecture
## Skill Friction Log — v1.0

> **Skill evaluated:** `framework-council`
> **Session evaluated:** Session 7 — Full Council Synthesis
> **Evaluation scope:** Six dimensions — Routing Quality, Voice Authenticity,
>   Tension Surfacing, Synthesis Quality, Phase Discipline, Spec Internal Consistency
> **Evidence sources:** `transcript-session-7-council.md`, `llm-as-database-v1_0-integrated-spec.md`,
>   `gap-backlog-v1.md`, `tension-map-v1.md`, six session summaries in project KB
> **Total friction entries:** 11
> **Entries by dimension:** Routing (2), Voice Authenticity (3), Tension Surfacing (2),
>   Synthesis Quality (2), Phase Discipline (1), Internal Consistency (1)

---

## Friction Entries

---

### SKILL-FRICTION-1

**Skill:** framework-council
**Session:** 7 — Full Council Synthesis
**Type:** Routing Failure

**Evidence:**
Session 7 T6 header (transcript line 1429): *"Primary voices: Warden and MEMIT Specialist,
with State Consistency on overlay-state implications."*

T6 speaker list across the full resolution (lines 1431–1563): 🛡️ Warden, 🔬 MEMIT Specialist,
⚖️ State Consistency Theorist. No 🗂️ Graph Data Architect voice appears anywhere in T6.

Tension map cross-reference for Pre-T6 (tension-map-v1.md): *"Addressed primarily by T6 —
drift-from-anchor + capacity model + scope test."* Pre-T6 specialist pairing per
`skill-design-decisions.md`: **Graph Data Architect vs. MEMIT Specialist** (Genesis
comprehensiveness vs. Genesis brittleness).

**Description:**
T6 addressed the pre-mapped tension Pre-T6, which belongs to the Graph Data Architect and
MEMIT Specialist. The council reframed this as a Warden-vs-MEMIT numeric reconciliation
problem (external-content cap vs. drift ceiling) and routed accordingly. That reframing was
useful — the numbers did need reconciling — but it eclipsed the Graph Data Architect's
stake in the same tension. The Graph Data Architect's concern is *what belongs in Genesis
and what does not*, which is the ontological question behind the capacity question. The
"minimal viable Genesis scope test" (transcript line 1445: "drift happens *relative to* a
stable foundation") was produced by the council narrator, not the Graph Data Architect.
The Graph Data Architect never spoke in T6, which means the spec's Genesis scoping rationale
is not grounded in the Graph Data Architect's voice.

**Confidence:** High — directly evidenced by absence of Graph Data Architect speaker tag
across T6's resolution body.

**Proposed fix:**
Add a Pre-Tension Routing Check to the council skill's Phase 3 (Tension Mapping) section.
Before routing any tension to specialist voices, the skill must check whether the tension
corresponds to a pre-mapped tension (T1–T6 per skill-design-decisions.md) and, if so, must
include the pre-mapped specialist pairing as the primary voice assignment regardless of how
the working-session tension was framed. If the session tension is a reframing of a pre-mapped
tension, the original pre-mapped specialists must still speak.

---

### SKILL-FRICTION-2

**Skill:** framework-council
**Session:** 7 — Full Council Synthesis
**Type:** Routing Failure

**Evidence:**
T2 resolution body (transcript lines 663–769). Speaker list:
✅ Validation Contract Architect, 🛡️ Warden, 🗂️ Graph Data Architect, 🔬 MEMIT Specialist.

Tension map T2 entry (tension-map-v1.md line 69):
*"TENSION-T2: TGA Independence vs. Correctness Depth —
Validation Contract Architect vs. Orchestration Comparativist."*

T2 header in session (transcript line 661):
*"Primary voices: Validation Contract, Warden, with MEMIT and State Consistency surfacing
secondary implications."* The Orchestration Comparativist is not named as a voice at all.

Pre-mapped tension Pre-T3 per `skill-design-decisions.md`:
**Validation Contract Architect vs. Orchestration Comparativist** — Validator independence
vs. test coverage at scale.

**Description:**
T2's resolution correctly engaged Validation Contract, Warden, Graph Data Architect, and
MEMIT Specialist. But the tension was catalogued — both in the pre-mapped list and in the
post-session tension map — as a Validation Contract vs. Orchestration Comparativist conflict.
The Orchestration Comparativist was the named representative of the scalability concern
(human-authored test suites create a bottleneck) that motivated the TGA four-layer cascade
design. Yet the Orchestration Comparativist never speaks in T2's resolution body. The scale
concern was resolved through Warden and Validation Contract dialogue alone. The result is
that T2's resolution has correct output but misattributed authorship — the tension map says
the Comparativist's concern was addressed, but the session record does not show the
Comparativist voicing or ratifying it.

**Confidence:** High — Orchestration Comparativist speaker tag absent from T2 resolution;
directly contradicts the tension map's specialist attribution.

**Proposed fix:**
When the council opens a tension for resolution, it must first verify which specialists are
named as primary voices in the tension map presentation. Any specialist named as primary
who has not spoken by the mid-resolution point should be explicitly invited: *"Before we
close this, let me hear from [Orchestration Comparativist] on the scale concern that
motivated this tension."* This prevents the pattern where a tension's attributed specialists
are a different set from its actual speakers.

---

### SKILL-FRICTION-3

**Skill:** framework-council
**Session:** 7 — Full Council Synthesis
**Type:** Voice Authenticity Failure

**Evidence:**
T4 resolution body (transcript lines 1013–1233). Graph Data Architect's sole contribution
(line 1040): *"I'll add a concern about agent YAMLs specifically. The YAML bundles system
prompt, temperature, and allowed tools. A modified YAML can change tool access — adding a
`web_fetch` tool to an agent that shouldn't have one, for instance. That's a scope escalation
without touching Write Scope Definitions."*

Pre-mapped tension Pre-T5 (`skill-design-decisions.md`):
**Graph Data Architect vs. Orchestration Comparativist** — Schema Stability vs. Agent
Autonomy. Resolution path listed in council SKILL.md: *"define a schema extension protocol
— agents can propose new relation types, but a review gate (human or Warden) must approve
additions."*

Tension map Pre-T5 entry (tension-map-v1.md lines 527–532):
*"The schema extension protocol — the mechanism by which agents could propose new relation
types for Warden/human approval — is described in the council skill as the resolution path
but is not explicitly specced as a protocol in the integrated document."*

**Description:**
The Graph Data Architect's defining instinct is: *"Can the schema actually say what the
system needs to say?"* In T4, the council had the opportunity to surface Pre-T5 as the
schema extension dimension of the configuration governance problem. The Graph Data Architect
should have raised: "While we're speccing what's immutable and what's Tier 3, I need a
protocol for authorized schema vocabulary extension. Agents will need to encode facts that
use relation labels not in the current schema, and the Gate currently enforces that
undeclared relations are rejected. We need a human-gated extension path." Instead, the
Graph Data Architect's T4 contribution was a security-domain concern about YAML tool access
— substantively correct, but not in the Graph Data Architect's primary domain. The schema
extension concern was never voiced. The voice authenticity failure is that the Graph Data
Architect behaved as a secondary security commentator rather than as the primary schema
domain voice.

**Confidence:** High — evidenced by (a) the single Graph Data Architect contribution being
a security concern not a schema concern, (b) the council skill's Pre-T5 resolution path
explicitly naming the extension protocol as the Graph Data Architect's deliverable, and (c)
the tension map's post-session finding that the extension protocol is absent from the spec.

**Proposed fix:**
Add a specialist instinct check to the council skill's specialist voice definitions. Before
each specialist speaks in a tension, the facilitator should internally verify whether the
specialist's *primary* instinct has been voiced, not just whether the specialist has said
something. For the Graph Data Architect, the check is: *"Has the schema expressivity concern
been raised? Has the vocabulary extension question been addressed?"* If not, the Graph Data
Architect must be directed to their primary instinct before secondary contributions are
allowed.

---

### SKILL-FRICTION-4

**Skill:** framework-council
**Session:** 7 — Full Council Synthesis
**Type:** Voice Authenticity Failure

**Evidence:**
T12 resolution body (transcript lines 2574–2590). All six specialists speak in sequence,
each delivering one sentence describing what trust assumption their domain makes. The
Orchestration Comparativist's contribution (line 2586): *"My Orchestrator-as-single-writer
model assumes there's one Orchestrator and it is who it claims to be."* The MEMIT
Specialist's contribution (line 2578): *"The base model is 'permanently frozen' (C8). This
is enforced how?"*

**Description:**
In T12, all six specialists are asked to confirm a trust assumption about their domain.
The resulting six-voice section is structurally neat but tonally convergent — every specialist
confirms "my component assumes X." This is narrated rather than voiced. The MEMIT Specialist's
response is authentically in-voice (it frames a question, which is characteristic). But most
other specialists state their trust assumption as a declarative fact, which produces a
chorus of confirmations rather than a cross-domain conversation. The Warden, in particular,
should have *challenged* other specialists' assumptions rather than summarized them — the
Warden's instinct is "what's the blast radius if this goes wrong, and can we detect it?" In
T12, the Warden summarizes the problem rather than pressing the other specialists on what
specific detection or prevention mechanism they assumed. The voices converge into a
documentation exercise rather than a final-tension exchange.

**Confidence:** Medium — the voices are present but their content is formulaic. The pattern
is inferred from comparing expected specialist instinct profiles against actual contributions.

**Proposed fix:**
In T12-type tensions (documentation of implicit assumptions), the council skill should
direct the Warden to interrogate other specialists' assumptions, not merely confirm its own.
Template: *"Warden, walk through each domain's stated assumption and identify which ones
the spec actually defends against and which ones are 'just trusted.' That produces the
Category 2 / Category 3 split."* This maintains the Warden's challenging instinct even in a
documentation tension.

---

### SKILL-FRICTION-5

**Skill:** framework-council
**Session:** 7 — Full Council Synthesis
**Type:** Voice Authenticity Failure

**Evidence:**
T2 resolution body (transcript lines 663–769). Tension map T2 attribution:
*"Validation Contract Architect vs. Orchestration Comparativist."*

Tension map summary table row (tension-map-v1.md line 555):
*"T2 — TGA independence vs. depth | Validation vs. Orchestration | ✅ Resolved."*

Actual resolution speakers: Validation Contract, Warden, Graph Data Architect, MEMIT
Specialist. The Orchestration Comparativist is absent.

**Description:**
This entry is related to SKILL-FRICTION-2 (routing) but addresses a distinct authenticity
problem: the Orchestration Comparativist's perspective was attributed to T2's resolution
without the Comparativist actually voicing it. The tension map says T2's scale concern
(Comparativist's side of Pre-T3) was resolved. But the resolution body shows the Validation
Contract and Warden reaching the four-layer cascade without the Comparativist's input. The
Comparativist's scale concern — *"human-authored test suites create a bottleneck at scale"*
— was preempted by the council rather than actually voiced and responded to by the Validation
Contract Architect. The result is a tension resolution whose attributed specialists do not
match the voices that actually produced it. This is not just a routing failure; it is the
council narrator speaking *for* a specialist voice rather than *through* it.

**Confidence:** High — directly evidenced by absent speaker tag in T2 resolution body.

**Proposed fix:**
Add to the council skill's facilitation principles: *"Do not speak for an absent specialist.
If a specialist's stake in a tension is named but the specialist has not spoken, pause the
resolution and explicitly invoke the specialist. A tension resolution is not valid if a
named primary specialist is absent from the dialogue."*

---

### SKILL-FRICTION-6

**Skill:** framework-council
**Session:** 7 — Full Council Synthesis
**Type:** Tension Surfacing Failure

**Evidence:**
Council SKILL.md Pre-T5: *"Schema Stability vs. Agent Autonomy — Resolution path: define a
schema extension protocol — agents can propose new relation types, but a review gate (human
or Warden) must approve additions."*

T4 resolution body (transcript lines 1013–1233): No mention of schema extension protocol.
The resolution scopes entirely to configuration artifact governance (Tier 1/2/3 model), not
to schema extension authority.

Tension map Pre-T5 entry (tension-map-v1.md lines 527–532):
*"⚠️ Partially resolved. The schema extension protocol...is described in the council skill
as the resolution path but is not explicitly specced as a protocol in the integrated document.
Agents are prevented from using undeclared relations, but the pathway for authorized schema
extension...is not contractually defined."*

**Description:**
Pre-T5 is one of six tensions baked into the council skill as a structural tension the
framework must resolve. T4 was the natural moment to surface it — the session was governing
configuration artifacts and Warden was speccing what Write Scope Definitions seal. The
council never named Pre-T5 explicitly during T4 and never introduced the schema extension
protocol question. The Graph Data Architect did not raise it (see SKILL-FRICTION-3). The
Orchestration Comparativist — the other named specialist in Pre-T5 — had no voice in T4 on
this question. The result is that Pre-T5 was only discovered as partially unresolved in
the tension map's post-session cross-reference section, not as a live issue during Session 7.
A pre-mapped tension that was never surfaced as a named discussion item during the synthesis
session is a surfacing failure even if later discovered post-hoc.

**Confidence:** High — pre-mapped tension not raised in session; post-session tension map
confirms it is partially unresolved; GAP-3 carries a sub-gap on this.

**Proposed fix:**
Add a Pre-Session Checklist to the council SKILL.md's Phase 3 (Tension Mapping). Before
presenting the council-derived tension map to the user, the facilitator must explicitly
verify each of the six pre-mapped tensions (T1–T6 in skill-design-decisions.md) appears in
the map — either as a named tension, as a sub-tension within a named tension, or with an
explicit disposition note explaining why it does not require a standalone entry in this
session. A pre-mapped tension may only be declared "addressed" if the specialist pairing
defined for that tension was given explicit voice during the addressing tension.

---

### SKILL-FRICTION-7

**Skill:** framework-council
**Session:** 7 — Full Council Synthesis
**Type:** Tension Surfacing Failure

**Evidence:**
Watchlist items in tension map presentation (transcript lines 420–428):

- W1: `GENESIS_LOCKED` consistency state not defined in S5 — *"needs a 2–3 line definition,
  not a major decision"*
- W2: Polysemantic noise vs. 0.85 inference probe threshold
- W3: Librarian Agent not specced — *"Accept as out-of-scope for v1, or note as v2?"*
- W4: L4 recovery when originating external doc unavailable
- W5: `must_not_contain` relation addition — *"small vocabulary decision"*

Council note at line 431: *"Twelve primary tensions plus five watchlist items... Most are
small clarifications or explicit scope documentations that never got written down."*

Subsequent transcript: None of W1–W5 is referenced again in T1–T12 resolution bodies or
in the synthesis close. No session summary block is present in the transcript.

**Description:**
The council named five watchlist items as *"smaller items worth naming"* with the implicit
promise that they would receive explicit disposition. Three of the five (W1, W3, W5) were
labeled as low-effort decisions the session could readily close. None received an explicit
close or documented deferral. The council proposed a working order (Cluster A → B → C → D)
and began at T1, but never returned to the watchlist. The watchlist was neither incorporated
into the work sequence (e.g., *"after T10, let's close W1 and W5"*) nor explicitly deferred
(*"these five items will be noted as post-synthesis editorial tasks"*). Items explicitly named
during the session must receive explicit disposition before synthesis. Presenting them and
then abandoning them is a stronger failure than not naming them at all, because the user
receives a false impression that the session addressed them.

**Confidence:** High — watchlist items are presented; no subsequent reference in the
transcript; no session summary block carries their disposition.

**Proposed fix:**
Add a Watchlist Closure Protocol to the council SKILL.md:
*"Any items placed on the watchlist during Phase 3 must receive explicit disposition before
the session enters Phase 4 (Synthesis). Acceptable dispositions: (a) closed inline at a
natural point during T1–T12 discussion, (b) explicitly added to the working sequence
('after T10, we address W1 and W5'), or (c) formally deferred with a notation in the session
summary block. A watchlist item may not be 'dropped' — it may only be closed or deferred.
The facilitator must run a watchlist check before beginning synthesis."*

---

### SKILL-FRICTION-8

**Skill:** framework-council
**Session:** 7 — Full Council Synthesis
**Type:** Synthesis Gap

**Evidence:**
Tension map T12 entry (tension-map-v1.md line 565):
*"T12 — Unlocatable | Unknown | ⚠️ Unlocatable | Not traceable in spec body |
Flag for council review."*

Tension map note on T12 (tension-map-v1.md lines 432–450): *"The integrated spec claims to
have resolved twelve tensions (per Appendix F)...The T12 tension resolved in the council
session (single-machine trust boundary documentation) produced clear outputs...but is
'unlocatable in spec body.'...Candidate tensions that might account for T12 include..."*

Session T12 resolution (transcript lines 2558–2731): Clear resolution; three-category Trust
Boundary Scope document accepted; Deployment Preconditions appendix accepted; outputs
explicitly named as additions to integrated spec.

Synthesis thinking block (transcript lines 2750–2783): No mention of T12 label; no mention
of verifying each tension's T-number was embedded in the corresponding spec section.

**Description:**
T12 was worked to a clear resolution in Session 7. The outputs — a Trust Boundary Scope
section and Deployment Preconditions appendix — are named in the resolution's implications
block. But the integrated spec's Appendix F claims twelve tensions, and the tension map
cannot trace T12 in the spec body. The synthesis phase did not include a step to verify
that each resolved tension carried its T-number as an inline reference in the spec body.
This makes one of the twelve tensions untraceable, which (a) undermines the traceability
guarantee of the integrated spec, (b) creates an apparent count discrepancy in Appendix F,
and (c) means future reviewers cannot determine which body section addresses the single-machine
trust boundary problem. The synthesis produced a correct *document* but an incomplete
*traceability graph*.

**Confidence:** High — tension map explicitly flags T12 as unlocatable; directly evidenced
by the post-synthesis analysis finding.

**Proposed fix:**
Add a Tension Traceability Check to the council SKILL.md's Phase 4 (Synthesis), as the
final pre-delivery step:
*"Before delivering the integrated spec, verify that each resolved tension T1–T[N] has
at least one inline `(T[N])` reference in the corresponding spec body section. For T[N]
whose output is a new standalone section (e.g., Trust Boundary Scope for T12), verify the
section header or its opening paragraph names the originating tension. Any tension whose
output is present but not labeled must be labeled before delivery."*

---

### SKILL-FRICTION-9

**Skill:** framework-council
**Session:** 7 — Full Council Synthesis
**Type:** Synthesis Gap

**Evidence:**
Council SKILL.md Pre-T5 resolution path: *"define a schema extension protocol — agents can
propose new relation types, but a review gate (human or Warden) must approve additions."*

Tension map Pre-T5 entry: *"⚠️ Partially resolved. The schema extension protocol...is not
explicitly specced as a protocol in the integrated document."*

Synthesis thinking block (transcript lines 2750–2783): No mention of checking pre-mapped
tensions against integrated spec content. The thinking block's planning covers document
structure and audience but contains no completeness verification against sessions 1–6 or
the six pre-mapped tensions.

Specific language: *"I'll skip the session summary details since those are just traceability
artifacts"* (line 2771) — this decision was made in the synthesis planning but is precisely
the step that would have caught Pre-T5's incomplete resolution.

**Description:**
The synthesis phase did not include a structured check of pre-mapped tensions against the
integrated spec's content. Pre-T5 (Schema Stability vs. Agent Autonomy) was pre-mapped as
a tension requiring a schema extension protocol — the means by which agents could *propose*
new relation types for authorized addition. The session's T4 discussion enforced the
enforcement side (agents are blocked from using undeclared relations) but produced no
protocol for the extension side. The synthesis produced a spec that correctly blocks
unauthorized extension but has no path for authorized extension. This is not a minor gap:
it means the framework has no designed mechanism for schema vocabulary to grow after
Genesis without a full Genesis migration token and Tier 1/2 ceremony. The synthesis missed
this because it built forward from "what did the session produce" rather than verifying
"what did the pre-mapped tensions require."

**Confidence:** High — tension map explicitly marks Pre-T5 as *"⚠️ Partially resolved"*
citing the missing protocol; council skill's resolution path confirms what was required.

**Proposed fix:**
Add a Pre-Mapped Tension Verification Pass to the council SKILL.md's Phase 4 (Synthesis).
Before beginning the integrated spec draft, the facilitator must check each of the six
pre-mapped tensions:
*"For each of T1–T6 in skill-design-decisions.md, confirm: (a) the tension was explicitly
worked during the session, and (b) the spec block corresponding to its resolution path
contains the mechanism the council skill specified as the resolution. If the mechanism is
absent, either add it or flag it as an open gap before synthesis proceeds."*

---

### SKILL-FRICTION-10

**Skill:** framework-council
**Session:** 7 — Full Council Synthesis
**Type:** Phase Discipline Failure

**Evidence:**
Transcript thinking block at line 1731: *"The user is moving forward to T8 without formally
answering the three decision questions for T7, which is a shift from their earlier 'All
recommendations approved' pattern. Given their consistent acceptance of every proposal so
far, I'm reading 'proceed to T8' as implicit approval of T7."*

Same pattern recurs at T9 ("proceed to T10"), T11 ("proceed to T12"), and each is noted in
the thinking blocks but absorbed silently into the record.

Session transcript close: No session summary block present. The session ended at the
integrated spec delivery (line 2824).

**Description:**
From T7 onward, the user's navigation commands ("Proceed to T8") replaced their earlier
explicit acceptance pattern ("All recommendations accepted"). The council correctly inferred
that these were acceptances, but silently absorbed the inference without any record. The
decisions behind T7, T9, and T11 were "accepted by navigation" — a practical reading of
the user's intent, but one that produces an ambiguous audit record. A session summary block
(required by project convention) would have flagged which decisions were explicitly accepted
vs. inferred. Without one, any future reader of the session record cannot distinguish
confirmed decisions from assumed ones. This is a phase discipline failure because the
project's "carry-forward convention" — which explicitly requires a session summary block —
was not produced. The session ended with spec delivery, not with a structured close.

**Confidence:** High — thinking blocks document the inference pattern; no session summary
block is present in the transcript.

**Proposed fix:**
Add to the council SKILL.md's Phase 4 closing protocol:
*"Before synthesis begins, produce a Session Summary Block. Format: decisions confirmed
explicitly / decisions accepted by navigation inference (list, with T-number) / watchlist
items disposed / interface contracts introduced. This block is the carry-forward input to
the next session and must be produced regardless of whether synthesis follows immediately.
Mark decisions accepted by inference with a '⚠️ inference' flag so the next session can
open with explicit ratification if needed."*

---

### SKILL-FRICTION-11

**Skill:** framework-council
**Session:** 7 — Full Council Synthesis
**Type:** Internal Inconsistency

**Evidence:**
Tension map header (tension-map-v1.md lines 6–9):
*"Tensions identified and worked: 12 (T1–T12 per Appendix F)...Tensions deferred /
unlocatable: 1."*

Tension map T12 entry (line 565): *"T12 — Unlocatable."*

Tension map note (lines 432–450): Candidate tensions for T12 are offered as speculation
(*"might account for T12 include..."*), suggesting the T12 label in the spec appendix
and the T12 tension worked in session are not clearly the same tension.

**Description:**
Appendix F of the integrated spec claims twelve tensions (T1–T12). The tension map — which
was produced from the integrated spec as its source document — cannot locate T12 in the spec
body. This creates an internal inconsistency: the spec's own appendix makes a traceability
claim that the spec's own analysis document cannot verify. The inconsistency has two possible
roots: (a) the synthesis numbered tensions in the appendix differently from how they were
labeled during the session (the session's T12 — single-machine trust boundary — produced
Part II of the spec, which may not be labeled as "T12" in the body), or (b) the synthesis
introduced a T12 label in Appendix F that was not produced during the session. Either way,
the spec counts a tension it cannot point to. This is not a gap to be closed later — it
undermines the spec's claim to be a fully traceable synthesis document.

**Confidence:** High — tension map explicitly flags the inconsistency; the count and
traceability failure are its direct finding.

**Proposed fix:**
The proposed fix is identical to SKILL-FRICTION-8's proposed fix (Tension Traceability
Check in Phase 4). Adding that check would have prevented this inconsistency. The additional
specific rule: *"Appendix F must not claim a higher tension count than the number of tensions
that have traceable inline T-references in the spec body. If the count exceeds the traceable
set, reduce the count and note the gap — do not inflate the count."*

---

## Council Performance Summary

**What the council did well in Session 7.** The council's opening tension map was the
session's standout achievement. Surfacing twelve live tensions from six session summaries —
including genuinely novel emergent tensions (T4 configuration fragmentation, T8 lock/hold
conflation, T10 pruning-to-queue routing gap, T11 audit trail unification) that were not in
the pre-mapped set — required careful cross-read across hundreds of decisions, constraints,
and interface contracts. The council held exploration open appropriately, declined to
synthesize until all twelve tensions had been worked, and maintained substantive specialist
dialogue throughout the core cluster work (T1–T5, T8–T11). The Warden's voice was
consistently sharp and in-character — the T4 threat-model inventory, the T5 token witness
framing, and the T11 audit unification argument each showed clear domain instinct. The T12
trust boundary framing — a documentation tension rather than a design conflict — was handled
gracefully, and the collective enrollment of all six specialists in confirming their domain's
trust assumptions was structurally effective. The integrated spec is demonstrably more
complete and more internally consistent than the sum of six session summaries, which is the
primary test for a synthesis session.

**Systematic weakness.** The most persistent failure pattern across SKILL-FRICTION-6, -7,
-8, -9, -10, and -11 is a shared structural cause: the council has no closing protocol.
Phase 4 (Synthesis) is defined as "when the user is ready to produce output" and the skill
instructs the facilitator to synthesize the session — but the skill does not specify what to
check *before* synthesis begins. The result is that every piece of named-but-unresolved
material — the five watchlist items, the Pre-T5 extension protocol, the T12 traceability
gap, the implicit-acceptance record — was absorbed forward into the spec without disposition.
The council excels at generating and working tensions, but has no systematic mechanism to
verify that what it named, it resolved; what it opened, it closed or deferred; and what it
claimed to capture, it actually captured with a traceable label. This is the gap the three
priority fixes below address.

---

## Priority Fixes

Ranked by impact on future council session quality.

---

### Priority Fix 1 — Pre-Synthesis Completeness Checklist

**Source entries:** SKILL-FRICTION-6, SKILL-FRICTION-7, SKILL-FRICTION-8, SKILL-FRICTION-9,
SKILL-FRICTION-10

**Impact:** Addresses five of eleven friction entries. The highest-leverage single change to
the skill.

**Proposed change to council SKILL.md:**

Add a Phase 4 Pre-Synthesis Gate — a mandatory checklist the facilitator runs before
beginning any synthesis pass:

```
PRE-SYNTHESIS GATE — run before entering Phase 4

1. PRE-MAPPED TENSION CHECK
   For each of the six pre-mapped tensions (T1–T6 in skill-design-decisions.md):
   - Was it named as a live tension or sub-tension during this session?
   - Was the specialist pairing listed in the pre-mapped definition given explicit voice?
   - Is the mechanism specified in the council skill's resolution path present in the
     session's working decisions?
   If any item is No: flag as a gap before synthesis.

2. WATCHLIST CLOSURE CHECK
   For each item placed on the watchlist during Phase 3:
   - Was it closed inline during T1–T[N] work?
   - If not, has it been explicitly deferred with a reason?
   An item may not proceed to synthesis as silently abandoned.

3. DECISION RECORD CHECK
   For any tension where the user's acceptance was inferred (navigation command rather
   than explicit confirmation): mark those decisions as ⚠️ inference in the session
   summary block.

4. TENSION LABEL CHECK
   Verify that every tension worked (T1–T[N]) has an identified output section in the
   spec plan. If a tension's output is a new standalone section, name that section before
   beginning the draft, so the T-label can be embedded correctly.

5. SESSION SUMMARY BLOCK FIRST
   Produce the session summary block before the integrated spec, not after.
   The session summary block is the input to synthesis, not a post-synthesis appendix.
```

---

### Priority Fix 2 — Absent Primary Specialist Enforcement

**Source entries:** SKILL-FRICTION-2, SKILL-FRICTION-3, SKILL-FRICTION-5

**Impact:** Addresses the voice-attribution failures that produce correct outputs attributed
to incorrect specialists. Prevents the pattern where a tension's named specialist pairing
in the tension map diverges from the specialists who actually spoke in the resolution body.

**Proposed change to council SKILL.md:**

Add to Phase 2 (Domain Exploration) and Phase 3 (Tension Mapping):

```
TENSION SPEAKER VERIFICATION

Before closing any tension as resolved:
1. Check which specialists are named as primary voices in the tension's opening framing.
2. Verify that each named primary specialist has contributed at least one substantive line
   of dialogue in the resolution body — not a summary sentence, but an argument, a
   constraint, or a counter-position.
3. If a named primary specialist has not spoken by the midpoint of the resolution:
   explicitly invoke them: "Before we close T[N], let me hear from [Specialist] on
   [their side of the tension]."
4. Do not attribute a tension resolution to a specialist who did not speak in it.
   If the Orchestration Comparativist's concern is satisfied without the Comparativist
   speaking, note this explicitly: "The Comparativist's scale concern is addressed by the
   dual-TGA cost-stratification; the Comparativist had no countervailing position."
```

---

### Priority Fix 3 — Pre-Mapped Tension Routing Assignment

**Source entries:** SKILL-FRICTION-1, SKILL-FRICTION-6

**Impact:** Addresses the structural cause of pre-mapped tensions being resolved through
the wrong specialist pairing. When a working-session tension reframes a pre-mapped tension,
the original specialist pairing must still be present.

**Proposed change to council SKILL.md:**

Add to the "Known Cross-Domain Tensions" section, after the six pre-mapped tension
definitions:

```
PRE-MAPPED TENSION ROUTING RULE

When a working-session tension (derived from OQ cross-read) addresses the same design
space as a pre-mapped tension, the facilitator must:

1. Name the pre-mapped tension explicitly: "T6 in the working map is also addressing
   Pre-T6 (Genesis Completeness vs. Lock-in). I need the Graph Data Architect and MEMIT
   Specialist to speak to this before we close on the capacity framing."

2. Invite the pre-mapped specialist pairing as primary voices, even if the
   working-session framing assigned different primary specialists.

3. A pre-mapped tension is not "addressed" unless:
   (a) its named specialist pairing was explicitly voiced, AND
   (b) the mechanism specified in its "Resolution path" is either present in the
       session's decisions or explicitly deferred with an OQ ID.

This rule prevents reframing from silently absorbing a pre-mapped tension's required
output. The six pre-mapped tensions exist precisely because they require specific
specialist voices to resolve — rerouting them to different specialists loses the
domain expertise the pre-mapping encodes.
```

---

*Skill Friction Log v1.0 — 11 entries across 6 dimensions*
*Ready for integration into council SKILL.md revision cycle*
*Revision to council SKILL.md: reference skill-design-decisions.md per modification rules*
