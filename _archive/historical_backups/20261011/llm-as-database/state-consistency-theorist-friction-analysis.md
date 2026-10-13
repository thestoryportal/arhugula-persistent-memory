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
