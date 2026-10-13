# LLM as Database: Agent Harness Architecture
## Gap Session Starter Prompts — All 8 Sessions

> **How to use:** Copy one session block at a time and paste it as the opening message
> in a new project conversation. Each prompt is self-contained. Run sessions in order
> (Session 1 before Session 3; Sessions 1–6 before Session 7).
>
> **Model and tool settings per the iteration guide (Step 2.2 table):**
> - Session 1 (Schema/MEMIT): Sonnet 4.6 | Web Search ✓ | Deep Research ✗
> - Session 2 (State Consistency): Opus 4.6 | Web Search ✓ | Deep Research ✗
> - Session 3 (Security): Sonnet 4.6 | Web Search ✓ | Deep Research ✗
> - Session 4 (Validation): Sonnet 4.6 | Web Search ✓ | Deep Research ✗
> - Session 5 (MEMIT/Write Engine): Opus 4.6 | Web Search ✓ | Deep Research ✓*
> - Session 6 (State Consistency): Opus 4.6 | Web Search ✓ | Deep Research ✗
> - Session 7 (Cross-domain): Opus 4.6 | Web Search ✓ | Deep Research ✗
> - Session 8 (Cross-domain): Opus 4.6 | Web Search ✓ | Deep Research ✗
>
> *Deep Research for Session 5 only if the session reaches MEMIT architecture compatibility
> questions requiring current research literature. For pure spec reasoning, Web Search suffices.
>
> **Important v1.1 note:** The v1.1 integrated spec (llm-as-database-v1_1-integrated-spec.md)
> was produced after the gap backlog was written and has already closed or partially closed
> several gaps. Each prompt below notes the current v1.1 status of each gap and redirects
> the session accordingly.

---

═══════════════════════════════════════════════════════════════════════════════
## GAP SESSION 1 OF 8 — MEMIT Specialist + Graph Data Architect
### Gaps: GAP-3 | Primary skill: memit-specialist
═══════════════════════════════════════════════════════════════════════════════

```
Gap Session 1 of 8 — MEMIT Specialist + Graph Data Architect

Context: This is a targeted gap resolution session for the LLM as Database
framework spec. The v1.1 integrated spec is the active baseline. I am resolving
specific open questions from the gap backlog.

─── v1.1 STATUS NOTE ──────────────────────────────────────────────────────────
GAP-3 is PARTIALLY CLOSED in v1.1. The v1.1 spec added:
- `larql_syntax_version` header field (D81, C-GATE-1) — present and required in all patches
- Gate pre-check #8 enforcing this field (§10.2)
- Versioned patch parser for compaction re-runs (D82)
- `larql_migration_manifest` in Tier 1 config (`genesis-seal.json`)
- Ledger entries: `VERSION_REJECTED`, `VERSION_UNSUPPORTED`, `LARQL_VERSION_LEGACY`
- `min_supported_larql_version` and `current_larql_version` in Tier 1 config

What REMAINS OPEN (OQ-W6 residual, deferred to v2 in §18.3 and §6):
- Migration path authorship: who writes the `larql_migration_manifest` entries?
- Deprecation ceremony: how and when is an old `larql_syntax_version` moved below
  `min_supported_larql_version`? What is the ceremony, the notice period, the operator
  action required?
- Multi-version team deployment: if two Coder Agents are running simultaneously and one
  was authored under v1.0 schema and one under v1.1, what does the Gate do with the
  LARQL_VERSION_LEGACY advisory path — is advisory acceptable for production or only
  for a transition window?

This session should: (a) verify the v1.1 closure is complete and internally consistent,
(b) produce v2 outline spec blocks for the three remaining residual items so that v2
planning has a defined starting point rather than a blank slate.
───────────────────────────────────────────────────────────────────────────────

Gaps to resolve in this session:

GAP-3
Domain(s): MEMIT Specialist, Graph Data Architect
Description: The `.larql` schema versioning strategy is deferred to v2 (OQ-W6, §18.3).
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
is not currently covered by the Gate's pre-checks. Security note (Warden): If the Gate's
pre-check list does not include a schema version check, an attacker who can replay a patch
authored under an older schema version might bypass Validator checks added in the newer version.
Blocked by: Decision on whether `.larql` patches carry an explicit schema version field.
Blocks: Complete Gate pre-check spec, Validator L1 static analysis completeness, compaction
re-run strategy for superseded patches across version boundaries, v2 planning generally.
Priority: Critical

Relevant context from v1.1 spec:

§8.5 — The `.larql` Canonical Format (D15, extended by T1, IC-SC1, D81, D90)
"Every patch MUST carry a `larql_syntax_version` header field declaring the `.larql` syntax
version under which it was authored (D81, C-GATE-1). Current version: '1.1' (incorporating the
T1 two-number importance model). The Gate's version pre-check (§10.2 pre-check #8) enforces
this field. Compaction re-run parsing of superseded patches across version boundaries requires
the versioned patch parser and `larql_migration_manifest` declared in Tier 1 config (D82)."

§8.10 — Anchor-Superseded Archive
"Compaction re-run MUST parse all active `.larql` patches through the versioned patch parser.
Patches carrying a `larql_syntax_version` below the current version are translated via the
`larql_migration_manifest` before passing to MEMIT compile. Translation failure aborts
compaction (D82). The migration manifest is a Tier 1 config artifact; it is updated at the
same time as `current_larql_version` whenever a `.larql` syntax version advance occurs."

§10.2 — Gate Pre-Check #8 (D81, C-GATE-1)
"8. `larql_syntax_version` present and within supported range (D81, C-GATE-1). Absent or below
`min_supported_larql_version` → `VERSION_REJECTED` (hard rejection, no retry budget consumed).
Above `current_larql_version` → `VERSION_UNSUPPORTED` (hard rejection, operator alert set).
Between minimum and current → `LARQL_VERSION_LEGACY` advisory entry written (async), patch
proceeds (D82)."

§9.3 — Validator L1 Static Analysis
"L1 — Static analysis — all patches, mandatory (syntax, schema conformance, vocabulary check,
`larql_syntax_version` conformance per IC-GATE-8)."

§13.2 — Tier 1 Config fields (genesis-seal.json)
"`current_larql_version`, `min_supported_larql_version`, `larql_migration_manifest`"

§18.3 — Deferred to v2
"OQ-W6 (residual) — `.larql` schema version migration path authorship, deprecation ceremony,
multi-version team deployment (Gate enforcement layer closed in v1.1)."

§6 — Category 3: Deferred to v2
"`.larql` schema version migration path authorship and deprecation ceremony (OQ-W6 residual)."

Invoke the memit-specialist skill. Begin with any clarifying questions you need, then:
1. Verify the v1.1 closure of GAP-3 is complete and internally consistent — are there any
   seams in the `larql_migration_manifest` → versioned parser → compaction re-run chain?
2. Produce v2 outline spec blocks for: (a) migration manifest authorship ceremony, (b)
   version deprecation ceremony and notice period policy, (c) multi-version team deployment
   advisory window policy.
3. Confirm whether the `LARQL_VERSION_LEGACY` advisory path is sufficient for the v1→v2
   transition or whether the spec needs to define a harder transition timeline.

At the end of the session, generate a Gap Session Summary Block:

GAPS RESOLVED: [list with resolution]
GAPS PARTIALLY RESOLVED: [list with what remains]
GAPS DEFERRED: [list with reason]
NEW GAPS SURFACED: [any that emerged during the session]
NEW TENSIONS SURFACED: [any cross-domain conflicts that appeared]
```

---

═══════════════════════════════════════════════════════════════════════════════
## GAP SESSION 2 OF 8 — State Consistency Theorist
### Gaps: GAP-6, GAP-7 | Primary skill: state-consistency-theorist
═══════════════════════════════════════════════════════════════════════════════

```
Gap Session 2 of 8 — State Consistency Theorist

Context: This is a targeted gap resolution session for the LLM as Database
framework spec. The v1.1 integrated spec is the active baseline. I am resolving
specific open questions from the gap backlog.

─── v1.1 STATUS NOTE ──────────────────────────────────────────────────────────
GAP-6 is FULLY CLOSED in v1.1 by D84 and IC-TC-RESET (§11.8.1).
GAP-7 is FULLY CLOSED in v1.1 by D85 and IC-TC-TIMEOUT (§11.5.1).

Both closures happened in the Interface Contract Review Session that produced v1.1.

This session should:
(a) Verify each closure is complete, internally consistent, and has no residual seams.
(b) Check whether D84 and D85 introduced any new tensions or gaps not present in v1.0.
(c) Confirm the CIRCUIT_RESET Ledger entry type (added by D84) is fully catalogued
    in Appendix C and consistent with the W1/W2/W3 writer model in §16.2.
(d) Confirm the two-value timeout model (D85) handles the Genesis timeout scenario
    described in GAP-7 — specifically whether a Genesis PREPARED timeout produces a
    circuit-breaker trip or a TC-managed abort, and whether that is consistent with
    Genesis being a non-restartable event.
───────────────────────────────────────────────────────────────────────────────

Gaps to resolve in this session:

GAP-6
Domain(s): State Consistency Theorist
Description: The circuit breaker reset authority is labeled "operational policy" and left
unspecced (OQ-TC1, §11.8). The spec defines when the circuit breaker trips and what happens
when it trips (systemwide write suspension until human reset). What was not defined:
- Who constitutes "human" for reset authority?
- What verification must accompany a reset request? Is a reset a signed operation?
- What Ledger entry does a reset produce? (`CIRCUIT_RESET` was missing from Appendix C)
- Can the Orchestrator partially resume (allow reads, block writes) before full human reset,
  or is it binary?
This matters because the circuit breaker is the last line of defense against cascading 2PC
failures. An underspecced reset path is a gap in the safety model.
Blocked by: Policy decision on reset authority scope and the reset ceremony.
Blocks: Appendix C Ledger entry type catalog completeness; complete TC spec.
Priority: High

GAP-7
Domain(s): State Consistency Theorist
Description: The PREPARED-state timeout value was unspecced (OQ-TPC1, §18.1). The original
spec set it at "2-hour working starting value" decoupled from invocation token TTL (T7,
§11.5). Issues: (a) A Genesis compile may take considerably longer than 2 hours on a large
Architect Agent patch (up to 10,000 edges, sub-batched at 2,000). (b) No spec for what
happens on PREPARED timeout: TC auto-compensate or circuit-breaker trip? (c) No spec for how
PREPARED-state timeout interacts with the Dependency Hold — if 2PC times out and compensates,
does the Hold persist?
Blocked by: Implementation experience with MEMIT compile times, or a decision to set Genesis
PREPARED timeout separately from incremental PREPARED timeout.
Blocks: Complete TC behavior spec for long-running compiles; Genesis 2PC behavior when compile
time exceeds timeout.
Priority: High

Relevant context from v1.1 spec:

§11.5.1 — PREPARED-State Timeout Behavior (D85) [v1.1 closure of GAP-7]
"Two configurable timeout values apply (both stored in Tier 1 config):
`incremental_prepared_timeout` (default 2 hours) for all non-Genesis transactions, and
`genesis_prepared_timeout` (no default; Gate blocks Genesis initiation if absent, C-GATE-2)
for Genesis compiles.
Incremental timeout: TC executes Phase 1 rollback, releases Write Lock, sets task to
`AWAITING_OPERATOR_RETRY`. Dependency Hold persists through timeout — the Hold MUST NOT be
released automatically on timeout; it persists until successful commit on retry or explicit
operator-signed Hold release. Retry requires fresh token (infrastructure failure class per
D67 — no retry budget consumed). Three consecutive timeouts on the same task → human review
queue escalation, flagged `repeated_timeout`.
Genesis timeout: circuit breaker trips immediately (`DIVERGED_STATE` type per IC-TC-RESET).
No auto-compensation — partial compile state is preserved as forensic evidence. Operator MUST
run full model integrity check against the pre-Genesis `IMMUTABLE_ANCHOR` baseline before the
reset ceremony may proceed (IC-TC-TIMEOUT)."

§11.8 — Circuit Breaker (D48, C-TC3) [original]
"Thresholds: 3 consecutive 2PC failures in one task → trip. 5 consecutive 2PC failures across
any tasks in a 10-minute window → trip. Diverged state → immediate trip, no auto-repair.
On trip: systemwide write suspension (READ_ONLY mode — see §11.8.1)."

§11.8.1 — READ_ONLY Mode and Write Resumption Ceremony (D84) [v1.1 closure of GAP-6]
"On any circuit-breaker trip, the TC enters READ_ONLY mode immediately without human action.
Inference, query, and read operations proceed normally; write token issuance is suspended.
Consistency Status API state transitions to `CIRCUIT_TRIPPED`.
Write resumption requires a signed reset ceremony (IC-TC-RESET). The TC independently
verifies preconditions before accepting any reset request — human attestation alone is not
sufficient. For `CONSECUTIVE_FAILURE` and `CROSS_TASK_FAILURE` trips: TC verifies compensation
is `COMPLETED` and current overlay hash matches the Ledger's most recent `COMMITTED` entry.
For `DIVERGED_STATE` trips: TC requires a `RECONCILIATION_COMPLETE` Ledger entry with
`result: 'CONSISTENT'` timestamped after the trip. All preconditions met plus valid operator
signature → TC writes `CIRCUIT_RESET` (GOVERNANCE, synchronous) and enters WRITE_ENABLED state.
Reset via the W3 emergency Ledger path is not permitted."

§17.3 — Dependency Hold
"PREPARED-state timeout does NOT automatically release the Hold (D85). Hold persists until
successful commit on retry or operator-signed Hold release (GOVERNANCE category, signed
ceremony)."

§13.2 — Tier 1 Config (genesis-seal.json)
"`incremental_prepared_timeout` and `genesis_prepared_timeout` (no default; must be set before
Genesis initiation per C-GATE-2) in addition to genesis hash fields."

§18.4 — Closed in Integration
"OQ-TC1 — Circuit breaker reset authority (D84: signed ceremony with independent TC
precondition verification; IC-TC-RESET). READ_ONLY automatic on trip; write resumption via
ceremony only."
"OQ-TPC1 — PREPARED-state timeout value (D85: two-value model — `incremental_prepared_timeout`
default 2 hours; `genesis_prepared_timeout` no default, Gate-blocked if absent; IC-TC-TIMEOUT)."

Invoke the state-consistency-theorist skill. Begin with any clarifying questions you need, then:
1. Verify D84 (GAP-6 closure) is complete: Is READ_ONLY mode sufficiently defined? Does the
   TC precondition verification for each trip type cover all edge cases? Is the CIRCUIT_RESET
   Ledger entry (GOVERNANCE, synchronous) correctly placed in the W1/W2/W3 writer model?
2. Verify D85 (GAP-7 closure) is complete: Does the two-value timeout model handle the
   Genesis compile scenario from the original gap description? Is it internally consistent
   that a Genesis PREPARED timeout trips the circuit breaker while an incremental PREPARED
   timeout does not?
3. Surface any new tensions or gaps introduced by D84/D85. In particular: does the
   operator-signed Hold release ceremony (for Dependency Hold persistence through timeout)
   need a corresponding Ledger entry type? Does Appendix C need a `HOLD_RELEASED_SIGNED` entry?
4. If any residual gaps are found, define them as new gap entries.

At the end of the session, generate a Gap Session Summary Block:

GAPS RESOLVED: [list with resolution]
GAPS PARTIALLY RESOLVED: [list with what remains]
GAPS DEFERRED: [list with reason]
NEW GAPS SURFACED: [any that emerged during the session]
NEW TENSIONS SURFACED: [any cross-domain conflicts that appeared]
```

---

═══════════════════════════════════════════════════════════════════════════════
## GAP SESSION 3 OF 8 — AISecOps Specialist
### Gaps: GAP-5 | Primary skill: aisecops-specialist
═══════════════════════════════════════════════════════════════════════════════

```
Gap Session 3 of 8 — AISecOps Specialist

Context: This is a targeted gap resolution session for the LLM as Database
framework spec. The v1.1 integrated spec is the active baseline. I am resolving
specific open questions from the gap backlog.

─── v1.1 STATUS NOTE ──────────────────────────────────────────────────────────
GAP-5 is FULLY CLOSED in v1.1 by D87 and IC-SCOPE-UPDATE (§10.9).

The v1.1 spec defined:
- Mid-flight update model: scope updates accepted without draining in-flight invocations
- `SCOPE_UPDATED` Ledger entry (GOVERNANCE, synchronous) written before registry update
- `SCOPE_HASH_MISMATCH` error code (distinct from generic infrastructure failure)
- Structured error payload: `current_scope_hash` + `scope_updated_at`
- Orchestrator MUST re-issue token against current scope hash (not stale)
- Three consecutive `SCOPE_HASH_MISMATCH` → human review escalation
- Active PREPARED transactions not interrupted; scope changes are forward-only

This session should:
(a) Verify the D87 closure is complete and the trust boundary is airtight.
(b) Check whether the `SCOPE_UPDATED` Ledger entry + `SCOPE_HASH_MISMATCH` error code
    combination fully closes the attack surface identified in the original GAP-5 security note.
(c) Verify the three-consecutive escalation rule (§14.3) handles the recovery loop scenario —
    what if the Orchestrator itself is in a bad state and keeps issuing tokens with the stale
    scope hash?
(d) Surface any new gaps introduced by D87.
───────────────────────────────────────────────────────────────────────────────

Gaps to resolve in this session:

GAP-5
Domain(s): Security (Warden), MEMIT Specialist
Description: The Write Scope Definition update ceremony for long-running projects was only
partially addressed (OQ-S4). The spec established the YAML ↔ Write Scope Definition binding
(§10.9) and stated that changes affecting prompt content require a signed ceremony plus
`expected_yaml_hash` update. What was not defined was the behavior when a scope update occurs
while there are active in-flight invocation tokens or open Write Locks. Specifically:
- A token carries `write_scope_hash` and `expected_yaml_hash` bound at issuance time (§10.4).
  If the Write Scope Definition is updated while that token is in its 10-minute TTL window,
  the Gate rejects the token at the `write_scope_hash` pre-check (step 4 of §10.2).
- The spec classified this as an "infrastructure failure" class token rejection (§14.3),
  which means it re-issues a fresh token and does not consume retry budget. But the ceremony
  for a scope update is not atomic with token issuance — there is a window where old tokens
  are invalid and the agent has not yet received a new one.
- No spec for how the Orchestrator serializes scope updates against in-flight invocations.
Blocked by: Decision on scope-update serialization semantics — drain-first or mid-flight
update with token-rejection recovery path.
Blocks: Complete token lifecycle spec for mid-flight update case; long-running project
governance spec.
Priority: High

Relevant context from v1.1 spec:

§10.9 — Agent YAML ↔ Write Scope Definition Binding (D87, IC-SCOPE-UPDATE) [v1.1 closure]
"Write Scope Definition updates are accepted mid-flight — no drain of in-flight invocations
is required. An update MUST produce a `SCOPE_UPDATED` Ledger entry (GOVERNANCE, synchronous)
before the Orchestrator's in-memory scope registry is updated. The entry carries
`previous_scope_hash`, `new_scope_hash`, `operator_signature`, and `affected_agent_ids`.
Any in-flight token whose `write_scope_hash` predates the update will fail at Gate pre-check
step 4 with error code `SCOPE_HASH_MISMATCH` (distinct from generic infrastructure failure).
The error payload includes `current_scope_hash` and `scope_updated_at`, enabling the
Orchestrator to issue a corrected token without consuming the agent's retry budget. Active
PREPARED transactions are not interrupted; scope changes are forward-only."

§14.3 — Failure Mode: SCOPE_HASH_MISMATCH
"Scope hash mismatch (`SCOPE_HASH_MISMATCH`) — infrastructure failure class (D87). Gate returns
structured payload including `current_scope_hash` and `scope_updated_at`. Orchestrator MUST
re-issue token against current scope hash — NOT the stale hash. Retry budget not consumed.
Distinguished from generic hash-mismatch by the `SCOPE_HASH_MISMATCH` error code. Three
consecutive `SCOPE_HASH_MISMATCH` errors for the same invocation → Orchestrator escalates to
human review queue (possible recovery loop or scope update ceremony failure)."

§10.4 — Invocation-Scoped Single-Use Tokens
"Token fields: `write_scope_hash` — Write Scope Definition version at issuance;
`expected_yaml_hash` — Agent YAML version at issuance. An attacker stealing a token must also
keep every anchored document unchanged within the TTL window."

§10.2 — Gate Pre-Check Step 4
"4. `write_scope_hash` matches current Write Scope Definition version."

§18.4 — Closed in Integration
"OQ-S4 — Scope version management across long-running projects (D87: mid-flight update model;
`SCOPE_HASH_MISMATCH` error code defined; IC-SCOPE-UPDATE)."

Invoke the aisecops-specialist skill. Begin with any clarifying questions you need, then:
1. Verify D87 (GAP-5 closure) is airtight from a trust boundary perspective: Does the
   `SCOPE_UPDATED` Ledger entry → registry update sequencing prevent any race condition where
   an agent submits a patch against an old scope definition after the registry has been updated
   but before the Ledger entry is written?
2. Audit the three-consecutive-SCOPE_HASH_MISMATCH escalation rule: is three the right
   threshold, or should the first mismatch after a scope update ceremony always succeed (if
   the Orchestrator correctly reads the new scope hash from the payload)?
3. Check whether `SCOPE_HASH_MISMATCH` as an infrastructure failure class is correctly
   categorized — a genuine infrastructure failure does not consume retry budget, but a
   recovery-loop attack (attacker repeatedly triggering scope updates to exhaust an agent's
   operation window) exploits this classification. Does the spec need a rate-limit or
   time-window on scope updates?
4. Confirm whether `affected_agent_ids` in the `SCOPE_UPDATED` entry is sufficient for the
   Orchestrator to proactively notify affected in-flight agents, or whether agents rely
   entirely on Gate rejection to discover the update.
5. Surface any new gaps or tensions introduced by D87.

At the end of the session, generate a Gap Session Summary Block:

GAPS RESOLVED: [list with resolution]
GAPS PARTIALLY RESOLVED: [list with what remains]
GAPS DEFERRED: [list with reason]
NEW GAPS SURFACED: [any that emerged during the session]
NEW TENSIONS SURFACED: [any cross-domain conflicts that appeared]
```

---

═══════════════════════════════════════════════════════════════════════════════
## GAP SESSION 4 OF 8 — Validation Contract Architect
### Gaps: GAP-8, GAP-10 | Primary skill: validation-contract-architect
═══════════════════════════════════════════════════════════════════════════════

```
Gap Session 4 of 8 — Validation Contract Architect

Context: This is a targeted gap resolution session for the LLM as Database
framework spec. The v1.1 integrated spec is the active baseline. I am resolving
specific open questions from the gap backlog.

─── v1.1 STATUS NOTE ──────────────────────────────────────────────────────────
GAP-8 is PARTIALLY CLOSED in v1.1 by D88 and IC-CORPUS-AUTH (§13.3).
The following items are now specced:
- Corpus authorship is a restricted operator role (C-GOC4); only identities in
  `corpus_author_identities` (Tier 1 config field) may submit cases
- No agent identity may appear in `corpus_author_identities`
- Case formats formally defined: Meta-Validator `{ id, prompt, expected_assertion_set, expected_pass }`
  and Meta-TGA `{ id, specification_fragment, gold_test_set }`
- Minimum viable corpus: 20 cases before a meaningful Health Score is produced
- Below minimum: `health_score` field is `NOT_COMPUTED` (not zero)
- Corpus staleness flag: `corpus_staleness_flag: true` if no case added in 90 days

REMAINING OPEN in GAP-8 (OQ-V5 residual, per §18.2):
- Corpus extension cadence: how often must the corpus be extended? The spec flags
  staleness at 90 days but does not mandate a cadence.
- Authorship rotation policy: if an identity in `corpus_author_identities` is compromised
  or leaves, what is the update ceremony for that Tier 1 field?

GAP-10 is STILL OPEN (OQ-V1, per §18.2):
"Mechanism (constitutional suite in Tier 2 sealed corpus) is specced; runtime tagging and
promotion ceremony are not."
───────────────────────────────────────────────────────────────────────────────

Gaps to resolve in this session:

GAP-8
Domain(s): Validation Contract Architect
Description: The held-out corpus authorship cadence and authority for Meta-Validator and
Meta-TGA was only partially specced (OQ-V5, §18.2). The mechanism is defined: Tier 2 sealed
corpus with versioned additive directories, operator-signed manifests, and per-case audit
reporting. What remains open:
- How frequently must the corpus be extended? The Meta-Validator fires every 50 commits or
  weekly (§9.11) — if the corpus stagnates, the Health Score becomes meaningless as the model
  overfits to held-out cases.
- What is the update ceremony for `corpus_author_identities` (a Tier 1 field) when an
  authorized author must be added or removed? Tier 1 is mint-once — this appears to be a
  structural contradiction the spec does not address.
Blocked by: Policy decision on corpus authorship rotation and cadence enforcement.
Blocks: Meta-Validator and Meta-TGA operational readiness.
Priority: High (partially resolved in v1.1 — this session closes residual items)

GAP-10
Domain(s): Validation Contract Architect
Description: The constitutional test failure classification policy is labeled "operational
policy" rather than a spec decision (OQ-V1, §18.2). The constraint is specced (C25):
"Constitutional test suite failures are treated as Tier 3 regardless of the error's surface
appearance." The mechanism by which the Validator knows it is running a constitutional test
versus a task-specific test is not defined. What is missing:
- How does the Validator distinguish constitutional tests from task-generated tests at
  runtime? Are they tagged? In a separate test namespace?
- Who decides what "constitutional" means — what criteria qualify a test for promotion to
  the sealed constitutional suite?
- Is there a promotion ceremony, or does the operator directly add to the sealed corpus?
Blocked by: Policy decision on constitutional test tagging and the promotion ceremony from
task-generated tests to constitutional status.
Blocks: Nothing in current spec. Affects operational clarity.
Priority: Medium

Relevant context from v1.1 spec:

§9.5 — Failure Classification and Retry Limits
"Constitutional test suite failures are treated as Tier 3 regardless of the error's surface
appearance (C25)."

§9.11 — Meta-Validator
"Runs every 50 commits or weekly, whichever first. Evaluated against a held-out human-authored
suite per the Sealed Corpus pattern. Corpus authorship requirements and minimum viable corpus
size (20 cases) are defined in IC-CORPUS-AUTH and §13.3 (D88). Health Score is `NOT_COMPUTED`
when corpus is below 20 cases."
Validator Health Score thresholds: ≥95% no action; 85–94% warning, human review within 48
hours; <85% Validator suspended, immediate human review, recent passes audited.

§13.2 — Tier 1 Config (genesis-seal.json)
"`corpus_author_identities` — Tier 1 config field." [Mint-once, never modified.]

§13.3 — Tier 2 Sealed Artifacts (D88, IC-CORPUS-AUTH) [v1.1 closure of GAP-8 core]
"Corpus authorship is a restricted operator role (C-GOC4). Only identities listed in
`corpus_author_identities` (Tier 1 config field) may submit cases. No agent identity MUST
appear in this list. Case formats are formally defined:
- Meta-Validator case format: `{ id, prompt, expected_assertion_set: [{ type, value }...], expected_pass }`
- Meta-TGA case format: `{ id, specification_fragment, gold_test_set: [{ test_name, assertion_count (≥2), asserts_symbols }...] }`
Minimum viable corpus: 20 cases. Below minimum, `health_score` field is `NOT_COMPUTED`.
A corpus staleness flag (`corpus_staleness_flag: true`) is set if no case has been added in
90 days. Cadence is operator-owned policy, not enforced by this spec."

Constitutional suite artifact (§13.3 Tier 2):
"`constitutional-suite/` — Constitutional test suite (promoted from S4 D32)."
"Validator has persistent read access during normal operation."

§18.2 — Operational Policy (Open Questions)
"OQ-V1 — Constitutional test failures as Tier 3 classification (policy). Mechanism
(constitutional suite in Tier 2 sealed corpus) is specced; runtime tagging and promotion
ceremony are not."
"OQ-V5 — PARTIALLY CLOSED by D88 (IC-CORPUS-AUTH). Corpus authorship role (C-GOC4), case
formats, and minimum viable corpus size (20 cases) now specced. Corpus extension cadence and
authorship rotation policy remain operator-owned."

Invoke the validation-contract-architect skill. Begin with any clarifying questions you need, then:

For GAP-8 residual items:
1. Address the Tier 1 contradiction: `corpus_author_identities` is a mint-once Tier 1 field,
   but operators need to add or remove authorized authors over the project lifetime. Define
   whether this requires a spec mechanism (e.g., an indirect approach — a Tier 2 artifact
   for the live author list, with Tier 1 containing only the bootstrapping identity) or an
   exceptional update ceremony for Tier 1.
2. Define whether the 90-day staleness flag is sufficient as the only cadence signal, or
   whether the spec should set a minimum cadence requirement (e.g., at least N cases added
   per M commits).

For GAP-10:
3. Define the runtime tagging mechanism: how does the Validator know at runtime that a given
   test belongs to the constitutional suite vs. a task-generated test? (Options: file path
   convention within the `constitutional-suite/` artifact; explicit `test_type` tag in test
   metadata; separate invocation call to a different corpus endpoint.)
4. Define constitutional qualification criteria: what properties must a test have to be
   eligible for promotion? (Options: asserts a framework-level invariant not specific to any
   task; passes against a known-good model state; authored by an identity in
   `corpus_author_identities`.)
5. Define the promotion ceremony: how does a task-generated test become constitutional?
   (Direct operator addition to `constitutional-suite/` Tier 2 artifact using the versioned
   additive directory pattern? Or a separate nomination and review workflow?)

At the end of the session, generate a Gap Session Summary Block:

GAPS RESOLVED: [list with resolution]
GAPS PARTIALLY RESOLVED: [list with what remains]
GAPS DEFERRED: [list with reason]
NEW GAPS SURFACED: [any that emerged during the session]
NEW TENSIONS SURFACED: [any cross-domain conflicts that appeared]
```

---

═══════════════════════════════════════════════════════════════════════════════
## GAP SESSION 5 OF 8 — MEMIT Specialist (+ Validation, State Consistency)
### Gaps: GAP-9, GAP-11, GAP-15 | Primary skill: memit-specialist
═══════════════════════════════════════════════════════════════════════════════

```
Gap Session 5 of 8 — MEMIT Specialist (secondary: Validation Contract Architect,
                                        State Consistency Theorist)

Context: This is a targeted gap resolution session for the LLM as Database
framework spec. The v1.1 integrated spec is the active baseline. I am resolving
specific open questions from the gap backlog.

─── v1.1 STATUS NOTE ──────────────────────────────────────────────────────────
GAP-9 (OQ-W8) is STILL OPEN — behavioral probe generalization beyond code domains
is not addressed in v1.1.

GAP-11 (OQ-SC2) is STILL OPEN — external document provenance tracking for Layer 4
facts is not addressed in v1.1 (§18.2 notes it is only partially addressed by
Layer4_domain project-lifetime retention).

GAP-15 (OQ-OC3) is PARTIALLY CLOSED in v1.1 by D86 and IC-OC-PROBE (§11.14).
The following is now specced:
- Compaction verification probe class: `probe_type: "COMPACTION_REGRESSION"`
- Structured `CompactionProbeReport` returned to TC before Phase 2 commit
- Sampling rates: 100% of CORE, ≥20% of SUPPORTING (floor 5 probes), 10% of INCIDENTAL
  (floor 3 probes)
- Random seed logged for reproducibility
- Abort thresholds: CORE pass rate = 1.0 (C-OC3, hard); SUPPORTING ≥95%; INCIDENTAL ≥80%
- Abort behavior: existing overlays retained, `COMPACTION_ABORTED` entry with serialized
  CompactionProbeReport as payload
- Probe infrastructure failure → `COMPACTION_PROBE_FAILED` (distinct entry type)

REMAINING OPEN in GAP-15 (OQ-OC3 residual):
- SUPPORTING and INCIDENTAL sampling rates (20% and 10%) and abort thresholds (95% and 80%)
  are explicitly provisional pending OQ-W1 (empirical threshold calibration). CORE threshold
  of 1.0 and C-OC3 are not provisional.
───────────────────────────────────────────────────────────────────────────────

Gaps to resolve in this session:

GAP-9
Domain(s): Validation Contract Architect, MEMIT Specialist
Description: Behavioral probe generalization beyond code domains is unspecced (OQ-W8, §18.1).
The spec's behavioral probe (§8.9 L2, §9.3 L2) is described in terms of "generation tests"
and "inference probes" — language implying a code-execution or code-fact retrieval framing.
The Validation Layer specifies "inference probe" as a mandatory gate for `CORE` and
`SUPPORTING` edges, but does not define what a behavioral probe looks like for non-code
domains (e.g., a `domain_concept` edge asserting a legal constraint, a business rule, or an
architectural invariant that does not correspond to runnable code). Without a domain-general
probe spec, the Validator's L2 check is only fully defined for code-domain deployments.
Blocked by: Decision on probe format generalization.
Blocks: Non-code deployment planning.
Priority: Medium

GAP-11
Domain(s): State Consistency Theorist, MEMIT Specialist
Description: Layer 4 domain knowledge recovery when the originating external document is
unavailable is only partially addressed (OQ-SC2, §18.2). The spec notes this is "partially
addressed by Layer4_domain project-lifetime retention." What is not defined:
- If a Layer 4 fact is written from an external document (e.g., a reference spec, a
  third-party API description) and that document later changes or disappears, the fact in
  `.vindex` may become stale. The Pruning Agent cannot catch this because the external
  document is not in Git.
- No mechanism for the harness to detect that the authoritative source for a Layer 4 fact
  has changed.
- The spec says "no auto-compile" for out-of-band changes — but out-of-band changes to
  external documents are not even detectable by the Pruning Agent, which monitors Git commits.
Blocked by: Decision on whether the harness tracks external document provenance for Layer 4
facts (URL pinning? hash of source at write time?).
Blocks: Nothing in current spec. Affects long-running project correctness.
Priority: Medium

GAP-15
Domain(s): Validation Contract Architect, MEMIT Specialist
Description: The compaction verification sample size was labeled a starting heuristic (OQ-OC3,
§18.1): "100% CORE + 10% random sample of others." What was not defined:
- How the 10% sample is drawn — random seed? Stratified by `declared_importance`? By age?
  By namespace?
- If compaction verification fails, the spec says "existing overlays retained" — but the
  failure report format returned by the Behavioral Probe to the TC was unspecced.
Blocked by: GAP-1 (OQ-W1 — empirical understanding of compaction frequency and total edge
volumes determines whether 10% is a meaningful sample or noise).
Blocks: Nothing independently; only the sampling threshold detail was missing.
Priority: Medium (partially resolved in v1.1 — this session addresses residuals)

Relevant context from v1.1 spec:

§8.9 — Post-Write Verification (D18)
"Two-level mandatory probe:
L1 — Storage probe (mandatory for all writes): `SELECT` read-back confirms edge was written.
L2 — Behavioral probe (mandatory for `declared_importance ∈ {CORE, SUPPORTING}`): generation
test confirms the fact fires correctly in inference.
Storage-pass / behavior-fail is a named failure mode (D19, D30).
Compaction verification uses a distinct probe class (`probe_type: 'COMPACTION_REGRESSION'`)
that tests whether previously encoded facts survived a recompile, not whether a new fact was
accepted. This probe is defined in IC-OC-PROBE and produces a `CompactionProbeReport`."

§9.3 — Validation Layer L2
"L2 — Inference probe — edges with `declared_importance ∈ {CORE, SUPPORTING}`, mandatory
(behavioral probe)."

§11.14 — Overlay Compaction (D86) [v1.1 partial closure of GAP-15]
"Verification (D66, extended D86): Behavioral Probe returns a structured `CompactionProbeReport`
to the TC before Phase 2 commit (IC-OC-PROBE). Sampling: 100% of CORE edges (full), ≥20% of
SUPPORTING edges (stratified, floor 5 probes), 10% of INCIDENTAL edges (stratified, floor 3
probes). Random seed logged for reproducibility. Abort thresholds: CORE pass rate MUST equal
1.0 (C-OC3 — any CORE failure is an immediate compaction abort); SUPPORTING ≥95%; INCIDENTAL
≥80%. Abort → existing overlays retained, `COMPACTION_ABORTED` Ledger entry with serialized
`CompactionProbeReport` as payload. CORE failures individually listed; SUPPORTING and INCIDENTAL
failures summary-logged unless ≤10 IDs.
Probe infrastructure failure → `COMPACTION_PROBE_FAILED` entry (distinct from
`COMPACTION_ABORTED`). All SUPPORTING and INCIDENTAL thresholds and sampling rates are
provisional pending OQ-OC3 / OQ-W1 calibration. The CORE 1.0 threshold and C-OC3 are not
provisional."

§11.13 — Out-of-Band Git Reconciliation
"Humans or external tools may commit to Git outside the harness pipeline. Pruning Agent detects
these and generates catch-up patches flagged `requires_human_review`. No auto-compile."

§18.1 — Empirical / Post-Deployment Tuning (Open Questions)
"OQ-W8 — Behavioral probe generalization beyond code domains."
"OQ-OC3 — Compaction verification sampling calibration (failure report format and abort
thresholds now specced by D86, IC-OC-PROBE; sampling rates for SUPPORTING and INCIDENTAL tiers
remain provisional pending OQ-W1 resolution)."

§18.2 — Operational Policy (Open Questions)
"OQ-SC2 — Layer 4 recovery when originating external document unavailable (partially addressed
by Layer4_domain project-lifetime retention; external document provenance tracking is unspecced)."

Invoke the memit-specialist skill. Begin with any clarifying questions you need, then:

For GAP-9 (behavioral probe generalization):
1. Define a domain-agnostic inference probe protocol. The core challenge: for a code-domain
   deployment, "the fact fires correctly in inference" has a verifiable meaning (the model
   generates correct code given a prompt). What is the equivalent verifiable criterion for
   a `domain_concept` edge asserting a legal constraint or business rule?
2. Define what "probe passes" means outside a code-execution context. Candidates: (a) model
   generates a description consistent with the written fact when prompted; (b) model correctly
   answers a templated factual question about the written edge; (c) model's probability
   distribution on a forced-choice question has the expected argmax.
3. Define whether the probe protocol is a Validator responsibility (who writes the probe
   template?) or an authoring-time responsibility (the agent who authors the `.larql` patch
   must also supply a probe template as part of the patch). Note the actor-critic independence
   constraint (D32–D33) if considering agent-supplied probes.

For GAP-11 (Layer 4 external document provenance):
4. Decide whether the harness tracks external document provenance for Layer 4 facts, and if
   so, define the provenance record structure. Options: (a) URL pinning with hash of source at
   write time — stored in `.larql` patch metadata and in the Ledger entry; (b) no tracking,
   but Layer 4 patches must declare an `external_source_id` that maps to a human-maintained
   registry; (c) no spec-level tracking — treated as operator responsibility.
5. If provenance tracking is specced: define what happens when a provenance check detects
   the source document has changed (triggers a Pruning-Agent-like catch-up workflow? Generates
   a staleness advisory Ledger entry?). Note that the Pruning Agent monitors Git commits, not
   external URLs — define whether provenance checking is a separate monitoring component or an
   extension of Pruning Agent scope.

For GAP-15 residual:
6. Verify D86 (partial closure) is internally consistent: does the "stratified" sampling
   description for SUPPORTING and INCIDENTAL tiers define stratification criteria sufficiently
   (stratified by what — `declared_importance` band only, or also by age, namespace, or tier)?
   The current spec says "stratified" but does not define the stratification key.

At the end of the session, generate a Gap Session Summary Block:

GAPS RESOLVED: [list with resolution]
GAPS PARTIALLY RESOLVED: [list with what remains]
GAPS DEFERRED: [list with reason]
NEW GAPS SURFACED: [any that emerged during the session]
NEW TENSIONS SURFACED: [any cross-domain conflicts that appeared]
```

---

═══════════════════════════════════════════════════════════════════════════════
## GAP SESSION 6 OF 8 — State Consistency Theorist
### Gaps: GAP-12, GAP-14 | Primary skill: state-consistency-theorist
═══════════════════════════════════════════════════════════════════════════════

```
Gap Session 6 of 8 — State Consistency Theorist

Context: This is a targeted gap resolution session for the LLM as Database
framework spec. The v1.1 integrated spec is the active baseline. I am resolving
specific open questions from the gap backlog.

─── v1.1 STATUS NOTE ──────────────────────────────────────────────────────────
GAP-12 is FULLY CLOSED in v1.1 by D89 and IC-LDG-RETAIN (§16.7).
The following is now specced:
- Retention policy declared at bootstrap via `PROJECT_INITIATED` (W2 bootstrap, immutable)
- Default: PROJECT_LIFETIME if not specified
- Immutable-downward: retention MUST NOT be shortened once configured (C-SL2)
- Extensions permitted via `RETENTION_OVERRIDE_EXTENDED` (GOVERNANCE, signed ceremony)
- Ledger blocks shortening regardless of operator key validity
- Unconditional invariant: epochs with `INTEGRITY_VIOLATION` retained INDEFINITELY
- Project close: `PROJECT_CLOSED` (LIFECYCLE, signed ceremony) seals final epoch, Ledger
  read-only
- Archival format: gzip bundles with operator-signed SHA-256 manifest, format version "1.0"
- `PROJECT_CLOSED` is write-final — Ledger read-only even if archival pending

This session should:
(a) Verify the D89 closure of GAP-12 is complete.
(b) Focus the bulk of the session on GAP-14 — the async threshold suite rationale framework.
    GAP-14 (T5/T11 thresholds) remains STILL OPEN.
───────────────────────────────────────────────────────────────────────────────

Gaps to resolve in this session:

GAP-12
Domain(s): State Consistency Theorist
Description: The full Ledger epoch retention policy was only mechanism-specced, not policy-
specced (OQ-SL1, §18.2, §16.7). The spec defined default project-lifetime retention and the
archival mechanism. What was not defined:
- What "project-lifetime" means operationally. When does a project end? Is there a ceremony?
- Can operators override the default retention period downward (shorter)?
- The archival storage format was unspecced beyond "compressed, manifest-sealed bundles."
Blocked by: Operational policy decision on project lifecycle and retention override governance.
Priority: Medium (fully resolved in v1.1 — verify closure in this session)

GAP-14
Domain(s): State Consistency Theorist, Orchestration Comparativist
Description: The async WAL flush cadence, Ledger verification intervals, and Reconciliation
Queue backlog thresholds are all listed as "starting heuristics" (§18.1, T5/T11 thresholds):
- WAL flush cadence before acknowledgment — unspecified; affects durability guarantee during
  the async write window.
- Light verification interval: every 100 entries (§16.4) — a starting heuristic with no
  justification for the 100-entry number.
- Full verification interval: 10,000 entries OR 24 hours (§16.4) — similarly provisional.
- Reconciliation backlog thresholds: 10 items / 7 days for warning; 50 items / 30 days for
  critical (§15.2) — no empirical basis stated.
Blocked by: Implementation experience with Ledger write volumes under realistic task
throughput and out-of-band Git commit rates.
Blocks: Nothing architecturally. All thresholds are tunable without spec changes.
Priority: Medium

Relevant context from v1.1 spec:

§16.7 — Ledger Epoch Archival and Retention Policy Interface (D89) [v1.1 closure of GAP-12]
"Retention policy (IC-LDG-RETAIN): Retention policy is declared at bootstrap via
`PROJECT_INITIATED` (LIFECYCLE, W2 bootstrap writer, immutable post-mint). Default if not
specified: PROJECT_LIFETIME. Retention is immutable-downward (C-SL2): once configured, it
MUST NOT be shortened. Extensions (longer retention) are permitted via
`RETENTION_OVERRIDE_EXTENDED` (GOVERNANCE, signed ceremony). The Ledger layer blocks any
shortening attempt regardless of operator key validity.
Unconditional invariant: Epochs containing any `INTEGRITY_VIOLATION` entry are retained
INDEFINITELY, regardless of configured retention policy and regardless of any operator
override attempt.
Project close: `PROJECT_CLOSED` (LIFECYCLE, signed ceremony) seals the final epoch and makes
the Ledger read-only. Archival format: gzip bundles with operator-signed SHA-256 manifest,
format version '1.0'. `PROJECT_CLOSED` is write-final — Ledger is read-only even if archival
is pending (cold storage unavailable). Archival retried with exponential backoff when storage
becomes available."

§16.3 — Write Mode Classification (async writes)
"Asynchronous (durable queue) — observation entries: Meta-Validator / Meta-TGA health records,
sealed corpus access records, config update notifications, `LARQL_VERSION_LEGACY` (advisory),
`CORPUS_CASE_ADDED`, `COMPACTION_CORPUS_SMALL` (advisory), `CONTENT_SPLIT_LOOP` (advisory).
Async writes go through WAL (`<harness_root>/.state-ledger/wal/`) before acknowledgment.
WAL replays on crash. Ordering preserved within the queue; Merkle-chain order remains
consistent."

§16.4 — Integrity Verification Cadence
"Light verification: every 100 entries appended. Verifies last ~10 entries. Cheap; catches
immediate corruption. Full verification: every 10,000 entries OR 24 hours, whichever first.
Walks entire chain. Chain-break detection during any verification triggers immediate write
suspension."

§15.2 — Backlog Signals (Reconciliation Queue)
"≤ 10 items, all < 7 days old: `NORMAL` state.
> 10 items OR any > 7 days: `RECONCILIATION_BACKLOG_WARNING` Ledger entry; state remains
`NORMAL`.
> 50 items OR any > 30 days: `RECONCILIATION_BACKLOG_CRITICAL` Ledger entry; Consistency
Status state becomes `RECONCILIATION_BACKLOG`.
`stale_urgent` edge count > 1,000 (D55): write suspension triggers independently."

§18.1 — Empirical / Post-Deployment Tuning
"T5 / T11 thresholds — async WAL flush cadence, verification intervals, backlog thresholds
— all starting heuristics."

Invoke the state-consistency-theorist skill. Begin with any clarifying questions you need, then:

For GAP-12:
1. Verify the D89 closure is complete: (a) Is `PROJECT_CLOSED` as a LIFECYCLE entry in the W1
   writer path (not W2 bootstrap) despite being a signed ceremony? The spec says W2 is
   "one-time bootstrap only" — is project close inside or outside bootstrap scope?
   (b) Does the exponential backoff retry for archival need a maximum retry count or a
   human alert threshold before the Ledger remains un-archived indefinitely?

For GAP-14 (the main work of this session):
2. Produce a rationale framework for each provisional threshold — not new values (empirical
   data is not available), but a definition of the guarantee each threshold is intended to
   satisfy. For each, state: what durability or detection guarantee does this threshold serve?
   what is the failure mode if the threshold is too high (too infrequent)? too low (too
   frequent)?
   - WAL flush cadence: what is the maximum data loss window this cadence should bound?
   - Light verification interval (100 entries): how many entries constitute a "meaningful
     corruption detection window" for the Merkle-chain-lite model?
   - Full verification interval (10,000 / 24h): what audit-completeness guarantee does this
     serve, and what is the cost model justification for the 24-hour fallback?
   - Reconciliation backlog thresholds (10/7d warning; 50/30d critical): what SLA on
     out-of-band sync are these proxies for?
3. Define the update ceremony for threshold values when empirical data becomes available:
   which Ledger entry type records a threshold change? Who has authority to change them?
   Are they Tier 1 (immutable) or Tier 3 (Git-committed config)?

At the end of the session, generate a Gap Session Summary Block:

GAPS RESOLVED: [list with resolution]
GAPS PARTIALLY RESOLVED: [list with what remains]
GAPS DEFERRED: [list with reason]
NEW GAPS SURFACED: [any that emerged during the session]
NEW TENSIONS SURFACED: [any cross-domain conflicts that appeared]
```

---

═══════════════════════════════════════════════════════════════════════════════
## GAP SESSION 7 OF 8 — Full Framework Council
### Gaps: GAP-2, GAP-1, GAP-4 | Primary skill: framework-council
═══════════════════════════════════════════════════════════════════════════════

```
Gap Session 7 of 8 — Full Framework Council

Context: This is a targeted gap resolution session for the LLM as Database
framework spec. The v1.1 integrated spec is the active baseline. I am resolving
specific open questions from the gap backlog.

─── v1.1 STATUS NOTE ──────────────────────────────────────────────────────────
All three gaps in this session remain FULLY OPEN in v1.1:
- GAP-2 (OQ-W2): MEMIT/target model architecture compatibility — unresolved.
- GAP-1 (OQ-W1): all drift/compaction thresholds remain provisional.
- GAP-4 (D72): orchestration path selection remains deferred to operator.

These gaps are externally blocked — they cannot be fully closed through spec work
alone. GAP-2 requires target model selection + MEMIT compatibility test. GAP-1
requires GAP-2 resolution + write-volume stress test data. GAP-4 requires an
operator decision on Path A, B, or C.

This session produces PREPARATORY SPEC WORK and CONTINGENT PATH SPECS:
- For GAP-2: a compatibility test protocol (what tests must pass before the write
  engine spec is considered verified against the chosen model).
- For GAP-1: a threshold validation framework (how provisional values become
  authoritative; the spec update ceremony when empirical data arrives).
- For GAP-4: three contingent spec blocks — one per path — so that when the operator
  selects a path, the relevant spec block activates without requiring another council session.

Full council is required because these gaps cascade across all six domains:
- GAP-2 affects: MEMIT write engine (layer targets), Security (edge cap justification),
  Validation (divergence check thresholds), State Consistency (compaction scheduling assumes
  MEMIT compile-time behavior).
- GAP-1 affects: State Consistency (drift/compaction triggers), Validation (compaction
  verification sampling rates), Security (backpressure ceiling justification).
- GAP-4 affects: Security (delegation token shape differs by path), State Consistency
  (2PC Transaction Controller placement differs by path), Orchestration (all non-negotiables
  must be verified per path).
───────────────────────────────────────────────────────────────────────────────

Gaps to resolve in this session:

GAP-2
Domain(s): MEMIT Specialist
Description: MEMIT's compatibility with the target model architecture has not been verified
(OQ-W2). The spec designates MEMIT as the write engine (D12) and specifies it targets
middle-to-late FFN layers (L15–L25 for a 32-layer model; §8.2, C15). These layer coordinates
are not universal constants; they depend on the target model's architectural depth and
attention-head configuration. If the target model has a different layer count, different FFN
width, or uses an architecture variant (MoE, Mamba-family, grouped-query attention) that
MEMIT's covariance-update math does not model correctly, the entire write engine spec is built
on an unverified assumption. Two downstream claims are contingent on this:
- Orthogonal projection and covariance balancer safeguards (D20, §8.2) assume MEMIT's
  mathematical guarantees hold for the chosen architecture.
- `declared_importance` ↔ `attention_weight` divergence check thresholds (0.5 and 0.9 in
  §8.6) are calibrated against MEMIT's expected output distribution.
Blocked by: Explicit target model specification + MEMIT compatibility test run.
Blocks: GAP-1 resolution; layer targeting spec correctness; edge cap justification.
Priority: Critical

GAP-1
Domain(s): MEMIT Specialist
Description: All drift-from-anchor and compaction threshold values are provisionally specified
but empirically unvalidated (OQ-W1). This includes:
- Drift warning: 1,500 edges since last anchor (§8.7, §11.14)
- Drift hard trigger: 8,000 edges (§8.7)
- MEMIT internal sub-batch ceiling: 2,000 edges (§8.8)
- Overlay file count trigger: 50+ files (§11.14)
- p95 inference latency trigger: 2× baseline (§11.14)
- `stale_urgent` backpressure ceiling: 1,000 edges (§11.12)
- 24-hour Pruning floor (§17.5)
These propagate into circuit-breaker logic, compaction scheduling, Pruning backpressure,
and write engine capacity planning.
Blocked by: Target model selection + write volume stress test against that model's FFN.
Blocks: GAP-5 (compaction verification sample tuning), meaningful circuit-breaker threshold
rationale, write-budget SLA spec.
Priority: Critical

GAP-4
Domain(s): Orchestration Comparativist
Description: Orchestration path selection (Path A — LangGraph alone; Path B — Claude Agent
SDK alone; Path C — Hybrid) is explicitly operator-decided (D72, §12.3). This leaves two
items underspecced:
(a) Nested sub-agent delegation token design: delegation tokens for nested sub-agent
    invocations (Path B/C nested cases) are deferred to v2. Without knowing which path is
    selected, the shape of this v2 feature cannot be outlined. Path A uses a different
    concurrency and subgraph model than Path B.
(b) Human-in-the-loop interface spec: review queues are defined (§15) but the mechanism by
    which the human returns a decision to the Orchestrator is defined only at the conceptual
    level (`approve_as_is`, `reject`, etc.). The actual interface — webhook, CLI, API endpoint,
    message queue — is path-dependent and fully unspecced.
Blocked by: Operator selection of Path A, B, or C.
Blocks: Delegation token v2 spec shape; HIL interface spec.
Priority: High

Relevant context from v1.1 spec:

§8.2 — MEMIT as the Designated Engine
"MEMIT is the designated write engine (D12). ROME, GRACE, and full fine-tuning are explicitly
excluded. MEMIT targets middle-to-late FFN layers (L15–L25 for a 32-layer model; C15).
Two mandatory safeguards (D20): orthogonal projection and covariance balancer."

§8.6 — Importance and Attention Weight — Two-Number Model (T1)
"A divergence check runs post-compile: if `declared_importance = CORE` yields engine-computed
`attention_weight < 0.5`, or `declared_importance = INCIDENTAL` yields `> 0.9`, the Validator
flags the write as a soft signal for review. Not a hard rejection."

§8.7 — Drift-from-Anchor Thresholds
"Drift warning: 1,500 edges since last anchor. Drift hard trigger: 8,000 edges.
All thresholds are provisional pending empirical validation against target model (OQ-W1)."

§8.8 — Architect Capacity Model
"MEMIT recommended batch size: 2,000 edges. Patches exceeding this are sub-batched internally.
Sub-batching is transparent to the ledger."

§11.12 — Pruning Agent
"Backpressure (D55): 24-hour staleness window; edges older than 24h classified `stale_urgent`.
At 1,000 `stale_urgent`, writes suspended until Pruning completes."

§11.14 — Overlay Compaction (triggers)
"Trigger conditions: Drift tier WARNING → schedule at next idle window. Drift tier HARD →
immediate, blocking writes. Time-based: every 30 days since last anchor.
`drift_state.overlay_file_count` ≥ 50: schedule. `drift_state.p95_latency_ratio` ≥ 2.0:
schedule. All drift threshold values are provisional pending empirical validation (OQ-W1)."

§12.3 — Three Path Options (D72)
"Path A — LangGraph alone. Path B — Claude Agent SDK alone. Path C — Hybrid (LangGraph + SDK).
No path is recommended in this spec. All three are comparable; selection is operational policy.
Regardless of path, the 2PC Transaction Controller and the Merkle-chain State Ledger are custom
components — no evaluated candidate ships them natively (D80)."

§15 — Review Pathways — Two-Queue Model
"Correctness Review Queue: decisions: `approve_as_is` | `reject` | `re_route_for_further_work`.
Reconciliation Review Queue: decisions: `approve_patch` | `reject_patch` | `modify_patch` |
`defer_with_reason`. Default on neglect [Correctness Queue]: task times out into logged
suspension. Default on neglect [Reconciliation Queue]: items accumulate; backlog signals
escalate."

§18.1 — Empirical Open Questions
"OQ-W1 — Cumulative edit volume degradation threshold (model-specific). All drift numbers
(1,500 / 8,000 / 2,000 sub-batch) are provisional."
"OQ-W2 — MEMIT/target model architecture compatibility verification."

Invoke the framework-council skill. Convene the full council — all six specialist voices are
needed. Begin with any clarifying questions you need, then address each gap in the sequence
below. The session produces conditional and preparatory spec blocks, not gap closures.

For GAP-2 (MEMIT Specialist primary, all specialists contribute conditional branches):
1. Define the MEMIT compatibility test protocol: what specific tests must pass against the
   chosen model architecture before the write engine spec is considered verified? Define the
   protocol sufficiently that an engineer could execute it without returning to the council.
2. Define the compatibility assessment dimensions: layer targeting (is L15–L25 correct for
   the chosen model?), covariance math validity (does MEMIT's formulation hold for the
   architecture variant?), safeguard behavior (do orthogonal projection and covariance
   balancer produce the expected outputs?), divergence check calibration (are 0.5 and 0.9
   meaningful thresholds for this model's output distribution?).
3. Produce conditional spec blocks: "If MEMIT compatibility confirmed: [spec text — adopt
   L15–L25 and existing thresholds as authoritative]. If architecture incompatible:
   [alternative evaluation criteria — what would the council need to assess a replacement
   write engine against the same requirements?]."
4. Each specialist should define their domain's plan B: what changes in their spec domain
   if MEMIT is found incompatible?

For GAP-1 (MEMIT Specialist primary, State Consistency and Validation contribute):
5. Define the threshold validation framework: a protocol for replacing provisional values
   with empirically grounded values. What scenario, what model, what measurement instruments,
   what pass/fail criteria for each threshold? The framework must be specific enough to
   execute.
6. Define the spec update ceremony: when empirical data replaces provisional values, which
   sections update, which IDs are promoted from provisional to authoritative, and who
   authorizes the update? Are these Tier 1 (immutable) or Tier 3 (Git-committed) config?
7. All current threshold values remain provisional. The session confirms they are flagged
   consistently throughout the spec and identifies any places where they appear without the
   provisional flag.

For GAP-4 (Orchestration Comparativist primary, Warden and State Consistency contribute):
8. Produce three conditional spec blocks — one per path, each marked "activates on operator
   selection of Path [X]":
   - Path A (LangGraph alone): delegation token shape for subgraph delegation; HIL decision
     delivery mechanism within LangGraph's concurrency model; 2PC TC placement within a
     LangGraph execution graph.
   - Path B (Claude Agent SDK alone): delegation token shape for nested sub-agent
     invocations; HIL decision delivery via SDK callback or interrupt; sub-agent write scope
     inheritance model.
   - Path C (Hybrid): delegation token handoff at the LangGraph ↔ SDK boundary; HIL delivery
     in a mixed concurrency model; scope inheritance when an SDK sub-agent is spawned from a
     LangGraph node.
9. For each path, Warden must define the trust boundary shape: where does the token
   verification happen in this path's execution model?
10. For each path, State Consistency Theorist must define where the 2PC Transaction
    Controller lives and how compaction scheduling is triggered within that path's event loop.

At the end of the session, generate a Gap Session Summary Block:

GAPS RESOLVED: [list with resolution]
GAPS PARTIALLY RESOLVED: [list with what remains]
GAPS DEFERRED: [list with reason]
NEW GAPS SURFACED: [any that emerged during the session]
NEW TENSIONS SURFACED: [any cross-domain conflicts that appeared]
```

---

═══════════════════════════════════════════════════════════════════════════════
## GAP SESSION 8 OF 8 — Full Framework Council (v2 Outline)
### Gaps: GAP-13, GAP-16, GAP-17, GAP-18, GAP-19 | Primary skill: framework-council
═══════════════════════════════════════════════════════════════════════════════

```
Gap Session 8 of 8 — Full Framework Council — v2 Outline Session

Context: This is a targeted gap resolution session for the LLM as Database
framework spec. The v1.1 integrated spec is the active baseline. All gaps in
this session are v2-deferred and cannot be closed in v1. The session produces
v2 OUTLINE SPEC BLOCKS — structured statements of what v2 must define — so that
v2 planning has a defined starting point and does not need to reopen v1
architectural decisions.

─── v1.1 STATUS NOTE ──────────────────────────────────────────────────────────
All five gaps in this session are v2-deferred and unchanged in v1.1:
- GAP-13 (OQ-S5): Genesis automation via secondary LLM reviewer — v2 only.
- GAP-16 (OQ-S8): Notification channels for integrity violations — deployment-specific,
  not spec (§5 Category 2).
- GAP-17 (OQ-CW1): Voluntary Write Lock release / inter-agent negotiation — v2 only
  (§6 Category 3).
- GAP-18 (OQ-SL2): Multi-machine Ledger replication and distributed consensus — v2 only
  (§6 Category 3).
- GAP-19: Orchestrator signing key rotation — v2 only (§10.5, §6 Category 3).

The v1.1 spec's §19 v2 Scope Targets provides the starting list. This session
extends it — producing a structured v2 outline block for each gap that defines:
(a) what v2 must specify, (b) what v1 leaves as the boundary condition, (c) what
architectural decisions v2 must NOT reopen without a full council session.
───────────────────────────────────────────────────────────────────────────────

Gaps to resolve in this session:

GAP-13
Domain(s): Security (Warden), Orchestration Comparativist
Description: The Genesis security model for fully automated pipelines is deferred (OQ-S5).
v1 mandates human review of the Architect Agent output patch before write engine execution
(§10.6 step 1). The v2 target mentions "secondary LLM reviewer as human-review proxy" — but
no spec language defines: what properties this proxy must have; what its trust level would be
relative to the Warden's trust model; how it would be authorized.
Blocked by: v2 initiation + policy decision on whether an LLM reviewer can be granted
Warden-level trust for Genesis authorization.
Priority: Medium

GAP-16
Domain(s): Security (Warden), Orchestration Comparativist
Description: Notification channels for integrity violations are explicitly out-of-spec (OQ-S8,
§18.2 / §5 Category 2). The spec produces `INTEGRITY_VIOLATION` and
`INTEGRITY_VIOLATION_EMERGENCY` Ledger entries and triggers write suspension — but defines no
mechanism for alerting the human operator. In an unattended deployment, write suspension with
no human notification is a silent failure.
Blocked by: Operational environment decision (deployment-specific).
Priority: Low

GAP-17
Domain(s): Orchestration Comparativist, State Consistency Theorist
Description: Voluntary scope-lock release and inter-agent negotiation are deferred to v2
(OQ-CW1, §18.3). Currently: Write Lock TTL is 60 minutes with auto-release. No mechanism for
an agent to voluntarily release a lock before TTL expiry. No negotiation protocol for two
agents needing overlapping write regions — the spec simply rejects the second lock acquisition.
In high-throughput scenarios, this creates unnecessary sequentialization.
Blocked by: v2 initiation.
Priority: Low

GAP-18
Domain(s): State Consistency Theorist
Description: Multi-machine harness Ledger replication is deferred to v2 (OQ-SL2, §18.3). The
append-only JSONL Ledger with Merkle-chain-lite integrity is explicitly designed for
single-machine deployment. No replication protocol, consistency model for distributed Ledger
reads, or leader-election mechanism for multi-machine Orchestrators is outlined.
Blocked by: v2 initiation + distributed systems architecture decision.
Priority: Low

GAP-19
Domain(s): Security (Warden)
Description: Orchestrator signing key rotation is deferred to v2 (§10.5). The current
Orchestrator key is generated at first boot and never rotated in v1. The spec notes that "full
PKI" is v2 — but provides no outline of what a rotation event would require (re-signing all
active tokens? re-anchoring the public half in both Ledger and `.harness/`? invalidating
in-flight operations?). Without even an outline, v2 spec will need to re-examine every
component that binds on the Orchestrator key.
Blocked by: v2 initiation.
Priority: Low

Relevant context from v1.1 spec:

§5 — Category 2: Out-of-Scope Operational Assumptions
"Notification infrastructure for integrity violations (OQ-S8 — deployment-specific)."

§6 — Category 3: Deferred to v2
"Full PKI: mass revocation lists, Orchestrator key rotation, multi-Orchestrator trust.
Delegation tokens for nested sub-agent invocations (Path B/C nested cases).
Multi-machine harness with Ledger replication and distributed consensus.
Voluntary Write Lock release and inter-agent negotiation (OQ-CW1).
Genesis security model for fully automated pipelines (OQ-S5)."

§10.5 — Orchestrator Signing Key
"Generated at first boot. Key rotation is v2 (Category 3)."

§10.6 — Genesis Security Protocol (step 1)
"Human review of Architect Agent output patch before write engine execution (mandatory in v1;
OQ-S5 fully-automated variant is v2)."

§16.7 — Ledger
"Append-only JSONL Ledger. Merkle-chain-lite integrity."

§17.2 — Write Lock
"60-minute TTL, auto-release. Scope: declared write region."

§19 — v2 Scope Targets
"Distributed trust: multi-machine harness with ledger replication and distributed consensus.
Key lifecycle management: Orchestrator key rotation. Agent-to-agent trust: peer agent review
delegation token design. Automation extensions: OQ-S5 resolution."

Invoke the framework-council skill. Convene the full council. Each gap requires input from the
specialists indicated. The output format for each gap is a v2 outline spec block (not a full
spec, not an implementation plan — a structured statement of v2 scope for that gap).

For each of the five gaps, produce a v2 outline spec block in this format:
  V2 OUTLINE — [GAP ID]: [short name]
  Primary domain(s): [which specialists own v2 work for this gap]
  What v2 MUST define:
    [itemized list of spec decisions v2 must make]
  What v1.1 leaves as the boundary:
    [what is already decided that v2 builds on — do not reopen]
  What v2 MUST NOT reopen without a full council session:
    [architectural decisions that are load-bearing and cannot be changed unilaterally]
  Trust or consistency constraints that carry into v2:
    [any v1 constraints that bound the v2 design space]

Council guidance per gap:

GAP-13 (Warden primary, Orchestration contributes):
- Warden: define the minimum property set a secondary LLM reviewer must satisfy to act as
  a human-review proxy for Genesis authorization. What does "Warden-level trust" require
  from an LLM? Can any LLM be granted this trust, or does it require attestation?
- Orchestration: define how this proxy would be invoked — does it get its own agent YAML
  and Write Scope Definition, or does it operate under a special Genesis-proxy token type?

GAP-16 (Warden primary, Orchestration contributes):
- Define the interface contract the notification subsystem must satisfy: inputs are
  `INTEGRITY_VIOLATION` and `INTEGRITY_VIOLATION_EMERGENCY` Ledger entries; the output is
  an operator-alerting signal. What guarantees must the notification subsystem provide
  (at-least-once delivery? latency SLA?). Mark channel selection as deployment-specific.

GAP-17 (Orchestration primary, State Consistency contributes):
- Orchestration: define the requirements a voluntary lock release ceremony must satisfy
  (atomicity with Lock Registry update, safety for in-progress operations referencing
  the lock). Define the requirements for an inter-agent write region negotiation protocol.
- State Consistency: define what the consistency model must guarantee during a negotiated
  lock handoff — does the Dependency Hold transfer, or is it re-declared?

GAP-18 (State Consistency primary):
- Define the consistency model requirements for a distributed Ledger: must reads be
  linearizable, or is eventual consistency acceptable for some entry types? Define leader-
  election requirements. Flag explicitly: Merkle-chain-lite as designed is single-machine-only.
  What changes in the chain integrity model for a replicated Ledger?

GAP-19 (Warden primary):
- Define what a key rotation event must guarantee: active token validity window (are tokens
  issued under the old key honored during a grace period?), in-flight operation safety (what
  happens to a PREPARED transaction whose token was issued under the old key?), public-key
  re-anchoring ceremony (both Ledger and `.harness/` copies). Flag all components that bind
  on the Orchestrator key — they must each define their key-rotation behavior.

At the end of the session, generate a Gap Session Summary Block:

GAPS RESOLVED: [list with resolution]
GAPS PARTIALLY RESOLVED: [list with what remains]
GAPS DEFERRED: [list with reason]
NEW GAPS SURFACED: [any that emerged during the session]
NEW TENSIONS SURFACED: [any cross-domain conflicts that appeared]
```

---

*Gap Session Starter Prompts — 8 sessions, all prompts populated*
*Source: gap-backlog-v1.md + llm-as-database-v1_1-integrated-spec.md + gap-session-schedule-v1.md*
*Note: v1.1 status of each gap reflected accurately as of the Interface Contract Review Session*
