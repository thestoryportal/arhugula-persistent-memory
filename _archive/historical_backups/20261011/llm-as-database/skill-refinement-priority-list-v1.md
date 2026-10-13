# Skill Refinement Priority List — v1.0
## LLM as Database: Agent Harness Architecture

```
Artifact type:   Skill Refinement Priority List
Basis:           skill-friction-log-v1.md (full log, all six specialist sessions + Session 7 council)
Status:          Draft
Version:         1.0
Scope:           All seven skills — graph-data-architect, memit-specialist, aisecops-specialist,
                 validation-contract-architect, state-consistency-theorist,
                 orchestration-comparativist, framework-council
Modification rule: Before acting on any recommendation below, review skill-design-decisions.md.
                   No skill boundary may be redrawn without documenting the rationale there first.
```

---

## How to Read This Document

Each skill entry reports:
- **Friction count** — total entries and confidence breakdown (High = directly evidenced in transcript;
  Medium = inferred from gap backlog or tension map).
- **Pattern** — the recurring failure mode that produced the majority of friction in that skill's session.
- **Refinement priority** — High / Medium / Low, reflecting expected payoff per unit of SKILL.md effort.
- **Top recommended fixes** — the one to three highest-leverage changes from the friction log's
  proposed fixes section.

Entries are ordered by refinement priority (High first), then by friction count within tier.

Modification prerequisites apply to all entries: consult `skill-design-decisions.md` before making any
change to a SKILL.md, and log the change in the skill refinement log before reinstall.

---

## Skill Refinement Priority List

---

### 1. `framework-council`

**Friction count:** 11 entries
**Confidence breakdown:** Not separately categorised in log header; inferred from entry types:
Routing (2), Voice Authenticity (3), Tension Surfacing (2), Synthesis Quality (2),
Phase Discipline (1), Internal Consistency (1).

**Pattern: Absent closing protocol.**
The council has no pre-synthesis gate. The skill defines Phase 4 as "produce synthesis output
when the user is ready" but specifies no checklist to run before synthesis begins. The result is
systematic: named-but-unresolved watchlist items proceed to the integrated spec as silently
abandoned; tensions are resolved without the specialist pairings mandated by `skill-design-decisions.md`;
the session summary block is produced *after* the integrated spec rather than as its input; and the
spec's tension count can exceed its own traceable inline references. Five of eleven friction entries
(SKILL-FRICTION-6, -7, -8, -9, -10) share this single root cause. A second recurring failure is
pre-mapped tension mis-routing: when a working-session tension reframes a pre-mapped tension
(Pre-T1–T6), the council reassigns primary specialist voices rather than preserving the original
pairing, producing correct resolution output with misattributed authorship (SKILL-FRICTION-1, -2).

Because the council is the synthesis layer that amplifies every upstream gap or closes it, its
failure mode has the highest multiplier of any skill. A working closing protocol would have
pre-empted or surfaced at least half the tensions that required full resolution in Session 7.

**Refinement priority: High**

**Top recommended fixes:**

1. **Pre-Synthesis Gate (addresses SKILL-FRICTION-6, -7, -8, -9, -10).**
   Add a mandatory Phase 4 checklist the facilitator runs before any synthesis pass:
   - Pre-mapped tension check: all six Pre-T pairings explicitly voiced.
   - Watchlist closure check: every watchlist item closed inline or explicitly deferred with a reason.
   - Decision record check: inferred acceptances flagged ⚠️ in the session summary block.
   - Tension label check: every T[N] has a named output section before the draft begins.
   - Session summary block produced *first*, as the input to synthesis, not as a post-synthesis appendix.

2. **Tension Speaker Verification (addresses SKILL-FRICTION-2, -3, -5).**
   Before closing any tension as resolved, verify each named primary specialist contributed at least
   one substantive line of dialogue in the resolution body. If a named primary did not speak by the
   midpoint of the resolution, explicitly invoke them. Do not attribute resolution to a specialist
   who did not speak in it.

3. **Pre-Mapped Tension Routing Rule (addresses SKILL-FRICTION-1, -6).**
   When a working-session tension addresses the same design space as a pre-mapped tension,
   name the pre-mapped tension explicitly and invite its designated specialist pairing as primary
   voices regardless of how the working-session framing was assigned. A pre-mapped tension is not
   "addressed" unless its named pairing was explicitly voiced and its specified resolution path
   is present or explicitly deferred with an OQ ID.

---

### 2. `graph-data-architect`

**Friction count:** 10 entries
**Confidence breakdown:** 6 High, 4 Medium.

**Pattern: Cross-domain forwarding failure.**
The skill produces internally coherent schema work but consistently fails to forward its
decisions to adjacent skills in usable form. Bidirectional traversal was established as a hard
requirement (D4) but not included in the interface contract to the MEMIT Specialist (IC1).
The polysemantic naming constraint (C2) was defined but not forwarded to the Validator in IC2.
Genesis write volume was described as "bounded" without asking the MEMIT Specialist what the
ceiling is. Schema versioning was never raised as a `.larql` format contract question despite
the format being the skill's primary interface output. Two pre-mapped structural tensions
(Pre-T2, Pre-T5) were deferred as plain open questions rather than named tensions with stub
interface contracts. The skill also has a systematic spec format failure: its internal Phase 2
template omits the "Tradeoffs decided" field required by the project's canonical block format,
so all four Session 1 spec blocks are missing this field.

As the first session in the arc, forwarding failures compound: every adjacent skill (MEMIT
Specialist, Validation Contract Architect, Orchestration Comparativist) inherited underspecified
contracts and had to reconstruct requirements independently. Three critical gaps (GAP-3 schema
versioning, GAP-11 Layer 4 provenance, Pre-T5 extension pathway) trace directly to this skill's
forwarding omissions.

**Refinement priority: High**

**Top recommended fixes:**

1. **Extend the Spec Output Checklist with forwarding checkpoints for every adjacent skill
   interface (addresses SKILL-FRICTION-1, -5, -9).**
   Add mandatory checklist items: bidirectional traversal forwarded to MEMIT interface contract;
   polysemantic risk register forwarded to Validation layer contract; schema version header field
   addressed or explicitly deferred as a blocking OQ before MEMIT session begins;
   Genesis write volume ceiling forwarded as a MEMIT Specialist requirement.

2. **Add "Tradeoffs decided" to the Phase 2 spec block template (addresses SKILL-FRICTION-2).**
   This field is mandatory in the project format. Capture tradeoffs during the Socratic Inquiry
   phase, do not leave them only in prose discussion. "Tradeoffs decided: None — this decision
   is unambiguous" is acceptable; omitting the field is not.

3. **Add a Pre-Mapped Tensions section to the Operating Mode (addresses SKILL-FRICTION-7, -8).**
   When a topic touches Pre-T2 (write volume vs. edit locality) or Pre-T5 (schema stability vs.
   agent autonomy), do not defer as a plain open question. Name the tension explicitly, state both
   competing requirements, and produce a stub interface contract: `IC-PENDING: [Tension name] —
   requires resolution with [Specialist] in Session [N]`.

---

### 3. `aisecops-specialist`

**Friction count:** 12 entries
**Confidence breakdown:** 5 High, 7 Medium.

**Pattern: Strong within domain, weak at passing information across boundaries.**
The skill's spec output within its domain was architecturally sound: the Patch Authorization Gate,
Write Scope Definitions, Genesis Security Protocol, and Audit Trail blocks required no structural
revision in Sessions 4–6, and all Session 3 interface contracts (IC10–IC16) were consumed without
conflict. The friction is concentrated at the domain's edges. The skill consistently produces
ownership claims without the storage contracts that downstream skills need: "stored outside mutable
layer" appears without naming a storage artifact, governance tier, or retention rule. Cross-domain
questions — token revocation lifecycle, scope version management, out-of-band Git write detection,
audit trail physical infrastructure — are classified as operational deferrals rather than being
explicitly routed to the sessions that need to answer them. This pattern caused T4 (configuration
authority fragmentation), T8 (audit trail vs. State Ledger unification), T11 (audit infrastructure
overlap), and multiple GAP entries to surface in Session 7 rather than being pre-empted at their
originating session. The security framing was correct; the forwarding was not.

**Refinement priority: High**

**Top recommended fixes:**

1. **Require physical storage contracts for all security artifacts introduced (addresses
   entries producing T11, T4, GAP-5, GAP-9).**
   Any spec block that introduces a security artifact (audit trail, Write Scope Definitions,
   genesis seal, config governance file) must name: the storage medium, the governance tier
   (using the tier model from `skill-design-decisions.md`), the retention rule, and the
   component with write authority. "Stored outside the mutable layer" is not a contract; it
   is a placement principle. The contract must specify *where* and *under what governance*.

2. **Add explicit cross-domain routing rules for three recurring boundary questions.**
   - Token revocation lifecycle → route to State Consistency Theorist as a 2PC-boundary question.
   - Scope version management → route to Orchestration Comparativist as a requirements question.
   - Out-of-band Git write detection → route to State Consistency Theorist for Ledger contract.
   Each of these must be forwarded with a concrete scenario, not just a flag that security
   implications exist (per SKILL-FRICTION-7 proposed fix for injection weight manipulation).

3. **Add Warden co-review flag to any spec block that touches the State Ledger or config
   governance (addresses SKILL-FRICTION-1, -2, T8, T11).**
   The State Ledger is jointly owned with the State Consistency Theorist. The skill's SKILL.md
   states this, but the operating mode does not require a co-review flag when Ledger-adjacent
   decisions are made. Add to the Spec Output Checklist: if a decision affects what gets recorded
   in the Ledger, how Ledger entries are structured, or where config governance artifacts live,
   it requires an explicit "STATE CONSISTENCY THEORIST REVIEW REQUIRED" flag in the session summary.

---

### 4. `validation-contract-architect`

**Friction count:** 9 entries
**Confidence breakdown:** 4 High, 5 Medium.

**Pattern: Deployment-blocking questions classified as operational deferrals, and
insufficient Warden-facing contracts.**
Two distinct failure modes appear in roughly equal measure. First, the skill consistently
misclassifies questions as operational policy when they are actually deployment-blocking spec
requirements. OQ-V5 (held-out corpus authorship) was deferred as "human operational policy"
when GAP-8 shows it must exist before the first Meta-Validator run. The compaction verification
boundary was passed to Session 5 as a State Consistency question when the Validation layer
co-owns post-compaction edge verification. Schema version conformance was not included in the
L1 static analysis pre-checks (GAP-3, Critical). Second, the Warden-facing interface contracts
produced by this skill are systematically insufficient: IC24 (Meta-Validator → Audit Trail)
exposed aggregate-only reporting when the Warden requires per-case test outcome records, triggering
T3 and the Sealed Corpus redesign in Session 7. The pre-mapped tension Pre-T3 (Validation vs.
Orchestration on TGA independence at scale) was deferred as a plain OQ-V3 with no cross-domain
flag and no routing to Session 6, causing T2 to require a four-layer cascade design in Session 7
that should have been roughed out earlier.

**Refinement priority: High**

**Top recommended fixes:**

1. **Add schema version conformance to the L1 static analysis spec block template
   (addresses SKILL-FRICTION-1, GAP-3).**
   The `.larql` Patch Validation criteria must include: does the patch declare a schema version
   header? Does it match the active spec version? Flag as OQ if schema versioning is undecided,
   but reserve the slot in the L1 checklist — its absence makes the Gate pre-check spec
   structurally incomplete.

2. **Add a Warden-facing contract review gate to Phase 1 inquiry
   (addresses SKILL-FRICTION-2, T3).**
   Before finalising any interface contract directed to the Audit Trail or Warden layer, ask:
   does the Warden require per-case test results to be individually logged, or is an aggregate
   health score sufficient? This question is mandatory before IC for Meta-Validator → Audit Trail
   is closed. Add to Key Risks: "Aggregate Meta-Validator reporting is insufficient for audit
   completeness."

3. **Add a deployment-blocking classification rule to Phase 1 inquiry
   (addresses SKILL-FRICTION-5, SKILL-FRICTION-3).**
   Before classifying any open question as "operational policy," ask: must this be resolved
   before the first operational run of the component it governs? If yes, it is not operational
   policy — it is a deployment-blocking requirement with a specified resolution deadline.
   Apply this rule specifically to corpus authorship policy, compaction verification ownership,
   and any other question whose deferral would render the first operational cycle incorrect.

---

### 5. `state-consistency-theorist`

**Friction count:** 10 entries
**Confidence breakdown:** 4 High, 6 Medium.

**Pattern: Strong single-domain synthesis, weak cross-domain interface hygiene.**
The skill produced the highest output density of any single session: eight spec blocks, 26
decisions, 30+ constraints, 30+ interface contracts. The 2PC boundary, Transaction Controller
compensating-transaction catalog, and State Ledger schema were detailed, internally consistent,
and correctly integrated prior session outputs. The friction is concentrated at domain
boundaries. The skill consistently produced specs that touched the trust boundary — catch-up
patch authorization, security incident detection, trust-bearing config governance, audit vs.
Ledger infrastructure overlap — without flagging these as requiring Warden co-review, despite
the SKILL.md explicitly stating "You do not own the trust boundary." The two highest-cost
instances (SKILL-FRICTION-1, T11: Audit Trail / State Ledger unification; SKILL-FRICTION-2,
T8: single-lock vs. two-lock model) required structural spec revision in Session 7 that the
skill could have pre-empted. A secondary failure mode is whole-question deferral when only
part of a question is empirically blocked: OQ-TPC1 (PREPARED-state timeout) was deferred
entirely as requiring hardware data when only the threshold value is empirical; the TC's
behavior policy on timeout expiry is specifiable now (GAP-7, High priority).

**Refinement priority: Medium-High**

**Top recommended fixes:**

1. **Add a trust-boundary check to the Spec Output Checklist (addresses SKILL-FRICTION-1,
   SKILL-FRICTION-2, T8, T11).**
   Any spec block or decision that names a storage artifact, access control policy, or write
   authorization rule must carry a "WARDEN CO-REVIEW FLAG" in the session summary. The flag does
   not stop the skill from speccing the component — it ensures the Warden receives the output
   before the spec is ratified. The State Ledger is jointly owned; any State Ledger spec must
   explicitly list what the Warden needs to confirm before the IC is closed.

2. **Add a bifurcation rule to Phase 2 operating mode (addresses SKILL-FRICTION-9, GAP-7).**
   When an open question has both empirical and policy components, defer the empirical part
   but spec the policy part immediately. For timeout thresholds specifically: the threshold value
   may be deferred to hardware validation; the TC behavior on timeout expiry (compensate in which
   direction / trip circuit breaker / emit what Ledger entry type / alert Orchestrator how) is a
   policy question that must be specced before the component is finalised.

3. **Add the State Ledger retention constraint as a required spec output (addresses
   SKILL-FRICTION-10, GAP-12).**
   The append-only constraint (C-SL1) and the retention architecture are inseparable at the spec
   level. Any State Ledger spec block must produce: a structural definition of verifiable archival;
   explicit constraints on which entry types (INTEGRITY_VIOLATION, IMMUTABLE_ANCHOR) can never be
   archived without elevated review; and a note that the compaction pipeline requires a defined
   archive-read interface contract. Deferring retention as operational is incorrect because
   retention architecture is bounded by the Merkle chain guarantee — a spec-level decision.

---

### 6. `orchestration-comparativist`

**Friction count:** 9 entries
**Confidence breakdown:** 4 High, 5 Medium.

**Pattern: Integration blindness at the synthesis boundary.**
The skill's primary deliverable — the requirements matrix, candidate evaluation, and three-path
decision blocks — was the most thorough artifact of the six sessions. All eight evaluation
dimensions were sourced to specific session IDs, and six of seven inherited open questions were
closed. The friction is concentrated in the skill's declared synthesis-layer responsibility.
The Orchestration Comparativist is supposed to be the integration layer that connects all five
peer domains — but three High-confidence friction items are failures of exactly this kind.
The HIL return mechanism (boundary between orchestration and human interaction design) was
left with payload defined but transport mechanism unspecced (GAP-4b). The schema extension
pathway (HS-7) was treated as an orchestration scheduling requirement without asking what
triggers it from the agent side (Pre-T5 partially unresolved). A new config file
(`.harness/path-classification.json`) was introduced without checking whether it conflicted
with Warden-owned config governance — triggering T4 config fragmentation in Session 7.
A secondary pattern: the skill compresses spec block quality as a session progresses, producing
complete five-field blocks early and truncated blocks late (SKILL-FRICTION-4).

**Refinement priority: Medium**

**Top recommended fixes:**

1. **Add a cross-domain synthesis pass before the evaluation grid (addresses
   SKILL-FRICTION-1, -2, -3).**
   Before producing the requirements matrix, explicitly check each inherited open question from
   Sessions 1–5 for cross-domain boundary implications. For any new persistent artifact introduced
   during evaluation: name its governance tier and authority, explicitly reconciling with existing
   patterns from Sessions 3 and 5. For any HIL trigger defined: confirm the interface contract
   specifies both the outbound payload AND the inbound mechanism for the human's decision return.

2. **Add a spec block format self-check at end of session (addresses SKILL-FRICTION-4).**
   Every OQ-resolution block produced in the session must contain all five canonical fields.
   "Tradeoffs decided: None — this decision is unambiguous" is acceptable; omitting the field
   is not. Apply this uniformly to blocks produced late in the session, not only early ones.

3. **Add Pre-Mapped Tensions section referencing Pre-T3 and Pre-T5 (addresses
   SKILL-FRICTION-2, -9, and session-4 cross-reference for Pre-T3).**
   Pre-T3 (Validation Contract Architect vs. Orchestration Comparativist — TGA independence vs.
   test coverage at scale) and Pre-T5 (Graph Data Architect vs. Orchestration Comparativist —
   schema stability vs. agent autonomy) are structural to this skill's domain. Both must be
   checked proactively before evaluation closes: if TGA-correctness questions are unresolved,
   flag them as requiring this skill's input; if schema extension workflow is unspecced, name
   it as an orchestration event requiring specification before the evaluation matrix is final.

---

### 7. `memit-specialist`

**Friction count:** 10 entries
**Confidence breakdown:** 3 High, 7 Medium.

**Pattern: Domain-local treatment of cross-domain decisions, and deferred-but-critical
format questions.**
The skill performed correctly on its explicitly prepared structural work: Phase 1 Socratic
inquiry, storage-pass / behavior-fail failure mode, spec block format, and downstream session
routing. The friction is concentrated in two related failure modes. First, decisions with
clear cross-domain reach were handled as MEMIT-internal: the `attention_weight` authority
question was deferred without probing despite the skill's own domain knowledge making it a
natural Phase 1 target (SKILL-FRICTION-1, most expensive single revision in the spec arc);
Pre-T2 and Pre-T6 were resolved as internal thresholding problems rather than flagged as
requiring Graph Data Architect input; delta composition was presented as a neutral A/B choice
when the MEMIT domain knowledge already forecloses it on correctness grounds. Second, the
`.larql` format was finalised without a schema versioning slot despite being the exclusive
agent-facing interface — a decision that produced GAP-3 (Critical) and blocked four other
gaps. The L1 Cache was introduced in a decision (D13) without receiving its own spec block,
leaving buffer capacity, flush triggers, and invalidation behavior unspecced.

**Refinement priority: Medium**

**Top recommended fixes:**

1. **Add injection weight authority to the Phase 1 Socratic Inquiry (addresses
   SKILL-FRICTION-1, most expensive single revision in arc).**
   Probe: "Should agents be allowed to declare the injection weight for an edge, or should
   injection strength be an engine-internal concern derived from metadata the agent can set?
   These are different architectures with different security and correctness implications."
   Add to Spec Output Checklist: injection weight authority confirmed, with authorship domain
   documented before the format spec is written.

2. **Add schema versioning to the Spec Output Checklist as a format-blocking requirement
   (addresses SKILL-FRICTION-3, -6, -10, GAP-3 Critical).**
   Any format declared as the exclusive agent-facing interface, committed to Git, and consumed
   by Gate, Validator, Write Engine, and compaction re-run requires a versioning strategy before
   finalisation. The checklist item must read: "`.larql` schema versioning addressed: schema
   version header field defined or explicitly deferred as OQ — with an explicit NOTE that this
   blocks Gate pre-check spec, Validator L1 static analysis, and compaction re-run specification."

3. **Add a Pre-Mapped Tensions section to the Operating Mode (addresses SKILL-FRICTION-4, -5).**
   Name Pre-T2 (Write Volume vs. Edit Locality — pending Graph Data Architect alignment) and
   Pre-T6 (Genesis Completeness vs. Lock-in — requires Graph Data Architect input) explicitly.
   Threshold decisions produced in isolation must be flagged as "pending Graph Data Architect
   alignment" in the session summary. Compaction strategy must foreclose delta composition as a
   constraint, not present it as a design choice: full MEMIT re-run is mandatory; delta
   composition is excluded on correctness grounds (D20).

---

## Summary Table

| Skill | Friction Count | High / Med | Pattern | Priority |
|---|---|---|---|---|
| `framework-council` | 11 | — | No closing protocol; pre-synthesis gate absent; voice attribution failures | **High** |
| `graph-data-architect` | 10 | 6 / 4 | Cross-domain forwarding failure; format field omissions | **High** |
| `aisecops-specialist` | 12 | 5 / 7 | Strong within domain; weak at passing info across boundaries; storage contracts missing | **High** |
| `validation-contract-architect` | 9 | 4 / 5 | Deployment-blocking questions classified as operational; insufficient Warden contracts | **High** |
| `state-consistency-theorist` | 10 | 4 / 6 | Strong single-domain synthesis; weak cross-domain interface hygiene; whole-question deferral | **Medium-High** |
| `orchestration-comparativist` | 9 | 4 / 5 | Integration blindness at synthesis boundary; spec quality compression late in session | **Medium** |
| `memit-specialist` | 10 | 3 / 7 | Cross-domain reach of domain-local decisions; format finalised without versioning slot | **Medium** |

**Total friction entries logged:** 71 across 7 skills.
**High confidence entries:** 30. **Medium confidence entries:** 41.

---

## Shared Deficiency Across All Skills

One failure pattern appears in five of seven skills and should be addressed at the project
level, not skill-by-skill:

**The "Tradeoffs decided" field is systematically absent from produced spec blocks.**

The project's canonical spec format requires five fields. Four skills (graph-data-architect,
orchestration-comparativist, and two others evidenced in the log) produced spec blocks missing
this field. The skills' internal Phase 2 templates do not include it. The fix is identical for
all of them: add the field to every skill's internal spec block template, with the note that
omission is not acceptable even for apparently unambiguous decisions.

Consider adding a project-level note to the framework iteration guide confirming this field is
mandatory and will be checked in any Phase 0 friction review.

---

*Skill Refinement Priority List v1.0*
*Compiled from: skill-friction-log-v1.md (all six specialist sessions + Session 7 council)*
*71 total friction entries across 7 skills | Evidence-grounded: no friction invented*
*Modification prerequisite for all skills: consult skill-design-decisions.md before reinstall*
