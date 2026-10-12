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
