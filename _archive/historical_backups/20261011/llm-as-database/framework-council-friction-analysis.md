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
